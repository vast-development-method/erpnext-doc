# Forms, reports and navigation · operations 77

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Tag

[Record definition](../../../../data/record-types/tag.json)

<a id="op-356ad7438d80ee"></a>
### Doc Tags.update

`operation_foundation_desk_record_definitions_tag_business_behavior_record_tags_update`

**Inputs** self, dn, tl.

**State and service calls** request set\_value on self.dt.

**Explicit results** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not tl.
  - Set tags from empty text.
- Otherwise.
  - Set tl from unique(filter(deferred anonymous expression, tl)).
  - Set tags from “,”.join(tl).
- Attempt the following.
  - Evaluate Platform.db.set\_value(self.dt, dn, “\_user\_tags”, tags, update\_modified = false).
  - Set doc from Platform.get\_lazy\_doc(self.dt, dn).
  - Evaluate update\_tags(doc, tags).
- On failure (Exception) bound to e.
  - If Platform.db.is\_missing\_column(e).
    - If not tags.
      - Return no value.
    - Evaluate self.setup().
    - Evaluate self.update(dn, tl).
  - Otherwise.
    - Propagate the active failure.

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup](operations-077.md#op-5a9b8fc8a70138).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L5610) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1268)

<a id="op-5a9b8fc8a70138"></a>
### Doc Tags.setup

`operation_foundation_desk_record_definitions_tag_business_behavior_record_tags_setup`

**Inputs** self.

**Local steps**

- Bind dependencies add\_column.
- Evaluate add\_column(self.dt, “\_user\_tags”, “Data”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L6019) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1267)

<a id="op-14a4f705b1c21c"></a>
### Delete tags for document

`operation_foundation_desk_record_definitions_tag_business_behavior_delete_tags_for_document`

**Inputs** doc.

**State and service calls** request delete on “Tag Link”.

**Explicit results** no value.

**Local steps**

- If not Platform.db.table\_exists(“Tag Link”).
  - Return no value.
- Evaluate Platform.db.delete(“Tag Link”, mapping(“document\_type” → doc.doctype, “document\_name” → doc.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L6096) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1256)

<a id="op-8b61870f374e2c"></a>
### Update tags

`operation_foundation_desk_record_definitions_tag_business_behavior_update_tags`

**Inputs** doc, tags.

**Record and data access** read “Tag Link” via get\_list · resolve a document from mapping(“doctype” → “Tag Link”, “document\_type” → doc.doctype, “document\_name” → doc.name, “title” → (doc.get\_title() or empty text), …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Tag Link”, “document\_type” → doc.doctype, “document\_name” → doc.name, “title” → (doc.get\_title() or empty text), …)) · request delete on “Tag Link”.

**Local steps**

- Evaluate doc.check\_permission(“write”).
- Set new\_tags from set of tag.strip() for tag drawn from tags.split(“,”) where tag.
  - Draw tag from tags.split(“,”), keep a combination only if (tag).
- Set existing\_tags from list of tag.tag for tag drawn from Platform.get\_list(“Tag Link”, filters = mapping(“document\_type” → doc.doctype, “document\_name” → doc.name), fields = list(“tag”)).
  - Draw tag from Platform.get\_list(“Tag Link”, filters = mapping(“document\_type” → doc.doctype, “document\_name” → doc.name), fields = list(“tag”)).
- Set added\_tags from (set(new\_tags) − set(existing\_tags)).
- For each tag in added\_tags.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Tag Link”, “document\_type” → doc.doctype, “document\_name” → doc.name, “title” → (nested operand in the contract.get\_title() or empty text), …)).insert(ignore\_permissions = true).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get\_title() → empty text.
- Set deleted\_tags from list((set(existing\_tags) − set(new\_tags))).
- For each tag in deleted\_tags.
  - Evaluate Platform.db.delete(“Tag Link”, mapping(“document\_type” → doc.doctype, “document\_name” → doc.name, “tag” → tag)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0190.json#L6251) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1270)

<a id="op-897e35eccebcf7"></a>
### Get documents for tag

`operation_foundation_desk_record_definitions_tag_business_behavior_get_documents_for_tag`

**Inputs** tag.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Tag Link” via get\_list.

**Explicit results** list of mapping(“doctype” → res.document\_type, “name” → res.document\_name, “content” → res.title) for res drawn from result.

**Local steps**

- Set tag from tag at slice 1 to no value.
- Set result from Platform.get\_list(“Tag Link”, filters = mapping(“tag” → tag), fields = list(“document\_type”, “document\_name”, “title”, “tag”)).
- Return list of mapping(“doctype” → res.document\_type, “name” → res.document\_name, “content” → res.title) for res drawn from result.
  - Draw res from result.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L809) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1257)

