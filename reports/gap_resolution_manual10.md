# Manuelle Nachpruefung der 10 gemergten Gap-Skips

- D005-r005: REMOVED gap leaf, replacement duplicates sibling {"fact": "screening_fee_charged", "op": "eq", "value": true}
- D007-r001: REMOVED gap leaf, replacement duplicates sibling {"fact": "tenancy_start_date", "op": "gte", "value": "2024-07-01"}
- D007-r016: REMOVED gap leaf, replacement duplicates sibling {"fact": "unit_covered_by_rent_ordinance", "op": "in", "value": ["fully_covered", "partially_covered"]}
- D052-r001: REMOVED gap leaf, replacement duplicates sibling {"fact": "state", "op": "eq", "value": "MA"}
- D052-r005: REMOVED gap leaf, replacement duplicates sibling {"fact": "tenancy_duration_years", "op": "gte", "value": 1}
- D065-r002: REMOVED gap leaf, replacement duplicates sibling {"fact": "application_fee_required", "op": "eq", "value": true}
- D065-r010: REMOVED gap leaf, replacement duplicates sibling {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- D065-r015: REMOVED gap leaf, replacement duplicates sibling {"fact": "rental_property_type", "op": "ne", "value": "owner_occupied_1_to_4_units"}
- D041-r011: REPLACED with eviction_is_no_fault, verbatim quote 207ch verified
- D043-r006: REMOVED gap leaf, verbatim offset quote verified; coverage LA+relocation_required, unless-cases in exemptions

Korrigierte Belegzitate:
- D041-r011: Tenant is not at-fault. The owner or immediate family member will move into the rental unit. A resident manager will move into the rental unit. Demolition and permanent removal from the rental market. Government order. Conversion to affordable housing.
- D043-r006: Relocation Offset: A landlord may offset the tenant's accumulated rent against any relocation assistance, unless the relocation assistance is owed because a termination of tenancy is required by a governmental agency order to vacate or comply issued for an unpermitted dwelling.

Die 8 C-Faelle sind Typ-A-Duplikate: Ersatz entspricht exakt einem Geschwister-Leaf, Loeschen ist semantikaequivalent (all(X,X,GAP)->all(X,X)). Regel-eigene quoted_span je verifiziert.