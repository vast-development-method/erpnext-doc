# Purchasing · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Supplier scorecard

[Record definition](../../../../data/record-types/supplier_scorecard.json)

<a id="op-144545fdaef742"></a>
### Supplier Scorecard.score within standing

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_supplier_scorecard_score_within_standing`

**Inputs** self, standing, highest\_grade.

**Explicit results** (above\_min and score ≤ standing.max\_grade) · (above\_min and (not standing.max\_grade or standing.max\_grade &gt; score)).

**Local steps**

- Set score from self.supplier\_score.
- Set above\_min from (not standing.min\_grade or standing.min\_grade ≤ score).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not standing.min\_grade → standing.min\_grade ≤ score.
- If (standing.max\_grade and standing.max\_grade equals highest\_grade).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in standing.max\_grade → standing.max\_grade equals highest\_grade.
  - Return (above\_min and score ≤ standing.max\_grade).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in above\_min → score ≤ standing.max\_grade.
- Return (above\_min and (not standing.max\_grade or standing.max\_grade &gt; score)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in above\_min → (not standing.max\_grade or standing.max\_grade &gt; score).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not standing.max\_grade → standing.max\_grade &gt; score.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0351.json#L4995) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L115)

<a id="op-08a566b46eb2fd"></a>
### Get timeline data

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_get_timeline_data`

**Inputs** doctype, name.

**Declared result** dict at tuple(float, float).

**Record and data access** resolve a document from doctype via get\_doc · execute query text (SELECT, Supplier Scorecard Period) · read “Supplier Scorecard Period” via get\_value.

**Explicit results** timeline\_data.

**Local steps**

- Set scs from Platform.get\_doc(doctype, name).
- Set timeline\_data from mapping().
- Set scorecards from Platform.db.sql(query text (SELECT, Supplier Scorecard Period), mapping(“scs” → scs.name), as\_dict = 1).
- For each sc in scorecards.
  - Set tuple(start\_date, end\_date, total\_score) from Platform.db.get\_value(“Supplier Scorecard Period”, sc.name, list(“start\_date”, “end\_date”, “total\_score”)).
  - For each single\_date in daterange(start\_date, end\_date).
    - Set timeline\_data at time.mktime(single\_date.timetuple()) from total\_score.
- Return timeline\_data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L211) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L109)

<a id="op-ddd371ec6e3cd9"></a>
### Daterange

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_daterange`

**Inputs** start\_date, end\_date.

**Local steps**

- For each n in range((int((end\_date − start\_date).days) + 1)).
  - yield (start\_date + timedelta(n)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0351.json#L5890) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L105)

<a id="op-3306c043b7e12a"></a>
### Refresh scorecards

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_refresh_scorecards`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Supplier Scorecard).

**State and service calls** savepoint “refresh\_scorecard” · rollback.

**Local steps**

- Set scorecards from Platform.db.sql(query text (SELECT, Supplier Scorecard), mapping(), as\_dict = 1).
- For each sc in scorecards.
  - Evaluate Platform.db.savepoint(“refresh\_scorecard”).
  - Attempt the following.
    - Evaluate make\_all\_scorecards(sc.name).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = “refresh\_scorecard”).
    - Evaluate Platform.log\_error(translated “Supplier Scorecard refresh failed”, reference\_doctype = “Supplier Scorecard”, reference\_name = sc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L112)

<a id="op-be0e951f980edc"></a>
### Make all scorecards

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_make_all_scorecards`

**Inputs** docname.

**Record and data access** resolve a document from “Supplier Scorecard” via get\_doc.

**State and service calls** call save on sc.

**Explicit results** scp\_count.

**Local steps**

- Set sc from Platform.get\_doc(“Supplier Scorecard”, docname).
- Set scp\_count from create\_scorecard\_periods(sc).
- If scp\_count &gt; 0.
  - Evaluate sc.save().
- Return scp\_count.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L110)

<a id="op-dac99c3bc63193"></a>
### Create scorecard periods

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_supplier_scorecard_create_scorecard_periods`

**Inputs** sc.

**Record and data access** resolve a document from “Supplier” via get\_doc.

