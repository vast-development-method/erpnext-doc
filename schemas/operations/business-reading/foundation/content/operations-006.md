# Web content and issued documents · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Personal data deletion request

[Record definition](../../../../data/record-types/personal_data_deletion_request.json)

<a id="op-4447af31134498"></a>
### Personal Data Deletion Request.autoname

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_autoname`

**Inputs** self.

**Local steps**

- Bind dependencies set\_name\_from\_naming\_options.
- Set pattern from re.compile(“^((&#91;a-zA-Z&#93;{1})\|(&#91;a-zA-Z&#93;{1}&#91;a-zA-Z&#93;{1})\|(&#91;a-zA-Z&#93;{1}&#91;0-9&#93;{1})\|(&#91;0-9&#93;{1}&#91;a-zA-Z&#93;{1})\|(&#91;a-zA-Z0-9&#93;&#91;-\_.a-zA-Z0 …”).
- Set domain from Platform.local.site.replace(“\_”, “-”).
- Set site from domain when pattern.match(domain), otherwise formatted text {domain}.com.
  - Value choice on pattern.match(domain) — true gives domain, false gives formatted text {domain}.com.
- Set autoname from formatted text format:deleted-user-{####}@{site}.
- Evaluate set\_name\_from\_naming\_options(autoname, self).
- Evaluate Platform.utils.validate\_email\_address(self.email, throw = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6734) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1233)

<a id="op-8b40c252eea7e2"></a>
### Personal Data Deletion Request.after insert

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_after_insert`

**Inputs** self.

**Local steps**

- Evaluate self.send\_verification\_mail().

If control reaches the end, it returns no value.

