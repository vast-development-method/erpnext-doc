# Integration and transport · operations 19

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Google calendar

[Record definition](../../../../data/record-types/google_calendar.json)

<a id="op-686a2cafbf1481"></a>
### Google calendar to repeat on

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_google_calendar_to_repeat_on`

**Inputs** start (named only), end (named only), recurrence (named only, default no value).

**Explicit results** repeat\_on.

**Local steps**

- Set repeat\_on from mapping(“starts\_on” → parse\_google\_calendar\_date(start), “ends\_on” → parse\_google\_calendar\_date(end), “all\_day” → 1 when start.get(“date”), otherwise 0, “repeat\_this\_event” → 1 when recurrence, otherwise 0, …).
  - Value choice on start.get(“date”) — true gives 1, false gives 0.
  - Value choice on recurrence — true gives 1, false gives 0.
- If not recurrence.
  - Return repeat\_on.
- Set tuple(google\_calendar\_frequency, until, byday) from get\_recurrence\_parameters(recurrence).
- Set repeat\_on at “repeat\_on” from google\_calendar\_frequencies.get(google\_calendar\_frequency).
- If repeat\_on at “repeat\_on” equals “Daily”.
  - Set repeat\_on at “ends\_on” from no value.
  - Set repeat\_on at “repeat\_till” from until.
- If (byday and repeat\_on at “repeat\_on” equals “Weekly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in byday → repeat\_on at “repeat\_on” equals “Weekly”.
  - Set repeat\_on at “repeat\_till” from until.
  - For each repeat\_day in byday.
    - Set repeat\_on at google\_calendar\_days at repeat\_day from 1.
- If (byday and repeat\_on at “repeat\_on” equals “Monthly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in byday → repeat\_on at “repeat\_on” equals “Monthly”.
  - Set byday from byday at 0.
  - Set tuple(repeat\_day\_week\_number, repeat\_day\_name) from tuple(no value, no value).
  - For each num in list(“-2”, “-1”, “1”, “2”, …).
    - If num belongs to byday.
      - Set repeat\_day\_week\_number from num.
      - Leave the innermost loop without its normal-exhaustion alternative.
  - For each day in list(“MO”, “TU”, “WE”, “TH”, …).
    - If day belongs to byday.
      - Set repeat\_day\_name from google\_calendar\_days.get(day).
      - Leave the innermost loop without its normal-exhaustion alternative.
  - Set start\_date from parse\_google\_calendar\_recurrence\_rule(int(repeat\_day\_week\_number), repeat\_day\_name).
  - Set repeat\_on at “starts\_on” from start\_date.
  - Set repeat\_on at “ends\_on” from add\_to\_date(start\_date, minutes = 5).
  - Set repeat\_on at “repeat\_till” from until.
- If repeat\_on at “repeat\_till” equals “Yearly”.
  - Set repeat\_on at “ends\_on” from no value.
  - Set repeat\_on at “repeat\_till” from until.
- Return repeat\_on.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L4177) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L3) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L729)

<a id="op-ab607200e24912"></a>
### Format date according to google calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_format_date_according_to_google_calendar`

**Inputs** all\_day, starts\_on, ends\_on = no value.

**Explicit results** date\_format.

**Local steps**

- If not ends\_on.
  - Set ends\_on from (starts\_on + timedelta(minutes = 10)).
- Set date\_format from mapping(“start” → mapping(“dateTime” → starts\_on.isoformat(), “timeZone” → get\_system\_timezone()), “end” → mapping(“dateTime” → ends\_on.isoformat(), “timeZone” → get\_system\_timezone())).
- If all\_day.
  - Evaluate date\_format at “start”.pop(“dateTime”).
  - Evaluate date\_format at “end”.pop(“dateTime”).
  - Evaluate date\_format at “start”.update(mapping(“date” → starts\_on.date().isoformat())).
  - Evaluate date\_format at “end”.update(mapping(“date” → ends\_on.date().isoformat())).
- Return date\_format.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L5315) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2001) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L721)

