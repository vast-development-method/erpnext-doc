# Accounting and settlement · operations 105

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-b21406393b0e48"></a>
### Create invoice discounting

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_create_invoice_discounting`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Sales Invoice” via get\_doc.

**State and service calls** request new\_doc for “Invoice Discounting”.

**Explicit results** invoice\_discounting.

**Local steps**

- Set invoice from Platform.get\_doc(“Sales Invoice”, source\_name).
- Set invoice\_discounting from Platform.new\_doc(“Invoice Discounting”).
- Set invoice\_discounting.company from invoice.company.
- Evaluate invoice\_discounting.append(“invoices”, mapping(“sales\_invoice” → source\_name, “customer” → invoice.customer, “posting\_date” → invoice.posting\_date, “outstanding\_amount” → invoice.outstanding\_amount)).
- Return invoice\_discounting.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L974)

<a id="op-bdc802a1c03295"></a>
### Update multi mode option

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_multi_mode_option`

**Inputs** doc, pos\_profile.

**State and service calls** toast with translated “Payment methods refreshed. Please review before proceeding.”.

**Explicit failure paths** validation helper — msg.format(“, ”.join(invalid\_modes)).

**Local steps**

- Bind local operation append\_payment for subsequent calls.
- Set mop\_refetched from (bool(doc.payments) and not doc.get(“is\_created\_using\_pos”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(doc.payments) → not doc.get(“is\_created\_using\_pos”).
- Evaluate doc.set(“payments”, list()).
- Set invalid\_modes from list().
- Set mode\_of\_payments from list of d.mode\_of\_payment for d drawn from pos\_profile.get(“payments”).
  - Draw d from pos\_profile.get(“payments”).
- Set mode\_of\_payments\_info from get\_mode\_of\_payments\_info(mode\_of\_payments, doc.company).
- For each row in pos\_profile.get(“payments”).
  - Set payment\_mode from mode\_of\_payments\_info.get(row.mode\_of\_payment).
  - If not payment\_mode.
    - Evaluate invalid\_modes.append(get\_link\_to\_form(“Mode of Payment”, row.mode\_of\_payment)).
    - Continue with the next iteration or loop test.
  - Set payment\_mode.default from row.default.
  - Evaluate append\_payment(payment\_mode).
- If invalid\_modes.
  - If invalid\_modes equals 1.
    - Set msg from translated “Please set default Cash or Bank account in Mode of Payment {}”.
  - Otherwise.
    - Set msg from translated “Please set default Cash or Bank account in Mode of Payments {}”.
  - Call the validation error handler Platform.throw(msg.format(“, ”.join(invalid\_modes)), title = translated “Missing Account”).
- If mop\_refetched.
  - Evaluate Platform.toast(translated “Payment methods refreshed. Please review before proceeding.”, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1067)

<a id="op-41e7c7679e3039"></a>
### Update multi mode option.append payment

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_update_multi_mode_option_append_payment`

**Inputs** payment\_mode.

**Local steps**

- Set payment from doc.append(“payments”, mapping()).
- Set payment.default from payment\_mode.default.
- Set payment.mode\_of\_payment from payment\_mode.mop.
- Set payment.account from payment\_mode.default\_account.
- Set payment.type from payment\_mode.type.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1068)

<a id="op-faafb230dd06e0"></a>
### Get all mode of payments

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_all_mode_of_payments`

**Inputs** doc.

**Explicit results** query.run(as\_dict = 1).

**Local steps**

- Set ModeOfPaymentAccount from Platform.qb.DocType(“Mode of Payment Account”).
- Set ModeOfPayment from Platform.qb.DocType(“Mode of Payment”).
- Set query from nested operand in the contract(nested operand in the contract).select(ModeOfPaymentAccount.default\_account, ModeOfPaymentAccount.parent, nested operand in the contract.as\_(“type”)).where(ModeOfPaymentAccou ….
- Return query.run(as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L975)

<a id="op-3547172e493495"></a>
### Get mode of payments info

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_mode_of_payments_info`

**Inputs** mode\_of\_payments, company.

**Record and data access** execute query text (SELECT, Mode of Payment Account).

**Explicit results** mapping of row.get(“mop”) → row for row drawn from data.

**Local steps**

- Set data from Platform.db.sql(query text (SELECT, Mode of Payment Account), tuple(company, mode\_of\_payments), as\_dict = 1).
- Return mapping of row.get(“mop”) → row for row drawn from data.
  - Draw row from data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L983)

<a id="op-e0f5b62e959b90"></a>
### Get mode of payment info

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_mode_of_payment_info`

**Inputs** mode\_of\_payment, company.

**Record and data access** execute query text (SELECT, Mode of Payment Account).

**Explicit results** Platform.db.sql(query text (SELECT, Mode of Payment Account), tuple(company, mode\_of\_payment), as\_dict = 1).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Mode of Payment Account), tuple(company, mode\_of\_payment), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L982)

<a id="op-3229b5e8521945"></a>
### Create dunning

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_create_dunning`

**Inputs** source\_name, target\_doc = no value, args = no value, ignore\_permissions = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_mapped\_doc(from\_doctype = “Sales Invoice”, from\_docname = source\_name, target\_doc = target\_doc, table\_maps = mapping(“Sales Invoice” → mapping(“doctype” → “Dunning”, “field\_map” → mapping(“customer\_add ….

**Local steps**

- If isinstance(args, bool).
  - Set ignore\_permissions from args.
  - Set args from no value.
- Set args from (Platform.parse\_json(args) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(args) → mapping().
- Bind dependencies get\_mapped\_doc.
- Bind local operation postprocess\_dunning for subsequent calls.
- Return get\_mapped\_doc(from\_doctype = “Sales Invoice”, from\_docname = source\_name, target\_doc = target\_doc, table\_maps = mapping(“Sales Invoice” → mapping(“doctype” → “Dunning”, “field\_map” → mapping(“customer\_add ….

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L972)

<a id="op-8eff2d4f6a092d"></a>
### Create dunning.postprocess dunning

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_create_dunning_postprocess_dunning`

**Inputs** source, target.

**Record and data access** read “Dunning Type” via exists · resolve a document from “Dunning Type” via get\_doc.

**Explicit failure paths** validation helper — translated “There are no overdue payments to include in this Dunning.”.

**Local steps**

- Set dunning\_type from Platform.db.exists(“Dunning Type”, mapping(“is\_default” → 1, “company” → source.company)).
- If dunning\_type.
  - Set dunning\_type from Platform.get\_doc(“Dunning Type”, dunning\_type).
  - Set target.dunning\_type from dunning\_type.name.
  - Set target.rate\_of\_interest from dunning\_type.rate\_of\_interest.
  - Set target.dunning\_fee from (flt(dunning\_type.dunning\_fee) ÷ target.conversion\_rate).
  - Set target.income\_account from dunning\_type.income\_account.
  - Set target.cost\_center from dunning\_type.cost\_center.
  - Set target.language from source.language.
- If source.payment\_schedule.
  - Set outstanding from get\_payment\_schedule\_outstanding(source, source.payment\_schedule).
  - For each row in target.overdue\_payments at slice no value to no value.
    - If (row.sales\_invoice equals source.name and row.payment\_schedule belongs to outstanding).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.sales\_invoice equals source.name → row.payment\_schedule belongs to outstanding.
      - Set row.outstanding from outstanding at row.payment\_schedule.
      - If flt(row.outstanding, row.precision(“outstanding”)) ≤ 0.
        - Evaluate target.remove(row).
- If (source.is\_opening equals “Yes” and not source.payment\_schedule and source.due\_date and getdate(source.due\_date) &lt; getdate(target.posting\_date) and flt(source.outstanding\_amount) &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in source.is\_opening equals “Yes” → not source.payment\_schedule → source.due\_date → getdate(source.due\_date) &lt; getdate(target.posting\_date) → flt(source.outstanding\_amount) &gt; 0.
  - Evaluate target.append(“overdue\_payments”, mapping(“sales\_invoice” → source.name, “due\_date” → source.due\_date, “outstanding” → get\_invoice\_outstanding(source))).
- If not target.overdue\_payments.
  - Call the validation error handler Platform.throw(translated “There are no overdue payments to include in this Dunning.”).
- Evaluate target.validate().
- If dunning\_type.
  - Evaluate target.get\_dunning\_letter\_text().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L973)

<a id="op-e98c8997771dd5"></a>
### Check if return invoice linked with payment entry

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_check_if_return_invoice_linked_with_payment_entry`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value · resolve a document from “Payment Entry” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If not Platform.get\_single\_value(“Accounts Settings”, “unlink\_payment\_on\_cancellation\_of\_invoice”).
  - Return no value.
- Set payment\_entries from list().
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Set invoice from self.return\_against.
- Otherwise.
  - Set invoice from self.name.
- Set payment\_entries from Platform.db.sql\_list(query text (SELECT, Payment Entry), invoice).
- Set links\_to\_pe from list().
- If payment\_entries.
  - For each payment in payment\_entries.
    - Set payment\_entry from Platform.get\_doc(“Payment Entry”, payment).
    - If len(payment\_entry.references) &gt; 1.
      - Evaluate links\_to\_pe.append(payment\_entry.name).
  - If links\_to\_pe.
    - Set payment\_entries\_link from list of get\_link\_to\_form(“Payment Entry”, name, label = name) for name drawn from links\_to\_pe.
      - Draw name from links\_to\_pe.
    - Set message from translated “Please cancel and amend the Payment Entry”.
    - Update message using + ((one space + “, ”.join(payment\_entries\_link)) + one space).
    - Update message using + translated “to unallocate the amount of this Return Invoice before cancelling it.”.
    - Call the validation error handler Platform.throw(message).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “unlink\_payment\_on\_cancellation\_of\_invoice”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1137)

<a id="op-0b910dc24e585e"></a>
### Get stored asset disposal values

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_get_stored_asset_disposal_values`

**Inputs** item.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“value\_after\_depreciation” → item.asset\_value\_after\_depreciation, “gross\_asset\_value” → item.asset\_gross\_value).

