# Accounting and settlement · operations 56

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Journal entry

[Record definition](../../../../data/record-types/journal_entry.json)

<a id="op-17ba46956c17ac"></a>
### Journal Entry.on cancel

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_on_cancel`

**Inputs** self.

**Local steps**

- Evaluate super().on\_cancel().
- Set from\_doc\_events from getattr(self, “ignore\_linked\_doctypes”, tuple()).
- Set self.ignore\_linked\_doctypes from tuple(“GL Entry”, “Stock Ledger Entry”, “Payment Ledger Entry”, “Repost Payment Ledger”, …).
- If (from\_doc\_events and from\_doc\_events differs from self.ignore\_linked\_doctypes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_doc\_events → from\_doc\_events differs from self.ignore\_linked\_doctypes.
  - Set self.ignore\_linked\_doctypes from (self.ignore\_linked\_doctypes + from\_doc\_events).
- Evaluate self.make\_gl\_entries(1).
- Evaluate JournalTaxWithholding(self).on\_cancel().
- Evaluate self.unlink\_advance\_entry\_reference().
- Evaluate self.unlink\_asset\_reference().
- Evaluate self.unlink\_inter\_company\_jv().
- Evaluate self.unlink\_asset\_adjustment\_entry().
- Evaluate self.update\_invoice\_discounting().
- Evaluate self.update\_payment\_order\_requests(cancel = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [make gl entries](operations-057.md#op-cfdfd9f84a32e5), [unlink advance entry reference](operations-056.md#op-2321e1dbb96871), [unlink asset reference](operations-056.md#op-38a8f790c4c21b), [unlink inter company jv](operations-056.md#op-2dd8dd63bd51f9), [unlink asset adjustment entry](operations-056.md#op-bc14608d2c0cf1), [update invoice discounting](operations-056.md#op-987035d50c80c7), [update payment order requests](operations-056.md#op-6aaa63e2185718).

**Values supplied outside this operation** selected callable from getattr(self, “ignore\_linked\_doctypes”, tuple()).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L112) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1126)

<a id="op-8943c790adce73"></a>
### Journal Entry.on trash

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_payment\_reference.
- Evaluate super().on\_trash().
- Evaluate clear\_payment\_reference(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L163) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L801)

<a id="op-6aaa63e2185718"></a>
### Journal Entry.update payment order requests

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_payment_order_requests`

**Inputs** self, cancel = false.

**Local steps**

- Bind dependencies update\_payment\_requests\_from\_journal\_entry.
- Evaluate update\_payment\_requests\_from\_journal\_entry(self, cancel = cancel).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L171) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L809)

<a id="op-6c32dd88edac91"></a>
### Journal Entry.get title

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_get_title`

**Inputs** self.

**Explicit results** (self.pay\_to\_recd\_from or self.accounts at 0.account).

**Local steps**

- Return (self.pay\_to\_recd\_from or self.accounts at 0.account).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.pay\_to\_recd\_from → self.accounts at 0.account.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L2847) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1122)

<a id="op-2731739197ca38"></a>
### Journal Entry.validate inter company accounts

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_inter_company_accounts`

**Inputs** self.

**Record and data access** read “Journal Entry” via get\_value · read “Company” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Total Credit/ Debit Amount should be same as linked Journal Entry”.

**Local steps**

- If (self.voucher\_type equals “Inter Company Journal Entry” and self.inter\_company\_journal\_entry\_reference).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Inter Company Journal Entry” → self.inter\_company\_journal\_entry\_reference.
  - Set doc from Platform.db.get\_value(“Journal Entry”, self.inter\_company\_journal\_entry\_reference, list(“company”, “total\_debit”, “total\_credit”), as\_dict = true).
  - Set account\_currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - Set previous\_account\_currency from Platform.get\_cached\_value(“Company”, doc.company, “default\_currency”).
  - If account\_currency equals previous\_account\_currency.
    - Set credit\_precision from self.precision(“total\_credit”).
    - Set debit\_precision from self.precision(“total\_debit”).
    - If (flt(self.total\_credit, credit\_precision) differs from flt(doc.total\_debit, debit\_precision) or flt(self.total\_debit, debit\_precision) differs from flt(doc.total\_credit, credit\_precision)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(self.total\_credit, credit\_precision) differs from flt(doc.total\_debit, debit\_precision) → flt(self.total\_debit, debit\_precision) differs from flt(doc.total\_credit, credit\_precision).
      - Call the validation error handler Platform.throw(translated “Total Credit/ Debit Amount should be same as linked Journal Entry”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”), Platform.get\_cached\_value(“Company”, doc.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L2913) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1223) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1151)

