# Record lifecycle and persistence · operations 85

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Report

[Record definition](../../../../data/record-types/report.json)

<a id="op-24e6108dc15d0c"></a>
### Report.is permitted

`operation_foundation_core_record_definitions_report_business_behavior_report_is_permitted`

**Inputs** self.

**Record and data access** read “Has Role” via get\_all.

**Explicit results** true.

**Local steps**

- Bind dependencies has\_common.
- Set allowed from list of d.role for d drawn from Platform.get\_all(“Has Role”, fields = list(“role”), filters = mapping(“parent” → self.name)).
  - Draw d from Platform.get\_all(“Has Role”, fields = list(“role”), filters = mapping(“parent” → self.name)).
- Set custom\_roles from get\_custom\_allowed\_roles(“report”, self.name).
- If custom\_roles.
  - Set allowed from custom\_roles.
- If not allowed.
  - Return true.
- If has\_common(Platform.get\_roles(), allowed).
  - Return true.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L1800) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L226) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L402)

<a id="op-1c28cca06e6173"></a>
### Report.update report json

`operation_foundation_core_record_definitions_report_business_behavior_report_update_report_structured_data`

**Inputs** self.

**Local steps**

- If not self.json.
  - Set self.json from “{}”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L2084) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L410)

<a id="op-0441bbb1310b0c"></a>
### Report.export doc

