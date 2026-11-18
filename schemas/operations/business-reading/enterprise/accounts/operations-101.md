# Accounting and settlement · operations 101

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sales invoice

[Record definition](../../../../data/record-types/sales_invoice.json)

<a id="op-40c79212842ff2"></a>
### Sales Invoice.validate account for change amount

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_account_for_change_amount`

**Inputs** self.

**Local steps**

- If (flt(self.change\_amount) and not self.account\_for\_change\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(self.change\_amount) → not self.account\_for\_change\_amount.
  - Evaluate msgprint(translated “Please enter Account for Change Amount”, raise\_exception = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L5866) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1050) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1180)

<a id="op-38f3777437a5bc"></a>
### Sales Invoice.validate dropship item

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_validate_dropship_item`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Stock cannot be updated because the invoice contains a drop shipping item. Please disable 'Update Stock' or  …”.

**Local steps**

- If not cint(self.update\_stock).
  - Return no value.
- If any(generator of item.delivered\_by\_supplier for item drawn from self.items).
  - Draw item from self.items.
  - Call the validation error handler Platform.throw(translated “Stock cannot be updated because the invoice contains a drop shipping item. Please disable 'Update Stock' or  …”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L6122) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1056) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1185)

<a id="op-3f5a6b0a462c8a"></a>
### Sales Invoice.update current stock

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_update_current_stock`

**Inputs** self.

**Local steps**

- Set bin\_qty\_map from get\_bin\_qty\_map((self.items + self.packed\_items)).
- For each item in self.items.
  - If (item.item\_code and item.warehouse).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code → item.warehouse.
    - Set bin\_data from bin\_qty\_map.get(tuple(item.item\_code, item.warehouse)).
    - Set item.actual\_qty from bin\_data.actual\_qty when bin\_data, otherwise 0.
      - Value choice on bin\_data — true gives bin\_data.actual\_qty, false gives 0.
- For each packed\_item in self.packed\_items.
  - Set bin\_data from bin\_qty\_map.get(tuple(packed\_item.item\_code, packed\_item.warehouse)).
  - Set packed\_item.actual\_qty from bin\_data.actual\_qty when bin\_data, otherwise 0.
    - Value choice on bin\_data — true gives bin\_data.actual\_qty, false gives 0.
  - Set packed\_item.projected\_qty from bin\_data.projected\_qty when bin\_data, otherwise 0.
    - Value choice on bin\_data — true gives bin\_data.projected\_qty, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L6277) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1045) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1175)

<a id="op-ad8e0241ec5f48"></a>
### Sales Invoice.update packing list

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_update_packing_list`

**Inputs** self.

**Local steps**

- If cint(self.update\_stock) equals 1.
  - Bind dependencies make\_packing\_list.
  - Evaluate make\_packing\_list(self).
- Otherwise.
  - Evaluate self.set(“packed\_items”, list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L6605) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1046) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1176)

<a id="op-aa34ef29b7c805"></a>
### Sales Invoice.set billing hours and amount

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_set_billing_hours_and_amount`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.is\_return.
  - Return no value.
- Set pending from list of row for row drawn from self.timesheets where (row.time\_sheet and not (row.timesheet\_detail and row.billing\_hours and row.billing\_amount)).
  - Draw row from self.timesheets, keep a combination only if ((row.time\_sheet and not (row.timesheet\_detail and row.billing\_hours and row.billing\_amount))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.time\_sheet → not (row.timesheet\_detail and row.billing\_hours and row.billing\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.timesheet\_detail → row.billing\_hours → row.billing\_amount.
- Set unbilled\_logs from mapping of name → get\_projectwise\_timesheet\_data(self.project, name) for name drawn from set of row.time\_sheet for row drawn from pending.
  - Draw name from set of row.time\_sheet for row drawn from pending.
  - Draw row from pending.
- Set exchange\_rates from mapping().
- For each row in pending.
  - If row.timesheet\_detail.
    - Evaluate self.fill\_from\_time\_log(row, unbilled\_logs at row.time\_sheet, exchange\_rates).
  - Otherwise.
    - Evaluate self.replace\_with\_time\_logs(row, unbilled\_logs at row.time\_sheet, exchange\_rates).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fill from time log](operations-101.md#op-b8d870c2bb9ce7), [replace with time logs](operations-101.md#op-89340d71d7ed3b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L403) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1041)

<a id="op-b8d870c2bb9ce7"></a>
### Sales Invoice.fill from time log

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_fill_from_time_log`

