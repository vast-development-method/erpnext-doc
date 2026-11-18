# Accounting and settlement · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank transaction

[Record definition](../../../../data/record-types/bank_transaction.json)

<a id="op-6685d58a3cccfb"></a>
### Get related bank gl entries

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_get_related_bank_general_ledger_entries`

**Inputs** docs.

**Record and data access** execute query text (SELECT, GL Entry, Account).

**Explicit results** mapping() · entries.

**Local steps**

- If not docs.
  - Return mapping().
- Set result from Platform.db.sql(query text (SELECT, GL Entry, Account), mapping(“docs” → docs), as\_dict = true).
- Set entries from mapping().
- For each row in result.
  - Set key from tuple(row at “doctype”, row at “docname”).
  - If key does not belong to entries.
    - Set entries at key from mapping().
  - Set entries at key at row at “gl\_account” from row at “amount”.
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L496) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L476)

<a id="op-20e00e3ca20f5d"></a>
### Get total allocated amount

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_get_total_allocated_amount`

**Inputs** docs.

**Record and data access** execute query text (SELECT, Bank Transaction Payments, Bank Transaction, Bank Account).

**Explicit results** mapping() · payment\_allocation\_details.

**Local steps**

- If not docs.
  - Return mapping().
- Set result from Platform.db.sql(query text (SELECT, Bank Transaction Payments, Bank Transaction, Bank Account), dict(docs = docs), as\_dict = true).
- Set payment\_allocation\_details from mapping().
- For each row in result.
  - Set row at “latest\_date” from getdate(row at “latest\_date”).
  - Set payment\_allocation\_details.setdefault(tuple(row at “payment\_document”, row at “payment\_entry”), mapping()) at row at “gl\_account” from row.
- Return payment\_allocation\_details.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L477)

