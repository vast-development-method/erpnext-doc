# Projects and time · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Project

[Record definition](../../../../data/record-types/project.json)

<a id="op-03eb5478f3c6d4"></a>
### Cost Drivers.build

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_build`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“activities” → self.activities at slice no value to DRIVER\_LIMIT when labour, otherwise no value, “employees” → self.labour\_by(timesheet.employee, Max(timesheet.employee\_name), DRIVER\_LIMIT) when l ….

**Local steps**

- Set timesheet from qb.DocType(“Timesheet”).
- Set labour from self.access at “timesheets”.
- Return mapping(“activities” → self.activities at slice no value to DRIVER\_LIMIT when labour, otherwise no value, “employees” → self.labour\_by(timesheet.employee, Max(timesheet.employee\_name), DRIVER\_LIMIT) when l ….
  - Value choice on labour — true gives self.activities at slice no value to DRIVER\_LIMIT, false gives no value.
  - Value choice on labour — true gives self.labour\_by(timesheet.employee, Max(timesheet.employee\_name), DRIVER\_LIMIT), false gives no value.
  - Value choice on self.access at “purchases” — true gives self.suppliers(), false gives no value.
  - Value choice on self.access at “materials” — true gives self.items(), false gives no value.

**Methods declared on this owner** [labour by](operations-003.md#op-596689359f0f74), [suppliers](operations-003.md#op-0aa8cf780cdef0), [items](operations-003.md#op-29216c7c033e3f).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1201)

<a id="op-bfccd3c560ecf6"></a>
### Cost Drivers.rate gaps

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_rate_gaps`

**Inputs** self.

**Declared result** (dict bitwise or no value).

**Explicit results** summarise\_rate\_gaps(self.activities) when self.access at “labour”, otherwise no value.

**Local steps**

- Return summarise\_rate\_gaps(self.activities) when self.access at “labour”, otherwise no value.
  - Value choice on self.access at “labour” — true gives summarise\_rate\_gaps(self.activities), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1205)

<a id="op-f01af2d3b7bc9c"></a>
### Cost Drivers.activities

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_activities`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Declared result** list at dict.

**Explicit results** self.labour\_by(qb.DocType(“Timesheet Detail”).activity\_type).

**Local steps**

- Return self.labour\_by(qb.DocType(“Timesheet Detail”).activity\_type).

**Methods declared on this owner** [labour by](operations-003.md#op-596689359f0f74).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1200)

<a id="op-596689359f0f74"></a>
### Cost Drivers.labour by

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_labour_by`

**Inputs** self, group, label = no value, limit = no value.

**Declared result** list at dict.

**Explicit results** grouped\_rows(query, group, measures, order\_by, …).

**Local steps**

- Set detail from qb.DocType(“Timesheet Detail”).
- Set timesheet from qb.DocType(“Timesheet”).
- Set query from nested operand in the contract.queries.time\_logs().join(timesheet).on(timesheet.name equals detail.parent).
- Set measures from mapping(“hours” → Sum(detail.hours)).
- If label is distinct from no value.
  - Set measures at “label” from label.
- If self.access at “labour”.
  - Set unpriced from detail.costing\_rate equals 0.
  - Set measures at “amount” from Sum(detail.base\_costing\_amount).
  - Set measures at “unpriced\_hours” from Sum(Case().when(unpriced, detail.hours).else\_(0)).
- Set order\_by from “amount” when self.access at “labour”, otherwise “hours”.
  - Value choice on self.access at “labour” — true gives “amount”, false gives “hours”.
- Return grouped\_rows(query, group, measures, order\_by, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1204)

