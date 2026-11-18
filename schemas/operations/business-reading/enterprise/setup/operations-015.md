# Company and master data · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Transaction deletion record

[Record definition](../../../../data/record-types/transaction_deletion_record.json)

<a id="op-cf5206809afbde"></a>
### Transaction Deletion Record.validate

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_validate`

**Inputs** self.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If not self.doctypes\_to\_be\_ignored.
  - Evaluate self.populate\_doctypes\_to\_be\_ignored\_table().
- Evaluate self.validate\_to\_delete\_list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [populate doctypes to be ignored table](operations-016.md#op-27479377e19588), [validate to delete list](operations-015.md#op-53a7f63aab9410).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L966) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1054) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L600)

<a id="op-53a7f63aab9410"></a>
### Transaction Deletion Record.validate to delete list

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_validate_to_delete_list`

**Inputs** self.

**Record and data access** read “DocType” via exists · read “DocType” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “DocType {0} does not exist”.format(item.doctype\_name) · validation helper — translated “Duplicate entry: {0}{1}”.format(item.doctype\_name, field\_desc) · validation helper — translated “Cannot delete protected core DocType: {0}”.format(item.doctype\_name) · validation helper — translated “Cannot add child table {0} to deletion list. Child tables are automatically deleted with their parent DocTypes.”.format(item.doctype\_name) · validation helper — translated “Cannot delete virtual DocType: {0}. Virtual DocTypes do not have database tables.”.format(item.doctype\_name) · 4 additional forms in the steps below.

**Local steps**

- If not self.doctypes\_to\_delete.
  - Return no value.
