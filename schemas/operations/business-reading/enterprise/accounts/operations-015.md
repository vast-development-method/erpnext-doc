# Accounting and settlement · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bank reconciliation tool

[Record definition](../../../../data/record-types/bank_reconciliation_tool.json)

<a id="op-5931e024fd93d7"></a>
### Get matching queries

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_matching_queries`

**Inputs** bank\_account, company, transaction, document\_types = no value, exact\_match = no value, account\_from\_to = no value, from\_date = no value, to\_date = no value, filter\_by\_reference\_date = no value, from\_reference\_date = no value, to\_reference\_date = no value, common\_filters = no value.

**Explicit results** queries.

**Local steps**

- Set queries from list().
- Set currency from get\_account\_currency(bank\_account).
- If “payment\_entry” belongs to document\_types.
  - Set query from get\_pe\_matching\_query(exact\_match, account\_from\_to, transaction, from\_date, …).
  - Evaluate queries.append(query).
- If “journal\_entry” belongs to document\_types.
  - Set query from get\_je\_matching\_query(exact\_match, transaction, from\_date, to\_date, …).
  - Evaluate queries.append(query).
- If (transaction.deposit &gt; 0.0 and “sales\_invoice” belongs to document\_types).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in transaction.deposit &gt; 0.0 → “sales\_invoice” belongs to document\_types.
  - Set query from get\_si\_matching\_query(exact\_match, currency, common\_filters, transaction).
  - Evaluate queries.append(query).
- If transaction.withdrawal &gt; 0.0.
  - If “purchase\_invoice” belongs to document\_types.
    - Set query from get\_pi\_matching\_query(exact\_match, currency, common\_filters).
    - Evaluate queries.append(query).
- If “bank\_transaction” belongs to document\_types.
  - Set query from get\_bt\_matching\_query(exact\_match, transaction).
  - Evaluate queries.append(query).
- Return queries.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L4689) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L287)

<a id="op-e38ada79e51d82"></a>
### Get bt matching query

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_bt_matching_query`

**Inputs** exact\_match, transaction.

**Explicit results** query.

**Local steps**

- Set bt from Platform.qb.DocType(“Bank Transaction”).
- Set field from “deposit” when transaction.withdrawal &gt; 0.0, otherwise “withdrawal”.
  - Value choice on transaction.withdrawal &gt; 0.0 — true gives “deposit”, false gives “withdrawal”.
- Set amount\_equality from getattr(bt, field) equals transaction.unallocated\_amount.
- Set amount\_rank from nested operand in the contract.terms.Case().when(amount\_equality, 1).else\_(0).
- Set amount\_condition from amount\_equality when exact\_match, otherwise getattr(bt, field) &gt; 0.0.
  - Value choice on exact\_match — true gives amount\_equality, false gives getattr(bt, field) &gt; 0.0.
