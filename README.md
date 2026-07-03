# EduOS — CasaOS Master Interface

A glassmorphic educational OS built with **Reflex (Python)** and managed as a multi-service **CasaOS** stack.

---

## Architecture

```
CasaOS Dashboard  ←  Master Interface / host management layer
    │
    ├── eduos_app      (port 3000)  — Reflex Educational UI
    │       └── ghcr.io/p7266473-max/edu_os:latest
    │
    └── eduos_webtop   (port 3001)  — Ubuntu XFCE Virtual Desktop
            └── lscr.io/linuxserver/webtop:ubuntu-xfce

Shared Volume: ~/casaos/eduos/study_materials
    ↕ visible in both containers simultaneously
```

---

## Quick Start

```bash
# 1. Create persistent data folders
mkdir -p ~/casaos/eduos/study_materials ~/casaos/eduos/notes

# 2. Pull & start both services
docker compose pull
docker compose up -d

# 3. Open in browser
#    EduOS UI      → http://localhost:3000
#    Linux Desktop → http://localhost:3001  (user: edu_user / pass: eduos2024)
```

### Install via CasaOS Custom App
1. **CasaOS Dashboard → App Store → Custom Install → Import**
2. Paste `docker-compose.yml` → **Install**
3. Two tiles appear: **EduOS** and **EduOS Desktop**

---

## Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| EduOS (Reflex) | `ghcr.io/p7266473-max/edu_os:latest` | 3000 | Educational desktop UI |
| Webtop (XFCE) | `lscr.io/linuxserver/webtop:ubuntu-xfce` | 3001 | Full Linux virtual desktop |

---

## Persistent Storage

| Host path | Container path | Used by |
|-----------|---------------|---------|
| `~/casaos/eduos/study_materials/` | `/app/data/study_materials` (EduOS) | Reflex app |
| `~/casaos/eduos/study_materials/` | `/config/Desktop/study_materials` (Webtop) | Linux desktop |
| `~/casaos/eduos/notes/` | `/app/data/notes` | EduOS Notepad |

Upload files via **CasaOS Files** → instantly available in both services.

---

## CI/CD — GitHub Actions → GHCR

Every `git push` to `main` (when app code changes) triggers the workflow:

```
push to main → GitHub Actions → docker build → ghcr.io/p7266473-max/edu_os:latest
                                                          ↓
                                              CasaOS: docker compose pull && up -d
```

Webtop is a **pre-built upstream image** — no build step needed.

---

## Local Development

```bash
pip install -r requirements.txt
reflex run
# → http://localhost:3000
```

## Change Webtop Password

Edit `docker-compose.yml` → `webtop` → `PASSWORD=your_new_password` → `docker compose up -d webtop`
