# Accounting and settlement · operations 90

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Process statement of accounts

[Record definition](../../../../data/record-types/process_statement_of_accounts.json)

<a id="op-2fc6a8f53f8c6a"></a>
### Get report pdf

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_report_portable_document`

**Inputs** doc, consolidated = true.

**Explicit results** false · get\_pdf(result, mapping(“orientation” → doc.orientation)) · statement\_dict.

**Local steps**

- Set statement\_dict from get\_statement\_dict(doc).
- If not bool(statement\_dict).
  - Return false.
- Otherwise.
  - If consolidated.
    - Set delimiter from text in the contract when doc.include\_break, otherwise empty text.
      - Value choice on doc.include\_break — true gives text in the contract, false gives empty text.
    - Set result from delimiter.join(list(statement\_dict.values())).
    - Return get\_pdf(result, mapping(“orientation” → doc.orientation)).
  - Otherwise.
    - For each tuple(customer, statement\_html) in statement\_dict.items().
      - Set statement\_dict at customer from get\_pdf(statement\_html, mapping(“orientation” → doc.orientation)).
    - Return statement\_dict.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L757) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L870)

<a id="op-6313d275fdf65a"></a>
### Get statement dict

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_statement_mapping`

**Inputs** doc, get\_statement\_dict = false.

**Record and data access** resolve a document from “Customer” via get\_doc.

**Explicit results** statement\_dict.

**Local steps**

- Set statement\_dict from mapping().
- Set ageing from empty text.
- For each entry in doc.customers.
  - If doc.include\_ageing.
    - Set ageing from set\_ageing(doc, entry).
  - Set tax\_id from Platform.get\_doc(“Customer”, entry.customer).tax\_id.
  - Set presentation\_currency from (doc.currency or get\_party\_account\_currency(“Customer”, entry.customer, doc.company) or get\_company\_currency(doc.company)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.currency → get\_party\_account\_currency(“Customer”, entry.customer, doc.company) → get\_company\_currency(doc.company).
  - Set filters from get\_common\_filters(doc).
  - If doc.ignore\_exchange\_rate\_revaluation\_journals.
    - Evaluate filters.update(mapping(“ignore\_err” → true)).
  - If doc.ignore\_cr\_dr\_notes.
    - Evaluate filters.update(mapping(“ignore\_cr\_dr\_notes” → true)).
  - If doc.report equals “General Ledger”.
    - Evaluate filters.update(get\_gl\_filters(doc, entry, tax\_id, presentation\_currency)).
    - Set tuple(col, res) from get\_soa(filters).
    - <a id="op-6313d275fdf65a-guard-26"></a>If len(res) equals 3.
      - Continue with the next iteration or loop test.
    - For each x in list(0, negative 2, negative 1).
      - Set res at x at “account” from (res at x at “account” or empty text).replace(“'”, empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in res at x at “account” → empty text.
  - Otherwise.
    - Evaluate filters.update(get\_ar\_filters(doc, entry)).
    - Set ar\_res from get\_ar\_soa(filters).
    - Set tuple(col, res) from tuple(ar\_res at 0, ar\_res at 1).
    - If not res.
      - Continue with the next iteration or loop test.
  - Set statement\_dict at entry.customer from list(res, ageing) when get\_statement\_dict, otherwise get\_html(doc, filters, entry, col, …).
    - Value choice on get\_statement\_dict — true gives list(res, ageing), false gives get\_html(doc, filters, entry, col, …).
- Return statement\_dict.

**Derived branch illustrations**

- At the comparison len(res) equals 3, length of res = 3 selects the branch that continues with the next loop iteration. With length of res = 4, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-6313d275fdf65a-guard-26)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L85) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L871)

<a id="op-c82933733a13ce"></a>
### Set ageing

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_set_ageing`

**Inputs** doc, entry.

**Explicit results** ageing.

**Local steps**

- Set ageing\_filters from Platform.\_dict(mapping(“company” → doc.company, “report\_date” → doc.to\_date when doc.report equals “General Ledger”, otherwise doc.posting\_date, “age\_as\_on” → “Report Date” when doc.report equals “General  ….
  - Value choice on doc.report equals “General Ledger” — true gives doc.to\_date, false gives doc.posting\_date.
  - Value choice on doc.report equals “General Ledger” — true gives “Report Date”, false gives “Today”.
- Set tuple(col1, ageing) from get\_ageing(ageing\_filters).
- If ageing.
  - Set ageing at 0 at “ageing\_based\_on” from doc.ageing\_based\_on.
- Return ageing.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L695) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L877)

<a id="op-1299ff9bc9b68d"></a>
### Get common filters

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_common_filters`

