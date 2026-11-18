# Integration and transport · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Google oauth

<a id="op-9674e7df885276"></a>
### Google OAuth.get google service object

`operation_foundation_integrations_google_delegated_authorization_business_behavior_google_o_authentication_get_google_service_object`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, access\_token, refresh\_token.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L1135) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1904) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L642)

<a id="op-dfc11fe61c0048"></a>
### Handle response

`operation_foundation_integrations_google_delegated_authorization_business_behavior_handle_response`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** response, error\_title, error\_message, raise\_err.

**Explicit result forms** a structured result, a value selected from the current context.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L1473) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1908) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L646)

<a id="op-6ccb7305a26368"></a>
### Is valid access token

`operation_foundation_integrations_google_delegated_authorization_business_behavior_is_valid_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** access\_token.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L1780) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1909) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L647)

<a id="op-b41240f8f0cba9"></a>
### Callback

`operation_foundation_integrations_google_delegated_authorization_business_behavior_callback`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** state, code, error.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** transaction control.

**Local structure** 4 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L1922) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1899) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L637)

## Record · Google settings

[Record definition](../../../../data/record-types/google_settings.json)

<a id="op-acc20f1e41f535"></a>
### Get file picker settings

`operation_foundation_integrations_record_definitions_google_settings_business_behavior_get_file_picker_settings`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Google Settings” via get\_cached\_doc.

**Explicit results** mapping() · mapping(“enabled” → true, “appId” → google\_settings.app\_id, “clientId” → google\_settings.client\_id).

**Local steps**

- Set google\_settings from Platform.get\_cached\_doc(“Google Settings”).
- If not (google\_settings.enable and google\_settings.google\_drive\_picker\_enabled).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in google\_settings.enable → google\_settings.google\_drive\_picker\_enabled.
  - Return mapping().
- Return mapping(“enabled” → true, “appId” → google\_settings.app\_id, “clientId” → google\_settings.client\_id).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Google Settings”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L5119) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L25) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L751)

## Service · Handler

<a id="op-482660bbc46881"></a>
### Handle

`operation_foundation_handler_business_behavior_handle`

**Inputs** no declared parameters.

**Explicit results** data.

**Local steps**

- Set cmd from Platform.local.form\_dict.cmd.
- Set data from no value.
- If cmd differs from “login”.
  - Set data from execute\_cmd(cmd).
- If data is distinct from no value.
  - If isinstance(data, Response).
    - Return data.
  - Set Platform.response at “message” from data.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L5136) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L415)

<a id="op-d3babffae8d074"></a>
### Execute cmd

`operation_foundation_handler_business_behavior_execute_command`

**Inputs** cmd, from\_async = false.

**Explicit results** run\_server\_script(server\_script) · Platform.call(method, expanded names Platform.form\_dict).

**Explicit failure paths** validation helper — translated “Failed to get method for command {0} with {1}”.format(cmd, str(e)).

**Local steps**

- Set cmd from Platform.override\_whitelisted\_method(cmd).
- Set server\_script from get\_server\_script\_map().get(“\_api”, mapping()).get(cmd).
- If server\_script.
  - Return run\_server\_script(server\_script).
- Attempt the following.
  - Set method from get\_attr(cmd).
- On failure (Exception) bound to e.
  - Call the validation error handler Platform.throw(translated “Failed to get method for command {0} with {1}”.format(cmd, str(e))).
- If from\_async.
  - Set method from method.queue.
- If method differs from run\_doc\_method.
  - Evaluate is\_whitelisted(method).
  - Evaluate is\_valid\_http\_method(method).
- Return Platform.call(method, expanded names Platform.form\_dict).

**Values supplied outside this operation** selected callable from get\_attr(cmd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L15) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L413)

<a id="op-749c1370de68a3"></a>
### Run server script

`operation_foundation_handler_business_behavior_run_server_script`

**Inputs** server\_script.

**Record and data access** resolve a document from “Server Script” via get\_doc.

**Explicit results** response.

**Local steps**

- Set response from Platform.get\_doc(“Server Script”, server\_script).execute\_method().
- If response differs from mapping().
  - Return response.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L5759) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L419)

<a id="op-ba4088efb157b6"></a>
### Is valid http method

`operation_foundation_handler_business_behavior_is_valid_hypertext_transfer_protocol_method`

**Inputs** method.

**Explicit results** no value.

**Local steps**

- If Platform.flags.in\_safe\_exec.
  - Return no value.
- If hasattr(Platform.local, “job”).
  - Return no value.
- Set http\_method from Platform.local.request.method.
- If http\_method does not belong to Platform.allowed\_http\_methods\_for\_whitelisted\_func at method.
  - Evaluate Platform.throw\_permission\_error().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L5868) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L416)

<a id="op-c9f4412d7b0a7f"></a>
### Logout

`operation_foundation_handler_business_behavior_logout`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** transaction control.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L6035) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L417)

<a id="op-4c5cfd7f43aeca"></a>
### Web logout

`operation_foundation_handler_business_behavior_web_logout`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** transaction control.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0243.json#L6146) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L421)

<a id="op-08250280ded128"></a>
### Upload file

`operation_foundation_handler_business_behavior_upload_file`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true, methods = list(“POST”)).

**Record and data access** read “File” via get\_value · resolve a document from mapping(“doctype” → “File”, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, “attached\_to\_field” → fieldname, …) via get\_doc.

**State and service calls** call save on Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, “attached\_to\_field” → fieldname, …)).

**Explicit results** no value · method() · Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, “attached\_to\_field” → fieldname, …)).save(ignore\_permissions = ignore\_permissions).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Guests are not allowed to upload files for {0} Doctype”.format(target\_doctype) · Platform.PermissionError · validation helper — translated “You can only upload JPG, PNG, GIF, PDF, TXT, CSV or Microsoft documents.”.

**Local steps**

- Set user from no value.
- If Platform.session.user equals “Guest”.
  - If Platform.get\_system\_settings(“allow\_guests\_to\_upload\_files”).
    - Set ignore\_permissions from true.
    - Set guest\_allowed\_docs from Platform.get\_system\_settings(“allowed\_doctypes\_for\_guest\_uploads”).
    - If guest\_allowed\_docs.
      - Set target\_doctype from Platform.form\_dict.doctype.
      - Set allowed\_docs from guest\_allowed\_docs.splitlines().
      - Set allowed\_docs from list of doc.strip() for doc drawn from allowed\_docs where doc.strip().
        - Draw doc from allowed\_docs, keep a combination only if (doc.strip()).
      - If (allowed\_docs and target\_doctype does not belong to allowed\_docs).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed\_docs → target\_doctype does not belong to allowed\_docs.
        - Call the validation error handler Platform.throw(translated “Guests are not allowed to upload files for {0} Doctype”.format(target\_doctype), Platform.PermissionError).
  - Otherwise.
    - Raise Platform.PermissionError.
- Otherwise.
  - Set user from Platform.get\_lazy\_doc(“User”, Platform.session.user).
  - Set ignore\_permissions from false.
- Set files from Platform.request.files.
- Set is\_private from Platform.form\_dict.is\_private.
- Set doctype from Platform.form\_dict.doctype.
- Set docname from Platform.form\_dict.docname.
- Set fieldname from Platform.form\_dict.fieldname.
- Set file\_url from Platform.form\_dict.file\_url.
- Set folder from (Platform.form\_dict.folder or “Home”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.folder → “Home”.
- Set method from Platform.form\_dict.method.
- Set filename from Platform.form\_dict.file\_name.
- Set optimize from Platform.form\_dict.optimize.
- Set content from no value.
- If library\_file bound to Platform.form\_dict.get(“library\_file\_name”).
  - Evaluate Platform.has\_permission(“File”, doc = library\_file, throw = true).
  - Set doc from Platform.get\_value(“File”, Platform.form\_dict.library\_file\_name, list(“is\_private”, “file\_url”, “file\_name”), as\_dict = true).
  - Set is\_private from doc.is\_private.
  - Set file\_url from doc.file\_url.
  - Set filename from doc.file\_name.
- If not ignore\_permissions.
  - Evaluate check\_write\_permission(doctype, docname).
- If “file” belongs to files.
  - Set file from files at “file”.
  - Set filename from file.filename.
  - If Platform.form\_dict.get(“chunk\_index”) is distinct from no value.
    - Set current\_chunk from int(Platform.form\_dict.chunk\_index).
    - Set total\_chunks from int(Platform.form\_dict.total\_chunk\_count).
    - Set offset from int(Platform.form\_dict.chunk\_byte\_offset).
  - Otherwise.
    - Set offset from 0.
    - Set current\_chunk from 0.
    - Set total\_chunks from 1.
  - Set temp\_path from Path(get\_files\_path((“.temp-” + get\_safe\_file\_name(filename)), is\_private = is\_private)).
  - Within temp\_path.open(“ab” when current\_chunk &gt; 0, otherwise “wb”) bound as f.
    - Value choice on current\_chunk &gt; 0 — true gives “ab”, false gives “wb”.
    - Set total\_file\_size from (Platform.form\_dict.total\_file\_size or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.form\_dict.total\_file\_size → 0.
    - Evaluate f.seek(offset).
    - Evaluate f.write(file.stream.read()).
    - If (not f.tell() ≥ int(total\_file\_size) or current\_chunk differs from (total\_chunks − 1)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not f.tell() ≥ int(total\_file\_size) → current\_chunk differs from (total\_chunks − 1).
      - Return no value.
  - Set content from temp\_path.read\_bytes().
  - Evaluate temp\_path.unlink().
  - Set content\_type from guess\_type(filename) at 0.
  - If (optimize and content\_type and content\_type.startswith(“image/”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in optimize → content\_type → content\_type.startswith(“image/”).
    - Bind dependencies optimize\_image.
    - Set args from mapping(“content” → content, “content\_type” → content\_type).
    - If Platform.form\_dict.max\_width.
      - Set args at “max\_width” from int(Platform.form\_dict.max\_width).
    - If Platform.form\_dict.max\_height.
      - Set args at “max\_height” from int(Platform.form\_dict.max\_height).
    - Set content from optimize\_image(expanded names args).
- Set Platform.local.uploaded\_file\_url from file\_url.
- Set Platform.local.uploaded\_file from content.
- Set Platform.local.uploaded\_filename from filename.
- If (content is distinct from no value and (Platform.session.user equals “Guest” or (user and not user.has\_desk\_access()))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in content is distinct from no value → (Platform.session.user equals “Guest” or (user and not user.has\_desk\_access())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.session.user equals “Guest” → (user and not user.has\_desk\_access()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in user → not user.has\_desk\_access().
  - Set filetype from guess\_type(filename) at 0.
  - If filetype does not belong to ALLOWED\_MIMETYPES.
    - Call the validation error handler Platform.throw(translated “You can only upload JPG, PNG, GIF, PDF, TXT, CSV or Microsoft documents.”).
- If method.
  - Set method from Platform.get\_attr(method).
  - Evaluate is\_whitelisted(method).
  - Evaluate is\_valid\_http\_method(method).
  - Return method().
- Otherwise.
  - Return Platform.get\_doc(mapping(“doctype” → “File”, “attached\_to\_doctype” → doctype, “attached\_to\_name” → docname, “attached\_to\_field” → fieldname, …)).save(ignore\_permissions = ignore\_permissions).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“allow\_guests\_to\_upload\_files”), Platform.get\_system\_settings(“allowed\_doctypes\_for\_guest\_uploads”) · effective access from Platform.has\_permission(“File”, doc = library\_file, throw = true) · selected callable from Platform.get\_attr(method).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L16) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L420)

<a id="op-5539c85337a8ed"></a>
### Check write permission

`operation_foundation_handler_business_behavior_check_write_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, name.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L2490) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L411)

