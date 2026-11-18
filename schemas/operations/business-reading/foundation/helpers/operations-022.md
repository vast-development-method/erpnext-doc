# Shared value and file services · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · File manager

<a id="op-e8f329f2bc6199"></a>
### Get file data from hash

`operation_foundation_utils_file_manager_business_behavior_get_file_data_from_hash`

**Inputs** content\_hash, is\_private = 0.

**Record and data access** read “File” via get\_all · resolve a document from “File” via get\_doc.

**Explicit results** mapping of k → b.get(k) for k drawn from Platform.get\_hooks() at “write\_file\_keys” · false.

**Local steps**

- For each name in Platform.get\_all(“File”, mapping(“content\_hash” → content\_hash, “is\_private” → is\_private), pluck = “name”).
  - Set b from Platform.get\_doc(“File”, name).
  - Return mapping of k → b.get(k) for k drawn from Platform.get\_hooks() at “write\_file\_keys”.
    - Draw k from Platform.get\_hooks() at “write\_file\_keys”.
- Return false.

**Values supplied outside this operation** selected callable from Platform.get\_hooks().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L1159) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L127)

<a id="op-d74232625d22ad"></a>
### Save file on filesystem

`operation_foundation_utils_file_manager_business_behavior_save_file_on_filesystem`

**Inputs** fname, content, content\_type = no value, is\_private = 0.

**Explicit results** mapping(“file\_name” → os.path.basename(fpath), “file\_url” → file\_url).

**Local steps**

- Set fpath from write\_file(content, fname, is\_private).
- If is\_private.
  - Set file\_url from formatted text /private/files/{fname}.
- Otherwise.
  - Set file\_url from formatted text /files/{fname}.
- Return mapping(“file\_name” → os.path.basename(fpath), “file\_url” → file\_url).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L1402) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1343) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L139)

<a id="op-5775d57967a3c6"></a>
### Get max file size

`operation_foundation_utils_file_manager_business_behavior_get_maximum_file_size`

**Inputs** no declared parameters.

**Explicit results** (conf.get(“max\_file\_size”) or 10485760).

**Local steps**

- Return (conf.get(“max\_file\_size”) or 10485760).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in conf.get(“max\_file\_size”) → 10485760.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L1626) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L132)

<a id="op-60f54c2e5367d1"></a>
### Check max file size

`operation_foundation_utils_file_manager_business_behavior_check_maximum_file_size`

**Inputs** content.

**State and service calls** msgprint with translated “File size exceeded the maximum allowed size of {0} MB”.format((max\_file\_size ÷ 1048576)).

**Explicit results** file\_size.

**Local steps**

- Set max\_file\_size from get\_max\_file\_size().
- Set file\_size from len(content).
- If file\_size &gt; max\_file\_size.
  - Evaluate Platform.msgprint(translated “File size exceeded the maximum allowed size of {0} MB”.format((max\_file\_size ÷ 1048576)), raise\_exception = MaxFileSizeReachedError).
- Return file\_size.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L1687) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1325) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L121)

<a id="op-f64af0684c0b47"></a>
### Write file

`operation_foundation_utils_file_manager_business_behavior_write_file`

**Inputs** content, fname, is\_private = 0.

**Explicit results** get\_files\_path(fname, is\_private = is\_private).

**Explicit failure paths** validation helper — translated “Invalid file name”.

**Local steps**

- Set file\_path from get\_files\_path(is\_private = is\_private).
- Evaluate Platform.create\_folder(file\_path).
- If os.path.realpath(os.path.dirname(os.path.join(file\_path, fname))) differs from os.path.realpath(file\_path).
  - Call the validation error handler Platform.throw(translated “Invalid file name”, title = translated “Invalid Upload”).
- If isinstance(content, str).
  - Set content from content.encode().
- Within open(os.path.join(file\_path.encode(“utf-8”), fname.encode(“utf-8”)), “wb+”) bound as f.
  - Evaluate f.write(content).
- Return get\_files\_path(fname, is\_private = is\_private).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L112) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1347) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L143)

<a id="op-a1421978b0bdf4"></a>
### Remove all

`operation_foundation_utils_file_manager_business_behavior_remove_all`

**Inputs** dt, dn, from\_delete = false, delete\_permanently = false.

**Record and data access** read “File” via get\_all.

**State and service calls** request delete\_doc for “File”.

**Explicit failure paths** propagate active failure.

**Local steps**

