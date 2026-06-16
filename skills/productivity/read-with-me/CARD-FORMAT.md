# CARD-FORMAT.md

HTML 复习卡片规范。`books/<书名>/cards/*.html` 使用此格式。

## 产出时机

- 章节读完
- 全书读完
- 用户明确要求
- 出现重大关系图需求(人物关系 / 概念网络 / 论证链)

## 文件命名

`0001-<dash-case-主题>.html`

编号全书递增,主题用 dash-case。例:
- `books/三体/cards/0001-黑暗森林法则.html`
- `books/三体/cards/0002-人物关系图.html`

## 风格(Tufte 风)

- **排版**:衬线字体(如 `Georgia` 或 `Noto Serif CJK SC`),行高 1.6-1.8,最大宽度 720px 居中
- **留白**:padding 充分,正文字号 16-18px
- **注释风格**:借鉴 Tufte 的 sidenote 风格——正文旁的小字注释
- **无外部依赖**:纯 HTML + 内联 CSS,不引 CDN(可打印、离线可用)
- **深色/浅色**:默认浅色背景,`@media (prefers-color-scheme: dark)` 支持暗色

## 结构(支持主动回忆)

每张卡片分两面:

### 正面(问题)

```html
<section class="card-front question">
  <h1>[核心问题]</h1>
  <p class="hint">[可选:一个提示,降低检索难度]</p>
  <button class="reveal">点击查看答案</button>
</section>
```

### 背面(答案 + 关系图)

```html
<section class="card-back answer" hidden>
  <h2>答案</h2>
  <div class="answer-body">
    [完整答案,2-5 段]
  </div>
  <h2>关系图</h2>
  <div class="diagram">
    [SVG 内联关系图 或 Mermaid 渲染]
  </div>
  <h2>相关永久笔记</h2>
  <ul>
    <li><a href="../NOTES.md#书名-P001">书名-P001</a> — 关联点</li>
  </ul>
  <h2>出处</h2>
  <p>[章节 + weread 链接 或 外部资源链接]</p>
</section>
```

### 切换机制

用简单 JS(内联,无外部库):

```javascript
<script>
document.querySelector('.reveal').addEventListener('click', function() {
  const answer = document.querySelector('.answer');
  answer.hidden = !answer.hidden;
  this.textContent = answer.hidden ? '点击查看答案' : '隐藏答案';
});
</script>
```

## 关系图绘制

### 人物关系图(虚构书)

用内联 SVG。节点是人物,边是关系,边标签说明关系类型。

```html
<svg viewBox="0 0 600 400">
  <g class="node" transform="translate(100,100)">
    <circle r="30" fill="#eee" stroke="#333"/>
    <text text-anchor="middle">人物A</text>
  </g>
  <line x1="130" y1="100" x2="270" y2="200" stroke="#666"/>
  <text x="200" y="140">敌对</text>
  <!-- ... -->
</svg>
```

### 概念网络(非虚构)

同上,节点是概念,边是"支持/反对/依赖/派生"关系。

### 论证链(非虚构)

用 SVG 画"前提 → 中间结论 → 最终结论"的有向图。

## 复习时间表联动

卡片产出时,在 `~/reading/READING-LOG.md` 的复习时间表新增一行:

```
| 三体-P003 | books/三体/cards/0001-黑暗森林.html | 2026-06-13 | 2026-06-14 | 1天 | - |
```

下次抽考后更新:间隔推进、正确率记录。

## 可打印

- `@media print` 样式:隐藏「点击查看答案」按钮,答案始终显示,关系图用黑色描边
- A4 友好:最大宽度在打印时自动扩展

## 维护规则

- 卡片产出后**不删除**,只追加(保留学习轨迹)
- 用户反馈某张卡片"太浅/太深"时,可追加修订版,旧版保留并标注 `rev: 2`
- 每张卡片底部显示版本和产出日期
