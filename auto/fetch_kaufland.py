#!/usr/bin/env python3
"""Holt die aktuellen Kaufland-Angebote (offizielle Seite) und schreibt data/<KW>/kaufland_raw.json.
Nutzung: fetch_kaufland.py <von-ISO z. B. 2026-11-23> <ausgabe.json>"""
import json,sys,subprocess
URL='https://filiale.kaufland.de/angebote/uebersicht.html'
def fetch_html():
    return subprocess.run(['curl','-sS','-m','60','-L','-A','Mozilla/5.0',URL],capture_output=True,text=True,check=True).stdout
def extract(h):
    j=h.find('"component":"OfferTemplate"');k=h.rfind('=',0,j);start=h.find('{',k)
    depth=0;inS=False;esc=False
    for p in range(start,len(h)):
        ch=h[p]
        if inS:
            if esc:esc=False
            elif ch=='\\':esc=True
            elif ch=='"':inS=False
        else:
            if ch=='"':inS=True
            elif ch=='{':depth+=1
            elif ch=='}':
                depth-=1
                if depth==0:return json.loads(h[start:p+1])
    raise RuntimeError('Angebotsdaten nicht gefunden')
if __name__=='__main__':
    von=sys.argv[1];d=extract(fetch_html())
    # Woche = alle Kategorien, deren Verkaufszeitraum in der Woche ab <von> liegt (Mo–Sa)
    import datetime
    v=datetime.date.fromisoformat(von);bis=(v+datetime.timedelta(days=5)).isoformat()
    sel=[]
    for cy in d['props']['offerData']['cycles']:
        for cat in cy['categories']:
            if von<=cat['salesFrom']<=bis and cat['salesTo']<=bis:
                for o in cat['offers']:
                    o=dict(o);o['_cat']=cat['displayName'];sel.append(o)
    json.dump({'quelle':URL,'von':von,'bis':bis,'anzahl':len(sel),'offers':sel},open(sys.argv[2],'w'),ensure_ascii=False)
    print(len(sel),'Angebote für',von,'bis',bis)
