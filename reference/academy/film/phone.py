"""Capture the client share link the way a client sees it on a phone (no sign-in)."""
import asyncio, json, urllib.request, re
from playwright.async_api import async_playwright
import live_auth
async def main():
    sess=live_auth.login(); t=live_auth.rest(sess,'prototype_shares?engagement_id=eq.5eed0000-0000-4000-8000-000000000001&revoked_at=is.null&select=token,prototype_version&order=created_at.desc')[0]['token']
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':390,'height':844}, device_scale_factor=3, is_mobile=True, has_touch=True, user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1')
        pg=await ctx.new_page(); await pg.goto('https://workshop.jshinnovations.com/p/'+t); await pg.wait_for_timeout(5000)
        await pg.screenshot(path='cap/p2/ph_who.jpg', quality=93); txt=await pg.locator('body').inner_text(); print(txt[:500])
        l=pg.get_by_text('Crew member').first
        if await l.count():
            await l.tap(); await pg.wait_for_timeout(3500); await pg.screenshot(path='cap/p2/ph_route.jpg', quality=93)
            fr=[f for f in pg.frames if f!=pg.main_frame]; print('frames',len(fr))
            tgt=fr[0] if fr else pg
            s=tgt.get_by_text('Pelican Point Yacht Club').first
            if await s.count():
                await s.tap(); await pg.wait_for_timeout(2500); await pg.screenshot(path='cap/p2/ph_stop.jpg', quality=93); print('stop ok')
        await b.close()
asyncio.run(main())
