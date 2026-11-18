# Integrations and service calls · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Command palette

<a id="op-b054abf6b820ce"></a>
### Search activity

`operation_relationships_binding_crm_api_command_palette_search_activity`

**Inputs** query.

**Explicit results** list() · list of \_activity\_row(hit, records at key) for tuple(key, hit) drawn from targets where key belongs to records.

**Local steps**

- Set search from CRMSearch().
- Attempt the following.
  - Set hits from search.search(query) at “results”.
- On failure (SQLiteSearchIndexMissingError).
  - Return list().
- If search.is\_post\_filter\_required.
  - Set hits from \_readable\_hits(hits).
- Set targets from \_activity\_targets(hits) at slice no value to ACTIVITY\_LIMIT.
- Set records from \_activity\_records(list of key for tuple(key, \_hit) drawn from targets).
  - Draw tuple(key, \_hit) from targets.
- Return list of \_activity\_row(hit, records at key) for tuple(key, hit) drawn from targets where key belongs to records.
  - Draw tuple(key, hit) from targets, keep a combination only if (key belongs to records).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L42) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L198) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L179)

<a id="op-44db4ee15ce7b3"></a>
### Readable hits

`operation_relationships_binding_crm_api_command_palette_readable_hits`

**Inputs** hits.

**Explicit results** list of hit for hit drawn from hits where \_parent\_of(hit) belongs to readable.

**Local steps**

- Set readable from \_activity\_records(list of \_parent\_of(hit) for hit drawn from hits).
  - Draw hit from hits.
- Return list of hit for hit drawn from hits where \_parent\_of(hit) belongs to readable.
  - Draw hit from hits, keep a combination only if (\_parent\_of(hit) belongs to readable).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L38) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L194) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L175)

<a id="op-0e0a6c6d26ea34"></a>
### Activity targets

`operation_relationships_binding_crm_api_command_palette_activity_targets`

**Inputs** hits.

**Explicit results** list(targets.items()).

**Local steps**

- Set deal\_by\_lead from \_readable\_deals\_by\_lead(hits).
- Set targets from mapping().
- For each hit in hits.
  - Set tuple(doctype, name) from \_parent\_of(hit).
  - If (doctype equals “CRM Lead” and name belongs to deal\_by\_lead).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “CRM Lead” → name belongs to deal\_by\_lead.
    - Set tuple(doctype, name) from tuple(“CRM Deal”, deal\_by\_lead at name).
  - Evaluate targets.setdefault(tuple(doctype, name), hit).
- Return list(targets.items()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L31) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L187) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L168)

<a id="op-c9d27748410b78"></a>
### Readable deals by lead

`operation_relationships_binding_crm_api_command_palette_readable_deals_by_lead`

**Inputs** hits.

**Record and data access** read “CRM Deal” via get\_list.

**Explicit results** mapping() · mapping of deal.lead → deal.name for deal drawn from deals.

**Local steps**

- Set leads from list of hit at “parent”.split(“:”, 1) at 1 for hit drawn from hits where hit at “parent”.startswith(“CRM Lead:”).
  - Draw hit from hits, keep a combination only if (hit at “parent”.startswith(“CRM Lead:”)).
- If not leads.
  - Return mapping().
- Set deals from Platform.get\_list(“CRM Deal”, filters = mapping(“lead” → list(“in”, leads)), fields = list(“name”, “lead”)).
- Return mapping of deal.lead → deal.name for deal drawn from deals.
  - Draw deal from deals.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L37) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L193) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L174)

<a id="op-c02241971949d5"></a>
### Parent of

`operation_relationships_binding_crm_api_command_palette_parent_of`

**Inputs** hit.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(doctype, name).

**Local steps**

- Set tuple(doctype, name) from hit at “parent”.split(“:”, 1).
- Return tuple(doctype, name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L35) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L191) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L172)

<a id="op-1e330112a949d3"></a>
### Activity records

`operation_relationships_binding_crm_api_command_palette_activity_records`

**Inputs** keys.

**Explicit results** mapping of tuple(record at “doctype”, record at “name”) → record for tuple(doctype, doctype\_names) drawn from names.items(), then record drawn from \_recent\_doctype(doctype, doctype\_names).

**Local steps**

- Set names from defaultdict(list).
- For each tuple(doctype, name) in keys.
  - Evaluate names at doctype.append(name).
