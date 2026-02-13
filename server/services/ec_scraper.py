"""
EC Data Scraper — for ingesting official Uganda Electoral Commission results.

In MVP mode this operates as a seed-data loader. When the actual EC publishes
machine-readable results, the scrape methods can be activated.
"""

from datetime import datetime
from typing import Optional

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database import ElectionResult, OfficialSource


class ECDataScraper:
    def __init__(self, base_url: str, use_seed_data: bool = True):
        self.base_url = base_url
        self.use_seed_data = use_seed_data

    async def scrape_and_store(self, db: AsyncSession) -> int:
        """
        Returns the number of new records stored.
        In seed mode this is a no-op (data is loaded via seed.py).
        """
        if self.use_seed_data:
            return 0

        # Placeholder for live scraping
        # When EC publishes results:
        # 1. Fetch the page at self.base_url/results
        # 2. Parse HTML/PDF
        # 3. Upsert into ElectionResult table
        return 0

    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page from the EC website."""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(
                    url,
                    headers={"User-Agent": "Yesveri Election Verifier/1.0"},
                )
                resp.raise_for_status()
                return resp.text
        except httpx.HTTPError:
            return None
