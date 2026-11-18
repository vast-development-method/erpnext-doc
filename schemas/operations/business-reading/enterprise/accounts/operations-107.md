# Accounting and settlement · operations 107

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Sales register

<a id="op-cc0a8395e2fe03"></a>
### Get invoice cc wh map

`operation_enterprise_accounts_report_sales_register_business_behavior_get_invoice_carbon_copy_warehouse_map`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** invoice\_cc\_wh\_map.

**Local steps**

- Set si\_items from Platform.db.sql((query text (SELECT, Sales Invoice Item) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(generator of inv.name for inv drawn from invoice\_list), as\_dict = 1).
  - Draw inv from invoice\_list.
- Set invoice\_cc\_wh\_map from mapping().
- For each d in si\_items.
  - If d.cost\_center.
    - Evaluate invoice\_cc\_wh\_map.setdefault(d.parent, nested operand in the contract.\_dict()).setdefault(“cost\_center”, list()).append(d.cost\_center).
  - If d.warehouse.
    - Evaluate invoice\_cc\_wh\_map.setdefault(d.parent, nested operand in the contract.\_dict()).setdefault(“warehouse”, list()).append(d.warehouse).
- Return invoice\_cc\_wh\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L25)

<a id="op-39bc4104ae9235"></a>
### Get mode of payments

`operation_enterprise_accounts_report_sales_register_business_behavior_get_mode_of_payments`

**Inputs** invoice\_list.

**State and service calls** execute a supplied database query.

**Explicit results** mode\_of\_payments.

**Local steps**

- Set mode\_of\_payments from mapping().
- If invoice\_list.
  - Set inv\_mop from Platform.db.sql((query text (SELECT, Sales Invoice Payment) modulo or format “, ”.join((list(“%s”) × len(invoice\_list)))), tuple(invoice\_list), as\_dict = 1).
  - For each d in inv\_mop.
    - Evaluate mode\_of\_payments.setdefault(d.parent, list()).append(d.mode\_of\_payment).
- Return mode\_of\_payments.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L928) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L30)

## Record · Sales taxes and charges template

[Record definition](../../../../data/record-types/sales_taxes_and_charges_template.json)

<a id="op-6969395659b685"></a>
### Sales Taxesand Charges Template.validate

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_business_behavior_sales_taxesand_charges_template_validate`

**Inputs** self.

**Local steps**

- Evaluate valdiate\_taxes\_and\_charges\_template(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0186.json#L7291) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L170)

<a id="op-a1a4dd1784eb2c"></a>
### Sales Taxesand Charges Template.autoname

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_business_behavior_sales_taxesand_charges_template_autoname`

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

[Applicable decision contract](../../../enterprise-decision-contracts/part-0186.json#L7343) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L168)

<a id="op-1c73d335178fda"></a>
### Sales Taxesand Charges Template.set missing values

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_business_behavior_sales_taxesand_charges_template_set_missing_values`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Local steps**

- For each data in self.taxes.
  - If (data.charge\_type equals “On Net Total” and flt(data.rate) equals 0.0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data.charge\_type equals “On Net Total” → flt(data.rate) equals 0.0.
    - Set data.rate from Platform.get\_cached\_value(“Account”, data.account\_head, “tax\_rate”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, data.account\_head, “tax\_rate”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0186.json#L7503) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L169)

<a id="op-a694d043533b3b"></a>
### Valdiate taxes and charges template

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_business_behavior_valdiate_taxes_and_charges_template`

**Inputs** doc.

**State and service calls** execute a supplied database query.

**Local steps**

- If doc.is\_default equals 1.
  - Evaluate Platform.db.sql(formatted text update ′tab{doc.doctype}′ set is\_default = 0  where is\_default = 1 and name != %s and company = %s, tuple(doc.name, doc.company)).
- Evaluate validate\_disabled(doc).
- Evaluate validate\_for\_tax\_category(doc).
- For each tax in doc.get(“taxes”).
  - Evaluate validate\_taxes\_and\_charges(tax).
  - Evaluate validate\_account\_head(tax.idx, tax.account\_head, doc.company, translated “Taxes and Charges”).
  - Evaluate validate\_cost\_center(tax, doc).
  - Evaluate validate\_inclusive\_tax(tax, doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L171)

<a id="op-11b0d1f2b0de04"></a>
### Validate disabled

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_business_behavior_validate_disabled`

**Inputs** doc.

**Explicit failure paths** validation helper — translated “Disabled template must not be default template”.

**Local steps**

- If (doc.is\_default and doc.disabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.is\_default → doc.disabled.
  - Call the validation error handler Platform.throw(translated “Disabled template must not be default template”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L465) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L172)

<a id="op-12acd2aff6c64b"></a>
### Validate for tax category

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_business_behavior_validate_for_tax_category`

**Inputs** doc.

**Record and data access** read doc.doctype via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A template with tax category {0} already exists. Only one template is allowed with each tax category”.format(Platform.bold(doc.tax\_category)).

**Local steps**

- If not doc.tax\_category.
  - Return no value.
- If Platform.db.exists(doc.doctype, mapping(“company” → doc.company, “tax\_category” → doc.tax\_category, “disabled” → 0, “name” → list(“!=”, doc.name))).
  - Call the validation error handler Platform.throw(translated “A template with tax category {0} already exists. Only one template is allowed with each tax category”.format(Platform.bold(doc.tax\_category))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L563) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L173)

