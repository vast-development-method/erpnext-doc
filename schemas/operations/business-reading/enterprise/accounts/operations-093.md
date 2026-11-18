# Accounting and settlement · operations 93

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Purchase invoice

[Record definition](../../../../data/record-types/purchase_invoice.json)

<a id="op-7bcccd1a45c166"></a>
### Purchase Invoice.set missing values

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_set_missing_values`

**Inputs** self, for\_validate = false.

**Record and data access** read “Account” via get\_cached\_value · read “Supplier” via get\_cached\_value.

**Local steps**

- If not self.credit\_to.
  - Set self.credit\_to from get\_party\_account(“Supplier”, self.supplier, self.company).
  - Set self.party\_account\_currency from Platform.get\_cached\_value(“Account”, self.credit\_to, “account\_currency”).
- If not self.due\_date.
  - Set self.due\_date from get\_due\_date(self.posting\_date, “Supplier”, self.supplier, self.company, template\_name = self.payment\_terms\_template, …).
- If self.supplier.
  - Set tuple(tax\_withholding\_category, tax\_withholding\_group) from Platform.get\_cached\_value(“Supplier”, self.supplier, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).
  - If not for\_validate.
    - If (tax\_withholding\_category or tax\_withholding\_group).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in tax\_withholding\_category → tax\_withholding\_group.
      - Set self.apply\_tds from 1.
- Evaluate super().set\_missing\_values(for\_validate).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.credit\_to, “account\_currency”), Platform.get\_cached\_value(“Supplier”, self.supplier, list(“tax\_withholding\_category”, “tax\_withholding\_group”)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L1773) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L764) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L936)

<a id="op-22905084f07d52"></a>
### Purchase Invoice.validate credit to acc

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_credit_to_accounting`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “Please ensure that the {0} account is a Balance Sheet account. You can change the parent account to a Balanc …”.format(Platform.bold(translated “Credit To”)) · validation helper — translated “Please ensure that the {0} account {1} is a Payable account. You can change the account type to Payable or s …”.format(Platform.bold(translated “Credit To”), Platform.bold(self.credit\_to)).

**Local steps**

- If not self.credit\_to.
  - Set self.credit\_to from get\_party\_account(“Supplier”, self.supplier, self.company).
  - If not self.credit\_to.
    - Evaluate self.raise\_missing\_debit\_credit\_account\_error(“Supplier”, self.supplier).
- Set account from Platform.get\_cached\_value(“Account”, self.credit\_to, list(“account\_type”, “report\_type”, “account\_currency”), as\_dict = true).
- If account.report\_type differs from “Balance Sheet”.
  - Call the validation error handler Platform.throw(translated “Please ensure that the {0} account is a Balance Sheet account. You can change the parent account to a Balanc …”.format(Platform.bold(translated “Credit To”)), title = translated  ….
- If (self.supplier and account.account\_type differs from “Payable”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.supplier → account.account\_type differs from “Payable”.
  - Call the validation error handler Platform.throw(translated “Please ensure that the {0} account {1} is a Payable account. You can change the account type to Payable or s …”.format(Platform.bold(translated “Credit To”), Platform.bold(self.c ….
- Set self.party\_account\_currency from account.account\_currency.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.credit\_to, list(“account\_type”, “report\_type”, “account\_currency”), as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L2210) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L774) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L946)

<a id="op-2a24938920a49e"></a>
### Purchase Invoice.validate with previous doc

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_with_previous_record`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value.

**Local steps**

- Evaluate super().validate\_with\_previous\_doc(mapping(“Purchase Order” → mapping(“ref\_dn\_field” → “purchase\_order”, “compare\_fields” → list(list(“supplier”, “=”), list(“company”, “=”), list(“currency”, “=”))), “Purch ….
- If (cint(Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”)) and not self.is\_return and not self.is\_internal\_supplier).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”)) → not self.is\_return → not self.is\_internal\_supplier.
  - Evaluate self.validate\_rate\_with\_reference\_doc(list(list(“Purchase Order”, “purchase\_order”, “po\_detail”), list(“Purchase Receipt”, “purchase\_receipt”, “pr\_detail”))).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “maintain\_same\_rate”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L2778) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L783) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L955)

<a id="op-b44eff2cbb9340"></a>
### Purchase Invoice.validate warehouse

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_warehouse`

**Inputs** self, for\_validate = true.

**Explicit failure paths** validation helper with WarehouseMissingError — translated “Row No {0}: Warehouse is required. Please set a Default Warehouse for Item {1} and Company {2}”.format(d.idx, d.item\_code, self.company).

**Local steps**

- If (self.update\_stock and for\_validate).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.update\_stock → for\_validate.
  - Set stock\_items from self.get\_stock\_items().
  - For each d in self.get(“items”).
    - If (not d.warehouse and d.item\_code belongs to stock\_items).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.warehouse → d.item\_code belongs to stock\_items.
      - Call the validation error handler Platform.throw(translated “Row No {0}: Warehouse is required. Please set a Default Warehouse for Item {1} and Company {2}”.format(d.idx, d.item\_code, self.company), exc = WarehouseMissingError).
- Evaluate super().validate\_warehouse().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L3456) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L782) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L954)

