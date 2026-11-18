# Shared transaction rules · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-156ee0a31c622d"></a>
### Accounts Controller.has cash discount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_has_cash_discount`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** bool((self.get(“is\_cash\_or\_non\_trade\_discount”) and self.get(“discount\_amount”))).

**Local steps**

- Return bool((self.get(“is\_cash\_or\_non\_trade\_discount”) and self.get(“discount\_amount”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_cash\_or\_non\_trade\_discount”) → self.get(“discount\_amount”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L924) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L164)

<a id="op-4911f4322decdf"></a>
### Accounts Controller.drop mapped discount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_drop_mapped_discount`

**Inputs** self, item.

**Local steps**

- Set item.mapped\_additional\_discount\_amount from 0.
- Evaluate self.clear\_stale\_mapped\_discount\_total().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear stale mapped discount total](operations-007.md#op-282acf06ebe91c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L150)

<a id="op-282acf06ebe91c"></a>
### Accounts Controller.clear stale mapped discount total

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_clear_stale_mapped_discount_total`

**Inputs** self.

**Local steps**

- If not self.has\_mapped\_discount.
  - Set self.discount\_amount from 0.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L147)

<a id="op-d590d989871082"></a>
### Accounts Controller.is discount header derived

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_is_discount_header_derived`

**Inputs** self.

**Wrappers, in declaration order** property.

**Explicit results** (self.get(“apply\_discount\_on”) equals “Net Total” and not flt(self.get(“additional\_discount\_percentage”)) and flt(self.get(“discount\_amount”), precision) equals flt(sum(generator of flt(nested operand in t ….

**Local steps**

- Set precision from self.precision(“discount\_amount”).
- Return (self.get(“apply\_discount\_on”) equals “Net Total” and not flt(self.get(“additional\_discount\_percentage”)) and flt(self.get(“discount\_amount”), precision) equals flt(sum(generator of flt(nested operand in t ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“apply\_discount\_on”) equals “Net Total” → not flt(self.get(“additional\_discount\_percentage”)) → flt(self.get(“discount\_amount”), precision) equals flt(sum(generator of flt(item.distributed\_discount\_amount) for item drawn from self.items), precision).
  - Draw item from self.items.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L927) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L167)

<a id="op-7d75233d51608b"></a>
### Accounts Controller.sync mapped discount with header

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_sync_mapped_discount_with_header`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return no value.
- Set header\_changed from any(generator of self.has\_value\_changed(field) for field drawn from ADDITIONAL\_DISCOUNT\_FIELDS).
  - Draw field from ADDITIONAL\_DISCOUNT\_FIELDS.
- If (self.has\_mapped\_discount and header\_changed and not self.is\_discount\_header\_derived).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.has\_mapped\_discount → header\_changed → not self.is\_discount\_header\_derived.
  - For each item in self.items.
    - Set item.mapped\_additional\_discount\_amount from 0.
- Otherwise.
  - If (previous.has\_mapped\_discount and not header\_changed).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous.has\_mapped\_discount → not header\_changed.
    - Evaluate self.clear\_stale\_mapped\_discount\_total().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear stale mapped discount total](operations-007.md#op-282acf06ebe91c).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L952) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L192)

<a id="op-017c913462ed98"></a>
### Accounts Controller.is same transaction side

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_is_same_transaction_side`

**Inputs** self, source\_doc.

**Explicit results** any(generator of (self.doctype belongs to transaction\_types and source\_doc.doctype belongs to transaction\_types) for transaction\_types drawn from tuple(PURCHASE\_TRANSACTION\_TYPES, SALES\_TRANSACTION\_TYPES)).

**Local steps**

- Return any(generator of (self.doctype belongs to transaction\_types and source\_doc.doctype belongs to transaction\_types) for transaction\_types drawn from tuple(PURCHASE\_TRANSACTION\_TYPES, SALES\_TRANSACTION\_TYPES)).
  - Draw transaction\_types from tuple(PURCHASE\_TRANSACTION\_TYPES, SALES\_TRANSACTION\_TYPES).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to transaction\_types → source\_doc.doctype belongs to transaction\_types.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L930) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L170)

<a id="op-e1e215e43c4aff"></a>
### Accounts Controller.before mapping

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_before_mapping`

**Inputs** self, source\_doc, table\_maps.

**Explicit results** no value.

**Local steps**

- If (not self.get(“items”) or not self.is\_same\_transaction\_side(source\_doc)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.get(“items”) → not self.is\_same\_transaction\_side(source\_doc).
  - Return no value.
- If self.has\_cash\_discount.
  - Evaluate self.keep\_cash\_discount(source\_doc).
- Otherwise.
  - If self.has\_different\_discount(source\_doc).
    - Evaluate self.calculate\_taxes\_and\_totals().
    - Evaluate self.move\_additional\_discount\_to\_items().
    - Set self.flags.mapped\_discount\_item\_count from len(self.items).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is same transaction side](operations-007.md#op-017c913462ed98), [keep cash discount](operations-007.md#op-938044386cce16), [has different discount](operations-007.md#op-3239dc8c8df2fd), [calculate taxes and totals](operations-002.md#op-52a893faf0bdd9), [move additional discount to items](operations-007.md#op-279a74350dfd17).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L5) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L905) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L145)

<a id="op-15fb09ca3a7798"></a>
### Accounts Controller.after mapping

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_after_mapping`

**Inputs** self, source\_doc.

**Local steps**

- Set cash\_discount from self.flags.pop(“mapped\_cash\_discount”, no value).
- Set existing\_item\_count from self.flags.pop(“mapped\_discount\_item\_count”, no value).
- If cash\_discount.
  - Evaluate self.update(cash\_discount).
  - Evaluate self.calculate\_taxes\_and\_totals().
- Otherwise.
  - If existing\_item\_count is identical to no value.
    - Evaluate self.set\_discount\_amount\_after\_mapping(source\_doc).
  - Otherwise.
    - Evaluate self.apply\_source\_discount\_to\_mapped\_items(source\_doc, existing\_item\_count).

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate taxes and totals](operations-002.md#op-52a893faf0bdd9), [set discount amount after mapping](operations-007.md#op-284f1e80aad754), [apply source discount to mapped items](operations-007.md#op-8fbd13d160059c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L74) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L590) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L295)

<a id="op-938044386cce16"></a>
### Accounts Controller.keep cash discount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_keep_cash_discount`

**Inputs** self, source\_doc.

**Explicit failure paths** validation helper — translated “The cash or non-trade discount cannot be combined with the discount of {0}.”.format(get\_link\_to\_form(source\_doc.doctype, source\_doc.name)).

**Local steps**

- If (source\_doc.get(“discount\_amount”) or source\_doc.has\_mapped\_discount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in source\_doc.get(“discount\_amount”) → source\_doc.has\_mapped\_discount.
  - Call the validation error handler Platform.throw(translated “The cash or non-trade discount cannot be combined with the discount of {0}.”.format(get\_link\_to\_form(source\_doc.doctype, source\_doc.name)), title = translated “Discounts Cannot B ….
- Set self.flags.mapped\_cash\_discount from mapping of field → self.get(field) for field drawn from ADDITIONAL\_DISCOUNT\_FIELDS.
  - Draw field from ADDITIONAL\_DISCOUNT\_FIELDS.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L932) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L172)

<a id="op-3239dc8c8df2fd"></a>
### Accounts Controller.has different discount

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_has_different_discount`

**Inputs** self, source\_doc.

**Explicit results** false · not (discount\_percentage and discount\_percentage equals flt(source\_doc.get(“additional\_discount\_percentage”)) and self.get(“apply\_discount\_on”) equals source\_doc.get(“apply\_discount\_on”)).

**Local steps**

- If (not flt(self.get(“discount\_amount”)) and not flt(source\_doc.get(“discount\_amount”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not flt(self.get(“discount\_amount”)) → not flt(source\_doc.get(“discount\_amount”)).
  - Return false.
- Set discount\_percentage from flt(self.get(“additional\_discount\_percentage”)).
- Return not (discount\_percentage and discount\_percentage equals flt(source\_doc.get(“additional\_discount\_percentage”)) and self.get(“apply\_discount\_on”) equals source\_doc.get(“apply\_discount\_on”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in discount\_percentage → discount\_percentage equals flt(source\_doc.get(“additional\_discount\_percentage”)) → self.get(“apply\_discount\_on”) equals source\_doc.get(“apply\_discount\_on”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L925) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L165)

<a id="op-8fbd13d160059c"></a>
### Accounts Controller.apply source discount to mapped items

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_apply_source_discount_to_mapped_items`

**Inputs** self, source\_doc, existing\_item\_count.

**Local steps**

- If len(self.items) equals existing\_item\_count.
  - Evaluate self.update(mapping(“additional\_discount\_percentage” → 0, “discount\_amount” → 0)).
- Otherwise.
  - Within self.mapped\_items\_only(existing\_item\_count).
    - Evaluate self.update(mapping of field → source\_doc.get(field) for field drawn from ADDITIONAL\_DISCOUNT\_FIELDS).
      - Draw field from ADDITIONAL\_DISCOUNT\_FIELDS.
    - Evaluate self.set\_discount\_amount\_after\_mapping(source\_doc).
    - Evaluate self.calculate\_taxes\_and\_totals().
    - Evaluate self.move\_additional\_discount\_to\_items().
- Evaluate self.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [mapped items only](operations-007.md#op-9abea527b0baf5), [set discount amount after mapping](operations-007.md#op-284f1e80aad754), [calculate taxes and totals](operations-002.md#op-52a893faf0bdd9), [move additional discount to items](operations-007.md#op-279a74350dfd17).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L904) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L144)

<a id="op-9abea527b0baf5"></a>
### Accounts Controller.mapped items only

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_mapped_items_only`

**Inputs** self, existing\_item\_count.

**Wrappers, in declaration order** contextmanager.

**Local steps**

- Set existing\_items from self.items at slice no value to existing\_item\_count.
- Evaluate self.set(“items”, self.items at slice existing\_item\_count to no value).
- Attempt the following.
  - yield no value.
- On exit, including pending return or failure.
  - Evaluate self.set(“items”, (existing\_items + self.items)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L938) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L178)

<a id="op-279a74350dfd17"></a>
### Accounts Controller.move additional discount to items

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_move_additional_discount_to_items`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (not self.discount\_amount or self.has\_mapped\_discount).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.discount\_amount → self.has\_mapped\_discount.
  - Return no value.
- For each item in self.items.
  - Set stock\_qty from get\_qty\_in\_stock\_uom(item).
  - If stock\_qty.
    - Set item.mapped\_additional\_discount\_amount from flt((flt(item.distributed\_discount\_amount) ÷ stock\_qty), item.precision(“mapped\_additional\_discount\_amount”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L939) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L179)

<a id="op-284f1e80aad754"></a>
### Accounts Controller.set discount amount after mapping

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_discount_amount_after_mapping`

**Inputs** self, source\_doc.

**Explicit results** no value.

**Local steps**

- If not self.is\_same\_transaction\_side(source\_doc).
  - Return no value.
- If (not self.meta.get\_field(“discount\_amount”) or not source\_doc.meta.get\_field(“discount\_amount”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.meta.get\_field(“discount\_amount”) → not source\_doc.meta.get\_field(“discount\_amount”).
  - Return no value.
- If not source\_doc.discount\_amount.
  - Return no value.
- If source\_doc.has\_mapped\_discount.
  - Evaluate self.clear\_stale\_mapped\_discount\_total().
  - Evaluate self.calculate\_taxes\_and\_totals().
  - Return no value.
- If source\_doc.get(“additional\_discount\_percentage”).
  - Return no value.
- Set item\_doctype from self.meta.get\_field(“items”).options.
- Set doctype\_table from Platform.qb.DocType(self.doctype).
- Set item\_table from Platform.qb.DocType(item\_doctype).
- Set is\_same\_doctype from self.doctype equals source\_doc.doctype.
- Set is\_return from (self.get(“is\_return”) and is\_same\_doctype).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → is\_same\_doctype.
- If (is\_same\_doctype and not is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_same\_doctype → not is\_return.
  - Return no value.
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).where(doctype\_table.discount\_amount differs from 0).select(Sum(doctype\_table.discount\_amount)).
- If is\_return.
  - Set query from query.where(doctype\_table.is\_return equals 1).where(doctype\_table.return\_against equals source\_doc.name).
- Otherwise.
  - Set item\_meta from Platform.get\_meta(item\_doctype).
  - Set reference\_fieldname from next(generator of row.fieldname for row drawn from item\_meta.fields where (row.fieldtype equals “Link” and row.options equals source\_doc.doctype and not row.get(“is\_custom\_field”)), no value).
    - Draw row from item\_meta.fields, keep a combination only if ((row.fieldtype equals “Link” and row.options equals source\_doc.doctype and not row.get(“is\_custom\_field”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.fieldtype equals “Link” → row.options equals source\_doc.doctype → not row.get(“is\_custom\_field”).
  - If not reference\_fieldname.
    - Return no value.
  - Set linked\_documents from nested operand in the contract(nested operand in the contract).select(item\_table.parent).where(item\_table at reference\_fieldname equals source\_doc.name).distinct().
  - Set documents\_with\_mapped\_discount from nested operand in the contract(nested operand in the contract).select(item\_table.parent).where(item\_table.parent.isin(linked\_documents)).where(item\_table.mapped\_additional\_discount\_amount differs from 0).
  - Set query from query.where(doctype\_table.name.isin(linked\_documents)).where(doctype\_table.name.notin(documents\_with\_mapped\_discount)).
- Set result from query.run().
- If not result.
  - Return no value.
- Set discount\_already\_applied from flt(result at 0 at 0).
- If not is\_return.
  - Update discount\_already\_applied using + self.get\_mapped\_discount\_applied(source\_doc, reference\_fieldname).
- If not discount\_already\_applied.
  - Return no value.
- If is\_return.
  - Update discount\_already\_applied using × negative 1.
- Set discount\_amount from max((source\_doc.discount\_amount − discount\_already\_applied), 0).
- If (discount\_amount and is\_return).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in discount\_amount → is\_return.
  - Update discount\_amount using × negative 1.
- Set self.discount\_amount from flt(discount\_amount, self.precision(“discount\_amount”)).
- Evaluate self.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Methods declared on this owner** [is same transaction side](operations-007.md#op-017c913462ed98), [clear stale mapped discount total](operations-007.md#op-282acf06ebe91c), [calculate taxes and totals](operations-002.md#op-52a893faf0bdd9), [get mapped discount applied](operations-007.md#op-dd31910a7a6a99).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L648) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L352)

<a id="op-dd31910a7a6a99"></a>
### Accounts Controller.get mapped discount applied

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_mapped_discount_applied`

**Inputs** self, source\_doc, reference\_fieldname.

**Explicit results** applied · ((applied × source\_doc.discount\_amount) ÷ distributed\_discount).

**Local steps**

- Set item\_table from Platform.qb.DocType(self.meta.get\_field(“items”).options).
- Set applied from flt(nested operand in the contract.where(nested operand in the contract differs from nested operand in the contract).run() at 0 at 0).
- Set distributed\_discount from sum(generator of flt(item.distributed\_discount\_amount) for item drawn from source\_doc.items).
  - Draw item from source\_doc.items.
- If not distributed\_discount.
  - Return applied.
- Return ((applied × source\_doc.discount\_amount) ÷ distributed\_discount).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L915) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L155)

<a id="op-729abb4bb40ade"></a>
### Get tax rate

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_tax_rate`

**Inputs** account\_head.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Account”, account\_head, list(“tax\_rate”, “account\_name”), as\_dict = true).

**Local steps**

- Set ptype from “select” when Platform.only\_has\_select\_perm(“Account”), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(“Account”) — true gives “select”, false gives “read”.
- If not Platform.has\_permission(“Account”, ptype, account\_head).
  - Evaluate \_refuse().
- Return Platform.get\_cached\_value(“Account”, account\_head, list(“tax\_rate”, “account\_name”), as\_dict = true).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Account”, ptype, account\_head) · configured or stored value from Platform.get\_cached\_value(“Account”, account\_head, list(“tax\_rate”, “account\_name”), as\_dict = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L995) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L235)

<a id="op-9c34e18252935e"></a>
### Validate tax master

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_tax_master`

**Inputs** master\_doctype, master\_name = no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “Invalid tax master doctype”.

**Local steps**

- If master\_doctype does not belong to TAX\_MASTER\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Invalid tax master doctype”, Platform.PermissionError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1033) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L273)

<a id="op-b57e8d0a885d1e"></a>
### Get default taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_default_taxes_and_charges`

**Inputs** master\_doctype, tax\_template = no value, company = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** default.

**Local steps**

- Set default from \_get\_default\_taxes\_and\_charges(master\_doctype, tax\_template, company).
- If (default and default.get(“taxes\_and\_charges”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in default → default.get(“taxes\_and\_charges”).
  - Evaluate require\_permission(master\_doctype, default at “taxes\_and\_charges”, “select”).
- Return default.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L985) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L225)

<a id="op-ad659ee6840458"></a>
### Get default taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_default_taxes_and_charges_768f91f906af`

**Inputs** master\_doctype, tax\_template = no value, company = no value.

**Record and data access** read master\_doctype via get\_cached\_value · read master\_doctype via get\_value.

**Explicit results** mapping() · no value · mapping(“taxes\_and\_charges” → default\_tax, “taxes” → \_get\_taxes\_and\_charges(master\_doctype, default\_tax)).

**Local steps**

- If not company.
  - Return mapping().
- Evaluate validate\_tax\_master(master\_doctype, tax\_template).
- If (tax\_template and company).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax\_template → company.
  - Set tax\_template\_company from Platform.get\_cached\_value(master\_doctype, tax\_template, “company”).
  - If tax\_template\_company equals company.
    - Return no value.
- Set default\_tax from Platform.db.get\_value(master\_doctype, mapping(“is\_default” → 1, “company” → company)).
- Return mapping(“taxes\_and\_charges” → default\_tax, “taxes” → \_get\_taxes\_and\_charges(master\_doctype, default\_tax)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(master\_doctype, tax\_template, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L86) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L986) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L226)