`operation_foundation_core_record_definitions_report_business_behavior_report_export_record`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- If (self.is\_standard equals “Yes” and Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard equals “Yes” → Platform.conf.developer\_mode.
  - Evaluate export\_to\_files(record\_list = list(list(“Report”, self.name)), record\_module = self.module, create\_init = true).
  - Evaluate self.create\_report\_py().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create report py](operations-085.md#op-f4658f3c5ebe76).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L2149) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L216) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L392)

<a id="op-f4658f3c5ebe76"></a>
### Report.create report py

`operation_foundation_core_record_definitions_report_business_behavior_report_create_report_business_behavior`

**Inputs** self.

**Local steps**

- If self.report\_type equals “Script Report”.
  - Evaluate make\_boilerplate(“controller.py”, self, mapping(“name” → self.name)).
  - Evaluate make\_boilerplate(“controller.js”, self, mapping(“name” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L2344) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L385)

<a id="op-4ffefd8b1f4b65"></a>
### Report.execute query report

`operation_foundation_core_record_definitions_report_business_behavior_report_execute_query_report`

**Inputs** self, filters.

**State and service calls** execute a supplied database query.

**Explicit results** list(columns, result).

**Explicit failure paths** validation helper — translated “Must specify a Query to run”.

**Local steps**

- If not self.query.
  - Call the validation error handler Platform.throw(translated “Must specify a Query to run”, title = translated “Report Document Error”).
- Evaluate check\_safe\_sql\_query(self.query).
- Set result from list of list(t) for t drawn from Platform.db.sql(self.query, filters).
  - Draw t from Platform.db.sql(self.query, filters).
- Set columns from (self.get\_columns() or list of cstr(c at 0) for c drawn from Platform.db.get\_description()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_columns() → list of cstr(c at 0) for c drawn from Platform.db.get\_description().
  - Draw c from Platform.db.get\_description().
- Return list(columns, result).

**Methods declared on this owner** [get columns](operations-084.md#op-55cfa4e81539cb).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L18) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L388)

<a id="op-89ea8291cfda39"></a>
### Report.execute script report

`operation_foundation_core_record_definitions_report_business_behavior_report_execute_script_report`

**Inputs** self, filters.

**State and service calls** call cancel on prepared\_report\_watcher.

**Explicit results** res.

**Local steps**

- Set threshold from 15.
- Set start\_time from datetime.datetime.now().
- Set prepared\_report\_watcher from no value.
- If (not self.prepared\_report and not self.disable\_prepared\_report\_automation).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.prepared\_report → not self.disable\_prepared\_report\_automation.
  - Set prepared\_report\_watcher from threading.Timer(interval = threshold, function = enable\_prepared\_report, kwargs = mapping(“report” → self.name, “site” → Platform.local.site)).
  - Evaluate prepared\_report\_watcher.start().
- Attempt the following.
  - If self.is\_standard equals “Yes”.
    - If self.snapshot\_report.
      - Set res from self.execute\_snapshot\_report(filters).
    - Otherwise.
      - Set res from self.execute\_module(filters).
  - Otherwise.
    - Set res from self.execute\_script(filters).
- On exit, including pending return or failure.
  - Evaluate (prepared\_report\_watcher and prepared\_report\_watcher.cancel()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in prepared\_report\_watcher → prepared\_report\_watcher.cancel().
- Set execution\_time from (datetime.datetime.now() − start\_time).total\_seconds().
- Evaluate Platform.cache.hset(“report\_execution\_time”, self.name, execution\_time).
- Return res.

**Methods declared on this owner** [execute snapshot report](operations-085.md#op-82baec207c7486), [execute module](operations-085.md#op-1fa0628a346908), [execute script](operations-085.md#op-56f441b14eb881).

**Values supplied outside this operation** clock or generated value from datetime.datetime.now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L19) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L390)

<a id="op-2398a6d5979ee4"></a>
### Report.get module method

`operation_foundation_core_record_definitions_report_business_behavior_report_get_module_method`

**Inputs** self, method.

**Record and data access** read “DocType” via get\_value.

**Explicit results** Platform.get\_attr(method\_path).

**Explicit failure paths** Exception(“Unknown report method”).

**Local steps**

- If method does not belong to tuple(“execute”, “execute\_snapshot\_report”, “get\_xlsx\_styles”).
  - Raise Exception(“Unknown report method”).
- Set module from (self.module or Platform.db.get\_value(“DocType”, self.ref\_doctype, “module”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.module → Platform.db.get\_value(“DocType”, self.ref\_doctype, “module”).
- Set method\_path from ((get\_report\_module\_dotted\_path(module, self.name) + “.”) + method).
- Return Platform.get\_attr(method\_path).

**Values supplied outside this operation** selected callable from Platform.get\_attr(method\_path).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L3420) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L220) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L396)

<a id="op-1fa0628a346908"></a>
### Report.execute module

`operation_foundation_core_record_definitions_report_business_behavior_report_execute_module`

**Inputs** self, filters.

**Explicit results** self.get\_module\_method(“execute”)(Platform.\_dict(filters)).

**Local steps**

- Return self.get\_module\_method(“execute”)(Platform.\_dict(filters)).

**Methods declared on this owner** [get module method](operations-085.md#op-2398a6d5979ee4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L3663) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L387)

<a id="op-56f441b14eb881"></a>
### Report.execute script

`operation_foundation_core_record_definitions_report_business_behavior_report_execute_script`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, filters.

**Explicit result forms** a structured result, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L3755) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L389)

<a id="op-82baec207c7486"></a>
### Report.execute snapshot report

`operation_foundation_core_record_definitions_report_business_behavior_report_execute_snapshot_report`

**Inputs** self, filters.

**Explicit results** tuple(list(), list()) · execute\_snapshot\_report(Platform.\_dict(filters)).

**Local steps**

- Attempt the following.
  - Set execute\_snapshot\_report from self.get\_module\_method(“execute\_snapshot\_report”).
- On failure (AttributeError).
  - Return tuple(list(), list()).
- Return execute\_snapshot\_report(Platform.\_dict(filters)).

**Methods declared on this owner** [get module method](operations-085.md#op-2398a6d5979ee4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L4018) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L215) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L391)

<a id="op-2f627ab05283cc"></a>
### Report.get data

`operation_foundation_core_record_definitions_report_business_behavior_report_get_data`

**Inputs** self, filters = no value, limit = no value, user = no value, as\_dict = false, ignore\_prepared\_report = false, are\_default\_filters = true.

**Explicit results** tuple(columns, result).

**Local steps**

- If self.report\_type belongs to tuple(“Query Report”, “Script Report”, “Custom Report”).
  - Set tuple(columns, result) from self.run\_query\_report(filters, user, ignore\_prepared\_report, are\_default\_filters).
- Otherwise.
  - Set tuple(columns, result) from self.run\_standard\_report(filters, limit, user).
- If as\_dict.
  - Set result from self.build\_data\_dict(result, columns).
- Return tuple(columns, result).

**Methods declared on this owner** [run query report](operations-085.md#op-96caa91ba520df), [run standard report](operations-085.md#op-0e001354825200), [build data dict](operations-085.md#op-24e9542bdbe68c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L4159) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L219) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L395)

<a id="op-96caa91ba520df"></a>
### Report.run query report

`operation_foundation_core_record_definitions_report_business_behavior_report_run_query_report`

**Inputs** self, filters = no value, user = no value, ignore\_prepared\_report = false, are\_default\_filters = true.

**Explicit results** tuple(columns, result).

**Local steps**

- Set tuple(columns, result) from tuple(list(), list()).
- Set data from \_run(report\_name = self.name, filters = filters, user = user, ignore\_prepared\_report = ignore\_prepared\_report, …).
- For each d in data.get(“columns”).
  - If isinstance(d, dict).
    - Set col from Platform.\_dict(d).
    - If not col.fieldname.
      - Set col.fieldname from col.label.
    - Evaluate columns.append(col).
  - Otherwise.
    - Set tuple(fieldtype, options) from tuple(“Data”, no value).
    - Set parts from d.split(“:”).
    - If len(parts) &gt; 1.
      - If parts at 1.
        - Set tuple(fieldtype, options) from tuple(parts at 1, no value).
        - If (fieldtype and “/” belongs to fieldtype).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldtype → “/” belongs to fieldtype.
          - Set tuple(fieldtype, options) from fieldtype.split(“/”).
    - Evaluate columns.append(Platform.\_dict(label = parts at 0, fieldtype = fieldtype, fieldname = parts at 0, options = options)).
- Update result using + data.get(“result”).
- Return tuple(columns, result).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L4454) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L229) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L405)

