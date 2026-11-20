# Cross-Department Operating Model
Version: 1.0 | Status: Proposed target specification, not implemented | Orchestrator: LangGraph | System of record: PostgreSQL

## 1. Purpose
Upgrade the deterministic planner into a governed operating system that turns business objectives into coordinated department work, assigns accountable owners, runs independent tasks concurrently, manages dependencies and handoffs, reviews deliverables, resolves conflicts, and reports integrated outcomes. This is a target design, not a claim about current functionality.

## 2. Operating principles
1. One accountable owner per workstream/deliverable; contributors may be many.
2. Director coordinates the integrated program; Department Heads manage workstreams; Specialists produce bounded outputs.
3. Important work is represented by typed, durable records, not chat-only instructions.
4. Independent tasks may run in parallel; dependent tasks wait for accepted prerequisites.
5. Parallelism, retries, time, tool access, and cost are bounded by policy.
6. PostgreSQL is authoritative for task state, artifacts, events, approvals, and audit.
7. Evidence, assumptions, confidence, and unknowns travel with every deliverable.
8. Independent QA is required for high-risk or consequential work.
9. Approval is separate from execution; a separate executor revalidates every external action.
10. No silent plan changes, dropped tasks, unbounded loops, or hidden agent-to-agent state.
11. Humans retain authority over objectives, budgets, access rights, risk policy, and consequential decisions.
12. Measure business outcomes, not agent message volume or raw task count.

## 3. Organization and accountability

### Executive roles
- Human CEO/CMO: sets objectives, KPI targets, budget ceiling, constraints, risk appetite, and approval rules.
- AI Marketing Director: accountable for the integrated program; validates brief, decomposes objectives, appoints workstream leads, resolves cross-department conflicts, monitors dependencies/cost/quality, consolidates results, and escalates decisions.
- Department Head: accountable for department delivery; accepts work, confirms capacity, delegates to specialists, manages dependencies, reviews outputs, coordinates peer departments, and escalates blockers.
- Specialist: responsible for a bounded task; uses allowlisted tools, returns structured evidence-backed outputs, reports progress/blockers, and cannot self-expand scope or permissions.

### RACI
| Operation | CEO/CMO | Director | Department Head | Specialist | Executor |
|---|---|---|---|---|---|
| Set objective, KPI, budget | A/R | C | I | I | I |
| Create integrated program proposal | A for material scope | R | C | I | I |
| Own department workstream | I | A for integrated outcome | R | C | I |
| Delegate specialist tasks | I | C | A/R | I | I |
| Produce specialist deliverable | I | I | A | R | I |
| Accept department deliverable | I | C | A/R | C | I |
| Integrate cross-department result | I | A/R | C | I | I |
| Approve external/financial action | A/R or authorized delegate | C | C | I | I |
| Execute approved action | I | I | I | I | R |
| Verify outcome | A for business result | R | R/C | C | R for execution receipt |

A = Accountable; R = Responsible; C = Consulted; I = Informed. Approval policy determines the authorized human, not an agent.

### Default collaboration matrix
| Work | Lead | Typical collaborators | Handoff |
|---|---|---|---|
| Market entry / annual strategy | Strategy & Brand | Intelligence, Analytics, Demand Gen, E-commerce, Operations | Evidence pack, strategy brief, KPI tree |
| Product launch | Strategy & Brand | Intelligence, Content, SEO, Social, Demand Gen, E-commerce, CRM, Analytics | Positioning, launch brief, claims evidence |
| Integrated campaign | Demand Generation | Strategy, Intelligence, Content, SEO, Social, CRM, E-commerce, Analytics, Operations | Campaign brief, channel plans, budget, measurement |
| Organic acquisition | SEO & SEM | Intelligence, Strategy, Content, Analytics | Keyword map, content briefs, technical backlog |
| Creative production | Content & Creative | Strategy, SEO, Social, Demand Gen, Operations | Approved brief, asset package, claim checklist |
| Influencer/social | Social Media & Influencer | Strategy, Content, Demand Gen, Analytics | Creator shortlist, content brief, tracking plan |
| Retention/lifecycle | CRM & Lifecycle | Intelligence, E-commerce, Analytics, Content | Segment, journey, consent/suppression rules |
| Marketplace/CRO | E-commerce & Conversion | Strategy, Content, SEO, Demand Gen, CRM, Analytics | Page requirements, CRO backlog, conversion report |
| Performance/budget review | Analytics & BI | All Heads, Director | KPI dataset, caveats, variance, decision memo |
| Launch readiness/operations | Marketing Operations | All Heads, Director | Integrated timeline, RACI, risk/readiness checklist |

Director selects the smallest sufficient set of departments for each objective; this matrix is a routing guide, not mandatory fan-out.

## 4. End-to-end operating lifecycle

