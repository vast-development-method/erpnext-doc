# Integrations and service calls · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Code list

[Record definition](../../../../data/record-types/code_list.json)

<a id="op-227e8ca900d383"></a>
### Code List.validate

`operation_enterprise_binding_enterprise_edi_doctype_code_list_code_list_codelist_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_default\_common\_code().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate default common code](operations-002.md#op-76039b981bda87).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1340) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L580)

<a id="op-76039b981bda87"></a>
### Code List.validate default common code

`operation_enterprise_binding_enterprise_edi_doctype_code_list_code_list_codelist_validate_default_common_code`

**Inputs** self.

**Record and data access** read “Common Code” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Default Common Code {0} does not belong to Code List {1}”.format(Platform.bold(self.default\_common\_code), Platform.bold(self.name)).

**Local steps**

- If not self.default\_common\_code.
  - Return no value.
- If Platform.db.get\_value(“Common Code”, self.default\_common\_code, “code\_list”) differs from self.name.
  - Call the validation error handler Platform.throw(translated “Default Common Code {0} does not belong to Code List {1}”.format(Platform.bold(self.default\_common\_code), Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1341) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L581)

<a id="op-c81717384972ce"></a>
### Code List.on trash

`operation_enterprise_edi_record_definitions_code_list_business_behavior_code_list_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.\_\_delete\_linked\_docs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete linked docs](operations-002.md#op-2b38096202828c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L10)

<a id="op-2b38096202828c"></a>
### Code List.delete linked docs

`operation_enterprise_edi_record_definitions_code_list_business_behavior_code_list_delete_linked_records`

**Inputs** self.

**Record and data access** read “Common Code” via get\_all.

**State and service calls** call db\_set on self · request delete\_doc for “Common Code”.

**Local steps**

- Evaluate self.db\_set(“default\_common\_code”, no value).
- Set linked\_docs from Platform.get\_all(“Common Code”, filters = mapping(“code\_list” → self.name), fields = list(“name”)).
- For each doc in linked\_docs.
  - Evaluate Platform.delete\_doc(“Common Code”, doc.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L4960) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L88) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L5)

<a id="op-2168e5f9daf0c5"></a>
### Code List.get codes for

`operation_enterprise_edi_record_definitions_code_list_business_behavior_code_list_get_codes_for`

**Inputs** self, doctype, name.

**Declared result** tuple at str.

**Explicit results** get\_codes\_for(self.name, doctype, name).

**Local steps**

- Return get\_codes\_for(self.name, doctype, name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L5166) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L90) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L7)

<a id="op-7b1fe32dd1a455"></a>
### Code List.get docnames for

`operation_enterprise_edi_record_definitions_code_list_business_behavior_code_list_get_record_names_for`

**Inputs** self, doctype, code.

**Declared result** tuple at str.

**Explicit results** get\_docnames\_for(self.name, doctype, code).

**Local steps**

- Return get\_docnames\_for(self.name, doctype, code).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L5268) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L9)

<a id="op-a79b7bcfe2648e"></a>
### Code List.get default code

`operation_enterprise_edi_record_definitions_code_list_business_behavior_code_list_get_default_code`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Common Code” via get\_value.

**Explicit results** Platform.db.get\_value(“Common Code”, self.default\_common\_code, “common\_code”) when self.default\_common\_code, otherwise no value.

**Local steps**

- Return Platform.db.get\_value(“Common Code”, self.default\_common\_code, “common\_code”) when self.default\_common\_code, otherwise no value.
  - Value choice on self.default\_common\_code — true gives Platform.db.get\_value(“Common Code”, self.default\_common\_code, “common\_code”), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L5370) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L8)

<a id="op-bc1d37c40f6c8f"></a>
### Code List.from genericode

`operation_enterprise_edi_record_definitions_code_list_business_behavior_code_list_from_genericode`

**Inputs** self, root.

**Local steps**

