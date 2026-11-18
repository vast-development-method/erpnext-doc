# Accounting and settlement · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Account category

[Record definition](../../../../data/record-types/account_category.json)

<a id="op-0e41d099c57341"></a>
### Account Category.after rename

`operation_enterprise_accounts_record_definitions_account_category_business_behavior_account_category_after_rename`

**Inputs** self, old\_name, new\_name, merge.

**State and service calls** msgprint with translated “Updated {0} Financial Report Row(s) with new category name”.format(len(updated\_formulas)).

**Explicit results** no value.

**Local steps**

- Bind dependencies FormulaFieldUpdater.
- Set row from Platform.qb.DocType(“Financial Report Row”).
- Set rows from Platform.\_dict(nested operand in the contract.select(nested operand in the contract.name, nested operand in the contract.calculation\_formula).where(nested operand in the contract.calculation\_formula.like(f ….
- If not rows.
  - Return no value.
- Set updater from FormulaFieldUpdater(field\_name = “account\_category”, value\_mapping = mapping(old\_name → new\_name), exclude\_operators = list(“like”, “not like”)).
- Set updated\_formulas from updater.update\_in\_rows(rows).
- If updated\_formulas.
  - Evaluate Platform.msgprint(translated “Updated {0} Financial Report Row(s) with new category name”.format(len(updated\_formulas))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0010.json#L5528) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L125)

<a id="op-7a4afd4bcb641f"></a>
### Import account categories

`operation_enterprise_accounts_record_definitions_account_category_business_behavior_import_account_categories`

**Inputs** template\_path.

**Explicit results** no value.

**Local steps**

- Set categories\_file from os.path.join(template\_path, “account\_categories.json”).
- If not os.path.exists(categories\_file).
  - Return no value.
- Within open(categories\_file) bound as f.
  - Set categories from json.load(f, object\_hook = Platform.\_dict).
- Evaluate create\_account\_categories(categories).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0010.json#L5975) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L127)

<a id="op-990528773df0fe"></a>
### Create account categories

`operation_enterprise_accounts_record_definitions_account_category_business_behavior_create_account_categories`

**Inputs** categories.

**Record and data access** read DOCTYPE via get\_all · resolve a document from mapping(expand category\_data, “doctype” → DOCTYPE, “name” → category\_name) via get\_doc.

**Explicit results** no value.

**Local steps**

- If not categories.
  - Return no value.
- Set existing\_categories from set(Platform.get\_all(DOCTYPE, pluck = “name”)).
- Set new\_categories from list().
- For each category\_data in categories.
  - Set category\_name from category\_data.get(“account\_category\_name”).
  - If (not category\_name or category\_name belongs to existing\_categories).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not category\_name → category\_name belongs to existing\_categories.
    - Continue with the next iteration or loop test.
  - Set doc from Platform.get\_doc(mapping(expand category\_data, “doctype” → DOCTYPE, “name” → category\_name)).
  - Evaluate new\_categories.append(doc).
  - Evaluate existing\_categories.add(category\_name).
- If new\_categories.
  - Evaluate bulk\_insert(DOCTYPE, new\_categories).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0010.json#L6183) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L126)

## Record · Account closing balance

[Record definition](../../../../data/record-types/account_closing_balance.json)

<a id="op-32b2ffbba5daf5"></a>
### Make closing entries

`operation_enterprise_accounts_record_definitions_account_closing_balance_business_behavior_make_closing_entries`

**Inputs** closing\_entries, voucher\_name, company, closing\_date.

**State and service calls** request bulk\_insert on “Account Closing Balance”.

**Explicit results** no value.

**Local steps**

- Set accounting\_dimensions from get\_accounting\_dimensions().
- Set previous\_closing\_entries from get\_previous\_closing\_entries(company, closing\_date, accounting\_dimensions).
- Set combined\_entries from (closing\_entries + previous\_closing\_entries).
- Set merged\_entries from aggregate\_with\_last\_account\_closing\_balance(combined\_entries, accounting\_dimensions).
- If not merged\_entries.
  - Return no value.
- Set exchange\_rate from get\_reporting\_currency\_exchange\_rate(company, closing\_date).
- Set timestamp from now().
- Set rows from list of get\_closing\_balance\_row(value, voucher\_name, closing\_date, exchange\_rate, …) for value drawn from merged\_entries.values().
  - Draw value from merged\_entries.values().
- Evaluate Platform.db.bulk\_insert(“Account Closing Balance”, fields = list(rows at 0), values = list of tuple(row.values()) for row drawn from rows, chunk\_size = 10000).
  - Draw row from rows.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L154) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L147)

<a id="op-aebadc20d1f8ed"></a>
### Get closing balance row

`operation_enterprise_binding_enterprise_accounts_doctype_account_closing_balance_account_closing_balance_get_closing_balance_row`

**Inputs** value, voucher\_name, closing\_date, exchange\_rate, timestamp.

**State and service calls** request new\_doc for “Account Closing Balance”.

**Explicit results** cle.get\_valid\_dict(convert\_dates\_to\_str = true, ignore\_virtual = true).

**Local steps**

- Set cle from Platform.new\_doc(“Account Closing Balance”).
- Evaluate cle.update(value).
- Evaluate cle.update(value at “dimensions”).
- Evaluate cle.update(mapping(“period\_closing\_voucher” → voucher\_name, “closing\_date” → closing\_date, “docstatus” → DocStatus.SUBMITTED, “owner” → Platform.session.user, …)).
- If exchange\_rate.
  - Evaluate set\_amount\_with\_exchange\_rate(cle, exchange\_rate).
- Evaluate cle.run\_method(“validate”).
- Evaluate cle.set\_new\_name().
- Return cle.get\_valid\_dict(convert\_dates\_to\_str = true, ignore\_virtual = true).

**Values supplied outside this operation** selected callable from cle.run\_method(“validate”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L756)

<a id="op-c48a55e5b3d3ed"></a>
### Aggregate with last account closing balance

`operation_enterprise_accounts_record_definitions_account_closing_balance_business_behavior_aggregate_with_last_account_closing_balance`

**Inputs** entries, accounting\_dimensions.

**Explicit results** merged\_entries.

**Local steps**

- Set merged\_entries from mapping().
- For each entry in entries.
  - Set tuple(key, key\_values) from generate\_key(entry, accounting\_dimensions).
  - Evaluate merged\_entries.setdefault(key, mapping(“debit” → 0, “credit” → 0, “debit\_in\_account\_currency” → 0, “credit\_in\_account\_currency” → 0)).
  - Set merged\_entries at key at “dimensions” from key\_values.
  - Update merged\_entries at key at “debit” using + entry.get(“debit”).
  - Update merged\_entries at key at “credit” using + entry.get(“credit”).
  - Update merged\_entries at key at “debit\_in\_account\_currency” using + entry.get(“debit\_in\_account\_currency”).
  - Update merged\_entries at key at “credit\_in\_account\_currency” using + entry.get(“credit\_in\_account\_currency”).
- Return merged\_entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0010.json#L6994) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L151) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L144)

<a id="op-4272137c433a60"></a>
### Generate key

`operation_enterprise_accounts_record_definitions_account_closing_balance_business_behavior_generate_key`

**Inputs** entry, accounting\_dimensions.

**Explicit results** tuple(tuple(key), key\_values).

**Local steps**

- Set key from list(cstr(entry.get(“account”)), cstr(entry.get(“account\_currency”)), cstr(entry.get(“cost\_center”)), cstr(entry.get(“project”)), …).
- Set key\_values from mapping(“company” → cstr(entry.get(“company”)), “account” → cstr(entry.get(“account”)), “account\_currency” → cstr(entry.get(“account\_currency”)), “cost\_center” → cstr(entry.get(“cost\_center”)), …).
- For each dimension in accounting\_dimensions.
  - Evaluate key.append(cstr(entry.get(dimension))).
  - Set key\_values at dimension from cstr(entry.get(dimension)).
- Return tuple(tuple(key), key\_values).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L152) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L145)

