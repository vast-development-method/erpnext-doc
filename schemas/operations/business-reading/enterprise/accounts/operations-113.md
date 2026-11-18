# Accounting and settlement · operations 113

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Tax withholding entry

[Record definition](../../../../data/record-types/tax_withholding_entry.json)

<a id="op-8ac8f44cfb6fae"></a>
### Tax Withholding Entry.get status

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_get_status`

**Inputs** self.

**Explicit results** “Cancelled” · “Under Withheld” · “Over Withheld” · “Settled”.

**Local steps**

- <a id="op-8ac8f44cfb6fae-guard-2"></a>If self.docstatus equals 2.
  - Return “Cancelled”.
- If (not self.withholding\_name and not self.under\_withheld\_reason).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.withholding\_name → not self.under\_withheld\_reason.
  - Return “Under Withheld”.
- Otherwise.
  - If not self.taxable\_name.
    - Return “Over Withheld”.
  - Otherwise.
    - Return “Settled”.

**Derived branch illustrations**

- At the comparison self.docstatus equals 2, self.docstatus = 2 (cancelled) selects the branch that returns “Cancelled”. With self.docstatus = 0 (draft), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8ac8f44cfb6fae-guard-2)

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L1265) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L492)

<a id="op-402ee2217dd5d5"></a>
### Tax Withholding Entry.validate adjustments

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_validate_adjustments`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Cannot create entry with different taxable AND withholding document links.”.format(self.idx).

**Local steps**

- If (self.is\_taxable\_different and self.is\_withholding\_different).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_taxable\_different → self.is\_withholding\_different.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Cannot create entry with different taxable AND withholding document links.”.format(self.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L1405) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L499)

<a id="op-67b8852da31b2d"></a>
### Tax Withholding Entry.validate tax withheld amount

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_validate_tax_withheld_amount`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Withholding Amount {1} does not match calculated amount {2}.”.format(self.idx, self.withholding\_amount, tax\_to\_withheld).

**Local steps**

- If (not self.withholding\_name or self.under\_withheld\_reason).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.withholding\_name → self.under\_withheld\_reason.
  - Return no value.
- Set precision from self.precision(“withholding\_amount”).
- Set allowance from 0.5.
- Set tax\_to\_withheld from flt((self.taxable\_amount × (self.tax\_rate ÷ 100)), precision).
- Set diff from abs((tax\_to\_withheld − self.withholding\_amount)).
- If diff &gt; allowance.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Withholding Amount {1} does not match calculated amount {2}.”.format(self.idx, self.withholding\_amount, tax\_to\_withheld)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L1526) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L500)

<a id="op-e38ce432f51199"></a>
### Tax Withholding Entry.is taxable different

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_is_taxable_different`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (self.taxable\_doctype differs from self.parenttype or self.taxable\_name differs from self.parent).

**Local steps**

- Return (self.taxable\_doctype differs from self.parenttype or self.taxable\_name differs from self.parent).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.taxable\_doctype differs from self.parenttype → self.taxable\_name differs from self.parent.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L1828) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L123) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L495)

<a id="op-9f38c845cf9c06"></a>
### Tax Withholding Entry.is withholding different

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_is_withholding_different`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (self.withholding\_doctype differs from self.parenttype or self.withholding\_name differs from self.parent).

**Local steps**

- Return (self.withholding\_doctype differs from self.parenttype or self.withholding\_name differs from self.parent).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.withholding\_doctype differs from self.parenttype → self.withholding\_name differs from self.parent.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L1924) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L124) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L496)

<a id="op-4b127a0b21371d"></a>
### Tax Withholding Entry.process tax withholding adjustments

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_process_tax_withholding_adjustments`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-4b127a0b21371d-guard-2"></a>If self.status differs from “Settled”.
  - Return no value.
- If self.is\_taxable\_different.
  - Evaluate self.\_adjust\_against\_old\_entries(field\_type = “taxable”).
- Otherwise.
  - If self.is\_withholding\_different.
    - Evaluate self.\_adjust\_against\_old\_entries(field\_type = “withholding”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status differs from “Settled”, self.status = “Under Withheld” selects the branch that returns no value. With self.status = “Settled”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4b127a0b21371d-guard-2)

