# Accounting and settlement · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Accounting dimension

[Record definition](../../../../data/record-types/accounting_dimension.json)

<a id="op-6e62709a94a8b9"></a>
### Toggle disabling

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_toggle_disabling`

**Inputs** doc.

**Record and data access** read “Custom Field” via get\_value · resolve a document from “Custom Field” via get\_doc.

**State and service calls** call save on custom\_field.

**Local steps**

- Set doc from json.loads(doc).
- If doc.get(“disabled”).
  - Set df from mapping(“read\_only” → 1).
- Otherwise.
  - Set df from mapping(“read\_only” → 0).
- Set doclist from get\_doctypes\_with\_dimensions().
- For each doctype in doclist.
  - Set field from Platform.db.get\_value(“Custom Field”, mapping(“dt” → doctype, “fieldname” → doc.get(“fieldname”))).
  - If field.
    - Set custom\_field from Platform.get\_doc(“Custom Field”, field).
    - Evaluate custom\_field.update(df).
    - Evaluate custom\_field.save().
  - Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L193) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L183)

<a id="op-cad7444ad1e9ba"></a>
### Get doctypes with dimensions

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_get_record_types_with_dimensions`

**Inputs** no declared parameters.

**Explicit results** Platform.get\_hooks(“accounting\_dimension\_doctypes”).

**Local steps**

- Return Platform.get\_hooks(“accounting\_dimension\_doctypes”).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“accounting\_dimension\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L6869) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L181)

<a id="op-a7a4f66b989f31"></a>
### Get accounting dimensions

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_get_accounting_dimensions`

**Inputs** as\_list = true.

**Record and data access** read “Accounting Dimension” via get\_all.

**Explicit results** list of d.fieldname for d drawn from accounting\_dimensions · accounting\_dimensions.

**Local steps**

- Set accounting\_dimensions from Platform.get\_all(“Accounting Dimension”, fields = list(“label”, “fieldname”, “disabled”, “document\_type”), filters = mapping(“disabled” → 0)).
- If as\_list.
  - Return list of d.fieldname for d drawn from accounting\_dimensions.
    - Draw d from accounting\_dimensions.
- Otherwise.
  - Return accounting\_dimensions.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0011.json#L6917) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L176)

<a id="op-3904ad128b571a"></a>
### Get checks for pl and bs accounts

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_get_checks_for_profit_and_loss_and_balance_sheet_accounts`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Accounting Dimension).

**Explicit results** Platform.db.sql(query text (SELECT, Accounting Dimension), as\_dict = 1).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Accounting Dimension), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L177)

<a id="op-7bd77bc297a661"></a>
### Get dimension with children

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_get_dimension_with_children`

**Inputs** doctype, dimensions.

**Record and data access** read doctype via get\_value · read doctype via get\_all.

**Explicit results** all\_dimensions.

**Local steps**

- If isinstance(dimensions, str).
  - Set dimensions from list(dimensions).
- Set all\_dimensions from list().
- For each dimension in dimensions.
  - Set tuple(lft, rgt) from Platform.db.get\_value(doctype, dimension, list(“lft”, “rgt”)).
  - Set children from Platform.get\_all(doctype, filters = mapping(“lft” → list(“&gt;=”, lft), “rgt” → list(“&lt;=”, rgt)), order\_by = “lft”).
  - Update all\_dimensions using + list of c.name for c drawn from children.
    - Draw c from children.
- Return all\_dimensions.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L325) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L189) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L179)

<a id="op-5970db382b42f5"></a>
### Get dimensions

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_get_dimensions`

**Inputs** with\_cost\_center\_and\_project = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** tuple(dimension\_filters, default\_dimensions\_map).

**Local steps**