<a id="op-4766b125a4459d"></a>
### Parse google calendar recurrence rule

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_parse_google_calendar_recurrence_rule`

**Inputs** repeat\_day\_week\_number, repeat\_day\_name.

**Explicit results** current\_date.

**Local steps**

- If repeat\_day\_week\_number &lt; 0.
  - Set repeat\_day\_week\_number from 4.
- Set weekdays from get\_weekdays().
- Set current\_date from now\_datetime().
- Set tuple(isset\_day\_name, isset\_day\_number) from tuple(false, false).
- While not isset\_day\_name.
  - Set isset\_day\_name from true when weekdays at nested operand in the contract.weekday().lower() equals repeat\_day\_name, otherwise false.
    - Value choice on weekdays at current\_date.weekday().lower() equals repeat\_day\_name — true gives true, false gives false.
  - Set current\_date from add\_days(current\_date, 1) when not isset\_day\_name, otherwise current\_date.
    - Value choice on not isset\_day\_name — true gives add\_days(current\_date, 1), false gives current\_date.
- While not isset\_day\_number.
  - Set week\_number from get\_week\_number(current\_date).
  - Set isset\_day\_number from true when week\_number equals repeat\_day\_week\_number, otherwise false.
    - Value choice on week\_number equals repeat\_day\_week\_number — true gives true, false gives false.
  - Set weeks from 1 when week\_number &lt; repeat\_day\_week\_number, otherwise negative 1.
    - Value choice on week\_number &lt; repeat\_day\_week\_number — true gives 1, false gives negative 1.
  - Set current\_date from add\_to\_date(current\_date, weeks = weeks) when not isset\_day\_number, otherwise current\_date.
    - Value choice on not isset\_day\_number — true gives add\_to\_date(current\_date, weeks = weeks), false gives current\_date.
- Return current\_date.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L5764) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L9) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L735)

<a id="op-cf94b3cae8ce1f"></a>
### Repeat on to google calendar recurrence rule

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_repeat_on_to_google_calendar_recurrence_rule`

**Inputs** doc.

**Explicit results** list(recurrence).

**Local steps**

- Set recurrence from framework\_frequencies.get(doc.repeat\_on).
- Set weekdays from get\_weekdays().
- If doc.repeat\_on equals “Weekly”.
  - Set byday from list of framework\_days.get(day.lower()) for day drawn from weekdays where doc.get(day.lower()).
    - Draw day from weekdays, keep a combination only if (doc.get(day.lower())).
  - Set recurrence from ((recurrence + “BYDAY=”) + “,”.join(byday)).
- Otherwise.
  - If doc.repeat\_on equals “Monthly”.
    - Set week\_number from str(get\_week\_number(get\_datetime(doc.starts\_on))).
    - Set week\_day from weekdays at get\_datetime(nested operand in the contract.starts\_on).weekday().lower().
    - Set recurrence from (((recurrence + “BYDAY=”) + week\_number) + framework\_days.get(week\_day)).
- Return list(recurrence).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L6212) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L10) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L736)

<a id="op-ec12c9ad9874c6"></a>
### Get week number

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_get_week_number`

**Inputs** dt.

**Explicit results** ceil((adjusted\_dom ÷ 7.0)).

**Local steps**

- Set first\_day from dt.replace(day = 1).
- Set dom from dt.day.
- Set adjusted\_dom from (dom + first\_day.weekday()).
- Return ceil((adjusted\_dom ÷ 7.0)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L6666) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2007) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L727)

<a id="op-cb890aca9c00f5"></a>
### Get recurrence parameters

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_get_recurrence_parameters`

**Inputs** recurrence.

**Declared result** RecurrenceParameters.

**Explicit results** tuple(frequency, until, byday).

**Local steps**

