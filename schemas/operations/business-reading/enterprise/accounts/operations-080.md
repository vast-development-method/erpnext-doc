# Accounting and settlement · operations 80

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pos invoice

<a id="op-c4fa1c7ebc3e03"></a>
### POSInvoice.set status

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_set_status`

**Inputs** self, update = false, status = no value, update\_modified = true.

**Record and data access** read “POS Invoice” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.is\_new().
  - If self.get(“amended\_from”).
    - Set self.status from “Draft”.
  - Return no value.
- Set total from (flt(self.rounded\_total) or flt(self.grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.rounded\_total) → flt(self.grand\_total).
- If not status.
  - If self.docstatus equals 2.
    - Set status from “Cancelled”.
  - Otherwise.
    - If self.docstatus equals 1.
      - If self.consolidated\_invoice.
        - Set self.status from “Consolidated”.
      - Otherwise.
        - If (flt(self.outstanding\_amount) &gt; 0 and getdate(self.due\_date) &lt; getdate(nowdate()) and self.is\_discounted and get\_discounting\_status(self.name) equals “Disbursed”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.outstanding\_amount) &gt; 0 → getdate(self.due\_date) &lt; getdate(nowdate()) → self.is\_discounted → get\_discounting\_status(self.name) equals “Disbursed”.
          - Set self.status from “Overdue and Discounted”.
        - Otherwise.
          - If (flt(self.outstanding\_amount) &gt; 0 and getdate(self.due\_date) &lt; getdate(nowdate())).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.outstanding\_amount) &gt; 0 → getdate(self.due\_date) &lt; getdate(nowdate()).
            - Set self.status from “Overdue”.
          - Otherwise.
            - If (0 &lt; flt(self.outstanding\_amount) &lt; total and self.is\_discounted and get\_discounting\_status(self.name) equals “Disbursed”).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in 0 &lt; flt(self.outstanding\_amount) &lt; total → self.is\_discounted → get\_discounting\_status(self.name) equals “Disbursed”.
              - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; flt(self.outstanding\_amount) &lt; total.
              - Set self.status from “Partly Paid and Discounted”.
            - Otherwise.
              - If 0 &lt; flt(self.outstanding\_amount) &lt; total.
                - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; flt(self.outstanding\_amount) &lt; total.
                - Set self.status from “Partly Paid”.
              - Otherwise.
                - If (flt(self.outstanding\_amount) &gt; 0 and getdate(self.due\_date) ≥ getdate(nowdate()) and self.is\_discounted and get\_discounting\_status(self.name) equals “Disbursed”).
                  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.outstanding\_amount) &gt; 0 → getdate(self.due\_date) ≥ getdate(nowdate()) → self.is\_discounted → get\_discounting\_status(self.name) equals “Disbursed”.
                  - Set self.status from “Unpaid and Discounted”.
                - Otherwise.
                  - If (flt(self.outstanding\_amount) &gt; 0 and getdate(self.due\_date) ≥ getdate(nowdate())).
                    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.outstanding\_amount) &gt; 0 → getdate(self.due\_date) ≥ getdate(nowdate()).
                    - Set self.status from “Unpaid”.
                  - Otherwise.
                    - If (flt(self.outstanding\_amount) ≤ 0 and self.is\_return equals 0 and Platform.db.get\_value(“POS Invoice”, mapping(“is\_return” → 1, “return\_against” → self.name, “docstatus” → 1))).
                      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.outstanding\_amount) ≤ 0 → self.is\_return equals 0 → Platform.db.get\_value(“POS Invoice”, mapping(“is\_return” → 1, “return\_against” → self.name, “docstatus” → 1)).
                      - Set self.status from “Credit Note Issued”.
                    - Otherwise.
                      - If self.is\_return equals 1.
                        - Set self.status from “Return”.
                      - Otherwise.
                        - If flt(self.outstanding\_amount) ≤ 0.
                          - Set self.status from “Paid”.
                        - Otherwise.
                          - Set self.status from “Submitted”.
    - Otherwise.
      - Set self.status from “Draft”.
- If update.
  - Evaluate self.db\_set(“status”, self.status, update\_modified = update\_modified).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L538)

<a id="op-a77c7d7c3e9331"></a>
### POSInvoice.set pos fields

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_set_point_of_sale_fields`

