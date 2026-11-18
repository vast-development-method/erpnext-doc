# Asset management · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-58582bbbc1b9dd"></a>
### Asset.has pending repair

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_has_pending_repair`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Asset Repair” via exists.

**Explicit results** false · bool(Platform.db.exists(“Asset Repair”, mapping(“asset” → self.name, “repair\_status” → “Pending”, “docstatus” → tuple(“&lt;”, 2)))).

**Local steps**

- If (self.docstatus differs from 1 or self.disposal\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 1 → self.disposal\_date.
  - Return false.
- Return bool(Platform.db.exists(“Asset Repair”, mapping(“asset” → self.name, “repair\_status” → “Pending”, “docstatus” → tuple(“&lt;”, 2)))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L233) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1298)

<a id="op-8b4ecdfd133e1d"></a>
### Asset.get status

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_status`

**Inputs** self.

**Explicit results** status.

**Local steps**

- If self.docstatus equals 0.
  - If self.asset\_type equals “Composite Asset”.
    - Set status from “Work In Progress”.
  - Otherwise.
    - Set status from “Draft”.
- Otherwise.
  - If self.docstatus equals 1.
    - Set status from “Submitted”.
    - If self.journal\_entry\_for\_scrap.
      - Set status from “Scrapped”.
    - Otherwise.
      - If self.is\_sold().
        - Set status from “Sold”.
      - Otherwise.
        - Set expected\_value\_after\_useful\_life from 0.
        - Set value\_after\_depreciation from self.value\_after\_depreciation.
        - If self.calculate\_depreciation.
          - Set idx from (self.get\_default\_finance\_book\_idx() or 0).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_default\_finance\_book\_idx() → 0.
          - Set expected\_value\_after\_useful\_life from self.finance\_books at idx.expected\_value\_after\_useful\_life.
          - Set value\_after\_depreciation from self.finance\_books at idx.value\_after\_depreciation.
          - If flt(value\_after\_depreciation) ≤ expected\_value\_after\_useful\_life.
            - Set status from “Fully Depreciated”.
          - Otherwise.
            - If flt(value\_after\_depreciation) &lt; flt(self.net\_purchase\_amount).
              - Set status from “Partially Depreciated”.
        - Otherwise.
          - If self.is\_fully\_depreciated.
            - Set status from “Fully Depreciated”.
  - Otherwise.
    - If self.docstatus equals 2.
      - Set status from “Cancelled”.
- Return status.

**Methods declared on this owner** [is sold](operations-003.md#op-1200137d2f6d7b), [get default finance book idx](operations-003.md#op-7d2cd45c95911b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L278)

<a id="op-1200137d2f6d7b"></a>
### Asset.is sold

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_is_sold`

**Inputs** self.

**Declared result** bool.

**Record and data access** read “Sales Invoice” via get\_all.

**Explicit results** false · bool(Platform.get\_all(“Sales Invoice”, filters = list(list(“Sales Invoice Item”, “asset”, “=”, self.name), list(“docstatus”, “=”, 1), list(“is\_return”, “=”, 0)), limit = 1)).

**Local steps**

- If not self.disposal\_date.
  - Return false.
- Return bool(Platform.get\_all(“Sales Invoice”, filters = list(list(“Sales Invoice Item”, “asset”, “=”, self.name), list(“docstatus”, “=”, 1), list(“is\_return”, “=”, 0)), limit = 1)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L235) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1300)

<a id="op-646a0636ec52af"></a>
### Asset.get value after depreciation

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_value_after_depreciation`

**Inputs** self, finance\_book = no value.

**Explicit results** flt(self.value\_after\_depreciation, self.precision(“net\_purchase\_amount”)) · flt(self.get(“finance\_books”) at 0.value\_after\_depreciation, self.precision(“net\_purchase\_amount”)) · flt(row.value\_after\_depreciation, self.precision(“net\_purchase\_amount”)).

**Local steps**

- If not self.calculate\_depreciation.
  - Return flt(self.value\_after\_depreciation, self.precision(“net\_purchase\_amount”)).
- If not finance\_book.
  - Return flt(self.get(“finance\_books”) at 0.value\_after\_depreciation, self.precision(“net\_purchase\_amount”)).
- For each row in self.get(“finance\_books”).
  - If finance\_book equals row.finance\_book.
    - Return flt(row.value\_after\_depreciation, self.precision(“net\_purchase\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L5552) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L279)

<a id="op-2e67ab72d1a96a"></a>
### Asset.sync value after depreciation

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_sync_value_after_depreciation`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Asset Finance Book” via get\_value.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If (not self.calculate\_depreciation or not self.get(“finance\_books”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.calculate\_depreciation → not self.get(“finance\_books”).
  - Return no value.
- Set row from self.finance\_books at (self.get\_default\_finance\_book\_idx() or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_default\_finance\_book\_idx() → 0.
- Evaluate self.db\_set(“value\_after\_depreciation”, Platform.db.get\_value(“Asset Finance Book”, row.name, “value\_after\_depreciation”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get default finance book idx](operations-003.md#op-7d2cd45c95911b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1302)

<a id="op-7d2cd45c95911b"></a>
### Asset.get default finance book idx

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_default_finance_book_position`

**Inputs** self.

**Explicit results** (cint(d.idx) − 1).

**Local steps**

- If (not self.get(“default\_finance\_book”) and self.company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“default\_finance\_book”) → self.company.
  - Set self.default\_finance\_book from Enterprise.get\_default\_finance\_book(self.company).
- If self.get(“default\_finance\_book”).
  - For each d in self.get(“finance\_books”).
    - If d.finance\_book equals self.default\_finance\_book.
      - Return (cint(d.idx) − 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L5854) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L271)

