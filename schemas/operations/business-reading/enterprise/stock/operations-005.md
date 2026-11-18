# Inventory and warehouses · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Cogs by item group

<a id="op-cbae3feed1a165"></a>
### Assign item groups to svd list

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_assign_item_groups_to_singular_value_decomposition_list`

**Inputs** svd\_list.

**Declared result** no value.

**Local steps**

- Set ig\_map from get\_item\_groups\_map(svd\_list).
- For each item in svd\_list.
  - Set item.item\_group from ig\_map at item.get(“item\_code”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L4732) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L442) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L92)

<a id="op-8f1dd2457a9e79"></a>
### Get item groups map

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_item_groups_map`

**Inputs** svd\_list.

**Declared result** dict at tuple(str, str).

**Record and data access** read “Item” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Item”, fields = list(“name”, “item\_group”), filters = list(tuple(“name”, “in”, item\_codes)), as\_list = true)).

**Local steps**

- Set item\_codes from set(generator of i at “item\_code” for i drawn from svd\_list).
  - Draw i from svd\_list.
- Return Platform.\_dict(Platform.get\_all(“Item”, fields = list(“name”, “item\_group”), filters = list(tuple(“name”, “in”, item\_codes)), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L4856) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L98)

<a id="op-12a185d19dd1b4"></a>
### Get item groups dict

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_get_item_groups_mapping`

**Inputs** no declared parameters.

**Declared result** ItemGroupsDict.

**Record and data access** read “Item Group” via get\_all.

**Explicit results** mapping of tuple(i at “lft”, i at “rgt”) → mapping(“name” → i at “name”, “is\_group” → i at “is\_group”) for i drawn from item\_groups\_list.

**Local steps**

- Set item\_groups\_list from Platform.get\_all(“Item Group”, fields = tuple(“name”, “is\_group”, “lft”, “rgt”)).
- Return mapping of tuple(i at “lft”, i at “rgt”) → mapping(“name” → i at “name”, “is\_group” → i at “is\_group”) for i drawn from item\_groups\_list.
  - Draw i from item\_groups\_list.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L5081) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L449) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L99)

<a id="op-f15bd4005ac98c"></a>
### Update leveled dict

`operation_enterprise_stock_report_cogs_by_item_group_business_behavior_update_leveled_mapping`

**Inputs** leveled\_dict.

**Declared result** no value.

**Local steps**

- For each k in leveled\_dict.
  - Evaluate leveled\_dict at k.update(mapping(“self\_value” → 0, “agg\_value” → 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0888.json#L5308) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L104)

## Record · Company restriction

[Record definition](../../../../data/record-types/company_restriction.json)

<a id="op-c019bdf7dc4ab6"></a>
### Get allowed companies

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_get_allowed_companies`

**Inputs** user, doctype.

**Explicit results** no value · (get\_allowed\_docs\_for\_doctype(user\_permissions at “Company”, doctype) or no value).

**Local steps**

- Bind dependencies get\_allowed\_docs\_for\_doctype, get\_user\_permissions.
- Set user\_permissions from get\_user\_permissions((user or Platform.session.user)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- If “Company” does not belong to user\_permissions.
  - Return no value.
- Return (get\_allowed\_docs\_for\_doctype(user\_permissions at “Company”, doctype) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_allowed\_docs\_for\_doctype(user\_permissions at “Company”, doctype) → no value.

**Values supplied outside this operation** effective access from get\_user\_permissions((user or Platform.session.user)).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L3906) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L841)

<a id="op-c98b978125c028"></a>
### Get permission query conditions

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype.

**Explicit result forms** no value, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L4078) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L845)

<a id="op-b8a1322b1faf70"></a>
### Get allowed masters condition

`operation_enterprise_binding_enterprise_stock_doctype_company_restriction_company_restriction_get_allowed_masters_condition`

**Inputs** field, doctype, user = no value.

**Explicit results** no value · field.isin(allowed\_masters).

**Local steps**

- If doctype does not belong to RESTRICTABLE\_MASTER\_DOCTYPES.
  - Return no value.
