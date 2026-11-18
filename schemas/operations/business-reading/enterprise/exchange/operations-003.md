# Integrations and service calls · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Common code

[Record definition](../../../../data/record-types/common_code.json)

<a id="op-0511b8c85479ca"></a>
### Common Code.validate distinct references

`operation_enterprise_edi_record_definitions_common_code_business_behavior_common_code_validate_distinct_references`

**Inputs** self.

**Record and data access** read “Common Code” via get\_all.

**Explicit failure paths** validation helper — translated “{0} {1} is already linked to Common Code {2}.”.format(link.link\_doctype, link.link\_name, get\_link\_to\_form(“Common Code”, existing\_link at “name”, existing\_link at “common\_code”)).

**Local steps**

- For each link in self.applies\_to.
  - Set existing\_links from Platform.get\_all(“Common Code”, filters = list(list(“name”, “!=”, self.name), list(“code\_list”, “=”, self.code\_list), list(“Dynamic Link”, “link\_doctype”, “=”, link.link\_doctype), list(“Dynamic Link”, “lin ….
  - If existing\_links.
    - Set existing\_link from existing\_links at 0.
    - Call the validation error handler Platform.throw(translated “{0} {1} is already linked to Common Code {2}.”.format(link.link\_doctype, link.link\_name, get\_link\_to\_form(“Common Code”, existing\_link at “name”, existing\_link at “common\_code”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L1161) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L127) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L43)

<a id="op-f485caced7375c"></a>
### Common Code.from genericode

`operation_enterprise_edi_record_definitions_common_code_business_behavior_common_code_from_genericode`

**Inputs** self, column\_map, xml\_element.

**Local steps**

- Set title\_column from column\_map.get(“title”).
- Set code\_column from column\_map at “code”.
- Set description\_column from column\_map.get(“description”).
- Set self.common\_code from get\_simple\_value(xml\_element, code\_column).text.
- If title\_column.
  - Set simple\_value\_title from get\_simple\_value(xml\_element, title\_column).
  - Set self.title from simple\_value\_title.text when simple\_value\_title is distinct from no value, otherwise self.common\_code.
    - Value choice on simple\_value\_title is distinct from no value — true gives simple\_value\_title.text, false gives self.common\_code.
- If description\_column.
  - Set simple\_value\_descr from get\_simple\_value(xml\_element, description\_column).
  - Set self.description from simple\_value\_descr.text when simple\_value\_descr is distinct from no value, otherwise no value.
    - Value choice on simple\_value\_descr is distinct from no value — true gives simple\_value\_descr.text, false gives no value.
- Set self.additional\_data from etree.tostring(xml\_element, encoding = “unicode”, pretty\_print = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L125) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L41)

<a id="op-913164809a8614"></a>
### Simple hash

`operation_enterprise_edi_record_definitions_common_code_business_behavior_simple_hash`

**Inputs** input\_string, length = 6.

**Explicit results** hashlib.blake2b(input\_string.encode(), digest\_size = (length floor divide 2)).hexdigest().

**Local steps**

- Return hashlib.blake2b(input\_string.encode(), digest\_size = (length floor divide 2)).hexdigest().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L2027) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L130) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L46)

<a id="op-bfdc5af70dbe5d"></a>
### Import genericode

`operation_enterprise_edi_record_definitions_common_code_business_behavior_import_genericode`

**Inputs** code\_list, file\_name, column\_map, filters = no value.

**Record and data access** resolve a document from “File” via get\_doc.

**State and service calls** call save on common\_code.

**Explicit results** total\_elements.

**Local steps**

- Set file\_doc from Platform.get\_doc(“File”, file\_name).
- Evaluate file\_doc.check\_permission(“read”).
- Set root from parse\_genericode\_content(file\_doc.get\_content(encodings = tuple())).
- Set elements from get\_filtered\_rows(root, (filters or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set total\_elements from len(elements).
- For each tuple(i, xml\_element) in enumerate(elements, start = 1).
  - Set code from get\_row\_code(xml\_element, column\_map at “code”).
  - Set common\_code from get\_common\_code(code\_list, code).
  - Evaluate common\_code.from\_genericode(column\_map, xml\_element).
  - Evaluate common\_code.save().
  - Evaluate Platform.publish\_progress(((i ÷ total\_elements) × 100), title = translated “Importing Common Codes”).
- Return total\_elements.

**Values supplied outside this operation** effective access from file\_doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L161) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L128) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L44)

<a id="op-1d4bb8acaeb8a2"></a>
### Get row code

`operation_enterprise_binding_enterprise_edi_doctype_common_code_common_code_get_row_code`

**Inputs** xml\_element, code\_column.

**Declared result** str.

**Explicit results** code.

