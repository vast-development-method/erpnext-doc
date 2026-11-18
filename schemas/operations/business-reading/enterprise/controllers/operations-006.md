# Shared transaction rules · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-c88bf097ec8aec"></a>
### Accounts Controller.set term outstanding

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_term_outstanding`

**Inputs** self, term, keep\_settled.

**Declared result** no value.

**Local steps**

- Set settled, base\_settled from 0.
- If keep\_settled.
  - Set settled from (flt(term.paid\_amount) + flt(term.discounted\_amount)).
  - Set base\_settled from (flt(term.base\_paid\_amount) + (flt(term.discounted\_amount) × flt(self.get(“conversion\_rate”)))).
- Set term.outstanding from flt((term.payment\_amount − settled), term.precision(“outstanding”)).
- Set term.base\_outstanding from flt((term.base\_payment\_amount − base\_settled), term.precision(“base\_outstanding”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L189)

<a id="op-4057557ccfe33b"></a>
### Accounts Controller.get order details

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_order_details`

**Inputs** self.

**Explicit results** tuple(no value, no value, no value) · tuple(prev\_doc, prev\_doctype, prev\_doctype\_name).

**Local steps**

- If not self.get(“items”).
  - Return tuple(no value, no value, no value).
- If self.doctype equals “Sales Invoice”.
  - Set prev\_doc from self.get(“items”) at 0.get(“sales\_order”).
  - Set prev\_doctype from “Sales Order”.
  - Set prev\_doctype\_name from “sales\_order”.
- Otherwise.
  - If self.doctype equals “Purchase Invoice”.
    - Set prev\_doc from self.get(“items”) at 0.get(“purchase\_order”).
    - Set prev\_doctype from “Purchase Order”.
    - Set prev\_doctype\_name from “purchase\_order”.
  - Otherwise.
    - Set prev\_doc from self.get(“items”) at 0.get(“prevdoc\_docname”).
    - Set prev\_doctype from “Quotation”.
    - Set prev\_doctype\_name from “prevdoc\_docname”.
- Return tuple(prev\_doc, prev\_doctype, prev\_doctype\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L916) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L156)

<a id="op-6610ba99afa59e"></a>
### Accounts Controller.linked order has payment terms

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_linked_order_has_payment_terms`

**Inputs** self, po\_or\_so, fieldname, doctype.

**Explicit results** true · false.

**Local steps**

- If (po\_or\_so and self.all\_items\_have\_same\_po\_or\_so(po\_or\_so, fieldname)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in po\_or\_so → self.all\_items\_have\_same\_po\_or\_so(po\_or\_so, fieldname).
  - If self.linked\_order\_has\_payment\_terms\_template(po\_or\_so, doctype).
    - Return true.
  - Otherwise.
    - If self.linked\_order\_has\_payment\_schedule(po\_or\_so).
      - Return true.
- Return false.

**Methods declared on this owner** [all items have same po or so](operations-006.md#op-49cd3875697b19), [linked order has payment terms template](operations-006.md#op-a3bc89a951736e), [linked order has payment schedule](operations-006.md#op-60e0ef9802242c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L174)

<a id="op-49cd3875697b19"></a>
### Accounts Controller.all items have same po or so

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_all_items_have_same_po_or_so`

**Inputs** self, po\_or\_so, fieldname.

**Explicit results** false · true.

**Local steps**

- For each item in self.get(“items”).
  - If item.get(fieldname) differs from po\_or\_so.
    - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L239) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L141)

<a id="op-a3bc89a951736e"></a>
### Accounts Controller.linked order has payment terms template

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_linked_order_has_payment_terms_template`

**Inputs** self, po\_or\_so, doctype.

**Record and data access** read doctype via get\_value.

**Explicit results** Platform.get\_value(doctype, po\_or\_so, “payment\_terms\_template”).

**Local steps**

- Return Platform.get\_value(doctype, po\_or\_so, “payment\_terms\_template”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L175)

<a id="op-60e0ef9802242c"></a>
### Accounts Controller.linked order has payment schedule

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_linked_order_has_payment_schedule`

