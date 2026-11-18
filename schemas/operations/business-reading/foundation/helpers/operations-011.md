# Shared value and file services · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Commands

<a id="op-50a6b75ae6a46a"></a>
### Log

`operation_foundation_utils_commands_business_behavior_log`

**Inputs** message, colour = empty text.

**Local steps**

- Set colours from mapping(“nc” → “ &#91;0m”, “blue” → “ &#91;94m”, “green” → “ &#91;92m”, “yellow” → “ &#91;93m”, …).
- Set colour from colours.get(colour, empty text).
- Set end\_line from “ &#91;0m”.
- Evaluate print(((colour + message) + end\_line)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6488) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1046) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1605)

<a id="op-90f9de1edb812e"></a>
### Warn

`operation_foundation_utils_commands_business_behavior_warn`

**Inputs** message, category = no value, stacklevel = 3.

**Local steps**

- Bind dependencies warn.
- Evaluate warn(message = message, category = category, stacklevel = stacklevel).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6691) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1048) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1607)

## Service · Connections

<a id="op-09a6b959358981"></a>
### Can connect

`operation_foundation_utils_connections_business_behavior_can_connect`

**Inputs** sock, address, timeout.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Evaluate sock.settimeout(timeout).
- Attempt the following.
  - Evaluate sock.connect(address).
  - Evaluate sock.shutdown(socket.SHUT\_RDWR).
  - Return true.
- On failure (OSError).
  - Return false.
- On exit, including pending return or failure.
  - Evaluate sock.close().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6795) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1049) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1608)

<a id="op-f7e65cebb706e8"></a>
### Is open

`operation_foundation_utils_connections_business_behavior_is_open`

**Inputs** scheme, hostname, port, path, timeout = 10.

**Declared result** bool.

**Explicit results** false · true · can\_connect(s, path, timeout).

**Explicit failure paths** UrlSchemeNotSupported(scheme).

**Local steps**

- If scheme belongs to tuple(“redis”, “rediss”, “postgres”, “mariadb”).
  - If (not hostname or not port).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hostname → not port.
    - Return false.
  - Attempt the following.
    - Set addresses from socket.getaddrinfo(hostname, port, socket.AF\_UNSPEC, socket.SOCK\_STREAM).
  - On failure (tuple(socket.gaierror, TypeError)).
    - Return false.
  - For each tuple(family, socket\_type, proto, \_, …) in addresses.
    - Set s from socket.socket(family, socket\_type, proto).
    - If can\_connect(s, address, timeout).
      - Return true.
  - Return false.
- If scheme equals “unix”.
  - If not path.
    - Return false.
  - Set s from socket.socket(socket.AF\_UNIX, socket.SOCK\_STREAM).
  - Return can\_connect(s, path, timeout).
- Raise UrlSchemeNotSupported(scheme).

**Values supplied outside this operation** service or queued work from socket.getaddrinfo(hostname, port, socket.AF\_UNSPEC, socket.SOCK\_STREAM), socket.socket(family, socket\_type, proto) and 1 further calls.

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L7018) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1053) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1612)

<a id="op-9f2fcca177e718"></a>
### Check database

`operation_foundation_utils_connections_business_behavior_check_database`

**Inputs** no declared parameters.

**Explicit results** mapping(db\_type → (db\_path.is\_file() and os.access(db\_path, (os.R\_OK bitwise or os.W\_OK)))) · mapping(db\_type → is\_open(“unix”, no value, no value, db\_socket)) · mapping(db\_type → is\_open(db\_type, db\_host, db\_port, no value)).

**Local steps**

- Set config from get\_conf().
- Set db\_type from config.get(“db\_type”, “mariadb”).
- If db\_type equals “sqlite”.
  - Set db\_path from ((Path(Platform.utils.get\_site\_path()) ÷ “db”) ÷ formatted text {config.db\_name}.db).
  - Return mapping(db\_type → (db\_path.is\_file() and os.access(db\_path, (os.R\_OK bitwise or os.W\_OK)))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in db\_path.is\_file() → os.access(db\_path, (os.R\_OK bitwise or os.W\_OK)).
- If db\_socket bound to config.get(“db\_socket”).
  - Return mapping(db\_type → is\_open(“unix”, no value, no value, db\_socket)).
- Set db\_host from config.get(“db\_host”, “127.0.0.1”).
- Set db\_port from config.get(“db\_port”, 3306 when db\_type equals “mariadb”, otherwise 5432).
  - Value choice on db\_type equals “mariadb” — true gives 3306, false gives 5432.
- Return mapping(db\_type → is\_open(db\_type, db\_host, db\_port, no value)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L7570) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1052) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1611)

