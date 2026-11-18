# Record lifecycle and persistence · operations 95

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Submission queue

[Record definition](../../../../data/record-types/submission_queue.json)

<a id="op-a347eeeb623dfd"></a>
### Format tb

`operation_foundation_core_record_definitions_submission_queue_business_behavior_format_tb`

**Inputs** traceback = no value.

**Explicit results** no value · traceback.strip().split(whitespace '\\n') at negative 1.

**Local steps**

- If not traceback.
  - Return no value.
- Return traceback.strip().split(whitespace '\\n') at negative 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L3902) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L594)

## Service · Sync

<a id="op-a14f20b6664a61"></a>
### Sync all

`operation_foundation_model_sync_business_behavior_sync_all`

**Inputs** force = 0, reset\_permissions = false.

**Local steps**

- Evaluate \_patch\_mode(true).
- For each app in Platform.get\_installed\_apps().
  - Evaluate sync\_for(app, force, reset\_permissions = reset\_permissions).
- Evaluate \_patch\_mode(false).
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0289.json#L6952) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1300)

<a id="op-a17301b4892eb8"></a>
### Sync for

`operation_foundation_model_sync_business_behavior_sync_for`

**Inputs** app\_name, force = 0, reset\_permissions = false.

**State and service calls** commit.

**Local steps**

- Set files from list().
- If app\_name equals “Platform”.
  - Set Platform\_PATH from Platform.get\_app\_path(“Platform”).
  - For each core\_module in list(“docfield”, “docperm”, “doctype\_action”, “doctype\_link”, …).
    - Evaluate files.append(os.path.join(Platform\_PATH, “core”, “doctype”, core\_module, …)).
  - For each dt in list(“user”, “docshare”, “custom\_docperm”, “docperm”, …).
    - Evaluate files.append(os.path.join(Platform\_PATH, “core”, “doctype”, dt, …)).
  - For each custom\_module in list(“custom\_field”, “property\_setter”).
    - Evaluate files.append(os.path.join(Platform\_PATH, “custom”, “doctype”, custom\_module, …)).
  - For each website\_module in list(“web\_form”, “web\_template”, “web\_form\_field”, “portal\_menu\_item”).
    - Evaluate files.append(os.path.join(Platform\_PATH, “website”, “doctype”, website\_module, …)).
  - For each desk\_module in list(“number\_card”, “dashboard\_chart”, “dashboard”, “onboarding\_permission”, …).
    - Evaluate files.append(os.path.join(Platform\_PATH, “desk”, “doctype”, desk\_module, …)).
  - For each tuple(module\_name, document\_type) in IMPORTABLE\_DOCTYPES.
    - Set file from os.path.join(Platform\_PATH, module\_name, “doctype”, document\_type, …).
    - If file does not belong to files.
      - Evaluate files.append(file).
- For each module\_name in (Platform.local.app\_modules.get(app\_name) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.app\_modules.get(app\_name) → list().
  - Set folder from os.path.dirname(Platform.get\_module(((app\_name + “.”) + module\_name)).\_\_file\_\_).
  - Set files from get\_doc\_files(files = files, start\_path = folder).
- Set files from get\_doc\_files(files = files, start\_path = Platform.get\_app\_path(app\_name), doctypes = APP\_ROOTED\_DOCTYPES).
- Set l from len(files).
- If l.
  - For each tuple(i, doc\_path) in enumerate(files).
    - Set imported from import\_file\_by\_path(doc\_path, force = force, ignore\_version = true, reset\_permissions = reset\_permissions).
    - If imported.
      - Evaluate Platform.db.commit(chain = true).
    - Evaluate update\_progress\_bar(formatted text Updating DocTypes for {app\_name}, i, l).
  - Evaluate print().
- Evaluate import\_desktop\_icon\_fixtures(app\_name, force = force).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1301)

<a id="op-5c47478672554b"></a>
### Get doc files

`operation_foundation_model_sync_business_behavior_get_record_files`

**Inputs** files, start\_path, doctypes = no value.

**Explicit results** files.

**Local steps**

