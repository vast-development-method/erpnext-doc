# Forms, reports and navigation · operations 54

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Save

<a id="op-4fbc5b073a4682"></a>
### Savedocs

`operation_foundation_desk_form_save_business_behavior_savedocs`

**Inputs** doc, action.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from json.loads(doc) via get\_doc · resolve a document from doc.doctype via get\_doc.

**State and service calls** call submit on doc · call save on doc · msgprint with Platform.\_(status\_message).

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(json.loads(doc)).
- If action equals “Cancel”.
  - Set doc from Platform.get\_doc(doc.doctype, doc.name).
- Evaluate capture\_doc(doc, action).
- If (doc.get(“\_\_islocal”) and doc.name.startswith((“new-” + nested operand in the contract.lower().replace(one space, “-”)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.get(“\_\_islocal”) → doc.name.startswith((“new-” + nested operand in the contract.doctype.lower().replace(one space, “-”))).
  - Set doc.\_\_temporary\_name from doc.name.
- For each child in doc.get\_all\_children().
  - Set child.\_\_temporary\_name from child.name.
- Evaluate set\_local\_name(doc).
- Set doc.docstatus from mapping(“Save” → DocStatus.DRAFT, “Submit” → DocStatus.SUBMITTED, “Update” → DocStatus.SUBMITTED, “Cancel” → DocStatus.CANCELLED) at action.
- If doc.docstatus.is\_submitted().
  - If (action equals “Submit” and doc.meta.queue\_in\_background and not is\_scheduler\_inactive()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in action equals “Submit” → doc.meta.queue\_in\_background → not is\_scheduler\_inactive().
    - Evaluate queue\_submission(doc, action).
    - Return no value.
  - Evaluate doc.submit().
- Otherwise.
  - Evaluate doc.save().
- Evaluate run\_onload(doc).
- Evaluate send\_updated\_docs(doc).
- Evaluate add\_data\_to\_monitor(doctype = doc.doctype, action = action).
- Set status\_message from “Submitted” when doc.docstatus.is\_submitted(), otherwise “Saved”.
  - Value choice on doc.docstatus.is\_submitted() — true gives “Submitted”, false gives “Saved”.
- Evaluate Platform.msgprint(Platform.\_(status\_message), indicator = “green”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L71) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L272)

<a id="op-87f4327d758c01"></a>
### Cancel

`operation_foundation_desk_form_save_business_behavior_cancel`

**Inputs** doctype = no value, name = no value, workflow\_state\_fieldname = no value, workflow\_state = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call cancel on doc · msgprint with Platform.\_(“Cancelled”).

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate capture\_doc(doc, “Cancel”).
- If (workflow\_state\_fieldname and workflow\_state).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in workflow\_state\_fieldname → workflow\_state.
  - Set workflow from get\_workflow\_name(doc.doctype).
  - If (workflow and workflow\_state\_fieldname equals get\_workflow\_state\_field(workflow)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in workflow → workflow\_state\_fieldname equals get\_workflow\_state\_field(workflow).
    - Evaluate doc.set(workflow\_state\_fieldname, workflow\_state).
- If (doc.meta.queue\_in\_background and not is\_scheduler\_inactive()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.queue\_in\_background → not is\_scheduler\_inactive().
  - Evaluate queue\_submission(doc, “Cancel”).
  - Return no value.
- Evaluate doc.cancel().
- Evaluate send\_updated\_docs(doc).
- Evaluate Platform.msgprint(Platform.\_(“Cancelled”), indicator = “red”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L70) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L270)

<a id="op-bf3224bf5c2c35"></a>
### Discard

`operation_foundation_desk_form_save_business_behavior_discard`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”, “PUT”)).

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** msgprint with Platform.\_(“Discarded”).

**Local steps**

- Set doc from Platform.get\_doc(doctype, name).
- Evaluate capture\_doc(doc, “Discard”).
- Evaluate doc.discard().
- Evaluate send\_updated\_docs(doc).
- Evaluate Platform.msgprint(Platform.\_(“Discarded”), indicator = “red”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L271)

<a id="op-ca81da0294cdbb"></a>
### Send updated docs

`operation_foundation_desk_form_save_business_behavior_send_updated_records`

**Inputs** doc.

**Local steps**

- Bind dependencies get\_docinfo.
- Evaluate get\_docinfo(doc).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Set d from doc.as\_dict().
- If hasattr(doc, “localname”).
  - Set d at “localname” from doc.localname.
- Evaluate Platform.response.docs.append(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L264) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L273)

<a id="op-ab202caaaf63f4"></a>
### Set local name

`operation_foundation_desk_form_save_business_behavior_set_local_name`

**Inputs** doc.

**Local steps**

- Bind local operation \_set\_local\_name for subsequent calls.
- Evaluate \_set\_local\_name(doc).
- For each child in doc.get\_all\_children().
  - Evaluate \_set\_local\_name(child).
- If doc.get(“\_\_newname”).
  - Set doc.name from doc.get(“\_\_newname”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L447) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L274)

