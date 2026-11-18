# Asset management · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset

[Record definition](../../../../data/record-types/asset.json)

<a id="op-2c0873a0f347ac"></a>
### Asset.validate

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_category().
- Evaluate self.validate\_precision().
- Evaluate self.validate\_linked\_purchase\_documents().
- Evaluate self.set\_purchase\_doc\_row\_item().
- Evaluate self.validate\_asset\_values().
- Evaluate self.validate\_opening\_accumulated\_depreciation().
- Evaluate self.validate\_asset\_and\_reference().
- Evaluate self.validate\_item().
- Evaluate self.validate\_cost\_center().
- Evaluate self.set\_missing\_values().
- Evaluate self.validate\_gross\_and\_purchase\_amount().
- Evaluate self.validate\_finance\_books().
- If self.calculate\_depreciation.
  - Set self.is\_fully\_depreciated from 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate category](operations-002.md#op-8ec70d5c8220e7), [validate precision](operations-002.md#op-ff3a7c9d3bd34b), [validate linked purchase documents](operations-002.md#op-25a77bdf022ef6), [set purchase doc row item](operations-001.md#op-576bdc28d1dd9d), [validate asset values](operations-002.md#op-79c295291e3510), [validate opening accumulated depreciation](operations-002.md#op-24e5031ae0907f), [validate asset and reference](operations-001.md#op-72cb71d71492d8), [validate item](operations-001.md#op-0a950ac770c963), [validate cost center](operations-001.md#op-4a99a0af78fb90), [set missing values](operations-001.md#op-65c4606f195d3b), [validate gross and purchase amount](operations-002.md#op-7041c6d9846734), [validate finance books](operations-002.md#op-8456efe8454254).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L296)

<a id="op-1ef6618becdfcb"></a>
### Asset.before save

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_before_save`

**Inputs** self.

**Local steps**

- Set self.total\_asset\_cost from (self.net\_purchase\_amount + self.additional\_asset\_cost).
- Set self.status from self.get\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get status](operations-003.md#op-8b4ecdfd133e1d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L6352) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L263)

<a id="op-ce3a54f420e9a4"></a>
### Asset.create asset depreciation schedule

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_create_asset_depreciation_schedule`

**Inputs** self.

**State and service calls** request new\_doc for “Asset Depreciation Schedule” · call save on new\_schedule.

**Explicit results** no value.

**Local steps**

- Evaluate self.set\_depr\_rate\_and\_value\_after\_depreciation().
- If (self.split\_from or not self.calculate\_depreciation).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.split\_from → not self.calculate\_depreciation.
  - Return no value.
- Set created\_schedules from list().
- For each fb\_row in self.get(“finance\_books”).
  - If not fb\_row.rate\_of\_depreciation.
    - Set fb\_row.rate\_of\_depreciation from self.get\_depreciation\_rate(fb\_row, on\_validate = true).
  - Set existing\_schedule from get\_asset\_depr\_schedule\_doc(self.name, “Draft”, fb\_row.finance\_book).
  - If not existing\_schedule.
    - Set new\_schedule from Platform.new\_doc(“Asset Depreciation Schedule”).
    - Set new\_schedule.asset from self.name.
    - Evaluate new\_schedule.create\_depreciation\_schedule(fb\_row).
    - Evaluate new\_schedule.save().
    - Evaluate created\_schedules.append(new\_schedule.name).
    - Continue with the next iteration or loop test.
  - Evaluate self.evaluate\_and\_recreate\_depreciation\_schedule(existing\_schedule, fb\_row).
  - Evaluate created\_schedules.append(existing\_schedule.name).
- Evaluate self.show\_schedule\_creation\_message(created\_schedules).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set depr rate and value after depreciation](operations-001.md#op-5475983e0b4483), [get depreciation rate](operations-003.md#op-ad4e22283a8ac3), [evaluate and recreate depreciation schedule](operations-001.md#op-0627a39c2f8efd), [show schedule creation message](operations-001.md#op-ee30862c036d08).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L6446) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L267)

<a id="op-0627a39c2f8efd"></a>
### Asset.evaluate and recreate depreciation schedule

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_evaluate_and_recreate_depreciation_schedule`

**Inputs** self, existing\_doc, fb\_row.

**State and service calls** call save on existing\_doc.

**Local steps**

- Set asset\_details\_changed from self.has\_asset\_details\_changed(existing\_doc).
- Set depreciation\_settings\_changed from self.has\_depreciation\_settings\_changed(existing\_doc, fb\_row).
- If self.should\_regenerate\_depreciation\_schedule(existing\_doc, asset\_details\_changed, depreciation\_settings\_changed).
  - Evaluate existing\_doc.create\_depreciation\_schedule(fb\_row).
  - Evaluate existing\_doc.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has asset details changed](operations-001.md#op-fe52de3683fb11), [has depreciation settings changed](operations-001.md#op-5f17e17cf5c1ea), [should regenerate depreciation schedule](operations-001.md#op-525133e2a3f243).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L6920) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L269)

<a id="op-fe52de3683fb11"></a>
### Asset.has asset details changed

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_has_asset_details_changed`

**Inputs** self, existing\_doc.

**Explicit results** (self.net\_purchase\_amount differs from existing\_doc.net\_purchase\_amount or self.opening\_accumulated\_depreciation differs from existing\_doc.opening\_accumulated\_depreciation or self.opening\_number\_of\_booked\_ ….

**Local steps**

- Return (self.net\_purchase\_amount differs from existing\_doc.net\_purchase\_amount or self.opening\_accumulated\_depreciation differs from existing\_doc.opening\_accumulated\_depreciation or self.opening\_number\_of\_booked\_ ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.net\_purchase\_amount differs from existing\_doc.net\_purchase\_amount → self.opening\_accumulated\_depreciation differs from existing\_doc.opening\_accumulated\_depreciation → self.opening\_number\_of\_booked\_depreciations differs from existing\_doc.opening\_number\_of\_booked\_depreciations.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L281)

<a id="op-5f17e17cf5c1ea"></a>
### Asset.has depreciation settings changed

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_has_depreciation_settings_changed`

**Inputs** self, existing\_doc, fb\_row.

**Explicit results** true · (fb\_row.depreciation\_method differs from existing\_doc.depreciation\_method or fb\_row.total\_number\_of\_depreciations differs from existing\_doc.total\_number\_of\_depreciations or fb\_row.frequency\_of\_depreciation ….

**Local steps**

- If (not existing\_doc.get(“depreciation\_schedule”) or fb\_row.depreciation\_method differs from “Manual”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not existing\_doc.get(“depreciation\_schedule”) → fb\_row.depreciation\_method differs from “Manual”.
  - Return true.
- Return (fb\_row.depreciation\_method differs from existing\_doc.depreciation\_method or fb\_row.total\_number\_of\_depreciations differs from existing\_doc.total\_number\_of\_depreciations or fb\_row.frequency\_of\_depreciation ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fb\_row.depreciation\_method differs from existing\_doc.depreciation\_method → fb\_row.total\_number\_of\_depreciations differs from existing\_doc.total\_number\_of\_depreciations → fb\_row.frequency\_of\_depreciation differs from existing\_doc.frequency\_of\_depreciation → getdate(fb\_row.depreciation\_start\_date) differs from existing\_doc.get(“depreciation\_schedule”) at 0.schedule\_date → fb\_row.expected\_value\_after\_useful\_life differs from existing\_doc.expected\_value\_after\_useful\_life.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L282)

<a id="op-525133e2a3f243"></a>
### Asset.should regenerate depreciation schedule

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_should_regenerate_depreciation_schedule`

**Inputs** self, existing\_doc, asset\_details\_changed, depreciation\_settings\_changed.

**Explicit results** true · false.

**Local steps**

- If not existing\_doc.get(“depreciation\_schedule”).
  - Return true.
- If (asset\_details\_changed or depreciation\_settings\_changed).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in asset\_details\_changed → depreciation\_settings\_changed.
  - Return true.
- Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L408) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L294)

