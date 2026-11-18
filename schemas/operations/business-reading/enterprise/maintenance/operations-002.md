# Equipment maintenance · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Maintenance schedule

[Record definition](../../../../data/record-types/maintenance_schedule.json)

<a id="op-46099b3c326bcd"></a>
### Make maintenance visit

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_make_maintenance_visit`

**Inputs** source\_name, target\_doc = no value, item\_name = no value, s\_id = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind dependencies get\_mapped\_doc.
- Bind local operation condition for subsequent calls.
- Bind local operation update\_status\_and\_detail for subsequent calls.
- Bind local operation update\_serial for subsequent calls.
- Set doclist from get\_mapped\_doc(“Maintenance Schedule”, source\_name, mapping(“Maintenance Schedule” → mapping(“doctype” → “Maintenance Visit”, “field\_map” → mapping(“name” → “maintenance\_schedule”), “validation” → mapping( ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L114)

<a id="op-477d3f979dfd42"></a>
### Make maintenance visit.condition

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_make_maintenance_visit_condition`

**Inputs** doc.

**Explicit results** doc.name equals s\_id · false · doc.completion\_status differs from “Fully Completed”.

**Local steps**

- If s\_id.
  - Return doc.name equals s\_id.
- If (item\_name and doc.item\_name differs from item\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_name → doc.item\_name differs from item\_name.
  - Return false.
- Return doc.completion\_status differs from “Fully Completed”.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L115)

<a id="op-c73042f8241a52"></a>
### Make maintenance visit.update status and detail

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_make_maintenance_visit_update_status_and_detail`

**Inputs** source, target, parent.

**Local steps**

- Set target.maintenance\_type from “Scheduled”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0449.json#L2758) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L117)

<a id="op-189486a54e148f"></a>
### Make maintenance visit.update serial

`operation_enterprise_maintenance_record_definitions_maintenance_schedule_business_behavior_make_maintenance_visit_update_serial`

**Inputs** source, target, parent.

**Record and data access** read “Maintenance Schedule Item” via get\_value · resolve a document from “Serial and Batch Bundle” via get\_doc.

**Local steps**

- If source.item\_reference.
  - If sbb bound to Platform.db.get\_value(“Maintenance Schedule Item”, source.item\_reference, “serial\_and\_batch\_bundle”).
    - Set serial\_nos from Platform.get\_doc(“Serial and Batch Bundle”, sbb).get\_serial\_nos().
    - If len(serial\_nos) equals 1.
      - Set target.serial\_no from serial\_nos at 0.
    - Otherwise.
      - Set target.serial\_no from empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0449.json#L2819) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L116)

## Record · Maintenance visit

[Record definition](../../../../data/record-types/maintenance_visit.json)

<a id="op-ae5753b166c7a8"></a>
### Maintenance Visit.validate serial no

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_validate_serial_number`

**Inputs** self.

**Record and data access** read “Serial No” via get\_value.

**Explicit failure paths** validation helper — translated “Serial No {0} does not exist”.format(d.serial\_no).

**Local steps**

- For each d in self.get(“purposes”).
  - If not d.serial\_no.
    - Continue with the next iteration or loop test.
  - Set serial from Platform.db.get\_value(“Serial No”, d.serial\_no, list(“serial\_no”, “warehouse”, “customer”), as\_dict = true).
  - If not serial.
    - Call the validation error handler Platform.throw(translated “Serial No {0} does not exist”.format(d.serial\_no)).
  - If (serial.warehouse and was\_delivered\_to(d.serial\_no, d.item\_code, self.customer)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in serial.warehouse → was\_delivered\_to(d.serial\_no, d.item\_code, self.customer).
    - Continue with the next iteration or loop test.
  - Evaluate validate\_serial\_no\_for\_customer(serial, self.customer).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L135)

<a id="op-9632f86b3c7674"></a>
### Maintenance Visit.validate purpose table

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_validate_purpose_table`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Add Items in the Purpose Table”.

**Local steps**

- If not self.purposes.
  - Call the validation error handler Platform.throw(translated “Add Items in the Purpose Table”, title = translated “Purposes Required”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0450.json#L582) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L134)

<a id="op-7106559026351b"></a>
### Maintenance Visit.get schedule details

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_get_schedule_details`

**Inputs** self.

**Explicit results** list(self.maintenance\_schedule\_detail) · list of purpose.maintenance\_schedule\_detail for purpose drawn from self.purposes where purpose.maintenance\_schedule\_detail.

