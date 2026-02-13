import asyncio

from server.tasks.celery_app import celery_app


@celery_app.task(name="server.tasks.cleanup_tasks.cleanup_expired")
def cleanup_expired():
    """Delete expired claim verification records."""
    asyncio.run(_cleanup())


async def _cleanup():
    from server.db.session import AsyncSessionLocal
    from server.services.cleanup_service import CleanupService

    async with AsyncSessionLocal() as db:
        service = CleanupService()
        count = await service.delete_expired(db)
        print(f"Cleaned up {count} expired claim verifications")
