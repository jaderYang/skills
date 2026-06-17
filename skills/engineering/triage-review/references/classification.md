# 分类决策树 & 回复模板

## 分类决策树

按优先级从高到低判断：

```
评论是否是 bug？（崩溃、逻辑错误、数据不一致）
├─ YES → FIX
└─ NO ↓

评论是否违反 harness docs 明确约束？
（CONTEXT.md 术语约定、RN.md pattern、StyleGuide.md 规则、AGENT-RULES.md 禁令）
├─ YES → FIX
└─ NO ↓

评论是否有 suggestion code 且改动 ≤3 文件？
├─ YES → FIX（suggestion 通常已给出具体代码）
└─ NO ↓

评论是否是架构级重构建议？
├─ YES → REPLY（超出当前 PR scope，说明后续处理）
└─ NO ↓

评论是否是纯疑问 / 需要解释？
├─ YES → REPLY（给出解释，不改代码）
└─ NO ↓

评论是否是 nit（代码风格、变量命名、可选优化）？
├─ YES → REPLY（接受或说明理由）
└─ NO ↓

无法明确分类？
└─ DISCUSS（列出犹豫的原因，等用户决定）
```

## 修复降级条件

FIX 类评论如遇到以下情况，降级为 DISCUSS：

- 修复涉及 **>3 个文件**
- 需要理解 skill **没有读取到的上下文**（如其他模块的内部实现）
- 修复后与项目中 **同类 pattern 矛盾**（grep 其他实现发现不一致）
- reviewer 的建议 **与 harness docs 冲突**

降级时在表格中标注原因。

## 回复模板

### REPLY — 接受但不修

```
认同，[简要说明原因]。会在后续 PR 中处理。
```

### REPLY — 不接受

```
这里 [解释当前做法的理由]，因为 [具体原因]。暂不修改。
```

### REPLY — 解释疑问

```
[直接回答问题，给出代码/逻辑层面的解释]。
```

### FIX — 已修复

```
已修复，[简要说明改了什么]。
```

### FIX — 部分修复

```
已按建议修复了 [X]，[Y] 部分因为 [原因] 采用了 [替代方案]。
```

### DISCUSS → 用户确认后

按用户指示使用 FIX 或 REPLY 模板。

## Harness Gap 判断标准

评论暴露了 harness docs 的 gap 当且仅当：

1. **规则缺失**：reviewer 指出的规范在 RN.md / StyleGuide.md / AGENT-RULES.md / CONTEXT.md 中都找不到对应条目
2. **规则模糊**：规则存在但 reviewer 仍然提出质疑，说明表述不够清晰
3. **规则过时**：规则与实际项目惯例已经不一致

Gap report 格式：

```
### Gap #N: [简短描述]
- 来源评论: [文件:行号] [reviewer]
- 类型: 缺失 / 模糊 / 过时
- 建议文档: [目标文件] 的 [section]
- 建议内容:
  [具体的规则文本]
```
