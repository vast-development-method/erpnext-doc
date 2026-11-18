# Accounting and settlement · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank statement import log

[Record definition](../../../../data/record-types/bank_statement_import_log.json)

<a id="op-991e62505c5585"></a>
### Get file properties

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_get_file_properties`

**Inputs** transactions.

**Explicit results** tuple(most\_common\_date\_format, most\_common\_amount\_format).

**Local steps**

- Set date\_format\_frequency from mapping(“%d/%m/%Y” → 0).
- Set amount\_format\_frequency from mapping(“Separate columns for withdrawal and deposit” → 0, “Amount column has "CR"/"DR" values” → 0, “Amount column has positive/negative values” → 0, “Transaction type column has "CR"/"DR" values” → 0, …).
- Set amount\_column\_has\_cr\_dr from false.
- For each transaction in transactions.
  - Set date\_format from transaction.get(“date\_format”).
  - If date\_format.
    - Set date\_format\_frequency at date\_format from (date\_format\_frequency.get(date\_format, 0) + 1).
  - If (transaction.get(“withdrawal”, no value) or transaction.get(“deposit”, no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction.get(“withdrawal”, no value) → transaction.get(“deposit”, no value).
    - Update amount\_format\_frequency at “Separate columns for withdrawal and deposit” using + 1.
    - Continue with the next iteration or loop test.
  - Set amount from transaction.get(“amount”, no value).
  - If not amount.
    - Continue with the next iteration or loop test.
  - Set debit\_credit from str((nested operand in the contract(nested operand in the contract) or empty text)).strip().lower().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction.get(“debit\_credit”) → empty text.
  - If get\_amount\_cr\_dr\_marker(amount).
    - Set amount\_column\_has\_cr\_dr from true.
    - Update amount\_format\_frequency at “Amount column has "CR"/"DR" values” using + 1.
  - Otherwise.
    - If (“deposit” belongs to debit\_credit or “withdrawal” belongs to debit\_credit).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in “deposit” belongs to debit\_credit → “withdrawal” belongs to debit\_credit.
      - Update amount\_format\_frequency at “Transaction type column has "Deposit"/"Withdrawal" values” using + 1.
    - Otherwise.
      - If debit\_credit belongs to tuple(“c”, “d”).
        - Update amount\_format\_frequency at “Transaction type column has "C"/"D" values” using + 1.
      - Otherwise.
        - If any(generator of token belongs to debit\_credit for token drawn from tuple(“cr”, “dr”, “debit”)).
          - Draw token from tuple(“cr”, “dr”, “debit”).
          - Update amount\_format\_frequency at “Transaction type column has "CR"/"DR" values” using + 1.
        - Otherwise.
          - Update amount\_format\_frequency at “Amount column has positive/negative values” using + 1.
- Set most\_common\_date\_format from max(date\_format\_frequency, key = date\_format\_frequency.get).
- Set most\_common\_amount\_format from max(amount\_format\_frequency, key = amount\_format\_frequency.get).
- If not amount\_format\_frequency at most\_common\_amount\_format.
  - Set most\_common\_amount\_format from “Amount column has positive/negative values”.
- If (amount\_column\_has\_cr\_dr and most\_common\_amount\_format equals “Amount column has positive/negative values”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in amount\_column\_has\_cr\_dr → most\_common\_amount\_format equals “Amount column has positive/negative values”.
  - Set most\_common\_amount\_format from “Amount column has "CR"/"DR" values”.
- Return tuple(most\_common\_date\_format, most\_common\_amount\_format).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L1259) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L392) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L372)

<a id="op-c3b9737eca5ca3"></a>
### Get statement details

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_get_statement_details`

**Inputs** statement\_import\_id.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)).

**Record and data access** resolve a document from “Bank Statement Import Log” via get\_doc.

**Explicit results** mapping(“doc” → doc, “date\_format” → formatted\_date\_format, “conflicting\_transactions” → conflicting\_transactions, “final\_transactions” → final\_transactions, …).

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import Log”, statement\_import\_id).
- Evaluate doc.check\_permission().
- Set char\_map from mapping(“%d” → “DD”, “%m” → “MM”, “%Y” → “YYYY”, “%y” → “YY”, …).
- Set formatted\_date\_format from doc.detected\_date\_format.
- For each tuple(char, replacement) in char\_map.items().
  - Set formatted\_date\_format from formatted\_date\_format.replace(char, replacement).
