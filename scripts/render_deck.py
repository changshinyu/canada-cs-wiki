#!/usr/bin/env python3
"""節點 7：渲染。slides/work/drafts/*.md → slides/deck.html
純腳本、沒有 AI：只做 markdown → HTML 轉換和套版，不可能改到任何一個字。
每頁頁尾自動列出「這頁用到的 wiki 頁面」（由 cards → 來源 wiki 推出），讓簡報和 wiki 的對應一目了然。
"""
import re, html, pathlib, markdown
ROOT = pathlib.Path(__file__).resolve().parent.parent
W = ROOT / "slides/work"

def card_sources():
    src = {}
    for p in (W / "cards").glob("*.md"):
        t = p.read_text(encoding="utf-8")
        wiki = re.search(r"來源 wiki：(\S+)", t).group(1)
        for cid in re.findall(r"^- \[([\w-]+)\]", t, re.M):
            src[cid] = wiki
    return src

def parse(p):
    m = re.match(r"---\n(.*?)\n---\n(.*)", p.read_text(encoding="utf-8"), re.S)
    meta = dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M))
    meta["cards"] = re.findall(r"[\w-]+", meta.get("cards", "").strip("[]"))
    return meta, m.group(2).strip()

def quiz(body):
    out = []
    for block in re.split(r"\n\s*\n", body):
        q = re.match(r"\?\?\? (.+)\n答：(.+)", block.strip(), re.S)
        if q:
            out.append(f'<details class="q"><summary>{html.escape(q.group(1))}</summary>'
                       f'<p>答：{html.escape(q.group(2).strip())}</p></details>')
    return "\n".join(out)

def render_body(meta, body):
    if meta["layout"] == "quiz":
        return quiz(body)
    h = markdown.markdown(body, extensions=["tables"])
    if meta["layout"] in ("split", "pitfalls", "big"):
        parts = re.split(r"(?=<h[23]>)", h)
        head, cols = parts[0], [x for x in parts[1:] if x.strip()]
        note = ""
        if cols and "<blockquote>" in cols[-1]:
            cols[-1], note = cols[-1].split("<blockquote>", 1)
            note = "<blockquote>" + note
        h = head + '<div class="cols">' + "".join(f'<div class="col">{c}</div>' for c in cols) + "</div>" + note
    return h