- Return mapping of tuple(record at “doctype”, record at “name”) → record for tuple(doctype, doctype\_names) drawn from names.items(), then record drawn from \_recent\_doctype(doctype, doctype\_names).
  - Draw tuple(doctype, doctype\_names) from names.items().
  - Draw record from \_recent\_doctype(doctype, doctype\_names).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L29) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L185) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L166)

<a id="op-caf8c1547a31d9"></a>
### Activity row

`operation_relationships_binding_crm_api_command_palette_activity_row`

**Inputs** hit, record.

**Explicit results** mapping(“source\_doctype” → hit at “doctype”, “source\_name” → hit at “name”, “parent\_doctype” → record at “doctype”, “parent\_name” → record at “name”, …).

**Local steps**

- Return mapping(“source\_doctype” → hit at “doctype”, “source\_name” → hit at “name”, “parent\_doctype” → record at “doctype”, “parent\_name” → record at “name”, …).

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L30) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L186) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L167)

<a id="op-1473f2d90910e7"></a>
### Get recent

`operation_relationships_binding_crm_api_command_palette_get_recent`

**Inputs** recent.

**Explicit results** results.

**Local steps**

- Set results from list().
- For each tuple(doctype, names) in recent.items().
  - If (doctype belongs to SEARCH\_TYPES and isinstance(names, list) and Platform.has\_permission(doctype, “read”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype belongs to SEARCH\_TYPES → isinstance(names, list) → Platform.has\_permission(doctype, “read”).
    - Evaluate results.extend(\_recent\_doctype(doctype, names at slice no value to 5)).
- Return results.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L32) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L188) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L169)

<a id="op-a4cdc5c55db797"></a>
### Recent doctype

`operation_relationships_binding_crm_api_command_palette_recent_doctype`

**Inputs** doctype, names.

**Record and data access** read doctype via get\_list.

**Explicit results** list() · list of \_record(by\_name at name, doctype, route, title\_field) for name drawn from names where name belongs to by\_name.

**Local steps**

- If not names.
  - Return list().
- Set tuple(route, title\_field, \_search\_fields) from SEARCH\_TYPES at doctype.
- Set rows from Platform.get\_list(doctype, fields = list(“name”, title\_field), filters = mapping(“name” → list(“in”, names))).
- Set by\_name from mapping of row.name → row for row drawn from rows.
  - Draw row from rows.
- Return list of \_record(by\_name at name, doctype, route, title\_field) for name drawn from names where name belongs to by\_name.
  - Draw name from names, keep a combination only if (name belongs to by\_name).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L39) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L195) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L176)

<a id="op-92ee6398460314"></a>
### Record

`operation_relationships_binding_crm_api_command_palette_record`

**Inputs** row, doctype, route, title\_field.

**Explicit results** mapping(“doctype” → doctype, “name” → row.name, “title” → (row.get(title\_field) or row.name), “route” → route).

**Local steps**

- Return mapping(“doctype” → doctype, “name” → row.name, “title” → (row.get(title\_field) or row.name), “route” → route).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(title\_field) → row.name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L40) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L196) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L177)

## Service · Comment

<a id="op-a4c32de0aec94d"></a>
### On update

`operation_relationships_application_interface_comment_business_behavior_on_update`

**Inputs** self, method.

**Local steps**

- Evaluate notify\_mentions(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L23) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L22)

<a id="op-f6074682db4116"></a>
### Notify mentions

`operation_relationships_application_interface_comment_business_behavior_notify_mentions`

**Inputs** doc.

**Record and data access** resolve a document from doc.reference\_doctype via get\_doc · read “User” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If doc.reference\_doctype does not belong to list(“CRM Lead”, “CRM Deal”).
  - Return no value.
- Set content from getattr(doc, “content”, no value).
- If not content.
  - Return no value.
