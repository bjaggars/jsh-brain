# REST helper: acts on the MRV TEST database as the film-set agent (RLS applies). TEST only.
import json, urllib.request, re, os
env=dict(l.strip().split('=',1) for l in open('/home/claude/myhomevault/.env.local') if '=' in l)
URL=env['VITE_SUPABASE_URL']; KEY=env['VITE_SUPABASE_ANON_KEY']
assert 'xhntyqjhvvadtavtszgi' in URL, 'TEST database only'
_t=None
def tok(email='filmset.agent@jshinnovations.com'):
    global _t
    if _t: return _t
    r=urllib.request.Request(URL+'/auth/v1/token?grant_type=password',data=json.dumps({'email':email,'password':os.environ.get('FILMSET_PASSWORD') or open('.pw').read()}).encode(),headers={'apikey':KEY,'Content-Type':'application/json'})
    _t=json.load(urllib.request.urlopen(r))['access_token']; return _t
def rest(method,path,body=None,prefer='return=representation'):
    r=urllib.request.Request(URL+'/rest/v1/'+path,method=method,data=None if body is None else json.dumps(body).encode(),headers={'apikey':KEY,'Authorization':'Bearer '+tok(),'Content-Type':'application/json','Prefer':prefer})
    try:
        d=urllib.request.urlopen(r).read(); return json.loads(d) if d else None
    except urllib.error.HTTPError as e: return {'ERR':e.code,'msg':e.read().decode()[:300]}