- Set protected from \_get\_protected\_doctypes\_internal().
- Set seen\_combinations from set().
- For each item in self.doctypes\_to\_delete.
  - If not Platform.db.exists(“DocType”, item.doctype\_name).
    - Call the validation error handler Platform.throw(translated “DocType {0} does not exist”.format(item.doctype\_name)).
  - Set composite\_key from tuple(item.doctype\_name, (item.company\_field or no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.company\_field → no value.
  - If composite\_key belongs to seen\_combinations.
    - Set field\_desc from formatted text  with company field '{item.company\_field}' when item.company\_field, otherwise empty text.
      - Value choice on item.company\_field — true gives formatted text  with company field '{item.company\_field}', false gives empty text.
    - Call the validation error handler Platform.throw(translated “Duplicate entry: {0}{1}”.format(item.doctype\_name, field\_desc), title = translated “Duplicate DocType”).
  - Evaluate seen\_combinations.add(composite\_key).
  - If item.doctype\_name belongs to protected.
    - Call the validation error handler Platform.throw(translated “Cannot delete protected core DocType: {0}”.format(item.doctype\_name), title = translated “Protected DocType”).
  - Set is\_child\_table from Platform.db.get\_value(“DocType”, item.doctype\_name, “istable”).
  - If is\_child\_table.
    - Call the validation error handler Platform.throw(translated “Cannot add child table {0} to deletion list. Child tables are automatically deleted with their parent DocTypes.”.format(item.doctype\_name), title = translated “Child Table Not Allowed”).
  - Set is\_virtual from Platform.db.get\_value(“DocType”, item.doctype\_name, “is\_virtual”).
  - If is\_virtual.
    - Call the validation error handler Platform.throw(translated “Cannot delete virtual DocType: {0}. Virtual DocTypes do not have database tables.”.format(item.doctype\_name), title = translated “Virtual DocType”).
  - Set valid\_company\_fields from self.\_get\_company\_link\_fields(item.doctype\_name).
  - If (valid\_company\_fields and not item.company\_field).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in valid\_company\_fields → not item.company\_field.
    - Call the validation error handler Platform.throw(translated “Select a Company field for DocType {0}”.format(item.doctype\_name), title = translated “Company Field Required”).
  - If item.company\_field.
    - If (“company” does not belong to valid\_company\_fields and len(valid\_company\_fields) &gt; 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in “company” does not belong to valid\_company\_fields → len(valid\_company\_fields) &gt; 1.
      - Call the validation error handler Platform.throw(translated “Cannot determine the owning company field for {0}”.format(item.doctype\_name), title = translated “Ambiguous Company Field”).
    - If (“company” belongs to valid\_company\_fields and item.company\_field differs from “company”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in “company” belongs to valid\_company\_fields → item.company\_field differs from “company”.
      - Call the validation error handler Platform.throw(translated “Only the owning company field may be used for {0}”.format(item.doctype\_name), title = translated “Invalid Company Field”).
    - If item.company\_field does not belong to valid\_company\_fields.
      - Call the validation error handler Platform.throw(translated “Field '{0}' is not a valid Company link field for DocType {1}”.format(item.company\_field, item.doctype\_name), title = translated “Invalid Company Field”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get company link fields](operations-015.md#op-1076bb8a27a8ed).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1057) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L603)

<a id="op-0c153b043f06d0"></a>
### Transaction Deletion Record.is any doctype in deletion list

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_is_any_record_type_in_deletion_list`

**Inputs** self, doctypes\_list.

**Explicit results** false · any(generator of doctype belongs to deletion\_doctypes for doctype drawn from doctypes\_list).

**Local steps**

- If not self.doctypes\_to\_delete.
  - Return false.
- Set deletion\_doctypes from set of d.doctype\_name for d drawn from self.doctypes\_to\_delete.
  - Draw d from self.doctypes\_to\_delete.
- Return any(generator of doctype belongs to deletion\_doctypes for doctype drawn from doctypes\_list).
  - Draw doctype from doctypes\_list.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L2081) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1041) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L588)

<a id="op-b49df11e34ef3b"></a>
### Transaction Deletion Record.generate job name for task

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_generate_job_name_for_task`

**Inputs** self, task = no value.

**Explicit results** formatted text {self.name}\_{method}.

**Local steps**

- Set method from self.task\_to\_internal\_method\_map at task.
- Return formatted text {self.name}\_{method}.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L2232) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1026) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L574)

<a id="op-ee8ebd66f1610a"></a>
### Transaction Deletion Record.generate job name for next tasks

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_generate_job_name_for_next_tasks`

**Inputs** self, task = no value.

**Explicit results** job\_names.

**Local steps**

- Set job\_names from list().
- Set current\_task\_idx from list(self.task\_to\_internal\_method\_map).index(task).
- For each tuple(idx, task) in enumerate(self.task\_to\_internal\_method\_map.keys(), 0).
  - If idx &gt; current\_task\_idx.
    - Evaluate job\_names.append(self.generate\_job\_name\_for\_task(task)).
- Return job\_names.

**Methods declared on this owner** [generate job name for task](operations-015.md#op-b49df11e34ef3b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L2336) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1025) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L573)

<a id="op-0ba4d00e482d1d"></a>
### Transaction Deletion Record.generate job name for all tasks

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_generate_job_name_for_all_tasks`

**Inputs** self.

**Explicit results** job\_names.

**Local steps**

- Set job\_names from list().
- For each task in self.task\_to\_internal\_method\_map.keys().
  - Evaluate job\_names.append(self.generate\_job\_name\_for\_task(task)).
- Return job\_names.

**Methods declared on this owner** [generate job name for task](operations-015.md#op-b49df11e34ef3b).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L2561) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1024) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L572)

<a id="op-089f39dc76c401"></a>
### Transaction Deletion Record.before submit

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_before_submit`

**Inputs** self.

**Record and data access** read “Transaction Deletion Record” via get\_all.

**Explicit failure paths** validation helper — translated “Cannot start deletion. Another deletion {0} is already queued/running. Please wait for it to complete.”.format(comma\_and(list of get\_link\_to\_form(“Transaction Deletion Record”, x) for x drawn f … · validation helper — translated “Please generate To Delete list before submitting”.

**Local steps**

- If queued\_docs bound to Platform.db.get\_all(“Transaction Deletion Record”, filters = mapping(“status” → tuple(“in”, list(“Running”, “Queued”)), “docstatus” → 1), pluck = “name”).
  - Call the validation error handler Platform.throw(translated “Cannot start deletion. Another deletion {0} is already queued/running. Please wait for it to complete.”.format(comma\_and(list of get\_link\_to\_form(“Transaction Deletion Record”, x ….
    - Draw x from queued\_docs.
- If (not self.doctypes\_to\_delete and not self.doctypes\_to\_be\_ignored).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.doctypes\_to\_delete → not self.doctypes\_to\_be\_ignored.
  - Call the validation error handler Platform.throw(translated “Please generate To Delete list before submitting”).
- If not self.doctypes\_to\_be\_ignored.
  - Evaluate self.populate\_doctypes\_to\_be\_ignored\_table().

If control reaches the end, it returns no value.

**Methods declared on this owner** [populate doctypes to be ignored table](operations-016.md#op-27479377e19588).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L2684) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1010) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L558)

<a id="op-a56c10a036e166"></a>
### Transaction Deletion Record.reset task flags

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_reset_task_flags`

**Inputs** self.

**Local steps**

- Set self.clear\_notifications\_status from “Pending”.
- Set self.delete\_bin\_data\_status from “Pending”.
- Set self.delete\_leads\_and\_addresses\_status from “Pending”.
- Set self.delete\_transactions\_status from “Pending”.
- Set self.initialize\_doctypes\_table\_status from “Pending”.
- Set self.reset\_company\_default\_values\_status from “Pending”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L3054) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1049) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L596)

