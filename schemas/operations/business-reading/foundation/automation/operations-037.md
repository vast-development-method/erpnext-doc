# Workflow, automation and dispatch · operations 37

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Relationships

<a id="op-7344495a31008f"></a>
### Get relationship definitions

`operation_foundation_binding_foundation_automation_engine_relationships_get_relationship_definitions`

**Inputs** source\_doctype.

**Declared result** list at dict.

**Explicit results** list of \_public(definition) for definition drawn from \_definitions(source\_doctype).

**Local steps**

- Return list of \_public(definition) for definition drawn from \_definitions(source\_doctype).
  - Draw definition from \_definitions(source\_doctype).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L227) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L443)

<a id="op-5a34f2a1cd3e1d"></a>
### Get relationship definition

`operation_foundation_binding_foundation_automation_engine_relationships_get_relationship_definition`

**Inputs** source\_doctype, relationship.

**Declared result** dict.

**Explicit results** \_public(\_definition(source\_doctype, relationship)).

**Local steps**

- Return \_public(\_definition(source\_doctype, relationship)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L226) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L442)

<a id="op-c688b6464beab4"></a>
### Get relationship targets

`operation_foundation_binding_foundation_automation_engine_relationships_get_relationship_targets`

**Inputs** source\_doctype, relationships.

**Declared result** dict at tuple(str, (str bitwise or no value)).

**Explicit results** targets.

**Explicit failure paths** validation helper — translated “Relationship {0} cannot be used as a single record alias”.format(item at “relationship”).

**Local steps**

- Set targets from mapping(“trigger” → source\_doctype).
- For each item in \_parse\_relationships(relationships).
  - Evaluate \_validate\_alias(item, targets).
  - Set definition from \_definition(targets at (item.get(“source”) or “trigger”), item at “relationship”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“source”) → “trigger”.
  - If definition at “cardinality” differs from “one”.
    - Call the validation error handler Platform.throw(translated “Relationship {0} cannot be used as a single record alias”.format(item at “relationship”)).
  - Set targets at item at “alias” from \_configured\_target(definition, item).
- Return targets.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L228) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L444)

<a id="op-3061b0a190e9d4"></a>
### Resolve relationships

`operation_foundation_binding_foundation_automation_engine_relationships_resolve_relationships`

**Inputs** trigger\_doc, relationships.

**Declared result** dict at tuple(str, dict).

**Explicit results** records.

**Local steps**

- Set records from mapping(“trigger” → \_reference(trigger\_doc)) when trigger\_doc, otherwise mapping().
  - Value choice on trigger\_doc — true gives mapping(“trigger” → \_reference(trigger\_doc)), false gives mapping().
- For each item in \_parse\_relationships(relationships).
  - Set source from load\_record(records.get((item.get(“source”) or “trigger”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“source”) → “trigger”.
  - Set records at item at “alias” from resolve\_one(source, item at “relationship”, item.get(“params”)).
- Return records.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L240) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L456)

<a id="op-f018a4209873d2"></a>
### Resolve one

`operation_foundation_binding_foundation_automation_engine_relationships_resolve_one`

**Inputs** source\_doc, relationship, params = no value.

**Declared result** dict.

**Explicit results** \_permitted\_reference(resolved at 0, definition).

**Explicit failure paths** validation helper — translated “Relationship {0} returns multiple records”.format(relationship) · validation helper — translated “Relationship {0} did not resolve to one record”.format(relationship).

**Local steps**

- Set definition from \_definition(source\_doc.doctype, relationship).
- If definition at “cardinality” differs from “one”.
  - Call the validation error handler Platform.throw(translated “Relationship {0} returns multiple records”.format(relationship)).
- Set name from \_provider\_name(definition, relationship).
- Set resolved from (definition at “provider”.resolve(source\_doc, name, (params or mapping())) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in definition at “provider”.resolve(source\_doc, name, (params or mapping())) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params → mapping().
- If len(resolved) differs from 1.
  - Call the validation error handler Platform.throw(translated “Relationship {0} did not resolve to one record”.format(relationship)).
- Return \_permitted\_reference(resolved at 0, definition).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L239) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L479) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L455)

<a id="op-6e5da1da5906d2"></a>
### Query related

`operation_foundation_binding_foundation_automation_engine_relationships_query_related`

**Inputs** source\_doc, relationship, filters = no value, limit = MAX\_RELATED\_ROWS.

**Declared result** list at dict.

**Explicit results** list of \_permitted\_reference(row, definition) for row drawn from (rows or list()).

**Local steps**

