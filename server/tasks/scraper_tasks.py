import asyncio

from server.tasks.celery_app import celery_app


@celery_app.task(name="server.tasks.scraper_tasks.refresh_ec_data")
def refresh_ec_data():
    """Refresh EC data from official sources (runs every 6 hours via Celery beat)."""
    asyncio.run(_refresh())


async def _refresh():
    from server.config import Settings
    from server.db.session import AsyncSessionLocal
    from server.services.ec_scraper import ECDataScraper

    settings = Settings()
    async with AsyncSessionLocal() as db:
        scraper = ECDataScraper(base_url=settings.ec_base_url)
        count = await scraper.scrape_and_store(db)
        if count > 0:
            print(f"EC scraper task: stored {count} new records from ec.or.ug")
        else:
            print("EC scraper task: no new data (site may be unreachable)")
