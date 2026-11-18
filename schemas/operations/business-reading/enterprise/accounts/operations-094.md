# Accounting and settlement · operations 94

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase invoice

[Record definition](../../../../data/record-types/purchase_invoice.json)

<a id="op-1c0e107858bb1d"></a>
### Purchase Invoice.get gl entries

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_get_general_ledger_entries`

**Inputs** self, inventory\_account\_map = no value.

**Explicit results** gl\_entries.

**Local steps**

- Set self.auto\_accounting\_for\_stock from Enterprise.is\_perpetual\_inventory\_enabled(self.company).
- If self.auto\_accounting\_for\_stock.
  - Set self.stock\_received\_but\_not\_billed from self.get\_company\_default(“stock\_received\_but\_not\_billed”).
- Otherwise.
  - Set self.stock\_received\_but\_not\_billed from no value.
- Set self.negative\_expense\_to\_be\_booked from 0.0.
- Set gl\_entries from list().
- Evaluate self.make\_supplier\_gl\_entry(gl\_entries).
- Evaluate self.make\_item\_gl\_entries(gl\_entries).
- Evaluate self.make\_precision\_loss\_gl\_entry(gl\_entries).
- Evaluate self.make\_tax\_gl\_entries(gl\_entries).
- Evaluate self.make\_internal\_transfer\_gl\_entries(gl\_entries).
- Evaluate self.make\_gl\_entries\_for\_tax\_withholding(gl\_entries).
- Set gl\_entries from make\_regional\_gl\_entries(gl\_entries, self).
- Set gl\_entries from merge\_similar\_entries(gl\_entries).
- Evaluate self.make\_payment\_gl\_entries(gl\_entries).
- Evaluate self.make\_write\_off\_gl\_entry(gl\_entries).
- Evaluate self.make\_gle\_for\_rounding\_adjustment(gl\_entries).
- Evaluate self.set\_transaction\_currency\_and\_rate\_in\_gl\_map(gl\_entries).
- Evaluate self.set\_gl\_entry\_for\_purchase\_expense(gl\_entries).
- Return gl\_entries.

**Methods declared on this owner** [make supplier gl entry](operations-094.md#op-57456b82571fd2), [make item gl entries](operations-094.md#op-b0349abc7b8d6b), [make tax gl entries](operations-094.md#op-eee3a2e8a18950), [make internal transfer gl entries](operations-094.md#op-ed79fe24cbfa10), [make gl entries for tax withholding](operations-094.md#op-44726e7d969c27), [make payment gl entries](operations-094.md#op-9a260cabd7cb3e), [make write off gl entry](operations-094.md#op-d260a3673cf47f), [make gle for rounding adjustment](operations-094.md#op-9d1a37c6eb576b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L751) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L923)

<a id="op-00cd13edc84398"></a>
### Purchase Invoice.check asset cwip enabled

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_check_asset_cwip_enabled`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit results** 1 · 0.

**Local steps**

- For each item in self.get(“items”).
  - If (item.item\_code and item.is\_fixed\_asset).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.item\_code → item.is\_fixed\_asset.
    - Set asset\_category from Platform.get\_cached\_value(“Item”, item.item\_code, “asset\_category”).
    - If is\_cwip\_accounting\_enabled(asset\_category).
      - Return 1.
- Return 0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, item.item\_code, “asset\_category”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L2921) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L919)

<a id="op-57456b82571fd2"></a>
### Purchase Invoice.make supplier gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_supplier_gl_entry`

**Inputs** self, gl\_entries.

**Local steps**

- Set grand\_total from self.rounded\_total when (self.rounding\_adjustment and self.rounded\_total), otherwise self.grand\_total.
  - Value choice on (self.rounding\_adjustment and self.rounded\_total) — true gives self.rounded\_total, false gives self.grand\_total.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.rounding\_adjustment → self.rounded\_total.
- Set base\_grand\_total from flt(self.base\_rounded\_total when (self.base\_rounding\_adjustment and self.base\_rounded\_total), otherwise self.base\_grand\_total, self.precision(“base\_grand\_total”)).
  - Value choice on (self.base\_rounding\_adjustment and self.base\_rounded\_total) — true gives self.base\_rounded\_total, false gives self.base\_grand\_total.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.base\_rounding\_adjustment → self.base\_rounded\_total.