**Methods declared on this owner** [adjust against old entries](operations-113.md#op-238469ac9fa0ae).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L2020) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L497)

<a id="op-238469ac9fa0ae"></a>
### Tax Withholding Entry.adjust against old entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_adjust_against_old_entries`

**Inputs** self, field\_type.

**Declared result** set.

**Record and data access** read DOCTYPE via get\_all · resolve a document from DOCTYPE via get\_doc.

**State and service calls** request set\_value on DOCTYPE · request copy\_doc for old\_entry · call insert on new\_entry.

**Explicit failure paths** validation helper — translated “Row #{0}: Could not find enough {1} entries to match. Remaining amount: {2}”.format(self.idx, status\_to\_find, remaining\_amount).

**Local steps**

- Set doctype\_field from formatted text {field\_type}\_doctype.
- Set docname\_field from formatted text {field\_type}\_name.
- Set amount\_field from formatted text {field\_type}\_amount.
- Set status\_to\_find from “Under Withheld” when field\_type equals “taxable”, otherwise “Over Withheld”.
  - Value choice on field\_type equals “taxable” — true gives “Under Withheld”, false gives “Over Withheld”.
- If not self.tax\_rate.
  - Set amount\_field from “taxable\_amount”.
- Set old\_entries from Platform.get\_all(DOCTYPE, filters = mapping(“tax\_withholding\_category” → self.tax\_withholding\_category, “status” → status\_to\_find, doctype\_field → self.get(doctype\_field), docname\_field → self.get(docname\_ ….
- Set value\_direction from negative 1 when self.get(amount\_field) &lt; 0, otherwise 1.
  - Value choice on self.get(amount\_field) &lt; 0 — true gives negative 1, false gives 1.
- Set remaining\_amount from abs(self.get(amount\_field)).
- Set docs\_needing\_reindex from set().
- Set precision from self.precision(“taxable\_amount”).
- For each old\_entry\_data in old\_entries.
  - Set old\_entry from Platform.get\_doc(DOCTYPE, expanded names old\_entry\_data).
  - Set old\_amount from abs(old\_entry.get(amount\_field)).
  - If (old\_entry.get(amount\_field) × value\_direction) &lt; 0.
    - Continue with the next iteration or loop test.
  - Set amount\_we\_can\_match from min(old\_amount, remaining\_amount).
  - Set proportion from (amount\_we\_can\_match ÷ old\_amount) when old\_amount, otherwise 0.
    - Value choice on old\_amount — true gives (amount\_we\_can\_match ÷ old\_amount), false gives 0.
  - Set values\_to\_update from self.\_get\_values\_to\_update(old\_entry, proportion, field\_type).
  - If old\_amount ≤ amount\_we\_can\_match.
    - Evaluate Platform.db.set\_value(DOCTYPE, old\_entry.name, values\_to\_update).
  - Otherwise.
    - Set balance\_amount from ((old\_amount − amount\_we\_can\_match) × value\_direction).
    - Set balance\_values from self.\_get\_balance\_values\_to\_update(old\_entry, proportion, field\_type).
    - Set balance\_values at amount\_field from balance\_amount.
    - Evaluate Platform.db.set\_value(DOCTYPE, old\_entry.name, balance\_values).
    - Set values\_to\_update at “withholding\_amount” from (old\_entry.withholding\_amount × proportion).
    - Set values\_to\_update at “taxable\_amount” from (old\_entry.taxable\_amount × proportion).
    - If self.tax\_rate differs from old\_entry.tax\_rate.
      - If not self.tax\_rate.
        - Set values\_to\_update at “withholding\_amount” from 0.
      - Otherwise.
        - Set values\_to\_update at “taxable\_amount” from flt(((values\_to\_update at “withholding\_amount” × 100) ÷ self.tax\_rate), precision).
    - Set new\_entry from Platform.copy\_doc(old\_entry).
    - Evaluate new\_entry.update(values\_to\_update).
    - Evaluate new\_entry.insert().
    - Evaluate docs\_needing\_reindex.add(tuple(old\_entry.parenttype, old\_entry.parent)).
  - Update remaining\_amount using − amount\_we\_can\_match.
  - <a id="op-238469ac9fa0ae-guard-89"></a>If remaining\_amount ≤ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
- After normal loop exhaustion.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Could not find enough {1} entries to match. Remaining amount: {2}”.format(self.idx, status\_to\_find, remaining\_amount)).
- Evaluate \_reset\_idx(docs\_needing\_reindex).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison remaining\_amount ≤ 0, remaining\_amount = 0 selects the branch that exits the enclosing loop. With remaining\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-238469ac9fa0ae-guard-89)

**Methods declared on this owner** [get values to update](operations-113.md#op-6c235e375a0214), [get balance values to update](operations-113.md#op-89b99568d228ac).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L489)

<a id="op-6c235e375a0214"></a>
### Tax Withholding Entry.get values to update

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_get_values_to_update`

**Inputs** self, old\_entry, proportion, field\_type.

**Explicit results** values.

**Local steps**

- Set field\_to\_update from “withholding” when field\_type equals “taxable”, otherwise “taxable”.
  - Value choice on field\_type equals “taxable” — true gives “withholding”, false gives “taxable”.
- Set values from mapping(formatted text {field\_to\_update}\_amount → (self.get(formatted text {field\_to\_update}\_amount) × proportion), formatted text {field\_to\_update}\_doctype → self.get(formatted text {field\_to\_update}\_doct ….
- If field\_to\_update equals “taxable”.
  - Evaluate values.update(currency = self.currency, conversion\_rate = self.conversion\_rate, under\_withheld\_reason = self.under\_withheld\_reason, lower\_deduction\_certificate = self.lower\_deduction\_certificate).
- Return values.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L3605) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L493)

<a id="op-89b99568d228ac"></a>
### Tax Withholding Entry.get balance values to update

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_get_balance_values_to_update`

**Inputs** self, old\_entry, proportion, field\_type.

**Explicit results** mapping(field → amount).

**Local steps**

- Set field\_to\_update from “withholding” when field\_type equals “taxable”, otherwise “taxable”.
  - Value choice on field\_type equals “taxable” — true gives “withholding”, false gives “taxable”.
- Set field from formatted text {field\_to\_update}\_amount.
- Set proportion from (1 − proportion).
- Set amount from flt((old\_entry.get(field) × proportion), self.precision(field)).
- Return mapping(field → amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L4119) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L491)

<a id="op-23849ee1ddcb76"></a>
### Tax Withholding Entry.clear old references

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_clear_old_references`

**Inputs** self.

**State and service calls** request set\_value on DOCTYPE.

**Explicit results** no value.

**Local steps**

- <a id="op-23849ee1ddcb76-guard-2"></a>If self.status does not belong to list(“Settled”, “Duplicate”).
  - Return no value.
- Set filters from mapping(“tax\_withholding\_category” → self.tax\_withholding\_category, “taxable\_doctype” → self.taxable\_doctype, “taxable\_name” → self.taxable\_name, “withholding\_doctype” → self.withholding\_doctype, …).
- If self.is\_taxable\_different.
  - Evaluate Platform.db.set\_value(DOCTYPE, filters, mapping(“withholding\_name” → empty text, “withholding\_doctype” → empty text, “withholding\_amount” → 0, “withholding\_date” → no value, …)).
- Otherwise.
  - If self.is\_withholding\_different.
    - If self.taxable\_amount &lt; 0.
      - Evaluate self.\_handle\_return\_invoice\_cancellation(filters).
    - Otherwise.
      - Evaluate Platform.db.set\_value(DOCTYPE, filters, mapping(“taxable\_name” → empty text, “taxable\_doctype” → empty text, “taxable\_date” → no value, “status” → “Over Withheld”)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status does not belong to list(“Settled”, “Duplicate”), self.status = “Under Withheld” selects the branch that returns no value. With self.status = “Settled”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-23849ee1ddcb76-guard-2)

**Methods declared on this owner** [handle return invoice cancellation](operations-113.md#op-cba8067a540301).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L4355) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L490)

<a id="op-cba8067a540301"></a>
### Tax Withholding Entry.handle return invoice cancellation

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_entry_handle_return_invoice_cancellation`

**Inputs** self, filters.

**Record and data access** read DOCTYPE via get\_all · resolve a document from DOCTYPE via get\_doc.

**State and service calls** request set\_value on DOCTYPE · request copy\_doc for Platform.get\_doc(DOCTYPE, expanded names entry) · call insert on new\_entry.

**Local steps**

- Set old\_entries from Platform.get\_all(DOCTYPE, filters = filters, fields = “\*”).
- Set docs\_needing\_reindex from set().
- For each entry in old\_entries.
  - Evaluate Platform.db.set\_value(DOCTYPE, entry.name, mapping(“taxable\_doctype” → entry.withholding\_doctype, “taxable\_name” → entry.withholding\_name, “taxable\_date” → entry.withholding\_date)).
  - <a id="op-cba8067a540301-guard-23"></a>If entry.withholding\_amount equals 0.
    - Continue with the next iteration or loop test.
  - Set new\_entry from Platform.copy\_doc(Platform.get\_doc(DOCTYPE, expanded names entry)).
  - Set values\_to\_update from mapping(“taxable\_amount” → abs(entry.taxable\_amount), “withholding\_amount” → 0, “status” → “Under Withheld”, “under\_withheld\_reason” → empty text, …).
  - Evaluate new\_entry.update(values\_to\_update).
  - Evaluate new\_entry.insert().
  - Evaluate docs\_needing\_reindex.add(tuple(entry.parenttype, entry.parent)).
- Evaluate \_reset\_idx(docs\_needing\_reindex).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison entry.withholding\_amount equals 0, entry.withholding\_amount = 0 selects the branch that continues with the next loop iteration. With entry.withholding\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cba8067a540301-guard-23)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L122) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L494)

