"""Builds CSVs for canton_be_fr_so from the reference extract and values transcribed from
downloaded official cantonal documents (see SOURCES.md). Run: python3 -I scripts/canton_be_fr_so_build.py"""
import csv
REF='/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv'
OUT='/home/user/Diaspora/data/canton_be_fr_so/'
ref=list(csv.DictReader(open(REF,encoding='utf8')))
CN={'Fribourg':'Fribourg / Freiburg','Solothurn':'Solothurn','Bern':'Bern / Berne'}
def bfs(c,y,t,p='Anwesenheitsbewilligung - Total',s='Geschlecht - Total'):
    v=[int(x['persons']) for x in ref if x['canton']==CN[c] and x['year']==str(y) and x['population_type']==t and x['permit']==p and x['sex']==s]
    return v[0] if v else None
PERM='Ständige Wohnbevölkerung'; NP='Nichtständige Wohnbevölkerung'
FR_URL='https://www.fr.ch/sites/default/files/2020-03/Annuaire%20statistique%20du%20canton%20de%20Fribourg%20-%20Edition%202020.pdf (T01-11, 2015-2018); https://www.fr.ch/sites/default/files/2023-05/annuaire-statistique-du-canton-de-fribourg--edition-2023_0.pdf (T01-11, 2010, 2019-2021)'
FR_DEF='Dec stock, foreign resident population permanent + non-permanent (STATPOP-based), nationality Romania'
fr={2010:325,2015:559,2016:636,2017:692,2018:797,2019:846,2020:922,2021:1030}
SO_DEF='31 Dec, cantonal GERES/RREG definition (RRB 2012/597): all with main residence incl. B,C,L,F,N,S; wider than BFS permanent'
so={2021:(1191,'https://so.ch/fileadmin/internet/fd/fd-afin/stat/01/Wohnbevoelkerung_2021.pdf'),
    2022:(1524,'https://so.ch/fileadmin/internet/fd/fd-afin/stat/01/Wohnbevoelkerung_2022.pdf'),
    2023:(1762,'https://so.ch/fileadmin/internet/fd/fd-afin/stat/01/bevoelkerungszahlen/Wohnbevoelkerung_2023.pdf'),
    2024:(1915,'https://so.ch/fileadmin/internet/fd/fd-afin/stat/01/Solothurn_zaehlt_25.pdf'),
    2025:(2052,'https://so.ch/fileadmin/internet/fd/fd-afin/stat/01/bevoelkerungszahlen/Solothurn_zaehlt_2026.pdf')}
# series file
with open(OUT+'cantonal_romanians_series.csv','w',newline='',encoding='utf8') as f:
    w=csv.writer(f); w.writerow(['canton','year','sex','value','definition','source_url'])
    for y,v in fr.items(): w.writerow(['Fribourg',y,'total',v,FR_DEF,FR_URL])
    for y,(v,u) in so.items(): w.writerow(['Solothurn',y,'total',v,SO_DEF,u])
    sx=so[5][0] if False else None
    w.writerow(['Solothurn',2025,'male',1176,SO_DEF,so[2025][1]]); w.writerow(['Solothurn',2025,'female',876,SO_DEF,so[2025][1]])
    w.writerow(['Solothurn',2024,'male',1041,SO_DEF,so[2024][1]]); w.writerow(['Solothurn',2024,'female',874,SO_DEF,so[2024][1]])
# crosscheck
rows=[]
def add(c,y,v,d,t_list,u):
    b=sum(bfs(c,y,t) for t in t_list)
    rows.append([c,y,v,d,b,v-b,round(100*(v-b)/b,2),u])
for y,v in fr.items(): add('Fribourg',y,v,FR_DEF+' | BFS comparator = permanent + non-permanent',[PERM,NP],FR_URL)
for y,(v,u) in so.items():
    add('Solothurn',y,v,SO_DEF+' | BFS comparator = permanent + non-permanent',[PERM,NP],u)
    add('Solothurn',y,v,SO_DEF+' | BFS comparator = permanent only',[PERM],u)
# FR 2010-2025 change in permanent pop quoted by SStat page
v=1105; b=bfs('Fribourg',2025,PERM)-bfs('Fribourg',2010,PERM)
rows.append(['Fribourg','2010-2025 change',v,'Increase 2010-2025 permanent resident pop., nationality Romania (text on SStat page)',b,v-b,0.0,'https://www.fr.ch/deef/ssd/statistiques-par-themes/migration-et-integration'])
with open(OUT+'cantonal_crosscheck.csv','w',newline='',encoding='utf8') as f:
    w=csv.writer(f); w.writerow(['canton','year','cantonal_value','cantonal_definition','bfs_value','diff_abs','diff_pct','source_url']); w.writerows(rows)
# SO profile from BFS reference
perms=['Anwesenheitsbewilligung - Total','Niedergelassener (C)','Aufenthalter (B)','Aufenthalter mit Erwerbstätigkeit (Ci)','Kurzaufenthalter (L)','Vorläufig Aufgenommener (F)','Asylsuchender (N)','Schutzbedürftiger (S)','Schweizer']
with open(OUT+'bfs_so_fr_be_permit_sex_profile.csv','w',newline='',encoding='utf8') as f:
    w=csv.writer(f); w.writerow(['canton','year','population_type','permit','sex','persons','source'])
    for x in ref:
        if x['canton'] in CN.values() and x['permit'] in perms:
            w.writerow([x['canton'],x['year'],x['population_type'],x['permit'],x['sex'],x['persons'],'derived from data/_reference/bfs_romanians_canton_year_permit_sex.csv (BFS STATPOP)'])
for r in rows: print(r[:3],r[4:7])
print('SO shares')
for y in range(2010,2026):
    t=bfs('Solothurn',y,PERM); b=bfs('Solothurn',y,PERM,'Aufenthalter (B)'); c=bfs('Solothurn',y,PERM,'Niedergelassener (C)')
    m=bfs('Solothurn',y,PERM,s='Mann'); n=bfs('Solothurn',y,NP)
    ch=bfs('Solothurn',y,PERM,'Schweizer')
    print(y,t,'B%',round(100*b/t),'C%',round(100*c/t),'male%',round(100*m/t),'nonperm',n,'CH',ch)
