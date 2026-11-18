# Forms, reports and navigation · operations 39

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Listview

<a id="op-a146db95432d4e"></a>
### Get group by count

`operation_foundation_desk_listview_business_behavior_get_group_by_count`

**Inputs** doctype, current\_filters, field.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read doctype via get\_list · read field\_meta.options via get\_value.

**Explicit results** nested operand in the contract(nested operand in the contract).orderby(count, order = Order.desc).limit(50).run(as\_dict = true) · data.

**Explicit failure paths** ValueError(“Field does not belong to doctype”).

**Local steps**

- Set current\_filters from Platform.parse\_json(current\_filters).
- If field equals “assigned\_to”.
  - Set ToDo from DocType(“ToDo”).
  - Set User from DocType(“User”).
  - Set count from Count(“\*”).as\_(“count”).
  - Set filtered\_records from Platform.qb.get\_query(doctype, filters = current\_filters, fields = list(“name”), ignore\_permissions = false).
  - Return nested operand in the contract(nested operand in the contract).orderby(count, order = Order.desc).limit(50).run(as\_dict = true).
- Set meta from Platform.get\_meta(doctype).
- If (not meta.has\_field(field) and not is\_default\_field(field)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.has\_field(field) → not is\_default\_field(field).
  - Raise ValueError(“Field does not belong to doctype”).
- Set data from Platform.get\_list(doctype, filters = current\_filters, group\_by = field, fields = list(mapping(“COUNT” → “\*”, “as” → “count”), formatted text {field} as name), order\_by = “count desc”, …).
- If field equals “owner”.
  - Set owner\_idx from no value.
  - For each tuple(idx, item) in enumerate(data).
    - If item.name equals Platform.session.user.
      - Set owner\_idx from idx.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If owner\_idx.
    - Set data from list(data.pop(owner\_idx), expanded data at slice 0 to 49).
  - Otherwise.
    - Set data from data at slice 0 to 50.
- Otherwise.
  - Set data from data at slice 0 to 50.
- If (field\_meta bound to meta.get\_field(field) and field\_meta.fieldtype equals “Link”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in field\_meta bound to meta.get\_field(field) → field\_meta.fieldtype equals “Link”.
  - Set link\_meta from Platform.get\_meta(field\_meta.options).
  - If link\_meta.show\_title\_field\_in\_link.
    - Set title\_field from link\_meta.get\_title\_field().
    - For each item in data.
      - Set item.title from Platform.get\_value(field\_meta.options, item.name, title\_field).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L77) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L298)

## Service · Llm

<a id="op-d1fb326db99540"></a>
### Is retryable

`operation_foundation_binding_foundation_studio_ai_llm_is_retryable`

**Inputs** exc.

**Declared result** bool.

**Explicit results** any(generator of cls.\_\_name\_\_ belongs to TRANSIENT\_ERROR\_NAMES for cls drawn from type(exc).\_\_mro\_\_).

**Local steps**

- Return any(generator of cls.\_\_name\_\_ belongs to TRANSIENT\_ERROR\_NAMES for cls drawn from type(exc).\_\_mro\_\_).
  - Draw cls from type(exc).\_\_mro\_\_.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1835)

<a id="op-d7de4e5f623828"></a>
### Loads tolerant

`operation_foundation_binding_foundation_studio_ai_llm_loads_tolerant`

**Inputs** raw.

**Declared result** tuple at tuple((object bitwise or no value), bool).

**Explicit results** tuple(no value, false) · tuple(json.loads(raw), false) · tuple(obj, true).

**Local steps**

