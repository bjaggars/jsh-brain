import json, re, subprocess, os, sys
sys.path.insert(0,'/home/claude/mrvfilm'); from films import FILMS
OUT='/home/claude/mrvfilm/out'
def dur(f):
    s=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode()); return f'{int(s//60)}:{int(s%60):02d}'
Q={'tour':("Where do you find your calendar, the marketing studio, vaults, reports and your profile?",["Office, in the bottom bar","The Needs you tile","The Buyers tile"],"Office holds everything behind the scenes."),
'needs':("On Needs your attention, what does Sweep do?",["Walks you through the items one at a time","Deletes every item","Emails every client"],"Sweep clears the list one item at a time. Take all suggestions accepts every suggested move at once."),
'assistant':("Where do the assistant's answers come from?",["Your own workspace: your clients, deals and calendar","The public internet","Other agents' data"],"It only uses what is in your workspace, and says so when something isn't there."),
'addclient':("What is enough to add a client to your book?",["A name and a phone number","A signed agreement","A pre-approval letter"],"A name and a phone number are enough. You can add the rest later."),
'card':("After you talk to a client, what do you tap on their card to record it?",["Note","Vault","Testimonial"],"Note records what happened and lets you set a follow up. It lands in History."),
'pipeline':("When you import your book from a spreadsheet, when does it upload?",["Only when you say go","As soon as you choose the file","Overnight"],"The columns map themselves and you can correct them. Nothing uploads until you say go."),
'buyer':("How do you enter more than one must-have on a buyer profile?",["Separate them with commas","Create one profile for each","They cannot be entered"],"Areas, must-haves and dealbreakers are each a list separated by commas."),
'preapp':("After you save a pre-approval, what does the buyer profile show?",["What they are approved to, and the lender","Their home address","Nothing changes"],"Approved to and the lender appear right on the profile."),
'logtour':("After you log a tour, which number goes up?",["Tours done","Offers made","Homes tracked"],"Tours done counts every tour you log for that buyer."),
'newlisting':("When does a new listing's page go live?",["When you save the listing","After the first showing","After you add ten photos"],"The page goes live when you save. You add photos and the story afterwards."),
'page':("Which photo does the listing page lead with?",["The hero, the first photo you add","The newest photo","A photo chosen at random"],"The first photo becomes the hero. You can change it later."),
'runlisting':("What do you enter when you change a listing's price?",["The new price and a note for the record","A new listing","A new seller"],"Price asks for the new number and a note, so the history explains itself."),
'request':("A buyer requests a showing. Where does the request appear?",["Needs you, under Showing requests","Marketing, under Results","Office, under Reports"],"Showing requests wait for you under Needs you until you confirm or decline."),
'calendar':("Where are contract deadlines added?",["On the listing, from its contract","With New, as a task","They cannot be added"],"Deadlines live with their contract. New adds tasks, appointments and events."),
'closing':("On a closing file, what does Next tell you?",["The very next thing to do","The commission","Which client to call"],"Next names the next step. Tap the pencil to change it."),
'vault':("When you add a document to a vault, who can see it?",["You choose: share with the client, or keep it private","Everyone in the brokerage","Only the MyRealtyVault team"],"Every upload asks whether to share with the client or keep it private to you."),
'form':("What state is a new form in before you publish it?",["Draft","Live","Archived"],"A form starts as a draft. Publish makes it live and gives you a link."),
'campaign':("When does a just listed email go out?",["Only after you review it and tap Send","As soon as it is created","At midnight"],"The email waits for your review. Nothing sends until you tap Send."),
'results':("What period does Results cover?",["The last thirty days","The last year","Today only"],"Results shows the last thirty days and tells you what to do next.")}
MT=['','Your day on one screen','Clients','Buyers','Listings','Showings and calendar','Closings and documents','Marketing']
mods=[{'id':f'm{i}','t':MT[i],'d':dur(f"{OUT}/MRV_Module{i}_Intro.mp4"),'L':[]} for i in range(1,8)]
k=0
for fid,F in FILMS.items():
    if F.get('kind','lesson')!='lesson': continue
    q,o,why=Q[fid]; a=k%3; k+=1; o2=o[1:]; o2.insert(a,o[0])
    mods[F['m']-1]['L'].append({'id':fid,'t':F['title'],'d':dur(f"{OUT}/MRV_{F['file']}.mp4"),'s':[b['vo'] for b in F['beats']],'q':{'q':q,'o':o2,'a':a,'why':why}})
