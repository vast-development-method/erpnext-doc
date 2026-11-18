# Forms, reports and navigation · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Build

<a id="op-4002ac68d190e3"></a>
### Get editor assets

`operation_foundation_binding_foundation_studio_build_get_editor_assets`

**Inputs** entry.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · mapping(“script” → (EDITOR\_ASSETS\_BASE + manifest at entry at “file”), “preloads” → preloads, “stylesheets” → list(dict.fromkeys(stylesheets))).

**Local steps**

- Set manifest\_path from Platform.get\_app\_path(“Platform”, “public”, “studio”, “.vite”, …).
- If not os.path.exists(manifest\_path).
  - Return no value.
- Within open(manifest\_path) bound as f.
  - Set manifest from json.load(f).
- If entry does not belong to manifest.
  - Return no value.
- Set tuple(preloads, stylesheets, seen) from tuple(list(), list(), set()).
- Bind local operation collect for subsequent calls.
- Evaluate collect(entry).
- Return mapping(“script” → (EDITOR\_ASSETS\_BASE + manifest at entry at “file”), “preloads” → preloads, “stylesheets” → list(dict.fromkeys(stylesheets))).

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L5) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1923) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1899)

<a id="op-9c6d5b57d06494"></a>
### Get editor assets.collect

`operation_foundation_binding_foundation_studio_build_get_editor_assets_collect`

**Inputs** key.

**Explicit results** no value.

**Local steps**

- If key belongs to seen.
  - Return no value.
- Evaluate seen.add(key).
- Set chunk from manifest at key.
- For each imported in chunk.get(“imports”, list()).
  - Evaluate collect(imported).
- If key differs from entry.
  - Evaluate preloads.append((EDITOR\_ASSETS\_BASE + chunk at “file”)).
- Evaluate stylesheets.extend(generator of (EDITOR\_ASSETS\_BASE + css) for css drawn from chunk.get(“css”, list())).
  - Draw css from chunk.get(“css”, list()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L6) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1924) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1900)

<a id="op-e5509d289e872c"></a>
### After app build

`operation_foundation_binding_foundation_studio_build_after_app_build`

**Inputs** built\_apps.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not built\_apps.
  - Return no value.
- Evaluate click.secho(“\\nBuilding Studio Apps...”, fg = “cyan”).
- Evaluate build\_standard\_apps(built\_apps).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L231) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1918) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1894)

## Record · Bulk update

[Record definition](../../../../data/record-types/bulk_update.json)

<a id="op-407c65580f8a0a"></a>
### Bulk Update.bulk update

`operation_foundation_desk_record_definitions_bulk_update_business_behavior_bulk_update_bulk_update`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read call context via get\_all.

**Explicit results** submit\_cancel\_or\_update\_docs(self.document\_type, docnames, “update”, mapping(self.field → self.update\_value)).

**Explicit failure paths** validation helper — translated “The Bulk Update could not happen due to &lt;b&gt;{0}&lt;/b&gt;”.format(str(e)).

**Local steps**

- Evaluate self.check\_permission(“write”).
- Set limit from self.limit when (self.limit and cint(self.limit) &lt; 500), otherwise 500.
  - Value choice on (self.limit and cint(self.limit) &lt; 500) — true gives self.limit, false gives 500.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.limit → cint(self.limit) &lt; 500.
- Set query\_args from mapping(“doctype” → self.document\_type, “limit” → limit, “pluck” → “name”).
- If self.condition.
  - Attempt the following.
    - Set filters from Platform.parse\_json(self.condition).
    - If isinstance(filters, dict).
      - If “or\_filters” belongs to filters.
        - Set query\_args at “or\_filters” from filters.pop(“or\_filters”).
    - Set query\_args at “filters” from filters.
  - On failure (Exception) bound to e.
    - Call the validation error handler Platform.throw(translated “The Bulk Update could not happen due to &lt;b&gt;{0}&lt;/b&gt;”.format(str(e))).
- Set docnames from Platform.get\_all(expanded names query\_args).
- Return submit\_cancel\_or\_update\_docs(self.document\_type, docnames, “update”, mapping(self.field → self.update\_value)).

**Values supplied outside this operation** effective access from self.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L3667) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L420)

<a id="op-40993f16550111"></a>
### Submit cancel or update docs

`operation_foundation_desk_record_definitions_bulk_update_business_behavior_submit_cancel_or_update_records`

