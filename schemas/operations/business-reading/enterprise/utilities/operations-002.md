# Supporting services · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bulk transaction log

[Record definition](../../../../data/record-types/bulk_transaction_log.json)

<a id="op-4e3d9bf38176bb"></a>
### Bulk Transaction Log.get list

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_get_list`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of serialize\_transaction\_log(x) for x drawn from query.run(as\_dict = true).

**Local steps**

- Evaluate Platform.has\_permission(“Bulk Transaction Log”, “read”, throw = true).
- Set log\_detail from qb.DocType(“Bulk Transaction Log Detail”).
- Set query from nested operand in the contract(nested operand in the contract).orderby(log\_detail.date, order = Order.desc).offset(cint(args.get(“start”))).limit((cint(args.get(“page\_length”)) or 20)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(args.get(“page\_length”)) → 20.
- Set query from filter\_by\_date(query, log\_detail, parse\_list\_filters(args.get(“filters”))).
- Return list of serialize\_transaction\_log(x) for x drawn from query.run(as\_dict = true).
  - Draw x from query.run(as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bulk Transaction Log”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L166) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L72) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1353)

<a id="op-101481dd6ddad6"></a>
### Bulk Transaction Log.get count

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_get_count`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Explicit results** filter\_by\_date(query, log\_detail, parse\_list\_filters(nested operand in the contract(nested operand in the contract))).run() at 0 at 0.

**Local steps**

- Evaluate Platform.has\_permission(“Bulk Transaction Log”, “read”, throw = true).
- Set log\_detail from qb.DocType(“Bulk Transaction Log Detail”).
- Set query from qb.from\_(log\_detail).select(Count(log\_detail.date).distinct()).
- Return filter\_by\_date(query, log\_detail, parse\_list\_filters(nested operand in the contract(nested operand in the contract))).run() at 0 at 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Bulk Transaction Log”, “read”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L165) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1352)

<a id="op-52381a61c307b1"></a>
### Bulk Transaction Log.get stats

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_get_stats`

**Inputs** args.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0336.json#L693) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L73) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1354)

<a id="op-18b63888f2709a"></a>
### Bulk Transaction Log.db update

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_database_update`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0336.json#L731) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1350)

<a id="op-2487b33d9b6bdb"></a>
### Bulk Transaction Log.delete

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_bulk_transaction_log_delete`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0336.json#L774) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1351)

<a id="op-bf6a3c1baa1c12"></a>
### Serialize transaction log

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_serialize_transaction_log`

**Inputs** data.

**Explicit results** Platform.\_dict(name = data.date, date = data.date, log\_entries = data.count, succeeded = data.succeeded, …).

**Local steps**

- Return Platform.\_dict(name = data.date, date = data.date, log\_entries = data.count, succeeded = data.succeeded, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0336.json#L807) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L76) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1357)

<a id="op-541aa8f4cc9a6c"></a>
### Count with status

`operation_enterprise_binding_enterprise_bulk_transaction_doctype_bulk_transaction_log_bulk_transaction_log_count_with_status`

**Inputs** log\_detail, status.

**Declared result** Sum.

**Explicit results** Sum(Case().when(log\_detail.transaction\_status equals status, 1).else\_(0)).

**Local steps**

- Return Sum(Case().when(log\_detail.transaction\_status equals status, 1).else\_(0)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L27)

<a id="op-d67b1909e3b618"></a>
### Filter by date

`operation_enterprise_binding_enterprise_bulk_transaction_doctype_bulk_transaction_log_bulk_transaction_log_filter_by_date`

**Inputs** query, log\_detail, conditions.

**Declared result** QueryBuilder.

**Explicit results** query.

**Explicit failure paths** validation helper — translated “Unsupported filter operator {0}”.format(operator).

**Local steps**

- For each tuple(operator, value) in conditions.
  - If operator does not belong to OPERATOR\_MAP.
    - Call the validation error handler Platform.throw(translated “Unsupported filter operator {0}”.format(operator)).
  - Set query from query.where(OPERATOR\_MAP at operator(log\_detail.date, value)).
- Return query.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L788) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L28)

<a id="op-d86f5ebb63255a"></a>
### Parse list filters

`operation_enterprise_bulk_transaction_record_definitions_bulk_transaction_log_business_behavior_parse_list_filters`

**Inputs** filters.

**Declared result** list at tuple.

**Explicit results** list of tuple(str(condition at negative nested operand in the contract).lower(), condition at negative 1) for condition drawn from conditions where (len(condition) ≥ 3 and condition at negative 3 equals “date”).

**Local steps**

