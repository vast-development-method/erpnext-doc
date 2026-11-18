# Asset management · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset repair

[Record definition](../../../../data/record-types/asset_repair.json)

<a id="op-0c046c00170a19"></a>
### Asset Repair.after delete

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_after_delete`

**Inputs** self.

**Local steps**

- Evaluate self.close\_pending\_repair\_activity(“Deleted”).
- Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [close pending repair activity](operations-016.md#op-a647733ff96619), [update status](operations-015.md#op-ef7d41413238d7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L547)

<a id="op-0d92e808128fdd"></a>
### Asset Repair.on discard

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_on_discard`

**Inputs** self.

**Local steps**

- Evaluate self.close\_pending\_repair\_activity(“Discarded”).
- Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [close pending repair activity](operations-016.md#op-a647733ff96619), [update status](operations-015.md#op-ef7d41413238d7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1391)

<a id="op-a647733ff96619"></a>
### Asset Repair.close pending repair activity

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_close_pending_repair_activity`

**Inputs** self, event.

**Local steps**

- If self.repair\_status equals “Pending”.
  - Evaluate self.add\_repair\_activity(event).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add repair activity](operations-015.md#op-53b74969a6136c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1388)

<a id="op-0ab2e536e8614e"></a>
### Asset Repair.check repair status

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_check_repair_status`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only an Asset Repair with Repair Status Completed can be submitted.”.

**Local steps**

- If (self.repair\_status differs from “Completed” and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.repair\_status differs from “Completed” → self.docstatus equals 1.
  - Call the validation error handler Platform.throw(translated “Only an Asset Repair with Repair Status Completed can be submitted.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L552)

<a id="op-e79b343ceec1ed"></a>
### Asset Repair.set downtime

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_set_downtime`

**Inputs** self.

**Local steps**

- If (self.repair\_status equals “Completed” and self.failure\_date and self.completion\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.repair\_status equals “Completed” → self.failure\_date → self.completion\_date.
  - Set self.downtime from formatted text {get\_downtime(self.failure\_date, self.completion\_date)} Hrs.
- Otherwise.
  - Set self.downtime from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L5491) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L560)

<a id="op-4d0db7e646b0c0"></a>
### Asset Repair.update asset value

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_update_asset_value`

**Inputs** self.

**State and service calls** call save on self.asset\_doc.

**Local steps**

- Set total\_repair\_cost from self.total\_repair\_cost when self.docstatus equals 1, otherwise (negative 1 × self.total\_repair\_cost).
  - Value choice on self.docstatus equals 1 — true gives self.total\_repair\_cost, false gives (negative 1 × self.total\_repair\_cost).
- Update self.asset\_doc.total\_asset\_cost using + flt(total\_repair\_cost).
- Update self.asset\_doc.additional\_asset\_cost using + flt(total\_repair\_cost).
- If self.asset\_doc.calculate\_depreciation.
  - For each row in self.asset\_doc.finance\_books.
    - Update row.value\_after\_depreciation using + flt(total\_repair\_cost).
- Otherwise.
  - Evaluate self.update\_value\_after\_depreciation(total\_repair\_cost).
- Set self.asset\_doc.flags.ignore\_validate\_update\_after\_submit from true.
- Set self.asset\_doc.flags.ignore\_permissions from true.
- Evaluate self.asset\_doc.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update value after depreciation](operations-016.md#op-35e8064e86f7eb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L562)

<a id="op-35e8064e86f7eb"></a>
### Asset Repair.update value after depreciation

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_update_value_after_depreciation`

**Inputs** self, total\_repair\_cost.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If (self.docstatus equals 2 and not self.asset\_value\_updated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 2 → not self.asset\_value\_updated.
  - Return no value.
- Update self.asset\_doc.value\_after\_depreciation using + flt(total\_repair\_cost).
- If self.docstatus equals 1.
  - Evaluate self.db\_set(“asset\_value\_updated”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1394)

<a id="op-942d061bfce34e"></a>
### Asset Repair.get total value of stock consumed

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_get_total_value_of_stock_consumed`

**Inputs** self.

**Explicit results** sum(list of flt(item.total\_value) for item drawn from self.get(“stock\_items”)).

**Local steps**

- Return sum(list of flt(item.total\_value) for item drawn from self.get(“stock\_items”)).
  - Draw item from self.get(“stock\_items”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0328.json#L5915) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L556)

<a id="op-75dbedd092916f"></a>
### Asset Repair.decrease stock quantity

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_decrease_stock_quantity`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Stock Entry”, “stock\_entry\_type” → “Material Issue”, “company” → self.company, “asset\_repair” → self.name, …) via get\_doc.

**State and service calls** call insert on stock\_entry · call submit on stock\_entry.

**Explicit results** no value.

**Local steps**

- If not self.get(“stock\_items”).
  - Return no value.
- Set stock\_entry from Platform.get\_doc(mapping(“doctype” → “Stock Entry”, “stock\_entry\_type” → “Material Issue”, “company” → self.company, “asset\_repair” → self.name, …)).
- Set accounting\_dimensions from mapping(“cost\_center” → self.cost\_center, “project” → self.project, expand mapping of dimension → self.get(dimension) for dimension drawn from get\_accounting\_dimensions()).
  - Draw dimension from get\_accounting\_dimensions().
- For each stock\_item in self.get(“stock\_items”).
  - Evaluate self.validate\_serial\_no(stock\_item).
  - Evaluate stock\_entry.append(“items”, mapping(“s\_warehouse” → stock\_item.warehouse, “item\_code” → stock\_item.item\_code, “qty” → stock\_item.consumed\_quantity, “basic\_rate” → stock\_item.valuation\_rate, …)).
- Set stock\_entry.flags.ignore\_permissions from true.
- Evaluate stock\_entry.insert().
- Evaluate stock\_entry.submit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate serial no](operations-016.md#op-8ab62c5a4553fc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L553)

<a id="op-9f1a3f8517af81"></a>
### Asset Repair.set consumed items cost from stock entry

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_set_consumed_items_cost_from_stock_entry`

**Inputs** self.

**Record and data access** read “Stock Entry” via get\_value · read “Stock Entry Detail” via get\_all.

**State and service calls** call db\_update on stock\_item · call db\_set on self.

**Explicit results** no value.

**Local steps**

- If not self.get(“stock\_items”).
  - Return no value.
- Set stock\_entry from Platform.db.get\_value(“Stock Entry”, mapping(“asset\_repair” → self.name, “docstatus” → 1)).
- Set stock\_entry\_items from Platform.get\_all(“Stock Entry Detail”, filters = mapping(“parent” → stock\_entry), fields = list(“valuation\_rate”, “amount”), order\_by = “idx”).
- For each tuple(stock\_item, stock\_entry\_item) in zip(self.stock\_items, stock\_entry\_items, strict = true).
  - Set stock\_item.valuation\_rate from stock\_entry\_item.valuation\_rate.
  - Set stock\_item.total\_value from stock\_entry\_item.amount.
  - Evaluate stock\_item.db\_update().
- Set consumed\_items\_cost from self.get\_total\_value\_of\_stock\_consumed().
- Evaluate self.db\_set(mapping(“consumed\_items\_cost” → consumed\_items\_cost, “total\_repair\_cost” → (flt(self.repair\_cost) + consumed\_items\_cost))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get total value of stock consumed](operations-016.md#op-942d061bfce34e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1393)

<a id="op-8ab62c5a4553fc"></a>
### Asset Repair.validate serial no

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_validate_serial_number`

**Inputs** self, stock\_item.

**Record and data access** read “Item” via get\_cached\_value.

**State and service calls** request set\_value on “Serial and Batch Bundle”.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- If (not stock\_item.serial\_and\_batch\_bundle and Platform.get\_cached\_value(“Item”, stock\_item.item\_code, “has\_serial\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not stock\_item.serial\_and\_batch\_bundle → Platform.get\_cached\_value(“Item”, stock\_item.item\_code, “has\_serial\_no”).
  - Set msg from formatted text Serial No Bundle is mandatory for Item {stock\_item.item\_code}.
  - Call the validation error handler Platform.throw(translated msg, title = translated “Missing Serial No Bundle”).
- If stock\_item.serial\_and\_batch\_bundle.
  - Set values\_to\_update from mapping(“type\_of\_transaction” → “Outward”, “voucher\_type” → “Stock Entry”).
  - Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, stock\_item.serial\_and\_batch\_bundle, values\_to\_update).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, stock\_item.item\_code, “has\_serial\_no”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L572)

<a id="op-6e258ae8f78981"></a>
### Asset Repair.make gl entries

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_make_general_ledger_entries`

**Inputs** self, cancel = false.

**Local steps**

- If cancel.
  - Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”).
- If flt(self.total\_repair\_cost) &gt; 0.
  - Set gl\_entries from self.get\_gl\_entries().
  - Evaluate make\_gl\_entries(gl\_entries, cancel).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl entries](operations-016.md#op-7f00a44f19a3d1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L557)

<a id="op-7f00a44f19a3d1"></a>
### Asset Repair.get gl entries

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_get_general_ledger_entries`

**Inputs** self.

**Explicit results** gl\_entries.

**Local steps**

- Set gl\_entries from list().
- Set fixed\_asset\_account from get\_asset\_account(“fixed\_asset\_account”, asset = self.asset, company = self.company).
- Evaluate self.get\_gl\_entries\_for\_repair\_cost(gl\_entries, fixed\_asset\_account).
- Evaluate self.get\_gl\_entries\_for\_consumed\_items(gl\_entries, fixed\_asset\_account).
- Return gl\_entries.

**Methods declared on this owner** [get gl entries for repair cost](operations-016.md#op-36594119febb08), [get gl entries for consumed items](operations-016.md#op-b22f959c3a55ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L555)

<a id="op-36594119febb08"></a>
### Asset Repair.get gl entries for repair cost

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_get_gl_entries_for_repair_cost`

**Inputs** self, gl\_entries, fixed\_asset\_account.

**Explicit results** no value.

**Local steps**

- If flt(self.repair\_cost) ≤ 0.
  - Return no value.
- Set debit\_against\_account from set().
- For each pi in self.invoices.
  - Evaluate debit\_against\_account.add(pi.expense\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → pi.expense\_account, “credit” → pi.repair\_cost, “credit\_in\_account\_currency” → pi.repair\_cost, “against” → fixed\_asset\_account, …), item = self)).
- Set debit\_against\_account from “, ”.join(debit\_against\_account).
- Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → fixed\_asset\_account, “debit” → self.repair\_cost, “debit\_in\_account\_currency” → self.repair\_cost, “against” → debit\_against\_account, …), item = self)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1390)

