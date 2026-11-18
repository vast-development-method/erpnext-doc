# Supporting services · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Transaction base

<a id="op-8e572e4a4bf8d6"></a>
### Transaction Base.handle internal parties

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_handle_internal_parties`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Set fetch\_valuation\_rate\_for\_internal\_transaction from cint(Platform.get\_single\_value(“Accounts Settings”, “fetch\_valuation\_rate\_for\_internal\_transaction”)).
- If ((self.get(“is\_internal\_customer”) or self.get(“is\_internal\_supplier”)) and fetch\_valuation\_rate\_for\_internal\_transaction).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.get(“is\_internal\_customer”) or self.get(“is\_internal\_supplier”)) → fetch\_valuation\_rate\_for\_internal\_transaction.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_internal\_customer”) → self.get(“is\_internal\_supplier”).
  - Set args from Platform.\_dict(mapping(“item\_code” → item\_obj.item\_code, “warehouse” → item\_obj.from\_warehouse when self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”), otherwise item\_obj.warehouse, “qty” ….
    - Value choice on self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”) — true gives item\_obj.from\_warehouse, false gives item\_obj.warehouse.
  - If self.doctype belongs to list(“Purchase Order”, “Sales Order”).
    - Evaluate args.update(mapping(“posting\_date” → self.transaction\_date, “posting\_time” → self.transaction\_time)).
  - Otherwise.
    - Evaluate args.update(mapping(“posting\_date” → self.posting\_date, “posting\_time” → self.posting\_time, “serial\_no” → item\_obj.serial\_no, “batch\_no” → item\_obj.batch\_no, …)).
  - Set rate from \_get\_incoming\_rate(args = args).
  - Set item\_obj.rate from (rate × item\_obj.conversion\_factor).
- Otherwise.
  - Evaluate self.set\_rate\_based\_on\_price\_list(item\_obj, item\_details).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set rate based on price list](operations-008.md#op-2e97ca3d89de6c).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “fetch\_valuation\_rate\_for\_internal\_transaction”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L110)

<a id="op-e75cacdf884106"></a>
### Transaction Base.add taxes from item template

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_add_taxes_from_item_template`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** request new\_doc for child\_doctype.

**Local steps**

- If (item\_details.item\_tax\_rate and Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_details.item\_tax\_rate → Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).
  - Set item\_tax\_template from Platform.json.loads(item\_details.item\_tax\_rate).
  - For each tuple(tax\_head, \_rate) in item\_tax\_template.items().
    - If \_rate equals NOT\_APPLICABLE\_TAX.
      - Continue with the next iteration or loop test.
    - Set found from list of x for x drawn from self.taxes where x.account\_head equals tax\_head.
      - Draw x from self.taxes, keep a combination only if (x.account\_head equals tax\_head).
    - If not found.
      - Set child\_doctype from self.get\_table\_field\_doctype(“taxes”).
      - Set child from Platform.new\_doc(child\_doctype, parent\_doc = self, parentfield = “taxes”).
      - Set child.charge\_type from “On Net Total”.
      - Set child.account\_head from tax\_head.
      - Set child.rate from 0.
      - Evaluate self.append(“taxes”, child).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L4378) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L98)

<a id="op-2e97ca3d89de6c"></a>
### Transaction Base.set rate based on price list

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_set_rate_based_on_price_list`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Local steps**

- If (item\_obj.price\_list\_rate and item\_obj.discount\_percentage).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_obj.price\_list\_rate → item\_obj.discount\_percentage.
  - Set item\_obj.rate from flt((item\_obj.price\_list\_rate × (1 − (item\_obj.discount\_percentage ÷ 100.0))), item\_obj.precision(“rate”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L4824) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L116)

<a id="op-075b8c5d5a197c"></a>
### Transaction Base.copy from first row

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_copy_from_first_row`

**Inputs** self, row, fields.

**Local steps**

- Set sibling\_rows from self.get(row.parentfield) when row, otherwise no value.
  - Value choice on row — true gives self.get(row.parentfield), false gives no value.
- If sibling\_rows.
  - Evaluate fields.extend(list of x.get(“fieldname”) for x drawn from get\_dimensions(true) at 0).
    - Draw x from get\_dimensions(true) at 0.
  - Set first\_row from sibling\_rows at 0.
  - Evaluate list of setattr(row, k, first\_row.get(k)) for k drawn from fields where hasattr(first\_row, k).
    - Draw k from fields, keep a combination only if (hasattr(first\_row, k)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L104)

