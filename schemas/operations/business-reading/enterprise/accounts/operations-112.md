# Accounting and settlement · operations 112

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Tax withholding category

[Record definition](../../../../data/record-types/tax_withholding_category.json)

<a id="op-2b03c88b2916af"></a>
### Tax Withholding Details.get ldc details

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_details_get_ldc_details`

**Inputs** self.

**Explicit results** ldc\_details.

**Local steps**

- Set ldc\_details from mapping().
- If self.party\_type differs from “Supplier”.
  - Return ldc\_details.
- Set ldc\_records from self.get\_valid\_ldc\_records(self.tax\_id).
- If not ldc\_records.
  - Return ldc\_details.
- Set ldc\_names from list of ldc.name for ldc drawn from ldc\_records.
  - Draw ldc from ldc\_records.
- Set ldc\_utilization\_map from self.get\_ldc\_utilization\_by\_category(ldc\_names, self.tax\_id).
- For each ldc in ldc\_records.
  - Set category\_name from ldc.tax\_withholding\_category.
  - Set unutilized\_amount from (ldc.certificate\_limit − (ldc\_utilization\_map.get(ldc.name) or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ldc\_utilization\_map.get(ldc.name) → 0.
  - If not unutilized\_amount.
    - Continue with the next iteration or loop test.
  - Set ldc\_details at category\_name from dict(ldc\_certificate = ldc.name, ldc\_unutilized\_amount = unutilized\_amount, ldc\_rate = ldc.rate).
- Return ldc\_details.

**Methods declared on this owner** [get valid ldc records](operations-112.md#op-80ed8f79c40eee), [get ldc utilization by category](operations-112.md#op-e221cd8ed24ac5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L3068) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1587) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L349)

<a id="op-80ed8f79c40eee"></a>
### Tax Withholding Details.get valid ldc records

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_details_get_valid_ldc_records`

**Inputs** self, tax\_id.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set ldc from Platform.qb.DocType(“Lower Deduction Certificate”).
- Set query from nested operand in the contract.qb.from\_(ldc).select(ldc.name, ldc.tax\_withholding\_category, ldc.rate, ldc.certificate\_limit).where((((ldc.valid\_from ≤ self.posting\_date bitwise and ldc.valid\_upto ≥ self.po ….
- Set query from query.where(ldc.pan\_no equals tax\_id) when tax\_id, otherwise query.where(ldc.supplier equals self.party).
  - Value choice on tax\_id — true gives query.where(ldc.pan\_no equals tax\_id), false gives query.where(ldc.supplier equals self.party).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L3461) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L351)

<a id="op-e221cd8ed24ac5"></a>
### Tax Withholding Details.get ldc utilization by category

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_tax_withholding_details_get_ldc_utilization_by_category`

**Inputs** self, ldc\_names, tax\_id.

**Explicit results** Platform.\_dict(query.run()).

**Local steps**

- Set twe from Platform.qb.DocType(“Tax Withholding Entry”).
- Set query from nested operand in the contract(nested operand in the contract).select(twe.lower\_deduction\_certificate, nested operand in the contract.as\_(“limit\_consumed”)).where(((((nested operand in the contract bitwise ….
- Set query from query.where(twe.tax\_id equals tax\_id) when tax\_id, otherwise query.where(twe.party equals self.party).
  - Value choice on tax\_id — true gives query.where(twe.tax\_id equals tax\_id), false gives query.where(twe.party equals self.party).
- Return Platform.\_dict(query.run()).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L3861) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L350)

<a id="op-6d7a81742d3e67"></a>
### Get tax id for party

`operation_enterprise_accounts_record_definitions_tax_withholding_category_business_behavior_get_tax_identifier_for_party`

**Inputs** party\_type, party.

**Wrappers, in declaration order** allow\_regional.

**Record and data access** read party\_type via get\_value.

**Explicit results** Platform.db.get\_value(party\_type, party, “tax\_id”).

**Local steps**

- Return Platform.db.get\_value(party\_type, party, “tax\_id”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L4363) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1579) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L341)

<a id="op-3ffd78afb67afb"></a>
### Get data

`operation_enterprise_accounts_record_definitions_tax_withholding_category_tax_withholding_category_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “tax\_withholding\_category”, “transactions” → list(mapping(“items” → list(“Supplier”)))).

**Local steps**

- Return mapping(“fieldname” → “tax\_withholding\_category”, “transactions” → list(mapping(“items” → list(“Supplier”)))).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0196.json#L4446) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L353)

## Report · Tax withholding details

<a id="op-2f3e1f4d7f061a"></a>
### Tax Withholding Details Report.initialize

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set self.entries from list().
- Set self.doc\_info from mapping().
- Set self.party\_details from mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L994) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L80)