<a id="op-006b84be6c62f5"></a>
### Get data

`operation_enterprise_accounts_record_definitions_sales_taxes_and_charges_template_sales_taxes_and_charges_template_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “taxes\_and\_charges”, “non\_standard\_fieldnames” → mapping(“Tax Rule” → “sales\_tax\_template”, “Subscription” → “sales\_tax\_template”), “transactions” → list(mapping(“label” → translated  ….

**Local steps**

- Return mapping(“fieldname” → “taxes\_and\_charges”, “non\_standard\_fieldnames” → mapping(“Tax Rule” → “sales\_tax\_template”, “Subscription” → “sales\_tax\_template”), “transactions” → list(mapping(“label” → translated  ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0187.json#L822) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L174)

## Record · Share balance

[Record definition](../../../../data/record-types/share_balance.json)

<a id="op-7fb8e147f8f1a8"></a>
### Share Balance.validate

`operation_enterprise_binding_enterprise_accounts_doctype_share_balance_share_balance_sharebalance_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Share balances can only be changed through Share Transfer”.

**Local steps**

- Call the validation error handler Platform.throw(translated “Share balances can only be changed through Share Transfer”, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1077)

<a id="op-05200183cd362b"></a>
### Share Balance.on trash

`operation_enterprise_binding_enterprise_accounts_doctype_share_balance_share_balance_sharebalance_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Share balances can only be changed through Share Transfer”.

**Local steps**

- Call the validation error handler Platform.throw(translated “Share balances can only be changed through Share Transfer”, title = translated “Not Allowed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L438) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1076)

## Report · Share balance

<a id="op-80e6aeb96622ce"></a>
### Execute

`operation_enterprise_accounts_report_share_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Please select date”.

**Local steps**

- If not filters.
  - Set filters from mapping().
- If not filters.get(“date”).
  - Call the validation error handler Platform.throw(translated “Please select date”).
- Set columns from get\_columns(filters).
- Set data from list().
- If not filters.get(“shareholder”).
  - Take no action here.
- Otherwise.
  - Set tuple(share\_type, no\_of\_shares, rate, amount) from tuple(1, 2, 3, 4).
  - Set all\_shares from get\_all\_shares(filters.get(“shareholder”), filters.get(“date”), filters.get(“company”)).
  - For each share\_entry in all\_shares.
    - Set row from false.
    - For each datum in data.
      - If datum at share\_type equals share\_entry.share\_type.
        - Update datum at no\_of\_shares using + share\_entry.no\_of\_shares.
        - Update datum at amount using + share\_entry.amount.
        - If datum at no\_of\_shares equals 0.
          - Set datum at rate from 0.
        - Otherwise.
          - Set datum at rate from (datum at amount ÷ datum at no\_of\_shares).
        - Set row from true.
        - Leave the innermost loop without its normal-exhaustion alternative.
    - If not row.
      - Set row from list(filters.get(“shareholder”), share\_entry.share\_type, share\_entry.no\_of\_shares, share\_entry.rate, …).
      - Evaluate data.append(row).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0280.json#L4514) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L40)

