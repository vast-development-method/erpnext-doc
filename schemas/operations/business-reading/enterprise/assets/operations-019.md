# Asset management · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Asset value adjustment

[Record definition](../../../../data/record-types/asset_value_adjustment.json)

<a id="op-7ec019a68ef5bb"></a>
### Asset Value Adjustment.update asset

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_update_asset`

**Inputs** self.

**Local steps**

- Set asset from self.update\_asset\_value\_after\_depreciation().
- Set note from self.get\_adjustment\_note().
- Evaluate reschedule\_depreciation(asset, note).
- Evaluate asset.set\_status().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update asset value after depreciation](operations-019.md#op-4492e02b2b7361), [get adjustment note](operations-019.md#op-b1ccaadcb521fc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0332.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L48) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L701)

<a id="op-4492e02b2b7361"></a>
### Asset Value Adjustment.update asset value after depreciation

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_update_asset_value_after_depreciation`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_update on row · call db\_update on asset.

**Explicit results** asset.

**Local steps**

- Set difference\_amount from self.difference\_amount when self.docstatus equals 1, otherwise (negative 1 × self.difference\_amount).
  - Value choice on self.docstatus equals 1 — true gives self.difference\_amount, false gives (negative 1 × self.difference\_amount).
- Set asset from Platform.get\_doc(“Asset”, self.asset).
- If asset.calculate\_depreciation.
  - For each row in asset.finance\_books.
    - If cstr(row.finance\_book) equals cstr(self.finance\_book).
      - Set salvage\_value\_adjustment from self.get\_adjusted\_salvage\_value\_amount(row, difference\_amount).
      - Update row.expected\_value\_after\_useful\_life using + salvage\_value\_adjustment.
      - Set row.value\_after\_depreciation from (row.value\_after\_depreciation + flt(difference\_amount)).
      - Set row.value\_adjustment\_amount from (flt(row.value\_adjustment\_amount) + flt(difference\_amount)).
      - Evaluate row.db\_update().
- Otherwise.
  - Set asset.value\_adjustment\_amount from (flt(asset.value\_adjustment\_amount) + flt(difference\_amount)).
- Update asset.value\_after\_depreciation using + flt(difference\_amount).
- Evaluate asset.db\_update().
- Return asset.

**Methods declared on this owner** [get adjusted salvage value amount](operations-019.md#op-007a368a616e20).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L140) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L49) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L702)

<a id="op-007a368a616e20"></a>
### Asset Value Adjustment.get adjusted salvage value amount

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_get_adjusted_salvage_value_amount`

**Inputs** self, row, difference\_amount.

**Explicit results** flt(((difference\_amount × row.salvage\_value\_percentage) ÷ 100)).

**Local steps**

- Return flt(((difference\_amount × row.salvage\_value\_percentage) ÷ 100)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L38) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L691)

<a id="op-b1ccaadcb521fc"></a>
### Asset Value Adjustment.get adjustment note

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_asset_value_adjustment_get_adjustment_note`

**Inputs** self.

**Explicit results** notes.

**Local steps**

- If self.docstatus equals 1.
  - Set notes from translated “This schedule was created when Asset {0} was adjusted through Asset Value Adjustment {1}.”.format(get\_link\_to\_form(“Asset”, self.asset), get\_link\_to\_form(self.get(“doctype”), self.get(“name”))).
- Otherwise.
  - If self.docstatus equals 2.
    - Set notes from translated “This schedule was created when Asset {0}'s Asset Value Adjustment {1} was cancelled.”.format(get\_link\_to\_form(“Asset”, self.asset), get\_link\_to\_form(self.get(“doctype”), self.get(“name”))).
- Return notes.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0332.json#L679) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L39) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L692)

<a id="op-ae0c71d7247d65"></a>
### Get value of accounting dimensions

`operation_enterprise_assets_record_definitions_asset_value_adjustment_business_behavior_get_value_of_accounting_dimensions`

**Inputs** asset\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Accounting Dimension” via get\_list · read “Asset” via get\_value.

**Explicit results** Platform.db.get\_value(“Asset”, asset\_name, fieldname = dimension\_fields, as\_dict = true).

**Local steps**

- Set dimension\_fields from list(expanded Platform.get\_list(“Accounting Dimension”, pluck = “fieldname”), “cost\_center”).
- Return Platform.db.get\_value(“Asset”, asset\_name, fieldname = dimension\_fields, as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L52) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L705)

