# Forms, reports and navigation · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · 404

<a id="op-58426a87b29add"></a>
### Get context

`operation_foundation_public_pages_404_business_behavior_get_context`

**Inputs** context.

**Local steps**

- Set context.http\_status\_code from 404.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L5860) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L24)

## Service · About

<a id="op-bcbab96c264e38"></a>
### Get context

`operation_foundation_public_pages_about_business_behavior_get_context`

**Inputs** context.

**Record and data access** resolve a document from “About Us Settings” via get\_cached\_doc.

**Explicit results** context.

**Explicit failure paths** Platform.Redirect.

**Local steps**

- Set context.doc from Platform.get\_cached\_doc(“About Us Settings”).
- If context.doc.is\_disabled.
  - Set Platform.local.flags.redirect\_location from “/404”.
  - Raise Platform.Redirect.
- Return context.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“About Us Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0543.json#L6215) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L25)

## Service · Activity

<a id="op-d366d859e5b2b0"></a>
### Get activity timeline

`operation_foundation_desk_form_activity_business_behavior_get_activity_timeline`

**Inputs** doctype, name, visible\_types = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“activities” → activities, “has\_more\_emails” → has\_more\_emails, “has\_more\_milestones” → has\_more\_milestones, “next\_milestone\_start” → next\_milestone\_start).

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name, check\_permission = true).
- Set user\_info from mapping().
- Set tuple(visible, version\_fields) from parse\_visible\_types(visible\_types).
- Bind local operation show for subsequent calls.
- Set tuple(emails, has\_more\_emails) from get\_email\_activities(doc, user\_info) when show(“email”), otherwise tuple(list(), false).
  - Value choice on show(“email”) — true gives get\_email\_activities(doc, user\_info), false gives tuple(list(), false).
- Set tuple(milestones, has\_more\_milestones, next\_milestone\_start) from get\_milestone\_activities(doc, user\_info) when show(“log”), otherwise tuple(list(), false, 0).
  - Value choice on show(“log”) — true gives get\_milestone\_activities(doc, user\_info), false gives tuple(list(), false, 0).
- Set activities from list(expanded get\_creation\_activity(doc, user\_info) when show(“log”), otherwise list(), expanded get\_edit\_activity(doc, user\_info) when show(“log”), otherwise list(), expanded emails, expanded get\_comment\_ ….
  - Value choice on show(“log”) — true gives get\_creation\_activity(doc, user\_info), false gives list().
  - Value choice on show(“log”) — true gives get\_edit\_activity(doc, user\_info), false gives list().
  - Value choice on show(“comment”, “log”, “attachment\_log”) — true gives get\_comment\_and\_log\_activities(doc, user\_info), false gives list().
  - Value choice on show(“log”) — true gives get\_view\_activities(doc, user\_info), false gives list().
  - Value choice on show(“version”) — true gives get\_version\_activities(doc, user\_info, version\_fields), false gives list().
- If visible is distinct from no value.
  - Set activities from list of a for a drawn from activities where a at “type” belongs to visible.
    - Draw a from activities, keep a combination only if (a at “type” belongs to visible).
- Evaluate activities.sort(key = deferred anonymous expression).
- Return mapping(“activities” → activities, “has\_more\_emails” → has\_more\_emails, “has\_more\_milestones” → has\_more\_milestones, “next\_milestone\_start” → next\_milestone\_start).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L5669) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L128)

<a id="op-4d872c5f6d27ac"></a>
### Get activity timeline.show

`operation_foundation_desk_form_activity_business_behavior_get_activity_timeline_show`

**Inputs** remaining positional values types.

**Declared result** bool.

**Explicit results** (visible is identical to no value or not visible.isdisjoint(types)).

**Local steps**

- Return (visible is identical to no value or not visible.isdisjoint(types)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in visible is identical to no value → not visible.isdisjoint(types).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L6689) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1644) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L129)

<a id="op-d3625d488532d4"></a>
### Parse visible types

`operation_foundation_desk_form_activity_business_behavior_parse_visible_types`

**Inputs** visible\_types.