- Set recurrence from recurrence.split(“;”).
- Set tuple(frequency, until, byday) from tuple(no value, no value, list()).
- For each token in recurrence.
  - If “RRULE:FREQ” belongs to token.
    - Set frequency from token.
  - Otherwise.
    - If “UNTIL” belongs to token.
      - Set \_until from token.replace(“UNTIL=”, empty text).rstrip(“Z”).
      - Set fmt from “%Y%m%dT%H%M%S” when “T” belongs to \_until, otherwise “%Y%m%d”.
        - Value choice on “T” belongs to \_until — true gives “%Y%m%dT%H%M%S”, false gives “%Y%m%d”.
      - Set until from datetime.strptime(\_until, fmt).
    - Otherwise.
      - If “BYDAY” belongs to token.
        - Set byday from token.split(“=”, 1) at 1.split(“,”).
- Return tuple(frequency, until, byday).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L6812) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2006) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L726)

<a id="op-f4fab97c35d58f"></a>
### Get conference data

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_get_conference_data`

**Inputs** doc.

**Explicit results** mapping(“createRequest” → mapping(“requestId” → doc.name, “conferenceSolutionKey” → mapping(“type” → “hangoutsMeet”)), “notes” → doc.description).

**Local steps**

- Return mapping(“createRequest” → mapping(“requestId” → doc.name, “conferenceSolutionKey” → mapping(“type” → “hangoutsMeet”)), “notes” → doc.description).

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L7206) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2004) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L724)

<a id="op-f10405e0873fa5"></a>
### Get attendees

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_get_attendees`

**Inputs** doc.

**Record and data access** read “Google Calendar” via get\_value.

**State and service calls** msgprint with translated “Contact / email not found. Did not add attendee for -&lt;br&gt;{0}”.format(text in the contract.join(generator of formatted text {d.get(“dt”)} {d.get(“dn”)} for d drawn from email\_not\_found)).

**Explicit results** attendees.

**Local steps**

- Set tuple(attendees, email\_not\_found) from tuple(list(), list()).
- Set owner from Platform.db.get\_value(“Google Calendar”, doc.google\_calendar, “user”).
- For each participant in doc.event\_participants.
  - Set p\_email from participant.get(“email”).
  - If (p\_email and p\_email differs from owner).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in p\_email → p\_email differs from owner.
    - Evaluate attendees.append(mapping(“email” → p\_email)).
  - Otherwise.
    - Evaluate email\_not\_found.append(mapping(“dt” → participant.reference\_doctype, “dn” → participant.reference\_docname)).
- If email\_not\_found.
  - Evaluate Platform.msgprint(translated “Contact / email not found. Did not add attendee for -&lt;br&gt;{0}”.format(text in the contract.join(generator of formatted text {nested operand in the contract.get(“dt”)} {nested o ….
    - Draw d from email\_not\_found.
- Return attendees.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2002) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L722)

## Record · Google contacts

[Record definition](../../../../data/record-types/google_contacts.json)

<a id="op-76e56e1518f67f"></a>
### Google Contacts.validate

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_google_contacts_validate`

**Inputs** self.

**Record and data access** read “Google Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Enable Google API in Google Settings.”.

**Local steps**

- If not Platform.db.get\_single\_value(“Google Settings”, “enable”).
  - Call the validation error handler Platform.throw(translated “Enable Google API in Google Settings.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Google Settings”, “enable”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L499) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L20) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L746)

<a id="op-9c57839f9e4987"></a>
### Google Contacts.get access token

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_google_contacts_get_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** ValidationError.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L618) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L19) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L745)

<a id="op-2537d34ffe4ebb"></a>
### Authorize access

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_authorize_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** g\_contact, reauthorize, code.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup, record mutation request.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L892) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L16) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L742)

<a id="op-f67e164ae9715a"></a>
### Get google contacts object

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_get_google_contacts_object`

**Inputs** g\_contact.

**Record and data access** resolve a document from “Google Contacts” via get\_doc.

**Explicit results** tuple(google\_contacts, account).

**Local steps**

- Set account from Platform.get\_doc(“Google Contacts”, g\_contact).
- Set oauth\_obj from GoogleOAuth(“contacts”).
- Set google\_contacts from oauth\_obj.get\_google\_service\_object(account.get\_access\_token(), account.get\_password(fieldname = “indexing\_refresh\_token”, raise\_exception = false)).
- Return tuple(google\_contacts, account).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L1393) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L17) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L743)