- Set self.title from escape\_html(get\_required\_text(root, “.//Identification/ShortName”)).
- Set self.version from get\_required\_text(root, “.//Identification/Version”).
- Set self.canonical\_uri from get\_required\_text(root, “.//CanonicalUri”).
- Set self.description from escape\_html(getattr(root.find(“.//Identification/LongName”), “text”, no value)).
- Set self.publisher from escape\_html(getattr(root.find(“.//Identification/Agency/ShortName”), “text”, no value)).
- If not self.publisher.
  - Set self.publisher from escape\_html(getattr(root.find(“.//Identification/Agency/LongName”), “text”, no value)).
- Set self.publisher\_id from getattr(root.find(“.//Identification/Agency/Identifier”), “text”, no value).
- Set self.url from getattr(root.find(“.//Identification/LocationUri”), “text”, no value).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(root.find(“.//Identification/LongName”), “text”, no value), getattr(root.find(“.//Identification/Agency/ShortName”), “text”, no value) and 3 further calls.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L89) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L6)

<a id="op-a92419833d3091"></a>
### Get required text

`operation_enterprise_binding_enterprise_edi_doctype_code_list_code_list_get_required_text`

**Inputs** root, path.

**Declared result** (str bitwise or no value).

**Explicit results** element.text.

**Explicit failure paths** validation helper — translated “The uploaded genericode file has no {0} element.”.format(path.split(“/”) at negative 1).

**Local steps**

- Set element from root.find(path).
- If element is identical to no value.
  - Call the validation error handler Platform.throw(translated “The uploaded genericode file has no {0} element.”.format(path.split(“/”) at negative 1), title = translated “Parsing Error”).
- Return element.text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1342) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L582)

<a id="op-1dc4f0f0171a74"></a>
### Version key

`operation_enterprise_edi_record_definitions_code_list_business_behavior_version_key`

**Inputs** version.

**Declared result** list.

**Explicit results** list of int(p) when p.isdigit(), otherwise p for p drawn from re.split(“(\\d+)”, (version or empty text)).

**Local steps**

- Return list of int(p) when p.isdigit(), otherwise p for p drawn from re.split(“(\\d+)”, (version or empty text)).
  - Draw p from re.split(“(\\d+)”, (version or empty text)).
  - Value choice on p.isdigit() — true gives int(p), false gives p.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in version → empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L5952) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L98) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L15)

<a id="op-8745bed52f3ce8"></a>
### Resolve code list

`operation_enterprise_edi_record_definitions_code_list_business_behavior_resolve_code_list`

**Inputs** code\_list.

**Wrappers, in declaration order** Platform.request\_cache.

**Declared result** (str bitwise or no value).

**Record and data access** read “Code List” via exists · read “Code List” via get\_all.

**Explicit results** code\_list · no value · max(candidates, key = deferred anonymous expression).name.

**Local steps**

- If Platform.db.exists(“Code List”, code\_list).
  - Return code\_list.
- Set candidates from Platform.get\_all(“Code List”, filters = mapping(“canonical\_uri” → code\_list), fields = list(“name”, “version”)).
- If not candidates.
  - Return no value.
- Return max(candidates, key = deferred anonymous expression).name.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L6087) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L97) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L14)

<a id="op-27e639861d05c2"></a>
### Get codes for

`operation_enterprise_edi_record_definitions_code_list_business_behavior_get_codes_for`

**Inputs** code\_list, doctype, name.

**Declared result** tuple at str.

**Explicit results** tuple() · tuple(generator of c at 0 for c drawn from codes) when codes, otherwise tuple().

**Local steps**

- If not code\_list bound to resolve\_code\_list(code\_list).
  - Return tuple().
- Set CommonCode from Platform.qb.DocType(“Common Code”).
- Set DynamicLink from Platform.qb.DocType(“Dynamic Link”).
- Set codes from nested operand in the contract(nested operand in the contract).distinct().orderby(CommonCode.common\_code).run().
- Return tuple(generator of c at 0 for c drawn from codes) when codes, otherwise tuple().
  - Value choice on codes — true gives tuple(generator of c at 0 for c drawn from codes), false gives tuple().
  - Draw c from codes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L6365) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L94) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L11)

<a id="op-1e7a4df9cf74bb"></a>
### Get docnames for

`operation_enterprise_edi_record_definitions_code_list_business_behavior_get_record_names_for`

**Inputs** code\_list, doctype, code.

**Declared result** tuple at str.

**Explicit results** tuple() · tuple(generator of d at 0 for d drawn from docnames) when docnames, otherwise tuple().

**Local steps**

- If not code\_list bound to resolve\_code\_list(code\_list).
  - Return tuple().
- Set CommonCode from Platform.qb.DocType(“Common Code”).
- Set DynamicLink from Platform.qb.DocType(“Dynamic Link”).
- Set docnames from nested operand in the contract(nested operand in the contract).distinct().orderby(DynamicLink.idx).run().
- Return tuple(generator of d at 0 for d drawn from docnames) when docnames, otherwise tuple().
  - Value choice on docnames — true gives tuple(generator of d at 0 for d drawn from docnames), false gives tuple().
  - Draw d from docnames.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L155) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L96) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L13)

<a id="op-64acb6776d213f"></a>
### Get default code

`operation_enterprise_edi_record_definitions_code_list_business_behavior_get_default_code`

**Inputs** code\_list.

**Declared result** (str bitwise or no value).

**Record and data access** read “Code List” via get\_value · read “Common Code” via get\_value.

**Explicit results** no value · Platform.db.get\_value(“Common Code”, code\_id, “common\_code”) when code\_id, otherwise no value.

**Local steps**

- If not code\_list bound to resolve\_code\_list(code\_list).
  - Return no value.
- Set code\_id from Platform.db.get\_value(“Code List”, code\_list, “default\_common\_code”).
- Return Platform.db.get\_value(“Common Code”, code\_id, “common\_code”) when code\_id, otherwise no value.
  - Value choice on code\_id — true gives Platform.db.get\_value(“Common Code”, code\_id, “common\_code”), false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0445.json#L513) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L95) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L12)

<a id="op-8294f7f788cb66"></a>
### Import genericode

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_import_genericode`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** import\_genericode\_content(doctype = “Code List”, docname = Platform.form\_dict.docname, content = content, file\_name = file\_name).

**Explicit failure paths** validation helper — translated “Importing Code Lists from remote URLs is not allowed.” · validation helper — translated “The uploaded file does not match the selected Code List.” · validation helper — translated “The uploaded file could not be parsed as a genericode XML document.”.

**Local steps**

- Evaluate Platform.has\_permission(“Code List”, “create”, throw = true).
- Attempt the following.
  - Set tuple(content, file\_name) from get\_uploaded\_genericode\_file().
  - Return import\_genericode\_content(doctype = “Code List”, docname = Platform.form\_dict.docname, content = content, file\_name = file\_name).
- On failure (RemoteGenericodeUrlNotAllowedError).
  - Call the validation error handler Platform.throw(translated “Importing Code Lists from remote URLs is not allowed.”, title = translated “Invalid Upload”).
- On failure (CodeListSelectionMismatchError).
  - Call the validation error handler Platform.throw(translated “The uploaded file does not match the selected Code List.”).
- On failure (etree.XMLSyntaxError).
  - Call the validation error handler Platform.throw(translated “The uploaded file could not be parsed as a genericode XML document.”, title = translated “Parsing Error”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Code List”, “create”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L156) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L102) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L19)

<a id="op-986044bb24c342"></a>
### Import genericode from url

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_import_genericode_from_resource_address`

**Inputs** url, doctype = “Code List”, docname = no value.

**Explicit results** import\_genericode\_content(doctype = doctype, docname = docname, content = content, file\_name = file\_name).

**Local steps**

- Set content from fetch\_genericode\_from\_url(url).
- Set file\_name from (urlsplit(url).path.rsplit(“/”, 1) at negative 1 or DEFAULT\_FILE\_NAME).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in urlsplit(url).path.rsplit(“/”, 1) at negative 1 → DEFAULT\_FILE\_NAME.
- Return import\_genericode\_content(doctype = doctype, docname = docname, content = content, file\_name = file\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L158) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L21)

<a id="op-961bcf22f8a273"></a>
### Get uploaded genericode file

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_get_uploaded_genericode_file`

**Inputs** no declared parameters.

**Declared result** tuple at tuple(bytes, (str bitwise or no value)).

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** tuple(uploaded\_data, file\_name) · tuple(file\_doc.get\_content(encodings = tuple()), file\_name).

**Explicit failure paths** Platform.ValidationError(translated “No file uploaded or URL provided.”) · RemoteGenericodeUrlNotAllowedError.

**Local steps**

- Set uploaded\_data from Platform.local.uploaded\_file.
- Set file\_name from Platform.local.uploaded\_filename.
- If (uploaded\_data and file\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in uploaded\_data → file\_name.
  - Return tuple(uploaded\_data, file\_name).
- Set file\_url from Platform.local.uploaded\_file\_url.
- If not file\_url.
  - Raise Platform.ValidationError(translated “No file uploaded or URL provided.”).
- If not is\_local\_file\_url(file\_url).
  - Raise RemoteGenericodeUrlNotAllowedError.
- Set file\_doc from Platform.get\_doc(“File”, mapping(“file\_url” → file\_url)).
- Evaluate file\_doc.check\_permission(“read”).
- Return tuple(file\_doc.get\_content(encodings = tuple()), file\_name).

**Values supplied outside this operation** effective access from file\_doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0445.json#L1288) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L101) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L18)

<a id="op-10691a49a2f8a8"></a>
### Is local file url

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_is_local_file_resource_address`

**Inputs** file\_url.

**Declared result** bool.

**Explicit results** false · (not parsed.scheme and not parsed.netloc and parsed.path.startswith(LOCAL\_FILE\_PREFIXES)).

**Local steps**

- If not file\_url.
  - Return false.
- Set parsed from urlsplit(file\_url.strip()).
- Return (not parsed.scheme and not parsed.netloc and parsed.path.startswith(LOCAL\_FILE\_PREFIXES)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not parsed.scheme → not parsed.netloc → parsed.path.startswith(LOCAL\_FILE\_PREFIXES).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0445.json#L1652) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L22)

<a id="op-eda4f4225701f3"></a>
### Fetch genericode from url

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_fetch_genericode_from_resource_address`

**Inputs** url.

**Declared result** bytes.

**Explicit results** response.content.

**Local steps**

- Set response from requests.get(url, timeout = GENERICODE\_FETCH\_TIMEOUT).
- Evaluate response.raise\_for\_status().
- Return response.content.

**Values supplied outside this operation** service or queued work from requests.get(url, timeout = GENERICODE\_FETCH\_TIMEOUT).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0445.json#L1812) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L99) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L16)

<a id="op-cc6e8897760458"></a>
### Import genericode content

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_import_genericode_content`

**Inputs** doctype, docname, content, file\_name.

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc.

**State and service calls** request new\_doc for doctype · call save on code\_list.

**Explicit results** mapping(“code\_list” → code\_list.name, “code\_list\_title” → code\_list.title, “file” → file\_doc.name, “columns” → columns, …).

**Explicit failure paths** CodeListSelectionMismatchError.

**Local steps**

- Set root from parse\_genericode\_content(content).
- Set name from get\_required\_text(root, “.//CanonicalVersionUri”).
- Set docname from (docname or name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in docname → name.
- If Platform.db.exists(doctype, docname).
  - Set code\_list from Platform.get\_doc(doctype, docname).
  - If code\_list.name differs from name.
    - Raise CodeListSelectionMismatchError.
- Otherwise.
  - Set code\_list from Platform.new\_doc(doctype).
  - Set code\_list.name from name.
- Evaluate code\_list.from\_genericode(root).
- Evaluate code\_list.save().
- Set file\_doc from save\_file(fname = (get\_safe\_file\_name((file\_name or empty text)).lstrip(“.”) or DEFAULT\_FILE\_NAME), content = content, dt = doctype, dn = code\_list.name, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_safe\_file\_name((file\_name or empty text)).lstrip(“.”) → DEFAULT\_FILE\_NAME.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in file\_name → empty text.
- Set tuple(columns, example\_values, filterable\_columns) from get\_genericode\_columns\_and\_examples(root).
- Return mapping(“code\_list” → code\_list.name, “code\_list\_title” → code\_list.title, “file” → file\_doc.name, “columns” → columns, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L157) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L20)

<a id="op-9114a3e53cc5ea"></a>
### Parse genericode content

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_parse_genericode_content`

**Inputs** content.

**Explicit results** etree.fromstring(content, parser = parser).

**Local steps**

- Set parser from etree.XMLParser(remove\_blank\_text = true, resolve\_entities = false, load\_dtd = false, no\_network = true).
- Return etree.fromstring(content, parser = parser).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0445.json#L2511) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L23)

<a id="op-604028ccdf2dc2"></a>
### Process genericode import

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_process_genericode_import`

**Inputs** code\_list\_name, file\_name, code\_column, title\_column = no value, description\_column = no value, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit results** import\_genericode(code\_list\_name, file\_name, column\_map, filters).

**Local steps**

- Bind dependencies import\_genericode.
- Evaluate Platform.has\_permission(“Common Code”, “create”, throw = true).
- Evaluate Platform.has\_permission(“Code List”, doc = code\_list\_name, throw = true).
- Set column\_map from mapping(“code” → unescape(code\_column), “title” → unescape(title\_column) when title\_column, otherwise no value, “description” → unescape(description\_column) when description\_column, otherwise no value).
  - Value choice on title\_column — true gives unescape(title\_column), false gives no value.
  - Value choice on description\_column — true gives unescape(description\_column), false gives no value.
- Set filters from mapping of unescape(column) → unescape(str(value)) for tuple(column, value) drawn from Platform.parse\_json((filters or mapping())).items().
  - Draw tuple(column, value) from Platform.parse\_json((filters or mapping())).items().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Return import\_genericode(code\_list\_name, file\_name, column\_map, filters).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Common Code”, “create”, throw = true), Platform.has\_permission(“Code List”, doc = code\_list\_name, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L159) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L24)

<a id="op-fdeaa86b494888"></a>
### Get genericode columns and examples

`operation_enterprise_edi_record_definitions_code_list_code_list_import_business_behavior_get_genericode_columns_and_examples`

**Inputs** root.

**Explicit results** tuple(columns, example\_values, filterable\_columns).

**Local steps**

- Set columns from list().
- Set example\_values from mapping().
- Set filterable\_columns from mapping().
- For each column in root.findall(“.//Column”).
  - Set column\_id from escape\_html(column.get(“Id”)).
  - Evaluate columns.append(column\_id).
  - Set example\_values at column\_id from list().
  - Set filterable\_columns at column\_id from set().
- For each row in root.findall(“.//SimpleCodeList/Row”).
  - For each value in row.findall(“Value”).
    - Set column\_id from escape\_html(value.get(“ColumnRef”)).
    - If column\_id does not belong to columns.
      - Evaluate columns.append(column\_id).
      - Set example\_values at column\_id from list().
      - Set filterable\_columns at column\_id from set().
    - Set simple\_value from value.find(“./SimpleValue”).
    - If simple\_value is identical to no value.
      - Continue with the next iteration or loop test.
    - Evaluate filterable\_columns at column\_id.add(escape\_html(simple\_value.text)).
- For each row in root.findall(“.//SimpleCodeList/Row”) at slice no value to 3.
  - For each value in row.findall(“Value”).
    - Set column\_id from value.get(“ColumnRef”).
    - Set simple\_value from value.find(“./SimpleValue”).
    - If simple\_value is identical to no value.
      - Continue with the next iteration or loop test.
    - Evaluate example\_values at column\_id.append(escape\_html(simple\_value.text)).
- Set filterable\_columns from mapping of k → list(v) for tuple(k, v) drawn from filterable\_columns.items() where len(v) ≤ 5.
  - Draw tuple(k, v) from filterable\_columns.items(), keep a combination only if (len(v) ≤ 5).
- Return tuple(columns, example\_values, filterable\_columns).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0445.json#L2928) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L100) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L17)

## Record · Common code

[Record definition](../../../../data/record-types/common_code.json)

<a id="op-a42ae3b49e6007"></a>
### Common Code.validate

`operation_enterprise_edi_record_definitions_common_code_business_behavior_common_code_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_distinct\_references().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate distinct references](operations-003.md#op-0511b8c85479ca).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L1110) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L126) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L42)
