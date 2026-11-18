# Accounting and settlement · operations 81

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pos invoice

<a id="op-7273bd3e243d05"></a>
### Add return modes

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_add_return_modes`

**Inputs** doc, pos\_profile.

**Local steps**

- Bind local operation append\_payment for subsequent calls.
- For each pos\_payment\_method in pos\_profile.get(“payments”).
  - Set pos\_payment\_method from pos\_payment\_method.as\_dict().
  - Set mode\_of\_payment from pos\_payment\_method.mode\_of\_payment.
  - If (pos\_payment\_method.allow\_in\_returns and not list of d for d drawn from doc.get(“payments”) where d.mode\_of\_payment equals mode\_of\_payment).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pos\_payment\_method.allow\_in\_returns → not list of d for d drawn from doc.get(“payments”) where d.mode\_of\_payment equals mode\_of\_payment.
    - Draw d from doc.get(“payments”), keep a combination only if (d.mode\_of\_payment equals mode\_of\_payment).
    - Set payment\_mode from get\_mode\_of\_payment\_info(mode\_of\_payment, doc.company).
    - Evaluate append\_payment(payment\_mode at 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0121.json#L2220) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L509)

<a id="op-7d0773ca127522"></a>
### Add return modes.append payment

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_add_return_modes_append_payment`

**Inputs** payment\_mode.

**Local steps**

- Set payment from doc.append(“payments”, mapping()).
- Set payment.default from payment\_mode.default.
- Set payment.mode\_of\_payment from payment\_mode.parent.
- Set payment.account from payment\_mode.default\_account.
- Set payment.type from payment\_mode.type.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0121.json#L2628) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L510)

<a id="op-76ad57c074d402"></a>
### Item query

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_item_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters, as\_dict = false.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** resolve a document from “POS Profile” via get\_cached\_doc.

**Explicit results** \_item\_query(doctype, txt, searchfield, start, …).

**Local steps**

- If pos\_profile bound to filters.get(“pos\_profile”) at 1.
  - Set pos\_profile from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).
  - If item\_groups bound to get\_item\_group(pos\_profile).
    - Set filters at “item\_group” from list(“in”, tuple(item\_groups)).
  - Remove filters at “pos\_profile”.
- Otherwise.
  - Evaluate filters.pop(“pos\_profile”, no value).
- Return \_item\_query(doctype, txt, searchfield, start, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L518)

<a id="op-f62acdbf4fe752"></a>
### Get item group

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_get_item_group`

**Inputs** pos\_profile.

**Explicit results** list(set(item\_groups)).

**Local steps**

- Set item\_groups from list().
- If pos\_profile.get(“item\_groups”).
  - For each row in pos\_profile.get(“item\_groups”).
    - Evaluate item\_groups.append(row.item\_group).
    - Evaluate item\_groups.extend(get\_descendants\_of(“Item Group”, row.item\_group)).
- Return list(set(item\_groups)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0121.json#L3180) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L514)

<a id="op-b13a4c32736853"></a>
### Create payments on invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_create_payments_on_invoice`

**Inputs** doc, idx, payment\_details.

**State and service calls** request new\_doc for “Sales Invoice Payment”.

**Explicit results** payment.

**Local steps**

- Bind dependencies get\_bank\_cash\_account.
- Set payment from Platform.new\_doc(“Sales Invoice Payment”).
- Set payment.idx from idx.
- Set payment.mode\_of\_payment from payment\_details.mode\_of\_payment.
- Set payment.amount from payment\_details.amount.
- Set payment.base\_amount from (payment.amount × doc.conversion\_rate).
- Set payment.parent from doc.name.
- Set payment.parentfield from “payments”.
- Set payment.parenttype from doc.doctype.
- Set payment.account from get\_bank\_cash\_account(payment.mode\_of\_payment, doc.company).get(“account”).
- Return payment.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0121.json#L3399) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L511)

## Record · Pos invoice merge log

