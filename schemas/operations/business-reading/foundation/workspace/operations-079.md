# Forms, reports and navigation · operations 79

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-4af8c48dadf895"></a>
### Add comment

`operation_foundation_desk_form_utils_business_behavior_add_comment`

**Inputs** reference\_doctype, reference\_name, content, comment\_email, comment\_by.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Declared result** “Comment”.

**Record and data access** read “User” via get\_cached\_value.

**State and service calls** request new\_doc for “Comment” · call insert on comment.

**Explicit results** comment.

**Local steps**

- Set reference\_doc from Platform.get\_lazy\_doc(reference\_doctype, reference\_name, check\_permission = true).
- Set comment from Platform.new\_doc(“Comment”).
- Evaluate comment.update(mapping(“comment\_type” → “Comment”, “reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “comment\_email” → Platform.session.user, …)).
- Evaluate comment.insert(ignore\_permissions = true).
- If Platform.get\_cached\_value(“User”, Platform.session.user, “follow\_commented\_documents”).
  - Evaluate \_follow\_document(comment.reference\_doctype, comment.reference\_name, Platform.session.user).
- Return comment.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“User”, Platform.session.user, “follow\_commented\_documents”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L72) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L283)

<a id="op-85da6bf0a5abe3"></a>
### Update comment

`operation_foundation_desk_form_utils_business_behavior_update_comment`

**Inputs** name, content.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Comment” via get\_doc.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Comment can only be edited by the owner”.

**Local steps**

- Set doc from Platform.get\_doc(“Comment”, name).
- If Platform.session.user does not belong to list(“Administrator”, doc.owner).
  - Call the validation error handler Platform.throw(translated “Comment can only be edited by the owner”, Platform.PermissionError).
- If (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Set reference\_doc from Platform.get\_lazy\_doc(doc.reference\_doctype, doc.reference\_name, check\_permission = true).
  - Set doc.content from extract\_images\_from\_html(reference\_doc, content, is\_private = true).
- Otherwise.
  - Set doc.content from content.
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L5227) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L288)

<a id="op-597f78b6a77e8d"></a>
### Update comment publicity

`operation_foundation_desk_form_utils_business_behavior_update_comment_publicity`

**Inputs** name, publish.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Comment” via get\_doc.

**State and service calls** call save on doc.

**Explicit failure paths** validation helper — translated “Comment publicity can only be updated by the original author or a System Manager.”.

**Local steps**

- Set doc from Platform.get\_doc(“Comment”, name).
- If (Platform.session.user differs from doc.owner and “System Manager” does not belong to Platform.get\_roles()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.session.user differs from doc.owner → “System Manager” does not belong to Platform.get\_roles().
  - Call the validation error handler Platform.throw(translated “Comment publicity can only be updated by the original author or a System Manager.”).
- Set doc.published from int(publish).
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L5599) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L289)

<a id="op-87de301f9e335c"></a>
### Get next

`operation_foundation_desk_form_utils_business_behavior_get_next`

**Inputs** doctype, value, prev, filters = no value, sort\_order = “desc”, sort\_field = “creation”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_value.

**State and service calls** msgprint with translated “No further records”.

**Explicit results** res at 0 at 0 · no value.

**Local steps**

- Set prev from int(prev).
- If not filters.
  - Set filters from list().
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- Set table from Platform.qb.DocType(doctype).
- Set name\_column from table.name.
- Set current\_sort\_value from Platform.db.get\_value(doctype, value, sort\_field).
- Set fallback from \_sort\_field\_fallback(doctype, sort\_field).
- If fallback is distinct from no value.
  - Set sort\_column from IfNull(table at sort\_field, fallback).
  - If current\_sort\_value is identical to no value.
    - Set current\_sort\_value from fallback.
- Otherwise.
  - Set sort\_column from table at sort\_field.
- Set is\_ascending from sort\_order.lower() equals “asc”.
- If prev equals is\_ascending.
  - Set composite\_condition from (sort\_column &lt; current\_sort\_value bitwise or (sort\_column equals current\_sort\_value bitwise and name\_column &lt; value)).
  - Set order from Platform.qb.desc.
- Otherwise.
  - Set composite\_condition from (sort\_column &gt; current\_sort\_value bitwise or (sort\_column equals current\_sort\_value bitwise and name\_column &gt; value)).
  - Set order from Platform.qb.asc.
