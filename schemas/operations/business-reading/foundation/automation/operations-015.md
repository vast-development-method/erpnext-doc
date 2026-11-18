# Workflow, automation and dispatch · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Client

<a id="op-7b0c96fafb5088"></a>
### Detail

`operation_foundation_binding_foundation_flow_daemon_client_detail`

**Inputs** response.

**Declared result** Any.

**Explicit results** response.text at slice no value to 500 · list of mapping(“loc” → item.get(“loc”), “msg” → item.get(“msg”)) for item drawn from detail where isinstance(item, dict) · detail.

**Local steps**

- Attempt the following.
  - Set body from response.json().
- On failure (ValueError).
  - Return response.text at slice no value to 500.
- Set detail from body.get(“detail”, body) when isinstance(body, dict), otherwise body.
  - Value choice on isinstance(body, dict) — true gives body.get(“detail”, body), false gives body.
- If isinstance(detail, list).
  - Return list of mapping(“loc” → item.get(“loc”), “msg” → item.get(“msg”)) for item drawn from detail where isinstance(item, dict).
    - Draw item from detail, keep a combination only if (isinstance(item, dict)).
- Return detail.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L199) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L924)

## Service · Commands

<a id="op-56fc6bf7225078"></a>
### Flow server

`operation_foundation_binding_foundation_flow_commands_init_flow_server`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.group(“flow-server”).

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L898) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L874)

<a id="op-970fa2a1ea3ce7"></a>
### Setup

`operation_foundation_binding_foundation_flow_commands_init_setup`

**Inputs** no declared parameters.

**Wrappers, in declaration order** flow\_server.command(“setup”).

**Local steps**

- Bind dependencies lifecycle.
- Evaluate \_run\_on\_every\_flow\_site(\_provision).
- If lifecycle.supervised().
  - Evaluate lifecycle.ensure\_running().
- Otherwise.
  - Evaluate lifecycle.restart().
- Evaluate \_run\_on\_every\_flow\_site(\_sync\_tools).
- Evaluate click.secho(lifecycle.status(), fg = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L879)

<a id="op-0d72cb721ea315"></a>
### Start

`operation_foundation_binding_foundation_flow_commands_init_start`

**Inputs** no declared parameters.

**Wrappers, in declaration order** flow\_server.command(“start”).

**Local steps**

- Bind dependencies lifecycle.
- If lifecycle.ensure\_running().
  - Evaluate \_run\_on\_every\_flow\_site(\_sync\_tools).
- Otherwise.
  - Evaluate click.echo(“already running; ′bench flow-server restart′ loads new extensions”).
- Evaluate click.secho(lifecycle.status(), fg = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L880)

<a id="op-6b0e95e8566967"></a>
### Serve

`operation_foundation_binding_foundation_flow_commands_init_serve`

**Inputs** no declared parameters.

**Wrappers, in declaration order** flow\_server.command(“serve”).

**Local steps**

- Bind dependencies lifecycle.
- Evaluate lifecycle.serve().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L878)

<a id="op-85cd66a2b55941"></a>
### Stop

`operation_foundation_binding_foundation_flow_commands_init_stop`

**Inputs** no declared parameters.

**Wrappers, in declaration order** flow\_server.command(“stop”).

**Explicit failure paths** click.ClickException(“supervisor runs the flow server; stop it with supervisorctl”).

**Local steps**

- Bind dependencies lifecycle.
- If lifecycle.supervised().
  - Raise click.ClickException(“supervisor runs the flow server; stop it with supervisorctl”).
- Evaluate lifecycle.stop().
- Evaluate click.echo(lifecycle.status()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L882)

<a id="op-d1d4afb1f6fcea"></a>
### Restart

`operation_foundation_binding_foundation_flow_commands_init_restart`

**Inputs** no declared parameters.

**Wrappers, in declaration order** flow\_server.command(“restart”).

**Explicit failure paths** click.ClickException(“supervisor runs the flow server; restart it with supervisorctl or ′pilot processes restart Platform′”).

**Local steps**

