# Supporting services · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Index

<a id="op-a9e588c81f7d4b"></a>
### Filter timeslots

`operation_enterprise_public_pages_book_appointment_index_business_behavior_filter_timeslots`

**Inputs** date, timeslots.

**Explicit results** filtered\_timeslots.

**Local steps**

- Set filtered\_timeslots from list().
- For each timeslot in timeslots.
  - If timeslot at “time”.date() equals date.
    - Evaluate filtered\_timeslots.append(timeslot).
- Return filtered\_timeslots.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L5453) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1462) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L890)

<a id="op-56d0f5e3dc4bb2"></a>
### Convert to guest timezone

`operation_enterprise_public_pages_book_appointment_index_business_behavior_convert_to_guest_timezone`

**Inputs** guest\_tz, datetimeobject.

**Explicit results** datetimeobject.

**Local steps**

- Set guest\_tz from zoneinfo.ZoneInfo(guest\_tz).
- Set local\_timezone from zoneinfo.ZoneInfo(get\_system\_timezone()).
- Set datetimeobject from datetimeobject.replace(tzinfo = local\_timezone).
- Set datetimeobject from datetimeobject.astimezone(guest\_tz).
- Return datetimeobject.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L5594) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1457) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L885)

<a id="op-a40495bb4e9afb"></a>
### Convert to system timezone

`operation_enterprise_public_pages_book_appointment_index_business_behavior_convert_to_system_timezone`

**Inputs** guest\_tz, datetimeobject.

**Explicit results** datetimeobject.

**Local steps**

- Set guest\_tz from zoneinfo.ZoneInfo(guest\_tz).
- Set datetimeobject from datetimeobject.replace(tzinfo = guest\_tz).
- Set system\_tz from zoneinfo.ZoneInfo(get\_system\_timezone()).
- Set datetimeobject from datetimeobject.astimezone(system\_tz).
- Return datetimeobject.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L5769) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1458) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L886)

