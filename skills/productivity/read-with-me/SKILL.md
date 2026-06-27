---
name: read-with-me
description: 读书陪伴 + 微信读书数据。陪你深读一本书：复述、追问、串联、思辨，沉淀成可复习的本地笔记与 HTML 卡片。支持智能推荐下一本书。触发词：/read-with-me, 陪我读, read with me, 读某书, 陪读, 推荐一本书, 下一本读什么。
---

The user has asked you to read with them. This is a stateful request — they intend to read a book (or multiple books) over many sessions.

## 书房工作区

用户的"书房"是一个独立目录（跨平台）。路径由用户首次设置后持久保存，后续直接使用。

### 初始化

1. 读取 `<SKILL_DIR>/config.json` 的 `readingDir` 字段。若存在且目录有效（含 `PROFILE.md`），直接使用。
2. 若 config.json 不存在或目录无效，**自动发现**：依次检查以下路径，找到含 `PROFILE.md` 的即为书房：
   - `~/reading`
   - 当前工作目录
   - `~/Documents/reading`
3. 若自动发现成功，写入 config.json 持久化，跳过询问。
4. 若仍未找到：用 AskUserQuestion 询问用户路径（默认建议 `~/reading/`，可自定义），确认后写入 config.json，`mkdir -p` 创建目录，走 [ONBOARDING.md](ONBOARDING.md) 初始化。

> Write 工具不接受 `~`，写入文件时须先 `echo ~/reading` 展开为绝对路径。

### 工作区结构

```
<readingDir>/
  PROFILE.md              # 阅读偏好(见 PROFILE-FORMAT.md)
  READING-LOG.md          # 跨书时间线 + 会话索引 + 复习时间表(见 READING-LOG-FORMAT.md)
  RESOURCES.md            # 方法论资源(见 RESOURCES-FORMAT.md)
  GLOSSARY.md             # (按需) 跨书人物/概念表
  books/<书名>/
    BOOK.md               # 元信息 + 全书地图 + 进度(见 BOOK-FORMAT.md)
    NOTES.md              # 三区笔记(见 BOOK-NOTES-FORMAT.md)
    cards/*.html          # 复习卡片(见 CARD-SPEC.md)
```

每次生成/更新工作区文件，严格遵循对应 `*-FORMAT.md` 模板。

## weread 数据

**必须用 helper 脚本取数**，不手写 curl:

```bash
python3 "<SKILL_DIR>/fetch_book_data.py" <bookId>
```

脚本自动查找 API key（环境变量 → `~/.config/weread/key` → `~/.claude/settings.json` → `~/.workbuddy/settings.json`），调用 5 个 weread 接口，输出统一 JSON：
- `/book/getprogress` — 阅读进度
- `/book/bookmarklist` — 个人划线（浅思考）
- `/book/bestbookmarks` — 热门划线
- `/book/info` — 书籍信息
- `/review/list/mine` — **个人评论/想法（深思考，优先级最高）**

### 数据优先级

陪读讨论时，数据优先级从高到低：
1. **userReviews**（个人评论/想法）— 用户的深思考，讨论的核心锚点
2. **userHighlights**（个人划线）— 用户的浅思考，可深挖的素材
3. **popularHighlights**（热门划线）— 其他读者的关注点，可作为补充视角

- **key 未配置时**: 打开引导页 `open ~/.claude/skills/weread-skills/setup-guide.html`。**不打印 key 值**。
- **降级**: key 未配 / 书不在书架 / 进度未同步 / 网络错误 → 不报错不卡死，简短说明"数据暂未同步"，以用户口述为准继续。
- **只读不写**: 不发想法、不发书评、不修改笔记，所有沉淀落本地。

## 陪读循环

三阶段: **开场 → 阅读中(用户自主) → 收尾**。

核心原则:
- **评论优先** — 用户的评论/想法（`userReviews`）是深思考，是讨论的核心锚点；划线是浅思考，可追问深挖。
- **用户定锚点** — 围绕用户的评论和划线讨论，不强制按章节覆盖。
- **一次一问** — 每次回复只抛一个问题，等用户回答后再进下一个。禁止一次性罗列多个问题或多个角度。追问是乒乓，不是连珠炮。

### 开场(每次必做)

1. 读 `BOOK.md`「上次进度」+ `READING-LOG.md` 最近会话 → 确认上次读到哪。
2. 执行 `fetch_book_data.py` 拉 weread 最新数据（进度 + 划线 + **评论**）。
3. **优先读评论**：`userReviews` 是用户的深思考，是讨论的核心锚点。新评论直接作为今日讨论的切入点。
4. 根据全书地图 + 上次进度，建议今天的阅读范围。
5. 从闪念区挑一个待续问题作为今天的阅读「镜头」。
6. 若有到期卡片，挑 1-2 张抽考: 用户合书回忆 → 核对 → 调整间隔(详见 [CARD-SPEC.md](CARD-SPEC.md))。
7. 告诉用户:「读完回来告诉我你读到了哪，我们聊。」

