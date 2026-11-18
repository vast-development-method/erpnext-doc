# Company and master data · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Transaction deletion record

[Record definition](../../../../data/record-types/transaction_deletion_record.json)

<a id="op-27479377e19588"></a>
### Transaction Deletion Record.populate doctypes to be ignored table

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_populate_record_types_to_be_ignored_table`

**Inputs** self.

**Local steps**

- Set doctypes\_to\_be\_ignored\_list from get\_doctypes\_to\_be\_ignored().
- For each doctype in doctypes\_to\_be\_ignored\_list.
  - Evaluate self.append(“doctypes\_to\_be\_ignored”, mapping(“doctype\_name” → doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0698.json#L2410) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1047) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L594)

<a id="op-c78a76fa8cb156"></a>
### Transaction Deletion Record.validate running task for doc

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_validate_running_task_for_record`

**Inputs** self, job\_names = no value.

**Explicit failure paths** validation helper — translated “{0} is already running for {1}”.format(comma\_and(list of get\_link\_to\_form(“RQ Job”, x) for x drawn from running\_tasks), self.name).

**Local steps**

- Set running\_tasks from list().
- For each x in job\_names.
  - If is\_job\_enqueued(x).
    - Evaluate running\_tasks.append(get\_job(x).get\_id()).
- If running\_tasks.
  - Call the validation error handler Platform.throw(translated “{0} is already running for {1}”.format(comma\_and(list of get\_link\_to\_form(“RQ Job”, x) for x drawn from running\_tasks), self.name)).
    - Draw x from running\_tasks.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0698.json#L2528) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1056) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L602)

<a id="op-7bdb2fcc1ad83e"></a>
### Transaction Deletion Record.validate doc status

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_validate_record_status`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is not running. Cannot trigger events for this Document”.format(get\_link\_to\_form(“Transaction Deletion Record”, self.name)).

**Local steps**

- <a id="op-7bdb2fcc1ad83e-guard-2"></a>If self.status differs from “Running”.
  - Call the validation error handler Platform.throw(translated “{0} is not running. Cannot trigger events for this Document”.format(get\_link\_to\_form(“Transaction Deletion Record”, self.name))).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status differs from “Running”, self.status = “Queued” selects the branch that calls the validation-error handler with translated “{0} is not running. Cannot trigger events for this Document”.format(get\_link\_to\_form(“Transaction Deletion Record”, self.name)). With self.status = “Running”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7bdb2fcc1ad83e-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1055) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L601)

<a id="op-bcbb63db6c23be"></a>
### Transaction Deletion Record.start deletion tasks

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_start_deletion_tasks`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call save on self.

