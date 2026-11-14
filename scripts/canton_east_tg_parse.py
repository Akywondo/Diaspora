import openpyxl,csv,sys
R='/home/user/Diaspora/data/canton_east/'
out=[]
wb=openpyxl.load_workbook(R+'raw/tg_kant_staatsang.xlsx',data_only=True);ws=wb.worksheets[0]
rows=list(ws.iter_rows(values_only=True));yrs=rows[2][1:12]
for r in rows:
    if r[0]=='Rumänien':
        for y,v in zip(yrs,r[1:12]): out.append(['TG',y,'Rumänien','total_foreign_permanent_resident',v,'tg_kant_staatsang.xlsx'])
    if r[0]=='' and r[1]==2015: pass
tot=rows[3][1:12]
for y,v in zip(yrs,tot): out.append(['TG',y,'Total foreign','total_foreign_permanent_resident',v,'tg_kant_staatsang.xlsx'])
wb=openpyxl.load_workbook(R+'raw/tg_kant_staatsang_bew.xlsx',data_only=True)
for ws in wb:
    rows=list(ws.iter_rows(values_only=True));hdr=[str(h).replace('\n',' ') if h else '' for h in rows[2]]
    for r in rows:
        if r[0]=='Rumänien':
            for h,v in zip(hdr[1:5],r[1:5]): out.append(['TG',int(ws.title),'Rumänien','permit:'+h,v,'tg_kant_staatsang_bew.xlsx'])
wb=openpyxl.load_workbook(R+'raw/tg_gmd_staatsang.xlsx',data_only=True)
for ws in wb:
    rows=list(ws.iter_rows(values_only=True));print(ws.title,[c for c in rows[3] if c][:8])
with open(R+'tg_romanians_by_year_permit.csv','w',newline='') as f:
    w=csv.writer(f);w.writerow(['canton','year','nationality','measure','persons','source_file']);w.writerows(out)
print(len(out))
wb=openpyxl.load_workbook(R+'raw/tg_2026q2_nat_bew.xlsx',data_only=True);ws=wb.worksheets[0]
for i,r in enumerate(ws.iter_rows(values_only=True)):
    if 4<=i<8 or i>2455 : print(i,r)
