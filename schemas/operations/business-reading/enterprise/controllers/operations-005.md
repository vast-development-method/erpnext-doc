# Shared transaction rules · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-a56b603bbc69fe"></a>
### Accounts Controller.get tax amounts

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_tax_amounts`

**Inputs** self, tax, enable\_discount\_accounting.

**Explicit results** tuple(amount, base\_amount).

**Local steps**

- Set amount from tax.tax\_amount\_after\_discount\_amount.
- Set base\_amount from tax.base\_tax\_amount\_after\_discount\_amount.
- If (enable\_discount\_accounting and self.get(“discount\_amount”) and self.get(“additional\_discount\_account”) and self.get(“apply\_discount\_on”) equals “Grand Total”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enable\_discount\_accounting → self.get(“discount\_amount”) → self.get(“additional\_discount\_account”) → self.get(“apply\_discount\_on”) equals “Grand Total”.
  - Set amount from tax.tax\_amount.
  - Set base\_amount from tax.base\_tax\_amount.
- Return tuple(amount, base\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L161)

<a id="op-0af4022a676440"></a>
### Accounts Controller.make discount gl entries

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_make_discount_gl_entries`

**Inputs** self, gl\_entries, deferred\_return\_items = no value.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Set enable\_discount\_accounting from cint(Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”)).
- If enable\_discount\_accounting.
  - For each item in self.get(“items”).
    - If (item.get(“discount\_amount”) and item.get(“discount\_account”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“discount\_amount”) → item.get(“discount\_account”).
      - Set discount\_amount from (item.discount\_amount × item.qty).
      - Set income\_account from self.get\_item\_income\_account(item, deferred\_return\_items).
      - Set account\_currency from get\_account\_currency(item.discount\_account).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → item.discount\_account, “against” → self.customer, “debit” → flt((discount\_amount × nested operand in the contract.get(“conversion\_rate”)), item.precis ….
      - Set account\_currency from get\_account\_currency(income\_account).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → income\_account, “voucher\_detail\_no” → item.name when (self.is\_return and item.enable\_deferred\_revenue), otherwise no value, “against” → self.customer, ….
        - Value choice on (self.is\_return and item.enable\_deferred\_revenue) — true gives item.name, false gives no value.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → item.enable\_deferred\_revenue.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
- If ((enable\_discount\_accounting or self.get(“is\_cash\_or\_non\_trade\_discount”)) and self.get(“additional\_discount\_account”) and self.get(“discount\_amount”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (enable\_discount\_accounting or self.get(“is\_cash\_or\_non\_trade\_discount”)) → self.get(“additional\_discount\_account”) → self.get(“discount\_amount”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in enable\_discount\_accounting → self.get(“is\_cash\_or\_non\_trade\_discount”).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.additional\_discount\_account, “against” → self.customer, “debit” → self.base\_discount\_amount, “cost\_center” → (self.cost\_center or Enterprise.get\_ ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → Enterprise.get\_default\_cost\_center(self.company).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get gl dict](operations-003.md#op-9b830044032472).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “enable\_discount\_accounting”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L936) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L176)

<a id="op-3769911b4b4fb3"></a>
### Accounts Controller.validate multiple billing

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_multiple_billing`

**Inputs** self, ref\_dt, item\_ref\_dn, based\_on.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value.

**State and service calls** msgprint with translated “Overbilling of {} ignored because you have {} role.”.format(total\_overbilled\_amt, role\_allowed\_to\_overbill).

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_allowance\_for.
- Set ref\_wise\_billed\_amount from self.get\_reference\_wise\_billed\_amt(ref\_dt, item\_ref\_dn, based\_on).
- If not ref\_wise\_billed\_amount.
  - Return no value.
- Set total\_overbilled\_amt from 0.0.
- Set overbilled\_items from list().
- Set precision from self.precision(based\_on, “items”).
- Set precision\_allowance from (1 ÷ (10 to the power precision)).
- Set role\_allowed\_to\_overbill from Platform.get\_single\_value(“Accounts Settings”, “role\_allowed\_to\_over\_bill”).
- Set is\_overbilling\_allowed from role\_allowed\_to\_overbill belongs to Platform.get\_roles().
- For each row in ref\_wise\_billed\_amount.values().
  - Set total\_billed\_amt from row.billed\_amt.
  - Set allowance from get\_allowance\_for(row.item\_code, mapping(), no value, no value, …) at 0.
  - Set max\_allowed\_amt from flt(((row.ref\_amt × (100 + allowance)) ÷ 100)).
  - If (total\_billed\_amt &lt; 0 and max\_allowed\_amt &lt; 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_billed\_amt &lt; 0 → max\_allowed\_amt &lt; 0.
    - Set tuple(total\_billed\_amt, max\_allowed\_amt) from tuple(abs(total\_billed\_amt), abs(max\_allowed\_amt)).
  - Set overbill\_amt from (total\_billed\_amt − max\_allowed\_amt).
  - Set row at “max\_allowed\_amt” from max\_allowed\_amt.
  - Update total\_overbilled\_amt using + overbill\_amt.
  - If (overbill\_amt &gt; precision\_allowance and not is\_overbilling\_allowed).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in overbill\_amt &gt; precision\_allowance → not is\_overbilling\_allowed.
    - If (self.doctype differs from “Purchase Invoice” or not cint(Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype differs from “Purchase Invoice” → not cint(Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”)).
      - Evaluate overbilled\_items.append(row).
- If overbilled\_items.
  - Evaluate self.throw\_overbill\_exception(overbilled\_items, precision).
- If (is\_overbilling\_allowed and total\_overbilled\_amt &gt; 0.1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_overbilling\_allowed → total\_overbilled\_amt &gt; 0.1.
  - Evaluate Platform.msgprint(translated “Overbilling of {} ignored because you have {} role.”.format(total\_overbilled\_amt, role\_allowed\_to\_overbill), indicator = “orange”, alert = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get reference wise billed amt](operations-005.md#op-7c0434334e8a65), [throw overbill exception](operations-005.md#op-678a7d6a044c30).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “role\_allowed\_to\_over\_bill”), Platform.db.get\_single\_value(“Buying Settings”, “bill\_for\_rejected\_quantity\_in\_purchase\_invoice”) · effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L967) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L207)

<a id="op-43c21ffe8aac92"></a>
### Accounts Controller.get billing reference details

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_billing_reference_details`

**Inputs** self, reference\_names, reference\_doctype, based\_on.

**Record and data access** read reference\_doctype via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(reference\_doctype, filters = mapping(“name” → tuple(“in”, reference\_names)), fields = list(“name”, based\_on), as\_list = 1)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(reference\_doctype, filters = mapping(“name” → tuple(“in”, reference\_names)), fields = list(“name”, based\_on), as\_list = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L914) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L154)

<a id="op-7c0434334e8a65"></a>
### Accounts Controller.get reference wise billed amt

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_reference_wise_billed_amt`

**Inputs** self, ref\_dt, item\_ref\_dn, based\_on.

**State and service calls** msgprint with translated “System will not check over billing since amount for Item {0} in {1} is zero”.format(item.item\_code, ref\_dt).

**Explicit results** no value · ref\_wise\_billed\_amount.

**Local steps**

- Set reference\_names from list of d.get(item\_ref\_dn) for d drawn from self.items where d.get(item\_ref\_dn).
  - Draw d from self.items, keep a combination only if (d.get(item\_ref\_dn)).
- If not reference\_names.
  - Return no value.
- Set ref\_wise\_billed\_amount from mapping().
- Set precision from self.precision(based\_on, “items”).
- Set reference\_details from self.get\_billing\_reference\_details(reference\_names, (ref\_dt + “ Item”), based\_on).
- Set already\_billed from self.get\_already\_billed\_amount(reference\_names, item\_ref\_dn, based\_on).
- For each item in self.items.
  - Set key from item.get(item\_ref\_dn).
  - If not key.
    - Continue with the next iteration or loop test.
  - Set ref\_amt from flt(reference\_details.get(key), precision).
  - Set current\_amount from flt(item.get(based\_on), precision).
  - If not ref\_amt.
    - If current\_amount.
      - Evaluate Platform.msgprint(translated “System will not check over billing since amount for Item {0} in {1} is zero”.format(item.item\_code, ref\_dt), title = translated “Warning”, indicator = “orange”).
    - Continue with the next iteration or loop test.
  - Evaluate ref\_wise\_billed\_amount.setdefault(key, Platform.\_dict(item\_code = item.item\_code, billed\_amt = 0.0, ref\_amt = ref\_amt, rows = list())).
  - Evaluate ref\_wise\_billed\_amount at key at “rows”.append(item.idx).
  - Set ref\_wise\_billed\_amount at key at “ref\_amt” from ref\_amt.
  - Update ref\_wise\_billed\_amount at key at “billed\_amt” using + current\_amount.
  - If key belongs to already\_billed.
    - Update ref\_wise\_billed\_amount at key at “billed\_amt” using + flt(already\_billed.pop(key, 0), precision).
- Return ref\_wise\_billed\_amount.

**Methods declared on this owner** [get billing reference details](operations-005.md#op-43c21ffe8aac92), [get already billed amount](operations-005.md#op-0c3723e5412892).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L918) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L158)

<a id="op-0c3723e5412892"></a>
### Accounts Controller.get already billed amount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_already_billed_amount`

**Inputs** self, reference\_names, item\_ref\_dn, based\_on.

**Explicit results** Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(join\_field).run()).

**Local steps**

- Set item\_doctype from Platform.qb.DocType(self.items at 0.doctype).
- Set based\_on\_field from Platform.qb.Field(based\_on).
- Set join\_field from Platform.qb.Field(item\_ref\_dn).
- Return Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(join\_field).run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L912) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L152)

<a id="op-678a7d6a044c30"></a>
### Accounts Controller.throw overbill exception

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_throw_overbill_exception`

**Inputs** self, overbilled\_items, precision.

**Explicit failure paths** validation helper — translated message.

**Local steps**

- Set message from (((translated text in the contract + text in the contract) + empty text.join(generator of nested operand in the contract(nested operand in the contract).format(nested operand in the contract.bold(nested op ….
  - Draw item from overbilled\_items.
  - Draw x from item.rows.
- Update message using + translated text in the contract.
- Call the validation error handler Platform.throw(translated message).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L193)

<a id="op-5a48a580f6731a"></a>
### Accounts Controller.get company default

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_company_default`

**Inputs** self, fieldname, ignore\_validation = false.

**Explicit results** get\_company\_default(self.company, fieldname, ignore\_validation = ignore\_validation).

**Local steps**

- Bind dependencies get\_company\_default.
- Return get\_company\_default(self.company, fieldname, ignore\_validation = ignore\_validation).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L4584) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L320)

