# Company and master data · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Authorization control

[Record definition](../../../../data/record-types/authorization_control.json)

<a id="op-61ff363f924ecf"></a>
### Authorization Control.get appr user role

`operation_enterprise_setup_record_definitions_authorization_control_business_behavior_authorization_control_get_appr_user_role`

**Inputs** self, det, doctype\_name, total, based\_on, condition, master\_name, company.

**Record and data access** execute query text (SELECT, Authorization Rule).format(“%s”, “%s”, “%s”, “%s”, …).

**State and service calls** msgprint with translated “Not authorized since {0} exceeds limits”.format(translated based\_on).

**Explicit failure paths** validation helper — translated “Can be approved by {0}”.format(comma\_or((appr\_roles + appr\_users))).

**Local steps**

- Set tuple(amt\_list, appr\_users, appr\_roles) from tuple(list(), list(), list()).
- Set tuple(\_users, \_roles) from tuple(empty text, empty text).
- If det.
  - For each x in det.
    - Evaluate amt\_list.append(flt(x at 0)).
  - Set max\_amount from max(amt\_list).
  - Set app\_dtl from Platform.db.sql(query text (SELECT, Authorization Rule).format(“%s”, “%s”, “%s”, “%s”, …), tuple(doctype\_name, flt(max\_amount), total, based\_on, …)).
  - If not app\_dtl.
    - Set app\_dtl from Platform.db.sql(query text (SELECT, Authorization Rule).format(“%s”, “%s”, “%s”, “%s”, …), tuple(doctype\_name, flt(max\_amount), total, based\_on)).
  - For each d in app\_dtl.
    - If d at 0.
      - Evaluate appr\_users.append(d at 0).
    - If d at 1.
      - Evaluate appr\_roles.append(d at 1).
  - If (not has\_common(appr\_roles, Platform.get\_roles()) and not has\_common(appr\_users, list(session at “user”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not has\_common(appr\_roles, Platform.get\_roles()) → not has\_common(appr\_users, list(session at “user”)).
    - Evaluate Platform.msgprint(translated “Not authorized since {0} exceeds limits”.format(translated based\_on)).
    - Call the validation error handler Platform.throw(translated “Can be approved by {0}”.format(comma\_or((appr\_roles + appr\_users)))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L58) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L266)

<a id="op-b867ab212e01cc"></a>
### Authorization Control.validate auth rule

`operation_enterprise_setup_record_definitions_authorization_control_business_behavior_authorization_control_validate_authentication_rule`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** self, doctype\_name, total, based\_on, cond, company, master\_name.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L61) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L698) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L269)

<a id="op-127e67d8ac6e1e"></a>
### Authorization Control.bifurcate based on type

`operation_enterprise_setup_record_definitions_authorization_control_business_behavior_authorization_control_bifurcate_based_on_type`

**Inputs** self, doctype\_name, total, av\_dis, based\_on, doc\_obj, val, company.

**Explicit results** no value.

**Local steps**

- Set add\_cond from empty text.
- Set auth\_value from av\_dis.
- If val equals 1.
  - Update add\_cond using + “ and system\_user = {}”.format(Platform.db.escape(session at “user”)).
- Otherwise.
  - If val equals 2.
    - Update add\_cond using + (“ and system\_role IN (%s)” modulo or format “, ”.join(generator of Platform.db.escape(r) for r drawn from Platform.get\_roles())).
      - Draw r from Platform.get\_roles().
  - Otherwise.
    - Update add\_cond using + “ and ifnull(system\_user,'') = '' and ifnull(system\_role,'') = ''”.
- If based\_on equals “Grand Total”.
  - Set auth\_value from total.
- Otherwise.
  - If based\_on equals “Customerwise Discount”.
    - If doc\_obj.
      - If doc\_obj.doctype equals “Quotation”.
        - Set customer from doc\_obj.party\_name when doc\_obj.quotation\_to equals “Customer”, otherwise no value.
          - Value choice on doc\_obj.quotation\_to equals “Customer” — true gives doc\_obj.party\_name, false gives no value.
      - Otherwise.
        - Set customer from doc\_obj.get(“customer”).
      - If not customer.
        - Return no value.
      - Update add\_cond using + formatted text  and master\_name = {Platform.db.escape(customer)}.