<a id="op-8af2ca61c9a461"></a>
### Get tags list for awesomebar

`operation_foundation_desk_record_definitions_tag_business_behavior_get_tags_list_for_awesomebar`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Tag” via get\_list.

**Explicit results** Platform.get\_list(“Tag”, pluck = “name”, order\_by = no value).

**Local steps**

- Return Platform.get\_list(“Tag”, pluck = “name”, order\_by = no value).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L284) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L812) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1260)

## Record · Tag link

[Record definition](../../../../data/record-types/tag_link.json)

<a id="op-0a7269b5dc41a1"></a>
### Tag Link.clear cache

`operation_foundation_desk_record_definitions_tag_link_business_behavior_tag_link_clear_cache`

**Inputs** self.

**Local steps**

- Evaluate super().clear\_cache().
- If has\_tags(self.document\_type).
  - Evaluate Platform.client\_cache.delete\_value(formatted text doctype\_has\_tags::{self.document\_type}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L1577) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1275)

<a id="op-fec93bb7126823"></a>
### On doctype update

`operation_foundation_desk_record_definitions_tag_link_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “Tag Link”.

**Local steps**

- Evaluate Platform.db.add\_index(“Tag Link”, list(“document\_type”, “document\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L1709) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1274)

<a id="op-f07538caa078e4"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_tag_link_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L1787) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L823) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1271)

<a id="op-a4a07de71866a1"></a>
### Has tags

`operation_foundation_desk_record_definitions_tag_link_business_behavior_has_tags`

**Inputs** doctype.

**Explicit results** Platform.client\_cache.get\_value(formatted text doctype\_has\_tags::{doctype}, generator = check\_db).

**Local steps**

- Bind local operation check\_db for subsequent calls.
- Return Platform.client\_cache.get\_value(formatted text doctype\_has\_tags::{doctype}, generator = check\_db).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L2018) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1272)

<a id="op-cc36314d93b3e0"></a>
### Has tags.check db

`operation_foundation_desk_record_definitions_tag_link_business_behavior_has_tags_check_database`

**Inputs** no declared parameters.

**Record and data access** read “Tag Link” via exists.

**Explicit results** Platform.db.exists(“Tag Link”, mapping(“document\_type” → doctype)).

**Local steps**

- Return Platform.db.exists(“Tag Link”, mapping(“document\_type” → doctype)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L2169) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L825) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1273)

## Service · Third party apps

<a id="op-ea6e461ea7573b"></a>
### Get context

`operation_foundation_public_pages_third_party_apps_business_behavior_get_context`

**Inputs** context.

**Record and data access** read “OAuth Bearer Token” via get\_all · read “OAuth Client” via get\_value · resolve a document from “OAuth Client” via get\_doc.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need to be logged in to access this page”.

**Local steps**

- If Platform.session.user equals “Guest”.
  - Call the validation error handler Platform.throw(translated “You need to be logged in to access this page”, Platform.PermissionError).
- Set active\_tokens from Platform.get\_all(“OAuth Bearer Token”, filters = list(list(“user”, “=”, Platform.session.user)), fields = list(“client”), distinct = true, order\_by = “creation”).
- Set client\_apps from list().
- For each token in active\_tokens.
  - Set creation from get\_first\_login(token.client).
  - Set app from mapping(“name” → token.get(“client”), “app\_name” → Platform.db.get\_value(“OAuth Client”, token.get(“client”), “app\_name”), “creation” → creation).
  - Evaluate client\_apps.append(app).
- Set app from no value.
- If Platform.form\_dict.get(“app”) belongs to set of client at “name” for client drawn from client\_apps.
  - Draw client from client\_apps.
  - Set app from Platform.get\_doc(“OAuth Client”, Platform.form\_dict.app).
  - Set app from app.\_\_dict\_\_.
  - Set app at “client\_secret” from no value.
- If app.
  - Set context.app from app.
- Set context.apps from client\_apps.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L86) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1397) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L99)

<a id="op-4107dc245f68e3"></a>
### Get first login

`operation_foundation_public_pages_third_party_apps_business_behavior_get_first_login`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** client.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L2497) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L100)

<a id="op-13bbbe01bc8b75"></a>
### Delete client

`operation_foundation_public_pages_third_party_apps_business_behavior_delete_client`

**Inputs** client\_id.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “OAuth Bearer Token” via get\_all.

**State and service calls** request delete\_doc for “OAuth Bearer Token”.

**Local steps**

- Set active\_client\_id\_tokens from Platform.get\_all(“OAuth Bearer Token”, filters = list(list(“user”, “=”, Platform.session.user), list(“client”, “=”, client\_id))).
- For each token in active\_client\_id\_tokens.
  - Evaluate Platform.delete\_doc(“OAuth Bearer Token”, token.get(“name”), ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L2759) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1396) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L98)

## Record · Todo

<a id="op-5958e93dee74dc"></a>
### To Do.validate

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_validate`

