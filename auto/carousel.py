#!/usr/bin/env python3
"""Karussell-Generator (Instagram-Bildposts / TikTok-Foto-Karussells), 5 Kacheln 1080x1350 (4:5).

Aufruf:  python3 auto/carousel.py [KW48] [A B C ...]
Ausgabe: out/carousel/<name>/tile_1..5.jpg, caption.txt, sources.md

Alle Texte und Zahlen stammen aus data/<KW>/<haendler>_products.json (Felder
brand, name, unit, price, card, old, oldLabel, save, valid, note). Berechnet wird nur
der Grundpreis (EUR/kg) aus Preis und der Mengenangabe im Feld unit; nur bei eindeutiger
Menge ein Wert, bei Spannen (z. B. 250-300 g) eine Spanne und kein Rang.
Rendern: ein einziger Chromium-Prozess (Playwright aus tools/node_modules), mit nice.
"""
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RET = {r["id"]: r for r in json.load(open(ROOT / "auto/retailers.json"))["retailers"]}
IG_OWN = "@spar.bert"
HASHTAGS_MAX = 5

# ---------------------------------------------------------------- Daten helfer


def load(kw, hid):
    return json.load(open(ROOT / "data" / kw / f"{hid}_products.json"))


def find(data, brand, name_part=""):
    hits = [p for p in data["products"] if p["brand"] == brand and name_part in p["name"]]
    if len(hits) != 1:
        raise SystemExit(f"Produkt nicht eindeutig: {brand} / {name_part}: {len(hits)} Treffer")
    return hits[0]


def comma(d):
    return f"{Decimal(d).quantize(Decimal('0.01'), ROUND_HALF_UP):.2f}".replace(".", ",")


def num(s):
    return Decimal(s.replace(".", "").replace(",", "."))


def euro(s):
    return f"{s} €"


def logo_of(hid):
    l = RET[hid].get("logo")
    if l:
        return l
    p = f"assets/logos/{hid}.png"
    return p if (ROOT / p).exists() else None


def asset_for(hid, img):
    for d in (f"assets/{hid}", "assets/offers", "assets/lidl"):
        p = ROOT / d / f"{img}.png"
        if p.exists() and (d != "assets/lidl" or hid == "lidl"):
            return p
    raise SystemExit(f"Freisteller fehlt: {hid}/{img}")


def grams(unit):
    """(min_g, max_g) aus dem Mengenfeld; None wenn nicht eindeutig lesbar."""
    u = unit.split("·")[0].replace(".", "")
    m = re.search(r"(\d+)\s*[–-]\s*(\d+)[\s-]*g\b", u)
    if m:
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"(\d+)[\s-]*g\b", u)
    if m and "×" not in u and "x" not in u.lower().replace("xxl", ""):
        return int(m.group(1)), int(m.group(1))
    return None


def per_kg(price, g):
    return (num(price) / Decimal(g) * 1000).quantize(Decimal("0.01"), ROUND_HALF_UP)


def weekday_range(d):
    wd = ["Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So."]
    v, b = date.fromisoformat(d["von"]), date.fromisoformat(d["bis"])
    return f"{wd[v.weekday()]} {v.day}. – {wd[b.weekday()]} {b.day}.{b.month}."


def de_date(iso):
    d = date.fromisoformat(iso)
    return f"{d.day}.{d.month}."


def valid_range(d):
    v, b = date.fromisoformat(d["von"]), date.fromisoformat(d["bis"])
    return f"{v.day}.–{b.day}.{b.month}.{b.year}"


def cond(hid, d, p):
    parts = []
    if p.get("card"):
        parts.append("mit " + RET[hid]["card"])
    v = p["valid"]
    if not v.startswith("gültig") and v != weekday_range(d):
        parts.append("nur " + v)
    return " · ".join(parts)


