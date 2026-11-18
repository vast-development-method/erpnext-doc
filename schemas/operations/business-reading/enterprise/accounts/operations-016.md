# Accounting and settlement · operations 16

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank statement import

[Record definition](../../../../data/record-types/bank_statement_import.json)

<a id="op-4b51fa56ef302c"></a>
### Get import status

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_get_import_status`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc · read “Data Import Log” via get\_all.

**Explicit results** import\_status.

**Local steps**

- Set import\_status from mapping().
- Set data\_import from Platform.get\_doc(“Bank Statement Import”, docname).
- Evaluate data\_import.check\_permission().
- Set import\_status at “status” from data\_import.status.
- Set logs from Platform.get\_all(“Data Import Log”, fields = list(mapping(“COUNT” → “\*”, “as” → “count”), “success”), filters = mapping(“data\_import” → docname), group\_by = “success”).
- Set total\_payload\_count from 0.
- For each log in logs.
  - Update total\_payload\_count using + log.get(“count”, 0).
  - If log.get(“success”).
    - Set import\_status at “success” from log.get(“count”).
  - Otherwise.
    - Set import\_status at “failed” from log.get(“count”).
- Set import\_status at “total\_records” from total\_payload\_count.
- Return import\_status.

**Values supplied outside this operation** effective access from data\_import.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L338) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L318)

<a id="op-2494352c574493"></a>
### Get import logs

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_get_import_logs`

**Inputs** docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Data Import Log” via get\_all.

**Explicit results** Platform.get\_all(“Data Import Log”, fields = list(“success”, “docname”, “messages”, “exception”, …), filters = mapping(“data\_import” → docname), limit\_page\_length = 5000, order\_by = “log\_index”).

**Local steps**

- Evaluate Platform.has\_permission(“Bank Statement Import”, throw = true).
- Return Platform.get\_all(“Data Import Log”, fields = list(“success”, “docname”, “messages”, “exception”, …), filters = mapping(“data\_import” → docname), limit\_page\_length = 5000, order\_by = “log\_index”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Statement Import”, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L1166) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L317)

<a id="op-8770ae8f00589a"></a>
### Upload bank statement

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_upload_bank_statement`

**Inputs** remaining named values args.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “Bank Statement Import”.

**Explicit results** bsi.

**Local steps**

- Evaluate Platform.has\_permission(“Bank Statement Import”, “create”, throw = true).
- Set args from Platform.\_dict(args).
- Set bsi from Platform.new\_doc(“Bank Statement Import”).
- If args.company.
  - Evaluate bsi.update(mapping(“company” → args.company)).
- If args.bank\_account.
  - Evaluate bsi.update(mapping(“bank\_account” → args.bank\_account)).
- Return bsi.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Statement Import”, “create”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L347) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L327)

## Record · Bank statement import log

[Record definition](../../../../data/record-types/bank_statement_import_log.json)

<a id="op-b9e7847fc4f975"></a>
### Bank Statement Import Log.before validate

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_currency().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set currency](operations-016.md#op-d5bfa3f6494546).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L4202) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L356) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L336)

<a id="op-d5bfa3f6494546"></a>
### Bank Statement Import Log.set currency

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_currency`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_cached\_value · read “Account” via get\_cached\_value.

**Local steps**

- Set account from Platform.get\_cached\_value(“Bank Account”, self.bank\_account, “account”).
- Set self.currency from Platform.get\_cached\_value(“Account”, account, “account\_currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, self.bank\_account, “account”), Platform.get\_cached\_value(“Account”, account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L4253) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L373) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L353)

