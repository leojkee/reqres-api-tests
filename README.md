# reqres-api-tests

API test automation framework for [DummyJSON](https://dummyjson.com) — built as a portfolio/demo project.

Covers auth, users, and products. Architecture mirrors production-grade frameworks: layered clients, encrypted test data in PostgreSQL, MFA support, Allure reporting.

## Stack

Python 3.12+, pytest, allure-pytest, requests, pydantic v2, SQLAlchemy 2.0, alembic, psycopg2, cryptography, pyotp, pytest-xdist

## Architecture

```
Tests → Steps → ApiFacade → API Clients → BaseClient → HTTP
```

- `api/` — HTTP clients, one class per domain (`AuthApi`, `UsersApi`, `ProductsApi`). Every method is wrapped with `@api_logger` which attaches request/response HTML to Allure.
- `api/api_facade.py` — single entry point, lazy-loads clients via `@property`. `AdminApiFacade` is a separate facade for admin credentials.
- `steps/` — orchestration layer. Each function runs a multi-step flow, validates responses with Pydantic and returns a `results` dict.
- `model/` — Pydantic v2 request/response schemas.
- `wrappers/` — `@api_logger` and `@step` decorators. Sensitive params (password, token) are masked in logs and Allure.
- `infrastructure/db/` — SQLAlchemy models + repositories. Test users stored with Fernet-encrypted passwords and MFA secrets.
- `mfa/` — TOTP via pyotp (GoogleAuthClient). Follows the same interface pattern as the production framework.
- `fixtures/` — pytest fixtures split by concern: `api_fixtures`, `db_fixture`, `mfa_fixtures`, `allure_hooks`.
- `data/` — random data generators (email, string, job title).
- `scripts/seed_data.py` — seeds test users into DB.

## Setup

**1. Generate encryption key**
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

**2. Create `.env`** (copy from `.env.example`, paste the key above into `ENCRYPTION_KEY`)

**3. Start PostgreSQL**
```bash
docker-compose up -d
```

**4. Run migrations and seed**
```bash
alembic upgrade head
python scripts/seed_data.py
```

**5. Install deps**
```bash
pip install -r requirements.txt
```

## Running tests

```bash
pytest -m smoke               # 7 tests, ~15s
pytest -m regression          # 26 tests, ~30s
pytest -m regression -n auto  # parallel
```

## Test markers

- `smoke` — critical subset
- `regression` — full suite
- `transaction` — tests that mutate real state (use carefully)
- `exclude` — skipped in CI

## CI

GitLab CI: `setup` (install + migrate + seed) → `test` (pytest with `$MARKERS`). Allure artifacts kept 1 day. Requires `ENCRYPTION_KEY` as CI variable.