<a id="op-cc5e4c0fa1a18e"></a>
### Get booked slot times for

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_booked_slot_times_for`

**Inputs** timeslots, appointment\_duration.

**Explicit results** list() · get\_booked\_slot\_times((min(timeslots) − duration), (max(timeslots) + duration)).

**Local steps**

- If not timeslots.
  - Return list().
- Bind dependencies get\_booked\_slot\_times.
- Set duration from datetime.timedelta(minutes = appointment\_duration).
- Return get\_booked\_slot\_times((min(timeslots) − duration), (max(timeslots) + duration)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L5944) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L894)

<a id="op-32a62c7b7e17d9"></a>
### Is slot available

`operation_enterprise_public_pages_book_appointment_index_business_behavior_is_slot_available`

**Inputs** timeslot, booked\_times, settings.

**Explicit results** true · overlapping &lt; settings.number\_of\_agents.

**Local steps**

- If not cint(settings.number\_of\_agents).
  - Return true.
- Set duration from datetime.timedelta(minutes = settings.appointment\_duration).
- Set tuple(lower, upper) from tuple((timeslot − duration), (timeslot + duration)).
- Set overlapping from sum(generator of 1 for booked drawn from booked\_times where lower &lt; booked &lt; upper).
  - Draw booked from booked\_times, keep a combination only if (lower &lt; booked &lt; upper).
  - Compare adjacent operands in order, stopping at the first false comparison in lower &lt; booked &lt; upper.
- Return overlapping &lt; settings.number\_of\_agents.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L900)

<a id="op-b71cf9efdf77d7"></a>
### Is holiday

`operation_enterprise_public_pages_book_appointment_index_business_behavior_is_holiday`

**Inputs** date, holiday\_list.

**Explicit results** any(generator of (h.holiday\_date equals date and not h.is\_half\_day) for h drawn from holiday\_list.holidays).

**Local steps**

- Return any(generator of (h.holiday\_date equals date and not h.is\_half\_day) for h drawn from holiday\_list.holidays).
  - Draw h from holiday\_list.holidays.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in h.holiday\_date equals date → not h.is\_half\_day.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L146) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L899)

<a id="op-8a02f0e478f9e3"></a>
### Get records

`operation_enterprise_public_pages_book_appointment_index_business_behavior_get_records`

**Inputs** start\_time, end\_time, settings.

**Explicit results** records.

**Local steps**

- Set records from list().
- For each record in settings.availability\_of\_slots.
  - If (record.day\_of\_week equals WEEKDAYS at start\_time.weekday() or record.day\_of\_week equals WEEKDAYS at end\_time.weekday()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in record.day\_of\_week equals WEEKDAYS at start\_time.weekday() → record.day\_of\_week equals WEEKDAYS at end\_time.weekday().
    - Evaluate records.append(record).
- Return records.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L6426) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L896)

<a id="op-f95b23ecf1b382"></a>
### Deltatime to datetime

`operation_enterprise_public_pages_book_appointment_index_business_behavior_deltatime_to_datetime`

**Inputs** date, deltatime.

**Explicit results** datetime.datetime.combine(date.date(), time).

**Local steps**

- Set time from (datetime.datetime.min + deltatime).time().
- Return datetime.datetime.combine(date.date(), time).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L6621) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1461) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L889)

<a id="op-666974c3860335"></a>
### Datetime to deltatime

`operation_enterprise_public_pages_book_appointment_index_business_behavior_datetime_to_deltatime`

**Inputs** date\_time.

**Explicit results** (date\_time − midnight).

**Local steps**

- Set midnight from datetime.datetime.combine(date\_time.date(), datetime.time.min).
- Return (date\_time − midnight).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0993.json#L6741) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1460) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L888)

<a id="op-0ccadf9949cc84"></a>
### Get context

`operation_enterprise_public_pages_book_appointment_verify_index_business_behavior_get_context`

**Inputs** context.

**Record and data access** read “Appointment” via get\_value · resolve a document from “Appointment” via get\_doc.

**Explicit results** context.

**Local steps**

- Set key from Platform.form\_dict.get(“key”).
- If not key.
  - Set context.success from false.
  - Return context.
- Set appointment\_name from Platform.db.get\_value(“Appointment”, mapping(“verification\_token” → sha256\_hash(key)), “name”).
- If not appointment\_name.
  - Set context.success from false.
  - Set context.message from translated “This verification link is invalid. Please book the appointment again.”.
  - Return context.
- Set appointment from Platform.get\_doc(“Appointment”, appointment\_name).
- If appointment.status equals “Closed”.
  - Set context.success from false.
  - Set context.message from translated “Appointment has been closed. Please book the appointment again.”.
  - Return context.
- If appointment.status equals “Open”.
  - Set context.success from true.
  - Set context.message from translated “Appointment is already verified.”.
  - Return context.
- If now\_datetime() &gt; add\_to\_date(appointment.creation, minutes = get\_verification\_link\_expiry()).
  - Set context.success from false.
  - Set context.message from translated “Verification link has expired.”.
  - Return context.
- If get\_datetime(appointment.scheduled\_time) &lt; now\_datetime().
  - Set context.success from false.
  - Set context.message from translated “The appointment time has passed. Please book the appointment again.”.
  - Return context.
- Attempt the following.
  - Evaluate verify\_appointment(appointment).
- On failure (Platform.ValidationError) bound to e.
  - Evaluate Platform.clear\_last\_message().
  - Set context.success from false.
  - Set context.message from str(e).
  - Return context.
- Set Platform.local.flags.commit from true.
- Set context.success from true.
- Return context.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L148) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L901)

<a id="op-fb87230e788ec4"></a>
### Verify appointment

`operation_enterprise_public_pages_book_appointment_verify_index_business_behavior_verify_appointment`

**Inputs** appointment.

**State and service calls** call save on appointment.

**Local steps**

- Set appointment.email\_verified from true.
- Set appointment.status from “Open”.
- Evaluate appointment.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L902)

<a id="op-338a59ea32af02"></a>
### Get context

`operation_enterprise_public_pages_support_index_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “Support Settings” via get\_doc · read “Help Article” via get\_all.

**Local steps**

- Set context.no\_cache from 1.
- Set context.align\_greeting from empty text.
- Set setting from Platform.get\_doc(“Support Settings”).
- Set context.greeting\_title from setting.greeting\_title.
- Set context.greeting\_subtitle from setting.greeting\_subtitle.
- Set favorite\_articles from get\_favorite\_articles\_by\_page\_view().
- If len(favorite\_articles) &lt; 6.
  - Set name\_list from list().
  - If favorite\_articles.
    - For each article in favorite\_articles.
      - Evaluate name\_list.append(article.name).
  - For each record in Platform.get\_all(“Help Article”, fields = list(“title”, “content”, “route”, “category”), filters = mapping(“name” → list(“not in”, tuple(name\_list)), “published” → 1), order\_by = “creation desc”, limit = ( ….
    - Evaluate favorite\_articles.append(record).
- Set context.favorite\_article\_list from get\_favorite\_articles(favorite\_articles).
- Set context.help\_article\_list from get\_help\_article\_list().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L394) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L905)

