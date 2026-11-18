# Shared transaction rules · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-99921e7b03a58e"></a>
### Accounts Controller.validate company

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_company`

**Inputs** self, dimension\_list, child = no value.

**Record and data access** read dimension via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0}: {1} does not belong to the Company: {2}”.format(dimension, Platform.bold(dimension\_value), self.company).

**Local steps**

- For each dimension in dimension\_list.
  - If not child.
    - Set dimension\_value from self.get(Platform.scrub(dimension)).
  - Otherwise.
    - Set dimension\_value from child.get(Platform.scrub(dimension)).
  - If dimension\_value.
    - Set company from Platform.get\_cached\_value(dimension, dimension\_value, “company”).
    - If (company and company differs from self.company).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → company differs from self.company.
      - Call the validation error handler Platform.throw(translated “{0}: {1} does not belong to the Company: {2}”.format(dimension, Platform.bold(dimension\_value), self.company)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(dimension, dimension\_value, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L3840) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L368)

<a id="op-b3710f59a5bf10"></a>
### Accounts Controller.validate party address and contact

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party_address_and_contact`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set tuple(party\_type, party) from self.get\_party().
- If not (party\_type and party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
  - Return no value.
- If party\_type equals “Customer”.
  - Set tuple(billing\_address, shipping\_address) from tuple(self.get(“customer\_address”), self.get(“shipping\_address\_name”)).
  - Evaluate self.validate\_party\_address(party, party\_type, billing\_address, shipping\_address).
- Otherwise.
  - If party\_type equals “Supplier”.
    - Set billing\_address from self.get(“supplier\_address”).
    - Evaluate self.validate\_party\_address(party, party\_type, billing\_address).
- Evaluate self.validate\_party\_contact(party, party\_type).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party](operations-005.md#op-1120b9a6c920b3), [validate party address](operations-002.md#op-4b926c741b0b4f), [validate party contact](operations-002.md#op-d44ad8968dd210).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L973) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L213)

<a id="op-4b926c741b0b4f"></a>
### Accounts Controller.validate party address

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party_address`

**Inputs** self, party, party\_type, billing\_address, shipping\_address = no value.

**Record and data access** read “Dynamic Link” via get\_all.

**Explicit failure paths** validation helper — translated “Billing Address does not belong to the {0}”.format(party) · validation helper — translated “Shipping Address does not belong to the {0}”.format(party).

**Local steps**

- If (billing\_address or shipping\_address).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in billing\_address → shipping\_address.
  - Set party\_address from Platform.get\_all(“Dynamic Link”, mapping(“link\_doctype” → party\_type, “link\_name” → party, “parenttype” → “Address”), pluck = “parent”).
  - If (billing\_address and billing\_address does not belong to party\_address).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in billing\_address → billing\_address does not belong to party\_address.
    - Call the validation error handler Platform.throw(translated “Billing Address does not belong to the {0}”.format(party)).
  - Otherwise.
    - If (shipping\_address and shipping\_address does not belong to party\_address).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in shipping\_address → shipping\_address does not belong to party\_address.
      - Call the validation error handler Platform.throw(translated “Shipping Address does not belong to the {0}”.format(party)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L972) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L212)

<a id="op-d44ad8968dd210"></a>
### Accounts Controller.validate party contact

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party_contact`

**Inputs** self, party, party\_type.

**Record and data access** read “Dynamic Link” via get\_all.

**Explicit failure paths** validation helper — translated “Contact Person does not belong to the {0}”.format(party).

**Local steps**

- If self.get(“contact\_person”).
  - Set contact from Platform.get\_all(“Dynamic Link”, mapping(“link\_doctype” → party\_type, “link\_name” → party, “parenttype” → “Contact”), pluck = “parent”).
  - If (self.contact\_person and self.contact\_person does not belong to contact).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.contact\_person → self.contact\_person does not belong to contact.
    - Call the validation error handler Platform.throw(translated “Contact Person does not belong to the {0}”.format(party)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L974) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L214)

