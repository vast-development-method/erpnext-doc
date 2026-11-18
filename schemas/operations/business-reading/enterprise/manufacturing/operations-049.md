# Production · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Workstation type

[Record definition](../../../../data/record-types/workstation_type.json)

<a id="op-5aec5a0cc4651c"></a>
### Workstation Type.before save

`operation_enterprise_manufacturing_record_definitions_workstation_type_business_behavior_workstation_type_before_save`

**Inputs** self.

**Local steps**

- Evaluate self.set\_hour\_rate().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set hour rate](operations-049.md#op-0cad6ba4044354).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L6763) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L92) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1011)

<a id="op-0cad6ba4044354"></a>
### Workstation Type.set hour rate

`operation_enterprise_manufacturing_record_definitions_workstation_type_business_behavior_workstation_type_set_hour_rate`

**Inputs** self.

**Local steps**

- Set self.hour\_rate from 0.0.
- For each row in self.workstation\_costs.
  - If row.operating\_cost.
    - Update self.hour\_rate using + flt(row.operating\_cost).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0536.json#L6814) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L93) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1012)

<a id="op-9eb15bac209f81"></a>
### Workstation Type.on update

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_type_workstation_type_workstationtype_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.update\_workstation\_costs().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update workstation costs](operations-049.md#op-dcb2b8c4cb1385).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L184) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1116)

<a id="op-dcb2b8c4cb1385"></a>
### Workstation Type.update workstation costs

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_type_workstation_type_workstationtype_update_workstation_costs`

**Inputs** self.

**Record and data access** resolve a document from “Workstation” via get\_doc.

**State and service calls** call save on workstation.

**Explicit results** no value.

**Local steps**

- Set previous from self.get\_doc\_before\_save().
- If not previous.
  - Return no value.
- Set old\_costs from get\_cost\_map(previous.workstation\_costs).
- If old\_costs equals get\_cost\_map(self.workstation\_costs).
  - Return no value.
- For each name in self.get\_workstations\_with\_costs(old\_costs).
  - Set workstation from Platform.get\_doc(“Workstation”, name).
  - Set workstation.workstation\_costs from list().
  - For each row in self.workstation\_costs.
    - Evaluate workstation.append(“workstation\_costs”, mapping(“operating\_component” → row.operating\_component, “operating\_cost” → row.operating\_cost)).
  - Evaluate workstation.save().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get workstations with costs](operations-049.md#op-e65bdcd5d78c2c).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L185) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1117)

<a id="op-e65bdcd5d78c2c"></a>
### Workstation Type.get workstations with costs

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_type_workstation_type_workstationtype_get_workstations_with_costs`

**Inputs** self, costs.

**Explicit results** list of name for tuple(name, rows) drawn from workstation\_costs.items() where get\_cost\_map(rows) equals costs.

**Local steps**

- Set workstation from Platform.qb.DocType(“Workstation”).
- Set cost from Platform.qb.DocType(“Workstation Cost”).
- Set rows from nested operand in the contract(nested operand in the contract).select(workstation.name, cost.operating\_component, cost.operating\_cost).where(workstation.workstation\_type equals self.name).run(as\_dict = true).
- Set workstation\_costs from mapping().
- For each row in rows.
  - Evaluate workstation\_costs.setdefault(row.name, list()).
  - If row.operating\_component.
    - Evaluate workstation\_costs at row.name.append(row).
- Return list of name for tuple(name, rows) drawn from workstation\_costs.items() where get\_cost\_map(rows) equals costs.
  - Draw tuple(name, rows) from workstation\_costs.items(), keep a combination only if (get\_cost\_map(rows) equals costs).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L183) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L105) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1115)

<a id="op-0ce4027c7f614f"></a>
### Get cost map

`operation_enterprise_binding_enterprise_manufacturing_doctype_workstation_type_workstation_type_get_cost_map`

**Inputs** rows.

**Explicit results** mapping of row.operating\_component → flt(row.operating\_cost) for row drawn from rows.

**Local steps**

- Return mapping of row.operating\_component → flt(row.operating\_cost) for row drawn from rows.
  - Draw row from rows.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0017.json#L182) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L104) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L1114)

<a id="op-79d13155bc8d39"></a>
### Get workstations

`operation_enterprise_manufacturing_record_definitions_workstation_type_business_behavior_get_workstations`

**Inputs** workstation\_type.

**Record and data access** read “Workstation” via get\_all.

**Explicit results** list of workstation.name for workstation drawn from workstations.

**Local steps**

- Set workstations from Platform.get\_all(“Workstation”, filters = mapping(“workstation\_type” → workstation\_type, “disabled” → 0), order\_by = “creation”).
- Return list of workstation.name for workstation drawn from workstations.
  - Draw workstation from workstations.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0032.json#L144) · [Binding](../../../current-decisions/enterprise/bindings-008.tsv#L91) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L1010)
