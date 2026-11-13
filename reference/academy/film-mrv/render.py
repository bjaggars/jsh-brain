"""JSH Training Academy · MyRealtyVault campus · phone-format film renderer.
Real captures from the TEST film set (Harbor & Oak Realty). The phone sits on the left, a moving zoom window on the right,
brass highlight rings, pointer + tap ripple, headline per step, Kokoro voice-over. Same voice and pacing as the AWP campus.
usage: python3 render.py <id,id|all|lessons|intros> [stills]"""
import json, math, os, subprocess, sys, random
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,30
F='/usr/share/fonts/opentype/inter/InterDisplay-'
def font(w,s): return ImageFont.truetype(F+w+'.otf',s)
def ease(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def eout(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
PAPER,INK,SOFT,BLUE,BRASS=(18,24,30),(232,237,241),(157,170,182),(110,168,232),(217,178,95)
def cmix(c,a,bg=None):
    bg=bg or PAPER; a=max(0.,min(1.,a)); return tuple(int(bg[i]+(c[i]-bg[i])*a) for i in range(3))
PX,PY,PW,PH=118,60,443,960            # phone screen on canvas (1 css px = 1 px)
ZX,ZY,ZW,ZH=650,236,1150,736          # zoom window
os.makedirs('vo',exist_ok=True); os.makedirs('out',exist_ok=True)
import importlib
FS=importlib.import_module(os.environ.get('FILMS','films')); FILMS,PATH=FS.FILMS,FS.PATH; CAPD=getattr(FS,'CAP','cap'); PRE=getattr(FS,'PREFIX','')
_s={}; _b={}
def S(n):
    if n not in _s:
        im=Image.open(f'{CAPD}/{n}.jpg').convert('RGB'); _s[n]=(im, im.resize((PW,PH),Image.LANCZOS))
        _b[n]=json.load(open(f'{CAPD}/{n}.json')) if os.path.exists(f'{CAPD}/{n}.json') else {}
    return _s[n]
def box(shot,k):
    S(shot)
    if isinstance(k,(list,tuple)): return tuple(k)
    return tuple(_b[shot][k])
def autocam(boxes):
    x0=min(b[0] for b in boxes); y0=min(b[1] for b in boxes); x1=max(b[0]+b[2] for b in boxes); y1=max(b[1]+b[3] for b in boxes)
    w=max(x1-x0+70,(y1-y0+70)*ZW/ZH,300); w=min(w,PW); h=w*ZH/ZW
    x=(x0+x1)/2-w/2; y=(y0+y1)/2-h/2
    return (min(max(x,0),PW-w), min(max(y,0),PH-h), w)
FULL=(0,PH/2-PW*ZH/ZW/2,PW)
def prep(film):
    prev=None
    for b in film['beats']:
        if b.get('talk'): b['cam']=None; prev=None; continue
        hl=[box(b['shot'],k) for k in b.get('hl',[])]; b['_hl']=hl
        b['_click']=box(b['shot'],b['click']) if b.get('click') else None
        tgt=b.get('cam') or (autocam(hl+([b['_click']] if b['_click'] else [])) if (hl or b['_click']) else FULL)
        pan=None
        if isinstance(tgt,tuple) and isinstance(tgt[0],tuple): pan,tgt=tgt[0],tgt[1]
        if tgt=='top': tgt=(0,0,PW)
        if tgt=='bottom': tgt=(0,PH-PW*ZH/ZW,PW)
        start=prev if (prev and b.get('same',True) and prev[1]==b['shot']) else None
        if pan: c0=pan
        elif start: c0=start[0]
        else:
            h=PW*ZH/ZW; cy=tgt[1]+tgt[2]*ZH/ZW/2; c0=(0,min(max(cy-h/2,0),PH-h),PW)
        b['cam']=(c0,tuple(tgt)); prev=(tuple(tgt), b.get('shot2',b['shot']))
def phone_base(d):
    d.rounded_rectangle((PX-16,PY-16,PX+PW+16,PY+PH+16),58,fill=(6,9,12),outline=(74,88,102),width=3)
_mask=Image.new('L',(PW,PH),0); ImageDraw.Draw(_mask).rounded_rectangle((0,0,PW-1,PH-1),42,fill=255)
_zmask=Image.new('L',(ZW,ZH),0); ImageDraw.Draw(_zmask).rounded_rectangle((0,0,ZW-1,ZH-1),26,fill=255)
def headline(d,kicker,cap,a,y=64):
    d.text((ZX,y),kicker,font=font('Bold',26),fill=cmix(BRASS,a))
    for s in (58,52,46,40):
        f=font('Bold',s)
        if d.textlength(cap,font=f)<=ZW: break
    d.text((ZX,y+44),cap,font=f,fill=cmix(INK,a))
def wrap(d,text,f,maxw):
    out=[]; cur=''
    for w in text.split():
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: out.append(cur); cur=w
    if cur: out.append(cur)
    return out
def card(film,kicker,title,sub,a=1.0,brand=True):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,330,176,386),12,fill=cmix(BRASS,a)); d.text((137,337),'J',font=font('Bold',35),fill=cmix((26,20,8),a,BRASS))
    d.text((196,340),'JSH Training Academy  ·  MyRealtyVault  ·  '+PATH,font=font('SemiBold',30),fill=cmix(SOFT,a))
    d.text((120,440),kicker.upper(),font=font('Bold',34),fill=cmix(BRASS,a))
    f=font('Bold',92 if d.textlength(title,font=font('Bold',92))<W-240 else 72 if d.textlength(title,font=font('Bold',72))<W-240 else 58); d.text((120,500),title,font=f,fill=cmix(INK,a))
    if sub:
        for i,l in enumerate(wrap(d,sub,font('Medium',40),W-260)): d.text((120,640+i*54),l,font=font('Medium',40),fill=cmix(SOFT,a))
    return im
