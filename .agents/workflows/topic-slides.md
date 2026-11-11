# Workflow：/topic-slides — 從 Wiki 產生教學 HTML 簡報（Graph 版）

> 依講義〈把你的工作拆成 AI 能做的流程〉的 Graph 設計。流程是**事先畫好的**，每一關的產出都是檔案，可以單獨打開、放進 git、單獨重跑。
> 主題：「去加拿大讀資訊碩士，要知道什麼？」｜讀者：不熟這個主題的台灣大學生｜知識來源：**只能用 `wiki/`**

## 五件事
| | 內容 |
|---|---|
| 🎯 目標 | 只用 wiki，產出 10–14 頁、可直接瀏覽的教學 HTML 簡報 `slides/deck.html` |
| 🚧 限制 | 不可用 wiki 以外的知識；渲染節點不可改字；每一關只能看、改規定的檔案 |
| ✅ 完成標準 | 所有檢查腳本全過＋獨立 AI 審查無「錯誤」＋使用者確認大綱 |
| 🛑 停止條件 | 全過就交件；任何一個內圈 loop 改滿 2 輪仍不過 → 停下來回報；覆蓋率關卡的相關頁面少於 3 頁 → 一開始就停 |
| ⏰ 觸發 | 使用者說「/topic-slides」或 wiki 有大改版時 |

## Graph
```
[1 檢索 wiki] → <2 覆蓋率關卡> → [3 證據卡] → <3a 證據卡檢查> → [4 大綱] → (4a 使用者確認)
      ↑                │不足→停          ↑ 退回：重抽那一張卡            │退回→改大綱或補檢索
      └──────────── 缺主題 ─────────────────────────────────────────────┘
→ [5 逐頁稿] → <5a 稿件檢查> → <6 忠實度審查（獨立 AI）> → [7 渲染 HTML] → <8 渲染檢查> → [9 交件 report]
     ↑ 內圈：寫→檢查→修（≤2 輪）   │退回→只修那一頁              │溢出→退回逐頁稿縮短
```
`[ ]` = AI 節點　`< >` = 檢查關卡（腳本或審查）　`( )` = 人工確認

## 每一關只能看什麼、改什麼
| 節點 | 只能看 | 產出 | 不能做 |
|---|---|---|---|
| 1 檢索 wiki | `wiki/index.md`＋相關頁 | `slides/work/sources.md` | 讀 raw 以外的網路資料 |
| 2 覆蓋率關卡（腳本） | sources.md | 通過 / 停 | — |
| 3 證據卡 | sources.md 列出的 **一頁** wiki | `slides/work/cards/<page>.md` | 混用其他頁、寫 wiki 沒有的事實 |
| 3a 證據卡檢查（腳本） | cards＋wiki＋raw | 通過 / 退回該卡 | — |
| 4 大綱 | cards | `slides/work/outline.md` | 引用卡片以外的內容 |
| 5 逐頁稿 | outline＋該頁指定的卡 | `slides/work/drafts/NN.md` | 用指定卡以外的內容 |
| 5a 稿件檢查（腳本） | drafts＋cards | 通過 / 退回該頁 | — |
| 6 忠實度審查（**新的 AI，不帶製作記憶**） | drafts＋cards＋wiki | `slides/work/review.md` | 動手改稿（只能報告） |
| 7 渲染（腳本 `render_deck.py`） | 已通過的 drafts | `slides/deck.html` | **改任何一個字**（排版時想順句子？不行！） |
| 8 渲染檢查（腳本） | deck.html＋drafts | 截圖＋通過 / 退回 | — |
| 9 交件 | 全部檢查結果 | `slides/work/report.md` | — |

## 錯在哪一關，就退回哪一關
| 問題 | 退回到 | 只動 |
|---|---|---|
| 某頁說法和卡片不符 | 5 逐頁稿 | 那一頁，其他頁不動 |
| 卡片數字在 wiki / raw 找不到 | 3 證據卡 | 那一張卡 |
| 某頁字太多、渲染溢出 | 5 逐頁稿 | 縮短那一頁，**不是在渲染時硬塞** |
| 大綱缺主題 | 1 檢索 | 補檢索、補卡 |

## 檢查腳本
- `scripts/check_cards.py`：每個事實都有 wiki 頁＋raw 出處；**事實裡的每個數字都要同時出現在該 wiki 頁和 raw 原文**（英文月份會先換成數字）
- `scripts/check_drafts.py`：頁數 10–14；每頁至少引用 1 張卡；**每頁裡的數字都要出現在它引用的卡片裡**；每頁字數上限
- `scripts/render_deck.py`：drafts → deck.html（純腳本，沒有 AI，所以渲染不可能改字）
- `scripts/check_render.py`：用無頭瀏覽器開 deck.html，逐頁截圖，檢查①內容沒有溢出 16:9 畫面 ②HTML 裡的文字跟 drafts 一字不差

## 狀態都是檔案
```
slides/
  deck.html            成品
  work/
    sources.md         1 檢索結果
    cards/             3 證據卡
    outline.md         4 大綱
    drafts/            5 逐頁稿
    review.md          6 審查報告
    screens/           8 截圖（不進 git）
    report.md          9 交件報告＝執行與檢查紀錄
```