- Bind dependencies lifecycle.
- If lifecycle.supervised().
  - Raise click.ClickException(“supervisor runs the flow server; restart it with supervisorctl or ′pilot processes restart Platform′”).
- Evaluate lifecycle.restart().
- Evaluate \_run\_on\_every\_flow\_site(\_sync\_tools).
- Evaluate click.secho(lifecycle.status(), fg = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L876)

<a id="op-3305a9416c65eb"></a>
### Status

`operation_foundation_binding_foundation_flow_commands_init_status`

**Inputs** no declared parameters.

**Wrappers, in declaration order** flow\_server.command(“status”).

**Local steps**

- Bind dependencies lifecycle.
- Evaluate click.echo(lifecycle.status()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L881)

<a id="op-e5d9557575bf31"></a>
### Run on every flow site

`operation_foundation_binding_foundation_flow_commands_init_run_on_every_flow_site`

**Inputs** step.

**Declared result** no value.

**Local steps**

- Bind dependencies get\_sites.
- For each site in get\_sites().
  - Evaluate Platform.init(site).
  - Attempt the following.
    - Evaluate Platform.connect().
    - Evaluate step(site).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L877)

<a id="op-dbaaa1d7bb8452"></a>
### Provision

`operation_foundation_binding_foundation_flow_commands_init_provision`

**Inputs** site.

**Declared result** no value.

**Local steps**

- Bind dependencies lifecycle.
- Evaluate lifecycle.provision\_site().
- Evaluate click.echo(formatted text provisioned {site}).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L875)

<a id="op-fbfee64bd97f4e"></a>
### Sync tools

`operation_foundation_binding_foundation_flow_commands_init_sync_tools`

**Inputs** \_site.

**Declared result** no value.

**State and service calls** commit.

**Local steps**

- Bind dependencies sync\_server\_tools.
- Evaluate sync\_server\_tools().
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L883)

## Service · Conditions

<a id="op-d4c6f4780eafae"></a>
### Evaluate filter tree

`operation_foundation_binding_foundation_automation_engine_conditions_evaluate_filter_tree`

**Inputs** doc, filters.

**Declared result** bool.

**Explicit results** true · evaluate\_filters(doc, list of \_normalise\_row(row) for row drawn from filters) · \_evaluate\_sequence(doc, filters).

**Local steps**

- Bind dependencies evaluate\_filters.
- If not filters.
  - Return true.
- If not \_has\_conjunctions(filters).
  - Return evaluate\_filters(doc, list of \_normalise\_row(row) for row drawn from filters).
    - Draw row from filters.
- Return \_evaluate\_sequence(doc, filters).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L147) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L363)

<a id="op-c388cbccde39f6"></a>
### Normalise row

`operation_foundation_binding_foundation_automation_engine_conditions_normalise_row`

**Inputs** row.

**Explicit results** list(row at 0, OPERATOR\_ALIASES at row at 1, expanded list(row) at slice 2 to no value) · row.

**Local steps**

- If (isinstance(row, (list bitwise or tuple)) and len(row) ≥ 2 and row at 1 belongs to OPERATOR\_ALIASES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(row, (list bitwise or tuple)) → len(row) ≥ 2 → row at 1 belongs to OPERATOR\_ALIASES.
  - Return list(row at 0, OPERATOR\_ALIASES at row at 1, expanded list(row) at slice 2 to no value).
- Return row.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L152) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L368)

<a id="op-affef00cc30b2a"></a>
### Has conjunctions

`operation_foundation_binding_foundation_automation_engine_conditions_has_conjunctions`

**Inputs** filters.

**Declared result** bool.

**Explicit results** any(generator of (isinstance(item, str) and item belongs to CONJUNCTIONS) for item drawn from filters).

**Local steps**

- Return any(generator of (isinstance(item, str) and item belongs to CONJUNCTIONS) for item drawn from filters).
  - Draw item from filters.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → item belongs to CONJUNCTIONS.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L151) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L367)

<a id="op-24d8ff6fef1bb7"></a>
### Evaluate sequence

`operation_foundation_binding_foundation_automation_engine_conditions_evaluate_sequence`

**Inputs** doc, filters.

