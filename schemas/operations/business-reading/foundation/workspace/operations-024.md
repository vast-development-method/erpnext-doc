# Forms, reports and navigation · operations 24

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dock

[Record definition](../../../../data/record-types/dock.json)

<a id="op-0e7f6a7de52399"></a>
### Dock.clear dock cache

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_clear_dock_cache`

**Inputs** self.

**Local steps**

- Evaluate drop\_dock\_caches(self.user).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3115) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L685)

<a id="op-62ea64b3e87add"></a>
### Dock.export dock

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_export_dock`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies export\_to\_files.
- If (not self.standard or Platform.flags.in\_import or not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.standard → Platform.flags.in\_import → not Platform.conf.developer\_mode.
  - Return no value.
- Evaluate export\_to\_files(record\_list = list(list(“Dock”, self.name)), record\_app = self.app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3171) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L686)

<a id="op-96a6130bacba0d"></a>
### Dock.exported file path

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_exported_file_path`

**Inputs** self.

**Declared result** str.

**Explicit results** exported\_file\_path(export\_root(record\_app = self.app), self.doctype, self.name).

**Local steps**

- Bind dependencies export\_root, exported\_file\_path.
- Return exported\_file\_path(export\_root(record\_app = self.app), self.doctype, self.name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3334) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L687)

<a id="op-e3ffacff7f069a"></a>
### Dock.is exported

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_is_exported`

**Inputs** self.

**Declared result** bool.

**Explicit results** false · os.path.exists(self.exported\_file\_path()).

**Local steps**

- Bind dependencies os.
- If (self.is\_new() or not self.app).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → not self.app.
  - Return false.
- Attempt the following.
  - Return os.path.exists(self.exported\_file\_path()).
- On failure (tuple(Platform.DoesNotExistError, ImportError)).
  - Evaluate Platform.clear\_last\_message().
  - Return false.

