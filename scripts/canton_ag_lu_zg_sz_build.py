import openpyxl,csv,sys
D='/home/user/Diaspora/data/canton_ag_lu_zg_sz/'
R=D+'raw/ag_annual_xlsx/ag_bev_%d.xlsx'
U='https://www.ag.ch/media/kanton-aargau/dfr/dokumente/statistik/publikationen/statistikthemen/01-bevoelkerung/'
# 1) arrivals series T12 (2025 file)
ws=openpyxl.load_workbook(R%2025,data_only=True)['T12']
rows=[]
for r in ws.iter_rows(min_row=5,values_only=True):
    r=[c for c in r if c is not None]
    if len(r)==7 and isinstance(r[0],int): rows.append((r[0],r[6]))
with open(D+'ag_romanians_arrivals_1973_2025.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['canton','year','indicator','persons','definition'])
    for y,v in rows: w.writerow(['Aargau',y,'immigration_from_abroad_romanian_nationals',v,'Zuzuege nach Herkunftsland Rumaenien (kantonale Bevoelkerungsstatistik, Tab. 12)'])
# 2) flows 2019-2025 (arrivals, departures, balance) by sex and CH/foreign nationality
out=[]
def add(y,ind,v):
    for lab,i in (('total_all',0),('men_all',1),('women_all',2),('foreign_total',6),('foreign_men',7),('foreign_women',8)):
        out.append(['Aargau',y,ind,lab,v[i]])
for y in range(2019,2026):
    wb=openpyxl.load_workbook(R%y,data_only=True)
    for sn in wb.sheetnames:
        if sn[:3] not in('T11','T12'): continue
        for r in wb[sn].iter_rows(values_only=True):
            c=[x for x in r if x is not None]
            if c and c[0]=='Rumänien' and len(c)>=9 and isinstance(c[1],int):
                title=str(wb[sn]['A1'].value or '')
                if y<=2023:
                    tag={'T11':None,'T12':'balance'}[sn[:3]]
                    if sn=='T11': tag='immigration' if not any(o[1]==y and o[2]=='immigration' for o in out) else 'emigration'
                else:
                    tag={'T11a':'immigration','T11b':'emigration','T11c':'balance'}.get(sn)
                if tag: add(y,tag,c[1:10])
with open(D+'ag_romanians_migration_2019_2025.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['canton','year','indicator','group','persons']);w.writerows(out)
# 3) stock 2025 (T22)
for r in openpyxl.load_workbook(R%2025,data_only=True)['T22'].iter_rows(values_only=True):
    c=[x for x in r if x is not None]
    if 'Rumänien' in c: st=c[c.index('Rumänien')+1-7+0:] if False else [None]*6+c[c.index('Rumänien')+1:c.index('Rumänien')+4]
with open(D+'ag_romanians_stock_2025.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['canton','year','reference_date','sex','persons','definition'])
    for s,v in (('total',st[6]),('men',st[7]),('women',st[8])): w.writerow(['Aargau',2025,'31-12',s,v,'staendige auslaendische Wohnbevoelkerung, kantonales Einwohnerregister (Tab. 22)'])
# 4) crosscheck
bfs={}
for r in csv.DictReader(open('/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv')):
    if r['population_type']=='Ständige Wohnbevölkerung' and r['permit']=='Anwesenheitsbewilligung - Total' and r['sex']=='Geschlecht - Total' and r['age_class']=='Altersklasse - Total':
        bfs[(r['canton'],int(r['year']))]=int(r['persons'])
with open(D+'cantonal_crosscheck.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow('canton,year,cantonal_value,cantonal_definition,bfs_value,diff_abs,diff_pct,source_url'.split(','))
    c=st[6];b=bfs[('Aargau',2025)]
    w.writerow(['Aargau',2025,c,'staendige auslaendische Wohnbevoelkerung 31.12., kant. Einwohnerregister',b,c-b,round((c-b)/b*100,2),U+'2025/edossier-bev-lkerung-2025-jahrespublikation.xlsx (Tab. 22)'])
    for k in ('Luzern','Zug','Schwyz'):
        w.writerow([k,2025,'',"not published for Romania in reachable sources",bfs[(k,2025)],'','',''])
    for k in ('Aargau','Luzern','Zug','Schwyz'): print(k,[ (y,bfs.get((k,y))) for y in (2010,2015,2019,2020,2025)])
print(rows[-8:],st)