## Report · Fixed asset register

<a id="op-a280c9080d9c6f"></a>
### Execute

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data, no value, chart).

**Local steps**

- Set filters from Platform.\_dict((filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Set chart from prepare\_chart\_data(data, filters) when filters.get(“group\_by”) does not belong to tuple(“Asset Category”, “Location”), otherwise mapping().
  - Value choice on filters.get(“group\_by”) does not belong to tuple(“Asset Category”, “Location”) — true gives prepare\_chart\_data(data, filters), false gives mapping().
- Return tuple(columns, data, no value, chart).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L3740) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L728)

<a id="op-d39182cdc6deed"></a>
### Get data

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_data`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value · read “Asset” via get\_list.

**Explicit results** data.

**Local steps**

- Set data from list().
- Set conditions from get\_conditions(filters).
- Set pr\_supplier\_map from get\_purchase\_receipt\_supplier\_map().
- Set pi\_supplier\_map from get\_purchase\_invoice\_supplier\_map().
- Set assets\_linked\_to\_fb from get\_assets\_linked\_to\_fb(filters).
- Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
- If (filters.include\_default\_book\_assets and company\_fb).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.include\_default\_book\_assets → company\_fb.
  - Set finance\_book from company\_fb.
- Otherwise.
  - If filters.finance\_book.
    - Set finance\_book from filters.finance\_book.
  - Otherwise.
    - Set finance\_book from no value.
- Set depreciation\_amount\_map from get\_asset\_depreciation\_amount\_map(filters, finance\_book).
- Set revaluation\_amount\_map from get\_asset\_value\_adjustment\_map(filters, finance\_book).
- If not finance\_book.
  - Evaluate value\_assets\_on\_first\_finance\_book(filters, assets\_linked\_to\_fb, depreciation\_amount\_map, revaluation\_amount\_map).
- Set group\_by from Platform.scrub(filters.get(“group\_by”)).
- Set end\_date from get\_report\_end\_date(filters).
- If group\_by belongs to tuple(“asset\_category”, “location”).
  - Set data from get\_group\_by\_data(group\_by, conditions, assets\_linked\_to\_fb, depreciation\_amount\_map, …).
  - Return data.
- Set fields from list(“name as asset\_id”, “asset\_name”, “status”, “department”, …).
- Set assets\_record from Platform.get\_list(“Asset”, filters = conditions, fields = fields).
- For each asset in assets\_record.
  - If (asset.calculate\_depreciation and asset.asset\_id does not belong to assets\_linked\_to\_fb).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset.calculate\_depreciation → asset.asset\_id does not belong to assets\_linked\_to\_fb.
    - Continue with the next iteration or loop test.
  - Set depreciation\_amount from (depreciation\_amount\_map.get(asset.asset\_id) or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in depreciation\_amount\_map.get(asset.asset\_id) → 0.0.
  - Set revaluation\_amount from revaluation\_amount\_map.get(asset.asset\_id, 0.0).
  - Set asset\_value from get\_asset\_value(asset, depreciation\_amount, revaluation\_amount, end\_date).
  - Set row from mapping(“asset\_id” → asset.asset\_id, “asset\_name” → asset.asset\_name, “status” → asset.status, “department” → asset.department, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pr\_supplier\_map.get(asset.purchase\_receipt) → pi\_supplier\_map.get(asset.purchase\_invoice).
  - Evaluate data.append(row).
- Return data.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L734)

<a id="op-5cd700663a5d0f"></a>
### Get asset value

`operation_enterprise_binding_enterprise_assets_report_fixed_asset_register_fixed_asset_register_get_asset_value`

**Inputs** asset, depreciation\_amount, revaluation\_amount, end\_date = no value.

**Declared result** float.

**Explicit results** 0.0 · (((asset.net\_purchase\_amount − asset.opening\_accumulated\_depreciation) − depreciation\_amount) + revaluation\_amount).

**Local steps**

- If is\_disposed\_by(asset, end\_date).
  - Return 0.0.
- Return (((asset.net\_purchase\_amount − asset.opening\_accumulated\_depreciation) − depreciation\_amount) + revaluation\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L22)

<a id="op-8428ed6e47eed1"></a>
### Is disposed by

`operation_enterprise_binding_enterprise_assets_report_fixed_asset_register_fixed_asset_register_is_disposed_by`

**Inputs** asset, end\_date.

**Declared result** bool.

**Explicit results** false · (not (end\_date and asset.disposal\_date) or getdate(asset.disposal\_date) ≤ getdate(end\_date)).

**Local steps**

- If asset.status does not belong to tuple(“Sold”, “Scrapped”, “Capitalized”).
  - Return false.
- Return (not (end\_date and asset.disposal\_date) or getdate(asset.disposal\_date) ≤ getdate(end\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (end\_date and asset.disposal\_date) → getdate(asset.disposal\_date) ≤ getdate(end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in end\_date → asset.disposal\_date.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L25)

<a id="op-b6fcd8435cc8f8"></a>
### Get report end date

`operation_enterprise_binding_enterprise_assets_report_fixed_asset_register_fixed_asset_register_get_report_end_date`

**Inputs** filters.

**Explicit results** filters.to\_date · filters.year\_end\_date.

**Local steps**

- If filters.filter\_based\_on equals “Date Range”.
  - Return filters.to\_date.
- If filters.filter\_based\_on equals “Fiscal Year”.
  - Return filters.year\_end\_date.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L24)

<a id="op-0f3a38c113bcbf"></a>
### Get conditions

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_conditions`

