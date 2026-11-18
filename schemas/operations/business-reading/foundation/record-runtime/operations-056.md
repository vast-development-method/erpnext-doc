# Record lifecycle and persistence · operations 56

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · File

[Record definition](../../../../data/record-types/file.json)

<a id="op-9e1a7dfe46a3c7"></a>
### Get safe file name

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_safe_file_name`

**Inputs** file\_name.

**Declared result** str.

**Explicit results** re.sub(“&#91;/\\\\%?#&#93;”, “\_”, file\_name).

**Local steps**

- Return re.sub(“&#91;/\\\\%?#&#93;”, “\_”, file\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L2735) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1615)

<a id="op-7a74e827eff4a9"></a>
### Check path safety

`operation_foundation_core_record_definitions_file_utils_business_behavior_check_path_safety`

**Inputs** base\_path, requested\_path.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set base\_path from os.path.realpath(base\_path).
- Set requested\_path from os.path.realpath(requested\_path).
- If os.path.commonpath(list(base\_path, requested\_path)) differs from base\_path.
  - Evaluate Platform.log\_error(title = “Attempted Unauthorized File Access”, message = formatted text Blocked access to: {requested\_path}).
  - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L2804) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1601)

## Service · File

<a id="op-fd8569c55afce0"></a>
### Unzip file

`operation_foundation_core_application_interface_file_business_behavior_unzip_file`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** file.unzip().

**Local steps**

- Set file from Platform.get\_doc(“File”, name).
- Return file.unzip().

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0036.json#L6560) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L904)

<a id="op-c6feeead31818b"></a>
### Get attached images

`operation_foundation_core_application_interface_file_business_behavior_get_attached_images`

**Inputs** doctype, names.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** Platform.\_dict.

**Record and data access** read “File” via get\_list.

**Explicit results** out.

**Local steps**

- If isinstance(names, str).
  - Set names from json.loads(names).
- Set img\_urls from Platform.db.get\_list(“File”, filters = mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → tuple(“in”, names), “is\_folder” → 0), fields = list(“file\_url”, “attached\_to\_name as docname”)).
- Set out from Platform.\_dict().
- For each i in img\_urls.
  - Set out at i.docname from out.get(i.docname, list()).
  - Evaluate out at i.docname.append(i.file\_url).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L156) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L897)

<a id="op-e87f0760d582f7"></a>
### Get files in folder

`operation_foundation_core_application_interface_file_business_behavior_get_files_in_folder`

**Inputs** folder, start = 0, page\_length = 20.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Record and data access** read “File” via get\_value · read “File” via get\_list.

**State and service calls** call insert on files.

**Explicit results** mapping(“files” → files at slice no value to page\_length, “has\_more” → len(files) &gt; page\_length).

**Local steps**

- Set attachment\_folder from Platform.db.get\_value(“File”, “Home/Attachments”, list(“name”, “file\_name”, “file\_url”, “is\_folder”, …), as\_dict = 1).
- Set files from Platform.get\_list(“File”, mapping(“folder” → folder), list(“name”, “file\_name”, “file\_url”, “is\_folder”, …), start = start, page\_length = (page\_length + 1)).
- If (folder equals “Home” and attachment\_folder does not belong to files).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in folder equals “Home” → attachment\_folder does not belong to files.
  - Evaluate files.insert(0, attachment\_folder).
- Return mapping(“files” → files at slice no value to page\_length, “has\_more” → len(files) &gt; page\_length).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L831) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L900)

<a id="op-f31fc755771efc"></a>
### Get files by search text

`operation_foundation_core_application_interface_file_business_behavior_get_files_by_search_text`

**Inputs** text.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “File” via get\_list.

**Explicit results** list() · Platform.get\_list(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_folder”, …), filters = mapping(“is\_folder” → false), or\_filters = mapping(“file\_name” → tuple(“like”, text), “file\_url” → text,  ….

**Local steps**

- If not text.
  - Return list().
- Set text from ((“%” + cstr(text).lower()) + “%”).
- Return Platform.get\_list(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_folder”, …), filters = mapping(“is\_folder” → false), or\_filters = mapping(“file\_name” → tuple(“like”, text), “file\_url” → text,  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L472) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L830) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L899)

<a id="op-fc04311b3357da"></a>
### Get max file size

`operation_foundation_core_application_interface_file_business_behavior_get_maximum_file_size`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Declared result** int.

**Explicit results** (((cint(Platform.get\_system\_settings(“max\_file\_size”)) × 1024) × 1024) or cint(Platform.conf.get(“max\_file\_size”)) or ((25 × 1024) × 1024)).

**Local steps**

- Return (((cint(Platform.get\_system\_settings(“max\_file\_size”)) × 1024) × 1024) or cint(Platform.conf.get(“max\_file\_size”)) or ((25 × 1024) × 1024)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ((cint(Platform.get\_system\_settings(“max\_file\_size”)) × 1024) × 1024) → cint(Platform.conf.get(“max\_file\_size”)) → ((25 × 1024) × 1024).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“max\_file\_size”).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L820) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L902)

<a id="op-2c47d33a32748f"></a>
### Get max extract size

`operation_foundation_core_application_interface_file_business_behavior_get_maximum_extract_size`

**Inputs** no declared parameters.

**Declared result** int.

**Explicit results** (((cint(Platform.get\_system\_settings(“max\_zip\_extract\_size”)) × 1024) × 1024) or cint(Platform.conf.get(“max\_zip\_extract\_size”)) or ((25 × 1024) × 1024)).

**Local steps**

- Return (((cint(Platform.get\_system\_settings(“max\_zip\_extract\_size”)) × 1024) × 1024) or cint(Platform.conf.get(“max\_zip\_extract\_size”)) or ((25 × 1024) × 1024)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ((cint(Platform.get\_system\_settings(“max\_zip\_extract\_size”)) × 1024) × 1024) → cint(Platform.conf.get(“max\_zip\_extract\_size”)) → ((25 × 1024) × 1024).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“max\_zip\_extract\_size”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L1001) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L901)

<a id="op-ee915e6db965e6"></a>
### Get max extract members

`operation_foundation_binding_foundation_core_api_file_get_max_extract_members`

**Inputs** no declared parameters.

**Declared result** int.

**Explicit results** (cint(Platform.conf.get(“max\_zip\_extract\_members”)) or 1000).

**Local steps**

- Return (cint(Platform.conf.get(“max\_zip\_extract\_members”)) or 1000).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.get(“max\_zip\_extract\_members”)) → 1000.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L121) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L579)

<a id="op-cb73c67939b1b3"></a>
### Get file chunk size

`operation_foundation_core_application_interface_file_business_behavior_get_file_chunk_size`

**Inputs** no declared parameters.

**Declared result** int.

**Explicit results** (cint(Platform.conf.get(“file\_chunk\_size”)) or ((25 × 1024) × 1024)).

**Local steps**

- Return (cint(Platform.conf.get(“file\_chunk\_size”)) or ((25 × 1024) × 1024)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.conf.get(“file\_chunk\_size”)) → ((25 × 1024) × 1024).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L1153) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L898)

<a id="op-1851fe9c4efbd1"></a>
### Create new folder

`operation_foundation_core_application_interface_file_business_behavior_create_new_folder`

**Inputs** file\_name, folder.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** File.

**State and service calls** request new\_doc for “File” · call insert on file.

**Explicit results** file.

**Local steps**

- Set file from Platform.new\_doc(“File”).
- Set file.file\_name from file\_name.
- Set file.is\_folder from 1.
- Set file.folder from folder.
- Evaluate file.insert(ignore\_if\_duplicate = true).
- Return file.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L1246) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L896)

<a id="op-d8c156e49e44b3"></a>
### Move file

`operation_foundation_core_application_interface_file_business_behavior_move_file`

**Inputs** file\_list, new\_parent, old\_parent.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Record and data access** resolve a document from “File” via get\_doc.

**State and service calls** call save on Platform.get\_doc(“File”, old\_parent) · call save on Platform.get\_doc(“File”, new\_parent).

**Local steps**

- If isinstance(file\_list, str).
  - Set file\_list from json.loads(file\_list).
- For each file\_obj in file\_list.
  - Evaluate setup\_folder\_path(file\_obj.get(“name”), new\_parent).
- Evaluate Platform.get\_doc(“File”, old\_parent).save().
- Evaluate Platform.get\_doc(“File”, new\_parent).save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L157) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L903)

<a id="op-2eb43dbf98f7a9"></a>
### Zip files

`operation_foundation_core_application_interface_file_business_behavior_zip_files`

**Inputs** files.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Set files from Platform.parse\_json(files).
- Set Platform.response at “filename” from “files.zip”.
- Set Platform.response at “filecontent” from File.zip\_files(files).
- Set Platform.response at “type” from “download”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0037.json#L1718) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L905)

## Service · Filter

<a id="op-a5635846294c01"></a>
### Sentinel.bool

`operation_foundation_types_filter_business_behavior_sentinel_boolean`

**Inputs** self.

**Declared result** bool.

**Explicit results** false.

**Local steps**

- Return false.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L7066) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1441)

<a id="op-4650ec82af7fcd"></a>
### Sentinel.str

`operation_foundation_types_filter_business_behavior_sentinel_text`

**Inputs** self.

**Wrappers, in declaration order** override.

**Declared result** str.

**Explicit results** “UNSPECIFIED”.

**Local steps**

- Return “UNSPECIFIED”.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L7105) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L814) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1442)

<a id="op-a51609f038d1dd"></a>
### Is unspecified

`operation_foundation_types_filter_business_behavior_is_unspecified`

**Inputs** value.

**Declared result** TypeGuard at Sentinel.

**Explicit results** value is identical to UNSPECIFIED.

**Local steps**

- Return value is identical to UNSPECIFIED.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L7149) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1440)

<a id="op-629948ae196354"></a>
### Type narrow

`operation_foundation_types_filter_business_behavior_type_narrow`

**Inputs** v.

**Declared result** \_Value.

**Explicit results** int(v) · v.

**Explicit failure paths** ValueError(formatted text Value must be one of types: {“, ”.join(generator of str(t.\_\_name\_\_) for t drawn from \_InputValue.\_\_args\_\_)}; found {type(v)}).

**Local steps**

- If isinstance(v, bool).
  - Return int(v).
- Otherwise.
  - If isinstance(v, \_Value).
    - Return v.
  - Otherwise.
    - Raise ValueError(formatted text Value must be one of types: {“, ”.join(generator of str(t.\_\_name\_\_) for t drawn from \_InputValue.\_\_args\_\_)}; found {type(v)}).
      - Draw t from \_InputValue.\_\_args\_\_.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0457.json#L7225) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1443)

<a id="op-01b3658e13dba3"></a>
### Filter Tuple.new

`operation_foundation_types_filter_business_behavior_filter_tuple_new`

**Inputs** cls (positional only), s (positional only) = no value, doctype (named only, default UNSPECIFIED), fieldname (named only, default UNSPECIFIED), operator (named only, default “=”), value (named only, default UNSPECIFIED).

**Declared result** Self.

**Explicit results** super().\_\_new\_\_(cls, doctype = doctype, fieldname = fieldname, operator = operator, value = \_value).

**Explicit failure paths** ValueError(formatted text Invalid sequence length: {len(s)}. Expected 2, 3, or 4 elements.) · ValueError(“doctype is required”) · ValueError(“fieldname is required”) · ValueError(“value is required; can be None”) · ValueError(error\_context).

**Local steps**

- Attempt the following.
  - If isinstance(s, Sequence).
    - If len(s) equals 2.
      - Set tuple(fieldname, value) from s.
    - Otherwise.
      - If len(s) equals 3.
        - Set tuple(fieldname, operator, value) from s.
      - Otherwise.
        - If len(s) equals 4.
          - Set tuple(doctype, fieldname, operator, value) from s.
        - Otherwise.
          - If len(s) equals 5.
            - Bind dependencies deprecation\_warning.
            - Evaluate record a compatibility advisory for the invoked interface.
            - Set tuple(doctype, fieldname, operator, value, …) from s.
          - Otherwise.
            - Raise ValueError(formatted text Invalid sequence length: {len(s)}. Expected 2, 3, or 4 elements.).
  - If (is\_unspecified(doctype) or doctype is identical to no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_unspecified(doctype) → doctype is identical to no value.
    - Raise ValueError(“doctype is required”).
  - If (is\_unspecified(fieldname) or fieldname is identical to no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_unspecified(fieldname) → fieldname is identical to no value.
    - Raise ValueError(“fieldname is required”).
  - If is\_unspecified(value).
    - Raise ValueError(“value is required; can be None”).
  - If (operator belongs to tuple(“in”, “not in”) and isinstance(value, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in operator belongs to tuple(“in”, “not in”) → isinstance(value, str).
    - Attempt the following.
      - Set parsed from json.loads(value).
      - Set value from parsed when isinstance(parsed, list), otherwise value.split(“,”).
        - Value choice on isinstance(parsed, list) — true gives parsed, false gives value.split(“,”).
    - On failure (ValueError).
      - Set value from value.split(“,”).
  - If isinstance(value, \_InputValue).
    - Set \_value from \_type\_narrow(value).
  - Otherwise.
    - Set \_value from tuple(generator of \_type\_narrow(v) for v drawn from value).
      - Draw v from value.
  - Return super().\_\_new\_\_(cls, doctype = doctype, fieldname = fieldname, operator = operator, value = \_value).
- On failure (Exception) bound to e.
  - Set error\_context from formatted text Error creating FilterTuple: Input: {s}, doctype={doctype}, fieldname={fieldname}, operator={operator}, value={value} Error: {e} Usage: FilterTuple( (f.
  - Raise ValueError(error\_context) with cause e.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L802) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1430)

<a id="op-dcec7e8fe7134d"></a>
### Filter Tuple.str

`operation_foundation_types_filter_business_behavior_filter_tuple_text`

**Inputs** self.

**Wrappers, in declaration order** override.

**Declared result** str.

**Explicit results** formatted text &lt;{self.doctype}&gt;.{self.fieldname} {self.operator} {value\_repr}.

**Local steps**

- Set value\_repr from formatted text '{self.value}' when isinstance(self.value, str), otherwise repr(self.value).
  - Value choice on isinstance(self.value, str) — true gives formatted text '{self.value}', false gives repr(self.value).
- Return formatted text &lt;{self.doctype}&gt;.{self.fieldname} {self.operator} {value\_repr}.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L1204) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L803) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1431)

<a id="op-5a7701a9e58b50"></a>
### Filters.initialize

`operation_foundation_types_filter_business_behavior_filters_initialize`

**Inputs** self (positional only), remaining positional values s, doctype (named only, default UNSPECIFIED).

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** ValueError(error\_context).

**Local steps**

- Evaluate super().\_\_init\_\_().
- Attempt the following.
  - If len(s) equals 1.
    - If len(s at 0) equals 0.
      - Return no value.
    - If (not isinstance(s at 0, FilterTuple) and isinstance(s at 0, Sequence) and not isinstance(s at 0 at 0, str) and isinstance(s at 0 at 0, (Sequence bitwise or Mapping))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not isinstance(s at 0, FilterTuple) → isinstance(s at 0, Sequence) → not isinstance(s at 0 at 0, str) → isinstance(s at 0 at 0, (Sequence bitwise or Mapping)).
      - Evaluate self.extend(cast(Iterable at ((FilterTuple bitwise or FilterTupleSpec) bitwise or FilterMappingSpec), s at 0), doctype).
    - Otherwise.
      - Evaluate self.extend(cast(Iterable at ((FilterTuple bitwise or FilterTupleSpec) bitwise or FilterMappingSpec), s), doctype).
  - Otherwise.
    - Evaluate self.extend(cast(Iterable at ((FilterTuple bitwise or FilterTupleSpec) bitwise or FilterMappingSpec), s), doctype).
- On failure (Exception) bound to e.
  - Set error\_lines from str(e).split(whitespace '\\n').
  - Set indented\_error from ((error\_lines at 0 + whitespace '\\n') + textwrap.indent(whitespace '\\n'.join(error\_lines at slice 1 to no value), 7 spaces)).
  - Set error\_context from formatted text  Error creating Filters: Input: {s}, doctype={doctype} Usage: Filters( FilterTuple(...), ...                                    )        Filters( (fie.
  - Raise ValueError(error\_context) with cause e.
- If self.
  - Evaluate self.optimize().

If control reaches the end, it returns no value.

**Methods declared on this owner** [extend](operations-056.md#op-1959c70aeedc5e), [optimize](operations-056.md#op-0219de499ede30).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L1406) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L806) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1434)

<a id="op-1959c70aeedc5e"></a>
### Filters.extend

`operation_foundation_types_filter_business_behavior_filters_extend`

**Inputs** self, values, doctype = UNSPECIFIED.

**Wrappers, in declaration order** override.

**Declared result** no value.

**Local steps**

- For each item in values.
  - Evaluate self.append(item, doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append](operations-056.md#op-06f7033d670c0e).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L2178) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1433)

<a id="op-06f7033d670c0e"></a>
### Filters.append

`operation_foundation_types_filter_business_behavior_filters_append`

**Inputs** self, value, doctype = UNSPECIFIED.

**Wrappers, in declaration order** override.

**Declared result** no value.

**Explicit failure paths** ValueError(“When initiated with a mapping, doctype keyword argument is required”) · TypeError(formatted text Expected FilterTruple, Mapping or Sequence, got {type(value).\_\_name\_\_}).

**Local steps**

- If isinstance(value, FilterTuple).
  - Evaluate super().append(value).
- Otherwise.
  - If isinstance(value, Mapping).
    - If (is\_unspecified(doctype) or doctype is identical to no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_unspecified(doctype) → doctype is identical to no value.
      - Raise ValueError(“When initiated with a mapping, doctype keyword argument is required”).
    - Evaluate self.\_init\_from\_mapping(value, doctype).
  - Otherwise.
    - If isinstance(value, Sequence).
      - Evaluate super().append(FilterTuple(value, doctype = doctype)).
    - Otherwise.
      - Raise TypeError(formatted text Expected FilterTruple, Mapping or Sequence, got {type(value).\_\_name\_\_}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [init from mapping](operations-056.md#op-ba8fd247fb28ae).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L2326) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1432)

<a id="op-ba8fd247fb28ae"></a>
### Filters.init from mapping

`operation_foundation_types_filter_business_behavior_filters_initialize_from_mapping`

**Inputs** self, s, doctype.

**Declared result** no value.

**Explicit failure paths** ValueError(formatted text Invalid value for key '{k}': expected value or (operator, value&#91;s&#93;) tuple).

**Local steps**

- For each tuple(k, v) in s.items().
  - If isinstance(v, \_InputValue).
    - Evaluate self.append(FilterTuple(doctype = doctype, fieldname = k, value = v)).
  - Otherwise.
    - If isinstance(v, Sequence).
      - Evaluate self.append(FilterTuple(doctype = doctype, fieldname = k, operator = v at 0, value = v at 1)).
    - Otherwise.
      - Raise ValueError(formatted text Invalid value for key '{k}': expected value or (operator, value&#91;s&#93;) tuple).

If control reaches the end, it returns no value.

**Methods declared on this owner** [append](operations-056.md#op-06f7033d670c0e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L2734) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L807) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1435)

<a id="op-0219de499ede30"></a>
### Filters.optimize

`operation_foundation_types_filter_business_behavior_filters_optimize`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind local operation group\_key for subsequent calls.
- Set optimized from Filters().
- For each tuple(tuple(doctype, fieldname, collatable), filters) in groupby(sorted(self, key = group\_key), key = group\_key).
  - If not collatable.
    - Evaluate optimized.extend(filters).
  - Otherwise.
    - Bind local operation \_values for subsequent calls.
    - Set values from tuple(\_values()).
    - Set \_op from “in” when len(values) &gt; 1, otherwise “=”.
      - Value choice on len(values) &gt; 1 — true gives “in”, false gives “=”.
    - Evaluate optimized.append(FilterTuple(doctype = doctype, fieldname = fieldname, operator = \_op, value = values when \_op equals “in”, otherwise values at 0)).
      - Value choice on \_op equals “in” — true gives values, false gives values at 0.
- Set self at slice no value to no value from optimized.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L3063) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1436)
