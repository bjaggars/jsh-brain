"""Fill the film-set questionnaire the way a (fictional) client would, on the public client page, and send it."""
import asyncio, json, sys
from playwright.async_api import async_playwright
URL='https://workshop.jshinnovations.com/i/nzaP6DR0ByBGp8wavwWwdjDXZRVYdaFv'
A={'Your name and role':'Riley Chen, owner','If the app only did one thing really well':'Tell the customer their bike is ready without us calling them.',
 "What's the biggest headache":'Paper repair tickets get lost and nobody knows which bikes are done.','Which tools or systems do you use':'Square for payments',
 'Who would use it?':'Two mechanics and the front counter','What does it absolutely have to do on day one':'Check a bike in, track the repair, and text the customer when it is ready.',
 'How do customers find out their bike is ready':'We call them, usually two or three times.'}
PICK=['1–10','Paper forms or a whiteboard','At a desk or counter','Phones','In 1–3 months']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1440,'height':810}, device_scale_factor=3)
        pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_timeout(5000)
        qs=await pg.evaluate("()=>[...document.querySelectorAll('.in-prompt')].map(e=>e.textContent.trim())"); print(len(qs), qs)
        for k,v in A.items():
            blk=pg.locator('.in-prompt', has_text=k).first.locator('xpath=..'); f=blk.locator('input[type=text], input:not([type]), textarea').first
            if await f.count(): await f.fill(v); print('filled',k[:30])
            else: print('NOFIELD',k[:30])
        for t in PICK:
            c=pg.get_by_role('button', name=t, exact=True).first
            if not await c.count(): c=pg.get_by_text(t, exact=True).first
            if await c.count(): await c.click(); print('picked',t)
        await pg.wait_for_timeout(2500); await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(400); await pg.screenshot(path='cap/p2/fc_top.jpg', quality=93)
        s=pg.locator('.in-send'); await s.evaluate("e=>window.scrollTo(0, e.getBoundingClientRect().bottom+window.scrollY-700)"); await pg.wait_for_timeout(500)
        print((await pg.locator('body').inner_text())[-260:].replace('\n',' | ')); await pg.screenshot(path='cap/p2/fc_end.jpg', quality=93); print('send box', await s.bounding_box())
        if len(sys.argv)>1 and sys.argv[1]=='send':
            await s.click(); await pg.wait_for_timeout(5000); await pg.evaluate('window.scrollTo(0,0)'); await pg.screenshot(path='cap/p2/fc_done.jpg', quality=93); print('AFTER:', (await pg.locator('body').inner_text())[:300].replace('\n',' | '))
        await b.close()
asyncio.run(main())
