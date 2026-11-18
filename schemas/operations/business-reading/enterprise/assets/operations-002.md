# Asset management · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-8456efe8454254"></a>
### Asset.validate finance books

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_finance_books`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{}: Please use a different Finance Book.”.format(d.idx) · validation helper — translated “Row #{}: Finance Book should not be empty since you're using multiple.”.format(d.idx).

**Local steps**

- If (not self.calculate\_depreciation or len(self.finance\_books) equals 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.calculate\_depreciation → len(self.finance\_books) equals 1.
  - Return no value.
- Set finance\_books from set().
- For each d in self.finance\_books.
  - If d.finance\_book belongs to finance\_books.
    - Call the validation error handler Platform.throw(translated “Row #{}: Please use a different Finance Book.”.format(d.idx), title = translated “Duplicate Finance Book”).
  - Otherwise.
    - Evaluate finance\_books.add(d.finance\_book).
  - If not d.finance\_book.
    - Call the validation error handler Platform.throw(translated “Row #{}: Finance Book should not be empty since you're using multiple.”.format(d.idx), title = translated “Missing Finance Book”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1406) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L306)

<a id="op-8ec70d5c8220e7"></a>
### Asset.validate category

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_category`

**Inputs** self.

**Record and data access** read “Asset Category” via get\_value.

**Explicit failure paths** validation helper — translated “This asset category is marked as non-depreciable. Please disable depreciation calculation or choose a differ …”.

**Local steps**

- Set non\_depreciable\_category from Platform.db.get\_value(“Asset Category”, self.asset\_category, “non\_depreciable\_category”).
- If (self.calculate\_depreciation and non\_depreciable\_category).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.calculate\_depreciation → non\_depreciable\_category.
  - Call the validation error handler Platform.throw(translated “This asset category is marked as non-depreciable. Please disable depreciation calculation or choose a differ …”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L302)

<a id="op-ff3a7c9d3bd34b"></a>
### Asset.validate precision

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_precision`

**Inputs** self.

**Local steps**

- If self.net\_purchase\_amount.
  - Set self.net\_purchase\_amount from flt(self.net\_purchase\_amount, self.precision(“net\_purchase\_amount”)).
- If self.opening\_accumulated\_depreciation.
  - Set self.opening\_accumulated\_depreciation from flt(self.opening\_accumulated\_depreciation, self.precision(“opening\_accumulated\_depreciation”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L5141) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L313)

<a id="op-79c295291e3510"></a>
### Asset.validate asset values

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_asset_values`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value · read “Purchase Invoice” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Net Purchase Amount is mandatory” · validation helper — translated “Please create purchase receipt or purchase invoice for the item {0}”.format(self.item\_code) · validation helper — translated “Update stock must be enabled for the purchase invoice {0}”.format(self.purchase\_invoice) · validation helper — translated “Enter depreciation details” · validation helper — translated “Depreciation cannot be calculated for fully depreciated assets” · 1 additional forms in the steps below.

**Local steps**

- If not self.asset\_category.
  - Set self.asset\_category from Platform.get\_cached\_value(“Item”, self.item\_code, “asset\_category”).