- Attempt the following.
  - For each fid in Platform.get\_all(“File”, mapping(“attached\_to\_doctype” → dt, “attached\_to\_name” → dn), pluck = “name”).
    - If from\_delete.
      - Evaluate Platform.delete\_doc(“File”, fid, ignore\_permissions = true, delete\_permanently = delete\_permanently).
    - Otherwise.
      - Evaluate remove\_file(fid = fid, attached\_to\_doctype = dt, attached\_to\_name = dn, from\_delete = from\_delete, …).
- On failure (Exception) bound to e.
  - If e.args at 0 differs from 1054.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L2167) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1339) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L135)

<a id="op-8b673590ed2c0a"></a>
### Remove file

`operation_foundation_utils_file_manager_business_behavior_remove_file`

**Inputs** fid = no value, attached\_to\_doctype = no value, attached\_to\_name = no value, from\_delete = false, delete\_permanently = false.

**Record and data access** read “File” via get\_value · resolve a document from attached\_to\_doctype via get\_doc.

**State and service calls** request delete\_doc for “File”.

**Explicit results** comment.

**Local steps**

- Set file\_name from no value.
- If not (attached\_to\_doctype and attached\_to\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in attached\_to\_doctype → attached\_to\_name.
  - Set attached from Platform.db.get\_value(“File”, fid, list(“attached\_to\_doctype”, “attached\_to\_name”, “file\_name”)).
  - If attached.
    - Set tuple(attached\_to\_doctype, attached\_to\_name, file\_name) from attached.
- Set tuple(ignore\_permissions, comment) from tuple(false, no value).
- If (attached\_to\_doctype and attached\_to\_name and not from\_delete).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in attached\_to\_doctype → attached\_to\_name → not from\_delete.
  - Set doc from Platform.get\_doc(attached\_to\_doctype, attached\_to\_name).
  - Set ignore\_permissions from (Platform.flags.in\_web\_form or doc.has\_permission(“write”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_web\_form → doc.has\_permission(“write”).
  - If not file\_name.
    - Set file\_name from Platform.db.get\_value(“File”, fid, “file\_name”).
  - Set comment from doc.add\_comment(“Attachment Removed”, file\_name).
  - Evaluate Platform.delete\_doc(“File”, fid, ignore\_permissions = ignore\_permissions, delete\_permanently = delete\_permanently).
- Return comment.

**Values supplied outside this operation** effective access from doc.has\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L2514) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1340) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L136)

<a id="op-1e34d25b843ffd"></a>
### Delete file data content

`operation_foundation_utils_file_manager_business_behavior_delete_file_data_content`

**Inputs** doc, only\_thumbnail = false.

**Local steps**

- Set method from get\_hook\_method(“delete\_file\_data\_content”, fallback = delete\_file\_from\_filesystem).
- Evaluate method(doc, only\_thumbnail = only\_thumbnail).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from get\_hook\_method(“delete\_file\_data\_content”, fallback = delete\_file\_from\_filesystem).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L3039) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L123)

<a id="op-e952d8507308b9"></a>
### Delete file from filesystem

`operation_foundation_utils_file_manager_business_behavior_delete_file_from_filesystem`

**Inputs** doc, only\_thumbnail = false.

**Local steps**

- If only\_thumbnail.
  - Evaluate delete\_file(doc.thumbnail\_url).
- Otherwise.
  - Evaluate delete\_file(doc.file\_url).
  - Evaluate delete\_file(doc.thumbnail\_url).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L3149) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L124)

<a id="op-9db219bd98eb27"></a>
### Delete file

`operation_foundation_utils_file_manager_business_behavior_delete_file`

**Inputs** path.

**State and service calls** msgprint with translated “It is risky to delete this file: {0}. Please contact your System Manager.”.format(path).

**Local steps**

- If path.
  - If “..” belongs to path.split(“/”).
    - Evaluate Platform.msgprint(translated “It is risky to delete this file: {0}. Please contact your System Manager.”.format(path)).
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

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L3275) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1326) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L122)

<a id="op-432e41f3b0254e"></a>
### Get file

`operation_foundation_utils_file_manager_business_behavior_get_file`

**Inputs** fname.

**Explicit results** list(file\_path.rsplit(“/”, 1) at negative 1, content).

**Local steps**

