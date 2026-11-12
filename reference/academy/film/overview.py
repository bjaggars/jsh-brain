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
OUT='AWP_Overview_Part1'
BEATS=[
 dict(kind='problem', cap='',
      vo="Building custom software usually starts with workshops. Weeks of meetings. Months of documents. And at the end, a binder and a guess."),
 dict(kind='title', cap='',
      vo="The JSH AI Workshop Platform changes that. It's one of the most advanced on the market. AI-driven, human-led, and it takes you from first conversation to clickable prototype in days."),
 dict(shot='ov_voices', cam=((0,0,1440),(300,168,840)), hl=[(371,400,698,170)], cap='An expert in the client’s industry, from minute one',
      vo="From the first minute, it works like a world-class expert in your client's industry. Create the engagement, and three expert voices are built for that business."),
 dict(shot='ov_apps', cam=((300,130,900),(325,285,720)), hl=['apps.looked'], cap='It researches the tools they use today',
      vo="It even researches the tools the client uses today."),
 dict(shot='ov_questions', cam=((130,75,1180),(320,290,770)), hl=[(371,622,698,66)], cap='No fixed script',
      vo="There's no fixed script. Each round of questions comes from the biggest gaps in what it has learned so far."),
 dict(shot='ov_q', cam=((0,0,1440),(130,250,1180)), hl=['q.card'], cap='Every answer sharpens the next question',
      vo="So every answer sharpens the next question."),
 dict(shot='ov_q', cam=((130,250,1180),(150,330,760)), hl=[], click='q.idk', cap='Don’t know? No problem',
      vo="And when the client doesn't know? No problem."),
 dict(shot='ov_recs', cam=((300,140,880),(340,330,740)), hl=['recs.practice'], cap='How others in their field handle it',
      vo="The platform shows how others in their field handle it."),
 dict(shot='ov_assume', cam=((320,170,820),(350,330,700)), hl=['assume.src'], cap='Accept it, or assume it for now',
      vo="Accept it, or assume it for now, and keep moving."),
 dict(shot='eng', cam=((0,120,1440),(110,470,1220)), hl=['top.personas','top.journeys','top.data','top.screens'], cap='Every answer lands in the Blueprint',
      vo="Behind the scenes, every answer lands in the Blueprint: the personas, their day-in-the-life journeys, the data, the screens."),
 dict(shot='ov_bc', cam=((300,200,860),(345,345,620)), hl=['bc.src'], cap='Every fact has a source',
      vo="Every fact is tagged with where it came from."),
 dict(shot='ov_top', shot2='ov_present', cam=((0,0,1440),(60,150,1000)), hl=['top.present'], click='top.present', cap='You run the room',
      vo="You stay in charge. You run the room, and Present to client shows them only what they should see."),
]
# ---- voice
meta_p='vo/ov.json'; texts=[b['vo'] for b in BEATS]
if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=texts:
    from kokoro_onnx import Kokoro
    k=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin'); durs=[]
    for i,b in enumerate(BEATS):
        a,sr=k.create(b['vo'],voice='af_heart',speed=1.02,lang='en-us'); sf.write(f'vo/ov_{i}.wav',a,sr); durs.append(len(a)/sr)
    json.dump({'texts':texts,'durs':durs},open(meta_p,'w'))
durs=json.load(open(meta_p))['durs']
LEAD,GAP,OUTRO=0.5,0.5,3.4
t=LEAD
for b,d in zip(BEATS,durs): b['s']=t; b['e']=t+d+GAP; t=b['e']
DUR=t+OUTRO
shots={}
def S(n):
    if n not in shots: shots[n]=Image.open(f'cap/{n}.jpg').convert('RGB')
    return shots[n]
def view(name,cam):
    im=S(name); sc=im.width/1440; x,y,w=cam; h=w*9/16; iw,ih=im.width/sc,im.height/sc
    x=min(max(x,0),iw-w); y=min(max(y,0),max(0,ih-h))
    return im.resize((W,H),Image.LANCZOS,box=(x*sc,y*sc,(x+w)*sc,(y+h)*sc)),(x,y,w)
def problem(p):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im,'RGBA')
    # left: twelve weeks filling up with meetings
    for j in range(12):
        a=ease((p*1.25-j/14)/0.10)
        if a<=0: continue
        cx,cy=250+(j%4)*190,300+(j//4)*170; col=(34,44,54,int(255*a))
        d.rounded_rectangle((cx,cy,cx+160,cy+140),14,fill=col,outline=(58,72,86,int(255*a)),width=2)
        d.rectangle((cx,cy+22,cx+160,cy+26),fill=(58,72,86,int(255*a)))
        d.text((cx+14,cy+2),f'WEEK {j+1}',font=font('SemiBold',15),fill=SOFT+(int(255*a),))
        for m in range(3):
            ma=ease((p*1.25-j/14-0.04*(m+1))/0.08)
            if ma>0: d.rounded_rectangle((cx+14,cy+40+m*30,cx+146-m*26,cy+60+m*30),6,fill=(110,168,232,int(150*ma)))
    # right: the documents pile up
    for j in range(9):
        a=ease((p*1.2-0.28-j/16)/0.10)
        if a<=0: continue
        ox,oy=1230+((j*37)%60)-30,720-j*46-int(40*(1-a))
        d.rounded_rectangle((ox,oy,ox+420,oy+62),8,fill=(226,230,234,int(245*a)),outline=(150,160,170,int(255*a)),width=2)
        for q in range(3): d.rectangle((ox+24,oy+16+q*12,ox+250+((j+q)*53)%130,oy+20+q*12),fill=(120,132,144,int(220*a)))
    k=ease((p-0.90)/0.10)
    if k>0: im=Image.blend(im,Image.new('RGB',(W,H),PAPER),k*0.85)
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
def endcard(a=1.0):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,360,184,424),14,fill=BRASS); d.text((140,368),'J',font=font('Bold',40),fill=(26,20,8))
    d.text((210,372),'JSH AI Workshop Platform',font=font('SemiBold',34),fill=SOFT)
    d.text((120,460),'Next: the prototype',font=font('Bold',92),fill=INK)
    d.text((120,582),'The clickable prototype, the feedback loop, and the build package.',font=font('Medium',40),fill=BLUE)
    d.text((120,660),'Overview, part 1 of 2 (preview)',font=font('Medium',34),fill=SOFT)
    return im
def scene(i,t):
    b=BEATS[i]; p=(t-b['s'])/(b['e']-b['s'])
    if b.get('kind')=='problem': return problem(p)
    if b.get('kind')=='title': return title(p)
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
    ts=[b['s']+(b['e']-b['s'])*f for b in BEATS for f in ((0.55,0.92) if b.get('kind') else (0.2,0.85))]+[DUR-1.5]
    ims=[frame(x).resize((640,360)) for x in ts]; n=len(ims); sh=Image.new('RGB',(640*4,360*math.ceil(n/4)))
    [sh.paste(im,(640*(k%4),360*(k//4))) for k,im in enumerate(ims)]; sh.save('shots/ov_sheet.jpg',quality=85); print(round(DUR,2)); sys.exit()
# ---- audio: VO + soft pad (ducked) + clicks
SR=48000; n=int(DUR*SR); vo=np.zeros(n); sfx=np.zeros(n)
for i,b in enumerate(BEATS):
    a,sr=sf.read(f'vo/ov_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int(b['s']*SR); a=a[:n-s]; vo[s:s+len(a)]+=a/(abs(a).max()+1e-9)*0.9
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
