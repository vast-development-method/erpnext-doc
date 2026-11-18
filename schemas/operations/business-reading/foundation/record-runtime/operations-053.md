# Record lifecycle and persistence · operations 53

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · File

[Record definition](../../../../data/record-types/file.json)

<a id="op-1d6aa9426fa18a"></a>
### File.on trash

`operation_foundation_core_record_definitions_file_business_behavior_file_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cannot delete Home and Attachments folders”.

**Local steps**

- If (self.is\_home\_folder or self.is\_attachments\_folder).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_home\_folder → self.is\_attachments\_folder.
  - Call the validation error handler Platform.throw(translated “Cannot delete Home and Attachments folders”).
- Evaluate self.validate\_empty\_folder().
- Evaluate self.validate\_protected\_file().
- Evaluate Platform.db.after\_commit.add(self.\_delete\_file\_on\_disk).
- If not self.is\_folder.
  - Evaluate self.add\_comment\_in\_reference\_doc(“Attachment Removed”, self.file\_name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate empty folder](operations-053.md#op-f532b38e968c5d), [validate protected file](operations-053.md#op-7d7772d4543606), [add comment in reference doc](operations-054.md#op-a4bbf6d9281f83).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L62) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1493)

<a id="op-358db65de7796a"></a>
### File.on rollback

`operation_foundation_core_record_definitions_file_business_behavior_file_on_rollback`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set rollback\_flags from tuple(“new\_file”, “original\_content”, “original\_path”).
- Bind local operation pop\_rollback\_flags for subsequent calls.
- If self.flags.new\_file.
  - Evaluate self.\_delete\_file\_on\_disk().
  - Evaluate pop\_rollback\_flags().
  - Return no value.
- If self.flags.original\_content.
  - Set file\_path from self.get\_full\_path().
  - If isinstance(self.flags.original\_content, bytes).
    - Set mode from “wb+”.
  - Otherwise.
    - If isinstance(self.flags.original\_content, str).
      - Set mode from “w+”.
  - Within open(file\_path, mode) bound as f.
    - Evaluate f.write(self.flags.original\_content).
    - Evaluate os.fsync(f.fileno()).
    - Evaluate pop\_rollback\_flags().
- If self.flags.original\_path.
  - Set target from self.flags.original\_path at “old”.
  - Set source from self.flags.original\_path at “new”.
  - Evaluate shutil.move(source, target).
  - Evaluate pop\_rollback\_flags().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete file on disk](operations-053.md#op-bb97673684944f), [get full path](operations-054.md#op-187737d314f064).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L1501) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1491)

<a id="op-7bbe1cf26fb01c"></a>
### File.on rollback.pop rollback flags

`operation_foundation_core_record_definitions_file_business_behavior_file_on_rollback_post_office_protocol_rollback_flags`

**Inputs** no declared parameters.

**Local steps**

- For each flag in rollback\_flags.
  - Evaluate self.flags.pop(flag, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L2046) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1492)

<a id="op-a26450eeb084d8"></a>
### File.get name based on parent folder

`operation_foundation_core_record_definitions_file_business_behavior_file_get_name_based_on_parent_folder`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Explicit results** os.path.join(self.folder, self.file\_name).

**Local steps**

- If self.folder.
  - Return os.path.join(self.folder, self.file\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L2114) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1496) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1484)

<a id="op-aa75d59eba4507"></a>
### File.get successors

`operation_foundation_core_record_definitions_file_business_behavior_file_get_successors`

**Inputs** self.

**Record and data access** read “File” via get\_all.

**Explicit results** Platform.get\_all(“File”, filters = mapping(“folder” → self.name), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“File”, filters = mapping(“folder” → self.name), pluck = “name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L2208) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1485)

<a id="op-68a371b94ad155"></a>
### File.validate file path

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_file_path`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “The File URL you've entered is incorrect”.

**Local steps**

- If self.is\_remote\_file.
  - Return no value.