<a id="op-333d66570971d1"></a>
### Tax Withholding Details Report.execute

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_execute`

**Inputs** cls, filters = no value.

**Wrappers, in declaration order** classmethod.

**Explicit results** cls(filters).run().

**Local steps**

- Return cls(filters).run().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L982) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L68)

<a id="op-4eede515a55f2e"></a>
### Tax Withholding Details Report.run

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_run`

**Inputs** self.

**Explicit results** tuple(self.get\_columns(), self.get\_data()).

**Local steps**

- Evaluate self.validate\_filters().
- Return tuple(self.get\_columns(), self.get\_data()).

**Methods declared on this owner** [validate filters](operations-112.md#op-fa79446e44f811), [get columns](operations-112.md#op-625fc7a0d63c4d), [get data](operations-112.md#op-8e461386c749c2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L217) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L81)

<a id="op-fa79446e44f811"></a>
### Tax Withholding Details Report.validate filters

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_validate_filters`

**Inputs** self.

**Local steps**

- Evaluate validate\_mandatory\_date\_range(self.filters).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L310) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L82)

<a id="op-8e461386c749c2"></a>
### Tax Withholding Details Report.get data

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_data`

**Inputs** self.

**Explicit results** list() · self.build\_rows().

**Local steps**

- Set self.entries from self.get\_entries\_query().run(as\_dict = true).
- Evaluate self.remove\_entries\_of\_restricted\_parties().
- If not self.entries.
  - Return list().
- Set self.doc\_info from self.fetch\_additional\_doc\_info().
- Set self.party\_details from self.fetch\_party\_details().
- Return self.build\_rows().

**Methods declared on this owner** [get entries query](operations-112.md#op-276cb5d5589239), [remove entries of restricted parties](operations-112.md#op-9001a6cd678b61), [fetch additional doc info](operations-112.md#op-1ce4aa83a1ed42), [fetch party details](operations-112.md#op-e1322658fe9d5c), [build rows](operations-112.md#op-f8229e22febc61).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L72)

<a id="op-9001a6cd678b61"></a>
### Tax Withholding Details Report.remove entries of restricted parties

`operation_enterprise_binding_enterprise_accounts_report_tax_withholding_details_tax_withholding_details_taxwithholdingdetailsreport_remove_entries_of_restricted_parties`

**Inputs** self.

**Local steps**

- Set permitted from self.get\_permitted\_parties().
- Set self.entries from list of entry for entry drawn from self.entries where (not entry.party or tuple(entry.party\_type, entry.party) belongs to permitted).
  - Draw entry from self.entries, keep a combination only if ((not entry.party or tuple(entry.party\_type, entry.party) belongs to permitted)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not entry.party → tuple(entry.party\_type, entry.party) belongs to permitted.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get permitted parties](operations-112.md#op-61c9a10376ec35).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L209) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1274)

<a id="op-61c9a10376ec35"></a>
### Tax Withholding Details Report.get permitted parties

`operation_enterprise_binding_enterprise_accounts_report_tax_withholding_details_tax_withholding_details_taxwithholdingdetailsreport_get_permitted_parties`

**Inputs** self.

**Declared result** set at tuple at tuple(str, str).

**Record and data access** read party\_type via get\_list.

**Explicit results** permitted.

**Local steps**

- Set parties\_by\_type from mapping().
- For each entry in self.entries.
  - If entry.party.
    - Evaluate parties\_by\_type.setdefault(entry.party\_type, set()).add(entry.party).
- Set permitted from set().
- For each tuple(party\_type, parties) in parties\_by\_type.items().
  - If not Platform.has\_permission(party\_type, “read”).
    - Continue with the next iteration or loop test.
  - Set names from Platform.get\_list(party\_type, filters = mapping(“name” → list(“in”, list(parties))), pluck = “name”).
  - Evaluate permitted.update(generator of tuple(party\_type, name) for name drawn from names).
    - Draw name from names.
- Return permitted.

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L208) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1273)

<a id="op-f8229e22febc61"></a>
### Tax Withholding Details Report.build rows

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_build_rows`

**Inputs** self.

**Explicit results** rows.

**Local steps**

- Set rows from list().
- For each entry in self.entries.
  - Set doc\_details from self.doc\_info.get(tuple(entry.transaction\_type, entry.ref\_no), mapping()) when entry.ref\_no, otherwise mapping().
    - Value choice on entry.ref\_no — true gives self.doc\_info.get(tuple(entry.transaction\_type, entry.ref\_no), mapping()), false gives mapping().
  - Set party\_info from self.party\_details.get(tuple(entry.party\_type, entry.party), mapping()).
  - Evaluate rows.append(mapping(expand entry, expand doc\_details, expand party\_info)).
- Evaluate rows.sort(key = deferred anonymous expression).
- Return rows.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L554) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L981) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L67)

<a id="op-276cb5d5589239"></a>
### Tax Withholding Details Report.get entries query

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_entries_query`

**Inputs** self.

**Explicit results** query.

**Local steps**

- Set twe from Platform.qb.DocType(“Tax Withholding Entry”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.withholding\_date ≤ nested operand in the contract.to\_date).where(IfNull(twe.withholding\_name, empty text) ….
- If self.filters.company.
  - Set query from query.where(twe.company equals self.filters.company).
- If self.filters.party\_type.
  - Set query from query.where(twe.party\_type equals self.filters.party\_type).
- If self.filters.party.
  - Set query from query.where(twe.party equals self.filters.party).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L920) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L73)

