# Accounting and settlement · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank statement import log

[Record definition](../../../../data/record-types/bank_statement_import_log.json)

<a id="op-6ba07318d07de3"></a>
### Bank Statement Import Log.get pdf tables

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_portable_document_tables`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** list() · json.loads(self.pdf\_tables) · self.pdf\_tables.

**Local steps**

- If not self.pdf\_tables.
  - Return list().
- If isinstance(self.pdf\_tables, str).
  - Return json.loads(self.pdf\_tables).
- Return self.pdf\_tables.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L1462) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L362) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L342)

<a id="op-f98980b5f9f96e"></a>
### Bank Statement Import Log.prepare pdf tables

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_prepare_portable_document_tables`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** tables.

**Local steps**

- Set content from self.get\_file\_doc().get\_content().
- Set password from self.get\_statement\_password().
- Set tables from extract\_pdf\_tables(content, password).
- Set pages from set of table at “page” for table drawn from tables.
  - Draw table from tables.
- Set page\_images from render\_pdf\_pages(content, password, pages).
- Set self.flags.\_pending\_page\_images from mapping of page → png for tuple(page, tuple(png, \_scale)) drawn from page\_images.items().
  - Draw tuple(page, tuple(png, \_scale)) from page\_images.items().
- Set page\_scales from mapping of page → scale for tuple(page, tuple(\_png, scale)) drawn from page\_images.items().
  - Draw tuple(page, tuple(\_png, scale)) from page\_images.items().
- For each table in tables.
  - Set table at “page\_image” from no value.
  - Set table at “render\_scale” from page\_scales.get(table at “page”).
  - Set tuple(header\_index, score) from detect\_header\_row(table at “rows”).
  - If score ≥ 2.
    - Set table at “header\_index” from header\_index.
    - Set table at “column\_mapping” from detect\_column\_mapping(table at “rows” at header\_index).
  - Otherwise.
    - Set table at “header\_index” from no value.
    - Set table at “column\_mapping” from guess\_column\_mapping\_by\_content(table at “rows”).
  - Set tuple(final\_transactions, table at “date\_format”, table at “amount\_format”) from build\_table\_transactions(table).
  - Set table at “included” from should\_include\_table(table, final\_transactions).
- Set self.pdf\_tables from json.dumps(tables).
- Return tables.

**Methods declared on this owner** [get file doc](operations-016.md#op-a9c8d6ce34460f), [get statement password](operations-016.md#op-ed5fc753fee9ec).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L1598) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L367) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L347)

<a id="op-32b9e194c21c8d"></a>
### Bank Statement Import Log.attach pdf page images

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_attach_portable_document_page_images`

**Inputs** self.

**State and service calls** call db\_set on self.

**Explicit results** no value.

**Local steps**

- Set pending from getattr(self.flags, “\_pending\_page\_images”, no value).
- If not pending.
  - Return no value.
- Set page\_urls from mapping of page → self.save\_page\_image(png, page) for tuple(page, png) drawn from pending.items().
  - Draw tuple(page, png) from pending.items().
- Set tables from self.get\_pdf\_tables().
- For each table in tables.
  - Set table at “page\_image” from page\_urls.get(table at “page”).
- Evaluate self.db\_set(“pdf\_tables”, json.dumps(tables), update\_modified = false).
- Set self.flags.\_pending\_page\_images from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [save page image](operations-017.md#op-7808f20ce40136), [get pdf tables](operations-017.md#op-6ba07318d07de3).

**Values supplied outside this operation** selected callable from getattr(self.flags, “\_pending\_page\_images”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L2387) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L334)

<a id="op-7808f20ce40136"></a>
### Bank Statement Import Log.save page image

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_save_page_image`

**Inputs** self, png\_bytes, page\_number.

**Declared result** str.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → formatted text statement-{self.name}-page-{page\_number}.png, “is\_private” → 1, “content” → png\_bytes, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → formatted text statement-{self.name}-page-{page\_number}.png, “is\_private” → 1, “content” → png\_bytes, …)).

**Explicit results** Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → formatted text statement-{nested operand in the contract.name}-page-{page\_number}.png, “is\_private” → 1, “content” → png\_bytes, …)).insert(ignore\_ ….

**Local steps**

- Return Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → formatted text statement-{nested operand in the contract.name}-page-{page\_number}.png, “is\_private” → 1, “content” → png\_bytes, …)).insert(ignore\_ ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L2719) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L369) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L349)