<a id="op-2e23778c740524"></a>
### Get reconciled bank transactions

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_get_reconciled_bank_transactions`

**Inputs** doctype, docname.

**Record and data access** read “Bank Transaction Payments” via get\_all.

**Explicit results** Platform.get\_all(“Bank Transaction Payments”, filters = mapping(“payment\_document” → doctype, “payment\_entry” → docname), pluck = “parent”).

**Local steps**

- Return Platform.get\_all(“Bank Transaction Payments”, filters = mapping(“payment\_document” → doctype, “payment\_entry” → docname), pluck = “parent”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L6148) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L474)

<a id="op-14806b61b2a7f8"></a>
### Remove from bank transaction

`operation_enterprise_accounts_record_definitions_bank_transaction_business_behavior_remove_from_bank_transaction`

**Inputs** doctype, docname.

**Record and data access** resolve a document from “Bank Transaction” via get\_doc.

**State and service calls** call save on bt.

**Local steps**

- For each bt\_name in get\_reconciled\_bank\_transactions(doctype, docname).
  - Set bt from Platform.get\_doc(“Bank Transaction”, bt\_name).
  - If bt.docstatus equals DocStatus.cancelled().
    - Continue with the next iteration or loop test.
  - Set modified from false.
  - For each pe in bt.payment\_entries.
    - If (pe.payment\_document equals doctype and pe.payment\_entry equals docname).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in pe.payment\_document equals doctype → pe.payment\_entry equals docname.
      - Evaluate bt.remove(pe).
      - Set modified from true.
  - If modified.
    - Evaluate bt.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0027.json#L6273) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L478)

<a id="op-bd786ce6b31b69"></a>
### Upload bank statement

`operation_enterprise_accounts_record_definitions_bank_transaction_bank_transaction_upload_business_behavior_upload_bank_statement`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“columns” → columns, “data” → data).

**Local steps**

- Evaluate Platform.has\_permission(“Bank Transaction”, “create”, throw = true).
- If getattr(Platform, “uploaded\_file”, no value).
  - Within open(Platform.uploaded\_file, “rb”) bound as upfile.
    - Set fcontent from upfile.read().
- Otherwise.
  - Set fcontent from Platform.local.uploaded\_file.
  - Set fname from Platform.local.uploaded\_filename.
- If Platform.safe\_encode(fname).lower().endswith(byte value).
  - Bind dependencies read\_csv\_content.
  - Set rows from read\_csv\_content(fcontent, false).
- Otherwise.
  - If Platform.safe\_encode(fname).lower().endswith(byte value).
    - Bind dependencies read\_xlsx\_file\_from\_attached\_file.
    - Set rows from read\_xlsx\_file\_from\_attached\_file(fcontent = fcontent).
- Set columns from rows at 0.
- Evaluate rows.pop(0).
- Set data from rows.
- Return mapping(“columns” → columns, “data” → data).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “create”, throw = true) · selected callable from getattr(Platform, “uploaded\_file”, no value).

**Boundaries to resolve** late-bound calls, callee failures, file state, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L451)

<a id="op-e1d5a0e1be9ad4"></a>
### Create bank entries

`operation_enterprise_accounts_record_definitions_bank_transaction_bank_transaction_upload_business_behavior_create_bank_entries`

**Inputs** columns, data, bank\_account.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Bank Transaction”) via get\_doc.

**State and service calls** call insert on bank\_transaction · call submit on bank\_transaction.

**Explicit results** mapping(“success” → success, “errors” → errors).

**Local steps**

- Evaluate Platform.has\_permission(“Bank Transaction”, “create”, throw = true).
- Evaluate Platform.has\_permission(“Bank Account”, doc = bank\_account, throw = true).
- Set header\_map from get\_header\_mapping(columns, bank\_account).
- Set success from 0.
- Set errors from 0.
- For each d in json.loads(data).
  - If all(generator of item is identical to no value for item drawn from d) is identical to true.
    - Draw item from d.
    - Continue with the next iteration or loop test.
  - Set fields from mapping().
  - For each tuple(key, value) in header\_map.items().
    - Evaluate fields.update(mapping(key → d at (int(value) − 1))).
  - Attempt the following.
    - Set bank\_transaction from Platform.get\_doc(mapping(“doctype” → “Bank Transaction”)).
    - Evaluate bank\_transaction.update(fields).
    - Set bank\_transaction.date from getdate(parse\_date(bank\_transaction.date)).
    - Set bank\_transaction.bank\_account from bank\_account.
    - Evaluate bank\_transaction.insert().
    - Evaluate bank\_transaction.submit().
    - Update success using + 1.
  - On failure (Exception).
    - Evaluate bank\_transaction.log\_error(“Bank entry creation failed”).
    - Update errors using + 1.
- Return mapping(“success” → success, “errors” → errors).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, “create”, throw = true), Platform.has\_permission(“Bank Account”, doc = bank\_account, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L448)

<a id="op-d7d33ead446643"></a>
### Get header mapping

`operation_enterprise_accounts_record_definitions_bank_transaction_bank_transaction_upload_business_behavior_get_header_mapping`

**Inputs** columns, bank\_account.

**Explicit results** header\_map.

**Local steps**

- Set mapping from get\_bank\_mapping(bank\_account).
- Set header\_map from mapping().
- For each column in json.loads(columns).
  - If column at “content” belongs to mapping.
    - Evaluate header\_map.update(mapping(mapping at column at “content” → column at “colIndex”)).
- Return header\_map.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L450)

<a id="op-a2362176878c69"></a>
### Get bank mapping

`operation_enterprise_accounts_record_definitions_bank_transaction_bank_transaction_upload_business_behavior_get_bank_mapping`

**Inputs** bank\_account.

**Record and data access** read “Bank Account” via get\_cached\_value · resolve a document from “Bank” via get\_doc.

**Explicit results** mapping.

**Local steps**

- Set bank\_name from Platform.get\_cached\_value(“Bank Account”, bank\_account, “bank”).
- Set bank from Platform.get\_doc(“Bank”, bank\_name).
- Set mapping from mapping of row.file\_field → row.bank\_transaction\_field for row drawn from bank.bank\_transaction\_mapping.
  - Draw row from bank.bank\_transaction\_mapping.
- Return mapping.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Bank Account”, bank\_account, “bank”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0028.json#L929) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L449)

## Record · Bank transaction rule

[Record definition](../../../../data/record-types/bank_transaction_rule.json)

<a id="op-869868780dc6ad"></a>
### Is expr eval formula

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_is_expr_evaluate_formula`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** formula.