- If (not flt(self.net\_purchase\_amount) and self.asset\_type differs from “Composite Asset”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(self.net\_purchase\_amount) → self.asset\_type differs from “Composite Asset”.
  - Call the validation error handler Platform.throw(translated “Net Purchase Amount is mandatory”, Platform.MandatoryError).
- If is\_cwip\_accounting\_enabled(self.asset\_category).
  - If (not self.asset\_type equals “Existing Asset” and not self.asset\_type equals “Composite Asset” and not self.purchase\_receipt and not self.purchase\_invoice).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.asset\_type equals “Existing Asset” → not self.asset\_type equals “Composite Asset” → not self.purchase\_receipt → not self.purchase\_invoice.
    - Call the validation error handler Platform.throw(translated “Please create purchase receipt or purchase invoice for the item {0}”.format(self.item\_code)).
  - If (not self.purchase\_receipt and self.purchase\_invoice and not Platform.db.get\_value(“Purchase Invoice”, self.purchase\_invoice, “update\_stock”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.purchase\_receipt → self.purchase\_invoice → not Platform.db.get\_value(“Purchase Invoice”, self.purchase\_invoice, “update\_stock”).
    - Call the validation error handler Platform.throw(translated “Update stock must be enabled for the purchase invoice {0}”.format(self.purchase\_invoice)).
- If not self.calculate\_depreciation.
  - Return no value.
- Otherwise.
  - If not self.finance\_books.
    - Call the validation error handler Platform.throw(translated “Enter depreciation details”).
  - If self.is\_fully\_depreciated.
    - Call the validation error handler Platform.throw(translated “Depreciation cannot be calculated for fully depreciated assets”).
- <a id="op-79c295291e3510-guard-40"></a>If self.asset\_type equals “Existing Asset”.
  - Return no value.
- If (self.available\_for\_use\_date and getdate(self.available\_for\_use\_date) &lt; getdate(self.purchase\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.available\_for\_use\_date → getdate(self.available\_for\_use\_date) &lt; getdate(self.purchase\_date).
  - Call the validation error handler Platform.throw(translated “Available-for-use Date should be after purchase date”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.asset\_type equals “Existing Asset”, self.asset\_type = “Existing Asset” selects the branch that returns no value. With self.asset\_type = “Composite Asset”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-79c295291e3510-guard-40)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “asset\_category”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L5314) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L300)

<a id="op-24e5031ae0907f"></a>
### Asset.validate opening accumulated depreciation

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_validate_opening_accumulated_depreciation`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Opening Accumulated Depreciation must be less than or equal to {0}”.format(self.net\_purchase\_amount).

**Local steps**

- If self.asset\_type differs from “Existing Asset”.
  - Set self.opening\_accumulated\_depreciation from 0.
  - Set self.opening\_number\_of\_booked\_depreciations from 0.
- Otherwise.
  - If (not self.calculate\_depreciation and flt(self.opening\_accumulated\_depreciation) &gt; flt(self.net\_purchase\_amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.calculate\_depreciation → flt(self.opening\_accumulated\_depreciation) &gt; flt(self.net\_purchase\_amount).
    - Call the validation error handler Platform.throw(translated “Opening Accumulated Depreciation must be less than or equal to {0}”.format(self.net\_purchase\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1303)

<a id="op-25a77bdf022ef6"></a>
### Asset.validate linked purchase documents

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_linked_purchase_documents`

**Inputs** self.

**Record and data access** read doctype via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} is in Draft. Submit it before creating the Asset.”.format(get\_link\_to\_form(doctype, purchase\_doc)).

**Local steps**

- If self.flags.is\_split\_asset.
  - Return no value.
- For each tuple(fieldname, doctype) in list(tuple(“purchase\_receipt”, “Purchase Receipt”), tuple(“purchase\_invoice”, “Purchase Invoice”)).
  - Set purchase\_doc from getattr(self, fieldname, no value).
  - If not purchase\_doc.
    - Continue with the next iteration or loop test.
  - If Platform.db.get\_value(doctype, purchase\_doc, “docstatus”) equals 0.
    - Call the validation error handler Platform.throw(translated “{0} is in Draft. Submit it before creating the Asset.”.format(get\_link\_to\_form(doctype, purchase\_doc))).
  - Evaluate self.validate\_asset\_qty\_with\_purchase\_doc(doctype, purchase\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset qty with purchase doc](operations-002.md#op-d34ba11551ee71).

**Values supplied outside this operation** selected callable from getattr(self, fieldname, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L6100) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1410) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L310)

<a id="op-d34ba11551ee71"></a>
### Asset.validate asset qty with purchase doc

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_asset_quantity_with_purchase_record`

**Inputs** self, doctype, purchase\_doc.

**Explicit failure paths** validation helper — translated text in the contract.format(self.asset\_quantity, purchased\_qty, doctype, get\_link\_to\_form(doctype, purchase\_doc), …).

**Local steps**

- Set Asset from Platform.qb.DocType(“Asset”).
- If doctype equals “Purchase Invoice”.
  - Set asset\_filter from Asset.purchase\_invoice equals purchase\_doc.
- Otherwise.
  - Set asset\_filter from Asset.purchase\_receipt equals purchase\_doc.
- Set existing\_asset\_qty from nested operand in the contract(nested operand in the contract).where(asset\_filter).run() at 0 at 0.
- Set PurchaseDoc from Platform.qb.DocType(doctype).
- Set PurchaseDocItems from Platform.qb.DocType(formatted text {doctype} Item).
- Set purchased\_qty from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.item\_code equals nested operand in the contract.item\_code).run() at 0 at 0.
- If (existing\_asset\_qty + self.asset\_quantity) &gt; purchased\_qty.
  - Call the validation error handler Platform.throw(translated text in the contract.format(self.asset\_quantity, purchased\_qty, doctype, get\_link\_to\_form(doctype, purchase\_doc), …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L299)

<a id="op-7041c6d9846734"></a>
### Asset.validate gross and purchase amount

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_gross_and_purchase_amount`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — error\_message.

**Local steps**

- <a id="op-7041c6d9846734-guard-2"></a>If self.asset\_type equals “Existing Asset”.
  - Return no value.
- If (self.net\_purchase\_amount and self.net\_purchase\_amount differs from self.purchase\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.net\_purchase\_amount → self.net\_purchase\_amount differs from self.purchase\_amount.
  - Set error\_message from translated “Net Purchase Amount should be &lt;b&gt;equal&lt;/b&gt; to purchase amount of one single Asset.”.
  - Update error\_message using + text in the contract.
  - Update error\_message using + translated “Please do not book expense of multiple assets against one single Asset.”.
  - Call the validation error handler Platform.throw(error\_message, title = translated “Invalid Net Purchase Amount”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.asset\_type equals “Existing Asset”, self.asset\_type = “Existing Asset” selects the branch that returns no value. With self.asset\_type = “Composite Asset”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7041c6d9846734-guard-2)

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L831) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L307)