- Set raw from (raw or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in raw → empty text.
- If not raw.
  - Return tuple(no value, false).
- Attempt the following.
  - Return tuple(json.loads(raw), false).
- On failure (json.JSONDecodeError).
  - Take no action here.
- Attempt the following.
  - Bind dependencies repair\_json.
  - Set obj from repair\_json(raw, return\_objects = true).
  - If obj does not belong to tuple(empty text, no value, list(), mapping()).
    - Return tuple(obj, true).
- On failure (Exception).
  - Take no action here.
- Return tuple(no value, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1836)

<a id="op-132c2351f4ba73"></a>
### Patch messages for provider

`operation_foundation_binding_foundation_studio_ai_llm_patch_messages_for_provider`

**Inputs** model, messages.

**Declared result** no value.

**Local steps**

- If “claude-” belongs to model.
  - For each m in messages.
    - If (isinstance(m.get(“content”), str) and “cache\_control” belongs to m).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(m.get(“content”), str) → “cache\_control” belongs to m.
      - Set m at “content” from list(mapping(“type” → “text”, “text” → m at “content”, “cache\_control” → m.pop(“cache\_control”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1838)

<a id="op-6315d5a3ccb99a"></a>
### Log content

`operation_foundation_binding_foundation_studio_ai_llm_log_content`

**Inputs** content.

**Declared result** str.

**Explicit results** str(content) · one space.join(parts).

**Local steps**

- If not isinstance(content, list).
  - Return str(content).
- Set parts from list().
- For each part in content.
  - If not isinstance(part, dict).
    - Evaluate parts.append(str(part)).
  - Otherwise.
    - If part.get(“type”) equals “image\_url”.
      - Evaluate parts.append(“&#91;image&#93;”).
    - Otherwise.
      - Evaluate parts.append(str(part.get(“text”, part))).
- Return one space.join(parts).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1837)

<a id="op-8a3e3cba01ceaf"></a>
### Complete

`operation_foundation_binding_foundation_studio_ai_llm_complete`

**Inputs** model, messages, params, stream (named only), api\_key (named only, default no value).

**Explicit results** content · resp.

**Local steps**

- Evaluate patch\_messages\_for\_provider(model, messages).
- Evaluate logger.info((formatted text LLM \| model={model} stream={stream} fallbacks={ModelRegistry.get\_fallbacks(model)} params={params}  + whitespace '\\n'.join(generator of formatted text &#91;{m at “role”}&#93; {\_log\_cont ….
  - Draw m from messages.
- Set resp from litellm.completion(model = model, messages = messages, stream = stream, api\_key = (api\_key or get\_api\_key()), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in api\_key → get\_api\_key().
  - Value choice on stream — true gives list(), false gives ModelRegistry.get\_fallbacks(model).
  - Value choice on stream — true gives mapping(“stream\_options” → mapping(“include\_usage” → true)), false gives mapping().
- If not stream.
  - Set content from (resp.choices at 0.message.content or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in resp.choices at 0.message.content → empty text.
  - Evaluate logger.info(formatted text LLM response \| length={len(content)} {content}).
  - Return content.
- Return resp.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L169) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1832)

<a id="op-82bf733f23b109"></a>
### Complete with tools

`operation_foundation_binding_foundation_studio_ai_llm_complete_with_tools`

**Inputs** model, messages, tools, params, api\_key (named only, default no value), stream (named only, default false).

**Explicit results** litellm.completion(model = model, messages = messages, tools = tools, stream = stream, …).

**Local steps**

- Evaluate patch\_messages\_for\_provider(model, messages).
- Evaluate logger.info((formatted text LLM tools \| model={model} stream={stream} tools={list of t at “function” at “name” for t drawn from tools}  + whitespace '\\n'.join(generator of formatted text &#91;{m at “role”}&#93; {\_ ….
  - Draw t from tools.
  - Draw m from messages.
- Return litellm.completion(model = model, messages = messages, tools = tools, stream = stream, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in api\_key → get\_api\_key().
  - Value choice on stream — true gives list(), false gives ModelRegistry.get\_fallbacks(model).
  - Value choice on stream — true gives mapping(“stream\_options” → mapping(“include\_usage” → true)), false gives mapping().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L170) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1857) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1833)

<a id="op-7f0804903e983d"></a>
### Get api key

`operation_foundation_binding_foundation_studio_ai_llm_get_api_key`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1858) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1834)

## Service · Load

<a id="op-fcbaa88b5125cb"></a>
### Getdoc

`operation_foundation_desk_form_load_business_behavior_getdoc`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from doctype via get\_doc.

**Explicit results** list().

**Explicit failure paths** Exception(“doctype and name required!”).

**Local steps**

- If not (doctype and name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.
  - Raise Exception(“doctype and name required!”).
- Attempt the following.
  - Set doc from Platform.get\_doc(doctype, name).
- On failure (Platform.DoesNotExistError).
  - Evaluate check\_doctype\_permission(doctype).
  - Evaluate Platform.clear\_last\_message().
  - Return list().
- Evaluate doc.check\_permission(“read”).
- If (key bound to Platform.can\_cache\_doc(tuple(doctype, name)) and Platform.cache.exists(key)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key bound to Platform.can\_cache\_doc(tuple(doctype, name)) → Platform.cache.exists(key).
  - Evaluate Platform.\_set\_document\_in\_cache(key, doc).
- Evaluate run\_onload(doc).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Evaluate doc.add\_viewed().
- Evaluate get\_docinfo(doc).
- Evaluate doc.add\_seen().
- Evaluate set\_link\_titles(doc).
- If Platform.response.docs is identical to no value.
  - Set Platform.local.response from \_dict(mapping(“docs” → list())).
- Evaluate Platform.response.docs.append(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L5783) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L246)

<a id="op-6bb76446235e05"></a>
### Getdoctype

`operation_foundation_desk_form_load_business_behavior_getdoctype`

**Inputs** doctype, with\_parent = false.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set docs from list().
- Set parent\_dt from no value.
- If (with\_parent and parent\_dt bound to Platform.model.meta.get\_parent\_dt(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in with\_parent → parent\_dt bound to Platform.model.meta.get\_parent\_dt(doctype).
  - Set docs from get\_meta\_bundle(parent\_dt).
  - Set Platform.response at “parent\_dt” from parent\_dt.
- If not docs.
  - Set docs from get\_meta\_bundle(doctype).
- Set Platform.response at “user\_settings” from get\_user\_settings((parent\_dt or doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_dt → doctype.
- Evaluate Platform.response.docs.extend(docs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L6358) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L247)

<a id="op-afd11a2b32bec9"></a>
### Get meta bundle

`operation_foundation_desk_form_load_business_behavior_get_meta_bundle`

**Inputs** doctype.

**Explicit results** bundle.

**Local steps**

- Set form\_meta from Platform.desk.form.meta.get\_meta(doctype).
- Set bundle from list(form\_meta.as\_dict(no\_nulls = true)).
- Evaluate bundle.extend(generator of nested operand in the contract.meta.get\_meta(df.options).as\_dict(no\_nulls = true, parenttype = doctype) for df drawn from form\_meta.fields where df.fieldtype belongs to Platform. ….
  - Draw df from form\_meta.fields, keep a combination only if (df.fieldtype belongs to Platform.model.table\_fields).
- Return bundle.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L6683) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L238)

<a id="op-0084d010feef31"></a>
### Get docinfo

`operation_foundation_desk_form_load_business_behavior_get_docinfo`

**Inputs** doc = no value, doctype = no value, name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Bind dependencies get\_docshares.
- If not doc.
  - Set doc from Platform.get\_lazy\_doc(doctype, name, check\_permission = true).
- Set all\_communications from \_get\_communications(doc.doctype, doc.name, limit = 21).
- Set automated\_messages from list of msg for msg drawn from all\_communications where msg at “communication\_type” equals “Automated Message”.
  - Draw msg from all\_communications, keep a combination only if (msg at “communication\_type” equals “Automated Message”).
- Set communications\_except\_auto\_messages from list of msg for msg drawn from all\_communications where msg at “communication\_type” differs from “Automated Message”.
  - Draw msg from all\_communications, keep a combination only if (msg at “communication\_type” differs from “Automated Message”).
- Set docinfo from Platform.\_dict(user\_info = mapping()).
- Evaluate add\_comments(doc, docinfo).
- Evaluate docinfo.update(mapping(“doctype” → doc.doctype, “name” → doc.name, “attachments” → get\_attachments(doc.doctype, doc.name), “communications” → communications\_except\_auto\_messages, …)).
- Evaluate update\_user\_info(docinfo, doc).
- Set Platform.response at “docinfo” from docinfo.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L63) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1750) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L235)

<a id="op-06299169d9eaf4"></a>
### Add comments

`operation_foundation_desk_form_load_business_behavior_add_comments`

**Inputs** doc, docinfo.

**Explicit results** comments.

**Local steps**

- Set docinfo.comments from list().
- Set docinfo.shared from list().
- Set docinfo.assignment\_logs from list().
- Set docinfo.attachment\_logs from list().
- Set docinfo.info\_logs from list().
- Set docinfo.like\_logs from list().
- Set docinfo.workflow\_logs from list().
- Set comments from get\_document\_comments(doc.doctype, doc.name, fields = list(“name”, “creation”, “content”, “owner”, …)).
- For each c in comments.
  - Select the first matching pattern against c.comment\_type.
    - Pattern “Comment”.
      - Set c.content from Platform.utils.markdown(c.content).
      - Evaluate docinfo.comments.append(c).
    - Pattern “Shared” or “Unshared”.
      - Evaluate docinfo.shared.append(c).
    - Pattern “Assignment Completed” or “Assigned”.
      - Evaluate docinfo.assignment\_logs.append(c).
    - Pattern “Attachment” or “Attachment Removed”.
      - Evaluate docinfo.attachment\_logs.append(c).
    - Pattern “Info” or “Edit” or “Label”.
      - Evaluate docinfo.info\_logs.append(c).
    - Pattern “Like”.
      - Evaluate docinfo.like\_logs.append(c).
    - Pattern “Workflow”.
      - Evaluate docinfo.workflow\_logs.append(c).
- Return comments.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L1051) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L227)

<a id="op-2656b637ebcbba"></a>
### Get milestones

`operation_foundation_desk_form_load_business_behavior_get_milestones`

**Inputs** doctype, name, start = 0, limit = 20.

**Record and data access** read “Milestone” via get\_all.

**Explicit results** Platform.get\_all(“Milestone”, fields = list(“name”, “creation”, “owner”, “track\_field”, …), filters = dict(reference\_type = doctype, reference\_name = str(name)), limit\_start = start, limit = limit, …).

**Local steps**

- Return Platform.get\_all(“Milestone”, fields = list(“name”, “creation”, “owner”, “track\_field”, …), filters = dict(reference\_type = doctype, reference\_name = str(name)), limit\_start = start, limit = limit, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L1751) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L239)

<a id="op-3198a63ed17f10"></a>
### Get attachments

`operation_foundation_desk_form_load_business_behavior_get_attachments`

**Inputs** dt, dn.

**Record and data access** read “File” via get\_all.

**Explicit results** Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “file\_type”, …), filters = mapping(“attached\_to\_name” → str(dn), “attached\_to\_doctype” → dt)).