<a id="op-3ec873497458ec"></a>
### Accounts Controller.get stock items

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_stock_items`

**Inputs** self.

**Record and data access** read “Item” via get\_values.

**Explicit results** stock\_items.

**Local steps**

- Set stock\_items from list().
- Set item\_codes from list(set(generator of item.item\_code for item drawn from self.get(“items”))).
  - Draw item from self.get(“items”).
- If item\_codes.
  - Set stock\_items from Platform.db.get\_values(“Item”, mapping(“name” → list(“in”, item\_codes), “is\_stock\_item” → 1), pluck = “name”, cache = true).
- Return stock\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L4680) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L325)

<a id="op-ce756b414b789a"></a>
### Accounts Controller.get asset items

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_asset_items`

**Inputs** self.

**Record and data access** read “Item” via get\_values.

**Explicit results** asset\_items.

**Local steps**

- Set asset\_items from list().
- Set item\_codes from list(set(generator of item.item\_code for item drawn from self.get(“items”))).
  - Draw item from self.get(“items”).
- If item\_codes.
  - Set asset\_items from Platform.db.get\_values(“Item”, mapping(“name” → list(“in”, item\_codes), “is\_fixed\_asset” → 1), pluck = “name”, cache = true).
- Return asset\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L4929) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L318)

