# Projects and time · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-30e5ac9e6371da"></a>
### Project Costing.build

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_build`

**Inputs** self.

**Declared result** dict.

**Explicit results** payload.

**Local steps**

- Set payload from mapping(“project” → self.project.name, “currency” → self.currency, “consumption\_voucher\_types” → CONSUMPTION\_VOUCHER\_TYPES, “access” → self.access, …).
- For each section in self.SECTIONS.
  - Attempt the following.
    - Set payload at section from getattr(self, section)().
  - On failure (Exception).
    - Set payload at section from no value.
    - Set payload at “errors” at section from 1.
    - Evaluate Platform.log\_error(title = (“Project Costing: ” + section)).
- Return payload.

**Values supplied outside this operation** selected callable from getattr(self, section).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1242)

<a id="op-e994de97b8b09d"></a>
### Project Costing.summary

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_summary`

**Inputs** self.

**Declared result** dict.

**Explicit results** summary.

**Local steps**

- Set summary from CostingSummary(self.project, self.totals, self.contract).build().
- Set summary at “hours” from sum(self.monthly\_hours.values()).
- Return summary.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L242) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1252)

<a id="op-aed137e427ab0d"></a>
### Project Costing.monthly

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_monthly`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** monthly\_rows(mapping(expand self.monthly\_amounts, “hours” → self.monthly\_hours)).

**Local steps**

- Return monthly\_rows(mapping(expand self.monthly\_amounts, “hours” → self.monthly\_hours)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L237) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1247)

<a id="op-0ad626b598fb48"></a>
### Project Costing.billing

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_billing`

**Inputs** self.

**Declared result** dict.

**Explicit results** ProjectBilling(self.project.name, self.access).build().

**Local steps**

- Return ProjectBilling(self.project.name, self.access).build().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1241)

<a id="op-267e5e58bbf3ef"></a>
### Project Costing.drivers

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_drivers`

**Inputs** self.

**Declared result** dict.

**Explicit results** self.cost\_drivers.build().

**Local steps**

- Return self.cost\_drivers.build().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1245)

<a id="op-c5e2def9030d63"></a>
### Project Costing.rate gaps

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_rate_gaps`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** self.cost\_drivers.rate\_gaps().

**Local steps**

- Return self.cost\_drivers.rate\_gaps().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L240) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1250)

<a id="op-34ab0ab5f4827e"></a>
### Project Costing.reports

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_reports`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** list of mapping(“name” → name, “filters” → mapping(fieldnames.get(name, dashboard.fieldname) → self.project.name)) for name drawn from permitted\_reports(names).

**Local steps**

- Set dashboard from Platform.get\_meta(“Project”).get\_dashboard\_data().
- Set names from tuple(generator of report for group drawn from (dashboard.get(“reports”) or list()), then report drawn from group at “items”).
  - Draw group from (dashboard.get(“reports”) or list()).
  - Draw report from group at “items”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dashboard.get(“reports”) → list().
- Set fieldnames from (dashboard.get(“non\_standard\_fieldnames”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dashboard.get(“non\_standard\_fieldnames”) → mapping().
- Return list of mapping(“name” → name, “filters” → mapping(fieldnames.get(name, dashboard.fieldname) → self.project.name)) for name drawn from permitted\_reports(names).
  - Draw name from permitted\_reports(names).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L241) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1251)

<a id="op-dee7d0d44c5881"></a>
### Project Costing.cost drivers

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_cost_drivers`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** CostDrivers.

**Explicit results** CostDrivers(self.project.name, self.access).

**Local steps**

- Return CostDrivers(self.project.name, self.access).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1244)

<a id="op-313a89523fa8e8"></a>
### Project Costing.monthly amounts

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_monthly_amounts`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, MonthlyAmounts).

**Explicit results** amounts.

**Local steps**

- Set amounts from mapping(“labour” → self.queries.labour\_cost(by\_month = true), “purchases” → self.queries.purchase\_cost(by\_month = true), “materials” → self.queries.material\_cost(by\_month = true)).
- If has\_Workforce().
  - Set amounts at “expenses” from self.queries.expense\_claim\_cost(by\_month = true).
- Set amounts at “billed” from self.queries.billed\_amount(by\_month = true).
- Return amounts.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L238) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1248)

<a id="op-bd233ad6f0b1a1"></a>
### Project Costing.monthly hours

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_monthly_hours`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** MonthlyAmounts.

**Explicit results** self.queries.labour\_hours(by\_month = true).

**Local steps**

- Return self.queries.labour\_hours(by\_month = true).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L239) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1249)

<a id="op-d588719c395fdd"></a>
### Project Costing.totals

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_totals`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of source → sum(months.values()) for tuple(source, months) drawn from self.monthly\_amounts.items().

**Local steps**

- Return mapping of source → sum(months.values()) for tuple(source, months) drawn from self.monthly\_amounts.items().
  - Draw tuple(source, months) from self.monthly\_amounts.items().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1253)

<a id="op-7b9fc90ebec90f"></a>
### Project Costing.contract

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_contract`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** float.

**Explicit results** self.queries.sales\_order\_amount().

**Local steps**

- Return self.queries.sales\_order\_amount().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1243)