<a id="op-0e001354825200"></a>
### Report.run standard report

`operation_foundation_core_record_definitions_report_business_behavior_report_run_standard_report`

**Inputs** self, filters, limit, user.

**Record and data access** read self.ref\_doctype via get\_list.

**Explicit results** tuple(columns, result).

**Local steps**

- Set params from json.loads(self.json).
- Set columns from self.get\_standard\_report\_columns(params).
- Set result from list().
- Set tuple(order\_by, group\_by, group\_by\_args) from self.get\_standard\_report\_order\_by(params).
- Set \_result from Platform.get\_list(self.ref\_doctype, fields = list of get\_group\_by\_field(group\_by\_args, c at 1) when (c at 0 equals “\_aggregate\_column” and group\_by\_args), otherwise Report.\_format(list(c at 1, c at 0)) for ….
  - Draw c from columns.
  - Value choice on (c at 0 equals “\_aggregate\_column” and group\_by\_args) — true gives get\_group\_by\_field(group\_by\_args, c at 1), false gives Report.\_format(list(c at 1, c at 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in c at 0 equals “\_aggregate\_column” → group\_by\_args.
- Set columns from self.build\_standard\_report\_columns(columns, group\_by\_args).
- Set result from (result + list of list(d) for d drawn from \_result).
  - Draw d from \_result.
- If params.get(“add\_totals\_row”).
  - Set result from append\_totals\_row(result).
- Return tuple(columns, result).

**Methods declared on this owner** [get standard report columns](operations-085.md#op-4af5c19961bb67), [get standard report order by](operations-085.md#op-c0339218359845), [get standard report filters](operations-085.md#op-24a157a5d7ce5e), [build standard report columns](operations-085.md#op-d61e474fc6fef8).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L23) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L230) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L406)

<a id="op-08a5fadc9c6d4a"></a>
### Report.format

`operation_foundation_core_record_definitions_report_business_behavior_report_format`

**Inputs** parts.

**Wrappers, in declaration order** staticmethod.

**Explicit results** “′tab{}′.′{}′”.format(expanded parts).

**Local steps**

- Return “′tab{}′.′{}′”.format(expanded parts).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L5691) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L217) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L393)

<a id="op-4af5c19961bb67"></a>
### Report.get standard report columns

`operation_foundation_core_record_definitions_report_business_behavior_report_get_standard_report_columns`

**Inputs** self, params.

**Explicit results** columns.

**Local steps**

- If params.get(“fields”).
  - Set columns from params.get(“fields”).
- Otherwise.
  - If params.get(“columns”).
    - Set columns from params.get(“columns”).
  - Otherwise.
    - Set columns from list(list(“name”, self.ref\_doctype)).
    - Evaluate columns.extend(generator of list(df.fieldname, self.ref\_doctype) for df drawn from Platform.get\_meta(self.ref\_doctype).fields where df.in\_list\_view).
      - Draw df from Platform.get\_meta(self.ref\_doctype).fields, keep a combination only if (df.in\_list\_view).
- Return columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L21) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L223) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L399)

