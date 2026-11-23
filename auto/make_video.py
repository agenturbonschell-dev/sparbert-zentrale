#!/usr/bin/env python3
"""Rendert (optional) und vertont das Wochenvideo eines Händlers. Nutzung: make_video.py <haendler-id> [--skip-render]
Ergebnis: out/<id>_KW48_ton.mp4 (Name nach Händler-ID und Datei data/KW48/<id>_products.json)"""
import sys,os,subprocess,json
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hid=sys.argv[1];skip='--skip-render' in sys.argv
pj=f'{ROOT}/data/KW48/{hid}_products.json';silent=f'{ROOT}/out/{hid}_KW48.mp4';ton=f'{ROOT}/out/{hid}_KW48_ton.mp4'
if not skip:subprocess.run(['python3',f'{ROOT}/auto/build_video.py',hid,pj,silent],check=True)
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://"+f'{ROOT}/templates/_build_{hid}.html'+"?cap');await p.waitForFunction('window.ready',null,{timeout:60000});const r=await p.evaluate(()=>({dur:DUR,outro:OUT,start:START,card:PRODUCTS.map(x=>!!x.card)}));console.log(JSON.stringify(r));await b.close()})()"
cfg=subprocess.run(['node','-e',js],capture_output=True,text=True,cwd=ROOT+'/tools',check=True).stdout.strip()
os.makedirs(f'{ROOT}/out/audio_{hid}',exist_ok=True);open(f'/tmp/mus_{hid}.json','w').write(cfg)
subprocess.run(['python3',f'{ROOT}/tools/music.py',f'/tmp/mus_{hid}.json',f'{ROOT}/out/audio_{hid}'],check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',silent,'-i',f'{ROOT}/out/audio_{hid}/mix.wav','-map','0:v','-map','1:a','-c:v','libx264','-crf','25','-maxrate','3500k','-bufsize','7000k','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-af','lowpass=f=7500,loudnorm=I=-17:TP=-1.5:LRA=7','-movflags','+faststart','-shortest',ton],check=True)
print('fertig',ton)