- Set filters from (filters or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- If isinstance(filters, dict).
  - Set filters from list of list(field, expanded value) when is\_list(value), otherwise list(field, value) for tuple(field, value) drawn from filters.items().
    - Draw tuple(field, value) from filters.items().
    - Value choice on is\_list(value) — true gives list(field, expanded value), false gives list(field, value).
- Set conditions from list of with\_operator(condition) for condition drawn from filters where is\_list(condition).
  - Draw condition from filters, keep a combination only if (is\_list(condition)).
- Return list of tuple(str(condition at negative nested operand in the contract).lower(), condition at negative 1) for condition drawn from conditions where (len(condition) ≥ 3 and condition at negative 3 equals “date”).
  - Draw condition from conditions, keep a combination only if ((len(condition) ≥ 3 and condition at negative 3 equals “date”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(condition) ≥ 3 → condition at negative 3 equals “date”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L167) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L75) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1356)

<a id="op-a21145334c6607"></a>
### With operator

`operation_enterprise_binding_enterprise_bulk_transaction_doctype_bulk_transaction_log_bulk_transaction_log_with_operator`

**Inputs** condition.

**Declared result** list.

**Explicit results** list(condition at 0, “=”, condition at 1) when len(condition) equals 2, otherwise list(condition).

**Local steps**

- Return list(condition at 0, “=”, condition at 1) when len(condition) equals 2, otherwise list(condition).
  - Value choice on len(condition) equals 2 — true gives list(condition at 0, “=”, condition at 1), false gives list(condition).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L790) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L30)

<a id="op-05df7d1e9c92ab"></a>
### Is list

`operation_enterprise_binding_enterprise_bulk_transaction_doctype_bulk_transaction_log_bulk_transaction_log_is_list`

**Inputs** value.

**Declared result** bool.

**Explicit results** isinstance(value, (list bitwise or tuple)).

**Local steps**

- Return isinstance(value, (list bitwise or tuple)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L29)

## Service · Commands

<a id="op-05b90c33a17461"></a>
### Call command

`operation_enterprise_commands_initialize_business_behavior_call_command`

**Inputs** cmd, context.

**Explicit results** click.Context(cmd, obj = context).forward(cmd).

**Local steps**

- Return click.Context(cmd, obj = context).forward(cmd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0364.json#L6704) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L588) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L293)

## Service · Email template

<a id="op-182ab834101f27"></a>
### Get email subject and message

`operation_enterprise_binding_enterprise_utilities_email_template_get_email_subject_and_message`

**Inputs** template\_name, context, default\_subject, default\_message.

**Declared result** tuple at tuple(str, str).

**Record and data access** resolve a document from “Email Template” via get\_cached\_doc.

**Explicit results** tuple(default\_subject, default\_message) · tuple(subject, message).

**Local steps**

- If not template\_name.
  - Return tuple(default\_subject, default\_message).
- Set template from Platform.get\_cached\_doc(“Email Template”, template\_name).
- Set subject from Platform.render\_template(template.subject, context, restrict\_globals = true).
- Set message from Platform.render\_template(template.response\_, context, restrict\_globals = true).
- Return tuple(subject, message).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Email Template”, template\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L39) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1320)

## Service · Enterprise

<a id="op-ef591f17c4f587"></a>
### Get default company

`operation_enterprise_initialize_business_behavior_get_default_company`

**Inputs** user = no value.

**Record and data access** read “Global Defaults” via get\_single\_value.

**Explicit results** default\_company.

**Local steps**

- Bind dependencies get\_user\_default\_as\_list.
- If not user.
  - Set user from Platform.session.user.
- Set companies from get\_user\_default\_as\_list(“company”, user).
- If companies.
  - Set default\_company from companies at 0.
- Otherwise.
  - Set default\_company from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).
- Return default\_company.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Global Defaults”, “default\_company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L4894) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L181) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L83)

<a id="op-a4e91a57c58148"></a>
### Get default currency

`operation_enterprise_initialize_business_behavior_get_default_currency`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Local steps**

- Set company from get\_default\_company().
- If company.
  - Return Platform.get\_cached\_value(“Company”, company, “default\_currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L5092) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L183) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L85)

<a id="op-3aaeb9e9f7b54b"></a>
### Get default cost center

`operation_enterprise_initialize_business_behavior_get_default_cost_center`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value · Platform.flags.company\_cost\_center at company.

**Local steps**

- If not company.
  - Return no value.
- If not Platform.flags.company\_cost\_center.
  - Set Platform.flags.company\_cost\_center from mapping().
- If company does not belong to Platform.flags.company\_cost\_center.
  - Set Platform.flags.company\_cost\_center at company from Platform.get\_cached\_value(“Company”, company, “cost\_center”).
- Return Platform.flags.company\_cost\_center at company.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “cost\_center”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L5189) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L182) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L84)

<a id="op-0457923954e5bd"></a>
### Get company currency

`operation_enterprise_initialize_business_behavior_get_company_currency`

**Inputs** company.

**Record and data access** read “Company” via get\_value.

**Explicit results** Platform.flags.company\_currency at company.

**Local steps**

- If not Platform.flags.company\_currency.
  - Set Platform.flags.company\_currency from mapping().
