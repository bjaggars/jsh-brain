"""JSH Training Academy overview film, for investors and new joiners. Screens are the Academy prototype; the lesson clip is a real AWP lesson.
usage: python3 academy_film.py [stills]"""
import json, math, os, subprocess, sys, glob
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
BX=json.load(open('cap/ac/boxes.json'))
BEATS=[
 dict(kind='card', lines=[('Great software fails for one reason.',INK,'Bold',92,0.0),('People don’t use it.',BRASS,'Bold',92,0.55)],
      vo="Great software fails for one simple reason. People don't use it."),
 dict(kind='card', lines=[('Adoption is the #1 risk in product development.',INK,'Bold',70,0.0),('Many products in our markets ship with little or no training.',SOFT,'SemiBold',50,0.5)],
      vo="We believe user adoption is the number one risk in product development. And many products in our markets ship with little or no training."),
 dict(kind='title', vo="So we built the JSH Training Academy. Training, built into every product we ship."),
 dict(shot='home_campus', cam=((0,0,1440),(230,150,1160)), hl=['hc.campus'], cap='A campus for every product',
      vo="Every JSH product gets its own campus. One Academy, one look, one way of learning."),
 dict(shot='path', cam=((0,0,1440),(230,60,1160)), hl=['path.start'], cap='Start with the big picture',
      vo="Each campus opens with a two-minute overview of the whole product."),
 dict(shot='path_mods', cam=((230,60,1160),(230,110,1160)), hl=[], cap='Short modules, in the order people work',
      vo="Then short modules, in the order people actually do the work."),
 dict(kind='clip', cap='One task per lesson, recorded on the real product',
      vo="Every lesson teaches one task, in under a minute, recorded on the real product. Real screens. A guiding camera. One consistent voice."),
 dict(shot='practice', cam=((0,0,1440),(250,60,1120)), hl=['pr.steps'], cap='Practice, right beside the steps',
      vo="Then they practice, right beside the steps. Each step ticks off as they do it."),
 dict(shot='quiz', cam=((0,0,1440),(430,150,950)), hl=['qz.quiz'], cap='A quick check, then certification',
      vo="A quick check completes the lesson. Finish the path, and you're certified."),
 dict(shot='inapp', cam=((0,0,1440),(230,150,1160)), hl=['ia.screen'], cap='Inside the product, one click away',
      vo="It lives inside the product. Help for the screen you're on is one click away, with no second sign-in."),
 dict(shot='agent', cam=((0,0,1440),(230,0,1100)), hl=[], cap='No second sign-in, and only their campus',
      vo="Customers come in through the product they already use, and see only their own campus."),
 dict(shot='team', cam=((0,0,1440),(250,170,1100)), hl=['tm.doors'], cap='Self-study, or instructor-led',
      vo="Customers learn on their own, at their own pace. Where it fits, like MyRealtyVault, they can also run instructor-led classes."),
 dict(shot='team_classes', cam=((0,0,1440),(250,300,1100)), hl=['tc.health'], cap='Lessons stay current with every release',
      vo="And it stays current. When a release changes a screen, the lessons that touch it are flagged, and re-recorded from their scripts."),
 dict(kind='card', lines=[('Lessons come from scripts, not film crews.',INK,'Bold',76,0.0),('A new campus takes days, not months.',BRASS,'Bold',76,0.5)],
      vo="Because every lesson is produced from a script, not a film crew, a new campus takes days, not months."),
 dict(kind='card', lines=[('Faster onboarding.',INK,'Bold',92,0.18),('Fewer support calls.',INK,'Bold',92,0.45),('Customers who stay.',BRASS,'Bold',92,0.70)],
      vo="The goal is simple. Faster onboarding, fewer support calls, and customers who stay."),
 dict(kind='card', lines=[('Most AI-first firms focus on building the product.',SOFT,'SemiBold',58,0.0),('JSH builds the product,',INK,'Bold',92,0.42),('and makes sure people can use it.',BRASS,'Bold',92,0.62)],
      vo="Most AI-first software firms focus on building the product. JSH builds the product, and makes sure people can use it."),
 dict(kind='close', vo="The JSH Training Academy. Because software only works when people use it."),
]
meta_p='vo/acf.json'; texts=[b['vo'] for b in BEATS]
if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=texts:
    from kokoro_onnx import Kokoro
    k=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin'); durs=[]
    for i,b in enumerate(BEATS):
        a,sr=k.create(b['vo'],voice='af_heart',speed=1.02,lang='en-us'); sf.write(f'vo/acf_{i}.wav',a,sr); durs.append(len(a)/sr)
    json.dump({'texts':texts,'durs':durs},open(meta_p,'w'))
