"""AWP Academy capture: real screens of the local dev build on the Demo engagement. Read-only: job + function calls are stubbed,
other clients' names in the engagements list are replaced with fictional ones before the page sees them."""
import asyncio, json
from playwright.async_api import async_playwright
DEMO='5eed0000-0000-4000-8000-000000000001'; B='http://127.0.0.1:5174'
FAKE=[('Route planner','Harborview Field Services','Field services'),('Member check-in','Pulse Fitness Studios','Fitness studios'),
      ('Job costing','Ridgeline Remodeling','Residential remodeling'),('Parts counter','Lakeside Outdoor Power','Outdoor power equipment dealers')]
boxes={}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(storage_state='state.json', viewport={'width':1440,'height':810}, device_scale_factor=2, timezone_id='America/Chicago')
        pg=await ctx.new_page(); polls={'n':0}
        async def health(r): await r.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'missing':[],'email':True}))
        async def fn(r): await r.fulfill(status=202, content_type='application/json', body='{}')
        async def rest_eng(r):
            if r.request.method!='GET' or 'is_stub' not in r.request.url or 'id=eq.' in r.request.url: return await r.continue_()
            resp=await r.fetch(); rows=await resp.json(); k=0
            for row in rows:
                if not row.get('is_stub'): row['name'],row['client_name'],row['industry']=FAKE[k%4]; k+=1
            await r.fulfill(response=resp, body=json.dumps(rows))
        async def rest_jobs(r):
            if r.request.method=='POST': return await r.fulfill(status=201, content_type='application/json', body=json.dumps({'id':'00000000-0000-4000-8000-00000000f115'}))
            if 'f115' not in r.request.url: return await r.continue_()
            polls['n']+=1; done=False   # never lands: landing with the questionnaire focus would create a draft on the Demo engagement
            await r.fulfill(status=200, content_type='application/json', body=json.dumps({'status':'done' if done else 'running','progress':'Building three expert voices','chars':0,'warning':None,'result':{'engagement_id':DEMO} if done else None,'error':None}))
        await pg.route('**/api/health', health); await pg.route('**/.netlify/functions/**', fn)
        await pg.route('**/rest/v1/engagements*', rest_eng); await pg.route('**/rest/v1/jobs*', rest_jobs)
        async def shot(n, full=False): await pg.screenshot(path=f'cap/{n}.jpg', quality=93, full_page=full)
        async def box(key, loc):
            if not await loc.count(): print('MISSING', key); return
            bb=await loc.bounding_box(); sy=await pg.evaluate('window.scrollY'); boxes[key]=[bb['x'],bb['y']+sy,bb['width'],bb['height']]
        # ---- list
        await pg.goto(B+'/'); await pg.wait_for_timeout(4000); await shot('list')
        await box('list.new', pg.get_by_role('button', name='New engagement').first); await box('list.rows', pg.locator('.list').first)
        await box('list.demo', pg.get_by_text('Counter-to-dock ordering').first)
        # ---- new engagement
        await pg.get_by_role('button', name='New engagement').first.click(); await pg.wait_for_timeout(1200); await shot('new0', True)
        ins=pg.locator('main input:visible, main textarea:visible')
        print('inputs', await ins.count(), [await ins.nth(i).get_attribute('placeholder') for i in range(await ins.count())])
        await ins.nth(0).fill('Counter-to-dock ordering'); await ins.nth(1).fill('Tidewater Marine Supply'); await ins.nth(2).fill('Marine parts distribution'); await pg.wait_for_timeout(300)
        await box('new.fields', pg.locator('label', has_text='Engagement name').first); await box('new.industry', pg.locator('label', has_text='Industry').first)
        await shot('new1', True)
        await box('new.pre', pg.locator('label.choice').first)
        await pg.get_by_placeholder('Name', exact=True).fill('Dana Reyes'); await pg.get_by_placeholder('name@company.com').fill('dana@tidewatermarine.example')
        await pg.locator('textarea').first.fill('Wants to replace the paper order sheets at the parts counter'); await pg.wait_for_timeout(300)
        await box('new.contact', pg.locator('label', has_text='Client contact').first); await box('new.notes', pg.locator('label', has_text='What you heard on the call').first)
        await box('new.create', pg.get_by_role('button', name='Create engagement')); await shot('new2', True)
        await pg.get_by_role('button', name='Create engagement').click(); await pg.wait_for_timeout(1500); await shot('new3', True)
        print('after create', pg.url)
        # ---- engagement (JSH view)
        await pg.unroute('**/rest/v1/jobs*')
        await pg.goto(B+'/?e='+DEMO); await pg.wait_for_timeout(5000); await shot('eng', True)
        await box('eng.present', pg.get_by_role('button', name='Present to client')); await box('eng.title', pg.get_by_text('Counter-to-dock ordering').first)
        for key,txt in [('eng.blueprint','Blueprint'),('eng.record','Workshop record'),('eng.intake','Pre-workshop questionnaire'),('eng.files','Client files'),('eng.before','Before the prototype'),('eng.proto','Prototype')]:
            h=pg.get_by_role('heading', name=txt, exact=True).first
            if await h.count(): 
                sec=h.locator('xpath=ancestor::section[1]'); await box(key, sec if await sec.count() else h)
        await box('eng.tabs', pg.get_by_text('JSH chamber', exact=True).first); await box('eng.voices', pg.get_by_text('Expert voices').first)
        await box('eng.check', pg.get_by_text('The 20 core client questions are answered').first)
        await box('eng.closing', pg.get_by_text('Client workshop: closing comments').first)
        await box('eng.protolock', pg.get_by_text('Opens when Workshop 1 is marked complete').first)
        await box('eng.review', pg.get_by_text('Review all questions and answers').first)
        # ---- present to client
        await pg.get_by_role('button', name='Present to client').click(); await pg.wait_for_timeout(1500); await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(400); await shot('present', True)
        await box('pres.pill', pg.get_by_role('button', name='Back to JSH view'))
        for key,txt in [('pres.blueprint','Blueprint'),('pres.record','Workshop record')]:
            h=pg.get_by_role('heading', name=txt, exact=True).first; sec=h.locator('xpath=ancestor::section[1]'); await box(key, sec if await sec.count() else h)
        q=pg.get_by_text("Walk me through a driver's morning").first
        if await q.count(): await box('pres.q', q)
        open('cap/present.txt','w').write(await pg.locator('body').inner_text())
        json.dump(boxes, open('cap/boxes.json','w'), indent=1); await b.close()
asyncio.run(main())
