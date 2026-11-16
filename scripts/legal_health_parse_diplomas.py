import zipfile,re,sys,csv,html
def read(path):
    z=zipfile.ZipFile(path)
    ss=[]
    for si in re.findall(r'<si>(.*?)</si>',z.read('xl/sharedStrings.xml').decode(),re.S):
        ss.append(html.unescape(''.join(re.findall(r'<t[^>]*>(.*?)</t>',si,re.S))))
    sh=z.read('xl/worksheets/sheet1.xml').decode()
    rows={}
    for m in re.finditer(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)',sh,re.S):
        col,r,attr,body=m.groups()
        if not body: continue
        v=re.search(r'<v>(.*?)</v>',body)
        if not v: continue
        v=v.group(1)
        if 't="s"' in attr: v=ss[int(v)]
        rows.setdefault(int(r),{})[col]=v
    return rows
if __name__=='__main__':
    rows=read(sys.argv[1])
    for r in sorted(rows)[:int(sys.argv[2])]: print(r,rows[r])