- Set allowed\_companies from get\_allowed\_companies(user, doctype).
- If (not allowed\_companies or doctype does not belong to get\_restricted\_master\_doctypes()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not allowed\_companies → doctype does not belong to get\_restricted\_master\_doctypes().
  - Return no value.
- Set master from Platform.qb.DocType(doctype).
- Set allowed\_masters from nested operand in the contract.qb.from\_(master).select(master.name).where(get\_restriction\_criterion(doctype, allowed\_companies)).
- Return field.isin(allowed\_masters).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L206)

<a id="op-4ee8185e7d7cf9"></a>
### Remove restricted masters

`operation_enterprise_binding_enterprise_stock_doctype_company_restriction_company_restriction_remove_restricted_masters`

**Inputs** rows, fieldname, doctype.

**Record and data access** read doctype via get\_all.

**Explicit results** rows · list of row for row drawn from rows where row.get(fieldname) belongs to allowed.

**Local steps**

- Set condition from get\_allowed\_masters\_condition(Platform.qb.DocType(doctype).name, doctype).
- Set names from list(set of row.get(fieldname) for row drawn from rows where row.get(fieldname)).
  - Draw row from rows, keep a combination only if (row.get(fieldname)).
- If (not condition or not names).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not condition → not names.
  - Return rows.
- Set allowed from set(Platform.get\_all(doctype, filters = list(mapping(“name” → tuple(“in”, names)), condition), pluck = “name”)).
- Return list of row for row drawn from rows where row.get(fieldname) belongs to allowed.
  - Draw row from rows, keep a combination only if (row.get(fieldname) belongs to allowed).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L154) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L714) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L211)

<a id="op-89407d013c0ae6"></a>
### Get restriction criterion

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_get_restriction_criterion`

**Inputs** doctype, companies.

**Explicit results** Bracket((parent.restrict\_to\_companies equals 0 bitwise or ExistsCriterion(allowed\_rows))).

**Local steps**

- Set parent from Platform.qb.DocType(doctype).
- Set restriction from Platform.qb.DocType(“Company Restriction”).
- Set allowed\_rows from nested operand in the contract.qb.from\_(restriction).select(restriction.name).where((((restriction.parenttype equals doctype bitwise and restriction.parentfield equals “allowed\_companies”) bitwise and rest ….
- Return Bracket((parent.restrict\_to\_companies equals 0 bitwise or ExistsCriterion(allowed\_rows))).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L4557) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L846)

<a id="op-0f5360c17a7cfc"></a>
### Has permission

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, the result of a delegated call.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L4900) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1310) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L848)

<a id="op-5758f8a8f1f527"></a>
### Get inherited permission query conditions

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_get_inherited_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user, doctype.

**Explicit result forms** a value selected from the current context, no value.

**Local structure** 4 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L843)

<a id="op-91337661f4b37a"></a>
### Get restricted master doctypes

`operation_enterprise_binding_enterprise_stock_doctype_company_restriction_company_restriction_get_restricted_master_doctypes`

**Inputs** no declared parameters.

**Record and data access** read “Company Restriction” via get\_all.

**Explicit results** Platform.get\_all(“Company Restriction”, filters = mapping(“parentfield” → “allowed\_companies”, “parenttype” → tuple(“in”, RESTRICTABLE\_MASTER\_DOCTYPES)), pluck = “parenttype”, distinct = true).

**Local steps**

- Return Platform.get\_all(“Company Restriction”, filters = mapping(“parentfield” → “allowed\_companies”, “parenttype” → tuple(“in”, RESTRICTABLE\_MASTER\_DOCTYPES)), pluck = “parenttype”, distinct = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L153) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L210)

<a id="op-b9ebe25d6dc427"></a>
### Get linked master criterion

`operation_enterprise_binding_enterprise_stock_doctype_company_restriction_company_restriction_get_linked_master_criterion`

**Inputs** doctype, link, companies.

**Explicit results** criterion.

**Local steps**

- Set table from Platform.qb.DocType(doctype).
- Set master from Platform.qb.DocType(link.doctype).
- Set blocked\_masters from nested operand in the contract.qb.from\_(master).select(master.name).where(get\_restriction\_criterion(link.doctype, companies).negate()).
- Set criterion from (IfNull(table at link.fieldname, empty text) equals empty text bitwise or table at link.fieldname.notin(blocked\_masters)).
- If link.doctype\_fieldname.
  - Set criterion from (IfNull(table at link.doctype\_fieldname, empty text) differs from link.doctype bitwise or criterion).
- Return criterion.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L208)

<a id="op-13d50f28e4e648"></a>
### Has inherited permission

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_has_inherited_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean false, Boolean true.

**Local structure** 2 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L847)

<a id="op-5a5341cfc9cccc"></a>
### Get inherited master links

`operation_enterprise_binding_enterprise_stock_doctype_company_restriction_company_restriction_get_inherited_master_links`

**Inputs** doctype.

**Explicit results** list() · get\_master\_links(meta).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If (doctype belongs to RESTRICTABLE\_MASTER\_DOCTYPES or meta.istable or meta.issingle).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype belongs to RESTRICTABLE\_MASTER\_DOCTYPES → meta.istable → meta.issingle.
  - Return list().
- Return get\_master\_links(meta).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L207)

<a id="op-eddda644d47bba"></a>
### Get master links

`operation_enterprise_binding_enterprise_stock_doctype_company_restriction_company_restriction_get_master_links`

**Inputs** meta.

**Explicit results** links.

**Local steps**

- Set links from list of MasterLink(field.fieldname, field.options) for field drawn from meta.get\_link\_fields() where field.options belongs to RESTRICTABLE\_MASTER\_DOCTYPES.
  - Draw field from meta.get\_link\_fields(), keep a combination only if (field.options belongs to RESTRICTABLE\_MASTER\_DOCTYPES).
- For each field in meta.get\_dynamic\_link\_fields().
  - Evaluate links.extend(generator of MasterLink(field.fieldname, doctype, field.options) for doctype drawn from RESTRICTABLE\_MASTER\_DOCTYPES).
    - Draw doctype from RESTRICTABLE\_MASTER\_DOCTYPES.
- Return links.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L712) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L209)

<a id="op-61be8f9b8a69b2"></a>
### Validate allowed companies

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_validate_allowed_companies`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Allowed Companies is required when Restrict to Companies is checked” · validation helper with Platform.PermissionError — translated “You are not permitted to add or remove Company {0} in Allowed Companies”.format(company).