<a id="op-d83119221b9865"></a>
### Set local name.set local name

`operation_foundation_desk_form_save_business_behavior_set_local_name_set_local_name`

**Inputs** d.

**Local steps**

- If (doc.get(“\_\_islocal”) or d.get(“\_\_islocal”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“\_\_islocal”) → d.get(“\_\_islocal”).
  - Set d.localname from d.name.
  - Set d.name from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0204.json#L715) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L275)

## Service · Scripts

<a id="op-c49f966002e4f8"></a>
### Run get page script

`operation_foundation_binding_foundation_studio_ai_agent_tools_scripts_run_get_page_script`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “No page in context.” · “This page has no script yet.” · formatted text Current page script (stored in {where}): {source}.

**Local steps**

- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “No page in context.”.
- Set source from page.get\_script\_source().
- If not source.strip().
  - Return “This page has no script yet.”.
- Set where from formatted text code file ({os.path.basename(page.get\_script\_file\_path())}) when page.has\_script\_file(), otherwise “the page's ′script′ field (DB)”.
  - Value choice on page.has\_script\_file() — true gives formatted text code file ({os.path.basename(page.get\_script\_file\_path())}), false gives “the page's ′script′ field (DB)”.
- Return formatted text Current page script (stored in {where}): {source}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L128) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1791)

<a id="op-2eddf69d07ff62"></a>
### Run set page script

`operation_foundation_binding_foundation_studio_ai_agent_tools_scripts_run_set_page_script`

**Inputs** ctx, args.

**Declared result** str.

**Explicit results** “FAILED: script is required — pass the FULL script, not a fragment.” · “FAILED: no page in context.” · “FAILED: a page script is an ES module — its default export must be ′export default function setup(context) { …” · \_write\_file\_script(ctx, page, source) · \_write\_db\_script(ctx, page, source).

**Local steps**

- Set source from args.get(“script”).
- If (not isinstance(source, str) or not source.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(source, str) → not source.strip().
  - Return “FAILED: script is required — pass the FULL script, not a fragment.”.
- Set page from load\_page(ctx).
- If page is identical to no value.
  - Return “FAILED: no page in context.”.
- If “export default” does not belong to source.
  - Return “FAILED: a page script is an ES module — its default export must be ′export default function setup(context) { …”.
- If page.is\_standard.
  - Return \_write\_file\_script(ctx, page, source).
- Return \_write\_db\_script(ctx, page, source).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L129) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1792)

<a id="op-b508827c157215"></a>
### Write db script

`operation_foundation_binding_foundation_studio_ai_agent_tools_scripts_write_db_script`

**Inputs** ctx, page, source.

**Declared result** str.

**Explicit results** “FAILED: you do not have permission to edit this page.” · formatted text FAILED: {error} · “Updated the page script. It runs live on the canvas now.”.

**Local steps**

- If not Platform.has\_permission(“Studio Page”, “write”, page.name).
  - Return “FAILED: you do not have permission to edit this page.”.
- Set page.script from source.
- If error bound to save\_page(page).
  - Return formatted text FAILED: {error}.
- Evaluate ctx.emit(“reload”, script = true).
- Return “Updated the page script. It runs live on the canvas now.”.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Studio Page”, “write”, page.name).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L130) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1793)

<a id="op-35cadb0bbf2496"></a>
### Write file script

`operation_foundation_binding_foundation_studio_ai_agent_tools_scripts_write_file_script`

**Inputs** ctx, page, source.

**Declared result** str.

**State and service calls** enqueue doc with “Studio App”.

**Explicit results** “FAILED: this page belongs to a repository app — its script lives in a code file editable only in developer m …” · “FAILED: writing a repository app's page script requires the System Manager role.” · “Wrote the page script to its code file and started an app rebuild. The change appears on the canvas only aft …”.

**Local steps**