**Explicit failure paths** validation helper — translated “Row {0} has no value in the code column {1}”.format(row\_number, Platform.bold(code\_column)).

**Local steps**

- Set code from getattr(get\_simple\_value(xml\_element, code\_column), “text”, no value).
- If not code.
  - Set row\_number from (int(xml\_element.xpath(“count(preceding-sibling::Row)”)) + 1).
  - Call the validation error handler Platform.throw(translated “Row {0} has no value in the code column {1}”.format(row\_number, Platform.bold(code\_column))).
- Return code.

**Values supplied outside this operation** selected callable from getattr(get\_simple\_value(xml\_element, code\_column), “text”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1345) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L585)

<a id="op-3bae56b89ad557"></a>
### Get common code

`operation_enterprise_binding_enterprise_edi_doctype_common_code_common_code_get_common_code`

**Inputs** code\_list, code.

**Declared result** CommonCode.

**Record and data access** read “Common Code” via get\_all · resolve a document from “Common Code” via get\_doc.

**State and service calls** request new\_doc for “Common Code”.

**Explicit results** Platform.get\_doc(“Common Code”, name) · common\_code.

**Local steps**

- Set existing from Platform.get\_all(“Common Code”, mapping(“code\_list” → code\_list, “common\_code” → code), list(“name”, “common\_code”)).
- If name bound to next(generator of row.name for row drawn from existing where row.common\_code equals code, no value).
  - Draw row from existing, keep a combination only if (row.common\_code equals code).
  - Return Platform.get\_doc(“Common Code”, name).
- Set common\_code from Platform.new\_doc(“Common Code”).
- Set common\_code.code\_list from code\_list.
- Return common\_code.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1343) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L583)

<a id="op-4134f04e152308"></a>
### Get filtered rows

`operation_enterprise_binding_enterprise_edi_doctype_common_code_common_code_get_filtered_rows`

**Inputs** root, filters.

**Declared result** list.

