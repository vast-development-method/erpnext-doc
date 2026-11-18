# Regional rules and controller overrides · operations 1

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Assignment rule

<a id="op-2f1189045c45d5"></a>
### CRMAssignment Rule.get user

`operation_relationships_binding_crm_overrides_assignment_rule_crmassignmentrule_get_user`

**Inputs** self, doc.

**Explicit results** super().get\_user(doc).

**Local steps**

- Set fieldname from USER\_POOL\_FIELDS.get(self.rule).
- If (self.document\_type does not belong to CRM\_DOCTYPES or not fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.document\_type does not belong to CRM\_DOCTYPES → not fieldname.
  - Return super().get\_user(doc).
- Set pool from getattr(self, fieldname).
- Set categories from get\_user\_categories(list of row.user for row drawn from pool where row.user).
  - Draw row from pool, keep a combination only if (row.user).
- Set active from list of row for row drawn from pool where categories.get(row.user) equals “Active”.
  - Draw row from pool, keep a combination only if (categories.get(row.user) equals “Active”).
- Set reachable from list of row for row drawn from pool where categories.get(row.user) belongs to tuple(“Active”, “Away”).
  - Draw row from pool, keep a combination only if (categories.get(row.user) belongs to tuple(“Active”, “Away”)).
- Evaluate setattr(self, fieldname, (active or reachable or pool)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in active → reachable → pool.
- Attempt the following.
  - Return super().get\_user(doc).
- On exit, including pending return or failure.
  - Evaluate setattr(self, fieldname, pool).

**Values supplied outside this operation** selected callable from getattr(self, fieldname).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L215) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L371) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L352)

## Service · Contact

<a id="op-5e114f740ee326"></a>
### Custom Contact.default list data

`operation_relationships_overrides_contact_business_behavior_custom_contact_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Name”, “type” → “Data”, “key” → “full\_name”, “width” → “17rem”), mapping(“label” → “Email”, “type” → “Data”, “key” → “email\_id”, “width” → “12rem”), mapping(“label” → “Phone”, “type ….
- Set rows from list(“name”, “full\_name”, “company\_name”, “email\_id”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L3259) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1416) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1392)

## Service · Data import

<a id="op-224ded0dad9fca"></a>
### Data Import List View.default list data

`operation_relationships_binding_crm_overrides_data_import_dataimportlistview_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “ID”, “type” → “Data”, “key” → “name”, “width” → “16rem”), mapping(“label” → “Status”, “type” → “Select”, “key” → “status”, “width” → “10rem”), mapping(“label” → “Document Type”, “ty ….
- Set rows from list(“name”, “status”, “reference\_doctype”, “import\_type”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L216) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L372) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L353)

## Service · Email template

<a id="op-e95ac208fcf00d"></a>
### Custom Email Template.default list data

`operation_relationships_overrides_email_template_business_behavior_custom_email_template_default_list_data`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Explicit results** mapping(“columns” → columns, “rows” → rows).

**Local steps**

- Set columns from list(mapping(“label” → “Name”, “type” → “Data”, “key” → “name”, “width” → “17rem”), mapping(“label” → “Subject”, “type” → “Data”, “key” → “subject”, “width” → “12rem”), mapping(“label” → “Enabled”, “type”  ….
- Set rows from list(“name”, “enabled”, “use\_html”, “reference\_doctype”, …).
- Return mapping(“columns” → columns, “rows” → rows).

**Boundaries to resolve** abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0055.json#L3787) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L1417) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L1393)

## Service · Notification log

<a id="op-212d1d959c20fb"></a>
### Before insert

`operation_relationships_extends_notification_log_business_behavior_before_insert`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- If doc.link.
  - Return no value.
- Set route from get\_crm\_route(doc.document\_type, doc.document\_name).
- If route.
  - Set doc.link from Platform.utils.get\_url(route).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L2112) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L743) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L724)

<a id="op-8a5e87754e140b"></a>
### Get crm route

`operation_relationships_extends_notification_log_business_behavior_get_customer_relationship_route`

**Inputs** doctype, name.

**Record and data access** read “CRM Task” via get\_value.

**Explicit results** no value · formatted text /crm/{list\_route}/{name}{suffix}.

**Local steps**

- If not name.
  - Return no value.
- Set suffix from empty text.
- If doctype equals “CRM Task”.
  - Set parent from Platform.db.get\_value(“CRM Task”, name, list(“reference\_doctype”, “reference\_docname”), as\_dict = true).
  - If (not parent or not parent.reference\_docname).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not parent → not parent.reference\_docname.
    - Return no value.
  - Set tuple(doctype, name) from tuple(parent.reference\_doctype, parent.reference\_docname).
  - Set suffix from “#tasks”.
- Set list\_route from CRM\_ROUTES.get(doctype).
- If not list\_route.
  - Return no value.
- Return formatted text /crm/{list\_route}/{name}{suffix}.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0028.json#L2261) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L744) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L725)
