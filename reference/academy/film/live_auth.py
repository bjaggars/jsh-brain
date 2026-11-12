import json, urllib.request
URL='https://comtcpdhainyrjazztpj.supabase.co'; SITE='https://workshop.jshinnovations.com'; DEMO='5eed0000-0000-4000-8000-000000000001'
ANON=__import__('re').search(r"eyJ[A-Za-z0-9_.-]+", open('login.py').read()).group(0)
def login():
    req=urllib.request.Request(URL+'/auth/v1/token?grant_type=password', data=json.dumps({'email':'filmset.academy@jshinnovations.com','password':open('.pw').read()}).encode(), headers={'apikey':ANON,'content-type':'application/json'})
    return json.loads(urllib.request.urlopen(req).read())
def rest(sess, path):
    req=urllib.request.Request(URL+'/rest/v1/'+path, headers={'apikey':ANON,'authorization':'Bearer '+sess['access_token']})
    return json.loads(urllib.request.urlopen(req).read())
