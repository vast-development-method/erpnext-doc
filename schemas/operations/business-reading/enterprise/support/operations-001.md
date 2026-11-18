# Customer support · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · First response time for issues

<a id="op-2e535861e9d7ad"></a>
### Execute

`operation_enterprise_support_report_first_response_time_for_issues_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set columns from list(mapping(“fieldname” → “creation\_date”, “label” → translated “Date”, “fieldtype” → “Date”, “width” → 300), mapping(“fieldname” → “first\_response\_time”, “fieldtype” → “Duration”, “label” → translated “F ….
- Set issue from Platform.qb.DocType(“Issue”).
- Set first\_response\_time from (get\_epoch\_seconds(issue.first\_responded\_on) − get\_epoch\_seconds(issue.creation)).
- Set data from nested operand in the contract(nested operand in the contract).groupby(Date(nested operand in the contract.creation)).orderby(Date(issue.creation), order = Platform.qb.desc).run().
- Return tuple(columns, data).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-012.tsv#L45) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1276)

<a id="op-913775d819ba55"></a>
### Get epoch seconds

`operation_enterprise_binding_enterprise_support_report_first_response_time_for_issues_first_response_time_for_issues_get_epoch_seconds`

**Inputs** field.

**Declared result** Floor.

**Explicit results** Floor(UnixTimestamp(field)).

**Local steps**

- Return Floor(UnixTimestamp(field)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L4) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1285)

<a id="op-df68357ac119a5"></a>
### Get permitted issues

`operation_enterprise_binding_enterprise_support_report_first_response_time_for_issues_first_response_time_for_issues_get_permitted_issues`

**Inputs** filters.

**Explicit results** Platform.qb.get\_query(“Issue”, fields = list(“name”), filters = company\_filter, ignore\_permissions = false).

**Local steps**

- Set company\_filter from mapping(“company” → filters.company) when filters.get(“company”), otherwise mapping().
  - Value choice on filters.get(“company”) — true gives mapping(“company” → filters.company), false gives mapping().
- Return Platform.qb.get\_query(“Issue”, fields = list(“name”), filters = company\_filter, ignore\_permissions = false).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L5) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1286)

## Record · Issue

[Record definition](../../../../data/record-types/issue.json)

<a id="op-5cdc51f4e6fc56"></a>
### Issue.validate

`operation_enterprise_support_record_definitions_issue_business_behavior_issue_validate`

**Inputs** self.

**Local steps**

- If (self.is\_new() and self.via\_customer\_portal).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.via\_customer\_portal.
  - Set self.flags.create\_communication from true.
- If (is\_website\_user() or Platform.flags.in\_web\_form).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_website\_user() → Platform.flags.in\_web\_form.
  - Evaluate self.restore\_staff\_only\_fields().
- If (Platform.flags.in\_web\_form and self.is\_new()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_web\_form → self.is\_new().
  - Set self.raised\_by from Platform.session.user.
- Otherwise.
  - If not self.raised\_by.
    - Set self.raised\_by from Platform.session.user.
- Evaluate self.set\_lead\_contact(self.raised\_by).
- Evaluate self.set\_opening\_time().

If control reaches the end, it returns no value.

**Methods declared on this owner** [restore staff only fields](operations-001.md#op-25401ed45f5333), [set lead contact](operations-001.md#op-589c089355bdda), [set opening time](operations-001.md#op-41a226a1561d2e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1121)

<a id="op-156b8ce0a3ae9b"></a>
### Issue.before save

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_issue_before_save`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If not self.service\_level\_agreement.
  - Evaluate self.record\_resolution\_metrics().

If control reaches the end, it returns no value.

