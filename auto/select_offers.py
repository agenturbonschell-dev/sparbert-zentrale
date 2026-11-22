#!/usr/bin/env python3
"""Wählt aus den Rohdaten die besten Angebote nach festen Regeln und prüft jede Zahl.
Nutzung: select_offers.py <raw.json> <products.json> <report.md>"""
import json,sys,re,datetime
TAGE=['Mo.','Di.','Mi.','Do.','Fr.','Sa.','So.']
def f(x):
    try:return float(str(x).replace('*','').replace('UVP','').strip())
    except:return None
def eur(x):return f'{x:.2f}'.replace('.',',')
def tag(iso):
    d=datetime.date.fromisoformat(iso);return f'{TAGE[d.weekday()]} {d.day}.'
def valid(von,bis,wochen_von):
    b=datetime.date.fromisoformat(bis);bt=f'{TAGE[b.weekday()]} {b.day}.{b.month}.'
    return f'gültig bis {bt}' if von<=wochen_von else f'{tag(von)} – {bt}'
FOOD={'Obst, Gemüse, Pflanzen','Fleisch, Geflügel, Wurst','Fisch','Molkereiprodukte, Fette','Tiefkühlkost','Feinkost, Konserven','Grundnahrungsmittel','Kaffee, Tee, Süßwaren, Knabberartikel','Getränke, Spirituosen','Drogerie, Tiernahrung'}
SEC={ # Reihenfolge im Video
 'TITELSEITE':{'Ab Mo.: Deutschlands beste Preise','Ab Do.: Deutschlands beste Preise','Ab Mo.: Unsere Knüller','Ab Do.: Unsere Knüller','Unsere Preisknüller zum Wochenende'},
 'FRISCH & ALLTAG':{'Obst, Gemüse, Pflanzen','Molkereiprodukte, Fette','Tiefkühlkost','Feinkost, Konserven','Grundnahrungsmittel','Fleisch, Geflügel, Wurst','Käse von mild bis herzhaft'},
 'GETRÄNKE':{'Getränke, Spirituosen'},
 'SÜSSES & SNACKS':{'Kaffee, Tee, Süßwaren, Knabberartikel','Süßes für alle','Am 6.12. ist Nikolaus'},
 'HAUSHALT & DROGERIE':{'Drogerie, Tiernahrung'},
}
QUOTA={'TITELSEITE':5,'FRISCH & ALLTAG':4,'GETRÄNKE':2,'SÜSSES & SNACKS':4,'HAUSHALT & DROGERIE':2}
BAD=re.compile(r'(?i)alkohol|wodka|whisk|rum\b|likör|bier|pils|hell\b|weißbier|radler|wein|sekt|gin\b|spirituos|tabak|waffe|feuerwerk|k-pop|kostüm|protein|ironmaxx')
def norm(o,wochen_von):
    p=f(o.get('formattedPrice'));old=f(o.get('formattedOldPrice'));card=f(o.get('loyaltyFormattedPrice'))
    t=(o.get('title') or '').strip();s=(o.get('subtitle') or '').strip()
    brand,name=(t,s) if s else ('',t)
    pf=re.search(r'\+\s*([\d.]+)\s*Pfand',o.get('detailDescription') or '')
    return dict(id=o['offerId'],cat=o['_cat'],brand=brand.upper(),name=name,unit=re.sub(r'^je\s*','je ',(o.get('unit') or '').replace(' - ','–').replace('Packg.','Packung').replace('-Fl.','-Flasche').replace(' x ',' × ').replace('Ka. ','Kasten ')),
      price=p,old=old,card=card,disc=o.get('discount') or 0,cdisc=o.get('loyaltyDiscount') or 0,von=o['salesFrom'],bis=o['salesTo'],
      pfand=f(pf.group(1)) if pf else None,image=o.get('listImage'),desc=o.get('detailDescription') or '',label=o.get('label'),
      valid=valid(o['salesFrom'],o['salesTo'],wochen_von))
def check(n):
    w=[]
    if not n['price']:w.append('kein Preis');return False,w
    if not n['old']:w.append('kein alter Preis');return False,w
    if n['price']>=n['old']:w.append('Preis nicht unter altem Preis');return False,w
    calc=round((1-n['price']/n['old'])*100)
    if abs(calc-n['disc'])>2:w.append(f'Rabatt {n["disc"]} % weicht von berechneten {calc} % ab')
    if n['card'] and n['card']>=n['price']:w.append('Card-Preis nicht unter Normalpreis');n['card']=None
    if not n['image']:w.append('kein Bild');return False,w
    return True,w
def main(raw,out,rep):
    d=json.load(open(raw));von=d['von'];seen={};warn=[]
    for o in d['offers']:
        n=norm(o,von);ok,w=check(n)
        if w:warn.append((n['brand'],n['name'],w))
        if not ok or n['cat'] not in FOOD|set().union(*SEC.values()):continue
        if BAD.search(f"{n['brand']} {n['name']} {n['desc']}"):continue
        key=(n['brand'],n['name']);
        if key not in seen or n['disc']>seen[key]['disc']:seen[key]=n
    pool=list(seen.values());picked=[];used=set()
    for sec,cats in SEC.items():
        c=[n for n in pool if n['cat'] in cats and n['id'] not in used and n['disc']>=25]
        c.sort(key=lambda n:(-(max(n['disc'],n['cdisc'] if n['card'] else 0)),n['price']))
        brands=set();k=0
        for n in c:
            if n['brand'] and n['brand'] in brands:continue   # eine Marke nur einmal je Block
            n['sec']=sec;picked.append(n);used.add(n['id']);brands.add(n['brand']);k+=1
            if k>=QUOTA[sec]:break
    prods=[]
    for n in picked:
        p=dict(sec=n['sec'],brand=n['brand'],name=n['name'],unit=n['unit'],price=eur(n['price']),old=eur(n['old']),save='-%d%%'%n['disc'],img=re.sub(r'\W','',n['id']),valid=n['valid'],image=n['image'])
        if n['card']:p['card']=eur(n['card']);p['save']='-%d%%'%(n['cdisc'] or round((1-n['card']/n['old'])*100))
        if n['pfand']:p['note']=f'zzgl. {eur(n["pfand"])} € Pfand'
        prods.append(p)
    json.dump({'von':von,'bis':d['bis'],'haendler':'kaufland','products':prods},open(out,'w'),ensure_ascii=False,indent=1)
    with open(rep,'w') as r:
        r.write(f'# Prüfbericht Kaufland {von} bis {d["bis"]}\n\n{len(prods)} Produkte gewählt aus {len(pool)} prüfbaren Angeboten.\n\n')
        for p in prods:r.write(f"- [{p['sec']}] {p['brand']} {p['name']} | {p.get('card') or p['price']} € (alt {p['old']} €) {p['save']} | {p['valid']}"+(f" | mit Card, ohne {p['price']} €" if p.get('card') else '')+(f" | {p['note']}" if p.get('note') else '')+'\n')
        r.write('\n## Auffälligkeiten (nicht verwendet oder zu prüfen)\n')
        for b,nm,w in warn[:40]:r.write(f'- {b} {nm}: {"; ".join(w)}\n')
    print(len(prods),'Produkte')
if __name__=='__main__':main(*sys.argv[1:4])