- Set definition from \_definition(source\_doc.doctype, relationship).
- Set limit from min((cint(limit) or MAX\_RELATED\_ROWS), MAX\_RELATED\_ROWS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(limit) → MAX\_RELATED\_ROWS.
- Set name from \_provider\_name(definition, relationship).
- Set rows from definition at “provider”.query(source\_doc, name, (filters or list()), limit).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- Return list of \_permitted\_reference(row, definition) for row drawn from (rows or list()).
  - Draw row from (rows or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L235) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L451)

<a id="op-4e7b7ed49b0afb"></a>
### Load record

`operation_foundation_binding_foundation_automation_engine_relationships_load_record`

**Inputs** reference, permission\_type = no value.

**Record and data access** resolve a document from reference at “doctype” via get\_doc.

**Explicit results** doc.

**Explicit failure paths** validation helper — translated “Record alias could not be resolved”.

**Local steps**

- If not reference.
  - Call the validation error handler Platform.throw(translated “Record alias could not be resolved”).
- Set doc from Platform.get\_doc(reference at “doctype”, reference at “name”).
- If permission\_type.
  - Evaluate doc.check\_permission(permission\_type).
- Return doc.

**Values supplied outside this operation** effective access from doc.check\_permission(permission\_type).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L229) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L445)

<a id="op-f532bb281d7f31"></a>
### Providers

`operation_foundation_binding_foundation_automation_engine_relationships_providers`

**Inputs** no declared parameters.

**Wrappers, in declaration order** request\_cache.

**Declared result** list.

**Explicit results** providers.

**Local steps**

- Bind dependencies SchemaRelationshipProvider.
- Set providers from list().
- For each path in Platform.get\_hooks(“automation\_relationships”).
  - Set provider from Platform.get\_attr(path).
  - Evaluate providers.append(provider() when isinstance(provider, type), otherwise provider).
    - Value choice on isinstance(provider, type) — true gives provider(), false gives provider.
- Evaluate providers.append(SchemaRelationshipProvider()).
- Return providers.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“automation\_relationships”), Platform.get\_attr(path).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L233) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L449)

<a id="op-40cefb85ddbe00"></a>
### Definitions

`operation_foundation_binding_foundation_automation_engine_relationships_definitions`

**Inputs** source\_doctype.

**Declared result** list at dict.

**Explicit results** list() · list(definitions.values()).

**Local steps**

- If not source\_doctype.
  - Return list().
- Set definitions from mapping().
- For each provider in \_providers().
  - For each item in (provider.get\_definitions(source\_doctype) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in provider.get\_definitions(source\_doctype) → list().
    - Set definition from \_validated\_definition(provider, source\_doctype, item).
    - Evaluate \_claim\_name(definitions, definition, source\_doctype).
- Return list(definitions.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L225) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L441)

<a id="op-e8923056dba43c"></a>
### Claim name

`operation_foundation_binding_foundation_automation_engine_relationships_claim_name`

**Inputs** definitions, definition, source\_doctype.

**Explicit failure paths** validation helper — translated “Duplicate automation relationship name on {0}”.format(source\_doctype).

**Local steps**

- Set held from definitions.get(definition at “name”).
- If (held and not definition.get(“derived”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in held → not definition.get(“derived”).
  - Call the validation error handler Platform.throw(translated “Duplicate automation relationship name on {0}”.format(source\_doctype)).
- If not held.
  - Set definitions at definition at “name” from definition.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L222) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L438)

<a id="op-0bd88f21332a4c"></a>
### Definition

`operation_foundation_binding_foundation_automation_engine_relationships_definition`

**Inputs** source\_doctype, relationship.

**Declared result** dict.

**Explicit results** definition.

**Explicit failure paths** validation helper — translated “Unknown automation relationship: {0}”.format(relationship).

**Local steps**

- For each definition in \_definitions(source\_doctype).
  - If definition at “name” equals relationship.
    - Return definition.
- Call the validation error handler Platform.throw(translated “Unknown automation relationship: {0}”.format(relationship)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L224) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L440)

<a id="op-3b473aedb305d6"></a>
### Validated definition

`operation_foundation_binding_foundation_automation_engine_relationships_validated_definition`

**Inputs** provider, source\_doctype, definition.

**Declared result** dict.

**Explicit results** definition.

**Explicit failure paths** validation helper — translated “Invalid automation relationship definition” · validation helper — translated “Relationship source DocType does not match”.

**Local steps**

- Set definition from \_renamed(dict(definition), source\_doctype).
- If (not definition.get(“name”) or definition.get(“cardinality”) does not belong to tuple(“one”, “many”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not definition.get(“name”) → definition.get(“cardinality”) does not belong to tuple(“one”, “many”).
  - Call the validation error handler Platform.throw(translated “Invalid automation relationship definition”).
- If definition.get(“source\_doctype”) does not belong to tuple(no value, source\_doctype).
  - Call the validation error handler Platform.throw(translated “Relationship source DocType does not match”).
- Set definition at “source\_doctype” from source\_doctype.
- Evaluate definition.setdefault(“provider”, provider).
- Return definition.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L243) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L459)

