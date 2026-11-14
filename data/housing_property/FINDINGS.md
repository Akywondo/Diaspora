# FINDINGS - housing and property (Romanians in Switzerland)

## Headline
No official BFS table gives tenure, ownership, rent or living space for nationality = Romania. The finest nationality breakdown is household-level: Swiss / mixed Swiss-foreign / all-foreign household (Strukturerhebung). The closest proxies are "foreign household" and "household with migration background".

## Key facts (all from files opened in this session; CSVs in this folder)
- Home-ownership rate, foreign households (all members foreign), Switzerland 2022: 12.9% (CI +-0.3) vs Swiss households 43.9%, mixed households 26.8%, all households 35.9%. Tenant/cooperative share: foreign 84.8%, Swiss 52.7%. Source https://dam-api.bfs.admin.ch/hub/api/dam/assets/30885334/master
- Foreign-household ownership 2012 -> 2017 -> 2022 (CH): 14.1% -> 13.6% -> 12.9%; Swiss 44.0 -> 45.9 -> 43.9.
- Foreign-household ownership 2022 by Grossregion: Zurich 8.1%, Genferseeregion (VD, GE, VS) 12.6%, Espace Mittelland (BE, SO, FR, NE, JU) 13.1%, Nordwestschweiz (AG, BS, BL) 15.9%, Ostschweiz (SG, TG, GR, SH, AR, AI, GL) 15.7%, Zentralschweiz 11.3%, Ticino 17.7%.
- Average net monthly rent (CHF, tenant/cooperative flats) 2022 by household nationality, CH: all 1412, Swiss 1392, mixed 1613, foreign 1378 (https://dam-api.bfs.admin.ch/hub/api/dam/assets/30885421/master). Zurich region 2022: foreign 1648 vs Swiss 1619; Genferseeregion foreign 1413 vs Swiss 1365; Ostschweiz foreign 1177 vs Swiss 1305. Note: not controlled for flat size/age.
- Average net rent by canton 2024 (CHF/month, all room sizes; https://dam-api.bfs.admin.ch/hub/api/dam/assets/36398431/master): CH 1485; ZH 1768; AG 1494; VD 1465; GE 1573; BE 1319; SG 1343; SO 1281; TG 1373; (Zug CHF 2024 is highest among cantons shown, Jura CHF 999 lowest).
- Home-ownership rate by canton 2023 (%; https://dam-api.bfs.admin.ch/hub/api/dam/assets/33947654/master): CH 35.8; ZH 26.7; BE 38.0; SO 45.7; SG 38.7; AG 45.5; TG 44.6; VD 30.0; GE 18.4. (Other years 2019-2022 in CSV.)
- Living space per person 2024 (m2; migration status of the HOUSEHOLD, not nationality): 1-person households CH 79.62 total / 84.80 without / 69.84 with migration background; households of 2+ persons CH 39.87 total / 46.27 without / 32.64 with / 36.20 mixed. BFS text: without-background households have 1.2x (1-person) and 1.4x (2+) the m2 per capita of migration-background households. Zurich 2024: 1-person 81.28 vs 67.72; 2+ 45.89 vs 32.74.
- Reading for Romanians (inference, flagged as such): Romanians are mostly recent labour migrants (B/L/C permits, see other agents' folders); the foreign-household ownership rate of ~13% is the only official anchor, so ownership by Romanians is very probably at or below this level - NOT measured.

## Legal frame (Lex Koller / BewG)
Official page could not be opened (www.bj.admin.ch, www.fedlex.admin.ch, www.ch.ch blocked). Only a search-engine summary of Federal Office of Justice material is available -> see Unverified leads. Not quoted as verified.

## Not published / not available
- Ownership rate, tenure, rent, rent burden (Mietbelastung), overcrowding, household size/type for nationality = Romania (or any single country): not found in STAT-TAB (catalogue: no housing table with a Romania value) nor in BFS housing/integration tables opened here.
- Mietbelastung and Wohneigentum by migration status: no indicator page of that name in the Integrationsindikatoren list (only Wohnfläche pro Person and Wohnbedingungen-Lärm are housing indicators); not found. Rent-burden by nationality would need Eurostat/SILC microdata (not checked).
- Tenure-by-nationality table stops at 2022 (data from 2023 not found); table gd-d-09.03.02.01-11 "Bewohnertyp nach Nationalität der Haushaltsmitglieder" (asset 31185926) returned 404.
- Household size/type by nationality: not checked/downloaded (budget).
- Actual property holdings / real-estate purchases by Romanian nationals: no official statistic found.

## Unverified leads (search snippet only, verified=no)
- BJ FAQ Lex Koller (https://www.bj.admin.ch/dam/de/sd-web/4c4DJ25jQFCr/faq-lex-koller-d.pdf): EU/EFTA nationals with lawful and actual residence in Switzerland (valid short-stay L, residence B or settled C permit under free movement) are not "persons abroad" and need no authorisation to buy property; main-residence exception concerns third-country nationals only. Also Federal Council proposal of 15 April 2026 to tighten rules (for third-country nationals) - not in force per snippet. Verify on https://www.bj.admin.ch/de/grundstueckerwerb-durch-personen-im-ausland and fedlex SR 211.412.41.
- Atlas page Wohneigentumsquote 2022: https://www.atlas.bfs.admin.ch/maps/13/map/mapIdOnly/27612_de.html (not opened).

## Blocked hosts I would need
www.bj.admin.ch (https://www.bj.admin.ch/de/grundstueckerwerb-durch-personen-im-ausland; FAQ PDF above), www.fedlex.admin.ch (https://www.fedlex.admin.ch/eli/cc/1984/1148_1148_1148/de), www.ch.ch. www.admin.ch gave 403 on a generic path.

## Cross-checks done
- Ownership 2023 CH 35.8% (canton file) vs 35.9% total in the 2022 nationality table vs "knapp 36%" for 2024 on https://statistik.admin.ch/de/themen/bau-wohnungswesen/wohnen: consistent.
- Rent CH 2022 total 1412 (nationality table) vs 2024 canton table 1485: different years, plausible.
