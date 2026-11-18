# Company and master data · operations 7

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Email digest

[Record definition](../../../../data/record-types/email_digest.json)

<a id="op-1f0f5fb052e809"></a>
### Email Digest.get summary of pending

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_summary_of_pending`

**Inputs** self, doc\_type, fieldname, getfield.

**Explicit results** mapping(“label” → self.meta.get\_label(fieldname), “value” → value, “billed\_value” → billed\_value, “delivered\_value” → delivered\_value, …).

**Local steps**

- Set doc from Platform.qb.DocType(doc\_type).
- Set tuple(value, count, billed\_value, delivered\_value) from nested operand in the contract.select(nested operand in the contract(nested operand in the contract, nested operand in the contract), nested operand in the contract(nested operand in the contract), nested  ….
- Return mapping(“label” → self.meta.get\_label(fieldname), “value” → value, “billed\_value” → billed\_value, “delivered\_value” → delivered\_value, …).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L106) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L839) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L397)

<a id="op-27e1ed4bab7735"></a>
### Email Digest.get summary of pending quotations

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_summary_of_pending_quotations`

**Inputs** self, fieldname.

**Explicit results** mapping(“label” → label, “value” → value, “last\_value” → last\_value, “count” → count).

**Local steps**

- Set quotation from Platform.qb.DocType(“Quotation”).
- Set tuple(value, count) from nested operand in the contract.select(nested operand in the contract(nested operand in the contract, nested operand in the contract), nested operand in the contract(nested operand in the contract)).where(( ….
- Set last\_value from nested operand in the contract(nested operand in the contract).where(((nested operand in the contract bitwise and nested operand in the contract) bitwise and (nested operand in the contract bitwise or nest … at 0.
- Set label from get\_link\_to\_report(“Quotation”, label = translated self.meta.get\_label(fieldname), report\_type = “Report Builder”, doctype = “Quotation”, filters = mapping(“status” → list(list(“!=”, “Ordered”), list(“!=”, ….
- Return mapping(“label” → label, “value” → value, “last\_value” → last\_value, “count” → count).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L107) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L840) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L398)

<a id="op-1e2cdbb9f92f01"></a>
### Email Digest.get summary of doc

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_summary_of_record`

**Inputs** self, doc\_type, fieldname.

**Explicit results** mapping(“label” → label, “value” → value, “last\_value” → last\_value, “count” → count).

**Local steps**

- Set date\_field from “posting\_date” when doc\_type belongs to list(“Sales Invoice”, “Purchase Invoice”), otherwise “transaction\_date”.
  - Value choice on doc\_type belongs to list(“Sales Invoice”, “Purchase Invoice”) — true gives “posting\_date”, false gives “transaction\_date”.
- Set value from flt(self.get\_total\_on(doc\_type, self.future\_from\_date, self.future\_to\_date) at 0.grand\_total).
- Set count from self.get\_total\_on(doc\_type, self.future\_from\_date, self.future\_to\_date) at 0.count.
- Set last\_value from flt(self.get\_total\_on(doc\_type, self.past\_from\_date, self.past\_to\_date) at 0.grand\_total).
- Set filters from mapping(date\_field → list(list(“&gt;=”, self.future\_from\_date), list(“&lt;=”, self.future\_to\_date)), “docstatus” → 1, “status” → list(list(“!=”, “Cancelled”)), “company” → self.company).
- Set label from get\_link\_to\_report(doc\_type, label = translated self.meta.get\_label(fieldname), report\_type = “Report Builder”, filters = filters, doctype = doc\_type).
- Return mapping(“label” → label, “value” → value, “last\_value” → last\_value, “count” → count).

**Methods declared on this owner** [get total on](operations-007.md#op-76bf5482d1fa2d).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L108) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L841) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L399)

<a id="op-76bf5482d1fa2d"></a>
### Email Digest.get total on

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_total_on`

**Inputs** self, doc\_type, from\_date, to\_date.

**Record and data access** read doc\_type via get\_all.

**Explicit results** Platform.get\_all(doc\_type, filters = mapping(date\_field → list(“between”, tuple(from\_date, to\_date)), “docstatus” → 1, “status” → list(“not in”, “Cancelled”), “company” → self.company), fields = list(mappi ….

**Local steps**

- Set date\_field from “posting\_date” when doc\_type belongs to list(“Sales Invoice”, “Purchase Invoice”), otherwise “transaction\_date”.
  - Value choice on doc\_type belongs to list(“Sales Invoice”, “Purchase Invoice”) — true gives “posting\_date”, false gives “transaction\_date”.
- Return Platform.get\_all(doc\_type, filters = mapping(date\_field → list(“between”, tuple(from\_date, to\_date)), “docstatus” → 1, “status” → list(“not in”, “Cancelled”), “company” → self.company), fields = list(mappi ….

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L111) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L844) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L402)

<a id="op-24a181f2c2de29"></a>
### Email Digest.get from to date

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_from_to_date`

**Inputs** self.

**Explicit results** tuple(from\_date, to\_date).

**Local steps**

- Set today from now\_datetime().date().
- If self.frequency equals “Daily”.
  - Set from\_date, to\_date from (today − timedelta(days = 1)).
- Otherwise.
  - If self.frequency equals “Weekly”.
    - Set from\_date from (today − timedelta(days = today.weekday(), weeks = 1)).
    - Set to\_date from (from\_date + timedelta(days = 6)).
  - Otherwise.
    - Set from\_date from (today − relativedelta(days = (today.day − 1), months = 1)).
    - Set to\_date from (today − relativedelta(days = today.day)).
- Return tuple(from\_date, to\_date).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L5226) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L811) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L369)

<a id="op-5620d8ab54702b"></a>
### Email Digest.set dates

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_set_dates`

**Inputs** self.

**Local steps**

- Set tuple(self.future\_from\_date, self.future\_to\_date) from tuple(self.from\_date, self.to\_date).
- If self.frequency equals “Daily”.
  - Set self.past\_from\_date, self.past\_to\_date from (self.future\_from\_date − relativedelta(days = 1)).
- Otherwise.
  - If self.frequency equals “Weekly”.
    - Set self.past\_from\_date from (self.future\_from\_date − relativedelta(weeks = 1)).
    - Set self.past\_to\_date from (self.future\_from\_date − relativedelta(days = 1)).
  - Otherwise.
    - Set self.past\_from\_date from (self.future\_from\_date − relativedelta(months = 1)).
    - Set self.past\_to\_date from (self.future\_from\_date − relativedelta(days = 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L5597) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L852) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L409)

<a id="op-9e0df030548220"></a>
### Email Digest.get next sending

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_next_sending`

**Inputs** self.

**Explicit results** send\_date.

**Local steps**

- Set tuple(from\_date, to\_date) from self.get\_from\_to\_date().
- Set send\_date from (to\_date + timedelta(days = 1)).
- If self.frequency equals “Daily”.
  - Set next\_send\_date from (send\_date + timedelta(days = 1)).
- Otherwise.
  - If self.frequency equals “Weekly”.
    - Set next\_send\_date from (send\_date + timedelta(weeks = 1)).
  - Otherwise.
    - Set next\_send\_date from (send\_date + relativedelta(months = 1)).
- Set self.next\_send from (formatdate(next\_send\_date) + “ at midnight”).
- Return send\_date.

**Methods declared on this owner** [get from to date](operations-007.md#op-24a181f2c2de29).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L5963) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L819) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L377)

<a id="op-901456238d63a9"></a>
### Email Digest.onload

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_onload`

**Inputs** self.

**Local steps**

- Evaluate self.get\_next\_sending().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get next sending](operations-007.md#op-9e0df030548220).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L6278) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L849) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L406)

<a id="op-0926f0bb782ef6"></a>
### Email Digest.fmt money

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_format_money`

**Inputs** self, value, absol = true.

**Explicit results** fmt\_money(abs(value), currency = self.currency) · fmt\_money(value, currency = self.currency).

**Local steps**

- If absol.
  - Return fmt\_money(abs(value), currency = self.currency).
- Otherwise.
  - Return fmt\_money(value, currency = self.currency).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0689.json#L6329) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L805) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L363)

<a id="op-d3be6b5d6e23d1"></a>
### Email Digest.get purchase orders items overdue list

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_email_digest_get_purchase_orders_items_overdue_list`

**Inputs** self.

**Explicit results** Platform.\_dict() · items\_by\_parent.

**Local steps**

- If not Platform.has\_permission(“Purchase Order”, “read”).
  - Return Platform.\_dict().
- Set po from Platform.qb.DocType(“Purchase Order”).
- Set poi from Platform.qb.DocType(“Purchase Order Item”).
- Set query from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.company equals nested operand in the contract.company).orderby(poi.parent, order = Platform.qb.desc).orde ….
- Set items\_by\_parent from Platform.\_dict().
- For each row in query.run(as\_dict = true).
  - Set row.link from get\_url\_to\_form(“Purchase Order”, row.parent).
  - Set row.rate from fmt\_money(row.rate, 2, row.currency).
  - Set row.amount from fmt\_money(row.amount, 2, row.currency).
  - Evaluate items\_by\_parent.setdefault(row.parent, list()).append(row).
- Return items\_by\_parent.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Purchase Order”, “read”) · clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L101) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L830) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L388)

<a id="op-0e9a886235c661"></a>
### Send

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_send`

**Inputs** no declared parameters.

**Record and data access** read “Email Digest” via get\_all · resolve a document from “Email Digest” via get\_doc.

**State and service calls** savepoint “email\_digest” · rollback.

**Local steps**

- Set now\_date from now\_datetime().date().
- For each ed in Platform.get\_all(“Email Digest”, filters = mapping(“enabled” → 1, “docstatus” → list(“&lt;”, 2)), fields = list(“name”), as\_list = true).
  - Evaluate Platform.db.savepoint(“email\_digest”).
  - Attempt the following.
    - Set ed\_obj from Platform.get\_doc(“Email Digest”, ed at 0).
    - If now\_date equals ed\_obj.get\_next\_sending().
      - Evaluate ed\_obj.\_send(continue\_on\_error = true).
  - On failure (Exception).
    - Evaluate Platform.db.rollback(save\_point = “email\_digest”).
    - Evaluate Platform.log\_error(title = formatted text Email Digest failed: {ed at 0}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L119) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L859) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L416)

<a id="op-85495c46f9349d"></a>
### Get digest msg

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_get_digest_message`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Email Digest” via get\_doc.

**Explicit results** email\_digest.get\_msg\_html().

**Local steps**

- Set email\_digest from Platform.get\_doc(“Email Digest”, name).
- Evaluate email\_digest.check\_permission().
- Return email\_digest.get\_msg\_html().

**Values supplied outside this operation** effective access from email\_digest.check\_permission().

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L117) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L856) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L413)

