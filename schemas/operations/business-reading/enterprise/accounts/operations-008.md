# Accounting and settlement · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Accounts receivable

<a id="op-d7a92103f9897a"></a>
### Receivable Payable Report.get permitted sales persons

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_permitted_sales_persons`

**Inputs** self, parenttype.

**Explicit results** no value · get\_allowed\_docs\_for\_doctype(permissions, parenttype).

**Local steps**

- If self.account\_type differs from “Receivable”.
  - Return no value.
- Set permissions from Platform.permissions.get\_user\_permissions(Platform.session.user).get(“Sales Person”, list()).
- If not permissions.
  - Return no value.
- Return get\_allowed\_docs\_for\_doctype(permissions, parenttype).

**Values supplied outside this operation** effective access from Platform.permissions.get\_user\_permissions(Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L995) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L580)

<a id="op-2e63a745d6cfe9"></a>
### Receivable Payable Report.get sales invoices or customers based on sales person

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_sales_invoices_or_customers_based_on_sales_person`

**Inputs** self.

**Record and data access** read “Sales Person” via get\_value.

**Explicit results** no value.

**Local steps**

- Set parenttypes from list(“Customer”, “Sales Invoice”).
- Set permitted from mapping of p → self.get\_permitted\_sales\_persons(p) for p drawn from parenttypes.
  - Draw p from parenttypes.
