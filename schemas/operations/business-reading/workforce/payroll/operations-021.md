# Payroll and benefits · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Salary withholding

[Record definition](../../../../data/record-types/salary_withholding.json)

<a id="op-1abad3b41680a9"></a>
### Salary Withholding.validate duplicate record

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_validate_duplicate_record`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Salary Withholding {0} already exists for employee {1} for the selected period”.format(get\_link\_to\_form(“Salary Withholding”, duplicate at 0), Platform.bold(formatted text {self.employee}: {sel ….

**Local steps**

- Set Withholding from Platform.qb.DocType(“Salary Withholding”).
- Set duplicate from nested operand in the contract(nested operand in the contract).select(Withholding.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in th ….
- If duplicate.
  - Call the validation error handler Platform.throw(translated “Salary Withholding {0} already exists for employee {1} for the selected period”.format(get\_link\_to\_form(“Salary Withholding”, duplicate at 0), Platform.bold(formatted text {self. ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L921) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1268)

<a id="op-4517f0efc909b2"></a>
### Salary Withholding.set status

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_set_status`

**Inputs** self, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- If self.docstatus equals 0.
  - Set status from “Draft”.
- Otherwise.
  - If self.docstatus equals 1.
    - If all(generator of cycle.is\_salary\_released for cycle drawn from self.cycles).
      - Draw cycle from self.cycles.
      - Set status from “Released”.
    - Otherwise.
      - Set status from “Withheld”.
  - Otherwise.
    - If self.docstatus equals 2.
      - Set status from “Cancelled”.
- If update.
  - Evaluate self.db\_set(“status”, status).
- Otherwise.
  - Set self.status from status.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L476) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L918) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1265)

<a id="op-97b71b56a6b411"></a>
### Salary Withholding.set withholding cycles and to date

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_set_withholding_cycles_and_to_date`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Local steps**

- Set self.to\_date from self.get\_to\_date().
- Set cycle\_from\_date, cycle\_to\_date from getdate(self.from\_date).
- Set self.cycles from list().
- While cycle\_to\_date &lt; getdate(self.to\_date).
  - Set cycle\_to\_date from (add\_to\_date(cycle\_from\_date, expanded names self.get\_frequency\_kwargs()) − relativedelta(days = 1)).
  - Evaluate self.append(“cycles”, mapping(“from\_date” → cycle\_from\_date, “to\_date” → cycle\_to\_date, “is\_salary\_released” → 0)).
  - Set cycle\_from\_date from add\_days(cycle\_to\_date, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get to date](operations-021.md#op-ef81a5b9ba7ec3), [get frequency kwargs](operations-021.md#op-2e9dbf4aa47b9f).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L759) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L919) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1266)

<a id="op-ef81a5b9ba7ec3"></a>
### Salary Withholding.get to date

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_get_to_date`

**Inputs** self.

**Declared result** str.

**Explicit results** to\_date.

**Local steps**

- Set from\_date from getdate(self.from\_date).
- Set kwargs from self.get\_frequency\_kwargs(self.number\_of\_withholding\_cycles).
- Set to\_date from (add\_to\_date(from\_date, expanded names kwargs) − relativedelta(days = 1)).
- Return to\_date.

