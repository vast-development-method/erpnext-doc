# Employment and attendance · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Leave encashment

[Record definition](../../../../data/record-types/leave_encashment.json)

<a id="op-d6da9ebc7942e1"></a>
### Leave Encashment.set encashed leaves in allocation

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_encashed_leaves_in_allocation`

**Inputs** self.

**Record and data access** read “Leave Allocation” via get\_value.

**State and service calls** request set\_value on “Leave Allocation”.

**Local steps**

- Evaluate Platform.db.set\_value(“Leave Allocation”, self.leave\_allocation, “total\_leaves\_encashed”, (Platform.db.get\_value(“Leave Allocation”, self.leave\_allocation, “total\_leaves\_encashed”) + self.encashment\_days)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L1485) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1301) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1277)

<a id="op-f1b7758e5910ea"></a>
### Leave Encashment.set encashment amount

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_encashment_amount`

**Inputs** self.

**Record and data access** read “Salary Structure Assignment” via get\_value · read “Salary Structure” via get\_value.

**Local steps**

- If not hasattr(self, “\_salary\_structure”).
  - Evaluate self.set\_salary\_structure().
- Set per\_day\_encashment from Platform.get\_value(“Salary Structure Assignment”, filters = mapping(“employee” → self.employee, “salary\_structure” → self.\_salary\_structure, “docstatus” → 1, “from\_date” → list(“&lt;=”, self.encashment\_date)) ….
- If not per\_day\_encashment.
  - Set per\_day\_encashment from Platform.db.get\_value(“Salary Structure”, self.\_salary\_structure, “leave\_encashment\_amount\_per\_day”).
- Set per\_day\_encashment from (per\_day\_encashment or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in per\_day\_encashment → 0.
- Set self.encashment\_amount from (self.encashment\_days × per\_day\_encashment) when per\_day\_encashment &gt; 0, otherwise 0.
  - Value choice on per\_day\_encashment &gt; 0 — true gives (self.encashment\_days × per\_day\_encashment), false gives 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set salary structure](operations-029.md#op-61647d3fcb2f99).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L1623) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1302) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1278)

<a id="op-d8ed85a45200b1"></a>
### Leave Encashment.set status

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_status`

**Inputs** self, update = false.

**State and service calls** call db\_set on self.

**Local steps**

- Set precision from self.precision(“paid\_amount”).
- Set status from no value.
- If self.docstatus equals 0.
  - Set status from “Draft”.
- Otherwise.
  - If self.docstatus equals 1.
    - If flt(self.encashment\_amount) &gt; flt(self.paid\_amount, precision).
      - Set status from “Unpaid”.
    - Otherwise.
      - Set status from “Paid”.
  - Otherwise.
    - If self.docstatus equals 2.
      - Set status from “Cancelled”.
- If update.
  - Evaluate self.db\_set(“status”, status).
  - Evaluate self.notify\_update().
- Otherwise.
  - Set self.status from status.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L2009) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1306) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1282)

<a id="op-eadf6c94feec76"></a>
### Leave Encashment.get leave allocation

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_get_leave_allocation`

**Inputs** self.

**Explicit results** leave\_allocation at 0 when leave\_allocation, otherwise no value.

**Local steps**

- Set date from (self.encashment\_date or getdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.encashment\_date → getdate().
- Set LeaveAllocation from Platform.qb.DocType(“Leave Allocation”).
- Set leave\_allocation from nested operand in the contract(nested operand in the contract).select(LeaveAllocation.name, LeaveAllocation.from\_date, LeaveAllocation.to\_date, LeaveAllocation.total\_leaves\_allocated, …).where(((((nested o ….
- Return leave\_allocation at 0 when leave\_allocation, otherwise no value.
  - Value choice on leave\_allocation — true gives leave\_allocation at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L2365) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1295) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1271)

<a id="op-247628f04d0ed0"></a>
### Leave Encashment.create leave ledger entry

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_create_leave_ledger_entry`

**Inputs** self, submit = true.

**Record and data access** read “Leave Type” via get\_value.

**Explicit results** no value.

**Local steps**

- Set args from Platform.\_dict(leaves = (self.encashment\_days × negative 1), from\_date = self.encashment\_date, to\_date = self.encashment\_date, is\_carry\_forward = 0).
- Evaluate create\_leave\_ledger\_entry(self, args, submit).
- Set leave\_allocation from self.get\_leave\_allocation().
- If not leave\_allocation.
  - Return no value.
- Set to\_date from leave\_allocation.get(“to\_date”).
- Set can\_expire from not Platform.db.get\_value(“Leave Type”, self.leave\_type, “is\_carry\_forward”).
- If (to\_date &lt; getdate() and can\_expire).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_date &lt; getdate() → can\_expire.
  - Set args from Platform.\_dict(leaves = self.encashment\_days, from\_date = to\_date, to\_date = to\_date, is\_carry\_forward = 0).
  - Evaluate create\_leave\_ledger\_entry(self, args, submit).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get leave allocation](operations-030.md#op-eadf6c94feec76).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L2739) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1292) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1268)

<a id="op-99f156d03ed1cf"></a>
### Leave Encashment.set total advance paid

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_set_total_advance_paid`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “Row {0}# Paid Amount cannot be greater than Encashment amount”.

**Local steps**

- Bind dependencies Abs, Sum.
- Set aple from Platform.qb.DocType(“Advance Payment Ledger Entry”).
- Set paid\_amount from (nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).run(as\_dict = true) at 0.paid\_amount or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op … → 0.
- If flt(paid\_amount) &gt; self.encashment\_amount.
  - Call the validation error handler Platform.throw(translated “Row {0}# Paid Amount cannot be greater than Encashment amount”).
- Evaluate self.db\_set(“paid\_amount”, paid\_amount).
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-030.md#op-d8ed85a45200b1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L3168) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1307) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1283)

<a id="op-f00cc8beb11f8f"></a>
### Leave Encashment.create gl entries

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_create_general_ledger_entries`

**Inputs** self, cancel = false.

**Local steps**

- Set gl\_entries from self.get\_gl\_entries().
- Evaluate make\_gl\_entries(gl\_entries, cancel).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries](operations-030.md#op-aea09d1a5e59a2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L3650) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1291) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1267)

<a id="op-aea09d1a5e59a2"></a>
### Leave Encashment.get gl entries

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_get_general_ledger_entries`

**Inputs** self.

**Explicit results** gl\_entry.

**Local steps**

- Set gl\_entry from list().
- Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → self.payable\_account, “credit” → self.encashment\_amount, “credit\_in\_account\_currency” → self.encashment\_amount, “against” → self.expense\_account, …), it ….
- Evaluate gl\_entry.append(self.get\_gl\_dict(mapping(“account” → self.expense\_account, “debit” → self.encashment\_amount, “debit\_in\_account\_currency” → self.encashment\_amount, “against” → self.payable\_account, …), item = self)).
- Return gl\_entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L3743) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1294) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1270)

<a id="op-0d4eff31084215"></a>
### Leave Encashment.on discard

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_leave_encashment_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L4175) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1298) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1274)