**Local steps**

- If not doc.get(“restrict\_to\_companies”).
  - Evaluate doc.set(“allowed\_companies”, list()).
- Otherwise.
  - If (not doc.get(“allowed\_companies”) and not doc.flags.ignore\_mandatory).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.get(“allowed\_companies”) → not doc.flags.ignore\_mandatory.
    - Call the validation error handler Platform.throw(translated “Allowed Companies is required when Restrict to Companies is checked”, Platform.MandatoryError).
- If doc.flags.ignore\_permissions.
  - Return no value.
- Set allowed\_companies from get\_allowed\_companies(Platform.session.user, doc.doctype).
- If not allowed\_companies.
  - Return no value.
- Set previous\_companies from set().
- If previous\_doc bound to doc.get\_doc\_before\_save().
  - Set previous\_companies from set of row.company for row drawn from (previous\_doc.get(“allowed\_companies”) or list()).
    - Draw row from (previous\_doc.get(“allowed\_companies”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in previous\_doc.get(“allowed\_companies”) → list().
- Set current\_companies from set of row.company for row drawn from (doc.get(“allowed\_companies”) or list()).
  - Draw row from (doc.get(“allowed\_companies”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“allowed\_companies”) → list().
- For each company in current\_companies.symmetric\_difference(previous\_companies).
  - If company does not belong to allowed\_companies.
    - Call the validation error handler Platform.throw(translated “You are not permitted to add or remove Company {0} in Allowed Companies”.format(company), Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L5348) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L849)

<a id="op-ed48de04a33914"></a>
### Validate transaction company

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_validate_transaction_company`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If (doc.doctype belongs to COMPANY\_RESTRICTION\_EXEMPT\_DOCTYPES or doc.meta.in\_create).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.doctype belongs to COMPANY\_RESTRICTION\_EXEMPT\_DOCTYPES → doc.meta.in\_create.
  - Return no value.
- Set company\_field from doc.meta.get\_field(“company”).
- If (not company\_field or company\_field.fieldtype differs from “Link” or company\_field.options differs from “Company”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not company\_field → company\_field.fieldtype differs from “Link” → company\_field.options differs from “Company”.
  - Return no value.
- Set company from doc.get(“company”).
- If not company.
  - Return no value.
- For each tuple(doctype, names) in get\_master\_references(doc).items().
  - Evaluate validate\_masters\_for\_company(doctype, names, company).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L5941) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1313) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L851)

<a id="op-2d99333f6df026"></a>
### Validate masters for company

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_validate_masters_for_company`

**Inputs** doctype, names, company.

**Explicit failure paths** validation helper with CompanyRestrictionError — translated “{0} {1} cannot be used with Company {2} because of Company Restrictions”.format(translated doctype, comma\_and(list of Platform.bold(name) for name drawn from blocked, add\_quotes = false), Platf ….

**Local steps**

- If blocked bound to get\_blocked\_masters(doctype, names, list(company)).
  - Call the validation error handler Platform.throw(translated “{0} {1} cannot be used with Company {2} because of Company Restrictions”.format(translated doctype, comma\_and(list of Platform.bold(name) for name drawn from blocked, add\_quotes  ….
    - Draw name from blocked.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1312) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L850)

<a id="op-64961742eb62e6"></a>
### Get master references

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_get_master_references`

**Inputs** doc.

**Explicit results** references.

**Local steps**

- Set references from defaultdict(set).
- Evaluate collect\_master\_references(list(doc), references).
- For each table\_field in doc.meta.get\_table\_fields().
  - If rows bound to doc.get(table\_field.fieldname).
    - Evaluate collect\_master\_references(rows, references).
- Return references.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0711.json#L6541) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L844)

<a id="op-ecefcadffd58d5"></a>
### Collect master references

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_collect_master_references`

**Inputs** rows, references.

**Local steps**

- Set links from get\_master\_links(Platform.get\_meta(rows at 0.doctype)).
- For each row in rows.
  - For each link in links.
    - If (link.doctype\_fieldname and row.get(link.doctype\_fieldname) differs from link.doctype).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in link.doctype\_fieldname → row.get(link.doctype\_fieldname) differs from link.doctype.
      - Continue with the next iteration or loop test.
    - If value bound to row.get(link.fieldname).
      - Evaluate references at link.doctype.add(value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L839)

<a id="op-78c0ce0ab6d264"></a>
### Get blocked masters

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_get_blocked_masters`

**Inputs** doctype, names, companies.

**Record and data access** read doctype via get\_all · read “Company Restriction” via get\_all.

**Explicit results** list() · sorted((set(restricted) − set(allowed))).

**Local steps**

- Set restricted from Platform.get\_all(doctype, filters = mapping(“name” → tuple(“in”, sorted(names)), “restrict\_to\_companies” → 1), pluck = “name”).
- If not restricted.
  - Return list().
- Set allowed from Platform.get\_all(“Company Restriction”, filters = mapping(“parenttype” → doctype, “parentfield” → “allowed\_companies”, “parent” → tuple(“in”, restricted), “company” → tuple(“in”, companies)), pluck = “parent”).
- Return sorted((set(restricted) − set(allowed))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L842)

<a id="op-e843ed5fa4a1db"></a>
### Company query

`operation_enterprise_stock_record_definitions_company_restriction_business_behavior_company_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters = no value.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Company” via get\_list.

**Explicit results** Platform.get\_list(“Company”, filters = filters, limit\_start = start, limit\_page\_length = page\_len, order\_by = “name”, …).

**Local steps**

- Set filters from Platform.parse\_json(filters) when filters, otherwise mapping().
  - Value choice on filters — true gives Platform.parse\_json(filters), false gives mapping().
- If isinstance(filters, list).
  - Evaluate filters.append(list(“Company”, “name”, “like”, formatted text %{txt}%)).
- Otherwise.
  - Set filters at “name” from tuple(“like”, formatted text %{txt}%).
- Return Platform.get\_list(“Company”, filters = filters, limit\_start = start, limit\_page\_length = page\_len, order\_by = “name”, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0712.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L840)

## Report · Delayed item report

<a id="op-bc8dcef8aa7cca"></a>
### Execute

`operation_enterprise_stock_report_delayed_item_report_business_behavior_execute`

**Inputs** filters = no value, consolidated = false.

**Explicit results** tuple(data, columns).

**Local steps**

- Evaluate validate\_date\_range(filters).
- Set tuple(data, columns) from DelayedItemReport(filters).run().
- Return tuple(data, columns).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0040.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-011.tsv#L464) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-012.tsv#L113)
