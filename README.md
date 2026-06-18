# Skills

个人 AI agent skills 集合，用于工程工作流。参考 [mattpocock/skills](https://github.com/mattpocock/skills) 建立。

## 目录结构

```
skills/
├── engineering/    — 代码工作流（调试、TDD、架构、PR）
├── productivity/   — 通用工具（阅读、规划、交接、写作）
├── fork/           — 来自 mattpocock/skills
├── misc/           — 杂项
├── personal/       — 个人定制
├── deprecated/     — 已废弃
└── in-progress/    — 开发中
```

## 所有 Skills

| 分类 | Skill | 说明 |
|------|-------|------|
| engineering | **triage-review** | PR Review Triage：分类处理人工 reviewer 的未解决评论，自动修复代码、回复评论、反馈 harness docs gap |
| productivity | **read-with-me** | 读书陪伴：融合 Adler 四层阅读法、Zettelkasten 卡片笔记法、循证学习法，配合微信读书数据，支持多会话深读、笔记沉淀和间隔复习 |
| fork | **grill-me** | 对计划或设计持续追问，逐个解决决策树的每个分支直到达成共识，适合动手写代码前压力测试方案 |
| fork | **teach** | 多会话渐进式教学，在工作区建立学习空间：MISSION 锚定目标、RESOURCES 积累资料、HTML 课程卡片逐步教授、learning records 追踪进度 |

## Skill 格式

每个 skill 是一个独立目录，包含 `SKILL.md` 主文件：

```
skills/<分类>/<skill名>/
├── SKILL.md           — 主文件（frontmatter + 指令）
└── (可选文件)          — 参考文档、模板、示例
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: 做什么、何时触发。
argument-hint: "可选：建议的参数格式"
disable-model-invocation: true  # 可选：禁止 Claude 自动调用
---
```

## 使用

将 skills 链接到项目：

```bash
./scripts/link-skills.sh
```

列出所有 skills：

```bash
./scripts/list-skills.sh
```
