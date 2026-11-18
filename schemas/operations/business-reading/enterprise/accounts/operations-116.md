# Accounting and settlement · operations 116

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Tax withholding entry

[Record definition](../../../../data/record-types/tax_withholding_entry.json)

<a id="op-f2037932db9636"></a>
### Journal Tax Withholding.get category names

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_get_category_names`

**Inputs** self.

**Explicit results** list() · list(self.doc.tax\_withholding\_category).

**Local steps**

- If not self.doc.tax\_withholding\_category.
  - Return list().
- Return list(self.doc.tax\_withholding\_category).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L4739) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L50) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L422)

<a id="op-274c8c53054d7f"></a>
### Journal Tax Withholding.update taxable amounts

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_update_taxable_amounts`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.category\_details.
  - Return no value.
- Set net\_amount from self.\_calculate\_net\_total().
- Set category from next(iter(self.category\_details.values())).
- Set category at “taxable\_amount” from net\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate net total](operations-116.md#op-ea7af788ee9dd4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L4818) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L434)

<a id="op-ea7af788ee9dd4"></a>
### Journal Tax Withholding.calculate net total

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_calculate_net_total`

**Inputs** self.

**Explicit results** flt(sum(generator of (d.get(self.reverse\_field) − d.get(self.party\_field)) for d drawn from self.doc.get(“accounts”) where (nested operand in the contract.get(nested operand in the contract.account) does n ….

**Local steps**

- Bind dependencies get\_account\_type\_map.
- Set account\_type\_map from get\_account\_type\_map(self.doc.company).
- Return flt(sum(generator of (d.get(self.reverse\_field) − d.get(self.party\_field)) for d drawn from self.doc.get(“accounts”) where (nested operand in the contract.get(nested operand in the contract.account) does n ….
  - Draw d from self.doc.get(“accounts”), keep a combination only if ((account\_type\_map.get(d.account) does not belong to tuple(“Tax”, “Chargeable”) and d.account differs from self.party\_account and not d.get(“is\_tax\_withholding\_account”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in account\_type\_map.get(d.account) does not belong to tuple(“Tax”, “Chargeable”) → d.account differs from self.party\_account → not d.get(“is\_tax\_withholding\_account”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L4977) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L46) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L418)

<a id="op-429433646630dd"></a>
### Journal Tax Withholding.get conversion rate

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_get_conversion_rate`

**Inputs** self.

**Explicit results** self.party\_row.get(“exchange\_rate”, 1.0).

**Local steps**

- Return self.party\_row.get(“exchange\_rate”, 1.0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L5284) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L51) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L423)

<a id="op-cd1a8e95b2941d"></a>
### Journal Tax Withholding.calculate taxes and totals

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_calculate_taxes_and_totals`

**Inputs** self.

**Local steps**

- Evaluate self.doc.set\_amounts\_in\_company\_currency().
- Evaluate self.doc.set\_total\_debit\_credit().
- Evaluate self.doc.set\_against\_account().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L5351) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L47) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L419)

<a id="op-4844171c6b80f6"></a>
### Journal Tax Withholding.update tax rows

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_update_tax_rows`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot apply TDS against multiple parties in one entry”.

**Local steps**

- If not self.\_should\_apply\_tds().
  - Evaluate self.\_cleanup\_duplicate\_tds\_rows(no value).
  - Return no value.
- If self.has\_multiple\_parties.
  - Call the validation error handler Platform.throw(translated “Cannot apply TDS against multiple parties in one entry”).
- Set account\_amount\_map from self.\_calculate\_account\_wise\_amount().
- If not account\_amount\_map.
  - Return no value.
- Evaluate self.\_reset\_existing\_tds().
- For each tuple(account\_head, tax\_amount) in account\_amount\_map.items().
  - If not tax\_amount.
    - Continue with the next iteration or loop test.
  - Evaluate self.\_create\_or\_update\_tds\_row(account\_head, tax\_amount).
  - Evaluate self.\_update\_party\_amount(tax\_amount, is\_reversal = false).
