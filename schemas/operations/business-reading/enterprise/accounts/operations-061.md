# Accounting and settlement · operations 61

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Order billing as on

<a id="op-03a28e9405d81d"></a>
### Order Billing As On.sum till date

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_sum_till_date`

**Inputs** self, field.

**Declared result** Sum.

**Explicit results** Sum(Case().when(nested operand in the contract.invoice.posting\_date ≤ self.as\_on\_date, field).else\_(0)).

**Local steps**

- Return Sum(Case().when(nested operand in the contract.invoice.posting\_date ≤ self.as\_on\_date, field).else\_(0)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L178) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1243)

<a id="op-3187aa3034a342"></a>
### Order Billing As On.get rows

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingason_get_rows`

**Inputs** self, order\_lines.

**Declared result** list at Platform.\_dict.

**Explicit results** query.run(as\_dict = true).

**Local steps**

- Set parent from Platform.qb.DocType(self.doctype).
- Set child from Platform.qb.DocType((self.doctype + “ Item”)).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract, …).where((nested operand in the contract equal ….
- If self.links.invoiced\_row\_link.
  - Set query from query.select(child at self.links.invoiced\_row\_link.as\_(“invoiced\_row”)).
- Return query.run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L175) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1240)

<a id="op-fd9758f5f7f8d1"></a>
### Order Billing Pool.initialize

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingpool_init`

**Inputs** self, amount, qty.

**Local steps**

- Set self.amount from flt(amount).
- Set self.qty from flt(qty).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1244)

<a id="op-6339915475fefd"></a>
### Order Billing Pool.take for delivery

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingpool_take_for_delivery`

**Inputs** self, row, billed.

**Declared result** float.

**Explicit results** flt(row.amount) · 0 · share.

**Local steps**

- If row.invoiced\_row.
  - Update self.amount using − flt(row.amount).
  - Return flt(row.amount).
- If (not self.amount or billed ≥ flt(row.amount)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.amount → billed ≥ flt(row.amount).
  - Return 0.
- Set share from min((flt(row.amount) − billed), self.amount).
- Update self.amount using − share.
- Return share.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1245)