<a id="op-26bdf98ebde1dc"></a>
### Download file

`operation_foundation_handler_business_behavior_download_file`

**Inputs** file\_url.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit failure paths** Platform.PermissionError.

**Local steps**

- Set file from find\_file\_by\_url(file\_url).
- If not file.
  - Raise Platform.PermissionError.
- Set Platform.local.response.filename from os.path.basename(file\_url).
- Set Platform.local.response.filecontent from file.get\_content().
- Set Platform.local.response.type from “download”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L2758) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L412)

<a id="op-0c11ef4c18897a"></a>
### Get attr

`operation_foundation_handler_business_behavior_get_attr`

**Inputs** cmd.

**Explicit results** method.

**Local steps**

- If “.” belongs to cmd.
  - Set method from Platform.get\_attr(cmd).
- Otherwise.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
  - Set method from globals() at cmd.
- Return method.

**Values supplied outside this operation** selected callable from Platform.get\_attr(cmd).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L2984) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L414)

<a id="op-617cd97887a118"></a>
### Run doc method

`operation_foundation_handler_business_behavior_run_record_method`

**Inputs** method, docs = no value, dt = no value, dn = no value, arg = no value, args = no value.

**Record and data access** resolve a document from dt via get\_doc · resolve a document from docs via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — “'dn' must be a string or an integer”.

