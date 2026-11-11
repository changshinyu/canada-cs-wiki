# 加拿大 CS 碩士 LLM Wiki × 教學 HTML 簡報

生成式 AI 第 10 週作業：先用「先討論、後生成」建立 LLM Wiki，再用事先畫好的 graph 把 Wiki 做成教學 HTML 簡報。

- **簡報**：`slides/deck.html`（GitHub Pages：`/slides/deck.html`，方向鍵翻頁）
- **Wiki**：`wiki/index.md`
- **作業說明**（graph 設計、執行紀錄、反思）：`docs/submission.md`

## 資料夾
```
AGENTS.md / CLAUDE.md        Wiki 規則（由 docs/interview.md 的需求訪談產生）
docs/interview.md            先討論：10 題需求訪談紀錄
docs/wiki-review-1.md        Wiki 獨立 AI 審查紀錄
raw/                         原始來源摘錄（URL＋查詢日期＋官方/非官方）
wiki/                        LLM Wiki：programs/（7 學程）、topics/（4 主題）、index.md、log.md
.agents/workflows/topic-slides.md   簡報 graph 規格
slides/work/                 graph 每一關的產出：sources、cards、outline、drafts、review、run-log、report
slides/deck.html             成品
scripts/                     可以實際執行的檢查
```

## 重跑
```bash
python3 scripts/lint.py            # Wiki lint
python3 scripts/check_coverage.py  # 2 覆蓋率關卡
python3 scripts/check_cards.py     # 3a 證據卡檢查
python3 scripts/check_drafts.py    # 5a 稿件檢查（可加頁碼只查某幾頁）
python3 scripts/render_deck.py     # 7 渲染
python3 scripts/check_render.py    # 8 渲染檢查（需要 playwright＋Chrome）
```

資料查詢日期 2026-11-11。內容僅供學習，申請前請以各校與 IRCC 官網為準。