**Explicit result forms** Boolean false, a comparison result.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0029.json#L5584) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L506) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L486)

<a id="op-d52a7d5992f957"></a>
### Validate amount formula

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_validate_amount_formula`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** formula.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 5 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0029.json#L5797) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L510) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L490)

<a id="op-ddb5b5ef340d03"></a>
### Bank Transaction Rule.before insert

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_bank_transaction_rule_before_insert`

**Inputs** self.

**Record and data access** read “Bank Transaction Rule” via get\_value.

**Local steps**

- If not self.priority.
  - Set highest\_priority from Platform.db.get\_value(“Bank Transaction Rule”, filters = mapping(“company” → self.company), fieldname = “priority”, order\_by = “priority DESC”).
  - Set self.priority from ((highest\_priority or 0) + 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in highest\_priority → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0029.json#L6351) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L502) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L482)

<a id="op-b636de4669c27e"></a>
### Bank Transaction Rule.validate

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_bank_transaction_rule_validate`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Min amount cannot be greater than max amount.” · validation helper — translated “Party type is required to create a payment entry.” · validation helper — translated “Party is required create a payment entry.” · validation helper — translated “Party account is required to create a payment entry.” · validation helper — translated “Please add an account for the Bank Entry rule.” · 4 additional forms in the steps below.

**Local steps**

- If (self.min\_amount and self.max\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.min\_amount → self.max\_amount.
  - If self.min\_amount &gt; self.max\_amount.
    - Call the validation error handler Platform.throw(translated “Min amount cannot be greater than max amount.”).
- If self.classify\_as equals “Payment Entry”.
  - If not self.party\_type.
    - Call the validation error handler Platform.throw(translated “Party type is required to create a payment entry.”).
  - If not self.party.
    - Call the validation error handler Platform.throw(translated “Party is required create a payment entry.”).
  - If not self.account.
    - Call the validation error handler Platform.throw(translated “Party account is required to create a payment entry.”).
- If self.classify\_as equals “Bank Entry”.
  - If (not self.bank\_entry\_type or self.bank\_entry\_type equals “Single Account”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.bank\_entry\_type → self.bank\_entry\_type equals “Single Account”.
    - If not self.account.
      - Call the validation error handler Platform.throw(translated “Please add an account for the Bank Entry rule.”).
  - Otherwise.
    - If self.bank\_entry\_type equals “Multiple Accounts”.
      - If not self.accounts.
        - Call the validation error handler Platform.throw(translated “Please configure accounts for the Bank Entry rule.”).
      - For each tuple(index, account) in enumerate(self.accounts).
        - If index equals (len(self.accounts) − 1).
          - If (account.debit or account.credit).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.debit → account.credit.
            - Call the validation error handler Platform.throw(translated “The last account row must not have any debit or credit amounts set.”).
        - Otherwise.
          - If account.debit.
            - Evaluate validate\_amount\_formula(account.debit).
          - If account.credit.
            - Evaluate validate\_amount\_formula(account.credit).
- For each rule in self.description\_rules.
  - If rule.check equals “Regex”.
    - Attempt the following.
      - Evaluate re.compile(rule.value).
    - On failure (re.error).
      - Call the validation error handler Platform.throw(translated “Invalid regex pattern.”).
- If self.bank\_entry\_type equals “Single Account”.
  - Set account\_company from Platform.get\_cached\_value(“Account”, self.account, “company”).
  - If account\_company differs from self.company.
    - Call the validation error handler Platform.throw(translated “Account company does not match with the rule company.”).
- If self.bank\_entry\_type equals “Multiple Accounts”.
  - For each account in self.accounts.
    - Set account\_company from Platform.get\_cached\_value(“Account”, account.account, “company”).
    - If account\_company differs from self.company.
      - Call the validation error handler Platform.throw(translated “Account company does not match with the rule company.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.account, “company”), Platform.get\_cached\_value(“Account”, account.account, “company”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L505) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L485)

<a id="op-13dd4d4233d095"></a>
### Bank Transaction Rule.on trash

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_bank_transaction_rule_on_trash`

**Inputs** self.

**State and service calls** request set\_value on “Bank Transaction”.

**Local steps**

- Attempt the following.
  - Evaluate Platform.db.set\_value(“Bank Transaction”, mapping(“matched\_transaction\_rule” → self.name), “matched\_transaction\_rule”, no value).
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L504) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L484)