**Local steps**

- Bind dependencies signature.
- If (not args and arg).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args → arg.
  - Set args from arg.
- If dt.
  - If not dn.
    - Set dn from dt.
  - If not isinstance(dn, (str bitwise or int)).
    - Call the validation error handler Platform.throw(“'dn' must be a string or an integer”).
  - Set doc from Platform.get\_doc(dt, dn, check\_permission = true).
- Otherwise.
  - Set docs from Platform.parse\_json(docs).
  - Set doc from Platform.get\_doc(docs, check\_permission = true).
  - Set doc.\_original\_modified from doc.modified.
  - Evaluate doc.check\_if\_latest().
- If not doc.
  - Evaluate Platform.throw\_permission\_error().
- Attempt the following.
  - Set args from Platform.parse\_json(args).
- On failure (ValueError).
  - Take no action here.
- Set method\_obj from getattr(doc, method).
- Set fn from getattr(method\_obj, “\_\_func\_\_”, method\_obj).
- Evaluate is\_whitelisted(fn).
- Evaluate is\_valid\_http\_method(fn).
- Set fnargs from list(signature(method\_obj).parameters).
- If (not fnargs or (len(fnargs) equals 1 and fnargs at 0 equals “self”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not fnargs → (len(fnargs) equals 1 and fnargs at 0 equals “self”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(fnargs) equals 1 → fnargs at 0 equals “self”.
  - Set response from doc.run\_method(method).
- Otherwise.
  - If (“args” belongs to fnargs or not isinstance(args, dict)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “args” belongs to fnargs → not isinstance(args, dict).
    - Set response from doc.run\_method(method, args).
  - Otherwise.
    - Set response from doc.run\_method(method, expanded names args).
- Evaluate doc.apply\_fieldlevel\_read\_permissions().
- Evaluate Platform.response.docs.append(doc).
- If response is identical to no value.
  - Return no value.
- If cint(Platform.form\_dict.get(“as\_csv”)).
  - Evaluate build\_csv\_response(response, translated doc.doctype.replace(one space, empty text)).
  - Return no value.
- Set Platform.response at “message” from response.
- Evaluate add\_data\_to\_monitor(methodname = method).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, method), getattr(method\_obj, “\_\_func\_\_”, method\_obj) and 3 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L3158) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L418)

## Service · Inbox

<a id="op-092d5de9a555e4"></a>
### Get email accounts

`operation_foundation_email_inbox_business_behavior_get_email_accounts`

**Inputs** user = no value.

**Record and data access** read “User Email” via get\_all.

**Explicit results** mapping(“email\_accounts” → list(), “all\_accounts” → empty text) · mapping(“email\_accounts” → email\_accounts, “all\_accounts” → all\_accounts).

**Local steps**

- If not user.
  - Set user from Platform.session.user.
- Set email\_accounts from list().
- Set accounts from Platform.get\_all(“User Email”, filters = mapping(“parent” → user), fields = list(“email\_account”, “email\_id”, “enable\_outgoing”), distinct = true, order\_by = “idx”).
- If not accounts.
  - Return mapping(“email\_accounts” → list(), “all\_accounts” → empty text).
- Set all\_accounts from “,”.join(generator of account.get(“email\_account”) for account drawn from accounts).
  - Draw account from accounts.
- If len(accounts) &gt; 1.
  - Evaluate email\_accounts.append(mapping(“email\_account” → all\_accounts, “email\_id” → “All Accounts”)).
- Evaluate email\_accounts.extend(accounts).
- Evaluate email\_accounts.extend(list(mapping(“email\_account” → “Sent”, “email\_id” → “Sent Mail”), mapping(“email\_account” → “Spam”, “email\_id” → “Spam”), mapping(“email\_account” → “Trash”, “email\_id” → “Trash”))).
- Return mapping(“email\_accounts” → email\_accounts, “all\_accounts” → all\_accounts).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L5056) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1062) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1495)

