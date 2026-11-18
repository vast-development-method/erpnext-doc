# Record lifecycle and persistence · operations 32

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Defaults

<a id="op-ca3a48e74cb0a9"></a>
### Add global default

`operation_foundation_defaults_business_behavior_add_global_default`

**Inputs** key, value.

**Local steps**

- Evaluate add\_default(key, value, “\_\_default”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L3060) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1546)

<a id="op-616c1d26cc2b99"></a>
### Get global default

`operation_foundation_defaults_business_behavior_get_global_default`

**Inputs** key.

**Explicit results** no value · value.

**Local steps**

- Set d from get\_defaults().get(key, no value).
- Set value from ((isinstance(d, (list bitwise or tuple)) and d at 0) or d).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (isinstance(d, (list bitwise or tuple)) and d at 0) → d.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(d, (list bitwise or tuple)) → d at 0.
- If not\_in\_user\_permission(key, value).
  - Return no value.
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L3127) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1553)

<a id="op-211e281ceaafda"></a>
### Set default

`operation_foundation_defaults_business_behavior_set_default`

**Inputs** key, value, parent, parenttype = “\_\_default”.

**State and service calls** request delete on “DefaultValue”.

**Explicit results** no value.

**Local steps**

- Set table from DocType(“DefaultValue”).
- Set current\_value from nested operand in the contract(nested operand in the contract).select(table.defvalue).for\_update().run(as\_dict = true).
- If current\_value.
  - If current\_value at 0.defvalue equals cstr(value).
    - Return no value.
  - Evaluate Platform.db.delete(“DefaultValue”, mapping(“defkey” → key, “parent” → parent)).
- If value is distinct from no value.
  - Evaluate add\_default(key, value, parent, parenttype).
- Otherwise.
  - Evaluate \_clear\_cache(parent).
- If parent.
  - Evaluate clear\_defaults\_cache(parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L16) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1560)

<a id="op-0a223aa15fb41c"></a>
### Add default

`operation_foundation_defaults_business_behavior_add_default`

**Inputs** key, value, parent, parenttype = no value.

**Record and data access** resolve a document from mapping(“doctype” → “DefaultValue”, “parent” → parent, “parenttype” → (parenttype or “\_\_default”), “parentfield” → “system\_defaults”, …) via get\_doc.

**State and service calls** call insert on d.

**Local steps**

- Set d from Platform.get\_doc(mapping(“doctype” → “DefaultValue”, “parent” → parent, “parenttype” → (parenttype or “\_\_default”), “parentfield” → “system\_defaults”, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parenttype → “\_\_default”.
- Evaluate d.insert(ignore\_permissions = true).
- Evaluate \_clear\_cache(parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L3772) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1545)

<a id="op-005f9acbe3afa0"></a>
### Clear default

`operation_foundation_defaults_business_behavior_clear_default`

**Inputs** key = no value, value = no value, parent = no value, name = no value, parenttype = no value.

**State and service calls** request delete on “DefaultValue”.

**Explicit failure paths** Exception(“&#91;clear\_default&#93; No key specified.”).

**Local steps**

- Set filters from mapping().
- If name.
  - Evaluate filters.update(mapping(“name” → name)).
- Otherwise.
  - If key.
    - Evaluate filters.update(mapping(“defkey” → key)).
  - If value.
    - Evaluate filters.update(mapping(“defvalue” → value)).
  - If parent.
    - Evaluate filters.update(mapping(“parent” → parent)).
  - If parenttype.
    - Evaluate filters.update(mapping(“parenttype” → parenttype)).
- If parent.
  - Evaluate clear\_defaults\_cache(parent).
- Otherwise.
  - Evaluate clear\_defaults\_cache(“\_\_default”).
  - Evaluate clear\_defaults\_cache(“\_\_global”).
- If not filters.
  - Raise Exception(“&#91;clear\_default&#93; No key specified.”).
- Evaluate Platform.db.delete(“DefaultValue”, filters).
- Evaluate \_clear\_cache(parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L4018) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1549)

<a id="op-cf4ad9fa0d8e93"></a>
### Get defaults for

`operation_foundation_defaults_business_behavior_get_defaults_for`

**Inputs** parent = “\_\_default”.

**Explicit results** defaults.

**Local steps**

- Set key from formatted text defaults::{parent}.
- Set defaults from Platform.client\_cache.get\_value(key).
- If defaults is identical to no value.
  - Set table from DocType(“DefaultValue”).
  - Set res from nested operand in the contract(nested operand in the contract).select(table.defkey, table.defvalue).orderby(“creation”).run(as\_dict = true).
  - Set defaults from Platform.\_dict().
  - For each d in res.
    - If d.defkey belongs to defaults.
      - If (not isinstance(defaults at d.defkey, list) and defaults at d.defkey differs from d.defvalue).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not isinstance(defaults at d.defkey, list) → defaults at d.defkey differs from d.defvalue.
        - Set defaults at d.defkey from list(defaults at d.defkey).
      - If d.defvalue does not belong to defaults at d.defkey.
        - Evaluate defaults at d.defkey.append(d.defvalue).
    - Otherwise.
      - If d.defvalue is distinct from no value.
        - Set defaults at d.defkey from d.defvalue.
  - Evaluate Platform.client\_cache.set\_value(key, defaults).
- Return defaults.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L4520) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1552)