<a id="op-3ac921792c56b0"></a>
### Accounts Controller.validate return against account

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_return_against_account`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**Explicit failure paths** validation helper — translated “Please set {0} to {1}, the same account that was used in the original invoice {2}.”.format(Platform.bold(\_(self.meta.get\_label(cr\_dr\_account\_field), context = self.doctype)), Platform.bold(orig ….

**Local steps**

- If (self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) and self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”) → self.is\_return → self.return\_against.
  - Set cr\_dr\_account\_field from “debit\_to” when self.doctype equals “Sales Invoice”, otherwise “credit\_to”.
    - Value choice on self.doctype equals “Sales Invoice” — true gives “debit\_to”, false gives “credit\_to”.
  - Set original\_account from Platform.get\_value(self.doctype, self.return\_against, cr\_dr\_account\_field).
  - If original\_account differs from self.get(cr\_dr\_account\_field).
    - Call the validation error handler Platform.throw(translated “Please set {0} to {1}, the same account that was used in the original invoice {2}.”.format(Platform.bold(\_(nested operand in the contract.meta.get\_label(cr\_dr\_account\_field), con ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L374)

<a id="op-91e2ef05500574"></a>
### Accounts Controller.validate deferred income expense account

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_deferred_income_expense_account`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Please update deferred revenue/expense account in item row or default account in company master”.format(item.idx).

**Local steps**