- Set c from Platform.qb.DocType(“Accounting Dimension Detail”).
- Set p from Platform.qb.DocType(“Accounting Dimension”).
- Set dimension\_filters from nested operand in the contract(nested operand in the contract).select(p.label, p.fieldname, p.document\_type).where(p.disabled equals 0).run(as\_dict = 1).
- Set default\_dimensions from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(p.fieldname, c.company, c.default\_dimension).run(a ….
- If isinstance(with\_cost\_center\_and\_project, str).
  - If with\_cost\_center\_and\_project.lower().strip() equals “true”.
    - Set with\_cost\_center\_and\_project from true.
  - Otherwise.
    - Set with\_cost\_center\_and\_project from false.
- If with\_cost\_center\_and\_project.
  - Evaluate dimension\_filters.extend(list(Platform.\_dict(mapping(“fieldname” → “cost\_center”, “document\_type” → “Cost Center”)), Platform.\_dict(mapping(“fieldname” → “project”, “document\_type” → “Project”)))).
- Set default\_dimensions\_map from mapping().
- For each dimension in default\_dimensions.
  - Evaluate default\_dimensions\_map.setdefault(dimension.company, mapping()).
  - Set default\_dimensions\_map at dimension.company at dimension.fieldname from dimension.default\_dimension.
- Return tuple(dimension\_filters, default\_dimensions\_map).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L190) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L180)

