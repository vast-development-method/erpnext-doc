# Accounting and settlement · operations 55

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Item wise sales register

<a id="op-dc8ce2f800a904"></a>
### Get grand total

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_grand_total`

**Inputs** filters, doctype.

**Record and data access** read doctype via get\_value.

**Explicit results** flt(Platform.db.get\_value(doctype, mapping(“docstatus” → 1, “posting\_date” → tuple(“between”, list(nested operand in the contract.get(“from\_date”), nested operand in the contract.get(“to\_date”)))), list(mappin …).

**Local steps**

- Return flt(Platform.db.get\_value(doctype, mapping(“docstatus” → 1, “posting\_date” → tuple(“between”, list(nested operand in the contract.get(“from\_date”), nested operand in the contract.get(“to\_date”)))), list(mappin …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0266.json#L424) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L772) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1114)

<a id="op-dca1d28e340401"></a>
### Get tax accounts

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_tax_accounts`

**Inputs** item\_list, columns, company\_currency, doctype = “Sales Invoice”, tax\_doctype = “Sales Taxes and Charges”.

**Explicit results** tuple(itemised\_tax, tax\_columns\_list).

**Local steps**

- Set invoice\_item\_row from list of d.name for d drawn from item\_list.
  - Draw d from item\_list.
- Set tax from Platform.qb.DocType(“Item Wise Tax Detail”).
- Set taxes\_and\_charges from Platform.qb.DocType(tax\_doctype).
- Set account from Platform.qb.DocType(“Account”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.account\_head equals nested operand in the contract.name).select(account.account\_type).where(tax.item\_row.isi ….
- If doctype equals “Purchase Invoice”.
  - Set query from query.where((taxes\_and\_charges.category.isin(list(“Total”, “Valuation and Total”)) bitwise and taxes\_and\_charges.base\_tax\_amount\_after\_discount\_amount differs from 0)).
- Set tax\_details from query.run(as\_dict = true).
- Set precision from (Platform.get\_precision(tax\_doctype, “tax\_amount”, currency = company\_currency) or 2).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_precision(tax\_doctype, “tax\_amount”, currency = company\_currency) → 2.
- Set tax\_columns from mapping().
- Set itemised\_tax from mapping().
- Set column\_keys from mapping().
- For each row in tax\_details.
  - Set account from (row.account\_head or handle\_html(row.description)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.account\_head → handle\_html(row.description).
  - Set column\_key from get\_column\_key(account, column\_keys).
  - If (column\_key does not belong to tax\_columns and row.amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in column\_key does not belong to tax\_columns → row.amount.
    - Set tax\_columns at column\_key from account.
  - Set rate from “NA” when row.rate equals 0, otherwise row.rate.
    - Value choice on row.rate equals 0 — true gives “NA”, false gives row.rate.
  - Set item\_taxes from itemised\_tax.setdefault(row.item\_row, mapping()).
  - If column\_key belongs to item\_taxes.
    - Set item\_taxes at column\_key.tax\_rate from combine\_tax\_rates(item\_taxes at column\_key.tax\_rate, rate).
  - Otherwise.
    - Set item\_taxes at column\_key from Platform.\_dict(mapping(“tax\_rate” → rate, “tax\_amount” → 0, “is\_other\_charges” → 0 when row.account\_type equals “Tax”, otherwise 1)).
      - Value choice on row.account\_type equals “Tax” — true gives 0, false gives 1.
  - Update item\_taxes at column\_key.tax\_amount using + flt(row.amount, precision).
- Set tax\_columns\_list from list(tax\_columns.keys()).
- Evaluate tax\_columns\_list.sort().
- For each column\_key in tax\_columns\_list.
  - Set account from tax\_columns at column\_key.
  - Evaluate columns.append(mapping(“label” → translated (account + “ Rate”), “fieldname” → formatted text {column\_key}\_rate, “fieldtype” → “Float”, “width” → 100)).
  - Evaluate columns.append(mapping(“label” → translated (account + “ Amount”), “fieldname” → formatted text {column\_key}\_amount, “fieldtype” → “Currency”, “options” → “currency”, …)).
- Update columns using + list(mapping(“label” → translated “Total Tax”, “fieldname” → “total\_tax”, “fieldtype” → “Currency”, “options” → “currency”, …), mapping(“label” → translated “Total Other Charges”, “fieldname” → “total\_othe ….
- Return tuple(itemised\_tax, tax\_columns\_list).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1118)

<a id="op-2d5c938e538b04"></a>
### Get column key

`operation_enterprise_binding_enterprise_accounts_report_item_wise_sales_register_item_wise_sales_register_get_column_key`

**Inputs** account, column\_keys.

**Declared result** str.

**Explicit results** column\_keys at account.

**Local steps**

- If account does not belong to column\_keys.
  - Set column\_keys at account from Platform.scrub(account).
  - If has\_scrubbed\_name\_clash(account).
    - Update column\_keys at account using + (“\_” + hashlib.sha256(nested operand in the contract.encode()).hexdigest() at slice no value to 8).
- Return column\_keys at account.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L585) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1223)

<a id="op-8f9522a0028732"></a>
### Has scrubbed name clash

`operation_enterprise_binding_enterprise_accounts_report_item_wise_sales_register_item_wise_sales_register_has_scrubbed_name_clash`

**Inputs** account.

**Declared result** bool.

**Record and data access** read “Account” via get\_all.

**Explicit results** any(generator of (name differs from account and Platform.scrub(name) equals Platform.scrub(account)) for name drawn from similar\_accounts).

**Local steps**

- Set pattern from re.sub(“&#91; \\-%\\\\&#93;”, “\_”, account).
- Set similar\_accounts from Platform.get\_all(“Account”, filters = mapping(“name” → tuple(“like”, pattern)), pluck = “name”).
- Return any(generator of (name differs from account and Platform.scrub(name) equals Platform.scrub(account)) for name drawn from similar\_accounts).
  - Draw name from similar\_accounts.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name differs from account → Platform.scrub(name) equals Platform.scrub(account).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L162) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L589) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1227)