**Methods declared on this owner** [get frequency kwargs](operations-021.md#op-2e9dbf4aa47b9f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L1114) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L916) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1263)

<a id="op-2e9dbf4aa47b9f"></a>
### Salary Withholding.get frequency kwargs

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_get_frequency_named_arguments`

**Inputs** self, withholding\_cycles = 0.

**Declared result** dict.

**Explicit results** frequency\_dict.get(self.payroll\_frequency).

**Local steps**

- Set cycles from (cint(withholding\_cycles) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(withholding\_cycles) → 1.
- Set frequency\_dict from mapping(“Monthly” → mapping(“months” → (1 × cycles)), “Bimonthly” → mapping(“months” → (2 × cycles)), “Fortnightly” → mapping(“days” → (14 × cycles)), “Weekly” → mapping(“days” → (7 × cycles)), …).
- Return frequency\_dict.get(self.payroll\_frequency).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L1280) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L915) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1262)

<a id="op-6eea188faba38e"></a>
### Salary Withholding.on discard

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_salary_withholding_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L1578) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L917) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1264)

<a id="op-105dc56f3459d1"></a>
### Get payroll frequency

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_get_payroll_frequency`

**Inputs** employee, posting\_date.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Record and data access** read “Salary Structure Assignment” via get\_value · read “Salary Structure” via get\_value.

**Explicit results** Platform.db.get\_value(“Salary Structure”, salary\_structure, “payroll\_frequency”).

**Explicit failure paths** validation helper — translated “No Salary Structure Assignment found for employee {0} on or before {1}”.format(employee, posting\_date).

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set salary\_structure from Platform.db.get\_value(“Salary Structure Assignment”, mapping(“employee” → employee, “from\_date” → tuple(“&lt;=”, posting\_date), “docstatus” → 1), “salary\_structure”, order\_by = “from\_date desc”).
- If not salary\_structure.
  - Call the validation error handler Platform.throw(translated “No Salary Structure Assignment found for employee {0} on or before {1}”.format(employee, posting\_date), title = translated “Error”).
- Return Platform.db.get\_value(“Salary Structure”, salary\_structure, “payroll\_frequency”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L1641) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L913) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1260)

<a id="op-5219be03f0d0a5"></a>
### Link bank entry in salary withholdings

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_link_bank_entry_in_salary_withholdings`

**Inputs** salary\_slips, bank\_entry.

**Local steps**

- Set WithholdingCycle from Platform.qb.DocType(“Salary Withholding Cycle”).
- Evaluate nested operand in the contract(nested operand in the contract).set(WithholdingCycle.journal\_entry, bank\_entry).where(WithholdingCycle.name.isin(list of salary\_slip.salary\_withholding\_cycle for salary\_slip  ….run().
  - Draw salary\_slip from salary\_slips.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L2042) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L914) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1261)

<a id="op-91d312658d204e"></a>
### Update salary withholding payment status

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_update_salary_withholding_payment_status`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- Set Withholding from Platform.qb.DocType(“Salary Withholding”).
- Set WithholdingCycle from Platform.qb.DocType(“Salary Withholding Cycle”).
- Set withholdings from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“salary\_withholding\_cycle”), nested operand in the contract.as\_(“salary\_withholding”), Withholding.e ….
- If not withholdings.
  - Return no value.
- Set cancel from method equals “on\_cancel”.
- Evaluate \_update\_payment\_status\_in\_payroll(withholdings, cancel = cancel).
- Evaluate \_update\_salary\_withholdings(withholdings, cancel = cancel).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L2260) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L923) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1270)

