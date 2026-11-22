#!/usr/bin/env python3
"""Lädt Händler-Packshots (weißer Hintergrund), stellt sie frei und gibt ihnen einen weißen Aufkleber-Rand.
Nutzung: cutout.py <products.json> <ausgabeordner>"""
import json,sys,subprocess,os
from PIL import Image,ImageFilter
import numpy as np
from collections import deque
def cut(src,dst):
    im=Image.open(src).convert('RGB');a=np.array(im).astype(int);H,W,_=a.shape
    near=(a.min(2)>=249);bg=np.zeros((H,W),bool);q=deque()
    for x in range(W):
        for y in(0,H-1):
            if near[y,x] and not bg[y,x]:bg[y,x]=1;q.append((y,x))
    for y in range(H):
        for x in(0,W-1):
            if near[y,x] and not bg[y,x]:bg[y,x]=1;q.append((y,x))
    while q:
        y,x=q.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and near[ny,nx] and not bg[ny,nx]:bg[ny,nx]=1;q.append((ny,nx))
    m=Image.fromarray(((~bg)*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.8))
    ys,xs=np.nonzero(np.array(m)>20)
    if len(xs)==0:return False
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    r=im.convert('RGBA');r.putalpha(m);r=r.crop((x0,y0,x1+1,y1+1))
    if max(r.size)/min(r.size)>5:return False        # Streifen, kein Produktbild
    s=900/max(r.size);r=r.resize((int(r.width*s),int(r.height*s)),Image.LANCZOS);pad=26
    can=Image.new('RGBA',(r.width+2*pad,r.height+2*pad),(0,0,0,0));al=Image.new('L',can.size,0);al.paste(r.getchannel('A'),(pad,pad))
    ring=al.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(1.2))
    w=Image.new('RGBA',can.size,(255,255,255,255));w.putalpha(ring);can.alpha_composite(w);can.alpha_composite(r,(pad,pad));can.save(dst);return True
if __name__=='__main__':
    d=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True);raw=os.path.join(out,'raw');os.makedirs(raw,exist_ok=True)
    ok=[];bad=[]
    for p in d['products']:
        rp=os.path.join(raw,p['img']+'.png')
        subprocess.run(['curl','-sS','-m','40','-o',rp,p['image']+'?wid=1100&hei=1100&fmt=png-alpha'],check=False)
        try:good=cut(rp,os.path.join(out,p['img']+'.png'))
        except Exception as e:good=False
        (ok if good else bad).append(p['img'])
    print('Bilder ok:',len(ok),'Fehler:',bad)
