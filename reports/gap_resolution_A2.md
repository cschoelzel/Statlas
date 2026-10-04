# Gap-Resolution Batch A2: D025 (9 Gap-Leaves)

Stand: 2026-10-04. Methode Typ-A wie in reports/gap_resolution_A.md: jeder Gap-Leaf steht als redundante AND-Klausel (logic.coverage.all[1]) neben einem vollstaendigen belegten Geschwister-Block; die Aufloesung entspricht der Loeschung des Platzhalters (AND-neutral, replacement null). Kein Leaf enthaelt eine eigenstaendige Tatsachenbehauptung. Alle Zitate (max 300 Zeichen, laengstes 285) wurden doppelt verifiziert: eigene Normalisierung (lower, nur a-z 0-9) UND scripts/verify_candidate.py D025, jeweils verbatim True. data/rules.json wurde NICHT veraendert. Patch: /tmp/gapfix_A2.json.

## D025-r001 / date (Duplikat-Leaf)

Titel: Security Deposit - Photograph Requirements Beginning April 1, 2025. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null.

Begruendung: Das Leaf date>=2025-04-01 dupliziert die Geschwister-Bedingung im inneren Block (state=CA, date>=2025-04-01); Loeschung AND-neutral. Beleg D025: "Beginning April 1, 2025, the landlord shall take photographs of the unit within a reasonable time after the possession of the unit is returned to the landlord"

## D025-r002 / unresolved_legal_evidence_D025_999

Titel: Service Member Protection - No Small Landlord Exception for Service Members. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von prospective_tenant_is_service_member=true).

Begruendung: Geschwister-Block (state=CA, service-member=true) bildet die Norm ab; Platzhalter redundant. Beleg D025: "Subparagraph (A) shall not apply if the prospective tenant is a service member. A landlord shall not refuse to enter into a rental agreement for residential property with a prospective tenant who is a service member"

## D025-r003 / unresolved_legal_evidence_D025_999

Titel: Prohibition on Deductions for Preexisting Conditions and Ordinary Wear and Tear. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von security_deposit_deduction_claimed=true).

Begruendung: Geschwister-Block (state=CA, deduction-claimed=true) plus belegte Exemptions (preexisted / wear-and-tear) bilden die Norm ab; Platzhalter redundant. Beleg D025: "The landlord shall not assert a claim against the tenant or the security for damages to the premises or any defective conditions that preexisted the tenancy, for ordinary wear and tear or the effects thereof"

## D025-r006 / unresolved_legal_evidence_D025_999

Titel: Prohibition on Excessive Professional Cleaning Charges. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von professional_cleaning_charge_claimed=true).

Begruendung: Geschwister-Block (state=CA, cleaning-charge=true) plus belegte Exemption (reasonably necessary) bilden die Norm ab; Platzhalter redundant. Beleg D025: "The landlord shall not require a tenant to pay for, or assert a claim against the tenant or the security for, professional carpet cleaning or other professional cleaning services, unless reasonably necessary to return the premises to the condition it was in at the inception of tenancy"

## D025-r009 / unresolved_legal_evidence_D025_999

Titel: Itemized Statement Based on Initial Inspection. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von initial_inspection_conducted=true).

Begruendung: Geschwister-Block (state=CA, inspection=true) bildet die Norm ab; Platzhalter redundant. Beleg D025: "Based on the inspection, the landlord shall give the tenant an itemized statement specifying repairs or cleanings that are proposed to be the basis of any deductions from the security"

## D025-r010 / unresolved_legal_evidence_D025_999

Titel: Inception Photographs Requirement. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von tenancy_commencement_date_on_or_after_2025_07_01=true).

Begruendung: Geschwister-Block (state=CA, tenancy ab 1.7.2025) bildet die Norm ab; Platzhalter redundant. Beleg D025: "For tenancies that begin on or after July 1, 2025, the landlord shall take photographs of the unit immediately before, or at the inception of, the tenancy"

## D025-r017 / unresolved_legal_evidence_D025_999

Titel: Post-Vacate Photographs Requirement. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von landlord_makes_deduction_from_security=true).

Begruendung: Geschwister-Block (state=CA, deduction=true) bildet die Norm ab; Platzhalter redundant. Beleg D025: "Beginning April 1, 2025, the landlord shall take photographs of the unit within a reasonable time after the possession of the unit is returned to the landlord"

## D025-r022 / unresolved_legal_evidence_D025_999

Titel: Security Deposit - Photographs with Deduction Claims. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null (entspricht Duplikat von state=CA).

Begruendung: Einziger Geschwister-Leaf ist state=CA; D025 ist California Civil Code CIV Abschnitt 1950.5 (Quelle leginfo.legislature.ca.gov), statewide. Platzhalter redundant. Beleg D025: "(a) This section applies to security for a rental agreement for residential property that is used as the dwelling of the tenant."

## D025-r023 / state (Duplikat-Leaf)

Titel: Security Deposit - Small Claims Court Jurisdiction. Pfad: logic.coverage.all[1]. Entscheidung: RESOLVED, replacement null.

Begruendung: Das Leaf state=CA dupliziert die Geschwister-Bedingung state=CA; Loeschung AND-neutral. CA-Geltung folgt aus D025-Provenienz (California Civil Code CIV 1950.5). Beleg D025: "(a) This section applies to security for a rental agreement for residential property that is used as the dwelling of the tenant."

## Bilanz

9 Gap-Leaves bearbeitet: 9 resolved, 0 open. Kein Gap erforderte einen neuen Fakt; nichts erfunden. data/ unveraendert (read-only eingehalten).