<a id="op-9ba57305dd099d"></a>
### Check redis

`operation_foundation_utils_connections_business_behavior_check_cache_service`

**Inputs** redis\_services = no value.

**Explicit results** status.

**Local steps**

- Set config from get\_conf().
- Set services from (redis\_services or REDIS\_KEYS).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in redis\_services → REDIS\_KEYS.
- Set status from mapping().
- For each srv in services.
  - Set url from urlparse(config at srv).
  - Set status at srv from is\_open(url.scheme, url.hostname, url.port, url.path).
- Return status.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L8028) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1050) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1609)

<a id="op-fbd9829c0df6ad"></a>
### Check connection

`operation_foundation_utils_connections_business_behavior_check_connection`

**Inputs** redis\_services = no value.

**Explicit results** service\_status.

**Local steps**

- Set service\_status from mapping().
- Evaluate service\_status.update(check\_database()).
- Evaluate service\_status.update(check\_redis(redis\_services)).
- Return service\_status.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1051) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1610)

## Service · Csvutils

<a id="op-a2527085630cb1"></a>
### Escape formula injection

`operation_foundation_utils_csvutils_business_behavior_escape_formula_injection`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** value.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L129) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1056) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1615)

<a id="op-13f84be7dacee6"></a>
### Unescape formula injection

`operation_foundation_utils_csvutils_business_behavior_unescape_formula_injection`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** value.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L234) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1064) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1623)

<a id="op-7be22ded7883be"></a>
### Read csv content from attached file

`operation_foundation_utils_csvutils_business_behavior_read_comma_separated_values_content_from_attached_file`

**Inputs** doc.

**Record and data access** read “File” via get\_all · resolve a document from “File” via get\_doc.

**Explicit results** read\_csv\_content(fcontent).

**Explicit failure paths** Exception · validation helper — translated “Unable to open attached file. Did you export it as CSV?”.

**Local steps**

- Set fileid from Platform.get\_all(“File”, fields = list(“name”), filters = mapping(“attached\_to\_doctype” → doc.doctype, “attached\_to\_name” → doc.name), order\_by = “creation desc”).
- If fileid.
  - Set fileid from fileid at 0.name.
- If not fileid.
  - Evaluate msgprint(translated “File not attached”).
  - Raise Exception.
- Attempt the following.
  - Set \_file from Platform.get\_doc(“File”, fileid).
  - Set fcontent from \_file.get\_content().
  - Return read\_csv\_content(fcontent).
- On failure (Exception).
  - Call the validation error handler Platform.throw(translated “Unable to open attached file. Did you export it as CSV?”, title = translated “Invalid CSV Format”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L414) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1061) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1620)

<a id="op-c501de0455bf36"></a>
### Read csv content

`operation_foundation_utils_csvutils_business_behavior_read_comma_separated_values_content`

**Inputs** fcontent, use\_sniffer = false, delimiter = no value.

**State and service calls** msgprint with translated “Unknown file encoding. Tried to use: {0}”.format(“, ”.join(FILE\_ENCODING\_OPTIONS)) · msgprint with translated “Delimiter detection failed. Try to enable custom delimiters and adjust the delimiter options as per your data.” · msgprint with translated “Not a valid Comma Separated Value (CSV File)”.

**Explicit results** rows.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not isinstance(fcontent, str).
  - Set decoded from false.
  - For each encoding in FILE\_ENCODING\_OPTIONS.
    - Attempt the following.
      - Set fcontent from str(fcontent, encoding).
      - Set decoded from true.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - On failure (UnicodeDecodeError).
      - Continue with the next iteration or loop test.
  - If not decoded.
    - Evaluate Platform.msgprint(translated “Unknown file encoding. Tried to use: {0}”.format(“, ”.join(FILE\_ENCODING\_OPTIONS)), raise\_exception = true).