- Set mentions from extract\_mentions(content).
- Set reference\_doc from Platform.get\_doc(doc.reference\_doctype, doc.reference\_name).
- For each mention in mentions.
  - Set owner from Platform.get\_cached\_value(“User”, doc.owner, “full\_name”).
  - Set doctype from doc.reference\_doctype.
  - If doctype.startswith(“CRM ”).
    - Set doctype from doctype at slice 4 to no value.lower().
  - Set name from reference\_doc.lead\_name when doctype equals “lead”, otherwise (reference\_doc.organization or reference\_doc.lead\_name).
    - Value choice on doctype equals “lead” — true gives reference\_doc.lead\_name, false gives (reference\_doc.organization or reference\_doc.lead\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in reference\_doc.organization → reference\_doc.lead\_name.
  - Set notification\_text from formatted text              &lt;div class="mb-2 leading-5 text-ink-gray-5"&gt;                 &lt;span class="font-medium text-ink-gray-9"&gt;{owner}&lt;/span&gt;                 &lt;sp.
  - Evaluate notify\_user(mapping(“owner” → doc.owner, “assigned\_to” → mention.email, “notification\_type” → “Mention”, “message” → doc.content, …)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(doc, “content”, no value) · configured or stored value from Platform.get\_cached\_value(“User”, doc.owner, “full\_name”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L65) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L22) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L21)

<a id="op-130d7063f592fe"></a>
### Extract mentions

`operation_relationships_application_interface_comment_business_behavior_extract_mentions`

**Inputs** html.

**Explicit results** list() · mentions.

**Local steps**

- If not html.
  - Return list().
- Set soup from BeautifulSoup(html, “html.parser”).
- Set mentions from list().
- For each d in soup.find\_all(“span”, attrs = mapping(“data-type” → “mention”)).
  - Evaluate mentions.append(Platform.\_dict(full\_name = d.get(“data-label”), email = d.get(“data-id”))).
- Return mentions.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L765) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L21) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L20)

<a id="op-a3b95619a1ef5b"></a>
### Add comment

`operation_relationships_application_interface_comment_business_behavior_add_comment`

**Inputs** reference\_doctype, reference\_name, content, attachments = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** comment.

**Local steps**

- Set comment from Platform\_add\_comment(reference\_doctype, reference\_name, content, comment\_email = Platform.session.user, comment\_by = get\_fullname(Platform.session.user)).
- If (attachments and comment.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in attachments → comment.name.
  - Evaluate add\_attachments(comment.name, attachments).
- Return comment.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L1003) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L20) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L19)

<a id="op-ef1dbc5a08271d"></a>
### Add attachments

`operation_relationships_application_interface_comment_business_behavior_add_attachments`

**Inputs** name, attachments.

**Declared result** no value.

**Record and data access** read “File” via get\_value.

**State and service calls** request new\_doc for “File” · call save on \_file.

**Local steps**

- For each a in attachments.
  - If isinstance(a, str).
    - Set attach from Platform.db.get\_value(“File”, mapping(“name” → a), list(“file\_url”, “is\_private”), as\_dict = 1).
    - Set file\_args from mapping(“file\_url” → attach.file\_url, “is\_private” → attach.is\_private).
  - Otherwise.
    - If (isinstance(a, dict) and “fcontent” belongs to a and “fname” belongs to a).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(a, dict) → “fcontent” belongs to a → “fname” belongs to a.
      - Set file\_args from mapping(“file\_name” → a at “fname”, “content” → a at “fcontent”, “is\_private” → 1).
    - Otherwise.
      - Continue with the next iteration or loop test.
  - Evaluate file\_args.update(mapping(“attached\_to\_doctype” → “Comment”, “attached\_to\_name” → name, “folder” → “Home/Attachments”)).
  - Set \_file from Platform.new\_doc(“File”).
  - Evaluate \_file.update(file\_args).
  - Evaluate \_file.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L1254) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L19) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L18)

## Service · Contact

<a id="op-ec325cc4f4fab7"></a>
### Validate

`operation_relationships_application_interface_contact_business_behavior_validate`

**Inputs** doc, method.

**Local steps**

- Evaluate update\_deals\_email\_mobile\_no(doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L1815) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L29) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L28)

<a id="op-0c7afe5c7b20e3"></a>
### Update deals email mobile no

`operation_relationships_application_interface_contact_business_behavior_update_deals_email_mobile_number`

**Inputs** doc.

**Record and data access** read “CRM Contacts” via get\_all · read “CRM Deal” via get\_values.

**State and service calls** request set\_value on “CRM Deal”.

**Local steps**