- Set conflicting\_transactions from check\_for\_conflicts(doc.bank\_account, doc.start\_date, doc.end\_date).
- If doc.is\_pdf().
  - Set pdf\_tables from doc.get\_pdf\_tables().
  - Set final\_transactions from doc.get\_pdf\_final\_transactions().
  - Return mapping(“doc” → doc, “date\_format” → formatted\_date\_format, “conflicting\_transactions” → conflicting\_transactions, “final\_transactions” → final\_transactions, …).
- Set raw\_data from doc.get\_data().
- Set tuple(transaction\_rows, \_starting\_index, \_ending\_index) from doc.get\_transaction\_rows(raw\_data).
- Set final\_transactions from doc.get\_final\_transactions(transaction\_rows = transaction\_rows).
- Return mapping(“doc” → doc, “date\_format” → formatted\_date\_format, “conflicting\_transactions” → conflicting\_transactions, “final\_transactions” → final\_transactions, …).

**Values supplied outside this operation** effective access from doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L2197) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L393) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L373)

<a id="op-a8637aaa3d45d0"></a>
### Update pdf tables

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_update_portable_document_tables`

**Inputs** statement\_import\_id, tables.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import Log” via get\_doc.

**Explicit results** get\_statement\_details(statement\_import\_id).

**Explicit failure paths** validation helper — translated “This statement has already been imported.”.

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import Log”, statement\_import\_id).
- Evaluate doc.check\_permission(“write”).
- If doc.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “This statement has already been imported.”, title = translated “Already Imported”).
- If isinstance(tables, str).
  - Set tables from json.loads(tables).
- Evaluate doc.apply\_pdf\_tables(tables).
- Return get\_statement\_details(statement\_import\_id).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L402) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L382)

<a id="op-0e9ebea0e35f02"></a>
### Reextract pdf table

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_reextract_portable_document_table`

**Inputs** statement\_import\_id, page, table\_index, bbox.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import Log” via get\_doc.

**Explicit results** get\_statement\_details(statement\_import\_id).

**Explicit failure paths** validation helper — translated “This statement has already been imported.”.

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import Log”, statement\_import\_id).
- Evaluate doc.check\_permission(“write”).
- If doc.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “This statement has already been imported.”, title = translated “Already Imported”).
- If isinstance(bbox, str).
  - Set bbox from json.loads(bbox).
- Set page from int(page).
- Set table\_index from int(table\_index).
- Set content from doc.get\_file\_doc().get\_content().
- Set password from doc.get\_statement\_password().
- Set rows from extract\_table\_in\_bbox(content, password, page, list of float(v) for v drawn from bbox).
  - Draw v from bbox.
- Set tables from doc.get\_pdf\_tables().
- For each table in tables.
  - If (table at “page” equals page and table at “table\_index” equals table\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in table at “page” equals page → table at “table\_index” equals table\_index.
    - Set old\_columns from max(generator of len(row) for row drawn from table.get(“rows”, list()), default = 0).
      - Draw row from table.get(“rows”, list()).
    - Set new\_columns from max(generator of len(row) for row drawn from rows, default = 0).
      - Draw row from rows.
    - Set table at “rows” from rows.
    - Set table at “bbox” from list of round(float(v), 2) for v drawn from bbox.
      - Draw v from bbox.
    - If (new\_columns differs from old\_columns or not table.get(“column\_mapping”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_columns differs from old\_columns → not table.get(“column\_mapping”).
      - Set tuple(header\_index, score) from detect\_header\_row(rows).
      - If score ≥ 2.
        - Set table at “header\_index” from header\_index.
        - Set table at “column\_mapping” from detect\_column\_mapping(rows at header\_index).
      - Otherwise.
        - Set table at “header\_index” from no value.
        - Set table at “column\_mapping” from guess\_column\_mapping\_by\_content(rows).
    - Set tuple(\_finals, table at “date\_format”, table at “amount\_format”) from build\_table\_transactions(table).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate doc.apply\_pdf\_tables(tables).
- Return get\_statement\_details(statement\_import\_id).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L396) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L376)

<a id="op-373e3eb92ddd38"></a>
### Set pdf table header

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_set_portable_document_table_header`

**Inputs** statement\_import\_id, page, table\_index, header\_index.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import Log” via get\_doc.

**Explicit results** get\_statement\_details(statement\_import\_id).

**Explicit failure paths** validation helper — translated “This statement has already been imported.”.

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import Log”, statement\_import\_id).
- Evaluate doc.check\_permission(“write”).
- If doc.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “This statement has already been imported.”, title = translated “Already Imported”).
- Set page from int(page).
- Set table\_index from int(table\_index).
- Set header\_index from int(header\_index).
- Set tables from doc.get\_pdf\_tables().
- For each table in tables.
  - If (table at “page” equals page and table at “table\_index” equals table\_index).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in table at “page” equals page → table at “table\_index” equals table\_index.
    - Set rows from table.get(“rows”, list()).
    - If 0 ≤ header\_index &lt; len(rows).
      - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ header\_index &lt; len(rows).
      - Set table at “header\_index” from header\_index.
      - Set candidate from detect\_column\_mapping(rows at header\_index).
      - If is\_meaningful\_mapping(candidate).
        - Set table at “column\_mapping” from candidate.
    - Otherwise.
      - Set table at “header\_index” from no value.
    - Set tuple(\_finals, table at “date\_format”, table at “amount\_format”) from build\_table\_transactions(table).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate doc.apply\_pdf\_tables(tables).
- Return get\_statement\_details(statement\_import\_id).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L4379) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L399) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L379)

<a id="op-df9260d3db62a3"></a>
### Update column mapping

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_update_column_mapping`

**Inputs** statement\_import\_id, column\_mapping.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import Log” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_statement\_details(statement\_import\_id).

**Explicit failure paths** validation helper — translated “This statement has already been imported.”.

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import Log”, statement\_import\_id).
- If doc.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “This statement has already been imported.”, title = translated “Already Imported”).
- If isinstance(column\_mapping, str).
  - Set column\_mapping from json.loads(column\_mapping).
