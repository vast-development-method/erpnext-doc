# Forms, reports and navigation · operations 26

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Dock

[Record definition](../../../../data/record-types/dock.json)

<a id="op-4fdc60c8110117"></a>
### Save app dock

`operation_foundation_desk_record_definitions_dock_business_behavior_save_application_dock`

**Inputs** app, items.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Dock” via get\_doc.

**State and service calls** call save on doc.

**Explicit results** resolve\_app\_dock(app).

**Explicit failure paths** validation helper — translated “{0} ships no dock yet. Export one to the app first.”.format(Platform.bold(app)).

**Local steps**

- Set app from check\_docked\_app(app).
- Evaluate check\_developer\_mode().
- Set doc from get\_dock(app, standard = 1).
- If not doc.
  - Call the validation error handler Platform.throw(translated “{0} ships no dock yet. Export one to the app first.”.format(Platform.bold(app))).
- Set doc from Platform.get\_doc(“Dock”, doc.name).
- Evaluate doc.set(“items”, list()).
- For each row in shape\_dock\_rows(items, require\_visible = false, below = mapping()).
  - Evaluate doc.append(“items”, mapping of field → row at field for field drawn from DOCK\_ITEM\_FIELDS).
    - Draw field from DOCK\_ITEM\_FIELDS.
- Evaluate doc.save().
- Return resolve\_app\_dock(app).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L6901) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L728)

<a id="op-b925efd8b91e16"></a>
### Get app dock layer

`operation_foundation_desk_record_definitions_dock_business_behavior_get_application_dock_layer`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Explicit results** list of mapping(expand rail\_entry(row), “hidden” → row at “hidden”) for row drawn from get\_app\_dock(check\_docked\_app(app)).

**Local steps**

- Return list of mapping(expand rail\_entry(row), “hidden” → row at “hidden”) for row drawn from get\_app\_dock(check\_docked\_app(app)).
  - Draw row from get\_app\_dock(check\_docked\_app(app)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0167.json#L7372) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L184) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L705)

<a id="op-2f6f9b69699e7e"></a>
### Reset dock for everyone

`operation_foundation_desk_record_definitions_dock_business_behavior_reset_dock_for_everyone`

**Inputs** app.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at dict.

**Record and data access** read “Dock” via get\_all.

**State and service calls** request delete\_doc for “Dock”.

**Explicit results** resolve\_app\_dock(app).

**Local steps**

- Evaluate check\_workspace\_manager(translated “You need to be Workspace Manager to reset the dock for everyone.”).
- Set app from check\_docked\_app(app).
- For each name in Platform.get\_all(“Dock”, filters = mapping(“app” → app, “standard” → 0), pluck = “name”).
  - Evaluate Platform.delete\_doc(“Dock”, name, force = true, ignore\_permissions = true).
- Return resolve\_app\_dock(app).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0168.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L725)

<a id="op-aaada203754da7"></a>
### Has permission

