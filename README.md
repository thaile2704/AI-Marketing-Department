# AI Marketing Department

Hybrid multi-model, multi-organization / multi-brand AI Marketing Operating System.

> **Current status: engineering MVP/scaffold — not production-ready.** The repository contains a logical 56-role registry, but not 56 fully executable agents.

## Product and architecture
- 1 AI Marketing Director + 10 Department Heads + 45 Specialists = 56 logical roles.
- FastAPI backend, PostgreSQL system of record, Next.js dashboard.
- LangGraph is the only agent workflow orchestrator.
- OpenAI + Anthropic through one model gateway.
- n8n/MCP are integration boundaries, not replacements for backend authorization.
- Human approval required for consequential external and financial actions.
- Strict organization/brand isolation is a production requirement.

## Documentation
Start with **[`docs/PROJECT_CONTEXT_FOR_CLAUDE.md`](docs/PROJECT_CONTEXT_FOR_CLAUDE.md)** for the complete project handoff and Claude Code context.

Additional focused documents:
- `docs/ARCHITECTURE.md` — approved technical architecture.
- `docs/DECISIONS.md` — architecture decision records.
- `docs/AGENT_SPECIFICATION.md` — role and executable-agent contract.
- `docs/IMPLEMENTATION_BACKLOG.md` — phased implementation and acceptance gates.
- `docs/SECURITY_RELEASE_GATES.md` — mandatory production security requirements.
- `.claude/CLAUDE.md` — Claude Code engineering rules.

## Safety
No production credentials or live external actions are enabled by default. Publishing, customer messaging, paid media changes, pricing, payments, deletion, and sensitive exports require explicit approval and a separately authorized executor.

## Development
See `docs/PROJECT_CONTEXT_FOR_CLAUDE.md` and `docs/CODESPACES.md` for environment setup and verification. Do not claim Codespaces or production readiness until actual runtime checks and CI pass.
