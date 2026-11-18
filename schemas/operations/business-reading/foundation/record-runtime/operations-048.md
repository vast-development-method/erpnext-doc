# Record lifecycle and persistence · operations 48

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-f89dcd40f8d59e"></a>
### Unlock document

`operation_foundation_model_document_business_behavior_unlock_document`

**Inputs** doctype, name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** msgprint with Platform.\_(“Document Unlocked”).

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name).
- Evaluate doc.check\_permission(“write”).
- Evaluate doc.unlock().
- Evaluate Platform.msgprint(Platform.\_(“Document Unlocked”), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L94) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1083)

<a id="op-b01c2a072fd985"></a>
### Get lazy controller

`operation_foundation_model_document_business_behavior_get_lazy_controller`

**Inputs** doctype, site (named only, default no value), meta (named only, default no value), controller (named only, default no value).

**Explicit results** original\_controller · lazy\_controllers at doctype.

**Local steps**

- Set lazy\_controllers from Platform.lazy\_controllers.setdefault((site or Platform.local.site), mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.
- If doctype does not belong to lazy\_controllers.
  - If meta is identical to no value.
    - Set meta from Platform.get\_meta(doctype).
  - Set original\_controller from (controller or get\_controller(doctype)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in controller → get\_controller(doctype).
  - If meta.is\_virtual.
    - Set lazy\_controllers at doctype from original\_controller.
    - Evaluate warnings.warn(formatted text Virtual doctypes don't support lazy loading: {doctype}, stacklevel = 3).
    - Return original\_controller.
  - Set lazy\_controller from type(formatted text Lazy{original\_controller.\_\_name\_\_}, tuple(LazyDocument, original\_controller), mapping()).
  - For each df in meta.get\_table\_fields().
    - Evaluate setattr(lazy\_controller, df.fieldname, LazyChildTable(df.fieldname, df.options)).
  - Set lazy\_controllers at doctype from lazy\_controller.
- Return lazy\_controllers at doctype.

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L4861) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1058)

<a id="op-272cabe5ab4a55"></a>
### Reconstruct lazy doc

`operation_foundation_model_document_business_behavior_reconstruct_lazy_record`

**Inputs** site, doctype, meta, original\_controller.

**Explicit results** controller.\_\_new\_\_(controller).

**Local steps**

- Set controller from get\_lazy\_controller(doctype, site = site, meta = meta, controller = original\_controller).
- Return controller.\_\_new\_\_(controller).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L5354) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1081)

<a id="op-48f7abd374cfd2"></a>
### Lazy Document.reduce

`operation_foundation_model_document_business_behavior_lazy_document_reduce`

**Inputs** self.

**Explicit results** tuple(\_reconstruct\_lazy\_doc, tuple(Platform.local.site, self.doctype, self.meta, original\_controller), self.\_\_getstate\_\_()).

**Local steps**

- Set original\_controller from type(self).\_\_bases\_\_ at 1.
- Return tuple(\_reconstruct\_lazy\_doc, tuple(Platform.local.site, self.doctype, self.meta, original\_controller), self.\_\_getstate\_\_()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L5498) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1079)

<a id="op-61d694b2e44d7e"></a>
### Lazy Document.load children from db

`operation_foundation_model_document_business_behavior_lazy_document_load_children_from_database`

**Inputs** self.

**Wrappers, in declaration order** override.

**Local steps**

- For each fieldname in self.\_table\_fieldnames.
  - Evaluate self.\_\_dict\_\_.pop(fieldname, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L5629) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1078)

<a id="op-7eb4112d4d05c7"></a>
### Lazy Document.get

`operation_foundation_model_document_business_behavior_lazy_document_get`

**Inputs** self, key, filters = no value, limit = no value, default = no value.

**Wrappers, in declaration order** override.

**Explicit results** super().get(key, filters, limit, default).

**Local steps**

- If (isinstance(key, str) and key belongs to self.\_table\_fieldnames).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(key, str) → key belongs to self.\_table\_fieldnames.
  - Evaluate getattr(self, key, no value).
