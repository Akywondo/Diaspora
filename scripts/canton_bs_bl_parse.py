import csv,collections,sys
R='/home/user/Diaspora/data/canton_bs_bl/'
rd=lambda f:csv.DictReader(open(R+'raw/'+f,encoding='utf-8-sig'),delimiter=';')
# flows
agg=collections.Counter()
for r in rd('bs_100138.csv'):
    if r['von_land']=='Rumänien' and r['ereignis_typ']=='Zuzug': k=(r['jahr'],'immigration_from_romania_to_BS')
    elif r['nach_land']=='Rumänien' and r['ereignis_typ']=='Wegzug': k=(r['jahr'],'emigration_from_BS_to_romania')
    elif r['nationalitaet'] and 0: continue
    else: continue
    agg[k]+=int(r['anzahl'] or 0)
w=csv.writer(open(R+'bs_romania_migration_by_year.csv','w',newline=''))
w.writerow(['year','flow','persons','note'])
for (y,k),v in sorted(agg.items()): w.writerow([y,k,v,'by previous/next country of residence = Romania (not nationality); 2026 partial year' if y=='2026' else 'by previous/next country of residence = Romania (not nationality)'])
nat=collections.Counter()
for r in rd('bs_100321.csv'):
    if r['ehem_staaatsangehorigkeit']=='Rumänien': nat[(r['jahr'],r['geschlecht'])]+=int(r['anzahl_eingeburgerte'])
w=csv.writer(open(R+'bs_naturalisations_former_romanian.csv','w',newline=''))
w.writerow(['year','sex','naturalised_persons'])
for (y,s),v in sorted(nat.items()): w.writerow([y,s,v])
yt=collections.Counter()
for (y,s),v in nat.items(): yt[y]+=v
print(sorted(yt.items())); print(sorted(agg.items()))
# births: only CH/Ausl
# crosscheck
bfs={}
for r in csv.DictReader(open('/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv')):
    if r['canton'] in('Basel-Stadt','Basel-Landschaft') and r['population_type'].startswith('Ständige') and r['permit'].startswith('Anwesenheitsbewilligung - Total') and r['sex'].startswith('Geschlecht') and r['age_class'].startswith('Alter'):
        bfs[(r['canton'],r['year'])]=int(r['persons'])
w=csv.writer(open(R+'cantonal_crosscheck.csv','w',newline=''))
w.writerow('canton,year,cantonal_value,cantonal_definition,bfs_value,diff_abs,diff_pct,source_url'.split(','))
for (c,y),v in sorted(bfs.items()):
    w.writerow([c,y,'','NOT PUBLISHED by canton for Romania (data.bs.ch gives only CH/BS/foreign totals; BL not retrieved)',v,'','','https://data.bs.ch/explore/dataset/100059/' if c=='Basel-Stadt' else 'https://www.statistik.bl.ch'])
print(len(bfs),[v for k,v in bfs.items() if k[1] in('2010','2025')])
