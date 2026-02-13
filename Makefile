.PHONY: dev dev-frontend dev-backend install seed migrate docker-up docker-down

# Development
dev: dev-backend dev-frontend

dev-frontend:
	npm run dev

dev-backend:
	uvicorn server.main:app --reload --host 0.0.0.0 --port 8000

install:
	npm install
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

# Database
seed:
	python scripts/seed_db.py

migrate:
	alembic upgrade head

# Docker
docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

# Build
build:
	npm run build
