# Integrations and service calls · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-39568886e4ee25"></a>
### Get expense claim summary

`operation_workforce_application_interface_initialize_business_behavior_get_expense_claim_summary`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Company” via get\_value.

**Explicit results** summary.

**Local steps**

- Set employee from get\_current\_employee().
- Bind dependencies Sum.
- Set Claim from Platform.qb.DocType(“Expense Claim”).
- Set pending\_claims\_case from nested operand in the contract.terms.Case().when(Claim.approval\_status equals “Draft”, Claim.total\_claimed\_amount).else\_(0).
- Set sum\_pending\_claims from Sum(pending\_claims\_case).as\_(“total\_pending\_amount”).
- Set approved\_claims\_case from nested operand in the contract.terms.Case().when(Claim.approval\_status equals “Approved”, Claim.total\_sanctioned\_amount).else\_(0).
- Set sum\_approved\_claims from Sum(approved\_claims\_case).as\_(“total\_approved\_amount”).
- Set approved\_total\_claimed\_case from nested operand in the contract.terms.Case().when(Claim.approval\_status equals “Approved”, Claim.total\_claimed\_amount).else\_(0).
- Set sum\_approved\_total\_claimed from Sum(approved\_total\_claimed\_case).as\_(“total\_claimed\_in\_approved”).
- Set rejected\_claims\_case from nested operand in the contract.terms.Case().when(Claim.approval\_status equals “Rejected”, Claim.total\_claimed\_amount).else\_(0).
- Set sum\_rejected\_claims from Sum(rejected\_claims\_case).as\_(“total\_rejected\_amount”).
- Set summary from nested operand in the contract.select(sum\_pending\_claims, sum\_approved\_claims, sum\_rejected\_claims, sum\_approved\_total\_claimed, …).where((nested operand in the contract.docstatus differs from 2 bitwise and … at 0.
- Set currency from Platform.db.get\_value(“Company”, summary.company, “default\_currency”).
- Set summary at “currency” from currency.
- Return summary.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L2444) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L21) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L21)

<a id="op-78fd00a01cd3bb"></a>
### Get expense type description

`operation_workforce_application_interface_initialize_business_behavior_get_expense_type_description`

**Inputs** expense\_type.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** read “Expense Claim Type” via get\_value.

**Explicit results** Platform.db.get\_value(“Expense Claim Type”, expense\_type, “description”).

**Local steps**

- Return Platform.db.get\_value(“Expense Claim Type”, expense\_type, “description”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L3299) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L24) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L24)

<a id="op-c09ec09b8f4848"></a>
### Get expense claim types