<a id="op-b22f959c3a55ff"></a>
### Asset Repair.get gl entries for consumed items

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_assetrepair_get_gl_entries_for_consumed_items`

**Inputs** self, gl\_entries, fixed\_asset\_account.

**Record and data access** read “Stock Entry” via get\_value · read “Stock Entry Detail” via get\_all · read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please set default Expense Account in Company {0}”.format(self.company).

**Local steps**

- If not self.get(“stock\_items”).
  - Return no value.
- Set stock\_entry\_name from Platform.db.get\_value(“Stock Entry”, mapping(“asset\_repair” → self.name), “name”).
- Set stock\_entry\_items from Platform.get\_all(“Stock Entry Detail”, filters = mapping(“parent” → stock\_entry\_name), fields = list(“expense\_account”, “amount”)).
- Set default\_expense\_account from no value.
- If not Enterprise.is\_perpetual\_inventory\_enabled(self.company).
  - Set default\_expense\_account from Platform.get\_cached\_value(“Company”, self.company, “default\_expense\_account”).
  - If not default\_expense\_account.
    - Call the validation error handler Platform.throw(translated “Please set default Expense Account in Company {0}”.format(self.company)).
- For each item in stock\_entry\_items.
  - If flt(item.amount) &gt; 0.
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → (item.expense\_account or default\_expense\_account), “credit” → item.amount, “credit\_in\_account\_currency” → item.amount, “against” → fixed\_asset\_account ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.expense\_account → default\_expense\_account.
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → fixed\_asset\_account, “debit” → item.amount, “debit\_in\_account\_currency” → item.amount, “against” → (item.expense\_account or default\_expense\_account),  ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.expense\_account → default\_expense\_account.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_expense\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1389)

<a id="op-99c6991ef0668f"></a>
### Asset Repair.set increase in asset life

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_set_increase_in_asset_life`