<a id="op-4df91a5de4f2e8"></a>
### Accounts Controller.calculate total advance from ledger

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_calculate_total_advance_from_ledger`

**Inputs** self.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.against\_voucher\_type equals nested operand in the contract.doctype).where(adv.against\_voucher\_no equals s ….

**Local steps**

- Set adv from Platform.qb.DocType(“Advance Payment Ledger Entry”).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.against\_voucher\_type equals nested operand in the contract.doctype).where(adv.against\_voucher\_no equals s ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L598) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L303)

<a id="op-92279463a2a77e"></a>
### Accounts Controller.set total advance paid

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_total_advance_paid`

**Inputs** self.

**State and service calls** request set\_value on self.doctype · call db\_set on self.

**Local steps**

- Set advance from self.calculate\_total\_advance\_from\_ledger().
- Set advance\_paid from 0.
- If advance.
  - Set advance from advance at 0.
  - Set advance\_paid from flt(advance.amount, self.precision(“advance\_paid”)).
  - If advance.account\_currency.
    - Set self.party\_account\_currency from advance.account\_currency.
    - Evaluate Platform.db.set\_value(self.doctype, self.name, “party\_account\_currency”, advance.account\_currency).
- Evaluate self.db\_set(“advance\_paid”, advance\_paid).
- Evaluate self.set\_advance\_payment\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate total advance from ledger](operations-005.md#op-4df91a5de4f2e8), [set advance payment status](operations-005.md#op-d4f48e8130a8f0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L654) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L358)

<a id="op-d4f48e8130a8f0"></a>
### Accounts Controller.set advance payment status

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_advance_payment_status`

**Inputs** self.

**Record and data access** read “Payment Request” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Unable to find exchange rate from {0} to {1} on {2}”.format(self.party\_account\_currency, self.company\_currency, self.transaction\_date).

**Local steps**

- Set new\_status from no value.
- Set PaymentRequest from Platform.qb.DocType(“Payment Request”).
- Set requested\_paid\_amount from Platform.get\_value(doctype = “Payment Request”, filters = mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name, “docstatus” → 1), fieldname = Sum((PaymentRequest.grand\_total − PaymentRe ….
- Set advance\_paid from flt(self.get(“advance\_paid”)).
- If (advance\_paid and self.get(“party\_account\_currency”) differs from self.get(“currency”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in advance\_paid → self.get(“party\_account\_currency”) differs from self.get(“currency”).
  - Set exchange\_rate from get\_exchange\_rate(self.party\_account\_currency, self.company\_currency, self.transaction\_date).
  - If not exchange\_rate.
    - Call the validation error handler Platform.throw(translated “Unable to find exchange rate from {0} to {1} on {2}”.format(self.party\_account\_currency, self.company\_currency, self.transaction\_date)).
  - Set advance\_paid from ((advance\_paid × exchange\_rate) ÷ self.conversion\_rate).
- Set paid\_amount from max(advance\_paid, flt(requested\_paid\_amount)).
- If not paid\_amount.
  - If self.doctype belongs to self.get\_advance\_payment\_doctypes(payment\_type = “receivable”).
    - Set new\_status from “Not Requested” when requested\_paid\_amount is identical to no value, otherwise “Requested”.
      - Value choice on requested\_paid\_amount is identical to no value — true gives “Not Requested”, false gives “Requested”.
  - Otherwise.
    - If self.doctype belongs to self.get\_advance\_payment\_doctypes(payment\_type = “payable”).
      - Set new\_status from “Not Initiated” when requested\_paid\_amount is identical to no value, otherwise “Initiated”.
        - Value choice on requested\_paid\_amount is identical to no value — true gives “Not Initiated”, false gives “Initiated”.
- Otherwise.
  - Set total\_amount from (self.get(“rounded\_total”) or self.get(“grand\_total”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“rounded\_total”) → self.get(“grand\_total”).
  - Set new\_status from “Fully Paid” when flt(paid\_amount, self.precision(“grand\_total”)) ≥ total\_amount, otherwise “Partially Paid”.
    - Value choice on flt(paid\_amount, self.precision(“grand\_total”)) ≥ total\_amount — true gives “Fully Paid”, false gives “Partially Paid”.
- If new\_status equals self.advance\_payment\_status.
  - Return no value.
- Evaluate self.db\_set(“advance\_payment\_status”, new\_status, update\_modified = false).
- Evaluate self.set\_status(update = true).
- Evaluate self.notify\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get advance payment doctypes](operations-006.md#op-26bd158ad36a78).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L349)

<a id="op-055321bad49b7a"></a>
### Accounts Controller.company abbr

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_company_abbreviation`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** self.\_abbr.

**Local steps**

- If not hasattr(self, “\_abbr”).
  - Set self.\_abbr from Platform.get\_cached\_value(“Company”, self.company, “abbr”).
- Return self.\_abbr.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “abbr”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L5358) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L310)

