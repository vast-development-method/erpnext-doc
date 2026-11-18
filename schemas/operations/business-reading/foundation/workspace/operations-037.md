# Forms, reports and navigation · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Linked with

<a id="op-73e7734c7b6cd1"></a>
### Process linked docs in dependency order.mark processed

`operation_foundation_desk_form_linked_with_business_behavior_process_linked_records_in_dependency_order_mark_processed`

**Inputs** no declared parameters.

**Local steps**

- Use enclosing bindings processed.
- Update processed using + 1.
- If progress\_title.
  - Evaluate Platform.publish\_progress(percent = ((processed ÷ total) × 100), title = progress\_title).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L7340) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L217)

<a id="op-63de825b3cf22b"></a>
### Capture pending side effects

`operation_foundation_desk_form_linked_with_business_behavior_capture_pending_side_effects`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“message\_log” → list(Platform.local.message\_log), “currently\_saving” → list((Platform.flags.currently\_saving or list())), “before\_commit” → len(Platform.db.before\_commit), “after\_commit” → len(Plat ….

**Local steps**

- Return mapping(“message\_log” → list(Platform.local.message\_log), “currently\_saving” → list((Platform.flags.currently\_saving or list())), “before\_commit” → len(Platform.db.before\_commit), “after\_commit” → len(Plat ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.currently\_saving → list().
  - Value choice on hasattr(Platform.local, “\_realtime\_log”) — true gives len(Platform.local.\_realtime\_log), false gives no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(Platform.local, “\_webhook\_queue”, no value) → list().

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_webhook\_queue”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L7445) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L188)

<a id="op-d793080046dda3"></a>
### Discard side effects since

`operation_foundation_desk_form_linked_with_business_behavior_discard_side_effects_since`

**Inputs** counts.

**Local steps**

- Set Platform.local.message\_log from counts at “message\_log”.
- Set Platform.flags.currently\_saving from counts at “currently\_saving”.
- Evaluate Platform.db.before\_commit.truncate(counts at “before\_commit”).
- Evaluate Platform.db.after\_commit.truncate(counts at “after\_commit”).
- For each callback in list(expanded Platform.db.before\_rollback.cut(counts at “before\_rollback”), expanded Platform.db.after\_rollback.cut(counts at “after\_rollback”)).
  - Evaluate callback().
- If counts at “realtime\_log” is identical to no value.
  - If hasattr(Platform.local, “\_realtime\_log”).
    - Remove Platform.local.\_realtime\_log.
- Otherwise.
  - If hasattr(Platform.local, “\_realtime\_log”).
    - Set Platform.local.\_realtime\_log from Platform.local.\_realtime\_log at slice no value to counts at “realtime\_log”.
- If getattr(Platform.local, “\_webhook\_queue”, no value).
  - Set Platform.local.\_webhook\_queue from Platform.local.\_webhook\_queue at slice no value to counts at “webhook\_queue”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_webhook\_queue”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L194)

<a id="op-3f64d23a7c8c33"></a>
### Validate linked doc

`operation_foundation_desk_form_linked_with_business_behavior_validate_linked_record`

**Inputs** docinfo, ignore\_doctypes\_on\_cancel\_all = no value.

**Explicit results** false · true.

**Local steps**

- If docinfo.get(“doctype”) belongs to (ignore\_doctypes\_on\_cancel\_all or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ignore\_doctypes\_on\_cancel\_all → list().
  - Return false.
- If not Platform.get\_meta(docinfo.get(“doctype”)).is\_submittable.
  - Return false.
- If docinfo.get(“docstatus”) differs from 1.
  - Return false.
- Set auto\_cancel\_exempt\_doctypes from get\_exempted\_doctypes().
- If docinfo.get(“doctype”) belongs to auto\_cancel\_exempt\_doctypes.
  - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L522) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L226)

<a id="op-53cc2f3b220562"></a>
### Get exempted doctypes

`operation_foundation_desk_form_linked_with_business_behavior_get_exempted_record_types`

**Inputs** no declared parameters.