- Set files from (files or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in files → list().
- Set general\_walk from doctypes is identical to no value.
- If general\_walk.
  - Set doctypes from (IMPORTABLE\_DOCTYPES + list of tuple(no value, Platform.scrub(dt)) for dt drawn from Platform.get\_hooks(“importable\_doctypes”)).
    - Draw dt from Platform.get\_hooks(“importable\_doctypes”).
- For each tuple(\_module, doctype) in doctypes.
  - Set doctype\_path from os.path.join(start\_path, doctype).
  - If os.path.exists(doctype\_path).
    - For each docname in os.listdir(doctype\_path).
      - If os.path.isdir(os.path.join(doctype\_path, docname)).
        - Set doc\_path from (os.path.join(doctype\_path, docname, docname) + “.json”).
        - If os.path.exists(doc\_path).
          - If doc\_path does not belong to files.
            - Evaluate files.append(doc\_path).
- If not general\_walk.
  - Return files.
- For each folder in tuple(“list\_filter”, “kanban\_board”).
  - For each doc\_path in glob.glob(os.path.join(start\_path, “doctype”, “\*”, folder, …)).
    - If doc\_path does not belong to files.
      - Evaluate files.append(doc\_path).
- For each doc\_path in glob.glob(os.path.join(start\_path, “doctype\_settings\_map”, “\*.json”)).
  - If doc\_path does not belong to files.
    - Evaluate files.append(doc\_path).
- Return files.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“importable\_doctypes”).

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L13) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1297)

<a id="op-05ad2777dea3a5"></a>
### Remove orphan doctypes

`operation_foundation_model_sync_business_behavior_remove_orphan_record_types`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all.

**State and service calls** request delete\_doc for “DocType” · commit.

**Explicit results** no value.

**Local steps**

- Set doctype\_names from Platform.get\_all(“DocType”, mapping(“custom” → 0), pluck = “name”).
- Set known\_doctypes from create\_entity\_file\_map(list(“DocType”)) at “DocType”.
- Set orphan\_doctypes from list of doctype for doctype drawn from doctype\_names where doctype does not belong to known\_doctypes.
  - Draw doctype from doctype\_names, keep a combination only if (doctype does not belong to known\_doctypes).
- If not orphan\_doctypes.
  - Return no value.
- Evaluate print(formatted text Orphaned DocType(s) found: {“, ”.join(orphan\_doctypes)}).
- For each tuple(i, name) in enumerate(orphan\_doctypes).
  - Evaluate Platform.delete\_doc(“DocType”, name, force = true, ignore\_missing = true).
  - Evaluate update\_progress\_bar(“Deleting orphaned DocTypes”, i, len(orphan\_doctypes)).
- Evaluate Platform.db.commit().
- Evaluate print().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L2166) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1299)

<a id="op-be55fe7916d4f7"></a>
### Remove orphan entities

`operation_foundation_model_sync_business_behavior_remove_orphan_entities`

**Inputs** entity\_types = no value.

**Record and data access** read entity via get\_all · read app\_entity via get\_all.

**State and service calls** request delete\_doc for entity · commit · request delete\_doc for app\_entity · request delete on app\_entity.

**Explicit results** no value.

**Local steps**

- Set entities from list(ORPHANABLE\_ENTITIES).
- Set entity\_filter\_map from mapping(“Workspace” → mapping(“public” → 1, “standard” → 1), “Page” → mapping(“standard” → “Yes”), “Report” → mapping(“is\_standard” → “Yes”), “Dashboard” → mapping(“is\_standard” → true), …).
- If entity\_types.
  - Set entities from entity\_types when isinstance(entity\_types, list), otherwise list(entity\_types).
    - Value choice on isinstance(entity\_types, list) — true gives entity\_types, false gives list(entity\_types).
- Set entity\_file\_map from create\_entity\_file\_map(entities).
- For each entity in entities.
  - Evaluate print(formatted text Removing orphan {entity}s).
  - Set all\_enitities from Platform.get\_all(entity, filters = entity\_filter\_map.get(entity), fields = list(“name”)).
  - For each tuple(i, w) in enumerate(all\_enitities).
    - Attempt the following.
      - Evaluate entity\_file\_map at entity at w.name.
    - On failure (KeyError).
      - Attempt the following.
        - Evaluate print(formatted text Deleting entity {entity} {w.name}).
        - Evaluate Platform.delete\_doc(entity, w.name, force = true, ignore\_missing = true).
        - Evaluate update\_progress\_bar(formatted text Deleting orphaned {entity}, i, len(all\_enitities)).
        - Evaluate print().
      - On failure (Exception) bound to e.
        - Evaluate print(formatted text Error occurred while deleting entity: {entity} {w.name}).
        - Evaluate print(e).
  - Evaluate Platform.db.commit().
