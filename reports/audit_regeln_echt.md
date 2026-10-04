# Regel-Audit: data/rules.json + output/rules.json vs. Starter-Pack (Echt-Befund, keine Mocks)

Stand: 2026-10-04. Geprüft: `data/rules.json` und `output/rules.json` (md5-verschieden, inhaltlich **identisch**: je 140 Records, gleiche IDs, gleiche Felder) gegen `participant-final-no-hour16 3/` (README, `dev/change_tests.json` T1–T5, `schema/rule_record.schema.json`, `corpus/corpus_manifest.csv` 87 Docs, `corpus/text/` 54 Texte, `corpus/links_only.csv` 33 Docs).

Methode: Kategorien/Status/Jurisdiktionen ausgezählt; jedes `quoted_span` normalisiert (klein, nur a-z0-9) als Substring in `corpus/text/<source_doc_id>.txt` gesucht; T1–T5-Regel-IDs gesucht; Manifest-Docs ohne Regeln gelistet. Keine neuen Daten erfunden.

## 1. Was stimmt

- Alle **6 Kategorien** vorhanden: rent_increase_limits 41, just_cause_eviction 34, security_deposits 31, application_screening_fees 17, screening_restrictions 13, algorithmic_rent_setting 4.
- Alle **3 States** vorhanden: CA 31, MA 19, NJ 11 (city-Regeln zusätzlich).
- Pflichtfelder nach Schema (team_rule_id, jurisdiction, level, category, status, title, requirement, citation, source_url, quoted_span): **alle 140 Records vollständig**, keine Doppel-IDs.
- **139 von 140** `quoted_span` sind wörtlich (normalisiert) im angegebenen Korpustext enthalten — keine erfundenen Zitate in diesen 139.
- Module B/C-Hüllen vorhanden: `output/lookups.json` (500 Adressen, as_of + disclaimer), `output/changes.json` (Keys T1–T5).

## 2. Fehlende Gesetze (Coverage Gaps — alle 5 Change-Tests betroffen)

| Test | Erwartete Regel | Befund |
|---|---|---|
| T1 | CA-ALG-01 (AB 325 / SB 763, eff 2026-01-01) | **Halb vorhanden, aber falsch datiert**: `D022-r001` (Quelle D022 = AB-325-Seite, chaptered 10.6.2025) steht auf `status=in_force`, `effective_date=2025-10-06`. Damit meldet T1 am 2025-12-31 fälschlich `applies` statt `not_yet_effective`. Korrektur (2026-01-01) steht **nicht** im Korpustext-Ausschnitt — vor Fix im Volltext verifizieren. SB 763 nirgends referenziert. |
| T2 | HOB-ALG-01 (Hoboken Ch. 155) | **Fehlt komplett.** Kein einziger Hoboken-Record. D032/D033/D034 (Hoboken) sind link-only ohne Text — echte Belegtexte müssen erst beschafft werden (vgl. Auftrag fetch_echte_belege). |
| T2 | JC-ALG-01 (Jersey City Ord. 25-057) | **Fehlt komplett.** Nur 2 JC-Regeln (`D036-r001/r002`, Rent Control Ch. 260). D035 (RealPage-Ban-Bericht) ist link-only ohne Text. |
| T3 | NJ-ALG-01 (FAIR Act, enacted 2026-07-20, effective 2027-07-01) | **Fehlt komplett**, obwohl der echte Gesetzestext vorliegt: `corpus/text/D069.txt` (P.L. 2026 c.43, approved 20.7.2026, §9: Inkrafttreten am 1. Tag des 12. Monats nach Enactment = 1.7.2027). 0 Regeln aus D069 extrahiert. D060 (FAIR-Secondary) link-only. |
| T4 | MA-ALG-P1/P2 (H.5222, S.2983, pending) | **Fehlen komplett**, obwohl echte Texte vorliegen: D045 (H.5222, Referred to House Ways and Means), D046 (S.2983), D047 (Bill-History). 0 Regeln aus D045/D046/D047. `pending`-Status gibt es nur 1× (D076 San Diego). |
| T5 | MA-RENT-P1 (Ballot IP 25-21, failed/struck 2026-06-23) | **Fehlt.** Status `failed` kommt in **0 von 140** Records vor. D059 (WBUR-Meldung) ist link-only. Positiv: keine Boston/Cambridge-Rent-Caps vorhanden (T5-Negativseite ok), aber der verlangte failed-Record fehlt. |

Zusätzlich: **Boston (60 Adressen), Newark (50), Hoboken (40)** haben **0 Regeln** — drei von neun Sample-Städten sind extraktionsseitig leer. Cambridge nur 1 Regel. Newark-Docs D070–D072 link-only.

## 3. Unbelegtes Zitat (1 Fall)

- `D017-r001` → `source_doc_id=D017`, aber D017 ist **link-only** (`california.public.law`, kein `text/D017.txt`). Das `quoted_span` kann gegen keinen Korpustext geprüft werden → **aus lookups entfernen oder echten Text beschaffen**, sonst Mock-Verdacht.

## 4. Jurisdiktions-Formatfehler (Schema: State-Code oder "City, ST")

- `Los Angeles` (4×), `San Francisco` (4×), `San Diego` (4×) ohne ", CA"; `California` (1×) statt `CA`. Betrifft u. a. Modul-B-Matching (postal_city vs. legal city).

## 5. Text-Docs ohne jede Regel (24, Auswahl mit Handlungsbedarf)

