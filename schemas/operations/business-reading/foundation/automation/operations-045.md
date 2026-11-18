# Workflow, automation and dispatch · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Scheduler

<a id="op-95ebc54d543d80"></a>
### Filter fieldnames

`operation_foundation_binding_foundation_automation_engine_scheduler_filter_fieldnames`

**Inputs** stored.

**Declared result** set at str.

**Explicit results** set() · set(stored.keys()) · set of row at 1 when len(row) &gt; 3, otherwise row at 0 for row drawn from stored where isinstance(row, (list bitwise or tuple)).

**Local steps**

- If not stored.
  - Return set().
- If isinstance(stored, dict).
  - Return set(stored.keys()).
- Return set of row at 1 when len(row) &gt; 3, otherwise row at 0 for row drawn from stored where isinstance(row, (list bitwise or tuple)).
  - Draw row from stored, keep a combination only if (isinstance(row, (list bitwise or tuple))).
  - Value choice on len(row) &gt; 3 — true gives row at 1, false gives row at 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L64) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L522)

<a id="op-37c50cac60e531"></a>
### Payload

`operation_foundation_binding_foundation_automation_engine_scheduler_payload`

**Inputs** fire\_at.

**Declared result** dict.

**Explicit results** mapping(“trigger\_type” → “Scheduled”, SCHEDULED\_PAYLOAD\_KEY → fire\_at.replace(microsecond = 0).strftime(“%Y-%m-%d %H:%M:%S”)).

**Local steps**

- Return mapping(“trigger\_type” → “Scheduled”, SCHEDULED\_PAYLOAD\_KEY → fire\_at.replace(microsecond = 0).strftime(“%Y-%m-%d %H:%M:%S”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L70) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L528)

<a id="op-ab66502214fcb1"></a>
### Process date based

`operation_foundation_binding_foundation_automation_engine_scheduler_process_date_based`

**Inputs** now = no value.

**Explicit results** no value.

**Local steps**

- If not settings.is\_enabled().
  - Return no value.
- Set today from getdate((now or now\_datetime())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in now → now\_datetime().
- Set queued from sum(generator of \_queue\_date\_rule(rule, today) for rule drawn from \_date\_based\_rules()).
  - Draw rule from \_date\_based\_rules().
- If queued.
  - Evaluate Platform.db.after\_commit.add(kick\_drainer).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L72) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L530)

<a id="op-b428c8ab7ef80d"></a>
### Date based rules

`operation_foundation_binding_foundation_automation_engine_scheduler_date_based_rules`

**Inputs** no declared parameters.

**Declared result** list.

**Record and data access** read “Automation Flow” via get\_all.

**Explicit results** Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “trigger\_type” → “Date Based”), fields = list(“name”, “document\_type”, “date\_field”, “date\_offset”, …)).

**Local steps**

- Return Platform.get\_all(“Automation Flow”, filters = mapping(“enabled” → 1, “trigger\_type” → “Date Based”), fields = list(“name”, “document\_type”, “date\_field”, “date\_offset”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L60) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L518)

<a id="op-4dce55a1ecadf9"></a>
### Queue date rule

`operation_foundation_binding_foundation_automation_engine_scheduler_queue_date_rule`

**Inputs** rule, today.

**Declared result** int.

**Explicit results** 0 · queued.

**Local steps**

- If not (rule.document\_type and rule.date\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rule.document\_type → rule.date\_field.
  - Return 0.
- Set handled from \_handled\_names(rule.name, get\_datetime(formatted text {today} 00:00:00)).
- Set queued from 0.
- For each name in \_due\_names(rule, \_target\_date(rule, today)).
  - If name belongs to handled.
    - Continue with the next iteration or loop test.
  - Evaluate queue\_trigger(rule.name, rule.document\_type, name, payload = \_date\_payload(rule, today)).
  - Update queued using + 1.
- Return queued.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L73) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L555) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L531)

<a id="op-349157ab8bc326"></a>
### Target date

`operation_foundation_binding_foundation_automation_engine_scheduler_target_date`

**Inputs** rule, today.

**Explicit results** add\_days(today, offset).

**Local steps**

- Set offset from cint(rule.date\_offset).
- If rule.date\_direction equals “After”.
  - Set offset from negative offset.