<a id="op-283e09b0ffc4d1"></a>
### Transaction Deletion Record.before save

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_before_save`

**Inputs** self.

**Local steps**

- Set self.status from empty text.
- Evaluate self.doctypes.clear().
- Evaluate self.reset\_task\_flags().

If control reaches the end, it returns no value.

**Methods declared on this owner** [reset task flags](operations-015.md#op-a56c10a036e166).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L3186) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L557)

<a id="op-3768c0c6599f68"></a>
### Transaction Deletion Record.on submit

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_on_submit`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Queued”).
- Evaluate self.\_start\_deletion\_tasks().

If control reaches the end, it returns no value.

**Methods declared on this owner** [start deletion tasks](operations-016.md#op-7172e6a7cc10eb).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1044) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L591)

<a id="op-d854a26f50de98"></a>
### Transaction Deletion Record.on cancel

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate self.\_clear\_deletion\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear deletion cache](operations-015.md#op-f7faa738d65191).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L3361) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1042) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L589)

<a id="op-ada702a38c661a"></a>
### Transaction Deletion Record.set deletion cache

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_set_deletion_cache`

**Inputs** self.

**Local steps**

- For each item in self.doctypes\_to\_delete.
  - Evaluate Platform.cache.set\_value(formatted text deletion\_running\_doctype:{item.doctype\_name}, self.name, expires\_in\_sec = DELETION\_CACHE\_TTL).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L3445) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1050) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L597)

<a id="op-f7faa738d65191"></a>
### Transaction Deletion Record.clear deletion cache

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_clear_deletion_cache`

**Inputs** self.

**Local steps**

- For each item in self.doctypes\_to\_delete.
  - Set key from formatted text deletion\_running\_doctype:{item.doctype\_name}.
  - If Platform.cache.get\_value(key) equals self.name.
    - Evaluate Platform.cache.delete\_value(key).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1011) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L559)

<a id="op-ea1ed39790a499"></a>
### Transaction Deletion Record.get child tables

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_child_tables`

**Inputs** self, doctype\_name.

**Record and data access** read “DocField” via get\_all · read “DocType” via get\_all.

**Explicit results** list() · child\_tables.

**Local steps**

- Set child\_tables from Platform.get\_all(“DocField”, filters = mapping(“parent” → doctype\_name, “fieldtype” → list(“in”, list(“Table”, “Table MultiSelect”))), pluck = “options”).
- If not child\_tables.
  - Return list().
- Set child\_tables from Platform.get\_all(“DocType”, filters = mapping(“name” → list(“in”, child\_tables), “is\_virtual” → 0), pluck = “name”).
- Return child\_tables.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L3659) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L577)

<a id="op-69e9580b6ecbac"></a>
### Transaction Deletion Record.get to delete row infos

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_to_delete_row_infos`

