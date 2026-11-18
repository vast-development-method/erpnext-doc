# Inventory and warehouses · operations 52

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Repost item valuation

[Record definition](../../../../data/record-types/repost_item_valuation.json)

<a id="op-fe9b5f02b4078f"></a>
### Repost Item Valuation.get saved repost started at

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_get_saved_repost_started_at`

**Inputs** self.

**Explicit results** get\_reposting\_data(self.reposting\_data\_file).get(“repost\_started\_at”).

**Local steps**

- If self.reposting\_data\_file.
  - Return get\_reposting\_data(self.reposting\_data\_file).get(“repost\_started\_at”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L566)

<a id="op-5a7dbdd7a0c40d"></a>
### Repost Item Valuation.merge queued item reposts

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_merge_queued_item_reposts`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If not self.can\_merge\_queued\_item\_reposts().
  - Return no value.
- Set merged from get\_mergeable\_item\_reposts(self).
- If not merged.
  - Return no value.
- Set items from list of get\_repost\_item(row) for row drawn from list(self, expanded merged).
  - Draw row from list(self, expanded merged).
- Evaluate self.db\_set(“items\_to\_be\_repost”, Platform.as\_json(items)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can merge queued item reposts](operations-052.md#op-7af222fd7f9d39).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L567)

<a id="op-7af222fd7f9d39"></a>
### Repost Item Valuation.can merge queued item reposts

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_can_merge_queued_item_reposts`

**Inputs** self.

**Record and data access** read “Stock Reposting Settings” via get\_single\_value.

**Explicit results** (self.based\_on equals “Item and Warehouse” and not self.items\_to\_be\_repost and not self.reposting\_data\_file and not self.via\_landed\_cost\_voucher and not self.repost\_only\_accounting\_ledgers and not Platform ….

**Local steps**

- Return (self.based\_on equals “Item and Warehouse” and not self.items\_to\_be\_repost and not self.reposting\_data\_file and not self.via\_landed\_cost\_voucher and not self.repost\_only\_accounting\_ledgers and not Platform ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.based\_on equals “Item and Warehouse” → not self.items\_to\_be\_repost → not self.reposting\_data\_file → not self.via\_landed\_cost\_voucher → not self.repost\_only\_accounting\_ledgers → not Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”) → not has\_failed\_merged\_repost(self.company).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L560)

<a id="op-99444f20b9a875"></a>
### Repost Item Valuation.get item reposts

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_get_item_reposts`

**Inputs** self.

**Explicit results** list of Platform.\_dict(row) for row drawn from items · list(get\_repost\_item(self)).

**Local steps**

- Set items from json.loads((self.items\_to\_be\_repost or “&#91;&#93;”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.items\_to\_be\_repost → “&#91;&#93;”.
- If len(items) &gt; 1.
  - Return list of Platform.\_dict(row) for row drawn from items.
    - Draw row from items.
- Return list(get\_repost\_item(self)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L562)

<a id="op-9f364102122188"></a>
### Repost Item Valuation.skip merged reposts

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_repostitemvaluation_skip_merged_reposts`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set merged from list of row.repost\_item\_valuation for row drawn from self.get\_item\_reposts() at slice 1 to no value.
  - Draw row from self.get\_item\_reposts() at slice 1 to no value.
- If (self.based\_on differs from “Item and Warehouse” or not merged).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.based\_on differs from “Item and Warehouse” → not merged.
  - Return no value.
- Set riv from Platform.qb.DocType(“Repost Item Valuation”).
- Evaluate nested operand in the contract(nested operand in the contract).set(riv.status, “Skipped”).where((nested operand in the contract.name.isin(merged) bitwise and riv.status equals “Queued”)).run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get item reposts](operations-052.md#op-99444f20b9a875).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L568)

<a id="op-be3eaf49ee5d5e"></a>
### Repost Item Valuation.recalculate valuation rate

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_recalculate_valuation_rate`

**Inputs** self.

**Record and data access** resolve a document from self.voucher\_type via get\_doc.

**State and service calls** call db\_set on item.

**Local steps**

- Set doc from Platform.get\_doc(self.voucher\_type, self.voucher\_no).
- If doc.get(“is\_internal\_supplier”).
  - Evaluate doc.set\_sales\_incoming\_rate\_for\_internal\_transfer().
- Evaluate doc.update\_valuation\_rate().
- For each item in doc.items.
  - Evaluate item.db\_set(“valuation\_rate”, item.valuation\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L6092) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L800) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L458)

<a id="op-9dd6179bd8763f"></a>
### Repost Item Valuation.recreate stock ledger entries

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_item_valuation_recreate_stock_ledger_entries`

**Inputs** self.

**Record and data access** resolve a document from self.voucher\_type via get\_doc.

**State and service calls** call db\_set on doc.

**Local steps**

- If (self.based\_on equals “Transaction” and self.recreate\_stock\_ledgers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.based\_on equals “Transaction” → self.recreate\_stock\_ledgers.
  - Set doc from Platform.get\_doc(self.voucher\_type, self.voucher\_no).
  - Evaluate doc.db\_set(“docstatus”, 2).
  - Evaluate doc.update\_stock\_ledger(allow\_negative\_stock = true).
  - Evaluate doc.db\_set(“docstatus”, 1).
  - Evaluate doc.update\_stock\_ledger(allow\_negative\_stock = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0799.json#L6286) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L801) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L459)

<a id="op-ce26badcde80eb"></a>
### Bulk restart reposting

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_bulk_restart_reposting`

**Inputs** names.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Repost Item Valuation” via get\_doc.

**State and service calls** msgprint with translated “Repost Item Valuation restarted for selected failed records.”.

**Local steps**

- Evaluate Platform.has\_permission(“Repost Item Valuation”, “write”, throw = true).
- Set names from Platform.parse\_json(names).
- For each name in names.
  - Set doc from Platform.get\_doc(“Repost Item Valuation”, name).
  - If doc.status differs from “Failed”.
    - Continue with the next iteration or loop test.
  - Evaluate doc.restart\_reposting().
- Evaluate Platform.msgprint(translated “Repost Item Valuation restarted for selected failed records.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Repost Item Valuation”, “write”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L427)

<a id="op-173e5b69a549c2"></a>
### Has failed merged repost

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_has_failed_merged_repost`

**Inputs** company.

**Record and data access** read “Repost Item Valuation” via get\_all.

**Explicit results** any(generator of len(json.loads(items)) &gt; 1 for items drawn from failed).

**Local steps**

- Set failed from Platform.get\_all(“Repost Item Valuation”, filters = mapping(“company” → company, “based\_on” → “Item and Warehouse”, “status” → “Failed”, “docstatus” → 1, …), pluck = “items\_to\_be\_repost”).
- Return any(generator of len(json.loads(items)) &gt; 1 for items drawn from failed).
  - Draw items from failed.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L559)

<a id="op-ba499e98e35588"></a>
### Get mergeable item reposts

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_get_mergeable_item_reposts`

**Inputs** doc.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(riv.creation).limit(MERGED\_REPOST\_LIMIT).run(as\_dict = true).

**Local steps**

- Set riv from Platform.qb.DocType(“Repost Item Valuation”).
- Return nested operand in the contract(nested operand in the contract).orderby(riv.creation).limit(MERGED\_REPOST\_LIMIT).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L556)