<a id="op-24a157a5d7ce5e"></a>
### Report.get standard report filters

`operation_foundation_core_record_definitions_report_business_behavior_report_get_standard_report_filters`

**Inputs** self, params, filters.

**Explicit results** \_filters.

**Local steps**

- Set \_filters from (params.get(“filters”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in params.get(“filters”) → list().
- If filters.
  - For each tuple(key, value) in filters.items().
    - Set tuple(condition, \_value) from tuple(“=”, value).
    - If isinstance(value, (list bitwise or tuple)).
      - Set tuple(condition, \_value) from value.
    - Evaluate \_filters.append(list(key, condition, \_value)).
- Return \_filters.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0097.json#L6081) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L224) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L400)

<a id="op-c0339218359845"></a>
### Report.get standard report order by

`operation_foundation_core_record_definitions_report_business_behavior_report_get_standard_report_order_by`

**Inputs** self, params.

**Explicit results** tuple(order\_by, group\_by, group\_by\_args).

**Local steps**

- Set group\_by\_args from no value.
- If params.get(“sort\_by”).
  - Set order\_by from ((Report.\_format(nested operand in the contract.get(“sort\_by”).split(“.”)) + one space) + params.get(“sort\_order”)).
- Otherwise.
  - If params.get(“order\_by”).
    - Set order\_by from params.get(“order\_by”).
  - Otherwise.
    - Set order\_by from (Report.\_format(list(self.ref\_doctype, “creation”)) + “ desc”).
- If params.get(“sort\_by\_next”).
  - Update order\_by using + (((“, ” + Report.\_format(nested operand in the contract(nested operand in the contract).split(“.”))) + one space) + params.get(“sort\_order\_next”)).
- Set group\_by from no value.
- If params.get(“group\_by”).
  - Set group\_by\_args from Platform.\_dict(params at “group\_by”).
  - Set group\_by from group\_by\_args at “group\_by”.
  - Set order\_by from “\_aggregate\_column desc”.
- Return tuple(order\_by, group\_by, group\_by\_args).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L22) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L225) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L401)

<a id="op-d61e474fc6fef8"></a>
### Report.build standard report columns

`operation_foundation_core_record_definitions_report_business_behavior_report_build_standard_report_columns`

**Inputs** self, columns, group\_by\_args.

**Explicit results** report\_columns.

**Local steps**

- Bind dependencies get\_default\_df.
- Set report\_columns from list().
- For each tuple(fieldname, doctype) in columns.
  - Set meta from Platform.get\_meta(doctype).
  - If meta\_df bound to meta.get\_field(fieldname).
    - Set column from meta\_df.as\_dict().
  - Otherwise.
    - If default\_df bound to get\_default\_df(fieldname).
      - Set column from default\_df.copy().
      - If not column.get(“label”).
        - Set column.label from meta.get\_label(fieldname).
    - Otherwise.
      - Set label from get\_group\_by\_column\_label(group\_by\_args, meta) when fieldname equals “\_aggregate\_column”, otherwise meta.get\_label(fieldname).
        - Value choice on fieldname equals “\_aggregate\_column” — true gives get\_group\_by\_column\_label(group\_by\_args, meta), false gives meta.get\_label(fieldname).
      - Set column from Platform.\_dict(mapping(“fieldname” → fieldname, “label” → label, “fieldtype” → “Link” when fieldname equals “name”, otherwise “Data”, “options” → doctype when fieldname equals “name”, otherwise no value)).
        - Value choice on fieldname equals “name” — true gives “Link”, false gives “Data”.
        - Value choice on fieldname equals “name” — true gives doctype, false gives no value.
  - Evaluate report\_columns.append(column).