<a id="op-793478f4735e0d"></a>
### Bank Transaction Rule.after delete

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_bank_transaction_rule_after_delete`

**Inputs** self.

**Record and data access** read “Bank Transaction Rule” via get\_all.

**State and service calls** request set\_value on “Bank Transaction Rule”.

**Local steps**

- Set rules from Platform.get\_all(“Bank Transaction Rule”, filters = mapping(“company” → self.company, “name” → list(“!=”, self.name)), order\_by = “priority asc”).
- For each tuple(i, rule) in enumerate(rules).
  - Evaluate Platform.db.set\_value(“Bank Transaction Rule”, rule.name, “priority”, (i + 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0030.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L501) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L481)

<a id="op-b620fc718ed445"></a>
### Bank Transaction Rule.evaluate rule

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_bank_transaction_rule_evaluate_rule`

**Inputs** self, transaction.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If self.company differs from transaction.company.
  - Return false.
- If self.transaction\_type equals “Withdrawal”.
  - If transaction.withdrawal equals 0.0.
    - Return false.
- If self.transaction\_type equals “Deposit”.
  - If transaction.deposit equals 0.0.
    - Return false.
- Set transaction\_amount from (transaction.withdrawal or transaction.deposit).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction.withdrawal → transaction.deposit.
- If (self.min\_amount and transaction\_amount &lt; self.min\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.min\_amount → transaction\_amount &lt; self.min\_amount.
  - Return false.
- If (self.max\_amount and transaction\_amount &gt; self.max\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.max\_amount → transaction\_amount &gt; self.max\_amount.
  - Return false.
- For each rule\_desc\_rule in self.description\_rules.
  - Set desc from (transaction.description or empty text).lower().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in transaction.description → empty text.
  - Set value from (rule\_desc\_rule.value or empty text).lower().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule\_desc\_rule.value → empty text.
  - If rule\_desc\_rule.check equals “Contains”.
    - If value belongs to desc.
      - Return true.
  - If rule\_desc\_rule.check equals “Starts With”.
    - If desc.startswith(value).
      - Return true.
  - If rule\_desc\_rule.check equals “Ends With”.
    - If desc.endswith(value).
      - Return true.
  - If rule\_desc\_rule.check equals “Regex”.
    - If re.search(value, desc).
      - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0030.json#L346) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L503) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L483)

<a id="op-d8191d98f40f12"></a>
### Scheduler run rule evaluation

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_scheduler_run_rule_evaluation`

**Inputs** no declared parameters.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Local steps**

- Set automatically\_run\_rules\_on\_unreconciled\_transactions from Platform.db.get\_single\_value(“Accounts Settings”, “automatically\_run\_rules\_on\_unreconciled\_transactions”).
- If automatically\_run\_rules\_on\_unreconciled\_transactions.
  - Evaluate \_run\_rule\_evaluation(force\_evaluate = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Accounts Settings”, “automatically\_run\_rules\_on\_unreconciled\_transactions”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0030.json#L1008) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L489)

<a id="op-64816c5355bf48"></a>
### Run rule evaluation

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_run_rule_evaluation`

**Inputs** force\_evaluate = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue.

**Local steps**

- Evaluate Platform.has\_permission(“Bank Transaction”, ptype = “write”, throw = true).
- Evaluate Platform.enqueue(method = \_run\_rule\_evaluation, force\_evaluate = force\_evaluate).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bank Transaction”, ptype = “write”, throw = true) · service or queued work from Platform.enqueue(method = \_run\_rule\_evaluation, force\_evaluate = force\_evaluate).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0002.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L507) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L487)

