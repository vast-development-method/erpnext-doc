# Organization Chart Advance

Kanak Infosystems describes a Frappe HR organization chart with company filtering, employee search/highlight, hierarchy views, rotation, zoom, centering and full screen. Interactive sharing, embedding and PDF/PNG export are advertised. The cohort lists version 15. The publisher's storefront also shows a version 16 option. That additional version is a storefront claim, without an installation result. [Marketplace listing](https://cloud.frappe.io/marketplace/apps/organizational_chart_knk) · [Publisher's versioned guide](https://www.kanakinfosystems.com/frappe/apps/15.0/organizational_chart_knk)

A public copy's manifest identifies Kanak and the technical name. Its tree service filters employees who have left, accepts a company and its immediate child companies, navigates the reporting-manager link and returns identity, name, image and designation. Its full-chart method starts from the first root returned. The UI exposes directional layouts and image, SVG and PDF export controls. Multiple layout directions and multiple reporting structures are different features. The inspected paths establish layout controls and the reporting-manager relation in this copy. [Chart service](https://github.com/MohamedAbdulsalam96/organisation_chart_kanak/blob/670fb963a241f037ee895ac57a252a178ac3fad6/organizational_chart_knk/organizational_chart/api/org_chart.py) · [Chart controls](https://github.com/MohamedAbdulsalam96/organisation_chart_kanak/blob/670fb963a241f037ee895ac57a252a178ac3fad6/organizational_chart_knk/public/js/hierarchy_chart.js)

## Proposed rebuild contract

Accept company scope, relationship type, optional focus employee, effective snapshot and viewer identity. Return visible node IDs, reporting edges, names and authorized display metadata. Include each eligible root in a forest, monotonically paginate broad levels, and flag a cycle or missing manager rather than recursing indefinitely. Search should focus by employee ID even if two names have the same translated spelling. Carry company scope and permissions into export and any shared view.

Translate tooltips, job titles when approved, department labels and empty-state messages. Preserve personal names and employee identifiers, with explicit optional display-name variants. A right-to-left toolbar and an individually chosen diagram orientation are independent settings. Export with the selected language, fonts and layout while keeping the same visible nodes and edges.

| Proposed acceptance case | Expected result |
|---|---|
| A company has two root managers and two employees with identical displayed names. Search by employee ID and export in Arabic. | Both authorized roots are present, the correct employee is highlighted and the PDF preserves Arabic shaping and the reporting edges. |
| The chart contains a cycle or an employee with a missing manager. | Rendering terminates. A diagnostic identifies the stable record keys to an authorized HR reviewer. Other branches remain navigable. |
| A viewer opens a shared chart after losing access to one company. | Nodes, thumbnails, counts and exports reflect current rights; an old share cannot disclose that company. |

Sharing semantics, cross-company depth, additional hierarchy types and authorization on a particular deployed build require direct evidence. [Named app repository](https://github.com/kanakinfo/organisation_chart_kanak)