- Set field\_map from mapping(“Sales Invoice” → “deferred\_revenue\_account”, “Purchase Invoice” → “deferred\_expense\_account”).
- For each item in self.get(“items”).
  - If (item.get(“enable\_deferred\_revenue”) or item.get(“enable\_deferred\_expense”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“enable\_deferred\_revenue”) → item.get(“enable\_deferred\_expense”).
    - If not item.get(field\_map.get(self.doctype)).
      - Set default\_deferred\_account from Platform.get\_cached\_value(“Company”, self.company, (“default\_” + field\_map.get(self.doctype))).
      - If not default\_deferred\_account.
        - Call the validation error handler Platform.throw(translated “Row #{0}: Please update deferred revenue/expense account in item row or default account in company master”.format(item.idx)).
      - Otherwise.
        - Evaluate item.set(field\_map.get(self.doctype), default\_deferred\_account).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, (“default\_” + field\_map.get(self.doctype))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L198)

<a id="op-77bb3f2648a06f"></a>
### Accounts Controller.validate auto repeat subscription dates

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_auto_repeat_subscription_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “To Date cannot be before From Date”.

**Local steps**

- If (self.get(“from\_date”) and self.get(“to\_date”) and getdate(self.from\_date) &gt; getdate(self.to\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“from\_date”) → self.get(“to\_date”) → getdate(self.from\_date) &gt; getdate(self.to\_date).
  - Call the validation error handler Platform.throw(translated “To Date cannot be before From Date”, title = translated “Invalid Auto Repeat Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L4563) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L367)

<a id="op-b6d2d3126785aa"></a>
### Accounts Controller.clear stale deferred fields

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_clear_stale_deferred_fields`

**Inputs** self.

**Local steps**

- Set field\_map from mapping(“Sales Invoice” → “deferred\_revenue\_account”, “Purchase Invoice” → “deferred\_expense\_account”).
- Set account\_field from field\_map.get(self.doctype).
- For each item in self.get(“items”).
  - If (item.get(“enable\_deferred\_revenue”) or item.get(“enable\_deferred\_expense”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“enable\_deferred\_revenue”) → item.get(“enable\_deferred\_expense”).
    - Continue with the next iteration or loop test.
  - Set item.service\_start\_date from no value.
  - Set item.service\_end\_date from no value.
  - Set item.service\_stop\_date from no value.
  - If account\_field.
    - Evaluate item.set(account\_field, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L146)

<a id="op-9f4ad62547daa9"></a>
### Accounts Controller.validate deferred start and end date

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_deferred_start_and_end_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Service Start and End Date is required for deferred accounting”.format(d.idx) · validation helper — translated “Row #{0}: Service Start Date cannot be greater than Service End Date”.format(d.idx) · validation helper — translated “Row #{0}: Service End Date cannot be before Invoice Posting Date”.format(d.idx).

**Local steps**

- For each d in self.items.
  - If (d.get(“enable\_deferred\_revenue”) or d.get(“enable\_deferred\_expense”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“enable\_deferred\_revenue”) → d.get(“enable\_deferred\_expense”).
    - If not (d.service\_start\_date and d.service\_end\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.service\_start\_date → d.service\_end\_date.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Service Start and End Date is required for deferred accounting”.format(d.idx)).
    - Otherwise.
      - If getdate(d.service\_start\_date) &gt; getdate(d.service\_end\_date).
        - Call the validation error handler Platform.throw(translated “Row #{0}: Service Start Date cannot be greater than Service End Date”.format(d.idx)).
      - Otherwise.
        - If getdate(self.posting\_date) &gt; getdate(d.service\_end\_date).
          - Call the validation error handler Platform.throw(translated “Row #{0}: Service End Date cannot be before Invoice Posting Date”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L959) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L199)

<a id="op-bc164e12cbe11c"></a>
### Accounts Controller.validate invoice documents schedule

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_invoice_documents_schedule`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.is\_return or (self.doctype equals “Purchase Invoice” and self.is\_paid) or (self.doctype equals “Sales Invoice” and self.is\_pos) or self.get(“is\_opening”) equals “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → (self.doctype equals “Purchase Invoice” and self.is\_paid) → (self.doctype equals “Sales Invoice” and self.is\_pos) → self.get(“is\_opening”) equals “Yes”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.is\_paid.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_pos.
  - Set self.payment\_terms\_template from empty text.
  - Set self.payment\_schedule from list().
- If self.is\_return.
  - Return no value.
- Evaluate self.validate\_payment\_schedule\_dates().
- Evaluate self.set\_due\_date().
- Evaluate self.set\_payment\_schedule().
- If not self.get(“ignore\_default\_payment\_terms\_template”).
  - Evaluate self.validate\_payment\_schedule\_amount().
  - Evaluate self.validate\_due\_date().
- Evaluate self.validate\_advance\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate payment schedule dates](operations-006.md#op-b1fa17a823f5cb), [set due date](operations-006.md#op-11a28093a93974), [set payment schedule](operations-005.md#op-f477c9b4096cad), [validate payment schedule amount](operations-006.md#op-c2ce7713c31da1), [validate due date](operations-003.md#op-05814f565ba4a6), [validate advance entries](operations-004.md#op-92d9f34573a809).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L965) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L205)

<a id="op-d5b0c6cedcec01"></a>
### Accounts Controller.validate non invoice documents schedule

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_non_invoice_documents_schedule`

**Inputs** self.

**Local steps**

- Evaluate self.set\_payment\_schedule().
- Evaluate self.validate\_payment\_schedule\_dates().
- Evaluate self.validate\_payment\_schedule\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set payment schedule](operations-005.md#op-f477c9b4096cad), [validate payment schedule dates](operations-006.md#op-b1fa17a823f5cb), [validate payment schedule amount](operations-006.md#op-c2ce7713c31da1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L968) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L208)

<a id="op-92313444a6e107"></a>
### Accounts Controller.validate all documents schedule

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_all_documents_schedule`

**Inputs** self.

**Local steps**

- If self.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Evaluate self.validate\_invoice\_documents\_schedule().
- Otherwise.
  - If self.doctype belongs to tuple(“Quotation”, “Purchase Order”, “Sales Order”).
    - Evaluate self.validate\_non\_invoice\_documents\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate invoice documents schedule](operations-002.md#op-bc164e12cbe11c), [validate non invoice documents schedule](operations-002.md#op-d5b0c6cedcec01).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L195)

<a id="op-fa93b5e0f51d57"></a>
### Accounts Controller.shift service dates

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_shift_service_dates`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Explicit results** no value.

**Local steps**

- If not (self.from\_date and self.to\_date and reference\_doc.from\_date and reference\_doc.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.from\_date → self.to\_date → reference\_doc.from\_date → reference\_doc.to\_date.
  - Return no value.
- Set from\_date from getdate(self.from\_date).
- Set reference\_from\_date from getdate(reference\_doc.from\_date).
- Set months from ((((from\_date.year − reference\_from\_date.year) × 12) + from\_date.month) − reference\_from\_date.month).
- Set days from date\_diff(from\_date, reference\_from\_date).
- Set shift\_by\_months from auto\_repeat\_doc.frequency belongs to month\_map.
- Set reference\_to\_date from getdate(reference\_doc.to\_date).
- Set to\_date from getdate(self.to\_date).
- Bind local operation shift for subsequent calls.
- For each tuple(item, reference\_item) in zip(self.items, reference\_doc.items, strict = true).
  - If reference\_item.service\_start\_date.
    - Set item.service\_start\_date from shift(reference\_item.service\_start\_date).
  - If reference\_item.service\_end\_date.
    - Set item.service\_end\_date from shift(reference\_item.service\_end\_date).
  - If (item.service\_start\_date and item.service\_end\_date and getdate(item.service\_end\_date) &lt; getdate(item.service\_start\_date)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.service\_start\_date → item.service\_end\_date → getdate(item.service\_end\_date) &lt; getdate(item.service\_start\_date).
    - Set item.service\_end\_date from add\_days(to\_date, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L190)

<a id="op-81107f6d7ad347"></a>
### Accounts Controller.shift service dates.shift

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_shift_service_dates_shift`

**Inputs** date.

**Explicit results** to\_date · add\_days(date, days) · min(shifted\_date, to\_date) · shifted\_date.

**Local steps**

- If getdate(date) equals reference\_to\_date.
  - Return to\_date.
- If not shift\_by\_months.
  - Return add\_days(date, days).
- Set shifted\_date from getdate(add\_months(date, months)).
- If getdate(date) equals get\_last\_day(date).
  - Set shifted\_date from get\_last\_day(shifted\_date).
- If getdate(date) &lt; reference\_to\_date.
  - Return min(shifted\_date, to\_date).
- Return shifted\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L191)

