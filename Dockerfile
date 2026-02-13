FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY server/ server/
COPY scripts/ scripts/
COPY data/ data/
COPY alembic.ini .

# Expose port (Render sets $PORT)
EXPOSE 8000

# Start — use $PORT if set (Render), otherwise 8000
CMD uvicorn server.main:app --host 0.0.0.0 --port ${PORT:-8000}