<a id="op-57053960fd57ba"></a>
### Purchase Invoice.validate item code

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_item_code`

**Inputs** self.

**State and service calls** msgprint with translated “Item Code required at Row No {0}”.format(d.idx).

**Local steps**

- For each d in self.get(“items”).
  - If not d.item\_code.
    - Evaluate Platform.msgprint(translated “Item Code required at Row No {0}”.format(d.idx), raise\_exception = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L3740) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L778) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L950)

<a id="op-f2164f97ab5a2d"></a>
### Purchase Invoice.set expense account

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_set_expense_account`

**Inputs** self, for\_validate = false.

**Record and data access** read “Purchase Order Item” via get\_value · execute query text (SELECT, GL Entry) · read “Purchase Receipt Item” via get\_cached\_value · read “GL Entry” via get\_value.

**State and service calls** msgprint with msg.

**Local steps**

- Set auto\_accounting\_for\_stock from Enterprise.is\_perpetual\_inventory\_enabled(self.company).
- If auto\_accounting\_for\_stock.
  - Set stock\_not\_billed\_account from self.get\_company\_default(“stock\_received\_but\_not\_billed”).
  - Set stock\_items from self.get\_stock\_items().
- Set self.asset\_received\_but\_not\_billed from no value.
- Set inventory\_account\_map from mapping().
- If self.update\_stock.
  - Evaluate self.validate\_item\_code().
  - Evaluate self.validate\_warehouse(for\_validate).
  - If auto\_accounting\_for\_stock.
    - Set inventory\_account\_map from self.get\_inventory\_account\_map().
