# Shared value and file services · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Response

<a id="op-548ccaca22fc0c"></a>
### As pdf

`operation_foundation_utils_response_business_behavior_as_portable_document`

**Inputs** no declared parameters.

**Explicit results** response.

**Local steps**

- Set response from Response().
- Set response.mimetype from “application/pdf”.
- Set filename from Platform.response at “filename”.encode(“utf-8”).decode(“unicode-escape”, “ignore”).
- Evaluate response.headers.add(“Content-Disposition”, “inline”, filename = filename).
- Set response.data from Platform.response at “filecontent”.
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L4655) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1754) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L538)

<a id="op-1c10312ea75198"></a>
### As binary

`operation_foundation_utils_response_business_behavior_as_binary`

**Inputs** no declared parameters.

**Explicit results** response.

**Local steps**

- Set response from Response().
- Set response.mimetype from “application/octet-stream”.
- Set filename from Platform.response at “filename”.
- Set filename from filename.encode(“utf-8”).decode(“unicode-escape”, “ignore”).
- Evaluate response.headers.add(“Content-Disposition”, “attachment”, filename = filename).
- Set response.data from Platform.response at “filecontent”.
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L4856) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1751) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L535)

<a id="op-7d1bd744d2f45d"></a>
### Make logs

`operation_foundation_utils_response_business_behavior_make_logs`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies ApiVersion, get\_api\_version.
- Select the first matching pattern against get\_api\_version().
  - Pattern ApiVersion.V1.
    - Evaluate \_make\_logs\_v1().
  - Pattern ApiVersion.V2.
    - Evaluate \_make\_logs\_v2().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L5075) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1764) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L548)

<a id="op-c687287e8e2050"></a>
### Make logs v1

`operation_foundation_utils_response_business_behavior_make_logs_v_1`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies guess\_exception\_source.
- Set response from Platform.local.response.
- If (Platform.error\_log and is\_traceback\_allowed()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.error\_log → is\_traceback\_allowed().
  - If source bound to guess\_exception\_source((Platform.local.error\_log and nested operand in the contract.local.error\_log at 0 at “exc”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.error\_log → Platform.local.error\_log at 0 at “exc”.
    - Set response at “\_exc\_source” from source.
  - Set response at “exc” from orjson.dumps(list of nested operand in the contract.utils.cstr(d at “exc”) for d drawn from Platform.local.error\_log).decode().
    - Draw d from Platform.local.error\_log.
- If Platform.local.message\_log.
  - Set response at “\_server\_messages” from orjson.dumps(list of nested operand in the contract(nested operand in the contract).decode() for d drawn from Platform.local.message\_log).decode().
    - Draw d from Platform.local.message\_log.
- If (Platform.debug\_log and is\_traceback\_allowed()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.debug\_log → is\_traceback\_allowed().
  - Set response at “\_debug\_messages” from orjson.dumps(Platform.local.debug\_log).decode().
- If Platform.flags.error\_message.
  - Set response at “\_error\_message” from Platform.flags.error\_message.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L5199) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1765) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L549)

<a id="op-ab00a087bbf4bf"></a>
### Make logs v2

`operation_foundation_utils_response_business_behavior_make_logs_v_2`

**Inputs** no declared parameters.

**Local steps**

- Set response from Platform.local.response.
- If Platform.local.message\_log.
  - Set response at “messages” from Platform.local.message\_log.
- If (Platform.debug\_log and is\_traceback\_allowed()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.debug\_log → is\_traceback\_allowed().
  - Set response at “debug” from list of mapping(“message” → m) for m drawn from Platform.local.debug\_log.
    - Draw m from Platform.local.debug\_log.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L5721) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L550)

<a id="op-d5032adc5e62e7"></a>
### Json handler

`operation_foundation_utils_response_business_behavior_structured_data_handler`

**Inputs** obj.

**Explicit results** str(obj) · format\_timedelta(obj) · obj.\_\_json\_\_() · list(obj) · float(obj) · 2 additional forms in the steps below.

**Explicit failure paths** TypeError(formatted text Object of type {type(obj)} with value of {obj} is not JSON serializable).

**Local steps**

- If isinstance(obj, DateOrTimeTypes).
  - Return str(obj).
