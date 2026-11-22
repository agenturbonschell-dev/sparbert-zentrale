import sys;sys.path.insert(0,'/home/user/work')
import numpy as np,cv2
from toon import *
from PIL import Image
INK=np.array([20,23,31],np.uint8)
def go(i,outdir):
    sub=np.load(f'p{i}_rgb.npy');mm=np.load(f'p{i}_mask.npy')
    den=cv2.fastNlMeansDenoisingColored(sub,None,7,7,5,15)
    cur=den
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
    er,ringm,al=smooth_alpha(mm);rgb=out.copy();rgb[ringm]=INK
    Image.fromarray(np.dstack([rgb,(al*255).astype(np.uint8)]),'RGBA').save(f'{outdir}/p{i}.png')
