"""Adds the MyRealtyVault campus (Agent path + Homeowner path) to the Academy prototype source.
Reads src.before-mrv.html, writes src.html. Lesson data comes straight from the film scripts."""
import json, subprocess, sys, importlib
sys.path.insert(0,'/home/claude/mrvfilm'); OUT='/home/claude/mrvfilm/out'
def dur(f):
    s=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]).decode()); return f'{int(s//60)}:{int(s%60):02d}'
QA={'tour':("Where do you find your calendar, the marketing studio, vaults, reports and your profile?",["Office, in the bottom bar","The Needs you tile","The Buyers tile"],"Office holds everything behind the scenes."),
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
'results':("What period does Results cover?",["The last thirty days","The last year","Today only"],"Results shows the last thirty days and tells you what to do next."),
'h_tour':("How do you tell your vault what you are doing right now?",["Pick a focus: Buying, Selling or My home","Create a new account","Ask your agent to set it"],"The focus at the top changes the whole page to match."),
'h_check':("A checklist step doesn't apply to you. What do you tap?",["Skip","Delete my account","Sign out"],"Skip removes the step from your count. Later keeps it for another day."),
'h_afford':("What does How much can I afford give you?",["A price and monthly payment you can be comfortable with","A loan offer from a lender","An appraisal of a home"],"It is an estimate for planning. It is not a loan offer or an appraisal."),
'h_search':("How do you save a home you found on another site?",["Copy its link and paste it into Home search","Email it to MyRealtyVault","Take a screenshot"],"Paste the link and the home lands in your saved homes, ready to rate."),
'h_hood':("What does Check a neighborhood tell you about an address?",["Flood zone, nearby public schools and what to ask","The seller's phone number","Who lives next door"],"It shows flood risk, insurance notes, nearby public schools and state buying facts."),
'h_docs':("Who can see a document right after you add it?",["Only you, until you choose to share it","Your lender","Every agent nearby"],"Documents are private to you. You choose if and when anyone else sees them."),
'h_lender':("What is true of a link you send to a lender?",["It is view-only, it expires, and you can turn it off","It lets them edit your documents","It never expires"],"You pick how long it lasts, see each time it is opened, and can turn it off."),
'h_sell':("What does What will I walk away with take off the sale price?",["Commission, title costs and your mortgage payoff","Only the commission","Nothing"],"It subtracts commission, estimated title and settlement costs, and your payoff."),
'h_own':("What do you enter to add the home you own?",["The address, when you bought it and what you paid","Your lender's password","Your neighbor's address"],"Address, purchase date and price start your home's history."),
'h_ask':("What does Ask MRV use to answer you?",["Your search, your saved homes and your notes","Other people's vaults","Nothing about you"],"It knows your search and your homes, and tells you what it would do and why."),
'h_cal':("What shows up on My calendar besides the plans you add?",["Showings your agent books and deadlines that are set","Your neighbors' plans","Nothing else"],"Your own plans, your agent's showings and deadlines all land on one calendar."),
'h_agent':("When you add your agent, who decides what they can see?",["You do, with three checkboxes","The agent","MyRealtyVault"],"You choose: saved homes and notes, your search, and documents you mark shared.")}
QA.update({'a_msg':("What must be on file before MyRealtyVault sends a text for you?",["The client's agreement to receive texts","A signed listing agreement","A pre-approval letter"],"Texts through the platform need the client's consent recorded first. You can always send from your own phone and log it."),
'a_suggest':("You add a home with Suggest a home. What is its state?",["Your pick, not sent yet","Sent to the buyer","Under contract"],"It waits in Matches as your pick until you send the list to your buyer."),
'a_offer':("What happens when you tap Save the draft offer?",["The offer is saved as a draft and nothing is sent","The offer is emailed to the seller","The buyer is charged earnest money"],"A draft is only for you. You send it later with Send the offer."),
'a_reports':("What does a deal need before it counts toward projected commission?",["Its numbers: price and your percent, or a flat amount","A photo","Ten showings"],"Tap the deal, add its numbers and save."),
'a_card':("Where does the name on Your card appear?",["It signs your letters and emails","Only on your phone","Nowhere"],"Your name signs letters and emails, and your social links go at the bottom of every marketing email."),
'a_look':("Who else sees the accent color you pick?",["Your clients, in their vaults","Nobody","Other brokerages"],"Your clients' vaults use the same accent. White or dark is set per device."),
'a_connect':("How do your showings get onto your own calendar?",["Copy the calendar link once and subscribe to it","Type each one in by hand","They cannot"],"Subscribe once in Outlook, Google or Apple. New items can take a few hours to appear."),
'a_bench':("Who sees the partners on your bench?",["Every client you serve, on their team","Only you","Every agent in town"],"Your lender, title company and inspector appear on each client's team, with your name on it."),
'a_help':("Where do feature ideas and bug reports go?",["Straight to the MyRealtyVault team","Nowhere","To your clients"],"Help answers how-to questions, and passes ideas and bugs to the team.")})
def load(mods_list, mods_t, pre):
    FILMS={}
    for mod in mods_list: FILMS.update(importlib.import_module(mod).FILMS)
    mods=[{'id':f'm{i}','t':mods_t[i],'d':dur(f"{OUT}/MRV_{pre}Module{i}_Intro.mp4"),'L':[]} for i in range(1,len(mods_t))]; k=0
    for fid,F in FILMS.items():
        if F.get('kind','lesson')!='lesson': continue
        q,o,why=QA[fid]; a=k%3; k+=1; o2=o[1:]; o2.insert(a,o[0])
        mods[F['m']-1]['L'].append({'id':fid,'t':F['title'],'d':dur(f"{OUT}/MRV_{pre}{F['file']}.mp4"),'s':[b['vo'] for b in F['beats']],'q':{'q':q,'o':o2,'a':a,'why':why}})
    ov=[f for f,F in FILMS.items() if F.get('kind')=='overview'][0]; wr=[f for f,F in FILMS.items() if F.get('kind')=='wrap'][0]
    return {'mods':mods,'ov':dur(f"{OUT}/MRV_{pre}{FILMS[ov]['file']}.mp4"),'wrap':dur(f"{OUT}/MRV_{pre}{FILMS[wr]['file']}.mp4")}
