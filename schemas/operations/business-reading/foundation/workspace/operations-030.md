# Forms, reports and navigation · operations 30

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Files

<a id="op-c2c5bcd66ac6d3"></a>
### Walk export folder

`operation_foundation_binding_foundation_studio_files_walk_export_folder`

**Inputs** root.

**Local steps**

- For each tuple(dirpath, dirnames, filenames) in os.walk(root).
  - Set dirnames at slice no value to no value from list of name for name drawn from dirnames where (not name.startswith(“.”) and name does not belong to tuple(“node\_modules”, “\_\_pycache\_\_”)).
    - Draw name from dirnames, keep a combination only if ((not name.startswith(“.”) and name does not belong to tuple(“node\_modules”, “\_\_pycache\_\_”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not name.startswith(“.”) → name does not belong to tuple(“node\_modules”, “\_\_pycache\_\_”).
  - Set folder from os.path.relpath(dirpath, root).replace(os.sep, “/”).
  - yield tuple(dirpath, filenames, empty text when folder equals “.”, otherwise folder).
    - Value choice on folder equals “.” — true gives empty text, false gives folder.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L249) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L56) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L144)

<a id="op-e8d310da5ecebe"></a>
### Discarded export files

`operation_foundation_binding_foundation_studio_files_discarded_export_files`

**Inputs** app.

**Declared result** list at str.

**Explicit results** list() · sorted(discarded).

**Local steps**

- If not app.Platform\_app.
  - Return list().
- Set root from app.get\_folder\_path().
- If not os.path.isdir(root).
  - Return list().
- Set discarded from list().
- For each tuple(\_dirpath, filenames, folder) in walk\_export\_folder(root).
  - For each filename in filenames.
    - Set path from formatted text {folder}/{filename} when folder, otherwise filename.
      - Value choice on folder — true gives formatted text {folder}/{filename}, false gives filename.
    - If (not is\_db\_file\_allowed(app.name, path) and not is\_regenerated\_file(app.name, path)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not is\_db\_file\_allowed(app.name, path) → not is\_regenerated\_file(app.name, path).
      - Evaluate discarded.append(path).
- Return sorted(discarded).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L222) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L29) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L117)

<a id="op-ba3472145d9fb2"></a>
### Is regenerated file

`operation_foundation_binding_foundation_studio_files_is_regenerated_file`

**Inputs** studio\_app, path.

**Declared result** bool.

**Explicit results** true · ((is\_page\_script\_path(path) or is\_component\_script\_path(path)) and path.endswith(“.js”)).

**Local steps**

- Set name from posixpath.basename(path).
- If (name.startswith(“.”) or name equals “tsconfig.json” or is\_export\_doc\_file(studio\_app, path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.startswith(“.”) → name equals “tsconfig.json” → is\_export\_doc\_file(studio\_app, path).
  - Return true.
- Return ((is\_page\_script\_path(path) or is\_component\_script\_path(path)) and path.endswith(“.js”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (is\_page\_script\_path(path) or is\_component\_script\_path(path)) → path.endswith(“.js”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_page\_script\_path(path) → is\_component\_script\_path(path).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L235) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L42) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L130)

<a id="op-8e6964490e1efa"></a>
### Is db file allowed

`operation_foundation_binding_foundation_studio_files_is_db_file_allowed`

**Inputs** studio\_app, path.

**Declared result** bool.

**Explicit results** false · not is\_export\_doc\_file(studio\_app, path).

**Local steps**

- Set name from posixpath.basename(path).
- If (name.startswith(“.”) or name equals “tsconfig.json” or name.lower() belongs to TAILWIND\_CONFIG\_FILES).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.startswith(“.”) → name equals “tsconfig.json” → name.lower() belongs to TAILWIND\_CONFIG\_FILES.
  - Return false.
- If posixpath.splitext(name) at 1.lower() does not belong to ALLOWED\_DB\_FILE\_EXTENSIONS.
  - Return false.
- If (path.startswith(“studio\_page/”) or is\_component\_script\_path(path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in path.startswith(“studio\_page/”) → is\_component\_script\_path(path).
  - Return false.
- Return not is\_export\_doc\_file(studio\_app, path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L231) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L38) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L126)

<a id="op-166912596aefb8"></a>
### Normalize path

`operation_foundation_binding_foundation_studio_files_normalize_path`

**Inputs** file\_path.

**Declared result** str.

**Explicit results** path.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid file path: {0}”.format(file\_path).

**Local steps**

- If not isinstance(file\_path, str).
  - Call the validation error handler Platform.throw(translated “Invalid file path: {0}”.format(file\_path), Platform.PermissionError).
- Set path from file\_path.strip().strip(“/”).
- Set first\_segment from path.split(“/”, 1) at 0.
- If (not path or “\\” belongs to path or first\_segment equals “..” or posixpath.normpath(path) differs from path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not path → “\\” belongs to path → first\_segment equals “..” → posixpath.normpath(path) differs from path.
  - Call the validation error handler Platform.throw(translated “Invalid file path: {0}”.format(file\_path), Platform.PermissionError).
- Return path.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L237) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L44) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L132)

