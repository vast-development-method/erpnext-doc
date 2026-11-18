# Accounting and settlement · operations 92

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Promotional scheme

[Record definition](../../../../data/record-types/promotional_scheme.json)

<a id="op-1589dca492c745"></a>
### Are price lists distinct

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_are_price_lists_distinct`

**Inputs** slab, other\_slab.

**Explicit results** false · true · all(generator of (d.get(“rate\_or\_discount”) or “Discount Percentage”) equals “Discount Percentage” for d drawn from tuple(slab, other\_slab)).

**Local steps**

- Set price\_lists from set((slab.get(“for\_price\_list”) or empty text), (other\_slab.get(“for\_price\_list”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in slab.get(“for\_price\_list”) → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in other\_slab.get(“for\_price\_list”) → empty text.
- <a id="op-1589dca492c745-guard-3"></a>If len(price\_lists) equals 1.
  - Return false.
- If empty text does not belong to price\_lists.
  - Return true.
- Return all(generator of (d.get(“rate\_or\_discount”) or “Discount Percentage”) equals “Discount Percentage” for d drawn from tuple(slab, other\_slab)).
  - Draw d from tuple(slab, other\_slab).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in d.get(“rate\_or\_discount”) → “Discount Percentage”.

**Derived branch illustrations**

- At the comparison len(price\_lists) equals 1, length of price\_lists = 1 selects the branch that returns false. With length of price\_lists = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-1589dca492c745-guard-3)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L293) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L931)

<a id="op-f665690c7ac5cf"></a>
### Are ranges overlapping

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_are_ranges_overlapping`

**Inputs** min\_value, max\_value, other\_min\_value, other\_max\_value.

**Explicit results** max(flt(min\_value), flt(other\_min\_value)) ≤ upper\_limit.

**Local steps**

- Set upper\_limit from min((flt(max\_value) or math.inf), (flt(other\_max\_value) or math.inf)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(max\_value) → math.inf.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in flt(other\_max\_value) → math.inf.
- Return max(flt(min\_value), flt(other\_min\_value)) ≤ upper\_limit.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L294) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L932)

<a id="op-04abf95eb42c40"></a>
### Raise for transaction exists

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_raise_for_transaction_exists`

**Inputs** name.

**Explicit failure paths** validation helper with TransactionExists — translated msg.

**Local steps**

- Set msg from formatted text You can't change the {Platform.bold(translated “Applicable For”)}  because transactions are present against the Promotional Scheme {Platform.bold(nam.
- Update msg using + “Kindly disable this Promotional Scheme and create new for new Applicable For.”.
- Call the validation error handler Platform.throw(translated msg, TransactionExists).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L2030) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L728) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L900)

<a id="op-fca21ca21356db"></a>
### Get linked pricing rules

`operation_enterprise_binding_enterprise_accounts_doctype_promotional_scheme_promotional_scheme_get_linked_pricing_rules`

**Inputs** pricing\_rules.

**Record and data access** read link\_field.parent via get\_single\_value · read link\_field.parent via get\_all.

**Explicit results** linked\_pricing\_rules.

**Local steps**

- Set linked\_pricing\_rules from set().
- For each link\_field in get\_link\_fields(“Pricing Rule”).
  - If link\_field.issingle is identical to no value.
    - Continue with the next iteration or loop test.
  - If link\_field.issingle.
    - Evaluate linked\_pricing\_rules.add(Platform.db.get\_single\_value(link\_field.parent, link\_field.fieldname)).
    - Continue with the next iteration or loop test.
  - Evaluate linked\_pricing\_rules.update(Platform.get\_all(link\_field.parent, filters = mapping(link\_field.fieldname → list(“in”, pricing\_rules)), pluck = link\_field.fieldname, distinct = true)).
- Return linked\_pricing\_rules.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(link\_field.parent, link\_field.fieldname).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L297) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L935)

<a id="op-ccdbe52f81094e"></a>
### Get pricing rules

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_get_pricing_rules`

**Inputs** doc, rules = no value.

**Explicit results** new\_doc.

**Local steps**

- If rules is identical to no value.
  - Set rules from mapping().
