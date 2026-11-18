# Inventory and warehouses · operations 51

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Repost item valuation

[Record definition](../../../../data/record-types/repost_item_valuation.json)

<a id="op-55d2493a171797"></a>
### Repost Item Valuation.validate recalculate valuation rate

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_validate_recalculate_valuation_rate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Recalculate Valuation Rate is only allowed for a Purchase Receipt or a Purchase Invoice with Update Stock”.

**Local steps**

- If (self.recalculate\_valuation\_rate and not self.can\_recalculate\_valuation\_rate()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.recalculate\_valuation\_rate → not self.can\_recalculate\_valuation\_rate().
  - Call the validation error handler Platform.throw(translated “Recalculate Valuation Rate is only allowed for a Purchase Receipt or a Purchase Invoice with Update Stock”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can recalculate valuation rate](operations-051.md#op-66e604ac83341b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1073) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L570)

<a id="op-66e604ac83341b"></a>
### Repost Item Valuation.can recalculate valuation rate

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_can_recalculate_valuation_rate`

**Inputs** self.

**Record and data access** read “Purchase Invoice” via get\_value.

**Explicit results** false · true · bool(Platform.db.get\_value(“Purchase Invoice”, self.voucher\_no, “update\_stock”)).

**Local steps**

- <a id="op-66e604ac83341b-guard-2"></a>If self.based\_on differs from “Transaction”.
  - Return false.
- If self.voucher\_type equals “Purchase Receipt”.
  - Return true.
- If self.voucher\_type equals “Purchase Invoice”.
  - Return bool(Platform.db.get\_value(“Purchase Invoice”, self.voucher\_no, “update\_stock”)).
- Return false.

**Derived branch illustrations**

- At the comparison self.based\_on differs from “Transaction”, self.based\_on = “Item and Warehouse” selects the branch that returns false. With self.based\_on = “Transaction”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-66e604ac83341b-guard-2)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L561)

<a id="op-c1ee0185c54918"></a>
### Repost Item Valuation.validate recreate stock ledgers

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_validate_recreate_stock_ledgers`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_all · read “Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If not self.recreate\_stock\_ledgers.
  - Return no value.
- Set items from list().
- If self.based\_on equals “Item and Warehouse”.
  - Evaluate items.append(self.item\_code).
- Otherwise.
  - Set items from list of d.item\_code for d drawn from get\_items\_to\_be\_repost(self.voucher\_type, self.voucher\_no).
    - Draw d from get\_items\_to\_be\_repost(self.voucher\_type, self.voucher\_no).
  - Update items using + Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“voucher\_type” → self.voucher\_type, “voucher\_no” → self.voucher\_no, “docstatus” → 1, “is\_cancelled” → 0), pluck = “item\_code”).
  - Set items from list(set(items)).
- If serial\_batch\_items bound to Platform.get\_all(“Item”, or\_filters = mapping(“has\_serial\_no” → 1, “has\_batch\_no” → 1), filters = mapping(“name” → tuple(“in”, items))).
  - Set item\_list from “, ”.join(list of d.name for d drawn from serial\_batch\_items).
    - Draw d from serial\_batch\_items.
  - Set msg from translated “Since {0} are Serial No/Batch No items, you cannot enable 'Recreate Stock Ledgers' in Repost Item Valuation.”.format(item\_list).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L472)

<a id="op-e9dee7e5fbe26c"></a>
### Repost Item Valuation.validate period closing voucher

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_validate_period_closing_voucher`

**Inputs** self.

**Explicit failure paths** validation helper — translated msg · validation helper — translated “Due to stock closing entry {0}, you cannot repost item valuation before {1}”.format(name, to\_date).

**Local steps**

- Set year\_end\_date from self.get\_max\_period\_closing\_date(self.company).
- If (year\_end\_date and getdate(self.posting\_date) ≤ getdate(year\_end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in year\_end\_date → getdate(self.posting\_date) ≤ getdate(year\_end\_date).
  - Set date from Platform.format(year\_end\_date, “Date”).
  - Set msg from formatted text Due to period closing, you cannot repost item valuation before {date}.
  - Call the validation error handler Platform.throw(translated msg).
- If self.voucher\_type.
  - Evaluate validate\_accounting\_period(list(Platform.\_dict(mapping(“posting\_date” → self.posting\_date, “company” → self.company, “voucher\_type” → self.voucher\_type)))).
- Set closing\_stock from self.get\_closing\_stock\_balance().
- If (closing\_stock and closing\_stock at 0.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in closing\_stock → closing\_stock at 0.name.
  - Set name from get\_link\_to\_form(“Stock Closing Entry”, closing\_stock at 0.name).
  - Set to\_date from Platform.format(closing\_stock at 0.posting\_date, “Date”).
  - Call the validation error handler Platform.throw(translated “Due to stock closing entry {0}, you cannot repost item valuation before {1}”.format(name, to\_date)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get max period closing date](operations-051.md#op-299b9215ef5fd0), [get closing stock balance](operations-051.md#op-3080eb0c78190b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L471)

<a id="op-0a4dee13300a89"></a>
### Repost Item Valuation.reset recreate stock ledgers

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_reset_recreate_stock_ledgers`