- Set query from nested operand in the contract(nested operand in the contract, order = nested operand in the contract).orderby(name\_column, order = order).where(composite\_condition).limit(1).
- If res bound to query.run(as\_list = true).
  - Return res at 0 at 0.
- Evaluate Platform.msgprint(translated “No further records”).
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L73) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L284)

<a id="op-a5f51df3c0fa26"></a>
### Sort field fallback

`operation_foundation_desk_form_utils_business_behavior_sort_field_fallback`

**Inputs** doctype, fieldname.

**Explicit results** no value · empty text · “0001-01-01” · “00:00:00”.

**Local steps**

- If fieldname belongs to tuple(“name”, “modified”, “creation”, “modified\_by”, …).
  - Return no value.
- Set df from Platform.get\_meta(doctype).get\_field(fieldname).
- If df is identical to no value.
  - Return empty text.
- If df.fieldtype belongs to tuple(“Check”, “Float”, “Int”, “Currency”, …).
  - Return no value.
- If getattr(df, “not\_nullable”, false).
  - Return no value.
- If df.fieldtype belongs to tuple(“Date”, “Datetime”).
  - Return “0001-01-01”.
- If df.fieldtype equals “Time”.
  - Return “00:00:00”.
- Return empty text.

**Values supplied outside this operation** selected callable from getattr(df, “not\_nullable”, false).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L6860) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L287)

<a id="op-00e88940c82a18"></a>
### Get pdf link

`operation_foundation_desk_form_utils_business_behavior_get_portable_document_link`

**Inputs** doctype, docname, print\_format = “Standard”, no\_letterhead = 0.

**Explicit results** formatted text /api/method/Platform.utils.print\_format.download\_pdf?{query}.

**Local steps**

- Set query from urlencode(mapping(“doctype” → doctype, “name” → docname, “format” → print\_format, “no\_letterhead” → no\_letterhead)).
- Return formatted text /api/method/Platform.utils.print\_format.download\_pdf?{query}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L74) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L285)

<a id="op-1d045320d8848c"></a>
### Validate route conflict

`operation_foundation_desk_utils_business_behavior_validate_route_conflict`

**Inputs** doctype, name.

**Record and data access** read \_doctype via get\_all.

**State and service calls** msgprint with Platform.\_(“Name already taken, please set a new name”).

**Explicit results** no value.

**Explicit failure paths** Platform.NameError.

**Local steps**

- If Platform.flags.in\_migrate.
  - Return no value.
- Set all\_names from list().
- For each \_doctype in list(“Page”, “Workspace”, “DocType”).
  - Evaluate all\_names.extend(list of slug(d) for d drawn from Platform.get\_all(\_doctype, pluck = “name”) where not (doctype equals \_doctype and d equals name)).
    - Draw d from Platform.get\_all(\_doctype, pluck = “name”), keep a combination only if (not (doctype equals \_doctype and d equals name)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals \_doctype → d equals name.
- If slug(name) belongs to all\_names.
  - Evaluate Platform.msgprint(Platform.\_(“Name already taken, please set a new name”)).
  - Raise Platform.NameError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L6264) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1011) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1444)

<a id="op-7bac6ff8cc3be7"></a>
### Slug

`operation_foundation_desk_utils_business_behavior_slug`

**Inputs** name.

**Explicit results** name.lower().replace(one space, “-”).

**Local steps**

- Return name.lower().replace(one space, “-”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L6608) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1010) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1443)

<a id="op-685aa6e9af0445"></a>
### Is item allowed

`operation_foundation_desk_utils_business_behavior_is_item_allowed`

**Inputs** name, item\_type, ctx.

**Record and data access** read “Report” via get\_value.

**Explicit results** name belongs to (ctx.allowed\_workspaces or list()) · true · (name belongs to (ctx.can\_read or list()) and name belongs to (ctx.restricted\_doctypes or list()) and Platform.has\_permission(name)) · false · (name belongs to (ctx.allowed\_pages or mapping()) and name belongs to (ctx.restricted\_pages or list())) · 2 additional forms in the steps below.

**Local steps**