- Set new\_doc from list().
- For each tuple(child\_doc, fields) in mapping(“price\_discount\_slabs” → price\_discount\_fields, “product\_discount\_slabs” → product\_discount\_fields).items().
  - If doc.get(child\_doc).
    - Evaluate new\_doc.extend(\_get\_pricing\_rules(doc, child\_doc, fields, rules)).
- Return new\_doc.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L2212) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L717) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L889)

<a id="op-d840b5109e371b"></a>
### Get pricing rules

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_get_pricing_rules_2`

**Inputs** doc, child\_doc, discount\_fields, rules = no value.

**Explicit results** new\_doc.

**Local steps**

- If rules is identical to no value.
  - Set rules from mapping().
- Set new\_doc from list().
- Set args from get\_args\_for\_pricing\_rule(doc).
- Set applicable\_for from Platform.scrub(doc.get(“applicable\_for”)).
- For each tuple(\_idx, d) in enumerate(doc.get(child\_doc)).
  - If d.name belongs to rules.
    - If not args.get(applicable\_for).
      - Set docname from get\_pricing\_rule\_docname(d).
      - Set pr from prepare\_pricing\_rule(args, doc, child\_doc, discount\_fields, …).
      - Evaluate new\_doc.append(pr).
    - Otherwise.
      - For each applicable\_for\_value in args.get(applicable\_for).
        - Set docname from get\_pricing\_rule\_docname(d, applicable\_for, applicable\_for\_value).
        - Set pr from prepare\_pricing\_rule(args, doc, child\_doc, discount\_fields, …).
        - Evaluate new\_doc.append(pr).
  - Otherwise.
    - If args.get(applicable\_for).
      - Set applicable\_for\_values from (args.get(applicable\_for) or list()).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(applicable\_for) → list().
      - For each applicable\_for\_value in applicable\_for\_values.
        - Set pr from prepare\_pricing\_rule(args, doc, child\_doc, discount\_fields, applicable\_for = applicable\_for, value = applicable\_for\_value, …).
        - Evaluate new\_doc.append(pr).
    - Otherwise.
      - Set pr from prepare\_pricing\_rule(args, doc, child\_doc, discount\_fields, …).
      - Evaluate new\_doc.append(pr).
- Return new\_doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L2451) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L718) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L890)

<a id="op-afa4eeca672d38"></a>
### Get pricing rule docname

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_get_pricing_rule_record_name`

**Inputs** row, applicable\_for = no value, applicable\_for\_value = no value.

**Declared result** str.

**Record and data access** read “Pricing Rule” via get\_all.

**Explicit results** docname at 0.name when docname, otherwise empty text.

**Local steps**

- Set fields from list(“promotional\_scheme\_id”, “name”).
- Set filters from mapping(“promotional\_scheme\_id” → row.name).
- If applicable\_for.
  - Evaluate fields.append(applicable\_for).
  - Set filters at applicable\_for from applicable\_for\_value.
- Set docname from Platform.get\_all(“Pricing Rule”, fields = fields, filters = filters).
- Return docname at 0.name when docname, otherwise empty text.
  - Value choice on docname — true gives docname at 0.name, false gives empty text.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L3216) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L716) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L888)

<a id="op-36e954157618c0"></a>
### Prepare pricing rule

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_prepare_pricing_rule`

**Inputs** args, doc, child\_doc, discount\_fields, d, docname = no value, applicable\_for = no value, value = no value.

**Record and data access** resolve a document from “Pricing Rule” via get\_doc.

**State and service calls** request new\_doc for “Pricing Rule”.

**Explicit results** set\_args(temp\_args, pr, doc, child\_doc, …).

**Local steps**

- If docname.
  - Set pr from Platform.get\_doc(“Pricing Rule”, docname).
- Otherwise.
  - Set pr from Platform.new\_doc(“Pricing Rule”).
- Set pr.title from doc.name.
- Set temp\_args from args.copy().
- If value.
  - Set temp\_args at applicable\_for from value.
- Return set\_args(temp\_args, pr, doc, child\_doc, …).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L3508) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L719) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L891)

<a id="op-d522d0e5c06e6c"></a>
### Set args

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_set_arguments`

