"""Homeowner film set (Jordan Avery, agentless) — captures every homeowner-promo still + tap points into cap_home/."""
import asyncio, json, datetime
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
OUT='cap_home/'
taps={}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(storage_state='hstate.json', viewport={'width':443,'height':960}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA, timezone_id='America/Chicago')
        pg = await ctx.new_page()
        exp = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
        async def stub(route):   # packet-create emails the lender: stubbed with production's success shape — nothing is sent
            await route.fulfill(status=200, content_type='application/json', body=json.dumps({'ok': True, 'emailed': True, 'expires_at': exp}))
        await pg.route('**/.netlify/functions/**', stub)
        async def shot(n): await pg.screenshot(path=OUT + n + '.jpg', quality=92)
        async def tap(loc, n):
            bb = await loc.bounding_box(); taps[n] = [bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2]; await loc.click()
        home = 'http://127.0.0.1:5173/'
        await pg.goto(home); await pg.wait_for_timeout(4000); await shot('c_dash')
        # affordability
        await tap(pg.get_by_text('How much can I afford?', exact=True).first, 'c_dash_afford'); await pg.wait_for_timeout(2000); await shot('d_calc')
        ins = pg.locator('input:visible')
        for i, v in enumerate(['98000', '450', '40000', '6.4']): await ins.nth(i).fill(v); await pg.wait_for_timeout(250)
        await pg.wait_for_timeout(1200); await shot('e_calc_filled')
        # checklist
        await pg.goto(home); await pg.wait_for_timeout(3500)
        await tap(pg.get_by_text('My checklist', exact=True).first, 'c_dash_check'); await pg.wait_for_timeout(2500); await shot('f_checklist')
        # documents
        await pg.goto(home); await pg.wait_for_timeout(3500)
        await pg.get_by_text('Documents').nth(2).click(); await pg.wait_for_timeout(3000); await shot('g_docs')
        # lender share
        await pg.goto(home); await pg.wait_for_timeout(3500)
        await tap(pg.get_by_text('Get pre-approved', exact=True).first, 'c_dash_share'); await pg.wait_for_timeout(2500); await shot('h_share')
        await tap(pg.get_by_text('Share documents', exact=True).first, 'h_share'); await pg.wait_for_timeout(2000)
        for cb in await pg.locator('input[type=checkbox]:visible').all(): await cb.check(); await pg.wait_for_timeout(150)
        await pg.locator('[data-e2e="hv-packet-name"]').fill('Gulf Coast Lending — Dana'); await pg.locator('[data-e2e="hv-packet-email"]').fill('dana@example.com')
        await pg.wait_for_timeout(500); await shot('i_share_form')
        await tap(pg.locator('[data-e2e="hv-packet-send"]'), 'i_share_form'); await pg.wait_for_timeout(2500); await shot('j_share_sent')
        # add your agent
        await pg.goto(home); await pg.wait_for_timeout(3500)
        await pg.get_by_text('Add your agent', exact=True).last.scroll_into_view_if_needed(); await pg.wait_for_timeout(600); await shot('k_dash_agent')
        await tap(pg.get_by_text('Add your agent', exact=True).last, 'k_dash_agent'); await pg.wait_for_timeout(2500); await shot('l_agent')
        print((await pg.locator('body').inner_text())[150:700].replace('\n', ' | '))
        json.dump(taps, open(OUT + 'taps.json', 'w'), indent=1); await b.close()
asyncio.run(main())
