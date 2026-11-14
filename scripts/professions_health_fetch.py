import json,urllib.request,csv,time,sys
B="https://www.pxweb.bfs.admin.ch/api/v1/de/"
D="/home/user/Diaspora/data/professions_health/"
def meta(t): return json.load(urllib.request.urlopen(B+f"{t}/{t}.px"))
def post(t,q):
    r=urllib.request.Request(B+f"{t}/{t}.px",json.dumps({"query":q,"response":{"format":"json-stat2"}}).encode(),{"Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(r))
def sel(m,code,texts):
    v=[x for x in m["variables"] if x["code"]==code][0]
    return [c for c,t in zip(v["values"],v["valueTexts"]) if t in texts]
def flat(js,out):
    ids=js["id"];dims=[list(js["dimension"][i]["category"]["label"].values()) for i in ids]
    import itertools
    rows=[]
    for k,combo in enumerate(itertools.product(*dims)):
        rows.append(list(combo)+[js["value"][k]])
    with open(out,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["_".join(ids) and [i for i in ids]] and [i.lower().replace(" ","_") for i in ids]+["value"]);w.writerows(rows)
# 103
t="px-x-1404010100_103";m=meta(t)
q=[{"code":"Anzahl Personen","selection":{"filter":"item","values":sel(m,"Anzahl Personen",["Internes Personal per Ende Jahr"])}},
{"code":"Funktion","selection":{"filter":"item","values":sel(m,"Funktion",["Funktion - Total","<< Ärzteschaft","<< Pflegepersonal"])}},
{"code":"Betriebstyp","selection":{"filter":"item","values":sel(m,"Betriebstyp",["Spitäler - Total"])}},
{"code":"Grossregion (<<) / Kanton (-)","selection":{"filter":"item","values":sel(m,"Grossregion (<<) / Kanton (-)",["Schweiz"])}},
{"code":"Geschlecht","selection":{"filter":"item","values":sel(m,"Geschlecht",["Geschlecht - Total"])}},
{"code":"Staatsangehörigkeit (Auswahl)","selection":{"filter":"all","values":["*"]}},
{"code":"Jahr","selection":{"filter":"all","values":["*"]}}]
flat(post(t,q),D+"hospital_staff_by_nationality_group_ch.csv");time.sleep(2)
t="px-x-1404010100_304";m=meta(t)
q=[{"code":"Grossregion (<<) / Kanton (-)","selection":{"filter":"item","values":sel(m,"Grossregion (<<) / Kanton (-)",["Schweiz"])}},
{"code":"Rechtlich-wirtschaftlicher Status","selection":{"filter":"item","values":sel(m,"Rechtlich-wirtschaftlicher Status",["Rechtlich-wirtschaftlicher Status - Total"])}},
{"code":"Ausbildung","selection":{"filter":"item","values":sel(m,"Ausbildung",["Ausbildung - Total","Arzt/Ärztin","Dipl. Pflegefachfrau/Pflegefachmann","Dipl. Pflegefachfrau/Pflegefachmann mit Weiterbildung","Fachfrau/-mann Betreuung FaBe","Fachangestellte Gesundheit (EFZ)"])}},
{"code":"Geschlecht","selection":{"filter":"item","values":sel(m,"Geschlecht",["Geschlecht - Total"])}},
{"code":"Anzahl Personen","selection":{"filter":"item","values":sel(m,"Anzahl Personen",["Anzahl Personen per Ende Jahr"])}},
{"code":"Herkunft des Diploms","selection":{"filter":"all","values":["*"]}},
{"code":"In Ausbildung","selection":{"filter":"item","values":sel(m,"In Ausbildung",["In Ausbildung - Total"])}},
{"code":"Jahr","selection":{"filter":"all","values":["*"]}}]
flat(post(t,q),D+"sociomedical_staff_by_diploma_origin_ch.csv")