**Inputs** doc.

**Explicit results** Platform.\_dict(mapping(“company” → doc.company, “finance\_book” → doc.finance\_book when doc.finance\_book, otherwise no value, “account” → list(doc.account) when doc.account, otherwise no value, “cost\_center ….

**Local steps**

- Return Platform.\_dict(mapping(“company” → doc.company, “finance\_book” → doc.finance\_book when doc.finance\_book, otherwise no value, “account” → list(doc.account) when doc.account, otherwise no value, “cost\_center ….
  - Value choice on doc.finance\_book — true gives doc.finance\_book, false gives no value.
  - Value choice on doc.account — true gives list(doc.account), false gives no value.
  - Draw cc from doc.cost\_center.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L2269) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L862)

<a id="op-f0dd86e54a87e8"></a>
### Get gl filters

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_general_ledger_filters`

**Inputs** doc, entry, tax\_id, presentation\_currency.

**Explicit results** mapping(“from\_date” → doc.from\_date, “to\_date” → doc.to\_date, “party\_type” → “Customer”, “party” → list(entry.customer), …).

**Local steps**

- Return mapping(“from\_date” → doc.from\_date, “to\_date” → doc.to\_date, “party\_type” → “Customer”, “party” → list(entry.customer), …).
  - Value choice on entry.customer\_name — true gives list(entry.customer\_name), false gives no value.
  - Draw p from doc.project.
  - Value choice on tax\_id — true gives tax\_id, false gives no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L2479) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L868)

<a id="op-32e58582e61a63"></a>
### Get ar filters

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_accounts_receivable_filters`

**Inputs** doc, entry.

**Explicit results** mapping(“report\_date” → doc.posting\_date when doc.posting\_date, otherwise no value, “party\_type” → “Customer”, “party” → list(entry.customer), “customer\_name” → entry.customer\_name when entry.customer\_name ….

**Local steps**

- Return mapping(“report\_date” → doc.posting\_date when doc.posting\_date, otherwise no value, “party\_type” → “Customer”, “party” → list(entry.customer), “customer\_name” → entry.customer\_name when entry.customer\_name ….
  - Value choice on doc.posting\_date — true gives doc.posting\_date, false gives no value.
  - Value choice on entry.customer\_name — true gives entry.customer\_name, false gives no value.
  - Value choice on doc.payment\_terms\_template — true gives doc.payment\_terms\_template, false gives no value.
  - Value choice on doc.sales\_partner — true gives doc.sales\_partner, false gives no value.
  - Value choice on doc.sales\_person — true gives doc.sales\_person, false gives no value.
  - Value choice on doc.territory — true gives doc.territory, false gives no value.

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L2833) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L861)

<a id="op-f8fa59fb211809"></a>
### Get html

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_document_markup`

**Inputs** doc, filters, entry, col, res, ageing.

**Record and data access** read “Print Format” via get\_value · read “Terms and Conditions” via get\_value.

**Explicit results** html.

**Local steps**

- Set base\_template\_path from “Platform/www/printview.html”.
- Set template\_path from “Enterprise/accounts/doctype/process\_statement\_of\_accounts/process\_statement\_of\_accounts\_accounts\_receivable.html”.
- If doc.report equals “General Ledger”.
  - Set template\_path from “Enterprise/accounts/doctype/process\_statement\_of\_accounts/process\_statement\_of\_accounts.html”.
- Set process\_soa\_html from Platform.get\_hooks(“process\_soa\_html”).
- If (process\_soa\_html and process\_soa\_html.get(doc.report)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in process\_soa\_html → process\_soa\_html.get(doc.report).
  - Set template\_path from process\_soa\_html at doc.report at negative 1.
- If doc.print\_format.
  - Set tuple(custom\_html, custom\_css) from Platform.db.get\_value(“Print Format”, doc.print\_format, list(“html”, “css”)).
  - Set template\_path from formatted text &lt;style&gt;{custom\_css}&lt;/style&gt; {custom\_html}.
- If doc.letter\_head.
  - Bind dependencies get\_letter\_head.
  - Set letter\_head from get\_letter\_head(doc, 0).
  - If letter\_head.get(“content”).
    - Set letter\_head at “content” from Platform.render\_template(letter\_head at “content”, mapping(“doc” → doc)).
  - If letter\_head.get(“footer”).
    - Set letter\_head at “footer” from Platform.render\_template(letter\_head at “footer”, mapping(“doc” → doc)).
- Set html from Platform.render\_template(template\_path, mapping(“filters” → filters, “data” → res, “report” → mapping(“report\_name” → doc.report, “columns” → col), “ageing” → ageing at 0 when (doc.include\_ageing and agein ….
  - Value choice on (doc.include\_ageing and ageing) — true gives ageing at 0, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.include\_ageing → ageing.
  - Value choice on doc.letter\_head — true gives letter\_head, false gives no value.
  - Value choice on doc.terms\_and\_conditions — true gives Platform.db.get\_value(“Terms and Conditions”, doc.terms\_and\_conditions, “terms”), false gives no value.
- Set html from Platform.render\_template(base\_template\_path, mapping(“body” → html, “css” → get\_print\_style(), “title” → (“Statement For ” + entry.customer))).
- Return html.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“process\_soa\_html”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L83) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L867)

<a id="op-9c971e8bcf418c"></a>
### Get customers based on territory or customer group

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_customers_based_on_territory_or_customer_group`

**Inputs** customer\_collection, collection\_name.

**Record and data access** resolve a document from customer\_collection via get\_doc · read customer\_collection via get\_list · read “Customer” via get\_list.

**Explicit results** Platform.get\_list(“Customer”, fields = list(“name”, “customer\_name”, “email\_id”), filters = list(list(“disabled”, “=”, 0), list(fields\_dict at customer\_collection, “IN”, selected))).

**Local steps**

- Set fields\_dict from mapping(“Customer Group” → “customer\_group”, “Territory” → “territory”).
- Set collection from Platform.get\_doc(customer\_collection, collection\_name).
- Set selected from list of customer.name for customer drawn from Platform.get\_list(customer\_collection, filters = list(list(“lft”, “&gt;=”, collection.lft), list(“rgt”, “&lt;=”, collection.rgt)), fields = list(“name”), order\_by =  ….
  - Draw customer from Platform.get\_list(customer\_collection, filters = list(list(“lft”, “&gt;=”, collection.lft), list(“rgt”, “&lt;=”, collection.rgt)), fields = list(“name”), order\_by = “lft asc, rgt desc”).
- Return Platform.get\_list(“Customer”, fields = list(“name”, “customer\_name”, “email\_id”), filters = list(list(“disabled”, “=”, 0), list(fields\_dict at customer\_collection, “IN”, selected))).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L4050) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L866)

<a id="op-701e85c288e748"></a>
### Get customers based on sales person

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_customers_based_on_sales_person`

**Inputs** sales\_person.

**Record and data access** read “Sales Person” via get\_value · execute query text (SELECT, Sales Team, Sales Person) · read “Customer” via get\_list.

**Explicit results** Platform.get\_list(“Customer”, fields = list(“name”, “customer\_name”, “email\_id”), filters = list(list(“name”, “in”, list(sales\_person\_records at “Customer”)))) · list().

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(“Sales Person”, sales\_person, list(“lft”, “rgt”)).
- Set records from Platform.db.sql(query text (SELECT, Sales Team, Sales Person), tuple(lft, rgt), as\_dict = 1).
- Set sales\_person\_records from Platform.\_dict().
- For each d in records.
  - Evaluate sales\_person\_records.setdefault(d.parenttype, set()).add(d.parent).
- If sales\_person\_records.get(“Customer”).
  - Return Platform.get\_list(“Customer”, fields = list(“name”, “customer\_name”, “email\_id”), filters = list(list(“name”, “in”, list(sales\_person\_records at “Customer”)))).
- Otherwise.
  - Return list().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L82) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L865)

<a id="op-2cd0235716a298"></a>
### Get recipients and cc

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_recipients_and_carbon_copy`

**Inputs** customer, doc.

**Record and data access** read “User” via get\_value.

**Explicit results** tuple(recipients, cc).

**Local steps**

- Set recipients from list().
- For each clist in doc.customers.
  - If clist.customer equals customer.
    - If clist.billing\_email.
      - For each email in clist.billing\_email.split(“,”).
        - Evaluate recipients.append(email.strip()).
    - If (doc.primary\_mandatory and clist.primary\_email).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.primary\_mandatory → clist.primary\_email.
      - For each email in clist.primary\_email.split(“,”).
        - Evaluate recipients.append(email.strip()).
- Set cc from list().
- If doc.cc\_to differs from empty text.
  - Attempt the following.
    - Set cc from list of Platform.get\_value(“User”, user.cc, “email”) for user drawn from doc.cc\_to.
      - Draw user from doc.cc\_to.
  - On failure (Exception).
    - Take no action here.
- Return tuple(recipients, cc).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L84) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L869)