<a id="op-dc26efc793331b"></a>
### Get repost item

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_get_repost_item`

**Inputs** row.

**Explicit results** Platform.\_dict(item\_code = row.item\_code, warehouse = row.warehouse, posting\_date = row.posting\_date, posting\_time = row.posting\_time, …).

**Local steps**

- Return Platform.\_dict(item\_code = row.item\_code, warehouse = row.warehouse, posting\_date = row.posting\_date, posting\_time = row.posting\_time, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1060) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L557)

<a id="op-4811c5789ed7f2"></a>
### On doctype update

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Repost Item Valuation”.

**Local steps**

- Evaluate Platform.db.add\_index(“Repost Item Valuation”, list(“warehouse”, “item\_code”), “item\_warehouse”).
- Evaluate Platform.db.add\_index(“Repost Item Valuation”, list(“voucher\_no”, “voucher\_type”, “status”), “voucher\_status”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L442)

<a id="op-74cf794bd0b7bf"></a>
### Repost

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost`

**Inputs** doc.

**Record and data access** read “Repost Item Valuation” via exists · read “Email Account” via get\_cached\_value.

**State and service calls** commit · call db\_set on doc · rollback · request set\_value on doc.doctype.

**Explicit results** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - Set Platform.flags.through\_repost\_item\_valuation from true.
  - If not Platform.db.exists(“Repost Item Valuation”, doc.name).
    - Return no value.
  - Update Platform.db.MAX\_WRITES\_PER\_TRANSACTION using × 4.
  - Set doc.flags.repost\_started\_at from (doc.get\_saved\_repost\_started\_at() or now()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_saved\_repost\_started\_at() → now().
  - Evaluate doc.set\_status(“In Progress”).
  - Evaluate doc.merge\_queued\_item\_reposts().
  - Evaluate mark\_closing\_entries\_outdated(doc.company, doc.posting\_date).
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
  - If (doc.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) and doc.recalculate\_valuation\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.voucher\_type belongs to list(“Purchase Receipt”, “Purchase Invoice”) → doc.recalculate\_valuation\_rate.
    - Evaluate doc.\_recalculate\_valuation\_rate().
  - If doc.recreate\_stock\_ledgers.
    - Evaluate doc.recreate\_stock\_ledger\_entries().
  - If doc.repost\_only\_accounting\_ledgers.
    - Evaluate repost\_gl\_entries(doc).
  - Otherwise.
    - Evaluate repost\_sl\_entries(doc).
    - Set vouchers from get\_reposted\_vouchers(doc).
    - Evaluate repost\_gl\_entries(doc, vouchers).
    - Evaluate update\_consumed\_material\_cost\_for\_vouchers(vouchers).
  - Evaluate doc.skip\_merged\_reposts().
  - Evaluate doc.set\_status(“Completed”).
  - Evaluate doc.db\_set(“reposting\_data\_file”, no value).
  - Evaluate remove\_attached\_file(doc.name).
- On failure (Exception) bound to e.
  - If Platform.in\_test.
    - Propagate the active failure.
  - Evaluate Platform.db.rollback().
  - Set traceback from Platform.get\_traceback().
  - Evaluate doc.log\_error(“Unable to repost item valuation”).
  - Set message from Platform.message\_log.pop() when Platform.message\_log, otherwise empty text.
    - Value choice on Platform.message\_log — true gives Platform.message\_log.pop(), false gives empty text.
  - If isinstance(message, dict).
    - Set message from message.get(“message”).
  - Set status from “Failed”.
  - Set traceback\_lower from traceback.lower() when traceback, otherwise empty text.
    - Value choice on traceback — true gives traceback.lower(), false gives empty text.
  - If (isinstance(e, RecoverableErrors) or (traceback\_lower and (“timeout” belongs to traceback\_lower or “deadlock found” belongs to traceback\_lower))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(e, RecoverableErrors) → (traceback\_lower and (“timeout” belongs to traceback\_lower or “deadlock found” belongs to traceback\_lower)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in traceback\_lower → (“timeout” belongs to traceback\_lower or “deadlock found” belongs to traceback\_lower).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “timeout” belongs to traceback\_lower → “deadlock found” belongs to traceback\_lower.
    - Set status from “In Progress”.
  - If traceback.
    - Update message using + ((text in the contract + text in the contract) + traceback).
  - Evaluate Platform.db.set\_value(doc.doctype, doc.name, mapping(“error\_log” → message, “status” → status)).
  - If isinstance(e, JobTimeoutException).
    - Propagate the active failure.
  - If status equals “Failed”.
    - Set outgoing\_email\_account from Platform.get\_cached\_value(“Email Account”, mapping(“default\_outgoing” → 1, “enable\_outgoing” → 1), “name”).
    - If (outgoing\_email\_account and not isinstance(e, RecoverableErrors)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in outgoing\_email\_account → not isinstance(e, RecoverableErrors).
      - Evaluate notify\_error\_to\_stock\_managers(doc, message).
      - Evaluate doc.set\_status(“Failed”).
- On exit, including pending return or failure.
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now() · configured or stored value from Platform.get\_cached\_value(“Email Account”, mapping(“default\_outgoing” → 1, “enable\_outgoing” → 1), “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L444)

<a id="op-5b92be89b5a28b"></a>
### Remove attached file

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_remove_attached_file`

**Inputs** docname.

**Record and data access** read “File” via get\_value.

**State and service calls** request delete\_doc for “File”.

**Local steps**

- If file\_name bound to Platform.db.get\_value(“File”, mapping(“attached\_to\_name” → docname, “attached\_to\_doctype” → “Repost Item Valuation”), “name”).
  - Evaluate Platform.delete\_doc(“File”, file\_name, ignore\_permissions = true, delete\_permanently = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L3293) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L443)

<a id="op-858d823979136b"></a>
### Repost sl entries

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_stock_ledger_entries`

**Inputs** doc.

**Local steps**

- If doc.based\_on equals “Transaction”.
  - Evaluate repost\_future\_sle(voucher\_type = doc.voucher\_type, voucher\_no = doc.voucher\_no, allow\_negative\_stock = doc.allow\_negative\_stock, via\_landed\_cost\_voucher = doc.via\_landed\_cost\_voucher, …).
- Otherwise.
  - Evaluate repost\_future\_sle(items\_to\_be\_repost = doc.get\_item\_reposts(), allow\_negative\_stock = doc.allow\_negative\_stock, via\_landed\_cost\_voucher = doc.via\_landed\_cost\_voucher, doc = doc, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L474)

<a id="op-4cdcaec5d888d3"></a>
### Repost gl entries

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_repost_general_ledger_entries`

**Inputs** doc, transactions = no value.

**Record and data access** read “Stock Reposting Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not cint(Enterprise.is\_perpetual\_inventory\_enabled(doc.company)).
  - Return no value.
- If (doc.repost\_only\_accounting\_ledgers and doc.based\_on equals “Transaction”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.repost\_only\_accounting\_ledgers → doc.based\_on equals “Transaction”.
  - Set transactions from list(tuple(doc.voucher\_type, doc.voucher\_no)).
  - Evaluate repost\_gle\_for\_stock\_vouchers(transactions, doc.posting\_date, doc.company, repost\_doc = doc).
  - Return no value.
- If transactions is identical to no value.
  - Set transactions from get\_reposted\_vouchers(doc).
- Set enable\_separate\_reposting\_for\_gl from Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_separate\_reposting\_for\_gl”).
- If (enable\_separate\_reposting\_for\_gl and doc.based\_on equals “Item and Warehouse” and not doc.repost\_only\_accounting\_ledgers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enable\_separate\_reposting\_for\_gl → doc.based\_on equals “Item and Warehouse” → not doc.repost\_only\_accounting\_ledgers.
  - Evaluate make\_reposting\_for\_accounting\_ledgers(transactions, doc.company, repost\_doc = doc).
- Otherwise.
  - Evaluate repost\_gle\_for\_stock\_vouchers(transactions, doc.posting\_date, doc.company, repost\_doc = doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_separate\_reposting\_for\_gl”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L788) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L446)

<a id="op-d85c121d48d815"></a>
### Get reposted vouchers

`operation_enterprise_binding_enterprise_stock_doctype_repost_item_valuation_repost_item_valuation_get_reposted_vouchers`

**Inputs** doc.

**Explicit results** (\_get\_directly\_dependent\_vouchers(doc) + list(get\_affected\_transactions(doc))).

**Local steps**

- Return (\_get\_directly\_dependent\_vouchers(doc) + list(get\_affected\_transactions(doc))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L558)

<a id="op-8f2dbea8be192a"></a>
### Get directly dependent vouchers

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_get_directly_dependent_vouchers`

**Inputs** doc.

**Explicit results** affected\_vouchers.

**Local steps**

- Set items from set().
- Set warehouses from set().
- If doc.based\_on equals “Transaction”.
  - Set ref\_doc from Platform.get\_lazy\_doc(doc.voucher\_type, doc.voucher\_no).
  - Set tuple(doc\_items, doc\_warehouses) from ref\_doc.get\_items\_and\_warehouses().
  - Evaluate items.update(doc\_items).
  - Evaluate warehouses.update(doc\_warehouses).
  - Set sles from get\_items\_to\_be\_repost(doc.voucher\_type, doc.voucher\_no).
  - Set sle\_items from set of sle.item\_code for sle drawn from sles.
    - Draw sle from sles.
  - Set sle\_warehouses from set of sle.warehouse for sle drawn from sles.
    - Draw sle from sles.
  - Evaluate items.update(sle\_items).
  - Evaluate warehouses.update(sle\_warehouses).
- Otherwise.
  - For each row in doc.get\_item\_reposts().
    - Evaluate items.add(row.item\_code).
    - Evaluate warehouses.add(row.warehouse).
- Set affected\_vouchers from get\_future\_stock\_vouchers(posting\_date = doc.posting\_date, posting\_time = doc.posting\_time, for\_warehouses = list(warehouses), for\_items = list(items), …).
- Return affected\_vouchers.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L433)

<a id="op-5d649f6165b107"></a>
### Notify error to stock managers

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_notify_error_to_stock_managers`

**Inputs** doc, traceback.

**State and service calls** sendmail.

**Local steps**

- Set recipients from get\_recipients().
- Set subject from translated “Error while reposting item valuation”.
- Set message from ((((translated “Hi,” + text in the contract) + translated “An error has been appeared while reposting item valuation via {0}”.format(get\_link\_to\_form(doc.doctype, doc.name))) + text in the contract) + tran ….
- Evaluate Platform.sendmail(recipients = recipients, subject = subject, message = message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = subject, message = message).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L5581) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L441)

<a id="op-a3e73a51d05e82"></a>
### Get recipients

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_get_recipients`

**Inputs** no declared parameters.

**Record and data access** read “Stock Reposting Settings” via get\_single\_value.

**Explicit results** recipients.

**Local steps**

- Set role from (Platform.db.get\_single\_value(“Stock Reposting Settings”, “notify\_reposting\_error\_to\_role”) or “Stock Manager”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Stock Reposting Settings”, “notify\_reposting\_error\_to\_role”) → “Stock Manager”.
- Set recipients from get\_users\_with\_role(role).
- Return recipients.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “notify\_reposting\_error\_to\_role”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L5843) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L437)

<a id="op-960d673464461d"></a>
### Run parallel reposting

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_run_parallel_reposting`

**Inputs** no declared parameters.

**Record and data access** read “Stock Reposting Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”).
  - Return no value.
- If not in\_configured\_timeslot().
  - Return no value.
- Set no\_of\_parallel\_reposting from (Platform.db.get\_single\_value(“Stock Reposting Settings”, “no\_of\_parallel\_reposting”) or 4).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“Stock Reposting Settings”, “no\_of\_parallel\_reposting”) → 4.
- Set riv\_entries from get\_repost\_item\_valuation\_entries(limit = (no\_of\_parallel\_reposting × 100)).
- Set entries\_in\_progress from get\_entries\_with\_active\_jobs().
- Set items from get\_items\_with\_active\_reposting(entries\_in\_progress).
- For each row in riv\_entries.
  - If row.name belongs to entries\_in\_progress.
    - Continue with the next iteration or loop test.
  - If (row.based\_on differs from “Item and Warehouse” or row.repost\_only\_accounting\_ledgers).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.based\_on differs from “Item and Warehouse” → row.repost\_only\_accounting\_ledgers.
    - Evaluate execute\_reposting\_entry(row.name).
    - Continue with the next iteration or loop test.
  - If row.item\_code belongs to items.
    - Continue with the next iteration or loop test.
  - Evaluate items.add(row.item\_code).
  - If len(items) &gt; no\_of\_parallel\_reposting.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate enqueue\_reposting\_entry(row.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Stock Reposting Settings”, “enable\_parallel\_reposting”), Platform.db.get\_single\_value(“Stock Reposting Settings”, “no\_of\_parallel\_reposting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L5958) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L475)

<a id="op-c18e82077631e1"></a>
### Enqueue reposting entry

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_enqueue_reposting_entry`

**Inputs** name.

**State and service calls** enqueue with execute\_reposting\_entry.

**Local steps**

- Evaluate Platform.enqueue(execute\_reposting\_entry, name = name, continue\_reposting = true, queue = “long”, timeout = 1800, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(execute\_reposting\_entry, name = name, continue\_reposting = true, queue = “long”, timeout = 1800, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L6447) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L429)

<a id="op-99d06d3243c79d"></a>
### Enqueue parallel reposting

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_enqueue_parallel_reposting`

**Inputs** no declared parameters.

**State and service calls** enqueue with run\_parallel\_reposting.

**Local steps**

- Evaluate Platform.enqueue(run\_parallel\_reposting, queue = “long”, timeout = 1800, job\_id = “run\_parallel\_reposting”, deduplicate = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(run\_parallel\_reposting, queue = “long”, timeout = 1800, job\_id = “run\_parallel\_reposting”, deduplicate = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L6579) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L428)

<a id="op-f50d720ae167ab"></a>
### Get entries with active jobs

`operation_enterprise_stock_record_definitions_repost_item_valuation_business_behavior_get_entries_with_active_jobs`

**Inputs** no declared parameters.

**Declared result** set.

**Explicit results** set of job\_id at slice len(prefix) to no value for job\_id drawn from job\_ids where job\_id.startswith(prefix).

**Local steps**

- Bind dependencies get\_queue.
- Set queue from get\_queue(“long”).
- Set job\_ids from (list(queue.get\_job\_ids()) + list(queue.started\_job\_registry.get\_job\_ids())).
- Set prefix from formatted text {Platform.local.site}\|\|{REPOSTING\_JOB\_ID\_PREFIX}.
- Return set of job\_id at slice len(prefix) to no value for job\_id drawn from job\_ids where job\_id.startswith(prefix).
  - Draw job\_id from job\_ids, keep a combination only if (job\_id.startswith(prefix)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0800.json#L6662) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L434)
