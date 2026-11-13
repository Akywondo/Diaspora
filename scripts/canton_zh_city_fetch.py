import json,sys,time,urllib.request,urllib.parse,os
OUT='/home/user/Diaspora/data/canton_zh/raw/'
B='https://data.stadt-zuerich.ch/api/3/action/'
def get(u):
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=90))
        except Exception as e:
            time.sleep(10)
    raise
def pkg(name):
    return get(B+'package_show?id='+name)['result']
if __name__=='__main__':
    for name in sys.argv[1:]:
        p=pkg(name); r=p['resources'][0]
        time.sleep(1)
        j=get(B+'datastore_search?resource_id=%s&limit=0'%r['id'])
        print(name,r['id'],j['result'].get('total'),[f['id'] for f in j['result']['fields']])
        time.sleep(1)
