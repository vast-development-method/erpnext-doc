# Shared transaction rules · operations 28

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Stock controller

<a id="op-5de7e854dbe1bc"></a>
### Create item wise repost entries

`operation_enterprise_controllers_stock_controller_business_behavior_create_item_wise_repost_entries`

**Inputs** voucher\_type, voucher\_no, allow\_zero\_rate = false, via\_landed\_cost\_voucher = false.

**State and service calls** request new\_doc for “Repost Item Valuation” · call submit on repost\_entry.

**Explicit results** repost\_entries.

**Local steps**

- Set stock\_ledger\_entries from get\_items\_to\_be\_repost(voucher\_type, voucher\_no).
- Set distinct\_item\_warehouses from set().
- Set repost\_entries from list().
- For each sle in stock\_ledger\_entries.
  - Set item\_wh from tuple(sle.item\_code, sle.warehouse).
  - If item\_wh belongs to distinct\_item\_warehouses.
    - Continue with the next iteration or loop test.
  - Evaluate distinct\_item\_warehouses.add(item\_wh).
  - Set repost\_entry from Platform.new\_doc(“Repost Item Valuation”).
  - Set repost\_entry.based\_on from “Item and Warehouse”.
  - Set repost\_entry.item\_code from sle.item\_code.
  - Set repost\_entry.warehouse from sle.warehouse.
  - Set repost\_entry.posting\_date from sle.posting\_date.
  - Set repost\_entry.posting\_time from sle.posting\_time.
  - Set repost\_entry.allow\_zero\_rate from allow\_zero\_rate.
  - Set repost\_entry.flags.ignore\_links from true.
  - Set repost\_entry.flags.ignore\_permissions from true.
  - Set repost\_entry.via\_landed\_cost\_voucher from via\_landed\_cost\_voucher.
  - Evaluate repost\_entry.submit().
  - Evaluate repost\_entries.append(repost\_entry).
- Return repost\_entries.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L937) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L616)

<a id="op-b4cc76ace5a604"></a>
### Make bundle for material transfer

`operation_enterprise_controllers_stock_controller_business_behavior_make_bundle_for_material_transfer`

**Inputs** remaining named values kwargs.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** request copy\_doc for bundle\_doc · call save on bundle\_doc · call submit on bundle\_doc.

**Explicit results** bundle\_doc.name.

**Local steps**

- If isinstance(kwargs, dict).
  - Set kwargs from Platform.\_dict(kwargs).
- Set bundle\_doc from Platform.get\_doc(“Serial and Batch Bundle”, kwargs.serial\_and\_batch\_bundle).
- If not kwargs.type\_of\_transaction.
  - Set kwargs.type\_of\_transaction from “Inward”.
- Set bundle\_doc from Platform.copy\_doc(bundle\_doc).
- Set bundle\_doc.docstatus from 0.
- Set bundle\_doc.warehouse from kwargs.warehouse.
- Set bundle\_doc.type\_of\_transaction from kwargs.type\_of\_transaction.
- Set bundle\_doc.voucher\_type from kwargs.voucher\_type.
- Set bundle\_doc.voucher\_no from empty text when (kwargs.is\_new or kwargs.docstatus equals 2), otherwise kwargs.voucher\_no.
  - Value choice on (kwargs.is\_new or kwargs.docstatus equals 2) — true gives empty text, false gives kwargs.voucher\_no.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kwargs.is\_new → kwargs.docstatus equals 2.
- Set bundle\_doc.is\_cancelled from 0.
- If kwargs.include\_bundle.
  - For each entry in Platform.get\_doc(“Serial and Batch Bundle”, kwargs.include\_bundle).entries.
    - Evaluate bundle\_doc.append(“entries”, entry.as\_dict(no\_default\_fields = true)).
- If kwargs.exclude\_serial\_nos.
  - Set keep from list of row for row drawn from bundle\_doc.entries where row.serial\_no does not belong to set(kwargs.exclude\_serial\_nos).
    - Draw row from bundle\_doc.entries, keep a combination only if (row.serial\_no does not belong to set(kwargs.exclude\_serial\_nos)).
  - Set bundle\_doc.entries from keep.
  - For each tuple(idx, row) in enumerate(keep, start = 1).
    - Set row.idx from idx.