<a id="op-a4ecede86beb27"></a>
### Transaction Base.add free item

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_add_free_item`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- Set free\_items from item\_details.get(“free\_item\_data”).
- If not free\_items.
  - Return no value.
- Set parentfield from item\_obj.parentfield.
- Set existing\_free\_items from list of x for x drawn from self.get(parentfield) where x.is\_free\_item.
  - Draw x from self.get(parentfield), keep a combination only if (x.is\_free\_item).
- For each free\_item in free\_items.
  - Set \_matches from list of x for x drawn from existing\_free\_items where (x.item\_code equals free\_item.get(“item\_code”) and x.pricing\_rules equals free\_item.get(“pricing\_rules”)).
    - Draw x from existing\_free\_items, keep a combination only if ((x.item\_code equals free\_item.get(“item\_code”) and x.pricing\_rules equals free\_item.get(“pricing\_rules”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in x.item\_code equals free\_item.get(“item\_code”) → x.pricing\_rules equals free\_item.get(“pricing\_rules”).
  - If \_matches.
    - Set row\_to\_modify from \_matches at 0.
  - Otherwise.
    - Set row\_to\_modify from self.append(parentfield).
  - For each tuple(k, \_v) in free\_item.items().
    - Evaluate setattr(row\_to\_modify, k, free\_item.get(k)).
  - Evaluate self.copy\_from\_first\_row(row\_to\_modify, list(“expense\_account”, “income\_account”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [copy from first row](operations-008.md#op-075b8c5d5a197c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L97)

<a id="op-57f699030bf3bb"></a>
### Transaction Base.conversion factor

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_conversion_factor`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If Platform.get\_meta(item\_obj.doctype).has\_field(“stock\_qty”).
  - Set item\_obj.stock\_qty from flt((item\_obj.qty × item\_obj.conversion\_factor), item\_obj.precision(“stock\_qty”)).
  - If self.doctype differs from “Material Request”.
    - Set item\_obj.total\_weight from flt((item\_obj.stock\_qty × item\_obj.weight\_per\_unit)).
    - Evaluate self.calculate\_net\_weight().
  - If Platform.flags.dont\_fetch\_price\_list\_rate.
    - Return no value.
  - If (not Platform.flags.dont\_fetch\_price\_list\_rate and Platform.get\_meta(self.doctype).has\_field(“price\_list\_currency”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.flags.dont\_fetch\_price\_list\_rate → Platform.get\_meta(self.doctype).has\_field(“price\_list\_currency”).
    - Evaluate self.\_apply\_price\_list(item\_obj, true).
  - Evaluate self.calculate\_stock\_uom\_rate(item\_obj).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate net weight](operations-008.md#op-7f459ae26522b9), [apply price list](operations-008.md#op-6983b20f011e79), [calculate stock uom rate](operations-008.md#op-11bed45430bad4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L5737) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L103)

<a id="op-11bed45430bad4"></a>
### Transaction Base.calculate stock uom rate

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_calculate_stock_unit_of_measure_rate`

**Inputs** self, item\_obj.

**Declared result** no value.

**Local steps**

- If item\_obj.rate.
  - Set item\_obj.stock\_uom\_rate from (flt(item\_obj.rate) ÷ flt(item\_obj.conversion\_factor)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0992.json#L6164) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L101)

<a id="op-2d4819bc1c183c"></a>
### Transaction Base.set item rate and discounts

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_set_item_rate_and_discounts`

**Inputs** self, item\_obj, item\_details.

**Declared result** no value.

**Local steps**

- Set effective\_item\_rate from item\_details.price\_list\_rate.
- Set item\_rate from item\_details.rate.
- If (item\_obj.parenttype belongs to list(“Sales Order”, “Quotation”) and item\_obj.blanket\_order\_rate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_obj.parenttype belongs to list(“Sales Order”, “Quotation”) → item\_obj.blanket\_order\_rate.
  - Set effective\_item\_rate from (flt(item\_obj.blanket\_order\_rate) × (flt(item\_obj.conversion\_factor) or 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item\_obj.conversion\_factor) → 1.
- If item\_obj.margin\_type equals “Percentage”.
  - Set item\_obj.rate\_with\_margin from (flt(effective\_item\_rate) + (flt(effective\_item\_rate) × (flt(item\_obj.margin\_rate\_or\_amount) ÷ 100))).
- Otherwise.
  - Set item\_obj.rate\_with\_margin from (flt(effective\_item\_rate) + flt(item\_obj.margin\_rate\_or\_amount)).
- Set item\_obj.base\_rate\_with\_margin from (flt(item\_obj.rate\_with\_margin) × flt(self.conversion\_rate)).
- Set item\_rate from flt(item\_obj.rate\_with\_margin, item\_obj.precision(“rate”)).
- If item\_obj.discount\_percentage.
  - Set item\_obj.discount\_amount from ((flt(item\_obj.rate\_with\_margin) × flt(item\_obj.discount\_percentage)) ÷ 100).
- If item\_obj.discount\_amount.
  - Set item\_rate from flt((item\_obj.rate\_with\_margin − item\_obj.discount\_amount), item\_obj.precision(“rate”)).
- Set item\_obj.rate from item\_rate.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L115)

<a id="op-7f459ae26522b9"></a>
### Transaction Base.calculate net weight

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_calculate_net_weight`

**Inputs** self.

**Local steps**

- Set self.total\_net\_weight from sum(list of (x.get(“total\_weight”) or 0) for x drawn from self.items).
  - Draw x from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in x.get(“total\_weight”) → 0.
- Evaluate self.apply\_shipping\_rule().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L100)

<a id="op-6983b20f011e79"></a>
### Transaction Base.apply price list

`operation_enterprise_utilities_transaction_base_business_behavior_transaction_base_apply_price_list`

**Inputs** self, item\_obj, reset\_plc\_conversion.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If self.doctype equals “Material Request”.
  - Return no value.
- If not reset\_plc\_conversion.
  - Set self.plc\_conversion\_rate from empty text.
- If (not self.items or not (item\_obj.get(“selling\_price\_list”) or item\_obj.get(“buying\_price\_list”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.items → not (item\_obj.get(“selling\_price\_list”) or item\_obj.get(“buying\_price\_list”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_obj.get(“selling\_price\_list”) → item\_obj.get(“buying\_price\_list”).
  - Return no value.
- If self.get(“in\_apply\_price\_list”).
  - Return no value.
- Set self.in\_apply\_price\_list from true.
- Bind dependencies \_apply\_price\_list.
- Set args from mapping(“items” → list of mapping(expand x.as\_dict(), “child\_docname” → x.name) for x drawn from self.items, “customer” → (self.customer or self.party\_name), “quotation\_to” → self.quotation\_to, “customer\_g ….
  - Draw x from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.customer → self.party\_name.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.selling\_price\_list → self.buying\_price\_list.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.transaction\_date → self.posting\_date.
  - Value choice on self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) — true gives self.update\_stock, false gives 0.
  - Value choice on self.doctype equals “Sales Invoice” — true gives self.pos\_profile, false gives empty text.
- Evaluate \_apply\_price\_list(cts = args, as\_doc = true, doc = self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L99)

<a id="op-706414ff595ca1"></a>
### Delete events

`operation_enterprise_utilities_transaction_base_business_behavior_delete_events`

**Inputs** ref\_type, ref\_name.

**State and service calls** request delete\_doc for “Event”.

**Local steps**

- Set events from (Platform.db.sql\_list(query text (SELECT, Event), tuple(ref\_type, ref\_name)) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.sql\_list(query text (SELECT, Event), tuple(ref\_type, ref\_name)) → list().
- If events.
  - Evaluate Platform.delete\_doc(“Event”, events, for\_reload = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L96)

<a id="op-08a82613dbd546"></a>
### Get whole number uoms

`operation_enterprise_binding_enterprise_utilities_transaction_base_get_whole_number_uoms`

**Inputs** uoms.

**Record and data access** read “UOM” via get\_values.

**Explicit results** set(generator of d at 0 for d drawn from Platform.db.get\_values(“UOM”, tuple(tuple(“name”, “in”, distinct\_uoms), tuple(“must\_be\_whole\_number”, “=”, 1)), cache = true)).

**Local steps**

- Set distinct\_uoms from tuple(set(generator of uom for uom drawn from uoms where uom)).
  - Draw uom from uoms, keep a combination only if (uom).
- Return set(generator of d at 0 for d drawn from Platform.db.get\_values(“UOM”, tuple(tuple(“name”, “in”, distinct\_uoms), tuple(“must\_be\_whole\_number”, “=”, 1)), cache = true)).
  - Draw d from Platform.db.get\_values(“UOM”, tuple(tuple(“name”, “in”, distinct\_uoms), tuple(“must\_be\_whole\_number”, “=”, 1)), cache = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1340)

<a id="op-947093b4dfb3fd"></a>
### Validate uom is integer

`operation_enterprise_utilities_transaction_base_business_behavior_validate_unit_of_measure_is_integer`

**Inputs** doc, uom\_field, qty\_fields, child\_dt = no value.

**Explicit results** no value.

**Local steps**

- If isinstance(qty\_fields, str).
  - Set qty\_fields from list(qty\_fields).
- Set uoms from set of d.get(uom\_field) for d drawn from doc.get\_all\_children().
  - Draw d from doc.get\_all\_children().
- Evaluate validate\_uoms\_are\_enabled(uoms).
- Set integer\_uoms from get\_whole\_number\_uoms(uoms).
- If not integer\_uoms.
  - Return no value.
- For each d in doc.get\_all\_children(parenttype = child\_dt).
  - If d.get(uom\_field) belongs to integer\_uoms.
    - For each f in qty\_fields.
      - Evaluate validate\_qty\_is\_integer(d.get(f), d.get(uom\_field), d.precision(f), d.idx).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L122)

<a id="op-95b2df6bfdfa40"></a>
### Validate item stock uom is integer

`operation_enterprise_binding_enterprise_utilities_transaction_base_validate_item_stock_uom_is_integer`

**Inputs** doc, item\_field, qty\_fields, child\_dt, row\_filter = no value.

**Record and data access** read “Item” via get\_all.

**Explicit results** no value.

**Local steps**

- If isinstance(qty\_fields, str).
  - Set qty\_fields from list(qty\_fields).
- Set rows from doc.get\_all\_children(parenttype = child\_dt).
- If row\_filter.
  - Set rows from list of d for d drawn from rows where row\_filter(d).
    - Draw d from rows, keep a combination only if (row\_filter(d)).
- Set item\_codes from set of d.get(item\_field) for d drawn from rows where d.get(item\_field).
  - Draw d from rows, keep a combination only if (d.get(item\_field)).
- If not item\_codes.
  - Return no value.
- Set item\_stock\_uoms from dict(Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, item\_codes)), fields = list(“name”, “stock\_uom”), as\_list = true)).
- Evaluate validate\_uoms\_are\_enabled(item\_stock\_uoms.values()).
- Set integer\_uoms from get\_whole\_number\_uoms(item\_stock\_uoms.values()).
- For each d in rows.
  - If stock\_uom bound to item\_stock\_uoms.get(d.get(item\_field)).
    - If stock\_uom belongs to integer\_uoms.
      - For each f in qty\_fields.
        - Evaluate validate\_qty\_is\_integer(d.get(f), stock\_uom, d.precision(f), d.idx).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1344)

<a id="op-6f079718ddfc0b"></a>
### Validate qty is integer

`operation_enterprise_binding_enterprise_utilities_transaction_base_validate_qty_is_integer`

**Inputs** qty, uom, precision, row\_idx.

**Explicit results** no value.

**Explicit failure paths** validation helper with UOMMustBeIntegerError — translated “Row {1}: Quantity ({0}) cannot be a fraction. To allow this, disable '{2}' in UOM {3}.”.format(qty, row\_idx, Platform.bold(translated “Must be Whole Number”), Platform.bold(uom)).

**Local steps**

- If not qty.
  - Return no value.
- Set qty from flt(qty, precision).
- If qty differs from cint(qty).
  - Call the validation error handler Platform.throw(translated “Row {1}: Quantity ({0}) cannot be a fraction. To allow this, disable '{2}' in UOM {3}.”.format(qty, row\_idx, Platform.bold(translated “Must be Whole Number”), Platform.bold(uom)) ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1345)

## Service · Uom data

<a id="op-91797a3c698274"></a>
### Extract

`operation_enterprise_gettext_extractors_unit_of_measure_data_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Local steps**

- Set uom\_list from json.load(fileobj).
- If not isinstance(uom\_list, list).
  - Return no value.
- For each uom\_data in uom\_list.
  - yield tuple(no value, “\_”, uom\_data.get(“uom\_name”), list(“Name of a UOM”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L6778) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L160) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L73)

## Service · Utilities

<a id="op-4a966553af3a6f"></a>
### Clear logs with references

`operation_enterprise_utilities_initialize_business_behavior_clear_logs_with_references`

**Inputs** doctype, filters.

**Record and data access** read doctype via get\_all · read “File” via get\_all.

**State and service calls** request delete\_doc for “File” · request delete on reference\_doctype · request delete on doctype.

**Local steps**

- Set names from Platform.get\_all(doctype, filters = filters, pluck = “name”).
- For each batch in create\_batch(names, 1000).
  - Set attached\_files from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → tuple(“in”, batch)), pluck = “name”).
  - If attached\_files.
    - Evaluate Platform.delete\_doc(“File”, attached\_files, ignore\_permissions = true, delete\_permanently = true).
  - For each tuple(reference\_doctype, tuple(doctype\_field, name\_field)) in LOG\_REFERENCE\_FIELDS.items().
    - Evaluate Platform.db.delete(reference\_doctype, mapping(doctype\_field → doctype, name\_field → tuple(“in”, batch))).
  - Evaluate Platform.db.delete(doctype, mapping(“name” → tuple(“in”, batch))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0988.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L275) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L69)