<a id="op-afd8c31428948b"></a>
### Combine tax rates

`operation_enterprise_binding_enterprise_accounts_report_item_wise_sales_register_item_wise_sales_register_combine_tax_rates`

**Inputs** existing\_rate, rate.

**Declared result** (float bitwise or str).

**Explicit results** “NA” · (flt(existing\_rate) + flt(rate)).

**Local steps**

- If “NA” belongs to tuple(existing\_rate, rate).
  - Return “NA”.
- Return (flt(existing\_rate) + flt(rate)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L584) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1222)

<a id="op-810bc63205a34e"></a>
### Get tax details query

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_tax_details_query`

**Inputs** doctype, tax\_doctype.

**Explicit results** query.

**Local steps**

- Set tax from Platform.qb.DocType(“Item Wise Tax Detail”).
- Set taxes\_and\_charges from Platform.qb.DocType(tax\_doctype).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.tax\_row equals nested operand in the contract.name).select(tax.parent, tax.item\_row, tax.rate, tax.amount, … ….
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0266.json#L2511) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1119)

<a id="op-91be67de89a0fd"></a>
### Add total row

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_add_total_row`

**Inputs** data, filters, prev\_group\_by\_value, item, total\_row\_map, group\_by\_field, subtotal\_display\_field, grand\_total, tax\_columns.

**Explicit results** tuple(data, prev\_group\_by\_value).

**Local steps**

- If prev\_group\_by\_value differs from item.get(group\_by\_field, empty text).
  - If prev\_group\_by\_value.
    - Set total\_row from total\_row\_map.get(prev\_group\_by\_value).
    - Evaluate data.append(total\_row).
    - Evaluate data.append(mapping()).
    - Evaluate add\_sub\_total\_row(total\_row, total\_row\_map, “total\_row”, tax\_columns).
  - Set prev\_group\_by\_value from item.get(group\_by\_field, empty text).
  - Evaluate total\_row\_map.setdefault(item.get(group\_by\_field, empty text), mapping(subtotal\_display\_field → get\_display\_value(filters, group\_by\_field, item), “stock\_qty” → 0.0, “amount” → 0.0, “bold” → 1, …)).
  - Evaluate total\_row\_map.setdefault(“total\_row”, mapping(subtotal\_display\_field → “Total”, “stock\_qty” → 0.0, “amount” → 0.0, “bold” → 1, …)).