- Set file\_path from get\_file\_path(fname).
- Within open(encode(file\_path), mode = “rb”) bound as f.
  - Set content from f.read().
  - Attempt the following.
    - Set content from content.decode().
  - On failure (UnicodeDecodeError).
    - Take no action here.
- Return list(file\_path.rsplit(“/”, 1) at negative 1, content).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L3686) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L126)

<a id="op-6252d22888bab3"></a>
### Get file path

`operation_foundation_utils_file_manager_business_behavior_get_file_path`

**Inputs** file\_name.

**Explicit results** no value · file\_path.

**Explicit failure paths** validation helper — translated “There is some problem with the file url: {0}”.format(file\_path) · validation helper — translated “Cannot access file path {0}”.format(file\_path).

**Local steps**

- If “../” belongs to file\_name.
  - Return no value.
- Set File from DocType(“File”).
- Set f from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise or nested operand in the contract equals nested operand in ….run().
- If f.
  - Set file\_name from f at 0 at 0.
- Set file\_path from file\_name.
- If “/” does not belong to file\_path.
  - Set file\_path from (“/files/” + file\_path).
- If file\_path.startswith(“/private/files/”).
  - Set is\_private from 1.
  - Set file\_path from get\_files\_path(expanded nested operand in the contract.split(“/private/files/”, 1) at 1.split(“/”), is\_private = is\_private).
- Otherwise.
  - If file\_path.startswith(“/files/”).
    - Set is\_private from 0.
    - Set file\_path from get\_files\_path(expanded nested operand in the contract.split(“/files/”, 1) at 1.split(“/”)).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “There is some problem with the file url: {0}”.format(file\_path)).
- Set base\_path from os.path.realpath(get\_files\_path(is\_private = is\_private)).
- If os.path.commonpath(tuple(base\_path, os.path.realpath(file\_path))) differs from base\_path.
  - Call the validation error handler Platform.throw(translated “Cannot access file path {0}”.format(file\_path)).
- Return file\_path.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L3917) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L129)

<a id="op-f248809e95d8c8"></a>
### Get content hash

`operation_foundation_utils_file_manager_business_behavior_get_content_hash`

**Inputs** content.

**Explicit results** hashlib.md5(content, usedforsecurity = false).hexdigest().

**Local steps**

- If isinstance(content, str).
  - Set content from content.encode().
- Return hashlib.md5(content, usedforsecurity = false).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L111) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L125)

<a id="op-d19228f88f9937"></a>
### Get file name

`operation_foundation_utils_file_manager_business_behavior_get_file_name`

**Inputs** fname, optional\_suffix.

**Record and data access** read “File” via get\_all.

**Explicit results** formatted text {partial}{optional\_suffix}{extn} · fname.

**Local steps**

- Set fname from cstr(fname).
- Set n\_records from Platform.get\_all(“File”, mapping(“file\_name” → fname), pluck = “name”).
- If (len(n\_records) &gt; 0 or os.path.exists(encode(get\_files\_path(fname)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(n\_records) &gt; 0 → os.path.exists(encode(get\_files\_path(fname))).
  - Set f from fname.rsplit(“.”, 1).
  - If len(f) equals 1.
    - Set tuple(partial, extn) from tuple(f at 0, empty text).
  - Otherwise.
    - Set tuple(partial, extn) from tuple(f at 0, (“.” + f at 1)).
  - Return formatted text {partial}{optional\_suffix}{extn}.
- Return fname.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L4829) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L128)

<a id="op-43b12af18dce13"></a>
### Add attachments

`operation_foundation_utils_file_manager_business_behavior_add_attachments`

**Inputs** doctype, name, attachments.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “File” via get\_value.

**Explicit results** files.

**Explicit failure paths** validation helper — translated “You need write permissions to add attachments to this record.” · validation helper — translated “You don't have permission to read/attach the file {0}.”.format(a).

**Local steps**

- If not Platform.has\_permission(doctype, “write”, doc = name).
  - Call the validation error handler Platform.throw(translated “You need write permissions to add attachments to this record.”).
- If isinstance(attachments, str).
  - Set attachments from json.loads(attachments).
- Set files from list().
- For each a in attachments.
  - If isinstance(a, str).
    - If not Platform.has\_permission(“File”, ptype = “read”, doc = a).
      - Call the validation error handler Platform.throw(translated “You don't have permission to read/attach the file {0}.”.format(a)).
    - Set attach from Platform.db.get\_value(“File”, mapping(“name” → a), list(“file\_name”, “file\_url”, “is\_private”), as\_dict = 1).
    - Set f from save\_url(attach.file\_url, attach.file\_name, doctype, name, …).
    - Evaluate files.append(f).
- Return files.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “write”, doc = name), Platform.has\_permission(“File”, ptype = “read”, doc = a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L110) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1324) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L120)