**Inputs** self, for\_validate = false.

**Record and data access** resolve a document from “POS Profile” via get\_doc · read “Customer” via get\_value · read “Customer Group” via get\_cached\_value · read “Terms and Conditions” via get\_value · read “Company” via get\_cached\_value.

**Explicit results** profile.

**Explicit failure paths** validation helper — translated “No POS Profile found. Please create a New POS Profile first”.

**Local steps**

- Bind dependencies ItemDetailsCtx, get\_pos\_profile, get\_pos\_profile\_item\_details\_.
- If not self.pos\_profile.
  - Set pos\_profile from (get\_pos\_profile(self.company) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_pos\_profile(self.company) → mapping().
  - If not pos\_profile.
    - Call the validation error handler Platform.throw(translated “No POS Profile found. Please create a New POS Profile first”).
  - Set self.pos\_profile from pos\_profile.get(“name”).
- Set profile from mapping().
- If self.pos\_profile.
  - Set profile from Platform.get\_doc(“POS Profile”, self.pos\_profile).
  - Set self.company from profile.get(“company”).
- If (not self.get(“payments”) and not for\_validate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“payments”) → not for\_validate.
  - Evaluate update\_multi\_mode\_option(self, profile).
- If (self.is\_return and not for\_validate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not for\_validate.
  - Evaluate add\_return\_modes(self, profile).
- If profile.
  - If (not for\_validate and not self.customer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not for\_validate → not self.customer.
    - Set self.customer from profile.customer.
  - Set self.account\_for\_change\_amount from (profile.get(“account\_for\_change\_amount”) or self.account\_for\_change\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in profile.get(“account\_for\_change\_amount”) → self.account\_for\_change\_amount.
  - Set self.set\_warehouse from (profile.get(“warehouse”) or self.set\_warehouse).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in profile.get(“warehouse”) → self.set\_warehouse.
  - For each fieldname in tuple(“currency”, “letter\_head”, “tc\_name”, “company”, …).
    - If not for\_validate.
      - Evaluate self.set(fieldname, profile.get(fieldname)).
  - If self.customer.
    - Set tuple(customer\_price\_list, customer\_group, customer\_currency) from Platform.db.get\_value(“Customer”, self.customer, list(“default\_price\_list”, “customer\_group”, “default\_currency”)).
    - Set customer\_group\_price\_list from Platform.get\_cached\_value(“Customer Group”, customer\_group, “default\_price\_list”).
    - Set selling\_price\_list from (customer\_price\_list or customer\_group\_price\_list or profile.get(“selling\_price\_list”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer\_price\_list → customer\_group\_price\_list → profile.get(“selling\_price\_list”).
    - If (customer\_currency and customer\_currency differs from profile.get(“currency”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in customer\_currency → customer\_currency differs from profile.get(“currency”).
      - Evaluate self.set(“currency”, customer\_currency).
  - Otherwise.
    - Set selling\_price\_list from profile.get(“selling\_price\_list”).
  - If selling\_price\_list.
    - Evaluate self.set(“selling\_price\_list”, selling\_price\_list).
  - For each item in self.get(“items”).
    - If item.get(“item\_code”).
      - Set profile\_details from get\_pos\_profile\_item\_details\_(ItemDetailsCtx(item.as\_dict()), profile.get(“company”), profile).
      - For each tuple(fname, val) in profile\_details.items().
        - If (not for\_validate or (for\_validate and not item.get(fname))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not for\_validate → (for\_validate and not item.get(fname)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → not item.get(fname).
          - Evaluate item.set(fname, val).
  - If (self.tc\_name and not self.terms).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.tc\_name → not self.terms.
    - Set self.terms from Platform.db.get\_value(“Terms and Conditions”, self.tc\_name, “terms”).
  - If (self.taxes\_and\_charges and not len(self.get(“taxes”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.taxes\_and\_charges → not len(self.get(“taxes”)).
    - Evaluate self.set\_taxes().
- If not self.account\_for\_change\_amount.
  - Set self.account\_for\_change\_amount from Platform.get\_cached\_value(“Company”, self.company, “default\_cash\_account”).
- Return profile.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer Group”, customer\_group, “default\_price\_list”), Platform.get\_cached\_value(“Company”, self.company, “default\_cash\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L537)

<a id="op-66c8a4b0ebbc5a"></a>
### POSInvoice.set missing values

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_set_missing_values`

**Inputs** self, for\_validate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_cached\_value · read “Print Format” via get\_value.

**Explicit results** mapping(“print\_format” → print\_format, “utm\_source” → profile.get(“utm\_source”), “utm\_campaign” → profile.get(“utm\_campaign”), “utm\_medium” → profile.get(“utm\_medium”), …).

**Local steps**

- Set profile from self.set\_pos\_fields(for\_validate).
- If not self.debit\_to.
  - Set self.debit\_to from get\_party\_account(“Customer”, self.customer, self.company).
  - Set self.party\_account\_currency from Platform.get\_cached\_value(“Account”, self.debit\_to, “account\_currency”).
- If (not self.due\_date and self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.due\_date → self.customer.
  - Set self.due\_date from get\_due\_date(self.posting\_date, “Customer”, self.customer, self.company, template\_name = self.payment\_terms\_template).
- Evaluate super(SalesInvoice, self).set\_missing\_values(for\_validate).
- Set print\_format from profile.get(“print\_format”) when profile, otherwise no value.
  - Value choice on profile — true gives profile.get(“print\_format”), false gives no value.
- If (not print\_format and not cint(Platform.db.get\_value(“Print Format”, “POS Invoice”, “disabled”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not print\_format → not cint(Platform.db.get\_value(“Print Format”, “POS Invoice”, “disabled”)).
  - Set print\_format from “POS Invoice”.
- If profile.
  - Return mapping(“print\_format” → print\_format, “utm\_source” → profile.get(“utm\_source”), “utm\_campaign” → profile.get(“utm\_campaign”), “utm\_medium” → profile.get(“utm\_medium”), …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pos fields](operations-080.md#op-a77c7d7c3e9331).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.debit\_to, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L535)

<a id="op-02745f7a8616c7"></a>
### POSInvoice.reset mode of payments

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_reset_mode_of_payments`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “POS Profile” via get\_cached\_doc.

**Local steps**

- If self.pos\_profile.
  - Set pos\_profile from Platform.get\_cached\_doc(“POS Profile”, self.pos\_profile).
  - Evaluate update\_multi\_mode\_option(self, pos\_profile).
  - Set self.paid\_amount from 0.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Profile”, self.pos\_profile).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0120.json#L4071) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L534)

<a id="op-3b1e647852abbc"></a>
### POSInvoice.create payment request

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_create_payment_request`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call submit on pay\_req.

**Explicit results** pay\_req.

**Explicit failure paths** validation helper — translated “Payment amount cannot be less than or equal to 0” · validation helper — translated “Please enter the phone number first”.

**Local steps**

- For each pay in self.payments.
  - If pay.type equals “Phone”.
    - <a id="op-3b1e647852abbc-guard-4"></a>If pay.amount ≤ 0.
      - Call the validation error handler Platform.throw(translated “Payment amount cannot be less than or equal to 0”).
    - If not self.contact\_mobile.
      - Call the validation error handler Platform.throw(translated “Please enter the phone number first”).
    - Set pay\_req from self.get\_existing\_payment\_request(pay).
    - If not pay\_req.
      - Set pay\_req from self.get\_new\_payment\_request(pay).
      - Evaluate pay\_req.submit().
    - Otherwise.
      - Evaluate pay\_req.request\_phone\_payment().
    - Return pay\_req.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison pay.amount ≤ 0, pay.amount = 0 selects the branch that calls the validation-error handler with translated “Payment amount cannot be less than or equal to 0”. With pay.amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-3b1e647852abbc-guard-4)

**Methods declared on this owner** [get existing payment request](operations-080.md#op-189df2ef0cfad7), [get new payment request](operations-080.md#op-6fdede0eac8709).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0120.json#L4219) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L526)

<a id="op-4cffacbed9de93"></a>
### POSInvoice.validate payments to collect

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_posinvoice_validate_payments_to_collect`

**Inputs** self, payments.

**Record and data access** read “POS Payment Method” via get\_all.

**Explicit failure paths** validation helper — translated “Payment amount must be greater than 0.” · validation helper — translated “Mode of Payment {0} is not allowed in POS Profile {1}.”.format(bold(payment.mode\_of\_payment), bold(self.pos\_profile)).

**Local steps**

- Set allowed\_modes from Platform.get\_all(“POS Payment Method”, filters = mapping(“parent” → self.pos\_profile), pluck = “mode\_of\_payment”).
- For each payment in payments.
  - Set payment from Platform.\_dict(payment).
  - If flt(payment.amount) ≤ 0.
    - Call the validation error handler Platform.throw(translated “Payment amount must be greater than 0.”).
  - If payment.mode\_of\_payment does not belong to allowed\_modes.
    - Call the validation error handler Platform.throw(translated “Mode of Payment {0} is not allowed in POS Profile {1}.”.format(bold(payment.mode\_of\_payment), bold(self.pos\_profile))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L265) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L903)

<a id="op-6fdede0eac8709"></a>
### POSInvoice.get new payment request

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_get_new_payment_request`

**Inputs** self, mop.

**Record and data access** read “Payment Gateway Account” via get\_value.

**Explicit results** make\_payment\_request(expanded names args).

**Local steps**

- Set payment\_gateway\_account from Platform.db.get\_value(“Payment Gateway Account”, mapping(“payment\_account” → mop.account), list(“name”)).
- Set args from mapping(“dt” → “POS Invoice”, “dn” → self.name, “recipient\_id” → self.contact\_mobile, “mode\_of\_payment” → mop.mode\_of\_payment, …).
- Return make\_payment\_request(expanded names args).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0120.json#L4554) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L530)

<a id="op-189df2ef0cfad7"></a>
### POSInvoice.get existing payment request

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_get_existing_payment_request`

**Inputs** self, pay.

**Record and data access** read “Payment Gateway Account” via get\_value · read “Payment Request” via get\_value · resolve a document from “Payment Request” via get\_doc.

**Explicit results** Platform.get\_doc(“Payment Request”, pr).

**Local steps**

- Set payment\_gateway\_account from Platform.db.get\_value(“Payment Gateway Account”, mapping(“payment\_account” → pay.account), list(“name”)).
- Set filters from mapping(“reference\_doctype” → “POS Invoice”, “reference\_name” → self.name, “payment\_gateway\_account” → payment\_gateway\_account, “email\_to” → self.contact\_mobile).
- Set pr from Platform.db.get\_value(“Payment Request”, filters = filters).
- If pr.
  - Return Platform.get\_doc(“Payment Request”, pr).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0120.json#L4866) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L529)

<a id="op-cb84dd7fd16df5"></a>
### POSInvoice.update payments

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_point_of_sale_invoice_update_payments`

**Inputs** self, payments.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call submit on payment.

**Explicit failure paths** validation helper — translated “Create Payment Entry for Consolidated POS Invoices.” · validation helper.

**Local steps**

- <a id="op-cb84dd7fd16df5-guard-2"></a>If self.status equals “Consolidated”.
  - Call the validation error handler Platform.throw(translated “Create Payment Entry for Consolidated POS Invoices.”).
- Evaluate self.validate\_payments\_to\_collect(payments).
- Set paid\_amount from flt(self.paid\_amount, self.precision(“paid\_amount”)).
- Set total from flt(((flt(self.rounded\_total) or flt(self.grand\_total)) − flt(self.write\_off\_amount)), self.precision(“grand\_total”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.rounded\_total) → flt(self.grand\_total).
- If paid\_amount ≥ total.
  - Call the validation error handler Platform.throw(title = translated “Invoice Paid”, msg = translated “This invoice has already been paid.”).
- Set idx from self.payments at negative 1.idx when self.payments, otherwise negative 1.
  - Value choice on self.payments — true gives self.payments at negative 1.idx, false gives negative 1.
- For each d in payments.
  - Update idx using + 1.
  - Set payment from create\_payments\_on\_invoice(self, idx, Platform.\_dict(d)).
  - Update paid\_amount using + flt(payment.amount).
  - Evaluate payment.submit().
- Set paid\_amount from flt(flt(paid\_amount), self.precision(“paid\_amount”)).
- Set base\_paid\_amount from flt(flt((paid\_amount × self.conversion\_rate)), self.precision(“base\_paid\_amount”)).
- Set outstanding\_amount from flt(flt((total − paid\_amount)), self.precision(“outstanding\_amount”)) when total &gt; paid\_amount, otherwise 0.
  - Value choice on total &gt; paid\_amount — true gives flt(flt((total − paid\_amount)), self.precision(“outstanding\_amount”)), false gives 0.
- Set change\_amount from flt(flt((paid\_amount − total)), self.precision(“change\_amount”)) when paid\_amount &gt; total, otherwise 0.
  - Value choice on paid\_amount &gt; total — true gives flt(flt((paid\_amount − total)), self.precision(“change\_amount”)), false gives 0.
- Set base\_change\_amount from flt((change\_amount × self.conversion\_rate), self.precision(“base\_change\_amount”)).
- Set pi from Platform.qb.DocType(“POS Invoice”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract).set(pi.change\_amount, change\_amount).set(pi.base\_change\_amount, base\_change\_amount).where(pi.name equals self.name).
- Evaluate query.run().
- Evaluate self.reload().
- Evaluate self.set\_status(update = true).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Consolidated”, self.status = “Consolidated” selects the branch that calls the validation-error handler with translated “Create Payment Entry for Consolidated POS Invoices.”. With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cb84dd7fd16df5-guard-2)

**Methods declared on this owner** [validate payments to collect](operations-080.md#op-4cffacbed9de93), [set status](operations-080.md#op-c4fa1c7ebc3e03).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L540)

<a id="op-f32966d5ae5829"></a>
### Get stock availability

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_get_stock_availability`

**Inputs** item\_code, warehouse.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Item” via get\_value · read “Product Bundle” via exists.

**Explicit results** tuple((bin\_qty − pos\_sales\_qty), is\_stock\_item, is\_negative\_stock\_allowed\_in\_pos(item\_code, bin\_data.reserved\_stock)) · tuple(get\_bundle\_availability(item\_code, warehouse), is\_stock\_item, false) · tuple(0, is\_stock\_item, false).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted for {0}”.format(warehouse).

**Local steps**

- Set ptype from “select” when Platform.only\_has\_select\_perm(“POS Profile”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“POS Profile”) — true gives “select”, false gives “read”.
- Evaluate Platform.has\_permission(“POS Profile”, ptype, throw = true).
- Bind dependencies get\_allowed\_docs\_for\_doctype, get\_user\_permissions.
- If warehouse\_permissions bound to get\_user\_permissions(Platform.session.user).get(“Warehouse”).
  - Set allowed\_warehouses from get\_allowed\_docs\_for\_doctype(warehouse\_permissions, “POS Invoice”).
  - If (allowed\_warehouses and warehouse does not belong to allowed\_warehouses).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_warehouses → warehouse does not belong to allowed\_warehouses.
    - Call the validation error handler Platform.throw(translated “Not permitted for {0}”.format(warehouse), Platform.PermissionError).
- If Platform.db.get\_value(“Item”, item\_code, “is\_stock\_item”).
  - Set is\_stock\_item from true.
  - Set bin\_data from get\_bin\_data(item\_code, warehouse).
  - Set bin\_qty from (flt(bin\_data.actual\_qty) − flt(bin\_data.reserved\_stock)).
  - Set pos\_sales\_qty from get\_pos\_reserved\_qty(item\_code, warehouse).
  - Return tuple((bin\_qty − pos\_sales\_qty), is\_stock\_item, is\_negative\_stock\_allowed\_in\_pos(item\_code, bin\_data.reserved\_stock)).
- Otherwise.
  - Set is\_stock\_item from true.
  - If Platform.db.exists(“Product Bundle”, mapping(“name” → item\_code, “disabled” → 0)).
    - Return tuple(get\_bundle\_availability(item\_code, warehouse), is\_stock\_item, false).
  - Otherwise.
    - Set is\_stock\_item from false.
    - Return tuple(0, is\_stock\_item, false).

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Profile”, ptype, throw = true), get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L115) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L517)

<a id="op-16f4000681f046"></a>
### Get bundle availability

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_get_bundle_availability`

**Inputs** bundle\_item\_code, warehouse.

**Record and data access** resolve a document from “Product Bundle” via get\_doc · read “Item” via get\_value.

**Explicit results** (bundle\_bin\_qty − pos\_sales\_qty).

**Local steps**

- Set product\_bundle from Platform.get\_doc(“Product Bundle”, bundle\_item\_code).
- Set bundle\_bin\_qty from 1000000.
- For each item in product\_bundle.items.
  - Set item\_bin\_qty from get\_bin\_qty(item.item\_code, warehouse).
  - Set max\_available\_bundles from (item\_bin\_qty ÷ item.qty).
  - If (bundle\_bin\_qty &gt; max\_available\_bundles and Platform.get\_value(“Item”, item.item\_code, “is\_stock\_item”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in bundle\_bin\_qty &gt; max\_available\_bundles → Platform.get\_value(“Item”, item.item\_code, “is\_stock\_item”).
    - Set bundle\_bin\_qty from max\_available\_bundles.
- Set pos\_sales\_qty from get\_pos\_reserved\_qty(bundle\_item\_code, warehouse).
- Return (bundle\_bin\_qty − pos\_sales\_qty).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L513)

<a id="op-4cc866cbce0f23"></a>
### Get bin qty

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_get_bin_quantity`

**Inputs** item\_code, warehouse.

**Explicit results** (flt(bin\_data.actual\_qty) − flt(bin\_data.reserved\_stock)).

**Local steps**

- Set bin\_data from get\_bin\_data(item\_code, warehouse).
- Return (flt(bin\_data.actual\_qty) − flt(bin\_data.reserved\_stock)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L512)

<a id="op-801d1344cee1b5"></a>
### Get bin data

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_get_bin_data`

**Inputs** item\_code, warehouse.

**Record and data access** read “Bin” via get\_value.

**Explicit results** (Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), list(“actual\_qty”, “reserved\_stock”), as\_dict = true) or Platform.\_dict()).

**Local steps**

- Return (Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), list(“actual\_qty”, “reserved\_stock”), as\_dict = true) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Bin”, mapping(“item\_code” → item\_code, “warehouse” → warehouse), list(“actual\_qty”, “reserved\_stock”), as\_dict = true) → Platform.\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L255) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L893)

<a id="op-34f30256bb062b"></a>
### Is negative stock allowed in pos

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_is_negative_stock_allowed_in_pos`

**Inputs** item\_code, reserved\_stock.

**Record and data access** resolve a document from “Stock Settings” via get\_cached\_doc.

**Explicit results** true · (flt(reserved\_stock) ≤ 0 and is\_negative\_stock\_allowed(item\_code = item\_code)).

**Local steps**

- If Platform.get\_cached\_doc(“Stock Settings”).allow\_negative\_stock.
  - Return true.
- Return (flt(reserved\_stock) ≤ 0 and is\_negative\_stock\_allowed(item\_code = item\_code)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(reserved\_stock) ≤ 0 → is\_negative\_stock\_allowed(item\_code = item\_code).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Stock Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L259) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L897)

<a id="op-ac847b8656e553"></a>
### Get pos reserved qty

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_get_point_of_sale_reserved_quantity`

**Inputs** item\_code, warehouse.

**Explicit results** get\_pos\_reserved\_qty\_map(set(item\_code), set(warehouse)).get(tuple(item\_code, warehouse), 0.0).

**Local steps**

- Return get\_pos\_reserved\_qty\_map(set(item\_code), set(warehouse)).get(tuple(item\_code, warehouse), 0.0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L515)

<a id="op-5842f62fe0adcb"></a>
### Get pos reserved qty map

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_get_pos_reserved_qty_map`

**Inputs** item\_codes, warehouses.

**Explicit results** reserved\_qty.

**Local steps**

- Set reserved\_qty from defaultdict(float).
- For each tuple(child\_table, qty\_column) in tuple(tuple(“POS Invoice Item”, “stock\_qty”), tuple(“Packed Item”, “qty”)).
  - For each row in get\_pos\_reserved\_qty\_from\_table(child\_table, qty\_column, item\_codes, warehouses).
    - Update reserved\_qty at tuple(row.item\_code, row.warehouse) using + flt(row.qty).
- Return reserved\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L256) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L894)

<a id="op-4c0a0f0f57ed9f"></a>
### Get pos reserved qty from table

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_get_point_of_sale_reserved_quantity_from_table`

**Inputs** child\_table, qty\_column, item\_codes, warehouses.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Local steps**

- Set p\_inv from Platform.qb.DocType(“POS Invoice”).
- Set p\_item from Platform.qb.DocType(child\_table).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L516)

<a id="op-ffbf88bbb0393c"></a>
### Get active bundle items

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_get_active_bundle_items`

**Inputs** item\_codes.

**Explicit results** bundle\_items.

**Local steps**

- Set bundle from Platform.qb.DocType(“Product Bundle”).
- Set bundle\_item from Platform.qb.DocType(“Product Bundle Item”).
- Set rows from nested operand in the contract(nested operand in the contract).select(bundle.new\_item\_code, bundle\_item.item\_code, bundle\_item.qty).where((nested operand in the contract.new\_item\_code.isin(list(item\_codes) ….
- Set bundle\_items from defaultdict(list).
- For each row in rows.
  - Evaluate bundle\_items at row.new\_item\_code.append(row).
- Return bundle\_items.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L253) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L891)

<a id="op-7d4321b0e4bc30"></a>
### Get required stock qty

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_get_required_stock_qty`

**Inputs** rows, bundle\_items.

**Explicit results** required\_qty.

**Local steps**

- Set required\_qty from defaultdict(float).
- For each row in rows.
  - For each component in (bundle\_items.get(row.item\_code) or list(Platform.\_dict(item\_code = row.item\_code, qty = 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bundle\_items.get(row.item\_code) → list(Platform.\_dict(item\_code = row.item\_code, qty = 1)).
    - Update required\_qty at tuple(component.item\_code, row.warehouse) using + (flt(component.qty) × flt(row.stock\_qty)).
- Return required\_qty.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L257) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L895)

<a id="op-116bc5f2454c4f"></a>
### Get available stock qty

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_get_available_stock_qty`

**Inputs** required\_qty.

**Explicit results** tuple(available\_qty, reserved\_stock\_keys).

**Local steps**

- Set keys from list of Platform.\_dict(item\_code = item\_code, warehouse = warehouse) for tuple(item\_code, warehouse) drawn from required\_qty.
  - Draw tuple(item\_code, warehouse) from required\_qty.
- Set bin\_qty from get\_bin\_qty\_map(keys).
- Set reserved\_qty from get\_pos\_reserved\_qty\_map(set of d.item\_code for d drawn from keys, set of d.warehouse for d drawn from keys).
  - Draw d from keys.
  - Draw d from keys.
- Set tuple(available\_qty, reserved\_stock\_keys) from tuple(mapping(), set()).
- For each key in required\_qty.
  - Set bin\_data from (bin\_qty.get(key) or Platform.\_dict()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in bin\_qty.get(key) → Platform.\_dict().
  - Set available\_qty at key from ((flt(bin\_data.actual\_qty) − flt(bin\_data.reserved\_stock)) − reserved\_qty at key).
  - If flt(bin\_data.reserved\_stock) &gt; 0.
    - Evaluate reserved\_stock\_keys.add(key).
- Return tuple(available\_qty, reserved\_stock\_keys).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L254) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L892)

<a id="op-b3f4d1d74c5d1d"></a>
### Get stock item details

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_get_stock_item_details`

**Inputs** item\_codes.

**Record and data access** read “Item” via get\_all.

**Explicit results** mapping of item.name → item for item drawn from items.

**Local steps**

- Set items from Platform.get\_all(“Item”, filters = mapping(“name” → list(“in”, list(item\_codes))), fields = list(“name”, “is\_stock\_item”, “allow\_negative\_stock”)).
- Return mapping of item.name → item for item drawn from items.
  - Draw item from items.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L258) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L896)

<a id="op-fe0c9c10a74acb"></a>
### Is stock check needed

`operation_enterprise_binding_enterprise_accounts_doctype_pos_invoice_pos_invoice_is_stock_check_needed`

**Inputs** item, has\_reserved\_stock.

**Explicit results** bool((item and item.is\_stock\_item and (has\_reserved\_stock or not item.allow\_negative\_stock))).

**Local steps**

- Return bool((item and item.is\_stock\_item and (has\_reserved\_stock or not item.allow\_negative\_stock))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item.is\_stock\_item → (has\_reserved\_stock or not item.allow\_negative\_stock).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_reserved\_stock → not item.allow\_negative\_stock.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L260) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L898)

<a id="op-54c36fc8c14ccb"></a>
### Make sales return

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_make_sales_return`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** make\_return\_doc(“POS Invoice”, source\_name, target\_doc).

**Local steps**

- Bind dependencies make\_return\_doc.
- Return make\_return\_doc(“POS Invoice”, source\_name, target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L520)

<a id="op-5caafff41bb1e0"></a>
### Make merge log

`operation_enterprise_accounts_record_definitions_point_of_sale_invoice_business_behavior_make_merge_log`

**Inputs** invoices.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “POS Invoice” via get\_values.

**State and service calls** request new\_doc for “POS Invoice Merge Log”.

**Explicit results** merge\_log.as\_dict().

**Explicit failure paths** validation helper — translated “At least one invoice has to be selected.”.

**Local steps**

- Bind dependencies json.
- If isinstance(invoices, str).
  - Set invoices from json.loads(invoices).
- <a id="op-5caafff41bb1e0-guard-7"></a>If len(invoices) equals 0.
  - Call the validation error handler Platform.throw(translated “At least one invoice has to be selected.”).
- Set merge\_log from Platform.new\_doc(“POS Invoice Merge Log”).
- Set merge\_log.posting\_date from getdate(nowdate()).
- For each inv in invoices.
  - Set inv at “name” from cstr(inv.get(“name”)).
  - If (not inv at “name” or not Platform.has\_permission(“POS Invoice”, “read”, doc = inv at “name”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not inv at “name” → not Platform.has\_permission(“POS Invoice”, “read”, doc = inv at “name”).
    - Evaluate \_refuse().
  - Set inv\_data from Platform.db.get\_values(“POS Invoice”, inv.get(“name”), list(“customer”, “posting\_date”, “grand\_total”), as\_dict = 1) at 0.
  - Set merge\_log.customer from inv\_data.customer.
  - Evaluate merge\_log.append(“pos\_invoices”, mapping(“pos\_invoice” → inv.get(“name”), “customer” → inv\_data.customer, “posting\_date” → inv\_data.posting\_date, “grand\_total” → inv\_data.grand\_total)).
- If merge\_log.get(“pos\_invoices”).
  - Return merge\_log.as\_dict().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(invoices) equals 0, length of invoices = 0 selects the branch that calls the validation-error handler with translated “At least one invoice has to be selected.”. With length of invoices = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-5caafff41bb1e0-guard-7)

**Values supplied outside this operation** clock or generated value from nowdate() · effective access from Platform.has\_permission(“POS Invoice”, “read”, doc = inv at “name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L519)
