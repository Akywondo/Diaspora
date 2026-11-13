"""Build tidy CSVs for canton_zh from raw downloads (run with python3 -I ... not needed; reads only data)."""
import csv,re,glob,openpyxl,zipfile,os
D='/home/user/Diaspora/data/canton_zh/'; R=D+'raw/'
def wr(fn,rows,cols):
    with open(D+fn,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
# 1 canton civil-law population (xlsx has broken drawing refs -> parse XML)
z=zipfile.ZipFile(R+'KTZH_00001143_00002169.xlsx')
ss=z.read('xl/sharedStrings.xml').decode()
t=[''.join(re.findall(r'<t[^>]*>([^<]*)</t>',x)) for x in re.findall(r'<si>(.*?)</si>',ss,re.S)]
x=z.read('xl/worksheets/sheet2.xml').decode()
hdr=None;rom=None
for row in re.findall(r'<row [^>]*>(.*?)</row>',x,re.S):
    vals=[]
    for ref,attr,inner in re.findall(r'<c r="([A-Z]+)\d+"([^>]*?)(?:/>|>(.*?)</c>)',row,re.S):
        v=re.search(r'<v>(.*?)</v>',inner or '')
        if v: vals.append(t[int(v.group(1))].strip() if 't="s"' in attr else v.group(1))
    if vals and vals[0].startswith('BFS_'): hdr=vals
    if len(vals)>2 and vals[1]=='Rumänien': rom=vals
out=[]
for h,v in zip(hdr,rom):
    m=re.fullmatch(r'TOTAL_(\d{4})',h)
    if m: out.append(dict(year=m.group(1),canton='Zürich',nationality='Rumänien',persons=v,definition='zivilrechtliche Wohnbevölkerung (Hauptwohnsitz), 31.12.; 2025 provisorisch'))
wr('romanians_canton_zh_civil_population_by_year.csv',out,list(out[0]))
cz={int(r['year']):int(r['persons']) for r in out}
# 2 ZEMIS 2016-2018
rows=[]
for fn,y in [('KTZH_00000123_00001228.xlsx',2016),('KTZH_00000123_00001229.xlsx',2017),('KTZH_00000123_00001230.xlsx',2018)]:
    wb=openpyxl.load_workbook(R+fn,read_only=True,data_only=True)
    for s in wb:
        for r in s.iter_rows(values_only=True):
            if 'Rumänien' in r:
                lvl=r[0]; name=r[1]; n=[c for c in r[3:] if isinstance(c,(int,float))]
                rows.append(dict(year=y,level=lvl,area=name,nationality='Rumänien',persons=r[3]))
wr('romanians_zh_municipality_zemis_2016_2018.csv',rows,list(rows[0]))
zem={r['year']:r['persons'] for r in rows if r['level']=='Kanton'}
# 3 city of Zürich
def load(fn): return list(csv.DictReader(open(R+fn,encoding='utf-8')))
g=lambda p: glob.glob(R+p)[0].split('/')[-1]
o=[dict(year=r['StichtagDatJahr'],persons=r['AnzBestWir']) for r in load(g('city_bev_bestand_nationen_hist_jahr_od3482*'))]
wr('romanians_city_zurich_by_year.csv',o,['year','persons'])
o=[dict(year=r['StichtagDatJahr'],sex=r['SexLang'],persons=r['AnzBestWir']) for r in load(g('city_bev_bestand_nationen_geschlecht*'))]
wr('romanians_city_zurich_by_year_sex.csv',o,['year','sex','persons'])
o=[dict(year=r['StichtagDatJahr'],quartier_code=r['QuarCd'],quartier=r['QuarLang'],persons=r['AnzBestWir']) for r in load(g('city_bev_bestand_jahr_quartier*'))]
wr('romanians_city_zurich_by_quartier_year.csv',o,['year','quartier_code','quartier','persons'])
o=[dict(year=r['StichtagDatJahr'],permit_group=r['AufArt2AggLang_noDM'],sex=r['SexLang'],persons=r['AnzBestWir']) for r in load(g('city_bev_bestand_jahr_nationalitaet_aufenthaltsart*'))]
wr('romanians_city_zurich_by_permit_sex_year.csv',o,['year','permit_group','sex','persons'])
o=[dict(year=r['StichtagDatJahr'],sex=r['SexKurz'],live_birth_flag=r['LebensfaehigkeitLang'],births=r['AnzGebuWir']) for r in load(g('city_bev_geburten*'))]
wr('romanians_city_zurich_births_by_year.csv',o,['year','sex','live_birth_flag','births'])
o=[dict(year=r['StichtagDatJahr'],sex=r['SexKurz'],age_group=r['AlterV20Kurz'],naturalisations=r['AnzEinbWir']) for r in load(g('city_bev_brw*'))]
wr('romanians_city_zurich_naturalisations_by_year_sex_age.csv',o,['year','sex','age_group','naturalisations'])
o=[dict(role='partner1_romanian',year=r['StichtagDatJahr'],partner1_nat=r['NationEp1HistLang'],partner2_nat=r['NationEp2HistLang'],sex1=r['SexEp1Lang'],sex2=r['SexEp2Lang'],marriages=r['AnzSchl']) for r in load('city_bev_ehe_nationalitaet_od3305__NationEp1HistLang.csv')]
o+=[dict(role='partner2_romanian',year=r['StichtagDatJahr'],partner1_nat=r['NationEp1HistLang'],partner2_nat=r['NationEp2HistLang'],sex1=r['SexEp1Lang'],sex2=r['SexEp2Lang'],marriages=r['AnzSchl']) for r in load('city_bev_ehe_nationalitaet_od3305__NationEp2HistLang.csv')]
wr('romanians_city_zurich_marriages.csv',o,list(o[0]))
o=[dict(year=r['Jahr'],month=r['MonatSort'],date=r['StichtagDat'],status=r['AufenthaltsstatusLang'],sex=r['SexLang'],persons=r['Anzahl']) for r in load(g('city_bev_monat_asyl*'))]
wr('romanians_city_zurich_asylum_sector_monthly.csv',o,['year','month','date','status','sex','persons'])
# 4 net migration from statistik.info 2015/09 table 1
nm=[('2002',57),('2009',104),('2014',213),('Jan-Oct 2015',107)]
wr('romanians_canton_zh_international_net_migration.csv',[dict(period=p,canton='Zürich',nationality='Rumänien',net_international_migration=v,source='statistik.info 2015/09 Tabelle 1 (ZEMIS), ständige ausländische Wohnbevölkerung') for p,v in nm],['period','canton','nationality','net_international_migration','source'])
# 5 crosscheck
ref={}
for r in csv.DictReader(open('/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv',encoding='utf-8')):
    if r['canton']=='Zürich' and r['population_type']=='Ständige Wohnbevölkerung' and r['sex']=='Geschlecht - Total' and r['permit']=='Anwesenheitsbewilligung - Total' and r['age_class']=='Altersklasse - Total': ref[int(r['year'])]=int(r['persons'])
cc=[]
U1='https://www.web.statistik.zh.ch/ogd/daten/ressourcen/KTZH_00001143_00002169.xlsx'
def add(y,v,d,u):
    b=ref[y]; cc.append(dict(canton='Zürich',year=y,cantonal_value=v,cantonal_definition=d,bfs_value=b,diff_abs=v-b,diff_pct=round((v-b)/b*100,2),source_url=u))
for y in sorted(cz): add(y,cz[y],'Kantonale Bevölkerungserhebung: zivilrechtliche Wohnbevölkerung (Hauptwohnsitz) 31.12.'+(' (provisional)' if y==2025 else ''),U1)
for y,u in [(2016,'KTZH_00000123_00001228'),(2017,'KTZH_00000123_00001229'),(2018,'KTZH_00000123_00001230')]:
    add(y,int(zem[y]),'Ständige ausländische Wohnbevölkerung (SEM ZEMIS-based, 31.12.)','https://www.web.statistik.zh.ch/ogd/daten/ressourcen/%s.xlsx'%u)
cc.sort(key=lambda r:(r['year'],r['cantonal_definition']))
wr('cantonal_crosscheck.csv',cc,list(cc[0]))
for r in cc: print(r['year'],r['cantonal_value'],r['bfs_value'],r['diff_abs'],r['diff_pct'],r['cantonal_definition'][:30])
