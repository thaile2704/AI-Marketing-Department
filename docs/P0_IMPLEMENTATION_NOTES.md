# P0 implementation notes

## Authentication contract
The API validates RS256/ES256 OIDC JWTs against the configured JWKS URL, issuer and audience. The identity provider must issue an object claim (default `org_roles`) mapping organization IDs to role arrays, e.g. `{"org_123":["organization_owner","approver"]}`. The API never trusts a caller-supplied approver identity.

For local Codespaces smoke tests only, set `APP_ENV=development` and `DEV_AUTH_ENABLED=true`. Supply headers:
- `X-Dev-User: local-user`
- `X-Dev-Org: demo-org`
- `X-Dev-Roles: organization_owner,approver,marketing_manager`

This bypass is intentionally unavailable outside development. Do not expose a development deployment publicly.

## API changes
- Task creation and listing are organization-role scoped.
- Approval creation resolves the task first and derives organization scope from the task.
- Approval decisions derive actor from the authenticated principal, enforce approver role, check expiry, and recompute the canonical payload hash.
- Approval decisions are records only; no external action executor exists yet.
- Audit events are written for task creation and approval request/decision.

## Migration
Run `alembic upgrade head` from the API working directory. Startup no longer invokes SQLAlchemy `create_all`.

## Known remaining security work
- PostgreSQL RLS and DB-level immutable audit triggers/permissions are not yet implemented.
- Organization-role claim mapping must be configured and tested against the chosen IdP.
- Brand-level authorization is not yet enforced independently of organization roles.
- Rate limits, quotas, secret manager integration, token revocation strategy, CSRF policy for browser sessions, and security scanning remain open.
- Existing databases need a reviewed migration/backup plan before applying the initial schema migration.
- Agent/tool execution remains disabled; approval records do not authorize an integration call by themselves.
