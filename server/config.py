from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database — Render provides DATABASE_URL automatically
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/yesveri_election"

    # Redis — optional, app works without it
    redis_url: str = "redis://localhost:6379/0"

    # EC Scraper
    ec_base_url: str = "https://www.ec.or.ug"
    ec_scrape_interval_hours: int = 6

    # Privacy
    claim_retention_hours: int = 24

    # OCR
    tesseract_cmd: str = "/usr/bin/tesseract"
    max_image_size_mb: int = 5

    # App — CORS origins (comma-separated in env, or JSON list)
    cors_origins: list[str] = [
        "https://yesveri.online",
        "https://www.yesveri.online",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    debug: bool = False

    # Port — Render sets this automatically
    port: int = 8000

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
