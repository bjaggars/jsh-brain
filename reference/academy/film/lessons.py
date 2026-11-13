"""Academy click-by-click lessons (AWP Facilitator path): real Demo-engagement captures, dynamic camera, gold highlights, pointer + click,
headline captions, Kokoro voice-over. Same voice, pacing and caption style as the approved module intros.
usage: python3 lessons.py <lesson_id|all> [stills]"""
import json, math, os, subprocess, sys
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
PRESENT=(144,335,136,35); YES=(165,412.7,135.7,44); ASSUME=(308.7,411.7,245.4,46); OFFER=(165,335.7,1110,122)
LESSONS={
 'present':dict(title='Present to client: the client-safe view', module='Module 4 · Run Workshop 1', file='Present_to_client', beats=[
   dict(shot='top2', cam=((0,0,1440),(60,150,1000)), hl=[PRESENT], cap='Before you share your screen',
        vo="Before you share your screen with a client, switch to the client-safe view."),
   dict(shot='top2', shot2='present2', cam=((60,150,1000),(60,150,1000)), hl=[PRESENT], click=PRESENT, cap='Choose Present to client',
        vo="Choose Present to client, under the client line."),
   dict(shot='present2', cam=((60,150,1000),(0,60,1440)), hl=[(150,262,240,45)], cap='Only what the client should see',
        vo="The page now shows only what the client should see: the progress bar, the Blueprint,"),
   dict(shot='pv_rec', cam=((0,0,1440),(120,60,1200)), hl=[(155,108,1130,350)], cap='Blueprint, Workshop record, Workshop questions',
        vo="the Workshop record, and the Workshop questions."),
   dict(shot='jv_hidden', cam=((0,0,1440),(100,60,1240)), hl=[(155,128,1130,190),(155,343,1130,420)], cap='Hidden: your working panels',
        vo="Hidden from them: the questionnaire panel, client files, readiness, the JSH chamber, and the prototype controls."),
   dict(shot='pv_q', cam=((0,0,1440),(60,0,1000)), hl=[(246,10,138,42)], click=(253,17,124,28), cap='Back to JSH view',
        vo="When you're done, Back to JSH view brings everything back."),
 ]),
 'ask':dict(title='Ask the next questions', module='Module 4 · Run Workshop 1', file='Ask_the_next_questions', beats=[
   dict(shot='q_round', cam=((0,0,1440),(130,90,1180)), hl=[(155,120,1130,30)], cap='Five questions at a time',
        vo="In the Client workshop tab, Ask the next questions brings five at a time, from the biggest gaps in the Blueprint."),
   dict(shot='q_round', cam=((130,90,1180),(150,120,1140)), hl=[(155,148,1130,258)], cap='Type the answer, then Save answer',
        vo="Each one says why it matters. Ask it in your own words, type what the client says, and choose Save answer."),
   dict(shot='idk_done', cam=((0,0,1440),(130,60,1180)), hl=[(155,136,1130,190)], cap='Facts go straight into the Blueprint',
        vo="The platform reads the answer, adds the facts to the Blueprint, and may raise a recommendation."),
   dict(shot='idk_offer', cam=((0,0,1440),(140,150,1160)), hl=[OFFER], cap='I don’t know offers the industry answer',
        vo="If the client doesn't know, choose I don't know. The platform offers what most businesses like theirs do."),
   dict(shot='idk_offer', cam=((140,150,1160),(150,235,1140)), hl=[YES,ASSUME], click=YES, cap='Accept it, or log an assumption',
        vo="Yes, that's us accepts it. Not sure, assume it for now logs an assumption to confirm later."),
   dict(shot='bp_full', cam=((0,0,1440),(120,60,1200)), hl=[], cap='Twenty core questions fill the Blueprint',
        vo="Keep going until the twenty core questions are done, and watch the Blueprint fill in."),
 ]),
 'ready':dict(title='Mark Workshop 1 complete', module='Module 4 · Run Workshop 1', file='Mark_Workshop_1_complete', beats=[
   dict(shot='early/readiness', cam=((0,0,1440),(100,20,1240)), hl=[(160,62,330,44)], cap='Before the prototype: the readiness checklist',
        vo="On the engagement, the panel called Before the prototype is your readiness checklist for Workshop 1."),
   dict(shot='early/readiness', cam=((100,20,1240),(130,90,1000)), hl=[(160,146,700,226)], cap='Every line must be checked',
        vo="Each line is something the prototype needs: the core questions answered, the rest answered or assumed, and a Blueprint at sixty percent."),
   dict(shot='early/readiness', cam=((130,90,1000),(120,250,1200)), hl=[(160,378,1120,310)], cap='Add closing comments, or Nothing to add',
        vo="Then add closing comments for the client side and for JSH. If there are none, choose Nothing to add."),
   dict(shot='ready_done', cam=((0,0,1440),(110,60,1100)), hl=[(160,84,400,40)], cap='It becomes Ready for the prototype',
        vo="When every line is checked, the panel becomes Ready for the prototype."),
   dict(shot='ready_done', shot2='w1_complete', cam=((110,60,1100),(110,80,1060)), hl=[(160,584,258,56)], click=(168,591,242,42), cap='Mark Workshop 1 complete',
        vo="Choose Mark Workshop 1 complete. The prototype step opens, and you can reopen Workshop 1 if anything changes."),
 ]),
}
shots={}
def S(n):
    if n not in shots:
        p=next(x for x in (f'cap/{n}.jpg',f'cap/p2/{n}.jpg',f'cap/early/{n}.jpg') if os.path.exists(x)); shots[n]=Image.open(p).convert('RGB')
    return shots[n]
