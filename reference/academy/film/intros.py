"""Academy module intro films (AWP Facilitator path). High-level: what the module is for, when you use it, what you can do by the end.
Wide shots of real Demo-engagement screens with a slow camera, a "you are here" module map, Kokoro voice-over, soft music bed.
usage: python3 intros.py <m1..m7|all> [stills]"""
import json, math, os, subprocess, sys
import numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
W,H,FPS=1920,1080,30
F='/usr/share/fonts/opentype/inter/InterDisplay-'
def font(w,s): return ImageFont.truetype(F+w+'.otf',s)
def ease(x): x=max(0.,min(1.,x)); return x*x*(3-2*x)
def eout(x): x=max(0.,min(1.,x)); return 1-(1-x)**3
PAPER,INK,SOFT,BLUE,BRASS,LINE=(18,24,30),(232,237,241),(157,170,182),(110,168,232),(217,178,95),(47,59,71)
def cmix(c,a,bg=None):
    bg=bg or PAPER; a=max(0.,min(1.,a)); return tuple(int(bg[i]+(c[i]-bg[i])*a) for i in range(3))
NAMES=['Get in and get around','Start an engagement','The pre-workshop questionnaire','Run Workshop 1','Read and shape the Blueprint','Build the prototype','Share and hand off']
WIDE=((0,0,1440),(70,40,1300))
MODS={
 'm1':dict(n=1, lessons=['Sign in with your email link','Read the engagements list','Find your way back'],
   intro="Module one. Get in and get around.",
   shots=[('signin',((0,0,1440),(90,50,760)),'Sign in with a link, no password',"The Workshop Platform has no passwords. You sign in with a link sent to your JSH email."),
          ('list',WIDE,'All engagements is home base',"All engagements is home base. Every client engagement is listed with its client, its industry, and its stage."),
          ('top2',((0,0,1440),(60,0,1000)),'One click back, from anywhere',"Open one and you're inside the engagement. All engagements is always one click away, at the top.")],
   end="By the end of this module, you'll sign in, read the list, and never get lost."),
 'm2':dict(n=2, lessons=['Create a new engagement','Edit setup and rebuild the expert voices','Delete an engagement safely'],
   intro="Module two. Start an engagement.",
   shots=[('new1',((0,150,1440),(60,200,900)),'One client, one app',"An engagement is one client and one app. Starting one takes a name, the client, and their industry."),
          ('ov_voices',((200,90,1100),(300,160,860)),'Three expert voices',"From those three things, the platform builds three expert voices that guide every question."),
          ('new2',((60,330,900),(70,520,860)),'Questionnaire first, or straight to live',"You'll also decide whether the client answers a short questionnaire first, or you go straight to a live workshop.")],
   end="By the end, you'll create an engagement, edit its setup, and delete one safely."),
 'm3':dict(n=3, lessons=['Prepare and pre-fill the questions','Preview it and email the client','Bring the answers into the Blueprint','Know their tools before the meeting'],
   intro="Module three. The pre-workshop questionnaire.",
   shots=[('cl_top',((60,0,1300),(150,20,780)),'Ten minutes, any device, no sign-in',"The pre-workshop questionnaire is a short, standard set of questions the client fills in before you meet. About ten minutes, on any device, with no sign-in."),
          ('eng',((120,1560,1100),(120,2050,1100)),'Pre-fill what you heard on the call',"Pre-fill what you heard on the call, and they just edit it. Then email it from the platform."),
          ('cl_end',((300,150,1000),(360,400,720)),'They answer only what they want to',"The client answers only what they want to. Anything they skip, you cover together in the workshop."),
          ('ov_apps',((180,40,1100),(300,120,880)),'Answers in, tools looked up',"When it comes back, their answers go straight into the Blueprint, every tool they named is looked up, and you get a meeting plan."),
          ('q_round',((0,0,1440),(130,90,1180)),'New questions, written from their answers',"The plan includes new questions, written from their answers. Anything unclear, or left open, becomes a question for the meeting.")],
   end="By the end, you'll prepare it, send it, bring the answers in, and know their tools before the meeting."),
 'm4':dict(n=4, lessons=['Present to client: the client-safe view','Work the Open-with checklist','Ask the next questions','Use the JSH chamber and import call notes','Mark Workshop 1 complete'],
   intro="Module four. Run Workshop 1.",
   shots=[('present2',WIDE,'A client-safe view while you run the room',"Workshop 1 is the conversation with the client. Present to client gives them a clean, client-safe view while you run the room."),
          ('q_round',((0,0,1440),(130,90,1180)),'Twenty core questions, five at a time',"The platform asks the questions, five at a time, from the biggest gaps in the Blueprint. Twenty core questions in all."),
          ('idk_offer',((0,0,1440),(140,150,1160)),'Don’t know? It offers the industry answer',"When they don't know, it offers how others in their industry do it."),
          ('ready_done',((0,0,1440),(60,30,1100)),'The checklist says when you’re done',"A readiness checklist tells you when you're done. Then you mark Workshop 1 complete.")],
   end="By the end, you'll present, ask, use the JSH chamber, and close out Workshop 1."),
 'm5':dict(n=5, lessons=['Read a Blueprint card','Adopt, rework or decline a recommendation','Confirm or correct an assumption'],
   intro="Module five. Read and shape the Blueprint.",
   shots=[('bp_full',((0,0,1440),(120,60,1200)),'Ten sections, each with a score',"The Blueprint is everything the platform knows about the app, in ten sections, each with a completion score."),
          ('jr2',((180,0,1080),(300,60,900)),'Every fact, and where it came from',"Open a card to see every fact, and where it came from."),
          ('recs_adopted',((180,0,1080),(300,150,900)),'Adopt, give feedback, or decline',"The domain expert makes recommendations. You adopt them, send them back with feedback, or decline with a reason."),
          ('ov_assume',((200,100,1100),(320,170,820)),'Assumptions are logged to confirm',"And anything assumed is logged, for you to confirm or correct.")],
   end="By the end, you'll read a card, handle recommendations, and settle assumptions."),
 'm6':dict(n=6, lessons=['Propose and approve a design direction','Build it and click through','Comment on a spot and tweak a screen','Update the Blueprint from feedback','Work with versions'],
   intro="Module six. Build the prototype.",
   shots=[('dd_top',WIDE,'First, a design direction',"First, the platform proposes a design direction: colors, type, tone, and one sample screen. You approve the look."),
          ('proto_a2',((0,0,1440),(140,40,1180)),'Then every screen, clickable',"Then it builds every screen into a clickable prototype you can enter as each kind of user."),
          ('cm_saved',((0,0,1440),(150,120,1150)),'Comment on any spot',"Comment on any spot, and tweak a screen from the comment."),
          ('ub2',((0,150,1440),(140,170,1160)),'Blueprint and prototype stay in step',"Bigger changes go through Update the Blueprint, so the Blueprint and the prototype never drift apart.")],
   end="By the end, you'll approve a direction, build, comment, update, and work with versions."),
 'm7':dict(n=7, lessons=['Create a share link for the client','Run the build-readiness check','Export the build package'],
   intro="Module seven. Share and hand off.",
   shots=[('PHONE',None,'On the client’s own phone, no sign-in',"A share link puts the prototype in the client's hands, on their own phone, with no sign-in."),
          ('readiness2',((0,0,1440),(130,40,1000)),'Every gap becomes a question',"The build-readiness check scores every section against what the build needs, and turns each gap into a question."),
          ('top2',((0,0,1440),(100,180,1240)),'Build-ready at ninety percent',"At ninety percent, with nothing left to confirm with the client, the engagement is build-ready, and a Product Engineer exports the build package for the JSH build team.")],
   end="By the end, you'll share a link, run the check, and know what happens at export."),
}
shots={}
def S(n):
    if n not in shots:
        p=next(x for x in (f'cap/{n}.jpg',f'cap/p2/{n}.jpg',f'cap/early/{n}.jpg') if os.path.exists(x)); shots[n]=Image.open(p).convert('RGB')
        if n=='list':
            im=shots[n]; sc=im.width/1440; bg=im.getpixel((int(130*sc),int(600*sc))); ImageDraw.Draw(im).rectangle((int(100*sc),int(470*sc),int(1340*sc),int(560*sc)),fill=bg)
    return shots[n]