<a id="op-b7efc68690a941"></a>
### Run rule evaluation

`operation_enterprise_accounts_record_definitions_bank_transaction_rule_business_behavior_run_rule_evaluation_2`

**Inputs** force\_evaluate = false.

**Record and data access** read “Bank Transaction Rule” via get\_all · read “Bank Transaction” via get\_all · resolve a document from “Bank Transaction Rule” via get\_doc.

**State and service calls** request set\_value on “Bank Transaction”.

**Explicit results** no value.

**Local steps**

- Set rules from Platform.get\_all(“Bank Transaction Rule”, fields = list(“name”), order\_by = “priority asc”).
- If not rules.
  - Return no value.
- Set filters from mapping(“status” → “Unreconciled”, “docstatus” → 1).
- If not force\_evaluate.
  - Set filters at “is\_rule\_evaluated” from 0.
- Set unreconciled\_transactions from Platform.get\_all(“Bank Transaction”, filters = filters, fields = list(“name”, “bank\_account”, “company”, “date”, …)).
- If not unreconciled\_transactions.
  - Return no value.
- Set rule\_docs from list().
- For each rule in rules.
  - Set rule\_doc from Platform.get\_doc(“Bank Transaction Rule”, rule.name).
  - Evaluate rule\_docs.append(rule\_doc).
- For each transaction in unreconciled\_transactions.
  - Set matched\_rule from no value.
  - For each rule in rule\_docs.
    - If rule.evaluate\_rule(transaction).
      - Set matched\_rule from rule.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Evaluate Platform.db.set\_value(“Bank Transaction”, transaction.name, mapping(“is\_rule\_evaluated” → 1, “matched\_transaction\_rule” → matched\_rule.name when matched\_rule, otherwise no value)).
    - Value choice on matched\_rule — true gives matched\_rule.name, false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0030.json#L1284) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L488)

## Report · Billed items to be received

<a id="op-a796a7f03aee9d"></a>
### Execute