<a id="op-d3fa3503f225cb"></a>
### Update doctypes

`operation_enterprise_utilities_initialize_business_behavior_update_record_types`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT) · resolve a document from “DocType” via get\_doc.

**State and service calls** call save on dt.

**Local steps**

- For each d in Platform.db.sql(query text (SELECT), as\_dict = 1).
  - Set dt from Platform.get\_doc(“DocType”, d.parent).
  - For each f in dt.fields.
    - If (f.fieldname equals d.fieldname and f.fieldtype belongs to tuple(“Text”, “Small Text”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in f.fieldname equals d.fieldname → f.fieldtype belongs to tuple(“Text”, “Small Text”).
      - Set f.fieldtype from “Text Editor”.
      - Evaluate dt.save().
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L278) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L72)

<a id="op-677814169ff1a7"></a>
### Get site info

`operation_enterprise_utilities_initialize_business_behavior_get_site_info`

**Inputs** site\_info.

**Record and data access** read “Global Defaults” via get\_single\_value · execute query text (SELECT, Company) · read “Company” via get\_cached\_value.

**Explicit results** mapping(“company” → company, “domain” → domain, “activation” → get\_level(site\_info)).

**Local steps**

- Set company from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).
- Set domain from no value.
- If not company.
  - Set company from Platform.db.sql(query text (SELECT, Company)).
  - Set company from company at 0 at 0 when company, otherwise no value.
    - Value choice on company — true gives company at 0 at 0, false gives no value.
