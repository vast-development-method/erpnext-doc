# Accounting and settlement · operations 96

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Purchase register

<a id="op-4ade8433e08754"></a>
### Get in invoice payable debit

`operation_enterprise_binding_enterprise_accounts_report_purchase_register_purchase_register_get_in_invoice_payable_debit`

**Inputs** inv.

**Explicit results** debit.

**Local steps**

- Set debit from flt(inv.base\_write\_off\_amount).
- If inv.is\_paid.
  - Update debit using + flt(inv.base\_paid\_amount).
- Return debit.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1253)

<a id="op-765a74b0f6153c"></a>
### Get columns

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_columns`

**Inputs** invoice\_list, additional\_table\_columns, include\_payments = false.

**Explicit results** tuple(columns, accounts at 0, accounts at 2, accounts at 1).

**Local steps**

- Set columns from list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Voucher”, “fieldname” → “voucher\_no”, “fieldty ….
- If (additional\_table\_columns and not include\_payments).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in additional\_table\_columns → not include\_payments.
  - Update columns using + additional\_table\_columns.
- If not include\_payments.
  - Update columns using + list(mapping(“label” → translated “Supplier Group”, “fieldname” → “supplier\_group”, “fieldtype” → “Link”, “options” → “Supplier Group”, …), mapping(“label” → translated “Tax Id”, “fieldname” → “tax\_id”, “f ….
- Otherwise.
  - Update columns using + list(mapping(“fieldname” → “payable\_account”, “label” → translated “Payable Account”, “fieldtype” → “Link”, “options” → “Account”, …), mapping(“fieldname” → “debit”, “label” → translated “Debit”, “fieldtyp ….
- Set tuple(account\_columns, accounts) from get\_account\_columns(invoice\_list, include\_payments).
- Set columns from (((((columns + account\_columns at 0) + account\_columns at 1) + list(mapping(“label” → translated “Net Total”, “fieldname” → “net\_total”, “fieldtype” → “Currency”, “options” → “currency”, …))) + account\_col ….
- If not include\_payments.
  - Update columns using + list(mapping(“label” → translated “Grand Total”, “fieldname” → “grand\_total”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“label” → translated “Rounded Total”, “fieldname” → “rounded\_tota ….
- Update columns using + list(mapping(“label” → translated “Remarks”, “fieldname” → “remarks”, “fieldtype” → “Data”, “width” → 120)).
- Return tuple(columns, accounts at 0, accounts at 2, accounts at 1).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L865) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1207)

<a id="op-a98a6d0b7f4a36"></a>
### Get account columns

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_account_columns`

**Inputs** invoice\_list, include\_payments.

**Explicit results** tuple(columns, accounts).

**Local steps**

- Set expense\_accounts from list().
- Set tax\_accounts from list().
- Set unrealized\_profit\_loss\_accounts from list().
- Set expense\_columns from list().
- Set tax\_columns from list().
- Set unrealized\_profit\_loss\_account\_columns from list().
- If invoice\_list.
  - Set expense\_accounts from Platform.db.sql\_list((query text (SELECT, Purchase Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(list of inv.name for inv drawn from invoice\_list)).
    - Draw inv from invoice\_list.
  - Set purchase\_taxes\_query from get\_taxes\_query(invoice\_list, “Purchase Taxes and Charges”, “Purchase Invoice”).
  - Set purchase\_tax\_accounts from purchase\_taxes\_query.run(as\_dict = true, pluck = “account\_head”).
  - Set tax\_accounts from purchase\_tax\_accounts.
  - If include\_payments.
    - Set advance\_taxes\_query from get\_taxes\_query(invoice\_list, “Advance Taxes and Charges”, “Payment Entry”).
    - Set advance\_tax\_accounts from advance\_taxes\_query.run(as\_dict = true, pluck = “account\_head”).
    - Set tax\_accounts from set((tax\_accounts + advance\_tax\_accounts)).
  - Set unrealized\_profit\_loss\_accounts from Platform.db.sql\_list((query text (SELECT, Purchase Invoice) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list)).
    - Draw inv from invoice\_list.
- For each account in expense\_accounts.
  - Evaluate expense\_columns.append(mapping(“label” → account, “fieldname” → Platform.scrub(account), “fieldtype” → “Currency”, “options” → “currency”, …)).
- For each account in tax\_accounts.
  - If account does not belong to expense\_accounts.
    - Evaluate tax\_columns.append(mapping(“label” → account, “fieldname” → Platform.scrub(account), “fieldtype” → “Currency”, “options” → “currency”, …)).
- For each account in unrealized\_profit\_loss\_accounts.
  - Evaluate unrealized\_profit\_loss\_account\_columns.append(mapping(“label” → account, “fieldname” → Platform.scrub((account + “\_unrealized”)), “fieldtype” → “Currency”, “options” → “currency”, …)).
- Set columns from list(expense\_columns, unrealized\_profit\_loss\_account\_columns, tax\_columns).
- Set accounts from list(expense\_accounts, unrealized\_profit\_loss\_accounts, tax\_accounts).
- Return tuple(columns, accounts).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L863) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1205)

