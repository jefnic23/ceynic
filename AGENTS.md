# Repository notes

- `frontend/` (SvelteKit) and `backend/` (FastAPI) are independent apps; run install and check commands from the relevant app directory, not the repository root. Frontend requires Node 22 (`engine-strict=true`); backend pins Python 3.11 in `.python-version`.
- Setup: `npm ci` in `frontend/`, `uv sync` in `backend/`. Local config goes in each app's `.env`; frontend builds need `PUBLIC_API_URL` (and CI supplies `PUBLIC_MEASUREMENT_ID` and `PUBLIC_RECAPTCHA_SITE_KEY`). Backend `src/config.py` requires more settings than just `DATABASE_URL`; importing the app initializes the database configuration.

## Checks and entrypoints

- Frontend: `npm run dev`; verify with `npm run check && npm run build` (CI order). `npm run lint` runs Prettier check and ESLint; there is no frontend test script.
- Backend: `uv run uvicorn src.main:app --reload`; verify with `uv run ruff check src alembic`. The backend pre-commit hooks also run `ruff-format`; no test suite is configured.
- API routers are registered in `backend/src/main.py`. SvelteKit storefront routes live under `frontend/src/routes/(ecomm)/` (route group, not a URL segment); `/admin` authentication and token refresh run through `frontend/src/hooks.server.ts` and `$lib/server/auth.ts`.

## Cross-app changes and database

- Backend classes decorated with `@frontend` generate `frontend/src/lib/schemas/*.json` and `frontend/src/lib/interfaces/*.d.ts`. After changing one, install both apps, run `uv run ceynic generate-frontend-models` from `backend/`, and include the generated changes. The generator needs `frontend/node_modules/.bin/json2ts`.
- SQLModel table metadata depends on `backend/src/models/registry.py`; add new mapped tables there for Alembic autogeneration. Migrations are explicit (`uv run alembic revision --autogenerate -m "..."`, review the revision, then `uv run alembic upgrade head`), not run at API startup. For an existing database, read `backend/README.md` before stamping the audited baseline; never assume it matches.
- The workflow in `.github/workflows/deploy.yml` checks both apps on `develop`, `staging`, and `main`, but deploys only on pushes to `staging`. It deploys the backend before the frontend; the backend `Procfile` runs `alembic upgrade head` on release.