**Inputs** self, doctype\_name, company\_field = no value, company = no value.

**Record and data access** read doctype\_name via count.

**Explicit results** mapping(“child\_doctypes” → child\_doctypes\_str, “document\_count” → doc\_count).

**Local steps**

- Set company from (company or self.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company → self.company.
- Set child\_tables from self.\_get\_child\_tables(doctype\_name).
- Set child\_doctypes\_str from “, ”.join(child\_tables) when child\_tables, otherwise empty text.
  - Value choice on child\_tables — true gives “, ”.join(child\_tables), false gives empty text.
- If (company\_field and company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_field → company.
  - Set doc\_count from Platform.db.count(doctype\_name, filters = mapping(company\_field → company)).
- Otherwise.
  - Set doc\_count from Platform.db.count(doctype\_name).
- Return mapping(“child\_doctypes” → child\_doctypes\_str, “document\_count” → doc\_count).

**Methods declared on this owner** [get child tables](operations-015.md#op-ea1ed39790a499).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L3937) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1036) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L583)

<a id="op-8f9ce64a991b72"></a>
### Transaction Deletion Record.has company field

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_has_company_field`

**Inputs** self, doctype\_name.

**Record and data access** read “DocField” via exists.

**Explicit results** Platform.db.exists(“DocField”, mapping(“parent” → doctype\_name, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”)).

**Local steps**

- Return Platform.db.exists(“DocField”, mapping(“parent” → doctype\_name, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L4242) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1037) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L584)

<a id="op-1076bb8a27a8ed"></a>
### Transaction Deletion Record.get company link fields

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_company_link_fields`

**Inputs** self, doctype\_name.

**Explicit results** list of field.fieldname for field drawn from Platform.get\_meta(doctype\_name).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Company”)).

**Local steps**

- Return list of field.fieldname for field drawn from Platform.get\_meta(doctype\_name).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Company”)).
  - Draw field from Platform.get\_meta(doctype\_name).get(“fields”, mapping(“fieldtype” → “Link”, “options” → “Company”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1031) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L579)

<a id="op-5f3cd05c14768e"></a>
### Transaction Deletion Record.generate to delete list

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_generate_to_delete_list`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all · read “DocType” via exists · read doctype\_name via count.

**State and service calls** call save on self.

**Explicit results** mapping(“count” → len(self.doctypes\_to\_delete)).

**Local steps**

- Set self.doctypes\_to\_delete from list().
- Set excluded from list of d.doctype\_name for d drawn from self.doctypes\_to\_be\_ignored.
  - Draw d from self.doctypes\_to\_be\_ignored.
- Evaluate excluded.extend(\_get\_protected\_doctypes\_internal()).
- Evaluate excluded.append(self.doctype).
- Set doctypes\_with\_company\_field from Platform.get\_all(“DocField”, filters = mapping(“fieldtype” → “Link”, “options” → “Company”), pluck = “parent”, distinct = true).
- Evaluate doctypes\_with\_company\_field.extend(Platform.get\_all(“Custom Field”, filters = mapping(“fieldtype” → “Link”, “options” → “Company”), pluck = “dt”, distinct = true)).
- Set doctypes\_with\_company\_field from list(dict.fromkeys(doctypes\_with\_company\_field)).
- Set doctypes\_with\_company from list().
- For each doctype\_name in doctypes\_with\_company\_field.
  - If doctype\_name belongs to excluded.
    - Continue with the next iteration or loop test.
  - If Platform.db.exists(“DocType”, doctype\_name).
    - Set meta from Platform.get\_meta(doctype\_name).
    - If (not meta.istable and not meta.is\_virtual).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.istable → not meta.is\_virtual.
      - Evaluate doctypes\_with\_company.append(doctype\_name).
- For each doctype\_name in doctypes\_with\_company.
  - Set company\_fields from self.\_get\_company\_link\_fields(doctype\_name).
  - If “company” does not belong to company\_fields.
    - Continue with the next iteration or loop test.
  - Set company\_fields from list(“company”).
  - Set child\_tables from self.\_get\_child\_tables(doctype\_name).
  - Set child\_doctypes\_str from “, ”.join(child\_tables) when child\_tables, otherwise empty text.
    - Value choice on child\_tables — true gives “, ”.join(child\_tables), false gives empty text.
  - For each company\_field in company\_fields.
    - Set doc\_count from Platform.db.count(doctype\_name, mapping(company\_field → self.company)).
    - Evaluate self.append(“doctypes\_to\_delete”, mapping(“doctype\_name” → doctype\_name, “company\_field” → company\_field, “document\_count” → doc\_count, “child\_doctypes” → child\_doctypes\_str)).
- Evaluate self.save().
- Return mapping(“count” → len(self.doctypes\_to\_delete)).

**Methods declared on this owner** [get company link fields](operations-015.md#op-1076bb8a27a8ed), [get child tables](operations-015.md#op-ea1ed39790a499).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1027) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L575)

<a id="op-8ac2fe29d4c7f2"></a>
### Transaction Deletion Record.populate doctype details

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_populate_record_type_details`