<a id="op-b3f82f38e8f043"></a>
### File hash

`operation_foundation_binding_foundation_studio_files_file_hash`

**Inputs** content.

**Declared result** str.

**Explicit results** hashlib.sha1(content.encode(“utf-8”)).hexdigest().

**Local steps**

- Return hashlib.sha1(content.encode(“utf-8”)).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L224) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L31) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L119)

<a id="op-e86e7c8155b65b"></a>
### Validate allowed extension

`operation_foundation_binding_foundation_studio_files_validate_allowed_extension`

**Inputs** file\_path, allowed = no value.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “A database app cannot hold Vue components. Export the app to a repository to add one.” · validation helper — translated “A database app has no TypeScript compiler. Write JavaScript, or export the app to a repository.” · validation helper — translated “Editing {0} files is not allowed.”.format((extension or “these”)).

**Local steps**

- Set extension from os.path.splitext(file\_path) at 1.lower().
- If extension belongs to (allowed or ALLOWED\_STUDIO\_FILE\_EXTENSIONS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in allowed → ALLOWED\_STUDIO\_FILE\_EXTENSIONS.
  - Return no value.
- If extension equals “.vue”.
  - Call the validation error handler Platform.throw(translated “A database app cannot hold Vue components. Export the app to a repository to add one.”).
- If extension equals “.ts”.
  - Call the validation error handler Platform.throw(translated “A database app has no TypeScript compiler. Write JavaScript, or export the app to a repository.”).
- Call the validation error handler Platform.throw(translated “Editing {0} files is not allowed.”.format((extension or “these”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extension → “these”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L245) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L52) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L140)

<a id="op-9c83c3fcd4826f"></a>
### Validate folder names

`operation_foundation_binding_foundation_studio_files_validate_folder_names`

**Inputs** file\_path.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} is a folder, so its name cannot end with {1}.”.format(folder, extension).

**Local steps**

- For each folder in posixpath.dirname(file\_path).split(“/”).
  - Set extension from posixpath.splitext(folder) at 1.lower().
  - If extension belongs to ALLOWED\_STUDIO\_FILE\_EXTENSIONS.
    - Call the validation error handler Platform.throw(translated “{0} is a folder, so its name cannot end with {1}.”.format(folder, extension)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L247) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L54) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L142)

<a id="op-042091eb3692b1"></a>
### Is export doc file

`operation_foundation_binding_foundation_studio_files_is_export_doc_file`

**Inputs** studio\_app, file\_path.

**Declared result** bool.

**Explicit results** false · (normalized.startswith(“studio\_page/”) or normalized.startswith(“studio\_components/”) or normalized equals formatted text {Platform.scrub(studio\_app)}.json).

**Local steps**

- Set normalized from file\_path.strip(“/”).
- If not normalized.lower().endswith(“.json”).
  - Return false.
- Return (normalized.startswith(“studio\_page/”) or normalized.startswith(“studio\_components/”) or normalized equals formatted text {Platform.scrub(studio\_app)}.json).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in normalized.startswith(“studio\_page/”) → normalized.startswith(“studio\_components/”) → normalized equals formatted text {Platform.scrub(studio\_app)}.json.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L232) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L39) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L127)

<a id="op-70b348fff76822"></a>
### Is export folder

`operation_foundation_binding_foundation_studio_files_is_export_folder`

**Inputs** file\_path.

**Declared result** bool.

