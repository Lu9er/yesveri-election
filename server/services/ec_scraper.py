"""
EC Data Scraper — ingests official results from ec.or.ug.

Known URL patterns (based on 2021):
  - /ecresults/{year}/Summary_PRESIDENT_FINAL_{year}.pdf
  - /ecresults/{year}/District_Summary_PRESIDENT_FINAL_{year}.pdf
  - /ecresults/{year}/MPS_RESULTS_{year}.pdf
  - /ecresults/{year}/ (HTML index with links to CSV/PDF)

The EC site uses Cloudflare and is frequently unreachable. The scraper
retries gracefully and falls back to seed data when the site is down.
"""

import hashlib
import re
from datetime import datetime
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from server.models.database import ElectionResult, OfficialSource


# Known EC results page patterns
EC_RESULTS_PATHS = [
    "/ecresults/2026/",
    "/ecresults/2026/presidential.html",
    "/ecresults/2026/parliamentary.html",
    "/election/results",
    "/election/results/2026",
]


class ECDataScraper:
    def __init__(self, base_url: str = "https://www.ec.or.ug"):
        self.base_url = base_url.rstrip("/")
        self.client_headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Yesveri/1.0; +https://yesveri.online)",
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
        }

    async def scrape_and_store(self, db: AsyncSession) -> int:
        """
        Attempt to scrape EC website for election results.
        Returns number of new/updated records, or 0 if site is unreachable.
        """
        total_stored = 0

        # Try each known results path
        for path in EC_RESULTS_PATHS:
            url = f"{self.base_url}{path}"
            html = await self.fetch_page(url)
            if html is None:
                continue

            print(f"EC scraper: fetched {url} ({len(html)} bytes)")

            # Parse results from the HTML
            results = self.parse_results_page(html, url)
            if not results:
                # Try to find links to more result pages
                links = self.extract_result_links(html)
                for link in links:
                    sub_html = await self.fetch_page(link)
                    if sub_html:
                        results.extend(self.parse_results_page(sub_html, link))

            if results:
                stored = await self.store_results(db, results, url)
                total_stored += stored

        if total_stored > 0:
            print(f"EC scraper: stored {total_stored} new results")
        else:
            print("EC scraper: no new results found (site may be down)")

        return total_stored

    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page from the EC website with retry."""
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(
                    timeout=30,
                    follow_redirects=True,
                ) as client:
                    resp = await client.get(url, headers=self.client_headers)
                    resp.raise_for_status()
                    return resp.text
            except (httpx.HTTPError, httpx.ConnectError, httpx.TimeoutException) as e:
                print(f"EC scraper: failed to fetch {url} (attempt {attempt + 1}): {e}")
        return None

    def parse_results_page(self, html: str, source_url: str) -> list[dict]:
        """
        Parse election results from an EC HTML page.
        Looks for HTML tables with candidate names, vote counts, etc.
        """
        soup = BeautifulSoup(html, "html.parser")
        results = []

        # Find all tables on the page
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            if len(rows) < 2:
                continue

            # Try to identify header row
            headers = []
            header_row = rows[0]
            for th in header_row.find_all(["th", "td"]):
                headers.append(th.get_text(strip=True).lower())

            if not headers:
                continue

            # Look for columns that indicate election data
            candidate_col = self._find_column(headers, ["candidate", "name", "contestant"])
            votes_col = self._find_column(headers, ["votes", "vote count", "total votes", "valid votes"])
            party_col = self._find_column(headers, ["party", "political party", "organisation"])
            pct_col = self._find_column(headers, ["percentage", "%", "percent", "pct"])
            district_col = self._find_column(headers, ["district", "constituency", "area"])

            if candidate_col is None or votes_col is None:
                continue

            # Determine election level from page context
            page_text = soup.get_text().lower()
            if "president" in page_text:
                election_level = "presidential"
                position = "President"
            elif "parliament" in page_text or "member of parliament" in page_text:
                election_level = "parliamentary"
                position = "Member of Parliament"
            else:
                election_level = "unknown"
                position = "Unknown"

            # Parse data rows
            for row in rows[1:]:
                cells = row.find_all(["td", "th"])
                if len(cells) <= max(candidate_col, votes_col):
                    continue

                candidate = cells[candidate_col].get_text(strip=True)
                votes_text = cells[votes_col].get_text(strip=True)

                # Clean vote count
                votes = self._parse_number(votes_text)
                if votes is None or not candidate:
                    continue

                result = {
                    "candidate_name": candidate,
                    "vote_count": votes,
                    "election_level": election_level,
                    "position": position,
                    "election_year": 2026,
                    "source_url": source_url,
                }

                if party_col is not None and party_col < len(cells):
                    result["party"] = cells[party_col].get_text(strip=True)

                if pct_col is not None and pct_col < len(cells):
                    pct = self._parse_float(cells[pct_col].get_text(strip=True))
                    if pct is not None:
                        result["percentage"] = pct

                if district_col is not None and district_col < len(cells):
                    result["district"] = cells[district_col].get_text(strip=True)
                else:
                    # Try to infer district from page title or heading
                    title = soup.find("h1") or soup.find("h2")
                    if title:
                        result["district"] = title.get_text(strip=True)
                    else:
                        result["district"] = "National"

                results.append(result)

        return results

    def extract_result_links(self, html: str) -> list[str]:
        """Extract links to other result pages from an index page."""
        soup = BeautifulSoup(html, "html.parser")
        links = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True).lower()
            # Look for links that likely point to results
            if any(kw in text for kw in ["result", "presidential", "parliamentary", "district"]):
                if href.startswith("http"):
                    links.append(href)
                elif href.startswith("/"):
                    links.append(f"{self.base_url}{href}")
                else:
                    links.append(f"{self.base_url}/ecresults/2026/{href}")
        return links

    async def store_results(self, db: AsyncSession, results: list[dict], source_url: str) -> int:
        """Store parsed results in the database, avoiding duplicates."""
        if not results:
            return 0

        # Get or create source
        content_hash = hashlib.sha256(str(results).encode()).hexdigest()[:16]
        source_query = await db.execute(
            select(OfficialSource).where(OfficialSource.url == source_url)
        )
        source = source_query.scalar()

        if source and source.content_hash == f"scraped_{content_hash}":
            # Same data already stored
            return 0

        if source:
            source.content_hash = f"scraped_{content_hash}"
            source.last_scraped = datetime.utcnow()
        else:
            source = OfficialSource(
                name="Uganda Electoral Commission",
                url=source_url,
                description=f"Scraped from {source_url}",
                content_hash=f"scraped_{content_hash}",
                last_scraped=datetime.utcnow(),
            )
            db.add(source)
            await db.flush()

        stored = 0
        for r in results:
            # Check for duplicate
            existing = await db.execute(
                select(ElectionResult).where(
                    ElectionResult.candidate_name == r["candidate_name"],
                    ElectionResult.district == r.get("district", "National"),
                    ElectionResult.election_year == r["election_year"],
                    ElectionResult.election_level == r["election_level"],
                )
            )
            if existing.scalar() is not None:
                continue

            record = ElectionResult(
                source_id=source.id,
                election_level=r["election_level"],
                election_year=r["election_year"],
                district=r.get("district", "National"),
                constituency=r.get("constituency"),
                position=r["position"],
                candidate_name=r["candidate_name"],
                party=r.get("party"),
                vote_count=r["vote_count"],
                percentage=r.get("percentage"),
                total_valid_votes=r.get("total_valid_votes"),
                is_winner=r.get("is_winner", 0),
            )
            db.add(record)
            stored += 1

        if stored > 0:
            await db.commit()

        return stored

    def _find_column(self, headers: list[str], keywords: list[str]) -> Optional[int]:
        """Find the index of a column matching any keyword."""
        for i, h in enumerate(headers):
            for kw in keywords:
                if kw in h:
                    return i
        return None

    def _parse_number(self, text: str) -> Optional[int]:
        """Parse a number from text, handling commas and spaces."""
        cleaned = re.sub(r"[,\s]", "", text)
        try:
            return int(cleaned)
        except ValueError:
            return None

    def _parse_float(self, text: str) -> Optional[float]:
        """Parse a float from text, handling % signs."""
        cleaned = re.sub(r"[%,\s]", "", text)
        try:
            return float(cleaned)
        except ValueError:
            return None