<a id="op-544c5b3426c5c8"></a>
### Get incomes expenses for period

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_get_incomes_expenses_for_period`

**Inputs** account, from\_date, to\_date.

**Explicit results** 0.0 · val.

**Local steps**

- Set fiscal\_year from get\_digest\_fiscal\_year(to\_date).
- If not fiscal\_year.
  - Return 0.0.
- Set val from 0.0.
- Set balance\_on\_to\_date from get\_balance\_on(account, date = to\_date).
- Set balance\_before\_from\_date from get\_balance\_on(account, date = (from\_date − timedelta(days = 1))).
- Set fy\_start\_date from fiscal\_year at 1.
- If from\_date equals fy\_start\_date.
  - Set val from balance\_on\_to\_date.
- Otherwise.
  - If from\_date &gt; fy\_start\_date.
    - Set val from (balance\_on\_to\_date − balance\_before\_from\_date).
  - Otherwise.
    - Set last\_year\_closing\_balance from get\_balance\_on(account, date = (fy\_start\_date − timedelta(days = 1))).
    - Set val from (balance\_on\_to\_date + (last\_year\_closing\_balance − balance\_before\_from\_date)).
- Return val.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L118) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L858) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L415)

<a id="op-5488b113d27c5b"></a>
### Get count for period

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_get_count_for_period`

