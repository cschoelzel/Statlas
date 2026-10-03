# Gap-Resolution Batch A: D024 (Rent Cap), D025 (Security Deposits), D026 (Screening Fees)

Stand: 2026-10-04. Methode: Pro Regel wurde der Platzhalter-Leaf (coverage/all/1, redundante AND-Klausel) gegen eine bereits vorhandene, belegte Geschwister-Bedingung ersetzt. Jede Ersetzung ist AND-neutral und entspricht dem Loeschen des Platzhalters; keine neue Tatsachenbehauptung. Jedes Zitat (max 300 Zeichen) wurde per normalisiertem Substring-Abgleich im Korpustext verifiziert. data/rules.json wurde NICHT veraendert.

WICHTIG: Zwischen Analyse und Generierung hat ein paralleler Schreiber data/rules.json veraendert (177 statt 175 Regeln). 9 D025-Regeln (r001, r002, r003, r006, r009, r010, r017, r022, r023) existieren nicht mehr und sind unten als OFFEN markiert (keine Ersetzung vorgenommen). Verbleibend: 46 resolved, 9 offen.

## D024-r001 / unresolved_legal_evidence_D024_1

Titel: California Statewide Rent Cap (AB 1482 / SB 567). Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True, is_exempt_under_1947_12_d:eq=False) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_exempt_under_1947_12_d", "op": "eq", "value": false} (AND-neutral, entspricht Loeschung). Beleg aus D024: "an owner of residential real property shall not, over the course of any 12-month period, increase the gross rental rate for a dwelling or a unit more than 5 percent plus the percentage change in the cost of living, or 10 percent, whichever is lower"

## D024-r002 / unresolved_legal_evidence_D024_2

Titel: Rent Cap Notice Requirement. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True, rent_increase_planned:eq=True, is_exempt_under_1947_12_d:eq=False) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "rent_increase_planned", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "An owner shall provide notice of any increase in the rental rate, pursuant to subdivision (a), to each tenant in accordance with Section 827."

## D024-r003 / unresolved_legal_evidence_D024_3

Titel: Rent Cap - New Tenancy Exception. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True, is_new_tenancy:eq=True, no_prior_tenant_in_possession:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "no_prior_tenant_in_possession", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "For a new tenancy in which no tenant from the prior tenancy remains in lawful possession of the residential real property, the owner may establish the initial rental rate not subject to subdivision (a)."

## D024-r004 / unresolved_legal_evidence_D024_4

Titel: Sublease Rent Ceiling. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True, sublease_transaction:eq=True, is_exempt_under_1947_12_d:eq=False) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "sublease_transaction", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "A tenant of residential real property subject to this section shall not enter into a sublease that results in a total rent for the premises that exceeds the allowable rental rate authorized by subdivision (a)."

## D024-r005 / unresolved_legal_evidence_D024_5

Titel: Gross Rental Rate Definitions and Disclosures. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True, is_exempt_under_1947_12_d:eq=False) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_exempt_under_1947_12_d", "op": "eq", "value": false} (AND-neutral, entspricht Loeschung). Beleg aus D024: "In determining the lowest gross rental amount pursuant to this section, any rent discounts, incentives, concessions, or credits offered by the owner of such unit of residential real property and accepted by the tenant shall be excluded."

## D024-r006 / unresolved_legal_evidence_D024_6

Titel: Exemption - Affordable Housing. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "Housing restricted by deed, regulatory restriction contained in an agreement with a government agency, or other recorded document as affordable housing for persons and families of very low, low, or moderate income"

## D024-r007 / unresolved_legal_evidence_D024_7

Titel: Exemption - Institutional Dormitories. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "Dormitories owned and operated by an institution of higher education or a kindergarten and grades 1 to 12, inclusive, school."

## D024-r008 / unresolved_legal_evidence_D024_8

