# Integration and transport · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · V1

<a id="op-ce38ff2aa30687"></a>
### Get values for link and dynamic link fields

`operation_foundation_application_interface_v1_business_behavior_get_values_for_link_and_dynamic_link_fields`

**Inputs** doc\_dict.

**Record and data access** resolve a document from doctype via get\_doc.

**Local steps**

- Set meta from Platform.get\_meta(doc\_dict.doctype).
- Set link\_fields from (meta.get\_link\_fields() + meta.get\_dynamic\_link\_fields()).
- For each field in link\_fields.
  - If not doc\_fieldvalue bound to getattr(doc\_dict, field.fieldname, no value).
    - Continue with the next iteration or loop test.
  - Set doctype from field.options when field.fieldtype equals “Link”, otherwise doc\_dict.get(field.options).
    - Value choice on field.fieldtype equals “Link” — true gives field.options, false gives doc\_dict.get(field.options).
  - Set link\_doc from Platform.get\_doc(doctype, doc\_fieldvalue, check\_permission = “read”).
  - Evaluate link\_doc.apply\_fieldlevel\_read\_permissions().
  - Evaluate doc\_dict.update(mapping(field.fieldname → link\_doc)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc\_dict, field.fieldname, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L1433) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L77) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L66)

<a id="op-e2f7839551ca3b"></a>
### Get values for table and multiselect fields

`operation_foundation_application_interface_v1_business_behavior_get_values_for_table_and_multiselect_fields`

**Inputs** doc\_dict.

**Local steps**

- Set meta from Platform.get\_meta(doc\_dict.doctype).
- Set table\_fields from meta.get\_table\_fields().
- For each field in table\_fields.
  - Set table\_link\_fieldnames from list of f.fieldname for f drawn from Platform.get\_meta(field.options).get\_link\_fields().
    - Draw f from Platform.get\_meta(field.options).get\_link\_fields().
  - Evaluate attach\_expanded\_links(field.options, doc\_dict.get(field.fieldname), table\_link\_fieldnames).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L1771) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L78) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L67)

<a id="op-88c0bf26cbc4a3"></a>
### Execute doc method

`operation_foundation_application_interface_v1_business_behavior_execute_record_method`

**Inputs** doctype, name, method = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** doc.run\_method(method, expanded names Platform.form\_dict).

**Local steps**

- Set method from (method or Platform.form\_dict.pop(“run\_method”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in method → Platform.form\_dict.pop(“run\_method”).
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.is\_whitelisted(method).
- Set method\_obj from getattr(doc, method).
- Set fn from getattr(method\_obj, “\_\_func\_\_”, method\_obj).
- Evaluate is\_valid\_http\_method(fn).
- If Platform.request.method equals “GET”.
  - Evaluate doc.check\_permission(“read”).
  - Return doc.run\_method(method, expanded names Platform.form\_dict).
- Otherwise.
  - If Platform.request.method equals “POST”.
    - Evaluate doc.check\_permission(“write”).
    - Return doc.run\_method(method, expanded names Platform.form\_dict).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, method), getattr(method\_obj, “\_\_func\_\_”, method\_obj) and 1 further calls · effective access from doc.check\_permission(“read”), doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L17) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L75) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L64)

<a id="op-a5a45ed5a61187"></a>
### Get request form data

`operation_foundation_application_interface_v1_business_behavior_get_request_form_data`

**Inputs** no declared parameters.

**Explicit results** Platform.parse\_json(data) · Platform.form\_dict.

**Local steps**

- If Platform.form\_dict.data is identical to no value.
  - Set data from Platform.safe\_decode(Platform.request.get\_data()).
- Otherwise.
  - Set data from Platform.form\_dict.data.
- Attempt the following.
  - Return Platform.parse\_json(data).
- On failure (ValueError).
  - Return Platform.form\_dict.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L2413) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L76) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L65)

## Service · V2

<a id="op-2405a50ad9c8dc"></a>
### Handle rpc call

`operation_foundation_application_interface_v2_business_behavior_handle_rpc_call`

**Inputs** method, doctype = no value.

**Explicit results** run\_server\_script(server\_script) · Platform.call(method, expanded names Platform.form\_dict).

**Explicit failure paths** validation helper — translated “Failed to get method {0} with {1}”.format(method, str(e)).

**Local steps**

- Bind dependencies load\_doctype\_module.
- If doctype.
  - Set module from load\_doctype\_module(doctype).
  - Set method from ((module.\_\_name\_\_ + “.”) + method).
- Set method from Platform.override\_whitelisted\_method(method).
- Set server\_script from get\_server\_script\_map().get(“\_api”, mapping()).get(method).
- If server\_script.
  - Return run\_server\_script(server\_script).
- Attempt the following.
  - Set method from Platform.get\_attr(method).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Failed to get method {0} with {1}”.format(method, str(e))).