- Evaluate self.\_recalculate\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [should apply tds](operations-116.md#op-46461fe1228afc), [cleanup duplicate tds rows](operations-116.md#op-0c4aaca8b3a7fc), [reset existing tds](operations-116.md#op-4a8d983a081b81), [create or update tds row](operations-116.md#op-81d7116055339b), [update party amount](operations-116.md#op-00c4ba123e0657), [recalculate totals](operations-116.md#op-4991c7d7609679).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L5448) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L433)

<a id="op-46461fe1228afc"></a>
### Journal Tax Withholding.should apply tds

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_should_apply_tax_deducted_at_source`

**Inputs** self.

**Explicit results** (self.doc.apply\_tds and self.doc.voucher\_type belongs to tuple(“Debit Note”, “Credit Note”)).

**Local steps**

- Return (self.doc.apply\_tds and self.doc.voucher\_type belongs to tuple(“Debit Note”, “Credit Note”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.apply\_tds → self.doc.voucher\_type belongs to tuple(“Debit Note”, “Credit Note”).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L5791) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L59) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L431)

<a id="op-4a8d983a081b81"></a>
### Journal Tax Withholding.reset existing tds

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_reset_existing_tax_deducted_at_source`

**Inputs** self.

**Local steps**

- For each row in self.existing\_tds\_rows.
  - Set tds\_amount from flt((row.get(“credit”) − row.get(“debit”)), self.precision).
  - If not tds\_amount.
    - Continue with the next iteration or loop test.
  - Evaluate self.\_update\_party\_amount(tds\_amount, is\_reversal = true).
  - Evaluate row.update(mapping(“credit” → 0, “credit\_in\_account\_currency” → 0, “debit” → 0, “debit\_in\_account\_currency” → 0)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update party amount](operations-116.md#op-00c4ba123e0657).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L5875) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L56) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L428)

<a id="op-00c4ba123e0657"></a>
### Journal Tax Withholding.update party amount

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_update_party_amount`

**Inputs** self, amount, is\_reversal = false.

**Local steps**

- Set amount from flt(amount, self.precision).
- Set amount\_in\_party\_currency from flt((amount ÷ self.party\_row.get(“exchange\_rate”, 1)), self.precision).
- Set active\_field from self.party\_field when self.party\_row.get(self.party\_field), otherwise self.reverse\_field.
  - Value choice on self.party\_row.get(self.party\_field) — true gives self.party\_field, false gives self.reverse\_field.
- If active\_field equals self.reverse\_field.
  - Set amount from negative amount.
  - Set amount\_in\_party\_currency from negative amount\_in\_party\_currency.
- Set direction from 1 when self.party\_type equals “Customer”, otherwise negative 1.
  - Value choice on self.party\_type equals “Customer” — true gives 1, false gives negative 1.
- If is\_reversal.
  - Set direction from negative direction.
- Set adjustment from (amount × direction).
- Set adjustment\_in\_party\_currency from (amount\_in\_party\_currency × direction).
- Set active\_field\_account\_currency from formatted text {active\_field}\_in\_account\_currency.
- Evaluate self.party\_row.update(mapping(active\_field → flt((nested operand in the contract.party\_row.get(active\_field) + adjustment), self.precision), active\_field\_account\_currency → flt((nested operand in the contr ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L6149) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L432)

<a id="op-81d7116055339b"></a>
### Journal Tax Withholding.create or update tds row

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_create_or_update_tax_deducted_at_source_row`

**Inputs** self, account\_head, tax\_amount.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Bind dependencies get\_account\_currency.
- Bind dependencies \_get\_exchange\_rate.
- Set account\_currency from get\_account\_currency(account\_head).
- Set company\_currency from Platform.get\_cached\_value(“Company”, self.doc.company, “default\_currency”).
- Set exchange\_rate from \_get\_exchange\_rate(account\_currency, company\_currency, self.doc.posting\_date).
- Set tax\_amount from flt(tax\_amount, self.precision).
- Set tax\_amount\_in\_account\_currency from flt((tax\_amount ÷ exchange\_rate), self.precision).
- Set tax\_row from no value.
- For each row in self.doc.get(“accounts”).
  - If (row.account equals account\_head and row.get(“is\_tax\_withholding\_account”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.account equals account\_head → row.get(“is\_tax\_withholding\_account”).
    - Set tax\_row from row.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not tax\_row.
  - Set tax\_row from self.doc.append(“accounts”, mapping(“account” → account\_head, “account\_currency” → account\_currency, “exchange\_rate” → exchange\_rate, “cost\_center” → (self.doc.get(“cost\_center”) or Enterprise.get\_default\_ ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“cost\_center”) → Enterprise.get\_default\_cost\_center(self.doc.company).
- Evaluate tax\_row.update(mapping(“credit” → tax\_amount, “credit\_in\_account\_currency” → tax\_amount\_in\_account\_currency, “debit” → 0, “debit\_in\_account\_currency” → 0)).
- Evaluate self.\_cleanup\_duplicate\_tds\_rows(tax\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cleanup duplicate tds rows](operations-116.md#op-0c4aaca8b3a7fc).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.doc.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L6704) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L421)

<a id="op-0c4aaca8b3a7fc"></a>
### Journal Tax Withholding.cleanup duplicate tds rows

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_cleanup_duplicate_tax_deducted_at_source_rows`

**Inputs** self, current\_tax\_row.

**Local steps**

- Set rows\_to\_remove from list of row for row drawn from self.doc.get(“accounts”) where (row.get(“is\_tax\_withholding\_account”) and row differs from current\_tax\_row).
  - Draw row from self.doc.get(“accounts”), keep a combination only if ((row.get(“is\_tax\_withholding\_account”) and row differs from current\_tax\_row)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.get(“is\_tax\_withholding\_account”) → row differs from current\_tax\_row.
- For each row in rows\_to\_remove.
  - Evaluate self.doc.remove(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0208.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L420)

<a id="op-4991c7d7609679"></a>
### Journal Tax Withholding.recalculate totals

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_recalculate_totals`

**Inputs** self.

**Local steps**

- Evaluate self.doc.set\_amounts\_in\_company\_currency().
- Evaluate self.doc.set\_total\_debit\_credit().
- Evaluate self.doc.set\_against\_account().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0208.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L55) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L427)

<a id="op-e5321e71c311d7"></a>
### Journal Tax Withholding.is tax withholding applicable

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_is_tax_withholding_applicable`

**Inputs** self.

**Explicit results** false · true.

**Local steps**

- If not self.\_should\_apply\_tds().
  - Set self.doc.tax\_withholding\_entries from list().
  - Return false.
- If not self.doc.tax\_withholding\_category.
  - Set self.doc.tax\_withholding\_entries from list().
  - Return false.
- Return true.

**Methods declared on this owner** [should apply tds](operations-116.md#op-46461fe1228afc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0208.json#L287) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L54) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L426)

<a id="op-18b75e53f29b0a"></a>
### Journal Tax Withholding.get linked payments

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_get_linked_payments`

**Inputs** self.

**Explicit results** Platform.\_dict().

**Local steps**

- Return Platform.\_dict().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0208.json#L430) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L424)

<a id="op-4c500654504f75"></a>
### Reset idx

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_reset_position`

**Inputs** docs\_to\_reset\_idx.

**Record and data access** read DOCTYPE via get\_all.

**State and service calls** request bulk\_update on DOCTYPE.

**Local steps**

- Set updates from mapping().
- For each tuple(doctype, docname) in docs\_to\_reset\_idx.
  - Set names from Platform.get\_all(DOCTYPE, filters = mapping(“parent” → docname, “parenttype” → doctype, “docstatus” → 1), pluck = “name”).
  - For each tuple(idx, name) in enumerate(names, start = 1).
    - Set updates at name from mapping(“idx” → idx).
- If updates.
  - Evaluate Platform.db.bulk\_update(DOCTYPE, updates, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0208.json#L479) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L444)

## Report · Tds computation summary

<a id="op-bc4219e15c3ba6"></a>
### TDSComputation Summary Report.validate filters

`operation_enterprise_accounts_report_tax_deducted_at_source_computation_summary_business_behavior_tax_deducted_at_source_computation_summary_report_validate_filters`

**Inputs** self.

**Explicit failure paths** validation helper — translated “From Date and To Date lie in different Fiscal Year”.

**Local steps**

- Evaluate super().validate\_filters().
- Set from\_year from get\_fiscal\_year(self.filters.from\_date) at 0.
- Set to\_year from get\_fiscal\_year(self.filters.to\_date) at 0.
- If from\_year differs from to\_year.
  - Call the validation error handler Platform.throw(translated “From Date and To Date lie in different Fiscal Year”).
- Set self.filters.fiscal\_year from from\_year.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0283.json#L1805) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L980) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L66)

<a id="op-d9adcff4b90d2c"></a>
### TDSComputation Summary Report.get data

`operation_enterprise_accounts_report_tax_deducted_at_source_computation_summary_business_behavior_tax_deducted_at_source_computation_summary_report_get_data`

**Inputs** self.

**Explicit results** self.group\_rows(super().get\_data()).

**Local steps**

- Return self.group\_rows(super().get\_data()).

**Methods declared on this owner** [group rows](operations-116.md#op-87e57b9b2ef5d3).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0283.json#L2027) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L64)

<a id="op-87e57b9b2ef5d3"></a>
### TDSComputation Summary Report.group rows

`operation_enterprise_accounts_report_tax_deducted_at_source_computation_summary_business_behavior_tax_deducted_at_source_computation_summary_report_group_rows`

**Inputs** self, data.

**Explicit results** list(grouped.values()).

**Local steps**

- Set grouped from mapping().
- For each row in data.
  - Set key from tuple(generator of row.get(f) for f drawn from self.GROUP\_BY\_FIELDS).
    - Draw f from self.GROUP\_BY\_FIELDS.
  - Set bucket from grouped.setdefault(key, mapping(expand mapping of f → row.get(f) for f drawn from self.CARRY\_OVER\_FIELDS, expand mapping of f → 0.0 for f drawn from self.AGGREGATE\_FIELDS)).
    - Draw f from self.CARRY\_OVER\_FIELDS.
    - Draw f from self.AGGREGATE\_FIELDS.
  - For each f in self.AGGREGATE\_FIELDS.
    - Update bucket at f using + (row.get(f) or 0.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(f) → 0.0.
- Return list(grouped.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0283.json#L2102) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L65)

<a id="op-d4afebd6dd8b67"></a>
### TDSComputation Summary Report.get columns

`operation_enterprise_accounts_report_tax_deducted_at_source_computation_summary_business_behavior_tax_deducted_at_source_computation_summary_report_get_columns`

**Inputs** self.

**Explicit results** list(mapping(“label” → translated “Tax Id”, “fieldname” → “tax\_id”, “fieldtype” → “Data”, “width” → 90), mapping(“label” → translated party\_type, “fieldname” → “party”, “fieldtype” → “Dynamic Link”, “optio ….

**Local steps**

- Set party\_type from self.filters.get(“party\_type”, “Party”).
- Return list(mapping(“label” → translated “Tax Id”, “fieldname” → “tax\_id”, “fieldtype” → “Data”, “width” → 90), mapping(“label” → translated party\_type, “fieldname” → “party”, “fieldtype” → “Dynamic Link”, “optio ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0283.json#L2445) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L63)

## Report · Trial balance

<a id="op-24a86282a9f90b"></a>
### Execute

`operation_enterprise_accounts_report_trial_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_company\_permission(filters.company).
- Evaluate validate\_filters(filters).
- Set data from get\_data(filters).
- Set columns from get\_columns().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1009) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L95)

<a id="op-9ff976d30e0cd5"></a>
### Validate company permission

`operation_enterprise_binding_enterprise_accounts_report_trial_balance_trial_balance_validate_company_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** company.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1277)

<a id="op-bcb0ad0e56cd3a"></a>
### Validate filters

`operation_enterprise_accounts_report_trial_balance_business_behavior_validate_filters`

**Inputs** filters.

**Record and data access** read “Fiscal Year” via get\_cached\_value.

**State and service calls** msgprint with translated “From Date should be within the Fiscal Year. Assuming From Date = {0}”.format(formatdate(filters.year\_start\_date)) · msgprint with translated “To Date should be within the Fiscal Year. Assuming To Date = {0}”.format(formatdate(filters.year\_end\_date)).

**Explicit failure paths** validation helper — translated “Fiscal Year {0} is required”.format(filters.fiscal\_year) · validation helper — translated “Fiscal Year {0} does not exist”.format(filters.fiscal\_year).

**Local steps**

- If not filters.fiscal\_year.
  - Call the validation error handler Platform.throw(translated “Fiscal Year {0} is required”.format(filters.fiscal\_year)).
- Set fiscal\_year from Platform.get\_cached\_value(“Fiscal Year”, filters.fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true).
- If not fiscal\_year.
  - Call the validation error handler Platform.throw(translated “Fiscal Year {0} does not exist”.format(filters.fiscal\_year)).
- Otherwise.
  - Set filters.year\_start\_date from getdate(fiscal\_year.year\_start\_date).
  - Set filters.year\_end\_date from getdate(fiscal\_year.year\_end\_date).
- If not filters.from\_date.
  - Set filters.from\_date from filters.year\_start\_date.
- If not filters.to\_date.
  - Set filters.to\_date from filters.year\_end\_date.
- Set filters.from\_date from getdate(filters.from\_date).
- Set filters.to\_date from getdate(filters.to\_date).
- Evaluate validate\_date\_range(filters).
- If (filters.from\_date &lt; filters.year\_start\_date or filters.from\_date &gt; filters.year\_end\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.from\_date &lt; filters.year\_start\_date → filters.from\_date &gt; filters.year\_end\_date.
  - Evaluate Platform.msgprint(translated “From Date should be within the Fiscal Year. Assuming From Date = {0}”.format(formatdate(filters.year\_start\_date))).
  - Set filters.from\_date from filters.year\_start\_date.
- If (filters.to\_date &lt; filters.year\_start\_date or filters.to\_date &gt; filters.year\_end\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.to\_date &lt; filters.year\_start\_date → filters.to\_date &gt; filters.year\_end\_date.
  - Evaluate Platform.msgprint(translated “To Date should be within the Fiscal Year. Assuming To Date = {0}”.format(formatdate(filters.year\_end\_date))).
  - Set filters.to\_date from filters.year\_end\_date.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Fiscal Year”, filters.fiscal\_year, list(“year\_start\_date”, “year\_end\_date”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1026) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L112)

<a id="op-2ed8dc5a089aee"></a>
### Get data

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_data`

**Inputs** filters.

**Record and data access** execute query text (SELECT, Account) · read “Accounts Settings” via get\_single\_value.

**Explicit results** no value · data.

**Local steps**

- Set accounts from Platform.db.sql(query text (SELECT, Account), filters.company, as\_dict = true).
- Set company\_currency from (filters.presentation\_currency or Enterprise.get\_company\_currency(filters.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.presentation\_currency → Enterprise.get\_company\_currency(filters.company).
- Set ignore\_is\_opening from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).
- If not accounts.
  - Return no value.
- Set tuple(accounts, accounts\_by\_name, parent\_children\_map) from filter\_accounts(accounts).
- Set gl\_entries\_by\_account from mapping().
- Set opening\_balances from get\_opening\_balances(filters, ignore\_is\_opening).
- Evaluate set\_gl\_entries\_by\_account(filters.company, filters.from\_date, filters.to\_date, filters, root\_lft = no value, root\_rgt = no value, ignore\_closing\_entries = not flt(filters.with\_period\_closing\_entry\_for\_curr ….
- Evaluate calculate\_values(accounts, gl\_entries\_by\_account, opening\_balances, filters.get(“show\_net\_values”), ignore\_is\_opening = ignore\_is\_opening).
- Evaluate accumulate\_values\_into\_parents(accounts, accounts\_by\_name).
- Set data from prepare\_data(accounts, filters, parent\_children\_map, company\_currency).
- Set data from filter\_out\_zero\_value\_rows(data, parent\_children\_map, show\_zero\_values = filters.get(“show\_zero\_values”)).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “ignore\_is\_opening\_check\_for\_reporting”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1014) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L100)

<a id="op-5b5dddb34d1aeb"></a>
### Get opening balances

`operation_enterprise_accounts_report_trial_balance_business_behavior_get_opening_balances`

**Inputs** filters, ignore\_is\_opening, exchange\_rate = no value, ignore\_reporting\_currency = true.

**Explicit results** balance\_sheet\_opening.

**Local steps**

- Set balance\_sheet\_opening from get\_rootwise\_opening\_balances(filters, “Balance Sheet”, ignore\_is\_opening, exchange\_rate, …).
- Set pl\_opening from get\_rootwise\_opening\_balances(filters, “Profit and Loss”, ignore\_is\_opening, exchange\_rate, …).
- Evaluate balance\_sheet\_opening.update(pl\_opening).
- Return balance\_sheet\_opening.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0284.json#L3568) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1018) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L104)