<a id="op-121becce27871b"></a>
### Sync

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_sync`

**Inputs** g\_contact = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Google Contacts” via get\_list.

**Explicit results** sync\_contacts\_from\_google\_contacts(g.name).

**Local steps**

- Set filters from mapping(“enable” → 1).
- If g\_contact.
  - Evaluate filters.update(mapping(“name” → g\_contact)).
- Set google\_contacts from Platform.get\_list(“Google Contacts”, filters = filters).
- For each g in google\_contacts.
  - Return sync\_contacts\_from\_google\_contacts(g.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L1587) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L22) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L748)

<a id="op-90c7f3d1d437c4"></a>
### Sync contacts from google contacts

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_sync_contacts_from_google_contacts`

**Inputs** g\_contact.

**Record and data access** resolve a document from mapping(“doctype” → “Contact”, “first\_name” → (name.get(“givenName”) or empty text), “middle\_name” → (name.get(“middleName”) or empty text), “last\_name” → (name.get(“familyName”) or empty text), …) via get\_doc.

**State and service calls** request set\_value on “Google Contacts” · commit · publish realtime with “import\_google\_contacts” · call insert on contact.

**Explicit results** no value · translated “{0} Google Contacts synced.”.format(contacts\_updated) when contacts\_updated &gt; 0, otherwise translated “No new Google Contacts synced.”.

**Explicit failure paths** validation helper — translated “Google Contacts - Could not sync contacts from Google Contacts {0}, error code {1}.”.format(account.name, err.resp.status).

**Local steps**

- Bind dependencies HttpError.
- Set tuple(google\_contacts, account) from get\_google\_contacts\_object(g\_contact).
- If not account.pull\_from\_google\_contacts.
  - Return no value.
- Set results from list().
- Set contacts\_updated from 0.
- Set sync\_token from (account.get\_password(fieldname = “next\_sync\_token”, raise\_exception = false) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.get\_password(fieldname = “next\_sync\_token”, raise\_exception = false) → no value.
- Set contacts from Platform.\_dict().
- While true.
  - Attempt the following.
    - Set contacts from nested operand in the contract().connections().list(resourceName = “people/me”, pageToken = contacts.get(“nextPageToken”), syncToken = sync\_token, pageSize = 2000, …).execute().
  - On failure (HttpError) bound to err.
    - Call the validation error handler Platform.throw(translated “Google Contacts - Could not sync contacts from Google Contacts {0}, error code {1}.”.format(account.name, err.resp.status)).
  - Evaluate results.extend(generator of contact for contact drawn from contacts.get(“connections”, list())).
    - Draw contact from contacts.get(“connections”, list()).
  - If not contacts.get(“nextPageToken”).
    - If contacts.get(“nextSyncToken”).
      - Evaluate Platform.db.set\_value(“Google Contacts”, account.name, “next\_sync\_token”, contacts.get(“nextSyncToken”)).
      - Evaluate Platform.db.commit().
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate Platform.db.set\_value(“Google Contacts”, account.name, “last\_sync\_on”, Platform.utils.now\_datetime()).
- For each tuple(idx, connection) in enumerate(results).
  - Evaluate Platform.publish\_realtime(“import\_google\_contacts”, dict(progress = (idx + 1), total = len(results)), user = Platform.session.user).
  - If not connection.get(“names”).
    - Continue with the next iteration or loop test.
  - For each name in connection.get(“names”).
    - If name.get(“metadata”).get(“primary”).
      - Update contacts\_updated using + 1.
      - Set contact from Platform.get\_doc(mapping(“doctype” → “Contact”, “first\_name” → (name.get(“givenName”) or empty text), “middle\_name” → (name.get(“middleName”) or empty text), “last\_name” → (name.get(“familyName”) or empty text), …)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.get(“givenName”) → empty text.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.get(“middleName”) → empty text.
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.get(“familyName”) → empty text.
      - For each email in connection.get(“emailAddresses”, list()).
        - Evaluate contact.add\_email(email\_id = email.get(“value”), is\_primary = 1 when email.get(“metadata”).get(“primary”), otherwise 0).
          - Value choice on email.get(“metadata”).get(“primary”) — true gives 1, false gives 0.
      - For each phone in connection.get(“phoneNumbers”, list()).
        - Evaluate contact.add\_phone(phone = phone.get(“value”), is\_primary\_phone = 1 when phone.get(“metadata”).get(“primary”), otherwise 0).
          - Value choice on phone.get(“metadata”).get(“primary”) — true gives 1, false gives 0.
      - Evaluate contact.insert(ignore\_permissions = true).
- Return translated “{0} Google Contacts synced.”.format(contacts\_updated) when contacts\_updated &gt; 0, otherwise translated “No new Google Contacts synced.”.
  - Value choice on contacts\_updated &gt; 0 — true gives translated “{0} Google Contacts synced.”.format(contacts\_updated), false gives translated “No new Google Contacts synced.”.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime() · service or queued work from Platform.publish\_realtime(“import\_google\_contacts”, dict(progress = (idx + 1), total = len(results)), user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L1821) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L23) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L749)

