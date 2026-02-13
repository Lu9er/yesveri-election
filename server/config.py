from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/yesveri_election"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # EC Scraper
    ec_base_url: str = "https://www.ec.or.ug"
    ec_scrape_interval_hours: int = 6

    # Privacy
    claim_retention_hours: int = 24

    # OCR
    tesseract_cmd: str = "/usr/bin/tesseract"
    max_image_size_mb: int = 5

    # App — add your Cloudflare Pages domain here after deployment
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000", "https://*.pages.dev"]
    debug: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
