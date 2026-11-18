# Customer support · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Service level agreement

[Record definition](../../../../data/record-types/service_level_agreement.json)

<a id="op-9df9b4efbc976b"></a>
### Get user time

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_user_time`

**Inputs** user, to\_string = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_datetime\_str(now\_datetime(user)) when to\_string, otherwise now\_datetime(user).

**Local steps**

- Return get\_datetime\_str(now\_datetime(user)) when to\_string, otherwise now\_datetime(user).
  - Value choice on to\_string — true gives get\_datetime\_str(now\_datetime(user)), false gives now\_datetime(user).

**Values supplied outside this operation** clock or generated value from now\_datetime(user).

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1212)

<a id="op-e58002b46dd2ae"></a>
### Get sla doctypes

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_get_service_level_agreement_record_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), redis\_cache().

**Record and data access** read “Service Level Agreement” via get\_all.

**Explicit results** doctypes.

**Local steps**

- Set doctypes from list().
- Set data from Platform.get\_all(“Service Level Agreement”, mapping(“enabled” → 1), list(“document\_type”), distinct = 1).
- For each entry in data.
  - Evaluate doctypes.append(entry.document\_type).
- Return doctypes.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0971.json#L411) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1208)

<a id="op-68c265fda4f725"></a>
### Add sla doctypes

`operation_enterprise_support_record_definitions_service_level_agreement_business_behavior_add_service_level_agreement_record_types`

**Inputs** bootinfo.

**Local steps**

- Set bootinfo.service\_level\_agreement\_doctypes from get\_sla\_doctypes().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0971.json#L609) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1191)

## Report · Support hour distribution

<a id="op-cc75df3a6f08ce"></a>
### Execute

`operation_enterprise_support_report_support_hour_distribution_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- If not filters.get(“periodicity”).
  - Set filters at “periodicity” from “Daily”.
- Set columns from get\_columns().
- Set tuple(data, timeslot\_wise\_count) from get\_data(filters).
- Set chart from get\_chart\_data(timeslot\_wise\_count).
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1309)

<a id="op-7ffb8d4fd72aa9"></a>
### Get data

`operation_enterprise_support_report_support_hour_distribution_business_behavior_get_data`

**Inputs** filters.

**Explicit results** tuple(data, time\_slot\_wise\_total\_count).

**Local steps**

- Set start\_date from getdate(filters.from\_date).
- Set data from list().
- Set time\_slot\_wise\_total\_count from mapping().
- While start\_date ≤ getdate(filters.to\_date).
  - Set hours\_count from mapping(“date” → start\_date).
  - For each tuple(key, value) in time\_slots.items().
    - Set start\_time from get\_datetime(“{} {}”.format(start\_date.strftime(“%Y-%m-%d”), value)).
    - Set end\_time from add\_to\_date(start\_time, hours = 3).
    - Set hours\_count at key from get\_hours\_count(start\_time, end\_time, filters.get(“company”)).
    - Set time\_slot\_wise\_total\_count at key from (time\_slot\_wise\_total\_count.get(key, 0) + hours\_count at key).
  - If hours\_count.
    - Evaluate data.append(hours\_count).
  - Set start\_date from add\_to\_date(start\_date, days = 1).
- Return tuple(data, time\_slot\_wise\_total\_count).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1312)

<a id="op-585188697949f4"></a>
### Get hours count

`operation_enterprise_support_report_support_hour_distribution_business_behavior_get_hours_count`

**Inputs** start\_time, end\_time, company = no value.

**Record and data access** read “Issue” via get\_list.

**Explicit results** Platform.get\_list(“Issue”, filters = filters, fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.

**Local steps**

- Set filters from list(list(“creation”, “&gt;=”, start\_time), list(“creation”, “&lt;”, end\_time)).
- If company.
  - Evaluate filters.append(list(“company”, “=”, company)).
- Return Platform.get\_list(“Issue”, filters = filters, fields = list(mapping(“COUNT” → “\*”, “as” → “count”))) at 0.count.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1313)

<a id="op-796d0d6a8b1cc9"></a>
### Get columns

