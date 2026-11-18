# Accounting and settlement · operations 83

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Pos opening entry

<a id="op-7d7cc7697f0356"></a>
### POSOpening Entry.on cancel

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_on_cancel`

**Inputs** self.

**State and service calls** publish realtime with formatted text poe\_{self.name}.

**Local steps**

- Evaluate self.set\_status(update = true).
- Evaluate Platform.publish\_realtime(formatted text poe\_{self.name}, message = mapping(“operation” → “Cancelled”), docname = formatted text POS Opening Entry/{self.name}).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(formatted text poe\_{self.name}, message = mapping(“operation” → “Cancelled”), docname = formatted text POS Opening Entry/{self.name}).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0127.json#L5002) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L452) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L634)

<a id="op-eb97c9c9cb53f7"></a>
### POSOpening Entry.check poe is cancellable

`operation_enterprise_accounts_record_definitions_point_of_sale_opening_entry_business_behavior_point_of_sale_opening_entry_check_poe_is_cancellable`

**Inputs** self.

**Explicit failure paths** validation helper.

**Local steps**

- Bind dependencies get\_invoices.
- Set invoices from get\_invoices(self.period\_start\_date, Platform.utils.get\_datetime(), self.pos\_profile, self.user).
- If invoices.get(“invoices”).
  - Call the validation error handler Platform.throw(title = translated “POS Opening Entry Cancellation Error”, msg = translated “POS Opening Entry cannot be cancelled as unconsolidated Invoices exists.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0127.json#L5164) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L450) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L632)

## Record · Pos profile

<a id="op-bb877729d0e785"></a>
### POSProfile.validate

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_terms\_and\_conditions(self.get(“tc\_name”), “selling”).
- Evaluate self.validate\_disabled().
- Evaluate self.validate\_default\_profile().
- Evaluate self.validate\_all\_link\_fields().
- Evaluate self.validate\_write\_off\_settings().
- Evaluate self.validate\_duplicate\_groups().
- Evaluate self.validate\_payment\_methods().
- Evaluate self.validate\_accounting\_dimensions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate disabled](operations-083.md#op-c27ca29575b301), [validate default profile](operations-083.md#op-44474d97a04135), [validate all link fields](operations-083.md#op-d8772632e8d915), [validate write off settings](operations-083.md#op-85ca144f3236e4), [validate duplicate groups](operations-083.md#op-47caa933ca6965), [validate payment methods](operations-083.md#op-a172e9ea4d3a22), [validate accounting dimensions](operations-083.md#op-8f955142527cfd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L38) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L474) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L656)

<a id="op-8f955142527cfd"></a>
### POSProfile.validate accounting dimensions

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate_accounting_dimensions`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is a mandatory Accounting Dimension. &lt;br&gt;Please set a value for {0} in Accounting Dimensions section.”.format(Platform.bold(acc\_dim.label)).

**Local steps**

- Set acc\_dims from get\_checks\_for\_pl\_and\_bs\_accounts().
- For each acc\_dim in acc\_dims.
  - If (self.company equals acc\_dim.company and not self.get(acc\_dim.fieldname) and (acc\_dim.mandatory\_for\_pl or acc\_dim.mandatory\_for\_bs)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.company equals acc\_dim.company → not self.get(acc\_dim.fieldname) → (acc\_dim.mandatory\_for\_pl or acc\_dim.mandatory\_for\_bs).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in acc\_dim.mandatory\_for\_pl → acc\_dim.mandatory\_for\_bs.
    - Call the validation error handler Platform.throw(translated “{0} is a mandatory Accounting Dimension. &lt;br&gt;Please set a value for {0} in Accounting Dimensions section.”.format(Platform.bold(acc\_dim.label)), title = translated “Mandatory Acc ….

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L834) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L475) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L657)