**Methods declared on this owner** [send verification mail](operations-006.md#op-45fa958148765b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L6998) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1230)

<a id="op-14d81b1bc63b7d"></a>
### Personal Data Deletion Request.generate url for confirmation

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_generate_resource_address_for_confirmation`

**Inputs** self.

**Explicit results** url.

**Local steps**

- Set params from mapping(“email” → self.email, “name” → self.name, “host\_name” → Platform.local.site).
- Set api from Platform.utils.get\_url(“/api/method/Platform.website.doctype.personal\_data\_deletion\_request.personal\_data\_deletion\_request.confirm\_deletion”).
- Set url from formatted text {api}?{get\_signed\_params(params)}.
- If Platform.conf.developer\_mode.
  - Evaluate print(formatted text URL generated for {self.doctype} {self.name}: {url}).
- Return url.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L7049) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L289) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1236)

<a id="op-b4ec7a15058206"></a>
### Personal Data Deletion Request.disable user

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_disable_user`

**Inputs** self.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Local steps**

- Set user from Platform.get\_doc(“User”, self.email).
- Set user.enabled from false.
- Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0522.json#L7350) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1234)

<a id="op-45fa958148765b"></a>
### Personal Data Deletion Request.send verification mail

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_send_verification_mail`

**Inputs** self.

**State and service calls** sendmail.

**Local steps**

- Set url from self.generate\_url\_for\_confirmation().
- Evaluate Platform.sendmail(recipients = self.email, subject = translated “Confirm Deletion of Account”, template = “delete\_data\_confirmation”, args = mapping(“email” → self.email, “name” → self.name, “host\_name” →  ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate url for confirmation](operations-006.md#op-14d81b1bc63b7d).

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.email, subject = translated “Confirm Deletion of Account”, template = “delete\_data\_confirmation”, args = mapping(“email” → self.email, “name” → self.name, “host\_name” →  ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L6) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1247)

<a id="op-6071b1ce346f1f"></a>
### Personal Data Deletion Request.notify system managers

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_notify_system_managers`

**Inputs** self.

**State and service calls** sendmail.

**Local steps**

- Set recipients from list().
- For each manager in get\_system\_managers(only\_name = true).
  - If is\_email\_notifications\_enabled(manager).
    - Evaluate recipients.append(manager).
- Evaluate Platform.sendmail(recipients = recipients, subject = translated “User {0} has requested for data deletion”.format(self.email), template = “data\_deletion\_approval”, args = mapping(“user” → self.email, “url” ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = recipients, subject = translated “User {0} has requested for data deletion”.format(self.email), template = “data\_deletion\_approval”, args = mapping(“user” → self.email, “url” ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L255) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L291) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1238)

<a id="op-f2d1fc2e7b752d"></a>
### Personal Data Deletion Request.validate data anonymization

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_validate_data_anonymization`

**Inputs** self.

**Explicit failure paths** validation helper — translated “This request has not yet been approved by the user.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If self.status differs from “Pending Approval”.
  - Call the validation error handler Platform.throw(translated “This request has not yet been approved by the user.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L572) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L304) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1251)

<a id="op-acc4e8c529ffcc"></a>
### Personal Data Deletion Request.trigger data deletion

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_trigger_data_deletion`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.validate\_data\_anonymization().
- Evaluate self.disable\_user().
- Evaluate self.anonymize\_data().
- Evaluate self.notify\_user\_after\_deletion().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate data anonymization](operations-006.md#op-f2d1fc2e7b752d), [disable user](operations-006.md#op-b4ec7a15058206), [anonymize data](operations-006.md#op-8d5031d78043cb), [notify user after deletion](operations-006.md#op-3d3060742a69ec).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L693) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L303) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1250)

<a id="op-8d5031d78043cb"></a>
### Personal Data Deletion Request.anonymize data

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_anonymize_data`

**Inputs** self.

**State and service calls** enqueue doc with self.doctype.

**Explicit results** Platform.enqueue\_doc(self.doctype, self.name, “\_anonymize\_data”, queue = “long”, timeout = 3000, now = Platform.in\_test).

**Local steps**

- Return Platform.enqueue\_doc(self.doctype, self.name, “\_anonymize\_data”, queue = “long”, timeout = 3000, now = Platform.in\_test).

**Values supplied outside this operation** service or queued work from Platform.enqueue\_doc(self.doctype, self.name, “\_anonymize\_data”, queue = “long”, timeout = 3000, now = Platform.in\_test).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L822) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1231)

<a id="op-3d3060742a69ec"></a>
### Personal Data Deletion Request.notify user after deletion

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_notify_user_after_deletion`

**Inputs** self.

**State and service calls** sendmail.

**Local steps**

- Evaluate Platform.sendmail(recipients = self.email, subject = translated “Your account has been deleted”, template = “account\_deletion\_notification”, args = mapping(“email” → self.email, “host\_name” → Platform.util ….

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(recipients = self.email, subject = translated “Your account has been deleted”, template = “account\_deletion\_notification”, args = mapping(“email” → self.email, “host\_name” → Platform.util ….

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L926) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L292) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1239)

<a id="op-01f86689a53371"></a>
### Personal Data Deletion Request.add deletion steps

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_add_deletion_steps`

**Inputs** self.

**State and service calls** call save on self.

**Explicit results** no value.

**Local steps**

- If self.deletion\_steps.
  - Return no value.
- For each step in (self.full\_match\_privacy\_docs + self.partial\_privacy\_docs).
  - Set row\_data from mapping(“status” → “Pending”, “document\_type” → step.get(“doctype”), “partial” → step.get(“partial”, false), “fields” → json.dumps(step.get(“redact\_fields”, list())), …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in step.get(“filtered\_by”) → empty text.
  - Evaluate self.append(“deletion\_steps”, row\_data).
- Set self.anonymization\_matrix from json.dumps(self.anonymization\_value\_map, indent = 4).
- Evaluate self.save().
- Evaluate self.reload().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L1111) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1229)

<a id="op-81eb361c39ffc8"></a>
### Personal Data Deletion Request.redact partial match data

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_redact_partial_match_data`

**Inputs** self, doctype.

**Local steps**

- Evaluate self.\_\_redact\_partial\_match\_data(doctype).
- Evaluate self.rename\_documents(doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [redact partial match data](operations-006.md#op-04656fac498b1c), [rename documents](operations-006.md#op-d082491f99c479).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L1511) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1242)

<a id="op-d082491f99c479"></a>
### Personal Data Deletion Request.rename documents

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_rename_documents`

**Inputs** self, doctype.

**Record and data access** read doctype at “doctype” via get\_all.

**State and service calls** request rename\_doc for doctype at “doctype”.

**Explicit results** no value.

**Local steps**

- If not doctype.get(“rename”).
  - Return no value.
- Bind local operation new\_name for subsequent calls.
- For each tuple(i, name) in enumerate(Platform.get\_all(doctype at “doctype”, filters = mapping(doctype.get(“filter\_by”, “owner”) → self.email), pluck = “name”)).
  - Evaluate Platform.rename\_doc(doctype at “doctype”, name, new\_name(self.anon, (i + 1)), force = true, show\_alert = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L1599) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1245)

<a id="op-79959454298a52"></a>
### Personal Data Deletion Request.rename documents.new name

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_rename_documents_new_name`

**Inputs** email, number.

**Explicit results** formatted text {email\_user}-{number}@{domain}.

**Local steps**

- Set tuple(email\_user, domain) from email.split(“@”).
- Return formatted text {email\_user}-{number}@{domain}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L2011) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1246)

<a id="op-58ad383cecf070"></a>
### Personal Data Deletion Request.redact full match data

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_redact_full_match_data`

**Inputs** self, ref, email.

**Record and data access** read ref at “doctype” via get\_all.

**Explicit results** no value.

**Local steps**

- Set filter\_by from ref.get(“filter\_by”, “owner”).
- Set docs from Platform.get\_all(ref at “doctype”, filters = mapping(filter\_by → email), fields = list(“name”, filter\_by)).
- If not docs.
  - Return no value.
- Set self.anonymize\_fields\_dict from self.generate\_anonymization\_dict(ref).
- For each doc in docs.
  - Evaluate self.redact\_doc(doc, ref).

If control reaches the end, it returns no value.

**Methods declared on this owner** [generate anonymization dict](operations-006.md#op-6b1fcfbed3316f), [redact doc](operations-006.md#op-1a9920dfbf1166).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L2136) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1241)

<a id="op-6b1fcfbed3316f"></a>
### Personal Data Deletion Request.generate anonymization dict

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_generate_anonymization_mapping`

**Inputs** self, ref.

**Explicit results** anonymize\_fields\_dict.

**Local steps**

- Set anonymize\_fields\_dict from mapping().
- Set meta from Platform.get\_meta(ref at “doctype”).
- For each field in ref.get(“redact\_fields”, list()).
  - Set field\_details from meta.get\_field(field).
  - If not field\_details.
    - Evaluate print(formatted text Incorrect personal\_field {field} defined in hooks).
    - Continue with the next iteration or loop test.
  - Set field\_value from self.anon when field\_details.unique, otherwise (self.anonymization\_value\_map.get(field\_details.options) or self.anonymization\_value\_map.get(field\_details.fieldtype) or field).
    - Value choice on field\_details.unique — true gives self.anon, false gives (self.anonymization\_value\_map.get(field\_details.options) or self.anonymization\_value\_map.get(field\_details.fieldtype) or field).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.anonymization\_value\_map.get(field\_details.options) → self.anonymization\_value\_map.get(field\_details.fieldtype) → field.
  - Set anonymize\_fields\_dict at field from field\_value.
- Return anonymize\_fields\_dict.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L2407) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1235)

