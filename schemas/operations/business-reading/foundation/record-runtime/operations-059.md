# Record lifecycle and persistence · operations 59

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Lazytranslatedstring

<a id="op-40bacd0394dc46"></a>
### Lazy Translate.eq

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_eq`

**Inputs** self, other.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4903) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1451)

<a id="op-3d6544d32b2b43"></a>
### Lazy Translate.lt

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_lt`

**Inputs** self, other.

**Explicit failure paths** NotImplementedError.

**Local steps**

- Raise NotImplementedError.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4952) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1453)

## Service · Link count

<a id="op-4049e401054a3b"></a>
### Notify link count

`operation_foundation_model_utils_link_count_business_behavior_notify_link_count`

**Inputs** doctype, name.

**Explicit results** no value.

**Local steps**

- If (doctype belongs to ignore\_doctypes or not Platform.request or random() &lt; 0.9).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype belongs to ignore\_doctypes → not Platform.request → random() &lt; 0.9.
  - Return no value.
- If not hasattr(Platform.local, “\_link\_count”).
  - Set Platform.local.\_link\_count from defaultdict(int).
  - Evaluate Platform.db.after\_commit.add(flush\_local\_link\_count).
- Update Platform.local.\_link\_count at tuple(doctype, name) using + 1.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from random().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L2598) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1320)

<a id="op-736342ae453e86"></a>
### Flush local link count

`operation_foundation_model_utils_link_count_business_behavior_flush_local_link_count`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- Set new\_links from getattr(Platform.local, “\_link\_count”, no value).
- If not new\_links.
  - Return no value.
- Set link\_count from (Platform.cache.get\_value(“\_link\_count”) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.cache.get\_value(“\_link\_count”) → mapping().
- Set flush from false.
- For each tuple(key, value) in new\_links.items().
  - If key belongs to link\_count.
    - Update link\_count at key using + value.
  - Otherwise.
    - If len(link\_count) &lt; LINK\_COUNT\_BUFFER\_SIZE.
      - Set link\_count at key from value.
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Set flush from true.
- If flush.
  - Evaluate Platform.cache.set\_value(“\_link\_count”, link\_count).
- Evaluate new\_links.clear().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “\_link\_count”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L2839) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1319)

<a id="op-f1dc3fa6f61345"></a>
### Update link count

`operation_foundation_model_utils_link_count_business_behavior_update_link_count`

**Inputs** no declared parameters.

**State and service calls** commit.

**Explicit failure paths** e.

**Local steps**

- Set link\_count from Platform.cache.get\_value(“\_link\_count”).
- If link\_count.
  - For each tuple(tuple(doctype, name), count) in link\_count.items().
    - Attempt the following.
      - Set table from Platform.qb.DocType(doctype).
      - Evaluate nested operand in the contract(nested operand in the contract).set(table.idx, (nested operand in the contract.idx + count)).where(table.name equals name).run().
      - Evaluate Platform.db.commit().
    - On failure (Exception) bound to e.
      - If not Platform.db.is\_table\_missing(e).
        - Raise e.
- Evaluate Platform.cache.delete\_value(“\_link\_count”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0291.json#L3181) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1321)

## Record · Log settings

[Record definition](../../../../data/record-types/log_settings.json)

<a id="op-44ad419cd0063a"></a>
### Log Type.clear old logs

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_type_clear_old_logs`

**Inputs** days.

**Wrappers, in declaration order** staticmethod.

**Declared result** no value.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L273) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1653)

<a id="op-1a94dbde3772bc"></a>
### Supports log clearing

`operation_foundation_core_record_definitions_log_settings_business_behavior_supports_log_clearing`

**Inputs** doctype.

**Wrappers, in declaration order** site\_cache.

**Declared result** bool.

**Explicit results** issubclass(controller, LogType) · false.

**Local steps**

- Attempt the following.
  - Set controller from get\_controller(doctype).
  - Return issubclass(controller, LogType).
- On failure (Exception).
  - Return false.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L319) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1655)

<a id="op-53207abc37e6dc"></a>
### Log Settings.validate

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.remove\_unsupported\_doctypes().
- Evaluate self.\_deduplicate\_entries().
- Evaluate self.add\_default\_logtypes().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove unsupported doctypes](operations-059.md#op-b1f662d4fe4cdb), [deduplicate entries](operations-059.md#op-db26f6129bbd95), [add default logtypes](operations-059.md#op-31eae1f597fe4c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L440) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1652)

<a id="op-b1f662d4fe4cdb"></a>
### Log Settings.remove unsupported doctypes

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_settings_remove_unsupported_record_types`

**Inputs** self.

**State and service calls** msgprint with msg.

**Local steps**

- For each entry in list(self.logs\_to\_clear).
  - If \_supports\_log\_clearing(entry.ref\_doctype).
    - Continue with the next iteration or loop test.
  - Set msg from translated “{} does not support automated log clearing.”.format(Platform.bold(entry.ref\_doctype)).
  - If Platform.conf.developer\_mode.
    - Update msg using + (text in the contract + translated “Implement ′clear\_old\_logs′ method to enable auto error clearing.”).
  - Evaluate Platform.msgprint(msg, title = translated “DocType not supported by Log Settings.”).
  - Evaluate self.remove(entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L531) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1696) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1651)