- If (self.file\_url and “..” belongs to self.file\_url.split(“/”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.file\_url → “..” belongs to self.file\_url.split(“/”).
  - Call the validation error handler Platform.throw(translated “The File URL you've entered is incorrect”, title = translated “Invalid File URL”).
- Set base\_path from os.path.realpath(get\_files\_path(is\_private = self.is\_private)).
- Set file\_path from os.path.realpath(self.get\_full\_path()).
- If os.path.commonpath(tuple(base\_path, file\_path)) differs from base\_path.
  - Call the validation error handler Platform.throw(translated “The File URL you've entered is incorrect”, title = translated “Invalid File URL”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get full path](operations-054.md#op-187737d314f064).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L68) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1522) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1510)

<a id="op-0b5b8fb833b838"></a>
### File.validate file url

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_file_resource_address`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated text in the contract.

**Local steps**

- If (self.is\_remote\_file or not self.file\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_remote\_file → not self.file\_url.
  - Return no value.
- If not self.file\_url.startswith(tuple(“/files/”, “/private/files/”)).
  - Call the validation error handler Platform.throw(translated text in the contract, title = translated “Invalid URL”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L2549) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1523) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1511)

<a id="op-434563a840c4b7"></a>
### File.handle is private changed

`operation_foundation_core_record_definitions_file_business_behavior_file_handle_is_private_changed`

**Inputs** self.

**Record and data access** read self.attached\_to\_doctype via get\_single\_value · read self.attached\_to\_doctype via exists.

**State and service calls** request set\_single\_value on self.attached\_to\_doctype · request set\_value on self.attached\_to\_doctype.

**Explicit results** no value.

**Explicit failure paths** validation helper with FileNotFoundError — translated “Cannot find file {} on disk”.format(source) · validation helper with FileExistsError — translated “A file with same name {} already exists”.format(target).

**Local steps**

- If self.is\_remote\_file.
  - Return no value.
- Bind dependencies Path.
- Set old\_file\_url from self.file\_url.
- Set file\_name from self.file\_url.split(“/”) at negative 1.
- Set private\_file\_path from Path(Platform.get\_site\_path(“private”, “files”, file\_name)).
- Set public\_file\_path from Path(Platform.get\_site\_path(“public”, “files”, file\_name)).
- If cint(self.is\_private).
  - Set source from public\_file\_path.
  - Set target from private\_file\_path.
  - Set url\_starts\_with from “/private/files/”.
- Otherwise.
  - Set source from private\_file\_path.
  - Set target from public\_file\_path.
  - Set url\_starts\_with from “/files/”.
- Set updated\_file\_url from formatted text {url\_starts\_with}{file\_name}.
- If updated\_file\_url equals old\_file\_url.
  - Return no value.
- If not source.exists().
  - Call the validation error handler Platform.throw(translated “Cannot find file {} on disk”.format(source), exc = FileNotFoundError).
- If target.exists().
  - Call the validation error handler Platform.throw(translated “A file with same name {} already exists”.format(target), exc = FileExistsError).
- Evaluate shutil.move(source, target).
- Set self.flags.original\_path from mapping(“old” → source, “new” → target).
- Evaluate Platform.db.after\_rollback.add(self.on\_rollback).
- Set self.file\_url from updated\_file\_url.
- Evaluate update\_existing\_file\_docs(self).
- If (not self.attached\_to\_doctype or not self.attached\_to\_name or not self.fetch\_attached\_to\_field(old\_file\_url)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.attached\_to\_doctype → not self.attached\_to\_name → not self.fetch\_attached\_to\_field(old\_file\_url).
  - Return no value.
- Set parent\_meta from Platform.get\_meta(self.attached\_to\_doctype).
- If parent\_meta.issingle.
  - If (parent\_meta.has\_field(self.attached\_to\_field) and Platform.db.get\_single\_value(self.attached\_to\_doctype, self.attached\_to\_field) equals old\_file\_url).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_meta.has\_field(self.attached\_to\_field) → Platform.db.get\_single\_value(self.attached\_to\_doctype, self.attached\_to\_field) equals old\_file\_url.
    - Evaluate Platform.db.set\_single\_value(self.attached\_to\_doctype, self.attached\_to\_field, self.file\_url).
- Otherwise.
  - If (parent\_meta.has\_field(self.attached\_to\_field) and Platform.db.exists(self.attached\_to\_doctype, mapping(“name” → self.attached\_to\_name, self.attached\_to\_field → old\_file\_url))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in parent\_meta.has\_field(self.attached\_to\_field) → Platform.db.exists(self.attached\_to\_doctype, mapping(“name” → self.attached\_to\_name, self.attached\_to\_field → old\_file\_url)).
    - Evaluate Platform.db.set\_value(self.attached\_to\_doctype, self.attached\_to\_name, self.attached\_to\_field, self.file\_url).

If control reaches the end, it returns no value.

**Methods declared on this owner** [fetch attached to field](operations-053.md#op-e35369fe4f12d5).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(self.attached\_to\_doctype, self.attached\_to\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L61) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1498) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1486)

<a id="op-e35369fe4f12d5"></a>
### File.fetch attached to field

`operation_foundation_core_record_definitions_file_business_behavior_file_fetch_attached_to_field`

**Inputs** self, old\_file\_url.

**Record and data access** resolve a document from self.attached\_to\_doctype via get\_doc.

**Explicit results** true.

**Local steps**

- If self.attached\_to\_field.
  - Return true.
- Set reference\_dict from Platform.get\_doc(self.attached\_to\_doctype, self.attached\_to\_name).as\_dict().
- For each tuple(key, value) in reference\_dict.items().
  - If value equals old\_file\_url.
    - Set self.attached\_to\_field from key.
    - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L4372) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1479)

<a id="op-1b2e813f3abdb9"></a>
### File.validate attachment limit

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_attachment_limit`

**Inputs** self.

**Record and data access** read “File” via get\_all.

**Explicit failure paths** validation helper with AttachmentLimitReached — translated “Maximum Attachment Limit of {0} has been reached for {1} {2}.”.format(Platform.bold(attachment\_limit), self.attached\_to\_doctype, self.attached\_to\_name).

**Local steps**

- Set attachment\_limit from 0.
- If (self.attached\_to\_doctype and self.attached\_to\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attached\_to\_doctype → self.attached\_to\_name.
  - Set attachment\_limit from cint(Platform.get\_meta(self.attached\_to\_doctype).max\_attachments).
- If attachment\_limit.
  - Set current\_attachment\_count from len(Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → self.attached\_to\_doctype, “attached\_to\_name” → self.attached\_to\_name), limit = (attachment\_limit + 1))).
  - If current\_attachment\_count ≥ attachment\_limit.
    - Call the validation error handler Platform.throw(translated “Maximum Attachment Limit of {0} has been reached for {1} {2}.”.format(Platform.bold(attachment\_limit), self.attached\_to\_doctype, self.attached\_to\_name), exc = AttachmentLimitReac ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L4564) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1516) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1504)

<a id="op-2880bcf229037f"></a>
### File.validate remote file

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_remote_file`

**Inputs** self.

**Local steps**

- Set site\_url from get\_url().
- If (self.file\_url and “/files/” belongs to self.file\_url and self.file\_url.startswith(site\_url)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.file\_url → “/files/” belongs to self.file\_url → self.file\_url.startswith(site\_url).
  - Set self.file\_url from self.file\_url.split(site\_url, 1) at 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L4959) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1514)

<a id="op-4f2f82967f68d2"></a>
### File.set folder name

`operation_foundation_core_record_definitions_file_business_behavior_file_set_folder_name`

**Inputs** self.

**Record and data access** read “File” via get\_value.

**Explicit results** no value.

**Local steps**

- If self.folder.
  - Return no value.
- If self.attached\_to\_doctype.
  - Set self.folder from Platform.db.get\_value(“File”, mapping(“is\_attachments\_folder” → 1)).
- Otherwise.
  - If not self.is\_home\_folder.
    - Set self.folder from “Home”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L5125) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1499)

<a id="op-45da8006d41a61"></a>
### File.set file type

`operation_foundation_core_record_definitions_file_business_behavior_file_set_file_type`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.is\_folder.
  - Return no value.
- Set file\_type from mimetypes.guess\_type(self.file\_name) at 0.
- If not file\_type.
  - Return no value.
- Set file\_extension from mimetypes.guess\_extension(file\_type).
- Set self.file\_type from file\_extension.lstrip(“.”).upper() when file\_extension, otherwise no value.
  - Value choice on file\_extension — true gives file\_extension.lstrip(“.”).upper(), false gives no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L5289) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1498)

<a id="op-87ec305de2fd44"></a>
### File.validate file on disk

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_file_on_disk`

**Inputs** self.

**Explicit results** true.

**Explicit failure paths** validation helper with IOError — translated “File {0} does not exist”.format(self.file\_url).

**Local steps**

- Set full\_path from self.get\_full\_path().
- If full\_path.startswith(URL\_PREFIXES).
  - Return true.
- If not os.path.exists(full\_path).
  - Call the validation error handler Platform.throw(translated “File {0} does not exist”.format(self.file\_url), IOError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get full path](operations-054.md#op-187737d314f064).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L5483) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1521) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1509)

<a id="op-7c5b82fe959e68"></a>
### File.validate file extension

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_file_extension`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper with FileTypeNotAllowed — translated “File type of {0} is not allowed”.format(file\_extension).

**Local steps**

- If (self.is\_folder or not Platform.request).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_folder → not Platform.request.
  - Return no value.
- Set allowed\_extensions from Platform.get\_system\_settings(“allowed\_file\_extensions”).
- If not allowed\_extensions.
  - Return no value.
- Set file\_extension from nested operand in the contract.splitext(nested operand in the contract.file\_name) at 1.lstrip(“.”).upper().
- If file\_extension does not belong to allowed\_extensions.splitlines().
  - Call the validation error handler Platform.throw(translated “File type of {0} is not allowed”.format(file\_extension), exc = FileTypeNotAllowed).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“allowed\_file\_extensions”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L5671) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1520) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1508)

<a id="op-7e31f65d1fb948"></a>
### File.check content

`operation_foundation_core_record_definitions_file_business_behavior_file_check_content`

**Inputs** self.

**Explicit failure paths** validation helper — translated “This PDF cannot be uploaded as it contains unsafe content.”.

**Local steps**

- Bind dependencies pdf\_contains\_js.
- If (self.file\_type equals “PDF” and self.\_content and pdf\_contains\_js(self.\_content)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.file\_type equals “PDF” → self.\_content → pdf\_contains\_js(self.\_content).
  - Call the validation error handler Platform.throw(translated “This PDF cannot be uploaded as it contains unsafe content.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L5965) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1482) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1470)

<a id="op-eeef550a333a43"></a>
### File.validate duplicate entry

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_duplicate_entry`

**Inputs** self.

**Record and data access** read “File” via get\_value · resolve a document from “File” via get\_cached\_doc.

**Local steps**

- If (not self.flags.ignore\_duplicate\_entry\_error and not self.is\_folder).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.flags.ignore\_duplicate\_entry\_error → not self.is\_folder.
  - If not self.content\_hash.
    - Evaluate self.generate\_content\_hash().
  - Set filters from mapping(“content\_hash” → self.content\_hash, “is\_private” → self.is\_private).
  - If self.name.
    - Evaluate filters.update(mapping(“name” → tuple(“!=”, self.name))).
  - If (self.attached\_to\_doctype and self.attached\_to\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attached\_to\_doctype → self.attached\_to\_name.
    - Evaluate filters.update(mapping(“attached\_to\_doctype” → self.attached\_to\_doctype, “attached\_to\_name” → self.attached\_to\_name)).
  - Set duplicate\_file from Platform.db.get\_value(“File”, filters, list(“name”, “file\_url”), as\_dict = 1).
  - If duplicate\_file.
    - Set duplicate\_file\_doc from Platform.get\_cached\_doc(“File”, duplicate\_file.name).
    - If duplicate\_file\_doc.exists\_on\_disk().
      - Set self.file\_url from duplicate\_file.file\_url.

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate content hash](operations-053.md#op-0c3c7893e43885).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“File”, duplicate\_file.name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L6106) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1518) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1506)

<a id="op-e31b8488b64ec5"></a>
### File.set file name

`operation_foundation_core_record_definitions_file_business_behavior_file_set_file_name`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Fields ′file\_name′ or ′file\_url′ must be set for File”.

**Local steps**

- If (not self.file\_name and not self.file\_url).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.file\_name → not self.file\_url.
  - Call the validation error handler Platform.throw(translated “Fields ′file\_name′ or ′file\_url′ must be set for File”, exc = Platform.MandatoryError).
- Otherwise.
  - If (not self.file\_name and self.file\_url).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.file\_name → self.file\_url.
    - Set self.file\_name from nested operand in the contract.file\_url.split(“/”) at negative 1.split(“?”) at 0.
  - Otherwise.
    - Set self.file\_name from re.sub(“/”, empty text, self.file\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L6603) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1497)

<a id="op-0c3c7893e43885"></a>
### File.generate content hash

`operation_foundation_core_record_definitions_file_business_behavior_file_generate_content_hash`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “File {0} does not exist”.format(file\_path).

**Local steps**

- If (self.content\_hash or not self.file\_url or self.is\_remote\_file).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.content\_hash → not self.file\_url → self.is\_remote\_file.
  - Return no value.
- Set file\_name from self.file\_url.split(“/”) at negative 1.
- Attempt the following.
  - Set file\_path from get\_files\_path(file\_name, is\_private = self.is\_private).
  - Within open(file\_path, “rb”) bound as f.
    - Set self.content\_hash from get\_content\_hash(f.read()).
- On failure (OSError).
  - Call the validation error handler Platform.throw(translated “File {0} does not exist”.format(file\_path)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0077.json#L6875) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1492) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1480)

<a id="op-dbee9394d52b88"></a>
### File.make thumbnail

`operation_foundation_core_record_definitions_file_business_behavior_file_make_thumbnail`

**Inputs** self, set\_as\_thumbnail = true, width = 300, height = 300, suffix = “small”, crop = false.

**Declared result** str.

**State and service calls** call save on image · call db\_set on self · msgprint with translated “Unable to write file format for {0}”.format(path).

**Explicit results** no value · thumbnail\_url.

**Local steps**

- Bind dependencies HTTPError, SSLError.
- Bind dependencies Image, ImageOps.
- If not self.file\_url.
  - Return no value.
- Attempt the following.
  - If self.file\_url.startswith(tuple(“/files”, “/private/files”)).
    - Set tuple(image, filename, extn) from get\_local\_image(self.file\_url).
  - Otherwise.
    - Set tuple(image, filename, extn) from get\_web\_image(self.file\_url).
- On failure (tuple(HTTPError, SSLError, OSError, TypeError)).
  - Return no value.
- Set size from tuple(width, height).
- If crop.
  - Set image from ImageOps.fit(image, size, Image.Resampling.LANCZOS).
- Otherwise.
  - Evaluate image.thumbnail(size, Image.Resampling.LANCZOS).
- Set thumbnail\_url from formatted text {filename}\_{suffix}.{extn}.
- Set path from os.path.abspath(Platform.get\_site\_path(“public”, thumbnail\_url.lstrip(“/”))).
- Attempt the following.
  - Evaluate image.save(path).
  - If set\_as\_thumbnail.
    - Evaluate self.db\_set(“thumbnail\_url”, thumbnail\_url).
- On failure (OSError).
  - Evaluate Platform.msgprint(translated “Unable to write file format for {0}”.format(path)).
  - Return no value.
- Return thumbnail\_url.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1502) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1490)

<a id="op-f532b38e968c5d"></a>
### File.validate empty folder

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_empty_folder`

**Inputs** self.

**Record and data access** read “File” via get\_all.

**Explicit failure paths** validation helper with FolderNotEmpty — translated “Folder {0} is not empty”.format(self.name).

**Local steps**

- If (self.is\_folder and Platform.get\_all(“File”, filters = mapping(“folder” → self.name), limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_folder → Platform.get\_all(“File”, filters = mapping(“folder” → self.name), limit = 1).
  - Call the validation error handler Platform.throw(translated “Folder {0} is not empty”.format(self.name), FolderNotEmpty).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L738) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1519) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1507)

<a id="op-7d7772d4543606"></a>
### File.validate protected file

`operation_foundation_core_record_definitions_file_business_behavior_file_validate_protected_file`

**Inputs** self.

**Record and data access** resolve a document from self.attached\_to\_doctype via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- If not (self.attached\_to\_doctype and self.attached\_to\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.attached\_to\_doctype → self.attached\_to\_name.
  - Return no value.
- Attempt the following.
  - Set ref\_doc from Platform.get\_doc(self.attached\_to\_doctype, self.attached\_to\_name).
- On failure (DoesNotExistError).
  - Return no value.
- If ref\_doc.docstatus equals 0.
  - Return no value.
- If not ref\_doc.meta.protect\_attached\_files.
  - Return no value.
- If (ref\_doc.docstatus equals 2 and ref\_doc.has\_permission(“delete”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_doc.docstatus equals 2 → ref\_doc.has\_permission(“delete”).
  - Return no value.
- Call the validation error handler Platform.throw(msg = translated “This file is attached to a protected document and cannot be deleted.”, title = translated “Protected File”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from ref\_doc.has\_permission(“delete”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0078.json#L924) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1527) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1513)

<a id="op-bb97673684944f"></a>
### File.delete file on disk

`operation_foundation_core_record_definitions_file_business_behavior_file_delete_file_on_disk`

**Inputs** self.

**Record and data access** read “File” via get\_all.

**Local steps**

- Set on\_disk\_file\_not\_shared from (self.content\_hash and not Platform.get\_all(“File”, filters = mapping(“content\_hash” → self.content\_hash, “name” → list(“!=”, self.name)), limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.content\_hash → not Platform.get\_all(“File”, filters = mapping(“content\_hash” → self.content\_hash, “name” → list(“!=”, self.name)), limit = 1).
- If on\_disk\_file\_not\_shared.
  - Evaluate self.delete\_file\_data\_content().
- Otherwise.
  - Evaluate self.delete\_file\_data\_content(only\_thumbnail = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete file data content](operations-054.md#op-2f894993f9ff2d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L60) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1476)

<a id="op-631aa3ceee4206"></a>
### File.unzip

`operation_foundation_core_record_definitions_file_business_behavior_file_unzip`

**Inputs** self.

**Declared result** list at “File”.

**State and service calls** request new\_doc for “File” · call save on file\_doc · request delete\_doc for “File”.

**Explicit results** files.

**Explicit failure paths** validation helper — translated “{0} is not a zip file”.format(self.file\_name) · validation helper — translated “Zip file contains more than the maximum allowed {0} files”.format(get\_max\_extract\_members()) · validation helper — translated “Zip file extracts to more than the maximum allowed size of {0} MB”.format((max\_extracted\_size floor divide 1048576)) · validation helper — translated “{0} is a not a valid zip file”.format(self.file\_name) · propagate active failure.

**Local steps**

- Bind dependencies get\_max\_extract\_members, get\_max\_extract\_size.
- If not self.file\_url.endswith(“.zip”).
  - Call the validation error handler Platform.throw(translated “{0} is not a zip file”.format(self.file\_name)).
- Evaluate self.check\_permission(“read”).
- Set zip\_path from self.get\_full\_path().
- Set max\_extracted\_size from get\_max\_extract\_size().
- Set files from list().
- Set total\_extracted\_size from 0.
- Within zipfile.ZipFile(zip\_path) bound as z.
  - Set members from list of file for file drawn from z.filelist where (not (file.is\_dir() or nested operand in the contract.filename.startswith(“\_\_MACOSX/”)) and not nested operand in the contract.basename(nested operand in t ….
    - Draw file from z.filelist, keep a combination only if ((not (file.is\_dir() or file.filename.startswith(“\_\_MACOSX/”)) and not nested operand in the contract.path.basename(file.filename).startswith(“.”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not (file.is\_dir() or file.filename.startswith(“\_\_MACOSX/”)) → not os.path.basename(file.filename).startswith(“.”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in file.is\_dir() → file.filename.startswith(“\_\_MACOSX/”).
  - If len(members) &gt; get\_max\_extract\_members().
    - Call the validation error handler Platform.throw(translated “Zip file contains more than the maximum allowed {0} files”.format(get\_max\_extract\_members())).
  - Set declared\_total\_size from sum(generator of file.file\_size for file drawn from members).
    - Draw file from members.
  - If declared\_total\_size &gt; max\_extracted\_size.
    - Call the validation error handler Platform.throw(translated “Zip file extracts to more than the maximum allowed size of {0} MB”.format((max\_extracted\_size floor divide 1048576))).
  - Attempt the following.
    - For each file in members.
      - Set filename from os.path.basename(file.filename).
      - Set file\_doc from Platform.new\_doc(“File”).
      - Attempt the following.
        - Set content from z.read(file.filename).
      - On failure (zipfile.BadZipFile).
        - Call the validation error handler Platform.throw(translated “{0} is a not a valid zip file”.format(self.file\_name)).
      - Update total\_extracted\_size using + len(content).
      - If total\_extracted\_size &gt; max\_extracted\_size.
        - Call the validation error handler Platform.throw(translated “Zip file extracts to more than the maximum allowed size of {0} MB”.format((max\_extracted\_size floor divide 1048576))).
      - Set file\_doc.content from content.
      - Set file\_doc.file\_name from filename.
      - Set file\_doc.folder from self.folder.
      - Set file\_doc.is\_private from self.is\_private.
      - Set file\_doc.attached\_to\_doctype from self.attached\_to\_doctype.
      - Set file\_doc.attached\_to\_name from self.attached\_to\_name.
      - Evaluate file\_doc.save().
      - Evaluate files.append(file\_doc).
  - On failure (Exception).
    - For each file\_doc in files.
      - Evaluate Platform.delete\_doc(“File”, file\_doc.name, ignore\_permissions = true, force = true).
    - Propagate the active failure.
- Evaluate Platform.delete\_doc(“File”, self.name).
- Return files.

**Methods declared on this owner** [get full path](operations-054.md#op-187737d314f064).

**Values supplied outside this operation** effective access from self.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L65) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1502)