<a id="op-22a3a2c67d1c16"></a>
### Journal Entry.validate depr account and depr entry voucher type

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_validate_depr_account_and_depr_entry_voucher_type`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Journal Entry type should be set as Depreciation Entry for asset depreciation” · validation helper — translated “Account {0} should be of type Expense”.format(d.account).

**Local steps**

- For each d in self.get(“accounts”).
  - If d.account\_type equals “Depreciation”.
    - <a id="op-22a3a2c67d1c16-guard-4"></a>If self.voucher\_type differs from “Depreciation Entry”.
      - Call the validation error handler Platform.throw(translated “Journal Entry type should be set as Depreciation Entry for asset depreciation”).
    - If Platform.get\_cached\_value(“Account”, d.account, “root\_type”) differs from “Expense”.
      - Call the validation error handler Platform.throw(translated “Account {0} should be of type Expense”.format(d.account)).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.voucher\_type differs from “Depreciation Entry”, self.voucher\_type = “Journal Entry” selects the branch that calls the validation-error handler with translated “Journal Entry type should be set as Depreciation Entry for asset depreciation”. With self.voucher\_type = “Depreciation Entry”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-22a3a2c67d1c16-guard-4)

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “root\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L812)

<a id="op-71f928ca8d06c9"></a>
### Journal Entry.validate stock accounts

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_stock_accounts`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with StockAccountInvalidTransaction — translated “Account: {0} can only be updated via Stock Transactions”.format(account).

**Local steps**

- If (not Enterprise.is\_perpetual\_inventory\_enabled(self.company) or self.voucher\_type equals “Periodic Accounting Entry”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Enterprise.is\_perpetual\_inventory\_enabled(self.company) → self.voucher\_type equals “Periodic Accounting Entry”.
  - Return no value.
- Set stock\_accounts from get\_stock\_accounts(self.company, accounts = self.accounts).
- For each account in stock\_accounts.
  - Set tuple(account\_bal, stock\_bal, warehouse\_list) from get\_stock\_and\_account\_balance(account, self.posting\_date, self.company).
  - If account\_bal equals stock\_bal.
    - Call the validation error handler Platform.throw(translated “Account: {0} can only be updated via Stock Transactions”.format(account), StockAccountInvalidTransaction).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L3423) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1229) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1154)

<a id="op-f20ca267d0e9fa"></a>
### Journal Entry.update asset value

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_asset_value`

**Inputs** self.

**Local steps**

- Evaluate self.update\_asset\_on\_depreciation().
- Evaluate self.update\_asset\_on\_disposal().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update asset on depreciation](operations-056.md#op-e3668f91a237dd), [update asset on disposal](operations-056.md#op-7d730daa9eb525).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L168) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L806)

<a id="op-e3668f91a237dd"></a>
### Journal Entry.update asset on depreciation

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_asset_on_depreciation`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · resolve a document from “Asset” via get\_cached\_doc.

**State and service calls** call db\_set on asset.

**Explicit results** no value.

**Local steps**

- <a id="op-e3668f91a237dd-guard-2"></a>If self.voucher\_type differs from “Depreciation Entry”.
  - Return no value.
