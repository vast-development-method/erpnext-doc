# Record lifecycle and persistence · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Client

<a id="op-b675861194d961"></a>
### Get count

`operation_foundation_client_business_behavior_get_count`

**Inputs** doctype, filters = no value, debug = false, cache = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_count().

**Local steps**

- Bind dependencies get\_count.
- Set Platform.form\_dict.doctype from doctype.
- Set Platform.form\_dict.filters from get\_safe\_filters(filters).
- Set Platform.form\_dict.debug from debug.
- Return get\_count().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L2330) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L555)

<a id="op-cbbd0efd0791c4"></a>
### Get

`operation_foundation_client_business_behavior_get`

**Inputs** doctype, name = no value, filters = no value, parent = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** doc.as\_dict().

**Local steps**

- If name.
  - Set doc from Platform.get\_doc(doctype, name).
- Otherwise.
  - If (filters or filters equals mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → filters equals mapping().
    - Set doc from Platform.get\_doc(doctype, Platform.parse\_json(filters)).
  - Otherwise.
    - Set doc from Platform.get\_doc(doctype).
- Evaluate doc.check\_permission().
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Return doc.as\_dict().

**Values supplied outside this operation** effective access from doc.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L112) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L554)

<a id="op-61c7fdce6bc2cf"></a>
### Get value

`operation_foundation_client_business_behavior_get_value`

**Inputs** doctype, fieldname, filters = no value, as\_dict = true, debug = false, parent = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** value at 0 when value, otherwise mapping() · no value · value at 0 when len(fields) &gt; 1, otherwise value at 0 at 0.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “No permission for {0}”.format(translated doctype).

**Local steps**

- If not Platform.has\_permission(doctype, parent\_doctype = parent).
  - Call the validation error handler Platform.throw(translated “No permission for {0}”.format(translated doctype), Platform.PermissionError).
- Set filters from get\_safe\_filters(filters).
- If isinstance(filters, str).
  - Set filters from mapping(“name” → filters).
- Attempt the following.
  - Set fields from Platform.parse\_json(fieldname).
- On failure (tuple(TypeError, ValueError)).
  - Set fields from list(fieldname).
- If not filters.
  - Set filters from no value.
- If Platform.get\_meta(doctype).issingle.
  - Set value from Platform.db.get\_values\_from\_single(fields, filters, doctype, as\_dict = as\_dict, debug = debug).
- Otherwise.
  - Set value from get\_list(doctype, filters = filters, fields = fields, debug = debug, limit\_page\_length = 1, …).
- If as\_dict.
  - Return value at 0 when value, otherwise mapping().
    - Value choice on value — true gives value at 0, false gives mapping().
- If not value.
  - Return no value.
- Return value at 0 when len(fields) &gt; 1, otherwise value at 0 at 0.
  - Value choice on len(fields) &gt; 1 — true gives value at 0, false gives value at 0 at 0.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, parent\_doctype = parent).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L2977) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L561)

<a id="op-803a2f48095e2f"></a>
### Get single value

`operation_foundation_client_business_behavior_get_single_value`

**Inputs** doctype, field.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(doctype, field).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “No permission for {0}”.format(translated doctype).

**Local steps**

- If not Platform.has\_permission(doctype).
  - Call the validation error handler Platform.throw(translated “No permission for {0}”.format(translated doctype), Platform.PermissionError).
- Return Platform.db.get\_single\_value(doctype, field).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype) · configured or stored value from Platform.db.get\_single\_value(doctype, field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L3816) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L559)

<a id="op-cbcf2504c48f16"></a>
### Set value

`operation_foundation_client_business_behavior_set_value`

**Inputs** doctype, name, fieldname, value = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doctype via get\_doc · read doctype via get\_value · resolve a document from doc.parenttype via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Explicit failure paths** validation helper — translated “Cannot edit standard fields”.

**Local steps**

- If fieldname belongs to (Platform.model.default\_fields + Platform.model.child\_table\_fields).
  - Call the validation error handler Platform.throw(translated “Cannot edit standard fields”).
- If not value.
  - Set values from fieldname.
  - If isinstance(fieldname, str).
    - Attempt the following.
      - Set values from json.loads(fieldname).
    - On failure (ValueError).
      - Set values from mapping(fieldname → empty text).
- Otherwise.
  - Set values from mapping(fieldname → value).
- If not Platform.get\_meta(doctype).istable.
  - Set doc from Platform.get\_doc(doctype, name).
  - Evaluate doc.update(values).