- Otherwise.
  - If isinstance(obj, timedelta).
    - Return format\_timedelta(obj).
  - Otherwise.
    - If isinstance(obj, LocalProxy).
      - Return str(obj).
    - Otherwise.
      - If hasattr(obj, “\_\_json\_\_”).
        - Return obj.\_\_json\_\_().
      - Otherwise.
        - If isinstance(obj, Iterable).
          - Return list(obj).
        - Otherwise.
          - If isinstance(obj, Decimal).
            - Return float(obj).
          - Otherwise.
            - If isinstance(obj, Match).
              - Return obj.string.
            - Otherwise.
              - If (type(obj) is identical to type or isinstance(obj, Exception)).
                - Evaluate in order, stop at the first true operand, otherwise use the last operand in type(obj) is identical to type → isinstance(obj, Exception).
                - Return repr(obj).
              - Otherwise.
                - If callable(obj).
                  - Return repr(obj).
                - Otherwise.
                  - If isinstance(obj, Path).
                    - Return str(obj).
                  - Otherwise.
                    - If isinstance(obj, UUID).
                      - Return str(obj).
                    - Otherwise.
                      - Raise TypeError(formatted text Object of type {type(obj)} with value of {obj} is not JSON serializable).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L5912) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L554)

<a id="op-c56feabc94e3f6"></a>
### As page

`operation_foundation_utils_response_business_behavior_as_page`

**Inputs** no declared parameters.

**Explicit results** get\_response(Platform.response at “route”, http\_status\_code = Platform.response.get(“http\_status\_code”)).

**Local steps**

- Bind dependencies get\_response.
- Return get\_response(Platform.response at “route”, http\_status\_code = Platform.response.get(“http\_status\_code”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L6531) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1753) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L537)

<a id="op-52459643265f3e"></a>
### Redirect

`operation_foundation_utils_response_business_behavior_redirect`

**Inputs** no declared parameters.

**Explicit results** werkzeug.utils.redirect(Platform.response.location).

**Local steps**

- Return werkzeug.utils.redirect(Platform.response.location).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L6629) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L551)

<a id="op-5e0dba66ef3c75"></a>
### Download backup

`operation_foundation_utils_response_business_behavior_download_backup`

**Inputs** path.

**Explicit results** send\_private\_file(path).

**Explicit failure paths** Forbidden(translated “You need to be logged in and have System Manager Role to be able to access backups.”) · validation helper with Platform.PermissionError — translated “Invalid backup path”.

**Local steps**

- Attempt the following.
  - Evaluate Platform.only\_for(tuple(“System Manager”, “Administrator”)).
  - Evaluate make\_access\_log(report\_name = “Backup”).
- On failure (Platform.PermissionError).
  - Raise Forbidden(translated “You need to be logged in and have System Manager Role to be able to access backups.”).
- Set filename from path.split(“/backups/”, 1) at 1.
- Set backup\_path from Platform.get\_site\_path(“private”, “backups”).
- Set requested\_path from Platform.get\_site\_path(“private”, “backups”, filename).
- Set is\_safe from check\_path\_safety(base\_path = backup\_path, requested\_path = requested\_path).
- If not is\_safe.
  - Call the validation error handler Platform.throw(translated “Invalid backup path”, Platform.PermissionError).
- Return send\_private\_file(path).

**Values supplied outside this operation** effective access from Platform.only\_for(tuple(“System Manager”, “Administrator”)).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L6687) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L543)

<a id="op-d78145c9598610"></a>
### Download private file

`operation_foundation_utils_response_business_behavior_download_private_file`

**Inputs** path.

**Declared result** Response.

**Explicit results** send\_private\_file(path.split(“/private”, 1) at 1, filename = file.file\_name).

