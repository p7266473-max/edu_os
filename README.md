# EduOS — CasaOS Master Interface

A glassmorphic educational OS built with **Reflex (Python)**, unified with an **Ubuntu XFCE virtual desktop**, managed as a professional multi-service **CasaOS** stack.

---

## Architecture

```
CasaOS Dashboard  ←  Master Interface
    │
    ├── eduos_app    (port 3000)  ─── Reflex Educational UI
    │       image: ghcr.io/p7266473-max/edu_os:latest
    │       api:   http://eduos_app:8000  (internal)
    │
    └── eduos_webtop (port 3001)  ─── Ubuntu XFCE Virtual Desktop
            image: lscr.io/linuxserver/webtop:ubuntu-xfce
            knows EduOS at: $EDUOS_API / $EDUOS_FRONTEND

Internal network: eduos_net
Shared volume:    ~/casaos/eduos/study_materials  (visible in BOTH services)
```

---

## Quick Start

```bash
# 1. Create data folders
mkdir -p ~/casaos/eduos/study_materials ~/casaos/eduos/notes

# 2. Configure environment (optional)
cp .env.example .env
nano .env   # set TZ, PASSWORD, etc.

# 3. Pull and start
docker compose pull
docker compose up -d

# EduOS UI      → http://localhost:3000
# Linux Desktop → http://localhost:3001  (edu_user / eduos2024)
```

---

## CasaOS Custom Install (Step-by-Step)

> Do this once — both services become permanent clickable icons on your dashboard.

1. Open **CasaOS Dashboard**
2. Click **App Store** (grid icon, top right)
3. Click **⊕ Custom Install** (top right of App Store)
4. Click **Import** and paste the contents of `docker-compose.yml`
5. Click **Install**
6. ✅ Two tiles appear on your dashboard:
   - **EduOS** — click → opens Reflex UI on port 3000
   - **EduOS Desktop** — click → opens Ubuntu XFCE on port 3001

To update after a `git push`:
```bash
docker compose pull eduos && docker compose up -d eduos
# Webtop stays live — it is not rebuilt by CI
```

---

## Cross-Service Communication

The Webtop container has these environment variables pre-set so you can interact with the EduOS backend **from inside the Linux desktop terminal**:

```bash
# Open a terminal in the Webtop desktop and run:

# Query EduOS kernel state (JSON)
curl $EDUOS_API/api/state | python3 -m json.tool

# Open EduOS UI in the desktop browser
xdg-open $EDUOS_FRONTEND

# List study materials
ls /config/Desktop/study_materials/
```

---

## Persistent Storage

| Host path | EduOS path | Webtop path | Purpose |
|-----------|-----------|------------|---------|
| `~/casaos/eduos/study_materials/` | `/app/data/study_materials` | `/config/Desktop/study_materials` | PDFs, course files |
| `~/casaos/eduos/notes/` | `/app/data/notes` | `/config/Desktop/notes` | Notepad files |
| *(Docker volume)* | `/app/.web` | — | Reflex build cache |
| *(Docker volume)* | — | `/config` | Webtop home dir |

Upload via **CasaOS Files** → instantly available in both services.

---

## CI/CD — GitHub Actions → GHCR

```
git push main
    → GitHub Actions (.github/workflows/build-push.yml)
        → docker build
        → push ghcr.io/p7266473-max/edu_os:latest
            → docker compose pull eduos && up -d   (on your host)
```

**Webtop is never rebuilt** — it's a pre-built LinuxServer image pulled directly.

---

## Local Development

```bash
pip install -r requirements.txt
reflex run
# → http://localhost:3000
```