<a id="op-0fb6cf0597f08c"></a>
### Update payment status in payroll

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_update_payment_status_in_payroll`

**Inputs** withholdings, cancel = false.

**Declared result** no value.

**Local steps**

- Set status from “Withheld” when cancel, otherwise “Submitted”.
  - Value choice on cancel — true gives “Withheld”, false gives “Submitted”.
- Set SalarySlip from Platform.qb.DocType(“Salary Slip”).
- Evaluate nested operand in the contract(nested operand in the contract).set(SalarySlip.status, status).where(SalarySlip.salary\_withholding\_cycle.isin(list of withholding.salary\_withholding\_cycle for withholding dra ….run().
  - Draw withholding from withholdings.
- Set employees from list of withholding.employee for withholding drawn from withholdings.
  - Draw withholding from withholdings.
- Set is\_salary\_withheld from 1 when cancel, otherwise 0.
  - Value choice on cancel — true gives 1, false gives 0.
- Set PayrollEmployee from Platform.qb.DocType(“Payroll Employee Detail”).
- Evaluate nested operand in the contract(nested operand in the contract).set(PayrollEmployee.is\_salary\_withheld, is\_salary\_withheld).where(PayrollEmployee.employee.isin(employees)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L2761) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L922) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1269)

<a id="op-4ea09f7d83da84"></a>
### Update salary withholdings

`operation_workforce_payroll_record_definitions_salary_withholding_business_behavior_update_salary_withholdings`

**Inputs** withholdings, cancel = false.

**Declared result** no value.

**Record and data access** resolve a document from “Salary Withholding” via get\_doc.

**State and service calls** call db\_set on cycle.

**Local steps**

- Set is\_salary\_released from 0 when cancel, otherwise 1.
  - Value choice on cancel — true gives 0, false gives 1.
- For each withholding in withholdings.
  - Set withholding\_doc from Platform.get\_doc(“Salary Withholding”, withholding.salary\_withholding).
  - For each cycle in withholding\_doc.cycles.
    - If cycle.name equals withholding.salary\_withholding\_cycle.
      - Evaluate cycle.db\_set(“is\_salary\_released”, is\_salary\_released).
      - If cancel.
        - Evaluate cycle.db\_set(“journal\_entry”, no value).
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate withholding\_doc.set\_status(update = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0141.json#L3195) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L924) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1271)

## Service · Utils

<a id="op-2e72bec71794d0"></a>
### Sanitize expression

`operation_workforce_payroll_utils_business_behavior_sanitize_expression`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** string.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L582) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1050) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1386)

<a id="op-2064266deb8478"></a>
### Get component abbr map

`operation_workforce_payroll_utils_business_behavior_get_component_abbreviation_map`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** Platform.cache().get\_value(SALARY\_COMPONENT\_VALUES, generator = \_fetch\_component\_values).

**Local steps**

- Bind local operation \_fetch\_component\_values for subsequent calls.
- Return Platform.cache().get\_value(SALARY\_COMPONENT\_VALUES, generator = \_fetch\_component\_values).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L730) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1044) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1380)

<a id="op-4c2d4403664052"></a>
### Get component abbr map.fetch component values

`operation_workforce_payroll_utils_business_behavior_get_component_abbreviation_map_fetch_component_values`

**Inputs** no declared parameters.

**Record and data access** read “Salary Component” via get\_all.

**Explicit results** mapping of abbr → 0 for abbr drawn from Platform.get\_all(“Salary Component”, pluck = “salary\_component\_abbr”).

**Local steps**

- Return mapping of abbr → 0 for abbr drawn from Platform.get\_all(“Salary Component”, pluck = “salary\_component\_abbr”).
  - Draw abbr from Platform.get\_all(“Salary Component”, pluck = “salary\_component\_abbr”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L876) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1045) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1381)

<a id="op-d6ba1f50dba774"></a>
### Get salary slip field defaults

`operation_workforce_payroll_utils_business_behavior_get_salary_slip_field_defaults`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** defaults.

**Local steps**

- Set defaults from get\_new\_doc(“Salary Slip”, as\_dict = true).
- For each df in Platform.get\_meta(“Salary Slip”).fields.
  - If (df.fieldtype belongs to numeric\_fieldtypes and defaults.get(df.fieldname) is identical to no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype belongs to numeric\_fieldtypes → defaults.get(df.fieldname) is identical to no value.
    - Set defaults at df.fieldname from 0.
- Return defaults.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L966) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1048) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1384)

<a id="op-50cdbd0665f9b2"></a>
### Get component eval context

`operation_workforce_payroll_utils_business_behavior_get_component_evaluate_context`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** employee, ssa\_as\_dict.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0003.json#L14) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1046) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1382)

<a id="op-0b8fd1e7877c34"></a>
### Check attributes

`operation_workforce_payroll_utils_business_behavior_check_attributes`

**Inputs** code.

**Declared result** no value.

**Explicit failure paths** SyntaxError(formatted text Illegal rule {Platform.bold(code)}. Cannot use "{attribute}") · SyntaxError(formatted text Operation not allowed: line {node.lineno} column {node.col\_offset}) · SyntaxError(formatted text Illegal rule {Platform.bold(code)}. Cannot use "{node.attr}").

**Local steps**

- Bind dependencies ast.
- Bind dependencies UNSAFE\_ATTRIBUTES.
- Set unsafe\_attrs from (set(UNSAFE\_ATTRIBUTES).union(list(“\_\_”)) − set(“format”)).
- For each attribute in unsafe\_attrs.
  - If attribute belongs to code.
    - Raise SyntaxError(formatted text Illegal rule {Platform.bold(code)}. Cannot use "{attribute}").
- Set BLOCKED\_NODES from tuple(ast.NamedExpr, ast.Lambda).
- Set tree from ast.parse(code, mode = “eval”).
- For each node in ast.walk(tree).
  - If isinstance(node, BLOCKED\_NODES).
    - Raise SyntaxError(formatted text Operation not allowed: line {node.lineno} column {node.col\_offset}).
  - If (isinstance(node, ast.Attribute) and isinstance(node.attr, str) and node.attr belongs to UNSAFE\_ATTRIBUTES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(node, ast.Attribute) → isinstance(node.attr, str) → node.attr belongs to UNSAFE\_ATTRIBUTES.
    - Raise SyntaxError(formatted text Illegal rule {Platform.bold(code)}. Cannot use "{node.attr}").

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L1398) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1043) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1379)

<a id="op-ed0f962f180904"></a>
### Safe eval

`operation_workforce_payroll_utils_business_behavior_safe_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** code, eval\_globals, eval\_locals.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L1978) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1049) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1385)

