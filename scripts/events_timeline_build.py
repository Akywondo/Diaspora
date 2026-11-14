#!/usr/bin/env python3
"""Build data/events_timeline/events.csv (+ eu2_quotas_by_period.csv) from the hand-curated
list below.

verified == "yes": the fact was read in this session on the official page given in source_url
(saved copies in data/events_timeline/raw/, log raw/_fetch_log.tsv; pages fetched with
scripts/events_timeline_fetch.py, vote results with scripts/events_timeline_votes.py).
verified == "no": general knowledge or search snippet only; such rows deliberately carry no
statistics, only the date, and are listed in FINDINGS.md.

Usage: python3 -I scripts/events_timeline_build.py
"""
import csv

D = "/home/user/Diaspora/data/events_timeline/"
COLS = ["date", "end_date", "date_precision", "title_en", "title_ro", "category",
        "description_en", "expected_effect", "source_url", "source_publisher", "verified"]
CATS = {"free_movement_law", "swiss_vote", "swiss_policy", "romania", "economy", "health",
        "schengen_eu", "bilateral"}
NSB = "https://www.admin.ch/de/nsb?id="
PX = "https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-1703030000_100/px-x-1703030000_100.px"
SEMFZA = "https://www.sem.admin.ch/de/personenfreizuegigkeit-schweiz-eu-efta"
OBS7 = "https://www.seco.admin.ch/dam/de/sd-web/tGPd29GhKkUD/7_Observatoriumsbericht_zum_FZA_SECO_2011_DE.pdf"
OBS11 = "https://www.seco.admin.ch/dam/de/sd-web/URr1ejlshfwB/11_Observatoriumsbericht_zum_FZA_SECO_2015_DE.pdf"
OBS13 = "https://www.seco.admin.ch/dam/de/sd-web/R1P1Z-xJbT0w/13_Observatoriumsbericht_zum_FZA_SECO_2017_DE.pdf"
BFS = "BFS (STAT-TAB px-x-1703030000_100)"
FC = "Swiss Federal Council (admin.ch press release)"
UNV = "unverified - general knowledge, no reachable official page"
EV = []


def E(*a):
    EV.append(a)


# id, date, end_date, precision, title_en, title_ro, category, description_en, expected_effect, url, publisher, verified
E("ro_1989", "1989-12-22", "1989-12-25", "day", "Fall of the communist regime in Romania", "Căderea regimului comunist în România", "romania",
  "Romanian Revolution of December 1989; end of the Ceausescu regime and of the closed-border policy.", "starts post-1989 emigration", "", UNV, "no")
E("eea_1992", "1992-12-06", "", "day", "Swiss voters reject EEA membership", "Elvețienii resping aderarea la SEE", "swiss_vote",
  "Federal decree on the European Economic Area rejected: 49.66% yes, turnout 78.74% (yes majority in 8 of 26 cantons, derived count).", "Switzerland stays outside EEA; bilateral path", PX, BFS, "yes")
E("fza_signed", "1999-06-21", "", "day", "Agreement on the Free Movement of Persons (AFMP) signed", "Semnarea Acordului privind libera circulație a persoanelor (ALCP)", "free_movement_law",
  "The AFMP between Switzerland and the EU was signed on 21 June 1999 (part of Bilaterals I).", "legal basis of free movement", SEMFZA, "SEM", "yes")
E("bil1_vote", "2000-05-21", "", "day", "Swiss vote approves Bilateral Agreements I", "Referendum: aprobarea Acordurilor bilaterale I", "swiss_vote",
  "Sectoral agreements Switzerland-EC (incl. free movement) approved: 67.19% yes, turnout 48.31%.", "enables AFMP", PX, BFS, "yes")
E("eu_visa_2002", "2002-01-01", "", "day", "Schengen states lift visa requirement for Romanian citizens", "Statele Schengen elimină vizele pentru cetățenii români", "schengen_eu",
  "Visa-free short stays for Romanians in the then Schengen area (Switzerland was not yet a Schengen member).", "eases mobility in the EU, not CH", "", UNV, "no")
E("fza_force", "2002-06-01", "", "day", "AFMP enters into force (EU-15/EFTA)", "Intrarea în vigoare a ALCP (UE-15/AELS)", "free_movement_law",
  "The AFMP has been in force since 1 June 2002; each EU enlargement was covered by an additional protocol.", "free movement for old EU states only", SEMFZA, "SEM", "yes")
