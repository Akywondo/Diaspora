import subprocess,time,os,sys
B="https://statistique.ge.ch/statistique/tel/domaines/01/"
OUT="/home/user/Diaspora/data/canton_ge/raw/"
L={"01_01":["T_01_01_8_05","T_01_01_8_05_1989-2013","T_01_01_8_06","T_01_01_8_06_1989-2013","T_01_01_8_07","T_01_01_8_07_1989-2013","T_01_01_8_04","T_01_01_8_04_1989-2013","T_01_01_8_08","T_01_01_16_08","T_01_01_8_01","T_01_01_12_02"],
"01_02":["T_01_02_1_08","T_01_02_1_08_1989-2013","T_01_02_1_09","T_01_02_1_09_1989-2013","T_01_02_1_10","T_01_02_1_10_1989-2013","T_01_02_1_03","T_01_02_1_04","T_01_02_1_14","T_01_02_7_02","T_01_02_9_02","T_01_02_9_04","T_01_02_1_07","T_01_02_8_01"]}
for d,fs in L.items():
    for f in fs:
        p=OUT+f+".xlsx"
        if os.path.exists(p) and os.path.getsize(p)>1000: continue
        for a in range(3):
            r=subprocess.run(["curl","-sS","-L","-m","90","-A","Mozilla/5.0",B+d+"/"+f+".xlsx","-o",p])
            time.sleep(1.5)
            if r.returncode==0 and os.path.getsize(p)>1000: break
        print(f,r.returncode,os.path.getsize(p) if os.path.exists(p) else None)