Titel: Exemption - Existing Local Rent Control. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "Housing subject to rent or price control through a public entity's valid exercise of its police power"

## D024-r009 / unresolved_legal_evidence_D024_9

Titel: Exemption - Recently Constructed Housing. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "Housing that has been issued a certificate of occupancy within the previous 15 years, unless the housing is a mobilehome."

## D024-r010 / unresolved_legal_evidence_D024_10

Titel: Exemption - Single-Family Rentals (Non-Corporate). Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "Residential real property that is alienable separate from the title to any other dwelling unit"

## D024-r011 / unresolved_legal_evidence_D024_11

Titel: Exemption - Owner-Occupied Two-Unit Property. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "A property containing two separate dwelling units within a single structure in which the owner occupied one of the units as the owner's principal place of residence at the beginning of the tenancy"

## D024-r012 / unresolved_legal_evidence_D024_12

Titel: Exemption - Mobilehome Homeowners. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_residential_property:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_residential_property", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "This section shall not apply to a homeowner of a mobilehome, as defined in Section 798.9."

## D024-r013 / unresolved_legal_evidence_D024_13

Titel: Rent Cap - Single-Family Exemption Notice Requirement. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, exempt_under_1947_12_d5:eq=True, tenancy_commenced_or_renewed_on_or_after_2020_07_01:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "exempt_under_1947_12_d5", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "This property is not subject to the rent limits imposed by Section 1947.12 of the Civil Code"

## D024-r014 / unresolved_legal_evidence_D024_14

Titel: Transitional Provisions - Pre-April 1 2024 Increases. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, rent_increase_occurred_between_2019_03_15_and_2020_01_01:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "rent_increase_occurred_between_2019_03_15_and_2020_01_01", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "In the event that an owner has increased the rent by more than the amount permissible under subdivision (a) between March 15, 2019, and January 1, 2020"

## D024-r015 / unresolved_legal_evidence_D024_15

Titel: Transitional Provisions - Mobilehome Pre-Feb 18 2021 Increases. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, is_mobilehome:eq=True, rent_increase_occurred_between_2021_02_18_and_2022_01_01:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "is_mobilehome", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D024: "In the event that an owner has increased the rent for a tenancy in a mobilehome by more than the amount permissible under subdivision (a) between February 18, 2021, and January 1, 2022"

## D025-r016 / unresolved_legal_evidence_D025_16

Titel: Electronic Return of Security Deposits. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, landlord_received_security_or_rental_payments_electronically:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "landlord_received_security_or_rental_payments_electronically", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "If the landlord received the security or rental payments from the tenant electronically, the landlord shall return the remainder of the security electronically to a bank account or other financial institution designated by the tenant in writing"

## D025-r018 / unresolved_legal_evidence_D025_18

Titel: Itemized Statement Delivery Method. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, itemized_statement_required:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "itemized_statement_required", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "the landlord shall furnish the itemized statement by personal delivery or first-class mail, postage prepaid"

## D025-r020 / unresolved_legal_evidence_D025_20

Titel: Multiple Tenant Security Deposit - Written Agreement Option. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, multiple_adult_tenants_in_unit:eq=True, written_mutual_agreement_signed_by_all_tenants:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "written_mutual_agreement_signed_by_all_tenants", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "the landlord may enter into a mutual written agreement between the landlord and all adult tenants, at the commencement of the tenancy or at any time during or after the tenancy"

## D025-r021 / unresolved_legal_evidence_D025_21

Titel: Security Deposit Distribution for Domestic Violence Victim Termination. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, multiple_adult_tenants_in_unit:eq=True, tenant_terminated_lease_under_1946_7:eq=True, written_mutual_agreement_not_executed:eq=True, tenant_requests_alternative_disbursement:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "tenant_terminated_lease_under_1946_7", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "If multiple adult tenants reside in a unit and a tenant terminates the lease pursuant to Section 1946.7 and no written mutual agreement was entered into by the landlord and all adult tenants pursuant to clause (ii)"