<a id="op-cdc3d43acffffc"></a>
### Get columns

`operation_enterprise_accounts_report_share_balance_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Shareholder” + “:Link/Shareholder:150”), (translated “Share Type” + “::90”), (translated “No of Shares” + “::90”), (translated “Average Rate” + “:Currency:90”), …).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0280.json#L5212) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L942) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L42)

<a id="op-7d2c8d4dc176b7"></a>
### Get all shares

`operation_enterprise_accounts_report_share_balance_business_behavior_get_all_shares`

**Inputs** shareholder, date, company = no value.

**Record and data access** read “Shareholder” via get\_value.

**Explicit results** list() · list of get\_block(get\_last\_receipt(received, share\_type, from\_no, to\_no), from\_no, to\_no) for tuple(share\_type, from\_no, to\_no) drawn from get\_held\_ranges(received, sent).

**Local steps**

- Set holder from Platform.db.get\_value(“Shareholder”, shareholder, list(“name”, “is\_company”, “company”), as\_dict = true).
- If not holder.
  - Return list().
- Set transfers from get\_transfers(holder, date, company).
- Set received from list of transfer for transfer drawn from transfers where is\_received(transfer, holder).
  - Draw transfer from transfers, keep a combination only if (is\_received(transfer, holder)).
- Set sent from list of transfer for transfer drawn from transfers where not is\_received(transfer, holder).
  - Draw transfer from transfers, keep a combination only if (not is\_received(transfer, holder)).
- Return list of get\_block(get\_last\_receipt(received, share\_type, from\_no, to\_no), from\_no, to\_no) for tuple(share\_type, from\_no, to\_no) drawn from get\_held\_ranges(received, sent).
  - Draw tuple(share\_type, from\_no, to\_no) from get\_held\_ranges(received, sent).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L41)

<a id="op-72eea95e3f5b84"></a>
### Get transfers

`operation_enterprise_binding_enterprise_accounts_report_share_balance_share_balance_get_transfers`

**Inputs** holder, date, company = no value.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set share\_transfer from Platform.qb.DocType(“Share Transfer”).
- Set is\_involved from (share\_transfer.to\_shareholder equals holder.name bitwise or share\_transfer.from\_shareholder equals holder.name).
- If holder.is\_company.
  - Update is\_involved using bitwise or (share\_transfer.transfer\_type.isin(list(“Issue”, “Purchase”)) bitwise and share\_transfer.company equals holder.company).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If company.
  - Set query from query.where(share\_transfer.company equals company).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L633) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1271)

<a id="op-4527551a8db0f7"></a>
### Is received

`operation_enterprise_binding_enterprise_accounts_report_share_balance_share_balance_is_received`

**Inputs** transfer, holder.

**Explicit results** true · transfer.to\_shareholder equals holder.name.

**Local steps**

- If (holder.is\_company and transfer.transfer\_type equals “Issue”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in holder.is\_company → transfer.transfer\_type equals “Issue”.
  - Return true.
- Return transfer.to\_shareholder equals holder.name.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L207) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L634) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1272)

<a id="op-26280d74e391a1"></a>
### Get held ranges

`operation_enterprise_binding_enterprise_accounts_report_share_balance_share_balance_get_held_ranges`

**Inputs** received, sent.

**Explicit results** held\_ranges.

**Local steps**

- Set changes from defaultdict(int).
- For each tuple(transfers, sign) in tuple(tuple(received, 1), tuple(sent, negative 1)).
  - For each transfer in transfers.
    - Update changes at tuple(transfer.share\_type, transfer.from\_no) using + sign.
    - Update changes at tuple(transfer.share\_type, (transfer.to\_no + 1)) using − sign.
- Set held\_ranges from list().
- Set held\_count from 0.
- For each tuple(tuple(share\_type, from\_no), tuple(next\_share\_type, next\_no)) in pairwise(sorted(changes)).
  - Update held\_count using + changes at tuple(share\_type, from\_no).
  - If (held\_count &gt; 0 and share\_type equals next\_share\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in held\_count &gt; 0 → share\_type equals next\_share\_type.
    - Evaluate held\_ranges.append(tuple(share\_type, from\_no, (next\_no − 1))).
- Return held\_ranges.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1269)

<a id="op-b2dfd0ed11e456"></a>
### Get last receipt

`operation_enterprise_binding_enterprise_accounts_report_share_balance_share_balance_get_last_receipt`

**Inputs** received, share\_type, from\_no, to\_no.

**Explicit results** list of transfer for transfer drawn from received where (transfer.share\_type equals share\_type and transfer.from\_no ≤ from\_no and transfer.to\_no ≥ to\_no) at negative 1.

**Local steps**

- Return list of transfer for transfer drawn from received where (transfer.share\_type equals share\_type and transfer.from\_no ≤ from\_no and transfer.to\_no ≥ to\_no) at negative 1.
  - Draw transfer from received, keep a combination only if ((transfer.share\_type equals share\_type and transfer.from\_no ≤ from\_no and transfer.to\_no ≥ to\_no)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in transfer.share\_type equals share\_type → transfer.from\_no ≤ from\_no → transfer.to\_no ≥ to\_no.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L632) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1270)

<a id="op-eee857493f89e7"></a>
### Get block

`operation_enterprise_binding_enterprise_accounts_report_share_balance_share_balance_get_block`

**Inputs** block, from\_no, to\_no.

**Explicit results** Platform.\_dict(share\_type = block.share\_type, from\_no = from\_no, to\_no = to\_no, no\_of\_shares = no\_of\_shares, …).

**Local steps**

- Set no\_of\_shares from ((to\_no − from\_no) + 1).
- Return Platform.\_dict(share\_type = block.share\_type, from\_no = from\_no, to\_no = to\_no, no\_of\_shares = no\_of\_shares, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L630) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1268)

## Report · Share ledger

<a id="op-6174b67a1b7560"></a>
### Execute

`operation_enterprise_accounts_report_share_ledger_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “Please select date”.

