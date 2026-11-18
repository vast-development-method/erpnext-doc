# Forms, reports and navigation · operations 36

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Linked with

<a id="op-53ea6e704f16be"></a>
### Submittable Document Tree.get doctype references

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_get_record_type_references`

**Inputs** self, doctype.

**Explicit results** self.\_references\_across\_doctypes.get(doctype, list()).

**Local steps**

- If self.\_references\_across\_doctypes is identical to no value.
  - Set get\_links\_to from self.get\_document\_sources().
  - Set limit\_link\_doctypes from self.get\_link\_sources().
  - Set self.\_references\_across\_doctypes from get\_references\_across\_doctypes(get\_links\_to, limit\_link\_doctypes).
- Return self.\_references\_across\_doctypes.get(doctype, list()).

**Methods declared on this owner** [get document sources](operations-036.md#op-16083f593f470c), [get link sources](operations-036.md#op-50fe7d40cb8787).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L4985) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L222)

<a id="op-16083f593f470c"></a>
### Submittable Document Tree.get document sources

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_get_document_sources`

**Inputs** self.

**Explicit results** list(set(list(expanded self.get\_link\_sources(), self.root\_doctype))).

**Local steps**

- Return list(set(list(expanded self.get\_link\_sources(), self.root\_doctype))).

