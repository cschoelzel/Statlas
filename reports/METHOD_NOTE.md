# Method Note: Rental Housing Law Navigator

**Stand:** 3. Oktober 2026 | **Stichtag:** 1. Oktober 2026 | **Version:** 1.0 (Hacknation 2026)

## 1. Architektur und Entwurfsentscheidungen

Der Rental Housing Law Navigator implementiert eine zustandslose, deterministische Drei-Werte-Logik-Engine für Mietrechtsvorschriften in den USA. Die Architektur trennt strikt zwischen unstrukturierter Vorbereitung (Quellengewinnung, automatisierte LLM-Extraktion) und deterministischer Auswertung zur Laufzeit.

```
[Quellenbestand: 87 Einträge] ──► [Anthropic Extraction] ──► [data/rules.json: 177 Regeln]
                                                                        │
[500 Sample-Adressen] ──► [Census Geocoder API] ──► [data/geography.json] ──► [navigator.engine]
                                                                                     │
                                                                           [output/lookups.json]
                                                                           [output/changes.json]
```

- **Vollständig deterministische Auswertung:** Keine LLM-Aufrufe zur Laufzeit. Die Auswertung einer Adresse dauert < 1 ms.
- **Keine stillschweigenden Annahmen:** Fehlende Fakten führen zu `unknown` und erzeugen gezielte Rückfragen (`targeted_questions`), anstatt Standardwerte anzunehmen.
- **Fail-Closed bei Mehrdeutigkeit:** Mehrdeutige Datums- oder Bedingungsausdrücke fallen auf `unknown` zurück und setzen ein Prüfungs-Flag (`coverage_review`).

## 2. Drei-Werte-Logik und Ausnahmebehandlung

Die Engine implementiert Kleene-Drei-Werte-Logik (`True`, `False`, `None`):
- **AND (`all`):** `False` dominiert `None`. Ein `False` reicht aus, um die Bedingung auszuschließen, selbst wenn andere Zweige unbekannt sind.
- **OR (`any`):** `True` dominiert `None`. Ein `True` reicht aus, um die Bedingung zu erfüllen.
- **NOT (`not`):** Invertiert `True`/`False`; `None` bleibt `None`.
- **Ausnahmen-Hierarchie:** Ausnahmen werden getrennt von Anwendungsbedingungen ausgewertet. Eine zutreffende Ausnahme schließt die Regel aus (`does_not_apply`), während eine unbekannte Ausnahme die Anwendung unsicher macht (`unknown`), nicht positiv bestätigt.

## 3. Geokodierung und Zuständigkeitshierarchie

- **Census Geocoding:** Alle 500 Adressen wurden über die offizielle US Census Geocoder API (Benchmark Public_AR_Current / Vintage Current_Current) aufgelöst. 492 Adressen wurden eindeutig einer Rechtsordnung (Bundesstaat + Gemeinde) zugeordnet; 8 Adressen sind als `unresolved` markiert (6 ohne Hausnummer im Sample, 1 ohne Census-Treffer trotz Hausnummer, 1 mit fehlender PLZ).
- **Fakten-Hierarchie:** Nutzerangaben (`user_reported`) überschreiben niemals amtliche Geokodierungsergebnisse für geschützte Felder (`state`, `legal_city`, `jurisdiction`).
- **Zuständigkeitskandidaten:** Lokale Regeln gelten nur in der jeweiligen Gemeinde (Trennlogik; die Hoboken-/Jersey-City-Verbotsregeln fehlen derzeit im Extrakt, siehe T2). Landesgesetze gelten bundesstaatsweit.

## 4. Änderungsanalyse (Tests T1–T5)

| Test | Rechtsvorschrift | Typ | Betroffene Adressen | Ergebnis |
|---|---|---|---|---|
| **T1** | CA AB 325 / SB 763 (Algorithmenverbot) | `as_of` | 0 (missing_rule_ids: [CA-ALG-01]) | Regel fehlt im Extrakt (kein belastbarer Quelltext); Engine liefert bewusst keine Treffer statt falscher. |
| **T2** | Hoboken vs. Jersey City | `boundary` | 0 (missing: [HOB-ALG-01, JC-ALG-01]) | Lokalregeln fehlen (nur Links ohne Volltext); Trennlogik steht, Newark bleibt unbeeinflusst. |
| **T3** | NJ FAIR Act (zukünftige Wirksamkeit) | `as_of` | 0 affected, 147 unresolved | Inkrafttreten 2027-07-01; am Stichtag korrekt `not_yet_effective`. Danach `unknown` (keine Preissoftware-Fakten in Sample-Daten); 0 `conflict_flag`, weil T2-Regeln fehlen. |
| **T4** | MA S.2983 / H.5222 (anhängige Gesetze) | `pending` | 105 affected + 8 geo-unresolved (= alle 110 MA-Adressen erklärt) | Als hypothetische Auswirkung ausgewertet (`pending`); nicht als geltendes Recht dargestellt. |
| **T5** | MA Rent Ballot Question (gescheitert) | `negative` | 0 | Als `failed` erfasst; keine Rechtswirkung auf MA-Adressen. |

## 5. Audit-Trail, Beweiskette und Transparenz

- Jeder Bescheid (`decision`) enthält: `team_rule_id`, `result`, `citations`, `official_text`, `source_url`, `retrieved_at`.
- Rückfragen enthalten die genaue Gesetzesfundstelle und den Grund der Relevanz.
- Alle Exportdateien sind über SHA-256-Fingerprint im `output/manifest.json` kryptografisch verankert.
- Reproduktion: `python3 -m navigator.extract --combine`, danach `python3 -m navigator.app export`, danach `python3 -m unittest discover -s tests` (67 Tests, ca. 12 s). Eingaben: `data/extraction/D*.json`; Ausgaben: `output/` mit SHA-256 in `output/manifest.json`.
- Reproduktion: `python3 -m navigator.extract --combine`, danach `python3 -m navigator.app export`, danach `python3 -m unittest discover -s tests` (67 Tests, ca. 12 s). Eingaben: `data/extraction/D*.json`; Ausgaben: `output/` mit SHA-256 in `output/manifest.json`. Live-Demo: `python3 -m navigator.app serve`, dann http://127.0.0.1:8765 oeffnen (die Webseiten brauchen den Server, direkter Datei-Export per file bleibt auf Wird geladen stehen).
- Abrufdaten: pro Regel als `retrieved_at` in `data/rules.json`; Korpus-, Geokodierungs- und Bill-Status-Zeitpunkte siehe `data/sources/index.json`.

## 6. Grenzen und Haftungsausschluss

- **Keine Rechtsberatung:** Das System dient der automatisierten Vorab-Analyse.
- **Quellenlücken:** 8 Adressen konnten nicht eindeutig geokodiert werden (6 ohne Hausnummer im Sample, 1 ohne Census-Treffer trotz Hausnummer, 1 mit fehlender PLZ); diese verbleiben im Status `unknown` und werden transparent ausgewiesen.
- **Ausstehende fachliche Prüfung:** Eine abschließende juristische Einzelfallprüfung durch qualifizierte Juristen wird ausdrücklich empfohlen.

*Hinweis: Not legal advice. Source gaps and unresolved interpretations require qualified review.*