<a id="op-3d37c28d31ffb3"></a>
### Asset.make asset movement

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_make_asset_movement`

**Inputs** self.

**Record and data access** read reference\_doctype via get\_value · resolve a document from mapping(“doctype” → “Asset Movement”, “assets” → assets, “purpose” → “Receipt”, “company” → self.company, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Asset Movement”, “assets” → assets, “purpose” → “Receipt”, “company” → self.company, …)) · call submit on asset\_movement.

**Local steps**

- Set reference\_doctype from “Purchase Receipt” when self.purchase\_receipt, otherwise “Purchase Invoice”.
  - Value choice on self.purchase\_receipt — true gives “Purchase Receipt”, false gives “Purchase Invoice”.
- Set reference\_docname from (self.purchase\_receipt or self.purchase\_invoice).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purchase\_receipt → self.purchase\_invoice.
- Set transaction\_date from getdate(self.purchase\_date).
- If reference\_docname.
  - Set tuple(posting\_date, posting\_time) from Platform.db.get\_value(reference\_doctype, reference\_docname, list(“posting\_date”, “posting\_time”)).
  - Set transaction\_date from get\_datetime(formatted text {posting\_date} {posting\_time}).
- Set assets from list(mapping(“asset” → self.name, “asset\_name” → self.asset\_name, “target\_location” → self.location, “to\_employee” → self.custodian, …)).
- Set asset\_movement from Platform.get\_doc(mapping(“doctype” → “Asset Movement”, “assets” → assets, “purpose” → “Receipt”, “company” → self.company, …)).insert().
- Evaluate asset\_movement.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L1051) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L283)

<a id="op-c6aa670b1e606c"></a>
### Asset.set depreciation rate

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_set_depreciation_rate`

