# Forms, reports and navigation · operations 59

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Sidebar

[Record definition](../../../../data/record-types/sidebar.json)

<a id="op-41c2446ee6e7c0"></a>
### Sidebar.after rename

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_after_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**Local steps**

- Bind dependencies rename\_sidebar\_rows.
- Evaluate rename\_sidebar\_rows(old\_name, new\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L3186) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1029)

<a id="op-ecd9c6186fb988"></a>
### Sidebar.on trash

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_sidebar_on_trash`

**Inputs** self.

**Local steps**

- Bind dependencies remove\_sidebar\_rows.
- Evaluate remove\_sidebar\_rows(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L26) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L775) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L751)

<a id="op-cbfbf5f7a542c2"></a>
### Sidebar.validate item routes

`operation_foundation_binding_foundation_desk_doctype_sidebar_sidebar_sidebar_validate_item_routes`

**Inputs** self.

**Local steps**

- For each item in self.items.
  - Evaluate validate\_item\_route(item).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L27) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L752)

<a id="op-b09da82ad70cca"></a>
### Sidebar.clear stored keys

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_clear_stored_keys`

**Inputs** self.

**Local steps**

- For each item in self.items.
  - Set item.key from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L3275) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1032)

<a id="op-e0ac2515bac919"></a>
### Sidebar.validate app content

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_validate_application_content`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “{0} belongs to its app and can only be edited in developer mode. Customize the sidebar instead to change it  …”.format(Platform.bold((self.name or self.title))).

**Local steps**

- If Platform.conf.developer\_mode.
  - Return no value.
- If any(generator of Platform.flags.get(flag) for flag drawn from SYSTEM\_WRITE\_FLAGS).
  - Draw flag from SYSTEM\_WRITE\_FLAGS.
  - Return no value.
- Call the validation error handler Platform.throw(translated “{0} belongs to its app and can only be edited in developer mode. Customize the sidebar instead to change it  …”.format(Platform.bold((self.name or self.title))), title = translat ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.name → self.title.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L3340) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1043)

<a id="op-5fc5c1f7f68123"></a>
### Sidebar.validate standard

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_validate_standard`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A standard sidebar needs a module or an app to be written to.” · validation helper — translated “App {0} is not installed, so a standard sidebar cannot be written to it.”.format(Platform.bold(self.app)) · validation helper — translated “Module {0} has no folder in an app, so a standard sidebar cannot be written to it.”.format(Platform.bold(self.module)).

**Local steps**

- If not self.standard.
  - Return no value.
- If not any(generator of self.has\_value\_changed(field) for field drawn from tuple(“standard”, “module”, “app”)).
  - Draw field from tuple(“standard”, “module”, “app”).
  - Return no value.
- Evaluate check\_developer\_mode().
- If not self.module.
  - If not self.app.
    - Call the validation error handler Platform.throw(translated “A standard sidebar needs a module or an app to be written to.”).
  - If self.app does not belong to Platform.get\_installed\_apps().
    - Call the validation error handler Platform.throw(translated “App {0} is not installed, so a standard sidebar cannot be written to it.”.format(Platform.bold(self.app))).
  - Return no value.
- Attempt the following.
  - Evaluate Platform.get\_module\_path(self.module).
- On failure (tuple(Platform.DoesNotExistError, ImportError)).
  - Evaluate Platform.clear\_last\_message().
  - Call the validation error handler Platform.throw(translated “Module {0} has no folder in an app, so a standard sidebar cannot be written to it.”.format(Platform.bold(self.module))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L3579) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1044)

