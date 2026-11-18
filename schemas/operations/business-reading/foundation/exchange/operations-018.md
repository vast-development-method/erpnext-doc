# Integration and transport · operations 18

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email unsubscribe

[Record definition](../../../../data/record-types/email_unsubscribe.json)

<a id="op-4d22957a40eb4d"></a>
### Email Unsubscribe.on update

`operation_foundation_email_record_definitions_email_unsubscribe_business_behavior_email_unsubscribe_on_update`

**Inputs** self.

**Record and data access** resolve a document from self.reference\_doctype via get\_doc.

**Local steps**

- If (self.reference\_doctype and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_doctype → self.reference\_name.
  - Set doc from Platform.get\_doc(self.reference\_doctype, self.reference\_name).
  - Evaluate doc.add\_comment(“Label”, translated “Left this conversation”, comment\_email = self.email).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0228.json#L6361) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L201)

## Record · Geolocation settings

[Record definition](../../../../data/record-types/geolocation_settings.json)

<a id="op-8542f47ef7b066"></a>
### Autocomplete

`operation_foundation_integrations_record_definitions_geolocation_settings_business_behavior_autocomplete`

**Inputs** txt.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Geolocation Settings” via get\_single.

**Explicit results** list() · list(provider.autocomplete(txt)).

**Explicit failure paths** validation helper — translated “This geolocation provider is not supported yet.” · Platform.ValidationError(translated “Address autocomplete failed”).

**Local steps**

- If not txt.
  - Return list().
- Set settings from Platform.get\_single(“Geolocation Settings”).
- If not settings.enable\_address\_autocompletion.
  - Return list().
- If settings.provider equals “Geoapify”.
  - Set provider from Geoapify(settings.get\_password(“api\_key”), Platform.local.lang).
- Otherwise.
  - If settings.provider equals “Nomatim”.
    - Set provider from Nomatim(base\_url = settings.base\_url, referer = get\_url(), lang = Platform.local.lang).
  - Otherwise.
    - If settings.provider equals “HERE”.
      - Set provider from Here(settings.get\_password(“api\_key”), Platform.local.lang).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “This geolocation provider is not supported yet.”).
- Attempt the following.
  - Return list(provider.autocomplete(txt)).
- On failure (requests.RequestException) bound to e.
  - Set status from getattr(e.response, “status\_code”, no value).
  - Evaluate Platform.log\_error(title = “Address autocomplete failed”, message = formatted text {type(e).\_\_name\_\_} (status {status})).
  - Raise Platform.ValidationError(translated “Address autocomplete failed”) with cause no value.

**Values supplied outside this operation** selected callable from getattr(e.response, “status\_code”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L59) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1991) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L711)

<a id="op-f3f69a7c06d5a6"></a>
### Geoapify.initialize

`operation_foundation_integrations_record_definitions_geolocation_settings_providers_geoapify_business_behavior_geoapify_initialize`

**Inputs** self, api\_key, lang = no value.

**Local steps**

- Set self.api\_key from api\_key.
- Set self.lang from lang.
- Set self.base\_url from text in the contract.

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0247.json#L7359) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1993) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L713)

<a id="op-d7c606e77f815c"></a>
### Geoapify.autocomplete

`operation_foundation_integrations_record_definitions_geolocation_settings_providers_geoapify_business_behavior_geoapify_autocomplete`

**Inputs** self, query.

**Local steps**

- Set params from mapping(“text” → query, “apiKey” → self.api\_key, “limit” → 5, “format” → “json”, …).
- Set response from requests.get(formatted text {self.base\_url}/v1/geocode/autocomplete, params = params).
- Evaluate response.raise\_for\_status().
- Set results from response.json() at “results”.
- For each result in results.
  - yield mapping(“label” → result at “formatted”, “value” → json.dumps(mapping(“address\_line1” → result.get(“address\_line1”), “city” → result.get(“city”), “state” → result.get(“state”), “pincode” → result.get(“post ….

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** service or queued work from requests.get(formatted text {self.base\_url}/v1/geocode/autocomplete, params = params).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1992) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L712)

<a id="op-1ee8b1fb5b212b"></a>
### Here.initialize

`operation_foundation_integrations_record_definitions_geolocation_settings_providers_here_business_behavior_here_initialize`

**Inputs** self, api\_key, lang = no value.

**Local steps**

- Set self.lang from lang.
- Set self.api\_key from api\_key.
- Set self.base\_url from text in the contract.

If control reaches the end, it returns no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L509) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1995) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L715)

