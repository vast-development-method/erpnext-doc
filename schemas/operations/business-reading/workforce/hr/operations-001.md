# Employment and attendance · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Appointment letter

[Record definition](../../../../data/record-types/appointment_letter.json)

<a id="op-b4c0e9bcfac5b9"></a>
### Appointment Letter.before insert

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_before_insert`

**Inputs** self.

**Local steps**

- If not self.shift\_type.
  - Evaluate self.set\_shift\_from\_employee().
- If not self.letter\_body.
  - Set self.appointment\_letter\_template from (self.appointment\_letter\_template or get\_default\_template()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.appointment\_letter\_template → get\_default\_template().
  - Set self.letter\_body from self.get\_template\_body().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set shift from employee](operations-001.md#op-08f59623848c59), [get template body](operations-001.md#op-be8fbcb9b34e6e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L10) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L61) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L61)

<a id="op-b8be74ff790132"></a>
### Appointment Letter.validate

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_validate`

**Inputs** self.

**Local steps**

- If not self.working\_hours.
  - Set self.working\_hours from get\_working\_hours(self.start\_time, self.end\_time).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L17) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L68) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L68)

<a id="op-be8fbcb9b34e6e"></a>
### Appointment Letter.get template body

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_get_template_body`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Appointment Letter Template” via get\_value.

**Explicit results** Platform.db.get\_value(“Appointment Letter Template”, self.appointment\_letter\_template, “letter\_body”).

**Local steps**

- If self.appointment\_letter\_template.
  - Return Platform.db.get\_value(“Appointment Letter Template”, self.appointment\_letter\_template, “letter\_body”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L15) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L66) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L66)

<a id="op-08f59623848c59"></a>
### Appointment Letter.set shift from employee

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_set_shift_from_employee`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Shift Type” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not self.employee.
  - Return no value.
- Set shift\_type from get\_shift\_type\_on(self.employee, getdate(self.appointment\_date)).
- If shift\_type.
  - Set self.shift\_type from shift\_type.
  - Set tuple(self.start\_time, self.end\_time) from Platform.get\_cached\_value(“Shift Type”, shift\_type, list(“start\_time”, “end\_time”)).
  - Set self.working\_hours from get\_working\_hours(self.start\_time, self.end\_time).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Shift Type”, shift\_type, list(“start\_time”, “end\_time”)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L16) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L67) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L67)

<a id="op-e3dd6b31c16b3f"></a>
### Appointment Letter.before print

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_before_print`

**Inputs** self, settings = no value.

**Local steps**

- Set self.letter\_body from self.get\_letter\_body\_html().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get letter body html](operations-001.md#op-802c6eeae6660f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L11) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L62) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L62)

<a id="op-802c6eeae6660f"></a>
### Appointment Letter.get letter body html

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_get_letter_body_html`

**Inputs** self.

**Declared result** str.

**Explicit results** body.

**Local steps**