- Otherwise.
  - Set doc from Platform.db.get\_value(doctype, name, list(“parenttype”, “parent”), as\_dict = true).
  - Set doc from Platform.get\_doc(doc.parenttype, doc.parent).
  - Set child from doc.getone(mapping(“doctype” → doctype, “name” → name)).
  - Evaluate child.update(values).
- Evaluate doc.save().
- Return doc.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L118) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L569)

<a id="op-41fa9b9350fb7a"></a>
### Insert

`operation_foundation_client_business_behavior_insert`

**Inputs** doc = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Explicit results** insert\_doc(doc).copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Return insert\_doc(doc).copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L115) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L563)

<a id="op-d961f6272d2010"></a>
### Insert many

`operation_foundation_client_business_behavior_insert_many`

**Inputs** docs = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Explicit results** list of insert\_doc(doc).name for doc drawn from docs.

**Explicit failure paths** validation helper — translated “Only 200 inserts allowed in one request”.

**Local steps**

- If isinstance(docs, str).
  - Set docs from json.loads(docs).
- If len(docs) &gt; 200.
  - Call the validation error handler Platform.throw(translated “Only 200 inserts allowed in one request”).
- Return list of insert\_doc(doc).name for doc drawn from docs.
  - Draw doc from docs.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L116) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L564)

<a id="op-8429393ddf7f12"></a>
### Save

`operation_foundation_client_business_behavior_save`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doc via get\_doc.

**State and service calls** call save on doc.

**Explicit results** doc.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Set doc from Platform.get\_doc(doc).
- Evaluate doc.save().
- Return doc.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L117) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L568)

<a id="op-851e2930f07b93"></a>
### Rename doc

`operation_foundation_client_business_behavior_rename_record`

**Inputs** doctype, old\_name, new\_name, merge = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**State and service calls** request rename\_doc for doctype.

**Explicit results** new\_name.

**Local steps**

- Set new\_name from Platform.rename\_doc(doctype, old\_name, new\_name, merge = merge).
- Return new\_name.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L5486) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L567)

<a id="op-a6ee95f359964f"></a>
### Submit

`operation_foundation_client_business_behavior_submit`

**Inputs** doc.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doc via get\_doc.

**State and service calls** call submit on doc.

**Explicit results** doc.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Local steps**

- If isinstance(doc, str).
  - Set doc from json.loads(doc).
- Set doc from Platform.get\_doc(doc).
- Evaluate doc.submit().
- Return doc.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L119) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L570)

<a id="op-7c13241649203b"></a>
### Cancel

`operation_foundation_client_business_behavior_cancel`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call cancel on wrapper.

**Explicit results** wrapper.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Local steps**

- Set wrapper from Platform.get\_doc(doctype, name).
- Evaluate wrapper.cancel().
- Return wrapper.copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L110) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L551)

<a id="op-afa6948fdded3c"></a>
### Delete

`operation_foundation_client_business_behavior_delete`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“DELETE”, “POST”)).

**Local steps**

- Evaluate delete\_doc(doctype, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L6023) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L552)

<a id="op-8ba025b758ea06"></a>
### Bulk update

`operation_foundation_client_business_behavior_bulk_update`

**Inputs** docs.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doc at “doctype” via get\_doc.

**State and service calls** call save on existing\_doc.

**Explicit results** mapping(“failed\_docs” → failed\_docs).

**Local steps**

- Set docs from json.loads(docs).
- Set failed\_docs from list().
- For each doc in docs.
  - Evaluate doc.pop(“flags”, no value).
  - Attempt the following.
    - Set existing\_doc from Platform.get\_doc(doc at “doctype”, doc at “docname”).
    - Evaluate existing\_doc.update(doc).
    - Evaluate existing\_doc.save().
  - On failure (Exception).
    - Evaluate failed\_docs.append(mapping(“doc” → doc, “exc” → Platform.utils.get\_traceback())).
- Return mapping(“failed\_docs” → failed\_docs).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L109) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L550)

<a id="op-f9ce001a70f2db"></a>
### Has permission

`operation_foundation_client_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, docname, perm\_type.

**Explicit result forms** a structured result.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L6504) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L562)

<a id="op-c43af96a65dffb"></a>
### Get doc permissions

`operation_foundation_client_business_behavior_get_record_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, docname.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L114) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L558)

<a id="op-b5b70b996de3f8"></a>
### Get password