<a id="op-0609014e5e1ccf"></a>
### Accounts Controller.before print

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_before_print`

**Inputs** self, settings = no value.

**Local steps**

- If self.docstatus.is\_draft().
  - Evaluate self.set\_missing\_terms\_for\_display().
- If self.doctype belongs to list(“Purchase Order”, “Sales Order”, “Sales Invoice”, “Purchase Invoice”, …).
  - If self.get(“group\_same\_items”).
    - Evaluate self.group\_similar\_items().
  - Set df from self.meta.get\_field(“discount\_amount”).
  - If (self.get(“discount\_amount”) and hasattr(self, “taxes”) and not len(self.taxes)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“discount\_amount”) → hasattr(self, “taxes”) → not len(self.taxes).
    - Evaluate df.set(“print\_hide”, 0).
    - Set self.discount\_amount from negative self.discount\_amount.
  - Otherwise.
    - Evaluate df.set(“print\_hide”, 1).
- Evaluate set\_print\_templates\_for\_item\_table(self, settings).
- Evaluate set\_print\_templates\_for\_taxes(self, settings).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing terms for display](operations-002.md#op-e491d0f18481e2), [group similar items](operations-005.md#op-07f7d4bc6202e7).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L300)

<a id="op-9da8abbc6fab47"></a>
### Accounts Controller.set missing terms

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_missing_terms`

**Inputs** self, raise\_exception = true.

**State and service calls** msgprint with message.

**Explicit results** no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If (not self.get(“tc\_name”) or self.get(“terms”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“tc\_name”) → self.get(“terms”).
  - Return no value.
- Bind dependencies TemplateError.
- Bind dependencies get\_terms\_and\_conditions.
- Attempt the following.
  - Set self.terms from get\_terms\_and\_conditions(self.tc\_name, self.as\_dict()).
- On failure (tuple(TemplateError, TypeError)) bound to e.
  - Set message from translated “Terms and Conditions {0} could not be rendered: {1}”.format(Platform.bold(self.tc\_name), e).
  - If raise\_exception.
    - Call the validation error handler Platform.throw(message).
  - Evaluate Platform.msgprint(message, indicator = “orange”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L650) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L354)

