# Inventory and warehouses · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Delivery note

[Record definition](../../../../data/record-types/delivery_note.json)

<a id="op-2d508957d71823"></a>
### Make inter company transaction.update item

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_make_inter_company_transaction_update_item`

**Inputs** source, target, source\_parent.

**Local steps**

- If source\_parent.doctype equals “Delivery Note”.
  - Set target.qty from get\_pending\_receipt\_qty(source).
- If source\_parent.doctype equals “Purchase Receipt”.
  - Set target.qty from (flt(source.qty) − flt(accepted\_returns.get(source.name))).
- If source.get(“use\_serial\_batch\_fields”).
  - Evaluate target.set(“use\_serial\_batch\_fields”, 1).
- If ((source.get(“serial\_no”) or source.get(“batch\_no”)) and not source.get(“serial\_and\_batch\_bundle”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (source.get(“serial\_no”) or source.get(“batch\_no”)) → not source.get(“serial\_and\_batch\_bundle”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.get(“serial\_no”) → source.get(“batch\_no”).
  - Evaluate target.set(“use\_serial\_batch\_fields”, 1).
- Evaluate clear\_item\_tax\_template\_of\_other\_company(target, details.get(“company”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L186) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L746) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L243)

<a id="op-819b7d2bc79608"></a>
### Has pending inter company qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_has_pending_inter_company_qty`

**Inputs** item, doctype, accepted\_returns = no value.

**Declared result** bool.

**Explicit results** (flt(item.qty) − flt((accepted\_returns or mapping()).get(item.name))) &gt; 0 · get\_pending\_receipt\_qty(item) &gt; 0.

**Local steps**

- If doctype equals “Purchase Receipt”.
  - Return (flt(item.qty) − flt((accepted\_returns or mapping()).get(item.name))) &gt; 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in accepted\_returns → mapping().
- Return get\_pending\_receipt\_qty(item) &gt; 0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L735) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L232)

<a id="op-c8165c2aadb5a1"></a>
### Get accepted returned qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_accepted_returned_qty`

**Inputs** receipt.

**Declared result** dict.

**Explicit results** get\_returned\_qty\_of\_rows(list of d.name for d drawn from receipt.items).

**Local steps**

- Bind dependencies get\_returned\_qty\_of\_rows.
- Return get\_returned\_qty\_of\_rows(list of d.name for d drawn from receipt.items).
  - Draw d from receipt.items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L723) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L220)

<a id="op-58fe380ce40591"></a>
### Get pending receipt qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_pending_receipt_qty`

**Inputs** item.

**Declared result** float.

**Explicit results** ((flt(item.qty) − returned\_qty) − flt(item.get(“received\_qty”))).

**Local steps**

