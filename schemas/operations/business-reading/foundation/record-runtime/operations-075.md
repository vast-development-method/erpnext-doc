# Record lifecycle and persistence · operations 75

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Platformclient

<a id="op-408299a5d0f86e"></a>
### Platform Client.exit context

`operation_foundation_frappeclient_business_behavior_foundation_client_exit`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate self.logout().

If control reaches the end, it returns no value.

**Methods declared on this owner** [logout](operations-075.md#op-c57651f6b22a7e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L2302) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L314)

<a id="op-add448e267054c"></a>
### Platform Client.login

`operation_foundation_frappeclient_business_behavior_foundation_client_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, username, password.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** AuthError, SiteExpiredError, SiteUnreachableError.

**Local structure** 3 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L116) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1558) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L323)

<a id="op-b845febdea48a5"></a>
### Platform Client.setup key authentication headers

`operation_foundation_frappeclient_business_behavior_foundation_client_setup_key_authentication_headers`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L2817) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1568) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L333)

<a id="op-c57651f6b22a7e"></a>
### Platform Client.logout

`operation_foundation_frappeclient_business_behavior_foundation_client_logout`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L3112) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1559) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L324)

<a id="op-81768d46e91bac"></a>
### Platform Client.get list

`operation_foundation_frappeclient_business_behavior_foundation_client_get_list`

**Inputs** self, doctype, fields = “&#91;"name"&#93;”, filters = no value, limit\_start = 0, limit\_page\_length = no value, order\_by = no value, group\_by = no value.

**Explicit results** self.post\_process(res).

**Local steps**

- If not isinstance(fields, str).
  - Set fields from json.dumps(fields).
- Set params from mapping(“fields” → fields, “order\_by” → order\_by, “group\_by” → group\_by).
- If filters.
  - Set params at “filters” from json.dumps(filters).
- If limit\_page\_length is distinct from no value.
  - Set params at “limit\_start” from limit\_start.
  - Set params at “limit\_page\_length” from limit\_page\_length.
- Set res from self.session.get(((self.url + “/api/resource/”) + doctype), params = params, verify = self.verify, headers = self.headers).
- Return self.post\_process(res).

**Methods declared on this owner** [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L3227) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L316)

<a id="op-3c5fbb3a6f1db3"></a>
### Platform Client.insert

`operation_foundation_frappeclient_business_behavior_foundation_client_insert`

**Inputs** self, doc.

**Explicit results** Platform.\_dict(self.post\_process(res)).

**Local steps**

- Set res from self.session.post(((self.url + “/api/resource/”) + doc.get(“doctype”)), data = mapping(“data” → Platform.as\_json(doc)), verify = self.verify, headers = self.headers).
- Return Platform.\_dict(self.post\_process(res)).

**Methods declared on this owner** [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L3692) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1556) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L321)

<a id="op-9f1f71812ccb72"></a>
### Platform Client.insert many

`operation_foundation_frappeclient_business_behavior_foundation_client_insert_many`

**Inputs** self, docs.

**Explicit results** self.post\_request(mapping(“cmd” → “Platform.client.insert\_many”, “docs” → Platform.as\_json(docs))).

**Local steps**

- Return self.post\_request(mapping(“cmd” → “Platform.client.insert\_many”, “docs” → Platform.as\_json(docs))).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L3917) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1557) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L322)

<a id="op-85dec2cafe37ed"></a>
### Platform Client.update

`operation_foundation_frappeclient_business_behavior_foundation_client_update`

**Inputs** self, doc.

**Explicit results** Platform.\_dict(self.post\_process(res)).

**Local steps**

- Set url from ((((self.url + “/api/resource/”) + doc.get(“doctype”)) + “/”) + cstr(doc.get(“name”))).
- Set res from self.session.put(url, data = mapping(“data” → Platform.as\_json(doc)), verify = self.verify, headers = self.headers).
- Return Platform.\_dict(self.post\_process(res)).

**Methods declared on this owner** [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L4063) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1570) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L335)

<a id="op-f2479bfacd548c"></a>
### Platform Client.bulk update

`operation_foundation_frappeclient_business_behavior_foundation_client_bulk_update`

**Inputs** self, docs.

**Explicit results** self.post\_request(mapping(“cmd” → “Platform.client.bulk\_update”, “docs” → Platform.as\_json(docs))).

**Local steps**

- Return self.post\_request(mapping(“cmd” → “Platform.client.bulk\_update”, “docs” → Platform.as\_json(docs))).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L4351) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L310)

<a id="op-45d0ef9ab7c2f0"></a>
### Platform Client.delete

`operation_foundation_frappeclient_business_behavior_foundation_client_delete`

**Inputs** self, doctype, name.

**Explicit results** self.post\_request(mapping(“cmd” → “Platform.client.delete”, “doctype” → doctype, “name” → name)).

**Local steps**

- Return self.post\_request(mapping(“cmd” → “Platform.client.delete”, “doctype” → doctype, “name” → name)).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L4497) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L312)

<a id="op-3584cf3818bacd"></a>
### Platform Client.submit

`operation_foundation_frappeclient_business_behavior_foundation_client_submit`

**Inputs** self, doc.

**Explicit results** self.post\_request(mapping(“cmd” → “Platform.client.submit”, “doc” → Platform.as\_json(doc))).

**Local steps**

- Return self.post\_request(mapping(“cmd” → “Platform.client.submit”, “doc” → Platform.as\_json(doc))).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L4653) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1569) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L334)

<a id="op-3bd7c8a5754bf9"></a>
### Platform Client.get value

`operation_foundation_frappeclient_business_behavior_foundation_client_get_value`

**Inputs** self, doctype, fieldname = no value, filters = no value.

**Explicit results** self.get\_request(mapping(“cmd” → “Platform.client.get\_value”, “doctype” → doctype, “fieldname” → (fieldname or “name”), “filters” → Platform.as\_json(filters))).

**Local steps**

- Return self.get\_request(mapping(“cmd” → “Platform.client.get\_value”, “doctype” → doctype, “fieldname” → (fieldname or “name”), “filters” → Platform.as\_json(filters))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in fieldname → “name”.

**Methods declared on this owner** [get request](operations-075.md#op-624134ca8d2bc5).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L4799) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1554) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L319)

<a id="op-9eb6acd798b3f9"></a>
### Platform Client.set value

`operation_foundation_frappeclient_business_behavior_foundation_client_set_value`

**Inputs** self, doctype, docname, fieldname, value.

**Explicit results** self.post\_request(mapping(“cmd” → “Platform.client.set\_value”, “doctype” → doctype, “name” → docname, “fieldname” → fieldname, …)).

**Local steps**

- Return self.post\_request(mapping(“cmd” → “Platform.client.set\_value”, “doctype” → doctype, “name” → docname, “fieldname” → fieldname, …)).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L5017) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1567) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L332)

<a id="op-9fcd13cdc8517a"></a>
### Platform Client.cancel

`operation_foundation_frappeclient_business_behavior_foundation_client_cancel`

**Inputs** self, doctype, name.

**Explicit results** self.post\_request(mapping(“cmd” → “Platform.client.cancel”, “doctype” → doctype, “name” → name)).

**Local steps**

- Return self.post\_request(mapping(“cmd” → “Platform.client.cancel”, “doctype” → doctype, “name” → name)).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L5219) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L311)

<a id="op-4a3b69c5aaf4e0"></a>
### Platform Client.get doc

`operation_foundation_frappeclient_business_behavior_foundation_client_get_record`

**Inputs** self, doctype, name = empty text, filters = no value, fields = no value.

**Explicit results** self.post\_process(res).

**Local steps**

- Set params from mapping().
- If filters.
  - Set params at “filters” from json.dumps(filters).
- If fields.
  - Set params at “fields” from json.dumps(fields).
- Set res from self.session.get(((((self.url + “/api/resource/”) + doctype) + “/”) + cstr(name)), params = params, verify = self.verify, headers = self.headers).
- Return self.post\_process(res).

**Methods declared on this owner** [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L5375) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L317)

<a id="op-67a113ac249888"></a>
### Platform Client.rename doc

`operation_foundation_frappeclient_business_behavior_foundation_client_rename_record`

**Inputs** self, doctype, old\_name, new\_name.

**Explicit results** self.post\_request(params).

**Local steps**

- Set params from mapping(“cmd” → “Platform.client.rename\_doc”, “doctype” → doctype, “old\_name” → old\_name, “new\_name” → new\_name).
- Return self.post\_request(params).

**Methods declared on this owner** [post request](operations-075.md#op-999122e3360120).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L5703) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1566) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L331)

<a id="op-86552ac6c4ad9b"></a>
### Platform Client.migrate doctype

`operation_foundation_frappeclient_business_behavior_foundation_client_migrate_record_type`

**Inputs** self, doctype, filters = no value, update = no value, verbose = 1, exclude = no value, preprocess = no value.

**Record and data access** read “User” via exists · resolve a document from mapping(“doctype” → “User”, “email” → doc.get(“owner”), “first\_name” → doc.get(“owner”).split(“@”, 1) at 0) via get\_doc · resolve a document from doc via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “User”, “email” → doc.get(“owner”), “first\_name” → nested operand in the contract.get(“owner”).split(“@”, 1) at 0)) · call insert on new\_doc.

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- Set tables from mapping().
- For each df in meta.get\_table\_fields().
  - If verbose.
    - Evaluate print((“getting ” + df.options)).
  - Set tables at df.fieldname from self.get\_list(df.options, limit\_page\_length = 999999).
- If verbose.
  - Evaluate print((“getting ” + doctype)).
- Set docs from self.get\_list(doctype, limit\_page\_length = 999999, filters = filters).
- If tables.
  - Set docs from list of Platform.\_dict(doc) for doc drawn from docs.
    - Draw doc from docs.
  - Set docs\_map from mapping of doc.name → doc for doc drawn from docs.
    - Draw doc from docs.
  - For each fieldname in tables.
    - For each child in tables at fieldname.
      - Set child from Platform.\_dict(child).
      - If child.parent belongs to docs\_map.
        - Evaluate docs\_map at child.parent.setdefault(fieldname, list()).append(child).
- If verbose.
  - Evaluate print((“inserting ” + doctype)).
- For each doc in docs.
  - If (exclude and doc at “name” belongs to exclude).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in exclude → doc at “name” belongs to exclude.
    - Continue with the next iteration or loop test.
  - If preprocess.
    - Evaluate preprocess(doc).
  - If not doc.get(“owner”).
    - Set doc at “owner” from “Administrator”.
  - If (doctype differs from “User” and not Platform.db.exists(“User”, doc.get(“owner”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype differs from “User” → not Platform.db.exists(“User”, doc.get(“owner”)).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “User”, “email” → doc.get(“owner”), “first\_name” → nested operand in the contract.split(“@”, 1) at 0)).insert().
  - If update.
    - Evaluate doc.update(update).
  - Set doc at “doctype” from doctype.
  - Set new\_doc from Platform.get\_doc(doc).
  - Evaluate new\_doc.insert().
  - If not meta.istable.
    - If doctype differs from “Communication”.
      - Evaluate self.migrate\_doctype(“Communication”, mapping(“reference\_doctype” → doctype, “reference\_name” → doc at “name”), update = mapping(“reference\_name” → new\_doc.name), verbose = 0).
    - If doctype differs from “File”.
      - Evaluate self.migrate\_doctype(“File”, mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → doc at “name”), update = mapping(“attached\_to\_name” → new\_doc.name), verbose = 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get list](operations-075.md#op-81768d46e91bac).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L5890) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1560) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L325)

<a id="op-18544b0a0ccbed"></a>
### Platform Client.migrate single

`operation_foundation_frappeclient_business_behavior_foundation_client_migrate_single`

**Inputs** self, doctype.

**Record and data access** resolve a document from doc via get\_doc · read doctype via get\_single\_value.

**State and service calls** call insert on Platform.get\_doc(doc).

**Local steps**

- Set doc from self.get\_doc(doctype, doctype).
- Set doc from Platform.get\_doc(doc).
- Set doc.modified from Platform.db.get\_single\_value(doctype, “modified”).
- Evaluate Platform.get\_doc(doc).insert().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get doc](operations-075.md#op-4a3b69c5aaf4e0).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(doctype, “modified”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0239.json#L7333) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1561) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L326)

<a id="op-10db34ff8c5bb2"></a>
### Platform Client.get api

`operation_foundation_frappeclient_business_behavior_foundation_client_get_application_programming_interface`

**Inputs** self, method, params = no value.

**Explicit results** self.post\_process(res).

**Local steps**

- If params is identical to no value.
  - Set params from mapping().
- Set res from self.session.get(formatted text {self.url}/api/method/{method}, params = params, verify = self.verify, headers = self.headers).
- Return self.post\_process(res).

**Methods declared on this owner** [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L315)

<a id="op-e936e88f346447"></a>
### Platform Client.post api

`operation_foundation_frappeclient_business_behavior_foundation_client_post_application_programming_interface`

**Inputs** self, method, params = no value, json = no value.

**Explicit results** self.post\_process(res).

**Local steps**

- Set url from formatted text {self.url}/api/method/{method}.
- If json is distinct from no value.
  - Set headers from mapping(expand self.headers, “content-type” → “application/json”).
  - Set res from self.session.post(url, json = json, verify = self.verify, headers = headers).
- Otherwise.
  - Set res from self.session.post(url, data = self.preprocess((params or mapping())), verify = self.verify, headers = self.headers).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in params → mapping().
- Return self.post\_process(res).

**Methods declared on this owner** [preprocess](operations-075.md#op-7530544b9eded7), [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L214) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1562) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L327)

<a id="op-624134ca8d2bc5"></a>
### Platform Client.get request

`operation_foundation_frappeclient_business_behavior_foundation_client_get_request`

**Inputs** self, params.

**Explicit results** res.

**Local steps**

- Set res from self.session.get(self.url, params = self.preprocess(params), verify = self.verify, headers = self.headers).
- Set res from self.post\_process(res).
- Return res.

**Methods declared on this owner** [preprocess](operations-075.md#op-7530544b9eded7), [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L564) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1553) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L318)

<a id="op-999122e3360120"></a>
### Platform Client.post request

`operation_foundation_frappeclient_business_behavior_foundation_client_post_request`

**Inputs** self, data.

**Explicit results** res.

**Local steps**

- Set res from self.session.post(self.url, data = self.preprocess(data), verify = self.verify, headers = self.headers).
- Set res from self.post\_process(res).
- Return res.

**Methods declared on this owner** [preprocess](operations-075.md#op-7530544b9eded7), [post process](operations-075.md#op-a57338b7c40687).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L732) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1564) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L329)

<a id="op-7530544b9eded7"></a>
### Platform Client.preprocess

`operation_foundation_frappeclient_business_behavior_foundation_client_preprocess`

**Inputs** self, params.

**Explicit results** params.

**Local steps**

- For each tuple(key, value) in params.items().
  - If isinstance(value, (dict bitwise or list)).
    - Set params at key from json.dumps(value).
- Return params.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L900) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1565) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L330)

<a id="op-a57338b7c40687"></a>
### Platform Client.post process

`operation_foundation_frappeclient_business_behavior_foundation_client_post_process`

**Inputs** self, response.

**Explicit results** rjson at “message” · rjson at “data” · no value.

**Explicit failure paths** propagate active failure · PlatformException(exc).

**Local steps**

- Attempt the following.
  - Set rjson from response.json().
- On failure (ValueError).
  - Evaluate print(response.text).
  - Propagate the active failure.
- If (rjson and (rjson.get(“exc”) or rjson.get(“exc\_type”) or rjson.get(“errors”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in rjson → (rjson.get(“exc”) or rjson.get(“exc\_type”) or rjson.get(“errors”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rjson.get(“exc”) → rjson.get(“exc\_type”) → rjson.get(“errors”).
  - Attempt the following.
    - Set exception from empty text.
    - If rjson.get(“exc”).
      - Set exception from json.loads(rjson at “exc”) at 0.
    - Otherwise.
      - If rjson.get(“exc\_type”).
        - Set exception from json.loads(rjson at “exc\_type”) at 0.
      - Otherwise.
        - If errors bound to rjson.get(“errrors”).
          - Set exception from (errors at 0.get(“exception”) or errors at 0.get(“type”)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in errors at 0.get(“exception”) → errors at 0.get(“type”).
    - Set exc from (“PlatformClient Request Failed\\n\\n” + exception).
  - On failure (Exception).
    - Set exc from rjson.get(“exc”).
  - Raise PlatformException(exc).
- If “message” belongs to rjson.
  - Return rjson at “message”.
- Otherwise.
  - If “data” belongs to rjson.
    - Return rjson at “data”.
  - Otherwise.
    - Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L1050) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1563) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L328)