<a id="op-ebabab7a539163"></a>
### Renamed

`operation_foundation_binding_foundation_automation_engine_relationships_renamed`

**Inputs** definition, source\_doctype.

**Declared result** dict.

**Explicit results** definition · mapping(expand derived, expand definition).

**Local steps**

- Set source from definition.pop(“derived\_from”, no value).
- If not source.
  - Return definition.
- Set definition at “derived\_name” from source.
- Bind dependencies SchemaRelationshipProvider.
- Set derived from dict(\_schema\_definition(source\_doctype, source)).
- Set derived at “provider” from SchemaRelationshipProvider().
- Evaluate derived.pop(“derived”, no value).
- Return mapping(expand derived, expand definition).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L238) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L454)

<a id="op-155d56dae261c6"></a>
### Schema definition

`operation_foundation_binding_foundation_automation_engine_relationships_schema_definition`

**Inputs** source\_doctype, relationship.

**Declared result** dict.

**Explicit results** definition.

**Explicit failure paths** validation helper — translated “Unknown derived relationship: {0} on {1}”.format(relationship, source\_doctype).

**Local steps**

- Bind dependencies derived\_definitions.
- For each definition in derived\_definitions(source\_doctype).
  - If definition at “name” equals relationship.
    - Return definition.
- Call the validation error handler Platform.throw(translated “Unknown derived relationship: {0} on {1}”.format(relationship, source\_doctype)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L241) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L481) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L457)

<a id="op-07852c51af7103"></a>
### Public

`operation_foundation_binding_foundation_automation_engine_relationships_public`

**Inputs** definition.

**Declared result** dict.

**Explicit results** mapping of key → value for tuple(key, value) drawn from definition.items() where key does not belong to INTERNAL\_KEYS.

**Local steps**

- Return mapping of key → value for tuple(key, value) drawn from definition.items() where key does not belong to INTERNAL\_KEYS.
  - Draw tuple(key, value) from definition.items(), keep a combination only if (key does not belong to INTERNAL\_KEYS).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L234) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L450)

<a id="op-e48bd84d5d7d21"></a>
### Allowed doctypes

`operation_foundation_binding_foundation_automation_engine_relationships_allowed_doctypes`

**Inputs** definition.

**Declared result** list.

**Explicit results** (definition.get(“target\_doctypes”) or list(definition at “target\_doctype”)).

**Local steps**

- Return (definition.get(“target\_doctypes”) or list(definition at “target\_doctype”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in definition.get(“target\_doctypes”) → list(definition at “target\_doctype”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L218) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L434)

<a id="op-295a0d0cce009b"></a>
### Configured target

`operation_foundation_binding_foundation_automation_engine_relationships_configured_target`

**Inputs** definition, item.

**Declared result** (str bitwise or no value).

**Explicit results** target.

**Explicit failure paths** validation helper — translated “Relationship target DocType is not allowed”.

**Local steps**

- Set target from (item.get(“target\_doctype”) or definition.get(“target\_doctype”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“target\_doctype”) → definition.get(“target\_doctype”).
- Set allowed from definition.get(“target\_doctypes”).
- If (target and allowed and target does not belong to allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target → allowed → target does not belong to allowed.
  - Call the validation error handler Platform.throw(translated “Relationship target DocType is not allowed”).
- Return target.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L223) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L439)

<a id="op-543a053e18ffd9"></a>
### Parse relationships

`operation_foundation_binding_foundation_automation_engine_relationships_parse_relationships`

**Inputs** relationships.

**Declared result** list at dict.

**Explicit results** list() · list of dict(item) for item drawn from parsed.

**Explicit failure paths** validation helper — translated “Relationships must be a JSON list”.

**Local steps**

- If not relationships.
  - Return list().
- Set parsed from Platform.parse\_json(relationships) when isinstance(relationships, str), otherwise relationships.
  - Value choice on isinstance(relationships, str) — true gives Platform.parse\_json(relationships), false gives relationships.
- If not isinstance(parsed, list).
  - Call the validation error handler Platform.throw(translated “Relationships must be a JSON list”).
- Return list of dict(item) for item drawn from parsed.
  - Draw item from parsed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L230) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L446)

<a id="op-529277c63b6cd3"></a>
### Validate alias

`operation_foundation_binding_foundation_automation_engine_relationships_validate_alias`

**Inputs** item, aliases.

