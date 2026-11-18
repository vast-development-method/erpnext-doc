# Forms, reports and navigation · operations 42

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Meta

<a id="op-029eaeb4546f82"></a>
### Form Meta.show missing doctype msg

`operation_foundation_desk_form_meta_business_behavior_form_meta_show_missing_record_type_message`

**Inputs** self, df.

**Explicit failure paths** validation helper — msg.

**Local steps**

- Evaluate Platform.clear\_last\_message().
- Set msg from translated “Field {0} is referring to non-existing doctype {1}.”.format(Platform.bold(df.fieldname), Platform.bold(df.options)).
- If df.get(“is\_custom\_field”).
  - Set custom\_field\_link from get\_link\_to\_form(“Custom Field”, df.name).
  - Update msg using + (one space + translated “Please delete the field from {0} or add the required doctype.”.format(custom\_field\_link)).
- Call the validation error handler Platform.throw(msg, title = translated “Missing DocType”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L4566) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L266)

<a id="op-fbc5d8eeb5eb6a"></a>
### Form Meta.load print formats

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_print_formats`

**Inputs** self.

**Record and data access** execute query text (SELECT, Print Format).

**Local steps**

- Set print\_formats from Platform.db.sql(query text (SELECT, Print Format), tuple(self.name), as\_dict = 1, update = mapping(“doctype” → “:Print Format”)).
- Evaluate self.set(“\_\_print\_formats”, print\_formats).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L4885) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L263)

<a id="op-e3aace1c4a9200"></a>
### Form Meta.load workflows

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_workflows`

**Inputs** self.

**Record and data access** read “Workflow” via exists · resolve a document from “Workflow” via get\_doc · resolve a document from “Workflow State” via get\_doc.

**Local steps**

- Set workflow\_name from self.get\_workflow().
- Set workflow\_docs from list().
- If (workflow\_name and Platform.db.exists(“Workflow”, workflow\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in workflow\_name → Platform.db.exists(“Workflow”, workflow\_name).
  - Set workflow from Platform.get\_doc(“Workflow”, workflow\_name).
  - Evaluate workflow\_docs.append(workflow).
  - Evaluate workflow\_docs.extend(generator of Platform.get\_doc(“Workflow State”, d.state) for d drawn from workflow.get(“states”)).
    - Draw d from workflow.get(“states”).
- Evaluate self.set(“\_\_workflow\_docs”, workflow\_docs).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L5084) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L265)

<a id="op-14e734223ccdd2"></a>
### Form Meta.load templates

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_templates`

**Inputs** self.

**Local steps**

- If not self.custom.
  - Set module from load\_doctype\_module(self.name).
  - Set app from module.\_\_name\_\_.split(“.”, 1) at 0.
  - Set templates from mapping().
  - If hasattr(module, “form\_grid\_templates”).
    - For each tuple(key, path) in module.form\_grid\_templates.items().
      - Set templates at key from get\_html\_format(Platform.get\_app\_path(app, path)).
    - Evaluate self.set(“\_\_form\_grid\_templates”, templates).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L5379) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L264)

<a id="op-282ff566bd0d44"></a>
### Form Meta.load dashboard

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_dashboard`

**Inputs** self.

**Local steps**

- Evaluate self.set(“\_\_dashboard”, self.get\_dashboard\_data()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L5665) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L260)