- For each item in self.get(“items”).
  - If (auto\_accounting\_for\_stock and item.item\_code belongs to stock\_items and self.is\_opening equals “No” and not item.is\_fixed\_asset and (not item.po\_detail or not Platform.db.get\_value(“Purchase Order Item”,  ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in auto\_accounting\_for\_stock → item.item\_code belongs to stock\_items → self.is\_opening equals “No” → not item.is\_fixed\_asset → (not item.po\_detail or not Platform.db.get\_value(“Purchase Order Item”, item.po\_detail, “delivered\_by\_supplier”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not item.po\_detail → not Platform.db.get\_value(“Purchase Order Item”, item.po\_detail, “delivered\_by\_supplier”).
    - If (self.update\_stock and item.warehouse and not item.from\_warehouse).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.update\_stock → item.warehouse → not item.from\_warehouse.
      - Set \_inv\_dict from self.get\_inventory\_account\_dict(item, inventory\_account\_map).
      - If (for\_validate and item.expense\_account and item.expense\_account differs from \_inv\_dict at “account”).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → item.expense\_account → item.expense\_account differs from \_inv\_dict at “account”.
        - Set msg from translated “Row {0}: Expense Head changed to {1} because account {2} is not linked to warehouse {3} or it is not the def …”.format(item.idx, Platform.bold(\_inv\_dict at “account”), Platform.bold(item.expens ….
        - Evaluate Platform.msgprint(msg, title = translated “Expense Head Changed”).
      - Set item.expense\_account from \_inv\_dict at “account”.
    - Otherwise.
      - If item.purchase\_receipt.
        - Set negative\_expense\_booked\_in\_pr from Platform.db.sql(query text (SELECT, GL Entry), tuple(item.purchase\_receipt, stock\_not\_billed\_account)).
        - If negative\_expense\_booked\_in\_pr.
          - If (for\_validate and item.expense\_account and item.expense\_account differs from stock\_not\_billed\_account).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → item.expense\_account → item.expense\_account differs from stock\_not\_billed\_account.
            - Set msg from translated “Row {0}: Expense Head changed to {1} because expense is booked against this account in Purchase Receipt {2}”.format(item.idx, Platform.bold(stock\_not\_billed\_account), Platform.bold(item.purchas ….
            - Evaluate Platform.msgprint(msg, title = translated “Expense Head Changed”).
          - Set item.expense\_account from stock\_not\_billed\_account.
      - Otherwise.
        - If (for\_validate and item.expense\_account and item.expense\_account differs from stock\_not\_billed\_account).
          - Evaluate in order, stop at the first false operand, otherwise use the last operand in for\_validate → item.expense\_account → item.expense\_account differs from stock\_not\_billed\_account.
          - Set msg from translated “Row {0}: Expense Head changed to {1} as no Purchase Receipt is created against Item {2}.”.format(item.idx, Platform.bold(stock\_not\_billed\_account), Platform.bold(item.item\_code)).
          - Update msg using + text in the contract.
          - Update msg using + translated “This is done to handle accounting for cases when Purchase Receipt is created after Purchase Invoice”.
          - Evaluate Platform.msgprint(msg, title = translated “Expense Head Changed”).
        - Set item.expense\_account from stock\_not\_billed\_account.
  - Otherwise.
    - If item.is\_fixed\_asset.
      - Set account from no value.
      - If (not item.pr\_detail and item.po\_detail).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.pr\_detail → item.po\_detail.
        - Set receipt\_item from Platform.get\_cached\_value(“Purchase Receipt Item”, mapping(“purchase\_order” → item.purchase\_order, “purchase\_order\_item” → item.po\_detail, “docstatus” → 1), list(“name”, “parent”), as\_dict = 1).
        - If receipt\_item.
          - Set item.pr\_detail from receipt\_item.name.
          - Set item.purchase\_receipt from receipt\_item.parent.
      - If item.pr\_detail.
        - If not self.asset\_received\_but\_not\_billed.
          - Set self.asset\_received\_but\_not\_billed from self.get\_company\_default(“asset\_received\_but\_not\_billed”).
        - Set arbnb\_booked\_in\_pr from Platform.db.get\_value(“GL Entry”, mapping(“voucher\_type” → “Purchase Receipt”, “voucher\_no” → item.purchase\_receipt, “account” → self.asset\_received\_but\_not\_billed), “name”).
        - If arbnb\_booked\_in\_pr.
          - Set account from self.asset\_received\_but\_not\_billed.
      - If not account.
        - Set account\_type from “capital\_work\_in\_progress\_account” when is\_cwip\_accounting\_enabled(item.asset\_category), otherwise “fixed\_asset\_account”.
          - Value choice on is\_cwip\_accounting\_enabled(item.asset\_category) — true gives “capital\_work\_in\_progress\_account”, false gives “fixed\_asset\_account”.
        - Set account from get\_asset\_category\_account(account\_type, item = item.item\_code, company = self.company).
        - If not account.
          - Set form\_link from get\_link\_to\_form(“Asset Category”, item.asset\_category).
          - Evaluate throw(translated “Please set Fixed Asset Account in {} against {}.”.format(form\_link, self.company), title = translated “Missing Account”).
      - Set item.expense\_account from account.
    - Otherwise.
      - If (not item.expense\_account and for\_validate).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item.expense\_account → for\_validate.
        - Evaluate throw(translated “Expense account is mandatory for item {0}”.format((item.item\_code or item.item\_name))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.item\_code → item.item\_name.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate item code](operations-093.md#op-57053960fd57ba), [validate warehouse](operations-093.md#op-b44eff2cbb9340).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Purchase Receipt Item”, mapping(“purchase\_order” → item.purchase\_order, “purchase\_order\_item” → item.po\_detail, “docstatus” → 1), list(“name”, “parent”), as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L763) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L935)

<a id="op-65fff90cccc550"></a>
### Purchase Invoice.validate expense account

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_validate_expense_account`

**Inputs** self.

**Local steps**

- For each item in self.get(“items”).
  - Evaluate validate\_account\_head(item.idx, item.expense\_account, self.company, translated “Expense”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L60) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L331) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L969)

<a id="op-3a5032940eb443"></a>
### Purchase Invoice.set against expense account

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_set_against_expense_account`

**Inputs** self, force = false.

**Local steps**

- Set against\_accounts from list().
- For each item in self.get(“items”).
  - If (item.expense\_account and item.expense\_account does not belong to against\_accounts).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.expense\_account → item.expense\_account does not belong to against\_accounts.
    - Evaluate against\_accounts.append(item.expense\_account).
- Set self.against\_expense\_account from “,”.join(against\_accounts).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L327) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L965)

<a id="op-e4344fe1c9e1b7"></a>
### Purchase Invoice.force set against expense account

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_force_set_against_expense_account`

**Inputs** self.

**State and service calls** request set\_value on self.doctype.

**Local steps**

- Evaluate self.set\_against\_expense\_account().
- Evaluate Platform.db.set\_value(self.doctype, self.name, “against\_expense\_account”, self.against\_expense\_account).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set against expense account](operations-093.md#op-3a5032940eb443).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L750) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L922)

<a id="op-3b2bc1c4dac60e"></a>
### Purchase Invoice.po required

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_purchase_order_required`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Supplier” via get\_value.

**Local steps**

- If (Platform.db.get\_single\_value(“Buying Settings”, “po\_required”) equals “Yes” and not self.is\_internal\_transfer() and not Platform.get\_value(“Supplier”, self.supplier, “allow\_purchase\_invoice\_creation\_witho ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Buying Settings”, “po\_required”) equals “Yes” → not self.is\_internal\_transfer() → not Platform.get\_value(“Supplier”, self.supplier, “allow\_purchase\_invoice\_creation\_without\_purchase\_order”).
  - For each d in self.get(“items”).
    - If not d.purchase\_order.
      - Set msg from translated “Purchase Order Required for item {}”.format(Platform.bold(d.item\_code)).
      - Update msg using + text in the contract.
      - Update msg using + translated “To submit the invoice without purchase order please set {0} as {1} in {2}”.format(Platform.bold(translated “Purchase Order Required”), Platform.bold(translated “No”), get\_link\_to\_form(“Buying S ….
      - Evaluate throw(msg, title = translated “Mandatory Purchase Order”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “po\_required”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L104) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L760) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L932)

<a id="op-f4b25926c8b5ae"></a>
### Purchase Invoice.pr required

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_purchase_receipt_required`

**Inputs** self.

**Record and data access** read “Buying Settings” via get\_single\_value · read “Supplier” via get\_value.

**Explicit results** no value.

**Local steps**

- If (Platform.db.get\_single\_value(“Buying Settings”, “pr\_required”) equals “Yes” and not self.update\_stock).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.get\_single\_value(“Buying Settings”, “pr\_required”) equals “Yes” → not self.update\_stock.
  - Set stock\_and\_asset\_items from self.get\_stock\_items().
  - Evaluate stock\_and\_asset\_items.extend(self.get\_asset\_items()).
  - If Platform.get\_value(“Supplier”, self.supplier, “allow\_purchase\_invoice\_creation\_without\_purchase\_receipt”).
    - Return no value.
  - For each d in self.get(“items”).
    - If (not d.purchase\_receipt and d.item\_code belongs to stock\_and\_asset\_items).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not d.purchase\_receipt → d.item\_code belongs to stock\_and\_asset\_items.
      - Set msg from translated “Purchase Receipt Required for item {}”.format(Platform.bold(d.item\_code)).
      - Update msg using + text in the contract.
      - Update msg using + translated “To submit the invoice without purchase receipt please set {0} as {1} in {2}”.format(Platform.bold(translated “Purchase Receipt Required”), Platform.bold(translated “No”), get\_link\_to\_form(“Buyi ….
      - Evaluate throw(msg, title = translated “Mandatory Purchase Receipt”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Buying Settings”, “pr\_required”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L105) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L761) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L933)

<a id="op-a5e7b362251f87"></a>
### Purchase Invoice.validate write off account

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_write_off_account`

**Inputs** self.

**Record and data access** read “Account” via get\_value.

**Explicit results** no value.

**Local steps**

- If (self.write\_off\_amount and not self.write\_off\_account).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.write\_off\_amount → not self.write\_off\_account.
  - Evaluate throw(translated “Please enter Write Off Account”).
- If not self.write\_off\_account.
  - Return no value.
- Set doc from Platform.db.get\_value(“Account”, self.write\_off\_account, list(“report\_type”, “is\_group”, “company”), as\_dict = true).
- If (not doc or doc.report\_type differs from “Profit and Loss” or doc.is\_group or doc.company differs from self.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc → doc.report\_type differs from “Profit and Loss” → doc.is\_group → doc.company differs from self.company.
  - Evaluate throw(translated “Please enter a valid Write Off Account”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L5067) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L784) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L956)

<a id="op-bdc7f431a4775d"></a>
### Purchase Invoice.validate write off cost center

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_write_off_cost_center`

**Inputs** self.

**Record and data access** read “Cost Center” via get\_value.

**Explicit results** no value.

**Local steps**

- If not self.write\_off\_cost\_center.
  - Return no value.
- Set doc from Platform.db.get\_value(“Cost Center”, self.write\_off\_cost\_center, list(“is\_group”, “company”), as\_dict = true).
- If (not doc or doc.is\_group or doc.company differs from self.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not doc → doc.is\_group → doc.company differs from self.company.
  - Evaluate throw(translated “Please enter a valid Write Off Cost Center”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0146.json#L5383) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L957)

<a id="op-99df3dabfcc1b6"></a>
### Purchase Invoice.check prev docstatus

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_check_previous_record_state`

**Inputs** self.

**Record and data access** execute query text (SELECT, Purchase) · execute query text (SELECT, Purchase Receipt).

**Explicit failure paths** validation helper — translated “Purchase Order {0} is not submitted”.format(d.purchase\_order) · validation helper — translated “Purchase Receipt {0} is not submitted”.format(d.purchase\_receipt).

**Local steps**

- For each d in self.get(“items”).
  - If d.purchase\_order.
    - Set submitted from Platform.db.sql(query text (SELECT, Purchase), d.purchase\_order).
    - If not submitted.
      - Call the validation error handler Platform.throw(translated “Purchase Order {0} is not submitted”.format(d.purchase\_order)).
  - If d.purchase\_receipt.
    - Set submitted from Platform.db.sql(query text (SELECT, Purchase Receipt), d.purchase\_receipt).
    - If not submitted.
      - Call the validation error handler Platform.throw(translated “Purchase Receipt {0} is not submitted”.format(d.purchase\_receipt)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L748) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L920)

<a id="op-ec446575fb22fc"></a>
### Purchase Invoice.update status updater args

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_update_status_updater_arguments`

**Inputs** self.

**Local steps**

- If cint(self.update\_stock).
  - Evaluate self.status\_updater.append(mapping(“source\_dt” → “Purchase Invoice Item”, “target\_dt” → “Purchase Order Item”, “join\_field” → “po\_detail”, “target\_field” → “received\_qty”, …)).
  - Evaluate self.status\_updater.append(mapping(“source\_dt” → “Purchase Invoice Item”, “target\_dt” → “Material Request Item”, “join\_field” → “material\_request\_item”, “target\_field” → “received\_qty”, …)).
  - If cint(self.is\_return).
    - Evaluate self.status\_updater.append(mapping(“source\_dt” → “Purchase Invoice Item”, “target\_dt” → “Purchase Order Item”, “join\_field” → “po\_detail”, “target\_field” → “returned\_qty”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L769) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L941)

<a id="op-708a7e1405944a"></a>
### Purchase Invoice.validate purchase receipt if update stock

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_purchase_receipt_if_update_stock`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Stock cannot be updated for Purchase Invoice {0} because a Purchase Receipt {1} has already been created for …”.format(self.name, item.purchase\_receipt).

**Local steps**

- If self.update\_stock.
  - For each item in self.get(“items”).
    - If item.purchase\_receipt.
      - Call the validation error handler Platform.throw(translated “Stock cannot be updated for Purchase Invoice {0} because a Purchase Receipt {1} has already been created for …”.format(self.name, item.purchase\_receipt), title = translated “Stoc ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L827) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L779) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L951)

<a id="op-983c87b1089ac2"></a>
### Purchase Invoice.validate for repost

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_validate_for_repost`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_write\_off\_account().
- Evaluate self.validate\_write\_off\_cost\_center().
- Evaluate self.validate\_expense\_account().
- Evaluate validate\_docs\_for\_voucher\_types(list(“Purchase Invoice”)).
- Evaluate validate\_docs\_for\_deferred\_accounting(list(), list(self.name)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate write off account](operations-093.md#op-a5e7b362251f87), [validate write off cost center](operations-093.md#op-bdc7f431a4775d), [validate expense account](operations-093.md#op-65fff90cccc550).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0005.json#L4) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L776) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L948)

<a id="op-966833b225c1fa"></a>
### Purchase Invoice.before submit

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_before_submit`

**Inputs** self.

**Local steps**

- Evaluate self.create\_remarks().

If control reaches the end, it returns no value.

**Methods declared on this owner** [create remarks](operations-092.md#op-cf09fe1346b9cc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L1185) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L744) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L916)

<a id="op-3cfc26d501ca0d"></a>
### Purchase Invoice.on submit

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_on_submit`

**Inputs** self.

**Record and data access** resolve a document from “Authorization Control” via get\_cached\_doc · read “Buying Settings” via get\_single\_value · resolve a document from self.doctype via get\_doc.

**Local steps**

- Evaluate super().on\_submit().
- Evaluate PurchaseTaxWithholding(self).on\_submit().
- Evaluate self.check\_prev\_docstatus().
- If (self.is\_return and not self.update\_billed\_amount\_in\_purchase\_order).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → not self.update\_billed\_amount\_in\_purchase\_order.
  - Set self.status\_updater from list().
- Evaluate self.update\_status\_updater\_args().
- Evaluate self.update\_prevdoc\_status().
- Evaluate Platform.get\_cached\_doc(“Authorization Control”).validate\_approving\_authority(self.doctype, self.company, self.base\_grand\_total).
- If not self.is\_return.
  - Evaluate self.update\_against\_document\_in\_jv().
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Purchase Receipt”).
  - Evaluate self.update\_billing\_status\_for\_zero\_amount\_refdoc(“Purchase Order”).
- Evaluate self.update\_billing\_status\_in\_pr().
- If self.update\_stock equals 1.
  - Evaluate self.make\_bundle\_for\_sales\_purchase\_return().
  - Evaluate self.make\_bundle\_using\_old\_serial\_batch\_fields().
  - Evaluate self.update\_stock\_ledger().
  - If self.is\_old\_subcontracting\_flow.
    - Evaluate self.set\_consumed\_qty\_in\_subcontract\_order().
- Evaluate self.make\_gl\_entries().
- If self.update\_stock equals 1.
  - Evaluate self.repost\_future\_sle\_and\_gle().
- If Platform.db.get\_single\_value(“Buying Settings”, “project\_update\_frequency”) equals “Each Transaction”.
  - Evaluate self.update\_project().
- Evaluate update\_linked\_doc(self.doctype, self.name, self.inter\_company\_invoice\_reference).
- Evaluate self.process\_common\_party\_accounting().
- If (self.is\_return and self.return\_against).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_return → self.return\_against.
  - Evaluate Platform.get\_doc(self.doctype, self.return\_against).set\_status(update = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [check prev docstatus](operations-093.md#op-99df3dabfcc1b6), [update status updater args](operations-093.md#op-ec446575fb22fc), [update billing status in pr](operations-094.md#op-fbf06faf221098), [make gl entries](operations-093.md#op-4d8effc07d1356), [update project](operations-094.md#op-9eb56a154ef3b4).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Authorization Control”), Platform.db.get\_single\_value(“Buying Settings”, “project\_update\_frequency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L102) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L757) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L929)

<a id="op-51405fdd2d27f0"></a>
### Purchase Invoice.on update after submit

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_on_update_after_submit`

**Inputs** self.

**Local steps**

- Set fields\_to\_check from list(“cash\_bank\_account”, “write\_off\_account”, “unrealized\_profit\_loss\_account”, “is\_opening”).
- Set child\_tables from mapping(“items” → tuple(“expense\_account”), “taxes” → tuple(“account\_head”)).
- Set needs\_repost from self.check\_if\_fields\_updated(fields\_to\_check, child\_tables).
- If needs\_repost.
  - Evaluate self.validate\_for\_repost().
  - Evaluate self.repost\_accounting\_entries().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for repost](operations-093.md#op-983c87b1089ac2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L103) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L758) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L930)

<a id="op-a5783a281fba25"></a>
### Purchase Invoice.refresh subscription status

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_refresh_subscription_status`

**Inputs** self.

**Local steps**

- If self.get(“subscription”).
  - Evaluate refresh\_subscription\_status(self.subscription).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L2166) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L762) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L934)

<a id="op-4d8effc07d1356"></a>
### Purchase Invoice.make gl entries

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_make_general_ledger_entries`

**Inputs** self, gl\_entries = no value, from\_repost = false.

**Local steps**

- Set update\_outstanding from “No” when (cint(self.is\_paid) or self.write\_off\_account), otherwise “Yes”.
  - Value choice on (cint(self.is\_paid) or self.write\_off\_account) — true gives “No”, false gives “Yes”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(self.is\_paid) → self.write\_off\_account.
- If self.docstatus equals 1.
  - Evaluate self.cancel\_provisional\_entries().
  - If not gl\_entries.
    - Set gl\_entries from self.get\_gl\_entries().
  - If gl\_entries.
    - Evaluate make\_gl\_entries(gl\_entries, update\_outstanding = update\_outstanding, merge\_entries = false, from\_repost = from\_repost).
    - Evaluate self.make\_exchange\_gain\_loss\_journal().
- Otherwise.
  - If self.docstatus equals 2.
    - Evaluate make\_reverse\_gl\_entries(voucher\_type = self.doctype, voucher\_no = self.name).
    - Evaluate self.cancel\_provisional\_entries().
- Evaluate self.update\_supplier\_outstanding(update\_outstanding).

If control reaches the end, it returns no value.

**Methods declared on this owner** [cancel provisional entries](operations-093.md#op-ba404987dcb0bd), [get gl entries](operations-094.md#op-1c0e107858bb1d), [update supplier outstanding](operations-093.md#op-4893d5be8421ac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L99) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L754) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L926)

<a id="op-ba404987dcb0bd"></a>
### Purchase Invoice.cancel provisional entries

`operation_enterprise_binding_enterprise_accounts_doctype_purchase_invoice_purchase_invoice_purchaseinvoice_cancel_provisional_entries`

**Inputs** self.

**Local steps**

- Set rows from set().
- Set purchase\_receipts from set().
- For each d in self.items.
  - If d.purchase\_receipt.
    - Evaluate purchase\_receipts.add(d.purchase\_receipt).
    - Evaluate rows.add(d.name).
- If rows.
  - Set gle from qb.DocType(“GL Entry”).
  - Set gle\_update\_query from qb.update(gle).set(gle.is\_cancelled, 1).where(((gle.voucher\_type equals “Purchase Receipt” bitwise and gle.voucher\_no.isin(purchase\_receipts)) bitwise and gle.voucher\_detail\_no.isin(rows))).
  - Evaluate gle\_update\_query.run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0010.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L311) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L949)

<a id="op-4893d5be8421ac"></a>
### Purchase Invoice.update supplier outstanding

`operation_enterprise_accounts_record_definitions_purchase_invoice_business_behavior_purchase_invoice_update_supplier_outstanding`

**Inputs** self, update\_outstanding.

**Local steps**

- If update\_outstanding equals “No”.
  - Evaluate update\_voucher\_outstanding(voucher\_type = self.doctype, voucher\_no = self.return\_against when (cint(self.is\_return) and self.return\_against), otherwise self.name, account = self.credit\_to, party\_type = “Su ….
    - Value choice on (cint(self.is\_return) and self.return\_against) — true gives self.return\_against, false gives self.name.
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in cint(self.is\_return) → self.return\_against.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0147.json#L2638) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L770) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L942)