- If (entity\_types and not set(entity\_types).issubset(set(APP\_LEVEL\_ENTITIES))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in entity\_types → not set(entity\_types).issubset(set(APP\_LEVEL\_ENTITIES)).
  - Return no value.
- For each app\_entity in APP\_LEVEL\_ENTITIES.
  - Evaluate print(formatted text Removing orphan {app\_entity}s).
  - Set all\_enitities from Platform.get\_all(app\_entity, filters = entity\_filter\_map.get(app\_entity), fields = list(“name”, “app”)).
  - For each tuple(i, entity) in enumerate(all\_enitities).
    - Attempt the following.
      - If entity.app.
        - Set app\_path from Platform.get\_app\_path(entity.app).
        - If not check\_if\_record\_exists(“app”, app\_path, app\_entity, entity.name).
          - Attempt the following.
            - Evaluate print(formatted text Deleting entity {app\_entity} {entity.name}).
            - Evaluate Platform.delete\_doc(app\_entity, entity.name, force = true, ignore\_missing = true).
            - Evaluate update\_progress\_bar(formatted text Deleting orphaned {app\_entity}, i, len(all\_enitities)).
            - Evaluate print().
          - On failure (Exception) bound to e.
            - Evaluate print(formatted text Error occurred while deleting entity: {app\_entity} {entity.name}).
            - Evaluate print(e).
    - On failure (ModuleNotFoundError) bound to e.
      - Evaluate print(e).
      - Evaluate print(formatted text Deleting entity {app\_entity} {entity.name}).
      - Evaluate Platform.db.delete(app\_entity, mapping(“name” → entity.name)).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L14) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1298)

<a id="op-2b184140e2c5ca"></a>
### Create entity file map

`operation_foundation_model_sync_business_behavior_create_entity_file_map`

**Inputs** entities.

**Explicit results** entity\_file\_map.

**Local steps**

- Bind dependencies read\_doc\_from\_file.
- Set entity\_file\_map from mapping().
- For each entity in entities.
  - Set entity\_file\_map at entity from mapping().
- For each app in Platform.get\_installed\_apps().
  - Set app\_path from Platform.get\_app\_path(app).
  - For each entity in entities.
    - Set entity\_folder from Platform.scrub(entity).
    - If entity\_folder equals “dashboard”.
      - Set entity\_folder from formatted text \*\_{entity\_folder}.
    - Set entity\_files from list(glob.glob(formatted text {app\_path}/\*\*/{entity\_folder}/\*\*/\*.json, recursive = true)).
    - For each file in entity\_files.
      - Set entity\_json from read\_doc\_from\_file(file).
      - If isinstance(entity\_json, dict).
        - Set entity\_file\_map at entity at entity\_json.get(“name”) from file.
      - Otherwise.
        - If isinstance(entity\_json, list).
          - If len(entity\_json) &gt; 0.
            - Set entity\_file\_map at entity at entity\_json at 0.get(“name”) from file.
- Return entity\_file\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L4323) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1295)

<a id="op-cc361749b80bdd"></a>
### Check if record exists

`operation_foundation_model_sync_business_behavior_check_if_record_exists`

**Inputs** type = no value, path = no value, entity\_type = no value, name = no value, module\_name = no value.

**Explicit results** true · false.

**Local steps**

- Set scrubbed\_name from Platform.scrub(name.lower()).
- Set scrubbed\_entity\_type from Platform.scrub(entity\_type.lower()).
- If (scrubbed\_entity\_type equals “dashboard” and module\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in scrubbed\_entity\_type equals “dashboard” → module\_name.
  - Set scrubbed\_entity\_type from formatted text {Platform.scrub(module\_name.lower())}\_dashboard.
- Bind local operation build\_path for subsequent calls.
- Set entity\_path from build\_path(scrubbed\_name).
- If os.path.exists(entity\_path).
  - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L4888) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1293)