- Set item\_type from item\_type.lower().
- If item\_type equals “workspace”.
  - Return name belongs to (ctx.allowed\_workspaces or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.allowed\_workspaces → list().
- If Platform.session.user equals “Administrator”.
  - Return true.
- If item\_type equals “doctype”.
  - Attempt the following.
    - Return (name belongs to (ctx.can\_read or list()) and name belongs to (ctx.restricted\_doctypes or list()) and Platform.has\_permission(name)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in name belongs to (ctx.can\_read or list()) → name belongs to (ctx.restricted\_doctypes or list()) → Platform.has\_permission(name).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.can\_read → list().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.restricted\_doctypes → list().
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
    - Return false.
- If item\_type equals “page”.
  - Return (name belongs to (ctx.allowed\_pages or mapping()) and name belongs to (ctx.restricted\_pages or list())).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in name belongs to (ctx.allowed\_pages or mapping()) → name belongs to (ctx.restricted\_pages or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.allowed\_pages → mapping().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.restricted\_pages → list().
- If item\_type equals “report”.
  - Return (not Platform.db.get\_value(“Report”, name, “disabled”, cache = true) and name belongs to ctx.allowed\_reports).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.db.get\_value(“Report”, name, “disabled”, cache = true) → name belongs to ctx.allowed\_reports.
- If item\_type equals “dashboard”.
  - Return name belongs to (ctx.allowed\_dashboards or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ctx.allowed\_dashboards → list().
- If item\_type belongs to tuple(“help”, “url”).
  - Return true.
- Return false.

**Values supplied outside this operation** effective access from Platform.has\_permission(name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L70) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1439)

<a id="op-3e13195827bda3"></a>
### Pop csv params

`operation_foundation_desk_utils_business_behavior_post_office_protocol_comma_separated_values_parameters`

**Inputs** form\_dict.

**Explicit results** mapping(“delimiter” → cstr(form\_dict.pop(“csv\_delimiter”, “,”)) at 0, “quoting” → cint(form\_dict.pop(“csv\_quoting”, QUOTE\_NONNUMERIC)), “decimal\_sep” → cstr(form\_dict.pop(“csv\_decimal\_sep”, “.”))).

**Local steps**

- Bind dependencies QUOTE\_NONNUMERIC.
- Bind dependencies cint, cstr.
- Return mapping(“delimiter” → cstr(form\_dict.pop(“csv\_delimiter”, “,”)) at 0, “quoting” → cint(form\_dict.pop(“csv\_quoting”, QUOTE\_NONNUMERIC)), “decimal\_sep” → cstr(form\_dict.pop(“csv\_decimal\_sep”, “.”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0216.json#L7336) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1440)

<a id="op-f523aa135a23ab"></a>
### Get csv bytes

`operation_foundation_desk_utils_business_behavior_get_comma_separated_values_bytes`

**Inputs** data, csv\_params.

**Declared result** bytes.

**Explicit results** file.getvalue().encode(“utf-8”).

**Local steps**

- Bind dependencies writer.
- Bind dependencies StringIO.
- Bind dependencies escape\_formula\_injection.
- Set decimal\_sep from csv\_params.pop(“decimal\_sep”, no value).
- Set \_data from list of list of escape\_formula\_injection(v) for v drawn from row for row drawn from data.
  - Draw row from data.
  - Draw v from row.
- If decimal\_sep.
  - Set \_data from apply\_csv\_decimal\_sep(\_data, decimal\_sep).
- Set file from StringIO().
- Set csv\_writer from writer(file, expanded names csv\_params).
- Evaluate csv\_writer.writerows(\_data).
- Return file.getvalue().encode(“utf-8”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1438)

<a id="op-19b450f783ca9b"></a>
### Apply csv decimal sep

`operation_foundation_desk_utils_business_behavior_apply_comma_separated_values_decimal_separation`

**Inputs** data, decimal\_sep.

**Declared result** list at list.

**Explicit results** data · list of list of str(value).replace(“.”, decimal\_sep, 1) when isinstance(value, float), otherwise value for value drawn from row for row drawn from data.

**Local steps**

- If decimal\_sep equals “.”.
  - Return data.
- Return list of list of str(value).replace(“.”, decimal\_sep, 1) when isinstance(value, float), otherwise value for value drawn from row for row drawn from data.
  - Draw row from data.
  - Draw value from row.
  - Value choice on isinstance(value, float) — true gives str(value).replace(“.”, decimal\_sep, 1), false gives value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L342) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1435)

<a id="op-49ab1919f8792c"></a>
### Provide binary file

`operation_foundation_desk_utils_business_behavior_provide_binary_file`

**Inputs** filename, extension, content.

**Declared result** no value.

**Local steps**

- Bind dependencies \_.
- Set Platform.response at “type” from “binary”.
- Set Platform.response at “filecontent” from content.
- Set Platform.response at “filename” from formatted text {translated filename}.{extension}.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L547) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1008) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1441)

<a id="op-12c02248cdf221"></a>
### Send report email

`operation_foundation_desk_utils_business_behavior_send_report_email`

**Inputs** user\_email, report\_name, file\_extension, content, attached\_to\_name.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → formatted text {report\_name}.{file\_extension}, “attached\_to\_doctype” → “Report”, “attached\_to\_name” → attached\_to\_name, …) via get\_doc.