**Explicit results** list(Platform.get\_hooks(“auto\_cancel\_exempted\_doctypes”)).

**Local steps**

- Return list(Platform.get\_hooks(“auto\_cancel\_exempted\_doctypes”)).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“auto\_cancel\_exempted\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L812) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L200)

<a id="op-9696397cd084aa"></a>
### Get linked docs

`operation_foundation_desk_form_linked_with_business_behavior_get_linked_records`

**Inputs** doctype, name, linkinfo = no value.

**Declared result** dict at tuple(str, list).

**Record and data access** read doctype via get\_value · read “DocField” via exists · read linked\_doctype via exists · read linked\_doctype via get\_all · read linked\_doctype via get\_list.

**Explicit results** results.

**Local steps**

- If isinstance(linkinfo, str).
  - Set linkinfo from json.loads(linkinfo).
- Set results from mapping().
- If not linkinfo.
  - Return results.
- Set is\_target\_doctype\_table from Platform.get\_meta(doctype).istable.
- For each tuple(linked\_doctype, link\_context) in linkinfo.items().
  - Set linked\_doctype\_meta from Platform.get\_meta(linked\_doctype).
  - If linked\_doctype\_meta.issingle.
    - Continue with the next iteration or loop test.
  - Set has\_permission from Platform.has\_permission(linked\_doctype).
  - Set filters from list().
  - Set or\_filters from list().
  - Set ret from no value.
  - Set parent\_info from no value.
  - If filters\_ctx bound to link\_context.get(“filters”).
    - Set filters from filters\_ctx.
  - Otherwise.
    - If link\_context.get(“get\_parent”).
      - If not is\_target\_doctype\_table.
        - Continue with the next iteration or loop test.
      - Set parent\_info from (parent\_info or Platform.db.get\_value(doctype, name, list(“parenttype”, “parent”), as\_dict = true, order\_by = no value)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_info → Platform.db.get\_value(doctype, name, list(“parenttype”, “parent”), as\_dict = true, order\_by = no value).
      - If not (parent\_info and parent\_info.parenttype equals linked\_doctype).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_info → parent\_info.parenttype equals linked\_doctype.
        - Continue with the next iteration or loop test.
      - Set filters from list(list(linked\_doctype, “name”, “=”, parent\_info.parent)).
    - Otherwise.
      - If child\_doctype bound to link\_context.get(“child\_doctype”).
        - Set child\_links from (link\_context.get(“child\_links”) or list(mapping(“child\_doctype” → child\_doctype, “fieldname” → link\_context at “fieldname”))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_context.get(“child\_links”) → list(mapping(“child\_doctype” → child\_doctype, “fieldname” → link\_context at “fieldname”)).
        - Set or\_filters from list of list(child\_link at “child\_doctype”, fieldname, “=”, name) for child\_link drawn from child\_links, then fieldname drawn from child\_link at “fieldname”.
          - Draw child\_link from child\_links.
          - Draw fieldname from child\_link at “fieldname”.
        - If doctype\_fieldname bound to link\_context.get(“doctype\_fieldname”).
          - Evaluate filters.append(list(child\_doctype, doctype\_fieldname, “=”, doctype)).
      - Otherwise.
        - If link\_fieldnames bound to link\_context.get(“fieldname”).
          - If isinstance(link\_fieldnames, str).
            - Set link\_fieldnames from list(link\_fieldnames).
          - Set or\_filters from list of list(linked\_doctype, fieldname, “=”, name) for fieldname drawn from link\_fieldnames.
            - Draw fieldname from link\_fieldnames.
          - If doctype\_fieldname bound to link\_context.get(“doctype\_fieldname”).
            - Evaluate filters.append(list(linked\_doctype, doctype\_fieldname, “=”, doctype)).
          - If linked\_doctype\_meta.istable.
            - If not (Platform.db.exists(“DocField”, mapping(“options” → linked\_doctype)) or Platform.db.exists(linked\_doctype, mapping(“parenttype” → doctype, “parent” → name))).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“DocField”, mapping(“options” → linked\_doctype)) → Platform.db.exists(linked\_doctype, mapping(“parenttype” → doctype, “parent” → name)).
              - Continue with the next iteration or loop test.
  - Set total\_count from len(Platform.get\_all(linked\_doctype, filters = filters, or\_filters = or\_filters, fields = list(“name”), order\_by = no value)).
  - If not total\_count.
    - Continue with the next iteration or loop test.
  - If has\_permission.
    - Set fields from (list of d.fieldname for d drawn from linked\_doctype\_meta.get(“fields”, mapping(“in\_list\_view” → 1, “fieldtype” → list(“not in”, tuple(“Image”, “HTML”, “Button”, expanded nested operand in the contract)))) ….
      - Draw d from linked\_doctype\_meta.get(“fields”, mapping(“in\_list\_view” → 1, “fieldtype” → list(“not in”, tuple(“Image”, “HTML”, “Button”, expanded nested operand in the contract.model.table\_fields)))).
    - If add\_fields bound to link\_context.get(“add\_fields”).
      - Update fields using + add\_fields.
    - Set fields from list of sf.strip() for sf drawn from fields where sf.
      - Draw sf from fields, keep a combination only if (sf).
    - Set ret from Platform.get\_list(doctype = linked\_doctype, fields = fields, filters = filters, or\_filters = or\_filters, …).
  - Set permitted\_count from len((ret or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ret → list().
  - Set results at linked\_doctype from mapping(“docs” → (ret or list()), “hidden\_count” → (total\_count − permitted\_count)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in ret → list().
- Return results.

**Values supplied outside this operation** effective access from Platform.has\_permission(linked\_doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L60) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L204)

<a id="op-82ae0f40c7bf1c"></a>
### Get

`operation_foundation_desk_form_linked_with_business_behavior_get`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_linked\_docs(doctype = doctype, name = docname, linkinfo = linked\_doctypes).

**Local steps**

- Evaluate Platform.has\_permission(doctype, doc = docname, throw = true).
- Set linked\_doctypes from get\_linked\_doctypes(doctype = doctype).
- Return get\_linked\_docs(doctype = doctype, name = docname, linkinfo = linked\_doctypes).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = docname, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L2687) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L197)

<a id="op-5274b9a7e06893"></a>
### Get linked doctypes

`operation_foundation_desk_form_linked_with_business_behavior_get_linked_record_types`

**Inputs** doctype, without\_ignore\_user\_permissions\_enabled = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** (linked\_doctypes bitwise or remove\_excluded\_doctypes(dynamic\_links)).

**Local steps**

- If without\_ignore\_user\_permissions\_enabled.
  - Set linked\_doctypes from Platform.cache.hget(“linked\_doctypes\_without\_ignore\_user\_permissions\_enabled”, doctype, deferred anonymous expression).
- Otherwise.
  - Set linked\_doctypes from Platform.cache.hget(“linked\_doctypes”, doctype, deferred anonymous expression).
- Set dynamic\_links from get\_dynamic\_linked\_fields(doctype, without\_ignore\_user\_permissions\_enabled).
- Return (linked\_doctypes bitwise or remove\_excluded\_doctypes(dynamic\_links)).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L58) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L202)