<a id="op-6d161a936b9c20"></a>
### Create accounting dimensions for doctype

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_create_accounting_dimensions_for_record_type`

**Inputs** doctype.

**Record and data access** read “Accounting Dimension” via get\_all · read “Custom Field” via get\_value.

**Explicit results** no value.

**Local steps**

- Set accounting\_dimensions from Platform.db.get\_all(“Accounting Dimension”, fields = list(“fieldname”, “label”, “document\_type”, “disabled”)).
- If not accounting\_dimensions.
  - Return no value.
- For each d in accounting\_dimensions.
  - Set field from Platform.db.get\_value(“Custom Field”, mapping(“dt” → doctype, “fieldname” → d.fieldname)).
  - If field.
    - Continue with the next iteration or loop test.
  - Set df from mapping(“fieldname” → d.fieldname, “label” → d.label, “fieldtype” → “Link”, “options” → d.document\_type, …).
  - Evaluate create\_custom\_field(doctype, df, ignore\_validate = true).
- Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L1433) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L173)

<a id="op-fb741869c6cc6e"></a>
### Get dimension fieldname

`operation_enterprise_accounts_record_definitions_accounting_dimension_business_behavior_get_dimension_fieldname`

**Inputs** dim\_doctype.

**Declared result** str.

**Record and data access** read “Accounting Dimension” via get\_value.

**Explicit results** Platform.scrub(dim\_doctype) · Platform.db.get\_value(“Accounting Dimension”, mapping(“document\_type” → dim\_doctype), “fieldname”).

**Local steps**

- If dim\_doctype belongs to tuple(“Cost Center”, “Project”).
  - Return Platform.scrub(dim\_doctype).
- Return Platform.db.get\_value(“Accounting Dimension”, mapping(“document\_type” → dim\_doctype), “fieldname”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L1852) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L178)

## Record · Accounting dimension filter

[Record definition](../../../../data/record-types/accounting_dimension_filter.json)

<a id="op-945b32ab65e413"></a>
### Accounting Dimension Filter.before save

`operation_enterprise_accounts_record_definitions_accounting_dimension_filter_business_behavior_accounting_dimension_filter_before_save`

**Inputs** self.

**Local steps**

- If not self.apply\_restriction\_on\_values.
  - Set self.allow\_or\_restrict from “Restrict”.
  - Evaluate self.set(“dimensions”, list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L3860) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L194) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L184)

<a id="op-f5f40c5a88428c"></a>
### Accounting Dimension Filter.validate

`operation_enterprise_accounts_record_definitions_accounting_dimension_filter_business_behavior_accounting_dimension_filter_validate`

**Inputs** self.

**Record and data access** read “Accounting Dimension” via get\_value.

**Local steps**

- Set self.fieldname from (Platform.db.get\_value(“Accounting Dimension”, mapping(“document\_type” → self.accounting\_dimension), “fieldname”) or Platform.scrub(self.accounting\_dimension)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Accounting Dimension”, mapping(“document\_type” → self.accounting\_dimension), “fieldname”) → Platform.scrub(self.accounting\_dimension).
- Evaluate self.validate\_applicable\_accounts().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate applicable accounts](operations-005.md#op-981a5ce5282531).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L3958) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L195) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L185)

<a id="op-981a5ce5282531"></a>
### Accounting Dimension Filter.validate applicable accounts

`operation_enterprise_accounts_record_definitions_accounting_dimension_filter_business_behavior_accounting_dimension_filter_validate_applicable_accounts`

**Inputs** self.

**Record and data access** execute query text (SELECT, Applicable).

**Explicit failure paths** validation helper — translated “Row {0}: {1} account already applied for Accounting Dimension {2}”.format(account.idx, Platform.bold(account.applicable\_on\_account), Platform.bold(self.accounting\_dimension)).

**Local steps**

- Set accounts from Platform.db.sql(query text (SELECT, Applicable), tuple(self.name, self.accounting\_dimension), as\_dict = 1).
- Set account\_list from list of d.account for d drawn from accounts.
  - Draw d from accounts.
- For each account in self.get(“accounts”).
  - If account.applicable\_on\_account belongs to account\_list.
    - Call the validation error handler Platform.throw(translated “Row {0}: {1} account already applied for Accounting Dimension {2}”.format(account.idx, Platform.bold(account.applicable\_on\_account), Platform.bold(self.accounting\_dimension))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L196) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L186)

<a id="op-1674c696fc0411"></a>
### Get dimension filter map

`operation_enterprise_accounts_record_definitions_accounting_dimension_filter_business_behavior_get_dimension_filter_map`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Applicable, Allowed Dimension).

**Explicit results** dimension\_filter\_map.

**Local steps**

- Set filters from Platform.db.sql(query text (SELECT, Applicable, Allowed Dimension), as\_dict = 1).
- Set dimension\_filter\_map from mapping().
- For each f in filters.
  - Evaluate build\_map(dimension\_filter\_map, f.fieldname, f.applicable\_on\_account, f.dimension\_value, …).
- Return dimension\_filter\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L198) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L188)

<a id="op-9793a528925cde"></a>
### Get dimension label

`operation_enterprise_binding_enterprise_accounts_doctype_accounting_dimension_filter_accounting_dimension_filter_get_dimension_label`

**Inputs** meta, fieldname.

**Explicit results** meta.get\_translated\_label(fieldname) · Platform.unscrub(fieldname).

**Local steps**

- If meta.has\_field(fieldname).
  - Return meta.get\_translated\_label(fieldname).
- Return Platform.unscrub(fieldname).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L759)

<a id="op-354aaf6d064fbf"></a>
### Build map

`operation_enterprise_accounts_record_definitions_accounting_dimension_filter_business_behavior_build_map`

**Inputs** map\_object, dimension, account, filter\_value, allow\_or\_restrict, is\_mandatory.

**Local steps**

- Evaluate map\_object.setdefault(tuple(dimension, account), mapping(“allowed\_dimensions” → list(), “is\_mandatory” → is\_mandatory, “allow\_or\_restrict” → allow\_or\_restrict)).
- If filter\_value.
  - Evaluate map\_object at tuple(dimension, account) at “allowed\_dimensions”.append(filter\_value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L5175) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L197) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L187)

## Record · Accounting period

[Record definition](../../../../data/record-types/accounting_period.json)

<a id="op-949ec79bdecf2a"></a>
### Accounting Period.validate

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_dates().
- Evaluate self.validate\_overlap().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate dates](operations-005.md#op-5e6f01bd94aca2), [validate overlap](operations-005.md#op-c3a29e23232c4d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L6883) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L214) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L204)

<a id="op-5e6f01bd94aca2"></a>
### Accounting Period.validate dates

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_validate_dates`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Start Date cannot be after End Date” · validation helper — translated “Accounting Period cannot be created for a future date. End Date {0} is after today.”.format(Platform.bold(Platform.format(self.end\_date, “Date”))).

