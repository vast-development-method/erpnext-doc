# Shared transaction rules · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Taxes and totals

<a id="op-94ce2155253968"></a>
### Get itemised tax breakup data

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_itemised_tax_breakup_data`

**Inputs** doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** itemised\_tax\_data.

**Local steps**

- Set itemised\_tax from get\_itemised\_tax(doc).
- Set itemised\_tax\_data from list().
- For each tuple(item\_code, taxes) in itemised\_tax.items().
  - Set taxable\_amount from next(iter(taxes.values())).get(“taxable\_amount”).
  - Evaluate itemised\_tax\_data.append(Platform.\_dict(mapping(“item” → item\_code, “taxable\_amount” → taxable\_amount, expand taxes))).
- Return itemised\_tax\_data.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L1084) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1140) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L809)

<a id="op-854d5e9ffdfea7"></a>
### Get itemised tax

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_itemised_tax`

**Inputs** doc, with\_tax\_account = false.

**Explicit results** itemised\_tax.

**Local steps**

- Set itemised\_tax from mapping().
- Set precision from doc.precision(“tax\_amount”, “taxes”).
- For each row in doc.get(“\_item\_wise\_tax\_details”).
  - Set item from row.get(“item”).
  - Set tax from row.get(“tax”).
  - If (not item or not tax).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item → not tax.
    - Continue with the next iteration or loop test.
  - Set item\_code from (item.item\_code or item.item\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.item\_code → item.item\_name.
  - If (getattr(tax, “category”, no value) and tax.category equals “Valuation”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(tax, “category”, no value) → tax.category equals “Valuation”.
    - Continue with the next iteration or loop test.
  - Set tax\_info from itemised\_tax.setdefault(item\_code, Platform.\_dict()).setdefault(tax.description, Platform.\_dict(mapping(“tax\_amount” → 0.0, “taxable\_amount” → 0.0, “tax\_rate” → row.rate))).
  - Update tax\_info.tax\_amount using + flt(row.amount, precision).
  - Set conversion\_rate from (doc.conversion\_rate or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.conversion\_rate → 1.
  - Update tax\_info.taxable\_amount using + flt((row.taxable\_amount ÷ conversion\_rate), precision).
  - If with\_tax\_account.
    - Set tax\_info.tax\_account from tax.account\_head.
- Return itemised\_tax.

**Values supplied outside this operation** selected callable from getattr(tax, “category”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L1358) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L808)

<a id="op-8f96db55ee0d9a"></a>
### Get rounded tax amount

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_rounded_tax_amount`

**Inputs** itemised\_tax, precision.

**Local steps**

- For each taxes in itemised\_tax.
  - For each row in taxes.values().
    - If (isinstance(row, dict) and isinstance(row at “tax\_amount”, float)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(row, dict) → isinstance(row at “tax\_amount”, float).
      - Set row at “tax\_amount” from flt(row at “tax\_amount”, precision).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L1954) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L815)

<a id="op-c5e3fd4cc66acb"></a>
### Get rounding tax settings

`operation_enterprise_controllers_taxes_and_totals_business_behavior_get_rounding_tax_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** Platform.get\_single\_value(“Accounts Settings”, “round\_row\_wise\_tax”).

**Local steps**

- Return Platform.get\_single\_value(“Accounts Settings”, “round\_row\_wise\_tax”).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “round\_row\_wise\_tax”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L2149) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L816)

<a id="op-4003617eac7599"></a>
### Ignore item wise tax details

`operation_enterprise_controllers_taxes_and_totals_business_behavior_ignore_item_wise_tax_details`

**Inputs** doc.

**Explicit results** true · false.

**Local steps**

- If not doc.meta.get\_field(“item\_wise\_tax\_details”).
  - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L2228) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L817)

<a id="op-465207bb94e6ef"></a>
### Process item wise tax details

`operation_enterprise_controllers_taxes_and_totals_business_behavior_process_item_wise_tax_details`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If ignore\_item\_wise\_tax\_details(doc).
  - Return no value.
