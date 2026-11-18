# Shared transaction rules · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-0ca6471b6c3f63"></a>
### Validate cost center

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_cost_center`

**Inputs** tax, doc.

**Record and data access** read “Cost Center” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Cost Center {1} does not belong to Company {2}”.format(tax.idx, Platform.bold(tax.cost\_center), Platform.bold(doc.company)).

**Local steps**

- If not tax.cost\_center.
  - Return no value.
- Set company from Platform.get\_cached\_value(“Cost Center”, tax.cost\_center, “company”).
- If company differs from doc.company.
  - Call the validation error handler Platform.throw(translated “Row {0}: Cost Center {1} does not belong to Company {2}”.format(tax.idx, Platform.bold(tax.cost\_center), Platform.bold(doc.company)), title = translated “Invalid Cost Center”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Cost Center”, tax.cost\_center, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1026) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L266)

<a id="op-ee98a327a7e627"></a>
### Validate inclusive tax

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_inclusive_tax`

**Inputs** tax, doc.

**Explicit failure paths** validation helper — translated “Valuation type charges can not be marked as Inclusive”.

**Local steps**

- Bind local operation \_on\_previous\_row\_error for subsequent calls.
- If cint(getattr(tax, “included\_in\_print\_rate”, no value)).
  - If tax.charge\_type equals “Actual”.
    - Evaluate throw(translated “Charge of type 'Actual' in row {0} cannot be included in Item Rate or Paid Amount”.format(tax.idx)).
  - Otherwise.
    - If (tax.charge\_type equals “On Previous Row Amount” and not cint(nested operand in the contract.get(“taxes”) at (nested operand in the contract(nested operand in the contract) − 1).included\_in\_print\_rate)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “On Previous Row Amount” → not cint(doc.get(“taxes”) at (cint(nested operand in the contract.row\_id) − 1).included\_in\_print\_rate).
      - Evaluate \_on\_previous\_row\_error(tax.row\_id).
    - Otherwise.
      - If (tax.charge\_type equals “On Previous Row Total” and not all(list of cint(t.included\_in\_print\_rate) for t drawn from nested operand in the contract.get(“taxes”) at slice no value to nested operand in the co ….
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type equals “On Previous Row Total” → not all(list of cint(t.included\_in\_print\_rate) for t drawn from doc.get(“taxes”) at slice no value to cint(nested operand in the contract.row\_id)).
        - Draw t from doc.get(“taxes”) at slice no value to cint(tax.row\_id).
        - Evaluate \_on\_previous\_row\_error((“1 - %d” modulo or format tuple(tax.row\_id))).
      - Otherwise.
        - If tax.get(“category”) equals “Valuation”.
          - Call the validation error handler Platform.throw(translated “Valuation type charges can not be marked as Inclusive”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(tax, “included\_in\_print\_rate”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1028) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L268)

<a id="op-2c4cbac58b7975"></a>
### Validate inclusive tax.on previous row error

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_inclusive_tax_on_previous_row_error`

**Inputs** row\_range.

**Local steps**

- Evaluate throw(translated “To include tax in row {0} in Item rate, taxes in rows {1} must also be included”.format(tax.idx, row\_range)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1029) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L269)

<a id="op-70b4567211ff36"></a>
### Is deduct with valuation

`operation_enterprise_binding_enterprise_controllers_accounts_controller_is_deduct_with_valuation`

**Inputs** tax.

**Declared result** bool.

**Explicit results** (tax.get(“category”) equals “Valuation” and tax.get(“add\_deduct\_tax”) equals “Deduct”).

**Local steps**

- Return (tax.get(“category”) equals “Valuation” and tax.get(“add\_deduct\_tax”) equals “Deduct”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.get(“category”) equals “Valuation” → tax.get(“add\_deduct\_tax”) equals “Deduct”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L998) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L238)

<a id="op-4601b8ad5b30ab"></a>
### Validate deduct with valuation category

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_deduct_with_valuation_category`

**Inputs** taxes, allowed\_account\_heads = no value.

**Declared result** no value.

**Local steps**

- For each tax in (taxes or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in taxes → list().
  - If (is\_deduct\_with\_valuation(tax) and tax.account\_head does not belong to (allowed\_account\_heads or set())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_deduct\_with\_valuation(tax) → tax.account\_head does not belong to (allowed\_account\_heads or set()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in allowed\_account\_heads → set().
    - Evaluate throw(translated “Row {0}: {1} cannot be {2} when {3} is {4}”.format(tax.idx, Platform.bold(translated “Add or Deduct”), Platform.bold(translated “Deduct”), Platform.bold(translated “Consider Tax or Charge ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1027) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L267)

<a id="op-22853c419c210a"></a>
### Set balance in account currency

`operation_enterprise_binding_enterprise_controllers_accounts_controller_set_balance_in_account_currency`

**Inputs** gl\_dict, account\_currency = no value, conversion\_rate = no value, company\_currency = no value.

**Explicit failure paths** validation helper — translated “Account: {0} with currency: {1} can not be selected”.format(gl\_dict.account, account\_currency).

**Local steps**

- If (not conversion\_rate and account\_currency differs from company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not conversion\_rate → account\_currency differs from company\_currency.
  - Call the validation error handler Platform.throw(translated “Account: {0} with currency: {1} can not be selected”.format(gl\_dict.account, account\_currency)).
- Set gl\_dict at “account\_currency” from account\_currency.
- If (flt(gl\_dict.debit) and not flt(gl\_dict.debit\_in\_account\_currency)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(gl\_dict.debit) → not flt(gl\_dict.debit\_in\_account\_currency).
  - Set gl\_dict.debit\_in\_account\_currency from gl\_dict.debit when account\_currency equals company\_currency, otherwise flt((gl\_dict.debit ÷ conversion\_rate), 2).
    - Value choice on account\_currency equals company\_currency — true gives gl\_dict.debit, false gives flt((gl\_dict.debit ÷ conversion\_rate), 2).
- If (flt(gl\_dict.credit) and not flt(gl\_dict.credit\_in\_account\_currency)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(gl\_dict.credit) → not flt(gl\_dict.credit\_in\_account\_currency).
  - Set gl\_dict.credit\_in\_account\_currency from gl\_dict.credit when account\_currency equals company\_currency, otherwise flt((gl\_dict.credit ÷ conversion\_rate), 2).
    - Value choice on account\_currency equals company\_currency — true gives gl\_dict.credit, false gives flt((gl\_dict.credit ÷ conversion\_rate), 2).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L242)

<a id="op-c7d1165b3dd664"></a>
### Get advance journal entries

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_advance_journal_entries`

**Inputs** party\_type, party, party\_account, amount\_field, order\_doctype, order\_list, include\_unallocated = true.

**Explicit results** list(journal\_entries).

**Local steps**

- Set journal\_entry from Platform.qb.DocType(“Journal Entry”).
- Set journal\_acc from Platform.qb.DocType(“Journal Entry Account”).
- Set q from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(ConstantColumn(“Journal Entry”).as\_(“reference\_typ ….
- If party\_type equals “Customer”.
  - Set q from q.where(journal\_acc.credit\_in\_account\_currency &gt; 0).
- Otherwise.
  - Set q from q.where(journal\_acc.debit\_in\_account\_currency &gt; 0).
- Set reference\_or\_condition from list().
- If include\_unallocated.
  - Evaluate reference\_or\_condition.append(journal\_acc.reference\_name.isnull()).
  - Evaluate reference\_or\_condition.append(journal\_acc.reference\_name equals empty text).
- If order\_list.
  - Evaluate reference\_or\_condition.append((journal\_acc.reference\_type equals order\_doctype bitwise and journal\_acc.reference\_name.isin(order\_list))).
- If reference\_or\_condition.
  - Set q from q.where(Criterion.any(reference\_or\_condition)).
- Set q from q.orderby(journal\_entry.posting\_date).
- Set journal\_entries from q.run(as\_dict = true).
- Return list(journal\_entries).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L221)

<a id="op-ed05134cb98bed"></a>
### Get advance payment entries for regional

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_advance_payment_entries_for_regional`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** get\_advance\_payment\_entries(expanded args, expanded names kwargs).

**Local steps**

- Return get\_advance\_payment\_entries(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L223)

<a id="op-7e4983045c679b"></a>
### Get advance payment entries

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_advance_payment_entries`

**Inputs** party\_type, party, party\_account, order\_doctype, order\_list = no value, default\_advance\_account = no value, include\_unallocated = true, against\_all\_orders = false, limit = no value, condition = no value.

**Explicit results** payment\_entries.

**Local steps**

- Set payment\_entries from list().
- Set payment\_entry from Platform.qb.DocType(“Payment Entry”).
- If (order\_list or against\_all\_orders).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in order\_list → against\_all\_orders.
  - Set q from get\_common\_query(party\_type, party, party\_account, default\_advance\_account, …).
  - Set payment\_ref from Platform.qb.DocType(“Payment Entry Reference”).
  - Set q from q.inner\_join(payment\_ref).on(payment\_entry.name equals payment\_ref.parent).
  - Set q from q.select(payment\_ref.allocated\_amount.as\_(“amount”), payment\_ref.name.as\_(“reference\_row”), payment\_ref.reference\_name.as\_(“against\_order”), payment\_entry.book\_advance\_payments\_in\_separate\_party\_account).
  - Set q from q.where(payment\_ref.reference\_doctype equals order\_doctype).
  - If order\_list.
    - Set q from q.where(payment\_ref.reference\_name.isin(order\_list)).
  - Set allocated from list(q.run(as\_dict = true)).
  - Update payment\_entries using + allocated.
- If include\_unallocated.
  - Set q from get\_common\_query(party\_type, party, party\_account, default\_advance\_account, …).
  - Set q from q.select(payment\_entry.unallocated\_amount.as\_(“amount”)).
  - Set q from q.where(payment\_entry.unallocated\_amount &gt; 0).
  - Set unallocated from list(q.run(as\_dict = true)).
  - Update payment\_entries using + unallocated.
- Return payment\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L222)

<a id="op-1e70faa41fdf9f"></a>
### Get common query

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_common_query`

**Inputs** party\_type, party, party\_account, default\_advance\_account, limit, condition.

**Record and data access** read “Party Type” via get\_value.

**Explicit results** q.

**Local steps**

- Set account\_type from Platform.db.get\_value(“Party Type”, party\_type, “account\_type”).
- Set payment\_type from “Receive” when account\_type equals “Receivable”, otherwise “Pay”.
  - Value choice on account\_type equals “Receivable” — true gives “Receive”, false gives “Pay”.
- Set payment\_entry from Platform.qb.DocType(“Payment Entry”).
- Set q from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.party\_type equals party\_type).where(payment\_entry.party equals party).where(payment\_entry.docstatus equals 1).
- Set field from “paid\_from” when payment\_type equals “Receive”, otherwise “paid\_to”.
  - Value choice on payment\_type equals “Receive” — true gives “paid\_from”, false gives “paid\_to”.
- Set q from q.select(payment\_entry at formatted text {field}\_account\_currency.as\_(“currency”)).
- Set q from q.select(payment\_entry at field).
- Set account\_condition from payment\_entry at field.isin(party\_account).
- If default\_advance\_account.
  - Set q from q.where((account\_condition bitwise or (payment\_entry at field equals default\_advance\_account bitwise and payment\_entry.book\_advance\_payments\_in\_separate\_party\_account equals 1))).
- Otherwise.
  - Set q from q.where(account\_condition).
- If payment\_type equals “Receive”.
  - Set q from q.select(payment\_entry.source\_exchange\_rate.as\_(“exchange\_rate”)).
- Otherwise.
  - Set q from q.select(payment\_entry.target\_exchange\_rate.as\_(“exchange\_rate”)).
- If condition.
  - Set common\_filter\_conditions from list().
  - Evaluate common\_filter\_conditions.append(payment\_entry.company equals condition at “company”).
  - If condition.get(“name”, no value).
    - Evaluate common\_filter\_conditions.append(payment\_entry.name.like(formatted text %{condition.get(“name”)}%)).
  - If condition.get(“from\_payment\_date”).
    - Evaluate common\_filter\_conditions.append(payment\_entry.posting\_date.gte(condition at “from\_payment\_date”)).
  - If condition.get(“to\_payment\_date”).
    - Evaluate common\_filter\_conditions.append(payment\_entry.posting\_date.lte(condition at “to\_payment\_date”)).
  - If condition.get(“get\_payments”) is identical to true.
    - If condition.get(“cost\_center”).
      - Evaluate common\_filter\_conditions.append(payment\_entry.cost\_center equals condition at “cost\_center”).
    - If condition.get(“accounting\_dimensions”).
      - Set apply\_strict\_user\_permissions from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).
      - For each tuple(field, val) in condition.get(“accounting\_dimensions”).items().
        - If isinstance(val, ((list bitwise or tuple) bitwise or set)).
          - Set value\_condition from payment\_entry at field.isin(val).
          - If apply\_strict\_user\_permissions.
            - Evaluate common\_filter\_conditions.append(value\_condition).
          - Otherwise.
            - Evaluate common\_filter\_conditions.append((IfNull(payment\_entry at field, empty text) equals empty text bitwise or value\_condition)).
        - Otherwise.
          - Evaluate common\_filter\_conditions.append(payment\_entry at field equals val).
    - If condition.get(“minimum\_payment\_amount”).
      - Evaluate common\_filter\_conditions.append(payment\_entry.unallocated\_amount.gte(condition at “minimum\_payment\_amount”)).
    - If condition.get(“maximum\_payment\_amount”).
      - Evaluate common\_filter\_conditions.append(payment\_entry.unallocated\_amount.lte(condition at “maximum\_payment\_amount”)).
  - Set q from q.where(Criterion.all(common\_filter\_conditions)).
- Set q from q.orderby(payment\_entry.posting\_date).
- Set q from q.limit(limit) when limit, otherwise q.
  - Value choice on limit — true gives q.limit(limit), false gives q.
- Return q.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L224)

<a id="op-3595d1755b2178"></a>
### Update invoice status

`operation_enterprise_controllers_accounts_controller_business_behavior_update_invoice_status`

**Inputs** no declared parameters.

**Local steps**

- Set today from getdate().
- Set payment\_schedule from Platform.qb.DocType(“Payment Schedule”).
- For each doctype in tuple(“Sales Invoice”, “Purchase Invoice”).
  - Set invoice from Platform.qb.DocType(doctype).
  - Set consider\_base\_amount from invoice.party\_account\_currency differs from invoice.currency.
  - Set payment\_amount from nested operand in the contract.terms.Case().when(consider\_base\_amount, payment\_schedule.base\_payment\_amount).else\_(payment\_schedule.payment\_amount).
  - Set payable\_amount from nested operand in the contract.qb.from\_(payment\_schedule).select(Sum(payment\_amount)).where((payment\_schedule.parent equals invoice.name bitwise and payment\_schedule.due\_date &lt; today)).
  - Set total from nested operand in the contract.terms.Case().when(invoice.disable\_rounded\_total, invoice.grand\_total).else\_(invoice.rounded\_total).
  - Set base\_total from nested operand in the contract.terms.Case().when(invoice.disable\_rounded\_total, invoice.base\_grand\_total).else\_(invoice.base\_rounded\_total).
  - Set total\_amount from nested operand in the contract.terms.Case().when(consider\_base\_amount, base\_total).else\_(total).
  - Set is\_overdue from (total\_amount − invoice.outstanding\_amount) &lt; payable\_amount.
  - Set conditions from (((invoice.docstatus equals 1 bitwise and invoice.outstanding\_amount &gt; 0) bitwise and (invoice.status.like(“Unpaid%”) bitwise or invoice.status.like(“Partly Paid%”))) bitwise and ((invoice.is\_pos bitwise a ….
    - Value choice on doctype equals “Sales Invoice” — true gives ((invoice.is\_pos bitwise and invoice.due\_date) &lt; today bitwise or is\_overdue), false gives is\_overdue.
  - Set status from nested operand in the contract.terms.Case().when(invoice.status.like(“%Discounted”), “Overdue and Discounted”).else\_(“Overdue”).
  - Evaluate nested operand in the contract(nested operand in the contract).set(“status”, status).where(conditions).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L379)

<a id="op-a59c507ec324ac"></a>
### Get payment terms

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_payment_terms`

**Inputs** terms\_template, posting\_date = no value, grand\_total = no value, base\_grand\_total = no value, bill\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · \_get\_payment\_terms(terms\_template, posting\_date, grand\_total, base\_grand\_total, …).

**Local steps**

- If not terms\_template.
  - Return no value.
- Set terms\_template from cstr(terms\_template).
- If not Platform.has\_permission(“Payment Terms Template”, “read”, doc = terms\_template).
  - Evaluate \_refuse().
- Return \_get\_payment\_terms(terms\_template, posting\_date, grand\_total, base\_grand\_total, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Terms Template”, “read”, doc = terms\_template).

**Boundaries to resolve** callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L231)

<a id="op-dd21144b72cc87"></a>
### Get payment terms

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_payment_terms_bf67c155e284`

**Inputs** terms\_template, posting\_date = no value, grand\_total = no value, base\_grand\_total = no value, bill\_date = no value.

**Record and data access** resolve a document from “Payment Terms Template” via get\_doc.

**Explicit results** no value · schedule.

**Local steps**

- If not terms\_template.
  - Return no value.
- Set terms\_doc from Platform.get\_doc(“Payment Terms Template”, terms\_template).
- Set schedule from list().
- For each d in terms\_doc.get(“terms”).
  - Set term\_details from get\_payment\_term\_details(d, posting\_date, grand\_total, base\_grand\_total, …).
  - Evaluate schedule.append(term\_details).
- Return schedule.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L232)

<a id="op-de267d634d0228"></a>
### Get payment term details

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_payment_term_details`

**Inputs** term, posting\_date = no value, grand\_total = no value, base\_grand\_total = no value, bill\_date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Payment Term” via get\_doc.

**Explicit results** term\_details.

**Local steps**

- Set term\_details from Platform.\_dict().
- If isinstance(term, str).
  - If (not term or not Platform.has\_permission(“Payment Term”, “select”, doc = term)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not term → not Platform.has\_permission(“Payment Term”, “select”, doc = term).
    - Evaluate \_refuse().
  - Set term from Platform.get\_doc(“Payment Term”, term).
- Otherwise.
  - If not hasattr(term, “payment\_term”).
    - Evaluate \_refuse().
  - Otherwise.
    - Set term\_details.payment\_term from term.payment\_term.
- Set fields\_to\_copy from list(“description”, “invoice\_portion”, “discount\_type”, “discount”, …).
- For each field in fields\_to\_copy.
  - Set term\_details at field from term.get(field).
- Set term\_details.payment\_amount from ((flt(term.invoice\_portion) × flt(grand\_total)) ÷ 100).
- Set term\_details.base\_payment\_amount from ((flt(term.invoice\_portion) × flt(base\_grand\_total)) ÷ 100).
- Set term\_details.outstanding from term\_details.payment\_amount.
- Set term\_details.base\_outstanding from term\_details.base\_payment\_amount.
- Set has\_discount from flt(term.get(“discount”)).
- Set date from (bill\_date or posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bill\_date → posting\_date.
- If date.
  - Set term\_details.due\_date from get\_due\_date(term, date).
  - Set term\_details.discount\_date from get\_discount\_date(term, date) when has\_discount, otherwise no value.
    - Value choice on has\_discount — true gives get\_discount\_date(term, date), false gives no value.
- If getdate(term\_details.due\_date) &lt; getdate(posting\_date).
  - Set term\_details.due\_date from posting\_date.
- Return term\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Term”, “select”, doc = term).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L230)

<a id="op-9722154582a900"></a>
### Get due date

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_due_date`

**Inputs** term, posting\_date = no value, bill\_date = no value.

**Explicit results** due\_date.

**Local steps**

- Set due\_date from no value.
- Set date from (bill\_date or posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bill\_date → posting\_date.
- If term.due\_date\_based\_on equals “Day(s) after invoice date”.
  - Set due\_date from add\_days(date, cint(term.credit\_days)).
- Otherwise.
  - If term.due\_date\_based\_on equals “Day(s) after the end of the invoice month”.
    - Set due\_date from add\_days(get\_last\_day(date), cint(term.credit\_days)).
  - Otherwise.
    - If term.due\_date\_based\_on equals “Month(s) after the end of the invoice month”.
      - Set due\_date from get\_last\_day(add\_months(date, cint(term.credit\_months))).
- Return due\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L228)

<a id="op-7efe7737064094"></a>
### Get discount date

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_discount_date`

**Inputs** term, posting\_date = no value, bill\_date = no value.

**Explicit results** discount\_validity.

**Local steps**

- Set discount\_validity from no value.
- Set date from (bill\_date or posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bill\_date → posting\_date.
- If term.discount\_validity\_based\_on equals “Day(s) after invoice date”.
  - Set discount\_validity from add\_days(date, cint(term.discount\_validity)).
- Otherwise.
  - If term.discount\_validity\_based\_on equals “Day(s) after the end of the invoice month”.
    - Set discount\_validity from add\_days(get\_last\_day(date), cint(term.discount\_validity)).
  - Otherwise.
    - If term.discount\_validity\_based\_on equals “Month(s) after the end of the invoice month”.
      - Set discount\_validity from get\_last\_day(add\_months(date, cint(term.discount\_validity))).
- Return discount\_validity.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L227)

<a id="op-e1b0d3541e9a76"></a>
### Get supplier block status

`operation_enterprise_controllers_accounts_controller_business_behavior_get_supplier_block_status`

**Inputs** party\_name.

**Record and data access** resolve a document from “Supplier” via get\_doc.

**Explicit results** info.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, party\_name).
- Set info from mapping(“on\_hold” → supplier.on\_hold, “release\_date” → supplier.release\_date, “hold\_type” → supplier.hold\_type).
- Return info.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L3906) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L377)

<a id="op-d9ce86075296ea"></a>
### Set child tax template and map

`operation_enterprise_binding_enterprise_controllers_accounts_controller_set_child_tax_template_and_map`

**Inputs** item, child\_item, parent\_doc.

**Local steps**

- Set ctx from ItemDetailsCtx(mapping(“item\_code” → item.item\_code, “posting\_date” → parent\_doc.transaction\_date, “tax\_category” → parent\_doc.get(“tax\_category”), “company” → parent\_doc.get(“company”), …)).
- Set item\_tax\_template from \_get\_item\_tax\_template(ctx, item.taxes).
- If not item\_tax\_template.
  - Set item\_tax\_template from \_get\_item\_tax\_template\_from\_item\_group(ctx, item.item\_group).
- Set child\_item.item\_tax\_template from item\_tax\_template.
- Set child\_item.item\_tax\_rate from \_get\_item\_tax\_map(doc = parent\_doc, tax\_template = child\_item.item\_tax\_template, as\_json = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1003) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L243)

<a id="op-311dcf884c0f87"></a>
### Set je amounts

`operation_enterprise_binding_enterprise_controllers_accounts_controller_set_je_amounts`

**Inputs** entry, amount, default\_amount = no value, is\_credit = true.

**Local steps**

- If is\_credit.
  - Set entry.credit\_in\_account\_currency from amount.
  - If default\_amount is distinct from no value.
    - Set entry.credit from default\_amount.
- Otherwise.
  - Set entry.debit\_in\_account\_currency from amount.
  - If default\_amount is distinct from no value.
    - Set entry.debit from default\_amount.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1004) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L244)

<a id="op-9152d072508310"></a>
### Add taxes from tax template

`operation_enterprise_binding_enterprise_controllers_accounts_controller_add_taxes_from_tax_template`

**Inputs** child\_item, parent\_doc, db\_insert = true.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**State and service calls** call db\_insert on tax\_row.

**Local steps**

- Set add\_taxes\_from\_item\_tax\_template from Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).
- If (child\_item.get(“item\_tax\_rate”) and add\_taxes\_from\_item\_tax\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in child\_item.get(“item\_tax\_rate”) → add\_taxes\_from\_item\_tax\_template.
  - Set tax\_map from json.loads(child\_item.get(“item\_tax\_rate”)).
  - For each tuple(tax\_type, tax\_rate) in tax\_map.items().
    - If tax\_rate equals NOT\_APPLICABLE\_TAX.
      - Continue with the next iteration or loop test.
    - Set tax\_rate from flt(tax\_rate).
    - Set taxes from (parent\_doc.get(“taxes”) or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_doc.get(“taxes”) → list().
    - Set found from any(generator of tax.account\_head equals tax\_type for tax drawn from taxes).
      - Draw tax from taxes.
    - If not found.
      - Set tax\_row from parent\_doc.append(“taxes”, mapping()).
      - Evaluate tax\_row.update(mapping(“description” → str(tax\_type).split(“ - ”) at 0, “charge\_type” → “On Net Total”, “account\_head” → tax\_type, “rate” → tax\_rate, …)).
      - If parent\_doc.doctype equals “Purchase Order”.
        - Evaluate tax\_row.update(mapping(“category” → “Total”, “add\_deduct\_tax” → “Add”)).
      - If db\_insert.
        - Evaluate tax\_row.db\_insert().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L219)

<a id="op-71f0a9af418c57"></a>
### Set order defaults

`operation_enterprise_binding_enterprise_controllers_accounts_controller_set_order_defaults`

**Inputs** parent\_doctype, parent\_doctype\_name, child\_doctype, child\_docname, trans\_item.

**Record and data access** resolve a document from parent\_doctype via get\_doc · resolve a document from “Item” via get\_doc.

**State and service calls** request new\_doc for child\_doctype.

**Explicit results** child\_item.

**Local steps**

- Set p\_doc from Platform.get\_doc(parent\_doctype, parent\_doctype\_name).
- Set child\_item from Platform.new\_doc(child\_doctype, parent\_doc = p\_doc, parentfield = child\_docname).
- Set item from Platform.get\_doc(“Item”, trans\_item.get(“item\_code”)).
- For each field in tuple(“item\_code”, “item\_name”, “description”, “item\_group”, …).
  - Evaluate child\_item.update(mapping(field → item.get(field))).
- Set date\_fieldname from “delivery\_date” when child\_doctype equals “Sales Order Item”, otherwise “schedule\_date”.
  - Value choice on child\_doctype equals “Sales Order Item” — true gives “delivery\_date”, false gives “schedule\_date”.
- Evaluate child\_item.update(mapping(date\_fieldname → (trans\_item.get(date\_fieldname) or p\_doc.get(date\_fieldname)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in trans\_item.get(date\_fieldname) → p\_doc.get(date\_fieldname).
- Set child\_item.stock\_uom from item.stock\_uom.
- Set child\_item.uom from (trans\_item.get(“uom”) or item.stock\_uom).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in trans\_item.get(“uom”) → item.stock\_uom.
- Set child\_item.warehouse from get\_new\_child\_item\_warehouse(p\_doc, item, trans\_item, child\_doctype).
- Set conversion\_factor from flt(get\_conversion\_factor(item.item\_code, child\_item.uom).get(“conversion\_factor”)).
- Set child\_item.conversion\_factor from (flt(trans\_item.get(“conversion\_factor”)) or conversion\_factor).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(trans\_item.get(“conversion\_factor”)) → conversion\_factor.
- Set child\_item.price\_list\_rate from flt(trans\_item.get(“price\_list\_rate”)).
- Evaluate child\_item.update(\_get\_bin\_details(child\_item.item\_code, child\_item.warehouse, p\_doc.get(“company”))).
- If child\_doctype belongs to list(“Purchase Order Item”, “Supplier Quotation Item”).
  - Set child\_item.base\_rate from 1.
  - Set child\_item.base\_amount from 1.
- Evaluate set\_child\_tax\_template\_and\_map(item, child\_item, p\_doc).
- Evaluate add\_taxes\_from\_tax\_template(child\_item, p\_doc).
- Return child\_item.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1005) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L245)

<a id="op-2ec748baad8908"></a>
### Get new child item warehouse

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_new_child_item_warehouse`

**Inputs** p\_doc, item, trans\_item, child\_doctype.

**Declared result** (str bitwise or no value).

**Explicit results** no value · warehouse.

**Explicit failure paths** validation helper — translated “Cannot find a default warehouse for item {0}. Please select one in the Update Items dialog, or set a default …”.format(Platform.bold(item.item\_code)).

**Local steps**

- Set warehouse from (trans\_item.get(“warehouse”) or get\_item\_warehouse\_(p\_doc, item, overwrite\_warehouse = true)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in trans\_item.get(“warehouse”) → get\_item\_warehouse\_(p\_doc, item, overwrite\_warehouse = true).
- If not warehouse.
  - If is\_warehouse\_required\_for\_new\_child\_item(child\_doctype, item, trans\_item).
    - Call the validation error handler Platform.throw(translated “Cannot find a default warehouse for item {0}. Please select one in the Update Items dialog, or set a default …”.format(Platform.bold(item.item\_code))).
  - Return no value.
- Evaluate validate\_warehouse\_company(warehouse, p\_doc.company).
- Evaluate validate\_disabled\_warehouse(warehouse).
- Evaluate is\_group\_warehouse(warehouse).
- Return warehouse.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L989) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L229)

<a id="op-717df17ce47156"></a>
### Is warehouse required for new child item

`operation_enterprise_binding_enterprise_controllers_accounts_controller_is_warehouse_required_for_new_child_item`

**Inputs** child\_doctype, item, trans\_item.

**Declared result** bool.

**Explicit results** true · bool((item.is\_stock\_item and flt(trans\_item.get(“qty”)) and not item.delivered\_by\_supplier)) · false.

**Local steps**

- If child\_doctype equals “Sales Order Item”.
  - Return true.
- If child\_doctype belongs to tuple(“Purchase Order Item”, “Supplier Quotation Item”).
  - Return bool((item.is\_stock\_item and flt(trans\_item.get(“qty”)) and not item.delivered\_by\_supplier)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_stock\_item → flt(trans\_item.get(“qty”)) → not item.delivered\_by\_supplier.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L999) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L239)

<a id="op-7d9fba0c51a4dc"></a>
### Get rows with kept reservation

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_rows_with_kept_reservation`

**Inputs** parent.

**Explicit results** set() · set of bundle\_rows.get(row, row) for row drawn from reserved.

**Local steps**

- If (parent.doctype differs from “Sales Order” or not flt(parent.per\_picked)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent.doctype differs from “Sales Order” → not flt(parent.per\_picked).
  - Return set().
- Bind dependencies get\_sre\_reserved\_qty\_details\_for\_voucher.
- Set bundle\_rows from mapping of d.name → d.parent\_detail\_docname for d drawn from parent.get(“packed\_items”).
  - Draw d from parent.get(“packed\_items”).
- Set reserved from get\_sre\_reserved\_qty\_details\_for\_voucher(parent.doctype, parent.name).
- Return set of bundle\_rows.get(row, row) for row drawn from reserved.
  - Draw row from reserved.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L234)