- If company does not belong to Platform.flags.company\_currency.
  - Set Platform.flags.company\_currency at company from Platform.db.get\_value(“Company”, company, “default\_currency”, cache = true).
- Return Platform.flags.company\_currency at company.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L5397) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L180) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L82)

<a id="op-dce6d6c41e33bd"></a>
### Set perpetual inventory

`operation_enterprise_initialize_business_behavior_set_perpetual_inventory`

**Inputs** enable = 1, company = no value.

**Record and data access** resolve a document from “Company” via get\_doc.

**State and service calls** call save on company.

**Local steps**

- If not company.
  - Set company from “\_Test Company” when Platform.in\_test, otherwise get\_default\_company().
    - Value choice on Platform.in\_test — true gives “\_Test Company”, false gives get\_default\_company().
- Set company from Platform.get\_doc(“Company”, company).
- Set company.enable\_perpetual\_inventory from enable.
- Evaluate company.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L5599) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L191) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L93)

<a id="op-651d5ffa804db4"></a>
### Encode company abbr

`operation_enterprise_initialize_business_behavior_encode_company_abbreviation`

**Inputs** name, company = no value, abbr = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** “ - ”.join(parts).

**Local steps**

- Set company\_abbr from (abbr or Platform.get\_cached\_value(“Company”, company, “abbr”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in abbr → Platform.get\_cached\_value(“Company”, company, “abbr”).
- Set parts from name.rsplit(“ - ”, 1).
- If parts at negative 1.lower() differs from company\_abbr.lower().
  - Evaluate parts.append(company\_abbr).
- Return “ - ”.join(parts).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “abbr”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L5769) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L179) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L81)

<a id="op-45581623e5e314"></a>
### Is perpetual inventory enabled

`operation_enterprise_initialize_business_behavior_is_perpetual_inventory_enabled`

**Inputs** company.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.local.enable\_perpetual\_inventory at company.

**Local steps**

- If not company.
  - Set company from “\_Test Company” when Platform.in\_test, otherwise get\_default\_company().
    - Value choice on Platform.in\_test — true gives “\_Test Company”, false gives get\_default\_company().
- If not hasattr(Platform.local, “enable\_perpetual\_inventory”).
  - Set Platform.local.enable\_perpetual\_inventory from mapping().
- If company does not belong to Platform.local.enable\_perpetual\_inventory.
  - Set Platform.local.enable\_perpetual\_inventory at company from (Platform.get\_cached\_value(“Company”, company, “enable\_perpetual\_inventory”) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Company”, company, “enable\_perpetual\_inventory”) → 0.
- Return Platform.local.enable\_perpetual\_inventory at company.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “enable\_perpetual\_inventory”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L6011) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L89)

<a id="op-6b981fa47abc0d"></a>
### Get default finance book

`operation_enterprise_initialize_business_behavior_get_default_finance_book`

**Inputs** company = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.local.default\_finance\_book at company.

**Local steps**

- If not company.
  - Set company from get\_default\_company().
- If not hasattr(Platform.local, “default\_finance\_book”).
  - Set Platform.local.default\_finance\_book from mapping().
- If company does not belong to Platform.local.default\_finance\_book.
  - Set Platform.local.default\_finance\_book at company from Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).
- Return Platform.local.default\_finance\_book at company.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_finance\_book”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L6278) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L184) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L86)

<a id="op-810dbb14ba2d56"></a>
### Get party account type

`operation_enterprise_initialize_business_behavior_get_party_account_type`

**Inputs** party\_type.

**Record and data access** read “Party Type” via get\_value.

**Explicit results** Platform.local.party\_account\_types at party\_type.

**Local steps**

- If not hasattr(Platform.local, “party\_account\_types”).
  - Set Platform.local.party\_account\_types from mapping().
- If party\_type does not belong to Platform.local.party\_account\_types.
  - Set Platform.local.party\_account\_types at party\_type from (Platform.db.get\_value(“Party Type”, party\_type, “account\_type”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Party Type”, party\_type, “account\_type”) → empty text.
- Return Platform.local.party\_account\_types at party\_type.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L6523) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L185) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L87)

<a id="op-6e29122c43e105"></a>
### Get region

`operation_enterprise_initialize_business_behavior_get_region`

**Inputs** company = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, company, “country”) · (Platform.flags.country or Platform.get\_system\_settings(“country”)).

**Local steps**

- If not company.
  - Set company from Platform.local.flags.company.
- If company.
  - Return Platform.get\_cached\_value(“Company”, company, “country”).
- Return (Platform.flags.country or Platform.get\_system\_settings(“country”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.country → Platform.get\_system\_settings(“country”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “country”), Platform.get\_system\_settings(“country”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L6737) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L88)

<a id="op-e8119efaa9730e"></a>
### Allow regional

`operation_enterprise_initialize_business_behavior_allow_regional`

**Inputs** fn.

**Explicit results** caller.

**Local steps**

- Bind local operation caller for subsequent calls.
- Return caller.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0001.json#L6907) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L176) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L78)