<a id="op-e1322658fe9d5c"></a>
### Tax Withholding Details Report.fetch party details

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_fetch_party_details`

**Inputs** self.

**Explicit results** party\_map.

**Local steps**

- Set parties\_by\_type from mapping of pt → set() for pt drawn from self.party\_types.
  - Draw pt from self.party\_types.
- For each entry in self.entries.
  - If (entry.party\_type belongs to parties\_by\_type and entry.party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.party\_type belongs to parties\_by\_type → entry.party.
    - Evaluate parties\_by\_type at entry.party\_type.add(entry.party).
- Set party\_map from mapping().
- For each tuple(party\_type, party\_set) in parties\_by\_type.items().
  - If not party\_set.
    - Continue with the next iteration or loop test.
  - Set query from self.get\_party\_query(party\_type, party\_set).
  - If query is identical to no value.
    - Continue with the next iteration or loop test.
  - For each row in query.run(as\_dict = true).
    - Set party\_map at tuple(party\_type, row.pop(“name”)) from row.
- Return party\_map.

**Methods declared on this owner** [get party query](operations-112.md#op-b743eded2e07bf).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L1799) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L70)

<a id="op-b743eded2e07bf"></a>
### Tax Withholding Details Report.get party query

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_party_query`

**Inputs** self, party\_type, party\_set.

**Explicit results** no value · nested operand in the contract.qb.from\_(doctype).select(expanded fields).where(doctype.name.isin(party\_set)).

**Local steps**

- Set doctype from Platform.qb.DocType(party\_type).
- Set fields from list(doctype.name).
- If party\_type equals “Supplier”.
  - Evaluate fields.extend(list(doctype.supplier\_type.as\_(“party\_entity\_type”), doctype.supplier\_name.as\_(“party\_name”))).
- Otherwise.
  - If party\_type equals “Customer”.
    - Evaluate fields.extend(list(doctype.customer\_type.as\_(“party\_entity\_type”), doctype.customer\_name.as\_(“party\_name”))).
  - Otherwise.
    - Return no value.
- Return nested operand in the contract.qb.from\_(doctype).select(expanded fields).where(doctype.name.isin(party\_set)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L2191) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L989) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L75)

<a id="op-1ce4aa83a1ed42"></a>
### Tax Withholding Details Report.fetch additional doc info

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_fetch_additional_record_info`

**Inputs** self.

**Explicit results** doc\_info.

**Local steps**

- Set docs\_by\_type from mapping of dt → set() for dt drawn from self.document\_types.
  - Draw dt from self.document\_types.
- For each entry in self.entries.
  - If (entry.ref\_no and entry.transaction\_type belongs to docs\_by\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.ref\_no → entry.transaction\_type belongs to docs\_by\_type.
    - Evaluate docs\_by\_type at entry.transaction\_type.add(entry.ref\_no).
- Set doc\_info from mapping().
- For each tuple(doctype\_name, voucher\_set) in docs\_by\_type.items().
  - If not voucher\_set.
    - Continue with the next iteration or loop test.
  - Set query from self.get\_doc\_info\_query(doctype\_name, voucher\_set).
  - If query is identical to no value.
    - Continue with the next iteration or loop test.
  - For each row in query.run(as\_dict = true).
    - Set doc\_info at tuple(doctype\_name, row.pop(“name”)) from row.
- Return doc\_info.

**Methods declared on this owner** [get doc info query](operations-112.md#op-60eaf7155601f7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L2592) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L983) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L69)

<a id="op-60eaf7155601f7"></a>
### Tax Withholding Details Report.get doc info query

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_record_info_query`

