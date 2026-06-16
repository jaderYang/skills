# Skills Repo

This repo contains agent skills for Claude Code and similar AI coding assistants.

## Conventions

- Each skill is a directory under `skills/<category>/` containing a `SKILL.md`
- Skill directory names use lowercase kebab-case (e.g., `grill-me`, `improve-architecture`)
- `SKILL.md` frontmatter must include `name` and `description`
- Skills should be small, composable, and model-agnostic
- Write instructions for the agent — talk about what "you" (the agent) should do

## Categories

- `engineering/` — Code-specific workflows (debug, TDD, architecture, PRs)
- `productivity/` — General tools (planning, handoff, writing, brainstorming)
- `misc/` — Useful but rarely needed
- `personal/` — Personal workflow customization
- `deprecated/` — Retired, kept for reference
- `in-progress/` — Under development, not yet stable