**Methods declared on this owner** [exported file path](operations-024.md#op-96a6130bacba0d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3441) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L688)

<a id="op-ae96b612552f45"></a>
### On doctype update

`operation_foundation_desk_record_definitions_dock_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_unique on “Dock”.

**Local steps**

- Evaluate Platform.db.add\_unique(“Dock”, tuple(“app”, “user”, “standard”), constraint\_name = “unique\_layer\_address”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3633) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L197) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L718)

<a id="op-05560b69e39cbb"></a>
### Mark as standard

`operation_foundation_desk_record_definitions_dock_business_behavior_mark_as_standard`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Record and data access** resolve a document from “Dock” via get\_doc.

**State and service calls** request new\_doc for “Dock” · savepoint savepoint · call save on doc · rollback · release savepoint savepoint · 1 additional forms in the steps below.

**Explicit results** doc.name.

**Explicit failure paths** validation helper — translated “There is nothing to export for {0}. Put some entries on its dock first.”.format(Platform.bold(app)) · validation helper — translated “Could not write {0}'s dock to it. Left unchanged.”.format(Platform.bold(app)) · propagate active failure.

**Local steps**

- Set app from check\_docked\_app(app).
- Evaluate check\_developer\_mode().
- Set doc from get\_dock(app, standard = 1).
- If doc.
  - Set doc from Platform.get\_doc(“Dock”, doc.name).
  - If doc.is\_exported().
    - Return doc.name.
- Otherwise.
  - Set rail from resolve\_app\_dock(app, gated = false).
  - If not rail.
    - Call the validation error handler Platform.throw(translated “There is nothing to export for {0}. Put some entries on its dock first.”.format(Platform.bold(app))).
  - Set doc from Platform.new\_doc(“Dock”).
  - Set doc.app from app.
  - For each row in rail.
    - Evaluate doc.append(“items”, mapping of field → row.get(field) for field drawn from DOCK\_ITEM\_FIELDS).
      - Draw field from DOCK\_ITEM\_FIELDS.
- Set savepoint from “mark\_dock\_standard”.
- Evaluate Platform.db.savepoint(savepoint).
- Attempt the following.
  - Set doc.standard from 1.
  - Evaluate doc.save().
  - If not doc.is\_exported().
    - Call the validation error handler Platform.throw(translated “Could not write {0}'s dock to it. Left unchanged.”.format(Platform.bold(app))).
- On failure (Exception).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Propagate the active failure.
- Evaluate Platform.db.release\_savepoint(savepoint).
- Evaluate Platform.msgprint(translated “{0}'s dock is now standard and exported to the app.”.format(Platform.bold(app)), alert = true, indicator = “green”).
- Return doc.name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L3730) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L195) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L716)

<a id="op-2be6e1f7dd64da"></a>
### Unmark as standard

`operation_foundation_desk_record_definitions_dock_business_behavior_unmark_as_standard`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**State and service calls** request delete\_doc for “Dock” · msgprint with translated “{0} now has no rail; its exported dock has been removed.”.format(Platform.bold(app)).

**Explicit results** no value.

**Local steps**

- Bind dependencies os.
- Bind dependencies shutil.
- Set app from check\_docked\_app(app).
- Evaluate check\_developer\_mode().
- Set doc from get\_dock(app, standard = 1).
- If not doc.
  - Return no value.
- Set path from doc.exported\_file\_path() when doc.is\_exported(), otherwise no value.
  - Value choice on doc.is\_exported() — true gives doc.exported\_file\_path(), false gives no value.
- Evaluate Platform.delete\_doc(“Dock”, doc.name, force = true).
- If path.
  - Evaluate shutil.rmtree(os.path.dirname(path), ignore\_errors = true).
- Evaluate Platform.msgprint(translated “{0} now has no rail; its exported dock has been removed.”.format(Platform.bold(app)), alert = true, indicator = “orange”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L4582) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L736)

<a id="op-2bc46aad43b0f9"></a>
### Check developer mode

`operation_foundation_desk_record_definitions_dock_business_behavior_check_developer_mode`

**Inputs** no declared parameters.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Enable developer mode to change whether a dock is standard -- it is backed by a file in its app.”.

**Local steps**

- If Platform.conf.developer\_mode.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Enable developer mode to change whether a dock is standard -- it is backed by a file in its app.”, title = translated “Not Editable”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L5011) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L679)

<a id="op-5002620771f5fd"></a>
### Rename sidebar rows

`operation_foundation_desk_record_definitions_dock_business_behavior_rename_sidebar_rows`

**Inputs** old\_name, new\_name.

**Declared result** no value.

**Record and data access** read “Dock Item” via get\_all · read “Dock” via get\_all.

**State and service calls** request set\_value on “Dock Item”.

**Explicit results** no value.

**Local steps**

- Set named from mapping(“parenttype” → “Dock”, “link\_type” → “Sidebar”).
- Set layers from Platform.get\_all(“Dock Item”, filters = mapping(expand named, “link\_to” → tuple(“in”, tuple(old\_name, new\_name))), pluck = “parent”, distinct = true).
- If not layers.
  - Return no value.
- Evaluate Platform.db.set\_value(“Dock Item”, mapping(expand named, “link\_to” → old\_name), “link\_to”, new\_name, update\_modified = false).
- For each layer in Platform.get\_all(“Dock”, filters = mapping(“name” → list(“in”, layers)), fields = list(“name”, “user”)).
  - Evaluate Platform.clear\_document\_cache(“Dock”, layer.name).
  - Evaluate drop\_dock\_caches(layer.user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L5121) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L723)

<a id="op-694cf87704d7d1"></a>
### Remove sidebar rows

`operation_foundation_binding_foundation_desk_doctype_dock_dock_remove_sidebar_rows`

**Inputs** name.

**Declared result** no value.

**Record and data access** read “Dock Item” via get\_all · read “Dock” via get\_all.

**State and service calls** request delete on “Dock Item”.

**Explicit results** no value.

**Local steps**

- Set named from mapping(“parenttype” → “Dock”, “link\_type” → “Sidebar”, “link\_to” → name).
- Set layers from Platform.get\_all(“Dock Item”, filters = named, pluck = “parent”, distinct = true).
- If not layers.
  - Return no value.
- Evaluate Platform.db.delete(“Dock Item”, named).
- For each layer in Platform.get\_all(“Dock”, filters = mapping(“name” → list(“in”, layers)), fields = list(“name”, “user”)).
  - Evaluate Platform.clear\_document\_cache(“Dock”, layer.name).
  - Evaluate drop\_dock\_caches(layer.user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L229) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L687)

<a id="op-50008212358b13"></a>
### Drop dock caches

`operation_foundation_desk_record_definitions_dock_business_behavior_drop_dock_caches`

**Inputs** user.

**Declared result** no value.

**Local steps**

- Evaluate Platform.cache.delete\_value(DOCK\_LAYERS\_CACHE\_KEY).
- Set Platform.local.dock\_cache from mapping(“app\_dock” → mapping(), “mounts” → no value).
- If user.
  - Evaluate Platform.cache.hdel(“bootinfo”, user).
- Otherwise.
  - Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L5610) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L179) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L700)

<a id="op-6e66918fd65d09"></a>
### Request cache for docks

`operation_foundation_desk_record_definitions_dock_business_behavior_request_cache_for_docks`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** Platform.local.dock\_cache.

**Local steps**

- If not hasattr(Platform.local, “dock\_cache”).
  - Set Platform.local.dock\_cache from mapping(“app\_dock” → mapping(), “mounts” → no value).
- Return Platform.local.dock\_cache.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L5793) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L724)

<a id="op-0bd7fa0c71768c"></a>
### Dock records

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_records`

**Inputs** no declared parameters.

**Declared result** list at dict.

**Record and data access** read “Dock” via get\_all.

**Explicit results** records.

**Local steps**

- Set records from Platform.cache.get\_value(DOCK\_LAYERS\_CACHE\_KEY).
- If records is identical to no value.
  - Set records from list of mapping(“name” → row.name, “app” → row.app, “user” → (row.user or SITE\_LAYER), “standard” → int((row.standard or 0)), …) for row drawn from Platform.get\_all(“Dock”, fields = list(“name”, “app”, “us ….
    - Draw row from Platform.get\_all(“Dock”, fields = list(“name”, “app”, “user”, “standard”, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.user → SITE\_LAYER.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.standard → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.mount\_on → no value.
  - Evaluate Platform.cache.set\_value(DOCK\_LAYERS\_CACHE\_KEY, records).
- Return records.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L5910) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L692)

<a id="op-cfae8742e7c9b9"></a>
### Get dock layers

`operation_foundation_desk_record_definitions_dock_business_behavior_get_dock_layers`

**Inputs** no declared parameters.

**Declared result** dict at tuple(tuple at tuple(str, str, int), str).

**Explicit results** mapping of tuple(row at “app”, row at “user”, row at “standard”) → row at “name” for row drawn from dock\_records().

**Local steps**

- Return mapping of tuple(row at “app”, row at “user”, row at “standard”) → row at “name” for row drawn from dock\_records().
  - Draw row from dock\_records().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L6294) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L187) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L708)

