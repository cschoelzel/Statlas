# Determinismus-Protokoll Runde 3 (2026-10-04)

- Export zweimal gelaufen (python3 -m navigator.app export): identische
  Datei-SHAs vor und nach dem Lauf.
- rules.json: 177 Regeln, Zitatpruefung 177 verifiziert, 0 unpruefbar.
- lookups.json: 500 Adressen, Stichtag 2026-10-01.
- changes.json: T1 0/0, T2 0/0, T3 0/0, T4 105/0, T5 0/0 (affected/conflict).
  T1/T2 missing_rule_ids dokumentiert, T5 correctly_empty, T4 pending.
- Manifest-Fingerprint: kanonischer Hash ueber rules+lookups+changes,
  laufstabil (534d3f... vor und nach Re-Export).
- Unit-Tests: 67/67 gruen.