`operation_enterprise_support_report_support_hour_distribution_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“fieldname” → “date”, “label” → translated “Date”, “fieldtype” → “Date”, “width” → 100)).
- For each label in list(“12AM - 3AM”, “3AM - 6AM”, “6AM - 9AM”, “9AM - 12PM”, …).
  - Evaluate columns.append(mapping(“fieldname” → label, “label” → translated label, “fieldtype” → “Data”, “width” → 120)).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L4774) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1311)

<a id="op-c511c1c8f9e0c5"></a>
### Get chart data

`operation_enterprise_support_report_support_hour_distribution_business_behavior_get_chart_data`

**Inputs** timeslot\_wise\_count.

**Explicit results** chart.

**Local steps**

- Set total\_count from list().
- Set timeslots from list(“12AM - 3AM”, “3AM - 6AM”, “6AM - 9AM”, “9AM - 12PM”, …).
- Set datasets from list().
- For each data in timeslots.
  - Evaluate total\_count.append(timeslot\_wise\_count.get(data, 0)).
- Evaluate datasets.append(mapping(“values” → total\_count)).
- Set chart from mapping(“data” → mapping(“labels” → timeslots, “datasets” → datasets)).
- Set chart at “type” from “line”.
- Return chart.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0975.json#L5056) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L81) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1310)

## Record · Warranty claim

[Record definition](../../../../data/record-types/warranty_claim.json)

<a id="op-70a84ace097419"></a>
### Warranty Claim.validate

`operation_enterprise_support_record_definitions_warranty_claim_business_behavior_warranty_claim_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Customer is required”.

**Local steps**