<a id="op-db26f6129bbd95"></a>
### Log Settings.deduplicate entries

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_settings_deduplicate_entries`

**Inputs** self.

**Local steps**

- Set seen from set().
- For each entry in list(self.logs\_to\_clear).
  - If entry.ref\_doctype belongs to seen.
    - Evaluate self.remove(entry).
  - Evaluate seen.add(entry.ref\_doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L813) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1649)

<a id="op-31eae1f597fe4c"></a>
### Log Settings.add default logtypes

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_settings_add_default_logtypes`

**Inputs** self.

**Record and data access** read “DocType” via exists.

**State and service calls** msgprint with translated “Added default log doctypes: {}”.format(“,”.join(added\_logtypes)).

**Local steps**

- Set existing\_logtypes from set of d.ref\_doctype for d drawn from self.logs\_to\_clear.
  - Draw d from self.logs\_to\_clear.
- Set added\_logtypes from set().
- Set default\_logtypes\_retention from Platform.get\_hooks(“default\_log\_clearing\_doctypes”, mapping()).
- For each tuple(logtype, retentions) in default\_logtypes\_retention.items().
  - If (logtype does not belong to existing\_logtypes and \_supports\_log\_clearing(logtype)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in logtype does not belong to existing\_logtypes → \_supports\_log\_clearing(logtype).
    - If not Platform.db.exists(“DocType”, logtype).
      - Continue with the next iteration or loop test.
    - Evaluate self.append(“logs\_to\_clear”, mapping(“ref\_doctype” → logtype, “days” → cint(retentions at negative 1))).
    - Evaluate added\_logtypes.add(logtype).
- If added\_logtypes.
  - Evaluate Platform.msgprint(translated “Added default log doctypes: {}”.format(“,”.join(added\_logtypes)), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“default\_log\_clearing\_doctypes”, mapping()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L971) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1647)

<a id="op-f5277b21509ddd"></a>
### Log Settings.clear logs

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_settings_clear_logs`

**Inputs** self.

**State and service calls** commit.

**Local steps**

- For each entry in self.logs\_to\_clear.
  - Set controller from get\_controller(entry.ref\_doctype).
  - Set func from controller.clear\_old\_logs.
  - Set kwargs from Platform.get\_newargs(func, mapping(“days” → entry.days)).
  - Evaluate func(expanded names kwargs).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_controller(entry.ref\_doctype).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L1429) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1693) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1648)

<a id="op-b9ffbdcb4e17a2"></a>
### Log Settings.register doctype

`operation_foundation_core_record_definitions_log_settings_business_behavior_log_settings_register_record_type`

**Inputs** self, doctype, days = 30.

**Local steps**

- Set existing\_logtypes from set of d.ref\_doctype for d drawn from self.logs\_to\_clear.
  - Draw d from self.logs\_to\_clear.
- If (doctype does not belong to existing\_logtypes and \_supports\_log\_clearing(doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype does not belong to existing\_logtypes → \_supports\_log\_clearing(doctype).
  - Evaluate self.append(“logs\_to\_clear”, mapping(“ref\_doctype” → doctype, “days” → cint(days))).
- Otherwise.
  - For each entry in self.logs\_to\_clear.
    - If entry.ref\_doctype equals doctype.
      - Set entry.days from days.
      - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L1629) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1650)

<a id="op-bbf480f0ea40d9"></a>
### Run log clean up

`operation_foundation_core_record_definitions_log_settings_business_behavior_run_log_clean_up`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Log Settings” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Log Settings”).
- Evaluate doc.remove\_unsupported\_doctypes().
- Evaluate doc.add\_default\_logtypes().
- Evaluate doc.save().
- Evaluate doc.clear\_logs().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L1914) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1654)

<a id="op-3510cc440f9071"></a>
### Has unseen error log

`operation_foundation_core_record_definitions_log_settings_business_behavior_has_unseen_error_log`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Error Log” via get\_all.

**Explicit results** mapping(“show\_alert” → true, “message” → translated “You have unseen {0}”.format(text in the contract)).

**Local steps**

- If Platform.get\_all(“Error Log”, filters = mapping(“seen” → 0), limit = 1).
  - Return mapping(“show\_alert” → true, “message” → translated “You have unseen {0}”.format(text in the contract)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L2043) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1646)

<a id="op-07025830b7bcb0"></a>
### Get log doctypes

`operation_foundation_core_record_definitions_log_settings_business_behavior_get_log_record_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “DocType” via get\_list.