data={'mods':mods,'ov':dur(f'{OUT}/MRV_Agent_Overview.mp4'),'wrap':dur(f'{OUT}/MRV_Agent_Path_WrapUp.mp4')}
JS=r'''
// ---------- MyRealtyVault campus · Agent path (films rendered from the TEST film set, Harbor & Oak Realty) ----------
const MRV = __DATA__;
const MALL = MRV.mods.flatMap(m => m.L.map(l => ({...l, m}))), MTOTAL = MALL.length;
let mdone = new Set(), mseen = new Set();
try { const s = JSON.parse(localStorage.getItem('jsh-academy-mrv-done')||'null'); if (Array.isArray(s)) mdone = new Set(s); const q = JSON.parse(localStorage.getItem('jsh-academy-mrv-seen')||'null'); if (Array.isArray(q)) mseen = new Set(q); } catch(e){}
const msave = () => { try { localStorage.setItem('jsh-academy-mrv-done', JSON.stringify([...mdone])); localStorage.setItem('jsh-academy-mrv-seen', JSON.stringify([...mseen])); } catch(e){} };
const MSEQ = []; MRV.mods.forEach(m => { MSEQ.push('mrv-intro-'+m.id); m.L.forEach(l => MSEQ.push('mrv-l-'+l.id)); }); MSEQ.push('mrv-wrap');
const mTitle = h => h==='mrv-wrap' ? 'Wrap-up: congratulations' : h.startsWith('mrv-intro-') ? `Module ${MRV.mods.findIndex(m=>m.id===h.slice(10))+1} intro: ${MRV.mods.find(m=>m.id===h.slice(10)).t}` : MALL.find(l=>l.id===h.slice(6)).t;
const mModDone = m => mseen.has(m.id) && m.L.every(l => mdone.has(l.id));
function mNext(){ for (const m of MRV.mods) { if (!mseen.has(m.id)) return 'mrv-intro-'+m.id; const l = m.L.find(l=>!mdone.has(l.id)); if (l) return 'mrv-l-'+l.id; } return null; }
function mUp(cur){ const i = MSEQ.indexOf(cur), nx = MSEQ[i+1]; if (!nx) return {over:'', bar:''};
  return {over:`<div class="upnext" id="upnext" hidden><div><small>Up next</small><b>${esc(mTitle(nx))}</b><div class="rowx" style="justify-content:center"><button class="btn" data-next="${nx}">Play next</button><button class="btn ghost" id="replay">Replay</button></div></div></div>`,
          bar:`<div class="vbar"><span>${i+1} of ${MSEQ.length} in the path</span><button class="btn quiet" data-next="${nx}" style="padding:2px 0">Next: ${esc(mTitle(nx))} ▸</button></div>`}; }
const mVid = (key, up) => `<div class="vwrap"><video controls playsinline preload="none" poster="mrv-${key}.jpg" src="mrv-${key}.mp4" style="display:block;width:100%;aspect-ratio:16/9;background:#0b1015"></video>${up.over}</div>${up.bar}`;
function mrvPath(){
  const n = mNext(), complete = MRV.mods.every(mModDone);
  return `
  <div class="eyebrow">Vault Academy · MyRealtyVault campus</div>
  <h1 class="h1">Agent path</h1>
  <p class="lead">Run your whole business from your phone. Seven modules, in the order an agent's day and a deal unfold.</p>
  <div class="box starthere" style="margin-top:18px"><div class="player" style="border-radius:12px"><video controls playsinline preload="none" poster="mrv-overview.jpg" src="mrv-overview.mp4" style="display:block;width:100%;aspect-ratio:16/9;background:#0b1015"></video></div>
   <div><div class="eyebrow" style="color:var(--brass)">Start here · ${MRV.ov}</div><h2 style="font-family:var(--display);font-weight:400;font-size:28px;line-height:1.15;margin:6px 0 8px">MyRealtyVault for agents: every home, every deal, one vault</h2><p style="margin:0;color:var(--soft)">The whole app in about a minute: your day on one screen, clients, buyers, listings, showings, closings, documents and marketing. Optional, and it doesn't count toward completion.</p></div></div>
  <div class="rowx" style="margin:16px 0 22px"><div class="meter" style="flex:1;min-width:180px"><i style="width:${Math.round(100*mdone.size/MTOTAL)}%"></i></div><span style="color:var(--brass);font-variant-numeric:tabular-nums">${mdone.size} of ${MTOTAL}</span>${n?`<button class="btn" data-go="${n}">${mdone.size||mseen.size?'Resume':'Start'}</button>`:''}</div>
  ${complete ? `<div class="box cert" style="margin-bottom:18px"><div class="seal">J</div><div><b style="font-size:18px">MyRealtyVault Certified Agent</b><div style="color:var(--soft)">Every lesson complete. Self-study learners get a completion certificate. In an instructor-led class, your trainer signs you off.</div></div></div>` : ''}
  <div class="mods">${MRV.mods.map((m,i)=>`
   <section class="mod">
    <div class="art">${art(['door','people','spark','screens','mail','link','people'][i])}</div>
    <div class="body">
     <div class="rowx" style="justify-content:space-between"><span class="n">Module ${i+1}</span><span class="pill ${mModDone(m)?'good':''}">${(mseen.has(m.id)?1:0)+m.L.filter(l=>mdone.has(l.id)).length}/${m.L.length+1}</span></div>
     <h3>${esc(m.t)}</h3>
     <ul class="les"><li><button data-go="mrv-intro-${m.id}"><span class="chk ${mseen.has(m.id)?'done':(n==='mrv-intro-'+m.id?'next':'')}">${mseen.has(m.id)?'✓':''}</span><span class="t">Module intro</span><span class="d">${m.d}</span></button></li>${m.L.map(l=>`<li><button data-go="mrv-l-${l.id}"><span class="chk ${mdone.has(l.id)?'done':(n==='mrv-l-'+l.id?'next':'')}">${mdone.has(l.id)?'✓':''}</span><span class="t">${esc(l.t)}</span><span class="d">${l.d}</span></button></li>`).join('')}${i===MRV.mods.length-1?`<li><button data-go="mrv-wrap"><span class="chk" style="border-color:var(--good);color:var(--good);font-size:9px">▶</span><span class="t">Wrap-up: congratulations</span><span class="d">${MRV.wrap}</span></button></li>`:''}</ul>
    </div>
   </section>`).join('')}</div>
  <div class="box" style="margin-top:18px"><h2>How this campus is taught</h2>
   <div class="doors"><div><b>Self-study</b><span>An agent opens the campus from inside MyRealtyVault with the sign-in they already have, and works through it alone.</span></div>
   <div><b>Instructor-led</b><span>A brokerage's trainer, or a JSH instructor, runs the same path as a class and sees the group's progress.</span></div>
   <div><b>Completing a lesson</b><span>Watch it, try it in the app, then answer the quick check. Each module starts with its intro.</span></div>
   <div><b>Where the films come from</b><span>Every screen is the real app on the training brokerage, Harbor &amp; Oak Realty. The people and homes are made up.</span></div></div></div>`;
}
function mrvView(h){
  if (h==='mrv') return mrvPath();
  const crumbs = (mid, pill) => `<div class="crumbs"><button data-go="mrv">Agent path</button><span>/</span><span>${mid}</span>${pill}</div>`;
  if (h==='mrv-wrap') return `${crumbs('Module 7','<span class="pill good">Wrap-up</span>')}
  <h1 class="h1" style="font-size:clamp(28px,4vw,38px)">Congratulations</h1>
  <div class="lesson" style="margin-top:16px"><div class="player">${mVid('wrap',{over:'',bar:''})}<div class="note">Plays after the last lesson of the path.</div></div>
   <div class="side"><div class="box"><h2>Your business is in one vault</h2><p style="margin:0;color:var(--soft)">Tomorrow morning, open Today, tap Needs you, and clear your list. Everything else follows from there.</p></div>
    <div class="box"><h2>What's next for you</h2><p style="margin:0 0 12px;color:var(--soft)">${mdone.size>=MTOTAL ? 'Every lesson is complete.' : `You have ${MTOTAL-mdone.size} lessons left on the path.`}</p><button class="btn" data-go="mrv">Back to the path</button></div></div></div>`;
  if (h.startsWith('mrv-intro-')) { const mid = h.slice(10), i = MRV.mods.findIndex(m=>m.id===mid); if (i<0) return mrvPath(); const m = MRV.mods[i], first = m.L.find(l=>!mdone.has(l.id)) || m.L[0];
    return `${crumbs('Module '+(i+1), `<span class="pill ${mseen.has(m.id)?'good':''}">${mseen.has(m.id)?'Intro watched ✓':'Start here'}</span>`)}
  <h1 class="h1" style="font-size:clamp(28px,4vw,38px)">${esc(m.t)}</h1>
  <div class="lesson" style="margin-top:16px"><div class="player">${mVid('intro-'+m.id, mUp(h))}<div class="note">What this module is for and what you'll be able to do by the end. Watch this first: it's part of the module.</div></div>
   <div class="side"><div class="box"><h2>In this module</h2><ol class="steps">${m.L.map(l=>`<li>${esc(l.t)} <span style="color:var(--soft)">· ${l.d}</span></li>`).join('')}</ol></div>
    <div class="rowx"><button class="btn" data-next="mrv-l-${first.id}">Start: ${esc(first.t)}</button></div></div></div>`; }
  const l = MALL.find(x=>x.id===h.slice(6)); if (!l) return mrvPath(); const nx = MSEQ[MSEQ.indexOf(h)+1];
  return `${crumbs(esc(l.m.t),'')}
  <h1 class="h1" style="font-size:clamp(28px,4vw,38px)">${esc(l.t)}</h1>
  <div class="lesson" style="margin-top:16px"><div class="player">${mVid('l-'+l.id, mUp(h))}<div class="note">Recorded from MyRealtyVault itself, on the training brokerage. The phone on the left is the real screen; the window on the right zooms in on each step.</div></div>
   <div class="side"><div class="box"><h2>Steps</h2><ol class="steps">${l.s.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div>
    <div class="box"><h2>Try it</h2><p style="margin:0;color:var(--soft)">Open MyRealtyVault on your phone and do the same steps with one of your own clients or listings. Practice inside the Academy arrives for this campus next.</p></div>
    <div class="box" id="mquiz"><h2>Quick check</h2><div>${esc(l.q.q)}</div><div class="opts">${l.q.o.map((o,k)=>`<button data-mopt="${k}">${esc(o)}</button>`).join('')}</div><p id="mwhy" style="margin:10px 0 0;color:var(--soft)">${mdone.has(l.id)?'':''}</p></div>
    <div class="rowx">${mdone.has(l.id) ? `<span class="pill good" style="font-size:14px;padding:6px 14px">Completed ✓</span>` : `<span style="color:var(--soft);font-size:14px">Answer the quick check to complete this lesson.</span>`}<button class="btn quiet" data-go="${nx}">${nx==='mrv-wrap'?'Finish: watch the wrap-up':'Next: '+esc(mTitle(nx))}</button></div></div></div>`;
}
function mrvWire(h){
  const v = $('.vwrap video'); if (v && h.startsWith('mrv-intro-')) v.addEventListener('ended', () => { mseen.add(h.slice(10)); msave(); });
  const quiz = $('#mquiz'); if (!quiz) return; const l = MALL.find(x=>x.id===h.slice(6));
  quiz.onclick = e => { const b = e.target.closest('[data-mopt]'); if (!b) return; const k = +b.dataset.mopt, ok = k===l.q.a;
    quiz.querySelectorAll('[data-mopt]').forEach(x=>x.classList.remove('right','wrong')); b.classList.add(ok?'right':'wrong');
    $('#mwhy').textContent = ok ? 'Correct. ' + l.q.why : 'Not quite. Try again.';
    if (ok && !mdone.has(l.id)) { mdone.add(l.id); msave(); const y = window.scrollY; render(); window.scrollTo(0, y); const q2 = $('#mquiz'); if (q2) { q2.querySelectorAll('[data-mopt]')[k].classList.add('right'); $('#mwhy').textContent = 'Correct. ' + l.q.why + ' Lesson complete.'; } } };
}
'''.replace('__DATA__',json.dumps(data,ensure_ascii=False))
s=open('src.before-mrv.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)>=1,a[:60]; s=s.replace(a,b) if n==0 else s.replace(a,b,n)
rep("function render(){", JS+"\nfunction render(){")
rep("  if (who==='agent') h = 'home';","  if (who==='agent' && !h.startsWith('mrv')) h = 'home';")
rep("const v = h.startsWith('lesson-') ?","const v = h.startsWith('mrv') ? mrvView(h) : h.startsWith('lesson-') ?")
rep("  wireNext();\n","  wireNext(); if (h.startsWith('mrv')) mrvWire(h);\n")
rep("if (ch.startsWith('intro-')) { seen.add(ch.slice(6)); saveSeen(); }","if (ch.startsWith('intro-')) { seen.add(ch.slice(6)); saveSeen(); } if (ch.startsWith('mrv-intro-')) { mseen.add(ch.slice(10)); msave(); }")
rep("""<button class="camprow" disabled><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault<span class="soon">next</span></button>""","""<button class="camprow ${h.startsWith('mrv')?'on':''}" data-go="mrv"><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault</button>""")
rep("""<button class="camprow" data-go="home"><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault</button>`; return; }""","""<button class="camprow" data-go="mrv"><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault · Agent path</button>`; return; }""")
rep("""<button class="camp" disabled><span class="pill">Next</span><b>MyRealtyVault</b><p>Vault Academy for agents, brokers and homeowners. Opens in the app from the ? on every screen.</p><div class="foot"><span>about 25 lessons at launch</span>""","""<button class="camp" data-go="mrv"><span class="pill blue">Agent path · live</span><b>MyRealtyVault</b><p>Vault Academy for agents, brokers and homeowners. The Agent path is recorded; the homeowner path is next.</p><div class="foot"><span>${MTOTAL} lessons · 7 modules</span>""")
rep("""<h2>Agent path <span class="sample">opens with the MyRealtyVault launch</span></h2>
    <p style="margin:0;color:var(--soft)">About 25 lessons at launch, recorded the same way as the Workshop Platform campus: a two-minute overview, a short intro per module, then one task per lesson. Homeowners get their own, shorter path.</p></div>""","""<h2>Agent path</h2>
    <p style="margin:0 0 12px;color:var(--soft)">${MTOTAL} lessons in 7 modules, recorded the same way as the Workshop Platform campus: a one-minute overview, a short intro per module, then one task per lesson. Homeowners get their own, shorter path next.</p><button class="btn" data-go="mrv">Open the Agent path</button></div>""")
rep("const is = k => (k==='path' ?","const is = k => h.startsWith('mrv') ? '' : (k==='path' ?")
open('src.html','w').write(s); print('patched', len(s), [ (m['t'],m['d'],len(m['L'])) for m in mods])