durs=json.load(open(meta_p))['durs']; LEAD,OUTRO=0.5,2.4; t=LEAD
for b,d in zip(BEATS,durs): b['s']=t; b['e']=t+d+(0.9 if b.get('kind') in('card','title','close') else 0.5); t=b['e']
DUR=t+OUTRO
shots={}
def S(n):
    if n not in shots: shots[n]=Image.open(f'cap/ac/{n}.jpg').convert('RGB')
    return shots[n]
def view(name,cam):
    im=S(name); sc=im.width/1440; x,y,w=cam; h=w*9/16; iw,ih=im.width/sc,im.height/sc
    x=min(max(x,0),iw-w); y=min(max(y,0),max(0,ih-h)); return im.resize((W,H),Image.LANCZOS,box=(x*sc,y*sc,(x+w)*sc,(y+h)*sc)),(x,y,w)
def brand(d,a,y=150):
    d.rounded_rectangle((120,y,176,y+56),12,fill=cmix(BRASS,a)); d.text((137,y+7),'J',font=font('Bold',35),fill=cmix((26,20,8),a,BRASS)); d.text((196,y+10),'JSH Innovations',font=font('SemiBold',30),fill=cmix(SOFT,a))
def card(b,tt):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); dur=b['e']-b['s']; n=len(b['lines']); total=sum(sz*1.35 for _,_,_,sz,_ in b['lines']); y=H/2-total/2
    for tx,col,wt,sz,at in b['lines']:
        a=ease((tt-at*dur)/0.45); f=font(wt,sz)
        while d.textlength(tx,font=f)>W-240: sz-=4; f=font(wt,sz)
        d.text((120,y+16*(1-a)),tx,font=f,fill=cmix(col,a)); y+=sz*1.35
    return im
def title(tt):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); a=ease(tt/0.5); brand(d,a,330)
    d.text((120,430),'JSH Training Academy',font=font('Bold',120),fill=cmix(INK,ease((tt-1.2)/0.5)))
    d.text((120,600),'Training, built into every product we ship.',font=font('SemiBold',52),fill=cmix(BLUE,ease((tt-3.4)/0.5)))
    return im
def close(tt):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); brand(d,ease(tt/0.4),330)
    d.text((120,430),'JSH Training Academy',font=font('Bold',120),fill=cmix(INK,ease(tt/0.5)))
    d.text((120,600),'Because software only works when people use it.',font=font('SemiBold',56),fill=cmix(BRASS,ease((tt-1.9)/0.5)))
    return im
CLIP='out/AWP_Lesson_Ask_the_next_questions.mp4'; CW,CH=1500,844
if not glob.glob('clipf/*.jpg'):
    os.makedirs('clipf',exist_ok=True); subprocess.run(['ffmpeg','-y','-loglevel','error','-ss','10.5','-t','14','-i',CLIP,'-vf',f'fps=30,scale={CW}:{CH}','-q:v','3','clipf/%04d.jpg'],check=True)
NCLIP=len(glob.glob('clipf/*.jpg'))
def caption(im,cap,p):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); ca=min(ease(p/0.08),1-ease((p-0.95)/0.05)); f=font('SemiBold',42); tw=d.textlength(cap,font=f)
    d.rounded_rectangle((W/2-tw/2-36,H-132,W/2+tw/2+36,H-52),40,fill=(11,16,21,int(240*ca)),outline=BRASS+(int(150*ca),),width=2); d.text((W/2-tw/2,H-117),cap,font=f,fill=INK+(int(255*ca),))
    return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