**Inputs** args, pr, doc, child\_doc, discount\_fields, child\_doc\_fields.

**Explicit results** pr.

**Local steps**

- Evaluate pr.update(args).
- For each field in (other\_fields + discount\_fields).
  - Set target\_field from field.
  - If target\_field belongs to list(“min\_amount”, “max\_amount”).
    - Set target\_field from “min\_amt” when field equals “min\_amount”, otherwise “max\_amt”.
      - Value choice on field equals “min\_amount” — true gives “min\_amt”, false gives “max\_amt”.
  - Evaluate pr.set(target\_field, child\_doc\_fields.get(field)).
- Set pr.promotional\_scheme\_id from child\_doc\_fields.name.
- Set pr.promotional\_scheme from doc.name.
- Set pr.disable from child\_doc\_fields.disable when child\_doc\_fields.disable, otherwise doc.disable.
  - Value choice on child\_doc\_fields.disable — true gives child\_doc\_fields.disable, false gives doc.disable.
- Set pr.price\_or\_product\_discount from “Price” when child\_doc equals “price\_discount\_slabs”, otherwise “Product”.
  - Value choice on child\_doc equals “price\_discount\_slabs” — true gives “Price”, false gives “Product”.
- For each field in list(“items”, “item\_groups”, “brands”).
  - If doc.get(field).
    - Evaluate pr.set(field, list()).
  - Set apply\_on from Platform.scrub(doc.get(“apply\_on”)).
  - For each d in doc.get(field).
    - Evaluate pr.append(field, mapping(apply\_on → d.get(apply\_on), “uom” → d.uom)).
- Return pr.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L3799) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L729) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L901)

<a id="op-0d77d4b05faac4"></a>
### Get args for pricing rule

`operation_enterprise_accounts_record_definitions_promotional_scheme_business_behavior_get_arguments_for_pricing_rule`

**Inputs** doc.

**Explicit results** args.

**Local steps**

- Set args from mapping(“promotional\_scheme” → doc.name).
- Set applicable\_for from Platform.scrub(doc.get(“applicable\_for”)).
- For each d in pricing\_rule\_fields.
  - If d equals applicable\_for.
    - Set items from list().
    - For each applicable\_for\_values in doc.get(applicable\_for).
      - Evaluate items.append(applicable\_for\_values.get(applicable\_for)).
    - Set args at d from items.
  - Otherwise.
    - Set args at d from doc.get(d).
- Return args.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L4449) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L715) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L887)

<a id="op-5aac10e7c446a6"></a>
### Get data

`operation_enterprise_accounts_record_definitions_promotional_scheme_promotional_scheme_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “promotional\_scheme”, “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“Pricing Rule”)))).

**Local steps**

- Return mapping(“fieldname” → “promotional\_scheme”, “transactions” → list(mapping(“label” → translated “Reference”, “items” → list(“Pricing Rule”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0144.json#L4751) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L730) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L902)

## Record · Purchase invoice

[Record definition](../../../../data/record-types/purchase_invoice.json)

<a id="op-61f5fc6bba56a8"></a>
### Purchase Invoice.initialize

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_initialize`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Evaluate super().\_\_init\_\_(expanded args, expanded names kwargs).
- Set self.status\_updater from list(mapping(“source\_dt” → “Purchase Invoice Item”, “target\_dt” → “Purchase Order Item”, “join\_field” → “po\_detail”, “target\_field” → “billed\_amt”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L98) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L752) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L924)

<a id="op-062cdb7ec365e1"></a>
### Purchase Invoice.onload

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_onload`

**Inputs** self.

**Record and data access** read “Supplier” via get\_cached\_value.

**Local steps**

- Evaluate super().onload().
- If self.supplier.
  - Set tuple(tax\_withholding\_category, tax\_withholding\_group) from Platform.get\_cached\_value(“Supplier”, self.supplier, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).
  - Evaluate self.set\_onload(“apply\_tds”, (tax\_withholding\_category or tax\_withholding\_group)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_withholding\_category → tax\_withholding\_group.
- If self.is\_new().
  - Evaluate self.set(“tax\_withholding\_entries”, list()).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Supplier”, self.supplier, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0145.json#L5758) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L759) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L931)

<a id="op-068432b512a63c"></a>
### Purchase Invoice.before save

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_before_save`

