import asyncio, json
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(storage_state='state.json', viewport={'width':443,'height':960}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA, timezone_id='America/Chicago')
        pg = await ctx.new_page()
        async def notify(route):
            await asyncio.sleep(0.4)
            await route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok':True,'sent':True,'to':'daniel.reyes@example.com','texted':True,'phone':'(352) 555-0171','sellersTold':['Priya Raman']}))
        await pg.route('**/.netlify/functions/**', notify)
        await pg.goto('http://127.0.0.1:5173/work'); await pg.wait_for_timeout(5000)
        await pg.get_by_text('Showings', exact=True).first.click(); await pg.wait_for_timeout(2500)
        await pg.get_by_text('Showings', exact=True).first.click(); await pg.wait_for_timeout(3500)
        await pg.locator('[data-e2e="showing-confirm"]').first.click()
        for i in range(12):
            r = pg.locator('[data-e2e="showing-receipt"]')
            if await r.count(): print(i, (await r.inner_text())[:200])
            await pg.screenshot(path=f'cap/burst_{i:02d}.jpg', quality=92); await pg.wait_for_timeout(120)
        await b.close()
asyncio.run(main())