**Inputs** doctype, docnames, action = “submit”, data = no value, task\_id = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** msgprint with translated “Bulk operation is enqueued in background.” · enqueue with \_bulk\_action.

**Explicit results** \_bulk\_action(doctype, docnames, action, data, …).

**Explicit failure paths** validation helper — translated “Bulk operations only support up to 500 documents.”.

**Local steps**

- If isinstance(docnames, str).
  - Set docnames from Platform.parse\_json(docnames).
- If len(docnames) &lt; 20.
  - Return \_bulk\_action(doctype, docnames, action, data, …).
- Otherwise.
  - If len(docnames) ≤ 500.
    - Evaluate Platform.msgprint(translated “Bulk operation is enqueued in background.”, alert = true).
    - Evaluate Platform.enqueue(\_bulk\_action, doctype = doctype, docnames = docnames, action = action, data = data, …).
  - Otherwise.
    - Call the validation error handler Platform.throw(translated “Bulk operations only support up to 500 documents.”, title = translated “Too Many Documents”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(\_bulk\_action, doctype = doctype, docnames = docnames, action = action, data = data, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L105) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L421)

<a id="op-ccb5281dec3358"></a>
### Bulk action

`operation_foundation_desk_record_definitions_bulk_update_business_behavior_bulk_action`

**Inputs** doctype, docnames, action, data, task\_id = no value.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call submit on doc · call cancel on doc · call save on doc · commit · rollback.

**Explicit results** failed.

**Local steps**

- If data.
  - Set data from Platform.parse\_json(data).
- Set child\_table\_updates from data.get(“child\_table\_updates”) when data, otherwise no value.
  - Value choice on data — true gives data.get(“child\_table\_updates”), false gives no value.
