# Company and master data · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Item group

[Record definition](../../../../data/record-types/item_group.json)

<a id="op-2646a00eee73ad"></a>
### Item Group.validate

`operation_enterprise_setup_record_definitions_item_group_business_behavior_item_group_validate`

**Inputs** self.

**Record and data access** read “Item Group” via get\_value.

**Local steps**

- If (not self.parent\_item\_group and not Platform.in\_test).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.parent\_item\_group → not Platform.in\_test.
  - Set root from Platform.db.get\_value(“Item Group”, mapping(“parent\_item\_group” → tuple(“is”, “not set”), “is\_group” → 1), order\_by = “lft asc”).
  - If (root and root differs from self.name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in root → root differs from self.name.
    - Set self.parent\_item\_group from root.
- Evaluate self.validate\_item\_group\_defaults().
- Evaluate self.check\_item\_tax().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item group defaults](operations-012.md#op-8b678c73a4b0d3), [check item tax](operations-012.md#op-bbc65c403a618e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L954) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L502)

<a id="op-bbc65c403a618e"></a>
### Item Group.check item tax

`operation_enterprise_setup_record_definitions_item_group_business_behavior_item_group_check_item_tax`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} entered twice {1} in Item Taxes”.format(Platform.bold(d.item\_tax\_template), formatted text for tax category {Platform.bold(d.tax\_category)} when d.tax\_category, otherwise empty text).

**Local steps**

- Set check\_list from list().
- For each d in self.get(“taxes”).
  - If d.item\_tax\_template.
    - If tuple(d.item\_tax\_template, d.tax\_category) belongs to check\_list.
      - Call the validation error handler Platform.throw(translated “{0} entered twice {1} in Item Taxes”.format(Platform.bold(d.item\_tax\_template), formatted text for tax category {Platform.bold(d.tax\_category)} when d.tax\_category, otherwise empty text)).
        - Value choice on d.tax\_category — true gives formatted text for tax category {Platform.bold(d.tax\_category)}, false gives empty text.
    - Otherwise.
      - Evaluate check\_list.append(tuple(d.item\_tax\_template, d.tax\_category)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L950) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L498)

<a id="op-19f3b16930b092"></a>
### Item Group.on update