**Explicit results** supported\_doctypes at slice start to page\_len.

**Local steps**

- Set filters from (filters or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → list().
- Evaluate filters.extend(list(list(“istable”, “=”, 0), list(“issingle”, “=”, 0), list(“name”, “like”, formatted text %%{txt}%%))).
- Set doctypes from Platform.get\_list(“DocType”, filters = filters, pluck = “name”).
- Set supported\_doctypes from list of tuple(d) for d drawn from doctypes where \_supports\_log\_clearing(d).
  - Draw d from doctypes, keep a combination only if (\_supports\_log\_clearing(d)).
- Return supported\_doctypes at slice start to page\_len.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L2219) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1645)

<a id="op-fb427f7b419fb6"></a>
### Clear log table

`operation_foundation_core_record_definitions_log_settings_business_behavior_clear_log_table`

**Inputs** doctype, days = 90.

**State and service calls** execute a supplied database query · rollback · commit.

**Explicit failure paths** Platform.ValidationError(formatted text Unsupported logging DocType: {doctype}) · propagate active failure.

**Local steps**

- Bind dependencies get\_table\_name.
- If doctype does not belong to Platform.get\_hooks(“default\_log\_clearing\_doctypes”, mapping()).
  - Raise Platform.ValidationError(formatted text Unsupported logging DocType: {doctype}).
- Set original from get\_table\_name(doctype).
- Set temporary from formatted text {original} temp\_table.
- Set backup from formatted text {original} backup\_table.
- Attempt the following.
  - If Platform.db.db\_type equals “postgres”.
    - Evaluate Platform.db.sql\_ddl(formatted text CREATE TABLE "{temporary}" (LIKE "{original}" INCLUDING ALL)).
    - Evaluate Platform.db.sql(formatted text INSERT INTO "{temporary}"  SELECT \* FROM "{original}"  WHERE "{original}"."creation" &gt; NOW() - INTERVAL '{days}' DAY).
    - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE "{original}" RENAME TO "{backup}").
    - Evaluate Platform.db.sql\_ddl(formatted text ALTER TABLE "{temporary}" RENAME TO "{original}").
  - Otherwise.
    - If Platform.db.db\_type equals “mariadb”.
      - Evaluate Platform.db.sql\_ddl(formatted text CREATE TABLE ′{temporary}′ LIKE ′{original}′).
      - Evaluate Platform.db.sql(formatted text INSERT INTO ′{temporary}′  SELECT \* FROM ′{original}′  WHERE ′{original}′.′creation′ &gt; NOW() - INTERVAL '{days}' DAY).
      - Evaluate Platform.db.sql\_ddl(formatted text RENAME TABLE ′{original}′ TO ′{backup}′, ′{temporary}′ TO ′{original}′).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.db.sql\_ddl(formatted text DROP TABLE IF EXISTS ′{temporary}′).
  - Propagate the active failure.
- When the protected block completes normally.
  - Evaluate Platform.db.sql\_ddl(formatted text DROP TABLE ′{backup}′).
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“default\_log\_clearing\_doctypes”, mapping()).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L80) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1644)

## Service · Mapper

<a id="op-7e15d8caf73774"></a>
### Make mapped doc

`operation_foundation_model_mapper_business_behavior_make_mapped_record`

**Inputs** method, source\_name, selected\_children = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** method(source\_name).

**Local steps**

- Set resolved\_method\_path from Platform.override\_whitelisted\_method(method).
- Set method from Platform.get\_attr(resolved\_method\_path).
- Evaluate Platform.is\_whitelisted(method).
- If selected\_children.
  - Set selected\_children from json.loads(selected\_children).