<a id="op-6f19d7c394edbf"></a>
### Get context

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_context`

**Inputs** customer, doc.

**Record and data access** resolve a document from “Customer” via get\_doc.

**Explicit results** mapping(“doc” → template\_doc, “customer” → Platform.get\_doc(“Customer”, customer)).

**Local steps**

- Set template\_doc from copy.deepcopy(doc).
- Remove template\_doc.customers.
- Set template\_doc.from\_date from format\_date(template\_doc.from\_date).
- Set template\_doc.to\_date from format\_date(template\_doc.to\_date).
- Return mapping(“doc” → template\_doc, “customer” → Platform.get\_doc(“Customer”, customer)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0142.json#L5541) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L863)

<a id="op-f633907822afc7"></a>
### Fetch customers

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_fetch_customers`

**Inputs** customer\_collection, collection\_name, primary\_mandatory.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Customer” via get\_list.

**Explicit results** customer\_list.

**Explicit failure paths** validation helper — translated “No Customers found with selected options.”.

**Local steps**

- Set customer\_list from list().
- Set customers from list().
- If customer\_collection equals “Sales Person”.
  - Set customers from get\_customers\_based\_on\_sales\_person(collection\_name).
  - If not bool(customers).
    - Call the validation error handler Platform.throw(translated “No Customers found with selected options.”).
