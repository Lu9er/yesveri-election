import asyncio

from server.tasks.celery_app import celery_app


@celery_app.task(name="server.tasks.scraper_tasks.refresh_ec_data")
def refresh_ec_data():
    """Refresh EC data from official sources."""
    asyncio.run(_refresh())


async def _refresh():
    from server.config import Settings
    from server.db.session import AsyncSessionLocal
    from server.services.ec_scraper import ECDataScraper

    settings = Settings()
    async with AsyncSessionLocal() as db:
        scraper = ECDataScraper(settings.ec_base_url)
        count = await scraper.scrape_and_store(db)
        print(f"Refreshed {count} EC records")
