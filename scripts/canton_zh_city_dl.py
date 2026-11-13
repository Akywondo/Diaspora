import json,csv,time,urllib.parse,sys
sys.path.insert(0,'/home/user/Diaspora/scripts')
from canton_zh_city_fetch import get,pkg,B,OUT
JOBS=[('bev_bestand_nationen_hist_jahr_od3482','NationHistLang'),
('bev_bestand_nationen_geschlecht_hist_jahr_od3485','NationHistLang'),
('bev_bestand_jahr_quartier_nationalitaet_od3361','NationHistLang'),
('bev_bestand_jahr_nationalitaet_aufenthaltsart_geschl_od3371','NationHistLang'),
('bev_geburten_jahr_geschlecht_nationalitaet_od4010','NationHistLang'),
('bev_brw_erwerb-ch-buergerrecht_nat_geschl_ag_od3600','NationBisherHistLang'),
('bev_ehe_nationalitaet_od3305','NationEp1HistLang'),
('bev_ehe_nationalitaet_od3305','NationEp2HistLang'),
('bev_monat_asylwesen_status_nationalitaet_geschlecht_od5236','NationHistLang')]
for name,col in JOBS:
    rid=pkg(name)['resources'][0]['id']; rows=[]; off=0
    while True:
        f=urllib.parse.quote(json.dumps({col:'Rumänien'}))
        j=get(B+'datastore_search?resource_id=%s&limit=5000&offset=%d&filters=%s'%(rid,off,f))['result']
        rows+=j['records']; off+=len(j['records']); time.sleep(1)
        if len(j['records'])<5000: break
    fn=OUT+'city_%s__%s.csv'%(name,col)
    if rows:
        with open(fn,'w',newline='',encoding='utf-8') as fh:
            w=csv.DictWriter(fh,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(name,col,len(rows))
