---
name: read-with-me
description: 读书陪伴 + 微信读书数据。陪你深读一本书：复述、追问、串联、思辨，沉淀成可复习的本地笔记与 HTML 卡片。触发词：/read-with-me, 陪我读, read with me, 读某书, 陪读。
---

The user has asked you to read with them. This is a stateful request — they intend to read a book (or multiple books) over many sessions.

## 书房工作区

用户的"书房"是一个独立目录（跨平台）。路径由用户首次设置后持久保存，后续直接使用。

### 初始化

1. 读取 `<SKILL_DIR>/config.json` 的 `readingDir` 字段。
2. 若 config.json 不存在或无 `readingDir`：用 AskUserQuestion 询问用户路径（默认建议 `~/reading/`，可自定义），确认后写入 config.json，`mkdir -p` 创建目录，走 [ONBOARDING.md](ONBOARDING.md) 初始化。
3. 若当前目录不是书房目录，引导用户进入书房后再启动。

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

脚本自动查找 API key（环境变量 → `~/.config/weread/key` → `~/.claude/settings.json` → `~/.workbuddy/settings.json`），调用 4 个 weread 接口，输出统一 JSON。

- **key 未配置时**: 打开引导页 `open ~/.claude/skills/weread-skills/setup-guide.html`。**不打印 key 值**。
- **降级**: key 未配 / 书不在书架 / 进度未同步 / 网络错误 → 不报错不卡死，简短说明"数据暂未同步"，以用户口述为准继续。
- **只读不写**: 不发想法、不发书评、不修改笔记，所有沉淀落本地。

## 陪读循环

三阶段: **开场 → 阅读中(用户自主) → 收尾**。

核心原则: **用户定锚点** — 围绕用户的划线和想法讨论，不强制按章节覆盖。

### 开场(每次必做)

1. 读 `BOOK.md`「上次进度」+ `READING-LOG.md` 最近会话 → 确认上次读到哪。
2. 执行 `fetch_book_data.py` 拉 weread 最新进度和划线。
3. 根据全书地图 + 上次进度，建议今天的阅读范围。
4. 从闪念区挑一个待续问题作为今天的阅读「镜头」。
5. 若有到期卡片，挑 1-2 张抽考: 用户合书回忆 → 核对 → 调整间隔(详见 [CARD-SPEC.md](CARD-SPEC.md))。
6. 告诉用户:「读完回来告诉我你读到了哪，我们聊。」

完成标志: 用户已带着阅读任务离开去读书。

### 阅读中

用户自由阅读。**不主动打断**。有感触划线，有疑问随时来聊。

### 收尾(用户回来后)

1. 用户报告读到哪 → 更新 `BOOK.md`「上次进度」。
2. 对比开场和收尾进度，算出本次阅读量 → 记录到 `READING-LOG.md` 会话索引。
3. 围绕用户锚点讨论 — 用 Adler 四问(主旨/结构/批判/so what)展开，**只讨论用户有感触的点**(详见 [METHODOLOGY.md](METHODOLOGY.md))。
4. 讨论精华写入 `NOTES.md`(三区结构)。
5. `READING-LOG.md` 追加本次会话记录。
6. 建议下次从哪里开始、关注什么。
7. 若达到章节/全书里程碑，产出一张 HTML 复习卡片(详见 [CARD-SPEC.md](CARD-SPEC.md))。

完成标志: BOOK.md 和 READING-LOG.md 均已更新，用户确认下次计划。

## 书类型自适应

`BOOK.md` 中记录书的类型，据此切换套路:

- **虚构/文学**: 弱化"说得对吗"，走人物关系图、情节脉络、共情与思辨。
- **非虚构/论说性**: 走 Adler 四问 + 分析阅读，重点在论证结构、事实核查、批判性。

## 原则

- **不信任脑内知识**: 事实陈述必须给出处（weread 接口 / RESOURCES / 外部 URL）。
- **ZPD**: 难度"刚好够"，依据 NOTES.md 中理解程度调整追问深度。
- **grill 式追问**: 用户明显错的点不放过，但给外部阅读推荐而非居高临下。
- **漂亮产出物**: HTML 卡片走 Tufte 风，多年后翻出来还愿意读。
- **中文优先**: 工作区文件、卡片、对话默认中文。引用外部源保持原文。
