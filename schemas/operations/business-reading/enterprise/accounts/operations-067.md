# Accounting and settlement · operations 67

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Payment entry

[Record definition](../../../../data/record-types/payment_entry.json)

<a id="op-665ff61be92cc2"></a>
### Get outstanding reference documents

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_outstanding_reference_documents`

**Inputs** args, validate = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value · read d.voucher\_type via get\_value.

**State and service calls** msgprint with translated “No outstanding {0} found for the {1} {2} which qualify the filters you have specified.”.format(translated ref\_document\_type, translated args.get(“party\_type”).lower(), Platform.bold(args.get(“party”))).

**Explicit results** no value · list() · data.

**Local steps**

- If isinstance(args, str).
  - Set args from json.loads(args).
- If args.get(“party\_type”) equals “Member”.
  - Return no value.
- If (args.get(“party\_type”) and args.get(“party”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“party\_type”) → args.get(“party”).
  - Set party\_to\_check from no value when has\_ignored\_field(“Payment Entry”, args at “party\_type”), otherwise args at “party”.
    - Value choice on has\_ignored\_field(“Payment Entry”, args at “party\_type”) — true gives no value, false gives args at “party”.
  - Evaluate Platform.has\_permission(args at “party\_type”, “read”, party\_to\_check, throw = true).
- If (not args.get(“get\_outstanding\_invoices”) and not args.get(“get\_orders\_to\_be\_billed”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not args.get(“get\_outstanding\_invoices”) → not args.get(“get\_orders\_to\_be\_billed”).
  - Set args at “get\_outstanding\_invoices” from true.
- Set ple from qb.DocType(“Payment Ledger Entry”).
- Set common\_filter from list().
- Set accounting\_dimensions\_filter from list().
- Set posting\_and\_due\_date from list().
- If (args.get(“party\_type”) equals “Supplier” and Platform.get\_lazy\_doc(“Supplier”, args at “party”).is\_blocked\_for(“Payments”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“party\_type”) equals “Supplier” → Platform.get\_lazy\_doc(“Supplier”, args at “party”).is\_blocked\_for(“Payments”).
  - Return list().
- Set party\_account\_currency from get\_account\_currency(args.get(“party\_account”)).
- Set company\_currency from Platform.get\_cached\_value(“Company”, args.get(“company”), “default\_currency”).
- Set condition from empty text.
- If (args.get(“voucher\_type”) and args.get(“voucher\_no”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“voucher\_type”) → args.get(“voucher\_no”).
  - Set condition from formatted text  and voucher\_type={Platform.db.escape(args at “voucher\_type”)} and voucher\_no={Platform.db.escape(args at “voucher\_no”)}.
  - Evaluate common\_filter.append(ple.voucher\_type equals args at “voucher\_type”).
  - Evaluate common\_filter.append(ple.voucher\_no equals args at “voucher\_no”).
- If args.get(“cost\_center”).
  - Update condition using + formatted text  and cost\_center={Platform.db.escape(args.get(“cost\_center”))}.
  - Evaluate accounting\_dimensions\_filter.append(ple.cost\_center equals args.get(“cost\_center”)).
- Set active\_dimensions from get\_dimensions() at 0.
- For each dim in active\_dimensions.
  - If args.get(dim.fieldname).
    - Update condition using + formatted text  and {dim.fieldname}={Platform.db.escape(args.get(dim.fieldname))}.
    - Evaluate accounting\_dimensions\_filter.append(ple at dim.fieldname equals args.get(dim.fieldname)).
- Set date\_fields\_dict from mapping(“posting\_date” → list(“from\_posting\_date”, “to\_posting\_date”), “due\_date” → list(“from\_due\_date”, “to\_due\_date”)).
- For each tuple(fieldname, date\_fields) in date\_fields\_dict.items().
  - Set from\_date from Platform.db.escape(str(args.get(date\_fields at 0))) when args.get(date\_fields at 0), otherwise no value.
    - Value choice on args.get(date\_fields at 0) — true gives Platform.db.escape(str(args.get(date\_fields at 0))), false gives no value.
  - Set to\_date from Platform.db.escape(str(args.get(date\_fields at 1))) when args.get(date\_fields at 1), otherwise no value.
    - Value choice on args.get(date\_fields at 1) — true gives Platform.db.escape(str(args.get(date\_fields at 1))), false gives no value.
  - If (args.get(date\_fields at 0) and args.get(date\_fields at 1)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(date\_fields at 0) → args.get(date\_fields at 1).
    - Update condition using + formatted text  and {fieldname} between {from\_date} and {to\_date}.
    - Evaluate posting\_and\_due\_date.append(ple at fieldname at slice args.get(date\_fields at 0) to args.get(date\_fields at 1)).
  - Otherwise.
    - If args.get(date\_fields at 0).
      - Update condition using + formatted text  and {fieldname} &gt;= {from\_date}.
      - Evaluate posting\_and\_due\_date.append(ple at fieldname.gte(args.get(date\_fields at 0))).
    - Otherwise.
      - If args.get(date\_fields at 1).
        - Update condition using + formatted text  and {fieldname} &lt;= {to\_date}.
        - Evaluate posting\_and\_due\_date.append(ple at fieldname.lte(args.get(date\_fields at 1))).
- If args.get(“company”).
  - Update condition using + “ and company = {}”.format(Platform.db.escape(args.get(“company”))).
  - Evaluate common\_filter.append(ple.company equals args.get(“company”)).
- Set outstanding\_invoices from list().
- Set negative\_outstanding\_invoices from list().
- Set party\_account from args.get(“party\_account”).
- If args.get(“book\_advance\_payments\_in\_separate\_party\_account”).
  - Set accounts from get\_party\_account(args.get(“party\_type”), args.get(“party”), args.get(“company”), include\_advance = true).
  - Set advance\_account from accounts at 1 when len(accounts) &gt; 1, otherwise no value.
    - Value choice on len(accounts) &gt; 1 — true gives accounts at 1, false gives no value.
  - If party\_account equals advance\_account.
    - Set party\_account from accounts at 0.
- If args.get(“get\_outstanding\_invoices”).
  - Set outstanding\_invoices from get\_outstanding\_invoices(args.get(“party\_type”), args.get(“party”), list(party\_account), common\_filter = common\_filter, posting\_date = posting\_and\_due\_date, min\_outstanding = args.get(“outstanding\_amt\_grea ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“vouchers”) → no value.
  - Set outstanding\_invoices from split\_refdocs\_based\_on\_payment\_terms(outstanding\_invoices, args.get(“company”)).
  - For each d in outstanding\_invoices.
    - Set d at “exchange\_rate” from 1.
    - If party\_account\_currency differs from company\_currency.
      - If d.voucher\_type belongs to Platform.get\_hooks(“invoice\_doctypes”).
        - Set d at “exchange\_rate” from Platform.db.get\_value(d.voucher\_type, d.voucher\_no, “conversion\_rate”).
      - Otherwise.
        - If d.voucher\_type equals “Journal Entry”.
          - Set d at “exchange\_rate” from get\_journal\_entry\_exchange\_rate(d.voucher\_no, args.get(“party\_type”), args.get(“party”), party\_account\_currency, …).
    - If d.voucher\_type belongs to “Purchase Invoice”.
      - Set d at “bill\_no” from Platform.db.get\_value(d.voucher\_type, d.voucher\_no, “bill\_no”).
  - If args.get(“party\_type”) differs from “Employee”.
    - Set negative\_outstanding\_invoices from get\_negative\_outstanding\_invoices(args.get(“party\_type”), args.get(“party”), args.get(“party\_account”), party\_account\_currency, condition = condition, …).
- Set orders\_to\_be\_billed from list().
- If args.get(“get\_orders\_to\_be\_billed”).
  - Set orders\_to\_be\_billed from get\_orders\_to\_be\_billed(args.get(“posting\_date”), args.get(“party\_type”), args.get(“party”), args.get(“company”), filters = args, …).
  - Set orders\_to\_be\_billed from split\_refdocs\_based\_on\_payment\_terms(orders\_to\_be\_billed, args.get(“company”)).
- Set data from ((negative\_outstanding\_invoices + outstanding\_invoices) + orders\_to\_be\_billed).
- If not data.
  - If (args.get(“get\_outstanding\_invoices”) and args.get(“get\_orders\_to\_be\_billed”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in args.get(“get\_outstanding\_invoices”) → args.get(“get\_orders\_to\_be\_billed”).
    - Set ref\_document\_type from “invoices or orders”.
  - Otherwise.
    - If args.get(“get\_outstanding\_invoices”).
      - Set ref\_document\_type from “invoices”.
    - Otherwise.
      - If args.get(“get\_orders\_to\_be\_billed”).
        - Set ref\_document\_type from “orders”.
  - If not validate.
    - Evaluate Platform.msgprint(translated “No outstanding {0} found for the {1} {2} which qualify the filters you have specified.”.format(translated ref\_document\_type, translated nested operand in the contract.get(“par ….
- Return data.

**Values supplied outside this operation** effective access from Platform.has\_permission(args at “party\_type”, “read”, party\_to\_check, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, args.get(“company”), “default\_currency”) · selected callable from Platform.get\_hooks(“invoice\_doctypes”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1445) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L32)

<a id="op-2b612abb1ec79c"></a>
### Split refdocs based on payment terms

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_split_refdocs_based_on_payment_terms`

