# Accounting and settlement · operations 115

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Tax withholding entry

[Record definition](../../../../data/record-types/tax_withholding_entry.json)

<a id="op-6a037ced128185"></a>
### Tax Withholding Controller.create base entry

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_create_base_entry`

**Inputs** self, source\_entry, category, tax\_rate, default\_obj.

**Explicit results** entry.

**Local steps**

- Set entry from mapping().
- If default\_obj.
  - Evaluate entry.update(default\_obj).
- Evaluate entry.update(mapping(“taxable\_doctype” → source\_entry.taxable\_doctype, “taxable\_name” → source\_entry.taxable\_name, “taxable\_date” → source\_entry.taxable\_date, “tax\_withholding\_category” → category.name, …)).
- Return entry.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L1287) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L455)

<a id="op-6aff5e22ca2dfe"></a>
### Tax Withholding Controller.should include entry

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_should_include_entry`

**Inputs** self, entry.

**Explicit results** (entry.get(“taxable\_name”) equals self.doc.name or entry.get(“withholding\_name”) equals self.doc.name).

**Local steps**

- Return (entry.get(“taxable\_name”) equals self.doc.name or entry.get(“withholding\_name”) equals self.doc.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“taxable\_name”) equals self.doc.name → entry.get(“withholding\_name”) equals self.doc.name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L1604) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L484)

<a id="op-00dbac452ee486"></a>
### Tax Withholding Controller.compute withheld amount

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_compute_withheld_amount`

**Inputs** self, taxable\_amount, tax\_rate, round\_off\_tax\_amount = false.

**Explicit results** flt(amount, 0) · flt(amount, self.precision).

**Local steps**

- Set amount from ((taxable\_amount × tax\_rate) ÷ 100).
- If round\_off\_tax\_amount.
  - Return flt(amount, 0).
- Return flt(amount, self.precision).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L1744) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L454)

<a id="op-f8d6aed7e728ed"></a>
### Tax Withholding Controller.process withholding entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_process_withholding_entries`

**Inputs** self.

**Local steps**

- Evaluate self.update\_tax\_rows().
- For each entry in self.doc.tax\_withholding\_entries.
  - Evaluate entry.set\_status(entry.status).
  - Evaluate entry.validate\_adjustments().
  - Evaluate entry.validate\_tax\_withheld\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update tax rows](operations-114.md#op-3de1299632b25a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L1888) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L481)

<a id="op-c5187147babb7a"></a>
### Tax Withholding Controller.on submit

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_on_submit`

**Inputs** self.

**Local steps**

- For each entry in self.doc.tax\_withholding\_entries.
  - Evaluate entry.\_process\_tax\_withholding\_adjustments().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2039) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L476)

<a id="op-1ab94189b9116b"></a>
### Tax Withholding Controller.on cancel

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_on_cancel`

**Inputs** self.

**Local steps**

- For each entry in self.doc.tax\_withholding\_entries.
  - Evaluate entry.\_clear\_old\_references().
  - Evaluate entry.set\_status().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2124) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L475)

<a id="op-af74397406c099"></a>
### Tax Withholding Controller.is tax withholding applicable

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_is_tax_withholding_applicable`

**Inputs** self.

**Explicit results** false · true.

**Local steps**

- Evaluate self.\_clear\_existing\_tax\_amounts().
- If (not self.doc.apply\_tds or self.doc.get(“is\_opening”) equals “Yes” or not self.\_get\_category\_names()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.doc.apply\_tds → self.doc.get(“is\_opening”) equals “Yes” → not self.\_get\_category\_names().
  - Set self.doc.tax\_withholding\_entries from list().
  - Return false.
- Return true.

**Methods declared on this owner** [clear existing tax amounts](operations-115.md#op-79be5de6107fcc), [get category names](operations-113.md#op-e09b222672920a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2227) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L472)

<a id="op-79be5de6107fcc"></a>
### Tax Withholding Controller.clear existing tax amounts

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_clear_existing_tax_amounts`

