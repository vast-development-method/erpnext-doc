# Forms, reports and navigation · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Address

[Record definition](../../../../data/record-types/address.json)

<a id="op-2f5289c4d86c97"></a>
### Get address templates

`operation_foundation_contacts_record_definitions_address_business_behavior_get_address_templates`

**Inputs** address.

**Record and data access** read “Address Template” via get\_value.

**Explicit results** result.

**Local steps**

- Set result from Platform.db.get\_value(“Address Template”, mapping(“country” → address.get(“country”)), list(“name”, “template”)).
- If not result.
  - Set result from get\_default\_address\_template().
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L2299) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L735) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L808)

<a id="op-86ebb2638f780c"></a>
### Get default address template

`operation_foundation_contacts_record_definitions_address_business_behavior_get_default_address_template`

**Inputs** no declared parameters.

**Record and data access** read “Address Template” via get\_value.

**Explicit results** result.

**Explicit failure paths** validation helper — translated “No default Address Template found. Please create a new one from Setup &gt; Printing and Branding &gt; Address Template.”.

**Local steps**

- Set result from Platform.db.get\_value(“Address Template”, mapping(“is\_default” → 1), list(“name”, “template”)).
- If not result.
  - Call the validation error handler Platform.throw(translated “No default Address Template found. Please create a new one from Setup &gt; Printing and Branding &gt; Address Template.”).
- Return result.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L2477) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L739) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L812)

<a id="op-921152eefa8f9d"></a>
### Get address template map

`operation_foundation_contacts_record_definitions_address_business_behavior_get_address_template_map`

**Inputs** addresses.

**Record and data access** read “Address Template” via get\_all.

**Explicit results** tuple(mapping(), no value) · tuple(address\_templates, default\_template).

**Local steps**

- If not addresses.
  - Return tuple(mapping(), no value).
- Set countries from set of address.get(“country”) for address drawn from addresses where address.get(“country”).
  - Draw address from addresses, keep a combination only if (address.get(“country”)).
- Set has\_missing\_country from any(generator of not address.get(“country”) for address drawn from addresses).
  - Draw address from addresses.
- Set address\_templates from mapping().
- If countries.
  - Set address\_templates from mapping of template.country → tuple(template.name, template.template) for template drawn from Platform.get\_all(“Address Template”, filters = mapping(“country” → tuple(“in”, tuple(countries))), fields = lis ….
    - Draw template from Platform.get\_all(“Address Template”, filters = mapping(“country” → tuple(“in”, tuple(countries))), fields = list(“country”, “name”, “template”)).
- Set default\_template from no value.
- If (len(address\_templates) &lt; len(countries) or has\_missing\_country).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(address\_templates) &lt; len(countries) → has\_missing\_country.
  - Set default\_template from get\_default\_address\_template().
- Return tuple(address\_templates, default\_template).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L2643) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L734) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L807)

<a id="op-215be89ee33ba2"></a>
### Get company address

`operation_foundation_contacts_record_definitions_address_business_behavior_get_company_address`

**Inputs** company.

**Explicit results** ret.

**Local steps**

- Set ret from Platform.\_dict().
- If company.
  - Set ret.company\_address from get\_default\_address(“Company”, company).
  - Set ret.company\_address\_display from render\_address(ret.company\_address, check\_permissions = false).
- Return ret.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L3142) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L736) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L809)

<a id="op-832f7d3530f6b2"></a>
### Address query

