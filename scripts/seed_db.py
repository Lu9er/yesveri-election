#!/usr/bin/env python3
"""Seed the database with Uganda election data."""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, func, delete
from server.db.session import AsyncSessionLocal, engine
from server.models.database import Base, ElectionResult, OfficialSource
from server.db.seed import SEED_SOURCE, SEED_RESULTS


async def seed(force: bool = False):
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Check if already seeded
        count = await db.execute(select(func.count(ElectionResult.id)))
        existing = count.scalar() or 0

        if existing > 0 and not force:
            print(f"Database already has {existing} election results. Use --force to reseed.")
            return

        if existing > 0 and force:
            print(f"Clearing {existing} existing election results...")
            await db.execute(delete(ElectionResult))
            await db.execute(delete(OfficialSource))
            await db.flush()

        # Create source
        source = OfficialSource(**SEED_SOURCE)
        db.add(source)
        await db.flush()

        # Create election results
        for result_data in SEED_RESULTS:
            result = ElectionResult(source_id=source.id, **result_data)
            db.add(result)

        await db.commit()
        print(f"Seeded {len(SEED_RESULTS)} election results from {SEED_SOURCE['name']}")


def main():
    force = "--force" in sys.argv
    asyncio.run(seed(force=force))


if __name__ == "__main__":
    main()
