# Record lifecycle and persistence · operations 29

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Db manager

<a id="op-64fb813b56789e"></a>
### Db Manager.delete user

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_delete_user`

**Inputs** self, target, host = no value.

**Local steps**

- Set host from (host or self.get\_current\_host()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in host → self.get\_current\_host().
- Evaluate self.db.sql(formatted text DROP USER IF EXISTS '{target}'@'{host}').

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current host](operations-028.md#op-cfd5870423adb0).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L7467) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1022) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1163)

<a id="op-7d749552aee7a7"></a>
### Db Manager.create database

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_create_database`

**Inputs** self, target.

**Local steps**

- If target belongs to self.get\_database\_list().
  - Evaluate self.drop\_database(target).
- Evaluate self.db.sql(formatted text CREATE DATABASE ′{target}′ CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get database list](operations-029.md#op-5cb5e6ce16cab3), [drop database](operations-029.md#op-035a8f4940a02e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0130.json#L7614) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1020) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1161)

<a id="op-035a8f4940a02e"></a>
### Db Manager.drop database

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_drop_database`

**Inputs** self, target.

**Local steps**

- Evaluate self.db.sql\_ddl(formatted text DROP DATABASE IF EXISTS ′{target}′).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1023) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1164)

<a id="op-5dc583b5aee551"></a>
### Db Manager.grant all privileges

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_grant_all_privileges`

**Inputs** self, target, user, host = no value.

**Local steps**

- Set host from (host or self.get\_current\_host()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in host → self.get\_current\_host().
- Set permissions from “SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW, EVENT, TRI …” when Platform.conf.rds\_db, otherwise “ALL PRIVILEGES”.
  - Value choice on Platform.conf.rds\_db — true gives “SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES, CREATE VIEW, EVENT, TRI …”, false gives “ALL PRIVILEGES”.
- Evaluate self.db.sql(formatted text GRANT {permissions} ON ′{target}′.\* TO '{user}'@'{host}').

If control reaches the end, it returns no value.

**Methods declared on this owner** [get current host](operations-028.md#op-cfd5870423adb0).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L91) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1027) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1168)

<a id="op-756e26f2bfcc59"></a>
### Db Manager.flush privileges

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_flush_privileges`

**Inputs** self.

**Local steps**

- Evaluate self.db.sql(“FLUSH PRIVILEGES”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L307) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1024) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1165)

<a id="op-5cb5e6ce16cab3"></a>
### Db Manager.get database list

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_get_database_list`

**Inputs** self.

**Explicit results** self.db.sql(“SHOW DATABASES”, pluck = true).

**Local steps**

- Return self.db.sql(“SHOW DATABASES”, pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0131.json#L365) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1026) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1167)

<a id="op-056234d35c17b6"></a>
### Db Manager.restore database

`operation_foundation_database_persistent_records_manager_business_behavior_database_manager_restore_database`

**Inputs** verbose, target, source, user, password.

**Wrappers, in declaration order** staticmethod.

**Declared result** no value.

**Explicit results** Platform.throw(translated “{} not found in PATH! This is required to restore the database.”.format(bin\_name), exc = Platform.ExecutableNotFound).

**Explicit failure paths** Exception(“′gzip′ not installed”) · validation helper with Platform.ExecutableNotFound — translated “{} not found in PATH! This is required to restore the database.”.format(bin\_name).

**Local steps**

- Bind dependencies shlex.
- Bind dependencies which.
- Bind dependencies get\_command.
- Bind dependencies execute\_in\_shell.
- Set command from list(“set -o pipefail;”).
- If source.endswith(“.gz”).
  - If gzip bound to which(“gzip”).
    - Evaluate command.extend(list(gzip, “-cd”, source, “\|”)).
  - Otherwise.
    - Raise Exception(“′gzip′ not installed”).
- Otherwise.
  - Evaluate command.extend(list(“cat”, source, “\|”)).
- If Platform.conf.db\_type equals “mariadb”.
  - Evaluate command.extend(list(“sed”, “'/\\/\\\*M\\{0,1\\}!999999\\\\- enable the sandbox mode \\\*\\//d'”, “\|”)).
  - Evaluate command.extend(list(“sed”, “'/\\/\\\*!&#91;0-9&#93;\* DEFINER=&#91;^ &#93;\* SQL SECURITY DEFINER \\\*\\//d'”, “\|”)).
- Set tuple(bin, args, bin\_name) from get\_command(socket = Platform.conf.db\_socket, host = Platform.conf.db\_host, port = Platform.conf.db\_port, user = user, …).
- If not bin.
  - Return Platform.throw(translated “{} not found in PATH! This is required to restore the database.”.format(bin\_name), exc = Platform.ExecutableNotFound).
- Evaluate command.append(bin).
- Evaluate command.append(shlex.join(args)).
- Evaluate execute\_in\_shell(one space.join(command), check\_exit\_code = true, verbose = verbose).
- Evaluate Platform.cache.delete\_keys(empty text).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L94) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1029) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L1170)

## Service · Db query

<a id="op-ebd67acfa323ed"></a>
### Parse sql

`operation_foundation_model_persistent_records_query_business_behavior_parse_database_query`

**Inputs** field.

**Wrappers, in declaration order** lru\_cache(maxsize = 128).

**Declared result** (Statement bitwise or no value).

**Explicit results** parsed at 0.

**Local steps**

- If parsed bound to sqlparse.parse(field).
  - Return parsed at 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L1685) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1257)