- Return super().get(key, filters, limit, default).

**Values supplied outside this operation** selected callable from getattr(self, key, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L5719) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1076)

<a id="op-c41843ab6c1d61"></a>
### Lazy Document.append

`operation_foundation_model_document_business_behavior_lazy_document_append`

**Inputs** self, key, value = no value, position = negative 1.

**Wrappers, in declaration order** override.

**Declared result** D.

**Explicit results** super().append(key, value, position).

**Local steps**

- If key does not belong to self.\_\_dict\_\_.
  - Evaluate getattr(self, key, no value).
- Return super().append(key, value, position).

**Values supplied outside this operation** selected callable from getattr(self, key, no value).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L5917) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1074)

<a id="op-8fa48f0fc1651e"></a>
### Lazy Document.db update all

`operation_foundation_model_document_business_behavior_lazy_document_database_update_all`

**Inputs** self.

**Wrappers, in declaration order** override.

**State and service calls** call db\_update on self · call db\_update on doc.

**Local steps**

- Evaluate self.db\_update().
- For each fieldname in self.\_table\_fieldnames.
  - If fieldname does not belong to self.\_\_dict\_\_.
    - Continue with the next iteration or loop test.
  - For each doc in self.get(fieldname).
    - Evaluate doc.db\_update().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-048.md#op-7eb4112d4d05c7).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L6110) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1075)

<a id="op-d799f4f5c6b818"></a>
### Lazy Document.init child tables

`operation_foundation_model_document_business_behavior_lazy_document_initialize_child_tables`

**Inputs** self.

**Wrappers, in declaration order** override.

**Explicit results** no value.

**Local steps**

- Return no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L6264) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1077)

<a id="op-3215e319a371e2"></a>
### Lazy Child Table.initialize

`operation_foundation_model_document_business_behavior_lazy_child_table_initialize`

**Inputs** self, fieldname, doctype.

**Declared result** no value.

**Local steps**

- Set self.fieldname from fieldname.
- Set self.doctype from doctype.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L6305) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L469) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1073)

<a id="op-82c2427f8097e5"></a>
### Lazy Child Table.get

`operation_foundation_model_document_business_behavior_lazy_child_table_get`

**Inputs** self, doc, objtype = no value.

**Explicit results** \_\_dict at fieldname.

**Local steps**

- Set fieldname from self.fieldname.
- Set \_\_dict from doc.\_\_dict\_\_.
- Require fieldname does not belong to \_\_dict or report “Descriptor should not override existing values”.
- Set children from (doc.\_load\_child\_table\_from\_db(fieldname, self.doctype) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.\_load\_child\_table\_from\_db(fieldname, self.doctype) → list().
- Set \_\_dict at fieldname from list().
- Evaluate doc.extend(fieldname, children).
- Return \_\_dict at fieldname.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L93) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1072)

<a id="op-5b16eb70613be0"></a>
### Copy doc

`operation_foundation_model_document_business_behavior_copy_record`

**Inputs** doc, ignore\_no\_copy = true.

**Declared result** “Document”.

**Explicit results** newdoc.

**Local steps**

- Bind dependencies copy.
- Bind dependencies MappingProxyType.
- Bind local operation remove\_no\_copy\_fields for subsequent calls.
- Set fields\_to\_clear from list(“name”, “owner”, “creation”, “modified”, …).
- If not Platform.in\_test.
  - Evaluate fields\_to\_clear.append(“docstatus”).
- If isinstance(doc, Document).
  - Set d from doc.as\_dict().
- Otherwise.
  - If isinstance(doc, MappingProxyType).
    - Set d from dict(doc).
  - Otherwise.
    - Set d from doc.
- Set newdoc from get\_doc(copy.deepcopy(d)).
- Evaluate newdoc.set(“\_\_islocal”, 1).
- For each fieldname in list(expanded fields\_to\_clear, “amended\_from”, “amendment\_date”).
  - Evaluate newdoc.set(fieldname, no value).
- If not ignore\_no\_copy.
  - Evaluate remove\_no\_copy\_fields(newdoc).
