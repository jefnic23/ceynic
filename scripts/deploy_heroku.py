"""Deploy one monorepo app through Heroku's source/build API (no Git force-push)."""

import argparse
import io
import json
import os
import subprocess
import tarfile
import time
from urllib.request import Request, urlopen


def api(method: str, path: str, token: str, data: dict | None = None) -> dict:
    request = Request(
        f"https://api.heroku.com/apps/{path}",
        data=json.dumps(data).encode() if data is not None else None,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.heroku+json; version=3",
            "Content-Type": "application/json",
        },
        method=method,
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", choices=("frontend", "backend"))
    parser.add_argument("app", help="Existing Heroku application name")
    parser.add_argument("--dry-run", action="store_true", help="Validate the archive without deploying")
    args = parser.parse_args()

    # A tree archive contains only the chosen app, at the root Heroku expects.
    archive = subprocess.run(
        ["git", "archive", "--format=tar.gz", f"HEAD:{args.directory}"],
        check=True,
        capture_output=True,
    ).stdout
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as tar:
        names = set(tar.getnames())
    required = "package.json" if args.directory == "frontend" else "Procfile"
    if required not in names:
        raise SystemExit(f"{args.directory} archive has no {required}")
    if args.dry_run:
        print(f"{args.directory}: {len(names)} files ready for {args.app}")
        return

    token = os.environ.get("HEROKU_API_KEY")
    if not token:
        raise SystemExit("HEROKU_API_KEY is required to deploy")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    source = api("POST", f"{args.app}/sources", token)["source_blob"]
    # The signed upload URL needs no Heroku authorization header.
    with urlopen(Request(source["put_url"], data=archive, method="PUT"), timeout=120):
        pass
    build = api(
        "POST",
        f"{args.app}/builds",
        token,
        {"source_blob": {"url": source["get_url"], "version": commit}},
    )
    print(f"Building {args.directory} at {commit} for {args.app} ({build['id']})", flush=True)
    release_id = None
    for _ in range(120):
        result = api("GET", f"{args.app}/builds/{build['id']}", token)
        if result["status"] == "succeeded":
            release_id = (result.get("release") or {}).get("id")
            if release_id:
                break
        if result["status"] == "failed":
            raise SystemExit(f"Heroku build failed for {args.app}: {build['output_stream_url']}")
        time.sleep(10)
    if not release_id:
        raise SystemExit(f"Timed out waiting for the {args.app} build/release: {build['output_stream_url']}")

    # The backend's Procfile runs Alembic in the release phase. A successful
    # build alone does not mean the new version (or migration) was released.
    for _ in range(120):
        release = api("GET", f"{args.app}/releases/{release_id}", token)
        if release["status"] == "succeeded":
            print(f"Released {args.app} at {commit}")
            return
        if release["status"] in ("failed", "expired"):
            raise SystemExit(f"Heroku release failed for {args.app}: {release['output_stream_url']}")
        time.sleep(10)
    raise SystemExit(f"Timed out waiting for the {args.app} release {release_id}")


if __name__ == "__main__":
    main()