- Set qty from 0.
- If (len(bundle\_doc.entries) equals 1 and abs(flt(kwargs.qty)) &lt; abs(flt(bundle\_doc.total\_qty)) and not bundle\_doc.has\_serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(bundle\_doc.entries) equals 1 → abs(flt(kwargs.qty)) &lt; abs(flt(bundle\_doc.total\_qty)) → not bundle\_doc.has\_serial\_no.
  - Set qty from kwargs.qty.
- If (kwargs.total\_qty and not bundle\_doc.has\_serial\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in kwargs.total\_qty → not bundle\_doc.has\_serial\_no.
  - Evaluate set\_entries\_total\_qty(bundle\_doc.entries, kwargs.total\_qty).
- For each row in bundle\_doc.entries.
  - Set row.is\_outward from 0.
  - Set row.qty from abs((qty or row.qty)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in qty → row.qty.
  - Set row.stock\_value\_difference from abs(row.stock\_value\_difference).
  - If kwargs.type\_of\_transaction equals “Outward”.
    - Update row.qty using × negative 1.
    - Update row.stock\_value\_difference using × negative 1.
    - Set row.is\_outward from 1.
  - Set row.warehouse from kwargs.warehouse.
  - Set row.posting\_datetime from bundle\_doc.posting\_datetime.
  - Set row.voucher\_type from bundle\_doc.voucher\_type.
  - Set row.voucher\_no from bundle\_doc.voucher\_no.
  - Set row.voucher\_detail\_no from bundle\_doc.voucher\_detail\_no.
  - Set row.type\_of\_transaction from bundle\_doc.type\_of\_transaction.
  - Set row.item\_code from bundle\_doc.item\_code.
- Evaluate bundle\_doc.set\_incoming\_rate().
- Evaluate bundle\_doc.calculate\_qty\_and\_amount().
- Set bundle\_doc.flags.ignore\_permissions from true.
- Set bundle\_doc.flags.ignore\_validate from true.
- If kwargs.do\_not\_submit.
  - Evaluate bundle\_doc.save(ignore\_permissions = true).
- Otherwise.
  - Evaluate bundle\_doc.submit().
  - If kwargs.docstatus differs from 2.
    - Evaluate bundle\_doc.check\_future\_entries\_exists().
- Return bundle\_doc.name.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L625)

<a id="op-05b659d212e344"></a>
### New reservation transfer

`operation_enterprise_binding_enterprise_controllers_stock_controller_new_reservation_transfer`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(qty = 0, serial\_nos = set(), batch\_qty = defaultdict(float)).

**Local steps**

- Return Platform.\_dict(qty = 0, serial\_nos = set(), batch\_qty = defaultdict(float)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L365)

<a id="op-a637f129655805"></a>
### Add transfer to reservation

`operation_enterprise_binding_enterprise_controllers_stock_controller_add_transfer_to_reservation`

**Inputs** sre\_doc, transfer.

**Declared result** no value.

**Local steps**

- If sre\_doc.reservation\_based\_on differs from “Serial and Batch”.
  - Set qty from min((flt(sre\_doc.reserved\_qty) − flt(sre\_doc.transferred\_qty)), transfer.qty).
- Otherwise.
  - Set qty from 0.
  - For each entry in sre\_doc.sb\_entries.
    - If sre\_doc.has\_serial\_no.
      - Set entry\_qty from 0.
      - If (not flt(entry.delivered\_qty) and entry.serial\_no belongs to transfer.serial\_nos).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(entry.delivered\_qty) → entry.serial\_no belongs to transfer.serial\_nos.
        - Set entry\_qty from 1.
        - Evaluate transfer.serial\_nos.discard(entry.serial\_no).
    - Otherwise.
      - Set entry\_qty from min((flt(entry.qty) − flt(entry.delivered\_qty)), transfer.batch\_qty at entry.batch\_no).
      - Update transfer.batch\_qty at entry.batch\_no using − entry\_qty.
    - Set entry.delivered\_qty from flt((flt(entry.delivered\_qty) + entry\_qty), entry.precision(“delivered\_qty”)).
    - Update qty using + entry\_qty.
- Update transfer.qty using − qty.
- Set sre\_doc.transferred\_qty from flt((flt(sre\_doc.transferred\_qty) + qty), sre\_doc.precision(“transferred\_qty”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L354)

<a id="op-9a01c7e9c1bb67"></a>
### Set entries total qty

`operation_enterprise_binding_enterprise_controllers_stock_controller_set_entries_total_qty`

**Inputs** entries, total\_qty.

**Local steps**

- Set entries at negative 1.qty from (abs(flt(total\_qty)) − sum(generator of abs(flt(row.qty)) for row drawn from entries at slice no value to negative 1)).
  - Draw row from entries at slice no value to negative 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L366)

<a id="op-9404a10cb9b77c"></a>
### Get item wise inventory account map

`operation_enterprise_controllers_stock_controller_business_behavior_get_item_wise_inventory_account_map`

**Inputs** rows, company.

**Explicit results** inventory\_map.

**Local steps**

- Set inventory\_map from Platform.\_dict().
- For each row in rows.
  - Set item\_code from row.rm\_item\_code when (hasattr(row, “rm\_item\_code”) and row.rm\_item\_code), otherwise row.item\_code.
    - Value choice on (hasattr(row, “rm\_item\_code”) and row.rm\_item\_code) — true gives row.rm\_item\_code, false gives row.item\_code.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(row, “rm\_item\_code”) → row.rm\_item\_code.
  - If not item\_code.
    - Continue with the next iteration or loop test.
  - If inventory\_map.get(item\_code).
    - Continue with the next iteration or loop test.
  - Set item\_defaults from get\_item\_defaults(item\_code, company).
  - If item\_defaults.default\_inventory\_account.
    - Set inventory\_map at item\_code from Platform.\_dict(mapping(“account” → item\_defaults.default\_inventory\_account, “account\_currency” → item\_defaults.inventory\_account\_currency)).
  - If not inventory\_map.get(item\_code).
    - Set item\_group\_defaults from get\_item\_group\_defaults(item\_code, company).
    - If item\_group\_defaults.default\_inventory\_account.
      - Set inventory\_map at item\_code from Platform.\_dict(mapping(“account” → item\_group\_defaults.default\_inventory\_account, “account\_currency” → item\_group\_defaults.inventory\_account\_currency)).
  - If not inventory\_map.get(item\_code).
    - Set brand\_defaults from get\_brand\_defaults(item\_code, company).
    - If brand\_defaults.default\_inventory\_account.
      - Set inventory\_map at item\_code from Platform.\_dict(mapping(“account” → brand\_defaults.default\_inventory\_account, “account\_currency” → brand\_defaults.inventory\_account\_currency)).
- Return inventory\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L3862) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L621)

