# ceynic

The [SvelteKit storefront](frontend/) and [FastAPI service](backend/) are separate applications in one repository. Run each command from its application's directory:

| App | Install | Develop | Check |
| --- | --- | --- | --- |
| `frontend/` | `npm ci` (Node 22) | `npm run dev` | `npm run check && npm run build` |
| `backend/` | `uv sync` (Python 3.11) | `uv run uvicorn src.main:app --reload` | `uv run ruff check src alembic` |

Put local configuration in `frontend/.env` (and, if needed, `frontend/.env.development`) and `backend/.env`. These files are ignored by Git. The frontend uses `PUBLIC_API_URL` to reach the backend; the backend reads `DATABASE_URL` and other settings from its environment. See [backend/README.md](backend/README.md) for database migration instructions.

To regenerate the frontend's JSON schemas and TypeScript interfaces after changing an exported backend model, install both applications and run `uv run ceynic generate-frontend-models` from `backend/`. Commit any generated changes in `frontend/src/lib/` alongside the backend change.

## Branches and deployments

Branch from `develop` for local work. Merge into `develop`, promote `develop` into `staging` for testing, then promote `staging` into `main` for production. Do not develop directly on `staging` or `main`.

The [Heroku deployment workflow](.github/workflows/deploy.yml) checks both apps and deploys them independently on promotion to `staging`: `backend/` to `ceynic-api-staging` (including its Alembic release command) and `frontend/` to `ceynic-staging`. It needs a GitHub Actions repository secret named `HEROKU_API_KEY`. Each app retains its Heroku config vars and buildpack. `develop` does not deploy.

Production frontend is the existing `ceynic` Heroku app. No production backend app is currently available in the Heroku account; before enabling automated `main` deployment, identify its deployment target and configure it separately. Production remains on its current release until promotion is deliberately configured. The original `ceynic-api` repository is retained as a historical archive, not a deployment source.
