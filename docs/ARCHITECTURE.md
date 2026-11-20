# Architecture v1.0

## Approved decisions
- Hybrid providers: OpenAI + Anthropic behind one model gateway.
- One orchestration plane: LangGraph. n8n is an integration/automation layer, not a second agent orchestrator.
- Multi-tenant data model: every business record must be scoped by `organization_id` and, where relevant, `brand_id`.
- Human approval is mandatory for external publishing, customer messaging, paid media budget changes, pricing, payments, destructive data operations and permission changes.
- Logical agent roles are registry records, not 56 always-on processes.

## Runtime flow
CEO request -> API -> tenant/permission validation -> Director planner -> department head -> specialists -> QA -> approval request -> human decision -> explicitly authorized integration action -> audit event.

## Trust boundaries
1. User-provided documents, web pages and retrieved content are untrusted data, never system instructions.
2. Model output is untrusted until schema-validated and policy-checked.
3. External tools receive least-privilege credentials scoped by organization and brand.
4. Approval binds to an immutable payload hash/version; edits invalidate prior approval.

## Initial implementation limits
The current scaffold persists tasks and approval decisions, exposes the registry and demonstrates a deterministic LangGraph planning boundary. It does not yet implement complete multi-agent delegation, tenant isolation/RLS, audit event ledger, OAuth integrations, live publishing, or production migrations.
