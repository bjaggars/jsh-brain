import asyncio, json
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
BASE='http://127.0.0.1:5173'
taps={}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(storage_state='state.json', viewport={'width':443,'height':960}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA, timezone_id='America/Chicago')
        pg = await ctx.new_page()
        # the server function that texts/emails: stubbed with production's success shape, so nothing is sent
        async def notify(route):
            await route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'sent':True,'to':'daniel.reyes@example.com','texted':True,'phone':'(352) 555-0171','sellersTold':['Priya Raman']}))
        await pg.route('**/.netlify/functions/**', notify)
        async def shot(name): await pg.screenshot(path=f'cap/{name}.jpg', quality=92)
        async def tap(loc, name):
            bb = await loc.bounding_box(); taps[name]=[bb['x']+bb['width']/2, bb['y']+bb['height']/2]
            await loc.click()
        await pg.goto(BASE+'/work'); await pg.wait_for_timeout(6000); await shot('a_home')
        await tap(pg.get_by_text('Showings', exact=True).first, 'a_home'); await pg.wait_for_timeout(3000); await shot('b_calendar')
        await tap(pg.get_by_text('Showings', exact=True).first, 'b_calendar'); await pg.wait_for_timeout(3500); await shot('c_showings')
        await tap(pg.locator('[data-e2e="showing-confirm"]').first, 'c_showings'); await pg.wait_for_timeout(3500); await shot('d_confirmed')
        await pg.goto(BASE+'/work'); await pg.wait_for_timeout(5000); await shot('e_home2')
        await tap(pg.get_by_text('Closings', exact=True).first, 'e_home2'); await pg.wait_for_timeout(3500); await shot('f_closings')
        await pg.goto(BASE+'/work?colors=1'); await pg.wait_for_timeout(5500); await shot('g_colors')
        await tap(pg.get_by_text('Gold', exact=True).first, 'g_colors'); await pg.wait_for_timeout(1500); await shot('h_gold')
        await tap(pg.get_by_text('Dark', exact=True).first, 'h_gold'); await pg.wait_for_timeout(1500); await shot('i_dark')
        json.dump(taps, open('cap/taps.json','w'), indent=1)
        await b.close()
asyncio.run(main())