**Inputs** self.

**State and service calls** call db\_set on d.

**Local steps**

- For each d in self.get(“finance\_books”).
  - Evaluate self.validate\_asset\_finance\_books(d).
  - Evaluate d.db\_set(“is\_rate\_of\_depreciation\_entered”, self.is\_entered\_depreciation\_rate(d), update\_modified = false).
  - Set d.rate\_of\_depreciation from self.get\_depreciation\_rate(d, on\_validate = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate asset finance books](operations-002.md#op-95929ccab357ed), [is entered depreciation rate](operations-003.md#op-70674f18cab470), [get depreciation rate](operations-003.md#op-ad4e22283a8ac3).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L289)

<a id="op-95929ccab357ed"></a>
### Asset.validate asset finance books

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_asset_finance_books`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row {0}: Expected Value After Useful Life cannot be negative”.format(row.idx) · validation helper — translated “Row {0}: Expected Value After Useful Life must be less than Net Purchase Amount”.format(row.idx).

**Local steps**

- Set row.expected\_value\_after\_useful\_life from flt(row.expected\_value\_after\_useful\_life, self.precision(“net\_purchase\_amount”)).
- If flt(row.expected\_value\_after\_useful\_life) &lt; 0.
  - Call the validation error handler Platform.throw(translated “Row {0}: Expected Value After Useful Life cannot be negative”.format(row.idx)).
- If flt(row.expected\_value\_after\_useful\_life) ≥ flt(self.net\_purchase\_amount).
  - Call the validation error handler Platform.throw(translated “Row {0}: Expected Value After Useful Life must be less than Net Purchase Amount”.format(row.idx)).
- If not row.depreciation\_start\_date.
  - Set row.depreciation\_start\_date from get\_last\_day(self.available\_for\_use\_date).
- Evaluate self.validate\_depreciation\_start\_date(row).
- Evaluate self.validate\_total\_number\_of\_depreciations\_and\_frequency(row).
- Evaluate self.validate\_written\_down\_value\_rate(row).
- If self.asset\_type differs from “Existing Asset”.
  - Set self.opening\_accumulated\_depreciation from 0.
  - Set self.opening\_number\_of\_booked\_depreciations from 0.
- Otherwise.
  - Evaluate self.validate\_opening\_depreciation\_values(row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate depreciation start date](operations-002.md#op-bd4c3913eedc33), [validate total number of depreciations and frequency](operations-002.md#op-797250c3c0e7b4), [validate written down value rate](operations-002.md#op-919e01957c3780), [validate opening depreciation values](operations-002.md#op-d889e0e7133630).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L298)

<a id="op-919e01957c3780"></a>
### Asset.validate written down value rate

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_validate_written_down_value_rate`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Set a Rate of Depreciation or an Expected Value After Useful Life for the Written Down Value method”.format(row.idx).

**Local steps**

- If (row.depreciation\_method equals “Written Down Value” and not flt(row.rate\_of\_depreciation) and not flt(row.expected\_value\_after\_useful\_life)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.depreciation\_method equals “Written Down Value” → not flt(row.rate\_of\_depreciation) → not flt(row.expected\_value\_after\_useful\_life).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Set a Rate of Depreciation or an Expected Value After Useful Life for the Written Down Value method”.format(row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1304)

<a id="op-d889e0e7133630"></a>
### Asset.validate opening depreciation values

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_opening_depreciation_values`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Opening Accumulated Depreciation must be less than or equal to {1}”.format(row.idx, depreciable\_amount) · validation helper — translated “Please set opening number of booked depreciations” · validation helper — translated “Row #{0}: Total Number of Depreciations cannot be less than or equal to Opening Number of Booked Depreciations”.format(row.idx).

**Local steps**

- Set row.expected\_value\_after\_useful\_life from flt(row.expected\_value\_after\_useful\_life, self.precision(“net\_purchase\_amount”)).
- Set depreciable\_amount from flt((flt(self.net\_purchase\_amount) − flt(row.expected\_value\_after\_useful\_life)), self.precision(“net\_purchase\_amount”)).
- If flt(self.opening\_accumulated\_depreciation) &gt; depreciable\_amount.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Opening Accumulated Depreciation must be less than or equal to {1}”.format(row.idx, depreciable\_amount)).
- If self.opening\_accumulated\_depreciation.
  - If not self.opening\_number\_of\_booked\_depreciations.
    - Call the validation error handler Platform.throw(translated “Please set opening number of booked depreciations”).
- Otherwise.
  - Set self.opening\_number\_of\_booked\_depreciations from 0.
- If flt(row.total\_number\_of\_depreciations) ≤ cint(self.opening\_number\_of\_booked\_depreciations).
  - Call the validation error handler Platform.throw(translated “Row #{0}: Total Number of Depreciations cannot be less than or equal to Opening Number of Booked Depreciations”.format(row.idx), title = translated “Invalid Schedule”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L2250) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L312)

<a id="op-797250c3c0e7b4"></a>
### Asset.validate total number of depreciations and frequency

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_total_number_of_depreciations_and_frequency`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Total Number of Depreciations must be greater than zero”.format(row.idx) · validation helper — translated “Row #{0}: Frequency of Depreciation must be greater than zero”.format(row.idx).

**Local steps**

- <a id="op-797250c3c0e7b4-guard-2"></a>If row.total\_number\_of\_depreciations ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Total Number of Depreciations must be greater than zero”.format(row.idx)).
- If row.frequency\_of\_depreciation ≤ 0.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Frequency of Depreciation must be greater than zero”.format(row.idx)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison row.total\_number\_of\_depreciations ≤ 0, row.total\_number\_of\_depreciations = 0 selects the branch that calls the validation-error handler with translated “Row #{0}: Total Number of Depreciations must be greater than zero”.format(row.idx). With row.total\_number\_of\_depreciations = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-797250c3c0e7b4-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L2759) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1414) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L314)

<a id="op-bd4c3913eedc33"></a>
### Asset.validate depreciation start date

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_depreciation_start_date`

**Inputs** self, row.

**Explicit failure paths** validation helper — translated “Row #{0}: Next Depreciation Date cannot be before Purchase Date”.format(row.idx) · validation helper — translated “Row #{0}: Next Depreciation Date cannot be before Available-for-use Date”.format(row.idx) · validation helper — translated “Row #{0}: Depreciation Start Date is required”.format(row.idx).

**Local steps**

- If row.depreciation\_start\_date.
  - If getdate(row.depreciation\_start\_date) &lt; getdate(self.purchase\_date).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Next Depreciation Date cannot be before Purchase Date”.format(row.idx)).
  - If getdate(row.depreciation\_start\_date) &lt; getdate(self.available\_for\_use\_date).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Next Depreciation Date cannot be before Available-for-use Date”.format(row.idx)).
- Otherwise.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Depreciation Start Date is required”.format(row.idx), title = translated “Invalid Schedule”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L2969) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L304)

<a id="op-f7508bfab7e1e2"></a>
### Asset.set total booked depreciations

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_set_total_booked_depreciations`

**Inputs** self.

**State and service calls** call db\_set on fb\_row.

**Local steps**

- For each fb\_row in self.get(“finance\_books”).
  - Set total\_number\_of\_booked\_depreciations from self.opening\_number\_of\_booked\_depreciations.
  - Set depr\_schedule from get\_depr\_schedule(self.name, “Active”, fb\_row.finance\_book).
  - If depr\_schedule.
    - For each je in depr\_schedule.
      - If je.journal\_entry.
        - Update total\_number\_of\_booked\_depreciations using + 1.
  - Evaluate fb\_row.db\_set(“total\_number\_of\_booked\_depreciations”, total\_number\_of\_booked\_depreciations).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L3337) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L293)

