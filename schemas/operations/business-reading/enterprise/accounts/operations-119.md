# Accounting and settlement · operations 119

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-f90aa0c88278ff"></a>
### Get values for columns

`operation_enterprise_accounts_report_utils_business_behavior_get_values_for_columns`

**Inputs** report\_columns, report\_row.

**Explicit results** values.

**Local steps**

- Set values from mapping().
- If not report\_columns.
  - Return values.
- For each column in report\_columns.
  - Set fieldname from column at “fieldname”.
  - Set values at fieldname from report\_row.get(fieldname).
- Return values.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L4255) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1074) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L145)

<a id="op-e77693a80695d1"></a>
### Get party details

`operation_enterprise_accounts_report_utils_business_behavior_get_party_details`

**Inputs** party\_type, party\_list.

**Explicit results** party\_details.

**Local steps**

- Set party\_details from mapping().
- Set party from Platform.qb.DocType(party\_type).
- Set query from nested operand in the contract.qb.from\_(party).select(party.name, party.tax\_id).where(party.name.isin(party\_list)).
- If party\_type equals “Supplier”.
  - Set query from query.select(party.supplier\_group).
- Otherwise.
  - Set query from query.select(party.customer\_group, party.territory).
- Set party\_detail\_list from query.run(as\_dict = true).
- For each party\_dict in party\_detail\_list.
  - Set party\_details at party\_dict.name from party\_dict.
- Return party\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L4410) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1069) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L140)

<a id="op-8190641f44d8a8"></a>
### Get taxes query

`operation_enterprise_accounts_report_utils_business_behavior_get_taxes_query`

**Inputs** invoice\_list, doctype, parenttype.

**Explicit results** query.where(taxes.category.isin(list(“Total”, “Valuation and Total”))) · query · query.where(taxes.charge\_type.isin(list(“On Paid Amount”, “Actual”))).

**Local steps**

- Set taxes from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nes ….
  - Draw inv from invoice\_list.
- If doctype equals “Purchase Taxes and Charges”.
  - Return query.where(taxes.category.isin(list(“Total”, “Valuation and Total”))).
- Otherwise.
  - If doctype equals “Sales Taxes and Charges”.
    - Return query.
- Return query.where(taxes.charge\_type.isin(list(“On Paid Amount”, “Actual”))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0287.json#L4778) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1073) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L144)

<a id="op-cd2dbf4ddb9a3d"></a>
### Get journal entries

`operation_enterprise_accounts_report_utils_business_behavior_get_journal_entries`

**Inputs** filters, args.

**Explicit results** journal\_entries.

**Local steps**

- Set je from Platform.qb.DocType(“Journal Entry”).
- Set journal\_account from Platform.qb.DocType(“Journal Entry Account”).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“doctype”), je.name, je.posting\_date, nested operand in the contract.as\_(nested operand in the contr ….
- Set query from apply\_common\_conditions(filters, query, doctype = “Journal Entry”, child\_doctype = “Journal Entry Account”, payments = true).
- Set journal\_entries from query.run(as\_dict = true).
- Return journal\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1067) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L138)

<a id="op-641442a1942877"></a>
### Get payment entries

`operation_enterprise_accounts_report_utils_business_behavior_get_payment_entries`

**Inputs** filters, args.

**Explicit results** payment\_entries.

**Local steps**

- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set paid\_from\_party from pe.paid\_from.isin(args.party\_account).
- Set query from nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“doctype”), pe.name, pe.posting\_date, nested operand in the contract.as\_(nested operand in the contr ….
- Set query from apply\_common\_conditions(filters, query, doctype = “Payment Entry”, payments = true).
- Set payment\_entries from query.run(as\_dict = true).
- If payment\_entries.
  - Set ded from Platform.qb.DocType(“Payment Entry Deduction”).
  - Set deduction\_totals from Platform.\_dict(nested operand in the contract.where((nested operand in the contract bitwise and nested operand in the contract)).groupby(ded.parent).run()).
    - Draw d from payment\_entries.
  - For each d in payment\_entries.
    - Set exchange\_rate from (d.source\_exchange\_rate when d.payment\_type equals “Receive”, otherwise d.target\_exchange\_rate or 1).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.source\_exchange\_rate when d.payment\_type equals “Receive”, otherwise d.target\_exchange\_rate → 1.
      - Value choice on d.payment\_type equals “Receive” — true gives d.source\_exchange\_rate, false gives d.target\_exchange\_rate.
    - Set d.base\_grand\_total from (flt(d.base\_grand\_total) + (flt(deduction\_totals.get(d.name)) ÷ exchange\_rate)).
  - Evaluate set\_party\_ledger\_amounts(payment\_entries, filters.get(args.party), args.party\_account).
- Return payment\_entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1070) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L141)

