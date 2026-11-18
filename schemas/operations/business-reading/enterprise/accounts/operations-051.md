# Accounting and settlement · operations 51

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Gross and net profit report

<a id="op-10491baa93f04d"></a>
### Get net profit

`operation_enterprise_accounts_report_gross_and_net_profit_report_business_behavior_get_net_profit`

**Inputs** non\_gross\_income, gross\_income, gross\_expense, non\_gross\_expense, period\_list, company, currency = no value, consolidated = false.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** profit\_loss.

**Local steps**

- Set profit\_loss from mapping(“account\_name” → ((“'” + translated “Net Profit”) + “'”), “account” → ((“'” + translated “Net Profit”) + “'”), “warn\_if\_negative” → true, “currency” → (currency or Platform.get\_cached\_value(“Compan ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set has\_value from false.
- Set gross\_income\_roots from list of row for row drawn from (gross\_income or list()) where not flt(row.get(“indent”)).
  - Draw row from (gross\_income or list()), keep a combination only if (not flt(row.get(“indent”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gross\_income → list().
- Set non\_gross\_income\_roots from list of row for row drawn from (non\_gross\_income or list()) where not flt(row.get(“indent”)).
  - Draw row from (non\_gross\_income or list()), keep a combination only if (not flt(row.get(“indent”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in non\_gross\_income → list().
- Set gross\_expense\_roots from list of row for row drawn from (gross\_expense or list()) where not flt(row.get(“indent”)).
  - Draw row from (gross\_expense or list()), keep a combination only if (not flt(row.get(“indent”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in gross\_expense → list().
- Set non\_gross\_expense\_roots from list of row for row drawn from (non\_gross\_expense or list()) where not flt(row.get(“indent”)).
  - Draw row from (non\_gross\_expense or list()), keep a combination only if (not flt(row.get(“indent”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in non\_gross\_expense → list().
- For each period in period\_list.
  - Set key from period when consolidated, otherwise period.key.
    - Value choice on consolidated — true gives period, false gives period.key.
  - Set gross\_income\_for\_period from sum(generator of flt(row.get(key, 0)) for row drawn from gross\_income\_roots).
    - Draw row from gross\_income\_roots.
  - Set non\_gross\_income\_for\_period from sum(generator of flt(row.get(key, 0)) for row drawn from non\_gross\_income\_roots).
    - Draw row from non\_gross\_income\_roots.
  - Set gross\_expense\_for\_period from sum(generator of flt(row.get(key, 0)) for row drawn from gross\_expense\_roots).
    - Draw row from gross\_expense\_roots.
  - Set non\_gross\_expense\_for\_period from sum(generator of flt(row.get(key, 0)) for row drawn from non\_gross\_expense\_roots).
    - Draw row from non\_gross\_expense\_roots.
  - Set total\_income from (gross\_income\_for\_period + non\_gross\_income\_for\_period).
  - Set total\_expense from (gross\_expense\_for\_period + non\_gross\_expense\_for\_period).
  - Set profit\_loss at key from (flt(total\_income) − flt(total\_expense)).
  - If profit\_loss at key.
    - Set has\_value from true.
    - If not profit\_loss.get(“total”).
      - Set profit\_loss at “total” from 0.
    - Update profit\_loss at “total” using + profit\_loss at key.
- If has\_value.
  - Return profit\_loss.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0254.json#L6088) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L991)

## Report · Gross profit

<a id="op-9a5dfd4ab61707"></a>
### Execute

`operation_enterprise_accounts_report_gross_profit_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not filters.
  - Set filters from Platform.\_dict().
- Set filters.currency from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set gross\_profit\_data from GrossProfitGenerator(filters).
- Set data from list().
- Set group\_wise\_columns from Platform.\_dict(mapping(“invoice” → list(“invoice\_or\_item”, “customer”, “customer\_group”, “customer\_name”, …), “item\_code” → list(“item\_code”, “item\_name”, “brand”, “description”, …), “warehouse” → list(“wa ….
- Set columns from get\_columns(group\_wise\_columns, filters).
- If filters.group\_by equals “Invoice”.
  - Evaluate get\_data\_when\_grouped\_by\_invoice(columns, gross\_profit\_data, filters, group\_wise\_columns, …).
- Otherwise.
  - Evaluate get\_data\_when\_not\_grouped\_by\_invoice(gross\_profit\_data, filters, group\_wise\_columns, data).
- Return tuple(columns, data).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L660) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1004)

<a id="op-c9e04a777a1e6e"></a>
### Get data when grouped by invoice

`operation_enterprise_accounts_report_gross_profit_business_behavior_get_data_when_grouped_by_invoice`

**Inputs** columns, gross\_profit\_data, filters, group\_wise\_columns, data.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Selling Settings” via get\_single\_value.

**State and service calls** call insert on columns.

**Local steps**

- Set column\_names from get\_column\_names().
- Set columns at 0 at “fieldname” from “sales\_invoice”.
- Set columns at 0 at “options” from “Item”.
- Set columns at 0 at “width” from 300.
- Set supplier\_master\_name from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).
- Set customer\_master\_name from Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).
- If (supplier\_master\_name equals “Supplier Name” and customer\_master\_name equals “Customer Name”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in supplier\_master\_name equals “Supplier Name” → customer\_master\_name equals “Customer Name”.
  - Remove columns at 4.
  - Evaluate columns.insert(1, columns.pop(4)).
- Otherwise.
  - Remove columns at 5.
  - Evaluate columns.insert(1, columns.pop(5)).
- Set total\_base\_amount from 0.
- Set total\_buying\_amount from 0.
- For each src in gross\_profit\_data.si\_list.
  - If src.indent equals 1.
    - Update total\_base\_amount using + (src.base\_amount or 0.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in src.base\_amount → 0.0.
    - Update total\_buying\_amount using + (src.buying\_amount or 0.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in src.buying\_amount → 0.0.
  - Set row from Platform.\_dict().
  - Set row.indent from src.indent.
  - Set row.parent\_invoice from src.parent\_invoice.
  - Set row.currency from filters.currency.
  - For each col in group\_wise\_columns.get(scrub(filters.group\_by)).
    - Set row at column\_names at col from src.get(col).
  - Evaluate data.append(row).
- Set total\_gross\_profit from flt((total\_base\_amount + abs(total\_buying\_amount)) when total\_buying\_amount &lt; 0, otherwise (total\_base\_amount − total\_buying\_amount)).
  - Value choice on total\_buying\_amount &lt; 0 — true gives (total\_base\_amount + abs(total\_buying\_amount)), false gives (total\_base\_amount − total\_buying\_amount).
- Evaluate data.append(Platform.\_dict(mapping(“sales\_invoice” → “Total”, “qty” → no value, “avg.\_selling\_rate” → no value, “valuation\_rate” → no value, …))).
  - Value choice on total\_base\_amount — true gives flt(((total\_gross\_profit ÷ abs(total\_base\_amount)) × 100.0), (cint(Platform.db.get\_default(“currency\_precision”)) or 3)), false gives 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“currency\_precision”)) → 3.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”), Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0255.json#L2312) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1007)

<a id="op-ebc4f725774d5c"></a>
### Get data when not grouped by invoice

`operation_enterprise_accounts_report_gross_profit_business_behavior_get_data_when_not_grouped_by_invoice`

**Inputs** gross\_profit\_data, filters, group\_wise\_columns, data.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Buying Settings” via get\_single\_value.

**Local steps**

- Set total\_base\_amount from 0.
- Set total\_buying\_amount from 0.
- Set group\_columns from group\_wise\_columns.get(scrub(filters.group\_by)).
- Set customer\_master\_name from Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).
- Set supplier\_master\_name from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).
- If (“customer\_name” belongs to group\_columns and (supplier\_master\_name equals “Supplier Name” and customer\_master\_name equals “Customer Name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “customer\_name” belongs to group\_columns → (supplier\_master\_name equals “Supplier Name” and customer\_master\_name equals “Customer Name”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in supplier\_master\_name equals “Supplier Name” → customer\_master\_name equals “Customer Name”.
  - Set group\_columns from list of col for col drawn from group\_columns where col differs from “customer\_name”.
    - Draw col from group\_columns, keep a combination only if (col differs from “customer\_name”).
- For each src in gross\_profit\_data.grouped\_data.
  - Update total\_base\_amount using + (src.base\_amount or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in src.base\_amount → 0.0.
  - Update total\_buying\_amount using + (src.buying\_amount or 0.0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in src.buying\_amount → 0.0.
  - Set row from (list of src.get(col) for col drawn from group\_columns + list(filters.currency)).
    - Draw col from group\_columns.
  - Evaluate data.append(row).
- If filters.group\_by equals “Sales Person”.
  - Set amounts from gross\_profit\_data.invoice\_item\_amounts.values().
  - Set total\_base\_amount from sum(generator of flt(amount.base\_amount) for amount drawn from amounts).
    - Draw amount from amounts.
  - Set total\_buying\_amount from sum(generator of flt(amount.buying\_amount) for amount drawn from amounts).
    - Draw amount from amounts.
- Set total\_gross\_profit from flt((total\_base\_amount + abs(total\_buying\_amount)) when total\_buying\_amount &lt; 0, otherwise (total\_base\_amount − total\_buying\_amount)).
  - Value choice on total\_buying\_amount &lt; 0 — true gives (total\_base\_amount + abs(total\_buying\_amount)), false gives (total\_base\_amount − total\_buying\_amount).
- Set currency\_precision from (cint(Platform.db.get\_default(“currency\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“currency\_precision”)) → 3.
- Set gross\_profit\_percent from ((total\_gross\_profit ÷ abs(total\_base\_amount)) × 100.0) when total\_base\_amount, otherwise 0.
  - Value choice on total\_base\_amount — true gives ((total\_gross\_profit ÷ abs(total\_base\_amount)) × 100.0), false gives 0.
- Set total\_row from mapping(group\_columns at 0 → “Total”, “base\_amount” → total\_base\_amount, “buying\_amount” → total\_buying\_amount, “gross\_profit” → total\_gross\_profit, …).
- Set total\_row from list of total\_row.get(col, no value) for col drawn from list(expanded group\_columns, “currency”).
  - Draw col from list(expanded group\_columns, “currency”).
- Evaluate data.append(total\_row).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”), Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1008)

<a id="op-37b5a301dd2242"></a>
### Get columns

`operation_enterprise_accounts_report_gross_profit_business_behavior_get_columns`

**Inputs** group\_wise\_columns, filters.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Selling Settings” via get\_single\_value.

**Explicit results** columns.

**Local steps**

- Set columns from list().
- Set supplier\_master\_name from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”).
- Set customer\_master\_name from Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).
- Set column\_map from Platform.\_dict(mapping(“parent” → mapping(“label” → translated “Sales Invoice”, “fieldname” → “parent\_invoice”, “fieldtype” → “Link”, “options” → “Sales Invoice”, …), “invoice\_or\_item” → mapping(“label” →  ….
- For each col in group\_wise\_columns.get(scrub(filters.group\_by)).
  - If (col equals “customer\_name” and (supplier\_master\_name equals “Supplier Name” and customer\_master\_name equals “Customer Name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in col equals “customer\_name” → (supplier\_master\_name equals “Supplier Name” and customer\_master\_name equals “Customer Name”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in supplier\_master\_name equals “Supplier Name” → customer\_master\_name equals “Customer Name”.
    - Continue with the next iteration or loop test.
  - Evaluate columns.append(column\_map.get(col)).
- Evaluate columns.append(mapping(“fieldname” → “currency”, “label” → translated “Currency”, “fieldtype” → “Link”, “options” → “Currency”, …)).
- Return columns.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “supp\_master\_name”), Platform.db.get\_single\_value(“Selling Settings”, “cust\_master\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0256.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1006)

<a id="op-9920f64f0ff90c"></a>
### Get column names

`operation_enterprise_accounts_report_gross_profit_business_behavior_get_column_names`

**Inputs** no declared parameters.

**Explicit results** Platform.\_dict(mapping(“invoice\_or\_item” → “sales\_invoice”, “customer” → “customer”, “customer\_group” → “customer\_group”, “customer\_name” → “customer\_name”, …)).

**Local steps**

- Return Platform.\_dict(mapping(“invoice\_or\_item” → “sales\_invoice”, “customer” → “customer”, “customer\_group” → “customer\_group”, “customer\_name” → “customer\_name”, …)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0256.json#L3547) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1005)

<a id="op-6591bbc1a3a5ce"></a>
### Gross Profit Generator.initialize

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.sle from mapping().
- Set self.data from list().
- Set self.average\_buying\_rate from mapping().
- Set self.filters from Platform.\_dict(filters).
- Evaluate self.load\_invoice\_items().
- Evaluate self.load\_drop\_ship\_buying\_rates().
- Evaluate self.get\_delivery\_notes().
- Evaluate self.load\_product\_bundle().
- Evaluate self.load\_bundle\_deliveries().
- If filters.group\_by equals “Invoice”.
  - Evaluate self.group\_items\_by\_invoice().
- Evaluate self.load\_non\_stock\_items().
- Evaluate self.get\_returned\_invoice\_items().
- Evaluate self.allocate\_legacy\_return\_items().
- Evaluate self.process().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load invoice items](operations-052.md#op-75c4a6cfacf489), [load drop ship buying rates](operations-052.md#op-0a50cd04568e9c), [get delivery notes](operations-052.md#op-c2af1304132507), [load product bundle](operations-052.md#op-c91a3e47163ed3), [load bundle deliveries](operations-052.md#op-06f8cc7506f608), [group items by invoice](operations-052.md#op-4b415c684af2ab), [load non stock items](operations-052.md#op-2c157d1a2d5d2b), [get returned invoice items](operations-051.md#op-f10143e7b5ecfb), [allocate legacy return items](operations-051.md#op-ad3905a3b25d02), [process](operations-051.md#op-e9929249c5bc80).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1027)

<a id="op-e9929249c5bc80"></a>
### Gross Profit Generator.process

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_process`

**Inputs** self.

**Local steps**

- Set self.grouped from mapping().
- Set self.grouped\_data from list().
- Set self.invoice\_item\_amounts from mapping().
- Set self.currency\_precision from (cint(Platform.db.get\_default(“currency\_precision”)) or 3).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“currency\_precision”)) → 3.
- Set self.float\_precision from (cint(Platform.db.get\_default(“float\_precision”)) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_default(“float\_precision”)) → 2.
- Set grouped\_by\_invoice from true when self.filters.get(“group\_by”) equals “Invoice”, otherwise false.
  - Value choice on self.filters.get(“group\_by”) equals “Invoice” — true gives true, false gives false.
- If grouped\_by\_invoice.
  - Set buying\_amount from 0.
  - Set base\_amount from 0.
- For each row in reversed(self.si\_list).
  - Set sales\_invoice\_item from row.item\_row.
  - If self.filters.get(“group\_by”) equals “Monthly”.
    - Set row.monthly from formatdate(row.posting\_date, “MMM YYYY”).
  - If self.skip\_row(row).
    - Continue with the next iteration or loop test.
  - Set row.base\_amount from flt(row.base\_net\_amount, self.currency\_precision).
  - Set product\_bundles from list().
  - If row.update\_stock.
    - Set product\_bundles from self.product\_bundles.get(row.parenttype, mapping()).get(row.parent, Platform.\_dict()).
  - Otherwise.
    - If row.dn\_detail.
      - Set product\_bundles from self.product\_bundles.get(“Delivery Note”, mapping()).get(row.delivery\_note, Platform.\_dict()).
      - Set row.item\_row from row.dn\_detail.
      - If (product\_bundles and not row.parent).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in product\_bundles → not row.parent.
        - Set product\_bundle from product\_bundles.get(row.parent\_invoice).
        - If product\_bundle.
          - For each packed\_item in product\_bundle.
            - If (packed\_item.get(“item\_code”) equals row.item\_code and packed\_item.get(“parent\_detail\_docname”) equals row.item\_row).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in packed\_item.get(“item\_code”) equals row.item\_code → packed\_item.get(“parent\_detail\_docname”) equals row.item\_row.
              - Set row.warehouse from packed\_item.warehouse.
              - Set row.base\_amount from packed\_item.base\_amount.
  - If (grouped\_by\_invoice and row.indent equals 0.0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in grouped\_by\_invoice → row.indent equals 0.0.
    - Set row.buying\_amount from buying\_amount.
    - Set row.base\_amount from base\_amount.
    - Set buying\_amount from 0.
    - Set base\_amount from 0.
  - Otherwise.
    - If row.is\_debit\_note.
      - If not grouped\_by\_invoice.
        - Set row.qty from 0.
      - Set row.buying\_amount from 0.
    - Otherwise.
      - If row.item\_code belongs to product\_bundles.
        - Set row.buying\_amount from flt(self.get\_buying\_amount\_from\_product\_bundle(row, product\_bundles at row.item\_code), self.currency\_precision).
      - Otherwise.
        - If row.item\_row belongs to self.bundle\_deliveries.
          - Set row.buying\_amount from flt(self.get\_buying\_amount\_from\_delivered\_bundles(row), self.currency\_precision).
        - Otherwise.
          - Set row.buying\_amount from flt(self.get\_buying\_amount(row, row.item\_code), self.currency\_precision).
  - If flt(row.qty).
    - Set row.buying\_rate from flt((row.buying\_amount ÷ flt(row.qty)), self.float\_precision) when not row.delivered\_by\_supplier, otherwise no value.
      - Value choice on not row.delivered\_by\_supplier — true gives flt((row.buying\_amount ÷ flt(row.qty)), self.float\_precision), false gives no value.
    - Set row.base\_rate from flt((row.base\_amount ÷ flt(row.qty)), self.float\_precision).
  - Otherwise.
    - If self.is\_not\_invoice\_row(row).
      - Set tuple(row.buying\_rate, row.base\_rate) from tuple(0.0, 0.0).
  - If self.is\_not\_invoice\_row(row).
    - Evaluate self.update\_return\_invoices(row, sales\_invoice\_item).
  - If (grouped\_by\_invoice and row.indent equals 1.0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in grouped\_by\_invoice → row.indent equals 1.0.
    - Update buying\_amount using + row.buying\_amount.
    - Update base\_amount using + row.base\_amount.
  - Set row.gross\_profit from flt((row.base\_amount + abs(row.buying\_amount)) when row.buying\_amount &lt; 0, otherwise (row.base\_amount − row.buying\_amount), self.currency\_precision).
    - Value choice on row.buying\_amount &lt; 0 — true gives (row.base\_amount + abs(row.buying\_amount)), false gives (row.base\_amount − row.buying\_amount).
  - If row.base\_amount.
    - Set row.gross\_profit\_percent from flt(((row.gross\_profit ÷ abs(row.base\_amount)) × 100.0), self.currency\_precision).
  - Otherwise.
    - Set row.gross\_profit\_percent from 0.0.
  - Evaluate self.grouped.setdefault(row.get(scrub(nested operand in the contract.filters.group\_by)), list()).append(row).
  - Set self.invoice\_item\_amounts at sales\_invoice\_item from Platform.\_dict(base\_amount = row.base\_amount, buying\_amount = row.buying\_amount).
- If self.grouped.
  - Evaluate self.get\_average\_rate\_based\_on\_group\_by().

If control reaches the end, it returns no value.

**Methods declared on this owner** [skip row](operations-051.md#op-52354173d20ccb), [get buying amount from product bundle](operations-051.md#op-e1116ea29e9be4), [get buying amount from delivered bundles](operations-051.md#op-203a8882c0d9c0), [get buying amount](operations-051.md#op-93f11b597462e7), [is not invoice row](operations-051.md#op-87ff65c6c3387c), [update return invoices](operations-051.md#op-8060af7f2a80a3), [get average rate based on group by](operations-051.md#op-9da0b719a22ed2).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1035)

<a id="op-8060af7f2a80a3"></a>
### Gross Profit Generator.update return invoices

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_update_return_invoices`

**Inputs** self, row, sales\_invoice\_item.

**Explicit results** no value.

**Local steps**

- Set returned\_item\_rows from self.returned\_invoices.get(row.parent, mapping()).get(sales\_invoice\_item).
- If not returned\_item\_rows.
  - Return no value.
- For each returned\_item\_row in returned\_item\_rows.
  - If returned\_item\_row.qty differs from 0.
    - If row.qty ≥ abs(returned\_item\_row.qty).
      - Update row.qty using + returned\_item\_row.qty.
      - Update row.base\_amount using + flt(returned\_item\_row.base\_amount, self.currency\_precision).
      - Set returned\_item\_row.qty from 0.
      - Set returned\_item\_row.base\_amount from 0.
    - Otherwise.
      - Update returned\_item\_row.qty using + row.qty.
      - Update returned\_item\_row.base\_amount using + row.base\_amount.
      - Set row.qty from 0.
      - Set row.base\_amount from 0.
- If row.delivered\_by\_supplier.
  - Set buying\_amount from self.get\_drop\_ship\_buying\_amount(row).
  - If buying\_amount is distinct from no value.
    - Set row.buying\_amount from flt(buying\_amount, self.currency\_precision).
- Otherwise.
  - Set row.buying\_amount from flt((flt(row.qty) × flt(row.buying\_rate)), self.currency\_precision).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get drop ship buying amount](operations-052.md#op-411d8554a99e64).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1040)

<a id="op-9da0b719a22ed2"></a>
### Gross Profit Generator.get average rate based on group by

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_average_rate_based_on_group_by`

**Inputs** self.

**Local steps**

- For each key in list(self.grouped).
  - If self.filters.get(“group\_by”) equals “Payment Term”.
    - For each tuple(i, row) in enumerate(self.grouped at key).
      - Set invoice\_portion from 0.
      - If (row.is\_return or (row.invoice\_portion is identical to no value and row.payment\_amount is identical to no value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.is\_return → (row.invoice\_portion is identical to no value and row.payment\_amount is identical to no value).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.invoice\_portion is identical to no value → row.payment\_amount is identical to no value.
        - Set invoice\_portion from 100.
      - Otherwise.
        - If row.invoice\_portion.
          - Set invoice\_portion from row.invoice\_portion.
        - Otherwise.
          - If row.payment\_amount.
            - Set invoice\_portion from ((row.payment\_amount × 100) ÷ row.base\_net\_amount).
      - If i equals 0.
        - Set new\_row from row.
        - Evaluate self.set\_average\_based\_on\_payment\_term\_portion(new\_row, row, invoice\_portion).
      - Otherwise.
        - Set new\_row.qty from flt((new\_row.qty + row.qty), self.float\_precision).
        - Evaluate self.set\_average\_based\_on\_payment\_term\_portion(new\_row, row, invoice\_portion, true).
    - Set new\_row from self.set\_average\_rate(new\_row).
    - Evaluate self.grouped\_data.append(new\_row).
  - Otherwise.
    - If self.filters.get(“group\_by”) differs from “Invoice”.
      - For each tuple(i, row) in enumerate(self.grouped at key).
        - If i equals 0.
          - Set new\_row from row.
        - Otherwise.
          - Set new\_row.qty from flt((new\_row.qty + row.qty), self.float\_precision).
          - Set new\_row.buying\_amount from flt((new\_row.buying\_amount + row.buying\_amount), self.currency\_precision).
          - Set new\_row.base\_amount from flt((new\_row.base\_amount + row.base\_amount), self.currency\_precision).
          - If self.filters.get(“group\_by”) equals “Sales Person”.
            - Set new\_row.allocated\_amount from flt((new\_row.allocated\_amount + row.allocated\_amount), self.currency\_precision).
      - Set new\_row from self.set\_average\_rate(new\_row).
      - Evaluate self.grouped\_data.append(new\_row).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set average based on payment term portion](operations-051.md#op-615981c1b41d73), [set average rate](operations-051.md#op-21d29ec86a7f92).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L670) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1014)

<a id="op-615981c1b41d73"></a>
### Gross Profit Generator.set average based on payment term portion

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_set_average_based_on_payment_term_portion`

**Inputs** self, new\_row, row, invoice\_portion, aggr = false.

**Local steps**

- Set cols from list(“base\_amount”, “buying\_amount”, “gross\_profit”).
- For each col in cols.
  - If aggr.
    - Update new\_row at col using + ((row at col × invoice\_portion) ÷ 100).
  - Otherwise.
    - Set new\_row at col from ((row at col × invoice\_portion) ÷ 100).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L1591) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1036)

<a id="op-87ff65c6c3387c"></a>
### Gross Profit Generator.is not invoice row

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_is_not_invoice_row`

**Inputs** self, row.

**Explicit results** ((self.filters.get(“group\_by”) equals “Invoice” and row.indent differs from 0.0) or self.filters.get(“group\_by”) differs from “Invoice”).

**Local steps**

- Return ((self.filters.get(“group\_by”) equals “Invoice” and row.indent differs from 0.0) or self.filters.get(“group\_by”) differs from “Invoice”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.filters.get(“group\_by”) equals “Invoice” and row.indent differs from 0.0) → self.filters.get(“group\_by”) differs from “Invoice”.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filters.get(“group\_by”) equals “Invoice” → row.indent differs from 0.0.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L1800) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1028)

<a id="op-21d29ec86a7f92"></a>
### Gross Profit Generator.set average rate

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_set_average_rate`

**Inputs** self, new\_row.

**Explicit results** new\_row.

**Local steps**

- Evaluate self.set\_average\_gross\_profit(new\_row).
- Set new\_row.buying\_rate from flt((new\_row.buying\_amount ÷ new\_row.qty), self.float\_precision) when new\_row.qty, otherwise 0.
  - Value choice on new\_row.qty — true gives flt((new\_row.buying\_amount ÷ new\_row.qty), self.float\_precision), false gives 0.
- Set new\_row.base\_rate from flt((new\_row.base\_amount ÷ new\_row.qty), self.float\_precision) when new\_row.qty, otherwise 0.
  - Value choice on new\_row.qty — true gives flt((new\_row.base\_amount ÷ new\_row.qty), self.float\_precision), false gives 0.
- Return new\_row.

**Methods declared on this owner** [set average gross profit](operations-051.md#op-05fff5198647e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L1944) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1038)

<a id="op-05fff5198647e7"></a>
### Gross Profit Generator.set average gross profit

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_set_average_gross_profit`

**Inputs** self, new\_row.

**Local steps**

- Set new\_row.gross\_profit from flt((new\_row.base\_amount + abs(new\_row.buying\_amount)) when new\_row.buying\_amount &lt; 0, otherwise (new\_row.base\_amount − new\_row.buying\_amount), self.currency\_precision).
  - Value choice on new\_row.buying\_amount &lt; 0 — true gives (new\_row.base\_amount + abs(new\_row.buying\_amount)), false gives (new\_row.base\_amount − new\_row.buying\_amount).
- Set new\_row.gross\_profit\_percent from flt(((new\_row.gross\_profit ÷ abs(new\_row.base\_amount)) × 100.0), self.currency\_precision) when new\_row.base\_amount, otherwise 0.
  - Value choice on new\_row.base\_amount — true gives flt(((new\_row.gross\_profit ÷ abs(new\_row.base\_amount)) × 100.0), self.currency\_precision), false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L2178) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1037)

<a id="op-f10143e7b5ecfb"></a>
### Gross Profit Generator.get returned invoice items

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_returned_invoice_items`

**Inputs** self.

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set si\_item from Platform.qb.DocType(“Sales Invoice Item”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.parent).select(si.name, si\_item.item\_code, si\_item.sales\_invoice\_ ….
- If self.filters.company.
  - Set query from query.where(si.company equals self.filters.company).
- Set returned\_invoices from query.run(as\_dict = 1).
- Set self.returned\_invoices from Platform.\_dict().
- Set self.legacy\_returned\_invoices from Platform.\_dict().
- For each inv in returned\_invoices.
  - Set invoice\_returns from self.returned\_invoices when inv.sales\_invoice\_item, otherwise self.legacy\_returned\_invoices.
    - Value choice on inv.sales\_invoice\_item — true gives self.returned\_invoices, false gives self.legacy\_returned\_invoices.
  - Evaluate invoice\_returns.setdefault(inv.return\_against, nested operand in the contract.\_dict()).setdefault((inv.sales\_invoice\_item or inv.item\_code), list()).append(inv).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in inv.sales\_invoice\_item → inv.item\_code.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1024)

<a id="op-ad3905a3b25d02"></a>
### Gross Profit Generator.allocate legacy return items

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_allocate_legacy_return_items`

**Inputs** self.

**Local steps**

- Set source\_invoice\_items from mapping().
- For each row in reversed(self.si\_list).
  - If (row.is\_return or not row.parent or self.skip\_row(row)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.is\_return → not row.parent → self.skip\_row(row).
    - Continue with the next iteration or loop test.
  - Evaluate source\_invoice\_items.setdefault(tuple(row.parent, row.item\_code), mapping()).setdefault(row.item\_row, row.qty).
- For each tuple(invoice, legacy\_invoice\_items) in self.legacy\_returned\_invoices.items().
  - Set returned\_invoice\_items from self.returned\_invoices.setdefault(invoice, Platform.\_dict()).
  - For each tuple(item\_code, legacy\_item\_rows) in legacy\_invoice\_items.items().
    - Set targets from self.get\_legacy\_return\_targets(source\_invoice\_items.get(tuple(invoice, item\_code), mapping()), returned\_invoice\_items).
    - For each legacy\_item\_row in legacy\_item\_rows.
      - Evaluate self.allocate\_legacy\_return\_item(legacy\_item\_row, targets, returned\_invoice\_items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [skip row](operations-051.md#op-52354173d20ccb), [get legacy return targets](operations-051.md#op-a11f362fa5581d), [allocate legacy return item](operations-051.md#op-cd3f6142b6a400).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L3035) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1010)

<a id="op-a11f362fa5581d"></a>
### Gross Profit Generator.get legacy return targets

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_legacy_return_targets`

**Inputs** self, source\_invoice\_items, returned\_invoice\_items.

**Explicit results** targets.

**Local steps**

- Set targets from list().
- For each tuple(item\_row, qty) in source\_invoice\_items.items().
  - Set linked\_return\_qty from sum(generator of flt(returned\_item.qty) for returned\_item drawn from returned\_invoice\_items.get(item\_row, list())).
    - Draw returned\_item from returned\_invoice\_items.get(item\_row, list()).
  - If available\_qty bound to max((flt(qty) + linked\_return\_qty), 0).
    - Evaluate targets.append(Platform.\_dict(item\_row = item\_row, available\_qty = available\_qty)).
- Evaluate targets.sort(key = deferred anonymous expression).
- Return targets.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L3484) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1023)

<a id="op-cd3f6142b6a400"></a>
### Gross Profit Generator.allocate legacy return item

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_allocate_legacy_return_item`

**Inputs** self, legacy\_item\_row, targets, returned\_invoice\_items.

**Explicit results** no value.

**Local steps**

- Set remaining\_qty from abs(flt(legacy\_item\_row.qty)).
- Set remaining\_base\_amount from flt(legacy\_item\_row.base\_amount).
- If not remaining\_qty.
  - Return no value.
- Set qty\_sign from negative 1 when legacy\_item\_row.qty &lt; 0, otherwise 1.
  - Value choice on legacy\_item\_row.qty &lt; 0 — true gives negative 1, false gives 1.
- For each target in targets.
  - If not target.available\_qty.
    - Continue with the next iteration or loop test.
  - Set allocated\_qty from min(target.available\_qty, remaining\_qty).
  - Set allocated\_item\_row from Platform.\_dict(legacy\_item\_row.copy()).
  - Set allocated\_item\_row.qty from (qty\_sign × allocated\_qty).
  - Set allocated\_item\_row.base\_amount from ((remaining\_base\_amount × allocated\_qty) ÷ remaining\_qty).
  - Evaluate returned\_invoice\_items.setdefault(target.item\_row, list()).append(allocated\_item\_row).
  - Update target.available\_qty using − allocated\_qty.
  - Update remaining\_qty using − allocated\_qty.
  - Update remaining\_base\_amount using − allocated\_item\_row.base\_amount.
  - If not remaining\_qty.
    - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L3845) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1009)

<a id="op-52354173d20ccb"></a>
### Gross Profit Generator.skip row

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_skip_row`

**Inputs** self, row.

**Explicit results** false · not row.get(scrub(group\_by)).

**Local steps**

- Set group\_by from self.filters.get(“group\_by”).
- If group\_by belongs to set(“Invoice”, “Monthly”).
  - Return false.
- Return not row.get(scrub(group\_by)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L4323) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1039)

<a id="op-e1116ea29e9be4"></a>
### Gross Profit Generator.get buying amount from product bundle

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_buying_amount_from_product_bundle`

**Inputs** self, row, product\_bundle.

**Explicit results** flt(buying\_amount, self.currency\_precision).

**Local steps**

- Set buying\_amount from 0.0.
- Set billed\_share from self.get\_billed\_share\_of\_bundle(row).
- For each packed\_item in product\_bundle.
  - If packed\_item.get(“parent\_detail\_docname”) equals row.item\_row.
    - Set packed\_item\_row from row.copy().
    - Set packed\_item\_row.warehouse from packed\_item.warehouse.
    - Set packed\_item\_row.delivered\_warehouse from no value.
    - Set packed\_item\_row.qty from ((packed\_item.total\_qty × negative 1) × billed\_share).
    - Set packed\_item\_row.serial\_and\_batch\_bundle from packed\_item.serial\_and\_batch\_bundle.
    - Update buying\_amount using + self.get\_buying\_amount(packed\_item\_row, packed\_item.item\_code).
- Return flt(buying\_amount, self.currency\_precision).

**Methods declared on this owner** [get billed share of bundle](operations-051.md#op-afe82e452dd6db), [get buying amount](operations-051.md#op-93f11b597462e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1017)

<a id="op-203a8882c0d9c0"></a>
### Gross Profit Generator.get buying amount from delivered bundles

`operation_enterprise_binding_enterprise_accounts_report_gross_profit_gross_profit_grossprofitgenerator_get_buying_amount_from_delivered_bundles`

**Inputs** self, row.

**Explicit results** buying\_amount.

**Local steps**

- Set buying\_amount from 0.0.
- For each tuple(delivered\_row, packed\_items) in self.bundle\_deliveries at row.item\_row.
  - Set delivery from row.copy().
  - Evaluate delivery.update(mapping(“dn\_detail” → delivered\_row.name, “delivery\_note” → delivered\_row.parent, “item\_row” → delivered\_row.name, “qty” → delivered\_row.stock\_qty)).
  - Update buying\_amount using + self.get\_buying\_amount\_from\_product\_bundle(delivery, packed\_items).
- Return buying\_amount.

**Methods declared on this owner** [get buying amount from product bundle](operations-051.md#op-e1116ea29e9be4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L578) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1216)

<a id="op-afe82e452dd6db"></a>
### Gross Profit Generator.get billed share of bundle

`operation_enterprise_binding_enterprise_accounts_report_gross_profit_gross_profit_grossprofitgenerator_get_billed_share_of_bundle`

**Inputs** self, row.

**Record and data access** read “Delivery Note Item” via get\_value.

**Explicit results** 1 · (flt(row.qty) ÷ delivered\_qty) when delivered\_qty, otherwise 1.

**Local steps**

- If not row.dn\_detail.
  - Return 1.
- Set delivered\_qty from flt(Platform.db.get\_value(“Delivery Note Item”, row.dn\_detail, “stock\_qty”)).
- Return (flt(row.qty) ÷ delivered\_qty) when delivered\_qty, otherwise 1.
  - Value choice on delivered\_qty — true gives (flt(row.qty) ÷ delivered\_qty), false gives 1.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L577) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1215)

<a id="op-d924f98c2ed4f9"></a>
### Gross Profit Generator.calculate buying amount from sle

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_calculate_buying_amount_from_stock_ledger_entry`

**Inputs** self, row, my\_sle, parenttype, parent, item\_row, item\_code.

**Explicit results** ((abs((previous\_stock\_value − flt(sle.stock\_value))) × flt(row.qty)) ÷ abs(flt(sle.qty))) · (flt(row.qty) × self.get\_average\_buying\_rate(row, item\_code)) · 0.0.

**Local steps**

- For each tuple(i, sle) in enumerate(my\_sle).
  - If (sle.voucher\_type equals parenttype and parent equals sle.voucher\_no and sle.voucher\_detail\_no equals item\_row).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sle.voucher\_type equals parenttype → parent equals sle.voucher\_no → sle.voucher\_detail\_no equals item\_row.
    - Set previous\_stock\_value from ((len(my\_sle) &gt; (i + 1) and flt(my\_sle at (i + 1).stock\_value)) or 0.0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (len(my\_sle) &gt; (i + 1) and flt(my\_sle at (i + 1).stock\_value)) → 0.0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(my\_sle) &gt; (i + 1) → flt(my\_sle at (i + 1).stock\_value).
    - If previous\_stock\_value.
      - Return ((abs((previous\_stock\_value − flt(sle.stock\_value))) × flt(row.qty)) ÷ abs(flt(sle.qty))).
    - Otherwise.
      - Return (flt(row.qty) × self.get\_average\_buying\_rate(row, item\_code)).
- Return 0.0.

**Methods declared on this owner** [get average buying rate](operations-052.md#op-c33a86156cf4e3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0257.json#L4765) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L668) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1012)

<a id="op-93f11b597462e7"></a>
### Gross Profit Generator.get buying amount

`operation_enterprise_accounts_report_gross_profit_business_behavior_gross_profit_generator_get_buying_amount`

**Inputs** self, row, item\_code.

**Explicit results** buying\_amount · (flt(row.qty) × item\_rate) · self.calculate\_buying\_amount\_from\_sle(row, my\_sle, parenttype, parent, …) · ((flt(row.qty) × flt(dn.total\_incoming\_value)) ÷ flt(dn.total\_qty)) · (flt(row.qty) × self.get\_average\_buying\_rate(row, item\_code)) · 1 additional forms in the steps below.

**Local steps**

- If row.delivered\_by\_supplier.
  - Set buying\_amount from self.get\_drop\_ship\_buying\_amount(row).
  - If buying\_amount is distinct from no value.
    - Return buying\_amount.
- If (item\_code belongs to self.non\_stock\_items and (row.project or row.cost\_center)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item\_code belongs to self.non\_stock\_items → (row.project or row.cost\_center).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.project → row.cost\_center.
  - Set item\_rate from self.get\_last\_purchase\_rate(item\_code, row).
  - Return (flt(row.qty) × item\_rate).
- Otherwise.
  - Set my\_sle from self.get\_stock\_ledger\_entries(item\_code, (row.delivered\_warehouse or row.warehouse)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.delivered\_warehouse → row.warehouse.
  - If ((row.update\_stock or row.dn\_detail) and my\_sle).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (row.update\_stock or row.dn\_detail) → my\_sle.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.update\_stock → row.dn\_detail.
    - Set parenttype from row.parenttype.
    - Set parent from (row.invoice or row.parent).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.invoice → row.parent.
    - If row.dn\_detail.
      - Set tuple(parenttype, parent) from tuple(“Delivery Note”, row.delivery\_note).
    - Return self.calculate\_buying\_amount\_from\_sle(row, my\_sle, parenttype, parent, …).
  - Otherwise.
    - If (row.item\_row and self.delivery\_notes.get(row.item\_row)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.item\_row → self.delivery\_notes.get(row.item\_row).
      - Set dn from self.delivery\_notes at row.item\_row.
      - If flt(dn.total\_qty).
        - Return ((flt(row.qty) × flt(dn.total\_incoming\_value)) ÷ flt(dn.total\_qty)).
      - Return (flt(row.qty) × self.get\_average\_buying\_rate(row, item\_code)).
    - Otherwise.
      - If (row.sales\_order and row.so\_detail).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.sales\_order → row.so\_detail.
        - Set incoming\_amount from self.get\_buying\_amount\_from\_so\_dn(row.sales\_order, row.so\_detail, item\_code).
        - If incoming\_amount.
          - Return (flt(row.qty) × incoming\_amount).
      - Otherwise.
        - Return (flt(row.qty) × self.get\_average\_buying\_rate(row, item\_code)).
- Return (flt(row.qty) × self.get\_average\_buying\_rate(row, item\_code)).

**Methods declared on this owner** [get drop ship buying amount](operations-052.md#op-411d8554a99e64), [get last purchase rate](operations-052.md#op-5b7d7a9260b173), [get stock ledger entries](operations-052.md#op-2f2ee4eee17c34), [calculate buying amount from sle](operations-051.md#op-d924f98c2ed4f9), [get average buying rate](operations-052.md#op-c33a86156cf4e3), [get buying amount from so dn](operations-052.md#op-79d6b5de94103f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1016)