**Inputs** account, fieldname, from\_date, to\_date.

**Explicit results** 0.0 · count.

**Local steps**

- Set fiscal\_year from get\_digest\_fiscal\_year(to\_date).
- If not fiscal\_year.
  - Return 0.0.
- Set count from 0.0.
- Set count\_on\_to\_date from get\_count\_on(account, fieldname, to\_date).
- Set count\_before\_from\_date from get\_count\_on(account, fieldname, (from\_date − timedelta(days = 1))).
- Set fy\_start\_date from fiscal\_year at 1.
- If from\_date equals fy\_start\_date.
  - Set count from count\_on\_to\_date.
- Otherwise.
  - If from\_date &gt; fy\_start\_date.
    - Set count from (count\_on\_to\_date − count\_before\_from\_date).
  - Otherwise.
    - Set last\_year\_closing\_count from get\_count\_on(account, fieldname, (fy\_start\_date − timedelta(days = 1))).
    - Set count from (count\_on\_to\_date + (last\_year\_closing\_count − count\_before\_from\_date)).
- Return count.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L116) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L855) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L412)

<a id="op-7d052866b046d9"></a>
### Get digest fiscal year

`operation_enterprise_binding_enterprise_setup_doctype_email_digest_email_digest_get_digest_fiscal_year`

