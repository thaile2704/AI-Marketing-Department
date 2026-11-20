# GitHub Codespaces

1. Open the repository on GitHub.
2. Select **Code → Codespaces → Create codespace on `engineering/audit-and-foundation`**.
3. Wait for the dev container to build. The container forwards ports 3000, 8000, and 5432.
4. Configure local-only environment variables from `.env.example`; never commit `.env` or API keys.
5. Start services with `docker compose up --build` if the Codespace host supports Docker Compose. If the devcontainer is attached to the API service, use the repository's compose environment as documented by the Codespaces terminal.
6. Verify `http://localhost:8000/api/v1/health`, `http://localhost:8000/docs`, and the forwarded frontend port.

Codespaces configuration is a development convenience, not proof that the application builds. Confirm the actual build and tests in the Codespaces terminal and CI.