<a id="op-0aa8cf780cdef0"></a>
### Cost Drivers.suppliers

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_suppliers`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** grouped\_rows(self.queries.non\_stock\_purchase\_items(), invoice.supplier, measures).

**Local steps**

- Set invoice from qb.DocType(“Purchase Invoice”).
- Set invoice\_item from qb.DocType(“Purchase Invoice Item”).
- Set measures from mapping(“label” → Max(invoice.supplier\_name), “amount” → Sum(invoice\_item.base\_net\_amount), “documents” → Count(invoice.name).distinct()).
- Return grouped\_rows(self.queries.non\_stock\_purchase\_items(), invoice.supplier, measures).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1206)

<a id="op-29216c7c033e3f"></a>
### Cost Drivers.items

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_costdrivers_items`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** grouped\_rows(self.queries.stock\_consumption\_entries(), ledger.item\_code, measures).

**Local steps**

- Set ledger from qb.DocType(“Stock Ledger Entry”).
- Set measures from mapping(“amount” → Sum((ledger.stock\_value\_difference × negative 1))).
- Return grouped\_rows(self.queries.stock\_consumption\_entries(), ledger.item\_code, measures).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1203)

<a id="op-90212f97994750"></a>
### Grouped rows

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_grouped_rows`

**Inputs** query, group, measures, order\_by = “amount”, limit = DRIVER\_LIMIT.

**Declared result** list at dict.

**Explicit results** query.limit(limit) when limit, otherwise query.run(as\_dict = true).

**Local steps**

- Set query from query.select(nested operand in the contract.as\_(“name”), expanded generator of nested operand in the contract for nested operand in the contract drawn from nested operand in the contract).groupby(group).or ….
  - Draw tuple(name, term) from measures.items().
- Return query.limit(limit) when limit, otherwise query.run(as\_dict = true).
  - Value choice on limit — true gives query.limit(limit), false gives query.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1207)

<a id="op-e28dd1e810444a"></a>
### Summarise rate gaps

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_drivers_summarise_rate_gaps`

**Inputs** activities.

**Declared result** dict.

**Explicit results** mapping(“hours” → unpriced\_hours, “share” → share, “estimate” → (unpriced\_hours × average\_rate) when average\_rate, otherwise no value, “understated” → share ≥ UNDERSTATED\_LABOUR\_SHARE).

**Local steps**

- Set unpriced\_hours from sum(generator of flt(row.unpriced\_hours) for row drawn from activities).
  - Draw row from activities.
- Set all\_hours from sum(generator of flt(row.hours) for row drawn from activities).
  - Draw row from activities.
- Set priced\_hours from (all\_hours − unpriced\_hours).
- Set average\_rate from (sum(generator of flt(row.amount) for row drawn from activities) ÷ priced\_hours) when priced\_hours, otherwise 0.
  - Value choice on priced\_hours — true gives (sum(generator of flt(row.amount) for row drawn from activities) ÷ priced\_hours), false gives 0.
  - Draw row from activities.
- Set share from flt(((unpriced\_hours × 100) ÷ all\_hours), 1) when all\_hours, otherwise 0.
  - Value choice on all\_hours — true gives flt(((unpriced\_hours × 100) ÷ all\_hours), 1), false gives 0.
- Return mapping(“hours” → unpriced\_hours, “share” → share, “estimate” → (unpriced\_hours × average\_rate) when average\_rate, otherwise no value, “understated” → share ≥ UNDERSTATED\_LABOUR\_SHARE).
  - Value choice on average\_rate — true gives (unpriced\_hours × average\_rate), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1208)