**Local steps**

- If self.maintenance\_schedule\_detail.
  - Return list(self.maintenance\_schedule\_detail).
- Return list of purpose.maintenance\_schedule\_detail for purpose drawn from self.purposes where purpose.maintenance\_schedule\_detail.
  - Draw purpose from self.purposes, keep a combination only if (purpose.maintenance\_schedule\_detail).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L602)

<a id="op-124bf1b68c15f0"></a>
### Maintenance Visit.validate maintenance date

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_validate_maintenance_date`

**Inputs** self.

**Record and data access** read “Maintenance Schedule Detail” via get\_value · read “Maintenance Schedule Item” via get\_value.

**Explicit failure paths** validation helper — translated “Date must be between {0} and {1}”.format(format\_date(start\_date), format\_date(end\_date)).

**Local steps**

- For each detail in self.get\_schedule\_details().
  - Set item\_ref from Platform.db.get\_value(“Maintenance Schedule Detail”, detail, “item\_reference”).
  - If item\_ref.
    - Set tuple(start\_date, end\_date) from Platform.db.get\_value(“Maintenance Schedule Item”, item\_ref, list(“start\_date”, “end\_date”)).
    - If (get\_datetime(self.mntc\_date) &lt; get\_datetime(start\_date) or get\_datetime(self.mntc\_date) &gt; get\_datetime(end\_date)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_datetime(self.mntc\_date) &lt; get\_datetime(start\_date) → get\_datetime(self.mntc\_date) &gt; get\_datetime(end\_date).
      - Call the validation error handler Platform.throw(translated “Date must be between {0} and {1}”.format(format\_date(start\_date), format\_date(end\_date))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get schedule details](operations-002.md#op-7106559026351b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L133)

<a id="op-1de37c8ee2af16"></a>
### Maintenance Visit.validate schedule details

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_validate_schedule_details`

**Inputs** self.

**Local steps**

