import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from server.api.router import api_router
from server.config import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load spaCy model
    import spacy

    try:
        app.state.nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("WARNING: en_core_web_sm not found, using blank model. Run: python -m spacy download en_core_web_sm")
        app.state.nlp = spacy.blank("en")

    # Auto-create tables and seed on first startup
    try:
        from server.db.session import engine
        from server.models.database import Base

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables ensured.")

        # Auto-seed if empty or if seed data version has changed
        from sqlalchemy import select, func, delete
        from server.db.session import AsyncSessionLocal
        from server.models.database import ElectionResult, OfficialSource
        from server.db.seed import SEED_SOURCE, SEED_RESULTS

        async with AsyncSessionLocal() as db:
            # Check if current seed version matches
            existing_source = await db.execute(
                select(OfficialSource).where(OfficialSource.content_hash == SEED_SOURCE["content_hash"])
            )
            if existing_source.scalar() is not None:
                print("Database has current seed data, skipping seed.")
            else:
                # Clear old data and reseed
                await db.execute(delete(ElectionResult))
                await db.execute(delete(OfficialSource))
                await db.flush()

                source = OfficialSource(**SEED_SOURCE)
                db.add(source)
                await db.flush()
                for r in SEED_RESULTS:
                    db.add(ElectionResult(source_id=source.id, **r))
                await db.commit()
                print(f"Seeded {len(SEED_RESULTS)} election results (version: {SEED_SOURCE['content_hash']}).")
    except Exception as e:
        print(f"WARNING: Could not auto-setup database: {e}")
        print("The app will start but verification endpoints may not work until DB is ready.")

    yield
    # Shutdown


app = FastAPI(
    title="Yesveri Election Verification",
    description="Verify election claims against official Uganda Electoral Commission data",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow configured origins + any .pages.dev domain for Cloudflare
cors_origins = list(settings.cors_origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_origin_regex=r"https://(.*\.pages\.dev|(.+\.)?yesveri\.online)",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix="/api")

# Serve built frontend in production
dist_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist", "public")
if os.path.exists(dist_path):
    app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
