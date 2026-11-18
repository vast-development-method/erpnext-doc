# Accounting and settlement · operations 103

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-39a1f171082386"></a>
### Sales Invoice.verify payment amount is negative

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_verify_payment_amount_is_negative`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0} (Payment Table): Amount must be negative”.format(entry.idx).

**Local steps**

- For each entry in self.payments.
  - <a id="op-39a1f171082386-guard-3"></a>If entry.amount &gt; 0.
    - Call the validation error handler Platform.throw(translated “Row #{0} (Payment Table): Amount must be negative”.format(entry.idx)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison entry.amount &gt; 0, entry.amount = 1 selects the branch that calls the validation-error handler with translated “Row #{0} (Payment Table): Amount must be negative”.format(entry.idx). With entry.amount = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-39a1f171082386-guard-3)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1061)

<a id="op-e0527769d43d3b"></a>
### Sales Invoice.make loyalty point entry

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_make_loyalty_point_entry`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Loyalty Point Entry”, “company” → self.company, “loyalty\_program” → lp\_details.loyalty\_program, “loyalty\_program\_tier” → lp\_details.tier\_name, …) via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set returned\_amount from self.get\_returned\_amount().
- Set current\_amount from (flt(self.grand\_total) − cint(self.loyalty\_amount)).
- Set eligible\_amount from (current\_amount − returned\_amount).
- Set lp\_details from get\_loyalty\_program\_details\_with\_points(self.customer, company = self.company, current\_transaction\_amount = current\_amount, loyalty\_program = self.loyalty\_program, expiry\_date = self.posting\_date, …).
- If (lp\_details and getdate(lp\_details.from\_date) ≤ getdate(self.posting\_date) and (not lp\_details.to\_date or getdate(lp\_details.to\_date) ≥ getdate(self.posting\_date))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lp\_details → getdate(lp\_details.from\_date) ≤ getdate(self.posting\_date) → (not lp\_details.to\_date or getdate(lp\_details.to\_date) ≥ getdate(self.posting\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not lp\_details.to\_date → getdate(lp\_details.to\_date) ≥ getdate(self.posting\_date).
  - Set collection\_factor from lp\_details.collection\_factor when lp\_details.collection\_factor, otherwise 1.0.
    - Value choice on lp\_details.collection\_factor — true gives lp\_details.collection\_factor, false gives 1.0.
  - Set points\_earned from cint((eligible\_amount ÷ collection\_factor)).
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Loyalty Point Entry”, “company” → self.company, “loyalty\_program” → lp\_details.loyalty\_program, “loyalty\_program\_tier” → lp\_details.tier\_name, …)).
    - Value choice on lp\_details.expiry\_duration — true gives add\_days(self.posting\_date, lp\_details.expiry\_duration), false gives NO\_EXPIRY\_DATE.
  - Set doc.flags.ignore\_permissions from 1.
  - Evaluate doc.save().
  - Evaluate self.set\_loyalty\_program\_tier().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get returned amount](operations-103.md#op-86c70bc8322fbd), [set loyalty program tier](operations-103.md#op-dac559a76b827d).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1032)

<a id="op-f8de9e8b8eb532"></a>
### Sales Invoice.delete loyalty point entry

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_delete_loyalty_point_entry`

**Inputs** self.

**Record and data access** execute query text (SELECT, Loyalty Point Entry).

**State and service calls** execute query text (DELETE, Loyalty Point Entry).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{} can't be cancelled since the Loyalty Points earned has been redeemed. First cancel the {} No {}”.format(self.doctype, self.doctype, invoice\_list).

**Local steps**

- Set lp\_entry from Platform.db.sql(query text (SELECT, Loyalty Point Entry), self.name, as\_dict = 1).
- If not lp\_entry.
  - Return no value.
- Set against\_lp\_entry from Platform.db.sql(query text (SELECT, Loyalty Point Entry), lp\_entry at 0.name, as\_dict = 1).
- If against\_lp\_entry.
  - Set invoice\_list from “, ”.join(list of d.invoice for d drawn from against\_lp\_entry).
    - Draw d from against\_lp\_entry.
  - Call the validation error handler Platform.throw(translated “{} can't be cancelled since the Loyalty Points earned has been redeemed. First cancel the {} No {}”.format(self.doctype, self.doctype, invoice\_list)).
- Otherwise.
  - Evaluate Platform.db.sql(query text (DELETE, Loyalty Point Entry), self.name).
  - Evaluate self.set\_loyalty\_program\_tier().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set loyalty program tier](operations-103.md#op-dac559a76b827d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1010)

<a id="op-dac559a76b827d"></a>
### Sales Invoice.set loyalty program tier

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_set_loyalty_program_tier`

**Inputs** self.

**Record and data access** resolve a document from “Customer” via get\_doc.

**State and service calls** call db\_set on customer.

**Local steps**

- Set lp\_details from get\_loyalty\_program\_details\_with\_points(self.customer, company = self.company, loyalty\_program = self.loyalty\_program, include\_expired\_entry = true).
- Set customer from Platform.get\_doc(“Customer”, self.customer).
- Evaluate customer.db\_set(“loyalty\_program\_tier”, lp\_details.tier\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1043)

<a id="op-86c70bc8322fbd"></a>
### Sales Invoice.get returned amount

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_returned_amount`

**Inputs** self.

**Explicit results** abs(returned\_amount at 0 at 0) when returned\_amount at 0 at 0, otherwise 0.

**Local steps**

- Bind dependencies Sum.
- Set doc from Platform.qb.DocType(self.doctype).
- Set returned\_amount from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.grand\_total)).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand i ….run().
- Return abs(returned\_amount at 0 at 0) when returned\_amount at 0 at 0, otherwise 0.
  - Value choice on returned\_amount at 0 at 0 — true gives abs(returned\_amount at 0 at 0), false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1023)

<a id="op-a2aff537441670"></a>
### Sales Invoice.apply loyalty points

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_apply_loyalty_points`

**Inputs** self.

**Record and data access** resolve a document from mapping(“doctype” → “Loyalty Point Entry”, “company” → self.company, “loyalty\_program” → self.loyalty\_program, “loyalty\_program\_tier” → lp\_entry.loyalty\_program\_tier, …) via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Bind dependencies get\_loyalty\_point\_entries, get\_redemption\_details.
- Set loyalty\_point\_entries from get\_loyalty\_point\_entries(self.customer, self.loyalty\_program, self.company, self.posting\_date).
- Set redemption\_details from get\_redemption\_details(self.customer, self.loyalty\_program, self.company).
- Set points\_to\_redeem from self.loyalty\_points.
- For each lp\_entry in loyalty\_point\_entries.
  - If lp\_entry.invoice equals self.name.
    - Continue with the next iteration or loop test.
  - Set available\_points from (lp\_entry.loyalty\_points − flt(redemption\_details.get(lp\_entry.name))).
  - If available\_points &gt; points\_to\_redeem.
    - Set redeemed\_points from points\_to\_redeem.
  - Otherwise.
    - Set redeemed\_points from available\_points.
  - Set doc from Platform.get\_doc(mapping(“doctype” → “Loyalty Point Entry”, “company” → self.company, “loyalty\_program” → self.loyalty\_program, “loyalty\_program\_tier” → lp\_entry.loyalty\_program\_tier, …)).
  - Set doc.flags.ignore\_permissions from 1.
  - Evaluate doc.save().
  - Update points\_to\_redeem using − redeemed\_points.
  - If points\_to\_redeem &lt; 1.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1003)

