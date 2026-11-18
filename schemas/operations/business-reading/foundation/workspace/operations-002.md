# Forms, reports and navigation · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Activity

<a id="op-16d994e435085b"></a>
### Get version activities

`operation_foundation_desk_form_activity_business_behavior_get_version_activities`

**Inputs** doc, user\_info, allowed\_fields = no value.

**Declared result** list at dict.

**Explicit results** list() · result.

**Local steps**

- Set versions from get\_versions(doc).
- If not versions.
  - Return list().
- Set doctype from doc.doctype.
- Set meta from doc.meta.
- Set permitted from readable\_permlevels(meta).
- Evaluate Platform.utils.add\_user\_info(set of v.owner for v drawn from versions where v.owner, user\_info).
  - Draw v from versions, keep a combination only if (v.owner).
- Set child\_cache from mapping().
- Set result from list().
- For each v in versions.
  - Set data from json.loads((v.data or “{}”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in v.data → “{}”.
  - Set changes from list().
  - For each tuple(fieldname, old, new) in data.get(“changed”, list()).
    - If fieldname equals “docstatus”.
      - If new equals 1.
        - Evaluate changes.append(format\_phrase\_change(translated “submitted this document”)).
      - Otherwise.
        - If new equals 2.
          - Evaluate changes.append(format\_phrase\_change(translated “cancelled this document”)).
      - Continue with the next iteration or loop test.
    - Set df from is\_field\_visible(meta, permitted, fieldname).
    - If not df.
      - Continue with the next iteration or loop test.
    - Evaluate changes.append(format\_version\_change(df, fieldname, old, new)).
  - Evaluate changes.extend(get\_child\_table\_changes(data, doctype, meta, permitted, …)).
  - If allowed\_fields is distinct from no value.
    - Set changes from list of c for c drawn from changes where c.get(“fieldname”) belongs to allowed\_fields.
      - Draw c from changes, keep a combination only if (c.get(“fieldname”) belongs to allowed\_fields).
  - Set author from get\_author\_info(v.owner, user\_info).
  - For each tuple(idx, change) in enumerate(changes).
    - Set change at “name” from formatted text {v.name}-{idx}.
    - Evaluate result.append(mapping(“type” → “version”, “key” → formatted text version:{v.name}-{idx}, “timestamp” → str(v.creation), “author” → author, …)).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L828) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1657) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L142)

<a id="op-32d29e49da5f83"></a>
### Format version change

`operation_foundation_desk_form_activity_business_behavior_format_version_change`

**Inputs** df, fieldname, old, new.

**Declared result** dict.

**Explicit results** mapping(“fieldname” → fieldname, “type” → “phrase”, “text” → translated “updated {0}”.format(label)) · mapping(“fieldname” → fieldname, “type” → “phrase”, “text” → translated “cleared {0}”.format(label)) · mapping(“fieldname” → fieldname, “type” → “diff”, “prefix” → translated “changed {0}”.format(label), “from” → old\_s, …) · mapping(“fieldname” → fieldname, “type” → “diff”, “prefix” → translated “set {0} to”.format(label), “to” → new\_s).

**Local steps**

- Set label from translated (df.label or fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → fieldname.
- Set old\_s from display\_value(old).
- Set new\_s from display\_value(new).
- If df.fieldtype belongs to LONG\_TEXT\_FIELDTYPES.
  - Return mapping(“fieldname” → fieldname, “type” → “phrase”, “text” → translated “updated {0}”.format(label)).
- If (old\_s and not new\_s).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_s → not new\_s.
  - Return mapping(“fieldname” → fieldname, “type” → “phrase”, “text” → translated “cleared {0}”.format(label)).
- If old\_s.
  - Return mapping(“fieldname” → fieldname, “type” → “diff”, “prefix” → translated “changed {0}”.format(label), “from” → old\_s, …).
- Return mapping(“fieldname” → fieldname, “type” → “diff”, “prefix” → translated “set {0} to”.format(label), “to” → new\_s).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L1958) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1642) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L127)

