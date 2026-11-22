from PIL import Image, ImageFilter
import numpy as np, json, sys
from collections import deque
PG='/home/user/work/lidl/pg/'
# name: (page, half-res box x0,y0,x1,y1, tol)
B={
 'nutella':(1,(0,395,240,690),55),
 'sekt':(1,(125,905,250,1075),55),
 'pizza':(1,(358,925,472,1055),55),
 'butter':(10,(385,440,700,665),50),
 'milchreis':(14,(300,90,595,325),50),
 'landliebe':(14,(490,345,645,505),50),
 'leerdammer':(11,(50,85,240,245),50),
 'miracel':(11,(545,85,695,240),50),
 'mccain':(33,(38,85,235,228),50),
 'iglo':(33,(252,85,430,238),50),
 'pampers':(35,(488,278,692,430),50),
 'cola':(11,(255,612,432,790),50),
 'volvic':(11,(532,880,695,1015),50),
 'chipsfrisch':(11,(262,345,445,505),50),
 'monte':(34,(35,615,238,812),50),
 'moevenpick':(34,(392,85,688,282),50),
 'ritter':(33,(482,82,672,238),50),
}
def cut(n):
    p,(x0,y0,x1,y1),tol=B[n]
    im=Image.open(f'{PG}p{p:02d}.jpg').convert('RGB')
    if n=='nutella':
        from PIL import ImageDraw
        ImageDraw.Draw(im).rectangle((290,830,480,970),fill=tuple(np.array(im.getpixel((420,1000)))))
    im=im.crop((x0*2,y0*2,x1*2,y1*2));a=np.array(im).astype(int);H,W,_=a.shape
    # Hintergrundfarben: Median der Randpixel
    edge=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]);cols=[]
    from collections import Counter
    c=Counter(map(tuple,(edge//16*16)));top=[np.array(k)+8 for k,_ in c.most_common(3)]
    near=np.zeros((H,W),bool)
    for col in top:near|=(np.abs(a-col).sum(2)<tol*2.2)
    bg=np.zeros((H,W),bool);q=deque()
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
    fg=~bg
    # größte zusammenhängende Komponente(n) behalten, Löcher füllen
    m=Image.fromarray((fg*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    m=np.array(m)>127
    lab=np.zeros((H,W),int);k=0;sizes=[]
    for y in range(H):
        for x in range(W):
            if m[y,x] and lab[y,x]==0:
                k+=1;lab[y,x]=k;qq=deque([(y,x)]);s=0
                while qq:
                    cy,cx=qq.popleft();s+=1
                    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
                        ny,nx=cy+dy,cx+dx
                        if 0<=ny<H and 0<=nx<W and m[ny,nx] and lab[ny,nx]==0:lab[ny,nx]=k;qq.append((ny,nx))
                sizes.append(s)
    keep=np.isin(lab,[i+1 for i,s in enumerate(sizes) if s>0.12*max(sizes)])
    # Löcher füllen
    inv=~keep;seen=np.zeros((H,W),bool);qq=deque()
    for x in range(W):
        for y in(0,H-1):
            if inv[y,x]:seen[y,x]=1;qq.append((y,x))
    for y in range(H):
        for x in(0,W-1):
            if inv[y,x] and not seen[y,x]:seen[y,x]=1;qq.append((y,x))
    while qq:
        y,x=qq.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<H and 0<=nx<W and inv[ny,nx] and not seen[ny,nx]:seen[ny,nx]=1;qq.append((ny,nx))
    keep=~seen
    al=Image.fromarray((keep*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    ys,xs=np.nonzero(np.array(al)>30);bx0,bx1,by0,by1=xs.min(),xs.max(),ys.min(),ys.max()
    rgba=im.convert('RGBA');rgba.putalpha(al);rgba=rgba.crop((bx0,by0,bx1+1,by1+1))
    pad=24;s=min(2.0,900/max(rgba.size));rgba=rgba.resize((int(rgba.width*s),int(rgba.height*s)),Image.LANCZOS)
    can=Image.new('RGBA',(rgba.width+2*pad,rgba.height+2*pad),(0,0,0,0))
    a2=Image.new('L',can.size,0);a2.paste(rgba.getchannel('A'),(pad,pad))
    ring=a2.filter(ImageFilter.MaxFilter(13)).filter(ImageFilter.GaussianBlur(1.2))
    w=Image.new('RGBA',can.size,(255,255,255,255));w.putalpha(ring);can.alpha_composite(w);can.alpha_composite(rgba,(pad,pad))
    can.save(f'/home/user/sparbert/assets/lidl/{n}.png');return can
if __name__=='__main__':
    names=sys.argv[1:] or list(B)
    sheet=Image.new('RGBA',(260*6,330*((len(names)+5)//6)),(90,150,90,255))
    for i,n in enumerate(names):
        c=cut(n);t=c.copy();t.thumbnail((250,320));sheet.alpha_composite(t,(260*(i%6)+5,330*(i//6)+5))
    sheet.convert('RGB').save('/tmp/lidlcut.png')
