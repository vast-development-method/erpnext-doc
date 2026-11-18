# Accounting and settlement · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Accounts receivable summary

<a id="op-4831fc268dcb5e"></a>
### Accounts Receivable Summary.get data

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_accounts_receivable_summary_get_data`

**Inputs** self, args.

**Record and data access** read doctype via get\_cached\_value.

**Local steps**

- Set self.data from list().
- Set self.receivables from ReceivablePayableReport(self.filters).run(args) at 1.
- Set self.currency\_precision from (get\_currency\_precision() or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_currency\_precision() → 2.
- Evaluate self.get\_party\_total(args).
- If self.filters.show\_gl\_balance.
  - Set gl\_balance\_map from self.get\_gl\_balance().
- For each tuple(party, party\_dict) in self.party\_total.items().
  - If flt(party\_dict.outstanding, self.currency\_precision) equals 0.
    - Continue with the next iteration or loop test.
  - Set row from Platform.\_dict().
  - Set row.party from party.
  - If self.party\_naming\_by equals “Naming Series”.
    - If self.account\_type equals “Payable”.
      - Set doctype from “Supplier”.
      - Set fieldname from “supplier\_name”.
    - Otherwise.
      - Set doctype from “Customer”.
      - Set fieldname from “customer\_name”.
    - Set row.party\_name from Platform.get\_cached\_value(doctype, party, fieldname).
  - Evaluate row.update(party\_dict).
  - Set row.advance from self.party\_advance.get(party, 0).
  - Update row.paid using − row.advance.
  - If self.filters.show\_gl\_balance.
    - Set row.gl\_balance from gl\_balance\_map.get(party).
    - Set row.diff from (flt(row.outstanding) − flt(row.gl\_balance)).
  - If self.filters.show\_future\_payments.
    - Set row.remaining\_balance from (flt(row.outstanding) − flt(row.future\_amount)).
  - Evaluate self.data.append(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get party total](operations-009.md#op-1156659d70bf2c), [get gl balance](operations-009.md#op-45c585b3914604).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(doctype, party, fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L600)

<a id="op-1156659d70bf2c"></a>
### Accounts Receivable Summary.get party total

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_accounts_receivable_summary_get_party_total`

**Inputs** self, args.

**Local steps**

- Set self.party\_total from Platform.\_dict().
- Set self.party\_advance from Platform.\_dict().
- Set invoice\_doctypes from Platform.get\_hooks(“invoice\_doctypes”).
- For each d in self.receivables.
  - Evaluate self.init\_party\_total(d).
  - For each k in list(self.party\_total at d.party).
    - If isinstance(self.party\_total at d.party at k, float).
      - Update self.party\_total at d.party at k using + (d.get(k) or 0.0).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(k) → 0.0.
  - If d.voucher\_type does not belong to invoice\_doctypes.
    - Evaluate self.party\_advance.setdefault(d.party, 0.0).
    - Update self.party\_advance at d.party using + self.get\_unallocated\_credit(d).
  - Evaluate self.set\_party\_details(d).

If control reaches the end, it returns no value.