E("ch_visa_2004", "2004-02-01", "", "month", "Switzerland lifts visa requirement for Romanian citizens (date unverified)", "Elveția elimină obligația de viză pentru cetățenii români (dată neverificată)", "swiss_policy",
  "Lead only: Switzerland is believed to have abolished the short-stay visa requirement for Romanian and Bulgarian nationals in early 2004; no official page found on a reachable host.", "visa-free visits up to 90 days", "", UNV, "no")
E("schengen_vote", "2005-06-05", "", "day", "Swiss vote approves Schengen/Dublin association", "Referendum: asocierea Elveției la Schengen/Dublin", "swiss_vote",
  "Bilateral agreements on association to Schengen and Dublin approved: 54.63% yes, turnout 56.64%.", "prepares Schengen entry 2008", PX, BFS, "yes")
E("eu10_vote", "2005-09-25", "", "day", "Swiss vote extends free movement to the 10 new EU states", "Referendum: extinderea liberei circulații la cele 10 noi state UE", "swiss_vote",
  "Extension of the AFMP to the 2004 accession states and revised accompanying measures approved: 55.98% yes, turnout 54.29%.", "precedent for Protocol II", PX, BFS, "yes")
E("prot1", "2006-04-01", "", "day", "Protocol I (EU-10) enters into force", "Intrarea în vigoare a Protocolului I (UE-10)", "free_movement_law",
  "Protocol I extending the AFMP to the ten 2004 accession states entered into force on 1 April 2006, with transitional restrictions for the EU-8 until 30 April 2011.", "model for later Romania regime", OBS7, "SECO/SEM/BFS/BSV Observatory report", "yes")
E("east_vote", "2006-11-26", "", "day", "Swiss vote approves the Eastern Europe Cooperation Act", "Referendum: Legea cooperării cu statele Europei de Est", "swiss_vote",
  "Federal Act on Cooperation with the States of Eastern Europe approved: 53.42% yes, turnout 44.98%; legal basis of the Swiss enlargement contribution.", "basis for contribution to new EU states", PX, BFS, "yes")
E("ro_eu", "2007-01-01", "", "day", "Romania and Bulgaria join the European Union", "România și Bulgaria aderă la Uniunea Europeană", "romania",
  "EU accession of Romania and Bulgaria; the AFMP did not yet apply to them (Protocol II needed).", "triggers Protocol II negotiations", "", UNV, "no")
E("prot2_signed", "2008-05-27", "", "day", "Protocol II (Bulgaria/Romania) signed in Brussels", "Semnarea Protocolului II (Bulgaria/România) la Bruxelles", "free_movement_law",
  "Protocol extending the AFMP to Bulgaria and Romania signed (date seen in a search snippet of an EJPD/EDA page only).", "prepares extension", "https://www.ejpd.admin.ch/ejpd/de/home/aktuell/news/2008/2008-05-27.html", "EJPD (host not reachable; search snippet)", "no")
E("crisis_2008", "2008-09-15", "2009-12-31", "month", "Global financial crisis and 2009 recession", "Criza financiară globală și recesiunea din 2009", "economy",
  "Global financial crisis (Lehman Brothers collapse, September 2008) followed by recession in Switzerland and a deep recession in Romania in 2009.", "push from Romania; weaker Swiss labour demand", "", UNV, "no")
E("ch_schengen", "2008-12-12", "", "day", "Switzerland becomes an operational Schengen member", "Elveția devine membru operațional Schengen", "schengen_eu",
  "Systematic person checks at land borders with Schengen neighbours ended on 12 December 2008 (airports followed in March 2009).", "Schengen visa rules apply", "", UNV, "no")
E("vote_2009", "2009-02-08", "", "day", "Swiss vote: continuation of free movement and extension to Bulgaria and Romania", "Referendum: continuarea liberei circulații și extinderea la Bulgaria și România", "swiss_vote",
  "Continuation of the AFMP and approval of Protocol II accepted: 59.61% yes, turnout 51.44% (yes majority in 22 of 26 cantons, derived count).", "clears Protocol II", PX, BFS, "yes")