**Local steps**

- Return Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “file\_type”, …), filters = mapping(“attached\_to\_name” → str(dn), “attached\_to\_doctype” → dt)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L62) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L230)

<a id="op-fb53eec9aef230"></a>
### Get filtered attachments

`operation_foundation_desk_form_load_business_behavior_get_filtered_attachments`

**Inputs** dt, dn, filters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from dt via get\_doc · read “File” via get\_all.

**Explicit results** Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “file\_type”, …), filters = list(list(“File”, “attached\_to\_name”, “=”, str(dn)), list(“File”, “attached\_to\_doctype”, “=”, dt), expande ….

**Explicit failure paths** validation helper — translated “Filters must be four-value rows with string doctypes, fields, and operators.” · validation helper — translated “Attachment Gallery filters must target File.”.

**Local steps**

- Evaluate Platform.get\_doc(dt, dn).check\_permission(“read”).
- Set filters from Platform.parse\_json(filters).
- If (not isinstance(filters, list) or any(generator of (not isinstance(filter\_row, list) or len(filter\_row) differs from 4 or not all(generator of nested operand in the contract for nested operand in the contr ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(filters, list) → any(generator of (not isinstance(filter\_row, list) or len(filter\_row) differs from 4 or not all(generator of nested operand in the contract(nested operand in the contract, nested operand in the contract) for v …).
  - Draw filter\_row from filters.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(filter\_row, list) → len(filter\_row) differs from 4 → not all(generator of isinstance(value, str) for value drawn from filter\_row at slice no value to 3).
  - Draw value from filter\_row at slice no value to 3.
  - Call the validation error handler Platform.throw(translated “Filters must be four-value rows with string doctypes, fields, and operators.”).
- If any(generator of filter\_row at 0 differs from “File” for filter\_row drawn from filters).
  - Draw filter\_row from filters.
  - Call the validation error handler Platform.throw(translated “Attachment Gallery filters must target File.”).
- Return Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “file\_type”, …), filters = list(list(“File”, “attached\_to\_name”, “=”, str(dn)), list(“File”, “attached\_to\_doctype”, “=”, dt), expande ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L3000) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1752) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L237)

<a id="op-65c8c54169c933"></a>
### Get versions

`operation_foundation_desk_form_load_business_behavior_get_versions`

**Inputs** doc.

**Declared result** list at dict.

**Record and data access** read “Version” via get\_all.

**Explicit results** list() · Platform.get\_all(“Version”, filters = dict(ref\_doctype = doc.doctype, docname = str(doc.name)), fields = list(“name”, “owner”, “creation”, “data”), limit = 10, order\_by = “creation desc”).

**Local steps**

- If not doc.meta.track\_changes.
  - Return list().
- Return Platform.get\_all(“Version”, filters = dict(ref\_doctype = doc.doctype, docname = str(doc.name)), fields = list(“name”, “owner”, “creation”, “data”), limit = 10, order\_by = “creation desc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L65) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L244)

<a id="op-e0de6bfd246dee"></a>
### Get communications

`operation_foundation_desk_form_load_business_behavior_get_communications`

**Inputs** doctype, name, start = 0, limit = 20.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_communications(doctype, name, cint(start), cint(limit)).

**Local steps**

- Bind dependencies cint.
- Evaluate Platform.get\_lazy\_doc(doctype, name).check\_permission().
- Return \_get\_communications(doctype, name, cint(start), cint(limit)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L3975) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L233)

<a id="op-161a2fbfff5f24"></a>
### Get comments

`operation_foundation_desk_form_load_business_behavior_get_comments`

**Inputs** doctype, name, comment\_type = “Comment”.

**Declared result** list at Platform.\_dict.

**Explicit results** comments.

**Local steps**

- If isinstance(comment\_type, list).
  - Set comment\_types from comment\_type.
- Otherwise.
  - If comment\_type equals “share”.
    - Set comment\_types from list(“Shared”, “Unshared”).
  - Otherwise.
    - If comment\_type equals “assignment”.
      - Set comment\_types from list(“Assignment Completed”, “Assigned”).
    - Otherwise.
      - If comment\_type equals “attachment”.
        - Set comment\_types from list(“Attachment”, “Attachment Removed”).
      - Otherwise.
        - Set comment\_types from list(comment\_type).
- Set comments from get\_document\_comments(doctype, name, fields = list(“name”, “creation”, “content”, “owner”, …), comment\_types = comment\_types).
- For each c in comments.
  - If c.comment\_type equals “Comment”.
    - Set c.content from Platform.utils.markdown(c.content).
- Return comments.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L4206) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L231)