- Set linked\_deals from Platform.get\_all(“CRM Contacts”, filters = mapping(“contact” → doc.name, “is\_primary” → 1), fields = list(“parent”)).
- For each linked\_deal in linked\_deals.
  - Set deal from Platform.db.get\_values(“CRM Deal”, linked\_deal.parent, list(“email”, “mobile\_no”), as\_dict = true) at 0.
  - If (deal.email differs from doc.email\_id or deal.mobile\_no differs from doc.mobile\_no).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in deal.email differs from doc.email\_id → deal.mobile\_no differs from doc.mobile\_no.
    - Evaluate Platform.db.set\_value(“CRM Deal”, linked\_deal.parent, mapping(“email” → doc.email\_id, “mobile\_no” → doc.mobile\_no)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L1874) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L28) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L27)

<a id="op-931395dd768fcc"></a>
### Get linked deals

`operation_relationships_application_interface_contact_business_behavior_get_linked_deals`

**Inputs** contact.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “CRM Contacts” via get\_all · resolve a document from “CRM Deal” via get\_cached\_doc.

**Explicit results** deals.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted”.

**Local steps**

- If not Platform.has\_permission(“Contact”, “read”, contact).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set deal\_names from Platform.get\_all(“CRM Contacts”, filters = mapping(“contact” → contact, “parenttype” → “CRM Deal”), fields = list(“parent”), distinct = true).
- Set deals from list().
- For each d in deal\_names.
  - Set deal from Platform.get\_cached\_doc(“CRM Deal”, d.parent, fields = list(“name”, “organization”, “currency”, “deal\_value”, …)).
  - Evaluate deals.append(deal.as\_dict()).
- Return deals.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”, “read”, contact) · configured or stored value from Platform.get\_cached\_doc(“CRM Deal”, d.parent, fields = list(“name”, “organization”, “currency”, “deal\_value”, …)).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L2260) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L25) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L24)

<a id="op-c1b6f61a6900dd"></a>
### Create new

`operation_relationships_application_interface_contact_business_behavior_create_new`

**Inputs** contact, field, value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contact” via get\_cached\_doc.

**State and service calls** call save on contact.

**Explicit results** true.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted” · validation helper — translated “Invalid field”.

**Local steps**

- If not Platform.has\_permission(“Contact”, “write”, contact).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set contact from Platform.get\_cached\_doc(“Contact”, contact).
- If field equals “email”.
  - Set email from mapping(“email\_id” → value, “is\_primary” → 1 when len(contact.email\_ids) equals 0, otherwise 0).
    - Value choice on len(contact.email\_ids) equals 0 — true gives 1, false gives 0.
  - Evaluate contact.append(“email\_ids”, email).
- Otherwise.
  - If field belongs to tuple(“mobile\_no”, “phone”).
    - Set mobile\_no from mapping(“phone” → value, “is\_primary\_mobile\_no” → 1 when len(contact.phone\_nos) equals 0, otherwise 0).
      - Value choice on len(contact.phone\_nos) equals 0 — true gives 1, false gives 0.
    - Evaluate contact.append(“phone\_nos”, mobile\_no).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid field”).
- Evaluate contact.save().
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”, “write”, contact) · configured or stored value from Platform.get\_cached\_doc(“Contact”, contact).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L2729) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L24) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L23)

<a id="op-e759cd960b5356"></a>
### Set as primary

`operation_relationships_application_interface_contact_business_behavior_set_as_primary`

**Inputs** contact, field, value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Contact” via get\_doc.

**State and service calls** call save on contact.

**Explicit results** true.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not permitted” · validation helper — translated “Invalid field”.

**Local steps**

- If not Platform.has\_permission(“Contact”, “write”, contact).
  - Call the validation error handler Platform.throw(translated “Not permitted”, Platform.PermissionError).
- Set contact from Platform.get\_doc(“Contact”, contact).
- If field equals “email”.
  - For each email in contact.email\_ids.
    - If email.email\_id equals value.
      - Set email.is\_primary from 1.
    - Otherwise.
      - Set email.is\_primary from 0.
- Otherwise.
  - If field belongs to tuple(“mobile\_no”, “phone”).
    - Set name from “is\_primary\_mobile\_no” when field equals “mobile\_no”, otherwise “is\_primary\_phone”.
      - Value choice on field equals “mobile\_no” — true gives “is\_primary\_mobile\_no”, false gives “is\_primary\_phone”.
    - For each phone in contact.phone\_nos.
      - If phone.phone equals value.
        - Evaluate phone.set(name, 1).
      - Otherwise.
        - Evaluate phone.set(name, 0).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Invalid field”).
- Evaluate contact.save().
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Contact”, “write”, contact).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L3307) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L27) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L26)