<a id="op-f29031eb221551"></a>
### POSInvoice Merge Log.validate

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_customer().
- Evaluate self.validate\_pos\_invoice\_status().
- Evaluate self.validate\_duplicate\_pos\_invoices().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate customer](operations-081.md#op-2bef35888f3448), [validate pos invoice status](operations-081.md#op-85affe9a0b723d), [validate duplicate pos invoices](operations-081.md#op-f556c04953dada).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0124.json#L2484) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L574)

<a id="op-f556c04953dada"></a>
### POSInvoice Merge Log.validate duplicate pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_validate_duplicate_point_of_sale_invoices`

**Inputs** self.

**Explicit failure paths** validation helper — error\_list.

**Local steps**

- Set pos\_occurences from mapping().
- For each tuple(idx, inv) in enumerate(self.pos\_invoices, 1).
  - Evaluate pos\_occurences.setdefault(inv.pos\_invoice, list()).append(idx).
- Set error\_list from list().
- For each tuple(key, value) in pos\_occurences.items().
  - If len(value) &gt; 1.
    - Evaluate error\_list.append(translated “{0} is added multiple times on rows: {1}”.format(Platform.bold(key), Platform.bold(value))).
- If error\_list.
  - Call the validation error handler Platform.throw(error\_list, title = translated “Duplicate POS Invoices found”, as\_list = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0124.json#L2575) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L576)

<a id="op-2bef35888f3448"></a>
### POSInvoice Merge Log.validate customer

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_validate_customer`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{}: POS Invoice {} is not against customer {}”.format(d.idx, d.pos\_invoice, self.customer).

**Local steps**

- If self.merge\_invoices\_based\_on equals “Customer Group”.
  - Evaluate self.validate\_customer\_group().
  - Return no value.
- For each d in self.pos\_invoices.
  - If d.customer differs from self.customer.
    - Call the validation error handler Platform.throw(translated “Row #{}: POS Invoice {} is not against customer {}”.format(d.idx, d.pos\_invoice, self.customer)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate customer group](operations-081.md#op-7a469cc18a6d2d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L575)

<a id="op-7a469cc18a6d2d"></a>
### POSInvoice Merge Log.validate customer group

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_merge_log_pos_invoice_merge_log_posinvoicemergelog_validate_customer_group`

**Inputs** self.

**Record and data access** read “Customer” via get\_all.

**Explicit failure paths** validation helper — translated “Customer Group is mandatory to merge invoices based on Customer Group” · validation helper — translated “Row #{0}: Customer {1} of POS Invoice {2} is not in Customer Group {3}”.format(d.idx, Platform.bold(d.customer), Platform.bold(d.pos\_invoice), Platform.bold(self.customer\_group)).

**Local steps**

- If not self.customer\_group.
  - Call the validation error handler Platform.throw(translated “Customer Group is mandatory to merge invoices based on Customer Group”).
- Set customer\_groups from list(self.customer\_group, expanded get\_descendants\_of(“Customer Group”, self.customer\_group)).
- Set customers\_outside\_group from Platform.get\_all(“Customer”, filters = mapping(“name” → list(“in”, list(set of d.customer for d drawn from self.pos\_invoices)), “customer\_group” → list(“not in”, customer\_groups)), pluck = “name”).
  - Draw d from self.pos\_invoices.
- For each d in self.pos\_invoices.
  - If d.customer belongs to customers\_outside\_group.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Customer {1} of POS Invoice {2} is not in Customer Group {3}”.format(d.idx, Platform.bold(d.customer), Platform.bold(d.pos\_invoice), Platform.bold(self.customer\_group))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L250) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L888)