- For each d in newdoc.get\_all\_children().
  - Evaluate d.set(“\_\_islocal”, 1).
  - For each fieldname in fields\_to\_clear.
    - Evaluate d.set(fieldname, no value).
  - If not ignore\_no\_copy.
    - Evaluate remove\_no\_copy\_fields(d).
- Return newdoc.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L72) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L942)

<a id="op-b1e4f957ebdd56"></a>
### Copy doc.remove no copy fields

`operation_foundation_model_document_business_behavior_copy_record_remove_number_copy_fields`

**Inputs** d.

**Local steps**

- For each df in d.meta.get(“fields”, mapping(“no\_copy” → 1)).
  - If hasattr(d, df.fieldname).
    - Evaluate d.set(df.fieldname, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L7358) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L943)

<a id="op-9935ae68cc6cd1"></a>
### New doc

`operation_foundation_model_document_business_behavior_new_record`

**Inputs** doctype, parent\_doc (named only, default no value), parentfield (named only, default no value), as\_dict (named only, default false), remaining named values kwargs.

**Declared result** “Document”.

**Explicit results** new\_doc.update(kwargs).

**Local steps**

- Bind dependencies get\_new\_doc.
- Set new\_doc from get\_new\_doc(doctype, parent\_doc, parentfield, as\_dict = as\_dict).
- Return new\_doc.update(kwargs).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L7510) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1080)

<a id="op-b1d2141ff646c9"></a>
### Get cached doc

`operation_foundation_model_document_business_behavior_get_cached_record`

**Inputs** remaining positional values args, remaining named values kwargs.

**Declared result** “Document”.

**Explicit results** doc.

**Local steps**

- If (key bound to can\_cache\_doc(args) and doc bound to Platform.cache.get\_value(key)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in key bound to can\_cache\_doc(args) → doc bound to Platform.cache.get\_value(key).
  - Return doc.
- Set doc from get\_doc(expanded args, expanded names kwargs).
- If not key.
  - Set key from get\_document\_cache\_key(doc.doctype, doc.name).
- Evaluate \_set\_document\_in\_cache(key, doc).
- Return doc.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0281.json#L7663) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1054)

<a id="op-6fde1bad2f2b11"></a>
### Set document in cache

`operation_foundation_model_document_business_behavior_set_document_in_cache`

**Inputs** key, doc.

**Declared result** no value.

**Local steps**

- Evaluate Platform.cache.set\_value(key, doc, expires\_in\_sec = 3600).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1082)

<a id="op-c0e2603aa7337b"></a>
### Can cache doc

`operation_foundation_model_document_business_behavior_can_cache_record`

**Inputs** args.

**Declared result** (str bitwise or no value).

**Explicit results** no value · get\_document\_cache\_key(doctype, name).

**Local steps**

- If not args.
  - Return no value.
- Set doctype from args at 0.
- Set name from doctype when (len(args) equals 1 or args at 1 is identical to no value), otherwise args at 1.
  - Value choice on (len(args) equals 1 or args at 1 is identical to no value) — true gives doctype, false gives args at 1.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(args) equals 1 → args at 1 is identical to no value.
- If (isinstance(doctype, str) and isinstance(name, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(doctype, str) → isinstance(name, str).
  - Return get\_document\_cache\_key(doctype, name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L98) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L939)

<a id="op-87242c19ce4e95"></a>
### Get document cache key

`operation_foundation_model_document_business_behavior_get_document_cache_key`

**Inputs** doctype, name.

**Explicit results** formatted text document\_cache::{doctype}::{name}.

**Local steps**

- Return formatted text document\_cache::{doctype}::{name}.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L339) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1056)

<a id="op-8fc42b053d7170"></a>
### Clear document cache

`operation_foundation_model_document_business_behavior_clear_document_cache`

**Inputs** doctype, name = no value.

**Declared result** no value.

**Local steps**

- Evaluate Platform.db.value\_cache.pop(doctype, no value).
- Bind local operation clear\_in\_redis for subsequent calls.
- Evaluate clear\_in\_redis().
- If hasattr(Platform.db, “after\_commit”).
  - Evaluate Platform.db.after\_commit.add(clear\_in\_redis).
  - Evaluate Platform.db.after\_rollback.add(clear\_in\_redis).