<a id="op-9c9e8eedc526b1"></a>
### Get expenses added to stock accounts

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_expenses_added_to_stock_accounts`

**Inputs** item\_code, company.

**Wrappers, in declaration order** Platform.request\_cache.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** details.

**Local steps**

- Bind dependencies get\_brand\_defaults.
- Bind dependencies get\_item\_group\_defaults.
- Bind dependencies get\_item\_defaults.
- Set fields from list(“expenses\_added\_to\_stock\_account”, “expenses\_added\_to\_stock\_contra\_account”).
- Set defaults from get\_item\_defaults(item\_code, company).
- Set details from Platform.\_dict(mapping of field → defaults.get(field) for field drawn from fields).
  - Draw field from fields.
- If not details.expenses\_added\_to\_stock\_account.
  - Set details from get\_item\_group\_defaults(item\_code, company).
- If not details.expenses\_added\_to\_stock\_account.
  - Set details from get\_brand\_defaults(item\_code, company).
- Set details from Platform.\_dict(mapping of field → details.get(field) for field drawn from fields).
  - Draw field from fields.
- For each field in fields.
  - If not details.get(field).
    - Set details at field from Platform.get\_cached\_value(“Company”, company, field).
- Return details.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, field).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L358)

<a id="op-212ba8605a39ec"></a>
### Get unusable outward bundle batches

`operation_enterprise_binding_enterprise_controllers_stock_controller_get_unusable_outward_bundle_batches`

**Inputs** bundles, posting\_date.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“bundle”), entry.batch\_no, batch.expiry\_date, batch.disabled).where(((nested operand in the contract ….

**Local steps**

- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set batch from Platform.qb.DocType(“Batch”).
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“bundle”), entry.batch\_no, batch.expiry\_date, batch.disabled).where(((nested operand in the contract ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L362)

<a id="op-145b42f6d2eaeb"></a>
### Unusable batch condition

`operation_enterprise_binding_enterprise_controllers_stock_controller_unusable_batch_condition`

**Inputs** batch, posting\_date.

**Explicit results** batch.disabled equals 1 · (batch.expiry\_date &lt; getdate(posting\_date) bitwise or batch.disabled equals 1).

**Local steps**

- If not posting\_date.
  - Return batch.disabled equals 1.
- Return (batch.expiry\_date &lt; getdate(posting\_date) bitwise or batch.disabled equals 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L426)

<a id="op-428eef2e32ca34"></a>
### Add picked batches

`operation_enterprise_binding_enterprise_controllers_stock_controller_add_picked_batches`

**Inputs** picked\_batches, entries.

**Local steps**

- For each entry in entries.
  - If entry.batch\_no.
    - Set picked from picked\_batches.setdefault(tuple(entry.batch\_no, entry.warehouse), Platform.\_dict(batch\_no = entry.batch\_no, warehouse = entry.warehouse, qty = 0)).
    - Update picked.qty using + entry.qty.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L353)

## Service · Subcontracting controller

<a id="op-99b27208a281ae"></a>
### Subcontracting Controller.initialize

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- If self.get(“is\_old\_subcontracting\_flow”).
  - Set self.subcontract\_data from Platform.\_dict(mapping(“order\_doctype” → “Purchase Order”, “order\_field” → “purchase\_order”, “rm\_detail\_field” → “po\_detail”, “receipt\_supplied\_items\_field” → “Purchase Receipt Item Supplied”, …)).
- Otherwise.
  - If self.doctype equals “Subcontracting Inward Order”.
    - Set self.subcontract\_data from Platform.\_dict(mapping(“order\_doctype” → “Subcontracting Inward Order”, “order\_field” → “subcontracting\_inward\_order”, “rm\_detail\_field” → “scio\_detail”)).
  - Otherwise.
    - Set self.subcontract\_data from Platform.\_dict(mapping(“order\_doctype” → “Subcontracting Order”, “order\_field” → “subcontracting\_order”, “rm\_detail\_field” → “sco\_rm\_detail”, “receipt\_supplied\_items\_field” → “Subcontracting Receipt Suppli ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L697)

<a id="op-8e7bb84d7b301b"></a>
### Subcontracting Controller.before validate

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_before_validate`