- If (grand\_total and not self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in grand\_total → not self.is\_internal\_transfer().
  - Evaluate self.add\_supplier\_gl\_entry(gl\_entries, base\_grand\_total, grand\_total).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add supplier gl entry](operations-094.md#op-16b8c32a77e556).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L324) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L962)

<a id="op-16b8c32a77e556"></a>
### Purchase Invoice.add supplier gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_add_supplier_gl_entry`

**Inputs** self, gl\_entries, base\_grand\_total, grand\_total, against\_account = no value, remarks = no value, skip\_merge = false.

**Local steps**

- Set against\_voucher from self.name.
- If (self.is\_return and self.return\_against and not self.update\_outstanding\_for\_self).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → not self.update\_outstanding\_for\_self.
  - Set against\_voucher from self.return\_against.
- Set gl from mapping(“account” → self.credit\_to, “party\_type” → “Supplier”, “party” → self.supplier, “due\_date” → self.due\_date, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in against\_account → self.against\_expense\_account.
  - Value choice on self.party\_account\_currency equals self.company\_currency — true gives base\_grand\_total, false gives grand\_total.
- If remarks.
  - Set gl at “remarks” from remarks.
- Evaluate gl\_entries.append(self.get\_gl\_dict(gl, self.party\_account\_currency, item = self)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L948)

<a id="op-b0349abc7b8d6b"></a>
### Purchase Invoice.make item gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_item_gl_entries`

**Inputs** self, gl\_entries.

**Record and data access** read “Stock Ledger Entry” via get\_all · read “Company” via get\_cached\_value · read “Buying Settings” via get\_single\_value · read “Item” via get\_cached\_value · execute query text (SELECT, GL Entry).

**Explicit failure paths** validation helper — translated “Please set account in Warehouse {0}”.format(self.supplier\_warehouse).

**Local steps**

- Bind dependencies get\_custom\_dimension\_overrides.
- Set stock\_items from self.get\_stock\_items().
- If (self.update\_stock and self.auto\_accounting\_for\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.update\_stock → self.auto\_accounting\_for\_stock.
  - Set inventory\_account\_map from self.get\_inventory\_account\_map().
- Set landed\_cost\_entries from self.get\_item\_account\_wise\_lcv\_entries().
- Set voucher\_wise\_stock\_value from mapping().
- If self.update\_stock.
  - Set stock\_ledger\_entries from Platform.get\_all(“Stock Ledger Entry”, fields = list(“voucher\_detail\_no”, “stock\_value\_difference”, “warehouse”), filters = mapping(“voucher\_no” → self.name, “voucher\_type” → self.doctype, “is\_cancelled” → 0)).
  - For each d in stock\_ledger\_entries.
    - Evaluate voucher\_wise\_stock\_value.setdefault(tuple(d.voucher\_detail\_no, d.warehouse), d.stock\_value\_difference).
- Set valuation\_tax\_accounts from list of d.account\_head for d drawn from self.get(“taxes”) where (d.category belongs to tuple(“Valuation”, “Valuation and Total”) and flt(d.base\_tax\_amount\_after\_discount\_amount)).
  - Draw d from self.get(“taxes”), keep a combination only if ((d.category belongs to tuple(“Valuation”, “Valuation and Total”) and flt(d.base\_tax\_amount\_after\_discount\_amount))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.category belongs to tuple(“Valuation”, “Valuation and Total”) → flt(d.base\_tax\_amount\_after\_discount\_amount).
- Set tuple(exchange\_rate\_map, net\_rate\_map) from get\_purchase\_document\_details(self).
- Set provisional\_accounting\_for\_non\_stock\_items from cint(Platform.get\_cached\_value(“Company”, self.company, “enable\_provisional\_accounting\_for\_non\_stock\_items”)).
- If provisional\_accounting\_for\_non\_stock\_items.
  - Evaluate self.get\_provisional\_accounts().
- Set adjust\_incoming\_rate from Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).
- For each item in self.get(“items”).
  - If (flt(item.base\_net\_amount) or (self.get(“update\_stock”) and (item.valuation\_rate or voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse))))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.base\_net\_amount) → (self.get(“update\_stock”) and (item.valuation\_rate or voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“update\_stock”) → (item.valuation\_rate or voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.valuation\_rate → voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse)).
    - If item.item\_code.
      - Evaluate Platform.get\_cached\_value(“Item”, item.item\_code, “asset\_category”).
    - If (self.update\_stock and self.auto\_accounting\_for\_stock and (item.item\_code belongs to stock\_items or item.is\_fixed\_asset)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.update\_stock → self.auto\_accounting\_for\_stock → (item.item\_code belongs to stock\_items or item.is\_fixed\_asset).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.item\_code belongs to stock\_items → item.is\_fixed\_asset.
      - Set account\_currency from get\_account\_currency(item.expense\_account).
      - Set warehouse\_debit\_amount from self.make\_stock\_adjustment\_entry(gl\_entries, item, voucher\_wise\_stock\_value, account\_currency).
      - If item.from\_warehouse.
        - Set \_inv\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map).
        - Set \_inv\_dict\_from\_warehouse from self.get\_inventory\_account\_dict(item, inventory\_account\_map, “from\_warehouse”).
        - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → \_inv\_dict at “account”, “against” → \_inv\_dict\_from\_warehouse at “account”, “cost\_center” → item.cost\_center, “project” → (item.project or self.project ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
        - Set rejected\_amount from self.make\_rejected\_warehouse\_gl\_entry(gl\_entries, item, voucher\_wise\_stock\_value, inventory\_account\_map).
        - Set credit\_amount from self.get\_transit\_stock\_value(item, voucher\_wise\_stock\_value).
        - If credit\_amount is identical to no value.
          - Set credit\_amount from item.base\_net\_amount.
          - If (self.is\_internal\_supplier and item.valuation\_rate).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_supplier → item.valuation\_rate.
            - Set credit\_amount from flt((item.valuation\_rate × item.stock\_qty)).
          - Update credit\_amount using + rejected\_amount.
        - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → \_inv\_dict\_from\_warehouse at “account”, “against” → \_inv\_dict at “account”, “cost\_center” → item.cost\_center, “project” → (item.project or self.project ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
        - If not self.is\_internal\_transfer().
          - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → item.expense\_account, “against” → self.supplier, “debit” → flt(item.base\_net\_amount, item.precision(“base\_net\_amount”)), “debit\_in\_transaction\_currenc ….
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
      - Otherwise.
        - Evaluate self.make\_rejected\_warehouse\_gl\_entry(gl\_entries, item, voucher\_wise\_stock\_value, inventory\_account\_map).
        - If not self.is\_internal\_transfer().
          - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → item.expense\_account, “against” → self.supplier, “debit” → warehouse\_debit\_amount, “debit\_in\_transaction\_currency” → flt((warehouse\_debit\_amount ÷ sel ….
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
      - If landed\_cost\_entries.
        - For each entry in landed\_cost\_entries.get(tuple(item.item\_code, item.name), list()).
          - If not (entry.amount or entry.base\_amount).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.amount → entry.base\_amount.
            - Continue with the next iteration or loop test.
          - Set lcv\_account\_currency from get\_account\_currency(entry.expense\_account).
          - Set credit\_in\_transaction\_currency from flt(entry.amount) when lcv\_account\_currency equals self.currency, otherwise flt((entry.base\_amount ÷ self.conversion\_rate), item.precision(“net\_amount”)).
            - Value choice on lcv\_account\_currency equals self.currency — true gives flt(entry.amount), false gives flt((entry.base\_amount ÷ self.conversion\_rate), item.precision(“net\_amount”)).
          - Set gl\_dict from self.get\_gl\_dict(mapping(“account” → entry.expense\_account, “against” → item.expense\_account, “cost\_center” → (entry.dimensions.cost\_center or item.cost\_center), “remarks” → (self.get(“remarks”) or transla ….
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.cost\_center → item.cost\_center.
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.dimensions.project → item.project → self.project.
          - Evaluate gl\_dict.update(get\_custom\_dimension\_overrides(entry)).
          - Evaluate gl\_entries.append(gl\_dict).
      - If flt(item.rm\_supp\_cost).
        - Set supplier\_wh\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map, “supplier\_warehouse”).
        - Set supplier\_inventory\_account from supplier\_wh\_dict at “account”.
        - If not supplier\_inventory\_account.
          - Call the validation error handler Platform.throw(translated “Please set account in Warehouse {0}”.format(self.supplier\_warehouse)).
        - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → supplier\_inventory\_account, “against” → item.expense\_account, “cost\_center” → item.cost\_center, “project” → (item.project or self.project), …), suppli ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
    - Otherwise.
      - Set expense\_account from item.expense\_account when (not item.enable\_deferred\_expense or self.is\_return), otherwise item.deferred\_expense\_account.
        - Value choice on (not item.enable\_deferred\_expense or self.is\_return) — true gives item.expense\_account, false gives item.deferred\_expense\_account.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.enable\_deferred\_expense → self.is\_return.
      - Set account\_currency from get\_account\_currency(expense\_account).
      - Set tuple(amount, base\_amount) from self.get\_amount\_and\_base\_amount(item, no value).
      - If provisional\_accounting\_for\_non\_stock\_items.
        - Evaluate self.make\_provisional\_gl\_entry(gl\_entries, item).
      - If not self.is\_internal\_transfer().
        - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → expense\_account, “against” → self.supplier, “debit” → base\_amount, “debit\_in\_transaction\_currency” → amount, …), account\_currency, item = item)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
        - If (not adjust\_incoming\_rate and item.get(“purchase\_receipt”) and self.auto\_accounting\_for\_stock).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in not adjust\_incoming\_rate → item.get(“purchase\_receipt”) → self.auto\_accounting\_for\_stock.
          - If (exchange\_rate\_map at item.purchase\_receipt and self.conversion\_rate differs from exchange\_rate\_map at item.purchase\_receipt and item.net\_rate equals net\_rate\_map at item.pr\_detail and item.item\_code belon ….
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in exchange\_rate\_map at item.purchase\_receipt → self.conversion\_rate differs from exchange\_rate\_map at item.purchase\_receipt → item.net\_rate equals net\_rate\_map at item.pr\_detail → item.item\_code belongs to stock\_items.
            - Set discrepancy\_caused\_by\_exchange\_rate\_difference from ((item.qty × item.net\_rate) × (exchange\_rate\_map at item.purchase\_receipt − self.conversion\_rate)).
            - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → expense\_account, “against” → self.supplier, “debit” → discrepancy\_caused\_by\_exchange\_rate\_difference, “cost\_center” → item.cost\_center, …), account\_cu ….
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
            - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.get\_company\_default(“exchange\_gain\_loss\_account”), “against” → self.supplier, “credit” → discrepancy\_caused\_by\_exchange\_rate\_difference, “cost\_ce ….
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
  - If (self.auto\_accounting\_for\_stock and self.is\_opening equals “No” and item.item\_code belongs to stock\_items and item.item\_tax\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.auto\_accounting\_for\_stock → self.is\_opening equals “No” → item.item\_code belongs to stock\_items → item.item\_tax\_amount.
    - If (item.purchase\_receipt and valuation\_tax\_accounts).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.purchase\_receipt → valuation\_tax\_accounts.
      - Set negative\_expense\_booked\_in\_pr from Platform.db.sql(query text (SELECT, GL Entry), tuple(item.purchase\_receipt, valuation\_tax\_accounts)).
      - Evaluate self.get\_company\_default(“asset\_received\_but\_not\_billed”) when item.is\_fixed\_asset, otherwise self.stock\_received\_but\_not\_billed.
        - Value choice on item.is\_fixed\_asset — true gives self.get\_company\_default(“asset\_received\_but\_not\_billed”), false gives self.stock\_received\_but\_not\_billed.
      - If not negative\_expense\_booked\_in\_pr.
        - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.stock\_received\_but\_not\_billed, “against” → self.supplier, “debit” → flt(item.item\_tax\_amount, item.precision(“item\_tax\_amount”)), “debit\_in\_trans ….
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.remarks → translated “Accounting Entry for Stock”.
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
        - Update self.negative\_expense\_to\_be\_booked using + flt(item.item\_tax\_amount, item.precision(“item\_tax\_amount”)).
  - If (item.is\_fixed\_asset and item.landed\_cost\_voucher\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_fixed\_asset → item.landed\_cost\_voucher\_amount.
    - Evaluate self.update\_net\_purchase\_amount\_for\_linked\_assets(item).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get provisional accounts](operations-094.md#op-4aac733813f667), [make stock adjustment entry](operations-094.md#op-7b75956a915bc9), [make rejected warehouse gl entry](operations-094.md#op-32d46763e10853), [get transit stock value](operations-094.md#op-c4ad594148d71e), [make provisional gl entry](operations-094.md#op-502fbc2580e38f), [update net purchase amount for linked assets](operations-094.md#op-a930181cedd8a4).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “enable\_provisional\_accounting\_for\_non\_stock\_items”), Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L319) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L957)

<a id="op-4aac733813f667"></a>
### Purchase Invoice.get provisional accounts

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_get_provisional_accounts`

**Inputs** self.

**Record and data access** read “Purchase Receipt Item” via get\_all · read “GL Entry” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies get\_order\_billing\_provisional\_reversals.
- Set self.provisional\_accounts from Platform.\_dict().
- Set self.order\_provisional\_reversals from get\_order\_billing\_provisional\_reversals(self).
- Set linked\_purchase\_receipts from set(list of d.purchase\_receipt for d drawn from self.items where d.purchase\_receipt).
  - Draw d from self.items, keep a combination only if (d.purchase\_receipt).
- If not linked\_purchase\_receipts.
  - Return no value.
- Set pr\_items from Platform.get\_all(“Purchase Receipt Item”, filters = mapping(“parent” → tuple(“in”, linked\_purchase\_receipts)), fields = list(“name”, “provisional\_expense\_account”, “qty”, “base\_rate”, …)).
- Set default\_provisional\_account from self.get\_company\_default(“default\_provisional\_account”).
- Set provisional\_accounts from set(list of d.provisional\_expense\_account when d.provisional\_expense\_account, otherwise default\_provisional\_account for d drawn from pr\_items).
  - Draw d from pr\_items.
  - Value choice on d.provisional\_expense\_account — true gives d.provisional\_expense\_account, false gives default\_provisional\_account.
- Set provisional\_gl\_entries from Platform.get\_all(“GL Entry”, filters = mapping(“voucher\_type” → “Purchase Receipt”, “voucher\_no” → tuple(“in”, linked\_purchase\_receipts), “account” → tuple(“in”, provisional\_accounts), “is\_cancelled” → 0), ….
- Set rows\_with\_provisional\_entries from list of d.voucher\_detail\_no for d drawn from provisional\_gl\_entries.
  - Draw d from provisional\_gl\_entries.
- For each item in pr\_items.
  - Set self.provisional\_accounts at item.name from mapping(“provisional\_account” → (item.provisional\_expense\_account or default\_provisional\_account), “qty” → item.qty, “base\_rate” → item.base\_rate, “rate” → item.rate, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.provisional\_expense\_account → default\_provisional\_account.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L42) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L951)

<a id="op-502fbc2580e38f"></a>
### Purchase Invoice.make provisional gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_provisional_gl_entry`

**Inputs** self, gl\_entries, item.

**Record and data access** read “Purchase Receipt” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Bind dependencies post\_provisional\_gl\_entry.
- If item.purchase\_receipt.
  - Set pr\_item from self.provisional\_accounts.get(item.pr\_detail, mapping()).
  - If pr\_item.get(“has\_provisional\_entry”).
    - Set conversion\_rate from Platform.get\_cached\_value(“Purchase Receipt”, item.purchase\_receipt, “conversion\_rate”).
    - Evaluate post\_provisional\_gl\_entry(self, item, gl\_entries, self.posting\_date, reverse = 1, item\_amount = ((min(item.qty, pr\_item.get(“qty”)) × pr\_item.get(“rate”)) × conversion\_rate), …).
  - Return no value.
- For each tuple(row, qty) in self.order\_provisional\_reversals.get(item.name, list()).
  - Evaluate post\_provisional\_gl\_entry(self, item, gl\_entries, self.posting\_date, reverse = 1, item\_amount = ((qty × flt(row.rate)) × flt(row.conversion\_rate)), pr\_detail = row.name, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Purchase Receipt”, item.purchase\_receipt, “conversion\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L321) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L959)

<a id="op-a930181cedd8a4"></a>
### Purchase Invoice.update net purchase amount for linked assets

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_update_net_purchase_amount_for_linked_assets`

**Inputs** self, item.

**Record and data access** read “Asset” via get\_all.

**State and service calls** request set\_value on “Asset”.

**Local steps**

- Set assets from Platform.db.get\_all(“Asset”, filters = mapping(“purchase\_invoice” → self.name, “item\_code” → item.item\_code, “purchase\_invoice\_item” → tuple(“in”, list(item.name, empty text))), fields = list(“name”, “asse ….
- For each asset in assets.
  - Set purchase\_amount from ((flt(item.valuation\_rate) × flt((item.conversion\_factor or 1))) × asset.asset\_quantity).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
  - Evaluate Platform.db.set\_value(“Asset”, asset.name, mapping(“net\_purchase\_amount” → purchase\_amount, “purchase\_amount” → purchase\_amount)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L967)

<a id="op-32d46763e10853"></a>
### Purchase Invoice.make rejected warehouse gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_rejected_warehouse_gl_entry`

**Inputs** self, gl\_entries, item, voucher\_wise\_stock\_value, inventory\_account\_map.

**Declared result** float.

**Explicit results** 0.0 · rejected\_amount when transfers\_rejected\_material, otherwise 0.0.

**Local steps**

- If not (item.rejected\_warehouse and flt(item.rejected\_qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.rejected\_warehouse → flt(item.rejected\_qty).
  - Return 0.0.
- Set transfers\_rejected\_material from self.is\_internal\_transfer().
- Set rejected\_amount from flt(voucher\_wise\_stock\_value.get(tuple(item.name, item.rejected\_warehouse)), item.precision(“base\_net\_amount”)).
- If not rejected\_amount.
  - Return 0.0.
- Set rejected\_account from self.get\_inventory\_account\_dict(item, inventory\_account\_map, “rejected\_warehouse”).
- Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → rejected\_account at “account”, “against” → item.expense\_account when transfers\_rejected\_material, otherwise self.supplier, “cost\_center” → item.cost\_c ….
  - Value choice on transfers\_rejected\_material — true gives item.expense\_account, false gives self.supplier.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Accounting Entry for Stock”.
- Return rejected\_amount when transfers\_rejected\_material, otherwise 0.0.
  - Value choice on transfers\_rejected\_material — true gives rejected\_amount, false gives 0.0.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L322) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L960)

<a id="op-c4ad594148d71e"></a>
### Purchase Invoice.get transit stock value

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_get_transit_stock_value`

**Inputs** self, item, voucher\_wise\_stock\_value.

**Declared result** (float bitwise or no value).

**Explicit results** no value · no value when stock\_value is identical to no value, otherwise negative flt(stock\_value).

**Local steps**

- If not (item.from\_warehouse and self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.from\_warehouse → self.is\_internal\_transfer().
  - Return no value.
- If item.rejected\_warehouse equals item.from\_warehouse.
  - Return no value.
- Set stock\_value from voucher\_wise\_stock\_value.get(tuple(item.name, item.from\_warehouse)).
- Return no value when stock\_value is identical to no value, otherwise negative flt(stock\_value).
  - Value choice on stock\_value is identical to no value — true gives no value, false gives negative flt(stock\_value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L44) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L315) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L953)

<a id="op-7b75956a915bc9"></a>
### Purchase Invoice.make stock adjustment entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_stock_adjustment_entry`

**Inputs** self, gl\_entries, item, voucher\_wise\_stock\_value, account\_currency.

**Explicit results** warehouse\_debit\_amount.

**Local steps**

- Set net\_amt\_precision from item.precision(“base\_net\_amount”).
- Set warehouse\_debit\_amount from flt((flt(item.valuation\_rate) × get\_stock\_qty(item, item.qty)), net\_amt\_precision).
- Set transit\_stock\_value from self.get\_transit\_stock\_value(item, voucher\_wise\_stock\_value).
- If transit\_stock\_value is distinct from no value.
  - Set rejected\_stock\_value from voucher\_wise\_stock\_value.get(tuple(item.name, item.rejected\_warehouse)).
  - Set warehouse\_debit\_amount from flt(((flt(transit\_stock\_value, net\_amt\_precision) − flt(rejected\_stock\_value, net\_amt\_precision)) + flt(item.landed\_cost\_voucher\_amount)), net\_amt\_precision).
- If (transit\_stock\_value is identical to no value and self.is\_return and self.update\_stock and (self.is\_internal\_supplier or not self.return\_against)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in transit\_stock\_value is identical to no value → self.is\_return → self.update\_stock → (self.is\_internal\_supplier or not self.return\_against).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_internal\_supplier → not self.return\_against.
  - Set net\_rate from item.base\_net\_amount.
  - If item.sales\_incoming\_rate.
    - Set net\_rate from (get\_transit\_amount(item, item.qty) + get\_transit\_amount(item, item.rejected\_qty)).
  - Set stock\_amount from ((net\_rate + item.item\_tax\_amount) + flt(item.landed\_cost\_voucher\_amount)).
  - Set warehouse\_debit\_amount from flt(voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse)), net\_amt\_precision).
  - Set returned\_stock\_value from (warehouse\_debit\_amount + flt(voucher\_wise\_stock\_value.get(tuple(item.name, item.rejected\_warehouse)), net\_amt\_precision)).
  - If flt(stock\_amount, net\_amt\_precision) differs from flt(returned\_stock\_value, net\_amt\_precision).
    - Set stock\_asset\_rbnb from self.get\_company\_default(“asset\_received\_but\_not\_billed”, ignore\_validation = true) when item.is\_fixed\_asset, otherwise self.get\_company\_default(“stock\_received\_but\_not\_billed”, ignore\_validation = true).
      - Value choice on item.is\_fixed\_asset — true gives self.get\_company\_default(“asset\_received\_but\_not\_billed”, ignore\_validation = true), false gives self.get\_company\_default(“stock\_received\_but\_not\_billed”, ignore\_validation = true).
    - Set fallback\_account from (item.expense\_account or stock\_asset\_rbnb) when self.is\_return, otherwise (stock\_asset\_rbnb or item.expense\_account).
      - Value choice on self.is\_return — true gives (item.expense\_account or stock\_asset\_rbnb), false gives (stock\_asset\_rbnb or item.expense\_account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.expense\_account → stock\_asset\_rbnb.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in stock\_asset\_rbnb → item.expense\_account.
    - Set cost\_of\_goods\_sold\_account from (self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true) or fallback\_account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true) → fallback\_account.
    - Set stock\_adjustment\_amt from (stock\_amount − returned\_stock\_value).
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → cost\_of\_goods\_sold\_account, “against” → item.expense\_account, “debit” → stock\_adjustment\_amt, “debit\_in\_transaction\_currency” → (stock\_adjustment\_amt  ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Stock Adjustment”.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
- Otherwise.
  - If (self.update\_stock and (transit\_stock\_value is distinct from no value or voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse))) and warehouse\_debit\_amount differs from flt(voucher\_wise\_stock\_value ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.update\_stock → (transit\_stock\_value is distinct from no value or voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse))) → warehouse\_debit\_amount differs from flt(voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse)), net\_amt\_precision).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transit\_stock\_value is distinct from no value → voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse)).
    - Set stock\_asset\_rbnb from self.get\_company\_default(“asset\_received\_but\_not\_billed”, ignore\_validation = true) when item.is\_fixed\_asset, otherwise self.get\_company\_default(“stock\_received\_but\_not\_billed”, ignore\_validation = true).
      - Value choice on item.is\_fixed\_asset — true gives self.get\_company\_default(“asset\_received\_but\_not\_billed”, ignore\_validation = true), false gives self.get\_company\_default(“stock\_received\_but\_not\_billed”, ignore\_validation = true).
    - Set fallback\_account from (item.expense\_account or stock\_asset\_rbnb) when self.is\_return, otherwise (stock\_asset\_rbnb or item.expense\_account).
      - Value choice on self.is\_return — true gives (item.expense\_account or stock\_asset\_rbnb), false gives (stock\_asset\_rbnb or item.expense\_account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.expense\_account → stock\_asset\_rbnb.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in stock\_asset\_rbnb → item.expense\_account.
    - Set cost\_of\_goods\_sold\_account from (self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true) or fallback\_account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_company\_default(“default\_expense\_account”, ignore\_validation = true) → fallback\_account.
    - Set stock\_amount from flt(voucher\_wise\_stock\_value.get(tuple(item.name, item.warehouse)), net\_amt\_precision).
    - Set stock\_adjustment\_amt from (warehouse\_debit\_amount − stock\_amount).
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → cost\_of\_goods\_sold\_account, “against” → item.expense\_account, “debit” → stock\_adjustment\_amt, “debit\_in\_transaction\_currency” → (stock\_adjustment\_amt  ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → translated “Stock Adjustment”.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.project → self.project.
    - Set warehouse\_debit\_amount from stock\_amount.
- Return warehouse\_debit\_amount.

**Methods declared on this owner** [get transit stock value](operations-094.md#op-c4ad594148d71e).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L323) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L961)

<a id="op-eee3a2e8a18950"></a>
### Purchase Invoice.make tax gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_tax_gl_entries`

**Inputs** self, gl\_entries.

**Explicit failure paths** validation helper — translated “Cost Center is required in row {0} in Taxes table for type {1}”.format(tax.idx, translated tax.category).

**Local steps**

- Set valuation\_tax from mapping().
- Set capitalized\_valuation\_tax from self.get\_capitalized\_valuation\_tax().
- For each tax in self.get(“taxes”).
  - Set tuple(amount, base\_amount) from self.get\_tax\_amounts(tax, no value).
  - If (tax.category belongs to tuple(“Total”, “Valuation and Total”) and flt(base\_amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.category belongs to tuple(“Total”, “Valuation and Total”) → flt(base\_amount).
    - Set account\_currency from get\_account\_currency(tax.account\_head).
    - Set dr\_or\_cr from “debit” when tax.add\_deduct\_tax equals “Add”, otherwise “credit”.
      - Value choice on tax.add\_deduct\_tax equals “Add” — true gives “debit”, false gives “credit”.
    - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → tax.account\_head, “against” → self.supplier, dr\_or\_cr → base\_amount, (dr\_or\_cr + “\_in\_account\_currency”) → base\_amount when account\_currency equals se ….
      - Value choice on account\_currency equals self.company\_currency — true gives base\_amount, false gives amount.
  - If (self.is\_opening equals “No” and tax.category belongs to tuple(“Valuation”, “Valuation and Total”) and flt(base\_amount) and not self.is\_internal\_transfer()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_opening equals “No” → tax.category belongs to tuple(“Valuation”, “Valuation and Total”) → flt(base\_amount) → not self.is\_internal\_transfer().
    - If (self.auto\_accounting\_for\_stock and not tax.cost\_center).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.auto\_accounting\_for\_stock → not tax.cost\_center.
      - Call the validation error handler Platform.throw(translated “Cost Center is required in row {0} in Taxes table for type {1}”.format(tax.idx, translated tax.category)).
    - Set valuation\_tax at tax.name from capitalized\_valuation\_tax.get(tax.name, 0.0).
- If (self.is\_opening equals “No” and self.negative\_expense\_to\_be\_booked and valuation\_tax).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_opening equals “No” → self.negative\_expense\_to\_be\_booked → valuation\_tax.
  - Set total\_valuation\_amount from sum(valuation\_tax.values()).
  - Set amount\_including\_divisional\_loss from self.negative\_expense\_to\_be\_booked.
  - Set i from 1.
  - For each tax in self.get(“taxes”).
    - If valuation\_tax.get(tax.name).
      - If i equals len(valuation\_tax).
        - Set applicable\_amount from amount\_including\_divisional\_loss.
      - Otherwise.
        - Set applicable\_amount from (self.negative\_expense\_to\_be\_booked × (valuation\_tax at tax.name ÷ total\_valuation\_amount)).
        - Update amount\_including\_divisional\_loss using − applicable\_amount.
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → tax.account\_head, “cost\_center” → tax.cost\_center, “against” → self.supplier, “credit” → applicable\_amount, …), item = tax)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.remarks → translated “Accounting Entry for Stock”.
      - Update i using + 1.
- If (self.auto\_accounting\_for\_stock and self.update\_stock and valuation\_tax).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.auto\_accounting\_for\_stock → self.update\_stock → valuation\_tax.
  - For each tax in self.get(“taxes”).
    - If valuation\_tax.get(tax.name).
      - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → tax.account\_head, “cost\_center” → tax.cost\_center, “against” → self.supplier, “credit” → valuation\_tax at tax.name, …), item = tax)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.remarks → translated “Accounting Entry for Stock”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L325) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L963)