**Inputs** filters.

**Explicit results** conditions.

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set conditions from mapping(“docstatus” → 1).
- Set status from filters.status.
- Set date\_field from Platform.scrub((filters.date\_based\_on or “Purchase Date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.date\_based\_on → “Purchase Date”.
- If filters.get(“company”).
  - Set conditions at “company” from filters.company.
- If filters.filter\_based\_on equals “Date Range”.
  - If (not filters.from\_date and not filters.to\_date).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.from\_date → not filters.to\_date.
    - Set filters.from\_date from add\_months(nowdate(), negative 12).
    - Set filters.to\_date from nowdate().
  - Set conditions at date\_field from list(“between”, list(filters.from\_date, filters.to\_date)).
- Otherwise.
  - If filters.filter\_based\_on equals “Fiscal Year”.
    - If (not filters.from\_fiscal\_year and not filters.to\_fiscal\_year).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filters.from\_fiscal\_year → not filters.to\_fiscal\_year.
      - Set default\_fiscal\_year from get\_fiscal\_year(today()) at 0.
      - Set filters.from\_fiscal\_year from default\_fiscal\_year.
      - Set filters.to\_fiscal\_year from default\_fiscal\_year.
    - Set fiscal\_year from get\_fiscal\_year\_data(filters.from\_fiscal\_year, filters.to\_fiscal\_year).
    - Evaluate validate\_fiscal\_year(fiscal\_year, filters.from\_fiscal\_year, filters.to\_fiscal\_year).
    - Set filters.year\_start\_date from getdate(fiscal\_year.year\_start\_date).
    - Set filters.year\_end\_date from getdate(fiscal\_year.year\_end\_date).
    - Set conditions at date\_field from list(“between”, list(filters.year\_start\_date, filters.year\_end\_date)).
- If filters.get(“only\_existing\_assets”).
  - Set conditions at “asset\_type” from “Existing Asset”.
- If filters.get(“asset\_category”).
  - Set conditions at “asset\_category” from filters.get(“asset\_category”).
- If filters.get(“cost\_center”).
  - Set conditions at “cost\_center” from filters.get(“cost\_center”).
- If status.
  - Set operand from “not in”.
  - If status does not belong to “In Location”.
    - Set operand from “in”.
  - Set conditions at “status” from tuple(operand, list(“Sold”, “Scrapped”, “Capitalized”)).
- Return conditions.

**Values supplied outside this operation** clock or generated value from nowdate(), today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L733)

<a id="op-a643a615d0d43f"></a>
### Prepare chart data

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_prepare_chart_data`

**Inputs** data, filters.

**Explicit results** no value · mapping(“data” → mapping(“labels” → labels\_values\_map.keys(), “datasets” → list(mapping(“name” → translated “Asset Value”, “values” → list of flt(nested operand in the contract(nested operand in the contra ….

**Local steps**

- If not data.
  - Return no value.
- Set labels\_values\_map from mapping().
- If filters.filter\_based\_on does not belong to tuple(“Date Range”, “Fiscal Year”).
  - Set filters\_filter\_based\_on from “Date Range”.
  - Set date\_field from “purchase\_date”.
  - Set filtered\_data from list of d for d drawn from data where d.get(date\_field).
    - Draw d from data, keep a combination only if (d.get(date\_field)).
  - Set filters\_from\_date from min(filtered\_data, key = deferred anonymous expression).get(date\_field).
  - Set filters\_to\_date from max(filtered\_data, key = deferred anonymous expression).get(date\_field).
- Otherwise.
  - Set filters\_filter\_based\_on from filters.filter\_based\_on.
  - Set date\_field from Platform.scrub(filters.date\_based\_on).
  - Set filters\_from\_date from filters.from\_date.
  - Set filters\_to\_date from filters.to\_date.
- Set period\_list from get\_period\_list(filters.from\_fiscal\_year, filters.to\_fiscal\_year, filters\_from\_date, filters\_to\_date, company = filters.company, ignore\_fiscal\_year = true, …).
- For each d in period\_list.
  - Evaluate labels\_values\_map.setdefault(d.get(“label”), Platform.\_dict(mapping(“asset\_value” → 0, “depreciated\_amount” → 0))).
- For each d in data.
  - If d.get(date\_field).
    - Set date from d.get(date\_field).
    - Set belongs\_to\_month from formatdate(date, “MMM YYYY”).
    - Update labels\_values\_map at belongs\_to\_month.asset\_value using + d.get(“asset\_value”).
    - Update labels\_values\_map at belongs\_to\_month.depreciated\_amount using + d.get(“depreciated\_amount”).
- Return mapping(“data” → mapping(“labels” → labels\_values\_map.keys(), “datasets” → list(mapping(“name” → translated “Asset Value”, “values” → list of flt(nested operand in the contract(nested operand in the contra ….
  - Draw d from labels\_values\_map.values().
  - Draw d from labels\_values\_map.values().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0333.json#L6224) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L738)

<a id="op-a82c0d8a217f8e"></a>
### Get assets linked to fb

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_assets_linked_to_fb`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** assets\_linked\_to\_fb.

**Explicit failure paths** validation helper — translated “To use a different finance book, please uncheck 'Include Default FB Assets'”.

**Local steps**

- Set afb from Platform.qb.DocType(“Asset Finance Book”).
- Set query from Platform.qb.from\_(afb).select(afb.parent).
- If filters.include\_default\_book\_assets.
  - Set company\_fb from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).
  - If (filters.finance\_book and company\_fb and cstr(filters.finance\_book) differs from cstr(company\_fb)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.finance\_book → company\_fb → cstr(filters.finance\_book) differs from cstr(company\_fb).
    - Call the validation error handler Platform.throw(translated “To use a different finance book, please uncheck 'Include Default FB Assets'”).
  - Set query from query.where((afb.finance\_book.isin(list(cstr(filters.finance\_book), cstr(company\_fb), empty text)) bitwise or afb.finance\_book.isnull())).
- Otherwise.
  - Set query from query.where((afb.finance\_book.isin(list(cstr(filters.finance\_book), empty text)) bitwise or afb.finance\_book.isnull())).
- Set assets\_linked\_to\_fb from set(chain(expanded query.run(as\_list = 1))).
- Return assets\_linked\_to\_fb.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_finance\_book”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L81) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L731)