- If based\_on belongs to tuple(“Itemwise Discount”, “Item Group wise Discount”).
  - If doc\_obj.
    - For each t in doc\_obj.get(“items”).
      - Set discount from flt(t.discount\_percentage).
      - If flt(t.price\_list\_rate).
        - Set discount from max(discount, flt((100 × (1 − (flt(nested operand in the contract.rate) ÷ flt(nested operand in the contract.price\_list\_rate)))), t.precision(“discount\_percentage”))).
      - Set master\_name from t.item\_code when based\_on equals “Itemwise Discount”, otherwise t.item\_group.
        - Value choice on based\_on equals “Itemwise Discount” — true gives t.item\_code, false gives t.item\_group.
      - Evaluate self.validate\_auth\_rule(doctype\_name, discount, based\_on, add\_cond, …).
- Otherwise.
  - Evaluate self.validate\_auth\_rule(doctype\_name, auth\_value, based\_on, add\_cond, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate auth rule](operations-001.md#op-b867ab212e01cc).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L57) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L265)

<a id="op-25a11ddb89c3a3"></a>
### Authorization Control.validate approving authority

`operation_enterprise_setup_record_definitions_authorization_control_business_behavior_authorization_control_validate_approving_authority`

**Inputs** self, doctype\_name, company, total, doc\_obj = empty text.

**Record and data access** read “Authorization Rule” via count · execute query text (SELECT, Authorization Rule) · execute query text (SELECT, Authorization Rule).format(“%s”, “, ”.join(generator of Platform.db.escape(r) for r drawn from Platform.get\_roles()), “, ”.join(generator of Platform.db.escape(b) for b drawn from final ….

**Explicit results** no value.

**Local steps**

- If not Platform.db.count(“Authorization Rule”).
  - Return no value.
- Set av\_dis from 0.
- If doc\_obj.
  - Set tuple(price\_list\_rate, base\_rate) from tuple(0, 0).
  - For each d in doc\_obj.get(“items”).
    - If (d.base\_price\_list\_rate or d.base\_rate).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.base\_price\_list\_rate → d.base\_rate.
      - Update price\_list\_rate using + ((flt(d.base\_price\_list\_rate) or flt(d.base\_rate)) × flt(d.qty)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.base\_price\_list\_rate) → flt(d.base\_rate).
      - Update base\_rate using + (flt(d.base\_rate) × flt(d.qty)).
  - If doc\_obj.get(“base\_discount\_amount”).
    - Update base\_rate using − flt(doc\_obj.base\_discount\_amount).
  - If price\_list\_rate.
    - Set av\_dis from (100 − flt(((base\_rate × 100) ÷ price\_list\_rate))).
- Set final\_based\_on from list(“Grand Total”, “Average Discount”, “Customerwise Discount”, “Itemwise Discount”, …).
- Set based\_on from list of x at 0 for x drawn from Platform.db.sql(query text (SELECT, Authorization Rule), tuple(doctype\_name, session at “user”, tuple(final\_based\_on), company)).
  - Draw x from Platform.db.sql(query text (SELECT, Authorization Rule), tuple(doctype\_name, session at “user”, tuple(final\_based\_on), company)).
- For each d in based\_on.
  - Evaluate self.bifurcate\_based\_on\_type(doctype\_name, total, av\_dis, d, …).
- For each r in based\_on.
  - If (r belongs to final\_based\_on and r does not belong to list(“Itemwise Discount”, “Item Group wise Discount”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in r belongs to final\_based\_on → r does not belong to list(“Itemwise Discount”, “Item Group wise Discount”).
    - Evaluate final\_based\_on.remove(r).
- Set based\_on from list of x at 0 for x drawn from Platform.db.sql(query text (SELECT, Authorization Rule).format(“%s”, “, ”.join(generator of nested operand in the contract.escape(r) for r drawn from nested operand in the c ….
  - Draw x from Platform.db.sql(query text (SELECT, Authorization Rule).format(“%s”, “, ”.join(generator of nested operand in the contract.db.escape(r) for r drawn from Platform.get\_roles()), “, ”.join(generator of nested ….
  - Draw r from Platform.get\_roles().
  - Draw b from final\_based\_on.
- For each d in based\_on.
  - Evaluate self.bifurcate\_based\_on\_type(doctype\_name, total, av\_dis, d, …).
- For each r in based\_on.
  - If (r belongs to final\_based\_on and r does not belong to list(“Itemwise Discount”, “Item Group wise Discount”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in r belongs to final\_based\_on → r does not belong to list(“Itemwise Discount”, “Item Group wise Discount”).
    - Evaluate final\_based\_on.remove(r).
- For each g in final\_based\_on.
  - Evaluate self.bifurcate\_based\_on\_type(doctype\_name, total, av\_dis, g, …).

If control reaches the end, it returns no value.

**Methods declared on this owner** [bifurcate based on type](operations-001.md#op-127e67d8ac6e1e).

**Values supplied outside this operation** effective access from Platform.get\_roles().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L697) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L268)

<a id="op-15455894ac5f7d"></a>
### Authorization Control.get value based rule

`operation_enterprise_setup_record_definitions_authorization_control_business_behavior_authorization_control_get_value_based_rule`

**Inputs** self, doctype\_name, employee, total\_claimed\_amount, company.

**Record and data access** execute query text (SELECT, Authorization Rule, Employee).

**Explicit results** rule.

**Local steps**

- Set val\_lst from list().
- Set val from Platform.db.sql(query text (SELECT, Authorization Rule, Employee), tuple(doctype\_name, employee, employee, total\_claimed\_amount, …)).
- If not val.
  - Set val from Platform.db.sql(query text (SELECT, Authorization Rule, Employee), tuple(doctype\_name, employee, employee, total\_claimed\_amount)).
- If val.
  - Set val\_lst from list of y at 0 for y drawn from val.
    - Draw y from val.
- Otherwise.
  - Evaluate val\_lst.append(0).
- Set max\_val from max(val\_lst).
- Set rule from Platform.db.sql(query text (SELECT, Authorization Rule, Employee), tuple(doctype\_name, company, employee, employee, …), as\_dict = 1).
- If not rule.
  - Set rule from Platform.db.sql(query text (SELECT, Authorization Rule, Employee), tuple(doctype\_name, employee, employee, flt(max\_val)), as\_dict = 1).
- Return rule.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L267)

## Record · Authorization rule

[Record definition](../../../../data/record-types/authorization_rule.json)

<a id="op-374eb1300a266f"></a>
### Authorization Rule.check duplicate entry

`operation_enterprise_setup_record_definitions_authorization_rule_business_behavior_authorization_rule_check_duplicate_entry`

**Inputs** self.

**Record and data access** execute query text (SELECT, Authorization Rule).

**Explicit failure paths** validation helper — translated “Duplicate Entry. Please check Authorization Rule {0}”.format(auth\_exists).

**Local steps**

- Set exists from Platform.db.sql(query text (SELECT, Authorization Rule), tuple(self.transaction, self.based\_on, cstr(self.system\_user), cstr(self.system\_role), …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.value → 0.
- Set auth\_exists from ((exists and exists at 0 at 0) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (exists and exists at 0 at 0) → empty text.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in exists → exists at 0 at 0.
- If auth\_exists.
  - Call the validation error handler Platform.throw(translated “Duplicate Entry. Please check Authorization Rule {0}”.format(auth\_exists)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L62) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L701) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L270)

<a id="op-2b69574cb8e487"></a>
### Authorization Rule.validate rule

`operation_enterprise_setup_record_definitions_authorization_rule_business_behavior_authorization_rule_validate_rule`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please enter Approving Role or Approving User” · validation helper — translated “Approving User cannot be same as user the rule is Applicable To” · validation helper — translated “Approving Role cannot be same as role the rule is Applicable To” · validation helper — translated “Cannot set authorization on basis of Discount for {0}”.format(self.transaction) · validation helper — translated “Discount must be between 0 and 100” · 1 additional forms in the steps below.

**Local steps**

- If (not self.approving\_role and not self.approving\_user).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.approving\_role → not self.approving\_user.
  - Call the validation error handler Platform.throw(translated “Please enter Approving Role or Approving User”).
- Otherwise.
  - If (self.system\_user and self.system\_user equals self.approving\_user).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.system\_user → self.system\_user equals self.approving\_user.
    - Call the validation error handler Platform.throw(translated “Approving User cannot be same as user the rule is Applicable To”).
  - Otherwise.
    - If (self.system\_role and self.system\_role equals self.approving\_role).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.system\_role → self.system\_role equals self.approving\_role.
      - Call the validation error handler Platform.throw(translated “Approving Role cannot be same as role the rule is Applicable To”).
    - Otherwise.
      - If (self.transaction belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”, “Stock Entry”) and self.based\_on belongs to list(“Average Discount”, “Customerwise Discount”, “Itemwise Discount” ….
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.transaction belongs to list(“Purchase Order”, “Purchase Receipt”, “Purchase Invoice”, “Stock Entry”) → self.based\_on belongs to list(“Average Discount”, “Customerwise Discount”, “Itemwise Discount”, “Item Group wise Discount”).
        - Call the validation error handler Platform.throw(translated “Cannot set authorization on basis of Discount for {0}”.format(self.transaction)).
      - Otherwise.
        - If (self.based\_on belongs to tuple(“Average Discount”, “Customerwise Discount”, “Itemwise Discount”, “Item Group wise Discount”) and not 0 ≤ flt(self.value) ≤ 100).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.based\_on belongs to tuple(“Average Discount”, “Customerwise Discount”, “Itemwise Discount”, “Item Group wise Discount”) → not 0 ≤ flt(self.value) ≤ 100.
          - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ flt(self.value) ≤ 100.
          - Call the validation error handler Platform.throw(translated “Discount must be between 0 and 100”).
        - Otherwise.
          - If (self.based\_on equals “Customerwise Discount” and not self.master\_name).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.based\_on equals “Customerwise Discount” → not self.master\_name.
            - Call the validation error handler Platform.throw(translated “Customer required for 'Customerwise Discount'”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L703) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L272)

<a id="op-ee4ef325bf2e68"></a>
### Authorization Rule.validate links

`operation_enterprise_binding_enterprise_setup_doctype_authorization_rule_authorization_rule_authorizationrule_validate_links`

**Inputs** self.

**Local steps**

- Set self.customer\_or\_item from mapping(“Customerwise Discount” → “Customer”, “Itemwise Discount” → “Item”, “Item Group wise Discount” → “Item Group”).get(self.based\_on, empty text).
- If not self.customer\_or\_item.
  - Set self.master\_name from empty text.
- Evaluate super().\_validate\_links().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L641) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L138)

<a id="op-de50777e001c94"></a>
### Authorization Rule.validate

`operation_enterprise_setup_record_definitions_authorization_rule_business_behavior_authorization_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_rule().
- Evaluate self.check\_duplicate\_entry().
- If not self.value.
  - Set self.value from 0.0.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate rule](operations-001.md#op-2b69574cb8e487), [check duplicate entry](operations-001.md#op-374eb1300a266f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L702) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L271)

## Record · Brand

[Record definition](../../../../data/record-types/brand.json)

<a id="op-f741a659b482bb"></a>
### Brand.validate

`operation_enterprise_binding_enterprise_setup_doctype_brand_brand_brand_validate`

**Inputs** self.

**Local steps**

- Bind dependencies validate\_item\_defaults.
- Evaluate validate\_item\_defaults(self.brand\_defaults).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L642) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L139)

<a id="op-3aaa8508f433a6"></a>
### Get brand defaults

`operation_enterprise_setup_record_definitions_brand_business_behavior_get_brand_defaults`

**Inputs** item, company.

**Record and data access** resolve a document from “Item” via get\_cached\_doc · resolve a document from “Brand” via get\_cached\_doc.

**Explicit results** row · Platform.\_dict().

**Local steps**

- Set item from Platform.get\_cached\_doc(“Item”, item).
- If item.brand.
  - Set brand from Platform.get\_cached\_doc(“Brand”, item.brand).
  - For each d in (brand.brand\_defaults or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in brand.brand\_defaults → list().
    - If d.company equals company.
      - Set row from d.as\_dict(no\_private\_properties = true).
      - Evaluate row.pop(“name”).
      - Return row.
- Return Platform.\_dict().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Item”, item), Platform.get\_cached\_doc(“Brand”, item.brand).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0682.json#L1574) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L706) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L274)

## Record · Company

[Record definition](../../../../data/record-types/company.json)

<a id="op-183dc71eb8cfe0"></a>
### Company.onload

`operation_enterprise_setup_record_definitions_company_business_behavior_company_onload`

**Inputs** self.

**Local steps**

- Evaluate load\_address\_and\_contact(self, “company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0682.json#L1847) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L722) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L290)

<a id="op-412da9ccea0ebf"></a>
### Company.check if transactions exist

`operation_enterprise_setup_record_definitions_company_business_behavior_company_check_if_transactions_exist`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “GL Entry” via exists · read “Stock Ledger Entry” via exists · execute query text (SELECT).format(doctype, “%s”).

**Explicit results** true · exists.

**Local steps**

- If (Platform.db.exists(“GL Entry”, mapping(“company” → self.name, “is\_cancelled” → 0)) or Platform.db.exists(“Stock Ledger Entry”, mapping(“company” → self.name, “is\_cancelled” → 0))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.exists(“GL Entry”, mapping(“company” → self.name, “is\_cancelled” → 0)) → Platform.db.exists(“Stock Ledger Entry”, mapping(“company” → self.name, “is\_cancelled” → 0)).
  - Return true.
- Set exists from false.
- For each doctype in list(“Sales Invoice”, “Delivery Note”, “Sales Order”, “Quotation”, …).
  - If Platform.db.sql(query text (SELECT).format(doctype, “%s”), self.name).
    - Set exists from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Return exists.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L69) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L713) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L281)

<a id="op-6ff24c3082f97a"></a>
### Company.validate

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate`

**Inputs** self.

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save().
- For each tuple(field, module) in tuple(tuple(“default\_selling\_terms”, “selling”), tuple(“default\_buying\_terms”, “buying”)).
  - If (not old\_doc or self.get(field) differs from old\_doc.get(field)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not old\_doc → self.get(field) differs from old\_doc.get(field).
    - Evaluate validate\_terms\_and\_conditions(self.get(field), module).
- Set self.update\_default\_account from false.
- If self.is\_new().
  - Set self.update\_default\_account from true.
- Evaluate self.validate\_abbr().
- Evaluate self.validate\_currency().
- Evaluate self.validate\_default\_accounts().
- Evaluate self.validate\_coa\_input().
- Evaluate self.validate\_perpetual\_inventory().
- Evaluate self.validate\_provisional\_account\_for\_non\_stock\_items().
- Evaluate self.check\_country\_change().
- Evaluate self.check\_parent\_changed().
- Evaluate self.set\_chart\_of\_accounts().
- Evaluate self.validate\_parent\_company().
- Evaluate self.set\_reporting\_currency().
- Evaluate self.validate\_inventory\_account\_settings().
- Evaluate self.validate\_warehouses().
- Evaluate self.cant\_change\_valuation\_method().
- Evaluate self.validate\_pending\_reposts(old\_doc).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate abbr](operations-001.md#op-53483bf9fee08a), [validate currency](operations-001.md#op-5bce385f3e6edd), [validate default accounts](operations-001.md#op-3be2dcf2c242a9), [validate coa input](operations-002.md#op-6f463628704ee6), [validate perpetual inventory](operations-002.md#op-6f3ca066ba0ed9), [validate provisional account for non stock items](operations-002.md#op-58f294eee0c281), [check country change](operations-002.md#op-a4ccb2b41c6b10), [check parent changed](operations-002.md#op-c3e293bcb72f26), [set chart of accounts](operations-002.md#op-8618353a493403), [validate parent company](operations-002.md#op-e48c8b10f592b2), [set reporting currency](operations-002.md#op-97248f668428d5), [validate inventory account settings](operations-001.md#op-c165a25f59a930), [validate warehouses](operations-001.md#op-664eb9e2d8453c), [cant change valuation method](operations-001.md#op-7c6689990f2f33), [validate pending reposts](operations-002.md#op-3c6dc41bf79a2c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L296)

<a id="op-7c6689990f2f33"></a>
### Company.cant change valuation method

`operation_enterprise_setup_record_definitions_company_business_behavior_company_cant_change_valuation_method`

**Inputs** self.

**Record and data access** execute query text (SELECT, Stock Ledger Entry, Item).

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Can't change the valuation method, as there are transactions against some items which do not have its own va …”.

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- Set previous\_valuation\_method from doc\_before\_save.get(“valuation\_method”).
- If (previous\_valuation\_method and previous\_valuation\_method differs from self.valuation\_method).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_valuation\_method → previous\_valuation\_method differs from self.valuation\_method.
  - Set sle from Platform.db.sql(query text (SELECT, Stock Ledger Entry, Item), self.name).
  - If sle.
    - Call the validation error handler Platform.throw(translated “Can't change the valuation method, as there are transactions against some items which do not have its own va …”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L68) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L711) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L279)

<a id="op-c165a25f59a930"></a>
### Company.validate inventory account settings

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_inventory_account_settings`

**Inputs** self.

**Record and data access** read “Stock Ledger Entry” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot enable Item-wise Inventory Account, as there are existing Stock Ledger Entries for the company {0} wi …”.format(bold(self.name)).

**Local steps**

- Set doc\_before\_save from self.get\_doc\_before\_save().
- If not doc\_before\_save.
  - Return no value.
- If (doc\_before\_save.enable\_item\_wise\_inventory\_account differs from self.enable\_item\_wise\_inventory\_account and Platform.db.get\_value(“Stock Ledger Entry”, mapping(“is\_cancelled” → 0, “company” → self.name),  ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_before\_save.enable\_item\_wise\_inventory\_account differs from self.enable\_item\_wise\_inventory\_account → Platform.db.get\_value(“Stock Ledger Entry”, mapping(“is\_cancelled” → 0, “company” → self.name), “name”) → doc\_before\_save.enable\_perpetual\_inventory.
  - Call the validation error handler Platform.throw(translated “Cannot enable Item-wise Inventory Account, as there are existing Stock Ledger Entries for the company {0} wi …”.format(bold(self.name)), title = translated “Cannot Change Invento ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0682.json#L4049) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L734) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L301)

<a id="op-664eb9e2d8453c"></a>
### Company.validate warehouses

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_warehouses`

**Inputs** self.

**Record and data access** read “Warehouse” via get\_value.

**Explicit failure paths** validation helper — translated “Group Warehouses cannot be used in transactions. Please change the value of {0}”.format(bold(label)) · validation helper — translated “{0} {1} does not belong to company {2}”.format(bold(label), bold(warehouse), bold(self.name)) · validation helper — translated “{0} {1} is disabled”.format(bold(label), bold(warehouse)) · validation helper — translated “{0} must be a Transit Warehouse”.format(bold(label)).

**Local steps**

- For each fieldname in tuple(“default\_warehouse”, “sample\_retention\_warehouse”, “default\_in\_transit\_warehouse”, “default\_warehouse\_for\_sales\_return”, …).
  - Set warehouse from self.get(fieldname).
  - If not warehouse.
    - Continue with the next iteration or loop test.
  - Set details from Platform.db.get\_value(“Warehouse”, warehouse, list(“is\_group”, “company”, “disabled”, “warehouse\_type”), as\_dict = true).
  - If not details.
    - Continue with the next iteration or loop test.
  - Set label from translated self.meta.get\_label(fieldname).
  - If details.is\_group.
    - Call the validation error handler Platform.throw(translated “Group Warehouses cannot be used in transactions. Please change the value of {0}”.format(bold(label)), title = translated “Incorrect Warehouse”).
  - If details.company differs from self.name.
    - Call the validation error handler Platform.throw(translated “{0} {1} does not belong to company {2}”.format(bold(label), bold(warehouse), bold(self.name)), title = translated “Incorrect Warehouse”).
  - If not self.is\_value\_new\_or\_changed(fieldname).
    - Continue with the next iteration or loop test.
  - If details.disabled.
    - Call the validation error handler Platform.throw(translated “{0} {1} is disabled”.format(bold(label), bold(warehouse))).
  - If (fieldname equals “default\_in\_transit\_warehouse” and details.warehouse\_type differs from “Transit”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname equals “default\_in\_transit\_warehouse” → details.warehouse\_type differs from “Transit”.
    - Call the validation error handler Platform.throw(translated “{0} must be a Transit Warehouse”.format(bold(label))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is value new or changed](operations-001.md#op-dc37d28d396044).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L741) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L306)

<a id="op-53483bf9fee08a"></a>
### Company.validate abbr

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_abbreviation`

**Inputs** self.

**Record and data access** execute query text (SELECT, Company).

**Explicit failure paths** validation helper — translated “Abbreviation is mandatory” · validation helper — translated “Abbreviation already used for another company”.

**Local steps**

- If not self.abbr.
  - Set self.abbr from empty text.join(generator of c at 0 for c drawn from nested operand in the contract.company\_name.split()).upper().
    - Draw c from self.company\_name.split().
- Set self.abbr from self.abbr.strip().
- If not self.abbr.strip().
  - Call the validation error handler Platform.throw(translated “Abbreviation is mandatory”).
- If Platform.db.sql(query text (SELECT, Company), tuple(self.name, self.abbr)).
  - Call the validation error handler Platform.throw(translated “Abbreviation already used for another company”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L297)

<a id="op-ce51e933dce1fa"></a>
### Company.create default tax template

`operation_enterprise_setup_record_definitions_company_business_behavior_company_create_default_tax_template`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.only\_for(tuple(“System Manager”, “Accounts Manager”)).
- Evaluate setup\_taxes\_and\_charges(self.name, self.country).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(tuple(“System Manager”, “Accounts Manager”)).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L70) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L286)

<a id="op-3be2dcf2c242a9"></a>
### Company.validate default accounts

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_default_accounts`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_value.

**Explicit failure paths** validation helper — translated “{0} currency must be same as company's default currency. Please select another account.”.format(bold(label)) · validation helper — translated “{0} must be a non-group Cost Center of {1}”.format(self.meta.get\_translated\_label(fieldname), self.name).

**Local steps**

- Set account\_filters from mapping(“default\_bank\_account” → mapping(“account\_type” → “Bank”), “default\_cash\_account” → mapping(“account\_type” → “Cash”), “default\_receivable\_account” → mapping(“root\_type” → “Asset”, “account\_type” →  ….
- For each tuple(fieldname, filters) in account\_filters.items().
  - Set account from self.get(fieldname).
  - If not account.
    - Continue with the next iteration or loop test.
  - Set label from self.meta.get\_translated\_label(fieldname).
  - If self.is\_value\_new\_or\_changed(fieldname).
    - Evaluate self.validate\_default\_account(account, label, filters).
  - If (self.is\_value\_new\_or\_changed(fieldname) or self.currency\_changed).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_value\_new\_or\_changed(fieldname) → self.currency\_changed.
    - If get\_account\_currency(account) does not belong to set(self.default\_currency, self.previous\_default\_currency).
      - Call the validation error handler Platform.throw(translated “{0} currency must be same as company's default currency. Please select another account.”.format(bold(label))).
- For each fieldname in tuple(“cost\_center”, “round\_off\_cost\_center”, “depreciation\_cost\_center”).
  - Set cost\_center from self.get(fieldname).
  - If (not cost\_center or not self.is\_value\_new\_or\_changed(fieldname)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cost\_center → not self.is\_value\_new\_or\_changed(fieldname).
    - Continue with the next iteration or loop test.
  - Set tuple(company, is\_group) from Platform.db.get\_value(“Cost Center”, cost\_center, list(“company”, “is\_group”)).
  - If (company differs from self.name or is\_group).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in company differs from self.name → is\_group.
    - Call the validation error handler Platform.throw(translated “{0} must be a non-group Cost Center of {1}”.format(self.meta.get\_translated\_label(fieldname), self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is value new or changed](operations-001.md#op-dc37d28d396044), [validate default account](operations-001.md#op-40374702eab9aa).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L77) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L733) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L300)

<a id="op-dc37d28d396044"></a>
### Company.is value new or changed

`operation_enterprise_binding_enterprise_setup_doctype_company_company_company_is_value_new_or_changed`

**Inputs** self, fieldname.

**Explicit results** (self.is\_new() or self.has\_value\_changed(fieldname)).

**Local steps**

- Return (self.is\_new() or self.has\_value\_changed(fieldname)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.has\_value\_changed(fieldname).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L643) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L140)

<a id="op-40374702eab9aa"></a>
### Company.validate default account

`operation_enterprise_binding_enterprise_setup_doctype_company_company_company_validate_default_account`

**Inputs** self, account, label, filters.

**Record and data access** read “Account” via get\_value.

**Explicit failure paths** validation helper — translated “Account {0} is disabled.”.format(bold(account)) · validation helper — translated “{0}: {1} is a group account.”.format(bold(label), bold(account)) · validation helper — translated “Account {0} does not belong to company: {1}”.format(account, self.name) · validation helper — translated “{0}: {1} has an invalid {2}”.format(label, account, key).

**Local steps**

- Set details from Platform.db.get\_value(“Account”, account, list(“company”, “is\_group”, “disabled”, “root\_type”, …), as\_dict = true).
- If details.disabled.
  - Call the validation error handler Platform.throw(translated “Account {0} is disabled.”.format(bold(account))).
- If details.is\_group.
  - Call the validation error handler Platform.throw(translated “{0}: {1} is a group account.”.format(bold(label), bold(account))).
- If details.company differs from self.name.
  - Call the validation error handler Platform.throw(translated “Account {0} does not belong to company: {1}”.format(account, self.name)).
- For each tuple(key, expected) in filters.items().
  - If details.get(key) does not belong to expected when isinstance(expected, tuple), otherwise tuple(expected).
    - Value choice on isinstance(expected, tuple) — true gives expected, false gives tuple(expected).
    - Call the validation error handler Platform.throw(translated “{0}: {1} has an invalid {2}”.format(label, account, key)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L645) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L142)

<a id="op-5bce385f3e6edd"></a>
### Company.validate currency

`operation_enterprise_setup_record_definitions_company_business_behavior_company_validate_currency`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot change company's default currency, because there are existing transactions. Transactions must be canc …”.

**Local steps**

- Set self.previous\_default\_currency from no value.
- Set self.currency\_changed from false.
- If self.is\_new().
  - Return no value.
- Set self.previous\_default\_currency from Platform.get\_cached\_value(“Company”, self.name, “default\_currency”).
- Set self.currency\_changed from bool((self.default\_currency and self.previous\_default\_currency and self.default\_currency differs from self.previous\_default\_currency)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.default\_currency → self.previous\_default\_currency → self.default\_currency differs from self.previous\_default\_currency.
- If (self.currency\_changed and self.check\_if\_transactions\_exist()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.currency\_changed → self.check\_if\_transactions\_exist().
  - Call the validation error handler Platform.throw(translated “Cannot change company's default currency, because there are existing transactions. Transactions must be canc …”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check if transactions exist](operations-001.md#op-412da9ccea0ebf).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.name, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L76) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L732) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L299)

<a id="op-977eac4b772be5"></a>
### Company.on update

`operation_enterprise_setup_record_definitions_company_business_behavior_company_on_update`

**Inputs** self.

**Record and data access** read “Account” via exists · read “Cost Center” via get\_value · read “Department” via get\_value.

**State and service calls** request set\_value on “Account” · request set\_value on “Currency”.

**Local steps**

- Evaluate NestedSet.on\_update(self).
- If self.currency\_changed.
  - Evaluate Platform.db.set\_value(“Account”, mapping(“company” → self.name, “account\_currency” → self.previous\_default\_currency), “account\_currency”, self.default\_currency, update\_modified = false).
  - Evaluate Platform.local.cache.pop(“account\_currency”, no value).
- If not Platform.db.exists(“Account”, mapping(“company” → self.name, “docstatus” → list(“&lt;”, 2))).
  - If not Platform.local.flags.ignore\_chart\_of\_accounts.
    - Set Platform.flags.country\_change from true.
    - Evaluate sync\_financial\_report\_templates(self.chart\_of\_accounts, self.existing\_company).
    - Evaluate self.create\_default\_accounts().
    - Evaluate self.create\_default\_warehouses().
- If not Platform.db.get\_value(“Cost Center”, mapping(“is\_group” → 0, “company” → self.name)).
  - Evaluate self.create\_default\_cost\_center().
- If Platform.flags.country\_change.
  - Evaluate install\_country\_fixtures(self.name, self.country).
  - Evaluate setup\_taxes\_and\_charges(self.name, self.country).
- If not Platform.db.get\_value(“Department”, mapping(“company” → self.name)).
  - Evaluate self.create\_default\_departments().
- If not Platform.local.flags.ignore\_chart\_of\_accounts.
  - Evaluate self.set\_default\_accounts().
  - If self.default\_cash\_account.
    - Evaluate self.set\_mode\_of\_payment\_account().
- If self.default\_currency.
  - Evaluate Platform.db.set\_value(“Currency”, self.default\_currency, “enabled”, 1).
- If (hasattr(Platform.local, “enable\_perpetual\_inventory”) and self.name belongs to Platform.local.enable\_perpetual\_inventory).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(Platform.local, “enable\_perpetual\_inventory”) → self.name belongs to Platform.local.enable\_perpetual\_inventory.
  - Set Platform.local.enable\_perpetual\_inventory at self.name from self.enable\_perpetual\_inventory.
- If Platform.flags.parent\_company\_changed.
  - Bind dependencies rebuild\_tree.
  - Evaluate rebuild\_tree(“Company”).
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create default accounts](operations-002.md#op-fe401ece3dddb3), [create default warehouses](operations-002.md#op-495dd1930a3784), [create default cost center](operations-002.md#op-b1a2639a2bf84d), [create default departments](operations-002.md#op-99980d5651d30d), [set default accounts](operations-002.md#op-9ae66e9fb3e155), [set mode of payment account](operations-002.md#op-b16287671e177a).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L72) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L721) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L289)