- Otherwise.
  - If customer\_collection equals “Sales Partner”.
    - Set customers from Platform.get\_list(“Customer”, fields = list(“name”, “customer\_name”, “email\_id”), filters = list(list(“default\_sales\_partner”, “=”, collection\_name))).
  - Otherwise.
    - Set customers from get\_customers\_based\_on\_territory\_or\_customer\_group(customer\_collection, collection\_name).
- For each customer in customers.
  - Set primary\_email from (customer.get(“email\_id”) or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in customer.get(“email\_id”) → empty text.
  - Set billing\_email from get\_customer\_emails(customer.name, 1, billing\_and\_primary = false).
  - If int(primary\_mandatory).
    - If primary\_email equals empty text.
      - Continue with the next iteration or loop test.
  - Evaluate customer\_list.append(mapping(“name” → customer.name, “customer\_name” → customer.customer\_name, “primary\_email” → primary\_email, “billing\_email” → billing\_email)).
- Return customer\_list.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L80) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L860)

<a id="op-e92e39f589faf9"></a>
### Get customer emails

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_get_customer_emails`

**Inputs** customer\_name, primary\_mandatory, billing\_and\_primary = true.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** execute query text (SELECT, Contact Email, Dynamic Link, Contact).format(mcond = get\_match\_cond(“Contact”)) · read “Customer” via get\_value.

**Explicit results** empty text · list((primary\_email or empty text), billing\_email at 0 at 0) · (billing\_email at 0 at 0 or empty text).

**Explicit failure paths** validation helper — translated “No billing email found for customer: {0}”.format(customer\_name) · validation helper — translated “No primary email found for customer: {0}”.format(customer\_name).

**Local steps**

- Evaluate Platform.has\_permission(“Customer”, “read”, customer\_name, throw = true).
- Set billing\_email from Platform.db.sql(query text (SELECT, Contact Email, Dynamic Link, Contact).format(mcond = get\_match\_cond(“Contact”)), customer\_name).
- If (len(billing\_email) equals 0 or billing\_email at 0 at 0 is identical to no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(billing\_email) equals 0 → billing\_email at 0 at 0 is identical to no value.
  - If billing\_and\_primary.
    - Call the validation error handler Platform.throw(translated “No billing email found for customer: {0}”.format(customer\_name)).
  - Otherwise.
    - Return empty text.
- If billing\_and\_primary.
  - Set primary\_email from Platform.get\_value(“Customer”, customer\_name, “email\_id”).
  - If (primary\_email is identical to no value and int(primary\_mandatory)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in primary\_email is identical to no value → int(primary\_mandatory).
    - Call the validation error handler Platform.throw(translated “No primary email found for customer: {0}”.format(customer\_name)).
  - Return list((primary\_email or empty text), billing\_email at 0 at 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in primary\_email → empty text.
- Otherwise.
  - Return (billing\_email at 0 at 0 or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in billing\_email at 0 at 0 → empty text.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Customer”, “read”, customer\_name, throw = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L81) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L864)

<a id="op-a4969f234827f3"></a>
### Download statements

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_download_statements`

