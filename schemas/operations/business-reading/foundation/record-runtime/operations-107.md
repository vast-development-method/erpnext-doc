# Record lifecycle and persistence · operations 107

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-fbdea2fb91119b"></a>
### Mask child query fields

`operation_foundation_query_builder_utils_business_behavior_mask_child_query_fields`

**Inputs** child\_queries, result.

**Explicit results** no value.

**Local steps**

- If not isinstance(result at 0, dict).
  - Return no value.
- Bind dependencies CORE\_DOCTYPES.
- Bind dependencies mask\_dict\_results.
- For each child\_query in child\_queries.
  - If child\_query.doctype belongs to CORE\_DOCTYPES.
    - Continue with the next iteration or loop test.
  - Set masked\_fields from Platform.get\_meta(child\_query.doctype).get\_masked\_fields(parenttype = child\_query.parent\_doctype).
  - If not masked\_fields.
    - Continue with the next iteration or loop test.
  - For each row in result.
    - Evaluate mask\_dict\_results((row.get(child\_query.fieldname) or list()), masked\_fields).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(child\_query.fieldname) → list().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L5605) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L187)

<a id="op-3bab1472c46540"></a>
### Execute child queries

`operation_foundation_query_builder_utils_business_behavior_execute_child_queries`

**Inputs** queries, result.

**Explicit results** no value.

**Local steps**

- If (not isinstance(result at 0, dict) or not result at 0.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(result at 0, dict) → not result at 0.name.
  - Return no value.
- Set parent\_names from list of d.name for d drawn from result.
  - Draw d from result.
- For each child\_query in queries.
  - Set data from child\_query.get\_query(parent\_names).run(as\_dict = 1).
  - For each row in result.
    - Set row at child\_query.fieldname from list().
    - For each d in data.
      - If (str(d.parent) equals str(row.name) and d.parentfield equals child\_query.fieldname).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in str(d.parent) equals str(row.name) → d.parentfield equals child\_query.fieldname.
        - If “parent” does not belong to child\_query.fields.
          - Remove d at “parent”.
        - If “parentfield” does not belong to child\_query.fields.
          - Remove d at “parentfield”.
        - Evaluate row at child\_query.fieldname.append(d).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L5893) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L180)

<a id="op-a0f05629710831"></a>
### Render criterion

`operation_foundation_binding_foundation_query_builder_utils_render_criterion`

**Inputs** criterion.

**Declared result** str.

**Explicit results** criterion.get\_sql(with\_namespace = true, quote\_char = quote\_char, param\_wrapper = EscapedValueWrapper(), subquery = true).

**Local steps**

- Set quote\_char from “′” when Platform.db.db\_type equals “mariadb”, otherwise “"”.
  - Value choice on Platform.db.db\_type equals “mariadb” — true gives “′”, false gives “"”.
- Return criterion.get\_sql(with\_namespace = true, quote\_char = quote\_char, param\_wrapper = EscapedValueWrapper(), subquery = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1691)

<a id="op-74cde57db03a8a"></a>
### Prepare query

`operation_foundation_query_builder_utils_business_behavior_prepare_query`

**Inputs** query.

**Explicit results** tuple(query, param\_collector.parameters).

**Explicit failure paths** Platform.PermissionError(“Only SELECT SQL allowed in scripting”).

**Local steps**

- Bind dependencies SERVER\_SCRIPT\_FILE\_PREFIX, check\_safe\_sql\_query.
- Set param\_collector from NamedParameterWrapper().
- Set query from query.get\_sql(param\_wrapper = param\_collector).
- If Platform.local.flags.get(“in\_safe\_exec”, false).
  - If not check\_safe\_sql\_query(query, throw = false).
    - Set callstack from inspect.stack().
    - If (len(callstack) ≥ 3 and SERVER\_SCRIPT\_FILE\_PREFIX belongs to callstack at 2.filename).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(callstack) ≥ 3 → SERVER\_SCRIPT\_FILE\_PREFIX belongs to callstack at 2.filename.
      - Raise Platform.PermissionError(“Only SELECT SQL allowed in scripting”).