**Declared result** tuple at tuple((set at str bitwise or no value), (list at str bitwise or no value)).

**Explicit results** tuple(no value, no value) · tuple(types, version\_fields).

**Explicit failure paths** validation helper — translated “visible\_types is not valid JSON: {0}”.format(visible\_types) · validation helper — translated “visible\_types must be a list” · validation helper — translated “visible\_types fields for {0} must be a list”.format(activity\_type) · validation helper — translated “visible\_types entries must be strings or {type: &#91;fields&#93;} maps”.

**Local steps**

- If isinstance(visible\_types, str).
  - Attempt the following.
    - Set visible\_types from Platform.parse\_json(visible\_types).
  - On failure (JSONDecodeError).
    - Call the validation error handler Platform.throw(translated “visible\_types is not valid JSON: {0}”.format(visible\_types)).
- If not visible\_types.
  - Return tuple(no value, no value).
- If not isinstance(visible\_types, list).
  - Call the validation error handler Platform.throw(translated “visible\_types must be a list”).
- Set types from set().
- Set version\_fields from no value.
- For each entry in visible\_types.
  - If isinstance(entry, str).
    - Evaluate types.add(entry).
  - Otherwise.
    - If isinstance(entry, dict).
      - For each tuple(activity\_type, fields) in entry.items().
        - If not isinstance(fields, list).
          - Call the validation error handler Platform.throw(translated “visible\_types fields for {0} must be a list”.format(activity\_type)).
        - Evaluate types.add(activity\_type).
        - If activity\_type equals “version”.
          - Set version\_fields from fields.
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “visible\_types entries must be strings or {type: &#91;fields&#93;} maps”).
- Return tuple(types, version\_fields).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0195.json#L6768) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1662) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L147)

<a id="op-ee729cd1bfac60"></a>
### Get more email activities

`operation_foundation_desk_form_activity_business_behavior_get_more_email_activities`

**Inputs** doctype, name, start.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“activities” → emails, “has\_more\_emails” → has\_more\_emails).

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name, check\_permission = true).
- Set user\_info from mapping().
- Set tuple(emails, has\_more\_emails) from get\_email\_activities(doc, user\_info, start = Platform.utils.cint(start)).
- Evaluate emails.sort(key = deferred anonymous expression).
- Return mapping(“activities” → emails, “has\_more\_emails” → has\_more\_emails).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1655) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L140)

<a id="op-8b1fb31c7e8edf"></a>
### Get more milestone activities

`operation_foundation_desk_form_activity_business_behavior_get_more_milestone_activities`

**Inputs** doctype, name, start.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** dict.

**Explicit results** mapping(“activities” → milestones, “has\_more\_milestones” → has\_more, “next\_milestone\_start” → next\_start).

**Local steps**

- Set doc from Platform.get\_lazy\_doc(doctype, name, check\_permission = true).
- Set user\_info from mapping().
- Set tuple(milestones, has\_more, next\_start) from get\_milestone\_activities(doc, user\_info, start = Platform.utils.cint(start)).
- Evaluate milestones.sort(key = deferred anonymous expression).
- Return mapping(“activities” → milestones, “has\_more\_milestones” → has\_more, “next\_milestone\_start” → next\_start).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L349) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1656) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L141)

<a id="op-af0016ce5b905b"></a>
### Get creation activity

`operation_foundation_desk_form_activity_business_behavior_get_creation_activity`

**Inputs** doc, user\_info.

**Declared result** list at dict.

**Explicit results** list(mapping(“type” → “log”, “key” → “creation”, “timestamp” → str(doc.creation), “author” → author, …)).

**Local steps**

- Evaluate Platform.utils.add\_user\_info(set(doc.owner), user\_info).
- Set author from get\_author\_info(doc.owner, user\_info).
- Set msg from get\_creation\_msg(doc.owner, author at “fullname”).
- Return list(mapping(“type” → “log”, “key” → “creation”, “timestamp” → str(doc.creation), “author” → author, …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L707) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1649) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L134)

<a id="op-a20ff394b27bff"></a>
### Get creation msg