**Inputs** document\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Process Statement Of Accounts” via get\_doc.

**Local steps**

- Set doc from Platform.get\_doc(“Process Statement Of Accounts”, document\_name).
- Evaluate doc.check\_permission(“read”).
- Set report from get\_report\_pdf(doc).
- If report.
  - Set Platform.local.response.filename from (doc.name + “.pdf”).
  - Set Platform.local.response.filecontent from report.
  - Set Platform.local.response.type from “download”.

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L79) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L859)

<a id="op-04631646fd6e06"></a>
### Send emails

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_send_emails`

**Inputs** document\_name, from\_scheduler = false, posting\_date = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** resolve a document from “Process Statement Of Accounts” via get\_doc · read “Email Account” via get\_value.

**State and service calls** enqueue · request set\_value on doc.doctype.

**Explicit results** true · false.

**Local steps**

- Set doc from Platform.get\_doc(“Process Statement Of Accounts”, document\_name).
- Evaluate doc.check\_permission().
- Set report from get\_report\_pdf(doc, consolidated = false).
- If report.
  - For each tuple(customer, report\_pdf) in report.items().
    - Set context from get\_context(customer, doc).
    - Set filename from Platform.render\_template(doc.pdf\_name, context, restrict\_globals = true).
    - Set attachments from list(mapping(“fname” → (filename + “.pdf”), “fcontent” → report\_pdf)).
    - Set tuple(recipients, cc) from get\_recipients\_and\_cc(customer, doc).
    - If not recipients.
      - Continue with the next iteration or loop test.
    - Set subject from Platform.render\_template(doc.subject, context, restrict\_globals = true).
    - Set message from Platform.render\_template(doc.body, context, restrict\_globals = true).
    - If doc.sender.
      - Set sender\_email from Platform.db.get\_value(“Email Account”, doc.sender, “email\_id”).
    - Otherwise.
      - Set sender\_email from Platform.session.user.
    - Evaluate Platform.enqueue(queue = “short”, method = Platform.sendmail, recipients = recipients, sender = sender\_email, …).
  - If (doc.enable\_auto\_email and from\_scheduler).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc.enable\_auto\_email → from\_scheduler.
    - Set posting\_date from getdate((posting\_date or today())).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in posting\_date → today().
    - Set new\_to\_date from getdate(doc.to\_date when doc.report equals “General Ledger”, otherwise doc.posting\_date).
      - Value choice on doc.report equals “General Ledger” — true gives doc.to\_date, false gives doc.posting\_date.
    - While new\_to\_date ≤ posting\_date.
      - If doc.frequency belongs to tuple(“Daily”, “Weekly”, “Biweekly”).
        - Set frequency from mapping(“Daily” → 1, “Weekly” → 7, “Biweekly” → 14).
        - Set new\_to\_date from add\_days(new\_to\_date, frequency at doc.frequency).
      - Otherwise.
        - Set new\_to\_date from add\_months(new\_to\_date, 1 when doc.frequency equals “Monthly”, otherwise 3).
          - Value choice on doc.frequency equals “Monthly” — true gives 1, false gives 3.
    - Set new\_from\_date from add\_months(new\_to\_date, (negative 1 × doc.filter\_duration)).
    - Evaluate doc.add\_comment(“Comment”, (“Emails sent on: ” + Platform.utils.format\_datetime(Platform.utils.now()))).
    - If doc.report equals “General Ledger”.
      - Evaluate Platform.db.set\_value(doc.doctype, doc.name, “to\_date”, new\_to\_date).
      - Evaluate Platform.db.set\_value(doc.doctype, doc.name, “from\_date”, new\_from\_date).
    - Otherwise.
      - Evaluate Platform.db.set\_value(doc.doctype, doc.name, “posting\_date”, new\_to\_date).
  - Return true.
- Otherwise.
  - Return false.

**Values supplied outside this operation** effective access from doc.check\_permission() · service or queued work from Platform.enqueue(queue = “short”, method = Platform.sendmail, recipients = recipients, sender = sender\_email, …) · clock or generated value from today(), Platform.utils.now().

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L694) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L876)

<a id="op-36b09a2953bf59"></a>
### Send auto email

`operation_enterprise_accounts_record_definitions_process_statement_of_accounts_business_behavior_send_auto_email`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Record and data access** read “Process Statement Of Accounts” via get\_list.

**Explicit results** true.

**Local steps**

- Evaluate Platform.has\_permission(“Process Statement Of Accounts”, throw = true).
- For each tuple(report, date\_field) in tuple(tuple(“General Ledger”, “to\_date”), tuple(“Accounts Receivable”, “posting\_date”)).
  - Set selected from Platform.get\_list(“Process Statement Of Accounts”, filters = mapping(“enable\_auto\_email” → 1, “report” → report, date\_field → list(“&lt;=”, today())), or\_filters = list(list(“start\_date”, “is”, “not set”), li ….
  - For each entry in selected.
    - Evaluate send\_emails(entry.name, from\_scheduler = true).
- Return true.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Process Statement Of Accounts”, throw = true) · clock or generated value from today().

**Boundaries to resolve** stored data, callee failures, effective access, time or generated values, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L88) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L875)

## Record · Process subscription

[Record definition](../../../../data/record-types/process_subscription.json)

<a id="op-dcec576fc4ce82"></a>
### Process Subscription.on submit

`operation_enterprise_accounts_record_definitions_process_subscription_business_behavior_process_subscription_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.process\_all\_subscription().

