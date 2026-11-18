# Integration and transport · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Discovery

<a id="op-c9c9b0050c15ae"></a>
### Unwrap method

`operation_foundation_application_interface_discovery_business_behavior_unwrap_method`

**Inputs** method.

**Declared result** Any.

**Explicit results** getattr(method, “\_\_func\_\_”, method).

**Local steps**

- Return getattr(method, “\_\_func\_\_”, method).

**Values supplied outside this operation** selected callable from getattr(method, “\_\_func\_\_”, method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L4945) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L67) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L56)

<a id="op-32228027f775bf"></a>
### Defining class

`operation_foundation_application_interface_discovery_business_behavior_defining_class`

**Inputs** controller, method.

**Declared result** (type bitwise or no value).

**Explicit results** next(generator of class\_ for class\_ drawn from inspect.getmro(controller) where method belongs to class\_.\_\_dict\_\_, no value).

**Local steps**

- Return next(generator of class\_ for class\_ drawn from inspect.getmro(controller) where method belongs to class\_.\_\_dict\_\_, no value).
  - Draw class\_ from inspect.getmro(controller), keep a combination only if (method belongs to class\_.\_\_dict\_\_).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L5010) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L34) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L23)

<a id="op-3620df324b80d3"></a>
### Is standard doctype method

`operation_foundation_application_interface_discovery_business_behavior_is_standard_record_type_method`

**Inputs** defining\_class.

**Declared result** bool.

**Explicit results** \_class\_path(defining\_class) equals “Platform.model.document.Document”.

**Local steps**

- Return \_class\_path(defining\_class) equals “Platform.model.document.Document”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L5145) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L45) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L34)

<a id="op-1e31f3b432d95b"></a>
### Doctype method applies

`operation_foundation_application_interface_discovery_business_behavior_record_type_method_applies`

**Inputs** meta, method.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If (method belongs to set(“submit”, “cancel”, “discard”) and not meta.is\_submittable).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method belongs to set(“submit”, “cancel”, “discard”) → not meta.is\_submittable.
  - Return false.
- If (method equals “rename” and not meta.allow\_rename).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “rename” → not meta.allow\_rename.
  - Return false.
- Return true.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L5261) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L58) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L47)

<a id="op-c909c9809e5481"></a>
### Discover whitelisted method paths

`operation_foundation_application_interface_discovery_business_behavior_discover_whitelisted_method_paths`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 3 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L5434) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L36) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L25)

<a id="op-db79f0044fe9bd"></a>
### Module path from file

`operation_foundation_application_interface_discovery_business_behavior_module_path_from_file`

**Inputs** app, app\_path, file\_path.

**Declared result** str.

**Explicit results** “.”.join(tuple(app, expanded parts)).

**Local steps**

- Set relative\_path from file\_path.relative\_to(app\_path).with\_suffix(empty text).
- Set parts from relative\_path.parts at slice no value to negative 1 when relative\_path.name equals “\_\_init\_\_”, otherwise relative\_path.parts.
  - Value choice on relative\_path.name equals “\_\_init\_\_” — true gives relative\_path.parts at slice no value to negative 1, false gives relative\_path.parts.
- Return “.”.join(tuple(app, expanded parts)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L5812) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L56) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L45)

<a id="op-21563b343cae1b"></a>
### Get module level whitelisted functions

