# Qualitätsprüfung 500 Adressen (echte Daten, kein Mock)

Stand: 2026-10-04 (Re-Lauf nach Engine-Fix, verifiziert).
Export-SHA `1e58deac6eef3b10328413e4402526c74bbe7bbafba6aa62fefea888060e2ad3`, 177 Regeln, 500 Adressen, 24.970 Entscheidungen:
unknown 24.572 (alle mit gezielter Rueckfrage, 0 ohne Frage), not_yet_effective 139, pending 259, applies 0.
Entscheidungen/Adresse min 13 / max 174, 0 Adressen ohne Entscheidungen, 8 unresolved ehrlich unknown.
Alle 70 Tests gruen (2 stale Test-Erwartungen auf kanonischen Fakt `unit_count` korrigiert, Root Cause: Alias-Normalisierung
jetzt am Eintritt von evaluate_condition/evaluate_formula statt nur in evaluate_rule).
Flip-Beweis (Frage-Antwort-Pfad funktioniert): A0003 Newark + unit_type=residential_dwelling + uses_coordinator_service=true
am 2027-07-02 => D069-r001 (NJ FAIR Act, P.L. 2026 c.043) kippt unknown -> applies, mit allen vier Belegfeldern
(citation, quoted_span, source_url, retrieved_at). T3-0-affected ist daher kein Engine-Fehler, sondern fehlende
Objektfakten im CSV (fail-closed per Ziel P8). Aeltere Abschnitte unten sind ueberholt, bleiben als Historie erhalten.

Stand: 2026-10-04. Quelle: `participant-final-no-hour16 3/data/sample_addresses.csv` (500 Zeilen + Kopf).
Pipeline: `navigator/engine.py` + `navigator/geography.py` + `data/geography.json` (U.S. Census) + `data/rules.json` (140 Regeln).
Export: `output/lookups.json` neu erzeugt (as_of 2026-10-01, sha 538259f7...). Keine Mock-Daten, keine erfundenen Geodaten.

## Update 2026-10-04 (nach Datenfix, nur echte Belege)

Regelbestand: 174 Records (162 in_force, 10 not_yet_effective, 3 pending: D045/D046 MA-Bills, D076 San Diego).
13 Jurisdiktionen normalisiert ("City, ST"), D017-r001 ohne Korpustext entfernt, D025-Doppel-IDs bereinigt.
D022-Datum bewusst nicht geändert (kein Korpus-Beleg, siehe audit Abschnitt 8). Hoboken/JC-Algo/MA-Ballot-failed
bleiben echte Lücken (link-only, kein Regeltext im Korpus) und sind dokumentiert statt erfunden.
Neu-Export (sha d1120e29...): 500 Adressen, 24.781 Entscheidungen — unknown 24.383, not_yet_effective 139, pending 259, applies 0.
Null erfundene applies: ohne Objektfakten (Tenancy-Dauer, RSO-Status, Gebaeudedaten) bleibt alles konservativ unknown/pending.
Alle 67 Tests grün. UI: results.html zeigt jetzt quoted_span + retrieved_at je Regel; tote Dateien web/app.js, web/style.css entfernt (Backup /tmp/webbackup).

## 1. Sind A00001 Postleitzahlen?

Nein. A0001–A0500 sind laufende Datensatz-IDs (Spalte `address_id`). Die PLZ steht in der eigenen Spalte `zip`.
Beispiel A0001: ID `A0001`, PLZ `90028`.

## 2. Kennzahlen

