from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.db.session import get_db
from server.models.database import ElectionResult, OfficialSource
from server.models.schemas import SourceListItem

router = APIRouter()


@router.get("/sources", response_model=list[SourceListItem])
async def list_sources(db: AsyncSession = Depends(get_db)):
    """List all available official EC data sources."""
    query = (
        select(
            OfficialSource.id,
            OfficialSource.name,
            OfficialSource.url,
            OfficialSource.description,
            OfficialSource.last_scraped,
            func.count(ElectionResult.id).label("result_count"),
        )
        .outerjoin(ElectionResult, ElectionResult.source_id == OfficialSource.id)
        .group_by(OfficialSource.id)
    )

    rows = await db.execute(query)
    results = rows.all()

    return [
        SourceListItem(
            id=row.id,
            name=row.name,
            url=row.url,
            description=row.description,
            last_scraped=row.last_scraped,
            result_count=row.result_count,
        )
        for row in results
    ]
