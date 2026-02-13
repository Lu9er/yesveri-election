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
        # If model not downloaded, use blank English model
        print("WARNING: en_core_web_sm not found, using blank model. Run: python -m spacy download en_core_web_sm")
        app.state.nlp = spacy.blank("en")

    yield
    # Shutdown: cleanup


app = FastAPI(
    title="Yesveri Election Verification",
    description="Verify election claims against official Uganda Electoral Commission data",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
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
