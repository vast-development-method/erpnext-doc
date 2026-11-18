# Shared value and file services · operations 21

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Error

<a id="op-53e78387d36094"></a>
### Log error

`operation_foundation_utils_error_business_behavior_log_error`

**Inputs** title = no value, message = no value, reference\_doctype = no value, reference\_name = no value, defer\_insert (named only, default false).

**Declared result** “ErrorLog”.

**Record and data access** resolve a document from “Error Log” via get\_doc.

**State and service calls** call insert on error\_log.

**Explicit results** no value · error\_log.

**Local steps**

- Bind dependencies get\_trace\_id.
- Set traceback from no value.
- If message.
  - If whitespace '\\n' belongs to title.
    - Set tuple(traceback, title) from tuple(title, message).
  - Otherwise.
    - Set traceback from message.
- Set traceback from Platform.as\_unicode((traceback or Platform.get\_traceback(with\_context = true))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in traceback → Platform.get\_traceback(with\_context = true).
- If not title.
  - If traceback.
    - Set title from traceback.splitlines() at negative 1 at slice no value to 140.
  - Otherwise.
    - Set title from “Error”.
- If not Platform.db.
  - Evaluate print(formatted text Failed to log error in db: {title}).
  - Return no value.
- Set trace\_id from get\_trace\_id().
- Set metadata from get\_error\_metadata().
- Set fingerprint from get\_error\_fingerprint().
- Set error\_log from Platform.get\_doc(doctype = “Error Log”, error = traceback, method = title, reference\_doctype = reference\_doctype, …).
- If (Platform.flags.read\_only or defer\_insert or Platform.db.in\_read\_only\_transaction).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.read\_only → defer\_insert → Platform.db.in\_read\_only\_transaction.
  - Evaluate error\_log.deferred\_insert().
- Otherwise.
  - Evaluate error\_log.insert(ignore\_permissions = true).
- If os.getenv(“Platform\_SENTRY\_DSN”).
  - Bind dependencies capture\_exception.
  - Evaluate capture\_exception(message = formatted text {title} {traceback}).
- Return error\_log.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L109) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L108)

<a id="op-b9567c9a1bc3e2"></a>
### Get error fingerprint

`operation_foundation_utils_error_business_behavior_get_error_fingerprint`

**Inputs** exception = no value.

**Declared result** (str bitwise or no value).

**Explicit results** no value · hashlib.sha1(nested operand in the contract.join(parts).encode(), usedforsecurity = false).hexdigest().

**Local steps**

- Bind dependencies get\_bench\_path.
- Within suppress(Exception).
  - If exception is identical to no value.
    - Set exception from sys.exc\_info() at 1.
  - If exception is identical to no value.
    - Return no value.
  - Set bench\_path from (get\_bench\_path() + “/”).
  - Set parts from list(type(exception).\_\_name\_\_).
  - For each tuple(frame, lineno) in traceback\_module.walk\_tb(exception.\_\_traceback\_\_).
    - Set code from frame.f\_code.
    - Set filename from code.co\_filename.replace(bench\_path, empty text).
    - Evaluate parts.append(formatted text {filename}:{lineno}:{code.co\_name}).
  - Return hashlib.sha1(nested operand in the contract.join(parts).encode(), usedforsecurity = false).hexdigest().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L2106) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1308) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L104)

<a id="op-502f182b9dc631"></a>
### Get error metadata

`operation_foundation_utils_error_business_behavior_get_error_metadata`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** Platform.as\_json(metadata).

**Local steps**

- Bind dependencies rq.
- Bind dependencies sanitized\_dict.
- Set metadata from mapping().
- Attempt the following.
  - If job bound to rq.get\_current\_job().
    - Set metadata at “type” from “background\_job”.
    - Set metadata at “job\_id” from job.id.
    - Set metadata at “job\_name” from Platform.cstr(job.kwargs.get(“method”)).
    - Set metadata at “queue” from job.origin.
    - Set metadata at “kwargs” from sanitized\_dict(job.kwargs).
    - If “run\_scheduled\_job” belongs to metadata at “job\_name”.
      - Set metadata at “scheduled” from true.
      - Set metadata at “job\_type” from job.kwargs.get(“kwargs”, mapping()).get(“job\_type”, empty text).
  - Otherwise.
    - Set metadata at “type” from “http\_request”.
    - For each key in tuple(“method”, “path”, “referrer”).
      - Set metadata at key from getattr(Platform.local.request, key).
    - Set metadata at “form\_dict” from sanitized\_dict(Platform.form\_dict).
  - Set metadata at “user” from getattr(Platform.session, “user”, “Unidentified”).
