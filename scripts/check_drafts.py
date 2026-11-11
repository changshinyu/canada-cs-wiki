#!/usr/bin/env python3
"""節點 5a：逐頁稿檢查。
  1. 頁數 10–14
  2. 每頁 frontmatter 有 layout、title、cards；除了 cover / agenda / end，每頁至少引用 1 張卡
  3. 引用的卡都存在
  4. 每頁（標題＋內文）裡的每個數字，都要出現在它引用的卡片裡（沒引用卡的頁不能有數字）
  5. 每頁字數上限 MAX_CHARS（去掉 markdown 符號後）
用法：python3 scripts/check_drafts.py [頁碼 ...]   只檢查指定頁（給「只修那一頁」的退回用）
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
W = ROOT / "slides/work"
MAX_CHARS = 260
NUM = re.compile(r"\d+(?:[.,]\d+)*")
NO_CARD_OK = {"cover", "agenda", "end"}

def nums(t): return {n.replace(",", "") for n in NUM.findall(t)}

def load_cards():
    cards = {}
    for p in (W / "cards").glob("*.md"):
        for m in re.finditer(r"^- \[([\w-]+)\] (.+)$", p.read_text(encoding="utf-8"), re.M):
            cards[m.group(1)] = re.sub(r"\[S:[^\]]+\]", "", m.group(2))
    return cards

def parse(p):
    txt = p.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", txt, re.S)
    if not m:
        return None, txt
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    meta["cards"] = re.findall(r"[\w-]+", meta.get("cards", "").strip("[]"))
    return meta, m.group(2)

def plain(body):
    t = re.sub(r"^\s*\|?[\s:\-|]+\|?\s*$", "", body, flags=re.M)
    t = re.sub(r"[#>*|`]|\?\?\?|^- ", "", t, flags=re.M)
    return re.sub(r"\s+", "", t)

def main():
    only = set(sys.argv[1:])
    cards = load_cards()
    files = sorted((W / "drafts").glob("*.md"))
    errors = []
    if not only and not (10 <= len(files) <= 14):
        errors.append(f"頁數 {len(files)} 不在 10–14")
    for p in files:
        if only and p.stem not in only:
            continue
        meta, body = parse(p)
        if meta is None:
            errors.append(f"{p.name}: 沒有 frontmatter"); continue
        for k in ("layout", "title"):
            if not meta.get(k):
                errors.append(f"{p.name}: 缺少 {k}")
        cs = meta["cards"]
        if not cs and meta.get("layout") not in NO_CARD_OK:
            errors.append(f"{p.name}: 沒有引用任何證據卡")
        allowed = set()
        for c in cs:
            if c not in cards:
                errors.append(f"{p.name}: 引用的卡 {c} 不存在")
            else:
                allowed |= nums(cards[c])
        for n in sorted(nums(meta.get("title", "") + body)):
            if n not in allowed:
                errors.append(f"{p.name}: 數字 {n} 不在引用的卡片 {cs or '（無）'} 裡")
        n_chars = len(plain(body))
        if n_chars > MAX_CHARS:
            errors.append(f"{p.name}: 內文 {n_chars} 字，超過上限 {MAX_CHARS}")
    print(f"check_drafts：{len(files)} 頁{'（只查 ' + ','.join(sorted(only)) + '）' if only else ''}｜錯誤 {len(errors)}")
    for e in errors:
        print("  ✗", e)
    if not errors:
        print("  ✓ 全部通過")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
