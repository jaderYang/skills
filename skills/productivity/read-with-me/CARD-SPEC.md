# HTML 卡片规范

`books/<书名>/cards/*.html` 的详细规范。

## 产出时机

- 章节读完 / 全书读完 / 用户明确要求 / 重大关系图需求（人物关系/概念网络/论证链）

## 文件命名

`0001-<dash-case-主题>.html`，编号全书递增。

## 风格: Tufte 风

- **排版**: 衬线字体（`Georgia` 或 `Noto Serif CJK SC`），行高 1.6-1.8，最大宽度 720px 居中
- **留白**: padding 充分，正文字号 16-18px
- **注释**: 借鉴 Tufte sidenote 风格
- **无外部依赖**: 纯 HTML + 内联 CSS，不引 CDN（可打印、离线可用）
- **深色/浅色**: 默认浅色，`@media (prefers-color-scheme: dark)` 支持暗色

## 结构: 支持主动回忆

### 正面（问题）

```html
<section class="card-front question">
  <h1>[核心问题]</h1>
  <p class="hint">[可选提示]</p>
  <button class="reveal">点击查看答案</button>
</section>
```

### 背面（答案 + 关系图）

```html
<section class="card-back answer" hidden>
  <h2>答案</h2>
  <div class="answer-body">[2-5 段]</div>
  <h2>关系图</h2>
  <div class="diagram">[SVG 内联 或 Mermaid]</div>
  <h2>相关永久笔记</h2>
  <ul><li><a href="../NOTES.md#书名-P001">书名-P001</a></li></ul>
</section>
```

### 切换 JS

```javascript
<script>
document.querySelector('.reveal').addEventListener('click', function() {
  const answer = document.querySelector('.answer');
  answer.hidden = !answer.hidden;
  this.textContent = answer.hidden ? '点击查看答案' : '隐藏答案';
});
</script>
```

## 关系图

- **人物关系图（虚构）**: 内联 SVG，节点=人物，边=关系
- **概念网络（非虚构）**: 节点=概念，边=支持/反对/依赖/派生
- **论证链（非虚构）**: 有向图: 前提 → 中间结论 → 最终结论

## 复习时间表联动

卡片产出时在 `READING-LOG.md` 复习时间表新增:

```
| 三体-P003 | books/三体/cards/0001-黑暗森林.html | 2026-06-13 | 2026-06-14 | 1天 | - |
```

间隔序列: 1天 → 3天 → 7天 → 14天 → 30天 → 90天。抽考正确推进，错误退回 1天。

## 可打印

- `@media print`: 隐藏按钮，答案始终显示，关系图黑色描边
- A4 友好: 最大宽度打印时自动扩展

## 维护

- 卡片产出后**不删除**，只追加
- 用户反馈"太浅/太深"时可追加修订版，旧版保留标注 `rev: 2`
- 每张卡片底部显示版本和产出日期
