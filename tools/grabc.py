import cv2, numpy as np, sys
from PIL import Image, ImageFilter
from collections import Counter, deque
PG='/home/user/work/lidl/pg/'
# name: (page, half-res box)  -- Boxen mit etwas Hintergrund rundherum
B={
 'nutella':(1,(0,395,240,690)),
 'butter':(10,(385,435,672,645)),
 'milchreis':(14,(405,82,600,325)),
 'landliebe':(14,(490,342,652,495)),
 'leerdammer':(11,(48,82,242,248)),
 'miracel':(11,(543,82,697,242)),
 'mccain':(33,(36,82,238,230)),
 'iglo':(33,(250,82,432,240)),
 'cola':(11,(250,604,342,788)),
 'arizona':(11,(16,610,110,888)),
 'chipsfrisch':(11,(260,342,448,508)),
 'monte':(34,(33,612,240,815)),
 'moevenpick':(34,(390,82,690,285)),
 'ritter':(33,(480,80,674,240)),
 'pampers':(35,(486,276,694,432)),
}
def run(n,iters=6):
    p,(x0,y0,x1,y1)=B[n]
    im=Image.open(f'{PG}p{p:02d}.jpg').convert('RGB')
    if n=='nutella':
        from PIL import ImageDraw
        ImageDraw.Draw(im).rectangle((290,830,480,970),fill=tuple(im.getpixel((420,1000))))
    im=im.crop((x0*2,y0*2,x1*2,y1*2));a=np.array(im);H,W,_=a.shape
    bgr=cv2.cvtColor(a,cv2.COLOR_RGB2BGR)
    # Hintergrundfarben aus dem Rand
    edge=np.concatenate([a[:6].reshape(-1,3),a[-6:].reshape(-1,3),a[:,:6].reshape(-1,3),a[:,-6:].reshape(-1,3)]).astype(int)
    c=Counter(map(tuple,edge//20*20));cols=[np.array(k)+10 for k,v in c.most_common(3)]
    if n=='nutella':cols+=[np.array([250,225,10]),np.array([235,200,0])]
    near=np.zeros((H,W),bool)
    for col in cols:near|=(np.abs(a.astype(int)-col).sum(2)<70)
    mask=np.full((H,W),cv2.GC_PR_FGD,np.uint8)
    mask[near]=cv2.GC_PR_BGD
    mask[:8]=cv2.GC_BGD;mask[-8:]=cv2.GC_BGD;mask[:,:8]=cv2.GC_BGD;mask[:,-8:]=cv2.GC_BGD
    # sicherer Vordergrund: Kern (erodierte Nicht-bg-Fläche)
    core=cv2.erode((~near).astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(41,41)))
    mask[core>0]=cv2.GC_FGD
    bg=np.zeros((1,65),np.float64);fg=np.zeros((1,65),np.float64)
    cv2.grabCut(bgr,mask,None,bg,fg,iters,cv2.GC_INIT_WITH_MASK)
    m=((mask==cv2.GC_FGD)|(mask==cv2.GC_PR_FGD)).astype(np.uint8)
    # größte Komponente + Löcher füllen + glätten
    nl,lab,st,_=cv2.connectedComponentsWithStats(m)
    if nl>1:
        keep=[i for i in range(1,nl) if st[i,4]>0.15*st[1:,4].max()]
        m=np.isin(lab,keep).astype(np.uint8)
    cnts,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE);m2=np.zeros_like(m);cv2.drawContours(m2,cnts,-1,1,-1)
    m2=cv2.morphologyEx(m2,cv2.MORPH_OPEN,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))
    al=cv2.GaussianBlur(m2.astype(np.float32),(0,0),2.2);al=np.clip((al-.5)*3+.5,0,1)
    al=cv2.erode(al,np.ones((3,3)))   # 1px nach innen gegen Farbsaum
    al=cv2.GaussianBlur(al,(0,0),.8)
    rgba=np.dstack([a,(al*255).astype(np.uint8)]);img=Image.fromarray(rgba,'RGBA')
    ys,xs=np.nonzero(al>.1);img=img.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    pad=24;s=min(2.0,900/max(img.size));img=img.resize((int(img.width*s),int(img.height*s)),Image.LANCZOS)
    can=Image.new('RGBA',(img.width+2*pad,img.height+2*pad),(0,0,0,0));a2=Image.new('L',can.size,0);a2.paste(img.getchannel('A'),(pad,pad))
    ring=a2.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(1.3))
    w=Image.new('RGBA',can.size,(255,255,255,255));w.putalpha(ring);can.alpha_composite(w);can.alpha_composite(img,(pad,pad))
    can.save(f'/home/user/sparbert/assets/lidl/{n}.png');return can
if __name__=='__main__':
    names=sys.argv[1:] or list(B)
    sheet=Image.new('RGBA',(300*5,360*((len(names)+4)//5)),(240,225,200,255))
    for i,n in enumerate(names):
        c=run(n);t=c.copy();t.thumbnail((290,350));sheet.alpha_composite(t,(300*(i%5)+5,360*(i//5)+5))
    sheet.convert('RGB').save('/tmp/gc.png')