<a id="op-cb67294961f514"></a>
### Value assets on first finance book

`operation_enterprise_binding_enterprise_assets_report_fixed_asset_register_fixed_asset_register_value_assets_on_first_finance_book`

**Inputs** filters, assets\_linked\_to\_fb, depreciation\_amount\_map, revaluation\_amount\_map.

**Declared result** no value.

**Local steps**

- Set first\_finance\_books from get\_first\_finance\_books(assets\_linked\_to\_fb).
- For each finance\_book in set(first\_finance\_books.values()).
  - Set book\_depreciation\_map from get\_asset\_depreciation\_amount\_map(filters, finance\_book).
  - Set book\_revaluation\_map from get\_asset\_value\_adjustment\_map(filters, finance\_book).
  - For each tuple(asset, asset\_finance\_book) in first\_finance\_books.items().
    - If asset\_finance\_book equals finance\_book.
      - Set depreciation\_amount\_map at asset from book\_depreciation\_map.get(asset, 0.0).
      - Set revaluation\_amount\_map at asset from book\_revaluation\_map.get(asset, 0.0).
- Evaluate assets\_linked\_to\_fb.update(first\_finance\_books).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L786) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L26)

<a id="op-24b55528beb52b"></a>
### Get first finance books

`operation_enterprise_binding_enterprise_assets_report_fixed_asset_register_fixed_asset_register_get_first_finance_books`