<a id="op-1a9920dfbf1166"></a>
### Personal Data Deletion Request.redact doc

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_redact_record`

**Inputs** self, doc, ref.

**State and service calls** request set\_value on ref at “doctype” · request rename\_doc for ref at “doctype”.

**Local steps**

- Set filter\_by from ref.get(“filter\_by”, “owner”).
- Set meta from Platform.get\_meta(ref at “doctype”).
- Set filter\_by\_meta from meta.get\_field(filter\_by).
- If (filter\_by\_meta and filter\_by\_meta.fieldtype differs from “Link”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filter\_by\_meta → filter\_by\_meta.fieldtype differs from “Link”.
  - Set value from doc at filter\_by.
  - If self.email belongs to value.
    - Set value from re.sub(self.email\_regex, self.anon, value).
    - Set value from re.sub(self.full\_name\_regex, self.anonymization\_value\_map at “Data”, value).
    - Set self.anonymize\_fields\_dict at filter\_by from value.
- Evaluate Platform.db.set\_value(ref at “doctype”, doc at “name”, self.anonymize\_fields\_dict, modified\_by = “Administrator”).
- If (ref.get(“rename”) and doc at “name” differs from self.anon).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref.get(“rename”) → doc at “name” differs from self.anon.
  - Evaluate Platform.rename\_doc(ref at “doctype”, doc at “name”, self.anon, force = true, show\_alert = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L2739) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1244)

<a id="op-f7edef8b07640a"></a>
### Personal Data Deletion Request.anonymize data

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_anonymize_data_2`

