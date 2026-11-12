"""Academy lesson renderer: real AWP captures, dynamic camera (pan/zoom per beat), highlights, click ripples, captions, voice-over.
usage: python3 lesson.py <lesson_id> [stills]"""
import json, math, os, subprocess, sys
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H,FPS=1920,1080,30
F='/usr/share/fonts/opentype/inter/InterDisplay-'
def font(w,s): return ImageFont.truetype(F+w+'.otf',s)
def ease(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def eout(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
PAPER,INK,SOFT,BLUE,BRASS=(18,24,30),(232,237,241),(157,170,182),(110,168,232),(217,178,95)
BX=json.load(open('cap/boxes.json'))
def bx(k,pad=10): x,y,w,h=BX[k]; return (x-pad,y-pad,w+2*pad,h+2*pad)
def ctr(k): x,y,w,h=BX[k]; return (x+w/2,y+h/2)
# cam = (x, y, width) in css px of the capture; height follows 16:9
LESSONS={
 'new':{'title':'Create a new engagement','module':'Start an engagement','beats':[
   dict(shot='list', cam=((0,0,1440),(130,50,1190)), hl=['list.new'], click='list.new',
        vo="Every workshop starts with an engagement. From All engagements, choose New engagement.", cap='All engagements → New engagement'),
   dict(shot='new0', shot2='new1', cam=((0,150,1440),(60,215,860)), hl=['new.fields','new.industry'],
        vo="Give it a short name, the client, and their industry. That's all the platform needs to think like an expert in their field.", cap='Name, client and industry'),
   dict(shot='new2', cam=((60,215,860),(70,520,860)), hl=['new.pre'],
        vo="Leave the pre-workshop questionnaire ticked to email the client a few questions first. Add their contact, and a line or two of what you heard on the call.", cap='Questionnaire first: add the client contact'),
   dict(shot='new2', cam=((70,520,860),(40,560,1000)), hl=['new.pre'],
        vo="Or untick it to go straight to a live workshop.", cap='Untick it for a live workshop'),
   dict(shot='new2', shot2='new3', cam=((40,560,1000),(40,700,780)), hl=['new.create'], click='new.create',
        vo="Then choose Create engagement. In about eight seconds, three expert voices are built.", cap='Create engagement'),
   dict(shot='eng', cam=((0,130,1440),(110,150,1220)), hl=[],
        vo="You land on the engagement, with its Blueprint at the top, ready for the next step.", cap='You are in'),
 ]},
}
L=LESSONS[sys.argv[1]]; LID=sys.argv[1]
# ---- voice
meta_p=f'vo/{LID}.json'
if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=[b['vo'] for b in L['beats']]:
    from kokoro_onnx import Kokoro
    k=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin'); durs=[]
    for i,b in enumerate(L['beats']):
        a,sr=k.create(b['vo'],voice='af_heart',speed=1.03,lang='en-us'); sf.write(f'vo/{LID}_{i}.wav',a,sr); durs.append(len(a)/sr)
    json.dump({'texts':[b['vo'] for b in L['beats']],'durs':durs},open(meta_p,'w'))
durs=json.load(open(meta_p))['durs']
INTRO,GAP,OUTRO=2.0,0.55,2.6
t=INTRO; 
for b,d in zip(L['beats'],durs): b['s']=t; b['e']=t+d+GAP; t=b['e']
DUR=t+OUTRO
shots={}
def S(n):
    if n not in shots: shots[n]=Image.open(f'cap/{n}.jpg').convert('RGB')
    return shots[n]
def view(name,cam):
    im=S(name); x,y,w=cam; h=w*9/16; iw,ih=im.width/2,im.height/2
    x=min(max(x,0),iw-w); y=min(max(y,0),max(0,ih-h))
    return im.resize((W,H),Image.LANCZOS,box=(x*2,y*2,(x+w)*2,(y+h)*2)),(x,y,w)
def card(title,sub,foot,a=1.0):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,400,184,464),14,fill=BRASS); d.text((140,408),'J',font=font('Bold',40),fill=(26,20,8))
    d.text((210,412),'JSH Training Academy',font=font('SemiBold',34),fill=SOFT)
    d.text((120,500),title,font=font('Bold',92),fill=INK); d.text((120,620),sub,font=font('Medium',40),fill=BLUE)
    if foot: d.text((120,700),foot,font=font('Medium',34),fill=SOFT)
    return im
