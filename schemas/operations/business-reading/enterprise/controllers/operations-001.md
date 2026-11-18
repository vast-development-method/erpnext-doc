# Shared transaction rules · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-da81164a8e3833"></a>
### Accounts Controller.get print settings

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_print_settings`

**Inputs** self.

**Explicit results** print\_setting\_fields.

**Local steps**

- Set print\_setting\_fields from list().
- Set items\_field from self.meta.get\_field(“items”).
- If (items\_field and items\_field.fieldtype equals “Table”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in items\_field → items\_field.fieldtype equals “Table”.
  - Update print\_setting\_fields using + list(“compact\_item\_print”, “print\_uom\_after\_quantity”).
- Set taxes\_field from self.meta.get\_field(“taxes”).
- If (taxes\_field and taxes\_field.fieldtype equals “Table”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in taxes\_field → taxes\_field.fieldtype equals “Table”.
  - Update print\_setting\_fields using + list(“print\_taxes\_with\_zero\_amount”).
- Return print\_setting\_fields.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L1418) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L618) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L323)

<a id="op-ede6af2bafe05a"></a>
### Accounts Controller.company currency

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_company_currency`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.\_\_company\_currency.

**Local steps**

- If not hasattr(self, “\_\_company\_currency”).
  - Set self.\_\_company\_currency from Enterprise.get\_company\_currency(self.company).
- Return self.\_\_company\_currency.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L1654) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L311)

<a id="op-07fec5f37c2b9a"></a>
### Accounts Controller.onload

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_onload`

**Inputs** self.

**Local steps**

- Evaluate self.set\_onload(“make\_payment\_via\_journal\_entry”, Platform.client\_cache.get\_doc(“Accounts Settings”).make\_payment\_via\_journal\_entry).
- If self.is\_new().
  - Set relevant\_docs from tuple(“Quotation”, “Purchase Order”, “Sales Order”, “Purchase Invoice”, …).
  - If self.doctype belongs to relevant\_docs.
    - Evaluate self.set\_payment\_schedule().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set payment schedule](operations-005.md#op-f477c9b4096cad).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L339)

<a id="op-b698ca64667791"></a>
### Accounts Controller.before insert

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_clearance\_date\_on\_amend().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear clearance date on amend](operations-001.md#op-9844078d116021).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L2009) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L594) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L299)

<a id="op-9844078d116021"></a>
### Accounts Controller.clear clearance date on amend

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_clear_clearance_date_on_amend`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.get(“amended\_from”).
  - Return no value.
- If self.meta.has\_field(“clearance\_date”).
  - Set self.clearance\_date from no value.
- For each payment in (self.get(“payments”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“payments”) → list().
  - If payment.meta.has\_field(“clearance\_date”).
    - Set payment.clearance\_date from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L2060) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L308)

<a id="op-e9e6c90af4c2ca"></a>
### Accounts Controller.on update

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_on_update`

**Inputs** self.

**Local steps**

- Bind dependencies process\_item\_wise\_tax\_details.
- Evaluate process\_item\_wise\_tax\_details(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L2279) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L338)

<a id="op-e30a1f15606dcf"></a>
### Accounts Controller.remove bundle for non stock invoices

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_remove_bundle_for_non_stock_invoices`

**Inputs** self.

**Local steps**

- Set has\_sabb from false.
- If (self.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”) and not self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”) → not self.update\_stock.
  - For each item in self.get(“items”).
    - If item.serial\_and\_batch\_bundle.
      - Set item.serial\_and\_batch\_bundle from no value.
      - Set has\_sabb from true.
