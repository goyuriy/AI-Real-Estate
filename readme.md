# SmplyHome

AI real estate chatbot that helps with title transactions.

## Features

- Task and transaction management for title workflows
- Admin backend for accounts, tasks, and transactions
- Docker support for deployment

## Tech stack

- **Backend:** Python 3.11, Django 4.1
- **Database:** PostgreSQL (production), SQLite (local dev)
- **Server:** Gunicorn
- **Deployment:** Docker (Alpine-based image)

## Prerequisites

- Python 3.11+
- PostgreSQL (for production)
- Docker (optional, for containerized run)

## Getting started

### Local development

1. Clone the repo and enter the project directory:
   ```bash
   git clone https://github.com/keyaidmin/SmplyHome.git && cd SmplyHome
   ```

2. Install dependencies (creates venv, installs requirements, sets up pre-commit):
   ```bash
   ./make.sh install
   source venv/bin/activate
   ```

3. Create a `.env` in the project root with at least:
   ```env
   DEBUG=True
   DOMAIN=localhost
   ```

4. Run the Django dev server:
   ```bash
   ./make.sh run-dev
   ```

The admin app is under `admin/`; use `admin/manage.py` for migrations and Django commands.

### Docker

Build and run with the project’s Dockerfile; the default `CMD` runs Gunicorn (see `make.sh run`). Set `HOST`, `PORT`, and any DB/env vars as needed for your environment.

## Project structure

- `admin/` — Django project (settings, apps: `accounts`, `task`, `transaction`, `filer`)
- `requirements.txt` / `requirements-dev.txt` — Python dependencies
- `make.sh` — Install, lint, test, run, and deploy commands
- `Dockerfile` — Production image (multi-stage, non-root user)

## License

See repository license file.