`operation_foundation_contacts_record_definitions_address_business_behavior_address_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Dynamic Link” via get\_all.

**Explicit results** search\_widget(“Address”, txt, filters = \_filters, searchfield = searchfield, start = start, page\_length = page\_len).

**Local steps**

- Bind dependencies search\_widget.
- Set link\_filters from mapping(“parenttype” → “Address”).
- If link\_doctype bound to filters.pop(“link\_doctype”, no value).
  - Set link\_filters at “link\_doctype” from link\_doctype.
- If link\_name bound to filters.pop(“link\_name”, no value).
  - Set link\_filters at “link\_name” from link\_name.
- Set \_filters from list of list(key, “=”, value) for tuple(key, value) drawn from filters.items().
  - Draw tuple(key, value) from filters.items().
- If (link\_doctype or link\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_doctype → link\_name.
  - Set linked\_addresses from Platform.get\_all(“Dynamic Link”, filters = link\_filters, pluck = “parent”).
  - Evaluate \_filters.append(list(“name”, “in”, linked\_addresses)).
- Return search\_widget(“Address”, txt, filters = \_filters, searchfield = searchfield, start = start, page\_length = page\_len).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L151) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L727) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L800)

<a id="op-6c05bc4311978b"></a>
### Get condensed address

`operation_foundation_contacts_record_definitions_address_business_behavior_get_condensed_address`

**Inputs** doc, no\_title = false.

**Explicit results** “, ”.join(generator of doc.get(d) for d drawn from fields where doc.get(d)).

**Local steps**

- Set fields from list(“address\_title”, “address\_line1”, “address\_line2”, “city”, …).
- If no\_title.
  - Evaluate fields.remove(“address\_title”).
- Return “, ”.join(generator of doc.get(d) for d drawn from fields where doc.get(d)).
  - Draw d from fields, keep a combination only if (doc.get(d)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L3781) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L737) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L810)

<a id="op-05fee52a59802e"></a>
### Update preferred address

`operation_foundation_contacts_record_definitions_address_business_behavior_update_preferred_address`

**Inputs** address, field.

**State and service calls** request set\_value on “Address”.

**Local steps**

- Evaluate Platform.db.set\_value(“Address”, address, field, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L4015) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L745) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L818)

<a id="op-2e97613443079b"></a>
### Get address display list

`operation_foundation_contacts_record_definitions_address_business_behavior_get_address_display_list`

**Inputs** doctype, name.

**Declared result** list at dict.

**Record and data access** read “Address” via get\_list.

**Explicit results** list() · address\_list.

**Local steps**

- If not Platform.has\_permission(“Address”, “read”).
  - Return list().
- Set address\_list from Platform.get\_list(“Address”, filters = list(list(“Dynamic Link”, “link\_doctype”, “=”, doctype), list(“Dynamic Link”, “link\_name”, “=”, name), list(“Dynamic Link”, “parenttype”, “=”, “Address”)), fields = l ….
- For each a in address\_list.
  - Set a at “display” from get\_address\_display(a).
- Return address\_list.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Address”, “read”).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L4097) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L732) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L805)

## Service · Address and contact

<a id="op-a03cb344f3363e"></a>
### Load address and contact

`operation_foundation_contacts_address_and_contact_business_behavior_load_address_and_contact`

**Inputs** doc, key = no value.

**Declared result** no value.

**Local steps**

- Bind dependencies get\_address\_display\_list.
- Bind dependencies get\_contact\_display\_list.
- Evaluate doc.set\_onload(“addr\_list”, get\_address\_display\_list(doc.doctype, doc.name)).
- Evaluate doc.set\_onload(“contact\_list”, get\_contact\_display\_list(doc.doctype, doc.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L2695) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L719) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L792)

<a id="op-750bb88162357f"></a>
### Remove link

`operation_foundation_contacts_address_and_contact_business_behavior_remove_link`

**Inputs** doctype, name, link\_doctype, link\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** no value.

**Record and data access** resolve a document from doctype via get\_doc.

**State and service calls** call save on doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Can only unlink an Address or a Contact”.

**Local steps**

- If doctype does not belong to tuple(“Address”, “Contact”).
  - Call the validation error handler Platform.throw(translated “Can only unlink an Address or a Contact”).
- Set doc from Platform.get\_doc(doctype, name).
- Evaluate doc.check\_permission(“write”).
- Set remaining from list of link for link drawn from doc.links where not (link.link\_doctype equals link\_doctype and link.link\_name equals link\_name).
  - Draw link from doc.links, keep a combination only if (not (link.link\_doctype equals link\_doctype and link.link\_name equals link\_name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals link\_doctype → link.link\_name equals link\_name.
- If len(remaining) equals len(doc.links).
  - Return no value.
- Set doc.links from remaining.
- Evaluate doc.save().
- Evaluate clear\_stale\_primary\_link(doctype, name, link\_doctype, link\_name).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L2866) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L720) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L793)

<a id="op-a4192eec910487"></a>
### Clear stale primary link

`operation_foundation_contacts_address_and_contact_business_behavior_clear_stale_primary_link`

**Inputs** doctype, name, link\_doctype, link\_name.

**Declared result** no value.

**Record and data access** read link\_doctype via get\_value.

**State and service calls** request set\_value on link\_doctype.

**Explicit results** no value.

**Local steps**

- Set meta from Platform.get\_meta(link\_doctype).
- Set primary\_fields from list of df.fieldname for df drawn from get\_primary\_link\_fields(meta, doctype).
  - Draw df from get\_primary\_link\_fields(meta, doctype).
- If not primary\_fields.
  - Return no value.
- Set values from (Platform.db.get\_value(link\_doctype, link\_name, primary\_fields, as\_dict = true) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(link\_doctype, link\_name, primary\_fields, as\_dict = true) → mapping().
- Set stale\_fields from list of fieldname for fieldname drawn from primary\_fields where values.get(fieldname) equals name.
  - Draw fieldname from primary\_fields, keep a combination only if (values.get(fieldname) equals name).
- If not stale\_fields.
  - Return no value.
- Evaluate Platform.has\_permission(link\_doctype, “write”, doc = link\_name, throw = true).
- Set updates from dict.fromkeys(stale\_fields).
- For each df in meta.fields.
  - If (df.fetch\_from and df.fetch\_from.split(“.”) at 0 belongs to stale\_fields).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fetch\_from → df.fetch\_from.split(“.”) at 0 belongs to stale\_fields.
    - Set updates at df.fieldname from no value.
- Evaluate Platform.db.set\_value(link\_doctype, link\_name, updates).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(link\_doctype, “write”, doc = link\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L3307) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L710) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L783)

<a id="op-10c372b98e7f8a"></a>
### Get primary link fields

`operation_foundation_contacts_address_and_contact_business_behavior_get_primary_link_fields`

**Inputs** meta, doctype.

**Declared result** list.

**Explicit results** list of df for df drawn from meta.get(“fields”, mapping(“fieldtype” → “Link”, “options” → doctype)) where “primary” belongs to df.fieldname.lower().

**Local steps**

- Return list of df for df drawn from meta.get(“fields”, mapping(“fieldtype” → “Link”, “options” → doctype)) where “primary” belongs to df.fieldname.lower().
  - Draw df from meta.get(“fields”, mapping(“fieldtype” → “Link”, “options” → doctype)), keep a combination only if (“primary” belongs to df.fieldname.lower()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L3851) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L717) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L790)

<a id="op-3baf85ca41fdfd"></a>
### Has permission

`operation_foundation_contacts_address_and_contact_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true.