- Return tuple(data, prev\_group\_by\_value).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1106)

<a id="op-7f3b81abff13dd"></a>
### Get display value

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_display_value`

**Inputs** filters, group\_by\_field, item.

**Explicit results** value.

**Local steps**

- If filters.get(“group\_by”) equals “Item”.
  - If item.get(“item\_code”) differs from item.get(“item\_name”).
    - Set value from formatted text {item.get(“item\_code”)}: {item.get(“item\_name”)}.
  - Otherwise.
    - Set value from item.get(“item\_code”, empty text).
- Otherwise.
  - If filters.get(“group\_by”) belongs to tuple(“Customer”, “Supplier”).
    - Set party from Platform.scrub(filters.get(“group\_by”)).
    - If item.get(party) differs from item.get((party + “\_name”)).
      - Set value from formatted text {item.get(party)}: {item.get((party + “\_name”))}.
    - Otherwise.
      - Set value from item.get(party).
  - Otherwise.
    - Set value from item.get(group\_by\_field).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0266.json#L3410) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1113)

<a id="op-a2fd78fd38f0ef"></a>
### Get group by and display fields

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_get_group_by_and_display_fields`

**Inputs** filters.

**Explicit results** tuple(group\_by\_field, subtotal\_display\_field).

**Local steps**

- If filters.get(“group\_by”) equals “Item”.
  - Set group\_by\_field from “item\_code”.
  - Set subtotal\_display\_field from “invoice”.
- Otherwise.
  - If filters.get(“group\_by”) equals “Invoice”.
    - Set group\_by\_field from “parent”.
    - Set subtotal\_display\_field from “item\_code”.
  - Otherwise.
    - Set group\_by\_field from Platform.scrub(filters.get(“group\_by”)).
    - Set subtotal\_display\_field from “item\_code”.
- Return tuple(group\_by\_field, subtotal\_display\_field).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0266.json#L3996) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L773) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1115)

<a id="op-abd0edc1bbcc95"></a>
### Add sub total row

`operation_enterprise_accounts_report_item_wise_sales_register_business_behavior_add_subordinate_total_row`

**Inputs** item, total\_row\_map, group\_by\_value, tax\_columns.

**Local steps**

- Set total\_row from total\_row\_map.get(group\_by\_value).
- Update total\_row at “stock\_qty” using + item at “stock\_qty”.
- Update total\_row at “amount” using + item at “amount”.
- Update total\_row at “total\_tax” using + item at “total\_tax”.
- Update total\_row at “total\_other\_charges” using + flt(item.get(“total\_other\_charges”)).
- Update total\_row at “total” using + item at “total”.
- Update total\_row at “percent\_gt” using + item at “percent\_gt”.
- For each tax in tax\_columns.
  - Evaluate total\_row.setdefault(formatted text {tax}\_amount, 0.0).
  - Update total\_row at formatted text {tax}\_amount using + flt(item at formatted text {tax}\_amount).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1105)

## Record · Journal entry

[Record definition](../../../../data/record-types/journal_entry.json)

<a id="op-f2ce926a84572c"></a>
### Journal Entry.initialize

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0061.json#L6555) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1124)