<a id="op-8819da2ef7c2ff"></a>
### Asset.validate expected value after useful life

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_expected_value_after_useful_life`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Depreciation Row {0}: Expected value after useful life must be greater than or equal to {1}”.format(row.idx, asset\_value\_after\_full\_schedule).

**Local steps**

- For each row in self.get(“finance\_books”).
  - Set depr\_schedule from get\_depr\_schedule(self.name, “Draft”, row.finance\_book).
  - If not depr\_schedule.
    - Continue with the next iteration or loop test.
  - Set accumulated\_depreciation\_after\_full\_schedule from max(list of d.accumulated\_depreciation\_amount for d drawn from depr\_schedule).
    - Draw d from depr\_schedule.
  - If accumulated\_depreciation\_after\_full\_schedule.
    - Set asset\_value\_after\_full\_schedule from flt((flt(self.net\_purchase\_amount) − flt(accumulated\_depreciation\_after\_full\_schedule)), self.precision(“net\_purchase\_amount”)).
    - If (row.expected\_value\_after\_useful\_life and row.expected\_value\_after\_useful\_life &lt; asset\_value\_after\_full\_schedule).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.expected\_value\_after\_useful\_life → row.expected\_value\_after\_useful\_life &lt; asset\_value\_after\_full\_schedule.
      - Call the validation error handler Platform.throw(translated “Depreciation Row {0}: Expected value after useful life must be greater than or equal to {1}”.format(row.idx, asset\_value\_after\_full\_schedule)).
    - Otherwise.
      - If not row.expected\_value\_after\_useful\_life.
        - Set row.expected\_value\_after\_useful\_life from asset\_value\_after\_full\_schedule.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L3550) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1405) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L305)

<a id="op-cecb9e383a66c5"></a>
### Asset.validate cancellation

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_cancellation`

