# Yesveri - Election Claim Verification

Compares election claims against official Uganda Electoral Commission data.

## What it does

- Extracts entities from claims (text or images)
- Checks against official EC announcements
- Shows match quality + source references
- Does NOT declare truth — shows alignment

## How it works

1. User submits claim (text or screenshot)
2. System extracts: candidates, votes, locations, percentages
3. Matches against EC snapshots (with source hashes)
4. Returns: alignment status + what we found + official record

## Alignment States

| Status | Meaning |
|--------|---------|
| MATCHES | Claim aligns with official EC data |
| CONFLICTS | Claim contradicts official EC data |
| NO_OFFICIAL_DATA | No EC announcement available yet |
| CANNOT_VERIFY | Insufficient info to extract verifiable claim |
| DATA_UPDATED | Official EC data changed since last check |

## Data sources

- Uganda Electoral Commission official results
- Stored with: URL + timestamp + content hash

## Privacy

- No storage of uploaded images
- Claims anonymized before logging
- Auto-delete after 24 hours
- No accounts, no tracking

## Tech stack

- **Backend**: FastAPI + PostgreSQL + Redis
- **OCR**: Tesseract
- **NLP**: spaCy
- **Frontend**: React + TypeScript + TailwindCSS + Shadcn/UI
- **Queue**: Celery (async processing)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 16
- Redis 7
- Tesseract OCR

### Development

```bash
# Install dependencies
npm install
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Set up database
createdb yesveri_election
python scripts/seed_db.py

# Start backend (terminal 1)
uvicorn server.main:app --reload --port 8000

# Start frontend (terminal 2)
npm run dev
```

### Docker

```bash
docker-compose up --build
# Then seed the database:
docker-compose exec app python scripts/seed_db.py
```

### Deploy to Railway

1. Push to GitHub
2. Connect repo to Railway
3. Add PostgreSQL and Redis services
4. Set environment variables from `.env.example`
5. Deploy

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/verify/text | Verify a text claim |
| POST | /api/verify/image | Verify an image (OCR + verify) |
| GET | /api/sources | List available EC data sources |
| GET | /api/health | System health check |

## License

MIT
