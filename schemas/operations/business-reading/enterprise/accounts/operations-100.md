# Accounting and settlement · operations 100

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-bf85303a77c6c0"></a>
### Sales Invoice.set pos fields

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_set_point_of_sale_fields`

**Inputs** self, for\_validate = false.

**Record and data access** read “Company” via get\_cached\_value · resolve a document from “POS Profile” via get\_doc · read “Customer” via get\_value · read “Customer Group” via get\_value · read “Terms and Conditions” via get\_value.

**Explicit results** no value · pos.

**Local steps**

- If cint(self.is\_pos) differs from 1.
  - Return no value.
- If not self.account\_for\_change\_amount.
  - Set self.account\_for\_change\_amount from Platform.get\_cached\_value(“Company”, self.company, “default\_cash\_account”).
- Bind dependencies ItemDetailsCtx, get\_pos\_profile, get\_pos\_profile\_item\_details\_.
- If (not self.pos\_profile and not self.flags.ignore\_pos\_profile).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.pos\_profile → not self.flags.ignore\_pos\_profile.
  - Set pos\_profile from (get\_pos\_profile(self.company) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_pos\_profile(self.company) → mapping().
  - If not pos\_profile.
    - Return no value.
  - Set self.pos\_profile from pos\_profile.get(“name”).
- Set pos from mapping().
- If self.pos\_profile.
  - Set pos from Platform.get\_doc(“POS Profile”, self.pos\_profile).
- If pos.
  - If not for\_validate.
    - Evaluate update\_multi\_mode\_option(self, pos).
    - Set self.tax\_category from pos.get(“tax\_category”).
  - If (not for\_validate and not self.customer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not for\_validate → not self.customer.
    - Set self.customer from pos.customer.
  - If not for\_validate.
    - Set self.ignore\_pricing\_rule from pos.ignore\_pricing\_rule.
  - If pos.get(“account\_for\_change\_amount”).
    - Set self.account\_for\_change\_amount from pos.get(“account\_for\_change\_amount”).
  - For each fieldname in tuple(“currency”, “letter\_head”, “tc\_name”, “company”, …).
    - If (not for\_validate or (for\_validate and not self.get(fieldname))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not for\_validate → (for\_validate and not self.get(fieldname)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → not self.get(fieldname).
      - Evaluate self.set(fieldname, pos.get(fieldname)).
  - If pos.get(“company\_address”).
    - Set self.company\_address from pos.get(“company\_address”).
  - If self.customer.
    - Set tuple(customer\_price\_list, customer\_group) from Platform.get\_value(“Customer”, self.customer, list(“default\_price\_list”, “customer\_group”)).
    - Set customer\_group\_price\_list from Platform.get\_value(“Customer Group”, customer\_group, “default\_price\_list”).
    - Set selling\_price\_list from (customer\_price\_list or customer\_group\_price\_list or pos.get(“selling\_price\_list”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer\_price\_list → customer\_group\_price\_list → pos.get(“selling\_price\_list”).
  - Otherwise.
    - Set selling\_price\_list from pos.get(“selling\_price\_list”).
  - If selling\_price\_list.
    - Evaluate self.set(“selling\_price\_list”, selling\_price\_list).
  - For each item in self.get(“items”).
    - If item.get(“item\_code”).
      - Set profile\_details from get\_pos\_profile\_item\_details\_(ItemDetailsCtx(item.as\_dict()), pos, pos, update\_data = true).
      - For each tuple(fname, val) in profile\_details.items().
        - If (not for\_validate or (for\_validate and not item.get(fname))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not for\_validate → (for\_validate and not item.get(fname)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → not item.get(fname).
          - Evaluate item.set(fname, val).
  - If not for\_validate.
    - Set dn\_flag from any(generator of d.get(“dn\_detail”) for d drawn from self.get(“items”)).
      - Draw d from self.get(“items”).
    - Set self.update\_stock from 0 when dn\_flag, otherwise cint(pos.get(“update\_stock”)).
      - Value choice on dn\_flag — true gives 0, false gives cint(pos.get(“update\_stock”)).
  - If (self.tc\_name and not self.terms).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.tc\_name → not self.terms.
    - Set self.terms from Platform.db.get\_value(“Terms and Conditions”, self.tc\_name, “terms”).
  - If (self.taxes\_and\_charges and not len(self.get(“taxes”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.taxes\_and\_charges → not len(self.get(“taxes”)).
    - Evaluate self.set\_taxes().
- Return pos.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_cash\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1041) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1171)

<a id="op-f3c9f099c2dd90"></a>
### Sales Invoice.get company abbr

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_get_company_abbreviation`

