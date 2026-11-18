# Payroll and benefits · operations 22

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-6fe5d15d7ba76d"></a>
### Get conditions

`operation_workforce_binding_workforce_payroll_utils_get_conditions`

**Inputs** filters.

**Explicit results** filter\_clauses.

**Local steps**

- Set SalarySlip from DocType(“Salary Slip”).
- Set filter\_clauses from list().
- If filters.get(“department”).
  - Evaluate filter\_clauses.append(SalarySlip.department equals filters at “department”).
- If filters.get(“branch”).
  - Evaluate filter\_clauses.append(SalarySlip.branch equals filters at “branch”).
- If filters.get(“company”).
  - Evaluate filter\_clauses.append(SalarySlip.company equals filters at “company”).
- If filters.get(“month”).
  - Evaluate filter\_clauses.append(Extract(“month”, SalarySlip.start\_date) equals int(filters at “month”)).
- If filters.get(“year”).
  - Evaluate filter\_clauses.append(Extract(“year”, SalarySlip.start\_date) equals int(filters at “year”)).
- If filters.get(“mode\_of\_payment”).
  - Evaluate filter\_clauses.append(SalarySlip.mode\_of\_payment equals filters at “mode\_of\_payment”).
- Return filter\_clauses.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L184) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L235) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L235)

<a id="op-edba79157c9255"></a>
### Get years

`operation_workforce_binding_workforce_payroll_utils_get_years`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** whitespace '\\n'.join(generator of str(year) for year drawn from year\_list).

**Local steps**

- Set SalarySlip from DocType(“Salary Slip”).
- Set year\_list from nested operand in the contract(nested operand in the contract).distinct().orderby(Extract(“year”, SalarySlip.end\_date), order = Platform.qb.desc).run(pluck = true).
- If not year\_list.
  - Set year\_list from list(getdate().year).
- Return whitespace '\\n'.join(generator of str(year) for year drawn from year\_list).
  - Draw year from year\_list.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/workforce/procedures-0001.json#L185) · [Binding](../../../current-decisions/workforce/bindings-001.tsv#L236) · [Declaration location](../../../current-decisions/workforce/evidence/locations-001.tsv#L236)