- Return add\_days(today, offset).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L77) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L535)

<a id="op-657a9e505ca293"></a>
### Due names

`operation_foundation_binding_foundation_automation_engine_scheduler_due_names`

**Inputs** rule, target.

**Declared result** list at str.

**Record and data access** read rule.document\_type via get\_all.

**Explicit results** \_condition\_filtered(rule, names).

**Local steps**

- Set filters from list(expanded \_normalize\_filters(Platform.parse\_json(rule.filters) when rule.filters, otherwise no value), list(rule.date\_field, “between”, list(formatted text {target} 00:00:00, formatted text {target} 23:59:59))).
  - Value choice on rule.filters — true gives Platform.parse\_json(rule.filters), false gives no value.
- Set names from Platform.get\_all(rule.document\_type, filters = filters, pluck = “name”).
- Return \_condition\_filtered(rule, names).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L62) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L520)

<a id="op-045730ea677214"></a>
### Normalize filters

`operation_foundation_binding_foundation_automation_engine_scheduler_normalize_filters`

**Inputs** stored.

**Declared result** list.

**Explicit results** list() · list(stored) · list of list(field, expanded value) when isinstance(value, (list bitwise or tuple)), otherwise list(field, “=”, value) for tuple(field, value) drawn from stored.items().

**Local steps**

- If not stored.
  - Return list().
- If not isinstance(stored, dict).
  - Return list(stored).
- Return list of list(field, expanded value) when isinstance(value, (list bitwise or tuple)), otherwise list(field, “=”, value) for tuple(field, value) drawn from stored.items().
  - Draw tuple(field, value) from stored.items().
  - Value choice on isinstance(value, (list bitwise or tuple)) — true gives list(field, expanded value), false gives list(field, “=”, value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L69) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L527)

<a id="op-54542ac7ef33f4"></a>
### Date payload

`operation_foundation_binding_foundation_automation_engine_scheduler_date_payload`

**Inputs** rule, today.

**Declared result** dict.

**Explicit results** mapping(“trigger\_type” → “Date Based”, “date\_field” → rule.date\_field, “occurrence\_date” → str(today)).

**Local steps**

- Return mapping(“trigger\_type” → “Date Based”, “date\_field” → rule.date\_field, “occurrence\_date” → str(today)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L61) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L519)

## Service · Schema relationships

<a id="op-17d55f377173ed"></a>
### Schema Relationship Provider.get definitions

`operation_foundation_binding_foundation_automation_engine_schema_relationships_schemarelationshipprovider_get_definitions`

**Inputs** self, source\_doctype.

**Declared result** list at dict.

**Explicit results** list(derived\_definitions(source\_doctype)).

**Local steps**

- Return list(derived\_definitions(source\_doctype)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L94) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L552)

<a id="op-90cde1455c3432"></a>
### Schema Relationship Provider.resolve

`operation_foundation_binding_foundation_automation_engine_schema_relationships_schemarelationshipprovider_resolve`

**Inputs** self, source\_doc, relationship, params.

**Declared result** list at dict.

**Explicit results** self.query(source\_doc, relationship, list(), no value) · resolver(source\_doc, definition).

**Local steps**

- Set definition from \_derived(source\_doc.doctype, relationship).
- Set resolver from FORWARD\_RESOLVERS.get(definition at “kind”).
- If not resolver.
  - Return self.query(source\_doc, relationship, list(), no value).
- Return resolver(source\_doc, definition).

**Methods declared on this owner** [query](operations-045.md#op-cad4a68a817cd1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L554)

<a id="op-cad4a68a817cd1"></a>
### Schema Relationship Provider.query

`operation_foundation_binding_foundation_automation_engine_schema_relationships_schemarelationshipprovider_query`

**Inputs** self, source\_doc, relationship, filters, limit.

**Declared result** list at dict.

**Record and data access** read target via get\_list.

**Explicit results** super().query(source\_doc, relationship, filters, limit) · list() · list of mapping(“doctype” → target, “name” → name) for name drawn from names.

**Local steps**

- Set definition from \_derived(source\_doc.doctype, relationship).
- If definition at “kind” does not belong to REVERSE\_KINDS.
  - Return super().query(source\_doc, relationship, filters, limit).
- Set target from definition at “target\_doctype”.
- Set own from \_reverse\_filters(definition, source\_doc).
- If own is identical to no value.
  - Return list().
- Set names from Platform.get\_list(target, filters = list(expanded own, expanded (filters or list())), pluck = “name”, limit = limit).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- Return list of mapping(“doctype” → target, “name” → name) for name drawn from names.
  - Draw name from names.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L95) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L553)