<a id="op-c967d6094c6a83"></a>
### Format phrase change

`operation_foundation_desk_form_activity_business_behavior_format_phrase_change`

**Inputs** text, fieldname = no value.

**Declared result** dict.

**Explicit results** mapping(“fieldname” → fieldname, “type” → “phrase”, “text” → text).

**Local steps**

- Return mapping(“fieldname” → fieldname, “type” → “phrase”, “text” → text).

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L2547) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1641) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L126)

<a id="op-4497ac9004d12d"></a>
### Get child table changes

`operation_foundation_desk_form_activity_business_behavior_get_child_table_changes`

**Inputs** data, doctype, meta, permitted, child\_cache.

**Declared result** list at dict.

**Explicit results** changes.

**Local steps**

- Set changes from list().
- For each tuple(key, template) in tuple(tuple(“added”, translated “added {0} row(s) to {1}”), tuple(“removed”, translated “removed {0} row(s) from {1}”)).
  - Set counts from mapping().
  - For each tuple(table\_fieldname, \_row) in data.get(key, list()).
    - Set counts at table\_fieldname from (counts.get(table\_fieldname, 0) + 1).
  - For each tuple(table\_fieldname, count) in counts.items().
    - Set df from is\_field\_visible(meta, permitted, table\_fieldname).
    - If not df.
      - Continue with the next iteration or loop test.
    - Evaluate changes.append(format\_phrase\_change(template.format(count, translated (df.label or table\_fieldname)), fieldname = table\_fieldname)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.label → table\_fieldname.
- For each entry in data.get(“row\_changed”, list()).
  - Set tuple(table\_fieldname, row\_index, \_row\_name, child\_changes) from entry.
  - Set df from is\_field\_visible(meta, permitted, table\_fieldname).
  - If not df.
    - Continue with the next iteration or loop test.
  - Set child\_dt from df.options.
  - If child\_dt does not belong to child\_cache.
    - Set child\_meta from Platform.get\_meta(child\_dt).
    - Set child\_cache at child\_dt from tuple(readable\_permlevels(child\_meta, parenttype = doctype), child\_meta).
  - Set tuple(child\_permitted, child\_meta) from child\_cache at child\_dt.
  - For each tuple(cfield, \_cold, cnew) in child\_changes.
    - Set cdf from is\_field\_visible(child\_meta, child\_permitted, cfield).
    - If not cdf.
      - Continue with the next iteration or loop test.
    - Evaluate changes.append(format\_phrase\_change(translated “set {0} to {1} in row #{2}”.format(translated (cdf.label or cfield), truncate\_value(cnew), (row\_index + 1)), fieldname = table\_fieldname)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in cdf.label → cfield.
- Return changes.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L2658) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1646) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L131)

<a id="op-781a7c055aae69"></a>
### Readable permlevels

`operation_foundation_desk_form_activity_business_behavior_readable_permlevels`

**Inputs** meta, parenttype = no value.

**Declared result** (set at int bitwise or no value).

**Explicit results** no value · levels.

**Local steps**

- If not meta.get\_permissions(parenttype).
  - Return no value.
- Set levels from set(meta.get\_permlevel\_access(“read”, parenttype, user = Platform.session.user)).
- If (0 does not belong to levels and Platform.share.get\_shared((parenttype or meta.name), Platform.session.user, rights = list(“read”), limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in 0 does not belong to levels → Platform.share.get\_shared((parenttype or meta.name), Platform.session.user, rights = list(“read”), limit = 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parenttype → meta.name.
  - Evaluate levels.add(0).
- Return levels.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L3625) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L148)

<a id="op-369edefa7a81ff"></a>
### Is field visible

`operation_foundation_desk_form_activity_business_behavior_is_field_visible`

**Inputs** meta, permlevels, fieldname.

**Explicit results** no value · df.

**Local steps**

- Set df from meta.get\_field(fieldname).
- If (not df or (df.hidden and not df.show\_on\_timeline)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → (df.hidden and not df.show\_on\_timeline).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.hidden → not df.show\_on\_timeline.
  - Return no value.
- If (permlevels is distinct from no value and df.permlevel does not belong to permlevels).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in permlevels is distinct from no value → df.permlevel does not belong to permlevels.
  - Return no value.
- Return df.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L3942) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1659) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L144)