- If not Platform.conf.developer\_mode.
  - Return “FAILED: this page belongs to a repository app — its script lives in a code file editable only in developer m …”.
- If “System Manager” does not belong to Platform.get\_roles().
  - Return “FAILED: writing a repository app's page script requires the System Manager role.”.
- Set page.script from source.
- Evaluate page.write\_script\_file().
- Evaluate Platform.enqueue\_doc(“Studio App”, page.studio\_app, “build\_app\_bundle”, queue = “long”, timeout = 1200).
- Return “Wrote the page script to its code file and started an app rebuild. The change appears on the canvas only aft …”.

**Values supplied outside this operation** effective access from Platform.get\_roles() · service or queued work from Platform.enqueue\_doc(“Studio App”, page.studio\_app, “build\_app\_bundle”, queue = “long”, timeout = 1200).

**Boundaries to resolve** external or queued work, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L131) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1818) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1794)

## Service · Search

<a id="op-feaa92293b3b10"></a>
### Sanitize searchfield

`operation_foundation_desk_search_business_behavior_sanitize_searchfield`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** searchfield.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0214.json#L6176) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L982) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1422)

<a id="op-017e2dfce44518"></a>
### Search link

`operation_foundation_desk_search_business_behavior_search_link`

**Inputs** doctype, txt, query = no value, filters = no value, page\_length = 10, searchfield = no value, reference\_doctype = no value, ignore\_user\_permissions = false, link\_fieldname (named only, default no value), start (named only, default 0), include\_image (named only, default false), keep\_order (named only, default false).

**Wrappers, in declaration order** Platform.whitelist(), http\_cache(max\_age = 60, stale\_while\_revalidate = (5 × 60)).

**Declared result** list at LinkSearchResults.

**Explicit results** rows.

**Local steps**

- Set results from search\_widget(doctype, txt.strip(), query, searchfield = searchfield, start = cint(start), page\_length = page\_length, filters = filters, …).
- Set rows from build\_for\_autosuggest(results, doctype = doctype).
- If sbool(include\_image).
  - Evaluate add\_images(rows, doctype).
- Return rows.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L67) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L984) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1424)

<a id="op-54364fc9edf8dc"></a>
### Get image field

`operation_foundation_binding_foundation_desk_search_get_image_field`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Explicit results** no value · meta.image\_field.

**Local steps**

- If not Platform.has\_permission(doctype, “read”).
  - Return no value.
- Set meta from Platform.get\_meta(doctype).
- If not meta.image\_field.
  - Return no value.
- Set df from meta.get\_field(meta.image\_field).
- If (not df or getattr(df, “is\_virtual”, false)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → getattr(df, “is\_virtual”, false).
  - Return no value.
- If (df.permlevel and df.permlevel does not belong to meta.get\_permlevel\_access(“read”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.permlevel → df.permlevel does not belong to meta.get\_permlevel\_access(“read”).
  - Return no value.
- Return meta.image\_field.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”) · selected callable from getattr(df, “is\_virtual”, false).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L845) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L821)

<a id="op-bd4f3102dce32b"></a>
### Add images

`operation_foundation_binding_foundation_desk_search_add_images`

**Inputs** rows, doctype.

**Declared result** no value.

**Record and data access** read doctype via get\_list.

**Explicit results** no value.

**Local steps**

- Set image\_field from get\_image\_field(doctype).
- If (not image\_field or not rows).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not image\_field → not rows.
  - Return no value.
- Set images from dict(Platform.get\_list(doctype, filters = mapping(“name” → list(“in”, list of r at “value” for r drawn from rows)), fields = list(“name”, image\_field), as\_list = true)).
  - Draw r from rows.
- For each row in rows.
  - Set image from images.get(row at “value”).
  - If image.
    - Set row at “image” from image.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L844) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L820)

<a id="op-03c2d62e3a1747"></a>
### Make dict from filter list

`operation_foundation_desk_search_business_behavior_make_mapping_from_filter_list`

**Inputs** filters.

**Declared result** dict.

**Explicit results** \_filters.

**Local steps**

- Set \_filters from mapping().
- For each f in filters.
  - Set tuple(fieldname, operator, value) from tuple(f at 1, f at 2, f at 3).
  - Set \_filters at fieldname from value when operator equals “=”, otherwise list(operator, value).
    - Value choice on operator equals “=” — true gives value, false gives list(operator, value).
- Return \_filters.

