# Forms, reports and navigation · operations 33

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Introspect

<a id="op-151903180bbcc4"></a>
### Run get whitelisted methods

`operation_foundation_binding_foundation_studio_ai_agent_tools_introspect_run_get_whitelisted_methods`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** ctx, args.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L120) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1783)

## Record · Kanban board

[Record definition](../../../../data/record-types/kanban_board.json)

<a id="op-e86980bd40e70a"></a>
### Kanban Board.validate

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_kanban_board_validate`

**Inputs** self.

**Local steps**

- If (self.is\_standard equals “Yes” or self.\_was\_standard()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_standard equals “Yes” → self.\_was\_standard().
  - Evaluate self.validate\_standard().
- Evaluate self.validate\_column\_name().

If control reaches the end, it returns no value.

**Methods declared on this owner** [was standard](operations-033.md#op-33ef92d748e212), [validate standard](operations-033.md#op-e91d67bcc42e1c), [validate column name](operations-033.md#op-7c7eb27a42d24d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L11) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L355) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L813)

<a id="op-e91d67bcc42e1c"></a>
### Kanban Board.validate standard

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_validate_standard`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Standard Kanban Boards can only be changed in developer mode” · validation helper — translated “Only a new Kanban Board can be made standard” · validation helper with Platform.MandatoryError — translated “Module is required for a standard Kanban Board” · validation helper — translated “A standard Kanban Board cannot be private” · validation helper — translated “A standard Kanban Board must use Kanban v2”.

**Local steps**

