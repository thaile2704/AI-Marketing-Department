# Architecture v1.1

## Product intent
AI Marketing Department is a governed, multi-organization / multi-brand AI Marketing Operating System. It coordinates research, strategy, specialist marketing work, approvals, execution, and measurement. It is not a chatbot and is not a production-ready autonomous department today.

## Approved technology decisions
- Next.js dashboard; FastAPI backend; PostgreSQL system of record; pgvector for future retrieval.
- LangGraph is the only agent workflow orchestrator.
- n8n is for integration automation/triggers, not agent delegation or workflow state.
- OpenAI and Anthropic are accessed through one model gateway.
- MCP provides controlled tool interfaces; it does not replace server-side authorization.
- Logical roles are registry profiles instantiated through a shared runtime, not 56 always-on services.

## Organization
1 AI Marketing Director + 10 Department Heads + 45 Specialists = 56 logical roles. Department inventory and specialist names are defined in `departments/agent_registry.json`. Registry membership does not mean an executable agent exists.

## Target workflow
CEO/CMO objective -> API identity/tenant/policy checks -> Director brief and task decomposition -> Department Heads -> Specialists -> department QA -> Director consolidation -> human approval where required -> separately authorized executor -> verification, audit, and outcome metrics.

## Logical layers
1. Presentation: Next.js Executive Workspace, Director Workspace, Department Workspace, Approval Center, Knowledge Center, Analytics.
2. Application/control: FastAPI, OIDC, RBAC, tenant/brand policy, API validation, audit, approval policy.
3. Orchestration: LangGraph Director, planner, router, dependency graph, retries, QA, approval gates.
4. Agent runtime: versioned role profiles, skills, tool allowlists, input/output schemas, model policy, cost/time limits.
5. Model gateway: OpenAI + Anthropic, task-based routing, fallback, usage/cost tracking, structured output.
6. Knowledge/data: PostgreSQL, pgvector, object storage, organization/brand/SOP/execution knowledge with provenance.
7. Integrations: MCP and n8n; tenant-scoped credentials; read-only first, write actions behind approval.

## Security and trust boundaries
- Every tenant-owned record and background job is organization-scoped; brand-scoped data carries brand scope.
- API checks permissions on every operation. PostgreSQL RLS is a mandatory production gate.
- Retrieved files, websites, and tool outputs are untrusted data, never instructions.
- Model output is untrusted until schema-validated, evidence-checked, and policy-checked.
- External tools use least-privilege credentials scoped to organization/brand.
- Consequential actions require human approval bound to exact payload hash/version, resource, tenant, action, and expiry.
- Approval is not execution. A separate executor revalidates authorization and approval, uses idempotency/one-time consumption, and audits the outcome.
- No self-approval, privilege escalation by agents, or default live external writes.

## Runtime and scale
Do not create one microservice per agent. A shared runtime loads a versioned profile and instantiates the role needed for a bounded task. Apply timeouts, max steps, retries, concurrency limits, token/cost budgets, structured output schemas, and independent QA.

## Current implementation boundary
The repository currently provides an engineering MVP scaffold: FastAPI, SQLAlchemy/Alembic, basic OIDC and organization-role checks, task/approval persistence, payload hash/expiry checks, an audit table with append-only DB trigger, a deterministic single-node LangGraph planning boundary, minimal provider adapters, a logical role registry, and a Next.js shell.

It does **not** yet provide complete multi-agent delegation, PostgreSQL RLS, independent brand authorization, full production IdP integration, approval execution, MCP/n8n connectors, full knowledge/RAG, production model routing/metering, completed dashboards, or production hardening. Do not claim production readiness.

## Architecture invariants
1. One orchestrator: LangGraph.
2. One system of record: PostgreSQL.
3. Policy before execution.
4. Human controls consequential actions.
5. Version profiles, prompts, workflows, outputs, and approvals.
6. Audit important decisions and actions.
7. Measure business outcomes separately from agent activity.
8. Shared role runtime, not 56 services.
9. Strict tenant/brand isolation.
10. No silent architecture changes; document approved changes in ADRs.
\n\n## Cross-department operating model
The detailed target contract is in [CROSS_DEPARTMENT_WORKFLOW.md](CROSS_DEPARTMENT_WORKFLOW.md). LangGraph remains the sole orchestrator; PostgreSQL remains the system of record and initial durable scheduling/control plane. The target workflow uses versioned programs, workstreams, tasks, dependencies, artifacts, collaboration requests, events/outbox, bounded parallel dispatch, department QA, Director integration, independent QA, approval gates, separate execution, and outcome verification. Cross-agent communication is typed and persisted; unrestricted agent chat is not authoritative. This is planned architecture, not implemented functionality.