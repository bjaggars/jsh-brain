"""Drive the Demo engagement on the live Workshop Platform as the film-set staff account (founder-approved 11/12).
usage: python3 live.py '<json list of ops>'   ops: ["answer",prefix,text] ["idk",prefix] ["idk_yes",prefix] ["idk_assume",prefix]
["click",button name,(nth)] ["text",visible text] ["tab",name] ["shot",name] ["full",name] ["scroll",text] ["fill",aria/placeholder,text] ["wait",sec] ["dump",css]"""
import asyncio, json, sys, urllib.request
from playwright.async_api import async_playwright
URL='https://comtcpdhainyrjazztpj.supabase.co'; SITE='https://workshop.jshinnovations.com'; DEMO='5eed0000-0000-4000-8000-000000000001'
ANON=__import__('re').search(r"eyJ[A-Za-z0-9_.-]+", open('login.py').read()).group(0)
def login():
    req=urllib.request.Request(URL+'/auth/v1/token?grant_type=password', data=json.dumps({'email':'filmset.academy@jshinnovations.com','password':open('.pw').read()}).encode(), headers={'apikey':ANON,'content-type':'application/json'})
    return json.loads(urllib.request.urlopen(req).read())
def rest(sess, path):
    req=urllib.request.Request(URL+'/rest/v1/'+path, headers={'apikey':ANON,'authorization':'Bearer '+sess['access_token']})
    return json.loads(urllib.request.urlopen(req).read())
async def main(ops):
    sess=login()
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1440,'height':810}, device_scale_factor=3, timezone_id='America/Chicago')
        pg=await ctx.new_page(); await pg.goto(SITE+'/')
        await pg.evaluate("s=>localStorage.setItem('sb-comtcpdhainyrjazztpj-auth-token', s)", json.dumps(sess))
        await pg.goto(SITE+'/?e='+DEMO); await pg.wait_for_timeout(5000)
        async def idle(maxs=900):
            pr=pg.locator('.progress')
            try: await pr.first.wait_for(state='visible', timeout=4000)
            except Exception: pass
            for _ in range(maxs):
                if not await pr.count(): break
                await pg.wait_for_timeout(1000)
            await pg.wait_for_timeout(1500)
            w=pg.locator('p.warn')
            if await w.count(): print('WARN:', (await w.first.inner_text())[:300])
        async def hidefoot(): await pg.evaluate("()=>{for(const e of document.querySelectorAll('footer')) if(/functions:/.test(e.textContent)) e.style.visibility='hidden'}")
        def card(prefix): return pg.locator('li.qcard', has_text=prefix).first
        for op in ops:
            k=op[0]
            try:
                if k=='answer':
                    c=card(op[1]); await c.scroll_into_view_if_needed(); await c.locator('textarea').fill(op[2]); await c.get_by_role('button', name='Save answer').click(); await idle()
                    n=pg.locator('.note').first; print('ANSWERED', op[1][:40], '->', (await n.inner_text())[-160:].replace('\n',' ') if await n.count() else '')
                elif k=='idk': c=card(op[1]); await c.scroll_into_view_if_needed(); await c.get_by_role('button', name="I don't know").click(); await pg.wait_for_timeout(700); print('OFFER', (await c.inner_text())[:400].replace('\n',' | '))
                elif k=='idk_yes': c=card(op[1]); await c.get_by_role('button', name="Yes, that's us").click(); await idle(); print('YES', op[1][:40])
                elif k=='idk_assume': c=card(op[1]); await c.get_by_role('button', name='Not sure, assume it for now').click(); await idle(); print('ASSUMED', op[1][:40])
                elif k=='click':
                    l=pg.get_by_role('button', name=op[1], exact=True).nth(op[2] if len(op)>2 else 0); await l.scroll_into_view_if_needed(); await l.click(); await idle(); print('CLICKED', op[1])
                elif k=='text': l=pg.get_by_text(op[1], exact=True).first; await l.scroll_into_view_if_needed(); await l.click(); await pg.wait_for_timeout(1200); print('TEXT', op[1])
                elif k=='tab': await pg.get_by_role('tab', name=op[1]).click(); await pg.wait_for_timeout(800)
                elif k=='scroll': await pg.get_by_text(op[1]).first.evaluate("(e,o)=>window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-o)", op[2] if len(op)>2 else 200); await pg.wait_for_timeout(500)
                elif k=='shot': await hidefoot(); await pg.screenshot(path=f'cap/p2/{op[1]}.jpg', quality=93); print('SHOT', op[1])
                elif k=='full': await hidefoot(); await pg.screenshot(path=f'cap/p2/{op[1]}.jpg', quality=90, full_page=True); print('FULL', op[1])
                elif k=='fill': l=pg.get_by_label(op[1]).first if not op[1].startswith('ph:') else pg.get_by_placeholder(op[1][3:]).first; await l.fill(op[2])
                elif k=='xy': await pg.mouse.click(op[1],op[2]); await pg.wait_for_timeout(900); print('XY',op[1:])
                elif k=='label': await pg.locator('label', has_text=op[1]).nth(op[2] if len(op)>2 else 0).click(); await pg.wait_for_timeout(300)
                elif k=='wait': await pg.wait_for_timeout(int(op[1]*1000))
                elif k=='dump': print('DUMP', (await pg.locator(op[1]).first.inner_text())[: (op[2] if len(op)>2 else 3000)])
                elif k=='box':
                    l=pg.get_by_text(op[2]).first if len(op)<4 else pg.locator(op[3]).first; bb=await l.bounding_box(); print('BOX', op[1], json.dumps([round(bb[x],1) for x in ('x','y','width','height')]) if bb else None)
            except Exception as e: print('ERR', op[:2], str(e)[:300]); break
        qs=rest(sess, f'questions?engagement_id=eq.{DEMO}&select=prompt,status,target_chamber,suggested_default,gap,phase&order=created_at')
        opn=[q for q in qs if q['status'] in('asked','pending') and q['gap']!='closing_comments']
        print('--- questions', len(qs), 'open', len(opn))
        for q in opn: print(f"[{q['target_chamber']}] {q['prompt']}  || DEFAULT: {q['suggested_default']}")
        print('--- top:', (await pg.locator('main').inner_text())[:0])
        await b.close()
asyncio.run(main(json.load(open(sys.argv[1])) if len(sys.argv)>1 else []))