<a id="op-0f4cb73a2f8cb9"></a>
### Get linked doctypes

`operation_foundation_desk_form_linked_with_business_behavior_get_linked_record_types_2`

**Inputs** doctype, without\_ignore\_user\_permissions\_enabled = false.

**Explicit results** remove\_excluded\_doctypes(ret).

**Local steps**

- Set ret from mapping().
- Evaluate ret.update(get\_linked\_fields(doctype, without\_ignore\_user\_permissions\_enabled)).
- For each dt in get\_parent\_doctypes(list(doctype), without\_ignore\_user\_permissions\_enabled) at doctype.
  - If dt belongs to ret.
    - Continue with the next iteration or loop test.
  - Set ret at dt from mapping(“get\_parent” → true).
- Return remove\_excluded\_doctypes(ret).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L59) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L203)

<a id="op-fa130844b6cfe9"></a>
### Get parent doctypes

`operation_foundation_binding_foundation_desk_form_linked_with_get_parent_doctypes`

**Inputs** child\_doctypes, without\_ignore\_user\_permissions\_enabled = false.

**Declared result** dict at tuple(str, list at str).

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** parents.

**Local steps**

- Set parents from mapping of child → list() for child drawn from child\_doctypes.
  - Draw child from child\_doctypes.
- If not parents.
  - Return parents.