- On failure (Exception).
  - Take no action here.
- Return Platform.as\_json(metadata).

**Values supplied outside this operation** selected callable from getattr(Platform.local.request, key), getattr(Platform.session, “user”, “Unidentified”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L2581) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L105)

<a id="op-0d25007e3bb94f"></a>
### Log error snapshot

`operation_foundation_utils_error_business_behavior_log_error_snapshot`

**Inputs** exception.

**Explicit results** no value.

**Local steps**

- If (getattr(exception, “skip\_error\_log”, false) or \_is\_ldap\_exception(exception)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(exception, “skip\_error\_log”, false) → \_is\_ldap\_exception(exception).
  - Return no value.
- Set logger from Platform.logger(with\_more\_info = true).
- Attempt the following.
  - Evaluate log\_error(title = str(exception), defer\_insert = true).
  - Evaluate logger.error(“New Exception collected in error log”).
  - Evaluate add\_data\_to\_monitor(exception = exception.\_\_class\_\_.\_\_name\_\_).
- On failure (Exception) bound to e.
  - Evaluate logger.error(formatted text Could not take error snapshot: {e}, exc\_info = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(exception, “skip\_error\_log”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L3226) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L109)

<a id="op-110885d84ed196"></a>
### Get default args

`operation_foundation_utils_error_business_behavior_get_default_arguments`

**Inputs** func.

**Explicit results** mapping of k → v.default for tuple(k, v) drawn from signature.parameters.items() where v.default is distinct from inspect.Parameter.empty.

**Local steps**

- Set signature from inspect.signature(func).
- Return mapping of k → v.default for tuple(k, v) drawn from signature.parameters.items() where v.default is distinct from inspect.Parameter.empty.
  - Draw tuple(k, v) from signature.parameters.items(), keep a combination only if (v.default is distinct from inspect.Parameter.empty).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L3534) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L103)

<a id="op-3e0ef813c4dd26"></a>
### Raise error on no output

`operation_foundation_utils_error_business_behavior_raise_error_on_number_output`

**Inputs** error\_message, error\_type = no value, keep\_quiet = no value.

**Explicit results** decorator\_raise\_error\_on\_no\_output.

**Local steps**

- Bind local operation decorator\_raise\_error\_on\_no\_output for subsequent calls.
- Return decorator\_raise\_error\_on\_no\_output.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L3680) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L110)

<a id="op-856bea1f34dd56"></a>
### Raise error on no output.decorator raise error on no output

`operation_foundation_utils_error_business_behavior_raise_error_on_number_output_decorator_raise_error_on_number_output`

**Inputs** func.

**Explicit results** wrapper\_raise\_error\_on\_no\_output.

**Local steps**

- Bind local operation wrapper\_raise\_error\_on\_no\_output for subsequent calls.
- Return wrapper\_raise\_error\_on\_no\_output.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L4065) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L111)

<a id="op-c68f49695f4856"></a>
### Raise error on no output.decorator raise error on no output.wrapper raise error on no output

`operation_foundation_utils_error_business_behavior_raise_error_on_number_output_decorator_raise_error_on_number_output_wrapper_raise_error_on_number_output`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(func).

**Explicit results** response.

**Explicit failure paths** validation helper with (error\_type or Exception) — error\_message.

**Local steps**

- Set response from func(expanded args, expanded names kwargs).
- If (callable(keep\_quiet) and keep\_quiet()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in callable(keep\_quiet) → keep\_quiet().
  - Return response.
- Set default\_kwargs from get\_default\_args(func).
- Set default\_raise\_error from default\_kwargs.get(“\_raise\_error”).
- Set raise\_error from kwargs.get(“\_raise\_error”) when “\_raise\_error” belongs to kwargs, otherwise default\_raise\_error.
  - Value choice on “\_raise\_error” belongs to kwargs — true gives kwargs.get(“\_raise\_error”), false gives default\_raise\_error.
- If (not response and raise\_error).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not response → raise\_error.
  - Call the validation error handler Platform.throw(error\_message, (error\_type or Exception)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in error\_type → Exception.
- Return response.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L4406) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L112)

<a id="op-04a47aa296e09a"></a>
### Guess exception source

`operation_foundation_utils_error_business_behavior_guess_exception_source`

**Inputs** exception.

**Declared result** (str bitwise or no value).

