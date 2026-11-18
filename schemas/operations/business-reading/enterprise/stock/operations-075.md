# Inventory and warehouses · operations 75

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Stock closing entry

[Record definition](../../../../data/record-types/stock_closing_entry.json)

<a id="op-1b4d0d97fed46f"></a>
### Stock Closing Entry.validate later closing entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_validate_later_closing_entry`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot cancel Stock Closing Entry {0} because the later Stock Closing Entry {1} is built on it. Cancel {1} first.”.format(self.name, get\_link\_to\_form(“Stock Closing Entry”, later\_entry)).

**Local steps**

- If later\_entry bound to self.get\_later\_closing\_entry().
  - Call the validation error handler Platform.throw(translated “Cannot cancel Stock Closing Entry {0} because the later Stock Closing Entry {1} is built on it. Cancel {1} first.”.format(self.name, get\_link\_to\_form(“Stock Closing Entry”, later ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get later closing entry](operations-075.md#op-9131fe81cfe20a).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L617)

<a id="op-f9cf8d3f5f9b14"></a>
### Stock Closing Entry.validate later closing entry for regenerate

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_validate_later_closing_entry_for_regenerate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot regenerate Stock Closing Entry {0} because the later Stock Closing Entry {1} is built on it. Cancel { …”.format(self.name, get\_link\_to\_form(“Stock Closing Entry”, later\_entry)).

**Local steps**

- If later\_entry bound to self.get\_later\_closing\_entry().
  - Call the validation error handler Platform.throw(translated “Cannot regenerate Stock Closing Entry {0} because the later Stock Closing Entry {1} is built on it. Cancel { …”.format(self.name, get\_link\_to\_form(“Stock Closing Entry”, later\_en ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get later closing entry](operations-075.md#op-9131fe81cfe20a).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L618)

<a id="op-9131fe81cfe20a"></a>
### Stock Closing Entry.get later closing entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_get_later_closing_entry`

**Inputs** self.

**Record and data access** read “Stock Closing Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Closing Entry”, mapping(“company” → self.company, “docstatus” → 1, “to\_date” → tuple(“&gt;”, self.to\_date), “name” → tuple(“!=”, self.name)), “name”, order\_by = “to\_date desc”).

**Local steps**

- Return Platform.db.get\_value(“Stock Closing Entry”, mapping(“company” → self.company, “docstatus” → 1, “to\_date” → tuple(“&gt;”, self.to\_date), “name” → tuple(“!=”, self.name)), “name”, order\_by = “to\_date desc”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L611)

<a id="op-a739ffc49ae5e2"></a>
### Stock Closing Entry.validate closed period lock

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_validate_closed_period_dependency_lock`

**Inputs** self.

**Record and data access** read “Period Closing Voucher” via get\_value.

**Explicit failure paths** validation helper — translated “Stock Closing Entry {0} belongs to a closed accounting period. Cancel the Period Closing Voucher {1} first.”.format(self.name, get\_link\_to\_form(“Period Closing Voucher”, pcv)).

**Local steps**

- Set pcv from Platform.db.get\_value(“Period Closing Voucher”, mapping(“company” → self.company, “docstatus” → 1, “period\_end\_date” → tuple(“&gt;=”, self.to\_date)), “name”).
- If pcv.
  - Call the validation error handler Platform.throw(translated “Stock Closing Entry {0} belongs to a closed accounting period. Cancel the Period Closing Voucher {1} first.”.format(self.name, get\_link\_to\_form(“Period Closing Voucher”, pcv)), t ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0822.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L740)

<a id="op-2e687c2e39ccbc"></a>
### Stock Closing Entry.validate submitted

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_validate_submitted`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Stock Closing Entry {0} must be submitted to generate the closing balance”.format(self.name).

**Local steps**

- <a id="op-2e687c2e39ccbc-guard-2"></a>If self.docstatus differs from 1.
  - Call the validation error handler Platform.throw(translated “Stock Closing Entry {0} must be submitted to generate the closing balance”.format(self.name)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus differs from 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Stock Closing Entry {0} must be submitted to generate the closing balance”.format(self.name). With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2e687c2e39ccbc-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L620)

<a id="op-78153e5d72d871"></a>
### Stock Closing Entry.validate no pending reposts

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_validate_no_pending_reposts`

**Inputs** self.

**Explicit failure paths** validation helper with PendingRepostingError — self.get\_pending\_reposts\_message().

**Local steps**

- Bind dependencies PendingRepostingError.
- If self.has\_pending\_reposts().
  - Call the validation error handler Platform.throw(self.get\_pending\_reposts\_message(), PendingRepostingError, title = translated “Stock Reposting Ongoing”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has pending reposts](operations-075.md#op-dfbe6572119924), [get pending reposts message](operations-075.md#op-86489a0616bfc1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L619)

<a id="op-dfbe6572119924"></a>
### Stock Closing Entry.has pending reposts

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_has_pending_reposts`

**Inputs** self.

**Explicit results** check\_pending\_reposting(self.to\_date, self.company, throw\_error = false).

**Local steps**

- Bind dependencies check\_pending\_reposting.
- Return check\_pending\_reposting(self.to\_date, self.company, throw\_error = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L614)

<a id="op-1aebd0766e6144"></a>
### Stock Closing Entry.has ledger changes since

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_has_ledger_changes_since`

**Inputs** self, started\_at.

**Explicit results** bool(nested operand in the contract.limit(1).for\_update().run()).

**Local steps**

- Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
- Return bool(nested operand in the contract.limit(1).for\_update().run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L613)

<a id="op-9be7c06469d9f7"></a>
### Stock Closing Entry.has pending reposts now

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_has_pending_reposts_now`

**Inputs** self.

**Explicit results** bool(nested operand in the contract.limit(1).for\_update().run()).

**Local steps**

- Set riv from Platform.qb.DocType(“Repost Item Valuation”).
- Return bool(nested operand in the contract.limit(1).for\_update().run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L615)

<a id="op-86489a0616bfc1"></a>
### Stock Closing Entry.get pending reposts message

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosingentry_get_pending_reposts_message`

**Inputs** self.

**Explicit results** translated “Cannot generate the closing balance of Stock Closing Entry {0} while Repost Item Valuation entries dated on  …”.format(self.name, Platform.bold(Platform.format(self.to\_date, “Date”))).

**Local steps**

- Return translated “Cannot generate the closing balance of Stock Closing Entry {0} while Repost Item Valuation entries dated on  …”.format(self.name, Platform.bold(Platform.format(self.to\_date, “Date”))).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L612)

<a id="op-eb12d28d6dffbf"></a>
### Stock Closing Entry.remove stock closing

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_remove_stock_closing`

**Inputs** self.

**Local steps**

- Set table from Platform.qb.DocType(“Stock Closing Balance”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(table.stock\_closing\_entry equals self.name).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0822.json#L277) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L737)

<a id="op-fba9c1d9fb1469"></a>
### Stock Closing Entry.enqueue job

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_enqueue_job`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_set on self · msgprint with translated “Stock Closing Entry {0} has been queued for processing, system will take sometime to complete it.”.format(self.name).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.validate\_submitted().
- Evaluate self.validate\_no\_pending\_reposts().
- Evaluate self.db\_set(“status”, “In Progress”).
- Evaluate enqueue(prepare\_closing\_stock\_balance, name = self.name, queue = “long”, timeout = 1500, enqueue\_after\_commit = true).
- Evaluate Platform.msgprint(translated “Stock Closing Entry {0} has been queued for processing, system will take sometime to complete it.”.format(self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate submitted](operations-075.md#op-2e687c2e39ccbc), [validate no pending reposts](operations-075.md#op-78153e5d72d871).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · service or queued work from enqueue(prepare\_closing\_stock\_balance, name = self.name, queue = “long”, timeout = 1500, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L731)

<a id="op-9eaadd4f3b5fd1"></a>
### Stock Closing Entry.regenerate closing balance

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_regenerate_closing_balance`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Evaluate self.validate\_submitted().
- Evaluate self.validate\_closed\_period\_lock().
- Evaluate self.validate\_later\_closing\_entry\_for\_regenerate().
- Evaluate self.remove\_stock\_closing().
- Evaluate self.enqueue\_job().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate submitted](operations-075.md#op-2e687c2e39ccbc), [validate closed period lock](operations-075.md#op-a739ffc49ae5e2), [validate later closing entry for regenerate](operations-075.md#op-f9cf8d3f5f9b14), [remove stock closing](operations-075.md#op-eb12d28d6dffbf), [enqueue job](operations-075.md#op-fba9c1d9fb1469).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L736)

<a id="op-bc340280d29e1d"></a>
### Stock Closing Entry.create stock closing balance entries

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_create_stock_closing_balance_entries`

**Inputs** self.

**State and service calls** request new\_doc for “Stock Closing Balance” · call save on new\_doc.

**Local steps**

- Bind dependencies get\_combine\_datetime.
- Set stk\_cl\_obj from StockClosing(self.company, self.from\_date, self.to\_date).
- Set entries from stk\_cl\_obj.get\_stock\_closing\_entries().
- For each key in entries.
  - Set row from entries at key.
  - If (row.actual\_qty equals 0.0 and row.stock\_value\_difference equals 0.0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.actual\_qty equals 0.0 → row.stock\_value\_difference equals 0.0.
    - Continue with the next iteration or loop test.
  - If row.fifo\_queue is distinct from no value.
    - Set row.fifo\_queue from json.dumps(row.fifo\_queue).
  - Evaluate set\_stock\_value\_and\_valuation\_rate(row).
  - Set new\_doc from Platform.new\_doc(“Stock Closing Balance”).
  - Evaluate new\_doc.update(row).
  - Set new\_doc.posting\_date from self.to\_date.
  - Set new\_doc.posting\_time from nowtime().
  - Set new\_doc.posting\_datetime from get\_combine\_datetime(self.to\_date, new\_doc.posting\_time).
  - Set new\_doc.stock\_closing\_entry from self.name.
  - Set new\_doc.company from self.company.
  - Evaluate new\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L730)

<a id="op-ae4d606753b85a"></a>
### Stock Closing Entry.get prepared data

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_entry_get_prepared_data`

**Inputs** self.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** parse\_json(data) · Platform.\_dict(mapping()).

**Local steps**

- If attachments bound to get\_attachments(self.doctype, self.name).
  - Set attachment from attachments at 0.
  - Set attached\_file from Platform.get\_doc(“File”, attachment.name).
  - Set data from gzip.decompress(attached\_file.get\_content()).
  - If data bound to json.loads(data.decode(“utf-8”)).
    - Set data from data.
  - Return parse\_json(data).
- Return Platform.\_dict(mapping()).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L732)

<a id="op-8fcaf6d7890f31"></a>
### Set stock value and valuation rate

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_set_stock_value_and_valuation_rate`

**Inputs** row.

**Local steps**

- Set row.stock\_value from flt(row.stock\_value\_difference).
- Set row.valuation\_rate from flt((row.stock\_value ÷ row.actual\_qty)) when row.actual\_qty, otherwise 0.0.
  - Value choice on row.actual\_qty — true gives flt((row.stock\_value ÷ row.actual\_qty)), false gives 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L607)

<a id="op-2522980e0bc0c5"></a>
### Prepare closing stock balance

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_prepare_closing_stock_balance`

**Inputs** name.

**Record and data access** resolve a document from “Stock Closing Entry” via get\_doc.

**State and service calls** call db\_set on doc.

**Explicit results** no value.

**Local steps**

- If not is\_submitted\_closing\_entry(name).
  - Return no value.
- Set doc from Platform.get\_doc(“Stock Closing Entry”, name).
- If doc.has\_pending\_reposts().
  - Evaluate doc.db\_set(“status”, “Failed”).
  - Evaluate doc.log\_error(title = translated “Stock Closing Entry Failed”, message = doc.get\_pending\_reposts\_message()).
  - Return no value.
- Evaluate doc.db\_set(“status”, “In Progress”).
- Set started\_at from now\_datetime().
- Attempt the following.
  - Evaluate doc.create\_stock\_closing\_balance\_entries().
  - If not is\_submitted\_closing\_entry(name, for\_update = true).
    - Evaluate doc.remove\_stock\_closing().
    - Evaluate doc.db\_set(“status”, “Cancelled”).
    - Return no value.
  - Evaluate lock\_company\_for\_closing(doc.company).
  - Set is\_outdated from (doc.has\_ledger\_changes\_since(started\_at) or doc.has\_pending\_reposts\_now()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.has\_ledger\_changes\_since(started\_at) → doc.has\_pending\_reposts\_now().
  - Evaluate doc.db\_set(“status”, “Outdated” when is\_outdated, otherwise “Completed”).
    - Value choice on is\_outdated — true gives “Outdated”, false gives “Completed”.
- On failure (Exception).
  - Evaluate doc.db\_set(“status”, “Failed”).
  - Evaluate doc.log\_error(title = “Stock Closing Entry Failed”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0038.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L728)

<a id="op-a93aeccf852cf4"></a>
### Is submitted closing entry

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_is_submitted_closing_entry`

**Inputs** name, for\_update = false.

**Record and data access** read “Stock Closing Entry” via get\_value.

**Explicit results** Platform.db.get\_value(“Stock Closing Entry”, name, “docstatus”, for\_update = for\_update) equals 1.

**Local steps**

- Return Platform.db.get\_value(“Stock Closing Entry”, name, “docstatus”, for\_update = for\_update) equals 1.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L604)

<a id="op-0ebe1c2e5ac4ba"></a>
### Stock Closing.initialize

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_initialize`

**Inputs** self, company, from\_date, to\_date, remaining named values kwargs.

**Local steps**

- Set self.company from company.
- Set self.from\_date from from\_date.
- Set self.to\_date from to\_date.
- Set self.kwargs from kwargs.
- Set self.inv\_dimensions from get\_inventory\_dimensions().
- Set self.last\_closing\_balance from self.get\_last\_stock\_closing\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get last stock closing entry](operations-076.md#op-0b6a09b16a72b8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0822.json#L1838) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L749)

<a id="op-cf93f96e4fbd31"></a>
### Stock Closing.get stock closing entries

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_stock_closing_entries`

**Inputs** self.

**Explicit results** closing\_stock.

**Local steps**

- Set sl\_entries from self.get\_sle\_entries().
- Set closing\_stock from Platform.\_dict().
- Set counted\_sles from set().
- For each row in sl\_entries.
  - Set dimensions\_keys from self.get\_keys(row).
  - For each dimension\_key in dimensions\_keys.
    - For each tuple(dimension\_fields, dimension\_values) in dimension\_key.items().
      - Set key from dimension\_values.
      - Set value\_difference from self.get\_value\_difference(row, dimension\_fields, key, counted\_sles).
      - If key belongs to closing\_stock.
        - Set actual\_qty from row.sabb\_qty when row.sabb\_qty is distinct from no value, otherwise row.actual\_qty.
          - Value choice on row.sabb\_qty is distinct from no value — true gives row.sabb\_qty, false gives row.actual\_qty.
        - Update closing\_stock at key.actual\_qty using + actual\_qty.
        - Update closing\_stock at key.stock\_value\_difference using + value\_difference.
        - If (row.sabb\_qty is identical to no value and not row.actual\_qty and row.qty\_after\_transaction is distinct from no value).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.sabb\_qty is identical to no value → not row.actual\_qty → row.qty\_after\_transaction is distinct from no value.
          - Set closing\_stock at key.actual\_qty from row.qty\_after\_transaction.
        - Set fifo\_queue from closing\_stock at key.fifo\_queue.
        - If fifo\_queue is distinct from no value.
          - Evaluate self.update\_fifo\_queue(fifo\_queue, actual\_qty, row.posting\_date).
          - Set closing\_stock at key.fifo\_queue from fifo\_queue.
      - Otherwise.
        - Set entries from self.get\_initialized\_entry(row, dimension\_fields, value\_difference).
        - Set closing\_stock at key from entries.
- Return closing\_stock.

**Methods declared on this owner** [get sle entries](operations-076.md#op-c59a1bf9ce692a), [get keys](operations-076.md#op-371eaec529bac8), [get value difference](operations-075.md#op-e638b619943600), [update fifo queue](operations-075.md#op-6eddd829e110c2), [get initialized entry](operations-075.md#op-aa21550a038f35).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L747)

<a id="op-e638b619943600"></a>
### Stock Closing.get value difference

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosing_get_value_difference`

**Inputs** self, row, dimension\_fields, key, counted\_sles.

**Explicit results** flt(row.sabb\_stock\_value\_difference) · flt(row.stock\_value\_difference) · 0.0.

**Local steps**

- If dimension\_fields differs from tuple(“item\_code”, “warehouse”).
  - If row.sabb\_stock\_value\_difference is distinct from no value.
    - Return flt(row.sabb\_stock\_value\_difference).
  - Return flt(row.stock\_value\_difference).
- If row.name.
  - If tuple(key, row.name) belongs to counted\_sles.
    - Return 0.0.
  - Evaluate counted\_sles.add(tuple(key, row.name)).
- Return flt(row.stock\_value\_difference).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L609)

<a id="op-6eddd829e110c2"></a>
### Stock Closing.update fifo queue

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_update_first_in_first_out_queue`

**Inputs** self, fifo\_queue, actual\_qty, posting\_date.

**Explicit results** no value.

**Local steps**

- If actual\_qty &gt; 0.
  - Evaluate fifo\_queue.append(list(actual\_qty, get\_date\_str(posting\_date))).
  - Return no value.
- Set qty\_to\_consume from abs(actual\_qty).
- While (qty\_to\_consume &gt; 0 and fifo\_queue).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in qty\_to\_consume &gt; 0 → fifo\_queue.
  - If fifo\_queue at 0 at 0 &gt; qty\_to\_consume.
    - Update fifo\_queue at 0 at 0 using − qty\_to\_consume.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Update qty\_to\_consume using − fifo\_queue at 0 at 0.
  - Evaluate fifo\_queue.pop(0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L750)

<a id="op-2e82ec7008e229"></a>
### Stock Closing.get initial fifo queue

`operation_enterprise_binding_enterprise_stock_doctype_stock_closing_entry_stock_closing_entry_stockclosing_get_initial_fifo_queue`

**Inputs** self, row, actual\_qty, has\_serial\_no.

**Explicit results** no value · fifo\_queue · list(list(actual\_qty, get\_date\_str(row.posting\_date))) when actual\_qty, otherwise list().

**Local steps**

- If has\_serial\_no.
  - Return no value.
- If (row.from\_closing\_balance and row.fifo\_queue).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.from\_closing\_balance → row.fifo\_queue.
  - Set fifo\_queue from json.loads(row.fifo\_queue).
  - If not flt((sum(generator of slot at 0 for slot drawn from fifo\_queue) − actual\_qty), 6).
    - Draw slot from fifo\_queue.
    - Return fifo\_queue.
- Return list(list(actual\_qty, get\_date\_str(row.posting\_date))) when actual\_qty, otherwise list().
  - Value choice on actual\_qty — true gives list(list(actual\_qty, get\_date\_str(row.posting\_date))), false gives list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0022.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L608)

<a id="op-aa21550a038f35"></a>
### Stock Closing.get initialized entry

`operation_enterprise_stock_record_definitions_stock_closing_entry_business_behavior_stock_closing_get_initialized_entry`

**Inputs** self, row, dimension\_fields, value\_difference.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** entry.

**Local steps**

- Set item\_details from Platform.get\_cached\_value(“Item”, row.item\_code, list(“item\_group”, “item\_name”, “stock\_uom”, “has\_serial\_no”), as\_dict = 1).
- Set inventory\_dimension\_key from no value.
- If dimension\_fields does not belong to list(tuple(“item\_code”, “warehouse”), tuple(“item\_code”, “warehouse”, “batch\_no”)).
  - Set inventory\_dimension\_key from json.dumps(dimension\_fields).
- Set actual\_qty from flt(row.sabb\_qty when row.sabb\_qty is distinct from no value, otherwise (row.actual\_qty or row.qty\_after\_transaction)).
  - Value choice on row.sabb\_qty is distinct from no value — true gives row.sabb\_qty, false gives (row.actual\_qty or row.qty\_after\_transaction).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.actual\_qty → row.qty\_after\_transaction.
- Set entry from Platform.\_dict(mapping(“item\_code” → row.item\_code, “warehouse” → row.warehouse, “actual\_qty” → actual\_qty, “stock\_value\_difference” → value\_difference, …)).
- If row.sabb\_batch\_no.
  - Set row.batch\_no from row.sabb\_batch\_no.
- For each field in dimension\_fields.
  - If row.get(field).
    - Set entry at field from row.get(field).
- Return entry.

**Methods declared on this owner** [get initial fifo queue](operations-075.md#op-2e82ec7008e229).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, row.item\_code, list(“item\_group”, “item\_name”, “stock\_uom”, “has\_serial\_no”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0039.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-010.tsv#L1133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-011.tsv#L743)
