# Accounting and settlement · operations 78

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pos closing entry

<a id="op-10e05fe5a8fb4e"></a>
### POSClosing Entry.validate pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate_point_of_sale_invoices`

**Inputs** self.

**Record and data access** read “POS Invoice” via get\_values.

**Explicit results** no value.

**Explicit failure paths** validation helper — error\_list.

**Local steps**

- Set invalid\_rows from list().
- For each d in self.pos\_invoices.
  - Set invalid\_row from mapping(“idx” → d.idx).
  - Set pos\_invoice from Platform.db.get\_values(“POS Invoice”, d.pos\_invoice, list(“consolidated\_invoice”, “pos\_profile”, “docstatus”, “owner”), as\_dict = 1) at 0.
  - If pos\_invoice.consolidated\_invoice.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “POS Invoice is already consolidated”).
    - Evaluate invalid\_rows.append(invalid\_row).
    - Continue with the next iteration or loop test.
  - If pos\_invoice.pos\_profile differs from self.pos\_profile.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “POS Profile doesn't match {}”.format(Platform.bold(self.pos\_profile))).
  - If pos\_invoice.docstatus differs from 1.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “POS Invoice is not submitted”).
  - If pos\_invoice.owner differs from self.user.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “POS Invoice isn't created by user {}”.format(Platform.bold(self.owner))).
  - If invalid\_row.get(“msg”).
    - Evaluate invalid\_rows.append(invalid\_row).
- If not invalid\_rows.
  - Return no value.
- Set error\_list from list().
- For each row in invalid\_rows.
  - For each msg in row.get(“msg”).
    - Evaluate error\_list.append(translated “Row #{}: {}”.format(row.get(“idx”), msg)).
- Call the validation error handler Platform.throw(error\_list, title = translated “Invalid POS Invoices”, as\_list = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L492)

<a id="op-3c32bbc55e1252"></a>
### POSClosing Entry.validate duplicate sales invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate_duplicate_sales_invoices`

**Inputs** self.

**Explicit failure paths** validation helper — error\_list.

**Local steps**

- Set sales\_invoice\_occurrences from mapping().
- For each tuple(idx, inv) in enumerate(self.sales\_invoices, 1).
  - Evaluate sales\_invoice\_occurrences.setdefault(inv.sales\_invoice, list()).append(idx).
- Set error\_list from list().
- For each tuple(key, value) in sales\_invoice\_occurrences.items().
  - If len(value) &gt; 1.
    - Evaluate error\_list.append(translated “{0} is added multiple times on rows: {1}”.format(Platform.bold(key), Platform.bold(value))).
- If error\_list.
  - Call the validation error handler Platform.throw(error\_list, title = translated “Duplicate Sales Invoices found”, as\_list = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L3468) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L490)

<a id="op-51e4db44510cd9"></a>
### POSClosing Entry.validate sales invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_validate_sales_invoices`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_values.

**Explicit results** no value.

**Explicit failure paths** validation helper — error\_list.

**Local steps**