<a id="op-781d300078ed43"></a>
### Order Billing Pool.take for receipt

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_orderbillingpool_take_for_receipt`

**Inputs** self, row, billed.

**Declared result** float.

**Explicit results** 0 · share.

**Local steps**

- If (not self.amount or billed ≥ flt(row.amount)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.amount → billed ≥ flt(row.amount).
  - Return 0.
- If (not billed and self.qty &gt; flt(row.qty)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not billed → self.qty &gt; flt(row.qty).
  - Set share from ((self.amount × flt(row.qty)) ÷ self.qty).
  - Update self.qty using − flt(row.qty).
- Otherwise.
  - Set share from min((flt(row.amount) − billed), self.amount).
  - Update self.qty using × (1 − (share ÷ self.amount)).
- Update self.amount using − share.
- Return share.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L181) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1246)

<a id="op-0b1b0fc97c20ba"></a>
### Group by order line

`operation_enterprise_binding_enterprise_accounts_report_order_billing_as_on_group_by_order_line`

**Inputs** rows.

**Declared result** dict at tuple(str, list at Platform.\_dict).

**Explicit results** grouped.

**Local steps**

- Set grouped from defaultdict(list).
- For each row in rows.
  - Evaluate grouped at row.order\_detail.append(row).
- Return grouped.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L168) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1233)

## Service · Party

<a id="op-9a5832b1db8fa9"></a>
### Get party details

`operation_enterprise_accounts_party_business_behavior_get_party_details`

**Inputs** party = no value, account = no value, party\_type = “Customer”, company = no value, posting\_date = no value, bill\_date = no value, price\_list = no value, currency = no value, doctype = no value, ignore\_permissions = false, fetch\_payment\_terms\_template = true, party\_address = no value, company\_address = no value, shipping\_address = no value, dispatch\_address = no value, pos\_profile = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** Platform.\_dict() · \_get\_party\_details(party, account, party\_type, company, …).

**Local steps**

- If not party.
  - Return Platform.\_dict().
- Return \_get\_party\_details(party, account, party\_type, company, …).

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L70) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L63)

<a id="op-bd7cbf55c7fdc6"></a>
### Get party details

`operation_enterprise_accounts_party_business_behavior_get_party_details_2`

**Inputs** party = no value, account = no value, party\_type = “Customer”, company = no value, posting\_date = no value, bill\_date = no value, price\_list = no value, currency = no value, doctype = no value, ignore\_permissions = false, fetch\_payment\_terms\_template = true, party\_address = no value, company\_address = no value, shipping\_address = no value, dispatch\_address = no value, pos\_profile = no value.

**Record and data access** resolve a document from party\_type via get\_doc · read “POS Profile” via get\_value.

**Explicit results** party\_details.

**Local steps**

- Set party\_details from Platform.\_dict(set\_account\_and\_due\_date(party, account, party\_type, company, …)).
- Set party from party\_details at party\_type.lower().
- Set party from Platform.get\_doc(party\_type, party).
- If not ignore\_permissions.
  - Set ptype from “select” when Platform.only\_has\_select\_perm(party\_type), otherwise “read”.
    - Value choice on Platform.only\_has\_select\_perm(party\_type) — true gives “select”, false gives “read”.
  - Evaluate Platform.has\_permission(party\_type, ptype, party, throw = true).
  - Evaluate validate\_party\_company(party\_type, party.name, company).
- Set currency from (party.get(“default\_currency”) or currency or get\_company\_currency(company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in party.get(“default\_currency”) → currency → get\_company\_currency(company).
- Set tuple(party\_address, shipping\_address) from set\_address\_details(party\_details, party, party\_type, doctype, ignore\_permissions = ignore\_permissions, …).
- Evaluate set\_contact\_details(party\_details, party, party\_type).
- Evaluate set\_other\_values(party\_details, party, party\_type).
- Evaluate set\_price\_list(party\_details, party, party\_type, price\_list, …).
- Set tax\_template from set\_taxes(party.name, party\_type, posting\_date, company, customer\_group = party\_details.customer\_group, supplier\_group = party\_details.supplier\_group, tax\_category = party\_details.tax\_category, billing\_add ….
- If tax\_template.
  - Set party\_details at “taxes\_and\_charges” from tax\_template.
- If cint(fetch\_payment\_terms\_template).
  - Set party\_details at “payment\_terms\_template” from get\_payment\_terms\_template(party.name, party\_type, company).
- If not party\_details.get(“currency”).
  - Set party\_details at “currency” from currency.
- If party\_type equals “Customer”.
  - Set party\_details at “sales\_team” from list of mapping(“sales\_person” → d.sales\_person, “allocated\_percentage” → (d.allocated\_percentage or no value), “commission\_rate” → d.commission\_rate) for d drawn from party.get(“sales\_team”).
    - Draw d from party.get(“sales\_team”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.allocated\_percentage → no value.
- If (not party\_details.get(“tax\_category”) and pos\_profile).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not party\_details.get(“tax\_category”) → pos\_profile.
  - Set party\_details at “tax\_category” from Platform.get\_value(“POS Profile”, pos\_profile, “tax\_category”).
- Return party\_details.

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, ptype, party, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L71) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L64)

<a id="op-5d7d36889c7dce"></a>
### Validate party company

`operation_enterprise_accounts_party_business_behavior_validate_party_company`

**Inputs** party\_type, party, company.

**Explicit results** no value.

**Local steps**

- If (not company or party\_type does not belong to tuple(“Customer”, “Supplier”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not company → party\_type does not belong to tuple(“Customer”, “Supplier”).
  - Return no value.
- Bind dependencies validate\_masters\_for\_company.
- Evaluate validate\_masters\_for\_company(party\_type, list(party), company).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0211.json#L6794) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L84)

<a id="op-c4e65f1246ad4c"></a>
### Set address details

`operation_enterprise_accounts_party_business_behavior_set_address_details`

**Inputs** party\_details, party, party\_type, doctype = no value, company = no value, party\_address = no value, company\_address = no value, shipping\_address = no value, dispatch\_address = no value, ignore\_permissions (named only, default false).

**Explicit results** tuple(party\_billing, party\_shipping).

**Local steps**

- Set party\_billing\_field from “customer\_address” when party\_type belongs to list(“Lead”, “Prospect”), otherwise (party\_type.lower() + “\_address”).
  - Value choice on party\_type belongs to list(“Lead”, “Prospect”) — true gives “customer\_address”, false gives (party\_type.lower() + “\_address”).
- Set party\_details at party\_billing\_field from (party\_address or get\_default\_address(party\_type, party.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_address → get\_default\_address(party\_type, party.name).
- If doctype.
  - Evaluate party\_details.update(get\_fetch\_values(doctype, party\_billing\_field, party\_details at party\_billing\_field)).
- Set party\_details.address\_display from render\_address(party\_details at party\_billing\_field, check\_permissions = not ignore\_permissions).
- If party\_type belongs to list(“Customer”, “Lead”).
  - Set party\_shipping\_field from “shipping\_address\_name”.
  - Set party\_shipping\_display from “shipping\_address”.
  - Set default\_shipping from shipping\_address.
- Otherwise.
  - Set party\_shipping\_field from “dispatch\_address”.
  - Set party\_shipping\_display from “dispatch\_address\_display”.
  - Set default\_shipping from dispatch\_address.
- Set party\_details at party\_shipping\_field from (default\_shipping or get\_party\_shipping\_address(party\_type, party.name)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in default\_shipping → get\_party\_shipping\_address(party\_type, party.name).
- Set party\_details at party\_shipping\_display from render\_address(party\_details at party\_shipping\_field, check\_permissions = not ignore\_permissions).
- If doctype.
  - Evaluate party\_details.update(get\_fetch\_values(doctype, party\_shipping\_field, party\_details at party\_shipping\_field)).
- If company\_address.
  - Set party\_details.company\_address from company\_address.
- Otherwise.
  - Evaluate party\_details.update(get\_company\_address(company)).
- If (doctype belongs to SALES\_TRANSACTION\_TYPES and party\_details.company\_address).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype belongs to SALES\_TRANSACTION\_TYPES → party\_details.company\_address.
  - Evaluate party\_details.update(get\_fetch\_values(doctype, “company\_address”, party\_details.company\_address)).
- If doctype belongs to PURCHASE\_TRANSACTION\_TYPES.
  - If shipping\_address.
    - Evaluate party\_details.update(shipping\_address = shipping\_address, shipping\_address\_display = render\_address(shipping\_address, check\_permissions = not ignore\_permissions), expanded names get\_fetch\_values(doctype, “ ….
  - If party\_details.company\_address.
    - Evaluate party\_details.update(billing\_address = party\_details.company\_address, billing\_address\_display = (party\_details.company\_address\_display or render\_address(party\_details.company\_address, check\_permissions = f ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in party\_details.company\_address\_display → render\_address(party\_details.company\_address, check\_permissions = false).
    - If not party\_details.shipping\_address.
      - Evaluate party\_details.update(shipping\_address = party\_details.billing\_address, shipping\_address\_display = party\_details.billing\_address\_display, expanded names get\_fetch\_values(doctype, “shipping\_address”, party\_d ….
- Set tuple(party\_billing, party\_shipping) from tuple(party\_details.get(party\_billing\_field), party\_details.get(party\_shipping\_field)).
- Set party\_details at “tax\_category” from get\_address\_tax\_category(party.get(“tax\_category”), party\_billing, party\_shipping).
- If doctype belongs to TRANSACTION\_TYPES.
  - Within temporary\_flag(“company”, company).
    - Evaluate get\_regional\_address\_details(party\_details, doctype, company).
- Return tuple(party\_billing, party\_shipping).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L82) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L75)

<a id="op-d2a7de60210016"></a>
### Get regional address details

`operation_enterprise_accounts_party_business_behavior_get_regional_address_details`

**Inputs** party\_details, doctype, company.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L1433) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L79) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L72)

<a id="op-466ba9b4fb310c"></a>
### Complete contact details

`operation_enterprise_accounts_party_business_behavior_complete_contact_details`

**Inputs** party\_details.

**Record and data access** read “Contact” via get\_value.

**Local steps**

- Set contact\_details from Platform.\_dict().
- If party\_details.party\_type equals “Employee”.
  - Bind dependencies get\_employee\_contact.
  - Set contact\_details from get\_employee\_contact(party\_details.party).
  - Evaluate contact\_details.update(mapping(“contact\_person” → no value, “contact\_phone” → no value)).
- Otherwise.
  - If party\_details.contact\_person.
    - Set contact\_details from Platform.db.get\_value(“Contact”, party\_details.contact\_person, list(“name as contact\_person”, “full\_name as contact\_display”, “email\_id as contact\_email”, “mobile\_no as contact\_mobile”, …), as\_dict = true).
  - Otherwise.
    - Set contact\_details from mapping(“contact\_person” → no value, “contact\_display” → no value, “contact\_email” → no value, “contact\_mobile” → no value, …).
- Evaluate party\_details.update(contact\_details).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L1489) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L58) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L52)

<a id="op-b9bbd41a0e2442"></a>
### Set contact details

`operation_enterprise_accounts_party_business_behavior_set_contact_details`

**Inputs** party\_details, party, party\_type.

**Local steps**

- Set party\_details.contact\_person from get\_default\_contact(party\_type, party.name).
- Evaluate complete\_contact\_details(party\_details).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L83) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L76)

<a id="op-4c477dee407e19"></a>
### Set other values

`operation_enterprise_accounts_party_business_behavior_set_other_values`

**Inputs** party\_details, party, party\_type.

**Local steps**

- Set to\_copy from list(“tax\_withholding\_category”, “tax\_withholding\_group”, “language”).
- If party\_type equals “Customer”.
  - Evaluate to\_copy.extend(list(“customer\_name”, “customer\_group”, “territory”)).
- Otherwise.
  - Evaluate to\_copy.extend(list(“supplier\_name”, “supplier\_group”)).
- For each f in to\_copy.
  - Set party\_details at f from party.get(f).
- For each f in (list(“currency”) + list(“sales\_partner”, “commission\_rate”) when party\_type equals “Customer”, otherwise list()).
  - Value choice on party\_type equals “Customer” — true gives list(“sales\_partner”, “commission\_rate”), false gives list().
  - If party.get((“default\_” + f)).
    - Set party\_details at f from party.get((“default\_” + f)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L2164) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L84) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L77)

<a id="op-275dc92b76f119"></a>
### Get default price list

`operation_enterprise_accounts_party_business_behavior_get_default_price_list`

**Inputs** party.

**Record and data access** read “Customer Group” via get\_cached\_value.

**Explicit results** price\_list · no value.

**Local steps**

- Set price\_list from party.get(“default\_price\_list”).
- If is\_price\_list\_enabled(price\_list).
  - Return price\_list.
- If party.doctype differs from “Customer”.
  - Return no value.
- Set price\_list from Platform.get\_cached\_value(“Customer Group”, party.customer\_group, “default\_price\_list”).
- If is\_price\_list\_enabled(price\_list).
  - Return price\_list.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Customer Group”, party.customer\_group, “default\_price\_list”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L2577) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L56)

<a id="op-7a540985830365"></a>
### Get permitted price lists

`operation_enterprise_binding_enterprise_accounts_party_get_permitted_price_lists`

**Inputs** doctype = no value.

**Explicit results** get\_allowed\_docs\_for\_doctype(permissions, doctype).

**Local steps**

- Set permissions from sorted(get\_user\_permissions().get(“Price List”, list()), key = deferred anonymous expression, reverse = true).
- Return get\_allowed\_docs\_for\_doctype(permissions, doctype).

**Values supplied outside this operation** effective access from get\_user\_permissions().

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1105)

<a id="op-ba6ac9fa56fa77"></a>
### Get usable price list

`operation_enterprise_binding_enterprise_accounts_party_get_usable_price_list`

**Inputs** price\_lists, party\_doctype.

**Record and data access** read “Price List” via get\_cached\_value.

**Explicit results** price\_list.

**Local steps**

- Set transaction\_side from “selling” when party\_doctype equals “Customer”, otherwise “buying”.
  - Value choice on party\_doctype equals “Customer” — true gives “selling”, false gives “buying”.
- For each price\_list in price\_lists.
  - Set details from Platform.get\_cached\_value(“Price List”, price\_list, list(“enabled”, transaction\_side), as\_dict = true).
  - If (details.enabled and details at transaction\_side).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in details.enabled → details at transaction\_side.
    - Return price\_list.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Price List”, price\_list, list(“enabled”, transaction\_side), as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1106)

<a id="op-b3101b9c0e776e"></a>
### Set price list

`operation_enterprise_accounts_party_business_behavior_set_price_list`

**Inputs** party\_details, party, party\_type, given\_price\_list, pos = no value, doctype = no value.

**Record and data access** read “Customer” via get\_value · read “POS Profile” via get\_value · read “Price List” via get\_value.

**Local steps**

- Set permitted\_price\_lists from get\_permitted\_price\_lists(doctype).
- If len(permitted\_price\_lists) equals 1.
  - Set price\_list from get\_usable\_price\_list(permitted\_price\_lists, party.doctype).
- Otherwise.
  - If (pos and party\_type equals “Customer”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pos → party\_type equals “Customer”.
    - Set customer\_price\_list from Platform.get\_value(“Customer”, party.name, “default\_price\_list”).
    - If is\_price\_list\_enabled(customer\_price\_list).
      - Set price\_list from customer\_price\_list.
    - Otherwise.
      - Set pos\_price\_list from Platform.get\_value(“POS Profile”, pos, “selling\_price\_list”).
      - Set price\_list from (pos\_price\_list or given\_price\_list).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in pos\_price\_list → given\_price\_list.
  - Otherwise.
    - Set price\_list from (get\_default\_price\_list(party) or given\_price\_list).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_default\_price\_list(party) → given\_price\_list.
    - If (price\_list and permitted\_price\_lists and price\_list does not belong to permitted\_price\_lists).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list → permitted\_price\_lists → price\_list does not belong to permitted\_price\_lists.
      - Set price\_list from get\_usable\_price\_list(permitted\_price\_lists, party.doctype).
- If (price\_list and not is\_price\_list\_enabled(price\_list)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in price\_list → not is\_price\_list\_enabled(price\_list).
  - Set price\_list from no value.
- If price\_list.
  - Set party\_details.price\_list\_currency from Platform.db.get\_value(“Price List”, price\_list, “currency”, cache = true).
- Set party\_details at “selling\_price\_list” when party.doctype equals “Customer”, otherwise “buying\_price\_list” from price\_list.
  - Value choice on party.doctype equals “Customer” — true gives “selling\_price\_list”, false gives “buying\_price\_list”.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L85) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L78)

<a id="op-bbc8672d4b59fe"></a>
### Set account and due date

`operation_enterprise_accounts_party_business_behavior_set_account_and_due_date`

**Inputs** party, account, party\_type, company, posting\_date, bill\_date, doctype.

**Explicit results** mapping(party\_type.lower() → party) · out.

**Local steps**

- If doctype does not belong to list(“POS Invoice”, “Sales Invoice”, “Purchase Invoice”).
  - Return mapping(party\_type.lower() → party).
- If party.
  - Set account from get\_party\_account(party\_type, party, company).
- Set account\_fieldname from “debit\_to” when party\_type equals “Customer”, otherwise “credit\_to”.
  - Value choice on party\_type equals “Customer” — true gives “debit\_to”, false gives “credit\_to”.
- Set out from mapping(party\_type.lower() → party, account\_fieldname → account, “due\_date” → get\_due\_date(posting\_date, party\_type, party, company, …)).
- Return out.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L3377) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L81) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L74)

<a id="op-81ba72da484e6a"></a>
### Get party account

`operation_enterprise_accounts_party_business_behavior_get_party_account`

**Inputs** party\_type, party = no value, company = no value, include\_advance = false.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** list(account, advance\_account) · list(account) · account.

**Local steps**

- Set account from find\_party\_account(party\_type, party, company).
- If account.
  - Evaluate check\_account\_permission(account).
- If (include\_advance and party and party\_type belongs to list(“Customer”, “Supplier”, “Student”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in include\_advance → party → party\_type belongs to list(“Customer”, “Supplier”, “Student”).
  - Set advance\_account from get\_party\_advance\_account(party\_type, party, company).
  - If advance\_account.
    - Evaluate check\_account\_permission(advance\_account).
    - Return list(account, advance\_account).
  - Return list(account).
- Return account.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L65) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L59)

<a id="op-2662477d4b082a"></a>
### Find party account

`operation_enterprise_binding_enterprise_accounts_party_find_party_account`

**Inputs** party\_type, party, company.

**Record and data access** read “Company” via get\_cached\_value · read “Party Account” via get\_value · read party\_type via get\_cached\_value · read “Account” via get\_cached\_value · read “Party Type” via get\_cached\_value.

**Explicit results** account.

**Explicit failure paths** validation helper — translated “Party Type is mandatory” · validation helper — translated “Please select a Company”.

**Local steps**

- If not party\_type.
  - Call the validation error handler Platform.throw(translated “Party Type is mandatory”).
- If not company.
  - Call the validation error handler Platform.throw(translated “Please select a Company”).
- If (not party and party\_type belongs to list(“Customer”, “Supplier”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not party → party\_type belongs to list(“Customer”, “Supplier”).
  - Set default\_account\_name from “default\_receivable\_account” when party\_type equals “Customer”, otherwise “default\_payable\_account”.
    - Value choice on party\_type equals “Customer” — true gives “default\_receivable\_account”, false gives “default\_payable\_account”.
  - Set account from Platform.get\_cached\_value(“Company”, company, default\_account\_name).
- Otherwise.
  - Set account from Platform.db.get\_value(“Party Account”, mapping(“parenttype” → party\_type, “parent” → party, “company” → company), “account”).
  - If (not account and party\_type belongs to list(“Customer”, “Supplier”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → party\_type belongs to list(“Customer”, “Supplier”).
    - Set party\_group\_doctype from “Customer Group” when party\_type equals “Customer”, otherwise “Supplier Group”.
      - Value choice on party\_type equals “Customer” — true gives “Customer Group”, false gives “Supplier Group”.
    - Set group from Platform.get\_cached\_value(party\_type, party, scrub(party\_group\_doctype)).
    - Set account from Platform.db.get\_value(“Party Account”, mapping(“parenttype” → party\_group\_doctype, “parent” → group, “company” → company), “account”).
  - If (not account and party\_type belongs to list(“Customer”, “Supplier”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not account → party\_type belongs to list(“Customer”, “Supplier”).
    - Set default\_account\_name from “default\_receivable\_account” when party\_type equals “Customer”, otherwise “default\_payable\_account”.
      - Value choice on party\_type equals “Customer” — true gives “default\_receivable\_account”, false gives “default\_payable\_account”.
    - Set account from Platform.get\_cached\_value(“Company”, company, default\_account\_name).
  - Set existing\_gle\_currency from get\_party\_gle\_currency(party\_type, party, company).
  - If existing\_gle\_currency.
    - If account.
      - Set account\_currency from Platform.get\_cached\_value(“Account”, account, “account\_currency”).
    - If ((account and account\_currency differs from existing\_gle\_currency) or not account).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in (account and account\_currency differs from existing\_gle\_currency) → not account.
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in account → account\_currency differs from existing\_gle\_currency.
      - Set account from get\_party\_gle\_account(party\_type, party, company).
  - If not account.
    - Set account\_type from Platform.get\_cached\_value(“Party Type”, party\_type, “account\_type”).
    - Set default\_account\_name from ((“default\_” + account\_type.lower()) + “\_account”).
    - Set account from Platform.get\_cached\_value(“Company”, company, default\_account\_name).
- Return account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, default\_account\_name), Platform.get\_cached\_value(party\_type, party, scrub(party\_group\_doctype)) and 2 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L466) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1104)

<a id="op-2cd728a2a9be21"></a>
### Check account permission

`operation_enterprise_binding_enterprise_accounts_party_check_account_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** account.

