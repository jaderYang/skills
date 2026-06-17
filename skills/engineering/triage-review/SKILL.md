---
name: triage-review
description: PR Review Triage：分类处理人工 reviewer 的未解决评论，修复代码、回复评论、反馈 harness docs gap。触发词：/triage-review、处理评论、pr comments。
model: opus
---

# PR Review Triage

处理人工 reviewer 的 PR 未解决评论：分类 → 修复 → 回复 → 反馈 harness gap。
与 `pk-review`（bot 自动迭代）互补，不重叠。
分类决策树、回复模板、gap 判断标准见 [references/classification.md](references/classification.md)。

## 参数

输入: $ARGUMENTS

- 纯数字 / `#数字` → 指定 PR 编号，从 GitHub API 拉取评论
- 纯文本描述 → 直接作为评论内容处理（离线 review / 代码审查工具输出）
- 无参数 → `gh pr list --head $(git branch --show-current) --json number --jq '.[0].number'` 自动检测当前分支 PR

## 流程

### Phase 1: 拉取评论

**来源判断**：根据输入类型决定评论获取方式。

**GitHub API 模式**（输入为 PR 编号或无参数）：

获取 unresolved inline comments：
```bash
gh api repos/{owner}/{repo}/pulls/{PR}/comments --paginate \
  --jq '.[] | select(.state != "resolved") | {id, path, line, body, user: .user.login, in_reply_to_id}'
```

获取顶层 review comments：
```bash
gh api repos/{owner}/{repo}/pulls/{PR}/reviews --paginate \
  --jq '.[] | select(.state == "COMMENTED") | {id, body, user: .user.login}'
```

**文本输入模式**（输入为评论内容文本）：

从文本中解析评论，提取：
- 文件名和行号（如 `RN/packages/react-ui-rn/README.md:21-22`）
- 评论内容（破折号后的描述）
- 设置 `has_comment_id = false`

**混合模式**：部分评论有 ID，部分无 ID。分别标记，Phase 9 按类型执行回复。

### Phase 2: 读取上下文

按顺序读取（每步只读必要部分，节省 token）：

1. **被评论代码**：Read 每条评论涉及的文件，取评论行 ±30 行
2. **CONTEXT.md**：项目领域知识（Model、NetworkService 等术语定义）
3. **harness docs**：`docs/RN.md`、`StyleGuide.md`、`docs/AGENT-RULES.md`
4. **同类 pattern**：Grep 同类实现验证 reviewer 建议是否符合项目惯例

### Phase 3: 分类

按 `references/classification.md` 决策树分类每条评论为 **FIX** / **REPLY** / **DISCUSS**。
分类必须给出依据（引用 harness docs 条目、CONTEXT.md 定义、或 grep 结果），无依据降级为 DISCUSS。

### Phase 4: [确认1] 分类表格

展示表格：`# | 文件:行号 | Reviewer | 评论摘要 | 分类 | 理由 | 处理方式`
用 AskUserQuestion 让用户确认或调整。

### Phase 5: 执行修复

- **FIX**：修改代码，修复后 Read 确认正确性
- **REPLY**：按 `references/classification.md` 模板生成回复文本（中文，简洁专业）
- **DISCUSS**：用户确认后转为 FIX 或 REPLY

### Phase 6: Harness Gap Report

对照评论检查 harness docs 覆盖 gap（缺失 / 模糊 / 过时）。
按 `references/classification.md` 格式输出。**只在发现 gap 时生成**。

### Phase 7: [确认2] 展示改动

展示代码 diff + harness docs diff（如有）。AskUserQuestion 确认。

### Phase 8: 展示回复

展示所有待发回复（`## 回复 #N — 文件:行号 @reviewer`）。
**自动发布到 PR，无需用户确认。**

### Phase 9: 执行回复

根据评论来源选择回复方式：

**有 comment ID**（GitHub API 模式）：
```bash
gh api repos/{owner}/{repo}/pulls/comments/{comment_id}/replies -f body="..."
```

**无 comment ID**（文本输入模式）：

将所有回复整合为一条 PR comment 发送：
```bash
gh pr comment {PR} --body="$(cat <<'EOF'
## Review 处理回复

| # | 文件:行号 | 问题摘要 | 处理 |
|---|---------|---------|------|
| 1 | `file:line` | 问题描述 | 已修复/说明 |
| 2 | `file:line` | 问题描述 | 已修复/说明 |
...

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

**混合模式**：有 ID 的逐条回复，无 ID 的合并为一条 PR comment。

完成后输出汇总。**不自动 push**。

## 硬性约束

- 不自动 push
- 回复中文，简洁专业
- 分类依据必须可验证