### Stage 0 — Objective intake
Capture organization_id, brand_id, requester, objective, context, audience, product/service, baseline, target KPI, deadline, budget ceiling, constraints, authorized data, risk class, and requested action. Reject or clarify missing tenant/brand scope, accountable requester, objective, or success measure. Never invent baseline data.

### Stage 1 — Director brief
Director retrieves authorized brand knowledge, clarifies ambiguity, distinguishes evidence from assumptions, identifies missing data, and creates a versioned ProgramBrief: problem, outcome, audience, offer, positioning constraints, KPI tree, budget envelope, horizon, assumptions, risks, and acceptance criteria. Human confirmation is required for material strategy, budget, or scope where policy says so.

### Stage 2 — Program decomposition
Director creates a Program with Workstreams and a dependency DAG. Each workstream has exactly one lead department. Each task has one accountable owner, optional contributors/reviewers, inputs, output schema, acceptance criteria, priority, risk, due date/SLA, estimated cost, and dependencies.
Planner must reuse valid artifacts, split work into deliverables, mark hard/soft dependencies, identify parallel branches, add cross-department handoffs and review gates, estimate cost/concurrency, and detect cycles. Reject cyclic graphs. Resolve ownership ambiguity before dispatch. Validate DAG, permissions, capacity, budget, and approval gates before execution.

### Stage 3 — Department acceptance and planning
Director sends each workstream to its lead Head. The Head accepts, declines with reason, or requests clarification; confirms capacity; selects eligible specialists from the registry; creates bounded tasks; sets internal review; and publishes a department plan. A Head may create a typed CollaborationRequest to another Head. Receiver accepts, declines with reason, or proposes alternative scope/date. Director resolves cross-department priority conflicts. No specialist starts without owner, scope, input/output contract, and acceptance criteria.

### Stage 4 — Scheduling and dispatch
Scheduler dispatches only tasks whose hard dependencies are accepted/completed and whose policy, approval, budget, and capacity gates pass.
- Fan out independent ready tasks concurrently; fan in at explicit barriers.
- Never start downstream work from unaccepted inputs unless provisional input is explicitly allowed.
- Enforce tenant, brand, department, provider, and global concurrency/cost limits.
- Use priority plus deadline/aging and fair scheduling to prevent starvation.
- Persist dispatch intent before worker handoff; use leases, heartbeats, and idempotency keys.
- Initial durable queue/control plane is PostgreSQL (transactional outbox and atomic claims); no Redis/broker addition without ADR.
- LangGraph remains the sole orchestrator. n8n is for external triggers/integration automation, not task delegation or workflow state.

### Stage 5 — Specialist execution
Each invocation receives task/run/correlation IDs, organization/brand scope, role profile and version, objective, bounded scope/non-goals, input artifact references, allowlisted tools, output schema, acceptance criteria, deadline, max steps, retry/token/cost budget, and escalation policy.
Specialist returns a structured TaskResult: status, summary, deliverable references, evidence, assumptions, confidence/unknowns, blockers, tool-call references, actual cost/time, and recommended next steps. It cannot claim completion without an output. It may return blocked or needs_input.

### Stage 6 — Department QA and collaboration
Head checks completeness, relevance, evidence, brand fit, policy, and acceptance criteria. Outcomes: accept, request revision with machine-readable findings, reject, or escalate.
Cross-department handoff:
1. Requesting Head creates CollaborationRequest with purpose, originating task, required artifact/schema, input references, priority, and due date.
2. Receiving Head accepts/declines/proposes alternative.
3. Receiver assigns a contributor and returns a versioned artifact with provenance.
4. Requesting Head validates and accepts or returns specific defects.
5. Both workstreams record dependency and event history.
No department silently overwrites another's accepted artifact. Disputes and resource conflicts escalate to Director.

### Stage 7 — Director integration and independent QA
Director waits for mandatory workstreams to be accepted, explicitly waived by authorized human, or failed. It integrates one coherent plan, checks channel consistency, contradictions, budget/KPI arithmetic, and evidence gaps. Independent QA is required by risk policy for sensitive claims, regulated categories, pricing, material spend/attribution, high-impact strategy, conflicting findings, and outputs connected to external execution. QA returns pass, pass-with-warnings, or fail with findings. Revision loops are bounded; after the limit, escalate.

### Stage 8 — Human decision
Decision packet includes recommendation, alternatives, expected impact, budget, risks, assumptions, source evidence, exact proposed external actions, and approval payload hash/version.
- L0: internal analysis/draft.
- L1: low-risk internal action within delegated policy.
- L2: consequential external publishing, messaging, campaign changes; explicit human approval.
- L3: financial/legal/high-risk action; designated approver and possible dual control.
Approval binds organization, brand, action, resource, immutable payload version/hash, approver, policy version, and expiry. Payload change invalidates approval. No self-approval.