<a id="op-7b5f607e873937"></a>
### Mounted apps

`operation_foundation_desk_record_definitions_dock_business_behavior_mounted_apps`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Explicit results** memo at “mounts” · mounts.

**Local steps**

- Set memo from request\_cache\_for\_docks().
- If memo at “mounts” is distinct from no value.
  - Return memo at “mounts”.
- Set shipped from mapping of row at “app” → row for row drawn from dock\_records() where row at “standard”.
  - Draw row from dock\_records(), keep a combination only if (row at “standard”).
- Set installed from Platform.get\_installed\_apps().
- Set mounts from mapping().
- For each tuple(app, row) in shipped.items().
  - Set host from row at “mount\_on”.
  - If (not host or host equals app or host does not belong to installed or app does not belong to installed).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not host → host equals app → host does not belong to installed → app does not belong to installed.
    - Continue with the next iteration or loop test.
  - If (host does not belong to shipped or not get\_app\_dock(host)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in host does not belong to shipped → not get\_app\_dock(host).
    - Continue with the next iteration or loop test.
  - If not get\_app\_dock(app).
    - Continue with the next iteration or loop test.
  - Set mounts at app from host.
- Set memo at “mounts” from mounts.
- Return mounts.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L130) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L196) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L717)

<a id="op-68f08e4bf240de"></a>
### Get dock

`operation_foundation_desk_record_definitions_dock_business_behavior_get_dock`

**Inputs** app, user = no value, standard = 0.

**Declared result** “Dock \| None”.

**Record and data access** resolve a document from “Dock” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Dock”, name) when name, otherwise no value.

**Local steps**