`operation_foundation_application_interface_discovery_business_behavior_get_module_level_whitelisted_functions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** file\_path.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 1 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L6024) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L40) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L29)

<a id="op-917aeed11db7f2"></a>
### Has whitelist decorator

`operation_foundation_application_interface_discovery_business_behavior_has_whitelist_decorator`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** node.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L6306) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L44) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L33)

<a id="op-79842bb8e5dcad"></a>
### Is whitelist decorator

`operation_foundation_application_interface_discovery_business_behavior_is_whitelist_decorator`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** decorator.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L6460) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L46) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L35)

<a id="op-b40716d4e60515"></a>
### Method params

`operation_foundation_application_interface_discovery_business_behavior_method_parameters`

**Inputs** fn.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** list() · params.

**Local steps**

- Attempt the following.
  - Set signature from inspect.signature(fn).
- On failure (tuple(TypeError, ValueError)).
  - Return list().
- Set params from list().
- For each tuple(name, parameter) in signature.parameters.items().
  - If name belongs to set(“self”, “cls”).
    - Continue with the next iteration or loop test.
  - Evaluate params.append(\_without\_none(mapping(“name” → name, “required” → parameter.default is identical to inspect.Parameter.empty, “default” → \_jsonable\_default(parameter.default), “type” → \_annotation\_name(parame ….
- Return params.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L6669) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L51) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L40)

<a id="op-83981b34b311b8"></a>
### Annotation name

`operation_foundation_application_interface_discovery_business_behavior_annotation_name`

**Inputs** annotation.

**Declared result** (str bitwise or no value).

**Explicit results** no value · annotation · inspect.formatannotation(annotation).

**Local steps**

- If annotation is identical to inspect.Parameter.empty.
  - Return no value.
- If isinstance(annotation, str).
  - Return annotation.
- Return inspect.formatannotation(annotation).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L7048) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L30) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L19)

<a id="op-14b1e66015c735"></a>
### Jsonable default

`operation_foundation_application_interface_discovery_business_behavior_jsonable_default`

**Inputs** default.

**Declared result** Any.

**Explicit results** no value · default · repr(default).

**Local steps**

- If default is identical to inspect.Parameter.empty.
  - Return no value.
- If (isinstance(default, (((((nested operand in the contract bitwise or nested operand in the contract) bitwise or bool) bitwise or list) bitwise or tuple) bitwise or dict)) or default is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(default, ((((((nested operand in the contract bitwise or nested operand in the contract) bitwise or float) bitwise or bool) bitwise or list) bitwise or tuple) bitwise or dict)) → default is identical to no value.
  - Return default.
- Return repr(default).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L7186) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L47) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L36)

<a id="op-d459ee7fd74218"></a>
### Without none

`operation_foundation_application_interface_discovery_business_behavior_without_none`

**Inputs** data.

**Declared result** dict at tuple(str, Any).

**Explicit results** mapping of key → value for tuple(key, value) drawn from data.items() where value is distinct from no value.

**Local steps**

- Return mapping of key → value for tuple(key, value) drawn from data.items() where value is distinct from no value.
  - Draw tuple(key, value) from data.items(), keep a combination only if (value is distinct from no value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0005.json#L7381) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L69) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L58)

## Record · Document follow

[Record definition](../../../../data/record-types/document_follow.json)

<a id="op-ae73aca9daf5e7"></a>
### Get permission query conditions

`operation_foundation_email_record_definitions_document_follow_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L5126) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1604)

<a id="op-ed88aabd4045cf"></a>
### Has permission