**Inputs** self.

**Local steps**

- For each row in self.doc.taxes.
  - If (row.is\_tax\_withholding\_account and row.tax\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_tax\_withholding\_account → row.tax\_amount.
    - Set row.tax\_amount from 0.
    - Set row.base\_tax\_amount\_after\_discount\_amount from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2404) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L81) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L453)

<a id="op-8a27df125d28f8"></a>
### Tax Withholding Controller.calculate taxes and totals

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_calculate_taxes_and_totals`

**Inputs** self.

**Local steps**

- Evaluate self.doc.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2519) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L450)

<a id="op-7c7cb348569578"></a>
### Tax Withholding Controller.get conversion rate

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_conversion_rate`

**Inputs** self.

**Explicit results** (self.doc.get(“conversion\_rate”) or 1).

**Local steps**

- Return (self.doc.get(“conversion\_rate”) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.get(“conversion\_rate”) → 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2572) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L466)

<a id="op-572c73e3677949"></a>
### Tax Withholding Controller.on validate

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_on_validate`

**Inputs** self.

**Local steps**

- If self.\_is\_tax\_withholding\_applicable().
  - Evaluate self.calculate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is tax withholding applicable](operations-115.md#op-af74397406c099), [calculate](operations-113.md#op-053df607fcda69).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2645) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L477)

<a id="op-bd035789519833"></a>
### Purchase Tax Withholding.initialize

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_purchase_tax_withholding_initialize`

**Inputs** self, doc.

**Local steps**

- Evaluate super().\_\_init\_\_(doc).
- Set self.party\_type from “Supplier”.
- Set self.party from doc.supplier.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2719) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L443)

<a id="op-3dd31805d592df"></a>
### Sales Tax Withholding.initialize

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_sales_tax_withholding_initialize`

**Inputs** self, doc.

**Local steps**

- Evaluate super().\_\_init\_\_(doc).
- Set self.party\_type from “Customer”.
- Set self.party from doc.customer.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2830) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L445)

<a id="op-472d496b1ec9a7"></a>
### Payment Tax Withholding.initialize

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_initialize`

**Inputs** self, doc.

**Local steps**

- Evaluate super().\_\_init\_\_(doc).
- Set self.party\_type from doc.party\_type.
- Set self.party from doc.party.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L2941) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L440)

<a id="op-95b8976364c147"></a>
### Payment Tax Withholding.get category names

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_get_category_names`

**Inputs** self.

**Explicit results** list() · list(self.doc.tax\_withholding\_category).

**Local steps**

- If not self.doc.tax\_withholding\_category.
  - Return list().
- Return list(self.doc.tax\_withholding\_category).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3051) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L436)

<a id="op-93b9137f389baf"></a>
### Payment Tax Withholding.update taxable amounts

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_update_taxable_amounts`

**Inputs** self.

**Local steps**

- Set category from next(iter(self.category\_details.values())).
- Set taxable\_amount\_in\_party\_currency from self.doc.unallocated\_amount.
- Update taxable\_amount\_in\_party\_currency using + sum(generator of flt(d.allocated\_amount) for d drawn from self.doc.references where d.reference\_doctype belongs to get\_advance\_payment\_doctypes()).
  - Draw d from self.doc.references, keep a combination only if (d.reference\_doctype belongs to get\_advance\_payment\_doctypes()).
- Set exchange\_rate from self.get\_conversion\_rate().
- Set taxable\_amount from flt((taxable\_amount\_in\_party\_currency × exchange\_rate), self.precision).
- Set category at “taxable\_amount” from taxable\_amount.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get conversion rate](operations-115.md#op-efaa1536f9afe4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3130) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L442)

<a id="op-efaa1536f9afe4"></a>
### Payment Tax Withholding.get conversion rate

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_get_conversion_rate`

**Inputs** self.

**Explicit results** (self.doc.source\_exchange\_rate or 1) · (self.doc.target\_exchange\_rate or 1).

**Local steps**

- If self.doc.payment\_type equals “Receive”.
  - Return (self.doc.source\_exchange\_rate or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.source\_exchange\_rate → 1.
- Otherwise.
  - Return (self.doc.target\_exchange\_rate or 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doc.target\_exchange\_rate → 1.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3422) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L437)

<a id="op-ab99afbf60bcb6"></a>
### Payment Tax Withholding.calculate taxes and totals

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_calculate_taxes_and_totals`

**Inputs** self.

**Local steps**

- Evaluate self.doc.apply\_taxes().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3533) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L63) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L435)