**Inputs** self.

**Local steps**

- If (self.recreate\_stock\_ledgers and self.based\_on differs from “Transaction”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.recreate\_stock\_ledgers → self.based\_on differs from “Transaction”.
  - Set self.recreate\_stock\_ledgers from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L2743) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L804) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L462)

<a id="op-03cff34d2b62c4"></a>
### Repost Item Valuation.validate later vouchers in closed period

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_validate_later_vouchers_in_closed_period`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with ClosedAccountingPeriod — translated “Cannot repost item valuation from {0} because {1} {2} falls in the closed Accounting Period {3}”.format(Platform.bold(Platform.format(self.posting\_date, “Date”)), voucher.voucher\_type, get\_link ….

**Local steps**

- If (self.repost\_only\_accounting\_ledgers or not cint(Enterprise.is\_perpetual\_inventory\_enabled(self.company))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.repost\_only\_accounting\_ledgers → not cint(Enterprise.is\_perpetual\_inventory\_enabled(self.company)).
  - Return no value.
- Set item\_warehouses from self.get\_item\_warehouses\_to\_repost().
- If not item\_warehouses.
  - Return no value.
- If voucher bound to self.get\_later\_voucher\_in\_closed\_period(item\_warehouses).
  - Call the validation error handler Platform.throw(translated “Cannot repost item valuation from {0} because {1} {2} falls in the closed Accounting Period {3}”.format(Platform.bold(Platform.format(self.posting\_date, “Date”)), voucher.voucher ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item warehouses to repost](operations-051.md#op-7002d7b74c27e8), [get later voucher in closed period](operations-051.md#op-c9a4883244e5f4).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1072) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L569)

<a id="op-7002d7b74c27e8"></a>
### Repost Item Valuation.get item warehouses to repost

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_get_item_warehouses_to_repost`

**Inputs** self.

**Explicit results** list(set of tuple(row.item\_code, row.warehouse) for row drawn from rows) · list(tuple(self.item\_code, self.warehouse)) · list().

**Local steps**

- If self.based\_on equals “Transaction”.
  - Set rows from get\_items\_to\_be\_repost(self.voucher\_type, self.voucher\_no).
  - Return list(set of tuple(row.item\_code, row.warehouse) for row drawn from rows).
    - Draw row from rows.
- If (self.item\_code and self.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → self.warehouse.
  - Return list(tuple(self.item\_code, self.warehouse)).
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L563)

<a id="op-c9a4883244e5f4"></a>
### Repost Item Valuation.get later voucher in closed period

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_get_later_voucher_in_closed_period`

**Inputs** self, item\_warehouses.

**Explicit results** result at 0 when result, otherwise no value.

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Set period from Platform.qb.DocType(“Accounting Period”).
- Set closed\_document from Platform.qb.DocType(“Closed Document”).
- Set query from nested operand in the contract(nested operand in the contract).select(sle.voucher\_type, sle.voucher\_no, nested operand in the contract.as\_(“accounting\_period”)).where(((((nested operand in the contract bit ….
- If self.voucher\_no.
  - Set query from query.where(sle.voucher\_no differs from self.voucher\_no).
- Set result from query.run(as\_dict = true).
- Return result at 0 when result, otherwise no value.
  - Value choice on result — true gives result at 0, false gives no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L564)

<a id="op-3080eb0c78190b"></a>
### Repost Item Valuation.get closing stock balance

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_get_closing_stock_balance`

**Inputs** self.

**Explicit results** list() · list(Platform.\_dict(name = closing\_entry.name, posting\_date = closing\_entry.to\_date)).

**Local steps**

