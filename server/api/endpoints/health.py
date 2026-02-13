from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Simple health check that always returns 200.
    This must NOT depend on database or Redis — hosts use this to know
    if the process is alive. A failing health check = container restart loop.
    """
    return {"status": "ok"}


@router.get("/health/detailed")
async def detailed_health_check():
    """Full health check including database and Redis status."""
    from sqlalchemy import func, select

    from server.config import Settings
    from server.db.session import AsyncSessionLocal
    from server.models.database import ElectionResult
    from server.services.cache_service import CacheService

    settings = Settings()

    # Check database
    db_ok = True
    total_results = 0
    ec_last_updated = None
    try:
        async with AsyncSessionLocal() as db:
            row = await db.execute(
                select(
                    func.count(ElectionResult.id),
                    func.max(ElectionResult.last_updated),
                )
            )
            result = row.one()
            total_results = result[0] or 0
            ec_last_updated = str(result[1]) if result[1] else None
    except Exception as e:
        db_ok = False

    # Check Redis
    cache = CacheService(settings.redis_url)
    redis_ok = await cache.is_healthy()

    return {
        "status": "healthy" if db_ok else "degraded",
        "database": db_ok,
        "redis": redis_ok,
        "ec_data_last_updated": ec_last_updated,
        "total_official_results": total_results,
    }
