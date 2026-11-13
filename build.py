"""Genera il sito statico in docs/ a partire da data/data.json."""
import json, pathlib, html, shutil
from registry import COUNTRIES, REGIONS
LANGS = {"it": 3, "en": 4}   # indice del nome nel registry
T = {
 "it": {"title":"Quota di mercato delle auto elettriche","sub":"Ultimo dato disponibile per paese, da fonti ufficiali","country":"Paese","last":"Ultimo dato","share":"Quota BEV","nodata":"in arrivo","home":"Home","sources":"Fonti dei dati","history":"Storico","month":"Mese","total":"Immatricolazioni","bev":"BEV","src":"Fonte","back":"Tutti i paesi","note":"Quota BEV = auto 100% elettriche sul totale delle nuove immatricolazioni di auto. I metodi di classificazione cambiano da paese a paese."},
 "en": {"title":"Electric car market share","sub":"Latest available data by country, from official sources","country":"Country","last":"Latest data","share":"BEV share","nodata":"coming soon","home":"Home","sources":"Data sources","history":"History","month":"Month","total":"Registrations","bev":"BEV","src":"Source","back":"All countries","note":"BEV share = fully electric cars as a share of new car registrations. Classification methods differ between countries."},
}
CSS = """
:root{--bg:#f2f4f3;--ink:#13211c;--mute:#5d6b65;--line:#d6dcd9;--bar:#0f8a5f;--track:#e1e6e3;--card:#fff}
@media(prefers-color-scheme:dark){:root{--bg:#0f1714;--ink:#e6efea;--mute:#93a39b;--line:#26332d;--bar:#3fd19a;--track:#1c2823;--card:#141e1a}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 'IBM Plex Sans',system-ui,sans-serif}
a{color:inherit}a:focus-visible{outline:2px solid var(--bar);outline-offset:2px}
header,main,footer{max-width:860px;margin:0 auto;padding:0 20px}
header{display:flex;justify-content:space-between;align-items:center;padding-top:20px;padding-bottom:20px;gap:16px;flex-wrap:wrap}
nav a{margin-right:16px;text-decoration:none;color:var(--mute)}nav a:hover{color:var(--ink)}
.brand{font-weight:700;text-decoration:none;margin-right:24px}
h1{font-size:clamp(1.8rem,5vw,2.6rem);line-height:1.1;margin:28px 0 6px;letter-spacing:-.02em}
.sub{color:var(--mute);margin:0 0 28px}
h2{font-size:1rem;margin:32px 0 8px;color:var(--mute);font-weight:600}
table{width:100%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
th,td{padding:10px 14px;text-align:left;border-bottom:1px solid var(--line)}th{font-size:.85rem;color:var(--mute);font-weight:500}
tr:last-child td{border-bottom:0}td.n,th.n{text-align:right;font-variant-numeric:tabular-nums}
.bar{display:flex;align-items:center;gap:10px;justify-content:flex-end}
.track{flex:0 1 140px;height:8px;background:var(--track);border-radius:4px;overflow:hidden;min-width:60px}
.fill{height:100%;background:var(--bar)}.pct{min-width:58px;font-weight:600}
.none{color:var(--mute)}.wrap{overflow-x:auto}
footer{padding-top:32px;padding-bottom:40px;color:var(--mute);font-size:.88rem}
select{background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:4px 8px}
"""
def pct(m): return None if not m or not m.get("total") else 100*m["bev"]/m["total"]
def fmt(x,lang): s=f"{x:.1f}"; return (s.replace(".",",") if lang=="it" else s)+" %"
def page(lang, title, body, depth):
    t=T[lang]; root="../"*depth; other="en" if lang=="it" else "it"
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap">
<style>{CSS}</style></head><body><header><div><a class="brand" href="{root}{lang}/">EV Tracker</a>
<nav style="display:inline"><a href="{root}{lang}/">{t['home']}</a><a href="{root}{lang}/sources.html">{t['sources']}</a></nav></div>
<a href="{root}{other}/">{other.upper()}</a></header><main>{body}</main>
<footer>{t['note']}</footer></body></html>"""
def build():
    data = json.loads(pathlib.Path("data/data.json").read_text()) if pathlib.Path("data/data.json").exists() else {}
    out = pathlib.Path("docs"); shutil.rmtree(out, ignore_errors=True); out.mkdir()
    (out/"index.html").write_text('<meta http-equiv="refresh" content="0;url=it/">')
    for lang, ni in LANGS.items():
        t=T[lang]; rows=""
        for rk,(rit,ren) in REGIONS.items():
            cs=[c for c in COUNTRIES if c[2]==rk]
            if not cs: continue
            rows+=f'<tr><th colspan="3">{rit if lang=="it" else ren}</th></tr>'
            for c in sorted(cs,key=lambda c:c[ni]):
                hist=data.get(c[0],{}); mo=max((m for m in hist if pct(hist[m]) is not None),default=None)
                name=html.escape(c[ni])
                if mo:
                    p=pct(hist[mo]); y,m=mo.split("-")
                    cell=f'<div class="bar"><div class="track"><div class="fill" style="width:{min(p,100):.1f}%"></div></div><span class="pct">{fmt(p,lang)}</span></div>'
                    rows+=f'<tr><td><a href="countries/{c[1]}.html">{name}</a></td><td>{m}/{y}</td><td class="n">{cell}</td></tr>'
                else:
                    rows+=f'<tr><td>{name}</td><td class="none">–</td><td class="n none">{t["nodata"]}</td></tr>'
        body=f'<h1>{t["title"]}</h1><p class="sub">{t["sub"]}</p><div class="wrap"><table><thead><tr><th>{t["country"]}</th><th>{t["last"]}</th><th class="n">{t["share"]}</th></tr></thead><tbody>{rows}</tbody></table></div>'
        d=out/lang; (d/"countries").mkdir(parents=True)
        (d/"index.html").write_text(page(lang,t["title"],body,1))
        src="".join(f'<tr><td>{html.escape(c[ni])}</td><td><a href="{c[6]}">{html.escape(c[5])}</a></td></tr>' for c in COUNTRIES)
        (d/"sources.html").write_text(page(lang,t["sources"],f'<h1>{t["sources"]}</h1><div class="wrap"><table><thead><tr><th>{t["country"]}</th><th>{t["src"]}</th></tr></thead><tbody>{src}</tbody></table></div>',1))
        for c in COUNTRIES:
            hist=data.get(c[0],{}); r="".join(
              f'<tr><td>{m}</td><td class="n">{v["total"]:,}</td><td class="n">{v["bev"]:,}</td><td class="n">{fmt(pct(v),lang)}</td></tr>'
              for m,v in sorted(hist.items(),reverse=True) if pct(v) is not None)
            b=f'<p><a href="../">← {t["back"]}</a></p><h1>{html.escape(c[ni])}</h1><p class="sub">{t["src"]}: <a href="{c[6]}">{html.escape(c[5])}</a></p>'
            if r: b+=f'<div class="wrap"><table><thead><tr><th>{t["month"]}</th><th class="n">{t["total"]}</th><th class="n">{t["bev"]}</th><th class="n">{t["share"]}</th></tr></thead><tbody>{r}</tbody></table></div>'
            else: b+=f'<p class="none">{t["nodata"]}</p>'
            (d/"countries"/f"{c[1]}.html").write_text(page(lang,c[ni],b,2))
build()