**Inputs** self.

**Record and data access** execute query text (SELECT, Company).

**Explicit results** Platform.db.sql(query text (SELECT, Company), self.company) at 0 at 0.

**Local steps**

- Return Platform.db.sql(query text (SELECT, Company), self.company) at 0 at 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1023) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1153)

<a id="op-df9fb75940d79c"></a>
### Sales Invoice.validate debit to acc

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_debit_to_accounting`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Debit To is required” · validation helper — msg.

**Local steps**

- If not self.debit\_to.
  - Set self.debit\_to from get\_party\_account(“Customer”, self.customer, self.company).
  - If not self.debit\_to.
    - Evaluate self.raise\_missing\_debit\_credit\_account\_error(“Customer”, self.customer).
- Set account from Platform.get\_cached\_value(“Account”, self.debit\_to, list(“account\_type”, “report\_type”, “account\_currency”), as\_dict = true).
- If not account.
  - Call the validation error handler Platform.throw(translated “Debit To is required”, title = translated “Account Missing”).
- If account.report\_type differs from “Balance Sheet”.
  - Set msg from (translated “Please ensure {} account is a Balance Sheet account.”.format(Platform.bold(translated “Debit To”)) + one space).
  - Update msg using + translated “You can change the parent account to a Balance Sheet account or select a different account.”.
  - Call the validation error handler Platform.throw(msg, title = translated “Invalid Account”).
- If (self.customer and account.account\_type differs from “Receivable”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.customer → account.account\_type differs from “Receivable”.
  - Set msg from (translated “Please ensure {} account {} is a Receivable account.”.format(Platform.bold(translated “Debit To”), Platform.bold(self.debit\_to)) + one space).
  - Update msg using + translated “Change the account type to Receivable or select a different account.”.
  - Call the validation error handler Platform.throw(msg, title = translated “Invalid Account”).
- Set self.party\_account\_currency from account.account\_currency.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.debit\_to, list(“account\_type”, “report\_type”, “account\_currency”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1054) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1183)

<a id="op-0d766644b5b568"></a>
### Sales Invoice.clear unallocated mode of payments

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_clear_unallocated_mode_of_payments`

**Inputs** self.

**State and service calls** execute query text (DELETE, Sales Invoice Payment).

**Local steps**

- Evaluate self.set(“payments”, self.get(“payments”, mapping(“amount” → list(“not in”, list(0, no value, empty text))))).
- Evaluate Platform.db.sql(query text (DELETE, Sales Invoice Payment), self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1020) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1150)

<a id="op-cd8e0040ccce50"></a>
### Sales Invoice.validate with previous doc

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_with_previous_record`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Sales Order” → mapping(“ref\_dn\_field” → “sales\_order”, “compare\_fields” → list(list(“customer”, “=”), list(“company”, “=”), list(“project”, “=”), list(“currency” ….
- If (cint(Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”)) and not self.is\_return and not self.is\_internal\_customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”)) → not self.is\_return → not self.is\_internal\_customer.
  - Evaluate self.validate\_rate\_with\_reference\_doc(list(list(“Sales Order”, “sales\_order”, “so\_detail”), list(“Delivery Note”, “delivery\_note”, “dn\_detail”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “maintain\_same\_sales\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L2151) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L10)

<a id="op-2aaac7e1aa0cac"></a>
### Sales Invoice.validate closed delivery notes

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_closed_delivery_notes`

**Inputs** self.

**Record and data access** read “Delivery Note” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Delivery Note {0} is closed and cannot be invoiced”.format(“, ”.join(generator of Platform.bold(name) for name drawn from closed)).

**Local steps**

- Set delivery\_notes from set of d.delivery\_note for d drawn from self.items where d.delivery\_note.
  - Draw d from self.items, keep a combination only if (d.delivery\_note).
- If (self.is\_return or not delivery\_notes).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → not delivery\_notes.
  - Return no value.
- If closed bound to Platform.get\_all(“Delivery Note”, filters = mapping(“name” → tuple(“in”, list(delivery\_notes)), “status” → “Closed”), pluck = “name”).
  - Call the validation error handler Platform.throw(translated “Delivery Note {0} is closed and cannot be invoiced”.format(“, ”.join(generator of Platform.bold(name) for name drawn from closed))).
    - Draw name from closed.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1053)