**Inputs** self.

**Local steps**

- If self.doctype belongs to list(“Subcontracting Order”, “Subcontracting Inward Order”, “Subcontracting Receipt”).
  - Evaluate self.remove\_empty\_rows().
  - Evaluate self.set\_items\_conversion\_factor().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove empty rows](operations-029.md#op-08cdfc9b892346), [set items conversion factor](operations-029.md#op-83e45f2564b86d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0392.json#L4795) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1000) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L677)

<a id="op-d5ff73c68ac52c"></a>
### Subcontracting Controller.validate

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_validate`

**Inputs** self.

**Local steps**

- If self.doctype belongs to list(“Subcontracting Order”, “Subcontracting Receipt”, “Subcontracting Inward Order”).
  - Evaluate self.validate\_items().
  - Evaluate self.create\_raw\_materials\_supplied\_or\_received(raw\_material\_table = “supplied\_items” when self.doctype differs from “Subcontracting Inward Order”, otherwise “received\_items”).
    - Value choice on self.doctype differs from “Subcontracting Inward Order” — true gives “supplied\_items”, false gives “received\_items”.
  - Evaluate self.validate\_company\_of\_warehouses().
  - Evaluate self.set\_valuation\_rate\_for\_rm().
- Otherwise.
  - Evaluate super().validate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate items](operations-029.md#op-5dec11ef964883), [create raw materials supplied or received](operations-031.md#op-b358c7a6655104), [validate company of warehouses](operations-028.md#op-83dd3edeeaaf15), [set valuation rate for rm](operations-028.md#op-44949d9123154f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1052) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L729)

<a id="op-83dd3edeeaaf15"></a>
### Subcontracting Controller.validate company of warehouses

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_validate_company_of_warehouses`

**Inputs** self.

**Local steps**

- Set warehouses from set of self.get(df.fieldname) for df drawn from self.meta.get\_link\_fields() where df.options equals “Warehouse”.
  - Draw df from self.meta.get\_link\_fields(), keep a combination only if (df.options equals “Warehouse”).
- For each table\_field in self.meta.get\_table\_fields().
  - Set child\_meta from Platform.get\_meta(table\_field.options).
  - Set fieldnames from list of df.fieldname for df drawn from child\_meta.get\_link\_fields() where df.options equals “Warehouse”.
    - Draw df from child\_meta.get\_link\_fields(), keep a combination only if (df.options equals “Warehouse”).
  - For each row in self.get(table\_field.fieldname).
    - Evaluate warehouses.update(generator of row.get(fieldname) for fieldname drawn from fieldnames).
      - Draw fieldname from fieldnames.
- For each warehouse in warehouses.
  - If warehouse.
    - Evaluate validate\_warehouse\_company(warehouse, self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L444)

<a id="op-44949d9123154f"></a>
### Subcontracting Controller.set valuation rate for rm

`operation_enterprise_controllers_subcontracting_controller_business_behavior_subcontracting_controller_set_valuation_rate_for_raw_material`

**Inputs** self.

**Local steps**

- Set rate\_changed from false.
- If self.doctype equals “Subcontracting Receipt”.
  - Set precision from Platform.get\_precision(“Subcontracting Receipt Supplied Item”, “rate”).
  - Set rates from self.get\_supplied\_item\_rates(self.supplied\_items).
  - For each tuple(row, rate) in zip(self.supplied\_items, rates, strict = true).
    - If flt(rate, precision) differs from flt(row.rate, precision).
      - Set row.rate from rate.
      - Set row.amount from (flt(row.consumed\_qty) × flt(rate)).
      - Set rate\_changed from true.
- If rate\_changed.
  - Evaluate self.calculate\_items\_qty\_and\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get supplied item rates](operations-028.md#op-b1d2e8858f3c83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1043) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L720)

<a id="op-b1d2e8858f3c83"></a>
### Subcontracting Controller.get supplied item rates

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_supplied_item_rates`

**Inputs** self, rows.

**Explicit results** rates.

**Local steps**

- Set rejected\_return\_rows from self.get\_rejected\_return\_rows().
- Set return\_rates from self.get\_consumed\_rates\_for\_return().
- Set original\_rows from mapping of item.name → item.subcontracting\_receipt\_item for item drawn from self.items.
  - Draw item from self.items.
- Set consumed\_serial\_batches from self.get\_consumed\_serial\_batches().
- Set bundle\_entries from self.get\_bundle\_entries(rows) when consumed\_serial\_batches, otherwise mapping().
  - Value choice on consumed\_serial\_batches — true gives self.get\_bundle\_entries(rows), false gives mapping().
- Set rates from list().
- For each row in rows.
  - Set return\_rate from no value.
  - If self.is\_return.
    - Set key from tuple(original\_rows.get(row.reference\_name), row.rm\_item\_code).
    - Set return\_rate from self.get\_serial\_batch\_return\_rate(row, consumed\_serial\_batches.get(key, mapping()), bundle\_entries).
    - If return\_rate is identical to no value.
      - Set return\_rate from return\_rates.get(key).
  - If row.reference\_name belongs to rejected\_return\_rows.
    - Evaluate rates.append(0.0).
  - Otherwise.
    - If return\_rate is distinct from no value.
      - Evaluate rates.append(return\_rate).
    - Otherwise.
      - Evaluate rates.append(\_get\_incoming\_rate(self.get\_supplied\_item\_rate\_args(row))).
- Return rates.

**Methods declared on this owner** [get rejected return rows](operations-029.md#op-c9c5b5813a25c1), [get consumed rates for return](operations-028.md#op-d1b99387ebd392), [get consumed serial batches](operations-029.md#op-4784b039e0b81d), [get bundle entries](operations-031.md#op-35127706a964f2), [get serial batch return rate](operations-028.md#op-bc9cd9d2986048), [get supplied item rate args](operations-028.md#op-b6c74f327e9d8a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L441)

<a id="op-bc9cd9d2986048"></a>
### Subcontracting Controller.get serial batch return rate

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_serial_batch_return_rate`

**Inputs** self, row, identities, bundle\_entries.

**Explicit results** no value · flt((sum(generator of (rate × qty) for tuple(rate, qty) drawn from returned) ÷ total\_qty), row.precision(“rate”)).

**Local steps**

- If row.serial\_and\_batch\_bundle.
  - Set returned from list of tuple(identities.get(tuple(entry.serial\_no, entry.batch\_no)), abs(flt(entry.qty))) for entry drawn from bundle\_entries.get(row.serial\_and\_batch\_bundle, list()).
    - Draw entry from bundle\_entries.get(row.serial\_and\_batch\_bundle, list()).
- Otherwise.
  - Set serial\_nos from set of serial\_no.casefold() for serial\_no drawn from get\_serial\_nos(row.serial\_no).
    - Draw serial\_no from get\_serial\_nos(row.serial\_no).
  - Set returned from list of tuple(identity, 1) for identity drawn from identities.values() where cstr(nested operand in the contract.serial\_number).casefold() belongs to serial\_nos when serial\_nos, otherwise (row.batch\_no and ….
    - Draw identity from identities.values(), keep a combination only if (cstr(identity.serial\_number).casefold() belongs to serial\_nos when serial\_nos, otherwise (row.batch\_no and identity.batch\_no equals row.batch\_no)).
    - Value choice on serial\_nos — true gives cstr(identity.serial\_number).casefold() belongs to serial\_nos, false gives (row.batch\_no and identity.batch\_no equals row.batch\_no).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.batch\_no → identity.batch\_no equals row.batch\_no.
- Set returned from list of tuple(identity.rate, qty) for tuple(identity, qty) drawn from returned where identity.
  - Draw tuple(identity, qty) from returned, keep a combination only if (identity).
- Set total\_qty from sum(generator of qty for tuple(\_rate, qty) drawn from returned).
  - Draw tuple(\_rate, qty) from returned.
- If not total\_qty.
  - Return no value.
- Return flt((sum(generator of (rate × qty) for tuple(rate, qty) drawn from returned) ÷ total\_qty), row.precision(“rate”)).
  - Draw tuple(rate, qty) from returned.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L439)

<a id="op-b6c74f327e9d8a"></a>
### Subcontracting Controller.get supplied item rate args

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_supplied_item_rate_args`

**Inputs** self, row.

**Explicit results** Platform.\_dict(mapping(“item\_code” → row.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).

**Local steps**

- Return Platform.\_dict(mapping(“item\_code” → row.rm\_item\_code, “warehouse” → self.supplier\_warehouse, “posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, …)).
  - Value choice on not self.is\_return — true gives negative 1, false gives 1.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L440)

<a id="op-d1b99387ebd392"></a>
### Subcontracting Controller.get consumed rates for return

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_consumed_rates_for_return`

**Inputs** self.

**Explicit results** mapping() · mapping of tuple(row.reference\_name, row.rm\_item\_code) → flt(row.rate) for row drawn from rows.

**Local steps**

- If not (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Return mapping().
- Set supplied\_item from Platform.qb.DocType(“Subcontracting Receipt Supplied Item”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bi ….
- Return mapping of tuple(row.reference\_name, row.rm\_item\_code) → flt(row.rate) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L430)

<a id="op-a9d0e47e1ced68"></a>
### Subcontracting Controller.is subcontracting receipt return

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_is_subcontracting_receipt_return`

**Inputs** self.

**Explicit results** (self.doctype equals “Subcontracting Receipt” and self.is\_return and self.return\_against).

**Local steps**

- Return (self.doctype equals “Subcontracting Receipt” and self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Subcontracting Receipt” → self.is\_return → self.return\_against.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L442)

<a id="op-c5d16d8bcd70f4"></a>
### Subcontracting Controller.get returnable raw materials

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_returnable_raw_materials`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Subcontracting Receipt Item” via get\_all · read “Subcontracting Receipt Supplied Item” via get\_all.

**Explicit results** mapping() · materials.

**Local steps**

- If not self.is\_subcontracting\_receipt\_return().
  - Return mapping().
- Set received\_qty from dict(Platform.get\_all(“Subcontracting Receipt Item”, filters = mapping(“parent” → self.return\_against), fields = list(“name”, “received\_qty”), as\_list = true)).
- Set tuple(returned\_fg\_qty, returned\_rm\_qty) from self.get\_qty\_taken\_back\_by\_earlier\_returns().
- Set item\_fields from list(“main\_item\_code”, “rm\_item\_code”, “item\_name”, “description”, …).
- Set materials from defaultdict(dict).
- For each row in Platform.get\_all(“Subcontracting Receipt Supplied Item”, filters = mapping(“parent” → self.return\_against, “consumed\_qty” → tuple(“!=”, 0)), fields = list(“reference\_name”, “consumed\_qty”, expanded item\_fi ….
  - Set material from materials at row.reference\_name.setdefault(row.rm\_item\_code, Platform.\_dict(item\_details = mapping of fieldname → row at fieldname for fieldname drawn from item\_fields, consumed\_qty = 0, received\_qty = flt ….
    - Draw fieldname from item\_fields.
  - Update material.consumed\_qty using + flt(row.consumed\_qty).
- Return materials.

**Methods declared on this owner** [is subcontracting receipt return](operations-028.md#op-a9d0e47e1ced68), [get qty taken back by earlier returns](operations-028.md#op-d2ae05a8ae179d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L437)

<a id="op-d2ae05a8ae179d"></a>
### Subcontracting Controller.get qty taken back by earlier returns

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_get_qty_taken_back_by_earlier_returns`

**Inputs** self.

**Explicit results** tuple(dict(fg\_qty), mapping of tuple(row, rm\_item) → qty for tuple(row, rm\_item, qty) drawn from rm\_qty).

**Local steps**

- Set receipt from Platform.qb.DocType(“Subcontracting Receipt”).
- Set item from Platform.qb.DocType(“Subcontracting Receipt Item”).
- Set supplied\_item from Platform.qb.DocType(“Subcontracting Receipt Supplied Item”).
- Set submitted\_return from ((receipt.return\_against equals self.return\_against bitwise and receipt.is\_return equals 1) bitwise and receipt.docstatus equals 1).
- Set fg\_qty from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(submitted\_return).groupby(item.subcontracting\_receipt\_item).run().
- Set rm\_qty from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(submitted\_return).groupby(item.subcontracting\_receipt\_item, supplied\_ite ….run().
- Return tuple(dict(fg\_qty), mapping of tuple(row, rm\_item) → qty for tuple(row, rm\_item, qty) drawn from rm\_qty).
  - Draw tuple(row, rm\_item, qty) from rm\_qty.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L434)

<a id="op-1218478997d6c0"></a>
### Subcontracting Controller.add returned raw materials

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_add_returned_raw_materials`

**Inputs** self, row.

**Local steps**

- For each material in self.returnable\_raw\_materials.get(row.subcontracting\_receipt\_item, mapping()).values().
  - Update material.returned\_fg\_qty using + abs(flt(row.received\_qty)).
  - Set qty from self.get\_return\_consumed\_qty(material).
  - Update material.returned\_qty using − qty.
  - If qty.
    - Evaluate self.\_\_add\_supplied\_or\_received\_item(row, Platform.\_dict(material.item\_details), qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get return consumed qty](operations-029.md#op-3a06a111a9e1a1), [add supplied or received item](operations-030.md#op-bb036061907bfd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L427)

<a id="op-3b3a961c21f91c"></a>
### Subcontracting Controller.count kept return rows

`operation_enterprise_binding_enterprise_controllers_subcontracting_controller_subcontractingcontroller_count_kept_return_rows`

**Inputs** self, rows.

**Local steps**

- For each row in rows.
  - For each tuple(rm\_item\_code, material) in self.returnable\_raw\_materials.get(row.subcontracting\_receipt\_item, mapping()).items().
    - Update material.returned\_fg\_qty using + abs(flt(row.received\_qty)).
    - Update material.returned\_qty using + sum(generator of abs(flt(supplied\_item.consumed\_qty)) for supplied\_item drawn from self.supplied\_items where tuple(supplied\_item.reference\_name, supplied\_item.rm\_item\_code) equals tuple(row.name, rm\_item\_code)).
      - Draw supplied\_item from self.supplied\_items, keep a combination only if (tuple(supplied\_item.reference\_name, supplied\_item.rm\_item\_code) equals tuple(row.name, rm\_item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L428)