- If not (doc.get(“update\_item\_wise\_tax\_details”) and doc.get(“\_item\_wise\_tax\_details”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“update\_item\_wise\_tax\_details”) → doc.get(“\_item\_wise\_tax\_details”).
  - Return no value.
- Set docs from list().
- For each row in doc.get(“\_item\_wise\_tax\_details”).
  - Set tax\_details from doc.append(“item\_wise\_tax\_details”, mapping(expand row, “docstatus” → doc.docstatus, “item\_row” → row.item.name, “tax\_row” → row.tax.name)).
  - Evaluate tax\_details.set\_new\_name().
  - Evaluate docs.append(tax\_details).
- Evaluate bulk\_insert(“Item Wise Tax Detail”, docs).
- Set doc.update\_item\_wise\_tax\_details from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L2312) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L822)

<a id="op-edeca29c13947f"></a>
### Init landed taxes and totals.initialize

`operation_enterprise_controllers_taxes_and_totals_business_behavior_initialize_landed_taxes_and_totals_initialize`

**Inputs** self, doc.

**Local steps**

- Set self.doc from doc.
- Set self.tax\_field from “taxes” when self.doc.doctype equals “Landed Cost Voucher”, otherwise “additional\_costs”.
  - Value choice on self.doc.doctype equals “Landed Cost Voucher” — true gives “taxes”, false gives “additional\_costs”.
- Evaluate self.set\_account\_currency().
- Evaluate self.set\_exchange\_rate().
- Evaluate self.set\_amounts\_in\_company\_currency().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set account currency](operations-036.md#op-dbac07e1375f51), [set exchange rate](operations-036.md#op-71f44bb3704755), [set amounts in company currency](operations-036.md#op-18af94a435c43b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L2687) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L818)

<a id="op-dbac07e1375f51"></a>
### Init landed taxes and totals.set account currency

`operation_enterprise_controllers_taxes_and_totals_business_behavior_initialize_landed_taxes_and_totals_set_account_currency`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.doc.company).
- For each d in self.doc.get(self.tax\_field).
  - If not d.account\_currency.
    - Set account\_currency from Platform.get\_cached\_value(“Account”, d.expense\_account, “account\_currency”).
    - Set d.account\_currency from (account\_currency or company\_currency).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in account\_currency → company\_currency.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.expense\_account, “account\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L2865) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1150) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L819)

<a id="op-71f44bb3704755"></a>
### Init landed taxes and totals.set exchange rate

