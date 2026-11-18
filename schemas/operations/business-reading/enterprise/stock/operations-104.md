# Inventory and warehouses · operations 104

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock reservation entry

[Record definition](../../../../data/record-types/stock_reservation_entry.json)

<a id="op-caeda0784be79a"></a>
### Get open serial batch entries

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_get_open_serial_batch_entries`

**Inputs** sre\_names, release.

**Declared result** list at dict.

**Explicit results** nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sb\_entry.idx).for\_update().run(as\_dict = true).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set open\_qty from sb\_entry.delivered\_qty when release, otherwise (sb\_entry.qty − sb\_entry.delivered\_qty).
  - Value choice on release — true gives sb\_entry.delivered\_qty, false gives (sb\_entry.qty − sb\_entry.delivered\_qty).
- Return nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(sb\_entry.idx).for\_update().run(as\_dict = true).
  - Value choice on release — true gives Order.desc, false gives Order.asc.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L814)

<a id="op-2cce71066f77b3"></a>
### Allocate serial batch qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_allocate_serial_batch_qty`

**Inputs** entries, limits, serial\_batch.

**Declared result** dict at tuple(str, float).

**Explicit results** moved\_qty.

**Local steps**

- Set limits from defaultdict(float, limits).
- Set serial\_nos from set((serial\_batch.get(“serial\_nos”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_batch.get(“serial\_nos”) → list().
- Set batches from defaultdict(float, (serial\_batch.get(“batches”) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in serial\_batch.get(“batches”) → mapping().
- Set moved\_qty from mapping().
- For each entry in entries.
  - Set qty from 0.
  - If (entry.serial\_no and entry.serial\_no belongs to serial\_nos and limits at entry.parent ≥ entry.open\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.serial\_no → entry.serial\_no belongs to serial\_nos → limits at entry.parent ≥ entry.open\_qty.
    - Set qty from entry.open\_qty.
    - Evaluate serial\_nos.remove(entry.serial\_no).
  - Otherwise.
    - If (not entry.serial\_no and entry.batch\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not entry.serial\_no → entry.batch\_no.
      - Set qty from min(entry.open\_qty, batches at entry.batch\_no, limits at entry.parent).
      - Update batches at entry.batch\_no using − qty.
  - Update limits at entry.parent using − qty.
  - If qty &gt; 0.
    - Set moved\_qty at entry.name from qty.
- Return moved\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L812)

<a id="op-40aa97c77667aa"></a>
### Add serial batch delivered qty

`operation_enterprise_binding_enterprise_stock_doctype_stock_reservation_entry_stock_reservation_entry_add_serial_batch_delivered_qty`

**Inputs** deltas.

**Declared result** no value.

**Local steps**

- Set rows\_by\_delta from defaultdict(list).
- For each tuple(name, delta) in deltas.items().
  - Evaluate rows\_by\_delta at delta.append(name).
- Set sb\_entry from Platform.qb.DocType(“Serial and Batch Entry”).
- For each tuple(delta, names) in rows\_by\_delta.items().
  - Evaluate nested operand in the contract(nested operand in the contract).set(sb\_entry.delivered\_qty, (nested operand in the contract.delivered\_qty + delta)).where(sb\_entry.name.isin(names)).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L811)

## Record · Stock settings

[Record definition](../../../../data/record-types/stock_settings.json)

<a id="op-037eb30b9aeb56"></a>
### Stock Settings.validate

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate`

**Inputs** self.

**Local steps**

- For each key in list(“item\_naming\_by”, “item\_group”, “stock\_uom”, “allow\_negative\_stock”, …).
  - Set value from self.get(key).
  - Evaluate Platform.db.set\_default(key, empty text when value is identical to no value, otherwise value).
    - Value choice on value is identical to no value — true gives empty text, false gives value.
- Bind dependencies set\_by\_naming\_series.
- Evaluate set\_by\_naming\_series(“Item”, “item\_code”, self.get(“item\_naming\_by”) equals “Naming Series”, hide\_name\_field = true, make\_mandatory = 0).
- Evaluate self.update\_barcode\_field\_visibility().
- Evaluate self.validate\_serial\_and\_batch\_no\_settings().
- Evaluate self.cant\_change\_valuation\_method().
- Evaluate self.validate\_clean\_description\_html().
- Evaluate self.validate\_pending\_reposts().
- Evaluate self.validate\_stock\_reservation().
- Evaluate self.validate\_auto\_insert\_price\_list\_rate\_if\_missing().
- Evaluate self.change\_precision\_for\_for\_sales().
- Evaluate self.change\_precision\_for\_purchase().
- Evaluate self.change\_precision\_for\_stock\_entry().
- Evaluate self.validate\_do\_not\_use\_batchwise\_valuation().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update barcode field visibility](operations-104.md#op-1b0ebc3982acb1), [validate serial and batch no settings](operations-104.md#op-170b1a572d2a94), [cant change valuation method](operations-104.md#op-9a9733d13ec18e), [validate clean description html](operations-104.md#op-0b350b422b7822), [validate pending reposts](operations-104.md#op-ff46c06afd4b52), [validate stock reservation](operations-104.md#op-cb6619c0259f54), [validate auto insert price list rate if missing](operations-104.md#op-6ee4d4fbf4ccd0), [change precision for for sales](operations-104.md#op-111b458f334225), [change precision for purchase](operations-104.md#op-9a7e1c50b820df), [change precision for stock entry](operations-104.md#op-a7c184ac3ed295), [validate do not use batchwise valuation](operations-104.md#op-4483c0247a5be5).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1226)

<a id="op-37e87573ed9b7e"></a>
### Stock Settings.on update

`operation_enterprise_binding_enterprise_stock_doctype_stock_settings_stock_settings_stocksettings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_boot\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear boot cache](operations-104.md#op-7d94ad4aedf593).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L842)

<a id="op-7d94ad4aedf593"></a>
### Stock Settings.clear boot cache

`operation_enterprise_binding_enterprise_stock_doctype_stock_settings_stock_settings_stocksettings_clear_boot_cache`

**Inputs** self.

**Local steps**

- If any(generator of self.has\_value\_changed(field) for field drawn from BOOT\_FIELDS).
  - Draw field from BOOT\_FIELDS.
  - Evaluate Platform.cache.delete\_key(“bootinfo”).
  - Evaluate Platform.db.after\_commit.add(deferred anonymous expression).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L841)

<a id="op-1b0ebc3982acb1"></a>
### Stock Settings.update barcode field visibility

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_update_barcode_field_visibility`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.has\_value\_changed(“show\_barcode\_field”).
  - Return no value.
- For each tuple(doctype, fieldname) in get\_transaction\_barcode\_fields().
  - Evaluate Platform.make\_property\_setter(mapping(“doctype” → doctype, “fieldname” → fieldname, “property” → “hidden”, “value” → 0 when self.show\_barcode\_field, otherwise 1), validate\_fields\_for\_doctype = false).
    - Value choice on self.show\_barcode\_field — true gives 0, false gives 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1225)

<a id="op-4483c0247a5be5"></a>
### Stock Settings.validate do not use batchwise valuation

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate_do_not_use_batchwise_valuation`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot disable {0} as it may lead to incorrect stock valuation.”.format(Platform.bold(translated “Do Not Use Batchwise Valuation”)).

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- If not Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“docstatus” → 1), limit = 1, pluck = “name”).
  - Return no value.
- If (doc\_before\_save.do\_not\_use\_batchwise\_valuation and not self.do\_not\_use\_batchwise\_valuation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.do\_not\_use\_batchwise\_valuation → not self.do\_not\_use\_batchwise\_valuation.
  - Call the validation error handler Platform.throw(translated “Cannot disable {0} as it may lead to incorrect stock valuation.”.format(Platform.bold(translated “Do Not Use Batchwise Valuation”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1229)

<a id="op-170b1a572d2a94"></a>
### Stock Settings.validate serial and batch no settings

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate_serial_and_batch_number_settings`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via exists · read “Item” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot disable Serial and Batch No for Item, as there are existing records for serial / batch.” · validation helper — translated “Cannot disable Serial and Batch No for Item, as there are items with serial / batch enabled.”.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- If doc\_before\_save.enable\_serial\_and\_batch\_no\_for\_item equals self.enable\_serial\_and\_batch\_no\_for\_item.
  - Return no value.
- If (doc\_before\_save.enable\_serial\_and\_batch\_no\_for\_item and not self.enable\_serial\_and\_batch\_no\_for\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.enable\_serial\_and\_batch\_no\_for\_item → not self.enable\_serial\_and\_batch\_no\_for\_item.
  - If Platform.db.exists(“Serial and Batch Bundle”, mapping(“docstatus” → 1)).
    - Call the validation error handler Platform.throw(translated “Cannot disable Serial and Batch No for Item, as there are existing records for serial / batch.”).
  - If (Platform.db.exists(“Item”, mapping(“has\_serial\_no” → 1)) or Platform.db.exists(“Item”, mapping(“has\_batch\_no” → 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“Item”, mapping(“has\_serial\_no” → 1)) → Platform.db.exists(“Item”, mapping(“has\_batch\_no” → 1)).
    - Call the validation error handler Platform.throw(translated “Cannot disable Serial and Batch No for Item, as there are items with serial / batch enabled.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1231)

<a id="op-9a9733d13ec18e"></a>
### Stock Settings.cant change valuation method

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_cant_change_valuation_method`

**Inputs** self.

**Record and data access** execute query text (SELECT, Stock Ledger Entry, Item).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Can't change the valuation method, as there are transactions against some items which do not have its own va …”.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- Set previous\_valuation\_method from doc\_before\_save.get(“valuation\_method”).
- If (previous\_valuation\_method and previous\_valuation\_method differs from self.valuation\_method).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_valuation\_method → previous\_valuation\_method differs from self.valuation\_method.
  - Set sle from Platform.db.sql(query text (SELECT, Stock Ledger Entry, Item)).
  - If sle.
    - Call the validation error handler Platform.throw(translated “Can't change the valuation method, as there are transactions against some items which do not have its own va …”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1220)

<a id="op-0b350b422b7822"></a>
### Stock Settings.validate clean description html

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate_clean_description_document_markup`

**Inputs** self.

**State and service calls** enqueue with “Enterprise.stock.doctype.stock\_settings.stock\_settings.clean\_all\_descriptions”.

**Local steps**

- If (int((self.clean\_description\_html or 0)) and not int((self.db\_get(“clean\_description\_html”) or 0))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in int((self.clean\_description\_html or 0)) → not int((self.db\_get(“clean\_description\_html”) or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.clean\_description\_html → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.db\_get(“clean\_description\_html”) → 0.
  - Evaluate Platform.enqueue(“Enterprise.stock.doctype.stock\_settings.stock\_settings.clean\_all\_descriptions”, now = Platform.in\_test, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Enterprise.stock.doctype.stock\_settings.stock\_settings.clean\_all\_descriptions”, now = Platform.in\_test, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0876.json#L5507) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1228)

<a id="op-ff46c06afd4b52"></a>
### Stock Settings.validate pending reposts

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate_pending_reposts`

**Inputs** self.

**Local steps**

- If self.stock\_frozen\_upto.
  - Evaluate check\_pending\_reposting(self.stock\_frozen\_upto).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0876.json#L5739) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1230)

<a id="op-cb6619c0259f54"></a>
### Stock Settings.validate stock reservation

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate_stock_reservation`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “As {0} is enabled, you can not enable {1}.”.format(Platform.bold(translated “Stock Reservation”), Platform.bold(translated “Allow Negative Stock”)) · validation helper — translated “As {0} is enabled, you can not enable {1}.”.format(Platform.bold(translated “Allow Negative Stock”), Platform.bold(translated “Stock Reservation”)) · validation helper — translated “As there are reserved stock, you cannot disable {0}.”.format(Platform.bold(translated “Stock Reservation”)).

**Local steps**

- If (not self.enable\_stock\_reservation and self.auto\_reserve\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.enable\_stock\_reservation → self.auto\_reserve\_stock.
  - Set self.auto\_reserve\_stock from 0.
- If Platform.in\_test.
  - Return no value.
- If self.has\_value\_changed(“allow\_negative\_stock”).
  - If (self.allow\_negative\_stock and self.enable\_stock\_reservation).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.allow\_negative\_stock → self.enable\_stock\_reservation.
    - Call the validation error handler Platform.throw(translated “As {0} is enabled, you can not enable {1}.”.format(Platform.bold(translated “Stock Reservation”), Platform.bold(translated “Allow Negative Stock”))).
- If self.has\_value\_changed(“enable\_stock\_reservation”).
  - If self.enable\_stock\_reservation.
    - If self.allow\_negative\_stock.
      - Call the validation error handler Platform.throw(translated “As {0} is enabled, you can not enable {1}.”.format(Platform.bold(translated “Allow Negative Stock”), Platform.bold(translated “Stock Reservation”))).
  - Otherwise.
    - Set has\_reserved\_stock from has\_open\_stock\_reservation().
    - If has\_reserved\_stock.
      - Call the validation error handler Platform.throw(translated “As there are reserved stock, you cannot disable {0}.”.format(Platform.bold(translated “Stock Reservation”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1232)

<a id="op-6ee4d4fbf4ccd0"></a>
### Stock Settings.validate auto insert price list rate if missing

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_validate_auto_insert_price_list_rate_if_missing`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**State and service calls** msgprint with translated “You have enabled {0} and {1} in {2}. This can lead to prices from the default price list being inserted in t …”.format(text in the contract.format(translated self.meta.get\_label(“auto\_insert\_pr ….

**Local steps**

- If (self.auto\_insert\_price\_list\_rate\_if\_missing and self.has\_value\_changed(“auto\_insert\_price\_list\_rate\_if\_missing”) and Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.auto\_insert\_price\_list\_rate\_if\_missing → self.has\_value\_changed(“auto\_insert\_price\_list\_rate\_if\_missing”) → Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”).
  - Set selling\_meta from Platform.get\_meta(“Selling Settings”).
  - Evaluate Platform.msgprint(translated “You have enabled {0} and {1} in {2}. This can lead to prices from the default price list being inserted in t …”.format(text in the contract.format(translated nested operand in ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “fallback\_to\_default\_price\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1227)

<a id="op-111b458f334225"></a>
### Stock Settings.change precision for for sales

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_change_precision_for_for_sales`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (doc\_before\_save and doc\_before\_save.allow\_to\_edit\_stock\_uom\_qty\_for\_sales equals self.allow\_to\_edit\_stock\_uom\_qty\_for\_sales).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.allow\_to\_edit\_stock\_uom\_qty\_for\_sales equals self.allow\_to\_edit\_stock\_uom\_qty\_for\_sales.
  - Return no value.
- If self.allow\_to\_edit\_stock\_uom\_qty\_for\_sales.
  - Set doctypes from list(“Sales Order Item”, “Sales Invoice Item”, “Delivery Note Item”, “Quotation Item”).
  - Evaluate self.make\_property\_setter\_for\_precision(doctypes).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make property setter for precision](operations-104.md#op-04773bff181375).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0876.json#L6760) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1221)

<a id="op-9a7e1c50b820df"></a>
### Stock Settings.change precision for purchase

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_change_precision_for_purchase`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (doc\_before\_save and doc\_before\_save.allow\_to\_edit\_stock\_uom\_qty\_for\_purchase equals self.allow\_to\_edit\_stock\_uom\_qty\_for\_purchase).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.allow\_to\_edit\_stock\_uom\_qty\_for\_purchase equals self.allow\_to\_edit\_stock\_uom\_qty\_for\_purchase.
  - Return no value.
- If self.allow\_to\_edit\_stock\_uom\_qty\_for\_purchase.
  - Set doctypes from list(“Purchase Order Item”, “Purchase Receipt Item”, “Purchase Invoice Item”, “Request for Quotation Item”, …).
  - Evaluate self.make\_property\_setter\_for\_precision(doctypes).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make property setter for precision](operations-104.md#op-04773bff181375).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0877.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1222)

<a id="op-a7c184ac3ed295"></a>
### Stock Settings.change precision for stock entry

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_change_precision_for_stock_entry`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (doc\_before\_save and doc\_before\_save.allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry equals self.allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry equals self.allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry.
  - Return no value.
- If self.allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry.
  - Set doctypes from list(“Stock Entry Detail”).
  - Evaluate self.make\_property\_setter\_for\_precision(doctypes).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make property setter for precision](operations-104.md#op-04773bff181375).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0877.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1223)

<a id="op-04773bff181375"></a>
### Stock Settings.make property setter for precision

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_stock_settings_make_property_setter_for_precision`

**Inputs** doctypes.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- For each doctype in doctypes.
  - Evaluate make\_property\_setter(doctype, “conversion\_factor”, “precision”, 9, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1224)

<a id="op-1d0b1f80989f95"></a>
### Clean all descriptions

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_clean_all_descriptions`

**Inputs** no declared parameters.

**Record and data access** read “Item” via get\_all.

**State and service calls** request set\_value on “Item”.

**Local steps**

- For each item in Platform.get\_all(“Item”, list(“name”, “description”)).
  - If item.description.
    - Set clean\_description from clean\_html(item.description).
    - If item.description differs from clean\_description.
      - Evaluate Platform.db.set\_value(“Item”, item.name, “description”, clean\_description).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0877.json#L646) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1218)

<a id="op-4a4c57b619bd9d"></a>
### Get enable stock uom editing

`operation_enterprise_stock_record_definitions_stock_settings_business_behavior_get_enable_stock_unit_of_measure_editing`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Stock Settings”, list(“allow\_to\_edit\_stock\_uom\_qty\_for\_sales”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”, “allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry”), as\_dict = 1).

**Local steps**

- Return Platform.get\_single\_value(“Stock Settings”, list(“allow\_to\_edit\_stock\_uom\_qty\_for\_sales”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”, “allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry”), as\_dict = 1).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, list(“allow\_to\_edit\_stock\_uom\_qty\_for\_sales”, “allow\_to\_edit\_stock\_uom\_qty\_for\_purchase”, “allow\_to\_edit\_stock\_uom\_qty\_for\_stock\_entry”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0877.json#L857) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L1219)

<a id="op-df8408cbae3898"></a>
### Get transaction barcode fields

`operation_enterprise_binding_enterprise_stock_doctype_stock_settings_stock_settings_get_transaction_barcode_fields`

**Inputs** no declared parameters.

**Record and data access** read “DocField” via get\_all.

**Explicit results** fields.

**Local steps**

- Set fields from list().
- For each doctype in Platform.get\_all(“DocField”, filters = mapping(“fieldname” → “scan\_barcode”), pluck = “parent”).
  - Evaluate fields.append(tuple(doctype, “scan\_barcode”)).
  - For each table\_field in Platform.get\_meta(doctype).get\_table\_fields().
    - If Platform.get\_meta(table\_field.options).has\_field(“barcode”).
      - Evaluate fields.append(tuple(table\_field.options, “barcode”)).
- Return fields.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L839)

<a id="op-77a9cddeb187a5"></a>
### Has open stock reservation

`operation_enterprise_binding_enterprise_stock_doctype_stock_settings_stock_settings_has_open_stock_reservation`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Local steps**

- Set sre from Platform.qb.DocType(“Stock Reservation Entry”).
- Return bool(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).limit(1).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0024.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L840)

## Report · Stock valuation comparison

<a id="op-1a6bbdd895e91a"></a>
### Execute

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Explicit failure paths** validation helper — translated “Please select a Company”.

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- If not filters.company.
  - Call the validation error handler Platform.throw(translated “Please select a Company”).
- Evaluate validate\_company\_permission(filters.company).
- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1561) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1058)

<a id="op-af4e3a69aa08de"></a>
### Get data

`operation_enterprise_binding_enterprise_stock_report_stock_valuation_comparison_stock_valuation_comparison_get_data`

**Inputs** filters.

**Declared result** list at dict.

**Explicit results** data.

**Local steps**

- Set tolerance from get\_default\_tolerance() when filters.get(“tolerance”) belongs to tuple(no value, empty text), otherwise flt(filters.tolerance).
  - Value choice on filters.get(“tolerance”) belongs to tuple(no value, empty text) — true gives get\_default\_tolerance(), false gives flt(filters.tolerance).
- Set item\_warehouses from list of tuple(row.item\_code, row.warehouse) for row drawn from get\_item\_warehouses(filters).
  - Draw row from get\_item\_warehouses(filters).
- Set adjusted\_until from get\_adjusted\_until(item\_warehouses, filters.to\_date).
- Set pending\_reposts from get\_pending\_reposts(item\_warehouses).
- Set data from list().
- For each tuple(item\_code, warehouse, expected\_valuation) in iterate\_expected\_valuations(item\_warehouses, to\_date = filters.to\_date).
  - Set rows from get\_rows\_to\_show(item\_code, warehouse, expected\_valuation, filters, …).
  - For each row in rows.
    - Set row.pending\_repost from pending\_reposts.get(tuple(item\_code, warehouse)).
  - Evaluate data.extend(rows).
- Return data.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0025.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1060)