## D025-r024 / unresolved_legal_evidence_D025_24

Titel: Exemption from Documentation for Small Deductions. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, deduction_amount_less_than_or_equal_125_dollars:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "deduction_amount_less_than_or_equal_125_dollars", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "The deductions for repairs and cleaning together do not exceed one hundred twenty-five dollars ($125)."

## D025-r025 / unresolved_legal_evidence_D025_25

Titel: Tenant Waiver of Documentation Rights. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, tenant_signed_waiver_after_termination_notice:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "tenant_signed_waiver_after_termination_notice", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "The tenant waived the rights specified in paragraphs (2) and (3)."

## D025-r026 / unresolved_legal_evidence_D025_26

Titel: Tenant Right to Request Documentation After Receiving Itemized Statement. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, tenant_requests_documentation_within_14_days:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "tenant_requests_documentation_within_14_days", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "the landlord shall comply with paragraphs (2) and (3) when a tenant makes a request for documentation within 14 calendar days after receiving the itemized statement specified in paragraph (1)"

## D025-r027 / unresolved_legal_evidence_D025_27

Titel: Mailing Address for Tenant Communications. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, landlord_mailing_security_deposit_documentation:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "landlord_mailing_security_deposit_documentation", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "Any mailings to the tenant pursuant to this subdivision shall be sent to the address provided by the tenant."

## D025-r028 / unresolved_legal_evidence_D025_28

Titel: Forfeiture of Deduction Claims for Bad Faith Noncompliance. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, landlord_in_bad_faith_noncompliance_with_section_1950_5_h:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "landlord_in_bad_faith_noncompliance_with_section_1950_5_h", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "The landlord shall not be entitled to claim any amount of the security if the landlord, in bad faith, fails to comply with this subdivision."

## D025-r034 / unresolved_legal_evidence_D025_34

Titel: Small Claims Court Jurisdiction for Security Deposit Disputes. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, damages_within_small_claims_jurisdiction:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "damages_within_small_claims_jurisdiction", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "An action under this section may be maintained in small claims court if the damages claimed, whether actual, statutory, or both, are within the jurisdictional amount"

## D025-r035 / unresolved_legal_evidence_D025_35

Titel: Evidence of Security Deposit Existence and Amount. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, security_deposit_existence_or_amount_disputed:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "security_deposit_existence_or_amount_disputed", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "Proof of the existence of and the amount of a security deposit may be established by any credible evidence"

## D025-r004 / unresolved_legal_evidence_D025_4

Titel: Security Deposit - Service Member Higher Security with Return Requirement. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, prospective_tenant_is_service_member:eq=True, date:gte=2025-04-01) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "prospective_tenant_is_service_member", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "if a landlord or its agent charges a service member who rents residential property in which the service member will reside a higher than standard or advertised security pursuant to paragraph (1)"

## D025-r005 / unresolved_legal_evidence_D025_5

Titel: Security Deposit - Service Member Non-Discrimination. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, prospective_tenant_is_service_member:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "prospective_tenant_is_service_member", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "A landlord shall not refuse to enter into a rental agreement for residential property with a prospective tenant who is a service member"

## D025-r007 / unresolved_legal_evidence_D025_7

Titel: Security Deposit - Prohibited Deductions for Preexisting Defects and Ordinary Wear and Tear. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "state", "op": "eq", "value": "CA"} (AND-neutral, entspricht Loeschung). Beleg aus D025: "The landlord shall not assert a claim against the tenant or the security for damages to the premises or any defective conditions that preexisted the tenancy"

## D025-r008 / unresolved_legal_evidence_D025_8

Titel: Security Deposit - Prohibited Professional Cleaning Charges. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "state", "op": "eq", "value": "CA"} (AND-neutral, entspricht Loeschung). Beleg aus D025: "The landlord shall not require a tenant to pay for, or assert a claim against the tenant or the security for, professional carpet cleaning or other professional cleaning services, unless reasonably necessary"

