# Inventory and warehouses · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Quality inspection

[Record definition](../../../../data/record-types/quality_inspection.json)

<a id="op-ed40e7503621d4"></a>
### Quality Inspection.on cancel

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Set self.ignore\_linked\_doctypes from “Serial and Batch Bundle”.
- Evaluate self.update\_qc\_reference().
- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update qc reference](operations-049.md#op-dad77e12780ee7).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L383)

<a id="op-c5289589dc84f2"></a>
### Quality Inspection.on trash

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.update\_qc\_reference(remove\_reference = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update qc reference](operations-049.md#op-dad77e12780ee7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L3400) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L720) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L386)

<a id="op-08ece159940489"></a>
### Quality Inspection.validate readings status mandatory

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_validate_readings_status_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Status is mandatory”.format(reading.idx).

**Local steps**

- For each reading in self.readings.
  - If not reading.status.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Status is mandatory”.format(reading.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L3462) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L731) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L397)

<a id="op-dad77e12780ee7"></a>
### Quality Inspection.update qc reference

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_update_qc_reference`

**Inputs** self, remove\_reference = false.

**State and service calls** execute a supplied database query · request set\_value on self.reference\_type.

**Local steps**

- Set quality\_inspection from self.name when (self.docstatus &lt; 2 and not remove\_reference), otherwise empty text.
  - Value choice on (self.docstatus &lt; 2 and not remove\_reference) — true gives self.name, false gives empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus &lt; 2 → not remove\_reference.
- If self.reference\_type equals “Job Card”.
  - If self.reference\_name.
    - Evaluate Platform.db.sql(formatted text   UPDATE ′tab{self.reference\_type}′  SET quality\_inspection = %s, modified = %s  WHERE name = %s and production\_item = %s  , tuple(quality\_inspection, self.mod ….
- Otherwise.
  - Set doctype from (self.reference\_type + “ Item”).
  - If self.reference\_type equals “Stock Entry”.
    - Set doctype from “Stock Entry Detail”.
  - If (doctype and self.reference\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → self.reference\_name.
    - Set child\_doc from Platform.qb.DocType(doctype).
    - Set query from nested operand in the contract.qb.update(child\_doc).set(child\_doc.quality\_inspection, quality\_inspection).where((child\_doc.parent equals self.reference\_name bitwise and child\_doc.item\_code equals self.item\_code)).
    - If (self.batch\_no and self.docstatus &lt; 2).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.batch\_no → self.docstatus &lt; 2.
      - Set query from query.where(child\_doc.batch\_no equals self.batch\_no).
    - If (self.docstatus equals 2 or remove\_reference).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus equals 2 → remove\_reference.
      - Set query from query.where(child\_doc.quality\_inspection equals self.name).
    - Otherwise.
      - Set query from query.where(IfNull(child\_doc.quality\_inspection, empty text).isin(list(empty text, self.name))).
    - If self.child\_row\_reference.
      - Set query from query.where(child\_doc.name equals self.child\_row\_reference).
    - Evaluate query.run().
    - Evaluate Platform.db.set\_value(self.reference\_type, self.reference\_name, “modified”, self.modified).
- If (self.reference\_type and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type → self.reference\_name.
  - Evaluate Platform.get\_lazy\_doc(self.reference\_type, self.reference\_name).notify\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L727) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L393)

<a id="op-8f21c2670696d7"></a>
### Quality Inspection.inspect and set status

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_inspect_and_set_status`

**Inputs** self.

**State and service calls** msgprint with translated “Status set to rejected as there are one or more rejected readings.”.

**Local steps**

- For each reading in self.readings.
  - If not reading.manual\_inspection.
    - If reading.formula\_based\_criteria.
      - Evaluate self.set\_status\_based\_on\_acceptance\_formula(reading).
    - Otherwise.
      - Evaluate self.set\_status\_based\_on\_acceptance\_values(reading).