**Inputs** self, row, time\_logs, exchange\_rates.

**Local steps**

- If log bound to next(generator of log for log drawn from time\_logs where log.name equals row.timesheet\_detail, no value).
  - Draw log from time\_logs, keep a combination only if (log.name equals row.timesheet\_detail).
  - Set row.billing\_hours from (row.billing\_hours or log.billing\_hours).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.billing\_hours → log.billing\_hours.
  - Set row.billing\_amount from (row.billing\_amount or self.get\_billing\_amount(log, exchange\_rates)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.billing\_amount → self.get\_billing\_amount(log, exchange\_rates).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get billing amount](operations-101.md#op-a5d7ae3a99b60d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1012)

<a id="op-89340d71d7ed3b"></a>
### Sales Invoice.replace with time logs

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_replace_with_time_logs`

**Inputs** self, row, time\_logs, exchange\_rates.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row {0}: Timesheet {1} has no unbilled billable time logs”.format(row.idx, Platform.bold(row.time\_sheet)).

**Local steps**

- Set listed from set of d.timesheet\_detail for d drawn from self.timesheets.
  - Draw d from self.timesheets.
- Set time\_logs from list of log for log drawn from time\_logs where log.name does not belong to listed.
  - Draw log from time\_logs, keep a combination only if (log.name does not belong to listed).
- If not time\_logs.
  - Call the validation error handler Platform.throw(translated “Row {0}: Timesheet {1} has no unbilled billable time logs”.format(row.idx, Platform.bold(row.time\_sheet))).
- If row.billing\_amount.
  - Evaluate self.link\_time\_log(row, time\_logs).
  - Return no value.
- Evaluate self.remove(row).
- For each log in time\_logs.
  - Evaluate self.append(“timesheets”, self.get\_timesheet\_row(log, exchange\_rates)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [link time log](operations-101.md#op-7f99e6d854cbf9), [get timesheet row](operations-101.md#op-39639a5f2faacc).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1038)

<a id="op-7f99e6d854cbf9"></a>
### Sales Invoice.link time log

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_link_time_log`

**Inputs** self, row, time\_logs.

**Explicit failure paths** validation helper — translated “Row {0}: Select the time log of Timesheet {1} that this amount bills”.format(row.idx, Platform.bold(row.time\_sheet)).

**Local steps**

- <a id="op-7f99e6d854cbf9-guard-3"></a>If len(time\_logs) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Row {0}: Select the time log of Timesheet {1} that this amount bills”.format(row.idx, Platform.bold(row.time\_sheet))).
- Set row.timesheet\_detail from time\_logs at 0.name.
- Set row.billing\_hours from (row.billing\_hours or time\_logs at 0.billing\_hours).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.billing\_hours → time\_logs at 0.billing\_hours.

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(time\_logs) &gt; 1, length of time\_logs = 2 selects the branch that calls the validation-error handler with translated “Row {0}: Select the time log of Timesheet {1} that this amount bills”.format(row.idx, Platform.bold(row.time\_sheet)). With length of time\_logs = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7f99e6d854cbf9-guard-3)

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1027)

<a id="op-1434e787121303"></a>
### Sales Invoice.update timesheet billing for project

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_update_timesheet_billing_for_project`

**Inputs** self.

**Local steps**

- If (not self.is\_return and not self.timesheets and self.project and self.has\_value\_changed(“project”) and self.is\_auto\_fetch\_timesheet\_enabled()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → not self.timesheets → self.project → self.has\_value\_changed(“project”) → self.is\_auto\_fetch\_timesheet\_enabled().
  - Evaluate self.add\_timesheet\_data().
- Otherwise.
  - Evaluate self.calculate\_billing\_amount\_for\_timesheet().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is auto fetch timesheet enabled](operations-101.md#op-f0abee473af68d), [add timesheet data](operations-101.md#op-4a0b523e49b876), [calculate billing amount for timesheet](operations-101.md#op-e4a6eba3585afc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1051)

<a id="op-f0abee473af68d"></a>
### Sales Invoice.is auto fetch timesheet enabled

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_is_auto_fetch_timesheet_enabled`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Projects Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“Projects Settings”, “fetch\_timesheet\_in\_sales\_invoice”).