<a id="op-4437fecd3c8656"></a>
### Journal Entry.validate

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate`

**Inputs** self.

**Local steps**

- <a id="op-4437fecd3c8656-guard-2"></a>If self.voucher\_type equals “Opening Entry”.
  - Set self.is\_opening from “Yes”.
- If not self.is\_opening.
  - Set self.is\_opening from “No”.
- If self.is\_opening equals “Yes”.
  - Evaluate validate\_opening\_entry\_against\_pcv(self.company).
- Set self.clearance\_date from no value.
- Evaluate self.validate\_account\_company().
- Evaluate self.validate\_party().
- Evaluate self.ensure\_supplier\_is\_not\_blocked().
- Evaluate self.validate\_entries\_for\_advance().
- Evaluate self.validate\_multi\_currency().
- Evaluate self.set\_amounts\_in\_company\_currency().
- Evaluate self.validate\_debit\_credit\_amount().
- Evaluate self.set\_total\_debit\_credit().
- If not Platform.flags.is\_reverse\_depr\_entry.
  - Evaluate self.validate\_against\_jv().
  - Evaluate self.validate\_stock\_accounts().
- Evaluate self.validate\_reference\_doc().
- If self.docstatus equals 0.
  - Evaluate self.set\_against\_account().
- Evaluate self.create\_remarks().
- Evaluate self.set\_print\_format\_fields().
- Evaluate self.validate\_credit\_debit\_note().
- Evaluate self.validate\_empty\_accounts\_table().
- Evaluate self.validate\_inter\_company\_accounts().
- Evaluate self.validate\_depr\_account\_and\_depr\_entry\_voucher\_type().
- Evaluate self.validate\_company\_in\_accounting\_dimension().
- Evaluate self.validate\_advance\_accounts().
- Evaluate JournalTaxWithholding(self).on\_validate().
- If (not self.title or (self.is\_new() and self.amended\_from)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.title → (self.is\_new() and self.amended\_from).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.amended\_from.
  - Set self.title from self.get\_title().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.voucher\_type equals “Opening Entry”, self.voucher\_type = “Opening Entry” selects the branch that assigns “Yes” to self.is\_opening. With self.voucher\_type = “Journal Entry”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-4437fecd3c8656-guard-2)

**Methods declared on this owner** [validate account company](operations-055.md#op-b25a41a12f9432), [validate party](operations-056.md#op-88d6351c134d8e), [validate entries for advance](operations-056.md#op-4953636b95e8be), [validate multi currency](operations-057.md#op-79b67fa98d3e46), [set amounts in company currency](operations-057.md#op-2d8efb445635b0), [validate debit credit amount](operations-057.md#op-a02cd4d3977469), [set total debit credit](operations-057.md#op-037540bec72f17), [validate against jv](operations-057.md#op-f785f1746bc81a), [validate stock accounts](operations-056.md#op-71f928ca8d06c9), [validate reference doc](operations-057.md#op-9c9dfd1b26c980), [set against account](operations-057.md#op-ff05d785ce3a81), [create remarks](operations-057.md#op-c963c6b4bcd0ce), [set print format fields](operations-057.md#op-77ef939269fb52), [validate credit debit note](operations-057.md#op-4e1606f7dbac32), [validate empty accounts table](operations-057.md#op-7175d9d60b9163), [validate inter company accounts](operations-056.md#op-2731739197ca38), [validate depr account and depr entry voucher type](operations-056.md#op-22a3a2c67d1c16), [validate advance accounts](operations-055.md#op-16e2f96a9bc2fa), [get title](operations-056.md#op-6c32dd88edac91).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1141)

<a id="op-b25a41a12f9432"></a>
### Journal Entry.validate account company

`operation_enterprise_binding_enterprise_accounts_doctype_journal_entry_journal_entry_journalentry_validate_account_company`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.company.
  - Return no value.
- For each d in self.get(“accounts”).
  - If d.account.
    - Evaluate validate\_account\_head(d.idx, d.account, self.company, translated “Journal Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L811)

<a id="op-16e2f96a9bc2fa"></a>
### Journal Entry.validate advance accounts

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_advance_accounts`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**State and service calls** msgprint with translated “Making Journal Entries against advance accounts: {0} is not recommended. These Journals won't be available f …”.format(Platform.bold(comma\_and(advance\_accounts\_used))).

**Local steps**

- Set journal\_accounts from set(list of x.account for x drawn from self.accounts).
  - Draw x from self.accounts.