<a id="op-83f5cc645e9de9"></a>
### Create project budget

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_create_project_budget`

**Inputs** project, account, amount, action, check\_from, split = “Monthly”, period\_amounts = no value, from\_fiscal\_year = no value, to\_fiscal\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** str.

**State and service calls** call insert on budget · call save on budget · call submit on budget.

**Explicit results** budget.name.

**Explicit failure paths** validation helper — translated “Choose what happens when spending goes over, and where it is checked”.

**Local steps**

- Evaluate check\_access(project).
- If (action does not belong to ACTIONS or check\_from does not belong to CHECK\_FROM).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in action does not belong to ACTIONS → check\_from does not belong to CHECK\_FROM.
  - Call the validation error handler Platform.throw(translated “Choose what happens when spending goes over, and where it is checked”).
- Set budget from new\_project\_budget(project, split, from\_fiscal\_year, to\_fiscal\_year).
- Evaluate budget.update(mapping(“account” → account, “budget\_amount” → amount, “distribute\_equally” → 1)).
- Evaluate set\_checks(budget, action, CHECK\_FROM at check\_from).
- Evaluate budget.insert().
- If period\_amounts.
  - Evaluate set\_distribution(budget, Platform.parse\_json(period\_amounts)).
  - Evaluate budget.save().
- Evaluate budget.submit().
- Return budget.name.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1214)

<a id="op-1f17d7232bec49"></a>
### Get budget defaults

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_get_budget_defaults`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** BudgetYears(project).defaults().

**Local steps**

- Evaluate check\_access(project).
- Return BudgetYears(project).defaults().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1215)

<a id="op-046ed1d7453740"></a>
### Get budget periods

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_get_budget_periods`

**Inputs** project, split = “Monthly”, from\_fiscal\_year = no value, to\_fiscal\_year = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list at dict.

**Explicit results** list of mapping(“start\_date” → start, “end\_date” → end, “in\_project” → runs(start, end)) for tuple(start, end) drawn from budget.get\_budget\_periods().

**Local steps**

- Evaluate check\_access(project).
- Set budget from new\_project\_budget(project, split, from\_fiscal\_year, to\_fiscal\_year).
- Evaluate budget.set\_fiscal\_year\_dates().
- Set runs from BudgetYears(project).runs\_between.
- Return list of mapping(“start\_date” → start, “end\_date” → end, “in\_project” → runs(start, end)) for tuple(start, end) drawn from budget.get\_budget\_periods().
  - Draw tuple(start, end) from budget.get\_budget\_periods().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1216)

<a id="op-c3829ce46d4937"></a>
### Get project budgets

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_get_project_budgets`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Record and data access** read “Project” via get\_value · read “Budget” via get\_list · read “Company” via get\_cached\_value.

**Explicit results** mapping(“currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “budgets” → list of budget\_row(budget) for budget drawn from budgets).

**Local steps**

- Evaluate check\_access(project).
- Set company from Platform.db.get\_value(“Project”, project, “company”).
- Set budgets from Platform.get\_list(“Budget”, filters = mapping(“budget\_against” → “Project”, “project” → project), fields = list(expanded BUDGET\_FIELDS, “from\_fiscal\_year”, “to\_fiscal\_year”, “distribution\_frequency”, …), o ….
- Return mapping(“currency” → Platform.get\_cached\_value(“Company”, company, “default\_currency”), “budgets” → list of budget\_row(budget) for budget drawn from budgets).
  - Draw budget from budgets.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1217)

<a id="op-8db0e5958d3d53"></a>
### Budget row

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_budget_row`

**Inputs** budget.

**Declared result** dict.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** mapping(“name” → budget.name, “account” → budget.account, “account\_name” → Platform.get\_cached\_value(“Account”, budget.account, “account\_name”), “amount” → flt(budget.budget\_amount), …).

**Local steps**

- Set control from budget\_control(budget).
- Return mapping(“name” → budget.name, “account” → budget.account, “account\_name” → Platform.get\_cached\_value(“Account”, budget.account, “account\_name”), “amount” → flt(budget.budget\_amount), …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, budget.account, “account\_name”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1209)

<a id="op-f7b1ba3e737c05"></a>
### New project budget

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_new_project_budget`

**Inputs** project, split, from\_fiscal\_year, to\_fiscal\_year.

**Record and data access** resolve a document from mapping(“doctype” → “Budget”, “budget\_against” → “Project”, “project” → project, “company” → Platform.db.get\_value(“Project”, project, “company”), …) via get\_doc · read “Project” via get\_value.

**Explicit results** Platform.get\_doc(mapping(“doctype” → “Budget”, “budget\_against” → “Project”, “project” → project, “company” → Platform.db.get\_value(“Project”, project, “company”), …)).