### Stage 9 — Authorized execution
A separate executor rechecks tenant/brand scope, current permission, approval, payload hash/version, expiry, idempotency, and connector policy. It performs only the approved action and records request/response, external IDs, timestamps, and outcome. Default connectors are read-only. External writes remain disabled until approval/execution gates are implemented and tested.

### Stage 10 — Verification and learning
Verify external state independently where possible. Compare actuals to baseline/target and attribution window; report variance, confidence, freshness, and cost. Learning produces versioned recommendations only; it cannot silently change strategy, prompts, permissions, budgets, or policies.

## 5. Contracts and durable records

### Task minimum fields
task_id, program_id, workstream_id, parent_task_id, organization_id, brand_id, lead_department_id, accountable_agent_id, assigned_agent_id, requester_id, reviewer_ids, title, objective, type, priority, risk, status, acceptance_criteria, input/output schema versions, required capabilities, tool policy, depends_on IDs, collaboration IDs, estimated effort/cost, budget reservation, due_at, retry policy, task/plan/profile/prompt versions, correlation_id, idempotency_key, timestamps.

### Artifact
artifact_id, type, title, version, status, organization_id, brand_id, program_id, task_id, producer, structured payload or object-storage reference, schema version, content hash, source references, evidence, assumptions, confidence, reviewer, findings, accepted_at. Statuses: draft, submitted, in_review, accepted, revision_requested, rejected, superseded.

### CollaborationRequest
request_id, from/to department, originating_task_id, requested_output_type, purpose, input_artifact_ids, required_schema, priority, due_at, status, accepted_by, assigned_agent_id, response_artifact_id, resolution_note.

### Durable events
Examples: program.created, brief.confirmed, workstream.proposed/accepted, task.ready/dispatched/started/progressed/blocked/completed/failed, artifact.submitted/accepted, revision.requested, collaboration.requested/accepted/resolved, approval.requested/granted/rejected, execution.started/succeeded/failed, program.completed.
Each event has event_id/type, aggregate_id, organization_id, brand_id, actor, timestamp, correlation_id, causation_id, schema_version, payload. Use transactional outbox so DB state and event publication cannot diverge; consumers are idempotent; never put secrets in event payloads. Agents communicate via typed requests, events, and artifact references—not unrestricted agent chat.

## 6. State machines

Program: draft -> awaiting_confirmation -> approved_for_planning -> planning -> running -> integrating -> awaiting_human_decision -> executing -> verifying -> completed. Exceptions: cancelled, rejected, failed, partially_completed, paused.

Workstream: proposed -> awaiting_department_acceptance -> accepted -> planning -> ready -> running -> reviewing -> accepted. Alternatives: blocked, revision_requested, failed, cancelled.

Task: draft -> ready -> queued -> assigned -> running -> submitted -> reviewing -> completed. Alternatives: blocked, needs_input, revision_requested, rejected, failed, cancelled, skipped, expired.

Validate transitions server-side and audit them. Agents cannot reopen terminal states; authorized reopen creates a new version/task.

## 7. Scheduling, retries, and recovery
- Persisted DAG scheduler; hard dependencies gate readiness; soft dependencies require explicit provisional-input policy.
- Atomic worker claims using DB locks/leases; safely reclaim stale leases.
- Unique idempotency key and attempt number for every execution.
- Retry transient errors only; schema, policy, permission, and validation errors require correction.
- Exponential backoff with jitter, capped attempts and elapsed time.
- Distinguish model timeout, tool timeout, task deadline, workflow deadline.
- Cancellation propagates to children where safe; in-flight external side effects require reconciliation, not fake rollback.
- Preserve successful siblings on partial failure.
- Pause/resume uses persisted checkpoint and plan version.
- Reserve budget before dispatch and reconcile with actual usage.

## 8. Conflict and escalation
Department Head handles missing input, low confidence, internal workload, and within-department scope. Director handles cross-department ownership disputes, incompatible outputs, resource/budget contention, deadline conflicts, repeated QA failure, and material scope change. Human escalation is mandatory for policy ambiguity, budget increases beyond delegation, sensitive claims, external action, legal/compliance risk, and strategic trade-offs. Escalation record includes issue, impact, options, evidence, recommendation, deadline, decision owner, and affected task IDs.

## 9. Service levels and scorecards
Initial configurable targets, not promises: acknowledge assignment within one work cycle; Head accepts/declines/clarifies within configured SLA; progress on state changes and heartbeat; blockers escalated immediately; collaboration request explicitly accepted/declined; retries bounded.
Track delivery (on-time, cycle time, blocked time, rework, dependency wait), quality (first-pass acceptance, revisions, evidence coverage, QA failure), coordination (handoff latency, conflict resolution), resources (cost, tokens, concurrency, utilization, variance), and business outcomes (CAC, ROAS, pipeline, revenue, conversion, retention, brand lift only where evidence supports attribution). Normalize complexity; do not reward raw task count or message volume.