**Inputs** self, doctype\_name, company = no value, company\_field = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via exists · read “DocType” via get\_value.

**Explicit results** mapping() · mapping(“child\_doctypes” → empty text, “document\_count” → 0, “error” → translated “{0} is a child table and will be deleted automatically with its parent”.format(doctype\_name)) · self.\_get\_to\_delete\_row\_infos(doctype\_name, company\_field = company\_field, company = company) · mapping(“child\_doctypes” → empty text, “document\_count” → 0, “error” → translated “Unable to fetch DocType details. Please contact system administrator.”).

**Explicit failure paths** validation helper — translated “DocType {0} does not exist”.format(doctype\_name).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If not doctype\_name.
  - Return mapping().
- If not Platform.db.exists(“DocType”, doctype\_name).
  - Call the validation error handler Platform.throw(translated “DocType {0} does not exist”.format(doctype\_name)).
- Set is\_child\_table from Platform.db.get\_value(“DocType”, doctype\_name, “istable”).
- If is\_child\_table.
  - Return mapping(“child\_doctypes” → empty text, “document\_count” → 0, “error” → translated “{0} is a child table and will be deleted automatically with its parent”.format(doctype\_name)).
- Attempt the following.
  - Return self.\_get\_to\_delete\_row\_infos(doctype\_name, company\_field = company\_field, company = company).
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(formatted text Error in populate\_doctype\_details for {doctype\_name}: {e}, “Transaction Deletion Record”).
  - Return mapping(“child\_doctypes” → empty text, “document\_count” → 0, “error” → translated “Unable to fetch DocType details. Please contact system administrator.”).

