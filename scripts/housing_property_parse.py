import openpyxl,csv,sys,os
R='/home/user/Diaspora/data/housing_property/'; RAW=R+'raw/'
def rows(ws): 
    for r in ws.iter_rows(values_only=True):
        c=[x for x in r if x is not None]
        if c: yield c
num=lambda x: isinstance(x,(int,float))
def w(name,hdr,data):
    with open(R+name,'w',newline='',encoding='utf-8') as f:
        cw=csv.writer(f); cw.writerow(hdr); cw.writerows(data)
    print(name,len(data))
# 1 tenure by household nationality (Grossregion)
G=['total','swiss_household','mixed_swiss_foreign_household','foreign_household']
out=[]
wb=openpyxl.load_workbook(RAW+'tenure_by_nationality_grossregion.xlsx',data_only=True)
for ws in wb.worksheets:
    reg=None
    for c in rows(ws):
        if len(c)==1 and isinstance(c[0],str) and c[0] in ('Schweiz','Genferseeregion','Espace Mittelland','Nordwestschweiz','Zürich','Ostschweiz','Zentralschweiz','Tessin'): reg=c[0]
        elif reg and isinstance(c[0],str) and len(c)==9 and all(num(x) for x in c[1:]):
            for i,g in enumerate(G): out.append([ws.title,reg,c[0],g,c[1+2*i],c[2+2*i]])
w('tenure_by_household_nationality_grossregion.csv',['year','region','tenure','household_nationality_group','share_percent','ci_pm_pp'],out)
# 2 rent by nationality
out=[]
wb=openpyxl.load_workbook(RAW+'rent_by_nationality_grossregion.xlsx',data_only=True)
for ws in wb.worksheets:
    reg=None
    for c in rows(ws):
        if isinstance(c[0],str) and len(c)==9 and all(num(x) for x in c[1:]):
            lab=c[0]
            if 'Zimmer' not in lab: reg=lab; lab='Total'
            if reg:
                for i,g in enumerate(G): out.append([ws.title,reg,lab,g,c[1+2*i],c[2+2*i]])
w('avg_net_rent_by_household_nationality_grossregion.csv',['year','region','rooms','household_nationality_group','avg_net_rent_chf_month','ci_pm_chf'],out)
# 3 rent by canton
out=[];cats=['total','1','2','3','4','5','6plus']
wb=openpyxl.load_workbook(RAW+'rent_canton.xlsx',data_only=True)
for ws in wb.worksheets:
    for c in rows(ws):
        if isinstance(c[0],str) and len(c)>=15 and num(c[1]) and (c[0]=='Schweiz' or c[0][0].isupper()) and not c[0].startswith('Durch'):
            v=c[1:]
            for i,k in enumerate(cats):
                if 2*i<len(v) and num(v[2*i]): out.append([ws.title,c[0],k,v[2*i],v[2*i+1] if 2*i+1<len(v) and num(v[2*i+1]) else ''])
w('avg_net_rent_by_canton_rooms.csv',['year','canton','rooms','avg_net_rent_chf_month','ci_pm_chf'],out)
# 4 ownership rate by canton (CSV)
code={'CH':'CH','CH040':'ZH','CH021':'BE','CH061':'LU','CH062':'UR','CH063':'SZ','CH064':'OW','CH065':'NW','CH051':'GL','CH066':'ZG','CH022':'FR','CH023':'SO','CH031':'BS','CH032':'BL','CH052':'SH','CH053':'AR','CH054':'AI','CH055':'SG','CH056':'GR','CH033':'AG','CH057':'TG','CH070':'TI','CH011':'VD','CH012':'VS','CH024':'NE','CH013':'GE','CH025':'JU'}
out=[]
for r in csv.DictReader(open(RAW+'own_canton.xlsx',encoding='utf-8-sig'),delimiter=';'):
    out.append([r['TIME_PERIOD'],code.get(r['GEO'],r['GEO']),r['GEO'],r['OBS_VALUE'],r['OBS_CONFIDENCE']])
w('home_ownership_rate_by_canton.csv',['year','canton','nuts_code','ownership_rate_percent','ci_pm_pp'],out)
# 5 living space per person by household migration status
out=[]
for f,grp,n in [('wohnflaeche_1pers.xlsx',['total','no_migration_background','migration_background'],3),('wohnflaeche_2plus.xlsx',['total','no_migration_background','migration_background','mixed'],4)]:
    wb=openpyxl.load_workbook(RAW+f,data_only=True)
    for ws in wb.worksheets:
        for c in rows(ws):
            if isinstance(c[0],str) and (c[0]=='Schweiz' or c[0][0].isupper()) and len(c)>=1+7*n and all(num(x) for x in c[1:1+7*n]):
                for j,ci in enumerate(cats):
                    for i,g in enumerate(grp):
                        out.append([ws.title,c[0],'1_person' if n==3 else '2plus_persons',ci,g,c[1+j*n+i]])
w('living_space_per_person_by_migration_status_canton.csv',['year','canton','household_size_class','rooms','household_migration_status','sqm_per_person'],out)
