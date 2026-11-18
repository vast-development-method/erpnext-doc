# Record lifecycle and persistence · operations 40

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Document

<a id="op-92000f88191c3e"></a>
### Get doc str

`operation_foundation_model_document_business_behavior_get_record_text`

**Inputs** doctype, name = no value, remaining named values kwargs.

**Wrappers, in declaration order** get\_doc.register(str).

**Declared result** “Document”.

**Explicit results** get\_doc\_permission\_check(doc, kwargs.get(“check\_permission”)).

**Explicit failure paths** ImportError(doctype).

**Local steps**

- If controller bound to get\_controller(doctype).
  - Set doc from controller(doctype, name, expanded names kwargs).
  - Return get\_doc\_permission\_check(doc, kwargs.get(“check\_permission”)).
- Raise ImportError(doctype).

**Values supplied outside this operation** selected callable from get\_controller(doctype).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4683) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1069)

<a id="op-416bafc0016cb9"></a>
### Get doc from mapping proxy

`operation_foundation_model_document_business_behavior_get_record_from_mapping_proxy`

**Inputs** data, remaining named values kwargs.

**Wrappers, in declaration order** get\_doc.register(MappingProxyType).

**Declared result** “Document”.

**Explicit results** get\_doc\_from\_dict(dict(data), expanded names kwargs).

**Local steps**

- Return get\_doc\_from\_dict(dict(data), expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L4908) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1067)

<a id="op-756585693c27e2"></a>
### Get doc from dict

`operation_foundation_model_document_business_behavior_get_record_from_mapping`

**Inputs** data, remaining named values kwargs.

**Wrappers, in declaration order** get\_doc.register(dict).

**Declared result** “Document”.

**Explicit results** get\_doc\_permission\_check(doc, kwargs.get(“check\_permission”)).

**Explicit failure paths** ValueError(“"doctype" is a required key”) · ImportError(data at “doctype”).

**Local steps**

- If “doctype” does not belong to data.
  - Raise ValueError(“"doctype" is a required key”).
- If controller bound to get\_controller(data at “doctype”).
  - Set doc from controller(expanded names data).
  - Return get\_doc\_permission\_check(doc, kwargs.get(“check\_permission”)).
- Raise ImportError(data at “doctype”).

**Values supplied outside this operation** selected callable from get\_controller(data at “doctype”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L5018) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1066)

<a id="op-fdd0c96b6943a0"></a>
### Get lazy doc

`operation_foundation_model_document_business_behavior_get_lazy_record`

**Inputs** doctype, name, for\_update (named only, default no value), check\_permission (named only, default no value).

**Declared result** “Document”.

**Explicit results** get\_doc(doctype, name, check\_permission = check\_permission) · get\_doc\_permission\_check(doc, check\_permission).

**Explicit failure paths** ImportError(doctype).

**Local steps**

- If doctype equals “DocType”.
  - Evaluate warnings.warn(“DocType doesn't support lazy loading”, stacklevel = 1).
  - Return get\_doc(doctype, name, check\_permission = check\_permission).
- If controller bound to get\_lazy\_controller(doctype).
  - Set doc from controller(doctype, name, for\_update = for\_update).
  - Return get\_doc\_permission\_check(doc, check\_permission).
- Raise ImportError(doctype).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0275.json#L5301) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1059)

<a id="op-cf3ef17741cf6f"></a>
### Get doc permission check

`operation_foundation_model_document_business_behavior_get_record_permission_check`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, check\_permission.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L960) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1068)

<a id="op-bc2c5ef6b3a3e6"></a>
### Document Base.initialize

`operation_foundation_binding_foundation_model_document_documentbase_init`

**Inputs** self, d.

**Local steps**

- Bind dependencies deprecation\_warning.
- Evaluate record a compatibility advisory for the invoked interface.
- Evaluate self.init\_from\_dict(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L198) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1630)

<a id="op-e435e7d1389c91"></a>
### Document.initialize

