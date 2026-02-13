# Stage 1: Build frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install

COPY client/ client/
COPY attached_assets/ attached_assets/
COPY vite.config.ts tsconfig.json tailwind.config.ts postcss.config.js components.json ./
RUN npm run build


# Stage 2: Python runtime
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

# Copy backend code
COPY server/ server/
COPY scripts/ scripts/
COPY alembic.ini .

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/dist/public dist/public

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
