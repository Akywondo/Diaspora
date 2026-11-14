import openpyxl,csv,sys
wb=openpyxl.load_workbook('/home/user/Diaspora/data/wages_income/raw/armutsquote_24205291.xlsx',data_only=True)
out=csv.writer(open('/home/user/Diaspora/data/wages_income/silc_poverty_rate_by_nationality_group.csv','w',newline=''))
out.writerow(['year','nationality_group','poor_persons_thousands','ci95_thousands','poverty_rate_pct','ci95_pct_points','share_of_total_population_pct','share_of_poor_pct'])
for ws in wb:
    on=False
    for r in ws.iter_rows(values_only=True):
        c=[x for x in r if x is not None]
        if not c: continue
        s=str(c[0]).strip()
        if s.startswith('Nationalität'): on=True; continue
        if on:
            if s in('Schweizer/innen','Ausländer/innen','Nord- oder Westeuropa','Südeuropa','Übrige Länder') or s.startswith(('Nord','Süd','Übrige L')):
                out.writerow([ws.title,s]+[round(x,3) if isinstance(x,float) else x for x in c[1:7]])
            else: break