<a id="op-32709cd0156874"></a>
### Here.autocomplete

`operation_foundation_integrations_record_definitions_geolocation_settings_providers_here_business_behavior_here_autocomplete`

**Inputs** self, query.

**Record and data access** read “Country” via get\_value.

**Local steps**

- Set params from mapping(“q” → query, “apiKey” → self.api\_key, “limit” → 5, “lang” → self.lang).
- Set response from requests.get(formatted text {self.base\_url}/autocomplete, params = params).
- Evaluate response.raise\_for\_status().
- Set results from response.json() at “items”.
- For each result in results.
  - Set address from result at “address”.
  - Set py\_country from pycountry.countries.get(alpha\_3 = address.get(“countryCode”)).
  - Set Platform\_country from Platform.db.get\_value(“Country”, mapping(“code” → py\_country.alpha\_2.lower())).
  - yield mapping(“label” → address at “label”, “value” → json.dumps(mapping(“address\_line1” → formatted text {nested operand in the contract} {nested operand in the contract}.strip(), “city” → address.get(“city”, e ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform\_country → empty text.

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** service or queued work from requests.get(formatted text {self.base\_url}/autocomplete, params = params).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L627) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1994) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L714)

<a id="op-d68651e236032d"></a>
### Nomatim.initialize

`operation_foundation_integrations_record_definitions_geolocation_settings_providers_nomatim_business_behavior_nomatim_initialize`

**Inputs** self, base\_url, referer, lang = no value.

**Local steps**

- Set self.lang from lang.
- Set self.referer from referer.
- Set self.base\_url from base\_url.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L1329) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1997) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L717)

<a id="op-2c8d70e343e845"></a>
### Nomatim.autocomplete

`operation_foundation_integrations_record_definitions_geolocation_settings_providers_nomatim_business_behavior_nomatim_autocomplete`

**Inputs** self, query.

**Record and data access** read “Country” via get\_value.

**Local steps**

- Set params from mapping(“q” → query, “format” → “json”, “limit” → 5, “addressdetails” → 1, …).
- Set response from requests.get(formatted text {self.base\_url}/search, params = params, headers = mapping(“Referer” → self.referer)).
- Evaluate response.raise\_for\_status().
- Set results from response.json().
- For each result in results.
  - If “address” does not belong to result.
    - Continue with the next iteration or loop test.
  - Set address from result at “address”.
  - yield mapping(“label” → result at “display\_name”, “value” → json.dumps(mapping(“address\_line1” → formatted text {nested operand in the contract} {nested operand in the contract}.strip(), “city” → (nested operand ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in address.get(“city”) → address.get(“town”) → address.get(“village”).

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** service or queued work from requests.get(formatted text {self.base\_url}/search, params = params, headers = mapping(“Referer” → self.referer)).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L1457) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1996) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L716)

## Record · Google calendar

[Record definition](../../../../data/record-types/google_calendar.json)

<a id="op-aa0cd57973af62"></a>
### Google Calendar.validate

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_google_calendar_validate`

**Inputs** self.

**Record and data access** resolve a document from “Google Settings” via get\_cached\_doc.

**Explicit results** google\_settings.

**Explicit failure paths** validation helper — translated “Enable Google API in Google Settings.” · validation helper — translated “Enter Client Id and Client Secret in Google Settings.”.

**Local steps**

- Set google\_settings from Platform.get\_cached\_doc(“Google Settings”).
- If not google\_settings.enable.
  - Call the validation error handler Platform.throw(translated “Enable Google API in Google Settings.”).
- If (not google\_settings.client\_id or not google\_settings.client\_secret).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not google\_settings.client\_id → not google\_settings.client\_secret.
  - Call the validation error handler Platform.throw(translated “Enter Client Id and Client Secret in Google Settings.”).
- Return google\_settings.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Google Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L2185) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L4) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L730)

<a id="op-c1e95f68f316e3"></a>
### Google Calendar.get access token

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_google_calendar_get_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self.

**Explicit result forms** the result of a delegated call.

**Locally raised failures** ValidationError.

**Observed service boundaries** validation or user-notification service.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L2388) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L2) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L728)

<a id="op-1587f1bb366a7c"></a>
### Authorize access

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_authorize_access`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** g\_calendar, reauthorize.

**Explicit result forms** the result of a delegated call.

**Observed service boundaries** effective access lookup, record lookup, record mutation request, transaction control, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L2893) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1998) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L718)