<a id="op-76aacc68af07cf"></a>
### Get costing access

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_get_costing_access`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** access.

**Local steps**

- Set access from mapping of key → can\_read(doctype) for tuple(key, doctype) drawn from SOURCE\_DOCTYPES.items().
  - Draw tuple(key, doctype) from SOURCE\_DOCTYPES.items().
- Set access at “labour” from can\_read\_labour\_cost().
- Set access at “materials” from (can\_read(“Stock Entry”) and can\_read(“Stock Ledger Entry”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in can\_read(“Stock Entry”) → can\_read(“Stock Ledger Entry”).
- Set access at “expenses” from (has\_Workforce() and can\_read(“Expense Claim”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in has\_Workforce() → can\_read(“Expense Claim”).
- Set access at “ledger” from can\_read(“GL Entry”).
- Set access at “create” from mapping of doctype → can\_create(doctype) for doctype drawn from NEW\_DOCTYPES.
  - Draw doctype from NEW\_DOCTYPES.
- Return access.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1234)

<a id="op-c986aa9993bffb"></a>
### Has Workforce

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_has_workforce`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** “Workforce” belongs to Platform.get\_installed\_apps().

**Local steps**

- Return “Workforce” belongs to Platform.get\_installed\_apps().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1237)

<a id="op-83555d65260664"></a>
### Permitted reports

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_permitted_reports`

**Inputs** names.

**Declared result** list at str.

**Record and data access** read “Report” via get\_all.

**Explicit results** list() · list of name for name drawn from names where (name belongs to enabled and can\_open\_report(name)).

**Local steps**

- If not names.
  - Return list().
- Set enabled from Platform.get\_all(“Report”, filters = mapping(“name” → list(“in”, names), “disabled” → 0), pluck = “name”).
- Return list of name for name drawn from names where (name belongs to enabled and can\_open\_report(name)).
  - Draw name from names, keep a combination only if ((name belongs to enabled and can\_open\_report(name))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name belongs to enabled → can\_open\_report(name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1240)

<a id="op-2c0337e71867a6"></a>
### Can open report

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_can_open_report`

**Inputs** name.

**Declared result** bool.

**Record and data access** resolve a document from “Report” via get\_cached\_doc.

**Explicit results** (not report.disabled and report.is\_permitted() and bool(Platform.has\_permission(report.ref\_doctype, “report”))).

**Local steps**

- Set report from get\_reference\_report(Platform.get\_cached\_doc(“Report”, name)).
- Return (not report.disabled and report.is\_permitted() and bool(Platform.has\_permission(report.ref\_doctype, “report”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not report.disabled → report.is\_permitted() → bool(Platform.has\_permission(report.ref\_doctype, “report”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Report”, name) · effective access from Platform.has\_permission(report.ref\_doctype, “report”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1223)

<a id="op-b9f32326028269"></a>
### Can read

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_can_read`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1224)

<a id="op-5c7c43d60289b6"></a>
### Can create

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_can_create`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** bool(Platform.has\_permission(doctype, “create”)).

**Local steps**

- Return bool(Platform.has\_permission(doctype, “create”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “create”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1222)

<a id="op-8762f1c554e7ea"></a>
### Can submit

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_can_submit`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** bool(Platform.has\_permission(doctype, “submit”)).

**Local steps**

- Return bool(Platform.has\_permission(doctype, “submit”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “submit”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1226)

<a id="op-b022895575ea3b"></a>
### Can read labour cost

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_can_read_labour_cost`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** Boolean false, Boolean true, a comparison result.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1225)

<a id="op-9c80bd9ab3b8fc"></a>
### Costing Summary.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_init`

**Inputs** self, project, totals, contract.

**Local steps**

- Set self.project from project.
- Set self.billed from flt(totals.get(“billed”)).
- Set self.sources from mapping of source → amount for tuple(source, amount) drawn from totals.items() where source differs from “billed”.
  - Draw tuple(source, amount) from totals.items(), keep a combination only if (source differs from “billed”).
- Set self.cost from sum(self.sources.values()).
- Set self.estimate from flt(project.estimated\_costing).
- Set self.contract from flt(contract).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1230)

<a id="op-d14fc231ce0564"></a>
### Costing Summary.build

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_build`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“status” → self.project.status, “percent\_complete” → flt(self.project.percent\_complete, 1), “sources” → self.sources, “cost” → self.cost, …).

**Local steps**

- Return mapping(“status” → self.project.status, “percent\_complete” → flt(self.project.percent\_complete, 1), “sources” → self.sources, “cost” → self.cost, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.estimate → no value.
  - Value choice on self.estimate — true gives (self.forecast − self.estimate), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.contract → no value.

**Methods declared on this owner** [percent of](operations-005.md#op-c26c62c0180e15), [health](operations-004.md#op-d186d1a2cfb855), [margins](operations-005.md#op-3703d7e8cef4a5), [is internal](operations-005.md#op-3a1e2dd03f01b7).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1227)

<a id="op-c7124d1a11461a"></a>
### Costing Summary.forecast

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_forecast`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** float.

**Explicit results** ((self.cost × 100) ÷ percent\_complete) · self.cost.

**Local steps**

- Set percent\_complete from flt(self.project.percent\_complete).
- If (self.project.status belongs to RUNNING\_STATUSES and 0 &lt; percent\_complete &lt; 100).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project.status belongs to RUNNING\_STATUSES → 0 &lt; percent\_complete &lt; 100.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; percent\_complete &lt; 100.
  - Return ((self.cost × 100) ÷ percent\_complete).
- Return self.cost.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1228)

<a id="op-d186d1a2cfb855"></a>
### Costing Summary.health

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_costingsummary_health`

**Inputs** self.

**Declared result** str.

**Explicit results** “empty” · “none” · “over” · “risk” · “ok”.

**Local steps**

- If (not self.cost and not self.billed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.cost → not self.billed.
  - Return “empty”.
- If not self.estimate.
  - Return “none”.
- If self.cost &gt; self.estimate.
  - Return “over”.
- If self.forecast &gt; ((self.estimate × (100 + FORECAST\_TOLERANCE)) ÷ 100).
  - Return “risk”.
- Return “ok”.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1229)