**Explicit results** root.xpath(formatted text .//SimpleCodeList/Row{predicate}, expanded names variables).

**Local steps**

- Set tuple(conditions, variables) from tuple(list(), mapping()).
- For each tuple(i, tuple(column\_ref, value)) in enumerate(filters.items()).
  - Evaluate conditions.append(formatted text Value&#91;@ColumnRef=$column{i}&#93;/SimpleValue=$value{i}).
  - Evaluate variables.update(mapping(formatted text column{i} → column\_ref, formatted text value{i} → value)).
- Set predicate from ((“&#91;” + “ and ”.join(conditions)) + “&#93;”) when conditions, otherwise empty text.
  - Value choice on conditions — true gives ((“&#91;” + “ and ”.join(conditions)) + “&#93;”), false gives empty text.
- Return root.xpath(formatted text .//SimpleCodeList/Row{predicate}, expanded names variables).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1344) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L584)

<a id="op-301a0209cafd10"></a>
### Get simple value

`operation_enterprise_binding_enterprise_edi_doctype_common_code_common_code_get_simple_value`

**Inputs** xml\_element, column\_ref.

**Declared result** “etree.Element \| None”.

**Explicit results** values at 0 when values, otherwise no value.

**Local steps**

- Set values from xml\_element.xpath(“./Value&#91;@ColumnRef=$column&#93;/SimpleValue”, column = column\_ref).
- Return values at 0 when values, otherwise no value.
  - Value choice on values — true gives values at 0, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1346) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L586)

<a id="op-df31135e0ae15c"></a>
### On doctype update

`operation_enterprise_edi_record_definitions_common_code_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Common Code”.

**Local steps**

- Evaluate Platform.db.add\_index(“Common Code”, list(“code\_list”, “common\_code”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L2759) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L129) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L45)

## Record · Communication medium

[Record definition](../../../../data/record-types/communication_medium.json)

<a id="op-025dba90c45c62"></a>
### Communication Medium.validate

`operation_enterprise_binding_enterprise_communication_doctype_communication_medium_communication_medium_communicationmedium_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_timeslots().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate timeslots](operations-003.md#op-640c42d509c839).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L237) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L899) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L139)

<a id="op-640c42d509c839"></a>
### Communication Medium.validate timeslots

`operation_enterprise_binding_enterprise_communication_doctype_communication_medium_communication_medium_communicationmedium_validate_timeslots`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row {0}: To Time must be later than From Time. Split overnight slots by day.”.format(slot.idx).

**Local steps**

- For each slot in self.timeslots.
  - If to\_timedelta(slot.from\_time) ≥ to\_timedelta(slot.to\_time).
    - Call the validation error handler Platform.throw(translated “Row {0}: To Time must be later than From Time. Split overnight slots by day.”.format(slot.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L238) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L900) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L140)

## Record · Incoming call settings

[Record definition](../../../../data/record-types/incoming_call_settings.json)

<a id="op-8518c48285eaf1"></a>
### Incoming Call Settings.validate

`operation_enterprise_telephony_record_definitions_incoming_call_settings_business_behavior_incoming_call_settings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_call\_schedule\_timeslot(self.call\_handling\_schedule).
- Evaluate self.validate\_call\_schedule\_overlaps(self.call\_handling\_schedule).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate call schedule timeslot](operations-003.md#op-0fcb582387127e), [validate call schedule overlaps](operations-003.md#op-af53fb977f6bbb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L4582) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1336)

<a id="op-0fcb582387127e"></a>
### Incoming Call Settings.validate call schedule timeslot

`operation_enterprise_telephony_record_definitions_incoming_call_settings_business_behavior_incoming_call_settings_validate_call_schedule_timeslot`

**Inputs** self, schedule.

**Explicit failure paths** validation helper — text in the contract.join(errors).

**Local steps**

- Set errors from list().
- For each record in schedule.
  - Set from\_time from self.time\_to\_seconds(record.from\_time).
  - Set to\_time from self.time\_to\_seconds(record.to\_time).
  - If from\_time ≥ to\_time.
    - Evaluate errors.append(translated “Call Schedule Row {0}: To time slot should always be ahead of From time slot. Split overnight slots by day.”.format(record.idx)).
- If errors.
  - Call the validation error handler Platform.throw(text in the contract.join(errors)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [time to seconds](operations-003.md#op-fe26dac8ee4c46).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1338)

<a id="op-af53fb977f6bbb"></a>
### Incoming Call Settings.validate call schedule overlaps

`operation_enterprise_telephony_record_definitions_incoming_call_settings_business_behavior_incoming_call_settings_validate_call_schedule_overlaps`

**Inputs** self, schedule.

**Explicit failure paths** validation helper — translated “Please fix overlapping time slots for {0}.”.format(day).

**Local steps**

- Set week\_days from set(list of each.day\_of\_week for each drawn from schedule).
  - Draw each from schedule.
- For each day in week\_days.
  - Set timeslots from list of tuple(record.from\_time, record.to\_time) for record drawn from schedule where record.day\_of\_week equals day.
    - Draw record from schedule, keep a combination only if (record.day\_of\_week equals day).
  - Set timeslots from sorted(map(deferred anonymous expression, timeslots)).
  - If len(timeslots) &lt; 2.
    - Continue with the next iteration or loop test.
  - For each i in range(1, len(timeslots)).
    - If self.check\_timeslots\_overlap(timeslots at (i − 1), timeslots at i).
      - Call the validation error handler Platform.throw(translated “Please fix overlapping time slots for {0}.”.format(day)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check timeslots overlap](operations-003.md#op-bf3509862ea695).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L4944) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1337)

<a id="op-bf3509862ea695"></a>
### Incoming Call Settings.check timeslots overlap

`operation_enterprise_telephony_record_definitions_incoming_call_settings_business_behavior_incoming_call_settings_check_timeslots_overlap`

**Inputs** ts1, ts2.

**Wrappers, in declaration order** staticmethod.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- If ((ts1 at 0 &lt; ts2 at 0 and ts1 at 1 ≤ ts2 at 0) or (ts1 at 0 ≥ ts2 at 1 and ts1 at 1 &gt; ts2 at 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (ts1 at 0 &lt; ts2 at 0 and ts1 at 1 ≤ ts2 at 0) → (ts1 at 0 ≥ ts2 at 1 and ts1 at 1 &gt; ts2 at 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ts1 at 0 &lt; ts2 at 0 → ts1 at 1 ≤ ts2 at 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ts1 at 0 ≥ ts2 at 1 → ts1 at 1 &gt; ts2 at 1.
  - Return false.
- Return true.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0976.json#L5391) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1334)

<a id="op-fe26dac8ee4c46"></a>
### Incoming Call Settings.time to seconds

`operation_enterprise_telephony_record_definitions_incoming_call_settings_business_behavior_incoming_call_settings_time_to_seconds`

**Inputs** time.

**Wrappers, in declaration order** staticmethod.

**Declared result** timedelta.

**Explicit results** to\_timedelta(time).

**Local steps**

- Return to\_timedelta(time).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1335)

## Record · Plaid settings

[Record definition](../../../../data/record-types/plaid_settings.json)

<a id="op-022da244d20318"></a>
### Plaid Connector.initialize

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_plaid_connector_business_behavior_plaid_connector_initialize`

**Inputs** self, access\_token = no value.

**Record and data access** read “Plaid Settings” via get\_single.

**Local steps**

- Set self.access\_token from access\_token.
- Set self.settings from Platform.get\_single(“Plaid Settings”).
- Set self.products from list(“transactions”).
- Set self.client\_name from Platform.local.site.
- Set self.client from plaid.Client(client\_id = self.settings.plaid\_client\_id, secret = self.settings.get\_password(“plaid\_secret”), environment = self.settings.plaid\_env, api\_version = “2020-09-14”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L2837) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L149) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L65)

<a id="op-b650145286a7e5"></a>
### Plaid Connector.get access token

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_plaid_connector_business_behavior_plaid_connector_get_access_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, public\_token.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** diagnostic or audit logging.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L3086) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L61)

<a id="op-8315923e358969"></a>
### Plaid Connector.get token request

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_plaid_connector_business_behavior_plaid_connector_get_token_request`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, update\_mode.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L3241) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L147) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L63)

<a id="op-1f65e41ae1c949"></a>
### Plaid Connector.get link token

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_plaid_connector_business_behavior_plaid_connector_get_link_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, update\_mode.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** diagnostic or audit logging, validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 2 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L3665) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L146) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L62)

<a id="op-0e746558131748"></a>
### Plaid Connector.get transactions

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_plaid_connector_business_behavior_plaid_connector_get_transactions`

**Inputs** self, start\_date, end\_date, account\_id = no value.

**Explicit results** transactions.

**Explicit failure paths** e.

**Local steps**

- Set kwargs from dict(access\_token = self.access\_token, start\_date = start\_date, end\_date = end\_date).
- If account\_id.
  - Evaluate kwargs.update(dict(account\_ids = list(account\_id))).
- Attempt the following.
  - Set response from self.client.Transactions.get(expanded names kwargs).
  - Set transactions from response at “transactions”.
  - While len(transactions) &lt; response at “total\_transactions”.
    - Set response from self.client.Transactions.get(expanded names kwargs, offset = len(transactions)).
    - If not response at “transactions”.
      - Leave the innermost loop without its normal-exhaustion alternative.
    - Evaluate transactions.extend(response at “transactions”).
  - Return transactions.
- On failure (ItemError) bound to e.
  - Raise e.
- On failure (Exception).
  - Evaluate Platform.log\_error(“Plaid: Transactions sync error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L148) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L64)

