# Shared transaction rules · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-6a850cd3e9d40a"></a>
### Accounts Controller.validate zero qty for return invoices with stock

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_zero_quantity_for_return_invoices_with_stock`

**Inputs** self.

**Explicit failure paths** validation helper — translated “For Return Invoices with Stock effect, '0' qty Items are not allowed. Following rows are affected: {0}”.format(Platform.bold(comma\_and(list of (“#” + str(nested operand in the contract.idx)) fo ….

**Local steps**

- Set rows from list().
- For each item in self.items.
  - If not (flt(item.qty) or flt(item.get(“rejected\_qty”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.qty) → flt(item.get(“rejected\_qty”)).
    - Evaluate rows.append(item).
- If rows.
  - Call the validation error handler Platform.throw(translated “For Return Invoices with Stock effect, '0' qty Items are not allowed. Following rows are affected: {0}”.format(Platform.bold(comma\_and(list of (“#” + nested operand in the contra ….
    - Draw x from rows.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L671) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L375)

<a id="op-8f6e3858e7a397"></a>
### Accounts Controller.is stock receipt

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_is_stock_receipt`

**Inputs** self.

**Declared result** bool.

**Explicit results** (self.doctype equals “Purchase Receipt” or (self.doctype equals “Purchase Invoice” and self.update\_stock)).

**Local steps**

