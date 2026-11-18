# Inventory and warehouses · operations 100

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reposting settings

[Record definition](../../../../data/record-types/stock_reposting_settings.json)

<a id="op-ad2871a72557bf"></a>
### Stock Reposting Settings.reset parallel reposting settings

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_stock_reposting_settings_reset_parallel_reposting_settings`

**Inputs** self.

**Local steps**

- If (not self.item\_based\_reposting and self.enable\_parallel\_reposting).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.item\_based\_reposting → self.enable\_parallel\_reposting.
  - Set self.enable\_parallel\_reposting from 0.
- If (self.enable\_parallel\_reposting and not self.no\_of\_parallel\_reposting).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.enable\_parallel\_reposting → not self.no\_of\_parallel\_reposting.
  - Set self.no\_of\_parallel\_reposting from 4.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L5771) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1135)

<a id="op-2ff6653983f29f"></a>
### Stock Reposting Settings.set minimum reposting time slot

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_stock_reposting_settings_set_minimum_reposting_time_slot`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.limit\_reposting\_timeslot.
  - Return no value.
- Set start\_time from get\_datetime(self.start\_time).
- Set end\_time from get\_datetime(self.end\_time).
- If start\_time &gt; end\_time.
  - Set end\_time from add\_to\_date(end\_time, days = 1, as\_datetime = true).
- Set diff from time\_diff\_in\_hours(end\_time, start\_time).
- If diff &lt; 10.
  - Set self.end\_time from add\_to\_date(start\_time, hours = 10).strftime(“%H:%M:%S”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1136)

<a id="op-3deddd19ddda07"></a>
### Stock Reposting Settings.convert to item wh reposting

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_stock_reposting_settings_convert_to_item_warehouse_reposting`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** request set\_value on “Repost Item Valuation” · call db\_set on self · msgprint with translated “Item Warehouse based reposting has been enabled.”.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set reposting\_data from get\_reposting\_entries().
- Set vouchers from list of d.voucher\_no for d drawn from reposting\_data.
  - Draw d from reposting\_data.
- Set item\_warehouses from mapping().
- For each ledger in get\_stock\_ledgers(vouchers).
  - Set key from tuple(ledger.item\_code, ledger.warehouse).
  - If key does not belong to item\_warehouses.
    - Set item\_warehouses at key from ledger.posting\_date.
  - Otherwise.
    - If Platform.utils.getdate(item\_warehouses.get(key)) &gt; Platform.utils.getdate(ledger.posting\_date).
      - Set item\_warehouses at key from ledger.posting\_date.
- For each tuple(key, posting\_date) in item\_warehouses.items().
  - Set tuple(item\_code, warehouse) from key.
  - Evaluate create\_repost\_item\_valuation(item\_code, warehouse, posting\_date).
- For each row in reposting\_data.
  - Evaluate Platform.db.set\_value(“Repost Item Valuation”, row.name, “status”, “Skipped”).
- Evaluate self.db\_set(“item\_based\_reposting”, 1).
- Evaluate Platform.msgprint(translated “Item Warehouse based reposting has been enabled.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L6204) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1134)

<a id="op-14d1115d28c2bf"></a>
### Get reposting entries

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_get_reposting_entries`

**Inputs** no declared parameters.

**Record and data access** read “Repost Item Valuation” via get\_all.

**Explicit results** Platform.get\_all(“Repost Item Valuation”, fields = list(“voucher\_no”, “name”), filters = mapping(“status” → tuple(“in”, list(“Queued”, “In Progress”)), “docstatus” → 1, “based\_on” → “Transaction”)).

**Local steps**

- Return Platform.get\_all(“Repost Item Valuation”, fields = list(“voucher\_no”, “name”), filters = mapping(“status” → tuple(“in”, list(“Queued”, “In Progress”)), “docstatus” → 1, “based\_on” → “Transaction”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L6810) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1124)