<a id="op-612b1f99f526fb"></a>
### Get invoices

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_invoices`

**Inputs** filters, additional\_query\_columns.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set pi from Platform.qb.DocType(“Purchase Invoice”).
- Set query from nested operand in the contract.qb.from\_(pi).select(ConstantColumn(“Purchase Invoice”).as\_(“doctype”), pi.name, pi.posting\_date, pi.credit\_to, …).where(pi.docstatus equals 1).
- If additional\_query\_columns.
  - For each col in additional\_query\_columns.
    - Set query from query.select(col).
- If filters.get(“supplier”).
  - Set query from query.where(pi.supplier equals filters.supplier).
- If filters.get(“supplier\_group”).
  - Set supplier from Platform.qb.DocType(“Supplier”).
  - Set query from query.where(pi.supplier.isin(nested operand in the contract(nested operand in the contract).select(supplier.name).where(supplier.supplier\_group.isin(get\_with\_descendants(“Supplier Group”, filters.supplier\_group))))).
- Set query from get\_conditions(filters, query, “Purchase Invoice”).
- Set query from apply\_common\_conditions(filters, query, doctype = “Purchase Invoice”, child\_doctype = “Purchase Invoice Item”).
- If filters.get(“include\_payments”).
  - Set party\_account from get\_party\_account(“Supplier”, filters.get(“supplier”), filters.get(“company”), include\_advance = true).
  - Set query from query.where(pi.credit\_to.isin(party\_account)).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(“Purchase Invoice”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set query from query.orderby(“posting\_date”, order = Order.desc).
- Set query from query.orderby(“name”, order = Order.desc).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1213)

<a id="op-478659bd20eebe"></a>
### Get conditions

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_conditions`

**Inputs** filters, query, doctype.

**Explicit results** query.

**Local steps**

- Set parent\_doc from Platform.qb.DocType(doctype).
- If filters.get(“mode\_of\_payment”).
  - Set query from query.where(parent\_doc.mode\_of\_payment equals filters.mode\_of\_payment).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0273.json#L5148) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L866) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1208)

<a id="op-3faa8de2638365"></a>
### Get payments

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_payments`

**Inputs** filters.

**Explicit results** (payment\_entries + journal\_entries).

**Local steps**

- Set args from Platform.\_dict(account = “credit\_to”, party = “supplier”, party\_name = “supplier\_name”, party\_account = get\_party\_account(“Supplier”, filters.supplier, filters.company, include\_advance = true)).
- Set payment\_entries from get\_payment\_entries(filters, args).
- Set journal\_entries from get\_journal\_entries(filters, args).
- Return (payment\_entries + journal\_entries).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1214)

<a id="op-1a29bac75ee723"></a>
### Get invoice expense map

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_invoice_expense_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** invoice\_expense\_map.

**Local steps**

- Set expense\_details from Platform.db.sql((query text (SELECT, Purchase Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set invoice\_expense\_map from mapping().
- For each d in expense\_details.
  - Evaluate invoice\_expense\_map.setdefault(d.parent, Platform.\_dict()).setdefault(d.expense\_account, list()).
  - Set invoice\_expense\_map at d.parent at d.expense\_account from flt(d.amount).
- Return invoice\_expense\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L868) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1210)

<a id="op-eaaeb7298522fb"></a>
### Get internal invoice map

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_internal_invoice_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** internal\_invoice\_map.

**Local steps**

- Set unrealized\_amount\_details from Platform.db.sql((query text (SELECT, Purchase Invoice) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set internal\_invoice\_map from mapping().
- For each d in unrealized\_amount\_details.
  - If d.unrealized\_profit\_loss\_account.
    - Evaluate internal\_invoice\_map.setdefault(tuple(d.name, d.unrealized\_profit\_loss\_account), d.amount).
- Return internal\_invoice\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L867) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1209)

<a id="op-6e80b67ae720fa"></a>
### Get invoice tax map

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_invoice_tax_map`