<a id="op-a1c578ec56b65c"></a>
### Check if record exists.build path

`operation_foundation_model_sync_business_behavior_check_if_record_exists_build_path`

**Inputs** entity\_name.

**Explicit results** os.path.join(path, scrubbed\_entity\_type, formatted text {entity\_name}.json) · os.path.join(path, scrubbed\_entity\_type, entity\_name, formatted text {entity\_name}.json).

**Local steps**

- If type equals “app”.
  - Return os.path.join(path, scrubbed\_entity\_type, formatted text {entity\_name}.json).
- Return os.path.join(path, scrubbed\_entity\_type, entity\_name, formatted text {entity\_name}.json).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L5360) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1294)

<a id="op-4a277c8154e46e"></a>
### Delete duplicate icons

`operation_foundation_model_sync_business_behavior_delete_duplicate_icons`

**Inputs** no declared parameters.

**Record and data access** read “Desktop Icon” via get\_all.

**State and service calls** request delete\_doc for “Desktop Icon” · commit.

**Local steps**

- For each app in Platform.get\_installed\_apps().
  - Set icons from Platform.get\_all(“Desktop Icon”, filters = list(mapping(“icon\_type” → “App”), mapping(“app” → app)), pluck = “name”).
  - If len(icons) &gt; 1.
    - For each i in icons.
      - Set app\_path from Platform.get\_app\_path(app).
      - If not check\_if\_record\_exists(type = “app”, path = app\_path, entity\_type = “Desktop Icon”, name = i).
        - Evaluate print(formatted text Deleting icon {i}).
        - Evaluate Platform.delete\_doc(“Desktop Icon”, i).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0290.json#L5523) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1296)

## Record · System settings

[Record definition](../../../../data/record-types/system_settings.json)

<a id="op-75c01dd7b8f8f6"></a>
### System Settings.validate

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_validate`

**Inputs** self.

**Record and data access** read “SMS Settings” via get\_single\_value · read “System Settings” via get\_single\_value.

**State and service calls** msgprint with translated “{0} can not be more than {1}”.format(label, 50).

**Explicit failure paths** validation helper — translated “Please select Minimum Password Score” · validation helper — translated “Session Expiry must be in format {0}”.format(“hh:mm”) · validation helper — translated “Please setup SMS before setting it as an authentication method, via SMS Settings”.

**Local steps**

- Bind dependencies toggle\_two\_factor\_auth.
- Set enable\_password\_policy from cint(self.enable\_password\_policy).
- Set minimum\_password\_score from cint(getattr(self, “minimum\_password\_score”, 0)).
- If (enable\_password\_policy and minimum\_password\_score ≤ 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in enable\_password\_policy → minimum\_password\_score ≤ 0.
  - Call the validation error handler Platform.throw(translated “Please select Minimum Password Score”).
- Otherwise.
  - If not enable\_password\_policy.
    - Set self.minimum\_password\_score from empty text.
- If self.session\_expiry.
  - Set parts from self.session\_expiry.split(“:”).
  - If (len(parts) differs from 2 or not (cint(parts at 0) or cint(parts at 1))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(parts) differs from 2 → not (cint(parts at 0) or cint(parts at 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(parts at 0) → cint(parts at 1).
    - Call the validation error handler Platform.throw(translated “Session Expiry must be in format {0}”.format(“hh:mm”)).
- If self.has\_value\_changed(“enable\_two\_factor\_auth”).
  - If self.enable\_two\_factor\_auth.
    - If self.two\_factor\_method equals “SMS”.
      - If not Platform.db.get\_single\_value(“SMS Settings”, “sms\_gateway\_url”).
        - Call the validation error handler Platform.throw(translated “Please setup SMS before setting it as an authentication method, via SMS Settings”).
    - Evaluate toggle\_two\_factor\_auth(true, roles = list(“All”)).
  - Otherwise.
    - Set self.bypass\_2fa\_for\_retricted\_ip\_users from 0.
    - Set self.bypass\_restrict\_ip\_check\_if\_2fa\_enabled from 0.
- Set Platform.flags.update\_last\_reset\_password\_date from false.
- If (self.force\_user\_to\_reset\_password and not cint(Platform.db.get\_single\_value(“System Settings”, “force\_user\_to\_reset\_password”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.force\_user\_to\_reset\_password → not cint(Platform.db.get\_single\_value(“System Settings”, “force\_user\_to\_reset\_password”)).
  - Set Platform.flags.update\_last\_reset\_password\_date from true.
- Evaluate self.validate\_user\_pass\_login().
- Evaluate self.validate\_backup\_limit().
- Evaluate self.validate\_file\_extensions().
- Evaluate self.validate\_otp\_sms\_template().
- If not self.link\_field\_results\_limit.
  - Set self.link\_field\_results\_limit from 10.
- If self.link\_field\_results\_limit &gt; 50.
  - Set self.link\_field\_results\_limit from 50.
  - Set label from translated self.meta.get\_label(“link\_field\_results\_limit”).
  - Evaluate Platform.msgprint(translated “{0} can not be more than {1}”.format(label, 50), alert = true, indicator = “yellow”).
- Evaluate self.validate\_snapshot\_reports().
- Evaluate self.validate\_submission\_queue\_timeout().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate user pass login](operations-095.md#op-a29d3f526ad874), [validate backup limit](operations-095.md#op-bfa1c165786fc0), [validate file extensions](operations-095.md#op-3064756b2434d8), [validate otp sms template](operations-095.md#op-00b8f3d63e2902), [validate snapshot reports](operations-095.md#op-06662238093f55), [validate submission queue timeout](operations-095.md#op-7b3dbaf068e23b).

**Values supplied outside this operation** selected callable from getattr(self, “minimum\_password\_score”, 0) · configured or stored value from Platform.db.get\_single\_value(“SMS Settings”, “sms\_gateway\_url”), Platform.db.get\_single\_value(“System Settings”, “force\_user\_to\_reset\_password”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L42) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L623)

<a id="op-00b8f3d63e2902"></a>
### System Settings.validate otp sms template

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_validate_one_time_password_short_message_service_template`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L7083) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L626)