`operation_workforce_application_interface_initialize_business_behavior_get_expense_claim_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** nested operand in the contract.qb.from\_(ClaimType).select(ClaimType.name, ClaimType.description).run(as\_dict = true).

**Local steps**

- Set ClaimType from Platform.qb.DocType(“Expense Claim Type”).
- Return nested operand in the contract.qb.from\_(ClaimType).select(ClaimType.name, ClaimType.description).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L3401) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L22) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L22)

<a id="op-a1436f48ccd471"></a>
### Get expense approval details

`operation_workforce_application_interface_initialize_business_behavior_get_expense_approval_details`

**Inputs** employee.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Employee” via get\_cached\_value · read “Department Approver” via get\_value · read “User” via get\_value · read “HR Settings” via get\_single\_value.

**Explicit results** dict(expense\_approver = expense\_approver, expense\_approver\_name = expense\_approver\_name, department\_approvers = department\_approvers, is\_mandatory = Platform.db.get\_single\_value(“HR Settings”, “expense\_app ….

**Local steps**

- Evaluate Platform.has\_permission(“Employee”, “read”, employee, throw = true).
- Set tuple(expense\_approver, department) from Platform.get\_cached\_value(“Employee”, employee, list(“expense\_approver”, “department”)).
- If (not expense\_approver and department).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not expense\_approver → department.
  - Set expense\_approver from Platform.db.get\_value(“Department Approver”, mapping(“parent” → department, “parentfield” → “expense\_approvers”, “idx” → 1), “approver”).
- Set expense\_approver\_name from Platform.db.get\_value(“User”, expense\_approver, “full\_name”, cache = true).
- Set department\_approvers from get\_department\_approvers(department, “expense\_approvers”).
- If (expense\_approver and expense\_approver does not belong to list of approver.name for approver drawn from department\_approvers).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expense\_approver → expense\_approver does not belong to list of approver.name for approver drawn from department\_approvers.
  - Draw approver from department\_approvers.
  - Evaluate department\_approvers.append(mapping(“name” → expense\_approver, “full\_name” → expense\_approver\_name)).
- Return dict(expense\_approver = expense\_approver, expense\_approver\_name = expense\_approver\_name, department\_approvers = department\_approvers, is\_mandatory = Platform.db.get\_single\_value(“HR Settings”, “expense\_app ….

**Values supplied outside this operation** effective access from Platform.has\_permission(“Employee”, “read”, employee, throw = true) · configured or stored value from Platform.get\_cached\_value(“Employee”, employee, list(“expense\_approver”, “department”)), Platform.db.get\_single\_value(“HR Settings”, “expense\_approver\_mandatory\_in\_expense\_claim”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L3) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L20) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L20)

<a id="op-50b4388e585b33"></a>
### Get employee advance balance

`operation_workforce_application_interface_initialize_business_behavior_get_employee_advance_balance`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** advances.

**Local steps**

- Set employee from get\_current\_employee().
- Set Advance from Platform.qb.DocType(“Employee Advance”).
- Set advances from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where(((nested operand in the contract bitw ….
- Return advances.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L4217) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L19) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L19)

<a id="op-6fc590776a3823"></a>
### Get company currencies

`operation_workforce_application_interface_initialize_business_behavior_get_company_currencies`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Company” via get\_list.

**Explicit results** mapping of company.name → tuple(company.default\_currency, symbols.get(company.default\_currency)) for company drawn from companies where company.default\_currency belongs to symbols.

**Local steps**

- Set companies from Platform.get\_list(“Company”, fields = list(“name”, “default\_currency”)).
- Set symbols from get\_currency\_symbols().
- Return mapping of company.name → tuple(company.default\_currency, symbols.get(company.default\_currency)) for company drawn from companies where company.default\_currency belongs to symbols.
  - Draw company from companies, keep a combination only if (company.default\_currency belongs to symbols).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L2) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L13) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L13)

<a id="op-11d5a2769cea35"></a>
### Get currency symbols

`operation_workforce_application_interface_initialize_business_behavior_get_currency_symbols`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping of currency.name → (currency.symbol or currency.name) for currency drawn from currencies.

**Local steps**

- Set Currency from Platform.qb.DocType(“Currency”).
- Set currencies from nested operand in the contract.qb.from\_(Currency).select(Currency.name, Currency.symbol).run(as\_dict = true).
- Return mapping of currency.name → (currency.symbol or currency.name) for currency drawn from currencies.
  - Draw currency from currencies.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency.symbol → currency.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L5035) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L14) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L14)

<a id="op-473057bc89812a"></a>
### Get company cost center and expense account

`operation_workforce_application_interface_initialize_business_behavior_get_company_cost_center_and_expense_account`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Company” via get\_value.

**Explicit results** Platform.db.get\_value(“Company”, company, list(“cost\_center”, “default\_expense\_claim\_payable\_account”, “default\_payroll\_payable\_account”), as\_dict = true).

**Local steps**

- Evaluate Platform.has\_permission(“Company”, “read”, company, throw = true).
- Return Platform.db.get\_value(“Company”, company, list(“cost\_center”, “default\_expense\_claim\_payable\_account”, “default\_payroll\_payable\_account”), as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “read”, company, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L5256) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L12) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L12)

<a id="op-48e9ed5dc6262f"></a>
### Get doctype fields

`operation_workforce_application_interface_initialize_business_behavior_get_record_type_fields`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list of field for field drawn from fields where (field.fieldtype belongs to SUPPORTED\_FIELD\_TYPES and field.fieldname differs from “amended\_from”).

**Local steps**

- Set fields from Platform.get\_meta(doctype).fields.
- Return list of field for field drawn from fields where (field.fieldtype belongs to SUPPORTED\_FIELD\_TYPES and field.fieldname differs from “amended\_from”).
  - Draw field from fields, keep a combination only if ((field.fieldtype belongs to SUPPORTED\_FIELD\_TYPES and field.fieldname differs from “amended\_from”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field.fieldtype belongs to SUPPORTED\_FIELD\_TYPES → field.fieldname differs from “amended\_from”.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L5435) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L34) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L34)

<a id="op-3607baf762b715"></a>
### Get doctype states

`operation_workforce_application_interface_initialize_business_behavior_get_record_type_states`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping of state.title → state.color.lower() for state drawn from states.

**Local steps**

- Set states from Platform.get\_meta(doctype).states.
- Return mapping of state.title → state.color.lower() for state drawn from states.
  - Draw state from states.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L5612) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L35) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L35)

<a id="op-df4f9a01c0353d"></a>
### Get attachments

`operation_workforce_application_interface_initialize_business_behavior_get_attachments`

**Inputs** dt, dn.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “File” via get\_list.

**Explicit results** Platform.get\_list(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_private”), filters = mapping(“attached\_to\_name” → str(dn), “attached\_to\_doctype” → dt)).

**Local steps**

- Evaluate Platform.has\_permission(dt, “read”, dn, throw = true).
- Return Platform.get\_list(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_private”), filters = mapping(“attached\_to\_name” → str(dn), “attached\_to\_doctype” → dt)).

**Values supplied outside this operation** effective access from Platform.has\_permission(dt, “read”, dn, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L5750) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L8) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L8)

<a id="op-8eb05552a7b450"></a>
### Upload base64 file

`operation_workforce_application_interface_initialize_business_behavior_upload_base_64_file`

**Inputs** content, filename, dt = no value, dn = no value, fieldname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “File”, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → fieldname, …) via get\_doc.

**State and service calls** call save on transpose\_img · call insert on Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → fieldname, …)).

**Explicit results** Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → fieldname, …)).insert().

**Explicit failure paths** validation helper — translated “You can only upload JPG, PNG, PDF, TXT or Microsoft documents.”.

**Local steps**

- Bind dependencies base64.
- Bind dependencies io.
- Bind dependencies guess\_type.
- Bind dependencies Image, ImageOps.
- Bind dependencies ALLOWED\_MIMETYPES.
- Set decoded\_content from base64.b64decode(content).
- Set content\_type from guess\_type(filename) at 0.
- If content\_type does not belong to ALLOWED\_MIMETYPES.
  - Call the validation error handler Platform.throw(translated “You can only upload JPG, PNG, PDF, TXT or Microsoft documents.”).
- If content\_type.startswith(“image/jpeg”).
  - Within Image.open(io.BytesIO(decoded\_content)) bound as image.
    - Set transpose\_img from ImageOps.exif\_transpose(image).
    - Set file\_content from io.BytesIO().
    - Evaluate transpose\_img.save(file\_content, format = “JPEG”).
    - Set file\_content from file\_content.getvalue().
- Otherwise.
  - Set file\_content from decoded\_content.
- Evaluate Platform.has\_permission(dt, “write”, dn, throw = true).
- Return Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → fieldname, …)).insert().

**Values supplied outside this operation** effective access from Platform.has\_permission(dt, “write”, dn, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L5997) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L44) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L44)

<a id="op-17f0580a41d148"></a>
### Delete attachment

`operation_workforce_application_interface_initialize_business_behavior_delete_attachment`

**Inputs** filename.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “File” via get\_value.

**State and service calls** request delete\_doc for “File”.

**Local steps**

- Set tuple(attached\_to\_doctype, attached\_to\_name) from Platform.db.get\_value(“File”, filename, list(“attached\_to\_doctype”, “attached\_to\_name”)).
- If (attached\_to\_doctype and attached\_to\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in attached\_to\_doctype → attached\_to\_name.
  - Evaluate Platform.has\_permission(attached\_to\_doctype, “write”, attached\_to\_name, throw = true).
- Evaluate Platform.delete\_doc(“File”, filename).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(attached\_to\_doctype, “write”, attached\_to\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L6741) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L4) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L4)

<a id="op-58393d22710e80"></a>
### Download pdf

`operation_workforce_application_interface_initialize_business_behavior_download_portable_document`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** (formatted text data:{content\_type};base64, + base64content.decode(“utf-8”)).

**Explicit failure paths** validation helper — translated “Failed to download PDF: {0}”.format(str(e)).

**Local steps**

- Bind dependencies base64.
- Bind dependencies download\_pdf.
- Set default\_print\_format from (Platform.get\_meta(doctype).default\_print\_format or “Standard”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_meta(doctype).default\_print\_format → “Standard”.
- Attempt the following.
  - Evaluate download\_pdf(doctype, docname, format = default\_print\_format).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Failed to download PDF: {0}”.format(str(e))).
- Set base64content from base64.b64encode(Platform.local.response.filecontent).
- Set content\_type from Platform.local.response.type.
- Return (formatted text data:{content\_type};base64, + base64content.decode(“utf-8”)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L6989) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L5) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L5)

<a id="op-c87bceddee8d9a"></a>
### Get workflow

`operation_workforce_application_interface_initialize_business_behavior_get_workflow`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from “Workflow” via get\_doc.

**Explicit results** Platform.\_dict() · Platform.get\_doc(“Workflow”, workflow).

**Local steps**

- Set workflow from get\_workflow\_name(doctype).
- If not workflow.
  - Return Platform.\_dict().
- Return Platform.get\_doc(“Workflow”, workflow).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0002.json#L7358) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L41) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L41)

<a id="op-27529fff4527db"></a>
### Get workflow state field

`operation_workforce_application_interface_initialize_business_behavior_get_workflow_state_field`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Record and data access** read “Workflow” via get\_value.

**Explicit results** no value · workflow\_state\_field.

**Local steps**

- Set workflow\_name from get\_workflow\_name(doctype).
- If not workflow\_name.
  - Return no value.
- Set tuple(override\_status, workflow\_state\_field) from Platform.db.get\_value(“Workflow”, workflow\_name, list(“override\_status”, “workflow\_state\_field”)).
- If not override\_status.
  - Return workflow\_state\_field.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L6) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L42) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L42)

<a id="op-58e55f5324eaba"></a>
### Get allowed states for workflow

`operation_workforce_application_interface_initialize_business_behavior_get_allowed_states_for_workflow`

**Inputs** workflow, user\_id.

**Declared result** list at str.

**Explicit results** list of transition.state for transition drawn from workflow.transitions where transition.allowed belongs to user\_roles.

**Local steps**

- Set user\_roles from Platform.get\_roles(user\_id).
- Return list of transition.state for transition drawn from workflow.transitions where transition.allowed belongs to user\_roles.
  - Draw transition from workflow.transitions, keep a combination only if (transition.allowed belongs to user\_roles).

**Values supplied outside this operation** effective access from Platform.get\_roles(user\_id).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L201) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L7) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L7)

<a id="op-448d0dcbe3e54e"></a>
### Get permitted fields for write

`operation_workforce_application_interface_initialize_business_behavior_get_permitted_fields_for_write`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** get\_permitted\_fields(doctype, permission\_type = “write”).

**Local steps**

- Return get\_permitted\_fields(doctype, permission\_type = “write”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L346) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L33) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L33)

## Service · Oauth

<a id="op-a5fb8e8b373ef1"></a>
### Oauth providers

`operation_workforce_application_interface_delegated_authorization_business_behavior_delegated_authorization_providers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L449) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L2) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L2)