**Local steps**

- If not (from\_fiscal\_year and to\_fiscal\_year).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_fiscal\_year → to\_fiscal\_year.
  - Set defaults from BudgetYears(project).defaults().
  - Set from\_fiscal\_year from (from\_fiscal\_year or defaults at “from\_fiscal\_year”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_fiscal\_year → defaults at “from\_fiscal\_year”.
  - Set to\_fiscal\_year from (to\_fiscal\_year or defaults at “to\_fiscal\_year”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_fiscal\_year → defaults at “to\_fiscal\_year”.
- Return Platform.get\_doc(mapping(“doctype” → “Budget”, “budget\_against” → “Project”, “project” → project, “company” → Platform.db.get\_value(“Project”, project, “company”), …)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1218)

<a id="op-103f0e94c90f16"></a>
### Budget Years.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_budgetyears_init`

**Inputs** self, project.

**Record and data access** read “Project” via get\_value.

**Local steps**

- Set self.project from Platform.db.get\_value(“Project”, project, list(“company”, “expected\_start\_date”, “expected\_end\_date”), as\_dict = true).
- Set self.start from getdate((self.project.expected\_start\_date or getdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.project.expected\_start\_date → getdate().
- Set self.end from getdate(self.project.expected\_end\_date) when self.project.expected\_end\_date, otherwise no value.
  - Value choice on self.project.expected\_end\_date — true gives getdate(self.project.expected\_end\_date), false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1211)

<a id="op-b8c951f663aea1"></a>
### Budget Years.defaults

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_budgetyears_defaults`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping(“fiscal\_years” → list of year.name for year drawn from years at slice years.index(first) to no value, “from\_fiscal\_year” → first.name, “to\_fiscal\_year” → last.name, “capped” → bool((self.end and se ….

**Explicit failure paths** validation helper — translated “Set up a Fiscal Year for {0} first”.format(self.project.company).

**Local steps**

- Set years from company\_fiscal\_years(self.project.company).
- If not years.
  - Call the validation error handler Platform.throw(translated “Set up a Fiscal Year for {0} first”.format(self.project.company)).
- Set first from year\_containing(years, self.start).
- Set last from year\_containing(years, self.end) when self.end, otherwise first.
  - Value choice on self.end — true gives year\_containing(years, self.end), false gives first.
- If years.index(last) &lt; years.index(first).
  - Set last from first.
- Return mapping(“fiscal\_years” → list of year.name for year drawn from years at slice years.index(first) to no value, “from\_fiscal\_year” → first.name, “to\_fiscal\_year” → last.name, “capped” → bool((self.end and se ….
  - Draw year from years at slice years.index(first) to no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.end → self.end &gt; getdate(years at negative 1.year\_end\_date).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1210)

<a id="op-423fbc27c591e1"></a>
### Budget Years.runs between

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_budgetyears_runs_between`

**Inputs** self, start, end.

**Declared result** bool.

**Explicit results** true · (getdate(start) ≤ self.end and getdate(end) ≥ self.start).

**Local steps**

- If not (self.project.expected\_start\_date and self.end).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project.expected\_start\_date → self.end.
  - Return true.
- Return (getdate(start) ≤ self.end and getdate(end) ≥ self.start).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(start) ≤ self.end → getdate(end) ≥ self.start.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1212)

<a id="op-69d738f68cb6cb"></a>
### Company fiscal years

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_company_fiscal_years`

**Inputs** company.

**Declared result** list at Platform.\_dict.

**Record and data access** read “Fiscal Year” via get\_all · read “Fiscal Year Company” via get\_all.

**Explicit results** list of year for year drawn from years where (not named.get(year.name) or company belongs to named at year.name).

**Local steps**

- Set years from Platform.get\_all(“Fiscal Year”, filters = mapping(“disabled” → 0), fields = list(“name”, “year\_start\_date”, “year\_end\_date”), order\_by = “year\_start\_date”).
- Set named from mapping().
- For each row in Platform.get\_all(“Fiscal Year Company”, fields = list(“parent”, “company”)).
  - Evaluate named.setdefault(row.parent, set()).add(row.company).
- Return list of year for year drawn from years where (not named.get(year.name) or company belongs to named at year.name).
  - Draw year from years, keep a combination only if ((not named.get(year.name) or company belongs to named at year.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not named.get(year.name) → company belongs to named at year.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L203) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1213)

<a id="op-4632090c7c6283"></a>
### Year containing

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_year_containing`

**Inputs** years, date.

**Declared result** Platform.\_dict.

**Explicit results** year · years at 0 when date &lt; getdate(years at 0.year\_start\_date), otherwise years at negative 1.

**Local steps**

- For each year in years.
  - If getdate(year.year\_start\_date) ≤ date ≤ getdate(year.year\_end\_date).
    - Compare adjacent operands in order, stopping at the first false comparison in getdate(year.year\_start\_date) ≤ date ≤ getdate(year.year\_end\_date).
    - Return year.
- Return years at 0 when date &lt; getdate(years at 0.year\_start\_date), otherwise years at negative 1.
  - Value choice on date &lt; getdate(years at 0.year\_start\_date) — true gives years at 0, false gives years at negative 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1221)

<a id="op-e2d32adddf87c1"></a>
### Set distribution

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_set_distribution`

**Inputs** budget, amounts.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Enter an amount for each of the {0} periods”.format(len(budget.budget\_distribution)).

**Local steps**

- If len(amounts) differs from len(budget.budget\_distribution).
  - Call the validation error handler Platform.throw(translated “Enter an amount for each of the {0} periods”.format(len(budget.budget\_distribution))).
- Set budget.distribute\_equally from 0.
- For each tuple(row, amount) in zip(budget.budget\_distribution, amounts, strict = true).
  - Set row.amount from flt(amount).
  - Set row.percent from ((flt(amount) × 100) ÷ flt(budget.budget\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1220)

<a id="op-e19510827a7a55"></a>
### Set checks

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_budgets_set_checks`

**Inputs** budget, action, stages.

**Declared result** no value.

**Local steps**

- For each tuple(stage, applies, annual, monthly) in CONTROL\_STAGES.
  - Set checked from stage belongs to stages.
  - Evaluate budget.set(applies, int(checked)).
  - If checked.
    - Evaluate budget.set(annual, action).
    - Evaluate budget.set(monthly, “Ignore”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1219)

<a id="op-7ab56e65c2bd18"></a>
### Get project costing

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_get_project_costing`

**Inputs** project.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** dict.

**Explicit results** ProjectCosting(project).build().

**Local steps**

- Evaluate check\_access(project).
- Return ProjectCosting(project).build().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1235)

<a id="op-05bf05015d1fe7"></a>
### Get project invoices

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_get_project_invoices`

**Inputs** project, start = 0.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Declared result** list at dict.

**Explicit results** (billing.invoices(start = max(start, 0), page\_length = INVOICE\_PAGE) or list()).

**Local steps**

- Evaluate check\_access(project).
- Set billing from ProjectBilling(project, get\_costing\_access()).
- Return (billing.invoices(start = max(start, 0), page\_length = INVOICE\_PAGE) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in billing.invoices(start = max(start, 0), page\_length = INVOICE\_PAGE) → list().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1236)

<a id="op-8dae9e3ae9b780"></a>
### Project Costing.initialize

`operation_enterprise_binding_enterprise_projects_doctype_project_costing_project_costing_projectcosting_init`

**Inputs** self, project.

**Record and data access** read “Project” via get\_value · read “Company” via get\_cached\_value.

**Local steps**

- Set self.project from Platform.db.get\_value(“Project”, project, PROJECT\_FIELDS, as\_dict = true).
- Set self.queries from ProjectCostQueries(project).
- Set self.access from get\_costing\_access().
- Set self.currency from Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.project.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1246)
