# Claude Code — Start Here

## Required reading
Read `docs/PROJECT_CONTEXT_FOR_CLAUDE.md` first. It is the consolidated handoff for product vision, approved architecture, 56-role organization, current code status, security gates, roadmap, and working protocol.

Then read:
- `.claude/CLAUDE.md`
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DECISIONS.md`
- `docs/AGENT_SPECIFICATION.md`
- `docs/IMPLEMENTATION_BACKLOG.md`
- `docs/SECURITY_RELEASE_GATES.md`
- Relevant source, migrations, and tests for the task.

## First prompt — inspect only
```text
Read docs/PROJECT_CONTEXT_FOR_CLAUDE.md and .claude/CLAUDE.md completely.
Inspect the current branch, git status, repository structure, source code, migrations, and tests.
Do not edit files yet.

Report:
1. Current implementation status versus approved architecture.
2. Concrete bugs, security gaps, missing dependencies, and docs/code mismatches.
3. The single highest-priority next milestone.
4. Exact files to change and why.
5. Acceptance criteria and test commands.

Do not change architecture, create placeholder agents, enable external actions, or run destructive commands. Wait for approval before implementation.
```

## Implementation protocol
After the user approves a milestone, implement only that slice, add tests, run exact commands, update relevant docs/ADRs, and report changed files plus test evidence. Do not claim tests passed unless actually executed.