**Methods declared on this owner** [init party total](operations-009.md#op-9c52f62c57ac70), [get unallocated credit](operations-009.md#op-c62e2d838f9a39), [set party details](operations-009.md#op-fc421f95b53f1b).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“invoice\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L601)

<a id="op-c62e2d838f9a39"></a>
### Accounts Receivable Summary.get unallocated credit

`operation_enterprise_binding_enterprise_accounts_report_accounts_receivable_summary_accounts_receivable_summary_accountsreceivablesummary_get_unallocated_credit`

**Inputs** self, row.

**Declared result** float.

**Explicit results** max((flt(row.paid) − flt(row.invoiced)), 0.0).

**Local steps**

- Return max((flt(row.paid) − flt(row.invoiced)), 0.0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1115)

<a id="op-9c52f62c57ac70"></a>
### Accounts Receivable Summary.init party total

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_accounts_receivable_summary_initialize_party_total`

**Inputs** self, row.

**Local steps**

- Set default\_dict from mapping(“invoiced” → 0.0, “paid” → 0.0, “credit\_note” → 0.0, “outstanding” → 0.0, …).
- For each i in list(0, expanded self.range\_numbers).
  - Set range\_key from formatted text range{i}.
  - Set default\_dict at range\_key from 0.0.
- Evaluate self.party\_total.setdefault(row.party, Platform.\_dict(default\_dict)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L602)

<a id="op-fc421f95b53f1b"></a>
### Accounts Receivable Summary.set party details

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_accounts_receivable_summary_set_party_details`

**Inputs** self, row.

**Local steps**

- Set self.party\_total at row.party.currency from row.currency.
- For each key in tuple(“territory”, “customer\_group”, “supplier\_group”).
  - If row.get(key).
    - Set self.party\_total at row.party at key from row.get(key, empty text).
- If row.sales\_person.
  - Evaluate self.party\_total at row.party.sales\_person.append(row.get(“sales\_person”, empty text)).
- If (self.filters.sales\_partner and row.get(“sales\_partner”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.sales\_partner → row.get(“sales\_partner”).
  - Set self.party\_total at row.party at “sales\_partner” from row.get(“sales\_partner”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0223.json#L6107) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L604)

<a id="op-dbfcdbbffcc13b"></a>
### Accounts Receivable Summary.get columns

`operation_enterprise_accounts_report_accounts_receivable_summary_business_behavior_accounts_receivable_summary_get_columns`

**Inputs** self.

**Local steps**

- Set self.columns from list().
- Evaluate self.add\_column(label = translated “Party Type”, fieldname = “party\_type”, fieldtype = “Link”, options = “DocType”, …).
- Evaluate self.add\_column(label = translated “Party”, fieldname = “party”, fieldtype = “Dynamic Link”, options = “party\_type”, …).
- If self.party\_naming\_by equals “Naming Series”.
  - Evaluate self.add\_column(label = translated “Supplier Name” when self.account\_type equals “Payable”, otherwise translated “Customer Name”, fieldname = “party\_name”, fieldtype = “Data”).
    - Value choice on self.account\_type equals “Payable” — true gives translated “Supplier Name”, false gives translated “Customer Name”.
- Set credit\_debit\_label from “Credit Note” when self.account\_type equals “Receivable”, otherwise “Debit Note”.
  - Value choice on self.account\_type equals “Receivable” — true gives “Credit Note”, false gives “Debit Note”.
- Evaluate self.add\_column(translated “Advance Amount”, fieldname = “advance”).
- Evaluate self.add\_column(translated “Invoiced Amount”, fieldname = “invoiced”).
- Evaluate self.add\_column(translated “Paid Amount”, fieldname = “paid”).
- Evaluate self.add\_column(translated credit\_debit\_label, fieldname = “credit\_note”).
- Evaluate self.add\_column(translated “Outstanding Amount”, fieldname = “outstanding”).
- If self.filters.show\_gl\_balance.
  - Evaluate self.add\_column(translated “GL Balance”, fieldname = “gl\_balance”).
  - Evaluate self.add\_column(translated “Difference”, fieldname = “diff”).
- Evaluate self.setup\_ageing\_columns().
- Evaluate self.add\_column(label = translated “Total Amount Due”, fieldname = “total\_due”).
- If self.filters.show\_future\_payments.
  - Evaluate self.add\_column(label = translated “Future Payment Amount”, fieldname = “future\_amount”).
  - Evaluate self.add\_column(label = translated “Remaining Balance”, fieldname = “remaining\_balance”).
- If self.account\_type equals “Receivable”.
  - Evaluate self.add\_column(label = translated “Territory”, fieldname = “territory”, fieldtype = “Link”, options = “Territory”).
  - Evaluate self.add\_column(label = translated “Customer Group”, fieldname = “customer\_group”, fieldtype = “Link”, options = “Customer Group”).
  - If self.filters.show\_sales\_person.
    - Evaluate self.add\_column(label = translated “Sales Person”, fieldname = “sales\_person”, fieldtype = “Data”).
  - If self.filters.sales\_partner.
    - Evaluate self.add\_column(label = translated “Sales Partner”, fieldname = “sales\_partner”, fieldtype = “Data”).
- Otherwise.
  - Evaluate self.add\_column(label = translated “Supplier Group”, fieldname = “supplier\_group”, fieldtype = “Link”, options = “Supplier Group”).
- Evaluate self.add\_column(label = translated “Currency”, fieldname = “currency”, fieldtype = “Link”, options = “Currency”, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L599)

<a id="op-45c585b3914604"></a>
### Accounts Receivable Summary.get gl balance

`operation_enterprise_binding_enterprise_accounts_report_accounts_receivable_summary_accounts_receivable_summary_accountsreceivablesummary_get_gl_balance`

**Inputs** self.

**Declared result** Platform.\_dict.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Set balance from (gle.credit − gle.debit) when self.account\_type equals “Payable”, otherwise (gle.debit − gle.credit).
  - Value choice on self.account\_type equals “Payable” — true gives (gle.credit − gle.debit), false gives (gle.debit − gle.credit).
- Set query from nested operand in the contract(nested operand in the contract).select(gle.party, Sum(balance)).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operan ….
- If self.filters.cost\_center.
  - Set query from query.where(gle.cost\_center.isin(get\_cost\_centers\_with\_children(self.filters.cost\_center))).
- Return Platform.\_dict(query.run()).

**Methods declared on this owner** [get party accounts](operations-009.md#op-5b545470af913b).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1113)

<a id="op-5b545470af913b"></a>
### Accounts Receivable Summary.get party accounts

`operation_enterprise_binding_enterprise_accounts_report_accounts_receivable_summary_accounts_receivable_summary_accountsreceivablesummary_get_party_accounts`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “Account” via get\_all.

**Explicit results** list(self.filters.party\_account) · Platform.get\_all(“Account”, filters = mapping(“account\_type” → self.account\_type, “company” → self.filters.company), pluck = “name”).

**Local steps**

- If self.filters.party\_account.
  - Return list(self.filters.party\_account).
- Return Platform.get\_all(“Account”, filters = mapping(“account\_type” → self.account\_type, “company” → self.filters.company), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1114)

## Record · Accounts settings

[Record definition](../../../../data/record-types/accounts_settings.json)

<a id="op-cf77f667a1d7a3"></a>
### Accounts Settings.validate

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_accounts_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_auto\_tax\_settings().
- Set old\_doc from self.get\_doc\_before\_save().
- Set clear\_cache from false.
- If old\_doc.add\_taxes\_from\_item\_tax\_template differs from self.add\_taxes\_from\_item\_tax\_template.
  - Evaluate Platform.db.set\_default(“add\_taxes\_from\_item\_tax\_template”, self.get(“add\_taxes\_from\_item\_tax\_template”, 0)).
  - Set clear\_cache from true.
- If old\_doc.enable\_common\_party\_accounting differs from self.enable\_common\_party\_accounting.
  - Evaluate Platform.db.set\_default(“enable\_common\_party\_accounting”, self.get(“enable\_common\_party\_accounting”, 0)).
  - Set clear\_cache from true.
- Evaluate self.validate\_stale\_days().
- If old\_doc.show\_payment\_schedule\_in\_print differs from self.show\_payment\_schedule\_in\_print.
  - Evaluate self.enable\_payment\_schedule\_in\_print().
- If old\_doc.enable\_accounting\_dimensions differs from self.enable\_accounting\_dimensions.
  - Evaluate toggle\_accounting\_dimension\_sections(not self.enable\_accounting\_dimensions).
  - Set clear\_cache from true.
- If old\_doc.enable\_discounts\_and\_margin differs from self.enable\_discounts\_and\_margin.
  - Evaluate toggle\_sales\_discount\_section(not self.enable\_discounts\_and\_margin).
  - Set clear\_cache from true.
- If old\_doc.enable\_loyalty\_point\_program differs from self.enable\_loyalty\_point\_program.
  - Evaluate toggle\_loyalty\_point\_program\_section(not self.enable\_loyalty\_point\_program).
  - Set clear\_cache from true.
- If old\_doc.enable\_subscription differs from self.enable\_subscription.
  - Evaluate toggle\_subscription\_sections(not self.enable\_subscription).
  - Set clear\_cache from true.
- If old\_doc.enable\_overdue\_billing\_threshold differs from self.enable\_overdue\_billing\_threshold.
  - Evaluate toggle\_overdue\_billing\_threshold\_field(not self.enable\_overdue\_billing\_threshold).
  - Set clear\_cache from true.
- If clear\_cache.
  - Evaluate Platform.clear\_cache().
- Evaluate self.validate\_and\_sync\_auto\_reconcile\_config().
- Evaluate self.update\_property\_for\_accounting\_dimension().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate auto tax settings](operations-009.md#op-5317e168121c49), [validate stale days](operations-009.md#op-41804540fbc480), [enable payment schedule in print](operations-009.md#op-1dde23cb7efe21), [validate and sync auto reconcile config](operations-009.md#op-224a4dde68f23a), [update property for accounting dimension](operations-009.md#op-09d60136af8d5f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L3385) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L214)

<a id="op-41804540fbc480"></a>
### Accounts Settings.validate stale days

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_accounts_settings_validate_stale_days`

**Inputs** self.

**State and service calls** msgprint with translated “Stale Days should start from 1.”.

**Local steps**

- If (not self.allow\_stale and cint(self.stale\_days) ≤ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.allow\_stale → cint(self.stale\_days) ≤ 0.
  - Evaluate Platform.msgprint(translated “Stale Days should start from 1.”, title = “Error”, indicator = “red”, raise\_exception = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L4178) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L227) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L217)

<a id="op-1dde23cb7efe21"></a>
### Accounts Settings.enable payment schedule in print

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_accounts_settings_enable_payment_schedule_in_print`

**Inputs** self.

**Local steps**

- Set show\_in\_print from cint(self.show\_payment\_schedule\_in\_print).
- For each doctype in tuple(“Sales Order”, “Sales Invoice”, “Purchase Order”, “Purchase Invoice”).
  - Evaluate make\_property\_setter(doctype, “due\_date”, “print\_hide”, show\_in\_print, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “payment\_schedule”, “print\_hide”, 0 when show\_in\_print, otherwise 1, validate\_fields\_for\_doctype = false, …).
    - Value choice on show\_in\_print — true gives 0, false gives 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L4337) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L212)

<a id="op-224a4dde68f23a"></a>
### Accounts Settings.validate and sync auto reconcile config

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_accounts_settings_validate_and_sync_auto_reconcile_configuration`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cron Interval should be between 1 and 59 Min” · validation helper — translated “Queue Size should be between 5 and 100”.

**Local steps**

- Set interval\_changed from self.has\_value\_changed(“auto\_reconciliation\_job\_trigger”).
- If (interval\_changed and not 0 &lt; cint(self.auto\_reconciliation\_job\_trigger) &lt; 60).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in interval\_changed → not 0 &lt; cint(self.auto\_reconciliation\_job\_trigger) &lt; 60.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 &lt; cint(self.auto\_reconciliation\_job\_trigger) &lt; 60.
  - Call the validation error handler Platform.throw(translated “Cron Interval should be between 1 and 59 Min”).
- If self.auto\_reconcile\_payments.
  - Evaluate sync\_auto\_reconcile\_config(self.auto\_reconciliation\_job\_trigger).
- If self.has\_value\_changed(“reconciliation\_queue\_size”).
  - If (cint(self.reconciliation\_queue\_size) &lt; 5 or cint(self.reconciliation\_queue\_size) &gt; 100).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(self.reconciliation\_queue\_size) &lt; 5 → cint(self.reconciliation\_queue\_size) &gt; 100.
    - Call the validation error handler Platform.throw(translated “Queue Size should be between 5 and 100”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L225) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L215)

<a id="op-5317e168121c49"></a>
### Accounts Settings.validate auto tax settings

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_accounts_settings_validate_auto_tax_settings`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You cannot enable both the settings '{0}' and '{1}'.”.format(Platform.bold(translated self.meta.get\_label(“add\_taxes\_from\_item\_tax\_template”)), Platform.bold(translated self.meta.get\_label(“add ….

**Local steps**

- If (self.add\_taxes\_from\_item\_tax\_template and self.add\_taxes\_from\_taxes\_and\_charges\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.add\_taxes\_from\_item\_tax\_template → self.add\_taxes\_from\_taxes\_and\_charges\_template.
  - Call the validation error handler Platform.throw(translated “You cannot enable both the settings '{0}' and '{1}'.”.format(Platform.bold(translated nested operand in the contract.meta.get\_label(“add\_taxes\_from\_item\_tax\_template”)), Platform ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L216)

<a id="op-09d60136af8d5f"></a>
### Accounts Settings.update property for accounting dimension

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_accounts_settings_update_property_for_accounting_dimension`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set doctypes from list of entry.document\_type for entry drawn from self.repost\_allowed\_types.
  - Draw entry from self.repost\_allowed\_types.
- If not doctypes.
  - Return no value.
- Bind dependencies get\_child\_docs.
- Update doctypes using + get\_child\_docs(doctypes).
- Evaluate set\_allow\_on\_submit\_for\_dimension\_fields(doctypes).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L5156) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L213)

<a id="op-9c3e8a26c6ab0d"></a>
### Get posting date confirmation

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_get_posting_date_confirmation`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** int.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** cint(Platform.db.get\_single\_value(“Accounts Settings”, “confirm\_before\_resetting\_posting\_date”, cache = false)).

**Local steps**

- Return cint(Platform.db.get\_single\_value(“Accounts Settings”, “confirm\_before\_resetting\_posting\_date”, cache = false)).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “confirm\_before\_resetting\_posting\_date”, cache = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L5302) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L219)

<a id="op-6aa6d3d6011785"></a>
### Toggle accounting dimension sections

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_toggle_accounting_dimension_sections`

**Inputs** hide.

**Local steps**

- Set accounting\_dimension\_doctypes from Platform.get\_hooks(“accounting\_dimension\_doctypes”).
- For each doctype in accounting\_dimension\_doctypes.
  - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, “accounting\_dimensions\_section”, hide).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“accounting\_dimension\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L5427) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L231) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L221)

<a id="op-e97d062930e7f9"></a>
### Toggle sales discount section

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_toggle_sales_discount_section`

**Inputs** hide.

**Local steps**

- For each doctype in (SELLING\_DOCTYPES + BUYING\_DOCTYPES).
  - Set meta from Platform.get\_meta(doctype).
  - If meta.has\_field(“additional\_discount\_section”).
    - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, “additional\_discount\_section”, hide).
  - If meta.has\_field(“discount\_and\_margin”).
    - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, “discount\_and\_margin”, hide).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L5538) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L234) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L224)

<a id="op-0c1bb80e67391b"></a>
### Toggle loyalty point program section

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_toggle_loyalty_point_program_section`

**Inputs** hide.

**Local steps**

- For each doctype in SELLING\_DOCTYPES.
  - Set meta from Platform.get\_meta(doctype).
  - If meta.has\_field(“loyalty\_points\_redemption”).
    - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, “loyalty\_points\_redemption”, hide).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L5750) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L232) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L222)

<a id="op-a8d3384f3c2274"></a>
### Toggle subscription sections

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_toggle_subscription_sections`

**Inputs** hide.

**Local steps**

- Set subscription\_doctypes from Platform.get\_hooks(“subscription\_doctypes”).
- For each doctype in subscription\_doctypes.
  - Evaluate create\_property\_setter\_for\_hiding\_field(doctype, “subscription\_section”, hide).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“subscription\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L5891) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L235) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L225)

