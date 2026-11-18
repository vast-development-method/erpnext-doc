# Asset management · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset movement

[Record definition](../../../../data/record-types/asset_movement.json)

<a id="op-fe526dc9233948"></a>
### Asset Movement.on cancel

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.set\_latest\_location\_and\_custodian\_in\_asset().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set latest location and custodian in asset](operations-015.md#op-29b48f812c00b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0327.json#L3835) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L530)

<a id="op-29b48f812c00b4"></a>
### Asset Movement.set latest location and custodian in asset

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_set_latest_location_and_custodian_in_asset`

**Inputs** self.

**Local steps**

- For each d in self.assets.
  - Set tuple(current\_location, current\_employee) from self.get\_latest\_location\_and\_custodian(d.asset).
  - Set tuple(changed\_location, previous\_custodian) from self.update\_asset\_location\_and\_custodian(d.asset, current\_location, current\_employee).
  - Set changed\_employee from current\_employee when previous\_custodian is distinct from no value, otherwise empty text.
    - Value choice on previous\_custodian is distinct from no value — true gives current\_employee, false gives empty text.
  - Evaluate self.log\_asset\_activity(d.asset, changed\_location, changed\_employee, previous\_custodian).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get latest location and custodian](operations-015.md#op-c58d635ec789e1), [update asset location and custodian](operations-015.md#op-106cb29498537d), [log asset activity](operations-015.md#op-c49f63edf4edea).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L532)

<a id="op-c58d635ec789e1"></a>
### Asset Movement.get latest location and custodian

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_get_latest_location_and_custodian`

**Inputs** self, asset.

**Explicit results** tuple(location, employee).

**Local steps**

- Set asm from Platform.qb.DocType(“Asset Movement”).
- Set asm\_item from Platform.qb.DocType(“Asset Movement Item”).
- Set location from self.get\_latest\_movement\_value(asset, asm\_item.target\_location, asm.purpose.isin(LOCATION\_PURPOSES)).
- Set employee from self.get\_latest\_movement\_value(asset, asm\_item.to\_employee, (asm.purpose.isin(CUSTODIAN\_PURPOSES) bitwise or IfNull(asm\_item.to\_employee, empty text) differs from empty text)).
- Return tuple(location, employee).

**Methods declared on this owner** [get latest movement value](operations-015.md#op-c98c2b8ad2f731).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L528)

<a id="op-c98c2b8ad2f731"></a>
### Asset Movement.get latest movement value

`operation_enterprise_binding_enterprise_assets_doctype_asset_movement_asset_movement_assetmovement_get_latest_movement_value`

**Inputs** self, asset, field, condition.

**Declared result** str.

**Explicit results** latest\_movement\_entry at 0 at 0 when latest\_movement\_entry, otherwise empty text.

**Local steps**

- Set asm from Platform.qb.DocType(“Asset Movement”).
- Set asm\_item from Platform.qb.DocType(“Asset Movement Item”).
- Set latest\_movement\_entry from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(asm.name, order = nested operand in the contract.qb.desc).limit(1).run().
- Return latest\_movement\_entry at 0 at 0 when latest\_movement\_entry, otherwise empty text.
  - Value choice on latest\_movement\_entry — true gives latest\_movement\_entry at 0 at 0, false gives empty text.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1384)

<a id="op-106cb29498537d"></a>
### Asset Movement.update asset location and custodian

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_update_asset_location_and_custodian`

**Inputs** self, asset\_id, location, employee.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** request set\_value on “Asset”.

**Explicit results** tuple(changed\_location, previous\_custodian).

**Local steps**

- Set asset from Platform.get\_doc(“Asset”, asset\_id).
- Set tuple(changed\_location, previous\_custodian) from tuple(empty text, no value).
- If cstr(employee) differs from cstr(asset.custodian).
  - Evaluate Platform.db.set\_value(“Asset”, asset\_id, “custodian”, cstr(employee)).
  - Set previous\_custodian from cstr(asset.custodian).
- If (location and location differs from asset.location).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in location → location differs from asset.location.
  - Evaluate Platform.db.set\_value(“Asset”, asset\_id, “location”, location).
  - Set changed\_location from location.
- Return tuple(changed\_location, previous\_custodian).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L533)

<a id="op-c49f63edf4edea"></a>
### Asset Movement.log asset activity

`operation_enterprise_assets_record_definitions_asset_movement_business_behavior_asset_movement_log_asset_activity`

**Inputs** self, asset\_id, location, employee, previous\_custodian = no value.

**Local steps**

- If (location and employee).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in location → employee.
  - Evaluate add\_asset\_activity(asset\_id, translated “Asset received at Location {0} and issued to Employee {1}”.format(get\_link\_to\_form(“Location”, location), get\_link\_to\_form(“Employee”, employee))).
- Otherwise.
  - If location.
    - Evaluate add\_asset\_activity(asset\_id, translated “Asset transferred to Location {0}”.format(get\_link\_to\_form(“Location”, location))).
  - Otherwise.
    - If employee.
      - Evaluate add\_asset\_activity(asset\_id, translated “Asset issued to Employee {0}”.format(get\_link\_to\_form(“Employee”, employee))).
    - Otherwise.
      - If previous\_custodian.
        - Evaluate add\_asset\_activity(asset\_id, translated “Asset returned by Employee {0}”.format(get\_link\_to\_form(“Employee”, previous\_custodian))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L529)

## Record · Asset repair

[Record definition](../../../../data/record-types/asset_repair.json)

<a id="op-4cfc9b5d77f233"></a>
### Asset Repair.validate

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate`

**Inputs** self.

**Local steps**

- Set self.asset\_doc from Platform.get\_lazy\_doc(“Asset”, self.asset).
- Evaluate self.validate\_asset().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_purchase\_invoices().
- Evaluate self.calculate\_consumed\_items\_cost().
- Evaluate self.calculate\_repair\_cost().
- Evaluate self.calculate\_total\_repair\_cost().
- Evaluate self.check\_repair\_status().
- Evaluate self.set\_downtime().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset](operations-015.md#op-592454823dfa34), [validate dates](operations-015.md#op-19baafe7bfc812), [validate purchase invoices](operations-015.md#op-0bf473b120a5a4), [calculate consumed items cost](operations-015.md#op-17b4973b1359fe), [calculate repair cost](operations-015.md#op-6d3c0219ad8754), [calculate total repair cost](operations-015.md#op-620185a179e2dc), [check repair status](operations-016.md#op-0ab2e536e8614e), [set downtime](operations-016.md#op-e79b343ceec1ed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L564)

<a id="op-2abac9a49ecc96"></a>
### Asset Repair.on update

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_on_update`

**Inputs** self.

**Local steps**

- If self.has\_value\_changed(“repair\_status”).
  - Evaluate self.add\_repair\_activity(self.repair\_status).
- If self.docstatus.is\_draft().
  - Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add repair activity](operations-015.md#op-53b74969a6136c), [update status](operations-015.md#op-ef7d41413238d7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1392)

<a id="op-592454823dfa34"></a>
### Asset Repair.validate asset

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_asset`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Asset {0} is in {1} status and cannot be repaired.”.format(get\_link\_to\_form(“Asset”, self.asset), self.asset\_doc.status).

**Local steps**

- If self.asset\_doc.status belongs to tuple(“Sold”, “Scrapped”, “Capitalized”).
  - Call the validation error handler Platform.throw(translated “Asset {0} is in {1} status and cannot be repaired.”.format(get\_link\_to\_form(“Asset”, self.asset), self.asset\_doc.status)).
- If self.asset\_doc.get\_status() equals “Fully Depreciated”.
  - Set self.capitalize\_repair\_cost from 0.
  - Set self.increase\_in\_asset\_life from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L565)

