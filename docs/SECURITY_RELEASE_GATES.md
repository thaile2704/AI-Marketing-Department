# Security Release Gates

These gates are mandatory before production use or real customer data.

## Identity and authorization
- OIDC login; validate issuer, audience, signature, expiry, and nonce.
- Derive actor identity from verified token claims; never accept `decided_by` or organization identity as trusted caller input.
- RBAC roles: platform_admin, organization_owner, marketing_manager, approver, analyst, agent_service.
- Enforce organization and brand membership server-side on every endpoint and background job.
- Deny by default. Separate read, create, approve, execute, administer permissions.

## Tenant data isolation
- Add organization_id and brand_id to all tenant-owned records and relevant foreign keys.
- Use PostgreSQL RLS with transaction-scoped tenant context; ensure connection-pool context is reset safely.
- Test cross-tenant reads, writes, list filters, object-ID guessing, and background jobs.

## Approval integrity
- Canonicalize action payload (stable JSON serialization) and persist SHA-256, payload version, tenant, action type, resource, expiry, requested_by.
- Approval decision must use authenticated actor identity and verify approver permission for that tenant/action.
- At execution, recompute payload hash and reject if changed, expired, already consumed, or outside approved scope.
- Use one-time execution/idempotency key; record decision and execution as separate events.
- Never let an LLM approve or bypass approval.

## Audit and secrets
- Append-only audit table; application role cannot update/delete audit rows.
- Record actor, tenant, event, target, timestamp, correlation ID, before/after hashes, outcome.
- Keep credentials out of Git, logs, prompts, browser bundles, and error responses.
- Use secret manager in production; rotate exposed credentials; redact sensitive values.

## Runtime and abuse controls
- Rate limits and per-tenant quotas for API, model tokens, tools, and concurrent jobs.
- Bound every agent by timeout, max steps, token/cost budget, and allowlisted tools.
- Treat retrieved documents/web pages/tool outputs as untrusted data.
- Validate model outputs against strict schemas and policy before side effects.
- External integrations start read-only. Write scopes require explicit approval and least-privilege credentials.

## CI acceptance
- Unit, integration, authorization, tenant-isolation, approval-replay, stale-payload, prompt-injection, and secret-redaction tests.
- Dependency and container scanning; pinned/reviewed actions; protected main branch.
- No production release until all critical gates are green.