- If not (self.filters.get(“sales\_person”) or any(generator of p is distinct from no value for p drawn from permitted.values())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.filters.get(“sales\_person”) → any(generator of p is distinct from no value for p drawn from permitted.values()).
  - Draw p from permitted.values().
  - Return no value.
- Set steam from Platform.qb.DocType(“Sales Team”).
- Set scope from list().
- For each parenttype in parenttypes.
  - Set criterion from steam.parenttype equals parenttype.
  - If allowed bound to permitted at parenttype is distinct from no value.
    - Update criterion using bitwise and steam.sales\_person.isin((allowed or list(empty text))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in allowed → list(empty text).
  - Evaluate scope.append(criterion).
- Set conditions from list(Criterion.any(scope)).
- If self.filters.get(“sales\_person”).
  - Set tuple(lft, rgt) from Platform.db.get\_value(“Sales Person”, self.filters.get(“sales\_person”), list(“lft”, “rgt”)).
  - Set sp from Platform.qb.DocType(“Sales Person”).
  - Evaluate conditions.append(steam.sales\_person.isin(nested operand in the contract(nested operand in the contract).select(sp.name).where((sp.lft ≥ lft bitwise and sp.rgt ≤ rgt)))).
- Set records from nested operand in the contract(nested operand in the contract, nested operand in the contract).distinct().where(Criterion.all(conditions)).run(as\_dict = 1).
- Set self.sales\_person\_records from Platform.\_dict().
- For each d in records.
  - Evaluate self.sales\_person\_records.setdefault(d.parenttype, set()).add(d.parent).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permitted sales persons](operations-008.md#op-d7a92103f9897a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L1179) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L582)

<a id="op-297ec549d920ca"></a>
### Receivable Payable Report.get invoices based on sales partner

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_invoices_based_on_sales_partner`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_all.

**Explicit results** no value.

**Local steps**

- If not self.filters.get(“sales\_partner”).
  - Return no value.
- Set self.sales\_partner\_invoices from set(Platform.get\_all(“Sales Invoice”, filters = mapping(“sales\_partner” → self.filters.get(“sales\_partner”), “docstatus” → 1, “company” → self.filters.company), pluck = “name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L2187) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L208) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L577)

<a id="op-a19fa26835c104"></a>
### Receivable Payable Report.prepare conditions

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_prepare_conditions`

**Inputs** self.

**Local steps**

- Set self.qb\_selection\_filter from list().
- Set self.or\_filters from list().
- For each \_party\_type in self.party\_type.
  - Evaluate self.add\_common\_filters().
  - If self.account\_type equals “Receivable”.
    - Evaluate self.add\_customer\_filters().
    - Evaluate self.exclude\_employee\_transaction().
  - Otherwise.
    - If self.account\_type equals “Payable”.
      - Evaluate self.add\_supplier\_filters().
- If self.filters.cost\_center.
  - Evaluate self.get\_cost\_center\_conditions().
- If self.filters.project.
  - Evaluate self.qb\_selection\_filter.append(self.ple.project.isin(self.filters.project)).
- Evaluate self.add\_user\_permission\_filters().
- Evaluate self.add\_accounting\_dimensions\_filters().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add common filters](operations-008.md#op-31f9f9cec7d97f), [add customer filters](operations-008.md#op-bbff1b1f7a81ed), [exclude employee transaction](operations-008.md#op-02fba46d6737c3), [add supplier filters](operations-008.md#op-bcb23f40dd2e65), [get cost center conditions](operations-008.md#op-eb68a237f7a124), [add user permission filters](operations-008.md#op-3af90c8978ab67), [add accounting dimensions filters](operations-008.md#op-5734fbb86fb7c8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L2421) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L219) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L588)

<a id="op-3af90c8978ab67"></a>
### Receivable Payable Report.add user permission filters

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_user_permission_filters`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self.

**Explicit result forms** no value.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L2794) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L551)

<a id="op-eb68a237f7a124"></a>
### Receivable Payable Report.get cost center conditions

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_cost_center_conditions`

**Inputs** self.

**Local steps**

- Set cost\_center\_list from get\_cost\_centers\_with\_children(self.filters.cost\_center).
- Evaluate self.qb\_selection\_filter.append(self.ple.cost\_center.isin(cost\_center\_list)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L3059) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L568)

<a id="op-31f9f9cec7d97f"></a>
### Receivable Payable Report.add common filters

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_common_filters`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Local steps**

- If self.filters.company.
  - Evaluate self.qb\_selection\_filter.append(self.ple.company equals self.filters.company).
- If self.filters.finance\_book.
  - Evaluate self.qb\_selection\_filter.append(self.ple.finance\_book equals self.filters.finance\_book).
- If self.filters.get(“party\_type”).
  - Evaluate self.qb\_selection\_filter.append(self.filters.party\_type equals self.ple.party\_type).
- If self.filters.get(“party”).
  - Evaluate self.qb\_selection\_filter.append(self.ple.party.isin(self.filters.party)).
- If self.filters.party\_account.
  - Evaluate self.qb\_selection\_filter.append(self.ple.account equals self.filters.party\_account).
- Otherwise.
  - Set accounts from list of d.name for d drawn from Platform.get\_all(“Account”, filters = mapping(“account\_type” → self.account\_type, “company” → self.filters.company)).
    - Draw d from Platform.get\_all(“Account”, filters = mapping(“account\_type” → self.account\_type, “company” → self.filters.company)).
  - If accounts.
    - Evaluate self.qb\_selection\_filter.append(self.ple.account.isin(accounts)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L3177) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L547)

<a id="op-bbff1b1f7a81ed"></a>
### Receivable Payable Report.add customer filters

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_customer_filters`

**Inputs** self.

**Local steps**

- Set self.customer from qb.DocType(“Customer”).
- If self.filters.get(“customer\_group”).
  - Set groups from get\_party\_group\_with\_children(“Customer”, self.filters.customer\_group).
  - Set customers from qb.from\_(self.customer).select(self.customer.name).where(self.customer at “customer\_group”.isin(groups)).
  - Evaluate self.qb\_selection\_filter.append(self.ple.party.isin(customers)).
- If self.filters.get(“territory”).
  - Set territories from get\_nested\_set\_children(“Territory”, self.filters.territory).
  - Set customers from qb.from\_(self.customer).select(self.customer.name).where(self.customer at “territory”.isin(territories)).
  - Evaluate self.qb\_selection\_filter.append(self.ple.party.isin(customers)).
- If self.filters.get(“payment\_terms\_template”).
  - Set customer\_ptt from self.ple.party.isin(nested operand in the contract.from\_(nested operand in the contract.customer).select(self.customer.name).where(self.customer.payment\_terms equals self.filters.get(“payment\_terms\_template”))).
  - Set si\_ptt from self.add\_payment\_term\_template\_filters(“Sales Invoice”).
  - Set sales\_ptt from self.ple.against\_voucher\_no.isin(si\_ptt).
  - Evaluate self.qb\_selection\_filter.append(Criterion.any(list(customer\_ptt, sales\_ptt))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add payment term template filters](operations-008.md#op-66946e2ceaed78).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L3783) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L548)

<a id="op-02fba46d6737c3"></a>
### Receivable Payable Report.exclude employee transaction

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_exclude_employee_transaction`

**Inputs** self.

**Local steps**

- Evaluate self.qb\_selection\_filter.append(self.ple.party\_type differs from “Employee”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L4617) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L562)

<a id="op-bcb23f40dd2e65"></a>
### Receivable Payable Report.add supplier filters

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_supplier_filters`

**Inputs** self.

**Local steps**

- Set supplier from qb.DocType(“Supplier”).
- If self.filters.get(“supplier\_group”).
  - Set groups from get\_party\_group\_with\_children(“Supplier”, self.filters.supplier\_group).
  - Evaluate self.qb\_selection\_filter.append(self.ple.party.isin(nested operand in the contract(nested operand in the contract).select(supplier.name).where(supplier.supplier\_group.isin(groups)))).
- If self.filters.get(“payment\_terms\_template”).
  - Set supplier\_ptt from self.ple.party.isin(nested operand in the contract.from\_(supplier).select(supplier.name).where(supplier.payment\_terms equals self.filters.get(“payment\_terms\_template”))).
  - Set pi\_ptt from self.add\_payment\_term\_template\_filters(“Purchase Invoice”).
  - Set purchase\_ptt from self.ple.against\_voucher\_no.isin(pi\_ptt).
  - Evaluate self.qb\_selection\_filter.append(Criterion.any(list(supplier\_ptt, purchase\_ptt))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add payment term template filters](operations-008.md#op-66946e2ceaed78).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L4700) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L550)

<a id="op-66946e2ceaed78"></a>
### Receivable Payable Report.add payment term template filters

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_payment_term_template_filters`

**Inputs** self, dtype.

**Explicit results** ptt.

**Local steps**

- Set voucher\_type from qb.DocType(dtype).
- Set ptt from nested operand in the contract(nested operand in the contract).select(voucher\_type.name).where(voucher\_type.payment\_terms\_template equals nested operand in the contract.filters.get(“payment\_terms\_template” ….
- If dtype equals “Purchase Invoice”.
  - Set party from “Supplier”.
  - Set party\_group\_type from “supplier\_group”.
  - Set acc\_type from “credit\_to”.
- Otherwise.
  - Set party from “Customer”.
  - Set party\_group\_type from “customer\_group”.
  - Set acc\_type from “debit\_to”.
- If self.filters.get(party\_group\_type).
  - Set party\_groups from get\_party\_group\_with\_children(party, self.filters.get(party\_group\_type)).
  - Set ptt from ptt.where(voucher\_type at party\_group\_type.isin(party\_groups)).
- If self.filters.party.
  - Set ptt from ptt.where(voucher\_type at party.lower().isin(self.filters.party)).
- If self.filters.cost\_center.
  - Set cost\_centers from get\_cost\_centers\_with\_children(self.filters.cost\_center).
  - Set ptt from ptt.where(voucher\_type.cost\_center.isin(cost\_centers)).
- If self.filters.party\_account.
  - Set ptt from ptt.where(voucher\_type at acc\_type equals self.filters.party\_account).
- Return ptt.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L5255) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L549)

<a id="op-5734fbb86fb7c8"></a>
### Receivable Payable Report.add accounting dimensions filters

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_accounting_dimensions_filters`

**Inputs** self.

**Record and data access** read “DocType” via get\_cached\_value.

**Local steps**

- Set accounting\_dimensions from get\_accounting\_dimensions(as\_list = false).
- If accounting\_dimensions.
  - For each dimension in accounting\_dimensions.
    - If self.filters.get(dimension.fieldname).
      - If Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).
        - Set self.filters at dimension.fieldname from get\_dimension\_with\_children(dimension.document\_type, self.filters.get(dimension.fieldname)).
        - Evaluate self.qb\_selection\_filter.append(self.ple at dimension.fieldname.isin(self.filters at dimension.fieldname)).
      - Otherwise.
        - Evaluate self.qb\_selection\_filter.append(self.ple at dimension.fieldname.isin(self.filters at dimension.fieldname)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, dimension.document\_type, “is\_tree”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L6005) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L545)

<a id="op-f326344dc15de6"></a>
### Receivable Payable Report.is return

`operation_enterprise_binding_enterprise_accounts_report_accounts_receivable_accounts_receivable_receivablepayablereport_is_return`

**Inputs** self, ple.

**Explicit results** (self.invoice\_details.get(ple.voucher\_no) or mapping()).get(“is\_return”).

**Local steps**

- Return (self.invoice\_details.get(ple.voucher\_no) or mapping()).get(“is\_return”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.invoice\_details.get(ple.voucher\_no) → mapping().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1112)

<a id="op-9338432b038ecb"></a>
### Receivable Payable Report.is invoice

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_is_invoice`

**Inputs** self, ple.

**Explicit results** true.

**Local steps**

- If ple.voucher\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Return true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L6395) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L218) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L587)

<a id="op-5ddbb4d1bd4eb1"></a>
### Receivable Payable Report.get party details

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_party_details`

**Inputs** self, party.

**Record and data access** read “Customer” via get\_value · read “Supplier” via get\_value.

**Explicit results** self.party\_details at party.

**Local steps**

- If party does not belong to self.party\_details.
  - If self.account\_type equals “Receivable”.
    - Set fields from list(“customer\_name”, “territory”, “customer\_group”, “customer\_primary\_contact”).
    - Set self.party\_details at party from Platform.db.get\_value(“Customer”, party, fields, as\_dict = true).
  - Otherwise.
    - Set self.party\_details at party from Platform.db.get\_value(“Supplier”, party, list(“supplier\_name”, “supplier\_group”), as\_dict = true).
- Return self.party\_details at party.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0218.json#L6484) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L578)

<a id="op-1515b81fcf1192"></a>
### Receivable Payable Report.get columns

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- Evaluate self.add\_column(translated “Posting Date”, fieldname = “posting\_date”, fieldtype = “Date”).
- Evaluate self.add\_column(label = translated “Party Type”, fieldname = “party\_type”, fieldtype = “Link”, options = “DocType”, …).
- Evaluate self.add\_column(label = translated “Party”, fieldname = “party”, fieldtype = “Dynamic Link”, options = “party\_type”, …).
- If self.account\_type equals “Receivable”.
  - Set label from translated “Receivable Account”.
- Otherwise.
  - If self.account\_type equals “Payable”.
    - Set label from translated “Payable Account”.
  - Otherwise.
    - Set label from translated “Party Account”.
- Evaluate self.add\_column(label = label, fieldname = “party\_account”, fieldtype = “Link”, options = “Account”, …).
- If self.party\_naming\_by equals “Naming Series”.
  - If self.account\_type equals “Payable”.
    - Set label from translated “Supplier Name”.
    - Set fieldname from “supplier\_name”.
  - Otherwise.
    - Set label from translated “Customer Name”.
    - Set fieldname from “customer\_name”.
  - Evaluate self.add\_column(label = label, fieldname = fieldname, fieldtype = “Data”, sticky = true).
- If self.account\_type equals “Receivable”.
  - Evaluate self.add\_column(translated “Customer Contact”, fieldname = “customer\_primary\_contact”, fieldtype = “Link”, options = “Contact”).
- Evaluate self.add\_column(label = translated “Cost Center”, fieldname = “cost\_center”, fieldtype = “Data”).
- Evaluate self.add\_column(label = translated “Project”, fieldname = “project”, fieldtype = “Link”, options = “Project”).
- Evaluate self.add\_column(label = translated “Voucher Type”, fieldname = “voucher\_type”, fieldtype = “Link”, options = “DocType”).
- Evaluate self.add\_column(label = translated “Voucher No”, fieldname = “voucher\_no”, fieldtype = “Dynamic Link”, options = “voucher\_type”, …).
- Evaluate self.add\_column(label = translated “Due Date”, fieldname = “due\_date”, fieldtype = “Date”).
- If self.account\_type equals “Payable”.
  - Evaluate self.add\_column(label = translated “Bill No”, fieldname = “bill\_no”, fieldtype = “Data”).
  - Evaluate self.add\_column(label = translated “Bill Date”, fieldname = “bill\_date”, fieldtype = “Date”).
- If self.filters.based\_on\_payment\_terms.
  - Evaluate self.add\_column(label = translated “Payment Term”, fieldname = “payment\_term”, fieldtype = “Data”).
  - Evaluate self.add\_column(label = translated “Invoice Grand Total”, fieldname = “invoice\_grand\_total”).
- Evaluate self.add\_column(translated “Invoiced Amount”, fieldname = “invoiced”).
- Evaluate self.add\_column(translated “Paid Amount”, fieldname = “paid”).
- If self.account\_type equals “Receivable”.
  - Evaluate self.add\_column(translated “Credit Note”, fieldname = “credit\_note”).
- Otherwise.
  - Evaluate self.add\_column(translated “Debit Note”, fieldname = “credit\_note”).
- Evaluate self.add\_column(translated “Outstanding Amount”, fieldname = “outstanding”).
- Evaluate self.add\_column(label = translated “Age (Days)”, fieldname = “age”, fieldtype = “Int”, width = 80).
- Evaluate self.setup\_ageing\_columns().
- Evaluate self.add\_column(label = translated “Currency”, fieldname = “currency”, fieldtype = “Link”, options = “Currency”, …).
- If self.filters.show\_future\_payments.
  - Evaluate self.add\_column(label = translated “Future Payment Ref”, fieldname = “future\_ref”, fieldtype = “Data”).
  - Evaluate self.add\_column(label = translated “Future Payment Amount”, fieldname = “future\_amount”).
  - Evaluate self.add\_column(label = translated “Remaining Balance”, fieldname = “remaining\_balance”).
- If self.filters.account\_type equals “Receivable”.
  - Evaluate self.add\_column(label = translated “Customer LPO”, fieldname = “po\_no”, fieldtype = “Data”).
  - If self.filters.show\_delivery\_notes.
    - Evaluate self.add\_column(label = translated “Delivery Notes”, fieldname = “delivery\_notes”, fieldtype = “Data”).
  - Evaluate self.add\_column(label = translated “Territory”, fieldname = “territory”, fieldtype = “Link”, options = “Territory”).
  - Evaluate self.add\_column(label = translated “Customer Group”, fieldname = “customer\_group”, fieldtype = “Link”, options = “Customer Group”).
  - If self.filters.show\_sales\_person.
    - Evaluate self.add\_column(label = translated “Sales Person”, fieldname = “sales\_person”, fieldtype = “Data”).
  - If self.filters.sales\_partner.
    - Evaluate self.add\_column(label = translated “Sales Partner”, fieldname = “sales\_partner”, fieldtype = “Data”).
- If self.filters.account\_type equals “Payable”.
  - Evaluate self.add\_column(label = translated “Supplier Group”, fieldname = “supplier\_group”, fieldtype = “Link”, options = “Supplier Group”).
- If self.filters.show\_remarks.
  - Evaluate self.add\_column(label = translated “Remarks”, fieldname = “remarks”, fieldtype = “Text”, width = 200).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-008.md#op-08ff76d475a135), [setup ageing columns](operations-008.md#op-09d37f34e6b6a2).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L567)

<a id="op-08ff76d475a135"></a>
### Receivable Payable Report.add column

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_add_column`

**Inputs** self, label, fieldname = no value, fieldtype = “Currency”, options = no value, width = 120, sticky = false.

**Local steps**

- If not fieldname.
  - Set fieldname from scrub(label).
- If fieldtype equals “Currency”.
  - Set options from “currency”.
- If fieldtype equals “Date”.
  - Set width from 90.
- Evaluate self.columns.append(dict(label = label, fieldname = fieldname, fieldtype = fieldtype, options = options, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0219.json#L2974) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L546)

<a id="op-09d37f34e6b6a2"></a>
### Receivable Payable Report.setup ageing columns

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_setup_ageing_columns`

**Inputs** self.

**Local steps**

- Set self.ageing\_column\_labels from list().
- Set ranges from list(expanded self.ranges, translated “Above”).
- Set prev\_range\_value from 0.
- Evaluate self.add\_column(label = translated “&lt;0”, fieldname = “range0”, fieldtype = “Currency”).
- Evaluate self.ageing\_column\_labels.append(translated “&lt;0”).
- For each tuple(idx, curr\_range\_value) in enumerate(ranges).
  - Set label from formatted text {prev\_range\_value}-{curr\_range\_value}.
  - Evaluate self.add\_column(label = label, fieldname = (“range” + str((idx + 1)))).
  - Evaluate self.ageing\_column\_labels.append(label).
  - If curr\_range\_value.isdigit().
    - Set prev\_range\_value from (cint(curr\_range\_value) + 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add column](operations-008.md#op-08ff76d475a135).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0219.json#L3281) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L596)

<a id="op-9de576d7c57741"></a>
### Receivable Payable Report.get chart data

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_chart_data`

**Inputs** self.

**Local steps**

- Set precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set rows from list().
- For each row in self.data.
  - Set row from Platform.\_dict(row).
  - If not cint(row.bold).
    - Set values from (list(flt(row.get(“range0”, 0), precision)) + list of flt(row.get(formatted text range{i}, 0), precision) for i drawn from self.range\_numbers).
      - Draw i from self.range\_numbers.
    - Evaluate rows.append(mapping(“values” → values)).
- Set self.chart from mapping(“data” → mapping(“labels” → self.ageing\_column\_labels, “datasets” → rows), “type” → “percentage”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0219.json#L3726) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L566)

<a id="op-a842dce1e18780"></a>
### Receivable Payable Report.get exchange rate revaluations

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_receivable_payable_report_get_exchange_rate_revaluations`

**Inputs** self.

**Local steps**

- Set je from qb.DocType(“Journal Entry”).
- Set results from nested operand in the contract(nested operand in the contract).select(je.name).where(((nested operand in the contract.company equals nested operand in the contract.company bitwise and nested operand in the ….run().
- Set self.err\_journals from list of x at 0 for x drawn from results when results, otherwise list().
  - Value choice on results — true gives list of x at 0 for x drawn from results, false gives list().
  - Draw x from results.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0219.json#L4168) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L202) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L571)

<a id="op-9788eb196f4b7f"></a>
### Get party group with children

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_get_party_group_with_children`

**Inputs** party, party\_groups.

**Explicit results** list() · get\_nested\_set\_children(formatted text {party} Group, party\_groups).

**Local steps**

- If party does not belong to tuple(“Customer”, “Supplier”).
  - Return list().
- Return get\_nested\_set\_children(formatted text {party} Group, party\_groups).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0219.json#L4477) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L544)

<a id="op-04ab759bfb4b32"></a>
### Get nested set children

`operation_enterprise_accounts_report_accounts_receivable_business_behavior_get_nested_set_children`

**Inputs** doctype, values.

**Record and data access** read doctype via exists · read doctype via get\_value · read doctype via get\_all.

**Explicit results** list(set(all\_values)).

**Explicit failure paths** validation helper — translated “Please select a valid {0}”.format(translated doctype) · validation helper — translated “{0}: {1} does not exist”.format(doctype, d).

**Local steps**

- If not isinstance(values, list).
  - Set values from list of d.strip() for d drawn from values.split(“,”) where d.strip().
    - Draw d from values.split(“,”), keep a combination only if (d.strip()).
- If not values.
  - Call the validation error handler Platform.throw(translated “Please select a valid {0}”.format(translated doctype)).
- Set all\_values from list().
- For each d in values.
  - If Platform.db.exists(doctype, d).
    - Set tuple(lft, rgt) from Platform.db.get\_value(doctype, d, list(“lft”, “rgt”)).
    - Set children from Platform.get\_all(doctype, filters = mapping(“lft” → list(“&gt;=”, lft), “rgt” → list(“&lt;=”, rgt)), pluck = “name”).
    - Update all\_values using + children.
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “{0}: {1} does not exist”.format(doctype, d)).
- Return list(set(all\_values)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0219.json#L4604) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L543)

## Report · Accounts receivable summary

<a id="op-fa391d2917c012"></a>
### Execute

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** AccountsReceivableSummary(filters).run(args).

**Local steps**

- Set args from mapping(“account\_type” → “Receivable”, “naming\_by” → list(“Selling Settings”, “cust\_master\_name”)).
- Return AccountsReceivableSummary(filters).run(args).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0223.json#L4103) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L236) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L605)

<a id="op-603863b2fba346"></a>
### Accounts Receivable Summary.run

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_accounts_receivable_summary_run`

**Inputs** self, args.

**Record and data access** read args.get(“naming\_by”) at 0 via get\_single\_value.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Set self.account\_type from args.get(“account\_type”).
- Set self.party\_type from get\_party\_types\_from\_account\_type(self.account\_type).
- Set self.party\_naming\_by from Platform.db.get\_single\_value(args.get(“naming\_by”) at 0, args.get(“naming\_by”) at 1).
- Evaluate self.get\_columns().
- Evaluate self.get\_data(args).
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [get columns](operations-009.md#op-dbfcdbbffcc13b), [get data](operations-009.md#op-4831fc268dcb5e).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(args.get(“naming\_by”) at 0, args.get(“naming\_by”) at 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0223.json#L4232) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L603)