<a id="op-d130b94e0df7f0"></a>
### Get favorite articles by page view

`operation_enterprise_public_pages_support_index_business_behavior_get_favorite_articles_by_page_view`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Help Article, Web Page View).

**Explicit results** Platform.db.sql(query text (SELECT, Help Article, Web Page View), as\_dict = true).

**Local steps**

- Return Platform.db.sql(query text (SELECT, Help Article, Web Page View), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L907)

<a id="op-09522a1a9d374d"></a>
### Get favorite articles

`operation_enterprise_public_pages_support_index_business_behavior_get_favorite_articles`

**Inputs** favorite\_articles.

**Explicit results** favorite\_article\_list.

**Local steps**

- Set favorite\_article\_list from list().
- For each article in favorite\_articles.
  - Set description from Platform.utils.strip\_html(article.content).
  - If len(description) &gt; 120.
    - Set description from (description at slice no value to 120 + “...”).
  - Set favorite\_article\_dict from mapping(“title” → article.title, “description” → description, “route” → article.route, “category” → article.category).
  - Evaluate favorite\_article\_list.append(favorite\_article\_dict).
- Return favorite\_article\_list.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L1459) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L906)

<a id="op-91c527013ce7c3"></a>
### Get help article list

`operation_enterprise_public_pages_support_index_business_behavior_get_help_article_list`

**Inputs** no declared parameters.

**Record and data access** read “Help Category” via get\_all · read “Help Article” via get\_all.

**Explicit results** help\_article\_list.

**Local steps**

- Set help\_article\_list from list().
- Set category\_list from Platform.get\_all(“Help Category”, fields = “name”).
- For each category in category\_list.
  - Set help\_articles from Platform.get\_all(“Help Article”, fields = “\*”, filters = mapping(“category” → category.name, “published” → 1), order\_by = “creation desc”, limit = 5).
  - If help\_articles.
    - Set help\_aricles\_per\_caetgory from mapping(“category” → category, “articles” → help\_articles).
    - Evaluate help\_article\_list.append(help\_aricles\_per\_caetgory).
- Return help\_article\_list.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0994.json#L1749) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L908)

## Service · Lines from txt file

<a id="op-6f5e545f959b9f"></a>
### Extract

`operation_enterprise_gettext_extractors_lines_from_text_resource_file_business_behavior_extract`

**Inputs** fileobj, remaining positional values args, remaining named values kwargs.

**Local steps**

- For each tuple(line\_no, line) in enumerate(fileobj.readlines()).
  - yield tuple((line\_no + 1), “\_”, line.decode().strip(), list()).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0447.json#L6633) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L159) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L72)

## Service · Material request info

<a id="op-df2bc9ba04eea3"></a>
### Get context

