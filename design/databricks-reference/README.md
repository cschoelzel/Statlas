# Databricks UI reference for Rental Housing Law Navigator

Collected 2026-10-03 from official Databricks documentation. Image provenance: sources.json. Screenshots illustrate particular documented versions and are not a pixel-perfect specification of every current workspace.

## References
- sql-editor-5.png: new SQL editor overview.
- sql-editor-6.png: annotated SQL editor tools, tabs, execution toolbar, parameter inputs and results table.
- workspace-3.png: workspace navigation and content hierarchy.
- workspace-5.png: compute view.
- workspace-7.png: jobs view.

## Implementation direction
Use a product workspace, with persistent left navigation, a compact page header, contextual actions, dense tables and contextual detail panels. Use white main surfaces, muted gray separators, restrained rounding, blue interaction states and subdued iconography. Avoid marketing-style hero sections. Treat colors and dimensions below as proposed approximations, not official tokens.

Proposed starting tokens: surface #FFFFFF, subtle surface #F7F9FA, border #DCE3E8, text #1B252D, muted text #607483, action #2272B4. Base text 13–14px; compact controls 32px; table rows 36px; spacing scale 4/8/12/16/24px; left navigation roughly 220px. Verify against selected full-screen reference before implementation.

## Project mapping
Navigation: Overview, Properties, Rules, Changes, Sources.
Properties: filterable address table with jurisdiction, applicability status and as-of date. Selecting a row opens applicable rules and source evidence in a right panel.
Rules: structured extraction results with original source text available next to each result.
Changes: change history and affected properties, with explicit pending and not_yet_effective states.
Sources: source documents and extraction runs, arranged as workspace assets.
Overview: compact operational metrics and recent processing activity.

Keep unknown, pending, and not_yet_effective distinguishable. Show citations and as-of dates close to claims. Include the challenge's legal-advice disclaimer.

## Integration boundary
Visual similarity alone does not create a Databricks integration. Deployment, identity, data access and embedding need a separate technical decision. Do not imply endorsement or an existing integration. The starter repository currently has no frontend; framework selection and implementation remain open.