def view(name,cam):
    im=S(name); sc=im.width/1440; x,y,w=cam; h=w*9/16; iw,ih=im.width/sc,im.height/sc
    x=min(max(x,0),iw-w); y=min(max(y,0),max(0,ih-h))
    return im.resize((W,H),Image.LANCZOS,box=(x*sc,y*sc,(x+w)*sc,(y+h)*sc))
_ph={}
def phone(p):
    im=Image.new('RGB',(W,H),PAPER)
    for j,n in enumerate(['ph_who','ph_route','ph_stop']):
        if n not in _ph:
            src=Image.open(f'cap/p2/{n}.jpg').convert('RGB').resize((398,862),Image.LANCZOS); m=Image.new('L',(398,862),0); ImageDraw.Draw(m).rounded_rectangle((0,0,397,861),34,fill=255); _ph[n]=(src,m)
        a=eout((p-0.03-j*0.10)/0.2)
        if a<=0: continue
        x=304+j*458; y=int(70+70*(1-a)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((x-12,y-12,x+410,y+874),44,fill=(8,11,15),outline=(70,84,98),width=3)
        src,m=_ph[n]; im.paste(Image.blend(Image.new('RGB',src.size,PAPER),src,a),(x,y),m)
    return im
def head(d,a=1.0):
    d.rounded_rectangle((120,150,176,206),12,fill=cmix(BRASS,a)); d.text((137,157),'J',font=font('Bold',35),fill=cmix((26,20,8),a,BRASS))
    d.text((196,160),'JSH Training Academy  ·  AI Workshop Platform  ·  Facilitator path',font=font('SemiBold',30),fill=cmix(SOFT,a))
def intro_card(M,p):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); a=ease(p/0.10); head(d,a)
    d.text((120,300),f"MODULE {M['n']} OF 7",font=font('Bold',36),fill=cmix(BRASS,a))
    d.text((120,360),NAMES[M['n']-1],font=font('Bold',104),fill=cmix(INK,a))
    # you-are-here map
    x=120; y=640; b=ease((p-0.25)/0.2)
    d.text((120,588),'WHERE THIS FITS',font=font('SemiBold',22),fill=cmix((111,125,138),b))
    for j,nm in enumerate(NAMES):
        f=font('SemiBold',24); tw=d.textlength(nm,font=f); wbox=tw+62; on=(j==M['n']-1); k=ease((p-0.25-j*0.035)/0.15)
        if x+wbox>W-110: x=120; y+=76
        d.rounded_rectangle((x,y,x+wbox,y+56),28,fill=cmix((34,44,54) if not on else BRASS,k),outline=cmix(LINE if not on else BRASS,k),width=2)
        d.text((x+18,y+13),str(j+1),font=font('Bold',24),fill=cmix((26,20,8) if on else (111,125,138),k,(BRASS if on else (34,44,54))))
        d.text((x+42,y+13),nm,font=f,fill=cmix((26,20,8) if on else SOFT,k,(BRASS if on else (34,44,54))))
        x+=wbox+14
    return im