`operation_enterprise_accounts_report_billed_items_to_be_received_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Set data from (get\_data(filters) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_data(filters) → list().
- Set columns from get\_columns().
- Return tuple(columns, data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0231.json#L5091) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L691)

<a id="op-12de5e3c2c9ae6"></a>
### Get data

`operation_enterprise_accounts_report_billed_items_to_be_received_business_behavior_get_data`

**Inputs** report\_filters.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set as\_on\_date from report\_filters.get(“posting\_date”).
- Set invoice from Platform.qb.DocType(“Purchase Invoice”).
- Set invoice\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set item from Platform.qb.DocType(“Item”).
- Set received from get\_received\_as\_on(as\_on\_date).
- Set returned from get\_returned\_as\_on(as\_on\_date).
- Set invoice\_first\_returns from get\_receipt\_returns\_as\_on(as\_on\_date, “purchase\_invoice\_item”, “invoice\_first\_returns”).
- Set receipt\_first from get\_receipt\_first\_received\_as\_on(as\_on\_date).
- Set received\_qty from (((IfNull(received.qty, 0) − IfNull(invoice\_first\_returns.qty, 0)) + IfNull(receipt\_first.qty, 0)) − IfNull(returned.stock\_qty, 0)).
- Set returned\_qty from IfNull(returned.qty, 0).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- If report\_filters.get(“purchase\_invoice”).
  - Set query from query.where(invoice.name equals report\_filters.get(“purchase\_invoice”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0006.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L337) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L693)

<a id="op-9ee5686481be6f"></a>
### Get received as on

`operation_enterprise_binding_enterprise_accounts_report_billed_items_to_be_received_billed_items_to_be_received_get_received_as_on`

**Inputs** as\_on\_date.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).groupby(receipt\_item.purchase\_invoice\_item).as\_(“received”).

**Local steps**

- Set receipt from Platform.qb.DocType(“Purchase Receipt”).
- Set receipt\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).groupby(receipt\_item.purchase\_invoice\_item).as\_(“received”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L497) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1135)

<a id="op-e7c541625e2293"></a>
### Get returned as on

`operation_enterprise_binding_enterprise_accounts_report_billed_items_to_be_received_billed_items_to_be_received_get_returned_as_on`

**Inputs** as\_on\_date.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).groupby(debit\_note\_item.purchase\_invoice\_item).as\_(“returned”).

**Local steps**

- Set debit\_note from Platform.qb.DocType(“Purchase Invoice”).
- Set debit\_note\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set stock\_returned\_qty from Case().when(debit\_note.update\_stock equals 1, negative debit\_note\_item.received\_qty).else\_(0).
- Set billing\_only\_qty from Case().when(debit\_note.update\_stock equals 0, negative debit\_note\_item.qty).else\_(0).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isnotnull()).groupby(debit\_note\_item.purchase\_invoice\_item).as\_(“returned”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L498) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1136)

<a id="op-dbea00ce233e6a"></a>
### Get receipt first received as on

`operation_enterprise_binding_enterprise_accounts_report_billed_items_to_be_received_billed_items_to_be_received_get_receipt_first_received_as_on`

**Inputs** as\_on\_date.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….

**Local steps**

- Set invoice from Platform.qb.DocType(“Purchase Invoice”).
- Set invoice\_item from Platform.qb.DocType(“Purchase Invoice Item”).
- Set receipt from Platform.qb.DocType(“Purchase Receipt”).
- Set receipt\_item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set receipt\_returns from get\_receipt\_returns\_as\_on(as\_on\_date, “name”, “receipt\_returns”).
- Set debit\_notes from get\_returned\_as\_on(as\_on\_date).
- Set billed\_qty from (invoice\_item.qty − IfNull(debit\_notes.billing\_only\_qty, 0)).
- Set billed\_before from (get\_billed\_through(invoice, invoice\_item, billed\_qty) − billed\_qty).
- Set unallocated from ((receipt\_item.received\_qty − IfNull(receipt\_returns.qty, 0)) − billed\_before).
- Set allocated from nested operand in the contract().when(unallocated ≥ billed\_qty, billed\_qty).when(unallocated &gt; 0, unallocated).else\_(0).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L495) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1133)

<a id="op-512b36cdde5202"></a>
### Get billed through

`operation_enterprise_binding_enterprise_accounts_report_billed_items_to_be_received_billed_items_to_be_received_get_billed_through`

**Inputs** invoice, invoice\_item, billed\_qty.

**Explicit results** nested operand in the contract(nested operand in the contract).over(invoice\_item.pr\_detail).orderby(invoice.posting\_date, invoice.name, invoice\_item.idx).rows(analytics.Preceding(), analytics.CURRENT\_ROW).

**Local steps**

- Return nested operand in the contract(nested operand in the contract).over(invoice\_item.pr\_detail).orderby(invoice.posting\_date, invoice.name, invoice\_item.idx).rows(analytics.Preceding(), analytics.CURRENT\_ROW).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L494) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1132)