<a id="op-37de73f50121c7"></a>
### Toggle overdue billing threshold field

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_toggle_overdue_billing_threshold_field`

**Inputs** hide.

**Local steps**

- Evaluate create\_property\_setter\_for\_hiding\_field(“Customer Credit Limit”, “overdue\_billing\_threshold”, hide).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L6002) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L233) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L223)

<a id="op-f96f27210874a9"></a>
### Create property setter for hiding field

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_create_property_setter_for_hiding_field`

**Inputs** doctype, field\_name, hide.

**Local steps**

- Evaluate make\_property\_setter(doctype, field\_name, “hidden”, hide, validate\_fields\_for\_doctype = false, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L6072) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L218)

<a id="op-9f6a9b898cb9fe"></a>
### Set allow on submit for dimension fields

`operation_enterprise_accounts_record_definitions_accounts_settings_business_behavior_set_allow_on_submit_for_dimension_fields`

**Inputs** doctypes.

**State and service calls** request set\_value on “Custom Field”.

**Local steps**

- For each dt in doctypes.
  - Set meta from Platform.get\_meta(dt).
  - For each dimension in get\_accounting\_dimensions().
    - Set df from meta.get\_field(dimension).
    - If (df and not df.allow\_on\_submit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → not df.allow\_on\_submit.
      - Evaluate Platform.db.set\_value(“Custom Field”, ((dt + “-”) + dimension), “allow\_on\_submit”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L6170) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L230) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L220)

## Service · Address

<a id="op-096eccc2fcf79e"></a>
### Enterprise Address.validate

`operation_enterprise_accounts_custom_address_business_behavior_enterprise_resource_planning_next_address_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_reference().
- Evaluate self.update\_company\_address().
- If hasattr(super(), “validate”).
  - Evaluate super().validate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate reference](operations-010.md#op-a922763c417be1), [update company address](operations-010.md#op-c5ec0528c65bcd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0002.json#L5134) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L11) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L5)

<a id="op-69aa8bad6d3a5d"></a>
### Enterprise Address.link address

`operation_enterprise_accounts_custom_address_business_behavior_enterprise_resource_planning_next_address_link_address`

**Inputs** self.

**Explicit results** no value · super().link\_address().

**Local steps**

- If self.get(“is\_your\_company\_address”).
  - Return no value.
- Return super().link\_address().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0002.json#L5263) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L8) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L2)