<a id="op-7d4bd57c59cc11"></a>
### Accounts Controller.raise missing debit credit account error

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_raise_missing_debit_credit_account_error`

**Inputs** self, party\_type, party.

**Explicit failure paths** validation helper with AccountMissingError — message.

**Local steps**

- Set db\_or\_cr from Platform.bold(translated “Debit To”) when self.doctype equals “Sales Invoice”, otherwise Platform.bold(translated “Credit To”).
  - Value choice on self.doctype equals “Sales Invoice” — true gives Platform.bold(translated “Debit To”), false gives Platform.bold(translated “Credit To”).
- Set rec\_or\_pay from “Receivable” when self.doctype equals “Sales Invoice”, otherwise “Payable”.
  - Value choice on self.doctype equals “Sales Invoice” — true gives “Receivable”, false gives “Payable”.
- Set link\_to\_party from Platform.utils.get\_link\_to\_form(party\_type, party).
- Set link\_to\_company from Platform.utils.get\_link\_to\_form(“Company”, self.company).
- Set message from translated “{0} Account not found against Customer {1}.”.format(db\_or\_cr, (Platform.bold(party) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.bold(party) → empty text.
- Update message using + ((text in the contract + translated “Please set one of the following:”) + text in the contract).
- Update message using + ((text in the contract + translated “'Account' in the Accounting section of Customer {0}”.format(link\_to\_party)) + “&lt;/li&gt;”).
- Update message using + ((text in the contract + translated “'Default {0} Account' in Company {1}”.format(rec\_or\_pay, link\_to\_company)) + “&lt;/li&gt;&lt;/ul&gt;”).
- Call the validation error handler Platform.throw(message, title = translated “Account Missing”, exc = AccountMissingError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L5490) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L341)

<a id="op-a9be434f8ccafd"></a>
### Accounts Controller.validate party

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party`