<a id="op-6245e913d42fd0"></a>
### Form Meta.load kanban meta

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_kanban_meta`

**Inputs** self.

**Local steps**

- Evaluate self.load\_kanban\_column\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load kanban column fields](operations-042.md#op-454b0d804b2093).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L5734) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L262)

<a id="op-454b0d804b2093"></a>
### Form Meta.load kanban column fields

`operation_foundation_desk_form_meta_business_behavior_form_meta_load_kanban_column_fields`

**Inputs** self.

**Record and data access** read “Kanban Board” via get\_list.

**Local steps**

- Attempt the following.
  - Set values from Platform.get\_list(“Kanban Board”, fields = list(“field\_name”), filters = mapping(“reference\_doctype” → self.name)).
  - Set fields from list of x at “field\_name” for x drawn from values.
    - Draw x from values.
  - Set fields from list(set(fields)).
  - Evaluate self.set(“\_\_kanban\_column\_fields”, fields).
- On failure (Platform.PermissionError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L5785) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L261)

<a id="op-5ca61def84dc40"></a>
### Get code files via hooks

`operation_foundation_desk_form_meta_business_behavior_get_code_files_via_hooks`

**Inputs** hook, name.

**Explicit results** code\_files.

**Local steps**

- Set code\_files from list().
- For each app\_name in Platform.get\_installed\_apps().
  - Set code\_hook from Platform.get\_hooks(hook, default = mapping(), app\_name = app\_name).
  - If not code\_hook.
    - Continue with the next iteration or loop test.
  - Set files from code\_hook.get(name, list()).
  - If not isinstance(files, list).
    - Set files from list(files).
  - For each file in files.
    - Set path from Platform.get\_app\_path(app\_name, expanded file.strip(“/”).split(“/”)).
    - Evaluate code\_files.append(path).
- Return code\_files.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook, default = mapping(), app\_name = app\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L68) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L268)

<a id="op-80904ddaa846f9"></a>
### Get js

`operation_foundation_desk_form_meta_business_behavior_get_client_script`

**Inputs** path.

**Explicit results** render\_include(js).

**Local steps**

- Set js from Platform.read\_file(path).
- If js.
  - Return render\_include(js).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0203.json#L6380) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L267)

## Service · Models

<a id="op-c03e319e55efba"></a>
### Model Registry.get label

`operation_foundation_binding_foundation_studio_ai_models_modelregistry_get_label`

**Inputs** cls, model\_id.

**Wrappers, in declaration order** classmethod.

**Declared result** str.

**Explicit results** m at “label” · model\_id.

**Local steps**

- For each m in cls.AVAILABLE.
  - If m at “id” equals model\_id.
    - Return m at “label”.
- Return model\_id.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L178) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1841)

<a id="op-dbf49d4c4f82ee"></a>
### Model Registry.is vision capable

`operation_foundation_binding_foundation_studio_ai_models_modelregistry_is_vision_capable`

**Inputs** cls, model\_id.

**Wrappers, in declaration order** classmethod.

**Declared result** bool.

**Explicit results** bool(m.get(“vision\_capable”)) · true.

**Local steps**

- For each m in cls.AVAILABLE.
  - If m at “id” equals model\_id.
    - Return bool(m.get(“vision\_capable”)).
- Return true.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L179) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1866) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1842)

<a id="op-9914e138b1809f"></a>
### Model Registry.get fallbacks

`operation_foundation_binding_foundation_studio_ai_models_modelregistry_get_fallbacks`

**Inputs** cls, model\_id.

**Wrappers, in declaration order** classmethod.

**Declared result** list at str.

**Explicit results** list() · list(cls.SIMPLE).

**Local steps**

- If (not model\_id or cls.SIMPLE belongs to model\_id).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not model\_id → cls.SIMPLE belongs to model\_id.
  - Return list().
- Return list(cls.SIMPLE).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L177) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1840)

<a id="op-ba63d77de80526"></a>
### Model Registry.list all

`operation_foundation_binding_foundation_studio_ai_models_modelregistry_list_all`

**Inputs** cls.

**Wrappers, in declaration order** classmethod.

**Declared result** list.

**Explicit results** cls.AVAILABLE.

**Local steps**

- Return cls.AVAILABLE.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L180) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1867) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1843)

<a id="op-cfeb06bda135c1"></a>
### Get ai models

`operation_foundation_binding_foundation_studio_ai_models_get_ai_models`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(), has\_page\_write\_perm().

**Declared result** list.

**Explicit results** ModelRegistry.list\_all().

**Local steps**

- Return ModelRegistry.list\_all().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1839)

## Record · Module onboarding

[Record definition](../../../../data/record-types/module_onboarding.json)

<a id="op-f9d229d32c2984"></a>
### Module Onboarding.on update

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_on_update`

**Inputs** self.

**Local steps**

- If Platform.conf.developer\_mode.
  - Evaluate export\_to\_files(record\_list = list(list(“Module Onboarding”, self.name)), record\_module = self.module).
  - For each step in self.steps.
    - Evaluate export\_to\_files(record\_list = list(list(“Onboarding Step”, step.step)), record\_module = self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L434) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L880)

<a id="op-da77ae55d82519"></a>
### Module Onboarding.get steps

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_get_steps`

**Inputs** self.

**Record and data access** resolve a document from “Onboarding Step” via get\_doc.

**Explicit results** list of Platform.get\_doc(“Onboarding Step”, step.step) for step drawn from self.steps.

**Local steps**

- Return list of Platform.get\_doc(“Onboarding Step”, step.step) for step drawn from self.steps.
  - Draw step from self.steps.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L631) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L421) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L878)

<a id="op-906efc9ace86ee"></a>
### Module Onboarding.required steps done

`operation_foundation_binding_foundation_desk_doctype_module_onboarding_module_onboarding_moduleonboarding_required_steps_done`

**Inputs** self.

**Declared result** bool.

**Record and data access** resolve a document from “Onboarding Step” via get\_doc.

**Explicit results** all(generator of Platform.get\_doc(“Onboarding Step”, row.step).is\_done() for row drawn from self.steps where not row.is\_optional).

**Local steps**

- Return all(generator of Platform.get\_doc(“Onboarding Step”, row.step).is\_done() for row drawn from self.steps where not row.is\_optional).
  - Draw row from self.steps, keep a combination only if (not row.is\_optional).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L266) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L724)

<a id="op-45a28c66f47357"></a>
### Module Onboarding.get allowed roles

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_get_allowed_roles`