**Explicit failure paths** validation helper — translated “Each relationship needs an alias and relationship name” · validation helper — translated “Duplicate record alias: {0}”.format(item at “alias”) · validation helper — translated “Unknown relationship source alias: {0}”.format(item.get(“source”)).

**Local steps**

- If (not item.get(“alias”) or not item.get(“relationship”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.get(“alias”) → not item.get(“relationship”).
  - Call the validation error handler Platform.throw(translated “Each relationship needs an alias and relationship name”).
- If item at “alias” belongs to aliases.
  - Call the validation error handler Platform.throw(translated “Duplicate record alias: {0}”.format(item at “alias”)).
- If (item.get(“source”) or “trigger”) does not belong to aliases.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“source”) → “trigger”.
  - Call the validation error handler Platform.throw(translated “Unknown relationship source alias: {0}”.format(item.get(“source”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L242) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L458)

<a id="op-640e47d62208ad"></a>
### Provider name

`operation_foundation_binding_foundation_automation_engine_relationships_provider_name`

**Inputs** definition, relationship.

**Declared result** str.

**Explicit results** (definition.get(“derived\_name”) or relationship).

**Local steps**

- Return (definition.get(“derived\_name”) or relationship).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in definition.get(“derived\_name”) → relationship.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L232) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L448)

<a id="op-37fc6caa882e02"></a>
### Reference

`operation_foundation_binding_foundation_automation_engine_relationships_reference`

**Inputs** doc.

**Declared result** dict.

**Explicit results** mapping(“doctype” → doc.doctype, “name” → doc.name).

**Local steps**

- Return mapping(“doctype” → doc.doctype, “name” → doc.name).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L237) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L453)

<a id="op-1fe676bf2a4891"></a>
### Permitted reference

`operation_foundation_binding_foundation_automation_engine_relationships_permitted_reference`

**Inputs** value, definition.

**Declared result** dict.

**Record and data access** read doctype via exists.

**Explicit results** mapping(“doctype” → doctype, “name” → name).

**Explicit failure paths** validation helper — translated “Relationship provider returned an invalid record reference” · validation helper — translated “Related record does not exist: {0} {1}”.format(doctype, name).

**Local steps**

- Set tuple(doctype, name) from tuple(value.get(“doctype”), value.get(“name”)).
- Set allowed from \_allowed\_doctypes(definition).
- If (not (doctype and name) or (any(allowed) and doctype does not belong to allowed)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not (doctype and name) → (any(allowed) and doctype does not belong to allowed).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in any(allowed) → doctype does not belong to allowed.
  - Call the validation error handler Platform.throw(translated “Relationship provider returned an invalid record reference”).
- If not Platform.db.exists(doctype, name).
  - Call the validation error handler Platform.throw(translated “Related record does not exist: {0} {1}”.format(doctype, name)).
- Evaluate Platform.has\_permission(doctype, “read”, doc = name, throw = true).
- Return mapping(“doctype” → doctype, “name” → name).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, doc = name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L231) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L447)

<a id="op-7cb09da91f5e44"></a>
### Query resolved

`operation_foundation_binding_foundation_automation_engine_relationships_query_resolved`

**Inputs** provider, source\_doc, relationship, filters, limit.

**Record and data access** read target\_doctype via get\_list.

**Explicit results** list() · list of mapping(“doctype” → target\_doctype, “name” → name) for name drawn from names.

**Explicit failure paths** validation helper — translated “Filtered relationship queries require one target DocType”.

**Local steps**

- Set references from (provider.resolve(source\_doc, relationship, mapping()) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in provider.resolve(source\_doc, relationship, mapping()) → list().
- If not references.
  - Return list().
- Set doctypes from set of item at “doctype” for item drawn from references.
  - Draw item from references.
- If len(doctypes) differs from 1.
  - Call the validation error handler Platform.throw(translated “Filtered relationship queries require one target DocType”).
- Set target\_doctype from doctypes.pop().
- Set names from Platform.get\_list(target\_doctype, filters = list(list(“name”, “in”, list of item at “name” for item drawn from references), expanded filters), pluck = “name”, limit = limit).
  - Draw item from references.
- Return list of mapping(“doctype” → target\_doctype, “name” → name) for name drawn from names.
  - Draw name from names.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L236) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L452)

## Record · Reminder

[Record definition](../../../../data/record-types/reminder.json)

<a id="op-c38234d16b6cb8"></a>
### Reminder.clear old logs

`operation_foundation_automation_record_definitions_reminder_business_behavior_reminder_clear_old_logs`

**Inputs** days = 30.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“Reminder”).
- Evaluate Platform.db.delete(table, filters = table.remind\_at &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0016.json#L2854) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L255)
