# AGENTS.md — 加拿大 CS 碩士 LLM Wiki

依 Karpathy 的 LLM Wiki 構想建立，規則來自 `docs/interview.md` 的需求訪談（2026-11-11）。

## 1. 目的與讀者
- Wiki 給使用者本人當作申請加拿大資訊類碩士的知識庫。
- 之後要從 Wiki 產出：教學 HTML 簡報（給不熟此主題的台灣大學生）、選校清單 / 申請時程表、SOP 素材。

## 2. 資料夾
```
raw/              原始來源（只新增，不修改）。檔名：YYYYMMDD-<slug>.md，開頭寫 URL、查詢日期、來源類型
wiki/index.md     目錄：列出每一頁和一行說明
wiki/log.md       ingest / lint 紀錄（只往下追加）
wiki/programs/    一個學程一頁（7 頁）
wiki/topics/      主題頁：requirements.md、costs.md、pgwp-immigration.md、course-vs-thesis.md
slides/           簡報 graph 的工作區（見 slides/WORKFLOW.md）
scripts/          可以實際執行的檢查腳本
```
`raw/` 不放個資或機密文件。

## 3. 範圍：7 個學程
waterloo-mmath-cs、waterloo-mmsc、ubc-msc-cs、mcgill-msc-cs、sfu-msc-cs、alberta-msc-cs、dalhousie-macs
（`wiki/programs/<slug>.md`）。排除財金、財工學程。

## 4. 寫作規則
- 全中文，專有名詞第一次出現時附英文原文，例如「研究型碩士（thesis-based）」。
- **出處**：每個數字、日期、門檻都要在同一行接上出處標記 `[S:<raw 檔名>]`；`raw/` 檔案開頭要有 URL 和查詢日期。
- **來源類型**：官方（學校官網、IRCC、加拿大政府）為主。非官方來源（論壇、心得）只能當補充，該行要標 `（非官方）`。
- **矛盾處理**：以官方為準。非官方的說法放在該頁的「## 爭議 / 備註」，兩邊都標出處。
- 不確定或來源沒寫的，寫「官網未載明」，**不可以自己推測或補數字**。
- **學程頁只寫本校事實，禁止跨校比較**（「最低」「唯一」「比 X 高」「N 個學程中」等）。比較只能寫在 `wiki/topics/` 主題頁，並且同時引用每一校的 raw。（2026-11-11 加入：ingest #3、#5、#6、#7 都犯同一種錯）
- 頁面之間用相對連結 `[文字](../topics/costs.md)`。

## 5. 學程頁固定欄位（每頁都要有這些 `##` 標題）
`## 概要`、`## 截止日`、`## 申請文件`、`## 語言門檻`、`## 學費`、`## 研究方向`、`## 特色課程`、`## 爭議 / 備註`

## 6. Ingest 流程（一次一篇）
1. 用 WebFetch 讀取來源，把相關內容摘錄存進 `raw/`（附 URL、查詢日期、官方 / 非官方）。
2. 更新受影響的學程頁和主題頁；新頁面要加進 `index.md`。
3. 在 `log.md` 追加：日期、來源、變更了哪些頁。
4. 跑 `python3 scripts/lint.py`，全過才往下。
5. 向使用者回報變更，**使用者確認後才 commit**，再處理下一篇。

## 7. Lint（`scripts/lint.py` + AI 審查）
腳本檢查：
1. 含數字的內容行都有 `[S:...]`，而且指到存在的 raw 檔
2. 引用非官方 raw 的行都有標 `（非官方）`
3. 相對連結沒有斷
4. 學程頁的固定欄位齊全
5. raw 的查詢日期超過 6 個月 → 警告「可能過期」
6. 沒有孤兒頁（每頁都要被 index.md 或其他頁連到）
8. 學程頁不可以出現跨校比較用語（最低、最高、唯一、其他學校、個學程中…）

AI 審查（開新對話，只給主題頁和學程頁）：
7. 主題頁比較表的數字和學程頁一致

## 8. 不可以做的事
- 不改 `raw/` 已存在的檔案內容。
- 不用 raw 以外的知識補 Wiki。
- 不刪 log.md 的紀錄。