**Inputs** refdocs, company.

**Declared result** list.

**Record and data access** read entry.voucher\_type via get\_value.

**State and service calls** msgprint with translated “Splitting {0} {1} into {2} rows as per Payment Terms”.format(translated entry.voucher\_type, Platform.bold(entry.voucher\_no), len(split\_rows)).

**Explicit results** outstanding\_refdoc\_after\_split.

**Local steps**

- Set exc\_rates from get\_currency\_data(refdocs, company).
- Set outstanding\_refdoc\_after\_split from list().
- For each entry in refdocs.
  - If entry.voucher\_type belongs to list(“Sales Invoice”, “Purchase Invoice”, “Sales Order”, “Purchase Order”).
    - If payment\_term\_template bound to Platform.db.get\_value(entry.voucher\_type, entry.voucher\_no, “payment\_terms\_template”).
      - Set split\_rows from get\_split\_invoice\_rows(entry, payment\_term\_template, exc\_rates).
      - If not split\_rows.
        - Continue with the next iteration or loop test.
      - <a id="op-2b612abb1ec79c-guard-15"></a>If len(split\_rows) &gt; 1.
        - Evaluate Platform.msgprint(translated “Splitting {0} {1} into {2} rows as per Payment Terms”.format(translated entry.voucher\_type, Platform.bold(entry.voucher\_no), len(split\_rows)), alert = true).
      - Update outstanding\_refdoc\_after\_split using + split\_rows.
      - Continue with the next iteration or loop test.
  - Evaluate outstanding\_refdoc\_after\_split.append(entry).
- Return outstanding\_refdoc\_after\_split.

**Derived branch illustrations**

- At the comparison len(split\_rows) &gt; 1, length of split\_rows = 2 selects the branch that requests a message with translated “Splitting {0} {1} into {2} rows as per Payment Terms”.format(translated entry.voucher\_type, Platform.bold(entry.voucher\_n …. With length of split\_rows = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-2b612abb1ec79c-guard-15)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0080.json#L4126) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1542) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L129)

<a id="op-94fcbdf57689cf"></a>
### Get currency data

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_currency_data`

**Inputs** outstanding\_refdocs, company = no value.

**Declared result** dict.

**Record and data access** read “Company” via get\_value · read doctype via get\_all.

**Explicit results** exc\_rates.

**Local steps**

- Set exc\_rates from Platform.\_dict().
- Set company\_currency from Platform.db.get\_value(“Company”, company, “default\_currency”) when company, otherwise no value.
  - Value choice on company — true gives Platform.db.get\_value(“Company”, company, “default\_currency”), false gives no value.
- For each doctype in list(“Sales Invoice”, “Purchase Invoice”, “Sales Order”, “Purchase Order”).
  - Set refdoc from list of x.voucher\_no for x drawn from outstanding\_refdocs where x.voucher\_type equals doctype.
    - Draw x from outstanding\_refdocs, keep a combination only if (x.voucher\_type equals doctype).
  - If not refdoc.
    - Continue with the next iteration or loop test.
  - For each x in Platform.db.get\_all(doctype, filters = mapping(“name” → list(“in”, refdoc)), fields = list(“name”, “currency”, “conversion\_rate”, “party\_account\_currency”)).
    - Set exc\_rates at x.name from Platform.\_dict(conversion\_rate = x.conversion\_rate, currency = x.currency, party\_account\_currency = x.party\_account\_currency, company\_currency = company\_currency).
- Return exc\_rates.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L23)

<a id="op-7b2cd28f0751e8"></a>
### Get split invoice rows

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_split_invoice_rows`

**Inputs** invoice, payment\_term\_template, exc\_rates.

**Declared result** list.

**Record and data access** read “Payment Terms Template” via get\_value · read “Payment Schedule” via get\_all.

**Explicit results** list(invoice) · split\_rows.

**Local steps**

- Set split\_rows from list().
- Set allocate\_payment\_based\_on\_payment\_terms from Platform.db.get\_value(“Payment Terms Template”, payment\_term\_template, “allocate\_payment\_based\_on\_payment\_terms”).
- If not allocate\_payment\_based\_on\_payment\_terms.
  - Return list(invoice).
- Set payment\_schedule from Platform.get\_all(“Payment Schedule”, filters = mapping(“parent” → invoice.voucher\_no), fields = list(“\*”), order\_by = “due\_date”).
- For each payment\_term in payment\_schedule.
  - If payment\_term.outstanding ≤ 0.1.
    - Continue with the next iteration or loop test.
  - Set doc\_details from exc\_rates.get(payment\_term.parent, no value).
  - Set is\_multi\_currency\_acc from (doc\_details.currency differs from doc\_details.company\_currency and doc\_details.party\_account\_currency differs from doc\_details.company\_currency).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc\_details.currency differs from doc\_details.company\_currency → doc\_details.party\_account\_currency differs from doc\_details.company\_currency.
  - Set payment\_term\_outstanding from flt(payment\_term.outstanding).
  - If not is\_multi\_currency\_acc.
    - Set payment\_term\_outstanding from (doc\_details.conversion\_rate × flt(payment\_term.outstanding)).
  - Evaluate split\_rows.append(Platform.\_dict(mapping(“due\_date” → invoice.due\_date, “currency” → invoice.currency, “voucher\_no” → invoice.voucher\_no, “voucher\_type” → invoice.voucher\_type, …))).
    - Value choice on payment\_term\_outstanding — true gives payment\_term\_outstanding, false gives invoice.outstanding\_amount.
- Return split\_rows.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L23) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1453) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L40)