<a id="op-5475983e0b4483"></a>
### Asset.set depr rate and value after depreciation

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_set_depr_rate_and_value_after_depreciation`

**Inputs** self.

**State and service calls** call db\_set on self · call db\_set on d.

**Explicit results** no value.

**Local steps**

- If self.split\_from.
  - Return no value.
- Evaluate self.db\_set(“value\_after\_depreciation”, ((flt(self.net\_purchase\_amount) − flt(self.opening\_accumulated\_depreciation)) + flt(self.additional\_asset\_cost)), update\_modified = false).
- If self.calculate\_depreciation.
  - Evaluate self.set\_depreciation\_rate().
  - For each d in self.finance\_books.
    - Evaluate d.db\_set(“value\_after\_depreciation”, self.value\_after\_depreciation).
- Otherwise.
  - Set self.finance\_books from list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set depreciation rate](operations-002.md#op-c6aa670b1e606c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L288)

<a id="op-ee30862c036d08"></a>
### Asset.show schedule creation message

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_show_schedule_creation_message`

**Inputs** self, schedules.

**State and service calls** msgprint with translated “Asset Depreciation Schedules created/updated:&lt;br&gt;{0}&lt;br&gt;&lt;br&gt;Please check, edit if needed, and submit the Asset.”.format(asset\_depr\_schedules\_links).