<a id="op-82489bd9567ed4"></a>
### Set party ledger amounts

`operation_enterprise_binding_enterprise_accounts_report_utils_set_party_ledger_amounts`

**Inputs** payment\_entries, party, party\_account.

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Set amounts from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
  - Draw d from payment\_entries.
- Set amounts from mapping of d.voucher\_no → d for d drawn from amounts.
  - Draw d from amounts.
- For each d in payment\_entries.
  - Set d.debit from flt(amounts.get(d.name, mapping()).get(“debit”)).
  - Set d.credit from flt(amounts.get(d.name, mapping()).get(“credit”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L215) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1280)

<a id="op-cdc4725689abdf"></a>
### Apply common conditions

`operation_enterprise_accounts_report_utils_business_behavior_apply_common_conditions`

**Inputs** filters, query, doctype, child\_doctype = no value, payments = false.

**Explicit results** query.

**Local steps**

- Set parent\_doc from Platform.qb.DocType(doctype).
- If child\_doctype.
  - Set child\_doc from Platform.qb.DocType(child\_doctype).
- Set join\_required from false.
- If filters.get(“company”).
  - Set query from query.where(parent\_doc.company equals filters.company).
- If filters.get(“from\_date”).
  - Set query from query.where(parent\_doc.posting\_date ≥ filters.from\_date).
- If filters.get(“to\_date”).
  - Set query from query.where(parent\_doc.posting\_date ≤ filters.to\_date).
- If payments.
  - If (doctype equals “Journal Entry” and filters.get(“cost\_center”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Journal Entry” → filters.get(“cost\_center”).
    - Set query from query.where(child\_doc.cost\_center.isin(get\_with\_descendants(“Cost Center”, filters.cost\_center))).
  - Otherwise.
    - If filters.get(“cost\_center”).
      - Set query from query.where(parent\_doc.cost\_center.isin(get\_with\_descendants(“Cost Center”, filters.cost\_center))).
- Otherwise.
  - If filters.get(“cost\_center”).
    - Set query from query.where(child\_doc.cost\_center.isin(get\_with\_descendants(“Cost Center”, filters.cost\_center))).
    - Set join\_required from true.
  - If filters.get(“warehouse”).
    - Set query from query.where(child\_doc.warehouse.isin(get\_with\_descendants(“Warehouse”, filters.warehouse))).
    - Set join\_required from true.
  - If filters.get(“item\_group”).
    - Set query from query.where(child\_doc.item\_group.isin(get\_with\_descendants(“Item Group”, filters.item\_group))).
    - Set join\_required from true.
- If not payments.
  - If filters.get(“brand”).
    - Set query from query.where(child\_doc.brand equals filters.brand).
    - Set join\_required from true.
- If join\_required.
  - Set query from query.inner\_join(child\_doc).on(parent\_doc.name equals child\_doc.parent).
  - Set query from query.where(child\_doc.parenttype equals doctype).
  - Set query from query.distinct().
- If parent\_doc.get\_table\_name() differs from “tabJournal Entry”.
  - Set query from filter\_invoices\_based\_on\_dimensions(filters, query, parent\_doc).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1059) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L130)

<a id="op-967866e419f8ba"></a>
### Get with descendants

`operation_enterprise_binding_enterprise_accounts_report_utils_get_with_descendants`

**Inputs** doctype, name.

**Declared result** list at str.

**Explicit results** list(name, expanded get\_descendants\_of(doctype, name, ignore\_permissions = true)).

**Local steps**

- Return list(name, expanded get\_descendants\_of(doctype, name, ignore\_permissions = true)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1278)

<a id="op-f8fcbd2ee6f9c9"></a>
### Get advance taxes and charges

`operation_enterprise_accounts_report_utils_business_behavior_get_advance_taxes_and_charges`

**Inputs** invoice\_list.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….

**Local steps**

