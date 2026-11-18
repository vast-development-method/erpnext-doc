# Accounting and settlement · operations 98

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Repost accounting ledger

[Record definition](../../../../data/record-types/repost_accounting_ledger.json)

<a id="op-eb303fe66aaae8"></a>
### Validate docs for voucher types

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_validate_records_for_voucher_types`

**Inputs** doc\_voucher\_types.

**Explicit failure paths** validation helper — translated “{0} {1} not allowed to be reposted. You can enable it by adding it '{2}' table in {3}.”.format(Platform.bold(comma\_and(list(disallowed\_types))), message, Platform.bold(“Allowed Doctype”), Platf ….

**Local steps**

- Set allowed\_types from get\_allowed\_types\_from\_settings().
- Set voucher\_types from set(doc\_voucher\_types).
- If disallowed\_types bound to voucher\_types.difference(allowed\_types).
  - Set message from “are” when len(disallowed\_types) &gt; 1, otherwise “is”.
    - Value choice on len(disallowed\_types) &gt; 1 — true gives “are”, false gives “is”.
  - Call the validation error handler Platform.throw(translated “{0} {1} not allowed to be reposted. You can enable it by adding it '{2}' table in {3}.”.format(Platform.bold(comma\_and(list(disallowed\_types))), message, Platform.bold(“Allowed D ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0161.json#L5774) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1097)

<a id="op-f236e9239d460d"></a>
### Get repost allowed types

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_get_repost_allowed_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Repost Allowed Types” via get\_all.

**Explicit results** allowed\_types · list().

**Local steps**

- Evaluate Platform.has\_permission(“Repost Accounting Ledger”, throw = true).
- If txt.
  - Evaluate filters.update(mapping(“document\_type” → tuple(“like”, formatted text %{txt}%))).
- If allowed\_types bound to Platform.db.get\_all(“Repost Allowed Types”, filters = filters, fields = list(“document\_type”), as\_list = 1, distinct = true).
  - Return allowed\_types.
- Return list().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Accounting Ledger”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1070)

## Record · Repost payment ledger

[Record definition](../../../../data/record-types/repost_payment_ledger.json)

<a id="op-b8fe24ebfc4a67"></a>
### Repost ple for voucher

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_ple_for_voucher`

**Inputs** voucher\_type, voucher\_no, gle\_map = no value.

**Local steps**

- If (voucher\_type and voucher\_no and gle\_map).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type → voucher\_no → gle\_map.
  - Evaluate \_delete\_pl\_entries(voucher\_type, voucher\_no).
  - Evaluate \_delete\_adv\_pl\_entries(voucher\_type, voucher\_no).
  - Evaluate create\_payment\_ledger\_entry(gle\_map, cancel = 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L3327) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1135)