<a id="op-8ce708459de357"></a>
### Display value

`operation_foundation_desk_form_activity_business_behavior_display_value`

**Inputs** value.

**Declared result** str.

**Explicit results** empty text · Platform.utils.strip\_html(str(value)).strip().

**Local steps**

- If (value is identical to no value or value equals empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value is identical to no value → value equals empty text.
  - Return empty text.
- Return Platform.utils.strip\_html(str(value)).strip().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L4148) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1640) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L125)

<a id="op-eaa35caeba420d"></a>
### Truncate value

`operation_foundation_desk_form_activity_business_behavior_truncate_value`

**Inputs** value.

**Declared result** str.

**Explicit results** empty text · (s at slice no value to 40 + “…”) when len(s) &gt; 40, otherwise s.

**Local steps**

- If (value is identical to no value or value equals empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value is identical to no value → value equals empty text.
  - Return empty text.
- Set s from Platform.utils.strip\_html(str(value)).
- Return (s at slice no value to 40 + “…”) when len(s) &gt; 40, otherwise s.
  - Value choice on len(s) &gt; 40 — true gives (s at slice no value to 40 + “…”), false gives s.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0197.json#L4281) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L149)

## Record · Address

[Record definition](../../../../data/record-types/address.json)

<a id="op-53819d65f3deef"></a>
### Address.setup

`operation_foundation_contacts_record_definitions_address_business_behavior_address_setup`

**Inputs** self.

**Local steps**

- Set self.flags.linked from false.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L6474) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L728) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L801)

<a id="op-e904173ebf97d4"></a>
### Address.autoname

`operation_foundation_contacts_record_definitions_address_business_behavior_address_autoname`

**Inputs** self.

**Record and data access** read “Address” via exists.

**Local steps**

- If (not self.address\_title and self.links).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.address\_title → self.links.
  - Set self.address\_title from (self.links at 0.link\_title or self.links at 0.link\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.links at 0.link\_title → self.links at 0.link\_name.
- If self.address\_title.
  - Set self.name from ((cstr(self.address\_title).strip() + “-”) + cstr(translated self.address\_type).strip()).
  - If Platform.db.exists(“Address”, self.name).
    - Set self.name from make\_autoname((((nested operand in the contract(nested operand in the contract).strip() + “-”) + cstr(nested operand in the contract.address\_type).strip()) + “-.#”), ignore\_validate = true).
- Otherwise.
  - Evaluate throw(translated “Address Title is mandatory.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L6525) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L722) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L795)

<a id="op-c844238eb4995c"></a>
### Address.validate

`operation_foundation_contacts_record_definitions_address_business_behavior_address_validate`

**Inputs** self.

**Local steps**

- Evaluate self.link\_address().
- Evaluate self.validate\_preferred\_address().
- Evaluate set\_link\_title(self).
- Evaluate deduplicate\_dynamic\_links(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [link address](operations-002.md#op-f8e78dbbef2530), [validate preferred address](operations-002.md#op-7b5b8e73770704).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L6967) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L729) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L802)

<a id="op-f8e78dbbef2530"></a>
### Address.link address

`operation_foundation_contacts_record_definitions_address_business_behavior_address_link_address`

**Inputs** self.

**Record and data access** read “Contact” via get\_value · resolve a document from “Contact” via get\_cached\_doc.

**Explicit results** true · false.

**Local steps**

- If not self.links.
  - Set contact\_name from Platform.db.get\_value(“Contact”, mapping(“email\_id” → self.owner)).
  - If contact\_name.
    - Set contact from Platform.get\_cached\_doc(“Contact”, contact\_name).
    - For each link in contact.links.
      - Evaluate self.append(“links”, dict(link\_doctype = link.link\_doctype, link\_name = link.link\_name)).
    - Return true.
- Return false.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Contact”, contact\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L7080) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L726) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L799)

