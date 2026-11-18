# Accounting and settlement · operations 60

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Notification for new fiscal year

<a id="op-6bbcf8dd197899"></a>
### Get context

`operation_enterprise_accounts_notification_notification_for_new_fiscal_year_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0211.json#L5008) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L50)

## Record · Opening invoice creation tool

[Record definition](../../../../data/record-types/opening_invoice_creation_tool.json)

<a id="op-4f56a6905cf1de"></a>
### Opening Invoice Creation Tool.onload

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_onload`

**Inputs** self.

**Local steps**

- Set tuple(summary, max\_count) from self.get\_opening\_invoice\_summary().
- Evaluate self.set\_onload(“opening\_invoices\_summary”, summary).
- Evaluate self.set\_onload(“max\_count”, max\_count).
- Evaluate self.set\_onload(“temporary\_opening\_account”, get\_temporary\_opening\_account(self.company)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get opening invoice summary](operations-060.md#op-ff536e485f1909).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L4646) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1255)

<a id="op-ff536e485f1909"></a>
### Opening Invoice Creation Tool.get opening invoice summary

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_get_opening_invoice_summary`

**Inputs** self.

**Record and data access** read “Company” via get\_list.

**Explicit results** tuple(no value, no value) · tuple(invoices\_summary, max\_count).

**Local steps**

- Bind local operation prepare\_invoice\_summary for subsequent calls.
- Set invoices\_summary from mapping().
- Set max\_count from mapping().
- Set companies from Platform.get\_list(“Company”, fields = list(“name as company”, “default\_currency as currency”)).
- If not companies.
  - Return tuple(no value, no value).
- Set company\_wise\_currency from mapping of row.company → row.currency for row drawn from companies.
  - Draw row from companies.
- For each doctype in list(“Sales Invoice”, “Purchase Invoice”).
  - Set invoice from Platform.qb.DocType(doctype).
  - Set company from Platform.qb.DocType(“Company”).
  - Set outstanding from Case().when(invoice.party\_account\_currency equals company.default\_currency, invoice.outstanding\_amount).else\_((invoice.outstanding\_amount × invoice.conversion\_rate)).
  - Set invoices from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
  - Evaluate prepare\_invoice\_summary(doctype, invoices).
- Set invoices\_summary\_companies from list(invoices\_summary.keys()).
- For each company in invoices\_summary\_companies.
  - Set invoices\_summary at escape\_html(company) from invoices\_summary.pop(company).
- Return tuple(invoices\_summary, max\_count).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1252)

<a id="op-0bf3c48cbc686d"></a>
### Opening Invoice Creation Tool.get opening invoice summary.prepare invoice summary

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_get_opening_invoice_summary_prepare_invoice_summary`

**Inputs** doctype, invoices.

**Local steps**

- Set paid\_amount from list().
- Set outstanding\_amount from list().
- For each invoice in invoices.
  - Set company from invoice.pop(“company”).
  - Set \_summary from invoices\_summary.get(company, mapping()).
  - Evaluate \_summary.update(mapping(“currency” → company\_wise\_currency.get(company), doctype → invoice)).
  - Evaluate invoices\_summary.update(mapping(company → \_summary)).
  - If invoice.paid\_amount.
    - Evaluate paid\_amount.append(invoice.paid\_amount).
  - If invoice.outstanding\_amount.
    - Evaluate outstanding\_amount.append(invoice.outstanding\_amount).
- If (paid\_amount or outstanding\_amount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in paid\_amount → outstanding\_amount.
  - Evaluate max\_count.update(mapping(doctype → mapping(“max\_paid” → max(paid\_amount) when paid\_amount, otherwise 0.0, “max\_due” → max(outstanding\_amount) when outstanding\_amount, otherwise 0.0))).
    - Value choice on paid\_amount — true gives max(paid\_amount), false gives 0.0.
    - Value choice on outstanding\_amount — true gives max(outstanding\_amount), false gives 0.0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L5790) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1253)

<a id="op-2fe8a6c7601cc9"></a>
### Opening Invoice Creation Tool.validate company

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_validate_company`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select the Company”.

**Local steps**

- If not self.company.
  - Call the validation error handler Platform.throw(translated “Please select the Company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0072.json#L6243) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1257)

<a id="op-0a089f68288351"></a>
### Opening Invoice Creation Tool.set missing values

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_set_missing_values`

**Inputs** self, row.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Quantity must be a positive number”.format(row.idx).