**Explicit failure paths** validation helper — translated “Only a submitted deletion with status Failed can be retried. {0} is {1} with status {2}.”.format(self.name, translated mapping(0 → “Draft”, 1 → “Submitted”, 2 → “Cancelled”) at self.docstatus,  ….

**Local steps**

- Evaluate self.reload().
- Evaluate self.check\_permission(“write”).
- If (self.docstatus differs from 1 or self.status differs from “Failed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 1 → self.status differs from “Failed”.
  - Call the validation error handler Platform.throw(translated “Only a submitted deletion with status Failed can be retried. {0} is {1} with status {2}.”.format(self.name, translated mapping(0 → “Draft”, 1 → “Submitted”, 2 → “Cancelled”) at s ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.status → “Not Set”.
- Evaluate self.validate\_to\_delete\_list().
- Evaluate self.before\_submit().
- Evaluate self.reset\_task\_flags().
- Set self.flags.ignore\_validate\_update\_after\_submit from true.
- Evaluate self.save().
- Evaluate self.\_start\_deletion\_tasks().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate to delete list](operations-015.md#op-53a7f63aab9410), [before submit](operations-015.md#op-089f39dc76c401), [reset task flags](operations-015.md#op-a56c10a036e166), [start deletion tasks](operations-016.md#op-7172e6a7cc10eb).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1051) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L598)

<a id="op-7172e6a7cc10eb"></a>
### Transaction Deletion Record.start deletion tasks

`operation_enterprise_binding_enterprise_setup_doctype_transaction_deletion_record_transaction_deletion_record_transactiondeletionrecord_start_deletion_tasks`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Running”).
- Evaluate self.\_set\_deletion\_cache().
- Evaluate self.enqueue\_task(task = “Delete Leads and Addresses”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set deletion cache](operations-015.md#op-ada702a38c661a), [enqueue task](operations-015.md#op-c63a57f907970b).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L180)

<a id="op-a720b6b35a7cf3"></a>
### Transaction Deletion Record.delete bins

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_bins`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_all · read doctype via get\_all.

**State and service calls** call db\_set on self · request delete on “Bin”.

**Explicit results** no value.

**Local steps**

- Evaluate self.validate\_doc\_status().
- If self.delete\_transactions\_status differs from “Completed”.
  - Evaluate self.enqueue\_task(task = “Delete Leads and Addresses”).
  - Return no value.
- If self.delete\_bin\_data\_status equals “Pending”.
  - Set stock\_related\_doctypes from list(“Item”, “Warehouse”, “Stock Entry”, “Delivery Note”, …).
  - If not self.\_is\_any\_doctype\_in\_deletion\_list(stock\_related\_doctypes).
    - Evaluate self.db\_set(“delete\_bin\_data\_status”, “Skipped”).
  - Otherwise.
    - Bind dependencies RECALCULATED\_FIELDS.
    - Bind dependencies get\_bin.
    - Set bin\_value\_fields from tuple(expanded RECALCULATED\_FIELDS, “reserved\_stock”).
    - Set warehouses from Platform.get\_all(“Warehouse”, filters = mapping(“company” → self.company), pluck = “name”).
    - Set item\_warehouses from set().
    - For each doctype in tuple(“Bin”, “Stock Ledger Entry”).
      - Evaluate item\_warehouses.update(generator of tuple(row) for row drawn from Platform.get\_all(doctype, filters = mapping(“warehouse” → list(“in”, warehouses)), fields = list(“item\_code”, “warehouse”), distinct = true ….
        - Draw row from Platform.get\_all(doctype, filters = mapping(“warehouse” → list(“in”, warehouses)), fields = list(“item\_code”, “warehouse”), distinct = true, as\_list = true).
    - For each tuple(item\_code, warehouse) in sorted(item\_warehouses).
      - Set bin from get\_bin(item\_code, warehouse).
      - Evaluate bin.recalculate\_values().
      - Evaluate bin.update\_reserved\_stock().
      - If not any(generator of flt(bin.get(field)) for field drawn from bin\_value\_fields).
        - Draw field from bin\_value\_fields.
        - Evaluate Platform.db.delete(“Bin”, mapping(“name” → bin.name, expand dict.fromkeys(bin\_value\_fields, 0))).
    - Evaluate self.db\_set(“delete\_bin\_data\_status”, “Completed”).
- Evaluate self.db\_set(“status”, “Completed”).
- Evaluate self.db\_set(“error\_log”, no value).
- Evaluate self.\_clear\_deletion\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doc status](operations-016.md#op-7bdb2fcc1ad83e), [enqueue task](operations-015.md#op-c63a57f907970b), [is any doctype in deletion list](operations-015.md#op-0c153b043f06d0), [clear deletion cache](operations-015.md#op-f7faa738d65191).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1012) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L560)

<a id="op-0bbb6972ee9cad"></a>
### Transaction Deletion Record.delete lead addresses

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_lead_addresses`

**Inputs** self.

**Record and data access** read “Lead” via get\_all.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- Evaluate self.validate\_doc\_status().
- If self.delete\_leads\_and\_addresses\_status equals “Pending”.
  - If not self.\_is\_any\_doctype\_in\_deletion\_list(list(“Lead”)).
    - Evaluate self.db\_set(“delete\_leads\_and\_addresses\_status”, “Skipped”).
    - Evaluate self.enqueue\_task(task = “Reset Company Values”).
    - Return no value.
  - Set leads from Platform.db.get\_all(“Lead”, filters = mapping(“company” → self.company), pluck = “name”).
  - If leads.
    - For each doctype in tuple(“Address”, “Contact”).
      - Evaluate self.delete\_lead\_linked\_records(doctype, leads).
    - Set customer from qb.DocType(“Customer”).
    - Evaluate nested operand in the contract(nested operand in the contract).set(customer.lead\_name, no value).where(customer.lead\_name.isin(leads)).run().
  - Evaluate self.db\_set(“delete\_leads\_and\_addresses\_status”, “Completed”).
- Evaluate self.enqueue\_task(task = “Reset Company Values”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doc status](operations-016.md#op-7bdb2fcc1ad83e), [is any doctype in deletion list](operations-015.md#op-0c153b043f06d0), [enqueue task](operations-015.md#op-c63a57f907970b), [delete lead linked records](operations-016.md#op-72ac05da0795b5).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1017) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L565)

<a id="op-72ac05da0795b5"></a>
### Transaction Deletion Record.delete lead linked records

`operation_enterprise_binding_enterprise_setup_doctype_transaction_deletion_record_transaction_deletion_record_transactiondeletionrecord_delete_lead_linked_records`

**Inputs** self, doctype, leads.

**Record and data access** read “Dynamic Link” via get\_all.

**State and service calls** request delete on doctype · request delete on “Dynamic Link”.

**Explicit results** no value.

**Local steps**

- Set linked\_records from Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → doctype, “link\_doctype” → “Lead”, “link\_name” → list(“in”, leads)), pluck = “parent”).
- If not linked\_records.
  - Return no value.
- Set dynamic\_link from qb.DocType(“Dynamic Link”).
- Set other\_links from qb.from\_(dynamic\_link).select(dynamic\_link.parent).where(((dynamic\_link.parenttype equals doctype bitwise and dynamic\_link.parent.isin(linked\_records)) bitwise and (dynamic\_link.link\_doctype differs from “ ….
- Set parent from qb.DocType(doctype).
- Set exclusive\_records from nested operand in the contract(nested operand in the contract).select(parent.name).where((nested operand in the contract.name.isin(linked\_records) bitwise and nested operand in the contract.name.notin(othe ….
- If exclusive\_records.
  - Evaluate self.delete\_version\_log(doctype, exclusive\_records).
  - Evaluate self.delete\_communications(doctype, exclusive\_records).
  - Evaluate self.delete\_comments(doctype, exclusive\_records).
  - Evaluate self.delete\_document\_references(doctype, exclusive\_records).
  - Evaluate self.unlink\_attachments(doctype, exclusive\_records).
  - Evaluate self.delete\_child\_tables(doctype, exclusive\_records).
  - Evaluate Platform.db.delete(doctype, mapping(“name” → list(“in”, exclusive\_records))).
- Evaluate Platform.db.delete(“Dynamic Link”, mapping(“parenttype” → doctype, “link\_doctype” → “Lead”, “link\_name” → list(“in”, leads))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete version log](operations-016.md#op-51c58c4c9375f4), [delete communications](operations-016.md#op-a5320aa79bcd7c), [delete comments](operations-017.md#op-fc0cf1c30b1c90), [delete document references](operations-016.md#op-251b4701cf7751), [unlink attachments](operations-017.md#op-56e1c5a46ef644), [delete child tables](operations-016.md#op-0e2fc20f065ae7).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L177)

<a id="op-02b50a84c9e457"></a>
### Transaction Deletion Record.reset company values

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_reset_company_values`

**Inputs** self.

**State and service calls** call db\_set on self · request set\_value on “Company”.

**Explicit results** no value.

**Local steps**

- Evaluate self.validate\_doc\_status().
- If self.reset\_company\_default\_values\_status equals “Pending”.
  - Set sales\_related\_doctypes from list(“Sales Order”, “Sales Invoice”, “Quotation”, “Delivery Note”).
  - If not self.\_is\_any\_doctype\_in\_deletion\_list(sales\_related\_doctypes).
    - Evaluate self.db\_set(“reset\_company\_default\_values\_status”, “Skipped”).
    - Evaluate self.enqueue\_task(task = “Clear Notifications”).
    - Return no value.
  - Evaluate Platform.db.set\_value(“Company”, self.company, mapping(“total\_monthly\_sales” → 0, “sales\_monthly\_history” → no value, “transactions\_annual\_history” → no value)).
  - Evaluate Platform.clear\_document\_cache(“Company”, self.company).
  - Evaluate self.db\_set(“reset\_company\_default\_values\_status”, “Completed”).
- Evaluate self.enqueue\_task(task = “Clear Notifications”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doc status](operations-016.md#op-7bdb2fcc1ad83e), [is any doctype in deletion list](operations-015.md#op-0c153b043f06d0), [enqueue task](operations-015.md#op-c63a57f907970b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1048) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L595)

<a id="op-60c00aeccba9d2"></a>
### Transaction Deletion Record.initialize doctypes to be deleted table

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_initialize_record_types_to_be_deleted_table`

**Inputs** self.

**Record and data access** read to\_delete\_item.doctype\_name via count.

**State and service calls** call db\_set on existing · call db\_set on self.

**Explicit failure paths** validation helper — translated “No DocTypes in To Delete list. Please generate or import the list before submitting.”.

**Local steps**

- Evaluate self.validate\_doc\_status().
- If self.initialize\_doctypes\_table\_status equals “Pending”.
  - If not self.doctypes\_to\_delete.
    - Call the validation error handler Platform.throw(translated “No DocTypes in To Delete list. Please generate or import the list before submitting.”, title = translated “Empty To Delete List”).
  - Set tables from self.get\_all\_child\_doctypes().
  - For each to\_delete\_item in self.doctypes\_to\_delete.
    - Set filters from mapping(to\_delete\_item.company\_field → self.company) when to\_delete\_item.company\_field, otherwise no value.
      - Value choice on to\_delete\_item.company\_field — true gives mapping(to\_delete\_item.company\_field → self.company), false gives no value.
    - If Platform.db.count(to\_delete\_item.doctype\_name, filters = filters) &gt; 0.
      - Set existing from next(generator of row for row drawn from self.doctypes where (row.doctype\_name equals to\_delete\_item.doctype\_name and row.docfield\_name equals to\_delete\_item.company\_field), no value).
        - Draw row from self.doctypes, keep a combination only if ((row.doctype\_name equals to\_delete\_item.doctype\_name and row.docfield\_name equals to\_delete\_item.company\_field)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.doctype\_name equals to\_delete\_item.doctype\_name → row.docfield\_name equals to\_delete\_item.company\_field.
      - If existing.
        - Evaluate existing.db\_set(“done”, 0).
      - Otherwise.
        - Evaluate self.populate\_doctypes\_table(tables, to\_delete\_item.doctype\_name, to\_delete\_item.company\_field, 0).
  - Evaluate self.db\_set(“initialize\_doctypes\_table\_status”, “Completed”).
- Evaluate self.enqueue\_task(task = “Delete Transactions”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doc status](operations-016.md#op-7bdb2fcc1ad83e), [get all child doctypes](operations-016.md#op-9a2325d01d5e7c), [populate doctypes table](operations-016.md#op-1675a8947e1e0e), [enqueue task](operations-015.md#op-c63a57f907970b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1040) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L587)

<a id="op-dc7389ca7b6190"></a>
### Transaction Deletion Record.delete company transactions

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_company_transactions`

**Inputs** self.

**Record and data access** read docfield.doctype\_name via count · read docfield.doctype\_name via get\_all · read “Transaction Deletion Record To Delete” via get\_value · read “Transaction Deletion Record Details” via get\_all.

**State and service calls** request set\_value on docfield.doctype · request set\_value on “Transaction Deletion Record To Delete” · call db\_set on self.

**Explicit failure paths** validation helper — translated “Cannot delete protected core DocType: {0}”.format(docfield.doctype\_name).

**Local steps**

- Evaluate self.validate\_doc\_status().
- If self.delete\_transactions\_status equals “Pending”.
  - Set protected\_doctypes from \_get\_protected\_doctypes\_internal().
  - For each docfield in self.doctypes.
    - If (docfield.doctype\_name differs from self.doctype and not docfield.done).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.doctype\_name differs from self.doctype → not docfield.done.
      - If docfield.doctype\_name belongs to protected\_doctypes.
        - Set error\_msg from formatted text CRITICAL: Attempted to delete protected DocType: {docfield.doctype\_name}.
        - Evaluate Platform.log\_error(error\_msg, “Transaction Deletion Security”).
        - Call the validation error handler Platform.throw(translated “Cannot delete protected core DocType: {0}”.format(docfield.doctype\_name), title = translated “Protected DocType”).
      - Set company\_field from docfield.docfield\_name.
      - If company\_field.
        - Set no\_of\_docs from self.get\_number\_of\_docs\_linked\_with\_specified\_company(docfield.doctype\_name, company\_field).
      - Otherwise.
        - Set no\_of\_docs from Platform.db.count(docfield.doctype\_name).
      - If no\_of\_docs &gt; 0.
        - If company\_field.
          - Set reference\_docs from Platform.get\_all(docfield.doctype\_name, filters = mapping(company\_field → self.company), fields = list(“name”), order\_by = “name asc”, limit = self.batch\_size).
        - Otherwise.
          - Set reference\_docs from Platform.get\_all(docfield.doctype\_name, fields = list(“name”), order\_by = “name asc”, limit = self.batch\_size).
        - Set reference\_doc\_names from list of r.name for r drawn from reference\_docs.
          - Draw r from reference\_docs.
        - Set batch\_nos from self.get\_affected\_batches(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.delete\_version\_log(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.delete\_communications(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.delete\_comments(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.delete\_document\_references(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.unlink\_attachments(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.delete\_child\_tables(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.delete\_docs\_linked\_with\_specified\_company(docfield.doctype\_name, reference\_doc\_names).
        - Evaluate self.recalculate\_batch\_quantities(batch\_nos).
        - Set processed from (int(docfield.no\_of\_docs) + len(reference\_doc\_names)).
        - Evaluate Platform.db.set\_value(docfield.doctype, docfield.name, “no\_of\_docs”, processed).
      - Otherwise.
        - Evaluate Platform.db.set\_value(docfield.doctype, docfield.name, “done”, 1).
        - Set to\_delete\_row from Platform.db.get\_value(“Transaction Deletion Record To Delete”, mapping(“parent” → self.name, “doctype\_name” → docfield.doctype\_name, “company\_field” → company\_field), “name”).
        - If to\_delete\_row.
          - Evaluate Platform.db.set\_value(“Transaction Deletion Record To Delete”, to\_delete\_row, “deleted”, 1).
  - Set pending\_doctypes from Platform.db.get\_all(“Transaction Deletion Record Details”, filters = mapping(“parent” → self.name, “done” → 0), pluck = “doctype\_name”).
  - If pending\_doctypes.
    - Evaluate self.enqueue\_task(task = “Delete Transactions”).
  - Otherwise.
    - Evaluate self.db\_set(“delete\_transactions\_status”, “Completed”).
    - Evaluate self.db\_set(“delete\_bin\_data\_status”, “Pending”).
    - Evaluate self.enqueue\_task(task = “Delete Bins”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doc status](operations-016.md#op-7bdb2fcc1ad83e), [get number of docs linked with specified company](operations-016.md#op-42337c9215a41d), [get affected batches](operations-016.md#op-ce075a99651bd9), [delete version log](operations-016.md#op-51c58c4c9375f4), [delete communications](operations-016.md#op-a5320aa79bcd7c), [delete comments](operations-017.md#op-fc0cf1c30b1c90), [delete document references](operations-016.md#op-251b4701cf7751), [unlink attachments](operations-017.md#op-56e1c5a46ef644), [delete child tables](operations-016.md#op-0e2fc20f065ae7), [delete docs linked with specified company](operations-016.md#op-de6d3ecd7b5365), [recalculate batch quantities](operations-016.md#op-558d8db127f103), [enqueue task](operations-015.md#op-c63a57f907970b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1016) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L564)

<a id="op-80854c7986a1ef"></a>
### Transaction Deletion Record.get doctypes to be ignored list

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_record_types_to_be_ignored_list`

**Inputs** self.

**Record and data access** read “DocType” via get\_all.

**Explicit results** doctypes\_to\_be\_ignored\_list.

**Local steps**

- Set doctypes\_to\_be\_ignored\_list from Platform.get\_all(“DocType”, or\_filters = list(list(“issingle”, “=”, 1), list(“is\_virtual”, “=”, 1)), pluck = “name”).
- For each doctype in self.doctypes\_to\_be\_ignored.
  - Evaluate doctypes\_to\_be\_ignored\_list.append(doctype.doctype\_name).
- Return doctypes\_to\_be\_ignored\_list.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L1576) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1034) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L581)

<a id="op-028eddd7a06b5f"></a>
### Transaction Deletion Record.get doctypes with company field

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_record_types_with_company_field`

**Inputs** self, doctypes\_to\_be\_ignored\_list.

**Record and data access** read “DocField” via get\_all.

**Explicit results** docfields.

**Local steps**

- Set docfields from Platform.get\_all(“DocField”, filters = mapping(“fieldtype” → “Link”, “options” → “Company”, “parent” → list(“not in”, doctypes\_to\_be\_ignored\_list)), fields = list(“parent”, “fieldname”)).
- Return docfields.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L1766) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1035) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L582)

<a id="op-9a2325d01d5e7c"></a>
### Transaction Deletion Record.get all child doctypes

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_all_child_record_types`

**Inputs** self.

**Record and data access** read “DocType” via get\_all.

**Explicit results** Platform.get\_all(“DocType”, filters = mapping(“istable” → 1), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“DocType”, filters = mapping(“istable” → 1), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L1948) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1028) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L576)

<a id="op-42337c9215a41d"></a>
### Transaction Deletion Record.get number of docs linked with specified company

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_number_of_records_linked_with_specified_company`

**Inputs** self, doctype, company\_fieldname.

**Record and data access** read doctype via count.

**Explicit results** Platform.db.count(doctype, mapping(company\_fieldname → self.company)).

**Local steps**

- Return Platform.db.count(doctype, mapping(company\_fieldname → self.company)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L2050) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L580)

<a id="op-5d92e7d2a9f367"></a>
### Transaction Deletion Record.get company field

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_get_company_field`

**Inputs** self, doctype\_name.

**Record and data access** read “DocField” via get\_value.

**Explicit results** Platform.db.get\_value(“DocField”, mapping(“parent” → doctype\_name, “fieldtype” → “Link”, “options” → “Company”), “fieldname”).

**Local steps**

- Return Platform.db.get\_value(“DocField”, mapping(“parent” → doctype\_name, “fieldtype” → “Link”, “options” → “Company”), “fieldname”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L2142) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1030) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L578)

<a id="op-1675a8947e1e0e"></a>
### Transaction Deletion Record.populate doctypes table

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_populate_record_types_table`

**Inputs** self, tables, doctype, company\_field, no\_of\_docs.

**State and service calls** call save on self.

**Local steps**

- Set self.flags.ignore\_validate\_update\_after\_submit from true.
- If doctype does not belong to tables.
  - Evaluate self.append(“doctypes”, mapping(“doctype\_name” → doctype, “docfield\_name” → company\_field, “no\_of\_docs” → no\_of\_docs)).
- Evaluate self.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L2279) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1046) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L593)

<a id="op-0e2fc20f065ae7"></a>
### Transaction Deletion Record.delete child tables

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_child_tables`

**Inputs** self, doctype, reference\_doc\_names.

**State and service calls** request delete on table.

**Local steps**

- Set child\_tables from self.\_get\_child\_tables(doctype).
- For each table in child\_tables.
  - Evaluate Platform.db.delete(table, mapping(“parenttype” → doctype, “parent” → list(“in”, reference\_doc\_names))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get child tables](operations-015.md#op-ea1ed39790a499).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1013) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L561)

<a id="op-de6d3ecd7b5365"></a>
### Transaction Deletion Record.delete docs linked with specified company

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_records_linked_with_specified_company`

**Inputs** self, doctype, reference\_doc\_names.

**State and service calls** request delete on doctype.

**Local steps**

- Evaluate Platform.db.delete(doctype, mapping(“name” → tuple(“in”, reference\_doc\_names))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L2639) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L567)

<a id="op-ce075a99651bd9"></a>
### Transaction Deletion Record.get affected batches

`operation_enterprise_binding_enterprise_setup_doctype_transaction_deletion_record_transaction_deletion_record_transactiondeletionrecord_get_affected_batches`

**Inputs** self, doctype, docnames.

**Record and data access** read doctype via get\_all · read “Serial and Batch Entry” via get\_all.

**Explicit results** batches.

**Local steps**

- Set batches from set().
- If doctype equals “Stock Ledger Entry”.
  - Set entries from Platform.get\_all(doctype, filters = mapping(“name” → list(“in”, docnames)), fields = list(“batch\_no”, “serial\_and\_batch\_bundle”)).
  - Evaluate batches.update(generator of row.batch\_no for row drawn from entries where row.batch\_no).
    - Draw row from entries, keep a combination only if (row.batch\_no).
  - Set bundles from list of row.serial\_and\_batch\_bundle for row drawn from entries where row.serial\_and\_batch\_bundle.
    - Draw row from entries, keep a combination only if (row.serial\_and\_batch\_bundle).
- Otherwise.
  - If doctype equals “Serial and Batch Bundle”.
    - Set bundles from docnames.
  - Otherwise.
    - Return batches.
- If bundles.
  - Evaluate batches.update(Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parenttype” → “Serial and Batch Bundle”, “parent” → list(“in”, bundles), “batch\_no” → list(“is”, “set”)), pluck = “batch\_no”)).
- Return batches.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L178)

<a id="op-558d8db127f103"></a>
### Transaction Deletion Record.recalculate batch quantities

`operation_enterprise_binding_enterprise_setup_doctype_transaction_deletion_record_transaction_deletion_record_transactiondeletionrecord_recalculate_batch_quantities`

**Inputs** self, batch\_nos.

**State and service calls** request set\_value on “Batch”.

**Explicit results** no value.

**Local steps**

- If not batch\_nos.
  - Return no value.
- Set sle from qb.DocType(“Stock Ledger Entry”).
- Set entry from qb.DocType(“Serial and Batch Entry”).
- Set legacy\_quantities from nested operand in the contract(nested operand in the contract).select(sle.batch\_no, nested operand in the contract.as\_(“qty”)).where(((nested operand in the contract.is\_cancelled equals 0 bitwise and neste ….
- Set bundle\_quantities from nested operand in the contract(nested operand in the contract).select(entry.batch\_no, nested operand in the contract.as\_(“qty”)).where(((nested operand in the contract.is\_cancelled equals 0 bitwise and nes ….
- Set quantities from dict.fromkeys(batch\_nos, 0).
- For each query in tuple(legacy\_quantities, bundle\_quantities).
  - For each row in query.run(as\_dict = true).
    - Update quantities at row.batch\_no using + row.qty.
- For each tuple(batch\_no, qty) in quantities.items().
  - Evaluate Platform.db.set\_value(“Batch”, batch\_no, “batch\_qty”, qty, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L179)

<a id="op-251b4701cf7751"></a>
### Transaction Deletion Record.delete document references

`operation_enterprise_binding_enterprise_setup_doctype_transaction_deletion_record_transaction_deletion_record_transactiondeletionrecord_delete_document_references`

**Inputs** self, doctype, docnames.

**State and service calls** request delete on reference\_doctype.

**Local steps**

- For each tuple(reference\_doctype, doctype\_field, name\_field) in tuple(tuple(“ToDo”, “reference\_type”, “reference\_name”), tuple(“DocShare”, “share\_doctype”, “share\_name”), tuple(“Tag Link”, “document\_type”, “document\_name”), tuple(“Document Follow”, “ref\_doctype”, “ref\_ ….
  - Evaluate Platform.db.delete(reference\_doctype, mapping(doctype\_field → doctype, name\_field → list(“in”, docnames))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L176)

<a id="op-51c58c4c9375f4"></a>
### Transaction Deletion Record.delete version log

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_version_log`

**Inputs** self, doctype, docnames.

**Local steps**

- Set versions from qb.DocType(“Version”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((versions.ref\_doctype equals doctype bitwise and nested operand in the contract.docname.isin(docnames))).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L3469) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L568)

<a id="op-a5320aa79bcd7c"></a>
### Transaction Deletion Record.delete communications

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_communications`

**Inputs** self, doctype, reference\_doc\_names.

**Record and data access** read “Communication” via get\_all.

**State and service calls** request delete\_doc for “Communication”.

**Explicit results** no value.

**Local steps**

- Set communications from Platform.get\_all(“Communication”, filters = mapping(“reference\_doctype” → doctype, “reference\_name” → list(“in”, reference\_doc\_names))).
- Set communication\_names from list of c.name for c drawn from communications.
  - Draw c from communications.
- If not communication\_names.
  - Return no value.
- For each batch in create\_batch(communication\_names, self.batch\_size).
  - Evaluate Platform.delete\_doc(“Communication”, batch, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L3653) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1015) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L563)