- Set filters from list(list(“fieldtype”, “in”, Platform.model.table\_fields), list(“options”, “in”, list(parents))).
- If without\_ignore\_user\_permissions\_enabled.
  - Evaluate filters.append(list(“ignore\_user\_permissions”, “!=”, 1)).
- Set rows from (Platform.get\_all(“DocField”, filters = filters, fields = list(“parent”, “options”)) + Platform.get\_all(“Custom Field”, filters = filters, fields = list(“dt as parent”, “options”))).
- For each row in rows.
  - Evaluate parents at row.options.append(row.parent).
- Return parents.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L785)

<a id="op-774228c600bcdb"></a>
### Remove excluded doctypes

`operation_foundation_binding_foundation_desk_form_linked_with_remove_excluded_doctypes`

**Inputs** linked\_doctypes.

**Declared result** dict.

**Record and data access** read “DocType” via get\_all.

**Explicit results** linked\_doctypes.

**Local steps**

- Set custom\_doctypes from Platform.get\_all(doctype = “DocType”, filters = list(list(“custom”, “=”, 1), list(“name”, “in”, list(linked\_doctypes))), as\_list = true).
- Set custom\_doctypes from list of item at 0 for item drawn from custom\_doctypes.
  - Draw item from custom\_doctypes.
- For each dt in list(linked\_doctypes).
  - If dt belongs to custom\_doctypes.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set doctype\_module from load\_doctype\_module(dt).
  - On failure (tuple(ImportError, KeyError)).
    - Continue with the next iteration or loop test.
  - If getattr(doctype\_module, “exclude\_from\_linked\_with”, false).
    - Remove linked\_doctypes at dt.
- Return linked\_doctypes.

**Values supplied outside this operation** selected callable from getattr(doctype\_module, “exclude\_from\_linked\_with”, false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L786)

<a id="op-852c5776351d7d"></a>
### Get linked fields

`operation_foundation_desk_form_linked_with_business_behavior_get_linked_fields`

**Inputs** doctype, without\_ignore\_user\_permissions\_enabled = false.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all · read “DocType” via get\_all.

**Explicit results** ret.

**Local steps**

- Set filters from list(list(“fieldtype”, “=”, “Link”), list(“options”, “=”, doctype)).
- If without\_ignore\_user\_permissions\_enabled.
  - Evaluate filters.append(list(“ignore\_user\_permissions”, “!=”, 1)).
- Set links from Platform.get\_all(“DocField”, fields = list(“parent”, “fieldname”), filters = filters, as\_list = 1).
- Update links using + Platform.get\_all(“Custom Field”, fields = list(“dt as parent”, “fieldname”), filters = filters, as\_list = 1).
- Set ret from mapping().
- If not links.
  - Return ret.
- Set links\_dict from defaultdict(list).
- For each tuple(doctype, fieldname) in links.
  - Evaluate links\_dict at doctype.append(fieldname).
- For each doctype\_name in links\_dict.
  - Set ret at doctype\_name from mapping(“fieldname” → links\_dict.get(doctype\_name)).
- Set table\_doctypes from Platform.get\_all(“DocType”, filters = list(list(“istable”, “=”, “1”), list(“is\_virtual”, “=”, “0”), list(“name”, “in”, tuple(links\_dict)))).
- Set child\_filters from list(list(“fieldtype”, “in”, Platform.model.table\_fields), list(“options”, “in”, tuple(generator of doctype.name for doctype drawn from table\_doctypes))).
  - Draw doctype from table\_doctypes.