<a id="op-1ab445bb957a0d"></a>
### Start payment ledger repost

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_start_payment_ledger_repost`

**Inputs** docname = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Repost Payment Ledger” via get\_doc · resolve a document from entry.voucher\_type via get\_doc.

**State and service calls** request set\_value on repost\_doc.doctype · rollback.

**Local steps**

- If docname.
  - Set repost\_doc from Platform.get\_doc(“Repost Payment Ledger”, docname).
  - Evaluate repost\_doc.check\_permission(“submit”).
  - If (repost\_doc.docstatus.is\_submitted() and repost\_doc.repost\_status belongs to list(“Queued”, “Failed”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in repost\_doc.docstatus.is\_submitted() → repost\_doc.repost\_status belongs to list(“Queued”, “Failed”).
    - Attempt the following.
      - For each entry in repost\_doc.repost\_vouchers.
        - Set doc from Platform.get\_doc(entry.voucher\_type, entry.voucher\_no).
        - If doc.doctype belongs to list(“Payment Entry”, “Journal Entry”).
          - Set gle\_map from doc.build\_gl\_map().
        - Otherwise.
          - Set gle\_map from doc.get\_gl\_entries().
        - Evaluate repost\_ple\_for\_voucher(entry.voucher\_type, entry.voucher\_no, gle\_map).
      - Evaluate Platform.db.set\_value(repost\_doc.doctype, repost\_doc.name, “repost\_error\_log”, empty text).
      - Evaluate Platform.db.set\_value(repost\_doc.doctype, repost\_doc.name, “repost\_status”, “Completed”).
    - On failure (Exception).
      - Evaluate Platform.db.rollback().
      - Set traceback from Platform.get\_traceback(with\_context = true).
      - If traceback.
        - Set message from (“Traceback: &lt;br&gt;” + traceback).
        - Evaluate Platform.db.set\_value(repost\_doc.doctype, repost\_doc.name, “repost\_error\_log”, message).
      - Evaluate Platform.db.set\_value(repost\_doc.doctype, repost\_doc.name, “repost\_status”, “Failed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from repost\_doc.check\_permission(“submit”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1136)

<a id="op-c72b3d4eb64625"></a>
### Repost Payment Ledger.initialize

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_payment_ledger_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.vouchers from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L4193) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1131)

<a id="op-dabd30e01dee70"></a>
### Repost Payment Ledger.before validate

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_payment_ledger_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.load\_vouchers\_based\_on\_filters().
- Evaluate self.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load vouchers based on filters](operations-098.md#op-85627685b12a0f), [set status](operations-098.md#op-cd758ae36c00c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L4293) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1129)

<a id="op-85627685b12a0f"></a>
### Repost Payment Ledger.load vouchers based on filters

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_payment_ledger_load_vouchers_based_on_filters`

**Inputs** self.

**Local steps**

- If not self.add\_manually.
  - Evaluate self.repost\_vouchers.clear().
  - Evaluate self.get\_vouchers().
  - Evaluate self.extend(“repost\_vouchers”, copy.deepcopy(self.vouchers)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get vouchers](operations-098.md#op-f2f4fdc9599cb5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L4364) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1132)

<a id="op-f2f4fdc9599cb5"></a>
### Repost Payment Ledger.get vouchers

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_payment_ledger_get_vouchers`

**Inputs** self.

**Local steps**

- Evaluate self.vouchers.clear().
- Set filter\_on\_voucher\_types from list(self.voucher\_type) when self.voucher\_type, otherwise VOUCHER\_TYPES.
  - Value choice on self.voucher\_type — true gives list(self.voucher\_type), false gives VOUCHER\_TYPES.
- For each vtype in filter\_on\_voucher\_types.
  - Set doc from qb.DocType(vtype).
  - Set doctype\_name from ConstantColumn(vtype).
  - Set query from qb.from\_(doc).select(doctype\_name.as\_(“voucher\_type”), doc.name.as\_(“voucher\_no”)).where(((doc.docstatus equals 1 bitwise and doc.company equals self.company) bitwise and doc.posting\_date.gte(self.posting\_date))).
  - Set entries from query.run(as\_dict = true).
  - Evaluate self.vouchers.extend(entries).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L4508) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1130)

<a id="op-cd758ae36c00c0"></a>
### Repost Payment Ledger.set status

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_payment_ledger_set_status`

**Inputs** self.

**Local steps**

- <a id="op-cd758ae36c00c0-guard-2"></a>If self.docstatus equals 0.
  - Set self.repost\_status from “Queued”.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus equals 0, self.docstatus = 0 (draft) selects the branch that assigns “Queued” to self.repost\_status. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cd758ae36c00c0-guard-2)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L4917) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1134)