- Set invalid\_rows from list().
- For each d in self.sales\_invoices.
  - Set invalid\_row from mapping(“idx” → d.idx).
  - Set sales\_invoice from Platform.db.get\_values(“Sales Invoice”, d.sales\_invoice, list(“pos\_profile”, “docstatus”, “is\_pos”, “owner”, …), as\_dict = 1) at 0.
  - If sales\_invoice.pos\_closing\_entry.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “Sales Invoice is already consolidated”).
    - Evaluate invalid\_rows.append(invalid\_row).
    - Continue with the next iteration or loop test.
  - If sales\_invoice.is\_pos equals 0.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “Sales Invoice does not have Payments”).
  - If sales\_invoice.is\_created\_using\_pos equals 0.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “Sales Invoice is not created using POS”).
  - If sales\_invoice.pos\_profile differs from self.pos\_profile.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “POS Profile doesn't match {}”.format(Platform.bold(self.pos\_profile))).
  - If sales\_invoice.docstatus differs from 1.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “Sales Invoice is not submitted”).
  - If sales\_invoice.owner differs from self.user.
    - Evaluate invalid\_row.setdefault(“msg”, list()).append(translated “Sales Invoice isn't created by user {}”.format(Platform.bold(self.owner))).
  - If invalid\_row.get(“msg”).
    - Evaluate invalid\_rows.append(invalid\_row).
- If not invalid\_rows.
  - Return no value.
- Set error\_list from list().
- For each row in invalid\_rows.
  - For each msg in row.get(“msg”).
    - Evaluate error\_list.append(translated “Row #{}: {}”.format(row.get(“idx”), msg)).
- Call the validation error handler Platform.throw(error\_list, title = translated “Invalid Sales Invoices”, as\_list = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L494)

<a id="op-498d8858ac8f91"></a>
### POSClosing Entry.before submit

`operation_enterprise_binding_enterprise_accounts_doctype_pos_closing_entry_pos_closing_entry_posclosingentry_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_session\_invoices\_are\_included().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate session invoices are included](operations-078.md#op-b63d3902ca092f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L246) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L884)

<a id="op-b63d3902ca092f"></a>
### POSClosing Entry.validate session invoices are included

`operation_enterprise_binding_enterprise_accounts_doctype_pos_closing_entry_pos_closing_entry_posclosingentry_validate_session_invoices_are_included`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L247) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L885)

<a id="op-4a155522974786"></a>
### POSClosing Entry.on submit

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_on_submit`

**Inputs** self.

**State and service calls** publish realtime with formatted text poe\_{self.pos\_opening\_entry}.

**Local steps**

- Evaluate consolidate\_pos\_invoices(closing\_entry = self).
- Evaluate Platform.publish\_realtime(formatted text poe\_{self.pos\_opening\_entry}, message = mapping(“operation” → “Closed”, “doc” → self), docname = formatted text POS Opening Entry/{self.pos\_opening\_entry}).
- Evaluate self.update\_sales\_invoices\_closing\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update sales invoices closing entry](operations-078.md#op-164ac4d6ab8723).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(formatted text poe\_{self.pos\_opening\_entry}, message = mapping(“operation” → “Closed”, “doc” → self), docname = formatted text POS Opening Entry/{self.pos\_opening\_entry}).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L4918) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L483)

<a id="op-2a290e83348fab"></a>
### POSClosing Entry.before cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_before_cancel`

**Inputs** self.

**Local steps**

- If self.status differs from “Failed”.
  - Evaluate self.check\_pce\_is\_cancellable().

If control reaches the end, it returns no value.

**Methods declared on this owner** [check pce is cancellable](operations-078.md#op-4ae2b6883a3e68).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L5107) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L479)

<a id="op-3ec92ea4c1bfc8"></a>
### POSClosing Entry.on cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate unconsolidate\_pos\_invoices(closing\_entry = self).
- Evaluate self.update\_sales\_invoices\_closing\_entry(cancel = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update sales invoices closing entry](operations-078.md#op-164ac4d6ab8723).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L5184) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L482)

<a id="op-331ffa63f20c55"></a>
### POSClosing Entry.retry

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_retry`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper — translated “Only a POS Closing Entry with status Failed can be retried”.

**Local steps**

- Evaluate self.load\_from\_db().
- If (self.docstatus equals 0 or self.status differs from “Failed”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus equals 0 → self.status differs from “Failed”.
  - Call the validation error handler Platform.throw(translated “Only a POS Closing Entry with status Failed can be retried”).
- If self.docstatus equals 2.
  - Evaluate self.check\_permission(“cancel”).
  - Evaluate self.check\_pce\_is\_cancellable().
  - Evaluate unconsolidate\_pos\_invoices(closing\_entry = self).
- Otherwise.
  - Evaluate self.check\_permission(“submit”).
  - Evaluate self.validate\_session\_invoices\_are\_included().
  - Evaluate consolidate\_pos\_invoices(closing\_entry = self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check pce is cancellable](operations-078.md#op-4ae2b6883a3e68), [validate session invoices are included](operations-078.md#op-b63d3902ca092f).

**Values supplied outside this operation** effective access from self.check\_permission(“cancel”), self.check\_permission(“submit”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L484)

<a id="op-83807d3f02a195"></a>
### POSClosing Entry.update opening entry

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_update_opening_entry`

**Inputs** self, for\_cancel = false.

**Record and data access** resolve a document from “POS Opening Entry” via get\_doc.

**State and service calls** call save on opening\_entry.

**Local steps**

- Set opening\_entry from Platform.get\_doc(“POS Opening Entry”, self.pos\_opening\_entry).
- Set opening\_entry.pos\_closing\_entry from self.name when not for\_cancel, otherwise no value.
  - Value choice on not for\_cancel — true gives self.name, false gives no value.
- Evaluate opening\_entry.set\_status().
- Evaluate opening\_entry.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L5349) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L486)

<a id="op-164ac4d6ab8723"></a>
### POSClosing Entry.update sales invoices closing entry

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_update_sales_invoices_closing_entry`

**Inputs** self, cancel = false.

**State and service calls** request set\_value on “Sales Invoice”.

**Local steps**

- For each d in self.sales\_invoices.
  - Evaluate Platform.db.set\_value(“Sales Invoice”, d.sales\_invoice, “pos\_closing\_entry”, self.name when not cancel, otherwise no value).
    - Value choice on not cancel — true gives self.name, false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L5506) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L487)

<a id="op-4ae2b6883a3e68"></a>
### POSClosing Entry.check pce is cancellable

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_point_of_sale_closing_entry_check_pce_is_cancellable`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via exists.

**Explicit failure paths** validation helper.

**Local steps**

- If Platform.db.exists(“POS Opening Entry”, mapping(“pos\_profile” → self.pos\_profile, “status” → “Open”)).
  - Call the validation error handler Platform.throw(title = translated “Cannot cancel POS Closing Entry”, msg = translated “POS Profile - {0} is currently open. Please close the POS or cancel the existing POS Opening Entry before ca …”.format ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0116.json#L5640) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L480)

<a id="op-1ea258a1e9a139"></a>
### Get cashiers

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_get_cashiers`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “POS Profile” via exists · read “POS Profile User” via get\_all.

**Explicit results** list() · list of c for c drawn from cashiers\_list.

**Local steps**

- Set pos\_profile from filters.get(“parent”).
- If (not pos\_profile or not Platform.db.exists(“POS Profile”, pos\_profile)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not pos\_profile → not Platform.db.exists(“POS Profile”, pos\_profile).
  - Return list().
- Set ptype from “select” when Platform.only\_has\_select\_perm(“POS Profile”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“POS Profile”) — true gives “select”, false gives “read”.
- Evaluate Platform.has\_permission(“POS Profile”, ptype, doc = pos\_profile, throw = true).
- Set cashiers\_list from Platform.get\_all(“POS Profile User”, filters = filters, fields = list(“user”), as\_list = 1).
- Return list of c for c drawn from cashiers\_list.
  - Draw c from cashiers\_list.

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Profile”, ptype, doc = pos\_profile, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L291) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L474)

<a id="op-67b0ceab32d067"></a>
### Get invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_get_invoices`

**Inputs** start, end, pos\_profile, user.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “POS Settings” via get\_single\_value.

**Explicit results** mapping(“invoices” → invoices, “payments” → get\_payments(invoices), “taxes” → get\_taxes(invoices)).

**Local steps**

- Evaluate Platform.has\_permission(“POS Profile”, doc = pos\_profile, throw = true).
- Evaluate Platform.has\_permission(“Sales Invoice”, throw = true).
- If Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”) equals “POS Invoice”.
  - Evaluate Platform.has\_permission(“POS Invoice”, throw = true).
- Set invoices from get\_session\_invoices(start, end, pos\_profile, user).
- Return mapping(“invoices” → invoices, “payments” → get\_payments(invoices), “taxes” → get\_taxes(invoices)).

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Profile”, doc = pos\_profile, throw = true), Platform.has\_permission(“Sales Invoice”, throw = true) and 1 further calls · configured or stored value from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L292) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L475)

