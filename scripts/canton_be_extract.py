import openpyxl,csv,sys,warnings,re
warnings.filterwarnings("ignore")
D="/home/user/Diaspora/data/canton_be/"
URL="https://www.fin.be.ch/content/dam/fin/dokumente/de/finanzverwaltung/statistik/bev%C3%B6lkerungsstatistik/bev%C3%B6lkerungsstand-und--struktur/2026/Staendige_ausl_WB_im_Kt_Bern_nach_detaill_Staatsangehoerigkeit_1990-2025_d.xlsx"
ws=openpyxl.load_workbook(D+"raw/nat_1990_2025.xlsx",data_only=True).active
rows=list(ws.iter_rows(values_only=True))
yrs=[int(re.sub(r'\D','',str(y))) if y else None for y in rows[2][1:]]
break_year=2010
out=[];tot={};rom={}
names=[]
for r in rows[3:]:
    if r[0] and isinstance(r[1],(int,float)):
        n=r[0].strip(); names.append(n)
        for y,v in zip(yrs,r[1:]):
            if y is None or v is None: continue
            out.append((n,int(y),v))
            if n=='Rumänien': rom[int(y)]=v
with open(D+"be_foreign_resident_by_nationality_1990_2025.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow(["canton","nationality_de","year","permanent_resident_population_31dec"])
    for n,y,v in out: w.writerow(["Bern",n,y,v])
# crosscheck
bfs={}
for r in csv.DictReader(open("/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv",encoding="utf-8")):
    if r["canton"].startswith("Bern") and r["population_type"]=="Ständige Wohnbevölkerung" and r["permit"].endswith("Total") and r["sex"].startswith("Geschlecht") and r["age_class"].endswith("Total"):
        bfs[int(r["year"])]=int(r["persons"])
with open(D+"cantonal_crosscheck.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f);w.writerow("canton,year,cantonal_value,cantonal_definition,bfs_value,diff_abs,diff_pct,source_url".split(","))
    for y in sorted(bfs):
        c=rom[y];b=bfs[y]
        w.writerow(["Bern",y,c,"permanent resident population (STATPOP from 2010), 31 Dec, nationality Romania; canton FV Bern re-publication",b,c-b,round((c-b)/b*100,2),URL])
print({y:(rom[y],bfs[y]) for y in sorted(bfs)})