**Explicit results** “Server Script” · formatted text {probably\_source at 0 at 0} (app).

**Local steps**

- Bind dependencies SERVER\_SCRIPT\_FILE\_PREFIX.
- Within suppress(Exception).
  - Set installed\_apps from Platform.get\_installed\_apps().
  - Set app\_priority from mapping of app → installed\_apps.index(app) for app drawn from installed\_apps.
    - Draw app from installed\_apps.
  - Set APP\_NAME\_REGEX from re.compile(“.\*File.\*apps/(?P&lt;app\_name&gt;\\w+)/\\1/”).
  - Set apps from Counter().
  - For each line in reversed(exception.splitlines()).
    - If SERVER\_SCRIPT\_FILE\_PREFIX belongs to line.
      - Return “Server Script”.
    - If matches bound to APP\_NAME\_REGEX.match(line).
      - Set app\_name from matches.group(“app\_name”).
      - Update apps at app\_name using + app\_priority.get(app\_name, 0).
  - If (probably\_source bound to apps.most\_common(1) and probably\_source at 0 at 0 differs from “Platform”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in probably\_source bound to apps.most\_common(1) → probably\_source at 0 at 0 differs from “Platform”.
    - Return formatted text {probably\_source at 0 at 0} (app).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L4723) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L106)

## Service · File lock

<a id="op-9ba193b60771b3"></a>
### Create lock

`operation_foundation_utils_file_dependency_lock_business_behavior_create_dependency_lock`

**Inputs** name.

**Explicit results** touch\_file(lock\_path) · false.

**Local steps**

- Set lock\_path from get\_lock\_path(name).
- If not check\_lock(lock\_path).
  - Return touch\_file(lock\_path).
- Otherwise.
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5216) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L114)

<a id="op-9dfbc45264f128"></a>
### Lock exists

`operation_foundation_utils_file_dependency_lock_business_behavior_dependency_lock_exists`

**Inputs** name.

**Explicit results** os.path.exists(get\_lock\_path(name)).

**Local steps**

- Return os.path.exists(get\_lock\_path(name)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5331) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1321) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L117)

<a id="op-31e86f6e864f7a"></a>
### Lock age

`operation_foundation_utils_file_dependency_lock_business_behavior_dependency_lock_age`

**Inputs** name.

**Declared result** float.

**Explicit results** (time() − Path(get\_lock\_path(name)).stat().st\_mtime).

**Local steps**

- Return (time() − Path(get\_lock\_path(name)).stat().st\_mtime).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5404) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L116)

<a id="op-81a36fd3188151"></a>
### Check lock

`operation_foundation_utils_file_dependency_lock_business_behavior_check_dependency_lock`

**Inputs** path, timeout = 600.

**Explicit results** false · true.

**Explicit failure paths** LockTimeoutError(path).

**Local steps**

- If not os.path.exists(path).
  - Return false.
- If (time() − os.path.getmtime(path)) &gt; timeout.
  - Raise LockTimeoutError(path).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5501) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L113)

<a id="op-d503c9487de020"></a>
### Delete lock

`operation_foundation_utils_file_dependency_lock_business_behavior_delete_dependency_lock`

**Inputs** name.

**Explicit results** true.

**Local steps**

- Set lock\_path from get\_lock\_path(name).
- Attempt the following.
  - Evaluate os.remove(lock\_path).
- On failure (OSError).
  - Take no action here.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5672) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L115)

<a id="op-d7100cd6ab573d"></a>
### Get lock path

`operation_foundation_utils_file_dependency_lock_business_behavior_get_dependency_lock_path`

**Inputs** name.

**Explicit results** get\_site\_path(LOCKS\_DIR, formatted text {name.lower()}.lock).

**Local steps**

- Return get\_site\_path(LOCKS\_DIR, formatted text {name.lower()}.lock).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5784) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1322) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L118)

<a id="op-4d6b83f0c5b538"></a>
### Release document locks

`operation_foundation_utils_file_dependency_lock_business_behavior_release_document_locks`

**Inputs** no declared parameters.

**Local steps**

- For each doc in Platform.local.locked\_documents.
  - Evaluate doc.unlock().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5868) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1323) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L119)

## Service · File manager

<a id="op-833f7cc24fae60"></a>
### Safe b64decode

`operation_foundation_utils_file_manager_business_behavior_safe_b_64_decode`

**Inputs** binary.

**Declared result** bytes.

**Explicit results** base64.b64decode((binary + byte value)).