**Inputs** self.

**Local steps**

- Set tuple(party\_type, party) from self.get\_party().
- Evaluate validate\_party\_frozen\_disabled(self.company, party\_type, party).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L969) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L209)

<a id="op-01e46d4caaf606"></a>
### Accounts Controller.validate party specific items

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party_specific_items`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Item {1} is not allowed for {2} {3}.”.format(row.idx, Platform.bold(row.item\_code), translated party\_type, Platform.bold(party)).

**Local steps**

- Set tuple(party\_type, party) from self.get\_party().
- If self.get(“quotation\_to”) equals “Customer”.
  - Set party from self.party\_name.
- If not party.
  - Return no value.
- Set allowed\_items\_condition from get\_allowed\_items\_condition(party\_type, party).
- Set rows from self.get\_rows\_for\_item\_restrictions() when allowed\_items\_condition is distinct from no value, otherwise list().
  - Value choice on allowed\_items\_condition is distinct from no value — true gives self.get\_rows\_for\_item\_restrictions(), false gives list().
- If not rows.
  - Return no value.
- Set item from Platform.qb.DocType(“Item”).
- Set allowed\_items from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(nested operand in the contract(nested operand in the contract))).where(allowed\_items\_condition).run( ….
  - Draw row from rows.
- For each row in rows.
  - If row.item\_code does not belong to allowed\_items.
    - Call the validation error handler Platform.throw(translated “Row {0}: Item {1} is not allowed for {2} {3}.”.format(row.idx, Platform.bold(row.item\_code), translated party\_type, Platform.bold(party)), title = translated “Item Restricted for Party”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3), [get rows for item restrictions](operations-005.md#op-2050c965a92583).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L215)

<a id="op-2050c965a92583"></a>
### Accounts Controller.get rows for item restrictions

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_rows_for_item_restrictions`

**Inputs** self.

**Record and data access** read formatted text {self.doctype} Item via get\_all.

**Explicit results** rows · list of row for row drawn from rows where (flt(row.qty) &gt; 0 or original\_items.get(row.get(reference\_field)) differs from row.item\_code).

**Local steps**

- Set rows from list of row for row drawn from self.get(“items”) where row.item\_code.
  - Draw row from self.get(“items”), keep a combination only if (row.item\_code).