<a id="op-c27ca29575b301"></a>
### POSProfile.validate disabled

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate_disabled`

**Inputs** self.

**Record and data access** read “POS Opening Entry” via exists.

**Explicit failure paths** validation helper — translated “POS Profile {0} cannot be disabled as there are ongoing POS sessions.”.format(Platform.bold(self.name)).

**Local steps**

- Set old\_doc from self.get\_doc\_before\_save().
- If (old\_doc and self.disabled and old\_doc.disabled differs from self.disabled and Platform.db.exists(“POS Opening Entry”, mapping(“pos\_profile” → self.name, “status” → “Open”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in old\_doc → self.disabled → old\_doc.disabled differs from self.disabled → Platform.db.exists(“POS Opening Entry”, mapping(“pos\_profile” → self.name, “status” → “Open”)).
  - Call the validation error handler Platform.throw(translated “POS Profile {0} cannot be disabled as there are ongoing POS sessions.”.format(Platform.bold(self.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L1094) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L478) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L660)

<a id="op-44474d97a04135"></a>
### POSProfile.validate default profile

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate_default_profile`

**Inputs** self.

**Record and data access** execute query text (SELECT, POS Profile User).

**Local steps**

- For each row in self.applicable\_for\_users.
  - Set res from Platform.db.sql(query text (SELECT, POS Profile User), tuple(row.user, self.name, self.company)).
  - If (row.default and res).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in row.default → res.
    - Evaluate msgprint(translated “Already set default in pos profile {0} for user {1}, kindly disabled default”.format(res at 0 at 0, row.user), raise\_exception = 1).
  - Otherwise.
    - If (not row.default and not res).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in not row.default → not res.
      - Evaluate msgprint(translated “User {0} doesn't have any default POS Profile. Check Default at Row {1} for this User.”.format(row.user, row.idx)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L39) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L477) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L659)

<a id="op-d8772632e8d915"></a>
### POSProfile.validate all link fields

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate_all_link_fields`

**Inputs** self.

**Record and data access** read mapping(“doctype” → link\_dt, “company” → self.company, “name” → link\_dn) via exists.

**Explicit failure paths** validation helper — translated “{0} does not belong to Company {1}”.format(link\_dn, self.company).

**Local steps**

- Set accounts from mapping(“Account” → list(self.income\_account, self.expense\_account), “Cost Center” → list(self.cost\_center), “Warehouse” → list(self.warehouse)).
- For each tuple(link\_dt, dn\_list) in accounts.items().
  - For each link\_dn in dn\_list.
    - If (link\_dn and not Platform.db.exists(mapping(“doctype” → link\_dt, “company” → self.company, “name” → link\_dn))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in link\_dn → not Platform.db.exists(mapping(“doctype” → link\_dt, “company” → self.company, “name” → link\_dn)).
      - Call the validation error handler Platform.throw(translated “{0} does not belong to Company {1}”.format(link\_dn, self.company)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L1944) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L476) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L658)

<a id="op-85ca144f3236e4"></a>
### POSProfile.validate write off settings

`operation_enterprise_binding_enterprise_accounts_doctype_pos_profile_pos_profile_posprofile_validate_write_off_settings`

**Inputs** self.

**Record and data access** read doctype via get\_value · read “Account” via get\_cached\_value.

**Explicit failure paths** validation helper — translated “{0} does not belong to Company {1}”.format(value, self.company) · validation helper — translated “{0} cannot be a group”.format(translated self.meta.get\_label(fieldname)) · validation helper — translated “Write Off Account must be a Profit and Loss account”.

**Local steps**

- For each tuple(fieldname, doctype) in tuple(tuple(“write\_off\_account”, “Account”), tuple(“write\_off\_cost\_center”, “Cost Center”)).
  - If not value bound to self.get(fieldname).
    - Continue with the next iteration or loop test.
  - Set tuple(company, is\_group) from Platform.db.get\_value(doctype, value, list(“company”, “is\_group”)).
  - If company differs from self.company.
    - Call the validation error handler Platform.throw(translated “{0} does not belong to Company {1}”.format(value, self.company)).
  - If is\_group.
    - Call the validation error handler Platform.throw(translated “{0} cannot be a group”.format(translated self.meta.get\_label(fieldname))).
  - If (doctype equals “Account” and Platform.get\_cached\_value(“Account”, value, “report\_type”) differs from “Profit and Loss”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in doctype equals “Account” → Platform.get\_cached\_value(“Account”, value, “report\_type”) differs from “Profit and Loss”.
    - Call the validation error handler Platform.throw(translated “Write Off Account must be a Profit and Loss account”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Account”, value, “report\_type”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0009.json#L170) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L268) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L906)

<a id="op-47caa933ca6965"></a>
### POSProfile.validate duplicate groups

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate_duplicate_groups`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Duplicate item group found in the item group table” · validation helper — translated “Duplicate customer group found in the customer group table”.

**Local steps**

- Set item\_groups from list of d.item\_group for d drawn from self.item\_groups.
  - Draw d from self.item\_groups.
- Set customer\_groups from list of d.customer\_group for d drawn from self.customer\_groups.
  - Draw d from self.customer\_groups.
- If len(item\_groups) differs from len(set(item\_groups)).
  - Call the validation error handler Platform.throw(translated “Duplicate item group found in the item group table”, title = translated “Duplicate Item Group”).
- If len(customer\_groups) differs from len(set(customer\_groups)).
  - Call the validation error handler Platform.throw(translated “Duplicate customer group found in the customer group table”, title = translated “Duplicate Customer Group”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L2283) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L479) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L661)

