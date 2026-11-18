# Accounting and settlement · operations 84

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Pos register

<a id="op-6605f339e94254"></a>
### Get conditions

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_get_conditions`

**Inputs** filters, p.

**Explicit results** conditions.

**Local steps**

- Set conditions from list(p.company equals filters.get(“company”), p.posting\_date ≥ filters.get(“from\_date”), p.posting\_date ≤ filters.get(“to\_date”)).
- If filters.get(“pos\_profile”).
  - Evaluate conditions.append(p.pos\_profile equals filters.get(“pos\_profile”)).
- If filters.get(“owner”).
  - Evaluate conditions.append(p.owner equals filters.get(“owner”)).
- If filters.get(“customer”).
  - Evaluate conditions.append(p.customer equals filters.get(“customer”)).
- If filters.get(“is\_return”).
  - Evaluate conditions.append(p.is\_return equals filters.get(“is\_return”)).
- If filters.get(“mode\_of\_payment”).
  - Set sip from Platform.qb.DocType(“Sales Invoice Payment”).
  - Evaluate conditions.append(p.name.isin(nested operand in the contract(nested operand in the contract).select(sip.parent).where(IfNull(sip.mode\_of\_payment, empty text) equals filters.get(“mode\_of\_payment”)))).
- Return conditions.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0269.json#L876) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L812) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1154)

<a id="op-58fa552b6f244a"></a>
### Get group by field

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_get_group_by_field`

**Inputs** group\_by.

**Explicit results** group\_by\_field.

**Local steps**

- Set group\_by\_field from empty text.
- If group\_by equals “POS Profile”.
  - Set group\_by\_field from “pos\_profile”.
- Otherwise.
  - If group\_by equals “Cashier”.
    - Set group\_by\_field from “owner”.
  - Otherwise.
    - If group\_by equals “Customer”.
      - Set group\_by\_field from “customer”.
    - Otherwise.
      - If group\_by equals “Payment Method”.
        - Set group\_by\_field from “mode\_of\_payment”.
- Return group\_by\_field.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0269.json#L1631) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L813) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1155)

<a id="op-227ca70795db19"></a>
### Get columns

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** columns.

**Local steps**

