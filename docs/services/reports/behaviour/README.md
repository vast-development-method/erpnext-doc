# Report behaviour and result layouts

This directory covers 288 report declarations in the inspected business, foundation, workforce and optional application sources. Two hotel declarations address the same report in the same module. The directory has 287 entries after reconciling that duplicate, including two saved user-activity layouts used as test fixtures. The French and general ledger declarations share a name but bind different modules. Select the module registered on the site.

| Business area | Report entries | Controls, procedures and column definitions |
|---|---:|---|
| [Accounting](accounting.md) | 57 | [Structured details](accounting.json) |
| [Accounting Exchange](accounting-exchange.md) | 1 | [Structured details](accounting-exchange.json) |
| [Assets](assets.md) | 3 | [Structured details](assets.json) |
| [Clinical Services](clinical-services.md) | 7 | [Structured details](clinical-services.json) |
| [Contacts](contacts.md) | 1 | [Structured details](contacts.json) |
| [Custom](custom.md) | 1 | [Structured details](custom.json) |
| [Customer Relationships](customer-relationships.md) | 9 | [Structured details](customer-relationships.json) |
| [Education](education.md) | 9 | [Structured details](education.json) |
| [Equipment Maintenance](equipment-maintenance.md) | 1 | [Structured details](equipment-maintenance.json) |
| [French Accounting](french-accounting.md) | 6 | [Structured details](french-accounting.json) |
| [German Accounting](german-accounting.md) | 2 | [Structured details](german-accounting.json) |
| [Hospitality](hospitality.md) | 1 | [Structured details](hospitality.json) |
| [Human Resources](human-resources.md) | 17 | [Structured details](human-resources.json) |
| [Indian Accounting](indian-accounting.md) | 19 | [Structured details](indian-accounting.json) |
| [Inventory](inventory.md) | 52 | [Structured details](inventory.json) |
| [Lending](lending.md) | 11 | [Structured details](lending.json) |
| [Manufacturing](manufacturing.md) | 21 | [Structured details](manufacturing.json) |
| [Nonprofit](nonprofit.md) | 1 | [Structured details](nonprofit.json) |
| [Operator Workspaces](operator-workspaces.md) | 1 | [Structured details](operator-workspaces.json) |
| [Payroll](payroll.md) | 8 | [Structured details](payroll.json) |
| [Procurement](procurement.md) | 10 | [Structured details](procurement.json) |
| [Projects](projects.md) | 5 | [Structured details](projects.json) |
| [Public Website](public-website.md) | 1 | [Structured details](public-website.json) |
| [Quality](quality.md) | 1 | [Structured details](quality.json) |
| [Regional](regional.md) | 4 | [Structured details](regional.json) |
| [Sales](sales.md) | 23 | [Structured details](sales.json) |
| [Subcontracting](subcontracting.md) | 3 | [Structured details](subcontracting.json) |
| [Support](support.md) | 4 | [Structured details](support.json) |
| [System Administration](system-administration.md) | 7 | [Structured details](system-administration.json) |
| [Utilities](utilities.md) | 1 | [Structured details](utilities.json) |

## Resolve a report

1. Read the report's reference record, role grants and enabled state. Report access, linked-record visibility and export authorization also affect the result. [Report execution and export](../../reporting-and-exports.md)
2. Read the declared controls. The browser uses configured report controls when its report settings supply a filter array. It falls back to the saved declaration’s filters when the settings omit that array. The structured entries distinguish record-declared controls from statically identified form controls, including known shared filter definitions. A dynamic default or options flag means the value is supplied by a function or site data. Conditional controls, including site-added dimensions, can depend on the actual configuration.
3. For a saved layout, use its field selections, filters and sort keys. For a query, use the [eleven documented row-selection and aggregation rules](query-rules.md). For a script, use its row procedure, declared columns and result builders. The field constructions record their enclosing conditions and iterations. Shared helpers, configured fields and inherited class methods can supply additional columns. Optional reports link their own [ordered procedures and module bindings](procedures/README.md). Where a stable operation identifier is present, the [business operation directory](../../../../schemas/operations/business-reading/README.md) supplies its local procedure.
4. Read the [worked dynamic outputs](dynamic-output.md) for ageing cutoffs, salary components, inventory dimensions and withholding groups. Report dates, stored values and user permissions all affect which rows survive. The examples give expected results for their stated inputs.

Source links identify the declaration or builder that produced each recorded fact. A locator on a class binding can point to its inherited dispatch; the derived class supplies the effective methods. A query declaration can select a field outside its grouping key. The query examples identify this explicitly where it affects the interpretation of a displayed result.

The retained [report directory](../README.md) also describes six report names without a standard declaration in the inspected business, foundation and workforce packages: batch split tree, daily work summary replies, professional tax deductions, provident fund deductions, relational database index suggestions and relational database query statistics. Those entries identify the historical data shape. Offering one on a site requires an actual report registration.
