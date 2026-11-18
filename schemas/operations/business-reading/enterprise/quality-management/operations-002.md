# Quality assurance · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Quality review

[Record definition](../../../../data/record-types/quality_review.json)

<a id="op-0e929bbdd85108"></a>
### Is review date

`operation_enterprise_binding_enterprise_quality_management_doctype_quality_review_quality_review_is_review_date`

**Inputs** goal\_date, today.

**Explicit results** min(cint(goal\_date), get\_last\_day(today).day) equals today.day.

**Local steps**

- Return min(cint(goal\_date), get\_last\_day(today).day) equals today.day.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L259) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L374) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1384)

<a id="op-b0f7ee0a1cd1c5"></a>
### Create review

`operation_enterprise_quality_management_record_definitions_quality_review_business_behavior_create_review`

**Inputs** goal.

**Record and data access** read “Quality Review” via exists · resolve a document from mapping(“doctype” → “Quality Review”, “goal” → goal, “date” → date) via get\_doc.

**State and service calls** call insert on review.

**Explicit results** no value.

**Local steps**

- Set date from Platform.utils.getdate().
- If Platform.db.exists(“Quality Review”, mapping(“goal” → goal, “date” → date)).
  - Return no value.
- Set review from Platform.get\_doc(mapping(“doctype” → “Quality Review”, “goal” → goal, “date” → date)).
- Evaluate review.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0033.json#L160) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1508) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L930)

<a id="op-1dc9f507eb8de2"></a>
### Get quarter

`operation_enterprise_quality_management_record_definitions_quality_review_business_behavior_get_quarter`

**Inputs** month.

**Explicit results** true · false.

**Local steps**

- If month belongs to list(“January”, “April”, “July”, “October”).
  - Return true.
- Otherwise.
  - Return false.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0614.json#L3972) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L1509) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-009.tsv#L931)

## Report · Review

<a id="op-53dcb7f64d2d13"></a>
### Execute

`operation_enterprise_binding_enterprise_quality_management_report_review_review_execute`

**Inputs** filters = no value.

**Explicit results** tuple(get\_columns(), get\_data()).

**Local steps**

- Return tuple(get\_columns(), get\_data()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L263) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L378) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1388)

<a id="op-457efed98f17e8"></a>
### Get columns

`operation_enterprise_binding_enterprise_quality_management_report_review_review_get_columns`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“label” → translated “Name”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Quality Action”, …), mapping(“label” → translated “Action”, “fieldname” → “corrective\_preventive”, “fieldt ….

**Local steps**

- Return list(mapping(“label” → translated “Name”, “fieldname” → “name”, “fieldtype” → “Link”, “options” → “Quality Action”, …), mapping(“label” → translated “Action”, “fieldname” → “corrective\_preventive”, “fieldt ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L264) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L379) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1389)

<a id="op-237aa55b99a52d"></a>
### Get data

`operation_enterprise_binding_enterprise_quality_management_report_review_review_get_data`

**Inputs** no declared parameters.

**Record and data access** read “Quality Action” via get\_list.

**Explicit results** Platform.get\_list(“Quality Action”, filters = mapping(“review” → list(“is”, “set”)), fields = list(“name”, “corrective\_preventive”, “review”, “date”, …)).

**Local steps**

- Return Platform.get\_list(“Quality Action”, filters = mapping(“review” → list(“is”, “set”)), fields = list(“name”, “corrective\_preventive”, “review”, “date”, …)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0018.json#L265) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1390)