**Inputs** invoice\_list, invoice\_expense\_map, expense\_accounts, include\_payments = false.

**State and service calls** execute a supplied database query.

**Explicit results** tuple(invoice\_expense\_map, invoice\_tax\_map).

**Local steps**

- Set tax\_details from Platform.db.sql((query text (SELECT, Purchase Taxes and Charges) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- If include\_payments.
  - Update tax\_details using + get\_advance\_taxes\_and\_charges(invoice\_list).
- Set invoice\_tax\_map from mapping().
- For each d in tax\_details.
  - If d.account\_head belongs to expense\_accounts.
    - If d.account\_head belongs to invoice\_expense\_map at d.parent.
      - Update invoice\_expense\_map at d.parent at d.account\_head using + flt(d.tax\_amount).
    - Otherwise.
      - Set invoice\_expense\_map at d.parent at d.account\_head from flt(d.tax\_amount).
  - Otherwise.
    - Evaluate invoice\_tax\_map.setdefault(d.parent, Platform.\_dict()).setdefault(d.account\_head, list()).
    - Set invoice\_tax\_map at d.parent at d.account\_head from flt(d.tax\_amount).
- Return tuple(invoice\_expense\_map, invoice\_tax\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L870) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1212)

<a id="op-8630186461b34d"></a>
### Get invoice po pr map

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_invoice_purchase_order_purchase_receipt_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** invoice\_po\_pr\_map.

**Local steps**

- Set pi\_items from Platform.db.sql((query text (SELECT, Purchase Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set invoice\_po\_pr\_map from mapping().
- For each d in pi\_items.
  - If d.purchase\_order.
    - Evaluate invoice\_po\_pr\_map.setdefault(d.parent, nested operand in the contract.\_dict()).setdefault(“purchase\_order”, list()).append(d.purchase\_order).
  - Set pr\_list from no value.
  - If d.purchase\_receipt.
    - Set pr\_list from list(d.purchase\_receipt).
  - Otherwise.
    - If d.po\_detail.
      - Set pr\_list from Platform.db.sql\_list(query text (SELECT, Purchase Receipt Item), d.po\_detail).
  - If pr\_list.
    - Evaluate invoice\_po\_pr\_map.setdefault(d.parent, Platform.\_dict()).setdefault(“purchase\_receipt”, pr\_list).
  - If d.project.
    - Evaluate invoice\_po\_pr\_map.setdefault(d.parent, nested operand in the contract.\_dict()).setdefault(“project”, list()).append(d.project).
- Return invoice\_po\_pr\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L869) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1211)

<a id="op-134f5c6ace05ba"></a>
### Get account details

`operation_enterprise_accounts_report_purchase_register_business_behavior_get_account_details`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** account\_map.

**Local steps**

- Set account\_map from mapping().
- Set accounts from list(set(list of inv.credit\_to for inv drawn from invoice\_list)).
  - Draw inv from invoice\_list.
- For each acc in Platform.db.sql((query text (SELECT, Account) modulo or format “, ”.join((list(“%s”) × len(accounts)))), tuple(accounts), as\_dict = 1).
  - Set account\_map at acc.name from acc.parent\_account.
- Return account\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L864) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1206)

## Record · Purchase taxes and charges template

[Record definition](../../../../data/record-types/purchase_taxes_and_charges_template.json)

<a id="op-7b0cc5c9bd4a6d"></a>
### Purchase Taxesand Charges Template.validate

