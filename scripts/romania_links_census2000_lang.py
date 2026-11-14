import json,urllib.request,csv
T="px-x-4003000000_123"; U=f"https://www.pxweb.bfs.admin.ch/api/v1/de/{T}/{T}.px"
m=json.load(open(f"/home/user/Diaspora/data/romania_links/raw/{T}_meta.json"))
reg=[v for v in m['variables'] if v['code'].startswith('Kanton')][0]
vals=[c for c,t in zip(reg['values'],reg['valueTexts']) if t=='Schweiz' or t.startswith('- ')]
body={"query":[{"code":reg['code'],"selection":{"filter":"item","values":vals}},
 {"code":"Hauptsprache","selection":{"filter":"item","values":[c for c,t in zip(m['variables'][3]['values'],m['variables'][3]['valueTexts']) if t in('Hauptsprachen - Total','Rumänisch')]}},
 {"code":"Wohnsitztyp","selection":{"filter":"all","values":["*"]}},
 {"code":m['variables'][2]['code'],"selection":{"filter":"all","values":["*"]}}],
 "response":{"format":"csv"}}
r=urllib.request.Request(U,data=json.dumps(body).encode(),headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0'})
open("/home/user/Diaspora/data/romania_links/raw/census2000_rumaenisch_raw.csv","wb").write(urllib.request.urlopen(r,timeout=90).read())