<a id="op-85affe9a0b723d"></a>
### POSInvoice Merge Log.validate pos invoice status

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_validate_point_of_sale_invoice_status`

**Inputs** self.

**Record and data access** read “POS Invoice” via get\_value.

**Explicit failure paths** validation helper — translated “Row #{}: POS Invoice {} is not submitted yet”.format(d.idx, bold\_pos\_invoice) · validation helper — translated “Row #{}: POS Invoice {} has been {}”.format(d.idx, bold\_pos\_invoice, bold\_status) · validation helper — msg.

**Local steps**

- For each d in self.pos\_invoices.
  - Set tuple(status, docstatus, is\_return, return\_against) from Platform.db.get\_value(“POS Invoice”, d.pos\_invoice, list(“status”, “docstatus”, “is\_return”, “return\_against”)).
  - Set bold\_pos\_invoice from Platform.bold(d.pos\_invoice).
  - Set bold\_status from Platform.bold(status).
  - <a id="op-85affe9a0b723d-guard-9"></a>If docstatus differs from 1.
    - Call the validation error handler Platform.throw(translated “Row #{}: POS Invoice {} is not submitted yet”.format(d.idx, bold\_pos\_invoice)).
  - If status equals “Consolidated”.
    - Call the validation error handler Platform.throw(translated “Row #{}: POS Invoice {} has been {}”.format(d.idx, bold\_pos\_invoice, bold\_status)).
  - If (is\_return and return\_against and return\_against does not belong to list of d.pos\_invoice for d drawn from self.pos\_invoices).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_return → return\_against → return\_against does not belong to list of d.pos\_invoice for d drawn from self.pos\_invoices.
    - Draw d from self.pos\_invoices.
    - Set bold\_return\_against from Platform.bold(return\_against).
    - Set return\_against\_status from Platform.db.get\_value(“POS Invoice”, return\_against, “status”).
    - If return\_against\_status differs from “Consolidated”.
      - Set msg from translated “Row #{}: The original Invoice {} of return invoice {} is not consolidated.”.format(d.idx, bold\_return\_against, bold\_pos\_invoice).
      - Update msg using + one space.
      - Update msg using + translated “The original invoice should be consolidated before or along with the return invoice.”.
      - Update msg using + text in the contract.
      - Update msg using + translated “You can add the original invoice {} manually to proceed.”.format(bold\_return\_against).
      - Call the validation error handler Platform.throw(msg).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison docstatus differs from 1, docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Row #{}: POS Invoice {} is not submitted yet”.format(d.idx, bold\_pos\_invoice). With docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-85affe9a0b723d-guard-9)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L577)

<a id="op-20c8bce8889ac9"></a>
### POSInvoice Merge Log.on submit

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “POS Invoice” via get\_cached\_doc.

**State and service calls** call save on self.

**Local steps**

- Set pos\_invoice\_docs from list of Platform.get\_cached\_doc(“POS Invoice”, d.pos\_invoice) for d drawn from self.pos\_invoices.
  - Draw d from self.pos\_invoices.
- Set returns from list of d for d drawn from pos\_invoice\_docs where d.get(“is\_return”) equals 1.
  - Draw d from pos\_invoice\_docs, keep a combination only if (d.get(“is\_return”) equals 1).
- Set sales from list of d for d drawn from pos\_invoice\_docs where d.get(“is\_return”) equals 0.
  - Draw d from pos\_invoice\_docs, keep a combination only if (d.get(“is\_return”) equals 0).
- Set tuple(sales\_invoice, credit\_notes) from tuple(empty text, mapping()).
- Set sales\_invoice\_doc from no value.
- If sales.
  - Set sales\_invoice\_doc from self.process\_merging\_into\_sales\_invoice(sales).
  - Set sales\_invoice from sales\_invoice\_doc.name.
- If returns.
  - Set distinguished\_returns from self.distinguish\_return\_pos\_invoices(returns, sales\_invoice\_doc).
  - Set credit\_notes from self.process\_merging\_into\_credit\_notes(distinguished\_returns).
- Evaluate self.save().
- Evaluate self.update\_pos\_invoices(pos\_invoice\_docs, sales\_invoice, credit\_notes).

If control reaches the end, it returns no value.

**Methods declared on this owner** [process merging into sales invoice](operations-081.md#op-980b061abfaebd), [distinguish return pos invoices](operations-081.md#op-3636e566f6cec0), [process merging into credit notes](operations-081.md#op-4762cde9038657), [update pos invoices](operations-081.md#op-a63450bd93be33).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Invoice”, d.pos\_invoice).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0124.json#L3876) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L569)

<a id="op-67132f6108f81d"></a>
### POSInvoice Merge Log.on cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_on_cancel`