**Observed service boundaries** effective access lookup.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L4011) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L718) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L791)

<a id="op-1d49152a174a2d"></a>
### Get permission query conditions for contact

`operation_foundation_contacts_address_and_contact_business_behavior_get_permission_query_conditions_for_contact`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L4364) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L715) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L788)

<a id="op-81a1ac80d09adc"></a>
### Get permission query conditions for address

`operation_foundation_contacts_address_and_contact_business_behavior_get_permission_query_conditions_for_address`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L4421) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L714) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L787)

<a id="op-51b2632555beb7"></a>
### Get permission query conditions

`operation_foundation_contacts_address_and_contact_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L4478) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L713) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L786)

<a id="op-ca197e111dde39"></a>
### Get permitted and not permitted links

`operation_foundation_contacts_address_and_contact_business_behavior_get_permitted_and_not_permitted_links`

**Inputs** doctype.

**Explicit results** mapping(“permitted\_links” → permitted\_links, “not\_permitted\_links” → not\_permitted\_links).

**Local steps**

- Set permitted\_links from list().
- Set not\_permitted\_links from list().
- Set meta from Platform.get\_meta(doctype).
- Set allowed\_doctypes from Platform.permissions.get\_doctypes\_with\_read().
- For each df in meta.get\_link\_fields().
  - If df.options does not belong to tuple(“Customer”, “Supplier”, “Company”, “Sales Partner”).
    - Continue with the next iteration or loop test.
  - If df.options belongs to allowed\_doctypes.
    - Evaluate permitted\_links.append(df).
  - Otherwise.
    - Evaluate not\_permitted\_links.append(df).
- Return mapping(“permitted\_links” → permitted\_links, “not\_permitted\_links” → not\_permitted\_links).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L4852) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L716) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L789)

<a id="op-92f5ff544fc468"></a>
### Delete contact and address

`operation_foundation_contacts_address_and_contact_business_behavior_delete_contact_and_address`

**Inputs** doctype, docname.

**Declared result** no value.

**Record and data access** read “Dynamic Link” via get\_all · resolve a document from parenttype via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- For each parenttype in tuple(“Contact”, “Address”).
  - For each name in Platform.get\_all(“Dynamic Link”, filters = mapping(“parenttype” → parenttype, “link\_doctype” → doctype, “link\_name” → docname), pluck = “parent”).
    - Set doc from Platform.get\_doc(parenttype, name).
    - If len(doc.links) equals 1.
      - Evaluate doc.delete().
    - Otherwise.
      - For each link in doc.links.
        - If (link.link\_doctype equals doctype and link.link\_name equals docname).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.link\_doctype equals doctype → link.link\_name equals docname.
          - Evaluate doc.remove(link).
          - Evaluate doc.save().
          - Leave the innermost loop without its normal-exhaustion alternative.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L5164) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L711) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L784)

<a id="op-f684221cc1f084"></a>
### Filter dynamic link doctypes

`operation_foundation_contacts_address_and_contact_business_behavior_filter_dynamic_link_record_types`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Declared result** list at list at str.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** list of list(doctype) for doctype drawn from valid\_doctypes.

**Local steps**

- Bind dependencies get\_doctypes\_with\_read.
- Set txt from (txt or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in txt → empty text.
- Set filters from (filters or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
- Set \_doctypes\_from\_df from Platform.get\_all(“DocField”, filters = filters, pluck = “parent”, distinct = true, order\_by = no value).
- Set doctypes\_from\_df from set of d for d drawn from \_doctypes\_from\_df where txt.lower() belongs to translated d.lower().
  - Draw d from \_doctypes\_from\_df, keep a combination only if (txt.lower() belongs to translated d.lower()).
- Evaluate filters.update(mapping(“dt” → tuple(“not in”, doctypes\_from\_df))).
- Set \_doctypes\_from\_cdf from Platform.get\_all(“Custom Field”, filters = filters, pluck = “dt”, distinct = true, order\_by = no value).
- Set doctypes\_from\_cdf from set of d for d drawn from \_doctypes\_from\_cdf where txt.lower() belongs to translated d.lower().
  - Draw d from \_doctypes\_from\_cdf, keep a combination only if (txt.lower() belongs to translated d.lower()).
- Set all\_doctypes from doctypes\_from\_df.union(doctypes\_from\_cdf).
- Set allowed\_doctypes from set(get\_doctypes\_with\_read()).
- Set valid\_doctypes from sorted(all\_doctypes.intersection(allowed\_doctypes)).
- Return list of list(doctype) for doctype drawn from valid\_doctypes.
  - Draw doctype from valid\_doctypes.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L5563) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L712) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L785)

<a id="op-051ba822501264"></a>
### Set link title

`operation_foundation_contacts_address_and_contact_business_behavior_set_link_title`

**Inputs** doc.

**Record and data access** resolve a document from link.link\_doctype via get\_doc.

**Explicit results** no value.

**Local steps**

- If not doc.links.
  - Return no value.
- For each link in doc.links.
  - Set linked\_doc from Platform.get\_doc(link.link\_doctype, link.link\_name).
  - Set doc\_title from linked\_doc.get\_title().
  - If link.link\_title differs from doc\_title.
    - Set link.link\_title from (doc\_title or link.link\_name).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc\_title → link.link\_name.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0032.json#L6278) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L721) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L794)

## Record · Address template

[Record definition](../../../../data/record-types/address_template.json)

<a id="op-62c00a415ca1b3"></a>
### Address Template.validate

`operation_foundation_contacts_record_definitions_address_template_business_behavior_address_template_validate`

**Inputs** self.

**State and service calls** msgprint with translated “Setting this Address Template as default as there is no other default”.

**Local steps**

- Evaluate validate\_template(self.template).
- If not self.template.
  - Set self.template from get\_default\_address\_template().
- If (not self.is\_default and not self.\_get\_previous\_default()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_default → not self.\_get\_previous\_default().
  - Set self.is\_default from 1.
  - If Platform.is\_setup\_complete().
    - Evaluate Platform.msgprint(translated “Setting this Address Template as default as there is no other default”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get previous default](operations-003.md#op-7327fdbdf2b5b4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L6823) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L749) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L822)

<a id="op-d675dbb6749eae"></a>
### Address Template.on update

`operation_foundation_contacts_record_definitions_address_template_business_behavior_address_template_on_update`

**Inputs** self.

**State and service calls** request set\_value on “Address Template”.

**Local steps**

- If (self.is\_default and previous\_default bound to self.\_get\_previous\_default()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_default → previous\_default bound to self.\_get\_previous\_default().
  - Evaluate Platform.db.set\_value(“Address Template”, previous\_default, “is\_default”, 0).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get previous default](operations-003.md#op-7327fdbdf2b5b4).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L7047) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L748) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L821)

<a id="op-1f566ae1bca6b5"></a>
### Address Template.on trash

`operation_foundation_contacts_record_definitions_address_template_business_behavior_address_template_on_trash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Default Address Template cannot be deleted”.

**Local steps**

- If self.is\_default.
  - Call the validation error handler Platform.throw(translated “Default Address Template cannot be deleted”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L7172) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L747) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L820)

<a id="op-7327fdbdf2b5b4"></a>
### Address Template.get previous default

`operation_foundation_contacts_record_definitions_address_template_business_behavior_address_template_get_previous_default`

**Inputs** self.

**Declared result** (str bitwise or no value).

**Record and data access** read “Address Template” via get\_value.

**Explicit results** Platform.db.get\_value(“Address Template”, mapping(“is\_default” → 1, “name” → tuple(“!=”, self.name))).

**Local steps**

- Return Platform.db.get\_value(“Address Template”, mapping(“is\_default” → 1, “name” → tuple(“!=”, self.name))).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0033.json#L7256) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L746) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L819)