- Set closing\_entry from get\_closing\_entry\_for\_closed\_period(self.company).
- If (not closing\_entry or getdate(self.posting\_date) &gt; getdate(closing\_entry.to\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not closing\_entry → getdate(self.posting\_date) &gt; getdate(closing\_entry.to\_date).
  - Return list().
- Return list(Platform.\_dict(name = closing\_entry.name, posting\_date = closing\_entry.to\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L794) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L452)

<a id="op-299b9215ef5fd0"></a>
### Repost Item Valuation.get max period closing date

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_get_maximum_period_closing_date`

**Inputs** company.

**Wrappers, in declaration order** staticmethod.

**Explicit results** query at 0 at 0 when (query and query at 0 at 0), otherwise no value.

**Local steps**

- Set table from Platform.qb.DocType(“Period Closing Voucher”).
- Set query from nested operand in the contract(nested operand in the contract).select(Max(nested operand in the contract.period\_end\_date)).where((table.company equals company bitwise and table.docstatus equals 1)).run().
- Return query at 0 at 0 when (query and query at 0 at 0), otherwise no value.
  - Value choice on (query and query at 0 at 0) — true gives query at 0 at 0, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query → query at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L3012) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L795) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L453)

<a id="op-2aa691f72acfb2"></a>
### Repost Item Valuation.validate accounts freeze

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_validate_accounts_freeze`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**State and service calls** msgprint with translated “Caution: This might alter frozen accounts.”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “You cannot repost item valuation before {}”.format(acc\_frozen\_till\_date).

**Local steps**

- Set acc\_frozen\_till\_date from Platform.db.get\_value(“Company”, self.company, “accounts\_frozen\_till\_date”).
- Set frozen\_accounts\_modifier from Platform.db.get\_value(“Company”, self.company, “role\_allowed\_for\_frozen\_entries”).
- If not acc\_frozen\_till\_date.
  - Return no value.
- If getdate(self.posting\_date) ≤ getdate(acc\_frozen\_till\_date).
  - If (frozen\_accounts\_modifier and Platform.session.user belongs to get\_users\_with\_role(frozen\_accounts\_modifier)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in frozen\_accounts\_modifier → Platform.session.user belongs to get\_users\_with\_role(frozen\_accounts\_modifier).
    - Evaluate Platform.msgprint(translated “Caution: This might alter frozen accounts.”).
    - Return no value.
  - Call the validation error handler Platform.throw(translated “You cannot repost item valuation before {}”.format(acc\_frozen\_till\_date)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L470)

<a id="op-07aac42b27da71"></a>
### Repost Item Valuation.reset field values

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_reset_field_values`

**Inputs** self.

**Local steps**

- <a id="op-07aac42b27da71-guard-2"></a>If self.based\_on equals “Transaction”.
  - Set self.item\_code from no value.
  - Set self.warehouse from no value.
- Set self.allow\_negative\_stock from 1.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.based\_on equals “Transaction”, self.based\_on = “Transaction” selects the branch that assigns no value to self.item\_code. With self.based\_on = “Item and Warehouse”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-07aac42b27da71-guard-2)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L3640) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L803) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L461)

<a id="op-438d197cc85fb1"></a>
### Repost Item Valuation.on cancel

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_attachment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear attachment](operations-051.md#op-ce884e192d9206).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L3745) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L796) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L454)

<a id="op-acb8cea7014164"></a>
### Repost Item Valuation.on trash

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_attachment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear attachment](operations-051.md#op-ce884e192d9206).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L3796) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L799) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L457)

<a id="op-421b54bcf256d0"></a>
### Repost Item Valuation.set company

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_set_company`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read self.voucher\_type via get\_cached\_value · read “Warehouse” via get\_cached\_value.

**Local steps**

- Evaluate self.check\_permission(“write”).
- If self.based\_on equals “Transaction”.
  - Set self.company from Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “company”).
- Otherwise.
  - If self.warehouse.
    - Set self.company from Platform.get\_cached\_value(“Warehouse”, self.warehouse, “company”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · configured or stored value from Platform.get\_cached\_value(self.voucher\_type, self.voucher\_no, “company”), Platform.get\_cached\_value(“Warehouse”, self.warehouse, “company”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L807) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L465)

<a id="op-5ad04e77ece282"></a>
### Repost Item Valuation.set status

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_set_status`

**Inputs** self, status = no value, write = true.

**State and service calls** call db\_set on self.

**Local steps**

- Set status from (status or self.status).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status → self.status.
- If not status.
  - Set self.status from “Queued”.
- Otherwise.
  - Set self.status from status.
- If write.
  - Evaluate self.db\_set(“status”, self.status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L4046) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L467)

<a id="op-ce884e192d9206"></a>
### Repost Item Valuation.clear attachment

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_clear_attachment`

**Inputs** self.

**State and service calls** request delete\_doc for “File” · call db\_set on self.

**Local steps**

- If attachments bound to get\_attachments(self.doctype, self.name).
  - Set attachment from attachments at 0.
  - Evaluate Platform.delete\_doc(“File”, attachment.name, ignore\_permissions = true, force = true).
- If self.reposting\_data\_file.
  - Evaluate self.db\_set(“reposting\_data\_file”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L4220) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L791) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L449)

<a id="op-74116c0a406f68"></a>
### Repost Item Valuation.on submit

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_on_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Evaluate mark\_closing\_entries\_outdated(self.company, self.posting\_date).
- If not Platform.in\_test.
  - Return no value.
