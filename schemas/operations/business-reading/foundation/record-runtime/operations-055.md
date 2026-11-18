# Record lifecycle and persistence · operations 55

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · File

[Record definition](../../../../data/record-types/file.json)

<a id="op-98ed8911f8abe0"></a>
### Get user permission field conditions

`operation_foundation_binding_foundation_core_doctype_file_file_get_user_permission_field_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, user\_permissions, strict\_user\_permissions.

**Explicit result forms** a value selected from the current context.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L172) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L630)

<a id="op-10b5876a8b37a9"></a>
### Make home folder

`operation_foundation_core_record_definitions_file_utils_business_behavior_make_home_folder`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “is\_folder” → 1, “is\_home\_folder” → 1, “file\_name” → “Home”) via get\_doc · resolve a document from mapping(“doctype” → “File”, “folder” → home.name, “is\_folder” → 1, “is\_attachments\_folder” → 1, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “File”, “is\_folder” → 1, “is\_home\_folder” → 1, “file\_name” → “Home”)) · call insert on Platform.get\_doc(mapping(“doctype” → “File”, “folder” → home.name, “is\_folder” → 1, “is\_attachments\_folder” → 1, …)).

**Local steps**

- Set home from Platform.get\_doc(mapping(“doctype” → “File”, “is\_folder” → 1, “is\_home\_folder” → 1, “file\_name” → “Home”)).insert(ignore\_if\_duplicate = true).
- Evaluate Platform.get\_doc(mapping(“doctype” → “File”, “folder” → home.name, “is\_folder” → 1, “is\_attachments\_folder” → 1, …)).insert(ignore\_if\_duplicate = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0084.json#L6600) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1618)

<a id="op-4c7910a331e891"></a>
### Setup folder path

`operation_foundation_core_record_definitions_file_utils_business_behavior_setup_folder_path`

**Inputs** filename, new\_parent.

**Declared result** no value.

**Record and data access** resolve a document from “File” via get\_doc.

**State and service calls** call save on file.

**Local steps**

- Set file from Platform.get\_doc(“File”, filename).
- Set file.folder from new\_parent.
- Evaluate file.save().
- If file.is\_folder.
  - Bind dependencies rename\_doc.
  - Evaluate rename\_doc(“File”, file.name, file.get\_name\_based\_on\_parent\_folder(), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0084.json#L6877) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1622)

<a id="op-461b91bc3a0bdb"></a>
### Get extension

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_extension`

**Inputs** filename, extn = no value, content = no value, response = no value.

**Declared result** str.

**Explicit results** \_extn at slice 1 to no value · extn.

**Local steps**

- Set mimetype from no value.
- If response.
  - Set content\_type from response.headers.get(“Content-Type”).
  - If content\_type.
    - Set \_extn from mimetypes.guess\_extension(content\_type).
    - If \_extn.
      - Return \_extn at slice 1 to no value.
- If extn.
  - If “?” belongs to extn.
    - Set extn from extn.split(“?”, 1) at 0.
  - Set mimetype from mimetypes.guess\_type(((filename + “.”) + extn)) at 0.
- If (mimetype is identical to no value and extn is identical to no value and content).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in mimetype is identical to no value → extn is identical to no value → content.
  - Set \_type\_info from filetype.match(content).
  - If \_type\_info.
    - Set extn from \_type\_info.extension.
- Return extn.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0084.json#L7081) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1611)

<a id="op-031da56f9a006c"></a>
### Get local image

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_local_image`

**Inputs** file\_url.

**Declared result** tuple at tuple(“ImageFile”, str, str).

**Explicit results** tuple(image, filename, extn).

**Explicit failure paths** validation helper — translated “Unable to read file format for {0}”.format(file\_url).

**Local steps**

- Bind dependencies Image.
- If file\_url.startswith(“/private”).
  - Set file\_url\_path from tuple(file\_url.lstrip(“/”)).
- Otherwise.
  - Set file\_url\_path from tuple(“public”, file\_url.lstrip(“/”)).
- Set file\_path from Platform.get\_site\_path(expanded file\_url\_path).
- Attempt the following.
  - Set image from Image.open(file\_path).
- On failure (OSError).
  - Call the validation error handler Platform.throw(translated “Unable to read file format for {0}”.format(file\_url)).
- Set content from no value.
- Attempt the following.
  - Set tuple(filename, extn) from file\_url.rsplit(“.”, 1).
- On failure (ValueError).
  - Within open(file\_path) bound as f.
    - Set content from f.read().
  - Set filename from file\_url.
  - Set extn from no value.
- Set extn from get\_extension(filename, extn, content).
- Return tuple(image, filename, extn).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1613)

<a id="op-a70132eec0ae9b"></a>
### Get web image

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_web_image`