<a id="op-7b5b8e73770704"></a>
### Address.validate preferred address

`operation_foundation_contacts_record_definitions_address_business_behavior_address_validate_preferred_address`

**Inputs** self.

**Local steps**

- Set preferred\_fields from list(“is\_primary\_address”, “is\_shipping\_address”).
- For each field in preferred\_fields.
  - If self.get(field).
    - For each link in self.links.
      - Set address from get\_preferred\_address(link.link\_doctype, link.link\_name, field).
      - If address.
        - Evaluate update\_preferred\_address(address, field).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L7339) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L730) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L803)

<a id="op-5b5c90c77178e4"></a>
### Address.get display

`operation_foundation_contacts_record_definitions_address_business_behavior_address_get_display`

**Inputs** self.

**Explicit results** get\_address\_display(self.as\_dict()).

**Local steps**

- Return get\_address\_display(self.as\_dict()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L7541) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L723) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L796)

<a id="op-c971baf32ee38b"></a>
### Address.has link

`operation_foundation_contacts_record_definitions_address_business_behavior_address_has_link`

**Inputs** self, doctype, name.

**Explicit results** true.

**Local steps**

- For each link in self.links.
  - If (link.link\_doctype equals doctype and link.link\_name equals name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals doctype → link.link\_name equals name.
    - Return true.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L7605) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L725) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L798)

<a id="op-a1c8a20d1a14b4"></a>
### Address.has common link

`operation_foundation_contacts_record_definitions_address_business_behavior_address_has_common_link`

**Inputs** self, doc.

**Explicit results** true · false.

**Local steps**

- Set reference\_links from list of tuple(link.link\_doctype, link.link\_name) for link drawn from doc.links.
  - Draw link from doc.links.
- For each link in self.links.
  - If tuple(link.link\_doctype, link.link\_name) belongs to reference\_links.
    - Return true.
- Return false.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L724) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L797)

<a id="op-2cf668abfbe090"></a>
### Get preferred address

`operation_foundation_contacts_record_definitions_address_business_behavior_get_preferred_address`

**Inputs** doctype, name, preferred\_key = “is\_primary\_address”.

**Record and data access** execute query text (SELECT, Address).format(“%s”, “%s”, preferred\_key, “%s”).

**Explicit results** address at 0.name · no value.

**Local steps**

- If preferred\_key belongs to list(“is\_shipping\_address”, “is\_primary\_address”).
  - Set address from Platform.db.sql(query text (SELECT, Address).format(“%s”, “%s”, preferred\_key, “%s”), tuple(doctype, name, 1), as\_dict = 1).
  - If address.
    - Return address at 0.name.
- Return no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L167) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L741) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L814)

<a id="op-1d592ec6110329"></a>
### Get default address

`operation_foundation_contacts_record_definitions_address_business_behavior_get_default_address`

**Inputs** doctype, name, sort\_key = “is\_primary\_address”.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Record and data access** read “Address” via get\_all.

**Explicit results** no value · addresses at 0 when addresses, otherwise no value.

**Local steps**

- If sort\_key does not belong to list(“is\_shipping\_address”, “is\_primary\_address”).
  - Return no value.
- Set addresses from Platform.get\_all(“Address”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, name), list(“disabled”, “=”, 0)), pluck = “name”, order\_by = formatted  ….
- Return addresses at 0 when addresses, otherwise no value.
  - Value choice on addresses — true gives addresses at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L391) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L738) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L811)

<a id="op-c20ff053680116"></a>
### Get address display

`operation_foundation_contacts_record_definitions_address_business_behavior_get_address_display`