A=load(['films','films_agent2'],['','Your day on one screen','Clients','Buyers','Listings','Showings and calendar','Closings and documents','Marketing','Your office'],'')
A.update(key='mrv',name='Agent path',lead="Run your whole business from your phone. Eight modules, in the order an agent's day and a deal unfold.",ovT='MyRealtyVault for agents: every home, every deal, one vault',ovB='The whole app in about a minute: your day on one screen, clients, buyers, listings, showings, closings, documents and marketing.',cert='MyRealtyVault Certified Agent',wrapH='Your business is in one vault',wrapP='Tomorrow morning, open Today, tap Needs you, and clear your list. Everything else follows from there.',tryit='Open MyRealtyVault on your phone and do the same steps with one of your own clients or listings.',who='the training brokerage, Harbor &amp; Oak Realty',arts=['door','people','spark','screens','mail','link','people','door'])
H=load(['films_home'],['','Your vault','Buying a home','Your documents','Selling and owning','Help, and your agent'],'Home_')
H.update(key='mrh',name='Homeowner path',lead='Your homes, your search and your documents in one vault, for life. Five short modules; take only the ones that fit what you are doing.',ovT='MyRealtyVault for homeowners: one vault, for life',ovB='The whole vault in under a minute: your checklist, buying tools, documents you share safely, selling and owning, and help whenever you want it.',cert='MyRealtyVault Homeowner path complete',wrapH='Your vault is yours for life',wrapP='Open your vault, look at your next step, and tap Do it.',tryit='Open your vault on your phone and do the same steps with your own search, homes or documents.',who='a training homeowner, Jordan Avery',arts=['door','spark','mail','screens','people'])
JS=r'''
// ---------- MyRealtyVault campus · Agent path and Homeowner path (films rendered from the TEST film set) ----------
const MRVP = __DATA__;
const mrvOf = h => MRVP.find(P => h===P.key || h.startsWith(P.key+'-'));
MRVP.forEach(P => { P.all = P.mods.flatMap(m => m.L.map(l => ({...l, m}))); P.total = P.all.length; P.done = new Set(); P.seen = new Set();
  try { const s = JSON.parse(localStorage.getItem('jsh-academy-'+P.key+'-done')||'null'); if (Array.isArray(s)) P.done = new Set(s); const q = JSON.parse(localStorage.getItem('jsh-academy-'+P.key+'-seen')||'null'); if (Array.isArray(q)) P.seen = new Set(q); } catch(e){}
  P.save = () => { try { localStorage.setItem('jsh-academy-'+P.key+'-done', JSON.stringify([...P.done])); localStorage.setItem('jsh-academy-'+P.key+'-seen', JSON.stringify([...P.seen])); } catch(e){} };
  P.seq = []; P.mods.forEach(m => { P.seq.push(P.key+'-intro-'+m.id); m.L.forEach(l => P.seq.push(P.key+'-l-'+l.id)); }); P.seq.push(P.key+'-wrap');
  P.title = h => h===P.key+'-wrap' ? 'Wrap-up: congratulations' : h.startsWith(P.key+'-intro-') ? `Module ${P.mods.findIndex(m=>m.id===h.slice(P.key.length+7))+1} intro: ${P.mods.find(m=>m.id===h.slice(P.key.length+7)).t}` : P.all.find(l=>l.id===h.slice(P.key.length+3)).t;
  P.modDone = m => P.seen.has(m.id) && m.L.every(l => P.done.has(l.id));
  P.next = () => { for (const m of P.mods) { if (!P.seen.has(m.id)) return P.key+'-intro-'+m.id; const l = m.L.find(l=>!P.done.has(l.id)); if (l) return P.key+'-l-'+l.id; } return null; };
  P.up = cur => { const i = P.seq.indexOf(cur), nx = P.seq[i+1]; if (!nx) return {over:'', bar:''};
    return {over:`<div class="upnext" id="upnext" hidden><div><small>Up next</small><b>${esc(P.title(nx))}</b><div class="rowx" style="justify-content:center"><button class="btn" data-next="${nx}">Play next</button><button class="btn ghost" id="replay">Replay</button></div></div></div>`,
            bar:`<div class="vbar"><span>${i+1} of ${P.seq.length} in the path</span><button class="btn quiet" data-next="${nx}" style="padding:2px 0">Next: ${esc(P.title(nx))} ▸</button></div>`}; };
  P.vid = (key, up) => `<div class="vwrap"><video controls playsinline preload="none" poster="${P.key}-${key}.jpg" src="${P.key}-${key}.mp4" style="display:block;width:100%;aspect-ratio:16/9;background:#0b1015"></video>${up.over}</div>${up.bar}`; });
const MTOTAL = MRVP.reduce((a,P)=>a+P.total,0);
function mrvPath(P){
  const n = P.next(), complete = P.mods.every(P.modDone);
  return `
  <div class="eyebrow">Vault Academy · MyRealtyVault campus</div>
  <h1 class="h1">${P.name}</h1>
  <div class="tabs2" role="tablist" style="margin:10px 0 6px;max-width:420px">${MRVP.map(X=>`<button role="tab" data-go="${X.key}" class="${X===P?'on':''}">${X.name}</button>`).join('')}</div>
  <p class="lead">${P.lead}</p>
  <div class="box starthere" style="margin-top:18px"><div class="player" style="border-radius:12px"><video controls playsinline preload="none" poster="${P.key}-overview.jpg" src="${P.key}-overview.mp4" style="display:block;width:100%;aspect-ratio:16/9;background:#0b1015"></video></div>
   <div><div class="eyebrow" style="color:var(--brass)">Start here · ${P.ov}</div><h2 style="font-family:var(--display);font-weight:400;font-size:28px;line-height:1.15;margin:6px 0 8px">${P.ovT}</h2><p style="margin:0;color:var(--soft)">${P.ovB} Optional, and it doesn't count toward completion.</p></div></div>
  <div class="rowx" style="margin:16px 0 22px"><div class="meter" style="flex:1;min-width:180px"><i style="width:${Math.round(100*P.done.size/P.total)}%"></i></div><span style="color:var(--brass);font-variant-numeric:tabular-nums">${P.done.size} of ${P.total}</span>${n?`<button class="btn" data-go="${n}">${P.done.size||P.seen.size?'Resume':'Start'}</button>`:''}</div>
  ${complete ? `<div class="box cert" style="margin-bottom:18px"><div class="seal">J</div><div><b style="font-size:18px">${P.cert}</b><div style="color:var(--soft)">Every lesson complete. Self-study learners get a completion certificate. In an instructor-led class, the trainer signs learners off.</div></div></div>` : ''}
  <div class="mods">${P.mods.map((m,i)=>`
   <section class="mod">
    <div class="art">${art(P.arts[i])}</div>
    <div class="body">
     <div class="rowx" style="justify-content:space-between"><span class="n">Module ${i+1}</span><span class="pill ${P.modDone(m)?'good':''}">${(P.seen.has(m.id)?1:0)+m.L.filter(l=>P.done.has(l.id)).length}/${m.L.length+1}</span></div>
     <h3>${esc(m.t)}</h3>
     <ul class="les"><li><button data-go="${P.key}-intro-${m.id}"><span class="chk ${P.seen.has(m.id)?'done':(n===P.key+'-intro-'+m.id?'next':'')}">${P.seen.has(m.id)?'✓':''}</span><span class="t">Module intro</span><span class="d">${m.d}</span></button></li>${m.L.map(l=>`<li><button data-go="${P.key}-l-${l.id}"><span class="chk ${P.done.has(l.id)?'done':(n===P.key+'-l-'+l.id?'next':'')}">${P.done.has(l.id)?'✓':''}</span><span class="t">${esc(l.t)}</span><span class="d">${l.d}</span></button></li>`).join('')}${i===P.mods.length-1?`<li><button data-go="${P.key}-wrap"><span class="chk" style="border-color:var(--good);color:var(--good);font-size:9px">▶</span><span class="t">Wrap-up: congratulations</span><span class="d">${P.wrap}</span></button></li>`:''}</ul>
    </div>
   </section>`).join('')}</div>
  <div class="box" style="margin-top:18px"><h2>How this campus is taught</h2>
   <div class="doors"><div><b>Self-study</b><span>Agents and homeowners open the campus from inside MyRealtyVault with the sign-in they already have. Homeowners see only the Homeowner path.</span></div>
   <div><b>Instructor-led</b><span>A brokerage's trainer, or a JSH instructor, runs the Agent path as a class and sees the group's progress.</span></div>
   <div><b>Completing a lesson</b><span>Watch it, try it in the app, then answer the quick check. Each module starts with its intro.</span></div>
   <div><b>Where the films come from</b><span>Every screen is the real app, signed in as ${P.who}. The people and homes are made up.</span></div></div></div>`;
}
function mrvView(h){
  const P = mrvOf(h); if (!P) return home(); const K = P.key;
  if (h===K) return mrvPath(P);
  const crumbs = (mid, pill) => `<div class="crumbs"><button data-go="${K}">${P.name}</button><span>/</span><span>${mid}</span>${pill}</div>`;
  if (h===K+'-wrap') return `${crumbs('Module '+P.mods.length,'<span class="pill good">Wrap-up</span>')}
  <h1 class="h1" style="font-size:clamp(28px,4vw,38px)">Congratulations</h1>
  <div class="lesson" style="margin-top:16px"><div class="player">${P.vid('wrap',{over:'',bar:''})}<div class="note">Plays after the last lesson of the path.</div></div>
   <div class="side"><div class="box"><h2>${P.wrapH}</h2><p style="margin:0;color:var(--soft)">${P.wrapP}</p></div>
    <div class="box"><h2>What's next for you</h2><p style="margin:0 0 12px;color:var(--soft)">${P.done.size>=P.total ? 'Every lesson is complete.' : `You have ${P.total-P.done.size} lessons left on the path.`}</p><button class="btn" data-go="${K}">Back to the path</button></div></div></div>`;
  if (h.startsWith(K+'-intro-')) { const mid = h.slice(K.length+7), i = P.mods.findIndex(m=>m.id===mid); if (i<0) return mrvPath(P); const m = P.mods[i], first = m.L.find(l=>!P.done.has(l.id)) || m.L[0];
    return `${crumbs('Module '+(i+1), `<span class="pill ${P.seen.has(m.id)?'good':''}">${P.seen.has(m.id)?'Intro watched ✓':'Start here'}</span>`)}
  <h1 class="h1" style="font-size:clamp(28px,4vw,38px)">${esc(m.t)}</h1>
  <div class="lesson" style="margin-top:16px"><div class="player">${P.vid('intro-'+m.id, P.up(h))}<div class="note">What this module is for and what you'll be able to do by the end. Watch this first: it's part of the module.</div></div>
   <div class="side"><div class="box"><h2>In this module</h2><ol class="steps">${m.L.map(l=>`<li>${esc(l.t)} <span style="color:var(--soft)">· ${l.d}</span></li>`).join('')}</ol></div>
    <div class="rowx"><button class="btn" data-next="${K}-l-${first.id}">Start: ${esc(first.t)}</button></div></div></div>`; }
  const l = P.all.find(x=>x.id===h.slice(K.length+3)); if (!l) return mrvPath(P); const nx = P.seq[P.seq.indexOf(h)+1];
  return `${crumbs(esc(l.m.t),'')}
  <h1 class="h1" style="font-size:clamp(28px,4vw,38px)">${esc(l.t)}</h1>
  <div class="lesson" style="margin-top:16px"><div class="player">${P.vid('l-'+l.id, P.up(h))}<div class="note">Recorded from MyRealtyVault itself. The phone on the left is the real screen; the window on the right zooms in on each step.</div></div>
   <div class="side"><div class="box"><h2>Steps</h2><ol class="steps">${l.s.map(s=>`<li>${esc(s)}</li>`).join('')}</ol></div>
    <div class="box"><h2>Try it</h2><p style="margin:0;color:var(--soft)">${P.tryit} Practice inside the Academy arrives for this campus next.</p></div>
    <div class="box" id="mquiz"><h2>Quick check</h2><div>${esc(l.q.q)}</div><div class="opts">${l.q.o.map((o,k)=>`<button data-mopt="${k}">${esc(o)}</button>`).join('')}</div><p id="mwhy" style="margin:10px 0 0;color:var(--soft)"></p></div>
    <div class="rowx">${P.done.has(l.id) ? `<span class="pill good" style="font-size:14px;padding:6px 14px">Completed ✓</span>` : `<span style="color:var(--soft);font-size:14px">Answer the quick check to complete this lesson.</span>`}<button class="btn quiet" data-go="${nx}">${nx===K+'-wrap'?'Finish: watch the wrap-up':'Next: '+esc(P.title(nx))}</button></div></div></div>`;
}
function mrvSeen(h){ const P = mrvOf(h); if (P && h.startsWith(P.key+'-intro-')) { P.seen.add(h.slice(P.key.length+7)); P.save(); } }
function mrvWire(h){
  const P = mrvOf(h); if (!P) return;
  const v = $('.vwrap video'); if (v) v.addEventListener('ended', () => mrvSeen(h));
  const quiz = $('#mquiz'); if (!quiz) return; const l = P.all.find(x=>x.id===h.slice(P.key.length+3));
  quiz.onclick = e => { const b = e.target.closest('[data-mopt]'); if (!b) return; const k = +b.dataset.mopt, ok = k===l.q.a;
    quiz.querySelectorAll('[data-mopt]').forEach(x=>x.classList.remove('right','wrong')); b.classList.add(ok?'right':'wrong');
    $('#mwhy').textContent = ok ? 'Correct. ' + l.q.why : 'Not quite. Try again.';
    if (ok && !P.done.has(l.id)) { P.done.add(l.id); P.save(); const y = window.scrollY; render(); window.scrollTo(0, y); const q2 = $('#mquiz'); if (q2) { q2.querySelectorAll('[data-mopt]')[k].classList.add('right'); $('#mwhy').textContent = 'Correct. ' + l.q.why + ' Lesson complete.'; } } };
}
'''.replace('__DATA__',json.dumps([A,H],ensure_ascii=False))
s=open('src.before-mrv.html').read()
def rep(a,b):
    global s
    assert s.count(a)>=1,a[:70]; s=s.replace(a,b)