<a id="op-45ada260bb587f"></a>
### Get previous closing entries

`operation_enterprise_accounts_record_definitions_account_closing_balance_business_behavior_get_previous_closing_entries`

**Inputs** company, closing\_date, accounting\_dimensions.

**Record and data access** read “Period Closing Voucher” via get\_all.

**Explicit results** entries.

**Local steps**

- Set entries from list().
- Set last\_period\_closing\_voucher from Platform.db.get\_all(“Period Closing Voucher”, filters = mapping(“docstatus” → 1, “company” → company, “period\_end\_date” → tuple(“&lt;”, closing\_date)), fields = list(“name”), order\_by = “period\_end\_date desc” ….
- If last\_period\_closing\_voucher.
  - Set account\_closing\_balance from Platform.qb.DocType(“Account Closing Balance”).
  - Set query from Platform.qb.from\_(account\_closing\_balance).select(account\_closing\_balance.company, account\_closing\_balance.account, account\_closing\_balance.account\_currency, account\_closing\_balance.debit, …).
  - For each dimension in accounting\_dimensions.
    - Set query from query.select(account\_closing\_balance at dimension).
  - Set query from query.where(account\_closing\_balance.period\_closing\_voucher equals last\_period\_closing\_voucher at 0.name).
  - Set entries from query.run(as\_dict = 1).
- Return entries.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L783) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L153) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L146)