<a id="op-37d93d1d85710f"></a>
### Sidebar.on update

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.remove\_previous\_export().
- Evaluate self.export\_sidebar().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove previous export](operations-059.md#op-1a478d2a0f2763), [export sidebar](operations-059.md#op-115312dc5b36be).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L4097) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1038)

<a id="op-1a478d2a0f2763"></a>
### Sidebar.remove previous export

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_remove_previous_export`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies os.
- Bind dependencies shutil.
- Set previous from self.get\_doc\_before\_save().
- If (not Platform.conf.developer\_mode or not previous or previous.name equals self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.conf.developer\_mode → not previous → previous.name equals self.name.
  - Return no value.
- If (previous.standard and previous.is\_exported()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous.standard → previous.is\_exported().
  - Evaluate shutil.rmtree(os.path.dirname(previous.exported\_file\_path()), ignore\_errors = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L4168) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1039)

<a id="op-115312dc5b36be"></a>
### Sidebar.export sidebar

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_export_sidebar`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies export\_to\_files.
- If (not self.standard or Platform.flags.in\_import or not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.standard → Platform.flags.in\_import → not Platform.conf.developer\_mode.
  - Return no value.
- If self.module.
  - Evaluate export\_to\_files(record\_list = list(list(“Sidebar”, self.name)), record\_module = self.module).
- Otherwise.
  - If self.app.
    - Evaluate export\_to\_files(record\_list = list(list(“Sidebar”, self.name)), record\_app = self.app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L4412) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1034)

<a id="op-9d8f805378549e"></a>
### Sidebar.exported file path

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_exported_file_path`

**Inputs** self.

**Declared result** str.

**Explicit results** exported\_file\_path(root, self.doctype, self.name).

**Local steps**

- Bind dependencies export\_root, exported\_file\_path.
- Set root from export\_root(module = self.module) when self.module, otherwise export\_root(record\_app = self.app).
  - Value choice on self.module — true gives export\_root(module = self.module), false gives export\_root(record\_app = self.app).
- Return exported\_file\_path(root, self.doctype, self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L4667) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1035)

<a id="op-63b845eee32380"></a>
### Sidebar.is exported

`operation_foundation_desk_record_definitions_sidebar_business_behavior_sidebar_is_exported`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · os.path.exists(self.exported\_file\_path()).

**Local steps**

- Bind dependencies os.
- If (self.is\_new() or not (self.module or self.app)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not (self.module or self.app).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.module → self.app.
  - Return false.
- Attempt the following.
  - Return os.path.exists(self.exported\_file\_path()).
- On failure (tuple(Platform.DoesNotExistError, ImportError)).
  - Evaluate Platform.clear\_last\_message().
  - Return false.

**Methods declared on this owner** [exported file path](operations-059.md#op-9d8f805378549e).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L4822) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L581) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1037)

<a id="op-6f5d9af4c73810"></a>
### Mark as standard

`operation_foundation_desk_record_definitions_sidebar_business_behavior_mark_as_standard`

**Inputs** module.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**State and service calls** savepoint savepoint · call save on doc · rollback · release savepoint savepoint · msgprint with translated “{0} is now standard and exported to {1}.”.format(Platform.bold(doc.name), Platform.bold(doc.app)).

**Explicit results** doc.name.

**Explicit failure paths** validation helper — translated “Could not write {0} to {1}. Left unchanged.”.format(Platform.bold(doc.name), Platform.bold((doc.app or “-”))) · propagate active failure.

**Local steps**

- Evaluate check\_developer\_mode().
- Set doc from materialize\_base(module).
- If (doc.standard and doc.is\_exported()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.standard → doc.is\_exported().
  - Return doc.name.
- Set savepoint from “mark\_sidebar\_standard”.
- Evaluate Platform.db.savepoint(savepoint).
- Attempt the following.
  - Set doc.standard from 1.
  - Set doc.app from get\_module\_placement(module).
  - Evaluate doc.save().
  - If not doc.is\_exported().
    - Call the validation error handler Platform.throw(translated “Could not write {0} to {1}. Left unchanged.”.format(Platform.bold(doc.name), Platform.bold((doc.app or “-”)))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.app → “-”.
- On failure (Exception).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Propagate the active failure.
- Evaluate Platform.db.release\_savepoint(savepoint).
- Evaluate Platform.msgprint(translated “{0} is now standard and exported to {1}.”.format(Platform.bold(doc.name), Platform.bold(doc.app)), alert = true, indicator = “green”).
- Return doc.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L5028) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1016)

<a id="op-f27f08aa186230"></a>
### Unmark as standard

`operation_foundation_desk_record_definitions_sidebar_business_behavior_unmark_as_standard`

**Inputs** sidebar.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Record and data access** read “Sidebar” via exists · resolve a document from “Sidebar” via get\_doc.

**State and service calls** msgprint with translated “{0} is no longer standard; its exported file has been removed.”.format(Platform.bold(doc.name)).

**Explicit results** no value.

**Local steps**

- Bind dependencies os.
- Bind dependencies shutil.
- Evaluate check\_developer\_mode().
- If not Platform.db.exists(“Sidebar”, sidebar).
  - Return no value.
- Set doc from Platform.get\_doc(“Sidebar”, sidebar).
- If not doc.standard.
  - Return no value.
- Set path from doc.exported\_file\_path() when doc.is\_exported(), otherwise no value.
  - Value choice on doc.is\_exported() — true gives doc.exported\_file\_path(), false gives no value.
- Evaluate doc.delete().
- If path.
  - Evaluate shutil.rmtree(os.path.dirname(path), ignore\_errors = true).
- Evaluate Platform.msgprint(translated “{0} is no longer standard; its exported file has been removed.”.format(Platform.bold(doc.name)), alert = true, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L5651) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1047)

<a id="op-23a609b95d69d6"></a>
### Check developer mode

`operation_foundation_desk_record_definitions_sidebar_business_behavior_check_developer_mode`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Enable developer mode to change whether a sidebar is standard -- it is backed by a file in its app.”.

**Local steps**

- If Platform.conf.developer\_mode.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Enable developer mode to change whether a sidebar is standard -- it is backed by a file in its app.”, title = translated “Not Editable”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L6079) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L992)

<a id="op-7760a7a3a08fb8"></a>
### Check shell

`operation_foundation_desk_record_definitions_sidebar_business_behavior_check_shell`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** module, shell.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L6189) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L993)

<a id="op-158bdeac3d097f"></a>
### Get sidebar

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_sidebar`

**Inputs** module.

**Declared result** “Sidebar \| None”.

**Record and data access** read “Sidebar” via get\_value · resolve a document from “Sidebar” via get\_doc.

**Explicit results** Platform.get\_doc(“Sidebar”, name) when name, otherwise no value.

**Local steps**

- Set name from Platform.db.get\_value(“Sidebar”, mapping(“name” → module, “module” → module)).
- Return Platform.get\_doc(“Sidebar”, name) when name, otherwise no value.
  - Value choice on name — true gives Platform.get\_doc(“Sidebar”, name), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L6549) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1010)