**Inputs** self.

**Explicit results** all\_roles.

**Local steps**

- Set all\_roles from list of role.role for role drawn from self.allow\_roles.
  - Draw role from self.allow\_roles.
- If “System Manager” does not belong to all\_roles.
  - Evaluate all\_roles.append(“System Manager”).
- Return all\_roles.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L720) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L877)

<a id="op-c4bacb2e28b165"></a>
### Module Onboarding.check completion

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_check_completion`

**Inputs** self.

**State and service calls** enqueue with self.mark\_as\_completed.

**Explicit results** true · false.

**Local steps**

- If self.is\_complete.
  - Return true.
- If self.required\_steps\_done().
  - Set self.is\_complete from true.
  - Evaluate Platform.enqueue(self.mark\_as\_completed, enqueue\_after\_commit = true).
  - Return true.
- Return false.

**Methods declared on this owner** [required steps done](operations-042.md#op-906efc9ace86ee).

**Values supplied outside this operation** service or queued work from Platform.enqueue(self.mark\_as\_completed, enqueue\_after\_commit = true).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L17) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L876)

<a id="op-8772c08ab7b0c8"></a>
### Module Onboarding.mark as completed

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_mark_as_completed`

**Inputs** self.

**State and service calls** call save on self.

**Local steps**

- Set self.is\_complete from true.
- Evaluate self.save(ignore\_permissions = true).
- Evaluate capture\_onboarding\_completed(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L18) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L422) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L879)

<a id="op-3bca805cbe54c9"></a>
### Module Onboarding.reset progress

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_reset_progress`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self · call db\_set on step · msgprint with translated “Module onboarding progress reset”.

**Local steps**

- Evaluate Platform.has\_permission(self.doctype, “write”, self.name, throw = true).
- Evaluate self.db\_set(“is\_complete”, 0).
- For each step in self.get\_steps().
  - Evaluate step.db\_set(“is\_complete”, 0).
  - Evaluate step.db\_set(“is\_skipped”, 0).
- Evaluate Platform.msgprint(translated “Module onboarding progress reset”, alert = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get steps](operations-042.md#op-da77ae55d82519).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “write”, self.name, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L19) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L425) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L882)

<a id="op-96eaa02c3cb329"></a>
### Module Onboarding.before export

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_before_export`

**Inputs** self, doc.

**Local steps**

- Set doc.is\_complete from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L1371) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L875)

<a id="op-1127cd59e055c3"></a>
### Module Onboarding.reset onboarding

`operation_foundation_desk_record_definitions_module_onboarding_business_behavior_module_onboarding_reset_onboarding`

**Inputs** self.

**State and service calls** call save on step · call save on self.

**Local steps**

- Evaluate Platform.only\_for(“Administrator”).
- Set self.is\_complete from 0.
- Set steps from self.get\_steps().
- For each step in steps.
  - Set step.is\_complete from 0.
  - Set step.is\_skipped from 0.
  - Evaluate step.save().
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get steps](operations-042.md#op-da77ae55d82519).

**Values supplied outside this operation** effective access from Platform.only\_for(“Administrator”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0177.json#L1425) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L881)

<a id="op-363db6b105e292"></a>
### Update completion

`operation_foundation_binding_foundation_desk_doctype_module_onboarding_module_onboarding_update_completion`

**Inputs** step.

**Record and data access** read “Onboarding Step Map” via get\_all · resolve a document from “Module Onboarding” via get\_doc.

**State and service calls** call db\_set on onboarding.

**Local steps**

- For each name in Platform.get\_all(“Onboarding Step Map”, filters = mapping(“parenttype” → “Module Onboarding”, “step” → step), pluck = “parent”).
  - Set onboarding from Platform.get\_doc(“Module Onboarding”, name).
  - Set done from onboarding.required\_steps\_done().
  - If bool(onboarding.is\_complete) differs from done.
    - Evaluate onboarding.db\_set(“is\_complete”, int(done)).
    - If done.
      - Evaluate capture\_onboarding\_completed(onboarding).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L267) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L725)