<a id="op-5c39eb4789b0ae"></a>
### Resolve link

`operation_foundation_binding_foundation_automation_engine_schema_relationships_resolve_link`

**Inputs** doc, definition.

**Declared result** list at dict.

**Explicit results** \_references(definition at “target\_doctype”, list(doc.get(definition at “fieldname”))).

**Local steps**

- Return \_references(definition at “target\_doctype”, list(doc.get(definition at “fieldname”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L92) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L550)

<a id="op-717a612ee6aca9"></a>
### Resolve child link

`operation_foundation_binding_foundation_automation_engine_schema_relationships_resolve_child_link`

**Inputs** doc, definition.

**Declared result** list at dict.

**Explicit results** \_references(definition at “target\_doctype”, list of row.get(definition at “fieldname”) for row drawn from rows).

**Local steps**

- Set rows from (doc.get(definition at “table\_fieldname”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(definition at “table\_fieldname”) → list().
- Return \_references(definition at “target\_doctype”, list of row.get(definition at “fieldname”) for row drawn from rows).
  - Draw row from rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L90) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L548)

<a id="op-a42b156faa5aa3"></a>
### Resolve dynamic link

`operation_foundation_binding_foundation_automation_engine_schema_relationships_resolve_dynamic_link`

**Inputs** doc, definition.

**Declared result** list at dict.

**Explicit results** list() · \_references(target, list(doc.get(definition at “fieldname”))).

**Local steps**

- Set target from doc.get(definition at “doctype\_fieldname”).
- If target belongs to \_ignored().
  - Return list().
- Return \_references(target, list(doc.get(definition at “fieldname”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L91) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L549)

<a id="op-d1ef15c0ddba9a"></a>
### Reverse filters

`operation_foundation_binding_foundation_automation_engine_schema_relationships_reverse_filters`

**Inputs** definition, source\_doc.

**Declared result** (list bitwise or no value).

**Explicit results** list(list(definition at “fieldname”, “=”, source\_doc.name)) · list(list(“name”, “in”, parents)) when parents, otherwise no value.

**Local steps**

- If definition at “kind” differs from “reverse\_child\_link”.
  - Return list(list(definition at “fieldname”, “=”, source\_doc.name)).
- Set parents from \_child\_parents(definition, source\_doc).
- Return list(list(“name”, “in”, parents)) when parents, otherwise no value.
  - Value choice on parents — true gives list(list(“name”, “in”, parents)), false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L93) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L551)

<a id="op-6bcec8ef7ba7fb"></a>
### Child parents

`operation_foundation_binding_foundation_automation_engine_schema_relationships_child_parents`

**Inputs** definition, source\_doc.

**Declared result** list at str.

**Record and data access** read definition at “child\_doctype” via get\_all.

**Explicit results** Platform.get\_all(definition at “child\_doctype”, filters = mapping(definition at “fieldname” → source\_doc.name, “parenttype” → definition at “target\_doctype”), pluck = “parent”, distinct = true).

**Local steps**

- Return Platform.get\_all(definition at “child\_doctype”, filters = mapping(definition at “fieldname” → source\_doc.name, “parenttype” → definition at “target\_doctype”), pluck = “parent”, distinct = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L79) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L537)

<a id="op-e4a810a18cfefb"></a>
### Derived definitions

`operation_foundation_binding_foundation_automation_engine_schema_relationships_derived_definitions`

**Inputs** source\_doctype.

**Wrappers, in declaration order** request\_cache.

**Declared result** list at dict.

**Explicit results** list() · \_deduplicate(definitions).

**Local steps**

- If (not source\_doctype or source\_doctype belongs to \_ignored()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not source\_doctype → source\_doctype belongs to \_ignored().
  - Return list().
- Set definitions from list(expanded \_forward\_links(source\_doctype), expanded \_forward\_dynamic\_links(source\_doctype), expanded \_child\_links(source\_doctype), expanded \_incoming(source\_doctype)).
- Return \_deduplicate(definitions).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L82) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L540)

