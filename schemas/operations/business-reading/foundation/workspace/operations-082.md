# Forms, reports and navigation · operations 82

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workspace

[Record definition](../../../../data/record-types/workspace.json)

<a id="op-26ad5983b32cc0"></a>
### Workspace.validate duplicate widget labels

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_validate_duplicate_widget_labels`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Duplicate {0} labels: {1}. Labels are used to tell widgets apart when a workspace is saved, so each {0} need …”.format(widget\_label, Platform.bold(“, ”.join(sorted(duplicates)))).

**Local steps**

- If (Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_import or Platform.flags.in\_patch).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_import → Platform.flags.in\_patch.
  - Return no value.
- Set widget\_labels from mapping(“shortcuts” → translated “Shortcut”, “charts” → translated “Chart”, “quick\_lists” → translated “Quick List”, “number\_cards” → translated “Number Card”, …).
- Set before\_save from self.get\_doc\_before\_save().
- For each tuple(parentfield, widget\_label) in widget\_labels.items().
  - Set counts from self.get\_widget\_label\_counts(self, parentfield).
  - Set stored from self.get\_widget\_label\_counts(before\_save, parentfield) when before\_save, otherwise mapping().
    - Value choice on before\_save — true gives self.get\_widget\_label\_counts(before\_save, parentfield), false gives mapping().
  - Set duplicates from set of label for tuple(label, count) drawn from counts.items() where (count &gt; 1 and count &gt; stored.get(label, 0)).
    - Draw tuple(label, count) from counts.items(), keep a combination only if ((count &gt; 1 and count &gt; stored.get(label, 0))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in count &gt; 1 → count &gt; stored.get(label, 0).
  - If duplicates.
    - Call the validation error handler Platform.throw(translated “Duplicate {0} labels: {1}. Labels are used to tell widgets apart when a workspace is saved, so each {0} need …”.format(widget\_label, Platform.bold(“, ”.join(sorted(duplicates)))) ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get widget label counts](operations-081.md#op-85a24cb1a018e3).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L2652) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L895) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1341)

<a id="op-e21947b1667802"></a>
### Workspace.before rename

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_before_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You need to be {0} to rename this document”.format(Platform.bold(“Workspace Manager”)).

**Local steps**

- If (self.public and not is\_workspace\_manager() and not disable\_saving\_as\_public()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.public → not is\_workspace\_manager() → not disable\_saving\_as\_public().
  - Call the validation error handler Platform.throw(translated “You need to be {0} to rename this document”.format(Platform.bold(“Workspace Manager”)), Platform.PermissionError, title = translated “Permission Error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L3331) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1328)

<a id="op-5531c36abb0acf"></a>
### Workspace.clear cache

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_clear_cache`

**Inputs** self.

**Local steps**

- Bind dependencies clear\_computed\_base\_for.
- Evaluate super().clear\_cache().
- Evaluate clear\_computed\_base\_for(self).
- If self.for\_user.
  - Evaluate Platform.cache.hdel(“bootinfo”, self.for\_user).
- Otherwise.
  - Evaluate Platform.cache.delete\_key(“bootinfo”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L3547) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1331)

<a id="op-9c533c9f53c137"></a>
### Workspace.after insert

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_after_insert`

**Inputs** self.

**Local steps**

- If not self.public.
  - Evaluate add\_to\_sidebar(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L33) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L758)

<a id="op-230488dc51e599"></a>
### Workspace.on update

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_on_update`

**Inputs** self.

**Record and data access** read “Module Def” via exists.

**Explicit results** no value.

**Local steps**

- Evaluate self.resettle\_sidebar\_rows().
- Evaluate self.relabel\_sidebar\_rows().
- If disable\_saving\_as\_public().
  - Return no value.