`operation_foundation_model_document_business_behavior_document_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** no value.

**Explicit failure paths** ValueError(“Illegal arguments”).

**Local steps**

- Set self.doctype from no value.
- Set self.name from no value.
- Set self.flags from Platform.\_dict().
- If args.
  - Set first\_arg from args at 0.
  - If isinstance(first\_arg, str).
    - Set self.doctype from first\_arg.
    - Set self.name from first\_arg when len(args) equals 1, otherwise args at 1.
      - Value choice on len(args) equals 1 — true gives first\_arg, false gives args at 1.
    - Set self.flags.for\_update from kwargs.get(“for\_update”, false).
    - Evaluate self.load\_from\_db().
    - Return no value.
  - If isinstance(first\_arg, dict).
    - Set kwargs from first\_arg.
- If kwargs.
  - Evaluate self.init\_from\_dict(kwargs).
  - Evaluate self.init\_child\_tables().
  - Evaluate self.init\_valid\_columns().
  - Return no value.
- Raise ValueError(“Illegal arguments”).

**Methods declared on this owner** [load from db](operations-040.md#op-923c03d02e51cf), [init from dict](operations-040.md#op-c79f82f915c986), [init child tables](operations-045.md#op-fa5f865a65cb4e), [init valid columns](operations-045.md#op-7a338f17f8457f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L76) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L377) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L988)

<a id="op-c79f82f915c986"></a>
### Document.init from dict

`operation_foundation_binding_foundation_model_document_document_init_from_dict`

**Inputs** self, d.

**Declared result** no value.

**Local steps**

- If d.get(“doctype”).
  - Set self.doctype from d at “doctype”.
- Evaluate self.update(d).
- Set self.dont\_update\_if\_missing from list().
- If hasattr(self, “\_\_setup\_\_”).
  - Evaluate self.\_\_setup\_\_().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update](operations-045.md#op-b90034268a7194).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L164) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1596)

<a id="op-01e6f7f3320f1b"></a>
### Document.is locked

`operation_foundation_model_document_business_behavior_document_is_locked`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** false · true.

**Local steps**

- Set signature from self.get\_signature().
- If not file\_lock.lock\_exists(signature).
  - Return false.
- If file\_lock.lock\_age(signature) &gt; DOCUMENT\_LOCK\_EXPIRY.
  - Return false.
- Return true.

**Methods declared on this owner** [get signature](operations-044.md#op-8c487683e98ecb).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L2864) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L380) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L991)

<a id="op-923c03d02e51cf"></a>
### Document.load from db

`operation_foundation_model_document_business_behavior_document_load_from_database`

**Inputs** self.

**Declared result** “Self”.

**Record and data access** execute query text (SELECT).format(table\_name = get\_table\_name(self.doctype, wrap\_in\_backticks = true), for\_update = for\_update) · read self.doctype via get\_value.

**State and service calls** request new\_doc for self.doctype.

**Explicit results** self.

**Explicit failure paths** validation helper with Platform.DoesNotExistError(doctype = self.doctype) — translated “{0} {1} not found”.format(translated self.doctype, self.name).

**Local steps**

- Set is\_doctype from self.doctype equals “DocType”.
- Set self.flags.ignore\_children from true.
- If (not is\_doctype and self.meta.issingle).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_doctype → self.meta.issingle.
  - Set single\_doc from Platform.db.get\_singles\_dict(self.doctype, for\_update = self.flags.for\_update).
  - If not single\_doc.
    - Set single\_doc from Platform.new\_doc(self.doctype, as\_dict = true).
    - Set single\_doc at “name” from self.doctype.
    - Remove single\_doc at “\_\_islocal”.
  - Evaluate self.init\_from\_dict(single\_doc).
  - Evaluate self.init\_valid\_columns().
  - Evaluate self.\_fix\_numeric\_types().
- Otherwise.
  - If (not is\_doctype and isinstance(self.name, (str bitwise or int))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_doctype → isinstance(self.name, (str bitwise or int)).
    - Set for\_update from empty text.
    - If (self.flags.for\_update and Platform.db.db\_type differs from “sqlite”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.for\_update → Platform.db.db\_type differs from “sqlite”.
      - Set for\_update from “FOR UPDATE”.
    - Set d from Platform.db.sql(query text (SELECT).format(table\_name = get\_table\_name(self.doctype, wrap\_in\_backticks = true), for\_update = for\_update), self.name, as\_dict = true).
    - Set d from d at 0 when d, otherwise d.
      - Value choice on d — true gives d at 0, false gives d.
  - Otherwise.
    - Set d from Platform.db.get\_value(doctype = self.doctype, filters = self.name, fieldname = “\*”, for\_update = self.flags.for\_update, …).
  - If not d.
    - Call the validation error handler Platform.throw(translated “{0} {1} not found”.format(translated self.doctype, self.name), Platform.DoesNotExistError(doctype = self.doctype)).
  - Evaluate self.init\_from\_dict(d).
- Evaluate self.flags.pop(“ignore\_children”, no value).
- Evaluate self.load\_children\_from\_db().
- If hasattr(self, “\_\_setup\_\_”).
  - Evaluate self.\_\_setup\_\_().
- Return self.

**Methods declared on this owner** [init from dict](operations-040.md#op-c79f82f915c986), [init valid columns](operations-045.md#op-7a338f17f8457f), [fix numeric types](operations-046.md#op-54f49255e9ad2e), [load children from db](operations-040.md#op-1d4d9c21c2a1cc).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L77) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L384) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L995)

<a id="op-5322bfe17ba85d"></a>
### Document.mask fields

`operation_foundation_model_document_business_behavior_document_mask_fields`

**Inputs** self.

**Local steps**

- Bind dependencies mask\_field\_value.
- Set mask\_fields from Platform.get\_meta(self.doctype).get\_masked\_fields().
- If mask\_fields.
  - Set self.flags.masked\_fieldnames from set of field.fieldname for field drawn from mask\_fields.
    - Draw field from mask\_fields.
- For each field in mask\_fields.
  - Set val from self.get(field.fieldname).
  - Evaluate self.set(field.fieldname, mask\_field\_value(field, val)).
- For each table\_field in self.meta.get\_table\_fields().
  - Set child\_mask\_fields from Platform.get\_meta(table\_field.options).get\_masked\_fields(parenttype = self.doctype).
  - If not child\_mask\_fields.
    - Continue with the next iteration or loop test.
  - Set masked\_fieldnames from set of field.fieldname for field drawn from child\_mask\_fields.
    - Draw field from child\_mask\_fields.
  - For each row in (self.get(table\_field.fieldname) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(table\_field.fieldname) → list().
    - Set row.flags.masked\_fieldnames from masked\_fieldnames.
    - For each field in child\_mask\_fields.
      - Evaluate row.set(field.fieldname, mask\_field\_value(field, row.get(field.fieldname))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L79) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L387) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L998)

<a id="op-1d4d9c21c2a1cc"></a>
### Document.load children from db

`operation_foundation_model_document_business_behavior_document_load_children_from_database`

**Inputs** self.

**Record and data access** read child\_doctype via get\_values.

**Explicit results** self.

**Local steps**

- Set is\_doctype from self.doctype equals “DocType”.
- For each tuple(fieldname, child\_doctype) in self.\_table\_fieldnames.items().
  - If (not is\_doctype and is\_virtual\_doctype(child\_doctype)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_doctype → is\_virtual\_doctype(child\_doctype).
    - Evaluate self.\_\_dict\_\_.pop(fieldname, no value).
    - Continue with the next iteration or loop test.
  - If is\_doctype.
    - Set children from Platform.db.get\_values(child\_doctype, mapping(“parent” → self.name, “parenttype” → self.doctype, “parentfield” → fieldname), “\*”, as\_dict = true, order\_by = “idx asc”, for\_update = self.flags.for\_update).
  - Otherwise.
    - Set children from self.\_load\_child\_table\_from\_db(fieldname, child\_doctype).
  - If children is identical to no value.
    - Set children from list().
  - Evaluate self.set(fieldname, children).
- Return self.

**Methods declared on this owner** [load child table from db](operations-040.md#op-a96ceee9b9aa79), [set](operations-045.md#op-b58a481a5882b4).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L4558) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L383) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L994)

<a id="op-a96ceee9b9aa79"></a>
### Document.load child table from db

`operation_foundation_model_document_business_behavior_document_load_child_table_from_database`

**Inputs** self, fieldname, child\_doctype.

**Record and data access** execute query text (SELECT).format(table\_name = get\_table\_name(child\_doctype, wrap\_in\_backticks = true), for\_update = for\_update).

**Explicit results** Platform.db.sql(query text (SELECT).format(table\_name = get\_table\_name(child\_doctype, wrap\_in\_backticks = true), for\_update = for\_update), mapping(“parent” → str(self.name), “parenttype” → self.doctype, “p ….

**Local steps**

- Set for\_update from empty text.
- If (self.flags.for\_update and Platform.db.db\_type differs from “sqlite”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.for\_update → Platform.db.db\_type differs from “sqlite”.
  - Set for\_update from “FOR UPDATE”.
- Return Platform.db.sql(query text (SELECT).format(table\_name = get\_table\_name(child\_doctype, wrap\_in\_backticks = true), for\_update = for\_update), mapping(“parent” → str(self.name), “parenttype” → self.doctype, “p ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L4984) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L382) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L993)

<a id="op-4c3e48e6329b61"></a>
### Document.reload

`operation_foundation_model_document_business_behavior_document_reload`

**Inputs** self.

**Declared result** “Self”.

**Explicit results** self.load\_from\_db().

**Local steps**

- Return self.load\_from\_db().

**Methods declared on this owner** [load from db](operations-040.md#op-923c03d02e51cf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L5351) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1003)

<a id="op-cf6cca3d48a149"></a>
### Document.get latest

`operation_foundation_model_document_business_behavior_document_get_latest`

**Inputs** self.

**Explicit results** self.\_doc\_before\_save.

**Local steps**

- If not getattr(self, “\_doc\_before\_save”, no value).
  - Evaluate self.load\_doc\_before\_save().
- Return self.\_doc\_before\_save.

**Methods declared on this owner** [load doc before save](operations-043.md#op-6916982d5f9ee2).

**Values supplied outside this operation** selected callable from getattr(self, “\_doc\_before\_save”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L5407) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L357) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L968)

<a id="op-5394672be646ab"></a>
### Document.check permission

`operation_foundation_model_document_business_behavior_document_check_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, permtype, permlevel.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L5503) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L954)