- Set fcontent from fcontent.encode(“utf-8”).
- Set content from list of Platform.safe\_decode(line) for line drawn from fcontent.splitlines(true).
  - Draw line from fcontent.splitlines(true).
- Set dialect from csv.get\_dialect(“excel”).
- If delimiter.
  - Set dialect from csv.excel().
  - Set dialect.delimiter from delimiter.
- Otherwise.
  - If use\_sniffer.
    - Set sniffer from Sniffer().
    - Set sample\_content from content at slice no value to 20 when len(content) &gt; 20, otherwise content.
      - Value choice on len(content) &gt; 20 — true gives content at slice no value to 20, false gives content.
    - Attempt the following.
      - Set dialect from sniffer.sniff(sample = whitespace '\\n'.join(sample\_content), delimiters = Platform.flags.delimiter\_options).
    - On failure (csv.Error).
      - Evaluate Platform.msgprint(translated “Delimiter detection failed. Try to enable custom delimiters and adjust the delimiter options as per your data.”, indicator = “orange”, alert = true).
- Attempt the following.
  - Set rows from list().
  - For each row in csv.reader(content, dialect = dialect).
    - Set r from list().
    - For each val in row.
      - Set val from unescape\_formula\_injection(val.strip()).
      - If val equals empty text.
        - Evaluate r.append(no value).
      - Otherwise.
        - Evaluate r.append(val).
    - Evaluate rows.append(r).
  - Return rows.
- On failure (Exception).
  - Evaluate Platform.msgprint(translated “Not a valid Comma Separated Value (CSV File)”).
  - Propagate the active failure.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L80) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1060) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1619)

<a id="op-4a8a812b6b05be"></a>
### Send csv to client

`operation_foundation_utils_csvutils_business_behavior_send_comma_separated_values_to_client`

**Inputs** args.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- If isinstance(args, str).
  - Set args from json.loads(args).
- Set args from Platform.\_dict(args).
- Set Platform.response at “result” from cstr(to\_csv(args.data)).
- Set Platform.response at “doctype” from args.filename.
- Set Platform.response at “type” from “csv”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L81) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1062) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1621)

<a id="op-1394a2dcc3f216"></a>
### To csv

`operation_foundation_utils_csvutils_business_behavior_to_comma_separated_values`

**Inputs** data.

**Explicit results** writer.getvalue().

**Local steps**

- Set writer from UnicodeWriter().
- For each row in data.
  - Evaluate writer.writerow(row).
- Return writer.getvalue().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L2114) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1063) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1622)

<a id="op-d29fcbd02d4233"></a>
### Build csv response

`operation_foundation_utils_csvutils_business_behavior_build_comma_separated_values_response`

**Inputs** data, filename.

**Local steps**

- Set Platform.response at “result” from cstr(to\_csv(data)).
- Set Platform.response at “doctype” from filename.
- Set Platform.response at “type” from “csv”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L2221) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1054) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1613)

<a id="op-4d08665073edfd"></a>
### Unicode Writer.initialize

`operation_foundation_utils_csvutils_business_behavior_unicode_writer_initialize`

**Inputs** self, encoding = “utf-8”, quoting = csv.QUOTE\_NONNUMERIC.

**Local steps**

- Set self.encoding from encoding.
- Set self.queue from StringIO().
- Set self.writer from csv.writer(self.queue, quoting = quoting).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L2374) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1066) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1625)

<a id="op-1a73f9af6b01df"></a>
### Unicode Writer.writerow

`operation_foundation_utils_csvutils_business_behavior_unicode_writer_writerow`

**Inputs** self, row.

**Local steps**

- Evaluate self.writer.writerow(list of escape\_formula\_injection(v) for v drawn from row).
  - Draw v from row.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L2519) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1067) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1626)

<a id="op-ca65e9f5db849d"></a>
### Unicode Writer.getvalue

`operation_foundation_utils_csvutils_business_behavior_unicode_writer_getvalue`

**Inputs** self.

**Explicit results** self.queue.getvalue().

**Local steps**

- Return self.queue.getvalue().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L2617) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1065) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1624)

<a id="op-9d1a2acc07cb99"></a>
### Check record

`operation_foundation_utils_csvutils_business_behavior_check_record`

