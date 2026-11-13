#!/bin/bash
# downloads Statistique Vaud xlsx for relevant domains (sequential, 0.6s pause)
cd /home/user/Diaspora/data/canton_vd/raw
grep -E 'Dom_(01|03|13|15|17|12|05)/Tableaux/.*xlsx$' allfiles.txt | while read u; do
 f=x/$(echo $u | sed 's#.*statvd/##;s#/#__#g'); [ -s "$f" ] || { curl -sS -L -m 60 -A "Mozilla/5.0" -o "$f" "https://www.vd.ch$u"; sleep 0.6; }
done
echo done > x/DONE