**Local steps**

- If not flt(item.asset\_gross\_value).
  - Return no value.
- Return mapping(“value\_after\_depreciation” → item.asset\_value\_after\_depreciation, “gross\_asset\_value” → item.asset\_gross\_value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L987)

<a id="op-a1f1f573542f04"></a>
### Get data

`operation_enterprise_accounts_record_definitions_sales_invoice_sales_invoice_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “sales\_invoice”, “non\_standard\_fieldnames” → mapping(“Delivery Note” → “against\_sales\_invoice”, “Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Reques ….

**Local steps**

- Return mapping(“fieldname” → “sales\_invoice”, “non\_standard\_fieldnames” → mapping(“Delivery Note” → “against\_sales\_invoice”, “Journal Entry” → “reference\_name”, “Payment Entry” → “reference\_name”, “Payment Reques ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L4624) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L14)

## Record · Sales invoice item

[Record definition](../../../../data/record-types/sales_invoice_item.json)

<a id="op-8f164cdb073cf9"></a>
### Sales Invoice Item.validate cost center

`operation_enterprise_accounts_record_definitions_sales_invoice_item_business_behavior_sales_invoice_item_validate_cost_center`

**Inputs** self, company.

**Record and data access** read “Cost Center” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Cost Center {1} does not belong to company {2}”.format(Platform.bold(self.idx), Platform.bold(self.cost\_center), Platform.bold(company)).

**Local steps**

- Set cost\_center\_company from Platform.get\_cached\_value(“Cost Center”, self.cost\_center, “company”).
- If cost\_center\_company differs from company.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Cost Center {1} does not belong to company {2}”.format(Platform.bold(self.idx), Platform.bold(self.cost\_center), Platform.bold(company))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Cost Center”, self.cost\_center, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0186.json#L6894) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1071) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L13)

<a id="op-4acd4b04034045"></a>
### Sales Invoice Item.set actual qty

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_item_sales_invoice_item_salesinvoiceitem_set_actual_qty`