**Local steps**

- If schedules.
  - Set asset\_depr\_schedules\_links from get\_comma\_separated\_links(schedules, “Asset Depreciation Schedule”).
  - Evaluate Platform.msgprint(translated “Asset Depreciation Schedules created/updated:&lt;br&gt;{0}&lt;br&gt;&lt;br&gt;Please check, edit if needed, and submit the Asset.”.format(asset\_depr\_schedules\_links)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L774) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L295)

<a id="op-9944825b166261"></a>
### Asset.on update

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.create\_asset\_depreciation\_schedule().
- Evaluate self.validate\_expected\_value\_after\_useful\_life().
- Evaluate self.set\_total\_booked\_depreciations().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create asset depreciation schedule](operations-001.md#op-ce3a54f420e9a4), [validate expected value after useful life](operations-002.md#op-8819da2ef7c2ff), [set total booked depreciations](operations-002.md#op-f7508bfab7e1e2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L914) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L287)

<a id="op-35361b77fb1411"></a>
### Asset.before submit

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_before_submit`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Please capitalize this asset before submitting.”.

**Local steps**

- If (self.asset\_type equals “Composite Asset” and not has\_active\_capitalization(self.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.asset\_type equals “Composite Asset” → not has\_active\_capitalization(self.name).
  - If (self.split\_from and has\_active\_capitalization(self.split\_from)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.split\_from → has\_active\_capitalization(self.split\_from).
    - Return no value.
  - Call the validation error handler Platform.throw(translated “Please capitalize this asset before submitting.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L1005) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L264)

<a id="op-6213c5ad7dcd3e"></a>
### Asset.on submit

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_in\_use\_date().
- Evaluate self.make\_asset\_movement().
- Evaluate self.reload().
- If (not self.booked\_fixed\_asset and self.asset\_type differs from “Composite Component” and self.validate\_make\_gl\_entry()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.booked\_fixed\_asset → self.asset\_type differs from “Composite Component” → self.validate\_make\_gl\_entry().
  - Evaluate self.make\_gl\_entries().
- If (self.calculate\_depreciation and not self.split\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.calculate\_depreciation → not self.split\_from.
  - Evaluate convert\_draft\_asset\_depr\_schedules\_into\_active(self).
- Evaluate self.set\_status().
- Evaluate add\_asset\_activity(self.name, translated “Asset submitted”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate in use date](operations-001.md#op-6ae61a06cfa3b2), [make asset movement](operations-002.md#op-3d37c28d31ffb3), [validate make gl entry](operations-003.md#op-1aff5971b9efa4), [make gl entries](operations-003.md#op-f81b7a4a38c48e), [set status](operations-002.md#op-af3901080c766c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L1182) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L286)

<a id="op-9e916b46080a40"></a>
### Asset.on cancel

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_on_cancel`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.validate\_cancellation().
- Evaluate self.cancel\_movement\_entries().
- Evaluate self.reload().
- Evaluate self.delete\_depreciation\_entries().
- Evaluate cancel\_asset\_depr\_schedules(self).
- Evaluate self.set\_status().
- Evaluate self.cancel\_asset\_capitalizations().
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”).
- If self.flags.cancelled\_by\_asset\_capitalization.
  - Update self.ignore\_linked\_doctypes using + tuple(“Asset Capitalization”).