- Set body from (self.letter\_body or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.letter\_body → empty text.
- For each tuple(key, value) in self.get\_placeholders().items().
  - Set text from escape\_html(cstr(value)).
  - Set body from body.replace(((“{{ ” + key) + “ }}”), text).replace(((“{{” + key) + “}}”), text).
- Return body.

**Methods declared on this owner** [get placeholders](operations-001.md#op-245ba69cd5ff96).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L13) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L64) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L64)

<a id="op-245ba69cd5ff96"></a>
### Appointment Letter.get placeholders

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_get_placeholders`

**Inputs** self.

**Declared result** dict.

**Record and data access** resolve a document from “Job Offer” via get\_cached\_doc · read “HR Settings” via get\_single\_value.

**Explicit results** mapping of key → empty text when value is identical to no value, otherwise value for tuple(key, value) drawn from placeholders.items().

**Local steps**

- Set offer from Platform.get\_cached\_doc(“Job Offer”, self.job\_offer) when self.job\_offer, otherwise Platform.\_dict().
  - Value choice on self.job\_offer — true gives Platform.get\_cached\_doc(“Job Offer”, self.job\_offer), false gives Platform.\_dict().
- Set placeholders from mapping(expand self.get\_field\_placeholders(), “applicant\_name” → self.applicant\_name, “company” → self.company, “employee” → self.employee, …).
  - Value choice on offer.ctc — true gives fmt\_money(offer.ctc, currency = offer.currency), false gives empty text.
  - Value choice on offer.variable — true gives fmt\_money(offer.variable, currency = offer.currency), false gives empty text.
  - Value choice on self.start\_time — true gives format\_time(self.start\_time, “h:mm a”), false gives empty text.
  - Value choice on self.end\_time — true gives format\_time(self.end\_time, “h:mm a”), false gives empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.working\_hours → offer.working\_hours.
  - Draw row from (offer.get(“leave\_allocations”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in offer.get(“leave\_allocations”) → list().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“HR Settings”, “retirement\_age”)) → empty text.
- Return mapping of key → empty text when value is identical to no value, otherwise value for tuple(key, value) drawn from placeholders.items().
  - Draw tuple(key, value) from placeholders.items().
  - Value choice on value is identical to no value — true gives empty text, false gives value.

**Methods declared on this owner** [get field placeholders](operations-001.md#op-fa843fa3d5678a).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Job Offer”, self.job\_offer), Platform.db.get\_single\_value(“HR Settings”, “retirement\_age”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L14) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L65) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L65)

<a id="op-fa843fa3d5678a"></a>
### Appointment Letter.get field placeholders

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_appointmentletter_get_field_placeholders`

**Inputs** self.

**Declared result** dict.

**Explicit results** mapping of formatted text doc.{df.fieldname} → self.get\_formatted(df.fieldname) for df drawn from self.meta.fields where (df.fieldtype does not belong to tuple(expanded no\_value\_fields, “Password”) and df. ….

**Local steps**

- Return mapping of formatted text doc.{df.fieldname} → self.get\_formatted(df.fieldname) for df drawn from self.meta.fields where (df.fieldtype does not belong to tuple(expanded no\_value\_fields, “Password”) and df. ….
  - Draw df from self.meta.fields, keep a combination only if ((df.fieldtype does not belong to tuple(expanded no\_value\_fields, “Password”) and df.fieldname differs from “letter\_body”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldtype does not belong to tuple(expanded no\_value\_fields, “Password”) → df.fieldname differs from “letter\_body”.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L12) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L63) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L63)

<a id="op-388731f4ee0a46"></a>
### Get shift type on

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_get_shift_type_on`

**Inputs** employee, date.

**Declared result** (str bitwise or no value).

**Record and data access** read “Shift Assignment” via get\_all · read “Employee” via get\_value.

**Explicit results** assignment at 0 when assignment, otherwise Platform.db.get\_value(“Employee”, employee, “default\_shift”).

**Local steps**

- Set assignment from Platform.get\_all(“Shift Assignment”, filters = mapping(“employee” → employee, “docstatus” → 1, “status” → “Active”, “start\_date” → tuple(“&lt;=”, date)), or\_filters = list(list(“end\_date”, “is”, “not set”), l ….
- Return assignment at 0 when assignment, otherwise Platform.db.get\_value(“Employee”, employee, “default\_shift”).
  - Value choice on assignment — true gives assignment at 0, false gives Platform.db.get\_value(“Employee”, employee, “default\_shift”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L22) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L73) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L73)

<a id="op-8bd37c49976f58"></a>
### Get working hours

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_get_working_hours`

**Inputs** start\_time, end\_time.

**Declared result** float.

**Explicit results** 0 · flt((seconds ÷ 3600), 2).

**Local steps**

- If not (start\_time and end\_time).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in start\_time → end\_time.
  - Return 0.
- Set seconds from ((to\_timedelta(end\_time) − to\_timedelta(start\_time)).total\_seconds() modulo or format 86400).
- Return flt((seconds ÷ 3600), 2).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L25) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L76) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L76)

<a id="op-a0859253a5e2ac"></a>
### Get title

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_get_title`

**Inputs** doctype, name, title\_field.

**Declared result** (str bitwise or no value).

**Record and data access** read doctype via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(doctype, name, title\_field) when name, otherwise no value.

**Local steps**

- Return Platform.get\_cached\_value(doctype, name, title\_field) when name, otherwise no value.
  - Value choice on name — true gives Platform.get\_cached\_value(doctype, name, title\_field), false gives no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(doctype, name, title\_field).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L23) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L74) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L74)

<a id="op-8ac7d9a9a3dc06"></a>
### Format date

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_format_date`

**Inputs** date.

**Declared result** str.

**Explicit results** global\_date\_format(date, “long”) when date, otherwise empty text.

**Local steps**

- Return global\_date\_format(date, “long”) when date, otherwise empty text.
  - Value choice on date — true gives global\_date\_format(date, “long”), false gives empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L18) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L69) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L69)

<a id="op-bde49330bf2549"></a>
### Format number

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_format_number`

**Inputs** value.

**Declared result** str.

**Explicit results** formatted text {flt(value)} when value, otherwise empty text.

**Local steps**

- Return formatted text {flt(value)} when value, otherwise empty text.
  - Value choice on value — true gives formatted text {flt(value)}, false gives empty text.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L20) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L71) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L71)

<a id="op-8d7188893ebd70"></a>
### Format days

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_format_days`

**Inputs** days.

