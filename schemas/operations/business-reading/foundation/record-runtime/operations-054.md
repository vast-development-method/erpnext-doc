# Record lifecycle and persistence · operations 54

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · File

[Record definition](../../../../data/record-types/file.json)

<a id="op-80caa2af066da6"></a>
### File.exists on disk

`operation_foundation_core_record_definitions_file_business_behavior_file_exists_on_disk`

**Inputs** self.

**Explicit results** os.path.exists(self.get\_full\_path()).

**Local steps**

- Return os.path.exists(self.get\_full\_path()).

**Methods declared on this owner** [get full path](operations-054.md#op-187737d314f064).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L3782) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1478)

<a id="op-cbacd25d2bb6ea"></a>
### File.get content

`operation_foundation_core_record_definitions_file_business_behavior_file_get_content`

**Inputs** self, encodings = no value.

**Declared result** (bytes bitwise or str).

**Explicit results** self.\_content.

**Explicit failure paths** validation helper — translated “Cannot get file contents of a Folder”.

**Local steps**

- If self.is\_folder.
  - Call the validation error handler Platform.throw(translated “Cannot get file contents of a Folder”).
- Evaluate self.validate\_file\_path().
- If self.get(“content”).
  - Set self.\_content from self.content.
  - If self.decode.
    - Set self.\_content from decode\_file\_content(self.\_content).
    - Set self.decode from false.
  - Return self.\_content.
- If self.file\_url.
  - Evaluate self.validate\_file\_url().
- Set file\_path from self.get\_full\_path().
- If encodings is identical to no value.
  - Set encodings from FILE\_ENCODING\_OPTIONS.
- Within open(file\_path, mode = “rb”) bound as f.
  - Set self.\_content from f.read().
  - Set kind from filetype.guess(self.\_content).
  - If (not kind and not self.\_content.startswith(OLE\_FILE\_SIGNATURE)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not kind → not self.\_content.startswith(OLE\_FILE\_SIGNATURE).
    - For each encoding in encodings.
      - Attempt the following.
        - Set self.\_content from self.\_content.decode(encoding).
        - Leave the innermost loop without its normal-exhaustion alternative.
      - On failure (UnicodeDecodeError).
        - Continue with the next iteration or loop test.
- Return self.\_content.

**Methods declared on this owner** [validate file path](operations-053.md#op-68a371b94ad155), [validate file url](operations-053.md#op-0b5b8fb833b838), [get full path](operations-054.md#op-187737d314f064).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L3854) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1481)

<a id="op-187737d314f064"></a>
### File.get full path

`operation_foundation_core_record_definitions_file_business_behavior_file_get_full_path`

**Inputs** self.

**Explicit results** file\_path.

**Explicit failure paths** validation helper — translated “There is some problem with the file url: {0}”.format(file\_path) · validation helper — translated “Cannot access file path {0}”.format(file\_path) · validation helper — translated “File name cannot have {0}”.format(os.path.sep).

**Local steps**

- Set file\_path from (self.file\_url or self.file\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.file\_url → self.file\_name.
- Set site\_url from get\_url().
- If (“/files/” belongs to file\_path and file\_path.startswith(site\_url)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “/files/” belongs to file\_path → file\_path.startswith(site\_url).
  - Set file\_path from file\_path.split(site\_url, 1) at 1.
- If “/” does not belong to file\_path.
  - If self.is\_private.
    - Set file\_path from formatted text /private/files/{file\_path}.
  - Otherwise.
    - Set file\_path from formatted text /files/{file\_path}.
- If file\_path.startswith(“/private/files/”).
  - Set file\_path from get\_files\_path(expanded nested operand in the contract.split(“/private/files/”, 1) at 1.split(“/”), is\_private = 1).
- Otherwise.
  - If file\_path.startswith(“/files/”).
    - Set file\_path from get\_files\_path(expanded nested operand in the contract.split(“/files/”, 1) at 1.split(“/”)).
  - Otherwise.
    - If file\_path.startswith(URL\_PREFIXES).
      - Take no action here.
    - Otherwise.
      - If not self.file\_url.
        - Call the validation error handler Platform.throw(translated “There is some problem with the file url: {0}”.format(file\_path)).
- If not is\_safe\_path(file\_path).
  - Call the validation error handler Platform.throw(translated “Cannot access file path {0}”.format(file\_path)).
- If os.path.sep belongs to self.file\_name.
  - Call the validation error handler Platform.throw(translated “File name cannot have {0}”.format(os.path.sep)).
- Return file\_path.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L4442) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1495) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1483)

<a id="op-5ef2425c94d152"></a>
### File.write file

`operation_foundation_core_record_definitions_file_business_behavior_file_write_file`

**Inputs** self.

**Explicit results** no value · file\_path.

**Local steps**

- If self.is\_remote\_file.
  - Return no value.
- Set file\_path from self.get\_full\_path().
- If isinstance(self.\_content, str).
  - Set self.\_content from self.\_content.encode().
- Evaluate self.check\_content().
- Within open(file\_path, “wb+”) bound as f.
  - Evaluate f.write(self.\_content).
  - Evaluate os.fsync(f.fileno()).
- Evaluate Platform.db.after\_rollback.add(self.on\_rollback).
- Return file\_path.

**Methods declared on this owner** [get full path](operations-054.md#op-187737d314f064), [check content](operations-053.md#op-7e31f65d1fb948).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L5197) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1529) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1515)

<a id="op-beb53f54919003"></a>
### File.save file

`operation_foundation_core_record_definitions_file_business_behavior_file_save_file`

**Inputs** self, content = no value, decode = false, ignore\_existing\_file\_check = false, overwrite = false.

**Record and data access** read “File” via get\_value · resolve a document from “File” via get\_cached\_doc · read “File” via exists.

**Explicit results** no value · write\_file\_method(self) · mapping(“file\_name” → self.file\_name, “file\_url” → self.file\_url) · self.save\_file\_on\_filesystem().

**Local steps**

- If self.is\_remote\_file.
  - Return no value.
- If not self.flags.new\_file.
  - Set self.flags.original\_content from self.get\_content().
- If content.
  - Set self.content from content.
  - Set self.decode from decode.
  - Evaluate self.get\_content().
- If not self.\_content.
  - Return no value.
- Set file\_exists from false.
- Set duplicate\_file from no value.
- Set self.is\_private from cint(self.is\_private).
- Set self.content\_type from mimetypes.guess\_type(self.file\_name) at 0.
- If (self.content\_type and self.content\_type equals “image/jpeg” and Platform.get\_system\_settings(“strip\_exif\_metadata\_from\_uploaded\_images”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.content\_type → self.content\_type equals “image/jpeg” → Platform.get\_system\_settings(“strip\_exif\_metadata\_from\_uploaded\_images”).
  - Bind dependencies strip\_exif\_data.
  - Set self.\_content from strip\_exif\_data(self.\_content, self.content\_type).
- Set self.file\_size from self.check\_max\_file\_size().
- Set self.content\_hash from get\_content\_hash(self.\_content).
- If (not ignore\_existing\_file\_check and not overwrite).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not ignore\_existing\_file\_check → not overwrite.
  - Set duplicate\_file from Platform.get\_value(“File”, mapping(“content\_hash” → self.content\_hash, “is\_private” → self.is\_private), list(“file\_url”, “name”), as\_dict = true).
- If duplicate\_file.
  - Set file\_doc from Platform.get\_cached\_doc(“File”, duplicate\_file.name).
  - If file\_doc.exists\_on\_disk().
    - If self.exists\_on\_disk().
      - If not self.file\_url.
        - Set self.file\_url from duplicate\_file.file\_url.
    - Otherwise.
      - Set self.file\_url from duplicate\_file.file\_url.
    - Set file\_exists from true.
- If not file\_exists.
  - Set in\_place from (overwrite and self.file\_url and not Platform.db.exists(“File”, mapping(“file\_url” → self.file\_url, “name” → tuple(“!=”, self.name)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in overwrite → self.file\_url → not Platform.db.exists(“File”, mapping(“file\_url” → self.file\_url, “name” → tuple(“!=”, self.name))).
  - If not in\_place.
    - Evaluate self.flags.pop(“original\_content”, no value).
    - Set self.file\_name from generate\_file\_name(name = self.file\_name, suffix = self.content\_hash at slice negative 6 to no value, is\_private = self.is\_private).
  - Evaluate call\_hook\_method(“before\_write\_file”, file\_size = self.file\_size).
  - Set write\_file\_method from get\_hook\_method(“write\_file”).
  - If write\_file\_method.
    - Return write\_file\_method(self).
  - If in\_place.
    - Evaluate self.write\_file().
    - Return mapping(“file\_name” → self.file\_name, “file\_url” → self.file\_url).
  - Return self.save\_file\_on\_filesystem().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get content](operations-054.md#op-cbacd25d2bb6ea), [check max file size](operations-054.md#op-a5f9c8a474933f), [exists on disk](operations-054.md#op-80caa2af066da6), [write file](operations-054.md#op-5ef2425c94d152), [save file on filesystem](operations-054.md#op-9ccf0f816454da).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“strip\_exif\_metadata\_from\_uploaded\_images”), Platform.get\_cached\_doc(“File”, duplicate\_file.name) · selected callable from get\_hook\_method(“write\_file”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L64) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1495)

<a id="op-9ccf0f816454da"></a>
### File.save file on filesystem

`operation_foundation_core_record_definitions_file_business_behavior_file_save_file_on_filesystem`

**Inputs** self.

**Explicit results** mapping(“file\_name” → os.path.basename(fpath), “file\_url” → self.file\_url).

**Local steps**

- Set safe\_file\_name from get\_safe\_file\_name(self.file\_name).
- If self.is\_private.
  - Set self.file\_url from formatted text /private/files/{safe\_file\_name}.
- Otherwise.
  - Set self.file\_url from formatted text /files/{safe\_file\_name}.
- Set fpath from self.write\_file().
- Return mapping(“file\_name” → os.path.basename(fpath), “file\_url” → self.file\_url).

**Methods declared on this owner** [write file](operations-054.md#op-5ef2425c94d152).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L6582) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1496)

<a id="op-a5f9c8a474933f"></a>
### File.check max file size

`operation_foundation_core_record_definitions_file_business_behavior_file_check_maximum_file_size`

**Inputs** self.

**Explicit results** file\_size.

**Explicit failure paths** validation helper with MaxFileSizeReachedError — msg.

**Local steps**

- Bind dependencies get\_max\_file\_size.
- Set max\_file\_size from get\_max\_file\_size().
- Set file\_size from len((self.\_content or byte value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.\_content → byte value.
- If file\_size &gt; max\_file\_size.
  - Set msg from translated “File size exceeded the maximum allowed size of {0} MB”.format((max\_file\_size ÷ 1048576)).
  - If Platform.has\_permission(“System Settings”, “write”).
    - Update msg using + (“.&lt;br&gt;” + translated “You can increase the limit from System Settings.”).
  - Call the validation error handler Platform.throw(msg, exc = MaxFileSizeReachedError).
- Return file\_size.

**Values supplied outside this operation** effective access from Platform.has\_permission(“System Settings”, “write”).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L59) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1471)

<a id="op-2f894993f9ff2d"></a>
### File.delete file data content

`operation_foundation_core_record_definitions_file_business_behavior_file_delete_file_data_content`

**Inputs** self, only\_thumbnail = false.

**Local steps**

- Set method from get\_hook\_method(“delete\_file\_data\_content”).
- If method.
  - Evaluate method(self, only\_thumbnail = only\_thumbnail).
- Otherwise.
  - Evaluate self.delete\_file\_from\_filesystem(only\_thumbnail = only\_thumbnail).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete file from filesystem](operations-054.md#op-0670c26907f39b).

**Values supplied outside this operation** selected callable from get\_hook\_method(“delete\_file\_data\_content”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L7130) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1486) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1474)

<a id="op-0670c26907f39b"></a>
### File.delete file from filesystem

`operation_foundation_core_record_definitions_file_business_behavior_file_delete_file_from_filesystem`

**Inputs** self, only\_thumbnail = false.

**Local steps**

- If only\_thumbnail.
  - Evaluate delete\_file(self.thumbnail\_url).
- Otherwise.
  - Evaluate delete\_file(self.file\_url).
  - Evaluate delete\_file(self.thumbnail\_url).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L7271) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1487) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1475)

<a id="op-4dbb353ac962be"></a>
### File.is downloadable

`operation_foundation_core_record_definitions_file_business_behavior_file_is_downloadable`

**Inputs** self.

**Explicit results** has\_permission(self, “read”).

**Local steps**

- Return has\_permission(self, “read”).

**Values supplied outside this operation** effective access from has\_permission(self, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L7397) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1488)

<a id="op-ebabd92cd0a8c1"></a>
### File.get extension

`operation_foundation_core_record_definitions_file_business_behavior_file_get_extension`

**Inputs** self.

**Explicit results** os.path.splitext(self.file\_name).

**Local steps**

- Return os.path.splitext(self.file\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L7458) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1494) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1482)

<a id="op-daae29cab9f22b"></a>
### File.create attachment record

`operation_foundation_core_record_definitions_file_business_behavior_file_create_attachment_record`

**Inputs** self.

**Local steps**

- Set icon from “ &lt;i class="fa fa-lock text-warning"&gt;&lt;/i&gt;” when self.is\_private, otherwise empty text.
  - Value choice on self.is\_private — true gives “ &lt;i class="fa fa-lock text-warning"&gt;&lt;/i&gt;”, false gives empty text.
- Set file\_url from quote(Platform.safe\_encode(self.file\_url), safe = “/:”) when self.file\_url, otherwise self.file\_name.
  - Value choice on self.file\_url — true gives quote(Platform.safe\_encode(self.file\_url), safe = “/:”), false gives self.file\_name.
- Set file\_name from escape\_html((self.file\_name or self.file\_url)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.file\_name → self.file\_url.
- Evaluate self.add\_comment\_in\_reference\_doc(“Attachment”, formatted text &lt;a href='{file\_url}' target='\_blank'&gt;{file\_name}&lt;/a&gt;{icon}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [add comment in reference doc](operations-054.md#op-a4bbf6d9281f83).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0079.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1485) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1473)

<a id="op-a4bbf6d9281f83"></a>
### File.add comment in reference doc

`operation_foundation_core_record_definitions_file_business_behavior_file_add_comment_in_reference_record`

**Inputs** self, comment\_type, text.

**Record and data access** resolve a document from self.attached\_to\_doctype via get\_doc.

**Local steps**

- If (self.attached\_to\_doctype and self.attached\_to\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attached\_to\_doctype → self.attached\_to\_name.
  - Attempt the following.
    - Set doc from Platform.get\_doc(self.attached\_to\_doctype, self.attached\_to\_name).
    - Evaluate doc.add\_comment(comment\_type, text).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.clear\_messages().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0079.json#L262) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1477) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1465)

<a id="op-d55f992556c228"></a>
### File.set is private

`operation_foundation_core_record_definitions_file_business_behavior_file_set_is_private`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.is\_private.
  - Return no value.
- If self.file\_url.
  - Set self.is\_private from cint(self.file\_url.startswith(“/private”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0079.json#L448) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1500)

<a id="op-e155f69972cd93"></a>
### File.validate file url matches record

`operation_foundation_binding_foundation_core_doctype_file_file_file_validate_file_url_matches_record`

**Inputs** self.

**Record and data access** read “File” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “The File URL does not belong to this File record”.

**Local steps**

- If not self.file\_url.
  - Return no value.
- Set actual\_file\_url from Platform.db.get\_value(“File”, self.name, “file\_url”) when self.name, otherwise no value.
  - Value choice on self.name — true gives Platform.db.get\_value(“File”, self.name, “file\_url”), false gives no value.
- If actual\_file\_url differs from self.file\_url.
  - Call the validation error handler Platform.throw(translated “The File URL does not belong to this File record”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L171) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L629)

<a id="op-0a0be33cc5c834"></a>
### File.optimize file

`operation_foundation_core_record_definitions_file_business_behavior_file_optimize_file`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Explicit results** no value.

**Explicit failure paths** TypeError(“Folders cannot be optimized”) · NotImplementedError(“Only local image files can be optimized”) · TypeError(“Optimization of SVG images is not supported”).

**Local steps**

- Evaluate Platform.has\_permission(self.doctype, “write”, self.name, throw = true).
- If self.is\_folder.
  - Raise TypeError(“Folders cannot be optimized”).
- Evaluate self.validate\_file\_url\_matches\_record().
- Set content\_type from mimetypes.guess\_type(self.file\_name) at 0.
- Set is\_local\_image from (content\_type.startswith(“image/”) and self.file\_size &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in content\_type.startswith(“image/”) → self.file\_size &gt; 0.
- Set is\_svg from content\_type equals “image/svg+xml”.
- If not is\_local\_image.
  - Raise NotImplementedError(“Only local image files can be optimized”).
- If is\_svg.
  - Raise TypeError(“Optimization of SVG images is not supported”).
- Bind dependencies optimize\_image.
- Set original\_content from self.get\_content().
- Set optimized\_content from optimize\_image(content = original\_content, content\_type = content\_type).
- If original\_content equals optimized\_content.
  - Return no value.
- Evaluate self.save\_file(content = optimized\_content, overwrite = true).
- Evaluate self.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate file url matches record](operations-054.md#op-e155f69972cd93), [get content](operations-054.md#op-cbacd25d2bb6ea), [save file](operations-054.md#op-beb53f54919003).

**Values supplied outside this operation** effective access from Platform.has\_permission(self.doctype, “write”, self.name, throw = true).

**Boundaries to resolve** stored data, callee failures, file state, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L63) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1494)

<a id="op-62dcf61dbb9de6"></a>
### File.unique url

`operation_foundation_core_record_definitions_file_business_behavior_file_unique_resource_address`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** ((self.file\_url + “?”) + urlencode(mapping(“fid” → self.name))) · self.file\_url.

**Local steps**

- Bind dependencies urlencode.
- If self.is\_private.
  - Return ((self.file\_url + “?”) + urlencode(mapping(“fid” → self.name))).
- Otherwise.
  - Return self.file\_url.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0079.json#L1006) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1501)

<a id="op-dad7e4ca1488df"></a>
### File.zip files

`operation_foundation_core_record_definitions_file_business_behavior_file_zip_files`

**Inputs** files.

**Wrappers, in declaration order** staticmethod.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** zip\_file.getvalue().

**Local steps**

- Set tuple(requested, added) from tuple(set(), set()).
- Set zip\_file from io.BytesIO().
- Set zf from zipfile.ZipFile(zip\_file, “w”, zipfile.ZIP\_DEFLATED).
- For each \_file in files.
  - If isinstance(\_file, str).
    - If \_file belongs to requested.
      - Continue with the next iteration or loop test.
    - Evaluate requested.add(\_file).
    - Set \_file from Platform.get\_doc(“File”, \_file).
  - If not isinstance(\_file, File).
    - Continue with the next iteration or loop test.
  - If (\_file.is\_folder or \_file.name belongs to added).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_file.is\_folder → \_file.name belongs to added.
    - Continue with the next iteration or loop test.
  - If not has\_permission(\_file, “read”).
    - Continue with the next iteration or loop test.
  - Evaluate added.add(\_file.name).
  - Evaluate zf.writestr(\_file.file\_name, \_file.get\_content()).
- Evaluate zf.close().
- Return zip\_file.getvalue().

**Values supplied outside this operation** effective access from has\_permission(\_file, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L70) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1516)

<a id="op-51bce35f2901ff"></a>
### On doctype update

`operation_foundation_core_record_definitions_file_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “File”.

**Local steps**

- Evaluate Platform.db.add\_index(“File”, list(“attached\_to\_doctype”, “attached\_to\_name”)).
- Evaluate Platform.db.add\_index(“File”, list(“file\_url(100)”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0079.json#L1485) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1519)

<a id="op-2ce041118a3c62"></a>
### Has permission

`operation_foundation_core_record_definitions_file_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, debug.

**Explicit result forms** Boolean false, Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 6 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L72) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1518)

<a id="op-5b489ded894a37"></a>
### Get permission query conditions

`operation_foundation_core_record_definitions_file_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Observed service boundaries** effective access lookup, record lookup.

**Local structure** 3 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L71) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1517)

<a id="op-15441be6d99837"></a>
### Scoped attachment condition

`operation_foundation_binding_foundation_core_doctype_file_file_scoped_attachment_condition`

**Inputs** doctype, user, exists\_condition.

**Declared result** str.

**Explicit results** formatted text (′tabFile′.′attached\_to\_doctype′ = {Platform.db.escape(doctype)}  AND (  EXISTS (  SELECT 1 FROM {table}  WHERE {table}.′name′ = ′tabFile′.′a.

**Local steps**

- Set table from get\_table\_name(doctype, wrap\_in\_backticks = true).
- Set shared\_names from Platform.share.get\_shared(doctype, user).
- Set shared\_condition from empty text.
- If shared\_names.
  - Set shared\_list from “, ”.join(generator of Platform.db.escape(name, percent = false) for name drawn from shared\_names).
    - Draw name from shared\_names.
  - Set shared\_condition from formatted text  OR ′tabFile′.′attached\_to\_name′ IN ({shared\_list}).
- Return formatted text (′tabFile′.′attached\_to\_doctype′ = {Platform.db.escape(doctype)}  AND (  EXISTS (  SELECT 1 FROM {table}  WHERE {table}.′name′ = ′tabFile′.′a.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L173) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L631)

<a id="op-20728e5e33fd6f"></a>
### Split doctypes by owner constraint

`operation_foundation_binding_foundation_core_doctype_file_file_split_doctypes_by_owner_constraint`

**Inputs** doctypes, user.

**Explicit results** tuple(openly\_readable, owner\_restricted).

**Local steps**

- Set tuple(openly\_readable, owner\_restricted) from tuple(list(), list()).
- For each doctype in doctypes.
  - If Platform.get\_meta(doctype).issingle.
    - Evaluate openly\_readable.append(doctype).
    - Continue with the next iteration or loop test.
  - Set role\_permissions from get\_role\_permissions(doctype, user = user).
  - If requires\_owner\_constraint(role\_permissions).
    - Evaluate owner\_restricted.append(doctype).
  - Otherwise.
    - Evaluate openly\_readable.append(doctype).
- Return tuple(openly\_readable, owner\_restricted).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L174) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L632)

<a id="op-3df2c1d6f9ead8"></a>
### Split doctypes by user permissions

`operation_foundation_binding_foundation_core_doctype_file_file_split_doctypes_by_user_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctypes, user.

**Explicit result forms** a structured result.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L175) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L633)
