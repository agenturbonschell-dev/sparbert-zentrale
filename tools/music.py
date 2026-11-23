#!/usr/bin/env python3
"""Erzeugt Musik-Bett + Soundeffekte passend zu den Produktzeiten und schreibt music.wav, sfx.wav, mix.wav.
Nutzung: music.py <config.json> <ausgabeordner>   config: {"dur":61.8,"start":[...],"len":[...],"card":[...]}"""
import numpy as np,json,sys,os
import sfx
SR=sfx.SR
def n2f(m):return 440*2**((m-69)/12)
def pluck(f,dur,d=.18):
    n=int(SR*dur);t=np.arange(n)/SR
    y=(np.sin(2*np.pi*f*t)+.35*np.sin(4*np.pi*f*t)+.15*np.sin(6*np.pi*f*t))*np.exp(-t/d)*np.minimum(t/.004,1);return y
def pad(freqs,dur):
    n=int(SR*dur);t=np.arange(n)/SR;y=sum(np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*1.003*t) for f in freqs)/len(freqs)
    return y*np.minimum(t/.08,1)*np.exp(-t/(dur*.9))*.5
def kick(dur=.22):
    n=int(SR*dur);t=np.arange(n)/SR;f=np.linspace(120,45,n);ph=2*np.pi*np.cumsum(f)/SR;return np.sin(ph)*np.exp(-t/.07)
def hat(dur=.06):
    n=int(SR*dur);r=np.random.default_rng(9).standard_normal(n);r=np.diff(r,prepend=0);return r*np.exp(-np.arange(n)/SR/.015)*.5
def clap(dur=.16):
    n=int(SR*dur);r=np.random.default_rng(4).standard_normal(n);return sfx.lp(r,.5)*np.exp(-np.arange(n)/SR/.05)
def put(out,s,at,g=1):
    i=int(at*SR)
    if i>=len(out):return
    e=min(len(out),i+len(s));out[i:e]+=s[:e-i]*g
# ---- moderne Stimmen ----
def saw(f,dur,d=.12,k=.2):
    n=int(SR*dur);t=np.arange(n)/SR;y=(2*((f*t)%1)-1)*.6+np.sin(2*np.pi*f*t)*.4
    return sfx.lp(y*np.exp(-t/d)*np.minimum(t/.003,1),k)
def stab(notes,dur=.2,d=.1):
    return sum(saw(n2f(m),dur,d,.28)+saw(n2f(m)*1.006,dur,d,.28) for m in notes)/len(notes)
def snare():
    n=int(SR*.18);t=np.arange(n)/SR;r=np.random.default_rng(7).standard_normal(n)
    return sfx.lp(r,.55)*np.exp(-t/.06)*.8+np.sin(2*np.pi*190*t)*np.exp(-t/.05)*.5
def shaker():
    n=int(SR*.05);r=np.diff(np.random.default_rng(2).standard_normal(n),prepend=0);return r*np.exp(-np.arange(n)/SR/.02)*.3
def riser(dur):
    n=int(SR*dur);t=np.arange(n)/SR;r=np.random.default_rng(11).standard_normal(n)
    return np.diff(r,prepend=0)*(t/dur)**2*.5
def crash():
    n=int(SR*1.4);t=np.arange(n)/SR;r=np.diff(np.random.default_rng(12).standard_normal(n),prepend=0);return r*np.exp(-t/.5)*.6
def music(dur,bpm=104,outro=None,swing=.2):
    out=np.zeros(int(dur*SR));beat=60/bpm;bar=4*beat;st=bar/16
    chords=[[57,60,64],[53,57,60],[60,64,67],[55,59,62]]   # Am F C G
    roots=[33,29,36,31]
    lead=[[0,None,2,None,4,None,2,0],[0,None,2,4,None,2,None,None]]
    pent=[69,72,74,76,79,81]
    nb=int(dur/bar)+1
    def T(b,s):return b*bar+s*st+(swing*st if s%2 else 0)   # Swing auf ungeraden 16teln
    for b in range(nb):
        ch=chords[b%4];rt=roots[b%4]
        in_out=outro is not None and b*bar>=outro-.01
        for s in (0,6,10) if not in_out else (0,3,6,8,10,14):
            put(out,kick(),T(b,s),.8)
        for s in (4,12):put(out,snare(),T(b,s),.6);put(out,clap(),T(b,s),.3)
        for s in range(16):put(out,hat() if s%2==0 else shaker(),T(b,s),.3 if s%4==0 else .2)
        for s,o in ((0,0),(3,0),(6,12),(8,0),(10,0),(14,12)):
            put(out,saw(n2f(rt+o),st*2.2,.16,.12),T(b,s),.5)
        for s in (2,5,9,13):put(out,stab([m+12 for m in ch],st*1.6,.09),T(b,s),.3)
        if b>=2 and not in_out:
            for j,deg in enumerate(lead[b%2]):
                if deg is not None:put(out,pluck(n2f(pent[deg]),st*2,.1),T(b,j*2),.22)
    if outro:
        put(out,riser(1.0),outro-1.0,.8);put(out,crash(),outro,.6)
    f=int(.8*SR);out[:f]*=np.linspace(0,1,f);out[-int(1.5*SR):]*=np.linspace(1,0,int(1.5*SR))
    return out