- If args.
  - Set Platform.flags.args from Platform.\_dict(json.loads(args)).
- Set Platform.flags.selected\_children from (selected\_children or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in selected\_children → no value.
- Return method(source\_name).

**Values supplied outside this operation** selected callable from Platform.get\_attr(resolved\_method\_path).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L97) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1093)

<a id="op-4d348cca2e4f72"></a>
### Map docs

`operation_foundation_model_mapper_business_behavior_map_records`

**Inputs** method, source\_names, target\_doc, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** target\_doc.

**Local steps**

- Set resolved\_method\_path from Platform.override\_whitelisted\_method(method).
- Set method from Platform.get\_attr(resolved\_method\_path).
- Evaluate Platform.is\_whitelisted(method).
- For each src in json.loads(source\_names).
  - Set \_args from tuple(src, target\_doc, json.loads(args)) when args, otherwise tuple(src, target\_doc).
    - Value choice on args — true gives tuple(src, target\_doc, json.loads(args)), false gives tuple(src, target\_doc).
  - Set target\_doc from method(expanded \_args).
- Return target\_doc.

**Values supplied outside this operation** selected callable from Platform.get\_attr(resolved\_method\_path).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L100) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L501) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1098)

<a id="op-0d724f0b894332"></a>
### Get mapped doc

`operation_foundation_model_mapper_business_behavior_get_mapped_record`

**Inputs** from\_doctype, from\_docname, table\_maps, target\_doc = no value, postprocess = no value, ignore\_permissions = false, ignore\_child\_tables = false, cached = false.

**Record and data access** resolve a document from json.loads(target\_parent) via get\_doc · resolve a document from json.loads(target\_doc) via get\_doc · resolve a document from from\_doctype via get\_cached\_doc · resolve a document from from\_doctype via get\_doc.

**State and service calls** request new\_doc for target\_doctype.

**Explicit results** ret\_doc.

**Local steps**

- Set apply\_strict\_user\_permissions from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).
- If not target\_doc.
  - Set target\_doctype from table\_maps at from\_doctype at “doctype”.
  - If table\_maps at from\_doctype.get(“on\_parent”).
    - Set target\_parent from table\_maps at from\_doctype.get(“on\_parent”).
    - If isinstance(target\_parent, str).
      - Set target\_parent from Platform.get\_doc(json.loads(target\_parent)).
    - Set target\_parentfield from target\_parent.get\_parentfield\_of\_doctype(target\_doctype).
    - Set target\_doc from Platform.new\_doc(target\_doctype, parent\_doc = target\_parent, parentfield = target\_parentfield).
    - Evaluate target\_parent.append(target\_parentfield, target\_doc).
    - Set ret\_doc from target\_parent.
  - Otherwise.
    - Set target\_doc from Platform.new\_doc(target\_doctype).
    - Set ret\_doc from target\_doc.
- Otherwise.
  - If isinstance(target\_doc, str).
    - Set target\_doc from Platform.get\_doc(json.loads(target\_doc)).
    - Set ret\_doc from target\_doc.
  - Otherwise.
    - Set ret\_doc from target\_doc.