<a id="op-76b500733188bf"></a>
### Bank Statement Import Log.get pdf final transactions

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_portable_document_final_transactions`

**Inputs** self.

**Declared result** list at dict.

**Explicit results** final\_transactions.

**Local steps**

- Set final\_transactions from list().
- For each table in self.get\_pdf\_tables().
  - If not table.get(“included”, true).
    - Continue with the next iteration or loop test.
  - Set tuple(table\_transactions, \_df, \_af) from build\_table\_transactions(table).
  - Evaluate final\_transactions.extend(table\_transactions).
- Return final\_transactions.

**Methods declared on this owner** [get pdf tables](operations-017.md#op-6ba07318d07de3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L2977) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L361) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L341)

<a id="op-8a08b6b14f333e"></a>
### Bank Statement Import Log.set pdf summary

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_portable_document_summary`

**Inputs** self, tables.

**Declared result** list at dict.

**Explicit results** final\_transactions.

**Local steps**

- Set final\_transactions from list().
- Set date\_format from no value.
- Set amount\_format from no value.
- For each table in tables.
  - If not table.get(“included”, true).
    - Continue with the next iteration or loop test.
  - Set tuple(table\_transactions, df, af) from build\_table\_transactions(table).
  - Evaluate final\_transactions.extend(table\_transactions).
  - If (table\_transactions and date\_format is identical to no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_transactions → date\_format is identical to no value.
    - Set tuple(date\_format, amount\_format) from tuple(df, af).
- Set self.detected\_date\_format from (date\_format or “%d/%m/%Y”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in date\_format → “%d/%m/%Y”.
- Set self.detected\_amount\_format from (amount\_format or “Separate columns for withdrawal and deposit”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in amount\_format → “Separate columns for withdrawal and deposit”.
- Set self.number\_of\_transactions from len(final\_transactions).
- Set total\_debits, total\_credits from 0.
- Set debit\_transactions, credit\_transactions from 0.
- Set start\_date, end\_date from no value.
- Set closing\_balance from no value.
- For each transaction in final\_transactions.
  - Set withdrawal from (transaction.get(“withdrawal”, 0) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction.get(“withdrawal”, 0) → 0.
  - Set deposit from (transaction.get(“deposit”, 0) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction.get(“deposit”, 0) → 0.
  - If withdrawal &gt; 0.
    - Update total\_debits using + withdrawal.
    - Update debit\_transactions using + 1.
  - If deposit &gt; 0.
    - Update total\_credits using + deposit.
    - Update credit\_transactions using + 1.
  - Set date from transaction.get(“date”).
  - If not date.
    - Continue with the next iteration or loop test.
  - Set tx\_date from getdate(date).
  - If (start\_date is identical to no value or tx\_date &lt; start\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in start\_date is identical to no value → tx\_date &lt; start\_date.
    - Set start\_date from tx\_date.
  - If (end\_date is identical to no value or tx\_date ≥ end\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in end\_date is identical to no value → tx\_date ≥ end\_date.
    - Set end\_date from tx\_date.
    - Set closing\_balance from transaction.get(“balance”).
- Set self.total\_debits from total\_debits.
- Set self.total\_credits from total\_credits.
- Set self.total\_debit\_transactions from debit\_transactions.
- Set self.total\_credit\_transactions from credit\_transactions.
- Set self.start\_date from getdate(start\_date) when start\_date, otherwise no value.
  - Value choice on start\_date — true gives getdate(start\_date), false gives no value.
- Set self.end\_date from getdate(end\_date) when end\_date, otherwise no value.
  - Value choice on end\_date — true gives getdate(end\_date), false gives no value.
- Set self.closing\_balance from get\_float\_amount(closing\_balance).
- Return final\_transactions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L3169) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L376) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L356)

<a id="op-36bb0846b62763"></a>
### Bank Statement Import Log.apply pdf tables

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_apply_portable_document_tables`

**Inputs** self, tables.

**State and service calls** call save on self.

**Local steps**

- Set self.pdf\_tables from json.dumps(tables).
- Evaluate self.set\_pdf\_summary(tables).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set pdf summary](operations-017.md#op-8a08b6b14f333e).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L4204) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L353) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L333)

<a id="op-7fe382967db4c1"></a>
### Bank Statement Import Log.insert transactions

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_insert_transactions`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank Account” via get\_value · read “Account” via get\_value · resolve a document from mapping(“doctype” → “Bank Transaction”, “date” → transaction.get(“date”), “status” → “Unreconciled”, “bank\_account” → self.bank\_account, …) via get\_doc.

**State and service calls** call insert on bank\_tx · call submit on bank\_tx · publish realtime with “bank-rec-statement-import-progress” · call save on self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The bank account is not a company account. Please select a company account” · validation helper — translated “The bank account is disabled. Please enable it”.

**Local steps**

- <a id="op-7fe382967db4c1-guard-2"></a>If self.status equals “Completed”.
  - Return no value.
- Set tuple(company, account, is\_company\_account, disabled) from Platform.get\_value(“Bank Account”, self.bank\_account, list(“company”, “account”, “is\_company\_account”, “disabled”)).
- If not is\_company\_account.
  - Call the validation error handler Platform.throw(translated “The bank account is not a company account. Please select a company account”, title = translated “Invalid Bank Account”).
- If disabled.
  - Call the validation error handler Platform.throw(translated “The bank account is disabled. Please enable it”, title = translated “Disabled Bank Account”).
- Set currency from Platform.get\_value(“Account”, account, “account\_currency”).
- Set progress from 0.
- If self.is\_pdf().
  - Set final\_transactions from self.get\_pdf\_final\_transactions().
- Otherwise.
  - Set raw\_data from self.get\_data().
  - Set tuple(transaction\_rows, \_starting\_index, \_ending\_index) from self.get\_transaction\_rows(raw\_data).
  - Set final\_transactions from self.get\_final\_transactions(transaction\_rows = transaction\_rows).
- Set total\_transactions from len(final\_transactions).
- For each transaction in final\_transactions.
  - Set bank\_tx from Platform.get\_doc(mapping(“doctype” → “Bank Transaction”, “date” → transaction.get(“date”), “status” → “Unreconciled”, “bank\_account” → self.bank\_account, …)).
  - Evaluate bank\_tx.insert().
  - Evaluate bank\_tx.submit().
  - Update progress using + 1.
  - Evaluate Platform.publish\_realtime(“bank-rec-statement-import-progress”, mapping(“progress” → round(((progress ÷ total\_transactions) × 100)), “current” → progress, “total” → total\_transactions), doctype = “Bank Sta ….
- Evaluate Platform.publish\_realtime(“bank-rec-statement-import-progress”, mapping(“progress” → 100, “current” → total\_transactions, “total” → total\_transactions), doctype = “Bank Statement Import Log”, docname = self.name).
- If (self.closing\_balance is distinct from no value and self.end\_date).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.closing\_balance is distinct from no value → self.end\_date.
  - Evaluate \_set\_closing\_balance\_as\_per\_statement(self.bank\_account, Platform.utils.getdate(self.end\_date), self.closing\_balance).
- Bind dependencies run\_rule\_evaluation.
- Evaluate run\_rule\_evaluation().
- Set self.status from “Completed”.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.status equals “Completed”, self.status = “Completed” selects the branch that returns no value. With self.status = “Not Started”, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-7fe382967db4c1-guard-2)

**Methods declared on this owner** [is pdf](operations-016.md#op-a43eca0db5e9a0), [get pdf final transactions](operations-017.md#op-76b500733188bf), [get data](operations-016.md#op-cc4ae66e9b9d44), [get transaction rows](operations-016.md#op-23ce0114ade565), [get final transactions](operations-016.md#op-cdc54186a95e8d).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“bank-rec-statement-import-progress”, mapping(“progress” → round(((progress ÷ total\_transactions) × 100)), “current” → progress, “total” → total\_transactions), doctype = “Bank Sta …, Platform.publish\_realtime(“bank-rec-statement-import-progress”, mapping(“progress” → 100, “current” → total\_transactions, “total” → total\_transactions), doctype = “Bank Statement Import Log”, docname = self.name).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L365) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L345)

<a id="op-cf0a4ca02aed61"></a>
### Detect header row

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_detect_header_row`

**Inputs** data.

**Declared result** tuple at tuple(int, int).

**Explicit results** tuple(row\_index, max\_valid\_columns).

**Local steps**

- Set row\_index from 0.
- Set max\_valid\_columns from 0.
- For each tuple(idx, row) in enumerate(data).
  - Set valid\_columns from 0.
  - For each cell in row.
    - If (not cell or not isinstance(cell, str)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cell → not isinstance(cell, str).
      - Continue with the next iteration or loop test.
    - If any(generator of keyword belongs to cell.lower() for keyword drawn from HEADER\_KEYWORDS).
      - Draw keyword from HEADER\_KEYWORDS.
      - Update valid\_columns using + 1.
  - If valid\_columns &gt; max\_valid\_columns.
    - Set max\_valid\_columns from valid\_columns.
    - Set row\_index from idx.
- Return tuple(row\_index, max\_valid\_columns).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L5724) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L385) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L365)

<a id="op-bf64bea818d866"></a>
### Detect column mapping

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_detect_column_mapping`

**Inputs** header\_row.

**Declared result** list at dict.

**Explicit results** columns.

**Local steps**

- Set column\_mapping from mapping().
- Set columns from list().
- For each tuple(idx, cell) in enumerate(header\_row).
  - If (not cell or not isinstance(cell, str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cell → not isinstance(cell, str).
    - Continue with the next iteration or loop test.
  - Set column from mapping(“index” → idx, “header\_text” → cell, “variable” → nested operand in the contract.replace(one space, “\_”).replace(“?”, empty text).replace(“.”, empty text), “maps\_to” → “Do not import”).
  - For each tuple(standard\_variable, names) in STANDARD\_VARIABLES.items().
    - If any(generator of name belongs to nested operand in the contract.lower().replace(“.”, empty text) for name drawn from names).
      - Draw name from names.
      - If column\_mapping.get(standard\_variable, no value) is identical to no value.
        - Set column at “maps\_to” from standard\_variable.
        - Set column\_mapping at standard\_variable from idx.
        - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate columns.append(column).
- Return columns.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L6063) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L384) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L364)

<a id="op-e829da26b9ec8f"></a>
### Is meaningful mapping

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_is_meaningful_mapping`

**Inputs** columns.

**Declared result** bool.

**Explicit results** any(generator of (col.get(“maps\_to”) and col at “maps\_to” differs from “Do not import”) for col drawn from columns).

**Local steps**

- Return any(generator of (col.get(“maps\_to”) and col at “maps\_to” differs from “Do not import”) for col drawn from columns).
  - Draw col from columns.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.get(“maps\_to”) → col at “maps\_to” differs from “Do not import”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L6613) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L395) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L375)

<a id="op-319eb755966fb1"></a>
### Guess column mapping by content

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_guess_column_mapping_by_content`

**Inputs** rows.

**Declared result** list at dict.

**Explicit results** list of mapping(“index” → idx, “header\_text” → empty text, “variable” → formatted text column\_{idx}, “maps\_to” → mapping.get(idx, “Do not import”)) for idx drawn from range(num\_cols).

**Local steps**

- Set num\_cols from max(generator of len(row) for row drawn from rows, default = 0).
  - Draw row from rows.
- Set column\_stats from list().
- For each idx in range(num\_cols).
  - Set cells from list of row at idx for row drawn from rows where (idx &lt; len(row) and str(nested operand in the contract at nested operand in the contract).strip() differs from empty text).
    - Draw row from rows, keep a combination only if ((idx &lt; len(row) and str(row at idx).strip() differs from empty text)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in idx &lt; len(row) → str(row at idx).strip() differs from empty text.
  - Set count from len(cells).
  - If not count.
    - Evaluate column\_stats.append(mapping(“index” → idx, “date\_ratio” → 0, “num\_ratio” → 0, “avg\_len” → 0, …)).
    - Continue with the next iteration or loop test.
  - Set date\_hits from sum(generator of 1 for c drawn from cells where (isinstance(c, str) and Platform.utils.guess\_date\_format(c))).
    - Draw c from cells, keep a combination only if ((isinstance(c, str) and Platform.utils.guess\_date\_format(c))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(c, str) → Platform.utils.guess\_date\_format(c).
  - Set num\_hits from sum(generator of 1 for c drawn from cells where get\_float\_amount(c) is distinct from no value).
    - Draw c from cells, keep a combination only if (get\_float\_amount(c) is distinct from no value).
  - Set avg\_len from (sum(generator of len(str(c)) for c drawn from cells) ÷ count).
    - Draw c from cells.
  - Evaluate column\_stats.append(mapping(“index” → idx, “date\_ratio” → (date\_hits ÷ count), “num\_ratio” → (num\_hits ÷ count), “avg\_len” → avg\_len, …)).
- Set mapping from mapping().
- Set numeric\_cols from list().
- Set date\_assigned from false.
- For each stat in column\_stats.
  - If stat at “count” equals 0.
    - Continue with the next iteration or loop test.
  - If (not date\_assigned and stat at “date\_ratio” ≥ 0.6).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not date\_assigned → stat at “date\_ratio” ≥ 0.6.
    - Set mapping at stat at “index” from “Date”.
    - Set date\_assigned from true.
  - Otherwise.
    - If stat at “num\_ratio” ≥ 0.6.
      - Evaluate numeric\_cols.append(stat at “index”).
- Set text\_cols from list of s for s drawn from column\_stats where (s at “count” and s at “index” does not belong to mapping and s at “index” does not belong to numeric\_cols).
  - Draw s from column\_stats, keep a combination only if ((s at “count” and s at “index” does not belong to mapping and s at “index” does not belong to numeric\_cols)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in s at “count” → s at “index” does not belong to mapping → s at “index” does not belong to numeric\_cols.
- If text\_cols.
  - Set mapping at max(text\_cols, key = deferred anonymous expression) at “index” from “Description”.
- If len(numeric\_cols) equals 1.
  - Set mapping at numeric\_cols at 0 from “Amount”.
- Return list of mapping(“index” → idx, “header\_text” → empty text, “variable” → formatted text column\_{idx}, “maps\_to” → mapping.get(idx, “Do not import”)) for idx drawn from range(num\_cols).
  - Draw idx from range(num\_cols).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L394) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L374)

<a id="op-39e36e97717c93"></a>
### Extract transaction rows

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_extract_transaction_rows`

**Inputs** data, column\_mapping, header\_index.

**Explicit results** tuple(transaction\_rows, transaction\_starting\_index, transaction\_ending\_index).

**Local steps**

- If header\_index is identical to no value.
  - Set header\_index from negative 1.
- Bind local operation cell for subsequent calls.
- Set transaction\_rows from list().
- Set transaction\_starting\_index from no value.
- Set transaction\_ending\_index from no value.
- Set valid\_rows from data at slice (header\_index + 1) to no value.
- For each tuple(row\_index, row) in enumerate(valid\_rows).
  - Set date from cell(row, “Date”).
  - Set amount from cell(row, “Amount”).
  - Set withdrawal from cell(row, “Withdrawal”).
  - Set deposit from cell(row, “Deposit”).
  - If not date.
    - Continue with the next iteration or loop test.
  - If isinstance(date, datetime).
    - Set date from date.strftime(“%Y-%m-%d”).
  - If not isinstance(date, str).
    - Continue with the next iteration or loop test.
  - If (not amount and not withdrawal and not deposit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not amount → not withdrawal → not deposit.
    - Continue with the next iteration or loop test.
  - Set row\_date\_format from Platform.utils.guess\_date\_format(date).
  - If not row\_date\_format.
    - Continue with the next iteration or loop test.
  - Set amount from get\_float\_amount(amount).
  - Set withdrawal from get\_float\_amount(withdrawal).
  - Set deposit from get\_float\_amount(deposit).
  - If (not amount and not withdrawal and not deposit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not amount → not withdrawal → not deposit.
    - Continue with the next iteration or loop test.
  - If transaction\_starting\_index is identical to no value.
    - Set transaction\_starting\_index from row\_index.
  - Set transaction\_ending\_index from row\_index.
  - Set transaction\_row from mapping(“date\_format” → row\_date\_format).
  - For each tuple(source\_field, target\_field) in FIELD\_MAP.items().
    - If source\_field belongs to column\_mapping.
      - Set transaction\_row at target\_field from cell(row, source\_field).
  - Evaluate transaction\_rows.append(transaction\_row).
- Set base\_index from (header\_index + 1).
- If transaction\_starting\_index is distinct from no value.
  - Update transaction\_starting\_index using + base\_index.
- If transaction\_ending\_index is distinct from no value.
  - Update transaction\_ending\_index using + base\_index.
- Return tuple(transaction\_rows, transaction\_starting\_index, transaction\_ending\_index).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L1395) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L368)

<a id="op-cc59be5a23a9fc"></a>
### Extract transaction rows.cell

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_extract_transaction_rows_cell`

**Inputs** row, key.

**Explicit results** no value · row at idx.

**Local steps**

- Set idx from column\_mapping.get(key).
- If (idx is identical to no value or idx ≥ len(row)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in idx is identical to no value → idx ≥ len(row).
  - Return no value.
- Return row at idx.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L2492) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L389) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L369)

<a id="op-2af8fe4b0e049d"></a>
### Compute final transactions

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_compute_final_transactions`

**Inputs** transaction\_rows, date\_format, amount\_format.

**Declared result** list.

**Explicit results** final\_transactions.

**Local steps**

- Set final\_transactions from list().
- Set unmarked\_is\_deposit from false.
- If amount\_format equals “Amount column has "CR"/"DR" values”.
  - Set markers from set of get\_amount\_cr\_dr\_marker(row.get(“amount”)) for row drawn from transaction\_rows.
    - Draw row from transaction\_rows.
  - Set unmarked\_is\_deposit from (markers − set(no value)) equals set(“dr”).
- Bind local operation parse\_amount for subsequent calls.
- For each transaction in transaction\_rows.
  - Set date from transaction.get(“date”).
  - If isinstance(date, datetime).
    - Set date from date.strftime(“%Y-%m-%d”).
  - Otherwise.
    - Set date from datetime.strptime(date, date\_format).strftime(“%Y-%m-%d”).
  - Set tuple(withdrawal, deposit) from parse\_amount(transaction).
  - Evaluate final\_transactions.append(mapping(expand transaction, “date” → date, “withdrawal” → withdrawal, “deposit” → deposit)).
- Return final\_transactions.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L2634) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L362)

<a id="op-4b5dcb5b08b1b7"></a>
### Compute final transactions.parse amount

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_compute_final_transactions_parse_amount`

**Inputs** transaction\_row.

**Explicit results** tuple(get\_float\_amount(transaction\_row.get(“withdrawal”)), get\_float\_amount(transaction\_row.get(“deposit”))) · tuple(0, abs(signed\_amount)) when marker equals “cr”, otherwise tuple(abs(signed\_amount), 0) · tuple(0, abs(signed\_amount)) when is\_deposit, otherwise tuple(abs(signed\_amount), 0) · tuple(0, abs(amount)) · tuple(abs(amount), 0) · 4 additional forms in the steps below.

**Local steps**

- If amount\_format equals “Separate columns for withdrawal and deposit”.
  - Return tuple(get\_float\_amount(transaction\_row.get(“withdrawal”)), get\_float\_amount(transaction\_row.get(“deposit”))).
- If amount\_format equals “Amount column has "CR"/"DR" values”.
  - Set amount from transaction\_row.get(“amount”).
  - Set marker from get\_amount\_cr\_dr\_marker(amount).
  - Set signed\_amount from (get\_float\_amount(amount) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_float\_amount(amount) → 0.
  - If marker.
    - Return tuple(0, abs(signed\_amount)) when marker equals “cr”, otherwise tuple(abs(signed\_amount), 0).
      - Value choice on marker equals “cr” — true gives tuple(0, abs(signed\_amount)), false gives tuple(abs(signed\_amount), 0).
  - Set is\_deposit from unmarked\_is\_deposit.
  - If signed\_amount &lt; 0.
    - Set is\_deposit from not is\_deposit.
  - Return tuple(0, abs(signed\_amount)) when is\_deposit, otherwise tuple(abs(signed\_amount), 0).
    - Value choice on is\_deposit — true gives tuple(0, abs(signed\_amount)), false gives tuple(abs(signed\_amount), 0).
- If amount\_format equals “Amount column has positive/negative values”.
  - Set amount from (get\_float\_amount(transaction\_row.get(“amount”, “0”)) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_float\_amount(transaction\_row.get(“amount”, “0”)) → 0.
  - If amount &gt; 0.
    - Return tuple(0, abs(amount)).
  - Otherwise.
    - Return tuple(abs(amount), 0).
- Set transaction\_type from str((nested operand in the contract(nested operand in the contract) or empty text)).strip().lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction\_row.get(“debit\_credit”) → empty text.
- Set amount from abs((get\_float\_amount(transaction\_row.get(“amount”, “0”)) or 0)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_float\_amount(transaction\_row.get(“amount”, “0”)) → 0.
- If amount\_format equals “Transaction type column has "CR"/"DR" values”.
  - Return tuple(0, amount) when “cr” belongs to transaction\_type, otherwise tuple(amount, 0).
    - Value choice on “cr” belongs to transaction\_type — true gives tuple(0, amount), false gives tuple(amount, 0).
- If amount\_format equals “Transaction type column has "C"/"D" values”.
  - Return tuple(0, amount) when transaction\_type equals “c”, otherwise tuple(amount, 0).
    - Value choice on transaction\_type equals “c” — true gives tuple(0, amount), false gives tuple(amount, 0).
- If amount\_format equals “Transaction type column has "Deposit"/"Withdrawal" values”.
  - Return tuple(0, amount) when “deposit” belongs to transaction\_type, otherwise tuple(amount, 0).
    - Value choice on “deposit” belongs to transaction\_type — true gives tuple(0, amount), false gives tuple(amount, 0).
- Return tuple(0, 0).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L4101) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L363)

<a id="op-18eac3dda74af7"></a>
### Build table transactions

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_build_table_transactions`

**Inputs** table.

**Explicit results** tuple(final\_transactions, date\_format, amount\_format).

**Local steps**

- Set column\_mapping from mapping().
- For each column in table.get(“column\_mapping”, list()).
  - If (column.get(“maps\_to”) and column at “maps\_to” differs from “Do not import”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in column.get(“maps\_to”) → column at “maps\_to” differs from “Do not import”.
    - Set column\_mapping at column at “maps\_to” from column at “index”.
- Set tuple(transaction\_rows, \_start, \_end) from extract\_transaction\_rows(table.get(“rows”, list()), column\_mapping, table.get(“header\_index”)).
- Set tuple(date\_format, amount\_format) from get\_file\_properties(transaction\_rows).
- Set final\_transactions from compute\_final\_transactions(transaction\_rows, date\_format, amount\_format).
- Return tuple(final\_transactions, date\_format, amount\_format).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L5086) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L359)

<a id="op-f750c828ed6fd9"></a>
### Should include table

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_should_include_table`

**Inputs** table, final\_transactions.

**Declared result** bool.

**Explicit results** false · any(generator of column.get(“maps\_to”) equals “Description” for column drawn from table.get(“column\_mapping”, list())).

**Local steps**

- If not final\_transactions.
  - Return false.
- Return any(generator of column.get(“maps\_to”) equals “Description” for column drawn from table.get(“column\_mapping”, list())).
  - Draw column from table.get(“column\_mapping”, list()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L5463) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L400) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L380)

<a id="op-16a37ae86b2327"></a>
### Clean cell

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_clean_cell`

**Inputs** cell.

**Declared result** str.

**Explicit results** empty text · str(cell).replace(whitespace '\\n', one space).strip().

**Local steps**

- If cell is identical to no value.
  - Return empty text.
- Return str(cell).replace(whitespace '\\n', one space).strip().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L5629) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L361)

<a id="op-31e272d75eb064"></a>
### Extract pdf tables

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_extract_portable_document_tables`

**Inputs** content, password = no value.

**Declared result** list at dict.

**Explicit results** tables.

**Explicit failure paths** validation helper — translated “PDF statement support requires the 'pdfplumber' library to be installed.” · validation helper — translated “This PDF is password protected. Please set the correct statement password on the Bank Account and try again.” · validation helper — translated “Could not detect any tables in this PDF. It may be a scanned or image-based statement, which is not supporte …”.

**Local steps**

- Attempt the following.
  - Bind dependencies pdfplumber.
- On failure (ImportError).
  - Call the validation error handler Platform.throw(translated “PDF statement support requires the 'pdfplumber' library to be installed.”, title = translated “Missing Dependency”).
- Bind dependencies PdfReader.
- Set reader from PdfReader(io.BytesIO(content)).
- If reader.is\_encrypted.
  - If not password.
    - Set password from empty text.
  - If not reader.decrypt(password).
    - Call the validation error handler Platform.throw(translated “This PDF is password protected. Please set the correct statement password on the Bank Account and try again.”, title = translated “Password Required”).
- Set text\_settings from mapping(“vertical\_strategy” → “text”, “horizontal\_strategy” → “text”).
- Set tables from list().
- Within pdfplumber.open(io.BytesIO(content), password = (password or empty text)) bound as pdf.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in password → empty text.
  - For each tuple(page\_number, page) in enumerate(pdf.pages, start = 1).
    - Set found\_tables from page.find\_tables().
    - If not found\_tables.
      - Set found\_tables from page.find\_tables(table\_settings = text\_settings).
    - For each tuple(table\_index, table) in enumerate(found\_tables).
      - Set rows from list of list of \_clean\_cell(c) for c drawn from row for row drawn from (table.extract() or list()).
        - Draw row from (table.extract() or list()).
        - Draw c from row.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in table.extract() → list().
      - Set rows from list of row for row drawn from rows where any(generator of cell differs from empty text for cell drawn from row).
        - Draw row from rows, keep a combination only if (any(generator of cell differs from empty text for cell drawn from row)).
        - Draw cell from row.
      - If not rows.
        - Continue with the next iteration or loop test.
      - Evaluate tables.append(mapping(“page” → page\_number, “table\_index” → table\_index, “bbox” → list of round(float(v), 2) for v drawn from table.bbox, “page\_width” → round(float(page.width), 2), …)).
        - Draw v from table.bbox.
- If not tables.
  - Call the validation error handler Platform.throw(translated “Could not detect any tables in this PDF. It may be a scanned or image-based statement, which is not supporte …”, title = translated “No Tables Detected”).
- Return tables.

**Boundaries to resolve** callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L5740) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L386) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L366)