- Set advance\_accounts from set().
- Evaluate advance\_accounts.add(Platform.get\_cached\_value(“Company”, self.company, “default\_advance\_received\_account”)).
- Evaluate advance\_accounts.add(Platform.get\_cached\_value(“Company”, self.company, “default\_advance\_paid\_account”)).
- If advance\_accounts\_used bound to (journal\_accounts bitwise and advance\_accounts).
  - Evaluate Platform.msgprint(translated “Making Journal Entries against advance accounts: {0} is not recommended. These Journals won't be available f …”.format(Platform.bold(comma\_and(advance\_accounts\_used)))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_advance\_received\_account”), Platform.get\_cached\_value(“Company”, self.company, “default\_advance\_paid\_account”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1142)

<a id="op-7199c0c314ae66"></a>
### Journal Entry.validate for repost

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_for_repost`

**Inputs** self.

**Local steps**

- Evaluate validate\_docs\_for\_voucher\_types(list(“Journal Entry”)).
- Evaluate validate\_docs\_for\_deferred\_accounting(list(self.name), list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L340) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1222) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1150)

<a id="op-e68d25cab193a7"></a>
### Journal Entry.submit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_submit`

**Inputs** self.

**Explicit results** self.\_submit().

**Local steps**

- If (len(self.accounts) &gt; 100 and not self.meta.queue\_in\_background).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(self.accounts) &gt; 100 → not self.meta.queue\_in\_background.
  - Evaluate queue\_submission(self, “\_submit”).
- Otherwise.
  - Return self.\_submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L438) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1207) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1135)

<a id="op-5ffa2a9dcc09e2"></a>
### Journal Entry.before cancel

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_before_cancel`

**Inputs** self.

**Local steps**

- Evaluate self.has\_asset\_adjustment\_entry().

If control reaches the end, it returns no value.

**Methods declared on this owner** [has asset adjustment entry](operations-056.md#op-7c3c06648dc4be).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1112)

<a id="op-188eccaf8406ac"></a>
### Journal Entry.cancel

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_cancel`

**Inputs** self.

**Explicit results** self.\_cancel().

**Local steps**

- If (len(self.accounts) &gt; 100 and not self.meta.queue\_in\_background).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(self.accounts) &gt; 100 → not self.meta.queue\_in\_background.
  - Evaluate queue\_submission(self, “\_cancel”).
- Otherwise.
  - Return self.\_cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1115)

<a id="op-b157dd11e27100"></a>
### Journal Entry.before submit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_before_submit`

**Inputs** self.

**Local steps**