**Explicit result forms** no value.

**Observed service boundaries** effective access lookup, validation or user-notification service.

**Local structure** 2 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L465) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1103)

<a id="op-519a5170dee219"></a>
### Get party advance account

`operation_enterprise_accounts_party_business_behavior_get_party_advance_account`

**Inputs** party\_type, party, company.

**Record and data access** read “Party Account” via get\_value · read party\_type via get\_cached\_value · read “Company” via get\_cached\_value.

**Explicit results** account.

**Local steps**

- Set account from Platform.db.get\_value(“Party Account”, mapping(“parenttype” → party\_type, “parent” → party, “company” → company), “advance\_account”).
- If not account.
  - Set party\_group\_doctype from “Customer Group” when party\_type equals “Customer”, otherwise “Supplier Group”.
    - Value choice on party\_type equals “Customer” — true gives “Customer Group”, false gives “Supplier Group”.
  - Set group from Platform.get\_cached\_value(party\_type, party, scrub(party\_group\_doctype)).
  - Set account from Platform.db.get\_value(“Party Account”, mapping(“parenttype” → party\_group\_doctype, “parent” → group, “company” → company), “advance\_account”).
- If not account.
  - Set account\_name from “default\_advance\_received\_account” when party\_type equals “Customer”, otherwise “default\_advance\_paid\_account”.
    - Value choice on party\_type equals “Customer” — true gives “default\_advance\_received\_account”, false gives “default\_advance\_paid\_account”.
  - Set account from Platform.get\_cached\_value(“Company”, company, account\_name).
- Return account.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(party\_type, party, scrub(party\_group\_doctype)), Platform.get\_cached\_value(“Company”, company, account\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0212.json#L5473) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L69) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L62)

<a id="op-a223d9a72d8465"></a>
### Get party account currency

`operation_enterprise_accounts_party_business_behavior_get_party_account_currency`

**Inputs** party\_type, party, company.

**Explicit results** Platform.local\_cache(“party\_account\_currency”, tuple(party\_type, party, company), generator).

**Local steps**

- Bind local operation generator for subsequent calls.
- Return Platform.local\_cache(“party\_account\_currency”, tuple(party\_type, party, company), generator).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0001.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-001.tsv#L60)