**Inputs** self.

**Explicit failure paths** validation helper — translated “There are active maintenance or repairs against the asset. You must complete all of them before cancelling t …” · validation helper — translated “Asset cannot be cancelled, as it is already {0}”.format(self.status).

**Local steps**

- <a id="op-cecb9e383a66c5-guard-2"></a>If self.status belongs to tuple(“In Maintenance”, “Out of Order”).
  - Call the validation error handler Platform.throw(translated “There are active maintenance or repairs against the asset. You must complete all of them before cancelling t …”).
- <a id="op-cecb9e383a66c5-guard-8"></a>If self.status does not belong to tuple(“Submitted”, “Partially Depreciated”, “Fully Depreciated”).
  - Call the validation error handler Platform.throw(translated “Asset cannot be cancelled, as it is already {0}”.format(self.status)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status belongs to tuple(“In Maintenance”, “Out of Order”), self.status = “In Maintenance” selects the branch that calls the validation-error handler with translated “There are active maintenance or repairs against the asset. You must complete all of them before cancelling t …”. With self.status = “Draft”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cecb9e383a66c5-guard-2)
- At the comparison self.status does not belong to tuple(“Submitted”, “Partially Depreciated”, “Fully Depreciated”), self.status = “Draft” selects the branch that calls the validation-error handler with translated “Asset cannot be cancelled, as it is already {0}”.format(self.status). With self.status = “Submitted”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-cecb9e383a66c5-guard-8)

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L3962) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L301)

