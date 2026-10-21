# ceynic

The [SvelteKit storefront](frontend/) and [FastAPI service](backend/) are separate applications in one repository. Run each command from its application's directory:

| App | Install | Develop | Check |
| --- | --- | --- | --- |
| `frontend/` | `npm ci` (Node 22) | `npm run dev` | `npm run check && npm run build` |
| `backend/` | `uv sync` (Python 3.11) | `uv run uvicorn src.main:app --reload` | `uv run ruff check src alembic` |

Put local configuration in `frontend/.env` (and, if needed, `frontend/.env.development`) and `backend/.env`. These files are ignored by Git. The frontend uses `PUBLIC_API_URL` to reach the backend; the backend reads `DATABASE_URL` and other settings from its environment. See [backend/README.md](backend/README.md) for database migration instructions.

To regenerate the frontend's JSON schemas and TypeScript interfaces after changing an exported backend model, install both applications and run `uv run ceynic generate-frontend-models` from `backend/`. Commit any generated changes in `frontend/src/lib/` alongside the backend change.

## Branches and deployments

Branch from `develop` for local work. Merge into `develop`, promote `develop` into `staging` for testing, then promote `staging` into `main` when ready. Do not develop directly on `staging` or `main`.

The [GitHub Actions workflow](.github/workflows/deploy.yml) checks both apps on pull requests targeting `develop`, `staging`, or `main`, and on pushes to those branches. After both checks pass on a push to `staging`, it deploys `backend/` to `ceynic-api-staging` (including its Alembic release command), then `frontend/` to `ceynic-staging`. Pull requests and pushes to `develop` or `main` do not deploy.

To enable staging deployments, add `HEROKU_API_KEY` and `HEROKU_EMAIL` (your Heroku account email) under GitHub **Settings → Secrets and variables → Actions → Repository secrets**. The workflow uses the Heroku CLI to push each application's subdirectory to its existing Heroku app. Configure each staging Heroku app's buildpack and config vars. In particular, `ceynic-staging` needs `PUBLIC_API_URL` pointing to the staging backend, plus its `PUBLIC_MEASUREMENT_ID` and `PUBLIC_RECAPTCHA_SITE_KEY`. The frontend check uses CI-only values; the deployed frontend is built by Heroku using its own app config vars. A push to `staging` starts the workflow automatically; see the **Actions** tab for the check and deploy jobs.

Production resources are not provisioned yet. `main` runs checks only; add production deployment after the frontend and backend Heroku apps and their config vars are ready. The original `ceynic-api` repository is retained as a historical archive, not a deployment source.
