# Supporting services · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-fc07979b49783d"></a>
### Are same phone number

`operation_relationships_utils_initialize_business_behavior_are_same_phone_number`

**Inputs** number1, number2, default\_region = “IN”, validate = true.

**Explicit results** false · formatted1 equals formatted2.

**Local steps**

- Attempt the following.
  - Set parsed1 from phonenumbers.parse(number1, default\_region).
  - Set parsed2 from phonenumbers.parse(number2, default\_region).
  - If (validate and not (phonenumbers.is\_valid\_number(parsed1) and phonenumbers.is\_valid\_number(parsed2))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in validate → not (phonenumbers.is\_valid\_number(parsed1) and phonenumbers.is\_valid\_number(parsed2)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in phonenumbers.is\_valid\_number(parsed1) → phonenumbers.is\_valid\_number(parsed2).
    - Return false.
  - Set formatted1 from phonenumbers.format\_number(parsed1, phonenumbers.PhoneNumberFormat.E164).
  - Set formatted2 from phonenumbers.format\_number(parsed2, phonenumbers.PhoneNumberFormat.E164).
  - Return formatted1 equals formatted2.
- On failure (phonenumbers.NumberParseException).
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L519) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1735) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L165)

<a id="op-4e9b0e98582ed4"></a>
### Seconds to duration

`operation_relationships_utils_initialize_business_behavior_seconds_to_duration`

**Inputs** seconds.

**Declared result** str.

**Explicit results** “0s” · formatted text {hours}h {minutes}m {seconds}s · formatted text {hours}h {minutes}m · formatted text {hours}h {seconds}s · formatted text {minutes}m {seconds}s · 3 additional forms in the steps below.

**Local steps**

- If not seconds.
  - Return “0s”.
- Set hours from floor((seconds floor divide 3600)).
- Set minutes from floor(((seconds modulo or format 3600) floor divide 60)).
- Set seconds from floor(((seconds modulo or format 3600) modulo or format 60)).
- If (hours and minutes and seconds).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hours → minutes → seconds.
  - Return formatted text {hours}h {minutes}m {seconds}s.
- Otherwise.
  - If (hours and minutes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in hours → minutes.
    - Return formatted text {hours}h {minutes}m.
  - Otherwise.
    - If (hours and seconds).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in hours → seconds.
      - Return formatted text {hours}h {seconds}s.
    - Otherwise.
      - If (minutes and seconds).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in minutes → seconds.
        - Return formatted text {minutes}m {seconds}s.
      - Otherwise.
        - If hours.
          - Return formatted text {hours}h.
        - Otherwise.
          - If minutes.
            - Return formatted text {minutes}m.
          - Otherwise.
            - If seconds.
              - Return formatted text {seconds}s.
            - Otherwise.
              - Return “0s”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L867) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1747) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L177)

<a id="op-2c80ec5010e030"></a>
### Is admin

`operation_relationships_utils_initialize_business_behavior_is_admin`

**Inputs** user = no value.

**Declared result** bool.

**Explicit results** user equals “Administrator”.

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Return user equals “Administrator”.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L1419) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1738) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L168)

<a id="op-b65d2f91adff4f"></a>
### Is sales user

`operation_relationships_utils_initialize_business_behavior_is_sales_user`

**Inputs** user = no value.

**Declared result** bool.

**Explicit results** (is\_admin() or “Sales Manager” belongs to Platform.get\_roles(user) or “Sales User” belongs to Platform.get\_roles(user)).

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Return (is\_admin() or “Sales Manager” belongs to Platform.get\_roles(user) or “Sales User” belongs to Platform.get\_roles(user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_admin() → “Sales Manager” belongs to Platform.get\_roles(user) → “Sales User” belongs to Platform.get\_roles(user).

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L1517) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1740) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L170)

<a id="op-4830f85cc5905c"></a>
### Sales user only

`operation_relationships_utils_initialize_business_behavior_sales_user_only`

**Inputs** fn.

**Declared result** callable.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L1686) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1745) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L175)

<a id="op-ba2670c585cf9b"></a>
### Sales user only.wrapper