**State and service calls** call save on \_file · sendmail.

**Local steps**

- Evaluate create\_exported\_report\_folder\_if\_not\_exists().
- Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → formatted text {report\_name}.{file\_extension}, “attached\_to\_doctype” → “Report”, “attached\_to\_name” → attached\_to\_name, …)).
- Evaluate \_file.save(ignore\_permissions = true).
- Set file\_url from Platform.utils.get\_url(\_file.get\_url()).
- Set file\_retention\_hours from (Platform.get\_system\_settings(“delete\_background\_exported\_reports\_after”) or 48).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“delete\_background\_exported\_reports\_after”) → 48.
- Evaluate Platform.sendmail(recipients = list(user\_email), subject = Platform.\_(“Your exported report: {0}”).format(report\_name), message = Platform.\_(“The report you requested has been generated.&lt;br&gt;&lt;br&gt;Click here  ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“delete\_background\_exported\_reports\_after”) · service or queued work from Platform.sendmail(recipients = list(user\_email), subject = Platform.\_(“Your exported report: {0}”).format(report\_name), message = Platform.\_(“The report you requested has been generated.&lt;br&gt;&lt;br&gt;Click here  ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L738) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1009) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1442)

<a id="op-211fe2df7b02e9"></a>
### Delete old exported report files

`operation_foundation_desk_utils_business_behavior_delete_old_exported_report_files`

**Inputs** no declared parameters.

**Record and data access** read “File” via get\_all.

**State and service calls** request delete\_doc for “File”.

**Local steps**

- Set file\_retention\_hours from (Platform.get\_system\_settings(“delete\_background\_exported\_reports\_after”) or 48).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“delete\_background\_exported\_reports\_after”) → 48.
- Set cutoff from Platform.utils.add\_to\_date(Platform.utils.now\_datetime(), hours = negative file\_retention\_hours).
- Set old\_files from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → “Report”, “creation” → tuple(“&lt;”, cutoff), “folder” → EXPORTED\_REPORT\_FOLDER\_PATH), pluck = “name”).
- For each file\_name in old\_files.
  - Attempt the following.
    - Evaluate Platform.delete\_doc(“File”, file\_name).
  - On failure (Exception).
    - Evaluate Platform.log\_error(formatted text Failed to delete old report file {file\_name}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“delete\_background\_exported\_reports\_after”) · clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L1266) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1437)

<a id="op-ff4b979ac4d65e"></a>
### Create exported report folder if not exists

`operation_foundation_desk_utils_business_behavior_create_exported_report_folder_if_not_exists`

**Inputs** no declared parameters.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → folder\_name, “is\_folder” → 1, “folder” → parent\_folder, …) via get\_doc.

**State and service calls** call insert on folder.

**Local steps**

- Set tuple(parent\_folder, folder\_name) from EXPORTED\_REPORT\_FOLDER\_PATH.split(“/”).
- Set folder from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → folder\_name, “is\_folder” → 1, “folder” → parent\_folder, …)).
- Evaluate folder.insert(ignore\_permissions = true, ignore\_if\_duplicate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0217.json#L1629) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1436)

<a id="op-5d070f62ff81f1"></a>
### Camel case to kebab case

`operation_foundation_binding_foundation_studio_utils_camel_case_to_kebab_case`

**Inputs** text, remove\_spaces = false.

**Explicit results** empty text · text.

**Local steps**

- If not text.
  - Return empty text.
- Set text from re.sub(“(?&lt;!^)(?=&#91;A-Z&#93;)”, “-”, text).lower().
- If remove\_spaces.
  - Set text from text.replace(one space, empty text).
- Return text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L17) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L87) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L175)