- Set columns from list(mapping(“label” → translated “Posting Date”, “fieldname” → “posting\_date”, “fieldtype” → “Date”, “width” → 90), mapping(“label” → translated “Invoice Type”, “fieldname” → “invoice\_type”, “fieldtype” → ….
- Return columns.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1153)

## Record · Pos settings

<a id="op-c01792dc2d7a6a"></a>
### POSSettings.validate

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_point_of_sale_settings_validate`

**Inputs** self.

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save().
- If old\_doc.invoice\_type differs from self.invoice\_type.
  - Evaluate self.validate\_invoice\_type().
- Evaluate self.validate\_duplicate\_invoice\_fields().
- Evaluate self.validate\_invoice\_fields().
- Evaluate self.validate\_duplicate\_pos\_search\_fields().
- Evaluate self.validate\_pos\_search\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate invoice type](operations-084.md#op-a8099592744526), [validate duplicate invoice fields](operations-084.md#op-8c4211ef5e9649), [validate invoice fields](operations-084.md#op-213c1deb8e3196), [validate duplicate pos search fields](operations-084.md#op-a608a39513fb67), [validate pos search fields](operations-084.md#op-b255bcab3975b6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L1902) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L492) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L674)

<a id="op-a8099592744526"></a>
### POSSettings.validate invoice type

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_point_of_sale_settings_validate_invoice_type`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via count.

**Explicit failure paths** validation helper — translated “{0} cannot be changed with opened Opening Entries.”.format(Platform.bold(translated “Invoice Type”)).

**Local steps**

- Set pos\_opening\_entries\_count from Platform.db.count(“POS Opening Entry”, filters = mapping(“docstatus” → 1, “status” → “Open”)).
- If pos\_opening\_entries\_count.
  - Call the validation error handler Platform.throw(translated “{0} cannot be changed with opened Opening Entries.”.format(Platform.bold(translated “Invoice Type”)), title = translated “Invoice Document Type Selection Error”).
- If self.invoice\_type equals “Sales Invoice”.
  - Evaluate self.validate\_unconsolidated\_pos\_invoices().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate unconsolidated pos invoices](operations-084.md#op-9cb9953f28ca27).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L678)

<a id="op-9cb9953f28ca27"></a>
### POSSettings.validate unconsolidated pos invoices

`operation_enterprise_binding_enterprise_accounts_doctype_pos_settings_pos_settings_possettings_validate_unconsolidated_pos_invoices`

**Inputs** self.

**Record and data access** read “POS Invoice” via get\_all.

**Explicit failure paths** validation helper — translated “{0} cannot be changed to Sales Invoice while POS Invoices {1} are not consolidated. Consolidate them with a  …”.format(Platform.bold(translated “Invoice Type”), “, ”.join(map(Platform.bold, unc ….

**Local steps**

- Set unconsolidated\_pos\_invoices from Platform.get\_all(“POS Invoice”, filters = mapping(“docstatus” → 1, “consolidated\_invoice” → list(“is”, “not set”)), pluck = “name”, limit = 10).
- If unconsolidated\_pos\_invoices.
  - Call the validation error handler Platform.throw(translated “{0} cannot be changed to Sales Invoice while POS Invoices {1} are not consolidated. Consolidate them with a  …”.format(Platform.bold(translated “Invoice Type”), “, ”.join(map(Pla ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L171) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L269) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L907)

<a id="op-8c4211ef5e9649"></a>
### POSSettings.validate duplicate invoice fields

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_point_of_sale_settings_validate_duplicate_invoice_fields`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- Set invoice\_fields from list of field.fieldname for field drawn from self.invoice\_fields.
  - Draw field from self.invoice\_fields.
- Set duplicate\_invoice\_fields from set of key for tuple(key, value) drawn from Counter(invoice\_fields).items() where value &gt; 1.
  - Draw tuple(key, value) from Counter(invoice\_fields).items(), keep a combination only if (value &gt; 1).
- If len(duplicate\_invoice\_fields).
  - For each field in duplicate\_invoice\_fields.
    - Call the validation error handler Platform.throw(title = translated “Duplicate POS Fields”, msg = translated “'{0}' has been already added.”.format(field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L2321) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L493) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L675)

<a id="op-213c1deb8e3196"></a>
### POSSettings.validate invoice fields

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_point_of_sale_settings_validate_invoice_fields`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- If not self.invoice\_type.
  - Return no value.
- Set meta from Platform.get\_meta(self.invoice\_type).
- For each field in self.invoice\_fields.
  - Set df from meta.get\_field(field.fieldname).
  - If (not df or not is\_valid\_invoice\_field(df)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → not is\_valid\_invoice\_field(df).
    - Call the validation error handler Platform.throw(title = translated “Invalid POS Field”, msg = translated “Row #{0}: '{1}' is not a valid field of {2}.”.format(field.idx, Platform.bold((field.fieldname or empty text)), Platform.bold(transl ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.fieldname → empty text.
  - Set field.label from df.label.
  - Set field.fieldtype from df.fieldtype.
  - Set field.options from df.options.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L2593) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L677)

<a id="op-a608a39513fb67"></a>
### POSSettings.validate duplicate pos search fields

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_point_of_sale_settings_validate_duplicate_point_of_sale_search_fields`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- Set fieldnames from list of field.fieldname for field drawn from self.pos\_search\_fields.
  - Draw field from self.pos\_search\_fields.
- Set duplicate\_fieldnames from set of key for tuple(key, value) drawn from Counter(fieldnames).items() where value &gt; 1.
  - Draw tuple(key, value) from Counter(fieldnames).items(), keep a combination only if (value &gt; 1).
- For each fieldname in duplicate\_fieldnames.
  - Call the validation error handler Platform.throw(title = translated “Duplicate POS Search Fields”, msg = translated “'{0}' has been already added.”.format(fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L3003) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L676)

<a id="op-b255bcab3975b6"></a>
### POSSettings.validate pos search fields

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_point_of_sale_settings_validate_point_of_sale_search_fields`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- Set searchable\_fields from mapping of df.fieldname → df for df drawn from get\_searchable\_item\_fields().
  - Draw df from get\_searchable\_item\_fields().
- For each field in self.pos\_search\_fields.
  - Set df from searchable\_fields.get(field.fieldname).
  - If not df.
    - Call the validation error handler Platform.throw(title = translated “Invalid POS Search Field”, msg = translated “Row #{0}: '{1}' cannot be used to search items.”.format(field.idx, Platform.bold((field.fieldname or empty text)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.fieldname → empty text.
  - If field.field differs from get\_search\_field\_option(df).
    - Call the validation error handler Platform.throw(title = translated “Invalid POS Search Field”, msg = translated “Row #{0}: '{1}' does not match {2}.”.format(field.idx, Platform.bold((field.field or empty text)), Platform.bold(df.fieldname))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.field → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L3253) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L679)

<a id="op-b481a889314e42"></a>
### Is valid invoice field

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_is_valid_invoice_field`

**Inputs** df.

**Explicit results** (df.fieldtype does not belong to no\_value\_fields or df.fieldtype equals “Button”).

**Local steps**

- Return (df.fieldtype does not belong to no\_value\_fields or df.fieldtype equals “Button”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → df.fieldtype equals “Button”.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L3712) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L491) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L673)

<a id="op-aca017189f51c3"></a>
### Get searchable item fields

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_get_searchable_item_fields`

**Inputs** no declared parameters.

**Explicit results** list of df for df drawn from Platform.get\_meta(“Item”).fields where (df.fieldtype belongs to SEARCH\_FIELD\_TYPES and df.fieldname does not belong to DO\_NOT\_INCLUDE\_FIELDS).

**Local steps**

- Return list of df for df drawn from Platform.get\_meta(“Item”).fields where (df.fieldtype belongs to SEARCH\_FIELD\_TYPES and df.fieldname does not belong to DO\_NOT\_INCLUDE\_FIELDS).
  - Draw df from Platform.get\_meta(“Item”).fields, keep a combination only if ((df.fieldtype belongs to SEARCH\_FIELD\_TYPES and df.fieldname does not belong to DO\_NOT\_INCLUDE\_FIELDS)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype belongs to SEARCH\_FIELD\_TYPES → df.fieldname does not belong to DO\_NOT\_INCLUDE\_FIELDS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L3791) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L490) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L672)

<a id="op-cc12fc66173f2a"></a>
### Get search field option

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_get_search_field_option`

**Inputs** df.

**Explicit results** formatted text {df.label} ({df.fieldname}).

**Local steps**

- Return formatted text {df.label} ({df.fieldname}).

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L3911) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L489) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L671)

<a id="op-faa0bb27cdedea"></a>
### Get pos search field options

`operation_enterprise_accounts_record_definitions_point_of_sale_settings_business_behavior_get_point_of_sale_search_field_options`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list of mapping(“option” → get\_search\_field\_option(df), “fieldname” → df.fieldname) for df drawn from get\_searchable\_item\_fields().

**Local steps**

- Evaluate Platform.has\_permission(“POS Settings”, throw = true).
- Return list of mapping(“option” → get\_search\_field\_option(df), “fieldname” → df.fieldname) for df drawn from get\_searchable\_item\_fields().
  - Draw df from get\_searchable\_item\_fields().

**Values supplied outside this operation** effective access from Platform.has\_permission(“POS Settings”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0129.json#L3987) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L488) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L670)

## Record · Pricing rule

[Record definition](../../../../data/record-types/pricing_rule.json)

<a id="op-ceb085bf69f898"></a>
### Pricing Rule.validate

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_mandatory().
- Evaluate self.validate\_duplicate\_apply\_on().
- Evaluate self.validate\_applicable\_for\_selling\_or\_buying().
- Evaluate self.validate\_min\_max\_amt().
- Evaluate self.validate\_min\_max\_qty().
- Evaluate self.validate\_recursion().
- Evaluate self.cleanup\_fields\_value().
- Evaluate self.validate\_rate\_or\_discount().
- Evaluate self.validate\_max\_discount().
- Evaluate self.validate\_price\_list\_with\_currency().
- Evaluate self.validate\_dates().
- Evaluate self.validate\_condition().
- Evaluate self.validate\_mixed\_with\_recursion().
- If not self.margin\_type.
  - Set self.margin\_rate\_or\_amount from 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate mandatory](operations-084.md#op-7a11a671af2f75), [validate duplicate apply on](operations-084.md#op-a572d97fedc945), [validate applicable for selling or buying](operations-084.md#op-fdf08641059727), [validate min max amt](operations-084.md#op-d0ae384a5f36a4), [validate min max qty](operations-084.md#op-43fc803cdb72d9), [validate recursion](operations-084.md#op-8f097aabb1411c), [cleanup fields value](operations-084.md#op-52641e60c34400), [validate rate or discount](operations-084.md#op-fa012bb6ca9513), [validate max discount](operations-085.md#op-6077822a21705b), [validate price list with currency](operations-085.md#op-2ceaedaa5ae44c), [validate dates](operations-085.md#op-94fa55a50c6684), [validate condition](operations-085.md#op-6184d320c1e09c), [validate mixed with recursion](operations-085.md#op-c49f8f954b5a17).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L188) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L522) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L704)

<a id="op-a572d97fedc945"></a>
### Pricing Rule.validate duplicate apply on

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_duplicate_apply_on`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Duplicate {0} found in the table”.format(self.apply\_on).

**Local steps**

- If self.apply\_on differs from “Transaction”.
  - Set apply\_on\_table from apply\_on\_dict.get(self.apply\_on).
  - If not apply\_on\_table.
    - Return no value.
  - Set apply\_on\_field from Platform.scrub(self.apply\_on).
  - Set values from list of d.get(apply\_on\_field) for d drawn from self.get(apply\_on\_table) where d.get(apply\_on\_field).
    - Draw d from self.get(apply\_on\_table), keep a combination only if (d.get(apply\_on\_field)).
  - If len(values) differs from len(set(values)).
    - Call the validation error handler Platform.throw(translated “Duplicate {0} found in the table”.format(self.apply\_on)).
  - If self.apply\_on equals “Item Code”.
    - Evaluate self.validate\_template\_with\_variant(values).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate template with variant](operations-084.md#op-84d1ed9c417308).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L514) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L526) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L708)

<a id="op-84d1ed9c417308"></a>
### Pricing Rule.validate template with variant

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_template_with_variant`

**Inputs** self, item\_codes.

**Record and data access** read “Item” via get\_all.

**Explicit failure paths** validation helper — translated “Variant {0} and its template {1} cannot both be added to the same Pricing Rule”.format(Platform.bold(variant.name), Platform.bold(variant.variant\_of)).

**Local steps**

- Set variants from Platform.get\_all(“Item”, filters = mapping(“name” → tuple(“in”, item\_codes), “variant\_of” → tuple(“in”, item\_codes)), fields = list(“name”, “variant\_of”)).
- If variants.
  - Set variant from variants at 0.
  - Call the validation error handler Platform.throw(translated “Variant {0} and its template {1} cannot both be added to the same Pricing Rule”.format(Platform.bold(variant.name), Platform.bold(variant.variant\_of))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L910) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L717)

<a id="op-7a11a671af2f75"></a>
### Pricing Rule.validate mandatory

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_mandatory`

**Inputs** self.

**Explicit failure paths** validation helper — translated “For the 'Apply Rule On Other' condition the field {0} is mandatory”.format(Platform.bold(self.apply\_rule\_on\_other)).

**Local steps**

- If (self.has\_priority and not self.priority).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_priority → not self.priority.
  - Evaluate throw(translated “Priority is mandatory”, Platform.MandatoryError, translated “Please Set Priority”).
- If (self.priority and not self.has\_priority).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.priority → not self.has\_priority.
  - Set self.has\_priority from 1.
- For each tuple(apply\_on, field) in apply\_on\_dict.items().
  - If (self.apply\_on equals apply\_on and len((self.get(field) or list())) &lt; 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.apply\_on equals apply\_on → len((self.get(field) or list())) &lt; 1.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(field) → list().
    - Evaluate throw(translated “{0} is not added in the table”.format(apply\_on), Platform.MandatoryError).
- Set tocheck from Platform.scrub(self.get(“applicable\_for”, empty text)).
- If (tocheck and not self.get(tocheck)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tocheck → not self.get(tocheck).
  - Evaluate throw(translated “{0} is required”.format(translated self.meta.get\_label(tocheck)), Platform.MandatoryError).
- If self.apply\_rule\_on\_other.
  - Set o\_field from (“other\_” + Platform.scrub(self.apply\_rule\_on\_other)).
  - If (not self.get(o\_field) and o\_field belongs to other\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(o\_field) → o\_field belongs to other\_fields.
    - Call the validation error handler Platform.throw(translated “For the 'Apply Rule On Other' condition the field {0} is mandatory”.format(Platform.bold(self.apply\_rule\_on\_other))).
- If (self.price\_or\_product\_discount equals “Price” and not self.rate\_or\_discount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.price\_or\_product\_discount equals “Price” → not self.rate\_or\_discount.
  - Evaluate throw(translated “Rate or Discount is required for the price discount.”, Platform.MandatoryError).
- If self.apply\_discount\_on\_rate.
  - If not self.priority.
    - Evaluate throw(translated “As the field {0} is enabled, the field {1} is mandatory.”.format(Platform.bold(translated “Apply Discount on Discounted Rate”), Platform.bold(translated “Priority”))).
  - If (self.priority and cint(self.priority) equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.priority → cint(self.priority) equals 1.
    - Evaluate throw(translated “As the field {0} is enabled, the value of the field {1} should be more than 1.”.format(Platform.bold(translated “Apply Discount on Discounted Rate”), Platform.bold(translated “Priority”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L527) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L709)

<a id="op-fdf08641059727"></a>
### Pricing Rule.validate applicable for selling or buying

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_applicable_for_selling_or_buying`

**Inputs** self.

**Local steps**

- If (not self.selling and not self.buying).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.selling → not self.buying.
  - Evaluate throw(translated “At least one of the Selling or Buying must be selected”).
- If (not self.selling and self.applicable\_for belongs to list(“Customer”, “Customer Group”, “Territory”, “Sales Partner”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.selling → self.applicable\_for belongs to list(“Customer”, “Customer Group”, “Territory”, “Sales Partner”, …).
  - Evaluate throw(translated “Selling must be checked, if Applicable For is selected as {0}”.format(self.applicable\_for)).
- If (not self.buying and self.applicable\_for belongs to list(“Supplier”, “Supplier Group”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.buying → self.applicable\_for belongs to list(“Supplier”, “Supplier Group”).
  - Evaluate throw(translated “Buying must be checked, if Applicable For is selected as {0}”.format(self.applicable\_for)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L2305) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L523) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L705)

<a id="op-43fc803cdb72d9"></a>
### Pricing Rule.validate min max qty

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_minimum_maximum_quantity`

**Inputs** self.

**Local steps**

- If (self.min\_qty and self.max\_qty and flt(self.min\_qty) &gt; flt(self.max\_qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.min\_qty → self.max\_qty → flt(self.min\_qty) &gt; flt(self.max\_qty).
  - Evaluate throw(translated “Min Qty can not be greater than Max Qty”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L2666) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L530) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L712)

<a id="op-d0ae384a5f36a4"></a>
### Pricing Rule.validate min max amt

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_minimum_maximum_amount`

**Inputs** self.

**Local steps**

- If (self.min\_amt and self.max\_amt and flt(self.min\_amt) &gt; flt(self.max\_amt)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.min\_amt → self.max\_amt → flt(self.min\_amt) &gt; flt(self.max\_amt).
  - Evaluate throw(translated “Min Amt can not be greater than Max Amt”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L2808) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L529) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L711)

<a id="op-8f097aabb1411c"></a>
### Pricing Rule.validate recursion

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_recursion`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- <a id="op-8f097aabb1411c-guard-2"></a>If self.price\_or\_product\_discount differs from “Product”.
  - Return no value.
- If (self.free\_item or self.same\_item).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.free\_item → self.same\_item.
  - If flt(self.recurse\_for) ≤ 0.
    - Set self.recurse\_for from 1.
- If self.is\_recursive.
  - If self.apply\_on equals “Transaction”.
    - Evaluate throw(translated “{0} is not supported when {1} is {2}”.format(Platform.bold(translated “Is Recursive”), Platform.bold(translated “Apply On”), Platform.bold(translated “Transaction”))).
  - If flt(self.apply\_recursion\_over) &gt; flt(self.min\_qty).
    - Evaluate throw(translated “Min Qty should be greater than Recurse Over Qty”).
  - If flt(self.apply\_recursion\_over) &lt; 0.
    - Evaluate throw(translated “Recurse Over Qty cannot be less than 0”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.price\_or\_product\_discount differs from “Product”, self.price\_or\_product\_discount = “Price” selects the branch that returns no value. With self.price\_or\_product\_discount = “Product”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-8f097aabb1411c-guard-2)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L716)

<a id="op-52641e60c34400"></a>
### Pricing Rule.cleanup fields value

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_cleanup_fields_value`

**Inputs** self.

**Local steps**

- For each logic\_field in list(“apply\_on”, “applicable\_for”, “rate\_or\_discount”).
  - Set fieldname from Platform.scrub((self.get(logic\_field) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(logic\_field) → empty text.
  - Set options from (self.meta.get\_options(logic\_field) or empty text).split(whitespace '\\n').
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.meta.get\_options(logic\_field) → empty text.
  - For each f in options.
    - If not f.
      - Continue with the next iteration or loop test.
    - Set scrubbed\_f from Platform.scrub(f).
    - If logic\_field equals “apply\_on”.
      - Set apply\_on\_f from apply\_on\_dict.get(f, f).
    - Otherwise.
      - Set apply\_on\_f from scrubbed\_f.
    - If scrubbed\_f differs from fieldname.
      - Evaluate self.set(apply\_on\_f, no value).
- If (self.mixed\_conditions and self.get(“same\_item”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.mixed\_conditions → self.get(“same\_item”).
  - Set self.same\_item from 0.
- Set apply\_rule\_on\_other from Platform.scrub((self.apply\_rule\_on\_other or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.apply\_rule\_on\_other → empty text.
- Set cleanup\_other\_fields from other\_fields when not apply\_rule\_on\_other, otherwise list of o\_field for o\_field drawn from other\_fields where o\_field differs from (“other\_” + apply\_rule\_on\_other).
  - Value choice on not apply\_rule\_on\_other — true gives other\_fields, false gives list of o\_field for o\_field drawn from other\_fields where o\_field differs from (“other\_” + apply\_rule\_on\_other).
  - Draw o\_field from other\_fields, keep a combination only if (o\_field differs from (“other\_” + apply\_rule\_on\_other)).
- For each other\_field in cleanup\_other\_fields.
  - Evaluate self.set(other\_field, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L3268) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L521) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L703)

<a id="op-fa012bb6ca9513"></a>
### Pricing Rule.validate rate or discount

`operation_enterprise_accounts_record_definitions_pricing_rule_business_behavior_pricing_rule_validate_rate_or_discount`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Free item code is not selected”.

**Local steps**

- For each field in list(“Rate”).
  - If flt(self.get(Platform.scrub(field))) &lt; 0.
    - Evaluate throw(translated “{0} can not be negative”.format(field)).
- If (self.price\_or\_product\_discount equals “Product” and not self.free\_item).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.price\_or\_product\_discount equals “Product” → not self.free\_item.
  - If self.mixed\_conditions.
    - Call the validation error handler Platform.throw(translated “Free item code is not selected”).
  - Otherwise.
    - Set self.same\_item from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0130.json#L3859) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L533) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L715)
