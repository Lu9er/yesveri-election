from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Requests ──────────────────────────────────────────────────────────────


class TextVerifyRequest(BaseModel):
    claim_text: str = Field(..., min_length=1, max_length=1000)


# ── Response sub-models ───────────────────────────────────────────────────


class ExtractedFields(BaseModel):
    candidate_name: Optional[str] = None
    party: Optional[str] = None
    position: Optional[str] = None
    district: Optional[str] = None
    vote_count: Optional[int] = None
    percentage: Optional[float] = None
    result_claim: Optional[str] = None


class OfficialDataResponse(BaseModel):
    candidate_name: str
    party: str
    position: str
    district: str
    vote_count: int
    percentage: float
    total_votes: int
    source_name: str
    source_url: Optional[str] = None
    last_updated: datetime


class SourceReferenceResponse(BaseModel):
    name: str
    url: Optional[str] = None
    last_updated: datetime


# ── Main responses ────────────────────────────────────────────────────────


class VerificationResponse(BaseModel):
    alignment: str
    extracted_fields: ExtractedFields
    official_data: Optional[OfficialDataResponse] = None
    explanation: str
    confidence: float
    source_reference: Optional[SourceReferenceResponse] = None
    verified_at: datetime


class ImageVerificationResponse(VerificationResponse):
    extracted_text: str


# ── Other endpoints ───────────────────────────────────────────────────────


class SourceListItem(BaseModel):
    id: int
    name: str
    url: Optional[str] = None
    description: Optional[str] = None
    last_scraped: Optional[datetime] = None
    result_count: int


class HealthResponse(BaseModel):
    status: str
    database: bool
    redis: bool
    ec_data_last_updated: Optional[datetime] = None
    total_official_results: int