- If not Platform.flags.in\_import.
  - Evaluate self.validate\_total\_debit\_and\_credit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate total debit and credit](operations-057.md#op-6e9eb3aba72aab).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L759) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1113)

<a id="op-6abaf5375da564"></a>
### Journal Entry.on submit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_cheque\_info().
- Evaluate self.make\_gl\_entries().
- Evaluate self.check\_credit\_limit().
- Evaluate self.update\_asset\_value().
- Evaluate self.update\_inter\_company\_jv().
- Evaluate self.update\_invoice\_discounting().
- Evaluate JournalTaxWithholding(self).on\_submit().
- Evaluate self.update\_payment\_order\_requests().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate cheque info](operations-056.md#op-aa19229c7343f8), [make gl entries](operations-057.md#op-cfdfd9f84a32e5), [check credit limit](operations-056.md#op-2449017fec857f), [update asset value](operations-056.md#op-f20ca267d0e9fa), [update inter company jv](operations-056.md#op-7805b35026630a), [update invoice discounting](operations-056.md#op-987035d50c80c7), [update payment order requests](operations-056.md#op-6aaa63e2185718).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L113) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1127)

<a id="op-03d5396ef53b7b"></a>
### Journal Entry.get balance for periodic accounting

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_get_balance_for_periodic_accounting`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “No difference found for stock account {0}”.format(Platform.bold(account)).

**Local steps**

- Evaluate self.validate\_company\_for\_periodic\_accounting().
- Set stock\_accounts from self.get\_stock\_accounts\_for\_periodic\_accounting().
- Evaluate self.set(“accounts”, list()).
- For each account in stock\_accounts.
  - Set tuple(account\_bal, stock\_bal, warehouse\_list) from get\_stock\_and\_account\_balance(account, self.posting\_date, self.company).
  - Set difference\_value from flt((stock\_bal − account\_bal), self.precision(“difference”)).
  - If difference\_value equals 0.
    - Evaluate Platform.msgprint(translated “No difference found for stock account {0}”.format(Platform.bold(account)), alert = true).
    - Continue with the next iteration or loop test.
  - Evaluate self.append(“accounts”, mapping(“account” → account, “debit\_in\_account\_currency” → difference\_value when difference\_value &gt; 0, otherwise 0, “credit\_in\_account\_currency” → abs(difference\_value) when differe ….
    - Value choice on difference\_value &gt; 0 — true gives difference\_value, false gives 0.
    - Value choice on difference\_value &lt; 0 — true gives abs(difference\_value), false gives 0.
  - Evaluate self.append(“accounts”, mapping(“account” → self.periodic\_entry\_difference\_account, “credit\_in\_account\_currency” → difference\_value when difference\_value &gt; 0, otherwise 0, “debit\_in\_account\_currency” → abs ….
    - Value choice on difference\_value &gt; 0 — true gives difference\_value, false gives 0.
    - Value choice on difference\_value &lt; 0 — true gives abs(difference\_value), false gives 0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate company for periodic accounting](operations-055.md#op-6bc7747b29e148), [get stock accounts for periodic accounting](operations-055.md#op-513bd2ca361f77).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1119)

<a id="op-6bc7747b29e148"></a>
### Journal Entry.validate company for periodic accounting

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_validate_company_for_periodic_accounting`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Periodic Accounting Entry is not allowed for company {0} with perpetual inventory enabled”.format(self.company) · validation helper — translated “Please select Periodic Accounting Entry Difference Account”.

**Local steps**

- If Enterprise.is\_perpetual\_inventory\_enabled(self.company).
  - Call the validation error handler Platform.throw(translated “Periodic Accounting Entry is not allowed for company {0} with perpetual inventory enabled”.format(self.company)).
- If not self.periodic\_entry\_difference\_account.
  - Call the validation error handler Platform.throw(translated “Please select Periodic Accounting Entry Difference Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L1751) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1145)

<a id="op-513bd2ca361f77"></a>
### Journal Entry.get stock accounts for periodic accounting

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_get_stock_accounts_for_periodic_accounting`

**Inputs** self.

**Record and data access** read “Account” via get\_all.

**Explicit results** list() · Platform.get\_all(“Account”, filters = mapping(“company” → self.company, “account\_type” → “Stock”, “root\_type” → “Asset”, “is\_group” → 0), pluck = “name”) · list(self.stock\_asset\_account).

**Explicit failure paths** validation helper — translated “Please select Stock Asset Account”.

**Local steps**

- <a id="op-513bd2ca361f77-guard-2"></a>If self.voucher\_type differs from “Periodic Accounting Entry”.
  - Return list().
- If self.for\_all\_stock\_asset\_accounts.
  - Return Platform.get\_all(“Account”, filters = mapping(“company” → self.company, “account\_type” → “Stock”, “root\_type” → “Asset”, “is\_group” → 0), pluck = “name”).
- If not self.stock\_asset\_account.
  - Call the validation error handler Platform.throw(translated “Please select Stock Asset Account”).
- Return list(self.stock\_asset\_account).

**Derived branch illustrations**

- At the comparison self.voucher\_type differs from “Periodic Accounting Entry”, self.voucher\_type = “Journal Entry” selects the branch that returns list(). With self.voucher\_type = “Periodic Accounting Entry”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-513bd2ca361f77-guard-2)

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0062.json#L1929) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1121)

<a id="op-39cbea8fdd57c9"></a>
### Journal Entry.on update after submit

`operation_enterprise_accounts_record_definitions_journal_entry_business_behavior_journal_entry_on_update_after_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.flags.get(“ignore\_reposting\_on\_reconciliation”).
  - Return no value.
- Set needs\_repost from self.check\_if\_fields\_updated(fields\_to\_check = list(), child\_tables = mapping(“accounts” → list())).
- If needs\_repost.
  - Evaluate self.validate\_for\_repost().
  - Evaluate self.repost\_accounting\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for repost](operations-055.md#op-7199c0c314ae66).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1199) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L1128)