**Inputs** self.

**Local steps**

- Set self.\_assignment from no value.
- If self.is\_new().
  - If self.assigned\_by equals self.allocated\_to.
    - Set assignment\_message from Platform.\_(“{0} self assigned this task: {1}”).format(get\_fullname(self.assigned\_by), self.description).
  - Otherwise.
    - Set assignment\_message from Platform.\_(“{0} assigned {1}: {2}”).format(get\_fullname(self.assigned\_by), get\_fullname(self.allocated\_to), self.description).
  - Set self.\_assignment from mapping(“text” → assignment\_message, “comment\_type” → “Assigned”).
- Otherwise.
  - If self.get\_db\_value(“status”) differs from self.status.
    - If self.allocated\_to equals Platform.session.user.
      - Set removal\_message from Platform.\_(“{0} removed their assignment.”).format(get\_fullname(Platform.session.user)).
    - Otherwise.
      - Set removal\_message from Platform.\_(“Assignment of {0} removed by {1}”).format(get\_fullname(self.allocated\_to), get\_fullname(Platform.session.user)).
    - Set self.\_assignment from mapping(“text” → removal\_message, “comment\_type” → “Assignment Completed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L5420) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L842) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1288)

<a id="op-2ac402b6cc8b56"></a>
### To Do.on update

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_on_update`

**Inputs** self.

**Local steps**

- If self.\_assignment.
  - Evaluate self.add\_assign\_comment(expanded names self.\_assignment).
- Evaluate self.update\_in\_reference().

If control reaches the end, it returns no value.

**Methods declared on this owner** [add assign comment](operations-077.md#op-dde8486a24f087), [update in reference](operations-077.md#op-89154e1befa5a6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L6010) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L840) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1286)

<a id="op-9ecccf0e80937f"></a>
### To Do.on trash

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.delete\_communication\_links().
- Evaluate self.update\_in\_reference().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete communication links](operations-077.md#op-98578493998186), [update in reference](operations-077.md#op-89154e1befa5a6).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L6108) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L839) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1285)

<a id="op-dde8486a24f087"></a>
### To Do.add assign comment

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_add_assign_comment`

**Inputs** self, text, comment\_type.

**Record and data access** resolve a document from self.reference\_type via get\_doc.

**Explicit results** no value.

**Local steps**

- If not (self.reference\_type and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type → self.reference\_name.
  - Return no value.
- Evaluate Platform.get\_doc(self.reference\_type, self.reference\_name).add\_comment(comment\_type, text).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L6179) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L836) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1282)