**Inputs** file\_url.

**Declared result** tuple at tuple(“ImageFile”, str, str).

**State and service calls** msgprint with translated “File '{0}' not found”.format(file\_url) · msgprint with translated “Unable to read file format for {0}”.format(file\_url) · msgprint with translated “Image link '{0}' is not valid”.format(file\_url).

**Explicit results** tuple(image, filename, extn).

**Explicit failure paths** validation helper — translated “Too many redirects while fetching {0}”.format(file\_url) · propagate active failure.

**Local steps**

- Bind dependencies requests.
- Bind dependencies requests.exceptions.
- Bind dependencies validate\_egress\_url.
- Bind dependencies Image.
- Set file\_url from Platform.utils.get\_url(file\_url).
- Set site\_url from Platform.utils.get\_url().rstrip(“/”).
- Bind local operation validate\_external\_url for subsequent calls.
- Evaluate validate\_external\_url(file\_url).
- For each \_attempt in range((MAX\_WEB\_IMAGE\_REDIRECTS + 1)).
  - Set r from requests.get(file\_url, stream = true, allow\_redirects = false).
  - If not r.is\_redirect.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - Set file\_url from urljoin(file\_url, r.headers at “Location”).
  - Evaluate validate\_external\_url(file\_url).
- After normal loop exhaustion.
  - Call the validation error handler Platform.throw(translated “Too many redirects while fetching {0}”.format(file\_url)).
- Attempt the following.
  - Evaluate r.raise\_for\_status().
- On failure (requests.exceptions.HTTPError) bound to e.
  - If “404” belongs to e.args at 0.
    - Evaluate Platform.msgprint(translated “File '{0}' not found”.format(file\_url)).
  - Otherwise.
    - Evaluate Platform.msgprint(translated “Unable to read file format for {0}”.format(file\_url)).
  - Propagate the active failure.
- Attempt the following.
  - Set image from Image.open(BytesIO(r.content)).
- On failure (Exception) bound to e.
  - Evaluate Platform.msgprint(translated “Image link '{0}' is not valid”.format(file\_url), raise\_exception = e).
- Attempt the following.
  - Set tuple(filename, extn) from file\_url.rsplit(“/”, 1) at 1.rsplit(“.”, 1).
- On failure (ValueError).
  - Set filename from get\_random\_filename().
  - Set extn from no value.
- Set extn from get\_extension(filename, extn, r.content).
- Set filename from (“/files/” + strip(unquote(filename))).
- Return tuple(image, filename, extn).

**Values supplied outside this operation** service or queued work from requests.get(file\_url, stream = true, allow\_redirects = false).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L75) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1616)

<a id="op-9351a7447fd2c9"></a>
### Get web image.validate external url

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_web_image_validate_external_resource_address`

**Inputs** url.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot fetch image from {0}: {1}”.format(url, str(e)).

**Local steps**

- If (url equals site\_url or url.startswith((site\_url + “/”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in url equals site\_url → url.startswith((site\_url + “/”)).
  - Return no value.
- Attempt the following.
  - Evaluate validate\_egress\_url(url).
- On failure (ValueError) bound to e.
  - Call the validation error handler Platform.throw(translated “Cannot fetch image from {0}: {1}”.format(url, str(e))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L76) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1617)

<a id="op-33c7db34fd4957"></a>
### Delete file

`operation_foundation_core_record_definitions_file_utils_business_behavior_delete_file`

**Inputs** path.

**Declared result** no value.

**Explicit failure paths** validation helper — translated “It is risky to delete this file: {0}. Please contact your System Manager.”.format(path).

**Local steps**

- If path.
  - If “..” belongs to path.split(“/”).
    - Call the validation error handler Platform.throw(translated “It is risky to delete this file: {0}. Please contact your System Manager.”.format(path)).
  - Set parts from os.path.split(path.strip(“/”)).
  - If parts at 0 equals “files”.
    - Set path from Platform.utils.get\_site\_path(“public”, “files”, parts at negative 1).
  - Otherwise.
    - Set path from Platform.utils.get\_site\_path(“private”, “files”, parts at negative 1).
  - Set path from encode(path).
  - If os.path.exists(path).
    - Evaluate os.remove(path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L1874) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1603)

<a id="op-0535d143e44351"></a>
### Remove file by url

`operation_foundation_core_record_definitions_file_utils_business_behavior_remove_file_by_resource_address`

**Inputs** file\_url, doctype = no value, name = no value.

**Declared result** “Document”.

**Record and data access** read “File” via get\_value.

**Explicit results** remove\_file(fid = fid).

**Local steps**

- If (doctype and name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name.
  - Set fid from Platform.db.get\_value(“File”, mapping(“file\_url” → file\_url, “attached\_to\_doctype” → doctype, “attached\_to\_name” → name)).
- Otherwise.
  - Set fid from Platform.db.get\_value(“File”, mapping(“file\_url” → file\_url)).
- If fid.
  - Bind dependencies remove\_file.
  - Return remove\_file(fid = fid).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L2290) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1621)

<a id="op-90715797723afe"></a>
### Get content hash

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_content_hash`