<a id="op-058a82d6a4a0ec"></a>
### Database Query.initialize

`operation_foundation_model_persistent_records_query_business_behavior_database_query_initialize`

**Inputs** self, doctype, user = no value.

**Local steps**

- Set self.doctype from doctype.
- Set self.tables from list().
- Set self.link\_tables from list().
- Set self.linked\_table\_aliases from mapping().
- Set self.linked\_table\_counter from Counter().
- Set self.conditions from list().
- Set self.or\_conditions from list().
- Set self.fields from no value.
- Set self.user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set self.ignore\_ifnull from false.
- Set self.flags from Platform.\_dict().
- Set self.reference\_doctype from no value.
- Set self.permission\_map from mapping().
- Set self.shared from list().
- Set self.\_fetch\_shared\_documents from false.
- Set self.\_metas from mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L132) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1228)

<a id="op-12778356591bd2"></a>
### Database Query.doctype meta

`operation_foundation_model_persistent_records_query_business_behavior_database_query_record_type_meta`

**Inputs** self.

**Wrappers, in declaration order** cached\_property.

**Explicit results** self.get\_meta(self.doctype).

**Local steps**

- Return self.get\_meta(self.doctype).

**Methods declared on this owner** [get meta](operations-029.md#op-79800d6d423b9a).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L2237) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1235)

<a id="op-79800d6d423b9a"></a>
### Database Query.get meta

`operation_foundation_model_persistent_records_query_business_behavior_database_query_get_meta`

**Inputs** self, doctype.

**Explicit results** self.\_metas at doctype.

**Local steps**

- If doctype does not belong to self.\_metas.
  - Set self.\_metas at doctype from Platform.get\_meta(doctype).
- Return self.\_metas at doctype.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L2302) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L633) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1224)

<a id="op-b891bf63416c12"></a>
### Database Query.query tables

`operation_foundation_model_persistent_records_query_business_behavior_database_query_query_tables`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (self.tables + list of d.table\_alias for d drawn from self.link\_tables).

**Local steps**

- Return (self.tables + list of d.table\_alias for d drawn from self.link\_tables).
  - Draw d from self.link\_tables.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0269.json#L2429) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1234)

<a id="op-d6c81390d1af58"></a>
### Database Query.execute

`operation_foundation_model_persistent_records_query_business_behavior_database_query_execute`

**Inputs** self, fields = no value, filters = no value, or\_filters = no value, docstatus = no value, group\_by = no value, order\_by = DefaultOrderBy, limit\_start = false, limit\_page\_length = no value, as\_list = false, with\_childnames = false, debug = false, ignore\_permissions = false, user = no value, with\_comment\_count = false, join = “left join”, distinct = false, start = no value, page\_length = no value, limit = no value, ignore\_ifnull = false, save\_user\_settings = false, save\_user\_settings\_fields = false, update = no value, user\_settings = no value, reference\_doctype = no value, run = true, strict = true, pluck = no value, ignore\_ddl = false, parent\_doctype (named only, default no value).

**Declared result** list.

**Explicit results** list() · Platform.call(controller.get\_list, args = kwargs, expanded names kwargs) · list of d at pluck for d drawn from result · result.

