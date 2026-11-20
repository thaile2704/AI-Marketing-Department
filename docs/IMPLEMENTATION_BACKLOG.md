# Implementation Backlog v1.1

This backlog distinguishes the existing scaffold from production gates. Do not mark an item complete based only on a config file or role registry entry.

## P0 — Engineering foundation and security (current priority)

### Codespaces and CI
- [ ] Validate Codespaces rebuild on the active engineering branch.
- [ ] Verify Node 22, npm, Python 3.12, service DNS, API health, and frontend response.
- [ ] Ensure CI runs backend tests and frontend production build.
- [ ] Keep Docker Compose and Codespaces instructions consistent.
- [ ] Confirm migrations run reliably on a fresh database and existing DB upgrade plan is reviewed.

### Identity and authorization
- [x] Initial OIDC JWT validation and organization-role checks are present in API code.
- [x] Local development identity bypass is explicitly gated by development environment and opt-in setting.
- [ ] Configure and test against the actual chosen IdP and real role claim mapping.
- [ ] Add complete RBAC for platform, organization, brand, read, create, approve, execute, and administer.
- [ ] Enforce brand-level authorization independently.
- [ ] Add negative tests for unauthenticated requests, forged identities, missing roles, and cross-organization access.

### Tenant isolation
- [ ] Add PostgreSQL RLS with transaction-scoped organization/brand context.
- [ ] Ensure connection-pool context is safely reset.
- [ ] Add cross-tenant read/write, object-ID guessing, filters, and background-job tests.
- [ ] Ensure every tenant-owned model and foreign key carries the required scope.

### Migrations and audit
- [x] Alembic migration framework and initial task/approval/audit schema exist.
- [x] Database trigger prevents UPDATE/DELETE on audit events.
- [ ] Review migration naming/history and test fresh install plus upgrade path.
- [ ] Complete audit coverage for task updates, agent runs, tool calls, admin actions, approval, execution, and failures.
- [ ] Add correlation IDs and before/after hashes where appropriate.
- [ ] Harden DB roles so application credentials cannot bypass audit immutability.

### Approval and execution safety
- [x] Canonical payload SHA-256, expiry, approver identity from principal, and row lock during decision are present.
- [ ] Bind approval to immutable payload version, organization, brand, resource, action scope, and current permission policy.
- [ ] Implement one-time execution/idempotency and consumed-state transition.
- [ ] Create separate executor that rechecks payload hash, expiry, scope, approval, and permission.
- [ ] Keep approval decision and external execution as separate audited events.
- [ ] Add replay, stale payload, concurrent decision, wrong-tenant approver, and expired approval tests.

### Secrets and abuse controls
- [ ] Production secret manager and key rotation.
- [ ] Secret/PII redaction in logs, prompts, errors, and browser bundles.
- [ ] Rate limits, per-tenant quotas, concurrency caps, and budget enforcement.
- [ ] Dependency/container/security scanning.
- [ ] Prompt-injection and untrusted retrieval tests.

## P1 — AI core and executable agent runtime
- [ ] Versioned agent profile schema and registry validation.
- [ ] Shared runtime that loads role instructions, skills, schemas, tools, permissions, and model policy.
- [ ] AI Director brief and structured task decomposition.
- [ ] Typed workstreams, dependencies, owners, acceptance criteria, and lifecycle state.
- [ ] Department Head delegation and specialist invocation.
- [ ] Parallel execution, bounded retries, timeouts, cancellation, and recovery.
- [ ] Independent QA, evidence checks, structured outputs, and revision loop.
- [ ] Model gateway routing by task tier, quality, latency, cost, and data policy.
- [ ] Provider fallback, retry policy, token/usage metering, per-tenant budgets.
- [ ] Prompt/profile/workflow versioning and traceability.
- [ ] Evaluation datasets and release thresholds for each executable agent.

## P2 — Integrations
- [ ] MCP tool gateway with allowlisted tools and server-side policy checks.
- [ ] n8n webhook integration with signed requests, replay protection, and idempotency.
- [ ] Google Analytics and Search Console read-only connectors.
- [ ] Meta Ads, Google Ads, TikTok, YouTube, CRM, and marketplace connectors.
- [ ] Per-organization/brand credential isolation and rotation.
- [ ] Read-only first; write scopes only after approval/execution gates pass.

## P3 — Product experience and knowledge
- [ ] Executive Command Center.
- [ ] AI Director Workspace and task/workstream detail.
- [ ] Department workspaces and agent registry administration.
- [ ] Approval inbox with exact payload/version/hash and risk context.
- [ ] Organization/brand switcher and access administration.
- [ ] Knowledge ingestion, versioning, provenance, and review status.
- [ ] Organization/brand/SOP/execution memory layers.
- [ ] Campaign calendar and deliverable management.
- [ ] KPI, attribution, cost, and business performance dashboards.

## P4 — Governed autonomy and scale
- [ ] Cross-department scheduling and collaboration.
- [ ] Budget recommendations and controlled allocation.
- [ ] Approved scheduled execution with verification.
- [ ] Outcome feedback loops and learning governance.
- [ ] Dynamic model/resource allocation under cost and policy limits.
- [ ] Multi-organization configuration, knowledge sharing boundaries, and cost allocation.

## Mandatory acceptance gates
- No unauthenticated protected operations.
- No cross-tenant/brand read or write.
- No stale, expired, replayed, forged, or out-of-scope approval can execute.
- No external write without explicit current approval and a separate authorized executor.
- Every important action is auditable.
- Every agent task has bounded time, steps, tools, and cost.
- Research claims have source provenance or are labeled as inference.
- CI, migration, and Codespaces checks are green before release.


## P1 — Cross-department workflow (new detailed scope)
- [ ] Program brief, versioned program/workstream/task/artifact schemas and migrations.
- [ ] Dependency DAG validation, cycle detection, hard/soft dependency semantics.
- [ ] Department acceptance, capacity confirmation, specialist assignment, and accountable ownership.
- [ ] PostgreSQL transactional outbox, durable scheduler, atomic task claim/lease, idempotency, and recovery.
- [ ] LangGraph bounded fan-out/fan-in with persisted checkpoints and concurrency/cost limits.
- [ ] Task lifecycle, collaboration request, escalation, artifact review, and event timeline APIs.
- [ ] Department QA, revision loops, Director integration, independent QA, and conflict resolution.
- [ ] Pause/resume/cancel, retry classification, partial failure, and human escalation.
- [ ] Executive, Director, Department, Task, and Approval workspaces.
- [ ] Tests for DAG ordering, parallelism, no premature dispatch, duplicate delivery, worker crash, cancellation, tenant/brand isolation, cost caps, and approval boundaries.
- [ ] Do not mark workflow implemented until acceptance criteria in docs/CROSS_DEPARTMENT_WORKFLOW.md pass.