- Evaluate is\_whitelisted(method).
- Evaluate is\_valid\_http\_method(method).
- Return Platform.call(method, expanded names Platform.form\_dict).

**Values supplied outside this operation** selected callable from Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L22) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L98) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L78)

<a id="op-5051a835af6af4"></a>
### Login

`operation_foundation_application_interface_v2_business_behavior_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L3272) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L99) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L79)

<a id="op-c74f4ef960e34a"></a>
### Logout

`operation_foundation_application_interface_v2_business_behavior_logout`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** transaction control.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L3297) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L80)

<a id="op-2461fbc5a40333"></a>
### Read doc

`operation_foundation_application_interface_v2_business_behavior_read_record`

**Inputs** doctype, name.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** \_doc.

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“read”).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Set \_doc from doc.as\_dict().
- For each key in \_doc.
  - Set df from doc.meta.get\_field(key).
  - If (df and df.fieldtype equals “Link” and isinstance(\_doc.get(key), int)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype equals “Link” → isinstance(\_doc.get(key), int).
    - Set \_doc at key from cstr(\_doc.get(key)).
- Return \_doc.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L3368) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L81)

<a id="op-4792411ea858c3"></a>
### Document list

`operation_foundation_application_interface_v2_business_behavior_document_list`

**Inputs** doctype.

**Declared result** list at dict at tuple(str, Any).

**Explicit results** data at slice no value to limit.

**Explicit failure paths** validation helper — translated “Custom get\_list method for {0} must return a QueryBuilder object or None, got {1}”.format(doctype, type(return\_value).\_\_name\_\_) · validation helper — translated “Error in {0}.get\_list: {1}”.format(doctype, str(e)).

**Local steps**

- Bind dependencies get\_controller.
- Set args from Platform.form\_dict.
- Set fields from Platform.parse\_json(args.get(“fields”, no value)).
- Set filters from Platform.parse\_json(args.get(“filters”, no value)).
- Set order\_by from args.get(“order\_by”, no value).
- Set start from cint(args.get(“start”, 0)).
- Set limit from cint(args.get(“limit”, 20)).
- Set group\_by from args.get(“group\_by”, no value).
- Set debug from args.get(“debug”, false).
- Set as\_dict from args.get(“as\_dict”, true).
- Set query from Platform.qb.get\_query(table = doctype, fields = fields, filters = filters, order\_by = order\_by, …).
- Set controller from get\_controller(doctype).
- If hasattr(controller, “get\_list”).
  - Attempt the following.
    - Set return\_value from controller.get\_list(query).
    - If return\_value is distinct from no value.
      - If not hasattr(return\_value, “run”).
        - Call the validation error handler Platform.throw(translated “Custom get\_list method for {0} must return a QueryBuilder object or None, got {1}”.format(doctype, type(return\_value).\_\_name\_\_)).
      - Set query from return\_value.
  - On failure (Exception) bound to e.
    - Call the validation error handler Platform.throw(translated “Error in {0}.get\_list: {1}”.format(doctype, str(e))).
- Set data from query.run(as\_dict = as\_dict, debug = debug).
- Set Platform.response at “has\_next\_page” from len(data) &gt; limit.
- Return data at slice no value to limit.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L20) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L90) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L75)

<a id="op-e64b1a82dab6d8"></a>
### Count

`operation_foundation_application_interface_v2_business_behavior_count`

**Inputs** doctype.

**Declared result** int.

**Explicit results** get\_count().

**Local steps**

- Bind dependencies get\_count.
- Set Platform.form\_dict.doctype from doctype.
- Return get\_count().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L4944) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L87) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L72)

<a id="op-109f6e0d53a106"></a>
### Create doc

`operation_foundation_application_interface_v2_business_behavior_create_record`

**Inputs** doctype.

**State and service calls** request new\_doc for doctype · call insert on doc.

**Explicit results** doc.insert().copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Local steps**

- Set data from Platform.form\_dict.
- Evaluate data.pop(“doctype”, no value).
- Set doc from Platform.new\_doc(doctype, expanded names data).
- If (name bound to data.get(“name”) and isinstance(name, (str bitwise or int))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in name bound to data.get(“name”) → isinstance(name, (str bitwise or int)).
  - Set doc.flags.name\_set from true.
- Return doc.insert().copy\_with\_fieldlevel\_read\_permissions().as\_dict().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L19) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L88) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L73)

<a id="op-80c455c66b7c49"></a>
### Copy doc

`operation_foundation_application_interface_v2_business_behavior_copy_record`

**Inputs** doctype, name, ignore\_no\_copy = true.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** request copy\_doc for doc.

**Explicit results** copy.as\_dict(no\_private\_properties = true, no\_nulls = true).

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“read”).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Set copy from Platform.copy\_doc(doc, ignore\_no\_copy = ignore\_no\_copy).
- Return copy.as\_dict(no\_private\_properties = true, no\_nulls = true).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L5271) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L86) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L71)

<a id="op-733fd4b2df28c2"></a>
### Update doc

`operation_foundation_application_interface_v2_business_behavior_update_record`

**Inputs** doctype, name.

**Record and data access** resolve a document from doctype via get\_doc · resolve a document from doc.parenttype via get\_doc.

**State and service calls** call save on doc · call save on Platform.get\_doc(doc.parenttype, doc.parent).

**Explicit results** doc.as\_dict().

**Local steps**

- Set data from Platform.form\_dict.
- Set doc from Platform.get\_doc(doctype, name, for\_update = true).
- Evaluate doc.check\_permission(“write”).
- Evaluate data.pop(“flags”, no value).
- Evaluate doc.update(data).
- Evaluate doc.save().
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- If doc.get(“parenttype”).
  - Evaluate Platform.get\_doc(doc.parenttype, doc.parent).save().
- Return doc.as\_dict().

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L24) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L103) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L83)

<a id="op-3c761da2ec7a6a"></a>
### Delete doc

`operation_foundation_application_interface_v2_business_behavior_delete_record`

**Inputs** doctype, name.

**State and service calls** call delete\_doc on Platform.client.

**Explicit results** “ok”.

**Local steps**

- Evaluate Platform.client.delete\_doc(doctype, name).
- Set Platform.response.http\_status\_code from 202.
- Return “ok”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L5781) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L89) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L74)

<a id="op-c2d3fba33094c4"></a>
### Get meta

`operation_foundation_application_interface_v2_business_behavior_get_meta`

**Inputs** doctype.

**Explicit results** Platform.get\_meta(doctype).

**Local steps**

- Evaluate Platform.only\_for(“All”).
- Return Platform.get\_meta(doctype).

**Values supplied outside this operation** effective access from Platform.only\_for(“All”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0006.json#L5888) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L97) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L77)

<a id="op-af65ad653795de"></a>
### Execute doc method

`operation_foundation_application_interface_v2_business_behavior_execute_record_method`

**Inputs** doctype, name, method = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** result.

**Local steps**

- Set method from (method or Platform.form\_dict.pop(“run\_method”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in method → Platform.form\_dict.pop(“run\_method”).
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.is\_whitelisted(method).
- Set method\_obj from getattr(doc, method).
- Set fn from getattr(method\_obj, “\_\_func\_\_”, method\_obj).
- Evaluate is\_valid\_http\_method(fn).
- Evaluate doc.check\_permission(PERMISSION\_MAP at Platform.request.method).
- Set result from doc.run\_method(method, expanded names Platform.form\_dict).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Evaluate Platform.response.docs.append(doc.as\_dict()).
- Return result.

**Values supplied outside this operation** selected callable from getattr(doc, method), getattr(method\_obj, “\_\_func\_\_”, method\_obj) and 1 further calls · effective access from doc.check\_permission(PERMISSION\_MAP at Platform.request.method).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L21) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L95) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L76)

<a id="op-74acdd3a3afc31"></a>
### Run doc method

`operation_foundation_application_interface_v2_business_behavior_run_record_method`

**Inputs** method, document, kwargs = no value.

**Record and data access** resolve a document from document via get\_doc · read doc.doctype via exists.

**Explicit results** response.

**Local steps**

- If isinstance(document, str).
  - Set document from Platform.parse\_json(document).
- If kwargs is identical to no value.
  - Set kwargs from mapping().
- Set doc from Platform.get\_doc(document).
- Set ptype from PERMISSION\_MAP at Platform.request.method.
- If (ptype equals “write” and doc.is\_new() and not doc.meta.issingle and not Platform.db.exists(doc.doctype, doc.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ptype equals “write” → doc.is\_new() → not doc.meta.issingle → not Platform.db.exists(doc.doctype, doc.name).
  - Set ptype from “create”.
- Evaluate doc.check\_permission(ptype).
- Set doc.\_original\_modified from doc.modified.
- Evaluate doc.check\_if\_latest().
- Set method\_obj from getattr(doc, method).
- Set fn from getattr(method\_obj, “\_\_func\_\_”, method\_obj).
- Evaluate is\_whitelisted(fn).
- Evaluate is\_valid\_http\_method(fn).
- Set new\_kwargs from get\_newargs(fn, kwargs).
- Set response from doc.run\_method(method, expanded names new\_kwargs).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Evaluate Platform.response.docs.append(doc).
- Return response.

**Values supplied outside this operation** effective access from doc.check\_permission(ptype) · selected callable from getattr(doc, method), getattr(method\_obj, “\_\_func\_\_”, method\_obj) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L102) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L82)

## Record · Webhook

[Record definition](../../../../data/record-types/webhook.json)

<a id="op-a2e95bd46226d8"></a>
### Get all webhooks

`operation_foundation_integrations_record_definitions_webhook_initialize_business_behavior_get_all_webhooks`

**Inputs** no declared parameters.

**Record and data access** read “Webhook” via get\_all.

**Explicit results** webhooks.

**Local steps**

- Set webhooks\_list from Platform.get\_all(“Webhook”, fields = list(“name”, “condition”, “webhook\_docevent”, “webhook\_doctype”, …), filters = mapping(“enabled” → true)).
- Set webhooks from mapping().
- For each w in webhooks\_list.
  - Evaluate webhooks.setdefault(w.webhook\_doctype, list()).append(w).
- Return webhooks.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L3146) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L141) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L848)

<a id="op-f7ddb43d3992f4"></a>
### Run webhooks

`operation_foundation_integrations_record_definitions_webhook_initialize_business_behavior_run_webhooks`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** doc, method.

**Explicit result forms** no value.

**Observed service boundaries** record lookup.

**Local structure** 8 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L3370) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L142) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L849)

<a id="op-0ec1d044fa3948"></a>
### Add webhook to queue

`operation_foundation_integrations_record_definitions_webhook_initialize_business_behavior_add_webhook_to_queue`

**Inputs** webhook, doc.

**Local steps**

- If not getattr(Platform.local, “\_webhook\_queue”, no value).
  - Set Platform.local.\_webhook\_queue from list().
  - Evaluate Platform.db.after\_commit.add(flush\_webhook\_execution\_queue).
- Evaluate Platform.local.\_webhook\_queue.append(Platform.\_dict(doc = doc, webhook = webhook)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_webhook\_queue”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L3947) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L139) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L846)

<a id="op-a207d3ccb3e4db"></a>
### Flush webhook execution queue

`operation_foundation_integrations_record_definitions_webhook_initialize_business_behavior_flush_webhook_execution_queue`

**Inputs** no declared parameters.

**State and service calls** enqueue with “Platform.integrations.doctype.webhook.webhook.enqueue\_webhook”.

**Explicit results** no value.

**Local steps**

- If not getattr(Platform.local, “\_webhook\_queue”, no value).
  - Return no value.
- Set uniq\_hooks from set().
- Set unique\_last\_instances from list().
- Evaluate Platform.local.\_webhook\_queue.reverse().
- For each execution in Platform.local.\_webhook\_queue.
  - Set key from tuple(execution.webhook.get(“name”), execution.doc.get(“name”)).
  - If key does not belong to uniq\_hooks.
    - Evaluate uniq\_hooks.add(key).
    - Evaluate unique\_last\_instances.append(execution).
- Remove Platform.local.\_webhook\_queue.
- Evaluate unique\_last\_instances.reverse().
- For each instance in unique\_last\_instances.
  - Evaluate Platform.enqueue(“Platform.integrations.doctype.webhook.webhook.enqueue\_webhook”, doc = instance.doc, webhook = instance.webhook, now = Platform.in\_test, queue = (instance.webhook.background\_jobs\_queue or  ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in instance.webhook.background\_jobs\_queue → “default”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_webhook\_queue”, no value) · service or queued work from Platform.enqueue(“Platform.integrations.doctype.webhook.webhook.enqueue\_webhook”, doc = instance.doc, webhook = instance.webhook, now = Platform.in\_test, queue = (instance.webhook.background\_jobs\_queue or  ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0256.json#L4135) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L140) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L847)

<a id="op-5285be09905f85"></a>
### Webhook.validate

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_docevent().
- Evaluate self.validate\_condition().
- Evaluate self.validate\_request\_url().
- Evaluate self.validate\_request\_body().
- Evaluate self.validate\_repeating\_fields().
- Evaluate self.validate\_secret().
- Set self.preview\_document from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate docevent](operations-034.md#op-d5385a0212e615), [validate condition](operations-034.md#op-5f2922cb0d7137), [validate request url](operations-034.md#op-83c216cf6a345c), [validate request body](operations-034.md#op-d802490e1ea3fc), [validate repeating fields](operations-034.md#op-4cb66eeca6e688), [validate secret](operations-034.md#op-99a0129885c108).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L132) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L839)

<a id="op-c3a3771fa5c6e1"></a>
### Webhook.on update

`operation_foundation_integrations_record_definitions_webhook_business_behavior_webhook_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.client\_cache.delete\_value(“webhooks”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0258.json#L173) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L836)

<a id="op-ac35833b102df4"></a>
### Webhook.after delete

`operation_foundation_binding_foundation_integrations_doctype_webhook_webhook_webhook_after_delete`

**Inputs** self.

**Local steps**

- Evaluate Platform.client\_cache.delete\_value(“webhooks”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L46) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1478)
