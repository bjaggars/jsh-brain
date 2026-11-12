"""AWP product overview film (Academy "Start here" + marketing product demo). Real captures of the Demo engagement,
dynamic camera, highlights, pointer, headline captions, Kokoro voice-over, soft music bed.
usage: python3 overview.py [stills]"""
import json, math, os, subprocess, sys
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,30
F='/usr/share/fonts/opentype/inter/InterDisplay-'
def font(w,s): return ImageFont.truetype(F+w+'.otf',s)
def ease(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def eout(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
PAPER,INK,SOFT,BLUE,BRASS=(18,24,30),(232,237,241),(157,170,182),(110,168,232),(217,178,95)
BX=json.load(open('cap/ov_boxes.json')); BX.update({k:v for k,v in json.load(open('cap/boxes.json')).items() if k.startswith('pres.')})
def R(k,pad=10):
    if not isinstance(k,str): return k
    x,y,w,h=BX[k]; pad=5 if h<30 else pad; return (x-pad,y-pad,w+2*pad,h+2*pad)
def ctr(k): x,y,w,h=BX[k]; return (x+w/2,y+h/2)
OUT='AWP_Overview'
BX.update({'qr.q1':[165,160.7,1110,27],'idk.offer':[165,335.7,1110,122],'idk.yes':[165,412.7,135.7,44],'idk.assume':[308.7,411.7,245.4,46],
 't2.present':[144,334.9,135.7,35],'t2.bar':[144,429.9,1152,21],'jr.src':[389,302,77.3,22],'cm.pins':[968,249.8,294,235],'pa.crew':[500,103,133,36]})
BEATS=[
 dict(kind='problem', cap='',
      vo="Building custom software usually starts with workshops. Weeks of meetings. Months of documents. And at the end, a binder and a guess."),
 dict(kind='title', cap='',
      vo="The JSH AI Workshop Platform changes that. It's one of the most advanced on the market. AI-driven, human-led, and it takes you from first conversation to clickable prototype in days."),
 dict(shot='ov_voices', cam=((0,0,1440),(300,168,840)), hl=[(371,400,698,170)], cap='An expert in the client’s industry, from minute one',
      vo="From the first minute, it works like a world-class expert in your client's industry. Create the engagement, and three expert voices are built for that business."),
 dict(shot='ov_apps', cam=((300,130,900),(325,285,720)), hl=['apps.looked'], cap='It researches the tools they use today',
      vo="It even researches the tools the client uses today."),
 dict(shot='q_round', cam=((0,0,1440),(130,90,1180)), hl=[(155,148,1130,258)], cap='No fixed script',
      vo="There's no fixed script. Each round of questions comes from the biggest gaps in what it has learned so far."),
 dict(shot='q_round', cam=((130,90,1180),(150,170,1140)), hl=[(155,410,1130,250)], cap='Every answer sharpens the next question',
      vo="So every answer sharpens the next question."),
 dict(shot='idk_offer', cam=((0,0,1440),(140,150,1160)), hl=[], cap='Don’t know? No problem',
      vo="And when the client doesn't know? No problem."),
 dict(shot='idk_offer', cam=((140,150,1160),(150,200,1140)), hl=['idk.offer'], cap='How others in their field handle it',
      vo="The platform shows how others in their field handle it."),
 dict(shot='idk_offer', cam=((150,200,1140),(150,235,1140)), hl=['idk.yes','idk.assume'], click='idk.yes', cap='Accept it, or assume it for now',
      vo="Accept it, or assume it for now, and keep moving."),
 dict(shot='bp_full', cam=((0,0,1440),(120,60,1200)), hl=[(614,220,212,210),(838,220,212,210),(1063,220,212,210),(165,442,212,229)], cap='Every answer lands in the Blueprint',
      vo="Behind the scenes, every answer lands in the Blueprint: the personas, their day-in-the-life journeys, the data, the screens."),
 dict(shot='jr2', cam=((250,0,940),(350,200,740)), hl=['jr.src'], cap='Every fact has a source',
      vo="Every fact is tagged with where it came from."),
 dict(shot='top2', shot2='present2', cam=((0,0,1440),(60,150,1000)), hl=['t2.present'], click='t2.present', cap='You run the room',
      vo="You stay in charge. You run the room, and Present to client shows them only what they should see."),
 dict(shot='proto_a2', shot2='proto_route2', cam=((0,0,1440),(140,40,1180)), hl=[], click='pa.crew', cap='A clickable prototype',
      vo="Then the Blueprint becomes a clickable prototype."),
 dict(kind='phone', cap='On their own phone. No sign-in.',
      vo="One the client can open on their own phone. No sign-in."),
 dict(shot='cm_saved', cam=((0,0,1440),(150,120,1150)), hl=['cm.pins'], cap='Comment right on the screen',
      vo="They react, and you comment right on the screen."),
 dict(shot='ub2', cam=((0,0,1440),(140,330,1160)), hl=[(160,412,1120,214)], cap='Blueprint and prototype update together',
      vo="The platform updates the Blueprint and the prototype together."),
 dict(shot='versions2', cam=((0,0,1440),(130,60,900)), hl=[(158,114,304,52)], cap='Version after version',
      vo="Version after version, until it's right."),
 dict(shot='readiness2', cam=((0,0,1440),(130,40,1000)), hl=[(160,134,300,44)], cap='A build-readiness check',
      vo="A build-readiness check scores what's left."),
 dict(shot='top2', cam=((0,0,1440),(100,180,1240)), hl=['t2.bar'], cap='The build package goes to the JSH build team',
      vo="Then the build package goes to the JSH build team: the foundation for building, testing, and training."),
 dict(kind='close', cap='',
      vo="Workshops in days, not months. An app in production in a few short months, not a year or more. This is the JSH AI Workshop Platform. Changing how software gets built, one client at a time."),
]
# ---- voice
meta_p='vo/ovf.json'; texts=[b['vo'] for b in BEATS]
if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=texts:
    from kokoro_onnx import Kokoro
    k=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin'); durs=[]
    for i,b in enumerate(BEATS):
        a,sr=k.create(b['vo'],voice='af_heart',speed=1.02,lang='en-us'); sf.write(f'vo/ovf_{i}.wav',a,sr); durs.append(len(a)/sr)
    json.dump({'texts':texts,'durs':durs},open(meta_p,'w'))
durs=json.load(open(meta_p))['durs']
LEAD,GAP,OUTRO=0.5,0.5,2.2
t=LEAD
for b,d in zip(BEATS,durs): b['s']=t; b['e']=t+d+GAP; t=b['e']
DUR=t+OUTRO
shots={}
def S(n):
    if n not in shots: shots[n]=Image.open(f'cap/{n}.jpg' if os.path.exists(f'cap/{n}.jpg') else f'cap/p2/{n}.jpg').convert('RGB')
    return shots[n]
def view(name,cam):
    im=S(name); sc=im.width/1440; x,y,w=cam; h=w*9/16; iw,ih=im.width/sc,im.height/sc
    x=min(max(x,0),iw-w); y=min(max(y,0),max(0,ih-h))
    return im.resize((W,H),Image.LANCZOS,box=(x*sc,y*sc,(x+w)*sc,(y+h)*sc)),(x,y,w)
import random
_docs=[]; _pc={'n':0,'base':None}
def _mkdocs():
    rnd=random.Random(7); titles=['Meeting notes','Requirements v4','Workshop 3 recap','Action items','Scope draft','Follow-up','Open questions','Sign-off (pending)','Requirements v7','Workshop 5 agenda','Change requests','Notes from the call']
    cells=[(c,r) for r in range(4) for c in range(7)]; rnd.shuffle(cells); cells+=[(rnd.uniform(0,6),rnd.uniform(0,3)) for _ in range(22)]
    for j,(c,r) in enumerate(cells):
        w,h=rnd.randint(300,360),rnd.randint(390,460); pg=Image.new('RGBA',(w+24,h+24),(0,0,0,0)); d=ImageDraw.Draw(pg)
        d.rounded_rectangle((14,16,w+22,h+22),6,fill=(0,0,0,70))
        tone=rnd.choice([(244,246,248),(236,239,242),(250,250,247),(229,234,239)]); d.rounded_rectangle((4,4,w+4,h+4),6,fill=tone+(255,),outline=(170,178,188,255),width=2)
        d.text((28,26),titles[j%len(titles)],font=font('Bold',21),fill=(40,52,64,255)); d.rectangle((28,60,w-20,62),fill=(150,160,172,255))
        y=80; k=rnd.randint(0,2)
        while y<h-30:
            if k==1 and 150<y<260:
                for q in range(3): d.rectangle((28,y+q*30,w-20,y+q*30+22),outline=(150,160,172,255),width=2); d.line((28+(w-48)//3,y+q*30,28+(w-48)//3,y+q*30+22),fill=(150,160,172,255),width=2)
                y+=100; continue
            if k==2 and y<200: d.rectangle((28,y,40,y+12),outline=(110,122,136,255),width=2); d.rectangle((50,y+3,rnd.randint(150,w-30),y+9),fill=(128,140,154,255)); y+=24; continue
            d.rectangle((28,y,rnd.randint(int(w*0.45),w-22),y+6),fill=(138,150,164,255)); y+=17 if rnd.random()>0.12 else 34
        pg=pg.rotate(rnd.uniform(-11,11),expand=True,resample=Image.BICUBIC)
        x=int(-70+c*(W+140-330)/6+rnd.uniform(-45,45)); yy=int(-60+r*(H+120-400)/3+rnd.uniform(-40,40))
        _docs.append((pg,x,yy,0.02+0.80*j/len(cells)))
def problem(p):
    if not _docs: _mkdocs()
    landed=[k for k,dc in enumerate(_docs) if p>=dc[3]+0.07]
    if _pc['base'] is None or len(landed)<_pc['n']: _pc['base']=Image.new('RGB',(W,H),PAPER); _pc['n']=0
    for k in landed[_pc['n']:]:
        pg,x,y,_=_docs[k]; _pc['base'].paste(pg,(x,y),pg)
    _pc['n']=len(landed); im=_pc['base'].copy()
    for pg,x,y,at in _docs:
        q=(p-at)/0.07
        if 0<q<1:
            e=eout(q); sc=1.35-0.35*e; g=pg.resize((int(pg.width*sc),int(pg.height*sc)),Image.BILINEAR)
            al=g.getchannel('A').point(lambda v,e=e:int(v*e)); im.paste(g,(x-(g.width-pg.width)//2,y-(g.height-pg.height)//2-int(30*(1-e))),al)
    k=ease((p-0.92)/0.08)
    if k>0: im=Image.blend(im,Image.new('RGB',(W,H),PAPER),k*0.9)
    return im
def title(p):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im,'RGBA')
    a=ease(p/0.10); d.rounded_rectangle((120,330,184,394),14,fill=BRASS+(int(255*a),)); d.text((140,338),'J',font=font('Bold',40),fill=(26,20,8,int(255*a)))
    d.text((210,342),'JSH Innovations',font=font('SemiBold',34),fill=SOFT+(int(255*a),))
    d.text((120,430),'JSH AI Workshop Platform',font=font('Bold',104),fill=INK+(int(255*a),))
    for j,(tx,at) in enumerate([('AI-driven.',0.42),('Human-led.',0.52)]):
        b=ease((p-at)/0.07); d.text((120+j*330,580),tx,font=font('SemiBold',56),fill=BLUE+(int(255*b),))
    b=ease((p-0.66)/0.08); d.text((120,680),'First conversation to clickable prototype, in days.',font=font('Medium',40),fill=SOFT+(int(255*b),))
    return im
_ph={}
def phone(p):
    im=Image.new('RGB',(W,H),PAPER)
    for j,n in enumerate(['ph_who','ph_route','ph_stop']):
        if n not in _ph:
            src=Image.open(f'cap/p2/{n}.jpg').convert('RGB').resize((398,862),Image.LANCZOS); m=Image.new('L',(398,862),0); ImageDraw.Draw(m).rounded_rectangle((0,0,397,861),34,fill=255); _ph[n]=(src,m)
        a=eout((p-0.04-j*0.13)/0.22)
        if a<=0: continue
        x=304+j*458; y=int(70+70*(1-a)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((x-12,y-12,x+410,y+874),44,fill=(8,11,15),outline=(70,84,98),width=3)
        src,m=_ph[n]; lay=Image.blend(Image.new('RGB',src.size,PAPER),src,a); im.paste(lay,(x,y),m)
    return im
def close(p):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im,'RGBA')
    a=ease(p/0.06); d.rounded_rectangle((120,300,184,364),14,fill=BRASS+(int(255*a),)); d.text((140,308),'J',font=font('Bold',40),fill=(26,20,8,int(255*a)))
    d.text((210,312),'JSH Innovations',font=font('SemiBold',34),fill=SOFT+(int(255*a),))
    b1=ease((p-0.02)/0.08); d.text((120,400),'Workshops in days, not months.',font=font('Bold',84),fill=INK+(int(255*b1),))
    b2=ease((p-0.24)/0.08); d.text((120,520),'In production in months, not a year or more.',font=font('SemiBold',54),fill=BLUE+(int(255*b2),))
    b3=ease((p-0.52)/0.08); d.text((120,650),'JSH AI Workshop Platform',font=font('Bold',50),fill=INK+(int(255*b3),))
    b4=ease((p-0.70)/0.08); d.text((120,724),'Changing how software gets built, one client at a time.',font=font('Medium',40),fill=BRASS+(int(255*b4),))
    return im
def endcard(a=1.0): return close(1.0)
def scene(i,t):
    b=BEATS[i]; p=(t-b['s'])/(b['e']-b['s'])
    if b.get('kind')=='problem': return problem(p)
    if b.get('kind')=='title': return title(p)
    if b.get('kind')=='close': return close(p)
    if b.get('kind')=='phone':
        im=phone(p); ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); ca=min(ease(p/0.08),1-ease((p-0.95)/0.05)); f=font('SemiBold',42); tw=d.textlength(b['cap'],font=f)
        d.rounded_rectangle((W/2-tw/2-36,H-132,W/2+tw/2+36,H-52),40,fill=(11,16,21,int(240*ca)),outline=BRASS+(int(150*ca),),width=2); d.text((W/2-tw/2,H-117),b['cap'],font=f,fill=INK+(int(255*ca),))
        return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    c0,c1=b['cam']; k=ease((p-0.06)/0.62); cam=tuple(c0[j]+(c1[j]-c0[j])*k for j in range(3))
    im,(cx,cy,cw)=view(b['shot'],cam)
    if b.get('shot2'):
        q=ease((p-0.50)/0.05)
        if q>0: im2,_=view(b['shot2'],cam); im=Image.blend(im,im2,q)
    sc=W/cw; ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ha=ease((p-0.30)/0.15)*(1-ease((p-0.93)/0.07))
    if b.get('shot2'): ha=ease((p-0.12)/0.12)*(1-ease((p-0.46)/0.04))
    if ha>0:
        for key in b.get('hl',[]):
            x,y,w,h=R(key); x0,y0,x1,y1=(x-cx)*sc,(y-cy)*sc,(x+w-cx)*sc,(y+h-cy)*sc; g=0.5+0.5*math.sin(t*5)
            d.rounded_rectangle((x0,y0,x1,y1),14,outline=BRASS+(int(255*ha),),width=5)
            d.rounded_rectangle((x0-9,y0-9,x1+9,y1+9),20,outline=BRASS+(int(90*ha*g),),width=4)
    if b.get('click'):
        c_at=0.46 if b.get('shot2') else 0.74
        px,py=ctr(b['click']); X,Y=(px-cx)*sc,(py-cy)*sc; cp=(p-c_at)/0.14; ap=ease((p-(c_at-0.26))/0.2)
        mx,my=X+150*(1-ap),Y+120*(1-ap)
        if p>c_at-0.3 and not (b.get('shot2') and p>c_at+0.2):
            d.polygon([(mx,my),(mx,my+34),(mx+9,my+26),(mx+16,my+40),(mx+22,my+37),(mx+15,my+24),(mx+26,my+24)],fill=(255,255,255,255),outline=(20,20,20,255))
        if 0<=cp<1: r=14+46*eout(cp); d.ellipse((X-r,Y-r,X+r,Y+r),outline=(255,255,255,int(230*(1-cp))),width=5)
    if b['cap']:
        ca=min(ease(p/0.08),1-ease((p-0.95)/0.05)); f=font('SemiBold',42); tw=d.textlength(b['cap'],font=f)
        d.rounded_rectangle((W/2-tw/2-36,H-132,W/2+tw/2+36,H-52),40,fill=(11,16,21,int(232*ca)),outline=BRASS+(int(150*ca),),width=2)
        d.text((W/2-tw/2,H-117),b['cap'],font=f,fill=INK+(int(255*ca),))
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
def last_frame(i):
    b=BEATS[i]; return scene(i,b['e']-1e-3)
_prev={}
def frame(t):
    if t<BEATS[0]['s']: return Image.blend(Image.new('RGB',(W,H),(0,0,0)),problem(0),ease(t/LEAD))
    if t>=DUR-OUTRO:
        k=ease((t-(DUR-OUTRO))/0.4); im=endcard()
        if k<1:
            if 'end' not in _prev: _prev['end']=last_frame(len(BEATS)-1)
            im=Image.blend(_prev['end'],im,k)
        f=ease((t-(DUR-0.5))/0.5)
        return Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),f) if f>0 else im
    i=max(j for j,b in enumerate(BEATS) if t>=b['s']); im=scene(i,t)
    if i>0 and t-BEATS[i]['s']<0.3:                 # dissolve between scenes
        if i not in _prev: _prev[i]=last_frame(i-1)
        im=Image.blend(_prev[i],im,ease((t-BEATS[i]['s'])/0.3))
    return im
if len(sys.argv)>1:
    ts=[BEATS[0]['s']+(BEATS[0]['e']-BEATS[0]['s'])*f for f in (0.15,0.45,0.75,0.9)]+[BEATS[1]['s']+0.1, BEATS[-1]['s']+1, BEATS[-1]['e']-0.3, DUR-0.9]
    ims=[frame(x).resize((640,360)) for x in ts]; n=len(ims); sh=Image.new('RGB',(640*4,360*math.ceil(n/4)))
    [sh.paste(im,(640*(k%4),360*(k//4))) for k,im in enumerate(ims)]; sh.save('shots/ov_sheet.jpg',quality=85); print(round(DUR,2)); sys.exit()
# ---- audio: VO + soft pad (ducked) + clicks
SR=48000; n=int(DUR*SR); vo=np.zeros(n); sfx=np.zeros(n)
for i,b in enumerate(BEATS):
    a,sr=sf.read(f'vo/ovf_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int(b['s']*SR); a=a[:n-s]; vo[s:s+len(a)]+=a/(abs(a).max()+1e-9)*0.9
    if b.get('click'):
        ct=b['s']+(b['e']-b['s'])*(0.46 if b.get('shot2') else 0.74); x=np.arange(int(0.03*SR))/SR; c=np.random.randn(len(x))*np.exp(-x*300)*0.3; s=int(ct*SR); sfx[s:s+len(c)]+=c
def nf(m): return 440*2**((m-69)/12)
tt=np.arange(n)/SR; pad=np.zeros(n); bar=4.0
minor=[[45,57,60,64],[41,53,57,60]]; major=[[48,55,60,64],[43,55,59,62],[45,57,60,64],[41,53,57,60]]
turn=BEATS[1]['s']; k=0; t0=0.0
while t0<DUR:
    ch=minor[k%2] if t0+bar/2<turn else major[k%4]; s=int(t0*SR); L=min(int((bar+1.2)*SR),n-s); x=np.arange(L)/SR
    env=np.minimum(x/1.2,1)*np.minimum((bar+1.2-x)/1.2,1); env=np.clip(env,0,1)
    sig=sum(np.sin(2*np.pi*nf(m)*x)+0.35*np.sin(2*np.pi*nf(m)*2*x+0.5)+0.5*np.sin(2*np.pi*nf(m)*1.003*x) for m in ch)/len(ch)
    pad[s:s+L]+=sig*env*0.16; t0+=bar; k+=1
env_vo=np.abs(vo); w=int(0.25*SR); env_vo=np.convolve(env_vo,np.ones(w)/w,'same'); duck=1-0.55*np.clip(env_vo/0.08,0,1)
pad*=duck; pad[:int(0.6*SR)]*=np.linspace(0,1,int(0.6*SR)); pad[-int(1.5*SR):]*=np.linspace(1,0,int(1.5*SR))
mix=vo+pad+sfx; mix=mix/max(1.0,abs(mix).max())*0.95
sf.write('out/ov.wav',np.stack([mix,mix],1),SR)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p','out/ov.tmp.mp4'],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); assert ff.wait()==0
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','out/ov.tmp.mp4','-i','out/ov.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',f'out/{OUT}.mp4'],check=True)
os.remove('out/ov.tmp.mp4'); print('ok',round(DUR,2))