**Methods declared on this owner** [get to delete row infos](operations-015.md#op-69e9580b6ecbac).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1045) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L592)

<a id="op-b842a97c730a51"></a>
### Transaction Deletion Record.export to delete template method

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_export_to_delete_template_method`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Generate To Delete list first”.

**Local steps**

- If not self.doctypes\_to\_delete.
  - Call the validation error handler Platform.throw(translated “Generate To Delete list first”).
- Bind dependencies csv.
- Bind dependencies StringIO.
- Set output from StringIO().
- Set writer from csv.writer(output).
- Evaluate writer.writerow(list(“doctype\_name”, “company\_field”, “child\_doctypes”)).
- For each item in self.doctypes\_to\_delete.
  - Evaluate writer.writerow(list(item.doctype\_name, (item.company\_field or empty text), (item.child\_doctypes or empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.company\_field → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.child\_doctypes → empty text.
- Set Platform.response at “result” from output.getvalue().
- Set Platform.response at “type” from “csv”.
- Set Platform.response at “doctype” from formatted text deletion\_template\_{self.company}\_{Platform.utils.now\_datetime().strftime(“%Y%m%d”)}.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0697.json#L5961) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1023) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L571)

<a id="op-be96ede8a9167d"></a>
### Transaction Deletion Record.import to delete template method

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_import_to_delete_template_method`

**Inputs** self, csv\_content.

**Record and data access** read “DocType” via exists · read “DocType” via get\_value.

**State and service calls** call save on self · msgprint with translated “Skipped {0} DocType(s):&lt;br&gt;{1}”.format(len(skipped), text in the contract.join(skipped)).

**Explicit results** mapping(“imported” → imported\_count, “skipped” → len(skipped)).

**Explicit failure paths** validation helper — translated “Invalid CSV format. Expected column: doctype\_name”.

**Local steps**

- Bind dependencies csv.
- Bind dependencies StringIO.
- Set reader from csv.DictReader(StringIO(csv\_content)).
- If “doctype\_name” does not belong to (reader.fieldnames or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reader.fieldnames → list().
  - Call the validation error handler Platform.throw(translated “Invalid CSV format. Expected column: doctype\_name”).
- Set protected from \_get\_protected\_doctypes\_internal().
- Set imported\_rows from list().
- Set skipped from list().
- For each row in reader.
  - Set doctype\_name from (row.get(“doctype\_name”) or empty text).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“doctype\_name”) → empty text.
  - Set company\_field from ((row.get(“company\_field”) or empty text).strip() or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (row.get(“company\_field”) or empty text).strip() → no value.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“company\_field”) → empty text.
  - If not doctype\_name.
    - Continue with the next iteration or loop test.
  - If doctype\_name belongs to protected.
    - Evaluate skipped.append(translated “{0}: Protected DocType”.format(doctype\_name)).
    - Continue with the next iteration or loop test.
  - If not Platform.db.exists(“DocType”, doctype\_name).
    - Evaluate skipped.append(translated “{0}: Not found”.format(doctype\_name)).
    - Continue with the next iteration or loop test.
  - Set is\_child from Platform.db.get\_value(“DocType”, doctype\_name, “istable”).
  - If is\_child.
    - Evaluate skipped.append(translated “{0}: Child table (auto-deleted with parent)”.format(doctype\_name)).
    - Continue with the next iteration or loop test.
  - Set is\_virtual from Platform.db.get\_value(“DocType”, doctype\_name, “is\_virtual”).
  - If is\_virtual.
    - Evaluate skipped.append(translated “{0}: Virtual DocType (no database table)”.format(doctype\_name)).
    - Continue with the next iteration or loop test.
  - Set db\_company\_fields from self.\_get\_company\_link\_fields(doctype\_name).
  - If (company\_field and company\_field does not belong to db\_company\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_field → company\_field does not belong to db\_company\_fields.
    - Evaluate skipped.append(translated “{0}: Invalid company field”.format(doctype\_name)).
    - Continue with the next iteration or loop test.
  - Set import\_company\_field from empty text.
  - If not db\_company\_fields.
    - Set details from self.\_get\_to\_delete\_row\_infos(doctype\_name).
  - Otherwise.
    - If (company\_field and company\_field belongs to db\_company\_fields).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_field → company\_field belongs to db\_company\_fields.
      - Set details from self.\_get\_to\_delete\_row\_infos(doctype\_name, company\_field).
      - Set import\_company\_field from company\_field.
    - Otherwise.
      - If “company” belongs to db\_company\_fields.
        - Set details from self.\_get\_to\_delete\_row\_infos(doctype\_name, “company”).
        - Set import\_company\_field from “company”.
      - Otherwise.
        - Set details from self.\_get\_to\_delete\_row\_infos(doctype\_name, db\_company\_fields at 0).
        - Set import\_company\_field from db\_company\_fields at 0.
  - Evaluate imported\_rows.append(mapping(“doctype\_name” → doctype\_name, “company\_field” → import\_company\_field, “document\_count” → details at “document\_count”, “child\_doctypes” → details at “child\_doctypes”)).
- Set imported\_count from len(imported\_rows).
- If imported\_rows.
  - Set self.doctypes\_to\_delete from list().
  - For each imported\_row in imported\_rows.
    - Evaluate self.append(“doctypes\_to\_delete”, imported\_row).
  - Evaluate self.save().
- If skipped.
  - Evaluate Platform.msgprint(translated “Skipped {0} DocType(s):&lt;br&gt;{1}”.format(len(skipped), text in the contract.join(skipped)), title = translated “Import Summary”, indicator = “orange”).
- Return mapping(“imported” → imported\_count, “skipped” → len(skipped)).

**Methods declared on this owner** [get company link fields](operations-015.md#op-1076bb8a27a8ed), [get to delete row infos](operations-015.md#op-69e9580b6ecbac).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1038) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L585)

<a id="op-c63a57f907970b"></a>
### Transaction Deletion Record.enqueue task

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_enqueue_task`

**Inputs** self, task = no value.

**State and service calls** enqueue with “Platform.utils.background\_jobs.run\_doc\_method”.

**Local steps**

- If (task and task belongs to self.task\_to\_internal\_method\_map).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in task → task belongs to self.task\_to\_internal\_method\_map.
  - Set job\_names from self.generate\_job\_name\_for\_next\_tasks(task = task).
  - Evaluate self.validate\_running\_task\_for\_doc(job\_names = job\_names).
  - Set job\_id from self.generate\_job\_name\_for\_task(task).
  - If self.process\_in\_single\_transaction.
    - Evaluate self.execute\_task(task\_to\_execute = task).
  - Otherwise.
    - Evaluate Platform.enqueue(“Platform.utils.background\_jobs.run\_doc\_method”, doctype = self.doctype, name = self.name, doc\_method = “execute\_task”, job\_id = job\_id, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate job name for next tasks](operations-015.md#op-ee8ebd66f1610a), [validate running task for doc](operations-016.md#op-c78a76fa8cb156), [generate job name for task](operations-015.md#op-b49df11e34ef3b), [execute task](operations-015.md#op-a518a452ea1933).

**Values supplied outside this operation** service or queued work from Platform.enqueue(“Platform.utils.background\_jobs.run\_doc\_method”, doctype = self.doctype, name = self.name, doc\_method = “execute\_task”, job\_id = job\_id, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0698.json#L1502) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L569)

<a id="op-a518a452ea1933"></a>
### Transaction Deletion Record.execute task

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_execute_task`

**Inputs** self, task\_to\_execute = no value.

**State and service calls** rollback · request set\_value on self.doctype.

**Explicit failure paths** propagate active failure.

**Local steps**

- If task\_to\_execute.
  - Set method from self.task\_to\_internal\_method\_map at task\_to\_execute.
  - If task bound to getattr(self, method, no value).
    - Attempt the following.
      - Evaluate task().
    - On failure (Exception).
      - If self.process\_in\_single\_transaction.
        - Evaluate self.\_clear\_deletion\_cache().
        - Propagate the active failure.
      - Evaluate Platform.db.rollback().
      - Set traceback from Platform.get\_traceback(with\_context = true).
      - If traceback.
        - Set message from (“Traceback: &lt;br&gt;” + traceback).
        - Evaluate Platform.db.set\_value(self.doctype, self.name, “error\_log”, message).
      - Evaluate Platform.db.set\_value(self.doctype, self.name, “status”, “Failed”).
      - Evaluate self.\_clear\_deletion\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear deletion cache](operations-015.md#op-f7faa738d65191).

**Values supplied outside this operation** selected callable from getattr(self, method, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L570)

<a id="op-fdbc305411242c"></a>
### Transaction Deletion Record.delete notifications

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_notifications`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_doc\_status().
- If self.clear\_notifications\_status equals “Pending”.
  - Evaluate clear\_notifications().
  - Evaluate self.db\_set(“clear\_notifications\_status”, “Completed”).
- Evaluate self.enqueue\_task(task = “Initialize Summary Table”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doc status](operations-016.md#op-7bdb2fcc1ad83e), [enqueue task](operations-015.md#op-c63a57f907970b).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0698.json#L2253) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L566)
