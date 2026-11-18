# Record lifecycle and persistence · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Database

<a id="op-bd7b8b43be038a"></a>
### Database.sql ddl

`operation_foundation_database_business_behavior_database_database_query_data_definition_language`

**Inputs** self, query, debug = false.

**Local steps**

- Set transaction\_control from self.\_disable\_transaction\_control.
- Set self.\_disable\_transaction\_control from 0.
- Evaluate self.commit().
- Evaluate self.sql(query, debug = debug).
- Set self.\_disable\_transaction\_control from transaction\_control.

If control reaches the end, it returns no value.

**Methods declared on this owner** [commit](operations-019.md#op-618c1b0592a4e5), [sql](operations-017.md#op-eb3702e2fa04e7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L6977) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1049)

<a id="op-8bae13939a865b"></a>
### Database.check transaction status

`operation_foundation_database_business_behavior_database_check_transaction_status`

**Inputs** self, query, query\_type = no value.

**Explicit results** no value.

**Explicit failure paths** Platform.TooManyWritesError(msg).

**Local steps**

- If not query\_type.
  - Set query\_type from get\_query\_type(query).
- Evaluate self.check\_implicit\_commit(query, query\_type).
- If query\_type belongs to COMMIT\_OR\_ROLLBACK.
  - Set self.transaction\_writes from 0.
  - Return no value.
- If query\_type belongs to WRITE\_QUERY\_TYPES.
  - Update self.transaction\_writes using + 1.
  - If Platform.conf.get(“max\_writes\_per\_transaction”).
    - Set self.MAX\_WRITES\_PER\_TRANSACTION from cint(Platform.conf.max\_writes\_per\_transaction).
  - If self.transaction\_writes &gt; self.MAX\_WRITES\_PER\_TRANSACTION.
    - If self.auto\_commit\_on\_many\_writes.
      - Evaluate self.commit().
    - Otherwise.
      - Set msg from ((text in the contract + translated “Too many changes to database in single action.”) + text in the contract).
      - Update msg using + (translated “The changes have been reverted.” + text in the contract).
      - Raise Platform.TooManyWritesError(msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check implicit commit](operations-018.md#op-737c82058dcec1), [commit](operations-019.md#op-618c1b0592a4e5).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L7133) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1039)

<a id="op-737c82058dcec1"></a>
### Database.check implicit commit

`operation_foundation_database_business_behavior_database_check_implicit_commit`

**Inputs** self, query, query\_type.

**Explicit failure paths** ImplicitCommitError(“This statement can cause implicit commit”, query).

**Local steps**

- If (query\_type belongs to IMPLICIT\_COMMIT\_QUERY\_TYPES and self.transaction\_writes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in query\_type belongs to IMPLICIT\_COMMIT\_QUERY\_TYPES → self.transaction\_writes.
  - Raise ImplicitCommitError(“This statement can cause implicit commit”, query).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0128.json#L7591) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1038)

<a id="op-0bad9587030196"></a>
### Database.fetch as dict

`operation_foundation_database_business_behavior_database_fetch_as_mapping`

**Inputs** self, result.

**Declared result** list at \_dict.

**Explicit results** list() · list of \_dict(zip(keys, row, strict = false)) for row drawn from result.

**Local steps**

- If not result.
  - Return list().
- Set keys from list of column at 0 for column drawn from self.\_cursor.description.
  - Draw column from self.\_cursor.description.
- Return list of \_dict(zip(keys, row, strict = false)) for row drawn from result.
  - Draw row from result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L915) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1058)

<a id="op-32431aabdc7c0a"></a>
### Database.clear db table cache

`operation_foundation_database_business_behavior_database_clear_database_table_cache`

**Inputs** query\_type.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- If query\_type belongs to CREATE\_OR\_DROP.
  - Evaluate Platform.client\_cache.delete\_value(“db\_tables”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L186) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L897) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1041)

<a id="op-660bc5b930a31f"></a>
### Database.get description

`operation_foundation_database_business_behavior_database_get_description`

**Inputs** self.

**Explicit results** self.\_cursor.description.

**Local steps**

- Return self.\_cursor.description.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L281) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L928) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1071)

<a id="op-a9e772c08b0f89"></a>
### Database.convert to lists

`operation_foundation_database_business_behavior_database_convert_to_lists`

**Inputs** res.

**Wrappers, in declaration order** staticmethod.

**Explicit results** list of list of value for value drawn from row for row drawn from res.

**Local steps**

- Return list of list of value for value drawn from row for row drawn from res.
  - Draw row from res.
  - Draw value from row.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L326) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1045)