<a id="op-1e9a3ae2674140"></a>
### Get orders to be billed

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_orders_to_be_billed`

**Inputs** posting\_date, party\_type, party, company, party\_account\_currency, company\_currency, cost\_center = no value, filters = no value.

**Record and data access** execute query text (SELECT).format(expanded names mapping(“rounded\_total\_field” → rounded\_total\_field, “grand\_total\_field” → grand\_total\_field, “voucher\_type” → voucher\_type, “party\_type” → scrub(party\_type), …)).

**Explicit results** list() · order\_list.

**Local steps**

- Set voucher\_type from no value.
- If party\_type equals “Customer”.
  - Set voucher\_type from “Sales Order”.
- Otherwise.
  - If party\_type equals “Supplier”.
    - Set voucher\_type from “Purchase Order”.
- If not voucher\_type.
  - Return list().
- Set condition from empty text.
- Set active\_dimensions from get\_dimensions(true) at 0.
- For each dim in active\_dimensions.
  - If filters.get(dim.fieldname).
    - Update condition using + formatted text  and {dim.fieldname}={Platform.db.escape(filters.get(dim.fieldname))}.
- If party\_account\_currency equals company\_currency.
  - Set grand\_total\_field from “base\_grand\_total”.
  - Set rounded\_total\_field from “base\_rounded\_total”.
- Otherwise.
  - Set grand\_total\_field from “grand\_total”.
  - Set rounded\_total\_field from “rounded\_total”.
- Set orders from Platform.db.sql(query text (SELECT).format(expanded names mapping(“rounded\_total\_field” → rounded\_total\_field, “grand\_total\_field” → grand\_total\_field, “voucher\_type” → voucher\_type, “party\_type” → scrub(p ….
- Set order\_list from list().
- For each d in orders.
  - If (filters and filters.get(“outstanding\_amt\_greater\_than”) and filters.get(“outstanding\_amt\_less\_than”) and not flt(filters.get(“outstanding\_amt\_greater\_than”)) ≤ flt(d.outstanding\_amount) ≤ flt(filters.get( ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.get(“outstanding\_amt\_greater\_than”) → filters.get(“outstanding\_amt\_less\_than”) → not flt(filters.get(“outstanding\_amt\_greater\_than”)) ≤ flt(d.outstanding\_amount) ≤ flt(filters.get(“outstanding\_amt\_less\_than”)).
    - Compare adjacent operands in order, stopping at the first false comparison in flt(filters.get(“outstanding\_amt\_greater\_than”)) ≤ flt(d.outstanding\_amount) ≤ flt(filters.get(“outstanding\_amt\_less\_than”)).
    - Continue with the next iteration or loop test.
  - Set d at “voucher\_type” from voucher\_type.
  - Set d at “exchange\_rate” from get\_exchange\_rate(party\_account\_currency, company\_currency, posting\_date).
  - Evaluate order\_list.append(d).
- Return order\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1441) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L28)

<a id="op-a0e99f7ece7e67"></a>
### Get negative outstanding invoices

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_negative_outstanding_invoices`

**Inputs** party\_type, party, party\_account, party\_account\_currency, company\_currency, cost\_center = no value, condition = no value.

**Record and data access** execute query text (SELECT).format\_map(mapping(“supplier\_condition” → supplier\_condition, “condition” → condition, “rounded\_total\_field” → rounded\_total\_field, “grand\_total\_field” → grand\_total\_field, …)).

**Explicit results** list() · Platform.db.sql(query text (SELECT).format\_map(mapping(“supplier\_condition” → supplier\_condition, “condition” → condition, “rounded\_total\_field” → rounded\_total\_field, “grand\_total\_field” → grand\_total\_fie ….

**Local steps**

- If party\_type does not belong to list(“Customer”, “Supplier”).
  - Return list().
- Set voucher\_type from “Sales Invoice” when party\_type equals “Customer”, otherwise “Purchase Invoice”.
  - Value choice on party\_type equals “Customer” — true gives “Sales Invoice”, false gives “Purchase Invoice”.
- Set account from “debit\_to” when voucher\_type equals “Sales Invoice”, otherwise “credit\_to”.
  - Value choice on voucher\_type equals “Sales Invoice” — true gives “debit\_to”, false gives “credit\_to”.
- Set supplier\_condition from empty text.
- If voucher\_type equals “Purchase Invoice”.
  - Set supplier\_condition from “and (release\_date is null or release\_date &lt;= CURRENT\_DATE)”.
- If party\_account\_currency equals company\_currency.
  - Set grand\_total\_field from “base\_grand\_total”.
  - Set rounded\_total\_field from “base\_rounded\_total”.
- Otherwise.
  - Set grand\_total\_field from “grand\_total”.
  - Set rounded\_total\_field from “rounded\_total”.
- Return Platform.db.sql(query text (SELECT).format\_map(mapping(“supplier\_condition” → supplier\_condition, “condition” → condition, “rounded\_total\_field” → rounded\_total\_field, “grand\_total\_field” → grand\_total\_fie ….
  - Value choice on party\_type equals “Customer” — true gives “debit\_to”, false gives “credit\_to”.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L14) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1439) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L26)

<a id="op-3ac5d9e4a36b1b"></a>
### Get party details

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_party_details`

**Inputs** company, party\_type, party, date, cost\_center = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read party\_type via exists · read party\_type via get\_value.

**Explicit results** mapping(“party\_account” → party\_account, “party\_name” → party\_name, “party\_account\_currency” → account\_currency, “party\_bank\_account” → party\_bank\_account, …).

**Explicit failure paths** validation helper — translated “{0} {1} does not exist”.format(translated party\_type, party).

**Local steps**

- Set bank\_account from empty text.
- Set party\_bank\_account from empty text.
- If not Platform.db.exists(party\_type, party).
  - Call the validation error handler Platform.throw(translated “{0} {1} does not exist”.format(translated party\_type, party)).
- Set ptype from “select” when Platform.only\_has\_select\_perm(party\_type), otherwise “read”.
  - Value choice on Platform.only\_has\_select\_perm(party\_type) — true gives “select”, false gives “read”.
- Set party\_to\_check from no value when has\_ignored\_field(“Payment Entry”, party\_type), otherwise party.
  - Value choice on has\_ignored\_field(“Payment Entry”, party\_type) — true gives no value, false gives party.
- Evaluate Platform.has\_permission(party\_type, ptype, party\_to\_check, throw = true).
- Evaluate validate\_party\_company(party\_type, party, company).
- Set party\_account from get\_party\_account(party\_type, party, company).
- Set account\_currency from get\_account\_currency(party\_account).
- Set \_party\_name from Platform.get\_meta(party\_type).get\_title\_field().
- Set party\_name from Platform.db.get\_value(party\_type, party, \_party\_name).
- If party\_type belongs to list(“Customer”, “Supplier”).
  - Set party\_bank\_account from get\_party\_bank\_account(party\_type, party).
  - Set bank\_account from get\_default\_company\_bank\_account(company, party\_type, party, ignore\_permissions = false).
- Return mapping(“party\_account” → party\_account, “party\_name” → party\_name, “party\_account\_currency” → account\_currency, “party\_bank\_account” → party\_bank\_account, …).

**Values supplied outside this operation** effective access from Platform.has\_permission(party\_type, ptype, party\_to\_check, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L19) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1447) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L34)

<a id="op-566b35b02086f3"></a>
### Get account details

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_account_details`

**Inputs** account, date, cost\_center = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Account” via get\_list · read “Account” via get\_cached\_value.

**Explicit results** Platform.\_dict(mapping(“account\_currency” → get\_account\_currency(account), “account\_type” → Platform.get\_cached\_value(“Account”, account, “account\_type”))).

**Explicit failure paths** validation helper — translated “Account: {0} is not permitted under Payment Entry”.format(account).

**Local steps**

- Evaluate Platform.has\_permission(“Payment Entry”, throw = true).
- Set account\_list from Platform.get\_list(“Account”, mapping(“name” → account), reference\_doctype = “Payment Entry”, limit = 1).
- If not account\_list.
  - Call the validation error handler Platform.throw(translated “Account: {0} is not permitted under Payment Entry”.format(account)).
- Return Platform.\_dict(mapping(“account\_currency” → get\_account\_currency(account), “account\_type” → Platform.get\_cached\_value(“Account”, account, “account\_type”))).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Entry”, throw = true) · configured or stored value from Platform.get\_cached\_value(“Account”, account, “account\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L10) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1433) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L20)