**Local steps**

- Return Platform.db.get\_single\_value(“Projects Settings”, “fetch\_timesheet\_in\_sales\_invoice”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Projects Settings”, “fetch\_timesheet\_in\_sales\_invoice”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0167.json#L6739) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1026) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1156)

<a id="op-4a0b523e49b876"></a>
### Sales Invoice.add timesheet data

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_add_timesheet_data`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set(“timesheets”, list()).
- If self.project.
  - Set exchange\_rates from mapping().
  - For each data in get\_projectwise\_timesheet\_data(self.project).
    - Evaluate self.append(“timesheets”, self.get\_timesheet\_row(data, exchange\_rates)).
  - Evaluate self.calculate\_billing\_amount\_for\_timesheet().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get timesheet row](operations-101.md#op-39639a5f2faacc), [calculate billing amount for timesheet](operations-101.md#op-e4a6eba3585afc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1013) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1143)

<a id="op-39639a5f2faacc"></a>
### Sales Invoice.get timesheet row

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_timesheet_row`

**Inputs** self, time\_log, exchange\_rates.

**Declared result** dict.

**Explicit results** mapping(“time\_sheet” → time\_log.time\_sheet, “billing\_hours” → time\_log.billing\_hours, “billing\_amount” → self.get\_billing\_amount(time\_log, exchange\_rates), “timesheet\_detail” → time\_log.name, …).

**Local steps**

- Return mapping(“time\_sheet” → time\_log.time\_sheet, “billing\_hours” → time\_log.billing\_hours, “billing\_amount” → self.get\_billing\_amount(time\_log, exchange\_rates), “timesheet\_detail” → time\_log.name, …).

**Methods declared on this owner** [get billing amount](operations-101.md#op-a5d7ae3a99b60d).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1025)

<a id="op-a5d7ae3a99b60d"></a>
### Sales Invoice.get billing amount

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_billing_amount`

**Inputs** self, time\_log, exchange\_rates.

**Declared result** float.

**Explicit results** time\_log.billing\_amount · (flt(time\_log.billing\_amount) × exchange\_rates at time\_log.currency).

**Explicit failure paths** validation helper — translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually.”.format(time\_log.currency, self.currency, self.posting\_date).

**Local steps**

- If (not time\_log.currency or time\_log.currency equals self.currency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not time\_log.currency → time\_log.currency equals self.currency.
  - Return time\_log.billing\_amount.
- If time\_log.currency does not belong to exchange\_rates.
  - Set exchange\_rate from get\_exchange\_rate(time\_log.currency, self.currency, self.posting\_date).
  - If not exchange\_rate.
    - Call the validation error handler Platform.throw(translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually.”.format(time\_log.currency, self.currency, self.posting\_date)).
  - Set exchange\_rates at time\_log.currency from exchange\_rate.
- Return (flt(time\_log.billing\_amount) × exchange\_rates at time\_log.currency).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1014)

<a id="op-e4a6eba3585afc"></a>
### Sales Invoice.calculate billing amount for timesheet

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_calculate_billing_amount_for_timesheet`

**Inputs** self.

**Local steps**

- Bind local operation timesheet\_sum for subsequent calls.
- Set self.total\_billing\_amount from timesheet\_sum(“billing\_amount”).
- Set self.total\_billing\_hours from timesheet\_sum(“billing\_hours”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1004)

<a id="op-f793c10e5ad51d"></a>
### Sales Invoice.calculate billing amount for timesheet.timesheet sum

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_calculate_billing_amount_for_timesheet_timesheet_sum`

**Inputs** field.

**Explicit results** sum(generator of (ts.get(field) or 0.0) for ts drawn from self.timesheets).

**Local steps**

- Return sum(generator of (ts.get(field) or 0.0) for ts drawn from self.timesheets).
  - Draw ts from self.timesheets.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ts.get(field) → 0.0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1005)

<a id="op-b79cd60fa881e1"></a>
### Sales Invoice.get warehouse

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_warehouse`

**Inputs** self.

**Record and data access** execute query text (SELECT, POS Profile).

**Explicit results** warehouse.

**Local steps**

- Set user\_pos\_profile from Platform.db.sql(query text (SELECT, POS Profile), tuple(Platform.session at “user”, self.company)).
- Set warehouse from user\_pos\_profile at 0 at 1 when user\_pos\_profile, otherwise no value.
  - Value choice on user\_pos\_profile — true gives user\_pos\_profile at 0 at 1, false gives no value.
- If not warehouse.
  - Set global\_pos\_profile from Platform.db.sql(query text (SELECT, POS Profile), self.company).
  - If global\_pos\_profile.
    - Set warehouse from global\_pos\_profile at 0 at 1.
  - Otherwise.
    - If not user\_pos\_profile.
      - Evaluate msgprint(translated “POS Profile required to make POS Entry”, raise\_exception = true).
- Return warehouse.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1026)

<a id="op-c58233b7079f3f"></a>
### Sales Invoice.set income account for fixed assets

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_set_income_account_for_fixed_assets`

**Inputs** self.

**Local steps**

- For each item in self.items.
  - Evaluate item.set\_income\_account\_for\_fixed\_asset(self.company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L404) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1042)

<a id="op-e62cfe01aef787"></a>
### Sales Invoice.check prev docstatus

`operation_enterprise_accounts_record_definitions_sales_invoice_business_behavior_sales_invoice_check_previous_record_state`

**Inputs** self.

**Record and data access** read “Sales Order” via get\_value · read “Delivery Note” via get\_value.

**Explicit failure paths** validation helper — translated “Sales Order {0} is not submitted”.format(d.sales\_order).

**Local steps**

- For each d in self.get(“items”).
  - If (d.sales\_order and Platform.db.get\_value(“Sales Order”, d.sales\_order, “docstatus”, cache = true) differs from 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.sales\_order → Platform.db.get\_value(“Sales Order”, d.sales\_order, “docstatus”, cache = true) differs from 1.
    - Call the validation error handler Platform.throw(translated “Sales Order {0} is not submitted”.format(d.sales\_order)).
  - If (d.delivery\_note and Platform.db.get\_value(“Delivery Note”, d.delivery\_note, “docstatus”, cache = true) differs from 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.delivery\_note → Platform.db.get\_value(“Delivery Note”, d.delivery\_note, “docstatus”, cache = true) differs from 1.
    - Evaluate throw(translated “Delivery Note {0} is not submitted”.format(d.delivery\_note)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0168.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L1149)

<a id="op-e158713d18972b"></a>
### Sales Invoice.split asset based on sale qty

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_split_asset_based_on_sale_qty`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Sell quantity cannot exceed the asset quantity. Asset {0} has only {1} item(s).”.format(asset, qty at “actual\_qty”).

**Local steps**

- Set asset\_qty\_map from self.get\_asset\_qty().
- For each tuple(asset, qty) in asset\_qty\_map.items().
  - If qty at “actual\_qty” &lt; qty at “sale\_qty”.
    - Call the validation error handler Platform.throw(translated “Sell quantity cannot exceed the asset quantity. Asset {0} has only {1} item(s).”.format(asset, qty at “actual\_qty”)).
  - Set remaining\_qty from (qty at “actual\_qty” − qty at “sale\_qty”).
  - If remaining\_qty &gt; 0.
    - Evaluate split\_asset(asset, remaining\_qty).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get asset qty](operations-101.md#op-53f03d8a01294e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L407) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1045)

<a id="op-53f03d8a01294e"></a>
### Sales Invoice.get asset qty

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_asset_qty`

**Inputs** self.

**Record and data access** read “Asset” via get\_all.

**Explicit results** asset\_qty\_map.

**Local steps**

- Set asset\_qty\_map from mapping().
- Set assets from set of row.asset for row drawn from self.items where (row.is\_fixed\_asset and row.asset).
  - Draw row from self.items, keep a combination only if ((row.is\_fixed\_asset and row.asset)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_fixed\_asset → row.asset.
- If (not assets or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not assets → self.is\_return.
  - Return asset\_qty\_map.
- Set asset\_actual\_qty from dict(Platform.db.get\_all(“Asset”, mapping(“name” → list(“in”, list(assets))), list(“name”, “asset\_quantity”), as\_list = true)).
- For each row in self.items.
  - If (row.is\_fixed\_asset and row.asset).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.is\_fixed\_asset → row.asset.
    - Set actual\_qty from asset\_actual\_qty.get(row.asset).
    - If row.asset belongs to asset\_qty\_map.keys().
      - Update asset\_qty\_map at row.asset at “sale\_qty” using + flt(row.qty).
    - Otherwise.
      - Evaluate asset\_qty\_map.setdefault(row.asset, mapping(“sale\_qty” → flt(row.qty), “actual\_qty” → flt(actual\_qty))).
- Return asset\_qty\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1013)

<a id="op-50d3c2f8a2f1a8"></a>
### Sales Invoice.process asset depreciation

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_process_asset_depreciation`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.is\_internal\_transfer().
  - Return no value.
- If ((self.is\_return and self.docstatus equals 2) or (not self.is\_return and self.docstatus equals 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.is\_return and self.docstatus equals 2) → (not self.is\_return and self.docstatus equals 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.docstatus equals 2.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_return → self.docstatus equals 1.
  - Evaluate self.depreciate\_asset\_on\_sale().
- Otherwise.
  - Evaluate self.restore\_asset().
- Evaluate self.update\_asset().

If control reaches the end, it returns no value.

**Methods declared on this owner** [depreciate asset on sale](operations-101.md#op-ca3705a2254019), [restore asset](operations-102.md#op-bca9e6987d3bea), [update asset](operations-102.md#op-5a3a12b9930c39).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1037)

<a id="op-35743dfc88611e"></a>
### Sales Invoice.set asset disposal values

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_set_asset_disposal_values`

**Inputs** self.

**Declared result** no value.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** call db\_set on item.

**Explicit results** no value.

**Local steps**

- If self.is\_internal\_transfer().
  - Return no value.
- For each item in self.get(“items”).
  - If (item.is\_fixed\_asset and item.asset).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_fixed\_asset → item.asset.
    - Set asset from Platform.get\_doc(“Asset”, item.asset).
    - Set values from get\_asset\_disposal\_values(asset, item.finance\_book).
    - Evaluate item.db\_set(mapping(“asset\_value\_after\_depreciation” → values at “value\_after\_depreciation”, “asset\_gross\_value” → values at “gross\_asset\_value”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1040)

<a id="op-ca3705a2254019"></a>
### Sales Invoice.depreciate asset on sale

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_depreciate_asset_on_sale`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**Local steps**

- Set disposal\_date from self.get\_disposal\_date().
- For each d in self.get(“items”).
  - If d.asset.
    - Set asset from Platform.get\_doc(“Asset”, d.asset).
    - If (asset.calculate\_depreciation and asset.status differs from “Fully Depreciated”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in asset.calculate\_depreciation → asset.status differs from “Fully Depreciated”.
      - Evaluate depreciate\_asset(asset, disposal\_date, self.get\_note\_for\_asset\_sale(asset)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get disposal date](operations-102.md#op-7b77f56c5f6393), [get note for asset sale](operations-101.md#op-d962e705ff2b4a).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1011)

<a id="op-d962e705ff2b4a"></a>
### Sales Invoice.get note for asset sale

`operation_enterprise_binding_enterprise_accounts_doctype_sales_invoice_sales_invoice_salesinvoice_get_note_for_asset_sale`

**Inputs** self, asset.

**Explicit results** translated “This schedule was created when Asset {0} was {1} through Sales Invoice {2}.”.format(get\_link\_to\_form(asset.doctype, asset.name), translated “returned” when self.is\_return, otherwise translated  ….

**Local steps**

- Return translated “This schedule was created when Asset {0} was {1} through Sales Invoice {2}.”.format(get\_link\_to\_form(asset.doctype, asset.name), translated “returned” when self.is\_return, otherwise translated  ….
  - Value choice on self.is\_return — true gives translated “returned”, false gives translated “sold”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1021)
