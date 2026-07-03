# EduOS — CasaOS Edition

A glassmorphic educational desktop OS built with **Reflex (Python)** and managed as a **CasaOS Custom App**.

---

## Architecture

```
CasaOS Dashboard (host layer)
    └── EduOS Custom App (Docker container)
            ├── Reflex Frontend  → port 3000  (Next.js)
            └── Reflex Backend   → port 8000  (FastAPI)
```

## Quick Start (Self-Hosted)

### Option A — Run directly with Docker Compose
```bash
# 1. Create persistent data folders
mkdir -p ~/casaos/eduos/study_materials ~/casaos/eduos/notes

# 2. Pull and run
docker compose up -d

# 3. Open browser → http://localhost:3000
```

### Option B — Install via CasaOS Custom App
1. Open **CasaOS Dashboard → App Store → Custom Install**
2. Click **Import** and paste the contents of `docker-compose.yml`
3. Click **Install**
4. Click the **EduOS** tile — it opens on port **3000**

---

## Persistent Study Data

| Local path (on your machine)             | Inside container              | Purpose                        |
|------------------------------------------|-------------------------------|-------------------------------|
| `~/casaos/eduos/study_materials/`        | `/app/data/study_materials/`  | PDFs, course modules, slides  |
| `~/casaos/eduos/notes/`                  | `/app/data/notes/`            | Notepad files                 |

Upload files via **CasaOS Files app** → they instantly appear inside the Reflex app.

---

## CI/CD — GitHub Container Registry

Every `git push` to `main` triggers `.github/workflows/build-push.yml` which:
1. Builds the Docker image
2. Pushes it to `ghcr.io/p7266473-max/edu_os:latest` (free, no credit card)

CasaOS will pull the new image on next container restart.

---

## Local Development
```bash
pip install -r requirements.txt
reflex run
# open http://localhost:3000
```
