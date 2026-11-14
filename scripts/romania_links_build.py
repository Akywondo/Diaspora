import csv
B='/home/user/Diaspora/data/romania_links/'
rows=list(csv.DictReader(open(B+'raw/dbl/20964155.csv',encoding='utf-8-sig'),delimiter=';'))
sx={'1':'men','2':'women','Total':'total'}; sc={'1':'with_second_citizenship','Total':'total','0':'unlabelled_code_0','88':'unlabelled_code_88'}
out=[]
for r in rows:
    if r['CTRYOFSECCITIZ']=='8232' and r['SECCITIZ'] in('1','Total'):
        out.append(dict(year=r['TIME_PERIOD'],second_citizenship_country='Romania',sex=sx[r['SEX']],swiss_group=sc[r['SECCITIZ']],persons=r['OBS_VALUE'] and round(float(r['OBS_VALUE'])),ci95_halfwidth_pct=r['OBS_CONFIDENCE'],bfs_status=r['OBS_STATUS']))
out.sort(key=lambda d:(d['year'],d['sex'],d['swiss_group']))
w=csv.DictWriter(open(B+'swiss_with_romanian_second_citizenship_2015_2020.csv','w',newline='',encoding='utf-8'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
tot={}
for r in rows:
    if r['CTRYOFSECCITIZ']=='Total' and r['SEX']=='Total' and r['SECCITIZ']=='1' and r['AGE']=='Total' and r['BIRTH_CTRY']=='Total' and r['CITIZBIRTHANDTODAY']=='Total'and r['CURRACT']=='Total' and r['SOCPROF']=='Total' and r['EDU']=='Total': tot[r['TIME_PERIOD']]=r['OBS_VALUE']
print(tot)
# census 2000
import io
raw=open(B+'raw/census2000_rumaenisch_raw.csv',encoding='latin-1').read()
rd=list(csv.reader(io.StringIO(raw)));
o=[]
for r in rd[1:]:
    o.append(dict(year=2000,residence_type=r[0],region=r[1].lstrip('- ').strip(),population_group=r[2].replace('Staatsangeh\xf6rigkeit - Total','Total').replace('Ausl\xe4nder','Foreigners').replace('Schweizer','Swiss'),all_main_languages_total=r[3],romanian_main_language=r[4]))
w=csv.DictWriter(open(B+'census2000_romanian_main_language_by_canton.csv','w',newline='',encoding='utf-8'),fieldnames=list(o[0]));w.writeheader();w.writerows(o)
print(len(o))