- If Platform.local.flags.get(“in\_render\_safe\_exec”, false).
  - Evaluate check\_safe\_sql\_query(query, throw = true).
- Return tuple(query, param\_collector.parameters).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L104) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L193)

<a id="op-297a13c43e3278"></a>
### Patch query execute

`operation_foundation_query_builder_utils_business_behavior_patch_query_execute`

**Inputs** no declared parameters.

**Local steps**

- Set QueryBuilder.run from execute\_query.
- Set QueryBuilder.walk from prepare\_query.
- Set \_SetOperation.run from execute\_query.
- Set \_SetOperation.walk from prepare\_query.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L6789) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L192)

<a id="op-2d7935ebb4ce3b"></a>
### Patch query aggregation

`operation_foundation_query_builder_utils_business_behavior_patch_query_aggregation`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies \_avg, \_max, \_min, \_sum.
- Set Base.max from \_max.
- Set Base.min from \_min.
- Set Base.avg from \_avg.
- Set Base.sum from \_sum.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L6879) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L191)

<a id="op-b2b41fd9acb303"></a>
### Patch get query

`operation_foundation_query_builder_utils_business_behavior_patch_get_query`

**Inputs** no declared parameters.

**Local steps**

- Set Base.get\_query from get\_query.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0320.json#L6991) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1499) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L190)

<a id="op-5a47fbb8b8d637"></a>
### Patch all

`operation_foundation_query_builder_utils_business_behavior_patch_all`

**Inputs** no declared parameters.

**Local steps**

- Evaluate patch\_query\_execute().
- Evaluate patch\_query\_aggregation().
- Evaluate patch\_get\_query().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L103) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L189)

## Record · Version

[Record definition](../../../../data/record-types/version.json)

<a id="op-d45033a189abe8"></a>
### Version.update version info

`operation_foundation_core_record_definitions_version_business_behavior_version_update_version_info`

**Inputs** self, old, new.

**Declared result** bool.

**Explicit results** self.for\_insert(new) · self.set\_diff(old, new).

**Local steps**

- If not old.
  - Return self.for\_insert(new).
- Otherwise.
  - Return self.set\_diff(old, new).

**Methods declared on this owner** [for insert](operations-107.md#op-5acf6bfa00e898), [set diff](operations-107.md#op-060c86984c9fbf).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L4537) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L880)

<a id="op-596c08ddb79a91"></a>
### Version.set impersonator

`operation_foundation_core_record_definitions_version_business_behavior_version_set_impersonator`

**Inputs** data.

**Wrappers, in declaration order** staticmethod.

**Explicit results** no value.

**Local steps**

- If not Platform.session.
  - Return no value.
- If impersonator bound to Platform.session.data.get(“impersonated\_by”).
  - Set data at “impersonated\_by” from impersonator.
- If audit\_user bound to Platform.session.data.get(“audit\_user”).
  - Set data at “audit\_user” from audit\_user.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L4671) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L879)

<a id="op-060c86984c9fbf"></a>
### Version.set diff

`operation_foundation_core_record_definitions_version_business_behavior_version_set_diff`

**Inputs** self, old, new.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set diff from get\_diff(old, new).
- If diff.
  - Evaluate self.set\_impersonator(diff).
  - Set self.ref\_doctype from new.doctype.
  - Set self.docname from new.name.
  - Set self.data from Platform.as\_json(diff, indent = no value, separators = tuple(“,”, “:”)).
  - Return true.
- Otherwise.
  - Return false.