**Local steps**

- Set row.qty from 1.0 when row.qty belongs to tuple(no value, empty text), otherwise flt(row.qty).
  - Value choice on row.qty belongs to tuple(no value, empty text) — true gives 1.0, false gives flt(row.qty).
- If (not isfinite(row.qty) or row.qty ≤ 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isfinite(row.qty) → row.qty ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Quantity must be a positive number”.format(row.idx)).
- Set row.currency from (row.currency or Platform.get\_cached\_value(“Company”, self.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.currency → Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
- Set row.temporary\_opening\_account from (row.temporary\_opening\_account or get\_temporary\_opening\_account(self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.temporary\_opening\_account → get\_temporary\_opening\_account(self.company).
- Set row.party\_type from “Customer” when self.invoice\_type equals “Sales”, otherwise “Supplier”.
  - Value choice on self.invoice\_type equals “Sales” — true gives “Customer”, false gives “Supplier”.
- Set row.item\_name from (row.item\_name or translated “Opening Invoice Item”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.item\_name → translated “Opening Invoice Item”.
- Set row.posting\_date from (row.posting\_date or nowdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.posting\_date → nowdate().
- Set row.due\_date from (row.due\_date or nowdate()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.due\_date → nowdate().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”) · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1256)

<a id="op-c4090fb2c4edb2"></a>
### Opening Invoice Creation Tool.validate mandatory invoice fields

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_validate_mandatory_invoice_fields`

**Inputs** self, row.

**Record and data access** read row.party\_type via exists.

**Explicit failure paths** validation helper — translated “Row #{}: Either Party ID or Party Name is required”.format(row.idx) · validation helper — translated “Row #{}: Party ID is required”.format(row.idx) · validation helper — translated “Row #{}: {} {} does not exist.”.format(row.idx, Platform.bold(row.party\_type), Platform.bold(row.party)) · validation helper — mandatory\_error\_msg.format(row.idx, d, self.invoice\_type).

**Local steps**

- If self.create\_missing\_party.
  - If (not row.party and not row.party\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.party → not row.party\_name.
    - Call the validation error handler Platform.throw(translated “Row #{}: Either Party ID or Party Name is required”.format(row.idx)).
  - If (not row.party and row.party\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.party → row.party\_name.
    - Set row.party from self.add\_party(row.party\_type, row.party\_name).
  - If (row.party and not Platform.db.exists(row.party\_type, row.party)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.party → not Platform.db.exists(row.party\_type, row.party).
    - Set row.party from self.add\_party(row.party\_type, row.party).
- Otherwise.
  - If not row.party.
    - Call the validation error handler Platform.throw(translated “Row #{}: Party ID is required”.format(row.idx)).
  - If not Platform.db.exists(row.party\_type, row.party).
    - Call the validation error handler Platform.throw(translated “Row #{}: {} {} does not exist.”.format(row.idx, Platform.bold(row.party\_type), Platform.bold(row.party))).
- Set mandatory\_error\_msg from translated “Row #{0}: {1} is required to create the Opening {2} Invoices”.
- For each d in tuple(“Outstanding Amount”, “Temporary Opening Account”).
  - If not row.get(scrub(d)).
    - Call the validation error handler Platform.throw(mandatory\_error\_msg.format(row.idx, d, self.invoice\_type)).
- Evaluate self.validate\_temporary\_opening\_account(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add party](operations-060.md#op-0481ef33cae874), [validate temporary opening account](operations-060.md#op-4da3192a62a5fb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1258)

<a id="op-4da3192a62a5fb"></a>
### Opening Invoice Creation Tool.validate temporary opening account

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_validate_temporary_opening_account`

**Inputs** self, row.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: {1} account is not of type {2}”.format(row.idx, row.temporary\_opening\_account, “Temporary”).

**Local steps**

- Set account\_type from Platform.get\_cached\_value(“Account”, row.temporary\_opening\_account, “account\_type”).
- If account\_type differs from “Temporary”.
  - Call the validation error handler Platform.throw(translated “Row #{0}: {1} account is not of type {2}”.format(row.idx, row.temporary\_opening\_account, “Temporary”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, row.temporary\_opening\_account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0073.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1259)

<a id="op-a01aa61e4d06b2"></a>
### Opening Invoice Creation Tool.get invoices

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_get_invoices`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** invoices.

**Local steps**

- Set invoices from list().
- For each row in self.invoices.
  - If not row.
    - Continue with the next iteration or loop test.
  - Evaluate self.set\_missing\_values(row).
  - Evaluate self.validate\_mandatory\_invoice\_fields(row).
  - Set invoice from self.get\_invoice\_dict(row).
  - Set company\_details from (Platform.get\_cached\_value(“Company”, self.company, list(“default\_currency”, “default\_letter\_head”), as\_dict = 1) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Company”, self.company, list(“default\_currency”, “default\_letter\_head”), as\_dict = 1) → mapping().
  - If company\_details.
    - Evaluate invoice.update(mapping(“currency” → row.currency, “letter\_head” → company\_details.get(“default\_letter\_head”))).
  - Evaluate invoices.append(invoice).
- Return invoices.

**Methods declared on this owner** [set missing values](operations-060.md#op-0a089f68288351), [validate mandatory invoice fields](operations-060.md#op-c4090fb2c4edb2), [get invoice dict](operations-060.md#op-db00c23fa2aac9).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, list(“default\_currency”, “default\_letter\_head”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1251)

<a id="op-0481ef33cae874"></a>
### Opening Invoice Creation Tool.add party

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_add_party`

**Inputs** self, party\_type, party.

**Record and data access** read party\_type via get\_list · read “Buying Settings” via get\_single\_value.

**State and service calls** request new\_doc for party\_type · call save on party\_doc.

**Explicit results** parties at 0 · party\_doc.name.

**Explicit failure paths** validation helper — translated “Multiple {0} records match {1}. Please select the Party ID.”.format(party\_type, Platform.bold(party)) · validation helper — translated “Please Set Supplier Group in Buying Settings.”.

**Local steps**

- Set parties from Platform.get\_list(party\_type, filters = mapping((scrub(party\_type) + “\_name”) → party), pluck = “name”, limit\_page\_length = 2).
- <a id="op-0481ef33cae874-guard-5"></a>If len(parties) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Multiple {0} records match {1}. Please select the Party ID.”.format(party\_type, Platform.bold(party))).
- If parties.
  - Return parties at 0.
- Set party\_doc from Platform.new\_doc(party\_type).
- If party\_type equals “Customer”.
  - Set party\_doc.customer\_name from party.
- Otherwise.
  - Set supplier\_group from Platform.db.get\_single\_value(“Buying Settings”, “supplier\_group”).
  - If not supplier\_group.
    - Call the validation error handler Platform.throw(translated “Please Set Supplier Group in Buying Settings.”).
  - Set party\_doc.supplier\_name from party.
  - Set party\_doc.supplier\_group from supplier\_group.
- Set party\_doc.flags.ignore\_mandatory from true.
- Evaluate party\_doc.save().
- Return party\_doc.name.

**Derived branch illustrations**

- At the comparison len(parties) &gt; 1, length of parties = 2 selects the branch that calls the validation-error handler with translated “Multiple {0} records match {1}. Please select the Party ID.”.format(party\_type, Platform.bold(party)). With length of parties = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-0481ef33cae874-guard-5)

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “supplier\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1248)

<a id="op-db00c23fa2aac9"></a>
### Opening Invoice Creation Tool.get invoice dict

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_get_invoice_mapping`

**Inputs** self, row = no value.

**Explicit results** invoice.

**Local steps**

- Bind local operation get\_item\_dict for subsequent calls.
- Set item from get\_item\_dict().
- Set invoice from Platform.\_dict(mapping(“items” → list(item), “is\_opening” → “Yes”, “set\_posting\_time” → 1, “company” → self.company, …)).
  - Value choice on self.invoice\_type equals “Sales” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
- If (self.invoice\_type equals “Purchase” and row.supplier\_invoice\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoice\_type equals “Purchase” → row.supplier\_invoice\_date.
  - Evaluate invoice.update(mapping(“bill\_date” → row.supplier\_invoice\_date)).
- Set accounting\_dimension from get\_accounting\_dimensions().
- For each dimension in accounting\_dimension.
  - Evaluate invoice.update(mapping(dimension → (self.get(dimension) or item.get(dimension)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(dimension) → item.get(dimension).
- Return invoice.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1249)

<a id="op-c512ba225ee05f"></a>
### Opening Invoice Creation Tool.get invoice dict.get item dict

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_get_invoice_mapping_get_item_mapping`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** item\_dict.

**Explicit failure paths** validation helper — translated “Please set the Default Cost Center in {0} company.”.format(Platform.bold(self.company)).

**Local steps**

- Set cost\_center from (row.get(“cost\_center”) or Platform.get\_cached\_value(“Company”, self.company, “cost\_center”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“cost\_center”) → Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).
- If not cost\_center.
  - Call the validation error handler Platform.throw(translated “Please set the Default Cost Center in {0} company.”.format(Platform.bold(self.company))).
- Set income\_expense\_account\_field from “income\_account” when row.party\_type equals “Customer”, otherwise “expense\_account”.
  - Value choice on row.party\_type equals “Customer” — true gives “income\_account”, false gives “expense\_account”.
- Set default\_uom from get\_default\_stock\_uom().
- Set qty from row.qty.
- Set description from (row.item\_name or translated “Opening Invoice Item”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.item\_name → translated “Opening Invoice Item”.
- Set item\_meta from Platform.get\_meta(formatted text {self.invoice\_type} Invoice Item).
- Set qty\_precision from get\_field\_precision(item\_meta.get\_field(“qty”)).
- Set rate\_precision from get\_field\_precision(item\_meta.get\_field(“rate”), currency = row.currency).
- Set amount\_precision from get\_field\_precision(item\_meta.get\_field(“amount”), currency = row.currency).
- Set amount from flt(row.outstanding\_amount, amount\_precision).
- Set rate from flt((amount ÷ qty), rate\_precision).
- If (flt(qty, qty\_precision) differs from qty or flt((rate × qty), amount\_precision) differs from amount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(qty, qty\_precision) differs from qty → flt((rate × qty), amount\_precision) differs from amount.
  - Update description using + (text in the contract + translated “Original Quantity: {0}”.format(qty)).
  - Set tuple(qty, rate) from tuple(1, amount).
- Set item\_dict from Platform.\_dict(mapping(“uom” → default\_uom, “rate” → (rate or 0.0), “qty” → qty, “conversion\_factor” → 1.0, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rate → 0.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.item\_name → “Opening Invoice Item”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“project”) → self.get(“project”).
- For each dimension in get\_accounting\_dimensions().
  - Evaluate item\_dict.update(mapping(dimension → row.get(dimension))).
- Return item\_dict.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1250)

<a id="op-d1294827caf68c"></a>
### Opening Invoice Creation Tool.make invoices

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_opening_invoice_creation_tool_make_invoices`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** start\_import(invoices).

**Explicit failure paths** validation helper — translated “Scheduler is inactive. Cannot import data.”.

**Local steps**

- Evaluate self.validate\_company().
- Set invoices from self.get\_invoices().
- If len(invoices) &lt; 50.
  - Return start\_import(invoices).
- Otherwise.
  - Bind dependencies is\_scheduler\_inactive.
  - If (is\_scheduler\_inactive() and not Platform.in\_test).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_scheduler\_inactive() → not Platform.in\_test.
    - Call the validation error handler Platform.throw(translated “Scheduler is inactive. Cannot import data.”, title = translated “Scheduler Inactive”).
  - Set job\_id from formatted text opening\_invoice::{self.name}.
  - If not is\_job\_enqueued(job\_id).
    - Evaluate enqueue(start\_import, queue = “default”, timeout = 6000, event = “opening\_invoice\_creation”, job\_id = job\_id, …).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.developer\_mode → Platform.in\_test.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate company](operations-060.md#op-2fe8a6c7601cc9), [get invoices](operations-060.md#op-a01aa61e4d06b2).

**Values supplied outside this operation** service or queued work from enqueue(start\_import, queue = “default”, timeout = 6000, event = “opening\_invoice\_creation”, job\_id = job\_id, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1254)

<a id="op-6c3929a3ae208e"></a>
### Start import

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_start_import`

**Inputs** invoices.

**Record and data access** resolve a document from d via get\_doc.

**State and service calls** savepoint savepoint · call insert on doc · call submit on doc · commit · rollback · 1 additional forms in the steps below.

**Explicit results** names.

**Local steps**

- Set errors from 0.
- Set names from list().
- Set total from len(invoices).
- For each tuple(idx, d) in enumerate(invoices).
  - Set savepoint from formatted text opening\_invoice\_{Platform.generate\_hash(length = 8)}.
  - Evaluate Platform.db.savepoint(savepoint).
  - Set is\_last from idx equals (total − 1).
  - Attempt the following.
    - Set invoice\_number from no value.
    - If d.invoice\_number.
      - Set invoice\_number from d.invoice\_number.
    - Set doc from Platform.get\_doc(d).
    - Set doc.flags.ignore\_mandatory from true.
    - Set doc.flags.dont\_auto\_add\_taxes from true.
    - Evaluate doc.insert(set\_name = invoice\_number).
    - Evaluate doc.submit().
    - If not Platform.in\_test.
      - Evaluate Platform.db.commit().
    - Evaluate names.append(doc.name).
    - Evaluate publish(idx, total, d.doctype, errors = errors when is\_last, otherwise no value).
      - Value choice on is\_last — true gives errors, false gives no value.
  - On failure (Exception).
    - Update errors using + 1.
    - Evaluate Platform.db.rollback().
    - Evaluate doc.log\_error(“Opening invoice creation failed”).
    - Evaluate publish(idx, total, d.doctype, errors = errors when is\_last, otherwise no value).
      - Value choice on is\_last — true gives errors, false gives no value.
- If errors.
  - Evaluate Platform.msgprint(translated “You had {} errors while creating opening invoices. Check {} for more details”.format(errors, text in the contract), indicator = “red”, title = translated “Error Occurred”).
- Return names.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 8).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L2)

<a id="op-ba3879807ab52d"></a>
### Publish

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_publish`

**Inputs** index, total, doctype, errors = no value.

**State and service calls** publish realtime with “opening\_invoice\_creation\_progress”.

**Local steps**

- Evaluate Platform.publish\_realtime(“opening\_invoice\_creation\_progress”, dict(title = translated “Opening Invoice Creation In Progress”, message = translated “Creating {} out of {} {}”.format((index + 1), total, doc ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“opening\_invoice\_creation\_progress”, dict(title = translated “Opening Invoice Creation In Progress”, message = translated “Creating {} out of {} {}”.format((index + 1), total, doc ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0073.json#L4092) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1260)

<a id="op-a990c36c3aa9fd"></a>
### Get temporary opening account

`operation_enterprise_accounts_record_definitions_opening_invoice_creation_tool_business_behavior_get_temporary_opening_account`

**Inputs** company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_all.

**Explicit results** no value · accounts at 0.name.

**Explicit failure paths** validation helper — translated “Please add a Temporary Opening account in Chart of Accounts”.

**Local steps**

- If not company.
  - Return no value.
- Evaluate Platform.has\_permission(“Company”, “read”, company, throw = true).
- Set accounts from Platform.get\_all(“Account”, filters = mapping(“company” → company, “account\_type” → “Temporary”)).
- If not accounts.
  - Call the validation error handler Platform.throw(translated “Please add a Temporary Opening account in Chart of Accounts”).
- Return accounts at 0.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, company, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1247)

## Service · Order billing as on

<a id="op-9b7b1527f6220b"></a>
### Order Billing As On.initialize

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_init`

**Inputs** self, doctype, links, as\_on\_date, precision.

**Local steps**

- Set self.doctype from doctype.
- Set self.links from links.
- Set self.as\_on\_date from as\_on\_date.
- Set self.precision from precision.
- Set self.invoice from Platform.qb.DocType(links.invoice).
- Set self.invoice\_item from Platform.qb.DocType((links.invoice + “ Item”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L176) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1241)

<a id="op-9661b670d42692"></a>
### Order Billing As On.get billed later

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_billed_later`

**Inputs** self.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping() · billed\_later.

**Local steps**

- Set order\_lines from self.get\_order\_lines\_billed\_after().
- If not order\_lines.
  - Return mapping().
- Set billed\_against\_lines from self.get\_billed\_against\_order\_lines(order\_lines).
- Set rows from self.get\_rows(order\_lines).
- Set billed\_against\_rows from self.get\_billed\_against\_rows(list of row.name for row drawn from rows).
  - Draw row from rows.
- Set billed\_later from mapping().
- For each tuple(order\_line, line\_rows) in group\_by\_order\_line(rows).items().
  - Set billed from billed\_against\_lines.get(order\_line, Platform.\_dict()).
  - Evaluate billed\_later.update(self.get\_line\_billed\_later(line\_rows, billed, billed\_against\_rows)).
- Return billed\_later.

**Methods declared on this owner** [get order lines billed after](operations-060.md#op-488aae624648f6), [get billed against order lines](operations-060.md#op-8e59c0adbe67b1), [get rows](operations-061.md#op-3187aa3034a342), [get billed against rows](operations-060.md#op-5645dcef45fd80), [get line billed later](operations-060.md#op-5804609fad9ac7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1236)

<a id="op-5804609fad9ac7"></a>
### Order Billing As On.get line billed later

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_line_billed_later`

**Inputs** self, rows, billed, billed\_against\_rows.

**Declared result** dict at tuple(str, float).

**Explicit results** billed\_later.

**Local steps**

- Set today from self.spread(rows, billed.amount, billed.qty, billed\_against\_rows, …).
- Set then from self.spread(rows, billed.amount\_then, billed.qty\_then, billed\_against\_rows, …).
- Set billed\_later from mapping().
- For each row in rows.
  - Set difference from flt(((today at row.name − then at row.name) × flt(row.conversion\_rate)), self.precision).
  - If difference.
    - Set billed\_later at row.name from difference.
- Return billed\_later.

**Methods declared on this owner** [spread](operations-060.md#op-97bc02e000f713).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L173) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1238)

<a id="op-97bc02e000f713"></a>
### Order Billing As On.spread

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_spread`

**Inputs** self, rows, amount, qty, billed\_against\_rows, billed\_field.

**Declared result** dict at tuple(str, float).

**Explicit results** mapping of row.name → take(row, flt(nested operand in the contract.get(nested operand in the contract.name, mapping()).get(billed\_field))) for row drawn from rows.

**Local steps**

- Set pool from OrderBillingPool(amount, qty).
- Set take from pool.take\_for\_receipt when self.doctype equals “Purchase Receipt”, otherwise pool.take\_for\_delivery.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives pool.take\_for\_receipt, false gives pool.take\_for\_delivery.
- Return mapping of row.name → take(row, flt(nested operand in the contract.get(nested operand in the contract.name, mapping()).get(billed\_field))) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L177) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1242)

<a id="op-488aae624648f6"></a>
### Order Billing As On.get order lines billed after

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_order_lines_billed_after`

**Inputs** self.

**Declared result** list at str.

**Explicit results** nested operand in the contract().where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract &gt; nested operand in the contract)).where((order\_link. ….

**Local steps**

- Set tuple(invoice, invoice\_item) from tuple(self.invoice, self.invoice\_item).
- Set order\_link from invoice\_item at self.links.invoice\_order\_link.
- Return nested operand in the contract().where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract &gt; nested operand in the contract)).where((order\_link. ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L174) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1239)

<a id="op-8e59c0adbe67b1"></a>
### Order Billing As On.get billed against order lines

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_billed_against_order_lines`

**Inputs** self, order\_lines.

**Declared result** dict at tuple(str, Platform.\_dict).

**Explicit results** mapping of row.detail → row for row drawn from query.run(as\_dict = true).

**Local steps**

- Set invoice\_item from self.invoice\_item.
- Set order\_link from invoice\_item at self.links.invoice\_order\_link.
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.update\_stock equals 0).where(order\_link.isin(order\_lines)).where(IfNull(i ….
- Return mapping of row.detail → row for row drawn from query.run(as\_dict = true).
  - Draw row from query.run(as\_dict = true).

**Methods declared on this owner** [get billed query](operations-060.md#op-f1710cc942fd64), [sum till date](operations-061.md#op-03a28e9405d81d).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L169) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1234)

<a id="op-5645dcef45fd80"></a>
### Order Billing As On.get billed against rows

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_billed_against_rows`

**Inputs** self, row\_names.

**Declared result** dict at tuple(str, Platform.\_dict).

**Explicit results** mapping() · mapping of row.detail → row for row drawn from query.run(as\_dict = true).

**Local steps**

- If not row\_names.
  - Return mapping().
- Set row\_link from self.invoice\_item at self.links.invoice\_link.
- Set query from self.get\_billed\_query(row\_link).where(row\_link.isin(row\_names)).
- Return mapping of row.detail → row for row drawn from query.run(as\_dict = true).
  - Draw row from query.run(as\_dict = true).

**Methods declared on this owner** [get billed query](operations-060.md#op-f1710cc942fd64).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1235)

<a id="op-f1710cc942fd64"></a>
### Order Billing As On.get billed query

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_billed_query`

**Inputs** self, link\_field.

**Declared result** QueryBuilder.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where((nested operand ….

**Local steps**

- Set invoice\_item from self.invoice\_item.
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where((nested operand ….

**Methods declared on this owner** [sum till date](operations-061.md#op-03a28e9405d81d).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L172) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1237)
