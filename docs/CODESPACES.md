# GitHub Codespaces

## Create the Codespace

1. Open this repository on GitHub.
2. Select **Code → Codespaces → Create codespace** and choose the branch you want to test (normally `main` or the active engineering branch).
3. The Dev Container attaches to the `web` service. This service is based on Node 22; the Dev Container Python feature adds Python 3.12 to the same workspace terminal.
4. Compose starts the `db`, `api`, and `web` services. Do not run `docker compose up` from inside the Codespaces terminal; the terminal is already inside the selected service container.
5. The post-create hook installs API Python dependencies and frontend npm dependencies.

## If the environment is missing Node or Python

After switching branches or changing `.devcontainer/devcontainer.json`, run **Ctrl+Shift+P → Codespaces: Rebuild Container**. A terminal restart is not enough: Dev Container features are installed during container creation.

Then verify:

```bash
node --version
npm --version
python --version
```

Expected major versions: Node 22, Python 3.12.

## Verify services

```bash
python -c "import socket; print('db resolves to', socket.gethostbyname('db'))"
curl -fsS http://localhost:8000/health
```

Open forwarded port 3000 for the dashboard and port 8000 for the FastAPI service. PostgreSQL is an internal Compose service; use the API connection string rather than installing PostgreSQL tools in the workspace container.

## Environment and secrets

Compose supplies safe local development defaults. Optional provider credentials can be placed in a local, untracked `.env` file using `.env.example` as a reference. Never commit `.env` or production credentials.

Codespaces configuration is a development convenience, not proof that the application is production-ready. CI and the remaining security release gates must pass before deployment.
