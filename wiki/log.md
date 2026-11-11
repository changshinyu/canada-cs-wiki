# Log

只往下追加。格式：`## [日期] 動作 | 來源` + 變更頁面清單。

## [2026-11-11] init
- 依 docs/interview.md 的需求摘要建立 AGENTS.md、資料夾、scripts/lint.py

## [2026-11-11] ingest #1 | Waterloo MMath CS
- raw：20261111-waterloo-mmath-cs、20261111-waterloo-cs-grad-faq、20261111-ets-toefl-score-scale
- 新增：programs/waterloo-mmath-cs.md；更新：index.md
- 發現：同一官方頁 TOEFL 有兩種寫法（5 vs 93）→ 補 ETS 新制來源，放在「爭議 / 備註」
- 自我檢查抓到：初稿有兩句不在 raw 裡的知識（TOEFL 新制、舊版手冊組別），違反 AGENTS.md §8 → 前者補 ETS 來源，後者刪除

## [2026-11-11] ingest #2 | UBC MSc CS
- raw：20261111-ubc-msc-cs
- 新增：programs/ubc-msc-cs.md；更新：index.md
- lint 第 1 次：✗ 孤兒頁（忘了加進 index）→ 補上 index 連結 → 通過
- 自我檢查：初稿把「$」寫成「加幣」屬於推測 → 改回頁面原文

## [2026-11-11] ingest #3 | McGill MSc CS
- raw：20261111-mcgill-msc-admission、20261111-mcgill-cs-deadlines-faq
- 新增：programs/mcgill-msc-cs.md；更新：index.md
- 發現矛盾 2 處（截止日新舊網址、TOEFL 分項）→ 依 AGENTS.md §4 以現行官方頁為準，寫進「爭議 / 備註」
- 本頁學費、研究方向、課程官網未載明 → 標「官網未載明於本頁」，不自行補
- lint 第 1 次：✗ 缺出處（一句跨學程的綜合比較寫在學程頁、沒有出處）→ 刪除，比較留給主題頁 → 通過

## [2026-11-11] ingest #4 | SFU MSc Computing Science
- raw：20261111-sfu-cs-grad-apply、20261111-sfu-msc-calendar（官方）、20261111-sfu-english-thirdparty（非官方，第一篇）
- 新增：programs/sfu-msc-cs.md；更新：index.md
- 官方頁沒有語言門檻 → 第三方分數標（非官方），放進爭議 / 備註，列為待補
- 一個官方網址（computing/.../admissions.html）WebFetch 只拿到導覽頁 → 改抓 FAS 申請頁