<a id="op-25ba22cddd00ac"></a>
### Create leave encashment

`operation_workforce_human_resources_record_definitions_leave_encashment_business_behavior_create_leave_encashment`

**Inputs** leave\_allocation.

**Record and data access** resolve a document from dict(doctype = “Leave Encashment”, leave\_period = allocation.leave\_period, employee = allocation.employee, leave\_type = allocation.leave\_type, …) via get\_doc.

**State and service calls** call insert on leave\_encashment.

**Local steps**

- For each allocation in leave\_allocation.
  - If not get\_assigned\_salary\_structure(allocation.employee, allocation.to\_date).
    - Continue with the next iteration or loop test.
  - Set leave\_encashment from Platform.get\_doc(dict(doctype = “Leave Encashment”, leave\_period = allocation.leave\_period, employee = allocation.employee, leave\_type = allocation.leave\_type, …)).
  - Evaluate leave\_encashment.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0059.json#L4238) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1288) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1264)

## Report · Leave ledger

<a id="op-5c5fe37b38192c"></a>
### Execute

`operation_workforce_human_resources_report_leave_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Declared result** tuple.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0086.json#L4452) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L10) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L359)

<a id="op-c9674b20f54d53"></a>
### Get columns

`operation_workforce_human_resources_report_leave_ledger_business_behavior_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Leave Ledger Entry”, “fieldname” → “leave\_ledger\_entry”, “fieldtype” → “Link”, “options” → “Leave Ledger Entry”, …), mapping(“label” → translated “Employee”, “fieldname”  ….

**Local steps**

- Return list(mapping(“label” → translated “Leave Ledger Entry”, “fieldname” → “leave\_ledger\_entry”, “fieldtype” → “Link”, “options” → “Leave Ledger Entry”, …), mapping(“label” → translated “Employee”, “fieldname”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0086.json#L4558) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L11) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L360)

<a id="op-513873f2e24aa2"></a>
### Get data

`operation_workforce_human_resources_report_leave_ledger_business_behavior_get_data`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** result.

**Local steps**

- Set Employee from Platform.qb.DocType(“Employee”).
- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set tuple(from\_date, to\_date) from tuple(filters.get(“from\_date”), filters.get(“to\_date”)).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.employee equals nested operand in the contract.name).select(Ledger.name.as\_(“leave\_ledger\_entry”), Ledger.em ….
- For each field in tuple(“employee”, “leave\_type”, “company”, “transaction\_type”, …).
  - If filters.get(field).
    - Set query from query.where(Ledger at field equals filters.get(field)).
- For each field in tuple(“department”, “status”).
  - If filters.get(field).
    - Set query from query.where(Employee at field equals filters.get(field)).
- Set query from query.orderby(Ledger.employee, Ledger.leave\_type, Ledger.from\_date).
- Set result from query.run(as\_dict = true).
- Set result from add\_total\_row(result, filters).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0086.json#L6058) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L12) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L361)

<a id="op-7e33dfd09ee7e3"></a>
### Add total row

`operation_workforce_human_resources_report_leave_ledger_business_behavior_add_total_row`

**Inputs** result, filters.

**Declared result** list at dict.

**Explicit results** result.

**Local steps**

- Set add\_total\_row from false.
- Set leave\_type from filters.get(“leave\_type”).
- If (filters.get(“employee”) and filters.get(“leave\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“employee”) → filters.get(“leave\_type”).
  - Set add\_total\_row from true.
- If not add\_total\_row.
  - If not filters.get(“employee”).
    - Set employees\_from\_result from list(set(list of row.employee for row drawn from result)).
      - Draw row from result.
    - <a id="op-7e33dfd09ee7e3-guard-12"></a>If len(employees\_from\_result) differs from 1.
      - Return result.
  - Set leave\_types\_from\_result from list(set(list of row.leave\_type for row drawn from result)).
    - Draw row from result.
  - If len(leave\_types\_from\_result) equals 1.
    - Set leave\_type from leave\_types\_from\_result at 0.
    - Set add\_total\_row from true.
- If not add\_total\_row.
  - Return result.
- Set total\_row from Platform.\_dict(mapping(“employee” → translated “Total Leaves ({0})”.format(leave\_type))).
- Set total\_row at “leaves” from sum(generator of (row.get(“leaves”) or 0) for row drawn from result).
  - Draw row from result.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“leaves”) → 0.
- Evaluate result.append(total\_row).
- Return result.

**Derived branch illustrations**

- At the comparison len(employees\_from\_result) differs from 1, length of employees\_from\_result = 2 selects the branch that returns result. With length of employees\_from\_result = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7e33dfd09ee7e3-guard-12)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0087.json#L6) · [Binding](../../../current-decisions/workforce/bindings-002.tsv#L9) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L358)

## Record · Leave ledger entry

[Record definition](../../../../data/record-types/leave_ledger_entry.json)

<a id="op-45918843d02a41"></a>
### Leave Ledger Entry.validate

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_leave_ledger_entry_validate`

**Inputs** self.

**Explicit failure paths** validation helper with InvalidLeaveLedgerEntry — translated “Leave Ledger Entry's To date needs to be after From date. Currently, From Date is {0} and To Date is {1}”.format(Platform.bold(formatdate(self.from\_date)), Platform.bold(formatdate(self.to\_date))).

**Local steps**

- If getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “Leave Ledger Entry's To date needs to be after From date. Currently, From Date is {0} and To Date is {1}”.format(Platform.bold(formatdate(self.from\_date)), Platform.bold(formatda ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L4509) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1332) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1308)

<a id="op-5f31eee14671e0"></a>
### Leave Ledger Entry.on cancel

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_leave_ledger_entry_on_cancel`

**Inputs** self.

**State and service calls** request set\_value on “Leave Allocation”.

**Explicit failure paths** validation helper — translated “Only expired allocation can be cancelled”.

**Local steps**

- If self.is\_expired.
  - Evaluate Platform.db.set\_value(“Leave Allocation”, self.transaction\_name, “expired”, 0).
- Otherwise.
  - If self.transaction\_type differs from “Leave Adjustment”.
    - Call the validation error handler Platform.throw(translated “Only expired allocation can be cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L4757) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1331) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1307)