<a id="op-2283e8efcf5b94"></a>
### Insert contacts to google contacts

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_insert_contacts_to_google_contacts`

**Inputs** doc, method = no value.

**Record and data access** read “Google Contacts” via exists.

**State and service calls** request set\_value on “Contact” · msgprint with translated “Google Calendar - Could not insert contact in Google Contacts {0}, error code {1}.”.format(account.name, err.resp.status).

**Explicit results** no value.

**Local steps**

- Bind dependencies HttpError.
- If (not Platform.db.exists(“Google Contacts”, mapping(“name” → doc.google\_contacts)) or doc.pulled\_from\_google\_contacts or not doc.sync\_with\_google\_contacts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.db.exists(“Google Contacts”, mapping(“name” → doc.google\_contacts)) → doc.pulled\_from\_google\_contacts → not doc.sync\_with\_google\_contacts.
  - Return no value.
- Set tuple(google\_contacts, account) from get\_google\_contacts\_object(doc.google\_contacts).
- If not account.push\_to\_google\_contacts.
  - Return no value.
- Set names from mapping(“givenName” → doc.first\_name, “middleName” → doc.middle\_name, “familyName” → doc.last\_name).
- Set phoneNumbers from list of mapping(“value” → phone\_no.phone) for phone\_no drawn from doc.phone\_nos.
  - Draw phone\_no from doc.phone\_nos.
- Set emailAddresses from list of mapping(“value” → email\_id.email\_id) for email\_id drawn from doc.email\_ids.
  - Draw email\_id from doc.email\_ids.
- Attempt the following.
  - Set contact from google\_contacts.people().createContact(body = mapping(“names” → list(names), “phoneNumbers” → phoneNumbers, “emailAddresses” → emailAddresses)).execute().
  - Evaluate Platform.db.set\_value(“Contact”, doc.name, “google\_contacts\_id”, contact.get(“resourceName”)).
- On failure (HttpError) bound to err.
  - Evaluate Platform.msgprint(translated “Google Calendar - Could not insert contact in Google Contacts {0}, error code {1}.”.format(account.name, err.resp.status)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L3492) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L21) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L747)

<a id="op-7a40d16dfea32b"></a>
### Update contacts to google contacts

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_update_contacts_to_google_contacts`

**Inputs** doc, method = no value.

**Record and data access** read “Google Contacts” via exists.

**State and service calls** msgprint with translated “Contact Synced with Google Contacts.” · msgprint with translated “Google Contacts - Could not update contact in Google Contacts {0}, error code {1}.”.format(account.name, err.resp.status).

**Explicit results** no value.

**Local steps**