<a id="op-91d5954bb76e09"></a>
### Get authentication url

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_get_authentication_resource_address`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** client\_id, redirect\_uri.

**Explicit result forms** a structured result.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L3782) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2003) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L723)

<a id="op-0d2af872c66a63"></a>
### Google callback

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_google_callback`

**Inputs** code = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** request set\_value on “Google Calendar” · commit.

**Local steps**

- Set google\_calendar from Platform.cache.hget(“google\_calendar”, “google\_calendar”).
- Evaluate Platform.db.set\_value(“Google Calendar”, google\_calendar, “authorization\_code”, code).
- Evaluate Platform.db.commit().
- Evaluate authorize\_access(google\_calendar).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L3895) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L5) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L731)

<a id="op-372e95c227084a"></a>
### Sync

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_sync`

**Inputs** g\_calendar = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Google Calendar” via get\_list.

**Explicit results** user\_messages.

**Local steps**

- Set filters from mapping(“enable” → 1, “pull\_from\_google\_calendar” → 1).
- Set user\_messages from list().
- If g\_calendar.
  - Evaluate filters.update(mapping(“name” → g\_calendar)).
- For each g in Platform.get\_list(“Google Calendar”, filters = filters, pluck = “name”).
  - Evaluate user\_messages.append(sync\_events\_from\_google\_calendar(g)).
- Return user\_messages.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L4100) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L11) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L737)

<a id="op-452d263ac336bf"></a>
### Get google calendar object

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_get_google_calendar_object`

**Inputs** g\_calendar.

**Record and data access** resolve a document from “Google Settings” via get\_cached\_doc · resolve a document from “Google Calendar” via get\_doc.

**Explicit results** tuple(google\_calendar, account.reload()).

**Local steps**

- Bind dependencies google.oauth2.credentials.
- Bind dependencies build.
- Set google\_settings from Platform.get\_cached\_doc(“Google Settings”).
- Set account from Platform.get\_doc(“Google Calendar”, g\_calendar).
- Set credentials from google.oauth2.credentials.Credentials(token = account.get\_access\_token(), refresh\_token = account.get\_password(fieldname = “refresh\_token”, raise\_exception = false), token\_uri = GoogleOAuth.OAUTH\_URL, clie ….
- Set google\_calendar from build(serviceName = “calendar”, version = “v3”, credentials = credentials, static\_discovery = false).
- Evaluate check\_google\_calendar(account.reload(), google\_calendar).
- Return tuple(google\_calendar, account.reload()).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Google Settings”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L4381) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2005) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L725)

<a id="op-9d5df5d96691df"></a>
### Check google calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_check_google_calendar`

**Inputs** account, google\_calendar.

**State and service calls** call insert on google\_calendar.calendars() · call db\_set on account · commit.

**Explicit results** google\_calendar.calendars().get(calendarId = account.google\_calendar\_id).execute().

**Explicit failure paths** validation helper — translated “Google Calendar - Could not find Calendar for {0}, error code {1}.”.format(account.name, err.resp.status) · validation helper — translated “Google Calendar - Could not create Calendar for {0}, error code {1}.”.format(account.name, err.resp.status).

**Local steps**

- Bind dependencies HttpError.
- If account.google\_calendar\_id.
  - Attempt the following.
    - Return google\_calendar.calendars().get(calendarId = account.google\_calendar\_id).execute().
  - On failure (HttpError) bound to err.
    - Call the validation error handler Platform.throw(translated “Google Calendar - Could not find Calendar for {0}, error code {1}.”.format(account.name, err.resp.status)).