**Inputs** self.

**Record and data access** read “Bin” via get\_value.

**Local steps**

- If (self.item\_code and self.warehouse).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → self.warehouse.
  - Set self.actual\_qty from (Platform.db.get\_value(“Bin”, mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse), “actual\_qty”) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Bin”, mapping(“item\_code” → self.item\_code, “warehouse” → self.warehouse), “actual\_qty”) → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L970)

<a id="op-45bb43acf264b7"></a>
### Sales Invoice Item.set income account for fixed asset

`operation_enterprise_accounts_record_definitions_sales_invoice_item_business_behavior_sales_invoice_item_set_income_account_for_fixed_asset`

**Inputs** self, company.

**Explicit results** no value.

**Local steps**

- If not self.is\_fixed\_asset.
  - Return no value.
- Set tuple(disposal\_account, depreciation\_cost\_center) from \_get\_disposal\_account\_and\_cost\_center(company).
- Set self.income\_account from disposal\_account.
- If not self.cost\_center.
  - Set self.cost\_center from depreciation\_cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L12)

## Report · Sales invoice trends

<a id="op-042a66c554c806"></a>
### Execute

`operation_enterprise_accounts_report_sales_invoice_trends_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(conditions at “columns”, data).

**Local steps**

- If not filters.
  - Set filters from mapping().
- Set data from list().
- Set conditions from get\_columns(filters, “Sales Invoice”).
- Set data from get\_data(filters, conditions).
- Return tuple(conditions at “columns”, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0275.json#L3017) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L891) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1231)

## Report · Sales partners commission

<a id="op-a6c5e563edaea0"></a>
### Execute

`operation_enterprise_binding_enterprise_accounts_report_sales_partners_commission_sales_partners_commission_execute`

**Inputs** filters = no value.

**Declared result** tuple at tuple(list, list).

**Explicit results** tuple(get\_columns(), get\_data(filters)).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Return tuple(get\_columns(), get\_data(filters)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L192) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L619) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1257)

<a id="op-494b23d0e1e5bc"></a>
### Get data

`operation_enterprise_binding_enterprise_accounts_report_sales_partners_commission_sales_partners_commission_get_data`

**Inputs** filters.

**Declared result** list at dict.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** list of get\_row(partner, amounts, currency) for tuple(partner, amounts) drawn from totals.items().

**Local steps**

- Set totals from mapping().
- For each doctype in tuple(“Sales Invoice”, “POS Invoice”).
  - If not Platform.has\_permission(doctype, “read”).
    - Continue with the next iteration or loop test.
  - For each row in get\_partner\_totals(doctype, filters).
    - Set partner from totals.setdefault(row.sales\_partner, dict.fromkeys(AMOUNT\_FIELDS, 0.0)).
    - For each field in AMOUNT\_FIELDS.
      - Update partner at field using + flt(row at field).
- Set currency from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Return list of get\_row(partner, amounts, currency) for tuple(partner, amounts) drawn from totals.items().
  - Draw tuple(partner, amounts) from totals.items().

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”) · configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L194) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1259)

<a id="op-57bf6aa04ca765"></a>
### Get partner totals

`operation_enterprise_binding_enterprise_accounts_report_sales_partners_commission_sales_partners_commission_get_partner_totals`

**Inputs** doctype, filters.

**Declared result** list at Platform.\_dict.

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, filters = get\_invoice\_filters(filters), fields = list(“sales\_partner”, mapping(“SUM” → “base\_net\_total”, “as” → “invoiced\_amount”), mapping(“SUM” → “amount\_eligible\_for\_commissio ….

**Local steps**

- Return Platform.get\_list(doctype, filters = get\_invoice\_filters(filters), fields = list(“sales\_partner”, mapping(“SUM” → “base\_net\_total”, “as” → “invoiced\_amount”), mapping(“SUM” → “amount\_eligible\_for\_commissio ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L196) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L623) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1261)

<a id="op-804b1f6b13a2d5"></a>
### Get invoice filters

`operation_enterprise_binding_enterprise_accounts_report_sales_partners_commission_sales_partners_commission_get_invoice_filters`

**Inputs** filters.

**Declared result** dict.

**Explicit results** invoice\_filters.

**Local steps**

- Set invoice\_filters from mapping(“docstatus” → 1, “company” → filters.company, “total\_commission” → list(“!=”, 0)).
- If (filters.from\_date and filters.to\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.from\_date → filters.to\_date.
  - Set invoice\_filters at “posting\_date” from list(“between”, list(filters.from\_date, filters.to\_date)).
- Otherwise.
  - If filters.from\_date.
    - Set invoice\_filters at “posting\_date” from list(“&gt;=”, filters.from\_date).
  - Otherwise.
    - If filters.to\_date.
      - Set invoice\_filters at “posting\_date” from list(“&lt;=”, filters.to\_date).
- Return invoice\_filters.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L195) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1260)

<a id="op-9ec8e1de220242"></a>
### Get row

`operation_enterprise_binding_enterprise_accounts_report_sales_partners_commission_sales_partners_commission_get_row`

**Inputs** partner, amounts, currency.

**Declared result** dict.

**Explicit results** mapping(“sales\_partner” → partner, expand amounts, “average\_commission\_rate” → average\_rate, “currency” → currency).

**Local steps**

- Set eligible from amounts at “amount\_eligible\_for\_commission”.
- Set average\_rate from ((amounts at “total\_commission” × 100) ÷ eligible) when eligible, otherwise no value.
  - Value choice on eligible — true gives ((amounts at “total\_commission” × 100) ÷ eligible), false gives no value.
- Return mapping(“sales\_partner” → partner, expand amounts, “average\_commission\_rate” → average\_rate, “currency” → currency).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L197) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L624) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1262)

<a id="op-e7143dd3ab9579"></a>
### Get columns

`operation_enterprise_binding_enterprise_accounts_report_sales_partners_commission_sales_partners_commission_get_columns`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Explicit results** list(mapping(“label” → translated “Sales Partner”, “fieldname” → “sales\_partner”, “fieldtype” → “Link”, “options” → “Sales Partner”, …), mapping(“label” → translated “Invoiced Amount (Excl. Tax)”, “fieldna ….

**Local steps**

- Return list(mapping(“label” → translated “Sales Partner”, “fieldname” → “sales\_partner”, “fieldtype” → “Link”, “options” → “Sales Partner”, …), mapping(“label” → translated “Invoiced Amount (Excl. Tax)”, “fieldna ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L620) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1258)

## Report · Sales payment summary

<a id="op-8ca1072140fbf6"></a>
### Execute

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(columns, data) from tuple(list(), list()).
- Set columns from get\_columns(filters).
- Set data from get\_pos\_sales\_payment\_data(filters) when filters.get(“is\_pos”), otherwise get\_sales\_payment\_data(filters, columns).
  - Value choice on filters.get(“is\_pos”) — true gives get\_pos\_sales\_payment\_data(filters), false gives get\_sales\_payment\_data(filters, columns).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L4)

<a id="op-1b3ab7c6aba724"></a>
### Get pos columns

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_point_of_sale_columns`

**Inputs** no declared parameters.

**Explicit results** list((translated “Date” + “:Date:80”), (translated “Owner” + “:Data:200”), (translated “Payment Mode” + “:Data:240”), (translated “Sales and Returns” + “:Currency/currency:120”), …).

**Local steps**

- Return list((translated “Date” + “:Date:80”), (translated “Owner” + “:Data:200”), (translated “Payment Mode” + “:Data:240”), (translated “Sales and Returns” + “:Currency/currency:120”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0275.json#L6503) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L9)

<a id="op-1a274a2f0c46e5"></a>
### Get columns

`operation_enterprise_accounts_report_sales_payment_summary_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** get\_pos\_columns() · list((translated “Date” + “:Date:80”), (translated “Owner” + “:Data:200”), (translated “Payment Mode” + “:Data:240”), (translated “Sales and Returns” + “:Currency/currency:120”), …).

**Local steps**

- If filters.get(“is\_pos”).
  - Return get\_pos\_columns().
- Otherwise.
  - Return list((translated “Date” + “:Date:80”), (translated “Owner” + “:Data:200”), (translated “Payment Mode” + “:Data:240”), (translated “Sales and Returns” + “:Currency/currency:120”), …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0275.json#L6745) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L901) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L5)