- If (not apply\_strict\_user\_permissions and not ignore\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not apply\_strict\_user\_permissions → not ignore\_permissions.
  - Evaluate target\_doc.check\_permission(“create”).
- If cached.
  - Set source\_doc from Platform.get\_cached\_doc(from\_doctype, from\_docname).
- Otherwise.
  - Set source\_doc from Platform.get\_doc(from\_doctype, from\_docname).
- If not ignore\_permissions.
  - Evaluate source\_doc.check\_permission(“read”).
- Evaluate ret\_doc.run\_method(“before\_mapping”, source\_doc, table\_maps).
- Evaluate map\_doc(source\_doc, target\_doc, table\_maps at source\_doc.doctype).
- Set row\_exists\_for\_parentfield from mapping().
- If not ignore\_child\_tables.
  - For each df in source\_doc.meta.get\_table\_fields().
    - Set source\_child\_doctype from df.options.
    - Set table\_map from table\_maps.get(source\_child\_doctype).
    - If not table\_map.
      - Set target\_df from target\_doc.meta.get\_field(df.fieldname).
      - If target\_df.
        - Set target\_child\_doctype from target\_df.options.
        - If (target\_df and target\_child\_doctype equals source\_child\_doctype and not df.no\_copy and not target\_df.no\_copy).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in target\_df → target\_child\_doctype equals source\_child\_doctype → not df.no\_copy → not target\_df.no\_copy.
          - Set table\_map from mapping(“doctype” → target\_child\_doctype).
    - If table\_map.
      - Set target\_child\_doctype from table\_map at “doctype”.
      - Set target\_parentfield from target\_doc.get\_parentfield\_of\_doctype(target\_child\_doctype).
      - If table\_map.get(“reset\_value”).
        - Evaluate setattr(target\_doc, target\_parentfield, list()).
      - For each source\_d in source\_doc.get(df.fieldname).
        - If “condition” belongs to table\_map.
          - If not table\_map at “condition”(source\_d).
            - Continue with the next iteration or loop test.
        - If (Platform.flags.selected\_children and df.fieldname belongs to Platform.flags.selected\_children and source\_d.name does not belong to Platform.flags.selected\_children at df.fieldname).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.selected\_children → df.fieldname belongs to Platform.flags.selected\_children → source\_d.name does not belong to Platform.flags.selected\_children at df.fieldname.
          - Continue with the next iteration or loop test.
        - If target\_parentfield does not belong to row\_exists\_for\_parentfield.
          - Set row\_exists\_for\_parentfield at target\_parentfield from true when target\_doc.get(target\_parentfield), otherwise false.
            - Value choice on target\_doc.get(target\_parentfield) — true gives true, false gives false.
        - If table\_map.get(“ignore”).
          - Continue with the next iteration or loop test.
        - If (table\_map.get(“add\_if\_empty”) and row\_exists\_for\_parentfield.get(target\_parentfield)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_map.get(“add\_if\_empty”) → row\_exists\_for\_parentfield.get(target\_parentfield).
          - Continue with the next iteration or loop test.
        - If (table\_map.get(“filter”) and table\_map.get(“filter”)(source\_d)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_map.get(“filter”) → table\_map.get(“filter”)(source\_d).
          - Continue with the next iteration or loop test.
        - Evaluate map\_child\_doc(source\_d, target\_doc, table\_map, source\_doc).
- If postprocess.
  - Evaluate postprocess(source\_doc, target\_doc).
- Evaluate ret\_doc.run\_method(“after\_mapping”, source\_doc).
- Evaluate ret\_doc.set\_onload(“load\_after\_mapping”, true).
- If (apply\_strict\_user\_permissions and not ignore\_permissions).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in apply\_strict\_user\_permissions → not ignore\_permissions.
  - Evaluate ret\_doc.check\_permission(“create”).
- Return ret\_doc.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”), Platform.get\_cached\_doc(from\_doctype, from\_docname) · effective access from target\_doc.check\_permission(“create”), source\_doc.check\_permission(“read”) and 1 further calls · selected callable from ret\_doc.run\_method(“before\_mapping”, source\_doc, table\_maps), ret\_doc.run\_method(“after\_mapping”, source\_doc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L96) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1092)

<a id="op-c72fb0a8819d3d"></a>
### Map doc

`operation_foundation_model_mapper_business_behavior_map_record`

**Inputs** source\_doc, target\_doc, table\_map, source\_parent = no value.

**Explicit failure paths** validation helper — (translated “Cannot map because following condition fails:” + formatted text  {key}={cstr(condition at 1)}).

**Local steps**

- If table\_map.get(“validation”).
  - For each tuple(key, condition) in table\_map at “validation”.items().
    - If (condition at 0 equals “=” and source\_doc.get(key) differs from condition at 1).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in condition at 0 equals “=” → source\_doc.get(key) differs from condition at 1.
      - Call the validation error handler Platform.throw((translated “Cannot map because following condition fails:” + formatted text  {key}={cstr(condition at 1)})).
- Evaluate map\_fields(source\_doc, target\_doc, table\_map, source\_parent).
- If “postprocess” belongs to table\_map.
  - Evaluate table\_map at “postprocess”(source\_doc, target\_doc, source\_parent).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L5584) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1097)

<a id="op-76a2b25611af11"></a>
### Map fields

`operation_foundation_model_mapper_business_behavior_map_fields`

**Inputs** source\_doc, target\_doc, table\_map, source\_parent.

**Local steps**

