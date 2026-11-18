# Accounting and settlement · operations 68

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment entry

[Record definition](../../../../data/record-types/payment_entry.json)

<a id="op-c1f0f5c9675409"></a>
### Set pending discount loss

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_pending_discount_loss`

**Inputs** pe, doc, discount\_amount, base\_total\_discount\_loss, party\_account\_currency.

**Record and data access** read “Accounts Settings” via get\_single\_value · read “Company” via get\_cached\_value.

**Local steps**

- If party\_account\_currency differs from doc.company\_currency.
  - Set discount\_amount from (discount\_amount × doc.get(“conversion\_rate”, 1)).
- Set discount\_amount from flt((discount\_amount − base\_total\_discount\_loss), doc.precision(“grand\_total”)).
- If discount\_amount &gt; 0.0.
  - Set positive\_negative from negative 1 when pe.payment\_type equals “Pay”, otherwise 1.
    - Value choice on pe.payment\_type equals “Pay” — true gives negative 1, false gives 1.
  - Set book\_tax\_loss from Platform.get\_single\_value(“Accounts Settings”, “book\_tax\_discount\_loss”).
  - Set account\_type from “round\_off\_account” when book\_tax\_loss, otherwise “default\_discount\_account”.
    - Value choice on book\_tax\_loss — true gives “round\_off\_account”, false gives “default\_discount\_account”.
  - Evaluate pe.append(“deductions”, mapping(“account” → Platform.get\_cached\_value(“Company”, pe.company, account\_type), “cost\_center” → (pe.cost\_center or Platform.get\_cached\_value(“Company”, pe.company, “cost\_center” ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in pe.cost\_center → Platform.get\_cached\_value(“Company”, pe.company, “cost\_center”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “book\_tax\_discount\_loss”), Platform.get\_cached\_value(“Company”, pe.company, account\_type) and 1 further calls.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0083.json#L1399) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1540) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L127)

<a id="op-26782cfa683f93"></a>
### Split early payment discount loss

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_split_early_payment_discount_loss`

**Inputs** pe, doc, valid\_discounts.

**Declared result** float.

**Explicit results** base\_total\_discount\_loss.

**Local steps**

- Set tuple(discount\_loss\_rows, base\_total\_discount\_loss) from get\_early\_payment\_discount\_loss(doc, valid\_discounts, pe.payment\_type, pe.company, …).
- For each row in discount\_loss\_rows.
  - Evaluate pe.append(“deductions”, row).
- Return base\_total\_discount\_loss.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L50) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1541) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L128)

<a id="op-d9327668201d29"></a>
### Get early payment discount loss

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_get_early_payment_discount_loss`

**Inputs** doc, valid\_discounts, payment\_type, company, cost\_center = no value.

**Declared result** tuple at tuple(list at dict, float).

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(list(), 0.0) · tuple(rows, base\_total\_discount\_loss).

**Local steps**

- Set total\_discount\_percent from get\_total\_discount\_percent(doc, valid\_discounts).
- If not total\_discount\_percent.
  - Return tuple(list(), 0.0).
- Set cost\_center from (cost\_center or Platform.get\_cached\_value(“Company”, company, “cost\_center”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cost\_center → Platform.get\_cached\_value(“Company”, company, “cost\_center”).
- Set positive\_negative from negative 1 when payment\_type equals “Pay”, otherwise 1.
  - Value choice on payment\_type equals “Pay” — true gives negative 1, false gives 1.
- Set base\_loss\_on\_income from (doc.get(“base\_total”) × (total\_discount\_percent ÷ 100)).
- Set rows from list(mapping(“account” → Platform.get\_cached\_value(“Company”, company, “default\_discount\_account”), “cost\_center” → cost\_center, “amount” → (flt(base\_loss\_on\_income, doc.precision(“total”)) × positive\_negative))).
- Set base\_loss\_by\_tax\_account from mapping().
- For each tax in doc.get(“taxes”, list()).
  - Set base\_tax\_loss from (tax.get(“base\_tax\_amount\_after\_discount\_amount”) × (total\_discount\_percent ÷ 100)).
  - Set account from tax.get(“account\_head”).
  - Set base\_loss\_by\_tax\_account at account from (base\_loss\_by\_tax\_account.get(account, 0) + base\_tax\_loss).
- Set tax\_precision from doc.precision(“tax\_amount\_after\_discount\_amount”, “taxes”).
- For each tuple(account, base\_tax\_loss) in base\_loss\_by\_tax\_account.items().
  - If base\_tax\_loss equals 0.0.
    - Continue with the next iteration or loop test.
  - Evaluate rows.append(mapping(“account” → account, “cost\_center” → cost\_center, “amount” → (flt(base\_tax\_loss, tax\_precision) × positive\_negative))).
- Set base\_loss\_on\_taxes from sum(base\_loss\_by\_tax\_account.values()).
- Set base\_total\_discount\_loss from flt((base\_loss\_on\_income + base\_loss\_on\_taxes), doc.precision(“grand\_total”)).
- Return tuple(rows, base\_total\_discount\_loss).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “cost\_center”), Platform.get\_cached\_value(“Company”, company, “default\_discount\_account”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L187) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L825)

<a id="op-2b7b27a718c4f7"></a>
### Get total discount percent

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_total_discount_percent`