def tile_from(hid, data, p, rank=None, grund=None):
    """Produkt -> Kachel-Dict. Alles aus den Feldern, Kartenname aus retailers.json."""
    r = RET[hid]
    card_name = r.get("card")
    t = dict(kind="product", retailer=r["name"], logo=logo_of(hid), brand=p["brand"], name=p["name"],
             img=str(asset_for(hid, p["img"])), rank=rank, grund=grund, save=p.get("save") or "")
    unit_parts = [x.strip() for x in p["unit"].split("·")]
    t["unit"] = unit_parts[0]
    chips = []
    if p.get("card"):
        t["main"], t["main_label"] = p["card"], f"MIT {card_name.upper()}"
        alts = []
        if p.get("price"):
            alts.append(("ohne " + card_name, p["price"], False))
        if p.get("old"):
            alts.append(((p.get("oldLabel") or "statt"), p["old"], True))
        elif not p.get("price"):
            pass
        if not p.get("price") and p.get("old"):
            # Nutella-Fall: kein Preis ohne Karte, nur Normalpreis in old
            alts = [((p.get("oldLabel") or "statt"), p["old"], False)]
        t["alts"] = alts
    else:
        t["main"], t["main_label"] = p["price"], ""
        t["alts"] = [((p.get("oldLabel") or "statt"), p["old"], True)] if p.get("old") else []
    full = weekday_range(data)
    v = p["valid"]
    if v.startswith("gültig"):
        chips.append(("ok", v[0].upper() + v[1:]))
    elif v == full:
        chips.append(("ok", "Gültig " + v))
    else:
        chips.append(("warn", "Nur " + v))
    for x in unit_parts[1:]:
        chips.append(("warn" if re.search(r"max\.|pro Kunde", x) else "info", x))
    if p.get("note"):
        chips.append(("warn" if "Pfand" in p["note"] else "info", p["note"]))
    t["chips"] = chips
    return t


