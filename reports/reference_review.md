# Unabhängige kleine Quellenreferenz

Stand: 3. Oktober 2026. Standard-Abfragedatum: 1. Oktober 2026.

Die Referenz wurde ausschließlich aus Originaltexten des gelieferten Corpus und dem Umsetzungsauftrag §§10–12 erstellt. Engine-Ausgaben, Implementierungsbegründungen und T1–T5 wurden nicht als Labels verwendet. 22 synthetische Fälle prüfen sechs Regelfamilien; Varianten derselben Norm sind keine unabhängigen Extraktionsnachweise. Keine fachlich anwaltliche Prüfung, zweite unabhängige Annotation oder verifizierte echte Objektfakten liegt vor. Die umfassenden Qualitätsgates bleiben offen.

Die Zeichenpositionen und eigenen SHA256 beziehen sich auf den unveränderten UTF-8-Quellentext, nicht auf den ungeklärten Manifesthash. Alle 22 Zitate wurden durch exakte Teilstringprüfung bestätigt.

## Quellenbefunde

- **D039, bestätigt:** Der Text ist eine Motion zur Untersuchung einer möglichen Verbotsregel. Daraus folgt kein geltendes LA-Verbot. Andere Quellen könnten unabhängig Verpflichtungen begründen.
- **D042, bestätigt:** Die 3-%-Angabe ist ausdrücklich auf 1. Juli 2025 bis 30. Juni 2026 begrenzt. Für Oktober 2026 liefert diese Fundstelle keinen aktuellen Prozentsatz. Die separate Utility-Aussage beginnt am 2. Februar 2026.
- **D045–D047, bestätigt:** Die gelieferten Texte zeigen Überweisung an Ways and Means; sie enthalten keinen materiellen vollständigen Billtext und keinen Nachweis der Verabschiedung. „Pending as supplied“ ist der corpusbezogene Status, keine aktuelle Online-Verifikation.
- **D069, Auslegung:** Die Verkündung ist mit 20. Juli 2026 bezeichnet. Der erste Tag des zwölften Folgemonats ist 1. Juli 2027 (August 2026 ist Monat eins). Die Norm ist am Standard-Abfragedatum zukünftig. Relative Datumsberechnung muss neben dem Status getestet werden.
- **D069, bestätigt:** Spreadsheet-Ausnahme verlangt zugleich kein AI und erforderliche menschliche Analyse. Research-Ausnahme verlangt, dass Daten nicht für gegenwärtige oder künftige Mietvertragsbedingungen verwendet werden. Gemischte öffentliche/nichtöffentliche Daten gelten insgesamt als nichtöffentlich.
- **D007, offene Auslegung/Quellenlücke:** Der amtliche Hinweis nennt eine kombinierte Kleinvermieter-Ausnahme (Eigentumsform UND Immobilenzahl UND Gesamtwohnungszahl). Die Summary schreibt „only two“; für die genaue ≤2-Grenze, bestehende Deposits, Service-Member-Ausnahmen und weitere Bedingungen ist Civil Code §1950.5 erforderlich. Der gelieferte D020-Volltext fehlt. Die Referenzfälle bilden nur die gelieferten Aussagen ab und sind kein vollständiger Deposit-Goldstandard.

## Reproduzierbare Befunde und Regressionen