**Declared result** bool.

**Explicit results** any(generator of all(generator of \_evaluate\_operand(doc, operand) for operand drawn from group) for group drawn from groups).

**Local steps**

- Set tuple(groups, current) from tuple(list(), list()).
- For each item in filters.
  - If (isinstance(item, str) and item equals “or”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → item equals “or”.
    - Evaluate groups.append(current).
    - Set current from list().
  - Otherwise.
    - If (isinstance(item, str) and item equals “and”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(item, str) → item equals “and”.
      - Continue with the next iteration or loop test.
    - Otherwise.
      - Evaluate current.append(item).
- Evaluate groups.append(current).
- Return any(generator of all(generator of \_evaluate\_operand(doc, operand) for operand drawn from group) for group drawn from groups).
  - Draw group from groups.
  - Draw operand from group.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L150) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L366)

<a id="op-33e41656820b39"></a>
### Evaluate operand

`operation_foundation_binding_foundation_automation_engine_conditions_evaluate_operand`

**Inputs** doc, operand.

**Declared result** bool.

**Explicit results** evaluate\_filter\_tree(doc, list(operand)).

**Local steps**

- If (isinstance(operand, (list bitwise or tuple)) and operand and isinstance(operand at 0, (list bitwise or tuple))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(operand, (list bitwise or tuple)) → operand → isinstance(operand at 0, (list bitwise or tuple)).
  - Return evaluate\_filter\_tree(doc, list(operand)).
- Return evaluate\_filter\_tree(doc, list(operand)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L148) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L388) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L364)

<a id="op-110862c0c32f0d"></a>
### Validate related condition

`operation_foundation_binding_foundation_automation_engine_conditions_validate_related_condition`

**Inputs** stored, targets.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Unknown related-condition source alias: {0}”.format(source).

**Local steps**

- Set condition from \_parse(stored).
- If not condition.
  - Return no value.
- Set source from condition at “source”.
- If source does not belong to targets.
  - Call the validation error handler Platform.throw(translated “Unknown related-condition source alias: {0}”.format(source)).
- If targets at source.
  - Evaluate get\_relationship\_definition(targets at source, condition at “relationship”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L158) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L374)

<a id="op-5defd3debcb833"></a>
### Evaluate related condition

`operation_foundation_binding_foundation_automation_engine_conditions_evaluate_related_condition`

**Inputs** stored, context.

**Declared result** bool.

**Explicit results** true · \_compare(condition, count).

**Local steps**

- Set condition from \_parse(stored).
- If not condition.
  - Return true.
- Set source from load\_record(context at “records”.get(condition at “source”), permission\_type = “read”).
- Set filters from \_render\_filters(condition at “filters”, context).
- Set limit from 1 when condition at “type” belongs to EXISTENCE\_OPERATORS, otherwise no value.
  - Value choice on condition at “type” belongs to EXISTENCE\_OPERATORS — true gives 1, false gives no value.
- Set count from len(query\_related(source, condition at “relationship”, filters, limit)).
- Return \_compare(condition, count).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L149) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L389) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L365)

<a id="op-5e6d358137476e"></a>
### Parse

`operation_foundation_binding_foundation_automation_engine_conditions_parse`

**Inputs** stored.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“type” → operator, “source” → (condition.get(“source”) or “trigger”), “relationship” → condition at “relationship”, “filters” → (condition.get(“filters”) or list()), …).

**Explicit failure paths** validation helper — translated “Related record condition must be a JSON object” · validation helper — translated “Unsupported related condition: {0}”.format(operator) · validation helper — translated “Related record condition needs a relationship”.

**Local steps**

- If not stored.
  - Return no value.
- Set condition from Platform.parse\_json(stored) when isinstance(stored, str), otherwise stored.
  - Value choice on isinstance(stored, str) — true gives Platform.parse\_json(stored), false gives stored.
- If not isinstance(condition, dict).
  - Call the validation error handler Platform.throw(translated “Related record condition must be a JSON object”).
