# Company enrichment · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Api

<a id="op-fe63b01763b026"></a>
### Enabled doctypes

`operation_relationships_domain_enrichment_application_interface_business_behavior_enabled_record_types`

**Inputs** cfg.

**Declared result** list at str.

**Explicit results** list() · list(ENRICHABLE\_DOCTYPES).

**Local steps**

- If not cfg.setting(“enabled”).
  - Return list().
- Return list(ENRICHABLE\_DOCTYPES).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L3799) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L418) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L399)

<a id="op-9f9311652f1d39"></a>
### Check writable

`operation_relationships_binding_crm_domain_enrichment_api_check_writable`

**Inputs** cfg, reference\_doctype, reference\_name.

**Record and data access** resolve a document from reference\_doctype via get\_doc.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Enrichment is not enabled for {0}.”.format(reference\_doctype).

**Local steps**

- If reference\_doctype does not belong to \_enabled\_doctypes(cfg).
  - Call the validation error handler Platform.throw(translated “Enrichment is not enabled for {0}.”.format(reference\_doctype), Platform.ValidationError).
- Set doc from Platform.get\_doc(reference\_doctype, reference\_name).
- Evaluate doc.check\_permission(“write”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L157) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L313) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L294)

<a id="op-63c162a823c559"></a>
### Completed runs

`operation_relationships_binding_crm_domain_enrichment_api_completed_runs`

**Inputs** reference\_doctype, reference\_name.

**Declared result** list at str.

**Record and data access** read “CRM Enrichment Run” via get\_all.

**Explicit results** Platform.get\_all(“CRM Enrichment Run”, filters = mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “status” → “Completed”), pluck = “name”, order\_by = “creation desc”).

**Local steps**

- Return Platform.get\_all(“CRM Enrichment Run”, filters = mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “status” → “Completed”), pluck = “name”, order\_by = “creation desc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L158) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L314) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L295)

<a id="op-7aa245608a3a44"></a>
### Run changes

`operation_relationships_binding_crm_domain_enrichment_api_run_changes`

**Inputs** runs.

**Declared result** dict at tuple(str, list).

**Record and data access** read “CRM Enrichment Run Change” via get\_all.

**Explicit results** mapping() · out.

**Local steps**

- If not runs.
  - Return mapping().
- Set rows from Platform.get\_all(“CRM Enrichment Run Change”, filters = mapping(“parenttype” → “CRM Enrichment Run”, “parent” → list(“in”, runs)), fields = list(“parent”, “fieldname”, “new\_value”), order\_by = “idx asc”).
- Set out from mapping().
- For each row in rows.
  - Evaluate out.setdefault(row.parent, list()).append(row).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L161) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L317) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L298)

<a id="op-c490c6c3b6c9da"></a>
### Undoable run

`operation_relationships_binding_crm_domain_enrichment_api_undoable_run`

**Inputs** runs.

**Declared result** (str bitwise or no value).

**Explicit results** next(generator of run for run drawn from runs where run belongs to changed, no value).

**Local steps**

- Set changed from \_run\_changes(runs).
- Return next(generator of run for run drawn from runs where run belongs to changed, no value).
  - Draw run from runs, keep a combination only if (run belongs to changed).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L163) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L319) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L300)

<a id="op-32182df27a92d5"></a>
### Enqueue run

`operation_relationships_domain_enrichment_application_interface_business_behavior_enqueue_run`

**Inputs** cfg, reference\_doctype, reference\_name, website.

**Declared result** dict.

**Explicit results** enqueue\_enrichment(reference\_doctype, reference\_name, website, Platform.session.user).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Set a website on this record before enriching.”.

**Local steps**

- Evaluate \_check\_writable(cfg, reference\_doctype, reference\_name).
- Set website from (website or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in website → empty text.
- If not website.
  - Call the validation error handler Platform.throw(translated “Set a website on this record before enriching.”, Platform.ValidationError).
- Return enqueue\_enrichment(reference\_doctype, reference\_name, website, Platform.session.user).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L232) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L419) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L400)

<a id="op-0bf6a31b3cd783"></a>
### Enrich

`operation_relationships_domain_enrichment_application_interface_business_behavior_enrich`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist(), rate\_limit(limit = ENRICH\_RATE\_LIMIT, seconds = 60).

**Declared result** dict.

**Record and data access** resolve a document from reference\_doctype via get\_doc.