- If (not Platform.conf.developer\_mode and not Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.developer\_mode → not Platform.flags.in\_migrate.
  - Call the validation error handler Platform.throw(translated “Standard Kanban Boards can only be changed in developer mode”, Platform.PermissionError).
- If self.is\_standard differs from “Yes”.
  - Return no value.
- If (not self.is\_new() and not self.\_was\_standard()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → not self.\_was\_standard().
  - Call the validation error handler Platform.throw(translated “Only a new Kanban Board can be made standard”).
- If not self.module.
  - Call the validation error handler Platform.throw(translated “Module is required for a standard Kanban Board”, Platform.MandatoryError).
- If self.private.
  - Call the validation error handler Platform.throw(translated “A standard Kanban Board cannot be private”).
- If not self.use\_kanban\_v2.
  - Call the validation error handler Platform.throw(translated “A standard Kanban Board must use Kanban v2”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [was standard](operations-033.md#op-33ef92d748e212).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L250) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L708)

<a id="op-33ef92d748e212"></a>
### Kanban Board.was standard

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_was_standard`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool((before and before.is\_standard equals “Yes”)).

**Local steps**

- Set before from self.get\_doc\_before\_save().
- Return bool((before and before.is\_standard equals “Yes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in before → before.is\_standard equals “Yes”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L251) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L709)

<a id="op-e8d286a50dd5f4"></a>
### Kanban Board.on change

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_kanban_board_on_change`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.reference\_doctype).
- Evaluate clear\_user\_settings\_cache(self.reference\_doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L6924) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L354) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L812)

<a id="op-6a63d1795e791f"></a>
### Kanban Board.on update

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_on_update`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not Platform.conf.developer\_mode or Platform.flags.in\_import).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.conf.developer\_mode → Platform.flags.in\_import.
  - Return no value.
- If self.is\_standard equals “Yes”.
  - Evaluate self.export\_board().
- Otherwise.
  - If self.\_was\_standard().
    - Evaluate self.get\_doc\_before\_save().remove\_export().

If control reaches the end, it returns no value.

**Methods declared on this owner** [export board](operations-033.md#op-7abc4f0486daee), [was standard](operations-033.md#op-33ef92d748e212).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L243) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L701)

<a id="op-416271fbab52c9"></a>
### Kanban Board.on trash

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_on_trash`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Standard Kanban Boards can only be deleted in developer mode”.

**Local steps**

- If (Platform.flags.in\_migrate or self.is\_standard differs from “Yes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_migrate → self.is\_standard differs from “Yes”.
  - Return no value.
- If not Platform.conf.developer\_mode.
  - Call the validation error handler Platform.throw(translated “Standard Kanban Boards can only be deleted in developer mode”, Platform.PermissionError).
- Evaluate self.remove\_export().

If control reaches the end, it returns no value.

**Methods declared on this owner** [remove export](operations-033.md#op-53addbefa68461).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L242) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L700)

<a id="op-53addbefa68461"></a>
### Kanban Board.remove export

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_remove_export`

**Inputs** self.

**Local steps**

- Set path from self.get\_export\_path().
- If os.path.exists(path).
  - Evaluate os.remove(path).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export path](operations-033.md#op-eca5d633b85bb5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L244) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L702)

<a id="op-c21895f423fa40"></a>
### Kanban Board.before rename

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_before_rename`

**Inputs** self, old, new, merge = false.

**Explicit failure paths** validation helper — translated “A standard Kanban Board cannot be renamed”.

**Local steps**

- If self.is\_standard equals “Yes”.
  - Call the validation error handler Platform.throw(translated “A standard Kanban Board cannot be renamed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L239) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L697)

<a id="op-eca5d633b85bb5"></a>
### Kanban Board.get export path

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_get_export_path`

**Inputs** self.

**Declared result** str.

**Explicit results** os.path.join(get\_module\_path(self.module), “doctype”, Platform.scrub(self.reference\_doctype), “kanban\_board”, …).

**Local steps**

- Return os.path.join(get\_module\_path(self.module), “doctype”, Platform.scrub(self.reference\_doctype), “kanban\_board”, …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L241) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L699)

<a id="op-7abc4f0486daee"></a>
### Kanban Board.export board

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_export_board`

**Inputs** self.

**Local steps**

- Set path from self.get\_export\_path().
- Evaluate Platform.create\_folder(os.path.dirname(path)).
- Within open(path, “w+”) bound as f.
  - Evaluate f.write((Platform.as\_json(self.as\_dict(no\_nulls = true, no\_private\_properties = true)) + whitespace '\\n')).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get export path](operations-033.md#op-eca5d633b85bb5).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L240) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L698)

<a id="op-d7cf7cd1bf70b0"></a>
### Kanban Board.before insert

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_kanban_board_before_insert`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_import.
  - Return no value.
- Set self.use\_kanban\_v2 from 1.
- Evaluate self.seed\_title\_and\_image\_fields().
- Evaluate self.seed\_card\_fields().
- Evaluate self.seed\_preview\_fields().
- Evaluate self.seed\_group\_by\_fields().

If control reaches the end, it returns no value.

**Methods declared on this owner** [seed title and image fields](operations-033.md#op-0fd37b6a1ebe1b), [seed card fields](operations-033.md#op-0fdea4a5d0d59b), [seed preview fields](operations-033.md#op-1e3e14fe986b27), [seed group by fields](operations-033.md#op-1ae5f8d30f5158).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L10) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L353) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L811)

<a id="op-0fd37b6a1ebe1b"></a>
### Kanban Board.seed title and image fields

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_seed_title_and_image_fields`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.reference\_doctype.
  - Return no value.
- If not self.title\_field.
  - Set self.title\_field from default\_title\_field(self.reference\_doctype).
- If not self.image\_field.
  - Set self.image\_field from default\_image\_field(self.reference\_doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L249) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L707)

<a id="op-0fdea4a5d0d59b"></a>
### Kanban Board.seed card fields

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_seed_card_fields`

**Inputs** self.

**Local steps**

- Evaluate self.\_seed\_field\_table(“card\_fields”, default\_card\_fieldnames(self.reference\_doctype)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [seed field table](operations-033.md#op-041ca6d255abaa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L245) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L703)

<a id="op-1e3e14fe986b27"></a>
### Kanban Board.seed preview fields

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_seed_preview_fields`

**Inputs** self.

**Local steps**

- Evaluate self.\_seed\_field\_table(“preview\_fields”, default\_preview\_fieldnames(self.reference\_doctype)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [seed field table](operations-033.md#op-041ca6d255abaa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L248) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L706)

<a id="op-1ae5f8d30f5158"></a>
### Kanban Board.seed group by fields

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_seed_group_by_fields`

**Inputs** self.

**Local steps**

- Evaluate self.\_seed\_field\_table(“group\_by\_fields”, default\_group\_by\_fieldnames(self.reference\_doctype)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [seed field table](operations-033.md#op-041ca6d255abaa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L247) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L705)

<a id="op-041ca6d255abaa"></a>
### Kanban Board.seed field table

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_kanbanboard_seed_field_table`

**Inputs** self, tablefield, fieldnames.

**Explicit results** no value.

**Local steps**

- If (self.get(tablefield) or not self.reference\_doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(tablefield) → not self.reference\_doctype.
  - Return no value.
- Set meta from Platform.get\_meta(self.reference\_doctype).
- Set skip from set(self.field\_name, self.title\_field, self.image\_field).
- For each fieldname in fieldnames.
  - If fieldname belongs to skip.
    - Continue with the next iteration or loop test.
  - Set df from meta.get\_field(fieldname).
  - Evaluate self.append(tablefield, mapping(“fieldname” → fieldname, “label” → df.label when df, otherwise fieldname)).
    - Value choice on df — true gives df.label, false gives fieldname.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L246) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L704)

<a id="op-7c7eb27a42d24d"></a>
### Kanban Board.validate column name

`operation_foundation_desk_record_definitions_kanban_board_business_behavior_kanban_board_validate_column_name`

**Inputs** self.

**State and service calls** msgprint with translated “Column Name cannot be empty”.

**Local steps**

- For each column in self.columns.
  - If not column.column\_name.
    - Evaluate Platform.msgprint(translated “Column Name cannot be empty”, raise\_exception = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L7102) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L356) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L814)