`operation_relationships_utils_initialize_business_behavior_sales_user_only_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(fn).

**Explicit results** fn(expanded args, expanded names kwargs).

**Explicit failure paths** validation helper with Platform.PermissionError.

**Local steps**

- If not is\_sales\_user().
  - Call the validation error handler Platform.throw(msg = translated “You are not permitted to access this resource.”, title = translated “Not Allowed”, exc = Platform.PermissionError).
- Return fn(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L1909) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1746) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L176)

<a id="op-80f647ec2197e4"></a>
### Is Platform version

`operation_relationships_utils_initialize_business_behavior_is_foundation_version`

**Inputs** version, above = false, below = false.

**Explicit results** major\_version ≥ target\_version · major\_version &lt; target\_version · major\_version equals target\_version.

**Local steps**

- Bind dependencies get\_Platform\_version.
- Set current\_version from get\_Platform\_version().
- Set major\_version from int(current\_version.split(“.”) at 0).
- Set target\_version from int(version.split(“.”) at 0).
- If above.
  - Return major\_version ≥ target\_version.
- If below.
  - Return major\_version &lt; target\_version.
- Return major\_version equals target\_version.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L2101) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1739) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L169)

<a id="op-5bdb8d943e87d5"></a>
### Should update modified

`operation_relationships_utils_initialize_business_behavior_should_update_modified`

**Inputs** doc.

**Declared result** bool.

**Record and data access** read “FCRM Settings” via get\_single\_value.

**Explicit results** false · true.

**Local steps**

- If not Platform.db.get\_single\_value(“FCRM Settings”, “update\_timestamp\_on\_new\_communication”).
  - Return false.
- If not (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Return false.
- If doc.reference\_doctype does not belong to list(“CRM Lead”, “CRM Deal”).
  - Return false.
- If doc.doctype does not belong to list(“Comment”, “Communication”).
  - Return false.
- Return true.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “update\_timestamp\_on\_new\_communication”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L2371) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1748) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L178)

<a id="op-60c7838506fd14"></a>
### Get communication status

`operation_relationships_utils_initialize_business_behavior_get_communication_status`

**Inputs** doc.

**Declared result** (str bitwise or no value).

**Record and data access** read “FCRM Settings” via get\_single\_value.

**Explicit results** no value · “Open” · “Replied”.

**Local steps**

- If doc.doctype differs from “Communication”.
  - Return no value.
- If not (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Return no value.
- If doc.sent\_or\_received does not belong to tuple(“Sent”, “Received”).
  - Return no value.
- Set auto\_reopen from Platform.db.get\_single\_value(“FCRM Settings”, “auto\_reopen\_on\_new\_communication”).
- Set auto\_replied from Platform.db.get\_single\_value(“FCRM Settings”, “auto\_mark\_replied\_on\_response”).
- If (doc.sent\_or\_received equals “Received” and auto\_reopen).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sent\_or\_received equals “Received” → auto\_reopen.
  - Return “Open”.
- Otherwise.
  - If (doc.sent\_or\_received equals “Sent” and auto\_replied).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sent\_or\_received equals “Sent” → auto\_replied.
    - Return “Replied”.
- Return no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“FCRM Settings”, “auto\_reopen\_on\_new\_communication”), Platform.db.get\_single\_value(“FCRM Settings”, “auto\_mark\_replied\_on\_response”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L2624) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1737) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L167)

<a id="op-81ff64ff3acd35"></a>
### Create lead from incoming email

`operation_relationships_utils_initialize_business_behavior_create_lead_from_incoming_email`

**Inputs** doc, method = no value.

**Record and data access** read “Email Account” via get\_value · read “CRM Lead” via exists · read “CRM Lead Source” via exists.

**State and service calls** request new\_doc for “CRM Lead” · call insert on lead · call save on doc.

**Explicit results** no value.

**Local steps**

- If doc.doctype differs from “Communication”.
  - Return no value.
- If (doc.sent\_or\_received differs from “Received” and doc.communication\_type differs from “Communication”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sent\_or\_received differs from “Received” → doc.communication\_type differs from “Communication”.
  - Return no value.
- If (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Return no value.
- If not doc.email\_account.
  - Return no value.
- Set create\_lead\_enabled from Platform.db.get\_value(“Email Account”, doc.email\_account, “create\_lead\_from\_incoming\_email”).
- If not create\_lead\_enabled.
  - Return no value.
- If Platform.db.exists(“CRM Lead”, mapping(“email” → doc.sender)).
  - Return no value.
- If \_is\_automated\_email\_sender(doc.sender).
  - Return no value.
- Set lead from Platform.new\_doc(“CRM Lead”).
- Set lead.email from doc.sender.
- If doc.sender\_full\_name.
  - Set lead.first\_name from doc.sender\_full\_name.split(one space) at 0.
  - Set lead.last\_name from doc.sender\_full\_name.split(one space) at negative 1 when len(doc.sender\_full\_name.split(one space)) &gt; 1, otherwise empty text.
    - Value choice on len(doc.sender\_full\_name.split(one space)) &gt; 1 — true gives doc.sender\_full\_name.split(one space) at negative 1, false gives empty text.
- Otherwise.
  - Set lead.first\_name from doc.sender.split(“@”) at 0.
- If Platform.db.exists(“CRM Lead Source”, “Email”).
  - Set lead.source from “Email”.
- Evaluate lead.insert(ignore\_permissions = true).
- Set doc.reference\_doctype from “CRM Lead”.
- Set doc.reference\_name from lead.name.
- Evaluate doc.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L39) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1736) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L166)

<a id="op-0fa94e548ef8b0"></a>
### Is automated email sender

`operation_relationships_binding_crm_utils_init_is_automated_email_sender`

**Inputs** sender.

**Declared result** bool.

**Explicit results** false · true · local.endswith(tuple(“-noreply”, “\_noreply”, “-no-reply”, “\_no-reply”)).

**Local steps**

- If (not sender or “@” does not belong to sender).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not sender → “@” does not belong to sender.
  - Return false.
- Set match from re.search(“&lt;?(&#91;^&lt;&gt;\\s&#93;+@&#91;^&lt;&gt;\\s&#93;+)&gt;?”, sender).
- Set address from match.group(1) when match, otherwise sender.
  - Value choice on match — true gives match.group(1), false gives sender.
- Set local from nested operand in the contract.split(“@”, 1) at 0.strip().lower().
- Set local from re.sub(“\\+.\*$”, empty text, local).
- If local belongs to \_AUTOMATED\_SENDER\_LOCAL\_PARTS.
  - Return true.
- Return local.endswith(tuple(“-noreply”, “\_noreply”, “-no-reply”, “\_no-reply”)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L229) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L385) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L366)

<a id="op-0975b64660f541"></a>
### On comment insert

`operation_relationships_utils_initialize_business_behavior_on_comment_insert`

**Inputs** doc, method = no value.

**State and service calls** enqueue with update\_modified\_background.

**Explicit results** no value.

**Local steps**

- If not (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Return no value.
- If (doc.reference\_doctype does not belong to list(“CRM Lead”, “CRM Deal”) or doc.comment\_type differs from “Comment”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.reference\_doctype does not belong to list(“CRM Lead”, “CRM Deal”) → doc.comment\_type differs from “Comment”.
  - Return no value.
- If not \_should\_update\_modified(doc).
  - Return no value.
- If (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Evaluate Platform.enqueue(update\_modified\_background, doctype = doc.reference\_doctype, docname = doc.reference\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(update\_modified\_background, doctype = doc.reference\_doctype, docname = doc.reference\_name).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L3740) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1741) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L171)

<a id="op-941c84d377489a"></a>
### Update modified background

`operation_relationships_utils_initialize_business_behavior_update_modified_background`

**Inputs** doctype, docname.

**State and service calls** request set\_value on doctype.

**Local steps**

- Evaluate Platform.db.set\_value(doctype, docname, “modified”, now(), update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L4032) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1749) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L179)

<a id="op-4782bce3c7b737"></a>
### On communication insert

`operation_relationships_utils_initialize_business_behavior_on_communication_insert`

**Inputs** doc, method = no value.

**Local steps**

- Evaluate create\_lead\_from\_incoming\_email(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L4144) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1742) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L172)

<a id="op-9029e81b045094"></a>
### On communication update

`operation_relationships_utils_initialize_business_behavior_on_communication_update`

**Inputs** doc, method = no value.

**Record and data access** read “Communication” via get\_last\_doc.

**State and service calls** request set\_value on doc.reference\_doctype.

**Explicit results** no value.

**Local steps**

- If not (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Return no value.
- If doc.reference\_doctype does not belong to list(“CRM Lead”, “CRM Deal”).
  - Return no value.
- Set should\_update\_modified from \_should\_update\_modified(doc).
- Set status from \_get\_communication\_status(doc).
- Set values from mapping().
- If should\_update\_modified.
  - Set values at “modified” from now().
- If status.
  - Set last\_communication from Platform.get\_last\_doc(“Communication”, mapping(“reference\_doctype” → doc.reference\_doctype, “reference\_name” → doc.reference\_name)).
  - If (last\_communication and last\_communication.name equals doc.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in last\_communication → last\_communication.name equals doc.name.
    - Set values at “communication\_status” from status.
- If not values.
  - Return no value.
- Evaluate Platform.db.set\_value(doc.reference\_doctype, doc.reference\_name, values, update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../relationships-decision-contracts/part-0067.json#L4224) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1743) · [Declaration location](../../../current-decisions/relationships/evidence/locations-002.tsv#L173)
