# Relationship automation · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Relationships

<a id="op-0696440d9b3e12"></a>
### CRMRelationship Provider.query

`operation_relationships_binding_crm_automation_relationships_crmrelationshipprovider_query`

**Inputs** self, source\_doc, relationship, filters, limit.

**Declared result** list at dict.

**Record and data access** read doctype via get\_list.

**Explicit results** super().query(source\_doc, relationship, filters, limit) · list of mapping(“doctype” → doctype, “name” → name) for name drawn from names.

**Local steps**

- Set definition from \_definition(source\_doc.doctype, relationship).
- Set linked from definition.get(“linked”).
- If not linked.
  - Return super().query(source\_doc, relationship, filters, limit).
- Set tuple(doctype, link\_filters) from linked(source\_doc).
- Set names from Platform.get\_list(doctype, filters = list(expanded link\_filters, expanded filters), pluck = “name”, limit = limit).
- Return list of mapping(“doctype” → doctype, “name” → name) for name drawn from names.
  - Draw name from names.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L141) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L297) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L278)

<a id="op-b3e815e2800c02"></a>
### Definition

`operation_relationships_binding_crm_automation_relationships_definition`

**Inputs** source\_doctype, relationship.

**Declared result** dict.

**Explicit results** definition.

**Explicit failure paths** validation helper — Platform.\_(“Unknown CRM relationship: {0}”).format(relationship).

**Local steps**

- For each definition in DEFINITIONS.get(source\_doctype, list()).
  - If definition at “name” equals relationship.
    - Return definition.
- Call the validation error handler Platform.throw(Platform.\_(“Unknown CRM relationship: {0}”).format(relationship)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L143) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L299) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L280)

<a id="op-410485df6cadd4"></a>
### Public

`operation_relationships_binding_crm_automation_relationships_public`

**Inputs** definition.

**Declared result** dict.

**Explicit results** mapping of key → value for tuple(key, value) drawn from definition.items() where key does not belong to tuple(“resolve”, “linked”).

**Local steps**

- Return mapping of key → value for tuple(key, value) drawn from definition.items() where key does not belong to tuple(“resolve”, “linked”).
  - Draw tuple(key, value) from definition.items(), keep a combination only if (key does not belong to tuple(“resolve”, “linked”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L147) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L303) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L284)

<a id="op-143ef2d52b74e6"></a>
### References

`operation_relationships_binding_crm_automation_relationships_references`

**Inputs** doctype, names.

**Declared result** list at dict.

**Explicit results** list of mapping(“doctype” → doctype, “name” → name) for name drawn from names where name.

**Local steps**

- Return list of mapping(“doctype” → doctype, “name” → name) for name drawn from names where name.
  - Draw name from names, keep a combination only if (name).

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L148) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L304) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L285)

<a id="op-af3714c8c58c63"></a>
### Communication filters

`operation_relationships_binding_crm_automation_relationships_communication_filters`

**Inputs** doc.

**Explicit results** list(list(“reference\_doctype”, “=”, doc.doctype), list(“reference\_name”, “=”, doc.name)).

**Local steps**

- Return list(list(“reference\_doctype”, “=”, doc.doctype), list(“reference\_name”, “=”, doc.name)).

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L137) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L293) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L274)

<a id="op-dc683431d379e7"></a>
### Task filters

`operation_relationships_binding_crm_automation_relationships_task_filters`

**Inputs** doc.

**Explicit results** list(list(“reference\_doctype”, “=”, doc.doctype), list(“reference\_docname”, “=”, doc.name)).

**Local steps**

- Return list(list(“reference\_doctype”, “=”, doc.doctype), list(“reference\_docname”, “=”, doc.name)).

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L150) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L306) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L287)

<a id="op-1873874d71be78"></a>
### Dynamic reference

`operation_relationships_binding_crm_automation_relationships_dynamic_reference`

**Inputs** name, label, doctype, filters.

**Declared result** dict.

**Explicit results** mapping(“name” → name, “label” → label, “cardinality” → “many”, “target\_doctype” → doctype, …).

**Local steps**

- Return mapping(“name” → name, “label” → label, “cardinality” → “many”, “target\_doctype” → doctype, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L144) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L300) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L281)

<a id="op-91e17affaaf706"></a>
### Communications

`operation_relationships_binding_crm_automation_relationships_communications`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** \_dynamic\_reference(“communications”, “Communications”, “Communication”, \_communication\_filters).

**Local steps**

- Return \_dynamic\_reference(“communications”, “Communications”, “Communication”, \_communication\_filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L139) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L295) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L276)

<a id="op-29979bb61d1d7a"></a>
### Tasks

`operation_relationships_binding_crm_automation_relationships_tasks`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** \_dynamic\_reference(“tasks”, “Tasks”, “CRM Task”, \_task\_filters).

**Local steps**

- Return \_dynamic\_reference(“tasks”, “Tasks”, “CRM Task”, \_task\_filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L151) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L307) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L288)

<a id="op-5a863068632b48"></a>
### Communication reference

`operation_relationships_binding_crm_automation_relationships_communication_reference`

**Inputs** doc.

**Declared result** list at dict.

**Explicit results** list() · \_references(doc.reference\_doctype, list(doc.reference\_name)).

**Local steps**

- If doc.reference\_doctype does not belong to COMMUNICATION\_REFERENCE\_DOCTYPES.
  - Return list().
- Return \_references(doc.reference\_doctype, list(doc.reference\_name)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L138) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L294) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L275)

<a id="op-a254b9e0613066"></a>
### Lead organization

`operation_relationships_binding_crm_automation_relationships_lead_organization`

**Inputs** lead.