**State and service calls** call insert on period\_card · call submit on period\_card · msgprint with ((((nested operand in the contract(nested operand in the contract).format(scp\_count, sc.supplier) + one space) + str(first\_start\_date)) + “ - ”) + str(last\_end\_date)).

**Explicit results** scp\_count.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, sc.supplier).
- Evaluate supplier.check\_permission(“write”).
- Set start\_date from getdate(supplier.creation).
- Set end\_date from get\_scorecard\_date(sc.period, start\_date).
- Set todays from getdate(nowdate()).
- Set scp\_count from 0.
- Set first\_start\_date from todays.
- Set last\_end\_date from todays.
- While end\_date &lt; todays.
  - Set overlapping\_end from get\_overlapping\_period\_end(sc.name, start\_date, end\_date).
  - If overlapping\_end.
    - Set start\_date from getdate(add\_days(overlapping\_end, 1)).
    - Set end\_date from get\_scorecard\_date(sc.period, start\_date).
    - Continue with the next iteration or loop test.
  - Set period\_card from make\_supplier\_scorecard(sc.name, no value).
  - Set period\_card.start\_date from start\_date.
  - Set period\_card.end\_date from end\_date.
  - Evaluate period\_card.insert(ignore\_permissions = true).
  - Evaluate period\_card.submit().
  - Set scp\_count from (scp\_count + 1).
  - If start\_date &lt; first\_start\_date.
    - Set first\_start\_date from start\_date.
  - Set last\_end\_date from end\_date.
  - Set start\_date from getdate(add\_days(end\_date, 1)).
  - Set end\_date from get\_scorecard\_date(sc.period, start\_date).
- <a id="op-dac99c3bc63193-guard-32"></a>If scp\_count &gt; 0.
  - Evaluate Platform.msgprint(((((nested operand in the contract.format(scp\_count, nested operand in the contract.supplier) + one space) + str(first\_start\_date)) + “ - ”) + str(last\_end\_date))).
- Return scp\_count.

**Derived branch illustrations**