<a id="op-33acd1c87775a8"></a>
### Is safe path

`operation_foundation_utils_file_manager_business_behavior_is_safe_path`

**Inputs** path.

**Declared result** bool.

**Explicit results** true · basedir equals os.path.commonpath(tuple(basedir, matchpath)).

**Local steps**

- If path.startswith(tuple(text in the contract, text in the contract, “/api/method/”)).
  - Return true.
- Set basedir from Platform.get\_site\_path().
- Set matchpath from os.path.abspath(path).
- Set basedir from os.path.abspath(basedir).
- Return basedir equals os.path.commonpath(tuple(basedir, matchpath)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L5853) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1338) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L134)

## Service · Fixtures

<a id="op-aa593c08bce31d"></a>
### Sync fixtures

`operation_foundation_utils_fixtures_business_behavior_sync_fixtures`

**Inputs** app = no value.

**Local steps**

- If app.
  - Set apps from list(app).
- Otherwise.
  - Set apps from Platform.get\_installed\_apps().
- Set Platform.flags.in\_fixtures from true.
- For each app in apps.
  - Evaluate import\_fixtures(app).
  - Evaluate import\_custom\_scripts(app).
- Set Platform.flags.in\_fixtures from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L6074) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1351) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L147)

<a id="op-25d0473c076bfe"></a>
### Import fixtures

`operation_foundation_utils_fixtures_business_behavior_import_fixtures`

**Inputs** app.

**Explicit results** no value.

**Local steps**

- Set fixtures\_path from Platform.get\_app\_path(app, “fixtures”).
- If not os.path.exists(fixtures\_path).
  - Return no value.
- Set fixture\_files from sorted(os.listdir(fixtures\_path)).
- For each fname in fixture\_files.
  - If not fname.endswith(“.json”).
    - Continue with the next iteration or loop test.
  - Set file\_path from Platform.get\_app\_path(app, “fixtures”, fname).
  - Attempt the following.
    - Evaluate import\_doc(file\_path, sort = true).
  - On failure (tuple(ImportError, Platform.DoesNotExistError)) bound to e.
    - Evaluate print(formatted text Skipping fixture syncing from the file {fname}. Reason: {e}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L6261) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1350) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L146)

<a id="op-83936f34a2ca54"></a>
### Import custom scripts

`operation_foundation_utils_fixtures_business_behavior_import_custom_scripts`

**Inputs** app.

**Explicit results** no value.

**Local steps**

- Set scripts\_folder from Platform.get\_app\_path(app, “fixtures”, “custom\_scripts”).
- If not os.path.exists(scripts\_folder).
  - Return no value.
- For each fname in os.listdir(scripts\_folder).
  - If not fname.endswith(“.js”).
    - Continue with the next iteration or loop test.
  - Evaluate click.secho(formatted text Importing Client Script ′{fname}′ from ′{scripts\_folder}′ is not supported. Convert the client script to fixture., fg = “red”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L6606) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1349) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L145)

<a id="op-dbd54a0e17eb96"></a>
### Export fixtures

`operation_foundation_utils_fixtures_business_behavior_export_fixtures`

**Inputs** app = no value.

**Explicit failure paths** click.exceptions.Exit(1).

**Local steps**

- If app.
  - Set apps from list(app).
- Otherwise.
  - Set apps from Platform.get\_installed\_apps().