<a id="op-5a4625706b63f2"></a>
### Sales Invoice.validate delivery note rows billed by invoice

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_delivery_note_rows_billed_by_invoice`

**Inputs** self.

**Record and data access** read “Delivery Note Item” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Delivery Note {1} was created from Sales Invoice {2}, which already bills it”.format(d.idx, Platform.bold(d.delivery\_note), get\_link\_to\_form(“Sales Invoice”, invoice)).

**Local steps**

- Set dn\_details from list of d.dn\_detail for d drawn from self.items where d.dn\_detail.
  - Draw d from self.items, keep a combination only if (d.dn\_detail).
- If (self.is\_return or not dn\_details).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → not dn\_details.
  - Return no value.
- Set billing\_invoices from Platform.\_dict(Platform.get\_all(“Delivery Note Item”, filters = mapping(“name” → tuple(“in”, dn\_details), “against\_sales\_invoice” → tuple(“is”, “set”)), fields = list(“name”, “against\_sales\_invoice”), as\_l ….
- For each d in self.items.
  - Set invoice from billing\_invoices.get(d.dn\_detail).
  - If (invoice and invoice differs from self.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in invoice → invoice differs from self.name.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Delivery Note {1} was created from Sales Invoice {2}, which already bills it”.format(d.idx, Platform.bold(d.delivery\_note), get\_link\_to\_form(“Sales Invoice”, invoice))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1055)

<a id="op-039c3e9bc951f3"></a>
### Sales Invoice.set against income account

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_set_against_income_account`

**Inputs** self.

**Local steps**

- Set against\_acc from list().
- For each d in self.get(“items”).
  - If (d.income\_account and d.income\_account does not belong to against\_acc).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.income\_account → d.income\_account does not belong to against\_acc.
    - Evaluate against\_acc.append(d.income\_account).
- Set self.against\_income\_account from “,”.join(against\_acc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L2872) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1038) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1168)

<a id="op-43052adce78f21"></a>
### Sales Invoice.force set against income account

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_force_set_against_income_account`

**Inputs** self.

**State and service calls** request set\_value on self.doctype.

**Local steps**

- Evaluate self.set\_against\_income\_account().
- Evaluate Platform.db.set\_value(self.doctype, self.name, “against\_income\_account”, self.against\_income\_account).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set against income account](operations-100.md#op-039c3e9bc951f3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L3052) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1022) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1152)

<a id="op-1a5d95cac2d3f1"></a>
### Sales Invoice.add remarks

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_add_remarks`

**Inputs** self.

**Local steps**

- If not self.remarks.
  - If self.po\_no.
    - Set self.remarks from translated “Against Customer Order {0}”.format(self.po\_no).
    - If self.po\_date.
      - Update self.remarks using + (one space + translated “dated {0}”.format(formatdate(self.po\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L3162) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1012) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1142)

<a id="op-c02e566edc3565"></a>
### Sales Invoice.validate auto set posting time

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_auto_set_posting_time`

**Inputs** self.

**Local steps**

- If (self.is\_new() and self.amended\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.amended\_from.
  - Set self.set\_posting\_time from 1.
- Evaluate self.validate\_posting\_time().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L3359) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1052) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1182)

<a id="op-b6525af3bc7696"></a>
### Sales Invoice.so dn required

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_sales_order_record_name_required`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Customer” via get\_value.

**Explicit results** no value.

**Local steps**

- If self.is\_return.
  - Return no value.
- Set prev\_doc\_field\_map from mapping(“Sales Order” → list(“so\_required”, “is\_pos”), “Delivery Note” → list(“dn\_required”, “update\_stock”)).
- For each tuple(key, value) in prev\_doc\_field\_map.items().
  - If Platform.get\_single\_value(“Selling Settings”, value at 0) equals “Yes”.
    - If Platform.get\_value(“Customer”, self.customer, value at 0).
      - Continue with the next iteration or loop test.
    - For each d in self.get(“items”).
      - If (d.item\_code and not d.get(nested operand in the contract.lower().replace(one space, “\_”)) and not self.get(value at 1)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.item\_code → not d.get(key.lower().replace(one space, “\_”)) → not self.get(value at 1).
        - Evaluate msgprint(translated “{0} is mandatory for Item {1}”.format(key, d.item\_code), raise\_exception = 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, value at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L3460) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1036) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1166)