<a id="op-27e74a98da3880"></a>
### Set amount in reporting currency

`operation_enterprise_accounts_record_definitions_account_closing_balance_business_behavior_set_amount_in_reporting_currency`

**Inputs** cle, company, closing\_date.

**Local steps**

- If exchange\_rate bound to get\_reporting\_currency\_exchange\_rate(company, closing\_date).
  - Evaluate set\_amount\_with\_exchange\_rate(cle, exchange\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L155) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L148)

<a id="op-fc8444ee6885a1"></a>
### Get reporting currency exchange rate

`operation_enterprise_binding_enterprise_accounts_doctype_account_closing_balance_account_closing_balance_get_reporting_currency_exchange_rate`

**Inputs** company, closing\_date.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value · reporting\_currency\_exchange\_rate.

**Explicit failure paths** validation helper with ReportingCurrencyExchangeNotFoundError.

**Local steps**

- Set tuple(default\_currency, reporting\_currency) from Platform.get\_cached\_value(“Company”, company, list(“default\_currency”, “reporting\_currency”)).
- If not reporting\_currency.
  - Return no value.
- Set reporting\_currency\_exchange\_rate from get\_exchange\_rate(default\_currency, reporting\_currency, closing\_date).
- If not reporting\_currency\_exchange\_rate.
  - Call the validation error handler Platform.throw(title = translated “Reporting Currency Exchange Not Found”, msg = translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually. ….
- Return reporting\_currency\_exchange\_rate.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, list(“default\_currency”, “reporting\_currency”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L757)

<a id="op-4c8c1b36f3a82c"></a>
### Set amount with exchange rate

`operation_enterprise_binding_enterprise_accounts_doctype_account_closing_balance_account_closing_balance_set_amount_with_exchange_rate`

**Inputs** cle, reporting\_currency\_exchange\_rate.

**Local steps**

- Set debit\_in\_reporting\_currency from flt((cle.get(“debit”, 0) × reporting\_currency\_exchange\_rate)).
- Set credit\_in\_reporting\_currency from flt((cle.get(“credit”, 0) × reporting\_currency\_exchange\_rate)).
- Evaluate cle.update(mapping(“reporting\_currency\_exchange\_rate” → reporting\_currency\_exchange\_rate, “debit\_in\_reporting\_currency” → debit\_in\_reporting\_currency, “credit\_in\_reporting\_currency” → credit\_in\_reporting\_currency)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L758)

## Record · Accounting dimension

[Record definition](../../../../data/record-types/accounting_dimension.json)

<a id="op-9ab767756ab5f4"></a>
### Accounting Dimension.before insert

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.set\_fieldname\_and\_label().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set fieldname and label](operations-004.md#op-c3d7506b14abc4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L2702) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L173) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L163)

<a id="op-9237ea479432c4"></a>
### Accounting Dimension.validate

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_doctype().
- Evaluate validate\_column\_name(self.fieldname).
- If self.has\_value\_changed(“fieldname”).
  - Evaluate self.validate\_fieldname\_conflict().
- Evaluate self.validate\_dimension\_defaults().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate doctype](operations-004.md#op-2a5ce00e20aa70), [validate fieldname conflict](operations-004.md#op-1e5c943bfd4b53), [validate dimension defaults](operations-004.md#op-ea9a187fe201b1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L177) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L167)

<a id="op-2a5ce00e20aa70"></a>
### Accounting Dimension.validate doctype

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_validate_record_type`

**Inputs** self.

**Record and data access** read “Accounting Dimension” via get\_value.

**Explicit failure paths** validation helper — msg · validation helper — translated “{0} cannot be used as an accounting dimension as it is not a standalone document type.”.format(Platform.bold(self.document\_type)) · validation helper — translated “Document Type already used as a dimension”.

**Local steps**

- If self.document\_type belongs to tuple(expanded core\_doctypes\_list, “Accounting Dimension”, “Project”, “Cost Center”, …).
  - Set msg from translated “Not allowed to create accounting dimension for {0}”.format(self.document\_type).
  - Call the validation error handler Platform.throw(msg).
- Set meta from Platform.get\_meta(self.document\_type).
- If (meta.istable or meta.issingle).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.istable → meta.issingle.
  - Call the validation error handler Platform.throw(translated “{0} cannot be used as an accounting dimension as it is not a standalone document type.”.format(Platform.bold(self.document\_type))).
- Set exists from Platform.db.get\_value(“Accounting Dimension”, mapping(“document\_type” → self.document\_type), list(“name”)).
- If (exists and self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in exists → self.is\_new().
  - Call the validation error handler Platform.throw(translated “Document Type already used as a dimension”).
- If not self.is\_new().
  - Evaluate self.validate\_document\_type\_change().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate document type change](operations-004.md#op-3ae8a1b5a970a6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L2869) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L171)

<a id="op-3ae8a1b5a970a6"></a>
### Accounting Dimension.validate document type change

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_validate_document_type_change`

**Inputs** self.

**Record and data access** read “Accounting Dimension” via get\_value.

**Explicit failure paths** validation helper — message.

**Local steps**

- Set doctype\_before\_save from Platform.db.get\_value(“Accounting Dimension”, self.name, “document\_type”).
- If doctype\_before\_save differs from self.document\_type.
  - Set message from translated “Cannot change Reference Document Type.”.
  - Update message using + translated “Please create a new Accounting Dimension if required.”.
  - Call the validation error handler Platform.throw(message).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L3394) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L169)