**Explicit failure paths** validation helper — translated “Fields must be a list or tuple when as\_list is enabled”.

**Local steps**

- Set self.user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- If not ignore\_permissions.
  - Evaluate self.check\_read\_permission(self.doctype, parent\_doctype = parent\_doctype).
- If (isinstance(fields, dict) or (fields and isinstance(fields, list) and isinstance(fields at 0, list))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in isinstance(fields, dict) → (fields and isinstance(fields, list) and isinstance(fields at 0, list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → isinstance(fields, list) → isinstance(fields at 0, list).
  - Set tuple(filters, fields) from tuple(fields, filters).
- Otherwise.
  - If (fields and isinstance(filters, list) and len(filters) &gt; 1 and isinstance(filters at 0, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fields → isinstance(filters, list) → len(filters) &gt; 1 → isinstance(filters at 0, str).
    - Set tuple(filters, fields) from tuple(fields, filters).
- If fields.
  - Set self.fields from fields.
- Otherwise.
  - Set self.fields from list(formatted text ′tab{self.doctype}′.′{(pluck or “name”)}′).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pluck → “name”.
- If start.
  - Set limit\_start from start.
- If page\_length.
  - Set limit\_page\_length from page\_length.
- If limit.
  - Set limit\_page\_length from limit.
- If (as\_list and not isinstance(self.fields, (Sequence bitwise or str)) and len(self.fields) &gt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in as\_list → not isinstance(self.fields, (Sequence bitwise or str)) → len(self.fields) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Fields must be a list or tuple when as\_list is enabled”).
- For each tuple(k, \_filters) in mapping(“filters” → (filters or Filters()), “or\_filters” → (or\_filters or Filters())).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → Filters().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in or\_filters → Filters().
  - If isinstance(\_filters, str).
    - Set \_filters from json.loads(\_filters).
  - If not isinstance(\_filters, Filters).
    - Set \_filters from Filters(\_filters, doctype = self.doctype).
  - Evaluate setattr(self, k, \_filters).
- Set self.docstatus from (docstatus or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in docstatus → list().
- Set self.group\_by from group\_by.
- Set self.order\_by from order\_by.
- Set self.limit\_start from cint(limit\_start).
- Set self.limit\_page\_length from cint(limit\_page\_length) when limit\_page\_length, otherwise no value.
  - Value choice on limit\_page\_length — true gives cint(limit\_page\_length), false gives no value.
- Set self.with\_childnames from with\_childnames.
- Set self.debug from debug.
- Set self.join from join.
- Set self.distinct from distinct.
- Set self.as\_list from as\_list.
- Set self.ignore\_ifnull from ignore\_ifnull.
- Set self.flags.ignore\_permissions from ignore\_permissions.
- Set self.update from update.
- Set self.user\_settings\_fields from copy.deepcopy(self.fields).
- Set self.run from run.
- Set self.strict from strict.
- Set self.ignore\_ddl from ignore\_ddl.
- Set self.parent\_doctype from parent\_doctype.
- Set self.reference\_doctype from (reference\_doctype or self.doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doctype → self.doctype.
- If user\_settings.
  - Set self.user\_settings from json.loads(user\_settings).
- If is\_virtual\_doctype(self.doctype).
  - Bind dependencies get\_controller.
  - Set controller from get\_controller(self.doctype).
  - If not hasattr(controller, “get\_list”).
    - Return list().
  - Evaluate self.parse\_args().
  - Set kwargs from (mapping(“as\_list” → as\_list, “with\_comment\_count” → with\_comment\_count, “save\_user\_settings” → save\_user\_settings, “save\_user\_settings\_fields” → save\_user\_settings\_fields, …) bitwise or self.\_\_dict\_\_).
  - Return Platform.call(controller.get\_list, args = kwargs, expanded names kwargs).
- Set self.with\_comment\_count from (sbool(with\_comment\_count) and not as\_list and bool(self.doctype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sbool(with\_comment\_count) → not as\_list → bool(self.doctype).
- Set self.columns from self.get\_table\_columns().
- If not self.columns.
  - Return list().
- Set result from self.build\_and\_run().
- If self.with\_comment\_count.
  - Evaluate self.add\_comment\_count(result).
- If save\_user\_settings.
  - Set self.save\_user\_settings\_fields from save\_user\_settings\_fields.
  - Evaluate self.update\_user\_settings().
- If pluck.
  - Return list of d at pluck for d drawn from result.
    - Draw d from result.
- If (self.doctype and result).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype → result.
  - Set result from self.mask\_fields(result).
- Return result.

**Methods declared on this owner** [check read permission](operations-030.md#op-35c46e6a0c453f), [parse args](operations-029.md#op-845715cb1746a0), [get table columns](operations-030.md#op-4607c9b36ef962), [build and run](operations-029.md#op-fe8f8affd0d991), [add comment count](operations-030.md#op-01ba2fd253a881), [update user settings](operations-031.md#op-0618935113e597), [mask fields](operations-029.md#op-2d6684ae57febb).

**Values supplied outside this operation** selected callable from get\_controller(self.doctype).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L130) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L629) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1221)

<a id="op-2d6684ae57febb"></a>
### Database Query.mask fields

`operation_foundation_model_persistent_records_query_business_behavior_database_query_mask_fields`

**Inputs** self, result.

**Explicit results** result · mask\_list\_results(result, masked\_fields, field\_index\_map) · mask\_dict\_results(result, masked\_fields).

**Local steps**

- Bind dependencies mask\_dict\_results, mask\_list\_results.
- Set masked\_fields from self.get\_masked\_fields().
- If not masked\_fields.
  - Return result.
- If self.as\_list.
  - Set field\_index\_map from mapping().
  - For each tuple(idx, field) in enumerate(self.fields).
    - If “ as ” belongs to field.lower().
      - Set alias from field.split(“ as ”) at 1.strip(“ '”).
      - Set field\_index\_map at alias from idx.
    - Otherwise.
      - Set col from field.split(“.”) at negative 1.strip(“′”).
      - Set field\_index\_map at col from idx.
  - Return mask\_list\_results(result, masked\_fields, field\_index\_map).
- Otherwise.
  - Return mask\_dict\_results(result, masked\_fields).

**Methods declared on this owner** [get masked fields](operations-029.md#op-940719a2c6fa90).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L133) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1229)

<a id="op-940719a2c6fa90"></a>
### Database Query.get masked fields

`operation_foundation_model_persistent_records_query_business_behavior_database_query_get_masked_fields`

**Inputs** self.

**Explicit results** meta.get\_masked\_fields(parenttype = self.parent\_doctype).

**Local steps**

- Set meta from self.get\_meta(self.doctype).
- Return meta.get\_masked\_fields(parenttype = self.parent\_doctype).

**Methods declared on this owner** [get meta](operations-029.md#op-79800d6d423b9a).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L131) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L631) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1223)

<a id="op-fe8f8affd0d991"></a>
### Database Query.build and run

`operation_foundation_model_persistent_records_query_business_behavior_database_query_build_and_run`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** list() · Platform.db.sql(query, as\_dict = not self.as\_list, debug = self.debug, update = self.update, ignore\_ddl = self.ignore\_ddl, …).

**Local steps**

- Set args from self.prepare\_args().
- Set args.limit from self.add\_limit().
- If not args.fields.
  - Return list().
- If args.conditions.
  - Set args.conditions from (“where ” + args.conditions).
- If self.distinct.
  - Set args.fields from (“distinct ” + args.fields).
  - If Platform.db.db\_type equals “postgres”.
    - Set args.order\_by from empty text.
- If (Platform.db.db\_type equals “postgres” and args.order\_by and args.group\_by).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.db\_type equals “postgres” → args.order\_by → args.group\_by.
  - Set args from self.prepare\_select\_args(args).
- Set query from query text (SELECT).format(expanded names args).
- Return Platform.db.sql(query, as\_dict = not self.as\_list, debug = self.debug, update = self.update, ignore\_ddl = self.ignore\_ddl, …).

**Methods declared on this owner** [prepare args](operations-029.md#op-572c3bcfb26947), [add limit](operations-030.md#op-a3a8f02e420241), [prepare select args](operations-029.md#op-c673b5fec59aa6).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L128) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L620) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1215)

<a id="op-572c3bcfb26947"></a>
### Database Query.prepare args

`operation_foundation_model_persistent_records_query_business_behavior_database_query_prepare_arguments`

**Inputs** self.

**Explicit results** args.

**Local steps**

- Evaluate self.parse\_args().
- Evaluate self.sanitize\_fields().
- Evaluate self.extract\_tables().
- Evaluate self.set\_optional\_columns().
- Evaluate self.build\_conditions().
- Evaluate self.apply\_fieldlevel\_read\_permissions().
- Set self.has\_own\_name from self.selects\_own\_name().
- If (self.with\_comment\_count and self.distinct and not self.has\_own\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.with\_comment\_count → self.distinct → not self.has\_own\_name.
  - Set self.with\_comment\_count from false.
- If (self.with\_comment\_count and not self.group\_by and “\_comments” belongs to self.columns).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.with\_comment\_count → not self.group\_by → “\_comments” belongs to self.columns.
  - Evaluate self.fields.append(formatted text ′tab{self.doctype}′.′\_comments′).
- Set args from Platform.\_dict().
- If self.with\_childnames.
  - For each t in self.tables.
    - If t differs from formatted text ′tab{self.doctype}′.
      - Evaluate self.fields.append(formatted text {t}.name as '{t at slice 4 to negative 1}:name').
- Set args.tables from self.tables at 0.
- For each child in self.tables at slice 1 to no value.
  - Set parent\_name from cast\_name(formatted text {self.tables at 0}.name).
  - Update args.tables using + formatted text  {self.join} {child} on ({child}.parenttype = {Platform.db.escape(self.doctype)} and {child}.parent = {parent\_name}).
- For each link in self.link\_tables.
  - Update args.tables using + formatted text  {self.join} {link.table\_name} {link.table\_alias} on ({link.table\_alias}.′name′ = {self.tables at 0}.′{link.fieldname}′).
- If self.grouped\_or\_conditions.
  - Evaluate self.conditions.append(formatted text ({“ or ”.join(self.grouped\_or\_conditions)})).
- Set args.conditions from “ and ”.join(self.conditions).
- If self.or\_conditions.
  - Update args.conditions using + (“ or ” when args.conditions, otherwise empty text + “ or ”.join(self.or\_conditions)).
    - Value choice on args.conditions — true gives “ or ”, false gives empty text.
- Evaluate self.set\_field\_tables().
- Evaluate self.cast\_name\_fields().
- Set fields from list().
- For each field in self.fields.
  - If field is identical to no value.
    - Evaluate fields.append(“NULL”).
    - Continue with the next iteration or loop test.
  - Set stripped\_field from field.strip().lower().
  - If (stripped\_field at 0 belongs to set(“′”, “\*”, “"”, “'”) or “(” belongs to stripped\_field or “distinct” belongs to stripped\_field).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in stripped\_field at 0 belongs to set(“′”, “\*”, “"”, “'”) → “(” belongs to stripped\_field → “distinct” belongs to stripped\_field.
    - Evaluate fields.append(field).
  - Otherwise.
    - If “as” belongs to stripped\_field.split(one space).
      - Set tuple(col, \_, new) from field.split().
      - Evaluate fields.append(formatted text ′{col}′ as {new}).
    - Otherwise.
      - Evaluate fields.append(formatted text ′{field}′).
- Set args.fields from “, ”.join(fields).
- Evaluate self.set\_order\_by(args).
- Evaluate self.validate\_order\_by\_and\_group\_by(args.order\_by).
- Set args.order\_by from ((args.order\_by and (“ order by ” + args.order\_by)) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (args.order\_by and (“ order by ” + args.order\_by)) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.order\_by → (“ order by ” + args.order\_by).
- Evaluate self.validate\_order\_by\_and\_group\_by(self.group\_by).
- Set args.group\_by from ((self.group\_by and (“ group by ” + self.group\_by)) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.group\_by and (“ group by ” + self.group\_by)) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.group\_by → (“ group by ” + self.group\_by).
- Return args.

**Methods declared on this owner** [parse args](operations-029.md#op-845715cb1746a0), [sanitize fields](operations-029.md#op-3bf67529575f4d), [extract tables](operations-030.md#op-ebaeeca9e28d31), [set optional columns](operations-030.md#op-64f96ca1260884), [build conditions](operations-030.md#op-137ddc8a2ffa57), [apply fieldlevel read permissions](operations-030.md#op-98805c4c4b2fd3), [selects own name](operations-031.md#op-2e4e1aa2b857a8), [set field tables](operations-030.md#op-1a15dc1b722e15), [cast name fields](operations-030.md#op-12822d54a64f99), [set order by](operations-030.md#op-f6b7a53a66a725), [validate order by and group by](operations-030.md#op-5df0c62cf89449).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L134) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1231)

<a id="op-c673b5fec59aa6"></a>
### Database Query.prepare select args

`operation_foundation_model_persistent_records_query_business_behavior_database_query_prepare_select_arguments`

**Inputs** self, args.

**Explicit results** args.

**Local steps**

- Set order\_field from ORDER\_BY\_PATTERN.sub(empty text, args.order\_by).
- If order\_field does not belong to args.fields.
  - Set extracted\_column, order\_column from order\_field.replace(“′”, empty text).
  - If “.” belongs to extracted\_column.
    - Set extracted\_column from extracted\_column.split(“.”) at 1.
  - Update args.fields using + formatted text , MAX({extracted\_column}) as ′{order\_column}′.
  - Set args.order\_by from args.order\_by.replace(order\_field, formatted text ′{order\_column}′).
- Return args.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L570) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1233)

<a id="op-845715cb1746a0"></a>
### Database Query.parse args

`operation_foundation_model_persistent_records_query_business_behavior_database_query_parse_arguments`

**Inputs** self.

**Local steps**

- If isinstance(self.fields, str).
  - If self.fields equals “\*”.
    - Set self.fields from list(“\*”).
  - Otherwise.
    - Attempt the following.
      - Set self.fields from json.loads(self.fields).
    - On failure (ValueError).
      - Set self.fields from list of f.strip() for f drawn from self.fields.split(“,”).
        - Draw f from self.fields.split(“,”).
- Set self.fields from list of f for f drawn from self.fields where f.
  - Draw f from self.fields, keep a combination only if (f).
- For each field in self.fields.
  - If “.” belongs to field.
    - Set original\_field from field.
    - Set alias from no value.
    - If “ as ” belongs to field.
      - Set tuple(field, alias) from field.split(“ as ”, 1).
    - Set tuple(linked\_fieldname, fieldname) from field.split(“.”, 1).
    - Set linked\_field from self.get\_meta(self.doctype).get\_field(linked\_fieldname).
    - If not linked\_field.
      - Continue with the next iteration or loop test.
    - Set linked\_doctype from linked\_field.options.
    - If linked\_field.fieldtype equals “Link”.
      - Set linked\_table from self.append\_link\_table(linked\_doctype, linked\_fieldname).
      - Set field from formatted text {linked\_table.table\_alias}.′{fieldname}′.
    - Otherwise.
      - Set field from formatted text ′tab{linked\_doctype}′.′{fieldname}′.
    - If alias.
      - Set field from formatted text {field} as {alias}.
    - Set self.fields at self.fields.index(original\_field) from field.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get meta](operations-029.md#op-79800d6d423b9a), [append link table](operations-030.md#op-5aaf1d39580d19).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L1830) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1230)

<a id="op-3bf67529575f4d"></a>
### Database Query.sanitize fields

`operation_foundation_model_persistent_records_query_business_behavior_database_query_sanitize_fields`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 7 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L2616) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1238)

<a id="op-aba48946cdc166"></a>
### Database Query.sanitize fields.find subqueries

`operation_foundation_model_persistent_records_query_business_behavior_database_query_sanitize_fields_find_subqueries`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** parsed.

**Explicit result forms** a value selected from the current context.

**Local structure** 4 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L4175) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1240)

<a id="op-c9a89d36f79651"></a>
### Database Query.sanitize fields.check sql token

`operation_foundation_model_persistent_records_query_business_behavior_database_query_sanitize_fields_check_database_query_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** statement.

**Local structure** 8 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L4477) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1239)

<a id="op-81b58446ca6e0a"></a>
### Database Query.sanitize fields.raise exception

`operation_foundation_model_persistent_records_query_business_behavior_database_query_sanitize_fields_raise_exception`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** no parameters.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L5036) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1242)

<a id="op-37d9fc4cadd726"></a>
### Database Query.sanitize fields.is query

`operation_foundation_model_persistent_records_query_business_behavior_database_query_sanitize_fields_is_query`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** field.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0270.json#L5105) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1241)