<a id="op-f60d443a17b08b"></a>
### Extract table in bbox

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_extract_table_in_bbox`

**Inputs** content, password, page\_number, bbox.

**Declared result** list at list at str.

**Explicit results** list of row for row drawn from rows where any(generator of cell differs from empty text for cell drawn from row).

**Local steps**

- Bind dependencies pdfplumber.
- Set text\_settings from mapping(“vertical\_strategy” → “text”, “horizontal\_strategy” → “text”).
- Within pdfplumber.open(io.BytesIO(content), password = (password or empty text)) bound as pdf.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in password → empty text.
  - Set page from pdf.pages at (page\_number − 1).
  - Set x0 from max(0, min(float(bbox at 0), page.width)).
  - Set top from max(0, min(float(bbox at 1), page.height)).
  - Set x1 from max((x0 + 1), min(float(bbox at 2), page.width)).
  - Set bottom from max((top + 1), min(float(bbox at 3), page.height)).
  - Set cropped from page.crop(tuple(x0, top, x1, bottom)).
  - Set table from (cropped.extract\_table() or cropped.extract\_table(table\_settings = text\_settings)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cropped.extract\_table() → cropped.extract\_table(table\_settings = text\_settings).
- Set rows from list of list of \_clean\_cell(cell) for cell drawn from row for row drawn from (table or list()).
  - Draw row from (table or list()).
  - Draw cell from row.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in table → list().
- Return list of row for row drawn from rows where any(generator of cell differs from empty text for cell drawn from row).
  - Draw row from rows, keep a combination only if (any(generator of cell differs from empty text for cell drawn from row)).
  - Draw cell from row.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0023.json#L6833) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L387) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L367)

<a id="op-92f77e3deb4130"></a>
### Render pdf pages

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_render_portable_document_pages`