<a id="op-e491d0f18481e2"></a>
### Accounts Controller.set missing terms for display

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_missing_terms_for_display`

**Inputs** self.

**State and service calls** msgprint with translated “Terms and Conditions {0} could not be rendered due to missing permissions.”.format(bold(self.tc\_name)).

**Local steps**

- Set message\_count from len(Platform.message\_log).
- Attempt the following.
  - Evaluate self.set\_missing\_terms(raise\_exception = false).
- On failure (Platform.PermissionError).
  - Remove Platform.message\_log at slice message\_count to no value.
  - Evaluate Platform.msgprint(translated “Terms and Conditions {0} could not be rendered due to missing permissions.”.format(bold(self.tc\_name)), alert = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing terms](operations-002.md#op-9da8abbc6fab47).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L944) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L184)

<a id="op-493ec3a0d7149a"></a>
### Accounts Controller.calculate paid amount

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_calculate_paid_amount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Note: Payment Entry will not be created since 'Cash or Bank Account' was not specified”.

**Local steps**

- If (hasattr(self, “is\_pos”) or hasattr(self, “is\_paid”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in hasattr(self, “is\_pos”) → hasattr(self, “is\_paid”).
  - Set is\_paid from (self.get(“is\_pos”) or self.get(“is\_paid”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_pos”) → self.get(“is\_paid”).
  - If is\_paid.
    - If not self.cash\_bank\_account.
      - Call the validation error handler Platform.throw(translated “Note: Payment Entry will not be created since 'Cash or Bank Account' was not specified”).
    - If (cint(self.is\_return) and self.grand\_total &gt; self.paid\_amount).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.grand\_total &gt; self.paid\_amount.
      - Set self.paid\_amount from flt(flt(self.grand\_total), self.precision(“paid\_amount”)).
    - Otherwise.
      - If (not flt(self.paid\_amount) and flt(self.outstanding\_amount) &gt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(self.paid\_amount) → flt(self.outstanding\_amount) &gt; 0.
        - Set self.paid\_amount from flt(flt(self.outstanding\_amount), self.precision(“paid\_amount”)).
    - Set self.base\_paid\_amount from flt((self.paid\_amount × self.conversion\_rate), self.precision(“base\_paid\_amount”)).
  - Otherwise.
    - Set self.paid\_amount from 0.
    - Set self.base\_paid\_amount from 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L5404) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L301)

<a id="op-491e4bbcd918e7"></a>
### Accounts Controller.set missing values

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_missing_values`

**Inputs** self, for\_validate = false.

**Local steps**

- If Platform.in\_test.
  - For each fieldname in list(“posting\_date”, “transaction\_date”).
    - If (self.meta.get\_field(fieldname) and not self.get(fieldname)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(fieldname) → not self.get(fieldname).
      - Evaluate self.set(fieldname, today()).
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L5992) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L651) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L355)

<a id="op-52a893faf0bdd9"></a>
### Accounts Controller.calculate taxes and totals

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_calculate_taxes_and_totals`

**Inputs** self.

**Local steps**

- Bind dependencies calculate\_taxes\_and\_totals.
- Evaluate calculate\_taxes\_and\_totals(self).
- If self.doctype belongs to tuple(“Sales Order”, “Delivery Note”, “Sales Invoice”, “POS Invoice”).
  - Evaluate self.calculate\_commission().
  - Evaluate self.calculate\_contribution().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L6182) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L302)

<a id="op-9ffa922ffe02b4"></a>
### Accounts Controller.validate date with fiscal year

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_date_with_fiscal_year`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set date\_field from no value.
- If self.meta.get\_field(“posting\_date”).
  - Set date\_field from “posting\_date”.
- Otherwise.
  - If self.meta.get\_field(“transaction\_date”).
    - Set date\_field from “transaction\_date”.
