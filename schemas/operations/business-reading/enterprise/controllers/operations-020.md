# Shared transaction rules · operations 20

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Selling controller

<a id="op-d35abb06c181d8"></a>
### Selling Controller.validate

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_terms\_and\_conditions(self.get(“tc\_name”), “selling”).
- Evaluate super().validate().
- Evaluate self.ensure\_customer\_is\_not\_blocked().
- Evaluate self.validate\_items().
- If not (self.get(“is\_debit\_note”) or self.get(“is\_return”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_debit\_note”) → self.get(“is\_return”).
  - Evaluate self.validate\_max\_discount().
- Evaluate self.validate\_selling\_price().
- Evaluate self.set\_qty\_as\_per\_stock\_uom().
- Evaluate self.set\_po\_nos(for\_validate = true).
- Evaluate self.set\_gross\_profit().
- Evaluate set\_default\_income\_account\_for\_item(self).
- Evaluate self.set\_customer\_address().
- Evaluate self.validate\_price\_list\_country().
- Evaluate self.validate\_for\_duplicate\_items().
- Evaluate self.validate\_target\_warehouse().
- If self.doctype equals “Sales Invoice”.
  - Evaluate self.validate\_against\_stock\_reservation\_entries().
- Evaluate self.validate\_auto\_repeat\_subscription\_dates().
- Evaluate self.validate\_sample\_retention\_warehouse().
- For each table\_field in list(“items”, “packed\_items”).
  - If self.get(table\_field).
    - Evaluate self.set\_serial\_and\_batch\_bundle(table\_field).

If control reaches the end, it returns no value.

**Methods declared on this owner** [ensure customer is not blocked](operations-021.md#op-6e2d05a614df44), [validate items](operations-021.md#op-25c89517d04706), [validate max discount](operations-020.md#op-ba23c01ec0485c), [validate selling price](operations-020.md#op-e82d982027d7a2), [set qty as per stock uom](operations-020.md#op-84835d138ce2a9), [set po nos](operations-021.md#op-6a3eac4009bf7e), [set gross profit](operations-021.md#op-8959895d51ba01), [set customer address](operations-021.md#op-75382fc12e443d), [validate price list country](operations-020.md#op-5e19325880c5fc), [validate for duplicate items](operations-021.md#op-f67870d74644dd), [validate target warehouse](operations-021.md#op-24f79a8603b2cb), [validate against stock reservation entries](operations-020.md#op-b3d0bd6e9193ff), [validate sample retention warehouse](operations-021.md#op-876c1bf60e8eee).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L7) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L584)

<a id="op-bb52b9bc7572c3"></a>
### Selling Controller.before update after submit

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_before_update_after_submit`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.meta.get\_field(“sales\_team”) and self.is\_child\_table\_same(“sales\_team”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(“sales\_team”) → self.is\_child\_table\_same(“sales\_team”).
  - Return no value.
- Evaluate self.calculate\_commission().
- Evaluate self.calculate\_contribution().

If control reaches the end, it returns no value.

**Methods declared on this owner** [calculate commission](operations-020.md#op-fa51625b5ab798), [calculate contribution](operations-020.md#op-ff1ed2bbec0113).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1103) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L343)

<a id="op-b3d0bd6e9193ff"></a>
### Selling Controller.validate against stock reservation entries

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_validate_against_stock_reservation_entries`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Row #{0}: Stock is reserved for item {1} in warehouse {2}.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(warehouses at 0) when len(warehouses) equals 1, otherwise translated “{ ….

**Local steps**

- If (self.get(“is\_return”) or (self.doctype equals “Sales Invoice” and not cint(self.get(“update\_stock”)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_return”) → (self.doctype equals “Sales Invoice” and not cint(self.get(“update\_stock”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → not cint(self.get(“update\_stock”)).
  - Return no value.
- Set so\_field from “against\_sales\_order” when self.doctype equals “Delivery Note”, otherwise “sales\_order”.
  - Value choice on self.doctype equals “Delivery Note” — true gives “against\_sales\_order”, false gives “sales\_order”.
- Set rows from list of item for item drawn from self.get(“items”) where (item.get(so\_field) and item.so\_detail).
  - Draw item from self.get(“items”), keep a combination only if ((item.get(so\_field) and item.so\_detail)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(so\_field) → item.so\_detail.
- Set reserved\_warehouses from get\_reserved\_warehouses\_by\_order\_row(list of item.so\_detail for item drawn from rows).
  - Draw item from rows.
- For each item in rows.
  - Set warehouses from reserved\_warehouses.get(item.so\_detail).
  - If not warehouses.
    - Continue with the next iteration or loop test.
  - If not item.warehouse.
    - Set item.warehouse from warehouses at 0.
  - Otherwise.
    - If item.warehouse does not belong to warehouses.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Stock is reserved for item {1} in warehouse {2}.”.format(item.idx, Platform.bold(item.item\_code), Platform.bold(warehouses at 0) when len(warehouses) equals 1, otherwis ….
        - Value choice on len(warehouses) equals 1 — true gives Platform.bold(warehouses at 0), false gives translated “{0} and {1}”.format(Platform.bold(“, ”.join(warehouses at slice no value to negative 1)), Platform.bold(warehouses at negative 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L51) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L349)

<a id="op-5e19325880c5fc"></a>
### Selling Controller.validate price list country

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_validate_price_list_country`

**Inputs** self.

**Record and data access** read “Address” via get\_value.

**Explicit results** no value.

**Local steps**

- Bind dependencies validate\_price\_list\_country.
- If (self.get(“is\_return”) or not self.get(“customer\_address”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_return”) → not self.get(“customer\_address”).
  - Return no value.
- Set country from Platform.db.get\_value(“Address”, self.customer\_address, “country”).
- Evaluate validate\_price\_list\_country(self.get(“selling\_price\_list”), country).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L350)

<a id="op-4ab21d1469dcbd"></a>
### Selling Controller.validate standalone serial nos customer

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_standalone_serial_numbers_customer`

**Inputs** self.

**Record and data access** read “Serial and Batch Entry” via get\_all · read “Serial No” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Serial No {0} is already assigned to customer {1}. Can only be returned against the customer {1}”.format(Platform.bold(sn.name), Platform.bold(sn.customer)).

**Local steps**

- If (not self.is\_return or self.return\_against).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.is\_return → self.return\_against.
  - Return no value.
- If self.doctype belongs to list(“Sales Invoice”, “Delivery Note”).
  - Set bundle\_ids from list of d.serial\_and\_batch\_bundle for d drawn from self.get(“items”) where d.serial\_and\_batch\_bundle.
    - Draw d from self.get(“items”), keep a combination only if (d.serial\_and\_batch\_bundle).
  - If not bundle\_ids.
    - Return no value.
  - Set serial\_nos from Platform.get\_all(“Serial and Batch Entry”, filters = mapping(“parent” → tuple(“in”, bundle\_ids), “serial\_no” → tuple(“is”, “set”)), pluck = “serial\_no”).
  - If not serial\_nos.
    - Return no value.
  - If serial\_nos bound to Platform.get\_all(“Serial No”, filters = mapping(“name” → tuple(“in”, serial\_nos), “customer” → tuple(“is”, “set”)), fields = list(“name”, “customer”)).
    - For each sn in serial\_nos.
      - If (sn.customer and sn.customer differs from self.customer).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in sn.customer → sn.customer differs from self.customer.
        - Call the validation error handler Platform.throw(translated “Serial No {0} is already assigned to customer {1}. Can only be returned against the customer {1}”.format(Platform.bold(sn.name), Platform.bold(sn.customer)), title = translated “ ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L3510) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L911) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L592)

<a id="op-37796d6e31450e"></a>
### Selling Controller.set missing values

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_missing_values`

**Inputs** self, for\_validate = false.

**Local steps**

- Evaluate super().set\_missing\_values(for\_validate).
- Evaluate self.set\_missing\_lead\_customer\_details(for\_validate = for\_validate).
- Evaluate self.set\_price\_list\_and\_item\_details(for\_validate = for\_validate).
- Evaluate self.set\_company\_contact\_person().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set missing lead customer details](operations-020.md#op-0843df428d0f8b), [set price list and item details](operations-020.md#op-79feaddadfe555), [set company contact person](operations-020.md#op-ef63cd02ade585).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L4156) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L890) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L571)

<a id="op-0843df428d0f8b"></a>
### Selling Controller.set missing lead customer details

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_missing_lead_customer_details`

**Inputs** self, for\_validate = false.

**Local steps**

- Set tuple(customer, lead) from tuple(no value, no value).
- If getattr(self, “customer”, no value).
  - Set customer from self.customer.
- Otherwise.
  - If (self.doctype equals “Opportunity” and self.party\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Opportunity” → self.party\_name.
    - If self.opportunity\_from equals “Customer”.
      - Set customer from self.party\_name.
    - Otherwise.
      - Set lead from self.party\_name.
  - Otherwise.
    - If (self.doctype equals “Quotation” and self.party\_name).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Quotation” → self.party\_name.
      - If self.quotation\_to equals “Customer”.
        - Set customer from self.party\_name.
      - Otherwise.
        - If self.quotation\_to equals “Lead”.
          - Set lead from self.party\_name.
- If customer.
  - Bind dependencies \_get\_party\_details.
  - Set party\_details from \_get\_party\_details(customer, ignore\_permissions = self.flags.ignore\_permissions, doctype = self.doctype, company = self.company, posting\_date = self.get(“posting\_date”), …).
  - If not self.meta.get\_field(“sales\_team”).
    - Evaluate party\_details.pop(“sales\_team”).
  - If self.get(“sales\_partner”).
    - Evaluate party\_details.pop(“commission\_rate”, no value).
  - Evaluate self.update\_if\_missing(party\_details).
- Otherwise.
  - If lead.
    - Bind dependencies get\_lead\_details.
    - Evaluate self.update\_if\_missing(get\_lead\_details(lead, posting\_date = (self.get(“transaction\_date”) or self.get(“posting\_date”)), company = self.company, doctype = self.doctype)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“transaction\_date”) → self.get(“posting\_date”).
- If (self.get(“taxes\_and\_charges”) and not self.get(“taxes”) and not for\_validate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“taxes\_and\_charges”) → not self.get(“taxes”) → not for\_validate.
  - Set taxes from \_get\_taxes\_and\_charges(“Sales Taxes and Charges Template”, self.taxes\_and\_charges).
  - For each tax in taxes.
    - Evaluate self.append(“taxes”, tax).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(self, “customer”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L889) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L570)

<a id="op-79feaddadfe555"></a>
### Selling Controller.set price list and item details

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_price_list_and_item_details`

**Inputs** self, for\_validate = false.

**Local steps**

- Evaluate self.set\_price\_list\_currency(“Selling”).
- Evaluate self.set\_missing\_item\_details(for\_validate = for\_validate).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L5283) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L893) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L574)

<a id="op-ef63cd02ade585"></a>
### Selling Controller.set company contact person

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_company_contact_person`

**Inputs** self.

**Record and data access** read “Company” via get\_cached\_value.

**Local steps**

- If (self.company and self.meta.has\_field(“company\_contact\_person”) and not self.company\_contact\_person).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → self.meta.has\_field(“company\_contact\_person”) → not self.company\_contact\_person.
  - Set self.company\_contact\_person from Platform.get\_cached\_value(“Company”, self.company, “default\_sales\_contact”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, self.company, “default\_sales\_contact”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L5376) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L884) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L565)

<a id="op-28f35cbe2ec048"></a>
### Selling Controller.remove shipping charge

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_remove_shipping_charge`

**Inputs** self.

**Record and data access** read “Shipping Rule” via get\_last\_doc.

**Local steps**

- If self.shipping\_rule.
  - Set shipping\_rule from Platform.get\_last\_doc(“Shipping Rule”, self.shipping\_rule).
  - Set existing\_shipping\_charge from self.get(“taxes”, mapping(“doctype” → “Sales Taxes and Charges”, “charge\_type” → “Actual”, “account\_head” → shipping\_rule.account, “cost\_center” → shipping\_rule.cost\_center)).
  - If existing\_shipping\_charge.
    - Evaluate self.get(“taxes”).remove(existing\_shipping\_charge at negative 1).
    - Evaluate self.calculate\_taxes\_and\_totals().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L5523) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L883) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L564)

<a id="op-2dd281e469ae62"></a>
### Selling Controller.set total in words

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_total_in_words`

**Inputs** self.

**Local steps**

- Bind dependencies money\_in\_words.
- If self.meta.get\_field(“base\_in\_words”).
  - Set base\_amount from abs(self.base\_grand\_total when self.is\_rounded\_total\_disabled(), otherwise self.base\_rounded\_total).
    - Value choice on self.is\_rounded\_total\_disabled() — true gives self.base\_grand\_total, false gives self.base\_rounded\_total.
  - Set self.base\_in\_words from money\_in\_words(base\_amount, self.company\_currency).
- If self.meta.get\_field(“in\_words”).
  - Set amount from abs(self.grand\_total when self.is\_rounded\_total\_disabled(), otherwise self.rounded\_total).
    - Value choice on self.is\_rounded\_total\_disabled() — true gives self.grand\_total, false gives self.rounded\_total.
  - Set self.in\_words from money\_in\_words(amount, self.currency).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0386.json#L5808) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L897) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L578)

<a id="op-fa51625b5ab798"></a>
### Selling Controller.calculate commission

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_calculate_commission`

**Inputs** self.

**Record and data access** read “Sales Partner” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- If not self.meta.get\_field(“commission\_rate”).
  - Return no value.
- If not self.get(“sales\_partner”).
  - Set self.commission\_rate from 0.
- Otherwise.
  - If (self.commission\_rate is identical to no value or (self.get\_doc\_before\_save() and self.has\_value\_changed(“sales\_partner”) and not self.has\_value\_changed(“commission\_rate”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.commission\_rate is identical to no value → (self.get\_doc\_before\_save() and self.has\_value\_changed(“sales\_partner”) and not self.has\_value\_changed(“commission\_rate”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get\_doc\_before\_save() → self.has\_value\_changed(“sales\_partner”) → not self.has\_value\_changed(“commission\_rate”).
    - Set self.commission\_rate from (Platform.get\_cached\_value(“Sales Partner”, self.sales\_partner, “commission\_rate”) or 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_cached\_value(“Sales Partner”, self.sales\_partner, “commission\_rate”) → 0.
- Evaluate self.round\_floats\_in(self, tuple(“amount\_eligible\_for\_commission”, “commission\_rate”)).
- If not 0 ≤ self.commission\_rate ≤ 100.0.
  - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ self.commission\_rate ≤ 100.0.
  - Evaluate throw(“{} {}”.format(translated self.meta.get\_label(“commission\_rate”), translated “must be between 0 and 100”)).
- Set self.amount\_eligible\_for\_commission from sum(generator of item.base\_net\_amount for item drawn from self.items where item.grant\_commission).
  - Draw item from self.items, keep a combination only if (item.grant\_commission).
- Set self.total\_commission from flt(((self.amount\_eligible\_for\_commission × self.commission\_rate) ÷ 100.0), self.precision(“total\_commission”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Sales Partner”, self.sales\_partner, “commission\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L871) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L552)

<a id="op-ff1ed2bbec0113"></a>
### Selling Controller.calculate contribution

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_calculate_contribution`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.meta.get\_field(“sales\_team”).
  - Return no value.
- Set total from 0.0.
- Set sales\_team from self.get(“sales\_team”).
- Evaluate self.validate\_sales\_team(sales\_team).
- For each sales\_person in sales\_team.
  - Evaluate self.round\_floats\_in(sales\_person).
  - Set sales\_person.allocated\_amount from flt(((flt(self.amount\_eligible\_for\_commission) × sales\_person.allocated\_percentage) ÷ 100.0), self.precision(“allocated\_amount”, sales\_person)).
  - Set sales\_person.incentives from flt(((sales\_person.allocated\_amount × flt(sales\_person.commission\_rate)) ÷ 100.0), self.precision(“incentives”, sales\_person)).
  - Update total using + sales\_person.allocated\_percentage.
- If (sales\_team and flt(total, self.precision(“allocated\_percentage”, “sales\_team”)) differs from 100.0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sales\_team → flt(total, self.precision(“allocated\_percentage”, “sales\_team”)) differs from 100.0.
  - Evaluate throw(translated “Total allocated percentage for sales team should be 100”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate sales team](operations-020.md#op-09206f43cf440a).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L872) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L553)

<a id="op-09206f43cf440a"></a>
### Selling Controller.validate sales team

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_sales_team`

**Inputs** self, sales\_team.

**Record and data access** read “Sales Person” via get\_all · resolve a document from self.doctype via get\_doc.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Sales Person {0} is a group.”.format(Platform.bold(row.name)) · validation helper — translated “Sales Person &lt;b&gt;{0}&lt;/b&gt; is disabled.”.format(row.name) · validation helper — translated “Sales Person {0} is repeated in the sales team.”.format(Platform.bold(row.sales\_person)) · validation helper — translated “Row #{0}: Contribution (%) must be between 0 and 100”.format(row.idx) · validation helper — translated “Row #{0}: Commission Rate must be between 0 and 100”.format(row.idx).

**Local steps**

- Set sales\_team from list of row for row drawn from sales\_team where row.sales\_person.
  - Draw row from sales\_team, keep a combination only if (row.sales\_person).
- Set sales\_persons from list of d.sales\_person for d drawn from sales\_team.
  - Draw d from sales\_team.
- If not sales\_persons.
  - Return no value.
- Set sales\_person\_status from Platform.db.get\_all(“Sales Person”, filters = mapping(“name” → list(“in”, sales\_persons)), fields = list(“name”, “enabled”, “is\_group”, “commission\_rate”)).
- Set inherited from set().
- If any(generator of not row.enabled for row drawn from sales\_person\_status).
  - Draw row from sales\_person\_status.
  - Set inherited from self.get\_inherited\_sales\_persons().
- For each row in sales\_person\_status.
  - If row.is\_group.
    - Call the validation error handler Platform.throw(translated “Sales Person {0} is a group.”.format(Platform.bold(row.name))).
  - If (not row.enabled and row.name does not belong to inherited).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.enabled → row.name does not belong to inherited.
    - Call the validation error handler Platform.throw(translated “Sales Person &lt;b&gt;{0}&lt;/b&gt; is disabled.”.format(row.name)).
- Set seen from set().
- For each row in sales\_team.
  - If row.sales\_person belongs to seen.
    - Call the validation error handler Platform.throw(translated “Sales Person {0} is repeated in the sales team.”.format(Platform.bold(row.sales\_person))).
  - Evaluate seen.add(row.sales\_person).
  - If not 0 ≤ flt(row.allocated\_percentage) ≤ 100.
    - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ flt(row.allocated\_percentage) ≤ 100.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Contribution (%) must be between 0 and 100”.format(row.idx)).
- Set previous from self.get\_doc\_before\_save().
- Set previous\_rows from mapping of row.name → row for row drawn from previous.get(“sales\_team”) when previous, otherwise mapping().
  - Value choice on previous — true gives mapping of row.name → row for row drawn from previous.get(“sales\_team”), false gives mapping().
  - Draw row from previous.get(“sales\_team”).
- Set master\_rates from mapping of row.name → flt(row.commission\_rate) for row drawn from sales\_person\_status.
  - Draw row from sales\_person\_status.
- Set return\_rates from mapping().
- If (self.get(“is\_return”) and self.get(“return\_against”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → self.get(“return\_against”).
  - Set source from Platform.get\_doc(self.doctype, self.return\_against).
  - Set return\_rates from mapping of row.sales\_person → row.commission\_rate for row drawn from source.sales\_team.
    - Draw row from source.sales\_team.
- For each row in sales\_team.
  - Set previous\_row from previous\_rows.get(row.name).
  - If (previous\_row and previous\_row.sales\_person equals row.sales\_person).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_row → previous\_row.sales\_person equals row.sales\_person.
    - Set commission\_rate from previous\_row.commission\_rate.
  - Otherwise.
    - Set commission\_rate from return\_rates.get(row.sales\_person, master\_rates at row.sales\_person).
  - If any(generator of not 0 ≤ flt(rate) ≤ 100 for rate drawn from tuple(row.commission\_rate, commission\_rate)).
    - Draw rate from tuple(row.commission\_rate, commission\_rate).
    - Compare adjacent operands in order, stopping at the first false comparison in 0 ≤ flt(rate) ≤ 100.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Commission Rate must be between 0 and 100”.format(row.idx)).
  - Set row.commission\_rate from commission\_rate.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get inherited sales persons](operations-020.md#op-740be3213e9d26).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L907) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L588)

<a id="op-740be3213e9d26"></a>
### Selling Controller.get inherited sales persons

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_get_inherited_sales_persons`

**Inputs** self.

**Record and data access** read “Sales Team” via get\_all.

**Explicit results** inherited.

**Local steps**

- Set inherited from set().
- For each tuple(doctype, names) in self.get\_sales\_team\_sources().items().
  - Evaluate inherited.update(Platform.get\_all(“Sales Team”, filters = mapping(“parenttype” → doctype, “parent” → list(“in”, list(names))), pluck = “sales\_person”)).
- Return inherited.

**Methods declared on this owner** [get sales team sources](operations-020.md#op-bed44b152a0f4d).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L345)

<a id="op-bed44b152a0f4d"></a>
### Selling Controller.get sales team sources

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_get_sales_team_sources`

**Inputs** self.

**Explicit results** sources.

**Local steps**

- Set sources from mapping().
- Bind local operation add for subsequent calls.
- If self.get(“is\_return”).
  - Evaluate add(self.doctype, self.get(“return\_against”)).
- Evaluate add(self.doctype, self.get(“amended\_from”)).
- If self.doctype equals “Sales Invoice”.
  - For each item in (self.get(“items”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“items”) → list().
    - Evaluate add(“Delivery Note”, item.get(“delivery\_note”)).
- Return sources.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L346)

<a id="op-dfe8ba8b0d09b0"></a>
### Selling Controller.get sales team sources.add

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_get_sales_team_sources_add`

**Inputs** doctype, name.

**Local steps**

- If name.
  - Evaluate sources.setdefault(doctype, set()).add(name).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L347)

<a id="op-ba23c01ec0485c"></a>
### Selling Controller.validate max discount

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_maximum_discount`

**Inputs** self.

**Record and data access** read “Item” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Maximum discount for Item {0} is {1}%”.format(d.item\_code, discount).

**Local steps**

- For each d in self.get(“items”).
  - If d.item\_code.
    - Set discount from flt(Platform.get\_cached\_value(“Item”, d.item\_code, “max\_discount”)).
    - If (discount and (flt(d.discount\_percentage) &gt; discount or (flt(d.rate\_with\_margin) &gt; 0 and flt(d.discount\_amount) &gt; flt(((nested operand in the contract × nested operand in the contract) ÷ 100), nested opera ….
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in discount → (flt(d.discount\_percentage) &gt; discount or (flt(d.rate\_with\_margin) &gt; 0 and flt(d.discount\_amount) &gt; flt(((nested operand in the contract(nested operand in the contract) × discount) ÷ 100), d.precision(“dis ….
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(d.discount\_percentage) &gt; discount → (flt(d.rate\_with\_margin) &gt; 0 and flt(d.discount\_amount) &gt; flt(((flt(nested operand in the contract.rate\_with\_margin) × discount) ÷ 100), d.precision(“discount\_amount”))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in flt(d.rate\_with\_margin) &gt; 0 → flt(d.discount\_amount) &gt; flt(((flt(d.rate\_with\_margin) × discount) ÷ 100), d.precision(“discount\_amount”)).
      - Call the validation error handler Platform.throw(translated “Maximum discount for Item {0} is {1}%”.format(d.item\_code, discount)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Item”, d.item\_code, “max\_discount”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L906) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L587)

<a id="op-84835d138ce2a9"></a>
### Selling Controller.set qty as per stock uom

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_set_quantity_as_per_stock_unit_of_measure`

**Inputs** self.

**Record and data access** read “Stock Settings” via get\_single\_value.

**Explicit failure paths** validation helper — translated “Row {0}: Conversion Factor is mandatory”.format(d.idx).

**Local steps**

- Set allow\_to\_edit\_stock\_qty from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”).
- For each d in self.get(“items”).
  - If d.meta.get\_field(“stock\_qty”).
    - If not d.conversion\_factor.
      - Call the validation error handler Platform.throw(translated “Row {0}: Conversion Factor is mandatory”.format(d.idx)).
    - Set d.stock\_qty from (flt(d.qty) × flt(d.conversion\_factor)).
    - If allow\_to\_edit\_stock\_qty.
      - Set d.stock\_qty from flt(d.stock\_qty, d.precision(“stock\_qty”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Stock Settings”, “allow\_to\_edit\_stock\_uom\_qty\_for\_sales”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0387.json#L261) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L895) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L576)

<a id="op-e82d982027d7a2"></a>
### Selling Controller.validate selling price

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_selling_price`

**Inputs** self.

**Record and data access** read “Selling Settings” via get\_single\_value · read “Item” via get\_cached\_value.

**Explicit results** no value.

**Local steps**

- Bind local operation throw\_message for subsequent calls.
- If (self.get(“is\_return”) or not Platform.get\_single\_value(“Selling Settings”, “validate\_selling\_price”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_return”) → not Platform.get\_single\_value(“Selling Settings”, “validate\_selling\_price”).
  - Return no value.
- If self.is\_internal\_transfer().
  - Return no value.
- Set is\_internal\_customer from self.get(“is\_internal\_customer”).
- For each item in self.items.
  - If (not item.item\_code or item.is\_free\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.item\_code → item.is\_free\_item.
    - Continue with the next iteration or loop test.
  - Set tuple(last\_purchase\_rate, is\_stock\_item) from Platform.get\_cached\_value(“Item”, item.item\_code, tuple(“last\_purchase\_rate”, “is\_stock\_item”)).
  - Set last\_purchase\_rate\_in\_sales\_uom from flt((last\_purchase\_rate × (item.conversion\_factor or 1)), item.precision(“base\_net\_rate”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
  - If flt(item.base\_net\_rate) &lt; flt(last\_purchase\_rate\_in\_sales\_uom).
    - Evaluate throw\_message(item.idx, item.item\_name, last\_purchase\_rate\_in\_sales\_uom, “last purchase rate”).
  - If (is\_internal\_customer or not is\_stock\_item).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_internal\_customer → not is\_stock\_item.
    - Continue with the next iteration or loop test.
  - Set rate\_field from “valuation\_rate” when self.doctype belongs to list(“Sales Order”, “Quotation”), otherwise “incoming\_rate”.
    - Value choice on self.doctype belongs to list(“Sales Order”, “Quotation”) — true gives “valuation\_rate”, false gives “incoming\_rate”.
  - If (item.get(rate\_field) and item.base\_net\_rate &lt; valuation\_rate bound to flt((nested operand in the contract.get(rate\_field) × (nested operand in the contract.conversion\_factor or 1)), item.precision(“base\_n ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(rate\_field) → item.base\_net\_rate &lt; valuation\_rate bound to flt((item.get(rate\_field) × (item.conversion\_factor or 1)), item.precision(“base\_net\_rate”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.conversion\_factor → 1.
    - Evaluate throw\_message(item.idx, item.item\_name, valuation\_rate, “valuation rate”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Selling Settings”, “validate\_selling\_price”), Platform.get\_cached\_value(“Item”, item.item\_code, tuple(“last\_purchase\_rate”, “is\_stock\_item”)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L590)

<a id="op-6a77567912f8bc"></a>
### Selling Controller.validate selling price.throw message

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_validate_selling_price_throw_message`

**Inputs** idx, item\_name, rate, ref\_rate\_field.

**Local steps**

- Evaluate throw(translated multiline text in the contract.format(idx, bold(item\_name), bold(ref\_rate\_field), bold(“net rate”), …), title = translated “Invalid Selling Price”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0029.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L910) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L591)

<a id="op-9a88f8932cc987"></a>
### Selling Controller.make packed item bundles

`operation_enterprise_binding_enterprise_controllers_selling_controller_sellingcontroller_make_packed_item_bundles`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Set packed\_rows from list of p for p drawn from self.get\_current\_packed\_rows() where not p.serial\_and\_batch\_bundle.
  - Draw p from self.get\_current\_packed\_rows(), keep a combination only if (not p.serial\_and\_batch\_bundle).
- If not packed\_rows.
  - Return no value.
- Set picked\_serial\_nos from self.get\_serial\_nos\_used\_in\_rows().
- Set picked\_batches from self.get\_batches\_used\_in\_rows().
- Set item\_rows from mapping of d.name → d for d drawn from self.items.
  - Draw d from self.items.
- For each p in packed\_rows.
  - Evaluate get\_serial\_and\_batch\_bundle(p, self, item\_rows at p.parent\_detail\_docname, picked\_serial\_nos, …).
- If self.is\_batch\_check\_needed().
  - Evaluate self.validate\_outward\_bundle\_batches(rows = packed\_rows).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0014.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L348)

<a id="op-17458b31ca2d3b"></a>
### Selling Controller.get item list

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_get_item_list`

**Inputs** self.

**Explicit results** il.

**Local steps**

- Set il from list().
- For each d in self.get(“items”).
  - If self.has\_product\_bundle(d.item\_code).
    - For each p in self.get(“packed\_items”).
      - If (p.parent\_detail\_docname equals d.name and p.parent\_item equals d.item\_code).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in p.parent\_detail\_docname equals d.name → p.parent\_item equals d.item\_code.
        - Evaluate il.append(Platform.\_dict(mapping(“warehouse” → (p.warehouse or d.warehouse), “item\_code” → p.item\_code, “qty” → flt(p.qty), “serial\_no” → p.serial\_no when self.docstatus equals 2, otherwise no value, …))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in p.warehouse → d.warehouse.
          - Value choice on self.docstatus equals 2 — true gives p.serial\_no, false gives no value.
          - Value choice on self.docstatus equals 2 — true gives p.batch\_no, false gives no value.
  - Otherwise.
    - Evaluate il.append(Platform.\_dict(mapping(“warehouse” → d.warehouse, “item\_code” → d.item\_code, “qty” → d.stock\_qty, “serial\_no” → d.serial\_no when self.docstatus equals 2, otherwise no value, …))).
      - Value choice on self.docstatus equals 2 — true gives d.serial\_no, false gives no value.
      - Value choice on self.docstatus equals 2 — true gives d.batch\_no, false gives no value.
- Return il.

**Methods declared on this owner** [has product bundle](operations-020.md#op-a9de367f9061d1).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0028.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L876) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L557)

<a id="op-a9de367f9061d1"></a>
### Selling Controller.has product bundle

`operation_enterprise_controllers_selling_controller_business_behavior_selling_controller_has_product_bundle`

**Inputs** self, item\_code.

**Explicit results** product\_bundle\_items at item\_code.

**Local steps**

- Set product\_bundle\_items from getattr(self, “\_product\_bundle\_items”, no value).
- If product\_bundle\_items is identical to no value.
  - Set self.\_product\_bundle\_items, product\_bundle\_items from mapping().
- If item\_code does not belong to product\_bundle\_items.
  - Evaluate self.\_fetch\_product\_bundle\_items(item\_code).
- Return product\_bundle\_items at item\_code.

**Methods declared on this owner** [fetch product bundle items](operations-021.md#op-54005c77ee891f).

**Values supplied outside this operation** selected callable from getattr(self, “\_product\_bundle\_items”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0387.json#L3092) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L881) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L562)