<a id="op-86e4e59493b3f8"></a>
### Repost Payment Ledger.on submit

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_repost_payment_ledger_on_submit`

**Inputs** self.

**State and service calls** msgprint with translated “Repost started in the background”.

**Local steps**

- Evaluate execute\_repost\_payment\_ledger(self.name).
- Evaluate Platform.msgprint(translated “Repost started in the background”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0163.json#L4990) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1133)

<a id="op-b70ae3b77fdd7c"></a>
### Execute repost payment ledger

`operation_enterprise_accounts_record_definitions_repost_payment_ledger_business_behavior_execute_repost_payment_ledger`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue.

**Local steps**

- Evaluate Platform.has\_permission(“Repost Payment Ledger”, ptype = “submit”, doc = docname, throw = true).
- Set job\_name from (“payment\_ledger\_repost\_” + docname).
- Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.repost\_payment\_ledger.repost\_payment\_ledger.start\_payment\_ledger\_repost”, docname = docname, is\_async = true, job\_name = job\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Payment Ledger”, ptype = “submit”, doc = docname, throw = true) · service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.repost\_payment\_ledger.repost\_payment\_ledger.start\_payment\_ledger\_repost”, docname = docname, is\_async = true, job\_name = job\_name).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1128)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-8dfc2c9e86f135"></a>
### Sales Invoice.initialize

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Sales Invoice Item”, “target\_field” → “billed\_amt”, “target\_ref\_field” → “amount”, “target\_dt” → “Sales Order Item”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1025) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1155)

<a id="op-0425322f3315e8"></a>
### Sales Invoice.set indicator

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_set_indicator`

**Inputs** self.

**Local steps**

- If self.outstanding\_amount &lt; 0.
  - Set self.indicator\_title from translated “Credit Note Issued”.
  - Set self.indicator\_color from “gray”.
- Otherwise.
  - If (self.outstanding\_amount &gt; 0 and getdate(self.due\_date) ≥ getdate(nowdate())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.outstanding\_amount &gt; 0 → getdate(self.due\_date) ≥ getdate(nowdate()).
    - Set self.indicator\_color from “orange”.
    - Set self.indicator\_title from translated “Unpaid”.
  - Otherwise.
    - If (self.outstanding\_amount &gt; 0 and getdate(self.due\_date) &lt; getdate(nowdate())).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.outstanding\_amount &gt; 0 → getdate(self.due\_date) &lt; getdate(nowdate()).
      - Set self.indicator\_color from “red”.
      - Set self.indicator\_title from translated “Overdue”.
    - Otherwise.
      - If cint(self.is\_return) equals 1.
        - Set self.indicator\_title from translated “Return”.
        - Set self.indicator\_color from “gray”.
      - Otherwise.
        - Set self.indicator\_color from “green”.
        - Set self.indicator\_title from translated “Paid”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1039) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1169)