E("prot2_force", "2009-06-01", "2016-05-31", "day", "Protocol II enters into force: transitional regime for Romanians", "Intrarea în vigoare a Protocolului II: regim tranzitoriu pentru români", "free_movement_law",
  "Protocol II in force since 1 June 2009. Transitional restrictions for Bulgarian/Romanian workers: quotas, priority for resident workers, prior control of wage and working conditions. Quotas 1 June 2009-31 May 2010: 362 B and 3620 L permits (EU-2 together).", "opens labour market under quotas", NSB + "61336", FC + "; quotas: 11th Observatory report, table B.3", "yes")
E("ro_austerity", "2010-07-01", "", "month", "Romanian austerity package (public wage cuts, VAT rise)", "Pachetul de austeritate din România (tăieri salariale, majorarea TVA)", "romania",
  "Austerity measures under the EU/IMF programme took effect in mid-2010: public-sector wage cut and VAT increase (figures not verified on a reachable official page).", "push factor, esp. health staff", "", UNV, "no")
E("eu8_full", "2011-05-01", "", "day", "Full free movement for the EU-8 states", "Liberă circulație deplină pentru statele UE-8", "free_movement_law",
  "Since 1 May 2011 nationals of the EU-8 have full free movement on the same terms as EU-17; Romania and Bulgaria remain under the transitional regime.", "comparison group, not Romania", OBS7, "SECO/SEM/BFS/BSV Observatory report", "yes")
E("ext_2011", "2011-06-01", "2014-05-31", "year", "First extension of the restrictions for Bulgaria and Romania", "Prima prelungire a restricțiilor pentru Bulgaria și România", "free_movement_law",
  "Switzerland extended the restrictions for Bulgarian and Romanian workers twice, in 2011 and 2014 (year verified; the 1 June 2011 start of phase 2 follows from the phase structure, the decision date was not verified). Quota 1 June 2011-31 May 2012: 684 B, 6355 L.", "keeps quotas and priority rule", NSB + "61336", FC, "yes")
E("eu_lab_2014", "2014-01-01", "", "day", "End of transitional restrictions for Romanians in all EU member states", "Sfârșitul restricțiilor tranzitorii pentru români în toate statele UE", "romania",
  "From 1 January 2014 Romanian workers had unrestricted access to the labour markets of all EU states (e.g. Germany, UK), while Switzerland kept quotas.", "diverts flows to EU states", "", UNV, "no")
E("mei_vote", "2014-02-09", "", "day", "Swiss vote accepts the initiative 'Against mass immigration'", "Referendum: acceptarea inițiativei «Împotriva imigrației în masă»", "swiss_vote",
  "Popular initiative accepted: 50.33% yes, turnout 56.57%. New Art. 121a requires annual ceilings and quotas; three years for implementation.", "threat of general quotas", PX, BFS + "; Federal Council statement " + NSB + "51948", "yes")
E("minwage_vote", "2014-05-18", "", "day", "Swiss voters reject a national minimum wage", "Referendum: respingerea salariului minim național", "swiss_vote",
  "Minimum wage initiative rejected: 23.73% yes, turnout 56.36%; minimum wages remain a cantonal matter.", "no federal wage floor", PX, BFS, "yes")
E("ext_2014", "2014-05-28", "2016-05-31", "day", "Final extension of the transitional period for Bulgaria and Romania", "Ultima prelungire a perioadei tranzitorii pentru Bulgaria și România", "free_movement_law",
  "Federal Council extends priority for residents, quotas and wage controls from 1 June 2014 to 31 May 2016. End 2013: 15199 Bulgarian and Romanian long-term residents (+18.1% in 2013; 0.8% of the EU/EFTA resident population); B quotas fully used in recent years.", "keeps quotas two more years", NSB + "53154", FC, "yes")
E("ro_pres_2014", "2014-11-02", "2014-11-16", "day", "Romanian presidential election: queues at diaspora polling stations", "Alegerile prezidențiale din România: cozi la secțiile din diaspora", "romania",
  "Two rounds (2 and 16 November 2014); many voters abroad could not vote because of long queues, a politically mobilising episode for the diaspora.", "diaspora political mobilisation", "", UNV, "no")
E("ecopop", "2014-11-30", "", "day", "Swiss voters reject the Ecopop initiative", "Referendum: respingerea inițiativei Ecopop", "swiss_vote",
  "Initiative 'Stop overpopulation' (cap on net immigration) rejected: 25.90% yes, turnout 49.98%.", "no hard immigration cap", PX, BFS, "yes")