**Methods declared on this owner** [record resolution metrics](operations-001.md#op-0333ccb7907f5c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1755) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1252)

<a id="op-0a4a9c02062ec9"></a>
### Issue.on update

`operation_enterprise_support_record_definitions_issue_business_behavior_issue_on_update`

**Inputs** self.

**Local steps**

- If (self.flags.create\_communication and self.via\_customer\_portal).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.create\_communication → self.via\_customer\_portal.
  - Evaluate self.create\_communication().
  - Set self.flags.communication\_created from no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [create communication](operations-001.md#op-fd9bb029492237).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0964.json#L6906) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1118)

<a id="op-6a5318126dd4d7"></a>
### Issue.on change

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_issue_on_change`

**Inputs** self.

**Local steps**

- If (self.status belongs to tuple(“Resolved”, “Closed”) and self.has\_value\_changed(“status”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.status belongs to tuple(“Resolved”, “Closed”) → self.has\_value\_changed(“status”).
  - Evaluate close\_all\_assignments(self.doctype, self.name, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1254)

<a id="op-25401ed45f5333"></a>
### Issue.restore staff only fields

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_issue_restore_staff_only_fields`

**Inputs** self.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- Set self.customer from doc\_before\_save.customer when doc\_before\_save, otherwise no value.
  - Value choice on doc\_before\_save — true gives doc\_before\_save.customer, false gives no value.
- Set self.status from doc\_before\_save.status when doc\_before\_save, otherwise “Open”.
  - Value choice on doc\_before\_save — true gives doc\_before\_save.status, false gives “Open”.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1256)

<a id="op-41a226a1561d2e"></a>
### Issue.set opening time

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_issue_set_opening_time`

**Inputs** self.

**Declared result** no value.

**Local steps**

- If not self.opening\_time.
  - Set self.opening\_time from get\_datetime(self.creation).time().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L73) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1257)

<a id="op-0333ccb7907f5c"></a>
### Issue.record resolution metrics

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_issue_record_resolution_metrics`

**Inputs** self.

**Declared result** no value.

**Local steps**

- Bind dependencies handle\_status\_change.
- Evaluate handle\_status\_change(self, true, hold\_statuses = list(), fulfillment\_statuses = RESOLVED\_STATUSES).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L71) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1255)

<a id="op-589c089355bdda"></a>
### Issue.set lead contact

`operation_enterprise_support_record_definitions_issue_business_behavior_issue_set_lead_contact`

**Inputs** self, email\_id.

**Record and data access** read “Lead” via get\_value · read “Contact Email” via get\_value · resolve a document from “Contact” via get\_doc.

**Local steps**

- Bind dependencies email.utils.
- Set email\_id from email.utils.parseaddr(email\_id) at 1.
- If email\_id.
  - If not self.lead.
    - Set self.lead from Platform.db.get\_value(“Lead”, mapping(“email\_id” → email\_id)).
  - If (not self.contact and not self.customer).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.contact → not self.customer.
    - Set self.contact from Platform.db.get\_value(“Contact Email”, mapping(“email\_id” → email\_id, “parenttype” → “Contact”), “parent”).
    - If self.contact.
      - Set contact from Platform.get\_doc(“Contact”, self.contact).
      - Set self.customer from contact.get\_link\_for(“Customer”).
  - If not self.company.
    - Set self.company from (Platform.db.get\_value(“Lead”, self.lead, “company”) or Platform.db.get\_default(“Company”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“Lead”, self.lead, “company”) → Platform.db.get\_default(“Company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1640) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1119)

<a id="op-fd9bb029492237"></a>
### Issue.create communication

`operation_enterprise_support_record_definitions_issue_business_behavior_issue_create_communication`

**Inputs** self.

**State and service calls** request new\_doc for “Communication” · call save on communication.

**Local steps**

- Set communication from Platform.new\_doc(“Communication”).
- Evaluate communication.update(mapping(“communication\_type” → “Communication”, “communication\_medium” → “Email”, “sent\_or\_received” → “Received”, “email\_status” → “Open”, …)).
- Set communication.flags.ignore\_permissions from true.
- Set communication.flags.ignore\_mandatory from true.
- Evaluate communication.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1116)