**Inputs** content.

**Declared result** str.

**Explicit results** hashlib.md5(content, usedforsecurity = false).hexdigest().

**Local steps**

- If isinstance(content, str).
  - Set content from content.encode().
- Return hashlib.md5(content, usedforsecurity = false).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L2591) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1609)

<a id="op-83c171882bd77b"></a>
### Generate file name

`operation_foundation_core_record_definitions_file_utils_business_behavior_generate_file_name`

**Inputs** name, suffix = no value, is\_private = false.

**Declared result** str.

**Explicit results** name · generate\_file\_name(name, is\_private = is\_private) · candidate\_path.

**Local steps**

- Bind local operation path\_exists for subsequent calls.
- If not path\_exists(name, is\_private).
  - Return name.
- Set candidate\_path from get\_file\_name(name, suffix).
- If path\_exists(candidate\_path, is\_private).
  - Return generate\_file\_name(name, is\_private = is\_private).
- Return candidate\_path.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L74) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1608)

<a id="op-eab76c0363f113"></a>
### Generate file name.path exists

`operation_foundation_binding_foundation_core_doctype_file_utils_generate_file_name_path_exists`

**Inputs** name, is\_private.

**Explicit results** os.path.exists(encode(get\_files\_path(name, is\_private = is\_private))).

**Local steps**

- Return os.path.exists(encode(get\_files\_path(name, is\_private = is\_private))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L176) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L634)

<a id="op-0ac38565640db2"></a>
### Get file name

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_file_name`

**Inputs** fname, optional\_suffix = no value.

**Declared result** str.

**Explicit results** formatted text {partial}{suffix}{extn}.

**Local steps**

- Set fname from cstr(fname).
- Set tuple(partial, extn) from os.path.splitext(fname).
- Set suffix from (optional\_suffix or Platform.generate\_hash(length = 6)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in optional\_suffix → Platform.generate\_hash(length = 6).
- Return formatted text {partial}{suffix}{extn}.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 6).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L3394) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1612)

<a id="op-4f92906c2a92f8"></a>
### Extract images from doc

`operation_foundation_core_record_definitions_file_utils_business_behavior_extract_images_from_record`

**Inputs** doc, fieldname, is\_private = true.

**Local steps**

- Set content from doc.get(fieldname).
- If doc.meta.make\_attachments\_public.
  - Set is\_private from false.
- Set content from extract\_images\_from\_html(doc, content, is\_private = is\_private).
- If Platform.flags.has\_dataurl.
  - Evaluate doc.set(fieldname, content).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L3613) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1606)

<a id="op-2e2d6411155cd3"></a>
### Extract images from html

`operation_foundation_core_record_definitions_file_utils_business_behavior_extract_images_from_document_markup`

**Inputs** doc, content, is\_private = false.

**Explicit results** content.

**Local steps**

- Set Platform.flags.has\_dataurl from false.
- Bind local operation \_save\_file for subsequent calls.
- If (content and isinstance(content, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in content → isinstance(content, str).
  - Set content from re.sub(text in the contract, \_save\_file, content).
- Return content.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L3823) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1604)

<a id="op-85098997f78614"></a>
### Extract images from html.save file

`operation_foundation_core_record_definitions_file_utils_business_behavior_extract_images_from_document_markup_save_file`

**Inputs** match.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → name, …) via get\_doc.

**State and service calls** call save on \_file.

**Explicit results** match.group(0) · formatted text &lt;img src="#broken-image" alt="{get\_corrupted\_image\_msg()}" · formatted text &lt;img src="{file\_url}".

**Local steps**

- Set data from match.group(1).split(“data:”) at 1.
- Set tuple(headers, content) from data.split(“,”).
- Set mtype from headers.split(“;”, 1) at 0.
- If isinstance(content, str).
  - Set content from content.encode(“utf-8”).
- If byte value belongs to content.
  - Set content from content.split(byte value) at 1.
- If not content.
  - Return match.group(0).
- Attempt the following.
  - Set content from safe\_b64decode(content).
- On failure (BinasciiError).
  - Set Platform.flags.has\_dataurl from true.
  - Return formatted text &lt;img src="#broken-image" alt="{get\_corrupted\_image\_msg()}".
- If “filename=” belongs to headers.
  - Set filename from headers.split(“filename=”) at negative 1.
  - Set filename from safe\_decode(filename).split(“;”, 1) at 0.
- Otherwise.
  - Set filename from get\_random\_filename(content\_type = mtype).
- If doc.meta.istable.
  - Set doctype from doc.parenttype.
  - Set name from doc.parent.
- Otherwise.
  - Set doctype from doc.doctype.
  - Set name from doc.name.
- Set \_file from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → filename, “attached\_to\_doctype” → doctype, “attached\_to\_name” → name, …)).
- Evaluate \_file.save(ignore\_permissions = true).
- Set file\_url from \_file.unique\_url.
- Set Platform.flags.has\_dataurl from true.
- Return formatted text &lt;img src="{file\_url}".

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L4871) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1605)

<a id="op-4193acbf5b18c8"></a>
### Get corrupted image msg

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_corrupted_image_message`