**Explicit results** \_enqueue\_run(cfg, reference\_doctype, reference\_name, website).

**Local steps**

- Set cfg from get\_config().
- Set doc from Platform.get\_doc(reference\_doctype, reference\_name).
- Set website from (doc.get(“website”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“website”) → empty text.
- Return \_enqueue\_run(cfg, reference\_doctype, reference\_name, website).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L4272) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L420) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L401)

<a id="op-b8517017f5bcac"></a>
### Retry

`operation_relationships_domain_enrichment_application_interface_business_behavior_retry`

**Inputs** run.

**Wrappers, in declaration order** Platform.whitelist(), rate\_limit(limit = ENRICH\_RATE\_LIMIT, seconds = 60).

**Declared result** dict.

**Record and data access** resolve a document from “CRM Enrichment Run” via get\_doc · resolve a document from run\_doc.reference\_doctype via get\_doc.

**Explicit results** \_enqueue\_run(cfg, run\_doc.reference\_doctype, run\_doc.reference\_name, website).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “This run has no linked record to re-enrich.”.

**Local steps**

- Set run\_doc from Platform.get\_doc(“CRM Enrichment Run”, run).
- If (not run\_doc.reference\_doctype or not run\_doc.reference\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not run\_doc.reference\_doctype → not run\_doc.reference\_name.
  - Call the validation error handler Platform.throw(translated “This run has no linked record to re-enrich.”, Platform.ValidationError).
- Set cfg from get\_config().
- Set target from Platform.get\_doc(run\_doc.reference\_doctype, run\_doc.reference\_name).
- Set website from ((target.get(“website”) or empty text).strip() or (run\_doc.source\_website or empty text).strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (target.get(“website”) or empty text).strip() → (run\_doc.source\_website or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target.get(“website”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in run\_doc.source\_website → empty text.
- Return \_enqueue\_run(cfg, run\_doc.reference\_doctype, run\_doc.reference\_name, website).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L4518) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L421) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L402)

<a id="op-22e943324aa697"></a>
### Undo

`operation_relationships_binding_crm_domain_enrichment_api_undo`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)), rate\_limit(limit = ENRICH\_RATE\_LIMIT, seconds = 60).

**Declared result** dict.

**Record and data access** resolve a document from “CRM Enrichment Run” via get\_doc.

**State and service calls** request set\_value on “CRM Enrichment Run”.

**Explicit results** out.

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Enrichment is still running for this record. Try again once it finishes.” · validation helper with Platform.ValidationError — translated “There is no enrichment to undo for this record.”.

**Local steps**

- Evaluate \_check\_writable(get\_config(), reference\_doctype, reference\_name).
- If is\_job\_enqueued(enrichment\_job\_id(reference\_doctype, reference\_name)).
  - Call the validation error handler Platform.throw(translated “Enrichment is still running for this record. Try again once it finishes.”, Platform.ValidationError).
- Set runs from \_completed\_runs(reference\_doctype, reference\_name).
- Set run from \_undoable\_run(runs).
- If not run.
  - Call the validation error handler Platform.throw(translated “There is no enrichment to undo for this record.”, Platform.ValidationError).
- Set out from Platform.get\_doc(“CRM Enrichment Run”, run).undo().
- For each newer in runs at slice no value to runs.index(run).
  - Evaluate Platform.db.set\_value(“CRM Enrichment Run”, newer, mapping(“status” → “Reverted”, “undone\_on” → now\_datetime(), “undone\_by” → Platform.session.user)).
- Return out.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L162) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L318) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L299)

<a id="op-e7c39243c3f869"></a>
### Get status

`operation_relationships_binding_crm_domain_enrichment_api_get_status`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** resolve a document from reference\_doctype via get\_doc · read “CRM Enrichment Run” via get\_value.

**Explicit results** mapping(“running” → is\_job\_enqueued(enrichment\_job\_id(reference\_doctype, reference\_name)), “last\_run\_status” → last\_run.status when last\_run, otherwise no value, “filled\_fields” → filled\_fields, “notes” → notes).

**Local steps**