<a id="op-649f4915d40fce"></a>
### Get module shell

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_module_shell`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** module, shell.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0181.json#L6715) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1006)

<a id="op-a378312b8dce3f"></a>
### Materialize base

`operation_foundation_desk_record_definitions_sidebar_business_behavior_materialize_base`

**Inputs** module.

**Declared result** “Sidebar”.

**State and service calls** request new\_doc for “Sidebar”.

**Explicit results** doc.

**Local steps**

- Set doc from get\_sidebar(module).
- If (doc and doc.items).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → doc.items.
  - Return doc.
- Set base from get\_computed\_base(module).
- If not doc.
  - Set doc from Platform.new\_doc(“Sidebar”).
  - Set doc.module from module.
  - Set doc.title from base.title.
  - Set doc.header\_icon from base.header\_icon.
- For each row in base.rows.
  - Evaluate doc.append(“items”, dict(row)).
- Return doc.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1017)

<a id="op-5d4ea0ef5e7462"></a>
### Get app sidebar layer

`operation_foundation_desk_record_definitions_sidebar_business_behavior_get_application_sidebar_layer`

**Inputs** module, shell = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**State and service calls** request new\_doc for “Workspace”.

**Explicit results** list of mapping(expand item, “hidden” → int((item.get(“hidden”) or 0)), “added” → 0) for item drawn from items.

**Local steps**

- Bind dependencies check\_module.
- Evaluate check\_developer\_mode().
- Evaluate check\_module(module).
- Evaluate check\_shell(module, shell).
- Set base from get\_module\_base(module, shell).
- Set items from filter\_sidebar\_items(base.rows, Platform.new\_doc(“Workspace”), check\_permission = false).
- Return list of mapping(expand item, “hidden” → int((item.get(“hidden”) or 0)), “added” → 0) for item drawn from items.
  - Draw item from items.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“hidden”) → 0.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L310) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1000)

<a id="op-5d28c8483dfdc1"></a>
### Save app sidebar

`operation_foundation_desk_record_definitions_sidebar_business_behavior_save_application_sidebar`

**Inputs** module, items, shell = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**State and service calls** call save on doc.

**Explicit results** module\_payload().

**Local steps**

- Bind dependencies check\_module, module\_payload.
- Evaluate check\_developer\_mode().
- Evaluate check\_module(module).
- Evaluate check\_shell(module, shell).
- If isinstance(items, str).
  - Set items from json.loads(items).
- Set doc from app\_document(module, shell).
- Evaluate doc.set(“items”, list()).
- For each row in items.
  - Evaluate doc.append(“items”, app\_item(row)).
- Set doc.standard from 1.
- Set doc.app from get\_module\_placement(module).
- Evaluate doc.save().
- Return module\_payload().

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L679) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1028)

<a id="op-29b2f37323e91d"></a>
### Reset app sidebar

`operation_foundation_desk_record_definitions_sidebar_business_behavior_reset_application_sidebar`

**Inputs** module, shell = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** module\_payload().

**Local steps**

- Bind dependencies check\_module, module\_payload.
- Evaluate check\_developer\_mode().
- Evaluate check\_module(module).
- Evaluate check\_shell(module, shell).
- Set document from get\_module\_shell(module, shell).
- If document.
  - Evaluate unmark\_as\_standard(document.name).
- Return module\_payload().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L1116) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1024)

<a id="op-bba3e808651b8a"></a>
### App document

`operation_foundation_desk_record_definitions_sidebar_business_behavior_application_document`

**Inputs** module, shell = no value.

**Declared result** “Sidebar”.

**Explicit results** (get\_module\_shell(module, shell) or materialize\_base(module)).

**Local steps**

- Return (get\_module\_shell(module, shell) or materialize\_base(module)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_module\_shell(module, shell) → materialize\_base(module).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L1352) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L987)

<a id="op-9e1a2b3b1e1e86"></a>
### App item

`operation_foundation_desk_record_definitions_sidebar_business_behavior_application_item`

**Inputs** row.

**Declared result** dict.

**Explicit results** item.

**Local steps**

- Set item from mapping of field → row.get(field) for field drawn from ARRANGED\_ITEM\_FIELDS.
  - Draw field from ARRANGED\_ITEM\_FIELDS.
- Set item at “navigate\_to\_tab” from row.get(“tab”).
- Set item at “hidden” from int(bool(row.get(“hidden”))).
- Set item at “added” from 0.
- Return item.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L1465) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L988)

<a id="op-45b16e84f77554"></a>
### Is linked

`operation_foundation_desk_record_definitions_sidebar_business_behavior_is_linked`

**Inputs** item.

**Declared result** bool.

**Explicit results** bool((item.get(“link\_to”) or item.get(“url”))).

**Local steps**

- Return bool((item.get(“link\_to”) or item.get(“url”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“link\_to”) → item.get(“url”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0182.json#L1695) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1013)