- If without\_ignore\_user\_permissions\_enabled.
  - Evaluate child\_filters.append(list(“ignore\_user\_permissions”, “!=”, 1)).
- For each tuple(parent, options) in Platform.get\_all(“DocField”, fields = list(“parent”, “options”), filters = child\_filters, as\_list = 1).
  - Set child\_link from mapping(“child\_doctype” → options, “fieldname” → links\_dict at options).
  - If (parent belongs to ret and “child\_doctype” belongs to ret at parent).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent belongs to ret → “child\_doctype” belongs to ret at parent.
    - If “child\_links” does not belong to ret at parent.
      - Set ret at parent at “child\_links” from list(dict(ret at parent)).
    - Evaluate ret at parent at “child\_links”.append(child\_link).
  - Otherwise.
    - Set ret at parent from child\_link.
  - Evaluate ret.pop(options, no value).
- Set virtual\_doctypes from Platform.get\_all(“DocType”, mapping(“is\_virtual” → 1), pluck = “name”).
- For each dt in virtual\_doctypes.
  - Evaluate ret.pop(dt, no value).
- Return ret.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0201.json#L3847) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L201)

<a id="op-cae7682972a851"></a>
### Get dynamic linked fields

`operation_foundation_desk_form_linked_with_business_behavior_get_dynamic_linked_fields`

**Inputs** doctype, without\_ignore\_user\_permissions\_enabled = false.

**Explicit results** ret.

**Local steps**

- Set ret from mapping().
- Set fields from list().
- For each df in get\_dynamic\_link\_map().get(doctype, list()).
  - Set meta from Platform.get\_meta(df.parent).
  - If meta.issingle.
    - Continue with the next iteration or loop test.
  - If (without\_ignore\_user\_permissions\_enabled and meta.get\_field(df.fieldname).ignore\_user\_permissions).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in without\_ignore\_user\_permissions\_enabled → meta.get\_field(df.fieldname).ignore\_user\_permissions.
    - Continue with the next iteration or loop test.
  - Evaluate fields.append(tuple(df, meta.istable)).
- Set parents from get\_parent\_doctypes(set of df.parent for tuple(df, is\_child) drawn from fields where is\_child, without\_ignore\_user\_permissions\_enabled).
  - Draw tuple(df, is\_child) from fields, keep a combination only if (is\_child).
- For each tuple(df, is\_child) in fields.
  - Set link from mapping(“fieldname” → list(df.fieldname), “doctype\_fieldname” → df.options).
  - If is\_child.
    - For each parenttype in parents at df.parent.
      - Set ret at parenttype from mapping(“child\_doctype” → df.parent, expand link).
  - Otherwise.
    - Set ret at df.parent from link.
- Return ret.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L57) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L199)

## Service · List

<a id="op-a1024fcc67b9ca"></a>
### Get list data

`operation_foundation_public_pages_list_business_behavior_get_list_data`

**Inputs** doctype, txt = no value, limit\_start = 0, fields = no value, cmd = no value, limit = 20, web\_form\_name = no value, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_list\_data\_for\_context(no value, doctype, txt, limit\_start, limit = limit, web\_form\_name = web\_form\_name, expanded names kwargs).

**Local steps**

- Return get\_list\_data\_for\_context(no value, doctype, txt, limit\_start, limit = limit, web\_form\_name = web\_form\_name, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L5709) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L39)

<a id="op-7346aaa77e2977"></a>
### Get list data for context

`operation_foundation_public_pages_list_business_behavior_get_list_data_for_context`

**Inputs** list\_context (positional only), doctype, txt = no value, limit\_start = 0, fields = no value, cmd = no value, limit = 20, web\_form\_name = no value, remaining named values kwargs.

**Explicit results** raw\_result.

**Explicit failure paths** validation helper — translated “Child DocTypes are not allowed”.

**Local steps**

- Set limit\_start from cint(limit\_start).
- If Platform.is\_table(doctype).
  - Call the validation error handler Platform.throw(translated “Child DocTypes are not allowed”, title = translated “Invalid DocType”).
