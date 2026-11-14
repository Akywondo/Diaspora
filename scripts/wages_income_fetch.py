import json,sys,time,urllib.request,csv
B='https://www.pxweb.bfs.admin.ch/api/v1/de/'
def post(t,q):
    body=json.dumps({"query":q,"response":{"format":"json-stat2"}}).encode()
    r=urllib.request.Request(B+t+'/'+t+'.px',body,{'Content-Type':'application/json','User-Agent':'Mozilla/5.0'})
    return json.load(urllib.request.urlopen(r,timeout=120))
def flat(js):
    ids=js['id'];cats=[js['dimension'][i]['category'] for i in ids]
    labs=[[c['label'][k] for k in sorted(c['index'],key=lambda x:c['index'][x])] for c in cats]
    codes=[sorted(c['index'],key=lambda x:c['index'][x]) for c in cats]
    import itertools
    vals=js['value'];n=0
    for combo in itertools.product(*[range(len(l)) for l in labs]):
        v=vals[n];n+=1
        yield ids,[codes[i][j] for i,j in enumerate(combo)],[labs[i][j] for i,j in enumerate(combo)],v
def sel(c,v): return {"code":c,"selection":{"filter":"item","values":v}}
allsel=lambda c:{"code":c,"selection":{"filter":"all","values":["*"]}}
t='px-x-0304010000_203'
js=post(t,[allsel('Jahr'),allsel('Grossregion'),allsel('Schweizer/innen und Ausländer/innen'),sel('Berufliche Stellung',['-1']),allsel('Geschlecht'),sel('Zentralwert und andere Perzentile',['1'])])
json.dump(js,open('/home/user/Diaspora/data/wages_income/raw/lse203.json','w'))
with open('/home/user/Diaspora/data/wages_income/lse_median_wage_by_permit_sex_region.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['year','region','nationality_permit_group','sex','median_gross_monthly_wage_chf_standardised'])
    for ids,c,l,v in flat(js): w.writerow([l[0],l[1],l[2],l[4],'' if v is None else v])
time.sleep(2)
t='px-x-0304010000_206'
js=post(t,[allsel('Jahr'),sel('Grossregion',['-1']),allsel('Wirtschaftsabteilung'),allsel('Schweizer/innen und Ausländer/innen'),sel('Dienstjahre',['-1']),sel('Zentralwert und andere Perzentile',['1'])])
json.dump(js,open('/home/user/Diaspora/data/wages_income/raw/lse206.json','w'))
with open('/home/user/Diaspora/data/wages_income/lse_median_wage_by_division_permit.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['year','division_code','division','nationality_permit_group','median_gross_monthly_wage_chf_standardised'])
    for ids,c,l,v in flat(js): w.writerow([l[0],c[2],l[2],l[3],'' if v is None else v])
