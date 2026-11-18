# Equipment maintenance · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Maintenance schedule

[Record definition](../../../../data/record-types/maintenance_schedule.json)

<a id="op-c1db5e508cb9d4"></a>
### Maintenance Schedule.generate schedule

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_generate_schedule`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value.

**Local steps**

- <a id="op-c1db5e508cb9d4-guard-2"></a>If self.docstatus differs from 0.
  - Return no value.
- Evaluate self.set(“schedules”, list()).
- Set count from 1.
- For each d in self.get(“items”).
  - Evaluate self.validate\_maintenance\_detail().
  - Set s\_list from list().
  - Set s\_list from self.create\_schedule\_list(d.start\_date, d.end\_date, d.no\_of\_visits, d.sales\_person).
  - For each i in range(d.no\_of\_visits).
    - Set child from self.append(“schedules”).
    - Set child.item\_code from d.item\_code.
    - Set child.item\_name from d.item\_name.
    - Set child.scheduled\_date from s\_list at i.strftime(“%Y-%m-%d”).
    - If d.serial\_no.
      - Set child.serial\_no from d.serial\_no.
    - Set child.idx from count.
    - Set count from (count + 1).
    - Set child.sales\_person from d.sales\_person.
    - Set child.completion\_status from “Pending”.
    - Set child.item\_reference from d.name.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 0, self.docstatus = 1 (submitted) selects the branch that returns no value. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c1db5e508cb9d4-guard-2)

**Methods declared on this owner** [validate maintenance detail](operations-001.md#op-aaf3701ce5fbc5), [create schedule list](operations-001.md#op-5823bab8d6cabb).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0448.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L97)

<a id="op-ebdef7a970e119"></a>
### Maintenance Schedule.validate end date visits

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_end_date_visits`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set days\_in\_period from mapping(“Weekly” → 7, “Monthly” → 30, “Quarterly” → 91, “Half Yearly” → 182, …).
- For each item in self.items.
  - If (item.periodicity and item.periodicity differs from “Random” and item.start\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.periodicity → item.periodicity differs from “Random” → item.start\_date.
    - Set days from days\_in\_period at item.periodicity.
    - If not item.end\_date.
      - Set item.end\_date from add\_days(item.start\_date, ((item.no\_of\_visits or 1) × days)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.no\_of\_visits → 1.
    - Set no\_of\_visits from round(((date\_diff(item.end\_date, item.start\_date) + 1) ÷ days)).
    - If not item.no\_of\_visits.
      - Set item.no\_of\_visits from no\_of\_visits.
    - Otherwise.
      - If item.no\_of\_visits differs from no\_of\_visits.
        - Evaluate throw(translated “Row {0}: {1} {2} visits need an End Date of {3}. Change the End Date or the Number of Visits.”.format(item.idx, item.no\_of\_visits, translated item.periodicity, formatdate(add\_days(item.start\_da …).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L204) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L105)

<a id="op-3957081f03f1ed"></a>
### Maintenance Schedule.on submit

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc · resolve a document from “Sales Person” via get\_doc · read “Maintenance Schedule Detail” via get\_all · resolve a document from mapping(“doctype” → “Event”, “subject” → description, “description” → description, “starts\_on” → (cstr(key at “scheduled\_date”) + “ 10:00:00”), …) via get\_doc.

**State and service calls** msgprint with translated “Setting Events to {0}, since the Employee attached to the below Sales Persons does not have a User ID{1}”.format(self.owner, (text in the contract + text in the contract.join(no\_email\_sp))) · call insert on event · call db\_set on self.

**Local steps**

- If not self.get(“schedules”).
  - Evaluate throw(translated “Please click on 'Generate Schedule' to get schedule”).
- Evaluate self.check\_serial\_no\_added().
- Evaluate self.validate\_schedule().
- Set email\_map from mapping().
- For each d in self.get(“items”).
  - If d.serial\_and\_batch\_bundle.
    - Set serial\_nos from Platform.get\_doc(“Serial and Batch Bundle”, d.serial\_and\_batch\_bundle).get\_serial\_nos().
    - If serial\_nos.
      - Evaluate self.validate\_serial\_no(d.item\_code, serial\_nos, d.start\_date).
      - Evaluate self.update\_amc\_date(serial\_nos, d.end\_date).
  - Set no\_email\_sp from list().
  - If (d.sales\_person and d.sales\_person does not belong to email\_map).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.sales\_person → d.sales\_person does not belong to email\_map.
    - Set sp from Platform.get\_doc(“Sales Person”, d.sales\_person).
    - Attempt the following.
      - Set email\_map at d.sales\_person from sp.get\_email\_id().
    - On failure (Platform.ValidationError).
      - Evaluate no\_email\_sp.append(d.sales\_person).
  - If no\_email\_sp.
    - Evaluate Platform.msgprint(translated “Setting Events to {0}, since the Employee attached to the below Sales Persons does not have a User ID{1}”.format(self.owner, (text in the contract + text in the contract.join( ….
  - Set scheduled\_date from Platform.db.get\_all(“Maintenance Schedule Detail”, mapping(“parent” → self.name, “item\_reference” → d.name), list(“scheduled\_date”), as\_list = false).
  - For each key in scheduled\_date.
    - Set description from Platform.\_(“Reference: {0}, Item Code: {1} and Customer: {2}”).format(self.name, d.item\_code, self.customer).
    - Set event from Platform.get\_doc(mapping(“doctype” → “Event”, “subject” → description, “description” → description, “starts\_on” → (cstr(key at “scheduled\_date”) + “ 10:00:00”), …)).
    - Evaluate event.add\_participant(self.doctype, self.name).
    - If email\_map.get(d.sales\_person).
      - Evaluate event.append(“event\_participants”, mapping(“reference\_doctype” → “Sales Person”, “reference\_docname” → d.sales\_person, “email” → email\_map at d.sales\_person)).
    - Evaluate event.insert(ignore\_permissions = 1).
- Evaluate self.db\_set(“status”, “Submitted”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check serial no added](operations-001.md#op-055b60302ed2d4), [validate schedule](operations-001.md#op-816151b3055e71), [validate serial no](operations-001.md#op-c3d958b2d051e9), [update amc date](operations-001.md#op-3a24ed88240890).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L100)

<a id="op-5823bab8d6cabb"></a>
### Maintenance Schedule.create schedule list

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_create_schedule_list`

**Inputs** self, start\_date, end\_date, no\_of\_visit, sales\_person.

**Explicit results** schedule\_list.

**Local steps**

- Set schedule\_list from list().
- Set start\_date\_copy from start\_date.
- Set date\_diff from (getdate(end\_date) − getdate(start\_date)).days.
- Set add\_by from (date\_diff ÷ no\_of\_visit).
- For each \_visit in range(cint(no\_of\_visit)).
  - If getdate(start\_date\_copy) &lt; getdate(end\_date).
    - Set start\_date\_copy from add\_days(start\_date\_copy, add\_by).
    - If len(schedule\_list) &lt; no\_of\_visit.
      - Set schedule\_date from self.validate\_schedule\_date\_for\_holiday\_list(getdate(start\_date\_copy), sales\_person, start\_date).
      - If schedule\_date &gt; getdate(end\_date).
        - If schedule\_date differs from getdate(start\_date\_copy).
          - Evaluate throw(translated “Every day from {0} to {1} is a holiday for Sales Person {2}.”.format(formatdate(start\_date), formatdate(end\_date), sales\_person)).
        - Set schedule\_date from getdate(end\_date).
      - Evaluate schedule\_list.append(schedule\_date).
- Return schedule\_list.

**Methods declared on this owner** [validate schedule date for holiday list](operations-001.md#op-63a1c33d3c32ae).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L96)

<a id="op-63a1c33d3c32ae"></a>
### Maintenance Schedule.validate schedule date for holiday list

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_schedule_date_for_holiday_list`

**Inputs** self, schedule\_date, sales\_person, start\_date.

**Record and data access** read “Sales Person” via get\_value · read “Company” via get\_cached\_value.

**Explicit results** working\_date.

**Local steps**

- Set employee from Platform.db.get\_value(“Sales Person”, sales\_person, “employee”).
- If employee.
  - Set holiday\_list from get\_holiday\_list\_for\_employee(employee, raise\_exception = false).
- Otherwise.
  - Set holiday\_list from Platform.get\_cached\_value(“Company”, self.company, “default\_holiday\_list”).
- Set holidays from Platform.db.sql\_list(query text (SELECT, Holiday), holiday\_list).
- Set working\_date from schedule\_date.
- While working\_date belongs to holidays.
  - Set working\_date from add\_days(working\_date, negative 1).
- If working\_date &lt; getdate(start\_date).
  - Set working\_date from schedule\_date.
  - While working\_date belongs to holidays.
    - Set working\_date from add\_days(working\_date, 1).
- Return working\_date.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_holiday\_list”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L111)

<a id="op-aaf3701ce5fbc5"></a>
### Maintenance Schedule.validate maintenance detail

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_maintenance_detail`

**Inputs** self.

**Local steps**

- If not self.get(“items”).
  - Evaluate throw(translated “Please enter Maintenance Details first”).
- For each d in self.get(“items”).
  - If not d.item\_code.
    - Evaluate throw(translated “Please select item code”).
  - Otherwise.
    - If (not d.start\_date or not d.end\_date).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not d.start\_date → not d.end\_date.
      - Evaluate throw(translated “Please select Start Date and End Date for Item {0}”.format(d.item\_code)).
    - Otherwise.
      - If not d.no\_of\_visits.
        - Evaluate throw(translated “Please mention no of visits required”).
  - If getdate(d.start\_date) ≥ getdate(d.end\_date).
    - Evaluate throw(translated “Start date should be less than end date for Item {0}”.format(d.item\_code)).
  - If d.no\_of\_visits &gt; date\_diff(d.end\_date, d.start\_date).
    - Evaluate throw(translated “Row {0}: Number of visits can not be more than the {1} days between Start and End Date”.format(d.idx, date\_diff(d.end\_date, d.start\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L206) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L107)

<a id="op-4f012ca9041d5b"></a>
### Maintenance Schedule.validate sales order

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_sales_order`

**Inputs** self.

**Record and data access** execute query text (SELECT, Maintenance Schedule).

**Local steps**

- For each d in self.get(“items”).
  - If d.sales\_order.
    - Set chk from Platform.db.sql(query text (SELECT, Maintenance Schedule), d.sales\_order).
    - If chk.
      - Evaluate throw(translated “Maintenance Schedule {0} exists against {1}”.format(chk at 0 at 0, d.sales\_order)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L109)

<a id="op-84ea43f194eb14"></a>
### Maintenance Schedule.validate items table change

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_items_table_change`

**Inputs** self.

**Explicit results** no value · true.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- For each tuple(prev\_item, item) in zip(doc\_before\_save.items, self.items, strict = false).
  - Set fields from list(“item\_code”, “start\_date”, “end\_date”, “periodicity”, …).
  - For each field in fields.
    - Set b\_doc from prev\_item.as\_dict().
    - Set doc from item.as\_dict().
    - If cstr(b\_doc at field) differs from cstr(doc at field).
      - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0448.json#L4577) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L205) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L106)

<a id="op-c710f3458fb7ba"></a>
### Maintenance Schedule.validate no of visits

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_number_of_visits`

**Inputs** self.

**Explicit results** len(self.schedules) differs from sum(generator of d.no\_of\_visits for d drawn from self.items).

**Local steps**

- Return len(self.schedules) differs from sum(generator of d.no\_of\_visits for d drawn from self.items).
  - Draw d from self.items.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0448.json#L4921) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L108)

<a id="op-98e1837f594741"></a>
### Maintenance Schedule.validate

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_end\_date\_visits().
- Evaluate self.validate\_maintenance\_detail().
- Evaluate self.validate\_sales\_order().
- Evaluate self.validate\_serial\_no\_bundle().
- If (not self.schedules or self.validate\_items\_table\_change() or self.validate\_no\_of\_visits()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.schedules → self.validate\_items\_table\_change() → self.validate\_no\_of\_visits().
  - Evaluate self.generate\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate end date visits](operations-001.md#op-ebdef7a970e119), [validate maintenance detail](operations-001.md#op-aaf3701ce5fbc5), [validate sales order](operations-001.md#op-4f012ca9041d5b), [validate serial no bundle](operations-001.md#op-326ecef2d75314), [validate items table change](operations-001.md#op-84ea43f194eb14), [validate no of visits](operations-001.md#op-c710f3458fb7ba), [generate schedule](operations-001.md#op-c1db5e508cb9d4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L104)

<a id="op-326ecef2d75314"></a>
### Maintenance Schedule.validate serial no bundle

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_serial_number_bundle`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- Set ids from list of d.serial\_and\_batch\_bundle for d drawn from self.items where d.serial\_and\_batch\_bundle.
  - Draw d from self.items, keep a combination only if (d.serial\_and\_batch\_bundle).
- If not ids.
  - Return no value.
- Set voucher\_nos from Platform.get\_all(“Serial and Batch Bundle”, fields = list(“name”, “voucher\_type”), filters = mapping(“name” → tuple(“in”, ids))).
- For each row in voucher\_nos.
  - If row.voucher\_type differs from “Maintenance Schedule”.
    - Set msg from formatted text Serial and Batch Bundle {row.name}  should have voucher type as 'Maintenance Schedule'.
    - Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L113)

<a id="op-18bfdeb5d4056a"></a>
### Maintenance Schedule.on update

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_on_update`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Draft”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0448.json#L5543) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L200) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L102)

<a id="op-3a24ed88240890"></a>
### Maintenance Schedule.update amc date

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_update_annual_maintenance_contract_date`

**Inputs** self, serial\_nos, amc\_expiry\_date = no value.

**Record and data access** resolve a document from “Serial No” via get\_doc.

**State and service calls** call save on serial\_no\_doc.

**Local steps**

- For each serial\_no in serial\_nos.
  - Set serial\_no\_doc from Platform.get\_doc(“Serial No”, serial\_no).
  - Set serial\_no\_doc.amc\_expiry\_date from amc\_expiry\_date.
  - Evaluate serial\_no\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L201) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L103)

<a id="op-c3d958b2d051e9"></a>
### Maintenance Schedule.validate serial no

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_serial_number`

**Inputs** self, item\_code, serial\_nos, amc\_start\_date.

**Record and data access** read “Serial No” via get\_value.

**Explicit failure paths** validation helper — translated “Serial No {0} not found”.format(serial\_no) · validation helper — translated “Serial No {0} does not belong to Item {1}”.format(Platform.bold(serial\_no), Platform.bold(item\_code)).

**Local steps**

- Set delivery\_dates from self.get\_delivery\_dates(item\_code, serial\_nos).
- For each serial\_no in serial\_nos.
  - Set sr\_details from Platform.db.get\_value(“Serial No”, serial\_no, list(“serial\_no”, “warranty\_expiry\_date”, “amc\_expiry\_date”, “warehouse”, …), as\_dict = 1).
  - If not sr\_details.
    - Call the validation error handler Platform.throw(translated “Serial No {0} not found”.format(serial\_no)).
  - If sr\_details.get(“item\_code”) differs from item\_code.
    - Call the validation error handler Platform.throw(translated “Serial No {0} does not belong to Item {1}”.format(Platform.bold(serial\_no), Platform.bold(item\_code)), title = translated “Invalid”).
  - If (sr\_details.warranty\_expiry\_date and getdate(sr\_details.warranty\_expiry\_date) ≥ getdate(amc\_start\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sr\_details.warranty\_expiry\_date → getdate(sr\_details.warranty\_expiry\_date) ≥ getdate(amc\_start\_date).
    - Evaluate throw(translated “Serial No {0} is under warranty upto {1}”.format(serial\_no, sr\_details.warranty\_expiry\_date)).
  - If (sr\_details.amc\_expiry\_date and getdate(sr\_details.amc\_expiry\_date) ≥ getdate(amc\_start\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sr\_details.amc\_expiry\_date → getdate(sr\_details.amc\_expiry\_date) ≥ getdate(amc\_start\_date).
    - Evaluate throw(translated “Serial No {0} is under maintenance contract upto {1}”.format(serial\_no, sr\_details.amc\_expiry\_date)).
  - Evaluate validate\_serial\_no\_for\_customer(sr\_details, self.customer).
  - Set delivery\_date from delivery\_dates.get(serial\_no).
  - If (delivery\_date and getdate(delivery\_date) ≥ getdate(amc\_start\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in delivery\_date → getdate(delivery\_date) ≥ getdate(amc\_start\_date).
    - Evaluate throw(translated “Maintenance start date can not be before delivery date for Serial No {0}”.format(serial\_no)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get delivery dates](operations-001.md#op-2d69f6236cc196).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L112)

<a id="op-2d69f6236cc196"></a>
### Maintenance Schedule.get delivery dates

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_schedule_maintenance_schedule_maintenanceschedule_get_delivery_dates`

**Inputs** self, item\_code, serial\_nos.

**Explicit results** dates.

**Local steps**

- Set bundle from Platform.qb.DocType(“Serial and Batch Bundle”).
- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….
- Set dates from mapping of row.serial\_no → row.posting\_datetime for row drawn from rows.
  - Draw row from rows.
- If missing bound to list of serial\_no for serial\_no drawn from serial\_nos where serial\_no does not belong to dates.
  - Draw serial\_no from serial\_nos, keep a combination only if (serial\_no does not belong to dates).
  - Evaluate dates.update(get\_legacy\_delivery\_dates(item\_code, missing)).
- Return dates.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L595)

<a id="op-816151b3055e71"></a>
### Maintenance Schedule.validate schedule

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_validate_schedule`

**Inputs** self.

**Local steps**

- Set item\_lst1 from list().
- Set item\_lst2 from list().
- For each d in self.get(“items”).
  - If d.item\_code does not belong to item\_lst1.
    - Evaluate item\_lst1.append(d.item\_code).
- For each m in self.get(“schedules”).
  - If m.item\_code does not belong to item\_lst2.
    - Evaluate item\_lst2.append(m.item\_code).
- If len(item\_lst1) differs from len(item\_lst2).
  - Evaluate throw(translated “Maintenance Schedule is not generated for all the items. Please click on 'Generate Schedule'”).
- Otherwise.
  - For each x in item\_lst1.
    - If x does not belong to item\_lst2.
      - Evaluate throw(translated “Please click on 'Generate Schedule'”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0449.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L110)

<a id="op-055b60302ed2d4"></a>
### Maintenance Schedule.check serial no added

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_check_serial_number_added`

**Inputs** self.

**Local steps**

- Set serial\_present from list().
- For each d in self.get(“items”).
  - If d.serial\_no.
    - Evaluate serial\_present.append(d.item\_code).
- For each m in self.get(“schedules”).
  - If serial\_present.
    - If (m.item\_code belongs to serial\_present and not m.serial\_no).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in m.item\_code belongs to serial\_present → not m.serial\_no.
      - Evaluate throw(translated “Please click on 'Generate Schedule' to fetch Serial No added for Item {0}”.format(m.item\_code)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0449.json#L392) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L95)

<a id="op-ecd1793589b168"></a>
### Maintenance Schedule.on cancel

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “Serial and Batch Bundle” via get\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- For each d in self.get(“items”).
  - If d.serial\_and\_batch\_bundle.
    - Set serial\_nos from Platform.get\_doc(“Serial and Batch Bundle”, d.serial\_and\_batch\_bundle).get\_serial\_nos().
    - If serial\_nos.
      - Set expiry\_dates from self.get\_other\_amc\_expiry\_dates(d.item\_code, serial\_nos).
      - For each serial\_no in serial\_nos.
        - Evaluate self.update\_amc\_date(list(serial\_no), expiry\_dates.get(serial\_no)).
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate delete\_events(self.doctype, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get other amc expiry dates](operations-001.md#op-ee95c8316bd3af), [update amc date](operations-001.md#op-3a24ed88240890).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L99)

<a id="op-ee95c8316bd3af"></a>
### Maintenance Schedule.get other amc expiry dates

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_schedule_maintenance_schedule_maintenanceschedule_get_other_amc_expiry_dates`

**Inputs** self, item\_code, serial\_nos.

**Record and data access** read “Maintenance Schedule Item” via get\_all.

**Explicit results** mapping() · expiry\_dates.

**Local steps**

- Set rows from Platform.get\_all(“Maintenance Schedule Item”, filters = mapping(“item\_code” → item\_code, “docstatus” → 1, “parent” → tuple(“!=”, self.name), “serial\_and\_batch\_bundle” → tuple(“is”, “set”)), fields = list(“ ….
- If not rows.
  - Return mapping().
- Set bundle\_serial\_nos from get\_serial\_nos\_from\_sle\_list(list of row.serial\_and\_batch\_bundle for row drawn from rows).
  - Draw row from rows.
- Set expiry\_dates from mapping().
- For each row in rows.
  - For each serial\_no in set(bundle\_serial\_nos.get(row.serial\_and\_batch\_bundle, list())).intersection(serial\_nos).
    - Set expiry\_dates at serial\_no from max(row.end\_date, expiry\_dates.get(serial\_no, row.end\_date)).
- Return expiry\_dates.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L596)

<a id="op-d343cb0853acc8"></a>
### Maintenance Schedule.on trash

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_on_trash`

**Inputs** self.

**Local steps**

- Evaluate delete\_events(self.doctype, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0449.json#L895) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L101)

<a id="op-e614051401637e"></a>
### Maintenance Schedule.get pending data

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_maintenance_schedule_get_pending_data`

**Inputs** self, data\_type, s\_date = no value, item\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** dates · items · schedule.name.

**Local steps**

- If data\_type equals “date”.
  - Set dates from empty text.
  - For each schedule in self.schedules.
    - If (schedule.item\_name equals item\_name and schedule.completion\_status equals “Pending”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule.item\_name equals item\_name → schedule.completion\_status equals “Pending”.
      - Set dates from ((dates + whitespace '\\n') + formatdate(schedule.scheduled\_date, “dd-MM-yyyy”)).
  - Return dates.
- Otherwise.
  - If data\_type equals “items”.
    - Set items from empty text.
    - For each item in self.items.
      - For each schedule in self.schedules.
        - If (item.item\_name equals schedule.item\_name and schedule.completion\_status equals “Pending”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_name equals schedule.item\_name → schedule.completion\_status equals “Pending”.
          - Set items from ((items + whitespace '\\n') + item.item\_name).
          - Leave the innermost loop without its normal-exhaustion alternative.
    - Return items.
  - Otherwise.
    - If data\_type equals “id”.
      - For each schedule in self.schedules.
        - If (schedule.item\_name equals item\_name and schedule.completion\_status equals “Pending” and s\_date equals formatdate(schedule.scheduled\_date, “dd-mm-yyyy”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule.item\_name equals item\_name → schedule.completion\_status equals “Pending” → s\_date equals formatdate(schedule.scheduled\_date, “dd-mm-yyyy”).
          - Return schedule.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L98)

<a id="op-1615c64999d972"></a>
### Validate serial no for customer

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_schedule_maintenance_schedule_validate_serial_no_for_customer`

**Inputs** serial, customer.

**State and service calls** msgprint with translated “Serial No {0} was sold to Customer {1}, not {2}”.format(number, Platform.bold(escape\_html(serial.customer)), Platform.bold(escape\_html(customer))).

**Explicit failure paths** validation helper — translated “Serial No {0} is still in stock in Warehouse {1}”.format(number, Platform.bold(serial.warehouse)).

**Local steps**

- Set number from Platform.bold(escape\_html(serial.serial\_no)).
- If serial.warehouse.
  - Call the validation error handler Platform.throw(translated “Serial No {0} is still in stock in Warehouse {1}”.format(number, Platform.bold(serial.warehouse))).
- If (serial.customer and serial.customer differs from customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial.customer → serial.customer differs from customer.
  - Evaluate Platform.msgprint(translated “Serial No {0} was sold to Customer {1}, not {2}”.format(number, Platform.bold(escape\_html(serial.customer)), Platform.bold(escape\_html(customer))), title = translated “Differe ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L597)

<a id="op-fd13feafa2bdfa"></a>
### Get legacy delivery dates

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_schedule_maintenance_schedule_get_legacy_delivery_dates`

**Inputs** item\_code, serial\_nos.

**Declared result** dict.

**Explicit results** dates.

**Local steps**

- Set ledger from Platform.qb.DocType(“Stock Ledger Entry”).
- Set rows from nested operand in the contract(nested operand in the contract).select(ledger.serial\_no, ledger.posting\_datetime).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise ….
  - Draw serial\_no from serial\_nos.
- Set dates from mapping().
- For each row in rows.
  - For each serial\_no in set(get\_serial\_nos(row.serial\_no)).intersection(serial\_nos).
    - Set dates at serial\_no from max(dates.get(serial\_no, row.posting\_datetime), row.posting\_datetime).
- Return dates.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L594)

<a id="op-a348c4abc81fa3"></a>
### Get serial nos from schedule

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_get_serial_numbers_from_schedule`

**Inputs** item\_code, schedule = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Maintenance Schedule Item” via get\_value.

**Explicit results** serial\_nos.

**Local steps**

- Set serial\_nos from list().
- If schedule.
  - Evaluate Platform.has\_permission(“Maintenance Schedule”, “read”, doc = schedule, throw = true).
  - Set serial\_nos from Platform.db.get\_value(“Maintenance Schedule Item”, mapping(“parent” → schedule, “item\_code” → item\_code), “serial\_no”).
- If serial\_nos.
  - Set serial\_nos from get\_serial\_nos(serial\_nos).
- Return serial\_nos.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Maintenance Schedule”, “read”, doc = schedule, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L94)