- For each app in apps.
  - Set fixture\_auto\_order from bool(next(iter(Platform.get\_hooks(“fixture\_auto\_order”, app\_name = app)), false)).
  - Set fixtures from Platform.get\_hooks(“fixtures”, app\_name = app).
  - Set prefix from no value.
  - For each tuple(index, fixture) in enumerate(fixtures, start = 1).
    - Set filters from no value.
    - Set or\_filters from no value.
    - If isinstance(fixture, dict).
      - Set filters from fixture.get(“filters”).
      - Set or\_filters from fixture.get(“or\_filters”).
      - Set prefix from fixture.get(“prefix”).
      - Set fixture from (fixture.get(“doctype”) or fixture.get(“dt”)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in fixture.get(“doctype”) → fixture.get(“dt”).
    - If fixture belongs to DISALLOWED\_FIXTURE\_DOCTYPES.
      - Evaluate click.secho(formatted text Cannot export "{fixture}" doctype as a fixture, since it can only be created in developer mode from desk. Remove the fixture for "{fixture}" doctype w, fg = “red”, err = true).
        - Value choice on filters — true gives filters, false gives or\_filters.
      - Raise click.exceptions.Exit(1).
    - Evaluate print(formatted text Exporting {fixture} app {app} filters {filters when filters, otherwise or\_filters}).
      - Value choice on filters — true gives filters, false gives or\_filters.
    - If not os.path.exists(Platform.get\_app\_path(app, “fixtures”)).
      - Evaluate os.mkdir(Platform.get\_app\_path(app, “fixtures”)).
    - Set filename from Platform.scrub(fixture).
    - If prefix.
      - Set filename from formatted text {prefix}\_{filename}.
    - If fixture\_auto\_order.
      - Set number\_of\_digits from len(str(len(fixtures))).
      - Set file\_number from str(index).zfill(number\_of\_digits).
      - Set filename from formatted text {file\_number}\_{filename}.
    - Evaluate export\_json(fixture, Platform.get\_app\_path(app, “fixtures”, (filename + “.json”)), filters = filters, or\_filters = or\_filters, order\_by = “idx asc, creation asc”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“fixture\_auto\_order”, app\_name = app), Platform.get\_hooks(“fixtures”, app\_name = app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0481.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1348) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L144)

## Service · Formatters

<a id="op-61ed7a6301cbed"></a>
### Format value

`operation_foundation_utils_formatters_business_behavior_format_value`

**Inputs** value, df = no value, doc = no value, currency = no value, translated = false, format = no value.

**Explicit results** value · formatdate(value) · format\_datetime(value) · format\_time(value) · format\_timedelta(value) · 12 additional forms in the steps below.

**Local steps**

- If isinstance(df, str).
  - Set df from Platform.\_dict(fieldtype = df).
- If not df.
  - Set df from Platform.\_dict().
  - Select the first matching pattern against value.
    - Pattern instance of datetime.datetime.
      - Set df.fieldtype from “Datetime”.
    - Pattern instance of datetime.date.
      - Set df.fieldtype from “Date”.
    - Pattern instance of datetime.timedelta.
      - Set df.fieldtype from “Time”.
    - Pattern instance of int.
      - Set df.fieldtype from “Int”.
    - Pattern instance of float.
      - Set df.fieldtype from “Float”.
    - Pattern any value.
      - Set df.fieldtype from “Data”.
- Otherwise.
  - If isinstance(df, dict).
    - Set df from Platform.\_dict(df).
- If value is identical to no value.
  - Set value from empty text.
- Otherwise.
  - If translated.
    - Set value from Platform.\_(value).
- If not df.
  - Return value.