**Explicit failure paths** Forbidden(translated “You don't have permission to access this file”).

**Local steps**

- Bind dependencies find\_file\_by\_url.
- If Platform.session.user equals “Guest”.
  - Raise Forbidden(translated “You don't have permission to access this file”).
- Set file from find\_file\_by\_url(path, name = Platform.form\_dict.fid).
- If not file.
  - Raise Forbidden(translated “You don't have permission to access this file”).
- Evaluate make\_access\_log(doctype = “File”, document = file.name, file\_type = os.path.splitext(path) at negative 1 at slice 1 to no value).
- Return send\_private\_file(path.split(“/private”, 1) at 1, filename = file.file\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0499.json#L7081) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1760) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L544)

<a id="op-f6373b65ced549"></a>
### Send private file

`operation_foundation_utils_response_business_behavior_send_private_file`

**Inputs** path, filename = no value.

**Declared result** Response.

**Explicit results** response.

**Explicit failure paths** NotFound.

**Local steps**

- Set path from os.path.join(Platform.local.conf.get(“private\_path”, “private”), path.strip(“/”)).
- Set filename from (filename or os.path.basename(path)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filename → os.path.basename(path).
- Set extension from os.path.splitext(path) at 1.
- Set as\_attachment from extension.lower() belongs to FORCE\_DOWNLOAD\_EXTENSIONS.
- If Platform.local.request.headers.get(“X-Use-X-Accel-Redirect”).
  - Set path from (“/protected/” + path).
  - Set response from Response().
  - Set response.headers at “X-Accel-Redirect” from quote(Platform.utils.encode(path)).
  - Set response.headers at “Cache-Control” from “private,max-age=3600,stale-while-revalidate=86400”.
  - Set response.headers at “Accept-Ranges” from “bytes”.
  - Set response.headers at “Content-Type” from (mimetypes.guess\_type(filename) at 0 or “application/octet-stream”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in mimetypes.guess\_type(filename) at 0 → “application/octet-stream”.
  - If as\_attachment.
    - Set response.headers at “Content-Disposition” from formatted text attachment; filename\*=UTF-8''{quote(filename)}.
- Otherwise.
  - Set filepath from Platform.utils.get\_site\_path(path).
  - If not os.path.exists(filepath).
    - Raise NotFound.
  - Set response from werkzeug.utils.send\_file(filepath, environ = Platform.local.request.environ, conditional = true, as\_attachment = as\_attachment, download\_name = filename).
- Return response.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L553)

<a id="op-537787c4289b3a"></a>
### Handle session stopped

`operation_foundation_utils_response_business_behavior_handle_session_stopped`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L742) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1761) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L545)

## Service · Safe exec

<a id="op-5f0316f9650db8"></a>
### Namespace Dict.getattr

`operation_foundation_utils_safe_exec_business_behavior_namespace_mapping_getattr`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, key.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L2028) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L586)

<a id="op-c3ec0224630ef4"></a>
### Namespace Dict.getattr.default function

`operation_foundation_utils_safe_exec_business_behavior_namespace_mapping_getattr_default_function`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** args, kwargs.

**Locally raised failures** AttributeError.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0549.json#L1095) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L587)

<a id="op-c92c73b3a5a2a6"></a>
### Platform Transformer.check name

`operation_foundation_utils_safe_exec_business_behavior_foundation_transformer_check_name`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, node, name, args, kwargs.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L2235) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1780) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L562)

<a id="op-f4c281a573a069"></a>
### Platform Print Collector.call print

`operation_foundation_utils_safe_exec_business_behavior_foundation_print_collector_call_print`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, objects, kwargs.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L2368) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L561)

<a id="op-e3dd642ba92230"></a>
### Is safe exec enabled

`operation_foundation_utils_safe_exec_business_behavior_is_safe_exec_enabled`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L2536) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L579)

<a id="op-0e6e96137b34c5"></a>
### Is render exec enabled

`operation_foundation_utils_safe_exec_business_behavior_is_render_exec_enabled`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L65) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L578)

<a id="op-ebde1667de6075"></a>
### Safe exec

`operation_foundation_utils_safe_exec_business_behavior_safe_exec`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** script, \_globals, \_locals, restrict\_commit\_rollback, script\_filename.

**Explicit result forms** a structured result.

**Observed service boundaries** validation or user-notification service.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L2706) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L594)

<a id="op-999ca0200b3227"></a>
### Compile code

`operation_foundation_utils_safe_exec_business_behavior_compile_code`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** script, filename, mode.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L3284) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L558)

<a id="op-b26bc2a9a31a05"></a>
### Safe eval

`operation_foundation_utils_safe_exec_business_behavior_safe_evaluate`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** code, eval\_globals, eval\_locals.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L67) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1811) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L593)

<a id="op-cdd0b0f9d03762"></a>
### Validate safe eval syntax

`operation_foundation_utils_safe_exec_business_behavior_validate_safe_evaluate_syntax`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** code.

**Locally raised failures** SyntaxError.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L3700) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1834) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L615)

<a id="op-c9b863cf724451"></a>
### Safe exec flags

`operation_foundation_utils_safe_exec_business_behavior_safe_exec_flags`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** no parameters.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L68) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L595)

<a id="op-3e65ebd8f9cf48"></a>
### Safe Doc.initialize

`operation_foundation_utils_safe_exec_business_behavior_safe_record_initialize`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, args, kwargs.

**Local structure** 2 condition or selection sites, 2 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0500.json#L4088) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L603)