# ---------------------------------------------------------------- HTML

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px;overflow:hidden}
body{font-family:"Arial Black","DejaVu Sans",Arial,sans-serif;font-weight:900;color:#14171f;position:relative}
.cream{background:radial-gradient(ellipse at 50% 38%,#fffaf0 0%,#fdebc8 62%,#f7d79a 100%)}
.cream:before{content:"";position:absolute;inset:0;background:repeating-conic-gradient(from 0deg at 50% 38%,rgba(255,255,255,.35) 0 6deg,rgba(255,255,255,0) 6deg 12deg)}
.bgimg{background:url(BGURL) center/cover}
.topband{position:absolute;left:0;right:0;top:0;height:18px;background:#e8201a}
.fit{display:block;overflow:hidden;white-space:nowrap}
.wrap{white-space:normal;line-height:1.05}
.ink{color:#14171f}.red{color:#e8201a}
.foot{position:absolute;left:60px;right:60px;bottom:30px;display:flex;justify-content:space-between;font-size:26px;font-weight:700;color:#6a3d22;font-family:Arial,"DejaVu Sans",sans-serif}
/* Produktkachel */
.col{position:absolute;left:60px;right:60px;top:42px;bottom:80px;display:flex;flex-direction:column;gap:14px}
.head{height:96px;display:flex;align-items:center;justify-content:space-between;flex:none}
.logo{height:96px;background:#fff;border:5px solid #14171f;border-radius:18px;display:flex;align-items:center;justify-content:center;padding:6px 16px}
.logo img{height:72px;max-width:260px;object-fit:contain}
.rank{background:#e8201a;color:#fff;border:5px solid #14171f;border-radius:18px;font-size:44px;padding:14px 26px;transform:rotate(3deg)}
.rank.g{background:#1f9a2a}
.rname{font-size:40px;padding:0 10px}
.imgcard{flex:1;min-height:250px;background:#fff;border:6px solid #14171f;border-radius:30px;box-shadow:0 10px 0 rgba(20,23,31,.18);display:flex;align-items:center;justify-content:center;padding:18px;position:relative;overflow:hidden}
.imgcard img{max-width:100%;max-height:100%;object-fit:contain}
.badge{position:absolute;right:16px;top:14px;background:#ffd23f;color:#e8201a;border:5px solid #14171f;border-radius:50%;width:150px;height:150px;display:flex;align-items:center;justify-content:center;font-size:44px;transform:rotate(8deg)}
.brand{font-size:32px;color:#e8201a;letter-spacing:1px;height:38px;flex:none}
.pname{font-size:62px;flex:none;display:flex;align-items:flex-start}
.pname span{display:block;width:100%;max-height:128px;overflow:hidden;line-height:1.04}
.unit{font-size:34px;font-weight:700;font-family:Arial,"DejaVu Sans",sans-serif;color:#3b3f4a;height:42px;flex:none}
.pricebox{display:flex;flex:none;height:250px;gap:18px;align-items:stretch}
.pl{flex:1;min-width:0;background:linear-gradient(#ff7a1a,#e8201a);border:6px solid #14171f;border-radius:30px;padding:12px 26px;color:#fff;display:flex;flex-direction:column;justify-content:center;position:relative}
.pl .lab{font-size:30px;color:#ffe9a8;height:36px}
.pl .big{font-size:170px;line-height:1;height:180px;text-shadow:5px 5px 0 rgba(20,23,31,.55)}
.pr{width:330px;flex:none;display:flex;flex-direction:column;justify-content:center;gap:10px}
.alt{background:#fff;overflow:hidden;border:5px solid #14171f;border-radius:20px;padding:10px 16px;font-family:Arial,"DejaVu Sans",sans-serif;font-weight:700;font-size:26px;color:#3b3f4a;line-height:1.15}
.alt b{display:inline-block;font-family:"Arial Black","DejaVu Sans",Arial,sans-serif;font-size:40px;color:#14171f}
.alt b.cross{text-decoration:line-through;text-decoration-thickness:5px;text-decoration-color:#e8201a;color:#6b6f7a}
.grund{flex:none;background:#14171f;color:#fff;border-radius:20px;padding:10px 24px;font-size:36px;height:62px;display:flex;align-items:center}
.grund small{font-family:Arial,"DejaVu Sans",sans-serif;font-weight:700;font-size:24px;color:#ffe9a8;margin-left:auto;padding-left:16px;white-space:nowrap}
.chips{display:flex;flex-wrap:wrap;gap:10px;flex:none;min-height:56px}
.chip{font-family:Arial,"DejaVu Sans",sans-serif;font-weight:800;font-size:28px;border:4px solid #14171f;border-radius:14px;padding:6px 16px;background:#fff}
.chip.warn{background:#e8201a;color:#fff}.chip.ok{background:#d9f2d0}.chip.info{background:#fff1c9}
/* Titel / Abschluss */
.kenn{position:absolute;left:50px;right:50px;top:36px;font-family:Arial,"DejaVu Sans",sans-serif;font-weight:700;font-size:25px;line-height:1.25;color:#14171f;background:rgba(255,255,255,.88);border-radius:14px;padding:8px 16px;text-align:center}
.card{position:absolute;left:70px;right:70px;background:rgba(255,255,255,.93);border:6px solid #14171f;border-radius:34px;padding:30px 34px;box-shadow:0 10px 0 rgba(20,23,31,.2)}
.t1{font-size:46px;color:#e8201a;height:56px}
.t2{font-size:104px;line-height:1;height:120px;margin-top:6px}
.t3{font-family:Arial,"DejaVu Sans",sans-serif;font-weight:700;font-size:34px;color:#3b3f4a;margin-top:10px;line-height:1.2}
.valid{display:inline-block;margin-top:14px;background:#14171f;color:#fff;border-radius:14px;padding:8px 20px;font-size:32px}
.logos{display:flex;gap:14px;margin-top:16px}
.logos .logo{height:110px}.logos .logo img{height:84px;max-width:240px}
.duck{position:absolute;filter:drop-shadow(0 8px 0 rgba(20,23,31,.18))}
.cta{background:#e8201a;color:#fff;border:6px solid #14171f;border-radius:26px;padding:18px 24px;text-align:center;font-size:54px;margin-top:14px}
.cta2{background:#ffd23f;color:#14171f;border:6px solid #14171f;border-radius:26px;padding:16px 24px;text-align:center;font-size:44px;margin-top:14px}
.sumrow{display:flex;align-items:center;gap:14px;border-bottom:3px solid rgba(20,23,31,.18);padding:10px 0;font-family:Arial,"DejaVu Sans",sans-serif;font-weight:700;font-size:28px}
.sumrow:last-child{border-bottom:0}
.sumrow .sr{font-family:"Arial Black","DejaVu Sans",Arial,sans-serif;width:200px;flex:none;font-size:30px}
.stack{position:absolute;left:70px;right:70px;top:40px;display:flex;flex-direction:column;gap:22px}
.stack .card{position:static}
.sumrow .sp{white-space:pre-line;flex:1;min-width:0;line-height:1.15}
.sumrow .sv{font-family:"Arial Black","DejaVu Sans",Arial,sans-serif;font-size:36px;color:#e8201a;white-space:nowrap;text-align:right}
.small{font-family:Arial,"DejaVu Sans",sans-serif;font-weight:700;font-size:26px;color:#3b3f4a;text-align:center;margin-top:12px}
.handle{font-size:60px;color:#e8201a;text-align:center;margin-top:10px}
"""

FIT_JS = """
document.querySelectorAll('.fit').forEach(e=>{let s=parseFloat(getComputedStyle(e).fontSize);
 while((e.scrollWidth>e.clientWidth+1)&&s>14){s-=2;e.style.fontSize=s+'px'}});
document.querySelectorAll('.pname span').forEach(e=>{let s=parseFloat(getComputedStyle(e).fontSize);
 while((e.scrollHeight>e.clientHeight+1)&&s>20){s-=2;e.style.fontSize=s+'px'}});
document.querySelectorAll('.alt b').forEach(e=>{let s=parseFloat(getComputedStyle(e).fontSize);e.style.whiteSpace='nowrap';e.style.display='inline-block';
 while((e.scrollWidth>e.parentElement.clientWidth-34)&&s>16){s-=2;e.style.fontSize=s+'px'}});
window.__ok=true;
"""


def E(s):
    return html.escape(str(s))


def uri(p):
    return Path(p).resolve().as_uri()


def page(body, bg="cream", n=1, total=5, foot=True):
    bgurl = uri(ROOT / "assets/off/bg7.jpg")
    css = CSS.replace("BGURL", bgurl)
    f = (f'<div class="foot"><span>Preise können je Markt abweichen</span><span>{n}/{total}</span></div>'
         if foot else "")
    top = '<div class="topband"></div>' if bg == "cream" else ""
    return (f'<!doctype html><meta charset="utf-8"><style>{css}</style>'
            f'<body class="{bg}">{top}{body}{f}<script>{FIT_JS}</script></body>')


def product_html(t, n, total=5):
    head_logo = (f'<div class="logo"><img src="{uri(ROOT / t["logo"])}"></div>' if t.get("logo")
                 else f'<div class="logo"><span class="fit" style="font-size:44px;max-width:300px">{E(t["retailer"])}</span></div>')
    rank = ""
    if t.get("rank"):
        rank = f'<div class="rank {"g" if t["rank"].startswith("PLATZ 1") else ""}">{E(t["rank"])}</div>'
    badge = f'<div class="badge">{E(t["save"])}</div>' if t["save"] else ""
    lab = f'<div class="lab fit">{E(t["main_label"])}</div>' if t["main_label"] else '<div class="lab">&nbsp;</div>'
    alts = ""
    for label, val, cross in t["alts"]:
        alts += (f'<div class="alt"><div>{E(label)}</div><b class="{"cross" if cross else ""}">{E(euro(val))}</b></div>')
    grund = ""
    if t.get("grund"):
        g = t["grund"]
        grund = (f'<div class="grund"><span class="fit" style="flex:1">{E(g["main"])}</span>'
                 f'<small>{E(g.get("side", ""))}</small></div>')
    chips = "".join(f'<span class="chip {c}">{E(x)}</span>' for c, x in t["chips"])
    body = f"""
<div class="col">
 <div class="head">{head_logo}{rank}</div>
 <div class="imgcard"><img src="{uri(t["img"])}">{badge}</div>
 <div class="brand fit">{E(t["brand"])}</div>
 <div class="pname"><span>{E(t["name"])}</span></div>
 <div class="unit fit">{E(t["unit"])}</div>
 <div class="pricebox"><div class="pl">{lab}<div class="big fit">{E(euro(t["main"]))}</div></div>
  <div class="pr">{alts}</div></div>
 {grund}
 <div class="chips">{chips}</div>
</div>"""
    return page(body, "cream", n, total)


def title_html(c):
    duck = uri(ROOT / "assets/off/hq6/p1.png")
    logos = "".join(f'<div class="logo"><img src="{uri(ROOT / l)}"></div>' for l in c["logos"])
    body = f"""
<div class="kenn">{E(c["kenn"])}</div>
<div class="card" style="top:150px">
 <div class="t1 fit">{E(c["t1"])}</div>
 <div class="t2 fit red">{E(c["t2"])}</div>
 <div class="t3">{E(c["t3"])}</div>
 <div class="valid">{E(c["valid"])}</div>
 <div class="logos">{logos}</div>
</div>
<img class="duck" src="{duck}" style="right:20px;bottom:50px;height:590px">"""
    return page(body, "bgimg", 1, 5)


def final_html(c):
    duck = uri(ROOT / "assets/off/hq6/p6.png")
    rows = ""
    for r in c["summary"]:
        rows += (f'<div class="sumrow"><span class="sr fit">{E(r["who"])}</span>'
                 f'<span class="sp">{E(r["what"])}</span><span class="sv">{E(r["val"])}</span></div>')
    body = f"""
<div class="stack">
 <div class="card">
  <div class="t1 fit" style="font-size:40px;height:48px;margin-bottom:6px">{E(c["sum_title"])}</div>
  {rows}
 </div>
 <div class="card" style="padding:20px 30px">
  <div class="cta fit" style="margin-top:0">Speichern fürs Einkaufen</div>
  <div class="cta2 fit">Folgen für mehr Spar-Checks</div>
  <div class="small">Preise können je Markt abweichen</div>
  <div class="handle fit">{IG_OWN}</div>
 </div>
</div>
<img class="duck" src="{duck}" style="left:50%;margin-left:-215px;bottom:14px;height:420px">"""
    return page(body, "bgimg", 5, 5, foot=False)


# ---------------------------------------------------------------- Rendern

NODE = r"""
const {chromium}=require('playwright');
const jobs=JSON.parse(process.argv[2]);
(async()=>{
 const b=await chromium.launch({args:['--disable-gpu','--renderer-process-limit=1']});
 const ctx=await b.newContext({viewport:{width:1080,height:1350},deviceScaleFactor:1});
 const p=await ctx.newPage();
 for(const j of jobs){
  await p.goto('file://'+j.html);
  await p.waitForFunction('window.__ok===true',null,{timeout:30000});
  await p.evaluate(()=>Promise.all([...document.images].map(i=>i.decode().catch(()=>0))));
  await p.screenshot({path:j.png,type:'png'});
 }
 await b.close();
})();
"""


def render(jobs):
    tools = ROOT / "tools"
    env = dict(os.environ, NODE_PATH=os.pathsep.join([str(tools / "node_modules"), "/opt/node-tools/node_modules"]))
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False) as f:
        f.write(NODE)
    try:
        subprocess.run(["nice", "-n", "19", "node", f.name, json.dumps(jobs)], check=True, env=env, cwd=tools)
    finally:
        os.unlink(f.name)


def build(c, out_root):
    from PIL import Image
    out = out_root / c["name"]
    out.mkdir(parents=True, exist_ok=True)
    pages = [title_html(c)] + [product_html(t, i + 2) for i, t in enumerate(c["tiles"])] + [final_html(c)]
    assert len(pages) == 5
    with tempfile.TemporaryDirectory() as td:
        jobs = []
        for i, h in enumerate(pages, 1):
            hp, pp = Path(td) / f"t{i}.html", Path(td) / f"t{i}.png"
            hp.write_text(h, encoding="utf-8")
            jobs.append(dict(html=str(hp), png=str(pp)))
        render(jobs)
        for i, j in enumerate(jobs, 1):
            im = Image.open(j["png"]).convert("RGB")
            assert im.size == (1080, 1350), im.size
            dest = out / f"tile_{i}.jpg"
            q = 95
            im.save(dest, "JPEG", quality=q, subsampling=0, optimize=True)
            assert dest.stat().st_size <= 8 * 1024 * 1024
    (out / "caption.txt").write_text(c["caption"], encoding="utf-8")
    (out / "sources.md").write_text(c["sources"], encoding="utf-8")
    print("fertig:", out)


# ---------------------------------------------------------------- Karussells


def handle(hid):
    h = RET[hid].get("handle_ig")
    return "@" + h if h else RET[hid]["name"]


def kennzeichnung(hids):
    return "Unbezahlte Werbung / Kostenlose Werbung für " + ", ".join(handle(h) for h in hids)


def caption(intro, hids, valid_line, extra, tags):
    assert len(tags) <= HASHTAGS_MAX
    return (f"{intro}\n\n{kennzeichnung(hids)}\n{valid_line}\n{extra}\n"
            "Preise können je Markt abweichen. Angebote teils nur mit App/Karte oder an bestimmten Tagen.\n\n"
            "Speichern fürs Einkaufen, folgen für mehr Spar-Checks: @spar.bert\n\n" + " ".join(tags) + "\n")


def carousel_A(kw):
    d = load(kw, "lidl")
    ps = [find(d, "NUTELLA"), find(d, "MÖVENPICK", "Eiscreme"), find(d, "LANDLIEBE")]
    tiles = [tile_from("lidl", d, p) for p in ps]
    summary = []
    for p in ps:
        main = p.get("card") or p["price"]
        who = "Lidl Plus" if p.get("card") else "Lidl"
        summary.append(dict(who=who, what=f'{p["brand"].title()} {p["name"]}\n{p["valid"]}', val=euro(main)))
    pct = ", ".join(f'{p["brand"].title()} {p["save"]}' for p in ps)
    nut = ps[0]
    src = f"""# Quellen: Lidl Top 3 der Woche

Datei: `data/{kw}/lidl_products.json` (von {d["von"]}, bis {d["bis"]}; Prüfung: `data/{kw}/pruefung_lidl.md`).

Auswahl: drei Produkte mit hohem Rabatt (Feld `save`): {pct}. Nutella ist wegen der Bedingungen
(Lidl Plus, nur bis Mi., Limit) gesetzt. Butter (-60 %) und Müller Milchreis (-52 %, ohne `old`) sind nicht
gewählt, Butter läuft im Karussell "Butter".

Felder je Kachel: `brand`, `name`, `unit` (Menge, Limit), `price`, `card` (Hauptpreis, wenn vorhanden), `old` mit `oldLabel`,
`save` (Rabatt-Stempel), `valid` (Tage), `note` (Pfand usw.).

Nutella: `card` 1,99 € ist Hauptpreis mit Lidl Plus; `price` ist leer (kein Preis ohne Karte im Datensatz), `old` 3,99 € ({nut["oldLabel"]}) steht als Vergleich.
`unit` "{nut["unit"]}" liefert das Limit; `valid` "{nut["valid"]}" ("Nur ..."-Hinweis).

Keine Berechnungen. Lidl-Handle `@lidlde` aus `auto/retailers.json`. Logo `assets/logos/lidl.png`, Freisteller `assets/lidl/`.
"""
    cap = caption(
        "Lidl Top 3 der Woche: drei starke Rabatte aus dem Prospekt.\n"
        f"Nutella nur mit Lidl Plus und nur bis Mi. 25.11., max. 3 pro Kunde.",
        ["lidl"],
        f"Gültig {valid_range(d)} (je Angebot teils kürzer, siehe Bilder)", "",
        ["#lidl", "#angebote", "#angebotederwoche", "#sparen", "#lidlplus"])
    return dict(name="A_lidl_top3", kenn=kennzeichnung(["lidl"]), t1="Lidl Top 3", t2="DER WOCHE",
                t3="3 starke Rabatte aus dem Lidl-Prospekt. Bedingungen stehen bei jedem Preis.",
                valid=f"Gültig {valid_range(d)} · Tage je Angebot", logos=[logo_of("lidl")],
                tiles=tiles, sum_title="Die 3 Angebote im Überblick", summary=summary,
                caption=cap, sources=src)


def butter_candidates(kw):
    items = []
    for hid, brand, part in [("lidl", "BAYERNKRONE", "Butter"), ("kaufland", "WEIHENSTEPHAN", "Butter"),
                             ("netto", "FRAU ANTJE", "Butter"), ("rewe", "KERRYGOLD", "Butter")]:
        d = load(kw, hid)
        items.append((hid, d, find(d, brand, part)))
    return items


def carousel_B(kw):
    cand = butter_candidates(kw)
    rows = []
    for hid, d, p in cand:
        g = grams(p["unit"])
        assert g and g[0] == g[1], p
        eff = p.get("card") or p["price"]
        rows.append(dict(hid=hid, d=d, p=p, g=g[0], eff=eff, kg=per_kg(eff, g[0]),
                         kg_alt=per_kg(p["price"], g[0]) if p.get("card") else None))
    rows.sort(key=lambda r: r["kg"])
    top = rows[:3]
    rank = {}
    for r in rows:
        rank[r["hid"]] = 1 + sum(1 for x in rows if x["kg"] < r["kg"])
    tiles = []
    for r in top:
        side = f'ohne {RET[r["hid"]]["card"]}: {comma(r["kg_alt"])} €/kg' if r["kg_alt"] else ""
        t = tile_from(r["hid"], r["d"], r["p"], rank=f"PLATZ {rank[r['hid']]}",
                      grund=dict(main=f'= {comma(r["kg"])} € pro kg', side=side))
        tiles.append(t)
    hids = [r["hid"] for r in top]
    summary = [dict(who=f"{rank[r['hid']]}. " + RET[r["hid"]]["name"],
                    what=f'{r["p"]["brand"].title()} {r["p"]["name"]}, {r["p"]["unit"].split("·")[0].strip()}'
                    + ("\n" + cond(r["hid"], r["d"], r["p"]) if cond(r["hid"], r["d"], r["p"]) else ""),
                    val=f'{comma(r["kg"])} €/kg') for r in top]
    tie = any(sum(1 for x in rows if x["kg"] == r["kg"]) > 1 for r in rows)
    lines = "\n".join(
        f'- {RET[r["hid"]]["name"]}: {r["p"]["brand"]} {r["p"]["name"]}, unit "{r["p"]["unit"]}" -> {r["g"]} g; '
        f'Preis {r["eff"]} € ({"card" if r["p"].get("card") else "price"}) / {r["g"]} g x 1000 = {comma(r["kg"])} €/kg'
        + (f' (ohne Karte: price {r["p"]["price"]} € = {comma(r["kg_alt"])} €/kg)' if r["kg_alt"] else "")
        + f'; valid "{r["p"]["valid"]}"; Rang {rank[r["hid"]]}' for r in rows)
    src = f"""# Quellen: Bestes Angebot der Woche, Butter (Preis-Check)

Dateien: `data/{kw}/lidl_products.json`, `kaufland_products.json`, `netto_products.json`, `rewe_products.json`
(alle geprüft, siehe `pruefung_*.md`). Händler ohne Butterangebot in den Daten (Penny, Edeka, Aldi Nord, Aldi Süd; bei Aldi Süd
nur Margarine) sind weggelassen (Regel 3: nichts gefunden, nicht "kein Angebot").

Alle vier Treffer haben eindeutig 250 g im Feld `unit`. Grundpreis = Preis / 250 g x 1000 (kaufmännisch auf 2 Stellen gerundet).
Es zählt der günstigste für jeden zugängliche Preis mit Karte/App-Bedingung als Hauptpreis (Kaufland: `card`).

{lines}

Rang: nach €/kg aufsteigend, gleiche Werte teilen den Platz. {"Lidl und Netto haben denselben Grundpreis (beide 0,99 € / 250 g) und teilen Platz 1." if tie else ""}
Gezeigt werden die 3 günstigsten; REWE (Kerrygold, 1,59 €, 6,36 €/kg) liegt dahinter und wird nicht gezeigt.

Bedingungen auf den Kacheln: Kaufland `card` = Kaufland Card (Hauptpreis), `price` = Preis ohne Karte; Netto-Butter nur Do. 26. – Sa. 28.11. (`valid`);
Lidl Mo. 23. – Sa. 28.11.

Hinweise/Schwächen: Kaufland-Feld `name` lautet "Butter oder Die Streichzarte" (ein Preis für beide, Mengen gleich 250 g);
ob der Preis für die reine Butter gilt, steht nicht getrennt in den Daten. Händler mit `unit`-Spanne oder ohne Menge werden nicht gerankt.
Logos `assets/logos/`, Freisteller: `assets/lidl/butter.png`, `assets/netto/butter.png`, `assets/offers/ART63261_KAV3769402.png`.
"""
    cap = caption(
        "Bestes Angebot der Woche: Butter. Preis-Check nach Grundpreis pro kg (je 250 g).\n"
        "Lidl und Netto gleichauf. Netto nur Do. 26. – Sa. 28.11., Kaufland nur mit Kaufland Card.",
        hids, f"Gültig {valid_range(cand[0][1])} (Netto: Do. 26. – Sa. 28.11.)", "",
        ["#butter", "#angebote", "#angebotederwoche", "#sparen", "#preischeck"])
    names = ", ".join(RET[h]["name"] for h in hids)
    return dict(name="B_butter_preischeck", kenn=kennzeichnung(hids), t1="Bestes Angebot der Woche", t2="BUTTER",
                t3="Preis-Check: je 250 g, Rang nach Grundpreis pro kg. Bedingungen je Händler.",
                valid=f"Gültig {valid_range(cand[0][1])} · Tage je Händler", logos=[logo_of(h) for h in hids],
                tiles=tiles, sum_title="Butter: Grundpreis pro kg", summary=summary, caption=cap, sources=src)


def carousel_C(kw):
    """Schokolade: nur Händler mit Tafelschokolade und nachvollziehbarer Menge; Mengenspannen -> Spanne, kein Rang."""
    spec = [("kaufland", "MILKA", "Schokolade"), ("netto", "MILKA", "Schokolade"), ("penny", "RITTER SPORT", "Bunte")]
    rows = []
    for hid, brand, part in spec:
        d = load(kw, hid)
        p = find(d, brand, part)
        g = grams(p["unit"])
        assert g, p
        eff = p.get("card") or p["price"]
        lo, hi = per_kg(eff, g[1]), per_kg(eff, g[0])
        rows.append(dict(hid=hid, d=d, p=p, g=g, eff=eff, lo=lo, hi=hi,
                         alt=(per_kg(p["price"], g[0]) if p.get("card") else None)))
    tiles = []
    for r in rows:
        txt = comma(r["lo"]) if r["lo"] == r["hi"] else f'{comma(r["lo"])}–{comma(r["hi"])}'
        side = ""
        if r["alt"] is not None:
            side = f'ohne {RET[r["hid"]]["card"]}: {comma(r["alt"])} €/kg'
        elif r["lo"] != r["hi"]:
            side = "Mengenspanne"
        tiles.append(tile_from(r["hid"], r["d"], r["p"], grund=dict(main=f"= {txt} € pro kg", side=side)))
    summary = []
    for r in rows:
        txt = comma(r["lo"]) if r["lo"] == r["hi"] else f'{comma(r["lo"])}–{comma(r["hi"])}'
        summary.append(dict(who=RET[r["hid"]]["name"], what=f'{r["p"]["brand"].title()} {r["p"]["name"]}, {r["p"]["unit"].split("·")[0].strip()}'
                            + ("\n" + cond(r["hid"], r["d"], r["p"]) if cond(r["hid"], r["d"], r["p"]) else ""),
                            val=f"{txt} €/kg"))
    hids = [r["hid"] for r in rows]
    lines = "\n".join(
        f'- {RET[r["hid"]]["name"]}: {r["p"]["brand"]} {r["p"]["name"]}, unit "{r["p"]["unit"]}" -> {r["g"][0]}–{r["g"][1]} g; '
        f'Preis {r["eff"]} € ({"card" if r["p"].get("card") else "price"}); {r["eff"]} / {r["g"][1]} g x 1000 = {comma(r["lo"])} €/kg, '
        f'{r["eff"]} / {r["g"][0]} g x 1000 = {comma(r["hi"])} €/kg'
        + (f'; ohne Karte price {r["p"]["price"]} € = {comma(r["alt"])} €/kg' if r["alt"] else "")
        + f'; valid "{r["p"]["valid"]}"' for r in rows)
    src = f"""# Quellen: Bestes Angebot der Woche, Schokolade (Preis-Check)

Dateien: `data/{kw}/kaufland_products.json`, `netto_products.json`, `penny_products.json` (geprüft, siehe `pruefung_*.md`).

Berücksichtigt: Tafelschokolade (Milka, Ritter Sport). Ausgeschlossen wie angewiesen: Haribo (Fruchtgummi).
Weitere Schokoladen-Treffer in den Daten sind teurer pro kg oder keine Tafeln und werden nicht gezeigt:
Lidl Ritter Sport Knusperstück 200 g, 2,99 € = 14,95 €/kg; REWE Lindt Lindor 200 g, 4,99 € = 24,95 €/kg;
REWE Milka Weihnachtsmann 45 g, 0,99 € = 22,00 €/kg. Kinder Riegel (Netto, 327–420 g) und Kinder Country (Aldi Süd, Rewe) sind
Riegel/Snacks, keine Tafeln, und nicht gerechnet. Gezeigt werden die 3 Händler mit dem niedrigsten möglichen Grundpreis.

Grundpreis = Preis / Menge x 1000. Wo `unit` eine Spanne nennt (Kaufland 250–300 g, Netto 85–110 g), steht die Spanne
(kleinste Menge = höchster €/kg, größte Menge = niedrigster €/kg). Weil sich die Spannen überlappen, gibt es KEINEN Rang
und keine "Platz"-Angabe; die Reihenfolge der Kacheln ist nach dem niedrigsten möglichen Grundpreis.

{lines}

Bedingungen: Penny `card` = Penny-App (Hauptpreis 0,99 €), `price` 1,11 € ohne App; Kaufland und Netto ohne Karte/App-Preis in den Daten, alle Mo. 23. – Sa. 28.11. (Kaufland "gültig bis Sa. 28.11.").
Weggelassen (Regel 3, nichts gefunden): Edeka (nur Smarties-Dragees), Aldi Nord, Aldi Süd (keine Tafelschokolade in den Daten). Übrige Händler: siehe oben.

Schwächen: Mengenspannen, "versch. Sorten" (Penny), die Packungen sind nicht identisch (Milka vs. Ritter Sport); Netto-Milka
ist mit 85–110 g eine kleinere Tafel. Die Aussage "bestes Angebot" bezieht sich nur auf den Grundpreis dieser Händler in den Daten.
Freisteller: `assets/offers/ART755152_KAV3769402.png` (Kaufland), `assets/netto/milka.png`, `assets/penny/ritter.png`.
"""
    cap = caption(
        "Bestes Angebot der Woche: Schokolade. Grundpreis pro kg im Vergleich (Tafeln).\n"
        "Packungsgrößen bei Kaufland und Netto sind Spannen, daher ohne Rangfolge. Penny: günstigster Preis nur mit Penny-App.",
        hids, f"Gültig {valid_range(rows[0]['d'])}", "",
        ["#schokolade", "#angebote", "#angebotederwoche", "#sparen", "#preischeck"])
    return dict(name="C_schokolade_preischeck", kenn=kennzeichnung(hids), t1="Bestes Angebot der Woche", t2="SCHOKOLADE",
                t3="Grundpreis pro kg im Vergleich. Mengenspannen, daher ohne Rangfolge.",
                valid=f"Gültig {valid_range(rows[0]['d'])}", logos=[logo_of(h) for h in hids],
                tiles=tiles, sum_title="Schokolade: Grundpreis pro kg", summary=summary, caption=cap, sources=src)


BUILDERS = {"A": carousel_A, "B": carousel_B, "C": carousel_C}

if __name__ == "__main__":
    args = sys.argv[1:]
    kw = next((a for a in args if a.startswith("KW")), "KW48")
    which = [a for a in args if a in BUILDERS] or list(BUILDERS)
    out_root = ROOT / "out/carousel"
    for k in which:
        build(BUILDERS[k](kw), out_root)