- If (not date\_field or not self.get(date\_field)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not date\_field → not self.get(date\_field).
  - Return no value.
- If self.meta.get\_field(“fiscal\_year”).
  - Evaluate validate\_fiscal\_year(self.get(date\_field), self.fiscal\_year, self.company, self.meta.get\_label(date\_field), …).
- Otherwise.
  - Evaluate get\_fiscal\_year(self.get(date\_field), company = self.company, label = self.meta.get\_label(date\_field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L6341) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L370)

<a id="op-ca5a0592338552"></a>
### Accounts Controller.validate party accounts

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_party_accounts`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: {1} {2} cannot be same as {3} (Party Account) {4}”.format(item.idx, Platform.bold(Platform.unscrub(item\_field)), item.get(item\_field), Platform.bold(Platform.unscrub(party\_account\_field)), …).

**Local steps**

- If self.doctype does not belong to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Return no value.
- If self.doctype equals “Sales Invoice”.
  - Set party\_account\_field from “debit\_to”.
  - Set item\_field from “income\_account”.
- Otherwise.
  - Set party\_account\_field from “credit\_to”.
  - Set item\_field from “expense\_account”.
- For each item in self.get(“items”).
  - If item.get(item\_field) equals self.get(party\_account\_field).
    - Call the validation error handler Platform.throw(translated “Row {0}: {1} {2} cannot be same as {3} (Party Account) {4}”.format(item.idx, Platform.bold(Platform.unscrub(item\_field)), item.get(item\_field), Platform.bold(Platform.unscrub(par ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L971) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L211)

<a id="op-9ae221375c47f6"></a>
### Accounts Controller.validate inter company reference

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_inter_company_reference`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — msg · validation helper — translated msg.

**Local steps**

- If self.get(“is\_return”).
  - Return no value.
- If self.doctype does not belong to tuple(“Purchase Invoice”, “Purchase Receipt”).
  - Return no value.
- If self.is\_internal\_transfer().
  - If (not (self.get(“inter\_company\_reference”) or self.get(“inter\_company\_invoice\_reference”) or self.get(“inter\_company\_order\_reference”)) and not self.get(“is\_return”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (self.get(“inter\_company\_reference”) or self.get(“inter\_company\_invoice\_reference”) or self.get(“inter\_company\_order\_reference”)) → not self.get(“is\_return”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“inter\_company\_reference”) → self.get(“inter\_company\_invoice\_reference”) → self.get(“inter\_company\_order\_reference”).
    - Set msg from translated “Internal Sale or Delivery Reference missing.”.
    - Update msg using + translated “Please create purchase from internal sale or delivery document itself”.
    - Call the validation error handler Platform.throw(msg, title = translated “Internal Sales Reference Missing”).
  - Set label from “Delivery Note Item” when self.doctype equals “Purchase Receipt”, otherwise “Sales Invoice Item”.
    - Value choice on self.doctype equals “Purchase Receipt” — true gives “Delivery Note Item”, false gives “Sales Invoice Item”.
  - Set field from Platform.scrub(label).
  - For each row in self.get(“items”).
    - If (not row.get(field) and not row.get(“delivery\_note\_packed\_item”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.get(field) → not row.get(“delivery\_note\_packed\_item”).
      - Set msg from formatted text At Row {row.idx}: The field {bold(label)} is mandatory for internal transfer.
      - Call the validation error handler Platform.throw(translated msg, title = translated “Internal Transfer Reference Missing”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is internal transfer](operations-006.md#op-13fa6c1b2d5ba8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L962) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L202)

<a id="op-2256c35ca7ff7b"></a>
### Accounts Controller.validate inter company currency

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_inter_company_currency`

**Inputs** self.

**Record and data access** read counterpart\_doctype via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Currency must be {0} to match {1} {2}”.format(bold(currency), counterpart\_doctype, bold(counterpart)).

**Local steps**

- If self.doctype does not belong to COUNTERPART\_REFERENCE.
  - Return no value.
- Set tuple(reference\_field, counterpart\_doctype) from COUNTERPART\_REFERENCE at self.doctype.
- Set counterpart from self.get(reference\_field).
- If not counterpart.
  - Return no value.
- Set currency from Platform.db.get\_value(counterpart\_doctype, counterpart, “currency”).
- If (currency and self.currency differs from currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in currency → self.currency differs from currency.
  - Call the validation error handler Platform.throw(translated “Currency must be {0} to match {1} {2}”.format(bold(currency), counterpart\_doctype, bold(counterpart))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L961) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L201)