**Inputs** self.

**State and service calls** call db\_update on row.

**Local steps**

- If (self.asset\_doc.calculate\_depreciation and cint(self.increase\_in\_asset\_life) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.asset\_doc.calculate\_depreciation → cint(self.increase\_in\_asset\_life) &gt; 0.
  - For each row in self.asset\_doc.finance\_books.
    - Set row.increase\_in\_asset\_life from (cint(row.increase\_in\_asset\_life) + (cint(self.increase\_in\_asset\_life) × 1 when self.docstatus equals 1, otherwise negative 1)).
      - Value choice on self.docstatus equals 1 — true gives 1, false gives negative 1.
    - Evaluate row.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0329.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L561)

<a id="op-104de111f35f93"></a>
### Asset Repair.get depreciation note

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_get_depreciation_note`

**Inputs** self.

**Explicit results** translated “This schedule was created when Asset {0} was repaired through Asset Repair {1}.”.format(get\_link\_to\_form(self.asset\_doc.doctype, self.asset\_doc.name), get\_link\_to\_form(self.doctype, self.name)).

**Local steps**

- Return translated “This schedule was created when Asset {0} was repaired through Asset Repair {1}.”.format(get\_link\_to\_form(self.asset\_doc.doctype, self.asset\_doc.name), get\_link\_to\_form(self.doctype, self.name)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0329.json#L235) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L554)

<a id="op-c92660b800b533"></a>
### Asset Repair.add asset activity

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_asset_repair_add_asset_activity`