- Set calendar from mapping(“summary” → account.calendar\_name, “timeZone” → Platform.get\_system\_settings(“time\_zone”)).
- Attempt the following.
  - Set created\_calendar from google\_calendar.calendars().insert(body = calendar).execute().
- On failure (HttpError) bound to err.
  - Call the validation error handler Platform.throw(translated “Google Calendar - Could not create Calendar for {0}, error code {1}.”.format(account.name, err.resp.status)).
- Evaluate account.db\_set(“google\_calendar\_id”, created\_calendar.get(“id”)).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“time\_zone”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L4805) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1999) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L719)

<a id="op-cce4714395467f"></a>
### Sync events from google calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_sync_events_from_google_calendar`

**Inputs** g\_calendar, method = no value.

**Record and data access** read “Event” via exists · read “Event” via get\_value · resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → “Event”, “reference\_name” → event\_name, …) via get\_doc.

**State and service calls** commit · msgprint with msg · call save on account · publish realtime with “import\_google\_calendar” · request set\_value on “Event” · 1 additional forms in the steps below.

**Explicit results** no value · translated “No Google Calendar Event to sync.” · translated “1 Google Calendar Event synced.” · translated “{0} Google Calendar Events synced.”.format(len(results)).

**Explicit failure paths** validation helper — msg.

**Local steps**

- Bind dependencies HttpError.
- Set tuple(google\_calendar, account) from get\_google\_calendar\_object(g\_calendar).
- If not account.pull\_from\_google\_calendar.
  - Return no value.
- Set sync\_token from (account.get\_password(fieldname = “next\_sync\_token”, raise\_exception = false) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in account.get\_password(fieldname = “next\_sync\_token”, raise\_exception = false) → no value.
- Set events from Platform.\_dict().
- Set results from list().
- While true.
  - Attempt the following.
    - Set events from google\_calendar.events().list(calendarId = account.google\_calendar\_id, maxResults = 2000, pageToken = events.get(“nextPageToken”), singleEvents = false, …).execute().
  - On failure (HttpError) bound to err.
    - Set msg from translated “Google Calendar - Could not fetch event from Google Calendar, error code {0}.”.format(err.resp.status).
    - If err.resp.status equals 410.
      - Evaluate set\_encrypted\_password(“Google Calendar”, account.name, empty text, “next\_sync\_token”).
      - Evaluate Platform.db.commit().
      - Update msg using + (one space + translated “Sync token was invalid and has been reset, Retry syncing.”).
      - Evaluate Platform.msgprint(msg, title = “Invalid Sync Token”, indicator = “blue”).
    - Otherwise.
      - Call the validation error handler Platform.throw(msg).
  - Evaluate results.extend(generator of event for event drawn from events.get(“items”, list())).
    - Draw event from events.get(“items”, list()).
  - If not events.get(“nextPageToken”).
    - If events.get(“nextSyncToken”).
      - Set account.next\_sync\_token from events.get(“nextSyncToken”).
      - Evaluate account.save().
    - Leave the innermost loop without its normal-exhaustion alternative.
- For each tuple(idx, event) in enumerate(results).
  - Evaluate Platform.publish\_realtime(“import\_google\_calendar”, mapping(“progress” → (idx + 1), “total” → len(results)), user = Platform.session.user).
  - If event.get(“status”) equals “confirmed”.
    - Set recurrence from no value.
    - If event.get(“recurrence”).
      - Within suppress(IndexError).
        - Set recurrence from event.get(“recurrence”) at 0.
    - If event.get(“recurringEventId”).
    - Otherwise.
      - If not Platform.db.exists(“Event”, mapping(“google\_calendar\_event\_id” → event.get(“id”))).
        - Evaluate insert\_event\_to\_calendar(account, event, recurrence).
      - Otherwise.
        - Evaluate update\_event\_in\_calendar(account, event, recurrence).
  - Otherwise.
    - If event.get(“status”) equals “cancelled”.
      - Set event\_name from Platform.db.get\_value(“Event”, mapping(“google\_calendar\_id” → account.google\_calendar\_id, “google\_calendar\_event\_id” → event.get(“id”))).
      - If event\_name.
        - Evaluate Platform.db.set\_value(“Event”, event\_name, “status”, “Closed”).
        - Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → “Event”, “reference\_name” → event\_name, …)).insert(ignore\_permissions = true).