**Inputs** content, password, pages, resolution = 150.

**Declared result** dict at tuple(int, tuple at tuple(bytes, float)).

**State and service calls** call save on page\_image.original.

**Explicit results** images.

**Local steps**

- Bind dependencies pdfplumber.
- Set images from mapping().
- Within pdfplumber.open(io.BytesIO(content), password = (password or empty text)) bound as pdf.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in password → empty text.
  - For each tuple(page\_number, page) in enumerate(pdf.pages, start = 1).
    - If page\_number does not belong to pages.
      - Continue with the next iteration or loop test.
    - Set page\_image from page.to\_image(resolution = resolution).
    - Set buffer from io.BytesIO().
    - Evaluate page\_image.original.save(buffer, format = “PNG”).
    - Set images at page\_number from tuple(buffer.getvalue(), round((resolution ÷ 72.0), 4)).
- Return images.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L377)

<a id="op-0915712a9979bd"></a>
### Get float amount

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_get_decimal_amount`

**Inputs** amount.

**Explicit results** no value · amount.

**Local steps**

- If not amount.
  - Return no value.
- If isinstance(amount, str).
  - Set amount from nested operand in the contract(nested operand in the contract, nested operand in the contract).replace(one space, empty text).replace(“cr”, empty text).replace(“dr”, empty text).
  - Set amount from re.sub(“&#91;^\\d.-&#93;”, empty text, amount).
  - Attempt the following.
    - Set amount from float(amount).
  - On failure (ValueError).
    - Return no value.
- Otherwise.
  - If isinstance(amount, int).
    - Set amount from float(amount).
  - Otherwise.
    - Attempt the following.
      - Set amount from float(amount).
    - On failure (ValueError).
      - Return no value.
- Return amount.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L465) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L391) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L371)

<a id="op-5659cb756b873e"></a>
### Get amount cr dr marker

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_get_amount_credit_debit_marker`

**Inputs** amount.

**Declared result** (str bitwise or no value).

**Explicit results** no value · match.group(group).lower().

**Local steps**

- If not isinstance(amount, str).
  - Return no value.
- Set match from AMOUNT\_CR\_DR\_PATTERN.search(amount).
- If not match.
  - Return no value.
- Set group from 1 when match.group(1), otherwise 2.
  - Value choice on match.group(1) — true gives 1, false gives 2.
- Set tuple(start, end) from match.span(group).
- Set remainder from (amount at slice no value to start + amount at slice end to no value).
- If not any(generator of char.isdigit() for char drawn from remainder).
  - Draw char from remainder.
  - Return no value.
- If sum(generator of char.isalpha() for char drawn from remainder) &gt; 3.
  - Draw char from remainder.
  - Return no value.
- Return match.group(group).lower().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L839) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L390) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L370)