**Local steps**

- If getdate(self.start\_date) &gt; getdate(self.end\_date).
  - Call the validation error handler Platform.throw(translated “Start Date cannot be after End Date”).
- If getdate(self.end\_date) &gt; getdate(nowdate()).
  - Call the validation error handler Platform.throw(translated “Accounting Period cannot be created for a future date. End Date {0} is after today.”.format(Platform.bold(Platform.format(self.end\_date, “Date”)))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0012.json#L6954) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L215) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L205)

<a id="op-70f27470ad57a9"></a>
### Accounting Period.before insert

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.bootstrap\_doctypes\_for\_closing().

If control reaches the end, it returns no value.

**Methods declared on this owner** [bootstrap doctypes for closing](operations-005.md#op-26c66ef1bcda7a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L211) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L201)

<a id="op-c37180b69d9b50"></a>
### Accounting Period.autoname

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_autoname`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set company\_abbr from Platform.get\_cached\_value(“Company”, self.company, “abbr”).
- Set self.name from “ - ”.join(list(self.period\_name, company\_abbr)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “abbr”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L210) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L200)

<a id="op-c3a29e23232c4d"></a>
### Accounting Period.validate overlap

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_validate_overlap`

**Inputs** self.

**Record and data access** execute query text (SELECT, Accounting Period).

**Explicit failure paths** validation helper with OverlapError — translated “Accounting Period overlaps with {0}”.format(existing\_accounting\_period at 0.get(“name”)).

**Local steps**

- Set existing\_accounting\_period from Platform.db.sql(query text (SELECT, Accounting Period), mapping(“start\_date” → self.start\_date, “end\_date” → self.end\_date, “name” → self.name, “company” → self.company), as\_dict = true).
- <a id="op-c3a29e23232c4d-guard-19"></a>If len(existing\_accounting\_period) &gt; 0.
  - Call the validation error handler Platform.throw(translated “Accounting Period overlaps with {0}”.format(existing\_accounting\_period at 0.get(“name”)), OverlapError).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(existing\_accounting\_period) &gt; 0, length of existing\_accounting\_period = 1 selects the branch that calls the validation-error handler with translated “Accounting Period overlaps with {0}”.format(existing\_accounting\_period at 0.get(“name”)). With length of existing\_accounting\_period = 0, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-c3a29e23232c4d-guard-19)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L216) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L206)

<a id="op-7fe011dd2faf4a"></a>
### Accounting Period.get doctypes for closing

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_get_record_types_for_closing`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** docs\_for\_closing.

**Local steps**

- Set docs\_for\_closing from list().
- Set doctypes from Platform.get\_hooks(“period\_closing\_doctypes”).
- Set closed\_doctypes from list of mapping(“document\_type” → doctype, “closed” → 1) for doctype drawn from doctypes.
  - Draw doctype from doctypes.
- For each closed\_doctype in closed\_doctypes.
  - Evaluate docs\_for\_closing.append(closed\_doctype).
- Return docs\_for\_closing.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“period\_closing\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L612) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L213) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L203)

<a id="op-26c66ef1bcda7a"></a>
### Accounting Period.bootstrap doctypes for closing

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_accounting_period_bootstrap_record_types_for_closing`

**Inputs** self.

**Local steps**

