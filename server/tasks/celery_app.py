from celery import Celery

from server.config import Settings

settings = Settings()

celery_app = Celery(
    "yesveri",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.beat_schedule = {
    "cleanup-expired-claims": {
        "task": "server.tasks.cleanup_tasks.cleanup_expired",
        "schedule": 3600.0,  # Every hour
    },
    "refresh-ec-data": {
        "task": "server.tasks.scraper_tasks.refresh_ec_data",
        "schedule": settings.ec_scrape_interval_hours * 3600,
    },
}
