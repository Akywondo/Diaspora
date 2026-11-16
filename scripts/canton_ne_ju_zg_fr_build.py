import csv,re,sys
base="/home/user/Diaspora/data/canton_ne_ju_zg_fr/"
ref="/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv"
bfs={}
for r in csv.DictReader(open(ref,encoding='utf-8')):
    if r['population_type'].startswith('Ständige') and 'Total' in r['permit'] and 'Total' in r['sex'] and 'Total' in r['age_class']:
        bfs[(r['canton'],int(r['year']))]=int(r['persons'])
print({k:v for k,v in bfs.items() if k[1]==2025 and k[0][:2] in('Ne','Ju','Zu','Fr')})
# Zug
zg=[]
for line in open(base+"raw/c12f7f49",encoding='utf-8',errors='ignore'):
    m=re.match(r'(\d{4}),"Rumänien","(\d+)"',line)
    if m: zg.append((int(m.group(1)),int(m.group(2))))
zurl="https://data.zg.ch/store/1/resource/204"
ne=[("Neuchâtel",2025,"total",549),("Neuchâtel",2025,"women",333),("Neuchâtel",2025,"men",216),("Neuchâtel",2025,"permit_C_etablis",191),("Neuchâtel",2025,"permit_B_sejour",353),("Neuchâtel",2025,"short_stay",5)]
w=csv.writer(open(base+"romanians_nuechatel_zug_canton_stats.csv","w",newline='',encoding='utf-8'))
w.writerow(["canton","year","breakdown","value","definition","source_url"])
for y,v in zg: w.writerow(["Zug",y,"total",v,"Auslaendische Wohnbevoelkerung nach Nationalitaet (STATPOP-based, 31 Dec)",zurl])
for c,y,b,v in ne: w.writerow([c,y,b,v,"Population etrangere selon nationalite, RCP Service de statistique NE (31 Dec)","https://stat.ne.ch/1f.html"])
cc=csv.writer(open(base+"cantonal_crosscheck.csv","w",newline='',encoding='utf-8'))
cc.writerow(["canton","year","cantonal_value","cantonal_definition","bfs_value","diff_abs","diff_pct","source_url"])
def key(n): return [k for k in bfs if k[1]==2025 and k[0].startswith(n)][0][0]
rows=[("Zug",key("Zug"),y,v,"Zug statistics STATPOP-based foreign pop by nationality",zurl) for y,v in zg]
rows.append(("Neuchâtel",key("Neuch"),2025,549,"NE RCP cantonal register, foreign pop (C+B+short stay <12m), 31 Dec","https://stat.ne.ch/1f.html"))
for c,k,y,v,d,u in rows:
    b=bfs[(k,y)]; cc.writerow([c,y,v,d,b,v-b,round(100*(v-b)/b,2),u])