**Inputs** self.

**Local steps**

- If not self.on\_hold.
  - Set self.release\_date from empty text.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0145.json#L5997) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L743) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L915)

<a id="op-8dc2c33da3ddf0"></a>
### Purchase Invoice.invoice is blocked

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_invoice_is_blocked`

**Inputs** self.

**Explicit results** (self.on\_hold and (not self.release\_date or self.release\_date &gt; getdate(nowdate()))).

**Local steps**

- Return (self.on\_hold and (not self.release\_date or self.release\_date &gt; getdate(nowdate()))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.on\_hold → (not self.release\_date or self.release\_date &gt; getdate(nowdate())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.release\_date → self.release\_date &gt; getdate(nowdate()).

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0145.json#L6062) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L753) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L925)

<a id="op-11bbb76b95bbce"></a>
### Purchase Invoice.validate

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate`

**Inputs** self.

**Local steps**

- If not self.is\_opening.
  - Set self.is\_opening from “No”.
- Evaluate self.validate\_posting\_time().
- Evaluate self.validate\_posting\_date\_with\_po().
- Evaluate super().validate().
- If not self.is\_return.
  - Evaluate self.po\_required().
  - Evaluate self.pr\_required().
  - Evaluate self.validate\_supplier\_invoice().
- If self.is\_paid equals 1.
  - Evaluate self.validate\_cash().
- Evaluate validate\_service\_stop\_date(self).
- Evaluate self.validate\_release\_date().
- Evaluate self.check\_conversion\_rate().
- Evaluate self.validate\_credit\_to\_acc().
- Evaluate self.clear\_unallocated\_advances(“Purchase Invoice Advance”, “advances”).
- Evaluate self.check\_purchase\_order\_on\_hold\_or\_close(“purchase\_order”, exclude\_if\_field = “purchase\_receipt”).
- Evaluate self.validate\_closed\_purchase\_receipts().
- Evaluate self.validate\_with\_previous\_doc().
- Evaluate self.validate\_uom\_is\_integer(“uom”, “qty”).
- Evaluate self.validate\_uom\_is\_integer(“stock\_uom”, “stock\_qty”).
- Evaluate self.set\_expense\_account(for\_validate = true).
- Evaluate self.validate\_expense\_account().
- Evaluate self.set\_against\_expense\_account().
- Evaluate self.validate\_write\_off\_account().
- Evaluate self.validate\_write\_off\_cost\_center().
- Evaluate self.validate\_multiple\_billing(“Purchase Receipt”, “pr\_detail”, “amount”).
- Evaluate self.set\_status().
- Evaluate self.validate\_purchase\_receipt\_if\_update\_stock().
- Evaluate self.validate\_exchange\_rate\_with\_purchase\_receipt().
- Evaluate validate\_inter\_company\_party(self.doctype, self.supplier, self.company, self.inter\_company\_invoice\_reference).
- Evaluate self.reset\_default\_field\_value(“set\_warehouse”, “items”, “warehouse”).
- Evaluate self.reset\_default\_field\_value(“rejected\_warehouse”, “items”, “rejected\_warehouse”).
- Evaluate self.reset\_default\_field\_value(“set\_from\_warehouse”, “items”, “from\_warehouse”).
- Evaluate PurchaseTaxWithholding(self).on\_validate().
- Evaluate self.set\_percentage\_received().
- If self.on\_hold.
  - Evaluate self.validate\_invoice\_hold().

If control reaches the end, it returns no value.