**Inputs** doc, valid\_discounts.

**Declared result** float.

**Explicit results** total\_discount\_percent.

**Local steps**

- Set total\_discount\_percent from (sum(generator of discount.get(“discount”) for discount drawn from valid\_discounts where discount.get(“type”) equals “Percentage”) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sum(generator of discount.get(“discount”) for discount drawn from valid\_discounts where discount.get(“type”) equals “Percentage”) → 0.0.
  - Draw discount from valid\_discounts, keep a combination only if (discount.get(“type”) equals “Percentage”).
- Set total\_discount\_amount from (sum(generator of discount.get(“discount”) for discount drawn from valid\_discounts where discount.get(“type”) equals “Amount”) or 0.0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in sum(generator of discount.get(“discount”) for discount drawn from valid\_discounts where discount.get(“type”) equals “Amount”) → 0.0.
  - Draw discount from valid\_discounts, keep a combination only if (discount.get(“type”) equals “Amount”).
- If total\_discount\_amount.
  - Set discount\_percentage from ((total\_discount\_amount ÷ doc.get(“grand\_total”)) × 100).
  - Update total\_discount\_percent using + discount\_percentage.
  - Return total\_discount\_percent.
- Return total\_discount\_percent.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0083.json#L2126) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1454) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L41)

<a id="op-595ac76f815dc0"></a>
### Get reference as per payment terms

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_reference_as_per_payment_terms`

**Inputs** payment\_schedule, dt, dn, doc, grand\_total, outstanding\_amount, party\_account\_currency.

**Explicit results** references.

**Local steps**

- Set references from list().
- Set remaining\_outstanding from outstanding\_amount.
- Set is\_multi\_currency\_acc from (doc.currency differs from doc.company\_currency and party\_account\_currency differs from doc.company\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.currency differs from doc.company\_currency → party\_account\_currency differs from doc.company\_currency.
- For each payment\_term in payment\_schedule.
  - Set payment\_term\_outstanding from flt(payment\_term.outstanding, payment\_term.precision(“payment\_amount”)).
  - If not is\_multi\_currency\_acc.
    - Set payment\_term\_outstanding from flt((payment\_term\_outstanding × doc.get(“conversion\_rate”)), payment\_term.precision(“payment\_amount”)).
  - If payment\_term\_outstanding.
    - Set allocated\_amount from min(payment\_term\_outstanding, remaining\_outstanding) when payment\_term\_outstanding &gt; 0, otherwise max(payment\_term\_outstanding, remaining\_outstanding).
      - Value choice on payment\_term\_outstanding &gt; 0 — true gives min(payment\_term\_outstanding, remaining\_outstanding), false gives max(payment\_term\_outstanding, remaining\_outstanding).
    - Set remaining\_outstanding from flt((remaining\_outstanding − allocated\_amount), payment\_term.precision(“payment\_amount”)).
    - Evaluate references.append(mapping(“reference\_doctype” → dt, “reference\_name” → dn, “bill\_no” → doc.get(“bill\_no”), “due\_date” → doc.get(“due\_date”), …)).
- Return references.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L37)

<a id="op-fbfb8034467e7f"></a>
### Get paid amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_paid_amount`

**Inputs** dt, dn, party\_type, party, account, due\_date.

**State and service calls** execute a supplied database query.

**Explicit results** paid\_amount at 0 at 0 when paid\_amount, otherwise 0.

**Local steps**

- If party\_type equals “Customer”.
  - Set dr\_or\_cr from “credit\_in\_account\_currency - debit\_in\_account\_currency”.
- Otherwise.
  - Set dr\_or\_cr from “debit\_in\_account\_currency - credit\_in\_account\_currency”.
- Set paid\_amount from Platform.db.sql(formatted text   select ifnull(sum({dr\_or\_cr}), 0) as paid\_amount  from ′tabGL Entry′  where against\_voucher\_type = %s  and against\_voucher = %s  and party\_ty, tuple(dt, dn, party\_ty ….
- Return paid\_amount at 0 at 0 when paid\_amount, otherwise 0.
  - Value choice on paid\_amount — true gives paid\_amount at 0 at 0, false gives 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1446) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L33)

<a id="op-27913eb34f5d69"></a>
### Make payment order

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_make_payment_order`

**Inputs** source\_name, target\_doc = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doclist.

**Local steps**

- Bind dependencies get\_mapped\_doc.
- Bind local operation set\_missing\_values for subsequent calls.
- Set doclist from get\_mapped\_doc(“Payment Entry”, source\_name, mapping(“Payment Entry” → mapping(“doctype” → “Payment Order”, “validation” → mapping(“docstatus” → list(“=”, 1)), “field\_no\_map” → list(“naming\_series”, “compa ….
  - Value choice on target\_doc — true gives list(“naming\_series”, “company”), false gives list(“naming\_series”).
- Return doclist.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1455) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L42)

<a id="op-2862b39530b2e7"></a>
### Make payment order.set missing values

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_make_payment_order_set_missing_values`

**Inputs** source, target.

**Local steps**

- Set target.payment\_order\_type from “Payment Entry”.
- Set target.company from (target.company or source.company).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target.company → source.company.
- Evaluate target.append(“references”, dict(reference\_doctype = “Payment Entry”, reference\_name = source.name, bank\_account = source.party\_bank\_account, amount = source.paid\_amount, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1456) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L43)

<a id="op-6dfd21432b2ec8"></a>
### Add regional gl entries

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_add_regional_general_ledger_entries`

**Inputs** gl\_entries, doc.

**Wrappers, in declaration order** Enterprise.allow\_regional.

**Explicit results** no value.

**Local steps**

- Return no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0083.json#L5070) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L17)

<a id="op-2b76b50426282b"></a>
### Get linked bank transactions

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_linked_bank_transactions`

**Inputs** payment\_entry.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list.

**Record and data access** read “Bank Transaction Payments” via get\_all.

**Explicit results** Platform.get\_all(“Bank Transaction Payments”, filters = mapping(“payment\_document” → “Payment Entry”, “payment\_entry” → payment\_entry), pluck = “parent”).

**Local steps**

- Evaluate Platform.has\_permission(“Payment Entry”, ptype = “read”, doc = payment\_entry, throw = true).
- Return Platform.get\_all(“Bank Transaction Payments”, filters = mapping(“payment\_document” → “Payment Entry”, “payment\_entry” → payment\_entry), pluck = “parent”).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Entry”, ptype = “read”, doc = payment\_entry, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0083.json#L5122) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1437) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L24)

<a id="op-dddf34d1254e7e"></a>
### Get data

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_dashboard_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payment\_entry”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”), “transactions” → list(mapping(“label” → translated “Accounting”, “items” → list(“Journal Entry”)))).

