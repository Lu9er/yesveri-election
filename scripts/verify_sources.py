#!/usr/bin/env python3
"""Verify all stored EC data snapshots."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func
from server.db.session import AsyncSessionLocal
from server.models.database import ElectionResult, OfficialSource


async def verify():
    async with AsyncSessionLocal() as db:
        # Get all sources
        sources = await db.execute(select(OfficialSource))
        source_list = sources.scalars().all()

        if not source_list:
            print("No sources found in database. Run seed_db.py first.")
            return

        print("=" * 70)
        print("YESVERI EC DATA SOURCE VERIFICATION")
        print("=" * 70)

        for source in source_list:
            # Count results for this source
            count_result = await db.execute(
                select(func.count(ElectionResult.id)).where(
                    ElectionResult.source_id == source.id
                )
            )
            count = count_result.scalar() or 0

            # Get distinct districts
            districts = await db.execute(
                select(func.count(ElectionResult.district.distinct())).where(
                    ElectionResult.source_id == source.id
                )
            )
            district_count = districts.scalar() or 0

            # Get distinct candidates
            candidates = await db.execute(
                select(func.count(ElectionResult.candidate_name.distinct())).where(
                    ElectionResult.source_id == source.id
                )
            )
            candidate_count = candidates.scalar() or 0

            print(f"\nSource: {source.name}")
            print(f"  URL:            {source.url or 'N/A'}")
            print(f"  Content Hash:   {source.content_hash or 'N/A'}")
            print(f"  Last Scraped:   {source.last_scraped or 'N/A'}")
            print(f"  Total Records:  {count}")
            print(f"  Districts:      {district_count}")
            print(f"  Candidates:     {candidate_count}")
            print(f"  Status:         {'OK' if count > 0 else 'EMPTY'}")

        # Summary
        total = await db.execute(select(func.count(ElectionResult.id)))
        total_count = total.scalar() or 0
        print(f"\n{'=' * 70}")
        print(f"TOTAL RECORDS: {total_count}")
        print(f"TOTAL SOURCES: {len(source_list)}")
        print(f"{'=' * 70}")


def main():
    asyncio.run(verify())


if __name__ == "__main__":
    main()