- If company.
  - Set domain from Platform.get\_cached\_value(“Company”, cstr(company), “domain”).
- Return mapping(“company” → company, “domain” → domain, “activation” → get\_level(site\_info)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”), Platform.get\_cached\_value(“Company”, cstr(company), “domain”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L276) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L70)

<a id="op-e5b0140e0b5f8f"></a>
### Payment app import guard

`operation_enterprise_utilities_initialize_business_behavior_payment_application_import_guard`

**Inputs** no declared parameters.

**Wrappers, in declaration order** contextmanager.

**Explicit failure paths** validation helper with Platform.AppNotInstalledError — msg.

**Local steps**

- Set marketplace\_link from text in the contract.
- Set github\_link from text in the contract.
- Set msg from translated “payments app is not installed. Please install it from {} or {}”.format(marketplace\_link, github\_link).
- If “payments” does not belong to Platform.get\_installed\_apps().
  - Call the validation error handler Platform.throw(msg, title = translated “Missing Payments App”, exc = Platform.AppNotInstalledError).
- Attempt the following.
  - yield no value.
- On failure (ImportError).
  - Call the validation error handler Platform.throw(msg, title = translated “Missing Payments App”, exc = Platform.AppNotInstalledError).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L71)

## Service · Utils

<a id="op-d7e6df4b6acb83"></a>
### Set default role