**Local steps**

- Return base64.b64decode((binary + byte value)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L5932) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1341) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L137)

<a id="op-4c188b90306252"></a>
### Get file url

`operation_foundation_utils_file_manager_business_behavior_get_file_resource_address`

**Inputs** file\_data\_name.

**Record and data access** read “File” via get\_value.

**Explicit results** (data.file\_url or data.file\_name).

**Local steps**

- Set data from Platform.db.get\_value(“File”, file\_data\_name, list(“file\_name”, “file\_url”), as\_dict = true).
- Return (data.file\_url or data.file\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data.file\_url → data.file\_name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L6005) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L131)

<a id="op-4f837d3553c565"></a>
### Upload

`operation_foundation_utils_file_manager_business_behavior_upload`

**Inputs** no declared parameters.

**Record and data access** resolve a document from dt via get\_doc.

**State and service calls** msgprint with translated “Please select a file or url”.

**Explicit results** mapping(“name” → file\_doc.name, “file\_name” → file\_doc.file\_name, “file\_url” → file\_doc.file\_url, “is\_private” → file\_doc.is\_private, …).

**Local steps**

- Set dt from Platform.form\_dict.doctype.
- Set dn from Platform.form\_dict.docname.
- Set file\_url from Platform.form\_dict.file\_url.
- Set filename from Platform.form\_dict.filename.
- Set Platform.form\_dict.is\_private from cint(Platform.form\_dict.is\_private).
- If (not filename and not file\_url).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not filename → not file\_url.
  - Evaluate Platform.msgprint(translated “Please select a file or url”, raise\_exception = true).
- Set file\_doc from get\_file\_doc().
- Set comment from mapping().
- If (dt and dn).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt → dn.
  - Set file\_url from file\_doc.file\_url.replace(“#”, “%23”) when file\_doc.file\_name, otherwise file\_doc.file\_url.
    - Value choice on file\_doc.file\_name — true gives file\_doc.file\_url.replace(“#”, “%23”), false gives file\_doc.file\_url.
  - Set icon from “ &lt;i class="fa fa-lock text-warning"&gt;&lt;/i&gt;” when file\_doc.is\_private, otherwise empty text.
    - Value choice on file\_doc.is\_private — true gives “ &lt;i class="fa fa-lock text-warning"&gt;&lt;/i&gt;”, false gives empty text.
  - Set file\_name from (file\_doc.file\_name or file\_doc.file\_url).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in file\_doc.file\_name → file\_doc.file\_url.
  - Set comment from Platform.get\_doc(dt, dn).add\_comment(“Attachment”, formatted text &lt;a href='{file\_url}' target='\_blank'&gt;{file\_name}&lt;/a&gt;{icon}).
- Return mapping(“name” → file\_doc.name, “file\_name” → file\_doc.file\_name, “file\_url” → file\_doc.file\_url, “is\_private” → file\_doc.is\_private, …).
  - Value choice on comment — true gives comment.as\_dict(), false gives mapping().

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L6136) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1346) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L142)

<a id="op-adf5c3af71794a"></a>
### Get file doc

`operation_foundation_utils_file_manager_business_behavior_get_file_record`

**Inputs** dt = no value, dn = no value, folder = no value, is\_private = no value, df = no value.

**Explicit results** file\_doc.

**Local steps**

- Set r from Platform.form\_dict.
- If dt is identical to no value.
  - Set dt from r.doctype.
- If dn is identical to no value.
  - Set dn from r.docname.
- If df is identical to no value.
  - Set df from r.docfield.
- If folder is identical to no value.
  - Set folder from r.folder.
- If is\_private is identical to no value.
  - Set is\_private from r.is\_private.
- If r.filedata.
  - Set file\_doc from save\_uploaded(dt, dn, folder, is\_private, …).
- Otherwise.
  - If r.file\_url.
    - Set file\_doc from save\_url(r.file\_url, r.filename, dt, dn, …).
- Return file\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L6762) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L130)

<a id="op-35fc6ffc40707d"></a>
### Save uploaded

`operation_foundation_utils_file_manager_business_behavior_save_uploaded`

**Inputs** dt, dn, folder, is\_private, df = no value.

**Explicit results** save\_file(fname, content, dt, dn, is\_private = is\_private, df = df, …).

**Explicit failure paths** Exception.

**Local steps**

- Set tuple(fname, content) from get\_uploaded\_content().
- If content.
  - Return save\_file(fname, content, dt, dn, is\_private = is\_private, df = df, …).
