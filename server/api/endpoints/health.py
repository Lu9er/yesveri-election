from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from server.config import Settings
from server.db.session import get_db
from server.models.database import ElectionResult
from server.models.schemas import HealthResponse
from server.services.cache_service import CacheService

router = APIRouter()
settings = Settings()


@router.get("/health", response_model=HealthResponse)
async def health_check(db: AsyncSession = Depends(get_db)):
    # Check database
    db_ok = True
    total_results = 0
    ec_last_updated = None
    try:
        row = await db.execute(
            select(
                func.count(ElectionResult.id),
                func.max(ElectionResult.last_updated),
            )
        )
        result = row.one()
        total_results = result[0] or 0
        ec_last_updated = result[1]
    except Exception:
        db_ok = False

    # Check Redis
    cache = CacheService(settings.redis_url)
    redis_ok = await cache.is_healthy()

    status = "healthy" if db_ok else "degraded"

    return HealthResponse(
        status=status,
        database=db_ok,
        redis=redis_ok,
        ec_data_last_updated=ec_last_updated,
        total_official_results=total_results,
    )