**Inputs** self, po\_or\_so.

**Record and data access** read “Payment Schedule” via get\_all.

**Explicit results** Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → po\_or\_so)).

**Local steps**

- Return Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → po\_or\_so)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L173)

<a id="op-4c933bde1f3168"></a>
### Accounts Controller.fetch payment terms from order

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_fetch_payment_terms_from_order`

**Inputs** self, po\_or\_so, po\_or\_so\_doctype, grand\_total, base\_grand\_total, automatically\_fetch\_payment\_terms.

**Record and data access** resolve a document from po\_or\_so\_doctype via get\_cached\_doc.

**Local steps**

- Set po\_or\_so from Platform.get\_cached\_doc(po\_or\_so\_doctype, po\_or\_so).
- Set self.payment\_schedule from list().
- Set self.payment\_terms\_template from po\_or\_so.payment\_terms\_template.
- Set posting\_date from (self.get(“bill\_date”) or self.get(“posting\_date”) or self.get(“transaction\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“bill\_date”) → self.get(“posting\_date”) → self.get(“transaction\_date”).
- For each schedule in po\_or\_so.payment\_schedule.
  - Set payment\_schedule from mapping(“payment\_term” → schedule.payment\_term, “due\_date” → schedule.due\_date, “invoice\_portion” → schedule.invoice\_portion, “mode\_of\_payment” → schedule.mode\_of\_payment, …).
  - If automatically\_fetch\_payment\_terms.
    - If schedule.due\_date\_based\_on.
      - Set payment\_schedule at “due\_date” from get\_due\_date(schedule, posting\_date).
      - Set payment\_schedule at “due\_date\_based\_on” from schedule.due\_date\_based\_on.
      - Set payment\_schedule at “credit\_days” from cint(schedule.credit\_days).
      - Set payment\_schedule at “credit\_months” from cint(schedule.credit\_months).
    - If (schedule.discount\_validity\_based\_on and flt(schedule.discount)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule.discount\_validity\_based\_on → flt(schedule.discount).
      - Set payment\_schedule at “discount\_date” from get\_discount\_date(schedule, posting\_date).
      - Set payment\_schedule at “discount\_validity\_based\_on” from schedule.discount\_validity\_based\_on.
      - Set payment\_schedule at “discount\_validity” from cint(schedule.discount\_validity).
    - Set payment\_schedule at “payment\_amount” from flt(((grand\_total × flt(payment\_schedule at “invoice\_portion”)) ÷ 100), schedule.precision(“payment\_amount”)).
    - Set payment\_schedule at “base\_payment\_amount” from flt(((base\_grand\_total × flt(payment\_schedule at “invoice\_portion”)) ÷ 100), schedule.precision(“base\_payment\_amount”)).
    - Set payment\_schedule at “outstanding” from payment\_schedule at “payment\_amount”.
    - If (schedule.discount\_type equals “Amount” and schedule.invoice\_portion).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in schedule.discount\_type equals “Amount” → schedule.invoice\_portion.
      - Set payment\_schedule at “discount” from flt(((flt(schedule.discount) × payment\_schedule at “payment\_amount”) ÷ schedule.payment\_amount), schedule.precision(“payment\_amount”)) when schedule.payment\_amount, otherwise 0.
        - Value choice on schedule.payment\_amount — true gives flt(((flt(schedule.discount) × payment\_schedule at “payment\_amount”) ÷ schedule.payment\_amount), schedule.precision(“payment\_amount”)), false gives 0.
  - Otherwise.
    - Set payment\_schedule at “base\_payment\_amount” from flt((schedule.base\_payment\_amount × self.get(“conversion\_rate”)), schedule.precision(“base\_payment\_amount”)).
  - If not schedule.invoice\_portion.
    - Set payment\_schedule at “payment\_amount” from schedule.payment\_amount.
    - Set payment\_schedule at “base\_payment\_amount” from flt((schedule.payment\_amount × self.get(“conversion\_rate”)), schedule.precision(“base\_payment\_amount”)).
    - Set payment\_schedule at “outstanding” from schedule.payment\_amount.
  - Set payment\_schedule at “base\_outstanding” from payment\_schedule at “base\_payment\_amount”.
  - Evaluate self.append(“payment\_schedule”, payment\_schedule).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(po\_or\_so\_doctype, po\_or\_so).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L151)

<a id="op-11a28093a93974"></a>
### Accounts Controller.set due date

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_due_date`