<a id="op-ed79fe24cbfa10"></a>
### Purchase Invoice.make internal transfer gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_internal_transfer_gl_entries`

**Inputs** self, gl\_entries.

**Local steps**

- If (self.is\_internal\_transfer() and flt(self.base\_total\_taxes\_and\_charges)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → flt(self.base\_total\_taxes\_and\_charges).
  - Set account\_currency from get\_account\_currency(self.unrealized\_profit\_loss\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.unrealized\_profit\_loss\_account, “against” → self.supplier, “credit” → flt(self.total\_taxes\_and\_charges), “credit\_in\_transaction\_currency” → flt(s ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L318) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L956)

<a id="op-44726e7d969c27"></a>
### Purchase Invoice.make gl entries for tax withholding

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_gl_entries_for_tax_withholding`

**Inputs** self, gl\_entries.

**Explicit results** no value.

**Local steps**

- If not self.apply\_tds.
  - Return no value.
- For each row in self.get(“taxes”).
  - If (not row.is\_tax\_withholding\_account or not row.tax\_amount).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not row.is\_tax\_withholding\_account → not row.tax\_amount.
    - Continue with the next iteration or loop test.
  - Set base\_tds\_amount from row.base\_tax\_amount\_after\_discount\_amount.
  - Set tds\_amount from row.tax\_amount\_after\_discount\_amount.
  - Evaluate self.add\_supplier\_gl\_entry(gl\_entries, base\_tds\_amount, tds\_amount).
  - Evaluate self.add\_supplier\_gl\_entry(gl\_entries, negative base\_tds\_amount, negative tds\_amount, against\_account = row.account\_head, remarks = translated “TDS Deducted”, skip\_merge = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add supplier gl entry](operations-094.md#op-16b8c32a77e556).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L316) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L954)

<a id="op-9a260cabd7cb3e"></a>
### Purchase Invoice.make payment gl entries

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_payment_gl_entries`

**Inputs** self, gl\_entries.

**Local steps**

- If (cint(self.is\_paid) and self.cash\_bank\_account and self.paid\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_paid) → self.cash\_bank\_account → self.paid\_amount.
  - Set against\_voucher from self.name.
  - If (self.is\_return and self.return\_against and not self.update\_outstanding\_for\_self).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against → not self.update\_outstanding\_for\_self.
    - Set against\_voucher from self.return\_against.
  - Set bank\_account\_currency from get\_account\_currency(self.cash\_bank\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.credit\_to, “party\_type” → “Supplier”, “party” → self.supplier, “against” → self.cash\_bank\_account, …), self.party\_account\_currency, item = self)).
    - Value choice on self.party\_account\_currency equals self.company\_currency — true gives self.base\_paid\_amount, false gives self.paid\_amount.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.cash\_bank\_account, “against” → self.supplier, “credit” → self.base\_paid\_amount, “credit\_in\_account\_currency” → self.base\_paid\_amount when bank\_ac ….
    - Value choice on bank\_account\_currency equals self.company\_currency — true gives self.base\_paid\_amount, false gives self.paid\_amount.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L320) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L958)