**Inputs** self, email = no value, anon = no value, set\_data = true, commit = false.

**State and service calls** commit · request rename\_doc for “User” · call db\_set on self.

**Local steps**

- Set email from (email or self.email).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in email → self.email.
- Set anon from (anon or self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in anon → self.name.
- If set\_data.
  - Evaluate self.\_\_set\_anonymization\_data(email, anon).
- Evaluate self.add\_deletion\_steps().
- Set self.full\_match\_doctypes from generator of doc for doc drawn from self.full\_match\_privacy\_docs where filter(deferred anonymous expression, self.deletion\_steps).
  - Draw doc from self.full\_match\_privacy\_docs, keep a combination only if (filter(deferred anonymous expression, self.deletion\_steps)).
- Set self.partial\_match\_doctypes from generator of doc for doc drawn from self.partial\_privacy\_docs where filter(deferred anonymous expression, self.deletion\_steps).
  - Draw doc from self.partial\_privacy\_docs, keep a combination only if (filter(deferred anonymous expression, self.deletion\_steps)).
- For each doctype in self.full\_match\_doctypes.
  - Evaluate self.redact\_full\_match\_data(doctype, email).
  - Evaluate self.set\_step\_status(doctype at “doctype”).
  - If commit.
    - Evaluate Platform.db.commit().
- For each doctype in self.partial\_match\_doctypes.
  - Evaluate self.redact\_partial\_match\_data(doctype).
  - Evaluate self.set\_step\_status(doctype at “doctype”).
  - If commit.
    - Evaluate Platform.db.commit().
- Evaluate Platform.rename\_doc(“User”, email, anon, force = true, show\_alert = false).
- Evaluate self.db\_set(“status”, “Deleted”).
- If commit.
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set anonymization data](operations-006.md#op-7b301f266a4ca1), [add deletion steps](operations-006.md#op-01f86689a53371), [redact full match data](operations-006.md#op-58ad383cecf070), [set step status](operations-006.md#op-ac7f03c17cf36f), [redact partial match data](operations-006.md#op-81eb361c39ffc8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L3313) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1232)

<a id="op-ac7f03c17cf36f"></a>
### Personal Data Deletion Request.set step status

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_set_step_status`

**Inputs** self, step, status = “Deleted”.

**State and service calls** call save on self.

**Local steps**

- Set del\_step from find(self.deletion\_steps, deferred anonymous expression).
- If not del\_step.
  - Set del\_step from find(self.deletion\_steps, deferred anonymous expression).
- Set del\_step.status from status.
- Evaluate self.save().
- Evaluate self.reload().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L4087) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1249)

<a id="op-7b301f266a4ca1"></a>
### Personal Data Deletion Request.set anonymization data

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_set_anonymization_data`

**Inputs** self, email, anon.

**Local steps**

- Set self.anon from (anon or self.name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in anon → self.name.
- Set self.full\_name from get\_fullname(email).
- Set self.email\_regex from get\_pattern(email).
- Set self.full\_name\_regex from get\_pattern(self.full\_name).
- Set self.is\_full\_name\_set from email differs from self.full\_name.
- Set self.anonymization\_value\_map at “Email” from self.anon.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L4355) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1248)