**Inputs** date.

**Explicit results** fiscal\_year · no value · get\_fiscal\_year(date).

**Local steps**

- Set fiscal\_year from get\_fiscal\_year(date, raise\_on\_missing = false).
- If fiscal\_year.
  - Return fiscal\_year.
- Set years from get\_fiscal\_years().
- If (years and date &lt; min(generator of year.year\_start\_date for year drawn from years)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in years → date &lt; min(generator of year.year\_start\_date for year drawn from years).
  - Draw year from years.
  - Return no value.
- Return get\_fiscal\_year(date).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L655) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L152)

<a id="op-b1f8960162ce69"></a>
### Get future date for calendaer event

`operation_enterprise_setup_record_definitions_email_digest_business_behavior_get_future_date_for_calendaer_event`

**Inputs** frequency.

**Explicit results** tuple(from\_date, to\_date).

**Local steps**

- Set from\_date, to\_date from today().
- If frequency equals “Weekly”.
  - Set to\_date from add\_to\_date(from\_date, weeks = 1).
- Otherwise.
  - If frequency equals “Monthly”.
    - Set to\_date from add\_to\_date(from\_date, months = 1).
- Return tuple(from\_date, to\_date).

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L1942) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L857) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L414)

<a id="op-e762a259f598cd"></a>
### Get random quote

`operation_enterprise_setup_record_definitions_email_digest_quotes_business_behavior_get_random_quote`

**Inputs** no declared parameters.

**Explicit results** random.choice(quotes).

**Local steps**

- Set quotes from list(tuple(“Start by doing what's necessary; then do what's possible; and suddenly you are doing the impossible.”, “Francis of Assisi”), tuple(“The best and most beautiful things in the world cannot be see ….
- Return random.choice(quotes).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L2130) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L860) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L417)

## Record · Employee

[Record definition](../../../../data/record-types/employee.json)

<a id="op-130f164b2399cd"></a>
### Employee.autoname

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_autoname`

**Inputs** self.

**Local steps**

- Evaluate set\_name\_by\_naming\_series(self).
- Set self.employee from self.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L5959) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L874) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L424)

<a id="op-5b4343b679315b"></a>
### Employee.validate

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate`

**Inputs** self.

**Record and data access** read “Department” via get\_value · read “Employee” via get\_value · resolve a document from “User” via get\_doc.

**State and service calls** call save on user.

**Explicit failure paths** validation helper — translated “Cannot assign a disabled Department”.

**Local steps**

- Bind dependencies validate\_status.
- Evaluate validate\_status(self.status, list(“Active”, “Inactive”, “Suspended”, “Left”)).
- Set self.employee from self.name.
- Evaluate self.set\_employee\_name().
- Evaluate self.validate\_date().
- Evaluate self.validate\_email().
- Evaluate self.validate\_status().
- Evaluate self.validate\_reports\_to().
- Set department\_to\_restore from self.flags.pop(“department\_to\_restore”, no value).
- If (self.department and self.has\_value\_changed(“department”) and self.department differs from department\_to\_restore).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.department → self.has\_value\_changed(“department”) → self.department differs from department\_to\_restore.
  - If Platform.db.get\_value(“Department”, self.department, “disabled”).
    - Call the validation error handler Platform.throw(translated “Cannot assign a disabled Department”).