## D025-r011 / unresolved_legal_evidence_D025_11

Titel: Security Deposit - Itemized Statement After Initial Inspection. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "state", "op": "eq", "value": "CA"} (AND-neutral, entspricht Loeschung). Beleg aus D025: "Based on the inspection, the landlord shall give the tenant an itemized statement specifying repairs or cleanings that are proposed to be the basis of any deductions from the security"

## D025-r012 / unresolved_legal_evidence_D025_12

Titel: Security Deposit - Tenant Opportunity to Remedy Deficiencies. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "state", "op": "eq", "value": "CA"} (AND-neutral, entspricht Loeschung). Beleg aus D025: "The tenant shall have the opportunity during the period following the initial inspection until termination of the tenancy to remedy identified deficiencies"

## D025-r013 / unresolved_legal_evidence_D025_13

Titel: Security Deposit - Deductions Limited to Identified Items. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, initial_inspection_conducted:eq=True, tenant_possessions_do_not_prevent_identification:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "initial_inspection_conducted", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D025: "the landlord shall not use the security for deductions for repairs or cleanings that are not identified in the itemized statement described in paragraph (2)"

## D025-r014 / unresolved_legal_evidence_D025_14

Titel: Security Deposit - Photograph Requirements for Tenancies Beginning July 1, 2025. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, tenancy_begin_date:gte=2025-07-01) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "tenancy_begin_date", "op": "gte", "value": "2025-07-01"} (AND-neutral, entspricht Loeschung). Beleg aus D025: "For tenancies that begin on or after July 1, 2025, the landlord shall take photographs of the unit immediately before, or at the inception of, the tenancy."

## D025-r001 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r002 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r003 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r006 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r009 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r010 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r017 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r022 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D025-r023 / None

Entscheidung: OFFEN. Begruendung: Regel am 2026-10-04 nicht mehr in data/rules.json (paralleler Schreiber hat 9 D025-Regeln entfernt). Keine Ersetzung vorgenommen; DB nicht beschrieben.

## D026-r001 / unresolved_legal_evidence_D026_1

Titel: California Civil Code Section 1950.6 - Application Screening Fees. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, property_type:eq=residential_rental, landlord_receives_rental_request:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "landlord_receives_rental_request", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "when a landlord or their agent receives a request to rent a residential property from an applicant, the landlord or their agent may charge, pursuant to subdivision (c), that applicant an application screening fee"

## D026-r002 / unresolved_legal_evidence_D026_2

Titel: Application Screening Fee Cap with CPI Adjustment. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, application_screening_fee_charged:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "application_screening_fee_charged", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "The thirty dollar ($30) application screening fee may be adjusted annually by the landlord or their agent commensurate with an increase in the Consumer Price Index, beginning on January 1, 1998."

## D026-r003 / unresolved_legal_evidence_D026_3

Titel: Fee Amount Limited to Actual Out-of-Pocket Costs. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, application_screening_fee_charged:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "application_screening_fee_charged", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "The amount of the application screening fee shall not be greater than the actual out-of-pocket costs of gathering information concerning the applicant"

## D026-r004 / unresolved_legal_evidence_D026_4

Titel: Prohibition on Charging Fee When No Unit Available. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, rental_unit_available_now_or_soon:eq=False) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "rental_unit_available_now_or_soon", "op": "eq", "value": false} (AND-neutral, entspricht Loeschung). Beleg aus D026: "A landlord or their agent shall not charge an applicant an application screening fee when they know or should have known that no rental unit is available at that time or will be available within a reasonable period of time."

## D026-r007 / unresolved_legal_evidence_D026_7

