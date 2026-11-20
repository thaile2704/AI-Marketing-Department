# Agent specification contract

Each executable agent must implement these fields before runtime activation:
- stable `agent_id`, display name, department and version
- mission, scope boundaries, allowed/forbidden actions
- input JSON schema and output JSON schema
- required evidence and citation policy
- model tier and maximum token/cost/time budget
- allowed tools and tenant/brand scope
- approval level and escalation conditions
- evaluation dataset and pass threshold

The registry currently defines logical identities and broad roles only. Do not mistake it for complete prompts or production-ready agent implementations. Add department-specific instructions and tests incrementally.