`operation_foundation_desk_form_activity_business_behavior_get_creation_message`

**Inputs** owner, fullname.

**Explicit results** translated “You created this document” · translated “{0} created this document”.format(fullname).

**Local steps**

- If Platform.session.user equals owner.
  - Return translated “You created this document”.
- Return translated “{0} created this document”.format(fullname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L1053) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1650) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L135)

<a id="op-e6e2db3b641547"></a>
### Get edit activity

`operation_foundation_desk_form_activity_business_behavior_get_edit_activity`

**Inputs** doc, user\_info.

**Declared result** list at dict.

**Explicit results** list() · list(mapping(“type” → “log”, “key” → “edited”, “timestamp” → str(doc.modified), “author” → author, …)).

**Local steps**

- If (not doc.modified or str(doc.modified) equals str(doc.creation)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc.modified → str(doc.modified) equals str(doc.creation).
  - Return list().
- Evaluate Platform.utils.add\_user\_info(set(doc.modified\_by), user\_info).
- Set author from get\_author\_info(doc.modified\_by, user\_info).
- Return list(mapping(“type” → “log”, “key” → “edited”, “timestamp” → str(doc.modified), “author” → author, …)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L1189) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1651) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L136)

<a id="op-06fe99e05062c3"></a>
### Get edit msg

`operation_foundation_desk_form_activity_business_behavior_get_edit_message`

**Inputs** modified\_by, fullname.

**Explicit results** translated “You last edited this document” · translated “{0} last edited this document”.format(fullname).

**Local steps**

- If Platform.session.user equals modified\_by.
  - Return translated “You last edited this document”.
- Return translated “{0} last edited this document”.format(fullname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L1595) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1652) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L137)

<a id="op-a5c28d3b28026a"></a>
### Get email activities

`operation_foundation_desk_form_activity_business_behavior_get_email_activities`

**Inputs** doc, user\_info, start = 0.

**Declared result** tuple at tuple(list at dict, bool).

**Explicit results** tuple(build\_email\_activities(communications, user\_info), has\_more).

**Local steps**

- Set communications from \_get\_communications(doc.doctype, doc.name, start = start, limit = (EMAIL\_PAGE\_SIZE + 1)).
- Set has\_more from len(communications) &gt; EMAIL\_PAGE\_SIZE.
- If has\_more.
  - Set communications from communications at slice no value to EMAIL\_PAGE\_SIZE.
- Evaluate Platform.utils.add\_user\_info(set of c.sender for c drawn from communications where c.sender, user\_info).
  - Draw c from communications, keep a combination only if (c.sender).
- Return tuple(build\_email\_activities(communications, user\_info), has\_more).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L1731) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1653) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L138)

<a id="op-707f4c08b7b350"></a>
### Build email activities

`operation_foundation_desk_form_activity_business_behavior_build_email_activities`

**Inputs** communications, user\_info.

**Declared result** list at dict.

**Explicit results** out.

**Local steps**