## Service · Roster

<a id="op-8fc8fb120d0b00"></a>
### Validate employee filters

`operation_workforce_application_interface_roster_business_behavior_validate_employee_filters`

**Inputs** employee\_filters.

**Declared result** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid employee filter: {0}”.format(Platform.bold(key)).

**Local steps**

- For each key in employee\_filters.
  - If key does not belong to ALLOWED\_EMPLOYEE\_FILTERS.
    - Call the validation error handler Platform.throw(translated “Invalid employee filter: {0}”.format(Platform.bold(key)), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L938) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L57) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L57)

<a id="op-904eb99d07cc34"></a>
### Validate shift filters

`operation_workforce_application_interface_roster_business_behavior_validate_shift_filters`

**Inputs** shift\_filters.

**Declared result** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid shift filter: {0}”.format(Platform.bold(key)).

**Local steps**

- For each key in shift\_filters.
  - If key does not belong to ALLOWED\_SHIFT\_FILTERS.
    - Call the validation error handler Platform.throw(translated “Invalid shift filter: {0}”.format(Platform.bold(key)), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L1108) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L58) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L58)

<a id="op-0951f2d4262fe3"></a>
### Get default company

`operation_workforce_application_interface_roster_business_behavior_get_default_company`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** Platform.defaults.get\_user\_default(“Company”).