<a id="op-1e24f9a4d70887"></a>
### Get taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_taxes_and_charges`

**Inputs** master\_doctype, master\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** \_get\_taxes\_and\_charges(master\_doctype, master\_name).

**Local steps**

- If master\_name.
  - Evaluate require\_permission(master\_doctype, master\_name, “select”).
- Return \_get\_taxes\_and\_charges(master\_doctype, master\_name).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L996) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L236)

<a id="op-95b39eb325ea11"></a>
### Get taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_get_taxes_and_charges_c7487090dfa0`

**Inputs** master\_doctype, master\_name.

**Record and data access** resolve a document from master\_doctype via get\_doc.

**Explicit results** no value · taxes\_and\_charges.

**Local steps**

- If not master\_name.
  - Return no value.
- Evaluate validate\_tax\_master(master\_doctype, master\_name).
- Bind dependencies child\_table\_fields, default\_fields.
- Set tax\_master from Platform.get\_doc(master\_doctype, master\_name).
- Set taxes\_and\_charges from list().
- For each tuple(\_i, tax) in enumerate(tax\_master.get(“taxes”)).
  - Set tax from tax.as\_dict().
  - For each fieldname in (default\_fields + child\_table\_fields).
    - If fieldname belongs to tax.
      - Remove tax at fieldname.
  - Evaluate taxes\_and\_charges.append(tax).