`operation_foundation_desk_record_definitions_dock_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, debug.

**Explicit result forms** Boolean true, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0168.json#L305) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L193) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L714)

<a id="op-c758bf76304069"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_dock_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0168.json#L507) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L188) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L709)

## Record · Doctype layout

<a id="op-ccc9a87ec7b64e"></a>
### Doc Type Layout.validate

`operation_foundation_binding_foundation_custom_doctype_doctype_layout_doctype_layout_doctypelayout_validate`

**Inputs** self.

**Local steps**

- If not self.route.
  - Set self.route from slug(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L194) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L652)

<a id="op-01ef859c4dbdf0"></a>
### Doc Type Layout.sync fields

`operation_foundation_binding_foundation_custom_doctype_doctype_layout_doctype_layout_doctypelayout_sync_fields`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · mapping(“added” → added, “removed” → removed).

**Local steps**

- Set doctype\_fields from Platform.get\_meta(self.document\_type, cached = false).fields.
- If self.is\_new().
  - Set added\_fields from list of field.fieldname for field drawn from doctype\_fields.
    - Draw field from doctype\_fields.
  - Set removed\_fields from list().
- Otherwise.
  - Set doctype\_fieldnames from set of field.fieldname for field drawn from doctype\_fields.
    - Draw field from doctype\_fields.
  - Set layout\_fieldnames from set of field.fieldname for field drawn from self.fields.
    - Draw field from self.fields.
  - Set added\_fields from list((doctype\_fieldnames − layout\_fieldnames)).
  - Set removed\_fields from list((layout\_fieldnames − doctype\_fieldnames)).
- If not (added\_fields or removed\_fields).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in added\_fields → removed\_fields.
  - Return no value.
- Set added from self.add\_fields(added\_fields, doctype\_fields).
- Set removed from self.remove\_fields(removed\_fields).
- For each tuple(index, field) in enumerate(self.fields).
  - Set field.idx from (index + 1).
- Return mapping(“added” → added, “removed” → removed).

**Methods declared on this owner** [add fields](operations-026.md#op-d156de2460400a), [remove fields](operations-026.md#op-1631f4bdb852ce).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L193) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L651)

<a id="op-d156de2460400a"></a>
### Doc Type Layout.add fields

`operation_foundation_binding_foundation_custom_doctype_doctype_layout_doctype_layout_doctypelayout_add_fields`

**Inputs** self, added\_fields, doctype\_fields.

**Declared result** list at dict.

**State and service calls** call insert on self.fields.

**Explicit results** added.

**Local steps**

- Set added from list().
- For each field in added\_fields.
  - Set field\_details from next(generator of f for f drawn from doctype\_fields where f.fieldname equals field, no value).
    - Draw f from doctype\_fields, keep a combination only if (f.fieldname equals field).
  - If not field\_details.
    - Continue with the next iteration or loop test.
  - Set row from self.append(“fields”, field\_details.as\_dict(no\_default\_fields = true)).
  - Set row\_data from row.as\_dict().
  - If field\_details.get(“insert\_after”).
    - Set insert\_after from next(generator of f for f drawn from self.fields where f.fieldname equals field\_details.insert\_after, no value).
      - Draw f from self.fields, keep a combination only if (f.fieldname equals field\_details.insert\_after).
    - If insert\_after.
      - Evaluate self.fields.insert(insert\_after.idx, row).
      - Evaluate self.fields.pop().
      - Set row\_data from mapping(“idx” → (insert\_after.idx + 1), “fieldname” → row.fieldname, “label” → row.label).
  - Evaluate added.append(row\_data).
- Return added.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L191) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L649)

<a id="op-1631f4bdb852ce"></a>
### Doc Type Layout.remove fields

`operation_foundation_binding_foundation_custom_doctype_doctype_layout_doctype_layout_doctypelayout_remove_fields`

**Inputs** self, removed\_fields.

**Declared result** list at dict.

**Explicit results** removed.

**Local steps**

- Set removed from list().
- For each field in removed\_fields.
  - Set field\_details from next(generator of f for f drawn from self.fields where f.fieldname equals field, no value).
    - Draw f from self.fields, keep a combination only if (f.fieldname equals field).
  - If field\_details.
    - Evaluate self.remove(field\_details).
    - Evaluate removed.append(field\_details.as\_dict()).
- Return removed.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L192) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L650)

## Service · Document follow

<a id="op-72ef16110fe516"></a>
### Update follow

`operation_foundation_desk_form_document_follow_business_behavior_update_follow`

**Inputs** doctype, doc\_name, following.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** bool(is\_following) · false.

**Local steps**

- Set following from Platform.utils.sbool(following).
- If following.
  - Set is\_following from follow\_document(doctype, doc\_name).
  - Return bool(is\_following).
- Otherwise.
  - Evaluate unfollow\_document(doctype, doc\_name).
  - Return false.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L2604) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1700) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L185)

<a id="op-b6e61be65cfb1c"></a>
### Follow document

`operation_foundation_desk_form_document_follow_business_behavior_follow_document`

**Inputs** doctype, doc\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_follow\_document(doctype, doc\_name, Platform.session.user).

**Local steps**

- Return \_follow\_document(doctype, doc\_name, Platform.session.user).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L53) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1680) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L165)

<a id="op-bce686a2127694"></a>
### Follow document

`operation_foundation_desk_form_document_follow_business_behavior_follow_document_2`

**Inputs** doctype, doc\_name, user, ignore\_permissions (named only, default false).

**Record and data access** read “User” via get\_value.

**State and service calls** toast with translated “Can't follow since changes are not tracked.” · toast with translated “Administrator can't follow” · toast with translated “Document follow is not enabled for this user.” · request new\_doc for “Document Follow” · call save on doc · 1 additional forms in the steps below.

**Explicit results** false · doc.

**Local steps**

- If (doctype belongs to tuple(“Communication”, “ToDo”, “Email Unsubscribe”, “File”, …) or doctype belongs to log\_types).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype belongs to tuple(“Communication”, “ToDo”, “Email Unsubscribe”, “File”, …) → doctype belongs to log\_types.
  - Return false.
- If not Platform.get\_meta(doctype).track\_changes.
  - Evaluate Platform.toast(translated “Can't follow since changes are not tracked.”).
  - Return false.
- If user equals “Administrator”.
  - Evaluate Platform.toast(translated “Administrator can't follow”).
  - Return false.
- If not Platform.has\_permission(doctype, “read”, doc = doc\_name, user = user).
  - Return false.
- If not Platform.db.get\_value(“User”, user, “document\_follow\_notify”, ignore = true, cache = true).
  - Evaluate Platform.toast(translated “Document follow is not enabled for this user.”).
  - Return false.
- If not is\_document\_followed(doctype, doc\_name, user).
  - If not Platform.has\_permission(“Document Follow”, “create”, user = user).
    - Return false.
  - Set doc from Platform.new\_doc(“Document Follow”).
  - Evaluate doc.update(mapping(“ref\_doctype” → doctype, “ref\_docname” → doc\_name, “user” → user)).
  - Evaluate doc.save(ignore\_permissions = true).
  - Evaluate Platform.toast(translated “Following document {0}”.format(doc\_name)).
  - Return doc.
- Return false.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, doc = doc\_name, user = user), Platform.has\_permission(“Document Follow”, “create”, user = user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L54) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L166)

<a id="op-d0e1dd734b5d5d"></a>
### Unfollow document

`operation_foundation_desk_form_document_follow_business_behavior_unfollow_document`

**Inputs** doctype, doc\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_unfollow\_document(doctype, doc\_name, Platform.session.user).

**Local steps**

- Return \_unfollow\_document(doctype, doc\_name, Platform.session.user).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L55) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1698) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L183)

<a id="op-2650d7936feddd"></a>
### Unfollow document

`operation_foundation_desk_form_document_follow_business_behavior_unfollow_document_2`

**Inputs** doctype, doc\_name, user.

**Record and data access** read “Document Follow” via get\_all.

**State and service calls** request delete\_doc for “Document Follow” · toast with translated “Un-following document {0}”.format(doc\_name).

**Explicit results** true · false.

**Local steps**

- Set doc from Platform.get\_all(“Document Follow”, filters = mapping(“ref\_doctype” → doctype, “ref\_docname” → doc\_name, “user” → user), fields = list(“name”), limit = 1).
- If doc.
  - Evaluate Platform.delete\_doc(“Document Follow”, doc at 0.name, force = true).
  - Evaluate Platform.toast(translated “Un-following document {0}”.format(doc\_name)).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L56) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1699) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L184)

<a id="op-626c5c113c2ce3"></a>
### Get message

`operation_foundation_desk_form_document_follow_business_behavior_get_message`

**Inputs** doc\_name, doctype, frequency, user.

**Explicit results** sorted(activity\_list, key = deferred anonymous expression, reverse = true).

**Local steps**

- Set activity\_list from (get\_version(doctype, doc\_name, frequency, user) + get\_comments(doctype, doc\_name, frequency, user)).
- Return sorted(activity\_list, key = deferred anonymous expression, reverse = true).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L4154) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L172)

<a id="op-1f09744136db5d"></a>
### Send email alert

`operation_foundation_desk_form_document_follow_business_behavior_send_email_alert`

**Inputs** receiver, docinfo, timeline.

**State and service calls** sendmail.

**Local steps**

- If receiver.
  - Evaluate Platform.sendmail(subject = translated “Document Follow Notification”, recipients = list(receiver), template = “document\_follow”, args = mapping(“docinfo” → docinfo, “timeline” → timeline)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.sendmail(subject = translated “Document Follow Notification”, recipients = list(receiver), template = “document\_follow”, args = mapping(“docinfo” → docinfo, “timeline” → timeline)).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L4342) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1695) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L180)

<a id="op-f4566c4f1652f5"></a>
### Send document follow mails

`operation_foundation_desk_form_document_follow_business_behavior_send_document_follow_mails`

**Inputs** frequency.

**State and service calls** commit.

**Local steps**

- Set user\_list from get\_user\_list(frequency).
- For each user in user\_list.
  - Set tuple(message, valid\_document\_follows) from get\_message\_for\_user(frequency, user).
  - If message.
    - Evaluate send\_email\_alert(user, valid\_document\_follows, message).
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L4500) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1694) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L179)

<a id="op-f4a5ebc1017bfb"></a>
### Get user list

`operation_foundation_desk_form_document_follow_business_behavior_get_user_list`

**Inputs** frequency.

**Explicit results** nested operand in the contract(nested operand in the contract).select(DocumentFollow.user).groupby(DocumentFollow.user).run(pluck = “user”).

**Local steps**

- Set DocumentFollow from DocType(“Document Follow”).
- Set User from DocType(“User”).
- Return nested operand in the contract(nested operand in the contract).select(DocumentFollow.user).groupby(DocumentFollow.user).run(pluck = “user”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L4675) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1690) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L175)

<a id="op-e89e26955a98eb"></a>
### Get message for user

`operation_foundation_desk_form_document_follow_business_behavior_get_message_for_user`

**Inputs** frequency, user.

**State and service calls** request delete on “Document Follow”.

**Explicit results** tuple(message, valid\_document\_follows).

**Local steps**

- Set message from list().
- Set latest\_document\_follows from get\_document\_followed\_by\_user(user).
- Set valid\_document\_follows from list().
- For each document\_follow in latest\_document\_follows.
  - If not Platform.has\_permission(document\_follow.ref\_doctype, “read”, doc = document\_follow.ref\_docname, user = user).
    - Evaluate Platform.db.delete(“Document Follow”, mapping(“ref\_doctype” → document\_follow.ref\_doctype, “ref\_docname” → document\_follow.ref\_docname, “user” → user)).
    - Continue with the next iteration or loop test.
  - Set content from get\_message(document\_follow.ref\_docname, document\_follow.ref\_doctype, frequency, user).
  - If content.
    - Set message from (message + content).
    - Evaluate valid\_document\_follows.append(mapping(“reference\_docname” → document\_follow.ref\_docname, “reference\_doctype” → document\_follow.ref\_doctype, “reference\_url” → get\_url\_to\_form(document\_follow.ref\_doctype, do ….
- Return tuple(message, valid\_document\_follows).

**Values supplied outside this operation** effective access from Platform.has\_permission(document\_follow.ref\_doctype, “read”, doc = document\_follow.ref\_docname, user = user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L5011) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L173)

<a id="op-a4420d9362d40b"></a>
### Get document followed by user

`operation_foundation_desk_form_document_follow_business_behavior_get_document_followed_by_user`

**Inputs** user.

**Explicit results** nested operand in the contract(nested operand in the contract, nested operand in the contract).orderby(DocumentFollow.creation).limit(20).run(as\_dict = true).

**Local steps**

- Set DocumentFollow from DocType(“Document Follow”).
- Return nested operand in the contract(nested operand in the contract, nested operand in the contract).orderby(DocumentFollow.creation).limit(20).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L5475) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L169)

<a id="op-6f03fdf7c77f6c"></a>
### Get version

`operation_foundation_desk_form_document_follow_business_behavior_get_version`

**Inputs** doctype, doc\_name, frequency, user.

**Record and data access** read “Version” via get\_all.

**Explicit results** timeline.

**Local steps**

- Set timeline from list().
- Set version from Platform.get\_all(“Version”, filters = list(list(“ref\_doctype”, “=”, doctype), list(“docname”, “=”, doc\_name), expanded \_get\_filters(frequency, user)), fields = list(“data”, “modified”, “modified\_by”)).
- If version.
  - For each v in version.
    - Set change from Platform.parse\_json(v.data).
    - Set time from Platform.utils.format\_datetime(v.modified, “hh:mm a”).
    - Set timeline\_items from list().
    - If change.changed.
      - Set timeline\_items from get\_field\_changed(change.changed, time, doctype, doc\_name, …).
    - If change.row\_changed.
      - Set timeline\_items from get\_row\_changed(change.row\_changed, time, doctype, doc\_name, …).
    - If change.added.
      - Set timeline\_items from get\_added\_row(change.added, time, doctype, doc\_name, …).
    - Set timeline from (timeline + timeline\_items).
- Return timeline.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L5685) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1691) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L176)

<a id="op-93db4566263bad"></a>
### Get comments

`operation_foundation_desk_form_document_follow_business_behavior_get_comments`

**Inputs** doctype, doc\_name, frequency, user.

**Explicit results** timeline.

**Local steps**

- Bind dependencies get\_document\_comments.
- Bind dependencies html2text.
- Set timeline from list().
- Set comments from get\_document\_comments(doctype, doc\_name, fields = list(“content”, “modified”, “modified\_by”, “comment\_type”), extra\_filters = \_get\_filters(frequency, user), user = user).
- For each comment in comments.
  - If comment.comment\_type equals “Like”.
    - Set by from formatted text  By : &lt;b&gt;{comment.modified\_by}&lt;b&gt;.
  - Otherwise.
    - If comment.comment\_type equals “Comment”.
      - Set by from formatted text Commented by : &lt;b&gt;{comment.modified\_by}&lt;b&gt;.
    - Otherwise.
      - Set by from empty text.
  - Set time from Platform.utils.format\_datetime(comment.modified, “hh:mm a”).
  - Evaluate timeline.append(mapping(“time” → comment.modified, “data” → mapping(“time” → time, “comment” → html2text(str(comment.content)), “by” → by), “doctype” → doctype, “doc\_name” → doc\_name, …)).
- Return timeline.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L6239) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L168)

<a id="op-4a27a9003822a0"></a>
### Is document followed

`operation_foundation_desk_form_document_follow_business_behavior_is_document_followed`

**Inputs** doctype, doc\_name, user.

**Record and data access** read “Document Follow” via exists.

**Explicit results** Platform.db.exists(“Document Follow”, mapping(“ref\_doctype” → doctype, “ref\_docname” → str(doc\_name), “user” → user)).

**Local steps**

- Return Platform.db.exists(“Document Follow”, mapping(“ref\_doctype” → doctype, “ref\_docname” → str(doc\_name), “user” → user)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0198.json#L6830) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1692) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L177)

<a id="op-29e8c97ece64c9"></a>
### Get row changed

`operation_foundation_desk_form_document_follow_business_behavior_get_row_changed`

**Inputs** row\_changed, time, doctype, doc\_name, v, user.

**Explicit results** items.

**Local steps**

- Bind dependencies html2text.
- Set items from list().
- For each d in row\_changed.
  - If not \_can\_read\_child\_table\_field(doctype, d at 0, d at 3 at 0 at 0, user).
    - Continue with the next iteration or loop test.
  - Set d at 0 from d at 0 when d at 0, otherwise one space.
    - Value choice on d at 0 — true gives d at 0, false gives one space.
  - Set d at 3 at 0 at 1 from d at 3 at 0 at 1 when d at 3 at 0 at 1, otherwise one space.
    - Value choice on d at 3 at 0 at 1 — true gives d at 3 at 0 at 1, false gives one space.
  - Evaluate items.append(mapping(“time” → v.modified, “data” → mapping(“time” → time, “table\_field” → d at 0, “row” → str(d at 1), “field” → d at 3 at 0 at 0, …), “doctype” → doctype, “doc\_name” → doc\_name, …)).
- Return items.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0199.json#L6) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1689) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L174)
