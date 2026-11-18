# Integrations and service calls · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · User permission

<a id="op-14770bf7f73158"></a>
### Mirror permission

`operation_relationships_integrations_enterprise_application_user_permission_business_behavior_mirror_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** src, target\_doctype, target\_value.

**Observed service boundaries** record lookup, record mutation request.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L1884) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1316) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1292)

## Service · Utils

<a id="op-bcdd50993a1056"></a>
### Should sync

`operation_relationships_integrations_enterprise_application_utils_business_behavior_should_sync`

**Inputs** no declared parameters.

**Declared result** bool.

**Record and data access** resolve a document from “Enterprise CRM Settings” via get\_cached\_doc.

**Explicit results** false · (bool(settings.enabled) and not settings.is\_Enterprise\_in\_different\_site).

**Local steps**

- If “Enterprise” does not belong to Platform.get\_installed\_apps().
  - Return false.
- Set settings from Platform.get\_cached\_doc(“Enterprise CRM Settings”).
- Return (bool(settings.enabled) and not settings.is\_Enterprise\_in\_different\_site).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(settings.enabled) → not settings.is\_Enterprise\_in\_different\_site.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Enterprise CRM Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L2208) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1328) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1304)

<a id="op-a9c71b864d8fdf"></a>
### Should push to Enterprise

`operation_relationships_integrations_enterprise_application_utils_business_behavior_should_push_to_enterprise`

**Inputs** no declared parameters.

**Declared result** bool.

**Record and data access** resolve a document from “Enterprise CRM Settings” via get\_cached\_doc.

**Explicit results** false · bool(settings.sync\_products).

**Local steps**

- If not should\_sync().
  - Return false.
- Set settings from Platform.get\_cached\_doc(“Enterprise CRM Settings”).
- Return bool(settings.sync\_products).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Enterprise CRM Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L2350) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1327) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1303)

<a id="op-a4a7044ecd8792"></a>
### In cascade

`operation_relationships_integrations_enterprise_application_utils_business_behavior_in_cascade`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool(Platform.flags.get(CASCADE\_FLAG)).

**Local steps**

- Return bool(Platform.flags.get(CASCADE\_FLAG)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L2463) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1323) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1299)

<a id="op-f5678bf04ecb26"></a>
### Set links

`operation_relationships_integrations_enterprise_application_utils_business_behavior_set_links`

**Inputs** item\_code, crm\_product\_name.

**Declared result** no value.

**State and service calls** request set\_value on “CRM Product” · request set\_value on “Item”.

**Local steps**

- Evaluate Platform.db.set\_value(“CRM Product”, crm\_product\_name, “Enterprise\_item\_code”, item\_code, update\_modified = false).
- Evaluate Platform.db.set\_value(“Item”, item\_code, “crm\_product\_code”, crm\_product\_name, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L2527) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1326) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1302)

<a id="op-c50c938963cd85"></a>
### Other side

`operation_relationships_integrations_enterprise_application_utils_business_behavior_other_side`

**Inputs** self\_doctype.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(“Item”, “crm\_product\_code”) · tuple(“CRM Product”, “Enterprise\_item\_code”).

**Local steps**

- If self\_doctype equals “CRM Product”.
  - Return tuple(“Item”, “crm\_product\_code”).
- Return tuple(“CRM Product”, “Enterprise\_item\_code”).

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L2682) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1324) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1300)

<a id="op-b451669780ff1b"></a>
### Find target for

`operation_relationships_integrations_enterprise_application_utils_business_behavior_find_target_for`

**Inputs** doctype, value.

**Declared result** (tuple at tuple(str, str) bitwise or no value).

**Record and data access** read “Item” via get\_value · read “CRM Product” via get\_value.

**Explicit results** no value · tuple(“Item”, item) when item, otherwise no value · tuple(“CRM Product”, prod) when prod, otherwise no value.

**Local steps**

- If (not doctype or not value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doctype → not value.
  - Return no value.
- If doctype equals “CRM Product”.
  - Set item from Platform.db.get\_value(“Item”, mapping(“crm\_product\_code” → value), “name”).
  - Return tuple(“Item”, item) when item, otherwise no value.
    - Value choice on item — true gives tuple(“Item”, item), false gives no value.
- If doctype equals “Item”.
  - Set prod from Platform.db.get\_value(“CRM Product”, mapping(“Enterprise\_item\_code” → value), “name”).
  - Return tuple(“CRM Product”, prod) when prod, otherwise no value.
    - Value choice on prod — true gives tuple(“CRM Product”, prod), false gives no value.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L2803) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1322) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1298)

<a id="op-8258817ae2e17c"></a>
### Validate rename conflict

`operation_relationships_integrations_enterprise_application_utils_business_behavior_validate_rename_conflict`

**Inputs** self\_doctype, olddn, newdn, merge.

**Record and data access** read other\_doctype via get\_value · read other\_doctype via exists.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot rename: an unrelated {0} '{1}' already exists on the other side. Resolve manually first.”.format(other\_doctype, newdn).

**Local steps**

- If (in\_cascade() or not \_should\_sync\_direction(self\_doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in in\_cascade() → not \_should\_sync\_direction(self\_doctype).
  - Return no value.
- Set tuple(other\_doctype, other\_link\_field) from \_other\_side(self\_doctype).
- Set linked from Platform.db.get\_value(other\_doctype, mapping(other\_link\_field → olddn), “name”).
- If not linked.
  - Return no value.
- If merge.
  - Set surviving from Platform.db.get\_value(other\_doctype, mapping(other\_link\_field → newdn), “name”).
  - If surviving.
    - Return no value.
- If linked equals newdn.
  - Return no value.
- If Platform.db.exists(other\_doctype, newdn).
  - Set existing\_link from Platform.db.get\_value(other\_doctype, newdn, other\_link\_field).
  - If existing\_link differs from olddn.
    - Call the validation error handler Platform.throw(translated “Cannot rename: an unrelated {0} '{1}' already exists on the other side. Resolve manually first.”.format(other\_doctype, newdn)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L3173) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1330) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1306)

<a id="op-603e521e6e4bf1"></a>
### Cascade rename

`operation_relationships_integrations_enterprise_application_utils_business_behavior_cascade_rename`

**Inputs** self\_doctype, olddn, newdn, merge.

**Record and data access** read other\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If (in\_cascade() or not \_should\_sync\_direction(self\_doctype)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in in\_cascade() → not \_should\_sync\_direction(self\_doctype).
  - Return no value.
- Set tuple(other\_doctype, other\_link\_field) from \_other\_side(self\_doctype).
- Set linked from Platform.db.get\_value(other\_doctype, mapping(other\_link\_field → olddn), “name”).
- If not linked.
  - Return no value.
- Set Platform.flags at CASCADE\_FLAG from true.
- Attempt the following.
  - If merge.
    - Set surviving from Platform.db.get\_value(other\_doctype, mapping(other\_link\_field → newdn), “name”).
    - If (surviving and surviving differs from linked).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in surviving → surviving differs from linked.
      - Evaluate rename\_doc(other\_doctype, linked, surviving, merge = true, ignore\_permissions = true).
      - Set target from surviving.
    - Otherwise.
      - If linked differs from newdn.
        - Evaluate rename\_doc(other\_doctype, linked, newdn, ignore\_permissions = true).
      - Set target from newdn.
  - Otherwise.
    - If linked differs from newdn.
      - Evaluate rename\_doc(other\_doctype, linked, newdn, ignore\_permissions = true).
    - Set target from newdn.
  - Evaluate \_resync\_links(self\_doctype, newdn, target).
- On exit, including pending return or failure.
  - Set Platform.flags at CASCADE\_FLAG from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L3659) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1321) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1297)

<a id="op-94aed925fbb28b"></a>
### Resync links

`operation_relationships_integrations_enterprise_application_utils_business_behavior_resync_links`

**Inputs** self\_doctype, self\_name, other\_name.

**Record and data access** read “CRM Product” via exists · read “Item” via exists.

**State and service calls** request set\_value on “CRM Product” · request set\_value on “Item”.

**Local steps**

- If self\_doctype equals “CRM Product”.
  - Set tuple(prod, item) from tuple(self\_name, other\_name).
- Otherwise.
  - Set tuple(prod, item) from tuple(other\_name, self\_name).
- If Platform.db.exists(“CRM Product”, prod).
  - Evaluate Platform.db.set\_value(“CRM Product”, prod, “Enterprise\_item\_code”, item, update\_modified = false).
- If Platform.db.exists(“Item”, item).
  - Evaluate Platform.db.set\_value(“Item”, item, “crm\_product\_code”, prod, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L4278) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1325) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1301)

<a id="op-4401110c640680"></a>
### Should sync direction

`operation_relationships_integrations_enterprise_application_utils_business_behavior_should_sync_direction`

**Inputs** self\_doctype.

**Explicit results** should\_push\_to\_Enterprise() · should\_sync().

**Local steps**

- If self\_doctype equals “CRM Product”.
  - Return should\_push\_to\_Enterprise().
- Return should\_sync().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0052.json#L4597) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1329) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1305)

<a id="op-e7c78a0532e177"></a>
### Get public url

`operation_relationships_integrations_twilio_utils_business_behavior_get_public_resource_address`

**Inputs** path = no value.

**Explicit results** (get\_url().split(“:8”, 1) at 0 + path).

**Local steps**

- Return (get\_url().split(“:8”, 1) at 0 + path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L3831) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1381) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1357)

<a id="op-8351d2de1021c4"></a>
### Merge dicts

`operation_relationships_integrations_twilio_utils_business_behavior_merge_dicts`

**Inputs** d1, d2.

**Explicit results** mapping of k → mapping(expand v, expand d2.get(k, mapping())) for tuple(k, v) drawn from d1.items().

**Local steps**

- Return mapping of k → mapping(expand v, expand d2.get(k, mapping())) for tuple(k, v) drawn from d1.items().
  - Draw tuple(k, v) from d1.items().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0054.json#L3930) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1382) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1358)

## Service · Views

<a id="op-53ccb8b3899ea0"></a>
### Get views

`operation_relationships_application_interface_views_business_behavior_get_views`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** views.

**Local steps**

- Set View from Platform.qb.DocType(“CRM View Settings”).
- Set query from nested operand in the contract.qb.from\_(View).select(“\*”).where(Criterion.any(list(View.user equals empty text, View.user equals Platform.session.user))).
- If doctype.
  - Set query from query.where(View.dt equals doctype).
- Set views from query.run(as\_dict = true).
- Return views.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L4098) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L162) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L143)

## Service · Whatsapp

<a id="op-ea1fb47bf331ba"></a>
### Validate access

`operation_relationships_application_interface_whatsapp_business_behavior_validate_access`

**Inputs** reference\_doctype = no value, reference\_name = no value, permtype = “read”.

**Record and data access** read reference\_doctype via exists · resolve a document from reference\_doctype via get\_doc.

**Explicit results** reference\_doc · no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Only sales users can access WhatsApp features.” · validation helper with Platform.DoesNotExistError — translated “Reference document {0} {1} does not exist.”.format(reference\_doctype, reference\_name) · validation helper with Platform.PermissionError — translated “Not permitted to access reference document {0} {1}.”.format(reference\_doctype, reference\_name).

**Local steps**

- If not any(generator of role belongs to ALLOWED\_WHATSAPP\_ROLES for role drawn from Platform.get\_roles()).
  - Draw role from Platform.get\_roles().
  - Call the validation error handler Platform.throw(translated “Only sales users can access WhatsApp features.”, Platform.PermissionError).
- If (reference\_doctype and reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype → reference\_name.
  - If not Platform.db.exists(reference\_doctype, reference\_name).
    - Call the validation error handler Platform.throw(translated “Reference document {0} {1} does not exist.”.format(reference\_doctype, reference\_name), Platform.DoesNotExistError).
  - Set reference\_doc from Platform.get\_doc(reference\_doctype, reference\_name).
  - If not reference\_doc.has\_permission(permtype).
    - Call the validation error handler Platform.throw(translated “Not permitted to access reference document {0} {1}.”.format(reference\_doctype, reference\_name), Platform.PermissionError).
  - Return reference\_doc.
- Return no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(), reference\_doc.has\_permission(permtype).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L4417) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L175) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L156)

<a id="op-ac9d26457275af"></a>
### Validate

`operation_relationships_application_interface_whatsapp_business_behavior_validate`

**Inputs** doc, method.

**Local steps**

- Set phone\_number from doc.get(“from”) when doc.type equals “Incoming”, otherwise doc.get(“to”).
  - Value choice on doc.type equals “Incoming” — true gives doc.get(“from”), false gives doc.get(“to”).
- If phone\_number.
  - Attempt the following.
    - Set tuple(name, doctype) from get\_contact\_lead\_or\_deal\_from\_number(phone\_number).
    - If (doctype and name is distinct from no value).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → name is distinct from no value.
      - Set doc.reference\_doctype from doctype.
      - Set doc.reference\_name from name.
  - On failure (Exception).
    - Evaluate Platform.log\_error(Platform.get\_traceback(), “CRM WhatsApp: failed to resolve contact from number”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L4857) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L174) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L155)

<a id="op-0f35a3e14bf42c"></a>
### On update

`operation_relationships_application_interface_whatsapp_business_behavior_on_update`

**Inputs** doc, method.

**State and service calls** publish realtime with “whatsapp\_message”.

**Local steps**

- If (doc.reference\_doctype and doc.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.reference\_doctype → doc.reference\_name.
  - Evaluate Platform.publish\_realtime(“whatsapp\_message”, mapping(“reference\_doctype” → doc.reference\_doctype, “reference\_name” → doc.reference\_name), doctype = doc.reference\_doctype, docname = doc.reference\_name).
- Evaluate notify\_agent(doc).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“whatsapp\_message”, mapping(“reference\_doctype” → doc.reference\_doctype, “reference\_name” → doc.reference\_name), doctype = doc.reference\_doctype, docname = doc.reference\_name).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L19) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L170) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L151)

<a id="op-04894ba961fbe9"></a>
### Notify agent

`operation_relationships_application_interface_whatsapp_business_behavior_notify_agent`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If doc.type equals “Incoming”.
  - If (not doc.reference\_doctype or not doc.reference\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.reference\_doctype → not doc.reference\_name.
    - Return no value.
  - Set doctype from doc.reference\_doctype.
  - If (doctype and doctype.startswith(“CRM ”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype → doctype.startswith(“CRM ”).
    - Set doctype from doctype at slice 4 to no value.lower().
  - Set safe\_reference\_name from Platform.utils.escape\_html(doc.reference\_name).
  - Set notification\_text from formatted text              &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                 &lt;span class="font-medium text-ink-gray-9"&gt;{translated “You”}&lt;/span&gt;.
  - Set assigned\_users from get\_assigned\_users(doc.reference\_doctype, doc.reference\_name).
  - For each user in assigned\_users.
    - Evaluate notify\_user(mapping(“owner” → doc.owner, “assigned\_to” → user, “notification\_type” → “WhatsApp”, “message” → doc.message, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L5274) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L169) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L150)

<a id="op-1acbdb78380704"></a>
### Is whatsapp enabled

`operation_relationships_application_interface_whatsapp_business_behavior_is_whatsapp_enabled`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via exists · read “WhatsApp Settings” via get\_cached\_value · read “WhatsApp Account” via get\_cached\_value.

**Explicit results** false · status equals “Active”.

**Local steps**

- If not Platform.db.exists(“DocType”, “WhatsApp Settings”).
  - Return false.
- Set default\_outgoing from Platform.get\_cached\_value(“WhatsApp Settings”, “WhatsApp Settings”, “default\_outgoing\_account”).
- If not default\_outgoing.
  - Return false.
- Set status from Platform.get\_cached\_value(“WhatsApp Account”, default\_outgoing, “status”).
- Return status equals “Active”.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“WhatsApp Settings”, “WhatsApp Settings”, “default\_outgoing\_account”), Platform.get\_cached\_value(“WhatsApp Account”, default\_outgoing, “status”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L5844) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L167) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L148)

<a id="op-303ba98f719376"></a>
### Is whatsapp installed

`operation_relationships_application_interface_whatsapp_business_behavior_is_whatsapp_installed`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via exists.

**Explicit results** false · true.

**Local steps**

- If not Platform.db.exists(“DocType”, “WhatsApp Settings”).
  - Return false.
- Return true.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0013.json#L6054) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L168) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L149)

<a id="op-83da3d0f5cb8ff"></a>
### Get whatsapp messages

`operation_relationships_application_interface_whatsapp_business_behavior_get_whatsapp_messages`

**Inputs** reference\_doctype, reference\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “DocType” via exists · read “WhatsApp Message” via get\_all · read “WhatsApp Templates” via exists · resolve a document from “WhatsApp Templates” via get\_doc.

**Explicit results** list() · list of message for message drawn from messages where message at “content\_type” differs from “reaction”.

**Local steps**

- Set reference\_doc from validate\_access(reference\_doctype, reference\_name).
- If “twilio\_integration” belongs to Platform.get\_installed\_apps().
  - Return list().
- If not Platform.db.exists(“DocType”, “WhatsApp Message”).
  - Return list().
- Set messages from list().
- If reference\_doctype equals “CRM Deal”.
  - Set lead from reference\_doc.get(“lead”).
  - If lead.
    - Evaluate validate\_access(“CRM Lead”, lead).
    - Set messages from Platform.get\_all(“WhatsApp Message”, filters = mapping(“reference\_doctype” → “CRM Lead”, “reference\_name” → lead), fields = list(“name”, “type”, “to”, “from”, …)).
- Update messages using + Platform.get\_all(“WhatsApp Message”, filters = mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name), fields = list(“name”, “type”, “to”, “from”, …)).
- Set template\_messages from list of message for message drawn from messages where message at “message\_type” equals “Template”.
  - Draw message from messages, keep a combination only if (message at “message\_type” equals “Template”).
- For each template\_message in template\_messages.
  - If not Platform.db.exists(“WhatsApp Templates”, template\_message at “template”).
    - Continue with the next iteration or loop test.
  - Set template from Platform.get\_doc(“WhatsApp Templates”, template\_message at “template”).
  - If template.
    - Set template\_message at “template\_name” from template.template\_name.
    - If template\_message at “template\_parameters”.
      - Set parameters from json.loads(template\_message at “template\_parameters”).
      - Set template.template from parse\_template\_parameters(template.template, parameters).
    - Set template\_message at “template” from template.template.
    - If template\_message at “template\_header\_parameters”.
      - Set header\_parameters from json.loads(template\_message at “template\_header\_parameters”).
      - Set template.header from parse\_template\_parameters(template.header, header\_parameters).
    - Set template\_message at “header” from template.header.
    - Set template\_message at “footer” from template.footer.
- Set reaction\_messages from list of message for message drawn from messages where message at “content\_type” equals “reaction”.
  - Draw message from messages, keep a combination only if (message at “content\_type” equals “reaction”).
- Evaluate reaction\_messages.reverse().
- For each reaction\_message in reaction\_messages.
  - Set reacted\_message from next(generator of m for m drawn from messages where m at “message\_id” equals reaction\_message at “reply\_to\_message\_id”, no value).
    - Draw m from messages, keep a combination only if (m at “message\_id” equals reaction\_message at “reply\_to\_message\_id”).
  - If reacted\_message.
    - Set reacted\_message at “reaction” from reaction\_message at “message”.
- For each message in messages.
  - Set from\_name from get\_from\_name(message) when message at “from”, otherwise translated “You”.
    - Value choice on message at “from” — true gives get\_from\_name(message), false gives translated “You”.
  - Set message at “from\_name” from from\_name.
- Set reply\_messages from list of message for message drawn from messages where message at “is\_reply”.
  - Draw message from messages, keep a combination only if (message at “is\_reply”).
- For each reply\_message in reply\_messages.
  - Set replied\_message from next(generator of m for m drawn from messages where m at “message\_id” equals reply\_message at “reply\_to\_message\_id”, no value).
    - Draw m from messages, keep a combination only if (m at “message\_id” equals reply\_message at “reply\_to\_message\_id”).
  - If replied\_message.
    - Set from\_name from get\_from\_name(reply\_message) when replied\_message at “from”, otherwise translated “You”.
      - Value choice on replied\_message at “from” — true gives get\_from\_name(reply\_message), false gives translated “You”.
    - Set message from replied\_message at “message”.
    - If replied\_message at “message\_type” equals “Template”.
      - Set message from replied\_message at “template”.
    - Set reply\_message at “reply\_message” from message.
    - Set reply\_message at “header” from (replied\_message.get(“header”) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in replied\_message.get(“header”) → empty text.
    - Set reply\_message at “footer” from (replied\_message.get(“footer”) or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in replied\_message.get(“footer”) → empty text.
    - Set reply\_message at “reply\_to” from replied\_message at “name”.
    - Set reply\_message at “reply\_to\_type” from replied\_message at “type”.
    - Set reply\_message at “reply\_to\_from” from from\_name.
- Return list of message for message drawn from messages where message at “content\_type” differs from “reaction”.
  - Draw message from messages, keep a combination only if (message at “content\_type” differs from “reaction”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L166) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L147)

<a id="op-1bdce3f9908f37"></a>
### Create whatsapp message

`operation_relationships_application_interface_whatsapp_business_behavior_create_whatsapp_message`

**Inputs** reference\_doctype, reference\_name, message, to, attach, reply\_to, content\_type = “text”.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “WhatsApp Message” via exists · resolve a document from “WhatsApp Message” via get\_doc.

**State and service calls** request new\_doc for “WhatsApp Message” · call insert on doc.

**Explicit results** doc.name.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Referenced WhatsApp message does not exist.” · validation helper with Platform.PermissionError — translated “Not permitted to access the referenced WhatsApp message.”.

**Local steps**

- Evaluate validate\_access(reference\_doctype, reference\_name).
- Set doc from Platform.new\_doc(“WhatsApp Message”).
- If reply\_to.
  - If not Platform.db.exists(“WhatsApp Message”, reply\_to).
    - Call the validation error handler Platform.throw(translated “Referenced WhatsApp message does not exist.”, Platform.DoesNotExistError).
  - Set reply\_doc from Platform.get\_doc(“WhatsApp Message”, reply\_to).
  - If not reply\_doc.has\_permission(“read”).
    - Call the validation error handler Platform.throw(translated “Not permitted to access the referenced WhatsApp message.”, Platform.PermissionError).
  - Evaluate validate\_access(reply\_doc.reference\_doctype, reply\_doc.reference\_name).
  - Evaluate doc.update(mapping(“is\_reply” → true, “reply\_to\_message\_id” → reply\_doc.message\_id)).
- Evaluate doc.update(mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “message” → (message or attach), “to” → to, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in message → attach.
- Evaluate doc.insert(ignore\_permissions = true).
- Return doc.name.

**Values supplied outside this operation** effective access from reply\_doc.has\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L2120) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L164) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L145)

<a id="op-f81acff4e48f0c"></a>
### Send whatsapp template

`operation_relationships_application_interface_whatsapp_business_behavior_send_whatsapp_template`

**Inputs** reference\_doctype, reference\_name, template, to.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request new\_doc for “WhatsApp Message” · call insert on doc.

**Explicit results** doc.name.

**Local steps**

- Evaluate validate\_access(reference\_doctype, reference\_name).
- Set doc from Platform.new\_doc(“WhatsApp Message”).
- Evaluate doc.update(mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “message\_type” → “Template”, “message” → “Template message”, …)).
- Evaluate doc.insert(ignore\_permissions = true).
- Return doc.name.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L2760) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L173) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L154)

<a id="op-bed1eb4ca12eb6"></a>
### React on whatsapp message

`operation_relationships_application_interface_whatsapp_business_behavior_react_on_whatsapp_message`

**Inputs** emoji, reply\_to\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “WhatsApp Message” via exists · resolve a document from “WhatsApp Message” via get\_doc.

**State and service calls** request new\_doc for “WhatsApp Message” · call insert on doc.

**Explicit results** doc.name.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Referenced WhatsApp message does not exist.” · validation helper with Platform.PermissionError — translated “Not permitted to access the referenced WhatsApp message.”.

**Local steps**

- Evaluate validate\_access().
- If not Platform.db.exists(“WhatsApp Message”, reply\_to\_name).
  - Call the validation error handler Platform.throw(translated “Referenced WhatsApp message does not exist.”, Platform.DoesNotExistError).
- Set reply\_to\_doc from Platform.get\_doc(“WhatsApp Message”, reply\_to\_name).
- If not reply\_to\_doc.has\_permission(“read”).
  - Call the validation error handler Platform.throw(translated “Not permitted to access the referenced WhatsApp message.”, Platform.PermissionError).
- Evaluate validate\_access(reply\_to\_doc.reference\_doctype, reply\_to\_doc.reference\_name).
- Set to from ((reply\_to\_doc.type equals “Incoming” and reply\_to\_doc.get(“from”)) or reply\_to\_doc.to).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (reply\_to\_doc.type equals “Incoming” and reply\_to\_doc.get(“from”)) → reply\_to\_doc.to.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in reply\_to\_doc.type equals “Incoming” → reply\_to\_doc.get(“from”).
- Set doc from Platform.new\_doc(“WhatsApp Message”).
- Evaluate doc.update(mapping(“reference\_doctype” → reply\_to\_doc.reference\_doctype, “reference\_name” → reply\_to\_doc.reference\_name, “message” → emoji, “to” → to, …)).
- Evaluate doc.insert(ignore\_permissions = true).
- Return doc.name.

**Values supplied outside this operation** effective access from reply\_to\_doc.has\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0014.json#L3093) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L172) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L153)