def end_card(M,p):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im); head(d,ease(p/0.08))
    d.text((120,290),'IN THIS MODULE',font=font('Bold',32),fill=cmix(BRASS,ease(p/0.08)))
    for j,t in enumerate(M['lessons']):
        k=ease((p-0.08-j*0.09)/0.12); y=360+j*92
        d.ellipse((120,y+8,164,y+52),outline=cmix(BRASS,k),width=3); d.text((142-d.textlength(str(j+1),font=font('Bold',26))/2,y+13),str(j+1),font=font('Bold',26),fill=cmix(BRASS,k))
        d.text((190,y),t,font=font('SemiBold',52),fill=cmix(INK,k))
    return im
def build(mid, stills=False):
    M=MODS[mid]; beats=[dict(kind='intro',vo=M['intro'])]+[dict(shot=s,cam=c,cap=cp,vo=v) for s,c,cp,v in M['shots']]+[dict(kind='end',vo=M['end'])]
    meta_p=f'vo/in_{mid}.json'; texts=[b['vo'] for b in beats]
    if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=texts:
        global KO
        if 'KO' not in globals():
            from kokoro_onnx import Kokoro
            KO=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin')
        durs=[]
        for i,b in enumerate(beats):
            a,sr=KO.create(b['vo'],voice='af_heart',speed=1.02,lang='en-us'); sf.write(f'vo/in_{mid}_{i}.wav',a,sr); durs.append(len(a)/sr)
        json.dump({'texts':texts,'durs':durs},open(meta_p,'w'))
    durs=json.load(open(meta_p))['durs']; LEAD,OUTRO=0.5,1.2; t=LEAD
    for b,dd in zip(beats,durs):
        b['s']=t; b['e']=t+dd+(1.9 if b.get('kind')=='intro' else 1.3 if b.get('kind')=='end' else 0.55); t=b['e']
    DUR=t+OUTRO
    def scene(i,t):
        b=beats[i]; p=(t-b['s'])/(b['e']-b['s'])
        if b.get('kind')=='intro': return intro_card(M,p)
        if b.get('kind')=='end': return end_card(M,min(1,(t-b['s'])/max(1e-6,(b['e']-b['s']))))
        if b['shot']=='PHONE': im=phone(p)
        else:
            c0,c1=b['cam']; k=ease(p*1.02); im=view(b['shot'],tuple(c0[j]+(c1[j]-c0[j])*k for j in range(3)))
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); ca=min(ease(p/0.08),1-ease((p-0.95)/0.05)); f=font('SemiBold',42); tw=d.textlength(b['cap'],font=f)
        d.rounded_rectangle((W/2-tw/2-36,H-132,W/2+tw/2+36,H-52),40,fill=(11,16,21,int(236*ca)),outline=BRASS+(int(150*ca),),width=2); d.text((W/2-tw/2,H-117),b['cap'],font=f,fill=INK+(int(255*ca),))
        return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    prev={}
    def frame(t):
        if t<beats[0]['s']: return Image.blend(Image.new('RGB',(W,H),(0,0,0)),intro_card(M,0),ease(t/LEAD))
        i=max(j for j,b in enumerate(beats) if t>=b['s']) ; tt=min(t,beats[-1]['e']-1e-3); im=scene(i,tt)
        if i>0 and t-beats[i]['s']<0.3:
            if i not in prev: prev[i]=scene(i-1,beats[i-1]['e']-1e-3)
            im=Image.blend(prev[i],im,ease((t-beats[i]['s'])/0.3))
        f=ease((t-(DUR-0.5))/0.5)
        return Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),f) if f>0 else im
    if stills:
        ts=[beats[0]['s']+1.6]+[b['s']+(b['e']-b['s'])*0.8 for b in beats[1:-1]]+[beats[-1]['e']-0.2]
        return [frame(x).resize((480,270)) for x in ts], DUR
    SR=48000; n=int(DUR*SR); vo=np.zeros(n)
    for i,b in enumerate(beats):
        a,sr=sf.read(f'vo/in_{mid}_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int((b['s']+(0.25 if b.get('kind') else 0))*SR); a=a[:n-s]; vo[s:s+len(a)]+=a/(abs(a).max()+1e-9)*0.9
    def nf(m): return 440*2**((m-69)/12)
    pad=np.zeros(n); bar=4.0; major=[[48,55,60,64],[43,55,59,62],[45,57,60,64],[41,53,57,60]]; k=0; t0=0.0
    while t0<DUR:
        ch=major[k%4]; s=int(t0*SR); L=min(int((bar+1.2)*SR),n-s); x=np.arange(L)/SR; env=np.clip(np.minimum(x/1.2,1)*np.minimum((bar+1.2-x)/1.2,1),0,1)
        sig=sum(np.sin(2*np.pi*nf(m)*x)+0.35*np.sin(2*np.pi*nf(m)*2*x+0.5)+0.5*np.sin(2*np.pi*nf(m)*1.003*x) for m in ch)/len(ch); pad[s:s+L]+=sig*env*0.15; t0+=bar; k+=1
    ev=np.abs(vo); w=int(0.25*SR); ev=np.convolve(ev,np.ones(w)/w,'same'); pad*=1-0.55*np.clip(ev/0.08,0,1); pad[:int(0.6*SR)]*=np.linspace(0,1,int(0.6*SR)); pad[-int(1.2*SR):]*=np.linspace(1,0,int(1.2*SR))
    x=np.arange(int(1.2*SR))/SR; ch=(np.sin(2*np.pi*660*x)+0.6*np.sin(2*np.pi*990*x))*np.exp(-x*4)*0.10; mixd=vo+pad; mixd[int(0.2*SR):int(0.2*SR)+len(ch)]+=ch
    mixd=mixd/max(1.0,abs(mixd).max())*0.95; sf.write(f'out/in_{mid}.wav',np.stack([mixd,mixd],1),SR)
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','23','-preset','medium','-pix_fmt','yuv420p',f'out/in_{mid}.tmp.mp4'],stdin=subprocess.PIPE)
    for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
    ff.stdin.close(); assert ff.wait()==0
    out=f"out/AWP_Module{M['n']}_Intro.mp4"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'out/in_{mid}.tmp.mp4','-i',f'out/in_{mid}.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],check=True)
    os.remove(f'out/in_{mid}.tmp.mp4'); print('ok',mid,round(DUR,2),os.path.getsize(out)//1024,'KB',flush=True)
ids=list(MODS) if sys.argv[1]=='all' else [sys.argv[1]]
if len(sys.argv)>2:
    rows=[];
    for mid in ids:
        ims,D=build(mid,True); print(mid,round(D,1)); rows.append(ims)
    sh=Image.new('RGB',(480*6,270*len(rows)),(0,0,0))
    for r,ims in enumerate(rows): [sh.paste(im,(480*c,270*r)) for c,im in enumerate(ims)]
    sh.save('shots/intros_sheet.jpg',quality=82)
else:
    for mid in ids: build(mid)