<a id="op-a29d3f526ad874"></a>
### System Settings.validate user pass login

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_validate_user_pass_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** no value.

**Observed service boundaries** record lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0107.json#L7282) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L628)

<a id="op-bfa1c165786fc0"></a>
### System Settings.validate backup limit

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_validate_backup_limit`

**Inputs** self.

**State and service calls** msgprint with translated “Number of backups must be greater than zero.”.

**Local steps**

- If (not self.backup\_limit or self.backup\_limit &lt; 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.backup\_limit → self.backup\_limit &lt; 1.
  - Evaluate Platform.msgprint(translated “Number of backups must be greater than zero.”, alert = true).
  - Set self.backup\_limit from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L624)

<a id="op-3064756b2434d8"></a>
### System Settings.validate file extensions

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_validate_file_extensions`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.allowed\_file\_extensions.
  - Return no value.
- Set self.allowed\_file\_extensions from whitespace '\\n'.join(generator of ext.strip().upper() for ext drawn from nested operand in the contract.allowed\_file\_extensions.strip().splitlines()).
  - Draw ext from self.allowed\_file\_extensions.strip().splitlines().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L146) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L625)

<a id="op-58bf2a9a515159"></a>
### System Settings.on update

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.set\_defaults().
- Evaluate clear\_system\_settings\_cache().
- If Platform.flags.update\_last\_reset\_password\_date.
  - Evaluate update\_last\_reset\_password\_date().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set defaults](operations-095.md#op-730fcd9a6c2e1b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L300) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L621)

<a id="op-730fcd9a6c2e1b"></a>
### System Settings.set defaults

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_set_defaults`

**Inputs** self.

**Local steps**

- Bind dependencies set\_default\_language.
- For each df in self.meta.get(“fields”).
  - If (df.fieldtype does not belong to no\_value\_fields and self.has\_value\_changed(df.fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → self.has\_value\_changed(df.fieldname).
    - Evaluate Platform.db.set\_default(df.fieldname, self.get(df.fieldname)).
- If self.language.
  - Evaluate set\_default\_language(self.language).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L401) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L622)

<a id="op-06662238093f55"></a>
### System Settings.validate snapshot reports

`operation_foundation_core_record_definitions_system_settings_business_behavior_system_settings_validate_snapshot_reports`

**Inputs** self.

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save().
- If (old\_doc.enable\_snapshot\_reports differs from self.enable\_snapshot\_reports or old\_doc.frequency differs from self.frequency).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in old\_doc.enable\_snapshot\_reports differs from self.enable\_snapshot\_reports → old\_doc.frequency differs from self.frequency.
  - Evaluate snapshot\_report\_scheduler(self.enable\_snapshot\_reports, self.frequency).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L630) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L627)

<a id="op-7b3dbaf068e23b"></a>
### System Settings.validate submission queue timeout

`operation_foundation_binding_foundation_core_doctype_system_settings_system_settings_systemsettings_validate_submission_queue_timeout`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} cannot be more than {1} seconds (1 hour)”.format(label, MAX\_SUBMISSION\_QUEUE\_TIMEOUT).

**Local steps**

- If cint(self.submission\_queue\_timeout) &gt; MAX\_SUBMISSION\_QUEUE\_TIMEOUT.
  - Set label from self.meta.get\_translated\_label(“submission\_queue\_timeout”).
  - Call the validation error handler Platform.throw(translated “{0} cannot be more than {1} seconds (1 hour)”.format(label, MAX\_SUBMISSION\_QUEUE\_TIMEOUT), title = translated “Invalid Submission Queue Timeout”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L182) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L640)

<a id="op-dde97744f64249"></a>
### Update last reset password date

`operation_foundation_core_record_definitions_system_settings_business_behavior_update_last_reset_password_date`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L779) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L629)

<a id="op-54eae7ceb3e3a2"></a>
### Load

`operation_foundation_core_record_definitions_system_settings_business_behavior_load`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“timezones” → get\_all\_timezones(), “defaults” → defaults).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- Bind dependencies get\_all\_timezones.
- If “System Manager” does not belong to Platform.get\_roles().
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set defaults from mapping().
- For each df in Platform.get\_meta(“System Settings”).get(“fields”).
  - If df.fieldtype belongs to tuple(“Select”, “Data”).
    - Set defaults at df.fieldname from get\_system\_settings(df.fieldname).
- Return mapping(“timezones” → get\_all\_timezones(), “defaults” → defaults).

**Values supplied outside this operation** effective access from Platform.get\_roles() · configured or stored value from get\_system\_settings(df.fieldname).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L40) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L618)

<a id="op-b5afee671b4bee"></a>
### Get system settings

`operation_foundation_core_record_definitions_system_settings_business_behavior_get_system_settings`

**Inputs** key.

**Explicit results** no value · system\_settings.get(key).

**Local steps**

- If not system\_settings bound to getattr(Platform.local, “system\_settings”, no value).
  - Attempt the following.
    - Set system\_settings from Platform.client\_cache.get\_doc(“System Settings”).
    - Set Platform.local.system\_settings from system\_settings.
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
    - Return no value.
- Return system\_settings.get(key).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “system\_settings”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L1195) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L617)

<a id="op-6bd5fea0559a99"></a>
### Clear system settings cache

`operation_foundation_core_record_definitions_system_settings_business_behavior_clear_system_settings_cache`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.client\_cache.delete\_value(Platform.get\_document\_cache\_key(“System Settings”, “System Settings”)).
- Evaluate Platform.cache.delete\_value(“system\_settings”).
- Evaluate Platform.cache.delete\_value(“time\_zone”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L1405) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L614)

<a id="op-2d8782a7cae143"></a>
### Sync system settings

`operation_foundation_core_record_definitions_system_settings_business_behavior_sync_system_settings`

**Inputs** no declared parameters.

**Record and data access** read “System Settings” via get\_single\_value.

**State and service calls** request set\_single\_value on “System Settings”.

**Local steps**

- If Platform.db.get\_single\_value(“System Settings”, “currency”) is identical to no value.
  - Evaluate Platform.db.set\_single\_value(“System Settings”, “currency”, Platform.defaults.get\_defaults() at “currency”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0108.json#L1543) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L620)