- Set out from list().
- For each c in communications.
  - Set info from (user\_info.get(c.sender) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_info.get(c.sender) → mapping().
  - Evaluate out.append(mapping(“type” → “email”, “key” → formatted text email:{c.name}, “timestamp” → str((c.communication\_date or c.creation)), “author” → mapping(“email” → c.sender, “fullname” → (c.sender\_full\_name  ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.communication\_date → c.creation.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.sender\_full\_name → info.get(“fullname”) → c.sender.
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L2068) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1639) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L124)

<a id="op-e0fc6c1c0688dc"></a>
### Parse email attachments

`operation_foundation_desk_form_activity_business_behavior_parse_email_attachments`

**Inputs** attachments.

**Declared result** list at dict.

**Explicit results** list() · out.

**Local steps**

- If not attachments.
  - Return list().
- Attempt the following.
  - Set parsed from json.loads(attachments) when isinstance(attachments, str), otherwise attachments.
    - Value choice on isinstance(attachments, str) — true gives json.loads(attachments), false gives attachments.
- On failure (tuple(json.JSONDecodeError, TypeError)).
  - Return list().
- Set out from list().
- For each a in (parsed or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed → list().
  - Set file\_url from a.get(“file\_url”).
  - Evaluate out.append(mapping(“file\_url” → file\_url, “file\_name” → (a.get(“file\_name”) or nested operand in the contract.split(“/”) at negative 1 when file\_url, otherwise no value), “is\_private” → a.get(“is\_private”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in a.get(“file\_name”) → file\_url.split(“/”) at negative 1 when file\_url, otherwise no value.
    - Value choice on file\_url — true gives file\_url.split(“/”) at negative 1, false gives no value.
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L2667) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1661) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L146)

<a id="op-615f896a502ac2"></a>
### Get comment and log activities

`operation_foundation_desk_form_activity_business_behavior_get_comment_and_log_activities`

**Inputs** doc, user\_info.

**Declared result** list at dict.

**Explicit results** out.

**Local steps**

- Set comment\_log\_data from Platform.\_dict().
- Evaluate add\_comments(doc, comment\_log\_data).
- Set all\_rows from ((((((nested operand in the contract.comments + nested operand in the contract.assignment\_logs) + comment\_log\_data.attachment\_logs) + comment\_log\_data.info\_logs) + comment\_log\_data.like\_logs) + comment\_log ….
- Evaluate Platform.utils.add\_user\_info(set of c.owner for c drawn from all\_rows where c.owner, user\_info).
  - Draw c from all\_rows, keep a combination only if (c.owner).
- Set out from list().
- Set attachments from get\_comment\_attachments(list of c.name for c drawn from comment\_log\_data.comments).
  - Draw c from comment\_log\_data.comments.
- For each c in comment\_log\_data.comments.
  - Set author from get\_author\_info(c.owner, user\_info).
  - Evaluate out.append(mapping(“type” → “comment”, “key” → formatted text comment:{c.name}, “timestamp” → str(c.creation), “author” → author, …)).
- For each c in comment\_log\_data.attachment\_logs.
  - Evaluate out.append(attachment\_log\_activity(c, get\_author\_info(c.owner, user\_info))).
- For each c in comment\_log\_data.like\_logs.
  - Set author from get\_author\_info(c.owner, user\_info).
  - Evaluate out.append(add\_activity\_record(c, author, “like”, translated “{0} liked”.format(author at “fullname”))).
- For each c in comment\_log\_data.assignment\_logs.
  - Set author from get\_author\_info(c.owner, user\_info).
  - Set text from activity\_text(c.content).
  - Set assignee from assignee\_from\_assignment(text, c.comment\_type).
  - If c.comment\_type equals “Assigned”.
    - Evaluate out.append(add\_activity\_record(c, author, “assigned”, text, assignee = assignee)).
  - Otherwise.
    - Evaluate out.append(add\_activity\_record(c, author, “assignment\_completed”, text, assignee = assignee)).
- For each c in comment\_log\_data.workflow\_logs.
  - Set author from get\_author\_info(c.owner, user\_info).
  - Evaluate out.append(add\_activity\_record(c, author, “workflow”, formatted text {author at “fullname”} {activity\_text(c.content)})).
- For each c in comment\_log\_data.info\_logs.
  - Set author from get\_author\_info(c.owner, user\_info).
  - Evaluate out.append(add\_activity\_record(c, author, “info”, formatted text {author at “fullname”} {activity\_text(c.content)})).
- For each c in comment\_log\_data.shared.
  - Set author from get\_author\_info(c.owner, user\_info).
  - Evaluate out.append(add\_activity\_record(c, author, “shared”, activity\_text(c.content))).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L3065) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1647) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L132)

<a id="op-4a48c46afc403a"></a>
### Get comment attachments

`operation_foundation_desk_form_activity_business_behavior_get_comment_attachments`

**Inputs** comment\_names.

**Declared result** dict at tuple(str, list at dict).

**Record and data access** read “File” via get\_all.

**Explicit results** mapping() · out.

**Local steps**

- If not comment\_names.
  - Return mapping().
- Set out from mapping().
- For each f in Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → “Comment”, “attached\_to\_name” → tuple(“in”, comment\_names)), fields = list(“file\_url”, “file\_name”, “is\_private”, “attached\_to\_name”), ord ….
  - Evaluate out.setdefault(f.attached\_to\_name, list()).append(mapping(“file\_url” → f.file\_url, “file\_name” → f.file\_name, “is\_private” → f.is\_private)).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L4591) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1648) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L133)