`operation_enterprise_portal_utils_business_behavior_set_default_role`

**Inputs** doc, method.

**Record and data access** read “Contact” via get\_value · resolve a document from “Contact” via get\_doc.

**Explicit results** no value.

**Local steps**

- If (Platform.flags.setting\_role or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.setting\_role → Platform.flags.in\_migrate.
  - Return no value.
- Set roles from Platform.get\_roles(doc.name).
- Set contact\_name from Platform.get\_value(“Contact”, dict(email\_id = doc.email)).
- If contact\_name.
  - Set contact from Platform.get\_doc(“Contact”, contact\_name).
  - For each link in contact.links.
    - Set Platform.flags.setting\_role from true.
    - If (link.link\_doctype equals “Customer” and “Customer” does not belong to roles).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals “Customer” → “Customer” does not belong to roles.
      - Evaluate doc.add\_roles(“Customer”).
    - Otherwise.
      - If (link.link\_doctype equals “Supplier” and “Supplier” does not belong to roles).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals “Supplier” → “Supplier” does not belong to roles.
        - Evaluate doc.add\_roles(“Supplier”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(doc.name).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0599.json#L4756) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L659)

<a id="op-211c7d064baeba"></a>
### Create customer or supplier

`operation_enterprise_portal_utils_business_behavior_create_customer_or_supplier`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_value · read “Portal Settings” via get\_single.

**Explicit results** no value · party.

**Local steps**

- Set user from Platform.session.user.
- If Platform.db.get\_value(“User”, user, “user\_type”) differs from “Website User”.
  - Return no value.
- Set user\_roles from Platform.get\_roles().
- Set portal\_settings from Platform.get\_single(“Portal Settings”).
- Set default\_role from portal\_settings.default\_role.
- If default\_role does not belong to list(“Customer”, “Supplier”).
  - Return no value.
- If (portal\_settings.default\_role and portal\_settings.default\_role belongs to user\_roles).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in portal\_settings.default\_role → portal\_settings.default\_role belongs to user\_roles.
  - Set doctype from portal\_settings.default\_role.
- Otherwise.
  - Set doctype from no value.
- If not doctype.
  - Return no value.
- If party\_exists(doctype, user).
  - Return no value.
- Set fullname from Platform.utils.get\_fullname(user).
- Set party from create\_party(doctype, fullname).
- Set alternate\_doctype from “Customer” when doctype equals “Supplier”, otherwise “Supplier”.
  - Value choice on doctype equals “Supplier” — true gives “Customer”, false gives “Supplier”.
- If party\_exists(alternate\_doctype, user).
  - Update fullname using + (“-” + doctype).
- Evaluate create\_party\_contact(doctype, fullname, user, party.name).
- Return party.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0599.json#L5195) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L655)

<a id="op-0377128b5b0e93"></a>
### Create party

`operation_enterprise_portal_utils_business_behavior_create_party`

**Inputs** doctype, fullname.

**State and service calls** request new\_doc for doctype · call insert on party.

**Explicit results** party.

**Local steps**

- Set party from Platform.new\_doc(doctype).
- Evaluate party.update(mapping(formatted text {doctype.lower()}\_name → fullname, formatted text {doctype.lower()}\_type → “Individual”)).
- Set party.flags.ignore\_mandatory from true.
- Evaluate party.insert(ignore\_permissions = true).
- Return party.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0599.json#L5764) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L656)

<a id="op-a66b89bdbe69d0"></a>
### Create party contact

`operation_enterprise_portal_utils_business_behavior_create_party_contact`

**Inputs** doctype, fullname, user, party\_name.

**State and service calls** request new\_doc for “Contact” · call insert on contact.

**Local steps**

- Set contact from Platform.new\_doc(“Contact”).
- Evaluate contact.update(mapping(“first\_name” → fullname, “email\_id” → user)).
- Evaluate contact.append(“links”, dict(link\_doctype = doctype, link\_name = party\_name)).
- Evaluate contact.append(“email\_ids”, dict(email\_id = user, is\_primary = true)).
- Set contact.flags.ignore\_mandatory from true.
- Evaluate contact.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0599.json#L5991) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L657)
