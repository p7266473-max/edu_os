# ─────────────────────────────────────────────────────────────────────────────
# EduOS — Production Dockerfile
# Wraps the Reflex app for CasaOS Custom App deployment
# ─────────────────────────────────────────────────────────────────────────────

# Stage 1 — install Node (Reflex needs it to build the frontend)
FROM node:20-slim AS node-base

# Stage 2 — Python runtime + Reflex
FROM python:3.12-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        unzip \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy Node binary from node-base so Reflex can build the JS frontend
COPY --from=node-base /usr/local/bin/node /usr/local/bin/node
COPY --from=node-base /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

WORKDIR /app

# Install Python dependencies first (layer-cached)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Reflex project
COPY . .

# Persistent data directory (mounted by CasaOS / docker-compose volume)
RUN mkdir -p /app/data/study_materials /app/data/notes

# Expose Reflex ports:
#   3000 → Next.js frontend (served by Reflex)
#   8000 → FastAPI/Starlette backend
EXPOSE 3000 8000

# Production startup: Reflex compiles the frontend on first run,
# then serves both frontend and backend
CMD ["python", "-m", "reflex", "run", "--env", "prod", "--backend-host", "0.0.0.0"]