- Return report\_columns.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L17) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L383)

<a id="op-24e9542bdbe68c"></a>
### Report.build data dict

`operation_foundation_core_record_definitions_report_business_behavior_report_build_data_mapping`

**Inputs** self, result, columns.

**Explicit results** data.

**Local steps**

- Set data from list().
- For each row in result.
  - If isinstance(row, (list bitwise or tuple)).
    - Set \_row from Platform.\_dict().
    - For each tuple(i, val) in enumerate(row).
      - Set \_row at columns at i.get(“fieldname”) from val.
  - Otherwise.
    - If isinstance(row, dict).
      - Set \_row from Platform.\_dict(row).
  - Evaluate data.append(\_row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0098.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L382)

<a id="op-a1f5034a8f4d15"></a>
### Report.validate standard report

`operation_foundation_core_record_definitions_report_business_behavior_report_validate_standard_report`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Only Administrator can save a standard report. Please rename and save.” · validation helper — translated “Standard reports can only be created in developer mode.”.

**Local steps**

- If Platform.session.user differs from “Administrator”.
  - Call the validation error handler Platform.throw(translated “Only Administrator can save a standard report. Please rename and save.”).
- If (not cint(Platform.conf.developer\_mode) and not (Platform.flags.in\_migrate or Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_import)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(Platform.conf.developer\_mode) → not (Platform.flags.in\_migrate or Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_import).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → Platform.flags.in\_patch → Platform.flags.in\_install → Platform.flags.in\_import.
  - Call the validation error handler Platform.throw(translated “Standard reports can only be created in developer mode.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L26) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L238) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L412)

<a id="op-fc8a0ebcf0398f"></a>
### Report.toggle disable

`operation_foundation_core_record_definitions_report_business_behavior_report_toggle_disable`

**Inputs** self, disable.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Explicit failure paths** validation helper — translated “You are not allowed to edit the report.”.

**Local steps**

- If not Platform.has\_permission(self.doctype, “write”, doc = self).
  - Call the validation error handler Platform.throw(translated “You are not allowed to edit the report.”).
- Evaluate self.db\_set(“disabled”, cint(disable)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “write”, doc = self).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L24) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L232) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L408)

<a id="op-a4843dcca8691b"></a>
### Report.get xlsx styles from module

`operation_foundation_core_record_definitions_report_business_behavior_report_get_spreadsheet_workbook_styles_from_module`

**Inputs** self, metadata.

**Declared result** dict.

**Explicit results** no value · method(metadata).

**Local steps**

- If (self.is\_standard differs from “Yes” or self.report\_type does not belong to tuple(“Query Report”, “Script Report”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_standard differs from “Yes” → self.report\_type does not belong to tuple(“Query Report”, “Script Report”).
  - Return no value.
- Attempt the following.
  - Set method from self.get\_module\_method(“get\_xlsx\_styles”).
- On failure (tuple(AttributeError, ModuleNotFoundError)).
  - Return no value.
- Return method(metadata).

**Methods declared on this owner** [get module method](operations-085.md#op-2398a6d5979ee4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L20) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L222) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L398)

<a id="op-e6e3d09d66ad85"></a>
### Is prepared report enabled

`operation_foundation_core_record_definitions_report_business_behavior_is_prepared_report_enabled`

**Inputs** report.

**Record and data access** read “Report” via get\_value.

**Explicit results** cint(Platform.db.get\_value(“Report”, report, “prepared\_report”)).

**Local steps**

- Return cint(Platform.db.get\_value(“Report”, report, “prepared\_report”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0098.json#L1428) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L379)

<a id="op-07cada1ff822fa"></a>
### Get report module dotted path

`operation_foundation_core_record_definitions_report_business_behavior_get_report_module_dotted_path`

**Inputs** module, report\_name.

**Explicit results** ((((((nested operand in the contract at nested operand in the contract + “.”) + scrub(module)) + “.report.”) + scrub(report\_name)) + “.”) + scrub(report\_name)).

**Local steps**

- Return ((((((nested operand in the contract at nested operand in the contract + “.”) + scrub(module)) + “.report.”) + scrub(report\_name)) + “.”) + scrub(report\_name)).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0098.json#L1519) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L378)