`operation_enterprise_setup_record_definitions_item_group_business_behavior_item_group_on_update`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_update(self).
- Evaluate self.validate\_one\_root().
- Evaluate self.delete\_child\_item\_groups\_key().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete child item groups key](operations-012.md#op-61a6b398714cd3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0694.json#L1597) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L953) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L501)

<a id="op-79b32fbc7d498e"></a>
### Item Group.on trash

`operation_enterprise_setup_record_definitions_item_group_business_behavior_item_group_on_trash`

**Inputs** self.

**Local steps**

- Evaluate NestedSet.on\_trash(self, allow\_root\_deletion = true).
- Evaluate self.delete\_child\_item\_groups\_key().

If control reaches the end, it returns no value.

**Methods declared on this owner** [delete child item groups key](operations-012.md#op-61a6b398714cd3).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0694.json#L1690) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L500)

<a id="op-61a6b398714cd3"></a>
### Item Group.delete child item groups key

`operation_enterprise_setup_record_definitions_item_group_business_behavior_item_group_delete_child_item_groups_key`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache().hdel(“child\_item\_groups”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0694.json#L1775) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L951) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L499)

<a id="op-8b678c73a4b0d3"></a>
### Item Group.validate item group defaults

`operation_enterprise_setup_record_definitions_item_group_business_behavior_item_group_validate_item_group_defaults`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_item\_defaults.
- Evaluate validate\_item\_defaults(self.item\_group\_defaults).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L955) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L503)

<a id="op-7c711e770c1ad5"></a>
### Get child item groups

`operation_enterprise_setup_record_definitions_item_group_business_behavior_get_child_item_groups`

**Inputs** item\_group\_name.

**Record and data access** read “Item Group” via get\_cached\_value · read “Item Group” via get\_all.

**Explicit results** (child\_item\_groups or mapping()).

**Local steps**

- Set item\_group from Platform.get\_cached\_value(“Item Group”, item\_group\_name, list(“lft”, “rgt”), as\_dict = 1).
- Set child\_item\_groups from list of d.name for d drawn from Platform.get\_all(“Item Group”, filters = mapping(“lft” → tuple(“&gt;=”, item\_group.lft), “rgt” → tuple(“&lt;=”, item\_group.rgt))).
  - Draw d from Platform.get\_all(“Item Group”, filters = mapping(“lft” → tuple(“&gt;=”, item\_group.lft), “rgt” → tuple(“&lt;=”, item\_group.rgt))).
- Return (child\_item\_groups or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in child\_item\_groups → mapping().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item Group”, item\_group\_name, list(“lft”, “rgt”), as\_dict = 1).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0694.json#L1914) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L496)

<a id="op-55e987d3982773"></a>
### Get item group defaults

`operation_enterprise_setup_record_definitions_item_group_business_behavior_get_item_group_defaults`

**Inputs** item, company.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · resolve a document from “Item Group” via get\_cached\_doc.

**Explicit results** row · Platform.\_dict().

**Local steps**

- Set item from Platform.get\_cached\_doc(“Item”, item).
- Set item\_group from Platform.get\_cached\_doc(“Item Group”, item.item\_group).
- For each d in (item\_group.item\_group\_defaults or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in item\_group.item\_group\_defaults → list().
  - If d.company equals company.
    - Set row from d.as\_dict(no\_private\_properties = true).
    - Evaluate row.pop(“name”).
    - Return row.
- Return Platform.\_dict().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item), Platform.get\_cached\_doc(“Item Group”, item.item\_group).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0694.json#L2167) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L949) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L497)

## Record · Party type

[Record definition](../../../../data/record-types/party_type.json)

<a id="op-6114fb363db13f"></a>
### Party Type.validate

`operation_enterprise_binding_enterprise_setup_doctype_party_type_party_type_partytype_validate`

**Inputs** self.

**Record and data access** read “GL Entry” via exists.

**Explicit failure paths** validation helper — translated “Cannot change Account Type for {0} after ledger entries exist”.format(self.name).

**Local steps**

- If (not self.is\_new() and self.has\_value\_changed(“account\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → self.has\_value\_changed(“account\_type”).
  - If Platform.db.exists(“GL Entry”, mapping(“party\_type” → self.name)).
    - Call the validation error handler Platform.throw(translated “Cannot change Account Type for {0} after ledger entries exist”.format(self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L661) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L158)

<a id="op-131a96e86a5df8"></a>
### Get party type

`operation_enterprise_setup_record_definitions_party_type_business_behavior_get_party_type`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “Account” via get\_value.

**Explicit results** list() · (result or list()).

**Local steps**

- Set PartyType from DocType(“Party Type”).
- Set get\_party\_type\_query from nested operand in the contract.qb.from\_(PartyType).select(PartyType.name).orderby(PartyType.name).
- Set condition\_list from list().
- Set account from filters.get(“account”) when filters, otherwise no value.
  - Value choice on filters — true gives filters.get(“account”), false gives no value.
- If account.
  - Set ptype from “select” when Platform.only\_has\_select\_perm(“Account”), otherwise “read”.
    - Value choice on Platform.only\_has\_select\_perm(“Account”) — true gives “select”, false gives “read”.
  - If (not isinstance(account, str) or not Platform.has\_permission(“Account”, ptype, doc = account)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(account, str) → not Platform.has\_permission(“Account”, ptype, doc = account).
    - Return list().
  - Set account\_type from Platform.db.get\_value(“Account”, account, “account\_type”).
  - If account\_type belongs to list(“Receivable”, “Payable”).
    - Evaluate condition\_list.append((PartyType.account\_type equals account\_type bitwise or PartyType.name equals “Employee”)).
  - Otherwise.
    - Evaluate condition\_list.append(PartyType.account\_type equals account\_type).
- For each condition in condition\_list.
  - Set get\_party\_type\_query from get\_party\_type\_query.where(condition).
- If Platform.local.lang equals “en”.
  - Set get\_party\_type\_query from get\_party\_type\_query.where(getattr(PartyType, searchfield).like(formatted text %{txt}%)).
  - Set get\_party\_type\_query from get\_party\_type\_query.limit(page\_len).
  - Set get\_party\_type\_query from get\_party\_type\_query.offset(start).
  - Set result from get\_party\_type\_query.run().
- Otherwise.
  - Set result from get\_party\_type\_query.run().
  - Set test\_str from txt.lower().
  - Set result from list of row for row drawn from result where test\_str belongs to Platform.\_(row at 0).lower().
    - Draw row from result, keep a combination only if (test\_str belongs to Platform.\_(row at 0).lower()).
  - Set result from result at slice start to (start + page\_len).
- Return (result or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result → list().

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”, ptype, doc = account) · selected callable from getattr(PartyType, searchfield).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L136) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L975) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L523)

## Record · Sales partner

[Record definition](../../../../data/record-types/sales_partner.json)

<a id="op-8e55e14efce63f"></a>
### Sales Partner.onload

`operation_enterprise_setup_record_definitions_sales_partner_business_behavior_sales_partner_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L2302) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L526)

<a id="op-6da25c4b308f6e"></a>
### Sales Partner.autoname

`operation_enterprise_setup_record_definitions_sales_partner_business_behavior_sales_partner_autoname`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L2354) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L976) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L524)

<a id="op-a6c61941aa2f0b"></a>
### Sales Partner.validate

`operation_enterprise_setup_record_definitions_sales_partner_business_behavior_sales_partner_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_targets(self.get(“targets”)).
- If not self.route.
  - Set self.route from (“partners/” + self.scrub(self.partner\_name)).
- Evaluate super().validate().
- Evaluate self.validate\_route().
- Evaluate self.validate\_targets().
- If self.partner\_website.
  - Bind dependencies urlsplit, urlunsplit.
  - Set parts from urlsplit(self.partner\_website).
  - If (not parts.netloc and parts.path).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not parts.netloc → parts.path.
    - Set parts from parts.\_replace(netloc = parts.path, path = empty text).
  - If (not parts.scheme or parts.scheme equals “http”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parts.scheme → parts.scheme equals “http”.
    - Set parts from parts.\_replace(scheme = “https”).
  - Set self.partner\_website from urlunsplit(parts).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate route](operations-012.md#op-95084123ecdf80), [validate targets](operations-012.md#op-17728536b1fe63).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L979) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L527)

<a id="op-95084123ecdf80"></a>
### Sales Partner.validate route

`operation_enterprise_binding_enterprise_setup_doctype_sales_partner_sales_partner_salespartner_validate_route`

**Inputs** self.

**Record and data access** read “Sales Partner” via exists.

**Explicit failure paths** validation helper — translated “Route {0} is already used by another Sales Partner. Please choose another route.”.format(Platform.bold(self.route)).

**Local steps**

- If Platform.db.exists(“Sales Partner”, mapping(“route” → self.route, “name” → list(“!=”, self.name))).
  - Call the validation error handler Platform.throw(translated “Route {0} is already used by another Sales Partner. Please choose another route.”.format(Platform.bold(self.route))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L665) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L162)

<a id="op-17728536b1fe63"></a>
### Sales Partner.validate targets

`operation_enterprise_binding_enterprise_setup_doctype_sales_partner_sales_partner_salespartner_validate_targets`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Either Target Qty or Target Amount is mandatory”.format(target.idx).

**Local steps**

- For each target in (self.get(“targets”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“targets”) → list().
  - If (not flt(target.target\_qty) and not flt(target.target\_amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(target.target\_qty) → not flt(target.target\_amount).
    - Call the validation error handler Platform.throw(translated “Row #{0}: Either Target Qty or Target Amount is mandatory”.format(target.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L666) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L163)

<a id="op-4da146c7fcb2f9"></a>
### Sales Partner.get context

`operation_enterprise_setup_record_definitions_sales_partner_business_behavior_sales_partner_get_context`

**Inputs** self, context.

**Record and data access** read “Dynamic Link” via get\_all · resolve a document from “Address” via get\_doc.

**Explicit results** context.

**Local steps**

- Set address\_names from Platform.db.get\_all(“Dynamic Link”, filters = mapping(“link\_doctype” → “Sales Partner”, “link\_name” → self.name, “parenttype” → “Address”), pluck = “parent”).
- Set addresses from list().
- For each address\_name in address\_names.
  - Set address\_doc from Platform.get\_doc(“Address”, address\_name).
  - Set city\_state from “, ”.join(list of item for item drawn from list(address\_doc.city, address\_doc.state) where item).
    - Draw item from list(address\_doc.city, address\_doc.state), keep a combination only if (item).
  - Set address\_rows from list(address\_doc.address\_line1, address\_doc.address\_line2, city\_state, address\_doc.pincode, …).
  - Evaluate addresses.append(mapping(“email” → address\_doc.email\_id, “partner\_address” → filter\_strip\_join(address\_rows, whitespace '\\n'), “phone” → filter\_strip\_join(cstr(nested operand in the contract.phone).split(“ ….
- Set context at “addresses” from addresses.
- Return context.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L137) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L977) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L525)

<a id="op-fe0a9fc77c05e1"></a>
### Get list context

`operation_enterprise_binding_enterprise_setup_doctype_sales_partner_sales_partner_get_list_context`

**Inputs** context = no value.

**Explicit results** mapping(“get\_list” → get\_published\_partners).

**Local steps**

- Return mapping(“get\_list” → get\_published\_partners).

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L663) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L160)

<a id="op-f052c88de24b38"></a>
### Get published partners

`operation_enterprise_binding_enterprise_setup_doctype_sales_partner_sales_partner_get_published_partners`

**Inputs** doctype, txt, filters, limit\_start, limit\_page\_length = 20, order\_by = no value.

**Record and data access** read “Sales Partner” via get\_all.

**Explicit results** Platform.get\_all(“Sales Partner”, filters = mapping(“show\_in\_website” → 1), fields = list(“name”, “partner\_name”, “partner\_type”, “territory”, …), limit\_start = limit\_start, limit\_page\_length = limit\_page\_length, …).

**Local steps**

- Return Platform.get\_all(“Sales Partner”, filters = mapping(“show\_in\_website” → 1), fields = list(“name”, “partner\_name”, “partner\_type”, “territory”, …), limit\_start = limit\_start, limit\_page\_length = limit\_page\_length, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L664) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L161)

<a id="op-aad835850c2e66"></a>
### Get commission rate

`operation_enterprise_binding_enterprise_setup_doctype_sales_partner_sales_partner_get_commission_rate`

**Inputs** sales\_partner.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** float.

**Record and data access** resolve a document from “Sales Partner” via get\_doc.

**Explicit results** flt(partner.commission\_rate).

**Local steps**

- Set partner from Platform.get\_doc(“Sales Partner”, sales\_partner).
- Evaluate partner.check\_permission(“select”).
- Return flt(partner.commission\_rate).

**Values supplied outside this operation** effective access from partner.check\_permission(“select”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L662) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L159)

## Record · Sales person

[Record definition](../../../../data/record-types/sales_person.json)

<a id="op-64eea9a38f6112"></a>
### Sales Person.validate

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Either target qty or target amount is mandatory.”.

**Local steps**

- Evaluate validate\_targets(self.get(“targets”)).
- If not self.enabled.
  - Evaluate self.validate\_sales\_person().
- Evaluate set\_root\_as\_default\_parent(self).
- For each d in (self.get(“targets”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“targets”) → list().
  - If (not flt(d.target\_qty) and not flt(d.target\_amount)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(d.target\_qty) → not flt(d.target\_amount).
    - Call the validation error handler Platform.throw(translated “Either target qty or target amount is mandatory.”).
- Evaluate self.validate\_employee\_id().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sales person](operations-012.md#op-c942c104da5096), [validate employee id](operations-013.md#op-a75640ee58865b).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L141) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L987) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L535)

<a id="op-1ccebbf5fb78bf"></a>
### Sales Person.onload

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_onload`

**Inputs** self.

**Local steps**

- Evaluate self.load\_dashboard\_info().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load dashboard info](operations-012.md#op-08c32ee2894625).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L3563) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L534)

<a id="op-08c32ee2894625"></a>
### Sales Person.load dashboard info

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_load_dashboard_info`

**Inputs** self.

**Record and data access** read “Sales Team” via get\_value.

**Local steps**

- Set company\_default\_currency from get\_default\_currency().
- Set allocated\_amount\_against\_order from flt(Platform.db.get\_value(“Sales Team”, mapping(“docstatus” → 1, “parenttype” → “Sales Order”, “sales\_person” → self.sales\_person\_name), list(mapping(“SUM” → “allocated\_amount”)))).
- Set allocated\_amount\_against\_invoice from flt(Platform.db.get\_value(“Sales Team”, mapping(“docstatus” → 1, “parenttype” → “Sales Invoice”, “sales\_person” → self.sales\_person\_name), list(mapping(“SUM” → “allocated\_amount”)))).
- Set info from mapping().
- Set info at “allocated\_amount\_against\_order” from allocated\_amount\_against\_order.
- Set info at “allocated\_amount\_against\_invoice” from allocated\_amount\_against\_invoice.
- Set info at “currency” from company\_default\_currency.
- Evaluate self.set\_onload(“dashboard\_info”, info).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L3614) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L984) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L532)

<a id="op-4d5861ecb5ed1a"></a>
### Sales Person.on update

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_on_update`

**Inputs** self.

**Local steps**

- Evaluate super().on\_update().
- Evaluate self.validate\_one\_root().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0695.json#L4047) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L533)

<a id="op-c942c104da5096"></a>
### Sales Person.validate sales person

`operation_enterprise_setup_record_definitions_sales_person_business_behavior_sales_person_validate_sales_person`

**Inputs** self.

**Explicit failure paths** validation helper — translated “The Sales Person is linked with {0}”.format(Platform.bold(formatted text &lt;a href="{get\_url\_to\_list(“Customer”)}?sales\_person={self.name}"&gt;{“Customers”}&lt;/a&gt;)) · validation helper — translated “Sales Person {0} cannot be disabled because {1} {2} is unfinished.”.format(Platform.bold(self.name), translated doctype, get\_link\_to\_form(doctype, linked\_transactions at 0 at 0)).

**Local steps**

- Set sales\_team from Platform.qb.DocType(“Sales Team”).
- Set query from nested operand in the contract(nested operand in the contract).where((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand i ….
- If query.
  - Call the validation error handler Platform.throw(translated “The Sales Person is linked with {0}”.format(Platform.bold(formatted text &lt;a href="{get\_url\_to\_list(“Customer”)}?sales\_person={self.name}"&gt;{“Customers”}&lt;/a&gt;))).
- For each doctype in tuple(“Sales Order”, “Delivery Note”).
  - Set transaction from Platform.qb.DocType(doctype).
  - Set unfinished from transaction.status.notin(tuple(“Completed”, “Closed”)) when doctype equals “Sales Order”, otherwise transaction.status.isin(tuple(“To Bill”, “Partially Billed”)).
    - Value choice on doctype equals “Sales Order” — true gives transaction.status.notin(tuple(“Completed”, “Closed”)), false gives transaction.status.isin(tuple(“To Bill”, “Partially Billed”)).
  - Set linked\_transactions from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and unfinished)).limit(1).run().
  - If linked\_transactions.
    - Call the validation error handler Platform.throw(translated “Sales Person {0} cannot be disabled because {1} {2} is unfinished.”.format(Platform.bold(self.name), translated doctype, get\_link\_to\_form(doctype, linked\_transactions at 0 at 0))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L989) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L537)