- If self.asset\_type differs from “Composite Component”.
  - Evaluate make\_reverse\_gl\_entries(voucher\_type = “Asset”, voucher\_no = self.name).
  - Evaluate self.db\_set(“booked\_fixed\_asset”, 0).
- Evaluate add\_asset\_activity(self.name, translated “Asset cancelled”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate cancellation](operations-002.md#op-cecb9e383a66c5), [cancel movement entries](operations-002.md#op-a0427e8d2e4ca6), [delete depreciation entries](operations-002.md#op-278dd374d9ecd7), [set status](operations-002.md#op-af3901080c766c), [cancel asset capitalizations](operations-002.md#op-f6e5f90683f288).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L285)

<a id="op-d7856953afb16c"></a>
### Asset.after insert

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_after_insert`

**Inputs** self.

**Local steps**

- Evaluate add\_asset\_activity(self.name, translated “Asset created”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L262)

<a id="op-2f504bff8afc34"></a>
### Asset.on trash

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_on_trash`

**Inputs** self.

**Local steps**

- Evaluate super().on\_trash().
- Evaluate self.delete\_draft\_depreciation\_schedules().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete draft depreciation schedules](operations-001.md#op-cfcdbbee9dd1d7).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L236) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1301)

<a id="op-f5b3d98b930227"></a>
### Asset.after delete

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_after_delete`

**Inputs** self.

**State and service calls** request delete on “Asset Activity”.

**Local steps**

- Evaluate Platform.db.delete(“Asset Activity”, mapping(“asset” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L261)

<a id="op-cfcdbbee9dd1d7"></a>
### Asset.delete draft depreciation schedules

`operation_enterprise_binding_enterprise_assets_doctype_asset_asset_asset_delete_draft_depreciation_schedules`

**Inputs** self.

**Record and data access** read “Asset Depreciation Schedule” via get\_all.

**State and service calls** request delete\_doc for “Asset Depreciation Schedule”.

**Local steps**

- For each schedule in Platform.get\_all(“Asset Depreciation Schedule”, filters = mapping(“asset” → self.name, “docstatus” → 0), pluck = “name”).
  - Evaluate Platform.delete\_doc(“Asset Depreciation Schedule”, schedule).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L229) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L656) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1294)

<a id="op-576bdc28d1dd9d"></a>
### Asset.set purchase doc row item

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_set_purchase_record_row_item`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.asset\_type equals “Existing Asset” or self.asset\_type equals “Composite Asset”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.asset\_type equals “Existing Asset” → self.asset\_type equals “Composite Asset”.
  - Return no value.
- Set self.purchase\_amount from self.net\_purchase\_amount.
- Set purchase\_doc\_type from “Purchase Receipt” when self.purchase\_receipt, otherwise “Purchase Invoice”.
  - Value choice on self.purchase\_receipt — true gives “Purchase Receipt”, false gives “Purchase Invoice”.
- Set purchase\_doc from (self.purchase\_receipt or self.purchase\_invoice).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purchase\_receipt → self.purchase\_invoice.
- If not purchase\_doc.
  - Return no value.
- Evaluate self.set((Platform.scrub(purchase\_doc\_type) + “\_item”), self.get\_linked\_item(purchase\_doc\_type, purchase\_doc)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get linked item](operations-001.md#op-4ee38fd7abdc79).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L291)

<a id="op-4ee38fd7abdc79"></a>
### Asset.get linked item

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_get_linked_item`

**Inputs** self, purchase\_doc\_type, purchase\_doc.

**Record and data access** resolve a document from purchase\_doc\_type via get\_doc.

**Explicit results** item.name · matching\_items at 0.name.

**Local steps**

- Set purchase\_doc from Platform.get\_doc(purchase\_doc\_type, purchase\_doc).
- Set fieldname from (Platform.scrub(purchase\_doc\_type) + “\_item”).
- Set matching\_items from purchase\_doc.get(“items”, mapping(“item\_code” → self.item\_code)).
- For each item in matching\_items.
  - If (item.name equals self.get(fieldname) and (not self.is\_new() or self.flags.is\_split\_asset)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.name equals self.get(fieldname) → (not self.is\_new() or self.flags.is\_split\_asset).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_new() → self.flags.is\_split\_asset.
    - Return item.name.
- Set linked\_asset\_qty from get\_linked\_asset\_qty(fieldname, list of item.name for item drawn from matching\_items, self.name).
  - Draw item from matching\_items.
- Set matching\_items from list of item for item drawn from matching\_items where (flt(item.qty) − flt(linked\_asset\_qty.get(item.name))) ≥ self.asset\_quantity.
  - Draw item from matching\_items, keep a combination only if ((flt(item.qty) − flt(linked\_asset\_qty.get(item.name))) ≥ self.asset\_quantity).
- For each item in matching\_items.
  - If item.name equals self.get(fieldname).
    - Return item.name.
- Set precision from self.precision(“net\_purchase\_amount”).
- For each item in matching\_items.
  - For each rate in tuple(flt(item.base\_net\_rate), (flt(item.valuation\_rate) × flt((item.conversion\_factor or 1)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
    - If flt((rate × self.asset\_quantity), precision) equals flt(self.net\_purchase\_amount, precision).
      - Return item.name.
- If len(matching\_items) equals 1.
  - Return matching\_items at 0.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L275)

<a id="op-72cb71d71492d8"></a>
### Asset.validate asset and reference

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_asset_and_reference`

**Inputs** self.

**Record and data access** resolve a document from reference\_doc via get\_doc.

**Explicit failure paths** validation helper — translated “Company of asset {0} and purchase document {1} doesn't matches.”.format(self.name, reference\_doc.get(“name”)) · validation helper — translated “Purchase Invoice cannot be made against an existing asset {0}”.format(self.name).

**Local steps**

- If (self.purchase\_invoice or self.purchase\_receipt).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purchase\_invoice → self.purchase\_receipt.
  - Set reference\_doc from “Purchase Invoice” when self.purchase\_invoice, otherwise “Purchase Receipt”.
    - Value choice on self.purchase\_invoice — true gives “Purchase Invoice”, false gives “Purchase Receipt”.
  - Set reference\_name from (self.purchase\_invoice or self.purchase\_receipt).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.purchase\_invoice → self.purchase\_receipt.
  - Set reference\_doc from Platform.get\_doc(reference\_doc, reference\_name).
  - If reference\_doc.get(“company”) differs from self.company.
    - Call the validation error handler Platform.throw(translated “Company of asset {0} and purchase document {1} doesn't matches.”.format(self.name, reference\_doc.get(“name”))).
- If (self.asset\_type equals “Existing Asset” and self.purchase\_invoice).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.asset\_type equals “Existing Asset” → self.purchase\_invoice.
  - Call the validation error handler Platform.throw(translated “Purchase Invoice cannot be made against an existing asset {0}”.format(self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L297)

<a id="op-0a950ac770c963"></a>
### Asset.validate item

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_item`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Item {0} does not exist”.format(self.item\_code) · validation helper — translated “Item {0} has been disabled”.format(self.item\_code) · validation helper — translated “Item {0} must be a Fixed Asset Item”.format(self.item\_code) · validation helper — translated “Item {0} must be a non-stock item”.format(self.item\_code).

**Local steps**

- Set item from Platform.get\_cached\_value(“Item”, self.item\_code, list(“is\_fixed\_asset”, “is\_stock\_item”, “disabled”), as\_dict = 1).
- If not item.
  - Call the validation error handler Platform.throw(translated “Item {0} does not exist”.format(self.item\_code)).
- Otherwise.
  - If item.disabled.
    - Call the validation error handler Platform.throw(translated “Item {0} has been disabled”.format(self.item\_code)).
  - Otherwise.
    - If not item.is\_fixed\_asset.
      - Call the validation error handler Platform.throw(translated “Item {0} must be a Fixed Asset Item”.format(self.item\_code)).
    - Otherwise.
      - If item.is\_stock\_item.
        - Call the validation error handler Platform.throw(translated “Item {0} must be a non-stock item”.format(self.item\_code)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, list(“is\_fixed\_asset”, “is\_stock\_item”, “disabled”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L3070) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1409) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L309)

<a id="op-4a99a0af78fb90"></a>
### Asset.validate cost center

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_cost_center`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_value · read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Cost Center {} doesn't belong to Company {}”.format(Platform.bold(self.cost\_center), Platform.bold(self.company)) · validation helper — translated “Cost Center {} is a group cost center and group cost centers cannot be used in transactions”.format(Platform.bold(self.cost\_center)) · validation helper — translated “Please set a Cost Center for the Asset or set an Asset Depreciation Cost Center for the Company {}”.format(Platform.bold(self.company)).

**Local steps**

- If self.cost\_center.
  - Set tuple(cost\_center\_company, cost\_center\_is\_group) from Platform.db.get\_value(“Cost Center”, self.cost\_center, list(“company”, “is\_group”)).
  - If cost\_center\_company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Cost Center {} doesn't belong to Company {}”.format(Platform.bold(self.cost\_center), Platform.bold(self.company)), title = translated “Invalid Cost Center”).
  - If cost\_center\_is\_group.
    - Call the validation error handler Platform.throw(translated “Cost Center {} is a group cost center and group cost centers cannot be used in transactions”.format(Platform.bold(self.cost\_center)), title = translated “Invalid Cost Center”).
- Otherwise.
  - If not Platform.get\_cached\_value(“Company”, self.company, “depreciation\_cost\_center”).
    - Call the validation error handler Platform.throw(translated “Please set a Cost Center for the Asset or set an Asset Depreciation Cost Center for the Company {}”.format(Platform.bold(self.company)), title = translated “Missing Cost Center”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “depreciation\_cost\_center”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L35) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L303)

<a id="op-6ae61a06cfa3b2"></a>
### Asset.validate in use date

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_validate_in_use_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Available for use date is required” · validation helper — translated “Depreciation Row {0}: Depreciation Posting Date cannot be before Available-for-use Date”.format(d.idx).

**Local steps**

- If (not self.available\_for\_use\_date and self.asset\_type differs from “Composite Component”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.available\_for\_use\_date → self.asset\_type differs from “Composite Component”.
  - Call the validation error handler Platform.throw(translated “Available for use date is required”).
- For each d in self.finance\_books.
  - If getdate(d.depreciation\_start\_date) &lt; getdate(self.available\_for\_use\_date).
    - Call the validation error handler Platform.throw(translated “Depreciation Row {0}: Depreciation Posting Date cannot be before Available-for-use Date”.format(d.idx), title = translated “Incorrect Date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L4009) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1408) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L308)

<a id="op-65c4606f195d3b"></a>
### Asset.set missing values

`operation_enterprise_assets_record_definitions_asset_business_behavior_asset_set_missing_values`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Local steps**

- If not self.asset\_category.
  - Set self.asset\_category from Platform.get\_cached\_value(“Item”, self.item\_code, “asset\_category”).
- If (self.item\_code and not self.get(“finance\_books”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.item\_code → not self.get(“finance\_books”).
  - Set finance\_books from get\_item\_details(self.item\_code, self.asset\_category, self.net\_purchase\_amount).
  - Evaluate self.set(“finance\_books”, finance\_books).
- If (self.asset\_owner equals “Company” and not self.asset\_owner\_company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.asset\_owner equals “Company” → not self.asset\_owner\_company.
  - Set self.asset\_owner\_company from self.company.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, self.item\_code, “asset\_category”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0307.json#L4283) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L290)
