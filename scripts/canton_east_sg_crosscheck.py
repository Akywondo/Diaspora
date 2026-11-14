import openpyxl,csv,re,pdfplumber
R='/home/user/Diaspora/data/canton_east/'
ref={}
for r in csv.DictReader(open('/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv',encoding='utf8')):
    if r['population_type']=='Ständige Wohnbevölkerung' and r['permit'].startswith('Anwesenheitsbewilligung - Total') and r['sex'].startswith('Geschlecht - Total') and r['age_class'].startswith('Altersklasse - Total'):
        ref[(r['canton'],int(r['year']))]=int(r['persons'])
print(sorted({k[0] for k in ref if 'Gallen' in k[0] or 'Thurgau' in k[0]}))
# SG series from PDF (ZEMIS, SEM definition)
p=pdfplumber.open(R+'raw/sg_ausl002.pdf');pg=p.pages[2].extract_text().split('\n')
yrs=list(range(2024,1990,-1));sg={}
for i,l in enumerate(pg):
    if l.strip()=='Rumänien':
        vals=[int(x.replace("'",'')) for x in pg[i+1].replace('Anzahl','').split()]
        sg=dict(zip(yrs,vals));break
print(len(sg),sg[2024],sg[2010])
# SG xlsx sheet 003 (2015-2024 first values 2852 differs by 1 for 2024)
ws=openpyxl.load_workbook(R+'raw/sg_ausl003.xlsx',data_only=True)['Kanton']
hdr=[r for r in ws.iter_rows(values_only=True) if r[0] and 'Staatsang' in str(r[0]) or (r[1]==2024)][:2]
sg3=None
for r in ws.iter_rows(values_only=True):
    if r[0]=='Rumänien': sg3=r[1:11]
print('ausl003 Romania row',sg3, [r[:11] for r in ws.iter_rows(min_row=4,max_row=9,values_only=True)][:4])
with open(R+'sg_romanians_permanent_foreign_resident_by_year.csv','w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['canton','year','nationality','persons','definition','source_file'])
    for y in sorted(sg): w.writerow(['SG',y,'Rumänien',sg[y],'ZEMIS/SEM permanent foreign resident pop. 31 Dec','B01_Ausl_002 (I_78) PDF p.3'])
# municipal 2024
ws=openpyxl.load_workbook(R+'raw/sg_ausl002.xlsx',data_only=True)['WK und Gemeinden Dez']
rows=list(ws.iter_rows(values_only=True))
hr=rows[5];c=hr.index('Rumänien');tc=hr.index('Total')
out=[]
for r in rows[6:]:
    nm=r[0] if isinstance(r[0],str) else (r[1] if isinstance(r[1],str) else None)
    if nm and r[c] is not None: out.append(['SG',2024,nm.strip(),r[tc] if r[tc] is not None else '',r[c]])
with open(R+'sg_romanians_by_municipality_2024.csv','w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['canton','year','unit','total_foreign_pop','romanian_nationals']);w.writerows(out)
print(len(out),[o for o in out if 'Buchs' in o[2] or 'Kanton' in o[2] or 'Werdenberg' in o[2] or 'Rheintal' in o[2]])
# crosscheck
tg={}
for r in csv.DictReader(open(R+'tg_romanians_by_year_permit.csv',encoding='utf8')):
    if r['nationality']=='Rumänien' and r['measure']=='total_foreign_permanent_resident': tg[int(r['year'])]=int(r['persons'])
rows=[]
def add(c,name,y,v,d,u):
    b=ref.get((name,y))
    if b is None: return
    rows.append([c,y,v,d,b,v-b,round((v-b)/b*100,2),u])
for y,v in sg.items(): add('SG','St. Gallen',y,v,'SG Fachstelle fuer Statistik, ZEMIS permanent foreign residents 31 Dec','https://www.sg.ch/content/dam/sgch/kanton-stgallen/statistik/b01/B01_Ausl_002_staendigeAuslWB_Staatsangeh%C3%B6rigkeit_Kt_WK_Gem.pdf')
for y,v in tg.items(): add('TG','Thurgau',y,v,'TG Amt fuer Daten und Statistik, permanent foreign residents 31 Dec','https://statistik.tg.ch/public/upload/assets/186079/2025_2015_BevKant_AuslStaatsangehoerigkeit.xlsx')
with open(R+'cantonal_crosscheck.csv','w',newline='',encoding='utf8') as f:
    w=csv.writer(f);w.writerow(['canton','year','cantonal_value','cantonal_definition','bfs_value','diff_abs','diff_pct','source_url']);w.writerows(rows)
for r in rows:
    if r[1] in (2010,2015,2020,2023,2024,2025): print(r[:2],r[2],r[4],r[5],r[6])
print(len(rows))