E("snb_2015", "2015-01-15", "", "day", "Swiss National Bank removes the EUR/CHF minimum exchange rate", "Banca Națională a Elveției renunță la cursul minim EUR/CHF", "economy",
  "The SNB discontinued the minimum exchange rate against the euro; the franc appreciated sharply (official SNB page not reachable).", "raises CHF wages in EUR/RON terms; slows hiring", "", UNV, "no")
E("full_2016", "2016-06-01", "2017-05-31", "day", "End of the transitional regime: full free movement for Romanians (first time)", "Sfârșitul regimului tranzitoriu: liberă circulație deplină pentru români (prima dată)", "free_movement_law",
  "Transitional period ended 31 May 2016 (ordinance adopted 13 April 2016). End 2015: 18364 Bulgarian and Romanian permanent residents (0.9% of the foreign resident population); 1542 workers admitted for long-term stay in 2015 (-22.1%). Safeguard clause possible until 31 May 2019 if immigration exceeds the 3-year mean by 10%.", "removes quotas, priority rule, wage pre-check", NSB + "61336", FC, "yes")
E("mei_impl", "2016-12-16", "", "day", "Parliament adopts the implementing law for Art. 121a (preference for job-seekers)", "Parlamentul adoptă legea de aplicare a art. 121a (prioritate pentru șomeri)", "swiss_policy",
  "Parliament's decision of 16 December 2016 implements the immigration article in a way compatible with the AFMP (job-seeker preference instead of quotas).", "no general quotas for EU nationals", NSB + "65099", FC, "yes")
E("valve_2017", "2017-06-01", "2018-05-31", "day", "Safeguard clause for Romania and Bulgaria: B permits capped", "Clauza de salvgardare pentru România și Bulgaria: permise B plafonate", "free_movement_law",
  "Federal Council decision of 10 May 2017: for 12 months from 1 June 2017 B permits for EU-2 workers limited to 996 units, released quarterly; conditions for L permits not met (no L quota).", "caps B permits; shifts to L permits", NSB + "66673", FC, "yes")
E("valve_2018", "2018-06-01", "2019-05-31", "day", "Safeguard clause extended for one more year", "Prelungirea clauzei de salvgardare cu încă un an", "free_movement_law",
  "Decision in principle 18 April 2018, ordinance 16 May 2018: B permits for EU-2 workers and self-employed stay limited to 996 units from 1 June 2018; L threshold not reached.", "caps B permits", NSB + "70776", FC, "yes")
E("job_duty", "2018-07-01", "", "day", "Job-vacancy notification duty enters into force", "Intră în vigoare obligația de anunțare a locurilor de muncă vacante", "swiss_policy",
  "Vacancies in occupations with unemployment above 8% must first be notified to the public employment service from 1 July 2018; threshold lowered to 5% on 1 January 2020.", "head start for resident job-seekers", NSB + "70466", FC, "yes")
E("ro_protest", "2018-08-10", "", "day", "Diaspora protest in Bucharest", "Protestul diasporei de la București", "romania",
  "Large anti-government rally organised by Romanians living abroad in Victoriei Square, dispersed by the gendarmerie.", "signals distrust; weakens return intent", "", UNV, "no")
E("ro_ep_2019", "2019-05-26", "", "day", "European elections and justice referendum: queues abroad again", "Alegeri europarlamentare și referendum: din nou cozi în diaspora", "romania",
  "Long queues at polling stations abroad; followed by a reform (three voting days abroad, postal voting) applied at the November 2019 presidential election.", "diaspora political mobilisation", "", UNV, "no")
E("full_2019", "2019-06-01", "", "day", "Unrestricted free movement for Romanians and Bulgarians", "Liberă circulație fără restricții pentru români și bulgari", "free_movement_law",
  "Safeguard clause expired on 31 May 2019 (ordinance amended 15 May 2019); from 1 June 2019 EU-2 nationals have full free movement on the same terms as other EU citizens. Protocol II allowed a transition of at most ten years.", "removes last quotas", NSB + "75029", FC, "yes")