<a id="op-b9d320eb86b00e"></a>
### Sales Invoice.onload

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_onload`

**Inputs** self.

**Record and data access** read “Customer” via get\_cached\_value.

**Local steps**

- Evaluate super().onload().
- If self.customer.
  - Set tuple(tax\_withholding\_category, tax\_withholding\_group) from Platform.get\_cached\_value(“Customer”, self.customer, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).
  - Evaluate self.set\_onload(“apply\_tds”, (tax\_withholding\_category or tax\_withholding\_group)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_withholding\_category → tax\_withholding\_group.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer”, self.customer, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0165.json#L6042) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1163)

<a id="op-e69827eca3ad7d"></a>
### Sales Invoice.validate

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Direct return is not allowed for Timesheet.”.

**Local steps**

- Evaluate self.validate\_auto\_set\_posting\_time().
- Evaluate super().validate().
- Evaluate self.is\_subcontracted().
- If not (self.is\_pos or self.is\_debit\_note).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_pos → self.is\_debit\_note.
  - Evaluate self.so\_dn\_required().
- Evaluate SalesTaxWithholding(self).on\_validate().
- Evaluate self.validate\_proj\_cust().
- Evaluate self.validate\_pos\_return().
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.check\_sales\_order\_on\_hold\_or\_close(“sales\_order”).
- Evaluate self.validate\_debit\_to\_acc().
- Evaluate self.clear\_unallocated\_advances(“Sales Invoice Advance”, “advances”).
- Evaluate self.validate\_fixed\_asset().
- Evaluate self.set\_income\_account\_for\_fixed\_assets().
- Evaluate self.validate\_item\_cost\_centers().
- Evaluate self.check\_conversion\_rate().
- Evaluate self.validate\_accounts().
- Evaluate validate\_inter\_company\_party(self.doctype, self.customer, self.company, self.inter\_company\_invoice\_reference).
- If (self.coupon\_code and self.counts\_coupon\_use()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.coupon\_code → self.counts\_coupon\_use().
  - Evaluate validate\_coupon\_code(self.coupon\_code, self.customer).
- If cint(self.is\_pos).
  - Evaluate self.validate\_pos().
- If cint(self.is\_created\_using\_pos).
  - Evaluate self.validate\_created\_using\_pos().
  - Evaluate self.validate\_full\_payment().
- Evaluate self.validate\_dropship\_item().
- If cint(self.update\_stock).
  - Evaluate self.validate\_warehouse().
  - Evaluate self.update\_current\_stock().
- Evaluate self.validate\_delivery\_note().
- Set is\_deferred\_invoice from any(generator of d.get(“enable\_deferred\_revenue”) for d drawn from self.get(“items”)).
  - Draw d from self.get(“items”).
- If is\_deferred\_invoice.
  - Evaluate validate\_service\_stop\_date(self).
- If not self.is\_opening.
  - Set self.is\_opening from “No”.
- Evaluate self.set\_against\_income\_account().
- If (self.is\_return and not self.return\_against and self.timesheets).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.return\_against → self.timesheets.
  - Call the validation error handler Platform.throw(translated “Direct return is not allowed for Timesheet.”).
- If not self.is\_return.
  - Evaluate self.validate\_time\_sheets\_are\_submitted().
- Evaluate self.validate\_delivery\_note\_rows\_billed\_by\_invoice().
- Evaluate self.validate\_closed\_delivery\_notes().
- Evaluate self.validate\_multiple\_billing(“Delivery Note”, “dn\_detail”, “amount”).
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - For each row in self.timesheets.
    - If row.billing\_hours.
      - Set row.billing\_hours from negative abs(row.billing\_hours).
    - If row.billing\_amount.
      - Set row.billing\_amount from negative abs(row.billing\_amount).
- Evaluate self.validate\_update\_stock\_for\_pick\_list\_reference().
- Evaluate self.set\_serial\_and\_batch\_bundle\_from\_pick\_list().
- Evaluate self.update\_packing\_list().
- Evaluate self.set\_billing\_hours\_and\_amount().
- Evaluate self.update\_timesheet\_billing\_for\_project().
- Evaluate self.set\_status().
- If (self.is\_pos and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_pos → not self.is\_return.
  - Evaluate self.verify\_payment\_amount\_is\_positive().
- If (self.is\_pos and self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_pos → self.is\_return.
  - Evaluate self.verify\_payment\_amount\_is\_negative().
- If (self.redeem\_loyalty\_points and self.loyalty\_points and not self.is\_consolidated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.redeem\_loyalty\_points → self.loyalty\_points → not self.is\_consolidated.
  - Evaluate validate\_loyalty\_points(self, self.loyalty\_points).
- Evaluate self.allow\_write\_off\_only\_on\_pos().
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate self.validate\_subcontracted\_sales\_order().
- Evaluate self.validate\_scio\_self\_rm\_qty().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate auto set posting time](operations-100.md#op-c02e566edc3565), [is subcontracted](operations-103.md#op-50791cd041e573), [so dn required](operations-100.md#op-b6525af3bc7696), [validate proj cust](operations-100.md#op-52a083bdca169a), [validate pos return](operations-099.md#op-7d024d645a521b), [validate with previous doc](operations-100.md#op-cd8e0040ccce50), [validate debit to acc](operations-100.md#op-df9fb75940d79c), [validate fixed asset](operations-098.md#op-037fe6953bf2ce), [set income account for fixed assets](operations-101.md#op-c58233b7079f3f), [validate item cost centers](operations-098.md#op-be9873b33574f4), [validate accounts](operations-098.md#op-a3d211850b8f5e), [counts coupon use](operations-103.md#op-83586bcd294ed4), [validate pos](operations-100.md#op-edfb8e9c769e2f), [validate created using pos](operations-100.md#op-c7b1057f5d07d2), [validate full payment](operations-100.md#op-95cadb5c02cdae), [validate dropship item](operations-101.md#op-38f3777437a5bc), [validate warehouse](operations-100.md#op-f3d4b2b080fd16), [update current stock](operations-101.md#op-3f5a6b0a462c8a), [validate delivery note](operations-100.md#op-2b89af9c87d8ad), [set against income account](operations-100.md#op-039c3e9bc951f3), [validate time sheets are submitted](operations-099.md#op-45e90820af32c1), [validate delivery note rows billed by invoice](operations-100.md#op-5a4625706b63f2), [validate closed delivery notes](operations-100.md#op-2aaac7e1aa0cac), [validate update stock for pick list reference](operations-098.md#op-59c028a76edea0), [update packing list](operations-101.md#op-ad8e0241ec5f48), [set billing hours and amount](operations-101.md#op-aa34ef29b7c805), [update timesheet billing for project](operations-101.md#op-1434e787121303), [set status](operations-103.md#op-606a81fc949758), [verify payment amount is positive](operations-102.md#op-8a65cdee3fa796), [verify payment amount is negative](operations-103.md#op-39a1f171082386), [allow write off only on pos](operations-100.md#op-a70f641ee6e0a4), [validate subcontracted sales order](operations-100.md#op-681460dcc500af), [validate scio self rm qty](operations-100.md#op-9c9b5a167cbce1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1049) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1179)

<a id="op-59c028a76edea0"></a>
### Sales Invoice.validate update stock for pick list reference

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_update_stock_for_pick_list_reference`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Update Stock must be checked for item {1} because it is against Pick List {2}.”.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.against\_pick\_list)).