<a id="op-730a341907e4d7"></a>
### Walk blocks

`operation_foundation_binding_foundation_studio_utils_walk_blocks`

**Inputs** blocks.

**Local steps**

- If isinstance(blocks, str).
  - Set blocks from Platform.parse\_json((blocks or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in blocks → “&#91;&#93;”.
- If isinstance(blocks, dict).
  - Set blocks from list(blocks).
- Set stack from list((blocks or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in blocks → list().
- While stack.
  - Set block from stack.pop().
  - If not isinstance(block, dict).
    - Continue with the next iteration or loop test.
  - yield block.
  - Evaluate stack.extend((block.get(“children”) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“children”) → list().
  - For each slot in (block.get(“componentSlots”) or mapping()).values().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in block.get(“componentSlots”) → mapping().
    - Set content from slot.get(“slotContent”) when isinstance(slot, dict), otherwise no value.
      - Value choice on isinstance(slot, dict) — true gives slot.get(“slotContent”), false gives no value.
    - If isinstance(content, list).
      - Evaluate stack.extend(content).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L34) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L104) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L192)

<a id="op-f67d6e5bca59c9"></a>
### Has page write perm

`operation_foundation_binding_foundation_studio_utils_has_page_write_perm`

**Inputs** message = no value.

**Explicit results** decorator.

**Local steps**

- Bind local operation decorator for subsequent calls.
- Return decorator.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L26) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L96) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L184)

<a id="op-b9685c3409a8a4"></a>
### Has page write perm.decorator

`operation_foundation_binding_foundation_studio_utils_has_page_write_perm_decorator`

**Inputs** fn.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L27) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L97) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L185)

<a id="op-11d6570b91ffc5"></a>
### Has page write perm.decorator.wrapper

`operation_foundation_binding_foundation_studio_utils_has_page_write_perm_decorator_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(fn).

**Explicit results** fn(expanded args, expanded names kwargs).

**Explicit failure paths** validation helper — error\_message.

**Local steps**

- If not Platform.has\_permission(“Studio Page”, ptype = “write”).
  - Set error\_message from (message or Platform.\_(“You do not have permission to modify pages”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in message → Platform.\_(“You do not have permission to modify pages”).
  - Call the validation error handler Platform.throw(error\_message).
- Return fn(expanded args, expanded names kwargs).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, ptype = “write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L28) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L98) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L186)

<a id="op-685d57e77a69db"></a>
### Validate app viewer access

`operation_foundation_binding_foundation_studio_utils_validate_app_viewer_access`

**Inputs** app\_name.

**Declared result** no value.

**Record and data access** read “Studio Page” via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — Platform.\_(“Not permitted”).

**Local steps**

- If Platform.has\_permission(“Studio Page”, ptype = “read”).
  - Return no value.
- Set page\_filters from mapping(“studio\_app” → app\_name, “published” → 1).
- If Platform.session.user equals “Guest”.
  - Set page\_filters at “allow\_guest” from 1.
- If not Platform.db.exists(“Studio Page”, page\_filters).
  - Call the validation error handler Platform.throw(Platform.\_(“Not permitted”), Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, ptype = “read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L30) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L100) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L188)

<a id="op-7a5571e63d0539"></a>
### Get studio folder

`operation_foundation_binding_foundation_studio_utils_get_studio_folder`

**Inputs** Platform\_app.

**Declared result** str.

**Explicit results** Platform.get\_app\_source\_path(Platform\_app, “studio”).

**Local steps**

- Return Platform.get\_app\_source\_path(Platform\_app, “studio”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L25) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L95) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L183)

<a id="op-60afa590044950"></a>
### Get export folder

`operation_foundation_binding_foundation_studio_utils_get_export_folder`

**Inputs** Platform\_app, app\_name.

**Declared result** str.

**Explicit results** os.path.join(get\_studio\_folder(Platform\_app), get\_export\_folder\_name(app\_name)).

**Local steps**

- Return os.path.join(get\_studio\_folder(Platform\_app), get\_export\_folder\_name(app\_name)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L21) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L91) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L179)