- If len(self.closed\_documents) equals 0.
  - For each doctype\_for\_closing in self.get\_doctypes\_for\_closing().
    - Evaluate self.append(“closed\_documents”, mapping(“document\_type” → doctype\_for\_closing.document\_type, “closed” → doctype\_for\_closing.closed)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doctypes for closing](operations-005.md#op-7fe011dd2faf4a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L815) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L212) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L202)

<a id="op-ecebf153110029"></a>
### Validate accounting period on doc save

`operation_enterprise_accounts_record_definitions_accounting_period_business_behavior_validate_accounting_period_on_record_save`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with ClosedAccountingPeriod — translated “You cannot create a {0} within the closed Accounting Period {1}”.format(doc.doctype, Platform.bold(accounting\_period at 0 at “name”)).

**Local steps**

- If doc.doctype equals “Bank Clearance”.
  - Return no value.
- Otherwise.
  - If doc.doctype equals “Asset”.
    - If doc.asset\_type equals “Existing Asset”.
      - Return no value.
    - Otherwise.
      - Set date from doc.available\_for\_use\_date.
  - Otherwise.
    - If doc.doctype equals “Asset Repair”.
      - Set date from doc.completion\_date.
    - Otherwise.
      - If doc.doctype equals “Period Closing Voucher”.
        - Set date from doc.period\_end\_date.
      - Otherwise.
        - Set date from doc.posting\_date.
- Set ap from Platform.qb.DocType(“Accounting Period”).
- Set cd from Platform.qb.DocType(“Closed Document”).
- Set accounting\_period from nested operand in the contract(nested operand in the contract).select(ap.name, ap.exempted\_role).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested oper ….
- If accounting\_period.
  - If (accounting\_period at 0.get(“exempted\_role”) and accounting\_period at 0.get(“exempted\_role”) belongs to Platform.get\_roles()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in accounting\_period at 0.get(“exempted\_role”) → accounting\_period at 0.get(“exempted\_role”) belongs to Platform.get\_roles().
    - Return no value.
  - Call the validation error handler Platform.throw(translated “You cannot create a {0} within the closed Accounting Period {1}”.format(doc.doctype, Platform.bold(accounting\_period at 0 at “name”)), ClosedAccountingPeriod).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0013.json#L986) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L217) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L207)

## Service · Accounts mixin

<a id="op-0db752729a09b1"></a>
### Accounts Test Mixin.create customer

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_create_customer`

**Inputs** self, customer\_name = “\_Test Customer”, currency = no value, default\_account = no value, company = no value.

**Record and data access** read “Customer” via exists · resolve a document from “Customer” via get\_doc.

**State and service calls** request new\_doc for “Customer” · call save on customer.

**Local steps**

- If not Platform.db.exists(“Customer”, customer\_name).
  - Set customer from Platform.new\_doc(“Customer”).
  - Set customer.customer\_name from customer\_name.
  - Set customer.type from “Individual”.
  - If currency.
    - Set customer.default\_currency from currency.
  - If (company and default\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → default\_account.
    - Evaluate customer.append(“accounts”, mapping(“company” → company, “account” → default\_account)).
  - Evaluate customer.save().
  - Set self.customer from customer.name.
- Otherwise.
  - If (company and default\_account).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in company → default\_account.
    - Set customer from Platform.get\_doc(“Customer”, customer\_name).
    - Set customer.accounts from list().
    - Evaluate customer.append(“accounts”, mapping(“company” → company, “account” → default\_account)).
    - Evaluate customer.save().
  - Set self.customer from customer\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0297.json#L4933) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1224) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L154)

<a id="op-15e0bdcc64c8b4"></a>
### Accounts Test Mixin.create supplier

`operation_enterprise_accounts_test_accounts_mixin_business_behavior_accounts_test_mixin_create_supplier`

**Inputs** self, supplier\_name = “\_Test Supplier”, currency = no value.

**Record and data access** read “Supplier” via exists.

**State and service calls** request new\_doc for “Supplier” · call save on supplier.

**Local steps**

- If not Platform.db.exists(“Supplier”, supplier\_name).
  - Set supplier from Platform.new\_doc(“Supplier”).
  - Set supplier.supplier\_name from supplier\_name.
  - Set supplier.supplier\_type from “Individual”.
  - Set supplier.supplier\_group from “Local”.
  - If currency.
    - Set supplier.default\_currency from currency.
  - Evaluate supplier.save().
  - Set self.supplier from supplier.name.
- Otherwise.
  - Set self.supplier from supplier\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0297.json#L5443) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1226) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L156)