E("job_duty5", "2020-01-01", "", "day", "Job-vacancy notification threshold lowered to 5%", "Pragul obligației de anunțare a locurilor vacante coboară la 5%", "swiss_policy",
  "As announced by the Federal Council in 2018, the unemployment threshold for the notification duty falls from 8% to 5% on 1 January 2020.", "more occupations covered", NSB + "70466", FC, "yes")
E("covid_in", "2020-03-13", "2020-06-14", "day", "COVID-19: Swiss entry restrictions introduced step by step", "COVID-19: restricții de intrare în Elveția introduse treptat", "health",
  "The Federal Council introduced entry restrictions step by step from 13 March 2020; until 15 June entry from most EU/EFTA states was allowed only in exceptional cases (restrictions with Germany and Austria eased on 16 May 2020).", "freezes new arrivals", NSB + "79426", FC, "yes")
E("covid_out", "2020-06-15", "", "day", "COVID-19: full free movement with EU/EFTA restored", "COVID-19: restabilirea liberei circulații cu UE/AELS", "health",
  "Entry restrictions towards all Schengen states lifted on 15 June 2020; full free movement again with all EU/EFTA states and the UK. Romania (non-Schengen) stayed on the risk list for third-country nationals, but persons with free-movement rights could enter.", "re-opens labour migration", NSB + "79426", FC, "yes")
E("limit_vote", "2020-09-27", "", "day", "Swiss voters reject the limitation initiative", "Referendum: respingerea inițiativei de limitare", "swiss_vote",
  "Initiative 'For moderate immigration' (termination of the AFMP) rejected: 38.29% yes, turnout 59.49% (yes majority in 4 of 26 cantons, derived count).", "free movement confirmed", PX, BFS, "yes")
E("fwa_2021", "2021-05-26", "", "day", "Federal Council ends talks on the institutional framework agreement", "Consiliul Federal încheie negocierile privind acordul-cadru instituțional", "bilateral",
  "Switzerland terminated the negotiations with the EU on an institutional agreement; starting point of the later package approach (Bilaterals III).", "uncertainty on bilateral path", "", UNV, "no")
E("frontex_vote", "2022-05-15", "", "day", "Swiss vote approves the Frontex regulation (Schengen)", "Referendum: aprobarea regulamentului Frontex (Schengen)", "swiss_vote",
  "Adoption of the EU Border and Coast Guard regulation approved: 71.48% yes, turnout 39.98%; Schengen association maintained.", "keeps Schengen membership", PX, BFS, "yes")
E("ro_elections_2024", "2024-11-24", "2025-05-18", "day", "Romanian presidential election annulled and re-run", "Alegerile prezidențiale din România: anulare și reluare", "romania",
  "First round 24 November 2024 annulled by the Constitutional Court in December 2024; re-run in May 2025 (4 and 18 May) with a high diaspora turnout.", "diaspora political mobilisation", "", UNV, "no")
E("vote_10m", "2026-06-14", "", "day", "Swiss voters reject the 'No to a 10-million Switzerland' initiative", "Referendum: respingerea inițiativei «Nu unei Elveții de 10 milioane»", "swiss_vote",
  "Sustainability initiative rejected by the people: 45.21% yes, turnout 58.86% (yes majority in 12 of 26 cantons, derived count; BFS table as published at access date).", "no population cap; AFMP not terminated", PX, BFS, "yes")
# EVENTS-UPDATE-BEGIN (rows with an id already used above REPLACE the earlier row)
OBS5 = "https://www.seco.admin.ch/dam/de/sd-web/qP1VM-Cl8W2j/5_Observatoriumsbericht_zum_FZA_SECO_2009_DE.pdf"
SECO_LM = "https://www.seco.admin.ch/dam/de/sd-web/3dmYe3hl-IiX/2026-01_Die_Lage_auf_dem_Arbeitsmarkt_DE.pdf"
SECO_P = "SECO (Die Lage auf dem Arbeitsmarkt, January 2026, table 17)"
EDA_RO = "https://www.eda.admin.ch/en/bilateral-relations-switzerland-romania"
DROP = {"job_duty5", "eu8_full", "eu_visa_2002"}
E("ch_visa_2004", "2004-02-22", "", "day", "Switzerland-Romania visa waiver agreement enters into force", "Intră în vigoare acordul Elveția-România de eliminare a vizelor", "swiss_policy",
  "Agreement of 15 December 2003 between the Swiss Federal Council and the Government of Romania on the mutual abolition of the visa requirement (SR 0.142.116.632.1) entered into force on 22 February 2004.", "visa-free short stays; no right to work", "https://www.sem.admin.ch/de/visumbefreiung-fuer-gewoehnliche-paesse", "SEM", "yes")
