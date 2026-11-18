# Sales relationships · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-b0dcde6a1a9ea2"></a>
### Get closed events

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_closed_events`

**Inputs** ref\_doctype, ref\_docname.

**Explicit results** get\_filtered\_events(ref\_doctype, ref\_docname, open = false).

**Local steps**

- Return get\_filtered\_events(ref\_doctype, ref\_docname, open = false).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L1460) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L64) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1363)

<a id="op-d66a39114c4b4e"></a>
### Can read source

`operation_enterprise_binding_enterprise_crm_utils_can_read_source`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doctype, docname, ignore\_permissions.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** effective access lookup.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L87) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1336) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L576)

<a id="op-b3bdded99f7aea"></a>
### Get filtered todos

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_filtered_todos`

**Inputs** ref\_doctype, ref\_docname, status.

**Record and data access** read “ToDo” via get\_all.

**Explicit results** Platform.get\_all(“ToDo”, filters = mapping(“reference\_type” → ref\_doctype, “reference\_name” → ref\_docname, “status” → status), fields = list(“name”, “description”, “allocated\_to”, “date”), order\_by = “date asc”).

**Local steps**

- Return Platform.get\_all(“ToDo”, filters = mapping(“reference\_type” → ref\_doctype, “reference\_name” → ref\_docname, “status” → status), fields = list(“name”, “description”, “allocated\_to”, “date”), order\_by = “date asc”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L1534) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L67) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1366)

<a id="op-7c9a7044452aee"></a>
### Get filtered events

`operation_enterprise_customer_relationship_management_utils_business_behavior_get_filtered_events`

**Inputs** ref\_doctype, ref\_docname, open.

**Explicit results** data.

**Local steps**

- Set event from Platform.qb.DocType(“Event”).
- Set event\_link from Platform.qb.DocType(“Event Participants”).
- If open.
  - Set event\_status\_filter from event.status equals “Open”.
- Otherwise.
  - Set event\_status\_filter from event.status differs from “Open”.
- Set query from nested operand in the contract(nested operand in the contract).select(event.name, event.subject, event.event\_category, event.starts\_on, …).where(((nested operand in the contract.reference\_doctype equals re ….
- Set data from query.run(as\_dict = true).
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0444.json#L1753) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L66) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1365)

<a id="op-b2f4a32e202468"></a>
### Open leads opportunities based on todays event

`operation_enterprise_customer_relationship_management_utils_business_behavior_open_leads_opportunities_based_on_todays_event`

**Inputs** no declared parameters.

**State and service calls** request set\_value on d.reference\_doctype.

**Local steps**

- Set event from Platform.qb.DocType(“Event”).
- Set event\_link from Platform.qb.DocType(“Event Participants”).
- Set query from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.parent equals nested operand in the contract.name).select(event\_link.reference\_doctype, event\_link.reference ….
- Set data from query.run(as\_dict = true).
- For each d in data.
  - Evaluate Platform.db.set\_value(d.reference\_doctype, mapping(“name” → d.reference\_docname, “status” → tuple(“in”, STATUSES\_REOPENED\_BY\_EVENT at d.reference\_doctype)), “status”, “Open”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L150) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L78) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1377)

<a id="op-631749a0e2c9f1"></a>
### CRMNote.add note

`operation_enterprise_customer_relationship_management_utils_business_behavior_customer_relationship_note_add_note`

**Inputs** self, note.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Local steps**

- Evaluate self.append(“notes”, mapping(“note” → note, “added\_by” → Platform.session.user, “added\_on” → now())).
- Evaluate self.save().
- Evaluate notify\_mentions(self.doctype, self.name, note).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** stored data, callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L143) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L60) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1359)

<a id="op-350c3699a662c0"></a>
### CRMNote.edit note

`operation_enterprise_customer_relationship_management_utils_business_behavior_customer_relationship_note_edit_note`

**Inputs** self, note, row\_id.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Local steps**

- For each d in self.notes.
  - If cstr(d.name) equals row\_id.
    - Set d.note from note.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L145) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L62) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1361)

<a id="op-6cf839493d835b"></a>
### CRMNote.delete note

`operation_enterprise_customer_relationship_management_utils_business_behavior_customer_relationship_note_delete_note`

**Inputs** self, row\_id.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call save on self.

**Local steps**

- For each d in self.notes.
  - If cstr(d.name) equals row\_id.
    - Evaluate self.remove(d).
    - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0030.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L61) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L1360)