- Set details from self.get\_schedule\_details().
- If details.
  - Evaluate self.validate\_schedule\_customer().
  - Evaluate self.validate\_schedule\_rows(details).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get schedule details](operations-002.md#op-7106559026351b), [validate schedule customer](operations-002.md#op-9c28de4ed6e0ed), [validate schedule rows](operations-002.md#op-d111ece5b79d7d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L606)

<a id="op-9c28de4ed6e0ed"></a>
### Maintenance Visit.validate schedule customer

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_validate_schedule_customer`

**Inputs** self.

**Record and data access** read “Maintenance Schedule” via get\_value.

**Explicit failure paths** validation helper — translated “Select a submitted Maintenance Schedule for the scheduled visits” · validation helper — translated “Customer {0} does not match the customer of Maintenance Schedule {1}”.format(Platform.bold(self.customer), Platform.bold(self.maintenance\_schedule)) · validation helper — translated “Company {0} does not match the company of Maintenance Schedule {1}”.format(Platform.bold(self.company), Platform.bold(self.maintenance\_schedule)).

**Local steps**

- Set schedule from Platform.db.get\_value(“Maintenance Schedule”, self.maintenance\_schedule, list(“customer”, “company”, “docstatus”), as\_dict = true).
- If (not schedule or schedule.docstatus differs from 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not schedule → schedule.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Select a submitted Maintenance Schedule for the scheduled visits”).
- If schedule.customer differs from self.customer.
  - Call the validation error handler Platform.throw(translated “Customer {0} does not match the customer of Maintenance Schedule {1}”.format(Platform.bold(self.customer), Platform.bold(self.maintenance\_schedule))).
- If schedule.company differs from self.company.
  - Call the validation error handler Platform.throw(translated “Company {0} does not match the company of Maintenance Schedule {1}”.format(Platform.bold(self.company), Platform.bold(self.maintenance\_schedule))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L605)

<a id="op-8891f90861c1e3"></a>
### Maintenance Visit.validate warranty claims

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_validate_warranty_claims`

**Inputs** self.

**Record and data access** read “Warranty Claim” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Warranty Claims {0} do not belong to Customer {1} and Company {2}”.format(escape\_html(“, ”.join(sorted(other\_claims))), Platform.bold(self.customer), Platform.bold(self.company)).

**Local steps**

- Set claims from set of purpose.prevdoc\_docname for purpose drawn from self.purposes where (purpose.prevdoc\_doctype equals “Warranty Claim” and purpose.prevdoc\_docname).
  - Draw purpose from self.purposes, keep a combination only if ((purpose.prevdoc\_doctype equals “Warranty Claim” and purpose.prevdoc\_docname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in purpose.prevdoc\_doctype equals “Warranty Claim” → purpose.prevdoc\_docname.
- If not claims.
  - Return no value.
- Set matching\_claims from Platform.get\_all(“Warranty Claim”, filters = mapping(“name” → tuple(“in”, list(claims)), “customer” → self.customer, “company” → self.company), pluck = “name”).
- If other\_claims bound to (claims − set(matching\_claims)).
  - Call the validation error handler Platform.throw(translated “Warranty Claims {0} do not belong to Customer {1} and Company {2}”.format(escape\_html(“, ”.join(sorted(other\_claims))), Platform.bold(self.customer), Platform.bold(self.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L608)

<a id="op-d111ece5b79d7d"></a>
### Maintenance Visit.validate schedule rows

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_validate_schedule_rows`

**Inputs** self, details.

**Record and data access** read “Maintenance Schedule Detail” via get\_all.

**Explicit failure paths** validation helper — translated “Schedule rows {0} do not belong to Maintenance Schedule {1}”.format(escape\_html(“, ”.join(missing)), Platform.bold(self.maintenance\_schedule)) · validation helper — translated “Row #{0}: Item {1} does not match the item of its schedule row”.format(purpose.idx, Platform.bold(escape\_html(purpose.item\_code))).

**Local steps**

- Set items from dict(Platform.get\_all(“Maintenance Schedule Detail”, filters = mapping(“name” → tuple(“in”, details), “parent” → self.maintenance\_schedule), fields = list(“name”, “item\_code”), as\_list = true)).
- If missing bound to list of detail for detail drawn from details where detail does not belong to items.
  - Draw detail from details, keep a combination only if (detail does not belong to items).
  - Call the validation error handler Platform.throw(translated “Schedule rows {0} do not belong to Maintenance Schedule {1}”.format(escape\_html(“, ”.join(missing)), Platform.bold(self.maintenance\_schedule))).
- For each purpose in self.purposes.
  - Set row\_item from items.get((self.maintenance\_schedule\_detail or purpose.maintenance\_schedule\_detail)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.maintenance\_schedule\_detail → purpose.maintenance\_schedule\_detail.
  - If (row\_item and row\_item differs from purpose.item\_code).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row\_item → row\_item differs from purpose.item\_code.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Item {1} does not match the item of its schedule row”.format(purpose.idx, Platform.bold(escape\_html(purpose.item\_code)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L607)

<a id="op-e94e4947851abc"></a>
### Maintenance Visit.validate

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_serial\_no().
- Evaluate self.validate\_schedule\_details().
- Evaluate self.validate\_warranty\_claims().
- Evaluate self.validate\_maintenance\_date().
- Evaluate self.validate\_purpose\_table().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate serial no](operations-002.md#op-ae5753b166c7a8), [validate schedule details](operations-002.md#op-1de37c8ee2af16), [validate warranty claims](operations-002.md#op-8891f90861c1e3), [validate maintenance date](operations-002.md#op-124bf1b68c15f0), [validate purpose table](operations-002.md#op-9632f86b3c7674).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L132)

<a id="op-dfb08900e8cef2"></a>
### Maintenance Visit.update status and actual date

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_update_status_and_actual_date`

**Inputs** self.

**State and service calls** request set\_value on “Maintenance Schedule Detail”.

**Explicit results** no value.

**Local steps**

- Set details from self.get\_schedule\_details().
- If not details.
  - Return no value.
- Set visits from self.get\_submitted\_schedule\_visits(details).
- For each detail in details.
  - Set references from list of visit for visit drawn from visits where visit.detail equals detail.
    - Draw visit from visits, keep a combination only if (visit.detail equals detail).
  - Set fully\_completed from list of visit for visit drawn from references where visit.completion\_status equals “Fully Completed”.
    - Draw visit from references, keep a combination only if (visit.completion\_status equals “Fully Completed”).
  - Set latest from next(iter((fully\_completed or references)), no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fully\_completed → references.
  - Evaluate Platform.db.set\_value(“Maintenance Schedule Detail”, detail, mapping(“completion\_status” → latest.completion\_status when latest, otherwise “Pending”, “actual\_date” → latest.mntc\_date when latest, otherwise ….
    - Value choice on latest — true gives latest.completion\_status, false gives “Pending”.
    - Value choice on latest — true gives latest.mntc\_date, false gives no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get schedule details](operations-002.md#op-7106559026351b), [get submitted schedule visits](operations-002.md#op-76558570672606).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L131)

<a id="op-76558570672606"></a>
### Maintenance Visit.get submitted schedule visits

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_get_submitted_schedule_visits`

**Inputs** self, details.

**Explicit results** visits.

**Local steps**

- Set visit from Platform.qb.DocType(“Maintenance Visit”).
- Set purpose from Platform.qb.DocType(“Maintenance Visit Purpose”).
- Set visits from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(visit.creation, order = Order.desc).for\_update().run(as\_dict = true).
- For each row in visits.
  - Set row.detail from (row.header\_detail or row.detail).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.header\_detail → row.detail.
- Return visits.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L603)

<a id="op-842296cb4be88c"></a>
### Maintenance Visit.update customer issue

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_update_customer_issue`

**Inputs** self, flag.

**Record and data access** resolve a document from “Warranty Claim” via get\_doc.

**State and service calls** call db\_update on wc\_doc.

**Local steps**

- If not self.maintenance\_schedule.
  - For each d in self.get(“purposes”).
    - If (d.prevdoc\_docname and d.prevdoc\_doctype equals “Warranty Claim”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.prevdoc\_docname → d.prevdoc\_doctype equals “Warranty Claim”.
      - If self.is\_superseded\_by\_completed\_visit(d.prevdoc\_docname).
        - Continue with the next iteration or loop test.
      - If flag equals 1.
        - Set mntc\_date from self.mntc\_date.
        - Set service\_person from d.service\_person.
        - Set work\_done from d.work\_done.
        - Set status from CLAIM\_STATUS.get(self.completion\_status, “Open”).
      - Otherwise.
        - Set mv from Platform.qb.DocType(“Maintenance Visit”).
        - Set mvp from Platform.qb.DocType(“Maintenance Visit Purpose”).
        - Set nm from nested operand in the contract(nested operand in the contract).orderby(mv.name, order = nested operand in the contract.qb.desc).limit(1).run().
        - If nm.
          - Set status from CLAIM\_STATUS.get(nm at 0 at 4, “Open”).
          - Set mntc\_date from ((nm and nm at 0 at 1) or empty text).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in (nm and nm at 0 at 1) → empty text.
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in nm → nm at 0 at 1.
          - Set service\_person from ((nm and nm at 0 at 2) or empty text).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in (nm and nm at 0 at 2) → empty text.
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in nm → nm at 0 at 2.
          - Set work\_done from ((nm and nm at 0 at 3) or empty text).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in (nm and nm at 0 at 3) → empty text.
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in nm → nm at 0 at 3.
        - Otherwise.
          - Set status from “Open”.
          - Set mntc\_date from no value.
          - Set service\_person from no value.
          - Set work\_done from no value.
      - Set wc\_doc from Platform.get\_doc(“Warranty Claim”, d.prevdoc\_docname).
      - Evaluate wc\_doc.update(mapping(“resolution\_date” → mntc\_date, “resolved\_by” → get\_user\_of\_sales\_person(service\_person), “resolution\_details” → work\_done, “status” → status)).
      - Evaluate wc\_doc.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is superseded by completed visit](operations-002.md#op-200b6a86a18102).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L130)

<a id="op-200b6a86a18102"></a>
### Maintenance Visit.is superseded by completed visit

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_maintenancevisit_is_superseded_by_completed_visit`

**Inputs** self, warranty\_claim.

**Declared result** bool.

**Explicit results** false · bool(completed\_visit).

**Local steps**

- <a id="op-200b6a86a18102-guard-3"></a>If self.completion\_status equals “Fully Completed”.
  - Return false.
- Set mv from Platform.qb.DocType(“Maintenance Visit”).
- Set mvp from Platform.qb.DocType(“Maintenance Visit Purpose”).
- Set completed\_visit from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contract equals nested op ….run().
- Return bool(completed\_visit).

**Derived branch illustrations**

- At the comparison self.completion\_status equals “Fully Completed”, self.completion\_status = “Fully Completed” selects the branch that returns false. With self.completion\_status = “Partially Completed”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-200b6a86a18102-guard-3)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L604)

<a id="op-4b5783e1f199e0"></a>
### Maintenance Visit.check if last visit

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_check_if_last_visit`

**Inputs** self.

**Record and data access** execute query text (SELECT, Maintenance Visit).

**Explicit failure paths** validation helper — translated “Cancel Maintenance Visits {0} before cancelling this Maintenance Visit”.format(check\_lst) · Exception.

**Local steps**

- Set check\_for\_docname from no value.
- For each d in self.get(“purposes”).
  - If (d.prevdoc\_docname and d.prevdoc\_doctype equals “Warranty Claim”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.prevdoc\_docname → d.prevdoc\_doctype equals “Warranty Claim”.
    - Set check\_for\_docname from d.prevdoc\_docname.
- If check\_for\_docname.
  - Set check from Platform.db.sql(query text (SELECT, Maintenance Visit), tuple(self.name, check\_for\_docname, self.mntc\_date, self.mntc\_date, …)).
  - If check.
    - Set check\_lst from list of x at 0 for x drawn from check.
      - Draw x from check.
    - Set check\_lst from “,”.join(check\_lst).
    - Call the validation error handler Platform.throw(translated “Cancel Maintenance Visits {0} before cancelling this Maintenance Visit”.format(check\_lst)).
    - Raise Exception.
  - Otherwise.
    - Evaluate self.update\_customer\_issue(0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update customer issue](operations-002.md#op-842296cb4be88c).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L126)

<a id="op-f474fc827de4b2"></a>
### Maintenance Visit.on submit

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.update\_customer\_issue(1).
- Evaluate self.db\_set(“status”, “Submitted”).
- Evaluate self.update\_status\_and\_actual\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update customer issue](operations-002.md#op-842296cb4be88c), [update status and actual date](operations-002.md#op-dfb08900e8cef2).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0450.json#L3605) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L128)

<a id="op-0e226faeb7ff60"></a>
### Maintenance Visit.on cancel

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.check\_if\_last\_visit().
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.update\_status\_and\_actual\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if last visit](operations-002.md#op-4b5783e1f199e0), [update status and actual date](operations-002.md#op-dfb08900e8cef2).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L127)

<a id="op-f21a208f5dcf10"></a>
### Maintenance Visit.on update

`operation_enterprise_maintenance_record_definitions_maintenance_visit_business_behavior_maintenance_visit_on_update`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0450.json#L3829) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L129)

<a id="op-8eeb56471952ad"></a>
### Get user of sales person

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_get_user_of_sales_person`

**Inputs** sales\_person.

**Declared result** (str bitwise or no value).

**Record and data access** read “Sales Person” via get\_value · read “Employee” via get\_value.

**Explicit results** Platform.db.get\_value(“Employee”, employee, “user\_id”) when employee, otherwise no value.

**Local steps**

- Set employee from (sales\_person and Platform.db.get\_value(“Sales Person”, sales\_person, “employee”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_person → Platform.db.get\_value(“Sales Person”, sales\_person, “employee”).
- Return Platform.db.get\_value(“Employee”, employee, “user\_id”) when employee, otherwise no value.
  - Value choice on employee — true gives Platform.db.get\_value(“Employee”, employee, “user\_id”), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L600)

<a id="op-740cdffd298167"></a>
### Was delivered to

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_was_delivered_to`

**Inputs** serial\_no, item\_code, customer.

**Declared result** bool.

**Explicit results** (has\_delivery\_to(get\_bundle\_deliveries(serial\_no), customer) or has\_delivery\_to(get\_legacy\_deliveries(serial\_no, item\_code), customer)).

**Local steps**

- Return (has\_delivery\_to(get\_bundle\_deliveries(serial\_no), customer) or has\_delivery\_to(get\_legacy\_deliveries(serial\_no, item\_code), customer)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_delivery\_to(get\_bundle\_deliveries(serial\_no), customer) → has\_delivery\_to(get\_legacy\_deliveries(serial\_no, item\_code), customer).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L609)

<a id="op-3c6886405a903b"></a>
### Has delivery to

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_has_delivery_to`

**Inputs** deliveries, customer.

**Declared result** bool.

**Record and data access** read doctype via exists.

**Explicit results** true · false.

**Local steps**

- For each doctype in tuple(“Delivery Note”, “Sales Invoice”).
  - Set names from list of row.voucher\_no for row drawn from deliveries where row.voucher\_type equals doctype.
    - Draw row from deliveries, keep a combination only if (row.voucher\_type equals doctype).
  - If (names and Platform.db.exists(doctype, mapping(“name” → tuple(“in”, names), “customer” → customer))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in names → Platform.db.exists(doctype, mapping(“name” → tuple(“in”, names), “customer” → customer)).
    - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L601)