| Kennzahl | Wert |
|---|---|
| Adressen gesamt | 500 |
| Geographie matched (Census) | 492 (98,4 %) |
| Geographie unresolved | 8 (1,6 %): A0098, A0128, A0295, A0346, A0352, A0376, A0380, A0384 |
| Regeln geladen | 140 (131 in_force, 8 not_yet_effective, 1 pending) |
| Entscheidungen gesamt | 15.580 |
| davon unknown | 15.523 (99,6 %) |
| davon pending | 57 (0,4 %, nur D076-r001 San Diego) |
| davon applies_* / does_not_apply | 0 / 0 |
| Adressen mit mind. 1 applies | 0 von 500 |
| Adressen komplett unknown | 443 von 500 |
| Adressen mit pending-Anteil | 57 (49 San Diego + 8 unresolved) |
| Entscheidungen pro Adresse | 11 (NJ Hoboken/Rest), 13 (Jersey City), 19 (Boston), 20 (Cambridge), 32 (San Diego), 38 (San Francisco), 47 (Los Angeles), 62 (Berkeley), 137 (unresolved) |
| Unterschiedliche Regeln in Lookups | 137 von 140 |
| Nie evaluiert (temporal beendet) | 3: D041-r005 (Ende 2024-01-31), D042-r001 (Ende 2026-06-30), D080-r002 (Ende 2026-02-28) |

### Nach Kategorie x Ergebnis

| Kategorie | unknown | pending |
|---|---|---|
| rent_increase_limits (41 Regeln) | 5.109 | 0 |
| just_cause_eviction (34) | 2.743 | 0 |
| security_deposits (31) | 2.463 | 0 |
| application_screening_fees (17) | 3.203 | 0 |
| screening_restrictions (13) | 1.614 | 0 |
| algorithmic_rent_setting (4) | 391 | 57 |

### Nach Status x Ergebnis

| Status | unknown | pending |
|---|---|---|
| in_force | 14.834 | 0 |
| not_yet_effective | 689 | 0 |
| pending | 0 | 57 |

### Top fehlende Fakten (Grund für unknown)

is_residential_property (3.072), tenancy_duration_days (1.590), is_vacation_or_recreational_purpose (1.582),
rental_property_type (1.323), is_mobilehome_homeowner (1.280), affordable_housing_restricted / certificate_of_occupancy_within_15_years /
institutional_dormitory / is_exempt_under_1947_12_d / owner_occupied_two_unit / single_family_noncorporate_owner /
subject_to_stricter_local_rent_control / application_screening_fee_charged (je 1.024),
state (1.088, nur unresolved), legal_city (592, nur unresolved).
Lesart: Die Engine ist konservativ-dreiwertig. Adressstamm + Census liefern fast keine objektbezogenen Fakten
(kein occupancy-Datum, keine Tenancy-Dauer, kein RSO-Status), also bleibt alles unknown. Das ist kein Geographie-Fehler,
sondern fehlende Nutzer-/Parzellenfakten. Kein einziges falsches applies.

## 3. Adress-Auffälligkeiten (echte CSV-Befunde)

| Befund | Anzahl | Beispiele |
|---|---|---|
| ZIP passt nicht zum Bundesstaat (NY-PLZ bei NJ-Adressen u.a.) | 27 | A0003 Newark NJ 11219 (Brooklyn), A0008 Jersey City NJ 78746 (Austin TX), A0017 Jersey City NJ 10949 (Nyack NY), A0102 Hoboken NJ 10003 (Manhattan) |
| ZIP leer | 130 | v.a. Cambridge/San Francisco (Datenbank ohne PLZ) |
| Ohne Hausnummer (Straße only) | 6 | A0098 Willowwood St, A0128, A0295 (Parzelle Harvard St Lot 2A-13), A0346, A0376, A0380 |
| Parzellen statt Adressen | 1 | A0295 Harvard St Lot 2A-13, Dorchester MA |
| units leer | 242 | gut die Hälfte ohne Einheitenzahl |
| year_built leer | 212 | insb. Berkeley/Cambridge/NJ-Parzellen |
| Mehrdeutige Treffer | 1 | A0352 40-42 Mt Prospect Ave Newark (mehrere Census-Treffer, keine Gemeinde ableitbar) |
| Census findet trotz vollständiger Adresse nichts | 1 | A0384 21 Guerrero St San Francisco CA (Census: kein Treffer) |
| Postal-City-Verteilung | — | Los Angeles 80, San Francisco 80, Newark 50, Jersey City 50, Cambridge 50, San Diego 49, Hoboken 40, Berkeley 40, Boston 23, Rest Boston-Nachbarschaften |