`operation_enterprise_accounts_record_definitions_purchase_taxes_and_charges_template_business_behavior_purchase_taxesand_charges_template_validate`

**Inputs** self.

**Local steps**

- Evaluate valdiate\_taxes\_and\_charges\_template(self).
- Evaluate validate\_deduct\_with\_valuation\_category(self.taxes).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1063)

<a id="op-be095018e23e5d"></a>
### Purchase Taxesand Charges Template.autoname

`operation_enterprise_accounts_record_definitions_purchase_taxes_and_charges_template_business_behavior_purchase_taxesand_charges_template_autoname`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If (self.company and self.title).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → self.title.
  - Set abbr from Platform.get\_cached\_value(“Company”, self.company, “abbr”).
  - Set self.name from formatted text {self.title} - {abbr}.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “abbr”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L4385) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1062)

<a id="op-d1d62da777a0ad"></a>
### Get data

`operation_enterprise_accounts_record_definitions_purchase_taxes_and_charges_template_purchase_taxes_and_charges_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “taxes\_and\_charges”, “non\_standard\_fieldnames” → mapping(“Tax Rule” → “purchase\_tax\_template”), “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Purc ….

**Local steps**

- Return mapping(“fieldname” → “taxes\_and\_charges”, “non\_standard\_fieldnames” → mapping(“Tax Rule” → “purchase\_tax\_template”), “transactions” → list(mapping(“label” → translated “Transactions”, “items” → list(“Purc ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L4545) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1064)

## Report · Received items to be billed

<a id="op-2a66d0260fd751"></a>
### Execute

`operation_enterprise_accounts_report_received_items_to_be_billed_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set columns from get\_column().
- Set args from get\_args().
- Set data from get\_ordered\_to\_be\_billed\_data(args, filters).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0274.json#L6109) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L882) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1222)

<a id="op-95123bfed974b5"></a>
### Get column

`operation_enterprise_accounts_report_received_items_to_be_billed_business_behavior_get_column`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Purchase Receipt”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Purchase Receipt”, …), mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype”  ….

**Local steps**

- Return list(mapping(“label” → translated “Purchase Receipt”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Purchase Receipt”, …), mapping(“label” → translated “Date”, “fieldname” → “date”, “fieldtype”  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0275.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1224)

<a id="op-7c004ba157416a"></a>
### Get args

`operation_enterprise_accounts_report_received_items_to_be_billed_business_behavior_get_arguments`

**Inputs** no declared parameters.

**Explicit results** mapping(“doctype” → “Purchase Receipt”, “party” → “supplier”, “date” → “posting\_date”, “order” → “name”, …).

**Local steps**

- Return mapping(“doctype” → “Purchase Receipt”, “party” → “supplier”, “date” → “posting\_date”, “order” → “name”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0275.json#L1255) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1223)

## Record · Repost accounting ledger

[Record definition](../../../../data/record-types/repost_accounting_ledger.json)

<a id="op-bf0ae3ab4873e1"></a>
### Repost Accounting Ledger.initialize

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.\_allowed\_types from get\_allowed\_types\_from\_settings().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L4790) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L943) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1077)

<a id="op-d43a12ee0b03b5"></a>
### Repost Accounting Ledger.validate

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_vouchers().
- Evaluate self.validate\_repost\_preconditions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate vouchers](operations-096.md#op-ace8d8b4bcc265), [validate repost preconditions](operations-096.md#op-b47657cb8385e0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L4900) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1083)

<a id="op-b47657cb8385e0"></a>
### Repost Accounting Ledger.validate repost preconditions

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate_repost_preconditions`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_for\_closed\_fiscal\_year().
- Evaluate self.validate\_for\_deferred\_accounting().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for closed fiscal year](operations-096.md#op-c7a674baf72d97), [validate for deferred accounting](operations-096.md#op-946f1f9a4bbb17).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L4971) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1087)

<a id="op-946f1f9a4bbb17"></a>
### Repost Accounting Ledger.validate for deferred accounting

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate_for_deferred_accounting`

**Inputs** self.

**Local steps**

- Set sales\_docs from list of x.voucher\_no for x drawn from self.vouchers where x.voucher\_type equals “Sales Invoice”.
  - Draw x from self.vouchers, keep a combination only if (x.voucher\_type equals “Sales Invoice”).
- Set purchase\_docs from list of x.voucher\_no for x drawn from self.vouchers where x.voucher\_type equals “Purchase Invoice”.
  - Draw x from self.vouchers, keep a combination only if (x.voucher\_type equals “Purchase Invoice”).
- Evaluate validate\_docs\_for\_deferred\_accounting(sales\_docs, purchase\_docs).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L5042) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1085)