`operation_enterprise_templates_pages_material_request_info_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from Platform.form\_dict.doctype via get\_doc · read “Property Setter” via get\_value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set context.no\_cache from 1.
- Set context.show\_sidebar from true.
- Set context.doc from Platform.get\_doc(Platform.form\_dict.doctype, Platform.form\_dict.name).
- If hasattr(context.doc, “set\_indicator”).
  - Evaluate context.doc.set\_indicator().
- Set context.parents from Platform.form\_dict.parents.
- Set context.title from Platform.form\_dict.name.
- If not (context.doc.has\_permission(“read”) or Platform.has\_website\_permission(context.doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.doc.has\_permission(“read”) → Platform.has\_website\_permission(context.doc).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set default\_print\_format from Platform.db.get\_value(“Property Setter”, dict(property = “default\_print\_format”, doc\_type = Platform.form\_dict.doctype), “value”).
- If default\_print\_format.
  - Set context.print\_format from default\_print\_format.
- Otherwise.
  - Set context.print\_format from “Standard”.
- Set context.doc.items from get\_more\_items\_info(context.doc.items, context.doc.name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from context.doc.has\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1341)

<a id="op-437071627851d7"></a>
### Get more items info

`operation_enterprise_templates_pages_material_request_info_business_behavior_get_more_items_info`

**Inputs** items, material\_request.

**Record and data access** read “Item” via get\_value · execute query text (SELECT, Work) · execute query text (SELECT, Stock Entry Detail).

**Explicit results** items.

**Local steps**

- For each item in items.
  - Set item.customer\_provided from Platform.get\_value(“Item”, item.item\_code, “is\_customer\_provided\_item”).
  - Set item.work\_orders from Platform.db.sql(query text (SELECT, Work), item.item\_code, as\_dict = 1).
  - Set item.delivered\_qty from flt(Platform.db.sql(query text (SELECT, Stock Entry Detail), tuple(material\_request, item.item\_code)) at 0 at 0).
- Return items.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1342)

## Service · Naming

<a id="op-3413f7f8bbc7b8"></a>
### Set by naming series

`operation_enterprise_utilities_naming_business_behavior_set_by_naming_series`

**Inputs** doctype, fieldname, naming\_series, hide\_name\_field = true, make\_mandatory = 1.

**State and service calls** execute query text (UPDATE).format(doctype = doctype, s = “%s”) · execute a supplied database query.

**Local steps**

- Bind dependencies make\_property\_setter.
- If naming\_series.
  - Evaluate make\_property\_setter(doctype, “naming\_series”, “hidden”, 0, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “naming\_series”, “reqd”, make\_mandatory, validate\_fields\_for\_doctype = false, …).
  - Attempt the following.
    - Evaluate Platform.db.sql(query text (UPDATE).format(doctype = doctype, s = “%s”), get\_default\_naming\_series(doctype)).
  - On failure (NamingSeriesNotSetError).
    - Take no action here.
  - If hide\_name\_field.
    - Evaluate make\_property\_setter(doctype, fieldname, “reqd”, 0, validate\_fields\_for\_doctype = false, …).
    - Evaluate make\_property\_setter(doctype, fieldname, “hidden”, 1, validate\_fields\_for\_doctype = false, …).
- Otherwise.
  - Evaluate make\_property\_setter(doctype, “naming\_series”, “reqd”, 0, validate\_fields\_for\_doctype = false, …).
  - Evaluate make\_property\_setter(doctype, “naming\_series”, “hidden”, 1, validate\_fields\_for\_doctype = false, …).
  - If hide\_name\_field.
    - Evaluate make\_property\_setter(doctype, fieldname, “hidden”, 0, validate\_fields\_for\_doctype = false, …).
    - Evaluate make\_property\_setter(doctype, fieldname, “reqd”, 1, validate\_fields\_for\_doctype = false, …).
    - Evaluate Platform.db.sql(formatted text update ′tab{doctype}′ set ′{fieldname}′=′name′ where  ifnull({fieldname}, '')='').

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L279) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-013.tsv#L73)

## Service · Notifications

<a id="op-b093dc3e301046"></a>
### Get notification config

`operation_enterprise_startup_notifications_business_behavior_get_notification_configuration`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all.

**Explicit results** notifications.

**Local steps**

- Set notifications from mapping(“for\_doctype” → mapping(“Issue” → mapping(“status” → “Open”), “Warranty Claim” → mapping(“status” → “Open”), “Task” → mapping(“status” → tuple(“in”, tuple(“Open”, “Overdue”))), “Project” → mapping( ….
- Set doctype from list of d for d drawn from notifications.get(“for\_doctype”).
  - Draw d from notifications.get(“for\_doctype”).
- For each doc in Platform.get\_all(“DocType”, fields = list(“name”), filters = mapping(“name” → tuple(“not in”, doctype), “is\_submittable” → 1)).
  - Set notifications at “for\_doctype” at doc.name from mapping(“docstatus” → 0).
- Return notifications.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L3371) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1145) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L686)

## Service · Order

<a id="op-35445aff159fba"></a>
### Get context

`operation_enterprise_templates_pages_order_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from Platform.form\_dict.doctype via get\_doc · read “Payment Request” via get\_value · read “Property Setter” via get\_value · read “Customer” via get\_value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Set context.no\_cache from 1.
- Set context.show\_sidebar from true.
- Set context.doc from Platform.get\_doc(Platform.form\_dict.doctype, Platform.form\_dict.name).
- If hasattr(context.doc, “set\_indicator”).
  - Evaluate context.doc.set\_indicator().
