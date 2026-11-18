# Shared transaction rules · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-52db43878d9f32"></a>
### Update gl dict with app based fields

`operation_enterprise_binding_enterprise_controllers_accounts_controller_update_gl_dict_with_app_based_fields`

**Inputs** doc, gl\_dict.

**Local steps**

- For each method in Platform.get\_hooks(“update\_gl\_dict\_with\_app\_based\_fields”, default = list()).
  - Evaluate Platform.get\_attr(method)(doc, gl\_dict).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“update\_gl\_dict\_with\_app\_based\_fields”, default = list()), Platform.get\_attr(method).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1019) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L259)

<a id="op-eebb5ab40f2c24"></a>
### Get missing company details

`operation_enterprise_controllers_accounts_controller_business_behavior_get_missing_company_details`

**Inputs** doctype, docname.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read doctype via get\_value · read “Company” via get\_value.

**State and service calls** msgprint with translated “Some required Company details are missing. You don't have permission to update them. Please contact your Sys …” · msgprint with translated “Company Address is missing. You don't have permission to update it. Please contact your System Manager.” · msgprint with translated “Company Address is missing. You don't have permission to create an Address. Please contact your System Manager.”.

**Explicit results** no value · false · mapping(“company\_logo” → company\_details.get(“company\_logo”), “website” → company\_details.get(“website”), “phone\_no” → company\_details.get(“phone\_no”), “email” → company\_details.get(“email”), …).

**Local steps**

- Bind dependencies get\_address\_display\_list.
- Set company from Platform.db.get\_value(doctype, docname, “company”).
- If doctype belongs to list(“Purchase Order”, “Purchase Invoice”, “Request for Quotation”).
  - Set company\_address from Platform.db.get\_value(doctype, docname, “billing\_address”).
- Otherwise.
  - Set company\_address from Platform.db.get\_value(doctype, docname, “company\_address”).