<a id="op-1a83edca337738"></a>
### Get stock ledgers

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_get_stock_ledgers`

**Inputs** vouchers.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** Platform.get\_all(“Stock Ledger Entry”, fields = list(“item\_code”, “warehouse”, “posting\_date”, “posting\_time”, …), filters = mapping(“voucher\_no” → tuple(“in”, vouchers))).

**Local steps**

- Return Platform.get\_all(“Stock Ledger Entry”, fields = list(“item\_code”, “warehouse”, “posting\_date”, “posting\_time”, …), filters = mapping(“voucher\_no” → tuple(“in”, vouchers))).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L6968) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1125)

<a id="op-86a1b4baef296a"></a>
### Create repost item valuation

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_create_repost_item_valuation`

**Inputs** item\_code, warehouse, posting\_date.

**Record and data access** resolve a document from mapping(“doctype” → “Repost Item Valuation”, “company” → Platform.get\_cached\_value(“Warehouse”, warehouse, “company”), “posting\_date” → posting\_date, “based\_on” → “Item and Warehouse”, …) via get\_doc · read “Warehouse” via get\_cached\_value.

**State and service calls** call submit on Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “company” → Platform.get\_cached\_value(“Warehouse”, warehouse, “company”), “posting\_date” → posting\_date, “based\_on” → “Item and Warehouse”, …)).

**Local steps**

- Evaluate Platform.get\_doc(mapping(“doctype” → “Repost Item Valuation”, “company” → Platform.get\_cached\_value(“Warehouse”, warehouse, “company”), “posting\_date” → posting\_date, “based\_on” → “Item and Warehouse”, …)).submit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, warehouse, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0866.json#L7120) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1123)

<a id="op-6f5c9c1df7ff5a"></a>
### Repost incorrect valuation entries

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_repost_incorrect_valuation_entries`

**Inputs** no declared parameters.

**Record and data access** read “Stock Reposting Settings” via get\_single\_value · read “Company” via get\_all.

**State and service calls** enqueue with repost\_incorrect\_valuation\_entries\_for\_company.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“Stock Reposting Settings”, “repost\_incorrect\_valuation\_entries”).
  - Return no value.
- For each company in Platform.get\_all(“Company”, pluck = “name”).
  - Evaluate Platform.enqueue(repost\_incorrect\_valuation\_entries\_for\_company, queue = “long”, job\_id = formatted text repost\_incorrect\_valuation::{company}, deduplicate = true, company = company).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “repost\_incorrect\_valuation\_entries”) · service or queued work from Platform.enqueue(repost\_incorrect\_valuation\_entries\_for\_company, queue = “long”, job\_id = formatted text repost\_incorrect\_valuation::{company}, deduplicate = true, company = company).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1129)

<a id="op-4f638ca80d2490"></a>
### Repost incorrect valuation entries for company

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_repost_incorrect_valuation_entries_for_company`

**Inputs** company.

**Local steps**

- Bind dependencies get\_fiscal\_year.
- Set fy\_start\_date from get\_fiscal\_year(today(), company = company) at 1.
- Evaluate \_repost\_stock\_ledger\_variance(company, fy\_start\_date).
- Evaluate \_repost\_stock\_account\_value\_comparison(company, fy\_start\_date).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1130)

<a id="op-1bfe67320935ec"></a>
### Repost stock ledger variance

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_repost_stock_ledger_variance`

**Inputs** company, fy\_start\_date.

**Explicit results** created.

**Local steps**

- Bind dependencies get\_stock\_ledger\_variance.
- Set created from list().
- For each row in (get\_stock\_ledger\_variance(mapping(“company” → company)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_stock\_ledger\_variance(mapping(“company” → company)) → list().
  - Set row from Platform.\_dict(row).
  - If (not row.posting\_date or getdate(row.posting\_date) &lt; getdate(fy\_start\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.posting\_date → getdate(row.posting\_date) &lt; getdate(fy\_start\_date).
    - Continue with the next iteration or loop test.
  - If has\_pending\_valuation\_repost(company, row.item\_code, row.warehouse).
    - Continue with the next iteration or loop test.
  - Evaluate create\_repost\_item\_valuation(row.item\_code, row.warehouse, row.posting\_date).
  - Evaluate created.append(row).
- If created.
  - Evaluate Platform.logger(“stock\_reposting”).info((formatted text Auto-reposted {len(created)} incorrect-valuation item-warehouse(s) for {company}:  + “, ”.join(generator of formatted text {d.item\_code} @ {d.warehou ….
    - Draw d from created.
- Return created.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L356) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1132)

<a id="op-11775ceb09967c"></a>
### Repost stock account value comparison

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_repost_stock_account_value_comparison`