- If not results.
  - Return translated “No Google Calendar Event to sync.”.
- Otherwise.
  - If len(results) equals 1.
    - Return translated “1 Google Calendar Event synced.”.
  - Otherwise.
    - Return translated “{0} Google Calendar Events synced.”.format(len(results)).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“import\_google\_calendar”, mapping(“progress” → (idx + 1), “total” → len(results)), user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0248.json#L5305) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L12) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L738)

<a id="op-c58b4eb2f7867f"></a>
### Insert event to calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_insert_event_to_calendar`

**Inputs** account, event, recurrence = no value.

**Record and data access** resolve a document from calendar\_event via get\_doc.

**State and service calls** call insert on e · call db\_set on e.

**Local steps**

- Set calendar\_event from (mapping(“doctype” → “Event”, “subject” → (event.get(“summary”) or “No Title”), “description” → event.get(“description”), “google\_calendar\_event” → 1, …) bitwise or google\_calendar\_to\_repeat\_on(recurrence  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in event.get(“summary”) → “No Title”.
  - Value choice on account.sync\_as\_public — true gives “Public”, false gives “Private”.
- Set e from Platform.get\_doc(calendar\_event).
- Evaluate update\_participants\_in\_event(calendar\_event = e, google\_event = event).
- Evaluate e.insert(ignore\_permissions = true).
- Evaluate e.db\_set(“owner”, account.user, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L7) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L733)

<a id="op-3dda1c53cf26d3"></a>
### Update participants in event

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_update_participants_in_event`

**Inputs** calendar\_event, google\_event.

**Record and data access** read “User” via get\_all.

**Local steps**

- Set google\_event\_participants from list of attendee at “email” for attendee drawn from google\_event.get(“attendees”, list()) where not attendee.get(“self”).
  - Draw attendee from google\_event.get(“attendees”, list()), keep a combination only if (not attendee.get(“self”)).
- Set in\_system\_participants from Platform.get\_all(“User”, filters = mapping(“email” → tuple(“in”, google\_event\_participants)), pluck = “email”).
- Set existing\_calendar\_participants from list of participant.reference\_docname for participant drawn from calendar\_event.event\_participants where participant.reference\_doctype equals “User”.
  - Draw participant from calendar\_event.event\_participants, keep a combination only if (participant.reference\_doctype equals “User”).
- For each participant in in\_system\_participants.
  - If participant does not belong to existing\_calendar\_participants.
    - Evaluate calendar\_event.add\_participant(“User”, participant).
- If len(in\_system\_participants) &lt; len(google\_event\_participants).
  - Evaluate calendar\_event.add\_participant(“User”, “Guest”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L563) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L15) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L741)

<a id="op-ad649b17928448"></a>
### Update event in calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_update_event_in_calendar`

**Inputs** account, event, recurrence = no value.

**Record and data access** resolve a document from “Event” via get\_doc.

**State and service calls** call save on calendar\_event.

**Local steps**

- Set calendar\_event from Platform.get\_doc(“Event”, mapping(“google\_calendar\_event\_id” → event.get(“id”))).
- Set calendar\_event.subject from event.get(“summary”).
- Set calendar\_event.description from event.get(“description”).
- Set calendar\_event.google\_meet\_link from event.get(“hangoutLink”).
- Evaluate calendar\_event.update(google\_calendar\_to\_repeat\_on(recurrence = recurrence, start = event.get(“start”), end = event.get(“end”))).
- Evaluate update\_participants\_in\_event(calendar\_event, event).
- Evaluate calendar\_event.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L999) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L13) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L739)

<a id="op-e4a8ee692d62db"></a>
### Insert event in google calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_insert_event_in_google_calendar`

**Inputs** doc, method = no value.

**Record and data access** read “Google Calendar” via exists.