**Inputs** address\_dict.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** (str bitwise or no value).

**Explicit results** render\_address(address\_dict).

**Local steps**

- Return render\_address(address\_dict).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L746) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L731) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L804)

<a id="op-d7a8bd5589d1e9"></a>
### Render address

`operation_foundation_contacts_record_definitions_address_business_behavior_render_address`

**Inputs** address, check\_permissions = true, address\_template = no value.

**Declared result** (str bitwise or no value).

**Record and data access** resolve a document from “Address” via get\_cached\_doc.

**Explicit results** no value · Platform.render\_template(template, address, restrict\_globals = true).

**Explicit failure paths** validation helper — translated “There is an error in your Address Template {0}”.format(name).

**Local steps**

- If not address.
  - Return no value.
- If not isinstance(address, dict).
  - Set address from Platform.get\_cached\_doc(“Address”, address).
  - If check\_permissions.
    - Evaluate address.check\_permission().
  - Set address from address.as\_dict().
- Set tuple(name, template) from (address\_template or get\_address\_templates(address)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in address\_template → get\_address\_templates(address).
- Attempt the following.
  - Return Platform.render\_template(template, address, restrict\_globals = true).
- On failure (TemplateSyntaxError).
  - Call the validation error handler Platform.throw(translated “There is an error in your Address Template {0}”.format(name)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Address”, address) · effective access from address.check\_permission().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L849) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L744) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L817)

<a id="op-833c7282ff0941"></a>
### Get territory from address

`operation_foundation_contacts_record_definitions_address_business_behavior_get_territory_from_address`

**Inputs** address.

**Record and data access** resolve a document from “Address” via get\_cached\_doc · read “Territory” via get\_value.

**Explicit results** no value · territory.

**Local steps**

- If not address.
  - Return no value.
- If isinstance(address, str).
  - Set address from Platform.get\_cached\_doc(“Address”, address).
- Set territory from no value.
- For each fieldname in tuple(“city”, “state”, “country”).
  - If address.get(fieldname).
    - Set territory from Platform.db.get\_value(“Territory”, address.get(fieldname)).
    - If territory.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return territory.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Address”, address).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L1236) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L742) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L815)

<a id="op-9c69ed97672ad3"></a>
### Get list context

`operation_foundation_contacts_record_definitions_address_business_behavior_get_list_context`

**Inputs** context = no value.

**Explicit results** context.

**Local steps**

- Set context from (context or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → Platform.\_dict().
- Evaluate context.update(mapping(“title” → translated “Addresses”, “get\_list” → get\_address\_list, “list\_template” → “templates/includes/list/list.html”, “row\_template” → “templates/includes/address\_row.html”, …)).
- Return context.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L1509) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L740) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L813)

<a id="op-480c5431aa757a"></a>
### Get address list

`operation_foundation_contacts_record_definitions_address_business_behavior_get_address_list`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, order\_by = no value.

**Explicit results** addresses.

**Local steps**

- Bind dependencies get\_list.
- Set user from Platform.session.user.
- If not filters.
  - Set filters from list().
- Attempt the following.
  - Set filters at “owner” from user.
- On failure (TypeError).
  - Evaluate filters.append(tuple(“Address”, “owner”, “=”, user)).
- Set addresses from get\_list(doctype, txt, filters, limit\_start, …).
- Set tuple(address\_templates, default\_template) from get\_address\_template\_map(addresses).
- For each address in addresses.
  - Set address.address\_display from render\_address(address, address\_template = (address\_templates.get(address.get(“country”)) or default\_template)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in address\_templates.get(address.get(“country”)) → default\_template.
- Return addresses.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L1683) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L733) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L806)

<a id="op-4de28d45781c6d"></a>
### Has website permission

`operation_foundation_contacts_record_definitions_address_business_behavior_has_website_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user, verbose.

**Explicit result forms** Boolean false, the result of a delegated call.

**Observed service boundaries** record lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L2098) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L743) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L816)