**Methods declared on this owner** [po required](operations-093.md#op-3b2bc1c4dac60e), [pr required](operations-093.md#op-f4b25926c8b5ae), [validate supplier invoice](operations-094.md#op-d572acf1cdbcfb), [validate cash](operations-092.md#op-c0c5d0b4e3a245), [validate release date](operations-092.md#op-fe315f014fa5f4), [validate credit to acc](operations-093.md#op-22905084f07d52), [validate closed purchase receipts](operations-092.md#op-000a63f1faa235), [validate with previous doc](operations-093.md#op-2a24938920a49e), [set expense account](operations-093.md#op-f2164f97ab5a2d), [validate expense account](operations-093.md#op-65fff90cccc550), [set against expense account](operations-093.md#op-3a5032940eb443), [validate write off account](operations-093.md#op-a5e7b362251f87), [validate write off cost center](operations-093.md#op-bdc7f431a4775d), [set status](operations-095.md#op-89809126a1dff5), [validate purchase receipt if update stock](operations-093.md#op-708a7e1405944a), [validate exchange rate with purchase receipt](operations-092.md#op-22c280f2018fdd), [set percentage received](operations-092.md#op-836d9f48f1c4e4), [validate invoice hold](operations-092.md#op-d26e935504da6d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L771) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L943)

<a id="op-836d9f48f1c4e4"></a>
### Purchase Invoice.set percentage received

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_set_percentage_received`

**Inputs** self.

**Local steps**

- Set total\_billed\_qty from 0.0.
- Set total\_received\_qty from 0.0.
- For each row in self.items.
  - If (row.purchase\_receipt and row.pr\_detail and row.received\_qty).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.purchase\_receipt → row.pr\_detail → row.received\_qty.
    - Update total\_billed\_qty using + row.qty.
    - Update total\_received\_qty using + row.received\_qty.
- If (total\_billed\_qty and total\_received\_qty).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in total\_billed\_qty → total\_received\_qty.
  - Set self.per\_received from ((total\_received\_qty ÷ total\_billed\_qty) × 100).

If control reaches the end, it returns no value.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L765) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L937)

<a id="op-22c280f2018fdd"></a>
### Purchase Invoice.validate exchange rate with purchase receipt

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_exchange_rate_with_purchase_receipt`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Purchase Receipt” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Exchange rate {0} does not match the exchange rate of Purchase Receipt {1}. Use the same exchange rate as th …”.format(Platform.bold(self.conversion\_rate), “, ”.join(mismatched), Platform.bold( ….

**Local steps**

- If (self.is\_internal\_transfer() or not Enterprise.is\_perpetual\_inventory\_enabled(self.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_internal\_transfer() → not Enterprise.is\_perpetual\_inventory\_enabled(self.company).
  - Return no value.
- If Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).
  - Return no value.
- Set stock\_items from self.get\_stock\_items().
- Set receipts from set of item.purchase\_receipt for item drawn from self.items where (item.purchase\_receipt and item.item\_code belongs to stock\_items).
  - Draw item from self.items, keep a combination only if ((item.purchase\_receipt and item.item\_code belongs to stock\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.purchase\_receipt → item.item\_code belongs to stock\_items.
- Evaluate receipts.update(self.get\_receipts\_billed\_through\_order(stock\_items)).
- If not receipts.
  - Return no value.
- Set mismatched from list of formatted text {Platform.bold(row.name)} ({row.conversion\_rate}) for row drawn from Platform.get\_all(“Purchase Receipt”, filters = mapping(“name” → tuple(“in”, list(receipts))), fields = list(“name ….
  - Draw row from Platform.get\_all(“Purchase Receipt”, filters = mapping(“name” → tuple(“in”, list(receipts))), fields = list(“name”, “currency”, “conversion\_rate”)), keep a combination only if ((row.currency equals self.currency and flt(row.conversion\_rate) and flt(row.conversion\_rate) differs from flt(self.conversion\_rate))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.currency equals self.currency → flt(row.conversion\_rate) → flt(row.conversion\_rate) differs from flt(self.conversion\_rate).
- If not mismatched.
  - Return no value.
- Call the validation error handler Platform.throw(translated “Exchange rate {0} does not match the exchange rate of Purchase Receipt {1}. Use the same exchange rate as th …”.format(Platform.bold(self.conversion\_rate), “, ”.join(mismatched), ….

If control reaches the end, it returns no value.

**Methods declared on this owner** [get receipts billed through order](operations-092.md#op-8923b85cacac59).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “set\_landed\_cost\_based\_on\_purchase\_invoice\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L775) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L947)

<a id="op-8923b85cacac59"></a>
### Purchase Invoice.get receipts billed through order

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_get_receipts_billed_through_order`

**Inputs** self, stock\_items.

**Explicit results** set() · receipts\_to\_validate.

**Local steps**

- If (self.update\_stock or self.is\_return).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.update\_stock → self.is\_return.
  - Return set().
- Set po\_details from list(set of item.po\_detail for item drawn from self.items where (item.po\_detail and not item.pr\_detail and item.item\_code belongs to stock\_items)).
  - Draw item from self.items, keep a combination only if ((item.po\_detail and not item.pr\_detail and item.item\_code belongs to stock\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.po\_detail → not item.pr\_detail → item.item\_code belongs to stock\_items.
- If not po\_details.
  - Return set().
- Set pr\_items from get\_purchase\_receipts\_against\_po\_details(po\_details).
- If not pr\_items.
  - Return set().
- Set po\_billed\_amounts from get\_billed\_amount\_against\_po(po\_details).
- Set pr\_billed\_amounts from get\_billed\_amount\_against\_pr(list of item.name for item drawn from pr\_items).
  - Draw item from pr\_items.
- For each item in self.items.
  - If item.pr\_detail.
    - Set pr\_billed\_amounts at item.pr\_detail from (pr\_billed\_amounts.get(item.pr\_detail, 0) + flt(item.amount)).
  - Otherwise.
    - If item.po\_detail belongs to po\_details.
      - Set billed from po\_billed\_amounts.setdefault(item.po\_detail, mapping(“billed\_amt” → 0, “billed\_qty” → 0)).
      - Update billed at “billed\_amt” using + flt(item.amount).
      - Update billed at “billed\_qty” using + flt(item.qty).
- Evaluate set\_qty\_and\_amount\_net\_of\_returns(pr\_items).
- Set receipts\_to\_validate from set().
- For each pr\_item in pr\_items.
  - Set billed\_details from po\_billed\_amounts.get(pr\_item.purchase\_order\_item, mapping()).
  - Set billed\_amt\_against\_po from flt(billed\_details.get(“billed\_amt”)).
  - Set billed\_qty\_against\_po from flt(billed\_details.get(“billed\_qty”)).
  - Set billed\_amt\_against\_pr from flt(pr\_billed\_amounts.get(pr\_item.name, 0)).
  - If (billed\_amt\_against\_po and billed\_amt\_against\_pr &lt; pr\_item.net\_amount).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in billed\_amt\_against\_po → billed\_amt\_against\_pr &lt; pr\_item.net\_amount.
    - If (not billed\_amt\_against\_pr and billed\_qty\_against\_po and billed\_qty\_against\_po &gt; pr\_item.net\_qty).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not billed\_amt\_against\_pr → billed\_qty\_against\_po → billed\_qty\_against\_po &gt; pr\_item.net\_qty.
      - Set billed\_amt\_against\_pr from ((billed\_amt\_against\_po × flt(pr\_item.net\_qty)) ÷ billed\_qty\_against\_po).
      - Update po\_billed\_amounts at pr\_item.purchase\_order\_item at “billed\_amt” using − billed\_amt\_against\_pr.
      - Update po\_billed\_amounts at pr\_item.purchase\_order\_item at “billed\_qty” using − pr\_item.net\_qty.
    - Otherwise.
      - Set pending\_to\_bill from (flt(pr\_item.net\_amount) − billed\_amt\_against\_pr).
      - Set consumed\_amt from min(pending\_to\_bill, billed\_amt\_against\_po).
      - Update billed\_amt\_against\_pr using + consumed\_amt.
      - Update po\_billed\_amounts at pr\_item.purchase\_order\_item at “billed\_amt” using − consumed\_amt.
      - Update po\_billed\_amounts at pr\_item.purchase\_order\_item at “billed\_qty” using × (1 − (consumed\_amt ÷ billed\_amt\_against\_po)).
  - If flt((billed\_amt\_against\_pr − flt(pr\_item.billed\_amt)), self.precision(“amount”, “items”)) &gt; 0.
    - Evaluate receipts\_to\_validate.add(pr\_item.parent).
- Return receipts\_to\_validate.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L43) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L314) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L952)

<a id="op-d26e935504da6d"></a>
### Purchase Invoice.validate invoice hold

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_invoice_hold`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Return Purchase Invoice cannot be held.” · validation helper — translated “Purchase Invoice can be held after submitting.”.

**Local steps**

- If self.is\_return.
  - Call the validation error handler Platform.throw(translated “Return Purchase Invoice cannot be held.”).
- <a id="op-d26e935504da6d-guard-5"></a>If self.docstatus &lt; 1.
  - Call the validation error handler Platform.throw(translated “Purchase Invoice can be held after submitting.”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison self.docstatus &lt; 1, self.docstatus = 0 (draft) selects the branch that calls the validation-error handler with translated “Purchase Invoice can be held after submitting.”. With self.docstatus = 1 (submitted), this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d26e935504da6d-guard-5)

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L972) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L777) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L949)

<a id="op-000a63f1faa235"></a>
### Purchase Invoice.validate closed purchase receipts

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_validate_closed_purchase_receipts`

**Inputs** self.

**Record and data access** read “Purchase Receipt” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Purchase Receipt {0} is closed and cannot be invoiced”.format(“, ”.join(generator of Platform.bold(name) for name drawn from closed)).

**Local steps**

- Set purchase\_receipts from set of d.purchase\_receipt for d drawn from self.items where d.purchase\_receipt.
  - Draw d from self.items, keep a combination only if (d.purchase\_receipt).
- If (self.is\_return or not purchase\_receipts).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_return → not purchase\_receipts.
  - Return no value.
- If closed bound to Platform.get\_all(“Purchase Receipt”, filters = mapping(“name” → tuple(“in”, list(purchase\_receipts)), “status” → “Closed”), pluck = “name”).
  - Call the validation error handler Platform.throw(translated “Purchase Receipt {0} is closed and cannot be invoiced”.format(“, ”.join(generator of Platform.bold(name) for name drawn from closed))).
    - Draw name from closed.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L59) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L330) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L968)

<a id="op-fe315f014fa5f4"></a>
### Purchase Invoice.validate release date

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_release_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Release date must be in the future”.

**Local steps**

- If (self.release\_date and getdate(nowdate()) ≥ getdate(self.release\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.release\_date → getdate(nowdate()) ≥ getdate(self.release\_date).
  - Call the validation error handler Platform.throw(translated “Release date must be in the future”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from nowdate().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L1119) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L780) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L952)

<a id="op-c0c5d0b4e3a245"></a>
### Purchase Invoice.validate cash

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_cash`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Cash or Bank Account is mandatory for making payment entry” · validation helper — translated “Paid amount + Write Off Amount can not be greater than Grand Total”.

**Local steps**

- If (not self.cash\_bank\_account and flt(self.paid\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.cash\_bank\_account → flt(self.paid\_amount).
  - Call the validation error handler Platform.throw(translated “Cash or Bank Account is mandatory for making payment entry”).
- If ((flt(self.paid\_amount) + flt(self.write\_off\_amount)) − flt((self.get(“rounded\_total”) or self.grand\_total))) &gt; (1 ÷ (10 to the power (self.precision(“base\_grand\_total”) + 1))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“rounded\_total”) → self.grand\_total.
  - Call the validation error handler Platform.throw(translated “Paid amount + Write Off Amount can not be greater than Grand Total”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L1265) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L773) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L945)

<a id="op-cf09fe1346b9cc"></a>
### Purchase Invoice.create remarks

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_create_remarks`

**Inputs** self.

**Local steps**

- If not self.remarks.
  - If self.bill\_no.
    - Set self.remarks from translated “Against Supplier Invoice {0}”.format(self.bill\_no).
    - If self.bill\_date.
      - Update self.remarks using + (one space + translated “dated {0}”.format(formatdate(self.bill\_date))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L1576) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L749) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L921)
