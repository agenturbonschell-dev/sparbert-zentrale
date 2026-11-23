#!/usr/bin/env python3
"""Baut aus den Kacheln eines Karussells ein Reel (9:16) mit eigener Musik (selbst erzeugt, lizenzfrei).
Nutzung: slideshow.py <karussell-ordner> <ausgabe.mp4>   (Ordner mit tile_1..5.jpg)"""
import sys,os,subprocess,glob
import numpy as np
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT+'/tools')
import sfx,music
def main(folder,out,per=3.2,fade=.45):
    tiles=sorted(glob.glob(f'{folder}/tile_*.jpg'));n=len(tiles)
    durs=[per+(.6 if i in(0,n-1) else 0) for i in range(n)]
    total=sum(durs)-fade*(n-1)
    # Musik + Wisch-Effekt an den Übergängen
    m=music.finish(music.music(total+.5),.5)
    s=np.zeros_like(m);t=0
    for d in durs[:-1]:
        t+=d-fade;music.put(s,sfx.whoosh()[:int(sfx.SR*.3)],t-.05,.4)
    music.put(s,sfx.swoosh_up()[:int(sfx.SR*.2)],.05,.3)
    mix=music.finish(np.tanh(m*.55+s*.5),.85)
    wav=out.replace('.mp4','.wav');sfx.save(wav,mix)
    inputs=[];filt=[]
    for i,tl in enumerate(tiles):
        inputs+=['-loop','1','-framerate','30','-t',f'{durs[i]:.2f}','-i',tl]
        filt.append(f"[{i}:v]split[a{i}][b{i}];[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg{i}];[b{i}]scale=1080:-2[fg{i}];[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p[v{i}]")
    cur='v0';off=durs[0]-fade
    for i in range(1,n):
        filt.append(f"[{cur}][v{i}]xfade=transition=fade:duration={fade}:offset={off:.2f}[x{i}]");cur=f'x{i}';off+=durs[i]-fade
    cmd=['ffmpeg','-y','-loglevel','error']+inputs+['-i',wav,'-filter_complex',';'.join(filt),'-map',f'[{cur}]','-map',f'{n}:a','-c:v','libx264','-crf','23','-preset','medium','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k','-af','lowpass=f=7500,loudnorm=I=-17:TP=-1.5:LRA=7','-movflags','+faststart','-shortest',out]
    subprocess.run(cmd,check=True);print('fertig',out,round(total,1),'s')
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