**Inputs** company, fy\_start\_date.

**Explicit results** no value.

**Local steps**

- Bind dependencies Enterprise.
- If not Enterprise.is\_perpetual\_inventory\_enabled(company).
  - Return no value.
- Bind dependencies create\_reposting\_entries.
- Bind dependencies get\_value\_comparison.
- Set to\_repost from list().
- Set misconfigured from list().
- Set comparison\_filters from Platform.\_dict(company = company, from\_date = fy\_start\_date, as\_on\_date = today()).
- For each row in (get\_value\_comparison(comparison\_filters) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_value\_comparison(comparison\_filters) → list().
  - Set row from Platform.\_dict(row).
  - If row.voucher\_type equals “Journal Entry”.
    - Continue with the next iteration or loop test.
  - If (not row.posting\_date or getdate(row.posting\_date) &lt; getdate(fy\_start\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.posting\_date → getdate(row.posting\_date) &lt; getdate(fy\_start\_date).
    - Continue with the next iteration or loop test.
  - Set wrong\_accounts from list of tuple(warehouse, account) for tuple(warehouse, account, account\_type) drawn from get\_voucher\_warehouse\_accounts(row.voucher\_no, company) where (account\_type and account\_type differs from “Stock”).
    - Draw tuple(warehouse, account, account\_type) from get\_voucher\_warehouse\_accounts(row.voucher\_no, company), keep a combination only if ((account\_type and account\_type differs from “Stock”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type → account\_type differs from “Stock”.
  - If wrong\_accounts.
    - Evaluate misconfigured.extend(generator of tuple(row.voucher\_type, row.voucher\_no, warehouse, account) for tuple(warehouse, account) drawn from wrong\_accounts).
      - Draw tuple(warehouse, account) from wrong\_accounts.
    - Continue with the next iteration or loop test.
  - Evaluate to\_repost.append(row).
- If to\_repost.
  - Evaluate create\_reposting\_entries(to\_repost, company).
  - Evaluate Platform.logger(“stock\_reposting”).info(formatted text Auto-reposted {len(to\_repost)} stock/account value mismatch voucher(s) for {company}.).
- If misconfigured.
  - Evaluate notify\_incorrect\_stock\_account(company, misconfigured).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L883) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1131)

<a id="op-eee885b7675611"></a>
### Get voucher warehouse accounts

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_get_voucher_warehouse_accounts`

**Inputs** voucher\_no, company.

**Record and data access** read “Stock Ledger Entry” via get\_all · read “Warehouse” via get\_cached\_value · read “Company” via get\_cached\_value · read “Account” via get\_cached\_value.

**Explicit results** rows.

**Local steps**

- Set warehouses from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“voucher\_no” → voucher\_no, “is\_cancelled” → 0), pluck = “warehouse”, distinct = true).
- Set rows from list().
- For each warehouse in set of w for w drawn from warehouses where w.
  - Draw w from warehouses, keep a combination only if (w).
  - Set account from (Platform.get\_cached\_value(“Warehouse”, warehouse, “account”) or Platform.get\_cached\_value(“Company”, company, “default\_inventory\_account”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Warehouse”, warehouse, “account”) → Platform.get\_cached\_value(“Company”, company, “default\_inventory\_account”).
  - Set account\_type from Platform.get\_cached\_value(“Account”, account, “account\_type”) when account, otherwise no value.
    - Value choice on account — true gives Platform.get\_cached\_value(“Account”, account, “account\_type”), false gives no value.
  - Evaluate rows.append(tuple(warehouse, account, account\_type)).
- Return rows.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Warehouse”, warehouse, “account”), Platform.get\_cached\_value(“Company”, company, “default\_inventory\_account”) and 1 further calls.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L1617) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1126)

<a id="op-dc169235e491b7"></a>
### Notify incorrect stock account

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_notify_incorrect_stock_account`

**Inputs** company, misconfigured.

**State and service calls** sendmail.

**Explicit results** no value.

**Local steps**

- Set recipients from get\_users\_with\_role(“System Manager”).
- If not recipients.
  - Return no value.
- Set items from empty text.join(generator of text in the contract.format(voucher\_type, get\_link\_to\_form(voucher\_type, voucher\_no), warehouse, (account or translated “No account set”)) for tuple(voucher\_type, voucher\_no, w ….
  - Draw tuple(voucher\_type, voucher\_no, warehouse, account) from misconfigured.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account → translated “No account set”.
- Set subject from translated “Incorrect Stock Asset Account in {0}”.format(company).
- Set message from (((translated “Stock and accounting values could not be reconciled by reposting for {0}.”.format(Platform.bold(company)) + text in the contract) + translated “The warehouse account(s) below are not of type ….
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, message = message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = subject, message = message).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L1998) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1128)

<a id="op-a571f2fcc5cb52"></a>
### Has pending valuation repost

`operation_enterprise_stock_record_definitions_stock_reposting_settings_business_behavior_has_pending_valuation_repost`

**Inputs** company, item\_code, warehouse.

**Record and data access** read “Repost Item Valuation” via exists.

**Explicit results** bool(Platform.db.exists(“Repost Item Valuation”, mapping(“company” → company, “item\_code” → item\_code, “warehouse” → warehouse, “based\_on” → “Item and Warehouse”, …))).

**Local steps**

- Return bool(Platform.db.exists(“Repost Item Valuation”, mapping(“company” → company, “item\_code” → item\_code, “warehouse” → warehouse, “based\_on” → “Item and Warehouse”, …))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L2421) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1127)

## Record · Stock reservation entry

[Record definition](../../../../data/record-types/stock_reservation_entry.json)

<a id="op-3d6280fd39d09f"></a>
### Stock Reservation Entry.validate

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies validate\_disabled\_warehouse, validate\_warehouse\_company.
- Evaluate self.validate\_amended\_doc().
- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_voucher().
- Evaluate self.validate\_group\_warehouse().
- Evaluate validate\_disabled\_warehouse(self.warehouse).
- Evaluate validate\_warehouse\_company(self.warehouse, self.company).
- Evaluate self.validate\_uom\_is\_integer().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate amended doc](operations-101.md#op-cce17b2b04cc68), [validate mandatory](operations-101.md#op-7f404ac15e3167), [validate voucher](operations-100.md#op-dc9f556414fb77), [validate group warehouse](operations-101.md#op-be75e5975a4ff1), [validate uom is integer](operations-101.md#op-9cb77aa8d87765).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L264) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1178)

<a id="op-da01e1cf10fec7"></a>
### Stock Reservation Entry.before insert

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_before_insert`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Set self.delivered\_qty, self.consumed\_qty, self.transferred\_qty from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L826)

<a id="op-dc9f556414fb77"></a>
### Stock Reservation Entry.validate voucher

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_validate_voucher`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Stock Settings” via get\_single\_value · read self.voucher\_type via get\_value.

**Explicit failure paths** validation helper — translated “Please enable {0} in the {1}.”.format(Platform.bold(translated “Stock Reservation”), Platform.bold(translated “Stock Settings”)) · validation helper — translated “{0} {1} must be submitted to reserve stock against it.”.format(translated self.voucher\_type, Platform.bold(self.voucher\_no)) · validation helper — translated “Item {0} is not a row of {1} {2}.”.format(Platform.bold(self.item\_code), translated self.voucher\_type, Platform.bold(self.voucher\_no)).

**Local steps**

- If (self.voucher\_type equals “Sales Order” and not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Sales Order” → not Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).
  - Call the validation error handler Platform.throw(translated “Please enable {0} in the {1}.”.format(Platform.bold(translated “Stock Reservation”), Platform.bold(translated “Stock Settings”))).
- If Platform.db.get\_value(self.voucher\_type, self.voucher\_no, “docstatus”) differs from 1.
  - Call the validation error handler Platform.throw(translated “{0} {1} must be submitted to reserve stock against it.”.format(translated self.voucher\_type, Platform.bold(self.voucher\_no))).
- If (self.voucher\_type equals “Sales Order” and not self.is\_row\_of\_voucher()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Sales Order” → not self.is\_row\_of\_voucher().
  - Call the validation error handler Platform.throw(translated “Item {0} is not a row of {1} {2}.”.format(Platform.bold(self.item\_code), translated self.voucher\_type, Platform.bold(self.voucher\_no))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is row of voucher](operations-100.md#op-5626bb857e5275).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “enable\_stock\_reservation”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L838)

<a id="op-5626bb857e5275"></a>
### Stock Reservation Entry.is row of voucher

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_is_row_of_voucher`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Sales Order Item” via exists · read “Packed Item” via exists.

**Explicit results** bool((Platform.db.exists(“Sales Order Item”, filters) or Platform.db.exists(“Packed Item”, filters))).

**Local steps**

- Set filters from mapping(“name” → self.voucher\_detail\_no, “parent” → self.voucher\_no, “item\_code” → self.item\_code).
- Return bool((Platform.db.exists(“Sales Order Item”, filters) or Platform.db.exists(“Packed Item”, filters))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“Sales Order Item”, filters) → Platform.db.exists(“Packed Item”, filters).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L832)

<a id="op-6219f717fc0e2e"></a>
### Stock Reservation Entry.before submit

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_before_submit`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.set\_reservation\_based\_on().
- Evaluate self.validate\_reservation\_based\_on\_qty().
- Evaluate self.auto\_reserve\_serial\_and\_batch().
- Evaluate self.validate\_reservation\_based\_on\_serial\_and\_batch().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set reservation based on](operations-101.md#op-18eb9b009fa026), [validate reservation based on qty](operations-101.md#op-e16f6b8905319e), [auto reserve serial and batch](operations-101.md#op-cfb4586cbbe416), [validate reservation based on serial and batch](operations-101.md#op-dafb12e7514c83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L6170) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1164)

<a id="op-f3ab786e8a4946"></a>
### Stock Reservation Entry.on submit

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_on_submit`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.update\_reserved\_qty\_in\_voucher().
- Evaluate self.update\_reserved\_qty\_in\_pick\_list().
- Evaluate self.update\_status().
- Evaluate self.update\_reserved\_stock\_in\_bin().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reserved qty in voucher](operations-101.md#op-afeacd6d58a62e), [update reserved qty in pick list](operations-101.md#op-51a2afd185d538), [update status](operations-101.md#op-ed9ab6c42d5f4a), [update reserved stock in bin](operations-101.md#op-e936824e5f0652).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L6281) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1170)

<a id="op-d730d8a70a1c78"></a>
### Stock Reservation Entry.on update after submit

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_on_update_after_submit`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.can\_be\_updated().
- Evaluate self.validate\_uom\_is\_integer().
- Evaluate self.set\_reservation\_based\_on().
- Evaluate self.validate\_reservation\_based\_on\_qty().
- Evaluate self.validate\_reservation\_based\_on\_serial\_and\_batch().
- Evaluate self.update\_reserved\_qty\_in\_voucher().
- Evaluate self.update\_status().
- Evaluate self.update\_reserved\_stock\_in\_bin().
- Evaluate self.reload().

If control reaches the end, it returns no value.

**Methods declared on this owner** [can be updated](operations-101.md#op-dfaebf87433070), [validate uom is integer](operations-101.md#op-9cb77aa8d87765), [set reservation based on](operations-101.md#op-18eb9b009fa026), [validate reservation based on qty](operations-101.md#op-e16f6b8905319e), [validate reservation based on serial and batch](operations-101.md#op-dafb12e7514c83), [update reserved qty in voucher](operations-101.md#op-afeacd6d58a62e), [update status](operations-101.md#op-ed9ab6c42d5f4a), [update reserved stock in bin](operations-101.md#op-e936824e5f0652).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L6392) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1171)

<a id="op-276f90e9ee5552"></a>
### Stock Reservation Entry.on cancel

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_on_cancel`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.update\_reserved\_qty\_in\_voucher().
- Evaluate self.update\_unreserved\_qty\_in\_sre().
- Evaluate self.update\_reserved\_qty\_in\_pick\_list().
- Evaluate self.update\_status().
- Evaluate self.update\_reserved\_stock\_in\_bin().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update reserved qty in voucher](operations-101.md#op-afeacd6d58a62e), [update unreserved qty in sre](operations-101.md#op-da43635c420173), [update reserved qty in pick list](operations-101.md#op-51a2afd185d538), [update status](operations-101.md#op-ed9ab6c42d5f4a), [update reserved stock in bin](operations-101.md#op-e936824e5f0652).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0867.json#L6602) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1169)

<a id="op-a470d3fc63c8cf"></a>
### Stock Reservation Entry.before cancel

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_before_cancel`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Evaluate self.validate\_reserved\_entries().
- Evaluate self.validate\_order\_usage().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reserved entries](operations-100.md#op-f8eacaea430ebe), [validate order usage](operations-100.md#op-4c813f5cee7988).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L248) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1163)

<a id="op-4c813f5cee7988"></a>
### Stock Reservation Entry.validate order usage

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_stockreservationentry_validate_order_usage`

**Inputs** self.

**Declared result** no value.

**Record and data access** read self.voucher\_type via get\_value · read “Stock Entry” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Stock Reservation Entry {0} is already used by {1} {2}. Close the {1} to release the unused stock.”.format(Platform.bold(self.name), translated self.voucher\_type, Platform.bold(self.voucher\_no)).

**Local steps**

- If (self.voucher\_type does not belong to tuple(“Work Order”, “Subcontracting Order”) or not (flt(self.transferred\_qty) or flt(self.consumed\_qty))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.voucher\_type does not belong to tuple(“Work Order”, “Subcontracting Order”) → not (flt(self.transferred\_qty) or flt(self.consumed\_qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.transferred\_qty) → flt(self.consumed\_qty).
  - Return no value.
- Set status from Platform.db.get\_value(self.voucher\_type, self.voucher\_no, “status”).
- If (status equals “Cancelled” or (status equals “Closed” and self.voucher\_type equals “Work Order”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status equals “Cancelled” → (status equals “Closed” and self.voucher\_type equals “Work Order”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status equals “Closed” → self.voucher\_type equals “Work Order”.
  - Return no value.
- If (self.from\_voucher\_type equals “Stock Entry” and Platform.db.get\_value(“Stock Entry”, self.from\_voucher\_no, “docstatus”) equals 2).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_voucher\_type equals “Stock Entry” → Platform.db.get\_value(“Stock Entry”, self.from\_voucher\_no, “docstatus”) equals 2.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Stock Reservation Entry {0} is already used by {1} {2}. Close the {1} to release the unused stock.”.format(Platform.bold(self.name), translated self.voucher\_type, Platform.bold(s ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L837)

<a id="op-f8eacaea430ebe"></a>
### Stock Reservation Entry.validate reserved entries

`operation_enterprise_stock_record_definitions_stock_reservation_entry_business_behavior_stock_reservation_entry_validate_reserved_entries`

**Inputs** self.

**Record and data access** read “Stock Reservation Entry” via get\_all · read “Work Order” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot cancel Stock Reservation Entry {0}, as it has used in the work order {1}. Please cancel the work orde …”.format(“, ”.join(list of Platform.bold(entry.name) for entry drawn from entries), ….

**Local steps**

- Set entries from Platform.get\_all(“Stock Reservation Entry”, fields = list(“voucher\_no as name”), filters = mapping(“status” → “Closed”, “docstatus” → 1, “from\_voucher\_type” → “Purchase Receipt”, “from\_voucher\_no” → self.f ….
- If entries.
  - Set work\_orders from Platform.get\_all(“Work Order”, fields = list(“name”), filters = mapping(“production\_plan” → tuple(“in”, list of entry.name for entry drawn from entries))).
    - Draw entry from entries.
  - Call the validation error handler Platform.throw(translated “Cannot cancel Stock Reservation Entry {0}, as it has used in the work order {1}. Please cancel the work orde …”.format(“, ”.join(list of Platform.bold(entry.name) for entry drawn ….
    - Draw entry from entries.
    - Draw wo from work\_orders.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L270) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1184)