**Declared result** list at dict.

**Record and data access** read “CRM Organization” via exists.

**Explicit results** \_references(“CRM Organization”, list(name)).

**Local steps**

- Set name from (lead.organization and Platform.db.exists(“CRM Organization”, mapping(“organization\_name” → lead.organization))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in lead.organization → Platform.db.exists(“CRM Organization”, mapping(“organization\_name” → lead.organization)).
- Return \_references(“CRM Organization”, list(name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L146) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L302) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L283)

<a id="op-389e6ff616eef9"></a>
### Lead contacts

`operation_relationships_binding_crm_automation_relationships_lead_contacts`

**Inputs** lead.

**Declared result** list at dict.

**Record and data access** read “Dynamic Link” via get\_all · read “Contact Email” via get\_all.

**Explicit results** \_references(“Contact”, sorted(set(names))).

**Local steps**

- Set names from Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → “Contact”, “link\_doctype” → “CRM Lead”, “link\_name” → lead.name), pluck = “parent”).
- If lead.email.
  - Update names using + Platform.get\_all(“Contact Email”, filters = mapping(“email\_id” → lead.email), pluck = “parent”).
- Return \_references(“Contact”, sorted(set(names))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L145) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L301) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L282)

<a id="op-73c5cb183e5354"></a>
### Rename

`operation_relationships_binding_crm_automation_relationships_rename`

**Inputs** name, derived\_from, label.

**Declared result** dict.

**Explicit results** mapping(“name” → name, “derived\_from” → derived\_from, “label” → label).

**Local steps**

- Return mapping(“name” → name, “derived\_from” → derived\_from, “label” → label).

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L149) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L305) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L286)

## Service · Scoring

<a id="op-31471eb6458106"></a>
### Adjust lead score

`operation_relationships_binding_crm_automation_scoring_adjust_lead_score`

**Inputs** lead, amount, reason = no value, min\_score = no value, max\_score = no value.

**Declared result** dict.

**State and service calls** call db\_set on lead.

**Explicit results** mapping(“detail” → translated “Lead score {0} → {1}{2}”.format(old\_value, new\_value, formatted text  ({reason}) when reason, otherwise empty text), “old\_value” → old\_value, “new\_value” → new\_value, “delta” ….

**Local steps**

- Evaluate lead.check\_permission(“write”).
- Evaluate \_lock(lead).
- Evaluate lead.reload().
- Set old\_value from cint(lead.get(SCORE\_FIELD)).
- Set new\_value from \_clamp((old\_value + cint(amount)), min\_score, max\_score).
- If new\_value differs from old\_value.
  - Evaluate lead.db\_set(SCORE\_FIELD, new\_value, update\_modified = false).
- Return mapping(“detail” → translated “Lead score {0} → {1}{2}”.format(old\_value, new\_value, formatted text  ({reason}) when reason, otherwise empty text), “old\_value” → old\_value, “new\_value” → new\_value, “delta” ….
  - Value choice on reason — true gives formatted text  ({reason}), false gives empty text.

**Values supplied outside this operation** effective access from lead.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L152) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L308) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L289)

<a id="op-0523ac576f53cc"></a>
### Set lead temperature

`operation_relationships_binding_crm_automation_scoring_set_lead_temperature`

**Inputs** lead, value.

**Declared result** dict.

**State and service calls** call db\_set on lead.

**Explicit results** mapping(“detail” → translated “Lead is now {0}”.format(value), “old\_value” → old\_value, “new\_value” → value).

**Explicit failure paths** validation helper — translated “Lead temperature must be one of {0}”.format(“, ”.join(options)).

**Local steps**

- Evaluate lead.check\_permission(“write”).
- Set options from temperature\_options().
- If value does not belong to options.
  - Call the validation error handler Platform.throw(translated “Lead temperature must be one of {0}”.format(“, ”.join(options))).
- Set old\_value from lead.get(TEMPERATURE\_FIELD).
- If value differs from old\_value.
  - Evaluate lead.db\_set(TEMPERATURE\_FIELD, value, update\_modified = false).
- Return mapping(“detail” → translated “Lead is now {0}”.format(value), “old\_value” → old\_value, “new\_value” → value).

**Values supplied outside this operation** effective access from lead.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L155) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L311) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L292)

<a id="op-f48b5ea6909b6f"></a>
### Temperature options

`operation_relationships_binding_crm_automation_scoring_temperature_options`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** list of option for option drawn from (field.options or empty text).split(whitespace '\\n') where option.

**Local steps**

- Set field from Platform.get\_meta(“CRM Lead”).get\_field(TEMPERATURE\_FIELD).
- Return list of option for option drawn from (field.options or empty text).split(whitespace '\\n') where option.
  - Draw option from (field.options or empty text).split(whitespace '\\n'), keep a combination only if (option).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in field.options → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L156) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L312) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L293)

<a id="op-7170c7b05f795c"></a>
### Clamp

`operation_relationships_binding_crm_automation_scoring_clamp`

**Inputs** value, min\_score, max\_score.

**Declared result** int.

**Explicit results** value.

**Local steps**

- If min\_score does not belong to tuple(no value, empty text).
  - Set value from max(value, cint(min\_score)).
- If max\_score does not belong to tuple(no value, empty text).
  - Set value from min(value, cint(max\_score)).
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L153) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L309) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L290)

<a id="op-8da62e53e49a3e"></a>
### Lock

`operation_relationships_binding_crm_automation_scoring_lock`

**Inputs** lead.

**Local steps**

- Set table from Platform.qb.DocType(lead.doctype).
- Evaluate nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name equals nested operand in the contract.name).for\_update().run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L154) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L310) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L291)