**Inputs** self, doctype\_name, voucher\_set.

**Explicit results** no value · nested operand in the contract.qb.from\_(doctype).select(expanded fields).where(doctype.name.isin(voucher\_set)).

**Local steps**

- If doctype\_name equals “Purchase Invoice”.
  - Set get\_doc\_fields from self.get\_purchase\_invoice\_fields.
- Otherwise.
  - If doctype\_name equals “Sales Invoice”.
    - Set get\_doc\_fields from self.get\_sales\_invoice\_fields.
  - Otherwise.
    - If doctype\_name equals “Payment Entry”.
      - Set get\_doc\_fields from self.get\_payment\_entry\_fields.
    - Otherwise.
      - If doctype\_name equals “Journal Entry”.
        - Set get\_doc\_fields from self.get\_journal\_entry\_fields.
      - Otherwise.
        - Return no value.
- Set doctype from Platform.qb.DocType(doctype\_name).
- Set fields from list(doctype.name, expanded get\_doc\_fields(doctype)).
- Return nested operand in the contract.qb.from\_(doctype).select(expanded fields).where(doctype.name.isin(voucher\_set)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L2984) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L992) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L78)

<a id="op-bff082bb024546"></a>
### Tax Withholding Details Report.get purchase invoice fields

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_purchase_invoice_fields`

**Inputs** self, doctype.

**Explicit results** list(doctype.grand\_total, doctype.base\_total, doctype.bill\_no.as\_(“supplier\_invoice\_no”), doctype.bill\_date.as\_(“supplier\_invoice\_date”)).

**Local steps**

- Return list(doctype.grand\_total, doctype.base\_total, doctype.bill\_no.as\_(“supplier\_invoice\_no”), doctype.bill\_date.as\_(“supplier\_invoice\_date”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L3375) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L991) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L77)

<a id="op-14efc7156df203"></a>
### Tax Withholding Details Report.get sales invoice fields

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_sales_invoice_fields`

**Inputs** self, doctype.

**Explicit results** list(doctype.grand\_total, doctype.base\_total).

**Local steps**

- Return list(doctype.grand\_total, doctype.base\_total).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L3490) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L79)

<a id="op-183fa56255bc9c"></a>
### Tax Withholding Details Report.get payment entry fields

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_payment_entry_fields`

**Inputs** self, doctype.

**Explicit results** list(doctype.paid\_amount\_after\_tax.as\_(“grand\_total”), doctype.base\_paid\_amount.as\_(“base\_total”)).

**Local steps**

- Return list(doctype.paid\_amount\_after\_tax.as\_(“grand\_total”), doctype.base\_paid\_amount.as\_(“base\_total”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L3551) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L990) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L76)

<a id="op-e109bc5d3714f8"></a>
### Tax Withholding Details Report.get journal entry fields

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_journal_entry_fields`

**Inputs** self, doctype.

**Explicit results** list(doctype.total\_debit.as\_(“grand\_total”), doctype.total\_debit.as\_(“base\_total”)).

**Local steps**

- Return list(doctype.total\_debit.as\_(“grand\_total”), doctype.total\_debit.as\_(“base\_total”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0282.json#L3655) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L988) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L74)

<a id="op-625fc7a0d63c4d"></a>
### Tax Withholding Details Report.get columns

`operation_enterprise_accounts_report_tax_withholding_details_business_behavior_tax_withholding_details_report_get_columns`

**Inputs** self.

**Explicit results** list(mapping(“label” → translated “Tax Withholding Category”, “options” → “Tax Withholding Category”, “fieldname” → “tax\_withholding\_category”, “fieldtype” → “Link”, …), mapping(“label” → translated “Tax I ….

**Local steps**

- Set party\_type from self.filters.get(“party\_type”, “Party”).
- Return list(mapping(“label” → translated “Tax Withholding Category”, “options” → “Tax Withholding Category”, “fieldname” → “tax\_withholding\_category”, “fieldtype” → “Link”, …), mapping(“label” → translated “Tax I ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L71)

## Record · Tax withholding entry

[Record definition](../../../../data/record-types/tax_withholding_entry.json)

<a id="op-b5ebb0936d89ae"></a>
### Tax Withholding Entry.set status

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_set_status`

**Inputs** self, status = no value.

**Local steps**

- If not status.
  - Set status from self.get\_status().
- Set self.status from status.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-113.md#op-8ac8f44cfb6fae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L1167) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L498)