E("ro_eu", "2007-01-01", "", "day", "Romania and Bulgaria join the European Union", "România și Bulgaria aderă la Uniunea Europeană", "romania",
  "Romania and Bulgaria (EU-2) joined the EU on 1 January 2007 (date as given in the Observatory report tables); the AFMP did not apply to them until Protocol II.", "triggers Protocol II negotiations", OBS5, "SECO/SEM/BFS/BSV Observatory report (5th, 2009)", "yes")
E("valve_eu8_eu17", "2014-04-30", "2014-05-31", "day", "Safeguard clause for EU-8 and EU-17 expires", "Expiră clauza de salvgardare pentru UE-8 și UE-17", "free_movement_law",
  "Quotas invoked in 2012 (EU-8) and June 2013 (EU-17) lapsed on 30 April and 31 May 2014; full free movement again for 25 EU states, while Romania and Bulgaria stayed under the transitional regime.", "Romanians still restricted while others freed", NSB + "52803", FC, "yes")
E("unemp_2009", "2009-01-01", "2010-12-31", "year", "Swiss registered unemployment peaks after the financial crisis", "Vârf al șomajului înregistrat în Elveția după criza financiară", "economy",
  "Registered unemployment rate (annual average): 2.6% in 2008, 3.7% in 2009, 3.5% in 2010, 2.8% in 2011; monthly peak 4.4% in December 2009.", "weaker labour demand at the start of Protocol II", SECO_LM, SECO_P, "yes")
E("unemp_2016", "2015-01-01", "2016-12-31", "year", "Unemployment rises after the franc shock", "Șomajul crește după șocul francului", "economy",
  "Registered unemployment rate (annual average): 3.0% in 2014, 3.2% in 2015, 3.3% in 2016, 3.1% in 2017, 2.5% in 2018.", "slower hiring 2015-2016", SECO_LM, SECO_P, "yes")
E("unemp_2020", "2020-01-01", "2021-12-31", "year", "COVID-19 unemployment peak, then tight labour market", "Vârful șomajului din pandemie, apoi piață a muncii tensionată", "economy",
  "Registered unemployment rate (annual average): 2.3% in 2019, 3.2% in 2020, 3.0% in 2021, 2.2% in 2022, 2.0% in 2023, 2.4% in 2024, 2.8% in 2025; monthly peak 3.7% in January-February 2021.", "temporary dip, then strong labour demand 2022-2023", SECO_LM, SECO_P, "yes")
E("covid_25mar", "2020-03-25", "", "day", "COVID-19: entry restrictions extended to all Schengen states", "COVID-19: restricțiile de intrare extinse la toate statele Schengen", "health",
  "On 25 March 2020 the Federal Council was informed that the entry restrictions had been extended to all Schengen states.", "near-complete halt of new entries", NSB + "78563", FC, "yes")
E("contrib1", "2009-01-01", "2019-12-31", "year", "First Swiss enlargement contribution to Romania", "Prima contribuție elvețiană (de extindere) pentru România", "bilateral",
  "Between 2009 and 2019 Switzerland financed projects in Romania with around CHF 180 million under the enlargement contribution (Federal Council wording of 12 December 2022).", "institutional ties; no direct migration effect", NSB + "92168", FC, "yes")
E("contrib1_fa", "2010-09-07", "", "day", "Framework agreement on the enlargement contribution signed with Romania (unverified)", "Semnarea acordului-cadru privind contribuția de extindere cu România (neverificat)", "bilateral",
  "Lead from a search snippet of an EDA page: bilateral framework agreements with Bulgaria and Romania signed in Bern; exact amount for Romania not verified (the EDA country site sits on a blocked host).", "starts project cooperation",
  "https://www.eda.admin.ch/schweizerbeitrag/en/home/the-swiss-contribution/countries/rumaenien/bilaterales-rahmenabkommen-mit-rumaenien.html", "EDA (redirects to a blocked host; search snippet)", "no")