<a id="op-2586767e98b200"></a>
### Throw error message

`operation_workforce_payroll_utils_business_behavior_throw_error_message`

**Inputs** row, error, title, description = no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- Set data from Platform.\_dict(mapping(“doctype” → row.parenttype, “name” → row.parent, “doclink” → get\_link\_to\_form(row.parenttype, row.parent), “row\_id” → row.idx, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in description → empty text.
- Set message from translated “Error while evaluating the {doctype} {doclink} at row {row\_id}. &lt;br&gt;&lt;br&gt; &lt;b&gt;Error:&lt;/b&gt; {error} &lt;br&gt;&lt;br&gt; &lt;b&gt;H …”.format(expanded names data).
- Call the validation error handler Platform.throw(message, title = title).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L2270) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1051) · [Declaration location](../../../current-decisions/workforce/evidence/locations-003.tsv#L2)

<a id="op-f7331f37741668"></a>
### Solve base for ctc

`operation_workforce_binding_workforce_payroll_utils_solve_base_for_ctc`

**Inputs** assignment, target\_ctc, tolerance = CTC\_SOLVER\_TOLERANCE.

**Declared result** tuple at tuple(float, float).

**Record and data access** read “Salary Structure” via get\_cached\_value.

**Explicit results** tuple(0.0, 0.0) · (solved or \_bisect\_base\_for\_ctc(ctc\_at, target\_ctc, scale, tolerance)) · tuple(base, ctc\_at(base)) · (solved or tuple(base, ctc\_at(base))).

**Local steps**

- Bind dependencies PERIODS\_PER\_YEAR.
- Set target\_ctc from flt(target\_ctc).
- If target\_ctc ≤ 0.
  - Return tuple(0.0, 0.0).
- Bind local operation ctc\_at for subsequent calls.
- Set frequency from Platform.get\_cached\_value(“Salary Structure”, assignment.salary\_structure, “payroll\_frequency”).
- Set scale from (target\_ctc ÷ PERIODS\_PER\_YEAR.get(frequency, 12)).
- Set tuple(low\_probe, high\_probe) from tuple((scale ÷ 2), scale).
- Set tuple(low\_ctc, high\_ctc) from tuple(ctc\_at(low\_probe), ctc\_at(high\_probe)).
- If high\_ctc &gt; low\_ctc.
  - Set solved from \_solve\_on\_line(ctc\_at, target\_ctc, tuple(low\_probe, low\_ctc), tuple(high\_probe, high\_ctc), …).
  - Return (solved or \_bisect\_base\_for\_ctc(ctc\_at, target\_ctc, scale, tolerance)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in solved → \_bisect\_base\_for\_ctc(ctc\_at, target\_ctc, scale, tolerance).
- Set tuple(base, achieved) from \_bisect\_base\_for\_ctc(ctc\_at, target\_ctc, scale, tolerance).
- If abs((achieved − high\_ctc)) ≤ tolerance.
  - Set base from flt(low\_probe, BASE\_PRECISION).
  - Return tuple(base, ctc\_at(base)).
- Set solved from \_solve\_on\_line(ctc\_at, target\_ctc, tuple((base ÷ 2), ctc\_at((base ÷ 2))), tuple(base, achieved), …).
- Return (solved or tuple(base, ctc\_at(base))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in solved → tuple(base, ctc\_at(base)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Salary Structure”, assignment.salary\_structure, “payroll\_frequency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L186) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L237) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L237)

<a id="op-c580213da868ef"></a>
### Solve base for ctc.ctc at

`operation_workforce_binding_workforce_payroll_utils_solve_base_for_ctc_ctc_at`

**Inputs** base.

**Declared result** float.

**Explicit results** flt(assignment.ctc).

**Local steps**

- Set assignment.base from flt(base, BASE\_PRECISION).
- Evaluate assignment.calculate\_ctc\_and\_gross().
- Return flt(assignment.ctc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L187) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L238) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L238)