**State and service calls** call insert on google\_calendar.events() · request set\_value on “Event” · msgprint with translated “Event Synced with Google Calendar.”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Google Calendar - Could not insert event in Google Calendar {0}, error code {1}.”.format(account.name, err.resp.status).

**Local steps**

- Bind dependencies HttpError.
- If (not doc.sync\_with\_google\_calendar or doc.pulled\_from\_google\_calendar or not Platform.db.exists(“Google Calendar”, mapping(“name” → doc.google\_calendar))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.sync\_with\_google\_calendar → doc.pulled\_from\_google\_calendar → not Platform.db.exists(“Google Calendar”, mapping(“name” → doc.google\_calendar)).
  - Return no value.
- Set tuple(google\_calendar, account) from get\_google\_calendar\_object(doc.google\_calendar).
- If not account.push\_to\_google\_calendar.
  - Return no value.
- Set event from mapping(“summary” → doc.subject, “description” → doc.description, “google\_calendar\_event” → 1).
- Evaluate event.update(format\_date\_according\_to\_google\_calendar(doc.all\_day, get\_datetime(doc.starts\_on), get\_datetime(doc.ends\_on) when doc.ends\_on, otherwise no value)).
  - Value choice on doc.ends\_on — true gives get\_datetime(doc.ends\_on), false gives no value.
- If doc.repeat\_on.
  - Evaluate event.update(mapping(“recurrence” → repeat\_on\_to\_google\_calendar\_recurrence\_rule(doc))).
- Evaluate event.update(mapping(“attendees” → get\_attendees(doc))).
- Set conference\_data\_version from 0.
- If doc.add\_video\_conferencing.
  - Evaluate event.update(mapping(“conferenceData” → get\_conference\_data(doc))).
  - Set conference\_data\_version from 1.
- Attempt the following.
  - Set event from google\_calendar.events().insert(calendarId = doc.google\_calendar\_id, body = event, conferenceDataVersion = conference\_data\_version, sendUpdates = “all”).execute().
  - Evaluate Platform.db.set\_value(“Event”, doc.name, mapping(“google\_calendar\_event\_id” → event.get(“id”), “google\_meet\_link” → event.get(“hangoutLink”)), update\_modified = false).
  - Evaluate Platform.msgprint(translated “Event Synced with Google Calendar.”).
- On failure (HttpError) bound to err.
  - Call the validation error handler Platform.throw(translated “Google Calendar - Could not insert event in Google Calendar {0}, error code {1}.”.format(account.name, err.resp.status)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L1381) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L6) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L732)

<a id="op-3ffb7107650bb8"></a>
### Update event in google calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_update_event_in_google_calendar`

**Inputs** doc, method = no value.

**Record and data access** read “Google Calendar” via exists.

**State and service calls** request set\_value on “Event” · msgprint with translated “Event Synced with Google Calendar.”.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Google Calendar - Could not update Event {0} in Google Calendar, error code {1}.”.format(doc.name, err.resp.status).

**Local steps**