E("contrib2", "2022-12-12", "", "day", "Second Swiss contribution: framework agreement with Romania signed", "A doua contribuție elvețiană: semnarea acordului-cadru cu România", "bilateral",
  "Signed in Bucharest by President Cassis and Finance Minister Caciu: Switzerland provides CHF 221.5 million for projects in Romania until 2029 (second-largest allocation of the cohesion part).", "institutional ties (vocational training, research)", NSB + "92168", FC + "; EDA " + EDA_RO, "yes")
E("contrib2_impl", "2025-02-20", "", "day", "Second Swiss contribution: five programme agreements signed", "A doua contribuție elvețiană: semnarea a cinci acorduri de program", "bilateral",
  "Five agreements for the implementation programmes of the second contribution were signed on 20 February 2025 (visit of Federal Councillor Cassis to Bucharest).", "project implementation starts", EDA_RO, "EDA", "yes")
E("ro_schengen_air", "2024-03-31", "", "day", "Romania joins Schengen for air and sea borders", "România intră în Schengen cu frontierele aeriene și maritime", "schengen_eu",
  "The EU Council decided unanimously at the end of 2023 to lift person checks at internal air and sea borders with Bulgaria and Romania as of 31 March 2024.", "easier air travel; residence rights unchanged", NSB + "103680", FC, "yes")
E("ro_schengen_land", "2025-01-01", "", "day", "Romania becomes a full Schengen member (land borders)", "România devine membru Schengen deplin (frontiere terestre)", "schengen_eu",
  "Internal land border controls with Romania and Bulgaria lifted as of 1 January 2025; the Federal Council approved the corresponding exchange of notes on 20 December 2024 (no direct effect for Switzerland).", "easier overland travel home",
  "https://ec.europa.eu/commission/presscorner/api/files/document/print/en/statement_24_6401/STATEMENT_24_6401_EN.pdf", "European Commission; Federal Council " + NSB + "103680", "yes")
E("bil3_concl", "2024-12-20", "", "day", "Switzerland-EU negotiations on the new package concluded in substance (unverified date)", "Încheierea de fond a negocierilor Elveția-UE pentru noul pachet (dată neverificată)", "bilateral",
  "Lead: material conclusion of the negotiations on the package (Bilaterals III), followed by initialling and a public consultation in 2025; exact dates not verified on a reachable page.", "prepares updated AFMP with safeguard clause", "", UNV, "no")
E("bil3_sign", "2026-03-02", "", "day", "Switzerland-EU package (Bilaterals III) signed in Brussels", "Semnarea pachetului Elveția-UE (Bilaterale III) la Bruxelles", "bilateral",
  "President Guy Parmelin and Commission President Ursula von der Leyen signed the agreements of the Switzerland-EU package on 2 March 2026.", "updated free-movement rules pending ratification", "https://www.admin.ch/de/newnsb/afSUBKNIaRs3s1tqaCebd", FC, "yes")
E("bil3_msg", "2026-03-13", "", "day", "Federal Council sends the Bilaterals III dispatch to Parliament (new safeguard clause)", "Consiliul Federal trimite Parlamentului mesajul privind Bilateralele III (nouă clauză de salvgardare)", "bilateral",
  "Dispatch adopted 13 March 2026 (36 federal acts amended): free movement stays labour-market oriented and a new safeguard clause lets Switzerland act on its own if EU immigration causes serious problems. Optional referendum proposed (confirmed 12 August 2026); package under parliamentary debate at access date, not in force.", "possible future limits on EU immigration",
  "https://www.admin.ch/de/newnsb/HWvQ3sxWQ8hU-xZ4yDnSf", FC + "; https://www.admin.ch/de/paket-schweiz-eu", "yes")
E("vote_10m", "2026-06-14", "", "day", "Swiss voters reject the 'No to a 10-million Switzerland' initiative", "Referendum: respingerea inițiativei «Nu unei Elveții de 10 milioane»", "swiss_vote",
  "Sustainability initiative rejected by the people: 45.21% yes, turnout 58.86% (yes majority in 12 of 26 cantons, derived count; BFS table last updated 2026-08-21).", "no population cap; AFMP not terminated", PX, BFS, "yes")