<a id="op-8eb295114e4510"></a>
### Get communications

`operation_foundation_desk_form_load_business_behavior_get_communications_2`

**Inputs** doctype, name, start = 0, limit = 20.

**Record and data access** read “File” via get\_all.

**Explicit results** communications.

**Local steps**

- Set communications from get\_communication\_data(doctype, name, start, limit).
- For each c in communications.
  - If c.communication\_type belongs to tuple(“Communication”, “Automated Message”).
    - Set c.attachments from json.dumps(Platform.get\_all(“File”, fields = list(“file\_url”, “is\_private”), filters = mapping(“attached\_to\_doctype” → “Communication”, “attached\_to\_name” → c.name))).
- Return communications.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L4703) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L234)

<a id="op-ea9c4b272f05de"></a>
### Get communication data

`operation_foundation_desk_form_load_business_behavior_get_communication_data`

**Inputs** doctype, name, start = 0, limit = 20, after = no value, fields = no value, group\_by = no value, as\_dict = true.

**Explicit results** Platform.db.multisql(mapping(“sqlite” → sqlite\_query, “\*” → query), dict(doctype = doctype, name = str(name), start = Platform.utils.cint(start), limit = limit, …), as\_dict = as\_dict).

**Local steps**

- If not fields.
  - Set fields from multiline text in the contract.
