# Shared transaction rules · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Budget controller

<a id="op-89676bc35c2deb"></a>
### Budget Validation.warn

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_warn`

**Inputs** self, msg.

**State and service calls** msgprint with msg.

**Local steps**

- Evaluate Platform.msgprint(msg, translated “Budget Exceeded”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L6192) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L411)

<a id="op-76a72db607aa18"></a>
### Budget Validation.execute action

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_execute_action`

**Inputs** self, action, msg.

**Explicit results** no value.

**Local steps**

- If (self.exception\_approver\_role and self.exception\_approver\_role belongs to Platform.get\_roles(Platform.session.user)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.exception\_approver\_role → self.exception\_approver\_role belongs to Platform.get\_roles(Platform.session.user).
  - Evaluate self.warn(msg).
  - Return no value.
- If action equals “Warn”.
  - Evaluate self.warn(msg).
- If action equals “Stop”.
  - Evaluate self.stop(msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [warn](operations-011.md#op-89676bc35c2deb), [stop](operations-010.md#op-514ef58828310c).

**Values supplied outside this operation** effective access from Platform.get\_roles(Platform.session.user).

**Boundaries to resolve** callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0370.json#L6273) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L389)

<a id="op-473ac16802a346"></a>
### Budget Validation.handle individual doctype action

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_individual_record_type_action`

**Inputs** self, key, config, budget, budget\_amt, existing\_amt, current\_amt, acc\_monthly\_budget.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If config.applies.
  - Set currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - Set annual\_diff from flt(((existing\_amt + current\_amt) − budget\_amt), self.amount\_precision).
  - If annual\_diff &gt; 0.
    - Set \_msg from translated “Annual Budget for Account {0} against {1}: {2} is {3}. It will be exceeded by {4}”.format(Platform.bold(key at 2), Platform.bold(Platform.unscrub(key at 0)), Platform.bold(key at 1), Platform.b ….
    - Evaluate self.execute\_action(config.action\_for\_annual, \_msg).
  - Set monthly\_diff from flt(((existing\_amt + current\_amt) − acc\_monthly\_budget), self.amount\_precision).
  - If monthly\_diff &gt; 0.
    - Set \_msg from translated “Accumulated Monthly Budget for Account {0} against {1}: {2} is {3}. It will be exceeded by {4}”.format(Platform.bold(key at 2), Platform.bold(Platform.unscrub(key at 0)), Platform.bold(key at 1 ….
    - Evaluate self.execute\_action(config.action\_for\_monthly, \_msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [execute action](operations-011.md#op-76a72db607aa18).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L401)

<a id="op-b163a6fd9d390a"></a>
### Budget Validation.handle purchase order overlimit

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_purchase_order_overlimit`

**Inputs** self, key, v\_map.

**Local steps**

- Evaluate self.handle\_individual\_doctype\_action(key, Platform.\_dict(mapping(“applies” → v\_map.budget\_doc.applicable\_on\_purchase\_order, “action\_for\_annual” → v\_map.budget\_doc.action\_if\_annual\_budget\_exceeded\_on\_po, “ ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle individual doctype action](operations-011.md#op-473ac16802a346).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L780) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L699) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L403)

<a id="op-a642cdc98feca7"></a>
### Budget Validation.handle material request overlimit

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_material_request_overlimit`

**Inputs** self, key, v\_map.

**Local steps**

- Evaluate self.handle\_individual\_doctype\_action(key, Platform.\_dict(mapping(“applies” → v\_map.budget\_doc.applicable\_on\_material\_request, “action\_for\_annual” → v\_map.budget\_doc.action\_if\_annual\_budget\_exceeded\_on\_mr, ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle individual doctype action](operations-011.md#op-473ac16802a346).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L975) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L402)

<a id="op-da995517eaa398"></a>
### Budget Validation.handle actual expense overlimit

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_actual_expense_overlimit`

**Inputs** self, key, v\_map.

**Local steps**

- Evaluate self.handle\_individual\_doctype\_action(key, Platform.\_dict(mapping(“applies” → v\_map.budget\_doc.applicable\_on\_booking\_actual\_expenses, “action\_for\_annual” → v\_map.budget\_doc.action\_if\_annual\_budget\_exceeded ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle individual doctype action](operations-011.md#op-473ac16802a346).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L1170) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L397)

<a id="op-ff482729c355c1"></a>
### Budget Validation.handle actions

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_actions`

**Inputs** self, key, v\_map.

**Local steps**

- Evaluate self.handle\_purchase\_order\_overlimit(key, v\_map).
- Evaluate self.handle\_material\_request\_overlimit(key, v\_map).
- Evaluate self.handle\_actual\_expense\_overlimit(key, v\_map).
- Evaluate self.handle\_cumulative\_overlimit(key, v\_map).

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle purchase order overlimit](operations-011.md#op-b163a6fd9d390a), [handle material request overlimit](operations-011.md#op-a642cdc98feca7), [handle actual expense overlimit](operations-011.md#op-da995517eaa398), [handle cumulative overlimit](operations-011.md#op-8cbce29643b329).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L1365) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L396)

<a id="op-8cbce29643b329"></a>
### Budget Validation.handle cumulative overlimit

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_cumulative_overlimit`

**Inputs** self, key, v\_map.

**Local steps**

- If v\_map.budget\_doc.applicable\_on\_cumulative\_expense.
  - Evaluate self.handle\_cumulative\_overlimit\_for\_monthly(key, v\_map).
  - Evaluate self.handle\_cumulative\_overlimit\_for\_annual(key, v\_map).

If control reaches the end, it returns no value.

**Methods declared on this owner** [handle cumulative overlimit for monthly](operations-011.md#op-c3d939b07f2dc1), [handle cumulative overlimit for annual](operations-011.md#op-f29b445c867eca).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L1526) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L398)

<a id="op-6a4962f50fa5f4"></a>
### Budget Validation.budget applicable for

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_budget_applicable_for`

**Inputs** self, v\_map, current\_amt.

**Declared result** str.

**Explicit results** “+”.join(doctypes).

**Local steps**

- Set budget\_doc from v\_map.budget\_doc.
- Set doctypes from list().
- If (budget\_doc.applicable\_on\_purchase\_order and v\_map.ordered\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in budget\_doc.applicable\_on\_purchase\_order → v\_map.ordered\_amount.
  - Evaluate doctypes.append(“Purchase Order”).
- If (budget\_doc.applicable\_on\_material\_request and v\_map.requested\_amount).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in budget\_doc.applicable\_on\_material\_request → v\_map.requested\_amount.
  - Evaluate doctypes.append(“Material Request”).
- If (budget\_doc.applicable\_on\_booking\_actual\_expenses and v\_map.actual\_expense).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in budget\_doc.applicable\_on\_booking\_actual\_expenses → v\_map.actual\_expense.
  - Evaluate doctypes.append(“Actual Expense”).
- If current\_amt.
  - Evaluate doctypes.append(“This Document”).
- Set doctypes from list of formatted text '{x}' for x drawn from doctypes.
  - Draw x from doctypes.
- Return “+”.join(doctypes).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L1647) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L383)

<a id="op-c3d939b07f2dc1"></a>
### Budget Validation.handle cumulative overlimit for monthly

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_cumulative_overlimit_for_monthly`

**Inputs** self, key, v\_map.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set current\_amt from ((v\_map.current\_ordered\_amount + v\_map.current\_requested\_amount) + v\_map.current\_actual\_exp\_amount).
- Set monthly\_diff from flt(((((v\_map.ordered\_amount + v\_map.requested\_amount) + v\_map.actual\_expense) + current\_amt) − v\_map.accumulated\_monthly\_budget), self.amount\_precision).
- If monthly\_diff &gt; 0.
  - Set currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - Set \_msg from translated “Accumulated Monthly Budget for Account {0} against {1} {2} is {3}. It will be collectively ({4}) exceeded by {5}”.format(Platform.bold(key at 2), Platform.bold(Platform.unscrub(key at 0)), Plat ….
  - Evaluate self.execute\_action(v\_map.budget\_doc.action\_if\_accumulated\_monthly\_exceeded\_on\_cumulative\_expense, \_msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [budget applicable for](operations-011.md#op-6a4962f50fa5f4), [execute action](operations-011.md#op-76a72db607aa18).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L120) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L696) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L400)

<a id="op-f29b445c867eca"></a>
### Budget Validation.handle cumulative overlimit for annual

`operation_enterprise_controllers_budget_controller_business_behavior_budget_validation_handle_cumulative_overlimit_for_annual`

**Inputs** self, key, v\_map.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set current\_amt from ((v\_map.current\_ordered\_amount + v\_map.current\_requested\_amount) + v\_map.current\_actual\_exp\_amount).
- Set total\_diff from flt(((((v\_map.ordered\_amount + v\_map.requested\_amount) + v\_map.actual\_expense) + current\_amt) − v\_map.budget\_amount), self.amount\_precision).
- If total\_diff &gt; 0.
  - Set currency from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).
  - Set \_msg from translated “Annual Budget for Account {0} against {1} {2} is {3}. It will be collectively ({4}) exceeded by {5}”.format(Platform.bold(key at 2), Platform.bold(Platform.unscrub(key at 0)), Platform.bold(key ….
  - Evaluate self.execute\_action(v\_map.budget\_doc.action\_if\_annual\_exceeded\_on\_cumulative\_expense, \_msg).

If control reaches the end, it returns no value.

**Methods declared on this owner** [budget applicable for](operations-011.md#op-6a4962f50fa5f4), [execute action](operations-011.md#op-76a72db607aa18).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L399)

## Service · Buying controller

<a id="op-72fd5db5a31c44"></a>
### Buying Controller.setup

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_setup`

**Inputs** self.

**Local steps**

- Set self.flags.ignore\_permlevel\_for\_fields from list(“buying\_price\_list”, “price\_list\_currency”).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0371.json#L3033) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L437)

<a id="op-84e8c8a9b37d1e"></a>
### Buying Controller.validate

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate`

**Inputs** self.

**Record and data access** read “Supplier” via get\_value.

**Local steps**

- Evaluate validate\_terms\_and\_conditions(self.get(“tc\_name”), “buying”).
- Evaluate self.set\_rate\_for\_standalone\_debit\_note().
- Evaluate super().validate().
- If (getattr(self, “supplier”, no value) and not self.supplier\_name).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in getattr(self, “supplier”, no value) → not self.supplier\_name.
  - Set self.supplier\_name from Platform.db.get\_value(“Supplier”, self.supplier, “supplier\_name”).
- Evaluate self.validate\_items().
- Evaluate self.set\_qty\_as\_per\_stock\_uom().
- Evaluate self.validate\_stock\_or\_nonstock\_items().
- Evaluate self.validate\_deduct\_with\_valuation\_taxes().
- Evaluate self.validate\_warehouse().
- Evaluate self.validate\_from\_warehouse().
- Evaluate self.set\_supplier\_address().
- Evaluate self.validate\_asset\_return().
- Evaluate self.validate\_auto\_repeat\_subscription\_dates().
- Evaluate self.create\_package\_for\_transfer().
- If self.doctype equals “Purchase Invoice”.
  - Evaluate self.validate\_purchase\_receipt\_if\_update\_stock().
  - If not self.update\_stock.
    - Evaluate validate\_duplicate\_items(self).
- If (self.doctype equals “Purchase Receipt” or (self.doctype equals “Purchase Invoice” and self.update\_stock)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → (self.doctype equals “Purchase Invoice” and self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.update\_stock.
  - Evaluate self.validate\_purchase\_return().
  - Evaluate self.validate\_rejected\_warehouse().
  - Evaluate self.validate\_accepted\_rejected\_qty().
  - Evaluate validate\_for\_items(self).
  - Evaluate self.validate\_for\_subcontracting().
  - If self.get(“is\_old\_subcontracting\_flow”).
    - Evaluate self.create\_raw\_materials\_supplied\_or\_received().
  - Evaluate self.set\_landed\_cost\_voucher\_amount().
- If self.doctype belongs to tuple(“Purchase Receipt”, “Purchase Invoice”).
  - Evaluate self.update\_valuation\_rate().
  - Evaluate self.sync\_accepted\_packages().
  - Evaluate self.set\_serial\_and\_batch\_bundle().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set rate for standalone debit note](operations-012.md#op-c3e0ab01f83f40), [validate items](operations-014.md#op-d06f798f24a326), [set qty as per stock uom](operations-013.md#op-253a0adebafa0b), [validate stock or nonstock items](operations-012.md#op-015fe9ad21d130), [validate deduct with valuation taxes](operations-012.md#op-6ad3e58515b45a), [validate from warehouse](operations-012.md#op-106884628087fb), [set supplier address](operations-012.md#op-993535efe00882), [validate asset return](operations-012.md#op-f6182ed95ebe7a), [create package for transfer](operations-011.md#op-62fe39b5ae43d9), [validate purchase return](operations-013.md#op-aeca9a901a720e), [validate accepted rejected qty](operations-013.md#op-86c4a0e5bae100), [validate for subcontracting](operations-013.md#op-f4838850312b46), [update valuation rate](operations-012.md#op-a70f2c1e5a7dfa), [sync accepted packages](operations-011.md#op-5f2163c981ce17).

**Values supplied outside this operation** selected callable from getattr(self, “supplier”, no value).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L740) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L444)

<a id="op-b8ccce905458f6"></a>
### Buying Controller.onload

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_onload`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Stock Settings” via get\_single\_value · read “Company” via get\_value · resolve a document from “Terms and Conditions” via get\_cached\_doc.

**Local steps**

- Evaluate super().onload().
- Evaluate self.set\_onload(“backflush\_based\_on”, Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”)).
- If (self.docstatus equals 1 and self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus equals 1 → self.doctype belongs to list(“Purchase Receipt”, “Purchase Invoice”).
  - Evaluate self.set\_onload(“allow\_to\_make\_qc\_after\_submission”, Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”)).
- If (self.docstatus.is\_draft() and self.get(“company”) and not self.get(“terms”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.docstatus.is\_draft() → self.get(“company”) → not self.get(“terms”).
  - If not self.get(“tc\_name”).
    - Set self.tc\_name from Platform.get\_value(“Company”, self.company, “default\_buying\_terms”).
  - Set tnc from Platform.get\_cached\_doc(“Terms and Conditions”, self.tc\_name) when self.tc\_name, otherwise no value.
    - Value choice on self.tc\_name — true gives Platform.get\_cached\_doc(“Terms and Conditions”, self.tc\_name), false gives no value.
  - If (tnc and not tnc.disabled and tnc.get(“buying”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tnc → not tnc.disabled → tnc.get(“buying”).
    - Evaluate self.set\_missing\_terms\_for\_display().

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “backflush\_raw\_materials\_of\_subcontract\_based\_on”), Platform.get\_single\_value(“Stock Settings”, “allow\_to\_make\_quality\_inspection\_after\_purchase\_or\_delivery”) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L426)

<a id="op-77d9b102213c98"></a>
### Buying Controller.validate posting date with po

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_validate_posting_date_with_purchase_order`

**Inputs** self.

**Record and data access** read “Purchase Order” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated msg.

**Local steps**

- Set po\_list from set of x.purchase\_order for x drawn from self.items where x.purchase\_order.
  - Draw x from self.items, keep a combination only if (x.purchase\_order).
- If not po\_list.
  - Return no value.
- Set invalid\_po from list().
- Set po\_dates from Platform.\_dict(Platform.get\_all(“Purchase Order”, filters = mapping(“name” → list(“in”, po\_list)), fields = list(“name”, “transaction\_date”), as\_list = true)).
- For each po in po\_list.
  - Set po\_date from po\_dates at po.
  - If getdate(po\_date) &gt; getdate(self.posting\_date).
    - Evaluate invalid\_po.append(tuple(get\_link\_to\_form(“Purchase Order”, po), format\_date(po\_date))).
- If not invalid\_po.
  - Return no value.
- Set msg from translated text in the contract.format(Platform.bold(format\_date(self.posting\_date))).
- For each tuple(po, date) in invalid\_po.
  - Update msg using + formatted text &lt;li&gt;{po} ({date})&lt;/li&gt;.
- Update msg using + “&lt;/ul&gt;”.
- Call the validation error handler Platform.throw(translated msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L747) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L451)

<a id="op-62fe39b5ae43d9"></a>
### Buying Controller.create package for transfer

`operation_enterprise_controllers_buying_controller_business_behavior_buying_controller_create_package_for_transfer`

**Inputs** self.

**Declared result** no value.

**Record and data access** read doctype via get\_all · read “Serial and Batch Entry” via get\_all.

**Explicit results** no value.

**Local steps**

- If (self.is\_internal\_transfer() and (self.doctype equals “Purchase Receipt” or (self.doctype equals “Purchase Invoice” and self.update\_stock))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_internal\_transfer() → (self.doctype equals “Purchase Receipt” or (self.doctype equals “Purchase Invoice” and self.update\_stock)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → (self.doctype equals “Purchase Invoice” and self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.update\_stock.
  - Set field from “delivery\_note\_item” when self.doctype equals “Purchase Receipt”, otherwise “sales\_invoice\_item”.
    - Value choice on self.doctype equals “Purchase Receipt” — true gives “delivery\_note\_item”, false gives “sales\_invoice\_item”.
  - Set doctype from “Delivery Note Item” when self.doctype equals “Purchase Receipt”, otherwise “Sales Invoice Item”.
    - Value choice on self.doctype equals “Purchase Receipt” — true gives “Delivery Note Item”, false gives “Sales Invoice Item”.
  - Set ids from list of d.get(field) for d drawn from self.get(“items”) where d.get(field).
    - Draw d from self.get(“items”), keep a combination only if (d.get(field)).
  - Set bundle\_ids from mapping().
  - If ids.
    - For each bundle in Platform.get\_all(doctype, filters = mapping(“name” → tuple(“in”, ids)), fields = list(“serial\_and\_batch\_bundle”, “name”)).
      - Set bundle\_ids at bundle.name from bundle.serial\_and\_batch\_bundle.
  - Evaluate bundle\_ids.update(self.get\_component\_packages()).
  - If not bundle\_ids.
    - Return no value.
  - For each item in self.get(“items”).
    - Set reference from (item.get(field) or item.get(“delivery\_note\_packed\_item”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(field) → item.get(“delivery\_note\_packed\_item”).
    - If (reference and not item.serial\_and\_batch\_bundle and bundle\_ids.get(reference)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference → not item.serial\_and\_batch\_bundle → bundle\_ids.get(reference).
      - Set item.serial\_and\_batch\_bundle from self.make\_accepted\_package(item, bundle\_ids.get(reference)).
    - Otherwise.
      - If (not self.is\_new() and item.serial\_and\_batch\_bundle and next(generator of old\_item for old\_item drawn from self.get\_doc\_before\_save().items where (old\_item.name equals item.name and old\_item.qty differs fr ….
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_new() → item.serial\_and\_batch\_bundle → next(generator of old\_item for old\_item drawn from self.get\_doc\_before\_save().items where (old\_item.name equals item.name and old\_item.qty differs from item.qty), no value) → len(sabe bound to Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → item.serial\_and\_batch\_bundle, “serial\_no” → list(“is”, “not set”)), pluck = “name”)) equals 1.
        - Draw old\_item from self.get\_doc\_before\_save().items, keep a combination only if ((old\_item.name equals item.name and old\_item.qty differs from item.qty)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_item.name equals item.name → old\_item.qty differs from item.qty.
        - Evaluate Platform.set\_value(“Serial and Batch Entry”, sabe at 0, “qty”, item.qty).
    - If (reference and bundle\_ids.get(reference) and item.get(field)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference → bundle\_ids.get(reference) → item.get(field).
      - Evaluate self.set\_rejected\_package(item, bundle\_ids.get(reference)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get component packages](operations-011.md#op-56e0ff7a9cfadd), [make accepted package](operations-011.md#op-d2fb1d37ea2b72), [set rejected package](operations-011.md#op-769f0e41d2fc69).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L710) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L414)

<a id="op-2b38da3b8e273b"></a>
### Buying Controller.get component incoming rates

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_component_incoming_rates`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Packed Item” via get\_all.

**Explicit results** mapping() · Platform.\_dict(Platform.get\_all(“Packed Item”, filters = mapping(“name” → tuple(“in”, packed\_items)), fields = list(“name”, “incoming\_rate”), as\_list = true)).

**Local steps**

- Set packed\_items from list of d.delivery\_note\_packed\_item for d drawn from self.get(“items”) where d.get(“delivery\_note\_packed\_item”).
  - Draw d from self.get(“items”), keep a combination only if (d.get(“delivery\_note\_packed\_item”)).
- If not packed\_items.
  - Return mapping().
- Return Platform.\_dict(Platform.get\_all(“Packed Item”, filters = mapping(“name” → tuple(“in”, packed\_items)), fields = list(“name”, “incoming\_rate”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L138) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1038) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L278)

<a id="op-56e0ff7a9cfadd"></a>
### Buying Controller.get component packages

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_component_packages`

**Inputs** self.

**Declared result** dict.

**Record and data access** read “Packed Item” via get\_all.

**Explicit results** mapping() · Platform.\_dict(Platform.get\_all(“Packed Item”, filters = mapping(“name” → tuple(“in”, packed\_items)), fields = list(“name”, “serial\_and\_batch\_bundle”), as\_list = true)).

**Local steps**

- Set packed\_items from list of d.delivery\_note\_packed\_item for d drawn from self.get(“items”) where d.get(“delivery\_note\_packed\_item”).
  - Draw d from self.get(“items”), keep a combination only if (d.get(“delivery\_note\_packed\_item”)).
- If not packed\_items.
  - Return mapping().
- Return Platform.\_dict(Platform.get\_all(“Packed Item”, filters = mapping(“name” → tuple(“in”, packed\_items)), fields = list(“name”, “serial\_and\_batch\_bundle”), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L139) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1039) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L279)

<a id="op-d2fb1d37ea2b72"></a>
### Buying Controller.make accepted package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_make_accepted_package`

**Inputs** self, row, package.

**Declared result** str.

**Explicit results** self.make\_package\_for\_transfer(package, row.from\_warehouse, type\_of\_transaction = “Outward”, do\_not\_submit = true, qty = get\_stock\_qty(row, row.qty)) · empty text · self.make\_package\_for\_transfer(package, row.warehouse, type\_of\_transaction = “Inward”, do\_not\_submit = true, qty = get\_stock\_qty(row, row.qty), exclude\_serial\_nos = self.get\_rejected\_serial\_nos(row)).

**Local steps**

- If not self.has\_rejected\_stock(row).
  - Return self.make\_package\_for\_transfer(package, row.from\_warehouse, type\_of\_transaction = “Outward”, do\_not\_submit = true, qty = get\_stock\_qty(row, row.qty)).
- If not flt(row.stock\_qty).
  - Return empty text.
- Return self.make\_package\_for\_transfer(package, row.warehouse, type\_of\_transaction = “Inward”, do\_not\_submit = true, qty = get\_stock\_qty(row, row.qty), exclude\_serial\_nos = self.get\_rejected\_serial\_nos(row)).

**Methods declared on this owner** [has rejected stock](operations-013.md#op-7619219c6072c9), [get rejected serial nos](operations-011.md#op-7b323d39d35438).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1065) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L305)

<a id="op-754fd3428e8e46"></a>
### Buying Controller.get delivered package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_delivered_package`

**Inputs** self, row.

**Declared result** (str bitwise or no value).

**Record and data access** read doctype via get\_value.

**Explicit results** no value · Platform.db.get\_value(doctype, row.get(field), “serial\_and\_batch\_bundle”).

**Local steps**

- Set field from “delivery\_note\_item” when self.doctype equals “Purchase Receipt”, otherwise “sales\_invoice\_item”.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives “delivery\_note\_item”, false gives “sales\_invoice\_item”.
- Set doctype from “Delivery Note Item” when self.doctype equals “Purchase Receipt”, otherwise “Sales Invoice Item”.
  - Value choice on self.doctype equals “Purchase Receipt” — true gives “Delivery Note Item”, false gives “Sales Invoice Item”.
- If not row.get(field).
  - Return no value.
- Return Platform.db.get\_value(doctype, row.get(field), “serial\_and\_batch\_bundle”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L142) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1042) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L282)

<a id="op-769f0e41d2fc69"></a>
### Buying Controller.set rejected package

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_set_rejected_package`

**Inputs** self, row, package.

**Declared result** no value.

**State and service calls** request set\_value on “Serial and Batch Bundle”.

**Explicit results** no value.

**Local steps**

- If (not self.has\_rejected\_stock(row) or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.has\_rejected\_stock(row) → self.is\_return.
  - Return no value.
- If (row.get(“rejected\_serial\_and\_batch\_bundle”) or not row.rejected\_warehouse).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in row.get(“rejected\_serial\_and\_batch\_bundle”) → not row.rejected\_warehouse.
  - Return no value.
- Set row.rejected\_serial\_and\_batch\_bundle from self.make\_package\_for\_transfer(package, row.rejected\_warehouse, type\_of\_transaction = “Inward”, do\_not\_submit = true, qty = get\_stock\_qty(row, row.rejected\_qty), exclude\_serial\_nos = self.get\_accepted\_seri ….
- Evaluate Platform.db.set\_value(“Serial and Batch Bundle”, row.rejected\_serial\_and\_batch\_bundle, “is\_rejected”, 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [has rejected stock](operations-013.md#op-7619219c6072c9), [get accepted serial nos](operations-011.md#op-6a556cf244400a).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1066) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L306)

<a id="op-6a556cf244400a"></a>
### Buying Controller.get accepted serial nos

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_accepted_serial_nos`

**Inputs** self, row.

**Declared result** list.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** list() · Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → row.serial\_and\_batch\_bundle, “serial\_no” → tuple(“is”, “set”)), pluck = “serial\_no”).

**Local steps**

- If not row.get(“serial\_and\_batch\_bundle”).
  - Return list().
- Return Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → row.serial\_and\_batch\_bundle, “serial\_no” → tuple(“is”, “set”)), pluck = “serial\_no”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L135) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1035) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L275)

<a id="op-5f2163c981ce17"></a>
### Buying Controller.sync accepted packages

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_sync_accepted_packages`

**Inputs** self.

**Declared result** no value.

**Record and data access** read “Serial and Batch Bundle” via get\_value.

**State and service calls** request delete\_doc for “Serial and Batch Bundle”.

**Explicit results** no value.

**Local steps**

- If (not self.is\_internal\_receipt() or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_internal\_receipt() → self.is\_return.
  - Return no value.
- For each row in self.get(“items”).
  - Set package from row.get(“serial\_and\_batch\_bundle”).
  - If not package.
    - Continue with the next iteration or loop test.
  - Set details from Platform.db.get\_value(“Serial and Batch Bundle”, package, list(“warehouse”, “type\_of\_transaction”, “docstatus”), as\_dict = true).
  - If (not details or details.docstatus differs from 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not details → details.docstatus differs from 0.
    - Continue with the next iteration or loop test.
  - If self.has\_rejected\_stock(row).
    - Set wanted from tuple(row.warehouse, “Inward”).
  - Otherwise.
    - Set wanted from tuple(row.from\_warehouse, “Outward”).
  - If tuple(details.warehouse, details.type\_of\_transaction) equals wanted.
    - Continue with the next iteration or loop test.
  - Set row.serial\_and\_batch\_bundle from self.make\_accepted\_package(row, (self.get\_delivered\_package(row) or package)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get\_delivered\_package(row) → package.
  - Evaluate Platform.delete\_doc(“Serial and Batch Bundle”, package, force = true, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is internal receipt](operations-013.md#op-df2f3b164c398c), [has rejected stock](operations-013.md#op-7619219c6072c9), [make accepted package](operations-011.md#op-d2fb1d37ea2b72), [get delivered package](operations-011.md#op-754fd3428e8e46).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1068) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L308)

<a id="op-7b323d39d35438"></a>
### Buying Controller.get rejected serial nos

`operation_enterprise_binding_enterprise_controllers_buying_controller_buyingcontroller_get_rejected_serial_nos`

**Inputs** self, row.

**Declared result** list.

**Record and data access** read “Serial and Batch Entry” via get\_all.

**Explicit results** list() · Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → row.rejected\_serial\_and\_batch\_bundle, “serial\_no” → tuple(“is”, “set”)), pluck = “serial\_no”) · get\_serial\_nos(row.get(“rejected\_serial\_no”)).

**Local steps**

- If not flt(row.get(“rejected\_qty”)).
  - Return list().
- If row.get(“rejected\_serial\_and\_batch\_bundle”).
  - Return Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → row.rejected\_serial\_and\_batch\_bundle, “serial\_no” → tuple(“is”, “set”)), pluck = “serial\_no”).
- Return get\_serial\_nos(row.get(“rejected\_serial\_no”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L152) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1052) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L292)
