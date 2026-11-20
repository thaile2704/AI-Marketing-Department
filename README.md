# AI Marketing Department

Hybrid multi-model, multi-company / multi-brand AI marketing platform. This repository is an **engineering MVP scaffold**, not a production-ready 56-agent autonomous service.

## Architecture
- FastAPI backend and PostgreSQL persistence
- LangGraph workflow boundary for controlled task orchestration
- OpenAI + Anthropic model gateway (provider selection by task tier)
- Agent registry: 1 Director + 10 department heads + 45 specialists = 56 logical roles
- Approval gates for externally visible or financially consequential actions
- Next.js dashboard shell
- n8n/MCP integration boundary (credentials and actual provider integrations are deployment-specific)

## Quick start
1. Copy `.env.example` to `.env`; add provider API keys.
2. `docker compose up --build`
3. API docs: http://localhost:8000/docs
4. Web shell: http://localhost:3000

The initial API persists tasks and approvals in PostgreSQL. LLM keys are optional for health checks and registry browsing; model-backed task execution requires a configured provider.

## Safety defaults
- Draft/research actions may run autonomously.
- Publishing, sending, ad spend changes, pricing changes, payments, deletion, and external customer communications require explicit approval and a separately configured integration.
- No credentials are committed. No live external actions are enabled by default.

## Claude Code
Open this folder in Claude Code and follow `.claude/CLAUDE.md`. The implementation backlog is in `docs/IMPLEMENTATION_BACKLOG.md`. Treat `docs/ARCHITECTURE.md`, `docs/DECISIONS.md`, schemas and tests as source of truth. Do not silently change approved architecture.

## Status
Implemented scaffold: API, PostgreSQL models, registry, model gateway adapters, approval endpoints, task workflow boundary, dashboard shell, Docker setup and tests. Remaining production work is explicitly listed in the backlog.
