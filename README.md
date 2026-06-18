# Skills

My personal collection of AI agent skills for engineering workflows.

## Structure

```
skills/
├── engineering/    — Code-specific workflow skills (debug, TDD, architecture)
├── productivity/   — General workflow tools (planning, handoff, writing)
├── fork/           — Forked from mattpocock/skills (see below)
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

## Fork

`skills/fork/` contains skills adopted from [mattpocock/skills](https://github.com/mattpocock/skills), kept as reference and starting point for customization.

| Skill | Description |
|-------|-------------|
| **grill-me** | 对计划或设计持续追问，逐个解决决策树的每个分支，直到达成共识。每个问题会附带推荐答案，能通过代码探索回答的会直接去查代码。适合在动手写代码前压力测试你的方案。 |
| **teach** | 多会话渐进式教学。在工作区内建立学习空间：用 MISSION.md 锚定学习目标，用 RESOURCES.md 积累高质量参考资料，通过 HTML 课程卡片逐步教授，用 learning records 追踪掌握进度。 |

## Inspiration

Inspired by [mattpocock/skills](https://github.com/mattpocock/skills).