<a id="op-c7a674baf72d97"></a>
### Repost Accounting Ledger.validate for closed fiscal year

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate_for_closed_fiscal_year`

**Inputs** self.

**Record and data access** read “Period Closing Voucher” via get\_all · read vtype via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot Resubmit Ledger entries for vouchers in Closed fiscal year.”.

**Local steps**

- If self.vouchers.
  - Set latest\_pcv from (Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“company” → self.company, “docstatus” → 1), order\_by = “period\_end\_date desc”, pluck = “period\_end\_date”, limit = 1) or no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“company” → self.company, “docstatus” → 1), order\_by = “period\_end\_date desc”, pluck = “period\_end\_date”, limit = 1) → no value.
  - If not latest\_pcv.
    - Return no value.
  - For each vtype in self.\_allowed\_types.
    - If names bound to list of x.voucher\_no for x drawn from self.vouchers where x.voucher\_type equals vtype.
      - Draw x from self.vouchers, keep a combination only if (x.voucher\_type equals vtype).
      - Set latest\_voucher from Platform.db.get\_all(vtype, filters = mapping(“name” → list(“in”, names)), pluck = “posting\_date”, order\_by = “posting\_date desc”, limit = 1) at 0.
      - If (latest\_voucher and latest\_pcv at 0 ≥ latest\_voucher).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in latest\_voucher → latest\_pcv at 0 ≥ latest\_voucher.
        - Call the validation error handler Platform.throw(translated “Cannot Resubmit Ledger entries for vouchers in Closed fiscal year.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L5228) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1084)

<a id="op-ace8d8b4bcc265"></a>
### Repost Accounting Ledger.validate vouchers

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate_vouchers`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Add atleast one voucher to repost.” · validation helper — translated “Cannot repost more than {0} vouchers at once. Split them into multiple documents.”.format(MAX\_VOUCHERS\_PER\_REPOST).

**Local steps**

- If not self.vouchers.
  - Call the validation error handler Platform.throw(translated “Add atleast one voucher to repost.”).
- If len(self.vouchers) &gt; MAX\_VOUCHERS\_PER\_REPOST.
  - Call the validation error handler Platform.throw(translated “Cannot repost more than {0} vouchers at once. Split them into multiple documents.”.format(MAX\_VOUCHERS\_PER\_REPOST)).
- Evaluate validate\_docs\_for\_voucher\_types(list of x.voucher\_type for x drawn from self.vouchers).
  - Draw x from self.vouchers.
- Evaluate self.validate\_no\_duplicate\_vouchers().
- Evaluate self.validate\_vouchers\_are\_submitted().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate no duplicate vouchers](operations-096.md#op-d715baea04e46e), [validate vouchers are submitted](operations-097.md#op-d293cb7f2f7552).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L5688) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1088)

<a id="op-d715baea04e46e"></a>
### Repost Accounting Ledger.validate no duplicate vouchers

`operation_enterprise_accounts_record_definitions_repost_accounting_ledger_business_behavior_repost_accounting_ledger_validate_number_duplicate_vouchers`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Duplicate vouchers found. Remove the duplicate vouchers to continue to repost.”.

**Local steps**

- Set vouchers from list of tuple(x.voucher\_type, x.voucher\_no) for x drawn from self.vouchers.
  - Draw x from self.vouchers.
- If len(vouchers) differs from len(set(vouchers)).
  - Call the validation error handler Platform.throw(translated “Duplicate vouchers found. Remove the duplicate vouchers to continue to repost.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0160.json#L5955) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1086)