`operation_foundation_client_business_behavior_get_password`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** doctype, name, fieldname.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L113) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L557)

<a id="op-60719ff590ae26"></a>
### Get time zone

`operation_foundation_client_business_behavior_get_time_zone`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit results** mapping(“time\_zone” → Platform.defaults.get\_defaults().get(“time\_zone”)).

**Local steps**

- Return mapping(“time\_zone” → Platform.defaults.get\_defaults().get(“time\_zone”)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L6971) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L560)

<a id="op-a5d08d5321b1ec"></a>
### Attach file

`operation_foundation_client_business_behavior_attach_file`

**Inputs** filename = no value, filedata = no value, doctype = no value, docname = no value, folder = no value, decode\_base64 = false, is\_private = no value, docfield = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, …) via get\_doc.

**State and service calls** call save on Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, …)) · call save on doc.

**Explicit results** file.

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, docname, check\_permission = true).
- Set file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, …)).save().
- If (docfield and doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield → doctype.
  - Evaluate doc.set(docfield, file.file\_url).
  - Evaluate doc.save().
- Return file.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L108) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L549)

<a id="op-8b8ff691f5e2db"></a>
### Is document amended

`operation_foundation_client_business_behavior_is_document_amended`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = (10 × 60)).

**Record and data access** read doctype via exists.

**Explicit results** Platform.db.exists(doctype, mapping(“amended\_from” → docname)) · false.

**Local steps**

- If Platform.permissions.has\_permission(doctype).
  - Attempt the following.
    - Return Platform.db.exists(doctype, mapping(“amended\_from” → docname)).
  - On failure (Platform.db.InternalError).
    - Take no action here.
- Return false.

**Values supplied outside this operation** effective access from Platform.permissions.has\_permission(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L7656) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L566)

<a id="op-9eb75545daf6ad"></a>
### Validate link and fetch

`operation_foundation_client_business_behavior_validate_link_and_fetch`

**Inputs** doctype, docname, fields\_to\_fetch = no value, query = no value, filters = no value, remaining named values search\_args.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”, “POST”)).

**Record and data access** resolve a document from doctype via get\_doc · read doctype via get\_value.

**State and service calls** msgprint with translated “You need {0} permission to fetch values from {1} {2}”.format(Platform.bold(translated “Read”), Platform.bold(doctype), Platform.bold(docname)).

**Explicit results** mapping() · values.

**Explicit failure paths** validation helper — translated “Document Name must not be empty”.

**Local steps**

- If not docname.
  - Call the validation error handler Platform.throw(translated “Document Name must not be empty”).