<a id="op-83586bcd294ed4"></a>
### Sales Invoice.counts coupon use

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_counts_coupon_use`

**Inputs** self.

**Explicit results** false · true · any(generator of coupon\_order\_items.get(item.so\_detail) differs from item.sales\_order for item drawn from self.items).

**Local steps**

- If (self.is\_return or self.get(“is\_consolidated”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → self.get(“is\_consolidated”).
  - Return false.
- If (not self.items or any(generator of (not nested operand in the contract.get(“sales\_order”) or not nested operand in the contract.get(“so\_detail”)) for item drawn from self.items)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.items → any(generator of (not item.get(“sales\_order”) or not item.get(“so\_detail”)) for item drawn from self.items).
  - Draw item from self.items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(“sales\_order”) → not item.get(“so\_detail”).
  - Return true.
- Set order from Platform.qb.DocType(“Sales Order”).
- Set order\_item from Platform.qb.DocType(“Sales Order Item”).
- Set coupon\_order\_items from dict(nested operand in the contract.select(nested operand in the contract.name, nested operand in the contract.parent).where((((nested operand in the contract bitwise and nested operand in the contract) bi ….
  - Draw item from self.items.
- Return any(generator of coupon\_order\_items.get(item.so\_detail) differs from item.sales\_order for item drawn from self.items).
  - Draw item from self.items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1009)

<a id="op-606a81fc949758"></a>
### Sales Invoice.set status

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_set_status`