<a id="op-f6e5f90683f288"></a>
### Asset.cancel asset capitalizations

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_cancel_asset_capitalizations`

**Inputs** self.

**Record and data access** read “Asset Capitalization” via get\_all · resolve a document from “Asset Capitalization” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Asset Capitalization”, capitalization).

**Local steps**

- Set capitalizations from Platform.get\_all(“Asset Capitalization”, filters = mapping(“target\_asset” → self.name, “docstatus” → 1), pluck = “name”).
- For each capitalization in capitalizations.
  - If capitalization differs from self.flags.cancelled\_by\_asset\_capitalization.
    - Evaluate Platform.get\_doc(“Asset Capitalization”, capitalization).cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L228) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1293)

<a id="op-a0427e8d2e4ca6"></a>
### Asset.cancel movement entries

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_cancel_movement_entries`

**Inputs** self.

**Record and data access** execute query text (SELECT, Asset Movement) · resolve a document from “Asset Movement” via get\_doc.

**State and service calls** call cancel on movement.

**Local steps**

- Set movements from Platform.db.sql(query text (SELECT, Asset Movement), self.name, as\_dict = 1).
- For each movement in movements.
  - Set movement from Platform.get\_doc(“Asset Movement”, movement.get(“name”)).
  - Evaluate movement.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L265)

<a id="op-278dd374d9ecd7"></a>
### Asset.delete depreciation entries

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_delete_depreciation_entries`

**Inputs** self.

**Record and data access** resolve a document from “Journal Entry” via get\_doc.

**State and service calls** call cancel on Platform.get\_doc(“Journal Entry”, d.journal\_entry) · call cancel on Platform.get\_doc(“Journal Entry”, depr\_entry.name) · call db\_set on self.

**Local steps**

- If self.calculate\_depreciation.
  - For each row in self.get(“finance\_books”).
    - Set depr\_schedule from get\_depr\_schedule(self.name, “Active”, row.finance\_book).
    - For each d in (depr\_schedule or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in depr\_schedule → list().
      - If d.journal\_entry.
        - Evaluate Platform.get\_doc(“Journal Entry”, d.journal\_entry).cancel().
- Otherwise.
  - Set depr\_entries from self.get\_manual\_depreciation\_entries().
  - For each depr\_entry in (depr\_entries or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in depr\_entries → list().
    - Evaluate Platform.get\_doc(“Journal Entry”, depr\_entry.name).cancel().
  - Evaluate self.db\_set(“value\_after\_depreciation”, (flt(self.net\_purchase\_amount) − flt(self.opening\_accumulated\_depreciation))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get manual depreciation entries](operations-003.md#op-024135f69eb126).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0308.json#L4556) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L268)

<a id="op-af3901080c766c"></a>
### Asset.set status

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_set_status`

**Inputs** self, status = no value.

**State and service calls** call db\_set on self.

**Local steps**

- If not status.
  - Set status from self.get\_maintenance\_status(self.get\_status()).
- Evaluate self.db\_set(“status”, status).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get maintenance status](operations-002.md#op-e8e939aed4cf49), [get status](operations-003.md#op-8b4ecdfd133e1d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L292)

<a id="op-e8e939aed4cf49"></a>
### Asset.get maintenance status

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_get_maintenance_status`

**Inputs** self, status.

**Declared result** str.

**Explicit results** “Out of Order” · “In Maintenance” · status.

**Local steps**

- If self.has\_pending\_repair().
  - Return “Out of Order”.
- If (status differs from “Fully Depreciated” and self.has\_due\_maintenance()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in status differs from “Fully Depreciated” → self.has\_due\_maintenance().
  - Return “In Maintenance”.
- Return status.

**Methods declared on this owner** [has pending repair](operations-003.md#op-58582bbbc1b9dd), [has due maintenance](operations-002.md#op-aaba5c9bb8535d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L231) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L658) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1296)

<a id="op-aaba5c9bb8535d"></a>
### Asset.has due maintenance

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_has_due_maintenance`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · has\_due\_maintenance(self.name).

**Local steps**

- If (self.docstatus differs from 1 or self.disposal\_date or not self.maintenance\_required).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.docstatus differs from 1 → self.disposal\_date → not self.maintenance\_required.
  - Return false.
- Return has\_due\_maintenance(self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L232) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L659) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1297)