- Set conditions from empty text.
- If after.
  - Update conditions using + formatted text   AND C.communication\_date &gt; {after}.
- If doctype equals “User”.
  - Update conditions using + “\\n\\t\\t\\tAND NOT (C.reference\_doctype='User' AND C.communication\_type='Communication')\\n\\t\\t”.
- Set part1 from formatted text   SELECT {fields}  FROM ′tabCommunication′ as C  WHERE C.communication\_type IN ('Communication', 'Automated Message')  AND (C.reference\_doctype =.
- Set part2 from formatted text   SELECT {fields}  FROM ′tabCommunication′ as C  INNER JOIN ′tabCommunication Link′ ON C.name=′tabCommunication Link′.parent  WHERE C.communicatio.
- Set sqlite\_query from formatted text   SELECT \* FROM (  SELECT \* FROM ({part1})  UNION ALL  SELECT \* FROM ({part2})  ) AS combined  {(group\_by or empty text)}  ORDER BY communic.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_by → empty text.
- Set query from formatted text   WITH part1 AS ({part1}), part2 AS ({part2})  SELECT \*  FROM (  SELECT \* FROM part1  UNION  SELECT \* FROM part2  ) AS combined  {(group\_by.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_by → empty text.
- Return Platform.db.multisql(mapping(“sqlite” → sqlite\_query, “\*” → query), dict(doctype = doctype, name = str(name), start = Platform.utils.cint(start), limit = limit, …), as\_dict = as\_dict).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L5001) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L232)

<a id="op-35ab60c45074df"></a>
### Get assignments

`operation_foundation_desk_form_load_business_behavior_get_assignments`

**Inputs** dt, dn.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** Platform.get\_all(“ToDo”, fields = list(“name”, “allocated\_to as owner”, “description”, “status”), filters = mapping(“reference\_type” → dt, “reference\_name” → str(dn), “status” → tuple(“not in”, tuple(“Canc ….

**Local steps**

- Return Platform.get\_all(“ToDo”, fields = list(“name”, “allocated\_to as owner”, “description”, “status”), filters = mapping(“reference\_type” → dt, “reference\_name” → str(dn), “status” → tuple(“not in”, tuple(“Canc ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L5752) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L229)

<a id="op-009316f1e8a6b2"></a>
### Run onload

`operation_foundation_desk_form_load_business_behavior_run_onload`

**Inputs** doc.

**Local steps**

- Evaluate doc.set(“\_\_onload”, Platform.\_dict()).
- Evaluate doc.run\_method(“onload”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“onload”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L5973) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L248)

<a id="op-a0520c96499749"></a>
### Get view logs

`operation_foundation_desk_form_load_business_behavior_get_view_logs`

**Inputs** doc.

**Declared result** list at dict.

**Record and data access** read “View Log” via get\_all.

**Explicit results** list() · Platform.get\_all(“View Log”, filters = mapping(“reference\_doctype” → doc.doctype, “reference\_name” → str(doc.name)), fields = list(“name”, “creation”, “owner”), order\_by = “creation desc”).

**Local steps**

- If not doc.meta.track\_views.
  - Return list().
- Return Platform.get\_all(“View Log”, filters = mapping(“reference\_doctype” → doc.doctype, “reference\_name” → str(doc.name)), fields = list(“name”, “creation”, “owner”), order\_by = “creation desc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0202.json#L6065) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L245)
