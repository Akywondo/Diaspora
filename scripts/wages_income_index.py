import openpyxl,csv
wb=openpyxl.load_workbook('/home/user/Diaspora/data/wages_income/raw/lohnindex_24745551.xlsx',data_only=True)
ws=wb['2010-2022']
out=csv.writer(open('/home/user/Diaspora/data/wages_income/swiss_wage_and_price_index_2010_2022.csv','w',newline=''))
out.writerow(['year','nominal_wage_index_1939_100_total','nominal_wage_index_men','nominal_wage_index_women','nominal_wage_change_pct_total','nominal_wage_change_pct_men','nominal_wage_change_pct_women','cpi_annual_avg_change_pct','real_wage_index_1939_100_total','real_wage_index_men','real_wage_index_women','real_wage_change_pct_total','real_wage_change_pct_men','real_wage_change_pct_women'])
for r in ws.iter_rows(values_only=True):
    c=[x for x in r if x is not None]
    try: y=int(str(c[0]).strip())
    except: continue
    if 2010<=y<=2022 and len(c)==14: out.writerow(c)