def pad(dur,SR=48000,gain=0.05):
    t=np.arange(int(dur*SR))/SR; out=np.zeros(len(t)); chords=[(220,277.2,329.6),(196,246.9,293.7),(174.6,220,261.6),(196,246.9,329.6)]
    for i in range(int(dur/4)+1):
        s=int(i*4*SR); seg=t[s:s+int(4.6*SR)]-i*4
        if len(seg)==0: break
        env=np.minimum(seg/1.2,1)*np.minimum((4.6-seg)/1.2,1); v=sum(np.sin(2*np.pi*f*seg)+0.4*np.sin(2*np.pi*2*f*seg) for f in chords[i%4])
        out[s:s+len(seg)]+=v*env
    out*=np.minimum(t/1.5,1)*np.minimum((dur-t)/2.5,1); return out/abs(out).max()*gain
def build(fid, stills=False):
    L=FILMS[fid]; beats=L['beats']; kind=L.get('kind','lesson'); prep(L)
    meta_p=f'vo/{fid}.json'; texts=[b['vo'] for b in beats]
    if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=texts:
        global KO
        if 'KO' not in globals():
            from kokoro_onnx import Kokoro
            KO=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin')
        durs=[]
        for i,b in enumerate(beats):
            a,sr=KO.create(b['vo'],voice='af_heart',speed=1.02,lang='en-us'); sf.write(f'vo/{fid}_{i}.wav',a,sr); durs.append(len(a)/sr)
        json.dump({'texts':texts,'durs':durs},open(meta_p,'w'))
    durs=json.load(open(meta_p))['durs']; INTRO,GAP,OUTRO=(2.6,0.6,3.2) if kind=='lesson' else (3.0,0.7,4.2); t=INTRO
    for b,dd in zip(beats,durs): b['s']=t; b['e']=t+dd+GAP; t=b['e']
    DUR=t+OUTRO; nb=len(beats)
    conf=[(random.Random(i).random(),random.Random(i+99).random(),random.Random(i+7).random(),i) for i in range(150)]
    def scene(i,t):
        b=beats[i]; p=(t-b['s'])/(b['e']-b['s']); im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); phone_base(d)
        hi,lo=S(b['shot']); c_at=0.50 if b.get('shot2') else 0.74; q=0
        if b.get('shot2'):
            q=ease((p-c_at-0.04)/0.05)
            if q>0: hi2,lo2=S(b['shot2']); lo=Image.blend(lo,lo2,q)
        if b.get('talk'):
            # slow drift on the phone, bullets on the right
            im.paste(lo,(PX,PY),_mask); ca=min(ease(p/0.08),1-ease((p-0.96)/0.04))
            pts=b.get('pts',[]); capl=wrap(d,b['cap'],font('Bold',86),ZW-40)
            tot=54+102*len(capl)+34+sum(66*len(wrap(d,pt,font('Medium',50),ZW-110))+22 for pt in pts); y=max(120,(H-tot)//2-20)
            d.text((ZX+30,y),b.get('kicker',L['module']).upper(),font=font('Bold',34),fill=cmix(BRASS,ca)); y+=62
            for l in capl: d.text((ZX+30,y),l,font=font('Bold',86),fill=cmix(INK,ca)); y+=102
            y+=34
            for j,pt in enumerate(pts):
                a=ca*eout((p-0.12-j*(0.5/max(len(pts),1)))/0.12)
                if a>0:
                    d.ellipse((ZX+34,y+24,ZX+50,y+40),fill=cmix(BRASS,a))
                for l in wrap(d,pt,font('Medium',50),ZW-110):
                    if a>0: d.text((ZX+76,y),l,font=font('Medium',50),fill=cmix(SOFT if j else INK,a))
                    y+=66
                y+=22
            if b.get('confetti'):
                for rx,ry,rc,k in conf:
                    yy=(ry*1.3-0.3+p*0.9)*H; xx=rx*W+math.sin(p*9+k)*26; col=[BRASS,BLUE,(232,237,241),(120,200,150)][k%4]
                    d.rectangle((xx,yy,xx+12,yy+20),fill=col)
            return im
        c0,c1=b['cam']; k=ease((p-0.05)/0.5); cx,cy,cw=(c0[j]+(c1[j]-c0[j])*k for j in range(3)); ch=cw*ZH/ZW; cx=min(max(cx,0),PW-cw); cy=min(max(cy,0),PH-ch-0.01); sc=hi.width/PW
        z=hi.resize((ZW,ZH),Image.BICUBIC,box=(cx*sc,cy*sc,(cx+cw)*sc,(cy+ch)*sc))
        if q>0: z=Image.blend(z,hi2.resize((ZW,ZH),Image.BICUBIC,box=(cx*sc,cy*sc,(cx+cw)*sc,(cy+ch)*sc)),q)
        # phone with the part outside the zoom region dimmed
        dim=Image.blend(lo,Image.new('RGB',lo.size,(10,14,18)),0.38*ease((p-0.02)/0.2)); dim.paste(lo.crop((int(cx),int(cy),int(cx+cw),int(cy+ch))),(int(cx),int(cy)))
        im.paste(dim,(PX,PY),_mask); d.rounded_rectangle((ZX-3,ZY-3,ZX+ZW+3,ZY+ZH+3),28,fill=(8,11,15),outline=(74,88,102),width=3); im.paste(z,(ZX,ZY),_zmask)
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); zs=ZW/cw
        d.rounded_rectangle((PX+cx-2,PY+cy-2,PX+cx+cw+2,PY+cy+ch+2),8,outline=BRASS+(235,),width=3)
        d.line((PX+cx+cw+2,PY+cy,ZX-3,ZY+24),fill=BRASS+(90,),width=2); d.line((PX+cx+cw+2,PY+cy+ch,ZX-3,ZY+ZH-24),fill=BRASS+(90,),width=2)
        ha=ease((p-0.30)/0.14)*(1-ease((p-0.94)/0.06))
        if b.get('shot2'): ha=ease((p-0.14)/0.12)*(1-ease((p-c_at)/0.04))
        if ha>0:
            g=0.5+0.5*math.sin(t*5)
            for x,y,w,h in b['_hl']:
                x0,y0,x1,y1=ZX+(x-4-cx)*zs,ZY+(y-4-cy)*zs,ZX+(x+w+4-cx)*zs,ZY+(y+h+4-cy)*zs
                x0,y0,x1,y1=max(x0,ZX+4),max(y0,ZY+4),min(x1,ZX+ZW-4),min(y1,ZY+ZH-4)
                if x1-x0>12 and y1-y0>12:
                    d.rounded_rectangle((x0,y0,x1,y1),16,outline=BRASS+(int(255*ha),),width=6); d.rounded_rectangle((x0-9,y0-9,x1+9,y1+9),22,outline=BRASS+(int(90*ha*g),),width=4)
                d.rounded_rectangle((PX+x-3,PY+y-3,PX+x+w+3,PY+y+h+3),6,outline=BRASS+(int(255*ha),),width=2)
        if b['_click']:
            bx_,by_,bw_,bh_=b['_click']; X,Y=ZX+(bx_+bw_/2-cx)*zs,ZY+(by_+bh_/2-cy)*zs; cp=(p-c_at)/0.14; ap=ease((p-(c_at-0.26))/0.2); mx,my=X+170*(1-ap),Y+130*(1-ap)
            if p>c_at-0.3 and not (b.get('shot2') and p>c_at+0.22):
                d.ellipse((mx-30,my-30,mx+30,my+30),fill=(255,255,255,70),outline=(255,255,255,235),width=4)
            if 0<=cp<1:
                r=30+60*eout(cp); d.ellipse((X-r,Y-r,X+r,Y+r),outline=(255,255,255,int(230*(1-cp))),width=6)
                r2=8+16*eout(cp); px_,py_=PX+bx_+bw_/2,PY+by_+bh_/2; d.ellipse((px_-r2,py_-r2,px_+r2,py_+r2),outline=BRASS+(int(255*(1-cp)),),width=3)
        im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB'); d=ImageDraw.Draw(im)
        ca=min(ease(p/0.08),1-ease((p-0.95)/0.05)); headline(d,f'STEP {i+1} OF {nb}',b['cap'],ca)
        for j in range(nb): d.ellipse((ZX+j*28,1012,ZX+14+j*28,1026),fill=BRASS if j<=i else (60,72,84))
        d.text((ZX+ZW-d.textlength(L['title'],font=font('Medium',24)),1006),L['title'],font=font('Medium',24),fill=(96,110,124))
        return im
    prev={}
    def frame(t):
        if t<INTRO:
            im=card(L,L['module'],L['title'],L.get('sub',''),ease(t/0.4)); k=ease((t-(INTRO-0.35))/0.35)
            return Image.blend(im,scene(0,beats[0]['s']),k) if k>0 else im
        if t>=DUR-OUTRO:
            o=L.get('outro') or ('Your turn','Now try it in the app','Then take the quick check to complete the lesson.')
            im=card(L,*o); k=ease((t-(DUR-OUTRO))/0.4)
            if k<1:
                if 'end' not in prev: prev['end']=scene(nb-1,beats[-1]['e']-1e-3)
                im=Image.blend(prev['end'],im,k)
            f=ease((t-(DUR-0.5))/0.5); return Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),f) if f>0 else im
        i=max(j for j,b in enumerate(beats) if t>=b['s']); im=scene(i,t)
        if i>0 and t-beats[i]['s']<0.3:
            if i not in prev: prev[i]=scene(i-1,beats[i-1]['e']-1e-3)
            im=Image.blend(prev[i],im,ease((t-beats[i]['s'])/0.3))
        return im
    if stills:
        return [frame(b['s']+(b['e']-b['s'])*(0.42 if b.get('shot2') else 0.86)).resize((640,360)) for b in beats], DUR
    SR=48000; n=int(DUR*SR); mixd=np.zeros(n)
    for i,b in enumerate(beats):
        a,sr=sf.read(f'vo/{fid}_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int(b['s']*SR); a=a[:n-s]; mixd[s:s+len(a)]+=a/(abs(a).max()+1e-9)*0.9
        if b.get('click'):
            ct=b['s']+(b['e']-b['s'])*(0.50 if b.get('shot2') else 0.74); x=np.arange(int(0.03*SR))/SR; c=np.random.randn(len(x))*np.exp(-x*300)*0.3; s=int(ct*SR); mixd[s:s+len(c)]+=c
    x=np.arange(int(1.2*SR))/SR; chm=(np.sin(2*np.pi*660*x)+0.6*np.sin(2*np.pi*990*x))*np.exp(-x*4)*0.12; mixd[int(0.2*SR):int(0.2*SR)+len(chm)]+=chm
    if kind!='lesson': mixd+=pad(DUR,SR,0.06)[:n]
    mixd=mixd/max(1.0,abs(mixd).max())*0.95; sf.write(f'out/{fid}.wav',np.stack([mixd,mixd],1),SR)
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','23','-preset','medium','-pix_fmt','yuv420p',f'out/{fid}.tmp.mp4'],stdin=subprocess.PIPE)
    for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
    ff.stdin.close(); assert ff.wait()==0
    out=f"out/MRV_{PRE}{L['file']}.mp4"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'out/{fid}.tmp.mp4','-i',f'out/{fid}.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],check=True)
    os.remove(f'out/{fid}.tmp.mp4'); os.remove(f'out/{fid}.wav'); print('ok',fid,round(DUR,1),os.path.getsize(out)//1024,'KB',flush=True)
if __name__=='__main__':
    a=sys.argv[1]; ids=list(FILMS) if a=='all' else [k for k,v in FILMS.items() if v.get('kind','lesson')=='lesson'] if a=='lessons' else [k for k,v in FILMS.items() if v.get('kind','lesson')!='lesson'] if a=='intros' else a.split(',')
    if len(sys.argv)>2:
        for fid in ids:
            ims,D=build(fid,True); print(fid,round(D,1),len(ims)); cols=3; sh=Image.new('RGB',(640*cols,360*((len(ims)+cols-1)//cols)),(0,0,0))
            for c,im in enumerate(ims): sh.paste(im,(640*(c%cols),360*(c//cols)))
            sh.save(f'out/sheet_{fid}.jpg',quality=80)
    else:
        for fid in ids: build(fid)