- Return (self.doctype equals “Purchase Receipt” or (self.doctype equals “Purchase Invoice” and self.update\_stock)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → (self.doctype equals “Purchase Invoice” and self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.update\_stock.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L171)

<a id="op-f7ec10e80f8d97"></a>
### Accounts Controller.validate qty is not zero

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_quantity_is_not_zero`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with InvalidQtyError.

**Local steps**

- If self.flags.allow\_zero\_qty.
  - Return no value.
- For each item in self.items.
  - If (self.is\_stock\_receipt() and item.get(“rejected\_qty”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_stock\_receipt() → item.get(“rejected\_qty”).
    - Continue with the next iteration or loop test.
  - If not flt(item.qty).
    - Call the validation error handler Platform.throw(msg = translated “Row #{0}: Quantity for Item {1} cannot be zero.”.format(item.idx, Platform.bold(item.item\_code)), title = translated “Invalid Quantity”, exc = InvalidQtyError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is stock receipt](operations-004.md#op-8f6e3858e7a397).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L669) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L373)

<a id="op-c152ca887cf87b"></a>
### Accounts Controller.validate account currency

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_account_currency`

**Inputs** self, account, account\_currency = no value.

**Explicit failure paths** validation helper — translated “Account {0} is invalid. Account Currency must be {1}”.format(account, ((one space + translated “or”) + one space).join(valid\_currency)).

**Local steps**

- Set valid\_currency from list(self.company\_currency).
- If (self.get(“currency”) and self.currency differs from self.company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“currency”) → self.currency differs from self.company\_currency.
  - Evaluate valid\_currency.append(self.currency).
- If account\_currency does not belong to valid\_currency.
  - Call the validation error handler Platform.throw(translated “Account {0} is invalid. Account Currency must be {1}”.format(account, ((one space + nested operand in the contract(nested operand in the contract)) + one space).join(valid\_currency))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L364)

<a id="op-0b7c476a2f416e"></a>
### Accounts Controller.clear unallocated advances

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_clear_unallocated_advances`

**Inputs** self, childtype, parentfield.

**Local steps**

- Evaluate self.set(parentfield, self.get(parentfield, mapping(“allocated\_amount” → list(“not in”, list(0, no value, empty text))))).
- Set doctype from Platform.qb.DocType(childtype).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where(((nested operand in the contract.parentfield equals parentfield bitwise and nested operand in the contract.parent equals nested ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L640) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L309)

<a id="op-106d0090be6843"></a>
### Accounts Controller.apply shipping rule

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_apply_shipping_rule`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Shipping Rule” via get\_doc.

**Local steps**

- If self.shipping\_rule.
  - Set shipping\_rule from Platform.get\_doc(“Shipping Rule”, self.shipping\_rule).
  - Evaluate shipping\_rule.apply(self).
  - Evaluate self.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate taxes and totals](operations-002.md#op-52a893faf0bdd9).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L942) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L592) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L297)

<a id="op-268d87f538db28"></a>
### Accounts Controller.get shipping address

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_shipping_address`

**Inputs** self.

**Record and data access** resolve a document from “Address” via get\_doc.

**Explicit results** Platform.get\_doc(“Address”, self.get(fieldname)) · mapping().

**Local steps**

- For each fieldname in tuple(“shipping\_address\_name”, “shipping\_address”).
  - Set shipping\_field from self.meta.get\_field(fieldname).
  - If (shipping\_field and shipping\_field.fieldtype equals “Link”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in shipping\_field → shipping\_field.fieldtype equals “Link”.
    - If self.get(fieldname).
      - Return Platform.get\_doc(“Address”, self.get(fieldname)).
- Return mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L1091) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L324)

<a id="op-394eadbcea28e8"></a>
### Accounts Controller.set advances

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_advances`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set res from self.get\_advance\_entries(include\_unallocated = not cint(self.get(“only\_include\_allocated\_payments”))).
- Evaluate self.set(“advances”, list()).
- Set advance\_allocated from 0.
- For each d in res.
  - If self.get(“party\_account\_currency”) equals self.company\_currency.
    - Set amount from (self.get(“base\_rounded\_total”) or self.base\_grand\_total).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“base\_rounded\_total”) → self.base\_grand\_total.
  - Otherwise.
    - Set amount from (self.get(“rounded\_total”) or self.grand\_total).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“rounded\_total”) → self.grand\_total.
  - Set allocated\_amount from min((amount − advance\_allocated), d.amount).
  - Update advance\_allocated using + flt(allocated\_amount).
  - Set advance\_row from mapping(“doctype” → (self.doctype + “ Advance”), “reference\_type” → d.reference\_type, “reference\_name” → d.reference\_name, “reference\_row” → d.reference\_row, …).
  - If d.get(“paid\_from”).
    - Set advance\_row at “account” from d.paid\_from.
  - If d.get(“paid\_to”).
    - Set advance\_row at “account” from d.paid\_to.
  - Evaluate self.append(“advances”, advance\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get advance entries](operations-004.md#op-3615806ea74019).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L350)

<a id="op-3615806ea74019"></a>
### Accounts Controller.get advance entries

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_advance_entries`

**Inputs** self, include\_unallocated = true.

**Explicit results** res.

**Local steps**

- Set party\_account from list().
- Set default\_advance\_account from no value.
- If self.doctype belongs to list(“Sales Invoice”, “POS Invoice”).
  - Set party\_type from “Customer”.
  - Set party from self.customer.
  - Set amount\_field from “credit\_in\_account\_currency”.
  - Set order\_field from “sales\_order”.
  - Set order\_doctype from “Sales Order”.
  - Evaluate party\_account.append(self.debit\_to).
- Otherwise.
  - Set party\_type from “Supplier”.
  - Set party from self.supplier.
  - Set amount\_field from “debit\_in\_account\_currency”.
  - Set order\_field from “purchase\_order”.
  - Set order\_doctype from “Purchase Order”.
  - Evaluate party\_account.append(self.credit\_to).
- Set party\_accounts from get\_party\_account(party\_type, party = party, company = self.company, include\_advance = true).
- If party\_accounts.
  - Evaluate party\_account.append(party\_accounts at 0).
  - Set default\_advance\_account from party\_accounts at 1 when len(party\_accounts) equals 2, otherwise no value.
    - Value choice on len(party\_accounts) equals 2 — true gives party\_accounts at 1, false gives no value.
- Set order\_list from list(set(generator of d.get(order\_field) for d drawn from self.get(“items”) where d.get(order\_field))).
  - Draw d from self.get(“items”), keep a combination only if (d.get(order\_field)).
- Set journal\_entries from get\_advance\_journal\_entries(party\_type, party, party\_account, amount\_field, …).
- Set payment\_entries from get\_advance\_payment\_entries\_for\_regional(party\_type, party, party\_account, order\_doctype, …).
- Set res from (journal\_entries + payment\_entries).
- Return res.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L316)

<a id="op-46909a017aa2fd"></a>
### Accounts Controller.is inclusive tax

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_is_inclusive_tax`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** is\_inclusive.

**Local steps**

- Set is\_inclusive from cint(Platform.get\_single\_value(“Accounts Settings”, “show\_inclusive\_tax\_in\_print”)).
- If is\_inclusive.
  - Set is\_inclusive from 0.
  - If self.get(“taxes”, filters = mapping(“included\_in\_print\_rate” → 1)).
    - Set is\_inclusive from 1.
- Return is\_inclusive.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “show\_inclusive\_tax\_in\_print”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L1459) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L625) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L330)