- Set name from get\_dock\_layers().get(tuple(app, (user or SITE\_LAYER), standard)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → SITE\_LAYER.
- Return Platform.get\_cached\_doc(“Dock”, name) when name, otherwise no value.
  - Value choice on name — true gives Platform.get\_cached\_doc(“Dock”, name), false gives no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Dock”, name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0166.json#L6929) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L186) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L707)

<a id="op-26681ddc233a17"></a>
### Stored row

`operation_foundation_desk_record_definitions_dock_business_behavior_stored_row`

**Inputs** row.

**Declared result** dict.

**Explicit results** mapping(expand mapping of field → (row.get(field) or no value) for field drawn from DESTINATION\_FIELDS, “icon” → (row.get(“icon”) or no value), “title” → (row.get(“title”) or no value), “added” → int((row. ….

**Local steps**

- Return mapping(expand mapping of field → (row.get(field) or no value) for field drawn from DESTINATION\_FIELDS, “icon” → (row.get(“icon”) or no value), “title” → (row.get(“title”) or no value), “added” → int((row. ….
  - Draw field from DESTINATION\_FIELDS.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(field) → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“icon”) → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“title”) → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“added”) → 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“hidden”) → 0.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L735)

<a id="op-8aa45c48d77ebe"></a>
### Points somewhere

`operation_foundation_desk_record_definitions_dock_business_behavior_points_somewhere`

**Inputs** entry.

**Declared result** bool.

**Explicit results** bool(entry.get(“url”)) · bool((entry.get(“link\_type”) and entry.get(“link\_to”))).

**Local steps**

- If entry.get(“link\_type”) equals “URL”.
  - Return bool(entry.get(“url”)).
- Return bool((entry.get(“link\_type”) and entry.get(“link\_to”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry.get(“link\_type”) → entry.get(“link\_to”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L309) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L721)

<a id="op-029553f41da98e"></a>
### Dock rows

`operation_foundation_desk_record_definitions_dock_business_behavior_dock_rows`

**Inputs** dock.

**Declared result** list at dict.

**Explicit results** list() · list of row for row drawn from rows where points\_somewhere(row).

**Local steps**

- If not dock.
  - Return list().
- Set rows from list of stored\_row(row) for row drawn from dock.items.
  - Draw row from dock.items.
- Return list of row for row drawn from rows where points\_somewhere(row).
  - Draw row from rows, keep a combination only if (points\_somewhere(row)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L492) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L693)

<a id="op-38ec093480ed8f"></a>
### Get app dock

`operation_foundation_desk_record_definitions_dock_business_behavior_get_application_dock`

**Inputs** app.

**Declared result** list at dict.

**Explicit results** memo at app.

**Local steps**

- Set memo from request\_cache\_for\_docks() at “app\_dock”.
- If app does not belong to memo.
  - Set memo at app from build\_app\_dock(app).
- Return memo at app.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L665) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L183) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L704)

<a id="op-96c4308e6862ca"></a>
### Build app dock

`operation_foundation_desk_record_definitions_dock_business_behavior_build_application_dock`

**Inputs** app.

**Declared result** list at dict.

**Explicit results** list() · rows.

**Local steps**

- Set shipped from get\_dock(app, standard = 1).
- If not shipped.
  - Return list().
- Set tuple(rows, seen) from tuple(list(), set()).
- For each row in dock\_rows(shipped).
  - Set key from dock\_key(row).
  - If key belongs to seen.
    - Continue with the next iteration or loop test.
  - Evaluate seen.add(key).
  - Evaluate rows.append(row).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L812) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L678)

<a id="op-b7ccb58d7c385d"></a>
### Get app base

`operation_foundation_desk_record_definitions_dock_business_behavior_get_application_base`

**Inputs** app.

**Declared result** list at dict.

**Explicit results** own · rows.

**Local steps**

- Set own from get\_app\_dock(app).
- Set mounts from mounted\_apps().
- If app does not belong to set(mounts.values()).
  - Return own.
- Set tuple(rows, seen) from tuple(list(own), set of dock\_key(row) for row drawn from own).
  - Draw row from own.
- For each companion in sorted(mounts, key = Platform.get\_installed\_apps().index).
  - If mounts at companion differs from app.
    - Continue with the next iteration or loop test.
  - For each row in get\_app\_dock(companion).
    - Set key from dock\_key(row).
    - If key belongs to seen.
      - Continue with the next iteration or loop test.
    - Evaluate seen.add(key).
    - Evaluate rows.append(row).
- Return rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L129) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L182) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L703)

<a id="op-fe08a6ed62cb52"></a>
### Get app entry set

`operation_foundation_desk_record_definitions_dock_business_behavior_get_application_entry_set`

**Inputs** app.

**Declared result** list at dict.

**Explicit results** list of rail\_entry(row) for row drawn from get\_app\_base(app) where is\_reachable(row).

**Local steps**

- Return list of rail\_entry(row) for row drawn from get\_app\_base(app) where is\_reachable(row).
  - Draw row from get\_app\_base(app), keep a combination only if (is\_reachable(row)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L1533) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L185) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L706)

<a id="op-65b45944be3928"></a>
### Apps screen sort key

`operation_foundation_desk_record_definitions_dock_business_behavior_apps_screen_sort_key`

**Inputs** no declared parameters.

**Explicit results** deferred anonymous expression.

**Local steps**

- Bind dependencies DEFAULT\_APP\_SEQUENCE\_ID.
- Set installed from Platform.get\_installed\_apps().
- Bind local operation sequence for subsequent calls.
- Return deferred anonymous expression.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L125) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L676)