<a id="op-f579c11e6566ce"></a>
### Validate leave allocation against leave application

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_validate_leave_allocation_against_leave_application`

**Inputs** ledger.

**Explicit failure paths** validation helper — translated “Leave allocation {0} is linked with the Leave Application {1}”.format(ledger.transaction\_name, “, ”.join(generator of get\_link\_to\_form(“Leave Application”, application) for application drawn fr ….

**Local steps**

- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set leave\_application\_records from nested operand in the contract(nested operand in the contract).select(Ledger.transaction\_name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operan ….
- If leave\_application\_records.
  - Call the validation error handler Platform.throw(translated “Leave allocation {0} is linked with the Leave Application {1}”.format(ledger.transaction\_name, “, ”.join(generator of get\_link\_to\_form(“Leave Application”, application) for appli ….
    - Draw application from leave\_application\_records.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L4927) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1335) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1311)

<a id="op-5d991f68101afb"></a>
### Create leave ledger entry

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_create_leave_ledger_entry`

**Inputs** ref\_doc, args, submit = true.

**Record and data access** resolve a document from ledger via get\_doc.

**State and service calls** call submit on doc.

**Local steps**

- Set ledger from Platform.\_dict(doctype = “Leave Ledger Entry”, employee = ref\_doc.employee, employee\_name = ref\_doc.employee\_name, leave\_type = ref\_doc.leave\_type, …).
- Evaluate ledger.update(args).
- If submit.
  - Set doc from Platform.get\_doc(ledger).
  - Set doc.flags.ignore\_permissions from 1.
  - Evaluate doc.submit().