<a id="op-1e5c943bfd4b53"></a>
### Accounting Dimension.validate fieldname conflict

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_validate_fieldname_conflict`

**Inputs** self.

**State and service calls** msgprint with translated “Fieldname {0} already exists in the following doctypes: {1}. A separate dimension field will not be added to …”.format(Platform.bold(self.fieldname), “, ”.join(generator of Platform.bold(d) for ….

**Local steps**

- Set conflicting\_doctypes from list().
- For each doctype in get\_doctypes\_with\_dimensions().
  - Set meta from Platform.get\_meta(doctype, cached = false).
  - If any(generator of f.fieldname equals self.fieldname for f drawn from meta.get(“fields”)).
    - Draw f from meta.get(“fields”).
    - Evaluate conflicting\_doctypes.append(doctype).
- If conflicting\_doctypes.
  - Evaluate Platform.msgprint(translated “Fieldname {0} already exists in the following doctypes: {1}. A separate dimension field will not be added to …”.format(Platform.bold(self.fieldname), “, ”.join(generator of Pl ….
    - Draw d from conflicting\_doctypes.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L3586) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L170)

<a id="op-ea9a187fe201b1"></a>
### Accounting Dimension.validate dimension defaults

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_validate_dimension_defaults`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Company {0} is added more than once”.format(Platform.bold(default.company)).