<a id="op-98990fdd4cc23b"></a>
### Clear cache

`operation_foundation_defaults_business_behavior_clear_cache`

**Inputs** parent.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_install.
  - Return no value.
- Evaluate Platform.clear\_cache(user = parent when parent does not belong to common\_default\_keys, otherwise no value).
  - Value choice on parent does not belong to common\_default\_keys — true gives parent, false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L5158) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1548)

## Record · Defaultvalue

<a id="op-91c483ff4f0a63"></a>
### On doctype update

`operation_foundation_core_record_definitions_defaultvalue_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** commit · request add\_index on “DefaultValue”.

**Local steps**

- Evaluate Platform.db.commit().
- Evaluate Platform.db.add\_index(doctype = “DefaultValue”, fields = list(“parent”, “defkey”), index\_name = “defaultvalue\_parent\_defkey\_index”).
- Evaluate Platform.db.add\_index(doctype = “DefaultValue”, fields = list(“parent”, “parenttype”), index\_name = “defaultvalue\_parent\_parenttype\_index”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0060.json#L6713) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1359) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1349)

## Service · Deferred insert

<a id="op-a04ad96f67e261"></a>
### Deferred insert

`operation_foundation_deferred_insert_business_behavior_deferred_insert`

**Inputs** doctype, records.

**Local steps**

- If isinstance(records, (dict bitwise or list)).
  - Set \_records from json.dumps(records).
- Otherwise.
  - Set \_records from records.
- Attempt the following.
  - Evaluate Platform.cache.rpush(formatted text {queue\_prefix}{doctype}, \_records).
- On failure (redis.exceptions.ConnectionError).
  - For each record in records.
    - Evaluate insert\_record(record, doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L5263) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1563)

<a id="op-c7d1de25c3f35a"></a>
### Save to db

`operation_foundation_deferred_insert_business_behavior_save_to_database`

**Inputs** no declared parameters.

**State and service calls** commit.

**Local steps**

- Set queue\_keys from Platform.cache.get\_keys(queue\_prefix).
- For each key in queue\_keys.
  - Set record\_count from 0.
  - Set queue\_key from get\_key\_name(key).
  - Set doctype from get\_doctype\_name(key).
  - While (Platform.cache.llen(queue\_key) &gt; 0 and record\_count ≤ 10000).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.cache.llen(queue\_key) &gt; 0 → record\_count ≤ 10000.
    - Set records from Platform.cache.lpop(queue\_key).
    - Set records from json.loads(records.decode(“utf-8”)).
    - If isinstance(records, dict).
      - Update record\_count using + 1.
      - Evaluate insert\_record(records, doctype).
      - Continue with the next iteration or loop test.
    - For each record in records.
      - Update record\_count using + 1.
      - Evaluate insert\_record(record, doctype).
      - If (record\_count modulo or format 100) equals 0.
        - Evaluate Platform.db.commit().
    - If (record\_count modulo or format 100) equals 0.
      - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L17) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1567)

<a id="op-6ecfda096da335"></a>
### Insert record

`operation_foundation_deferred_insert_business_behavior_insert_record`

**Inputs** record, doctype.

**Record and data access** resolve a document from record via get\_doc.

**State and service calls** call insert on Platform.get\_doc(record).

**Local steps**

- Attempt the following.
  - Evaluate record.update(mapping(“doctype” → doctype)).
  - Evaluate Platform.get\_doc(record).insert().
- On failure (Exception) bound to e.
  - Evaluate Platform.logger().error(formatted text Error while inserting deferred {doctype} record: {e}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L6129) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1566)

<a id="op-1168a4ce913c82"></a>
### Get key name

`operation_foundation_deferred_insert_business_behavior_get_key_name`

**Inputs** key.

**Declared result** str.

**Explicit results** cstr(key).split(“\|”) at 1.

**Local steps**

- Return cstr(key).split(“\|”) at 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L6352) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1564)

<a id="op-b94989b4d7ce20"></a>
### Get doctype name

`operation_foundation_deferred_insert_business_behavior_get_record_type_name`

**Inputs** key.

**Declared result** str.

**Explicit results** cstr(key).split(queue\_prefix) at 1.

**Local steps**

- Return cstr(key).split(queue\_prefix) at 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0149.json#L6435) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1565)

## Service · Delete doc

<a id="op-31dfba6224a009"></a>
### Delete doc

`operation_foundation_model_delete_record_business_behavior_delete_record`

**Inputs** doctype = no value, name = no value, force = 0, ignore\_doctypes = no value, for\_reload = false, ignore\_permissions = false, flags = no value, ignore\_on\_trash = false, ignore\_missing = true, delete\_permanently = false.

**Declared result** (bool bitwise or no value).

**Record and data access** resolve a document from doctype via get\_doc · read doctype via exists · read doctype via get\_value.

**State and service calls** request delete on “Custom Field” · request delete on “\_\_global\_search” · enqueue with “Platform.model.delete\_doc.delete\_dynamic\_links”.

**Explicit results** false.

**Explicit failure paths** validation helper — translated “{0} is a Virtual DocType and must implement its own delete() method.”.format(doctype) · Platform.DoesNotExistError(doctype = doctype) · validation helper — translated “Standard DocType can not be deleted.” · validation helper with type(error) — translated “This document can not be deleted right now as it's being modified by another user. Please try again after so …” · validation helper with Platform.LinkExistsError — translated “You can disable this {0} instead of deleting it.”.format(translated doctype) · 1 additional forms in the steps below.

**Local steps**

- If not ignore\_doctypes.
  - Set ignore\_doctypes from list().
- If not doctype.
  - Set doctype from Platform.form\_dict.get(“dt”).
  - Set name from Platform.form\_dict.get(“dn”).
- Set is\_virtual from is\_virtual\_doctype(doctype).
- Set names from name.
- If (isinstance(name, str) or isinstance(name, int)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(name, str) → isinstance(name, int).
  - Set names from list(name).
- For each name in (names or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in names → list().
  - If is\_virtual.
    - Set doc from Platform.get\_doc(doctype, name).
    - Evaluate update\_flags(doc, flags, ignore\_permissions).
    - Evaluate check\_permission\_and\_not\_submitted(doc).
    - Bind dependencies Document.
    - If type(doc).delete equals Document.delete.
      - Call the validation error handler Platform.throw(translated “{0} is a Virtual DocType and must implement its own delete() method.”.format(doctype)).
    - Evaluate doc.delete().
    - Continue with the next iteration or loop test.
  - If not Platform.db.exists(doctype, name).
    - If not ignore\_missing.
      - Raise Platform.DoesNotExistError(doctype = doctype).
    - Otherwise.
      - Return false.
  - Set doc from no value.
  - If doctype equals “DocType”.
    - If for\_reload.
      - Attempt the following.
        - Set doc from Platform.get\_doc(doctype, name).
      - On failure (Platform.DoesNotExistError).
        - Take no action here.
      - When the protected block completes normally.
        - Evaluate doc.run\_method(“before\_reload”).
    - Otherwise.
      - Set doc from Platform.get\_doc(doctype, name).
      - If not (doc.custom or Platform.conf.developer\_mode or Platform.flags.in\_patch or force).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.custom → Platform.conf.developer\_mode → Platform.flags.in\_patch → force.
        - Call the validation error handler Platform.throw(translated “Standard DocType can not be deleted.”).
      - Evaluate update\_flags(doc, flags, ignore\_permissions).
      - Evaluate check\_permission\_and\_not\_submitted(doc).
      - Evaluate Platform.db.delete(“Custom Field”, mapping(“options” → name, “fieldtype” → tuple(“in”, Platform.model.table\_fields))).
      - Evaluate Platform.db.delete(“\_\_global\_search”, mapping(“doctype” → name)).
    - Evaluate delete\_from\_table(doctype, name, ignore\_doctypes, no value).
    - If (Platform.conf.developer\_mode and not doc.custom and not (for\_reload or Platform.flags.in\_migrate or Platform.flags.in\_install or Platform.flags.in\_uninstall)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → not doc.custom → not (for\_reload or Platform.flags.in\_migrate or Platform.flags.in\_install or Platform.flags.in\_uninstall).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in for\_reload → Platform.flags.in\_migrate → Platform.flags.in\_install → Platform.flags.in\_uninstall.
      - Attempt the following.
        - Evaluate delete\_controllers(name, doc.module).
      - On failure (tuple(OSError, KeyError)).
        - Take no action here.
    - Evaluate Platform.clear\_cache(doctype = name).
  - Otherwise.
    - Attempt the following.
      - Evaluate Platform.db.get\_value(doctype, name, for\_update = true, wait = false).
    - On failure (tuple(Platform.QueryTimeoutError, Platform.QueryDeadlockError)) bound to error.
      - Call the validation error handler Platform.throw(translated “This document can not be deleted right now as it's being modified by another user. Please try again after so …”, exc = type(error)).
    - Set doc from Platform.get\_doc(doctype, name).
    - If not for\_reload.
      - Evaluate update\_flags(doc, flags, ignore\_permissions).
      - Evaluate check\_permission\_and\_not\_submitted(doc).
      - Set doc.flags.force\_delete from force.
      - If not ignore\_on\_trash.
        - Evaluate doc.run\_method(“on\_trash”).
        - Set doc.flags.in\_delete from true.
        - Evaluate doc.run\_method(“on\_change”).
      - If not force.
        - Attempt the following.
          - Evaluate check\_if\_doc\_is\_linked(doc).
          - Evaluate check\_if\_doc\_is\_dynamically\_linked(doc).
        - On failure (Platform.LinkExistsError) bound to e.
          - If (doc.meta.has\_field(“enabled”) or doc.meta.has\_field(“disabled”)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.meta.has\_field(“enabled”) → doc.meta.has\_field(“disabled”).
            - Call the validation error handler Platform.throw(translated “You can disable this {0} instead of deleting it.”.format(translated doctype), Platform.LinkExistsError).
          - Otherwise.
            - Raise e.
    - Evaluate update\_naming\_series(doc).
    - Evaluate delete\_from\_table(doctype, name, ignore\_doctypes, doc).
    - Evaluate doc.run\_method(“after\_delete”).
    - Evaluate remove\_all(doctype, name, from\_delete = true, delete\_permanently = delete\_permanently).
    - If not for\_reload.
      - Evaluate Platform.enqueue(“Platform.model.delete\_doc.delete\_dynamic\_links”, doctype = doc.doctype, name = doc.name, now = Platform.in\_test, enqueue\_after\_commit = true).
  - Evaluate delete\_all\_passwords\_for(doctype, name).
  - Evaluate doc.clear\_cache().
  - Evaluate delete\_for\_document(doc).
  - Evaluate delete\_tags\_for\_document(doc).
  - If for\_reload.
    - Set delete\_permanently from true.
  - If not delete\_permanently.
    - Evaluate add\_to\_deleted\_document(doc).
  - If (doc and not for\_reload).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → not for\_reload.
    - If not Platform.flags.in\_patch.
      - Attempt the following.
        - Evaluate doc.notify\_update().
        - Evaluate insert\_feed(doc).
      - On failure (ImportError).
        - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from doc.run\_method(“before\_reload”), doc.run\_method(“on\_trash”) and 2 further calls · service or queued work from Platform.enqueue(“Platform.model.delete\_doc.delete\_dynamic\_links”, doctype = doc.doctype, name = doc.name, now = Platform.in\_test, enqueue\_after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L929)

<a id="op-948058c5f79ea8"></a>
### Add to deleted document

`operation_foundation_model_delete_record_business_behavior_add_to_deleted_document`

**Inputs** doc.

**Record and data access** resolve a document from “Deleted Document” via get\_doc.

**State and service calls** call db\_insert on Platform.get\_doc(doctype = “Deleted Document”, deleted\_doctype = doc.doctype, deleted\_name = doc.name, data = doc.as\_json(), …).

**Local steps**

- If (doc.doctype differs from “Deleted Document” and Platform.flags.in\_install differs from “Platform”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype differs from “Deleted Document” → Platform.flags.in\_install differs from “Platform”.
  - Evaluate Platform.get\_doc(doctype = “Deleted Document”, deleted\_doctype = doc.doctype, deleted\_name = doc.name, data = doc.as\_json(), …).db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L2577) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L920)

<a id="op-8a95654072127e"></a>
### Update naming series

`operation_foundation_model_delete_record_business_behavior_update_naming_series`

**Inputs** doc.

**Local steps**

- If doc.meta.autoname.
  - If (doc.meta.autoname.startswith(“naming\_series:”) and getattr(doc, “naming\_series”, no value)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.autoname.startswith(“naming\_series:”) → getattr(doc, “naming\_series”, no value).
    - Evaluate revert\_series\_if\_last(doc.naming\_series, doc.name, doc).
  - Otherwise.
    - If doc.meta.autoname.split(“:”, 1) at 0 does not belong to tuple(“Prompt”, “field”, “hash”, “autoincrement”).
      - Evaluate revert\_series\_if\_last(doc.meta.autoname, doc.name, doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, “naming\_series”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L2778) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L936)

<a id="op-a571d930ccaa4b"></a>
### Delete from table

`operation_foundation_model_delete_record_business_behavior_delete_from_table`

**Inputs** doctype, name, ignore\_doctypes, doc.

**Record and data access** read “DocField” via get\_all.

**State and service calls** request delete on “Singles” · request delete on doctype · request delete on child\_doctype.

**Local steps**

- If (doctype differs from “DocType” and doctype equals name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype differs from “DocType” → doctype equals name.
  - Evaluate Platform.db.delete(“Singles”, mapping(“doctype” → name)).
- Otherwise.
  - Evaluate Platform.db.delete(doctype, mapping(“name” → name)).
- If doc.
  - Set child\_doctypes from list of d.options for d drawn from doc.meta.get\_table\_fields() where Platform.get\_meta(d.options).is\_virtual equals 0.
    - Draw d from doc.meta.get\_table\_fields(), keep a combination only if (Platform.get\_meta(d.options).is\_virtual equals 0).
- Otherwise.
  - Set child\_doctypes from Platform.get\_all(“DocField”, fields = “options”, filters = mapping(“fieldtype” → list(“in”, Platform.model.table\_fields), “parent” → doctype), pluck = “options”).
- Set child\_doctypes\_to\_delete from (set(child\_doctypes) − set(ignore\_doctypes)).
- For each child\_doctype in child\_doctypes\_to\_delete.
  - Evaluate Platform.db.delete(child\_doctype, mapping(“parenttype” → doctype, “parent” → name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L3057) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L928)

<a id="op-198aba5d2d5a31"></a>
### Update flags

`operation_foundation_model_delete_record_business_behavior_update_flags`

**Inputs** doc, flags = no value, ignore\_permissions = false.

**Local steps**

- If ignore\_permissions.
  - If not flags.
    - Set flags from mapping().
  - Set flags at “ignore\_permissions” from ignore\_permissions.
- If flags.
  - Evaluate doc.flags.update(flags).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L3625) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L935)

<a id="op-48e57f68c3ca06"></a>
### Check permission and not submitted

`operation_foundation_model_delete_record_business_behavior_check_permission_and_not_submitted`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L3771) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L923)

<a id="op-5726dc75b3037f"></a>
### Get linked docs

`operation_foundation_model_delete_record_business_behavior_get_linked_records`

**Inputs** doc, method = “Delete”, limit = no value.

**Declared result** list at dict.

**Record and data access** read link\_dt via get\_single\_value · read link\_dt via get\_values.

**Explicit results** linked\_docs.

**Explicit failure paths** LinkedDocumentsOverflow.

**Local steps**

- Bind dependencies get\_link\_fields.
- Set link\_fields from get\_link\_fields(doc.doctype).
- Set ignored\_doctypes from set().
- If (method equals “Cancel” and doc\_ignore\_flags bound to doc.get(“ignore\_linked\_doctypes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “Cancel” → doc\_ignore\_flags bound to doc.get(“ignore\_linked\_doctypes”).
  - Evaluate ignored\_doctypes.update(doc\_ignore\_flags).
- If method equals “Delete”.
  - Evaluate ignored\_doctypes.update(Platform.get\_hooks(“ignore\_links\_on\_delete”)).
- Set linked\_docs from list().
- For each lf in link\_fields.
  - Set tuple(link\_dt, link\_field, issingle) from tuple(lf at “parent”, lf at “fieldname”, lf at “issingle”).
  - If (link\_dt belongs to ignored\_doctypes or (link\_field equals “amended\_from” and method equals “Cancel”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_dt belongs to ignored\_doctypes → (link\_field equals “amended\_from” and method equals “Cancel”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in link\_field equals “amended\_from” → method equals “Cancel”.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set meta from Platform.get\_meta(link\_dt).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_last\_message().
    - Continue with the next iteration or loop test.
  - If issingle.
    - If Platform.db.get\_single\_value(link\_dt, link\_field) equals doc.name.
      - Evaluate linked\_docs.append(mapping(“doc” → doc.name, “reference\_doctype” → link\_dt, “reference\_docname” → link\_dt)).
    - Continue with the next iteration or loop test.
  - Set fields from list(“name”, “docstatus”).
  - If meta.istable.
    - Evaluate fields.extend(list(“parent”, “parenttype”)).
  - If (limit and len(linked\_docs) ≥ limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(linked\_docs) ≥ limit.
    - Raise LinkedDocumentsOverflow.
  - Set rows from Platform.db.get\_values(link\_dt, mapping(link\_field → doc.name), fields, as\_dict = true, order\_by = no value, limit = limit).
  - If (limit and len(rows) ≥ limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(rows) ≥ limit.
    - Raise LinkedDocumentsOverflow.
  - For each item in rows.
    - Set item\_parent from getattr(item, “parent”, no value).
    - Set linked\_parent\_doctype from item.parenttype when item\_parent, otherwise link\_dt.
      - Value choice on item\_parent — true gives item.parenttype, false gives link\_dt.
    - If linked\_parent\_doctype belongs to ignored\_doctypes.
      - Continue with the next iteration or loop test.
    - If (method differs from “Delete” and (method differs from “Cancel” or not DocStatus(nested operand in the contract.docstatus).is\_submitted())).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in method differs from “Delete” → (method differs from “Cancel” or not DocStatus(item.docstatus).is\_submitted()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in method differs from “Cancel” → not DocStatus(item.docstatus).is\_submitted().
      - Continue with the next iteration or loop test.
    - Otherwise.
      - If (link\_dt equals doc.doctype and (item\_parent or item.name) equals doc.name).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in link\_dt equals doc.doctype → (item\_parent or item.name) equals doc.name.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_parent → item.name.
        - Continue with the next iteration or loop test.
      - Otherwise.
        - Set reference\_docname from (item\_parent or item.name).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_parent → item.name.
        - Evaluate linked\_docs.append(mapping(“doc” → doc.name, “reference\_doctype” → linked\_parent\_doctype, “reference\_docname” → reference\_docname)).
- Return linked\_docs.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“ignore\_links\_on\_delete”), getattr(item, “parent”, no value) · configured or stored value from Platform.db.get\_single\_value(link\_dt, link\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L4115) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L932)

<a id="op-aadd523d541856"></a>
### Check if doc is linked

`operation_foundation_model_delete_record_business_behavior_check_if_record_is_linked`

**Inputs** doc, method = “Delete”.

**Local steps**

- Set links from get\_linked\_docs(doc, method).
- If links.
  - Set link from links at 0.
  - Evaluate raise\_link\_exists\_exception(doc, link at “reference\_doctype”, link at “reference\_docname”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0274.json#L5441) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L922)

<a id="op-9f1e99961c5f51"></a>
### Get dynamic linked docs

`operation_foundation_model_delete_record_business_behavior_get_dynamic_linked_records`

**Inputs** doc, method = “Delete”, limit = no value.

**Declared result** list at dict.

**Explicit results** linked\_docs.

**Explicit failure paths** LinkedDocumentsOverflow.

**Local steps**

- Set linked\_docs from list().
- For each df in get\_dynamic\_link\_map().get(doc.doctype, list()).
  - If (limit and len(linked\_docs) ≥ limit).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(linked\_docs) ≥ limit.
    - Raise LinkedDocumentsOverflow.
  - Set ignore\_linked\_doctypes from (doc.get(“ignore\_linked\_doctypes”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“ignore\_linked\_doctypes”) → list().
  - If (df.parent belongs to Platform.get\_hooks(“ignore\_links\_on\_delete”) or (df.parent belongs to ignore\_linked\_doctypes and method equals “Cancel”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.parent belongs to Platform.get\_hooks(“ignore\_links\_on\_delete”) → (df.parent belongs to ignore\_linked\_doctypes and method equals “Cancel”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.parent belongs to ignore\_linked\_doctypes → method equals “Cancel”.
    - Continue with the next iteration or loop test.
  - Set meta from Platform.get\_meta(df.parent).
  - If meta.issingle.
    - Set refdoc from Platform.db.get\_singles\_dict(df.parent).
    - If (refdoc.get(df.options) equals doc.doctype and refdoc.get(df.fieldname) equals doc.name and ((method equals “Delete” and not nested operand in the contract(nested operand in the contract).is\_cancelled()) o ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in refdoc.get(df.options) equals doc.doctype → refdoc.get(df.fieldname) equals doc.name → ((method equals “Delete” and not DocStatus(nested operand in the contract.docstatus).is\_cancelled()) or (method equals “Cancel” and DocStatus(refdoc.docstatus).is\_submitted())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (method equals “Delete” and not DocStatus(refdoc.docstatus).is\_cancelled()) → (method equals “Cancel” and DocStatus(refdoc.docstatus).is\_submitted()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “Delete” → not DocStatus(refdoc.docstatus).is\_cancelled().
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “Cancel” → DocStatus(refdoc.docstatus).is\_submitted().
      - Evaluate linked\_docs.append(mapping(“doc” → doc.name, “reference\_doctype” → df.parent, “reference\_docname” → df.parent, “at\_position” → empty text)).
  - Otherwise.
    - Set RefDoc from DocType(df.parent).
    - Set fields from list(RefDoc.name, RefDoc.docstatus).
    - If meta.istable.
      - Evaluate fields.extend(list(RefDoc.parent, RefDoc.parenttype, RefDoc.idx)).
    - Set query from nested operand in the contract(nested operand in the contract).select(expanded fields).where(RefDoc at df.options equals doc.doctype).where(RefDoc at df.fieldname equals doc.name).
    - If (df.parent equals “Submission Queue” and method equals “Delete”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.parent equals “Submission Queue” → method equals “Delete”.
      - Set query from query.where(RefDoc.status equals “Queued”).
    - If method equals “Delete”.
      - Set query from query.where(RefDoc.docstatus differs from DocStatus.cancelled()).
    - Otherwise.
      - If method equals “Cancel”.
        - Set query from query.where(RefDoc.docstatus equals DocStatus.submitted()).
    - If limit.
      - Set query from query.limit(limit).
    - Set rows from query.run(as\_dict = true).
    - If (limit and len(rows) ≥ limit).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in limit → len(rows) ≥ limit.
      - Raise LinkedDocumentsOverflow.
    - For each refdoc in rows.
      - If ((method equals “Delete” and not DocStatus(nested operand in the contract.docstatus).is\_cancelled()) or (method equals “Cancel” and DocStatus(refdoc.docstatus).is\_submitted())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in (method equals “Delete” and not DocStatus(refdoc.docstatus).is\_cancelled()) → (method equals “Cancel” and DocStatus(refdoc.docstatus).is\_submitted()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “Delete” → not DocStatus(refdoc.docstatus).is\_cancelled().
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in method equals “Cancel” → DocStatus(refdoc.docstatus).is\_submitted().
        - Set reference\_doctype from refdoc.parenttype when meta.istable, otherwise df.parent.
          - Value choice on meta.istable — true gives refdoc.parenttype, false gives df.parent.
        - Set reference\_docname from refdoc.parent when meta.istable, otherwise refdoc.name.
          - Value choice on meta.istable — true gives refdoc.parent, false gives refdoc.name.
        - If (reference\_doctype belongs to Platform.get\_hooks(“ignore\_links\_on\_delete”) or (reference\_doctype belongs to ignore\_linked\_doctypes and method equals “Cancel”)).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doctype belongs to Platform.get\_hooks(“ignore\_links\_on\_delete”) → (reference\_doctype belongs to ignore\_linked\_doctypes and method equals “Cancel”).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype belongs to ignore\_linked\_doctypes → method equals “Cancel”.
          - Continue with the next iteration or loop test.
        - Set at\_position from formatted text at Row: {refdoc.idx} when meta.istable, otherwise empty text.
          - Value choice on meta.istable — true gives formatted text at Row: {refdoc.idx}, false gives empty text.
        - Evaluate linked\_docs.append(mapping(“doc” → doc.name, “reference\_doctype” → reference\_doctype, “reference\_docname” → reference\_docname, “at\_position” → at\_position)).
- Return linked\_docs.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“ignore\_links\_on\_delete”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L71) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L931)

<a id="op-02b0ca8c7a5a76"></a>
### Check if doc is dynamically linked

`operation_foundation_model_delete_record_business_behavior_check_if_record_is_dynamically_linked`

**Inputs** doc, method = “Delete”.

**Local steps**

- Set links from get\_dynamic\_linked\_docs(doc, method).
- If links.
  - Set link from links at 0.
  - Evaluate raise\_link\_exists\_exception(doc, link at “reference\_doctype”, link at “reference\_docname”, link at “at\_position”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L1723) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L308) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L921)

<a id="op-803717980432e3"></a>
### Raise link exists exception

`operation_foundation_model_delete_record_business_behavior_raise_link_exists_exception`

**Inputs** doc, reference\_doctype, reference\_docname, row = empty text.

**Explicit failure paths** validation helper with Platform.LinkExistsError — translated “Cannot delete or cancel because {0} {1} is linked with {2} {3} {4}”.format(translated doc.doctype, doc\_link, translated reference\_doctype, reference\_link, …).

**Local steps**

- Set doc\_link from get\_link\_to\_form(doc.doctype, doc.name, doc.name).
- Set reference\_link from get\_link\_to\_form(reference\_doctype, reference\_docname, reference\_docname).
- If reference\_doctype equals reference\_docname.
  - Set reference\_doctype from empty text.
- Call the validation error handler Platform.throw(translated “Cannot delete or cancel because {0} {1} is linked with {2} {3} {4}”.format(translated doc.doctype, doc\_link, translated reference\_doctype, reference\_link, …), Platform.LinkExistsError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L1890) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L934)
