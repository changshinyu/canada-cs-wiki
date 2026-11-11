#!/usr/bin/env python3
"""節點 3a：證據卡檢查。
每張卡 = slides/work/cards/<wiki-page-stem>.md，每個事實一行：
  - [<card-id>] <事實> [S:<raw-stem>]
規則：
  1. 卡片標頭要有「來源 wiki：wiki/...md」，而且只能有一個來源頁（不可混用）
  2. 每個事實都要有 [S:raw]，raw 要存在，而且該 wiki 頁有引用這篇 raw
  3. 事實裡的每個數字，都要同時出現在該 wiki 頁、以及 raw 原文（英文月份先換成數字）
  4. card-id 全域唯一
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
CARDS = ROOT / "slides/work/cards"
MONTHS = {m: str(i) for i, m in enumerate(
    ["January","February","March","April","May","June","July","August",
     "September","October","November","December"], 1)}
NUM = re.compile(r"\d+(?:[.,]\d+)*")

def nums(text):
    return {n.replace(",", "") for n in NUM.findall(text)}

def norm_raw(text):
    for m, i in MONTHS.items():
        text = re.sub(rf"\b{m}\b", f" {i} ", text)
    return text

def main():
    errors, ids, total = [], {}, 0
    for card in sorted(CARDS.glob("*.md")):
        txt = card.read_text(encoding="utf-8")
        srcs = re.findall(r"來源 wiki：(\S+)", txt)
        if len(srcs) != 1:
            errors.append(f"{card.name}: 必須剛好有 1 個「來源 wiki」，找到 {len(srcs)}")
            continue
        wiki = ROOT / srcs[0]
        if not wiki.exists():
            errors.append(f"{card.name}: 來源 wiki 不存在 {srcs[0]}"); continue
        wtxt = wiki.read_text(encoding="utf-8")
        wnums = nums(re.sub(r"\[S:[^\]]+\]", "", wtxt))
        for i, line in enumerate(txt.splitlines(), 1):
            m = re.match(r"- \[([\w-]+)\] (.+)$", line)
            if not m:
                continue
            total += 1
            cid, body = m.groups()
            if cid in ids:
                errors.append(f"{card.name}:{i} card-id 重複 {cid}（也在 {ids[cid]}）")
            ids[cid] = card.name
            cites = re.findall(r"\[S:([^\]]+)\]", body)
            if not cites:
                errors.append(f"{card.name}:{i} [{cid}] 沒有 [S:raw]"); continue
            stems = [s.strip() for c in cites for s in c.split(",")]
            rawtxt = ""
            for s in stems:
                rp = ROOT / "raw" / f"{s}.md"
                if not rp.exists():
                    errors.append(f"{card.name}:{i} [{cid}] raw 不存在 {s}"); continue
                if s not in wtxt:
                    errors.append(f"{card.name}:{i} [{cid}] wiki 頁 {srcs[0]} 沒有引用 {s}")
                rawtxt += norm_raw(rp.read_text(encoding="utf-8"))
            claim = re.sub(r"\[S:[^\]]+\]", "", body)
            rnums = nums(rawtxt)
            for n in sorted(nums(claim)):
                if n not in wnums:
                    errors.append(f"{card.name}:{i} [{cid}] 數字 {n} 不在 wiki 頁 {srcs[0]}")
                if n not in rnums:
                    errors.append(f"{card.name}:{i} [{cid}] 數字 {n} 不在 raw {','.join(stems)}")
    print(f"check_cards：{len(list(CARDS.glob('*.md')))} 張卡、{total} 個事實｜錯誤 {len(errors)}")
    for e in errors:
        print("  ✗", e)
    if not errors:
        print("  ✓ 全部通過")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