**Inputs** no declared parameters.

**Explicit results** translated “Image: Corrupted Data Stream”.

**Local steps**

- Return translated “Image: Corrupted Data Stream”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L5766) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1610)

<a id="op-4bbb8dc7d54a00"></a>
### Get random filename

`operation_foundation_core_record_definitions_file_utils_business_behavior_get_random_filename`

**Inputs** content\_type = no value.

**Declared result** str.

**Explicit results** (random\_string(7) + (extn or empty text)).

**Local steps**

- Set extn from no value.
- If content\_type.
  - Set extn from mimetypes.guess\_extension(content\_type).
- Return (random\_string(7) + (extn or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extn → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L5810) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1614)

<a id="op-13e52d46bd4d28"></a>
### Update existing file docs

`operation_foundation_core_record_definitions_file_utils_business_behavior_update_existing_file_records`

**Inputs** doc.

**Declared result** no value.

**Local steps**

- Set file\_doctype from Platform.qb.DocType(“File”).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.content\_hash equals nested operand in the contract.content\_hash).where(fi ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0085.json#L5950) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1623)

<a id="op-3ae71b89eb546d"></a>
### Attach files to document

`operation_foundation_core_record_definitions_file_utils_business_behavior_attach_files_to_document`

**Inputs** doc, event.

**Declared result** no value.

**Record and data access** read “File” via exists · resolve a document from “File” via get\_doc.

**State and service calls** request set\_value on “File” · call insert on file.

**Local steps**

- Set attach\_fields from doc.meta.get(“fields”, mapping(“fieldtype” → list(“in”, list(“Attach”, “Attach Image”)))).
- For each df in attach\_fields.
  - If not doc.has\_value\_changed(df.fieldname).
    - Continue with the next iteration or loop test.
  - Set value from doc.get(df.fieldname).
  - If not (value or empty text).startswith(tuple(“/files”, “/private/files”, text in the contract, text in the contract)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in value → empty text.
    - Continue with the next iteration or loop test.
  - If Platform.db.exists(“File”, mapping(“file\_url” → value, “attached\_to\_name” → doc.name, “attached\_to\_doctype” → doc.doctype, “attached\_to\_field” → df.fieldname)).
    - Continue with the next iteration or loop test.
  - Set unattached\_file from Platform.db.exists(“File”, mapping(“file\_url” → value, “attached\_to\_name” → no value, “attached\_to\_doctype” → no value, “attached\_to\_field” → no value, …)).
  - If unattached\_file.
    - Evaluate Platform.db.set\_value(“File”, unattached\_file, field = mapping(“attached\_to\_name” → doc.name, “attached\_to\_doctype” → doc.doctype, “attached\_to\_field” → df.fieldname, “is\_private” → cint(value.startswith(“ ….
    - Continue with the next iteration or loop test.
  - Set file from Platform.get\_doc(doctype = “File”, file\_url = value, attached\_to\_name = doc.name, attached\_to\_doctype = doc.doctype, …).
  - Set messages from len(Platform.local.message\_log).
  - Attempt the following.
    - Evaluate file.insert(ignore\_permissions = true).
  - On failure (Exception).
    - Remove Platform.local.message\_log at slice messages to no value.
    - Evaluate doc.log\_error(“Error Attaching File”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L73) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1600)

<a id="op-14c6c8ce67c405"></a>
### Relink files

`operation_foundation_core_record_definitions_file_utils_business_behavior_relink_files`

**Inputs** doc, fieldname, temp\_doc\_name.

**Record and data access** read “File” via get\_value.

**State and service calls** request set\_value on “File”.

**Explicit results** no value.

**Local steps**

- If not temp\_doc\_name.
  - Return no value.
- Bind dependencies add\_to\_date, now\_datetime.
- Set mislinked\_file from Platform.db.get\_value(“File”, mapping(“file\_url” → doc.get(fieldname), “attached\_to\_name” → temp\_doc\_name, “attached\_to\_doctype” → doc.doctype, “attached\_to\_field” → fieldname, …)).
- If mislinked\_file.
  - Evaluate Platform.db.set\_value(“File”, mislinked\_file, field = mapping(“attached\_to\_name” → doc.name)).
  - Return no value.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L1196) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1619)

<a id="op-4dc739e8aa1d01"></a>
### Relink mismatched files

`operation_foundation_core_record_definitions_file_utils_business_behavior_relink_mismatched_files`

**Inputs** doc.

**Declared result** no value.

**State and service calls** request set\_value on “File”.

**Explicit results** no value.

**Local steps**

- If not doc.get(“\_\_temporary\_name”, no value).
  - Return no value.
- Set attach\_fields from doc.meta.get(“fields”, mapping(“fieldtype” → list(“in”, list(“Attach”, “Attach Image”)))).
- For each df in attach\_fields.
  - If doc.get(df.fieldname).
    - Evaluate relink\_files(doc, df.fieldname, doc.\_\_temporary\_name).
- Set table\_fields from doc.meta.get(“fields”, mapping(“fieldtype” → “Table”)).
- For each table\_df in table\_fields.
  - Set child\_rows from (doc.get(table\_df.fieldname) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(table\_df.fieldname) → list().
  - If not child\_rows.
    - Continue with the next iteration or loop test.
  - Set child\_meta from Platform.get\_meta(table\_df.options).
  - Set child\_attach\_fields from child\_meta.get(“fields”, mapping(“fieldtype” → list(“in”, list(“Attach”, “Attach Image”)))).
  - If not child\_attach\_fields.
    - Continue with the next iteration or loop test.
  - For each child\_row in child\_rows.
    - For each child\_df in child\_attach\_fields.
      - Set file\_url from child\_row.get(child\_df.fieldname).
      - If file\_url.
        - Evaluate Platform.db.set\_value(“File”, mapping(“file\_url” → file\_url, “attached\_to\_name” → doc.\_\_temporary\_name), mapping(“attached\_to\_name” → doc.name)).
- Evaluate doc.delete\_key(“\_\_temporary\_name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L1564) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1620)

<a id="op-3485b88bcf80f3"></a>
### Decode file content

`operation_foundation_core_record_definitions_file_utils_business_behavior_decode_file_content`

**Inputs** content.

**Declared result** bytes.

**Explicit results** safe\_b64decode(content).

**Local steps**

- If isinstance(content, str).
  - Set content from content.encode(“utf-8”).
- If byte value belongs to content.
  - Set content from content.split(byte value) at 1.
- Return safe\_b64decode(content).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L2252) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1602)

<a id="op-d9ff87fcabfdf8"></a>
### Find file by url

`operation_foundation_core_record_definitions_file_utils_business_behavior_find_file_by_resource_address`

**Inputs** path, name = no value.

**Declared result** (“File” bitwise or no value).

**Record and data access** read “File” via get\_all · resolve a document from “File” via get\_doc.

**Explicit results** file.

**Local steps**

- Set filters from mapping(“file\_url” → str(path)).
- If name.
  - Set filters at “name” from str(name).
- Set files from Platform.get\_all(“File”, filters = filters, fields = “\*”).
- For each file\_data in files.
  - Set file from Platform.get\_doc(doctype = “File”, expanded names file\_data).
  - If file.is\_downloadable().
    - Return file.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L2429) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1607)