<a id="op-19baafe7bfc812"></a>
### Asset Repair.validate dates

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Completion Date is mandatory for a completed Asset Repair” · validation helper — translated “Completion Date can not be before Failure Date. Please adjust the dates accordingly.”.

**Local steps**

- If (self.repair\_status equals “Completed” and not self.completion\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.repair\_status equals “Completed” → not self.completion\_date.
  - Call the validation error handler Platform.throw(translated “Completion Date is mandatory for a completed Asset Repair”).
- If (self.completion\_date and getdate(self.failure\_date) &gt; getdate(self.completion\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.completion\_date → getdate(self.failure\_date) &gt; getdate(self.completion\_date).
  - Call the validation error handler Platform.throw(translated “Completion Date can not be before Failure Date. Please adjust the dates accordingly.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L566)

<a id="op-0bf473b120a5a4"></a>
### Asset Repair.validate purchase invoices

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_purchase_invoices`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_purchase\_invoices().
- Evaluate self.validate\_purchase\_invoice\_status().
- For each d in self.invoices.
  - Evaluate self.validate\_expense\_account(d).
  - Evaluate self.validate\_purchase\_invoice\_repair\_cost(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate purchase invoices](operations-015.md#op-e9faa8080c00eb), [validate purchase invoice status](operations-015.md#op-5d38f2e237f40d), [validate expense account](operations-015.md#op-cd562dd508cff8), [validate purchase invoice repair cost](operations-015.md#op-006c52db55ce44).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L2241) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L571)

<a id="op-e9faa8080c00eb"></a>
### Asset Repair.validate duplicate purchase invoices

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_duplicate_purchase_invoices`

**Inputs** self.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set purchase\_invoices from set().
- Set duplicates from list().
- For each row in self.invoices.
  - Set key from tuple(row.purchase\_invoice, row.expense\_account).
  - If key belongs to purchase\_invoices.
    - Evaluate duplicates.append(tuple(row.idx, row.purchase\_invoice, row.expense\_account)).
  - Otherwise.
    - Evaluate purchase\_invoices.add(key).
- If duplicates.
  - Set duplicate\_links from empty text.join(list of formatted text &lt;li&gt;{translated “Row #{0}:”.format(idx)} {get\_link\_to\_form(“Purchase Invoice”, pi)} - {Platform.bold(account)}&lt;/li&gt; for tuple(idx, pi, account) drawn from duplicates).
    - Draw tuple(idx, pi, account) from duplicates.
  - Set msg from (translated “The following rows are duplicates:” + formatted text &lt;br&gt;&lt;ul&gt;{duplicate\_links}&lt;/ul&gt;).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L2381) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L567)

<a id="op-5d38f2e237f40d"></a>
### Asset Repair.validate purchase invoice status

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_purchase_invoice_status`

**Inputs** self.

**Record and data access** read “Purchase Invoice” via get\_all.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Set pi\_names from list of row.purchase\_invoice for row drawn from self.invoices.
  - Draw row from self.invoices.
- Set docstatus from Platform.\_dict(Platform.db.get\_all(“Purchase Invoice”, filters = mapping(“name” → list(“in”, pi\_names)), fields = list(“name”, “docstatus”), as\_list = true)).
- Set invalid\_invoice from list().
- For each row in self.invoices.
  - If docstatus.get(row.purchase\_invoice) differs from 1.
    - Evaluate invalid\_invoice.append(tuple(row.idx, row.purchase\_invoice)).
- If invalid\_invoice.
  - Set invoice\_links from empty text.join(list of formatted text &lt;li&gt;{translated “Row #{0}:”.format(idx)} {get\_link\_to\_form(“Purchase Invoice”, pi)}&lt;/li&gt; for tuple(idx, pi) drawn from invalid\_invoice).
    - Draw tuple(idx, pi) from invalid\_invoice.
  - Set msg from (translated “The following Purchase Invoices are not submitted:” + formatted text &lt;br&gt;&lt;ul&gt;{invoice\_links}&lt;/ul&gt;).
  - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L2861) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L570)

<a id="op-cd562dd508cff8"></a>
### Asset Repair.validate expense account

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_expense_account`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Expense account {1} is not valid for Purchase Invoice {2}. Only expense accounts from non-stock it …”.format(row.idx, Platform.bold(row.expense\_account), get\_link\_to\_form(“Purchase In ….

**Local steps**

- Set valid\_accounts from \_get\_expense\_accounts\_for\_purchase\_invoice(row.purchase\_invoice).
- If row.expense\_account does not belong to valid\_accounts.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Expense account {1} is not valid for Purchase Invoice {2}. Only expense accounts from non-stock it …”.format(row.idx, Platform.bold(row.expense\_account), get\_link\_to\_fo ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L3408) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L568)

<a id="op-006c52db55ce44"></a>
### Asset Repair.validate purchase invoice repair cost

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_purchase_invoice_repair_cost`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Repair cost {1} exceeds available amount {2} for Purchase Invoice {3} and Account {4}”.format(row.idx, Platform.bold(Platform.format\_value(row.repair\_cost, mapping(“fieldtype” → “Curr ….

**Local steps**

- Set available\_amount from \_get\_unallocated\_repair\_cost(row.purchase\_invoice, row.expense\_account, exclude\_asset\_repair = self.name).
- Set row.repair\_cost from flt(row.repair\_cost, row.precision(“repair\_cost”)).
- If row.repair\_cost &gt; available\_amount.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Repair cost {1} exceeds available amount {2} for Purchase Invoice {3} and Account {4}”.format(row.idx, Platform.bold(Platform.format\_value(row.repair\_cost, mapping(“fie ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L569)

<a id="op-53b74969a6136c"></a>
### Asset Repair.add repair activity

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_add_repair_activity`

**Inputs** self, event.

**Local steps**

- Set subject from mapping(“Pending” → translated “Asset out of order due to Asset Repair {0}”, “Completed” → translated “Asset Repair {0} marked as Completed”, “Cancelled” → translated “Asset Repair {0} marked as Cancelled” ….
- Evaluate self.add\_asset\_activity(subject.format(get\_link\_to\_form(“Asset Repair”, self.name))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add asset activity](operations-016.md#op-c92660b800b533).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1386)

<a id="op-ef7d41413238d7"></a>
### Asset Repair.update status

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_update_status`

**Inputs** self.

**State and service calls** enqueue with update\_asset\_status\_after\_repair.

**Local steps**

- Evaluate Platform.enqueue(update\_asset\_status\_after\_repair, asset = self.asset, enqueue\_after\_commit = true, now = Platform.in\_test).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(update\_asset\_status\_after\_repair, asset = self.asset, enqueue\_after\_commit = true, now = Platform.in\_test).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L563)

<a id="op-17b4973b1359fe"></a>
### Asset Repair.calculate consumed items cost

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_calculate_consumed_items_cost`

**Inputs** self.

**Local steps**

- Set consumed\_items\_cost from 0.0.
- For each item in self.get(“stock\_items”).
  - Set item.total\_value from (flt(item.valuation\_rate) × flt(item.consumed\_quantity)).
  - Update consumed\_items\_cost using + item.total\_value.
- Set self.consumed\_items\_cost from consumed\_items\_cost.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L4250) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L548)

<a id="op-6d3c0219ad8754"></a>
### Asset Repair.calculate repair cost

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_calculate_repair_cost`

**Inputs** self.

**Local steps**

- Set self.repair\_cost from sum(generator of flt(pi.repair\_cost) for pi drawn from self.invoices).
  - Draw pi from self.invoices.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L4419) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L549)

<a id="op-620185a179e2dc"></a>
### Asset Repair.calculate total repair cost

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_calculate_total_repair_cost`

**Inputs** self.

**Local steps**

- Set self.total\_repair\_cost from (flt(self.repair\_cost) + flt(self.consumed\_items\_cost)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L4517) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L550)

<a id="op-3127ea74e8b093"></a>
### Asset Repair.on submit

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.decrease\_stock\_quantity().
- Evaluate self.set\_consumed\_items\_cost\_from\_stock\_entry().
- If self.get(“capitalize\_repair\_cost”).
  - Evaluate self.update\_asset\_value().
  - Evaluate self.set\_increase\_in\_asset\_life().
  - Set depreciation\_note from self.get\_depreciation\_note().
  - Evaluate reschedule\_depreciation(self.asset\_doc, depreciation\_note).
  - Evaluate self.make\_gl\_entries().
- Evaluate self.add\_asset\_activity().
- Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [decrease stock quantity](operations-016.md#op-75dbedd092916f), [set consumed items cost from stock entry](operations-016.md#op-9f1a3f8517af81), [update asset value](operations-016.md#op-4d0db7e646b0c0), [set increase in asset life](operations-016.md#op-99c6991ef0668f), [get depreciation note](operations-016.md#op-104de111f35f93), [make gl entries](operations-016.md#op-6e258ae8f78981), [add asset activity](operations-016.md#op-c92660b800b533), [update status](operations-015.md#op-ef7d41413238d7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L559)

<a id="op-27049791b78d9d"></a>
### Asset Repair.cancel sabb

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_cancel_stock_accounting_balance`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call db\_set on row · call cancel on doc.

**Local steps**

- For each row in self.stock\_items.
  - If sabb bound to row.serial\_and\_batch\_bundle.
    - Evaluate row.db\_set(“serial\_and\_batch\_bundle”, no value).
    - Set doc from Platform.get\_doc(“Serial and Batch Bundle”, sabb).
    - Evaluate doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L4822) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L551)

<a id="op-f620081124bf4e"></a>
### Asset Repair.on cancel

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Evaluate self.cancel\_stock\_entry().
- Set self.asset\_doc from Platform.get\_doc(“Asset”, self.asset).
- If self.get(“capitalize\_repair\_cost”).
  - Evaluate self.update\_asset\_value().
  - Evaluate self.make\_gl\_entries(cancel = true).
  - Evaluate self.set\_increase\_in\_asset\_life().
  - Set depreciation\_note from self.get\_depreciation\_note().
  - Evaluate reschedule\_depreciation(self.asset\_doc, depreciation\_note).
- Evaluate self.add\_asset\_activity().
- Evaluate self.cancel\_sabb().

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel stock entry](operations-015.md#op-29a7e304ec53ff), [update asset value](operations-016.md#op-4d0db7e646b0c0), [make gl entries](operations-016.md#op-6e258ae8f78981), [set increase in asset life](operations-016.md#op-99c6991ef0668f), [get depreciation note](operations-016.md#op-104de111f35f93), [add asset activity](operations-016.md#op-c92660b800b533), [cancel sabb](operations-015.md#op-27049791b78d9d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L558)

<a id="op-29a7e304ec53ff"></a>
### Asset Repair.cancel stock entry

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_cancel_stock_entry`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_value · resolve a document from “Stock Entry” via get\_doc.

**State and service calls** call cancel on stock\_entry.

**Local steps**

- Set stock\_entry from Platform.db.get\_value(“Stock Entry”, mapping(“asset\_repair” → self.name, “docstatus” → 1)).
- If stock\_entry.
  - Set stock\_entry from Platform.get\_doc(“Stock Entry”, stock\_entry).
  - Set stock\_entry.flags.ignore\_permissions from true.
  - Evaluate stock\_entry.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1387)