If control reaches the end, it returns no value.

**Methods declared on this owner** [process all subscription](operations-090.md#op-f9a8490e695eaa).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0143.json#L5539) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L708) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L885)

<a id="op-f9a8490e695eaa"></a>
### Process Subscription.process all subscription

`operation_enterprise_accounts_record_definitions_process_subscription_business_behavior_process_subscription_process_all_subscription`

**Inputs** self.

**Record and data access** read “Subscription” via get\_all.

**State and service calls** enqueue.

**Local steps**

- Set filters from mapping(“status” → tuple(“!=”, “Cancelled”)).
- If self.subscription.
  - Set filters at “name” from self.subscription.
- Set subscriptions from Platform.get\_all(“Subscription”, filters, pluck = “name”).
- For each subscription in create\_batch(subscriptions, 500).
  - Evaluate Platform.enqueue(method = “Enterprise.accounts.doctype.subscription.subscription.process\_all”, queue = “long”, subscription = subscription, posting\_date = self.posting\_date, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.accounts.doctype.subscription.subscription.process\_all”, queue = “long”, subscription = subscription, posting\_date = self.posting\_date, …).

**Boundaries to resolve** stored data, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L709) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L886)

<a id="op-0988efc5bee138"></a>
### Create subscription process

`operation_enterprise_accounts_record_definitions_process_subscription_business_behavior_create_subscription_process`

**Inputs** subscription = no value, posting\_date = no value.

**State and service calls** request new\_doc for “Process Subscription” · call submit on doc.

**Local steps**

- Set doc from Platform.new\_doc(“Process Subscription”).
- Set doc.subscription from subscription.
- Set doc.posting\_date from getdate(posting\_date).
- Evaluate doc.submit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0143.json#L5912) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L707) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L884)

## Report · Profit and loss statement

<a id="op-d51d7073c29f61"></a>
### Execute

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_execute`

**Inputs** filters = no value.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** FinancialReportEngine().execute(filters) · no value · tuple(columns, data, no value, chart, …).

**Local steps**

- If (filters and filters.report\_template).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters → filters.report\_template.
  - Return FinancialReportEngine().execute(filters).
- Set period\_list from build\_period\_list(filters).
- If not period\_list.
  - Return no value.
- Set income from get\_data(filters.company, “Income”, “Credit”, period\_list, filters = filters, accumulated\_values = filters.accumulated\_values, ignore\_closing\_entries = true).
- Set expense from get\_data(filters.company, “Expense”, “Debit”, period\_list, filters = filters, accumulated\_values = filters.accumulated\_values, ignore\_closing\_entries = true).
- Set net\_profit\_loss from get\_net\_profit\_loss(income, expense, period\_list, filters.company, accumulated\_values = bool(filters.accumulated\_values), …).
- Set data from list().
- Evaluate data.extend((income or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in income → list().
- Evaluate data.extend((expense or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in expense → list().
- If net\_profit\_loss.
  - Evaluate data.append(net\_profit\_loss).
- Set columns from get\_columns(filters.periodicity, period\_list, filters.accumulated\_values, filters.company, selected\_view = filters.get(“selected\_view”)).
- Set currency from (filters.presentation\_currency or Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.presentation\_currency → Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set chart from get\_chart\_data(filters, period\_list, income, expense, …).
- Set tuple(report\_summary, primitive\_summary) from get\_report\_summary(period\_list, filters.periodicity, income, expense, …).
- If filters.get(“selected\_view”) equals “Growth”.
  - Evaluate compute\_growth\_view\_data(data, period\_list).
- If filters.get(“selected\_view”) equals “Margin”.
  - Evaluate compute\_margin\_view\_data(data, period\_list, income at negative 2 when income, otherwise no value).
    - Value choice on income — true gives income at negative 2, false gives no value.
- Return tuple(columns, data, no value, chart, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L817) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1159)

<a id="op-f25915c861332c"></a>
### Get report summary

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_get_report_summary`

