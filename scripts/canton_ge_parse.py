import openpyxl,csv,re,sys,os
R="/home/user/Diaspora/data/canton_ge/raw/"
O="/home/user/Diaspora/data/canton_ge/"
BASE="https://statistique.ge.ch/statistique/tel/domaines/01/"
def num(c):
    if isinstance(c,(int,float)): return c
    return None
def flag(c):
    return '' if isinstance(c,(int,float)) else (str(c).strip() if c is not None else '')
def rom_row(ws):
    for r in ws.iter_rows(values_only=True):
        if isinstance(r[0],str) and r[0].strip()=='Roumanie': return list(r)
def tot_row(ws,names):
    for r in ws.iter_rows(values_only=True):
        if isinstance(r[0],str) and r[0].strip() in names: return list(r)
def yearhdr(ws):
    for i,r in enumerate(ws.iter_rows(values_only=True),1):
        if i==8: return r
def yr(c):
    m=re.match(r'(\d{4})',str(c)); return int(m.group(1)) if m else None
def series(files,tab,title,measure,unit,dfn,outrows,totnames):
    for f,d in files:
        wb=openpyxl.load_workbook(R+f+'.xlsx',data_only=True)
        for ws in wb:
            h=yearhdr(ws); rr=rom_row(ws); tt=tot_row(ws,totnames)
            if not rr: continue
            for j,c in enumerate(h):
                y=yr(c)
                if y is None or j==0: continue
                v=rr[j] if j<len(rr) else None
                if v is None: continue
                note='' if str(c).strip()==str(y) else 'column label: '+str(c)
                outrows.append(dict(table=tab,year=y,measure=measure,value=num(v) if num(v) is not None else '',suppressed_flag=flag(v),
                  unit=unit,canton_total=(num(tt[j]) if tt and num(tt[j]) is not None else ''),definition=dfn,notes=note,source_url=BASE+d+'/'+f+'.xlsx'))
rows=[]
series([('T_01_01_8_05','01_01'),('T_01_01_8_05_1989-2013','01_01')],'T 01.01.8.05','','resident_population_romanian_nationals','persons',
 'OCSTAT cantonal population statistics, population residante (permanent+non-permanent incl. international officials and asylum domain) at 31 Dec; nationality',rows,{'Population totale','Total'})
# dedupe: keep overlap years from newer file (2013 appears in both)
seen={};
for r in rows: seen[(r['year'],r['notes'])]=r  # later file overrides? order: new first then old -> keep new
rows2={}
for r in rows:
    k=(r['year'],r['notes'])
    if k not in rows2: rows2[k]=r
rows=sorted(rows2.values(),key=lambda r:(r['year'],r['notes']))
def write(name,rs):
    fn=O+name
    with open(fn,'w',newline='',encoding='utf-8') as fh:
        w=csv.DictWriter(fh,fieldnames=list(rs[0].keys())); w.writeheader(); w.writerows(rs)
    print(name,len(rs))
write('ge_romanians_resident_stock_by_year.csv',rows)

flows=[]
for meas,fl in [('immigrants_from_abroad','T_01_02_1_08'),('emigrants_to_abroad','T_01_02_1_09'),('net_external_migration','T_01_02_1_10')]:
    tab=fl.replace('T_','T ').replace('_','.')
    tmp=[]
    series([(fl,'01_02'),(fl+'_1989-2013','01_02')],tab,'',meas,'persons','OCSTAT external migration movement (to/from abroad), annual totals, by nationality',tmp,{'Immigrés','Emigrés','Solde migratoire','Total'})
    seen={}
    for r in tmp:
        k=(r['year'],r['notes'])
        if k not in seen: seen[k]=r
    flows+=sorted(seen.values(),key=lambda r:(r['year'],r['notes']))
write('ge_romanians_external_migration_by_year.csv',flows)

# age groups
age=[]
for yy,(f,d) in [(None,('T_01_01_8_06','01_01'))]: pass
for f in ['T_01_01_8_06','T_01_01_8_06_1989-2013']:
    wb=openpyxl.load_workbook(R+f+'.xlsx',data_only=True)
    for ws in wb:
        y=int(ws.title)
        rr=rom_row(ws)
        if not rr: continue
        tt=tot_row(ws,{'Population totale','Total'})
        vals=[c for c in rr[1:] if c is not None]
        labs=['0-19','20-39','40-64','65+','total']
        if len(vals)!=5: print('AGE anomaly',f,y,vals); continue
        for l,v in zip(labs,vals):
            age.append(dict(table='T 01.01.8.06',year=y,age_group=l,value=num(v) if num(v) is not None else '',suppressed_flag=flag(v),unit='persons',definition='foreign resident population by age group and nationality, 31 Dec',source_url=BASE+'01_01/'+f+'.xlsx'))
seen={}
for r in age:
    k=(r['year'],r['age_group'])
    if k not in seen: seen[k]=r
write('ge_romanians_by_age_group.csv',sorted(seen.values(),key=lambda r:(r['year'],r['age_group'])))

# permits
perm=[]
L7=['short_stay_L','residence_B','settled_C','international_officials','asylum_domain','temporary_protection_S','total']
L6=['short_stay_L','residence_B','settled_C','international_officials','asylum_domain','total']
Lold=['short_term_resident','long_term_resident_BC_L12plus','international_officials','asylum_domain','total']
for f in ['T_01_01_8_07','T_01_01_8_07_1989-2013']:
    wb=openpyxl.load_workbook(R+f+'.xlsx',data_only=True)
    for ws in wb:
        y=int(ws.title); rr=rom_row(ws)
        if not rr: continue
        vals=[c for c in rr[1:] if c is not None]
        labs={7:L7,6:L6,5:Lold}.get(len(vals))
        if not labs: print('PERM anomaly',f,y,vals); continue
        sch='old (to 2013): short-term/long-term/international/asylum' if len(vals)==5 else 'from 2014: permit-based'
        for l,v in zip(labs,vals):
            perm.append(dict(table='T 01.01.8.07',year=y,permit_category=l,value=num(v) if num(v) is not None else '',suppressed_flag=flag(v),unit='persons',category_scheme=sch,definition='foreign resident population by residence permit type and nationality, 31 Dec; ( ) = suppressed for data protection; - = zero',source_url=BASE+'01_01/'+f+'.xlsx'))
seen={}
for r in perm:
    k=(r['year'],r['permit_category'])
    if k not in seen: seen[k]=r
write('ge_romanians_by_permit_type.csv',sorted(seen.values(),key=lambda r:(r['year'],r['permit_category'])))

# naturalisations
nat=[]
wb=openpyxl.load_workbook(R+'T_01_02_9_02.xlsx',data_only=True)
for ws in wb:
    h=yearhdr(ws); rr=rom_row(ws); tt=tot_row(ws,{'Total'})
    if not rr: continue
    for j,c in enumerate(h):
        y=yr(c)
        if y is None or j==0 or rr[j] is None: continue
        nat.append(dict(table='T 01.02.9.02',year=y,value=num(rr[j]) if num(rr[j]) is not None else '',suppressed_flag=flag(rr[j]),unit='persons',canton_total=num(tt[j]) if tt and num(tt[j]) is not None else '',definition='naturalisations (ordinary, facilitated, reintegration) of permanent residents of canton Geneva by former nationality; SEM/SYMIC data',source_url=BASE+'01_02/T_01_02_9_02.xlsx',sheet=ws.title))
write('ge_romanians_naturalisations_by_year.csv',sorted(nat,key=lambda r:r['year']))
