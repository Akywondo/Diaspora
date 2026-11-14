# Diaspora română în Elveția — date oficiale

Extrase de date și scripturi pentru raportul „Diaspora română în Elveția — raport statistic
complet" (noiembrie 2026). Raportul: <https://claude.ai/artifact/To7kWwKfXWWBLiUWKJgzaK>

Toate cifrele provin din surse oficiale (BFS/OFS, SEM, SECO, cantoane, Eurostat). Nimic nu este
estimat; ce nu este publicat pentru cetățenia română este notat ca atare în `FINDINGS.md`.

## Structură

| Dosar | Conținut |
| --- | --- |
| `data/_catalog/` | catalogul celor 633 de tabele BFS STAT-TAB, cu marcaj pentru cele care conțin România |
| `data/_reference/` | români pe canton, an, tip de populație, permis și sex, 2010–2025 (STATPOP) |
| `data/bfs_core/` | seriile federale: bilanț demografic 1981–2025, vârste, comune, țara nașterii, fluxuri, naturalizări, stare civilă, ajutor social |
| `data/sem_migration/` | registrul ZEMIS al SEM: motive de intrare, fluxuri, stoc pe cantoane, frontalieri, 2008–2026 |
| `data/seco_labour/` | indicatori din rapoartele Observatorului SECO pentru libera circulație |
| `data/events_timeline/` | cronologia evenimentelor, cu sursa oficială și starea verificării; contingente UE-2 |
| `data/eurostat_compare/` | români pe țări europene, câștiguri nete, context România–Elveția |
| `data/wages_income/` | salarii mediane după permis, sex, regiune și ramură (LSE), sărăcie pe grupe |
| `data/housing_property/` | statut de ocupare, chirii și rata de proprietate (aproximări oficiale) |
| `data/professions_health/` | personal spitalicesc după cetățenie (grupe) |
| `data/romania_links/` | dublă cetățenie, limba română la recensământul din 2000 |
| `data/canton_*/` | statisticile proprii ale cantoanelor și comparația cu BFS |
| `scripts/` | scripturile de descărcare și prelucrare |

Fiecare dosar tematic are un `SOURCES.md` (sursa, tabelul, adresa, definiția fiecărui fișier) și,
unde agentul de cercetare a apucat să îl scrie, un `FINDINGS.md` (constatări, ce nu este publicat,
piste neverificate, site-uri inaccesibile). Descărcările brute (`raw/`) nu sunt păstrate în
depozit; adresele lor sunt în `SOURCES.md`.

## Reproducere

```bash
python3 scripts/build_pxweb_catalog.py          # catalogul STAT-TAB
python3 scripts/fetch_reference_canton_year.py  # extrasul de referință pe cantoane
python3 scripts/fetch_bfs_core.py               # toate seriile federale (sau un pas: ... migration)
```

API-ul BFS acceptă cel mult 50 de apeluri la 15 secunde și 100 000 de celule pe apel;
`scripts/pxweb.py` respectă aceste limite.

## Definiții

- **Populația rezidentă permanentă**: permise B și C, permise L de cel puțin 12 luni, funcționari
  internaționali; la 31 decembrie. Rezidenții pe termen scurt și frontalierii sunt numărați separat.
- **Criteriul este cetățenia**: românii naturalizați apar ca elvețieni. Pentru originea după țara
  nașterii, vezi `data/bfs_core/born_in_romania_*`.
- STATPOP (BFS) și ZEMIS (SEM) sunt registre diferite; diferă cu 0,7 % la nivel național în 2025.
