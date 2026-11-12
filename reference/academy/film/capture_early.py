"""Archive of every early-stage (pre-Workshop-1-complete) screen of the Demo engagement, taken before it is moved forward. Read-only."""
import asyncio, json
from playwright.async_api import async_playwright
DEMO='5eed0000-0000-4000-8000-000000000001'; B='http://127.0.0.1:5174'; boxes={}; writes=[]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(storage_state='state.json', viewport={'width':1440,'height':810}, device_scale_factor=3, timezone_id='America/Chicago')
        pg=await ctx.new_page()
        async def guard(r):
            q=r.request
            if q.method in('GET','HEAD','OPTIONS'): return await r.continue_()
            writes.append((q.method,q.url[:100])); await r.fulfill(status=200, content_type='application/json', body='[]')
        async def fn(r): writes.append(('FN',r.request.url[-50:])); await r.fulfill(status=202, content_type='application/json', body='{}')
        async def health(r): await r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'missing':[],'email':True}))
        await pg.route('**/rest/v1/**', guard); await pg.route('**/.netlify/functions/**', fn); await pg.route('**/api/health', health)
        async def hidefoot(): await pg.evaluate("()=>{for(const e of document.querySelectorAll('footer')) if(/functions:/.test(e.textContent)) e.style.visibility='hidden'}")
        async def box(key, loc, page=False):
            if not await loc.count(): print('MISSING', key); return
            bb=await loc.first.bounding_box(); sy=await pg.evaluate('window.scrollY') if page else 0; boxes[key]=[bb['x'],bb['y']+sy,bb['width'],bb['height']]
        await pg.goto(B+'/?e='+DEMO); await pg.wait_for_timeout(5000); await hidefoot()
        await pg.screenshot(path='cap/early/eng_full.jpg', quality=92, full_page=True)
        open('cap/early/eng_full.txt','w').write(await pg.locator('body').inner_text())
        for t in ['Review all questions and answers','The 20 core client questions are answered','Client workshop: closing comments','JSH: closing comments','Opens when Workshop 1 is marked complete','Nothing to add','Save comments','Prepare the questionnaire']:
            await box('full.'+t[:24], pg.get_by_text(t), True)
        cards=['Business context',"Today's setup",'Personas','Day-in-the-life journeys','Data','Screens','Integrations','Roles and permissions','Speed, security and scale','Brand and design','Expert voices','Questions','Assumptions','Recommendations','Current apps','Perfect-world wishes']
        for c in cards:
            l=pg.get_by_text(c, exact=True).first
            if not await l.count(): print('MISSING',c); continue
            await l.click(); await pg.wait_for_timeout(1000); d=pg.locator('[role=dialog]').first
            n=c.replace(' ','_').replace("'",'').replace(',','')
            await pg.screenshot(path=f'cap/early/card_{n}.jpg', quality=92); await box('card.'+n, d)
            open(f'cap/early/card_{n}.txt','w').write(await d.inner_text() if await d.count() else '')
            cl=pg.get_by_role('button', name='Close').first
            if await cl.count(): await cl.click()
            await pg.wait_for_timeout(300)
        # JSH chamber tab
        t=pg.get_by_text('JSH chamber', exact=True).first; await t.evaluate("e=>window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-200)"); await t.click(); await pg.wait_for_timeout(1200)
        await pg.screenshot(path='cap/early/jsh_chamber.jpg', quality=92); 
        sec=t.locator('xpath=ancestor::section[1]'); open('cap/early/jsh_chamber.txt','w').write(await (sec if await sec.count() else pg.locator('body')).inner_text())
        # review all questions and answers
        rv=pg.get_by_text('Review all questions and answers').first
        if await rv.count():
            await rv.evaluate("e=>window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-200)"); await rv.click(); await pg.wait_for_timeout(1200); await pg.screenshot(path='cap/early/review.jpg', quality=92)
            d=pg.locator('[role=dialog]').first; open('cap/early/review.txt','w').write(await d.inner_text() if await d.count() else (await pg.locator('body').inner_text()))
            cl=pg.get_by_role('button', name='Close').first
            if await cl.count(): await cl.click()
        # readiness panel in view
        rd=pg.get_by_text('Before the prototype', exact=True).first; await rd.evaluate("e=>window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-60)"); await pg.wait_for_timeout(500); await pg.screenshot(path='cap/early/readiness.jpg', quality=92)
        for t2 in ['The 20 core client questions are answered','The Blueprint reaches 60%','No recommendations waiting on you','Client workshop: closing comments','JSH: closing comments']:
            await box('ready.'+t2[:22], pg.get_by_text(t2))
        # present to client, full page
        await pg.evaluate('window.scrollTo(0,0)'); await pg.get_by_role('button', name='Present to client').click(); await pg.wait_for_timeout(1500); await hidefoot()
        await pg.screenshot(path='cap/early/present_full.jpg', quality=92, full_page=True); open('cap/early/present_full.txt','w').write(await pg.locator('body').inner_text())
        json.dump(boxes, open('cap/early/boxes.json','w'), indent=1); print('WRITES', writes); await b.close()
asyncio.run(main())