**Local steps**

- If not filters.
  - Set filters from mapping().
- If not filters.get(“date”).
  - Call the validation error handler Platform.throw(translated “Please select date”).
- Set columns from get\_columns(filters).
- Set date from filters.get(“date”).
- Set data from list().
- If not filters.get(“shareholder”).
  - Take no action here.
- Otherwise.
  - Set transfers from get\_all\_transfers(date, filters.get(“shareholder”)).
  - For each transfer in transfers.
    - If transfer.transfer\_type equals “Transfer”.
      - If transfer.from\_shareholder equals filters.get(“shareholder”).
        - Update transfer.transfer\_type using + formatted text  to {transfer.to\_shareholder}.
      - Otherwise.
        - Update transfer.transfer\_type using + formatted text  from {transfer.from\_shareholder}.
    - Set row from list(filters.get(“shareholder”), transfer.date, transfer.transfer\_type, transfer.share\_type, …).
    - Evaluate data.append(row).
- Return tuple(columns, data).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0281.json#L1880) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L956) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L55)

<a id="op-3ee1adf5df07a5"></a>
### Get columns

`operation_enterprise_accounts_report_share_ledger_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list((translated “Shareholder” + “:Link/Shareholder:150”), (translated “Date” + “:Date:100”), (translated “Transfer Type” + “::140”), (translated “Share Type” + “::90”), …).
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0281.json#L2463) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L958) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L57)

<a id="op-999c76bea3db3a"></a>
### Get all transfers

`operation_enterprise_accounts_report_share_ledger_business_behavior_get_all_transfers`

**Inputs** date, shareholder.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text SELECT \* FROM ′tabShare Transfer′  WHERE ((DATE(date) &lt;= %(date)s AND from\_shareholder = %(shareholder)s {condition})  OR (DATE(date) &lt;= %(date)s AN, mapping(“date” → date, ….

**Local steps**

- Set condition from one space.
- Return Platform.db.sql(formatted text SELECT \* FROM ′tabShare Transfer′  WHERE ((DATE(date) &lt;= %(date)s AND from\_shareholder = %(shareholder)s {condition})  OR (DATE(date) &lt;= %(date)s AN, mapping(“date” → date, ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L957) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L56)

## Record · Share transfer

[Record definition](../../../../data/record-types/share_transfer.json)

<a id="op-daf02d7abf7e43"></a>
### Share Transfer.on submit

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_on_submit`