**Inputs** self.

**Local steps**

- Set due\_dates from list of d.due\_date for d drawn from self.get(“payment\_schedule”) where d.due\_date.
  - Draw d from self.get(“payment\_schedule”), keep a combination only if (d.due\_date).
- If due\_dates.
  - Set self.due\_date from max(due\_dates).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L182)

<a id="op-b1fa17a823f5cb"></a>
### Accounts Controller.validate payment schedule dates

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_payment_schedule_dates`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Due Date in the Payment Terms table cannot be before Posting Date”.format(d.idx) · validation helper — translated “Rows with duplicate due dates in other rows were found: {0}”.format(duplicates).

**Local steps**

- Set dates from list().
- Set li from list().
- If (self.doctype equals “Sales Invoice” and self.is\_pos).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_pos.
  - Return no value.
- For each d in self.get(“payment\_schedule”).
  - If not flt(d.discount).
    - Set d.discount\_date from no value.
  - Evaluate d.validate\_from\_to\_dates(“discount\_date”, “due\_date”).
  - If (self.doctype belongs to list(“Sales Order”, “Quotation”) and getdate(d.due\_date) &lt; getdate(self.transaction\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Sales Order”, “Quotation”) → getdate(d.due\_date) &lt; getdate(self.transaction\_date).
    - Call the validation error handler Platform.throw(translated “Row {0}: Due Date in the Payment Terms table cannot be before Posting Date”.format(d.idx)).
  - Otherwise.
    - If d.due\_date belongs to dates.
      - Evaluate li.append(translated “{0} in row {1}”.format(d.due\_date, d.idx)).
  - Evaluate dates.append(d.due\_date).
- If li.
  - Set duplicates from (text in the contract + text in the contract.join(li)).
  - Call the validation error handler Platform.throw(translated “Rows with duplicate due dates in other rows were found: {0}”.format(duplicates), title = translated “Payment Schedule”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L217)

<a id="op-c2ce7713c31da1"></a>
### Accounts Controller.validate payment schedule amount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_payment_schedule_amount`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Total Payment Amount in Payment Schedule must be equal to Grand / Rounded Total”.

**Local steps**

- If ((self.doctype equals “Sales Invoice” and self.is\_pos) or self.get(“is\_opening”) equals “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.doctype equals “Sales Invoice” and self.is\_pos) → self.get(“is\_opening”) equals “Yes”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_pos.
  - Return no value.