**Local steps**

- Return mapping(“fieldname” → “payment\_entry”, “non\_standard\_fieldnames” → mapping(“Journal Entry” → “reference\_name”), “transactions” → list(mapping(“label” → translated “Accounting”, “items” → list(“Journal Entry”)))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L186) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L824)

## Record · Payment entry reference

[Record definition](../../../../data/record-types/payment_entry_reference.json)

<a id="op-94777ded23b5d1"></a>
### Payment Entry Reference.payment request outstanding

`operation_enterprise_accounts_record_definitions_payment_entry_reference_business_behavior_payment_entry_reference_payment_request_outstanding`

**Inputs** self.

**Wrappers, in declaration order** property.

**Record and data access** read “Payment Request” via get\_value.

**Explicit results** no value · Platform.db.get\_value(“Payment Request”, self.payment\_request, “outstanding\_amount”).

**Local steps**

- If not self.payment\_request.
  - Return no value.
- Return Platform.db.get\_value(“Payment Request”, self.payment\_request, “outstanding\_amount”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4093) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1546) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L133)

## Record · Payment gateway account

[Record definition](../../../../data/record-types/payment_gateway_account.json)

<a id="op-b2530be2363926"></a>
### Payment Gateway Account.autoname

`operation_enterprise_accounts_record_definitions_payment_gateway_account_business_behavior_payment_gateway_account_autoname`