<a id="op-30af53a27a3d63"></a>
### Accounts Controller.should show taxes as table in print

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_should_show_taxes_as_table_in_print`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** cint(Platform.get\_single\_value(“Accounts Settings”, “show\_taxes\_as\_table\_in\_print”)).

**Local steps**

- Return cint(Platform.get\_single\_value(“Accounts Settings”, “show\_taxes\_as\_table\_in\_print”)).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “show\_taxes\_as\_table\_in\_print”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L1649) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L360)

<a id="op-92d9f34573a809"></a>
### Accounts Controller.validate advance entries

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_advance_entries`

**Inputs** self.

**State and service calls** msgprint with translated “Payment Entry {0} is linked against Order {1}, check if it should be pulled as advance in this invoice.”.format(d.reference\_name, d.against\_order).

**Explicit results** no value.

**Local steps**

- Set order\_field from “sales\_order” when self.doctype equals “Sales Invoice”, otherwise “purchase\_order”.
  - Value choice on self.doctype equals “Sales Invoice” — true gives “sales\_order”, false gives “purchase\_order”.
- Set order\_list from list(set(generator of d.get(order\_field) for d drawn from self.get(“items”) where d.get(order\_field))).
  - Draw d from self.get(“items”), keep a combination only if (d.get(order\_field)).
- If not order\_list.
  - Return no value.
- Set advance\_entries from self.get\_advance\_entries(include\_unallocated = false).
- If advance\_entries.
  - Set advance\_entries\_against\_si from list of d.reference\_name for d drawn from self.get(“advances”).
    - Draw d from self.get(“advances”).
  - For each d in advance\_entries.
    - If (not advance\_entries\_against\_si or d.reference\_name does not belong to advance\_entries\_against\_si).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not advance\_entries\_against\_si → d.reference\_name does not belong to advance\_entries\_against\_si.
      - Evaluate Platform.msgprint(translated “Payment Entry {0} is linked against Order {1}, check if it should be pulled as advance in this invoice.”.format(d.reference\_name, d.against\_order)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get advance entries](operations-004.md#op-3615806ea74019).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L365)

<a id="op-55557a2929b1dd"></a>
### Accounts Controller.set advance gain or loss

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_advance_gain_or_loss`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.get(“conversion\_rate”) equals 1 or not self.get(“advances”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“conversion\_rate”) equals 1 → not self.get(“advances”).
  - Return no value.
- Set is\_purchase\_invoice from self.doctype equals “Purchase Invoice”.
- Set party\_account from self.credit\_to when is\_purchase\_invoice, otherwise self.debit\_to.
  - Value choice on is\_purchase\_invoice — true gives self.credit\_to, false gives self.debit\_to.
- If get\_account\_currency(party\_account) differs from self.currency.
  - Return no value.
- For each d in self.get(“advances”).
  - Set advance\_exchange\_rate from d.ref\_exchange\_rate.
  - If (d.allocated\_amount and self.conversion\_rate differs from advance\_exchange\_rate).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.allocated\_amount → self.conversion\_rate differs from advance\_exchange\_rate.
    - Set base\_allocated\_amount\_in\_ref\_rate from (advance\_exchange\_rate × d.allocated\_amount).
    - Set base\_allocated\_amount\_in\_inv\_rate from (self.conversion\_rate × d.allocated\_amount).
    - Set difference from (base\_allocated\_amount\_in\_ref\_rate − base\_allocated\_amount\_in\_inv\_rate).
    - Set d.exchange\_gain\_loss from difference.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L348)

<a id="op-ad3a18552012fc"></a>
### Accounts Controller.make precision loss gl entry

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_make_precision_loss_gl_entry`

**Inputs** self, gl\_entries.

**Local steps**

- Set tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening) from get\_round\_off\_account\_and\_cost\_center(self.company, “Purchase Invoice”, self.name, self.use\_company\_roundoff\_cost\_center).
- Set precision\_loss from (self.get(“base\_net\_total”) − flt((self.get(“net\_total”) × self.conversion\_rate), self.precision(“net\_total”))).
- Set credit\_or\_debit from “credit” when self.doctype equals “Purchase Invoice”, otherwise “debit”.
  - Value choice on self.doctype equals “Purchase Invoice” — true gives “credit”, false gives “debit”.