<a id="op-8d9b18c042405f"></a>
### Issue.get timeline communications

`operation_enterprise_support_record_definitions_issue_business_behavior_issue_get_timeline_communications`

**Inputs** self, after = no value, after\_name = no value.

**Record and data access** read “Communication” via get\_all · read “Communication Link” via get\_all.

**Explicit results** tuple(referenced, linked).

**Local steps**

- Set date\_filter from mapping(“communication\_date” → tuple(“&gt;=”, after)) when after, otherwise mapping().
  - Value choice on after — true gives mapping(“communication\_date” → tuple(“&gt;=”, after)), false gives mapping().
- Bind local operation at\_or\_after for subsequent calls.
- Set referenced from at\_or\_after(Platform.get\_all(“Communication”, filters = mapping(“reference\_doctype” → “Issue”, “reference\_name” → self.name, expand date\_filter), fields = list(“name”, “communication\_date”))).
- Set link\_parents from Platform.get\_all(“Communication Link”, filters = mapping(“link\_doctype” → “Issue”, “link\_name” → self.name), pluck = “parent”).
- Set linked from at\_or\_after(Platform.get\_all(“Communication”, filters = mapping(“name” → tuple(“in”, link\_parents), expand date\_filter), fields = list(“name”, “communication\_date”))) when link\_parents, otherwise set().
  - Value choice on link\_parents — true gives at\_or\_after(Platform.get\_all(“Communication”, filters = mapping(“name” → tuple(“in”, link\_parents), expand date\_filter), fields = list(“name”, “communication\_date”))), false gives set().
- Return tuple(referenced, linked).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1117)

<a id="op-9d24d3885270c2"></a>
### Issue.get timeline communications.at or after

`operation_enterprise_binding_enterprise_support_doctype_issue_issue_issue_get_timeline_communications_at_or_after`

**Inputs** rows.

**Explicit results** set of row.name for row drawn from rows · set of row.name for row drawn from rows where tuple(row.communication\_date, row.name) ≥ tuple(after, after\_name).

**Local steps**

- If (not after or not after\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not after → not after\_name.
  - Return set of row.name for row drawn from rows.
    - Draw row from rows.
- Return set of row.name for row drawn from rows where tuple(row.communication\_date, row.name) ≥ tuple(after, after\_name).
  - Draw row from rows, keep a combination only if (tuple(row.communication\_date, row.name) ≥ tuple(after, after\_name)).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L1756) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L1253)

<a id="op-94f21e4955e04d"></a>
### Issue.split issue

`operation_enterprise_support_record_definitions_issue_business_behavior_issue_split_issue`

**Inputs** self, subject, communication\_id.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Communication” via get\_doc · resolve a document from replicated\_issue via get\_doc · resolve a document from mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → “Issue”, “reference\_name” → replicated\_issue.name, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(replicated\_issue) · call save on doc · call insert on Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → “Issue”, “reference\_name” → replicated\_issue.name, …)).

**Explicit results** replicated\_issue.name.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Communication {0} is not on the timeline of Issue {1}”.format(communication\_id, self.name).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set tuple(referenced, linked) from self.get\_timeline\_communications().
- If communication\_id does not belong to (referenced bitwise or linked).
  - Call the validation error handler Platform.throw(translated “Communication {0} is not on the timeline of Issue {1}”.format(communication\_id, self.name), Platform.PermissionError).
