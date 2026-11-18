# Employment and attendance · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Unpaid expense claim

<a id="op-d84281698e700c"></a>
### Execute

`operation_workforce_human_resources_report_unpaid_expense_claim_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data) · tuple(columns, build\_grouped\_result(data, filters)).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_unclaimed\_expese\_claims(filters).
- If not data.
  - Return tuple(columns, data).
- If (not filters or not filters.get(“group\_by”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters → not filters.get(“group\_by”).
  - Return tuple(columns, data).
- Return tuple(columns, build\_grouped\_result(data, filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0094.json#L4435) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L114) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L463)

<a id="op-a76b37f0e48b56"></a>
### Get columns

`operation_workforce_human_resources_report_unpaid_expense_claim_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

**Local steps**

- Return list(mapping(“label” → translated “Employee”, “fieldname” → “employee”, “fieldtype” → “Link”, “options” → “Employee”, …), mapping(“label” → translated “Employee Name”, “fieldname” → “employee\_name”, “field ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0094.json#L4643) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L115) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L464)

<a id="op-c57c7a5922977b"></a>
### Build grouped result

`operation_workforce_human_resources_report_unpaid_expense_claim_business_behavior_build_grouped_result`

**Inputs** data, filters.

**Explicit results** result.

**Local steps**

- Set group\_by from filters.get(“group\_by”).
- Set group\_key\_field from scrub(group\_by).
- Set grouped from OrderedDict().
- Set group\_labels from OrderedDict().
- Set group\_totals from OrderedDict().
- For each row in data.
  - Set group\_key from row.get(group\_key\_field).
  - Evaluate grouped.setdefault(group\_key, list()).append(row).
  - If group\_key does not belong to group\_totals.
    - If group\_by equals “Employee”.
      - Set group\_labels at group\_key from formatted text {row.employee}: {row.employee\_name} when row.employee\_name, otherwise row.employee.
        - Value choice on row.employee\_name — true gives formatted text {row.employee}: {row.employee\_name}, false gives row.employee.
    - Otherwise.
      - Set group\_labels at group\_key from group\_key.
    - Set group\_totals at group\_key from Platform.\_dict(total\_sanctioned\_amount = 0, total\_amount\_reimbursed = 0, outstanding\_amt = 0).
  - Update group\_totals at group\_key.total\_sanctioned\_amount using + (row.total\_sanctioned\_amount or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.total\_sanctioned\_amount → 0.
  - Update group\_totals at group\_key.total\_amount\_reimbursed using + (row.total\_amount\_reimbursed or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.total\_amount\_reimbursed → 0.
  - Update group\_totals at group\_key.outstanding\_amt using + (row.outstanding\_amt or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.outstanding\_amt → 0.
- Set result from list().
- Set grand\_total from Platform.\_dict(total\_sanctioned\_amount = 0, total\_amount\_reimbursed = 0, outstanding\_amt = 0).
- For each tuple(key, rows) in grouped.items().
  - Set totals from group\_totals at key.
  - Update grand\_total.total\_sanctioned\_amount using + totals.total\_sanctioned\_amount.
  - Update grand\_total.total\_amount\_reimbursed using + totals.total\_amount\_reimbursed.
  - Update grand\_total.outstanding\_amt using + totals.outstanding\_amt.
  - Evaluate result.append(Platform.\_dict(employee = (group\_labels.get(key) or translated “Not Set”), total\_sanctioned\_amount = totals.total\_sanctioned\_amount, total\_amount\_reimbursed = totals.total\_amount\_reimbursed,  ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_labels.get(key) → translated “Not Set”.
  - For each row in rows.
    - Evaluate result.append(Platform.\_dict(row, indent = 1)).
- Evaluate result.append(Platform.\_dict(employee = translated “Total”, total\_sanctioned\_amount = grand\_total.total\_sanctioned\_amount, total\_amount\_reimbursed = grand\_total.total\_amount\_reimbursed, outstanding\_amt = g ….
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0094.json#L5685) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L113) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L462)

<a id="op-0d7023d5d9b055"></a>
### Get unclaimed expese claims

`operation_workforce_human_resources_report_unpaid_expense_claim_business_behavior_get_unclaimed_expese_claims`

**Inputs** filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set ec from Platform.qb.DocType(“Expense Claim”).
- Set emp from Platform.qb.DocType(“Employee”).
- Set ple from Platform.qb.DocType(“Payment Ledger Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If filters.get(“employee”).
  - Set query from query.where(ec.employee equals filters.get(“employee”)).
- If filters.get(“company”).
  - Set query from query.where(ec.company equals filters.get(“company”)).
- If filters.get(“department”).
  - Set query from query.where(ec.department equals filters.get(“department”)).
- If filters.get(“branch”).
  - Set query from query.where(emp.branch equals filters.get(“branch”)).
- If filters.get(“group\_by”) equals “Department”.
  - Set query from query.orderby(ec.department).
- Otherwise.
  - If filters.get(“group\_by”) equals “Branch”.
    - Set query from query.orderby(emp.branch).
  - Otherwise.
    - Set query from query.orderby(ec.employee).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L116) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L465)

## Service · Utils

<a id="op-df98da9b631e1a"></a>
### Set employee name

`operation_workforce_human_resources_utils_business_behavior_set_employee_name`

**Inputs** doc.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- If (doc.employee and not doc.employee\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.employee → not doc.employee\_name.
  - Set doc.employee\_name from Platform.db.get\_value(“Employee”, doc.employee, “employee\_name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L5555) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L163) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L512)

<a id="op-3551959852acc9"></a>
### Update employee work history

`operation_workforce_human_resources_utils_business_behavior_update_employee_work_history`

**Inputs** employee, details, date = no value, cancel = false.

**Explicit results** employee.

**Local steps**

- If not details.
  - Return employee.
- If (not employee.internal\_work\_history and not cancel).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not employee.internal\_work\_history → not cancel.
  - Evaluate employee.append(“internal\_work\_history”, mapping(“branch” → employee.branch, “designation” → employee.designation, “department” → employee.department, “from\_date” → employee.date\_of\_joining)).
- Set internal\_work\_history from mapping().
- For each item in details.
  - Set field from Platform.get\_meta(“Employee”).get\_field(item.fieldname).
  - If not field.
    - Continue with the next iteration or loop test.
  - Set new\_value from item.new when not cancel, otherwise item.current.
    - Value choice on not cancel — true gives item.new, false gives item.current.
  - Set new\_value from get\_formatted\_value(new\_value, field.fieldtype).
  - Evaluate setattr(employee, item.fieldname, new\_value).
  - If item.fieldname belongs to list(“department”, “designation”, “branch”).
    - Set internal\_work\_history at item.fieldname from item.new.
- If (internal\_work\_history and not cancel).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in internal\_work\_history → not cancel.
  - Set internal\_work\_history at “from\_date” from date.
  - Evaluate employee.append(“internal\_work\_history”, internal\_work\_history).
- If cancel.
  - Evaluate delete\_employee\_work\_history(details, employee, date).
- Evaluate update\_to\_date\_in\_work\_history(employee, cancel).
- Return employee.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L5677) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L167) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L516)

<a id="op-6973a20c78311f"></a>
### Get formatted value

`operation_workforce_human_resources_utils_business_behavior_get_formatted_value`

**Inputs** value, fieldtype.

**Explicit results** no value · value.

**Local steps**

- If not value.
  - Return no value.
- If fieldtype equals “Date”.
  - Set value from getdate(value).
- Otherwise.
  - If fieldtype equals “Datetime”.
    - Set value from get\_datetime(value).
  - Otherwise.
    - If fieldtype belongs to list(“Currency”, “Float”).
      - Set number\_format from (Platform.db.get\_default(“number\_format”) or “#,###.##”).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_default(“number\_format”) → “#,###.##”.
      - Set tuple(decimal\_str, comma\_str, \_number\_format\_precision) from get\_number\_format\_info(number\_format).
      - If (comma\_str equals “.” and decimal\_str equals “,”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in comma\_str equals “.” → decimal\_str equals “,”.
        - Set value from value.replace(“,”, “#$”).
        - Set value from value.replace(“.”, “,”).
        - Set value from value.replace(“#$”, “.”).
      - Set value from flt(value).
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L6337) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L142) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L491)

<a id="op-f3b999d8f80d51"></a>
### Delete employee work history

`operation_workforce_human_resources_utils_business_behavior_delete_employee_work_history`

**Inputs** details, employee, date.

**State and service calls** request delete on “Employee Internal Work History” · call save on employee.

**Local steps**

- Set filters from mapping().
- For each d in details.
  - For each history in employee.internal\_work\_history.
    - If (d.property equals “Department” and history.department equals d.new).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.property equals “Department” → history.department equals d.new.
      - Set department from d.new.
      - Set filters at “department” from department.
    - If (d.property equals “Designation” and history.designation equals d.new).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.property equals “Designation” → history.designation equals d.new.
      - Set designation from d.new.
      - Set filters at “designation” from designation.
    - If (d.property equals “Branch” and history.branch equals d.new).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.property equals “Branch” → history.branch equals d.new.
      - Set branch from d.new.
      - Set filters at “branch” from branch.
    - If (date and date equals history.from\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in date → date equals history.from\_date.
      - Set filters at “from\_date” from date.
- If filters.
  - Evaluate Platform.db.delete(“Employee Internal Work History”, filters).
  - Evaluate employee.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0095.json#L6793) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L132) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L481)

<a id="op-dca124759ed793"></a>
### Update to date in work history

`operation_workforce_human_resources_utils_business_behavior_update_to_date_in_work_history`

**Inputs** employee, cancel.

**Explicit results** no value.

**Local steps**

- If not employee.internal\_work\_history.
  - Return no value.
- For each tuple(idx, row) in enumerate(employee.internal\_work\_history).
  - If (not row.from\_date or idx equals 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.from\_date → idx equals 0.
    - Continue with the next iteration or loop test.
  - Set prev\_row from employee.internal\_work\_history at (idx − 1).
  - If not prev\_row.to\_date.
    - Set prev\_row.to\_date from add\_days(row.from\_date, negative 1).
- If cancel.
  - Set employee.internal\_work\_history at negative 1.to\_date from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L169) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L518)

<a id="op-2dd476531b6b70"></a>
### Get employee field property

`operation_workforce_human_resources_utils_business_behavior_get_employee_field_property`

**Inputs** employee, fieldname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Employee” via get\_doc.

**Explicit results** no value · mapping(“value” → value, “datatype” → field.fieldtype, “label” → field.label, “options” → field.options).

**Local steps**

- If not (employee and fieldname).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in employee → fieldname.
  - Return no value.
- Set field from Platform.get\_meta(“Employee”).get\_field(fieldname).
- If not field.
  - Return no value.
- Set doc from Platform.get\_doc(“Employee”, employee, check\_permission = true).
- Set value from doc.get(fieldname).
- If field.fieldtype equals “Date”.
  - Set value from formatdate(value).
- Otherwise.
  - If field.fieldtype equals “Datetime”.
    - Set value from format\_datetime(value).
- Return mapping(“value” → value, “datatype” → field.fieldtype, “label” → field.label, “options” → field.options).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L286) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L139) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L488)

<a id="op-22d07da7c5b0b3"></a>
### Validate dates

`operation_workforce_human_resources_utils_business_behavior_validate_dates`

**Inputs** doc, from\_date, to\_date, restrict\_future\_dates = true.

**Record and data access** read “Employee” via get\_value.

**Explicit failure paths** validation helper — translated “To date can not be less than from date” · validation helper — translated “Future dates not allowed” · validation helper — translated “From date can not be less than employee's joining date” · validation helper — translated “To date can not greater than employee's relieving date”.

**Local steps**

- Set tuple(date\_of\_joining, relieving\_date) from Platform.db.get\_value(“Employee”, doc.employee, list(“date\_of\_joining”, “relieving\_date”)).
- If getdate(from\_date) &gt; getdate(to\_date).
  - Call the validation error handler Platform.throw(translated “To date can not be less than from date”).
- Otherwise.
  - If (getdate(from\_date) &gt; getdate(nowdate()) and restrict\_future\_dates).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getdate(from\_date) &gt; getdate(nowdate()) → restrict\_future\_dates.
    - Call the validation error handler Platform.throw(translated “Future dates not allowed”).
  - Otherwise.
    - If (date\_of\_joining and getdate(from\_date) &lt; getdate(date\_of\_joining)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in date\_of\_joining → getdate(from\_date) &lt; getdate(date\_of\_joining).
      - Call the validation error handler Platform.throw(translated “From date can not be less than employee's joining date”).
    - Otherwise.
      - If (relieving\_date and getdate(to\_date) &gt; getdate(relieving\_date)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in relieving\_date → getdate(to\_date) &gt; getdate(relieving\_date).
        - Call the validation error handler Platform.throw(translated “To date can not greater than employee's relieving date”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L714) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L172) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L521)

<a id="op-ccae629101dbe3"></a>
### Validate overlap

`operation_workforce_human_resources_utils_business_behavior_validate_overlap`

**Inputs** doc, from\_date, to\_date, company = no value.

**Local steps**

- If not doc.name.
  - Set doc.name from (“New ” + doc.doctype).
- Set table from Platform.qb.DocType(doc.doctype).
- Set query from nested operand in the contract.qb.from\_(table).select(table.name).where(table.name differs from doc.name).
- Set condition from get\_doc\_condition(doc.doctype, table, doc.get(“employee”), from\_date, …).
- If condition is distinct from no value.
  - Set query from query.where(condition).
- Set overlap\_doc from query.run(as\_dict = true).
- If overlap\_doc.
  - If doc.get(“employee”).
    - Set exists\_for from doc.employee.
  - If company.
    - Set exists\_for from company.
  - Evaluate throw\_overlap\_error(doc, exists\_for, overlap\_doc at 0.name, from\_date, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L1234) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L175) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L524)

<a id="op-a0e66e9f348a9f"></a>
### Get doc condition

`operation_workforce_human_resources_utils_business_behavior_get_record_condition`

**Inputs** doctype, table, employee, from\_date, to\_date, company.

**Explicit results** ((table.employee equals employee bitwise and table.docstatus &lt; 2) bitwise and ((table.work\_from\_date.between(from\_date, to\_date) bitwise or table.work\_end\_date.between(from\_date, to\_date)) bitwise or (tabl … · (table.company equals company bitwise and ((table.from\_date.between(from\_date, to\_date) bitwise or table.to\_date.between(from\_date, to\_date)) bitwise or (table.from\_date &lt; from\_date bitwise and table.to\_da ….

**Local steps**

- If doctype equals “Compensatory Leave Request”.
  - Return ((table.employee equals employee bitwise and table.docstatus &lt; 2) bitwise and ((table.work\_from\_date.between(from\_date, to\_date) bitwise or table.work\_end\_date.between(from\_date, to\_date)) bitwise or (tabl ….
- Otherwise.
  - If doctype equals “Leave Period”.
    - Return (table.company equals company bitwise and ((table.from\_date.between(from\_date, to\_date) bitwise or table.to\_date.between(from\_date, to\_date)) bitwise or (table.from\_date &lt; from\_date bitwise and table.to\_da ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L1759) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L151) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L500)

<a id="op-9461b642a246a6"></a>
### Throw overlap error

`operation_workforce_human_resources_utils_business_behavior_throw_overlap_error`

**Inputs** doc, exists\_for, overlap\_doc, from\_date, to\_date.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set msg from ((translated “A {0} exists between {1} and {2} (”.format(doc.doctype, formatdate(from\_date), formatdate(to\_date)) + formatted text  &lt;b&gt;&lt;a href="/app/Form/{doc.doctype}/{overlap\_doc}"&gt;{overlap\_doc}&lt;/a&gt;&lt;/b&gt;) ….
- Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L2174) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L166) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L515)

<a id="op-a516d690bfff8b"></a>
### Validate duplicate exemption for payroll period

`operation_workforce_human_resources_utils_business_behavior_validate_duplicate_exemption_for_payroll_period`

**Inputs** doctype, docname, payroll\_period, employee.

**Record and data access** read doctype via exists.

**Explicit failure paths** validation helper with DuplicateDeclarationError — translated “{0} already exists for employee {1} and period {2}”.format(doctype, employee, payroll\_period).

**Local steps**

- Set existing\_record from Platform.db.exists(doctype, mapping(“payroll\_period” → payroll\_period, “employee” → employee, “docstatus” → list(“&lt;”, 2), “name” → list(“!=”, docname))).
- If existing\_record.
  - Call the validation error handler Platform.throw(translated “{0} already exists for employee {1} and period {2}”.format(doctype, employee, payroll\_period), DuplicateDeclarationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L2435) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L173) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L522)

<a id="op-0e9c4b2d752a57"></a>
### Validate tax declaration

`operation_workforce_human_resources_utils_business_behavior_validate_tax_declaration`

**Inputs** declarations.

**Explicit failure paths** validation helper — translated “More than one selection for {0} not allowed”.format(d.exemption\_sub\_category).

**Local steps**

- Set subcategories from list().
- For each d in declarations.
  - If d.exemption\_sub\_category belongs to subcategories.
    - Call the validation error handler Platform.throw(translated “More than one selection for {0} not allowed”.format(d.exemption\_sub\_category)).
  - Evaluate subcategories.append(d.exemption\_sub\_category).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L2685) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L176) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L525)

<a id="op-2074f8c399bea6"></a>
### Get total exemption amount

`operation_workforce_human_resources_utils_business_behavior_get_total_exemption_amount`

**Inputs** declarations.

**Record and data access** read “Employee Tax Exemption Category” via get\_value.

**Explicit results** total\_exemption\_amount.

**Local steps**

- Set exemptions from Platform.\_dict().
- For each d in declarations.
  - Evaluate exemptions.setdefault(d.exemption\_category, Platform.\_dict()).
  - Set category\_max\_amount from exemptions.get(d.exemption\_category).max\_amount.
  - If not category\_max\_amount.
    - Set category\_max\_amount from Platform.db.get\_value(“Employee Tax Exemption Category”, d.exemption\_category, “max\_amount”).
    - Set exemptions.get(d.exemption\_category).max\_amount from category\_max\_amount.
  - Set sub\_category\_exemption\_amount from d.max\_amount when (d.max\_amount and flt(d.amount) &gt; flt(d.max\_amount)), otherwise d.amount.
    - Value choice on (d.max\_amount and flt(d.amount) &gt; flt(d.max\_amount)) — true gives d.max\_amount, false gives d.amount.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.max\_amount → flt(d.amount) &gt; flt(d.max\_amount).
  - Evaluate exemptions.get(d.exemption\_category).setdefault(“total\_exemption\_amount”, 0.0).
  - Update exemptions.get(d.exemption\_category).total\_exemption\_amount using + flt(sub\_category\_exemption\_amount).
  - If (category\_max\_amount and exemptions.get(d.exemption\_category).total\_exemption\_amount &gt; category\_max\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in category\_max\_amount → exemptions.get(d.exemption\_category).total\_exemption\_amount &gt; category\_max\_amount.
    - Set exemptions.get(d.exemption\_category).total\_exemption\_amount from category\_max\_amount.
- Set total\_exemption\_amount from sum(list of flt(d.total\_exemption\_amount) for d drawn from exemptions.values()).
  - Draw d from exemptions.values().
- Return total\_exemption\_amount.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L2863) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L157) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L506)

<a id="op-e28cdff3d284d6"></a>
### Get leave period

`operation_workforce_human_resources_utils_business_behavior_get_leave_period`

**Inputs** from\_date, to\_date, company.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** leave\_period.

**Local steps**

- Set LeavePeriod from Platform.qb.DocType(“Leave Period”).
- Set leave\_period from nested operand in the contract(nested operand in the contract).select(LeavePeriod.name, LeavePeriod.from\_date, LeavePeriod.to\_date).where(((nested operand in the contract.company equals company bitwise and ….
- If leave\_period.
  - Return leave\_period.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L3469) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L147) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L496)

<a id="op-857a0504c1a96d"></a>
### Generate leave encashment

`operation_workforce_human_resources_utils_business_behavior_generate_leave_encashment`

**Inputs** no declared parameters.

**Record and data access** read “HR Settings” via get\_single\_value · read “Leave Type” via get\_all · read “Leave Allocation” via get\_all.

**Local steps**

- Bind dependencies create\_leave\_encashment.
- If Platform.db.get\_single\_value(“HR Settings”, “auto\_leave\_encashment”).
  - Set leave\_type from Platform.get\_all(“Leave Type”, filters = mapping(“allow\_encashment” → 1), fields = list(“name”)).
  - Set leave\_type from list of l at “name” for l drawn from leave\_type.
    - Draw l from leave\_type.
  - Set leave\_allocation from Platform.get\_all(“Leave Allocation”, filters = list(list(“to\_date”, “=”, add\_days(getdate(), negative 1)), list(“leave\_type”, “in”, leave\_type)), fields = list(“employee”, “leave\_period”, “leave\_type”, “to ….
  - Evaluate create\_leave\_encashment(leave\_allocation = leave\_allocation).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “auto\_leave\_encashment”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L3877) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L133) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L482)

<a id="op-defcbc4c42a05e"></a>
### Allocate earned leaves

`operation_workforce_human_resources_utils_business_behavior_allocate_earned_leaves`

**Inputs** no declared parameters.

**Record and data access** read “Employee” via get\_value.

**Local steps**

- Set e\_leave\_types from get\_earned\_leaves().
- Set today from (Platform.flags.current\_date or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.current\_date → getdate().
- Set failed\_allocations from list().
- For each e\_leave\_type in e\_leave\_types.
  - Set leave\_allocations from get\_leave\_allocations(today, e\_leave\_type.name).
  - For each allocation in leave\_allocations.
    - If allocation.earned\_leave\_schedule\_exists.
      - Set tuple(allocation\_date, earned\_leaves) from (get\_upcoming\_earned\_leave\_from\_schedule(allocation.name, today) or tuple(no value, no value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_upcoming\_earned\_leave\_from\_schedule(allocation.name, today) → tuple(no value, no value).
      - Set annual\_allocation from get\_annual\_allocation\_from\_policy(allocation, e\_leave\_type).
    - Otherwise.
      - Set date\_of\_joining from Platform.db.get\_value(“Employee”, allocation.employee, “date\_of\_joining”).
      - Set allocation\_date from get\_expected\_allocation\_date\_for\_period(e\_leave\_type.earned\_leave\_frequency, e\_leave\_type.allocate\_on\_day, today, date\_of\_joining, effective\_from = no value).
      - Set annual\_allocation from get\_annual\_allocation\_from\_policy(allocation, e\_leave\_type).
      - Set earned\_leaves from calculate\_upcoming\_earned\_leave(allocation, e\_leave\_type, date\_of\_joining).
    - If (not allocation\_date or allocation\_date differs from today).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not allocation\_date → allocation\_date differs from today.
      - Continue with the next iteration or loop test.
    - Attempt the following.
      - Evaluate update\_previous\_leave\_allocation(allocation, annual\_allocation, e\_leave\_type, earned\_leaves, …).
    - On failure (Exception) bound to e.
      - Evaluate log\_allocation\_error(allocation.name, e).
      - Evaluate failed\_allocations.append(allocation.name).
- If failed\_allocations.
  - Evaluate send\_email\_for\_failed\_allocations(failed\_allocations).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L4289) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L125) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L474)

<a id="op-8aefb3fb49d700"></a>
### Get upcoming earned leave from schedule

`operation_workforce_human_resources_utils_business_behavior_get_upcoming_earned_leave_from_schedule`

**Inputs** allocation\_name, today.

**Record and data access** read “Earned Leave Schedule” via get\_value.

**Explicit results** Platform.db.get\_value(“Earned Leave Schedule”, mapping(“parent” → allocation\_name, “attempted” → 0, “allocation\_date” → today), list(“allocation\_date”, “number\_of\_leaves”)).

**Local steps**

- Return Platform.db.get\_value(“Earned Leave Schedule”, mapping(“parent” → allocation\_name, “attempted” → 0, “allocation\_date” → today), list(“allocation\_date”, “number\_of\_leaves”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L4928) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L158) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L507)

<a id="op-886598a2fd93bc"></a>
### Get annual allocation from policy

`operation_workforce_human_resources_utils_business_behavior_get_annual_allocation_from_policy`

**Inputs** allocation, e\_leave\_type.

**Record and data access** read “Leave Policy Detail” via get\_value.

**Explicit results** Platform.db.get\_value(“Leave Policy Detail”, filters = mapping(“parent” → allocation.leave\_policy, “leave\_type” → e\_leave\_type.name), fieldname = list(“annual\_allocation”)).

**Local steps**

- Return Platform.db.get\_value(“Leave Policy Detail”, filters = mapping(“parent” → allocation.leave\_policy, “leave\_type” → e\_leave\_type.name), fieldname = list(“annual\_allocation”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L5074) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L134) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L483)

<a id="op-20f91a047e298f"></a>
### Calculate upcoming earned leave

`operation_workforce_human_resources_utils_business_behavior_calculate_upcoming_earned_leave`

**Inputs** allocation, e\_leave\_type, date\_of\_joining.

**Explicit results** earned\_leave.

**Local steps**

- Set annual\_allocation from get\_annual\_allocation\_from\_policy(allocation, e\_leave\_type).
- Set earned\_leave from get\_monthly\_earned\_leave(date\_of\_joining, annual\_allocation, e\_leave\_type.earned\_leave\_frequency, e\_leave\_type.rounding).
- Return earned\_leave.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0096.json#L5216) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L129) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L478)

<a id="op-44e574f4e10522"></a>
### Update previous leave allocation

`operation_workforce_human_resources_utils_business_behavior_update_previous_leave_allocation`

**Inputs** allocation, annual\_allocation, e\_leave\_type, earned\_leaves, today, allocated\_via = “Scheduler”.

**Record and data access** resolve a document from “Leave Allocation” via get\_doc.

**State and service calls** call db\_set on allocation.

**Explicit failure paths** validation helper with OverAllocationError — translated “Allocation was skipped due to maximum leave allocation limit set in leave type. Please increase the limit an …”.

**Local steps**

- Set allocation from Platform.get\_doc(“Leave Allocation”, allocation.name).
- Set precision from allocation.precision(“total\_leaves\_allocated”).
- Set annual\_allocation from flt(annual\_allocation, precision).
- Set earned\_leaves from flt(earned\_leaves, precision).
- If (earned\_leaves &gt; 0 and e\_leave\_type.earned\_leave\_frequency differs from “Yearly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in earned\_leaves &gt; 0 → e\_leave\_type.earned\_leave\_frequency differs from “Yearly”.
  - Set leaves\_left\_in\_annual\_quota from max(flt((annual\_allocation − allocation.get\_existing\_leave\_count()), precision), 0).
  - Set earned\_leaves from min(earned\_leaves, leaves\_left\_in\_annual\_quota).
- If (earned\_leaves &gt; 0 and e\_leave\_type.max\_leaves\_allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in earned\_leaves &gt; 0 → e\_leave\_type.max\_leaves\_allowed.
  - Set leaves\_quota from flt((e\_leave\_type.max\_leaves\_allowed − allocation.total\_leaves\_allocated), precision).
  - If leaves\_quota ≤ 0.
    - Call the validation error handler Platform.throw(translated “Allocation was skipped due to maximum leave allocation limit set in leave type. Please increase the limit an …”, OverAllocationError).
  - Otherwise.
    - If leaves\_quota &lt; earned\_leaves.
      - Set earned\_leaves from leaves\_quota.
- If earned\_leaves.
  - Evaluate allocation.db\_set(“total\_leaves\_allocated”, (earned\_leaves + allocation.total\_leaves\_allocated), update\_modified = false).
  - Evaluate create\_additional\_leave\_ledger\_entry(allocation, earned\_leaves, today).
- Set earned\_leave\_schedule from qb.DocType(“Earned Leave Schedule”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(earned\_leave\_schedule.failed, 0).set(earned\_leave\_schedule.failure\_reason, empty text).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0002.json#L86) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L168) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L517)