<a id="op-52a083bdca169a"></a>
### Sales Invoice.validate proj cust

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_project_customer`

**Inputs** self.

**Record and data access** execute query text (SELECT, Project).

**Local steps**

- If (self.project and self.customer).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.project → self.customer.
  - Set res from Platform.db.sql(query text (SELECT, Project), tuple(self.project, self.customer)).
  - If not res.
    - Evaluate throw(translated “Customer {0} does not belong to project {1}”.format(self.customer, self.project)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L5)

<a id="op-edfb8e9c769e2f"></a>
### Sales Invoice.validate pos

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_point_of_sale`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Paid amount + Write Off Amount can not be greater than Grand Total”.

**Local steps**

- If not self.get(“is\_consolidated”).
  - For each payment in (self.get(“payments”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“payments”) → list().
    - Evaluate validate\_enabled\_mode\_of\_payment(payment.mode\_of\_payment).
- If self.is\_return.
  - Set invoice\_total from (self.rounded\_total or self.grand\_total).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.rounded\_total → self.grand\_total.
  - If ((abs(flt(self.paid\_amount)) + abs(flt(self.write\_off\_amount))) − abs(flt(invoice\_total))) &gt; (1.0 ÷ (10.0 to the power (self.precision(“grand\_total”) + 1.0))).
    - Call the validation error handler Platform.throw(translated “Paid amount + Write Off Amount can not be greater than Grand Total”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1061) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L3)

<a id="op-5898d8f5e90584"></a>
### Sales Invoice.validate mandatory pos fields

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_mandatory_pos_fields`

**Inputs** self.

**Record and data access** read “POS Settings” via get\_single\_value · read “POS Field” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.MandatoryError — message.format(“, ”.join(map(Platform.bold, missing\_fields))).

**Local steps**

- If (Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”) differs from self.doctype or (self.doctype equals “Sales Invoice” and self.flags.is\_consolidated)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”) differs from self.doctype → (self.doctype equals “Sales Invoice” and self.flags.is\_consolidated).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.flags.is\_consolidated.
  - Return no value.
- Set mandatory\_fields from Platform.get\_all(“POS Field”, filters = mapping(“parent” → “POS Settings”, “parenttype” → “POS Settings”, “reqd” → 1), fields = list(“fieldname”, “label”, “fieldtype”)).
- Set missing\_fields from list().
- For each field in mandatory\_fields.
  - If (field.fieldtype equals “Check” or not self.meta.has\_field(field.fieldname)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.fieldtype equals “Check” → not self.meta.has\_field(field.fieldname).
    - Continue with the next iteration or loop test.
  - Set value from self.get(field.fieldname).
  - Set value from empty text when value belongs to tuple(no value, list()), otherwise cstr(value).
    - Value choice on value belongs to tuple(no value, list()) — true gives empty text, false gives cstr(value).
  - If (field.fieldtype equals “Text Editor” and “&lt;img” belongs to value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype equals “Text Editor” → “&lt;img” belongs to value.
    - Continue with the next iteration or loop test.
  - If not strip\_html(value).strip().
    - Evaluate missing\_fields.append(translated field.label).
- If not missing\_fields.
  - Return no value.
- Set message from translated “{0} is mandatory in POS Settings”.
- If len(missing\_fields) &gt; 1.
  - Set message from translated “{0} are mandatory in POS Settings”.
- Call the validation error handler Platform.throw(message.format(“, ”.join(map(Platform.bold, missing\_fields))), Platform.MandatoryError, title = translated “Missing POS Fields”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L419) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1057)

<a id="op-c7b1057f5d07d2"></a>
### Sales Invoice.validate created using pos

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_validate_created_using_pos`

**Inputs** self.

**Record and data access** read “POS Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “POS Profile is mandatory to mark this invoice as POS Transaction.” · validation helper — translated “Transactions using Sales Invoice in POS are disabled.”.

**Local steps**

- If (self.is\_created\_using\_pos and not self.pos\_profile).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_created\_using\_pos → not self.pos\_profile.
  - Call the validation error handler Platform.throw(translated “POS Profile is mandatory to mark this invoice as POS Transaction.”).