- Set meta from Platform.get\_meta(doctype).
- Set fields\_to\_fetch from Platform.parse\_json(fields\_to\_fetch).
- Set can\_cache from (not fields\_to\_fetch and Platform.request.method equals “GET”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not fields\_to\_fetch → Platform.request.method equals “GET”.
- Evaluate search\_args.update(as\_dict = false, page\_length = PAGE\_LENGTH\_FOR\_LINK\_VALIDATION, txt = translated docname when (query and meta.translated\_doctype), otherwise docname, for\_link\_validation = true).
  - Value choice on (query and meta.translated\_doctype) — true gives translated docname, false gives docname.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query → meta.translated\_doctype.
- Set search\_result from Platform.call(search\_widget, doctype = doctype, query = query, filters = filters, expanded names search\_args).
- If not search\_result.
  - Return mapping().
- Set values from no value.
- Set is\_virtual\_dt from bool(meta.get(“is\_virtual”)).
- If is\_virtual\_dt.
  - Attempt the following.
    - Set doc from Platform.get\_doc(doctype, docname).
    - Evaluate doc.check\_permission(“select”).
    - Set values from mapping(“name” → doc.name).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
- Otherwise.
  - Set columns\_to\_fetch from list(“name”).
  - If Platform.is\_table(doctype).
    - Evaluate columns\_to\_fetch.append(“parenttype”).
  - Set values from Platform.db.get\_value(doctype, docname, columns\_to\_fetch, as\_dict = true).
- If not values.
  - Return mapping().
- Set name\_to\_compare from values at “name”.
- Set parent\_doctype from values.pop(“parenttype”, no value).
- If (len(search\_result) &lt; PAGE\_LENGTH\_FOR\_LINK\_VALIDATION and not any(generator of item at 0 equals name\_to\_compare for item drawn from search\_result)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(search\_result) &lt; PAGE\_LENGTH\_FOR\_LINK\_VALIDATION → not any(generator of item at 0 equals name\_to\_compare for item drawn from search\_result).
  - Draw item from search\_result.
  - Return mapping().
- If is\_virtual\_dt.
  - Return values.
- If not fields\_to\_fetch.
  - If can\_cache.
    - Evaluate Platform.local.response\_headers.set(“Cache-Control”, “private,max-age=1800,stale-while-revalidate=7200”).
  - Return values.
- Attempt the following.
  - Evaluate values.update(get\_value(doctype, fields\_to\_fetch, docname, parent = parent\_doctype)).
- On failure (Platform.PermissionError).
  - Evaluate Platform.clear\_last\_message().
  - Evaluate Platform.msgprint(translated “You need {0} permission to fetch values from {1} {2}”.format(Platform.bold(translated “Read”), Platform.bold(doctype), Platform.bold(docname)), title = translated “Cannot Fetc ….
- Return values.

**Values supplied outside this operation** effective access from doc.check\_permission(“select”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L571)

<a id="op-12ea6099f217da"></a>
### Insert doc

`operation_foundation_client_business_behavior_insert_record`

**Inputs** doc.

**Declared result** “Document”.

**Record and data access** resolve a document from doc.parenttype via get\_doc · resolve a document from doc via get\_doc.

**State and service calls** call save on parent · call insert on Platform.get\_doc(doc).

**Explicit results** parent · Platform.get\_doc(doc).insert().

**Explicit failure paths** validation helper — translated “Parenttype, Parent and Parentfield are required to insert a child record”.

**Local steps**

- Set doc from Platform.\_dict(doc).
- If Platform.is\_table(doc.doctype).
  - If not (doc.parenttype and doc.parent and doc.parentfield).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.parenttype → doc.parent → doc.parentfield.
    - Call the validation error handler Platform.throw(translated “Parenttype, Parent and Parentfield are required to insert a child record”).
  - Set parent from Platform.get\_doc(doc.parenttype, doc.parent).
  - Evaluate parent.append(doc.parentfield, doc).
  - Evaluate parent.save().
  - Return parent.
- Return Platform.get\_doc(doc).insert().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0020.json#L1410) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L565)

<a id="op-c5e85bc596ae4d"></a>
### Delete doc

`operation_foundation_client_business_behavior_delete_record`

**Inputs** doctype, name.

**Record and data access** read doctype via get\_value · resolve a document from parenttype via get\_doc.

**State and service calls** call save on parent · request delete\_doc for doctype.

**Explicit failure paths** Platform.DoesNotExistError(doctype = doctype).

**Local steps**

- If Platform.is\_table(doctype).
  - Set values from Platform.db.get\_value(doctype, name, list(“parenttype”, “parent”, “parentfield”)).
  - If not values.
    - Raise Platform.DoesNotExistError(doctype = doctype).
  - Set tuple(parenttype, parent, parentfield) from values.
  - Set parent from Platform.get\_doc(parenttype, parent).
  - If not parent.has\_permission(“write”).
    - Raise Platform.DoesNotExistError(doctype = doctype).
  - For each row in parent.get(parentfield).
    - If row.name equals name.
      - Evaluate parent.remove(row).
      - Evaluate parent.save().
      - Leave the innermost loop without its normal-exhaustion alternative.
- Otherwise.
  - Evaluate Platform.delete\_doc(doctype, name, ignore\_missing = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from parent.has\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L111) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L553)

## Record · Comment

[Record definition](../../../../data/record-types/comment.json)

<a id="op-44b797b1f9a7be"></a>
### Comment.after insert

`operation_foundation_core_record_definitions_comment_business_behavior_comment_after_insert`

**Inputs** self.

**Local steps**

- Evaluate notify\_mentions(self.reference\_doctype, self.reference\_name, self.content, source\_doctype = self.doctype, source\_name = self.name).
- Evaluate self.notify\_change(“add”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [notify change](operations-004.md#op-e699ccfaaa847c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L3815) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L968)

<a id="op-ed1074ee1211b7"></a>
### Comment.validate

`operation_foundation_core_record_definitions_comment_business_behavior_comment_validate`

**Inputs** self.

**Local steps**

- If not self.comment\_email.
  - Set self.comment\_email from Platform.session.user.
- Set self.content from Platform.utils.sanitize\_html(self.content, always\_sanitize = true, disallowed\_tags = list(“form”, “input”, “button”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0040.json#L3943) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L973)