<a id="op-d2beaf8c97d698"></a>
### Create email flag queue

`operation_foundation_email_inbox_business_behavior_create_email_flag_queue`

**Inputs** names, action.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Email Flag Queue) · resolve a document from mapping(“uid” → uid, “action” → action, “communication” → name, “doctype” → “Email Flag Queue”, …) via get\_doc.

**State and service calls** request delete\_doc for “Email Flag Queue” · call save on flag\_queue · call db\_set on doc.

**Explicit results** no value.

**Local steps**

- Bind local operation mark\_as\_seen\_unseen for subsequent calls.
- If not all(list(names, action)).
  - Return no value.
- For each name in Platform.parse\_json(names).
  - Set doc from Platform.get\_lazy\_doc(“Communication”, name, check\_permission = “read”).
  - Set tuple(uid, seen\_status, email\_account) from tuple(doc.uid, doc.seen, doc.email\_account).
  - If not uid.
    - Set uid from negative 1.
  - If not seen\_status.
    - Set seen\_status from 0.
  - If (not uid or uid equals negative 1).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not uid → uid equals negative 1.
    - Continue with the next iteration or loop test.
  - Set seen from 1 when action equals “Read”, otherwise 0.
    - Value choice on action equals “Read” — true gives 1, false gives 0.
  - If ((action equals “Read” and seen\_status equals 0) or (action equals “Unread” and seen\_status equals 1)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in (action equals “Read” and seen\_status equals 0) → (action equals “Unread” and seen\_status equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in action equals “Read” → seen\_status equals 0.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in action equals “Unread” → seen\_status equals 1.
    - Set create\_new from true.
    - Set email\_flag\_queue from Platform.db.sql(query text (SELECT, Email Flag Queue), mapping(“name” → name), as\_dict = true).
    - For each queue in email\_flag\_queue.
      - If queue.action differs from action.
        - Evaluate Platform.delete\_doc(“Email Flag Queue”, queue.name, ignore\_permissions = true, force = true).
      - Otherwise.
        - If queue.action equals action.
          - Set create\_new from false.
    - If create\_new.
      - Set flag\_queue from Platform.get\_doc(mapping(“uid” → uid, “action” → action, “communication” → name, “doctype” → “Email Flag Queue”, …)).
      - Evaluate flag\_queue.save(ignore\_permissions = true).
      - Evaluate doc.db\_set(“seen”, seen, update\_modified = false).
      - Evaluate mark\_as\_seen\_unseen(doc, action).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L73) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1060) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1493)