<a id="op-024135f69eb126"></a>
### Asset.get manual depreciation entries

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_manual_depreciation_entries`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** records.

**Local steps**

- Set tuple(\_, \_, depreciation\_expense\_account) from get\_depreciation\_accounts(self.asset\_category, self.company).
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set records from nested operand in the contract(nested operand in the contract).orderby(gle.posting\_date).orderby(gle.creation).run(as\_dict = true).
- Return records.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L6104) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L276)

<a id="op-1aff5971b9efa4"></a>
### Asset.validate make gl entry

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_make_general_ledger_entry`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** true · false · cwip\_booked.

**Local steps**

- <a id="op-1aff5971b9efa4-guard-2"></a>If self.asset\_type equals “Composite Asset”.
  - Return true.
- Set purchase\_document from self.get\_purchase\_document().
- If not purchase\_document.
  - Return false.
- Set asset\_bought\_with\_invoice from purchase\_document equals self.purchase\_invoice.
- Set fixed\_asset\_account from self.get\_fixed\_asset\_account().
- Set cwip\_enabled from is\_cwip\_accounting\_enabled(self.asset\_category).
- Set cwip\_account from self.get\_cwip\_account(cwip\_enabled = cwip\_enabled).
- Set query from query text (SELECT, GL Entry).
- If asset\_bought\_with\_invoice.
  - Set expense\_booked from Platform.db.sql(query, tuple(purchase\_document, fixed\_asset\_account), as\_dict = 1).
  - If expense\_booked.
    - Return false.
  - Set cwip\_booked from Platform.db.sql(query, tuple(purchase\_document, cwip\_account), as\_dict = 1).
  - If cwip\_booked.
    - Return true.
- Otherwise.
  - If not cwip\_account.
    - Return false.
  - Set cwip\_booked from Platform.db.sql(query, tuple(purchase\_document, cwip\_account), as\_dict = 1).
  - Return cwip\_booked.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.asset\_type equals “Composite Asset”, self.asset\_type = “Composite Asset” selects the branch that returns true. With self.asset\_type = “Existing Asset”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-1aff5971b9efa4-guard-2)

**Methods declared on this owner** [get purchase document](operations-003.md#op-ca1e9ce31ac6d1), [get fixed asset account](operations-003.md#op-927ab5ad657f32), [get cwip account](operations-003.md#op-559d00ce0b328e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1411) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L311)

<a id="op-ca1e9ce31ac6d1"></a>
### Asset.get purchase document

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_purchase_document`

**Inputs** self.

**Record and data access** read “Purchase Invoice” via get\_value.

**Explicit results** purchase\_document.

**Local steps**

- Set asset\_bought\_with\_invoice from (self.purchase\_invoice and Platform.db.get\_value(“Purchase Invoice”, self.purchase\_invoice, “update\_stock”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.purchase\_invoice → Platform.db.get\_value(“Purchase Invoice”, self.purchase\_invoice, “update\_stock”).
- Set purchase\_document from self.purchase\_invoice when asset\_bought\_with\_invoice, otherwise self.purchase\_receipt.
  - Value choice on asset\_bought\_with\_invoice — true gives self.purchase\_invoice, false gives self.purchase\_receipt.
- Return purchase\_document.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L536) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L277)

<a id="op-927ab5ad657f32"></a>
### Asset.get fixed asset account

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_fixed_asset_account`

**Inputs** self.

**Explicit results** fixed\_asset\_account.

**Explicit failure paths** validation helper — translated “Set {0} in asset category {1} for company {2}”.format(Platform.bold(translated “Fixed Asset Account”), Platform.bold(self.asset\_category), Platform.bold(self.company)).

**Local steps**

- Set fixed\_asset\_account from get\_asset\_category\_account(“fixed\_asset\_account”, no value, self.name, no value, …).
- If not fixed\_asset\_account.
  - Call the validation error handler Platform.throw(translated “Set {0} in asset category {1} for company {2}”.format(Platform.bold(translated “Fixed Asset Account”), Platform.bold(self.asset\_category), Platform.bold(self.company)), title = t ….
- Return fixed\_asset\_account.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L675) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L274)