- If not (self.get(“is\_return”) and self.get(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → self.get(“return\_against”).
  - Return rows.
- Set reference\_field from “dn\_detail” when self.doctype equals “Delivery Note”, otherwise (Platform.scrub(self.doctype) + “\_item”).
  - Value choice on self.doctype equals “Delivery Note” — true gives “dn\_detail”, false gives (Platform.scrub(self.doctype) + “\_item”).
- Set original\_items from dict(Platform.get\_all(formatted text {self.doctype} Item, filters = mapping(“parent” → self.return\_against, “docstatus” → 1), fields = list(“name”, “item\_code”), as\_list = true)).
- Return list of row for row drawn from rows where (flt(row.qty) &gt; 0 or original\_items.get(row.get(reference\_field)) differs from row.item\_code).
  - Draw row from rows, keep a combination only if ((flt(row.qty) &gt; 0 or original\_items.get(row.get(reference\_field)) differs from row.item\_code)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(row.qty) &gt; 0 → original\_items.get(row.get(reference\_field)) differs from row.item\_code.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L919) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L159)

<a id="op-1120b9a6c920b3"></a>
### Accounts Controller.get party

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_party`

**Inputs** self.

**Explicit results** tuple(party\_type, party).

**Local steps**

- Set party\_type from no value.
- If self.doctype belongs to tuple(“Opportunity”, “Quotation”, “Sales Order”, “Delivery Note”, …).
  - Set party\_type from “Customer”.
- Otherwise.
  - If self.doctype belongs to tuple(“Supplier Quotation”, “Purchase Order”, “Purchase Receipt”, “Purchase Invoice”).
    - Set party\_type from “Supplier”.
  - Otherwise.
    - If self.meta.get\_field(“customer”).
      - Set party\_type from “Customer”.
    - Otherwise.
      - If self.meta.get\_field(“supplier”).
        - Set party\_type from “Supplier”.
- Set party from self.get(party\_type.lower()) when party\_type, otherwise no value.
  - Value choice on party\_type — true gives self.get(party\_type.lower()), false gives no value.
- Return tuple(party\_type, party).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L617) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L322)

<a id="op-647bca4fdf7600"></a>
### Accounts Controller.validate currency

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_currency`

**Inputs** self.

**Explicit failure paths** validation helper with InvalidCurrency — translated “Accounting Entry for {0}: {1} can only be made in currency: {2}”.format(party\_type, party, party\_account\_currency).

**Local steps**

- If self.get(“currency”).
  - Set tuple(party\_type, party) from self.get\_party().
  - If (party\_type and party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
    - Set party\_account\_currency from get\_party\_account\_currency(party\_type, party, self.company).
    - If (party\_account\_currency and party\_account\_currency differs from self.company\_currency and self.currency differs from party\_account\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account\_currency → party\_account\_currency differs from self.company\_currency → self.currency differs from party\_account\_currency.
      - Call the validation error handler Platform.throw(translated “Accounting Entry for {0}: {1} can only be made in currency: {2}”.format(party\_type, party, party\_account\_currency), InvalidCurrency).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L197)

<a id="op-927957e38d80fe"></a>
### Accounts Controller.validate party account currency

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party_account_currency`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Party Account {0} currency ({1}) and document currency ({2}) should be same”.format(Platform.bold(party\_account), party\_account\_currency, self.currency).

**Local steps**

- If self.doctype does not belong to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Return no value.
- If self.is\_opening equals “Yes”.
  - Return no value.
- Set tuple(party\_type, party) from self.get\_party().
- Set party\_gle\_currency from get\_party\_gle\_currency(party\_type, party, self.company).
- Set party\_account from self.get(“debit\_to”) when self.doctype equals “Sales Invoice”, otherwise self.get(“credit\_to”).
  - Value choice on self.doctype equals “Sales Invoice” — true gives self.get(“debit\_to”), false gives self.get(“credit\_to”).
- Set party\_account\_currency from get\_account\_currency(party\_account).
- Set allow\_multi\_currency\_invoices\_against\_single\_party\_account from Platform.db.get\_singles\_value(“Accounts Settings”, “allow\_multi\_currency\_invoices\_against\_single\_party\_account”).
- If (not party\_gle\_currency and party\_account\_currency differs from self.currency and not allow\_multi\_currency\_invoices\_against\_single\_party\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not party\_gle\_currency → party\_account\_currency differs from self.currency → not allow\_multi\_currency\_invoices\_against\_single\_party\_account.
  - Call the validation error handler Platform.throw(translated “Party Account {0} currency ({1}) and document currency ({2}) should be same”.format(Platform.bold(party\_account), party\_account\_currency, self.currency)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L970) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L210)

<a id="op-06927ca4e8c7e3"></a>
### Accounts Controller.delink advance entries

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_delink_advance_entries`

**Inputs** self, linked\_doc\_name.

**State and service calls** request set\_value on self.doctype.

**Local steps**

- Set total\_allocated\_amount from 0.
- For each adv in self.advances.
  - Set consider\_for\_total\_advance from true.
  - If adv.reference\_name equals linked\_doc\_name.
    - Set doctype from Platform.qb.DocType((self.doctype + “ Advance”)).
    - Evaluate nested operand in the contract(nested operand in the contract).delete().where(doctype.name equals adv.name).run().
    - Set consider\_for\_total\_advance from false.
  - If consider\_for\_total\_advance.
    - Update total\_allocated\_amount using + flt(adv.allocated\_amount, adv.precision(“allocated\_amount”)).
- Evaluate Platform.db.set\_value(self.doctype, self.name, “total\_advance”, total\_allocated\_amount, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L313)

<a id="op-07f7d4bc6202e7"></a>
### Accounts Controller.group similar items

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_group_similar_items`

**Inputs** self.

**Local steps**

- Set grouped\_items from mapping().
- Set count from 0.
- Set fields\_to\_group from Platform.get\_hooks(“fields\_for\_group\_similar\_items”).
- Set fields\_to\_group from set(fields\_to\_group).
- For each item in self.items.
  - Set item\_values from grouped\_items.setdefault(item.item\_code, defaultdict(int)).
  - For each field in fields\_to\_group.
    - Update item\_values at field using + item.get(field, 0).
- Set duplicate\_list from list().
- For each item in self.items.
  - If item.item\_code belongs to grouped\_items.
    - Update count using + 1.
    - For each field in fields\_to\_group.
      - Evaluate item.set(field, grouped\_items at item.item\_code at field).
    - If item.qty.
      - Set item.rate from flt((flt(item.amount) ÷ flt(item.qty)), item.precision(“rate”)).
    - Otherwise.
      - Set item.rate from 0.
    - Set item.idx from count.
    - Remove grouped\_items at item.item\_code.
  - Otherwise.
    - Evaluate duplicate\_list.append(item).
- For each item in duplicate\_list.
  - Evaluate self.remove(item).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“fields\_for\_group\_similar\_items”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L6238) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L328)

<a id="op-f477c9b4096cad"></a>
### Accounts Controller.set payment schedule

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_payment_schedule`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Payment Terms Template” via get\_value.

**Explicit results** no value.

**Local steps**

- If ((self.doctype equals “Sales Invoice” and self.is\_pos) or self.get(“is\_opening”) equals “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.doctype equals “Sales Invoice” and self.is\_pos) → self.get(“is\_opening”) equals “Yes”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_pos.
  - Set self.payment\_terms\_template from empty text.
  - Return no value.
- Set party\_account\_currency from self.get(“party\_account\_currency”).
- If not party\_account\_currency.
  - Set tuple(party\_type, party) from self.get\_party().
  - If (party\_type and party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
    - Set party\_account\_currency from get\_party\_account\_currency(party\_type, party, self.company).
- Set posting\_date from (self.get(“bill\_date”) or self.get(“posting\_date”) or self.get(“transaction\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“bill\_date”) → self.get(“posting\_date”) → self.get(“transaction\_date”).
- Set date from self.get(“due\_date”).
- Set due\_date from (date or posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in date → posting\_date.
- Set base\_grand\_total from flt((self.get(“base\_rounded\_total”) or self.base\_grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“base\_rounded\_total”) → self.base\_grand\_total.
- Set grand\_total from flt((self.get(“rounded\_total”) or self.grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“rounded\_total”) → self.grand\_total.
- Set automatically\_fetch\_payment\_terms from 0.
- If self.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”, “Sales Order”).
  - Set tuple(po\_or\_so, doctype, fieldname) from self.get\_order\_details().
  - Set automatically\_fetch\_payment\_terms from cint(Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”)).
  - If self.doctype differs from “Sales Order”.
    - Set base\_grand\_total from (base\_grand\_total − flt(self.base\_write\_off\_amount)).
    - Set grand\_total from (grand\_total − flt(self.write\_off\_amount)).
- If self.get(“total\_advance”).
  - If party\_account\_currency equals self.company\_currency.
    - Update base\_grand\_total using − self.get(“total\_advance”).
    - Set grand\_total from flt((base\_grand\_total ÷ self.get(“conversion\_rate”)), self.precision(“grand\_total”)).
  - Otherwise.
    - Update grand\_total using − self.get(“total\_advance”).
    - Set base\_grand\_total from flt((grand\_total × self.get(“conversion\_rate”)), self.precision(“base\_grand\_total”)).
- If not self.get(“payment\_schedule”).
  - If (self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “Sales Order”) and automatically\_fetch\_payment\_terms and self.linked\_order\_has\_payment\_terms(po\_or\_so, fieldname, doctype)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “Sales Order”) → automatically\_fetch\_payment\_terms → self.linked\_order\_has\_payment\_terms(po\_or\_so, fieldname, doctype).
    - Evaluate self.fetch\_payment\_terms\_from\_order(po\_or\_so, doctype, grand\_total, base\_grand\_total, …).
    - If self.get(“payment\_terms\_template”).
      - Set self.ignore\_default\_payment\_terms\_template from 1.
  - Otherwise.
    - If self.get(“payment\_terms\_template”).
      - Set data from \_get\_payment\_terms(self.payment\_terms\_template, posting\_date, grand\_total, base\_grand\_total).
      - For each item in data.
        - Evaluate self.append(“payment\_schedule”, item).
    - Otherwise.
      - If self.doctype does not belong to list(“Purchase Receipt”).
        - Set data from dict(due\_date = due\_date, invoice\_portion = 100, payment\_amount = grand\_total, base\_payment\_amount = base\_grand\_total).
        - Evaluate self.append(“payment\_schedule”, data).
- Set allocate\_payment\_based\_on\_payment\_terms from Platform.db.get\_value(“Payment Terms Template”, self.payment\_terms\_template, “allocate\_payment\_based\_on\_payment\_terms”).
- If not (automatically\_fetch\_payment\_terms and allocate\_payment\_based\_on\_payment\_terms and self.linked\_order\_has\_payment\_terms(po\_or\_so, fieldname, doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in automatically\_fetch\_payment\_terms → allocate\_payment\_based\_on\_payment\_terms → self.linked\_order\_has\_payment\_terms(po\_or\_so, fieldname, doctype).
  - Set keep\_settled from (self.docstatus equals 1 and getattr(self, “\_action”, no value) differs from “submit”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → getattr(self, “\_action”, no value) differs from “submit”.
  - For each d in self.get(“payment\_schedule”).
    - If d.invoice\_portion.
      - Set d.payment\_amount from flt(((grand\_total × flt(d.invoice\_portion)) ÷ 100), d.precision(“payment\_amount”)).
      - Set d.base\_payment\_amount from flt(((base\_grand\_total × flt(d.invoice\_portion)) ÷ 100), d.precision(“base\_payment\_amount”)).
    - Otherwise.
      - If not d.invoice\_portion.
        - Set d.base\_payment\_amount from flt((d.payment\_amount × self.get(“conversion\_rate”)), d.precision(“base\_payment\_amount”)).
    - Evaluate self.set\_term\_outstanding(d, keep\_settled).
- Otherwise.
  - Evaluate self.fetch\_payment\_terms\_from\_order(po\_or\_so, doctype, grand\_total, base\_grand\_total, …).
  - Set self.ignore\_default\_payment\_terms\_template from 1.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3), [get order details](operations-006.md#op-4057557ccfe33b), [linked order has payment terms](operations-006.md#op-6610ba99afa59e), [fetch payment terms from order](operations-006.md#op-4c933bde1f3168), [set term outstanding](operations-006.md#op-c88bf097ec8aec).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “automatically\_fetch\_payment\_terms”) · selected callable from getattr(self, “\_action”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L186)