<a id="op-d260a3673cf47f"></a>
### Purchase Invoice.make write off gl entry

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_write_off_gl_entry`

**Inputs** self, gl\_entries.

**Local steps**

- If (self.write\_off\_account and flt(self.write\_off\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.write\_off\_account → flt(self.write\_off\_amount).
  - Set write\_off\_account\_currency from get\_account\_currency(self.write\_off\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.credit\_to, “party\_type” → “Supplier”, “party” → self.supplier, “against” → self.write\_off\_account, …), self.party\_account\_currency, item = self)).
    - Value choice on self.party\_account\_currency equals self.company\_currency — true gives self.base\_write\_off\_amount, false gives self.write\_off\_amount.
    - Value choice on (cint(self.is\_return) and self.return\_against) — true gives self.return\_against, false gives self.name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.return\_against.
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → self.write\_off\_account, “against” → self.supplier, “credit” → flt(self.base\_write\_off\_amount), “credit\_in\_account\_currency” → self.base\_write\_off\_amou ….
    - Value choice on write\_off\_account\_currency equals self.company\_currency — true gives self.base\_write\_off\_amount, false gives self.write\_off\_amount.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → self.write\_off\_cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L326) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L964)

<a id="op-9d1a37c6eb576b"></a>
### Purchase Invoice.make gle for rounding adjustment

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_make_gle_for_rounding_adjustment`