- Set returned\_qty from (flt(item.get(“returned\_qty”)) ÷ (flt(item.get(“conversion\_factor”)) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.get(“conversion\_factor”)) → 1.
- Return ((flt(item.qty) − returned\_qty) − flt(item.get(“received\_qty”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L229)

<a id="op-823f03ac8ebb2b"></a>
### Get component receipt map

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_component_receipt_map`

**Inputs** bundle\_rows.

**Declared result** dict.

**Explicit results** mapping(“doctype” → “Purchase Receipt Item”, “field\_map” → mapping(“target\_warehouse” → “from\_warehouse”, “name” → “delivery\_note\_packed\_item”), “field\_no\_map” → list(“warehouse”), “condition” → deferred a ….

**Local steps**

- Bind local operation update\_component for subsequent calls.
- Return mapping(“doctype” → “Purchase Receipt Item”, “field\_map” → mapping(“target\_warehouse” → “from\_warehouse”, “name” → “delivery\_note\_packed\_item”), “field\_no\_map” → list(“warehouse”), “condition” → deferred a ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L222)

<a id="op-ebedd00025a367"></a>
### Get component receipt map.update component

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_component_receipt_map_update_component`

**Inputs** source, target, source\_parent.

**Local steps**

- Set target.qty from get\_pending\_component\_qty(source, bundle\_rows at source.parent\_detail\_docname).
- Set target.rate from flt(source.incoming\_rate).
- If (source.get(“use\_serial\_batch\_fields”) or source.get(“serial\_no”) or source.get(“batch\_no”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source.get(“use\_serial\_batch\_fields”) → source.get(“serial\_no”) → source.get(“batch\_no”).
  - Evaluate target.set(“use\_serial\_batch\_fields”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L223)

<a id="op-700fbf48a07ded"></a>
### Get pending component qty

`operation_enterprise_binding_enterprise_stock_doctype_delivery_note_delivery_note_get_pending_component_qty`

**Inputs** packed\_item, bundle\_row.

**Declared result** float.

**Explicit results** 0.0 · ((flt(packed\_item.qty) × kept\_share) − flt(packed\_item.get(“received\_qty”))).

**Local steps**

- Set bundle\_qty from flt((bundle\_row.stock\_qty or bundle\_row.qty)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundle\_row.stock\_qty → bundle\_row.qty.
- If not bundle\_qty.
  - Return 0.0.
- Set kept\_share from (1 − (flt(bundle\_row.returned\_qty) ÷ bundle\_qty)).
- Return ((flt(packed\_item.qty) × kept\_share) − flt(packed\_item.get(“received\_qty”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L228)

<a id="op-b85340c22319cb"></a>
### Get data

`operation_enterprise_stock_record_definitions_delivery_note_delivery_note_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “delivery\_note”, “non\_standard\_fieldnames” → mapping(“Stock Entry” → “delivery\_note\_no”, “Quality Inspection” → “reference\_name”, “Auto Repeat” → “reference\_document”, “Purchase Recei ….

**Local steps**

- Return mapping(“fieldname” → “delivery\_note”, “non\_standard\_fieldnames” → mapping(“Stock Entry” → “delivery\_note\_no”, “Quality Inspection” → “reference\_name”, “Auto Repeat” → “reference\_document”, “Purchase Recei ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0714.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L893)

## Report · Delivery note trends

<a id="op-9c53836bc48be5"></a>
### Execute

`operation_enterprise_stock_report_delivery_note_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data, no value, chart\_data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Delivery Note”).
- Set data from get\_data(filters, conditions).
- Set chart\_data from get\_chart\_data(data, conditions, filters).
- Return tuple(conditions at “columns”, data, no value, chart\_data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L6521) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L120)

<a id="op-ca0c2cb14428c3"></a>
### Get chart data

`operation_enterprise_stock_report_delivery_note_trends_business_behavior_get_chart_data`

**Inputs** data, conditions, filters.

**Explicit results** list() · mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Total Delivered Amount”, “values” → datapoints))), “type” → “bar”, “fieldtype” → “Currency”, “options” → “currency”, …).

**Local steps**

- Bind local operation wrap\_in\_quotes for subsequent calls.
- If not data.
  - Return list().
- Set tuple(labels, datapoints) from tuple(list(), list()).
- If filters.get(“group\_by”).
  - Set data from list of row for row drawn from data where row at 0.
    - Draw row from data, keep a combination only if (row at 0).
- Set data from sorted(data, key = deferred anonymous expression, reverse = true).
- If len(data) &gt; 10.
  - Set data from data at slice no value to 10.
- For each row in data.
  - If row at 0 equals wrap\_in\_quotes(translated “Total”).
    - Continue with the next iteration or loop test.
  - Evaluate labels.append(row at 0).
  - Evaluate datapoints.append(row at negative 1).
- Return mapping(“data” → mapping(“labels” → labels, “datasets” → list(mapping(“name” → translated “Total Delivered Amount”, “values” → datapoints))), “type” → “bar”, “fieldtype” → “Currency”, “options” → “currency”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L6732) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L121)

<a id="op-34887fb330ba37"></a>
### Get chart data.wrap in quotes

`operation_enterprise_stock_report_delivery_note_trends_business_behavior_get_chart_data_wrap_in_quotes`

**Inputs** label.

**Explicit results** formatted text '{label}'.

**Local steps**

- Return formatted text '{label}'.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0889.json#L7395) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L122)

## Record · Delivery settings

[Record definition](../../../../data/record-types/delivery_settings.json)

<a id="op-fa22ae5af1c120"></a>
### Delivery Settings.validate

`operation_enterprise_binding_enterprise_stock_doctype_delivery_settings_delivery_settings_deliverysettings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dispatch\_attachment().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dispatch attachment](operations-009.md#op-ad66b92445adfa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L257)

<a id="op-ad66b92445adfa"></a>
### Delivery Settings.validate dispatch attachment

`operation_enterprise_binding_enterprise_stock_doctype_delivery_settings_delivery_settings_deliverysettings_validate_dispatch_attachment`

**Inputs** self.

**Record and data access** read “Print Format” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Dispatch Attachment {0} must be a Print Format for Delivery Note”.format(Platform.bold(self.dispatch\_attachment)).

**Local steps**

- If not self.dispatch\_attachment.
  - Return no value.
- If Platform.db.get\_value(“Print Format”, self.dispatch\_attachment, “doc\_type”) differs from “Delivery Note”.
  - Call the validation error handler Platform.throw(translated “Dispatch Attachment {0} must be a Print Format for Delivery Note”.format(Platform.bold(self.dispatch\_attachment))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L258)

## Record · Delivery trip

[Record definition](../../../../data/record-types/delivery_trip.json)

<a id="op-f4b72bbd7a2812"></a>
### Delivery Trip.initialize

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Record and data access** read “Global Defaults” via get\_single\_value · read “UOM Conversion Factor” via get\_value.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.default\_distance\_uom from (Platform.db.get\_single\_value(“Global Defaults”, “default\_distance\_unit”) or “Meter”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Global Defaults”, “default\_distance\_unit”) → “Meter”.
- Set self.uom\_conversion\_factor from Platform.db.get\_value(“UOM Conversion Factor”, mapping(“from\_uom” → “Meter”, “to\_uom” → self.default\_distance\_uom), “value”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “default\_distance\_unit”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L1818) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L970)

<a id="op-d984881a74b1d9"></a>
### Delivery Trip.on discard

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_on_discard`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.update\_delivery\_notes(delete = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-010.md#op-a4f8e6794f2c38), [update delivery notes](operations-010.md#op-ce086a65ec0526).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2054) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L972)

<a id="op-cd400eae2c9c2b"></a>
### Delivery Trip.after mapping

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_after_mapping`

**Inputs** self, source\_doc.

**Local steps**

- For each stop in self.delivery\_stops at slice no value to no value.
  - If not any(generator of stop.get(df.fieldname) for df drawn from stop.meta.fields).
    - Draw df from stop.meta.fields.
    - Evaluate self.remove(stop).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2136) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1486) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L967)

<a id="op-6c418691faad9e"></a>
### Delivery Trip.validate

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A driver must be set to submit.”.

**Local steps**

- If (self.\_action equals “submit” and not self.driver).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_action equals “submit” → not self.driver.
  - Call the validation error handler Platform.throw(translated “A driver must be set to submit.”).
- If self.\_action equals “submit”.
  - Evaluate self.validate\_driver().
  - Evaluate self.validate\_delivery\_note\_not\_draft().
- Evaluate self.validate\_delivery\_notes\_not\_on\_other\_trips().
- Evaluate self.validate\_stop\_addresses().
- Evaluate self.validate\_stop\_contacts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate driver](operations-010.md#op-136cd3943f4e42), [validate delivery note not draft](operations-010.md#op-2fb7c7808c3552), [validate delivery notes not on other trips](operations-010.md#op-7320c44914e1c9), [validate stop addresses](operations-009.md#op-b1a17280037b39), [validate stop contacts](operations-009.md#op-339cb6fb0bbc78).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1500) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L981)

<a id="op-087a41d6ac4b02"></a>
### Delivery Trip.on update

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_delivery\_notes().
- Evaluate self.release\_removed\_delivery\_notes().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update delivery notes](operations-010.md#op-ce086a65ec0526), [release removed delivery notes](operations-010.md#op-59bdfb429d9e4c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L975)

<a id="op-eb3d833045fd8a"></a>
### Delivery Trip.on trash

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.update\_delivery\_notes(delete = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update delivery notes](operations-010.md#op-ce086a65ec0526).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2544) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L974)

<a id="op-18c870dc9f8e65"></a>
### Delivery Trip.on submit

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-010.md#op-a4f8e6794f2c38).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2606) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L973)

<a id="op-c10132a7b866cc"></a>
### Delivery Trip.on update after submit

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_on_update_after_submit`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-010.md#op-a4f8e6794f2c38).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2657) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L976)

<a id="op-1cbfb4b712c66f"></a>
### Delivery Trip.on cancel

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.update\_status().
- Evaluate self.update\_delivery\_notes(delete = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status](operations-010.md#op-a4f8e6794f2c38), [update delivery notes](operations-010.md#op-ce086a65ec0526).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2708) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L971)

<a id="op-b1a17280037b39"></a>
### Delivery Trip.validate stop addresses

`operation_enterprise_stock_record_definitions_delivery_trip_business_behavior_delivery_trip_validate_stop_addresses`

**Inputs** self.

**Record and data access** resolve a document from “Address” via get\_doc.

**Local steps**

- For each stop in self.delivery\_stops.
  - If (stop.address and not stop.customer\_address).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in stop.address → not stop.customer\_address.
    - Set stop.customer\_address from get\_address\_display(Platform.get\_doc(“Address”, stop.address).as\_dict()).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0726.json#L2790) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L983)

<a id="op-339cb6fb0bbc78"></a>
### Delivery Trip.validate stop contacts

`operation_enterprise_binding_enterprise_stock_doctype_delivery_trip_delivery_trip_deliverytrip_validate_stop_contacts`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Contact {1} does not belong to Customer {2}”.format(stop.idx, Platform.bold(stop.contact), Platform.bold(stop.customer)).

**Local steps**

- Set stops from list of stop for stop drawn from self.delivery\_stops where (stop.contact and stop.customer).
  - Draw stop from self.delivery\_stops, keep a combination only if ((stop.contact and stop.customer)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in stop.contact → stop.customer.
- If not stops.
  - Return no value.
- Set dynamic\_link from Platform.qb.DocType(“Dynamic Link”).
- Set contact\_customers from set(nested operand in the contract.select(nested operand in the contract.parent, nested operand in the contract.link\_name).where(((nested operand in the contract equals nested operand in the contract bitwi ….
  - Draw stop from stops.
- For each stop in stops.
  - If tuple(stop.contact, stop.customer) does not belong to contact\_customers.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Contact {1} does not belong to Customer {2}”.format(stop.idx, Platform.bold(stop.contact), Platform.bold(stop.customer))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0021.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L767) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L264)