- Set comm\_to\_split\_from from Platform.get\_doc(“Communication”, communication\_id).
- Bind dependencies deepcopy.
- Set replicated\_issue from deepcopy(self).
- Set replicated\_issue.subject from subject.
- Set replicated\_issue.issue\_split\_from from self.name.
- Set replicated\_issue.first\_response\_time from 0.
- Set replicated\_issue.first\_responded\_on from no value.
- Set replicated\_issue.creation from now\_datetime().
- Set replicated\_issue.opening\_time from no value.
- Set replicated\_issue.status from “Open”.
- Set replicated\_issue.opening\_date from getdate().
- Set replicated\_issue.resolution\_time from no value.
- Set replicated\_issue.user\_resolution\_time from no value.
- Set replicated\_issue.sla\_resolution\_date from no value.
- Set replicated\_issue.on\_hold\_since from no value.
- Set replicated\_issue.total\_hold\_time from no value.
- If replicated\_issue.service\_level\_agreement.
  - Set replicated\_issue.service\_level\_agreement\_creation from now\_datetime().
  - Set replicated\_issue.service\_level\_agreement from no value.
  - Set replicated\_issue.agreement\_status from “First Response Due”.
  - Set replicated\_issue.response\_by from no value.
  - Set replicated\_issue.sla\_resolution\_by from no value.
- Evaluate Platform.get\_doc(replicated\_issue).insert().
- Set tuple(referenced, linked) from self.get\_timeline\_communications(after = comm\_to\_split\_from.communication\_date, after\_name = comm\_to\_split\_from.name).
- For each name in sorted((referenced bitwise or linked)).
  - Set doc from Platform.get\_doc(“Communication”, name).
  - If name belongs to referenced.
    - Set doc.reference\_name from replicated\_issue.name.
  - For each link in doc.timeline\_links.
    - If (link.link\_doctype equals “Issue” and link.link\_name equals self.name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals “Issue” → link.link\_name equals self.name.
      - Set link.link\_name from replicated\_issue.name.
  - Evaluate doc.save(ignore\_permissions = true).
- Evaluate Platform.get\_doc(mapping(“doctype” → “Comment”, “comment\_type” → “Info”, “reference\_doctype” → “Issue”, “reference\_name” → replicated\_issue.name, …)).insert(ignore\_permissions = true).
- Return replicated\_issue.name.

**Methods declared on this owner** [get timeline communications](operations-001.md#op-8d9b18c042405f).

**Values supplied outside this operation** effective access from self.check\_permission(“write”) · clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1120)

<a id="op-78b6d3e138524b"></a>
### Get list context

`operation_enterprise_support_record_definitions_issue_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** mapping(“title” → translated “Issues”, “get\_list” → get\_issue\_list, “row\_template” → “templates/includes/issue\_row.html”, “show\_sidebar” → true, …).

**Local steps**

- Return mapping(“title” → translated “Issues”, “get\_list” → get\_issue\_list, “row\_template” → “templates/includes/issue\_row.html”, “show\_sidebar” → true, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L2011) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1627) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1107)

<a id="op-5c2be119fc6ca6"></a>
### Get issue list

`operation_enterprise_support_record_definitions_issue_business_behavior_get_issue_list`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, order\_by = no value.

**Explicit results** get\_list(doctype, txt, filters, limit\_start, ignore\_permissions = ignore\_permissions, …).

**Local steps**

- Bind dependencies get\_list.
- Bind dependencies get\_parents\_for\_user.
- Set user from Platform.session.user.
- Set ignore\_permissions from false.
- If (is\_website\_user() and user differs from “Guest”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_website\_user() → user differs from “Guest”.
  - If not filters.
    - Set filters from mapping().
  - If customers bound to get\_parents\_for\_user(“Customer”).
    - Set filters at “customer” from list(“in”, customers).
  - Otherwise.
    - Set filters at “raised\_by” from user.
  - Set ignore\_permissions from true.
- Return get\_list(doctype, txt, filters, limit\_start, ignore\_permissions = ignore\_permissions, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1626) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1106)

<a id="op-a8958c07ed45a1"></a>
### Set multiple status

`operation_enterprise_support_record_definitions_issue_business_behavior_set_multiple_status`

**Inputs** names, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid name”.

**Local steps**

- For each name in Platform.parse\_json(names).
  - If not isinstance(name, str).
    - Call the validation error handler Platform.throw(translated “Invalid name”, Platform.PermissionError).
  - Evaluate set\_status(name, status).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1646) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1125)

<a id="op-8aed96e274b650"></a>
### Set status

`operation_enterprise_support_record_definitions_issue_business_behavior_set_status`

**Inputs** name, status.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Issue” via get\_doc.

**State and service calls** call save on issue.

**Local steps**

- Evaluate Platform.has\_permission(“Issue”, “write”, name, throw = true).
- Set issue from Platform.get\_doc(“Issue”, name).
- Set issue.status from status.
- Evaluate issue.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Issue”, “write”, name, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1647) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1126)

<a id="op-57929c0ab3acce"></a>
### Auto close tickets

`operation_enterprise_support_record_definitions_issue_business_behavior_auto_close_tickets`

**Inputs** no declared parameters.

**Record and data access** read “Support Settings” via get\_single\_value · resolve a document from “Issue” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- Set auto\_close\_after\_days from Platform.db.get\_single\_value(“Support Settings”, “close\_issue\_after\_days”).
- If not auto\_close\_after\_days.
  - Return no value.
- Set table from Platform.qb.DocType(“Issue”).
- Set issues from nested operand in the contract(nested operand in the contract).select(table.name).where((table.modified &lt; (nested operand in the contract() − nested operand in the contract(days = nested operand in the con ….
- For each issue in issues.
  - Set doc from Platform.get\_doc(“Issue”, issue).
  - Set doc.status from “Closed”.
  - Set doc.flags.ignore\_permissions from true.
  - Set doc.flags.ignore\_mandatory from true.
  - Evaluate doc.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Support Settings”, “close\_issue\_after\_days”) · clock or generated value from Now().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0965.json#L2913) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1101)

<a id="op-17a857c18887da"></a>
### Has website permission

`operation_enterprise_support_record_definitions_issue_business_behavior_has_website_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, verbose.

**Explicit result forms** Boolean true, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0042.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1631) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1111)