- If not self.manual\_inspection.
  - Set self.status from “Accepted”.
  - For each reading in self.readings.
    - If reading.status equals “Rejected”.
      - Set self.status from “Rejected”.
      - Evaluate Platform.msgprint(translated “Status set to rejected as there are one or more rejected readings.”, alert = true).
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Methods declared on this owner** [set status based on acceptance formula](operations-049.md#op-16befc1935b79a), [set status based on acceptance values](operations-049.md#op-feba4bb1a03bef).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L4565) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L381)

<a id="op-b8b540637b929f"></a>
### Quality Inspection.validate reading number format

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_validate_reading_number_format`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Reading {1} {2} is not a valid number in the {3} number format. Use {4} as the decimal separator.”.format(reading.idx, i, Platform.bold(value), Platform.bold(number\_format.string), …).

**Local steps**

- Set number\_format from get\_reading\_number\_format().
- Set tuple(decimal\_str, comma\_str) from get\_reading\_separators(number\_format).
- Set before\_save from self.get\_doc\_before\_save().
- For each reading in self.readings.
  - If (not cint(reading.numeric) or cint(reading.manual\_inspection)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cint(reading.numeric) → cint(reading.manual\_inspection).
    - Continue with the next iteration or loop test.
  - Set stored from (before\_save and before\_save.get(“readings”, mapping(“name” → reading.name))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in before\_save → before\_save.get(“readings”, mapping(“name” → reading.name)).
  - Set stored from stored at 0 when stored, otherwise no value.
    - Value choice on stored — true gives stored at 0, false gives no value.
  - For each i in range(1, 11).
    - Set field from (“reading\_” + str(i)).
    - Set value from reading.get(field).
    - If (value is identical to no value or not value.strip()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in value is identical to no value → not value.strip().
      - Continue with the next iteration or loop test.
    - If (stored and stored.get(field) equals value).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in stored → stored.get(field) equals value.
      - Continue with the next iteration or loop test.
    - If parse\_reading(value, decimal\_str, comma\_str) is identical to no value.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Reading {1} {2} is not a valid number in the {3} number format. Use {4} as the decimal separator.”.format(reading.idx, i, Platform.bold(value), Platform.bold(number\_for ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L4848) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L396)

<a id="op-feba4bb1a03bef"></a>
### Quality Inspection.set status based on acceptance values

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_set_status_based_on_acceptance_values`

**Inputs** self, reading.

**Local steps**

- If not cint(reading.numeric).
  - Set reading\_value from (reading.get(“reading\_value”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reading.get(“reading\_value”) → empty text.
  - Set value from (reading.get(“value”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reading.get(“value”) → empty text.
  - Set result from reading\_value equals value.
- Otherwise.
  - Set result from self.min\_max\_criteria\_passed(reading).
- Set reading.status from “Accepted” when result, otherwise “Rejected”.
  - Value choice on result — true gives “Accepted”, false gives “Rejected”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [min max criteria passed](operations-049.md#op-ec454346984e60).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L5537) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L726) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L392)

<a id="op-ec454346984e60"></a>
### Quality Inspection.min max criteria passed

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_minimum_maximum_criteria_passed`

**Inputs** self, reading.

**Explicit results** false · has\_reading.

**Local steps**

- Set has\_reading from false.
- For each i in range(1, 11).
  - Set reading\_value from reading.get((“reading\_” + str(i))).
  - If (reading\_value is distinct from no value and reading\_value.strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reading\_value is distinct from no value → reading\_value.strip().
    - Set has\_reading from true.
    - Set result from flt(reading.get(“min\_value”)) ≤ parse\_float(reading\_value) ≤ flt(reading.get(“max\_value”)).
      - Compare adjacent operands in order, stopping at the first false comparison in flt(reading.get(“min\_value”)) ≤ parse\_float(reading\_value) ≤ flt(reading.get(“max\_value”)).
    - If not result.
      - Return false.
- Return has\_reading.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L5780) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L382)

<a id="op-16befc1935b79a"></a>
### Quality Inspection.set status based on acceptance formula

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_set_status_based_on_acceptance_formula`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, reading.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L6104) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L725) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L391)

<a id="op-8a011d91081915"></a>
### Quality Inspection.get formula evaluation data

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_get_formula_evaluation_data`

**Inputs** self, reading.

**Explicit results** data.

**Local steps**

- Set data from mapping().
- If not cint(reading.numeric).
  - Set data from mapping(“reading\_value” → reading.get(“reading\_value”)).
- Otherwise.
  - For each i in range(1, 11).
    - Set field from (“reading\_” + str(i)).
    - If reading.get(field) is identical to no value.
      - Set data at field from 0.0.
      - Continue with the next iteration or loop test.
    - Set data at field from parse\_float(reading.get(field)).
  - Set data at “mean” from self.calculate\_mean(reading).
- Return data.

**Methods declared on this owner** [calculate mean](operations-049.md#op-caeb620cd77477).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L6616) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L378)

<a id="op-caeb620cd77477"></a>
### Quality Inspection.calculate mean

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_calculate_mean`

**Inputs** self, reading.

**Explicit results** actual\_mean.

**Local steps**

- Bind dependencies mean.
- Set readings\_list from list().
- For each i in range(1, 11).
  - Set reading\_value from reading.get((“reading\_” + str(i))).
  - If (reading\_value is distinct from no value and reading\_value.strip()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reading\_value is distinct from no value → reading\_value.strip().
    - Evaluate readings\_list.append(parse\_float(reading\_value)).
- Set actual\_mean from mean(readings\_list) when readings\_list, otherwise 0.
  - Value choice on readings\_list — true gives mean(readings\_list), false gives 0.
- Return actual\_mean.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0796.json#L6969) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L377)

<a id="op-076310eea0ea56"></a>
### Item query

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Job Card” via get\_list · read “Stock Entry” via get\_list · read “Item” via get\_list.

**Explicit results** list() · Platform.get\_list(“Job Card”, filters = mapping(“name” → reference\_name), fields = list(“production\_item”, “item\_name”), as\_list = true) · query.run().

**Local steps**

- Set reference\_doctype from filters.get(“reference\_doctype”).
- Set reference\_name from filters.get(“reference\_name”).
- If (not reference\_doctype or not reference\_name or not isinstance(reference\_name, str)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not reference\_doctype → not reference\_name → not isinstance(reference\_name, str).
  - Return list().
- Otherwise.
  - If reference\_doctype equals “Job Card”.
    - Return Platform.get\_list(“Job Card”, filters = mapping(“name” → reference\_name), fields = list(“production\_item”, “item\_name”), as\_list = true).
  - Otherwise.
    - Set my\_filters from list(list(“items.parent”, “=”, reference\_name), “and”, list(“items.item\_code”, “like”, formatted text %{txt}%), “and”, …).
    - Set require\_distinct\_warehouse from false.
    - If reference\_doctype equals “Stock Entry”.
      - Set purposes from Platform.get\_list(“Stock Entry”, filters = mapping(“name” → reference\_name), pluck = “purpose”).
      - Set purpose from purposes at 0 when purposes, otherwise no value.
        - Value choice on purposes — true gives purposes at 0, false gives no value.
      - Evaluate my\_filters.extend(list(“and”, list(“items.secondary\_item\_type”, “is”, “not set”), “and”, list(“items.valuation\_type”, “is”, “not set”))).
      - If purpose equals “Manufacture”.
        - Evaluate my\_filters.extend(list(“and”, list(“items.is\_finished\_item”, “=”, 1))).
      - Otherwise.
        - If purpose belongs to QI\_INCOMING\_PURPOSES.
          - Evaluate my\_filters.extend(list(“and”, list(“items.t\_warehouse”, “is”, “set”))).
        - Otherwise.
          - If purpose belongs to QI\_OUTGOING\_PURPOSES.
            - Evaluate my\_filters.extend(list(“and”, list(“items.s\_warehouse”, “is”, “set”))).
            - Set require\_distinct\_warehouse from true.
          - Otherwise.
            - Return list().
    - Otherwise.
      - If filters.get(“inspection\_type”) differs from “In Process”.
        - Evaluate my\_filters.extend(list(“and”, list(“items.item\_code”, “in”, Platform.get\_list(“Item”, filters = mapping(“inspection\_required\_before\_purchase” when nested operand in the contract equals nested operand in th ….
          - Value choice on filters.get(“inspection\_type”) equals “Incoming” — true gives “inspection\_required\_before\_purchase”, false gives “inspection\_required\_before\_delivery”.
    - Set query from Platform.get\_query(reference\_doctype, fields = list(“items.item\_code, items.item\_name”), filters = my\_filters, offset = start, limit = page\_len, …).
    - If require\_distinct\_warehouse.
      - Set child from Platform.qb.DocType(Platform.get\_meta(reference\_doctype).get\_field(“items”).options).
      - Set query from query.where((child.t\_warehouse.isnull() bitwise or child.s\_warehouse differs from child.t\_warehouse)).
    - Return query.run().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L371)

<a id="op-477de21a4310fe"></a>
### Quality inspection query

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_quality_inspection_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Quality Inspection” via get\_list.

**Explicit results** Platform.get\_list(“Quality Inspection”, limit\_start = start, limit\_page\_length = page\_len, filters = mapping(“docstatus” → tuple(“&lt;”, 2), “name” → tuple(“like”, (“%%%s%%” modulo or format txt)), “item\_code ….

**Local steps**

- Return Platform.get\_list(“Quality Inspection”, limit\_start = start, limit\_page\_length = page\_len, filters = mapping(“docstatus” → tuple(“&lt;”, 2), “name” → tuple(“like”, (“%%%s%%” modulo or format txt)), “item\_code ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L388)

<a id="op-42ecabc834a27a"></a>
### Make quality inspection

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_make_quality_inspection`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doc.

**Local steps**

- Bind local operation postprocess for subsequent calls.
- Set doc from get\_mapped\_doc(“BOM”, source\_name, mapping(“BOM” → mapping(“doctype” → “Quality Inspection”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_map” → mapping(“name” → “bom\_no”, “item” → “item\_code ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L372)

<a id="op-5eee43bcdae528"></a>
### Make quality inspection.postprocess

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_make_quality_inspection_postprocess`

**Inputs** source, doc.

**Local steps**

- Set doc.inspected\_by from Platform.session.user.
- Evaluate doc.get\_quality\_inspection\_template().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0797.json#L2189) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L373)

<a id="op-119abfe5122358"></a>
### Get reading number format

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_get_reading_number_format`

**Inputs** no declared parameters.

**Declared result** NumberFormat.

**Explicit results** NumberFormat.from\_string(number\_format).

**Local steps**

- Set number\_format from Platform.defaults.get\_user\_default(“number\_format”).
- If number\_format does not belong to NUMBER\_FORMAT\_MAP.
  - Set number\_format from “#,###.##”.
- Return NumberFormat.from\_string(number\_format).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0797.json#L2270) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L369)

<a id="op-9903d20048ea26"></a>
### Get reading separators

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_get_reading_separators`

**Inputs** number\_format.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(decimal\_str, empty text when comma\_str equals decimal\_str, otherwise comma\_str).

**Local steps**

- Set decimal\_str from (number\_format.decimal\_separator or “.”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in number\_format.decimal\_separator → “.”.
- Set comma\_str from number\_format.thousands\_separator.
- Return tuple(decimal\_str, empty text when comma\_str equals decimal\_str, otherwise comma\_str).
  - Value choice on comma\_str equals decimal\_str — true gives empty text, false gives comma\_str.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0797.json#L2394) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L370)

<a id="op-854075f36e4204"></a>
### Parse reading

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_parse_reading`

**Inputs** value, decimal\_str, comma\_str.

**Declared result** (float bitwise or no value).

**Explicit results** no value · number when isfinite(number), otherwise no value.

**Local steps**

- Set value from value.strip().
- Set integer\_part from value.partition(decimal\_str) at 0.
- If (comma\_str and comma\_str belongs to integer\_part).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in comma\_str → comma\_str belongs to integer\_part.
  - Set groups from integer\_part.split(comma\_str).
  - Set lead from groups at 0 at slice 1 to no value when groups at 0 at slice no value to 1 belongs to tuple(“+”, “-”), otherwise groups at 0.
    - Value choice on groups at 0 at slice no value to 1 belongs to tuple(“+”, “-”) — true gives groups at 0 at slice 1 to no value, false gives groups at 0.
  - If (not 1 ≤ len(lead) ≤ 3 or len(groups at negative 1) differs from 3).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not 1 ≤ len(lead) ≤ 3 → len(groups at negative 1) differs from 3.
    - Compare adjacent operands in order, stopping at the first false comparison in 1 ≤ len(lead) ≤ 3.
    - Return no value.
  - If any(generator of len(group) does not belong to tuple(2, 3) for group drawn from groups at slice 1 to negative 1).
    - Draw group from groups at slice 1 to negative 1.
    - Return no value.
  - Set value from value.replace(comma\_str, empty text).
- If decimal\_str differs from “.”.
  - Set value from value.replace(decimal\_str, “.”).
- Attempt the following.
  - Set number from float(value).
- On failure (ValueError).
  - Return no value.
- Return number when isfinite(number), otherwise no value.
  - Value choice on isfinite(number) — true gives number, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0797.json#L2529) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L375)

<a id="op-1cf05e811e604a"></a>
### Parse float

`operation_enterprise_stock_record_definitions_quality_inspection_business_behavior_parse_decimal`

**Inputs** num.

**Declared result** float.

**Explicit results** flt(parse\_reading(num, decimal\_str, comma\_str)).

**Local steps**

- Set tuple(decimal\_str, comma\_str) from get\_reading\_separators(get\_reading\_number\_format()).
- Return flt(parse\_reading(num, decimal\_str, comma\_str)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0797.json#L3179) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L374)

<a id="op-ba366bf3710424"></a>
### Validate qi reference

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_quality_inspection_validate_qi_reference`

**Inputs** doc, row, item\_code = no value.

**Record and data access** read “Quality Inspection” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Please select a valid Quality Inspection with Reference Type {1} and Reference Name {2}.”.format(row.idx, Platform.bold(doc.doctype), Platform.bold(doc.name)) · validation helper — translated “Row #{0}: Please select a valid Quality Inspection with Item Code {1}.”.format(row.idx, Platform.bold((item\_code or row.item\_code))).

**Local steps**

- If not row.get(“quality\_inspection”).
  - Return no value.
- Set qi from Platform.db.get\_value(“Quality Inspection”, row.quality\_inspection, list(“reference\_type”, “reference\_name”, “item\_code”), as\_dict = true).
- If not qi.
  - Return no value.
- If (qi.reference\_type differs from doc.doctype or qi.reference\_name differs from doc.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in qi.reference\_type differs from doc.doctype → qi.reference\_name differs from doc.name.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Please select a valid Quality Inspection with Reference Type {1} and Reference Name {2}.”.format(row.idx, Platform.bold(doc.doctype), Platform.bold(doc.name))).
- If qi.item\_code differs from (item\_code or row.item\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_code → row.item\_code.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Please select a valid Quality Inspection with Item Code {1}.”.format(row.idx, Platform.bold((item\_code or row.item\_code)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_code → row.item\_code.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1052) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L549)

## Record · Quality inspection template

[Record definition](../../../../data/record-types/quality_inspection_template.json)

<a id="op-e8780deddf7a77"></a>
### Quality Inspection Template.validate

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_template_quality_inspection_template_qualityinspectiontemplate_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_duplicate\_parameters().
- For each row in self.item\_quality\_inspection\_parameter.
  - Evaluate self.validate\_acceptance\_formula(row).
  - Evaluate self.validate\_acceptance\_values(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate duplicate parameters](operations-049.md#op-4947383f7d1401), [validate acceptance formula](operations-049.md#op-ac0e11c7e9c7b7), [validate acceptance values](operations-049.md#op-9348f0a14318cf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1053) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L550)

<a id="op-4947383f7d1401"></a>
### Quality Inspection Template.validate duplicate parameters

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_template_quality_inspection_template_qualityinspectiontemplate_validate_duplicate_parameters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Parameter {1} is added more than once”.format(row.idx, Platform.bold(row.specification)).

**Local steps**

- Set parameters from set().
- For each row in self.item\_quality\_inspection\_parameter.
  - If row.specification belongs to parameters.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Parameter {1} is added more than once”.format(row.idx, Platform.bold(row.specification))).
  - Evaluate parameters.add(row.specification).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1056) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L553)

<a id="op-9348f0a14318cf"></a>
### Quality Inspection Template.validate acceptance values

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_template_quality_inspection_template_qualityinspectiontemplate_validate_acceptance_values`

**Inputs** self, row.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Minimum Value cannot be greater than Maximum Value for parameter {1}”.format(row.idx, Platform.bold(row.specification)) · validation helper — translated “Row #{0}: Acceptance Criteria Value is required for parameter {1}”.format(row.idx, Platform.bold(row.specification)).

**Local steps**

- If row.formula\_based\_criteria.
  - Return no value.
- If (row.numeric and flt(row.min\_value) &gt; flt(row.max\_value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.numeric → flt(row.min\_value) &gt; flt(row.max\_value).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Minimum Value cannot be greater than Maximum Value for parameter {1}”.format(row.idx, Platform.bold(row.specification))).
- If (not row.numeric and not row.value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.numeric → not row.value.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Acceptance Criteria Value is required for parameter {1}”.format(row.idx, Platform.bold(row.specification))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1055) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L552)

<a id="op-ac0e11c7e9c7b7"></a>
### Quality Inspection Template.validate acceptance formula

`operation_enterprise_binding_enterprise_stock_doctype_quality_inspection_template_quality_inspection_template_qualityinspectiontemplate_validate_acceptance_formula`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Acceptance Criteria Formula is required for parameter {1}”.format(row.idx, Platform.bold(row.specification)).

**Local steps**

- If (row.formula\_based\_criteria and not cstr(row.acceptance\_formula).strip()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.formula\_based\_criteria → not cstr(row.acceptance\_formula).strip().
  - Call the validation error handler Platform.throw(translated “Row #{0}: Acceptance Criteria Formula is required for parameter {1}”.format(row.idx, Platform.bold(row.specification))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1054) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L551)