**Inputs** self.

**State and service calls** call save on shareholder · call save on doc.

**Local steps**

- If self.transfer\_type equals “Issue”.
  - Set shareholder from self.get\_company\_shareholder().
  - Evaluate shareholder.append(“share\_balance”, mapping(“share\_type” → self.share\_type, “from\_no” → self.from\_no, “to\_no” → self.to\_no, “rate” → self.rate, …)).
  - Set shareholder.flags.from\_share\_transfer from true.
  - Evaluate shareholder.save().
  - Set doc from self.get\_shareholder\_doc(self.to\_shareholder).
  - Evaluate doc.append(“share\_balance”, mapping(“share\_type” → self.share\_type, “from\_no” → self.from\_no, “to\_no” → self.to\_no, “rate” → self.rate, …)).
  - Set doc.flags.from\_share\_transfer from true.
  - Evaluate doc.save().
- Otherwise.
  - If self.transfer\_type equals “Purchase”.
    - Evaluate self.remove\_shares(self.from\_shareholder).
    - Evaluate self.remove\_shares(self.get\_company\_shareholder().name).
  - Otherwise.
    - If self.transfer\_type equals “Transfer”.
      - Evaluate self.remove\_shares(self.from\_shareholder).
      - Set doc from self.get\_shareholder\_doc(self.to\_shareholder).
      - Evaluate doc.append(“share\_balance”, mapping(“share\_type” → self.share\_type, “from\_no” → self.from\_no, “to\_no” → self.to\_no, “rate” → self.rate, …)).
      - Set doc.flags.from\_share\_transfer from true.
      - Evaluate doc.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get company shareholder](operations-108.md#op-cefe93315abede), [get shareholder doc](operations-108.md#op-94976d6fcc091c), [remove shares](operations-108.md#op-d413cbcb1d1b43).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L182)

<a id="op-51b1a60ae1b321"></a>
### Share Transfer.on cancel

`operation_enterprise_accounts_record_definitions_share_transfer_business_behavior_share_transfer_on_cancel`

**Inputs** self.

**State and service calls** call save on from\_shareholder · call save on compnay\_shareholder.

**Local steps**

- If self.transfer\_type equals “Issue”.
  - Set compnay\_shareholder from self.get\_company\_shareholder().
  - Evaluate self.remove\_shares(compnay\_shareholder.name).
  - Evaluate self.remove\_shares(self.to\_shareholder).
- Otherwise.
  - If self.transfer\_type equals “Purchase”.
    - Set compnay\_shareholder from self.get\_company\_shareholder().
    - Set from\_shareholder from self.get\_shareholder\_doc(self.from\_shareholder).
    - Evaluate from\_shareholder.append(“share\_balance”, mapping(“share\_type” → self.share\_type, “from\_no” → self.from\_no, “to\_no” → self.to\_no, “rate” → self.rate, …)).
    - Set from\_shareholder.flags.from\_share\_transfer from true.
    - Evaluate from\_shareholder.save().
    - Evaluate compnay\_shareholder.append(“share\_balance”, mapping(“share\_type” → self.share\_type, “from\_no” → self.from\_no, “to\_no” → self.to\_no, “rate” → self.rate, …)).
    - Set compnay\_shareholder.flags.from\_share\_transfer from true.
    - Evaluate compnay\_shareholder.save().
  - Otherwise.
    - If self.transfer\_type equals “Transfer”.
      - Evaluate self.remove\_shares(self.to\_shareholder).
      - Set from\_shareholder from self.get\_shareholder\_doc(self.from\_shareholder).
      - Evaluate from\_shareholder.append(“share\_balance”, mapping(“share\_type” → self.share\_type, “from\_no” → self.from\_no, “to\_no” → self.to\_no, “rate” → self.rate, …)).
      - Set from\_shareholder.flags.from\_share\_transfer from true.
      - Evaluate from\_shareholder.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get company shareholder](operations-108.md#op-cefe93315abede), [remove shares](operations-108.md#op-d413cbcb1d1b43), [get shareholder doc](operations-108.md#op-94976d6fcc091c).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L181)
