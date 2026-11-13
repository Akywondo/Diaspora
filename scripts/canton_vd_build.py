import openpyxl,csv,sys,re
R='/home/user/Diaspora/data/canton_vd/'
U='https://www.vd.ch/fileadmin/user_upload/organisation/dfin/statvd/Dom_01/Tableaux/'
def rows(f,sh):
    ws=openpyxl.load_workbook(R+'raw/'+f,read_only=True,data_only=True)[sh]
    return [list(r) for r in ws.iter_rows(values_only=True)]
# 1 foreign pop by nationality: Romania + total + Bulgaria + a few
rs=rows('T01.02.18.xlsx','Serie')
hdr=next(r for r in rs if r and any(c==2000 for c in r))
yrs=[int(re.match(r'\d{4}',str(c)).group()) for c in hdr if c is not None]
col=[i for i,c in enumerate(hdr) if c is not None]
out=[]
for r in rs:
    lab=(r[col[0]-1] if col[0]>0 else None) or ''
    lab=next((c for c in r if isinstance(c,str)),None)
    if lab and lab.strip() in ('Roumanie','Bulgarie','Pologne','Total population étrangère'):
        for y,i in zip(yrs,col):
            v=r[i]
            if isinstance(v,(int,float)): out.append(dict(canton='Vaud',year=y,nationality=lab.strip(),persons=int(v),
              definition='permanent resident foreign population, 31 Dec (2000-2013 SEM/ZAR; from 2014 cantonal register RCPers; from 2017 incl. asylum >=1y and intl officials)',source_table='T01.02.18',source_url=U+'T01.02.18.xlsx'))
w=csv.DictWriter(open(R+'vd_foreign_population_by_nationality_series.csv','w',newline='',encoding='utf-8'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
# asylum
rs=rows('T01.02.23.xlsx','Serie'); h=next(r for r in rs if r and r[0]=='Nationalité' or (r and 'Nationalité' in r))
ro=next(r for r in rs if 'Roumanie' in r)
o2=[]
for i,c in enumerate(h):
    m=re.match(r'\d{4}',str(c)) if c is not None else None
    if m: 
        v=ro[i]; o2.append(dict(canton='Vaud',year=int(m.group()),nationality='Roumanie',new_asylum_applications=(0 if v=='–' else int(v)),note=('dash in source = 0' if v=='–' else ''),source_url=U+'T01.02.23.xlsx'))
w=csv.DictWriter(open(R+'vd_romania_new_asylum_applications.csv','w',newline='',encoding='utf-8'),fieldnames=list(o2[0]));w.writeheader();w.writerows(o2)
# crosscheck
bfs={}
for r in csv.DictReader(open('/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv',encoding='utf-8')):
    if r['canton'].startswith('Vaud') and r['permit'].endswith('Total') and r['sex'].endswith('Total') and r['age_class'].endswith('Total') and r['population_type'].startswith('Ständ'):
        bfs[int(r['year'])]=int(r['persons'])
o3=[]
for d in out:
    if d['nationality']=='Roumanie' and d['year'] in bfs:
        b=bfs[d['year']]; c=d['persons']
        o3.append(dict(canton='Vaud',year=d['year'],cantonal_value=c,cantonal_definition=d['definition'],bfs_value=b,diff_abs=c-b,diff_pct=round(100*(c-b)/b,2),source_url=d['source_url']))
w=csv.DictWriter(open(R+'cantonal_crosscheck.csv','w',newline='',encoding='utf-8'),fieldnames=list(o3[0]));w.writeheader();w.writerows(o3)
for d in o3: print(d['year'],d['cantonal_value'],d['bfs_value'],d['diff_abs'],d['diff_pct'])

# naturalisations
wb=openpyxl.load_workbook(R+'raw/x/Dom_01__Tableaux__T01.03.05.xlsx',read_only=True,data_only=True)
def get(sh,lab):
    rs=[list(r) for r in wb[sh].iter_rows(values_only=True)]
    h=next(r for r in rs if 'Nationalité' in r); idx=[i for i,c in enumerate(h) if isinstance(c,int)]
    r=next(r for r in rs if any(isinstance(c,str) and c.strip()==lab for c in r))
    return {h[i]:r[i] for i in idx}
a=get('Serie','Roumanie');t=get('Serie','Total');q=get('Taux','Roumanie')
o4=[dict(canton='Vaud',year=y,romanians_naturalised=a[y],all_nationalities_naturalised=t[y],romania_acquisition_rate_pct=round(q[y],3),
  source='SEM SYMIC via Statistique Vaud T01.03.05',source_url=U+'T01.03.05.xlsx',note='rate = acquisitions as % of foreign population (of that nationality) at start of year') for y in sorted(a)]
w=csv.DictWriter(open(R+'vd_romanians_naturalisations.csv','w',newline='',encoding='utf-8'),fieldnames=list(o4[0]));w.writeheader();w.writerows(o4)