- Otherwise.
  - Evaluate delete\_ledger\_entry(ledger).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L5350) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1325) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1301)

<a id="op-6ca6c04519413f"></a>
### Delete ledger entry

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_delete_ledger_entry`

**Inputs** ledger.

**Local steps**

- If ledger.transaction\_type equals “Leave Allocation”.
  - Evaluate validate\_leave\_allocation\_against\_leave\_application(ledger).
- Set expired\_entry from get\_previous\_expiry\_ledger\_entry(ledger).
- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((Ledger.transaction\_name equals ledger.transaction\_name bitwise or Ledger.name equals expired\_entry)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L5656) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1326) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1302)

<a id="op-aa25fa53f20308"></a>
### Get previous expiry ledger entry

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_get_previous_expiry_ledger_entry`

**Inputs** ledger.

**Record and data access** read “Leave Ledger Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Leave Ledger Entry”, filters = mapping(“creation” → tuple(“like”, (creation\_date + “%”)), “employee” → ledger.employee, “leave\_type” → ledger.leave\_type, “is\_expired” → 1, …), fieldn ….

**Local steps**

- Set creation\_date from Platform.db.get\_value(“Leave Ledger Entry”, filters = mapping(“transaction\_name” → ledger.transaction\_name, “is\_expired” → 0, “transaction\_type” → “Leave Allocation”), fieldname = list(“creation”)).
- Set creation\_date from creation\_date.strftime(DATE\_FORMAT) when creation\_date, otherwise empty text.
  - Value choice on creation\_date — true gives creation\_date.strftime(DATE\_FORMAT), false gives empty text.
- Return Platform.db.get\_value(“Leave Ledger Entry”, filters = mapping(“creation” → tuple(“like”, (creation\_date + “%”)), “employee” → ledger.employee, “leave\_type” → ledger.leave\_type, “is\_expired” → 1, …), fieldn ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L5916) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1329) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1305)