**Inputs** self, gl\_entries.

**Explicit failure paths** validation helper — translated “Opening Invoice has rounding adjustment of {0}.&lt;br&gt;&lt;br&gt; '{1}' account is required to post these values. Plea …”.format(Platform.bold(self.rounding\_adjustment), Platform.bold(“Round Off for Open ….

**Local steps**

- If (not self.is\_internal\_transfer() and self.rounding\_adjustment and self.base\_rounding\_adjustment).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_internal\_transfer() → self.rounding\_adjustment → self.base\_rounding\_adjustment.
  - Set tuple(round\_off\_account, round\_off\_cost\_center, round\_off\_for\_opening) from get\_round\_off\_account\_and\_cost\_center(self.company, “Purchase Invoice”, self.name, self.use\_company\_roundoff\_cost\_center).
  - If (self.is\_opening equals “Yes” and self.rounding\_adjustment).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_opening equals “Yes” → self.rounding\_adjustment.
    - If not round\_off\_for\_opening.
      - Call the validation error handler Platform.throw(translated “Opening Invoice has rounding adjustment of {0}.&lt;br&gt;&lt;br&gt; '{1}' account is required to post these values. Plea …”.format(Platform.bold(self.rounding\_adjustment), Platform.bold(“Rou ….
    - Otherwise.
      - Set round\_off\_account from round\_off\_for\_opening.
  - Set round\_off\_account\_currency from get\_account\_currency(round\_off\_account).
  - Evaluate gl\_entries.append(self.get\_gl\_dict(mapping(“account” → round\_off\_account, “against” → self.supplier, “debit\_in\_transaction\_currency” → flt(self.rounding\_adjustment, self.precision(“rounding\_adjustment”)),  ….
    - Value choice on round\_off\_account\_currency equals self.company\_currency — true gives self.base\_rounding\_adjustment, false gives self.rounding\_adjustment.
    - Value choice on self.use\_company\_roundoff\_cost\_center — true gives round\_off\_cost\_center, false gives (self.cost\_center or round\_off\_cost\_center).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.cost\_center → round\_off\_cost\_center.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L46) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L317) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L955)

<a id="op-677b057621c831"></a>
### Purchase Invoice.on cancel

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_on_cancel`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · resolve a document from self.doctype via get\_doc.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate check\_if\_return\_invoice\_linked\_with\_payment\_entry(self).
- If (self.is\_return and self.is\_internal\_supplier).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.is\_internal\_supplier.
  - Evaluate self.validate\_internal\_transfer\_qty().
- Evaluate super().on\_cancel().
- Evaluate PurchaseTaxWithholding(self).on\_cancel().
- Evaluate self.check\_purchase\_order\_on\_hold\_or\_close(“purchase\_order”, exclude\_if\_field = “purchase\_receipt”).
- If (self.is\_return and not self.update\_billed\_amount\_in\_purchase\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.update\_billed\_amount\_in\_purchase\_order.
  - Set self.status\_updater from list().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- If not self.is\_return.
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Purchase Receipt”).
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Purchase Order”).
- Evaluate self.update\_billing\_status\_in\_pr().
- If self.update\_stock equals 1.
  - Evaluate self.update\_stock\_ledger().
  - Evaluate self.delete\_auto\_created\_batches().
  - If self.is\_old\_subcontracting\_flow.
    - Evaluate self.set\_consumed\_qty\_in\_subcontract\_order().
- Evaluate self.make\_gl\_entries\_on\_cancel().
- If self.update\_stock equals 1.
  - Evaluate self.repost\_future\_sle\_and\_gle().
- If Platform.db.get\_single\_value(“Buying Settings”, “project\_update\_frequency”) equals “Each Transaction”.
  - Evaluate self.update\_project().
- Evaluate self.db\_set(“status”, “Cancelled”).
- Evaluate unlink\_inter\_company\_doc(self.doctype, self.name, self.inter\_company\_invoice\_reference).
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Repost Item Valuation”, “Repost Payment Ledger”, …).
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate Platform.get\_doc(self.doctype, self.return\_against).set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [update status updater args](operations-093.md#op-ec446575fb22fc), [update billing status in pr](operations-094.md#op-fbf06faf221098), [update project](operations-094.md#op-9eb56a154ef3b4).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “project\_update\_frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L927)

<a id="op-9eb56a154ef3b4"></a>
### Purchase Invoice.update project

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_update_project`

**Inputs** self.

**Local steps**

- Evaluate update\_purchase\_cost(set of d.project for d drawn from self.items where d.project).
  - Draw d from self.items, keep a combination only if (d.project).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L768) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L940)

<a id="op-d572acf1cdbcfb"></a>
### Purchase Invoice.validate supplier invoice

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_supplier_invoice`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value · execute query text (SELECT, Purchase Invoice).

**Explicit failure paths** validation helper — translated “Supplier Invoice No exists in Purchase Invoice {0}”.format(get\_link\_to\_form(“Purchase Invoice”, pi)).

**Local steps**

- If self.bill\_no.
  - If cint(Platform.get\_single\_value(“Accounts Settings”, “check\_supplier\_invoice\_uniqueness”)).
    - Set fiscal\_year from get\_fiscal\_year(self.posting\_date, company = self.company, as\_dict = true).
    - Set pi from Platform.db.sql(query text (SELECT, Purchase Invoice), mapping(“bill\_no” → self.bill\_no, “supplier” → self.supplier, “name” → self.name, “year\_start\_date” → fiscal\_year.year\_start\_date, …)).
    - If pi.
      - Set pi from pi at 0 at 0.
      - Call the validation error handler Platform.throw(translated “Supplier Invoice No exists in Purchase Invoice {0}”.format(get\_link\_to\_form(“Purchase Invoice”, pi))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “check\_supplier\_invoice\_uniqueness”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L781) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L953)

<a id="op-fbf06faf221098"></a>
### Purchase Invoice.update billing status in pr

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_update_billing_status_in_pr`

**Inputs** self, update\_modified = true.

**Record and data access** read “Buying Settings” via get\_single\_value.

**State and service calls** request set\_value on “Purchase Receipt Item”.

**Explicit results** no value.

**Local steps**

- If (self.is\_return and not self.update\_billed\_amount\_in\_purchase\_receipt).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.update\_billed\_amount\_in\_purchase\_receipt.
  - Return no value.
- Set updated\_pr from list().
- Set po\_details from list().
- Set pr\_details\_billed\_amt from self.get\_pr\_details\_billed\_amt().
- For each d in self.get(“items”).
  - If d.pr\_detail.
    - Evaluate Platform.db.set\_value(“Purchase Receipt Item”, d.pr\_detail, “billed\_amt”, flt(pr\_details\_billed\_amt.get(d.pr\_detail)), update\_modified = update\_modified).
    - Evaluate updated\_pr.append(d.purchase\_receipt).
  - Otherwise.
    - If d.po\_detail.
      - Evaluate po\_details.append(d.po\_detail).
- If po\_details.
  - Update updated\_pr using + update\_billed\_amount\_based\_on\_po(po\_details, update\_modified).
- Set adjust\_incoming\_rate from Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).
- For each pr in set(updated\_pr).
  - Bind dependencies update\_billing\_percentage.
  - Set pr\_doc from Platform.get\_lazy\_doc(“Purchase Receipt”, pr).
  - Evaluate update\_billing\_percentage(pr\_doc, update\_modified = update\_modified, adjust\_incoming\_rate = adjust\_incoming\_rate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get pr details billed amt](operations-094.md#op-3ea57a8f51ad5d).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L328) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L966)

<a id="op-3ea57a8f51ad5d"></a>
### Purchase Invoice.get pr details billed amt

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_get_pr_details_billed_amt`

**Inputs** self.

**Explicit results** pr\_details\_billed\_amt.

**Local steps**

- Set pr\_details\_billed\_amt from mapping().
- Set pr\_details from list of d.get(“pr\_detail”) for d drawn from self.get(“items”) where d.get(“pr\_detail”).
  - Draw d from self.get(“items”), keep a combination only if (d.get(“pr\_detail”)).
- If pr\_details.
  - Set doctype from Platform.qb.DocType(“Purchase Invoice Item”).
  - Set query from nested operand in the contract(nested operand in the contract).select(doctype.pr\_detail, Sum(nested operand in the contract.amount)).where((nested operand in the contract.isin(pr\_details) bitwise and docty ….
  - Set pr\_details\_billed\_amt from Platform.\_dict(query.run(as\_list = 1)).
- Return pr\_details\_billed\_amt.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L950)

<a id="op-e381b093e482bd"></a>
### Purchase Invoice.on recurring

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_on_recurring`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Local steps**

- Evaluate super().on\_recurring(reference\_doc, auto\_repeat\_doc).
- Set self.due\_date from no value.
- Evaluate self.shift\_service\_dates(reference\_doc, auto\_repeat\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L928)

<a id="op-af9f0b42b6ab40"></a>
### Purchase Invoice.block invoice

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_block_invoice`

**Inputs** self, hold\_comment = no value, release\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set self.on\_hold from 1.
- Set self.release\_date from release\_date.
- Evaluate self.validate\_block\_invoice().
- Evaluate self.db\_set(mapping(“on\_hold” → 1, “hold\_comment” → cstr(hold\_comment), “release\_date” → release\_date)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate block invoice](operations-095.md#op-b0f7bbaaf8ebee).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L4978) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L745) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L917)