Wichtig: Die Geographie löst trotz falscher PLZ korrekt auf (Fallback-Query normalisiert Straßenbereiche und lässt die
mitgelieferte PLZ weg; Originaladresse bleibt unverändert). Beispiel A0008 (PLZ 78746 aus Texas) ist korrekt als
Jersey City NJ gematcht. Die PLZ-Fehler stammen aus den Quell-Parzellendatensätzen, nicht aus der Engine.

## 4. Manueller Stichproben-Check (14 Adressen)

Geprüft: Census-Jurisdiktion vs. CSV-Angabe, Regelauswahl (Team-IDs), Ergebnislage. Alle Entscheidungen unknown/pending, keine falschen applies.

| ID | Adresse (CSV) | Census-Jurisdiktion | Regelauswahl korrekt? | Befund |
|---|---|---|---|---|
| A0001 | 6238 De Longpre Ave, Los Angeles CA 90028 | Los Angeles, CA (matched) | Ja: 47 Entscheidungen, CA-State + LA-City-Regeln (D041/D042/D043-Familie) | unknown, korrekt |
| A0002 | 1031-1035 Clinton St, Hoboken NJ 07030 | Hoboken, NJ (matched) | Teilweise: 11 Entscheidungen, nur NJ-State-Regeln. Keine einzige Hoboken-City-Regel, weil data/rules.json null Hoboken-Regeln enthält | Coverage-Lücke |
| A0005 | 1609 Addison St, Berkeley CA 94703 | Berkeley, CA (matched) | Ja: 62 Entscheidungen inkl. D001-r001 Algorithmus-Verbot Berkeley | unknown (Fakten fehlen), Auswahl korrekt |
| A0018 | 1906 Bonita Ave, Berkeley CA 94704 | Berkeley, CA (matched) | Ja: gleiche 62 wie A0005 | konsistent, korrekt |
| A0006 | 69-71 Westland Av, Boston MA 02115 | Boston, MA (matched) | Ja: 19 Entscheidungen, MA-State + Boston-Regeln | unknown, korrekt |
| A0009 | 322-322.5 Western Ave, Cambridge MA (ohne PLZ) | Cambridge, MA (matched, ZIP-lose Fallback-Query) | Ja: 20 Entscheidungen inkl. Cambridge-Regel | unknown, korrekt |
| A0008 | 1065 Summit Ave, Jersey City NJ 78746 (falsche PLZ) | Jersey City, NJ (matched trotz Texas-PLZ) | Ja: 13 Entscheidungen = 11 NJ-State + 2 Jersey-City-Regeln (D036-r001/r002 Rent Control) | unknown, korrekt |
| A0012 | 1064 Summit Ave, Jersey City NJ 07728 (falsche PLZ) | Jersey City, NJ (matched) | Ja: gleiche 13 wie A0008 | konsistent, korrekt |
| A0016 | 3515 Fillmore St, San Francisco CA (ohne PLZ) | San Francisco, CA (matched) | Teilweise: 38 Entscheidungen; D080-r001 enthalten, aber D080-r002 fehlt überall (Jurisdiktion San Francisco ohne , CA plus Ende 2026-02-28) | Datenfehler (siehe 5.) |
| A0019 | 3820 Haines St, San Diego CA 92109 | San Diego, CA (matched) | Ja: 32 Entscheidungen inkl. D076-r001 pending (San-Diego-Algorithmus-Verbot, Entwurf) | pending statt unknown, korrekt |
| A0003 | 876-878 S 14th St, Newark NJ 11219 (Brooklyn-PLZ) | Newark, NJ (matched) | Ja: 11 NJ-State-Regeln | unknown, PLZ-Fehler schadlos |
| A0098 | Willowwood St, Dorchester MA (ohne Nummer) | unresolved (kein Census-Treffer) | Systematisch: 137 Entscheidungen = alle Regeln unknown, inkl. fehlendem state/legal_city | korrekt-konservativ, aber laut |
| A0352 | 40-42 Mt Prospect Ave, Newark NJ | unresolved (mehrdeutig) | 137 Entscheidungen, alle unknown | korrekt, Mehrdeutigkeit wird nicht geraten |
| A0384 | 21 Guerrero St, San Francisco CA | unresolved (kein Census-Treffer trotz vollständiger Adresse) | 137 Entscheidungen, alle unknown | echte Lücke im Census-Match, kein Engine-Fehler |