**Inputs** self.

**Record and data access** resolve a document from “POS Invoice” via get\_cached\_doc.

**Local steps**

- Set pos\_invoice\_docs from list of Platform.get\_cached\_doc(“POS Invoice”, d.pos\_invoice) for d drawn from self.pos\_invoices.
  - Draw d from self.pos\_invoices.
- Set credit\_notes from self.get\_consolidated\_credit\_notes().
- Evaluate self.update\_pos\_invoices(pos\_invoice\_docs).
- Evaluate self.cancel\_linked\_invoices(credit\_notes).
- Evaluate self.serial\_and\_batch\_bundle\_reference\_for\_pos\_invoice().
- Evaluate self.delink\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get consolidated credit notes](operations-081.md#op-0658c0b2245625), [update pos invoices](operations-081.md#op-a63450bd93be33), [cancel linked invoices](operations-081.md#op-2d8f13b5e162b0), [serial and batch bundle reference for pos invoice](operations-081.md#op-becb79b5ce70e8), [delink serial and batch bundle](operations-081.md#op-d586eb28d111ac).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Invoice”, d.pos\_invoice).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L568)

<a id="op-980b061abfaebd"></a>
### POSInvoice Merge Log.process merging into sales invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_process_merging_into_sales_invoice`

**Inputs** self, data.

**State and service calls** call save on sales\_invoice · call submit on sales\_invoice.

**Explicit results** sales\_invoice.

**Local steps**

- Set sales\_invoice from self.get\_new\_sales\_invoice().
- Set sales\_invoice from self.merge\_pos\_invoice\_into(sales\_invoice, data).
- Set sales\_invoice.is\_consolidated from 1.
- Set sales\_invoice.flags.is\_consolidated from true.
- Set sales\_invoice.set\_posting\_time from 1.
- If not sales\_invoice.posting\_date.
  - Set sales\_invoice.posting\_date from getdate(self.posting\_date).
- If not sales\_invoice.posting\_time.
  - Set sales\_invoice.posting\_time from get\_time(self.posting\_time).
- Evaluate sales\_invoice.save().
- Evaluate sales\_invoice.submit().
- Set self.consolidated\_invoice from sales\_invoice.name.
- Return sales\_invoice.

**Methods declared on this owner** [get new sales invoice](operations-081.md#op-c77e7ffbdb1ceb), [merge pos invoice into](operations-081.md#op-0e7674ebc29326).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L571)

<a id="op-4762cde9038657"></a>
### POSInvoice Merge Log.process merging into credit notes

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_process_merging_into_credit_notes`

**Inputs** self, data.

**State and service calls** call save on credit\_note · call submit on credit\_note.

**Explicit results** credit\_notes.

**Local steps**

- Set credit\_notes from mapping().
- For each tuple(key, value) in data.items().
  - If not value.
    - Continue with the next iteration or loop test.
  - Set credit\_note from self.get\_new\_sales\_invoice().
  - Set credit\_note.is\_return from 1.
  - Set credit\_note from self.merge\_pos\_invoice\_into(credit\_note, value).
  - Set credit\_note.return\_against from key.
  - Set credit\_note.is\_consolidated from 1.
  - Set credit\_note.flags.is\_consolidated from true.
  - Set credit\_note.set\_posting\_time from 1.
  - Set credit\_note.posting\_date from getdate(self.posting\_date).
  - Set credit\_note.posting\_time from get\_time(self.posting\_time).
  - Evaluate credit\_note.save().
  - Evaluate credit\_note.submit().
  - Set self.consolidated\_credit\_note from credit\_note.name.
  - Set credit\_notes at credit\_note.name from list of d.name for d drawn from value.
    - Draw d from value.
- Return credit\_notes.

**Methods declared on this owner** [get new sales invoice](operations-081.md#op-c77e7ffbdb1ceb), [merge pos invoice into](operations-081.md#op-0e7674ebc29326).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L570)

<a id="op-3636e566f6cec0"></a>
### POSInvoice Merge Log.distinguish return pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_distinguish_return_point_of_sale_invoices`

**Inputs** self, data, sales\_invoice\_doc = no value.

**Record and data access** read “POS Invoice” via get\_value.

**Explicit results** return\_invoices.

**Local steps**

- Set return\_invoices from mapping().
- Set return\_invoices at sales\_invoice\_doc.name when sales\_invoice\_doc, otherwise no value from list().
  - Value choice on sales\_invoice\_doc — true gives sales\_invoice\_doc.name, false gives no value.
- For each doc in data.
  - Set sales\_invoices\_of\_return\_against from Platform.db.get\_value(“POS Invoice”, doc.return\_against, “consolidated\_invoice”).
  - If sales\_invoices\_of\_return\_against.
    - If sales\_invoices\_of\_return\_against belongs to return\_invoices.
      - Evaluate return\_invoices at sales\_invoices\_of\_return\_against.append(doc).
    - Otherwise.
      - Set return\_invoices at sales\_invoices\_of\_return\_against from list(doc).
  - Otherwise.
    - Evaluate return\_invoices at sales\_invoice\_doc.name when sales\_invoice\_doc, otherwise no value.append(doc).
      - Value choice on sales\_invoice\_doc — true gives sales\_invoice\_doc.name, false gives no value.
- Return return\_invoices.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0124.json#L5245) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L564)

<a id="op-0e7674ebc29326"></a>
### POSInvoice Merge Log.merge pos invoice into

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_merge_point_of_sale_invoice_into`

**Inputs** self, invoice, data.

**Record and data access** read “POS Profile” via get\_value.

**Explicit results** invoice.

**Explicit failure paths** validation helper — translated “Please set Accounting Dimension {} in {}”.format(Platform.bold(dimension.label), Platform.get\_desk\_link(“POS Profile”, invoice.pos\_profile)).

**Local steps**

- Set tuple(items, payments, taxes, item\_tax\_details) from tuple(list(), list(), list(), list()).
- Set tuple(loyalty\_amount\_sum, loyalty\_points\_sum, idx) from tuple(0, 0, 1).
- Set reversed\_rows from get\_reversed\_rows(list of doc.return\_against for doc drawn from data where doc.is\_return).
  - Draw doc from data, keep a combination only if (doc.is\_return).
- For each doc in data.
  - Set old\_new\_item\_map from Platform.\_dict().
  - Set old\_new\_tax\_map from Platform.\_dict().
  - Evaluate map\_doc(doc, invoice, table\_map = mapping(“doctype” → invoice.doctype)).
  - If doc.get(“posting\_date”).
    - Set invoice.posting\_date from getdate(doc.posting\_date).
    - Set invoice.posting\_time from get\_time(doc.posting\_time).
  - If doc.redeem\_loyalty\_points.
    - Set invoice.loyalty\_redemption\_account from doc.loyalty\_redemption\_account.
    - Set invoice.loyalty\_redemption\_cost\_center from doc.loyalty\_redemption\_cost\_center.
    - Update loyalty\_points\_sum using + doc.loyalty\_points.
    - Update loyalty\_amount\_sum using + doc.loyalty\_amount.
  - For each item in doc.get(“items”).
    - Set item.rate from item.net\_rate.
    - Set item.amount from item.net\_amount.
    - Set item.base\_amount from item.base\_net\_amount.
    - Set item.price\_list\_rate from 0.
    - Set si\_item from map\_child\_doc(item, invoice, mapping(“doctype” → “Sales Invoice Item”, “field\_map” → mapping(“incoming\_rate” → “incoming\_rate”))).
    - Set si\_item.pos\_invoice from doc.name.
    - Set si\_item.pos\_invoice\_item from item.name.
    - If doc.is\_return.
      - Set reversed\_row from (reversed\_rows.get(item.pos\_invoice\_item) or Platform.\_dict()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in reversed\_rows.get(item.pos\_invoice\_item) → Platform.\_dict().
      - Set si\_item.sales\_invoice\_item from reversed\_row.get(“name”).
      - If si\_item.sales\_invoice\_item.
        - Set si\_item.rate from reversed\_row.rate.
    - If item.serial\_and\_batch\_bundle.
      - Set si\_item.serial\_and\_batch\_bundle from item.serial\_and\_batch\_bundle.
    - Evaluate items.append(si\_item).
    - Set old\_new\_item\_map at item.name from si\_item.
  - For each tax in doc.get(“taxes”).
    - Set found from false.
    - For each t in taxes.
      - If (t.account\_head equals tax.account\_head and t.cost\_center equals tax.cost\_center).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in t.account\_head equals tax.account\_head → t.cost\_center equals tax.cost\_center.
        - Set t.tax\_amount from (flt(t.tax\_amount) + flt(tax.tax\_amount\_after\_discount\_amount)).
        - Set t.base\_tax\_amount from (flt(t.base\_tax\_amount) + flt(tax.base\_tax\_amount\_after\_discount\_amount)).
        - Set old\_new\_tax\_map at tax.name from t.
        - Set found from true.
    - If not found.
      - Set tax.charge\_type from “Actual”.
      - Set tax.idx from idx.
      - Set tax.row\_id from no value.
      - Update idx using + 1.
      - Set tax.included\_in\_print\_rate from 0.
      - Set tax.tax\_amount from tax.tax\_amount\_after\_discount\_amount.
      - Set tax.base\_tax\_amount from tax.base\_tax\_amount\_after\_discount\_amount.
      - Set tax.dont\_recompute\_tax from 1.
      - Evaluate taxes.append(tax).
      - Set old\_new\_tax\_map at tax.name from tax.
  - For each payment in doc.get(“payments”).
    - Set found from false.
    - For each pay in payments.
      - If (pay.account equals payment.account and pay.mode\_of\_payment equals payment.mode\_of\_payment).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in pay.account equals payment.account → pay.mode\_of\_payment equals payment.mode\_of\_payment.
        - Set pay.amount from (flt(pay.amount) + flt(payment.amount)).
        - Set pay.base\_amount from (flt(pay.base\_amount) + flt(payment.base\_amount)).
        - Set found from true.
    - If not found.
      - Evaluate payments.append(payment).
  - For each d in (doc.get(“item\_wise\_tax\_details”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“item\_wise\_tax\_details”) → list().
    - Set row from Platform.\_dict(item = old\_new\_item\_map at d.item\_row, tax = old\_new\_tax\_map at d.tax\_row, amount = d.amount, rate = d.rate, …).
    - Evaluate item\_tax\_details.append(row).
- If loyalty\_points\_sum.
  - Set invoice.redeem\_loyalty\_points from 1.
  - Set invoice.loyalty\_points from loyalty\_points\_sum.
  - Set invoice.loyalty\_amount from loyalty\_amount\_sum.
- Evaluate invoice.set(“items”, items).
- Evaluate invoice.set(“payments”, payments).
- Evaluate invoice.set(“taxes”, taxes).
- Evaluate set\_summed\_amounts(invoice, data, list(“rounding\_adjustment”, “base\_rounding\_adjustment”, “rounded\_total”, “base\_rounded\_total”, …)).
- Set invoice.flags.keep\_change\_amount from true.
- Set invoice.additional\_discount\_percentage from 0.
- Set invoice.discount\_amount from 0.0.
- Set invoice.taxes\_and\_charges from no value.
- Set invoice.ignore\_pricing\_rule from 1.
- Set invoice.customer from self.customer.
- Set invoice.disable\_rounded\_total from cint(Platform.db.get\_value(“POS Profile”, invoice.pos\_profile, “disable\_rounded\_total”)).
- Set accounting\_dimensions from get\_checks\_for\_pl\_and\_bs\_accounts().
- Set accounting\_dimensions\_fields from list of d.fieldname for d drawn from accounting\_dimensions.
  - Draw d from accounting\_dimensions.
- Set dimension\_values from Platform.db.get\_value(“POS Profile”, mapping(“name” → invoice.pos\_profile), list(expanded accounting\_dimensions\_fields, “cost\_center”, “project”), as\_dict = 1).
- For each dimension in accounting\_dimensions.
  - Set dimension\_value from data at 0.get(dimension.fieldname) when data at 0.get(dimension.fieldname), otherwise dimension\_values.get(dimension.fieldname).
    - Value choice on data at 0.get(dimension.fieldname) — true gives data at 0.get(dimension.fieldname), false gives dimension\_values.get(dimension.fieldname).
  - If (not dimension\_value and (dimension.mandatory\_for\_pl or dimension.mandatory\_for\_bs)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not dimension\_value → (dimension.mandatory\_for\_pl or dimension.mandatory\_for\_bs).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in dimension.mandatory\_for\_pl → dimension.mandatory\_for\_bs.
    - Call the validation error handler Platform.throw(translated “Please set Accounting Dimension {} in {}”.format(Platform.bold(dimension.label), Platform.get\_desk\_link(“POS Profile”, invoice.pos\_profile))).
  - Evaluate invoice.set(dimension.fieldname, dimension\_value).
- Evaluate invoice.set(“cost\_center”, data at 0.get(“cost\_center”) when data at 0.get(“cost\_center”), otherwise dimension\_values.get(“cost\_center”)).
  - Value choice on data at 0.get(“cost\_center”) — true gives data at 0.get(“cost\_center”), false gives dimension\_values.get(“cost\_center”).
- Evaluate invoice.set(“project”, data at 0.get(“project”) when data at 0.get(“project”), otherwise dimension\_values.get(“project”)).
  - Value choice on data at 0.get(“project”) — true gives data at 0.get(“project”), false gives dimension\_values.get(“project”).
- If self.merge\_invoices\_based\_on equals “Customer Group”.
  - Set invoice.flags.ignore\_pos\_profile from true.
  - Set invoice.pos\_profile from empty text.
- Evaluate invoice.set(“sales\_partner”, no value).
- Evaluate invoice.set(“commission\_rate”, 0).
- Evaluate invoice.set(“total\_commission”, 0).
- Set invoice.\_item\_wise\_tax\_details from item\_tax\_details.
- Return invoice.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L567)

<a id="op-c77e7ffbdb1ceb"></a>
### POSInvoice Merge Log.get new sales invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_get_new_sales_invoice`

**Inputs** self.

**State and service calls** request new\_doc for “Sales Invoice”.

**Explicit results** sales\_invoice.

**Local steps**

- Set sales\_invoice from Platform.new\_doc(“Sales Invoice”).
- Set sales\_invoice.customer from self.customer.
- Set sales\_invoice.is\_pos from 1.
- Set sales\_invoice.posting\_date from no value.
- Set sales\_invoice.posting\_time from no value.
- Return sales\_invoice.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L3208) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L565)