**Declared result** str.

**Explicit results** empty text · translated “{0} ({1}) days”.format(in\_words(days), days) when days &gt; 1, otherwise translated “one (1) day”.

**Local steps**

- If not days.
  - Return empty text.
- Return translated “{0} ({1}) days”.format(in\_words(days), days) when days &gt; 1, otherwise translated “one (1) day”.
  - Value choice on days &gt; 1 — true gives translated “{0} ({1}) days”.format(in\_words(days), days), false gives translated “one (1) day”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L19) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L70) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L70)

<a id="op-960ac724d79ba0"></a>
### Format probation

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_format_probation`

**Inputs** days.

**Declared result** str.

**Explicit results** format\_days(days) · translated “{0} ({1}) months”.format(in\_words(months), months) when months &gt; 1, otherwise translated “one (1) month”.

**Local steps**

- If (not days or (days modulo or format 30)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not days → (days modulo or format 30).
  - Return format\_days(days).
- Set months from (days floor divide 30).
- Return translated “{0} ({1}) months”.format(in\_words(months), months) when months &gt; 1, otherwise translated “one (1) month”.
  - Value choice on months &gt; 1 — true gives translated “{0} ({1}) months”.format(in\_words(months), months), false gives translated “one (1) month”.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L21) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L72) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L72)

<a id="op-a3f76d8a400cdf"></a>
### Split days

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_split_days`

**Inputs** days.

**Declared result** list at str.

**Explicit results** list of day.strip() for day drawn from (days or empty text).split(“,”) where day.strip().

**Local steps**

- Return list of day.strip() for day drawn from (days or empty text).split(“,”) where day.strip().
  - Draw day from (days or empty text).split(“,”), keep a combination only if (day.strip()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in days → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L26) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L77) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L77)

<a id="op-357fdaa808afb3"></a>
### Get working days

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_appointment_letter_get_working_days`

**Inputs** weekly\_off\_days.

**Declared result** str.

**Explicit results** empty text · translated “{0} to {1}”.format(translated working\_days at 0, translated working\_days at negative 1) · comma\_and(list of translated day for day drawn from working\_days, add\_quotes = false).

**Local steps**

- Set off\_days from split\_days(weekly\_off\_days).
- If not off\_days.
  - Return empty text.
- Set week from list(calendar.day\_name).
- Set working\_days from list of day for day drawn from week where day does not belong to off\_days.
  - Draw day from week, keep a combination only if (day does not belong to off\_days).
- Set positions from list of week.index(day) for day drawn from working\_days.
  - Draw day from working\_days.
- If (len(working\_days) &gt; 2 and positions equals list(range(positions at 0, (positions at negative nested operand in the contract + 1)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(working\_days) &gt; 2 → positions equals list(range(positions at 0, (positions at negative 1 + 1))).
  - Return translated “{0} to {1}”.format(translated working\_days at 0, translated working\_days at negative 1).
- Return comma\_and(list of translated day for day drawn from working\_days, add\_quotes = false).
  - Draw day from working\_days.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L24) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L75) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L75)

## Record · Appointment letter template

[Record definition](../../../../data/record-types/appointment_letter_template.json)

<a id="op-7f00d5a729ee57"></a>
### Appointment Letter Template.on update

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_template_appointment_letter_template_appointmentlettertemplate_on_update`

**Inputs** self.

**State and service calls** request set\_value on “Appointment Letter Template”.

**Local steps**

- If self.is\_default.
  - Evaluate Platform.db.set\_value(“Appointment Letter Template”, mapping(“name” → tuple(“!=”, self.name), “is\_default” → 1), “is\_default”, 0, update\_modified = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L27) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L78) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L78)

<a id="op-9af02da20fa8b2"></a>
### Get default letter body

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_template_appointment_letter_template_get_default_letter_body`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** formatted text &lt;div class="ql-editor read-mode"&gt;{body}&lt;/div&gt;.

**Local steps**

- Set path from Platform.get\_app\_path(“Workforce”, “hr”, “doctype”, “appointment\_letter\_template”, …).
- Set body from empty text.join(generator of line.strip() for line drawn from Platform.read\_file(path).splitlines()).
  - Draw line from Platform.read\_file(path).splitlines().
- Return formatted text &lt;div class="ql-editor read-mode"&gt;{body}&lt;/div&gt;.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L29) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L80) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L80)

<a id="op-d3b642243652ad"></a>
### Get default template

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_template_appointment_letter_template_get_default_template`

**Inputs** no declared parameters.

**Declared result** (str bitwise or no value).

**Record and data access** read “Appointment Letter Template” via get\_value.

**Explicit results** Platform.db.get\_value(“Appointment Letter Template”, mapping(“is\_default” → 1)).