# ---- moderne Effekte: Mausklick, Tap, Swipe, Blip, Glitzer ----
def click(g2=.5):
    n=int(SR*.2);y=np.zeros(n)
    for at,g in ((0,1),(.075,g2)):
        m=int(SR*.02);t=np.arange(m)/SR;r=np.diff(np.random.default_rng(int(at*100)+1).standard_normal(m),prepend=0)
        c=(r*.7+np.sin(2*np.pi*2600*t)*.6)*np.exp(-t/.0045)*g;i=int(at*SR);y[i:i+m]+=c
    return y
def tap():
    return sfx.tone((1000,520),.07,d=.02)*.8+click(0)[:int(SR*.07)]*.5
def blip():
    return sfx.tone((480,1150),.11,d=.05)*.7+.25*sfx.tone((960,2300),.11,d=.03)
def swipe():
    n=int(SR*.2);r=np.random.default_rng(5).standard_normal(n);bp=sfx.lp(r,.4)-sfx.lp(r,.06);return bp*np.sin(np.linspace(0,np.pi,n))**1.5*2.2
def thump():
    return sfx.tone((150,48),.2,d=.08)*.9
def sparkle(n=3,base=2093):
    y=np.zeros(int(SR*.5))
    for k in range(n):
        f=base*[1,1.25,1.5,2][k%4];s=sfx.tone(f,.25,d=.09)*.45;i=int(k*.06*SR);y[i:i+len(s)]+=s[:len(y)-i]
    return y
def notif():
    y=np.zeros(int(SR*.6))
    for at,f in ((0,1319),(.11,1760)):
        s=sfx.tone(f,.4,d=.14)*.6;i=int(at*SR);y[i:i+len(s)]+=s[:len(y)-i]
    return y
def sfxtrack(cfg):
    dur=cfg['dur'];out=np.zeros(int(dur*SR));S=cfg['start'];C=cfg['card']
    put(out,swipe(),0.15,.8)
    for i,t0 in enumerate(S):
        v=i%3                                           # abwechselnd drei Klangfarben
        put(out,thump(),t0+.04,.6)
        put(out,[click,tap,swipe][v](),t0+.05,[.9,.8,.7][v])       # Karte erscheint
        put(out,blip(),t0+.75,.5)                                 # Sparbert poppt rein
        put(out,sparkle(3 if v!=1 else 2,[2093,2349,2637][v]),t0+1.1,.5)  # Preis
        if C[i]:put(out,click(.9),t0+1.5,.7);put(out,notif()[:int(SR*.5)],t0+1.62,.4)  # Karten-Hinweis
    o=cfg.get('outro')
    if o:
        put(out,swipe(),o+.1,.8);put(out,thump(),o+.15,.7);put(out,sparkle(4,2093),o+.2,.6)
        put(out,click(.9),o+1.5+.15,1.0);put(out,notif(),o+1.7,.7)       # Folgen-Button gedrückt
        for k,d in enumerate((.9,1.05)):put(out,tap(),o+.15+d,.6)         # Chips
    return out
def finish(x,peak):
    p=np.abs(x).max();return x/p*peak if p>0 else x
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
    m=finish(music(cfg['dur'],outro=cfg.get('outro')),.5);s=finish(sfxtrack(cfg),.8)
    sfx.save(f'{out}/music.wav',m);sfx.save(f'{out}/sfx.wav',s)
    mix=np.tanh((m*.45+s*.9))/np.tanh(1);sfx.save(f'{out}/mix.wav',finish(mix,.85))
    print('ok',cfg['dur'],'s')