<a id="op-83c1acc252a78d"></a>
### Bank Statement Import Log.validate

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_validate`

**Inputs** self.

**Record and data access** read “Bank Account” via get\_value.

**Explicit failure paths** validation helper — translated “You do not have permission to import bank transactions” · validation helper — translated “You do not have permission to import and submit bank transactions” · validation helper — translated “The bank account is not a company account. Please select a company account” · validation helper — translated “The bank account is disabled. Please enable it”.

**Local steps**

- If not Platform.has\_permission(“Bank Transaction”, “write”).
  - Call the validation error handler Platform.throw(translated “You do not have permission to import bank transactions”, title = translated “Permission Denied”).
- If not Platform.has\_permission(“Bank Transaction”, “create”).
  - Call the validation error handler Platform.throw(translated “You do not have permission to import bank transactions”, title = translated “Permission Denied”).
- If not Platform.has\_permission(“Bank Transaction”, “submit”).
  - Call the validation error handler Platform.throw(translated “You do not have permission to import and submit bank transactions”, title = translated “Permission Denied”).
- Set tuple(is\_company\_account, disabled) from Platform.get\_value(“Bank Account”, self.bank\_account, list(“is\_company\_account”, “disabled”)).
- If not is\_company\_account.
  - Call the validation error handler Platform.throw(translated “The bank account is not a company account. Please select a company account”, title = translated “Invalid Bank Account”).
- If disabled.
  - Call the validation error handler Platform.throw(translated “The bank account is disabled. Please enable it”, title = translated “Disabled Bank Account”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “write”), Platform.has\_permission(“Bank Transaction”, “create”) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L4385) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L358)

<a id="op-e46b004a165065"></a>
### Bank Statement Import Log.before insert

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_before_insert`

**Inputs** self.

**Local steps**

- If self.is\_pdf().
  - Set tables from self.prepare\_pdf\_tables().
  - Evaluate self.set\_pdf\_summary(tables).