<a id="op-2b94f355c8adfa"></a>
### Search emails

`operation_relationships_application_interface_contact_business_behavior_search_emails`

**Inputs** txt.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** results.

**Local steps**

- Set doctype from “Contact”.
- Set meta from Platform.get\_meta(doctype).
- Set filters from list(list(“Contact”, “email\_id”, “is”, “set”)).
- If meta.get(“fields”, mapping(“fieldname” → “enabled”, “fieldtype” → “Check”)).
  - Evaluate filters.append(list(doctype, “enabled”, “=”, 1)).
- If meta.get(“fields”, mapping(“fieldname” → “disabled”, “fieldtype” → “Check”)).
  - Evaluate filters.append(list(doctype, “disabled”, “!=”, 1)).
- Set or\_filters from list().
- Set search\_fields from list(“full\_name”, “email\_id”, “name”).
- If txt.
  - For each f in search\_fields.
    - Evaluate or\_filters.append(list(doctype, f.strip(), “like”, formatted text %{txt}%)).
- Set results from Platform.get\_list(doctype, filters = filters, fields = search\_fields, or\_filters = or\_filters, limit\_start = 0, …).
- Return results.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L3883) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L26) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L25)

## Service · Dashboard

<a id="op-ddc4870cafd788"></a>
### Timestamp Diff.initialize

`operation_relationships_application_interface_dashboard_business_behavior_timestamp_diff_initialize`

**Inputs** self, unit, start, end, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(“TIMESTAMPDIFF”, unit, start, end, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L4534) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L56) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L52)

<a id="op-4122868677569b"></a>
### Reset to default

`operation_relationships_application_interface_dashboard_business_behavior_reset_to_default`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.only\_for(“System Manager”, true).
- Evaluate create\_default\_manager\_dashboard(force = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”, true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L4642) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L55) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L51)

<a id="op-66b49992dc4da6"></a>
### Get dashboard

`operation_relationships_application_interface_dashboard_business_behavior_get_dashboard`

**Inputs** from\_date = no value, to\_date = no value, user = no value.

**Wrappers, in declaration order** Platform.whitelist(), sales\_user\_only.

**Record and data access** read “CRM Dashboard” via exists · read “CRM Dashboard” via get\_value.

**State and service calls** commit.

**Explicit results** layout.

**Local steps**

- If (not from\_date or not to\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not from\_date → not to\_date.
  - Set from\_date from Platform.utils.get\_first\_day((from\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in from\_date → Platform.utils.nowdate().
  - Set to\_date from Platform.utils.get\_last\_day((to\_date or Platform.utils.nowdate())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in to\_date → Platform.utils.nowdate().
- Set roles from Platform.get\_roles(Platform.session.user).
- Set is\_sales\_manager from (“Sales Manager” belongs to roles or “System Manager” belongs to roles).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “Sales Manager” belongs to roles → “System Manager” belongs to roles.
- Set is\_sales\_user from (“Sales User” belongs to roles and not is\_sales\_manager).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in “Sales User” belongs to roles → not is\_sales\_manager.
- If is\_sales\_user.
  - Set user from Platform.session.user.
- Set dashboard from Platform.db.exists(“CRM Dashboard”, “Manager Dashboard”).
- Set layout from list().
- If not dashboard.
  - Set layout from json.loads(create\_default\_manager\_dashboard()).
  - Evaluate Platform.db.commit().
- Otherwise.
  - Set layout from json.loads((Platform.db.get\_value(“CRM Dashboard”, “Manager Dashboard”, “layout”) or “&#91;&#93;”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(“CRM Dashboard”, “Manager Dashboard”, “layout”) → “&#91;&#93;”.
- For each l in layout.
  - Set method\_name from formatted text get\_{l at “name”}.
  - If hasattr(Platform.get\_attr(“crm.api.dashboard”), method\_name).
    - Set method from getattr(Platform.get\_attr(“crm.api.dashboard”), method\_name).
    - Set l at “data” from method(from\_date, to\_date, user).
  - Otherwise.
    - Set l at “data” from no value.
- Return layout.

**Values supplied outside this operation** clock or generated value from Platform.utils.nowdate() · effective access from Platform.get\_roles(Platform.session.user) · selected callable from Platform.get\_attr(“crm.api.dashboard”), getattr(Platform.get\_attr(“crm.api.dashboard”), method\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0003.json#L4739) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L40) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L36)