rep("function render(){", JS+"\nfunction render(){")
rep("  if (who==='agent') h = 'home';","  if (who==='agent' && !mrvOf(h)) h = 'home';")
rep("const v = h.startsWith('lesson-') ?","const v = mrvOf(h) ? mrvView(h) : h.startsWith('lesson-') ?")
rep("  wireNext();\n","  wireNext(); if (mrvOf(h)) mrvWire(h);\n")
rep("if (ch.startsWith('intro-')) { seen.add(ch.slice(6)); saveSeen(); }","if (ch.startsWith('intro-')) { seen.add(ch.slice(6)); saveSeen(); } mrvSeen(ch);")
rep("""<button class="camprow" disabled><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault<span class="soon">next</span></button>""","""<button class="camprow ${mrvOf(h)?'on':''}" data-go="mrv"><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault</button>""")
rep("""<button class="camprow" data-go="home"><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault</button>`; return; }""","""<button class="camprow" data-go="mrv"><span class="dot" style="background:#4f9a6a"></span>MyRealtyVault · Agent path</button>`; return; }""")
rep("""<button class="camp" disabled><span class="pill">Next</span><b>MyRealtyVault</b><p>Vault Academy for agents, brokers and homeowners. Opens in the app from the ? on every screen.</p><div class="foot"><span>about 25 lessons at launch</span>""","""<button class="camp" data-go="mrv"><span class="pill blue">Agent + Homeowner paths · live</span><b>MyRealtyVault</b><p>Vault Academy for agents, brokers and homeowners. Two paths recorded: Agent and Homeowner.</p><div class="foot"><span>${MTOTAL} lessons · 2 paths</span>""")
rep("""<h2>Agent path <span class="sample">opens with the MyRealtyVault launch</span></h2>
    <p style="margin:0;color:var(--soft)">About 25 lessons at launch, recorded the same way as the Workshop Platform campus: a two-minute overview, a short intro per module, then one task per lesson. Homeowners get their own, shorter path.</p></div>""","""<h2>Agent path</h2>
    <p style="margin:0 0 12px;color:var(--soft)">${MRVP[0].total} lessons in ${MRVP[0].mods.length} modules, recorded the same way as the Workshop Platform campus: a one-minute overview, a short intro per module, then one task per lesson. Homeowners get their own, shorter path of ${MRVP[1].total} lessons.</p><button class="btn" data-go="mrv">Open the Agent path</button></div>""")
rep("const is = k => (k==='path' ?","const is = k => mrvOf(h) ? '' : (k==='path' ?")
open('src.html','w').write(s); print('patched', len(s), [(P['name'],P['ov'],sum(len(m['L']) for m in P['mods'])) for P in (A,H)])