<a id="op-a63450bd93be33"></a>
### POSInvoice Merge Log.update pos invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_update_point_of_sale_invoices`

**Inputs** self, invoice\_docs, sales\_invoice = empty text, credit\_notes = no value.

**State and service calls** call save on doc.

**Local steps**

- For each doc in invoice\_docs.
  - Evaluate doc.load\_from\_db().
  - Set inv from sales\_invoice.
  - If (doc.is\_return and credit\_notes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_return → credit\_notes.
    - For each tuple(key, value) in credit\_notes.items().
      - If doc.name belongs to value.
        - Set inv from key.
        - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate doc.update(mapping(“consolidated\_invoice” → no value when self.docstatus equals 2, otherwise inv)).
    - Value choice on self.docstatus equals 2 — true gives no value, false gives inv.
  - Evaluate doc.set\_status(update = true).
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L3350) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L573)

<a id="op-becb79b5ce70e8"></a>
### POSInvoice Merge Log.serial and batch bundle reference for pos invoice

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_serial_and_batch_bundle_reference_for_point_of_sale_invoice`

**Inputs** self.

**Record and data access** resolve a document from “POS Invoice” via get\_doc.

**Local steps**

- For each d in self.pos\_invoices.
  - Set pos\_invoice from Platform.get\_doc(“POS Invoice”, d.pos\_invoice).
  - For each table\_name in list(“items”, “packed\_items”).
    - Evaluate pos\_invoice.set\_serial\_and\_batch\_bundle(table\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L3670) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L572)

<a id="op-d586eb28d111ac"></a>
### POSInvoice Merge Log.delink serial and batch bundle

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_delink_serial_and_batch_bundle`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set bundles from self.get\_serial\_and\_batch\_bundles().
- If not bundles.
  - Return no value.
