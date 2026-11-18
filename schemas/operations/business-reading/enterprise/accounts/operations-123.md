# Accounting and settlement · operations 123

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-e1f333db2ea42a"></a>
### Update subscription on invoice update

`operation_enterprise_accounts_utils_business_behavior_update_subscription_on_invoice_update`

**Inputs** doc, method = no value.

**Declared result** no value.

**Local steps**

- If doc.get(“subscription”).
  - Evaluate refresh\_subscription\_status(doc.subscription).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L5831) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1354) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L254)

<a id="op-5e367401531c1e"></a>
### Refresh subscription status

`operation_enterprise_accounts_utils_business_behavior_refresh_subscription_status`

**Inputs** name.

**Declared result** no value.

**Record and data access** resolve a document from “Subscription” via get\_doc.

**State and service calls** call save on subscription.

**Local steps**

- Set subscription from Platform.get\_doc(“Subscription”, name).
- Evaluate subscription.set\_subscription\_status().
- Evaluate subscription.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0306.json#L5950) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1339) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L240)

## Report · Voucher wise balance

<a id="op-e1c7a9925cd3c1"></a>
### Execute

`operation_enterprise_accounts_report_voucher_wise_balance_business_behavior_execute`

**Inputs** filters = no value.

**Explicit results** tuple(columns, data).

**Explicit failure paths** validation helper — translated “{0} is mandatory”.format(translated “Company”).

**Local steps**

- Evaluate validate\_date\_range(filters).
- If not (filters or mapping()).get(“company”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in filters → mapping().
  - Call the validation error handler Platform.throw(translated “{0} is mandatory”.format(translated “Company”)).
- Set columns from get\_columns().
- Set data from get\_data(filters).
- Return tuple(columns, data).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1077) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L148)

<a id="op-d91dcc5bef67a2"></a>
### Get columns

`operation_enterprise_accounts_report_voucher_wise_balance_business_behavior_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Voucher No”, “fieldname” → “voucher\_no”, “fiel ….

**Local steps**

- Return list(mapping(“label” → translated “Voucher Type”, “fieldname” → “voucher\_type”, “fieldtype” → “Link”, “options” → “DocType”, …), mapping(“label” → translated “Voucher No”, “fieldname” → “voucher\_no”, “fiel ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1078) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L149)

<a id="op-c991b7acad880e"></a>
### Get data

`operation_enterprise_accounts_report_voucher_wise_balance_business_behavior_get_data`

**Inputs** filters.

**Explicit results** apply\_filters(query, filters, gle).run(as\_dict = true).

**Local steps**

- Set gle from Platform.qb.DocType(“GL Entry”).
- Set query from nested operand in the contract(nested operand in the contract, nested operand in the contract, nested operand in the contract, nested operand in the contract).where(nested operand in the contract.is\_cancel ….
- Return apply\_filters(query, filters, gle).run(as\_dict = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1079) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L150)

<a id="op-e16432cf287fa2"></a>
### Apply filters

`operation_enterprise_accounts_report_voucher_wise_balance_business_behavior_apply_filters`

**Inputs** query, filters, gle.

**Explicit results** query.

**Local steps**

- Set query from query.where(gle.company equals filters.company).
- If filters.get(“voucher\_type”).
  - Set query from query.where(gle.voucher\_type equals filters.voucher\_type).
- If filters.get(“from\_date”).
  - Set query from query.where(gle.posting\_date ≥ filters.from\_date).
- If filters.get(“to\_date”).
  - Set query from query.where(gle.posting\_date ≤ filters.to\_date).
- Return query.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0007.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-003.tsv#L1076) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-004.tsv#L147)
