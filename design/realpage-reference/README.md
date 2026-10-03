# RealPage / OneSite — UI direction for Rental Housing Law Navigator

Primary visual direction supplied by the user on 2026-10-03. This supersedes Databricks as the intended visual reference. Images are user-supplied references; dates, authenticity and software versions have not been independently verified.

## Reference hierarchy

1. leasing-occupancy.png: primary shell, navigation, page hierarchy and compact operational lists.
2. onesite-dashboard.png: modular operational dashboard and collapsed icon navigation.
3. onesite-affordable.png: supporting reference for compliance-related dashboard organization; image is blurred and partly obscured, so do not infer exact typography or dimensions.
4. portfolio-dashboard.png: supporting reference for KPI hierarchy and table/chart balance. Its horizontal orange navigation differs from the first reference; do not mix the two shells.

## Chosen direction

Use the first screenshot's dark slate top bar and expanded slate left navigation, with the second screenshot's modular white dashboard panels. Keep a single consistent shell. Orange is a small brand accent; blue indicates links, active controls and primary actions. Avoid combining the orange tab navigation of reference 4 with the blue navigation of reference 1.

## Visual specification

Values below are implementation starting points approximated from the supplied images, not official design tokens.

- Top bar: #34474F, approximately 40–48px high; product name left, search and utility actions right.
- Expanded sidebar: #485F69, approximately 184–208px wide; muted white line icons and labels; selected row #30464F; thin separators.
- Main background: #F1F3F4; content panels #FFFFFF; panel headers #F7F8F8.
- Borders: #DFE3E5, 1px; subtle shadows only if needed for panel separation.
- Primary/link blue: #3698D4; restrained orange accent: #D95F16.
- Text: #30383C; secondary text #737B80. Neutral sans-serif using Arial or system font as an initial approximation.
- Body 13–14px; labels 11–12px; panel headings 14–16px; page title 18–20px; KPI value 28–36px.
- Spacing: 4/8/12/16/24px; compact table rows 32–36px; panel gaps 12–16px.
- Panel corners: 0–3px. Standard controls rectangular and compact; pill rounding only for view switches where the reference uses it.
- Charts must represent actual application data; do not add occupancy or revenue graphics merely to match the reference.

## Shell and navigation

Top bar: solution name, Property Management context, global search, activity/notifications and user menu. Preserve the solution's own name; do not imply official RealPage authorship.

Sidebar: Dashboard, Properties, Rules, Changes, Sources. Each row has a simple monochrome icon and a readable label. Sidebar can collapse to icons, with accessible labels/tooltips.

Page header: module icon and title, breadcrumb, selected property/portfolio on the right. Below it: shared property selector, jurisdiction filter and as-of date. Filters persist when moving between module views.

## Dashboard

First row of compact summary panels: properties evaluated, rules found, properties affected by changes, and unresolved applicability. Use real computed values; otherwise show an explicit empty state.

Second row: a wider Action Required table and a Recent Changes list. Third row: Review Queue and Source/Extraction Status. Each panel has a small title, contextual action and light separator. Every KPI drills into the corresponding filtered table.

## Main workflow

1. Choose portfolio or property and as-of date.
2. Review applicability in a dense table: property, jurisdiction, rule category, status, effective date and source.
3. Select a row to inspect the rule, why it applies, source passage and extraction provenance.
4. Open a change to see affected properties and before/after evidence.

Use a contextual side panel for step 3 as a proposed extension, not a feature proven by these screenshots. Preserve the underlying table and filter state when closing it.

## Status and evidence

Never collapse unknown into not applicable. Distinguish applies, does not apply, unknown, pending and not_yet_effective with text labels, optionally reinforced with color. Put source citations and the relevant date close to conclusions. Show empty, loading and error states explicitly. Include the participant guide's legal-advice disclaimer in the relevant review flow.

## Acceptance criteria

A screenshot of the finished app should read as an operational property-management workspace: slate shell, compact navigation, persistent property context, rectangular white panels, blue interaction accents and dense readable data. It must have one consistent navigation scheme, meaningful drilldowns, visible source evidence, and no decorative marketing hero or oversized card layout.

Visual similarity supports the demo story but does not establish an integration. Integration deployment, authentication and data access remain separate implementation work. The repository currently contains the challenge starter pack and no application frontend.