- If (self.flags.dont\_run\_in\_test or Platform.flags.dont\_execute\_stock\_reposts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.dont\_run\_in\_test → Platform.flags.dont\_execute\_stock\_reposts.
  - Return no value.
- Evaluate repost(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L798) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L456)

<a id="op-0926823580cc34"></a>
### Repost Item Valuation.before cancel

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.check\_pending\_repost\_against\_cancelled\_transaction().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check pending repost against cancelled transaction](operations-051.md#op-72e07e002ccbc5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L4541) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L447)

<a id="op-72e07e002ccbc5"></a>
### Repost Item Valuation.check pending repost against cancelled transaction

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_check_pending_repost_against_cancelled_transaction`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- <a id="op-72e07e002ccbc5-guard-2"></a>If self.status does not belong to tuple(“Queued”, “In Progress”).
  - Return no value.
- Set msg from translated “Cannot cancel as processing of cancelled documents is pending.”.
- Update msg using + (text in the contract + translated “Please try again in an hour.”).
- Call the validation error handler Platform.throw(msg, title = translated “Pending processing”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to tuple(“Queued”, “In Progress”), self.status = “Completed” selects the branch that returns no value. With self.status = “Queued”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-72e07e002ccbc5-guard-2)

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L4592) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L790) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L448)

<a id="op-80cd52639b55cf"></a>
### Repost Item Valuation.restart reposting

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_restart_reposting`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_update on self.

**Explicit failure paths** validation helper — translated “Only a submitted Repost Item Valuation with status Failed can be restarted”.

**Local steps**

- Evaluate self.load\_from\_db().
- Evaluate self.check\_permission(“write”).
- If (self.docstatus differs from 1 or self.status differs from “Failed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 1 → self.status differs from “Failed”.
  - Call the validation error handler Platform.throw(translated “Only a submitted Repost Item Valuation with status Failed can be restarted”).
- Evaluate self.set\_status(“Queued”, write = false).
- Set self.current\_index from 0.
- Set self.distinct\_item\_and\_warehouse from no value.
- Set self.items\_to\_be\_repost from no value.
- Set self.gl\_reposting\_index from 0.
- Set self.total\_reposting\_count from 0.
- Set self.total\_vouchers from 0.
- Set self.vouchers\_posted from 0.
- Evaluate self.clear\_attachment().
- Evaluate self.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status](operations-051.md#op-5ad04e77ece282), [clear attachment](operations-051.md#op-ce884e192d9206).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L806) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L464)

<a id="op-3708e677ed88c1"></a>
### Repost Item Valuation.skipped similar reposts

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_skipped_similar_reposts`

**Inputs** self.

**Record and data access** read “Repost Item Valuation” via get\_all · read “Repost Item Valuation” via get\_value.

**State and service calls** request set\_value on “Repost Item Valuation”.

**Local steps**

- Set repost\_entries from Platform.get\_all(“Repost Item Valuation”, filters = mapping(“based\_on” → “Transaction”, “voucher\_type” → self.voucher\_type, “voucher\_no” → self.voucher\_no, “docstatus” → 1, …), fields = list(“name”, “repos ….
- For each entry in repost\_entries.
  - If Platform.db.get\_value(“Repost Item Valuation”, entry.reposting\_reference, “status”) equals “Completed”.
    - Evaluate Platform.db.set\_value(“Repost Item Valuation”, entry.name, “status”, “Skipped”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L5042) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L468)

<a id="op-7f68397a34c2d7"></a>
### Repost Item Valuation.deduplicate similar repost

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_deduplicate_similar_repost`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- If self.repost\_only\_accounting\_ledgers.
  - Evaluate self.skipped\_similar\_reposts().
  - Return no value.
- <a id="op-7f68397a34c2d7-guard-9"></a>If self.based\_on differs from “Item and Warehouse”.
  - Return no value.
- Set filters from mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse, “name” → self.name, “posting\_date” → self.posting\_date, …).
- Evaluate Platform.db.sql(multiline text in the contract, filters).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.based\_on differs from “Item and Warehouse”, self.based\_on = “Transaction” selects the branch that returns no value. With self.based\_on = “Item and Warehouse”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7f68397a34c2d7-guard-9)

**Methods declared on this owner** [skipped similar reposts](operations-051.md#op-3708e677ed88c1), [get repost started at](operations-051.md#op-7da78382d73b1b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L793) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L451)

<a id="op-7da78382d73b1b"></a>
### Repost Item Valuation.get repost started at

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_get_repost_started_at`

**Inputs** self.

**Explicit results** (self.flags.repost\_started\_at or now()).

**Local steps**

- Return (self.flags.repost\_started\_at or now()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.flags.repost\_started\_at → now().

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L565)