### REF-MOTION

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D039; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "date": "2026-10-01", "algorithmic_pricing": true}`
- Erwartet: `{"source_status": "motion", "ban_from_this_source": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 131–431 in reference_cases.json.
- Dauerhafte Regression: REF-MOTION.

### REF-LA-RATE-2025-06-30

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D042; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "rso_covered": true, "date": "2025-06-30"}`
- Erwartet: `{"three_percent_supported_by_source": false, "current_rate_if_outside": "unknown"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 377–418 in reference_cases.json.
- Dauerhafte Regression: REF-LA-RATE-2025-06-30.

### REF-LA-RATE-2025-07-01

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D042; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "rso_covered": true, "date": "2025-07-01"}`
- Erwartet: `{"three_percent_supported_by_source": true, "current_rate_if_outside": "unknown"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 377–418 in reference_cases.json.
- Dauerhafte Regression: REF-LA-RATE-2025-07-01.

### REF-LA-RATE-2026-06-30

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D042; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "rso_covered": true, "date": "2026-06-30"}`
- Erwartet: `{"three_percent_supported_by_source": true, "current_rate_if_outside": "unknown"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 377–418 in reference_cases.json.
- Dauerhafte Regression: REF-LA-RATE-2026-06-30.

### REF-LA-RATE-2026-07-01

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D042; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "rso_covered": true, "date": "2026-07-01"}`
- Erwartet: `{"three_percent_supported_by_source": false, "current_rate_if_outside": "unknown"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 377–418 in reference_cases.json.
- Dauerhafte Regression: REF-LA-RATE-2026-07-01.

### REF-LA-RATE-2026-10-01

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D042; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "rso_covered": true, "date": "2026-10-01"}`
- Erwartet: `{"three_percent_supported_by_source": false, "current_rate_if_outside": "unknown"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 377–418 in reference_cases.json.
- Dauerhafte Regression: REF-LA-RATE-2026-10-01.

### REF-LA-UTILITY

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D042; Einordnung: confirmed
- Minimale Eingabe: `{"city": "Los Angeles", "rso_covered": true, "date": "2026-02-02", "utilities_supplied": true}`
- Erwartet: `{"additional_utility_percentage_permitted": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 421–531 in reference_cases.json.
- Dauerhafte Regression: REF-LA-UTILITY.

### REF-MA-D045

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D045; Einordnung: confirmed
- Minimale Eingabe: `{"state": "MA", "date": "2026-10-01"}`
- Erwartet: `{"source_status": "pending_as_supplied", "full_bill_text_available": false, "enacted_ban_supported": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 683–773 in reference_cases.json.
- Dauerhafte Regression: REF-MA-D045.

### REF-MA-D046

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D046; Einordnung: confirmed
- Minimale Eingabe: `{"state": "MA", "date": "2026-10-01"}`
- Erwartet: `{"source_status": "pending_as_supplied", "full_bill_text_available": false, "enacted_ban_supported": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 1131–1222 in reference_cases.json.
- Dauerhafte Regression: REF-MA-D046.

### REF-MA-D047

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D047; Einordnung: confirmed
- Minimale Eingabe: `{"state": "MA", "date": "2026-10-01"}`
- Erwartet: `{"source_status": "pending_as_supplied", "full_bill_text_available": false, "enacted_ban_supported": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 1143–1234 in reference_cases.json.
- Dauerhafte Regression: REF-MA-D047.

### REF-FAIR-TIME-2026-10-01

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D069; Einordnung: interpretation
- Minimale Eingabe: `{"state": "NJ", "date": "2026-10-01", "enactment_date": "2026-07-20"}`
- Erwartet: `{"effective_date": "2027-07-01", "operative_status": "future"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 10181–10283 in reference_cases.json.
- Dauerhafte Regression: REF-FAIR-TIME-2026-10-01.

### REF-FAIR-TIME-2027-06-30

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D069; Einordnung: interpretation
- Minimale Eingabe: `{"state": "NJ", "date": "2027-06-30", "enactment_date": "2026-07-20"}`
- Erwartet: `{"effective_date": "2027-07-01", "operative_status": "future"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 10181–10283 in reference_cases.json.
- Dauerhafte Regression: REF-FAIR-TIME-2027-06-30.

### REF-FAIR-TIME-2027-07-01

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D069; Einordnung: interpretation
- Minimale Eingabe: `{"state": "NJ", "date": "2027-07-01", "enactment_date": "2026-07-20"}`
- Erwartet: `{"effective_date": "2027-07-01", "operative_status": "effective"}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 10181–10283 in reference_cases.json.
- Dauerhafte Regression: REF-FAIR-TIME-2027-07-01.

### REF-FAIR-SPREADSHEET

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D069; Einordnung: confirmed
- Minimale Eingabe: `{"state": "NJ", "date": "2027-07-01", "tool": "spreadsheet", "uses_ai": false, "requires_human_analysis": true}`
- Erwartet: `{"algorithmic_device": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 3464–3612 in reference_cases.json.
- Dauerhafte Regression: REF-FAIR-SPREADSHEET.

### REF-FAIR-RESEARCH

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D069; Einordnung: confirmed
- Minimale Eingabe: `{"state": "NJ", "date": "2027-07-01", "use": "research_only", "used_for_current_or_future_lease_terms": false}`
- Erwartet: `{"coordinating_function": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 5082–5439 in reference_cases.json.
- Dauerhafte Regression: REF-FAIR-RESEARCH.

### REF-FAIR-MIXED-DATA

- Schweregrad: critical; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D069; Einordnung: confirmed
- Minimale Eingabe: `{"state": "NJ", "date": "2027-07-01", "data_contains_public": true, "data_contains_nonpublic": true}`
- Erwartet: `{"combined_data_nonpublic": true}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 6637–6772 in reference_cases.json.
- Dauerhafte Regression: REF-FAIR-MIXED-DATA.

### REF-DEPOSIT-QUALIFIES

- Schweregrad: high; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D007; Einordnung: interpretation
- Minimale Eingabe: `{"state": "CA", "date": "2026-10-01", "new_tenancy": true, "properties": 2, "total_units": 4, "ownership": "natural_person"}`
- Erwartet: `{"max_months_from_supplied_summary": 2, "statute_crosscheck_required": true}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 513–826 in reference_cases.json.
- Dauerhafte Regression: REF-DEPOSIT-QUALIFIES.

### REF-DEPOSIT-TOO-MANY-UNITS

- Schweregrad: high; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D007; Einordnung: interpretation
- Minimale Eingabe: `{"state": "CA", "date": "2026-10-01", "new_tenancy": true, "properties": 2, "total_units": 5, "ownership": "natural_person"}`
- Erwartet: `{"max_months_from_supplied_summary": 1, "statute_crosscheck_required": true}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 513–826 in reference_cases.json.
- Dauerhafte Regression: REF-DEPOSIT-TOO-MANY-UNITS.

### REF-DEPOSIT-CORPORATION

- Schweregrad: high; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D007; Einordnung: interpretation
- Minimale Eingabe: `{"state": "CA", "date": "2026-10-01", "new_tenancy": true, "properties": 2, "total_units": 4, "ownership": "corporation"}`
- Erwartet: `{"max_months_from_supplied_summary": 1, "statute_crosscheck_required": true}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 513–826 in reference_cases.json.
- Dauerhafte Regression: REF-DEPOSIT-CORPORATION.

### REF-DEPOSIT-MISSING-OWNERSHIP

- Schweregrad: high; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D007; Einordnung: interpretation
- Minimale Eingabe: `{"state": "CA", "date": "2026-10-01", "new_tenancy": true, "properties": 2, "total_units": 4}`
- Erwartet: `{"max_months_from_supplied_summary": "unknown", "statute_crosscheck_required": true}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 513–826 in reference_cases.json.
- Dauerhafte Regression: REF-DEPOSIT-MISSING-OWNERSHIP.

### REF-DEPOSIT-LAST-MONTH

- Schweregrad: high; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D007; Einordnung: confirmed
- Minimale Eingabe: `{"state": "CA", "date": "2026-10-01", "last_month_rent_prepaid": true}`
- Erwartet: `{"counts_toward_security_deposit": true}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 827–887 in reference_cases.json.
- Dauerhafte Regression: REF-DEPOSIT-LAST-MONTH.

### REF-DEPOSIT-FIRST-MONTH

- Schweregrad: high; Anforderung: §§10–12 independent source/status/time/exception validation
- Quelle: D007; Einordnung: confirmed
- Minimale Eingabe: `{"state": "CA", "date": "2026-10-01", "first_month_rent_prepaid": true}`
- Erwartet: `{"counts_toward_security_deposit": false}`
- Tatsächlich: nicht getestet; Engine-Ausgaben wurden nicht konsultiert.
- Beleg: exakte Originalspanne 888–953 in reference_cases.json.
- Dauerhafte Regression: REF-DEPOSIT-FIRST-MONTH.

## Freigabegrenzen

Die Fälle dürfen Status-, Zeit- und Ausnahmefehler aufdecken. Sie belegen weder 99 % Genauigkeit noch vollständigen Recall. Kein Enginefehler wird allein wegen eines erwarteten Gegenbeispiels als bestätigt bezeichnet; dazu ist ein tatsächlicher Vergleich erforderlich. Deposit-Kleinvermieterfälle erfordern primären Statutenabgleich vor rechtlicher Freigabe. Die eigenen Labels sind vor einem abschließenden Holdout einzufrieren und dürfen bei Optimierung nicht als neuer unabhängiger Testsatz gezählt werden.
