# Employment and attendance · operations 45

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Vehicle log

[Record definition](../../../../data/record-types/vehicle_log.json)

<a id="op-72d901b012f2bf"></a>
### Has non vehicle log expenses

`operation_workforce_human_resources_record_definitions_vehicle_log_business_behavior_has_non_vehicle_log_expenses`

**Inputs** expense\_claim.

**Declared result** bool.

**Explicit results** any(generator of row.description differs from vehicle\_log\_description for row drawn from expense\_claim.expenses).

**Local steps**

- Set vehicle\_log\_description from translated “Vehicle Expenses”.
- Return any(generator of row.description differs from vehicle\_log\_description for row drawn from expense\_claim.expenses).
  - Draw row from expense\_claim.expenses.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../workforce-decision-contracts/part-0079.json#L1831) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L1633) · [Declaration location](../../../current-decisions/workforce/evidence/locations-002.tsv#L242)