<a id="op-126bec167e460b"></a>
### Process expired allocation

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_process_expired_allocation`

**Inputs** no declared parameters.

**Record and data access** read “Leave Type” via get\_values.

**Local steps**

- Set leave\_type\_records from Platform.db.get\_values(“Leave Type”, filters = mapping(“expire\_carry\_forwarded\_leaves\_after\_days” → tuple(“&gt;”, 0)), fieldname = list(“name”)).
- Set leave\_type from (list of record at 0 for record drawn from leave\_type\_records or list(empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of record at 0 for record drawn from leave\_type\_records → list(empty text).
  - Draw record from leave\_type\_records.
- Set Ledger from Platform.qb.DocType(“Leave Ledger Entry”).as\_(“l”).
- Set InnerLedger from Platform.qb.DocType(“Leave Ledger Entry”).
- Set inner\_query from nested operand in the contract.qb.from\_(InnerLedger).select(InnerLedger.name).where(((((nested operand in the contract.transaction\_name equals nested operand in the contract.transaction\_name bitwise and ne ….
- Set expire\_allocation from nested operand in the contract(nested operand in the contract).select(Ledger.leaves, Ledger.to\_date, Ledger.from\_date, Ledger.employee, …).where(((nested operand in the contract.negate() bitwise and nested ….
- If expire\_allocation.
  - Evaluate create\_expiry\_ledger\_entry(expire\_allocation).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L6294) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1334) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1310)

<a id="op-2a2112564505f2"></a>
### Create expiry ledger entry

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_create_expiry_ledger_entry`

**Inputs** allocations.

**Local steps**

- For each allocation in allocations.
  - If allocation.is\_carry\_forward.
    - Evaluate expire\_carried\_forward\_allocation(allocation).
  - Otherwise.
    - Evaluate expire\_allocation(allocation).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L7091) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1324) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1300)

<a id="op-a66f4c3bcc6eeb"></a>
### Get remaining leaves

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_get_remaining_leaves`

**Inputs** allocation.

**Record and data access** read “Leave Ledger Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Leave Ledger Entry”, filters = mapping(“employee” → allocation.employee, “leave\_type” → allocation.leave\_type, “to\_date” → tuple(“&lt;=”, allocation.to\_date), “docstatus” → 1), fieldnam ….

**Local steps**

- Return Platform.db.get\_value(“Leave Ledger Entry”, filters = mapping(“employee” → allocation.employee, “leave\_type” → allocation.leave\_type, “to\_date” → tuple(“&lt;=”, allocation.to\_date), “docstatus” → 1), fieldnam ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0060.json#L7194) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1330) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1306)

<a id="op-1319d14e0598b4"></a>
### Expire allocation

`operation_workforce_human_resources_record_definitions_leave_ledger_entry_business_behavior_expire_allocation`

**Inputs** allocation, expiry\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Leave Allocation” via get\_doc.

**State and service calls** request set\_value on “Leave Allocation”.

**Explicit results** no value.

**Local steps**

- Bind dependencies json.
- If isinstance(allocation, str).
  - Set allocation from json.loads(allocation).
  - Set allocation from Platform.get\_doc(“Leave Allocation”, allocation at “name”).
- If getattr(allocation, “docstatus”, 0) equals 2.
  - Return no value.
- Evaluate Platform.has\_permission(“Leave Allocation”, “write”, allocation.name, throw = true).
- Set leaves from get\_remaining\_leaves(allocation).
- Set expiry\_date from expiry\_date when expiry\_date, otherwise allocation.to\_date.
  - Value choice on expiry\_date — true gives expiry\_date, false gives allocation.to\_date.
- If leaves.
  - Set args from dict(leaves = (flt(leaves) × negative 1), transaction\_name = allocation.name, transaction\_type = “Leave Allocation”, from\_date = expiry\_date, …).
  - Evaluate create\_leave\_ledger\_entry(allocation, args).
- Evaluate Platform.db.set\_value(“Leave Allocation”, allocation.name, “expired”, 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(allocation, “docstatus”, 0) · effective access from Platform.has\_permission(“Leave Allocation”, “write”, allocation.name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0061.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1327) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L1303)