def view(name,cam):
    im=S(name); sc=im.width/1440; x,y,w=cam; h=w*9/16; iw,ih=im.width/sc,im.height/sc
    x=min(max(x,0),iw-w); y=min(max(y,0),max(0,ih-h))
    return im.resize((W,H),Image.LANCZOS,box=(x*sc,y*sc,(x+w)*sc,(y+h)*sc)),(x,y,w)
def card(kicker,title,sub,a=1.0):
    im=Image.new('RGB',(W,H),PAPER); d=ImageDraw.Draw(im)
    d.rounded_rectangle((120,330,176,386),12,fill=cmix(BRASS,a)); d.text((137,337),'J',font=font('Bold',35),fill=cmix((26,20,8),a,BRASS))
    d.text((196,340),'JSH Training Academy  ·  AI Workshop Platform  ·  Facilitator path',font=font('SemiBold',30),fill=cmix(SOFT,a))
    d.text((120,440),kicker.upper(),font=font('Bold',34),fill=cmix(BRASS,a))
    f=font('Bold',92 if d.textlength(title,font=font('Bold',92))<W-240 else 72); d.text((120,500),title,font=f,fill=cmix(INK,a))
    if sub: d.text((120,640),sub,font=font('Medium',40),fill=cmix(SOFT,a))
    return im