- Return taxes\_and\_charges.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L997) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L237)

<a id="op-fc4dab1a9ed5cf"></a>
### Validate conversion rate

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_conversion_rate`

**Inputs** currency, conversion\_rate, conversion\_rate\_label, company.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- Set company\_currency from Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- If not conversion\_rate.
  - Evaluate throw(translated “{0} is mandatory. Maybe Currency Exchange record is not created for {1} to {2}.”.format(conversion\_rate\_label, currency, company\_currency)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1025) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L265)

<a id="op-b59c15d2afe65b"></a>
### Validate taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_taxes_and_charges`

**Inputs** tax.

**Explicit failure paths** validation helper — translated “Can refer row only if the charge type is 'On Previous Row Amount' or 'Previous Row Total'” · validation helper — translated “Cannot select charge type as 'On Previous Row Amount' or 'On Previous Row Total' for first row” · validation helper — translated “Please specify a valid Row ID for row {0} in table {1}”.format(tax.idx, translated tax.doctype) · validation helper — translated “Cannot refer row number greater than or equal to current row number for this Charge type”.

**Local steps**

- If (tax.charge\_type belongs to list(“Actual”, “On Net Total”, “On Paid Amount”) and tax.row\_id).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.charge\_type belongs to list(“Actual”, “On Net Total”, “On Paid Amount”) → tax.row\_id.
  - Call the validation error handler Platform.throw(translated “Can refer row only if the charge type is 'On Previous Row Amount' or 'Previous Row Total'”).