<a id="op-3ec0e8c1fad7e9"></a>
### Get session invoices

`operation_enterprise_binding_enterprise_accounts_doctype_pos_closing_entry_pos_closing_entry_get_session_invoices`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** start, end, pos\_profile, user.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L245) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L883)

<a id="op-17e1f4802a61ec"></a>
### Get payments

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_get_payments`

**Inputs** invoices.

**Explicit results** list() · list of Platform.\_dict(mode\_of\_payment = mode, amount = amount) for tuple(mode, amount) drawn from amount\_by\_mode.items().

**Local steps**

- If not len(invoices).
  - Return list().
- Set rows\_by\_invoice from get\_payment\_rows\_by\_invoice(invoices).
- For each invoice in invoices.
  - If not flt(invoice.change\_amount).
    - Continue with the next iteration or loop test.
  - Set rows from rows\_by\_invoice.get(tuple(invoice.doctype, invoice.name), list()).
  - If row bound to get\_change\_payment\_row(rows, invoice.account\_for\_change\_amount).
    - Set row.amount from (flt(row.amount) − flt(invoice.change\_amount)).
- Set amount\_by\_mode from mapping().
- For each rows in rows\_by\_invoice.values().
  - For each row in rows.
    - Set amount\_by\_mode at row.mode\_of\_payment from (amount\_by\_mode.get(row.mode\_of\_payment, 0) + flt(row.amount)).
- Return list of Platform.\_dict(mode\_of\_payment = mode, amount = amount) for tuple(mode, amount) drawn from amount\_by\_mode.items().
  - Draw tuple(mode, amount) from amount\_by\_mode.items().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L476)

<a id="op-3e1a68737fa722"></a>
### Get payment rows by invoice

`operation_enterprise_binding_enterprise_accounts_doctype_pos_closing_entry_pos_closing_entry_get_payment_rows_by_invoice`

**Inputs** invoices.

**Explicit results** rows\_by\_invoice.

**Local steps**

- Set SalesInvoicePayment from DocType(“Sales Invoice Payment”).
- Set rows from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract(neste ….
  - Draw d from invoices.
- Set rows\_by\_invoice from mapping().
- For each row in rows.
  - Evaluate rows\_by\_invoice.setdefault(tuple(row.parenttype, row.parent), list()).append(row).
- Return rows\_by\_invoice.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L244) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L882)

<a id="op-2489a244a026a6"></a>
### Get change payment row

`operation_enterprise_binding_enterprise_accounts_doctype_pos_closing_entry_pos_closing_entry_get_change_payment_row`

**Inputs** rows, change\_account.

**Explicit results** (next(generator of row for row drawn from change\_account\_rows where row.type equals “Cash”, no value) or next(iter(change\_account\_rows), no value) or next(generator of row for row drawn from rows where row ….

**Local steps**

- Set change\_account\_rows from list of row for row drawn from rows where row.account equals change\_account.
  - Draw row from rows, keep a combination only if (row.account equals change\_account).
- Return (next(generator of row for row drawn from change\_account\_rows where row.type equals “Cash”, no value) or next(iter(change\_account\_rows), no value) or next(generator of row for row drawn from rows where row ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in next(generator of row for row drawn from change\_account\_rows where row.type equals “Cash”, no value) → next(iter(change\_account\_rows), no value) → next(generator of row for row drawn from rows where row.type equals “Cash”, no value).
  - Draw row from change\_account\_rows, keep a combination only if (row.type equals “Cash”).
  - Draw row from rows, keep a combination only if (row.type equals “Cash”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L243) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L881)

<a id="op-4f1630be07a5b5"></a>
### Get taxes

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_get_taxes`