**Local steps**

- Set companies from list().
- For each default in self.get(“dimension\_defaults”).
  - If default.company does not belong to companies.
    - Evaluate companies.append(default.company).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Company {0} is added more than once”.format(Platform.bold(default.company))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L3974) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L178) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L168)

<a id="op-57132356ffd1b6"></a>
### Accounting Dimension.on update

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_on_update`

**Inputs** self.

**State and service calls** enqueue with make\_dimension\_in\_accounting\_doctypes.

**Local steps**

- If Platform.in\_test.
  - Evaluate make\_dimension\_in\_accounting\_doctypes(doc = self).
- Otherwise.
  - Evaluate Platform.enqueue(make\_dimension\_in\_accounting\_doctypes, doc = self, queue = “long”, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(make\_dimension\_in\_accounting\_doctypes, doc = self, queue = “long”, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L4186) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L175) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L165)

<a id="op-8decdd0c9774d4"></a>
### Accounting Dimension.on trash

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_on_trash`

**Inputs** self.

**State and service calls** enqueue with delete\_accounting\_dimension.

**Local steps**

- If Platform.in\_test.
  - Evaluate delete\_accounting\_dimension(doc = self).
- Otherwise.
  - Evaluate Platform.enqueue(delete\_accounting\_dimension, doc = self, queue = “long”, enqueue\_after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(delete\_accounting\_dimension, doc = self, queue = “long”, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L4311) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L174) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L164)

<a id="op-c3d7506b14abc4"></a>
### Accounting Dimension.set fieldname and label

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_accounting_dimension_set_fieldname_and_label`

**Inputs** self.

**Local steps**

- If not self.label.
  - Set self.label from cstr(self.document\_type).
- If not self.fieldname.
  - Set self.fieldname from scrub(self.label).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L4436) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L166)

<a id="op-e9d42edd672a66"></a>
### Make dimension in accounting doctypes

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_make_dimension_in_accounting_record_types`

**Inputs** doc, doclist = no value.

**Local steps**

- If not doclist.
  - Set doclist from get\_doctypes\_with\_dimensions().
- Set doc\_count from len(get\_accounting\_dimensions()).
- Set count from 0.
- Set repostable\_doctypes from get\_allowed\_types\_from\_settings(child\_doc = true).
- For each doctype in doclist.
  - If ((doc\_count + 1) modulo or format 2) equals 0.
    - Set insert\_after\_field from “dimension\_col\_break”.
  - Otherwise.
    - Set insert\_after\_field from “accounting\_dimensions\_section”.
  - Set df from mapping(“fieldname” → doc.fieldname, “label” → doc.label, “fieldtype” → “Link”, “options” → doc.document\_type, …).
    - Value choice on doctype belongs to repostable\_doctypes — true gives 1, false gives 0.
  - Set meta from Platform.get\_meta(doctype, cached = false).
  - Set fieldnames from list of d.fieldname for d drawn from meta.get(“fields”).
    - Draw d from meta.get(“fields”).
  - If df at “fieldname” does not belong to fieldnames.
    - If doctype equals “Budget”.
      - Evaluate add\_dimension\_to\_budget\_doctype(df.copy(), doc).
    - Otherwise.
      - Evaluate create\_custom\_field(doctype, df, ignore\_validate = true).
  - Update count using + 1.
  - Evaluate Platform.publish\_progress(((count × 100) ÷ len(doclist)), title = translated “Creating Dimensions...”).
  - Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L4573) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L192) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L182)