**Inputs** self, update = false, status = no value, update\_modified = true.

**Record and data access** read “Sales Invoice” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - If self.get(“amended\_from”).
    - Set self.status from “Draft”.
  - Return no value.
- Set outstanding\_amount from flt(self.outstanding\_amount, self.precision(“outstanding\_amount”)).
- Set total from get\_total\_in\_party\_account\_currency(self).
- If not status.
  - If self.docstatus equals 2.
    - Set status from “Cancelled”.
  - Otherwise.
    - If self.docstatus equals 1.
      - If self.is\_internal\_transfer().
        - Set self.status from “Internal Transfer”.
      - Otherwise.
        - If is\_overdue(self, total).
          - Set self.status from “Overdue”.
        - Otherwise.
          - If 0 &lt; outstanding\_amount &lt; total.
            - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; outstanding\_amount &lt; total.
            - Set self.status from “Partly Paid”.
          - Otherwise.
            - If (outstanding\_amount &gt; 0 and getdate(self.due\_date) ≥ getdate()).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in outstanding\_amount &gt; 0 → getdate(self.due\_date) ≥ getdate().
              - Set self.status from “Unpaid”.
            - Otherwise.
              - If (self.is\_return equals 0 and Platform.db.get\_value(“Sales Invoice”, mapping(“is\_return” → 1, “return\_against” → self.name, “docstatus” → 1))).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return equals 0 → Platform.db.get\_value(“Sales Invoice”, mapping(“is\_return” → 1, “return\_against” → self.name, “docstatus” → 1)).
                - Set self.status from “Credit Note Issued”.
              - Otherwise.
                - If self.is\_return equals 1.
                  - Set self.status from “Return”.
                - Otherwise.
                  - <a id="op-606a81fc949758-guard-29"></a>If outstanding\_amount ≤ 0.
                    - Set self.status from “Paid”.
                  - Otherwise.
                    - Set self.status from “Submitted”.
      - If (self.status belongs to tuple(“Unpaid”, “Partly Paid”, “Overdue”) and self.is\_discounted and get\_discounting\_status(self.name) equals “Disbursed”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status belongs to tuple(“Unpaid”, “Partly Paid”, “Overdue”) → self.is\_discounted → get\_discounting\_status(self.name) equals “Disbursed”.
        - Update self.status using + “ and Discounted”.
    - Otherwise.
      - Set self.status from “Draft”.
- If update.
  - Evaluate self.db\_set(“status”, self.status, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison outstanding\_amount ≤ 0, outstanding\_amount = 0 selects the branch that assigns “Paid” to self.status. With outstanding\_amount = 1, the alternative assigns “Submitted” to self.status. [Local guard](#op-606a81fc949758-guard-29)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1042) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1172)

<a id="op-50791cd041e573"></a>
### Sales Invoice.is subcontracted

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_is_subcontracted`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Sales Order” via exists.

**Explicit results** self.has\_subcontracted.

**Local steps**

- Set sales\_orders from list of item.sales\_order for item drawn from self.items where item.sales\_order.
  - Draw item from self.items, keep a combination only if (item.sales\_order).
- If (not self.has\_subcontracted and sales\_orders).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.has\_subcontracted → sales\_orders.
  - Set self.has\_subcontracted from bool(Platform.db.exists(“Sales Order”, mapping(“name” → list(“in”, sales\_orders), “is\_subcontracted” → 1))).
- If self.has\_subcontracted.
  - Set self.update\_stock from 0.
- Return self.has\_subcontracted.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1027) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1157)

<a id="op-cf37890d2b1998"></a>
### Get total in party account currency

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_total_in_party_account_currency`

**Inputs** doc.

**Explicit results** flt(doc.get(total\_fieldname), doc.precision(total\_fieldname)).

**Local steps**

- Set total\_fieldname from “grand\_total” when doc.disable\_rounded\_total, otherwise “rounded\_total”.
  - Value choice on doc.disable\_rounded\_total — true gives “grand\_total”, false gives “rounded\_total”.
- If doc.party\_account\_currency differs from doc.currency.
  - Set total\_fieldname from (“base\_” + total\_fieldname).
- Return flt(doc.get(total\_fieldname), doc.precision(total\_fieldname)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L988)

<a id="op-ea7b420189eeb0"></a>
### Is overdue

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_is_overdue`

**Inputs** doc, total.

**Explicit results** no value · getdate(doc.due\_date) &lt; today · flt((total − outstanding\_amount), doc.precision(“outstanding\_amount”)) &lt; payable\_amount.

**Local steps**

- Set outstanding\_amount from flt(doc.outstanding\_amount, doc.precision(“outstanding\_amount”)).
- <a id="op-ea7b420189eeb0-guard-3"></a>If outstanding\_amount ≤ 0.
  - Return no value.
- Set today from getdate().
- If (doc.get(“is\_pos”) or not doc.get(“payment\_schedule”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“is\_pos”) → not doc.get(“payment\_schedule”).
  - Return getdate(doc.due\_date) &lt; today.
- Set payment\_amount\_field from “base\_payment\_amount” when doc.party\_account\_currency differs from doc.currency, otherwise “payment\_amount”.
  - Value choice on doc.party\_account\_currency differs from doc.currency — true gives “base\_payment\_amount”, false gives “payment\_amount”.
- Set payable\_amount from flt(sum(generator of payment.get(payment\_amount\_field) for payment drawn from doc.payment\_schedule where getdate(payment.due\_date) &lt; today), doc.precision(“outstanding\_amount”)).
  - Draw payment from doc.payment\_schedule, keep a combination only if (getdate(payment.due\_date) &lt; today).
- Return flt((total − outstanding\_amount), doc.precision(“outstanding\_amount”)) &lt; payable\_amount.

**Derived branch illustrations**

- At the comparison outstanding\_amount ≤ 0, outstanding\_amount = 0 selects the branch that returns no value. With outstanding\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-ea7b420189eeb0-guard-3)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L989)

<a id="op-8619472d629084"></a>
### Get discounting status

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_discounting_status`

**Inputs** sales\_invoice.

**Record and data access** execute query text (SELECT, Invoice Discounting).

**Explicit results** status.

**Local steps**

- Set status from no value.
- Set invoice\_discounting\_list from Platform.db.sql(query text (SELECT, Invoice Discounting), sales\_invoice).
- For each d in invoice\_discounting\_list.
  - Set status from d at 0.
  - If status equals “Disbursed”.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return status.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L977)

<a id="op-52b7aa050f0660"></a>
### Validate inter company party

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_validate_inter_company_party`

**Inputs** doctype, party, company, inter\_company\_reference.

**Record and data access** resolve a document from ref\_doc via get\_doc · read partytype via get\_value · read ref\_partytype via get\_cached\_value · read “Allowed To Transact With” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Invalid {0} for Inter Company Transaction.”.format(translated partytype) · validation helper — translated “Invalid Company for Inter Company Transaction.” · validation helper — translated “{0} not allowed to transact with {1}. Please change the Company or add the Company in the 'Allowed To Transa …”.format(translated partytype, company).

**Local steps**

- If not party.
  - Return no value.
- If doctype belongs to list(“Sales Invoice”, “Sales Order”).
  - Set tuple(partytype, ref\_partytype, internal) from tuple(“Customer”, “Supplier”, “is\_internal\_customer”).
  - If doctype equals “Sales Invoice”.
    - Set ref\_doc from “Purchase Invoice”.
  - Otherwise.
    - Set ref\_doc from “Purchase Order”.
- Otherwise.
  - Set tuple(partytype, ref\_partytype, internal) from tuple(“Supplier”, “Customer”, “is\_internal\_supplier”).
  - If doctype equals “Purchase Invoice”.
    - Set ref\_doc from “Sales Invoice”.
  - Otherwise.
    - Set ref\_doc from “Sales Order”.
- If inter\_company\_reference.
  - Set doc from Platform.get\_doc(ref\_doc, inter\_company\_reference).
  - Set ref\_party from doc.supplier when doctype belongs to list(“Sales Invoice”, “Sales Order”), otherwise doc.customer.
    - Value choice on doctype belongs to list(“Sales Invoice”, “Sales Order”) — true gives doc.supplier, false gives doc.customer.
  - If Platform.db.get\_value(partytype, mapping(“represents\_company” → doc.company, “disabled” → 0), “name”) differs from party.
    - Call the validation error handler Platform.throw(translated “Invalid {0} for Inter Company Transaction.”.format(translated partytype)).
  - If Platform.get\_cached\_value(ref\_partytype, ref\_party, “represents\_company”) differs from company.
    - Call the validation error handler Platform.throw(translated “Invalid Company for Inter Company Transaction.”).
- Otherwise.
  - If Platform.db.get\_value(partytype, mapping(“name” → party, internal → 1), “name”) equals party.
    - Set companies from Platform.get\_all(“Allowed To Transact With”, fields = list(“company”), filters = mapping(“parenttype” → partytype, “parent” → party)).
    - Set companies from list of d.company for d drawn from companies.
      - Draw d from companies.
    - If company does not belong to companies.
      - Call the validation error handler Platform.throw(translated “{0} not allowed to transact with {1}. Please change the Company or add the Company in the 'Allowed To Transa …”.format(translated partytype, company)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(ref\_partytype, ref\_party, “represents\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1072)

<a id="op-0b5d70b44834cd"></a>
### Get inter company counterpart

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_inter_company_counterpart`

**Inputs** doctype.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(ref\_doc, “inter\_company\_invoice\_reference”) · tuple(ref\_doc, “inter\_company\_order\_reference”).

**Local steps**

- If doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Set ref\_doc from “Purchase Invoice” when doctype equals “Sales Invoice”, otherwise “Sales Invoice”.
    - Value choice on doctype equals “Sales Invoice” — true gives “Purchase Invoice”, false gives “Sales Invoice”.
  - Return tuple(ref\_doc, “inter\_company\_invoice\_reference”).
- Set ref\_doc from “Purchase Order” when doctype equals “Sales Order”, otherwise “Sales Order”.
  - Value choice on doctype equals “Sales Order” — true gives “Purchase Order”, false gives “Sales Order”.
- Return tuple(ref\_doc, “inter\_company\_order\_reference”).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L978)

<a id="op-177a8ee1937fde"></a>
### Update linked doc

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_linked_doc`

**Inputs** doctype, name, inter\_company\_reference.

**State and service calls** request set\_value on ref\_doc.

**Local steps**

- Set tuple(ref\_doc, ref\_field) from get\_inter\_company\_counterpart(doctype).
- If inter\_company\_reference.
  - Evaluate Platform.db.set\_value(ref\_doc, inter\_company\_reference, ref\_field, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1066)

<a id="op-b84d945ce735ad"></a>
### Unlink inter company doc

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_unlink_inter_company_doc`

**Inputs** doctype, name, inter\_company\_reference.

**Record and data access** read ref\_doc via get\_value · read doctype via get\_value.

**State and service calls** request set\_value on doctype · request set\_value on ref\_doc.

**Explicit results** no value.

**Local steps**

- Set tuple(ref\_doc, ref\_field) from get\_inter\_company\_counterpart(doctype).
- If not inter\_company\_reference.
  - Return no value.
- Evaluate Platform.db.set\_value(doctype, name, ref\_field, empty text).
- If Platform.db.get\_value(ref\_doc, inter\_company\_reference, ref\_field) differs from name.
  - Return no value.
- Set remaining\_counterpart from Platform.db.get\_value(doctype, mapping(ref\_field → inter\_company\_reference, “docstatus” → 1)).
- Evaluate Platform.db.set\_value(ref\_doc, inter\_company\_reference, ref\_field, (remaining\_counterpart or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in remaining\_counterpart → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1064)

<a id="op-445be37682f8c9"></a>
### Get list context

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies get\_list\_context.
- Set list\_context from get\_list\_context(context).
- Evaluate list\_context.update(mapping(“show\_sidebar” → true, “show\_search” → true, “no\_breadcrumbs” → true, “title” → translated “Invoices”, …)).
- Return list\_context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L3419) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1139)