**Explicit results** (normalized belongs to tuple(“studio\_page”, “studio\_components”) or bool(re.fullmatch(“studio\_page/&#91;^/&#93;+”, normalized))).

**Local steps**

- Set normalized from file\_path.strip(“/”).
- Return (normalized belongs to tuple(“studio\_page”, “studio\_components”) or bool(re.fullmatch(“studio\_page/&#91;^/&#93;+”, normalized))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in normalized belongs to tuple(“studio\_page”, “studio\_components”) → bool(re.fullmatch(“studio\_page/&#91;^/&#93;+”, normalized)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L233) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L40) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L128)

<a id="op-01e8bd28907f73"></a>
### Validate editable

`operation_foundation_binding_foundation_studio_files_validate_editable`

**Inputs** studio\_app, file\_path.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} is generated by Studio and is read-only.”.format(file\_path) · validation helper — translated “{0} runs at build time; edit it in the repository.”.format(file\_path).

**Local steps**

- If is\_export\_doc\_file(studio\_app, file\_path).
  - Call the validation error handler Platform.throw(translated “{0} is generated by Studio and is read-only.”.format(file\_path)).
- If os.path.basename(file\_path).lower() belongs to TAILWIND\_CONFIG\_FILES.
  - Call the validation error handler Platform.throw(translated “{0} runs at build time; edit it in the repository.”.format(file\_path)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L246) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L53) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L141)

<a id="op-07598cff245772"></a>
### Validate folder removable

`operation_foundation_binding_foundation_studio_files_validate_folder_removable`

**Inputs** file\_path.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “{0} is managed by Studio and can't be removed or renamed.”.format(file\_path).

**Local steps**

- If is\_export\_folder(file\_path).
  - Call the validation error handler Platform.throw(translated “{0} is managed by Studio and can't be removed or renamed.”.format(file\_path)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L248) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L55) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L143)

## Record · Form tour

[Record definition](../../../../data/record-types/form_tour.json)

<a id="op-f750cd8cff07ec"></a>
### Form Tour.before save

`operation_foundation_desk_record_definitions_form_tour_business_behavior_form_tour_before_save`

**Inputs** self.

**Record and data access** read “Workspace” via get\_value · read “Dashboard” via get\_value · read “DocType” via get\_value.

**Local steps**

- If (self.is\_standard and not self.module).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_standard → not self.module.
  - If self.workspace\_name.
    - Set self.module from Platform.db.get\_value(“Workspace”, self.workspace\_name, “module”).
  - Otherwise.
    - If self.dashboard\_name.
      - Set dashboard\_doctype from Platform.db.get\_value(“Dashboard”, self.dashboard\_name, “module”).
      - Set self.module from Platform.db.get\_value(“DocType”, dashboard\_doctype, “module”).
    - Otherwise.
      - Set self.module from “Desk”.
- If not self.ui\_tour.
  - Set meta from Platform.get\_meta(self.reference\_doctype).
  - For each step in self.steps.
    - If (step.is\_table\_field and step.parent\_fieldname).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in step.is\_table\_field → step.parent\_fieldname.
      - Set parent\_field\_df from meta.get\_field(step.parent\_fieldname).
      - Set step.child\_doctype from parent\_field\_df.options.
      - Set field\_df from Platform.get\_meta(step.child\_doctype).get\_field(step.fieldname).
      - Set step.label from field\_df.label.
      - Set step.fieldtype from field\_df.fieldtype.
    - Otherwise.
      - Set field\_df from meta.get\_field(step.fieldname).
      - Set step.label from field\_df.label.
      - Set step.fieldtype from field\_df.fieldtype.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L1346) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L778)

<a id="op-1861e5e0391597"></a>
### Form Tour.on update

`operation_foundation_desk_record_definitions_form_tour_business_behavior_form_tour_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_key(“bootinfo”).
- If (Platform.conf.developer\_mode and self.is\_standard).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.is\_standard.
  - Evaluate export\_to\_files(list(list(“Form Tour”, self.name)), self.module).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L1946) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L780)

<a id="op-e8d06c28b1e795"></a>
### Form Tour.on trash

`operation_foundation_desk_record_definitions_form_tour_business_behavior_form_tour_on_trash`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L2091) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L779)

<a id="op-478e0633aaade9"></a>
### Reset tour

`operation_foundation_desk_record_definitions_form_tour_business_behavior_reset_tour`

**Inputs** tour\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “User” via get\_all · read “User” via get\_value.

**State and service calls** request set\_value on “User” · msgprint with translated “Successfully reset onboarding status for all users.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- For each user in Platform.get\_all(“User”, pluck = “name”).
  - Set onboarding\_status from Platform.parse\_json(Platform.db.get\_value(“User”, user, “onboarding\_status”)).
  - Evaluate onboarding\_status.pop(tour\_name, no value).
  - Evaluate Platform.db.set\_value(“User”, user, “onboarding\_status”, Platform.as\_json(onboarding\_status), update\_modified = false).
  - Evaluate Platform.cache.hdel(“bootinfo”, user).
- Evaluate Platform.msgprint(translated “Successfully reset onboarding status for all users.”, alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L2149) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L782)

<a id="op-48e597867d13d4"></a>
### Update user status

`operation_foundation_desk_record_definitions_form_tour_business_behavior_update_user_status`

**Inputs** value, step.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “User”.

**Local steps**

- Bind dependencies capture.
- Set step from Platform.parse\_json(step).
- Set tour from Platform.parse\_json(value).
- Evaluate capture(Platform.scrub(formatted text {step.parent}\_{step.title}), app = “Platform\_ui\_tours”, properties = mapping(“is\_completed” → tour.is\_completed)).
- Evaluate Platform.db.set\_value(“User”, Platform.session.user, “onboarding\_status”, value, update\_modified = false).
- Evaluate Platform.cache.hdel(“bootinfo”, Platform.session.user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L2533) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L783)

<a id="op-aec4f30067b3a7"></a>
### Get onboarding ui tours

`operation_foundation_desk_record_definitions_form_tour_business_behavior_get_onboarding_user_interface_tours`

**Inputs** no declared parameters.

**Record and data access** read “Form Tour” via get\_all.

**Explicit results** list() · list of list(tour.name, json.loads(tour.page\_route)) for tour drawn from ui\_tours.

**Local steps**

- If not Platform.get\_system\_settings(“enable\_onboarding”).
  - Return list().
- Set ui\_tours from Platform.get\_all(“Form Tour”, filters = mapping(“ui\_tour” → 1), fields = list(“page\_route”, “name”)).
- Return list of list(tour.name, json.loads(tour.page\_route)) for tour drawn from ui\_tours.
  - Draw tour from ui\_tours.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_onboarding”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L2887) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L781)

## Service · Full text search

<a id="op-3c8afdeff968c2"></a>
### Full Text Search.initialize

`operation_foundation_search_full_text_search_business_behavior_full_text_search_initialize`

**Inputs** self, index\_name.

**Local steps**

- Set self.index\_name from index\_name.
- Set self.index\_path from get\_index\_path(index\_name).
- Set self.schema from self.get\_schema().
- Set self.id from self.get\_id().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get schema](operations-030.md#op-dce891e447a484), [get id](operations-030.md#op-215d03d44ced8d).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L2660) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L443)

<a id="op-dce891e447a484"></a>
### Full Text Search.get schema

`operation_foundation_search_full_text_search_business_behavior_full_text_search_get_schema`

**Inputs** self.

**Explicit results** Schema(name = ID(stored = true), content = TEXT(stored = true)).

**Local steps**

- Return Schema(name = ID(stored = true), content = TEXT(stored = true)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L2806) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L442)

<a id="op-ffe770a42efb49"></a>
### Full Text Search.get fields to search

`operation_foundation_search_full_text_search_business_behavior_full_text_search_get_fields_to_search`

**Inputs** self.

**Explicit results** list(“name”, “content”).

**Local steps**

- Return list(“name”, “content”).

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L2904) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L438)

<a id="op-215d03d44ced8d"></a>
### Full Text Search.get id

`operation_foundation_search_full_text_search_business_behavior_full_text_search_get_identifier`

**Inputs** self.

**Explicit results** “name”.

**Local steps**

- Return “name”.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L2960) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1762) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L439)

<a id="op-1e9878cf310b6f"></a>
### Full Text Search.get items to index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_get_items_to_index`

**Inputs** self.

**Explicit results** list().

**Local steps**

- Return list().

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3002) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L441)

<a id="op-e9e50b757039fa"></a>
### Full Text Search.get document to index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_get_document_to_index`

**Inputs** self.

**Explicit results** mapping().

**Local steps**

- Return mapping().

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3039) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L437)
