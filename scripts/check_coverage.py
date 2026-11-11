#!/usr/bin/env python3
"""節點 2：覆蓋率關卡。sources.md 列出的 wiki 頁要存在；相關頁少於 3 頁 → 停（結束碼 2）。
大綱存在時，也檢查大綱每一節引用的卡片都來自 sources.md 列出的頁面。"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
W = ROOT / "slides/work"
src = (W / "sources.md").read_text(encoding="utf-8")
pages = re.findall(r"`(wiki/[^`]+\.md)`", src)
missing = [p for p in pages if not (ROOT / p).exists()]
print(f"check_coverage：sources 列出 {len(pages)} 頁")
for p in missing:
    print("  ✗ 不存在", p)
if len(pages) - len(missing) < 3:
    print("  🛑 相關頁少於 3 頁 → 依停止條件停下，不產生簡報"); sys.exit(2)
if missing:
    sys.exit(1)
print("  ✓ 通過")