<a id="op-d72d25afd68186"></a>
### Get bank cash account

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_get_bank_cash_account`

**Inputs** mode\_of\_payment, company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Mode of Payment Account” via get\_value.

**Explicit results** mapping(“account” → account).

**Explicit failure paths** validation helper — translated “Please set default Cash or Bank account in Mode of Payment {0}”.format(get\_link\_to\_form(“Mode of Payment”, mode\_of\_payment)).

**Local steps**

- Set account from Platform.db.get\_value(“Mode of Payment Account”, mapping(“parent” → mode\_of\_payment, “company” → company), “default\_account”).
- If not account.
  - Call the validation error handler Platform.throw(translated “Please set default Cash or Bank account in Mode of Payment {0}”.format(get\_link\_to\_form(“Mode of Payment”, mode\_of\_payment)), title = translated “Missing Account”).
- Return mapping(“account” → account).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1138)

<a id="op-d1810f9b38959a"></a>
### Make maintenance schedule

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_maintenance_schedule`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Set doclist from get\_mapped\_doc(“Sales Invoice”, source\_name, mapping(“Sales Invoice” → mapping(“doctype” → “Maintenance Schedule”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Sales Invoice Item” → mapping(“docty ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1000)

<a id="op-47770f3d911822"></a>
### Make delivery note

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_delivery_note`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind local operation set\_missing\_values for subsequent calls.
- Bind local operation update\_item for subsequent calls.
- Set doclist from get\_mapped\_doc(“Sales Invoice”, source\_name, mapping(“Sales Invoice” → mapping(“doctype” → “Delivery Note”, “validation” → mapping(“docstatus” → list(“=”, 1))), “Sales Invoice Item” → mapping(“doctype” → “ ….
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L990)

<a id="op-f887f3e6294e65"></a>
### Make delivery note.set missing values

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_delivery_note_set_missing_values`

**Inputs** source, target.

**Local steps**

- Evaluate target.run\_method(“set\_missing\_values”).
- Evaluate target.run\_method(“set\_po\_nos”).
- Evaluate target.run\_method(“calculate\_taxes\_and\_totals”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from target.run\_method(“set\_missing\_values”), target.run\_method(“set\_po\_nos”) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L991)

<a id="op-420507d27b8759"></a>
### Make delivery note.update item

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_delivery_note_update_item`

**Inputs** source\_doc, target\_doc, source\_parent.

**Local steps**

- Set target\_doc.qty from (flt(source\_doc.qty) − flt(source\_doc.delivered\_qty)).
- Set target\_doc.stock\_qty from (target\_doc.qty × flt(source\_doc.conversion\_factor)).
- Set target\_doc.base\_amount from (target\_doc.qty × flt(source\_doc.base\_rate)).
- Set target\_doc.amount from (target\_doc.qty × flt(source\_doc.rate)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L992)

<a id="op-c72bcc6434b05f"></a>
### Make sales return

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_make_sales_return`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“Sales Invoice”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“Sales Invoice”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1001)

<a id="op-5590bc2b409e41"></a>
### Get inter company details

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_inter_company_details`

**Inputs** doc, doctype.

**Record and data access** read “Supplier” via get\_all · read “Customer” via get\_cached\_value · read “Customer” via get\_all · read “Supplier” via get\_cached\_value.

**Explicit results** mapping(“party” → party, “company” → company).

**Explicit failure paths** validation helper — translated “No Supplier found for Inter Company Transactions which represents company {0}”.format(Platform.bold(doc.company)) · validation helper — translated “No Customer found for Inter Company Transactions which represents company {0}”.format(Platform.bold(doc.company)).

**Local steps**

- If doctype belongs to list(“Sales Invoice”, “Sales Order”, “Delivery Note”).
  - Set parties from Platform.db.get\_all(“Supplier”, fields = list(“name”), filters = mapping(“disabled” → 0, “is\_internal\_supplier” → 1, “represents\_company” → doc.company)).
  - Set company from Platform.get\_cached\_value(“Customer”, doc.customer, “represents\_company”).
  - If not parties.
    - Call the validation error handler Platform.throw(translated “No Supplier found for Inter Company Transactions which represents company {0}”.format(Platform.bold(doc.company))).
  - Set party from get\_internal\_party(parties, “Supplier”, doc).
- Otherwise.
  - Set parties from Platform.db.get\_all(“Customer”, fields = list(“name”), filters = mapping(“disabled” → 0, “is\_internal\_customer” → 1, “represents\_company” → doc.company)).
  - Set company from Platform.get\_cached\_value(“Supplier”, doc.supplier, “represents\_company”).
  - If not parties.
    - Call the validation error handler Platform.throw(translated “No Customer found for Inter Company Transactions which represents company {0}”.format(Platform.bold(doc.company))).
  - Set party from get\_internal\_party(parties, “Customer”, doc).
- Return mapping(“party” → party, “company” → company).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer”, doc.customer, “represents\_company”), Platform.get\_cached\_value(“Supplier”, doc.supplier, “represents\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L979)