- Otherwise.
  - If tax.charge\_type belongs to list(“On Previous Row Amount”, “On Previous Row Total”).
    - If cint(tax.idx) equals 1.
      - Call the validation error handler Platform.throw(translated “Cannot select charge type as 'On Previous Row Amount' or 'On Previous Row Total' for first row”).
    - Otherwise.
      - If not tax.row\_id.
        - Call the validation error handler Platform.throw(translated “Please specify a valid Row ID for row {0} in table {1}”.format(tax.idx, translated tax.doctype)).
      - Otherwise.
        - If (tax.row\_id and cint(tax.row\_id) ≥ cint(tax.idx)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in tax.row\_id → cint(tax.row\_id) ≥ cint(tax.idx).
          - Call the validation error handler Platform.throw(translated “Cannot refer row number greater than or equal to current row number for this Charge type”).
- If tax.charge\_type equals “Actual”.
  - Set tax.rate from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L134) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1034) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L274)

<a id="op-454b1a3278c9dd"></a>
### Validate account head

`operation_enterprise_binding_enterprise_controllers_accounts_controller_validate_account_head`

**Inputs** idx, account, company, context = no value.

**Declared result** no value.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row {0}: The {3} Account {1} does not belong to the company {2}”.format(idx, Platform.bold(account), Platform.bold(company), (context or empty text)) · validation helper — translated “You selected the account group {1} as {2} Account in row {0}. Please select a single account.”.format(idx, Platform.bold(account), (context or empty text)).

**Local steps**

- If company differs from Platform.get\_cached\_value(“Account”, account, “company”).
  - Call the validation error handler Platform.throw(translated “Row {0}: The {3} Account {1} does not belong to the company {2}”.format(idx, Platform.bold(account), Platform.bold(company), (context or empty text)), title = translated “Invalid Account”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → empty text.
- If Platform.get\_cached\_value(“Account”, account, “is\_group”).
  - Call the validation error handler Platform.throw(translated “You selected the account group {1} as {2} Account in row {0}. Please select a single account.”.format(idx, Platform.bold(account), (context or empty text)), title = translated “I ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in context → empty text.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, account, “company”), Platform.get\_cached\_value(“Account”, account, “is\_group”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L121) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1021) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L261)