- Evaluate self.warn\_if\_serial\_no\_not\_delivered\_to\_customer().
- If (self.status equals “Cancelled” and self.has\_value\_changed(“status”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Cancelled” → self.has\_value\_changed(“status”).
  - Evaluate self.validate\_no\_active\_visits().
- If (session at “user” differs from “Guest” and not self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in session at “user” differs from “Guest” → not self.customer.
  - Call the validation error handler Platform.throw(translated “Customer is required”).
- Evaluate self.set\_resolution().
- Evaluate self.set\_warranty\_amc\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [warn if serial no not delivered to customer](operations-007.md#op-18519ab9bc3c59), [validate no active visits](operations-007.md#op-70c77819aa86dd), [set resolution](operations-007.md#op-4e775bb4536ab9), [set warranty amc status](operations-007.md#op-4748a4ff7cd279).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L37) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1273)

<a id="op-4e775bb4536ab9"></a>
### Warranty Claim.set resolution

`operation_enterprise_binding_enterprise_support_doctype_warranty_claim_warranty_claim_warrantyclaim_set_resolution`

**Inputs** self.

**Record and data access** read “Warranty Claim” via get\_value.

**Local steps**

- Set previous\_status from Platform.db.get\_value(“Warranty Claim”, self.name, “status”).
- If (self.status equals “Closed” and not self.resolution\_date and previous\_status differs from “Closed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status equals “Closed” → not self.resolution\_date → previous\_status differs from “Closed”.
  - Set self.resolution\_date from now\_datetime().
- Otherwise.
  - If (self.status differs from “Closed” and previous\_status equals “Closed”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status differs from “Closed” → previous\_status equals “Closed”.
    - Set self.resolution\_date from no value.
    - Set self.resolved\_by from no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1281)

<a id="op-4748a4ff7cd279"></a>
### Warranty Claim.set warranty amc status

`operation_enterprise_binding_enterprise_support_doctype_warranty_claim_warranty_claim_warrantyclaim_set_warranty_amc_status`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not (self.warranty\_expiry\_date or self.amc\_expiry\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.warranty\_expiry\_date → self.amc\_expiry\_date.
  - Return no value.
- Set complaint\_date from getdate(self.complaint\_date).
- Set warranty\_expiry from (self.warranty\_expiry\_date and getdate(self.warranty\_expiry\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.warranty\_expiry\_date → getdate(self.warranty\_expiry\_date).
- Set amc\_expiry from (self.amc\_expiry\_date and getdate(self.amc\_expiry\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.amc\_expiry\_date → getdate(self.amc\_expiry\_date).
- If (warranty\_expiry and warranty\_expiry ≥ complaint\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in warranty\_expiry → warranty\_expiry ≥ complaint\_date.
  - Set self.warranty\_amc\_status from “Under Warranty”.
- Otherwise.
  - If amc\_expiry.
    - Set self.warranty\_amc\_status from “Under AMC” when amc\_expiry ≥ complaint\_date, otherwise “Out of AMC”.
      - Value choice on amc\_expiry ≥ complaint\_date — true gives “Under AMC”, false gives “Out of AMC”.
  - Otherwise.
    - Set self.warranty\_amc\_status from “Out of Warranty”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1282)

<a id="op-18519ab9bc3c59"></a>
### Warranty Claim.warn if serial no not delivered to customer

`operation_enterprise_binding_enterprise_support_doctype_warranty_claim_warranty_claim_warrantyclaim_warn_if_serial_no_not_delivered_to_customer`

**Inputs** self.

**Declared result** no value.

**State and service calls** msgprint with message.

**Explicit results** no value.

**Local steps**

- If not (self.serial\_no and self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.serial\_no → self.customer.
  - Return no value.
- If not (self.has\_value\_changed(“serial\_no”) or self.has\_value\_changed(“customer”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“serial\_no”) → self.has\_value\_changed(“customer”).
  - Return no value.
- If message bound to self.get\_serial\_no\_ownership\_warning().
  - Evaluate Platform.msgprint(message, title = translated “Check Serial No”, indicator = “orange”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial no ownership warning](operations-007.md#op-6b28cd43a4b220).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L3) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1284)

<a id="op-6b28cd43a4b220"></a>
### Warranty Claim.get serial no ownership warning

`operation_enterprise_binding_enterprise_support_doctype_warranty_claim_warranty_claim_warrantyclaim_get_serial_no_ownership_warning`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Serial No” via get\_value.

**Explicit results** no value · translated “Serial No {0} was delivered to Customer {1}, not to {2}.”.format(serial\_no, Platform.bold(escape\_html(serial.customer)), Platform.bold(escape\_html(self.customer))) · translated “Serial No {0} is still in stock in Warehouse {1} and was not delivered to a customer.”.format(serial\_no, Platform.bold(escape\_html(serial.warehouse))).

**Local steps**

- Set serial from Platform.db.get\_value(“Serial No”, self.serial\_no, list(“customer”, “warehouse”), as\_dict = true).
- If not serial.
  - Return no value.
- Set serial\_no from Platform.bold(escape\_html(self.serial\_no)).
- If (serial.customer and serial.customer differs from self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial.customer → serial.customer differs from self.customer.
  - Return translated “Serial No {0} was delivered to Customer {1}, not to {2}.”.format(serial\_no, Platform.bold(escape\_html(serial.customer)), Platform.bold(escape\_html(self.customer))).
- If (not serial.customer and serial.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not serial.customer → serial.warehouse.
  - Return translated “Serial No {0} is still in stock in Warehouse {1} and was not delivered to a customer.”.format(serial\_no, Platform.bold(escape\_html(serial.warehouse))).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1280)

<a id="op-70c77819aa86dd"></a>
### Warranty Claim.validate no active visits

`operation_enterprise_binding_enterprise_support_doctype_warranty_claim_warranty_claim_warrantyclaim_validate_no_active_visits`

**Inputs** self.

**Record and data access** execute query text (SELECT, Maintenance Visit).

**Explicit failure paths** validation helper — translated “Cancel Material Visit {0} before cancelling this Warranty Claim”.format(lst1).

**Local steps**

- Set lst from Platform.db.sql(query text (SELECT, Maintenance Visit), self.name).
- If lst.
  - Set lst1 from “,”.join(generator of x at 0 for x drawn from lst).
    - Draw x from lst.
  - Call the validation error handler Platform.throw(translated “Cancel Material Visit {0} before cancelling this Warranty Claim”.format(lst1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L2) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1283)

<a id="op-abb1f7c5420ee8"></a>
### Warranty Claim.on update

`operation_enterprise_support_record_definitions_warranty_claim_business_behavior_warranty_claim_on_update`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0972.json#L6062) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L36) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1272)

<a id="op-0c61791bdfd125"></a>
### Make maintenance visit

`operation_enterprise_support_record_definitions_warranty_claim_business_behavior_make_maintenance_visit`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Maintenance Visit) · resolve a document from “Warranty Claim” via get\_doc.

**Explicit results** target\_doc.

**Local steps**

- Bind dependencies get\_mapped\_doc, map\_child\_doc.
- Bind local operation \_update\_links for subsequent calls.
- Set visit from Platform.db.sql(query text (SELECT, Maintenance Visit), source\_name).
- If not visit.
  - Set target\_doc from get\_mapped\_doc(“Warranty Claim”, source\_name, mapping(“Warranty Claim” → mapping(“doctype” → “Maintenance Visit”, “field\_map” → mapping())), target\_doc).
  - Set source\_doc from Platform.get\_doc(“Warranty Claim”, source\_name).
  - If source\_doc.get(“item\_code”).
    - Set table\_map from mapping(“doctype” → “Maintenance Visit Purpose”, “postprocess” → \_update\_links).
    - Evaluate map\_child\_doc(source\_doc, target\_doc, table\_map, source\_doc).
  - Return target\_doc.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L33) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1270)

<a id="op-ae97a6cde59e7d"></a>
### Make maintenance visit.update links

`operation_enterprise_support_record_definitions_warranty_claim_business_behavior_make_maintenance_visit_update_links`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Set target\_doc.prevdoc\_doctype from source\_parent.doctype.
- Set target\_doc.prevdoc\_docname from source\_parent.name.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0972.json#L6818) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L34) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1271)