## 10. Target persistence and orchestration architecture
Keep approved stack: FastAPI, PostgreSQL, LangGraph only, shared role-profile runtime, model gateway, Next.js.
Logical persistence: programs, briefs, workstreams, tasks, dependencies, agent_profiles, agent_runs/attempts, artifacts/reviews, evidence_sources, collaboration_requests, escalations, domain_events, outbox_events, workflow_checkpoints, budget_reservations, usage_records, approval_requests, execution_records, audit_events.
PostgreSQL is initial durable queue/control plane using transactional outbox, atomic claim/lease, row locks, unique idempotency, and checkpoint persistence. Add broker only by ADR after measured need.
Conceptual LangGraph: intake -> validate_scope -> director_brief -> plan_program -> validate_dag -> department_acceptance -> schedule_ready_tasks -> dispatch_parallel -> await_results -> department_review -> collaboration_or_revision -> director_integration -> independent_qa -> human_approval_gate -> authorized_executor -> verify_outcome -> report. Conditional paths handle blocked/failed/revision/approval. Fan-out/fan-in uses persisted task IDs and checkpoints, never in-memory-only state.

## 11. Target API surface
POST /programs; GET /programs/{id}; POST /programs/{id}/plan; POST /programs/{id}/confirm; GET /programs/{id}/workstreams; GET /tasks/{id}; POST /tasks/{id}/accept; POST /tasks/{id}/submit; POST /tasks/{id}/review; POST /collaboration-requests; POST /collaboration-requests/{id}/respond; POST /tasks/{id}/cancel; POST /programs/{id}/pause; POST /programs/{id}/resume; GET /programs/{id}/events; GET /departments/{id}/workload. Approval and execution endpoints remain separate. All routes require tenant/brand authorization, validation, rate limits, audit, and idempotency as appropriate. This is a target contract, not permission to add untested endpoints.

## 12. Dashboard requirements
- Executive: objective/KPI, program health, department status, budget/cost, risks, pending decisions, forecast, outcomes.
- Director: DAG, workstream owners, cross-department dependencies, conflicts, workload, deadlines, quality gates, plan changes.
- Department: accepted work, specialist assignments, capacity, blockers, collaboration inbox/outbox, QA queue, deliverables, SLA.
- Task: brief, owner, status timeline, dependencies, attempts, cost, artifacts, evidence, reviewer findings, approvals, audit.
- Approval: exact action/payload diff/hash/version, tenant/brand, risk, approver, expiry, alternatives, execution status.

## 13. Delivery roadmap
P1 durable orchestration: typed schemas/migrations; DAG validation/cycle detection; persisted state/events/outbox/correlation; Head acceptance/ownership; Postgres scheduler/leases/idempotency; LangGraph fan-out/fan-in/checkpoint recovery; lifecycle APIs; tests for ordering, parallelism, tenant isolation, crashes, duplicate delivery, cancellation, budget caps.
P2 collaboration: typed requests/inbox/outbox; department review and artifact acceptance/revision; Director conflict resolution/escalations; independent QA/evidence validation; workload/SLA dashboards.
P3 governed execution: payload-bound approval and separate executor; read-only connectors and verification; approved writes; KPI measurement/outcome feedback.

## 14. Acceptance criteria
Workflow is not complete until:
- Objective creates versioned program brief and measurable KPI tree.
- Director creates valid DAG with workstream owners and acceptance criteria.
- All 10 department profiles can accept/decline/clarify using common contract.
- At least three independent workstreams execute concurrently within configured limits.
- Downstream tasks never start before hard dependencies are accepted.
- Head delegates to specialists and reviews structured deliverables.
- One department can request, receive, accept, and trace another department's artifact.
- QA revision is bounded and audited; Director integrates outputs and surfaces conflicts/evidence gaps.
- Worker crash recovers without lost state or duplicate side effects.
- Pause/resume/cancel/partial failure/timeout/retry are tested.
- Tenant/brand isolation covers every task, event, artifact, run, and collaboration request.
- Cost, attempts, transitions, tool calls, approvals, and execution are auditable.
- No external write without current authorization, exact payload approval, and separate executor.
- Executive, Director, Department, and Task views exist.
- CI and migration tests pass; implemented vs planned status is accurate.

## 15. Explicit non-goals
No 56 always-on agents or microservices; no free-form autonomous swarm; no chat-only state; no unbounded parallelism/retries; no automatic live budget/ad/price/CRM/publishing changes; no second orchestrator; no treating LLM plans as approved executable instructions.
