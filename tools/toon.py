import cv2, numpy as np
def toon_upscale(sub,mm,k=4,K=30,mix=.78):
    h,w=sub.shape[:2]
    up=cv2.resize(sub,None,fx=k,fy=k,interpolation=cv2.INTER_CUBIC)
    up=cv2.bilateralFilter(up,9,26,5);up=cv2.bilateralFilter(up,7,20,4)
    lab=cv2.cvtColor(up,cv2.COLOR_RGB2LAB).astype(np.float32)
    fgm=cv2.resize(mm.astype(np.uint8)*255,None,fx=k,fy=k,interpolation=cv2.INTER_LINEAR)>100
    pts=lab[fgm]
    rng=np.random.default_rng(1);idx=rng.choice(len(pts),min(160000,len(pts)),replace=False)
    crit=(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,25,.5)
    _,_,cent=cv2.kmeans(pts[idx],K,None,crit,2,cv2.KMEANS_PP_CENTERS)
    flat=lab.reshape(-1,3);lab_idx=np.empty(len(flat),np.int32)
    for s in range(0,len(flat),400000):
        d=((flat[s:s+400000,None,:]-cent[None,:,:])**2).sum(2);lab_idx[s:s+400000]=d.argmin(1)
    post=cent[lab_idx].reshape(lab.shape)
    post=cv2.cvtColor(np.clip(post,0,255).astype(np.uint8),cv2.COLOR_LAB2RGB)
    post=cv2.medianBlur(post,5)
    out=(post.astype(np.float32)*mix+up.astype(np.float32)*(1-mix))
    out=np.clip(out,0,255).astype(np.uint8)
    # schärfen
    blur=cv2.GaussianBlur(out,(0,0),1.6);out=cv2.addWeighted(out,1.5,blur,-.5,0)
    return out,up
def smooth_alpha(mm,k=4,ring=14,pad=0):
    A=cv2.resize(mm.astype(np.uint8)*255,None,fx=k,fy=k,interpolation=cv2.INTER_CUBIC).astype(np.float32)/255
    A=cv2.GaussianBlur(A,(0,0),3.4);sil=(A>.5).astype(np.uint8)
    # Rand-Halo entfernen (6 px), sauberen Tintenring neu aufbauen
    er=cv2.erode(sil,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*5+1,2*5+1)))
    di=cv2.dilate(er,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*(5+ring)+1,2*(5+ring)+1)))
    ringm=(di==1)&(er==0)
    al=cv2.GaussianBlur(di.astype(np.float32),(0,0),1.1)
    return er.astype(bool),ringm,al