<a id="op-3f56307456c46e"></a>
### Get company defaults

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_company_defaults`

**Inputs** company.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** Platform.get\_cached\_value(“Company”, company, fields, as\_dict = 1).

**Local steps**

- Evaluate Platform.has\_permission(“Company”, doc = company, throw = true).
- Set fields from list(“write\_off\_account”, “exchange\_gain\_loss\_account”, “cost\_center”).
- Return Platform.get\_cached\_value(“Company”, company, fields, as\_dict = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(“Company”, doc = company, throw = true) · configured or stored value from Platform.get\_cached\_value(“Company”, company, fields, as\_dict = 1).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L11) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L22)

<a id="op-82a7539f256439"></a>
### Get journal entry exchange rate

`operation_enterprise_binding_enterprise_accounts_doctype_payment_entry_payment_entry_get_journal_entry_exchange_rate`

**Inputs** voucher\_no, party\_type, party, account\_currency, party\_account = no value.

**Record and data access** read “Journal Entry Account” via get\_all.

**Explicit results** (sum(generator of (row.debit − row.credit) for row drawn from rows) ÷ amount) when amount, otherwise 1.

**Local steps**

- Evaluate Platform.has\_permission(“Journal Entry”, “read”, voucher\_no, throw = true).
- Set filters from mapping(“parent” → voucher\_no, “party\_type” → party\_type, “party” → party, “account\_currency” → account\_currency).
- If party\_account.
  - Set filters at “account” from party\_account.
- Set rows from Platform.get\_all(“Journal Entry Account”, filters = filters, or\_filters = list(list(“reference\_type”, “is”, “not set”), list(“reference\_type”, “in”, get\_advance\_payment\_doctypes())), fields = list(“debit”, ….
- Set amount from sum(generator of (row.debit\_in\_account\_currency − row.credit\_in\_account\_currency) for row drawn from rows).
  - Draw row from rows.
- Return (sum(generator of (row.debit − row.credit) for row drawn from rows) ÷ amount) when amount, otherwise 1.
  - Value choice on amount — true gives (sum(generator of (row.debit − row.credit) for row drawn from rows) ÷ amount), false gives 1.
  - Draw row from rows.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Journal Entry”, “read”, voucher\_no, throw = true).

**Boundaries to resolve** stored data, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L188) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L826)

<a id="op-96a97396b32ea1"></a>
### Get outstanding on journal entry

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_outstanding_on_journal_entry`

**Inputs** voucher\_no, party\_type, party.

**Explicit results** tuple(outstanding\_amount, total\_amount).

**Local steps**

