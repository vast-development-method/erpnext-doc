# Purchasing · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Report · Subcontracted item to be received

<a id="op-4e95995a1f50db"></a>
### Get data

`operation_enterprise_buying_report_subcontracted_item_to_be_received_business_behavior_get_data`

**Inputs** data, filters.

**Local steps**

- Set orders from get\_subcontract\_orders(filters).
- Set orders\_name from list of order.name for order drawn from orders.
  - Draw order from orders.
- Set subcontracted\_items from get\_subcontract\_order\_supplied\_item(filters.order\_type, orders\_name).
- For each item in subcontracted\_items.
  - For each order in orders.
    - If (order.name equals item.parent and item.received\_qty &lt; item.qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in order.name equals item.parent → item.received\_qty &lt; item.qty.
      - Set row from mapping(“subcontract\_order” → item.parent, “date” → order.transaction\_date, “supplier” → order.supplier, “fg\_item\_code” → item.item\_code, …).
      - Evaluate data.append(row).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L249)

<a id="op-91425a5a1dd7e7"></a>
### Get subcontract orders

`operation_enterprise_buying_report_subcontracted_item_to_be_received_business_behavior_get_subcontract_orders`

**Inputs** filters.

**Record and data access** read filters.order\_type via get\_all.

**Explicit results** Platform.get\_all(filters.order\_type, filters = record\_filters, fields = list(“name”, “transaction\_date”, “supplier”)).

**Local steps**

- Set record\_filters from list(list(“supplier”, “=”, filters.supplier), list(“transaction\_date”, “&lt;=”, filters.to\_date), list(“transaction\_date”, “&gt;=”, filters.from\_date), list(“docstatus”, “=”, 1), …).
- If filters.order\_type equals “Purchase Order”.
  - Evaluate record\_filters.append(list(“is\_old\_subcontracting\_flow”, “=”, 1)).