<a id="op-c0bc266858c138"></a>
### Forward links

`operation_foundation_binding_foundation_automation_engine_schema_relationships_forward_links`

**Inputs** source\_doctype.

**Declared result** list at dict.

**Local steps**

- For each field in Platform.get\_meta(source\_doctype).get\_link\_fields().
  - If field.options belongs to \_ignored().
    - Continue with the next iteration or loop test.
  - yield mapping(“name” → field.fieldname, “label” → translated (field.label or field.fieldname), “cardinality” → “one”, “target\_doctype” → field.options, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.label → field.fieldname.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L84) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L542)

<a id="op-a3dd7ac5dfd2a9"></a>
### Forward dynamic links

`operation_foundation_binding_foundation_automation_engine_schema_relationships_forward_dynamic_links`

**Inputs** source\_doctype.

**Declared result** list at dict.

**Local steps**

- For each field in Platform.get\_meta(source\_doctype).get\_dynamic\_link\_fields().
  - yield mapping(“name” → field.fieldname, “label” → translated (field.label or field.fieldname), “cardinality” → “one”, “target\_doctype” → no value, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.label → field.fieldname.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L83) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L541)

<a id="op-437a30ce4845a0"></a>
### Child links

`operation_foundation_binding_foundation_automation_engine_schema_relationships_child_links`

**Inputs** source\_doctype.

**Declared result** list at dict.

**Local steps**

- For each table in Platform.get\_meta(source\_doctype).get\_table\_fields().
  - For each field in Platform.get\_meta(table.options).get\_link\_fields().
    - If field.options belongs to \_ignored().
      - Continue with the next iteration or loop test.
    - yield mapping(“name” → formatted text {table.fieldname}\_{field.fieldname}, “label” → translated “{0} ({1})”.format(translated (field.label or field.fieldname), translated (table.label or table.fieldname)), “card ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.label → field.fieldname.
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in table.label → table.fieldname.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L78) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L536)

<a id="op-bee990d53399c4"></a>
### Incoming

`operation_foundation_binding_foundation_automation_engine_schema_relationships_incoming`

**Inputs** source\_doctype.

**Declared result** list at dict.

**Local steps**

- Bind dependencies get\_linked\_fields.
- For each tuple(doctype, link) in (get\_linked\_fields(source\_doctype) or mapping()).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_linked\_fields(source\_doctype) → mapping().
  - If not \_is\_queryable(doctype).
    - Continue with the next iteration or loop test.
  - For each fieldname in (link.get(“fieldname”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in link.get(“fieldname”) → list().
    - yield \_incoming\_definition(doctype, fieldname, link.get(“child\_doctype”)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L86) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L544)

<a id="op-e7aa271bb34278"></a>
### Incoming definition

`operation_foundation_binding_foundation_automation_engine_schema_relationships_incoming_definition`

**Inputs** doctype, fieldname, child\_doctype.

**Declared result** dict.

**Explicit results** mapping(“name” → formatted text {Platform.scrub(doctype)}\_via\_{fieldname}, “label” → translated “{0} (by {1})”.format(translated doctype, fieldname), “cardinality” → “many”, “target\_doctype” → doctype, …).

**Local steps**

- Return mapping(“name” → formatted text {Platform.scrub(doctype)}\_via\_{fieldname}, “label” → translated “{0} (by {1})”.format(translated doctype, fieldname), “cardinality” → “many”, “target\_doctype” → doctype, …).
  - Value choice on child\_doctype — true gives “reverse\_child\_link”, false gives “reverse\_link”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L87) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L545)

<a id="op-bf9c942331e190"></a>
### Is queryable

`operation_foundation_binding_foundation_automation_engine_schema_relationships_is_queryable`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** false · not (meta.istable or meta.issingle or meta.is\_virtual).

**Local steps**

- If doctype belongs to \_ignored().
  - Return false.
- Set meta from Platform.get\_meta(doctype).
- Return not (meta.istable or meta.issingle or meta.is\_virtual).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.istable → meta.issingle → meta.is\_virtual.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L88) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L546)