<a id="op-a172e9ea4d3a22"></a>
### POSProfile.validate payment methods

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_validate_payment_methods`

**Inputs** self.

**Record and data access** read “Mode of Payment Account” via get\_value.

**Explicit failure paths** validation helper — translated “Payment methods are mandatory. Please add at least one payment method.” · validation helper — translated “Please select a default mode of payment” · validation helper — translated “You can only select one mode of payment as default” · validation helper — msg.format(“, ”.join(invalid\_modes)).

**Local steps**

- If not self.payments.
  - Call the validation error handler Platform.throw(translated “Payment methods are mandatory. Please add at least one payment method.”).
- Set default\_mode from list of d.default for d drawn from self.payments where d.default.
  - Draw d from self.payments, keep a combination only if (d.default).
- If not default\_mode.
  - Call the validation error handler Platform.throw(translated “Please select a default mode of payment”).
- <a id="op-a172e9ea4d3a22-guard-9"></a>If len(default\_mode) &gt; 1.
  - Call the validation error handler Platform.throw(translated “You can only select one mode of payment as default”).
- Set invalid\_modes from list().
- For each d in self.payments.
  - Set account from Platform.db.get\_value(“Mode of Payment Account”, mapping(“parent” → d.mode\_of\_payment, “company” → self.company), “default\_account”).
  - If not account.
    - Evaluate invalid\_modes.append(get\_link\_to\_form(“Mode of Payment”, d.mode\_of\_payment)).
- If invalid\_modes.
  - If invalid\_modes equals 1.
    - Set msg from translated “Please set default Cash or Bank account in Mode of Payment {}”.
  - Otherwise.
    - Set msg from translated “Please set default Cash or Bank account in Mode of Payments {}”.
  - Call the validation error handler Platform.throw(msg.format(“, ”.join(invalid\_modes)), title = translated “Missing Account”).

If control reaches the end, it returns no value.

**Derived branch illustrations**

- At the comparison len(default\_mode) &gt; 1, length of default\_mode = 2 selects the branch that calls the validation-error handler with translated “You can only select one mode of payment as default”. With length of default\_mode = 1, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-a172e9ea4d3a22-guard-9)

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L40) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L480) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L662)

<a id="op-3e83c5cfbe33ef"></a>
### POSProfile.on update

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.set\_defaults().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set defaults](operations-083.md#op-447bc1e599c736).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L3241) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L471) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L653)

<a id="op-0c7ade81d9efee"></a>
### POSProfile.on trash

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.set\_defaults(include\_current\_pos = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set defaults](operations-083.md#op-447bc1e599c736).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L3292) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L470) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L652)

<a id="op-447bc1e599c736"></a>
### POSProfile.set defaults

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_set_defaults`

**Inputs** self, include\_current\_pos = true.

**Local steps**

- Evaluate Platform.defaults.clear\_default(“is\_pos”).
- Set pfu from Platform.qb.DocType(“POS Profile User”).
- Set query from nested operand in the contract.qb.from\_(pfu).select(pfu.user).where(pfu.default equals 1).
- If not include\_current\_pos.
  - Set query from query.where(pfu.name differs from self.name).