**Inputs** assets\_linked\_to\_fb.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping of asset → finance\_book for tuple(asset, finance\_book) drawn from rows where (finance\_book and asset does not belong to assets\_linked\_to\_fb).

**Local steps**

- Set afb from Platform.qb.DocType(“Asset Finance Book”).
- Set rows from nested operand in the contract(nested operand in the contract).select(afb.parent, afb.finance\_book).where((afb.parenttype equals “Asset” bitwise and afb.idx equals 1)).run().
- Return mapping of asset → finance\_book for tuple(asset, finance\_book) drawn from rows where (finance\_book and asset does not belong to assets\_linked\_to\_fb).
  - Draw tuple(asset, finance\_book) from rows, keep a combination only if ((finance\_book and asset does not belong to assets\_linked\_to\_fb)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in finance\_book → asset does not belong to assets\_linked\_to\_fb.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L23)

<a id="op-8457e076643c52"></a>
### Get asset depreciation amount map

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_asset_depreciation_amount_map`

**Inputs** filters, finance\_book.

**Explicit results** dict(asset\_depr\_amount\_map).

**Local steps**

- Set start\_date from filters.from\_date when filters.filter\_based\_on equals “Date Range”, otherwise filters.year\_start\_date.
  - Value choice on filters.filter\_based\_on equals “Date Range” — true gives filters.from\_date, false gives filters.year\_start\_date.
- Set end\_date from filters.to\_date when filters.filter\_based\_on equals “Date Range”, otherwise filters.year\_end\_date.
  - Value choice on filters.filter\_based\_on equals “Date Range” — true gives filters.to\_date, false gives filters.year\_end\_date.
- Set asset from Platform.qb.DocType(“Asset”).
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set aca from Platform.qb.DocType(“Asset Category Account”).
- Set company from Platform.qb.DocType(“Company”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_opening equals “No”).where(company.name equals filters.company).where(asset.docstatus equals 1).
- If filters.only\_existing\_assets.
  - Set query from query.where(asset.asset\_type equals “Existing Asset”).
- If filters.asset\_category.
  - Set query from query.where(asset.asset\_category equals filters.asset\_category).
- If filters.cost\_center.
  - Set query from query.where(asset.cost\_center equals filters.cost\_center).
- If filters.status.
  - If filters.status equals “In Location”.
    - Set query from query.where(asset.status.notin(list(“Sold”, “Scrapped”, “Capitalized”))).
  - Otherwise.
    - Set query from query.where(asset.status.isin(list(“Sold”, “Scrapped”, “Capitalized”))).
- If finance\_book.
  - Set query from query.where((gle.finance\_book.isin(list(cstr(finance\_book), empty text)) bitwise or gle.finance\_book.isnull())).
- Otherwise.
  - Set query from query.where((gle.finance\_book.isin(list(empty text)) bitwise or gle.finance\_book.isnull())).
- If filters.filter\_based\_on belongs to tuple(“Date Range”, “Fiscal Year”).
  - Set query from query.where(gle.posting\_date ≥ start\_date).
  - Set query from query.where(gle.posting\_date ≤ end\_date).
- Set query from query.groupby(asset.name).
- Set asset\_depr\_amount\_map from query.run().
- Return dict(asset\_depr\_amount\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L79) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L729)

<a id="op-aab94a2a4ac0f2"></a>
### Get asset value adjustment map

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_asset_value_adjustment_map`