Zusatzprobe pending-Arithmetik: 57 pending = 49 San-Diego-Adressen (postal) + 8 unresolved (Jurisdiktion unbekannt, D076 daher nicht ausschließbar). Geht exakt auf.

## 5. Top-Fehler und Fix-Vorschläge (nichts davon eingebaut)

1. Hoboken hat null Regeln. Der reale Hoboken-Algorithmus-Ban (Ch. 155, Rat 10.7.2024) fehlt komplett. Alle 40 Hoboken-Adressen bekommen nur NJ-State-Regeln. Vorschlag: Hoboken Ch. 155 als City-Regel (Jersey City, NJ-Vorbild D036) extrahieren, erst dann greift dort die Algo-Kategorie.
2. Jersey-City-Algorithmus-Verbot (Ord. 25-057, 19.5.2025) fehlt. D036 deckt nur Rent Control ab. Vorschlag: Ord. 25-057 (+ Präzisierung 25-076) als zweite Jersey-City-Regel aufnehmen.
3. Kaputte Jurisdiktions-Strings: 12 City-Regeln ohne , Staat (D040 Los Angeles x4, D073 San Diego x4, D080/D083 San Francisco x4) plus 1x California statt CA. Für gematchte Adressen werden sie richtigerweise ausgeschlossen (covered=False), für unresolved laufen sie als unknown mit. Vorschlag: Strings auf City, ST normalisieren und Regressionstest Jurisdiktion gegen Gazetteer einführen.
4. D041-r005 trägt Status not_yet_effective bei effective 2020-03-30 und Ende 2024-01-31. Harmlos (Datumslogik beendet sie korrekt), aber Status-String falsch. Vorschlag: Status auf beendet/in_force-historisch korrigieren oder Statusfeld aus Daten ableiten statt pflegen.
5. 130 leere ZIPs und 27 falsche ZIPs im Sample. Für Census-Match unschädlich (ZIP wird ignoriert), aber jede PLZ-basierte Anzeige wäre falsch. Vorschlag: PLZ nie als Jurisdiktionsbeweis verwenden (bereits so), zusätzlich ZIP-Plausibilitätswarnung in der UI.
6. Unresolved-Adressen zeigen alle 137 Regeln als unknown (state/legal_city missing). Konservativ richtig, aber für Nutzer laut und nicht priorisiert. Vorschlag: Unresolved-Fall in der UI trennen (Jurisdiktion zuerst klären) statt 137 unknown-Zeilen.
7. 99,6 % unknown ist ehrlich, aber ohne gezielte Fragen tarihui nutzlos. Die Engine stellt bereits targeted_questions. Vorschlag: Fragen-Flow (Belegung, RSO-Status, Baujahr/CoO-Datum) in der UI prominent machen, sonst bleibt das Tool eine Jurisdiktionsauskunft.

## 6. Fazit

Jurisdiktion: 492/500 korrekt gematcht, 8 ehrlich unresolved, falsche PLZ werden neutralisiert. Regelauswahl pro Stadt
stimmt (Berkeley 62, LA 47, SF 38, San Diego 32, Cambridge 20, Boston 19, Jersey City 13, NJ-Rest 11).
Ergebnisse: null falsche applies, aber auch null echte Antworten (99,6 % unknown) wegen fehlender Objektfakten.
Größte inhaltliche Lücken: Hoboken- und Jersey-City-Algorithmus-Verbote fehlen im Regelsatz, 12 Jurisdiktions-Strings sind
fehlerhaft formatiert. Echte Belegtexte (Hoboken Ch. 155, JC Ord. 25-057/25-076, Cella-SJC-13864) sind separat unter
corpus/text/ zu sichern (Suchbudget des Beleg-Subagents bereits verbraucht, nur noch browser.open mit Integer-IDs).