**Inputs** self, subject = no value.

**Local steps**

- If not subject.
  - Set subject from translated “Asset updated due to Asset Repair {0} {1}.”.format(get\_link\_to\_form(self.doctype, self.name), “submission” when self.docstatus equals 1, otherwise “cancellation”).
    - Value choice on self.docstatus equals 1 — true gives “submission”, false gives “cancellation”.
- Evaluate add\_asset\_activity(self.asset, subject).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0329.json#L371) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L546)

<a id="op-fb83a84775d073"></a>
### Update asset status after repair

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_update_asset_status_after_repair`

**Inputs** asset.

**Declared result** no value.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Evaluate Platform.get\_doc(“Asset”, asset, for\_update = true).set\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1397)

<a id="op-ea410f7ee32814"></a>
### Check asset repair access

`operation_enterprise_binding_enterprise_assets_doctype_asset_repair_asset_repair_check_asset_repair_access`

**Inputs** company = no value.

**Local steps**

- Evaluate Platform.has\_permission(“Asset Repair”, throw = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Asset Repair”, throw = true).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1395)

<a id="op-f7bb45f4e3d040"></a>
### Get downtime

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_downtime`

**Inputs** failure\_date, completion\_date.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** round(downtime, 2).

**Local steps**

- Set downtime from time\_diff\_in\_hours(completion\_date, failure\_date).
- Return round(downtime, 2).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L574)

<a id="op-3a67521b6a7fee"></a>
### Get purchase invoice

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_purchase_invoice`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Explicit results** query.run(as\_list = 1).

**Local steps**

- Evaluate check\_asset\_repair\_access(filters.get(“company”) when isinstance(filters, dict), otherwise no value).
  - Value choice on isinstance(filters, dict) — true gives filters.get(“company”), false gives no value.
- Set pi from DocType(“Purchase Invoice”).
- Set pi\_item from DocType(“Purchase Invoice Item”).
- Set item from DocType(“Item”).
- Set query from nested operand in the contract(nested operand in the contract).select(pi.name).distinct().where((((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the c ….
- If txt.
  - Set query from query.where(pi.name.like(formatted text %{txt}%)).
- Return query.run(as\_list = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L577)

<a id="op-7c3e4813d2d1c6"></a>
### Get expense accounts

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_expense_accounts`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Purchase Invoice” via get\_value.

**Explicit results** list() · list of list(account) for account drawn from expense\_accounts.

**Local steps**

- Set purchase\_invoice from filters.get(“purchase\_invoice”).
- If (not isinstance(purchase\_invoice, str) or not purchase\_invoice).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(purchase\_invoice, str) → not purchase\_invoice.
  - Return list().
- Set company from Platform.db.get\_value(“Purchase Invoice”, purchase\_invoice, “company”).
- If not company.
  - Return list().
- Evaluate check\_asset\_repair\_access(company).
- Set expense\_accounts from \_get\_expense\_accounts\_for\_purchase\_invoice(purchase\_invoice).
- Return list of list(account) for account drawn from expense\_accounts.
  - Draw account from expense\_accounts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L575)

<a id="op-67aa20681d79ef"></a>
### Get expense accounts for purchase invoice

`operation_enterprise_assets_record_definitions_asset_repair_business_behavior_get_expense_accounts_for_purchase_invoice`

**Inputs** purchase\_invoice.

**Declared result** list at str.

**Record and data access** read “Purchase Invoice Item” via get\_all · read “Item” via get\_all.

**Explicit results** list() · list(expense\_accounts).

**Local steps**

- Set pi\_items from Platform.db.get\_all(“Purchase Invoice Item”, filters = mapping(“parent” → purchase\_invoice), fields = list(“item\_code”, “expense\_account”, “is\_fixed\_asset”)).
- If not pi\_items.
  - Return list().
- Set item\_codes from set of item.item\_code for item drawn from pi\_items where item.item\_code.
  - Draw item from pi\_items, keep a combination only if (item.item\_code).
- Set stock\_items from set().
- If item\_codes.
  - Set stock\_items from set(Platform.db.get\_all(“Item”, filters = mapping(“name” → list(“in”, list(item\_codes)), “is\_stock\_item” → 1), pluck = “name”)).
- Set expense\_accounts from set().
- For each item in pi\_items.
  - If (item.item\_code and item.item\_code belongs to stock\_items).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code → item.item\_code belongs to stock\_items.
    - Continue with the next iteration or loop test.
  - If item.is\_fixed\_asset.
    - Continue with the next iteration or loop test.
  - If item.expense\_account.
    - Evaluate expense\_accounts.add(item.expense\_account).
- Return list(expense\_accounts).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0329.json#L1610) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L576)