CSS = r"""
:root{--ink:#14213d;--muted:#5c6378;--accent:#c8102e;--paper:#fbf8f3;--line:#e6dfd3;--soft:#f3ede4}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#1d2333;font-family:"Noto Sans TC","Noto Sans CJK TC","PingFang TC","Microsoft JhengHei",sans-serif;color:var(--ink)}
#stage{position:fixed;inset:0;display:flex;align-items:center;justify-content:center}
.slide{position:absolute;width:1280px;height:720px;background:var(--paper);padding:64px 80px 70px;display:none;flex-direction:column;overflow:hidden;transform-origin:center center}
.slide.on{display:flex}
.slide::before{content:"";position:absolute;left:0;top:0;bottom:0;width:10px;background:var(--accent)}
.kicker{font-size:15px;letter-spacing:.18em;color:var(--accent);font-weight:700;margin-bottom:10px}
h1{font-size:44px;line-height:1.25;font-weight:800;margin-bottom:28px;letter-spacing:.01em}
.content{flex:1;font-size:24px;line-height:1.6;min-height:0}
.content ul{list-style:none}
.content li{position:relative;padding-left:28px;margin:8px 0}
.content li::before{content:"";position:absolute;left:4px;top:.62em;width:10px;height:10px;border-radius:2px;background:var(--accent)}
.content strong{color:var(--accent);font-weight:800}
.content h2{font-size:30px;margin:4px 0 8px;color:var(--ink)}
.content h3{font-size:24px;margin:0 0 8px;color:var(--accent)}
.content p{margin:6px 0}
table{width:100%;border-collapse:collapse;font-size:22px;background:#fff;border:1px solid var(--line)}
th,td{padding:12px 16px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--ink);color:#fff;font-weight:700}
td:first-child{font-weight:700;color:var(--muted);white-space:nowrap}
blockquote{margin-top:20px;padding:12px 18px;background:var(--soft);border-left:4px solid var(--ink);font-size:20px;color:var(--muted)}
.cols{display:flex;gap:28px}
.col{flex:1;background:#fff;border:1px solid var(--line);border-radius:10px;padding:20px 22px;font-size:21px}
.layout-big .col h2{font-size:28px;color:var(--accent)}
.layout-timeline .content li{padding-left:0;margin:0;display:flex;gap:24px;align-items:baseline;border-left:3px solid var(--line);padding:8px 0 8px 26px}
.layout-timeline .content li::before{left:-8px;top:18px;width:13px;height:13px;border-radius:50%}
.layout-timeline .content li strong{min-width:170px;font-size:26px;color:var(--ink)}
.layout-checklist .content li{font-size:22px;margin:10px 0}
.layout-agenda .content li{font-size:30px;margin:18px 0}
.layout-cover,.layout-end{background:var(--ink);color:#fff}
.layout-cover h1{font-size:60px;margin-top:150px;color:#fff}
.layout-cover .content{color:#d7dbe6;font-size:26px}
.layout-cover .content p:last-child{margin-top:28px;font-size:20px;letter-spacing:.06em;color:#9aa3b8}
.layout-end h1{color:#fff}.layout-end .content{color:#e7eaf2}.layout-end .content strong{color:#ff8a8a}
.layout-end blockquote{background:rgba(255,255,255,.08);border-color:#ff8a8a;color:#cfd5e3}
.layout-cover .kicker,.layout-end .kicker{color:#ff8a8a}
details.q{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 20px;margin:12px 0;font-size:23px}
details.q summary{cursor:pointer;font-weight:700;list-style:none}
details.q summary::before{content:"Q";display:inline-block;width:30px;height:30px;line-height:30px;text-align:center;border-radius:50%;background:var(--accent);color:#fff;margin-right:12px;font-size:17px}
details.q p{margin-top:10px;color:var(--muted);padding-left:42px}
.foot{position:absolute;left:80px;right:80px;bottom:22px;display:flex;justify-content:space-between;font-size:13px;color:#9a917f}
.layout-cover .foot,.layout-end .foot{color:#7f89a3}
#bar{position:fixed;left:0;bottom:0;height:4px;background:var(--accent);transition:width .25s}
#nav{position:fixed;right:18px;bottom:14px;display:flex;gap:8px}
#nav button{background:rgba(255,255,255,.12);color:#fff;border:0;border-radius:6px;padding:6px 12px;font-size:15px;cursor:pointer}
@media print{#nav,#bar{display:none}.slide{display:flex!important;position:relative;transform:none!important;page-break-after:always}#stage{position:static;display:block}}
"""

JS = r"""
const S=[...document.querySelectorAll('.slide')];let i=0;
function fit(){const k=Math.min(innerWidth/1280,innerHeight/720)*0.96;S.forEach(s=>s.style.transform=`scale(${k})`)}
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,j)=>s.classList.toggle('on',j===i));
document.getElementById('bar').style.width=((i+1)/S.length*100)+'%';history.replaceState(null,'','#'+(i+1))}
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))go(i+1);if(['ArrowLeft','PageUp'].includes(e.key))go(i-1)});
addEventListener('resize',fit);document.getElementById('prev').onclick=()=>go(i-1);document.getElementById('next').onclick=()=>go(i+1);
fit();go((parseInt(location.hash.slice(1))||1)-1);
"""

def main():
    src = card_sources()
    files = sorted((W / "drafts").glob("*.md"))
    slides = []
    for k, p in enumerate(files, 1):
        meta, body = parse(p)
        wikis = sorted({src[c] for c in meta["cards"] if c in src})
        foot_src = "來源：" + "、".join(wikis) if wikis else "來源：本專案 LLM Wiki"
        slides.append(
            f'<section class="slide layout-{meta["layout"]}" data-draft="{p.stem}">'
            f'<div class="kicker">加拿大 CS 碩士入門 · {k:02d}</div>'
            f'<h1>{html.escape(meta["title"])}</h1>'
            f'<div class="content">{render_body(meta, body)}</div>'
            f'<div class="foot"><span>{html.escape(foot_src)}</span><span>{k} / {len(files)}</span></div>'
            f'</section>')
    doc = f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>去加拿大讀資訊碩士，要知道什麼？</title><style>{CSS}</style></head>
<body><div id="stage">{''.join(slides)}</div><div id="bar"></div>
<div id="nav"><button id="prev" aria-label="上一頁">←</button><button id="next" aria-label="下一頁">→</button></div>
<script>{JS}</script></body></html>"""
    out = ROOT / "slides/deck.html"
    out.write_text(doc, encoding="utf-8")
    print(f"render_deck：{len(files)} 頁 → {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
