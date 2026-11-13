import asyncio, json, sys
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'; BASE='http://127.0.0.1:5173'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(storage_state='state.json', viewport={'width':443,'height':960}, device_scale_factor=1, is_mobile=True, has_touch=True, user_agent=UA, timezone_id='America/Chicago')
        pg=await ctx.new_page(); writes=[]
        async def guard(r):
            q=r.request
            if q.method in('GET','HEAD','OPTIONS') or '/auth/v1/' in q.url or '/rpc/' in q.url: return await r.continue_()
            writes.append((q.method,q.url[-70:])); await r.fulfill(status=200, content_type='application/json', body='[]')
        async def fn(r): writes.append(('FN',r.request.url[-50:])); await r.fulfill(status=200, content_type='application/json', body='{"ok":true}')
        await pg.route('**/rest/v1/**', guard); await pg.route('**/.netlify/functions/**', fn)
        for path in sys.argv[1:]:
            await pg.goto(BASE+'/work'); await pg.wait_for_timeout(4200); ok=True
            for name in path.split('>'):
                if name=='HOME': continue
                l=pg.get_by_text(name, exact=True).locator('visible=true').first
                if not await l.count(): l=pg.get_by_text(name).locator('visible=true').first
                if not await l.count(): print('MISSING',path,'@',name); ok=False; break
                try: await l.click(timeout=6000)
                except Exception as e: print('NOCLICK',path,'@',name); ok=False; break
                await pg.wait_for_timeout(2600)
            if not ok: continue
            fn_=path.replace(' ','_').replace('>','__'); await pg.screenshot(path=f'ex/{fn_}.jpg', quality=55)
            t=await pg.locator('body').inner_text(); open(f'ex/{fn_}.txt','w').write(t)
            print('=====',path,pg.url.replace(BASE,''),len(t)); print(' | '.join(x.strip() for x in t.split('\n') if x.strip())[:650])
        print('WRITES',writes[:8]); await b.close()
asyncio.run(main())