<a id="op-e8bbe755bfa655"></a>
### Get author info

`operation_foundation_desk_form_activity_business_behavior_get_author_info`

**Inputs** owner, user\_info.

**Declared result** dict.

**Explicit results** mapping(“email” → (info.get(“email”) or owner), “fullname” → (info.get(“fullname”) or owner), “image” → info.get(“image”)).

**Local steps**

- Set info from (user\_info.get(owner) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_info.get(owner) → mapping().
- Return mapping(“email” → (info.get(“email”) or owner), “fullname” → (info.get(“fullname”) or owner), “image” → info.get(“image”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in info.get(“email”) → owner.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in info.get(“fullname”) → owner.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L4966) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1645) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L130)

<a id="op-181d70e939ab0d"></a>
### Activity text

`operation_foundation_desk_form_activity_business_behavior_activity_text`

**Inputs** html.

**Declared result** str.

**Explicit results** unescape\_html(Platform.utils.strip\_html((html or empty text))).strip().

**Local steps**

- Return unescape\_html(Platform.utils.strip\_html((html or empty text))).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in html → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L47) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1635) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L120)

<a id="op-dbb511637f9b03"></a>
### Assignee from assignment

`operation_foundation_desk_form_activity_business_behavior_assignee_from_assignment`

**Inputs** text, comment\_type.

**Declared result** (str bitwise or no value).

**Explicit results** no value when assignee\_idx is identical to no value, otherwise groups.get(assignee\_idx) · no value.

**Local steps**

- If comment\_type equals “Assigned”.
  - Set templates from tuple(tuple(translated “{0} self assigned this task: {1}”, no value), tuple(translated “{0} assigned {1}: {2}”, 1)).
- Otherwise.
  - Set templates from tuple(tuple(translated “{0} removed their assignment.”, no value), tuple(translated “Assignment of {0} removed by {1}”, 0)).
- For each tuple(template, assignee\_idx) in templates.
  - Set groups from match\_format\_template(template, text).
  - If groups is identical to no value.
    - Continue with the next iteration or loop test.
  - Return no value when assignee\_idx is identical to no value, otherwise groups.get(assignee\_idx).
    - Value choice on assignee\_idx is identical to no value — true gives no value, false gives groups.get(assignee\_idx).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L5276) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L122)

<a id="op-f3008541338321"></a>
### Match format template

`operation_foundation_desk_form_activity_business_behavior_match_format_template`

**Inputs** template, text.

**Declared result** (dict at tuple(int, str) bitwise or no value).

**Explicit results** no value · mapping of placeholder → match.group((i + 1)) for tuple(i, placeholder) drawn from enumerate(order).

**Local steps**

- Set pattern from list(“^”).
- Set order from list().
- For each part in re.split(“(\\{\\d+\\})”, template).
  - Set m from re.fullmatch(“\\{(\\d+)\\}”, part).
  - If m.
    - Evaluate order.append(int(m.group(1))).
    - Evaluate pattern.append(“(.+?)”).
  - Otherwise.
    - Evaluate pattern.append(re.escape(part)).
- Evaluate pattern.append(“\\Z”).
- Set match from re.match(empty text.join(pattern), text, re.DOTALL).
- If not match.
  - Return no value.
- Return mapping of placeholder → match.group((i + 1)) for tuple(i, placeholder) drawn from enumerate(order).
  - Draw tuple(i, placeholder) from enumerate(order).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L5618) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1660) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L145)

<a id="op-dab579f9827c07"></a>
### Attachment log activity

`operation_foundation_desk_form_activity_business_behavior_attachment_log_activity`

**Inputs** c, author.

**Declared result** dict.