for _i, _d, _p, _c, _ro in (("mw_ne", "2017-08-01", "month", "Neuchâtel", "Neuchâtel"), ("mw_ju", "2018-02-01", "month", "Jura", "Jura"),
                            ("mw_ge", "2020-11-01", "day", "Geneva", "Geneva"), ("mw_ti", "2021-01-01", "year", "Ticino", "Ticino"),
                            ("mw_bs", "2022-07-01", "day", "Basel-Stadt", "Basel-Stadt")):
    E(_i, _d, "", _p, "Cantonal minimum wage introduced in %s (unverified)" % _c, "Introducerea salariului minim cantonal în %s (neverificat)" % _ro, "economy",
      "One of the five cantons (NE, JU, GE, TI, BS) with a statutory cantonal minimum wage; date and hourly amount not verified on a reachable official page.", "wage floor in low-pay sectors", "", UNV, "no")
E("ro_health_wages", "2018-03-01", "", "month", "Romania raises public health-sector wages", "România majorează salariile din sănătatea publică", "romania",
  "Pay rise for doctors and nurses in public hospitals, meant to slow the emigration of health workers that followed EU accession and the 2010 wage cuts (not verified on a reachable official page).", "reduces push for health staff", "", UNV, "no")
# EVENTS-UPDATE-END

QUOTAS = [  # period_start, period_end, permit, quota_units(11th report), final exhaustion %, printed value in 'Kontingente' row of 13th report
    ("2009-06-01", "2010-05-31", "B", 362, 100, 362), ("2010-06-01", "2011-05-31", "B", 523, 100, 523),
    ("2011-06-01", "2012-05-31", "B", 684, 100, 684), ("2012-06-01", "2013-05-31", "B", 885, 100, 885),
    ("2013-06-01", "2014-05-31", "B", 1046, 82, 1046), ("2014-06-01", "2015-05-31", "B", 1126, 93, 1056),
    ("2015-06-01", "2016-05-31", "B", "", 76, 922),
    ("2009-06-01", "2010-05-31", "L", 3620, 87, 3620), ("2010-06-01", "2011-05-31", "L", 4987, 100, 4987),
    ("2011-06-01", "2012-05-31", "L", 6355, 95, 6355), ("2012-06-01", "2013-05-31", "L", 7722, 92, 7722),
    ("2013-06-01", "2014-05-31", "L", 9090, 88, 9090), ("2014-06-01", "2015-05-31", "L", 10457, 72, 7505),
    ("2015-06-01", "2016-05-31", "L", "", 62, 7279),
]


def main():
    by_id = {}
    order = []
    for e in EV:
        assert len(e) == len(COLS) + 1, e[:3]
        if e[0] not in by_id:
            order.append(e[0])
        by_id[e[0]] = e
    rows = []
    for i in [x for x in order if x not in DROP]:
        r = dict(zip(COLS, by_id[i][1:]))
        assert r["category"] in CATS, r
        assert r["verified"] in ("yes", "no"), r
        assert len(r["date"]) == 10 and r["date_precision"] in ("day", "month", "year"), r
        rows.append(r)
    rows.sort(key=lambda r: (r["date"], r["title_en"]))
    with open(D + "events.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    with open(D + "eu2_quotas_by_period.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["period_start", "period_end", "regime", "permit_type", "quota_units", "quota_exhaustion_pct",
                    "value_printed_in_quota_row_13th_report", "nationalities", "source_url", "note"])
        for ps, pe, p, q, ex, pr in QUOTAS:
            note = "quota from table B.3 of the 11th Observatory report (2015); exhaustion from 13th report (2017)"
            if q == "":
                note = ("year-7 quota not stated in any reachable source; the 13th report prints %s in the quota row, "
                        "which for 2014/15 equals permits issued, not the quota" % pr)
            w.writerow([ps, pe, "transitional_quota_protocol_II", p, q, ex, pr, "Bulgaria+Romania (EU-2)", OBS11 + " ; " + OBS13, note])
        for ps, pe, u in (("2017-06-01", "2018-05-31", NSB + "66673"), ("2018-06-01", "2019-05-31", NSB + "70776")):
            w.writerow([ps, pe, "safeguard_clause", "B", 996, "", "", "Bulgaria+Romania (EU-2)", u,
                        "B permits for workers/self-employed, released quarterly; no quota for L permits"])
    n = sum(1 for r in rows if r["verified"] == "yes")
    print("events:", len(rows), "| verified yes:", n, "| no:", len(rows) - n)


if __name__ == "__main__":
    main()