完成标志: 用户已带着阅读任务离开去读书。

### 阅读中

用户自由阅读。**不主动打断**。有感触划线，有疑问随时来聊。

### 收尾(用户回来后)

1. 用户报告读到哪 → 更新 `BOOK.md`「上次进度」。
2. 对比开场和收尾进度，算出本次阅读量 → 记录到 `READING-LOG.md` 会话索引。
3. 重新拉取 weread 数据（含新增评论）。
4. **围绕用户评论讨论** — `userReviews` 是深思考，优先作为讨论锚点；划线是浅思考，可追问深挖。用 Adler 四问(主旨/结构/批判/so what)展开(详见 [METHODOLOGY.md](METHODOLOGY.md))。
5. 讨论精华写入 `NOTES.md`(三区结构)，评论可直接加工为永久笔记。
6. `READING-LOG.md` 追加本次会话记录。
7. 建议下次从哪里开始、关注什么。
8. 若达到章节/全书里程碑，产出一张 HTML 复习卡片(详见 [CARD-SPEC.md](CARD-SPEC.md))。

完成标志: BOOK.md 和 READING-LOG.md 均已更新，用户确认下次计划。

## 书类型自适应

`BOOK.md` 中记录书的类型，据此切换套路:

- **虚构/文学**: 弱化"说得对吗"，走人物关系图、情节脉络、共情与思辨。
- **非虚构/论说性**: 走 Adler 四问 + 分析阅读，重点在论证结构、事实核查、批判性。

## 推荐下本书

### 触发时机

- 收尾时用户说"推荐下一本"
- 用户主动说"推荐一本书" / "下一本读什么"
- 读完一本书时自动建议

### 数据源

| 维度 | 来源 | 说明 |
|------|------|------|
| 口味 | `PROFILE.md` | 偏好领域（如 AI、投资理财、小说）、禁忌 |
| 历史 | `READING-LOG.md` | 在读/读完/想读列表 |
| 深思考 | 最近一本书的 `userReviews` | 用户评论/想法，体现真实兴趣 |
| AI 讨论 | 最近一本书的 `NOTES.md` 永久笔记 | 经过加工的核心观点 |

### 流程

1. 读 `READING-LOG.md` → 找到最近更新最晚的书（在读优先），取其 `bookId`
2. 读 `PROFILE.md` → 提取偏好领域（每个领域一个关键词）+ 禁忌
3. 读最近一本书的 `NOTES.md` → 提取永久笔记主题（作为推荐理由的素材）
4. 执行推荐脚本，每个领域一个 `--search`:
   ```bash
   python3 "<SKILL_DIR>/recommend_book.py" <bookId> --search "AI" --search "投资" --search "小说"
   ```
   脚本调用 weread API（个性化推荐 + 相似书 + 关键词搜索），按 bookId 去重后输出候选 JSON。
5. AI 交叉筛选:
   - **排除**「读完」的书
   - **保留**「在读」的书
   - **标注**「想读」列表中命中的候选:「你之前标记过想读」
   - 匹配口味领域
   - 关联用户最近评论/讨论中的观点
6. **虚实搭配提示**: 若最近连续读非虚构 → 提示「要不要换换口味？」（软提示，不强制过滤）
7. **按领域分组输出**: 每个领域推荐一本，每本含:
   - 书名、作者、评分、类型标签（虚构/非虚构）
   - **推荐理由**（引用用户具体评论/观点，如"你在《浪潮将至》中提到'码农本农'，这本书深入探讨 AI 对职业的影响"）
   - 来源标记（个性化推荐 / 相似书 / 关键词搜索）

### 降级

- **无评论** → 用划线 + 热门划线作为推荐依据
- **API 失败** → 不报错不卡死，说明情况，以 skill 自身判断推荐

### 示例输出

```
📚 推荐下本书

🤖 AI 方向
《XXX》— 作者 · 评分 85 · 非虚构
理由: 你在《浪潮将至》里评论"码农本农"，这本书深入探讨 AI 对程序员职业的冲击…
来源: 关键词搜索 "AI"

💰 投资理财
《YYY》— 作者 · 评分 78 · 非虚构
理由: 你最近在读的几本都偏技术视角，这本从投资角度…
来源: 个性化推荐

📖 小说
《ZZZ》— 作者 · 评分 92 · 虚构
理由: 你最近连续读了三本非虚构，换换口味？这本…
来源: 关键词搜索 "小说"
```

## 原则

- **不信任脑内知识**: 事实陈述必须给出处（weread 接口 / RESOURCES / 外部 URL）。
- **ZPD**: 难度"刚好够"，依据 NOTES.md 中理解程度调整追问深度。
- **grill 式追问**: 用户明显错的点不放过，但给外部阅读推荐而非居高临下。
- **漂亮产出物**: HTML 卡片走 Tufte 风，多年后翻出来还愿意读。
- **中文优先**: 工作区文件、卡片、对话默认中文。引用外部源保持原文。