- Return Platform.get\_all(filters.order\_type, filters = record\_filters, fields = list(“name”, “transaction\_date”, “supplier”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L251)

<a id="op-fecb0d2d07142f"></a>
### Get subcontract order supplied item

`operation_enterprise_buying_report_subcontracted_item_to_be_received_business_behavior_get_subcontract_order_supplied_item`

**Inputs** order\_type, orders.

**Record and data access** read formatted text {order\_type} Item via get\_all.

**Explicit results** Platform.get\_all(formatted text {order\_type} Item, filters = list(tuple(“parent”, “IN”, orders)), fields = list(“parent”, “item\_code”, “item\_name”, “qty”, …)).

**Local steps**

- Return Platform.get\_all(formatted text {order\_type} Item, filters = list(tuple(“parent”, “IN”, orders)), fields = list(“parent”, “item\_code”, “item\_name”, “qty”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0361.json#L6615) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L250)

## Report · Subcontracted raw materials to be transferred

<a id="op-afff51e3b24e5e"></a>
### Execute

`operation_enterprise_buying_report_subcontracted_raw_materials_to_be_transferred_business_behavior_execute`

**Inputs** filters = no value.

**State and service calls** msgprint with translated “To Date must be greater than From Date”.

**Explicit results** tuple(columns, (data or list())).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If filters.from\_date &gt; filters.to\_date.
  - Evaluate Platform.msgprint(translated “To Date must be greater than From Date”).
- Set columns from get\_columns(filters).
- Set data from get\_data(filters).
- Return tuple(columns, (data or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in data → list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L544) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L254)

<a id="op-93edf6f9773f83"></a>
### Get columns

`operation_enterprise_buying_report_subcontracted_raw_materials_to_be_transferred_business_behavior_get_columns`

**Inputs** filters.

**Explicit results** list(mapping(“label” → translated “Subcontract Order”, “fieldtype” → “Link”, “fieldname” → “subcontract\_order”, “options” → filters.order\_type, …), mapping(“label” → translated “Date”, “fieldtype” → “Date” ….

**Local steps**

- Return list(mapping(“label” → translated “Subcontract Order”, “fieldtype” → “Link”, “fieldname” → “subcontract\_order”, “options” → filters.order\_type, …), mapping(“label” → translated “Date”, “fieldtype” → “Date” ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L545) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L255)

<a id="op-2432fa57814b12"></a>
### Get data

`operation_enterprise_buying_report_subcontracted_raw_materials_to_be_transferred_business_behavior_get_data`

**Inputs** filters.

**Explicit results** data.

**Local steps**

- Set order\_rm\_item\_details from get\_order\_items\_to\_supply(filters).
- Set data from list().
- For each row in order\_rm\_item\_details.
  - Set transferred\_qty from ((row.get(“transferred\_qty”) or 0) − (row.get(“returned\_qty”) or 0)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“transferred\_qty”) → 0.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“returned\_qty”) → 0.
  - If transferred\_qty &lt; row.get(“reqd\_qty”, 0).
    - Set pending\_qty from Platform.utils.flt((row.get(“reqd\_qty”, 0) − transferred\_qty)).
    - Set row.p\_qty from pending\_qty when pending\_qty &gt; 0, otherwise 0.
      - Value choice on pending\_qty &gt; 0 — true gives pending\_qty, false gives 0.
    - Evaluate data.append(row).
- Return data.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0362.json#L1948) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L256)

<a id="op-350ae661cf2d42"></a>
### Get order items to supply

`operation_enterprise_buying_report_subcontracted_raw_materials_to_be_transferred_business_behavior_get_order_items_to_supply`

**Inputs** filters.

**Record and data access** read filters.order\_type via get\_all.

**Explicit results** Platform.db.get\_all(filters.order\_type, fields = list(“name as subcontract\_order”, “transaction\_date as date”, “supplier as supplier”, formatted text ′tab{supplied\_items\_table}′.rm\_item\_code as rm\_item\_cod ….

**Local steps**

- Set supplied\_items\_table from “Purchase Order Item Supplied” when filters.order\_type equals “Purchase Order”, otherwise “Subcontracting Order Supplied Item”.
  - Value choice on filters.order\_type equals “Purchase Order” — true gives “Purchase Order Item Supplied”, false gives “Subcontracting Order Supplied Item”.
- Set record\_filters from list(list(filters.order\_type, “per\_received”, “&lt;”, “100”), list(filters.order\_type, “supplier”, “=”, filters.supplier), list(filters.order\_type, “transaction\_date”, “&lt;=”, filters.to\_date), list(filters.ord ….
- If filters.order\_type equals “Purchase Order”.
  - Evaluate record\_filters.append(list(filters.order\_type, “is\_old\_subcontracting\_flow”, “=”, 1)).
- Return Platform.db.get\_all(filters.order\_type, fields = list(“name as subcontract\_order”, “transaction\_date as date”, “supplier as supplier”, formatted text ′tab{supplied\_items\_table}′.rm\_item\_code as rm\_item\_cod ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L547) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L257)

## Record · Supplier

[Record definition](../../../../data/record-types/supplier.json)

<a id="op-d72eeab57b6c48"></a>
### Supplier.onload

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self).
- Evaluate self.load\_dashboard\_info().

If control reaches the end, it returns no value.

**Methods declared on this owner** [load dashboard info](operations-008.md#op-cffbed09719820).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L738) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L307) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L66)

<a id="op-46282ce5536fa8"></a>
### Supplier.before save

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_before_save`

**Inputs** self.

**Local steps**

- If not self.on\_hold.
  - Set self.release\_date from empty text.
- Otherwise.
  - If (self.on\_hold and not self.hold\_type).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.on\_hold → not self.hold\_type.
    - Set self.hold\_type from “All”.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L810) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L300) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L59)

<a id="op-f2faae99fd1e9e"></a>
### Supplier.is blocked for

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_supplier_is_blocked_for`

**Inputs** self, hold\_type.

**Declared result** bool.

**Explicit results** bool((self.on\_hold and self.hold\_type belongs to tuple(“All”, hold\_type) and (not self.release\_date or getdate(nowdate()) &lt; getdate(self.release\_date)))).

**Local steps**

- Return bool((self.on\_hold and self.hold\_type belongs to tuple(“All”, hold\_type) and (not self.release\_date or getdate(nowdate()) &lt; getdate(self.release\_date)))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.on\_hold → self.hold\_type belongs to tuple(“All”, hold\_type) → (not self.release\_date or getdate(nowdate()) &lt; getdate(self.release\_date)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.release\_date → getdate(nowdate()) &lt; getdate(self.release\_date).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L212) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L114)

<a id="op-cffbed09719820"></a>
### Supplier.load dashboard info

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_load_dashboard_info`

**Inputs** self.

**Local steps**

- Set info from get\_dashboard\_info(self.doctype, self.name).
- Evaluate self.set\_onload(“dashboard\_info”, info).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L925) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L304) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L63)

<a id="op-ed48611ce7de0e"></a>
### Supplier.autoname

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_autoname`

**Inputs** self.

**Local steps**

- Set supp\_master\_name from Platform.defaults.get\_global\_default(“supp\_master\_name”).
- If supp\_master\_name equals “Supplier Name”.
  - Set self.name from self.supplier\_name.
- Otherwise.
  - If supp\_master\_name equals “Naming Series”.
    - Evaluate set\_name\_by\_naming\_series(self).
  - Otherwise.
    - Evaluate set\_name\_from\_naming\_options(Platform.get\_meta(self.doctype).autoname, self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L1025) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L298) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L57)

<a id="op-c484091443bc3c"></a>
### Supplier.on update

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.create\_primary\_contact().
- Evaluate self.create\_primary\_address().
- Evaluate link\_portal\_users\_to\_contacts(self).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create primary contact](operations-008.md#op-f239d7c6623099), [create primary address](operations-008.md#op-8fbc0d76efd2c7).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L1234) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L306) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L65)

<a id="op-e8781778e9e369"></a>
### Supplier.add role for user

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_add_role_for_user`

**Inputs** self.

**Local steps**

- For each portal\_user in self.portal\_users.
  - Evaluate add\_role\_for\_portal\_user(portal\_user, “Supplier”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L1326) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L295) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L54)

<a id="op-0f8827a5dcac11"></a>
### Supplier.add supplier role

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_add_supplier_role`

**Inputs** self, portal\_user.

**Record and data access** resolve a document from “User” via get\_doc.

**State and service calls** msgprint with translated “Please add 'Supplier' role to user {0}.”.format(portal\_user.user) · msgprint with translated “Added Supplier Role to User {0}.”.format(Platform.bold(user\_doc.name)).

**Explicit results** no value.

**Local steps**

- If not portal\_user.is\_new().
  - Return no value.
- Set user\_doc from Platform.get\_doc(“User”, portal\_user.user).
- Set roles from set of r.role for r drawn from user\_doc.roles.
  - Draw r from user\_doc.roles.
- If “Supplier” belongs to roles.
  - Return no value.
- If “System Manager” does not belong to Platform.get\_roles().
  - Evaluate Platform.msgprint(translated “Please add 'Supplier' role to user {0}.”.format(portal\_user.user), alert = true).
  - Return no value.
- Evaluate user\_doc.add\_roles(“Supplier”).
- Evaluate Platform.msgprint(translated “Added Supplier Role to User {0}.”.format(Platform.bold(user\_doc.name)), alert = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L1406) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L296) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L55)

<a id="op-4a855d3d1a42c7"></a>
### Supplier.validate

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_validate`

**Inputs** self.

**Local steps**

- Set self.flags.is\_new\_doc from self.is\_new().
- If Platform.defaults.get\_global\_default(“supp\_master\_name”) equals “Naming Series”.
  - If not self.naming\_series.
    - Evaluate msgprint(translated “Series is mandatory”, raise\_exception = 1).
- Evaluate validate\_party\_accounts(self).
- Evaluate validate\_default\_price\_list\_side(self.default\_price\_list, “buying”).
- Evaluate self.validate\_supplier\_group().
- Evaluate self.validate\_internal\_supplier().
- Evaluate self.validate\_primary\_contact\_and\_address().
- Evaluate self.add\_role\_for\_user().
- Evaluate self.validate\_currency\_for\_receivable\_payable\_and\_advance\_account().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate supplier group](operations-008.md#op-34c5d6b547d0c5), [validate internal supplier](operations-008.md#op-bd69be5b9c66a9), [validate primary contact and address](operations-008.md#op-ede84a210d14ba), [add role for user](operations-008.md#op-e8781778e9e369).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L205) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L308) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L67)

<a id="op-34c5d6b547d0c5"></a>
### Supplier.validate supplier group

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_supplier_validate_supplier_group`

**Inputs** self.

**Record and data access** read “Supplier Group” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot select a Group type Supplier Group. Please select a non-group Supplier Group.”.

**Local steps**

- If not self.supplier\_group.
  - Return no value.
- If Platform.db.get\_value(“Supplier Group”, self.supplier\_group, “is\_group”).
  - Call the validation error handler Platform.throw(translated “Cannot select a Group type Supplier Group. Please select a non-group Supplier Group.”, title = translated “Invalid Supplier Group”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L214) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L116)

<a id="op-ede84a210d14ba"></a>
### Supplier.validate primary contact and address

`operation_enterprise_binding_enterprise_buying_doctype_supplier_supplier_supplier_validate_primary_contact_and_address`

**Inputs** self.

**Record and data access** read “Dynamic Link” via exists.

**Explicit failure paths** validation helper — translated “{0} {1} is not linked to Supplier {2}”.format(translated link\_doctype, Platform.bold(name), Platform.bold(self.name)).

**Local steps**

- For each tuple(fieldname, link\_doctype) in tuple(tuple(“supplier\_primary\_contact”, “Contact”), tuple(“supplier\_primary\_address”, “Address”)).
  - Set name from self.get(fieldname).
  - If (not name or not self.has\_value\_changed(fieldname)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not name → not self.has\_value\_changed(fieldname).
    - Continue with the next iteration or loop test.
  - If not Platform.db.exists(“Dynamic Link”, mapping(“parenttype” → link\_doctype, “parent” → name, “link\_doctype” → “Supplier”, “link\_name” → self.name)).
    - Call the validation error handler Platform.throw(translated “{0} {1} is not linked to Supplier {2}”.format(translated link\_doctype, Platform.bold(name), Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L213) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L875) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L115)

<a id="op-d9342f7bca741e"></a>
### Supplier.get supplier group details

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_get_supplier_group_details`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Supplier Group” via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(“Supplier Group”, self.supplier\_group, check\_permission = “read”).
- Set self.payment\_terms from empty text.
- Set self.accounts from list().
- If doc.accounts.
  - For each account in doc.accounts.
    - Set child from self.append(“accounts”).
    - Set child.company from account.company.
    - Set child.account from account.account.
- If doc.payment\_terms.
  - Set self.payment\_terms from doc.payment\_terms.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L204) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L303) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L62)

<a id="op-bd69be5b9c66a9"></a>
### Supplier.validate internal supplier

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_validate_internal_supplier`

**Inputs** self.

**Record and data access** read “Supplier” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Internal Supplier {0} already exists for {1}. Disable it to make this Supplier internal.”.format(internal\_supplier\_link, Platform.bold(self.represents\_company)).

**Local steps**

- If not self.is\_internal\_supplier.
  - Set self.represents\_company from empty text.
- If self.disabled.
  - Return no value.
- Set internal\_supplier from Platform.db.get\_value(“Supplier”, mapping(“is\_internal\_supplier” → 1, “represents\_company” → self.represents\_company, “disabled” → 0, “name” → tuple(“!=”, self.name)), “name”).
- If internal\_supplier.
  - Set internal\_supplier\_link from get\_link\_to\_form(“Supplier”, internal\_supplier).
  - Call the validation error handler Platform.throw(translated “Internal Supplier {0} already exists for {1}. Disable it to make this Supplier internal.”.format(internal\_supplier\_link, Platform.bold(self.represents\_company)), title = translat ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L206) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L309) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L68)

<a id="op-f239d7c6623099"></a>
### Supplier.create primary contact

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_create_primary_contact`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies make\_contact.
- If not self.supplier\_primary\_contact.
  - If (self.mobile\_no or self.email\_id).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.mobile\_no → self.email\_id.
    - Set contact from make\_contact(self).
    - Evaluate self.db\_set(“supplier\_primary\_contact”, contact.name).
    - Evaluate self.db\_set(“mobile\_no”, self.mobile\_no).
    - Evaluate self.db\_set(“email\_id”, self.email\_id).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L203) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L302) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L61)

<a id="op-8fbc0d76efd2c7"></a>
### Supplier.create primary address

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_create_primary_address`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Bind dependencies get\_address\_display.
- Bind dependencies make\_address.
- If (self.flags.is\_new\_doc and self.get(“address\_line1”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.flags.is\_new\_doc → self.get(“address\_line1”).
  - Set address from make\_address(self).
  - Set address\_display from get\_address\_display(address.name).
  - Evaluate self.db\_set(“supplier\_primary\_address”, address.name).
  - Evaluate self.db\_set(“primary\_address”, address\_display).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0026.json#L202) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L301) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L60)

<a id="op-b28b2d50481cd2"></a>
### Supplier.on trash

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_on_trash`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- If self.supplier\_primary\_contact.
  - Evaluate self.db\_set(“supplier\_primary\_contact”, no value).
- If self.supplier\_primary\_address.
  - Evaluate self.db\_set(“supplier\_primary\_address”, no value).
- Evaluate delete\_contact\_and\_address(“Supplier”, self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L3104) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L305) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L64)

<a id="op-a9f8f5da6f0b2d"></a>
### Supplier.before rename

`operation_enterprise_buying_record_definitions_supplier_business_behavior_supplier_before_rename`

**Inputs** self, olddn, newdn, merge = false.

**Local steps**

- If merge.
  - Evaluate validate\_party\_currency\_before\_merging(“Supplier”, olddn, newdn).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0348.json#L3261) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L299) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L58)