<a id="op-095f655e46d4f8"></a>
### Plaid Settings.get link token

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_plaid_settings_get_link_token`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0446.json#L4423) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L142) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L58)

<a id="op-5f5ac5ea835315"></a>
### Get plaid configuration

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_get_plaid_configuration`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Plaid Settings” via get\_single\_value · read “Plaid Settings” via get\_single.

**Explicit results** mapping(“plaid\_env” → plaid\_settings.plaid\_env, “link\_token” → plaid\_settings.get\_link\_token(), “client\_name” → Platform.local.site) · “disabled”.

**Local steps**

- Evaluate Platform.has\_permission(“Plaid Settings”, throw = true).
- If Platform.db.get\_single\_value(“Plaid Settings”, “enabled”).
  - Set plaid\_settings from Platform.get\_single(“Plaid Settings”).
  - Return mapping(“plaid\_env” → plaid\_settings.plaid\_env, “link\_token” → plaid\_settings.get\_link\_token(), “client\_name” → Platform.local.site).
- Return “disabled”.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Plaid Settings”, throw = true) · configured or stored value from Platform.db.get\_single\_value(“Plaid Settings”, “enabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L55)

<a id="op-9bae4fa8e8d8d1"></a>
### Add institution

`operation_enterprise_enterprise_application_integrations_record_definitions_plaid_settings_business_behavior_add_institution`

**Inputs** token, response.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Bank” via exists · resolve a document from mapping(“doctype” → “Bank”, “bank\_name” → response at “institution” at “name”, “plaid\_access\_token” → access\_token) via get\_doc · resolve a document from “Bank” via get\_doc.

**State and service calls** call insert on bank · call save on bank.

**Explicit results** bank.

**Local steps**

- Evaluate Platform.has\_permission(“Plaid Settings”, throw = true).
- Set response from Platform.parse\_json(response).
- Set plaid from PlaidConnector().
- Set access\_token from plaid.get\_access\_token(token).
- Set bank from no value.
- If not Platform.db.exists(“Bank”, response at “institution” at “name”).
  - Attempt the following.
    - Set bank from Platform.get\_doc(mapping(“doctype” → “Bank”, “bank\_name” → response at “institution” at “name”, “plaid\_access\_token” → access\_token)).
    - Evaluate bank.insert().
  - On failure (Exception).
    - Evaluate Platform.log\_error(“Plaid Link Error”).
- Otherwise.
  - Set bank from Platform.get\_doc(“Bank”, response at “institution” at “name”).
  - Set bank.plaid\_access\_token from access\_token.
  - Evaluate bank.save().
- Return bank.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Plaid Settings”, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L50)