- For each d in self.get(“accounts”).
  - If (d.reference\_type equals “Asset” and d.reference\_name and Platform.get\_cached\_value(“Account”, d.account, “root\_type”) equals “Expense” and d.debit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Asset” → d.reference\_name → Platform.get\_cached\_value(“Account”, d.account, “root\_type”) equals “Expense” → d.debit.
    - Set asset from Platform.get\_cached\_doc(“Asset”, d.reference\_name).
    - If asset.calculate\_depreciation.
      - Evaluate self.update\_journal\_entry\_link\_on\_depr\_schedule(asset, d).
      - Evaluate self.update\_value\_after\_depreciation(asset, d.debit).
      - Evaluate asset.sync\_value\_after\_depreciation().
    - Otherwise.
      - Evaluate asset.db\_set(“value\_after\_depreciation”, (asset.value\_after\_depreciation − d.debit)).
    - Evaluate asset.set\_status().
    - Evaluate asset.set\_total\_booked\_depreciations().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.voucher\_type differs from “Depreciation Entry”, self.voucher\_type = “Journal Entry” selects the branch that returns no value. With self.voucher\_type = “Depreciation Entry”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-e3668f91a237dd-guard-2)

**Methods declared on this owner** [update journal entry link on depr schedule](operations-056.md#op-c7eec53c257ad8), [update value after depreciation](operations-056.md#op-89298679bf6526).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “root\_type”), Platform.get\_cached\_doc(“Asset”, d.reference\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L166) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L804)

<a id="op-89298679bf6526"></a>
### Journal Entry.update value after depreciation

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_value_after_depreciation`

**Inputs** self, asset, depr\_amount.

**State and service calls** request set\_value on “Asset Finance Book”.

**Local steps**

- Set fb\_idx from 1.
- If self.finance\_book.
  - For each fb\_row in asset.get(“finance\_books”).
    - If fb\_row.finance\_book equals self.finance\_book.
      - Set fb\_idx from fb\_row.idx.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set fb\_row from asset.get(“finance\_books”) at (fb\_idx − 1).
- Update fb\_row.value\_after\_depreciation using − depr\_amount.
- Evaluate Platform.db.set\_value(“Asset Finance Book”, fb\_row.name, “value\_after\_depreciation”, fb\_row.value\_after\_depreciation).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L172) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L810)

<a id="op-c7eec53c257ad8"></a>
### Journal Entry.update journal entry link on depr schedule

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_journal_entry_link_on_depr_schedule`

**Inputs** self, asset, je\_row.

**State and service calls** request set\_value on “Depreciation Schedule”.

**Local steps**

- Set depr\_schedule from get\_depr\_schedule(asset.name, “Active”, self.finance\_book).
- Set precision from je\_row.precision(“debit”).
- For each d in (depr\_schedule or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in depr\_schedule → list().
  - If (d.schedule\_date equals self.posting\_date and not d.journal\_entry and flt(d.depreciation\_amount, precision) equals flt(je\_row.debit, precision)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.schedule\_date equals self.posting\_date → not d.journal\_entry → flt(d.depreciation\_amount, precision) equals flt(je\_row.debit, precision).
    - Evaluate Platform.db.set\_value(“Depreciation Schedule”, d.name, “journal\_entry”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L170) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L808)

<a id="op-7d730daa9eb525"></a>
### Journal Entry.update asset on disposal

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_asset_on_disposal`

**Inputs** self.

**Record and data access** resolve a document from “Asset” via get\_doc.

**State and service calls** request set\_value on “Asset”.

**Local steps**

- If self.voucher\_type equals “Asset Disposal”.
  - Set disposed\_assets from list().
  - For each d in self.get(“accounts”).
    - If (d.reference\_type equals “Asset” and d.reference\_name and d.reference\_name does not belong to disposed\_assets).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type equals “Asset” → d.reference\_name → d.reference\_name does not belong to disposed\_assets.
      - Evaluate Platform.db.set\_value(“Asset”, d.reference\_name, mapping(“disposal\_date” → self.posting\_date, “journal\_entry\_for\_scrap” → self.name)).
      - Set asset\_doc from Platform.get\_doc(“Asset”, d.reference\_name).
      - Evaluate asset\_doc.set\_status().
      - Evaluate disposed\_assets.append(d.reference\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L167) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L805)

<a id="op-7805b35026630a"></a>
### Journal Entry.update inter company jv

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_update_inter_company_journal_voucher`

**Inputs** self.

**State and service calls** request set\_value on “Journal Entry”.

**Local steps**

- If (self.voucher\_type equals “Inter Company Journal Entry” and self.inter\_company\_journal\_entry\_reference).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Inter Company Journal Entry” → self.inter\_company\_journal\_entry\_reference.
  - Evaluate Platform.db.set\_value(“Journal Entry”, self.inter\_company\_journal\_entry\_reference, “inter\_company\_journal\_entry\_reference”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L3721) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1139)

<a id="op-987035d50c80c7"></a>
### Journal Entry.update invoice discounting

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_update_invoice_discounting`

**Inputs** self.

**Record and data access** resolve a document from “Invoice Discounting” via get\_doc.

**Local steps**

- Bind local operation \_validate\_invoice\_discounting\_status for subsequent calls.
- Set invoice\_discounting\_list from list(set(list of d.reference\_name for d drawn from self.accounts where d.reference\_type equals “Invoice Discounting”)).
  - Draw d from self.accounts, keep a combination only if (d.reference\_type equals “Invoice Discounting”).
- For each inv\_disc in invoice\_discounting\_list.
  - Set inv\_disc\_doc from Platform.get\_doc(“Invoice Discounting”, inv\_disc).
  - Set status from no value.
  - For each d in self.accounts.
    - If (d.account equals inv\_disc\_doc.short\_term\_loan and d.reference\_name equals inv\_disc).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.account equals inv\_disc\_doc.short\_term\_loan → d.reference\_name equals inv\_disc.
      - If self.docstatus equals 1.
        - If d.credit &gt; 0.
          - Evaluate \_validate\_invoice\_discounting\_status(inv\_disc, inv\_disc\_doc.status, “Sanctioned”, d.idx).
          - Set status from “Disbursed”.
        - Otherwise.
          - If d.debit &gt; 0.
            - Evaluate \_validate\_invoice\_discounting\_status(inv\_disc, inv\_disc\_doc.status, “Disbursed”, d.idx).
            - Set status from “Settled”.
      - Otherwise.
        - If d.credit &gt; 0.
          - Evaluate \_validate\_invoice\_discounting\_status(inv\_disc, inv\_disc\_doc.status, “Disbursed”, d.idx).
          - Set status from “Sanctioned”.
        - Otherwise.
          - If d.debit &gt; 0.
            - Evaluate \_validate\_invoice\_discounting\_status(inv\_disc, inv\_disc\_doc.status, “Settled”, d.idx).
            - Set status from “Disbursed”.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If status.
    - Evaluate inv\_disc\_doc.set\_status(status = status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1140)

<a id="op-2a4102835bafe0"></a>
### Journal Entry.update invoice discounting.validate invoice discounting status

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_update_invoice_discounting_validate_invoice_discounting_status`

**Inputs** inv\_disc, id\_status, expected\_status, row\_id.

**Explicit failure paths** validation helper — translated “Row #{0}: Status must be {1} for Invoice Discounting {2}”.format(d.idx, expected\_status, id\_link).

**Local steps**

- Set id\_link from get\_link\_to\_form(“Invoice Discounting”, inv\_disc).
- If id\_status differs from expected\_status.
  - Call the validation error handler Platform.throw(translated “Row #{0}: Status must be {1} for Invoice Discounting {2}”.format(d.idx, expected\_status, id\_link)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L169) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L807)

<a id="op-2321e1dbb96871"></a>
### Journal Entry.unlink advance entry reference

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_unlink_advance_entry_reference`

**Inputs** self.

**Record and data access** resolve a document from d.reference\_type via get\_doc.

**State and service calls** call db\_update on d.

**Local steps**

- For each d in self.get(“accounts”).
  - If (d.is\_advance equals “Yes” and d.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.is\_advance equals “Yes” → d.reference\_type belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
    - Set doc from Platform.get\_doc(d.reference\_type, d.reference\_name).
    - Evaluate doc.delink\_advance\_entries(self.name).
    - Set d.reference\_type from empty text.
    - Set d.reference\_name from empty text.
    - Evaluate d.db\_update().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L4620) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1209) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1137)

<a id="op-38a8f790c4c21b"></a>
### Journal Entry.unlink asset reference

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_unlink_asset_reference`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value · resolve a document from “Asset” via get\_doc · read “Asset” via get\_value.

**State and service calls** call db\_set on s · call db\_update on fb\_row · call db\_set on asset.

**Explicit failure paths** validation helper — translated “Journal Entry for Asset scrapping cannot be cancelled. Please restore the Asset.”.

**Local steps**

- For each d in self.get(“accounts”).
  - If (self.voucher\_type equals “Depreciation Entry” and d.reference\_type equals “Asset” and d.reference\_name and Platform.get\_cached\_value(“Account”, d.account, “root\_type”) equals “Expense” and d.debit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Depreciation Entry” → d.reference\_type equals “Asset” → d.reference\_name → Platform.get\_cached\_value(“Account”, d.account, “root\_type”) equals “Expense” → d.debit.
    - Set asset from Platform.get\_doc(“Asset”, d.reference\_name).
    - If asset.calculate\_depreciation.
      - Set je\_found from false.
      - For each fb\_row in asset.get(“finance\_books”).
        - If je\_found.
          - Leave the innermost loop without its normal-exhaustion alternative.
        - Set depr\_schedule from get\_depr\_schedule(asset.name, “Active”, fb\_row.finance\_book).
        - For each s in (depr\_schedule or list()).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in depr\_schedule → list().
          - If s.journal\_entry equals self.name.
            - Evaluate s.db\_set(“journal\_entry”, no value).
            - Update fb\_row.value\_after\_depreciation using + d.debit.
            - Evaluate fb\_row.db\_update().
            - Set je\_found from true.
            - Leave the innermost loop without its normal-exhaustion alternative.
      - If not je\_found.
        - Set fb\_idx from 1.
        - If self.finance\_book.
          - For each fb\_row in asset.get(“finance\_books”).
            - If fb\_row.finance\_book equals self.finance\_book.
              - Set fb\_idx from fb\_row.idx.
              - Leave the innermost loop without its normal-exhaustion alternative.
        - Set fb\_row from asset.get(“finance\_books”) at (fb\_idx − 1).
        - Update fb\_row.value\_after\_depreciation using + d.debit.
        - Evaluate fb\_row.db\_update().
      - Evaluate asset.sync\_value\_after\_depreciation().
    - Otherwise.
      - Evaluate asset.db\_set(“value\_after\_depreciation”, (asset.value\_after\_depreciation + d.debit)).
    - Evaluate asset.set\_status().
    - Evaluate asset.set\_total\_booked\_depreciations().
  - Otherwise.
    - If (self.voucher\_type equals “Journal Entry” and d.reference\_type equals “Asset” and d.reference\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Journal Entry” → d.reference\_type equals “Asset” → d.reference\_name.
      - Set journal\_entry\_for\_scrap from Platform.db.get\_value(“Asset”, d.reference\_name, “journal\_entry\_for\_scrap”).
      - If journal\_entry\_for\_scrap equals self.name.
        - Call the validation error handler Platform.throw(translated “Journal Entry for Asset scrapping cannot be cancelled. Please restore the Asset.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “root\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L165) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L803)

<a id="op-2dd8dd63bd51f9"></a>
### Journal Entry.unlink inter company jv

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_unlink_inter_company_journal_voucher`

**Inputs** self.

**State and service calls** request set\_value on “Journal Entry”.

**Local steps**

- If (self.voucher\_type equals “Inter Company Journal Entry” and self.inter\_company\_journal\_entry\_reference).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.voucher\_type equals “Inter Company Journal Entry” → self.inter\_company\_journal\_entry\_reference.
  - Evaluate Platform.db.set\_value(“Journal Entry”, self.inter\_company\_journal\_entry\_reference, “inter\_company\_journal\_entry\_reference”, empty text).
  - Evaluate Platform.db.set\_value(“Journal Entry”, self.name, “inter\_company\_journal\_entry\_reference”, empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L4880) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1138)

<a id="op-7c3c06648dc4be"></a>
### Journal Entry.has asset adjustment entry

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_has_asset_adjustment_entry`

**Inputs** self.

**Record and data access** read “Asset Value Adjustment” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot cancel this document as it is linked with the submitted Asset Value Adjustment &lt;b&gt;{0}&lt;/b&gt;. Please can …”.format(Platform.utils.get\_link\_to\_form(“Asset Value Adjustment”, asset\_value\_adjustment)).

**Local steps**

- If self.flags.get(“via\_asset\_value\_adjustment”).
  - Return no value.
- Set asset\_value\_adjustment from Platform.db.get\_value(“Asset Value Adjustment”, mapping(“docstatus” → 1, “journal\_entry” → self.name), “name”).
- If asset\_value\_adjustment.
  - Call the validation error handler Platform.throw(translated “Cannot cancel this document as it is linked with the submitted Asset Value Adjustment &lt;b&gt;{0}&lt;/b&gt;. Please can …”.format(Platform.utils.get\_link\_to\_form(“Asset Value Adjustment”, a ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L162) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L800)

<a id="op-bc14608d2c0cf1"></a>
### Journal Entry.unlink asset adjustment entry

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_unlink_asset_adjustment_entry`

**Inputs** self.

**Local steps**

- Set AssetValueAdjustment from Platform.qb.DocType(“Asset Value Adjustment”).
- Evaluate nested operand in the contract(nested operand in the contract).set(AssetValueAdjustment.journal\_entry, no value).where(AssetValueAdjustment.journal\_entry equals self.name).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L164) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L802)

<a id="op-88d6351c134d8e"></a>
### Journal Entry.validate party

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_party`

**Inputs** self.

**Record and data access** read “Party Type” via exists · read “Account” via get\_cached\_value · read “Party Type” via get\_value.

**Explicit failure paths** validation helper — translated “Row {0}: {1} is not a valid Party Type”.format(d.idx, d.party\_type) · validation helper — translated “Row {0}: Party Type and Party is required for Receivable / Payable account {1}”.format(d.idx, d.account) · validation helper — translated “Row {0}: Account {1} and Party Type {2} have different account types”.format(d.idx, d.account, d.party\_type).

**Local steps**

- For each d in self.get(“accounts”).
  - If (d.party\_type and not Platform.db.exists(“Party Type”, d.party\_type)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type → not Platform.db.exists(“Party Type”, d.party\_type).
    - Call the validation error handler Platform.throw(translated “Row {0}: {1} is not a valid Party Type”.format(d.idx, d.party\_type)).
  - Set account\_type from Platform.get\_cached\_value(“Account”, d.account, “account\_type”).
  - If account\_type belongs to list(“Receivable”, “Payable”).
    - If (not (d.party\_type and d.party) and not self.party\_not\_required).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (d.party\_type and d.party) → not self.party\_not\_required.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type → d.party.
      - Call the validation error handler Platform.throw(translated “Row {0}: Party Type and Party is required for Receivable / Payable account {1}”.format(d.idx, d.account)).
    - Otherwise.
      - If (d.party\_type and Platform.db.get\_value(“Party Type”, d.party\_type, “account\_type”) differs from account\_type and d.party\_type differs from “Employee”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type → Platform.db.get\_value(“Party Type”, d.party\_type, “account\_type”) differs from account\_type → d.party\_type differs from “Employee”.
        - Call the validation error handler Platform.throw(translated “Row {0}: Account {1} and Party Type {2} have different account types”.format(d.idx, d.account, d.party\_type)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1228) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1153)

<a id="op-2449017fec857f"></a>
### Journal Entry.check credit limit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_check_credit_limit`

**Inputs** self.

**Local steps**

- Set customers from list(set(generator of d.party for d drawn from self.get(“accounts”) where (d.party\_type equals “Customer” and d.party and flt(nested operand in the contract.debit) &gt; 0))).
  - Draw d from self.get(“accounts”), keep a combination only if ((d.party\_type equals “Customer” and d.party and flt(d.debit) &gt; 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type equals “Customer” → d.party → flt(d.debit) &gt; 0.
- If customers.
  - Bind dependencies check\_credit\_limit, is\_sales\_order\_credit\_check\_bypassed.
  - For each customer in customers.
    - Set ignore\_outstanding\_sales\_order from is\_sales\_order\_credit\_check\_bypassed(customer, self.company).
    - Evaluate check\_credit\_limit(customer, self.company, ignore\_outstanding\_sales\_order).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1116)

<a id="op-aa19229c7343f8"></a>
### Journal Entry.validate cheque info

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_cheque_info`

**Inputs** self.

**Local steps**

- If self.voucher\_type belongs to list(“Bank Entry”).
  - If (not self.cheque\_no or not self.cheque\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.cheque\_no → not self.cheque\_date.
    - Evaluate msgprint(translated “Reference No &amp; Reference Date is required for {0}”.format(self.voucher\_type), raise\_exception = 1).
- If (self.cheque\_date and not self.cheque\_no).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.cheque\_date → not self.cheque\_no.
  - Evaluate msgprint(translated “Reference No is mandatory if you entered Reference Date”, raise\_exception = 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L5981) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1144)

<a id="op-4953636b95e8be"></a>
### Journal Entry.validate entries for advance

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_entries_for_advance`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: Payment against Sales/Purchase Order should always be marked as advance”.format(d.idx) · validation helper — translated “Row {0}: Advance against Customer must be credit”.format(d.idx) · validation helper — translated “Row {0}: Advance against Supplier must be debit”.format(d.idx).

**Local steps**

- For each d in self.get(“accounts”).
  - If d.reference\_type does not belong to tuple(“Sales Invoice”, “Purchase Invoice”, “Journal Entry”).
    - If ((d.party\_type equals “Customer” and flt(d.credit) &gt; 0) or (d.party\_type equals “Supplier” and flt(d.debit) &gt; 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (d.party\_type equals “Customer” and flt(d.credit) &gt; 0) → (d.party\_type equals “Supplier” and flt(d.debit) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type equals “Customer” → flt(d.credit) &gt; 0.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type equals “Supplier” → flt(d.debit) &gt; 0.
      - If d.is\_advance equals “No”.
        - Evaluate msgprint(translated “Row {0}: Please check 'Is Advance' against Account {1} if this is an advance entry.”.format(d.idx, d.account), alert = true).
      - Otherwise.
        - If (d.reference\_type belongs to tuple(“Sales Order”, “Purchase Order”) and d.is\_advance differs from “Yes”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.reference\_type belongs to tuple(“Sales Order”, “Purchase Order”) → d.is\_advance differs from “Yes”.
          - Call the validation error handler Platform.throw(translated “Row {0}: Payment against Sales/Purchase Order should always be marked as advance”.format(d.idx)).
    - If d.is\_advance equals “Yes”.
      - If (d.party\_type equals “Customer” and flt(d.debit) &gt; 0).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type equals “Customer” → flt(d.debit) &gt; 0.
        - Call the validation error handler Platform.throw(translated “Row {0}: Advance against Customer must be credit”.format(d.idx)).
      - Otherwise.
        - If (d.party\_type equals “Supplier” and flt(d.credit) &gt; 0).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.party\_type equals “Supplier” → flt(d.credit) &gt; 0.
          - Call the validation error handler Platform.throw(translated “Row {0}: Advance against Supplier must be debit”.format(d.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0063.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1221) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1149)