- Set ple from Platform.qb.DocType(“Payment Ledger Entry”).
- Set outstanding from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.amount\_in\_account\_currency)).where((((nested operand in the contract equals nested operand in the co ….run().
- Set outstanding\_amount from outstanding at 0 at 0 when outstanding, otherwise 0.
  - Value choice on outstanding — true gives outstanding at 0 at 0, false gives 0.
- Set total from nested operand in the contract(nested operand in the contract).select(Sum(nested operand in the contract.amount\_in\_account\_currency)).where((((nested operand in the contract equals nested operand in the co ….run().
- Set total\_amount from total at 0 at 0 when total, otherwise 0.
  - Value choice on total — true gives total at 0 at 0, false gives 0.
- Return tuple(outstanding\_amount, total\_amount).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0081.json#L2119) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1444) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L31)

<a id="op-769660492c3c82"></a>
### Get reference details

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_reference_details`

**Inputs** reference\_doctype, reference\_name, party\_account\_currency, party\_type = no value, party = no value, party\_account = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Payment Entry” via get\_all · read “Party Type” via get\_value.

**Explicit results** res.

**Local steps**

- Set total\_amount, outstanding\_amount, exchange\_rate, account from no value.
- Evaluate Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).
- Set ref\_doc from Platform.get\_lazy\_doc(reference\_doctype, reference\_name).
- Set company\_currency from (ref\_doc.get(“company\_currency”) or Enterprise.get\_company\_currency(ref\_doc.company)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“company\_currency”) → Enterprise.get\_company\_currency(ref\_doc.company).
- Set account\_type from no value.
- Set payment\_type from no value.
- If reference\_doctype equals “Dunning”.
  - Set total\_amount, outstanding\_amount from ref\_doc.get(“dunning\_amount”).
  - Set exchange\_rate from 1.
- Otherwise.
  - If (reference\_doctype equals “Journal Entry” and ref\_doc.docstatus equals 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in reference\_doctype equals “Journal Entry” → ref\_doc.docstatus equals 1.
    - If ref\_doc.multi\_currency.
      - Set exchange\_rate from get\_journal\_entry\_exchange\_rate(reference\_name, party\_type, party, party\_account\_currency, …).
    - Otherwise.
      - Set exchange\_rate from 1.
    - Set tuple(outstanding\_amount, total\_amount) from get\_outstanding\_on\_journal\_entry(reference\_name, party\_type, party).
  - Otherwise.
    - If reference\_doctype equals “Payment Entry”.
      - If reverse\_payment\_details bound to Platform.db.get\_all(“Payment Entry”, filters = mapping(“name” → reference\_name), fields = list(“payment\_type”, “party\_type”)) at 0.
        - Set payment\_type from reverse\_payment\_details.payment\_type.
        - Set account\_type from Platform.db.get\_value(“Party Type”, reverse\_payment\_details.party\_type, “account\_type”).
      - Set exchange\_rate from 1.
    - Otherwise.
      - If reference\_doctype differs from “Journal Entry”.
        - If not total\_amount.
          - If party\_account\_currency equals company\_currency.
            - Set total\_amount from (ref\_doc.get(“base\_rounded\_total”) or ref\_doc.get(“rounded\_total”) or ref\_doc.get(“base\_grand\_total”) or ref\_doc.get(“grand\_total”)).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“base\_rounded\_total”) → ref\_doc.get(“rounded\_total”) → ref\_doc.get(“base\_grand\_total”) → ref\_doc.get(“grand\_total”).
            - Set exchange\_rate from 1.
          - Otherwise.
            - Set total\_amount from (ref\_doc.get(“rounded\_total”) or ref\_doc.get(“grand\_total”)).
              - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“rounded\_total”) → ref\_doc.get(“grand\_total”).
        - If not exchange\_rate.
          - Set exchange\_rate from (ref\_doc.get(“conversion\_rate”) or get\_exchange\_rate(party\_account\_currency, company\_currency, ref\_doc.posting\_date)).
            - Evaluate in order, stop at the first true operand, otherwise use the last operand in ref\_doc.get(“conversion\_rate”) → get\_exchange\_rate(party\_account\_currency, company\_currency, ref\_doc.posting\_date).
        - If reference\_doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
          - Set outstanding\_amount from ref\_doc.get(“outstanding\_amount”).
          - Set account from ref\_doc.get(“debit\_to”) when reference\_doctype equals “Sales Invoice”, otherwise ref\_doc.get(“credit\_to”).
            - Value choice on reference\_doctype equals “Sales Invoice” — true gives ref\_doc.get(“debit\_to”), false gives ref\_doc.get(“credit\_to”).
        - Otherwise.
          - Set outstanding\_amount from (flt(total\_amount) − flt(ref\_doc.get(“advance\_paid”))).
        - If reference\_doctype belongs to list(“Sales Order”, “Purchase Order”).
          - Set party\_type from “Customer” when reference\_doctype equals “Sales Order”, otherwise “Supplier”.
            - Value choice on reference\_doctype equals “Sales Order” — true gives “Customer”, false gives “Supplier”.
          - Set party\_field from “customer” when reference\_doctype equals “Sales Order”, otherwise “supplier”.
            - Value choice on reference\_doctype equals “Sales Order” — true gives “customer”, false gives “supplier”.
          - Set party from ref\_doc.get(party\_field).
          - Set account from get\_party\_account(party\_type, party, ref\_doc.company).
      - Otherwise.
        - Set exchange\_rate from get\_exchange\_rate(party\_account\_currency, company\_currency, ref\_doc.posting\_date).
- Set res from Platform.\_dict(mapping(“due\_date” → ref\_doc.get(“due\_date”), “total\_amount” → flt(total\_amount), “outstanding\_amount” → flt(outstanding\_amount), “exchange\_rate” → flt(exchange\_rate), …)).
- If account.
  - Evaluate res.update(mapping(“account” → account)).
- Return res.

**Values supplied outside this operation** effective access from Platform.has\_permission(reference\_doctype, “read”, reference\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1451) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L38)

<a id="op-266623a03d7e9c"></a>
### Get payment entry

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_payment_entry`

**Inputs** dt, dn, party\_amount = no value, bank\_account = no value, bank\_amount = no value, party\_type = no value, payment\_type = no value, reference\_date = no value, created\_from\_payment\_request = false.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from dt via get\_doc · read “Accounts Settings” via get\_single\_value · read “Bank Account” via get\_value · read “Account” via get\_value · read “Payment Terms Template” via get\_cached\_value.

**State and service calls** request new\_doc for “Payment Entry” · msgprint with translated “{0} is on hold till {1}”.format(doc.name, doc.release\_date).

**Explicit results** pe.

**Explicit failure paths** validation helper — translated “Dunning {0} has already been settled through Dunning {1}.”.format(dn, successor) · validation helper — translated “Can only make payment against unbilled {0}”.format(translated dt).

**Local steps**

- Evaluate Platform.has\_permission(“Payment Entry”, ptype = “create”, throw = true).
- Set doc from Platform.get\_doc(dt, dn).
- Evaluate doc.check\_permission().
- If (dt equals “Dunning” and successor bound to doc.get\_settled\_successor()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Dunning” → successor bound to doc.get\_settled\_successor().
  - Call the validation error handler Platform.throw(translated “Dunning {0} has already been settled through Dunning {1}.”.format(dn, successor)).
- Set over\_billing\_allowance from Platform.get\_single\_value(“Accounts Settings”, “over\_billing\_allowance”).
- If (dt belongs to tuple(“Sales Order”, “Purchase Order”) and flt(doc.per\_billed, 2) ≥ (100.0 + over\_billing\_allowance)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt belongs to tuple(“Sales Order”, “Purchase Order”) → flt(doc.per\_billed, 2) ≥ (100.0 + over\_billing\_allowance).
  - Call the validation error handler Platform.throw(translated “Can only make payment against unbilled {0}”.format(translated dt)).
- If not party\_type.
  - Set party\_type from set\_party\_type(dt).
- Set party\_account from set\_party\_account(dt, dn, doc, party\_type).
- Set party\_account\_currency from set\_party\_account\_currency(dt, party\_account, doc).
- If not payment\_type.
  - Set payment\_type from set\_payment\_type(dt, doc).
- Set tuple(grand\_total, outstanding\_amount) from set\_grand\_total\_and\_outstanding\_amount(party\_amount, dt, party\_account\_currency, doc).
- Set bank from get\_bank\_cash\_account(doc, bank\_account).
- If (party\_type belongs to list(“Customer”, “Supplier”) and not bank).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_type belongs to list(“Customer”, “Supplier”) → not bank.
  - Set party\_bank\_account from get\_party\_bank\_account(party\_type, doc.get(scrub(party\_type))).
  - If party\_bank\_account.
    - Set account from Platform.db.get\_value(“Bank Account”, party\_bank\_account, “account”).
    - Set bank from get\_bank\_cash\_account(doc, account).
- Set tuple(paid\_amount, received\_amount) from set\_paid\_amount\_and\_received\_amount(dt, party\_account\_currency, bank, outstanding\_amount, …).
- Set reference\_date from getdate(reference\_date).
- Set tuple(paid\_amount, received\_amount, discount\_amount, valid\_discounts) from apply\_early\_payment\_discount(paid\_amount, received\_amount, doc, party\_account\_currency, …).
- Set pe from Platform.new\_doc(“Payment Entry”).
- Set pe.payment\_type from payment\_type.
- Set pe.company from doc.company.
- Set pe.cost\_center from doc.get(“cost\_center”).
- Set pe.posting\_date from nowdate().
- Set pe.reference\_date from reference\_date.
- Set pe.mode\_of\_payment from doc.get(“mode\_of\_payment”).
- Set pe.party\_type from party\_type.
- Set pe.party from doc.get(scrub(party\_type)).
- Set pe.contact\_person from doc.get(“contact\_person”).
- Evaluate complete\_contact\_details(pe).
- Evaluate pe.ensure\_supplier\_is\_not\_blocked().
- Set pe.paid\_from from party\_account when payment\_type equals “Receive”, otherwise bank.account.
  - Value choice on payment\_type equals “Receive” — true gives party\_account, false gives bank.account.
- Set pe.paid\_to from party\_account when payment\_type equals “Pay”, otherwise bank.account.
  - Value choice on payment\_type equals “Pay” — true gives party\_account, false gives bank.account.
- Set pe.paid\_from\_account\_currency from party\_account\_currency when payment\_type equals “Receive”, otherwise bank.account\_currency.
  - Value choice on payment\_type equals “Receive” — true gives party\_account\_currency, false gives bank.account\_currency.
- Set pe.paid\_to\_account\_currency from party\_account\_currency when payment\_type equals “Pay”, otherwise bank.account\_currency.
  - Value choice on payment\_type equals “Pay” — true gives party\_account\_currency, false gives bank.account\_currency.
- Set pe.paid\_from\_account\_type from Platform.db.get\_value(“Account”, pe.paid\_from, “account\_type”).
- Set pe.paid\_to\_account\_type from Platform.db.get\_value(“Account”, pe.paid\_to, “account\_type”).
- Set pe.paid\_amount from paid\_amount.
- Set pe.received\_amount from received\_amount.
- Set pe.letter\_head from doc.get(“letter\_head”).
- Set pe.bank\_account from Platform.db.get\_value(“Bank Account”, mapping(“is\_company\_account” → 1, “is\_default” → 1, “company” → doc.company, “disabled” → 0), “name”).
- If dt belongs to list(“Purchase Order”, “Sales Order”, “Sales Invoice”, “Purchase Invoice”).
  - Set pe.project from (doc.get(“project”) or reduce(deferred anonymous expression, list of x.get(“project”) for x drawn from doc.get(“items”), no value)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“project”) → reduce(deferred anonymous expression, list of x.get(“project”) for x drawn from doc.get(“items”), no value).
    - Draw x from doc.get(“items”).
- If pe.party\_type belongs to list(“Customer”, “Supplier”).
  - Set bank\_account from get\_party\_bank\_account(pe.party\_type, pe.party).
  - Evaluate pe.set(“party\_bank\_account”, bank\_account).
  - Evaluate pe.set\_bank\_account\_data().
- If (doc.doctype equals “Purchase Invoice” and doc.invoice\_is\_blocked()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype equals “Purchase Invoice” → doc.invoice\_is\_blocked().
  - Evaluate Platform.msgprint(translated “{0} is on hold till {1}”.format(doc.name, doc.release\_date)).
- Otherwise.
  - If (doc.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”, “Purchase Order”, “Sales Order”) and Platform.get\_cached\_value(“Payment Terms Template”, doc.payment\_terms\_template, “allocate\_payment\_bas ….
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype belongs to tuple(“Sales Invoice”, “Purchase Invoice”, “Purchase Order”, “Sales Order”) → Platform.get\_cached\_value(“Payment Terms Template”, doc.payment\_terms\_template, “allocate\_payment\_based\_on\_payment\_terms”).
    - For each reference in get\_reference\_as\_per\_payment\_terms(doc.payment\_schedule, dt, dn, doc, …).
      - Evaluate pe.append(“references”, reference).
  - Otherwise.
    - If dt equals “Dunning”.
      - For each tuple(overdue\_payment, outstanding) in doc.get\_unpaid\_overdue\_payments(in\_account\_currency = true).
        - Evaluate pe.append(“references”, mapping(“reference\_doctype” → “Sales Invoice”, “reference\_name” → overdue\_payment.sales\_invoice, “payment\_term” → overdue\_payment.payment\_term, “due\_date” → overdue\_payment.due\_date, …)).
      - If unpaid\_dunning\_amount bound to doc.get\_unpaid\_base\_dunning\_amount() &gt; 0.
        - Evaluate pe.append(“deductions”, mapping(“account” → doc.income\_account, “cost\_center” → doc.cost\_center, “amount” → (negative 1 × unpaid\_dunning\_amount), “description” → translated “Interest and/or dunning fee”, …)).
    - Otherwise.
      - Evaluate pe.append(“references”, mapping(“reference\_doctype” → dt, “reference\_name” → dn, “bill\_no” → doc.get(“bill\_no”), “due\_date” → doc.get(“due\_date”), …)).
- Evaluate pe.setup\_party\_account\_field().
- Evaluate pe.set\_missing\_values().
- Evaluate pe.set\_missing\_ref\_details().
- Evaluate update\_accounting\_dimensions(pe, doc).
- If (party\_account and bank).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in party\_account → bank.
  - If discount\_amount.
    - Set base\_total\_discount\_loss from 0.
    - If Platform.get\_single\_value(“Accounts Settings”, “book\_tax\_discount\_loss”).
      - Set base\_total\_discount\_loss from split\_early\_payment\_discount\_loss(pe, doc, valid\_discounts).
    - Evaluate set\_pending\_discount\_loss(pe, doc, discount\_amount, base\_total\_discount\_loss, …).
  - Evaluate pe.set\_exchange\_rate().
  - Evaluate pe.set\_amounts().
- If not created\_from\_payment\_request.
  - Evaluate allocate\_open\_payment\_requests\_to\_references(pe.references, pe.precision(“paid\_amount”)).
- Return pe.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Payment Entry”, ptype = “create”, throw = true), doc.check\_permission() · configured or stored value from Platform.get\_single\_value(“Accounts Settings”, “over\_billing\_allowance”), Platform.get\_cached\_value(“Payment Terms Template”, doc.payment\_terms\_template, “allocate\_payment\_based\_on\_payment\_terms”) and 1 further calls · clock or generated value from nowdate().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L20) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1448) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L35)

<a id="op-a05b87fdab0f20"></a>
### Get open payment requests for references

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_open_payment_remote_requests_for_references`

**Inputs** references = no value.

**Explicit results** no value · reference\_payment\_requests.

**Local steps**

- If not references.
  - Return no value.
- Set refs from set of tuple(row.reference\_doctype, row.reference\_name) for row drawn from references where (row.reference\_doctype and row.reference\_name and row.allocated\_amount).
  - Draw row from references, keep a combination only if ((row.reference\_doctype and row.reference\_name and row.allocated\_amount)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.reference\_doctype → row.reference\_name → row.allocated\_amount.
- If not refs.
  - Return no value.
- Set PR from Platform.qb.DocType(“Payment Request”).
- Set response from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.outstanding\_amount &gt; 0).orderby(Coalesce(PR.transaction\_date, PR.creation), order = Platform.qb.asc).run( ….
- If not response.
  - Return no value.
- Set reference\_payment\_requests from mapping().
- For each row in response.
  - Set key from tuple(row.reference\_doctype, row.reference\_name).
  - If key does not belong to reference\_payment\_requests.
    - Set reference\_payment\_requests at key from mapping(row.name → row.outstanding\_amount).
  - Otherwise.
    - Set reference\_payment\_requests at key at row.name from row.outstanding\_amount.
- Return reference\_payment\_requests.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1440) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L27)

<a id="op-67bfc4b5b627a8"></a>
### Allocate open payment requests to references

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_allocate_open_payment_remote_requests_to_references`

**Inputs** references = no value, precision = no value.

**State and service calls** request copy\_doc for row · call insert on references.

**Explicit results** no value.

**Local steps**

- If not references.
  - Return no value.
- Set references\_open\_payment\_requests from get\_open\_payment\_requests\_for\_references(references).
- If not references\_open\_payment\_requests.
  - Return no value.
- If not precision.
  - Set precision from references at 0.precision(“allocated\_amount”).
- Set row\_number from 1.
- Set MOVE\_TO\_NEXT\_ROW from 1.
- Set TO\_SKIP\_NEW\_ROW from 2.
- While row\_number ≤ len(references).
  - Set row from references at (row\_number − 1).
  - Set reference\_key from tuple(row.reference\_doctype, row.reference\_name).
  - Set row.idx from row\_number.
  - Set reference\_payment\_requests from references\_open\_payment\_requests.get(reference\_key).
  - If not reference\_payment\_requests.
    - Update row\_number using + MOVE\_TO\_NEXT\_ROW.
    - Continue with the next iteration or loop test.
  - Set tuple(payment\_request, pr\_outstanding\_amount) from next(iter(reference\_payment\_requests.items())).
  - Set allocated\_amount from row.allocated\_amount.
  - Set row.payment\_request from payment\_request.
  - If pr\_outstanding\_amount equals allocated\_amount.
    - Remove reference\_payment\_requests at payment\_request.
    - Update row\_number using + MOVE\_TO\_NEXT\_ROW.
  - Otherwise.
    - If pr\_outstanding\_amount &gt; allocated\_amount.
      - Update reference\_payment\_requests at payment\_request using − allocated\_amount.
      - Update row\_number using + MOVE\_TO\_NEXT\_ROW.
    - Otherwise.
      - Remove reference\_payment\_requests at payment\_request.
      - Set row.allocated\_amount from pr\_outstanding\_amount.
      - Set allocated\_amount from flt((allocated\_amount − pr\_outstanding\_amount), precision).
      - While allocated\_amount.
        - Set new\_row from Platform.copy\_doc(row).
        - Evaluate references.insert(row\_number, new\_row).
        - Set tuple(payment\_request, pr\_outstanding\_amount) from next(iter(reference\_payment\_requests.items()), tuple(no value, no value)).
        - Set new\_row.idx from (row\_number + 1).
        - Set new\_row.payment\_request from payment\_request.
        - Set new\_row.allocated\_amount from min(pr\_outstanding\_amount when pr\_outstanding\_amount, otherwise allocated\_amount, allocated\_amount).
          - Value choice on pr\_outstanding\_amount — true gives pr\_outstanding\_amount, false gives allocated\_amount.
        - If (not payment\_request or not pr\_outstanding\_amount).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in not payment\_request → not pr\_outstanding\_amount.
          - Update row\_number using + TO\_SKIP\_NEW\_ROW.
          - Leave the innermost loop without its normal-exhaustion alternative.
        - Otherwise.
          - If pr\_outstanding\_amount equals allocated\_amount.
            - Remove reference\_payment\_requests at payment\_request.
            - Update row\_number using + TO\_SKIP\_NEW\_ROW.
            - Leave the innermost loop without its normal-exhaustion alternative.
          - Otherwise.
            - If pr\_outstanding\_amount &gt; allocated\_amount.
              - Update reference\_payment\_requests at payment\_request using − allocated\_amount.
              - Update row\_number using + TO\_SKIP\_NEW\_ROW.
              - Leave the innermost loop without its normal-exhaustion alternative.
            - Otherwise.
              - Set allocated\_amount from flt((allocated\_amount − pr\_outstanding\_amount), precision).
              - Remove reference\_payment\_requests at payment\_request.
              - Update row\_number using + MOVE\_TO\_NEXT\_ROW.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L4348) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L18)

<a id="op-3d59748823bd72"></a>
### Update accounting dimensions

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_update_accounting_dimensions`

**Inputs** pe, doc.

**Local steps**

- Bind dependencies get\_accounting\_dimensions.
- For each dimension in get\_accounting\_dimensions().
  - Evaluate pe.set(dimension, doc.get(dimension)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L5427) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1543) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L130)

<a id="op-0c6c93e653c555"></a>
### Get bank cash account

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_get_bank_cash_account`

**Inputs** doc, bank\_account.

**Explicit results** bank.

**Local steps**

- Set bank from get\_default\_bank\_cash\_account(doc.company, “Bank”, mode\_of\_payment = doc.get(“mode\_of\_payment”), account = bank\_account, fetch\_balance = false).
- If not bank.
  - Set bank from get\_default\_bank\_cash\_account(doc.company, “Cash”, mode\_of\_payment = doc.get(“mode\_of\_payment”), account = bank\_account, fetch\_balance = false).
- Return bank.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L5540) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L21)

<a id="op-237c85c10d2630"></a>
### Set party type

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_party_type`

**Inputs** dt.

**Explicit results** party\_type.

**Local steps**

- If dt belongs to tuple(“Sales Invoice”, “Sales Order”, “Dunning”).
  - Set party\_type from “Customer”.
- Otherwise.
  - If dt belongs to tuple(“Purchase Invoice”, “Purchase Order”).
    - Set party\_type from “Supplier”.
- Return party\_type.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L5777) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1538) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L125)

<a id="op-f5975556c6be3d"></a>
### Set party account

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_party_account`

**Inputs** dt, dn, doc, party\_type.

**Explicit results** party\_account.

**Local steps**

- If dt equals “Sales Invoice”.
  - Set party\_account from (get\_party\_account\_based\_on\_invoice\_discounting(dn) or doc.debit\_to).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_party\_account\_based\_on\_invoice\_discounting(dn) → doc.debit\_to.
- Otherwise.
  - If dt equals “Purchase Invoice”.
    - Set party\_account from doc.credit\_to.
  - Otherwise.
    - Set party\_account from get\_party\_account(party\_type, doc.get(party\_type.lower()), doc.company).
- Return party\_account.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L5942) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1536) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L123)

<a id="op-6128f5483bed49"></a>
### Set party account currency

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_party_account_currency`

**Inputs** dt, party\_account, doc.

**Explicit results** party\_account\_currency.

**Local steps**

- If dt does not belong to tuple(“Sales Invoice”, “Purchase Invoice”).
  - Set party\_account\_currency from get\_account\_currency(party\_account).
- Otherwise.
  - Set party\_account\_currency from (doc.get(“party\_account\_currency”) or get\_account\_currency(party\_account)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“party\_account\_currency”) → get\_account\_currency(party\_account).
- Return party\_account\_currency.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L6182) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1537) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L124)

<a id="op-dd75535885cb64"></a>
### Set payment type

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_payment_type`

**Inputs** dt, doc.

**Explicit results** payment\_type.

**Local steps**

- If ((dt equals “Sales Order” or (dt equals “Sales Invoice” and doc.outstanding\_amount &gt; 0)) or (dt equals “Purchase Invoice” and doc.outstanding\_amount &lt; 0) or dt equals “Dunning”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (dt equals “Sales Order” or (dt equals “Sales Invoice” and doc.outstanding\_amount &gt; 0)) → (dt equals “Purchase Invoice” and doc.outstanding\_amount &lt; 0) → dt equals “Dunning”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dt equals “Sales Order” → (dt equals “Sales Invoice” and doc.outstanding\_amount &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Sales Invoice” → doc.outstanding\_amount &gt; 0.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in dt equals “Purchase Invoice” → doc.outstanding\_amount &lt; 0.
  - Set payment\_type from “Receive”.
- Otherwise.
  - Set payment\_type from “Pay”.
- Return payment\_type.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0082.json#L6361) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1539) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L126)

<a id="op-6d37bbe3378334"></a>
### Set grand total and outstanding amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_grand_total_and_outstanding_amount`

**Inputs** party\_amount, dt, party\_account\_currency, doc.

**Explicit results** tuple(grand\_total, outstanding\_amount).

**Local steps**

- Set grand\_total, outstanding\_amount from 0.
- If party\_amount.
  - Set grand\_total, outstanding\_amount from party\_amount.
- Otherwise.
  - If dt belongs to tuple(“Sales Invoice”, “Purchase Invoice”).
    - If party\_account\_currency equals doc.company\_currency.
      - Set grand\_total from (doc.base\_rounded\_total or doc.base\_grand\_total).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.base\_rounded\_total → doc.base\_grand\_total.
    - Otherwise.
      - Set grand\_total from (doc.rounded\_total or doc.grand\_total).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.rounded\_total → doc.grand\_total.
    - Set outstanding\_amount from doc.outstanding\_amount.
  - Otherwise.
    - If dt equals “Dunning”.
      - Set grand\_total from sum(generator of outstanding for tuple(row, outstanding) drawn from doc.get\_unpaid\_overdue\_payments(in\_account\_currency = true)).
        - Draw tuple(row, outstanding) from doc.get\_unpaid\_overdue\_payments(in\_account\_currency = true).
      - Update grand\_total using + doc.get\_unpaid\_dunning\_amount() when party\_account\_currency equals doc.currency, otherwise doc.get\_unpaid\_base\_dunning\_amount().
        - Value choice on party\_account\_currency equals doc.currency — true gives doc.get\_unpaid\_dunning\_amount(), false gives doc.get\_unpaid\_base\_dunning\_amount().
      - Set outstanding\_amount from grand\_total.
    - Otherwise.
      - If party\_account\_currency equals doc.company\_currency.
        - Set grand\_total from flt((doc.get(“base\_rounded\_total”) or doc.get(“base\_grand\_total”))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“base\_rounded\_total”) → doc.get(“base\_grand\_total”).
      - Otherwise.
        - Set grand\_total from flt((doc.get(“rounded\_total”) or doc.get(“grand\_total”))).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“rounded\_total”) → doc.get(“grand\_total”).
      - Set outstanding\_amount from (doc.get(“outstanding\_amount”) or (grand\_total − flt(doc.advance\_paid))).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“outstanding\_amount”) → (grand\_total − flt(doc.advance\_paid)).
- Return tuple(grand\_total, outstanding\_amount).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L49) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1534) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L121)

