# Architecture Decision Records

## ADR-001: Single orchestration plane
**Decision:** LangGraph owns stateful agent workflows. n8n handles external triggers and SaaS integrations. Avoid duplicate orchestration state.

## ADR-002: Hybrid model gateway
**Decision:** OpenAI and Anthropic are accessed through one adapter. Routing is policy-based and benchmark-driven, not hard-coded by provider claims.

## ADR-003: Multi-tenant by default
**Decision:** All tenant-owned records carry organization scope and relevant brand scope. API authorization and PostgreSQL RLS are mandatory before production.

## ADR-004: Approval before consequential actions
**Decision:** Model generation never directly implies permission to publish, spend, send, delete, export sensitive data, or change commercial terms. Approval and execution are separate.

## ADR-005: Registry-first agents
**Decision:** Logical roles are declarative registry entries; a shared runtime instantiates roles per task to control cost and complexity. Registry presence is not proof of executable implementation.

## ADR-006: Shared role-driven runtime
**Decision:** Do not create one microservice or always-on process per logical agent. Load versioned profiles into a shared runtime with bounded tools, budgets, schemas, and evaluation.

## ADR-007: Human-in-the-loop levels
**Decision:** L0 internal research/drafting; L1 automated validation/QA; L2 human approval for externally visible or financially consequential actions; L3 restricted/high-impact actions requiring explicit human control and separate policy.

## ADR-008: PostgreSQL is the system of record
**Decision:** Business state, tasks, approvals, audit events, and usage records are persisted in PostgreSQL. Retrieved knowledge can be indexed in pgvector but must retain source provenance and versioning.

## ADR-009: Policy enforcement belongs in the backend
**Decision:** MCP is a tool interface, not an authorization layer. The FastAPI policy layer and authorized executor enforce tenant scope, roles, approvals, and tool permissions before side effects.

## Change policy
Any architecture change requires an explicit proposal, impact analysis, user approval, updated ADR, migration plan, and tests. Never silently replace an approved component.