- Set failed from list().
- Set num\_documents from len(docnames).
- For each tuple(idx, docname) in enumerate(docnames, 1).
  - Set doc from Platform.get\_doc(doctype, docname).
  - Attempt the following.
    - Set message from empty text.
    - If (action equals “submit” and doc.docstatus.is\_draft()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in action equals “submit” → doc.docstatus.is\_draft().
      - If (doc.meta.queue\_in\_background and not is\_scheduler\_inactive()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.meta.queue\_in\_background → not is\_scheduler\_inactive().
        - Evaluate queue\_submission(doc, action).
        - Set message from translated “Queuing {0} for Submission”.format(doctype).
      - Otherwise.
        - Evaluate doc.submit().
        - Set message from translated “Submitting {0}”.format(doctype).
    - Otherwise.
      - If (action equals “cancel” and doc.docstatus.is\_submitted()).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in action equals “cancel” → doc.docstatus.is\_submitted().
        - Evaluate doc.cancel().
        - Set message from translated “Cancelling {0}”.format(doctype).
      - Otherwise.
        - If (action equals “update” and not doc.docstatus.is\_cancelled()).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in action equals “update” → not doc.docstatus.is\_cancelled().
          - If child\_table\_updates.
            - Set table\_fields from doc.meta.get\_table\_fields().
            - For each tuple(child\_doctype, field\_updates) in child\_table\_updates.items().
              - Set table\_fieldname from next(generator of field.fieldname for field drawn from table\_fields where field.options equals child\_doctype, no value).
                - Draw field from table\_fields, keep a combination only if (field.options equals child\_doctype).
              - If (table\_fieldname and hasattr(doc, table\_fieldname)).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in table\_fieldname → hasattr(doc, table\_fieldname).
                - Set child\_meta from Platform.get\_meta(child\_doctype).
                - Set child\_docs from getattr(doc, table\_fieldname).
                - For each child\_doc in child\_docs.
                  - For each tuple(fieldname, value) in field\_updates.items().
                    - If child\_meta.has\_field(fieldname).
                      - Evaluate setattr(child\_doc, fieldname, value).
          - If data.
            - Evaluate doc.update(data).
          - Evaluate doc.save().
          - Set message from translated “Updating {0}”.format(doctype).
        - Otherwise.
          - Evaluate failed.append(docname).
    - Evaluate Platform.db.commit().
    - Evaluate Platform.publish\_progress(percent = ((idx ÷ num\_documents) × 100), title = message, description = docname, task\_id = task\_id).
  - On failure (Exception).
    - Evaluate Platform.log\_error(“Bulk action failed”).
    - Evaluate failed.append(docname).
    - Evaluate Platform.db.rollback().
- Return failed.

**Values supplied outside this operation** selected callable from getattr(doc, table\_fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0155.json#L4899) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L419)

## Service · Calendar

<a id="op-ef6a5f3484a7fe"></a>
### Update event

`operation_foundation_desk_calendar_business_behavior_update_event`

**Inputs** args, field\_map.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from args.doctype via get\_doc.

**State and service calls** call save on w.

**Local steps**

- Set args from Platform.\_dict(json.loads(args)).
- Set field\_map from Platform.\_dict(json.loads(field\_map)).
- Set w from Platform.get\_doc(args.doctype, args.name).
- Evaluate w.set(field\_map.start, args at field\_map.start).
- Evaluate w.set(field\_map.end, args.get(field\_map.end)).
- Evaluate w.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L37) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L66)

<a id="op-bc5e6bff4dcb3f"></a>
### Get event conditions

`operation_foundation_desk_calendar_business_behavior_get_event_conditions`

**Inputs** doctype, filters = no value.

**Explicit results** get\_filters\_cond(doctype, filters, list(), with\_match\_conditions = true).

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Not Permitted”.

**Local steps**

- Bind dependencies get\_filters\_cond.
- If not Platform.has\_permission(doctype).
  - Call the validation error handler Platform.throw(translated “Not Permitted”, Platform.PermissionError).
- Return get\_filters\_cond(doctype, filters, list(), with\_match\_conditions = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0152.json#L6583) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L64)

<a id="op-80c310418d34be"></a>
### Get events

`operation_foundation_desk_calendar_business_behavior_get_events`

**Inputs** doctype, start, end, field\_map, filters = no value, fields = no value, order\_by = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_list.

**Explicit results** Platform.get\_list(doctype, fields = fields, filters = filters, order\_by = order\_by).

**Explicit failure paths** validation helper — translated “{0} is not a valid field of {1}”.format(field\_map.get(key), doctype).

**Local steps**

- Set tuple(start, end) from tuple(getdate(start), get\_datetime(end)).
- Set field\_map from Platform.\_dict(json.loads(field\_map)).
- Set fields from Platform.parse\_json(fields).
- Set doc\_meta from Platform.get\_meta(doctype).
- For each d in doc\_meta.fields.
  - If d.fieldtype equals “Color”.
    - Evaluate field\_map.update(mapping(“color” → d.fieldname)).
- Set filters from json.loads(filters) when filters, otherwise list().
  - Value choice on filters — true gives json.loads(filters), false gives list().
- If not fields.
  - Set fields from list(field\_map.start, field\_map.end, field\_map.title, “name”).
- If field\_map.color.
  - Evaluate fields.append(field\_map.color).
- Set valid\_columns from doc\_meta.get\_valid\_columns().
- For each key in tuple(“start”, “end”).
  - If field\_map.get(key) does not belong to valid\_columns.
    - Call the validation error handler Platform.throw(translated “{0} is not a valid field of {1}”.format(field\_map.get(key), doctype)).
- Set dt from Platform.qb.DocType(doctype).
- Set start\_field from functions.IfNull(dt at field\_map.start, dt at field\_map.end).
- Set end\_field from functions.IfNull(dt at field\_map.end, dt at field\_map.start).
- Update filters using + list(list(start\_field, “&lt;=”, end), list(end\_field, “&gt;=”, start)).
- Set fields from list(set of field for field drawn from fields where field).
  - Draw field from fields, keep a combination only if (field).
- Return Platform.get\_list(doctype, fields = fields, filters = filters, order\_by = order\_by).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L36) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L65)

## Record · Client script

[Record definition](../../../../data/record-types/client_script.json)

<a id="op-da186361478fc3"></a>
### Client Script.on update