**Local steps**

- Return Platform.defaults.get\_user\_default(“Company”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L1278) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L48) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L48)

<a id="op-544b4508f4104d"></a>
### Get permitted filter doctypes

`operation_workforce_binding_workforce_api_roster_get_permitted_filter_doctypes`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** list of doctype for doctype drawn from FILTER\_DOCTYPES where Platform.has\_permission(doctype, “select”).

**Local steps**

- Return list of doctype for doctype drawn from FILTER\_DOCTYPES where Platform.has\_permission(doctype, “select”).
  - Draw doctype from FILTER\_DOCTYPES, keep a combination only if (Platform.has\_permission(doctype, “select”)).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “select”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L9) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L60) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L60)

<a id="op-d20ff087621590"></a>
### Get events

`operation_workforce_application_interface_roster_business_behavior_get_events`

**Inputs** month\_start, month\_end, employee\_filters, shift\_filters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict at tuple(str, list at dict).

**Explicit results** events.

**Local steps**

- Evaluate \_validate\_employee\_filters(employee\_filters).
- Evaluate \_validate\_shift\_filters(shift\_filters).
- Set holidays from get\_holidays(month\_start, month\_end, employee\_filters).
- Set leaves from get\_leaves(month\_start, month\_end, employee\_filters).
- Set shifts from get\_shifts(month\_start, month\_end, employee\_filters, shift\_filters).
- Set events from mapping().
- For each event in list(holidays, leaves, shifts).
  - For each tuple(key, value) in event.items().
    - If key belongs to events.
      - Evaluate events at key.extend(value).
    - Otherwise.
      - Set events at key from value.
- Return events.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../workforce-decision-contracts/part-0003.json#L1355) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L49) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L49)