**Methods declared on this owner** [get link sources](operations-036.md#op-50fe7d40cb8787).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L5167) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L219)

<a id="op-50fe7d40cb8787"></a>
### Submittable Document Tree.get link sources

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_get_link_sources`

**Inputs** self.

**Explicit results** list((set(self.get\_submittable\_doctypes()) − set((get\_exempted\_doctypes() or list())))).

**Local steps**

- Return list((set(self.get\_submittable\_doctypes()) − set((get\_exempted\_doctypes() or list())))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_exempted\_doctypes() → list().

**Methods declared on this owner** [get submittable doctypes](operations-036.md#op-c2925199953efc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L5259) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L220)

<a id="op-c2925199953efc"></a>
### Submittable Document Tree.get submittable doctypes

`operation_foundation_desk_form_linked_with_business_behavior_submittable_document_tree_get_submittable_record_types`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “DocType” via get\_all.

**Explicit results** self.\_submittable\_doctypes.

**Local steps**

- If not self.\_submittable\_doctypes.
  - Set self.\_submittable\_doctypes from Platform.get\_all(“DocType”, mapping(“is\_submittable” → 1), pluck = “name”, order\_by = no value).
- Return self.\_submittable\_doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L5373) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L223)

<a id="op-9dd1429d8d4962"></a>
### Get child tables of doctypes

`operation_foundation_desk_form_linked_with_business_behavior_get_child_tables_of_record_types`

**Inputs** doctypes = no value.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** child\_tables\_by\_doctype.

**Local steps**

- Set filters from list(list(“fieldtype”, “=”, “Table”)).
- Set filters\_for\_docfield from filters.
- Set filters\_for\_customfield from filters.
- If doctypes.
  - Set filters\_for\_docfield from list(expanded filters, list(“parent”, “in”, tuple(doctypes))).
  - Set filters\_for\_customfield from list(expanded filters, list(“dt”, “in”, tuple(doctypes))).
- Set links from Platform.get\_all(“DocField”, fields = list(“parent”, “fieldname”, “options as child\_table”), filters = filters\_for\_docfield, as\_list = 1, order\_by = no value).
- Update links using + Platform.get\_all(“Custom Field”, fields = list(“dt as parent”, “fieldname”, “options as child\_table”), filters = filters\_for\_customfield, as\_list = 1, order\_by = no value).
- Set child\_tables\_by\_doctype from defaultdict(list).
- For each tuple(doctype, fieldname, child\_table) in links.
  - Evaluate child\_tables\_by\_doctype at doctype.append(mapping(“doctype” → doctype, “fieldname” → fieldname, “child\_table” → child\_table)).
- Return child\_tables\_by\_doctype.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L5527) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L198)

<a id="op-8c10628822fa0e"></a>
### Get references across doctypes

`operation_foundation_desk_form_linked_with_business_behavior_get_references_across_record_types`

**Inputs** to\_doctypes = no value, limit\_link\_doctypes = no value.

**Declared result** list.

**Explicit results** references.

**Local steps**

- If limit\_link\_doctypes.
  - Set child\_tables\_by\_doctype from get\_child\_tables\_of\_doctypes(limit\_link\_doctypes).
  - Set all\_child\_tables from list of each at “child\_table” for each drawn from itertools.chain(expanded child\_tables\_by\_doctype.values()).
    - Draw each from itertools.chain(expanded child\_tables\_by\_doctype.values()).
  - Set limit\_link\_doctypes from (limit\_link\_doctypes + all\_child\_tables).
- Otherwise.
  - Set child\_tables\_by\_doctype from get\_child\_tables\_of\_doctypes().
  - Set all\_child\_tables from list of each at “child\_table” for each drawn from itertools.chain(expanded child\_tables\_by\_doctype.values()).
    - Draw each from itertools.chain(expanded child\_tables\_by\_doctype.values()).
- Set references\_by\_link\_fields from get\_references\_across\_doctypes\_by\_link\_field(to\_doctypes, limit\_link\_doctypes).
- Set references\_by\_dlink\_fields from get\_references\_across\_doctypes\_by\_dynamic\_link\_field(to\_doctypes, limit\_link\_doctypes).
- Set references from references\_by\_link\_fields.copy().
- For each tuple(k, v) in references\_by\_dlink\_fields.items().
  - Evaluate references.setdefault(k, list()).extend(v).
- For each links in references.values().
  - For each link in links.
    - Set link at “is\_child” from link at “doctype” belongs to all\_child\_tables.
- Return references.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L6078) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L206)

<a id="op-68d8af853e4b04"></a>
### Get references across doctypes by link field

`operation_foundation_desk_form_linked_with_business_behavior_get_references_across_record_types_by_link_field`

**Inputs** to\_doctypes = no value, limit\_link\_doctypes = no value.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** links\_by\_doctype.

**Local steps**

- Set filters from list(list(“fieldtype”, “=”, “Link”)).
- If to\_doctypes.
  - Update filters using + list(list(“options”, “in”, tuple(to\_doctypes))).
- Set filters\_for\_docfield from filters at slice no value to no value.
- Set filters\_for\_customfield from filters at slice no value to no value.
- If limit\_link\_doctypes.
  - Update filters\_for\_docfield using + list(list(“parent”, “in”, tuple(limit\_link\_doctypes))).
  - Update filters\_for\_customfield using + list(list(“dt”, “in”, tuple(limit\_link\_doctypes))).
- Set links from Platform.get\_all(“DocField”, fields = list(“parent”, “fieldname”, “options as linked\_to”), filters = filters\_for\_docfield, as\_list = 1).
- Update links using + Platform.get\_all(“Custom Field”, fields = list(“dt as parent”, “fieldname”, “options as linked\_to”), filters = filters\_for\_customfield, as\_list = 1).
- Set links\_by\_doctype from defaultdict(list).
- For each tuple(doctype, fieldname, linked\_to) in links.
  - Evaluate links\_by\_doctype at linked\_to.append(mapping(“doctype” → doctype, “fieldname” → fieldname)).
- Return links\_by\_doctype.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L6641) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L208)

<a id="op-f54defb791e219"></a>
### Get references across doctypes by dynamic link field

`operation_foundation_desk_form_linked_with_business_behavior_get_references_across_record_types_by_dynamic_link_field`

**Inputs** to\_doctypes = no value, limit\_link\_doctypes = no value.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all · read doctype via get\_all.

**Explicit results** links\_by\_doctype.

**Local steps**

- Set filters from list(list(“fieldtype”, “=”, “Dynamic Link”)).
- Set filters\_for\_docfield from filters at slice no value to no value.
- Set filters\_for\_customfield from filters at slice no value to no value.
- If limit\_link\_doctypes.
  - Update filters\_for\_docfield using + list(list(“parent”, “in”, tuple(limit\_link\_doctypes))).
  - Update filters\_for\_customfield using + list(list(“dt”, “in”, tuple(limit\_link\_doctypes))).
- Set links from Platform.get\_all(“DocField”, fields = list(“parent as doctype”, “fieldname”, “options as doctype\_fieldname”), filters = filters\_for\_docfield, as\_list = 1, order\_by = no value).
- Update links using + Platform.get\_all(“Custom Field”, fields = list(“dt as doctype”, “fieldname”, “options as doctype\_fieldname”), filters = filters\_for\_customfield, as\_list = 1, order\_by = no value).
- Set links\_by\_doctype from defaultdict(list).
- For each tuple(doctype, fieldname, doctype\_fieldname) in links.
  - Attempt the following.
    - Set filters from list(list(doctype\_fieldname, “in”, to\_doctypes)) when to\_doctypes, otherwise list().
      - Value choice on to\_doctypes — true gives list(list(doctype\_fieldname, “in”, to\_doctypes)), false gives list().
    - For each linked\_to in Platform.get\_all(doctype, pluck = doctype\_fieldname, filters = filters, distinct = 1).
      - If linked\_to.
        - Evaluate links\_by\_doctype at linked\_to.append(mapping(“doctype” → doctype, “fieldname” → fieldname, “doctype\_fieldname” → doctype\_fieldname)).
  - On failure (Platform.db.ProgrammingError).
    - Continue with the next iteration or loop test.
- Return links\_by\_doctype.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L207)

<a id="op-3ff1652f058e1f"></a>
### Get referencing documents

`operation_foundation_desk_form_linked_with_business_behavior_get_referencing_documents`

**Inputs** reference\_doctype, reference\_names, link\_info, get\_parent\_if\_child\_table\_doc = true, parent\_filters = no value, child\_filters = no value, allowed\_parents = no value, limit = no value.

**Record and data access** read from\_table via get\_all · read parent via get\_all.

**Explicit results** mapping(from\_table → names) · documents.

**Explicit failure paths** LinkedDocumentsOverflow.

**Local steps**

- Set from\_table from link\_info at “doctype”.
- Set filters from list(list(link\_info at “fieldname”, “in”, tuple(reference\_names))).
- If link\_info.get(“doctype\_fieldname”).
  - Evaluate filters.append(list(link\_info at “doctype\_fieldname”, “=”, reference\_doctype)).
- If not link\_info.get(“is\_child”).
  - Evaluate filters.extend((parent\_filters or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_filters → list().
  - Set names from Platform.get\_all(from\_table, filters, pluck = “name”, order\_by = no value, limit = limit).
  - If (limit and len(names) ≥ limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(names) ≥ limit.
    - Raise LinkedDocumentsOverflow.
  - Return mapping(from\_table → names).
- Evaluate filters.extend((child\_filters or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_filters → list().
- Set res from Platform.get\_all(from\_table, filters = filters, fields = list(“name”, “parenttype”, “parent”), order\_by = no value, limit = limit).
- If (limit and len(res) ≥ limit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(res) ≥ limit.
  - Raise LinkedDocumentsOverflow.
- Set documents from defaultdict(list).
- For each tuple(parent, rows) in itertools.groupby(res, key = deferred anonymous expression).
  - If (allowed\_parents and parent does not belong to allowed\_parents).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_parents → parent does not belong to allowed\_parents.
    - Continue with the next iteration or loop test.
  - Set filters from ((parent\_filters or list()) + list(list(“name”, “in”, tuple(generator of row.parent for row drawn from rows)))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parent\_filters → list().
    - Draw row from rows.
  - Evaluate documents at parent.extend((Platform.get\_all(parent, filters = filters, pluck = “name”, order\_by = no value) or list())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(parent, filters = filters, pluck = “name”, order\_by = no value) → list().
- Return documents.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L745) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L209)

<a id="op-e0623ea3ab0fdf"></a>
### Cancel all linked docs

`operation_foundation_desk_form_linked_with_business_behavior_cancel_all_linked_records`

**Inputs** docs = no value, ignore\_doctypes\_on\_cancel\_all = no value, root\_doctype = no value, root\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** enqueue\_discovery(“cancel”, root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all) · enqueue\_linked\_docs\_processing(to\_cancel, “cancel”, root\_doctype, root\_name, …).

**Local steps**

- Set ignore\_doctypes\_on\_cancel\_all from (Platform.parse\_json(ignore\_doctypes\_on\_cancel\_all) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(ignore\_doctypes\_on\_cancel\_all) → list().
- If docs is identical to no value.
  - Return enqueue\_discovery(“cancel”, root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all).
- Set docs from deduplicated(Platform.parse\_json(docs)).
- Set to\_cancel from list of doc for doc drawn from docs where validate\_linked\_doc(doc, ignore\_doctypes\_on\_cancel\_all).
  - Draw doc from docs, keep a combination only if (validate\_linked\_doc(doc, ignore\_doctypes\_on\_cancel\_all)).
- If (len(to\_cancel) &gt; MAX\_SYNCHRONOUS\_LINKED\_DOCS or is\_cancelled\_in\_background(root\_doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(to\_cancel) &gt; MAX\_SYNCHRONOUS\_LINKED\_DOCS → is\_cancelled\_in\_background(root\_doctype).
  - Return enqueue\_linked\_docs\_processing(to\_cancel, “cancel”, root\_doctype, root\_name, …).
- If (root\_doctype and root\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_doctype → root\_name.
  - Attempt the following.
    - Set to\_cancel from keep\_currently\_linked(to\_cancel, “cancel”, root\_doctype, root\_name, limit = MAX\_LINKED\_DOCUMENTS\_LISTED, …).
  - On failure (LinkedDocumentsOverflow).
    - Return enqueue\_discovery(“cancel”, root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all).
  - Set to\_cancel from list(expanded to\_cancel, Platform.\_dict(doctype = root\_doctype, name = root\_name)).
- Evaluate process\_linked\_docs\_in\_dependency\_order(to\_cancel, cancel\_linked\_doc, translated “Cancelling documents”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L1754) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L186)

<a id="op-4733593cee90b5"></a>
### Cancel linked doc

`operation_foundation_desk_form_linked_with_business_behavior_cancel_linked_record`

**Inputs** docinfo.

**Record and data access** resolve a document from docinfo.get(“doctype”) via get\_doc.

**State and service calls** call cancel on doc.

**Local steps**

- Set doc from Platform.get\_doc(docinfo.get(“doctype”), docinfo.get(“name”)).
- If doc.docstatus.is\_submitted().
  - Evaluate doc.cancel().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L2445) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1702) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L187)

<a id="op-0dcdcf09e29ff1"></a>
### Is cancelled in background

`operation_foundation_desk_form_linked_with_business_behavior_is_cancelled_in_background`

**Inputs** doctype.

**Explicit results** bool((doctype and Platform.get\_meta(doctype).queue\_in\_background and not is\_scheduler\_inactive())).

**Local steps**

- Return bool((doctype and Platform.get\_meta(doctype).queue\_in\_background and not is\_scheduler\_inactive())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → Platform.get\_meta(doctype).queue\_in\_background → not is\_scheduler\_inactive().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L2593) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L211)

<a id="op-b72c8971fd2a19"></a>
### Get linked docs to delete

`operation_foundation_desk_form_linked_with_business_behavior_get_linked_records_to_delete`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“docs” → docs, “count” → len(docs), “truncated” → truncated).

**Local steps**

- Evaluate Platform.has\_permission(doctype, doc = name, throw = true).
- Set tuple(docs, truncated) from collect\_deletion\_blockers(doctype, name, limit = MAX\_LINKED\_DOCUMENTS\_LISTED).
- Return mapping(“docs” → docs, “count” → len(docs), “truncated” → truncated).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, doc = name, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L2691) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L205)

<a id="op-d8cf4ebfb575cd"></a>
### Collect deletion blockers

`operation_foundation_desk_form_linked_with_business_behavior_collect_deletion_blockers`

**Inputs** doctype, name, limit = no value.

**Declared result** tuple at tuple(list, bool).

**Explicit results** tuple(list(), true) · tuple(docs, false).

**Local steps**

- Set root\_key from tuple(doctype, name).
- Set depth\_by\_document from mapping(root\_key → 0).
- Set queue from deque(list(root\_key)).
- Set fetch\_limit from (limit + 1) when limit, otherwise no value.
  - Value choice on limit — true gives (limit + 1), false gives no value.
- While queue.
  - Set parent\_key from queue.popleft().
  - Set parent from Platform.\_dict(doctype = parent\_key at 0, name = parent\_key at 1).
  - Attempt the following.
    - Set links from get\_statically\_linked\_docs(parent, method = “Delete”, limit = fetch\_limit).
    - Set dynamic\_links from get\_dynamic\_linked\_docs(parent, method = “Delete”, limit = fetch\_limit).
  - On failure (LinkedDocumentsOverflow).
    - Return tuple(list(), true).
  - For each link in list(expanded links, expanded dynamic\_links).
    - Set key from tuple(link at “reference\_doctype”, link at “reference\_docname”).
    - If key belongs to depth\_by\_document.
      - Continue with the next iteration or loop test.
    - If (limit and len(depth\_by\_document) &gt; limit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(depth\_by\_document) &gt; limit.
      - Return tuple(list(), true).
    - If not Platform.has\_permission(key at 0, doc = key at 1).
      - Continue with the next iteration or loop test.
    - Set depth\_by\_document at key from (depth\_by\_document at parent\_key + 1).
    - Evaluate queue.append(key).
- Set docs from list of mapping(“doctype” → dt, “name” → docname) for tuple(dt, docname) drawn from depth\_by\_document where tuple(dt, docname) differs from root\_key.
  - Draw tuple(dt, docname) from depth\_by\_document, keep a combination only if (tuple(dt, docname) differs from root\_key).
- Evaluate docs.sort(key = deferred anonymous expression, reverse = true).
- Return tuple(docs, false).

**Values supplied outside this operation** effective access from Platform.has\_permission(key at 0, doc = key at 1).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L2909) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L190)

<a id="op-9a9e2c25b713e6"></a>
### Delete all linked docs

`operation_foundation_desk_form_linked_with_business_behavior_delete_all_linked_records`

**Inputs** docs = no value, root\_doctype = no value, root\_name = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (dict bitwise or no value).

**Explicit results** enqueue\_discovery(“delete”, root\_doctype, root\_name) · enqueue\_linked\_docs\_processing(to\_delete, “delete”, root\_doctype, root\_name).

**Local steps**

- If docs is identical to no value.
  - Return enqueue\_discovery(“delete”, root\_doctype, root\_name).
- Set to\_delete from deduplicated(Platform.parse\_json(docs)).
- If len(to\_delete) &gt; MAX\_SYNCHRONOUS\_LINKED\_DOCS.
  - Return enqueue\_linked\_docs\_processing(to\_delete, “delete”, root\_doctype, root\_name).
- If (root\_doctype and root\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_doctype → root\_name.
  - Attempt the following.
    - Set to\_delete from keep\_currently\_linked(to\_delete, “delete”, root\_doctype, root\_name, limit = MAX\_LINKED\_DOCUMENTS\_LISTED).
  - On failure (LinkedDocumentsOverflow).
    - Return enqueue\_discovery(“delete”, root\_doctype, root\_name).
  - Set to\_delete from list(expanded to\_delete, Platform.\_dict(doctype = root\_doctype, name = root\_name)).
- Evaluate process\_linked\_docs\_in\_dependency\_order(to\_delete, delete\_linked\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L3809) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1707) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L192)

<a id="op-721651ef7453ab"></a>
### Keep currently linked

`operation_foundation_desk_form_linked_with_business_behavior_keep_currently_linked`

**Inputs** docs, action, root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all = no value, limit = no value.

**Explicit results** list of doc for doc drawn from docs where tuple(doc.get(“doctype”), doc.get(“name”)) belongs to current.

**Explicit failure paths** LinkedDocumentsOverflow.

**Local steps**

- If action equals “cancel”.
  - Set tuple(current\_docs, truncated) from collect\_cancellation\_blockers(root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all, limit = limit).
- Otherwise.
  - Set tuple(current\_docs, truncated) from collect\_deletion\_blockers(root\_doctype, root\_name, limit = limit).
- If truncated.
  - Raise LinkedDocumentsOverflow.
- Set current from set of tuple(doc at “doctype”, doc at “name”) for doc drawn from current\_docs.
  - Draw doc from current\_docs.
- Return list of doc for doc drawn from docs where tuple(doc.get(“doctype”), doc.get(“name”)) belongs to current.
  - Draw doc from docs, keep a combination only if (tuple(doc.get(“doctype”), doc.get(“name”)) belongs to current).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L4317) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L212)

<a id="op-3b1faccf43e729"></a>
### Delete linked doc

`operation_foundation_desk_form_linked_with_business_behavior_delete_linked_record`

**Inputs** docinfo.

**State and service calls** request delete\_doc for docinfo.get(“doctype”).

**Local steps**

- Evaluate Platform.delete\_doc(docinfo.get(“doctype”), docinfo.get(“name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L4702) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L193)

<a id="op-1634c9865fce02"></a>
### Enqueue discovery

`operation_foundation_desk_form_linked_with_business_behavior_enqueue_discovery`

**Inputs** action, root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all = no value.

**Explicit results** enqueue\_linked\_docs\_processing(list(), action, root\_doctype, root\_name, discover = true, …).

**Explicit failure paths** validation helper — translated “Either the documents to process or a root document is required”.

**Local steps**

- If not (root\_doctype and root\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_doctype → root\_name.
  - Call the validation error handler Platform.throw(translated “Either the documents to process or a root document is required”).
- Evaluate Platform.has\_permission(root\_doctype, doc = root\_name, throw = true).
- Return enqueue\_linked\_docs\_processing(list(), action, root\_doctype, root\_name, discover = true, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(root\_doctype, doc = root\_name, throw = true).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L4801) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L195)

<a id="op-300dbebfffbb7b"></a>
### Enqueue linked docs processing

`operation_foundation_desk_form_linked_with_business_behavior_enqueue_linked_records_processing`

**Inputs** docs, action, root\_doctype, root\_name, ignore\_doctypes\_on\_cancel\_all = no value, discover = false.

**State and service calls** enqueue with process\_linked\_docs\_in\_background.

**Explicit results** mapping(“queued” → true).

**Local steps**

- Set root from tuple(root\_doctype, root\_name) when (root\_doctype and root\_name), otherwise no value.
  - Value choice on (root\_doctype and root\_name) — true gives tuple(root\_doctype, root\_name), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in root\_doctype → root\_name.
- Set job\_kwargs from mapping().
- If root.
  - Set digest from hashlib.sha256(nested operand in the contract(nested operand in the contract).encode()).hexdigest() at slice no value to 16.
  - Set job\_kwargs from mapping(“job\_id” → formatted text linked\_docs\_{digest}, “deduplicate” → true).
- Evaluate Platform.enqueue(process\_linked\_docs\_in\_background, docs = docs, action = action, root = root, discover = discover, …).
- Return mapping(“queued” → true).

**Values supplied outside this operation** service or queued work from Platform.enqueue(process\_linked\_docs\_in\_background, docs = docs, action = action, root = root, discover = discover, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L5008) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L196)

<a id="op-6ddb028235955a"></a>
### Process linked docs in background

`operation_foundation_desk_form_linked_with_business_behavior_process_linked_records_in_background`

**Inputs** docs, action, root = no value, discover = false, ignore\_doctypes\_on\_cancel\_all = no value.

**Record and data access** read “User” via get\_value.

**State and service calls** savepoint “linked\_docs\_job” · rollback.

**Explicit results** no value.

**Local steps**

- If not Platform.db.get\_value(“User”, Platform.session.user, “enabled”).
  - Return no value.
- If root.
  - If (discover and action equals “cancel”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in discover → action equals “cancel”.
    - Set tuple(docs, \_truncated) from collect\_cancellation\_blockers(expanded root, ignore\_doctypes\_on\_cancel\_all).
  - Otherwise.
    - If discover.
      - Set tuple(docs, \_truncated) from collect\_deletion\_blockers(expanded root).
    - Otherwise.
      - Set docs from keep\_currently\_linked(docs, action, expanded root, ignore\_doctypes\_on\_cancel\_all).
  - Set docs from list(expanded docs, Platform.\_dict(doctype = root at 0, name = root at 1)).
- Set process from cancel\_linked\_doc when action equals “cancel”, otherwise delete\_linked\_doc.
  - Value choice on action equals “cancel” — true gives cancel\_linked\_doc, false gives delete\_linked\_doc.
- Set side\_effect\_counts from capture\_pending\_side\_effects().
- Evaluate Platform.db.savepoint(“linked\_docs\_job”).
- Set error from no value.
- Attempt the following.
  - Evaluate process\_linked\_docs\_in\_dependency\_order(docs, process).
- On failure (DEFERRABLE\_ERRORS) bound to blocker.
  - Evaluate Platform.db.rollback(save\_point = “linked\_docs\_job”).
  - Evaluate discard\_side\_effects\_since(side\_effect\_counts).
  - Set error from blocker.
- On failure (Platform.QueryDeadlockError) bound to deadlock.
  - Evaluate Platform.db.rollback().
  - Set error from deadlock.
- Evaluate notify\_linked\_docs\_processed(linked\_docs\_job\_message(action, len(docs), error)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L5413) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L215)

<a id="op-88a4b55ef9cee0"></a>
### Linked docs job message

`operation_foundation_desk_form_linked_with_business_behavior_linked_records_job_message`

**Inputs** action, count, error = no value.

**Explicit results** failed.format(count, error) when error, otherwise done.format(count).

**Local steps**

- Set messages from mapping(“cancel” → tuple(translated “Cancelled {0} linked documents.”, translated “Could not cancel {0} linked documents: {1}”), “delete” → tuple(translated “Deleted {0} linked documents.”, translated “Cou ….
- Set tuple(done, failed) from messages at action.
- Return failed.format(count, error) when error, otherwise done.format(count).
  - Value choice on error — true gives failed.format(count, error), false gives done.format(count).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L6117) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L213)

<a id="op-8fc289b2bec0f4"></a>
### Notify linked docs processed

`operation_foundation_desk_form_linked_with_business_behavior_notify_linked_records_processed`

**Inputs** message.

**State and service calls** publish realtime with “msgprint”.

**Local steps**

- Bind dependencies enqueue\_create\_notification.
- Evaluate Platform.publish\_realtime(“msgprint”, mapping(“message” → message, “alert” → true), user = Platform.session.user, after\_commit = true).
- Evaluate enqueue\_create\_notification(list(Platform.session.user), mapping(“type” → “Alert”, “subject” → message)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“msgprint”, mapping(“message” → message, “alert” → true), user = Platform.session.user, after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L6366) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L214)

<a id="op-4154ca2d21e777"></a>
### Deduplicated

`operation_foundation_desk_form_linked_with_business_behavior_deduplicated`

**Inputs** docs.

**Explicit results** unique.

**Local steps**

- Set seen from set().
- Set unique from list().
- For each doc in docs.
  - Set key from tuple(doc.get(“doctype”), doc.get(“name”)).
  - If key does not belong to seen.
    - Evaluate seen.add(key).
    - Evaluate unique.append(doc).
- Return unique.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L6558) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1706) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L191)

<a id="op-2ff5cfd359ea00"></a>
### Process linked docs in dependency order

`operation_foundation_desk_form_linked_with_business_behavior_process_linked_records_in_dependency_order`

**Inputs** docs, process, progress\_title = no value.

**State and service calls** savepoint save\_point · rollback · release savepoint save\_point.

**Local steps**

- Set total from len(docs).
- Set processed from 0.
- Set save\_point from “process\_linked\_doc”.
- Bind local operation mark\_processed for subsequent calls.
- While docs.
  - Set deferred from list().
  - For each doc in docs.
    - Set side\_effect\_counts from capture\_pending\_side\_effects().
    - Evaluate Platform.db.savepoint(save\_point).
    - Attempt the following.
      - Evaluate process(doc).
    - On failure (DEFERRABLE\_ERRORS).
      - Evaluate Platform.db.rollback(save\_point = save\_point).
      - Evaluate discard\_side\_effects\_since(side\_effect\_counts).
      - Evaluate deferred.append(doc).
      - Continue with the next iteration or loop test.
    - Evaluate Platform.db.release\_savepoint(save\_point).
    - Evaluate mark\_processed().
  - If len(deferred) equals len(docs).
    - Evaluate process(deferred at 0).
    - Evaluate mark\_processed().
    - Set deferred from deferred at slice 1 to no value.
  - Set docs from deferred.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0200.json#L6775) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L216)
