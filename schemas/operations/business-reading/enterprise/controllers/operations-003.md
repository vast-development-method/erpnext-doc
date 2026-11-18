# Shared transaction rules · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Accounts controller

<a id="op-e144558218dba6"></a>
### Accounts Controller.validate internal transaction

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_internal_transaction`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not cint(Platform.get\_single\_value(“Accounts Settings”, “maintain\_same\_internal\_transaction\_rate”)).
  - Return no value.
- Set doctypes\_list from list(“Sales Order”, “Sales Invoice”, “Purchase Order”, “Purchase Invoice”).
- If (self.doctype belongs to doctypes\_list and (self.get(“is\_internal\_customer”) or self.get(“is\_internal\_supplier”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to doctypes\_list → (self.get(“is\_internal\_customer”) or self.get(“is\_internal\_supplier”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_internal\_customer”) → self.get(“is\_internal\_supplier”).
  - Evaluate self.validate\_internal\_transaction\_based\_on\_voucher\_type().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate internal transaction based on voucher type](operations-003.md#op-a7c17b56b4c7de).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “maintain\_same\_internal\_transaction\_rate”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L63) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L963) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L203)

<a id="op-a7c17b56b4c7de"></a>
### Accounts Controller.validate internal transaction based on voucher type

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_internal_transaction_based_on_voucher_type`

**Inputs** self.

**Local steps**