**Inputs** self.

**Record and data access** read “Company” via get\_value.

**Local steps**

- Set abbr from Platform.db.get\_value(“Company”, self.company, “abbr”).
- Set self.name from ((((self.payment\_gateway + “ - ”) + self.currency) + “ - ”) + abbr).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4202) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1635) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L198)

<a id="op-32bcfadb675e38"></a>
### Payment Gateway Account.validate

`operation_enterprise_accounts_record_definitions_payment_gateway_account_business_behavior_payment_gateway_account_validate`

**Inputs** self.

**Record and data access** read “Account” via get\_cached\_value.

**Local steps**

- Set self.currency from Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_currency”).
- Evaluate self.update\_default\_payment\_gateway().
- Evaluate self.set\_as\_default\_if\_not\_set().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update default payment gateway](operations-068.md#op-1923fdbe4b089c), [set as default if not set](operations-068.md#op-bbaa07c8d90c23).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, self.payment\_account, “account\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4347) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1638) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L201)

<a id="op-1923fdbe4b089c"></a>
### Payment Gateway Account.update default payment gateway

`operation_enterprise_accounts_record_definitions_payment_gateway_account_business_behavior_payment_gateway_account_update_default_payment_gateway`

**Inputs** self.

**State and service calls** request set\_value on “Payment Gateway Account”.

**Local steps**

- If self.is\_default.
  - Evaluate Platform.db.set\_value(“Payment Gateway Account”, mapping(“is\_default” → 1, “name” → list(“!=”, self.name), “company” → self.company), “is\_default”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4474) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1637) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L200)

<a id="op-bbaa07c8d90c23"></a>
### Payment Gateway Account.set as default if not set

`operation_enterprise_accounts_record_definitions_payment_gateway_account_business_behavior_payment_gateway_account_set_as_default_if_not_set`

**Inputs** self.

**Record and data access** read “Payment Gateway Account” via exists.

**Local steps**

- If not Platform.db.exists(“Payment Gateway Account”, mapping(“is\_default” → 1, “name” → tuple(“!=”, self.name), “company” → self.company)).
  - Set self.is\_default from 1.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4636) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1636) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L199)

<a id="op-23a60301a911c5"></a>
### Get data

`operation_enterprise_accounts_record_definitions_payment_gateway_account_payment_gateway_account_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “payment\_gateway\_account”, “non\_standard\_fieldnames” → mapping(“Subscription Plan” → “payment\_gateway”), “transactions” → list(mapping(“items” → list(“Payment Request”)), mapping(“ite ….

**Local steps**

- Return mapping(“fieldname” → “payment\_gateway\_account”, “non\_standard\_fieldnames” → mapping(“Subscription Plan” → “payment\_gateway”), “transactions” → list(mapping(“items” → list(“Payment Request”)), mapping(“ite ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0090.json#L4795) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1639) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L202)

## Report · Payment ledger

<a id="op-e3d04a0017ba8d"></a>
### Payment Ledger.initialize

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_initialize`

**Inputs** self, filters = no value.

**Local steps**