**Inputs** filters, finance\_book.

**Explicit results** dict(asset\_adjustment\_map).

**Local steps**

- Set start\_date from filters.from\_date when filters.filter\_based\_on equals “Date Range”, otherwise filters.year\_start\_date.
  - Value choice on filters.filter\_based\_on equals “Date Range” — true gives filters.from\_date, false gives filters.year\_start\_date.
- Set end\_date from filters.to\_date when filters.filter\_based\_on equals “Date Range”, otherwise filters.year\_end\_date.
  - Value choice on filters.filter\_based\_on equals “Date Range” — true gives filters.to\_date, false gives filters.year\_end\_date.
- Set asset from Platform.qb.DocType(“Asset”).
- Set gle from Platform.qb.DocType(“GL Entry”).
- Set aca from Platform.qb.DocType(“Asset Category Account”).
- Set company from Platform.qb.DocType(“Company”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.is\_opening equals “No”).where(company.name equals filters.company).where(asset.docstatus equals 1).
- If filters.only\_existing\_assets.
  - Set query from query.where(asset.asset\_type equals “Existing Asset”).
- If filters.asset\_category.
  - Set query from query.where(asset.asset\_category equals filters.asset\_category).
- If filters.cost\_center.
  - Set query from query.where(asset.cost\_center equals filters.cost\_center).
- If filters.status.
  - If filters.status equals “In Location”.
    - Set query from query.where(asset.status.notin(list(“Sold”, “Scrapped”, “Capitalized”))).
  - Otherwise.
    - Set query from query.where(asset.status.isin(list(“Sold”, “Scrapped”, “Capitalized”))).
- If finance\_book.
  - Set query from query.where((gle.finance\_book.isin(list(cstr(finance\_book), empty text)) bitwise or gle.finance\_book.isnull())).
- Otherwise.
  - Set query from query.where((gle.finance\_book.isin(list(empty text)) bitwise or gle.finance\_book.isnull())).
- If filters.filter\_based\_on belongs to tuple(“Date Range”, “Fiscal Year”).
  - Set query from query.where(gle.posting\_date ≥ start\_date).
  - Set query from query.where(gle.posting\_date ≤ end\_date).
- Set query from query.groupby(asset.name).
- Set asset\_adjustment\_map from query.run().
- Return dict(asset\_adjustment\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0334.json#L2120) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L80) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L730)

<a id="op-bd605d3da6baf4"></a>
### Get group by data

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_group_by_data`

**Inputs** group\_by, conditions, assets\_linked\_to\_fb, depreciation\_amount\_map, revaluation\_amount\_map, end\_date.

**Record and data access** read “Asset” via get\_list.

**Explicit results** data.

**Local steps**

- Set fields from list(group\_by, “name”, “net\_purchase\_amount”, “opening\_accumulated\_depreciation”, …).
- Set assets from Platform.get\_list(“Asset”, filters = conditions, fields = fields).
- Set data from list().
- For each a in assets.
  - If (a.calculate\_depreciation and a.name does not belong to assets\_linked\_to\_fb).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.calculate\_depreciation → a.name does not belong to assets\_linked\_to\_fb.
    - Continue with the next iteration or loop test.
  - Set a at “depreciated\_amount” from depreciation\_amount\_map.get(a at “name”, 0.0).
  - Set a at “revaluation\_amount” from revaluation\_amount\_map.get(a at “name”, 0.0).
  - Set a at “asset\_value” from get\_asset\_value(a, a at “depreciated\_amount”, a at “revaluation\_amount”, end\_date).
  - Remove a at “name”.
  - Remove a at “calculate\_depreciation”.
  - Remove a at “status”.
  - Remove a at “disposal\_date”.
  - Set idx from (list of i for tuple(i, d) drawn from enumerate(data) where a at group\_by equals d at group\_by or list(no value)) at 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of i for tuple(i, d) drawn from enumerate(data) where a at group\_by equals d at group\_by → list(no value).
    - Draw tuple(i, d) from enumerate(data), keep a combination only if (a at group\_by equals d at group\_by).
  - If idx is identical to no value.
    - Evaluate data.append(a).
  - Otherwise.
    - For each field in tuple(“net\_purchase\_amount”, “opening\_accumulated\_depreciation”, “depreciated\_amount”, “asset\_value”).
      - Set data at idx at field from (data at idx at field + a at field).
- Return data.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L85) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L735)

<a id="op-d835664f3b1758"></a>
### Get purchase receipt supplier map

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_purchase_receipt_supplier_map`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Purchase Receipt).

