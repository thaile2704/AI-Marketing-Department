# Architecture Decision Records

## ADR-001: Single orchestration plane
Decision: LangGraph owns stateful agent workflows. n8n handles external triggers and SaaS integrations. Avoid duplicate orchestration state.

## ADR-002: Hybrid model gateway
Decision: OpenAI and Anthropic are accessed through one adapter. Routing is policy-based and benchmark-driven, not hard-coded by brand claims.

## ADR-003: Multi-tenant by default
Decision: all tenant-owned records carry organization and brand scope. API authentication and PostgreSQL row-level security are mandatory before production.

## ADR-004: Approval before consequential actions
Decision: model generation never directly implies permission to publish, spend, send, delete or change commercial terms.

## ADR-005: Registry-first agents
Decision: roles are declarative registry entries; agent runtime is shared and instantiated per task to control cost and complexity.