<a id="op-7c00bcfccd48a8"></a>
### Tax Withholding Controller.initialize

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_initialize`

**Inputs** self, doc.

**Local steps**

- Set self.doc from doc.
- Set self.entries from list().
- Set self.precision from self.doc.precision(“withholding\_amount”, “tax\_withholding\_entries”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L5552) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L471)

<a id="op-9b28e3818d4f15"></a>
### Tax Withholding Controller.get category details

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_category_details`

**Inputs** self.

**Explicit results** TaxWithholdingDetails(category\_names, self.doc.tax\_withholding\_group, self.doc.posting\_date, self.party\_type, …).get().

**Local steps**

- Set category\_names from self.\_get\_category\_names().
- Return TaxWithholdingDetails(category\_names, self.doc.tax\_withholding\_group, self.doc.posting\_date, self.party\_type, …).get().

**Methods declared on this owner** [get category names](operations-113.md#op-e09b222672920a).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L5675) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L463)

<a id="op-e09b222672920a"></a>
### Tax Withholding Controller.get category names

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_category_names`

**Inputs** self.

**Explicit results** category\_names.

**Local steps**

- Set category\_names from set(generator of item.tax\_withholding\_category for item drawn from self.doc.items where (item.tax\_withholding\_category and item.apply\_tds)).
  - Draw item from self.doc.items, keep a combination only if ((item.tax\_withholding\_category and item.apply\_tds)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.tax\_withholding\_category → item.apply\_tds.
- Return category\_names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L5815) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L464)

<a id="op-053df607fcda69"></a>
### Tax Withholding Controller.calculate

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_calculate`

**Inputs** self.

**Local steps**

- Set self.category\_details from self.\_get\_category\_details().
- Evaluate self.\_update\_taxable\_amounts().
- If not self.doc.override\_tax\_withholding\_entries.
  - Evaluate self.\_generate\_withholding\_entries().
- Evaluate self.\_process\_withholding\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get category details](operations-113.md#op-9b28e3818d4f15), [update taxable amounts](operations-114.md#op-e2e35de2aba826), [generate withholding entries](operations-113.md#op-feb52a094f2413), [process withholding entries](operations-115.md#op-f8d6aed7e728ed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L5931) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L448)

<a id="op-feb52a094f2413"></a>
### Tax Withholding Controller.generate withholding entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_generate_withholding_entries`

**Inputs** self.

**Local steps**

- Set self.doc.tax\_withholding\_entries from list().
- Evaluate self.\_evaluate\_thresholds().
- For each category in self.category\_details.values().
  - Update self.entries using + self.\_create\_entries\_for\_category(category).
- Evaluate self.doc.extend(“tax\_withholding\_entries”, self.entries).

If control reaches the end, it returns no value.

**Methods declared on this owner** [evaluate thresholds](operations-114.md#op-a112b4e9cd2be7), [create entries for category](operations-113.md#op-9e02a00d961704).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L6074) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L462)

<a id="op-9e02a00d961704"></a>
### Tax Withholding Controller.create entries for category

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_create_entries_for_category`

**Inputs** self, category.

**Explicit results** entries.

**Local steps**

- Set entries from list().
- If not category.taxable\_amount.
  - Return entries.
- If not category.threshold\_crossed.
  - Evaluate entries.append(self.\_create\_under\_withheld\_entry(category)).
  - Set category.taxable\_amount from 0.
  - Return entries.
- If category.unused\_threshold.
  - Evaluate entries.append(self.\_create\_threshold\_exemption\_entry(category)).
  - <a id="op-9e02a00d961704-guard-16"></a>If category.taxable\_amount ≤ 0.
    - Return entries.
- Set open\_entries from self.\_get\_open\_entries\_for\_category(category).
- Set under\_entries from open\_entries at “under\_withheld”.
- Set over\_entries from open\_entries at “over\_withheld”.
- Evaluate entries.extend(self.\_adjust\_under\_over\_withheld(under\_entries, over\_entries, category)).
- If self.\_is\_return\_against\_invoice().
  - Evaluate entries.extend(self.\_process\_return\_ldc\_entries(under\_entries, category)).
- Otherwise.
  - If category.ldc\_unutilized\_amount.
    - Evaluate entries.extend(self.\_process\_ldc\_entries(under\_entries, over\_entries, category)).
- Evaluate entries.extend(self.\_merge\_entries(under\_entries, over\_entries, category)).
- Return entries.

**Derived branch illustrations**

- At the comparison category.taxable\_amount ≤ 0, category.taxable\_amount = 0 selects the branch that returns entries. With category.taxable\_amount = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-9e02a00d961704-guard-16)

**Methods declared on this owner** [create under withheld entry](operations-113.md#op-db9d0e099e3608), [create threshold exemption entry](operations-113.md#op-04a8921864d082), [get open entries for category](operations-113.md#op-110aeeec262c72), [adjust under over withheld](operations-114.md#op-69efb152f6ffb9), [is return against invoice](operations-113.md#op-7caf0ec25a2b80), [process return ldc entries](operations-113.md#op-04d4cbfa154de7), [process ldc entries](operations-113.md#op-ce30d8dfa7688d), [merge entries](operations-114.md#op-84c72bb7bb4b28).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L85) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L457)

<a id="op-db9d0e099e3608"></a>
### Tax Withholding Controller.create under withheld entry

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_create_under_withheld_entry`

**Inputs** self, category.

**Explicit results** mapping(expand self.\_create\_default\_entry(category), “taxable\_amount” → category.taxable\_amount, “withholding\_doctype” → empty text, “withholding\_name” → empty text, …).

**Local steps**

- Return mapping(expand self.\_create\_default\_entry(category), “taxable\_amount” → category.taxable\_amount, “withholding\_doctype” → empty text, “withholding\_name” → empty text, …).

**Methods declared on this owner** [create default entry](operations-114.md#op-753b555ec11a26).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L6735) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L460)

<a id="op-04a8921864d082"></a>
### Tax Withholding Controller.create threshold exemption entry

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_create_threshold_exemption_entry`

**Inputs** self, category.

**Explicit results** mapping(expand self.\_create\_default\_entry(category), “taxable\_amount” → taxable\_amount, “under\_withheld\_reason” → “Threshold Exemption”).

**Local steps**

- Set taxable\_amount from min(category.unused\_threshold, category.taxable\_amount).
- Update category.taxable\_amount using − taxable\_amount.
- Return mapping(expand self.\_create\_default\_entry(category), “taxable\_amount” → taxable\_amount, “under\_withheld\_reason” → “Threshold Exemption”).

**Methods declared on this owner** [create default entry](operations-114.md#op-753b555ec11a26).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L6893) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L459)

<a id="op-110aeeec262c72"></a>
### Tax Withholding Controller.get open entries for category

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_get_open_entries_for_category`

**Inputs** self, category.

**Explicit results** open\_entries.

**Local steps**

- Set entries from self.\_get\_historical\_entries(category).
- Set linked\_payments from self.\_get\_linked\_payments().
- Set open\_entries from mapping(“under\_withheld” → deque(), “over\_withheld” → deque()).
- Evaluate self.\_categorize\_historical\_entries(entries, linked\_payments, open\_entries).
- Set current\_entry from self.\_create\_default\_entry(category).
- Evaluate current\_entry.update(mapping(“taxable\_amount” → category.taxable\_amount, “withholding\_doctype” → empty text, “withholding\_name” → empty text, “withholding\_date” → empty text)).
- Evaluate open\_entries at “under\_withheld”.appendleft(current\_entry).
- Return open\_entries.

**Methods declared on this owner** [get historical entries](operations-114.md#op-e832668badeada), [get linked payments](operations-114.md#op-6a8e184a8a5e35), [categorize historical entries](operations-113.md#op-6819013ef030ec), [create default entry](operations-114.md#op-753b555ec11a26).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0205.json#L7053) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L469)

<a id="op-6819013ef030ec"></a>
### Tax Withholding Controller.categorize historical entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_categorize_historical_entries`

**Inputs** self, entries, linked\_payments, open\_entries.

**Local steps**

- For each entry in entries.
  - If entry.status equals “Under Withheld”.
    - Evaluate open\_entries at “under\_withheld”.append(entry).
    - Continue with the next iteration or loop test.
  - Set key from tuple(entry.withholding\_doctype, entry.withholding\_name).
  - If key belongs to linked\_payments.
    - Set total\_value from (entry.taxable\_amount − entry.withholding\_amount).
    - If not total\_value.
      - Continue with the next iteration or loop test.
    - Set proportion from (linked\_payments at key ÷ total\_value).
    - Set proportion from min(proportion, 1).
    - Update entry.withholding\_amount using × proportion.
    - Evaluate open\_entries at “over\_withheld”.appendleft(entry).
    - Continue with the next iteration or loop test.
  - If entry.withholding\_doctype belongs to list(“Payment Entry”, “Journal Entry”).
    - Continue with the next iteration or loop test.
  - Evaluate open\_entries at “over\_withheld”.append(entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L79) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L451)

<a id="op-ce30d8dfa7688d"></a>
### Tax Withholding Controller.process ldc entries

`operation_enterprise_accounts_record_definitions_tax_withholding_entry_business_behavior_tax_withholding_controller_process_ldc_entries`

**Inputs** self, under\_entries, over\_entries, category.

**Explicit results** self.\_merge\_entries(under\_entries, over\_entries, category, tax\_rate = category.ldc\_rate, constraint = category.ldc\_unutilized\_amount, default\_obj = ldc\_config).

**Local steps**

- Set ldc\_config from mapping(“under\_withheld\_reason” → “Lower Deduction Certificate”, “lower\_deduction\_certificate” → category.ldc\_certificate).
- Return self.\_merge\_entries(under\_entries, over\_entries, category, tax\_rate = category.ldc\_rate, constraint = category.ldc\_unutilized\_amount, default\_obj = ldc\_config).

**Methods declared on this owner** [merge entries](operations-114.md#op-84c72bb7bb4b28).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0206.json#L413) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L478)

<a id="op-7caf0ec25a2b80"></a>
### Tax Withholding Controller.is return against invoice

`operation_enterprise_binding_enterprise_accounts_doctype_tax_withholding_entry_tax_withholding_entry_taxwithholdingcontroller_is_return_against_invoice`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool((self.doc.get(“is\_return”) and self.doc.get(“return\_against”))).

**Local steps**

- Return bool((self.doc.get(“is\_return”) and self.doc.get(“return\_against”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doc.get(“is\_return”) → self.doc.get(“return\_against”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1088)

<a id="op-04d4cbfa154de7"></a>
### Tax Withholding Controller.process return ldc entries

`operation_enterprise_binding_enterprise_accounts_doctype_tax_withholding_entry_tax_withholding_entry_taxwithholdingcontroller_process_return_ldc_entries`

**Inputs** self, under\_entries, category.

**Declared result** list.

**Explicit results** list() · entries.

**Local steps**

- Set current\_entry from under\_entries at 0 when under\_entries, otherwise no value.
  - Value choice on under\_entries — true gives under\_entries at 0, false gives no value.
- If not (current\_entry and current\_entry.taxable\_name equals self.doc.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_entry → current\_entry.taxable\_name equals self.doc.name.
  - Return list().
- Set entries from list().
- For each ldc\_entry in self.\_get\_original\_ldc\_entries(category).
  - If flt(current\_entry.taxable\_amount, self.precision) ≥ 0.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate entries.extend(self.\_reverse\_ldc\_entry(current\_entry, ldc\_entry, category)).
- If not flt(current\_entry.taxable\_amount, self.precision).
  - Evaluate under\_entries.popleft().
- Return entries.

**Methods declared on this owner** [get original ldc entries](operations-114.md#op-c6358da7ebb3c7), [reverse ldc entry](operations-114.md#op-e34c502a2d5623).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1089)
