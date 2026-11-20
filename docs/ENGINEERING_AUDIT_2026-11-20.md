# Engineering Audit – 2026-11-20

Repository: `thaile2704/AI-Marketing-Department`  
Audited ref: `main` at `d2d716a1e3d7832f4c5c199fd1c0dbd8e0cd7284`  
Scope: source files and repository tree inspected through GitHub. No Codespaces shell/runtime was available during this audit.

## Executive result

The repository is a scaffold, not a production-ready multi-agent platform. The registry contains logical roles, while runtime orchestration is currently a deterministic single-node planning graph. No claim of production readiness or successful container execution is made.

## Confirmed findings

| Severity | Area | Evidence / impact |
|---|---|---|
| Critical | Authentication | API routes have no authentication dependency. Anyone able to reach the API can create/read tasks and decide approvals. |
| Critical | Tenant isolation | `GET /tasks` accepts caller-supplied `organization_id`; there is no authenticated membership check or database row-level security. Approval listing is global. |
| Critical | Approval integrity | Decision endpoint accepts caller-supplied `decided_by`; approval does not bind to a canonical payload hash/version and does not verify tenant membership. |
| High | Auditability | No append-only audit ledger for task/approval state changes or tool actions. |
| High | Schema lifecycle | Development startup calls `Base.metadata.create_all`; no Alembic migration directory/config was found in the audited tree. |
| High | Agent runtime | Workflow is one deterministic `classify_and_plan` node. It does not delegate to department heads or specialists. |
| High | Model gateway | Provider selected by one global setting; no per-task routing, retry/fallback, usage metering, or organization quotas. |
| Medium | Runtime verification | No container/Codespaces execution was possible from the GitHub connector; Docker build and browser behavior remain unverified. |
| Medium | Development environment | No `.devcontainer/devcontainer.json` or CI workflow existed in the audited tree. |

## Corrections to earlier conversational audit

- `.claude/CLAUDE.md` **does exist** in the audited tree and contains project engineering rules.
- `docs/CLAUDE_CODE_START_HERE.md` also exists.
- The earlier claim that the actual Claude instructions were under `claude/CLAUDE.md` was incorrect. The repository's canonical path is `.claude/CLAUDE.md`.

## Existing strengths

- Clear architecture decision: LangGraph is the only agent orchestrator; n8n is an integration layer.
- Explicit human-approval policy for consequential external actions.
- Registry separates logical agent roles from always-on processes.
- Existing FastAPI, SQLAlchemy async, PostgreSQL/pgvector Docker service, Next.js, and provider adapters provide a useful starting scaffold.

## Required release gates

1. OIDC authentication and server-derived user identity.
2. RBAC and organization/brand membership enforced on every read/write.
3. Database tenant isolation (prefer PostgreSQL RLS plus application checks).
4. Alembic migrations; production startup must never call `create_all`.
5. Approval records bind immutable canonical payload hash, version, tenant, action scope, expiry, and approver identity.
6. Append-only audit events with actor, tenant, target, action, timestamp, correlation ID, and outcome.
7. Security tests: unauthenticated access, cross-tenant reads/writes, stale approval, approval replay, forged approver, prompt injection, secret redaction.
8. CI must execute API tests and frontend production build.
9. Codespaces/Docker runtime must be exercised before claiming deployability.

## Status

This commit adds development-environment and CI scaffolding plus this audit record. It does **not** implement the critical security controls listed above. Do not use real customer data, production credentials, paid advertising actions, external publishing, or customer messaging until all release gates pass.