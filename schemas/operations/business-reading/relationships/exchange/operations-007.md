# Integrations and service calls · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Doc share

<a id="op-a23510863fe0d0"></a>
### Before validate

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_before_validate`

**Inputs** doc, method = no value.

**Local steps**

- Set sync from \_sync(doc).
- Set old from doc.get\_doc\_before\_save().
- If (old and sync.has\_data\_updated(old) and sync.sync\_active()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old → sync.has\_data\_updated(old) → sync.sync\_active().
  - Evaluate sync.delete\_mirror\_for(old).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1296) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1272)

<a id="op-a5e1e18d85fe69"></a>
### After insert

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_after_insert`

**Inputs** doc, method = no value.

**Local steps**

- Set sync from \_sync(doc).
- If sync.should\_mirror().
  - Evaluate sync.create\_mirror().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L173) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1295) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1271)

<a id="op-c284652d58c43b"></a>
### On update

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_on_update`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- Set sync from \_sync(doc).
- If not sync.should\_mirror().
  - Return no value.
- Set old from doc.get\_doc\_before\_save().
- If (old and sync.has\_data\_updated(old)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old → sync.has\_data\_updated(old).
  - Evaluate sync.create\_mirror().
- Otherwise.
  - Evaluate sync.sync\_state\_to\_mirror().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L281) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1299) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1275)

<a id="op-69fd8f0c2ffa09"></a>
### On trash

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_on_trash`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- Set sync from \_sync(doc).
- If not sync.should\_mirror().
  - Return no value.
- Set mirror from sync.find\_mirror().
- If not mirror.
  - Return no value.
- Evaluate sync.set\_mirror\_flags(mirror).
- Evaluate mirror.delete(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L478) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1298) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1274)