[Applicable decision contract](../../../foundation-decision-contracts/part-0215.json#L420) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L979) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1419)

<a id="op-5f9cd6d00e50e8"></a>
### Search widget

`operation_foundation_desk_search_business_behavior_search_widget`

**Inputs** doctype, txt, query = no value, searchfield = no value, start = 0, page\_length = 10, filters = no value, filter\_fields = no value, as\_dict = false, reference\_doctype = no value, ignore\_user\_permissions = false, link\_fieldname (named only, default no value), for\_link\_validation (named only, default false), query\_filters\_as\_dict (named only, default false), keep\_order (named only, default false).

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**State and service calls** call insert on formatted\_fields.

**Explicit results** list() · values.

**Explicit failure paths** propagate active failure.

**Local steps**

- If ignore\_user\_permissions.
  - If (reference\_doctype and link\_fieldname).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype → link\_fieldname.
    - Set ignore\_user\_permissions from validate\_ignore\_user\_permissions(reference\_doctype, link\_fieldname, doctype).
  - Otherwise.
    - Evaluate Platform.logger().error(“setting ignore\_user\_permissions=True requires reference\_doctype and link\_fieldname to be set. Ignoring flag.”).
    - Set ignore\_user\_permissions from false.
- Set start from cint(start).
- Set page\_length from cint(page\_length).
- If page\_length ≤ 0.
  - Set page\_length from PAGE\_LENGTH\_FOR\_LINK\_VALIDATION.
- If isinstance(filters, str).
  - Set filters from json.loads(filters).
- If searchfield.
  - Evaluate sanitize\_searchfield(searchfield).
- If not searchfield.
  - Set searchfield from “name”.
- Set standard\_queries from (Platform.get\_hooks().standard\_queries or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks().standard\_queries → mapping().
- If (not query and doctype belongs to standard\_queries).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not query → doctype belongs to standard\_queries.
  - Set query from standard\_queries at doctype at negative 1.
- If filters is identical to no value.
  - Set filters from mapping().
- If query.
  - Set meta from Platform.get\_meta(doctype).
  - Set query\_txt from empty text when meta.translated\_doctype, otherwise txt.
    - Value choice on meta.translated\_doctype — true gives empty text, false gives txt.
  - Set query\_start from 0 when meta.translated\_doctype, otherwise start.
    - Value choice on meta.translated\_doctype — true gives 0, false gives start.
  - Set query\_page\_length from PAGE\_LENGTH\_FOR\_LINK\_VALIDATION when meta.translated\_doctype, otherwise page\_length.
    - Value choice on meta.translated\_doctype — true gives PAGE\_LENGTH\_FOR\_LINK\_VALIDATION, false gives page\_length.
  - If (sbool(query\_filters\_as\_dict) and isinstance(filters, list)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sbool(query\_filters\_as\_dict) → isinstance(filters, list).
    - Set filters from make\_dict\_from\_filter\_list(filters).
  - If ignore\_user\_permissions.
    - Set Platform.flags.ignore\_user\_permissions\_for\_doctype from doctype.
  - Attempt the following.
    - Evaluate is\_whitelisted(Platform.get\_attr(query)).
    - Set values from Platform.call(query, doctype, query\_txt, searchfield, as\_dict = as\_dict, reference\_doctype = reference\_doctype, ignore\_user\_permissions = ignore\_user\_permissions, link\_fieldname = link\_fieldname, …).
  - On failure (tuple(Platform.PermissionError, Platform.AppNotInstalledError, ImportError)).
    - If Platform.local.conf.developer\_mode.
      - Propagate the active failure.
    - Otherwise.
      - Evaluate Platform.respond\_as\_web\_page(title = “Invalid Method”, html = “Method not found”, indicator\_color = “red”, http\_status\_code = 404).
      - Return list().
  - On exit, including pending return or failure.
    - Set Platform.flags.ignore\_user\_permissions\_for\_doctype from no value.
  - If (not for\_link\_validation and meta.translated\_doctype).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not for\_link\_validation → meta.translated\_doctype.
    - Set values from page\_translated(values, txt, as\_dict, start, …).
  - Return values.
- Set meta from Platform.get\_meta(doctype).
- Set include\_disabled from false.
- If isinstance(filters, dict).
  - If “include\_disabled” belongs to filters.
    - If filters at “include\_disabled” equals 1.
      - Set include\_disabled from true.
    - Evaluate filters.pop(“include\_disabled”).
  - Set filters from list of make\_filter\_tuple(doctype, key, value) for tuple(key, value) drawn from filters.items().
    - Draw tuple(key, value) from filters.items().
- If for\_link\_validation.
  - Evaluate filters.append(list(doctype, “name”, “=”, txt)).
- Set or\_filters from list().
- If txt.
  - Set field\_types from set(“Autocomplete”, “Data”, “Text”, “Small Text”, …).
  - Set search\_fields from list(“name”).
  - If meta.title\_field.
    - Evaluate search\_fields.append(meta.title\_field).
  - If meta.search\_fields.
    - Evaluate search\_fields.extend(meta.get\_search\_fields()).
  - For each f in search\_fields.
    - Set fmeta from meta.get\_field(f.strip()).
    - If (not meta.translated\_doctype and (f equals “name” or (fmeta and fmeta.fieldtype belongs to field\_types))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.translated\_doctype → (f equals “name” or (fmeta and fmeta.fieldtype belongs to field\_types)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f equals “name” → (fmeta and fmeta.fieldtype belongs to field\_types).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fmeta → fmeta.fieldtype belongs to field\_types.
      - Evaluate or\_filters.append(list(doctype, f.strip(), “like”, formatted text %{txt}%)).
- If not include\_disabled.
  - If meta.get(“fields”, mapping(“fieldname” → “enabled”, “fieldtype” → “Check”)).
    - Evaluate filters.append(list(doctype, “enabled”, “=”, 1)).
  - If meta.get(“fields”, mapping(“fieldname” → “disabled”, “fieldtype” → “Check”)).
    - Evaluate filters.append(list(doctype, “disabled”, “!=”, 1)).
- Set fields from get\_std\_fields\_list(meta, (searchfield or “name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in searchfield → “name”.
- If filter\_fields.
  - Set fields from list(set((fields + json.loads(filter\_fields)))).
- Set formatted\_fields from list of f.strip() for f drawn from fields.
  - Draw f from fields.
- If (meta.show\_title\_field\_in\_link and meta.title\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.show\_title\_field\_in\_link → meta.title\_field.
  - Evaluate formatted\_fields.insert(1, formatted text {meta.title\_field} as label).
- Set order\_by\_based\_on\_meta from get\_order\_by(doctype, meta).
- Set order\_by from formatted text idx desc, {order\_by\_based\_on\_meta}, ′tab{doctype}′.′name′ asc.
- Set add\_relevance from (bool(txt) and not for\_link\_validation and not meta.translated\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(txt) → not for\_link\_validation → not meta.translated\_doctype.
- If add\_relevance.
  - Set \_txt from Platform.db.escape((txt or empty text).replace(“%”, empty text).replace(“@”, empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in txt → empty text.
  - Set \_relevance\_expr from mapping(“DIV” → list(1, mapping(“NULLIF” → list(mapping(“LOCATE” → list(\_txt, “name”)), 0)))).
  - Set \_relevance from mapping(“IFNULL” → list(\_relevance\_expr, negative 9999), “as” → “\_relevance”).
  - Evaluate formatted\_fields.append(\_relevance).
  - Set order\_by from formatted text \_relevance desc, {order\_by}.
- Set values from Platform.get\_list(doctype, filters = filters, fields = formatted\_fields, or\_filters = or\_filters, limit\_start = 0 when meta.translated\_doctype, otherwise start, …).
  - Value choice on meta.translated\_doctype — true gives 0, false gives start.
  - Value choice on meta.translated\_doctype — true gives no value, false gives page\_length.
- If not for\_link\_validation.
  - If meta.translated\_doctype.
    - Set values from page\_translated(values, txt, as\_dict, start, …).
  - Otherwise.
    - If not keep\_order.
      - Set values from sorted(values, key = deferred anonymous expression).
  - If add\_relevance.
    - If as\_dict.
      - For each r in values.
        - Evaluate r.pop(“\_relevance”, no value).
    - Otherwise.
      - Set values from list of r at slice no value to negative 1 for r drawn from values.
        - Draw r from values.
- Return values.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(), Platform.get\_attr(query).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L68) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L985) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1425)

<a id="op-7d5ffe9e4161bc"></a>
### Page translated

`operation_foundation_binding_foundation_desk_search_page_translated`

**Inputs** values, txt, as\_dict, start, page\_length.

**Declared result** list.

**Explicit results** values at slice start to (start + page\_length).

**Local steps**

- Set values from filter\_translated(values, txt, as\_dict).
- Set values from sorted(values, key = deferred anonymous expression).
- Return values at slice start to (start + page\_length).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L822)

<a id="op-3a725d836d087f"></a>
### Validate ignore user permissions

`operation_foundation_desk_search_business_behavior_validate_ignore_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** form\_doctype, link\_fieldname, link\_doctype.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** record lookup.

**Local structure** 18 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L69) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L988) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1426)

<a id="op-a981a22dbe3133"></a>
### Validate ignore user permissions.throw

`operation_foundation_desk_search_business_behavior_validate_ignore_user_permissions_throw`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** message.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0215.json#L5788) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L989) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1427)

<a id="op-b5fdfb30f085bf"></a>
### Validate ignore user permissions.can search

`operation_foundation_binding_foundation_desk_search_validate_ignore_user_permissions_can_search`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** fields.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L98) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L823)

<a id="op-941450dc077a74"></a>
### Get std fields list

`operation_foundation_desk_search_business_behavior_get_standard_fields_list`

**Inputs** meta, key.

**Explicit results** sflist.

**Local steps**

- Set sflist from list(“name”).
- If (meta.title\_field and meta.title\_field does not belong to sflist).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.title\_field → meta.title\_field does not belong to sflist.
  - Evaluate sflist.append(meta.title\_field).
- If key does not belong to sflist.
  - Evaluate sflist.append(key).
- If meta.search\_fields.
  - For each d in meta.search\_fields.split(“,”).
    - If d.strip() does not belong to sflist.
      - Evaluate sflist.append(d.strip()).
- Return sflist.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0215.json#L5869) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L976) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1416)

<a id="op-e6b233d4063431"></a>
### Build for autosuggest

`operation_foundation_desk_search_business_behavior_build_for_autosuggest`

**Inputs** res, doctype.

**Declared result** list at LinkSearchResults.

**Explicit results** results.

**Local steps**

- Bind local operation to\_string for subsequent calls.
- Set results from list().
- Set meta from Platform.get\_meta(doctype).
- If meta.show\_title\_field\_in\_link.
  - For each item in res.
    - Set item from list(item).
    - If len(item) equals 1.
      - Set item from list(item at 0, item at 0).
    - Set label from translated item at 1 when meta.translated\_doctype, otherwise item at 1.
      - Value choice on meta.translated\_doctype — true gives translated item at 1, false gives item at 1.
    - Set item at 1 from item at 0.
    - If (len(item) ≥ 3 and item at 2 equals label).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(item) ≥ 3 → item at 2 equals label.
      - Remove item at 2.
    - Set autosuggest\_row from mapping(“value” → item at 0, “description” → to\_string(item at slice 1 to no value)).
    - If label.
      - Set autosuggest\_row at “label” from label.
    - Evaluate results.append(autosuggest\_row).
- Otherwise.
  - For each item in res.
    - Set label from translated item at 0 when meta.translated\_doctype, otherwise item at 0.
      - Value choice on meta.translated\_doctype — true gives translated item at 0, false gives item at 0.
    - Evaluate results.append(mapping(“value” → item at 0, “description” → to\_string(item at slice 1 to no value), “label” → label)).
- Return results.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L65) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1411)

<a id="op-236c1d437115cd"></a>
### Build for autosuggest.to string

`operation_foundation_desk_search_business_behavior_build_for_autosuggest_to_string`

**Inputs** parts.

**Explicit results** “, ”.join(unique(generator of translated cstr(part) when meta.translated\_doctype, otherwise cstr(part) for part drawn from parts where part)).

**Local steps**

- Return “, ”.join(unique(generator of translated cstr(part) when meta.translated\_doctype, otherwise cstr(part) for part drawn from parts where part)).
  - Draw part from parts, keep a combination only if (part).
  - Value choice on meta.translated\_doctype — true gives translated cstr(part), false gives cstr(part).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0215.json#L7173) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1412)

<a id="op-49e30a462179b4"></a>
### Scrub custom query

`operation_foundation_desk_search_business_behavior_scrub_custom_query`

**Inputs** query, key, txt.

**Explicit results** query.

**Local steps**

- If “%(key)s” belongs to query.
  - Set query from query.replace(“%(key)s”, key).
- If “%s” belongs to query.
  - Set query from query.replace(“%s”, ((txt or empty text) + “%”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in txt → empty text.
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0215.json#L7321) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L983) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1423)