- Set company\_details from Platform.get\_value(“Company”, company, list(“company\_logo”, “website”, “phone\_no”, “email”), as\_dict = true).
- Set required\_fields from list(company\_details.get(“phone\_no”), company\_details.get(“email”)).
- If (not all(required\_fields) and not Platform.has\_permission(“Company”, “write”, throw = false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not all(required\_fields) → not Platform.has\_permission(“Company”, “write”, throw = false).
  - Evaluate Platform.msgprint(translated “Some required Company details are missing. You don't have permission to update them. Please contact your Sys …”).
  - Return no value.
- If (not company\_address and not Platform.has\_permission(doctype, “write”, throw = false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not company\_address → not Platform.has\_permission(doctype, “write”, throw = false).
  - Evaluate Platform.msgprint(translated “Company Address is missing. You don't have permission to update it. Please contact your System Manager.”).
  - Return no value.
- Set address\_display\_list from get\_address\_display\_list(“Company”, company).
- Set address\_line from address\_display\_list at 0.get(“address\_line1”) when address\_display\_list, otherwise empty text.
  - Value choice on address\_display\_list — true gives address\_display\_list at 0.get(“address\_line1”), false gives empty text.
- Set needs\_new\_company\_address from not address\_line.
- If (needs\_new\_company\_address and not Platform.has\_permission(“Address”, “create”, throw = false)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in needs\_new\_company\_address → not Platform.has\_permission(“Address”, “create”, throw = false).
  - Evaluate Platform.msgprint(translated “Company Address is missing. You don't have permission to create an Address. Please contact your System Manager.”).
  - Return no value.
- Evaluate required\_fields.append(company\_address).
- Evaluate required\_fields.append(address\_line).
- If (all(required\_fields) and not needs\_optional\_company\_details(company, company\_details)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in all(required\_fields) → not needs\_optional\_company\_details(company, company\_details).
  - Return false.
- Return mapping(“company\_logo” → company\_details.get(“company\_logo”), “website” → company\_details.get(“website”), “phone\_no” → company\_details.get(“phone\_no”), “email” → company\_details.get(“email”), …).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “write”, throw = false), Platform.has\_permission(doctype, “write”, throw = false) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L114) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L376)

<a id="op-edb972ef163907"></a>
### Needs optional company details

`operation_enterprise_binding_enterprise_controllers_accounts_controller_needs_optional_company_details`

**Inputs** company, company\_details.

**Explicit results** false · company does not belong to skipped.

**Local steps**

- Bind dependencies get\_user\_settings.
- If (company\_details.get(“company\_logo”) and company\_details.get(“website”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in company\_details.get(“company\_logo”) → company\_details.get(“website”).
  - Return false.
- If not Platform.has\_permission(“Company”, “write”, doc = company, throw = false).
  - Return false.
- Set skipped from (Platform.parse\_json(get\_user\_settings(“Company”)).get(“skipped\_print\_details”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.parse\_json(get\_user\_settings(“Company”)).get(“skipped\_print\_details”) → list().
- Return company does not belong to skipped.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, “write”, doc = company, throw = false).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L241)

<a id="op-8a96f27572a4a5"></a>
### Update company master and address

`operation_enterprise_controllers_accounts_controller_business_behavior_update_company_master_and_address`

**Inputs** current\_doctype, name, company, details.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from mapping(“doctype” → “Address”, “address\_title” → details.get(“address\_title”), “address\_type” → details.get(“address\_type”), “address\_line1” → details.get(“address\_line1”), …) via get\_doc.

**State and service calls** request set\_value on “Company” · call insert on address\_doc.

**Explicit failure paths** validation helper — translated “You don't have permission to update this document. Please contact your System Manager.” · validation helper — translated “You don't have permission to update Company details. Please contact your System Manager.” · validation helper — translated “You don't have permission to create a Company Address. Please contact your System Manager.”.

**Local steps**

- Bind dependencies validate\_email\_address.
- If not Platform.has\_permission(current\_doctype, “write”, doc = name, throw = false).
  - Call the validation error handler Platform.throw(translated “You don't have permission to update this document. Please contact your System Manager.”, title = translated “Insufficient Permissions”).
- If not Platform.has\_permission(“Company”, “write”, doc = company, throw = false).
  - Call the validation error handler Platform.throw(translated “You don't have permission to update Company details. Please contact your System Manager.”, title = translated “Insufficient Permissions”).
- If isinstance(details, str).
  - Set details from Platform.parse\_json(details).
- If details.get(“email”).
  - Evaluate validate\_email\_address(details.get(“email”), throw = true).
- Set company\_fields from list(“company\_logo”, “website”, “phone\_no”, “email”).
- Set company\_fields\_to\_update from mapping of field → details.get(field) for field drawn from company\_fields where details.get(field).
  - Draw field from company\_fields, keep a combination only if (details.get(field)).
- If company\_fields\_to\_update.
  - Evaluate Platform.db.set\_value(“Company”, company, company\_fields\_to\_update).
- Set company\_address from details.get(“company\_address”).
- If details.get(“address\_line1”).
  - If not Platform.has\_permission(“Address”, “create”, throw = false).
    - Call the validation error handler Platform.throw(translated “You don't have permission to create a Company Address. Please contact your System Manager.”, title = translated “Insufficient Permissions”).
  - Set address\_doc from Platform.get\_doc(mapping(“doctype” → “Address”, “address\_title” → details.get(“address\_title”), “address\_type” → details.get(“address\_type”), “address\_line1” → details.get(“address\_line1”), …)).
  - Evaluate address\_doc.insert().
  - Set company\_address from address\_doc.name.
- Evaluate update\_doc\_company\_address(current\_doctype, name, company\_address, details).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(current\_doctype, “write”, doc = name, throw = false), Platform.has\_permission(“Company”, “write”, doc = company, throw = false) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0369.json#L5383) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L378)

<a id="op-92adf8615a3772"></a>
### Update doc company address

`operation_enterprise_controllers_accounts_controller_business_behavior_update_record_company_address`

**Inputs** current\_doctype, docname, company\_address, details.

**Record and data access** read current\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If not company\_address.
  - Return no value.
- Set address\_field\_map from mapping(“Purchase Order” → tuple(“billing\_address”, “billing\_address\_display”), “Purchase Invoice” → tuple(“billing\_address”, “billing\_address\_display”), “Sales Order” → tuple(“company\_address”, “company\_a ….
- Set tuple(address\_field, display\_field) from address\_field\_map.get(current\_doctype, tuple(“company\_address”, “company\_address\_display”)).
- Set current\_display from Platform.db.get\_value(current\_doctype, docname, display\_field).
- If (current\_display and not details.get(“address\_line1”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_display → not details.get(“address\_line1”).
  - Return no value.
- Bind dependencies DocType.
- Set DocType from DocType(current\_doctype).
- Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(getattr(DocType, display\_field), get\_address\_display(company\_address)).where(DocType.name equals docname).run().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(DocType, address\_field), getattr(DocType, display\_field).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L380)

<a id="op-b907b78e2a43b6"></a>
### Get qty in stock uom

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_qty_in_stock_uom`

**Inputs** item.

**Declared result** float.

**Explicit results** (flt(item.qty) × (flt(item.get(“conversion\_factor”)) or 1)).

**Local steps**

- Return (flt(item.qty) × (flt(item.get(“conversion\_factor”)) or 1)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(item.get(“conversion\_factor”)) → 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L993) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L233)

## Service · Budget controller

<a id="op-55e652c705daeb"></a>
### Budget Validation.initialize

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_initialize`

**Inputs** self, doc = no value, gl\_map = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If doc.
  - Set self.document\_type from doc.get(“doctype”).
  - Set self.doc from doc.
  - Set self.company from doc.get(“company”).
  - Set self.doc\_date from doc.get(“transaction\_date”).
- Otherwise.
  - If gl\_map.
    - Set self.document\_type from “GL Map”.
    - Set self.gl\_map from gl\_map.
    - Set self.company from gl\_map at 0.company.
    - Set self.doc\_date from gl\_map at 0.posting\_date.
- Set fy from get\_fiscal\_year(self.doc\_date).
- Set self.fiscal\_year from fy at 0.
- Set self.fy\_start\_date from fy at 1.
- Set self.fy\_end\_date from fy at 2.
- Evaluate self.get\_dimensions().
- Set self.exception\_approver\_role from Platform.get\_cached\_value(“Company”, self.company, “exception\_budget\_approver\_role”).
- Set self.amount\_precision from Platform.get\_precision(“Budget”, “budget\_amount”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get dimensions](operations-010.md#op-7dfa2acb0f87ef).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “exception\_budget\_approver\_role”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L122) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L700) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L404)

<a id="op-20b6cd527c0fcc"></a>
### Budget Validation.validate

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_validate`

**Inputs** self.

**Local steps**

- Evaluate self.build\_validation\_map().
- Evaluate self.validate\_for\_overbooking().

If control reaches the end, it returns no value.

**Methods declared on this owner** [build validation map](operations-010.md#op-6ce0d9ea478909), [validate for overbooking](operations-010.md#op-c9473800c48987).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L502) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L705) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L409)

<a id="op-6ce0d9ea478909"></a>
### Budget Validation.build validation map

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_build_validation_map`

**Inputs** self.

**Local steps**

- Evaluate self.build\_budget\_keys().
- Evaluate self.build\_item\_keys().
- Evaluate self.build\_to\_validate\_map().

If control reaches the end, it returns no value.

**Methods declared on this owner** [build budget keys](operations-010.md#op-0d74cde29da9b5), [build item keys](operations-010.md#op-f4a8f2411eaf0d), [build to validate map](operations-010.md#op-c798f77bebcfee).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L573) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L388)

<a id="op-a9cd16be7e0a53"></a>
### Budget Validation.initialize dict

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_initialize_mapping`

**Inputs** self, key.

**Explicit results** \_obj.

**Local steps**

- Set \_obj from Platform.\_dict(mapping(“budget\_amount” → self.budget\_map at key.budget\_amount, “budget\_doc” → self.budget\_map at key, “requested\_amount” → 0, “ordered\_amount” → 0, …)).
- Evaluate \_obj.update(mapping(“accumulated\_monthly\_budget” → get\_accumulated\_monthly\_budget(self.budget\_map at key.name, self.doc\_date))).
- If self.document\_type belongs to list(“Purchase Order”, “Material Request”).
  - Evaluate \_obj.update(mapping(“items\_to\_process” → self.item\_map at key)).
- Otherwise.
  - If self.document\_type equals “GL Map”.
    - Evaluate \_obj.update(mapping(“gl\_to\_process” → self.item\_map at key)).
- Return \_obj.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L664) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L405)

<a id="op-c1b623b3c3b3b3"></a>
### Budget Validation.overlap

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_overlap`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (self.budget\_keys bitwise and self.item\_keys).

**Local steps**

- Return (self.budget\_keys bitwise and self.item\_keys).

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L1095) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L407)

<a id="op-c798f77bebcfee"></a>
### Budget Validation.build to validate map

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_build_to_validate_map`

**Inputs** self.

**Local steps**

- Set self.to\_validate from Platform.\_dict().
- For each key in self.overlap.
  - Set self.to\_validate at key from self.initialize\_dict(key).

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize dict](operations-010.md#op-a9cd16be7e0a53).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L1153) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L387)

<a id="op-c9473800c48987"></a>
### Budget Validation.validate for overbooking

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_validate_for_overbooking`

**Inputs** self.

**Local steps**

- For each tuple(key, v) in self.to\_validate.items().
  - Evaluate self.get\_ordered\_amount(key).
  - Evaluate self.get\_requested\_amount(key).
  - Evaluate self.handle\_actions(key, v).
  - If self.document\_type equals “GL Map”.
    - Set v.current\_actual\_exp\_amount from sum(list of (x.debit − x.credit) for x drawn from v.get(“gl\_to\_process”, list())).
      - Draw x from v.get(“gl\_to\_process”, list()).
  - Evaluate self.get\_actual\_expense(key).
  - Evaluate self.handle\_actions(key, v).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get ordered amount](operations-010.md#op-ac4be91b81062b), [get requested amount](operations-010.md#op-387b3ae823ea92), [handle actions](operations-011.md#op-ff482729c355c1), [get actual expense](operations-010.md#op-e8f615915f9302).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L1274) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L410)

<a id="op-532c716b1d205f"></a>
### Budget Validation.get child nodes

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_get_child_nodes`

**Inputs** self, budget\_against, dimension.

**Record and data access** read budget\_against via get\_all.

**Explicit results** Platform.db.get\_all(budget\_against, filters = mapping(“lft” → list(“&gt;=”, lft), “rgt” → list(“&lt;=”, rgt)), as\_list = 1).

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_all(budget\_against, filters = mapping(“name” → dimension), fields = list(“lft”, “rgt”), as\_list = 1) at 0.
- Return Platform.db.get\_all(budget\_against, filters = mapping(“lft” → list(“&gt;=”, lft), “rgt” → list(“&lt;=”, rgt)), as\_list = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L1586) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L392)

<a id="op-458c528df8808f"></a>
### Budget Validation.budget keys

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_budget_keys`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.budget\_map.keys().

**Local steps**

- Return self.budget\_map.keys().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L1840) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L384)

<a id="op-0d74cde29da9b5"></a>
### Budget Validation.build budget keys

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_build_budget_keys`

**Inputs** self.

**Record and data access** read \_bud.budget\_against via get\_cached\_value.

**Local steps**

- Set self.budget\_map from OrderedDict().
- For each \_bud in self.get\_budget\_records().
  - Set budget\_against from Platform.scrub(\_bud.budget\_against).
  - Set dimension from \_bud.get(budget\_against).
  - If (\_bud.is\_tree and Platform.get\_cached\_value(\_bud.budget\_against, dimension, “is\_group”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_bud.is\_tree → Platform.get\_cached\_value(\_bud.budget\_against, dimension, “is\_group”).
    - Set child\_nodes from self.get\_child\_nodes(\_bud.budget\_against, dimension).
    - For each child in child\_nodes.
      - Set key from tuple(budget\_against, child at 0, \_bud.account).
      - Set self.budget\_map at key from \_bud.
  - Otherwise.
    - Set key from tuple(budget\_against, dimension, \_bud.account).
    - Set self.budget\_map at key from \_bud.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get budget records](operations-010.md#op-796c6df5e02bd1), [get child nodes](operations-010.md#op-532c716b1d205f).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(\_bud.budget\_against, dimension, “is\_group”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L1898) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L385)

<a id="op-29b830d6e4572f"></a>
### Budget Validation.item keys

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_item_keys`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** self.item\_map.keys().

**Local steps**

- Return self.item\_map.keys().

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L2273) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L406)

<a id="op-f4a8f2411eaf0d"></a>
### Budget Validation.build item keys

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_build_item_keys`

**Inputs** self.

**Local steps**

- Set self.item\_map from OrderedDict().
- If self.document\_type belongs to list(“Purchase Order”, “Material Request”).
  - For each itm in self.doc.items.
    - For each dim in self.dimensions.
      - If itm.get(dim.get(“fieldname”)).
        - Set key from tuple(dim.get(“fieldname”), itm.get(dim.get(“fieldname”)), itm.expense\_account).
        - Evaluate self.item\_map.setdefault(key, list()).append(itm).
- Otherwise.
  - If self.document\_type equals “GL Map”.
    - For each gl in self.gl\_map.
      - For each dim in self.dimensions.
        - If gl.get(dim.get(“fieldname”)).
          - Set key from tuple(dim.get(“fieldname”), gl.get(dim.get(“fieldname”)), gl.get(“account”)).
          - Evaluate self.item\_map.setdefault(key, list()).append(gl).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L2331) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L386)

<a id="op-7dfa2acb0f87ef"></a>
### Budget Validation.get dimensions

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_get_dimensions`

**Inputs** self.

**Record and data access** read “Accounting Dimension” via get\_all.

**Local steps**

- Set self.dimensions from list().
- For each \_x in Platform.db.get\_all(“Accounting Dimension”).
  - Evaluate self.dimensions.append(Platform.get\_lazy\_doc(“Accounting Dimension”, \_x.name)).
- Evaluate self.dimensions.extend(list(mapping(“fieldname” → “cost\_center”, “document\_type” → “Cost Center”), mapping(“fieldname” → “project”, “document\_type” → “Project”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L2909) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L393)

<a id="op-796c6df5e02bd1"></a>
### Budget Validation.get budget records

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_get_budget_records`

**Inputs** self.

**Declared result** list.

**Explicit results** \_budgets.

**Local steps**

- Set bud from qb.DocType(“Budget”).
- Set query from qb.from\_(bud).select(bud.name, bud.budget\_against, bud.company, bud.account, …).where((((bud.docstatus equals 1 bitwise and bud.company equals self.company) bitwise and bud.budget\_start\_date ≤ self.doc\_dat ….
- For each x in self.dimensions.
  - Set query from query.select(bud at x.get(“fieldname”)).
- Set \_budgets from query.run(as\_dict = true).
- For each x in \_budgets.
  - Set x.is\_tree from Platform.get\_meta(x.budget\_against).is\_tree.
- Return \_budgets.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L3177) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L391)

<a id="op-ac4be91b81062b"></a>
### Budget Validation.get ordered amount

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_get_ordered_amount`

**Inputs** self, key = no value.

**Local steps**

- If key.
  - Set po from qb.DocType(“Purchase Order”).
  - Set poi from qb.DocType(“Purchase Order Item”).
  - Set conditions from list().
  - Evaluate conditions.append(po.company.eq(self.company)).
  - Evaluate conditions.append(po.docstatus.eq(1)).
  - Evaluate conditions.append(po.status.ne(“Closed”)).
  - Evaluate conditions.append(po.transaction\_date at slice self.fy\_start\_date to self.fy\_end\_date).
  - Evaluate conditions.append(poi.amount.gt(poi.billed\_amt)).
  - Evaluate conditions.append(poi.expense\_account.eq(key at 2)).
  - Evaluate conditions.append(poi at key at 0.eq(key at 1)).
  - If ordered\_amount bound to nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).where(Criterion.all(conditions)).run(as\_dict = true).
    - Set self.to\_validate at key.ordered\_amount from (ordered\_amount at 0.amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in ordered\_amount at 0.amount → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L394)

<a id="op-387b3ae823ea92"></a>
### Budget Validation.get requested amount

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_get_requested_amount`

**Inputs** self, key = no value.

**Local steps**

- If key.
  - Set mr from qb.DocType(“Material Request”).
  - Set mri from qb.DocType(“Material Request Item”).
  - Set conditions from list().
  - Evaluate conditions.append(mr.company.eq(self.company)).
  - Evaluate conditions.append(mr.docstatus.eq(1)).
  - Evaluate conditions.append(mr.material\_request\_type.eq(“Purchase”)).
  - Evaluate conditions.append(mr.status.ne(“Stopped”)).
  - Evaluate conditions.append(mr.transaction\_date at slice self.fy\_start\_date to self.fy\_end\_date).
  - Evaluate conditions.append(mri.stock\_qty.gt(mri.ordered\_qty)).
  - Evaluate conditions.append(mri.expense\_account.eq(key at 2)).
  - Evaluate conditions.append(mri at key at 0.eq(key at 1)).
  - If requested\_amount bound to nested operand in the contract.select(nested operand in the contract(nested operand in the contract)).where(Criterion.all(conditions)).run(as\_dict = true).
    - Set self.to\_validate at key.requested\_amount from (requested\_amount at 0.amount or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in requested\_amount at 0.amount → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L395)

<a id="op-e8f615915f9302"></a>
### Budget Validation.get actual expense

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_get_actual_expense`

**Inputs** self, key = no value.

**Local steps**

- If key.
  - Set gl from qb.DocType(“GL Entry”).
  - Set query from qb.from\_(gl).select((nested operand in the contract(nested operand in the contract) − nested operand in the contract(nested operand in the contract)).as\_(“balance”)).where((((((nested operand in the contra ….
  - If actual\_expense bound to query.run(as\_dict = true).
    - Set self.to\_validate at key.actual\_expense from (actual\_expense at 0.balance or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in actual\_expense at 0.balance → 0.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L5593) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L390)

<a id="op-514ef58828310c"></a>
### Budget Validation.stop

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_stop`

**Inputs** self, msg.

**Explicit failure paths** validation helper with BudgetError — msg.

**Local steps**

- Call the validation error handler Platform.throw(msg, BudgetError, title = translated “Budget Exceeded”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L6100) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L704) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L408)