def scene(i,t):
    b=BEATS[i]; tt=t-b['s']; p=tt/(b['e']-b['s']); k=b.get('kind')
    if k=='card': return card(b,tt)
    if k=='title': return title(tt)
    if k=='close': return close(tt)
    if k=='clip':
        im=Image.new('RGB',(W,H),(10,14,18)); fr=Image.open('clipf/%04d.jpg'%(min(NCLIP,int(tt*30)+1))); x0=(W-CW)//2; y0=40
        d=ImageDraw.Draw(im); d.rounded_rectangle((x0-6,y0-6,x0+CW+6,y0+CH+6),18,fill=(47,59,71)); m=Image.new('L',(CW,CH),0); ImageDraw.Draw(m).rounded_rectangle((0,0,CW-1,CH-1),14,fill=255); im.paste(fr,(x0,y0),m)
        return caption(im,b['cap'],p)
    c0,c1=b['cam']; kk=ease((p-0.05)/0.7); cam=tuple(c0[j]+(c1[j]-c0[j])*kk for j in range(3)); im,(cx,cy,cw)=view(b['shot'],cam); sc=W/cw
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); ha=ease((p-0.3)/0.15)*(1-ease((p-0.93)/0.07))
    if ha>0:
        for key in b.get('hl',[]):
            x,y,w,h=BX[key]; x0,y0,x1,y1=(x-8-cx)*sc,(y-8-cy)*sc,(x+w+8-cx)*sc,(y+h+8-cy)*sc; g=0.5+0.5*math.sin(t*5)
            d.rounded_rectangle((x0,y0,x1,y1),18,outline=BRASS+(int(255*ha),),width=5); d.rounded_rectangle((x0-9,y0-9,x1+9,y1+9),24,outline=BRASS+(int(90*ha*g),),width=4)
    return caption(Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB'),b['cap'],p)
prev={}
def frame(t):
    if t<BEATS[0]['s']: return Image.new('RGB',(W,H),PAPER)
    if t>=BEATS[-1]['e']:
        im=close(t-BEATS[-1]['s']); f=ease((t-(DUR-0.6))/0.6); return Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),f) if f>0 else im
    i=max(j for j,b in enumerate(BEATS) if t>=b['s']); im=scene(i,t)
    if i>0 and t-BEATS[i]['s']<0.3:
        if i not in prev: prev[i]=scene(i-1,BEATS[i-1]['e']-1e-3)
        im=Image.blend(prev[i],im,ease((t-BEATS[i]['s'])/0.3))
    return im
if len(sys.argv)>1:
    ts=[b['s']+(b['e']-b['s'])*0.85 for b in BEATS]; sh=Image.new('RGB',(480*5,270*4))
    [sh.paste(frame(x).resize((480,270)),(480*(k%5),270*(k//5))) for k,x in enumerate(ts)]; sh.save('shots/acf_sheet.jpg',quality=84); print(round(DUR,1)); sys.exit()
SR=48000; n=int(DUR*SR); vo=np.zeros(n)
for i,b in enumerate(BEATS):
    a,sr=sf.read(f'vo/acf_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int((b['s']+(0.3 if b.get('kind') in('card','title','close') else 0))*SR); a=a[:n-s]; vo[s:s+len(a)]+=a/(abs(a).max()+1e-9)*0.9
def nf(m): return 440*2**((m-69)/12)
pad=np.zeros(n); bar=4.0; minor=[[45,57,60,64],[41,53,57,60]]; major=[[48,55,60,64],[43,55,59,62],[45,57,60,64],[41,53,57,60]]; turn=BEATS[2]['s']; k=0; t0=0.0
while t0<DUR:
    ch=minor[k%2] if t0+bar/2<turn else major[k%4]; s=int(t0*SR); L=min(int((bar+1.2)*SR),n-s); x=np.arange(L)/SR; env=np.clip(np.minimum(x/1.2,1)*np.minimum((bar+1.2-x)/1.2,1),0,1)
    sig=sum(np.sin(2*np.pi*nf(m)*x)+0.35*np.sin(2*np.pi*nf(m)*2*x+0.5)+0.5*np.sin(2*np.pi*nf(m)*1.003*x) for m in ch)/len(ch); pad[s:s+L]+=sig*env*0.16; t0+=bar; k+=1
ev=np.abs(vo); w=int(0.25*SR); ev=np.convolve(ev,np.ones(w)/w,'same'); pad*=1-0.55*np.clip(ev/0.08,0,1); pad[:int(0.6*SR)]*=np.linspace(0,1,int(0.6*SR)); pad[-int(1.5*SR):]*=np.linspace(1,0,int(1.5*SR))
mixd=vo+pad; mixd=mixd/max(1.0,abs(mixd).max())*0.95; sf.write('out/acf.wav',np.stack([mixd,mixd],1),SR)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','22','-preset','medium','-pix_fmt','yuv420p','out/acf.tmp.mp4'],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); assert ff.wait()==0
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','out/acf.tmp.mp4','-i','out/acf.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart','out/JSH_Academy_Overview.mp4'],check=True)
os.remove('out/acf.tmp.mp4'); print('ok',round(DUR,2),os.path.getsize('out/JSH_Academy_Overview.mp4')//1024,'KB')