- At the comparison scp\_count &gt; 0, scp\_count = 1 selects the branch that requests a message with ((((nested operand in the contract(nested operand in the contract).format(scp\_count, sc.supplier) + one space) + str(first\_start\_date …. With scp\_count = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-dac99c3bc63193-guard-32)

**Values supplied outside this operation** effective access from supplier.check\_permission(“write”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L844) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L84)

<a id="op-555c05b0f4b44a"></a>
### Get scorecard date

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_get_scorecard_date`

**Inputs** period, start\_date.

**Explicit results** end\_date.

**Local steps**

- If period equals “Per Week”.
  - Set end\_date from getdate(add\_days(start\_date, 6)).
- Otherwise.
  - If period equals “Per Month”.
    - Set end\_date from get\_last\_day(start\_date).
  - Otherwise.
    - If period equals “Per Year”.
      - Set end\_date from add\_days(add\_years(start\_date, 1), negative 1).
- Return end\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L210) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L108)

<a id="op-8d2b80560bd298"></a>
### Get default scorecard variables

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_get_default_scorecard_variables`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“param\_name” → “total\_accepted\_items”, “variable\_label” → “Total Accepted Items”, “path” → “get\_total\_accepted\_items”), mapping(“param\_name” → “total\_accepted\_amount”, “variable\_label” → “Tota ….

**Local steps**

- Return list(mapping(“param\_name” → “total\_accepted\_items”, “variable\_label” → “Total Accepted Items”, “path” → “get\_total\_accepted\_items”), mapping(“param\_name” → “total\_accepted\_amount”, “variable\_label” → “Tota ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L107)

<a id="op-411fb5d87aaa7d"></a>
### Get default scorecard standing

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_get_default_scorecard_standing`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“min\_grade” → 0.0, “prevent\_rfqs” → 1, “warn\_rfqs” → 0, “notify\_supplier” → 0, …), mapping(“min\_grade” → 30.0, “prevent\_rfqs” → 0, “warn\_rfqs” → 1, “notify\_supplier” → 0, …), mapping(“min\_grad ….

**Local steps**

- Return list(mapping(“min\_grade” → 0.0, “prevent\_rfqs” → 1, “warn\_rfqs” → 0, “notify\_supplier” → 0, …), mapping(“min\_grade” → 30.0, “prevent\_rfqs” → 0, “warn\_rfqs” → 1, “notify\_supplier” → 0, …), mapping(“min\_grad ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L1154) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L106)

<a id="op-d0326de35dbf14"></a>
### Make default records

`operation_enterprise_buying_record_definitions_supplier_scorecard_business_behavior_make_default_records`

**Inputs** no declared parameters.

**Record and data access** resolve a document from d via get\_doc.

**State and service calls** call insert on Platform.get\_doc(d).

**Local steps**

- Set install\_variable\_docs from get\_default\_scorecard\_variables().
- For each d in install\_variable\_docs.
  - Attempt the following.
    - Set d at “doctype” from “Supplier Scorecard Variable”.
    - Evaluate Platform.get\_doc(d).insert().
  - On failure (Platform.NameError).
    - Take no action here.
- Set install\_standing\_docs from get\_default\_scorecard\_standing().
- For each d in install\_standing\_docs.
  - Attempt the following.
    - Set d at “doctype” from “Supplier Scorecard Standing”.
    - Evaluate Platform.get\_doc(d).insert().
  - On failure (Platform.NameError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L111)

<a id="op-bb517343a36b3f"></a>
### Get data

`operation_enterprise_buying_record_definitions_supplier_scorecard_supplier_scorecard_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“heatmap” → true, “heatmap\_message” → translated “This covers all scorecards tied to this Setup”, “fieldname” → “supplier”, “transactions” → list(mapping(“label” → translated “Scorecards”, “items”  ….

**Local steps**

- Return mapping(“heatmap” → true, “heatmap\_message” → translated “This covers all scorecards tied to this Setup”, “fieldname” → “supplier”, “transactions” → list(mapping(“label” → translated “Scorecards”, “items”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L142)

## Record · Supplier scorecard criteria

[Record definition](../../../../data/record-types/supplier_scorecard_criteria.json)

<a id="op-6556c182037c43"></a>
### Supplier Scorecard Criteria.validate

`operation_enterprise_buying_record_definitions_supplier_scorecard_criteria_business_behavior_supplier_scorecard_criteria_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_variables().
- Evaluate self.validate\_formula().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate variables](operations-012.md#op-e3011bfcda69f6), [validate formula](operations-012.md#op-480e94b13d6370).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L4730) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L123)

<a id="op-e3011bfcda69f6"></a>
### Supplier Scorecard Criteria.validate variables

`operation_enterprise_buying_record_definitions_supplier_scorecard_criteria_business_behavior_supplier_scorecard_criteria_validate_variables`

**Inputs** self.

**Local steps**

- Evaluate \_get\_variables(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L4801) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L125)

<a id="op-480e94b13d6370"></a>
### Supplier Scorecard Criteria.validate formula

`operation_enterprise_buying_record_definitions_supplier_scorecard_criteria_business_behavior_supplier_scorecard_criteria_validate_formula`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L124)

<a id="op-006538c4127660"></a>
### Get criteria list

`operation_enterprise_buying_record_definitions_supplier_scorecard_criteria_business_behavior_get_criteria_list`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Supplier Scorecard Criteria).

**Explicit results** criteria.

**Local steps**

- Set criteria from Platform.db.sql(query text (SELECT, Supplier Scorecard Criteria), mapping(), as\_dict = 1).
- Return criteria.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L120)

<a id="op-a95e6bf8d4024b"></a>
### Get variables

`operation_enterprise_buying_record_definitions_supplier_scorecard_criteria_business_behavior_get_variables`

**Inputs** criteria\_name.

**Record and data access** resolve a document from “Supplier Scorecard Criteria” via get\_doc.

**Explicit results** \_get\_variables(criteria).

**Local steps**

- Set criteria from Platform.get\_doc(“Supplier Scorecard Criteria”, criteria\_name).
- Return \_get\_variables(criteria).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L5366) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L121)

<a id="op-b6c6c20dfeded7"></a>
### Get variables

`operation_enterprise_buying_record_definitions_supplier_scorecard_criteria_business_behavior_get_variables_2`

**Inputs** criteria.

**Record and data access** execute query text (SELECT, Supplier Scorecard Variable).

**Explicit results** my\_variables.

**Explicit failure paths** validation helper with InvalidFormulaVariable — ((translated “Unable to find variable:” + one space) + str(match.group(1))).

**Local steps**

- Set my\_variables from list().
- Set regex from “\\{(.\*?)\\}”.
- Set mylist from re.finditer(regex, criteria.formula, (re.MULTILINE bitwise or re.DOTALL)).
- For each tuple(\_dummy1, match) in enumerate(mylist).
  - For each \_dummy2 in range(0, len(match.groups())).
    - Attempt the following.
      - Set var from Platform.db.sql(query text (SELECT, Supplier Scorecard Variable), mapping(“param” → match.group(1)), as\_dict = 1) at 0.
      - Evaluate my\_variables.append(var).
    - On failure (Exception).
      - Call the validation error handler Platform.throw(((translated “Unable to find variable:” + one space) + str(match.group(1))), InvalidFormulaVariable).
- Return my\_variables.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L122)

## Record · Supplier scorecard period

[Record definition](../../../../data/record-types/supplier_scorecard_period.json)

<a id="op-6f95f2e20b9fb0"></a>
### Supplier Scorecard Period.validate

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_validate`

**Inputs** self.

**Record and data access** read “Supplier Scorecard” via get\_value.

**Local steps**

- Set self.supplier from Platform.db.get\_value(“Supplier Scorecard”, self.scorecard, “supplier”).
- Evaluate self.validate\_from\_to\_dates(“start\_date”, “end\_date”).
- Evaluate self.validate\_overlapping\_period().
- Evaluate self.validate\_criteria\_weights().
- Evaluate self.calculate\_variables().
- Evaluate self.calculate\_criteria().
- Evaluate self.calculate\_score().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate overlapping period](operations-012.md#op-c240073936ccbe), [validate criteria weights](operations-012.md#op-4f533332615a12), [calculate variables](operations-012.md#op-6e49dfb8e2170d), [calculate criteria](operations-012.md#op-529a942b5a8fe6), [calculate score](operations-012.md#op-4f3eff9c50272f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L137)

<a id="op-c240073936ccbe"></a>
### Supplier Scorecard Period.validate overlapping period

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_period_supplier_scorecard_period_supplierscorecardperiod_validate_overlapping_period`

**Inputs** self.

**Local steps**

- If has\_overlapping\_period(self.scorecard, self.start\_date, self.end\_date).
  - Evaluate throw(translated “Supplier Scorecard {0} already has a submitted period overlapping {1} to {2}”.format(self.scorecard, formatdate(self.start\_date), formatdate(self.end\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L843) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L83)

<a id="op-4f533332615a12"></a>
### Supplier Scorecard Period.validate criteria weights

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_validate_criteria_weights`

**Inputs** self.

**Local steps**

- Set weight from 0.
- For each c in self.criteria.
  - Update weight using + c.weight.
- If flt(weight, 2) differs from 100.
  - Evaluate throw(translated “Criteria weights must add up to 100%”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L138)

<a id="op-6e49dfb8e2170d"></a>
### Supplier Scorecard Period.calculate variables

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_calculate_variables`

**Inputs** self.

**Local steps**

- For each var in self.variables.
  - If “.” belongs to var.path.
    - Set method\_to\_call from import\_string\_path(var.path).
    - Set var.value from method\_to\_call(self).
  - Otherwise.
    - Set method\_to\_call from getattr(variable\_functions, var.path).
    - Set var.value from method\_to\_call(self).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(variable\_functions, var.path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L6392) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L134)

<a id="op-529a942b5a8fe6"></a>
### Supplier Scorecard Period.calculate criteria

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_calculate_criteria`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L132)

<a id="op-4f3eff9c50272f"></a>
### Supplier Scorecard Period.calculate score

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_calculate_score`

**Inputs** self.

**Local steps**

- Set myscore from 0.
- For each crit in self.criteria.
  - If crit.max\_score.
    - Update myscore using + ((crit.score × crit.weight) ÷ crit.max\_score).
- Set self.total\_score from myscore.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L133)

<a id="op-8ee4589a2b74a7"></a>
### Supplier Scorecard Period.calculate weighted score

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_calculate_weighted_score`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, weighing\_function.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0352.json#L6965) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L135)
