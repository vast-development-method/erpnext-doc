# Shared transaction rules · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Employee reminders

<a id="op-901641a1863352"></a>
### Get sender email

`operation_workforce_controllers_employee_reminders_business_behavior_get_sender_email`

**Inputs** no declared parameters.

**Declared result** (str bitwise or no value).

**Record and data access** read “HR Settings” via get\_single\_value.

**Explicit results** Platform.db.get\_single\_value(“HR Settings”, “sender\_email”).

**Local steps**

- Return Platform.db.get\_single\_value(“HR Settings”, “sender\_email”).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“HR Settings”, “sender\_email”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0005.json#L2182) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L273) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L273)