<a id="op-2c847b28594aa2"></a>
### Set paid amount and received amount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_set_paid_amount_and_received_amount`

**Inputs** dt, party\_account\_currency, bank, outstanding\_amount, payment\_type, bank\_amount, doc.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** tuple(paid\_amount, received\_amount).

**Local steps**

- Set paid\_amount, received\_amount from 0.
- If party\_account\_currency equals bank.account\_currency.
  - Set paid\_amount, received\_amount from abs(outstanding\_amount).
- Otherwise.
  - Set paid\_amount from abs(outstanding\_amount).
  - If bank\_amount.
    - Set received\_amount from bank\_amount.
  - Otherwise.
    - Set company\_currency from Platform.get\_cached\_value(“Company”, doc.get(“company”), “default\_currency”).
    - If (bank and company\_currency differs from bank.account\_currency).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in bank → company\_currency differs from bank.account\_currency.
      - Set conversion\_rate from get\_exchange\_rate(bank.account\_currency, party\_account\_currency).
      - Set received\_amount from (paid\_amount ÷ conversion\_rate).
    - Otherwise.
      - Set conversion\_rate from get\_exchange\_rate(doc.get(“currency”, company\_currency), company\_currency).
      - Set received\_amount from (paid\_amount × conversion\_rate).
  - If payment\_type equals “Pay”.
    - Set tuple(paid\_amount, received\_amount) from tuple(received\_amount, paid\_amount).