<a id="op-7a36e3204ee5eb"></a>
### Solve on line

`operation_workforce_binding_workforce_payroll_utils_solve_on_line`

**Inputs** ctc\_at, target\_ctc, low, high, tolerance.

**Explicit results** no value · tuple(candidate, achieved).

**Local steps**

- Set tuple(tuple(low\_base, low\_ctc), tuple(high\_base, high\_ctc)) from tuple(low, high).
- Set slope from ((high\_ctc − low\_ctc) ÷ (high\_base − low\_base)).
- If slope ≤ 0.
  - Return no value.
- Set candidate from flt((low\_base + ((target\_ctc − low\_ctc) ÷ slope)), BASE\_PRECISION).
- If candidate &lt; 0.
  - Return no value.
- Set achieved from ctc\_at(candidate).
- If abs((achieved − target\_ctc)) ≤ tolerance.
  - Return tuple(candidate, achieved).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L188) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L239) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L239)

<a id="op-db7735d135b58e"></a>
### Bisect base for ctc

`operation_workforce_binding_workforce_payroll_utils_bisect_base_for_ctc`

**Inputs** ctc\_at, target\_ctc, scale, tolerance.

**Declared result** tuple at tuple(float, float).

**Explicit results** tuple(base, ctc\_at(base)).

**Local steps**

- Set tuple(low, high) from tuple(0.0, (scale or 1.0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in scale → 1.0.
- For each \_expansion in range(CTC\_SOLVER\_BRACKET\_EXPANSIONS).
  - If ctc\_at(high) ≥ target\_ctc.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set tuple(low, high) from tuple(high, (high × 2)).
- After normal loop exhaustion.
  - Set base from flt(high, BASE\_PRECISION).
  - Return tuple(base, ctc\_at(base)).
- For each \_iteration in range(CTC\_SOLVER\_MAX\_ITERATIONS).
  - If (high − low) ≤ tolerance.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set mid from ((low + high) ÷ 2).
  - If ctc\_at(mid) &lt; target\_ctc.
    - Set low from mid.
  - Otherwise.
    - Set high from mid.
- Set base from flt(high, BASE\_PRECISION).
- Return tuple(base, ctc\_at(base)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L183) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L234) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L234)

<a id="op-762eba5287b682"></a>
### Get payroll settings for payment days

`operation_workforce_payroll_utils_business_behavior_get_payroll_settings_for_payment_days`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Payroll Settings” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Payroll Settings”, no value, list(“payroll\_based\_on”, “consider\_unmarked\_attendance\_as”, “include\_holidays\_in\_total\_working\_days”, “consider\_marked\_attendance\_on\_holidays”), as\_d ….

**Local steps**

- Return Platform.get\_cached\_value(“Payroll Settings”, no value, list(“payroll\_based\_on”, “consider\_unmarked\_attendance\_as”, “include\_holidays\_in\_total\_working\_days”, “consider\_marked\_attendance\_on\_holidays”), as\_d ….

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Payroll Settings”, no value, list(“payroll\_based\_on”, “consider\_unmarked\_attendance\_as”, “include\_holidays\_in\_total\_working\_days”, “consider\_marked\_attendance\_on\_holidays”), as\_d ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0150.json#L2604) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L1047) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L1383)