- Set self.filters from filters.
- Set tuple(self.columns, self.data) from tuple(list(), list()).
- Set self.voucher\_dict from OrderedDict().
- Set self.voucher\_amount from list().
- Set self.ple from qb.DocType(“Payment Ledger Entry”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0267.json#L1516) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L789) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1131)

<a id="op-4819783d701741"></a>
### Payment Ledger.init voucher dict

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_initialize_voucher_mapping`

**Inputs** self.

**Local steps**

- If self.voucher\_amount.
  - For each ple in self.voucher\_amount.
    - Set group\_by\_key from no value.
    - If not self.filters.group\_party.
      - Set group\_by\_key from tuple(ple.against\_voucher\_type, ple.against\_voucher\_no, ple.party).
    - Otherwise.
      - Set group\_by\_key from tuple(ple.party\_type, ple.party).
    - Set target from no value.
    - If ple.amount &gt; 0.
      - Set target from self.voucher\_dict.setdefault(group\_by\_key, mapping()).setdefault(“increase”, list()).
    - Otherwise.
      - Set target from self.voucher\_dict.setdefault(group\_by\_key, mapping()).setdefault(“decrease”, list()).
    - If target is distinct from no value.
      - Set entry from Platform.\_dict(posting\_date = ple.posting\_date, account = ple.account, party\_type = ple.party\_type, party = ple.party, …).
      - If self.filters.include\_account\_currency.
        - Set entry at “amount\_in\_account\_currency” from ple.amount\_in\_account\_currency.
      - Evaluate target.append(entry).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0267.json#L1692) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L790) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1132)

<a id="op-e825fd916b6396"></a>
### Payment Ledger.build data

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_build_data`

**Inputs** self.

**Local steps**

- Evaluate self.data.clear().
- For each value in self.voucher\_dict.values().
  - Set voucher\_data from list().
  - If value.get(“increase”).
    - Evaluate voucher\_data.extend(value.get(“increase”)).
  - If value.get(“decrease”).
    - Evaluate voucher\_data.extend(value.get(“decrease”)).
  - If voucher\_data.
    - Set total from 0.
    - Set total\_in\_account\_currency from 0.
    - For each x in voucher\_data.
      - Update total using + x.amount.
      - If self.filters.include\_account\_currency.
        - Update total\_in\_account\_currency using + x.amount\_in\_account\_currency.
    - Set entry from Platform.\_dict(against\_voucher\_no = “Outstanding:”, amount = total, currency = voucher\_data at 0.currency, company = voucher\_data at 0.company).
    - If self.filters.include\_account\_currency.
      - Set entry at “amount\_in\_account\_currency” from total\_in\_account\_currency.
    - Evaluate voucher\_data.append(entry).
    - Evaluate voucher\_data.append(Platform.\_dict(currency = voucher\_data at 0.currency, company = voucher\_data at 0.company)).
    - Evaluate self.data.extend(voucher\_data).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0267.json#L2269) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L786) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1128)

<a id="op-c642f58b76156f"></a>
### Payment Ledger.build conditions

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_build_conditions`

**Inputs** self.

**Record and data access** read “Party Type” via get\_all.

**Explicit results** no value.

**Local steps**

- Set self.conditions from list().
- If self.filters.company.
  - Evaluate self.conditions.append(self.ple.company equals self.filters.company).
- If self.filters.account.
  - Evaluate self.conditions.append(self.ple.account.isin(self.filters.account)).
- If self.filters.period\_start\_date.
  - Evaluate self.conditions.append(self.ple.posting\_date.gte(self.filters.period\_start\_date)).
- If self.filters.period\_end\_date.
  - Evaluate self.conditions.append(self.ple.posting\_date.lte(self.filters.period\_end\_date)).
- If self.filters.voucher\_no.
  - Evaluate self.conditions.append(self.ple.voucher\_no equals self.filters.voucher\_no).
- If self.filters.against\_voucher\_no.
  - Evaluate self.conditions.append(self.ple.against\_voucher\_no equals self.filters.against\_voucher\_no).
- If self.filters.party\_type.
  - Evaluate self.conditions.append(self.ple.party\_type equals self.filters.party\_type).
- If self.filters.party.
  - Evaluate self.conditions.append(self.ple.party.isin(self.filters.party)).
- Bind dependencies get\_user\_permissions.
- Bind dependencies get\_allowed\_docs\_for\_doctype.
- Set user\_permissions from get\_user\_permissions().
- If not user\_permissions.
  - Return no value.
- Set strict from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).
- For each party\_type in Platform.db.get\_all(“Party Type”, pluck = “name”).
  - If party\_type does not belong to user\_permissions.
    - Continue with the next iteration or loop test.
  - Set allowed\_parties from get\_allowed\_docs\_for\_doctype(user\_permissions at party\_type, “Payment Ledger Entry”).
  - If not allowed\_parties.
    - Continue with the next iteration or loop test.
  - Set condition from (IfNull(self.ple.party\_type, empty text) differs from party\_type bitwise or self.ple.party.isin(allowed\_parties)).
  - If not strict.
    - Update condition using bitwise or IfNull(self.ple.party, empty text) equals empty text.
  - Evaluate self.conditions.append(condition).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from get\_user\_permissions() · configured or stored value from Platform.get\_system\_settings(“apply\_strict\_user\_permissions”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L785) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1127)

<a id="op-a9da35d0f713e7"></a>
### Payment Ledger.get data

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_get_data`

**Inputs** self.

**Local steps**

- Set ple from self.ple.
- Evaluate self.build\_conditions().
- Set query from nested operand in the contract(nested operand in the contract).select(ple.star).where(ple.delinked equals 0).where(Criterion.all(self.conditions)).
- Bind dependencies build\_match\_conditions.
- If match\_conditions bound to build\_match\_conditions(“Payment Ledger Entry”).
  - Set query from query.where(Bracket(LiteralValue(match\_conditions))).
- Set self.voucher\_amount from query.run(as\_dict = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [build conditions](operations-068.md#op-c642f58b76156f).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L788) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1130)

<a id="op-e0e5dd15c9feae"></a>
### Payment Ledger.get columns

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_get_columns`

**Inputs** self.

**Local steps**

- Set options from no value.
- Evaluate self.columns.append(dict(label = translated “Posting Date”, fieldname = “posting\_date”, fieldtype = “Date”, options = options, …)).
- Evaluate self.columns.append(dict(label = translated “Account”, fieldname = “account”, fieldtype = “data”, options = options, …)).
- Evaluate self.columns.append(dict(label = translated “Party Type”, fieldname = “party\_type”, fieldtype = “Link”, options = “DocType”, …)).
- Evaluate self.columns.append(dict(label = translated “Party”, fieldname = “party”, fieldtype = “Dynamic Link”, options = “party\_type”, …)).
- Evaluate self.columns.append(dict(label = translated “Voucher Type”, fieldname = “voucher\_type”, fieldtype = “Link”, options = “DocType”, …)).
- Evaluate self.columns.append(dict(label = translated “Voucher No”, fieldname = “voucher\_no”, fieldtype = “Dynamic Link”, options = “voucher\_type”, …)).
- Evaluate self.columns.append(dict(label = translated “Against Voucher Type”, fieldname = “against\_voucher\_type”, fieldtype = “Link”, options = “DocType”, …)).
- Evaluate self.columns.append(dict(label = translated “Against Voucher No”, fieldname = “against\_voucher\_no”, fieldtype = “Dynamic Link”, options = “against\_voucher\_type”, …)).
- Evaluate self.columns.append(dict(label = translated “Amount”, fieldname = “amount”, fieldtype = “Currency”, options = “Company:company:default\_currency”, …)).
- If self.filters.include\_account\_currency.
  - Evaluate self.columns.append(dict(label = translated “Amount in Account Currency”, fieldname = “amount\_in\_account\_currency”, fieldtype = “Currency”, options = “currency”, …)).
- Evaluate self.columns.append(dict(label = translated “Currency”, fieldname = “currency”, fieldtype = “Link”, options = “Currency”, …)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L24) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L787) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1129)

<a id="op-89f08174256d55"></a>
### Payment Ledger.run

`operation_enterprise_accounts_report_payment_ledger_business_behavior_payment_ledger_run`

**Inputs** self.

**Explicit results** tuple(self.columns, self.data).

**Local steps**

- Evaluate self.get\_columns().
- Evaluate self.get\_data().
- Evaluate self.init\_voucher\_dict().
- Evaluate self.build\_data().
- Return tuple(self.columns, self.data).

**Methods declared on this owner** [get columns](operations-068.md#op-e0e5dd15c9feae), [get data](operations-068.md#op-a9da35d0f713e7), [init voucher dict](operations-068.md#op-4819783d701741), [build data](operations-068.md#op-e825fd916b6396).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0267.json#L4893) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L791) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1133)