- Bind dependencies HttpError.
- If (not doc.sync\_with\_google\_calendar or doc.modified equals doc.creation or not Platform.db.exists(“Google Calendar”, mapping(“name” → doc.google\_calendar))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.sync\_with\_google\_calendar → doc.modified equals doc.creation → not Platform.db.exists(“Google Calendar”, mapping(“name” → doc.google\_calendar)).
  - Return no value.
- If (doc.sync\_with\_google\_calendar and not doc.google\_calendar\_event\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.sync\_with\_google\_calendar → not doc.google\_calendar\_event\_id.
  - Evaluate insert\_event\_in\_google\_calendar(doc).
  - Return no value.
- Set tuple(google\_calendar, account) from get\_google\_calendar\_object(doc.google\_calendar).
- If not account.push\_to\_google\_calendar.
  - Return no value.
- Attempt the following.
  - Set event from google\_calendar.events().get(calendarId = doc.google\_calendar\_id, eventId = doc.google\_calendar\_event\_id).execute().
  - Set event at “summary” from doc.subject.
  - Set event at “description” from doc.description.
  - Set event at “recurrence” from repeat\_on\_to\_google\_calendar\_recurrence\_rule(doc).
  - Set event at “status” from “cancelled” when (doc.status equals “Cancelled” or doc.status equals “Closed”), otherwise event.get(“status”).
    - Value choice on (doc.status equals “Cancelled” or doc.status equals “Closed”) — true gives “cancelled”, false gives event.get(“status”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.status equals “Cancelled” → doc.status equals “Closed”.
  - Evaluate event.update(format\_date\_according\_to\_google\_calendar(doc.all\_day, get\_datetime(doc.starts\_on), get\_datetime(doc.ends\_on) when doc.ends\_on, otherwise no value)).
    - Value choice on doc.ends\_on — true gives get\_datetime(doc.ends\_on), false gives no value.
  - Set conference\_data\_version from 0.
  - If doc.add\_video\_conferencing.
    - Evaluate event.update(mapping(“conferenceData” → get\_conference\_data(doc))).
    - Set conference\_data\_version from 1.
  - Otherwise.
    - If (doc.get\_doc\_before\_save().add\_video\_conferencing or event.get(“hangoutLink”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_doc\_before\_save().add\_video\_conferencing → event.get(“hangoutLink”).
      - Evaluate event.update(mapping(“conferenceData” → no value)).
      - Set conference\_data\_version from 1.
  - Evaluate event.update(mapping(“attendees” → get\_attendees(doc))).
  - Set event from google\_calendar.events().update(calendarId = doc.google\_calendar\_id, eventId = doc.google\_calendar\_event\_id, body = event, conferenceDataVersion = conference\_data\_version, …).execute().
  - Evaluate Platform.db.set\_value(“Event”, doc.name, mapping(“google\_meet\_link” → event.get(“hangoutLink”)), update\_modified = false).
  - Evaluate doc.notify\_update().
  - Evaluate Platform.msgprint(translated “Event Synced with Google Calendar.”).
- On failure (HttpError) bound to err.
  - Call the validation error handler Platform.throw(translated “Google Calendar - Could not update Event {0} in Google Calendar, error code {1}.”.format(doc.name, err.resp.status)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L2297) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L14) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L740)

<a id="op-dddf19cd8299e6"></a>
### Delete event from google calendar

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_delete_event_from_google_calendar`

**Inputs** doc, method = no value.

**Record and data access** read “Google Calendar” via exists.

**State and service calls** msgprint with translated “Google Calendar - Could not delete Event {0} from Google Calendar, error code {1}.”.format(doc.name, err.resp.status).

**Explicit results** no value.

**Local steps**

- Bind dependencies HttpError.
- If not Platform.db.exists(“Google Calendar”, mapping(“name” → doc.google\_calendar, “push\_to\_google\_calendar” → 1)).
  - Return no value.
- Set tuple(google\_calendar, \_) from get\_google\_calendar\_object(doc.google\_calendar).
- Attempt the following.
  - Set event from google\_calendar.events().get(calendarId = doc.google\_calendar\_id, eventId = doc.google\_calendar\_event\_id).execute().
  - Set event at “recurrence” from no value.
  - Set event at “status” from “cancelled”.
  - Evaluate google\_calendar.events().update(calendarId = doc.google\_calendar\_id, eventId = doc.google\_calendar\_event\_id, body = event).execute().
- On failure (HttpError) bound to err.
  - Evaluate Platform.msgprint(translated “Google Calendar - Could not delete Event {0} from Google Calendar, error code {1}.”.format(doc.name, err.resp.status)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L3518) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L2000) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L720)

<a id="op-c1cb5225ea87ab"></a>
### Parse google calendar date

`operation_foundation_integrations_record_definitions_google_calendar_business_behavior_parse_google_calendar_date`

**Inputs** dt.

**Explicit results** get\_datetime(dt.get(“date”)) · parser.parse(nested operand in the contract.get(“dateTime”)).astimezone(ZoneInfo(get\_system\_timezone())).replace(tzinfo = no value).

**Local steps**

- If dt.get(“date”).
  - Return get\_datetime(dt.get(“date”)).
- Return parser.parse(nested operand in the contract.get(“dateTime”)).astimezone(ZoneInfo(get\_system\_timezone())).replace(tzinfo = no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0249.json#L3978) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L8) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L734)