<a id="op-a28a57da7e8c8d"></a>
### Update issue

`operation_enterprise_support_record_definitions_issue_business_behavior_update_issue`

**Inputs** contact, method.

**State and service calls** execute query text (UPDATE, Issue).

**Local steps**

- Evaluate Platform.db.sql(query text (UPDATE, Issue), contact.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1127)

<a id="op-015f25ec272f64"></a>
### Make task

`operation_enterprise_support_record_definitions_issue_business_behavior_make_task`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** get\_mapped\_doc(“Issue”, source\_name, mapping(“Issue” → mapping(“doctype” → “Task”)), target\_doc).

**Local steps**

- Return get\_mapped\_doc(“Issue”, source\_name, mapping(“Issue” → mapping(“doctype” → “Task”)), target\_doc).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1644) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1123)

<a id="op-1f20be856be95e"></a>
### Make issue from communication

`operation_enterprise_support_record_definitions_issue_business_behavior_make_issue_from_communication`

**Inputs** communication, ignore\_communication\_links = false.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Communication” via get\_doc · resolve a document from mapping(“doctype” → “Issue”, “subject” → doc.subject, “description” → doc.content, “communication\_medium” → doc.communication\_medium, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Issue”, “subject” → doc.subject, “description” → doc.content, “communication\_medium” → doc.communication\_medium, …)).

**Explicit results** issue.name.

**Local steps**

- Evaluate Platform.has\_permission(“Communication”, doc = communication, throw = true).
- Set doc from Platform.get\_doc(“Communication”, communication).
- Set issue from Platform.get\_doc(mapping(“doctype” → “Issue”, “subject” → doc.subject, “description” → doc.content, “communication\_medium” → doc.communication\_medium, …)).insert().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.phone\_no → empty text.
- Evaluate link\_communication\_to\_document(doc, “Issue”, issue.name, ignore\_communication\_links).
- Return issue.name.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Communication”, doc = communication, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0043.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L1643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L1122)