`operation_foundation_custom_record_definitions_client_script_business_behavior_client_script_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L1936) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L927)

<a id="op-a5b3b207eb007d"></a>
### Client Script.on trash

`operation_foundation_custom_record_definitions_client_script_business_behavior_client_script_on_trash`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache(doctype = self.dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L1999) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L781) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L926)

## Service · Commands

<a id="op-cac20a6ae80189"></a>
### Build studio app

`operation_foundation_binding_foundation_studio_commands_init_build_studio_app`

**Inputs** context, app\_name, site = no value.

**Wrappers, in declaration order** click.command(“build-studio-app”), click.argument(“app\_name”), click.option(“--site”, help = “site name”), pass\_context.

**Record and data access** resolve a document from “Studio App” via get\_doc.

**Explicit failure paths** SystemExit(1).

**Local steps**

- Bind dependencies StudioApp.
- If not site.
  - Set site from get\_site(context).
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Set app from Platform.get\_doc(“Studio App”, app\_name).
- Set result from app.generate\_app\_build().
- If build\_error bound to result.get(“build\_error”).
  - Evaluate click.secho(formatted text Build failed for '{app\_name}' — see the output above (Error Log: {build\_error at “error\_log”}), fg = “red”).
  - Raise SystemExit(1).
- Evaluate print(formatted text Studio App '{app\_name}' built successfully.).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L31) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1925)

<a id="op-72a686e75b5527"></a>
### Watch studio

`operation_foundation_binding_foundation_studio_commands_init_watch_studio`

**Inputs** context.

**Wrappers, in declaration order** click.command(“watch-studio”), pass\_context.

**Local steps**

- Bind dependencies watch.
- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- Attempt the following.
  - Evaluate watch(site).
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L32) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1926)

## Service · Components

<a id="op-70f9e0cd85afb0"></a>
### Get component definition

`operation_foundation_binding_foundation_studio_components_get_component_definition`

**Inputs** component.

**Declared result** dict.

**Explicit results** Platform.get\_file\_json(path).

**Explicit failure paths** validation helper — translated “Studio has no prop definition for {0}. Component names are case sensitive. Some components that work only in …”.format(Platform.bold(escape\_html(component))).

**Local steps**

- Set path from get\_schema\_files().get(component).
- If not path.
  - Call the validation error handler Platform.throw(translated “Studio has no prop definition for {0}. Component names are case sensitive. Some components that work only in …”.format(Platform.bold(escape\_html(component))), title = translated  ….
- Return Platform.get\_file\_json(path).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1927)

<a id="op-8f875bab8d0015"></a>
### Get schema files

`operation_foundation_binding_foundation_studio_components_get_schema_files`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Explicit results** mapping of file\_name.removesuffix(“.json”) → os.path.join(folder, library, file\_name) for library drawn from sorted(os.listdir(folder)) where os.path.isdir(os.path.join(folder, library)), then file\_name dr ….

**Local steps**

- Set folder from Platform.get\_app\_source\_path(“Platform”, expanded SCHEMA\_FOLDER).
- Return mapping of file\_name.removesuffix(“.json”) → os.path.join(folder, library, file\_name) for library drawn from sorted(os.listdir(folder)) where os.path.isdir(os.path.join(folder, library)), then file\_name dr ….
  - Draw library from sorted(os.listdir(folder)), keep a combination only if (os.path.isdir(os.path.join(folder, library))).
  - Draw file\_name from os.listdir(os.path.join(folder, library)), keep a combination only if (file\_name.endswith(“.json”)).

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1928)

## Record · Console log

[Record definition](../../../../data/record-types/console_log.json)

<a id="op-2fbd904ce304a7"></a>
### Console Log.after delete

`operation_foundation_desk_record_definitions_console_log_business_behavior_console_log_after_delete`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self.

**Observed service boundaries** validation or user-notification service.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0156.json#L3706) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L431)

## Record · Contact

[Record definition](../../../../data/record-types/contact.json)

<a id="op-2e99f8527d6844"></a>
### Contact.autoname

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_autoname`

**Inputs** self.

**Record and data access** read “Contact” via exists.

**Local steps**

- Set self.name from self.\_get\_full\_name().
- For each link in self.links.
  - Set self.name from ((self.name + “-”) + cstr(link.link\_name).strip()).
  - Leave the innermost loop without its normal-exhaustion alternative.
