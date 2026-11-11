import asyncio, json
from playwright.async_api import async_playwright
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
OUT='cap_home/'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(storage_state='hstate.json', viewport={'width':443,'height':960}, device_scale_factor=2, is_mobile=True, has_touch=True, user_agent=UA, timezone_id='America/Chicago')
        pg = await ctx.new_page()
        await pg.goto('http://127.0.0.1:5173/'); await pg.wait_for_timeout(4500)
        # hide the floating Ask MRV button so it doesn't smear across the scroll
        await pg.screenshot(path=OUT + 'm_dash_full.jpg', quality=92, full_page=True)
        boxes = {}
        for name in ['Home search', 'Check a neighborhood', 'Mortgage calculator', 'Cash to close', 'Compare homes', 'Make an offer']:
            el = pg.get_by_text(name, exact=True).first
            card = el.locator('xpath=ancestor::*[self::button or self::a or contains(@class,"card") or contains(@class,"tile")][1]')
            bb = await (card.bounding_box() if await card.count() else el.bounding_box())
            sy = await pg.evaluate('window.scrollY'); boxes[name] = [bb['x'], bb['y'] + sy, bb['width'], bb['height']]
        json.dump(boxes, open(OUT + 'tiles.json', 'w'), indent=1); print(boxes)
        await b.close()
asyncio.run(main())
