# Onboarding

## 第一次进空书房（书房目录不存在或为空）

1. 创建书房目录结构（`mkdir -p`）。
2. **检查 weread API key**: 运行 `python3 "<SKILL_DIR>/fetch_book_data.py" --check`，若返回 `configured: false`，打开引导页 `open ~/.claude/skills/weread-skills/setup-guide.html`，等用户配好再继续。
3. 用 AskUserQuestion 问用户 3-5 个问题，据此初始化 `PROFILE.md`:
   - 读书口味（虚构 vs 非虚构，哪些领域）
   - 读书目标/动机
   - 每周大概阅读时间
   - 陪读强度（温和 vs grill）
4. 调 `/shelf/sync` 把用户书架同步进 `READING-LOG.md` 的"在读"段（最多 20 本最近更新）。
5. 创建初始 `RESOURCES.md`，预填 Adler/Ahrens/循证学习三条已查证源（见 RESOURCES-FORMAT.md）。

## 首次陪读某本书（`books/<书名>/` 不存在）

1. 用 weread 拉 bookId + 章节目录。
2. 问用户:
   - 为什么读这本书？→ 落地在 BOOK.md 的 mission
   - 想从这本书得到什么？→ 落地在 BOOK.md 的"想得到什么"
   - 书类型: 虚构还是非虚构？→ 决定招式切换
3. 跑一次**检视模式**: 读目录/序/结构，画出全书地图（落地在 BOOK.md）。
4. 创建 `books/<书名>/BOOK.md` 和空的 `NOTES.md`（三区骨架）。

## 进度追踪

- **数据源**: BOOK.md 的「上次进度」+ READING-LOG.md 会话索引 + weread `/book/getprogress`
- **节奏推算**: 前 3 次只记录不推算；第 4 次起计算平均每次阅读量，据此建议阅读范围
- **更新时机**: 开场拉 weread 确认进度；收尾用户报告后更新 BOOK.md + READING-LOG.md