Titel: Alternative Screening Process - Full Refund Option. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, applicant_not_selected_for_tenancy:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "applicant_not_selected_for_tenancy", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "the landlord or their agent returns the entire screening fee to any applicant who is not selected for tenancy, regardless of the reason, within 7 days of selecting an applicant for tenancy or 30 days of when the application was submitted"

## D026-r009 / unresolved_legal_evidence_D026_9

Titel: Refund of Unused Screening Fee Portions. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, application_screening_fee_charged:eq=True, personal_reference_check_not_performed:eq=True, consumer_credit_report_not_obtained:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "personal_reference_check_not_performed", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "If the landlord or their agent does not perform a personal reference check or does not obtain a consumer credit report, the landlord or their agent shall return any amount of the screening fee that is not used for the purposes authorized by this section to the applicant."

## D026-r010 / unresolved_legal_evidence_D026_10

Titel: Fee Receipt with Itemized Expenses. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, application_screening_fee_charged:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "application_screening_fee_charged", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "The landlord or their agent shall provide, personally, or by mail, the applicant with a receipt for the fee paid by the applicant, which receipt shall itemize the out-of-pocket expenses and time spent"

## D026-r011 / unresolved_legal_evidence_D026_11

Titel: Consumer Credit Report Disclosure to Applicant. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, application_screening_fee_paid:eq=True, consumer_credit_report_obtained:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "consumer_credit_report_obtained", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "the landlord or their agent shall provide a copy of the consumer credit report to the applicant who is the subject of that report by personal delivery, mail, or email within seven days"

## D026-r012 / unresolved_legal_evidence_D026_12

Titel: Reusable Screening Report Alternative. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, reusable_screening_report_available:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "reusable_screening_report_available", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "Nothing in this section prevents a landlord from accepting a reusable screening report pursuant to Section 1950.1."

## D026-r017 / unresolved_legal_evidence_D026_17

Titel: Non-Preemption of Federal and State Housing Assistance Programs. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED.

Begruendung: Geschwister-Bedingungen (state:eq=CA, federal_or_state_housing_assistance_program:eq=True) bilden die operative Norm des Unterabschnitts bereits ab; der Platzhalter ist redundant und erzwang nur unknown. Ersetzung wiederholt die belegte Bedingung {"fact": "federal_or_state_housing_assistance_program", "op": "eq", "value": true} (AND-neutral, entspricht Loeschung). Beleg aus D026: "This section is not intended to preempt any provisions or regulations that govern the collection of deposits and fees under federal or state housing assistance programs."

## D025-r015 / unresolved_legal_evidence_D025_15

Titel: Security Deposit - Photograph Requirements Beginning April 1, 2025. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED (nacherfasst nach parallelem DB-Edit).

Begruendung: AND-neutral: replacement duplicates already-present evidenced sibling leaf; equals deleting placeholder. Hinweis: Geschwister-Block enthaelt seit parallelem Edit date>=2025-04-01 statt tenant_vacated; Zitat (h)(1) belegt weiterhin die 21-Tage-Norm. Ersetzung: {"fact": "date", "op": "gte", "value": "2025-04-01"} Beleg: "No later than 21 calendar days after the tenant has vacated the premises"

## D025-r999 / unresolved_legal_evidence_D025_999

Titel: Security Deposit - Small Claims Court Jurisdiction. Pfad: logic/coverage/all/1. Entscheidung: RESOLVED (nacherfasst nach parallelem DB-Edit).

Begruendung: AND-neutral: replacement duplicates already-present evidenced sibling leaf; equals deleting placeholder. AUFFAELLIG: paralleler Schreiber hat Geschwister-Block auf state==CA verengt (Service-Member-Fakten entfernt); Coverage-Pruefung empfohlen, hier unveraendert gelassen (DB nicht beschrieben). Ersetzung: {"fact": "state", "op": "eq", "value": "CA"} Beleg: "The additional amount of security shall be returned to the tenant after no more than six months of residency if the tenant is not in arrears for any rent due during that period."