- Set pos\_view\_users from query.run(as\_list = 1, pluck = true).
- For each user in pos\_view\_users.
  - If user.
    - Evaluate Platform.defaults.set\_user\_default(“is\_pos”, 1, user).
  - Otherwise.
    - Evaluate Platform.defaults.set\_global\_default(“is\_pos”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L3354) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L473) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L655)

<a id="op-6ad5bc2272bbe7"></a>
### Get item groups

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_get_item_groups`

**Inputs** pos\_profile.

**Record and data access** resolve a document from “POS Profile” via get\_cached\_doc.

**Explicit results** list(set(item\_groups)).

**Local steps**

- Set item\_groups from list().
- Set pos\_profile from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).
- Set permitted\_item\_groups from get\_permitted\_nodes(“Item Group”).
- If pos\_profile.get(“item\_groups”).
  - For each data in pos\_profile.get(“item\_groups”).
    - Evaluate item\_groups.extend(list of d.name for d drawn from get\_child\_nodes(“Item Group”, data.item\_group) where (not permitted\_item\_groups or d.name belongs to permitted\_item\_groups)).
      - Draw d from get\_child\_nodes(“Item Group”, data.item\_group), keep a combination only if ((not permitted\_item\_groups or d.name belongs to permitted\_item\_groups)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not permitted\_item\_groups → d.name belongs to permitted\_item\_groups.
- If (not item\_groups and permitted\_item\_groups).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not item\_groups → permitted\_item\_groups.
  - Set item\_groups from list(permitted\_item\_groups).
- Return list(set(item\_groups)).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“POS Profile”, pos\_profile).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L3770) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L468) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L650)

<a id="op-b45d7972197350"></a>
### Get permitted nodes

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_get_permitted_nodes`

**Inputs** group\_type.

**Record and data access** read group\_type via get\_value.

**Explicit results** nodes.

**Local steps**

- Set nodes from list().
- Set permitted\_nodes from get\_permitted\_documents(group\_type).
- If not permitted\_nodes.
  - Return nodes.
- For each node in permitted\_nodes.
  - If Platform.db.get\_value(group\_type, node, “is\_group”).
    - Evaluate nodes.extend(list of d.name for d drawn from get\_child\_nodes(group\_type, node)).
      - Draw d from get\_child\_nodes(group\_type, node).
  - Otherwise.
    - Evaluate nodes.append(node).
- Return nodes.

**Values supplied outside this operation** effective access from get\_permitted\_documents(group\_type).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0128.json#L4141) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L469) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L651)

<a id="op-337f0fa8580e59"></a>
### Get child nodes

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_get_child_nodes`

**Inputs** group\_type, root.

**Record and data access** read group\_type via get\_value.

**State and service calls** execute a supplied database query.

**Explicit results** Platform.db.sql(formatted text  Select name, lft, rgt from ′tab{group\_type}′ where  lft &gt;= {lft} and rgt &lt;= {rgt} order by lft, as\_dict = 1).

**Local steps**

- Set tuple(lft, rgt) from Platform.db.get\_value(group\_type, root, list(“lft”, “rgt”)).
- Return Platform.db.sql(formatted text  Select name, lft, rgt from ′tab{group\_type}′ where  lft &gt;= {lft} and rgt &lt;= {rgt} order by lft, as\_dict = 1).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L36) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L467) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L649)

<a id="op-acefae2e0f8606"></a>
### Pos profile query

`operation_enterprise_accounts_record_definitions_point_of_sale_profile_business_behavior_point_of_sale_profile_query`

**Inputs** doctype, txt, searchfield, start, page\_len, filters.

**Wrappers, in declaration order** Platform.whitelist(), Platform.validate\_and\_sanitize\_search\_inputs.

**Record and data access** read “POS Profile” via get\_list.

**Explicit results** mapping() · pos\_profile.

**Local steps**

- Set user from Platform.session at “user”.
- Set company from (filters.get(“company”) or Platform.defaults.get\_user\_default(“company”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters.get(“company”) → Platform.defaults.get\_user\_default(“company”).
- Set allowed\_pos\_profiles from Platform.get\_list(“POS Profile”, pluck = “name”).
- If not allowed\_pos\_profiles.
  - Return mapping().
- Set pf from Platform.qb.DocType(“POS Profile”).
- Set pfu from Platform.qb.DocType(“POS Profile User”).
- Set pos\_profile from nested operand in the contract(nested operand in the contract).limit(page\_len).offset(start).run().
- If not pos\_profile.
  - Set pos\_profile from nested operand in the contract(nested operand in the contract).select(pf.name).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and nested operand in the contrac ….run().
- Return pos\_profile.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0004.json#L37) · [Binding](../../../current-decisions/enterprise/bindings-002.tsv#L472) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-002.tsv#L654)

## Report · Pos register

<a id="op-68b31077d76af2"></a>
### Execute

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_execute`