**Local steps**

- If (self.update\_stock or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.update\_stock → self.is\_return.
  - Return no value.
- For each row in self.items.
  - If row.get(“against\_pick\_list”).
    - Call the validation error handler Platform.throw(translated “Row {0}: Update Stock must be checked for item {1} because it is against Pick List {2}.”.format(row.idx, Platform.bold(row.item\_code), Platform.bold(row.against\_pick\_list))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0166.json#L1815) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L8)

<a id="op-a3d211850b8f5e"></a>
### Sales Invoice.validate accounts

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_accounts`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_write\_off\_account().
- Evaluate self.validate\_account\_for\_change\_amount().
- Evaluate self.validate\_income\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate write off account](operations-100.md#op-8f241247fcdfe9), [validate account for change amount](operations-101.md#op-40c79212842ff2), [validate income account](operations-098.md#op-a1c5766b59d752).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0166.json#L2037) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1051) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1181)

<a id="op-6c7593fa0981f3"></a>
### Sales Invoice.validate for repost

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_for_repost`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_write\_off\_account().
- Evaluate self.validate\_account\_for\_change\_amount().
- Evaluate self.validate\_income\_account().
- Evaluate validate\_docs\_for\_voucher\_types(list(“Sales Invoice”)).
- Evaluate validate\_docs\_for\_deferred\_accounting(list(self.name), list()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate write off account](operations-100.md#op-8f241247fcdfe9), [validate account for change amount](operations-101.md#op-40c79212842ff2), [validate income account](operations-098.md#op-a1c5766b59d752).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0166.json#L2128) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1057) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1186)

<a id="op-037fe6953bf2ce"></a>
### Sales Invoice.validate fixed asset

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_fixed_asset`

**Inputs** self.

**Record and data access** read “Asset” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Asset {1} is already added in another row”.format(d.idx, d.asset) · validation helper — translated “'Update Stock' cannot be checked for fixed asset sale” · validation helper — translated “Row #{0}: Asset {1} must be submitted”.format(d.idx, d.asset) · validation helper — translated “Row #{0}: Asset {1} cannot be sold, it is already {2}”.format(d.idx, d.asset, asset\_status) · validation helper — translated “Row #{0}: Asset {1} is already sold”.format(d.idx, d.asset) · 2 additional forms in the steps below.

**Local steps**

- If self.doctype differs from “Sales Invoice”.
  - Return no value.
- Set seen\_assets from set().
- For each d in self.get(“items”).
  - If d.is\_fixed\_asset.
    - If (d.asset and not self.is\_return).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.asset → not self.is\_return.
      - If d.asset belongs to seen\_assets.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Asset {1} is already added in another row”.format(d.idx, d.asset)).
      - Evaluate seen\_assets.add(d.asset).
    - If d.asset.
      - If not self.is\_return.
        - Set tuple(asset\_status, asset\_docstatus) from Platform.db.get\_value(“Asset”, d.asset, list(“status”, “docstatus”)).
        - If self.update\_stock.
          - Call the validation error handler Platform.throw(translated “'Update Stock' cannot be checked for fixed asset sale”).
        - Otherwise.
          - If asset\_docstatus equals 0.
            - Call the validation error handler Platform.throw(translated “Row #{0}: Asset {1} must be submitted”.format(d.idx, d.asset)).
          - Otherwise.
            - If asset\_status belongs to tuple(“Scrapped”, “Cancelled”, “Capitalized”).
              - Call the validation error handler Platform.throw(translated “Row #{0}: Asset {1} cannot be sold, it is already {2}”.format(d.idx, d.asset, asset\_status)).
            - Otherwise.
              - If (asset\_status equals “Sold” and not self.is\_return).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset\_status equals “Sold” → not self.is\_return.
                - Call the validation error handler Platform.throw(translated “Row #{0}: Asset {1} is already sold”.format(d.idx, d.asset)).
        - Evaluate self.validate\_asset\_sale\_date(d).
      - Otherwise.
        - If not self.return\_against.
          - Call the validation error handler Platform.throw(translated “Row #{0}: Return Against is required for returning asset”.format(d.idx)).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Row #{0}: You must select an Asset for Item {1}.”.format(d.idx, d.item\_code), title = translated “Missing Asset”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset sale date](operations-098.md#op-a9be7279f072d5).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L418) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1056)

<a id="op-a9be7279f072d5"></a>
### Sales Invoice.validate asset sale date

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_asset_sale_date`

**Inputs** self, item.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Asset {1} cannot be sold before its last depreciation entry dated {2}”.format(item.idx, item.asset, Platform.format(last\_depreciation\_date, “Date”)).

**Local steps**

- Set last\_depreciation\_date from get\_last\_depreciation\_date(item.asset).
- If (last\_depreciation\_date and getdate(self.posting\_date) &lt; last\_depreciation\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_depreciation\_date → getdate(self.posting\_date) &lt; last\_depreciation\_date.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Asset {1} cannot be sold before its last depreciation entry dated {2}”.format(item.idx, item.asset, Platform.format(last\_depreciation\_date, “Date”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1052)

<a id="op-be9873b33574f4"></a>
### Sales Invoice.validate item cost centers

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_item_cost_centers`

**Inputs** self.

**Local steps**

- For each item in self.items.
  - Evaluate item.validate\_cost\_center(self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0166.json#L2286) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L2)

<a id="op-a1c5766b59d752"></a>
### Sales Invoice.validate income account

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_income_account`

**Inputs** self.

**Local steps**

- For each item in self.get(“items”).
  - Evaluate validate\_account\_head(item.idx, item.income\_account, self.company, translated “Income”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0166.json#L2363) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1188)

<a id="op-e227e028bf0972"></a>
### Sales Invoice.before save

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_paid\_amount().
- Evaluate self.set\_account\_for\_mode\_of\_payment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set paid amount](operations-099.md#op-d485c9ee08267b), [set account for mode of payment](operations-099.md#op-da8799df07a11c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1145)

<a id="op-35be7ccf302d70"></a>
### Sales Invoice.before submit

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.add\_remarks().
- If cint(self.is\_created\_using\_pos).
  - Evaluate self.validate\_mandatory\_pos\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add remarks](operations-100.md#op-1a5d95cac2d3f1), [validate mandatory pos fields](operations-100.md#op-5898d8f5e90584).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1146)
