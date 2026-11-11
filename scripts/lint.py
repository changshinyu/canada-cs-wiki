#!/usr/bin/env python3
"""Wiki lint — AGENTS.md §7 的 1–6 項腳本檢查。
用法：python3 scripts/lint.py [--today YYYY-MM-DD]
結束碼：0 = 沒有錯誤（可能有警告），1 = 有錯誤。
"""
import re, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW, WIKI = ROOT / "raw", ROOT / "wiki"
REQUIRED = ["概要", "截止日", "申請文件", "語言門檻", "學費", "研究方向", "特色課程", "爭議 / 備註"]
CITE = re.compile(r"\[S:([^\]]+)\]")
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")

def parse_raw():
    meta = {}
    for f in sorted(RAW.glob("*.md")):
        txt = f.read_text(encoding="utf-8")
        m = re.match(r"---\n(.*?)\n---", txt, re.S)
        d = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M)) if m else {}
        meta[f.stem] = d
    return meta

def main():
    today = datetime.date.today()
    if "--today" in sys.argv:
        today = datetime.date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
    errors, warns = [], []
    raw = parse_raw()

    # raw 檔頭
    for stem, d in raw.items():
        for k in ("url", "retrieved", "type"):
            if k not in d:
                errors.append(f"[raw] {stem}: 檔頭缺少 {k}")
        if d.get("type") not in ("official", "unofficial"):
            errors.append(f"[raw] {stem}: type 必須是 official 或 unofficial")
        # 5. 過期
        try:
            age = (today - datetime.date.fromisoformat(d.get("retrieved", ""))).days
            if age > 183:
                warns.append(f"[5 過期] raw/{stem}: 查詢於 {d['retrieved']}，超過 6 個月，可能過期")
        except ValueError:
            errors.append(f"[raw] {stem}: retrieved 不是 YYYY-MM-DD")

    pages = sorted(WIKI.rglob("*.md"))
    inbound = {p.resolve(): 0 for p in pages}

    for p in pages:
        rel = p.relative_to(ROOT)
        lines = p.read_text(encoding="utf-8").splitlines()
        in_code = False
        for i, line in enumerate(lines, 1):
            if line.startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            # 3. 連結
            for target in LINK.findall(line):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                t = (p.parent / target).resolve()
                if not t.exists():
                    errors.append(f"[3 斷連結] {rel}:{i} → {target}")
                elif t in inbound and t != p.resolve():
                    inbound[t] += 1
            if p.name == "log.md" or p.name == "index.md":
                continue
            cites = CITE.findall(line)
            # 1. 數字要有出處
            body = CITE.sub("", LINK.sub("", line))
            stripped = line.strip()
            is_skip = (stripped.startswith("#") or re.fullmatch(r"\|?[\s:\-|]+\|?", stripped or "x")
                       or stripped.startswith(">"))
            if not is_skip and re.search(r"\d", body) and not cites:
                errors.append(f"[1 缺出處] {rel}:{i}: {stripped[:60]}")
            for c in cites:
                for stem in [s.strip() for s in c.split(",")]:
                    if stem not in raw:
                        errors.append(f"[1 出處不存在] {rel}:{i}: [S:{stem}]")
                    # 2. 非官方要標
                    elif raw[stem].get("type") == "unofficial" and "（非官方）" not in line:
                        errors.append(f"[2 未標非官方] {rel}:{i}: 引用 {stem} 但沒寫（非官方）")
        # 4. 學程頁固定欄位
        if p.parent.name == "programs":
            heads = {l[3:].strip() for l in lines if l.startswith("## ")}
            for h in REQUIRED:
                if h not in heads:
                    errors.append(f"[4 缺欄位] {rel}: 缺少「## {h}」")

    # 6. 孤兒頁
    for p, n in inbound.items():
        if p.name in ("index.md",):
            continue
        if n == 0:
            errors.append(f"[6 孤兒頁] {p.relative_to(ROOT)} 沒有任何頁面連到")

    print(f"lint：{len(pages)} 個 wiki 頁、{len(raw)} 篇 raw｜錯誤 {len(errors)}｜警告 {len(warns)}")
    for e in errors:
        print("  ✗", e)
    for w in warns:
        print("  ⚠", w)
    if not errors:
        print("  ✓ 全部通過")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