`operation_foundation_email_record_definitions_document_follow_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, a comparison result.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0218.json#L5282) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1605)

## Service · Documents

<a id="op-944d1695aaa373"></a>
### Get document

`operation_foundation_binding_foundation_mcp_tools_documents_get_document`

**Inputs** doctype, name.

**Declared result** dict.

**Explicit results** v2.read\_doc(doctype, name).

**Local steps**

- Return v2.read\_doc(doctype, name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1523)

<a id="op-119b69cc857c81"></a>
### Count documents

`operation_foundation_binding_foundation_mcp_tools_documents_count_documents`

**Inputs** doctype, filters = no value.

**Declared result** int.

**Explicit results** v2.count(doctype).

**Local steps**

- Within form\_dict(mapping(“filters” → filters)).
  - Return v2.count(doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1520)

<a id="op-b64547184cee12"></a>
### List documents

`operation_foundation_binding_foundation_mcp_tools_documents_list_documents`

**Inputs** doctype, filters = no value, fields = no value, order\_by = no value, start = 0, limit = 20.

**Declared result** dict.

**Explicit results** mapping(“documents” → documents, “has\_next\_page” → has\_next\_page).

**Local steps**

- Set arguments from mapping(“filters” → filters, “fields” → fields, “order\_by” → order\_by, “start” → start, …).
- Within form\_dict(mapping of key → value for tuple(key, value) drawn from arguments.items() where value is distinct from no value).
  - Draw tuple(key, value) from arguments.items(), keep a combination only if (value is distinct from no value).
  - Set documents from v2.document\_list(doctype).
  - Set has\_next\_page from bool(Platform.response.get(“has\_next\_page”)).
- Return mapping(“documents” → documents, “has\_next\_page” → has\_next\_page).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1524)

<a id="op-171e629ed55899"></a>
### Create document

`operation_foundation_binding_foundation_mcp_tools_documents_create_document`

**Inputs** doctype, data.

**Declared result** dict.

**Explicit results** v2.create\_doc(doctype).

**Local steps**

- Within form\_dict(data).
  - Return v2.create\_doc(doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L89) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1521)

<a id="op-9e11cb27557d7c"></a>
### Update document

`operation_foundation_binding_foundation_mcp_tools_documents_update_document`

**Inputs** doctype, name, data.

**Declared result** dict.

**Explicit results** v2.update\_doc(doctype, name).

**Local steps**

- Within form\_dict(data).
  - Return v2.update\_doc(doctype, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1525)

<a id="op-aa46fbca685b4c"></a>
### Delete document

`operation_foundation_binding_foundation_mcp_tools_documents_delete_document`

**Inputs** doctype, name.

**Declared result** no value.

**State and service calls** call delete\_doc on v2.

**Local steps**

- Evaluate v2.delete\_doc(doctype, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1522)

## Service · Email

<a id="op-4606470ed6b70d"></a>
### Sendmail to system managers

`operation_foundation_email_initialize_business_behavior_sendmail_to_system_managers`

**Inputs** subject, content.

**State and service calls** sendmail.

**Local steps**

- Evaluate Platform.sendmail(recipients = get\_system\_managers(), subject = subject, content = content).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = get\_system\_managers(), subject = subject, content = content).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L1842) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1073) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1506)

<a id="op-3cae25a45c3c7d"></a>
### Get contact list

`operation_foundation_email_initialize_business_behavior_get_contact_list`

**Inputs** txt, page\_length = 20, extra\_filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Contact” via get\_list.

**Explicit results** list of Platform.\_dict(value = d.email\_id, label = d.email\_id, description = d.full\_name) for d drawn from contacts.

**Local steps**

- If extra\_filters.
  - Set extra\_filters from Platform.parse\_json(extra\_filters).
- Set filters from list(list(“Contact Email”, “email\_id”, “is”, “set”)).
- If extra\_filters.
  - Evaluate filters.extend(extra\_filters).
- Set fields from list(“first\_name”, “middle\_name”, “last\_name”, “company\_name”).
- Set contacts from Platform.get\_list(“Contact”, fields = list(“full\_name”, “′tabContact Email′.email\_id”), filters = filters, or\_filters = (list of list(field, “like”, formatted text %{txt}%) for field drawn from fields + li ….
  - Draw field from fields.
- Return list of Platform.\_dict(value = d.email\_id, label = d.email\_id, description = d.full\_name) for d drawn from contacts.
  - Draw d from contacts.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L1936) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1069) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1502)

<a id="op-77c472fc60964c"></a>
### Get recipient avatars

`operation_foundation_binding_foundation_email_init_get_recipient_avatars`

**Inputs** emails.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “Contact” via get\_list.

**Explicit results** mapping(“user\_info” → mapping(), “contact\_images” → mapping()) · mapping(“user\_info” → user\_info, “contact\_images” → contact\_images).

**Local steps**

- Attempt the following.
  - Set addresses from Platform.parse\_json(emails).
- On failure (ValueError).
  - Set addresses from no value.
- If not isinstance(addresses, list).
  - Return mapping(“user\_info” → mapping(), “contact\_images” → mapping()).
- Set cleaned from generator of e.strip().lower() for e drawn from addresses where (isinstance(e, str) and e.strip()).
  - Draw e from addresses, keep a combination only if ((isinstance(e, str) and e.strip())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(e, str) → e.strip().
- Set addresses from list(dict.fromkeys(cleaned)) at slice no value to 100.
- Set user\_info from mapping().
- Evaluate Platform.utils.add\_user\_info(addresses, user\_info).
- Set contact\_images from mapping().
- Set remaining from list of a for a drawn from addresses where not user\_info.get(a, mapping()).get(“image”).
  - Draw a from addresses, keep a combination only if (not user\_info.get(a, mapping()).get(“image”)).
- If (remaining and Platform.has\_permission(“Contact”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in remaining → Platform.has\_permission(“Contact”).
  - For each row in Platform.get\_list(“Contact”, fields = list(“′tabContact Email′.email\_id”, “image”), filters = list(list(“Contact Email”, “email\_id”, “in”, remaining), list(“Contact”, “image”, “is”, “set”)), limit\_page\_length = 0).
    - If row.email\_id.
      - Evaluate contact\_images.setdefault(row.email\_id.lower(), row.image).
- Return mapping(“user\_info” → user\_info, “contact\_images” → contact\_images).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L104) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L829)