- If self.get(“payment\_schedule”).
  - Set total from 0.
  - Set base\_total from 0.
  - For each d in self.get(“payment\_schedule”).
    - Update total using + flt(d.payment\_amount, d.precision(“payment\_amount”)).
    - Update base\_total using + flt(d.base\_payment\_amount, d.precision(“base\_payment\_amount”)).
  - Set tuple(grand\_total, base\_grand\_total) from self.get\_payment\_schedule\_grand\_totals().
  - If (abs((flt(total, nested operand in the contract.precision(“grand\_total”)) − flt(grand\_total, nested operand in the contract.precision(“grand\_total”)))) &gt; 0.1 or abs((flt(base\_total, nested operand in the c ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in abs((flt(total, self.precision(“grand\_total”)) − flt(grand\_total, self.precision(“grand\_total”)))) &gt; 0.1 → abs((flt(base\_total, self.precision(“base\_grand\_total”)) − flt(base\_grand\_total, self.precision(“base\_grand\_total”)))) &gt; 0.1.
    - Call the validation error handler Platform.throw(translated “Total Payment Amount in Payment Schedule must be equal to Grand / Rounded Total”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get payment schedule grand totals](operations-006.md#op-d37f01375d26dd).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L216)

<a id="op-d37f01375d26dd"></a>
### Accounts Controller.get payment schedule grand totals

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_payment_schedule_grand_totals`

**Inputs** self.

**Explicit results** tuple(grand\_total, base\_grand\_total).

**Local steps**

- Set party\_account\_currency from self.get(“party\_account\_currency”).
- If not party\_account\_currency.
  - Set tuple(party\_type, party) from self.get\_party().
  - If (party\_type and party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
    - Set party\_account\_currency from get\_party\_account\_currency(party\_type, party, self.company).
- Set base\_grand\_total from flt((self.get(“base\_rounded\_total”) or self.base\_grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“base\_rounded\_total”) → self.base\_grand\_total.
- Set grand\_total from flt((self.get(“rounded\_total”) or self.grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“rounded\_total”) → self.grand\_total.
- If self.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Set base\_grand\_total from (base\_grand\_total − flt(self.base\_write\_off\_amount)).
  - Set grand\_total from (grand\_total − flt(self.write\_off\_amount)).
- If self.get(“total\_advance”).
  - If party\_account\_currency equals self.company\_currency.
    - Update base\_grand\_total using − self.get(“total\_advance”).
    - Set grand\_total from flt((base\_grand\_total ÷ self.get(“conversion\_rate”)), self.precision(“grand\_total”)).
  - Otherwise.
    - Update grand\_total using − self.get(“total\_advance”).
    - Set base\_grand\_total from flt((grand\_total × self.get(“conversion\_rate”)), self.precision(“base\_grand\_total”)).
- Return tuple(grand\_total, base\_grand\_total).

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L917) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L157)

<a id="op-b402aab8597362"></a>
### Accounts Controller.is rounded total disabled

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_is_rounded_total_disabled`

**Inputs** self.

**Record and data access** read “Global Defaults” via get\_single\_value.

**Explicit results** self.disable\_rounded\_total · Platform.db.get\_single\_value(“Global Defaults”, “disable\_rounded\_total”).

**Local steps**

- If self.meta.get\_field(“disable\_rounded\_total”).
  - Return self.disable\_rounded\_total.
- Otherwise.
  - Return Platform.db.get\_single\_value(“Global Defaults”, “disable\_rounded\_total”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “disable\_rounded\_total”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0368.json#L6841) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L334)

<a id="op-7d65c0d8977f92"></a>
### Accounts Controller.set inter company account

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_inter_company_account`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — msg.

**Local steps**

- If (self.is\_internal\_transfer() and not self.unrealized\_profit\_loss\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → not self.unrealized\_profit\_loss\_account.
  - Set unrealized\_profit\_loss\_account from Platform.get\_cached\_value(“Company”, self.company, “unrealized\_profit\_loss\_account”).
  - If not unrealized\_profit\_loss\_account.
    - Set msg from translated “Please select Unrealized Profit / Loss account or add default Unrealized Profit / Loss account account for c …”.format(Platform.bold(self.company)).
    - Call the validation error handler Platform.throw(msg).
  - Set self.unrealized\_profit\_loss\_account from unrealized\_profit\_loss\_account.

If control reaches the end, it returns no value.

**Methods declared on this owner** [is internal transfer](operations-006.md#op-13fa6c1b2d5ba8).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “unrealized\_profit\_loss\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L183)

<a id="op-13fa6c1b2d5ba8"></a>
### Accounts Controller.is internal transfer

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_is_internal_transfer`

**Inputs** self.

**Explicit results** false · true.

**Local steps**

- If self.doctype belongs to tuple(“Sales Invoice”, “Delivery Note”, “Sales Order”).
  - Set internal\_party\_field from “is\_internal\_customer”.
- Otherwise.
  - If self.doctype belongs to tuple(“Purchase Invoice”, “Purchase Receipt”, “Purchase Order”).
    - Set internal\_party\_field from “is\_internal\_supplier”.
  - Otherwise.
    - Return false.
- If (self.get(internal\_party\_field) and self.represents\_company equals self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(internal\_party\_field) → self.represents\_company equals self.company.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L331)

<a id="op-af87cb1380583a"></a>
### Accounts Controller.process common party accounting

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_process_common_party_accounting`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- Set is\_invoice from self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
- If not is\_invoice.
  - Return no value.
- If Platform.get\_single\_value(“Accounts Settings”, “enable\_common\_party\_accounting”).
  - Set party\_link from self.get\_common\_party\_link().
  - If (party\_link and self.outstanding\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_link → self.outstanding\_amount.
    - Evaluate self.create\_advance\_and\_reconcile(party\_link).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get common party link](operations-006.md#op-b573031d193a7b), [create advance and reconcile](operations-006.md#op-ec7d7f6039fd77).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_common\_party\_accounting”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L340)

<a id="op-b573031d193a7b"></a>
### Accounts Controller.get common party link

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_common_party_link`

**Inputs** self.

**Record and data access** read “Party Link” via get\_value.

**Explicit results** Platform.db.get\_value(doctype = “Party Link”, filters = mapping(“secondary\_role” → party\_type, “secondary\_party” → party), fieldname = list(“primary\_role”, “primary\_party”), as\_dict = true).

**Local steps**

- Set tuple(party\_type, party) from self.get\_party().
- Return Platform.db.get\_value(doctype = “Party Link”, filters = mapping(“secondary\_role” → party\_type, “secondary\_party” → party), fieldname = list(“primary\_role”, “primary\_party”), as\_dict = true).

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L319)

<a id="op-ec7d7f6039fd77"></a>
### Accounts Controller.create advance and reconcile

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_create_advance_and_reconcile`

**Inputs** self, party\_link.

**State and service calls** request new\_doc for “Journal Entry” · call save on jv · call submit on jv.

**Local steps**

- Set tuple(secondary\_party\_type, secondary\_party) from self.get\_party().
- Set tuple(primary\_party\_type, primary\_party) from tuple(party\_link.primary\_role, party\_link.primary\_party).
- Set primary\_account from get\_party\_account(primary\_party\_type, primary\_party, self.company).
- Set secondary\_account from get\_party\_account(secondary\_party\_type, secondary\_party, self.company).
- Set primary\_account\_currency from get\_account\_currency(primary\_account).
- Set secondary\_account\_currency from get\_account\_currency(secondary\_account).
- Set default\_currency from Enterprise.get\_company\_currency(self.company).
- Set multi\_currency from (primary\_account\_currency differs from default\_currency or secondary\_account\_currency differs from default\_currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in primary\_account\_currency differs from default\_currency → secondary\_account\_currency differs from default\_currency.
- Set jv from Platform.new\_doc(“Journal Entry”).
- Set jv.voucher\_type from “Journal Entry”.
- Set jv.posting\_date from self.posting\_date.
- Set jv.company from self.company.
- Set jv.remark from formatted text Adjustment for {self.doctype} {self.name}.
- Set jv.is\_system\_generated from true.
- Set reconcilation\_entry from Platform.\_dict().
- Set advance\_entry from Platform.\_dict().
- Set reconcilation\_entry.account from secondary\_account.
- Set reconcilation\_entry.party\_type from secondary\_party\_type.
- Set reconcilation\_entry.party from secondary\_party.
- Set reconcilation\_entry.reference\_type from self.doctype.
- Set reconcilation\_entry.reference\_name from self.name.
- Set reconcilation\_entry.cost\_center from (self.cost\_center or Enterprise.get\_default\_cost\_center(self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → Enterprise.get\_default\_cost\_center(self.company).
- Set advance\_entry.account from primary\_account.
- Set advance\_entry.party\_type from primary\_party\_type.
- Set advance\_entry.party from primary\_party.
- Set advance\_entry.cost\_center from (self.cost\_center or Enterprise.get\_default\_cost\_center(self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → Enterprise.get\_default\_cost\_center(self.company).
- Set advance\_entry.is\_advance from “No” when self.is\_return, otherwise “Yes”.
  - Value choice on self.is\_return — true gives “No”, false gives “Yes”.
- Set dimensions\_dict from Platform.\_dict().
- Set active\_dimensions from get\_dimensions() at 0.
- For each dim in active\_dimensions.
  - Set dimensions\_dict at dim.fieldname from self.get(dim.fieldname).
- Evaluate reconcilation\_entry.update(dimensions\_dict).
- Evaluate advance\_entry.update(dimensions\_dict).
- If multi\_currency.
  - Set exc\_rate\_primary\_to\_default from 1 when primary\_account\_currency equals default\_currency, otherwise get\_exchange\_rate(primary\_account\_currency, default\_currency, self.posting\_date).
    - Value choice on primary\_account\_currency equals default\_currency — true gives 1, false gives get\_exchange\_rate(primary\_account\_currency, default\_currency, self.posting\_date).
  - Set exc\_rate\_secondary\_to\_default from 1 when secondary\_account\_currency equals default\_currency, otherwise get\_exchange\_rate(secondary\_account\_currency, default\_currency, self.posting\_date).
    - Value choice on secondary\_account\_currency equals default\_currency — true gives 1, false gives get\_exchange\_rate(secondary\_account\_currency, default\_currency, self.posting\_date).
  - Set exc\_rate\_secondary\_to\_primary from 1 when secondary\_account\_currency equals primary\_account\_currency, otherwise get\_exchange\_rate(secondary\_account\_currency, primary\_account\_currency, self.posting\_date).
    - Value choice on secondary\_account\_currency equals primary\_account\_currency — true gives 1, false gives get\_exchange\_rate(secondary\_account\_currency, primary\_account\_currency, self.posting\_date).
  - Set outstanding\_amount from abs(self.outstanding\_amount).
  - Set os\_in\_default\_currency from (outstanding\_amount × exc\_rate\_secondary\_to\_default).
  - Set os\_in\_primary\_currency from (outstanding\_amount × exc\_rate\_secondary\_to\_primary).
  - Set reconciliation\_is\_credit from self.doctype equals “Sales Invoice” differs from bool(self.is\_return).
  - Evaluate \_set\_je\_amounts(reconcilation\_entry, outstanding\_amount, os\_in\_default\_currency, reconciliation\_is\_credit).
  - Evaluate \_set\_je\_amounts(advance\_entry, os\_in\_primary\_currency, os\_in\_default\_currency, not reconciliation\_is\_credit).
  - Set reconcilation\_entry.exchange\_rate from exc\_rate\_secondary\_to\_default.
  - Set advance\_entry.exchange\_rate from exc\_rate\_primary\_to\_default.
- Otherwise.
  - Set outstanding\_amount from abs(self.outstanding\_amount).
  - Set reconciliation\_is\_credit from self.doctype equals “Sales Invoice” differs from bool(self.is\_return).
  - Evaluate \_set\_je\_amounts(reconcilation\_entry, outstanding\_amount, is\_credit = reconciliation\_is\_credit).
  - Evaluate \_set\_je\_amounts(advance\_entry, outstanding\_amount, is\_credit = not reconciliation\_is\_credit).
- Set jv.multi\_currency from multi\_currency.
- Evaluate jv.append(“accounts”, reconcilation\_entry).
- Evaluate jv.append(“accounts”, advance\_entry).
- Evaluate jv.save().
- Evaluate jv.submit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L312)

<a id="op-1f9ccfb64d37e7"></a>
### Accounts Controller.check conversion rate

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_check_conversion_rate`

**Inputs** self.

**State and service calls** msgprint with translated “Conversion rate is 1.00, but document currency is different from company currency”.

**Local steps**

- Set default\_currency from Enterprise.get\_company\_currency(self.company).
- If not default\_currency.
  - Evaluate throw(translated “Please enter default currency in Company Master”).
- If not self.conversion\_rate.
  - Evaluate throw(translated “Conversion rate cannot be 0”).
- If (self.currency equals default\_currency and flt(self.conversion\_rate) differs from 1.0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency equals default\_currency → flt(self.conversion\_rate) differs from 1.0.
  - Evaluate throw(translated “Conversion rate must be 1.00 if document currency is same as company currency”).
- If (self.currency differs from default\_currency and flt(self.conversion\_rate) equals 1.0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency differs from default\_currency → flt(self.conversion\_rate) equals 1.0.
  - Evaluate Platform.msgprint(translated “Conversion rate is 1.00, but document currency is different from company currency”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L229) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L600) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L305)

<a id="op-15e97da08eb5cb"></a>
### Accounts Controller.check finance books

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_check_finance_books`

**Inputs** self, item, asset.

**Explicit failure paths** validation helper — translated “Select finance book for the item {0} at row {1}”.format(item.item\_code, item.idx).

**Local steps**

- If (len(asset.finance\_books) &gt; 1 and not item.get(“finance\_book”) and not self.get(“finance\_book”) and asset.finance\_books at 0.finance\_book).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(asset.finance\_books) &gt; 1 → not item.get(“finance\_book”) → not self.get(“finance\_book”) → asset.finance\_books at 0.finance\_book.
  - Call the validation error handler Platform.throw(translated “Select finance book for the item {0} at row {1}”.format(item.item\_code, item.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L594) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L306)

<a id="op-9741ec29612924"></a>
### Accounts Controller.check if fields updated

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_check_if_fields_updated`

**Inputs** self, fields\_to\_check, child\_tables.

**Explicit results** true · false.

**Local steps**

- Set doc\_before\_update from self.get\_doc\_before\_save().
- Set accounting\_dimensions from list(expanded get\_accounting\_dimensions(), “cost\_center”, “project”).
- Update fields\_to\_check using + accounting\_dimensions.
- For each field in fields\_to\_check.
  - If doc\_before\_update.get(field) differs from self.get(field).
    - Return true.
- For each table in child\_tables.
  - If check\_if\_child\_table\_updated(doc\_before\_update.get(table), self.get(table), child\_tables at table).
    - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L307)

<a id="op-ac6297b4bf1966"></a>
### Accounts Controller.repost accounting entries

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_repost_accounting_entries`

**Inputs** self.

**State and service calls** request new\_doc for “Repost Accounting Ledger” · call insert on repost\_ledger · call submit on repost\_ledger.

**Local steps**

- Set repost\_ledger from Platform.new\_doc(“Repost Accounting Ledger”).
- Set repost\_ledger.company from self.company.
- Evaluate repost\_ledger.append(“vouchers”, mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name)).
- Set repost\_ledger.flags.ignore\_permissions from true.
- Evaluate repost\_ledger.insert().
- Evaluate repost\_ledger.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L347)

<a id="op-26bd158ad36a78"></a>
### Accounts Controller.get advance payment doctypes

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_advance_payment_record_types`

**Inputs** self, payment\_type = no value.

**Declared result** list.

**Explicit results** \_get\_advance\_payment\_doctypes(payment\_type = payment\_type).

**Local steps**

- Return \_get\_advance\_payment\_doctypes(payment\_type = payment\_type).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L1379) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L317)

<a id="op-f1ea3a18396a2b"></a>
### Accounts Controller.set transaction currency and rate in gl map

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_transaction_currency_and_rate_in_general_ledger_map`

**Inputs** self, gl\_entries.

**Local steps**

- For each x in gl\_entries.
  - Set x at “transaction\_currency” from self.currency.
  - Set x at “transaction\_exchange\_rate” from (self.get(“conversion\_rate”) or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“conversion\_rate”) → 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L359)

<a id="op-98d88d3252496e"></a>
### Accounts Controller.has mapped discount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_has_mapped_discount`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** any(generator of item.get(“mapped\_additional\_discount\_amount”) for item drawn from self.get(“items”)).

**Local steps**

- Return any(generator of item.get(“mapped\_additional\_discount\_amount”) for item drawn from self.get(“items”)).
  - Draw item from self.get(“items”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L926) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L166)