<a id="op-253c8a1dec383e"></a>
### Database.get

`operation_foundation_database_business_behavior_database_get`

**Inputs** self, doctype, filters = no value, as\_dict = true, cache = false.

**Explicit results** self.get\_value(doctype, filters, “\*”, as\_dict = as\_dict, cache = cache).

**Local steps**

- Return self.get\_value(doctype, filters, “\*”, as\_dict = as\_dict, cache = cache).

**Methods declared on this owner** [get value](operations-018.md#op-5d85ba3f12ad2b).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L404) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L919) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1062)

<a id="op-5d85ba3f12ad2b"></a>
### Database.get value

`operation_foundation_database_business_behavior_database_get_value`

**Inputs** self, doctype, filters = no value, fieldname = “name”, ignore = false, as\_dict = false, debug = false, order\_by = DefaultOrderBy, cache = false, for\_update = false, run (named only, default true), pluck (named only, default false), distinct (named only, default false), skip\_locked (named only, default false), wait (named only, default true).

**Explicit results** result · no value · row · row at 0.

**Local steps**

- Set result from self.get\_values(doctype, filters, fieldname, ignore, cache = cache, for\_update = for\_update, run = run, pluck = pluck, …).
- If not run.
  - Return result.
- If not result.
  - Return no value.
- Set row from result at 0.
- If (as\_dict or len(row) &gt; 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in as\_dict → len(row) &gt; 1.
  - Return row.
- Return row at 0.

**Methods declared on this owner** [get values](operations-018.md#op-a39bd0dd6ea867).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L528) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1086)

<a id="op-a39bd0dd6ea867"></a>
### Database.get values

`operation_foundation_database_business_behavior_database_get_values`

**Inputs** self, doctype, filters = no value, fieldname = “name”, ignore = false, as\_dict = false, debug = false, order\_by = DefaultOrderBy, update = no value, cache = false, for\_update = false, run (named only, default true), pluck (named only, default false), distinct (named only, default false), limit (named only, default no value), skip\_locked (named only, default false), wait (named only, default true).

**Explicit results** self.value\_cache at doctype at filters at fieldname · no value · out.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies is\_single\_doctype.
- Set out from no value.
- If isinstance(fieldname, list).
  - Set fieldname from tuple(fieldname).
- If (cache and isinstance(filters, str) and fieldname belongs to self.value\_cache at doctype at filters).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cache → isinstance(filters, str) → fieldname belongs to self.value\_cache at doctype at filters.
  - Return self.value\_cache at doctype at filters at fieldname.
- If distinct.
  - Set order\_by from no value.
- If isinstance(filters, list).
  - If filters bound to list(generator of f for f drawn from filters where f is distinct from no value).
    - Draw f from filters, keep a combination only if (f is distinct from no value).
    - Set out from Platform.qb.get\_query(table = doctype, fields = fieldname, filters = filters, order\_by = order\_by, …).run(debug = debug, run = run, as\_dict = as\_dict, pluck = pluck).
  - Otherwise.
    - Set out from mapping().
- Otherwise.
  - If (filters is distinct from no value and (filters differs from doctype or doctype equals “DocType”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters is distinct from no value → (filters differs from doctype or doctype equals “DocType”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters differs from doctype → doctype equals “DocType”.
    - Attempt the following.
      - If order\_by.
        - Set order\_by from “creation” when order\_by equals DefaultOrderBy, otherwise order\_by.
          - Value choice on order\_by equals DefaultOrderBy — true gives “creation”, false gives order\_by.
      - Set query from Platform.qb.get\_query(table = doctype, filters = filters, order\_by = order\_by, for\_update = for\_update, …).
      - If (isinstance(fieldname, str) and fieldname equals “\*”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fieldname, str) → fieldname equals “\*”.
        - Set as\_dict from true.
      - Set out from query.run(as\_dict = as\_dict, debug = debug, update = update, run = run, …).
    - On failure (Exception) bound to e.
      - If (ignore and (Platform.db.is\_missing\_column(e) or Platform.db.is\_table\_missing(e) or str(e).startswith(“Invalid DocType”))).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in ignore → (Platform.db.is\_missing\_column(e) or Platform.db.is\_table\_missing(e) or str(e).startswith(“Invalid DocType”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.is\_missing\_column(e) → Platform.db.is\_table\_missing(e) → str(e).startswith(“Invalid DocType”).
        - Set out from no value.
      - Otherwise.
        - Propagate the active failure.
  - Otherwise.
    - If is\_single\_doctype(doctype).
      - Set fields from list(fieldname) when (isinstance(fieldname, str) and fieldname differs from “\*”), otherwise fieldname.
        - Value choice on (isinstance(fieldname, str) and fieldname differs from “\*”) — true gives list(fieldname), false gives fieldname.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(fieldname, str) → fieldname differs from “\*”.
      - Set out from self.get\_values\_from\_single(fields, filters, doctype, as\_dict, run = run, pluck = pluck, distinct = distinct, …).
    - Otherwise.
      - Return no value.
- If (cache and isinstance(filters, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cache → isinstance(filters, str).
  - Set self.value\_cache at doctype at filters at fieldname from out.
- Return out.

**Methods declared on this owner** [get values from single](operations-018.md#op-b7712ab637c275).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L1069) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1087)

<a id="op-b7712ab637c275"></a>
### Database.get values from single

`operation_foundation_database_business_behavior_database_get_values_from_single`

**Inputs** self, fields, filters, doctype, as\_dict = false, debug = false, update = no value, run (named only, default true), pluck (named only, default false), distinct (named only, default false).

**Explicit results** list() · list(values) when values, otherwise list() · list(list(map(values.get, fields))) · r · list(list of r.get(field) for field drawn from fields) · 1 additional forms in the steps below.

**Local steps**

- Bind dependencies get\_default\_df.
- Set meta from Platform.get\_meta(doctype).
- Bind local operation \_cast for subsequent calls.
- If (fields equals “\*” or isinstance(filters, dict)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fields equals “\*” → isinstance(filters, dict).
  - Set values from self.get\_singles\_dict(doctype, cast = true).
  - If isinstance(filters, dict).
    - For each tuple(key, value) in filters.items().
      - If values.get(key) differs from value.
        - Return list().
  - If as\_dict.
    - Return list(values) when values, otherwise list().
      - Value choice on values — true gives list(values), false gives list().
  - If isinstance(fields, list).
    - Return list(list(map(values.get, fields))).
- Otherwise.
  - Set r from Platform.qb.get\_query(“Singles”, filters = mapping(“field” → tuple(“in”, tuple(fields)), “doctype” → doctype), fields = list(“field”, “value”), distinct = distinct).run(pluck = pluck, debug = debug, as\_dict = false).
  - If not run.
    - Return r.
  - If not r.
    - Return list().
  - Set r from \_dict(r).
  - For each tuple(k, v) in r.items().
    - Set r at k from \_cast(k, v).
  - If update.
    - Evaluate r.update(update).
  - If not as\_dict.
    - Return list(list of r.get(field) for field drawn from fields).
      - Draw field from fields.
  - Return list(r).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get singles dict](operations-018.md#op-695e794d20081a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L2602) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1088)

<a id="op-099093be53ab73"></a>
### Database.get values from single.cast

`operation_foundation_database_business_behavior_database_get_values_from_single_cast`

**Inputs** field, val.

**Explicit results** val · cast\_fieldtype(df.fieldtype, val).

**Local steps**

- Set df from (meta.get\_field(field) or get\_default\_df(field)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.get\_field(field) → get\_default\_df(field).
- If not df.
  - Return val.
- Return cast\_fieldtype(df.fieldtype, val).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L3600) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1089)

<a id="op-695e794d20081a"></a>
### Database.get singles dict

`operation_foundation_database_business_behavior_database_get_singles_mapping`

**Inputs** self, doctype, debug = false, for\_update (named only, default false), cast (named only, default false).

**Explicit results** \_dict(queried\_result) · return\_value.

**Local steps**

- Set queried\_result from Platform.qb.get\_query(“Singles”, filters = mapping(“doctype” → doctype), fields = list(“field”, “value”), for\_update = for\_update).run(debug = debug).
- If not cast.
  - Return \_dict(queried\_result).
- Attempt the following.
  - Set meta from Platform.get\_meta(doctype).
- On failure (DoesNotExistError).
  - Return \_dict(queried\_result).
- Set return\_value from \_dict().
- For each tuple(fieldname, value) in queried\_result.
  - If df bound to meta.get\_field(fieldname).
    - Set casted\_value from cast\_fieldtype(df.fieldtype, value).
  - Otherwise.
    - Set casted\_value from value.
  - Set return\_value at fieldname from casted\_value.
- Return return\_value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L3740) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1080)

<a id="op-0899a51e063d58"></a>
### Database.get all

`operation_foundation_database_business_behavior_database_get_all`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read expanded args via get\_all.

**Explicit results** Platform.get\_all(expanded args, expanded names kwargs).

**Local steps**

- Return Platform.get\_all(expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L4182) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L920) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1063)

<a id="op-dfaafa7807c0c1"></a>
### Database.get list

`operation_foundation_database_business_behavior_database_get_list`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read expanded args via get\_list.

**Explicit results** Platform.get\_list(expanded args, expanded names kwargs).

**Local steps**

- Return Platform.get\_list(expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L4256) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L932) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1075)

<a id="op-f0c41b4667a379"></a>
### Database.get update dict

`operation_foundation_database_business_behavior_database_get_update_mapping`

**Inputs** fieldname, value, modified (named only), modified\_by (named only), update\_modified (named only).

**Wrappers, in declaration order** staticmethod.

**Declared result** dict at tuple(str, Any).

**Explicit results** update\_dict.

**Local steps**

- Set update\_dict from fieldname when isinstance(fieldname, dict), otherwise mapping(fieldname → value).
  - Value choice on isinstance(fieldname, dict) — true gives fieldname, false gives mapping(fieldname → value).
- If update\_modified.
  - Set modified from (modified or now()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in modified → now().
  - Set modified\_by from (modified\_by or Platform.session.user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in modified\_by → Platform.session.user.
  - Evaluate update\_dict.update(mapping(“modified” → modified, “modified\_by” → modified\_by)).
- Return update\_dict.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L79) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1085)

<a id="op-aa1f344b0e80a2"></a>
### Database.set single value

`operation_foundation_database_business_behavior_database_set_single_value`

**Inputs** self, doctype, fieldname, value = no value, modified (named only, default no value), modified\_by (named only, default no value), update\_modified (named only, default true), debug (named only, default false).

**State and service calls** request delete on “Singles” · call insert on Platform.qb.into(“Singles”).columns(“doctype”, “field”, “value”).

**Local steps**

- Set to\_update from self.\_get\_update\_dict(fieldname, value, modified = modified, modified\_by = modified\_by, update\_modified = update\_modified).
- Evaluate Platform.db.delete(“Singles”, filters = mapping(“field” → tuple(“in”, tuple(to\_update)), “doctype” → doctype), debug = debug).
- Set singles\_data from generator of tuple(doctype, key, sbool(value)) for tuple(key, value) drawn from to\_update.items().
  - Draw tuple(key, value) from to\_update.items().
- Evaluate nested operand in the contract(nested operand in the contract).columns(“doctype”, “field”, “value”).insert(expanded singles\_data).run(debug = debug).
- Evaluate Platform.clear\_document\_cache(doctype, doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get update dict](operations-018.md#op-f0c41b4667a379).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L4647) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1110)

<a id="op-c2705a40229f66"></a>
### Database.get single value

`operation_foundation_database_business_behavior_database_get_single_value`

**Inputs** self, doctype, fieldname, cache = true, debug (named only, default false), for\_update (named only, default false), run (named only, default true).

**Explicit results** self.value\_cache at doctype at fieldname · val.

**Explicit failure paths** validation helper — translated “Field {0} does not exist on {1}”.format(Platform.bold(fieldname), Platform.bold(doctype), self.InvalidColumnName).

**Local steps**

- Bind dependencies get\_default\_df.
- If (cache and not for\_update and run and fieldname belongs to self.value\_cache at doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cache → not for\_update → run → fieldname belongs to self.value\_cache at doctype.
  - Return self.value\_cache at doctype at fieldname.
- Set val from Platform.qb.get\_query(table = “Singles”, filters = mapping(“doctype” → doctype, “field” → fieldname), fields = “value”, for\_update = for\_update).run(debug = debug, run = run).
- If not run.
  - Return val.
- Set val from val at 0 at 0 when val, otherwise no value.
  - Value choice on val — true gives val at 0 at 0, false gives no value.
- Set df from (Platform.get\_meta(doctype).get\_field(fieldname) or get\_default\_df(fieldname)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_meta(doctype).get\_field(fieldname) → get\_default\_df(fieldname).
- If not df.
  - Call the validation error handler Platform.throw(translated “Field {0} does not exist on {1}”.format(Platform.bold(fieldname), Platform.bold(doctype), self.InvalidColumnName)).
- Set val from cast\_fieldtype(df.fieldtype, val).
- If (cache and not for\_update and run).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cache → not for\_update → run.
  - Set self.value\_cache at doctype at fieldname from val.
- Return val.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L5165) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1079)

<a id="op-6e81e55e536e7d"></a>
### Database.get singles value

`operation_foundation_database_business_behavior_database_get_singles_value`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Explicit results** self.get\_single\_value(expanded args, expanded names kwargs).

**Local steps**

- Return self.get\_single\_value(expanded args, expanded names kwargs).

**Methods declared on this owner** [get single value](operations-018.md#op-c2705a40229f66).

**Values supplied outside this operation** configured or stored value from self.get\_single\_value(expanded args, expanded names kwargs).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L5829) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L938) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1081)

<a id="op-e1be696554aa8e"></a>
### Database.set value

`operation_foundation_database_business_behavior_database_set_value`

**Inputs** self, dt, dn, field, val = no value, modified = no value, modified\_by = no value, update\_modified = true, debug = false.

**Explicit results** no value.

**Local steps**

- Bind dependencies is\_single\_doctype.
- If (dn is identical to no value or dt equals dn).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dn is identical to no value → dt equals dn.
  - If not is\_single\_doctype(dt).
    - Return no value.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
  - Evaluate self.set\_single\_value(doctype = dt, fieldname = field, value = val, debug = debug, …).
  - Return no value.
- Set to\_update from self.\_get\_update\_dict(field, val, modified = modified, modified\_by = modified\_by, update\_modified = update\_modified).
- Set query from Platform.qb.get\_query(table = dt, filters = dn, update = true).
- If isinstance(dn, FilterValue).
  - Evaluate Platform.clear\_document\_cache(dt, convert\_to\_value(dn)).
- Otherwise.
  - Evaluate Platform.clear\_document\_cache(dt).
- For each tuple(column, value) in to\_update.items().
  - Set query from query.set(column, value).
- Evaluate query.run(debug = debug).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set single value](operations-018.md#op-aa1f344b0e80a2), [get update dict](operations-018.md#op-f0c41b4667a379).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L5907) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1111)

<a id="op-09cb2a34925baf"></a>
### Database.bulk update

`operation_foundation_database_business_behavior_database_bulk_update`

**Inputs** self, doctype, doc\_updates, chunk\_size (named only, default 100), modified (named only, default no value), modified\_by (named only, default no value), update\_modified (named only, default true), debug (named only, default false).

**Explicit results** no value.

**Local steps**

- If not doc\_updates.
  - Return no value.
- Set modified\_dict from no value.
- If update\_modified.
  - Set modified\_dict from self.\_get\_update\_dict(mapping(), no value, modified = modified, modified\_by = modified\_by, update\_modified = update\_modified).
- Set total\_docs from len(doc\_updates).
- Set iterator from iter(doc\_updates.items()).
- For each \_\_ in range(0, total\_docs, chunk\_size).
  - Set doc\_chunk from dict(itertools.islice(iterator, chunk\_size)).
  - Evaluate self.\_build\_and\_run\_bulk\_update\_query(doctype, doc\_chunk, modified\_dict, debug).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get update dict](operations-018.md#op-f0c41b4667a379), [build and run bulk update query](operations-018.md#op-51aa9789b12041).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L6564) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1037)

<a id="op-51aa9789b12041"></a>
### Database.build and run bulk update query

`operation_foundation_database_business_behavior_database_build_and_run_bulk_update_query`

**Inputs** doctype, doc\_updates, modified\_dict = no value, debug = false.

**Wrappers, in declaration order** staticmethod.

**Explicit results** no value.

**Local steps**

- If not doc\_updates.
  - Return no value.
- Set dt from Platform.qb.DocType(doctype).
- Set update\_query from Platform.qb.update(dt).
- Set conditions from mapping().
- Set docnames from list(doc\_updates.keys()).
- For each tuple(docname, row) in doc\_updates.items().
  - For each tuple(field, value) in row.items().
    - If field does not belong to conditions.
      - Set conditions at field from Case().
    - Evaluate conditions at field.when(dt.name equals docname, value).
- For each field in conditions.
  - Set update\_query from update\_query.set(dt at field, conditions at field.else\_(dt at field)).
- If modified\_dict.
  - For each tuple(column, value) in modified\_dict.items().
    - Set update\_query from update\_query.set(dt at column, value).
- Evaluate update\_query.where(dt.name.isin(docnames)).run(debug = debug).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L74) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1035)

<a id="op-405c13ec6a3309"></a>
### Database.set global

`operation_foundation_database_business_behavior_database_set_global`

**Inputs** self, key, val, user = “\_\_global”.

**Local steps**

- Evaluate self.set\_default(key, val, user).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set default](operations-019.md#op-dc820da7a7a9aa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L7603) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1108)

<a id="op-632a99564c1a53"></a>
### Database.get global

`operation_foundation_database_business_behavior_database_get_global`

**Inputs** self, key, user = “\_\_global”.

**Explicit results** self.get\_default(key, user).

**Local steps**

- Return self.get\_default(key, user).

**Methods declared on this owner** [get default](operations-019.md#op-d9bba948775069).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0129.json#L7692) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L929) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1072)