- Otherwise.
  - If df.get(“fieldtype”) equals “Date”.
    - Return formatdate(value).
  - Otherwise.
    - If df.get(“fieldtype”) equals “Datetime”.
      - Return format\_datetime(value).
    - Otherwise.
      - If df.get(“fieldtype”) equals “Time”.
        - Attempt the following.
          - Return format\_time(value).
        - On failure (ParserError).
          - Return format\_timedelta(value).
      - Otherwise.
        - If (value equals 0 and df.get(“fieldtype”) belongs to tuple(“Int”, “Float”, “Currency”, “Percent”) and df.get(“print\_hide\_if\_no\_value”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in value equals 0 → df.get(“fieldtype”) belongs to tuple(“Int”, “Float”, “Currency”, “Percent”) → df.get(“print\_hide\_if\_no\_value”).
          - Return empty text.
        - Otherwise.
          - If df.get(“fieldtype”) equals “Currency”.
            - Set default\_currency from Platform.db.get\_default(“currency”).
            - Set currency from (currency or get\_field\_currency(df, doc) or default\_currency).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → get\_field\_currency(df, doc) → default\_currency.
            - Return fmt\_money(value, precision = get\_field\_precision(df, doc), currency = currency, format = format).
          - Otherwise.
            - If df.get(“fieldtype”) equals “Float”.
              - Set precision from get\_field\_precision(df, doc).
              - Set currency from (currency or get\_field\_currency(df, doc)).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → get\_field\_currency(df, doc).
              - If (not df.options and value is distinct from no value).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in not df.options → value is distinct from no value.
                - Set temp from cstr(value).split(“.”).
                - If (len(temp) equals 1 or cint(temp at 1) equals 0).
                  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(temp) equals 1 → cint(temp at 1) equals 0.
                  - Set precision from 0.
              - Return fmt\_money(value, precision = precision, currency = currency).
            - Otherwise.
              - If df.get(“fieldtype”) equals “Int”.
                - Return empty text when value equals empty text, otherwise cstr(cint(value)).
                  - Value choice on value equals empty text — true gives empty text, false gives cstr(cint(value)).
              - Otherwise.
                - If df.get(“fieldtype”) equals “Percent”.
                  - Return formatted text {flt(value, 2)}%.
                - Otherwise.
                  - If df.get(“fieldtype”) belongs to tuple(“Text”, “Small Text”, “Long Text”).
                    - If not BLOCK\_TAGS\_PATTERN.search(value).
                      - Return Platform.safe\_decode(value).replace(whitespace '\\n', text in the contract).
                  - Otherwise.
                    - If df.get(“fieldtype”) equals “Markdown Editor”.
                      - Return Platform.utils.markdown(value).
                    - Otherwise.
                      - If df.get(“fieldtype”) equals “Table MultiSelect”.
                        - Set values from list().
                        - Set meta from Platform.get\_meta(df.options).
                        - Set link\_field from next(generator of df for df drawn from meta.fields where df.fieldtype equals “Link”).
                          - Draw df from meta.fields, keep a combination only if (df.fieldtype equals “Link”).
                        - For each v in value.
                          - Evaluate v.update(mapping(“\_\_link\_titles” → doc.get(“\_\_link\_titles”))).
                          - Set formatted\_value from format\_value(v.get(link\_field.fieldname, empty text), link\_field, v).
                          - Evaluate values.append(formatted\_value).
                        - Return “, ”.join(values).
                      - Otherwise.
                        - If df.get(“fieldtype”) equals “Duration”.
                          - Set hide\_days from df.hide\_days.
                          - Return format\_duration(value, hide\_days).
                        - Otherwise.
                          - If df.get(“fieldtype”) equals “Text Editor”.
                            - Return formatted text &lt;div class='ql-snow'&gt;{value}&lt;/div&gt;.
                          - Otherwise.
                            - If df.get(“fieldtype”) belongs to list(“Link”, “Dynamic Link”).
                              - If (not doc or not doc.get(“\_\_link\_titles”) or not df.options).
                                - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc → not doc.get(“\_\_link\_titles”) → not df.options.
                                - Return value.
                              - Set doctype from df.options.
                              - If df.get(“fieldtype”) equals “Dynamic Link”.
                                - If not df.parent.
                                  - Return value.
                                - Set meta from Platform.get\_meta(df.parent).
                                - Set \_field from meta.get\_field(df.options).
                                - Set doctype from \_field.options.
                              - Return doc.\_\_link\_titles.get(formatted text {doctype}::{value}, value).
                            - Otherwise.
                              - If df.get(“fieldtype”) equals “Select”.
                                - If isinstance(value, str).
                                  - Return Platform.\_(value, context = (df.parent or empty text)).
                                    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.parent → empty text.
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L113) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1352) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L148)

## Service · Global search

<a id="op-a5bcaf15c0bef1"></a>
### Setup global search table

`operation_foundation_utils_global_search_business_behavior_setup_global_search_table`

**Inputs** no declared parameters.

**Local steps**

- Evaluate Platform.db.create\_global\_search\_table().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0481.json#L3842) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1370) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L166)

<a id="op-9e21936f93188c"></a>
### Reset

`operation_foundation_utils_global_search_business_behavior_reset`

**Inputs** no declared parameters.

**State and service calls** request delete on “\_\_global\_search”.

**Local steps**

- Evaluate Platform.db.delete(“\_\_global\_search”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0481.json#L3887) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1368) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L164)

<a id="op-f9eb0b6a745130"></a>
### Get doctypes with global search

`operation_foundation_utils_global_search_business_behavior_get_record_types_with_global_search`

**Inputs** with\_child\_tables = true.

**Explicit results** Platform.cache.get\_value(“doctypes\_with\_global\_search”, \_get).

**Local steps**

- Bind local operation \_get for subsequent calls.
- Return Platform.cache.get\_value(“doctypes\_with\_global\_search”, \_get).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L115) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1361) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L157)