<a id="op-82e97712bf5539"></a>
### Add dimension to budget doctype

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_add_dimension_to_budget_record_type`

**Inputs** df, doc.

**Record and data access** read “Property Setter” via exists · resolve a document from “Property Setter” via get\_doc · resolve a document from mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → “DocField”, “doc\_type” → “Budget”, “field\_name” → “budget\_against”, …) via get\_doc.

**State and service calls** call save on property\_setter\_doc · call insert on Platform.get\_doc(mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → “DocField”, “doc\_type” → “Budget”, “field\_name” → “budget\_against”, …)).

**Local steps**

- Evaluate df.update(mapping(“insert\_after” → “cost\_center”, “depends\_on” → formatted text eval:doc.budget\_against == '{doc.document\_type}')).
- Evaluate create\_custom\_field(“Budget”, df, ignore\_validate = true).
- Set property\_setter from Platform.db.exists(“Property Setter”, “Budget-budget\_against-options”).
- If property\_setter.
  - Set property\_setter\_doc from Platform.get\_doc(“Property Setter”, “Budget-budget\_against-options”).
  - Set property\_setter\_doc.value from ((property\_setter\_doc.value + whitespace '\\n') + doc.document\_type).
  - Evaluate property\_setter\_doc.save().
  - Evaluate Platform.clear\_cache(doctype = “Budget”).
- Otherwise.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Property Setter”, “doctype\_or\_field” → “DocField”, “doc\_type” → “Budget”, “field\_name” → “budget\_against”, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L5325) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L172)

<a id="op-58cee4cc2dbb1a"></a>
### Delete accounting dimension

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_delete_accounting_dimension`

**Inputs** doc.

**Record and data access** resolve a document from “Property Setter” via get\_doc.

**State and service calls** execute query text (DELETE, Custom Field).format(“%s”, “, ”.join((list(“%s”) × len(doclist)))) · execute query text (DELETE, Property Setter).format(“%s”, “, ”.join((list(“%s”) × len(doclist)))) · call save on budget\_against\_property.

**Local steps**

- Set doclist from get\_doctypes\_with\_dimensions().
- Evaluate Platform.db.sql(query text (DELETE, Custom Field).format(“%s”, “, ”.join((list(“%s”) × len(doclist)))), tuple(list(doc.fieldname, expanded doclist))).
- Evaluate Platform.db.sql(query text (DELETE, Property Setter).format(“%s”, “, ”.join((list(“%s”) × len(doclist)))), tuple(list(doc.fieldname, expanded doclist))).
- Set budget\_against\_property from Platform.get\_doc(“Property Setter”, “Budget-budget\_against-options”).
- Set value\_list from budget\_against\_property.value.split(whitespace '\\n') at slice 3 to no value.
- If doc.document\_type belongs to value\_list.
  - Evaluate value\_list.remove(doc.document\_type).
- Set budget\_against\_property.value from (“\\nCost Center\\nProject\\n” + whitespace '\\n'.join(value\_list)).
- Evaluate budget\_against\_property.save().
- For each doctype in doclist.
  - Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L174)

<a id="op-a0c92cd072959b"></a>
### Disable dimension

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_disable_dimension`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with toggle\_disabling.

**Local steps**

- Evaluate Platform.has\_permission(“Accounting Dimension”, “write”, throw = true).
- If Platform.in\_test.
  - Evaluate toggle\_disabling(doc = doc).
- Otherwise.
  - Evaluate Platform.enqueue(toggle\_disabling, doc = doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Accounting Dimension”, “write”, throw = true) · service or queued work from Platform.enqueue(toggle\_disabling, doc = doc).

**Boundaries to resolve** external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L175)