- Set against from self.supplier when self.doctype equals “Purchase Invoice”, otherwise self.customer.
  - Value choice on self.doctype equals “Purchase Invoice” — true gives self.supplier, false gives self.customer.
- If precision\_loss.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → round\_off\_account, “against” → against, credit\_or\_debit → precision\_loss, “cost\_center” → round\_off\_cost\_center when self.use\_company\_roundoff\_cost\_ce ….
    - Value choice on self.use\_company\_roundoff\_cost\_center — true gives round\_off\_cost\_center, false gives (self.cost\_center or round\_off\_cost\_center).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → round\_off\_cost\_center.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl dict](operations-003.md#op-9b830044032472).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L937) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L177)

<a id="op-0641b7b7ca1db7"></a>
### Accounts Controller.gain loss journal already booked

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_gain_loss_journal_already_booked`

**Inputs** self, gain\_loss\_account, exc\_gain\_loss, ref2\_dt, ref2\_dn, ref2\_detail\_no.

**Declared result** bool.

**Record and data access** read “Journal Entry Account” via get\_all · read “Journal Entry” via get\_all.

**Explicit results** true · false.

**Local steps**

- If res bound to Platform.db.get\_all(“Journal Entry Account”, filters = mapping(“docstatus” → 1, “account” → gain\_loss\_account, “reference\_type” → ref2\_dt, “reference\_name” → ref2\_dn, …), pluck = “parent”).
  - Set res from list(set of x for x drawn from res).
    - Draw x from res.
  - If exc\_vouchers bound to Platform.db.get\_all(“Journal Entry”, filters = mapping(“name” → list(“in”, res), “voucher\_type” → “Exchange Gain Or Loss”), fields = list(“voucher\_type”, “total\_debit”, “total\_credit”)).
    - Set booked\_voucher from exc\_vouchers at 0.
    - If (booked\_voucher.total\_debit equals exc\_gain\_loss and booked\_voucher.total\_credit equals exc\_gain\_loss and booked\_voucher.voucher\_type equals “Exchange Gain Or Loss”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in booked\_voucher.total\_debit equals exc\_gain\_loss → booked\_voucher.total\_credit equals exc\_gain\_loss → booked\_voucher.voucher\_type equals “Exchange Gain Or Loss”.
      - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L315)

<a id="op-96f85b3decc29b"></a>
### Accounts Controller.make exchange gain loss journal

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_make_exchange_gain_loss_journal`

**Inputs** self, args = no value, dimensions\_dict = no value.

**Declared result** no value.

**Record and data access** read arg.voucher\_type via get\_value · read “Company” via get\_cached\_value.

**State and service calls** msgprint with translated “Exchange Gain/Loss amount has been booked through {0}”.format(get\_link\_to\_form(“Journal Entry”, je)).

**Local steps**

- If self.docstatus equals 1.
  - If dimensions\_dict is identical to no value.
    - Set dimensions\_dict from Platform.\_dict().
    - Set active\_dimensions from get\_dimensions() at 0.
    - For each dim in active\_dimensions.
      - Set dimensions\_dict at dim.fieldname from self.get(dim.fieldname).
  - If self.get(“doctype”) equals “Journal Entry”.
    - If args.
      - Set precision from get\_currency\_precision().
      - For each arg in args.
        - If ((flt(arg.get(“difference\_amount”, 0), precision) differs from 0 or flt(arg.get(“exchange\_gain\_loss”, 0), precision) differs from 0) and arg.get(“difference\_account”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in (flt(arg.get(“difference\_amount”, 0), precision) differs from 0 or flt(arg.get(“exchange\_gain\_loss”, 0), precision) differs from 0) → arg.get(“difference\_account”).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(arg.get(“difference\_amount”, 0), precision) differs from 0 → flt(arg.get(“exchange\_gain\_loss”, 0), precision) differs from 0.
          - Set party\_account from arg.get(“account”).
          - Set gain\_loss\_account from arg.get(“difference\_account”).
          - Set difference\_amount from (arg.get(“difference\_amount”) or arg.get(“exchange\_gain\_loss”)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in arg.get(“difference\_amount”) → arg.get(“exchange\_gain\_loss”).
          - Set dr\_or\_cr from “debit” when difference\_amount &gt; 0, otherwise “credit”.
            - Value choice on difference\_amount &gt; 0 — true gives “debit”, false gives “credit”.
          - If (self.is\_payable\_account(self.doctype, party\_account) and arg.get(“against\_voucher\_type”) does not belong to tuple(“Journal Entry”, “Payment Entry”)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_payable\_account(self.doctype, party\_account) → arg.get(“against\_voucher\_type”) does not belong to tuple(“Journal Entry”, “Payment Entry”).
            - Set dr\_or\_cr from “credit” when dr\_or\_cr equals “debit”, otherwise “debit”.
              - Value choice on dr\_or\_cr equals “debit” — true gives “credit”, false gives “debit”.
          - Set reverse\_dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
            - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
          - If not self.gain\_loss\_journal\_already\_booked(gain\_loss\_account, difference\_amount, self.doctype, self.name, …).
            - Set posting\_date from (arg.get(“difference\_posting\_date”) or Platform.db.get\_value(arg.voucher\_type, arg.voucher\_no, “posting\_date”)).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in arg.get(“difference\_posting\_date”) → Platform.db.get\_value(arg.voucher\_type, arg.voucher\_no, “posting\_date”).
            - Set je from create\_gain\_loss\_journal(self.company, posting\_date, arg.get(“party\_type”), arg.get(“party”), …).
            - Evaluate Platform.msgprint(translated “Exchange Gain/Loss amount has been booked through {0}”.format(get\_link\_to\_form(“Journal Entry”, je))).
  - If self.get(“doctype”) equals “Payment Entry”.
    - Set gain\_loss\_to\_book from list of x for x drawn from self.references where x.exchange\_gain\_loss differs from 0.
      - Draw x from self.references, keep a combination only if (x.exchange\_gain\_loss differs from 0).
    - Set booked from list().
    - If gain\_loss\_to\_book.
      - Evaluate list of x.reference\_doctype for x drawn from gain\_loss\_to\_book.
        - Draw x from gain\_loss\_to\_book.
      - Evaluate list of x.reference\_name for x drawn from gain\_loss\_to\_book.
        - Draw x from gain\_loss\_to\_book.
      - Set je from qb.DocType(“Journal Entry”).
      - Set jea from qb.DocType(“Journal Entry Account”).
      - Set parents from nested operand in the contract(nested operand in the contract).select(jea.parent).where(((nested operand in the contract.reference\_type equals “Payment Entry” bitwise and nested operand in the contract.ref ….run().
      - Set booked from list().
      - If parents.
        - Set booked from nested operand in the contract(nested operand in the contract).select(jea.reference\_type, jea.reference\_name, jea.reference\_detail\_no).where(((nested operand in the contract.docstatus equals 1 bitwise and  ….run().
    - For each d in gain\_loss\_to\_book.
      - If (d.exchange\_gain\_loss and tuple(d.reference\_doctype, d.reference\_name, str(d.idx)) does not belong to booked).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.exchange\_gain\_loss → tuple(d.reference\_doctype, d.reference\_name, str(d.idx)) does not belong to booked.
        - If self.book\_advance\_payments\_in\_separate\_party\_account.
          - Set party\_account from d.account.
        - Otherwise.
          - If self.payment\_type equals “Receive”.
            - Set party\_account from self.paid\_from.
          - Otherwise.
            - If self.payment\_type equals “Pay”.
              - Set party\_account from self.paid\_to.
        - Set dr\_or\_cr from “debit” when d.exchange\_gain\_loss &gt; 0, otherwise “credit”.
          - Value choice on d.exchange\_gain\_loss &gt; 0 — true gives “debit”, false gives “credit”.
        - If self.is\_payable\_account(d.reference\_doctype, party\_account).
          - Set dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
            - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
        - Set reverse\_dr\_or\_cr from “debit” when dr\_or\_cr equals “credit”, otherwise “credit”.
          - Value choice on dr\_or\_cr equals “credit” — true gives “debit”, false gives “credit”.
        - Set gain\_loss\_account from Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”).
        - Set je from create\_gain\_loss\_journal(self.company, args.get(“difference\_posting\_date”) when args, otherwise self.posting\_date, self.party\_type, self.party, …).
          - Value choice on args — true gives args.get(“difference\_posting\_date”), false gives self.posting\_date.
        - Evaluate Platform.msgprint(translated “Exchange Gain/Loss amount has been booked through {0}”.format(get\_link\_to\_form(“Journal Entry”, je))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is payable account](operations-004.md#op-51a59f29750412), [gain loss journal already booked](operations-004.md#op-0641b7b7ca1db7).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L335)

<a id="op-51a59f29750412"></a>
### Accounts Controller.is payable account

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_is_payable_account`

**Inputs** self, reference\_doctype, account.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** true · false.

**Local steps**

- If (reference\_doctype equals “Purchase Invoice” or (reference\_doctype belongs to tuple(“Journal Entry”, “Payment Entry”) and Platform.get\_cached\_value(“Account”, account, “account\_type”) equals “Payable”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doctype equals “Purchase Invoice” → (reference\_doctype belongs to tuple(“Journal Entry”, “Payment Entry”) and Platform.get\_cached\_value(“Account”, account, “account\_type”) equals “Payable”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype belongs to tuple(“Journal Entry”, “Payment Entry”) → Platform.get\_cached\_value(“Account”, account, “account\_type”) equals “Payable”.
  - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “account\_type”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L629) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L333)

<a id="op-e9230b0b7a07c8"></a>
### Accounts Controller.update against document in jv

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_update_against_document_in_journal_voucher`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If self.doctype equals “Sales Invoice”.
  - Set party\_type from “Customer”.
  - Set party from self.customer.
  - Set party\_account from self.debit\_to.
  - Set dr\_or\_cr from “credit\_in\_account\_currency”.
- Otherwise.
  - Set party\_type from “Supplier”.
  - Set party from self.supplier.
  - Set party\_account from self.credit\_to.
  - Set dr\_or\_cr from “debit\_in\_account\_currency”.
- Set lst from list().
- For each d in self.get(“advances”).
  - If flt(d.allocated\_amount) &gt; 0.
    - Set args from Platform.\_dict(mapping(“voucher\_type” → d.reference\_type, “voucher\_no” → d.reference\_name, “voucher\_detail\_no” → d.reference\_row, “against\_voucher\_type” → self.doctype, …)).
      - Value choice on self.party\_account\_currency differs from self.company\_currency — true gives self.conversion\_rate, false gives 1.
      - Value choice on self.party\_account\_currency equals self.company\_currency — true gives self.base\_grand\_total, false gives self.grand\_total.
    - Evaluate lst.append(args).
- If lst.
  - Bind dependencies reconcile\_against\_document.
  - Set active\_dimensions from get\_dimensions() at 0.
  - For each x in lst.
    - For each dim in active\_dimensions.
      - If self.get(dim.fieldname).
        - Evaluate x.update(mapping(dim.fieldname → self.get(dim.fieldname))).
  - Evaluate reconcile\_against\_document(lst, active\_dimensions = active\_dimensions).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “exchange\_gain\_loss\_account”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L362)

<a id="op-1d34601e3a8ae6"></a>
### Accounts Controller.cancel system generated credit debit notes

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_cancel_system_generated_credit_debit_notes`

**Inputs** self.

**Record and data access** read “Journal Entry” via get\_all · resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Journal Entry”, x).

**Local steps**

- If self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Set voucher\_type from “Credit Note” when self.doctype equals “Sales Invoice”, otherwise “Debit Note”.
    - Value choice on self.doctype equals “Sales Invoice” — true gives “Credit Note”, false gives “Debit Note”.
  - Set journals from Platform.db.get\_all(“Journal Entry”, filters = mapping(“is\_system\_generated” → 1, “reference\_type” → self.doctype, “reference\_name” → self.name, “voucher\_type” → voucher\_type, …), pluck = “name”).
  - For each x in journals.
    - Evaluate Platform.get\_doc(“Journal Entry”, x).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L3350) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L304)

<a id="op-d023e890c0def0"></a>
### Accounts Controller.on cancel

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_on_cancel`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Bind dependencies remove\_from\_bank\_transaction.
- Bind dependencies cancel\_common\_party\_journal, cancel\_exchange\_gain\_loss\_journal, unlink\_ref\_doc\_from\_payment\_entries.
- Evaluate remove\_from\_bank\_transaction(self.doctype, self.name).
- If self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “Payment Entry”, “Journal Entry”).
  - Evaluate self.cancel\_system\_generated\_credit\_debit\_notes().
  - Evaluate cancel\_exchange\_gain\_loss\_journal(self).
  - Evaluate cancel\_common\_party\_journal(self).
  - If Platform.get\_single\_value(“Accounts Settings”, “unlink\_payment\_on\_cancellation\_of\_invoice”).
    - Evaluate unlink\_ref\_doc\_from\_payment\_entries(self).
- Otherwise.
  - If self.doctype belongs to list(“Sales Order”, “Purchase Order”).
    - If Platform.get\_single\_value(“Accounts Settings”, “unlink\_advance\_payment\_on\_cancelation\_of\_order”).
      - Evaluate unlink\_ref\_doc\_from\_payment\_entries(self).
    - If self.doctype equals “Sales Order”.
      - Evaluate self.unlink\_ref\_doc\_from\_po().

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel system generated credit debit notes](operations-004.md#op-1d34601e3a8ae6), [unlink ref doc from po](operations-004.md#op-e904e8b93df450).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “unlink\_payment\_on\_cancellation\_of\_invoice”), Platform.get\_single\_value(“Accounts Settings”, “unlink\_advance\_payment\_on\_cancelation\_of\_order”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L3682) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L336)

<a id="op-e904e8b93df450"></a>
### Accounts Controller.unlink ref doc from po

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_unlink_reference_record_from_purchase_order`

**Inputs** self.

**Record and data access** read “Purchase Order Item” via get\_all.

**State and service calls** request set\_value on “Purchase Order Item” · msgprint with translated “Purchase Orders {0} are un-linked”.format(whitespace '\\n'.join(linked\_po)).

**Explicit results** no value.

**Local steps**

- Set so\_items from list of item.name for item drawn from self.items.
  - Draw item from self.items.
- Set filters from mapping(“sales\_order” → self.name, “sales\_order\_item” → list(“in”, so\_items), “docstatus” → list(“&lt;”, 2)).
- Set linked\_po\_items from Platform.get\_all(“Purchase Order Item”, filters = filters, fields = list(“parent”, “sales\_order\_item”)).
- If not linked\_po\_items.
  - Return no value.
- Evaluate Platform.db.set\_value(“Purchase Order Item”, filters, mapping(“sales\_order” → no value, “sales\_order\_item” → no value)).
- Evaluate self.update\_ordered\_qty\_in\_items(set of item.sales\_order\_item for item drawn from linked\_po\_items).
  - Draw item from linked\_po\_items.
- Set linked\_po from sorted(set of item.parent for item drawn from linked\_po\_items).
  - Draw item from linked\_po\_items.
- Evaluate Platform.msgprint(translated “Purchase Orders {0} are un-linked”.format(whitespace '\\n'.join(linked\_po))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update ordered qty in items](operations-004.md#op-31d3127ddaa762).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L361)

<a id="op-31d3127ddaa762"></a>
### Accounts Controller.update ordered qty in items

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_update_ordered_qty_in_items`

**Inputs** self, so\_items.

**State and service calls** request set\_value on “Sales Order Item”.

**Local steps**

- Set purchase\_order\_item from Platform.qb.DocType(“Purchase Order Item”).
- Set ordered\_qty from dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(purchase\_order\_item.sales\_order\_item).run()).
- Set items\_by\_ordered\_qty from defaultdict(list).
- For each so\_item in so\_items.
  - Evaluate items\_by\_ordered\_qty at flt(ordered\_qty.get(so\_item)).append(so\_item).
- For each tuple(qty, items) in items\_by\_ordered\_qty.items().
  - Evaluate Platform.db.set\_value(“Sales Order Item”, mapping(“name” → list(“in”, items)), “ordered\_qty”, qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L194)

<a id="op-39783523911317"></a>
### Accounts Controller.get tax map

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_tax_map`

**Inputs** self.

**Explicit results** tax\_map.

**Local steps**

- Set tax\_map from mapping().
- For each tax in self.get(“taxes”).
  - Evaluate tax\_map.setdefault(tax.account\_head, 0.0).
  - Update tax\_map at tax.account\_head using + tax.tax\_amount.
- Return tax\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L922) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L162)

<a id="op-e31dadcf3298d0"></a>
### Accounts Controller.get amount and base amount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_amount_and_base_amount`

**Inputs** self, item, enable\_discount\_accounting.

**Explicit results** tuple(item.amount, item.base\_amount) · tuple(amount, base\_amount).

**Local steps**

- Set amount from item.net\_amount.
- Set base\_amount from item.base\_net\_amount.
- If (enable\_discount\_accounting and self.get(“discount\_amount”) and self.get(“additional\_discount\_account”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enable\_discount\_accounting → self.get(“discount\_amount”) → self.get(“additional\_discount\_account”).
  - If not hasattr(self, “\_\_has\_distributed\_discount\_set”).
    - Set self.\_\_has\_distributed\_discount\_set from any(generator of i.distributed\_discount\_amount for i drawn from self.get(“items”)).
      - Draw i from self.get(“items”).
  - If not self.\_\_has\_distributed\_discount\_set.
    - Return tuple(item.amount, item.base\_amount).
  - Update amount using + item.distributed\_discount\_amount.
  - Update base\_amount using + flt((item.distributed\_discount\_amount × self.get(“conversion\_rate”)), item.precision(“distributed\_discount\_amount”)).
- Return tuple(amount, base\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L913) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L153)
