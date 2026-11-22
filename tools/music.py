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
def music(dur,bpm=108):
    out=np.zeros(int(dur*SR));beat=60/bpm;bar=4*beat
    chords=[[60,64,67],[67,71,74],[69,72,76],[65,69,72]]   # C G Am F
    basses=[36,43,45,41]
    nb=int(dur/bar)+1
    for b in range(nb):
        t0=b*bar;ch=chords[b%4];bs=basses[b%4]
        put(out,pad([n2f(m) for m in ch],bar),t0,.35)
        for k in range(8):                                   # Achtel-Bass
            put(out,pluck(n2f(bs),beat*.5,.12),t0+k*beat/2,.55 if k%2==0 else .3)
        arp=[ch[0]+12,ch[1]+12,ch[2]+12,ch[1]+12,ch[2]+12,ch[1]+12,ch[0]+12,ch[2]+12]
        for k,m in enumerate(arp):put(out,pluck(n2f(m),beat*.5,.1),t0+k*beat/2,.28)
        for k in range(4):
            put(out,kick(),t0+k*beat,.7)
            put(out,hat(),t0+k*beat+beat/2,.35)
        put(out,clap(),t0+beat,.4);put(out,clap(),t0+3*beat,.4)
    # Ein-/Ausblenden
    f=int(1.2*SR);out[:f]*=np.linspace(0,1,f);out[-int(2*SR):]*=np.linspace(1,0,int(2*SR))
    return out
def sfxtrack(cfg):
    dur=cfg['dur'];out=np.zeros(int(dur*SR));S=cfg['start'];C=cfg['card']
    put(out,sfx.whoosh(),0.2,.7)
    for i,t0 in enumerate(S):
        put(out,sfx.pop(),t0+.05,.9)          # Karte
        put(out,sfx.pop(),t0+.75,.55)         # Sparbert
        put(out,sfx.swoosh_up()[:int(SR*.2)],t0+.97,.35)
        put(out,sfx.ding(1568)[:int(SR*.5)],t0+1.12,.45)   # Preisschild
        if C[i]:put(out,sfx.ding(1175)[:int(SR*.45)],t0+1.5,.4)   # Card-Hinweis
    put(out,sfx.cha(),dur-1.6,.6)
    return out
def finish(x,peak):
    p=np.abs(x).max();return x/p*peak if p>0 else x
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
    m=finish(music(cfg['dur']),.5);s=finish(sfxtrack(cfg),.8)
    sfx.save(f'{out}/music.wav',m);sfx.save(f'{out}/sfx.wav',s)
    mix=np.tanh((m*.45+s*.9))/np.tanh(1);sfx.save(f'{out}/mix.wav',finish(mix,.85))
    print('ok',cfg['dur'],'s')
