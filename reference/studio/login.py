"""Sign in as the film-set agent once; saves state.json (gitignored) for capture.py / burst.py.
Usage: FILMSET_PASSWORD=... python3 login.py   (app running locally at :5173 against TEST)"""
import asyncio, os
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': 443, 'height': 960}, device_scale_factor=2, is_mobile=True, has_touch=True)
        pg = await ctx.new_page(); await pg.goto('http://127.0.0.1:5173/login'); await pg.wait_for_timeout(2500)
        await pg.locator('input[type="email"]').fill('filmset.agent@jshinnovations.com')
        await pg.locator('input[type="password"]').fill(os.environ['FILMSET_PASSWORD'])
        await pg.locator('input[type="password"]').press('Enter'); await pg.wait_for_timeout(6000)
        await ctx.storage_state(path='state.json'); await b.close(); print('signed in')
asyncio.run(main())