D069 (FAIR — T3!), D045/D046/D047 (MA-Bills — T4!), D004, D010–D014, D016, D025, D027, D029, D039, D045–D047, D049, D050, D053, D057, D058, D067, D068, D078, D082. Hinweis: manche sind Bye-Product-Texte ohne Regelgehalt — pro Doc bewusst entscheiden (Regel oder dokumentierte Lücke), nicht pauschal übernehmen.

## 6. Kein Mock-Verdacht bei Zitaten, aber Lücken sind keine Ersetzung wert

139/140 Zitate sind echt belegt. Die 6 fehlenden Regelkomplexe dürfen **nicht** aus Sekundärwissen handcodiert werden (README: Extraktion muss automatisiert aus dem Korpus laufen) — erst echte Texte für D032–D035, D059, D060 beschaffen (Auftrag fetch_echte_belege), dann Pipeline erneut laufen lassen. D069/D045/D046/D047 können sofort (Texte vorhanden) extrahiert werden.

## 7. Fix-Liste (priorisiert)

1. D069 → NJ-ALG-01 (`not_yet_effective`, effective 2027-07-01, conflict_with JC/Hoboken als Flag, nicht als Removal).
2. D045/D046 → MA-ALG-P1/P2 (`pending`, Boston+Cambridge).
3. D022 → effective_date auf 2026-01-01 korrigieren **falls** Volltext das hergibt (T1), sonst als `coverage gap` mit abweichendem Enactment-Datum dokumentieren.
4. Echte Texte für Hoboken Ch. 155, JC Ord. 25-057, D059-Ballot, D060 beschaffen; danach HOB-ALG-01, JC-ALG-01, MA-RENT-P1 (`failed`) extrahieren.
5. `D017-r001` belegen oder streichen.
6. 13 Jurisdiktions-Strings normalisieren (`Los Angeles, CA` etc.).
7. Danach `output/rules.json`, `lookups.json` (500 Adressen, v. a. NJ/MA/Hoboken), `changes.json` T1–T5 neu erzeugen und erneut auditieren.

## 8. Fix-Durchlauf 2026-10-04 (nur Korpus-belegt, keine erfundenen Daten)

Backup: /tmp/rules.backup.20261004.json (175 Records). Ergebnis: 174 Records, valides JSON, keine Doppel-IDs.

1. Jurisdiktion normalisiert (13 Records, je quoted_span normalisiert als Substring im Korpus-Doc verifiziert: Prefix+Suffix je 60 Zeichen):
   - D040 4x 'Los Angeles' -> 'Los Angeles, CA' (Doc: City-of-LA-Seite, "City of Los Angeles" im Text)
   - D042 1x 'California' -> 'CA' (Doc: LA-Seite, Inhalt ist State-Law-Zitat -> State-Code korrekt)
   - D073 4x 'San Diego' -> 'San Diego, CA' (Doc: San Diego Municipal Code Ch. 9)
   - D080 2x + D083 2x 'San Francisco' -> 'San Francisco, CA' (Docs: SF.gov Rent Board)
2. D022 (Cartwright Act, AB 325): Volltext D022.txt gelesen. Enthalten: "Approved by Governor October 06, 2025", "Filed with Secretary of State October 06, 2025", Chapter 338. NICHT enthalten: kein "January", kein "effective", keine Operativklausel. Die Behauptung effective 2026-01-01 (CA-Default fur Non-Urgency-Bills) steht NICHT im Volltext -> NICHT korrigiert (kein Datum erfinden). effective_date bleibt 2025-10-06 (= Chaptered-Datum). LUCKE: operatives Datum unbelegt; Feld als evidence_gap zu markieren bzw. bei Re-Export mit coverage-gap-Flag zu versehen.
3. D017-r001 ENTFERNT: participant-final-no-hour16 3/corpus/text/D017.txt existiert NICHT (Korpus: 54 Docs, D017 fehlt). quoted_span daher gegen keinen Korpustext prufbar. Regel aus data/rules.json gestrichen (Deaktivierung = Entfernung, da Engine alle Records ohne Status-Filter ladt). Betroffene Regel: "California Civil Code Section 1950.6 - Application Screening Fees". Re-Import nur mit echtem D017-Volltext.
4. D047/D059/D032/D033/D034/D035/D060: D047.txt existiert, ist aber reine BillHistory-Landingpage (S.2983, "Referred to Senate Committee on Ways and Means") ohne operativen Regeltext -> KEINE Regel extrahiert/erfunden, LUCKE bleibt dokumentiert (Abschnitt 2, T4). D059/D032/D033/D034/D035/D060 haben KEIN Korpus-Doc (nicht unter den 54 Docs) -> keine Belege, keine Regeln, LUCKE bleibt. Zusatz: kein bestehender Record referenziert D047/D059/D032-D035/D060 (einzige fehlende Doc-Referenz war D017), also keine Orphans zu bereinigen.
5. Doppel-IDs bereinigt (Pflicht: keine Doppel-IDs): D025-r015 war 2x, D025-r999 war 9x vergeben. Alle 11 quoted_spans gegen D025.txt verifiziert (Prefix+Suffix je 60 Zeichen Substring). Erste r015-Belegung behalten, Rest fortlaufend auf freie Nummern: D025-r001, -r002, -r003, -r006, -r009, -r010, -r017, -r022, -r023, -r029 (alphabetisch nach Titel). Keine Inhalte geandert, nur IDs.

Bewusst offengelassen: D022-Datum (s.o.); D047/D059/D032-D035/D060-Regeln (kein operativer Text im Korpus); D017-Re-Import (braucht echten Volltext). Als Nachstes: output/* neu exportieren, Tests laufen lassen.