<a id="op-559d00ce0b328e"></a>
### Asset.get cwip account

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_cwip_account`

**Inputs** self, cwip\_enabled = false.

**Explicit results** cwip\_account.

**Explicit failure paths** propagate active failure.

**Local steps**

- Set cwip\_account from no value.
- Attempt the following.
  - Set cwip\_account from get\_asset\_account(“capital\_work\_in\_progress\_account”, self.name, self.asset\_category, self.company).
- On failure (Exception).
  - If cwip\_enabled.
    - Propagate the active failure.
- Return cwip\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L952) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L270)

<a id="op-f81b7a4a38c48e"></a>
### Asset.make gl entries

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_make_general_ledger_entries`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- If self.check\_asset\_capitalization\_gl\_entries().
  - Return no value.
- Set gl\_entries from list().
- Set purchase\_document from self.get\_purchase\_document().
- Set tuple(fixed\_asset\_account, cwip\_account) from tuple(self.get\_fixed\_asset\_account(), self.get\_cwip\_account()).
- If ((self.asset\_type equals “Composite Asset” or (purchase\_document and self.purchase\_amount)) and getdate(self.available\_for\_use\_date) ≤ getdate()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.asset\_type equals “Composite Asset” or (purchase\_document and self.purchase\_amount)) → getdate(self.available\_for\_use\_date) ≤ getdate().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.asset\_type equals “Composite Asset” → (purchase\_document and self.purchase\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in purchase\_document → self.purchase\_amount.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → cwip\_account, “against” → fixed\_asset\_account, “remarks” → (self.get(“remarks”) or translated “Accounting Entry for Asset”), “posting\_date” → self.ava ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Asset”.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → fixed\_asset\_account, “against” → cwip\_account, “remarks” → (self.get(“remarks”) or translated “Accounting Entry for Asset”), “posting\_date” → self.ava ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Asset”.
- If gl\_entries.
  - Bind dependencies make\_gl\_entries.
  - Evaluate make\_gl\_entries(gl\_entries).
  - Evaluate self.db\_set(“booked\_fixed\_asset”, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check asset capitalization gl entries](operations-003.md#op-ff361a64e3d882), [get purchase document](operations-003.md#op-ca1e9ce31ac6d1), [get fixed asset account](operations-003.md#op-927ab5ad657f32), [get cwip account](operations-003.md#op-559d00ce0b328e).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L1112) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L284)

<a id="op-ff361a64e3d882"></a>
### Asset.check asset capitalization gl entries

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_check_asset_capitalization_general_ledger_entries`

**Inputs** self.

**Record and data access** read “Asset Capitalization” via get\_value.

**Explicit results** has\_gl\_entries(“Asset Capitalization”, asset\_capitalization, target\_fixed\_asset\_account) · true · false.

**Local steps**

- If self.asset\_type equals “Composite Asset”.
  - Set result from Platform.db.get\_value(“Asset Capitalization”, mapping(“target\_asset” → self.name, “docstatus” → 1), list(“name”, “target\_fixed\_asset\_account”)).
  - If result.
    - Set tuple(asset\_capitalization, target\_fixed\_asset\_account) from result.
    - Return has\_gl\_entries(“Asset Capitalization”, asset\_capitalization, target\_fixed\_asset\_account).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L1880) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L266)

<a id="op-ad4e22283a8ac3"></a>
### Asset.get depreciation rate

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_depreciation_rate`

**Inputs** self, args, on\_validate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** self.get\_double\_declining\_balance\_rate(args, rate\_field\_precision) · self.get\_written\_down\_value\_rate(args, rate\_field\_precision, on\_validate).

**Local steps**

- If isinstance(args, str).
  - Set args from json.loads(args).
- Set rate\_field\_precision from (Platform.get\_single\_value(“System Settings”, “float\_precision”) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_single\_value(“System Settings”, “float\_precision”) → 2.
- If args.get(“depreciation\_method”) equals “Double Declining Balance”.
  - Return self.get\_double\_declining\_balance\_rate(args, rate\_field\_precision).
- Otherwise.
  - If args.get(“depreciation\_method”) equals “Written Down Value”.
    - Return self.get\_written\_down\_value\_rate(args, rate\_field\_precision, on\_validate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get double declining balance rate](operations-003.md#op-c3edfc69a6880d), [get written down value rate](operations-003.md#op-5e246841a5dd37).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“System Settings”, “float\_precision”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L272)

<a id="op-70674f18cab470"></a>
### Asset.is entered depreciation rate

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_is_entered_depreciation_rate`

**Inputs** self, settings.

**Declared result** bool.

**Explicit results** false · true · flt(rate, precision) differs from flt(self.get\_initial\_depreciation\_rate(settings), precision).

**Local steps**

- Set rate from flt(settings.get(“rate\_of\_depreciation”)).
- If (settings.get(“depreciation\_method”) differs from “Written Down Value” or not rate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings.get(“depreciation\_method”) differs from “Written Down Value” → not rate.
  - Return false.
- If not flt(settings.get(“expected\_value\_after\_useful\_life”)).
  - Return true.
- Set precision from Platform.get\_precision(“Asset Finance Book”, “rate\_of\_depreciation”).
- Return flt(rate, precision) differs from flt(self.get\_initial\_depreciation\_rate(settings), precision).

**Methods declared on this owner** [get initial depreciation rate](operations-003.md#op-ff44976f585f80).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L234) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1299)

<a id="op-ff44976f585f80"></a>
### Asset.get initial depreciation rate

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_get_initial_depreciation_rate`

**Inputs** self, settings.

**Declared result** float.

**Explicit results** self.get\_depreciation\_rate(mapping of fieldname → settings.get(fieldname) for fieldname drawn from fieldnames).

**Local steps**

- Set fieldnames from tuple(“depreciation\_method”, “expected\_value\_after\_useful\_life”, “total\_number\_of\_depreciations”, “frequency\_of\_depreciation”).
- Return self.get\_depreciation\_rate(mapping of fieldname → settings.get(fieldname) for fieldname drawn from fieldnames).
  - Draw fieldname from fieldnames.

**Methods declared on this owner** [get depreciation rate](operations-003.md#op-ad4e22283a8ac3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L230) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1295)

<a id="op-c3edfc69a6880d"></a>
### Asset.get double declining balance rate

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_double_declining_balance_rate`

**Inputs** self, args, rate\_field\_precision.

**Explicit results** flt((200.0 ÷ ((flt(nested operand in the contract.get(“total\_number\_of\_depreciations”), 2) × flt(nested operand in the contract.get(“frequency\_of\_depreciation”))) ÷ 12)), rate\_field\_precision).

**Local steps**

- Return flt((200.0 ÷ ((flt(nested operand in the contract.get(“total\_number\_of\_depreciations”), 2) × flt(nested operand in the contract.get(“frequency\_of\_depreciation”))) ÷ 12)), rate\_field\_precision).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L2450) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L273)

<a id="op-5e246841a5dd37"></a>
### Asset.get written down value rate

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_written_down_value_rate`

**Inputs** self, args, rate\_field\_precision, on\_validate.

**Explicit results** args.get(“rate\_of\_depreciation”) · flt(depreciation\_rate, rate\_field\_precision).

**Local steps**

- If (args.get(“rate\_of\_depreciation”) and on\_validate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“rate\_of\_depreciation”) → on\_validate.
  - Return args.get(“rate\_of\_depreciation”).
- If (args.get(“rate\_of\_depreciation”) and not flt(args.get(“expected\_value\_after\_useful\_life”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“rate\_of\_depreciation”) → not flt(args.get(“expected\_value\_after\_useful\_life”)).
  - Return args.get(“rate\_of\_depreciation”).
- If flt(args.get(“value\_after\_depreciation”)).
  - Set current\_asset\_value from flt(args.get(“value\_after\_depreciation”)).
- Otherwise.
  - Set current\_asset\_value from (flt(self.net\_purchase\_amount) − flt(self.opening\_accumulated\_depreciation)).
- Set value from (flt(args.get(“expected\_value\_after\_useful\_life”)) ÷ current\_asset\_value).
- Set pending\_number\_of\_depreciations from ((flt(args.get(“total\_number\_of\_depreciations”), 2) − flt(self.opening\_number\_of\_booked\_depreciations)) − flt(args.get(“total\_number\_of\_booked\_depreciations”))).
- Set pending\_years from (((pending\_number\_of\_depreciations × flt(args.get(“frequency\_of\_depreciation”))) + cint(args.get(“increase\_in\_asset\_life”))) ÷ 12).
- Set depreciation\_rate from (100 × (1 − math.pow(value, (1.0 ÷ pending\_years)))).
- Return flt(depreciation\_rate, rate\_field\_precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L2609) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L280)

<a id="op-b50d072a180879"></a>
### Has gl entries

`operation_enterprise_assets_record_definitions_asset_business_behavior_has_general_ledger_entries`

**Inputs** doctype, docname, target\_account.

**Explicit results** len(gl\_entries) &gt; 0.

**Local steps**

- Set gl\_entry from Platform.qb.DocType(“GL Entry”).
- Set gl\_entries from nested operand in the contract(nested operand in the contract).select(gl\_entry.account).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contr ….
- Return len(gl\_entries) &gt; 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L3313) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1421) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L321)

<a id="op-707dc99c3dea36"></a>
### Update maintenance status

`operation_enterprise_assets_record_definitions_asset_business_behavior_update_maintenance_status`

**Inputs** no declared parameters.

**Record and data access** read “Asset” via get\_all · resolve a document from “Asset” via get\_doc.

**Local steps**

- Set assets from Platform.get\_all(“Asset”, filters = mapping(“docstatus” → 1, “maintenance\_required” → 1, “disposal\_date” → tuple(“is”, “not set”))).
- For each asset in assets.
  - Evaluate Platform.get\_doc(“Asset”, asset.name).set\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1424) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L324)

<a id="op-ac5f92354edb9a"></a>
### Has due maintenance

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_has_due_maintenance`

**Inputs** asset\_name.

**Declared result** bool.

**Record and data access** read “Asset Maintenance Log” via exists.

**Explicit results** bool(Platform.db.exists(“Asset Maintenance Log”, mapping(“asset\_name” → asset\_name, “docstatus” → 0, “maintenance\_status” → tuple(“in”, list(“Planned”, “Overdue”)), “due\_date” → tuple(“&lt;=”, today())))).

**Local steps**

- Return bool(Platform.db.exists(“Asset Maintenance Log”, mapping(“asset\_name” → asset\_name, “docstatus” → 0, “maintenance\_status” → tuple(“in”, list(“Planned”, “Overdue”)), “due\_date” → tuple(“&lt;=”, today())))).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1312)

<a id="op-7d952a1266af5e"></a>
### Make post gl entry

`operation_enterprise_assets_record_definitions_asset_business_behavior_make_post_general_ledger_entry`

**Inputs** no declared parameters.

**Record and data access** read “Asset Category” via get\_all · read “Asset” via get\_all.

**Local steps**

- Set asset\_categories from Platform.db.get\_all(“Asset Category”, fields = list(“name”, “enable\_cwip\_accounting”)).
- For each asset\_category in asset\_categories.
  - If cint(asset\_category.enable\_cwip\_accounting).
    - Set assets from Platform.db.get\_all(“Asset”, filters = mapping(“asset\_category” → asset\_category.name, “booked\_fixed\_asset” → 0, “available\_for\_use\_date” → tuple(“&lt;=”, nowdate()), “docstatus” → 1), pluck = “name”).
    - For each asset in assets.
      - Evaluate post\_cwip\_gl\_entry(asset).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1423) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L323)

<a id="op-3fa24b9061637e"></a>
### Post cwip gl entry

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_post_cwip_gl_entry`

**Inputs** asset\_name.

**Declared result** no value.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** savepoint “cwip\_gl\_entry” · rollback.

**Local steps**

- Evaluate Platform.db.savepoint(“cwip\_gl\_entry”).
- Attempt the following.
  - Set asset from Platform.get\_doc(“Asset”, asset\_name).
  - If asset.validate\_make\_gl\_entry().
    - Evaluate asset.make\_gl\_entries().
- On failure (Exception).
  - Evaluate Platform.db.rollback(save\_point = “cwip\_gl\_entry”).
  - Evaluate Platform.log\_error(title = translated “Could not move asset {0} out of CWIP”.format(asset\_name), reference\_doctype = “Asset”, reference\_name = asset\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1317)

<a id="op-6bfd008b5fb0b8"></a>
### Get asset naming series

`operation_enterprise_assets_record_definitions_asset_business_behavior_get_asset_naming_series`

**Inputs** no declared parameters.

**Explicit results** meta.get\_field(“naming\_series”).options.

**Local steps**

- Set meta from Platform.get\_meta(“Asset”).
- Return meta.get\_field(“naming\_series”).options.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0309.json#L4365) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L316)