- Set no\_copy\_fields from set(((((list of nested operand in the contract.fieldname for d drawn from nested operand in the contract(nested operand in the contract) where (nested operand in the contract or nested operand in the contract) …).
  - Draw d from source\_doc.meta.get(“fields”), keep a combination only if ((d.no\_copy equals 1 or d.fieldtype belongs to table\_fields)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.no\_copy equals 1 → d.fieldtype belongs to table\_fields.
  - Draw d from target\_doc.meta.get(“fields”), keep a combination only if (d.fieldtype belongs to table\_fields).
- For each df in target\_doc.meta.get(“fields”).
  - If df.fieldname does not belong to no\_copy\_fields.
    - Set val from source\_doc.get(df.fieldname).
    - If val does not belong to tuple(no value, empty text).
      - Evaluate target\_doc.set(df.fieldname, val).
    - Otherwise.
      - If df.fieldtype equals “Link”.
        - If not target\_doc.get(df.fieldname).
          - If df.options equals source\_doc.doctype.
            - Evaluate target\_doc.set(df.fieldname, source\_doc.name).
          - Otherwise.
            - If (source\_parent and df.options equals source\_parent.doctype).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in source\_parent → df.options equals source\_parent.doctype.
              - Evaluate target\_doc.set(df.fieldname, source\_parent.name).
- Set field\_map from table\_map.get(“field\_map”).
- If field\_map.
  - If isinstance(field\_map, dict).
    - For each tuple(source\_key, target\_key) in field\_map.items().
      - Set val from source\_doc.get(source\_key).
      - If val does not belong to tuple(no value, empty text).
        - Evaluate target\_doc.set(target\_key, val).
  - Otherwise.
    - For each fmap in field\_map.
      - Set val from source\_doc.get(fmap at 0).
      - If val does not belong to tuple(no value, empty text).
        - Evaluate target\_doc.set(fmap at 1, val).
- If source\_doc.idx.
  - Set target\_doc.idx from source\_doc.idx.
- For each df in target\_doc.meta.get(“fields”, mapping(“fieldtype” → “Link”)).
  - If target\_doc.get(df.fieldname).
    - Evaluate map\_fetch\_fields(target\_doc, df, no\_copy\_fields).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L5970) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1096)

<a id="op-d0c8097336e6ef"></a>
### Map fetch fields

`operation_foundation_model_mapper_business_behavior_map_fetch_fields`

**Inputs** target\_doc, df, no\_copy\_fields.

**Record and data access** resolve a document from df.options via get\_doc.

**Explicit results** no value.

**Local steps**

- Set linked\_doc from no value.
- For each fetch\_df in target\_doc.meta.get(“fields”, mapping(“fetch\_from” → formatted text ^{df.fieldname}.)).
  - If ((not target\_doc.get(fetch\_df.fieldname) or fetch\_df.fieldtype equals “Read Only”) and fetch\_df.fieldname does not belong to no\_copy\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (not target\_doc.get(fetch\_df.fieldname) or fetch\_df.fieldtype equals “Read Only”) → fetch\_df.fieldname does not belong to no\_copy\_fields.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not target\_doc.get(fetch\_df.fieldname) → fetch\_df.fieldtype equals “Read Only”.
    - Set source\_fieldname from fetch\_df.fetch\_from.split(“.”) at 1.
    - If not linked\_doc.
      - Attempt the following.
        - Set linked\_doc from Platform.get\_doc(df.options, target\_doc.get(df.fieldname)).
      - On failure (Exception).
        - Return no value.
    - Set val from linked\_doc.get(source\_fieldname).
    - If val does not belong to tuple(no value, empty text).
      - Evaluate target\_doc.set(fetch\_df.fieldname, val).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L99) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1095)

<a id="op-b396a04ba9675f"></a>
### Map child doc

`operation_foundation_model_mapper_business_behavior_map_child_record`

**Inputs** source\_d, target\_parent, table\_map, source\_parent = no value.

**State and service calls** request new\_doc for target\_child\_doctype.

**Explicit results** target\_d.

**Local steps**

- Set target\_child\_doctype from table\_map at “doctype”.
- Set target\_parentfield from target\_parent.get\_parentfield\_of\_doctype(target\_child\_doctype).
- Set target\_d from Platform.new\_doc(target\_child\_doctype, parent\_doc = target\_parent, parentfield = target\_parentfield).
- Evaluate map\_doc(source\_d, target\_d, table\_map, source\_parent).
- Set target\_d.idx from no value.
- Evaluate target\_parent.append(target\_parentfield, target\_d).
- Return target\_d.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L98) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1094)
