# ADR-0002: Optional free-tier proxy as an "economy" model route

Status: PROPOSED (needs owner approval before merge; extends ADR-0001 model gateway)

## Context
Token cost is the main scaling constraint. FreeLLMAPI (github.com/tashfeenahmed/freellmapi, MIT) is a self-hosted,
single-user, OpenAI-compatible proxy that aggregates free tiers of many providers with failover.
It does not create quota; it pools allowances from accounts the operator already owns.

## Decision
Add `free_proxy` as an optional third provider in `model_gateway`, with these constraints:
1. Disabled unless `FREE_PROXY_ENABLED=true` and `FREE_PROXY_API_KEY` is set.
2. Used only when `tier="economy"` AND `data_class="public"`. Default `data_class` is `internal`, so nothing reaches it implicitly.
3. Never receives customer data, credentials, unpublished strategy or personal data (free tiers may log or train on prompts).
4. Never used for approval decisions, final quality review or anything that triggers an external action.
5. Falls back to the paid providers on any failure.
6. One operator, one account per upstream provider, no resale, no sharing the proxy (upstream ToS).

## Consequences
- Lower cost for bulk drafting/research on public information.
- Inconsistent quality and availability: outputs from this route are drafts that still pass human approval.
- Not suitable for production customer workloads; paid providers remain the production path.
- Run the proxy on localhost / a private network only; it is protected by a single key.