- Set sle\_table from Platform.qb.DocType(“Stock Ledger Entry”).
- Set query from nested operand in the contract.qb.update(sle\_table).set(sle\_table.serial\_and\_batch\_bundle, no value).where((sle\_table.serial\_and\_batch\_bundle.isin(bundles) bitwise and sle\_table.is\_cancelled) equals 1).
- Evaluate query.run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get serial and batch bundles](operations-081.md#op-074e45c428bb54).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L3819) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L563)

<a id="op-074e45c428bb54"></a>
### POSInvoice Merge Log.get serial and batch bundles

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_get_serial_and_batch_bundles`

**Inputs** self.

**Record and data access** read “POS Invoice Item” via get\_all.

**Explicit results** Platform.get\_all(“POS Invoice Item”, filters = mapping(“docstatus” → 1, “parent” → list(“in”, pos\_invoices), “serial\_and\_batch\_bundle” → list(“is”, “set”)), pluck = “serial\_and\_batch\_bundle”) · list().

**Local steps**

- Set pos\_invoices from list().
- For each d in self.pos\_invoices.
  - Evaluate pos\_invoices.append(d.pos\_invoice).
- If pos\_invoices.
  - Return Platform.get\_all(“POS Invoice Item”, filters = mapping(“docstatus” → 1, “parent” → list(“in”, pos\_invoices), “serial\_and\_batch\_bundle” → list(“is”, “set”)), pluck = “serial\_and\_batch\_bundle”).
- Return list().

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0125.json#L4069) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L566)

<a id="op-0658c0b2245625"></a>
### POSInvoice Merge Log.get consolidated credit notes

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_merge_log_pos_invoice_merge_log_posinvoicemergelog_get_consolidated_credit_notes`

**Inputs** self.

**Record and data access** read “POS Invoice” via get\_all.

**Explicit results** Platform.get\_all(“POS Invoice”, filters = mapping(“name” → list(“in”, list of d.pos\_invoice for d drawn from self.pos\_invoices), “is\_return” → 1, “consolidated\_invoice” → list(“is”, “set”)), pluck = “conso ….

**Local steps**

- Return Platform.get\_all(“POS Invoice”, filters = mapping(“name” → list(“in”, list of d.pos\_invoice for d drawn from self.pos\_invoices), “is\_return” → 1, “consolidated\_invoice” → list(“is”, “set”)), pluck = “conso ….
  - Draw d from self.pos\_invoices.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L249) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L887)

<a id="op-2d8f13b5e162b0"></a>
### POSInvoice Merge Log.cancel linked invoices

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_merge_log_business_behavior_point_of_sale_invoice_merge_log_cancel_linked_invoices`

**Inputs** self, credit\_notes.

**Record and data access** resolve a document from “Sales Invoice” via get\_doc.

**State and service calls** call cancel on si.

**Local steps**

- For each si\_name in list(expanded credit\_notes, self.consolidated\_invoice).
  - If not si\_name.
    - Continue with the next iteration or loop test.
  - Set si from Platform.get\_doc(“Sales Invoice”, si\_name).
  - Set si.flags.ignore\_validate from true.
  - Evaluate si.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L562)

<a id="op-5c09c9bd1e469f"></a>
### Set summed amounts

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_merge_log_pos_invoice_merge_log_set_summed_amounts`

**Inputs** invoice, data, fieldnames.

**Local steps**

- For each fieldname in fieldnames.
  - Evaluate invoice.set(fieldname, sum(generator of flt(doc.get(fieldname)) for doc drawn from data)).
    - Draw doc from data.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L252) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L890)