- Set doc from Platform.get\_doc(reference\_doctype, reference\_name).
- Evaluate doc.check\_permission(“read”).
- Set last\_run from Platform.db.get\_value(“CRM Enrichment Run”, mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name), list(“name”, “status”, “notes”), as\_dict = true, order\_by = “creation desc”).
- Set tuple(filled\_fields, notes) from tuple(list(), list()).
- If (last\_run and last\_run.status equals “Completed”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_run → last\_run.status equals “Completed”.
  - For each change in \_run\_changes(list(last\_run.name)).get(last\_run.name, list()).
    - Set df from doc.meta.get\_field(change.fieldname).
    - Set label from translated df.label when (df and df.label), otherwise change.fieldname.
      - Value choice on (df and df.label) — true gives translated df.label, false gives change.fieldname.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.label.
    - If label does not belong to filled\_fields.
      - Evaluate filled\_fields.append(label).
  - Set notes from (last\_run.notes or empty text).splitlines().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in last\_run.notes → empty text.
- Return mapping(“running” → is\_job\_enqueued(enrichment\_job\_id(reference\_doctype, reference\_name)), “last\_run\_status” → last\_run.status when last\_run, otherwise no value, “filled\_fields” → filled\_fields, “notes” → notes).
  - Value choice on last\_run — true gives last\_run.status, false gives no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L160) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L316) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L297)

<a id="op-98079c53365966"></a>
### Get enriched fields

`operation_relationships_binding_crm_domain_enrichment_api_get_enriched_fields`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** resolve a document from reference\_doctype via get\_doc.

**Explicit results** list() · out.

**Local steps**

- Set doc from Platform.get\_doc(reference\_doctype, reference\_name).
- Evaluate doc.check\_permission(“read”).
- Set runs from \_completed\_runs(reference\_doctype, reference\_name).
- If not runs.
  - Return list().
- Set refreshed from set of mapping.target\_fieldname for mapping drawn from get\_config().mappings\_by\_doctype.get(reference\_doctype, list()) where mapping.write\_policy equals POLICY\_ALWAYS\_REFRESH.
  - Draw mapping from get\_config().mappings\_by\_doctype.get(reference\_doctype, list()), keep a combination only if (mapping.write\_policy equals POLICY\_ALWAYS\_REFRESH).
- Set changes\_by\_run from \_run\_changes(runs).
- Set tuple(out, seen) from tuple(list(), set()).
- For each run in runs.
  - For each change in changes\_by\_run.get(run, list()).
    - If change.fieldname belongs to seen.
      - Continue with the next iteration or loop test.
    - Evaluate seen.add(change.fieldname).
    - Set df from doc.meta.get\_field(change.fieldname).
    - If not df.
      - Continue with the next iteration or loop test.
    - Set value from restore\_value(df, change.new\_value).
    - Evaluate out.append(mapping(“fieldname” → change.fieldname, “label” → translated df.label, “value” → value, “edited” → cstr(doc.get(change.fieldname)) differs from cstr(value), …)).
- Return out.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L159) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L315) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L296)

## Service · Config

<a id="op-b8f883291737c8"></a>
### Setting

`operation_relationships_domain_enrichment_configuration_business_behavior_setting`

**Inputs** doc, key.

**Explicit results** DEFAULT\_SETTINGS.get(key) when val belongs to tuple(no value, empty text), otherwise val.

**Local steps**

- Set val from doc.get(key).
- Return DEFAULT\_SETTINGS.get(key) when val belongs to tuple(no value, empty text), otherwise val.
  - Value choice on val belongs to tuple(no value, empty text) — true gives DEFAULT\_SETTINGS.get(key), false gives val.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L4922) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L434) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L415)

<a id="op-49eb771d732172"></a>
### Get settings