<a id="op-8b7f3bdd13e808"></a>
### Sync shared docs

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_sync_shared_records`

**Inputs** no declared parameters.

**Record and data access** read “DocShare” via get\_list · read “Item” via get\_value · read “CRM Product” via get\_value.

**Explicit results** no value.

**Local steps**

- If not should\_sync().
  - Return no value.
- Set product\_shares from Platform.get\_list(“DocShare”, filters = mapping(“share\_doctype” → “CRM Product”), fields = list(“\*”)).
- Set item\_shares from Platform.get\_list(“DocShare”, filters = mapping(“share\_doctype” → “Item”), fields = list(“\*”)).
- Set existing\_product from set of tuple(s.user, s.share\_name) for s drawn from product\_shares.
  - Draw s from product\_shares.
- Set existing\_item from set of tuple(s.user, s.share\_name) for s drawn from item\_shares.
  - Draw s from item\_shares.
- For each share in item\_shares.
  - Set product from Platform.db.get\_value(“Item”, share.share\_name, “crm\_product\_code”).
  - If (not product or tuple(share.user, product) belongs to existing\_product).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not product → tuple(share.user, product) belongs to existing\_product.
    - Continue with the next iteration or loop test.
  - Evaluate \_mirror\_share(share, “CRM Product”, product).
  - Evaluate existing\_product.add(tuple(share.user, product)).
- For each share in product\_shares.
  - Set item from Platform.db.get\_value(“CRM Product”, share.share\_name, “Enterprise\_item\_code”).
  - If (not item or tuple(share.user, item) belongs to existing\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item → tuple(share.user, item) belongs to existing\_item.
    - Continue with the next iteration or loop test.
  - Evaluate \_mirror\_share(share, “Item”, item).
  - Evaluate existing\_item.add(tuple(share.user, item)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L673) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1301) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1277)

<a id="op-8f885493d6953a"></a>
### Mirror share

`operation_relationships_integrations_enterprise_application_record_share_business_behavior_mirror_share`

**Inputs** src, target\_doctype, target\_value.

**Record and data access** resolve a document from data via get\_doc.

**State and service calls** call insert on doc.

**Local steps**

- Set data from dict(src).
- For each k in tuple(“name”, “owner”, “creation”, “modified”, …).
  - Evaluate data.pop(k, no value).
- Evaluate data.update(mapping(“doctype” → “DocShare”, “share\_doctype” → target\_doctype, “share\_name” → target\_value)).
- Set doc from Platform.get\_doc(data).
- Set doc.flags at MIRROR\_FLAG from true.
- Set doc.flags.ignore\_share\_permission from true.
- Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0051.json#L1357) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1297) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1273)

## Service · Email

<a id="op-0cd2bc57ef19a9"></a>
### Cancel scheduled email

`operation_relationships_binding_crm_api_email_cancel_scheduled_email`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “File” via get\_all.

**State and service calls** request delete\_doc for “Email Queue”.

**Explicit results** mapping(“subject” → communication.subject, “content” → communication.content, “sender” → communication.sender, “recipients” → communication.recipients, …).

**Local steps**

- Set tuple(communication, queues) from get\_scheduled\_email(name).
- Set file\_urls from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → “Communication”, “attached\_to\_name” → name), pluck = “file\_url”).
- Set attachments from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → communication.reference\_doctype, “attached\_to\_name” → communication.reference\_name, “file\_url” → list(“in”, file\_urls)), fields = list(“na ….
  - Value choice on file\_urls — true gives Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → communication.reference\_doctype, “attached\_to\_name” → communication.reference\_name, “file\_url” → list(“in”, file\_urls)), fields = list(“na …, false gives list().
- For each queue in queues.
  - Evaluate Platform.delete\_doc(“Email Queue”, queue, ignore\_permissions = true, ignore\_on\_trash = true).
- Evaluate communication.delete(ignore\_permissions = true).
- Return mapping(“subject” → communication.subject, “content” → communication.content, “sender” → communication.sender, “recipients” → communication.recipients, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L55) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L211) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L192)

<a id="op-4b287d71015974"></a>
### Send scheduled email now

`operation_relationships_binding_crm_api_email_send_scheduled_email_now`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Email Queue” via get\_doc.

**State and service calls** call db\_set on communication · request set\_value on “Email Queue”.

**Local steps**

- Set tuple(communication, queues) from get\_scheduled\_email(name).
- Evaluate communication.db\_set(mapping(“send\_after” → no value, “delivery\_status” → “Sending”, “communication\_date” → now\_datetime())).
- For each queue in queues.
  - Evaluate Platform.db.set\_value(“Email Queue”, queue, “send\_after”, no value).
  - Evaluate Platform.get\_doc(“Email Queue”, queue).send().

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L57) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L213) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L194)

<a id="op-39393f6f0ce15d"></a>
### Stamp send time

`operation_relationships_binding_crm_api_email_stamp_send_time`

**Inputs** doc, method = no value.

**State and service calls** request set\_value on “Communication”.

**Explicit results** no value.

**Local steps**

- If (doc.delivery\_status differs from “Sent” or not doc.send\_after).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.delivery\_status differs from “Sent” → not doc.send\_after.
  - Return no value.
- If get\_datetime(doc.communication\_date) ≥ get\_datetime(doc.send\_after).
  - Return no value.
- Evaluate Platform.db.set\_value(“Communication”, doc.name, “communication\_date”, now\_datetime(), update\_modified = false).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L58) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L214) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L195)

<a id="op-b3a080af2bffdd"></a>
### Get scheduled email

`operation_relationships_binding_crm_api_email_get_scheduled_email`

**Inputs** name.

**Record and data access** resolve a document from “Communication” via get\_doc.

**Explicit results** tuple(communication, list of q.name for q drawn from queues).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You can only change emails you scheduled” · validation helper — translated “This email is no longer scheduled” · validation helper — translated “This email is already being sent”.

**Local steps**

- Set communication from Platform.get\_doc(“Communication”, name).
- If communication.owner differs from Platform.session.user.
  - Call the validation error handler Platform.throw(translated “You can only change emails you scheduled”, Platform.PermissionError).
- If communication.delivery\_status differs from “Scheduled”.
  - Call the validation error handler Platform.throw(translated “This email is no longer scheduled”).
- Set EmailQueue from Platform.qb.DocType(“Email Queue”).
- Set queues from nested operand in the contract(nested operand in the contract, nested operand in the contract).where(nested operand in the contract.communication equals name).for\_update().run(as\_dict = true).
- If any(generator of q.status differs from “Not Sent” for q drawn from queues).
  - Draw q from queues.
  - Call the validation error handler Platform.throw(translated “This email is already being sent”).
- Return tuple(communication, list of q.name for q drawn from queues).
  - Draw q from queues.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L56) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L212) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L193)

## Service · Exchange rate

<a id="op-e9c9268c478f84"></a>
### Get exchange rate

`operation_relationships_application_interface_exchange_rate_business_behavior_get_exchange_rate`

**Inputs** from\_currency, to\_currency, date = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** cached\_rate · rate.

**Local steps**

- If not date.
  - Set date from “latest”.
- Set cache\_date from Platform.utils.today() when date equals “latest”, otherwise date.
  - Value choice on date equals “latest” — true gives Platform.utils.today(), false gives date.
- Set cache\_key from formatted text exchange\_rate\_{from\_currency}\_{to\_currency}\_{cache\_date}.
- Set cached\_rate from Platform.cache().get\_value(cache\_key).
- If cached\_rate is distinct from no value.
  - Return cached\_rate.
- Set tuple(rate, api\_used) from \_fetch\_exchange\_rate(from\_currency, to\_currency, date).
- If rate is distinct from no value.
  - Evaluate Platform.cache().set\_value(cache\_key, rate).
  - Return rate.
- Evaluate \_raise\_exchange\_rate\_error(from\_currency, to\_currency, date, api\_used).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.today().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L1611) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L76) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L58)

<a id="op-ce13e4d163932c"></a>
### Fetch exchange rate

`operation_relationships_application_interface_exchange_rate_business_behavior_fetch_exchange_rate`

**Inputs** from\_currency, to\_currency, date.

**Record and data access** read “FCRM Settings” via get\_single.

**Explicit results** tuple(\_fetch\_from\_exchangerate\_host(settings, from\_currency, to\_currency, date), provider) · tuple(\_fetch\_from\_exchangerate\_api(settings, from\_currency, to\_currency), provider) · tuple(rate, provider) · tuple(rate, “fawazahmed-exchange-api”) · tuple(rate, “frankfurter”) · 1 additional forms in the steps below.

**Local steps**

- Set settings from Platform.get\_single(“FCRM Settings”).
- Set provider from settings.service\_provider.
- If provider equals “exchangerate.host”.
  - Return tuple(\_fetch\_from\_exchangerate\_host(settings, from\_currency, to\_currency, date), provider).
- If provider equals “exchangerate-api”.
  - Return tuple(\_fetch\_from\_exchangerate\_api(settings, from\_currency, to\_currency), provider).
- If provider equals “frankfurter.app”.
  - Set rate from \_fetch\_from\_frankfurter(from\_currency, to\_currency, date).
  - If rate is distinct from no value.
    - Return tuple(rate, provider).
  - Set rate from \_fetch\_from\_fawaz\_api(from\_currency, to\_currency, date).
  - Return tuple(rate, “fawazahmed-exchange-api”).
- If provider equals “fawazahmed-exchange-api”.
  - Set rate from \_fetch\_from\_fawaz\_api(from\_currency, to\_currency, date).
  - If rate is distinct from no value.
    - Return tuple(rate, provider).
  - Set rate from \_fetch\_from\_frankfurter(from\_currency, to\_currency, date).
  - Return tuple(rate, “frankfurter”).
- Set rate from \_fetch\_from\_frankfurter(from\_currency, to\_currency, date).
- If rate is distinct from no value.
  - Return tuple(rate, “frankfurter”).
- Return tuple(\_fetch\_from\_fawaz\_api(from\_currency, to\_currency, date), “fawazahmed-exchange-api”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L2050) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L71) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L53)

<a id="op-6ec9d8eb90b47f"></a>
### Fetch from frankfurter

`operation_relationships_application_interface_exchange_rate_business_behavior_fetch_from_frankfurter`

**Inputs** from\_currency, to\_currency, date.

**Explicit results** res.json().get(“rates”, mapping()).get(to\_currency) · no value.

**Local steps**

- Attempt the following.
  - Set res from requests.get(formatted command or address in the contract, timeout = 5).
  - If res.ok.
    - Return res.json().get(“rates”, mapping()).get(to\_currency).
- On failure (Exception).
  - Take no action here.
- Return no value.

**Values supplied outside this operation** service or queued work from requests.get(formatted command or address in the contract, timeout = 5).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L2682) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L75) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L57)

<a id="op-f0759a2ee5c8ec"></a>
### Fetch from fawaz api

`operation_relationships_application_interface_exchange_rate_business_behavior_fetch_from_fawaz_application_programming_interface`

**Inputs** from\_currency, to\_currency, date.

**Explicit results** res.json() at from\_lower at to\_lower · no value.

**Local steps**

- Set from\_lower from from\_currency.lower().
- Set to\_lower from to\_currency.lower().
- Set date\_str from “latest” when date equals “latest”, otherwise date.
  - Value choice on date equals “latest” — true gives “latest”, false gives date.
- Set urls from list(formatted command or address in the contract, formatted command or address in the contract).
- For each url in urls.
  - Attempt the following.
    - Set res from requests.get(url, timeout = 5).
    - If res.ok.
      - Return res.json() at from\_lower at to\_lower.
  - On failure (Exception).
    - Continue with the next iteration or loop test.
- Return no value.

**Values supplied outside this operation** service or queued work from requests.get(url, timeout = 5).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L2928) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L74) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L56)

<a id="op-ccb4aedec01a02"></a>
### Fetch from exchangerate host

`operation_relationships_application_interface_exchange_rate_business_behavior_fetch_from_exchangerate_host`

**Inputs** settings, from\_currency, to\_currency, date.

**Explicit results** res.json() at “result” · no value.

**Explicit failure paths** validation helper — translated “Access Key is required for Service Provider: {0}”.format(Platform.bold(settings.service\_provider)).

**Local steps**

- If not settings.access\_key.
  - Call the validation error handler Platform.throw(translated “Access Key is required for Service Provider: {0}”.format(Platform.bold(settings.service\_provider))).
- Set params from mapping(“access\_key” → settings.access\_key, “from” → from\_currency, “to” → to\_currency, “amount” → 1).
- If date differs from “latest”.
  - Set params at “date” from date.
- Set res from requests.get(text in the contract, params = params, timeout = 5).
- If res.ok.
  - Return res.json() at “result”.
- Return no value.

**Values supplied outside this operation** service or queued work from requests.get(text in the contract, params = params, timeout = 5).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L3293) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L73) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L55)

<a id="op-4b15edc6dff982"></a>
### Fetch from exchangerate api

`operation_relationships_application_interface_exchange_rate_business_behavior_fetch_from_exchangerate_application_programming_interface`

**Inputs** settings, from\_currency, to\_currency.

**Explicit results** data at “conversion\_rate” · no value.

**Explicit failure paths** validation helper — translated “Access Key is required for Service Provider: {0}”.format(Platform.bold(settings.service\_provider)).

**Local steps**

- If not settings.access\_key.
  - Call the validation error handler Platform.throw(translated “Access Key is required for Service Provider: {0}”.format(Platform.bold(settings.service\_provider))).
- Set res from requests.get(formatted command or address in the contract, timeout = 5).
- If res.ok.
  - Set data from res.json().
  - If data at “result” equals “success”.
    - Return data at “conversion\_rate”.
- Return no value.

**Values supplied outside this operation** service or queued work from requests.get(formatted command or address in the contract, timeout = 5).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L3688) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L72) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L54)

<a id="op-3680ab1489dd58"></a>
### Raise exchange rate error

`operation_relationships_application_interface_exchange_rate_business_behavior_raise_exchange_rate_error`

**Inputs** from\_currency, to\_currency, date, api\_used.

**Explicit failure paths** validation helper — translated “Ask your manager to set up the Exchange Rate Provider, as default provider does not support currency convers …”.format(from\_currency, to\_currency) · validation helper — translated “Setup the Exchange Rate Provider other than 'Frankfurter' in settings, as default provider does not support  …”.format(from\_currency, to\_currency) · validation helper — translated “Failed to fetch exchange rate from {0} to {1} on {2}. Please check your internet connection or try again later.”.format(from\_currency, to\_currency, date).

**Local steps**

- Evaluate Platform.log\_error(title = “Exchange Rate Fetch Error”, message = formatted text Failed to fetch exchange rate from {from\_currency} to {to\_currency} using {api\_used} API.).
- If api\_used equals “frankfurter”.
  - Set user from Platform.session.user.
  - Set is\_manager from (“System Manager” belongs to Platform.get\_roles(user) or “Sales Manager” belongs to Platform.get\_roles(user) or user equals “Administrator”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “System Manager” belongs to Platform.get\_roles(user) → “Sales Manager” belongs to Platform.get\_roles(user) → user equals “Administrator”.
  - If not is\_manager.
    - Call the validation error handler Platform.throw(translated “Ask your manager to set up the Exchange Rate Provider, as default provider does not support currency convers …”.format(from\_currency, to\_currency)).
  - Call the validation error handler Platform.throw(translated “Setup the Exchange Rate Provider other than 'Frankfurter' in settings, as default provider does not support  …”.format(from\_currency, to\_currency)).
- Call the validation error handler Platform.throw(translated “Failed to fetch exchange rate from {0} to {1} on {2}. Please check your internet connection or try again later.”.format(from\_currency, to\_currency, date)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L4035) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L77) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L59)

## Service · Form

<a id="op-101ff7e0282351"></a>
### Ensure form source

`operation_relationships_application_interface_form_business_behavior_ensure_form_source`

**Inputs** no declared parameters.

**Declared result** str.

**Record and data access** read “CRM Lead Source” via exists · resolve a document from mapping(“doctype” → “CRM Lead Source”, “source\_name” → FORM\_SOURCE) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Lead Source”, “source\_name” → FORM\_SOURCE)).

**Explicit results** FORM\_SOURCE.

**Local steps**

- If not Platform.db.exists(“CRM Lead Source”, FORM\_SOURCE).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Lead Source”, “source\_name” → FORM\_SOURCE)).insert(ignore\_permissions = true).
- Return FORM\_SOURCE.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L4525) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L84) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L66)

<a id="op-7b58576a364989"></a>
### Seeded visible fieldnames

`operation_relationships_application_interface_form_business_behavior_seeded_visible_fieldnames`

**Inputs** document\_type.

**Declared result** set.

**Explicit results** names.

**Local steps**

- Set names from set().
- For each section in SEED\_LAYOUT.get(document\_type, list()).
  - For each col in section at “columns”.
    - Evaluate names.update(col).
- Return names.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L4682) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L100) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L82)

<a id="op-287f461deab594"></a>
### Guest can select

`operation_relationships_application_interface_form_business_behavior_guest_can_select`

**Inputs** doctype.

**Declared result** bool.

**Explicit results** (bool(doctype) and Platform.has\_permission(doctype, ptype = “select”, user = “Guest”)).

**Local steps**

- Return (bool(doctype) and Platform.has\_permission(doctype, ptype = “select”, user = “Guest”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in bool(doctype) → Platform.has\_permission(doctype, ptype = “select”, user = “Guest”).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, ptype = “select”, user = “Guest”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L4832) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L90) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L72)

<a id="op-20d97602ec5b7f"></a>
### Link target doctypes

`operation_relationships_application_interface_form_business_behavior_link_target_record_types`

**Inputs** no declared parameters.

**Declared result** set.

**Explicit results** targets.

**Local steps**

- Set targets from set().
- For each document\_type in ALLOWED\_DOCTYPES.
  - For each df in Platform.get\_meta(document\_type).fields.
    - If (df.fieldtype equals “Link” and df.options).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype equals “Link” → df.options.
      - Evaluate targets.add(df.options).
- Return targets.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L4944) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L92) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L74)

<a id="op-6e5644ecc38b12"></a>
### Mappable fields

`operation_relationships_application_interface_form_business_behavior_mappable_fields`

**Inputs** document\_type.

**Declared result** list at dict.

**Explicit results** fields.

**Local steps**

- Set meta from Platform.get\_meta(document\_type).
- Set fields from list().
- For each df in meta.fields.
  - If df.fieldtype does not belong to SUPPORTED\_FIELDTYPES.
    - Continue with the next iteration or loop test.
  - If (not df.fieldname or df.fieldname belongs to DENIED\_FIELDNAMES).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df.fieldname → df.fieldname belongs to DENIED\_FIELDNAMES.
    - Continue with the next iteration or loop test.
  - If (df.hidden or df.read\_only).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.hidden → df.read\_only.
    - Continue with the next iteration or loop test.
  - Evaluate fields.append(mapping(“fieldname” → df.fieldname, “label” → (df.label or df.fieldname), “fieldtype” → df.fieldtype, “options” → df.options, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → df.fieldname.
- Return fields.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L5113) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L95) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L77)

<a id="op-396f15b60b690e"></a>
### Default status

`operation_relationships_application_interface_form_business_behavior_default_status`

**Inputs** document\_type.

**Declared result** (str bitwise or no value).

**Record and data access** read status\_dt via exists · read status\_dt via get\_all.

**Explicit results** preferred · rows at 0 when rows, otherwise no value.

**Local steps**

- Set status\_dt from “CRM Lead Status” when document\_type equals “CRM Lead”, otherwise “CRM Deal Status”.
  - Value choice on document\_type equals “CRM Lead” — true gives “CRM Lead Status”, false gives “CRM Deal Status”.
- Set preferred from “New” when document\_type equals “CRM Lead”, otherwise “Qualification”.
  - Value choice on document\_type equals “CRM Lead” — true gives “New”, false gives “Qualification”.
- If Platform.db.exists(status\_dt, preferred).
  - Return preferred.
- Set rows from Platform.get\_all(status\_dt, mapping(“type” → “Open”), pluck = “name”).
- Return rows at 0 when rows, otherwise no value.
  - Value choice on rows — true gives rows at 0, false gives no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L5496) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L81) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L63)

<a id="op-81c8ff8e96415d"></a>
### Seed visible fields

`operation_relationships_application_interface_form_business_behavior_seed_visible_fields`

**Inputs** document\_type.

**Declared result** list at dict.

**Explicit results** rows.

**Local steps**

- Set catalog from mapping of f at “fieldname” → f for f drawn from \_mappable\_fields(document\_type).
  - Draw f from \_mappable\_fields(document\_type).
- Bind local operation \_break for subsequent calls.
- Set rows from list().
- Set n from 0.
- For each section in SEED\_LAYOUT.get(document\_type, list()).
  - Update n using + 1.
  - Evaluate rows.append(\_break(“Section Break”, n, (section.get(“label”) or empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in section.get(“label”) → empty text.
  - For each tuple(ci, col) in enumerate(section at “columns”).
    - If ci &gt; 0.
      - Update n using + 1.
      - Evaluate rows.append(\_break(“Column Break”, n)).
    - For each fn in col.
      - Set f from catalog.get(fn).
      - If not f.
        - Continue with the next iteration or loop test.
      - Evaluate rows.append(mapping(“fieldname” → f at “fieldname”, “label” → f at “label”, “fieldtype” → f at “fieldtype”, “options” → f at “options”, …)).
        - Value choice on f at “reqd” — true gives 1, false gives 0.
- Return rows.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0010.json#L5767) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L98) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L80)
