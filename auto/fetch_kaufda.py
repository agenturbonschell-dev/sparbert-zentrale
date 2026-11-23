#!/usr/bin/env python3
"""Holt strukturierte Angebote eines Händlers von kaufda.de (__NEXT_DATA__, type OFFER) mit Preis, Altpreis, Bedingungen (APP-PREIS …), Gültigkeit.
Nutzung: fetch_kaufda.py <slug> <ausgabe.json>   slug z. B. Edeka, REWE, Netto-Marken-Discount, Aldi-Nord, Aldi-Sued, Penny"""
import json,re,subprocess,sys
def page(slug):
    h=subprocess.run(['curl','-sS','-m','60','-L','-A','Mozilla/5.0',f'https://www.kaufda.de/Geschaefte/{slug}'],capture_output=True,text=True,check=True).stdout
    m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',h,re.S)
    if not m:raise SystemExit('keine Daten für '+slug)
    return json.loads(m.group(1))
def offers(d):
    out={}
    def w(o):
        if isinstance(o,dict):
            if o.get('type')=='OFFER' and o.get('prices'):out.setdefault(o['id'],o)
            for v in o.values():w(v)
        elif isinstance(o,list):
            for v in o:w(v)
    w(d);return list(out.values())
def norm(o,publisher=None):
    p=o['prices'];cond=' '.join(c.get('other','') for c in p.get('conditions',[]) if c.get('other')).strip()
    return dict(id=o['id'],publisher=o.get('publisherName'),title=(o.get('title') or '').strip(),brand=(o.get('brand') or '').strip(),desc=(o.get('description') or '').strip(),
        price=p.get('mainPrice'),old=p.get('secondaryPrice') or None,uvp=p.get('secondaryPriceIsUVP'),cond=cond,disc=p.get('description'),
        von=o.get('validFrom','')[:10],bis=o.get('validUntil','')[:10],image=(o.get('offerImages') or {}).get('url',{}).get('large'),cats=o.get('categories',[]))
if __name__=='__main__':
    slug,out=sys.argv[1:3];offs=[norm(o) for o in offers(page(slug))]
    json.dump(offs,open(out,'w'),ensure_ascii=False,indent=1);print(len(offs),'Angebote',slug)
