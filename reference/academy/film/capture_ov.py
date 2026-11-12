"""Overview capture: viewport shots (1440x810 @2x) of the Demo engagement. Strictly read-only: every non-GET to the database and every
server-function call is answered locally and never reaches the platform."""
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
        async def shot(n): await pg.wait_for_timeout(500); await pg.screenshot(path=f'cap/{n}.jpg', quality=93)
        async def box(key, loc):
            if not await loc.count(): print('MISSING', key); return
            bb=await loc.bounding_box(); boxes[key]=[bb['x'],bb['y'],bb['width'],bb['height']]
        async def close():
            c=pg.get_by_role('button', name='Close').first
            if await c.count(): await c.click()
            await pg.wait_for_timeout(400)
        await pg.goto(B+'/?e='+DEMO); await pg.wait_for_timeout(5000)
        await pg.evaluate("()=>{for(const e of document.querySelectorAll('p,div,footer,small')){ if(e.children.length<2 && /^Build \\w+, functions:/.test(e.textContent.trim())) e.style.visibility='hidden'; }}")
        await shot('ov_top')
        await box('top.present', pg.get_by_role('button', name='Present to client'))
        for k,t in [('top.personas','Personas'),('top.journeys','Day-in-the-life journeys'),('top.data','Data'),('top.screens','Screens'),('top.bc','Business context'),('top.voices','Expert voices'),('top.apps','Current apps'),('top.assume','Assumptions')]:
            l=pg.get_by_text(t, exact=True).first; card=l.locator('xpath=ancestor::button[1]')
            await box(k, card if await card.count() else l)
        h=pg.get_by_role('heading', name='Blueprint', exact=True).first; await box('top.bp', h.locator('xpath=ancestor::section[1]'))
        async def dlg(name, key, marks):
            await pg.get_by_text(name, exact=True).first.click(); await pg.wait_for_timeout(1200)
            d=pg.locator('[role=dialog]').first; await box(key+'.dlg', d)
            for mk,txt in marks: await box(key+'.'+mk, d.get_by_text(txt).first)
            await shot('ov_'+key); await close()
        await dlg('Expert voices','voices',[('client','Client expert'),('arch','Discovery architect'),('domain','Domain expert')])
        await dlg('Current apps','apps',[('inv','Inventory system'),('invoice','Invoicing app'),('text','Driver group text'),('looked','Every tool has been looked up')])
        await dlg('Questions','questions',[('q1','What goes wrong most often'),('q2','Which tools do your counters'),('q3',"Walk me through a driver's morning")])
        await dlg('Business context','bc',[('fact','core problem'),('src','Client said')])
        await dlg('Assumptions','assume',[('a1','Drivers run one morning route'),('src','Industry default')])
        await dlg('Recommendations','recs',[('r1','Drivers capture a delivery photo'),('practice','Industry practice')])
        # the live question
        q=pg.locator('li.qcard').first; await q.evaluate("e=>window.scrollTo(0, e.getBoundingClientRect().top+window.scrollY-300)"); await pg.wait_for_timeout(500)
        await box('q.card', q); await box('q.core', pg.get_by_text('Core questions: 3 of 20 asked').first); await box('q.idk', q.get_by_role('button', name="I don't know")); await box('q.tabs', pg.get_by_text('Client workshop', exact=True).first)
        await shot('ov_q')
        # present to client
        await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(300)
        await pg.get_by_role('button', name='Present to client').click(); await pg.wait_for_timeout(1500); await pg.evaluate('window.scrollTo(0,0)')
        await box('pv.pill', pg.get_by_role('button', name='Back to JSH view')); await shot('ov_present')
        json.dump(boxes, open('cap/ov_boxes.json','w'), indent=1); print('WRITES', writes); await b.close()
asyncio.run(main())