**Local steps**

- Return Platform.db.get\_value(“Appointment Letter Template”, mapping(“is\_default” → 1)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L30) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L81) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L81)

<a id="op-3c08f2e84b558a"></a>
### Create default template

`operation_workforce_binding_workforce_hr_doctype_appointment_letter_template_appointment_letter_template_create_default_template`

**Inputs** no declared parameters.

**Declared result** no value.

**Record and data access** read “Appointment Letter Template” via exists · resolve a document from mapping(“doctype” → “Appointment Letter Template”, “template\_name” → template\_name, “is\_default” → 1, “letter\_body” → get\_default\_letter\_body()) via get\_doc.

**State and service calls** request set\_value on “Appointment Letter Template” · call insert on Platform.get\_doc(mapping(“doctype” → “Appointment Letter Template”, “template\_name” → template\_name, “is\_default” → 1, “letter\_body” → get\_default\_letter\_body())).

**Explicit results** no value.

**Local steps**

- If get\_default\_template().
  - Return no value.
- Set template\_name from translated “Standard Appointment Letter”.
- If Platform.db.exists(“Appointment Letter Template”, template\_name).
  - Evaluate Platform.db.set\_value(“Appointment Letter Template”, template\_name, “is\_default”, 1).
  - Return no value.
- Evaluate Platform.get\_doc(mapping(“doctype” → “Appointment Letter Template”, “template\_name” → template\_name, “is\_default” → 1, “letter\_body” → get\_default\_letter\_body())).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L28) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L79) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L79)

## Record · Appraisal

[Record definition](../../../../data/record-types/appraisal.json)

<a id="op-edadb4a5a3cb89"></a>
### Appraisal.validate

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_validate`

**Inputs** self.

**Local steps**

- Evaluate self.set\_kra\_evaluation\_method().
- Evaluate validate\_active\_employee(self.employee).
- Evaluate validate\_active\_appraisal\_cycle(self.appraisal\_cycle).
- Evaluate self.validate\_duplicate().
- Evaluate self.validate\_total\_weightage(“appraisal\_kra”, “KRAs”).
- Evaluate self.validate\_total\_weightage(“self\_ratings”, “Self Ratings”).
- Evaluate self.set\_goal\_score().
- Evaluate self.calculate\_self\_appraisal\_score().
- Evaluate self.calculate\_avg\_feedback\_score().
- Evaluate self.calculate\_final\_score().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set kra evaluation method](operations-001.md#op-0bf8623cdff1fd), [validate duplicate](operations-001.md#op-b9cc2f7acb6a07), [set goal score](operations-002.md#op-22592bc36b7639), [calculate self appraisal score](operations-002.md#op-b7e4271f622c54), [calculate avg feedback score](operations-002.md#op-53fb826f66ff2d), [calculate final score](operations-002.md#op-70355f2163bdaa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L3089) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L321) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L318)

<a id="op-b9cc2f7acb6a07"></a>
### Appraisal.validate duplicate

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_validate_duplicate`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “Appraisal {0} already exists for Employee {1} for this Appraisal Cycle or overlapping period”.format(get\_link\_to\_form(“Appraisal”, duplicate), Platform.bold(self.employee\_name)).

**Local steps**

- Set Appraisal from Platform.qb.DocType(“Appraisal”).
- Set duplicate from nested operand in the contract(nested operand in the contract).select(Appraisal.name).where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contrac ….run().
- Set duplicate from duplicate at 0 at 0 when duplicate, otherwise 0.
  - Value choice on duplicate — true gives duplicate at 0 at 0, false gives 0.
- If duplicate.
  - Call the validation error handler Platform.throw(translated “Appraisal {0} already exists for Employee {1} for this Appraisal Cycle or overlapping period”.format(get\_link\_to\_form(“Appraisal”, duplicate), Platform.bold(self.employee\_name)), ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L3354) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L322) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L319)

<a id="op-0bf8623cdff1fd"></a>
### Appraisal.set kra evaluation method

`operation_workforce_human_resources_record_definitions_appraisal_business_behavior_appraisal_set_key_result_area_evaluation_method`

**Inputs** self.

**Record and data access** read “Appraisal Cycle” via get\_value.

**Local steps**

- If (self.is\_new() and self.appraisal\_cycle and Platform.db.get\_value(“Appraisal Cycle”, self.appraisal\_cycle, “kra\_evaluation\_method”) equals “Manual Rating”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.appraisal\_cycle → Platform.db.get\_value(“Appraisal Cycle”, self.appraisal\_cycle, “kra\_evaluation\_method”) equals “Manual Rating”.
  - Set self.rate\_goals\_manually from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0006.json#L3992) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L319) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L316)