- Set operator from (condition.get(“type”) or “RelatedExists”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition.get(“type”) → “RelatedExists”.
- If operator does not belong to OPERATORS.
  - Call the validation error handler Platform.throw(translated “Unsupported related condition: {0}”.format(operator)).
- If not condition.get(“relationship”).
  - Call the validation error handler Platform.throw(translated “Related record condition needs a relationship”).
- Return mapping(“type” → operator, “source” → (condition.get(“source”) or “trigger”), “relationship” → condition at “relationship”, “filters” → (condition.get(“filters”) or list()), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition.get(“source”) → “trigger”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition.get(“filters”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in condition.get(“comparison”) → “&gt;=”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L153) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L369)

<a id="op-994bb639efcf40"></a>
### Compare

`operation_foundation_binding_foundation_automation_engine_conditions_compare`

**Inputs** condition, count.

**Declared result** bool.

**Explicit results** count &gt; 0 · count equals 0 · comparison(count, condition at “value”).

**Explicit failure paths** validation helper — translated “Unsupported count comparison: {0}”.format(condition at “comparison”).

**Local steps**

- If condition at “type” equals “RelatedExists”.
  - Return count &gt; 0.
- If condition at “type” equals “RelatedNotExists”.
  - Return count equals 0.
- Set comparison from COMPARISONS.get(condition at “comparison”).
- If not comparison.
  - Call the validation error handler Platform.throw(translated “Unsupported count comparison: {0}”.format(condition at “comparison”)).
- Return comparison(count, condition at “value”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L144) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L360)

<a id="op-6e23b5c72c7e47"></a>
### Render filters

`operation_foundation_binding_foundation_automation_engine_conditions_render_filters`

**Inputs** filters, context.

**Explicit results** filters · \_render\_value(filters, \_template\_context(context, templates)).

**Local steps**

- Set templates from list(\_templates(filters)).
- If not templates.
  - Return filters.
- Return \_render\_value(filters, \_template\_context(context, templates)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L370)

<a id="op-f8d2fdab613ee0"></a>
### Templates

`operation_foundation_binding_foundation_automation_engine_conditions_templates`

**Inputs** value.

**Local steps**

- If isinstance(value, str).
  - If “{{” belongs to value.
    - yield value.
- Otherwise.
  - If isinstance(value, list).
    - For each item in value.
      - yield values from \_templates(item).
  - Otherwise.
    - If isinstance(value, dict).
      - yield values from \_templates(list(value.values())).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L157) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L373)

<a id="op-31bee18a9b3dfa"></a>
### Template context

`operation_foundation_binding_foundation_automation_engine_conditions_template_context`

**Inputs** context, templates.

**Declared result** dict.

**Explicit results** mapping(“context” → context, expand records).

**Local steps**

- Set referenced from mapping of alias → reference for tuple(alias, reference) drawn from context at “records”.items() where any(generator of alias belongs to template for template drawn from templates).
  - Draw tuple(alias, reference) from context at “records”.items(), keep a combination only if (any(generator of alias belongs to template for template drawn from templates)).
  - Draw template from templates.
- Set records from mapping of alias → load\_record(reference, permission\_type = “read”) for tuple(alias, reference) drawn from referenced.items().
  - Draw tuple(alias, reference) from referenced.items().
- Return mapping(“context” → context, expand records).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L372)

<a id="op-3b58398a472b59"></a>
### Render value

`operation_foundation_binding_foundation_automation_engine_conditions_render_value`

**Inputs** value, render\_context.

**Explicit results** Platform.render\_template(value, render\_context) · list of \_render\_value(item, render\_context) for item drawn from value · mapping of key → \_render\_value(item, render\_context) for tuple(key, item) drawn from value.items() · value.

**Local steps**

- If (isinstance(value, str) and “{{” belongs to value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → “{{” belongs to value.
  - Return Platform.render\_template(value, render\_context).
- If isinstance(value, list).
  - Return list of \_render\_value(item, render\_context) for item drawn from value.
    - Draw item from value.
- If isinstance(value, dict).
  - Return mapping of key → \_render\_value(item, render\_context) for tuple(key, item) drawn from value.items().
    - Draw tuple(key, item) from value.items().
- Return value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0001.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L371)
