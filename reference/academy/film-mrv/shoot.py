"""MRV film-set driver (phone). Local Vite preview against the TEST database, signed in as the film-set agent (Ava Marshall,
Harbor & Oak Realty). TEST ONLY. Netlify functions are stubbed (nothing is emailed or texted) unless named in ALLOW_FN, which
proxies that one function to the TEST site. A real name that exists in the film-set tenant is masked on screen.
usage: python3 shoot.py ops.json   ops: ["goto",path] ["tap",text,(nth)] ["tapx",text] (substring) ["btn",name,(nth)] ["css",selector,(nth)]
["fill",target,text] target = "ph:<placeholder>" | "lb:<label>" | css   ["select",css,label] ["wheel",dy] ["into",text|css:sel]
["shot",name,{key:locator}] locator = text | "css:..." | "btn:..." | "ph:..."  ["dump",(n)] ["wait",s] ["js",code] ["key",key]"""
import asyncio, json, sys, os, re
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
BASE='http://127.0.0.1:5173'; TEST='https://myrealtyvault.app'; ALLOW=set(filter(None,os.environ.get('ALLOW_FN','').split(',')))
MASK=[('Brice Jaggars','Jordan Avery'),('kim@jaggars.com','jordan.avery@example.com'),('Brice','Jordan'),('Jaggars','Avery'),('Synovus','Gulf Coast Lending')]
CAP=os.environ.get('CAP','cap'); NOW=os.environ.get('NOW','2026-11-12T08:40:00')
async def main(ops):
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context(storage_state=os.environ.get('STATE','state.json'), viewport={'width':443,'height':960}, device_scale_factor=3, is_mobile=True, has_touch=True, user_agent=UA, timezone_id='America/New_York', locale='en-US')
        pg=await ctx.new_page(); log=[]
        if NOW!='real': await pg.clock.install(time=NOW)
        async def rest(r):
            q=r.request
            try:
                resp=await r.fetch()
                if q.method!='GET': log.append((q.method,q.url.split('/rest/v1/')[1][:60],resp.status))
                body=await resp.text()
                for a,c in MASK: body=body.replace(a,c)
                await r.fulfill(response=resp, body=body)
            except Exception as e:
                try: await r.continue_()
                except Exception: pass
        async def fn(r):
            name=r.request.url.split('/functions/')[1].split('?')[0]
            if name in ALLOW:
                import urllib.request
                q=r.request; hd={k:v for k,v in q.headers.items() if k.lower() in('authorization','content-type','apikey','accept')}
                def go():
                    rq=urllib.request.Request(TEST+'/.netlify/functions/'+q.url.split('/functions/')[1],method=q.method,data=q.post_data_buffer,headers=hd)
                    try:
                        x=urllib.request.urlopen(rq,timeout=120); return x.status,x.read().decode(),x.headers.get('content-type','application/json')
                    except urllib.error.HTTPError as e: return e.code,e.read().decode(),'application/json'
                st,body,ct=await asyncio.to_thread(go)
                for a,c in MASK: body=body.replace(a,c)
                log.append(('FN-LIVE',name,st)); return await r.fulfill(status=st, content_type=ct, body=body)
            log.append(('FN-STUB',name,r.request.method)); await r.fulfill(status=200, content_type='application/json', body=os.environ.get('FN_BODY','{"ok":true}'))
        await pg.route('**/rest/v1/**', rest); await pg.route('**/.netlify/functions/**', fn)
        def loc(s):
            if s.startswith('css:'): return pg.locator(s[4:]).locator('visible=true')
            if s.startswith('btn:'): return pg.get_by_role('button', name=s[4:], exact=True).locator('visible=true')
            if s.startswith('ph:'): return pg.get_by_placeholder(s[3:]).locator('visible=true')
            if s.startswith('lb:'): return pg.get_by_label(s[3:]).locator('visible=true')
            if s.startswith('i:'): return pg.get_by_text(re.compile('^\\s*'+re.escape(s[2:])+'\\s*$', re.I)).locator('visible=true')
            if s.startswith('~'): return pg.get_by_text(s[1:]).locator('visible=true')
            return pg.get_by_text(s, exact=True).locator('visible=true')
        def nth(l,op,i=2): return l.nth(op[i]) if len(op)>i and isinstance(op[i],int) else l.first
        for op in ops:
            k=op[0]
            try:
                if k=='goto': await pg.goto(BASE+op[1]); await pg.wait_for_timeout(4500)
                elif k=='tap': await nth(loc(op[1]),op).click(timeout=7000); await pg.wait_for_timeout(1800)
                elif k=='tapx': await nth(loc('~'+op[1]),op).click(timeout=7000); await pg.wait_for_timeout(1800)
                elif k=='btn': await nth(loc('btn:'+op[1]),op).click(timeout=7000); await pg.wait_for_timeout(1800)
                elif k=='css': await nth(loc('css:'+op[1]),op).click(timeout=7000); await pg.wait_for_timeout(1800)
                elif k=='fill': await nth(loc(op[1] if op[1][:3] in('ph:','lb:') else 'css:'+op[1]),op,3).fill(op[2]); await pg.wait_for_timeout(250)
                elif k=='type': await loc(op[1] if op[1][:3] in('ph:','lb:') else 'css:'+op[1]).first.press_sequentially(op[2], delay=20); await pg.wait_for_timeout(600)
                elif k=='select': await loc('css:'+op[1]).first.select_option(**({'index':op[2]} if isinstance(op[2],int) else {'label':op[2]})); await pg.wait_for_timeout(500)
                elif k=='wheel': await pg.mouse.move(220,500); await pg.mouse.wheel(0,op[1]); await pg.wait_for_timeout(700)
                elif k=='into': await loc(op[1]).first.evaluate("(e,o)=>e.scrollIntoView({block:o})", op[2] if len(op)>2 else 'center'); await pg.wait_for_timeout(600)
                elif k=='file': await pg.locator(op[1]).first.set_input_files(op[2]); await pg.wait_for_timeout(1500)
                elif k=='xy': await pg.touchscreen.tap(op[1],op[2]); await pg.wait_for_timeout(1500)
                elif k=='key': await pg.keyboard.press(op[1]); await pg.wait_for_timeout(800)
                elif k=='wait': await pg.wait_for_timeout(int(op[1]*1000))
                elif k=='js': print('JS', json.dumps(await pg.evaluate(op[1]))[:3000])
                elif k=='shot':
                    await pg.evaluate("""()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(n.nodeValue.includes('127.0.0.1:5173'))n.nodeValue=n.nodeValue.replace(/https?:..127.0.0.1:5173/g,'myrealtyvault.app').replace(/127.0.0.1:5173/g,'myrealtyvault.app')}}""")
                    await pg.screenshot(path=f'{CAP}/{op[1]}.jpg', quality=92, type='jpeg'); bx={}
                    for key,s in (op[2] if len(op)>2 else {}).items():
                        l=loc(s[0]).nth(s[1]) if isinstance(s,list) else loc(s).first
                        bb=await l.bounding_box() if await l.count() else None
                        if bb: bx[key]=[round(bb['x'],1),round(bb['y'],1),round(bb['width'],1),round(bb['height'],1)]
                        else: print('  NOBOX',op[1],key)
                    json.dump(bx,open(f'{CAP}/{op[1]}.json','w')); print('SHOT',op[1],bx)
                elif k=='dump':
                    t=await pg.locator('body').inner_text(); print('DUMP',' | '.join(x.strip() for x in t.split('\n') if x.strip())[(op[1] if len(op)>1 and op[1]<0 else 0):(op[1] if len(op)>1 and op[1]>0 else (None if len(op)>1 else 1500))])
                    els=await pg.evaluate("""()=>[...document.querySelectorAll('input,textarea,select,button')].filter(e=>e.offsetParent&&e.getBoundingClientRect().top<960&&e.getBoundingClientRect().bottom>0).map(e=>e.tagName[0]+':'+(e.placeholder||e.getAttribute('aria-label')||e.name||e.textContent||'').trim().slice(0,28)+(e.type&&e.tagName=='INPUT'?'('+e.type+')':''))""")
                    print('  ELS',' ¦ '.join(els)[-900:])
            except Exception as e: print('ERR',op[:2],str(e)[:240]); break
        print('URL',pg.url.replace(BASE,''),'LOG',log[-14:]); await ctx.storage_state(path=os.environ.get('STATE','state.json')); await b.close()
asyncio.run(main(json.load(open(sys.argv[1]))))
