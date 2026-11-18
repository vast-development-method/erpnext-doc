# Equipment maintenance · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Maintenance visit

[Record definition](../../../../data/record-types/maintenance_visit.json)

<a id="op-d8ff3b480058f7"></a>
### Get bundle deliveries

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_get_bundle_deliveries`

**Inputs** serial\_no.

**Declared result** list.

**Explicit results** nested operand in the contract(nested operand in the contract).select(entry.voucher\_type, entry.voucher\_no).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and  ….

**Local steps**

- Set entry from Platform.qb.DocType(“Serial and Batch Entry”).
- Return nested operand in the contract(nested operand in the contract).select(entry.voucher\_type, entry.voucher\_no).where(((((nested operand in the contract bitwise and nested operand in the contract) bitwise and  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L109) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1358) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L598)

<a id="op-8d06ed95e16416"></a>
### Get legacy deliveries

`operation_enterprise_binding_enterprise_maintenance_doctype_maintenance_visit_maintenance_visit_get_legacy_deliveries`

**Inputs** serial\_no, item\_code.

**Declared result** list.

**Record and data access** read “Stock Ledger Entry” via get\_all.

**Explicit results** list of entry for entry drawn from entries where serial\_no belongs to get\_serial\_nos(entry.serial\_no).

**Local steps**

- Set entries from Platform.get\_all(“Stock Ledger Entry”, filters = mapping(“item\_code” → item\_code, “serial\_no” → list(“like”, formatted text %{serial\_no}%), “actual\_qty” → list(“&lt;”, 0), “is\_cancelled” → 0, …), fields = lis ….
- Return list of entry for entry drawn from entries where serial\_no belongs to get\_serial\_nos(entry.serial\_no).
  - Draw entry from entries, keep a combination only if (serial\_no belongs to get\_serial\_nos(entry.serial\_no)).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0015.json#L110) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1359) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L599)
