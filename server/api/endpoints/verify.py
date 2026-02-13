import hashlib
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from server.config import Settings
from server.db.session import get_db
from server.models.database import ClaimVerification
from server.models.schemas import (
    ExtractedFields,
    ImageVerificationResponse,
    OfficialDataResponse,
    SourceReferenceResponse,
    TextVerifyRequest,
    VerificationResponse,
)
from server.services.deterministic_matcher import DeterministicMatcher
from server.services.entity_extractor import EntityExtractor
from server.services.explanation_generator import ExplanationGenerator
from server.services.ocr_processor import OCRProcessor

router = APIRouter()
settings = Settings()


async def _verify_claim_text(
    claim_text: str,
    claim_type: str,
    request: Request,
    db: AsyncSession,
    extracted_text: str | None = None,
) -> dict:
    """Shared verification pipeline for text and image claims."""

    nlp = request.app.state.nlp

    # 1. Extract entities
    extractor = EntityExtractor(nlp)
    extracted = extractor.extract(claim_text)

    # 2. Match against official data
    matcher = DeterministicMatcher()
    match_result = await matcher.match(extracted, db)

    # 3. Generate explanation
    generator = ExplanationGenerator()
    explanation = generator.generate(
        match_result.alignment,
        extracted,
        match_result.official_result,
        match_result.conflicts,
    )

    # 4. Build response data
    official_data = None
    source_ref = None

    if match_result.official_result:
        r = match_result.official_result
        s = match_result.source

        official_data = OfficialDataResponse(
            candidate_name=r.candidate_name,
            party=r.party or "Independent",
            position=r.position,
            district=r.district,
            vote_count=r.vote_count,
            percentage=r.percentage or 0.0,
            total_votes=r.total_valid_votes or 0,
            source_name=s.name if s else "Uganda Electoral Commission",
            source_url=s.url if s else None,
            last_updated=r.last_updated or datetime.utcnow(),
        )

        source_ref = SourceReferenceResponse(
            name=s.name if s else "Uganda Electoral Commission",
            url=s.url if s else None,
            last_updated=s.last_scraped or r.last_updated or datetime.utcnow(),
        )

    # 5. Store verification record (auto-expires in 24h)
    now = datetime.utcnow()
    ip_hash = hashlib.sha256(
        (request.client.host or "unknown").encode()
    ).hexdigest()[:16]

    verification = ClaimVerification(
        claim_text=claim_text[:500],  # Truncate for privacy
        claim_type=claim_type,
        extracted_text=extracted_text,
        extracted_fields=extracted,
        matched_result_id=(
            match_result.official_result.id if match_result.official_result else None
        ),
        alignment_status=match_result.alignment.value,
        confidence=match_result.confidence,
        explanation=explanation,
        ip_hash=ip_hash,
        verified_at=now,
        expires_at=now + timedelta(hours=settings.claim_retention_hours),
    )
    db.add(verification)
    await db.commit()

    return {
        "alignment": match_result.alignment.value,
        "extracted_fields": ExtractedFields(**extracted),
        "official_data": official_data,
        "explanation": explanation,
        "confidence": match_result.confidence,
        "source_reference": source_ref,
        "verified_at": now,
        "extracted_text": extracted_text,
    }


@router.post("/verify/text", response_model=VerificationResponse)
async def verify_text_claim(
    body: TextVerifyRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await _verify_claim_text(
        claim_text=body.claim_text,
        claim_type="text",
        request=request,
        db=db,
    )
    return VerificationResponse(**{k: v for k, v in result.items() if k != "extracted_text"})


@router.post("/verify/image", response_model=ImageVerificationResponse)
async def verify_image_claim(
    request: Request,
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Validate file size
    contents = await image.read()
    max_bytes = settings.max_image_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"Image too large. Maximum size is {settings.max_image_size_mb}MB.",
        )

    # Validate content type
    content_type = image.content_type or ""
    if content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(
            status_code=400,
            detail="Invalid image format. Please upload JPG, PNG, or WebP.",
        )

    # OCR
    ocr = OCRProcessor(settings.tesseract_cmd)
    try:
        extracted_text = ocr.extract_text(contents)
    except Exception as e:
        raise HTTPException(
            status_code=422,
            detail=f"Could not extract text from image: {str(e)}",
        )

    if not extracted_text.strip():
        raise HTTPException(
            status_code=422,
            detail="No text could be extracted from the image. Try a clearer screenshot.",
        )

    # Image bytes are NOT stored — privacy requirement
    result = await _verify_claim_text(
        claim_text=extracted_text,
        claim_type="image",
        request=request,
        db=db,
        extracted_text=extracted_text,
    )

    return ImageVerificationResponse(**result)
