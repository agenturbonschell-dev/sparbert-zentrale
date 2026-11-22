#!/usr/bin/env python3
"""Setzt products.json in die Händler-Vorlage ein und rendert das Video (4 Prozesse parallel, 2× Auflösung, danach auf 1080×1920).
Nutzung: build_video.py <haendler-id> <products.json> <ausgabe.mp4>"""
import json,sys,re,os,subprocess,datetime,math,time
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGE=['Mo.','Di.','Mi.','Do.','Fr.','Sa.','So.']
def build_html(hid,data,out_html):
    cfg={r['id']:r for r in json.load(open(f'{ROOT}/auto/retailers.json'))['retailers']}[hid]
    tpl={'kaufland':'angebote_kaufland','lidl':'angebote_lidl'}.get(hid,'angebote_kaufland')
    s=open(f'{ROOT}/templates/{tpl}.html').read()
    v=datetime.date.fromisoformat(data['von']);b=datetime.date.fromisoformat(data['bis'])
    date_txt=f'gültig {v.day}. – {b.day}.{b.month:02d}.{b.year}'
    prods=[{k:p[k] for k in p if k!='image'} for p in data['products']]
    a=s.index('const PRODUCTS=[');e=s.index('];',a)+2
    s=s[:a]+'const PRODUCTS='+json.dumps(prods,ensure_ascii=False,indent=1)+';'+s[e:]
    s=re.sub(r"const DATE_TXT='[^']*';",f"const DATE_TXT='{date_txt}';",s)
    s=s.replace('../assets/offers/','../assets/offers/')
    open(out_html,'w').write(s);return out_html
def frames(html):
    js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://"+html+"?cap');await p.waitForFunction('window.ready',null,{timeout:60000});console.log(Math.ceil(await p.evaluate(()=>window.DUR)*30));await b.close()})()"
    return int(subprocess.run(['node','-e',js],capture_output=True,text=True,cwd=ROOT+'/tools',check=True).stdout.strip())
def render(html,out):
    n=frames(html);q=math.ceil(n/4);procs=[];segs=[]
    for k in range(4):
        a,b=k*q,min(n,(k+1)*q);seg=f'/tmp/seg_{os.getpid()}_{k}.mp4';segs.append(seg)
        procs.append(subprocess.Popen(['node',f'{ROOT}/tools/render3.js','file://'+html,str(a),str(b),seg,'2'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
    for p in procs:p.wait()
    lst=f'/tmp/list_{os.getpid()}.txt';open(lst,'w').write(''.join(f"file '{s}'\n" for s in segs))
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',lst,'-c','copy',out],check=True);return n
if __name__=='__main__':
    hid,pj,out=sys.argv[1:4];data=json.load(open(pj))
    html=build_html(hid,data,f'{ROOT}/templates/_build_{hid}.html');n=render(html,out);print('fertig',out,n,'Frames')