- Evaluate doc.apply\_column\_mapping(column\_mapping).
- Evaluate doc.save().
- Return get\_statement\_details(statement\_import\_id).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L401) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L381)

<a id="op-1ce26fd37f8954"></a>
### Set header index

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_set_header_index`

**Inputs** statement\_import\_id, header\_index.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import Log” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** get\_statement\_details(statement\_import\_id).

**Explicit failure paths** validation helper — translated “This statement has already been imported.”.

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import Log”, statement\_import\_id).
- If doc.status equals “Completed”.
  - Call the validation error handler Platform.throw(translated “This statement has already been imported.”, title = translated “Already Imported”).
- Evaluate doc.apply\_header\_index(int(header\_index)).
- Evaluate doc.save().
- Return get\_statement\_details(statement\_import\_id).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L5435) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L378)

<a id="op-d753b1b77e1bc1"></a>
### Check for conflicts

`operation_enterprise_accounts_record_definitions_bank_statement_import_log_business_behavior_check_for_conflicts`

**Inputs** bank\_account, start\_date, end\_date.

**Record and data access** read “Bank Transaction” via get\_all.

**Explicit results** conflicts.

**Local steps**

- Set conflicts from Platform.get\_all(“Bank Transaction”, filters = mapping(“bank\_account” → bank\_account, “date” → list(“between”, list(start\_date, end\_date)), “docstatus” → 1), fields = list(“name”, “date”, “withdrawal”, “de ….
- Return conflicts.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0024.json#L5719) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L360)

## Record · Bank transaction

[Record definition](../../../../data/record-types/bank_transaction.json)

<a id="op-5f7021238ab588"></a>
### Auto Match Party.initialize

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_match_party_initialize`

**Inputs** self, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- Evaluate self.\_\_dict\_\_.update(kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2143) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L434)

<a id="op-6030bada4f4331"></a>
### Auto Match Party.get

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_match_party_get`

**Inputs** self, key.

**Explicit results** self.\_\_dict\_\_.get(key, no value).

**Local steps**

- Return self.\_\_dict\_\_.get(key, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2206) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L433)

<a id="op-aec03bdc5ebc42"></a>
### Auto Match Party.match

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_match_party_match`

**Inputs** self.

**Declared result** (tuple bitwise or no value).

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** result.

**Local steps**

- Set result from no value.
- Set result from AutoMatchbyAccountIBAN(bank\_party\_account\_number = self.bank\_party\_account\_number, bank\_party\_iban = self.bank\_party\_iban, deposit = self.deposit).match().
- Set fuzzy\_matching\_enabled from Platform.get\_single\_value(“Accounts Settings”, “enable\_fuzzy\_matching”).
- If (not result and fuzzy\_matching\_enabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not result → fuzzy\_matching\_enabled.
  - Set result from AutoMatchbyPartyNameDescription(bank\_party\_name = self.bank\_party\_name, description = self.description, deposit = self.deposit).match().
- Return result.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “enable\_fuzzy\_matching”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2274) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L435)

<a id="op-d4fc3b15cfb871"></a>
### Auto Matchby Account IBAN.initialize

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_account_international_bank_account_number_initialize`

**Inputs** self, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- Evaluate self.\_\_dict\_\_.update(kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2544) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L438)

<a id="op-404b1b02baa317"></a>
### Auto Matchby Account IBAN.get

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_account_international_bank_account_number_get`