<a id="op-04656fac498b1c"></a>
### Personal Data Deletion Request.redact partial match data

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_redact_partial_match_data_2`

**Inputs** self, doctype.

**State and service calls** execute a supplied database query.

**Local steps**

- Set match\_fields from list().
- Set editable\_text\_fields from set(“Small Text”, “Text”, “Text Editor”, “Code”, …).
- For each df in Platform.get\_meta(doctype at “doctype”).fields.
  - If df.fieldtype does not belong to editable\_text\_fields.
    - Continue with the next iteration or loop test.
  - Update match\_fields using + list(formatted text ′{df.fieldname}′= REPLACE(REPLACE(′{df.fieldname}′, %(name)s, 'REDACTED'), %(email)s, '{self.anon}')).
- Set update\_predicate from formatted text SET  {“, ”.join(match\_fields)}.
- Set where\_predicate from empty text when doctype.get(“strict”), otherwise formatted text WHERE ′{doctype.get(“filter\_by”, “owner”)}′ = %(email)s.
  - Value choice on doctype.get(“strict”) — true gives empty text, false gives formatted text WHERE ′{doctype.get(“filter\_by”, “owner”)}′ = %(email)s.
- Evaluate Platform.db.sql(formatted text UPDATE ′tab{doctype at “doctype”}′ {update\_predicate} {where\_predicate}, mapping(“name” → self.full\_name, “email” → self.email)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L4590) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1243)

<a id="op-3a1464b99733d3"></a>
### Personal Data Deletion Request.put on hold

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_personal_data_deletion_request_put_on_hold`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Evaluate self.db\_set(“status”, “On Hold”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L30) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L293) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1240)

<a id="op-a492d0177080c7"></a>
### Process data deletion request

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_process_data_deletion_request`

**Inputs** no declared parameters.

**Record and data access** read “Website Settings” via get\_single\_value · read “Personal Data Deletion Request” via get\_all · resolve a document from “Personal Data Deletion Request” via get\_doc.

**Explicit results** no value.

**Local steps**

- Set auto\_account\_deletion from Platform.db.get\_single\_value(“Website Settings”, “auto\_account\_deletion”).
- If auto\_account\_deletion &lt; 1.
  - Return no value.
- Set requests from Platform.get\_all(“Personal Data Deletion Request”, filters = mapping(“status” → “Pending Approval”), pluck = “name”).
- For each request in requests.
  - Set doc from Platform.get\_doc(“Personal Data Deletion Request”, request).
  - If time\_diff\_in\_hours(get\_datetime(), doc.creation) ≥ auto\_account\_deletion.
    - Evaluate doc.add\_comment(“Comment”, translated “The User record for this request has been auto-deleted due to inactivity by system admins.”).
    - Evaluate doc.trigger\_data\_deletion().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Website Settings”, “auto\_account\_deletion”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0523.json#L5183) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L305) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1252)

<a id="op-4ec271610c300e"></a>
### Remove unverified record

`operation_foundation_website_record_definitions_personal_data_deletion_request_business_behavior_remove_unverified_record`

**Inputs** no declared parameters.

**State and service calls** execute query text (DELETE, Personal Data Deletion Request).

**Local steps**

- Evaluate Platform.db.sql(query text (DELETE, Personal Data Deletion Request)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0019.json#L31) · [Binding](../../../current-decisions/foundation/bindings-008.tsv#L306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L1253)