def frame(t):
    if t<INTRO:
        im=card(L['title'],L['module'],'JSH AI Workshop Platform · Facilitator path')
        k=ease((t-(INTRO-0.35))/0.35)
        if k>0: nxt,_=view(L['beats'][0]['shot'],L['beats'][0]['cam'][0]); im=Image.blend(im,nxt,k)
        return im
    if t>=DUR-OUTRO:
        im=card('Try it yourself','Practice on the Demo engagement: Counter-to-dock ordering','Then take the quick check to mark this lesson complete.')
        k=1-ease((t-(DUR-OUTRO))/0.35)
        if k>0: b=L['beats'][-1]; prev,_=view(b['shot'],b['cam'][1]); im=Image.blend(im,prev,k)
        return im
    i=max(j for j,b in enumerate(L['beats']) if t>=b['s']); b=L['beats'][i]; p=(t-b['s'])/(b['e']-b['s'])
    c0,c1=b['cam']; k=ease((p-0.08)/0.6); cam=tuple(c0[j]+(c1[j]-c0[j])*k for j in range(3))
    name=b['shot']
    im,(cx,cy,cw)=view(name,cam)
    if b.get('shot2'):
        q=ease((p-0.55)/0.12) if not b.get('click') else ease((p-0.80)/0.06)
        if q>0: im2,_=view(b['shot2'],cam); im=Image.blend(im,im2,q)
    sc=W/cw; ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ha=ease((p-0.25)/0.15)*(1-ease((p-0.92)/0.08))
    if ha>0 and not (b.get('shot2') and b.get('click') and p>0.8):
        for key in b.get('hl',[]):
            x,y,w,h=bx(key); x0,y0,x1,y1=(x-cx)*sc,(y-cy)*sc,(x+w-cx)*sc,(y+h-cy)*sc; g=0.5+0.5*math.sin(t*5)
            d.rounded_rectangle((x0,y0,x1,y1),14,outline=BRASS+(int(255*ha),),width=5)
            d.rounded_rectangle((x0-9,y0-9,x1+9,y1+9),20,outline=BRASS+(int(90*ha*g),),width=4)
    if b.get('click'):
        px,py=ctr(b['click']); X,Y=(px-cx)*sc,(py-cy)*sc; cp=(p-0.74)/0.14
        ap=ease((p-0.5)/0.2)                              # pointer glides in
        mx,my=X+140*(1-ap),Y+110*(1-ap)
        if p>0.45: d.polygon([(mx,my),(mx,my+34),(mx+9,my+26),(mx+16,my+40),(mx+22,my+37),(mx+15,my+24),(mx+26,my+24)],fill=(255,255,255,255),outline=(20,20,20,255))
        if 0<=cp<1: r=14+46*eout(cp); d.ellipse((X-r,Y-r,X+r,Y+r),outline=(255,255,255,int(230*(1-cp))),width=5)
    # caption strip
    ca=min(ease(p/0.08),1-ease((p-0.95)/0.05))
    f=font('SemiBold',40); tw=d.textlength(b['cap'],font=f)
    d.rounded_rectangle((W/2-tw/2-34,H-128,W/2+tw/2+34,H-52),38,fill=(11,16,21,int(225*ca)),outline=(47,59,71,int(255*ca)),width=2)
    d.text((W/2-tw/2,H-114),b['cap'],font=f,fill=INK+(int(255*ca),))
    # progress dots
    for j in range(len(L['beats'])):
        d.ellipse((60+j*26,H-98,74+j*26,H-84),fill=(BRASS if j<=i else (60,72,84))+(230,))
    im=Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    if i>0 and b['shot']!=L['beats'][i-1].get('shot2',L['beats'][i-1]['shot']) and t-b['s']<0.25:      # cut between screens: quick cross-dissolve
        pb=L['beats'][i-1]; prev,_=view(pb.get('shot2',pb['shot']),pb['cam'][1]); im=Image.blend(prev,im,ease((t-b['s'])/0.25))
    return im
if len(sys.argv)>2:
    ts=[0.8]+[b['s']+(b['e']-b['s'])*f for b in L['beats'] for f in (0.5,0.88)]+[DUR-1]
    ims=[frame(x).resize((480,270)) for x in ts]; n=len(ims); sh=Image.new('RGB',(480*4,270*math.ceil(n/4)))
    [sh.paste(im,(480*(k%4),270*(k//4))) for k,im in enumerate(ims)]; sh.save(f'shots/{LID}_sheet.jpg',quality=85); print(round(DUR,2)); sys.exit()
# ---- audio: VO + soft clicks
SR=48000; n=int(DUR*SR); mix=np.zeros(n)
for i,b in enumerate(L['beats']):
    a,sr=sf.read(f'vo/{LID}_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int(b['s']*SR); mix[s:s+len(a)]+=a[:n-s]/(abs(a).max()+1e-9)*0.9
    if b.get('click'):
        ct=b['s']+(b['e']-b['s'])*0.74; x=np.arange(int(0.03*SR))/SR; c=np.random.randn(len(x))*np.exp(-x*300)*0.35; s=int(ct*SR); mix[s:s+len(c)]+=c
x=np.arange(int(1.2*SR))/SR; ch=(np.sin(2*np.pi*660*x)+0.6*np.sin(2*np.pi*990*x))*np.exp(-x*4)*0.12; mix[int(0.2*SR):int(0.2*SR)+len(ch)]+=ch
sf.write(f'out/{LID}.wav',np.stack([mix,mix],1)*0.9,SR)
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','19','-preset','veryfast','-pix_fmt','yuv420p',f'out/{LID}.tmp.mp4'],stdin=subprocess.PIPE)
for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
ff.stdin.close(); assert ff.wait()==0
subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'out/{LID}.tmp.mp4','-i',f'out/{LID}.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',f'out/AWP_Academy_{LID}.mp4'],check=True)
os.remove(f'out/{LID}.tmp.mp4'); print('ok',round(DUR,2))
