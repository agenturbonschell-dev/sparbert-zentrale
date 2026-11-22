import numpy as np, wave, sys, json
SR=44100
def env(n,a=.005,d=.15,sus=0.0):
    t=np.arange(n)/SR;e=np.minimum(t/a,1)*np.exp(-t/d);return e
def tone(f,dur,wave='sin',d=.12,a=.004):
    n=int(SR*dur);t=np.arange(n)/SR
    if isinstance(f,tuple):ph=2*np.pi*np.cumsum(np.linspace(f[0],f[1],n))/SR
    else:ph=2*np.pi*f*t
    y=np.sin(ph) if wave=='sin' else (2*(ph/(2*np.pi)%1)-1)*.6+np.sin(ph)*.4
    return y*env(n,a,d)
def noise(dur,d=.12,a=.003):
    n=int(SR*dur);return np.random.default_rng(3).standard_normal(n)*env(n,a,d)
def lp(x,k):
    out=np.copy(x);
    for i in range(1,len(x)):out[i]=out[i-1]+k*(x[i]-out[i-1])
    return out
def pop(): # weicher Blubb-Pop
    return .9*tone((620,240),.16,d=.05)+.25*lp(noise(.16,.02),.4)
def whoosh():
    n=int(SR*.45);x=lp(np.random.default_rng(5).standard_normal(n),.12)*np.sin(np.linspace(0,np.pi,n))**2;return x*1.6
def ding(f=1318):
    return .6*tone(f,.6,d=.22)+.35*tone(f*2.01,.6,d=.15)+.2*tone(f*3.02,.6,d=.08)
def cha():  # Kasse-Klingel + Münzen
    y=ding(1760)*.8
    for k,dt in enumerate([.07,.13,.2,.27]):
        c=tone(3200+k*300,.12,d=.03)*.35;y=add(y,c,dt)
    return y
def swoosh_up():
    return .7*tone((300,1500),.28,d=.2)+.15*lp(noise(.28,.18),.3)
def add(a,b,at):
    a=np.asarray(a)
    i=int(at*SR);n=max(len(a),i+len(b));o=np.zeros(n);o[:len(a)]+=a;o[i:i+len(b)]+=b;return o
def mix(events,dur):
    out=np.zeros(int(dur*SR)+SR)
    for at,fn,g in events:
        s=fn()*g;i=int(at*SR);out[i:i+len(s)]+=s[:len(out)-i]
    pk=np.abs(out).max();out=out/pk*0.55 if pk>0 else out
    # sanfter Limiter
    out=np.tanh(out*1.3)/np.tanh(1.3)*.8
    return out[:int(dur*SR)]
def save(fn,y):
    y16=(np.clip(y,-1,1)*32767).astype(np.int16)
    with wave.open(fn,'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(y16.tobytes())
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]));ev=[]
    F={'pop':pop,'whoosh':whoosh,'ding':ding,'cha':cha,'up':swoosh_up}
    for e in cfg['events']:ev.append((e['t'],F[e['fx']],e.get('g',1)))
    save(sys.argv[2],mix(ev,cfg['dur']))