- Set adv\_taxes from Platform.qb.DocType(“Advance Taxes and Charges”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contr ….
  - Draw inv from invoice\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0288.json#L1194) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1063) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L134)

<a id="op-53410e97637198"></a>
### Filter invoices based on dimensions

`operation_enterprise_accounts_report_utils_business_behavior_filter_invoices_based_on_dimensions`

**Inputs** filters, query, parent\_doc.

**Record and data access** read “DocType” via get\_cached\_value.

**Explicit results** query.

**Local steps**

- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- If accounting\_dimensions.
  - For each dimension in accounting\_dimensions.
    - If filters.get(dimension.fieldname).
      - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
        - Set filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, filters.get(dimension.fieldname)).
      - Set fieldname from dimension.fieldname.
      - Set query from query.where(parent\_doc at fieldname.isin(filters at fieldname)).
- Return query.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0288.json#L1641) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1062) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L133)

<a id="op-8d91e41d328a26"></a>
### Get opening row

`operation_enterprise_accounts_report_utils_business_behavior_get_opening_row`

**Inputs** party\_type, party, from\_date, company.

**Explicit results** nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“account”), nested operand in the contract.as\_(“debit”), nested operand in the contract.as\_(“credit” ….

**Local steps**

- Evaluate Platform.has\_permission(party\_type, “read”, party, throw = true).
- Set party\_account from get\_party\_account(party\_type, party, company, include\_advance = true).
- Set gle from Platform.qb.DocType(“GL Entry”).
- Return nested operand in the contract(nested operand in the contract).select(nested operand in the contract.as\_(“account”), nested operand in the contract.as\_(“debit”), nested operand in the contract.as\_(“credit” ….

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, “read”, party, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L139)

<a id="op-a5128685f5362f"></a>
### Has gl entry restrictions

`operation_enterprise_binding_enterprise_accounts_report_utils_has_gl_entry_restrictions`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool(build\_match\_conditions(“GL Entry”)).

**Local steps**

- Bind dependencies build\_match\_conditions.
- Return bool(build\_match\_conditions(“GL Entry”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1279)

<a id="op-2f054f2eb6d51c"></a>
### Get fiscal year

`operation_enterprise_accounts_utils_business_behavior_get_fiscal_year`

**Inputs** date = no value, fiscal\_year = no value, label = “Date”, verbose = 1, company = no value, as\_dict = false, boolean = no value, raise\_on\_missing = true, truncate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** tuple(“-”.join(generator of y at slice negative 2 to no value for y drawn from fiscal\_year at 0.split(“-”)), fiscal\_year at 1, fiscal\_year at 2) · fiscal\_year · false.

**Local steps**

- If isinstance(raise\_on\_missing, str).
  - Set raise\_on\_missing from loads(raise\_on\_missing).
- If isinstance(boolean, str).
  - Set boolean from loads(boolean).
- If boolean is distinct from no value.
  - Set raise\_on\_missing from not boolean.
- Set fiscal\_years from get\_fiscal\_years(date, fiscal\_year, label, verbose, as\_dict = as\_dict, raise\_on\_missing = raise\_on\_missing, …).
- If fiscal\_years.
  - Set fiscal\_year from fiscal\_years at 0.
  - If truncate.
    - Return tuple(“-”.join(generator of y at slice negative 2 to no value for y drawn from fiscal\_year at 0.split(“-”)), fiscal\_year at 1, fiscal\_year at 2).
      - Draw y from fiscal\_year at 0.split(“-”).
  - Return fiscal\_year.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L214)

<a id="op-f125dc7f7ccbe1"></a>
### Get fiscal years

`operation_enterprise_accounts_utils_business_behavior_get_fiscal_years`

**Inputs** transaction\_date = no value, fiscal\_year = no value, label = “Date”, verbose = 1, company = no value, as\_dict = false, boolean = no value, raise\_on\_missing = true.

**State and service calls** msgprint with error\_msg.

**Explicit results** all\_fiscal\_years · tuple(fy) · tuple(tuple(fy.name, fy.year\_start\_date, fy.year\_end\_date)) · list().

**Explicit failure paths** FiscalYearError(error\_msg).

**Local steps**

- If transaction\_date.
  - Set transaction\_date from getdate(transaction\_date).
- If boolean is distinct from no value.
  - Set raise\_on\_missing from not boolean.
- Set all\_fiscal\_years from \_get\_fiscal\_years(company = company).
- If (not transaction\_date and not fiscal\_year).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not transaction\_date → not fiscal\_year.
  - Return all\_fiscal\_years.
- For each fy in all\_fiscal\_years.
  - If ((fiscal\_year and fy.name equals fiscal\_year) or (transaction\_date and getdate(fy.year\_start\_date) ≤ transaction\_date and getdate(fy.year\_end\_date) ≥ transaction\_date)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (fiscal\_year and fy.name equals fiscal\_year) → (transaction\_date and getdate(fy.year\_start\_date) ≤ transaction\_date and getdate(fy.year\_end\_date) ≥ transaction\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fiscal\_year → fy.name equals fiscal\_year.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in transaction\_date → getdate(fy.year\_start\_date) ≤ transaction\_date → getdate(fy.year\_end\_date) ≥ transaction\_date.
    - If as\_dict.
      - Return tuple(fy).
    - Otherwise.
      - Return tuple(tuple(fy.name, fy.year\_start\_date, fy.year\_end\_date)).
- If raise\_on\_missing.
  - Set error\_msg from translated “{0} {1} is not in any active Fiscal Year”.format(translated label, formatdate(transaction\_date)).
  - If company.
    - Set error\_msg from translated “{0} for {1}”.format(error\_msg, Platform.bold(company)).
  - If verbose equals 1.
    - Evaluate Platform.msgprint(error\_msg).
  - Raise FiscalYearError(error\_msg).
- Return list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L216)

<a id="op-64803cd6d7b1a0"></a>
### Get fiscal years

`operation_enterprise_accounts_utils_business_behavior_get_fiscal_years_2`

**Inputs** company = no value.

**Explicit results** fiscal\_years.

**Local steps**

- Set fiscal\_years from (Platform.cache().hget(“fiscal\_years”, company) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache().hget(“fiscal\_years”, company) → list().
- If not fiscal\_years.
  - Set FY from DocType(“Fiscal Year”).
  - Set query from nested operand in the contract.qb.from\_(FY).select(FY.name, FY.year\_start\_date, FY.year\_end\_date).where(FY.disabled equals 0).
  - If company.
    - Set FYC from DocType(“Fiscal Year Company”).
    - Set company\_years from nested operand in the contract.qb.from\_(FYC).select(FYC.parent).where(FYC.company equals company).
    - Set query from query.where((nested operand in the contract(nested operand in the contract).negate() bitwise or nested operand in the contract.name.isin(company\_years))).orderby(Case().when(nested operand in the contract. ….
  - Set query from query.orderby(FY.year\_start\_date, order = Order.desc).
  - Set fiscal\_years from query.run(as\_dict = true).
  - Evaluate Platform.cache().hset(“fiscal\_years”, company, fiscal\_years).
- Return fiscal\_years.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L217)

<a id="op-440235c50584b8"></a>
### Get fiscal year filter field

`operation_enterprise_accounts_utils_business_behavior_get_fiscal_year_filter_field`

**Inputs** company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** field.

**Local steps**

- Set field from mapping(“fieldtype” → “Select”, “options” → list(), “operator” → “Between”, “query\_value” → true).
- Set fiscal\_years from get\_fiscal\_years(company = company).
- For each fiscal\_year in fiscal\_years.
  - Evaluate field at “options”.append(mapping(“label” → fiscal\_year.name, “value” → fiscal\_year.name, “query\_value” → list(fiscal\_year.year\_start\_date.strftime(“%Y-%m-%d”), fiscal\_year.year\_end\_date.strftime(“%Y-%m-%d”)))).
- Return field.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L215)

<a id="op-6fdcd7e35db871"></a>
### Validate fiscal year

`operation_enterprise_accounts_utils_business_behavior_validate_fiscal_year`

**Inputs** date, fiscal\_year, company, label = “Date”, doc = no value.

**Local steps**

- Set years from list of f at 0 for f drawn from get\_fiscal\_years(date, label = translated label, company = company).
  - Draw f from get\_fiscal\_years(date, label = translated label, company = company).
- If fiscal\_year does not belong to years.
  - If doc.
    - Set doc.fiscal\_year from years at 0.
  - Otherwise.
    - Evaluate throw(translated “{0} '{1}' not in Fiscal Year {2}”.format(translated label, formatdate(date), fiscal\_year)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0299.json#L5232) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L258)

<a id="op-8a154cb9c52691"></a>
### Get balance on

`operation_enterprise_accounts_utils_business_behavior_get_balance_on`

**Inputs** account = no value, date = no value, party\_type = no value, party = no value, company = no value, in\_account\_currency = true, cost\_center = no value, ignore\_account\_permission = false, account\_type = no value, start\_date = no value, finance\_book = no value, include\_default\_fb\_balances = false, apply\_gl\_entry\_permissions = false.

**Record and data access** resolve a document from “Account” via get\_doc · read “Company” via get\_cached\_value · read “Account” via get\_all · execute query text (SELECT, GL Entry).format(select\_field, “ and ”.join(cond)).

**Explicit results** 0.0 · flt(bal).

**Local steps**

- If (not account and Platform.form\_dict.get(“account”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → Platform.form\_dict.get(“account”).
  - Set account from Platform.form\_dict.get(“account”).
- If (not date and Platform.form\_dict.get(“date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not date → Platform.form\_dict.get(“date”).
  - Set date from Platform.form\_dict.get(“date”).
- If (not party\_type and Platform.form\_dict.get(“party\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not party\_type → Platform.form\_dict.get(“party\_type”).
  - Set party\_type from Platform.form\_dict.get(“party\_type”).
- If (not party and Platform.form\_dict.get(“party”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not party → Platform.form\_dict.get(“party”).
  - Set party from Platform.form\_dict.get(“party”).
- If (not cost\_center and Platform.form\_dict.get(“cost\_center”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cost\_center → Platform.form\_dict.get(“cost\_center”).
  - Set cost\_center from Platform.form\_dict.get(“cost\_center”).
- Set cond from list(“is\_cancelled=0”).
- If start\_date.
  - Evaluate cond.append((“posting\_date &gt;= %s” modulo or format Platform.db.escape(cstr(start\_date)))).
- If date.
  - Evaluate cond.append((“posting\_date &lt;= %s” modulo or format Platform.db.escape(cstr(date)))).
- Otherwise.
  - Set date from nowdate().
- If account.
  - Set acc from Platform.get\_doc(“Account”, account).
- Attempt the following.
  - Evaluate get\_fiscal\_year(date, company = company, verbose = 0) at 1.
- On failure (FiscalYearError).
  - If getdate(date) &gt; getdate(nowdate()).
    - Evaluate get\_fiscal\_year(nowdate(), verbose = 1) at 1.
  - Otherwise.
    - Return 0.0.
- If account.
  - Set report\_type from acc.report\_type.
- Otherwise.
  - Set report\_type from empty text.
- If (cost\_center and report\_type equals “Profit and Loss”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cost\_center → report\_type equals “Profit and Loss”.
  - Set cc from Platform.get\_lazy\_doc(“Cost Center”, cost\_center).
  - If cc.is\_group.
    - Evaluate cond.append(formatted text  exists (  select 1 from ′tabCost Center′ cc where cc.name = gle.cost\_center  and cc.lft &gt;= {cc.lft} and cc.rgt &lt;= {cc.rgt}  )).
  - Otherwise.
    - Evaluate cond.append(formatted text gle.cost\_center = {Platform.db.escape(cost\_center)} ).
- If account.
  - If not (Platform.flags.ignore\_account\_permission or ignore\_account\_permission).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.ignore\_account\_permission → ignore\_account\_permission.
    - Evaluate acc.check\_permission(“read”).
  - If acc.is\_group.
    - Evaluate cond.append(formatted text exists (  select name from ′tabAccount′ ac where ac.name = gle.account  and ac.lft &gt;= {acc.lft} and ac.rgt &lt;= {acc.rgt}  )).
    - If acc.account\_currency equals Platform.get\_cached\_value(“Company”, acc.company, “default\_currency”).
      - Set in\_account\_currency from false.
  - Otherwise.
    - Evaluate cond.append(formatted text gle.account = {Platform.db.escape(account)} ).
- If account\_type.
  - Set accounts from Platform.db.get\_all(“Account”, filters = mapping(“company” → company, “account\_type” → account\_type, “is\_group” → 0), pluck = “name”, order\_by = “lft”).
  - Evaluate cond.append((“\\n\\t\\t\\tgle.account in (%s)\\n\\t\\t” modulo or format “, ”.join(list of nested operand in the contract.db.escape(account) for account drawn from accounts))).
    - Draw account from accounts.
- If (party\_type and party).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
  - Evaluate Platform.has\_permission(party\_type, “read”, party, throw = true).
  - Evaluate cond.append(formatted text gle.party\_type = {Platform.db.escape(party\_type)} and gle.party = {Platform.db.escape(party)} ).
- Set default\_finance\_book from no value.
- If company.
  - Evaluate cond.append((“gle.company = %s ” modulo or format Platform.db.escape(company))).
  - Set default\_finance\_book from Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).
- Set finance\_books from list(empty text).
- If finance\_book.
  - Evaluate finance\_books.append(finance\_book).
- If (default\_finance\_book and include\_default\_fb\_balances).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in default\_finance\_book → include\_default\_fb\_balances.
  - Evaluate finance\_books.append(default\_finance\_book).
- Evaluate cond.append(“(gle.finance\_book IS NULL OR gle.finance\_book IN %s)”).
- If apply\_gl\_entry\_permissions.
  - Evaluate cond.extend(get\_gl\_entry\_match\_conditions()).
- If (account or (party\_type and party) or account\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account → (party\_type and party) → account\_type.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type → party.
  - Set precision from get\_currency\_precision().
  - If in\_account\_currency.
    - Set select\_field from “sum(round(debit\_in\_account\_currency, %s)) - sum(round(credit\_in\_account\_currency, %s))”.
  - Otherwise.
    - Set select\_field from “sum(round(debit, %s)) - sum(round(credit, %s))”.
  - Set bal from Platform.db.sql(query text (SELECT, GL Entry).format(select\_field, “ and ”.join(cond)), tuple(precision, precision, tuple(finance\_books))) at 0 at 0.
  - Return flt(bal).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate() · effective access from acc.check\_permission(“read”), Platform.has\_permission(party\_type, “read”, party, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, acc.company, “default\_currency”), Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L207)

<a id="op-61d4dc23afbd81"></a>
### Get gl entry match conditions

`operation_enterprise_binding_enterprise_accounts_utils_get_gl_entry_match_conditions`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list() · list(formatted text ({match\_conditions})).

**Local steps**

- Bind dependencies build\_match\_conditions.
- Set match\_conditions from build\_match\_conditions(“GL Entry”).
- If not match\_conditions.
  - Return list().
- For each quoted\_table in tuple(“′tabGL Entry′.”, “"tabGL Entry".”).
  - Set match\_conditions from match\_conditions.replace(quoted\_table, “gle.”).
- Return list(formatted text ({match\_conditions})).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L218) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1283)

<a id="op-c5dc1d15601cb8"></a>
### Get count on

`operation_enterprise_accounts_utils_business_behavior_get_count_on`

**Inputs** account, fieldname, date.

**Record and data access** resolve a document from “Account” via get\_doc · execute query text (SELECT, GL Entry).format(“ and ”.join(cond)).

**State and service calls** execute a supplied database query.

**Explicit results** 0.0 · count.

**Local steps**

- Set cond from list(“is\_cancelled=0”).
- If date.
  - Evaluate cond.append((“posting\_date &lt;= %s” modulo or format Platform.db.escape(cstr(date)))).
- Otherwise.
  - Set date from nowdate().
- Attempt the following.
  - Set year\_start\_date from get\_fiscal\_year(date, verbose = 0) at 1.
- On failure (FiscalYearError).
  - If getdate(date) &gt; getdate(nowdate()).
    - Set year\_start\_date from get\_fiscal\_year(nowdate(), verbose = 1) at 1.
  - Otherwise.
    - Return 0.0.
- If account.
  - Set acc from Platform.get\_doc(“Account”, account).
  - If not Platform.flags.ignore\_account\_permission.
    - Evaluate acc.check\_permission(“read”).
  - If acc.report\_type equals “Profit and Loss”.
    - Evaluate cond.append((“posting\_date &gt;= '%s' and voucher\_type != 'Period Closing Voucher'” modulo or format year\_start\_date)).
  - If acc.is\_group.
    - Evaluate cond.append(formatted text exists (  select name from ′tabAccount′ ac where ac.name = gle.account  and ac.lft &gt;= {acc.lft} and ac.rgt &lt;= {acc.rgt}  )).
  - Otherwise.
    - Evaluate cond.append(formatted text gle.account = {Platform.db.escape(account)} ).
  - Set entries from Platform.db.sql(query text (SELECT, GL Entry).format(“ and ”.join(cond)), as\_dict = true).
  - Set count from 0.
  - For each gle in entries.
    - If fieldname does not belong to tuple(“invoiced\_amount”, “payables”).
      - Update count using + 1.
    - Otherwise.
      - Set dr\_or\_cr from “debit” when fieldname equals “invoiced\_amount”, otherwise “credit”.
        - Value choice on fieldname equals “invoiced\_amount” — true gives “debit”, false gives “credit”.
      - Set cr\_or\_dr from “credit” when fieldname equals “invoiced\_amount”, otherwise “debit”.
        - Value choice on fieldname equals “invoiced\_amount” — true gives “credit”, false gives “debit”.
      - Set select\_fields from “ifnull(sum(credit-debit),0)” when fieldname equals “invoiced\_amount”, otherwise “ifnull(sum(debit-credit),0)”.
        - Value choice on fieldname equals “invoiced\_amount” — true gives “ifnull(sum(credit-debit),0)”, false gives “ifnull(sum(debit-credit),0)”.
      - If (not gle.against\_voucher or gle.against\_voucher\_type belongs to list(“Sales Order”, “Purchase Order”) or (gle.against\_voucher equals gle.voucher\_no and gle.get(dr\_or\_cr) &gt; 0)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not gle.against\_voucher → gle.against\_voucher\_type belongs to list(“Sales Order”, “Purchase Order”) → (gle.against\_voucher equals gle.voucher\_no and gle.get(dr\_or\_cr) &gt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in gle.against\_voucher equals gle.voucher\_no → gle.get(dr\_or\_cr) &gt; 0.
        - Set payment\_amount from Platform.db.sql(formatted text   SELECT {select\_fields}  FROM ′tabGL Entry′ gle  WHERE docstatus &lt; 2 and posting\_date &lt;= %(date)s and against\_voucher = %(voucher\_no)s, mapping(“date” → date, ….
        - Set outstanding\_amount from ((flt(gle.get(dr\_or\_cr)) − flt(gle.get(cr\_or\_dr))) − payment\_amount).
        - Set currency\_precision from (get\_currency\_precision() or 2).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_currency\_precision() → 2.
        - If abs(flt(outstanding\_amount)) &gt; (0.1 ÷ (10 to the power currency\_precision)).
          - Update count using + 1.
  - Return count.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate() · effective access from acc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L212)

<a id="op-b94801ca6350e2"></a>
### Add ac

`operation_enterprise_accounts_utils_business_behavior_add_account`

**Inputs** args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Account” · call insert on ac.

**Explicit results** ac.name.

**Local steps**

- Bind dependencies make\_tree\_args.
- If not args.
  - Set args from Platform.local.form\_dict.
- Evaluate args.pop(“ignore\_permissions”, no value).
- Evaluate Platform.has\_permission(“Account”, “create”, throw = true).
- Set args.doctype from “Account”.
- Set args from make\_tree\_args(expanded names args).
- Set ac from Platform.new\_doc(“Account”).
- Evaluate ac.update(args).
- If not ac.parent\_account.
  - Set ac.parent\_account from args.get(“parent”).
- Set ac.old\_parent from empty text.
- Set ac.freeze\_account from “No”.
- If cint(ac.get(“is\_root”)).
  - Set ac.parent\_account from no value.
  - Set ac.flags.ignore\_mandatory from true.
- Evaluate ac.insert().
- Return ac.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”, “create”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1271) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L176)

<a id="op-e856ff922ba4ce"></a>
### Add cc

`operation_enterprise_accounts_utils_business_behavior_add_carbon_copy`

**Inputs** args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** request new\_doc for “Cost Center” · call insert on cc.

**Explicit results** cc.name.

**Local steps**

- Bind dependencies make\_tree\_args.
- If not args.
  - Set args from Platform.local.form\_dict.
- Set args.doctype from “Cost Center”.
- Set args from make\_tree\_args(expanded names args).
- If args.parent\_cost\_center equals args.company.
  - Set args.parent\_cost\_center from “{} - {}”.format(args.parent\_cost\_center, Platform.get\_cached\_value(“Company”, args.company, “abbr”)).
- Set cc from Platform.new\_doc(“Cost Center”).
- Evaluate cc.update(args).
- If not cc.parent\_cost\_center.
  - Set cc.parent\_cost\_center from args.get(“parent”).
- Set cc.old\_parent from empty text.
- Evaluate cc.insert().
- Return cc.name.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, args.company, “abbr”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1272) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L177)

<a id="op-f834b69c91e577"></a>
### Build dimensions dict for exc gain loss

`operation_enterprise_accounts_utils_business_behavior_build_dimensions_mapping_for_exception_gain_loss`

**Inputs** entry = no value, active\_dimensions = no value.

**Explicit results** dimensions\_dict.

**Local steps**

- Set dimensions\_dict from Platform.\_dict().
- If (entry and active\_dimensions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry → active\_dimensions.
  - For each dim in active\_dimensions.
    - If entry\_dimension bound to entry.get(dim.fieldname).
      - Set dimensions\_dict at dim.fieldname from entry\_dimension.
- Return dimensions\_dict.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0300.json#L5463) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1277) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L182)

<a id="op-61d1672267661e"></a>
### Reconcile against document

`operation_enterprise_accounts_utils_business_behavior_reconcile_against_document`

**Inputs** args, skip\_ref\_details\_update\_for\_pe = false, active\_dimensions = no value.

**Record and data access** resolve a document from voucher\_type via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set reconciled\_entries from mapping().
- For each row in args.
  - If not reconciled\_entries.get(tuple(row.voucher\_type, row.voucher\_no)).
    - Set reconciled\_entries at tuple(row.voucher\_type, row.voucher\_no) from list().
  - Evaluate reconciled\_entries at tuple(row.voucher\_type, row.voucher\_no).append(row).
- For each tuple(key, entries) in reconciled\_entries.items().
  - Set tuple(voucher\_type, voucher\_no) from key.
  - Set doc from Platform.get\_doc(voucher\_type, voucher\_no).
  - Set Platform.flags.ignore\_party\_validation from true.
  - Set reposting\_rows from list().
  - For each entry in entries.
    - Evaluate check\_if\_advance\_entry\_modified(entry).
    - Evaluate validate\_allocated\_amount(entry).
    - Set dimensions\_dict from \_build\_dimensions\_dict\_for\_exc\_gain\_loss(entry, active\_dimensions).
    - If voucher\_type equals “Journal Entry”.
      - Set referenced\_row from update\_reference\_in\_journal\_entry(entry, doc, do\_not\_save = false).
      - Evaluate entry.update(mapping(“referenced\_row” → referenced\_row.name)).
      - Evaluate doc.make\_exchange\_gain\_loss\_journal(list(entry), dimensions\_dict).
    - Otherwise.
      - Set referenced\_row from update\_reference\_in\_payment\_entry(entry, doc, do\_not\_save = true, skip\_ref\_details\_update\_for\_pe = skip\_ref\_details\_update\_for\_pe, dimensions\_dict = dimensions\_dict).
      - If (referenced\_row.get(“outstanding\_amount”) and entry.get(“outstanding\_amount”) is identical to no value).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in referenced\_row.get(“outstanding\_amount”) → entry.get(“outstanding\_amount”) is identical to no value.
        - Update referenced\_row.outstanding\_amount using − flt(entry.allocated\_amount).
      - Evaluate reposting\_rows.append(referenced\_row).
  - Evaluate doc.save(ignore\_permissions = true).
  - If (voucher\_type equals “Payment Entry” and doc.book\_advance\_payments\_in\_separate\_party\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in voucher\_type equals “Payment Entry” → doc.book\_advance\_payments\_in\_separate\_party\_account.
    - For each row in reposting\_rows.
      - Evaluate doc.make\_advance\_gl\_entries(entry = row).
  - Otherwise.
    - Evaluate \_delete\_pl\_entries(voucher\_type, voucher\_no).
    - Evaluate \_delete\_adv\_pl\_entries(voucher\_type, voucher\_no).
    - Set gl\_map from doc.build\_gl\_map().
    - Bind dependencies process\_debit\_credit\_difference.
    - Evaluate process\_debit\_credit\_difference(gl\_map).
    - Evaluate create\_payment\_ledger\_entry(gl\_map, update\_outstanding = “No”, cancel = 0, adv\_adj = 1).
  - For each entry in entries.
    - Evaluate update\_voucher\_outstanding(entry.against\_voucher\_type, entry.against\_voucher, entry.account, entry.party\_type, …).
  - Set Platform.flags.ignore\_party\_validation from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0300.json#L5662) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L239)