`operation_relationships_domain_enrichment_configuration_business_behavior_get_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “CRM Enrichment Settings” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“CRM Enrichment Settings”).

**Local steps**

- Return Platform.get\_cached\_doc(“CRM Enrichment Settings”).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“CRM Enrichment Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5043) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L431) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L412)

<a id="op-fb9c40381ed561"></a>
### Auto enrich enabled for

`operation_relationships_domain_enrichment_configuration_business_behavior_auto_enrich_enabled_for`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** bool((\_setting(s, “enabled”) and \_setting(s, “auto\_enrich”) and doctype belongs to ENRICHABLE\_DOCTYPES)).

**Local steps**

- Set s from get\_settings().
- Return bool((\_setting(s, “enabled”) and \_setting(s, “auto\_enrich”) and doctype belongs to ENRICHABLE\_DOCTYPES)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_setting(s, “enabled”) → \_setting(s, “auto\_enrich”) → doctype belongs to ENRICHABLE\_DOCTYPES.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5094) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L422) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L403)

<a id="op-6aed3ccc6678c3"></a>
### Rule.label

`operation_relationships_domain_enrichment_configuration_business_behavior_rule_label`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** self.industry when self.rule\_type equals “Industry”, otherwise self.target\_value.

**Local steps**

- Return self.industry when self.rule\_type equals “Industry”, otherwise self.target\_value.
  - Value choice on self.rule\_type equals “Industry” — true gives self.industry, false gives self.target\_value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5245) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L432) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L413)

<a id="op-0ce308ff3aff99"></a>
### Rule.matches

`operation_relationships_domain_enrichment_configuration_business_behavior_rule_matches`

**Inputs** self, text.

**Declared result** int.

**Explicit results** 0 · sum(generator of len(rx.findall(text)) for tuple(rx, \_raw) drawn from self.patterns).

**Local steps**

- If not text.
  - Return 0.
- Return sum(generator of len(rx.findall(text)) for tuple(rx, \_raw) drawn from self.patterns).
  - Draw tuple(rx, \_raw) from self.patterns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5324) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L433) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L414)

<a id="op-d9e53a5021ee72"></a>
### Enrichment Config.setting

`operation_relationships_domain_enrichment_configuration_business_behavior_enrichment_configuration_setting`

**Inputs** self, key, default = no value.

**Explicit results** DEFAULT\_SETTINGS.get(key, default) · val.

**Local steps**

- Set val from self.settings.get(key).
- If val belongs to tuple(no value, empty text).
  - Return DEFAULT\_SETTINGS.get(key, default).
- Return val.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5468) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L429) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L410)

<a id="op-952607c78882e4"></a>
### Enrichment Config.rules

`operation_relationships_domain_enrichment_configuration_business_behavior_enrichment_configuration_rules`

**Inputs** self, rule\_type.

**Declared result** list.

**Explicit results** self.rules\_by\_type.get(rule\_type, list()).

**Local steps**

- Return self.rules\_by\_type.get(rule\_type, list()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5613) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L428) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L409)

<a id="op-2aa55b466c1bf0"></a>
### Compile pattern

`operation_relationships_domain_enrichment_configuration_business_behavior_compile_pattern`

**Inputs** pattern, is\_regex.

**Explicit results** re.compile(pattern, re.IGNORECASE) · re.compile(formatted text \\b{re.escape(pattern)}\\b, re.IGNORECASE) · no value.

**Local steps**

- Attempt the following.
  - If is\_regex.
    - Return re.compile(pattern, re.IGNORECASE).
  - Return re.compile(formatted text \\b{re.escape(pattern)}\\b, re.IGNORECASE).
- On failure (re.error).
  - Evaluate Platform.log\_error(title = “Domain Enrichment: invalid rule pattern”, message = formatted text Could not compile pattern: {pattern}).
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5689) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L427) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L408)

<a id="op-0398d59185cfdd"></a>
### Build rules

`operation_relationships_domain_enrichment_configuration_business_behavior_build_rules`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “CRM Enrichment Rule” via get\_all · resolve a document from “CRM Enrichment Rule” via get\_doc.

**Explicit results** rules\_by\_type.

**Local steps**

- Set rules\_by\_type from mapping().
- Set names from Platform.get\_all(“CRM Enrichment Rule”, filters = mapping(“enabled” → 1), pluck = “name”).
- For each name in names.
  - Set doc from Platform.get\_doc(“CRM Enrichment Rule”, name).
  - Set compiled from list().
  - For each pat in (doc.patterns or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.patterns → list().
    - Set rx from \_compile\_pattern(pat.pattern, pat.is\_regex).
    - If rx is distinct from no value.
      - Evaluate compiled.append(tuple(rx, pat.pattern)).
  - If not compiled.
    - Continue with the next iteration or loop test.
  - Set rule from Rule(rule\_type = doc.rule\_type, target\_value = (doc.target\_value or empty text), industry = (doc.industry or empty text), weight = (doc.weight or 1.0), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.target\_value → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.industry → empty text.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.weight → 1.0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.match\_scope → “Full Text”.
  - Evaluate rules\_by\_type.setdefault(doc.rule\_type, list()).append(rule).
- Return rules\_by\_type.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L5927) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L425) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L406)

<a id="op-bed3cd5fa3a88e"></a>
### Build mappings

`operation_relationships_domain_enrichment_configuration_business_behavior_build_mappings`

**Inputs** no declared parameters.

**Declared result** dict.

**Record and data access** read “CRM Enrichment Field Mapping” via get\_all.

**Explicit results** mappings\_by\_doctype.

**Local steps**

- Set mappings\_by\_doctype from mapping().
- Set rows from Platform.get\_all(“CRM Enrichment Field Mapping”, filters = mapping(“enabled” → 1), fields = list(“source\_key”, “target\_doctype”, “target\_fieldname”, “write\_policy”, …)).
- For each row in rows.
  - Set mapping from Mapping(source\_key = row.source\_key, target\_doctype = row.target\_doctype, target\_fieldname = row.target\_fieldname, write\_policy = (row.write\_policy or “Fill if empty”), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.write\_policy → “Fill if empty”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.create\_missing\_link → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.default\_values → empty text.
  - Evaluate mappings\_by\_doctype.setdefault(row.target\_doctype, list()).append(mapping).
- Return mappings\_by\_doctype.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L6442) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L424) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L405)

<a id="op-7ef44dc9706115"></a>
### Build settings

`operation_relationships_domain_enrichment_configuration_business_behavior_build_settings`

**Inputs** settings\_doc.

**Declared result** dict.

**Explicit results** out.

**Local steps**

- Set out from mapping().
- For each key in DEFAULT\_SETTINGS.
  - Set out at key from settings\_doc.get(key).
- Return out.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0017.json#L6806) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L426) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L407)

<a id="op-e8dda4aec6a17c"></a>
### Build config

`operation_relationships_domain_enrichment_configuration_business_behavior_build_configuration`

**Inputs** no declared parameters.

**Declared result** EnrichmentConfig.

**Record and data access** resolve a document from “CRM Enrichment Settings” via get\_cached\_doc.

**Explicit results** EnrichmentConfig(settings = \_build\_settings(settings\_doc), rules\_by\_type = \_build\_rules(), mappings\_by\_doctype = \_build\_mappings(), link\_priority = link\_priority, …).

**Local steps**

- Set settings\_doc from Platform.get\_cached\_doc(“CRM Enrichment Settings”).
- Set link\_priority from (list of tuple(kw.keyword.lower(), (kw.weight or 1.0)) for kw drawn from (settings\_doc.link\_priority\_order or list()) where kw.keyword or list(DEFAULT\_LINK\_PRIORITY)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of tuple(kw.keyword.lower(), (kw.weight or 1.0)) for kw drawn from (settings\_doc.link\_priority\_order or list()) where kw.keyword → list(DEFAULT\_LINK\_PRIORITY).
  - Draw kw from (settings\_doc.link\_priority\_order or list()), keep a combination only if (kw.keyword).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in kw.weight → 1.0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings\_doc.link\_priority\_order → list().
- Set skip\_patterns from list of sp.pattern for sp drawn from (settings\_doc.skip\_patterns or list()) where sp.pattern.
  - Draw sp from (settings\_doc.skip\_patterns or list()), keep a combination only if (sp.pattern).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings\_doc.skip\_patterns → list().
- Set allowed\_domains from list of d.domain.lower().strip() for d drawn from (settings\_doc.allowed\_domains or list()) where d.domain.
  - Draw d from (settings\_doc.allowed\_domains or list()), keep a combination only if (d.domain).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings\_doc.allowed\_domains → list().
- Set blocked\_domains from list of d.domain.lower().strip() for d drawn from (settings\_doc.blocked\_domains or list()) where d.domain.
  - Draw d from (settings\_doc.blocked\_domains or list()), keep a combination only if (d.domain).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in settings\_doc.blocked\_domains → list().
- Return EnrichmentConfig(settings = \_build\_settings(settings\_doc), rules\_by\_type = \_build\_rules(), mappings\_by\_doctype = \_build\_mappings(), link\_priority = link\_priority, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“CRM Enrichment Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L423) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L404)

<a id="op-828b02d48688fb"></a>
### Get config

`operation_relationships_domain_enrichment_configuration_business_behavior_get_configuration`

**Inputs** no declared parameters.

**Declared result** EnrichmentConfig.

**Explicit results** \_build\_config().

**Local steps**

- Return \_build\_config().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L506) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L430) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L411)