**Inputs** period\_list, periodicity, income, expense, net\_profit\_loss, currency, filters, consolidated = false.

**Explicit results** tuple(list(mapping(“value” → net\_income, “label” → income\_label, “datatype” → “Currency”, “currency” → currency), mapping(“value” → net\_expense, “label” → expense\_label, “datatype” → “Currency”, “currency” ….

**Local steps**

- Set tuple(net\_income, net\_expense, net\_profit) from tuple(0.0, 0.0, 0.0).
- If filters.get(“accumulated\_in\_group\_company”).
  - Set period\_list from get\_filtered\_list\_for\_consolidated\_report(filters, period\_list).
  - Set keys from list of period when consolidated, otherwise period.key for period drawn from period\_list.
    - Draw period from period\_list.
    - Value choice on consolidated — true gives period, false gives period.key.
- Otherwise.
  - Set keys from get\_period\_keys\_for\_total(period\_list, filters.accumulated\_values, consolidated).
- For each key in keys.
  - If income.
    - Update net\_income using + flt(income at negative 2.get(key)).
  - If expense.
    - Update net\_expense using + flt(expense at negative 2.get(key)).
  - If net\_profit\_loss.
    - Update net\_profit using + flt(net\_profit\_loss.get(key)).
- If (len(period\_list) equals 1 and periodicity equals “Yearly”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(period\_list) equals 1 → periodicity equals “Yearly”.
  - Set profit\_label from translated “Profit This Year”.
  - Set income\_label from translated “Total Income This Year”.
  - Set expense\_label from translated “Total Expense This Year”.
- Otherwise.
  - Set profit\_label from translated “Net Profit”.
  - Set income\_label from translated “Total Income”.
  - Set expense\_label from translated “Total Expense”.
- Return tuple(list(mapping(“value” → net\_income, “label” → income\_label, “datatype” → “Currency”, “currency” → currency), mapping(“value” → net\_expense, “label” → expense\_label, “datatype” → “Currency”, “currency” ….
  - Value choice on net\_profit &gt; 0 — true gives “Green”, false gives “Red”.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0269.json#L4106) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L822) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1164)

<a id="op-e65283e016413e"></a>
### Get net profit loss

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_get_net_profit_loss`

**Inputs** income, expense, period\_list, company, currency = no value, consolidated = false, accumulated\_values = false.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** net\_profit\_loss.

**Local steps**

- Set net\_profit\_loss from mapping(“account\_name” → ((“'” + translated “Profit for the year”) + “'”), “account” → ((“'” + translated “Profit for the year”) + “'”), “warn\_if\_negative” → true, “currency” → (currency or Platform.get\_ca ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in currency → Platform.get\_cached\_value(“Company”, company, “default\_currency”).
- Set has\_value from false.
- For each period in period\_list.
  - Set key from period when consolidated, otherwise period.key.
    - Value choice on consolidated — true gives period, false gives period.key.
  - Set total\_income from flt(income at negative 2 at key, 3) when income, otherwise 0.
    - Value choice on income — true gives flt(income at negative 2 at key, 3), false gives 0.
  - Set total\_expense from flt(expense at negative 2 at key, 3) when expense, otherwise 0.
    - Value choice on expense — true gives flt(expense at negative 2 at key, 3), false gives 0.
  - Set net\_profit\_loss at key from (total\_income − total\_expense).
  - If net\_profit\_loss at key.
    - Set has\_value from true.
- Set total\_keys from get\_period\_keys\_for\_total(period\_list, accumulated\_values, consolidated).
- Set net\_profit\_loss at “total” from flt(sum(generator of net\_profit\_loss.get(k, 0.0) for k drawn from total\_keys)).
  - Draw k from total\_keys.
- If has\_value.
  - Return net\_profit\_loss.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, company, “default\_currency”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0269.json#L5034) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L821) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1163)

<a id="op-28f89740f40b4a"></a>
### Get chart data

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_get_chart_data`

**Inputs** filters, chart\_columns, income, expense, net\_profit\_loss, currency.

**Explicit results** chart.

**Local steps**

- Set labels from list of col.get(“label”) for col drawn from chart\_columns.
  - Draw col from chart\_columns.
- Set tuple(income\_data, expense\_data, net\_profit) from tuple(list(), list(), list()).
- For each col in chart\_columns.
  - Set key from (col.get(“key”) or col.get(“fieldname”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in col.get(“key”) → col.get(“fieldname”).
  - If income.
    - Evaluate income\_data.append(income at negative 2.get(key)).
  - If expense.
    - Evaluate expense\_data.append(expense at negative 2.get(key)).
  - If net\_profit\_loss.
    - Evaluate net\_profit.append(net\_profit\_loss.get(key)).
- Set datasets from list().
- If income\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Income”, “values” → income\_data)).
- If expense\_data.
  - Evaluate datasets.append(mapping(“name” → translated “Expense”, “values” → expense\_data)).
- If net\_profit.
  - Evaluate datasets.append(mapping(“name” → translated “Net Profit/Loss”, “values” → net\_profit)).
- Set chart from mapping(“data” → mapping(“labels” → labels, “datasets” → datasets)).
- If not filters.accumulated\_values.
  - Set chart at “type” from “bar”.
- Otherwise.
  - Set chart at “type” from “line”.
- Set chart at “fieldtype” from “Currency”.
- Set chart at “options” from “currency”.
- Set chart at “currency” from currency.
- Return chart.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0269.json#L5662) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1161)

<a id="op-36305d90c079b3"></a>
### Execute snapshot report

`operation_enterprise_accounts_report_profit_and_loss_statement_business_behavior_execute_snapshot_report`

**Inputs** filters.

**Record and data access** read “Company” via get\_cached\_value.

**Explicit results** execute(filters) · tuple(columns, data, no value, chart, …).

**Explicit failure paths** validation helper — translated “Profit and Loss Statement requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”)).

**Local steps**

- If (filters.report\_template or has\_gl\_entry\_restrictions()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.report\_template → has\_gl\_entry\_restrictions().
  - Return execute(filters).
- Bind dependencies get\_latest\_sync.
- If not conn bound to get\_latest\_sync(“GL Entry”).
  - Call the validation error handler Platform.throw(translated “Profit and Loss Statement requires {0} to be synced to DuckDB”.format(Platform.bold(“GL Entry”))).
- Set period\_list from build\_period\_list(filters).
- Set income from \_get\_data\_duckdb(conn, filters, “Income”, “Credit”, …).
- Set expense from \_get\_data\_duckdb(conn, filters, “Expense”, “Debit”, …).
- Set net\_profit\_loss from get\_net\_profit\_loss(income, expense, period\_list, filters.company, accumulated\_values = bool(filters.accumulated\_values), …).
- Set data from list().
- Evaluate data.extend((income or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in income → list().
- Evaluate data.extend((expense or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in expense → list().
- If net\_profit\_loss.
  - Evaluate data.append(net\_profit\_loss).
- Set columns from get\_columns(filters.periodicity, period\_list, filters.accumulated\_values, filters.company, selected\_view = filters.get(“selected\_view”)).
- Set currency from (filters.presentation\_currency or Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.presentation\_currency → Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).
- Set chart from get\_chart\_data(filters, period\_list, income, expense, …).
- Set tuple(report\_summary, primitive\_summary) from get\_report\_summary(period\_list, filters.periodicity, income, expense, …).
- If filters.get(“selected\_view”) equals “Growth”.
  - Evaluate compute\_growth\_view\_data(data, period\_list).
- If filters.get(“selected\_view”) equals “Margin”.
  - Evaluate compute\_margin\_view\_data(data, period\_list, income at negative 2 when income, otherwise no value).
    - Value choice on income — true gives income at negative 2, false gives no value.
- Return tuple(columns, data, no value, chart, …).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Company”, filters.company, “default\_currency”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L818) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1160)