<a id="op-ff3a952e5f77a8"></a>
### Create email flag queue.mark as seen unseen

`operation_foundation_email_inbox_business_behavior_create_email_flag_queue_mark_as_seen_unseen`

**Inputs** doc, action.

**State and service calls** call db\_set on doc.

**Local steps**

- If action equals “Read”.
  - Evaluate doc.add\_seen().
- Otherwise.
  - Set \_seen from json.loads((doc.\_seen or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.\_seen → “&#91;&#93;”.
  - Set \_seen from list of user for user drawn from \_seen where Platform.session.user differs from user.
    - Draw user from \_seen, keep a combination only if (Platform.session.user differs from user).
  - Evaluate doc.db\_set(“\_seen”, json.dumps(\_seen), update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L6839) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1061) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1494)

<a id="op-1e2c4f5bfb729c"></a>
### Mark as closed open

`operation_foundation_email_inbox_business_behavior_mark_as_closed_open`

**Inputs** communication, status.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate set\_value(“Communication”, communication, “status”, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L7070) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1064) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1497)

<a id="op-f2c1b111d19777"></a>
### Move email

`operation_foundation_email_inbox_business_behavior_move_email`

**Inputs** communication, email\_account.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate set\_value(“Communication”, communication, “email\_account”, email\_account).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L7179) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1067) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1500)

<a id="op-fbbc4f4b72b343"></a>
### Mark as trash

`operation_foundation_email_inbox_business_behavior_mark_as_trash`

**Inputs** communication.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate set\_value(“Communication”, communication, “email\_status”, “Trash”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L7288) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1066) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1499)

<a id="op-82fd4426fd4264"></a>
### Mark as spam

`operation_foundation_email_inbox_business_behavior_mark_as_spam`

**Inputs** communication, sender.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Email Rule” via get\_value · resolve a document from mapping(“doctype” → “Email Rule”, “email\_id” → sender, “is\_spam” → 1) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Email Rule”, “email\_id” → sender, “is\_spam” → 1)).

**Local steps**

- Set email\_rule from Platform.db.get\_value(“Email Rule”, mapping(“email\_id” → sender)).
- If not email\_rule.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Email Rule”, “email\_id” → sender, “is\_spam” → 1)).insert(ignore\_permissions = true).
- Evaluate set\_value(“Communication”, communication, “email\_status”, “Spam”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L7385) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1065) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1498)

<a id="op-a8b84132c9a893"></a>
### Link communication to document

`operation_foundation_email_inbox_business_behavior_link_communication_to_document`

**Inputs** doc, reference\_doctype, reference\_name, ignore\_communication\_links.

**State and service calls** call save on doc.

**Local steps**

- If not ignore\_communication\_links.
  - Set doc.reference\_doctype from reference\_doctype.
  - Set doc.reference\_name from reference\_name.
  - Set doc.status from “Linked”.
  - Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0234.json#L7666) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1063) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1496)