**Inputs** self, key.

**Explicit results** self.\_\_dict\_\_.get(key, no value).

**Local steps**

- Return self.\_\_dict\_\_.get(key, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2607) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L436)

<a id="op-a1dae9c5e45485"></a>
### Auto Matchby Account IBAN.match

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_account_international_bank_account_number_match`

**Inputs** self.

**Explicit results** no value · self.match\_account\_in\_party().

**Local steps**

- If not (self.bank\_party\_account\_number or self.bank\_party\_iban).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bank\_party\_account\_number → self.bank\_party\_iban.
  - Return no value.
- Return self.match\_account\_in\_party().

**Methods declared on this owner** [match account in party](operations-018.md#op-27971f6f456e92).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2675) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L459) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L439)

<a id="op-27971f6f456e92"></a>
### Auto Matchby Account IBAN.match account in party

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_account_international_bank_account_number_match_account_in_party`

**Inputs** self.

**Declared result** (tuple bitwise or no value).

**Record and data access** read “Bank Account” via get\_all · read “Employee” via get\_all.

**Explicit results** no value · tuple(result at “party\_type”, result at “party”) · tuple(“Employee”, employee\_result at 0).

**Local steps**

- If not (self.bank\_party\_account\_number or self.bank\_party\_iban).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bank\_party\_account\_number → self.bank\_party\_iban.
  - Return no value.
- Set party\_result from Platform.db.get\_all(“Bank Account”, or\_filters = self.get\_or\_filters(), filters = mapping(“party\_type” → tuple(“is”, “set”), “party” → tuple(“is”, “set”)), fields = list(“party”, “party\_type”), limit\_page\_ ….
- If result bound to party\_result at 0 when party\_result, otherwise no value.
  - Value choice on party\_result — true gives party\_result at 0, false gives no value.
  - Return tuple(result at “party\_type”, result at “party”).
- If employee\_result bound to Platform.db.get\_all(“Employee”, or\_filters = self.get\_or\_filters(“Employee”), pluck = “name”, limit\_page\_length = 1).
  - Return tuple(“Employee”, employee\_result at 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get or filters](operations-018.md#op-a169df10221551).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L2766) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L440)

<a id="op-a169df10221551"></a>
### Auto Matchby Account IBAN.get or filters

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_account_international_bank_account_number_get_or_filters`

**Inputs** self, party = no value.

**Declared result** dict.

**Explicit results** or\_filters.

**Local steps**

- Set or\_filters from mapping().
- If self.bank\_party\_account\_number.
  - Set bank\_ac\_field from “bank\_ac\_no” when party equals “Employee”, otherwise “bank\_account\_no”.
    - Value choice on party equals “Employee” — true gives “bank\_ac\_no”, false gives “bank\_account\_no”.
  - Set or\_filters at bank\_ac\_field from self.bank\_party\_account\_number.
- If self.bank\_party\_iban.
  - Set or\_filters at “iban” from self.bank\_party\_iban.
- Return or\_filters.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L3204) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L437)

<a id="op-a9a1220813e3ac"></a>
### Auto Matchby Party Name Description.initialize

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_party_name_description_initialize`

**Inputs** self, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- Evaluate self.\_\_dict\_\_.update(kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L3415) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L463) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L443)

<a id="op-b0de9f4a534178"></a>
### Auto Matchby Party Name Description.get

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_party_name_description_get`

**Inputs** self, key.

**Explicit results** self.\_\_dict\_\_.get(key, no value).

**Local steps**

- Return self.\_\_dict\_\_.get(key, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L3478) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L442)

<a id="op-6792c92b097158"></a>
### Auto Matchby Party Name Description.match

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_party_name_description_match`

**Inputs** self.

**Declared result** (tuple bitwise or no value).

**Explicit results** no value · self.match\_party\_name\_desc\_in\_party().

**Local steps**

- If not (self.bank\_party\_name or self.description).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bank\_party\_name → self.description.
  - Return no value.
- Return self.match\_party\_name\_desc\_in\_party().