<a id="op-24c35b081c0061"></a>
### Payment Tax Withholding.get open entries for category

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_get_open_entries_for_category`

**Inputs** self, category.

**Explicit results** open\_entries.

**Local steps**

- Set open\_entries from mapping(“under\_withheld” → deque(), “over\_withheld” → deque()).
- Set current\_entry from Platform.\_dict(mapping(expand self.\_create\_default\_entry(category), “taxable\_amount” → category.taxable\_amount, “taxable\_doctype” → empty text, “taxable\_name” → empty text, …)).
- Evaluate open\_entries at “over\_withheld”.append(current\_entry).
- Return open\_entries.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3586) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L438)

<a id="op-87e6d7e6e0b2b6"></a>
### Payment Tax Withholding.is threshold crossed for category

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_is_threshold_crossed_for_category`

**Inputs** self, category.

**Explicit results** true.

**Local steps**

- Return true.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3834) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L441)

<a id="op-84197f2e3e1333"></a>
### Payment Tax Withholding.get unused threshold

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_payment_tax_withholding_get_unused_threshold`

**Inputs** self, category.

**Explicit results** 0.

**Local steps**

- Return 0.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3878) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L439)

<a id="op-81415947e0395f"></a>
### Journal Tax Withholding.initialize

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_initialize`

**Inputs** self, doc.

**Local steps**

- Evaluate super().\_\_init\_\_(doc).
- Set self.party from no value.
- Set self.party\_type from no value.
- Set self.party\_account from no value.
- Set self.party\_row from no value.
- Set self.existing\_tds\_rows from list().
- Set self.precision from no value.
- Set self.has\_multiple\_parties from false.
- Set self.party\_field from no value.
- Set self.reverse\_field from no value.
- Evaluate self.\_setup\_party\_info().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup party info](operations-115.md#op-c22303f46a04f1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L3922) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L53) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L425)

<a id="op-c22303f46a04f1"></a>
### Journal Tax Withholding.setup party info

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_setup_party_info`

**Inputs** self.

**Local steps**

- For each row in self.doc.get(“accounts”).
  - If (row.party\_type belongs to tuple(“Customer”, “Supplier”) and row.party).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.party\_type belongs to tuple(“Customer”, “Supplier”) → row.party.
    - If (self.party and row.party differs from self.party).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.party → row.party differs from self.party.
      - Set self.has\_multiple\_parties from true.
    - If not self.party.
      - Set self.party from row.party.
      - Set self.party\_type from row.party\_type.
      - Set self.party\_account from row.account.
      - Set self.party\_row from row.
  - If row.get(“is\_tax\_withholding\_account”).
    - Evaluate self.existing\_tds\_rows.append(row).
- If self.party\_type.
  - Evaluate self.\_setup\_direction\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup direction fields](operations-115.md#op-09a0cfd3616422).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L4157) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L430)

<a id="op-09a0cfd3616422"></a>
### Journal Tax Withholding.setup direction fields

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_journal_tax_withholding_setup_direction_fields`

**Inputs** self.

**Local steps**

- If self.party\_type equals “Supplier”.
  - Set self.party\_field from “credit”.
  - Set self.reverse\_field from “debit”.
- Otherwise.
  - Set self.party\_field from “debit”.
  - Set self.reverse\_field from “credit”.
- Set self.precision from self.doc.precision(self.party\_field, self.party\_row).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0207.json#L4539) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L57) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L429)