- If self.can\_export().
  - Evaluate self.export\_workspace().
  - If (self.has\_value\_changed(“title”) or self.has\_value\_changed(“module”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.has\_value\_changed(“title”) → self.has\_value\_changed(“module”).
    - Set previous from self.get\_doc\_before\_save().
    - If (previous and previous.get(“module”) and previous.get(“title”) and Platform.db.exists(“Module Def”, previous.get(“module”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous → previous.get(“module”) → previous.get(“title”) → Platform.db.exists(“Module Def”, previous.get(“module”)).
      - Evaluate delete\_folder(previous.get(“module”), “Workspace”, previous.get(“title”)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [resettle sidebar rows](operations-082.md#op-0f9d1c1e758518), [relabel sidebar rows](operations-082.md#op-337d583c4036f7), [can export](operations-082.md#op-a9f51899917aa3), [export workspace](operations-082.md#op-a3568a0b1a3b5a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L47) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1337)

<a id="op-337d583c4036f7"></a>
### Workspace.relabel sidebar rows

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_relabel_sidebar_rows`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies relabel\_workspace\_rows.
- Set previous from self.get\_doc\_before\_save().
- If (not previous or previous.get(“title”) equals self.title).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous → previous.get(“title”) equals self.title.
  - Return no value.
- Evaluate relabel\_workspace\_rows(self.name, self.title).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L37) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L762)

<a id="op-0f9d1c1e758518"></a>
### Workspace.resettle sidebar rows

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_resettle_sidebar_rows`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies remove\_workspace\_rows.
- Set previous from self.get\_doc\_before\_save().
- If (not previous or all(generator of previous.get(field) equals self.get(field) for field drawn from tuple(“module”, “public”, “for\_user”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not previous → all(generator of previous.get(field) equals self.get(field) for field drawn from tuple(“module”, “public”, “for\_user”)).
  - Draw field from tuple(“module”, “public”, “for\_user”).
  - Return no value.
- Evaluate remove\_workspace\_rows(self.name, (previous.get(“for\_user”) or self.for\_user or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous.get(“for\_user”) → self.for\_user → no value.
- Evaluate add\_to\_sidebar(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L38) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L763)

<a id="op-a3568a0b1a3b5a"></a>
### Workspace.export workspace

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_export_workspace`

**Inputs** self.

**Local steps**

- If self.can\_export().
  - Evaluate export\_to\_files(record\_list = list(list(“Workspace”, self.name)), record\_module = self.module).

If control reaches the end, it returns no value.

**Methods declared on this owner** [can export](operations-082.md#op-a9f51899917aa3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L45) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1333)

<a id="op-a9f51899917aa3"></a>
### Workspace.can export

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_can_export`

**Inputs** self.

**Explicit results** bool((Platform.conf.developer\_mode and self.standard and self.module)).

**Local steps**

- Return bool((Platform.conf.developer\_mode and self.standard and self.module)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → self.standard → self.module.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L34) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L759)

<a id="op-9e76d8e31ac24a"></a>
### Workspace.before export

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_before_export`

**Inputs** self, doc.

**Local steps**

- If (doc.title differs from doc.label and doc.label equals doc.name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.title differs from doc.label → doc.label equals doc.name.
  - Set self.name, doc.name, doc.label from doc.title.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L4232) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1327)

<a id="op-3037806988dcde"></a>
### Workspace.on trash

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “You need to be Workspace Manager to delete a public workspace.”.

**Local steps**

- If (self.public and not is\_workspace\_manager()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.public → not is\_workspace\_manager().
  - Call the validation error handler Platform.throw(translated “You need to be Workspace Manager to delete a public workspace.”).
- Evaluate self.delete\_desktop\_icon().
- Evaluate self.drop\_sidebar\_rows().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete desktop icon](operations-082.md#op-91260f01c0e36c), [drop sidebar rows](operations-082.md#op-2c060d91f0da6e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L46) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1336)

<a id="op-2c060d91f0da6e"></a>
### Workspace.drop sidebar rows

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_drop_sidebar_rows`

**Inputs** self.

**Local steps**

- Bind dependencies remove\_workspace\_rows.
- Evaluate remove\_workspace\_rows(self.name, (self.for\_user or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.for\_user → no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L35) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L760)

<a id="op-91260f01c0e36c"></a>
### Workspace.delete desktop icon

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_delete_desktop_icon`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not is\_desktop\_icons\_page().
  - Return no value.
- Evaluate Platform.delete\_doc\_if\_exists(“Desktop Icon”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L4499) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L886) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1332)

<a id="op-3435ebbe56ac58"></a>
### Workspace.after delete

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_after_delete`

**Inputs** self.

**Record and data access** read “Module Def” via exists.

**Explicit results** no value.

**Local steps**

- Evaluate self.keep\_copy\_for\_restore().
- If disable\_saving\_as\_public().
  - Return no value.
- If (self.can\_export() and Platform.db.exists(“Module Def”, self.module)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.can\_export() → Platform.db.exists(“Module Def”, self.module).
  - Evaluate delete\_folder(self.module, “Workspace”, self.title).

If control reaches the end, it returns no value.

**Methods declared on this owner** [keep copy for restore](operations-082.md#op-7967cd0d766c9c), [can export](operations-082.md#op-a9f51899917aa3).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L44) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L880) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1326)

<a id="op-7967cd0d766c9c"></a>
### Workspace.keep copy for restore

`operation_foundation_binding_foundation_desk_doctype_workspace_workspace_workspace_keep_copy_for_restore`

**Inputs** self.

**Record and data access** read “Version” via get\_value · read “Deleted Document” via exists.

**Explicit results** no value.

**Local steps**

- If not Platform.flags.in\_import.
  - Return no value.
- Set last\_edit from Platform.db.get\_value(“Version”, mapping(“ref\_doctype” → “Workspace”, “docname” → self.name), “creation”, order\_by = “creation desc”).
- If not last\_edit.
  - Return no value.
- If Platform.db.exists(“Deleted Document”, mapping(“deleted\_doctype” → “Workspace”, “deleted\_name” → self.name, “creation” → tuple(“&gt;”, last\_edit))).
  - Return no value.
- Bind dependencies add\_to\_deleted\_document.
- Evaluate add\_to\_deleted\_document(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L36) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L785) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L761)

<a id="op-7f45f8c1b281ab"></a>
### Workspace.rename private workspaces

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_rename_private_workspaces`

**Inputs** old\_name, new\_name.

**Wrappers, in declaration order** staticmethod.

**Record and data access** read “Workspace” via get\_all · read “Workspace” via exists.

**State and service calls** request set\_value on “Workspace”.

**Local steps**

- For each workspace in Platform.get\_all(“Workspace”, filters = mapping(“for\_user” → old\_name), fields = list(“name”, “title”), limit = 0).
  - Set new\_label from formatted text {workspace.title}-{new\_name}.
  - If workspace.name differs from new\_label.
    - If Platform.db.exists(“Workspace”, new\_label).
      - Evaluate Platform.db.set\_value(“Workspace”, workspace.name, “for\_user”, new\_name).
      - Continue with the next iteration or loop test.
    - Evaluate rename\_doc(“Workspace”, workspace.name, new\_label, force = true, show\_alert = false, ignore\_permissions = true).
  - Evaluate Platform.db.set\_value(“Workspace”, new\_label, mapping(“for\_user” → new\_name, “label” → new\_label)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L4766) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1339)

<a id="op-c1404556ddb623"></a>
### Workspace.get link groups

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_get_link_groups`

**Inputs** self.

**Explicit results** cards.

**Local steps**

- Set cards from list().
- Set current\_card from Platform.\_dict(mapping(“label” → “Link”, “type” → “Card Break”, “icon” → no value, “hidden” → false)).
- Set card\_links from list().
- For each link in self.links.
  - Set link from link.as\_dict().
  - If link.type equals “Card Break”.
    - If (card\_links and (not current\_card.get(“only\_for”) or current\_card.get(“only\_for”) equals Platform.get\_system\_settings(“country”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in card\_links → (not current\_card.get(“only\_for”) or current\_card.get(“only\_for”) equals Platform.get\_system\_settings(“country”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not current\_card.get(“only\_for”) → current\_card.get(“only\_for”) equals Platform.get\_system\_settings(“country”).
      - Set current\_card at “links” from card\_links.
      - Evaluate cards.append(current\_card).
    - Set current\_card from link.
    - Set card\_links from list().
  - Otherwise.
    - If (not link.get(“only\_for”) or link.get(“only\_for”) equals Platform.get\_system\_settings(“country”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not link.get(“only\_for”) → link.get(“only\_for”) equals Platform.get\_system\_settings(“country”).
      - Evaluate card\_links.append(link).
- Set current\_card at “links” from card\_links.
- Evaluate cards.append(current\_card).
- Return cards.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“country”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L5224) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1334)

<a id="op-a24a098f5576d7"></a>
### Workspace.build links table from card

`operation_foundation_desk_record_definitions_workspace_business_behavior_workspace_build_links_table_from_card`

**Inputs** self, config.

**Local steps**

- For each tuple(idx, card) in enumerate(config).
  - Set links from loads(card.get(“links”)).
  - For each tuple(idx, link) in enumerate(self.links).
    - If (link.get(“label”) equals card.get(“label”) and link.get(“type”) equals “Card Break”).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.get(“label”) equals card.get(“label”) → link.get(“type”) equals “Card Break”.
      - If link.link\_count equals 0.
        - For each tuple(count, card\_link) in enumerate(self.links at slice (idx + 1) to no value).
          - If card\_link.get(“type”) equals “Card Break”.
            - Leave the innermost loop without its normal-exhaustion alternative.
          - Set link.link\_count from (count + 1).
      - Remove self.links at slice idx to ((idx + link.link\_count) + 1).
  - Evaluate self.append(“links”, mapping(“label” → card.get(“label”), “type” → “Card Break”, “icon” → card.get(“icon”), “description” → card.get(“description”), …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in card.get(“hidden”) → false.
    - Value choice on not self.links — true gives 1, false gives (self.links at negative 1.idx + 1).
  - For each link in links.
    - Evaluate self.append(“links”, mapping(“label” → link.get(“label”), “type” → “Link”, “link\_type” → link.get(“link\_type”), “link\_to” → link.get(“link\_to”), …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L5800) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L884) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1330)

<a id="op-1c9dbcc5fdc0eb"></a>
### Disable saving as public

`operation_foundation_desk_record_definitions_workspace_business_behavior_disable_saving_as_public`

**Inputs** no declared parameters.

**Explicit results** (Platform.flags.in\_install or Platform.flags.in\_uninstall or Platform.flags.in\_patch or Platform.in\_test or Platform.flags.in\_fixtures or Platform.flags.in\_migrate).

**Local steps**

- Return (Platform.flags.in\_install or Platform.flags.in\_uninstall or Platform.flags.in\_patch or Platform.in\_test or Platform.flags.in\_fixtures or Platform.flags.in\_migrate).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_install → Platform.flags.in\_uninstall → Platform.flags.in\_patch → Platform.in\_test → Platform.flags.in\_fixtures → Platform.flags.in\_migrate.

[Applicable decision contract](../../../foundation-decision-contracts/part-0193.json#L6937) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1301)

<a id="op-4ce12cbe13468d"></a>
### Module page

`operation_foundation_desk_record_definitions_workspace_business_behavior_module_page`

**Inputs** module.

**Declared result** (Platform.\_dict bitwise or no value).

**Record and data access** read “Workspace” via get\_value.

**Explicit results** Platform.db.get\_value(“Workspace”, module, list(“name”, “module”), as\_dict = true).

**Local steps**

- Return Platform.db.get\_value(“Workspace”, module, list(“name”, “module”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L869) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1315)

<a id="op-2862d379bbb785"></a>
### Module name is free

`operation_foundation_desk_record_definitions_workspace_business_behavior_module_name_is_free`

**Inputs** module.

**Declared result** bool.

**Record and data access** read “Module Def” via exists.

**Explicit results** false · (page is identical to no value or page.module equals module).

**Local steps**

- If Platform.db.exists(“Module Def”, module).
  - Return false.
- Set page from module\_page(module).
- Return (page is identical to no value or page.module equals module).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in page is identical to no value → page.module equals module.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L121) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L868) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1314)

<a id="op-e32562cb039622"></a>
### Sanitize content

`operation_foundation_desk_record_definitions_workspace_business_behavior_sanitize_content`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** content.

**Explicit result forms** a value selected from the current context, the result of a delegated call.

**Local structure** 1 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L277) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L871) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1317)

<a id="op-f7a3698bbf8174"></a>
### Sanitize strings

`operation_foundation_desk_record_definitions_workspace_business_behavior_sanitize_strings`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** value.

**Explicit result forms** a structured result, a value selected from the current context, the result of a delegated call.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L477) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L872) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1318)

<a id="op-34557abdfdda41"></a>
### Welcome blocks

`operation_foundation_desk_record_definitions_workspace_business_behavior_welcome_blocks`

**Inputs** title.

**Declared result** list at dict.

**Explicit results** list(mapping(“type” → “header”, “data” → mapping(“text” → translated “Welcome to the {0} workspace”.format(title))), mapping(“type” → “paragraph”, “data” → mapping(“text” → translated “Click on the {0} men ….

**Local steps**

- Return list(mapping(“type” → “header”, “data” → mapping(“text” → translated “Welcome to the {0} workspace”.format(title))), mapping(“type” → “paragraph”, “data” → mapping(“text” → translated “Click on the {0} men ….

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0194.json#L714) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L1325)