- If (not txt and Platform.form\_dict.search).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not txt → Platform.form\_dict.search.
  - Set txt from Platform.form\_dict.search.
  - Remove Platform.form\_dict at “search”.
- Set controller from get\_controller(doctype).
- Set meta from Platform.get\_meta(doctype).
- Set filters from prepare\_filters(doctype, controller, kwargs).
- If list\_context is identical to no value.
  - Set list\_context from get\_list\_context(Platform.\_dict(), doctype, web\_form\_name).
- Set list\_context.title\_field from getattr(controller, “website”, mapping()).get(“page\_title\_field”, (meta.title\_field or “name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.title\_field → “name”.
- If list\_context.filters.
  - Evaluate filters.update(list\_context.filters).
- If web\_form\_name.
  - Set dynamic\_filters from get\_dynamic\_filters(web\_form\_name).
  - If dynamic\_filters.
    - Evaluate filters.update(dynamic\_filters).
- Set \_get\_list from (list\_context.get\_list or get\_list).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list\_context.get\_list → get\_list.
- Set kwargs from dict(doctype = doctype, txt = txt, filters = filters, limit\_start = limit\_start, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list\_context.order\_by → “creation desc”.
- If (not list\_context.get\_list and (list\_context.allow\_guest or meta.allow\_guest\_to\_view)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not list\_context.get\_list → (list\_context.allow\_guest or meta.allow\_guest\_to\_view).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list\_context.allow\_guest → meta.allow\_guest\_to\_view.
  - Set kwargs at “ignore\_permissions” from true.
- Set raw\_result from \_get\_list(expanded names kwargs).
- Set Platform.flags.list\_context from list\_context.
- Return raw\_result.

**Values supplied outside this operation** selected callable from get\_controller(doctype), getattr(controller, “website”, mapping()).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L5953) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L40)

<a id="op-4194dd14dc13e7"></a>
### Prepare filters

`operation_foundation_public_pages_list_business_behavior_prepare_filters`

**Inputs** doctype, controller, kwargs.

**Explicit results** filters.

**Local steps**

- For each key in kwargs.keys().
  - Attempt the following.
    - Set kwargs at key from json.loads(kwargs at key).
  - On failure (ValueError).
    - Take no action here.
- Set filters from Platform.\_dict(kwargs).
- Set meta from Platform.get\_meta(doctype).
- If (hasattr(controller, “website”) and controller.website.get(“condition\_field”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(controller, “website”) → controller.website.get(“condition\_field”).
  - Set filters at controller.website at “condition\_field” from 1.
- Otherwise.
  - If meta.is\_published\_field.
    - Set filters at meta.is\_published\_field from 1.
- If filters.pathname.
  - Evaluate resolve\_path(filters.pathname).
  - For each tuple(key, val) in Platform.local.form\_dict.items().
    - If (key does not belong to filters and key differs from “flags”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in key does not belong to filters → key differs from “flags”.
      - Set filters at key from val.
- Bind dependencies DEFAULT\_FIELD\_LABELS.
- For each fieldname in list(filters.keys()).
  - If (not meta.has\_field(fieldname) and fieldname does not belong to DEFAULT\_FIELD\_LABELS.keys()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.has\_field(fieldname) → fieldname does not belong to DEFAULT\_FIELD\_LABELS.keys().
    - Remove filters at fieldname.
- Return filters.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0544.json#L6905) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L41)

<a id="op-e494e9d1fe3ce7"></a>
### Get list context

`operation_foundation_public_pages_list_business_behavior_get_list_context`

**Inputs** context, doctype, web\_form\_name = no value.

**Record and data access** resolve a document from “Module Def” via get\_doc.

**Explicit results** list\_context.

**Local steps**

- Bind dependencies load\_doctype\_module.
- Bind dependencies get\_web\_form\_module.
- Set list\_context from (context or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → Platform.\_dict().
- Set meta from Platform.get\_meta(doctype).
- Bind local operation update\_context\_from\_module for subsequent calls.
- If not meta.custom.
  - Set module from load\_doctype\_module(doctype).
  - Set list\_context from update\_context\_from\_module(module, list\_context).
- If (meta.custom and web\_form\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.custom → web\_form\_name.
  - Set webform\_list\_contexts from Platform.get\_hooks(“webform\_list\_context”).
  - If (webform\_list\_contexts and not Platform.get\_doc(“Module Def”, meta.module).custom).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in webform\_list\_contexts → not Platform.get\_doc(“Module Def”, meta.module).custom.
    - Set out from Platform.\_dict((Platform.get\_attr(webform\_list\_contexts at 0)(meta.module) or mapping())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_attr(webform\_list\_contexts at 0)(meta.module) → mapping().
    - If out.
      - Set list\_context from out.
- If web\_form\_name.
  - Set web\_form from Platform.get\_lazy\_doc(“Web Form”, web\_form\_name).
  - Set list\_context from update\_context\_from\_module(get\_web\_form\_module(web\_form), list\_context).
- If (not meta.custom and not list\_context.row\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.custom → not list\_context.row\_template.
  - Set list\_context.row\_template from meta.get\_row\_template().
- If (not meta.custom and not list\_context.list\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not meta.custom → not list\_context.list\_template.
  - Set list\_context.template from meta.get\_list\_template().
- Return list\_context.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“webform\_list\_context”), Platform.get\_attr(webform\_list\_contexts at 0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L37)

<a id="op-bea4036556a6b6"></a>
### Get list context.update context from module

`operation_foundation_public_pages_list_business_behavior_get_list_context_update_context_from_module`

**Inputs** module, list\_context.

**Explicit results** list\_context.

**Local steps**

- If hasattr(module, “get\_list\_context”).
  - Set out from Platform.\_dict((module.get\_list\_context(list\_context) or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in module.get\_list\_context(list\_context) → mapping().
  - If out.
    - Set list\_context from out.
- Return list\_context.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L783) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L38)

<a id="op-6ac99c812d6bc4"></a>
### Get list

`operation_foundation_public_pages_list_business_behavior_get_list`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, ignore\_permissions = false, fields = no value, order\_by = no value, or\_filters = no value.

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, fields = fields, filters = filters, or\_filters = or\_filters, limit\_start = limit\_start, …).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If not filters.
  - Set filters from list().
- Set distinct from false.
- If not fields.
  - Set fields from “\*”.
  - Set distinct from true.
- If or\_filters is identical to no value.
  - Set or\_filters from list().
- If txt.
  - If meta.search\_fields.
    - Evaluate or\_filters.extend(generator of list(doctype, f, “like”, ((“%” + txt) + “%”)) for f drawn from meta.get\_search\_fields() where (f equals “name” or nested operand in the contract.get\_field(f).fieldtype belong ….
      - Draw f from meta.get\_search\_fields(), keep a combination only if ((f equals “name” or meta.get\_field(f).fieldtype belongs to tuple(“Autocomplete”, “Data”, “Text”, “Small Text”, …))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in f equals “name” → meta.get\_field(f).fieldtype belongs to tuple(“Autocomplete”, “Data”, “Text”, “Small Text”, …).
  - Otherwise.
    - If isinstance(filters, dict).
      - Set filters at “name” from tuple(“like”, ((“%” + txt) + “%”)).
    - Otherwise.
      - Evaluate filters.append(list(doctype, “name”, “like”, ((“%” + txt) + “%”))).
- Return Platform.get\_list(doctype, fields = fields, filters = filters, or\_filters = or\_filters, limit\_start = limit\_start, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L932) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L36)

<a id="op-65cbaa68a7bcae"></a>
### Get dynamic filters

`operation_foundation_public_pages_list_business_behavior_get_dynamic_filters`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** web\_form\_name.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 1 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0545.json#L1611) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L35)

## Record · List filter

[Record definition](../../../../data/record-types/list_filter.json)

<a id="op-daa95b25ce7180"></a>
### List Filter.autoname

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_autoname`

**Inputs** self.

**Local steps**

- If self.is\_standard.
  - Set self.name from formatted text {self.reference\_doctype}-{\_clean\_filter\_name(self.filter\_name)}.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L255) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L713)

<a id="op-52c11995a464d5"></a>
### List Filter.before insert

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_before_insert`

**Inputs** self.

**Record and data access** read “List Filter” via get\_all.

**Local steps**

- If (self.is\_standard and not self.layout\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → not self.layout\_order.
  - Set last from Platform.get\_all(“List Filter”, filters = mapping(“reference\_doctype” → self.reference\_doctype, “is\_standard” → 1), pluck = “layout\_order”, order\_by = “layout\_order desc”, limit = 1).
  - Set self.layout\_order from (last at 0 when last, otherwise 0 + 1).
    - Value choice on last — true gives last at 0, false gives 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L256) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L714)

<a id="op-3d816483fefbed"></a>
### List Filter.validate

`operation_foundation_desk_record_definitions_list_filter_business_behavior_list_filter_validate`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not allowed to create or edit global layouts” · validation helper with Platform.PermissionError — translated “You are not allowed to assign layouts to other users”.

**Local steps**

- If (self.is\_standard or self.\_was\_standard()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_standard → self.\_was\_standard().
  - Evaluate self.validate\_standard().
- If not self.for\_user.
  - If not \_can\_edit\_global\_filter().
    - Call the validation error handler Platform.throw(translated “You are not allowed to create or edit global layouts”, Platform.PermissionError).
  - Return no value.
- If (self.for\_user differs from Platform.session.user and not \_can\_edit\_global\_filter()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.for\_user differs from Platform.session.user → not \_can\_edit\_global\_filter().
  - Call the validation error handler Platform.throw(translated “You are not allowed to assign layouts to other users”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [was standard](operations-038.md#op-870a8ed1e4d24b), [validate standard](operations-037.md#op-54d14808585080).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L15) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L846)

<a id="op-54d14808585080"></a>
### List Filter.validate standard

`operation_foundation_binding_foundation_desk_doctype_list_filter_list_filter_listfilter_validate_standard`

**Inputs** self.

**Record and data access** read “List Filter” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Standard list layouts can only be changed in developer mode” · validation helper — translated “Only a new list layout can be made standard” · validation helper — translated “A standard list layout cannot belong to a user” · validation helper with Platform.MandatoryError — translated “Filter Name, Reference Document Type and Module are required for a standard list layout” · validation helper with Platform.DuplicateEntryError — translated “Standard list layout {0} already exists with a similar name”.format(Platform.bold(name)).

**Local steps**

- If (not Platform.conf.developer\_mode and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_migrate.
  - Call the validation error handler Platform.throw(translated “Standard list layouts can only be changed in developer mode”, Platform.PermissionError).
- If not self.is\_standard.
  - Return no value.
- If (not self.is\_new() and not self.\_was\_standard()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → not self.\_was\_standard().
  - Call the validation error handler Platform.throw(translated “Only a new list layout can be made standard”).
- If self.for\_user.
  - Call the validation error handler Platform.throw(translated “A standard list layout cannot belong to a user”).
- If not (self.filter\_name and self.reference\_doctype and self.module).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.filter\_name → self.reference\_doctype → self.module.
  - Call the validation error handler Platform.throw(translated “Filter Name, Reference Document Type and Module are required for a standard list layout”, Platform.MandatoryError).
- For each name in Platform.get\_all(“List Filter”, filters = mapping(“reference\_doctype” → self.reference\_doctype, “is\_standard” → 1, “name” → tuple(“!=”, self.name)), pluck = “name”).
  - If Platform.scrub(name) equals Platform.scrub(self.name).
    - Call the validation error handler Platform.throw(translated “Standard list layout {0} already exists with a similar name”.format(Platform.bold(name)), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [was standard](operations-038.md#op-870a8ed1e4d24b).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L261) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L719)