<a id="op-1db81fefd3c63e"></a>
### Document.has permission

`operation_foundation_model_document_business_behavior_document_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, permtype, debug, user.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L5617) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L369) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L980)

<a id="op-ec41b359fabf18"></a>
### Document.handle permission failure

`operation_foundation_model_document_business_behavior_document_handle_permission_failure`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, perm\_type.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L5780) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L979)

<a id="op-f356379dacb050"></a>
### Document.raise no permission to

`operation_foundation_model_document_business_behavior_document_raise_number_permission_to`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, perm\_type.

**Locally raised failures** PermissionError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L5943) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1002)

<a id="op-cfe802198e4bce"></a>
### Document.insert

`operation_foundation_model_document_business_behavior_document_insert`

**Inputs** self, ignore\_permissions = no value, ignore\_links = no value, ignore\_if\_duplicate = false, ignore\_mandatory = no value, set\_name = no value, set\_child\_names = true.

**Declared result** “Self”.

**Record and data access** read “User” via get\_cached\_value.

**State and service calls** call db\_insert on self · call db\_insert on d.

**Explicit results** self.

**Local steps**

- If self.flags.in\_print.
  - Return self.
- Set self.flags.notifications\_executed from list().
- If ignore\_permissions is distinct from no value.
  - Set self.flags.ignore\_permissions from ignore\_permissions.
- If ignore\_links is distinct from no value.
  - Set self.flags.ignore\_links from ignore\_links.
- If ignore\_mandatory is distinct from no value.
  - Set self.flags.ignore\_mandatory from ignore\_mandatory.
- Evaluate self.set(“\_\_islocal”, true).
- Evaluate self.\_set\_defaults().
- Evaluate self.set\_user\_and\_timestamp().
- Evaluate self.set\_docstatus().
- Evaluate self.check\_permission(“create”).
- Evaluate self.check\_if\_latest().
- Evaluate self.\_validate\_links().
- Evaluate self.run\_method(“before\_insert”).
- Evaluate self.set\_new\_name(set\_name = set\_name, set\_child\_names = set\_child\_names).
- Evaluate self.set\_parent\_in\_children().
- Evaluate self.validate\_higher\_perm\_levels().
- Set self.flags.in\_insert from true.
- Evaluate self.run\_before\_save\_methods().
- Evaluate self.\_validate().
- Evaluate self.set\_docstatus().
- Set self.flags.in\_insert from false.
- If getattr(self.meta, “issingle”, 0).
  - Evaluate self.update\_single(self.get\_valid\_dict()).
- Otherwise.
  - Evaluate self.db\_insert(ignore\_if\_duplicate = ignore\_if\_duplicate).
- If not getattr(self.meta, “is\_virtual”, false).
  - For each d in self.get\_all\_children().
    - Evaluate d.db\_insert().
- Evaluate self.reset\_computed\_child\_tables().
- Evaluate self.run\_method(“after\_insert”).
- Set self.flags.in\_insert from true.
- If self.get(“amended\_from”).
  - Evaluate self.validate\_amended\_from().
  - Evaluate self.copy\_attachments\_from\_amended\_from().
- Evaluate relink\_mismatched\_files(self).
- Evaluate self.run\_post\_save\_methods().
- Set self.flags.in\_insert from false.
- If hasattr(self, “\_\_islocal”).
  - Evaluate delattr(self, “\_\_islocal”).
- If hasattr(self, “\_\_unsaved”).
  - Evaluate delattr(self, “\_\_unsaved”).
- If not (Platform.flags.in\_migrate or Platform.local.flags.in\_install or Platform.flags.in\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.local.flags.in\_install → Platform.flags.in\_setup\_wizard.
  - If Platform.get\_cached\_value(“User”, Platform.session.user, “follow\_created\_documents”).
    - Evaluate \_follow\_document(self.doctype, self.name, Platform.session.user).
- Return self.

**Methods declared on this owner** [set](operations-045.md#op-b58a481a5882b4), [set defaults](operations-042.md#op-260bfc0ce25898), [set user and timestamp](operations-041.md#op-e276da7d33f1d3), [set docstatus](operations-041.md#op-7a66a9775cbc64), [check permission](operations-040.md#op-5394672be646ab), [check if latest](operations-042.md#op-0148e812fab947), [validate links](operations-042.md#op-d0e8ca580d3b7a), [run method](operations-042.md#op-b5adf9fc5af1a0), [set new name](operations-041.md#op-a4b137fe489488), [set parent in children](operations-042.md#op-2839bf040beb76), [validate higher perm levels](operations-042.md#op-d8cda0d8ca39a4), [run before save methods](operations-043.md#op-6237ba21102192), [validate](operations-041.md#op-e142794d43e726), [update single](operations-041.md#op-51e59fec4fa09e), [get valid dict](operations-045.md#op-c47e5bad7a2c34), [db insert](operations-046.md#op-bf3615830b875a), [get all children](operations-042.md#op-c0f0e764f5c4d1), [reset computed child tables](operations-041.md#op-dea25b21fb6ae0), [get](operations-045.md#op-59f5a4cf162623), [validate amended from](operations-040.md#op-3329da2a679fd1), [copy attachments from amended from](operations-041.md#op-d4b9d1aec534bc), [run post save methods](operations-043.md#op-0c820dbc721118).

**Values supplied outside this operation** effective access from self.check\_permission(“create”) · selected callable from self.run\_method(“before\_insert”), getattr(self.meta, “issingle”, 0) and 2 further calls · configured or stored value from Platform.get\_cached\_value(“User”, Platform.session.user, “follow\_created\_documents”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0276.json#L6244) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L378) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L989)

<a id="op-39a20656da1053"></a>
### Document.check if locked

`operation_foundation_model_document_business_behavior_document_check_if_locked`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.DocumentLockedError — translated “This document is currently locked and queued for execution. Please try again after some time.”.

**Local steps**

- If (not self.creation or not self.is\_locked).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.creation → not self.is\_locked.
  - Return no value.
- Set primary\_action from no value.
- If file\_lock.lock\_age(self.get\_signature()) &gt; DOCUMENT\_LOCK\_SOFT\_EXPIRY.
  - Set primary\_action from mapping(“label” → “Force Unlock”, “server\_action” → “Platform.model.document.unlock\_document”, “hide\_on\_success” → true, “args” → mapping(“doctype” → self.doctype, “name” → self.name)).
- Call the validation error handler Platform.throw(translated “This document is currently locked and queued for execution. Please try again after some time.”, title = translated “Document Queued”, primary\_action = primary\_action, exc = Platf ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get signature](operations-044.md#op-8c487683e98ecb).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L952)

<a id="op-5d89aac355c0bc"></a>
### Document.save

`operation_foundation_model_document_business_behavior_document_save`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Declared result** “Self”.

**Explicit results** self.\_save(expanded args, expanded names kwargs).

**Local steps**

- Return self.\_save(expanded args, expanded names kwargs).

**Methods declared on this owner** [save](operations-040.md#op-ea01a6cfb29b61).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L384) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1020)

<a id="op-ea01a6cfb29b61"></a>
### Document.save

`operation_foundation_model_document_business_behavior_document_save_2`

**Inputs** self, ignore\_permissions = no value, ignore\_version = no value.

**Declared result** “Self”.

**State and service calls** call insert on self · call db\_update on self.

**Explicit results** self · self.insert().

**Local steps**

- If self.flags.in\_print.
  - Return self.
- Set self.flags.notifications\_executed from list().
- If ignore\_permissions is distinct from no value.
  - Set self.flags.ignore\_permissions from ignore\_permissions.
- Set self.flags.ignore\_version from Platform.in\_test when ignore\_version is identical to no value, otherwise ignore\_version.
  - Value choice on ignore\_version is identical to no value — true gives Platform.in\_test, false gives ignore\_version.
- If (self.get(“\_\_islocal”) or not self.get(“name”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“\_\_islocal”) → not self.get(“name”).
  - Return self.insert().
- Evaluate self.check\_if\_locked().
- Evaluate self.\_set\_defaults().
- Evaluate self.\_restore\_masked\_fields\_from\_db().
- Evaluate self.check\_permission(“write”, “save”).
- Evaluate self.set\_user\_and\_timestamp().
- Evaluate self.set\_docstatus().
- Evaluate self.check\_if\_latest().
- Evaluate self.set\_parent\_in\_children().
- Evaluate self.set\_name\_in\_children().
- Evaluate self.validate\_higher\_perm\_levels().
- Evaluate self.\_validate\_links().
- Evaluate self.run\_before\_save\_methods().
- If self.\_action differs from “cancel”.
  - Evaluate self.\_validate().
- If self.\_action equals “update\_after\_submit”.
  - Evaluate self.validate\_update\_after\_submit().
- Evaluate self.set\_docstatus().
- If self.meta.issingle.
  - Evaluate self.update\_single(self.get\_valid\_dict()).
- Otherwise.
  - Evaluate self.db\_update().
- Evaluate self.update\_children().
- Evaluate self.reset\_computed\_child\_tables().
- Evaluate self.run\_post\_save\_methods().
- If hasattr(self, “\_\_unsaved”).
  - Evaluate delattr(self, “\_\_unsaved”).
- Return self.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623), [insert](operations-040.md#op-cfe802198e4bce), [check if locked](operations-040.md#op-39a20656da1053), [set defaults](operations-042.md#op-260bfc0ce25898), [restore masked fields from db](operations-042.md#op-7eac18ffc32aae), [check permission](operations-040.md#op-5394672be646ab), [set user and timestamp](operations-041.md#op-e276da7d33f1d3), [set docstatus](operations-041.md#op-7a66a9775cbc64), [check if latest](operations-042.md#op-0148e812fab947), [set parent in children](operations-042.md#op-2839bf040beb76), [set name in children](operations-042.md#op-d257082ba8108f), [validate higher perm levels](operations-042.md#op-d8cda0d8ca39a4), [validate links](operations-042.md#op-d0e8ca580d3b7a), [run before save methods](operations-043.md#op-6237ba21102192), [validate](operations-041.md#op-e142794d43e726), [validate update after submit](operations-042.md#op-e23f7bbd8476c3), [update single](operations-041.md#op-51e59fec4fa09e), [get valid dict](operations-045.md#op-c47e5bad7a2c34), [db update](operations-046.md#op-fa126f30709bdc), [update children](operations-041.md#op-e1b06d0b7564c6), [reset computed child tables](operations-041.md#op-dea25b21fb6ae0), [run post save methods](operations-043.md#op-0c820dbc721118).

**Values supplied outside this operation** effective access from self.check\_permission(“write”, “save”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L467) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1021)

<a id="op-3329da2a679fd1"></a>
### Document.validate amended from

`operation_foundation_model_document_business_behavior_document_validate_amended_from`

**Inputs** self.

**Record and data access** read self.doctype via get\_value.

**Explicit failure paths** validation helper — message.

**Local steps**

- If Platform.db.get\_value(self.doctype, self.get(“amended\_from”), “docstatus”) differs from 2.
  - Set message from translated “{0} cannot be amended because it is not cancelled. Please cancel the document before creating an amendment.”.format(Platform.utils.get\_link\_to\_form(self.doctype, self.get(“amended\_from”))).
  - Call the validation error handler Platform.throw(message, title = translated “Amendment Not Allowed”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get](operations-045.md#op-59f5a4cf162623).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0277.json#L1298) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1040)