- Otherwise.
  - Set data from self.get\_data().
  - Evaluate self.set\_file\_properties(data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is pdf](operations-016.md#op-a43eca0db5e9a0), [prepare pdf tables](operations-017.md#op-f98980b5f9f96e), [set pdf summary](operations-017.md#op-8a08b6b14f333e), [get data](operations-016.md#op-cc4ae66e9b9d44), [set file properties](operations-016.md#op-05daa8168b859f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L4959) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L355) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L335)

<a id="op-a15e7d6edffbf3"></a>
### Bank Statement Import Log.after insert

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_after_insert`

**Inputs** self.

**Local steps**

- If self.is\_pdf().
  - Evaluate self.attach\_pdf\_page\_images().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is pdf](operations-016.md#op-a43eca0db5e9a0), [attach pdf page images](operations-017.md#op-32b9e194c21c8d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L5116) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L350) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L330)

<a id="op-05daa8168b859f"></a>
### Bank Statement Import Log.set file properties

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_file_properties`

**Inputs** self, raw\_data.

**Local steps**

- Evaluate self.set\_header\_row\_index(raw\_data).
- Evaluate self.set\_column\_mapping(raw\_data).
- Evaluate self.recompute\_properties(raw\_data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set header row index](operations-016.md#op-addc5cf8ade939), [set column mapping](operations-016.md#op-e4cf4ff2ad2e9f), [recompute properties](operations-016.md#op-fd1d4313f6eda1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L5190) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L354)

<a id="op-fd1d4313f6eda1"></a>
### Bank Statement Import Log.recompute properties

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_recompute_properties`

**Inputs** self, raw\_data.

**Local steps**

- Set tuple(transaction\_rows, transaction\_starting\_index, transaction\_ending\_index) from self.get\_transaction\_rows(raw\_data).
- Set self.detected\_transaction\_starting\_index from transaction\_starting\_index.
- Set self.detected\_transaction\_ending\_index from transaction\_ending\_index.
- Set self.number\_of\_transactions from len(transaction\_rows).
- Set tuple(date\_format, amount\_format) from get\_file\_properties(transaction\_rows).
- Set self.detected\_amount\_format from amount\_format.
- Set self.detected\_date\_format from date\_format.
- Evaluate self.set\_closing\_balance(transaction\_rows).
- Evaluate self.set\_total\_debits\_and\_credits(transaction\_rows = transaction\_rows).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get transaction rows](operations-016.md#op-23ce0114ade565), [set closing balance](operations-016.md#op-445822303c9294), [set total debits and credits](operations-016.md#op-5116bca868399d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L5318) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L368) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L348)

<a id="op-5116bca868399d"></a>
### Bank Statement Import Log.set total debits and credits

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_total_debits_and_credits`

**Inputs** self, transaction\_rows.

**Local steps**

- Set total\_debits from 0.
- Set total\_credits from 0.
- Set debit\_transactions from 0.
- Set credit\_transactions from 0.
- Set final\_transactions from self.get\_final\_transactions(transaction\_rows = transaction\_rows).
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
- Set self.total\_debits from total\_debits.
- Set self.total\_credits from total\_credits.
- Set self.total\_debit\_transactions from debit\_transactions.
- Set self.total\_credit\_transactions from credit\_transactions.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get final transactions](operations-016.md#op-cdc54186a95e8d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L5605) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L377) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L357)

<a id="op-a9c8d6ce34460f"></a>
### Bank Statement Import Log.get file doc

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_file_record`

**Inputs** self.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** Platform.get\_doc(“File”, mapping(“file\_url” → self.file)).

**Local steps**

- Return Platform.get\_doc(“File”, mapping(“file\_url” → self.file)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6008) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L339)

<a id="op-02e23bb870facb"></a>
### Bank Statement Import Log.get file extension

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_file_extension`

**Inputs** self.

**Explicit results** nested operand in the contract.get\_file\_doc().get\_extension() at 1.lower().

**Local steps**

- Return nested operand in the contract.get\_file\_doc().get\_extension() at 1.lower().

**Methods declared on this owner** [get file doc](operations-016.md#op-a9c8d6ce34460f).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6092) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L338)

<a id="op-a43eca0db5e9a0"></a>
### Bank Statement Import Log.is pdf

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_is_portable_document`

**Inputs** self.

**Explicit results** self.get\_file\_extension() equals “.pdf”.

**Local steps**

- Return self.get\_file\_extension() equals “.pdf”.

**Methods declared on this owner** [get file extension](operations-016.md#op-02e23bb870facb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6173) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L366) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L346)

<a id="op-ed5fc753fee9ec"></a>
### Bank Statement Import Log.get statement password

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_statement_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6236) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L363) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L343)

<a id="op-cc4ae66e9b9d44"></a>
### Bank Statement Import Log.get data

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_data`

**Inputs** self.

**Explicit results** data.

**Explicit failure paths** validation helper — translated “Import template should be of type .csv, .xlsx, .xls or .pdf”.

**Local steps**

- Set file\_doc from self.get\_file\_doc().
- Set extension from self.get\_file\_extension().
- Set content from file\_doc.get\_content().
- If extension does not belong to tuple(“.csv”, “.xlsx”, “.xls”).
  - Call the validation error handler Platform.throw(translated “Import template should be of type .csv, .xlsx, .xls or .pdf”, title = translated “Invalid File Type”).
- If extension equals “.csv”.
  - Set data from read\_csv\_content(content).
- Otherwise.
  - If extension equals “.xlsx”.
    - Set data from read\_xlsx\_file\_from\_attached\_file(fcontent = content).
  - Otherwise.
    - If extension equals “.xls”.
      - Set data from read\_xls\_file\_from\_attached\_file(content).
- Return data.

**Methods declared on this owner** [get file doc](operations-016.md#op-a9c8d6ce34460f), [get file extension](operations-016.md#op-02e23bb870facb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6352) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L357) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L337)

<a id="op-addc5cf8ade939"></a>
### Bank Statement Import Log.set header row index

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_header_row_index`

**Inputs** self, data.

**Local steps**

- Set tuple(self.detected\_header\_index, \_) from detect\_header\_row(data).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6720) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L375) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L355)

<a id="op-e4cf4ff2ad2e9f"></a>
### Bank Statement Import Log.set column mapping

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_column_mapping`

**Inputs** self, data.

**Local steps**

- Evaluate self.set\_column\_mapping\_from\_columns(detect\_column\_mapping(data at self.detected\_header\_index)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set column mapping from columns](operations-016.md#op-98d6440b9dcad8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6823) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L371) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L351)

<a id="op-98d6440b9dcad8"></a>
### Bank Statement Import Log.set column mapping from columns

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_column_mapping_from_columns`

**Inputs** self, columns.

**Local steps**

- Set self.column\_mapping from list().
- For each col in columns.
  - Set index from col at “index”.
  - Evaluate self.append(“column\_mapping”, mapping(“header\_text” → (col.get(“header\_text”) or translated “Column {0}”.format((index + 1))), “variable” → (col.get(“variable”) or formatted text column\_{index}), “maps\_to” ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“header\_text”) → translated “Column {0}”.format((index + 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“variable”) → formatted text column\_{index}.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L372) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L352)

<a id="op-936898a9dd7d4d"></a>
### Bank Statement Import Log.apply column mapping

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_apply_column_mapping`

**Inputs** self, columns.

**Local steps**

- Evaluate self.set\_column\_mapping\_from\_columns(columns).
- Evaluate self.recompute\_properties(self.get\_data()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set column mapping from columns](operations-016.md#op-98d6440b9dcad8), [recompute properties](operations-016.md#op-fd1d4313f6eda1), [get data](operations-016.md#op-cc4ae66e9b9d44).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L353) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L351) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L331)

<a id="op-9cc8fdab813137"></a>
### Bank Statement Import Log.apply header index

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_apply_header_index`

**Inputs** self, header\_index.

**Local steps**

- Set raw\_data from self.get\_data().
- If 0 ≤ header\_index &lt; len(raw\_data).
  - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ header\_index &lt; len(raw\_data).
  - Set self.detected\_header\_index from header\_index.
  - Set candidate from detect\_column\_mapping(raw\_data at header\_index).
  - If is\_meaningful\_mapping(candidate).
    - Evaluate self.set\_column\_mapping\_from\_columns(candidate).
- Otherwise.
  - Set self.detected\_header\_index from negative 1.
- Evaluate self.recompute\_properties(raw\_data).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data](operations-016.md#op-cc4ae66e9b9d44), [set column mapping from columns](operations-016.md#op-98d6440b9dcad8), [recompute properties](operations-016.md#op-fd1d4313f6eda1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L469) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L352) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L332)

<a id="op-23ce0114ade565"></a>
### Bank Statement Import Log.get transaction rows

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_transaction_rows`

**Inputs** self, data.

**Explicit results** extract\_transaction\_rows(data, column\_mapping, self.detected\_header\_index).

**Local steps**

- Set column\_mapping from mapping().
- For each column in self.column\_mapping.
  - If column.maps\_to differs from “Do not import”.
    - Set column\_mapping at column.maps\_to from column.index.
- Return extract\_transaction\_rows(data, column\_mapping, self.detected\_header\_index).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L727) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L364) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L344)

<a id="op-445822303c9294"></a>
### Bank Statement Import Log.set closing balance

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_set_closing_balance`

**Inputs** self, transactions.

**Local steps**

- Set statement\_start\_date from no value.
- Set statement\_end\_date from no value.
- Set closing\_balance from no value.
- Set date\_format from self.detected\_date\_format.
- For each transaction in transactions.
  - Set date from transaction.get(“date”).
  - If not date.
    - Continue with the next iteration or loop test.
  - If isinstance(date, datetime).
    - Set tx\_date from date.
  - Otherwise.
    - Set tx\_date from datetime.strptime(date, date\_format).
  - If (statement\_start\_date is identical to no value or tx\_date &lt; statement\_start\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in statement\_start\_date is identical to no value → tx\_date &lt; statement\_start\_date.
    - Set statement\_start\_date from tx\_date.
  - If (statement\_end\_date is identical to no value or tx\_date ≥ statement\_end\_date).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in statement\_end\_date is identical to no value → tx\_date ≥ statement\_end\_date.
    - Set statement\_end\_date from tx\_date.
    - Set closing\_balance from transaction.get(“balance”).
- Set self.start\_date from getdate(statement\_start\_date).
- Set self.end\_date from getdate(statement\_end\_date).
- Set self.closing\_balance from get\_float\_amount(closing\_balance).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L909) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L370) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L350)

<a id="op-cdc54186a95e8d"></a>
### Bank Statement Import Log.get final transactions

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_bank_statement_import_log_get_final_transactions`

**Inputs** self, transaction\_rows.

**Explicit results** compute\_final\_transactions(transaction\_rows, self.detected\_date\_format, self.detected\_amount\_format).

**Local steps**

- Return compute\_final\_transactions(transaction\_rows, self.detected\_date\_format, self.detected\_amount\_format).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0022.json#L1382) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L360) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L340)