`operation_enterprise_controllers_taxes_and_totals_business_behavior_initialize_landed_taxes_and_totals_set_exchange_rate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Exchange Rate is mandatory”.format(d.idx).

**Local steps**

- Set company\_currency from Enterprise.get\_company\_currency(self.doc.company).
- For each d in self.doc.get(self.tax\_field).
  - If d.account\_currency equals company\_currency.
    - Set d.exchange\_rate from 1.
  - Otherwise.
    - If not d.exchange\_rate.
      - Set d.exchange\_rate from get\_exchange\_rate(self.doc.posting\_date, account = d.expense\_account, account\_currency = d.account\_currency, company = self.doc.company).
  - If not d.exchange\_rate.
    - Call the validation error handler Platform.throw(translated “Row {0}: Exchange Rate is mandatory”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L3071) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L821)

<a id="op-18af94a435c43b"></a>
### Init landed taxes and totals.set amounts in company currency

`operation_enterprise_controllers_taxes_and_totals_business_behavior_initialize_landed_taxes_and_totals_set_amounts_in_company_currency`

**Inputs** self.

**Local steps**

- For each d in self.doc.get(self.tax\_field).
  - Set d.amount from flt(d.amount, d.precision(“amount”)).
  - Set d.base\_amount from flt((d.amount × flt(d.exchange\_rate)), d.precision(“base\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0404.json#L3408) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L820)

## Service · Trends

<a id="op-fae544f7c2cd12"></a>
### Get tables

`operation_enterprise_binding_enterprise_controllers_trends_get_tables`

**Inputs** trans.

**Explicit results** tuple(Platform.qb.DocType(trans), Platform.qb.DocType(formatted text {trans} Item)).

**Local steps**

- Return tuple(Platform.qb.DocType(trans), Platform.qb.DocType(formatted text {trans} Item)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L465)

<a id="op-b7b1ce87240a3b"></a>
### Get columns

`operation_enterprise_controllers_trends_business_behavior_get_columns`

**Inputs** filters, trans.

**Explicit results** conditions.

**Local steps**

- Evaluate validate\_filters(filters).
- Set based\_on\_details from based\_wise\_columns\_query(filters.get(“based\_on”), trans).
- Set tuple(period\_cols, period\_select) from period\_wise\_columns\_query(filters, trans).
- Set group\_by\_cols from group\_wise\_column(filters.get(“group\_by”), trans).
- Set columns from ((based\_on\_details at “based\_on\_cols” + period\_cols) + list((translated “Total(Qty)” + “:Float:120”), (translated “Total(Amt)” + “:Currency/currency:120”))).
- If group\_by\_cols.
  - Set columns from (((based\_on\_details at “based\_on\_cols” + group\_by\_cols) + period\_cols) + list((translated “Total(Qty)” + “:Float:120”), (translated “Total(Amt)” + “:Currency/currency:120”))).
- Set conditions from mapping(“based\_on\_select” → based\_on\_details at “based\_on\_select”, “period\_wise\_select” → period\_select, “columns” → columns, “group\_by” → based\_on\_details at “based\_on\_group\_by”, …).
- Set conditions at “company\_currency” from Enterprise.get\_company\_currency(filters.get(“company”)) when filters.get(“company”), otherwise no value.
  - Value choice on filters.get(“company”) — true gives Enterprise.get\_company\_currency(filters.get(“company”)), false gives no value.
- Return conditions.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L995)

<a id="op-b3316652fe2680"></a>
### Validate filters

`operation_enterprise_controllers_trends_business_behavior_validate_filters`

**Inputs** filters.

**Record and data access** read “Fiscal Year” via exists.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated f) · validation helper — translated “Fiscal Year {0} Does Not Exist”.format(filters.get(“fiscal\_year”)) · validation helper — translated “'Based On' and 'Group By' can not be same” · validation helper.

**Local steps**

- If not filters.get(“fiscal\_year”).
  - Set filters at “fiscal\_year” from get\_fiscal\_year(today()) at 0.
- If not filters.get(“company”).
  - Set filters at “company” from Platform.defaults.get\_user\_default(“Company”).
- For each f in list(“Fiscal Year”, “Based On”, “Period”, “Company”).
  - If not filters.get(f.lower().replace(one space, “\_”)).
    - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated f)).
- If not Platform.db.exists(“Fiscal Year”, filters.get(“fiscal\_year”)).
  - Call the validation error handler Platform.throw(translated “Fiscal Year {0} Does Not Exist”.format(filters.get(“fiscal\_year”))).
- If filters.get(“based\_on”) equals filters.get(“group\_by”).
  - Call the validation error handler Platform.throw(translated “'Based On' and 'Group By' can not be same”).
- If (filters.get(“period\_based\_on”) and filters.period\_based\_on does not belong to list(“bill\_date”, “posting\_date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“period\_based\_on”) → filters.period\_based\_on does not belong to list(“bill\_date”, “posting\_date”).
  - Call the validation error handler Platform.throw(msg = translated “{0} can be either {1} or {2}.”.format(Platform.bold(“Period based On”), Platform.bold(“Posting Date”), Platform.bold(“Billing Date”)), title = translated “Invalid Filter”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1005)

<a id="op-99d2885f96c3aa"></a>
### Get item codes

`operation_enterprise_binding_enterprise_controllers_trends_get_item_codes`

**Inputs** filters.

**Explicit results** item\_codes.

**Local steps**

- Set item\_codes from (filters.get(“item\_code”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“item\_code”) → list().
- If isinstance(item\_codes, str).
  - Set item\_codes from list(item\_codes).
- Return item\_codes.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L164) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L462)

<a id="op-427b39bd6d1cad"></a>
### Get trans date

`operation_enterprise_binding_enterprise_controllers_trends_get_trans_date`

**Inputs** filters, trans, t1.

**Explicit results** t1.transaction\_date · Coalesce(t1.bill\_date, t1.posting\_date) · t1.posting\_date.

**Local steps**

- If trans does not belong to list(“Sales Invoice”, “Purchase Invoice”, “Purchase Receipt”, “Delivery Note”).
  - Return t1.transaction\_date.
- If (filters.period\_based\_on equals “bill\_date” and trans belongs to list(“Sales Invoice”, “Purchase Invoice”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.period\_based\_on equals “bill\_date” → trans belongs to list(“Sales Invoice”, “Purchase Invoice”).
  - Return Coalesce(t1.bill\_date, t1.posting\_date).
- Return t1.posting\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L466)

<a id="op-e99f4cdeafe498"></a>
### Get conditions

`operation_enterprise_binding_enterprise_controllers_trends_get_conditions`

**Inputs** filters, conditions, t1, t2.

**Explicit results** criteria.

**Local steps**

- Set criteria from list(t1.docstatus equals 1).
- If (not filters.get(“include\_closed\_orders”) and conditions.get(“trans”) belongs to list(“Sales Order”, “Purchase Order”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.get(“include\_closed\_orders”) → conditions.get(“trans”) belongs to list(“Sales Order”, “Purchase Order”).
  - Evaluate criteria.append(t1.status differs from “Closed”).
- If filters.get(“based\_on”) equals “Project”.
  - Evaluate criteria.append(conditions at “group\_by” at 0 differs from empty text).
- Set permission\_condition from get\_permission\_condition(conditions at “trans”).
- If permission\_condition is distinct from no value.
  - Evaluate criteria.append(permission\_condition).
- If item\_codes bound to get\_item\_codes(filters).
  - Evaluate criteria.append(t2.item\_code.isin(item\_codes)).
- Return criteria.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L163) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L461)

<a id="op-f1638203bf6f96"></a>
### Get base query

`operation_enterprise_binding_enterprise_controllers_trends_get_base_query`

**Inputs** filters, conditions, t1, t2, year\_start\_date, year\_end\_date.

**Explicit results** query.

**Local steps**

- Set trans\_date from get\_trans\_date(filters, conditions at “trans”, t1).
- Set query from nested operand in the contract.qb.from\_(t1).inner\_join(t2).on(t2.parent equals t1.name).
- For each tuple(table, criterion) in conditions at “joins”.
  - Set query from query.inner\_join(table).on(criterion).
- Set query from query.where(t1.company equals filters.get(“company”)).where(trans\_date at slice year\_start\_date to year\_end\_date).
- For each criterion in get\_conditions(filters, conditions, t1, t2).
  - Set query from query.where(criterion).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1220) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L460)

<a id="op-138767a23045dd"></a>
### Get data

`operation_enterprise_controllers_trends_business_behavior_get_data`

**Inputs** filters, conditions.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**State and service calls** call insert on dt.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set inc from empty text.
- Set tuple(t1, t2) from get\_tables(conditions at “trans”).
- Set tuple(year\_start\_date, year\_end\_date) from Platform.get\_cached\_value(“Fiscal Year”, filters.get(“fiscal\_year”), list(“year\_start\_date”, “year\_end\_date”)).
- Set base from get\_base\_query(filters, conditions, t1, t2, …).
- Set empty\_group\_label from translated “No Customer Group” when (conditions.get(“trans”) equals “Quotation” and filters.get(“based\_on”) equals “Customer Group”), otherwise no value.
  - Value choice on (conditions.get(“trans”) equals “Quotation” and filters.get(“based\_on”) equals “Customer Group”) — true gives translated “No Customer Group”, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in conditions.get(“trans”) equals “Quotation” → filters.get(“based\_on”) equals “Customer Group”.
- If filters.get(“group\_by”).
  - Set sel\_col from no value.
  - Set ind from conditions at “columns”.index(conditions at “grbc” at 0).
  - If filters.get(“group\_by”) equals “Item”.
    - Set sel\_col from t2.item\_code.
  - Otherwise.
    - If filters.get(“group\_by”) equals “Customer”.
      - If conditions.get(“trans”) equals “Quotation”.
        - Set sel\_col from Concat(t1.quotation\_to, “: ”, t1.party\_name).
      - Otherwise.
        - Set sel\_col from t1.customer.
    - Otherwise.
      - If filters.get(“group\_by”) equals “Supplier”.
        - Set sel\_col from t1.supplier.
  - Set based\_on\_key from conditions at “group\_by” at 0.
  - If filters.get(“based\_on”) belongs to list(“Customer”, “Supplier”).
    - Set inc from 3.
  - Otherwise.
    - If filters.get(“based\_on”) belongs to list(“Item”).
      - Set inc from 2.
    - Otherwise.
      - Set inc from 1.
  - Set data1 from base.select(expanded nested operand in the contract at nested operand in the contract, expanded nested operand in the contract at nested operand in the contract).groupby(expanded conditions at “group\_by”). ….
  - For each d in range(len(data1)).
    - Set dt from data1 at d.
    - Evaluate dt.insert(ind, empty text).
    - Evaluate data.append(dt).
    - Set row from nested operand in the contract(nested operand in the contract).distinct().where(based\_on\_key equals data1 at d at 0).run(as\_list = 1).
    - For each i in range(len(row)).
      - Set des from list of empty text for q drawn from range(len(conditions at “columns”)).
        - Draw q from range(len(conditions at “columns”)).
      - Set company from Platform.qb.DocType(“Company”).
      - Set row1 from nested operand in the contract(nested operand in the contract).where(based\_on\_key equals nested operand in the contract at nested operand in the contract).groupby(company.default\_currency, sel\_col).run(as\_list = 1).
      - Set des at ind from row at i at 0.
      - Set des at (ind − 1) from row1 at 0 at 0.
      - For each j in range(1, (len(conditions at “columns”) − inc)).
        - Set des at (j + inc) from row1 at 0 at j.
      - Evaluate data.append(des).
    - If (empty\_group\_label and not dt at 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in empty\_group\_label → not dt at 0.
      - Set dt at 0 from empty\_group\_label.
  - Set total\_row from calculate\_total\_row(data1, conditions at “columns”, conditions.get(“company\_currency”)).
  - Evaluate data.append(total\_row).
- Otherwise.
  - Set data from base.select(expanded nested operand in the contract at nested operand in the contract, expanded nested operand in the contract at nested operand in the contract).groupby(expanded conditions at “group\_by”). ….
  - If empty\_group\_label.
    - For each row in data.
      - If not row at 0.
        - Set row at 0 from empty\_group\_label.
  - Set total\_row from calculate\_total\_row(data, conditions at “columns”, conditions.get(“company\_currency”)).
  - Evaluate data.append(total\_row).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, filters.get(“fiscal\_year”), list(“year\_start\_date”, “year\_end\_date”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L996)

<a id="op-b59d29b8d046d0"></a>
### Get permission condition

`operation_enterprise_binding_enterprise_controllers_trends_get_permission_condition`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L464)

<a id="op-d650da35f45629"></a>
### Calculate total row

`operation_enterprise_controllers_trends_business_behavior_calculate_total_row`

**Inputs** data, columns, company\_currency = no value.

**Explicit results** total\_row.

**Local steps**

- Bind local operation wrap\_in\_quotes for subsequent calls.
- Set total\_values from mapping().
- Set currency\_col\_idx from no value.
- For each tuple(i, col) in enumerate(columns).
  - If isinstance(col, dict).
    - If (col.get(“fieldtype”) equals “Link” and col.get(“options”) equals “Currency”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.get(“fieldtype”) equals “Link” → col.get(“options”) equals “Currency”.
      - Set currency\_col\_idx from i.
  - Otherwise.
    - If (“Float” belongs to col or “Currency/currency” belongs to col).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in “Float” belongs to col → “Currency/currency” belongs to col.
      - Set total\_values at i from 0.
- For each row in data.
  - For each i in total\_values.keys().
    - Update total\_values at i using + row at i when row at i is distinct from no value, otherwise 0.
      - Value choice on row at i is distinct from no value — true gives row at i, false gives 0.
- Set total\_row from list(wrap\_in\_quotes(translated “Total”)).
- For each i in range(1, len(columns)).
  - Evaluate total\_row.append(total\_values.get(i, no value)).
- If currency\_col\_idx is distinct from no value.
  - Set total\_row at currency\_col\_idx from company\_currency.
- Return total\_row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L993)

<a id="op-b0ede0caa30ae4"></a>
### Calculate total row.wrap in quotes

`operation_enterprise_controllers_trends_business_behavior_calculate_total_row_wrap_in_quotes`

**Inputs** label.

**Explicit results** formatted text '{label}'.

**Local steps**

- Return formatted text '{label}'.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0422.json#L7529) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L994)

<a id="op-1e02186b41fb2f"></a>
### Get mon

`operation_enterprise_controllers_trends_business_behavior_get_mon`

**Inputs** dt.

**Explicit results** getdate(dt).strftime(“%b”).

**Local steps**

- Return getdate(dt).strftime(“%b”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0422.json#L7586) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L997)

<a id="op-a2338017708b8a"></a>
### Period wise columns query

`operation_enterprise_controllers_trends_business_behavior_period_wise_columns_query`

**Inputs** filters, trans.

**Explicit results** tuple(pwc, period\_select).

**Local steps**

- Set tuple(t1, t2) from get\_tables(trans).
- Set trans\_date from get\_trans\_date(filters, trans, t1).
- Set tuple(pwc, period\_select) from tuple(list(), list()).
- Set bet\_dates from get\_period\_date\_ranges(filters.get(“period”), filters.get(“fiscal\_year”)).
- If filters.get(“period”) differs from “Yearly”.
  - For each dt in bet\_dates.
    - Evaluate get\_period\_wise\_columns(dt, filters.get(“period”), pwc).
    - Update period\_select using + get\_period\_wise\_terms(dt, trans\_date, t2).
- Otherwise.
  - Set pwc from list((((translated nested operand in the contract.get(“fiscal\_year”) + “ (”) + translated “Qty”) + “):Float:120”), (((translated nested operand in the contract.get(“fiscal\_year”) + “ (”) + translated “Amt” ….
  - Set period\_select from list(Sum(t2.stock\_qty), Sum(t2.base\_net\_amount)).
- Update period\_select using + list(Sum(t2.stock\_qty), Sum(t2.base\_net\_amount)).
- Return tuple(pwc, period\_select).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1002)

<a id="op-da358dfd564b93"></a>
### Get period wise columns

`operation_enterprise_controllers_trends_business_behavior_get_period_wise_columns`

**Inputs** bet\_dates, period, pwc.

**Local steps**

- If period equals “Monthly”.
  - Update pwc using + list((((translated get\_mon(nested operand in the contract at nested operand in the contract) + “ (”) + translated “Qty”) + “):Float:120”), (((translated get\_mon(nested operand in the contract at nested ope ….
- Otherwise.
  - Update pwc using + list((((((nested operand in the contract(nested operand in the contract) + “-”) + translated nested operand in the contract(nested operand in the contract)) + “ (”) + translated “Qty”) + “):Float:120”), (( ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0423.json#L657) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1000)