<a id="op-98578493998186"></a>
### To Do.delete communication links

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_delete_communication_links`

**Inputs** self.

**State and service calls** request delete on “Communication Link”.

**Explicit results** Platform.db.delete(“Communication Link”, mapping(“link\_doctype” → self.doctype, “link\_name” → self.name)).

**Local steps**

- Return Platform.db.delete(“Communication Link”, mapping(“link\_doctype” → self.doctype, “link\_name” → self.name)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L6317) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L837) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1283)

<a id="op-89154e1befa5a6"></a>
### To Do.update in reference

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_update_in_reference`

**Inputs** self.

**Record and data access** read “ToDo” via get\_values.

**State and service calls** request set\_single\_value on self.reference\_type · request set\_value on self.reference\_type.

**Explicit results** no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- If not (self.reference\_type and self.reference\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.reference\_type → self.reference\_name.
  - Return no value.
- Attempt the following.
  - Set assignments from Platform.db.get\_values(“ToDo”, mapping(“reference\_type” → self.reference\_type, “reference\_name” → str(self.reference\_name), “status” → tuple(“not in”, tuple(“Cancelled”, “Closed”)), “allocated\_to” → tuple( ….
  - Evaluate assignments.reverse().
  - If Platform.get\_meta(self.reference\_type).issingle.
    - Evaluate Platform.db.set\_single\_value(self.reference\_type, “\_assign”, json.dumps(assignments) when assignments, otherwise empty text, update\_modified = false).
      - Value choice on assignments — true gives json.dumps(assignments), false gives empty text.
  - Otherwise.
    - Evaluate Platform.db.set\_value(self.reference\_type, self.reference\_name, “\_assign”, json.dumps(assignments) when assignments, otherwise empty text, update\_modified = false).
      - Value choice on assignments — true gives json.dumps(assignments), false gives empty text.
- On failure (Exception) bound to e.
  - If (Platform.db.is\_table\_missing(e) and Platform.flags.in\_install).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.is\_table\_missing(e) → Platform.flags.in\_install.
    - Return no value.
  - Otherwise.
    - If Platform.db.is\_missing\_column(e).
      - Bind dependencies add\_column.
      - Evaluate add\_column(self.reference\_type, “\_assign”, “Text”).
      - Evaluate self.update\_in\_reference().
    - Otherwise.
      - Propagate the active failure.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L6427) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L841) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1287)

<a id="op-08052b23cb0df4"></a>
### To Do.get owners

`operation_foundation_desk_record_definitions_todo_business_behavior_to_do_get_owners`

**Inputs** cls, filters = no value.

**Wrappers, in declaration order** classmethod.

**Record and data access** read cls.DocType via get\_all.

**Explicit results** list of parse\_addr(row.allocated\_to) at 1 for row drawn from rows where row.allocated\_to.

**Local steps**

- Set rows from Platform.get\_all(cls.DocType, filters = (filters or mapping()), fields = list(“allocated\_to”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Return list of parse\_addr(row.allocated\_to) at 1 for row drawn from rows where row.allocated\_to.
  - Draw row from rows, keep a combination only if (row.allocated\_to).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L7069) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L838) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1284)

<a id="op-ac56d3cd7c377e"></a>
### On doctype update

`operation_foundation_desk_record_definitions_todo_business_behavior_on_record_type_update`

**Inputs** no declared parameters.

**State and service calls** request add\_index on “ToDo”.

**Local steps**

- Evaluate Platform.db.add\_index(“ToDo”, list(“reference\_type”, “reference\_name”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0191.json#L7248) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L835) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1281)

<a id="op-c479557ed38059"></a>
### Get permission query conditions

`operation_foundation_desk_record_definitions_todo_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** no value, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0192.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L832) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1278)

<a id="op-df0d3c6c0c9080"></a>
### Has permission

`operation_foundation_desk_record_definitions_todo_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0192.json#L282) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L833) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1279)
