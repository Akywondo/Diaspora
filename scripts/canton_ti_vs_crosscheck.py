import csv
rows=[]
for r in csv.DictReader(open('/home/user/Diaspora/data/_reference/bfs_romanians_canton_year_permit_sex.csv')):
    if r['canton'] in('Ticino','Valais / Wallis') and r['permit'].endswith('Total') and r['sex'].endswith('Total') and r['population_type'].startswith('Ständ'):
        rows.append(r)
with open('/home/user/Diaspora/data/canton_ti_vs/cantonal_crosscheck.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow('canton year cantonal_value cantonal_definition bfs_value diff_abs diff_pct source_url'.split())
    for r in rows:
        w.writerow([r['canton'],r['year'],'','NOT RETRIEVED (cantonal host blocked / no Romania figure published in accessible docs)',r['persons'],'','','https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-0103010000_101/px-x-0103010000_101.px'])
