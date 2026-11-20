# Production implementation backlog

## P0 – Required before real users/data
- [ ] Authentication (OIDC) and RBAC; tenant membership checks on every endpoint.
- [ ] PostgreSQL row-level security and tenant isolation tests.
- [ ] Alembic migrations; remove development `create_all` from production.
- [ ] Immutable audit log for task changes, tool calls, approvals and decisions.
- [ ] Approval payload hash/version binding; reject stale approvals.
- [ ] Secret manager; rotate keys; redact logs; rate limits and quotas.
- [ ] Unit, integration, security and prompt-injection tests.

## P1 – Agent execution
- [ ] Agent runtime that loads registry policy, department instructions and skills.
- [ ] Director task decomposition into typed subtasks with dependency graph.
- [ ] Department head delegation, parallel execution, timeout and retry policy.
- [ ] Independent QA with evidence/source checks and structured output schemas.
- [ ] Model routing by task tier, latency, token cost, evaluation score and fallback.
- [ ] Usage metering and per-organization budgets.

## P2 – Integrations
- [ ] MCP server with allowlisted tools and per-tenant credentials.
- [ ] n8n webhook integration with signed requests and idempotency keys.
- [ ] Google Analytics/Search Console, Meta Ads, Google Ads, TikTok, CRM and marketplace connectors.
- [ ] Read-only mode first; write actions only after explicit approval.

## P3 – Product experience
- [ ] Web task creation, task detail, approval inbox and agent registry pages.
- [ ] Company/brand switcher and access administration.
- [ ] Knowledge ingestion, document versioning and source citations.
- [ ] KPI dashboards, campaign calendar, cost and performance reporting.

## Acceptance gates
- No cross-tenant read/write in automated tests.
- No external write action without current approval bound to exact payload.
- Every generated claim in research reports has source provenance or is labeled as inference.
- Agent tasks have bounded time, token, tool and cost budgets.
