import sys;sys.path.insert(0,'/home/user/work')
import numpy as np,cv2
from toon import toon_upscale
from PIL import Image
INK=np.array([20,23,31],np.uint8)
def clean_ring(mm,k=4,ring=15):
    A=cv2.resize(mm.astype(np.uint8)*255,None,fx=k,fy=k,interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
    h,w=A.shape
    pad=ring*3;A=np.pad(A,pad)
    sil=cv2.GaussianBlur(A,(0,0),9.0)>0.5                       # Silhouette stark geglättet
    sil=cv2.GaussianBlur(sil.astype(np.float32),(0,0),6.0)>0.5
    inner=cv2.erode(sil.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))   # Original-Halo ausblenden
    outer=cv2.dilate(sil.astype(np.uint8),cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*ring+1,2*ring+1)))
    outer=(cv2.GaussianBlur(outer.astype(np.float32),(0,0),11.0)>0.5).astype(np.uint8)            # runde, weiche Außenlinie
    # Antialiasing
    al_out=cv2.GaussianBlur(outer.astype(np.float32),(0,0),1.8)
    return inner.astype(bool)[pad:-pad,pad:-pad],al_out[pad:-pad,pad:-pad]
def go(i,outdir):
    sub=np.load(f'p{i}_rgb.npy');mm=np.load(f'p{i}_mask.npy')
    den=cv2.fastNlMeansDenoisingColored(sub,None,7,7,5,15);cur=den
    for _ in range(2):
        cur=cv2.resize(cur,None,fx=2,fy=2,interpolation=cv2.INTER_LANCZOS4)
        b=cv2.GaussianBlur(cur,(0,0),1.3);cur=cv2.addWeighted(cur,1.6,b,-.6,0)
    up=cv2.bilateralFilter(cur,7,22,4)
    lab=cv2.cvtColor(up,cv2.COLOR_RGB2LAB).astype(np.float32)
    k=4;fgm=cv2.resize(mm.astype(np.uint8)*255,None,fx=k,fy=k,interpolation=cv2.INTER_LINEAR)>100
    pts=lab[fgm];rng=np.random.default_rng(1);idx=rng.choice(len(pts),min(160000,len(pts)),replace=False)
    _,_,cent=cv2.kmeans(pts[idx],56,None,(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,25,.5),2,cv2.KMEANS_PP_CENTERS)
    flat=lab.reshape(-1,3);li=np.empty(len(flat),np.int32)
    for s in range(0,len(flat),400000):
        dd=((flat[s:s+400000,None,:]-cent[None,:,:])**2).sum(2);li[s:s+400000]=dd.argmin(1)
    post=cv2.cvtColor(np.clip(cent[li].reshape(lab.shape),0,255).astype(np.uint8),cv2.COLOR_LAB2RGB);post=cv2.medianBlur(post,5)
    out=np.clip(post.astype(np.float32)*.55+up.astype(np.float32)*.45,0,255).astype(np.uint8)
    inner,al=clean_ring(mm)
    # Innenfläche: Farbe; Ring: Tinte. Außerhalb inner liegende Pixel (Randhalo + Ring) -> Tinte
    rgb=out.copy();rgb[~inner]=INK
    Image.fromarray(np.dstack([rgb,(al*255).astype(np.uint8)]),'RGBA').save(f'{outdir}/p{i}.png')
