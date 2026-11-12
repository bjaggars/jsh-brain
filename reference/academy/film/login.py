import asyncio, json, urllib.request
from playwright.async_api import async_playwright
URL='https://comtcpdhainyrjazztpj.supabase.co'; ANON='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNvbXRjcGRoYWlueXJqYXp6dHBqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA1MjEwMzUsImV4cCI6MjEwNjA5NzAzNX0.eoJ_1krbFEch8jITRc8nbYNauzl71gL-3iP1-iM_tls'
req=urllib.request.Request(URL+'/auth/v1/token?grant_type=password', data=json.dumps({'email':'filmset.academy@jshinnovations.com','password':open('.pw').read()  # film-set password: local file, never committed}).encode(), headers={'apikey':ANON,'content-type':'application/json'})
sess=json.loads(urllib.request.urlopen(req).read()); print('token ok', sess['user']['email'])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':1440,'height':810}, device_scale_factor=2, timezone_id='America/Chicago')
        pg=await ctx.new_page(); await pg.goto('http://127.0.0.1:5174/')
        await pg.evaluate("s=>localStorage.setItem('sb-comtcpdhainyrjazztpj-auth-token', s)", json.dumps(sess))
        await pg.goto('http://127.0.0.1:5174/'); await pg.wait_for_timeout(4000)
        await pg.screenshot(path='x_list.jpg', quality=80)
        print((await pg.locator('body').inner_text())[:600].replace('\n',' | '))
        await pg.goto('http://127.0.0.1:5174/?e=5eed0000-0000-4000-8000-000000000001'); await pg.wait_for_timeout(5000)
        await pg.screenshot(path='x_eng.jpg', quality=70, full_page=True)
        t=await pg.locator('body').inner_text(); open('x_eng.txt','w').write(t); print(len(t))
        await ctx.storage_state(path='state.json'); await b.close()
asyncio.run(main())