**Explicit results** Platform.\_dict(Platform.db.sql(query text (SELECT, Purchase Receipt))).

**Local steps**

- Return Platform.\_dict(Platform.db.sql(query text (SELECT, Purchase Receipt))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L87) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L737)

<a id="op-9a357c2f2a68a9"></a>
### Get purchase invoice supplier map

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_purchase_invoice_supplier_map`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Purchase Invoice).

**Explicit results** Platform.\_dict(Platform.db.sql(query text (SELECT, Purchase Invoice))).

**Local steps**

- Return Platform.\_dict(Platform.db.sql(query text (SELECT, Purchase Invoice))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L86) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L736)

<a id="op-423ed88376ba6b"></a>
### Get columns

`operation_enterprise_assets_report_fixed_asset_register_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated filters.get(“group\_by”), “fieldtype” → “Link”, “fieldname” → Platform.scrub(filters.get(“group\_by”)), “options” → filters.get(“group\_by”), …), mapping(“label” → translated … · list(mapping(“label” → translated “Asset ID”, “fieldtype” → “Link”, “fieldname” → “asset\_id”, “options” → “Asset”, …), mapping(“label” → translated “Asset Name”, “fieldtype” → “Data”, “fieldname” → “asset\_ ….

**Local steps**

- If filters.get(“group\_by”) belongs to list(“Asset Category”, “Location”).
  - Return list(mapping(“label” → translated filters.get(“group\_by”), “fieldtype” → “Link”, “fieldname” → Platform.scrub(filters.get(“group\_by”)), “options” → filters.get(“group\_by”), …), mapping(“label” → translated ….
- Return list(mapping(“label” → translated “Asset ID”, “fieldtype” → “Link”, “fieldname” → “asset\_id”, “options” → “Asset”, …), mapping(“label” → translated “Asset Name”, “fieldtype” → “Data”, “fieldname” → “asset\_ ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L732)

## Record · Location

[Record definition](../../../../data/record-types/location.json)

<a id="op-7405829bfe542b"></a>
### Location.validate

`operation_enterprise_assets_record_definitions_location_business_behavior_location_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_coordinates().
- Evaluate self.calculate\_location\_area().
- Set self.previous\_ancestors from list() when self.is\_new(), otherwise self.get\_ancestors().
  - Value choice on self.is\_new() — true gives list(), false gives self.get\_ancestors().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate coordinates](operations-020.md#op-b898d6bc6cd078), [calculate location area](operations-020.md#op-44ff11e16cb4d8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L723)

<a id="op-66e6457f16c615"></a>
### Location.on update

`operation_enterprise_assets_record_definitions_location_business_behavior_location_on_update`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_update(self).
- Evaluate self.update\_ancestor\_location\_features().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update ancestor location features](operations-020.md#op-084ede4fb61d27).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L720)

<a id="op-ddb6bc783fc024"></a>
### Location.on trash

`operation_enterprise_assets_record_definitions_location_business_behavior_location_on_trash`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.validate\_if\_child\_exists(self).
- Set ancestors from self.get\_ancestors().
- Evaluate update\_nsm(self).
- For each ancestor in ancestors.
  - Evaluate set\_features\_in\_ancestor(ancestor, set(self.location\_name), list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0008.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L68) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L719)
