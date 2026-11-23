#!/usr/bin/env python3
"""Gegenprüfung (zweiter Prüfweg): holt die Kaufland-Angebote LIVE neu und vergleicht jedes Produkt der products.json
(per offerId) mit Preis, Altpreis, Kartenpreis. Exit-Code 0 = alles stimmt, 1 = Abweichung (dann NICHT posten).
Nutzung: gegencheck.py kaufland <products.json> <kaufland_raw.json>
Lidl/andere: Prospektseiten werden von der Prüferin (zweite Person/Agent) visuell gegengeprüft, Ergebnis -> data/<KW>/pruefung_<haendler>.md"""
import json,sys,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import fetch_kaufland as fk
def f(x):
    try:return round(float(str(x).replace('*','').replace(',','.').strip()),2)
    except:return None
def eur(s):return f(str(s).replace(',','.')) if s not in (None,'') else None
def main(hid,pj,raw):
    if hid!='kaufland':print('nur kaufland automatisch; sonst Prüferin');return 2
    data=json.load(open(pj));live={}
    d=fk.extract(fk.fetch_html())
    def walk(o):
        if isinstance(o,dict):
            if 'offerId' in o:live[re.sub(r'\W','',o['offerId'])]=o
            for v in o.values():walk(v)
        elif isinstance(o,list):
            for v in o:walk(v)
    walk(d)
    bad=[];ok=0
    for p in data['products']:
        o=live.get(p['img'])
        if not o:bad.append((p['brand'],'Angebot live nicht mehr gefunden'));continue
        w=[]
        if eur(p['price'])!=f(o.get('formattedPrice')):w.append(f"Preis {p['price']} <> {o.get('formattedPrice')}")
        if p.get('old') and eur(p['old'])!=f(o.get('formattedOldPrice')):w.append(f"alt {p['old']} <> {o.get('formattedOldPrice')}")
        if p.get('card') and eur(p['card'])!=f(o.get('loyaltyFormattedPrice')):w.append(f"Karte {p['card']} <> {o.get('loyaltyFormattedPrice')}")
        if not p.get('card') and f(o.get('loyaltyFormattedPrice')):w.append('Kartenpreis live vorhanden, im Video nicht gezeigt')
        if w:bad.append((p['brand'],'; '.join(w)))
        else:ok+=1
    print(f'{ok} von {len(data["products"])} Produkten stimmen mit der Live-Quelle überein')
    for b,w in bad:print('ABWEICHUNG',b,w)
    return 1 if bad else 0
if __name__=='__main__':sys.exit(main(*sys.argv[1:4]))