<a id="op-6d0f6cebb10551"></a>
### Default title field

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_title_field`

**Inputs** doctype.

**Declared result** str.

**Explicit results** title · df.fieldname · “name”.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set title from meta.get(“title\_field”).
- If title.
  - Set df from meta.get\_field(title).
  - If (df and df.fieldtype belongs to TITLE\_FIELDTYPES).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.fieldtype belongs to TITLE\_FIELDTYPES.
    - Return title.
- For each df in meta.fields.
  - If (df.fieldtype belongs to TITLE\_FIELDTYPES and df.fieldname and not df.hidden).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype belongs to TITLE\_FIELDTYPES → df.fieldname → not df.hidden.
    - Return df.fieldname.
- Return “name”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L236) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L694)

<a id="op-6af068c35a2b9b"></a>
### Default image field

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_image_field`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Explicit results** meta.image\_field · images at 0.fieldname when images, otherwise no value.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If meta.image\_field.
  - Return meta.image\_field.
- Set images from meta.get\_image\_fields().
- Return images at 0.fieldname when images, otherwise no value.
  - Value choice on images — true gives images at 0.fieldname, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L233) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L691)

<a id="op-474f7fd84527c1"></a>
### Default card fieldnames

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_card_fieldnames`

**Inputs** doctype.

**Declared result** list at str.

**Explicit results** fieldnames at slice no value to 6.

**Local steps**

- Bind dependencies no\_value\_fields, table\_fields.
- Set meta from Platform.get\_meta(doctype).
- Bind local operation usable for subsequent calls.
- Set fieldnames from list of df.fieldname for df drawn from meta.fields where (df.in\_list\_view and usable(df)).
  - Draw df from meta.fields, keep a combination only if ((df.in\_list\_view and usable(df))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.in\_list\_view → usable(df).
- If not fieldnames.
  - Set fieldnames from list of df.fieldname for df drawn from meta.fields where (df.reqd and usable(df)).
    - Draw df from meta.fields, keep a combination only if ((df.reqd and usable(df))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.reqd → usable(df).
- Return fieldnames at slice no value to 6.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L230) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L688)

<a id="op-5075555f8c6e23"></a>
### Default card fieldnames.usable

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_card_fieldnames_usable`

**Inputs** df.

**Explicit results** (df.fieldtype does not belong to no\_value\_fields and df.fieldtype does not belong to table\_fields and df.fieldtype differs from “Check” and not df.hidden).

**Local steps**

- Return (df.fieldtype does not belong to no\_value\_fields and df.fieldtype does not belong to table\_fields and df.fieldtype differs from “Check” and not df.hidden).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → df.fieldtype does not belong to table\_fields → df.fieldtype differs from “Check” → not df.hidden.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L231) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L689)

<a id="op-a8a82fba641697"></a>
### Default preview fieldnames

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_preview_fieldnames`

**Inputs** doctype.

**Declared result** list at str.

**Explicit results** fieldnames at slice no value to 6.

**Local steps**

- Bind dependencies no\_value\_fields, table\_fields.
- Set meta from Platform.get\_meta(doctype).
- Set skip from set(meta.get\_title\_field(), meta.image\_field, “name”).
- Bind local operation usable for subsequent calls.
- Set fieldnames from list of df.fieldname for df drawn from meta.fields where (df.in\_preview and usable(df)).
  - Draw df from meta.fields, keep a combination only if ((df.in\_preview and usable(df))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.in\_preview → usable(df).
- If not fieldnames.
  - Set fieldnames from list of df.fieldname for df drawn from meta.fields where (df.reqd and usable(df)).
    - Draw df from meta.fields, keep a combination only if ((df.reqd and usable(df))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.reqd → usable(df).
- Return fieldnames at slice no value to 6.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L234) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L692)

<a id="op-706a08506d506f"></a>
### Default preview fieldnames.usable

`operation_foundation_binding_foundation_desk_doctype_kanban_board_kanban_board_default_preview_fieldnames_usable`

**Inputs** df.

**Explicit results** (df.fieldtype does not belong to no\_value\_fields and df.fieldtype does not belong to table\_fields and df.fieldtype differs from “Check” and not df.hidden and df.fieldname does not belong to skip).

**Local steps**

- Return (df.fieldtype does not belong to no\_value\_fields and df.fieldtype does not belong to table\_fields and df.fieldtype differs from “Check” and not df.hidden and df.fieldname does not belong to skip).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to no\_value\_fields → df.fieldtype does not belong to table\_fields → df.fieldtype differs from “Check” → not df.hidden → df.fieldname does not belong to skip.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L235) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L693)
