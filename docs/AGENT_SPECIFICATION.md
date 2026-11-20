# Agent Organization and Specification v1.1

## Organization count
Target structure: 1 AI Marketing Director + 10 Department Heads + 45 Specialists = 56 logical roles. These are role definitions in `departments/agent_registry.json`, not 56 deployed services or fully implemented agents.

## Department roster

| Department | Head | Specialists |
|---|---|---|
| Marketing Intelligence | Marketing Intelligence Department Head | Market Researcher; Competitor Analyst; Customer Insight Analyst; Industry Analyst; Data Researcher |
| Marketing Strategy & Brand | Marketing Strategy & Brand Department Head | Marketing Strategist; Brand Strategist; STP Analyst; Product Marketing Manager; Pricing Strategist |
| SEO & SEM | SEO & SEM Department Head | SEO Specialist; Keyword Researcher; Content SEO Specialist; PPC Specialist |
| Content & Creative | Content & Creative Department Head | Content Strategist; Copywriter; Content Writer; Creative Director; Graphic Design Agent; Video Producer |
| Social Media & Influencer | Social Media & Influencer Department Head | Social Media Strategist; Facebook Specialist; TikTok Specialist; YouTube Specialist; Influencer Manager |
| Demand Generation | Demand Generation Department Head | Growth Strategist; Campaign Manager; Performance Marketer; Lead Generation Specialist |
| CRM & Lifecycle | CRM & Lifecycle Department Head | CRM Strategist; Email Marketing Specialist; Retention Specialist; Loyalty Manager |
| E-commerce & Conversion | E-commerce & Conversion Department Head | E-commerce Manager; Marketplace Specialist; CRO Specialist; Sales Funnel Specialist |
| Analytics & Business Intelligence | Analytics & BI Department Head | Marketing Analyst; Attribution Analyst; Financial Analyst; Business Intelligence Analyst |
| Marketing Operations | Marketing Operations Department Head | Marketing Operations Manager; Project Manager; Quality Assurance Agent; Marketing Documentation Agent |

## Executive Director
The AI Marketing Director receives business objectives, creates structured briefs, decomposes work into workstreams/dependencies, selects departments, routes tasks, tracks quality/cost/SLA, consolidates results, requests human approval, and reports measured outcomes. It cannot approve its own proposals or grant itself permissions.

## Department Head contract
Each Head owns department planning, specialist delegation, dependency management, review, quality, deadlines, resource usage, and consolidated delivery. It escalates cross-department conflicts, policy issues, missing data, and budget changes.

## Specialist contract
Each specialist performs a bounded domain task, uses only allowlisted tools/data, returns schema-valid outputs with source provenance, labels assumptions/uncertainty, and escalates out-of-scope requests. Draft/recommendation permissions do not imply publish/spend/send permissions.

## Executable agent profile schema
Every activated agent requires:
- Stable `agent_id`, name, department, tier, profile version.
- Mission, scope, non-goals, prohibited actions.
- System instructions and operational rules.
- Input and output JSON schemas.
- Skills and allowlisted tools.
- Organization/brand scope and permission policy.
- Evidence/citation and uncertainty policy.
- Model policy, fallback, token/cost/time budgets.
- Approval level and escalation rules.
- Quality criteria, evaluation dataset, pass threshold.
- Prompt/profile version, owner, audit metadata.

## Runtime rules
- Shared runtime loads role profiles on demand; no one-service-per-agent architecture.
- Model selection is task-based, not permanently hardcoded per role.
- Validate every output against schema and policy.
- Treat retrieved content and tool outputs as untrusted.
- Bound time, steps, retries, concurrency, and cost.
- Independent QA for consequential or high-risk outputs.
- Department Head reviews specialist outputs; Director consolidates department outputs.
- Human approval is mandatory for external or financial side effects.

## Example task boundaries
- Competitor Analyst: may research and compare public competitor information; may not make unsupported claims or contact competitors.
- Content Writer: may create drafts; may not publish or send.
- PPC Specialist: may analyze campaign data and recommend changes; may not change spend or launch campaigns without approval.
- Pricing Strategist: may analyze scenarios and recommend prices; may not alter live pricing.
- Quality Assurance Agent: may flag failures and request revisions; may not approve its own deliverable as final when independent review is required.

## Activation rule
A registry entry is only a declared logical role. Mark an agent executable only after its profile, schemas, tool permissions, tests, evaluation threshold, observability, and bounded runtime are implemented. Keep registry count and executable count separate in APIs and dashboards.
\n\n## Cross-department operating contract
Department Heads are accountable workstream owners, not merely prompt wrappers. They accept or decline work, confirm capacity, decompose work, assign eligible specialists, review deliverables, issue typed collaboration requests, accept/reject handoffs, and escalate conflicts. Specialists receive bounded task envelopes and return schema-validated TaskResults with artifact references, evidence, assumptions, blockers, usage, and recommended next steps. The Director owns integrated program health, cross-department priority resolution, plan changes, consolidation, and escalation. Detailed RACI, handoff contracts, and lifecycle are in [CROSS_DEPARTMENT_WORKFLOW.md](CROSS_DEPARTMENT_WORKFLOW.md).