**Inputs** filters = no value.

**State and service calls** call insert on columns.

**Explicit results** tuple(list(), list()) · tuple(columns, pos\_entries) · tuple(columns, grouped\_data).

**Local steps**

- If not filters.
  - Return tuple(list(), list()).
- Evaluate validate\_filters(filters).
- Set columns from get\_columns(filters).
- Set group\_by\_field from get\_group\_by\_field(filters.get(“group\_by”)).
- Set pos\_entries from get\_pos\_entries(filters, group\_by\_field).
- If group\_by\_field differs from “mode\_of\_payment”.
  - Evaluate concat\_mode\_of\_payments(pos\_entries).
- If not group\_by\_field.
  - Return tuple(columns, pos\_entries).
- Set tuple(invoice\_map, grouped\_data) from tuple(mapping(), list()).
- For each d in pos\_entries.
  - Evaluate invoice\_map.setdefault(d at group\_by\_field, list()).append(d).
- For each key in invoice\_map.
  - Set invoices from invoice\_map at key.
  - Update grouped\_data using + invoices.
  - Evaluate add\_subtotal\_row(grouped\_data, invoices, group\_by\_field, key).
- Set column\_index from next(generator of index for tuple(index, d) drawn from enumerate(columns) where d at “fieldname” equals group\_by\_field, no value).
  - Draw tuple(index, d) from enumerate(columns), keep a combination only if (d at “fieldname” equals group\_by\_field).
- Evaluate columns.insert(0, columns.pop(column\_index)).
- Return tuple(columns, grouped\_data).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0268.json#L5523) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L810) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1152)

<a id="op-1796e1e97b503b"></a>
### Get pos entries

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_get_point_of_sale_entries`

**Inputs** filters, group\_by\_field.

**Explicit results** entries.

**Local steps**

- Set entries from get\_invoice\_entries(“POS Invoice”, filters, group\_by\_field).
- Update entries using + get\_invoice\_entries(“Sales Invoice”, filters, group\_by\_field).
- Set sort\_field from (group\_by\_field or “posting\_date”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in group\_by\_field → “posting\_date”.
- Evaluate entries.sort(key = deferred anonymous expression).
- If group\_by\_field equals “mode\_of\_payment”.
  - Evaluate show\_grand\_total\_once(entries).
- Return entries.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L814) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1156)

<a id="op-bfc314d8f3ee49"></a>
### Get invoice entries

`operation_enterprise_binding_enterprise_accounts_report_pos_register_pos_register_get_invoice_entries`

**Inputs** doctype, filters, group\_by\_field.

**Explicit results** list() · query.run(as\_dict = 1).

**Local steps**

- If not Platform.has\_permission(doctype, “select”).
  - Return list().
- Set p from Platform.qb.DocType(doctype).
- Set query from nested operand in the contract(nested operand in the contract).select(p.posting\_date, nested operand in the contract.as\_(“invoice\_type”), nested operand in the contract.as\_(“pos\_invoice”), p.pos\_profile, … ….
- If doctype equals “Sales Invoice”.
  - Set query from query.where((p.is\_pos equals 1 bitwise and p.is\_consolidated equals 0)).
- For each condition in get\_conditions(filters, p).
  - Set query from query.where(condition).
- If group\_by\_field equals “mode\_of\_payment”.
  - Set sip from Platform.qb.DocType(“Sales Invoice Payment”).
  - Set paid\_amount from (sip.base\_amount − Case().when(sip.type equals “Cash”, p.base\_change\_amount).else\_(0)).
  - Set query from nested operand in the contract(nested operand in the contract).on((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nested operand in t ….
- Otherwise.
  - Set query from query.select((p.base\_paid\_amount − p.base\_change\_amount).as\_(“paid\_amount”)).
- Return query.run(as\_dict = 1).

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “select”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1249)

<a id="op-d9c763357dfcd3"></a>
### Show grand total once

`operation_enterprise_binding_enterprise_accounts_report_pos_register_pos_register_show_grand_total_once`

**Inputs** entries.

**Local steps**

- Set seen from set().
- For each entry in entries.
  - Set invoice from tuple(entry.invoice\_type, entry.pos\_invoice).
  - If invoice belongs to seen.
    - Set entry.grand\_total from 0.
  - Evaluate seen.add(invoice).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0011.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L1250)

<a id="op-681164d4773a6a"></a>
### Concat mode of payments

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_concat_mode_of_payments`

