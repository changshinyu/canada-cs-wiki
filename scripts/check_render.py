#!/usr/bin/env python3
"""節點 8：渲染檢查（無頭 Chrome）。
  1. 每一頁的內容區沒有溢出 1280×720 版面（垂直、水平）
  2. HTML 每頁的標題＋內文文字，和對應的逐頁稿一字不差（去掉空白與 markdown 符號後比對）
  3. 逐頁截圖到 slides/work/screens/NN.png
"""
import re, sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parent.parent
W = ROOT / "slides/work"
STRIP = re.compile(r"[\s#>*|`\-:?]")

def draft_text(p):
    m = re.match(r"---\n(.*?)\n---\n(.*)", p.read_text(encoding="utf-8"), re.S)
    title = re.search(r"^title:\s*(.*)$", m.group(1), re.M).group(1)
    body = re.sub(r"^\s*\|?[\s:\-|]+\|?\s*$", "", m.group(2), flags=re.M)
    return STRIP.sub("", title), STRIP.sub("", body)

def main():
    shots = W / "screens"; shots.mkdir(exist_ok=True)
    errors = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = b.new_page(viewport={"width": 1280, "height": 720})
        pg.goto((ROOT / "slides/deck.html").as_uri())
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        for k in range(n):
            info = pg.evaluate("""k=>{const s=[...document.querySelectorAll('.slide')];
              s.forEach((x,j)=>x.classList.toggle('on',j===k));const x=s[k],c=x.querySelector('.content');
              return {draft:x.dataset.draft,h:c.scrollHeight,ch:c.clientHeight,w:c.scrollWidth,cw:c.clientWidth,
                      title:x.querySelector('h1').textContent,body:c.textContent}}""", k)
            d = info["draft"]
            if info["h"] > info["ch"] + 1:
                errors.append(f"{d}: 垂直溢出 {info['h'] - info['ch']}px → 退回逐頁稿縮短")
            if info["w"] > info["cw"] + 1:
                errors.append(f"{d}: 水平溢出 {info['w'] - info['cw']}px → 退回逐頁稿縮短")
            t, body = draft_text(W / "drafts" / f"{d}.md")
            if STRIP.sub("", info["title"]) != t:
                errors.append(f"{d}: 標題和逐頁稿不一致")
            got = STRIP.sub("", info["body"]).replace("答", "")
            if got != body.replace("答", ""):
                errors.append(f"{d}: 內文和逐頁稿不一致（渲染改到字了）")
            pg.locator(".slide.on").screenshot(path=str(shots / f"{d}.png"))
        b.close()
    print(f"check_render：{n} 頁，截圖在 slides/work/screens/｜錯誤 {len(errors)}")
    for e in errors:
        print("  ✗", e)
    if not errors:
        print("  ✓ 全部通過")
    sys.exit(1 if errors else 0)

if __name__ == "__main__":
    main()