- If Platform.db.exists(“Contact”, self.name).
  - Set self.name from append\_number\_if\_name\_exists(“Contact”, self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get full name](operations-011.md#op-9c1a54c56a7ce5).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L887) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L839)

<a id="op-831bda092329ff"></a>
### Contact.validate

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Select Google Contacts to which contact should be synced.”.

**Local steps**

- Set self.full\_name from self.\_get\_full\_name().
- Evaluate self.set\_primary\_email().
- Evaluate self.set\_primary(“phone”).
- Evaluate self.set\_primary(“mobile\_no”).
- Evaluate self.set\_user().
- Evaluate set\_link\_title(self).
- Evaluate deduplicate\_dynamic\_links(self).
- Evaluate self.validate\_primary\_contact().
- If (self.get(“sync\_with\_google\_contacts”) and not self.get(“google\_contacts”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“sync\_with\_google\_contacts”) → not self.get(“google\_contacts”).
  - Call the validation error handler Platform.throw(translated “Select Google Contacts to which contact should be synced.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get full name](operations-011.md#op-9c1a54c56a7ce5), [set primary email](operations-011.md#op-081bd5e914646c), [set primary](operations-011.md#op-3dfb8843fac1ec), [set user](operations-010.md#op-ab970173353d32), [validate primary contact](operations-010.md#op-d396a2bb0c1637).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L1136) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L778) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L851)

<a id="op-d396a2bb0c1637"></a>
### Contact.validate primary contact

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_validate_primary_contact`

**Inputs** self.

**Declared result** no value.

**State and service calls** request set\_value on “Contact”.

**Explicit results** no value.

**Local steps**

- If not self.is\_primary\_contact.
  - Return no value.
- Set links from set of tuple(link.link\_doctype, link.link\_name) for link drawn from self.links.
  - Draw link from self.links.
- If not links.
  - Return no value.
- Evaluate self.\_lock\_linked\_documents(links).
- Set primary\_contacts from self.\_get\_linked\_primary\_contacts(links).
- If primary\_contacts.
  - Evaluate Platform.db.set\_value(“Contact”, mapping(“name” → list(“in”, primary\_contacts)), “is\_primary\_contact”, 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [lock linked documents](operations-010.md#op-4f48c93b4b19e2), [get linked primary contacts](operations-010.md#op-6c2d32b3ae6f11).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L1463) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L779) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L852)

<a id="op-4f48c93b4b19e2"></a>
### Contact.lock linked documents

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_dependency_lock_linked_documents`

**Inputs** self, links.

**Declared result** no value.

**Local steps**

- Set links\_by\_doctype from mapping().
- For each tuple(doctype, name) in links.
  - Evaluate links\_by\_doctype.setdefault(doctype, set()).add(name).
- For each tuple(doctype, names) in sorted(links\_by\_doctype.items()).
  - Evaluate Platform.qb.get\_query(doctype, fields = list(“name”), filters = mapping(“name” → list(“in”, sorted(names))), order\_by = “name”, for\_update = true).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L1732) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L840)

<a id="op-6c2d32b3ae6f11"></a>
### Contact.get linked primary contacts

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_get_linked_primary_contacts`

**Inputs** self, links.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).where(nested operand in the contract.parentfield equals “links”).where(link\_filter).run(pluck = true).

**Local steps**

- Set Contact from Platform.qb.DocType(“Contact”).
- Set DynamicLink from Platform.qb.DocType(“Dynamic Link”).
- Set link\_filter from no value.
- For each tuple(doctype, name) in links.
  - Set condition from (DynamicLink.link\_doctype equals doctype bitwise and DynamicLink.link\_name equals name).
  - Set link\_filter from condition when link\_filter is identical to no value, otherwise (link\_filter bitwise or condition).
    - Value choice on link\_filter is identical to no value — true gives condition, false gives (link\_filter bitwise or condition).
- Return nested operand in the contract(nested operand in the contract).where(nested operand in the contract.parentfield equals “links”).where(link\_filter).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L2061) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L843)

<a id="op-ab970173353d32"></a>
### Contact.set user

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_set_user`

**Inputs** self.

**Record and data access** read “User” via get\_value.

**Local steps**

- If (not self.user and self.email\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.user → self.email\_id.
  - Set self.user from Platform.db.get\_value(“User”, mapping(“email” → self.email\_id)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L2647) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L850)

<a id="op-aa7d4916504c2d"></a>
### Contact.get link for

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_get_link_for`

**Inputs** self, link\_doctype.

**Explicit results** link.link\_name · no value.

**Local steps**

- For each link in self.links.
  - If link.link\_doctype equals link\_doctype.
    - Return link.link\_name.
- Return no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L2777) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L842)

<a id="op-cbd5b85c2255d9"></a>
### Contact.has link

`operation_foundation_contacts_record_definitions_contact_business_behavior_contact_has_link`

**Inputs** self, doctype, name.

**Explicit results** true.

**Local steps**

- For each link in self.links.
  - If (link.link\_doctype equals doctype and link.link\_name equals name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals doctype → link.link\_name equals name.
    - Return true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0034.json#L2876) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L846)