**Inputs** pos\_entries.

**Local steps**

- Set mode\_of\_payments from get\_mode\_of\_payments(set(generator of d.pos\_invoice for d drawn from pos\_entries)).
  - Draw d from pos\_entries.
- For each entry in pos\_entries.
  - If mode\_of\_payments.get(entry.pos\_invoice).
    - Set entry.mode\_of\_payment from “, ”.join(mode\_of\_payments.get(entry.pos\_invoice, list())).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0268.json#L6970) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L809) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1151)

<a id="op-0d200ef9d7d372"></a>
### Add subtotal row

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_add_subtotal_row`

**Inputs** data, group\_invoices, group\_by\_field, group\_by\_value.

**Local steps**

- Set grand\_total from sum(generator of d.grand\_total for d drawn from group\_invoices).
  - Draw d from group\_invoices.
- Set paid\_amount from sum(generator of d.paid\_amount for d drawn from group\_invoices).
  - Draw d from group\_invoices.
- Evaluate data.append(mapping(group\_by\_field → group\_by\_value, “grand\_total” → grand\_total, “paid\_amount” → paid\_amount, “bold” → 1)).
- Evaluate data.append(mapping()).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0268.json#L7164) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L808) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1150)

<a id="op-0f8b6f7b89a346"></a>
### Validate filters

`operation_enterprise_accounts_report_point_of_sale_register_business_behavior_validate_filters`

**Inputs** filters.

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”) · validation helper — translated “{0} and {1} are mandatory”.format(Platform.bold(translated “From Date”), Platform.bold(translated “To Date”)) · validation helper — translated “Can not filter based on POS Profile, if grouped by POS Profile” · validation helper — translated “Can not filter based on Customer, if grouped by Customer” · validation helper — translated “Can not filter based on Cashier, if grouped by Cashier” · 1 additional forms in the steps below.

**Local steps**

- If not filters.get(“company”).
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- If (not filters.get(“from\_date”) or not filters.get(“to\_date”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not filters.get(“from\_date”) → not filters.get(“to\_date”).
  - Call the validation error handler Platform.throw(translated “{0} and {1} are mandatory”.format(Platform.bold(translated “From Date”), Platform.bold(translated “To Date”))).
- Evaluate validate\_date\_range(filters).
- If (filters.get(“pos\_profile”) and filters.get(“group\_by”) equals translated “POS Profile”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“pos\_profile”) → filters.get(“group\_by”) equals translated “POS Profile”.
  - Call the validation error handler Platform.throw(translated “Can not filter based on POS Profile, if grouped by POS Profile”).
- If (filters.get(“customer”) and filters.get(“group\_by”) equals translated “Customer”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“customer”) → filters.get(“group\_by”) equals translated “Customer”.
  - Call the validation error handler Platform.throw(translated “Can not filter based on Customer, if grouped by Customer”).
- If (filters.get(“owner”) and filters.get(“group\_by”) equals translated “Cashier”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“owner”) → filters.get(“group\_by”) equals translated “Cashier”.
  - Call the validation error handler Platform.throw(translated “Can not filter based on Cashier, if grouped by Cashier”).
- If (filters.get(“mode\_of\_payment”) and filters.get(“group\_by”) equals translated “Payment Method”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in filters.get(“mode\_of\_payment”) → filters.get(“group\_by”) equals translated “Payment Method”.
  - Call the validation error handler Platform.throw(translated “Can not filter based on Payment Method, if grouped by Payment Method”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L32) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L815) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-003.tsv#L1157)