- Set context.parents from Platform.form\_dict.parents.
- Set context.title from Platform.form\_dict.name.
- Set context.payment\_ref from Platform.db.get\_value(“Payment Request”, mapping(“reference\_name” → Platform.form\_dict.name), “name”).
- Set default\_print\_format from Platform.db.get\_value(“Property Setter”, dict(property = “default\_print\_format”, doc\_type = Platform.form\_dict.doctype), “value”).
- If default\_print\_format.
  - Set context.print\_format from default\_print\_format.
- Otherwise.
  - Set context.print\_format from “Standard”.
- If not (context.doc.has\_permission(“read”) or Platform.has\_website\_permission(context.doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.doc.has\_permission(“read”) → Platform.has\_website\_permission(context.doc).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Set context.available\_loyalty\_points from 0.0.
- If context.doc.get(“customer”).
  - Set customer\_loyalty\_program from Platform.db.get\_value(“Customer”, context.doc.customer, “loyalty\_program”).
  - If customer\_loyalty\_program.
    - Bind dependencies get\_loyalty\_details.
    - Set loyalty\_details from get\_loyalty\_details(context.doc.customer, customer\_loyalty\_program).
    - Set context.available\_loyalty\_points from int(loyalty\_details.get(“loyalty\_points”)).
- Set tuple(context.show\_pay\_button, context.pay\_amount) from get\_payment\_details(context.doc).
- Set context.show\_make\_pi\_button from false.
- If context.doc.get(“supplier”).
  - Set context.show\_make\_pi\_button from Platform.has\_permission(“Purchase Invoice”, “create”).
- If (context.show\_pay\_button or context.show\_make\_pi\_button).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.show\_pay\_button → context.show\_make\_pi\_button.
  - Set context.csrf\_token from get\_csrf\_token().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from context.doc.has\_permission(“read”), Platform.has\_permission(“Purchase Invoice”, “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1344)

<a id="op-af8cc2e36d7f1f"></a>
### Get attachments

`operation_enterprise_templates_pages_order_business_behavior_get_attachments`

**Inputs** dt, dn.

**Record and data access** read “File” via get\_all.

**Explicit results** Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_private”), filters = mapping(“attached\_to\_name” → dn, “attached\_to\_doctype” → dt, “is\_private” → 0)).

**Local steps**

- Return Platform.get\_all(“File”, fields = list(“name”, “file\_name”, “file\_url”, “is\_private”), filters = mapping(“attached\_to\_name” → dn, “attached\_to\_doctype” → dt, “is\_private” → 0)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0977.json#L1536) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1343)

<a id="op-ee44072114dc72"></a>
### Get payment details

`operation_enterprise_templates_pages_order_business_behavior_get_payment_details`

**Inputs** doc.

**Explicit results** tuple(false, 0) · tuple(true, amount) when amount &gt; 0, otherwise tuple(false, 0).

**Local steps**

- If (“payments” does not belong to Platform.get\_installed\_apps() or doc.doctype does not belong to PORTAL\_PAYABLE\_DOCTYPES or doc.docstatus differs from 1 or not (has\_website\_permission(doc, “read”, Platform.s ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “payments” does not belong to Platform.get\_installed\_apps() → doc.doctype does not belong to PORTAL\_PAYABLE\_DOCTYPES → doc.docstatus differs from 1 → not (has\_website\_permission(doc, “read”, Platform.session.user) or (Platform.has\_permission(“Payment Request”, “create”) and doc.has\_permission(“read”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_website\_permission(doc, “read”, Platform.session.user) → (Platform.has\_permission(“Payment Request”, “create”) and doc.has\_permission(“read”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.has\_permission(“Payment Request”, “create”) → doc.has\_permission(“read”).
  - Return tuple(false, 0).
- Set amount from get\_amount(doc).
- Return tuple(true, amount) when amount &gt; 0, otherwise tuple(false, 0).
  - Value choice on amount &gt; 0 — true gives tuple(true, amount), false gives tuple(false, 0).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Request”, “create”), doc.has\_permission(“read”).

**Boundaries to resolve** callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1345)

## Service · Partners

<a id="op-44c7df1a1da691"></a>
### Get context

`operation_enterprise_templates_pages_partners_business_behavior_get_context`

**Inputs** context.

**Record and data access** execute query text (SELECT, Sales Partner).

**Explicit results** mapping(“partners” → partners, “title” → page\_title).

**Local steps**

- Set partners from Platform.db.sql(query text (SELECT, Sales Partner), as\_dict = true).
- Return mapping(“partners” → partners, “title” → page\_title).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1346)