**Explicit results** mapping(“type” → “attachment\_log”, “key” → formatted text attachment:{c.name}, “timestamp” → str(c.creation), “author” → author, …).

**Local steps**

- Set action from “removed” when c.comment\_type equals “Attachment Removed”, otherwise “added”.
  - Value choice on c.comment\_type equals “Attachment Removed” — true gives “removed”, false gives “added”.
- Set content from (c.content or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.content → empty text.
- Set href from re.search(“href=&#91;'"&#93;(&#91;^'"&#93;+)&#91;'"&#93;”, content).
- Set file\_url from href.group(1) when (href and action equals “added”), otherwise no value.
  - Value choice on (href and action equals “added”) — true gives href.group(1), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in href → action equals “added”.
- Return mapping(“type” → “attachment\_log”, “key” → formatted text attachment:{c.name}, “timestamp” → str(c.creation), “author” → author, …).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in file\_url → file\_url.startswith(“/private/”).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L6086) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L123)

<a id="op-6b402bf1a419c3"></a>
### Add activity record

`operation_foundation_desk_form_activity_business_behavior_add_activity_record`

**Inputs** c, author, subtype, text, assignee = no value.

**Declared result** dict.

**Explicit results** mapping(“type” → “log”, “key” → formatted text log:{c.name}, “timestamp” → str(c.creation), “author” → author, …).

**Local steps**

- Set data from mapping(“name” → c.name, “subtype” → subtype, “text” → text).
- If assignee is distinct from no value.
  - Set data at “assignee” from assignee.
- Return mapping(“type” → “log”, “key” → formatted text log:{c.name}, “timestamp” → str(c.creation), “author” → author, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L6555) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L121)

<a id="op-8f2c741e767b92"></a>
### Get view activities

`operation_foundation_desk_form_activity_business_behavior_get_view_activities`

**Inputs** doc, user\_info.

**Declared result** list at dict.

**Explicit results** out.

**Local steps**

- Set views from get\_view\_logs(doc).
- Evaluate Platform.utils.add\_user\_info(set of v.owner for v drawn from views where v.owner, user\_info).
  - Draw v from views, keep a combination only if (v.owner).
- Set out from list().
- For each v in views.
  - Set author from get\_author\_info(v.owner, user\_info).
  - Evaluate out.append(mapping(“type” → “log”, “key” → formatted text view:{v.name}, “timestamp” → str(v.creation), “author” → author, …)).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0196.json#L6884) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1658) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L143)

<a id="op-584378cc12bd89"></a>
### Get milestone activities

`operation_foundation_desk_form_activity_business_behavior_get_milestone_activities`

**Inputs** doc, user\_info, start = 0.

**Declared result** tuple at tuple(list at dict, bool, int).

**Explicit results** tuple(list(), false, next\_start) · tuple(out, has\_more, next\_start).

**Local steps**

- Set milestones from get\_milestones(doc.doctype, doc.name, start = start, limit = (MILESTONE\_PAGE\_SIZE + 1)).
- Set has\_more from len(milestones) &gt; MILESTONE\_PAGE\_SIZE.
- If has\_more.
  - Set milestones from milestones at slice no value to MILESTONE\_PAGE\_SIZE.
- Set next\_start from (start + len(milestones)).
- If not milestones.
  - Return tuple(list(), false, next\_start).
- Set permitted from readable\_permlevels(doc.meta).
- Evaluate Platform.utils.add\_user\_info(set of m.owner for m drawn from milestones where m.owner, user\_info).
  - Draw m from milestones, keep a combination only if (m.owner).
- Set out from list().
- For each m in milestones.
  - Set df from is\_field\_visible(doc.meta, permitted, m.track\_field).
  - If not df.
    - Continue with the next iteration or loop test.
  - Set author from get\_author\_info(m.owner, user\_info).
  - Evaluate out.append(mapping(“type” → “log”, “key” → formatted text milestone:{m.name}, “timestamp” → str(m.creation), “author” → author, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → m.track\_field.
- Return tuple(out, has\_more, next\_start).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1654) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L139)