- Evaluate self.set\_preferred\_email().
- Evaluate self.validate\_preferred\_email().
- If self.user\_id.
  - Evaluate self.validate\_user\_details().
- Otherwise.
  - Set existing\_user\_id from Platform.db.get\_value(“Employee”, self.name, “user\_id”).
  - If existing\_user\_id.
    - Evaluate self.validate\_user\_access(existing\_user\_id).
    - Set user from Platform.get\_doc(“User”, existing\_user\_id).
    - Evaluate validate\_employee\_role(user, ignore\_emp\_check = true).
    - Evaluate user.save(ignore\_permissions = true).
    - Evaluate remove\_user\_permission(“Employee”, self.name, existing\_user\_id, ignore\_permissions = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set employee name](operations-007.md#op-90d011199c31d1), [validate date](operations-008.md#op-cb276baeca2d1a), [validate email](operations-008.md#op-8ee8916428e0db), [validate status](operations-008.md#op-20eecc13c89699), [validate reports to](operations-008.md#op-8acf6b3c1b7133), [set preferred email](operations-008.md#op-fa68abe542f7bb), [validate preferred email](operations-008.md#op-09421b0c790141), [validate user details](operations-007.md#op-c4b1f35b93b72c), [validate user access](operations-007.md#op-39dd822b7e420f).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L123) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L885) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L435)

<a id="op-ff93d2b2d71412"></a>
### Employee.after rename

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_after_rename`

**Inputs** self, old, new, merge.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“employee”, new).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L6534) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L873) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L423)

<a id="op-90d011199c31d1"></a>
### Employee.set employee name

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_set_employee_name`

**Inputs** self.

**Local steps**

- Set self.employee\_name from one space.join(filter(deferred anonymous expression, list(self.first\_name, self.middle\_name, self.last\_name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L6618) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L879) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L429)

<a id="op-c4b1f35b93b72c"></a>
### Employee.validate user details

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_user_details`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.user\_id.
  - Return no value.
- Evaluate self.validate\_for\_enabled\_user\_id().
- Evaluate self.validate\_duplicate\_user\_id().
- If any(generator of self.has\_value\_changed(field) for field drawn from tuple(“user\_id”, “status”, “create\_user\_permission”)).
  - Draw field from tuple(“user\_id”, “status”, “create\_user\_permission”).
  - Evaluate self.validate\_user\_access().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate for enabled user id](operations-008.md#op-238bb28a9aa90e), [validate duplicate user id](operations-008.md#op-2a81d536c2c19b), [validate user access](operations-007.md#op-39dd822b7e420f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L894) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L444)

<a id="op-39dd822b7e420f"></a>
### Employee.validate user access

`operation_enterprise_binding_enterprise_setup_doctype_employee_employee_employee_validate_user_access`

**Inputs** self, user = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper with Platform.PermissionError — translated “You are not permitted to link or update User {0}”.format(Platform.bold(user)).

**Local steps**

- Set editor\_roles from set(Platform.get\_roles()).
- If “System Manager” belongs to editor\_roles.
  - Return no value.
- Set user from (user or self.user\_id).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → self.user\_id.
- If (set(Platform.get\_roles(user)) bitwise and (get\_admin\_roles() − editor\_roles)).
  - Call the validation error handler Platform.throw(translated “You are not permitted to link or update User {0}”.format(Platform.bold(user)), Platform.PermissionError).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(), Platform.get\_roles(user).

**Boundaries to resolve** late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L97) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L657) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L154)

<a id="op-6a0daaee810b1d"></a>
### Employee.validate auto user creation

`operation_enterprise_setup_record_definitions_employee_business_behavior_employee_validate_auto_user_creation`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.MandatoryError — translated “Company or Personal Email is mandatory when 'Create User Automatically' is enabled”.

**Local steps**

- If (self.create\_user\_automatically and not (self.prefered\_email or self.company\_email or self.personal\_email)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.create\_user\_automatically → not (self.prefered\_email or self.company\_email or self.personal\_email).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.prefered\_email → self.company\_email → self.personal\_email.
  - Call the validation error handler Platform.throw(translated “Company or Personal Email is mandatory when 'Create User Automatically' is enabled”, Platform.MandatoryError, title = translated “Auto User Creation Error”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0690.json#L6830) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L886) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L436)