**Methods declared on this owner** [match party name desc in party](operations-018.md#op-e4a5481d5e5883).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L3546) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L444)

<a id="op-e4a5481d5e5883"></a>
### Auto Matchby Party Name Description.match party name desc in party

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_party_name_description_match_party_name_description_in_party`

**Inputs** self.

**Declared result** (tuple bitwise or no value).

**Record and data access** read party via get\_all.

**Explicit results** result.

**Local steps**

- Set result from no value.
- Set parties from get\_parties\_in\_order(self.deposit).
- For each party in parties.
  - Set filters from mapping(“status” → “Active”) when party equals “Employee”, otherwise mapping(“disabled” → 0).
    - Value choice on party equals “Employee” — true gives mapping(“status” → “Active”), false gives mapping(“disabled” → 0).
  - Set field from formatted text {party.lower()}\_name.
  - Set names from Platform.get\_all(party, filters = filters, fields = list(formatted text {field} as party\_name, “name”)).
  - For each field in list(“bank\_party\_name”, “description”).
    - If not self.get(field).
      - Continue with the next iteration or loop test.
    - Set tuple(result, skip) from self.fuzzy\_search\_and\_return\_result(party, names, field).
    - If (result or skip).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → skip.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If (result or skip).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → skip.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return result.

**Methods declared on this owner** [get](operations-018.md#op-b0de9f4a534178), [fuzzy search and return result](operations-018.md#op-bdb36d8eb06252).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L3645) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L445)

<a id="op-bdb36d8eb06252"></a>
### Auto Matchby Party Name Description.fuzzy search and return result

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_party_name_description_fuzzy_search_and_return_result`

**Inputs** self, party, names, field.

**Declared result** (tuple bitwise or no value).

**Explicit results** tuple(tuple(party, party\_name), skip) when party\_name, otherwise tuple(no value, skip).

**Local steps**

- Set skip from false.
- Set result from process.extract(query = self.get(field), choices = mapping of row.get(“name”) → row.get(“party\_name”) for row drawn from names, scorer = fuzz.token\_set\_ratio, processor = default\_process).
  - Draw row from names.
- Set tuple(party\_name, skip) from self.process\_fuzzy\_result(result).
- Return tuple(tuple(party, party\_name), skip) when party\_name, otherwise tuple(no value, skip).
  - Value choice on party\_name — true gives tuple(tuple(party, party\_name), skip), false gives tuple(no value, skip).

**Methods declared on this owner** [get](operations-018.md#op-b0de9f4a534178), [process fuzzy result](operations-018.md#op-774245467d40e4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L4115) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L441)

<a id="op-774245467d40e4"></a>
### Auto Matchby Party Name Description.process fuzzy result

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_auto_matchby_party_name_description_process_fuzzy_result`

**Inputs** self, result.

**Explicit results** tuple(no value, false) · tuple(first\_result at PARTY\_ID when first\_result at SCORE &gt; CUTOFF, otherwise no value, true) · tuple(no value, true) · tuple(first\_result at PARTY\_ID, true).

**Local steps**

- Set tuple(SCORE, PARTY\_ID, CUTOFF) from tuple(1, 2, 80).
- If (not result or not len(result)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not result → not len(result).
  - Return tuple(no value, false).
- Set first\_result from result at 0.
- If len(result) equals 1.
  - Return tuple(first\_result at PARTY\_ID when first\_result at SCORE &gt; CUTOFF, otherwise no value, true).
    - Value choice on first\_result at SCORE &gt; CUTOFF — true gives first\_result at PARTY\_ID, false gives no value.
- If first\_result at SCORE &gt; CUTOFF.
  - Set second\_result from result at 1.
  - If first\_result at SCORE equals second\_result at SCORE.
    - Return tuple(no value, true).
  - Return tuple(first\_result at PARTY\_ID, true).
- Otherwise.
  - Return tuple(no value, false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L4421) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L446)

<a id="op-52f746ad120e5c"></a>
### Get parties in order

`operation_enterprise_accounts_record_definitions_bank_transaction_auto_match_party_business_behavior_get_parties_in_order`

**Inputs** deposit.

**Declared result** list.

**Explicit results** list(“Customer”, “Supplier”, “Employee”) when flt(deposit) &gt; 0, otherwise list(“Supplier”, “Employee”, “Customer”).

**Local steps**

- Return list(“Customer”, “Supplier”, “Employee”) when flt(deposit) &gt; 0, otherwise list(“Supplier”, “Employee”, “Customer”).
  - Value choice on flt(deposit) &gt; 0 — true gives list(“Customer”, “Supplier”, “Employee”), false gives list(“Supplier”, “Employee”, “Customer”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L4810) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L447)

<a id="op-ef19d5d4c188ed"></a>
### Bank Transaction.before validate

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_bank_transaction_before_validate`

**Inputs** self.

**Local steps**

- Evaluate self.handle\_excluded\_fee().
- Evaluate self.update\_allocated\_amount().

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle excluded fee](operations-019.md#op-52de0923a27478), [update allocated amount](operations-019.md#op-a717d4756822c0).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0026.json#L4946) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L457)