- Set order from list(“Sales Order”, “Purchase Order”).
- Set invoice from list(“Sales Invoice”, “Purchase Invoice”).
- If (self.doctype belongs to order and self.get(“inter\_company\_order\_reference”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to order → self.get(“inter\_company\_order\_reference”).
  - Set linked\_doctype from “Sales Order” when self.doctype equals “Purchase Order”, otherwise “Purchase Order”.
    - Value choice on self.doctype equals “Purchase Order” — true gives “Sales Order”, false gives “Purchase Order”.
  - Evaluate self.validate\_line\_items(linked\_doctype, “sales\_order” when linked\_doctype equals “Sales Order”, otherwise “purchase\_order”, “sales\_order\_item” when linked\_doctype equals “Sales Order”, otherwise “purchase ….
    - Value choice on linked\_doctype equals “Sales Order” — true gives “sales\_order”, false gives “purchase\_order”.
    - Value choice on linked\_doctype equals “Sales Order” — true gives “sales\_order\_item”, false gives “purchase\_order\_item”.
- Otherwise.
  - If (self.doctype belongs to invoice and self.get(“inter\_company\_invoice\_reference”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to invoice → self.get(“inter\_company\_invoice\_reference”).
    - Set linked\_doctype from “Sales Invoice” when self.doctype equals “Purchase Invoice”, otherwise “Purchase Invoice”.
      - Value choice on self.doctype equals “Purchase Invoice” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
    - Evaluate self.validate\_line\_items(linked\_doctype, “sales\_invoice” when linked\_doctype equals “Sales Invoice”, otherwise “purchase\_invoice”, “sales\_invoice\_item” when linked\_doctype equals “Sales Invoice”, otherwise ….
      - Value choice on linked\_doctype equals “Sales Invoice” — true gives “sales\_invoice”, false gives “purchase\_invoice”.
      - Value choice on linked\_doctype equals “Sales Invoice” — true gives “sales\_invoice\_item”, false gives “purchase\_invoice\_item”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate line items](operations-003.md#op-bc454c8ef842c4).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L64) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L964) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L204)

<a id="op-bc454c8ef842c4"></a>
### Accounts Controller.validate line items

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_line_items`

**Inputs** self, ref\_dt, ref\_dn\_field, ref\_link\_field.

**Record and data access** read “Accounts Settings” via get\_cached\_value · read “Has Role” via get\_all.

**State and service calls** msgprint with translated “Row #{0}: Rate must be same as {1}: {2} ({3} / {4})”.format(d.idx, ref\_dt, self.inter\_company\_invoice\_reference when d.parenttype belongs to tuple(“Sales Invoice”, “Purchase Invoice”), otherwis ….

**Explicit failure paths** validation helper — stop\_actions.

**Local steps**

- Set tuple(action, role\_allowed\_to\_override) from Platform.get\_cached\_value(“Accounts Settings”, “Accounts Settings”, list(“maintain\_same\_rate\_action”, “role\_to\_override\_stop\_action”)).
- Set reference\_names from list of d.get(ref\_link\_field) for d drawn from self.get(“items”) where d.get(ref\_link\_field).
  - Draw d from self.get(“items”), keep a combination only if (d.get(ref\_link\_field)).
- Set reference\_details from self.get\_reference\_details(reference\_names, (ref\_dt + “ Item”)).
- Set stop\_actions from list().
- For each d in self.get(“items”).
  - If d.get(ref\_link\_field).
    - Set ref\_rate from reference\_details.get(d.get(ref\_link\_field)).
    - If (ref\_rate is distinct from no value and abs(flt((d.rate − ref\_rate), d.precision(“rate”))) ≥ 0.01).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in ref\_rate is distinct from no value → abs(flt((d.rate − ref\_rate), d.precision(“rate”))) ≥ 0.01.
      - If action equals “Stop”.
        - Set user\_roles from list of r at “role” for r drawn from Platform.get\_all(“Has Role”, filters = mapping(“parent” → Platform.session.user), fields = list(“role”)).
          - Draw r from Platform.get\_all(“Has Role”, filters = mapping(“parent” → Platform.session.user), fields = list(“role”)).
        - If role\_allowed\_to\_override does not belong to user\_roles.
          - Evaluate stop\_actions.append(translated “Row #{0}: Rate must be same as {1}: {2} ({3} / {4})”.format(d.idx, ref\_dt, self.inter\_company\_invoice\_reference when d.parenttype belongs to tuple(“Sales Invoice”, “Purchase ….
            - Value choice on d.parenttype belongs to tuple(“Sales Invoice”, “Purchase Invoice”) — true gives self.inter\_company\_invoice\_reference, false gives d.get(ref\_dn\_field).
      - Otherwise.
        - Evaluate Platform.msgprint(translated “Row #{0}: Rate must be same as {1}: {2} ({3} / {4})”.format(d.idx, ref\_dt, self.inter\_company\_invoice\_reference when d.parenttype belongs to tuple(“Sales Invoice”, “Purchase I ….
          - Value choice on d.parenttype belongs to tuple(“Sales Invoice”, “Purchase Invoice”) — true gives self.inter\_company\_invoice\_reference, false gives d.get(ref\_dn\_field).
- If stop\_actions.
  - Call the validation error handler Platform.throw(stop\_actions, as\_list = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Accounts Settings”, “Accounts Settings”, list(“maintain\_same\_rate\_action”, “role\_to\_override\_stop\_action”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L966) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L206)

<a id="op-12cd99873226e1"></a>
### Accounts Controller.disable pricing rule on internal transfer

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_disable_pricing_rule_on_internal_transfer`

**Inputs** self.

**State and service calls** msgprint with translated “Disabled pricing rules since this {} is an internal transfer”.format(self.doctype).

**Local steps**

- If (not self.get(“ignore\_pricing\_rule”) and self.is\_internal\_transfer()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.get(“ignore\_pricing\_rule”) → self.is\_internal\_transfer().
  - Set self.ignore\_pricing\_rule from 1.
  - Evaluate Platform.msgprint(translated “Disabled pricing rules since this {} is an internal transfer”.format(self.doctype), alert = 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is internal transfer](operations-006.md#op-13fa6c1b2d5ba8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L8) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L908) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L148)

<a id="op-0f94e735336fd9"></a>
### Accounts Controller.disable tax included prices for internal transfer

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_disable_tax_included_prices_for_internal_transfer`

**Inputs** self.

**State and service calls** msgprint with translated “Disabled tax included prices since this {} is an internal transfer”.format(self.doctype).

**Local steps**

- If self.is\_internal\_transfer().
  - Set tax\_updated from false.
  - For each tax in self.get(“taxes”).
    - If tax.get(“included\_in\_print\_rate”).
      - Set tax.included\_in\_print\_rate from 0.
      - Set tax\_updated from true.
  - If tax\_updated.
    - Evaluate Platform.msgprint(translated “Disabled tax included prices since this {} is an internal transfer”.format(self.doctype), alert = 1).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is internal transfer](operations-006.md#op-13fa6c1b2d5ba8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L909) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L149)

<a id="op-05814f565ba4a6"></a>
### Accounts Controller.validate due date

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_validate_due_date`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If (self.get(“is\_pos”) or self.doctype does not belong to list(“Sales Invoice”, “Purchase Invoice”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_pos”) → self.doctype does not belong to list(“Sales Invoice”, “Purchase Invoice”).
  - Return no value.
- Bind dependencies validate\_due\_date.
- Set posting\_date from self.posting\_date when self.doctype equals “Sales Invoice”, otherwise (self.bill\_date or self.posting\_date).
  - Value choice on self.doctype equals “Sales Invoice” — true gives self.posting\_date, false gives (self.bill\_date or self.posting\_date).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.bill\_date → self.posting\_date.
- If (Platform.flags.in\_import and getdate(self.due\_date) &lt; getdate(posting\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.flags.in\_import → getdate(self.due\_date) &lt; getdate(posting\_date).
  - Set self.due\_date from posting\_date.
- Otherwise.
  - If self.doctype belongs to list(“Sales Invoice”, “Purchase Invoice”).
    - Set bill\_date from self.bill\_date when self.doctype equals “Purchase Invoice”, otherwise no value.
      - Value choice on self.doctype equals “Purchase Invoice” — true gives self.bill\_date, false gives no value.
    - Evaluate validate\_due\_date(posting\_date = posting\_date, due\_date = self.due\_date, bill\_date = bill\_date, template\_name = self.payment\_terms\_template, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0367.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L667) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L371)

<a id="op-d649e39f12e30f"></a>
### Accounts Controller.set price list currency

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_price_list_currency`

**Inputs** self, buying\_or\_selling.

**Record and data access** read “Price List” via get\_value.

**Local steps**

- If self.meta.get\_field(“posting\_date”).
  - Set transaction\_date from self.posting\_date.
- Otherwise.
  - Set transaction\_date from self.transaction\_date.
- If self.meta.get\_field(“currency”).
  - If buying\_or\_selling.lower() equals “selling”.
    - Set fieldname from “selling\_price\_list”.
    - Set args from “for\_selling”.
  - Otherwise.
    - Set fieldname from “buying\_price\_list”.
    - Set args from “for\_buying”.
  - If (self.meta.get\_field(fieldname) and self.get(fieldname)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.meta.get\_field(fieldname) → self.get(fieldname).
    - Set previous\_price\_list\_currency from self.price\_list\_currency.
    - Set self.price\_list\_currency from Platform.db.get\_value(“Price List”, self.get(fieldname), “currency”).
    - If self.price\_list\_currency equals self.company\_currency.
      - Set self.plc\_conversion\_rate from 1.0.
    - Otherwise.
      - If (not self.plc\_conversion\_rate or (previous\_price\_list\_currency and previous\_price\_list\_currency differs from self.price\_list\_currency)).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.plc\_conversion\_rate → (previous\_price\_list\_currency and previous\_price\_list\_currency differs from self.price\_list\_currency).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_price\_list\_currency → previous\_price\_list\_currency differs from self.price\_list\_currency.
        - Set self.plc\_conversion\_rate from get\_exchange\_rate(self.price\_list\_currency, self.company\_currency, transaction\_date, args).
  - If not self.currency.
    - Set self.currency from self.price\_list\_currency.
    - Set self.conversion\_rate from self.plc\_conversion\_rate.
  - Otherwise.
    - If self.currency equals self.company\_currency.
      - Set self.conversion\_rate from 1.0.
    - Otherwise.
      - If not self.conversion\_rate.
        - Set self.conversion\_rate from get\_exchange\_rate(self.currency, self.company\_currency, transaction\_date, args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L652) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L356)

<a id="op-34d5d6710586cf"></a>
### Accounts Controller.on recurring

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_on_recurring`

**Inputs** self, reference\_doc, auto\_repeat\_doc.

**Local steps**

- Evaluate self.refresh\_exchange\_rates().

If control reaches the end, it returns no value.

**Methods declared on this owner** [refresh exchange rates](operations-003.md#op-64c5de21b982bd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L940) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L180)

<a id="op-64c5de21b982bd"></a>
### Accounts Controller.refresh exchange rates

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_refresh_exchange_rates`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot create recurring document: no exchange rate found for {0} to {1} on {2}. Please create a Currency Exc …”.format(currency, self.company\_currency, transaction\_date).

**Local steps**

- If not self.meta.get\_field(“conversion\_rate”).
  - Return no value.
- Set transaction\_date from (self.get(“posting\_date”) or self.get(“transaction\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“posting\_date”) → self.get(“transaction\_date”).
- Set args from “for\_buying” when self.meta.get\_field(“buying\_price\_list”), otherwise “for\_selling”.
  - Value choice on self.meta.get\_field(“buying\_price\_list”) — true gives “for\_buying”, false gives “for\_selling”.
- For each tuple(currency\_field, rate\_field) in tuple(tuple(“currency”, “conversion\_rate”), tuple(“price\_list\_currency”, “plc\_conversion\_rate”)).
  - Set currency from self.get(currency\_field).
  - If (not currency or currency equals self.company\_currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not currency → currency equals self.company\_currency.
    - Continue with the next iteration or loop test.
  - Set exchange\_rate from get\_exchange\_rate(currency, self.company\_currency, transaction\_date, args).
  - If not exchange\_rate.
    - Call the validation error handler Platform.throw(translated “Cannot create recurring document: no exchange rate found for {0} to {1} on {2}. Please create a Currency Exc …”.format(currency, self.company\_currency, transaction\_date), title = ….
  - Evaluate self.set(rate\_field, exchange\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L41) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L941) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L181)

<a id="op-6689ce50209c18"></a>
### Accounts Controller.set missing item details

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_missing_item_details`

**Inputs** self, for\_validate = false.

**Record and data access** read “Pricing Rule” via get\_cached\_value.

**Local steps**

- Bind dependencies get\_serial\_nos.
- If hasattr(self, “items”).
  - Set parent\_dict from mapping().
  - For each fieldname in self.meta.get\_valid\_columns().
    - Set parent\_dict at fieldname from self.get(fieldname).
  - If self.doctype belongs to list(“Quotation”, “Sales Order”, “Delivery Note”, “Sales Invoice”).
    - Set document\_type from formatted text {self.doctype} Item.
    - Evaluate parent\_dict.update(mapping(“document\_type” → document\_type)).
  - If (self.doctype equals “Quotation” and self.quotation\_to equals “Customer” and parent\_dict.get(“party\_name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Quotation” → self.quotation\_to equals “Customer” → parent\_dict.get(“party\_name”).
    - Evaluate parent\_dict.update(mapping(“customer” → parent\_dict.get(“party\_name”))).
  - Set self.pricing\_rules from list().
  - Set removed\_pricing\_rules from set().
  - For each item in self.get(“items”).
    - If item.get(“item\_code”).
      - Set ctx from ItemDetailsCtx(parent\_dict.copy()).
      - Evaluate ctx.update(item.as\_dict()).
      - Evaluate ctx.update(mapping(“doctype” → self.doctype, “name” → self.name, “child\_doctype” → item.doctype, “child\_docname” → item.name, …)).
        - Value choice on hasattr(self, “ignore\_pricing\_rule”) — true gives self.ignore\_pricing\_rule, false gives 0.
      - If not ctx.transaction\_date.
        - Set ctx.transaction\_date from ctx.posting\_date.
      - If self.get(“is\_subcontracted”).
        - Set ctx.is\_subcontracted from self.is\_subcontracted.
      - Set ret from \_get\_item\_details(ctx, self, for\_validate = for\_validate, overwrite\_warehouse = false).
      - If ret.get(“pricing\_rule\_removed”).
        - Evaluate removed\_pricing\_rules.update((set(get\_applied\_pricing\_rules(ctx.get(“pricing\_rules”))) − set(get\_applied\_pricing\_rules(ret.get(“pricing\_rules”))))).
      - For each tuple(fieldname, value) in ret.items().
        - If (item.meta.get\_field(fieldname) and value is distinct from no value).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.meta.get\_field(fieldname) → value is distinct from no value.
          - If (item.get(fieldname) is identical to no value or fieldname belongs to force\_item\_fields or (fieldname belongs to list(“serial\_no”, “batch\_no”) and item.get(“use\_serial\_batch\_fields”))).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(fieldname) is identical to no value → fieldname belongs to force\_item\_fields → (fieldname belongs to list(“serial\_no”, “batch\_no”) and item.get(“use\_serial\_batch\_fields”)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname belongs to list(“serial\_no”, “batch\_no”) → item.get(“use\_serial\_batch\_fields”).
            - Evaluate item.set(fieldname, value).
            - If (fieldname equals “batch\_no” and item.batch\_no and not item.is\_free\_item).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname equals “batch\_no” → item.batch\_no → not item.is\_free\_item.
              - If ret.get(“rate”).
                - Evaluate item.set(“rate”, ret.get(“rate”)).
              - If (not item.get(“price\_list\_rate”) and ret.get(“price\_list\_rate”)).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“price\_list\_rate”) → ret.get(“price\_list\_rate”).
                - Evaluate item.set(“price\_list\_rate”, ret.get(“price\_list\_rate”)).
          - Otherwise.
            - If (fieldname belongs to list(“cost\_center”, “conversion\_factor”) and not item.get(fieldname)).
              - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname belongs to list(“cost\_center”, “conversion\_factor”) → not item.get(fieldname).
              - Evaluate item.set(fieldname, value).
            - Otherwise.
              - If (fieldname equals “item\_tax\_rate” and not (self.get(“is\_return”) and self.get(“return\_against”))).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname equals “item\_tax\_rate” → not (self.get(“is\_return”) and self.get(“return\_against”)).
                - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“is\_return”) → self.get(“return\_against”).
                - Evaluate item.set(fieldname, value).
              - Otherwise.
                - If fieldname equals “serial\_no”.
                  - Set item\_conversion\_factor from (item.get(“conversion\_factor”) or 1.0).
                    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.get(“conversion\_factor”) → 1.0.
                  - Set item\_qty from (abs(item.get(“qty”)) × item\_conversion\_factor).
                  - If item\_qty differs from len(get\_serial\_nos(item.get(“serial\_no”))).
                    - Evaluate item.set(fieldname, value).
                - Otherwise.
                  - If (ret.get(“pricing\_rule\_removed”) and value is distinct from no value and fieldname belongs to list(“price\_list\_rate”, “discount\_percentage”, “discount\_amount”, “rate”, …)).
                    - Evaluate in order, stop at the first false operand, otherwise use the last operand in ret.get(“pricing\_rule\_removed”) → value is distinct from no value → fieldname belongs to list(“price\_list\_rate”, “discount\_percentage”, “discount\_amount”, “rate”, …).
                    - Evaluate item.set(fieldname, value).
                  - Otherwise.
                    - If (fieldname equals “expense\_account” and not item.get(“expense\_account”)).
                      - Evaluate in order, stop at the first false operand, otherwise use the last operand in fieldname equals “expense\_account” → not item.get(“expense\_account”).
                      - Set item.expense\_account from value.
      - If (self.doctype belongs to list(“Purchase Invoice”, “Sales Invoice”) and item.meta.get\_field(“is\_fixed\_asset”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Invoice”, “Sales Invoice”) → item.meta.get\_field(“is\_fixed\_asset”).
        - Evaluate item.set(“is\_fixed\_asset”, ret.get(“is\_fixed\_asset”, 0)).
      - If (self.doctype belongs to list(“Purchase Invoice”, “Sales Invoice”) and item.meta.get\_field(“tax\_withholding\_category”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype belongs to list(“Purchase Invoice”, “Sales Invoice”) → item.meta.get\_field(“tax\_withholding\_category”).
        - If (not item.get(“tax\_withholding\_category”) and ret.get(“tax\_withholding\_category”)).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.get(“tax\_withholding\_category”) → ret.get(“tax\_withholding\_category”).
          - Evaluate item.set(“tax\_withholding\_category”, ret.get(“tax\_withholding\_category”)).
      - If (hasattr(item, “cost\_center”) and not item.get(“cost\_center”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(item, “cost\_center”) → not item.get(“cost\_center”).
        - Evaluate item.set(“cost\_center”, (self.get(“cost\_center”) or Enterprise.get\_default\_cost\_center(self.company))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“cost\_center”) → Enterprise.get\_default\_cost\_center(self.company).
      - If ret.get(“pricing\_rules”).
        - Evaluate self.apply\_pricing\_rule\_on\_items(item, ret).
        - Evaluate self.set\_pricing\_rule\_details(item, ret).
    - Otherwise.
      - Set uom from item.get(“uom”).
      - Set stock\_uom from item.get(“stock\_uom”).
      - If bool(uom) differs from bool(stock\_uom).
        - Set item.stock\_uom, item.uom from (uom or stock\_uom).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in uom → stock\_uom.
      - Set item.conversion\_factor from (get\_uom\_conv\_factor(item.get(“uom”), item.get(“stock\_uom”)) or item.get(“conversion\_factor”) or 1).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_uom\_conv\_factor(item.get(“uom”), item.get(“stock\_uom”)) → item.get(“conversion\_factor”) → 1.
  - If removed\_pricing\_rules.
    - Evaluate removed\_pricing\_rules.difference\_update(generator of row.pricing\_rule for row drawn from self.pricing\_rules).
      - Draw row from self.pricing\_rules.
    - For each item in self.items at slice no value to no value.
      - If (item.get(“is\_free\_item”) and item.get(“pricing\_rules”) belongs to removed\_pricing\_rules and not Platform.get\_cached\_value(“Pricing Rule”, item.pricing\_rules, “dont\_enforce\_free\_item\_qty”)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“is\_free\_item”) → item.get(“pricing\_rules”) belongs to removed\_pricing\_rules → not Platform.get\_cached\_value(“Pricing Rule”, item.pricing\_rules, “dont\_enforce\_free\_item\_qty”).
        - Evaluate self.remove(item).
  - If self.doctype equals “Purchase Invoice”.
    - Evaluate self.set\_expense\_account(for\_validate).

If control reaches the end, it returns no value.

**Methods declared on this owner** [apply pricing rule on items](operations-003.md#op-fcf87894c2a795), [set pricing rule details](operations-003.md#op-84dbb15c76e435).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Pricing Rule”, item.pricing\_rules, “dont\_enforce\_free\_item\_qty”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L100) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L649) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L353)

<a id="op-fcf87894c2a795"></a>
### Accounts Controller.apply pricing rule on items

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_apply_pricing_rule_on_items`

**Inputs** self, item, pricing\_rule\_args.

**Record and data access** resolve a document from “Pricing Rule” via get\_cached\_doc.

**State and service calls** msgprint with translated “Row {0}: user has not applied the rule {1} on the item {2}”.format(item.idx, Platform.bold(title), Platform.bold(item.item\_code)).

**Explicit results** no value.

**Local steps**

- If not pricing\_rule\_args.get(“validate\_applied\_rule”, 0).
  - If pricing\_rule\_args.get(“price\_or\_product\_discount”) equals “Price”.
    - Evaluate item.set(“pricing\_rules”, pricing\_rule\_args.get(“pricing\_rules”)).
    - If pricing\_rule\_args.get(“apply\_rule\_on\_other\_items”).
      - Set other\_items from json.loads(pricing\_rule\_args.get(“apply\_rule\_on\_other\_items”)).
      - If (other\_items and item.item\_code does not belong to other\_items).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in other\_items → item.item\_code does not belong to other\_items.
        - Return no value.
    - Evaluate item.set(“discount\_percentage”, pricing\_rule\_args.get(“discount\_percentage”)).
    - Evaluate item.set(“discount\_amount”, pricing\_rule\_args.get(“discount\_amount”)).
    - If (pricing\_rule\_args.get(“has\_pricing\_rule\_for\_rate”) or pricing\_rule\_args.get(“pricing\_rule\_for”) equals “Rate”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in pricing\_rule\_args.get(“has\_pricing\_rule\_for\_rate”) → pricing\_rule\_args.get(“pricing\_rule\_for”) equals “Rate”.
      - Evaluate item.set(“price\_list\_rate”, pricing\_rule\_args.get(“price\_list\_rate”)).
    - If item.get(“price\_list\_rate”).
      - Set item.rate from flt((item.price\_list\_rate × (1.0 − (flt(item.discount\_percentage) ÷ 100.0))), item.precision(“rate”)).
      - If item.get(“discount\_amount”).
        - Set item.rate from (item.price\_list\_rate − item.discount\_amount).
    - If (item.get(“apply\_discount\_on\_discounted\_rate”) and pricing\_rule\_args.get(“rate”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“apply\_discount\_on\_discounted\_rate”) → pricing\_rule\_args.get(“rate”).
      - Set item.rate from pricing\_rule\_args.get(“rate”).
  - Otherwise.
    - If pricing\_rule\_args.get(“free\_item\_data”).
      - Evaluate apply\_pricing\_rule\_for\_free\_items(self, pricing\_rule\_args.get(“free\_item\_data”)).
- Otherwise.
  - If pricing\_rule\_args.get(“validate\_applied\_rule”).
    - For each pricing\_rule in get\_applied\_pricing\_rules(item.get(“pricing\_rules”)).
      - Set pricing\_rule\_doc from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rule).
      - For each field in list(“discount\_percentage”, “discount\_amount”, “rate”).
        - If item.get(field) &lt; pricing\_rule\_doc.get(field).
          - Set title from get\_link\_to\_form(“Pricing Rule”, pricing\_rule).
          - Evaluate Platform.msgprint(translated “Row {0}: user has not applied the rule {1} on the item {2}”.format(item.idx, Platform.bold(title), Platform.bold(item.item\_code))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Pricing Rule”, pricing\_rule).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L75) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L591) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L296)

<a id="op-84dbb15c76e435"></a>
### Accounts Controller.set pricing rule details

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_set_pricing_rule_details`

**Inputs** self, item\_row, args.

**Explicit results** no value.

**Local steps**

- Set pricing\_rules from get\_applied\_pricing\_rules(args.get(“pricing\_rules”)).
- If not pricing\_rules.
  - Return no value.
- For each pricing\_rule in pricing\_rules.
  - Evaluate self.append(“pricing\_rules”, mapping(“pricing\_rule” → pricing\_rule, “item\_code” → item\_row.item\_code, “child\_docname” → item\_row.name, “rule\_applied” → true)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0367.json#L5387) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L653) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L357)

<a id="op-91d4f460887993"></a>
### Accounts Controller.set taxes

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_taxes`

**Inputs** self.

**Record and data access** read tax\_master\_doctype via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.meta.get\_field(“taxes”).
  - Return no value.
- Set tax\_master\_doctype from self.meta.get\_field(“taxes\_and\_charges”).options.
- If ((self.is\_new() or self.is\_pos\_profile\_changed()) and not self.get(“taxes”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in (self.is\_new() or self.is\_pos\_profile\_changed()) → not self.get(“taxes”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.is\_pos\_profile\_changed().
  - If (self.company and not self.get(“taxes\_and\_charges”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company → not self.get(“taxes\_and\_charges”).
    - Set self.taxes\_and\_charges from Platform.db.get\_value(tax\_master\_doctype, mapping(“is\_default” → 1, “company” → self.company)).
  - Evaluate self.append\_taxes\_from\_master(tax\_master\_doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [is pos profile changed](operations-003.md#op-6c3b2642e3e3fa), [append taxes from master](operations-003.md#op-27e22c44837cb7).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L47) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L947) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L187)

<a id="op-6c3b2642e3e3fa"></a>
### Accounts Controller.is pos profile changed

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_is_pos_profile_changed`

**Inputs** self.

**Record and data access** read “Sales Invoice” via get\_value.

**Explicit results** true.

**Local steps**

- If (self.doctype equals “Sales Invoice” and self.is\_pos and self.pos\_profile differs from Platform.db.get\_value(“Sales Invoice”, self.name, “pos\_profile”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_pos → self.pos\_profile differs from Platform.db.get\_value(“Sales Invoice”, self.name, “pos\_profile”).
  - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L929) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L169)

<a id="op-810c32f9d25d61"></a>
### Accounts Controller.set taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_taxes_and_charges`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If self.doctype equals “Material Request”.
  - Return no value.
- If (self.get(“taxes”) or self.get(“is\_pos”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“taxes”) → self.get(“is\_pos”).
  - Return no value.
- If self.flags.dont\_auto\_add\_taxes.
  - Return no value.
- If (Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_taxes\_and\_charges\_template”) and hasattr(self, “taxes\_and\_charges”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_taxes\_and\_charges\_template”) → hasattr(self, “taxes\_and\_charges”).
  - If tax\_master\_doctype bound to self.meta.get\_field(“taxes\_and\_charges”).options.
    - Evaluate self.append\_taxes\_from\_master(tax\_master\_doctype).
- If Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).
  - Evaluate self.append\_taxes\_from\_item\_tax\_template().

If control reaches the end, it returns no value.

**Methods declared on this owner** [append taxes from master](operations-003.md#op-27e22c44837cb7), [append taxes from item tax template](operations-003.md#op-6902c038f7eea1).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_taxes\_and\_charges\_template”), Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L48) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L948) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L188)

<a id="op-27e22c44837cb7"></a>
### Accounts Controller.append taxes from master

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_append_taxes_from_master`

**Inputs** self, tax\_master\_doctype = no value.

**Local steps**

- If self.get(“taxes\_and\_charges”).
  - If not tax\_master\_doctype.
    - Set tax\_master\_doctype from self.meta.get\_field(“taxes\_and\_charges”).options.
  - Evaluate self.extend(“taxes”, \_get\_taxes\_and\_charges(tax\_master\_doctype, self.get(“taxes\_and\_charges”))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L3) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L903) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L143)

<a id="op-6902c038f7eea1"></a>
### Accounts Controller.append taxes from item tax template

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_append_taxes_from_item_tax_template`

**Inputs** self.

**Record and data access** read “Accounts Settings” via get\_single\_value.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).
  - Return no value.
- For each row in self.items.
  - Set item\_tax\_rate from row.get(“item\_tax\_rate”).
  - If not item\_tax\_rate.
    - Continue with the next iteration or loop test.
  - If isinstance(item\_tax\_rate, str).
    - Set item\_tax\_rate from parse\_json(item\_tax\_rate).
  - For each tuple(account\_head, \_rate) in item\_tax\_rate.items().
    - Set row from self.get\_tax\_row(account\_head).
    - If not row.
      - Evaluate self.append(“taxes”, mapping(“charge\_type” → “On Net Total”, “account\_head” → account\_head, “rate” → 0, “description” → account\_head, …)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get tax row](operations-003.md#op-a4262a39574722).

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “add\_taxes\_from\_item\_tax\_template”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L902) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L142)

<a id="op-a4262a39574722"></a>
### Accounts Controller.get tax row

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_get_tax_row`

**Inputs** self, account\_head.

**Explicit results** row.

**Local steps**

- For each row in self.taxes.
  - If row.account\_head equals account\_head.
    - Return row.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L923) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L163)

<a id="op-b71432a26122d7"></a>
### Accounts Controller.set other charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_set_other_charges`

**Inputs** self.

**Local steps**

- Evaluate self.set(“taxes”, list()).
- Evaluate self.set\_taxes().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set taxes](operations-003.md#op-91d4f460887993).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L45) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L945) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L185)

<a id="op-e552f0ca97555f"></a>
### Accounts Controller.validate enabled taxes and charges

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_enabled_taxes_and_charges`

**Inputs** self.

**Record and data access** read taxes\_and\_charges\_doctype via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} '{1}' is disabled”.format(taxes\_and\_charges\_doctype, self.taxes\_and\_charges).

**Local steps**

- Set taxes\_and\_charges\_doctype from self.meta.get\_options(“taxes\_and\_charges”).
- If (self.taxes\_and\_charges and Platform.get\_cached\_value(taxes\_and\_charges\_doctype, self.taxes\_and\_charges, “disabled”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.taxes\_and\_charges → Platform.get\_cached\_value(taxes\_and\_charges\_doctype, self.taxes\_and\_charges, “disabled”).
  - Call the validation error handler Platform.throw(translated “{0} '{1}' is disabled”.format(taxes\_and\_charges\_doctype, self.taxes\_and\_charges)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(taxes\_and\_charges\_doctype, self.taxes\_and\_charges, “disabled”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L960) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L200)

<a id="op-03eae2138a1719"></a>
### Accounts Controller.validate tax account company

`operation_enterprise_binding_enterprise_controllers_accounts_controller_accountscontroller_validate_tax_account_company`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Row #{0}: Account {1} does not belong to company {2}”.format(d.idx, d.account\_head, self.company).

**Local steps**

- For each d in self.get(“taxes”).
  - If d.account\_head.
    - Set tax\_account\_company from Platform.get\_cached\_value(“Account”, d.account\_head, “company”).
    - If tax\_account\_company differs from self.company.
      - Call the validation error handler Platform.throw(translated “Row #{0}: Account {1} does not belong to company {2}”.format(d.idx, d.account\_head, self.company)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, d.account\_head, “company”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0013.json#L78) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L978) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L218)

<a id="op-9b830044032472"></a>
### Accounts Controller.get gl dict

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_general_ledger_mapping`

**Inputs** self, args, account\_currency = no value, item = no value.

**Explicit results** gl\_dict.

**Explicit failure paths** validation helper — translated “Multiple fiscal years exist for the date {0}. Please set company in Fiscal Year”.format(formatdate(posting\_date)).

**Local steps**

- Set posting\_date from (args.get(“posting\_date”) or self.get(“posting\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“posting\_date”) → self.get(“posting\_date”).
- Set fiscal\_years from get\_fiscal\_years(posting\_date, company = self.company).
- If len(fiscal\_years) &gt; 1.
  - Call the validation error handler Platform.throw(translated “Multiple fiscal years exist for the date {0}. Please set company in Fiscal Year”.format(formatdate(posting\_date))).
- Otherwise.
  - Set fiscal\_year from fiscal\_years at 0 at 0.
- Set gl\_dict from Platform.\_dict(mapping(“company” → self.company, “posting\_date” → posting\_date, “fiscal\_year” → fiscal\_year, “voucher\_type” → self.doctype, …)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“remarks”) → self.get(“remark”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“is\_opening”) → “No”.
- Within temporary\_flag(“company”, self.company).
  - Evaluate update\_gl\_dict\_with\_regional\_fields(self, gl\_dict).
- Evaluate update\_gl\_dict\_with\_app\_based\_fields(self, gl\_dict).
- Set accounting\_dimensions from get\_accounting\_dimensions().
- Set dimension\_dict from Platform.\_dict().
- For each dimension in accounting\_dimensions.
  - Set value from self.get(dimension).
  - If (item and item.get(dimension)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item → item.get(dimension).
    - Set value from item.get(dimension).
  - If isinstance(value, (list bitwise or dict)).
    - Continue with the next iteration or loop test.
  - Set dimension\_dict at dimension from value.
- Evaluate gl\_dict.update(dimension\_dict).
- Evaluate gl\_dict.update(args).
- If not account\_currency.
  - Set account\_currency from get\_account\_currency(gl\_dict.account).
- If (gl\_dict.account and self.doctype does not belong to list(“Journal Entry”, “Period Closing Voucher”, “Payment Entry”, “Purchase Receipt”, …)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_dict.account → self.doctype does not belong to list(“Journal Entry”, “Period Closing Voucher”, “Payment Entry”, “Purchase Receipt”, …).
  - Evaluate self.validate\_account\_currency(gl\_dict.account, account\_currency).
- If (gl\_dict.account and self.doctype does not belong to list(“Journal Entry”, “Period Closing Voucher”, “Payment Entry”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in gl\_dict.account → self.doctype does not belong to list(“Journal Entry”, “Period Closing Voucher”, “Payment Entry”).
  - Evaluate set\_balance\_in\_account\_currency(gl\_dict, account\_currency, (args.get(“transaction\_exchange\_rate”) or self.get(“conversion\_rate”)), self.company\_currency).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“transaction\_exchange\_rate”) → self.get(“conversion\_rate”).
- If self.doctype does not belong to list(“Purchase Invoice”, “Sales Invoice”, “Journal Entry”, “Payment Entry”).
  - Evaluate gl\_dict.update(mapping(“transaction\_currency” → (self.get(“currency”) or self.company\_currency), “transaction\_exchange\_rate” → (args.get(“transaction\_exchange\_rate”) or self.get(“conversion\_rate”, 1)), “de ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(“currency”) → self.company\_currency.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“transaction\_exchange\_rate”) → self.get(“conversion\_rate”, 1).
- If (not args.get(“against\_voucher\_type”) and self.get(“against\_voucher\_type”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args.get(“against\_voucher\_type”) → self.get(“against\_voucher\_type”).
  - Evaluate gl\_dict.update(mapping(“against\_voucher\_type” → self.get(“against\_voucher\_type”))).
- If (not args.get(“against\_voucher”) and self.get(“against\_voucher”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args.get(“against\_voucher”) → self.get(“against\_voucher”).
  - Evaluate gl\_dict.update(mapping(“against\_voucher” → self.get(“against\_voucher”))).
- Return gl\_dict.

**Methods declared on this owner** [get voucher subtype](operations-003.md#op-5b54dc329e98ca), [validate account currency](operations-004.md#op-c152ca887cf87b), [get value in transaction currency](operations-003.md#op-0d008f0bec1b1b).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L321)

<a id="op-5b54dc329e98ca"></a>
### Accounts Controller.get voucher subtype

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_voucher_subtype`

**Inputs** self.

**Explicit results** voucher\_subtype · self.get(voucher\_subtypes at self.doctype) · “Purchase Return” · “Sales Return” · “Credit Note” · 2 additional forms in the steps below.

**Local steps**

- Set voucher\_subtypes from mapping(“Journal Entry” → “voucher\_type”, “Payment Entry” → “payment\_type”, “Stock Entry” → “stock\_entry\_type”, “Asset Capitalization” → “entry\_type”).
- For each method\_name in Platform.get\_hooks(“voucher\_subtypes”).
  - Set voucher\_subtype from Platform.get\_attr(method\_name)(self).
  - If voucher\_subtype.
    - Return voucher\_subtype.
- If self.doctype belongs to voucher\_subtypes.
  - Return self.get(voucher\_subtypes at self.doctype).
- Otherwise.
  - If (self.doctype equals “Purchase Receipt” and self.is\_return).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Receipt” → self.is\_return.
    - Return “Purchase Return”.
  - Otherwise.
    - If (self.doctype equals “Delivery Note” and self.is\_return).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Delivery Note” → self.is\_return.
      - Return “Sales Return”.
    - Otherwise.
      - If (self.doctype equals “Sales Invoice” and self.is\_return).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_return.
        - Return “Credit Note”.
      - Otherwise.
        - If (self.doctype equals “Sales Invoice” and self.is\_debit\_note).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Sales Invoice” → self.is\_debit\_note.
          - Return “Debit Note”.
        - Otherwise.
          - If (self.doctype equals “Purchase Invoice” and self.is\_return).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.doctype equals “Purchase Invoice” → self.is\_return.
            - Return “Debit Note”.
- Return self.doctype.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“voucher\_subtypes”), Platform.get\_attr(method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L622) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L327)

<a id="op-0d008f0bec1b1b"></a>
### Accounts Controller.get value in transaction currency

`operation_enterprise_controllers_accounts_controller_business_behavior_accounts_controller_get_value_in_transaction_currency`

**Inputs** self, account\_currency, gl\_dict, field.

**Explicit results** gl\_dict.get((field + “\_in\_account\_currency”)) · flt((gl\_dict.get(field, 0) ÷ self.get(“conversion\_rate”, 1))).

**Local steps**

- If account\_currency equals self.get(“currency”).
  - Return gl\_dict.get((field + “\_in\_account\_currency”)).
- Otherwise.
  - Return flt((gl\_dict.get(field, 0) ÷ self.get(“conversion\_rate”, 1))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L621) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L326)