- If (doctype equals “System Settings” and hasattr(Platform.local, “system\_settings”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “System Settings” → hasattr(Platform.local, “system\_settings”).
  - Evaluate delattr(Platform.local, “system\_settings”).
- If (doctype equals “Website Settings” and hasattr(Platform.local, “website\_settings”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Website Settings” → hasattr(Platform.local, “website\_settings”).
  - Evaluate delattr(Platform.local, “website\_settings”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L424) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L940)

<a id="op-05c9e7a845d117"></a>
### Clear document cache.clear in redis

`operation_foundation_model_document_business_behavior_clear_document_cache_clear_in_cache_service`

**Inputs** no declared parameters.

**Local steps**

- If name is distinct from no value.
  - Evaluate Platform.cache.delete\_value(get\_document\_cache\_key(doctype, name)).
- Otherwise.
  - Evaluate Platform.cache.delete\_keys(get\_document\_cache\_key(doctype, empty text)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L911) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L941)

<a id="op-bfabfadbf9331c"></a>
### Get cached value

`operation_foundation_model_document_business_behavior_get_cached_value`

**Inputs** doctype, name, fieldname = “name”, as\_dict = false.

**Declared result** Any.

**Explicit results** no value · doc.get(fieldname) · Platform.\_dict(zip(fieldname, values, strict = false)) · values.

**Explicit failure paths** validation helper — “Cannot make dict for single fieldname”.

**Local steps**

- Attempt the following.
  - Set doc from get\_cached\_doc(doctype, name).
- On failure (Platform.DoesNotExistError).
  - Evaluate Platform.clear\_last\_message().
  - Return no value.
- If isinstance(fieldname, str).
  - If as\_dict.
    - Call the validation error handler Platform.throw(“Cannot make dict for single fieldname”).
  - Return doc.get(fieldname).
- Set values from list of doc.get(f) for f drawn from fieldname.
  - Draw f from fieldname.
- If as\_dict.
  - Return Platform.\_dict(zip(fieldname, values, strict = false)).
- Return values.

**Values supplied outside this operation** configured or stored value from get\_cached\_doc(doctype, name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L1046) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1055)

<a id="op-b9ce3a9752547a"></a>
### Get single value

`operation_foundation_model_document_business_behavior_get_single_value`

**Inputs** setting (positional only), fieldname (positional only), as\_dict (named only, default false).

**Explicit results** get\_cached\_value(setting, setting, fieldname = fieldname, as\_dict = as\_dict).

**Local steps**

- Return get\_cached\_value(setting, setting, fieldname = fieldname, as\_dict = as\_dict).

**Values supplied outside this operation** configured or stored value from get\_cached\_value(setting, setting, fieldname = fieldname, as\_dict = as\_dict).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L1441) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1071)

<a id="op-c93b94295fbe83"></a>
### Get last doc

`operation_foundation_model_document_business_behavior_get_last_record`

**Inputs** doctype, filters = no value, order\_by = “creation desc”, for\_update (named only, default false).

**Record and data access** read doctype via get\_all.

**Explicit results** get\_doc(doctype, d at 0, for\_update = for\_update).

**Explicit failure paths** Platform.DoesNotExistError(doctype = doctype).

**Local steps**

- Set d from Platform.get\_all(doctype, filters = filters, limit\_page\_length = 1, order\_by = order\_by, pluck = “name”).
- If d.
  - Return get\_doc(doctype, d at 0, for\_update = for\_update).
- Otherwise.
  - Raise Platform.DoesNotExistError(doctype = doctype).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L1546) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1057)

<a id="op-6e0420a6d9feb0"></a>
### Get single

`operation_foundation_model_document_business_behavior_get_single`

**Inputs** doctype.

**Explicit results** get\_doc(doctype, doctype).

**Local steps**

- Return get\_doc(doctype, doctype).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0282.json#L1780) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L466) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1070)
