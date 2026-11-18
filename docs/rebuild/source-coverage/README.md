# Shipped navigation, indicators and setup records

An accounts clerk can open a link labelled **Home**, arrive at the **Accounting** workspace, and select **Total Incoming Bills**. That last number comes from submitted purchase invoices, the clerk's default company, the active fiscal year and the source records visible to the query. The links, date rules, aggregation and access checks each come from a different declaration. The [operator workflows and acceptance examples](operator-workflows.md) trace those decisions, including the effect of a language change.

## Source coverage

The [object register](records.tsv) and [supporting data register](supporting-data.tsv) account for **all 703 tracked JSON files beneath the two application packages whose path has no directory named `doctype`**. The November release pins are [ERPNext 16.60.0](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264) and [Frappe 16.60.1](https://github.com/frappe/frappe/tree/199a0385c00e572664a099a57a00be6ce7404eeb).

| Population | ERPNext | Framework | What a reader can verify |
|---|---:|---:|---|
| Named, object-form records | 579 | 109 | Type, original record name, source module when present, package-relative path and Git blob ID. Two Framework DocType objects under `custom/fixtures` are marked as fixtures. |
| Lists and objects without a root record type | 10 | 5 | File shape, top-level entry count, source path and Git blob ID. Examples include 239 UOM definitions, 235 conversion rows, 29 account categories, country data, demo records and a test sidebar. |
| **Total JSON files in scope** | **589** | **114** | Every file is assigned to one of the two registers. |

The application packages contain additional assets and executable code. The [canonical record dictionary](../model/INDEX.md) covers DocType definitions inside the `doctype` folders. The [runtime surface register](../surfaces/README.md) covers report executors, controllers, hooks and test declarations. A report in both indexes is one source record viewed from two perspectives. Site-added records and app ordering enter through the [effective site profile](../configuration/README.md).

| Published projection | ERPNext | Framework | Details retained |
|---|---:|---:|---|
| [ERP workspaces](erpnext-workspace.tsv) and [Framework workspaces](frappe-workspace.tsv) | 858 rows | 95 rows | Ordered links, shortcuts, embedded sidebar rows, chart and number-card bindings, and quick lists across 24 workspaces. |
| [ERP sidebars and dock](erpnext-sidebar.tsv) and [Framework sidebars and dock](frappe-sidebar.tsv) | 324 rows | 181 rows | 26 Sidebar documents and two Docks. Includes grouping, drill-down destinations, URI rows and declared routing options. |
| [Workspace Sidebar exports](erpnext-compatibility.tsv) | 395 rows | 0 | The 14 ERP exports whose source record type is `Workspace Sidebar`. The similarly named `Sidebar` objects have a separate identity. |
| [Dashboard and report-center entries](erpnext-dashboard.tsv) | 78 rows | 0 | Nine dashboards plus the accounting report center, including their referenced charts, cards and reports. |
| [Indicator definitions](indicators.tsv) | 91 | 16 | 57 Number Cards and 50 Dashboard Charts, with source DocTypes or reports, aggregation, dates, static filters and expressions for resolving contextual filters. |
| [Onboarding sequence](onboarding.tsv) | 69 steps | 0 | Nine guides, 39 required and 30 optional step positions. Access roles, action, stable destination and initial field values are recorded for each position. |
| [Settings exposed from business records](settings-map.tsv) | 165 field mappings | 0 | 31 maps connect an affected record to a field on its source settings document. Each mapping resolves to a declared field and includes its label, type, permission level and declared default where present. |

**Navigation lookup.** Each of the 1,931 navigation rows has a one-based position in its source array. The `lookup` column matches the exact target type and name to a shipped record in either package, including canonical DocTypes. A match establishes identity at these pins. There are **1,710 matches**, **216 structural or other rows without a target**, **three URI targets** and **two named targets without a matching definition**. Repeated references to a destination and the same link appearing in distinct source objects retain separate positions.

| Named target without a matching definition | Evidence | Rebuild treatment |
|---|---|---|
| `Item Standard Cost` | The Stock workspace declares a sidebar item of type DocType with this name. [Shipped item](https://github.com/frappe/erpnext/blob/886ab6ae187244e7f1b852393384ab6019d56264/erpnext/stock/workspace/stock/stock.json#L1129-L1143) | Record the unresolved binding. Resolve the effective site's installed metadata before making this destination navigable. |
| `Background Task` | The Framework System sidebar declares this target as a DocType. [Shipped item](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/system/sidebar/system/system.json#L119-L135) | Apply the same resolution rule. Neither source lookup establishes a runtime error or a substitute record. |

**Using the files.** TSV files are UTF-8 with one header row. Composite column values use JSON within a TSV cell. Join an owner to the object register on package, record type and exact record name. For a matched DocType target, use the [record index](../model/record-index.json). For another matched target, use its package, type and name in the object register. Follow the complete source file for fields outside a projection. A declared filter expression is source evidence. A replacement may implement its resolved condition directly in any language.

To check the denominator from either pinned checkout, run the following command there. It prints the eligible paths and their exact Git object IDs. The two TSV registers give one row per path, preserving case and the leading package directory.

```sh
package=$(git ls-tree -d --name-only HEAD -- erpnext frappe)
git ls-tree -r HEAD -- "$package" |
  awk -F '\t' '$2 ~ /\.json$/ && $2 !~ /\/doctype\// {split($1, x, " "); print x[3], $2}'
```