- Bind dependencies HttpError.
- If (not Platform.db.exists(“Google Contacts”, mapping(“name” → doc.google\_contacts)) or doc.modified equals doc.creation or not doc.sync\_with\_google\_contacts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not Platform.db.exists(“Google Contacts”, mapping(“name” → doc.google\_contacts)) → doc.modified equals doc.creation → not doc.sync\_with\_google\_contacts.
  - Return no value.
- If (doc.sync\_with\_google\_contacts and not doc.google\_contacts\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sync\_with\_google\_contacts → not doc.google\_contacts\_id.
  - Evaluate insert\_contacts\_to\_google\_contacts(doc).
  - Return no value.
- Set tuple(google\_contacts, account) from get\_google\_contacts\_object(doc.google\_contacts).
- If not account.push\_to\_google\_contacts.
  - Return no value.
- Set names from mapping(“givenName” → doc.first\_name, “middleName” → doc.middle\_name, “familyName” → doc.last\_name).
- Set phoneNumbers from list of mapping(“value” → phone\_no.phone) for phone\_no drawn from doc.phone\_nos.
  - Draw phone\_no from doc.phone\_nos.
- Set emailAddresses from list of mapping(“value” → email\_id.email\_id) for email\_id drawn from doc.email\_ids.
  - Draw email\_id from doc.email\_ids.
- Attempt the following.
  - Set contact from google\_contacts.people().get(resourceName = doc.google\_contacts\_id, personFields = “names,emailAddresses,organizations,phoneNumbers”).execute().
  - Set contact at “names” from list(names).
  - Set contact at “phoneNumbers” from phoneNumbers.
  - Set contact at “emailAddresses” from emailAddresses.
  - Evaluate google\_contacts.people().updateContact(resourceName = doc.google\_contacts\_id, body = mapping(“names” → list(names), “phoneNumbers” → phoneNumbers, “emailAddresses” → emailAddresses, “etag” → contact.get(“e ….
  - Evaluate Platform.msgprint(translated “Contact Synced with Google Contacts.”).
- On failure (HttpError) bound to err.
  - Evaluate Platform.msgprint(translated “Google Contacts - Could not update contact in Google Contacts {0}, error code {1}.”.format(account.name, err.resp.status)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L4134) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L24) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L750)

<a id="op-9d8f5efe91fcc2"></a>
### Get indexed value

`operation_foundation_integrations_record_definitions_google_contacts_business_behavior_get_indexed_value`

**Inputs** d, index, key.

**Explicit results** empty text · d at index.get(key).

**Local steps**

- If not d.
  - Return empty text.
- Attempt the following.
  - Return d at index.get(key).
- On failure (IndexError).
  - Return empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0250.json#L4996) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L18) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L744)

## Service · Google oauth

<a id="op-e513af14b2e512"></a>
### Create google oauth state

`operation_foundation_integrations_google_delegated_authorization_business_behavior_create_google_delegated_authorization_state`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** state.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L6522) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1901) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L639)

<a id="op-87c7ed89be7e05"></a>
### Consume google oauth state

`operation_foundation_integrations_google_delegated_authorization_business_behavior_consume_google_delegated_authorization_state`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** token.

**Explicit result forms** a value selected from the current context, no value.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L6673) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1900) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L638)

<a id="op-0a07654b925ec1"></a>
### Google OAuth.initialize

`operation_foundation_integrations_google_delegated_authorization_business_behavior_google_o_authentication_initialize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, domain, validate, config.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0260.json#L6846) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1905) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L643)

<a id="op-b7107614161ae7"></a>
### Google OAuth.validate google settings

`operation_foundation_integrations_google_delegated_authorization_business_behavior_google_o_authentication_validate_google_settings`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1907) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L645)

<a id="op-664e31245137fa"></a>
### Google OAuth.authorize

`operation_foundation_integrations_google_delegated_authorization_business_behavior_google_o_authentication_authorize`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, oauth\_code.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L228) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1902) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L640)

<a id="op-f31a83ee151197"></a>
### Google OAuth.refresh access token

`operation_foundation_integrations_google_delegated_authorization_business_behavior_google_o_authentication_refresh_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, refresh\_token.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L553) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1906) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L644)

<a id="op-bac46df0850eaf"></a>
### Google OAuth.get authentication url

`operation_foundation_integrations_google_delegated_authorization_business_behavior_google_o_authentication_get_authentication_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, state.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0261.json#L851) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1903) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L641)