- Return tuple(paid\_amount, received\_amount).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, doc.get(“company”), “default\_currency”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0083.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1535) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L122)

<a id="op-59e1a06f4e6578"></a>
### Apply early payment discount

`operation_enterprise_accounts_record_definitions_payment_entry_business_behavior_apply_early_payment_discount`

**Inputs** paid\_amount, received\_amount, doc, party\_account\_currency, reference\_date.

**State and service calls** msgprint with translated “Discount of {} applied as per Payment Term”.format(money).

**Explicit results** tuple(paid\_amount, received\_amount, total\_discount, valid\_discounts).

**Local steps**

- Set total\_discount from 0.
- Set valid\_discounts from list().
- Set eligible\_for\_payments from list(“Sales Order”, “Sales Invoice”, “Purchase Order”, “Purchase Invoice”).
- Set has\_payment\_schedule from (hasattr(doc, “payment\_schedule”) and doc.payment\_schedule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(doc, “payment\_schedule”) → doc.payment\_schedule.
- Set is\_multi\_currency from party\_account\_currency differs from doc.company\_currency.
- If (doc.doctype belongs to eligible\_for\_payments and has\_payment\_schedule).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.doctype belongs to eligible\_for\_payments → has\_payment\_schedule.
  - For each term in doc.payment\_schedule.
    - If (term.outstanding and not term.discounted\_amount and term.discount and reference\_date ≤ term.discount\_date).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in term.outstanding → not term.discounted\_amount → term.discount → reference\_date ≤ term.discount\_date.
      - If term.discount\_type equals “Percentage”.
        - Set grand\_total from doc.get(“grand\_total”) when is\_multi\_currency, otherwise doc.get(“base\_grand\_total”).
          - Value choice on is\_multi\_currency — true gives doc.get(“grand\_total”), false gives doc.get(“base\_grand\_total”).
        - Set discount\_amount from (flt(grand\_total) × (term.discount ÷ 100)).
      - Otherwise.
        - Set discount\_amount from term.discount.
      - Set conversion\_rate from doc.get(“conversion\_rate”, 1) when is\_multi\_currency, otherwise 1.
        - Value choice on is\_multi\_currency — true gives doc.get(“conversion\_rate”, 1), false gives 1.
      - Set discount\_amount\_in\_foreign\_currency from (discount\_amount × conversion\_rate).
      - If doc.doctype equals “Sales Invoice”.
        - Update paid\_amount using − discount\_amount.
        - Update received\_amount using − discount\_amount\_in\_foreign\_currency.
      - Otherwise.
        - Update received\_amount using − discount\_amount.
        - Update paid\_amount using − discount\_amount\_in\_foreign\_currency.
      - Evaluate valid\_discounts.append(mapping(“type” → term.discount\_type, “discount” → term.discount)).
      - Update total\_discount using + discount\_amount.
  - If total\_discount.
    - Set currency from doc.get(“currency”) when is\_multi\_currency, otherwise doc.company\_currency.
      - Value choice on is\_multi\_currency — true gives doc.get(“currency”), false gives doc.company\_currency.
    - Set money from Platform.utils.fmt\_money(total\_discount, currency = currency).
    - Evaluate Platform.msgprint(translated “Discount of {} applied as per Payment Term”.format(money), alert = 1).
- Return tuple(paid\_amount, received\_amount, total\_discount, valid\_discounts).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0003.json#L9) · [Binding](../../../current-decisions/enterprise/bindings-001.tsv#L1432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L19)
