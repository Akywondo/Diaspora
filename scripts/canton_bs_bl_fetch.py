import subprocess,time,sys,os
out='/home/user/Diaspora/data/canton_bs_bl/raw/'
ids=sys.argv[1:]
for i in ids:
    f=out+f'bs_{i}.csv'
    for a in range(5):
        r=subprocess.run(['curl','-sS','-L','-m','120','-A','Mozilla/5.0','-o',f,'-w','%{http_code}',
          f'https://data.bs.ch/api/explore/v2.1/catalog/datasets/{i}/exports/csv?delimiter=%3B&limit=-1'],capture_output=True,text=True)
        if r.stdout.strip()=='200' and os.path.getsize(f)>0: print(i,'ok',os.path.getsize(f)); break
        print(i,'retry',r.stdout,r.stderr[:60]); time.sleep(10)
    time.sleep(2)
