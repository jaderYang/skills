# Skills

My personal collection of AI agent skills for engineering workflows.

## Structure

```
skills/
├── engineering/    — Code-specific workflow skills (debug, TDD, architecture)
├── productivity/   — General workflow tools (planning, handoff, writing)
├── misc/           — Rarely used but useful tools
├── personal/       — Personal-use skills
├── deprecated/     — Retired skills
└── in-progress/    — Work-in-progress skills
```

## Skill Format

Each skill lives in its own directory with a `SKILL.md` file:

```
skills/<category>/<skill-name>/
├── SKILL.md           — Main skill file (frontmatter + instructions)
└── (optional files)   — Reference docs, templates, examples
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: What it does and when to trigger it.
argument-hint: "optional: suggested argument format"
disable-model-invocation: true  # optional: prevents Claude from auto-calling
---
```

## Usage

Link skills into your project:

```bash
./scripts/link-skills.sh
```

List available skills:

```bash
./scripts/list-skills.sh
```

## Inspiration

Inspired by [mattpocock/skills](https://github.com/mattpocock/skills).
