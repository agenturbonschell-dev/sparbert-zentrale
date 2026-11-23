#!/usr/bin/env python3
"""Erzeugt Beschreibungstext + Hashtags je Video aus den Produktdaten. Nutzung: caption.py <haendler-id> <products.json> [variante]"""
import json,sys,random,datetime
def load(p):return json.load(open(p,encoding='utf-8'))
def make(retailer,data,variant=0,platform='ig'):
    cfg=load(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'retailers.json'));R={r['id']:r for r in cfg['retailers']}[retailer]
    prods=data['products'];von,bis=data['von'],data['bis']        # ISO-Datum, aus den Quelldaten
    d=lambda s:datetime.date.fromisoformat(s).strftime('%d.%m.')
    tag=R.get('handle_ig' if platform=='ig' else 'handle_tt')
    ref=('@'+tag.lstrip('@')) if tag else R['name']
    top=sorted(prods,key=lambda p:-int(p.get('save','0').strip('-%') or 0))[:3]
    hooks=[f"🔥 {R['name']}: Das sind die besten Angebote vom {d(von)} bis {d(bis)}!",
           f"💰 Diese Woche bei {R['name']}: {top[0]['brand'].title()} {top[0]['name']} für {(top[0].get('card') or top[0]['price'])} €!",
           f"🛒 Nicht verpassen! {R['name']}-Angebote {d(von)}–{d(bis)}"]
    lines=[hooks[variant%len(hooks)],'']
    for p in prods[:6]:
        price=p.get('card') or p['price']
        parts=[]
        if p.get('card') and R['card']:parts.append(f"mit {R['card']}")
        v=p.get('valid') or ''
        if v and not v.startswith('gültig bis Sa') and not (v.startswith('Mo.') and v.rstrip('.').endswith(f"Sa. {bis[8:]}.{bis[5:7]}")):parts.append(v.replace('gültig ','').rstrip('.')) # Tages-Bedingung zeigen
        if 'max.' in (p.get('unit') or ''):parts.append(p['unit'].split('·')[-1].strip())
        cond=f" ({', '.join(parts)})" if parts else ''
        lines.append(f"• {p['brand'].title()} {p['name']}: {price} €{cond}")
    lines+=['',f"📅 Gültig {d(von)} bis {d(bis)}",
            f"Unbezahlte Werbung / Kostenlose Werbung für {ref}",
            "Preise können je Markt abweichen. Angebote teils nur mit App/Karte oder an bestimmten Tagen.",'']
    tags=cfg['hashtags_basis']+cfg['hashtags_je_haendler'][retailer]
    # Instagram: höchstens 5 Hashtags (Händler-Tags zuerst, dann die stärksten Basis-Tags)
    pick=[t for t in cfg['hashtags_je_haendler'][retailer]]+[t for t in cfg['hashtags_basis'] if t not in cfg['hashtags_je_haendler'][retailer]]
    return '\n'.join(lines)+' '.join(pick[:5])
if __name__=='__main__':
    print(make(sys.argv[1],load(sys.argv[2]),int(sys.argv[3]) if len(sys.argv)>3 else 0))