**Methods declared on this owner** [set impersonator](operations-107.md#op-596c08ddb79a91).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L4852) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L878)

<a id="op-5acf6bfa00e898"></a>
### Version.for insert

`operation_foundation_core_record_definitions_version_business_behavior_version_for_insert`

**Inputs** self, doc.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set updater\_reference from doc.flags.updater\_reference.
- If not updater\_reference.
  - Return false.
- Set data from mapping(“creation” → doc.creation, “updater\_reference” → updater\_reference, “created\_by” → doc.owner).
- Evaluate self.set\_impersonator(data).
- Set self.ref\_doctype from doc.doctype.
- Set self.docname from doc.name.
- Set self.data from Platform.as\_json(data, indent = no value, separators = tuple(“,”, “:”)).
- Return true.

**Methods declared on this owner** [set impersonator](operations-107.md#op-596c08ddb79a91).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L5098) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L875)

<a id="op-c596b8d42712a8"></a>
### Version.get data

`operation_foundation_core_record_definitions_version_business_behavior_version_get_data`

**Inputs** self.

**Explicit results** json.loads(self.data).

**Local steps**

- Return json.loads(self.data).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L5387) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L876)

<a id="op-f892dc92c7e82f"></a>
### Version.onload

`operation_foundation_core_record_definitions_version_business_behavior_version_onload`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.data.
  - Return no value.
- Set data from self.get\_data().
- Set changed from data.get(“changed”, list()).
- If not changed.
  - Return no value.
- Set html\_diffs from mapping().
- For each item in changed.
  - If len(item) ≥ 3.
    - Set tuple(fieldname, old\_str, new\_str) from tuple(item at 0, \_as\_string(item at 1), \_as\_string(item at 2)).
    - If not \_should\_generate\_html\_diff(old\_str, new\_str).
      - Continue with the next iteration or loop test.
    - Set html\_diff from \_generate\_html\_diff(old\_str, new\_str).
    - If html\_diff.
      - Set html\_diffs at fieldname from html\_diff.