**Inputs** invoices.

**Explicit results** list() · data.

**Local steps**

- If not len(invoices).
  - Return list().
- Set invoices\_name from list of d.name for d drawn from invoices.
  - Draw d from invoices.
- Set SalesInvoiceTaxesCharges from DocType(“Sales Taxes and Charges”).
- Set query from nested operand in the contract(nested operand in the contract).where((nested operand in the contract(nested operand in the contract) bitwise and nested operand in the contract(nested operand in the contrac ….
- Set data from query.run(as\_dict = 1).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0117.json#L619) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L477)

<a id="op-23f6725ad54552"></a>
### Make closing entry from opening

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_make_closing_entry_from_opening`

**Inputs** opening\_entry.

**State and service calls** request new\_doc for “POS Closing Entry”.

**Explicit results** closing\_entry.

**Local steps**

- Set closing\_entry from Platform.new\_doc(“POS Closing Entry”).
- Set closing\_entry.pos\_opening\_entry from opening\_entry.name.
- Set closing\_entry.period\_start\_date from opening\_entry.period\_start\_date.
- Set closing\_entry.period\_end\_date from Platform.utils.get\_datetime().
- Set closing\_entry.pos\_profile from opening\_entry.pos\_profile.
- Set closing\_entry.user from opening\_entry.user.
- Set closing\_entry.company from opening\_entry.company.
- Set closing\_entry.grand\_total from 0.
- Set closing\_entry.net\_total from 0.
- Set closing\_entry.total\_quantity from 0.
- Set closing\_entry.total\_taxes\_and\_charges from 0.
- Set data from get\_invoices(closing\_entry.period\_start\_date, closing\_entry.period\_end\_date, closing\_entry.pos\_profile, closing\_entry.user).
- Set pos\_invoices from list().
- Set sales\_invoices from list().
- Set taxes from list of Platform.\_dict(mapping(“account\_head” → tx.account\_head, “amount” → tx.tax\_amount)) for tx drawn from data.get(“taxes”).
  - Draw tx from data.get(“taxes”).
- Set payments from list of Platform.\_dict(mapping(“mode\_of\_payment” → p.mode\_of\_payment, “opening\_amount” → 0, “expected\_amount” → p.amount)) for p drawn from data.get(“payments”).
  - Draw p from data.get(“payments”).
- For each d in data.get(“invoices”).
  - Set invoice from “pos\_invoice” when d.doctype equals “POS Invoice”, otherwise “sales\_invoice”.
    - Value choice on d.doctype equals “POS Invoice” — true gives “pos\_invoice”, false gives “sales\_invoice”.
  - Set invoice\_data from Platform.\_dict(mapping(invoice → d.name, “posting\_date” → d.posting\_date, “grand\_total” → d.grand\_total, “customer” → d.customer, …)).
  - If d.doctype equals “POS Invoice”.
    - Evaluate pos\_invoices.append(invoice\_data).
  - Otherwise.
    - Evaluate sales\_invoices.append(invoice\_data).
  - Update closing\_entry.grand\_total using + flt(d.grand\_total).
  - Update closing\_entry.net\_total using + flt(d.net\_total).
  - Update closing\_entry.total\_quantity using + flt(d.total\_qty).
  - Update closing\_entry.total\_taxes\_and\_charges using + flt(d.total\_taxes\_and\_charges).
- Evaluate closing\_entry.set(“pos\_invoices”, pos\_invoices).
- Evaluate closing\_entry.set(“sales\_invoices”, sales\_invoices).
- Evaluate closing\_entry.set(“payment\_reconciliation”, payments).
- Evaluate closing\_entry.set(“taxes”, taxes).
- Return closing\_entry.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0117.json#L999) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L478)

<a id="op-a248ac2ff39326"></a>
### Build invoice query

`operation_enterprise_accounts_record_definitions_point_of_sale_closing_entry_business_behavior_build_invoice_query`

**Inputs** invoice\_doctype, user, pos\_profile, start, end.

**Explicit results** query.

**Local steps**

- Set InvoiceDocType from DocType(invoice\_doctype).
- Set query from nested operand in the contract.qb.from\_(InvoiceDocType).select(InvoiceDocType.name, InvoiceDocType.customer, InvoiceDocType.posting\_date, InvoiceDocType.grand\_total, …).where(((((nested operand in the cont ….
- If invoice\_doctype equals “POS Invoice”.
  - Set query from query.where(fn.IfNull(InvoiceDocType.consolidated\_invoice, empty text).eq(empty text)).
- Otherwise.
  - Set query from query.where((InvoiceDocType.is\_created\_using\_pos equals 1 bitwise and fn.IfNull(InvoiceDocType.pos\_closing\_entry, empty text).eq(empty text))).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L290) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L473)

## Record · Pos invoice

<a id="op-9f8aa3d95516e7"></a>
### POSInvoice.initialize

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0118.json#L4909) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L531)

<a id="op-77f5764844a3d3"></a>
### POSInvoice.validate

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please select Customer first” · validation helper — translated “POS Invoice should have the field {0} checked.”.format(Platform.bold(translated “Include Payment”)).

**Local steps**

- If not self.customer.
  - Call the validation error handler Platform.throw(translated “Please select Customer first”).
- If not cint(self.is\_pos).
  - Call the validation error handler Platform.throw(translated “POS Invoice should have the field {0} checked.”.format(Platform.bold(translated “Include Payment”))).
- Evaluate super(SalesInvoice, self).validate().
- Evaluate self.validate\_auto\_set\_posting\_time().
- Evaluate self.validate\_pos\_opening\_entry().
- Evaluate self.validate\_is\_pos\_using\_sales\_invoice().
- Evaluate self.validate\_mode\_of\_payment().
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_debit\_to\_acc().
- Evaluate self.validate\_write\_off\_account().
- Evaluate self.validate\_loyalty\_transaction().
- Evaluate self.set\_pos\_paid\_amount().
- Evaluate self.validate\_change\_amount().
- Evaluate self.validate\_change\_account().
- Evaluate self.validate\_item\_cost\_centers().
- Evaluate self.validate\_warehouse().
- Evaluate self.validate\_serialised\_or\_batched\_item().
- Evaluate self.validate\_stock\_availablility().
- Evaluate self.validate\_return\_items\_qty().
- Evaluate self.set\_status().
- Evaluate self.validate\_pos().
- Evaluate self.validate\_payment\_amount().
- Evaluate self.validate\_company\_with\_pos\_company().
- Evaluate self.validate\_full\_payment().
- Evaluate self.update\_packing\_list().
- If (self.coupon\_code and self.counts\_coupon\_use()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.coupon\_code → self.counts\_coupon\_use().
  - Evaluate validate\_coupon\_code(self.coupon\_code, self.customer).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate is pos using sales invoice](operations-079.md#op-fede8a1ee4745e), [validate mode of payment](operations-079.md#op-8c794bd3718a64), [validate loyalty transaction](operations-079.md#op-15346b78f0c4b5), [set pos paid amount](operations-079.md#op-1e3bfe125ecd5e), [validate change amount](operations-079.md#op-fdc9b0225cb55d), [validate change account](operations-079.md#op-52d55db02a4bbc), [validate serialised or batched item](operations-079.md#op-7e936d87fc81b5), [validate stock availablility](operations-079.md#op-9df628d748a94f), [validate return items qty](operations-079.md#op-6267292a7cb408), [set status](operations-080.md#op-c4fa1c7ebc3e03), [validate payment amount](operations-079.md#op-15f07558f65b99), [validate company with pos company](operations-079.md#op-1749f21f793e59).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L541)

<a id="op-2311c6954e6a64"></a>
### POSInvoice.before submit

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_mandatory\_pos\_fields().
- Evaluate self.set\_outstanding\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set outstanding amount](operations-079.md#op-5863bde92b1c9b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L522)