- Set ref\_rank from nested operand in the contract.terms.Case().when(bt.reference\_number equals transaction.reference\_number, 1).else\_(0).
- Set unallocated\_rank from nested operand in the contract.terms.Case().when(bt.unallocated\_amount equals transaction.unallocated\_amount, 1).else\_(0).
- Set party\_condition from ((bt.party\_type equals transaction.party\_type bitwise and bt.party equals transaction.party) bitwise and bt.party.isnotnull()).
- Set party\_rank from nested operand in the contract.terms.Case().when(party\_condition, 1).else\_(0).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.bank\_account equals nested operand in the contract.bank\_account).where(amount\_condition).where(bt.docstat ….
- Return query.

**Values supplied outside this operation** selected callable from getattr(bt, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0018.json#L5384) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L284)

<a id="op-8290b933b4ca57"></a>
### Get pe matching query

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_pe_matching_query`

**Inputs** exact\_match, account\_from\_to, transaction, from\_date, to\_date, filter\_by\_reference\_date, from\_reference\_date, to\_reference\_date, common\_filters.

**Explicit results** query.

**Local steps**

- Set to\_from from “to” when transaction.deposit &gt; 0.0, otherwise “from”.
  - Value choice on transaction.deposit &gt; 0.0 — true gives “to”, false gives “from”.
- Set currency\_field from formatted text paid\_{to\_from}\_account\_currency.
- Set payment\_type from “Receive” when transaction.deposit &gt; 0.0, otherwise “Pay”.
  - Value choice on transaction.deposit &gt; 0.0 — true gives “Receive”, false gives “Pay”.
- Set pe from Platform.qb.DocType(“Payment Entry”).
- Set ref\_condition from pe.reference\_no equals transaction.reference\_number.
- Set ref\_rank from nested operand in the contract.terms.Case().when(ref\_condition, 1).else\_(0).
- Set amount\_field from pe.received\_amount\_after\_tax when account\_from\_to equals “paid\_to”, otherwise pe.paid\_amount\_after\_tax.
  - Value choice on account\_from\_to equals “paid\_to” — true gives pe.received\_amount\_after\_tax, false gives pe.paid\_amount\_after\_tax.
- Set amount\_equality from amount\_field equals transaction.unallocated\_amount.
- Set amount\_rank from nested operand in the contract.terms.Case().when(amount\_equality, 1).else\_(0).
- Set amount\_condition from amount\_equality when exact\_match, otherwise amount\_field &gt; 0.0.
  - Value choice on exact\_match — true gives amount\_equality, false gives amount\_field &gt; 0.0.
- Set party\_condition from ((pe.party\_type equals transaction.party\_type bitwise and pe.party equals transaction.party) bitwise and pe.party.isnotnull()).
- Set party\_rank from nested operand in the contract.terms.Case().when(party\_condition, 1).else\_(0).
- Set filter\_by\_date from pe.posting\_date.between(from\_date, to\_date).
- If cint(filter\_by\_reference\_date).
  - Set filter\_by\_date from pe.reference\_date.between(from\_reference\_date, to\_reference\_date).
- Set query from nested operand in the contract(nested operand in the contract).where(amount\_condition).where(filter\_by\_date).orderby(pe.reference\_date when cint(filter\_by\_reference\_date), otherwise pe.posting\_date).
  - Value choice on cint(filter\_by\_reference\_date) — true gives pe.reference\_date, false gives pe.posting\_date.
- If Platform.flags.auto\_reconcile\_vouchers is identical to true.
  - Set query from query.where(ref\_condition).
- Return query.

**Values supplied outside this operation** selected callable from getattr(pe, currency\_field), getattr(pe, account\_from\_to).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0019.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L289)

<a id="op-2e921f3f23c3c1"></a>
### Get je matching query

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_je_matching_query`

**Inputs** exact\_match, transaction, from\_date, to\_date, filter\_by\_reference\_date, from\_reference\_date, to\_reference\_date, common\_filters.

**Explicit results** query.

**Local steps**

- Set cr\_or\_dr from “credit” when transaction.withdrawal &gt; 0.0, otherwise “debit”.
  - Value choice on transaction.withdrawal &gt; 0.0 — true gives “credit”, false gives “debit”.
- Set je from Platform.qb.DocType(“Journal Entry”).
- Set jea from Platform.qb.DocType(“Journal Entry Account”).
- Set amount\_field from formatted text {cr\_or\_dr}\_in\_account\_currency.
- Set filter\_by\_date from je.posting\_date.between(from\_date, to\_date).
- If cint(filter\_by\_reference\_date).
  - Set filter\_by\_date from je.cheque\_date.between(from\_reference\_date, to\_reference\_date).
- Set subquery from nested operand in the contract(nested operand in the contract).where(filter\_by\_date).groupby(je.name).orderby(je.cheque\_date when cint(filter\_by\_reference\_date), otherwise je.posting\_date).
  - Value choice on cint(filter\_by\_reference\_date) — true gives je.cheque\_date, false gives je.posting\_date.
- If Platform.flags.auto\_reconcile\_vouchers is identical to true.
  - Set subquery from subquery.where(je.cheque\_no equals transaction.reference\_number).
- Set ref\_rank from nested operand in the contract.terms.Case().when(subquery.reference\_no equals transaction.reference\_number, 1).else\_(0).
- Set amount\_equality from subquery.paid\_amount equals transaction.unallocated\_amount.
- Set amount\_rank from nested operand in the contract.terms.Case().when(amount\_equality, 1).else\_(0).
- Set query from nested operand in the contract.qb.from\_(subquery).select(“\*”, ((nested operand in the contract + nested operand in the contract) + 1).as\_(“rank”)).where(amount\_equality when exact\_match, otherwise subquery ….
  - Value choice on exact\_match — true gives amount\_equality, false gives subquery.paid\_amount &gt; 0.0.
- Return query.

**Values supplied outside this operation** selected callable from getattr(jea, amount\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L285)

<a id="op-0992c246797e2a"></a>
### Get si matching query

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_sales_invoice_matching_query`

**Inputs** exact\_match, currency, common\_filters, transaction.

**Explicit results** query.

**Local steps**

- Set si from Platform.qb.DocType(“Sales Invoice”).
- Set sip from Platform.qb.DocType(“Sales Invoice Payment”).
- Set ref\_condition from sip.reference\_no equals transaction.reference\_number.
- Set ref\_rank from nested operand in the contract.terms.Case().when(ref\_condition, 1).else\_(0).
- Set amount\_equality from sip.amount equals common\_filters.amount.
- Set amount\_rank from nested operand in the contract.terms.Case().when(amount\_equality, 1).else\_(0).
- Set amount\_condition from amount\_equality when exact\_match, otherwise sip.amount &gt; 0.0.
  - Value choice on exact\_match — true gives amount\_equality, false gives sip.amount &gt; 0.0.
- Set party\_condition from si.customer equals common\_filters.party.
- Set party\_rank from nested operand in the contract.terms.Case().when(party\_condition, 1).else\_(0).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.account equals nested operand in the contract.bank\_account).where(amount\_condition).where(si.currency equ ….
- If Platform.flags.auto\_reconcile\_vouchers is identical to true.
  - Set query from query.where(ref\_condition).
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0019.json#L2727) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L292)

<a id="op-24da3869e17505"></a>
### Get pi matching query

`operation_enterprise_accounts_record_definitions_bank_reconciliation_tool_business_behavior_get_purchase_invoice_matching_query`

**Inputs** exact\_match, currency, common\_filters.

**Explicit results** query.

**Local steps**

- Set purchase\_invoice from Platform.qb.DocType(“Purchase Invoice”).
- Set amount\_equality from purchase\_invoice.paid\_amount equals common\_filters.amount.
- Set amount\_rank from nested operand in the contract.terms.Case().when(amount\_equality, 1).else\_(0).
- Set amount\_condition from amount\_equality when exact\_match, otherwise purchase\_invoice.paid\_amount &gt; 0.0.
  - Value choice on exact\_match — true gives amount\_equality, false gives purchase\_invoice.paid\_amount &gt; 0.0.
- Set party\_condition from purchase\_invoice.supplier equals common\_filters.party.
- Set party\_rank from nested operand in the contract.terms.Case().when(party\_condition, 1).else\_(0).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.cash\_bank\_account equals nested operand in the contract.bank\_account).where(amount\_condition).where(purch ….
- Return query.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0019.json#L3753) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L290)

## Record · Bank statement import

[Record definition](../../../../data/record-types/bank_statement_import.json)

<a id="op-1f0f8a8b71ae3d"></a>
### Bank Statement Import.initialize

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_bank_statement_import_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L1528) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L310)

<a id="op-87d2f86bde61a9"></a>
### Bank Statement Import.validate

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_bank_statement_import_validate`

**Inputs** self.

**Record and data access** resolve a document from “Bank” via get\_doc.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If (not (self.import\_file or self.google\_sheets\_url) or (doc\_before\_save and doc\_before\_save.import\_file differs from self.import\_file) or (doc\_before\_save and doc\_before\_save.google\_sheets\_url differs from s ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (self.import\_file or self.google\_sheets\_url) → (doc\_before\_save and doc\_before\_save.import\_file differs from self.import\_file) → (doc\_before\_save and doc\_before\_save.google\_sheets\_url differs from self.google\_sheets\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.import\_file → self.google\_sheets\_url.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.import\_file differs from self.import\_file.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save → doc\_before\_save.google\_sheets\_url differs from self.google\_sheets\_url.
  - Set template\_options\_dict from mapping().
  - Set column\_to\_field\_map from mapping().
  - Set bank from Platform.get\_doc(“Bank”, self.bank).
  - For each i in bank.bank\_transaction\_mapping.
    - Set column\_to\_field\_map at i.file\_field from i.bank\_transaction\_field.
  - Set template\_options\_dict at “column\_to\_field\_map” from column\_to\_field\_map.
  - Set self.template\_options from json.dumps(template\_options\_dict).
  - Set self.template\_warnings from empty text.
- If (self.import\_file and not nested operand in the contract.import\_file.lower().endswith(“.txt”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.import\_file → not self.import\_file.lower().endswith(“.txt”).
  - Evaluate self.get\_importer().
  - Evaluate self.validate\_google\_sheets\_url().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L332) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L312)

<a id="op-bac6a44daff2f1"></a>
### Bank Statement Import.start import

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_bank_statement_import_start_import`

**Inputs** self.

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**Explicit results** job\_id · no value.

**Explicit failure paths** validation helper — translated “Please add the Bank Account column” · validation helper — translated “Scheduler is inactive. Cannot import data.”.

**Local steps**

- Set preview from Platform.get\_doc(“Bank Statement Import”, self.name).get\_preview\_from\_template(self.import\_file, self.google\_sheets\_url).
- If “Bank Account” does not belong to json.dumps(preview at “columns”).
  - Call the validation error handler Platform.throw(translated “Please add the Bank Account column”).
- Bind dependencies is\_job\_enqueued.
- Bind dependencies is\_scheduler\_inactive.
- Set run\_now from (Platform.in\_test or Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → Platform.conf.developer\_mode.
- If (is\_scheduler\_inactive() and not run\_now).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_scheduler\_inactive() → not run\_now.
  - Call the validation error handler Platform.throw(translated “Scheduler is inactive. Cannot import data.”, title = translated “Scheduler Inactive”).
- Set job\_id from formatted text bank\_statement\_import::{self.name}.
- If not is\_job\_enqueued(job\_id).
  - Evaluate enqueue(start\_import, queue = “default”, timeout = 6000, event = “data\_import”, job\_id = job\_id, …).
  - Return job\_id.
- Return no value.

**Values supplied outside this operation** service or queued work from enqueue(start\_import, queue = “default”, timeout = 6000, event = “data\_import”, job\_id = job\_id, …).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L2052) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L311)

<a id="op-341653bd4e6f72"></a>
### Preprocess mt940 content

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_preprocess_mt_940_content`

**Inputs** content.

**Declared result** str.

**Explicit results** content · processed\_content.

**Local steps**

- If “:28C:” does not belong to content.
  - Return content.
- Set pattern from re.compile(“(?m)^(:28C:)(\\d{6,})(/\\d+)?(\\s\*)$”).
- Bind local operation replace\_statement\_number for subsequent calls.
- Set processed\_content from pattern.sub(replace\_statement\_number, content).
- Return processed\_content.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L2633) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L323)

<a id="op-c8a8f5f4acb83d"></a>
### Preprocess mt940 content.replace statement number

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_preprocess_mt_940_content_replace_statement_number`

**Inputs** match.

**Explicit results** (((prefix + statement\_num) + sequence\_part) + trailing\_space).

**Local steps**

- Set prefix from match.group(1).
- Set statement\_num from match.group(2).
- Set sequence\_part from (match.group(3) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in match.group(3) → empty text.
- Set trailing\_space from (match.group(4) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in match.group(4) → empty text.
- If len(statement\_num) &gt; 5.
  - Set statement\_num from statement\_num at slice negative 5 to no value.
- Return (((prefix + statement\_num) + sequence\_part) + trailing\_space).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L3017) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L324)

<a id="op-5a665605d16b37"></a>
### Get transaction reference

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_get_transaction_reference`

**Inputs** txn\_data.

**Declared result** str.

**Explicit results** customer\_reference · ((txn\_data.get(“bank\_reference”) or empty text).strip() or (txn\_data.get(“transaction\_reference”) or empty text).strip()).

**Local steps**

- Set customer\_reference from (txn\_data.get(“customer\_reference”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in txn\_data.get(“customer\_reference”) → empty text.
- If len(customer\_reference) equals MT940\_CUSTOMER\_REFERENCE\_MAX\_LEN.
  - Update customer\_reference using + (txn\_data.get(“extra\_details”) or empty text).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in txn\_data.get(“extra\_details”) → empty text.
- If (customer\_reference and customer\_reference.upper() differs from “NONREF”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in customer\_reference → customer\_reference.upper() differs from “NONREF”.
  - Return customer\_reference.
- Return ((txn\_data.get(“bank\_reference”) or empty text).strip() or (txn\_data.get(“transaction\_reference”) or empty text).strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (txn\_data.get(“bank\_reference”) or empty text).strip() → (txn\_data.get(“transaction\_reference”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in txn\_data.get(“bank\_reference”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in txn\_data.get(“transaction\_reference”) → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L3279) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L320)

<a id="op-0207d4b3a6742a"></a>
### Convert mt940 to csv

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_convert_mt_940_to_comma_separated_values`

**Inputs** data\_import, mt940\_file\_path.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**Explicit results** saved\_file.file\_url.

**Explicit failure paths** validation helper — translated “The uploaded file does not appear to be in valid MT940 format.” · validation helper — translated “MT940 file detected. Please enable 'Import MT940 Format' to proceed.” · validation helper — translated “Failed to parse MT940 format. Error: {0}”.format(str(e)) · validation helper — translated “Parsed file is not in valid MT940 format or contains no transactions.”.

**Local steps**

- Set doc from Platform.get\_doc(“Bank Statement Import”, data\_import).
- Evaluate doc.check\_permission(“write”).
- Set tuple(\_file\_doc, content) from get\_file(mt940\_file\_path).
- Set is\_mt940 from is\_mt940\_format(content).
- If not is\_mt940.
  - Call the validation error handler Platform.throw(translated “The uploaded file does not appear to be in valid MT940 format.”).
- If (is\_mt940 and not doc.import\_mt940\_fromat).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_mt940 → not doc.import\_mt940\_fromat.
  - Call the validation error handler Platform.throw(translated “MT940 file detected. Please enable 'Import MT940 Format' to proceed.”).
- Attempt the following.
  - Set processed\_content from preprocess\_mt940\_content(content).
  - Set transactions from mt940.parse(processed\_content).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Failed to parse MT940 format. Error: {0}”.format(str(e))).
- If not transactions.
  - Call the validation error handler Platform.throw(translated “Parsed file is not in valid MT940 format or contains no transactions.”).
- Set csv\_buffer from io.StringIO().
- Set writer from csv.writer(csv\_buffer).
- Set headers from list(“Date”, “Deposit”, “Withdrawal”, “Description”, …).
- Evaluate writer.writerow(headers).
- For each txn in transactions.
  - Set txn\_date from getattr(txn, “date”, no value).
  - Set raw\_date from txn.data.get(“date”, empty text).
  - If txn\_date.
    - Set date\_str from txn\_date.strftime(“%Y-%m-%d”).
  - Otherwise.
    - If isinstance(raw\_date, (date bitwise or datetime)).
      - Set date\_str from raw\_date.strftime(“%Y-%m-%d”).
    - Otherwise.
      - Set date\_str from str(raw\_date).
  - Set raw\_amount from str(txn.data.get(“amount”, empty text)).
  - Set parts from raw\_amount.strip().split().
  - Set amount\_value from float(parts at 0) when parts, otherwise 0.0.
    - Value choice on parts — true gives float(parts at 0), false gives 0.0.
  - Set deposit from amount\_value when amount\_value &gt; 0, otherwise empty text.
    - Value choice on amount\_value &gt; 0 — true gives amount\_value, false gives empty text.
  - Set withdrawal from abs(amount\_value) when amount\_value &lt; 0, otherwise empty text.
    - Value choice on amount\_value &lt; 0 — true gives abs(amount\_value), false gives empty text.
  - Set description from (txn.data.get(“transaction\_details”) or txn.data.get(“extra\_details”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in txn.data.get(“transaction\_details”) → txn.data.get(“extra\_details”) → empty text.
  - Set reference from get\_transaction\_reference(txn.data).
  - Set currency from txn.data.get(“currency”, empty text).
  - Evaluate writer.writerow(list(date\_str, deposit, withdrawal, description, …)).
- Set csv\_content from csv\_buffer.getvalue().encode(“utf-8”).
- Evaluate csv\_buffer.close().
- Set filename from formatted text {Platform.utils.now\_datetime().strftime(“%Y%m%d%H%M%S”)}\_converted\_mt940.csv.
- Set saved\_file from save\_file(filename, csv\_content, doc.doctype, doc.name, is\_private = true, df = “import\_file”).
- Return saved\_file.file\_url.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”) · selected callable from getattr(txn, “date”, no value) · clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L333) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L313)

<a id="op-3374480e6aa7a6"></a>
### Get preview from template

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_get_preview_from_template`

**Inputs** data\_import, import\_file = no value, google\_sheets\_url = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**Explicit results** bsi.get\_preview\_from\_template(import\_file, google\_sheets\_url).

**Local steps**

- Set bsi from Platform.get\_doc(“Bank Statement Import”, data\_import).
- Evaluate bsi.check\_permission().
- Return bsi.get\_preview\_from\_template(import\_file, google\_sheets\_url).

**Values supplied outside this operation** effective access from bsi.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L319)

<a id="op-9497c824ddab4d"></a>
### Form start import

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_form_start_import`

**Inputs** data\_import.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**Explicit results** bsi.start\_import().

**Local steps**

- Set bsi from Platform.get\_doc(“Bank Statement Import”, data\_import).
- Evaluate bsi.check\_permission(“write”).
- Return bsi.start\_import().

**Values supplied outside this operation** effective access from bsi.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L316)

<a id="op-44954ede3aac8d"></a>
### Download errored template

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_download_errored_template`

**Inputs** data\_import\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**Local steps**

- Set data\_import from Platform.get\_doc(“Bank Statement Import”, data\_import\_name).
- Evaluate data\_import.check\_permission().
- Evaluate data\_import.export\_errored\_rows().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from data\_import.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L334) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L314)

<a id="op-1cb2ed19aa553b"></a>
### Download import log

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_download_import_log`

**Inputs** data\_import\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**Explicit results** bsi.download\_import\_log().

**Local steps**

- Set bsi from Platform.get\_doc(“Bank Statement Import”, data\_import\_name).
- Evaluate bsi.check\_permission().
- Return bsi.download\_import\_log().

**Values supplied outside this operation** effective access from bsi.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L335) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L315)

<a id="op-1ae1b67ee789fe"></a>
### Is mt940 format

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_is_mt_940_format`

**Inputs** content.

**Declared result** bool.

**Explicit results** all(generator of tag belongs to content for tag drawn from required\_tags).

**Local steps**

- Set required\_tags from list(“:20:”, “:25:”, “:28C:”, “:61:”).
- Return all(generator of tag belongs to content for tag drawn from required\_tags).
  - Draw tag from required\_tags.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L5657) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L321)

<a id="op-7cdc26796b275b"></a>
### Parse data from template

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_parse_data_from_template`

**Inputs** raw\_data.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each tuple(\_i, row) in enumerate(raw\_data).
  - If all(generator of v belongs to INVALID\_VALUES for v drawn from row).
    - Draw v from row.
    - Continue with the next iteration or loop test.
  - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L5774) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L322)

<a id="op-a88ea37349483d"></a>
### Start import

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_start_import`

**Inputs** data\_import, bank\_account, import\_file\_path, google\_sheets\_url, bank, template\_options.

**Record and data access** resolve a document from “Bank Statement Import” via get\_doc.

**State and service calls** rollback · call db\_set on data\_import · publish realtime with “data\_import\_refresh”.

**Local steps**

- Evaluate update\_mapping\_db(bank, template\_options).
- Set data\_import from Platform.get\_doc(“Bank Statement Import”, data\_import).
- Set file from import\_file\_path when import\_file\_path, otherwise google\_sheets\_url.
  - Value choice on import\_file\_path — true gives import\_file\_path, false gives google\_sheets\_url.
- Set import\_file from ImportFile(“Bank Transaction”, file = file, import\_type = “Insert New Records”).
- Set data from parse\_data\_from\_template(import\_file.raw\_data).
- If not data\_import.get(“payload\_count”).
  - Set data\_import.payload\_count from (len(data) − 1).
- If import\_file\_path.
  - Evaluate add\_bank\_account(data, bank\_account).
  - Evaluate write\_files(import\_file, data).
- Attempt the following.
  - Set i from Importer(data\_import.reference\_doctype, data\_import = data\_import).
  - Evaluate i.import\_data().
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate data\_import.db\_set(“status”, “Error”).
  - Evaluate data\_import.log\_error(“Bank Statement Import failed”).
- On exit, including pending return or failure.
  - Set Platform.flags.in\_import from false.
- Evaluate Platform.publish\_realtime(“data\_import\_refresh”, mapping(“data\_import” → data\_import.name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“data\_import\_refresh”, mapping(“data\_import” → data\_import.name)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L5939) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L325)

<a id="op-5493f0591c843b"></a>
### Update mapping db

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_update_mapping_database`

**Inputs** bank, template\_options.

**Record and data access** resolve a document from “Bank” via get\_doc.

**State and service calls** call save on bank.

**Local steps**

- Set bank from Platform.get\_doc(“Bank”, bank).
- For each d in bank.bank\_transaction\_mapping.
  - Evaluate d.delete().
- For each d in json.loads(template\_options) at “column\_to\_field\_map”.items().
  - Evaluate bank.append(“bank\_transaction\_mapping”, mapping(“bank\_transaction\_field” → d at 1, “file\_field” → d at 0)).
- Evaluate bank.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L326)

<a id="op-a2b65ce016d4e4"></a>
### Add bank account

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_add_bank_account`

**Inputs** data, bank\_account.

**Local steps**

- Set bank\_account\_loc from no value.
- If “Bank Account” does not belong to data at 0.
  - Evaluate data at 0.append(“Bank Account”).
- Otherwise.
  - For each tuple(loc, header) in enumerate(data at 0).
    - If header equals “Bank Account”.
      - Set bank\_account\_loc from loc.
- For each row in data at slice 1 to no value.
  - If bank\_account\_loc.
    - Set row at bank\_account\_loc from bank\_account.
  - Otherwise.
    - Evaluate row.append(bank\_account).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L329) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L309)

<a id="op-85556072d9e57a"></a>
### Write files

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_write_files`

**Inputs** import\_file, data.

**Local steps**

- Set full\_file\_path from import\_file.file\_doc.get\_full\_path().
- Set parts from import\_file.file\_doc.get\_extension().
- Set extension from parts at 1.
- Set extension from extension.lstrip(“.”).
- If extension equals “csv”.
  - Within open(full\_file\_path, “w”, newline = empty text) bound as file.
    - Set writer from csv.writer(file).
    - Evaluate writer.writerows(data).
- Otherwise.
  - If extension belongs to tuple(“xlsx”, “xls”).
    - Evaluate write\_xlsx(data, “trans”, file\_path = full\_file\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0020.json#L7089) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L348) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L328)

<a id="op-5173be9bb53f12"></a>
### Write xlsx

`operation_enterprise_accounts_record_definitions_bank_statement_import_business_behavior_write_spreadsheet_workbook`

**Inputs** data, sheet\_name, wb = no value, column\_widths = no value, file\_path = no value.

**State and service calls** call save on wb.

**Explicit results** true.

**Local steps**

- Set column\_widths from (column\_widths or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in column\_widths → list().
- If wb is identical to no value.
  - Set wb from openpyxl.Workbook(write\_only = true).
- Set ws from wb.create\_sheet(sheet\_name, 0).
- For each tuple(i, column\_width) in enumerate(column\_widths).
  - If column\_width.
    - Set ws.column\_dimensions at get\_column\_letter((i + 1)).width from column\_width.
- Set row1 from ws.row\_dimensions at 1.
- Set row1.font from Font(name = “Calibri”, bold = true).
- For each row in data.
  - Set clean\_row from list().
  - For each item in row.
    - If (isinstance(item, str) and sheet\_name does not belong to list(“Data Import Template”, “Data Export”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → sheet\_name does not belong to list(“Data Import Template”, “Data Export”).
      - Set value from handle\_html(item).
    - Otherwise.
      - Set value from item.
    - If (isinstance(item, str) and next(ILLEGAL\_CHARACTERS\_RE.finditer(value), no value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → next(ILLEGAL\_CHARACTERS\_RE.finditer(value), no value).
      - Set value from re.sub(ILLEGAL\_CHARACTERS\_RE, empty text, value).
    - Evaluate clean\_row.append(value).
  - Evaluate ws.append(clean\_row).
- Evaluate wb.save(file\_path).
- Return true.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0021.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L349) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L329)