- Otherwise.
  - Raise Exception.

**Boundaries to resolve** callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L7181) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1345) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L141)

<a id="op-6fc0e1bc50d455"></a>
### Save url

`operation_foundation_utils_file_manager_business_behavior_save_resource_address`

**Inputs** file\_url, filename, dt, dn, folder, is\_private, df = no value.

**Record and data access** resolve a document from mapping(“doctype” → “File”, “file\_url” → file\_url, “file\_name” → filename, “attached\_to\_doctype” → dt, …) via get\_doc · resolve a document from “File” via get\_doc.

**State and service calls** call insert on f.

**Explicit results** Platform.get\_doc(“File”, f.duplicate\_entry) · f.

**Local steps**

- Set file\_url from unquote(file\_url).
- Set file\_size from Platform.form\_dict.file\_size.
- Set f from Platform.get\_doc(mapping(“doctype” → “File”, “file\_url” → file\_url, “file\_name” → filename, “attached\_to\_doctype” → dt, …)).
- Set f.flags.ignore\_permissions from true.
- Attempt the following.
  - Evaluate f.insert().
- On failure (Platform.DuplicateEntryError).
  - Return Platform.get\_doc(“File”, f.duplicate\_entry).
- Return f.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0479.json#L7355) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1344) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L140)

<a id="op-dc8045c679197a"></a>
### Get uploaded content

`operation_foundation_utils_file_manager_business_behavior_get_uploaded_content`

**Inputs** no declared parameters.

**State and service calls** msgprint with translated “No file attached”.

**Explicit results** tuple(Platform.uploaded\_filename, Platform.uploaded\_content) · tuple(no value, no value).

**Local steps**

- If “filedata” belongs to Platform.form\_dict.
  - If “,” belongs to Platform.form\_dict.filedata.
    - Set Platform.form\_dict.filedata from Platform.form\_dict.filedata.rsplit(“,”, 1) at 1.
  - Set Platform.uploaded\_content from safe\_b64decode(Platform.form\_dict.filedata).
  - Set Platform.uploaded\_filename from Platform.form\_dict.filename.
  - Return tuple(Platform.uploaded\_filename, Platform.uploaded\_content).
- Otherwise.
  - Evaluate Platform.msgprint(translated “No file attached”).
  - Return tuple(no value, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L133)

<a id="op-bc07638b79c8e2"></a>
### Save file

`operation_foundation_utils_file_manager_business_behavior_save_file`

**Inputs** fname, content, dt, dn, folder = no value, decode = false, is\_private = 0, df = no value.

**Record and data access** resolve a document from file\_data via get\_doc · resolve a document from “File” via get\_doc.

**State and service calls** call insert on f.

**Explicit results** Platform.get\_doc(“File”, f.duplicate\_entry) · f.

**Local steps**

- If decode.
  - If isinstance(content, str).
    - Set content from content.encode(“utf-8”).
  - If byte value belongs to content.
    - Set content from content.split(byte value) at 1.
  - Set content from safe\_b64decode(content).
- Set file\_size from check\_max\_file\_size(content).
- Set content\_hash from get\_content\_hash(content).
- Set content\_type from mimetypes.guess\_type(fname) at 0.
- Set fname from get\_file\_name(fname, content\_hash at slice negative 6 to no value).
- Set file\_data from get\_file\_data\_from\_hash(content\_hash, is\_private = is\_private).
- If not file\_data.
  - Evaluate call\_hook\_method(“before\_write\_file”, file\_size = file\_size).
  - Set write\_file\_method from get\_hook\_method(“write\_file”, fallback = save\_file\_on\_filesystem).
  - Set file\_data from write\_file\_method(fname, content, content\_type = content\_type, is\_private = is\_private).
  - Set file\_data from copy(file\_data).
- Evaluate file\_data.update(mapping(“doctype” → “File”, “attached\_to\_doctype” → dt, “attached\_to\_name” → dn, “attached\_to\_field” → df, …)).
- Set f from Platform.get\_doc(file\_data).
- Set f.flags.ignore\_permissions from true.
- Attempt the following.
  - Evaluate f.insert().
- On failure (Platform.DuplicateEntryError).
  - Return Platform.get\_doc(“File”, f.duplicate\_entry).
- Return f.

**Values supplied outside this operation** selected callable from get\_hook\_method(“write\_file”, fallback = save\_file\_on\_filesystem).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0480.json#L284) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1342) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L138)