- Set self.invoice\_type\_in\_pos from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).
- If (self.invoice\_type\_in\_pos equals “POS Invoice” and not self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.invoice\_type\_in\_pos equals “POS Invoice” → not self.is\_return.
  - Call the validation error handler Platform.throw(translated “Transactions using Sales Invoice in POS are disabled.”).
- Evaluate self.validate\_pos\_opening\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate pos opening entry](operations-100.md#op-6802474649dda7).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“POS Settings”, “invoice\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1054)

<a id="op-95cadb5c02cdae"></a>
### Sales Invoice.validate full payment

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_full_payment`

**Inputs** self.

**Record and data access** read “POS Profile” via get\_value.

**Explicit failure paths** validation helper with PartialPaymentValidationError.

**Local steps**

- Set allow\_partial\_payment from Platform.db.get\_value(“POS Profile”, self.pos\_profile, “allow\_partial\_payment”).
- Set invoice\_total from (flt(self.rounded\_total) or flt(self.grand\_total)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.rounded\_total) → flt(self.grand\_total).
- If (self.docstatus equals 1 and not self.is\_return and not allow\_partial\_payment and flt((flt(self.paid\_amount) + flt(self.write\_off\_amount)), self.precision(“grand\_total”)) &lt; invoice\_total).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → not self.is\_return → not allow\_partial\_payment → flt((flt(self.paid\_amount) + flt(self.write\_off\_amount)), self.precision(“grand\_total”)) &lt; invoice\_total.
  - Call the validation error handler Platform.throw(msg = translated “Partial Payment in POS Transactions are not allowed.”, exc = PartialPaymentValidationError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1058) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1187)

<a id="op-6802474649dda7"></a>
### Sales Invoice.validate pos opening entry

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_point_of_sale_opening_entry`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper · validation helper — translated “Posting date and time must be on the same day as, and at or after, the start of POS Opening Entry {0}: {1}.”.format(opening\_entry.name, opening\_entry.period\_start\_date).

**Local steps**

- Set opening\_entries from Platform.get\_all(“POS Opening Entry”, fields = list(“name”, “period\_start\_date”), filters = mapping(“pos\_profile” → self.pos\_profile, “status” → “Open”), order\_by = “period\_start\_date desc”).
- If not opening\_entries.
  - Call the validation error handler Platform.throw(title = translated “POS Opening Entry Missing”, msg = translated “No open POS Opening Entry found for POS Profile {0}.”.format(Platform.bold(self.pos\_profile))).
- <a id="op-6802474649dda7-guard-16"></a>If len(opening\_entries) &gt; 1.
  - Call the validation error handler Platform.throw(title = translated “Multiple POS Opening Entry”, msg = translated “POS Profile - {0} has multiple open POS Opening Entries. Please close or cancel the existing entries before  …”.format(self ….
- Set opening\_entry from opening\_entries at 0.
- If self.set\_posting\_time.
  - Set posting\_datetime from get\_datetime(formatted text {self.posting\_date} {(self.posting\_time or “00:00:00”)}).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.posting\_time → “00:00:00”.
  - If (getdate(posting\_datetime) differs from getdate(opening\_entry.period\_start\_date) or posting\_datetime &lt; get\_datetime(opening\_entry.period\_start\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getdate(posting\_datetime) differs from getdate(opening\_entry.period\_start\_date) → posting\_datetime &lt; get\_datetime(opening\_entry.period\_start\_date).
    - Call the validation error handler Platform.throw(translated “Posting date and time must be on the same day as, and at or after, the start of POS Opening Entry {0}: {1}.”.format(opening\_entry.name, opening\_entry.period\_start\_date)).
  - If getdate(posting\_datetime) &lt; getdate().
    - Return no value.
- If getdate(opening\_entry.period\_start\_date) differs from getdate().
  - Call the validation error handler Platform.throw(title = translated “Outdated POS Opening Entry”, msg = translated “POS Opening Entry - {0} is outdated. Please close the POS and create a new POS Opening Entry.”.format(opening\_entries at 0. ….

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(opening\_entries) &gt; 1, length of opening\_entries = 2 selects the branch that calls the validation-error handler. With length of opening\_entries = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6802474649dda7-guard-16)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L4)

<a id="op-f3d4b2b080fd16"></a>
### Sales Invoice.validate warehouse

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_warehouse`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Warehouse required for stock Item {0}”.format(d.item\_code).

**Local steps**

- Evaluate super().validate\_warehouse().
- For each d in self.get\_item\_list().
  - If (not d.warehouse and d.item\_code and Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.warehouse → d.item\_code → Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”).
    - Call the validation error handler Platform.throw(translated “Warehouse required for stock Item {0}”.format(d.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “is\_stock\_item”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L4310) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L9)

<a id="op-2b89af9c87d8ad"></a>
### Sales Invoice.validate delivery note

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_delivery_note`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Stock cannot be updated against the following Delivery Notes: {0}”.format(comma\_and(notes)).

**Local steps**

- If not cint(self.update\_stock).
  - Return no value.
- Set notes from list of item.delivery\_note for item drawn from self.items where item.delivery\_note.
  - Draw item from self.items, keep a combination only if (item.delivery\_note).
- If notes.
  - Call the validation error handler Platform.throw(translated “Stock cannot be updated against the following Delivery Notes: {0}”.format(comma\_and(notes))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L4524) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1055) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1184)

<a id="op-a70f641ee6e0a4"></a>
### Sales Invoice.allow write off only on pos

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_allow_write_off_only_on_pos`

**Inputs** self.

**Local steps**

- If (not self.is\_pos and self.write\_off\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_pos → self.write\_off\_account.
  - Set self.write\_off\_account from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1002)

<a id="op-681460dcc500af"></a>
### Sales Invoice.validate subcontracted sales order

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_subcontracted_sales_order`

**Inputs** self.

**Record and data access** read “Sales Order” via get\_all.

**Explicit failure paths** validation helper — translated “All items must be linked to a Sales Order or Subcontracting Inward Order for this Sales Invoice.” · validation helper — translated “All linked Sales Orders must be subcontracted.”.

**Local steps**

- If self.has\_subcontracted.
  - If list of item for item drawn from self.items where (not item.sales\_order and not item.scio\_detail).
    - Draw item from self.items, keep a combination only if ((not item.sales\_order and not item.scio\_detail)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.sales\_order → not item.scio\_detail.
    - Call the validation error handler Platform.throw(translated “All items must be linked to a Sales Order or Subcontracting Inward Order for this Sales Invoice.”).
  - If not all(Platform.get\_all(“Sales Order”, mapping(“name” → list(“in”, list of nested operand in the contract.sales\_order for item drawn from nested operand in the contract.items where nested operand in the contract. …).
    - Draw item from self.items, keep a combination only if (item.sales\_order).
    - Call the validation error handler Platform.throw(translated “All linked Sales Orders must be subcontracted.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L4719) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L7)

<a id="op-9c9b5a167cbce1"></a>
### Sales Invoice.validate scio self rm qty

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_sales_commission_self_raw_material_quantity`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Stock quantity {1} ({2}) for item {3} cannot exceed {4}”.format(item.idx, stock\_qty at item.scio\_detail, item.stock\_uom, get\_link\_to\_form(“Item”, item.item\_code), …).

**Local steps**

- Set self\_rms from list of item for item drawn from self.items where item.scio\_detail.
  - Draw item from self.items, keep a combination only if (item.scio\_detail).
- If self\_rms.
  - Set stock\_qty from self.get\_scio\_self\_rm\_stock\_qty().
  - Set table from Platform.qb.DocType(“Subcontracting Inward Order Received Item”).
  - Set query from nested operand in the contract.qb.from\_(table).select(table.required\_qty, table.consumed\_qty, table.billed\_qty, table.name).where((table.docstatus equals 1 bitwise and table.name.isin(list(stock\_qty)))).
  - Set result from query.run(as\_dict = true).
  - Set data from mapping of item.name → item for item drawn from result.
    - Draw item from result.
  - For each item in self\_rms.
    - Set row from data.get(item.scio\_detail).
    - Set max\_qty from (max(row.required\_qty, row.consumed\_qty) − row.billed\_qty).
    - If stock\_qty at item.scio\_detail &gt; max\_qty.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Stock quantity {1} ({2}) for item {3} cannot exceed {4}”.format(item.idx, stock\_qty at item.scio\_detail, item.stock\_uom, get\_link\_to\_form(“Item”, item.item\_code), …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get scio self rm stock qty](operations-099.md#op-2f0d73b6126f99).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1064) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L6)

<a id="op-8f241247fcdfe9"></a>
### Sales Invoice.validate write off account

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_write_off_account`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If (flt(self.write\_off\_amount) and not self.write\_off\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.write\_off\_amount) → not self.write\_off\_account.
  - Set self.write\_off\_account from Platform.get\_cached\_value(“Company”, self.company, “write\_off\_account”).
- If (flt(self.write\_off\_amount) and not self.write\_off\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.write\_off\_amount) → not self.write\_off\_account.
  - Evaluate msgprint(translated “Please enter Write Off Account”, raise\_exception = 1).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “write\_off\_account”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L5646) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L11)