- If html\_diffs.
  - Evaluate self.set\_onload(“html\_diffs”, html\_diffs).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get data](operations-107.md#op-c596b8d42712a8).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0118.json#L5445) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L877)

<a id="op-3de5e09271d6aa"></a>
### Get diff

`operation_foundation_core_record_definitions_version_business_behavior_get_diff`

**Inputs** old, new, for\_child = false, compare\_cancelled = false.

**Record and data access** read field\_meta.options via get\_values.

**Explicit results** no value · out.

**Local steps**

- If not new.
  - Return no value.
- Set blacklisted\_fields from list(“Markdown Editor”, “Text Editor”, “Code”, “HTML Editor”).
- Set data\_import from new.flags.via\_data\_import.
- Set updater\_reference from new.flags.updater\_reference.
- Set out from Platform.\_dict(changed = list(), added = list(), removed = list(), row\_changed = list(), …).
- If not for\_child.
  - Set amended\_from from new.get(“amended\_from”).
  - Set old\_row\_name\_field from “\_amended\_from” when (amended\_from and amended\_from equals old.name), otherwise “name”.
    - Value choice on (amended\_from and amended\_from equals old.name) — true gives “\_amended\_from”, false gives “name”.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in amended\_from → amended\_from equals old.name.
- For each df in new.meta.fields.
  - If (df.fieldtype belongs to FIELDTYPES\_TO\_IGNORE or getattr(df, “is\_virtual”, false)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldtype belongs to FIELDTYPES\_TO\_IGNORE → getattr(df, “is\_virtual”, false).
    - Continue with the next iteration or loop test.
  - Set tuple(old\_value, new\_value) from tuple(old.get(df.fieldname), new.get(df.fieldname)).
  - If df.fieldtype belongs to tuple(“Link”, “Dynamic Link”).
    - Set tuple(old\_value, new\_value) from tuple(cstr(old\_value), cstr(new\_value)).
  - If df.fieldtype belongs to datetime\_fields.
    - If (old\_value is identical to no value and new\_value equals empty text).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_value is identical to no value → new\_value equals empty text.
      - Set new\_value from no value.
  - If (not for\_child and df.fieldtype belongs to table\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not for\_child → df.fieldtype belongs to table\_fields.
    - Set old\_rows\_by\_name from mapping().
    - For each d in old\_value.
      - Set old\_rows\_by\_name at d.name from d.
    - Set found\_rows from set().
    - For each tuple(i, d) in enumerate(new\_value).
      - Set old\_row\_name from getattr(d, old\_row\_name\_field, no value).
      - If compare\_cancelled.
        - If amended\_from.
          - If len(old\_value) &gt; i.
            - Set old\_row\_name from old\_value at i.name.
      - If (old\_row\_name and old\_row\_name belongs to old\_rows\_by\_name).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_row\_name → old\_row\_name belongs to old\_rows\_by\_name.
        - Evaluate found\_rows.add(old\_row\_name).
        - Set diff from get\_diff(old\_rows\_by\_name at old\_row\_name, d, for\_child = true).
        - If (diff and diff.changed).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in diff → diff.changed.
          - Evaluate out.row\_changed.append(tuple(df.fieldname, i, d.name, diff.changed)).
      - Otherwise.
        - Evaluate out.added.append(list(df.fieldname, d.as\_dict())).
    - For each d in old\_value.
      - If d.name does not belong to found\_rows.
        - Evaluate out.removed.append(list(df.fieldname, d.as\_dict())).
  - Otherwise.
    - If old\_value differs from new\_value.
      - If df.fieldtype does not belong to blacklisted\_fields.
        - Set old\_value from old.get\_formatted(df.fieldname) when old\_value, otherwise old\_value.
          - Value choice on old\_value — true gives old.get\_formatted(df.fieldname), false gives old\_value.
        - Set new\_value from new.get\_formatted(df.fieldname) when new\_value, otherwise new\_value.
          - Value choice on new\_value — true gives new.get\_formatted(df.fieldname), false gives new\_value.
      - If old\_value differs from new\_value.
        - Set doctype from (new.doctype or old.doctype).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in new.doctype → old.doctype.
        - If doctype.
          - Set meta from Platform.get\_meta(doctype).
          - If (field\_meta bound to meta.get\_field(df.fieldname) and field\_meta.fieldtype equals “Link”).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in field\_meta bound to meta.get\_field(df.fieldname) → field\_meta.fieldtype equals “Link”.
            - Set link\_meta from Platform.get\_meta(field\_meta.options).
            - If (link\_meta.show\_title\_field\_in\_link and title\_field bound to link\_meta.get\_title\_field() differs from “name”).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in link\_meta.show\_title\_field\_in\_link → title\_field bound to link\_meta.get\_title\_field() differs from “name”.
              - Set tuple(old\_title\_val, new\_title\_val) from tuple(empty text, empty text).
              - Set result from Platform.db.get\_values(field\_meta.options, mapping(“name” → tuple(“in”, tuple(old\_value, new\_value))), list(“name”, title\_field)).
              - For each r in result.
                - If r at 0 equals old\_value.
                  - Set old\_title\_val from r at 1.
                - Otherwise.
                  - If r at 0 equals new\_value.
                    - Set new\_title\_val from r at 1.
              - Evaluate out.changed.append(tuple(df.fieldname, old\_title\_val, new\_title\_val)).
              - Continue with the next iteration or loop test.
        - Evaluate out.changed.append(tuple(df.fieldname, old\_value, new\_value)).
- If not for\_child.
  - For each key in tuple(“name”, “docstatus”).
    - Set old\_value from getattr(old, key).
    - Set new\_value from getattr(new, key).
    - If old\_value differs from new\_value.
      - Evaluate out.changed.append(list(key, old\_value, new\_value)).
- If any(tuple(out.changed, out.added, out.removed, out.row\_changed)).
  - Return out.
- Otherwise.
  - Return no value.

**Values supplied outside this operation** selected callable from getattr(df, “is\_virtual”, false), getattr(d, old\_row\_name\_field, no value) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L872)

<a id="op-1a30de2f33a73f"></a>
### On doctype update

`operation_foundation_core_record_definitions_version_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Version”.

**Local steps**

- Evaluate Platform.db.add\_index(“Version”, list(“ref\_doctype”, “docname”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L2217) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L873)

<a id="op-617ba7cf7a31b5"></a>
### Generate html diff

`operation_foundation_core_record_definitions_version_business_behavior_generate_document_markup_diff`

**Inputs** old\_str, new\_str.

**Declared result** (str bitwise or no value).

**Explicit results** html\_diff.

**Local steps**

- Set old\_lines from old\_str.splitlines(keepends = true).
- Set new\_lines from new\_str.splitlines(keepends = true).
- Set differ from difflib.HtmlDiff(wrapcolumn = 80).
- Set html\_diff from differ.make\_table(old\_lines, new\_lines, fromdesc = Platform.\_(“Original”), todesc = Platform.\_(“New”), context = true, numlines = 3).
- Return html\_diff.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L2295) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L709) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L871)

<a id="op-459767a0e4d1a4"></a>
### Should generate html diff

`operation_foundation_core_record_definitions_version_business_behavior_should_generate_document_markup_diff`

**Inputs** old\_str, new\_str.

**Declared result** bool.

**Explicit results** (old\_str and new\_str and (whitespace '\\n' belongs to old\_str or whitespace '\\n' belongs to new\_str or len(old\_str) &gt; 80 or len(new\_str) &gt; 80)).

**Local steps**

- Return (old\_str and new\_str and (whitespace '\\n' belongs to old\_str or whitespace '\\n' belongs to new\_str or len(old\_str) &gt; 80 or len(new\_str) &gt; 80)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_str → new\_str → (whitespace '\\n' belongs to old\_str or whitespace '\\n' belongs to new\_str or len(old\_str) &gt; 80 or len(new\_str) &gt; 80).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in whitespace '\\n' belongs to old\_str → whitespace '\\n' belongs to new\_str → len(old\_str) &gt; 80 → len(new\_str) &gt; 80.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L2568) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L874)

<a id="op-ddb24a1e01a7cc"></a>
### As string

`operation_foundation_core_record_definitions_version_business_behavior_as_string`

**Inputs** value.

**Declared result** str.

**Explicit results** cstr(value) when value is distinct from no value, otherwise empty text.

**Local steps**

- Return cstr(value) when value is distinct from no value, otherwise empty text.
  - Value choice on value is distinct from no value — true gives cstr(value), false gives empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L2728) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L708) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L870)

## Record · View log

[Record definition](../../../../data/record-types/view_log.json)

<a id="op-1e4b0f80139202"></a>
### View Log.clear old logs

`operation_foundation_core_record_definitions_view_log_business_behavior_view_log_clear_old_logs`

**Inputs** days = 180.

**Wrappers, in declaration order** staticmethod.

**State and service calls** request delete on table.

**Local steps**

- Bind dependencies Interval.
- Bind dependencies Now.
- Set table from Platform.qb.DocType(“View Log”).
- Evaluate Platform.db.delete(table, filters = table.creation &lt; (Now() − Interval(days = days))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L3251) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L897)

## Service · Virtual doctype

<a id="op-a2eced77a4b305"></a>
### Virtual Doctype.get list

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_get_list`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Declared result** list at Platform.\_dict.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6080) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1347)

<a id="op-dd8fdb227dcaf0"></a>
### Virtual Doctype.get count

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_get_count`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Declared result** int.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6131) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1346)

<a id="op-985b5079242fdd"></a>
### Virtual Doctype.get stats

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_get_stats`

**Inputs** remaining named values kwargs.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6172) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1348)

<a id="op-cd1162bf8bb517"></a>
### Virtual Doctype.db insert

`operation_foundation_model_virtual_record_type_business_behavior_virtual_record_type_database_insert`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Declared result** no value.

**Local steps**

- No executable step follows the declaration.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0292.json#L6211) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1343)