- If has\_sabb.
  - Evaluate self.remove\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove serial and batch bundle](operations-001.md#op-e4ed509dcb803d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L2339) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L343)

<a id="op-641b96881a3999"></a>
### Accounts Controller.ensure supplier is not blocked

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_ensure_supplier_is_not_blocked`

**Inputs** self.

**State and service calls** msgprint with translated “{0} is blocked so this transaction cannot proceed”.format(supplier).

**Explicit results** no value.

**Local steps**

- If (self.meta.has\_field(“is\_return”) and self.is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.has\_field(“is\_return”) → self.is\_return.
  - Return no value.
- Set tuple(hold\_type, suppliers) from self.get\_supplier\_hold\_scope().
- For each supplier in set of supplier for supplier drawn from suppliers where supplier.
  - Draw supplier from suppliers, keep a combination only if (supplier).
  - If Platform.get\_lazy\_doc(“Supplier”, supplier).is\_blocked\_for(hold\_type).
    - Evaluate Platform.msgprint(translated “{0} is blocked so this transaction cannot proceed”.format(supplier), raise\_exception = 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get supplier hold scope](operations-001.md#op-01f32f3ea65992).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L314)

<a id="op-01f32f3ea65992"></a>
### Accounts Controller.get supplier hold scope

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_supplier_hold_scope`

**Inputs** self.

**Declared result** tuple at tuple((str bitwise or no value), list at str).

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** tuple(“Invoices”, list(self.supplier)) · tuple(“All”, list(self.supplier)) · tuple(“All”, list of row.supplier for row drawn from self.suppliers) · tuple(“Payments”, list(self.party)) · tuple(“Payments”, list of row.party for row drawn from self.accounts where (row.party\_type equals “Supplier” and (flt(nested operand in the contract.debit\_in\_account\_currency) − flt(nested operand in the c … · 1 additional forms in the steps below.

**Local steps**

- If self.doctype belongs to tuple(“Purchase Order”, “Purchase Invoice”).
  - Return tuple(“Invoices”, list(self.supplier)).
- If self.doctype belongs to tuple(“Purchase Receipt”, “Supplier Quotation”).
  - Return tuple(“All”, list(self.supplier)).
- If self.doctype equals “Request for Quotation”.
  - Return tuple(“All”, list of row.supplier for row drawn from self.suppliers).
    - Draw row from self.suppliers.
- If (self.doctype equals “Payment Entry” and self.party\_type equals “Supplier”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Payment Entry” → self.party\_type equals “Supplier”.
  - Return tuple(“Payments”, list(self.party)).
- If (self.doctype equals “Journal Entry” and any(generator of ((nested operand in the contract(nested operand in the contract) − nested operand in the contract(nested operand in the contract)) &gt; 0 and nested o ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Journal Entry” → any(generator of ((flt(nested operand in the contract.credit\_in\_account\_currency) − flt(nested operand in the contract.debit\_in\_account\_currency)) &gt; 0 and Platform.get\_cached\_value(“Account”, row.account, “acc …).
  - Draw row from self.accounts.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (flt(row.credit\_in\_account\_currency) − flt(row.debit\_in\_account\_currency)) &gt; 0 → Platform.get\_cached\_value(“Account”, row.account, “account\_type”) belongs to tuple(“Bank”, “Cash”).
  - Return tuple(“Payments”, list of row.party for row drawn from self.accounts where (row.party\_type equals “Supplier” and (flt(nested operand in the contract.debit\_in\_account\_currency) − flt(nested operand in the c ….
    - Draw row from self.accounts, keep a combination only if ((row.party\_type equals “Supplier” and (flt(row.debit\_in\_account\_currency) − flt(row.credit\_in\_account\_currency)) &gt; 0)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.party\_type equals “Supplier” → (flt(row.debit\_in\_account\_currency) − flt(row.credit\_in\_account\_currency)) &gt; 0.
- Return tuple(no value, list()).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, row.account, “account\_type”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L160)

<a id="op-0de7194df30a3f"></a>
### Accounts Controller.validate against voucher outstanding

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_against_voucher_outstanding`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**State and service calls** msgprint with msg.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_meta.
- If not get\_meta(self.doctype).has\_field(“outstanding\_amount”).
  - Return no value.
- If (self.get(“is\_return”) and self.return\_against and not (self.get(“is\_pos”) or self.get(“is\_paid”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → self.return\_against → not (self.get(“is\_pos”) or self.get(“is\_paid”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_pos”) → self.get(“is\_paid”).
  - Set against\_voucher\_outstanding from Platform.get\_value(self.doctype, self.return\_against, “outstanding\_amount”).
  - Set document\_type from “Credit Note” when self.doctype equals “Sales Invoice”, otherwise “Debit Note”.
    - Value choice on self.doctype equals “Sales Invoice” — true gives “Credit Note”, false gives “Debit Note”.
  - Set msg from empty text.
  - If self.get(“update\_outstanding\_for\_self”).
    - Set msg from translated “We can see {0} is made against {1}. If you want {1}'s outstanding to be updated, uncheck the '{2}' checkbox.”.format(Platform.bold(document\_type), get\_link\_to\_form(self.doctype, self.get(“retur ….
  - Otherwise.
    - If (not self.update\_outstanding\_for\_self and abs((flt(self.rounded\_total) or flt(self.grand\_total))) &gt; flt(against\_voucher\_outstanding)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.update\_outstanding\_for\_self → abs((flt(self.rounded\_total) or flt(self.grand\_total))) &gt; flt(against\_voucher\_outstanding).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.rounded\_total) → flt(self.grand\_total).
      - Set self.update\_outstanding\_for\_self from 1.
      - Set msg from translated “The outstanding amount {0} in {1} is lesser than {2}. Updating the outstanding to this invoice.”.format(against\_voucher\_outstanding, get\_link\_to\_form(self.doctype, self.get(“return\_against”)),  ….
  - If msg.
    - Update msg using + (text in the contract + translated “You can use {0} to reconcile against {1} later.”.format(get\_link\_to\_form(“Payment Reconciliation”), get\_link\_to\_form(self.doctype, self.get(“return\_against”)))).
    - Evaluate Platform.msgprint(msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L3050) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L366)

<a id="op-6c2ac22d9816eb"></a>
### Accounts Controller.is negative grand total allowed

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_is_negative_grand_total_allowed`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value.

**Explicit results** bool(Platform.get\_single\_value(“Selling Settings”, “allow\_negative\_rates\_for\_items”)) · bool(Platform.get\_single\_value(“Buying Settings”, “allow\_negative\_rates\_for\_items”)) · false.

**Local steps**

- If self.doctype equals “Sales Order”.
  - Return bool(Platform.get\_single\_value(“Selling Settings”, “allow\_negative\_rates\_for\_items”)).
- If self.doctype equals “Purchase Order”.
  - Return bool(Platform.get\_single\_value(“Buying Settings”, “allow\_negative\_rates\_for\_items”)).
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “allow\_negative\_rates\_for\_items”), Platform.get\_single\_value(“Buying Settings”, “allow\_negative\_rates\_for\_items”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L3917) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L628) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L332)

<a id="op-9d7345a6581367"></a>
### Accounts Controller.validate

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Rows: {0} in {1} section are Invalid. Reference Name should point to a valid Payment Entry or Journal Entry.”.format(Platform.bold(comma\_and(list of x.idx for x drawn from invalid\_advances)), P ….

**Local steps**

- Evaluate self.sync\_mapped\_discount\_with\_header().
- If (not self.get(“is\_return”) and not self.get(“is\_debit\_note”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“is\_return”) → not self.get(“is\_debit\_note”).
  - Evaluate self.validate\_qty\_is\_not\_zero().
- If (self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “POS Invoice”) and self.get(“is\_return”) and self.get(“update\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”, “POS Invoice”) → self.get(“is\_return”) → self.get(“update\_stock”).
  - Evaluate self.validate\_zero\_qty\_for\_return\_invoices\_with\_stock().
- If (self.get(“\_action”) and self.\_action differs from “update\_after\_submit”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“\_action”) → self.\_action differs from “update\_after\_submit”.
  - Evaluate self.set\_missing\_values(for\_validate = true).
- Evaluate self.validate\_price\_list().
- If self.get(“\_action”) equals “submit”.
  - Evaluate self.remove\_bundle\_for\_non\_stock\_invoices().
- Evaluate self.ensure\_supplier\_is\_not\_blocked().
- Evaluate self.validate\_date\_with\_fiscal\_year().
- Evaluate self.validate\_party\_accounts().
- If self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - If self.is\_return.
    - Evaluate self.validate\_qty().
  - Otherwise.
    - Evaluate self.clear\_stale\_deferred\_fields().
    - Evaluate self.validate\_deferred\_start\_and\_end\_date().
- Evaluate self.validate\_inter\_company\_reference().
- Evaluate self.validate\_inter\_company\_currency().
- Evaluate self.validate\_internal\_transaction().
- Evaluate self.disable\_pricing\_rule\_on\_internal\_transfer().
- Evaluate self.disable\_tax\_included\_prices\_for\_internal\_transfer().
- Evaluate self.set\_incoming\_rate().
- Evaluate self.init\_internal\_values().
- Evaluate self.validate\_against\_voucher\_outstanding().
- If self.meta.get\_field(“taxes\_and\_charges”).
  - Evaluate self.validate\_enabled\_taxes\_and\_charges().
  - Evaluate self.validate\_tax\_account\_company().
- Evaluate self.set\_taxes\_and\_charges().
- If self.meta.get\_field(“currency”).
  - Evaluate self.calculate\_taxes\_and\_totals().
  - If (not self.meta.get\_field(“is\_return”) or not self.is\_return).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.meta.get\_field(“is\_return”) → not self.is\_return.
    - If not self.is\_negative\_grand\_total\_allowed().
      - Evaluate self.validate\_value(“base\_grand\_total”, “&gt;=”, 0).
  - Evaluate validate\_return(self).
- Evaluate self.validate\_all\_documents\_schedule().
- Evaluate self.validate\_party().
- Evaluate self.validate\_party\_specific\_items().
- Evaluate self.validate\_currency().
- Evaluate self.validate\_party\_account\_currency().
- Evaluate self.validate\_return\_against\_account().
- If self.doctype belongs to list(“Purchase Invoice”, “Sales Invoice”).
  - If invalid\_advances bound to list of x for x drawn from self.advances where (not x.reference\_type or not x.reference\_name).
    - Draw x from self.advances, keep a combination only if ((not x.reference\_type or not x.reference\_name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not x.reference\_type → not x.reference\_name.
    - Call the validation error handler Platform.throw(translated “Rows: {0} in {1} section are Invalid. Reference Name should point to a valid Payment Entry or Journal Entry.”.format(Platform.bold(comma\_and(list of x.idx for x drawn from invali ….
      - Draw x from invalid\_advances.
  - Set pos\_check\_field from “is\_pos” when self.doctype equals “Sales Invoice”, otherwise “is\_paid”.
    - Value choice on self.doctype equals “Sales Invoice” — true gives “is\_pos”, false gives “is\_paid”.
  - If (cint(self.allocate\_advances\_automatically) and not cint(self.get(pos\_check\_field))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.allocate\_advances\_automatically) → not cint(self.get(pos\_check\_field)).
    - Evaluate self.set\_advances().
  - Evaluate self.set\_advance\_gain\_or\_loss().
  - Evaluate self.validate\_deferred\_income\_expense\_account().
  - Evaluate self.set\_inter\_company\_account().
- If self.doctype equals “Purchase Invoice”.
  - Evaluate self.calculate\_paid\_amount().
- Within temporary\_flag(“company”, self.company).
  - Evaluate validate\_regional(self).
  - Evaluate validate\_einvoice\_fields(self).
- If (self.doctype differs from “Material Request” and not self.ignore\_pricing\_rule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype differs from “Material Request” → not self.ignore\_pricing\_rule.
  - Evaluate apply\_pricing\_rule\_on\_transaction(self).
- Evaluate self.set\_total\_in\_words().
- Evaluate self.set\_default\_letter\_head().
- Evaluate self.validate\_company\_in\_accounting\_dimension().
- Evaluate self.validate\_party\_address\_and\_contact().
- Evaluate self.validate\_company\_linked\_addresses().

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync mapped discount with header](operations-007.md#op-7d75233d51608b), [validate qty is not zero](operations-004.md#op-f7ec10e80f8d97), [validate zero qty for return invoices with stock](operations-004.md#op-6a850cd3e9d40a), [set missing values](operations-002.md#op-491e4bbcd918e7), [validate price list](operations-001.md#op-6b1babe9ee44a2), [remove bundle for non stock invoices](operations-001.md#op-e30a1f15606dcf), [ensure supplier is not blocked](operations-001.md#op-641b96881a3999), [validate date with fiscal year](operations-002.md#op-9ffa922ffe02b4), [validate party accounts](operations-002.md#op-ca5a0592338552), [clear stale deferred fields](operations-002.md#op-b6d2d3126785aa), [validate deferred start and end date](operations-002.md#op-9f4ad62547daa9), [validate inter company reference](operations-002.md#op-9ae221375c47f6), [validate inter company currency](operations-002.md#op-2256c35ca7ff7b), [validate internal transaction](operations-003.md#op-e144558218dba6), [disable pricing rule on internal transfer](operations-003.md#op-12cd99873226e1), [disable tax included prices for internal transfer](operations-003.md#op-0f94e735336fd9), [init internal values](operations-001.md#op-1f82b3d4819507), [validate against voucher outstanding](operations-001.md#op-0de7194df30a3f), [validate enabled taxes and charges](operations-003.md#op-e552f0ca97555f), [validate tax account company](operations-003.md#op-03eae2138a1719), [set taxes and charges](operations-003.md#op-810c32f9d25d61), [calculate taxes and totals](operations-002.md#op-52a893faf0bdd9), [is negative grand total allowed](operations-001.md#op-6c2ac22d9816eb), [validate all documents schedule](operations-002.md#op-92313444a6e107), [validate party](operations-005.md#op-a9be434f8ccafd), [validate party specific items](operations-005.md#op-01e46d4caaf606), [validate currency](operations-005.md#op-647bca4fdf7600), [validate party account currency](operations-005.md#op-927957e38d80fe), [validate return against account](operations-002.md#op-3ac921792c56b0), [set advances](operations-004.md#op-394eadbcea28e8), [set advance gain or loss](operations-004.md#op-55557a2929b1dd), [validate deferred income expense account](operations-002.md#op-91e2ef05500574), [set inter company account](operations-006.md#op-7d65c0d8977f92), [calculate paid amount](operations-002.md#op-493ec3a0d7149a), [set default letter head](operations-001.md#op-18cd4a2215d807), [validate company in accounting dimension](operations-001.md#op-dd4fbd870e699e), [validate party address and contact](operations-002.md#op-b3710f59a5bf10), [validate company linked addresses](operations-001.md#op-f3eddbf285facf).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L363)

<a id="op-f3eddbf285facf"></a>
### Accounts Controller.validate company linked addresses

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_company_linked_addresses`

**Inputs** self.

**Record and data access** read “Dynamic Link” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} does not belong to the Company {1}.”.format(translated self.meta.get\_label(field), bold(self.company)).

**Local steps**

- Set address\_fields from list().
- Set sales\_doctypes from tuple(“Quotation”, “Sales Order”, “Delivery Note”, “Sales Invoice”).
- Set purchase\_doctypes from tuple(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”, “Supplier Quotation”).
- If self.doctype belongs to sales\_doctypes.
  - Set address\_fields from list(“dispatch\_address\_name”, “company\_address”).
- Otherwise.
  - If self.doctype belongs to purchase\_doctypes.
    - Set address\_fields from list(“billing\_address”, “shipping\_address”).
- If not address\_fields.
  - Return no value.
- Set is\_drop\_ship from (self.doctype belongs to set(“Purchase Order”, “Purchase Invoice”, “Sales Order”, “Sales Invoice”) and self.is\_drop\_ship(self.items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to set(“Purchase Order”, “Purchase Invoice”, “Sales Order”, “Sales Invoice”) → self.is\_drop\_ship(self.items).
- For each field in address\_fields.
  - Set address from self.get(field).
  - If (field belongs to list(“dispatch\_address\_name”, “shipping\_address”) and is\_drop\_ship).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in field belongs to list(“dispatch\_address\_name”, “shipping\_address”) → is\_drop\_ship.
    - Continue with the next iteration or loop test.
  - If (address and not Platform.db.exists(“Dynamic Link”, mapping(“parent” → address, “parenttype” → “Address”, “link\_doctype” → “Company”, “link\_name” → self.company))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in address → not Platform.db.exists(“Dynamic Link”, mapping(“parent” → address, “parenttype” → “Address”, “link\_doctype” → “Company”, “link\_name” → self.company)).
    - Call the validation error handler Platform.throw(translated “{0} does not belong to the Company {1}.”.format(translated self.meta.get\_label(field), bold(self.company))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is drop ship](operations-001.md#op-d0ccd000e4df28).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L196)

<a id="op-d0ccd000e4df28"></a>
### Accounts Controller.is drop ship

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_is_drop_ship`

**Inputs** items.

**Wrappers, in declaration order** staticmethod.

**Explicit results** any(generator of item.delivered\_by\_supplier for item drawn from items).

**Local steps**

- Return any(generator of item.delivered\_by\_supplier for item drawn from items).
  - Draw item from items.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L168)

<a id="op-6b1babe9ee44a2"></a>
### Accounts Controller.validate price list

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_price_list`

**Inputs** self.

**Record and data access** read “Price List” via get\_value · read self.doctype via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Price List {0} is disabled”.format(get\_link\_to\_form(“Price List”, price\_list)) · validation helper — message.format(get\_link\_to\_form(“Price List”, price\_list)).

**Local steps**

- If self.get(“selling\_price\_list”).
  - Set tuple(price\_list\_field, transaction\_side) from tuple(“selling\_price\_list”, “selling”).
- Otherwise.
  - Set tuple(price\_list\_field, transaction\_side) from tuple(“buying\_price\_list”, “buying”).
- Set price\_list from self.get(price\_list\_field).
- If not price\_list.
  - Return no value.
- Set details from (Platform.db.get\_value(“Price List”, price\_list, list(“enabled”, transaction\_side), as\_dict = true) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Price List”, price\_list, list(“enabled”, transaction\_side), as\_dict = true) → Platform.\_dict().
- Set fits\_transaction from (details.get(transaction\_side) or self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in details.get(transaction\_side) → self.is\_internal\_transfer().
- If (details.enabled and fits\_transaction).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in details.enabled → fits\_transaction.
  - Return no value.
- If (self.get(“is\_return”) and self.get(“return\_against”) and price\_list equals Platform.db.get\_value(self.doctype, mapping(“name” → self.return\_against, “docstatus” → 1), price\_list\_field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → self.get(“return\_against”) → price\_list equals Platform.db.get\_value(self.doctype, mapping(“name” → self.return\_against, “docstatus” → 1), price\_list\_field).
  - Return no value.
- If not details.enabled.
  - Call the validation error handler Platform.throw(translated “Price List {0} is disabled”.format(get\_link\_to\_form(“Price List”, price\_list)), title = translated “Disabled Price List”).
- If transaction\_side equals “selling”.
  - Set message from translated “Price List {0} cannot be used on a selling transaction”.
- Otherwise.
  - Set message from translated “Price List {0} cannot be used on a buying transaction”.
- Call the validation error handler Platform.throw(message.format(get\_link\_to\_form(“Price List”, price\_list)), title = translated “Invalid Price List”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is internal transfer](operations-006.md#op-13fa6c1b2d5ba8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L372)

<a id="op-18cd4a2215d807"></a>
### Accounts Controller.set default letter head

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_default_letter_head`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- If (hasattr(self, “letter\_head”) and not self.letter\_head).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(self, “letter\_head”) → not self.letter\_head.
  - Set self.letter\_head from Platform.db.get\_value(“Company”, self.company, “default\_letter\_head”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0365.json#L6557) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L351)

<a id="op-1f82b3d4819507"></a>
### Accounts Controller.init internal values

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_initialize_internal_values`

**Inputs** self.

**Local steps**

- If self.docstatus.is\_draft().
  - Set fields from list(“billed\_amt”, “delivered\_qty”).
  - For each item in self.get(“items”).
    - For each field in fields.
      - If hasattr(item, field).
        - Evaluate item.set(field, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L329)

<a id="op-f77e815ac07367"></a>
### Accounts Controller.before cancel

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate validate\_einvoice\_fields(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L198) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L298)

<a id="op-bd851e3f24ff8b"></a>
### Accounts Controller.remove references in unreconcile

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_remove_references_in_unreconcile`

**Inputs** self.

**Record and data access** resolve a document from “Unreconcile Payment” via get\_doc · read “Unreconcile Payment” via get\_all.

**State and service calls** call save on unreconcile\_doc · call cancel on \_doc.

**Local steps**

- Set upe from Platform.qb.DocType(“Unreconcile Payment Entries”).
- Set rows from nested operand in the contract(nested operand in the contract).select(upe.name, upe.parent).where((upe.reference\_doctype equals self.doctype bitwise and upe.reference\_name equals self.name)).run(as\_dict = true).
- If rows.
  - Set references\_map from Platform.\_dict().
  - For each x in rows.
    - Evaluate references\_map.setdefault(x.parent, list()).append(x.name).
  - For each tuple(doc, rows) in references\_map.items().
    - Set unreconcile\_doc from Platform.get\_doc(“Unreconcile Payment”, doc).
    - For each row in rows.
      - Evaluate unreconcile\_doc.remove(unreconcile\_doc.get(“allocations”, mapping(“name” → row)) at 0).
    - Set unreconcile\_doc.flags.ignore\_validate\_update\_after\_submit from true.
    - Set unreconcile\_doc.flags.ignore\_links from true.
    - Evaluate unreconcile\_doc.save(ignore\_permissions = true).
- Set unreconcile\_docs from Platform.db.get\_all(“Unreconcile Payment”, filters = mapping(“voucher\_no” → self.name)).
- For each x in unreconcile\_docs.
  - Set \_doc from Platform.get\_doc(“Unreconcile Payment”, x.name).
  - If \_doc.docstatus equals 1.
    - Evaluate \_doc.cancel().
  - Evaluate \_doc.delete().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L250) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L345)

<a id="op-90b9d867f1275e"></a>
### Accounts Controller.remove references in repost doctypes

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_remove_references_in_repost_record_types`

**Inputs** self.

**Record and data access** resolve a document from doc at 0 via get\_doc.

**State and service calls** call save on repost\_doc.

**Explicit failure paths** validation helper — translated “The following cancelled repost entries exist for &lt;b&gt;{0}&lt;/b&gt;:&lt;br&gt;&lt;br&gt;{1}&lt;br&gt;&lt;br&gt;Kindly delete these entries b …”.format(self.name, entries).

**Local steps**

- Set repost\_doctypes from list(“Repost Payment Ledger Items”, “Repost Accounting Ledger Items”).
- For each \_doctype in repost\_doctypes.
  - Set dt from Platform.qb.DocType(\_doctype).
  - Set cancelled\_entries from nested operand in the contract(nested operand in the contract).select(dt.parent, dt.parenttype).where(((nested operand in the contract.voucher\_type equals nested operand in the contract.doctype bitwise and ….
  - If cancelled\_entries.
    - Set entries from text in the contract.join(list of get\_link\_to\_form(d.parenttype, d.parent) for d drawn from cancelled\_entries).
      - Draw d from cancelled\_entries.
    - Call the validation error handler Platform.throw(translated “The following cancelled repost entries exist for &lt;b&gt;{0}&lt;/b&gt;:&lt;br&gt;&lt;br&gt;{1}&lt;br&gt;&lt;br&gt;Kindly delete these entries b …”.format(self.name, entries)).
  - Set rows from nested operand in the contract(nested operand in the contract).select(dt.name, dt.parent, dt.parenttype).where((dt.voucher\_type equals self.doctype bitwise and dt.voucher\_no equals self.name)).run(as\_dict = true).
  - If rows.
    - Set references\_map from Platform.\_dict().
    - For each x in rows.
      - Evaluate references\_map.setdefault(tuple(x.parenttype, x.parent), list()).append(x.name).
    - For each tuple(doc, rows) in references\_map.items().
      - Set repost\_doc from Platform.get\_doc(doc at 0, doc at 1).
      - For each row in rows.
        - If \_doctype equals “Repost Payment Ledger Items”.
          - Evaluate repost\_doc.remove(repost\_doc.get(“repost\_vouchers”, mapping(“name” → row)) at 0).
        - Otherwise.
          - Evaluate repost\_doc.remove(repost\_doc.get(“vouchers”, mapping(“name” → row)) at 0).
      - Set repost\_doc.flags.ignore\_validate\_update\_after\_submit from true.
      - Set repost\_doc.flags.ignore\_links from true.
      - Evaluate repost\_doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L996) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L344)

<a id="op-054fa7de16ba04"></a>
### Accounts Controller.remove advance payment ledger entries

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_remove_advance_payment_ledger_entries`

**Inputs** self.

**Local steps**

- Set adv from qb.DocType(“Advance Payment Ledger Entry”).
- Evaluate nested operand in the contract(nested operand in the contract).delete().where((nested operand in the contract.voucher\_type.eq(self.doctype) bitwise and nested operand in the contract.voucher\_no.eq(self.name))).run().
- If self.doctype belongs to self.get\_advance\_payment\_doctypes().
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where((nested operand in the contract.against\_voucher\_type.eq(self.doctype) bitwise and nested operand in the contract.against\_vouche ….run().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get advance payment doctypes](operations-006.md#op-26bd158ad36a78).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L2050) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L342)

<a id="op-69d857ec6025ed"></a>
### Accounts Controller.on trash

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_on_trash`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Cancelled transactions cannot be deleted when Immutable Ledger is enabled.”.

**Local steps**

- Bind dependencies delete\_exchange\_gain\_loss\_journal, is\_immutable\_ledger\_enabled.
- If (self.docstatus equals 2 and is\_immutable\_ledger\_enabled()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 2 → is\_immutable\_ledger\_enabled().
  - Call the validation error handler Platform.throw(translated “Cancelled transactions cannot be deleted when Immutable Ledger is enabled.”, title = translated “Immutable Ledger Enabled”).
- Evaluate self.\_remove\_references\_in\_repost\_doctypes().
- Evaluate self.\_remove\_references\_in\_unreconcile().
- Evaluate self.remove\_serial\_and\_batch\_bundle().
- If Platform.get\_single\_value(“Accounts Settings”, “delete\_linked\_ledger\_entries”).
  - Evaluate delete\_exchange\_gain\_loss\_journal(self).
  - Set ple from Platform.qb.DocType(“Payment Ledger Entry”).
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where(((nested operand in the contract.voucher\_type equals nested operand in the contract.doctype bitwise and nested operand in the c ….run().
  - Set gle from Platform.qb.DocType(“GL Entry”).
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where((gle.voucher\_type equals self.doctype bitwise and gle.voucher\_no equals self.name)).run().
  - Set sle from Platform.qb.DocType(“Stock Ledger Entry”).
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where((sle.voucher\_type equals self.doctype bitwise and sle.voucher\_no equals self.name)).run().
  - Evaluate self.\_remove\_advance\_payment\_ledger\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove references in repost doctypes](operations-001.md#op-90b9d867f1275e), [remove references in unreconcile](operations-001.md#op-bd851e3f24ff8b), [remove serial and batch bundle](operations-001.md#op-e4ed509dcb803d), [remove advance payment ledger entries](operations-001.md#op-054fa7de16ba04).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “delete\_linked\_ledger\_entries”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L337)

<a id="op-e4ed509dcb803d"></a>
### Accounts Controller.remove serial and batch bundle

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_remove_serial_and_batch_bundle`

**Inputs** self.

**Record and data access** read “Serial and Batch Bundle” via get\_all · read “Batch” via get\_all.

**State and service calls** request delete\_doc for “Serial and Batch Bundle” · request delete\_doc for “Batch”.

**Local steps**

- Set bundles from Platform.get\_all(“Serial and Batch Bundle”, filters = mapping(“voucher\_type” → self.doctype, “voucher\_no” → self.name, “docstatus” → tuple(“!=”, 1))).
- For each bundle in bundles.
  - Evaluate Platform.delete\_doc(“Serial and Batch Bundle”, bundle.name).
- Set batches from Platform.get\_all(“Batch”, filters = mapping(“reference\_doctype” → self.doctype, “reference\_name” → self.name)).
- For each row in batches.
  - Evaluate Platform.delete\_doc(“Batch”, row.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L3101) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L346)

<a id="op-dd4fbd870e699e"></a>
### Accounts Controller.validate company in accounting dimension

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_company_in_accounting_dimension`

**Inputs** self.

**Local steps**

- Set doc\_field from DocType(“DocField”).
- Set accounting\_dimension from DocType(“Accounting Dimension”).
- Set dimension\_list from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.document\_type).where(doc\_field.fieldname equals “company”).run( ….
- Set dimension\_list from sum(dimension\_list, list(“Project”, “Cost Center”)).
- Evaluate self.validate\_company(dimension\_list).
- For each child in (self.get\_all\_children() or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_all\_children() → list().
  - Evaluate self.validate\_company(dimension\_list, child).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate company](operations-002.md#op-99921e7b03a58e).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0366.json#L3443) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L369)