**Inputs** d.

**Record and data access** resolve a document from d via get\_doc.

**State and service calls** msgprint with translated “{0} is required”.format(docfield.label).

**Explicit failure paths** validation helper — translated “{0} must be one of {1}”.format(\_(docfield.label, context = docfield.parent), comma\_or(docfield.options.split(whitespace '\\n'))).

**Local steps**

- Bind dependencies parse\_date.
- Set doc from Platform.get\_doc(d).
- For each key in d.
  - Set docfield from doc.meta.get\_field(key).
  - Set val from d at key.
  - If docfield.
    - If (docfield.reqd and (val equals empty text or val is identical to no value)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.reqd → (val equals empty text or val is identical to no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in val equals empty text → val is identical to no value.
      - Evaluate Platform.msgprint(translated “{0} is required”.format(docfield.label), raise\_exception = 1).
    - If (docfield.fieldtype equals “Select” and val and docfield.options).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in docfield.fieldtype equals “Select” → val → docfield.options.
      - If val does not belong to docfield.options.split(whitespace '\\n').
        - Call the validation error handler Platform.throw(translated “{0} must be one of {1}”.format(\_(docfield.label, context = docfield.parent), comma\_or(docfield.options.split(whitespace '\\n')))).
    - If (val and docfield.fieldtype equals “Date”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in val → docfield.fieldtype equals “Date”.
      - Set d at key from parse\_date(val).
    - Otherwise.
      - If (val and docfield.fieldtype belongs to list(“Int”, “Check”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in val → docfield.fieldtype belongs to list(“Int”, “Check”).
        - Set d at key from cint(val).
      - Otherwise.
        - If (val and docfield.fieldtype belongs to list(“Currency”, “Float”, “Percent”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in val → docfield.fieldtype belongs to list(“Currency”, “Float”, “Percent”).
          - Set d at key from flt(val).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L2670) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1055) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1614)

<a id="op-ecf26d3adff28b"></a>
### Import doc

`operation_foundation_utils_csvutils_business_behavior_import_record`

**Inputs** d, doctype, overwrite, row\_idx, submit = false, ignore\_links = false.

**Record and data access** read doctype via exists · resolve a document from doctype via get\_doc · resolve a document from d via get\_doc.

**State and service calls** call submit on doc · call save on doc · call insert on doc.

**Explicit results** (“Updated row (#%d) %s” modulo or format tuple((row\_idx + 1), getlink(doctype, d at “name”))) · (“Ignored row (#%d) %s (exists)” modulo or format tuple((row\_idx + 1), getlink(doctype, d at “name”))) · (“Inserted row (#%d) %s” modulo or format tuple((row\_idx + 1), getlink(doctype, doc.get(“name”)))).

**Local steps**

- If (d.get(“name”) and Platform.db.exists(doctype, d at “name”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“name”) → Platform.db.exists(doctype, d at “name”).
  - If overwrite.
    - Set doc from Platform.get\_doc(doctype, d at “name”).
    - Set doc.flags.ignore\_links from ignore\_links.
    - Evaluate doc.update(d).
    - If d.get(“docstatus”) equals 1.
      - Evaluate doc.update\_after\_submit().
    - Otherwise.
      - If (d.get(“docstatus”) equals 0 and submit).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“docstatus”) equals 0 → submit.
        - Evaluate doc.submit().
      - Otherwise.
        - Evaluate doc.save().
    - Return (“Updated row (#%d) %s” modulo or format tuple((row\_idx + 1), getlink(doctype, d at “name”))).
  - Otherwise.
    - Return (“Ignored row (#%d) %s (exists)” modulo or format tuple((row\_idx + 1), getlink(doctype, d at “name”))).
- Otherwise.
  - Set doc from Platform.get\_doc(d).
  - Set doc.flags.ignore\_links from ignore\_links.
  - Evaluate doc.insert().
  - If submit.
    - Evaluate doc.submit().
  - Return (“Inserted row (#%d) %s” modulo or format tuple((row\_idx + 1), getlink(doctype, doc.get(“name”)))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L3393) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1059) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1618)

<a id="op-d160efb437e4dd"></a>
### Getlink

`operation_foundation_utils_csvutils_business_behavior_getlink`

**Inputs** doctype, name.

**Explicit results** text in the contract.format(expanded names locals()).

**Local steps**

- Return text in the contract.format(expanded names locals()).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L4083) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1058) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1617)

<a id="op-0c15930e357cb0"></a>
### Get csv content from google sheets

`operation_foundation_utils_csvutils_business_behavior_get_comma_separated_values_content_from_google_sheets`

**Inputs** url.

**Explicit results** response.content.

**Explicit failure paths** validation helper — translated “Google Sheets URL is invalid or not publicly accessible.” · validation helper — translated “Google Sheets URL must end with "gid={number}". Copy and paste the URL from the browser address bar and try again.”.

**Local steps**

- Evaluate validate\_google\_sheets\_url(url).
- If “gid=” belongs to url.
  - Set gid from url.rsplit(“gid=”, 1) at 1.
- Otherwise.
  - Set gid from 0.
- Set url from url.rsplit(“/edit”, 1) at 0.
- Set url from (url + formatted text /export?format=csv&amp;gid={gid}).
- Bind dependencies requests.
- Set headers from mapping(“Accept” → “text/csv”).
- Set response from requests.get(url, headers = headers).
- If response.ok.
  - If response.text.strip().endswith(“&lt;/html&gt;”).
    - Call the validation error handler Platform.throw(translated “Google Sheets URL is invalid or not publicly accessible.”, title = translated “Invalid URL”).
  - Return response.content.
- Otherwise.
  - If response.status\_code equals 400.
    - Call the validation error handler Platform.throw(translated “Google Sheets URL must end with "gid={number}". Copy and paste the URL from the browser address bar and try again.”, title = translated “Incorrect URL”).
  - Otherwise.
    - Evaluate response.raise\_for\_status().

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from requests.get(url, headers = headers).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L4155) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1057) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1616)

<a id="op-faf1c7d6b88d14"></a>
### Validate google sheets url

`operation_foundation_utils_csvutils_business_behavior_validate_google_sheets_resource_address`

**Inputs** url.

**Explicit failure paths** validation helper — translated “"{0}" is not a valid Google Sheets URL”.format(url).

**Local steps**

- Bind dependencies urlparse.
- Set u from urlparse(url).
- If (u.scheme differs from “https” or u.netloc differs from “docs.google.com” or “/spreadsheets/” does not belong to u.path).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in u.scheme differs from “https” → u.netloc differs from “docs.google.com” → “/spreadsheets/” does not belong to u.path.
  - Call the validation error handler Platform.throw(translated “"{0}" is not a valid Google Sheets URL”.format(url), title = translated “Invalid URL”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0471.json#L4670) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1068) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1627)

## Service · Dashboard

<a id="op-d69b95e7f58479"></a>
### Cache source

`operation_foundation_utils_dashboard_business_behavior_cache_source`

**Inputs** function.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L82) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1069) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1628)

<a id="op-e44e860210635a"></a>
### Cache source.wrapper

`operation_foundation_utils_dashboard_business_behavior_cache_source_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** wraps(function).

**Record and data access** resolve a document from “Dashboard Chart” via get\_doc.

**Explicit results** function(chart = chart, no\_cache = no\_cache) · results.

**Local steps**

- If kwargs.get(“chart\_name”).
  - Set chart from Platform.get\_doc(“Dashboard Chart”, kwargs.get(“chart\_name”)).
- Otherwise.
  - Set chart from kwargs.get(“chart”).
- Set no\_cache from kwargs.get(“no\_cache”).
- If no\_cache.
  - Return function(chart = chart, no\_cache = no\_cache).
- Set chart\_name from Platform.parse\_json(chart).name.
- Set cache\_key from formatted text chart-data:{chart\_name}.
- If cint(kwargs.get(“refresh”)).
  - Set results from generate\_and\_cache\_results(kwargs, function, cache\_key, chart).
- Otherwise.
  - Set cached\_results from Platform.cache.get\_value(cache\_key).
  - If cached\_results.
    - Set results from Platform.parse\_json(Platform.safe\_decode(cached\_results)).
  - Otherwise.
    - Set results from generate\_and\_cache\_results(kwargs, function, cache\_key, chart).
- Return results.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L83) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1070) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1629)