def build(lid, stills=False):
    L=LESSONS[lid]; beats=L['beats']; meta_p=f'vo/ls_{lid}.json'; texts=[b['vo'] for b in beats]
    if not os.path.exists(meta_p) or json.load(open(meta_p))['texts']!=texts:
        global KO
        if 'KO' not in globals():
            from kokoro_onnx import Kokoro
            KO=Kokoro('/home/claude/jsh-brain/reference/studio/models/kokoro-v1.0.onnx','/home/claude/jsh-brain/reference/studio/models/voices-v1.0.bin')
        durs=[]
        for i,b in enumerate(beats):
            a,sr=KO.create(b['vo'],voice='af_heart',speed=1.02,lang='en-us'); sf.write(f'vo/ls_{lid}_{i}.wav',a,sr); durs.append(len(a)/sr)
        json.dump({'texts':texts,'durs':durs},open(meta_p,'w'))
    durs=json.load(open(meta_p))['durs']; INTRO,GAP,OUTRO=2.4,0.55,3.0; t=INTRO
    for b,dd in zip(beats,durs): b['s']=t; b['e']=t+dd+GAP; t=b['e']
    DUR=t+OUTRO
    def scene(i,t):
        b=beats[i]; p=(t-b['s'])/(b['e']-b['s']); c0,c1=b['cam']; k=ease((p-0.06)/0.62); cam=tuple(c0[j]+(c1[j]-c0[j])*k for j in range(3))
        im,(cx,cy,cw)=view(b['shot'],cam); c_at=0.50 if b.get('shot2') else 0.74
        if b.get('shot2'):
            q=ease((p-c_at-0.04)/0.05)
            if q>0: im2,_=view(b['shot2'],cam); im=Image.blend(im,im2,q)
        sc=W/cw; ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
        ha=ease((p-0.28)/0.15)*(1-ease((p-0.93)/0.07))
        if b.get('shot2'): ha=ease((p-0.10)/0.12)*(1-ease((p-c_at)/0.04))
        if ha>0:
            for x,y,w,h in b.get('hl',[]):
                pad=5 if h<32 else 8; x0,y0,x1,y1=(x-pad-cx)*sc,(y-pad-cy)*sc,(x+w+pad-cx)*sc,(y+h+pad-cy)*sc; g=0.5+0.5*math.sin(t*5)
                d.rounded_rectangle((x0,y0,x1,y1),14,outline=BRASS+(int(255*ha),),width=5); d.rounded_rectangle((x0-9,y0-9,x1+9,y1+9),20,outline=BRASS+(int(90*ha*g),),width=4)
        if b.get('click'):
            bx_,by_,bw_,bh_=b['click']; X,Y=(bx_+bw_/2-cx)*sc,(by_+bh_/2-cy)*sc; cp=(p-c_at)/0.14; ap=ease((p-(c_at-0.26))/0.2); mx,my=X+150*(1-ap),Y+120*(1-ap)
            if p>c_at-0.3 and not (b.get('shot2') and p>c_at+0.22):
                d.polygon([(mx,my),(mx,my+34),(mx+9,my+26),(mx+16,my+40),(mx+22,my+37),(mx+15,my+24),(mx+26,my+24)],fill=(255,255,255,255),outline=(20,20,20,255))
            if 0<=cp<1: r=14+46*eout(cp); d.ellipse((X-r,Y-r,X+r,Y+r),outline=(255,255,255,int(230*(1-cp))),width=5)
        ca=min(ease(p/0.08),1-ease((p-0.95)/0.05)); f=font('SemiBold',42); tw=d.textlength(b['cap'],font=f)
        d.rounded_rectangle((W/2-tw/2-36,H-132,W/2+tw/2+36,H-52),40,fill=(11,16,21,int(236*ca)),outline=BRASS+(int(150*ca),),width=2); d.text((W/2-tw/2,H-117),b['cap'],font=f,fill=INK+(int(255*ca),))
        for j in range(len(beats)): d.ellipse((60+j*26,H-98,74+j*26,H-84),fill=(BRASS if j<=i else (60,72,84))+(230,))
        return Image.alpha_composite(im.convert('RGBA'),ov).convert('RGB')
    prev={}
    def frame(t):
        if t<INTRO:
            im=card(L['module'],L['title'],'',ease(t/0.4)); k=ease((t-(INTRO-0.35))/0.35)
            return Image.blend(im,scene(0,beats[0]['s']),k) if k>0 else im
        if t>=DUR-OUTRO:
            im=card('Your turn','Now practice it','Open the Practice tab, then take the quick check to complete the lesson.'); k=ease((t-(DUR-OUTRO))/0.4)
            if k<1:
                if 'end' not in prev: prev['end']=scene(len(beats)-1,beats[-1]['e']-1e-3)
                im=Image.blend(prev['end'],im,k)
            f=ease((t-(DUR-0.5))/0.5); return Image.blend(im,Image.new('RGB',(W,H),(0,0,0)),f) if f>0 else im
        i=max(j for j,b in enumerate(beats) if t>=b['s']); im=scene(i,t)
        if i>0 and t-beats[i]['s']<0.3 and (beats[i]['shot']!=beats[i-1].get('shot2',beats[i-1]['shot']) or beats[i]['cam'][0]!=beats[i-1]['cam'][1]):
            if i not in prev: prev[i]=scene(i-1,beats[i-1]['e']-1e-3)
            im=Image.blend(prev[i],im,ease((t-beats[i]['s'])/0.3))
        return im
    if stills:
        ts=[b['s']+(b['e']-b['s'])*f for b in beats for f in (0.45,0.9)]; return [frame(x).resize((480,270)) for x in ts], DUR
    SR=48000; n=int(DUR*SR); mixd=np.zeros(n)
    for i,b in enumerate(beats):
        a,sr=sf.read(f'vo/ls_{lid}_{i}.wav'); a=np.interp(np.arange(int(len(a)*SR/sr))*sr/SR,np.arange(len(a)),a); s=int(b['s']*SR); a=a[:n-s]; mixd[s:s+len(a)]+=a/(abs(a).max()+1e-9)*0.9
        if b.get('click'):
            ct=b['s']+(b['e']-b['s'])*(0.50 if b.get('shot2') else 0.74); x=np.arange(int(0.03*SR))/SR; c=np.random.randn(len(x))*np.exp(-x*300)*0.3; s=int(ct*SR); mixd[s:s+len(c)]+=c
    x=np.arange(int(1.2*SR))/SR; ch=(np.sin(2*np.pi*660*x)+0.6*np.sin(2*np.pi*990*x))*np.exp(-x*4)*0.12; mixd[int(0.2*SR):int(0.2*SR)+len(ch)]+=ch
    mixd=mixd/max(1.0,abs(mixd).max())*0.95; sf.write(f'out/ls_{lid}.wav',np.stack([mixd,mixd],1),SR)
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','23','-preset','medium','-pix_fmt','yuv420p',f'out/ls_{lid}.tmp.mp4'],stdin=subprocess.PIPE)
    for k in range(int(DUR*FPS)): ff.stdin.write(frame(k/FPS).tobytes())
    ff.stdin.close(); assert ff.wait()==0
    out=f"out/AWP_Lesson_{L['file']}.mp4"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',f'out/ls_{lid}.tmp.mp4','-i',f'out/ls_{lid}.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',out],check=True)
    os.remove(f'out/ls_{lid}.tmp.mp4'); print('ok',lid,round(DUR,2),os.path.getsize(out)//1024,'KB',flush=True)
ids=list(LESSONS) if sys.argv[1]=='all' else sys.argv[1].split(',')
if len(sys.argv)>2:
    rows=[]
    for lid in ids:
        ims,D=build(lid,True); print(lid,round(D,1)); rows.append(ims)
    wmax=max(len(r) for r in rows); sh=Image.new('RGB',(480*wmax,270*len(rows)),(0,0,0))
    for r,ims in enumerate(rows): [sh.paste(im,(480*c,270*r)) for c,im in enumerate(ims)]
    sh.save('shots/lessons_sheet.jpg',quality=82)
else:
    for lid in ids: build(lid)
