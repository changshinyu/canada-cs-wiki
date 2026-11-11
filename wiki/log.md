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

## [2026-11-11] ingest #5 | Alberta MSc Computing Science
- raw：20261111-alberta-cs-grad-admissions（官方）、20261111-alberta-thirdparty-listing（非官方）
- 新增：programs/alberta-msc-cs.md；更新：index.md
- **重要更正**：訪談 Q3 說 Alberta 有 course-based，官方寫明 2021/7 起停辦 → 依官方，並在備註記錄更正
- lint 第 1 次：✗ 缺出處（更正說明那行含題號數字）→ 改寫並接上官方出處 → 通過

## [2026-11-11] ingest #6 | Dalhousie MACS
- raw：20261111-dalhousie-macs、20261111-dalhousie-macs-admission-process（皆官方）
- 新增：programs/dalhousie-macs.md；更新：index.md
- 官方頁本身有錯置段落（介紹 MDI）與過期標題 → 寫進爭議 / 備註
- 自我忠實度檢查：✗ 2 句跨學程比較（「7 個學程中最低」等）雖然有 [S:] 但 raw 沒寫，lint 抓不到 → 改成只陳述本校事實；跨校比較留給主題頁

## [2026-11-11] ingest #7 | Waterloo MMSc
- raw：20261111-waterloo-mmsc、20261111-waterloo-mse-dept-apply（皆官方）
- 新增：programs/waterloo-mmsc.md；更新：index.md
- lint 第 1 次：✗ 缺出處（「7 個學程裡唯一」跨校比較）、✗ 孤兒頁
- **流程修改**：跨校比較第 4 次出現 → AGENTS.md §4 加「學程頁禁止跨校比較」；scripts/lint.py 加第 8 項自動抓比較用語（把檢查從「事後回頭看」往前移到「每篇 ingest 的 lint」）
- 自我檢查：刪掉一句 raw 沒寫的推論（6/1 與線上 MMSc 相同）
- 新檢查第 8 項第一版誤判 3 處「最低 GPA」（門檻不是比較）→ 規則改成只抓「最低的」等比較級 → 通過
- 第二次誤判：McGill「學到最多的一次成就」→ 移除「最多的 / 最少的」
