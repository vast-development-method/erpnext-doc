# Purchasing · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Supplier scorecard period

[Record definition](../../../../data/record-types/supplier_scorecard_period.json)

<a id="op-74a0a4a7b38b7f"></a>
### Supplier Scorecard Period.get eval statement

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_supplier_scorecard_period_get_evaluate_statement`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, formula.

**Explicit result forms** a value selected from the current context.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L388) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L136)

<a id="op-dccaae947b10af"></a>
### Has overlapping period

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_period_supplier_scorecard_period_has_overlapping_period`

**Inputs** scorecard, start\_date, end\_date.

**Explicit results** bool(get\_overlapping\_period\_end(scorecard, start\_date, end\_date)).

**Local steps**

- Return bool(get\_overlapping\_period\_end(scorecard, start\_date, end\_date)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L180) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L842) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L82)

<a id="op-0239700b921db8"></a>
### Get overlapping period end

`operation_enterprise_binding_enterprise_buying_doctype_supplier_scorecard_period_supplier_scorecard_period_get_overlapping_period_end`

**Inputs** scorecard, start\_date, end\_date.

**Record and data access** read “Supplier Scorecard Period” via get\_all.

**Explicit results** ends at 0 when ends, otherwise no value.

**Local steps**

- Set ends from Platform.get\_all(“Supplier Scorecard Period”, filters = mapping(“scorecard” → scorecard, “docstatus” → 1, “start\_date” → list(“&lt;=”, end\_date), “end\_date” → list(“&gt;=”, start\_date)), pluck = “end\_date”, orde ….
- Return ends at 0 when ends, otherwise no value.
  - Value choice on ends — true gives ends at 0, false gives no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0012.json#L179) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L841) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L81)

<a id="op-9876092df20b0e"></a>
### Import string path

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_import_string_path`

**Inputs** path.

**Explicit results** mod.

**Local steps**

- Set components from path.split(“.”).
- Set mod from \_\_import\_\_(components at 0).
- For each comp in components at slice 1 to no value.
  - Set mod from getattr(mod, comp).
- Return mod.

**Values supplied outside this operation** selected callable from getattr(mod, comp).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L317) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L380) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L128)

<a id="op-d42572db7af719"></a>
### Make supplier scorecard

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_make_supplier_scorecard`

**Inputs** source\_name, target\_doc = no value.

**Explicit results** doc.

**Local steps**

- Bind local operation update\_criteria\_fields for subsequent calls.
- Bind local operation post\_process for subsequent calls.
- Set doc from get\_mapped\_doc(“Supplier Scorecard”, source\_name, mapping(“Supplier Scorecard” → mapping(“doctype” → “Supplier Scorecard Period”), “Supplier Scorecard Scoring Criteria” → mapping(“doctype” → “Supplier Scor ….
- Return doc.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L476) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L381) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L129)

<a id="op-f81408be627e54"></a>
### Make supplier scorecard.update criteria fields

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_make_supplier_scorecard_update_criteria_fields`

**Inputs** obj, target, source\_parent.

**Record and data access** read “Supplier Scorecard Criteria” via get\_value.

**Local steps**

- Set tuple(target.max\_score, target.formula) from Platform.db.get\_value(“Supplier Scorecard Criteria”, obj.criteria\_name, list(“max\_score”, “formula”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L955) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L383) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L131)

<a id="op-5cc5bf336af170"></a>
### Make supplier scorecard.post process

`operation_enterprise_buying_record_definitions_supplier_scorecard_period_business_behavior_make_supplier_scorecard_post_process`

**Inputs** source, target.

**Local steps**

- Set variables from list().
- For each cr in target.criteria.
  - For each var in get\_variables(cr.criteria\_name).
    - If var does not belong to variables.
      - Evaluate variables.append(var).
- Evaluate target.extend(“variables”, variables).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L1086) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L382) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L130)

## Record · Supplier scorecard standing

[Record definition](../../../../data/record-types/supplier_scorecard_standing.json)

<a id="op-56a37142adffb5"></a>
### Get scoring standing

`operation_enterprise_buying_record_definitions_supplier_scorecard_standing_business_behavior_get_scoring_standing`

**Inputs** standing\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Supplier Scorecard Standing” via get\_doc.

**Explicit results** standing.

**Local steps**

- Set standing from Platform.get\_doc(“Supplier Scorecard Standing”, standing\_name).
- Evaluate standing.check\_permission(“read”).
- Return standing.

**Values supplied outside this operation** effective access from standing.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L12) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L397) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L140)

<a id="op-ed5e2dae7a0790"></a>
### Get standings list

`operation_enterprise_buying_record_definitions_supplier_scorecard_standing_business_behavior_get_standings_list`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Supplier Scorecard Standing” via get\_list.

**Explicit results** standings.

**Local steps**

- Set standings from Platform.get\_list(“Supplier Scorecard Standing”, fields = list(“name”)).
- Return standings.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L13) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L398) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L141)

## Record · Supplier scorecard variable

[Record definition](../../../../data/record-types/supplier_scorecard_variable.json)

<a id="op-3dbdd15016cdee"></a>
### Supplier Scorecard Variable.validate

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_supplier_scorecard_variable_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_path\_exists().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate path exists](operations-013.md#op-f6a3554acb41ff).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L2832) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L435) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L172)

<a id="op-f6a3554acb41ff"></a>
### Supplier Scorecard Variable.validate path exists

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_supplier_scorecard_variable_validate_path_exists`

**Inputs** self.

**Explicit failure paths** validation helper with VariablePathNotFound — translated (“Could not find path for ” + self.path).

**Local steps**

- If “.” belongs to self.path.
  - Attempt the following.
    - Bind dependencies import\_string\_path.
    - Evaluate import\_string\_path(self.path).
  - On failure (AttributeError).
    - Call the validation error handler Platform.throw(translated (“Could not find path for ” + self.path), VariablePathNotFound).
- Otherwise.
  - If not hasattr(sys.modules at \_\_name\_\_, self.path).
    - Call the validation error handler Platform.throw(translated (“Could not find path for ” + self.path), VariablePathNotFound).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L34) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L436) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L173)

<a id="op-db44a6c7455e14"></a>
### Get total workdays

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_workdays`

**Inputs** scorecard.

**Explicit results** (date\_diff(scorecard.end\_date, scorecard.start\_date) + 1).

**Local steps**

- Return (date\_diff(scorecard.end\_date, scorecard.start\_date) + 1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L33) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L434) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L171)

<a id="op-3f47e0714c0173"></a>
### Get item workdays

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_item_workdays`

**Inputs** scorecard.

**Explicit results** (result at 0 at 0 or 0).

**Local steps**

- Set PO from Platform.qb.DocType(“Purchase Order”).
- Set PO\_Item from Platform.qb.DocType(“Purchase Order Item”).
- Set result from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.received\_qty &lt; nested operand in the contract.qty).where(PO\_Item.schedule\_date at slice scorecard.start\_d ….run().
- Return (result at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result at 0 at 0 → 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L16) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L415) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L152)

<a id="op-488e5508522936"></a>
### Get total cost of shipments

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_cost_of_shipments`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase).

**Explicit results** data · 0.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If data.
  - Return data.
- Otherwise.
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L426) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L163)

<a id="op-764c502091f242"></a>
### Get cost of delayed shipments

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_cost_of_delayed_shipments`

**Inputs** scorecard.

**Explicit results** (get\_total\_cost\_of\_shipments(scorecard) − get\_cost\_of\_on\_time\_shipments(scorecard)).

**Local steps**

- Return (get\_total\_cost\_of\_shipments(scorecard) − get\_cost\_of\_on\_time\_shipments(scorecard)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0353.json#L4233) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L412) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L149)

<a id="op-41b611f0b4eb64"></a>
### Get cost of on time shipments

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_cost_of_on_time_shipments`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase).

**Explicit results** total\_delivered\_on\_time\_costs · 0.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set total\_delivered\_on\_time\_costs from Platform.db.sql(query text (SELECT, Purchase), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If total\_delivered\_on\_time\_costs.
  - Return total\_delivered\_on\_time\_costs.
- Otherwise.
  - Return 0.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L15) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L413) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L150)

<a id="op-f6269e78664e8e"></a>
### Get total days late

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_days_late`

**Inputs** scorecard.

**Explicit results** (total\_missed\_late\_days + total\_delivered\_late\_days).

**Local steps**

- Set PO from Platform.qb.DocType(“Purchase Order”).
- Set PO\_Item from Platform.qb.DocType(“Purchase Order Item”).
- Set PR from Platform.qb.DocType(“Purchase Receipt”).
- Set PR\_Item from Platform.qb.DocType(“Purchase Receipt Item”).
- Set total\_delivered\_late\_days from (nested operand in the contract.where(nested operand in the contract equals nested operand in the contract).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(nested operand in the contract.docstatus equals 1).run() at 0 at 0 → 0.
- Set total\_missed\_late\_days from (nested operand in the contract.where(nested operand in the contract at nested operand in the contract).run() at 0 at 0 or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in nested operand in the contract(nested operand in the contract).where(nested operand in the contract.schedule\_date at slice nested operand in the contract to nested operand in the contract).run() at 0 at 0 → 0.
- Return (total\_missed\_late\_days + total\_delivered\_late\_days).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L427) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L164)

<a id="op-6f6362a93b9457"></a>
### Get on time shipments

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_on_time_shipments`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase).

**Explicit results** total\_items\_delivered\_on\_time.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set total\_items\_delivered\_on\_time from Platform.db.sql(query text (SELECT, Purchase), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not total\_items\_delivered\_on\_time.
  - Set total\_items\_delivered\_on\_time from 0.
- Return total\_items\_delivered\_on\_time.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L17) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L417) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L154)

<a id="op-43121dbeec2cc3"></a>
### Get late shipments

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_late_shipments`

**Inputs** scorecard.

**Explicit results** (get\_total\_shipments(scorecard) − get\_on\_time\_shipments(scorecard)).

**Local steps**

- Return (get\_total\_shipments(scorecard) − get\_on\_time\_shipments(scorecard)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0354.json#L752) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L416) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L153)

<a id="op-245c0e6d91e756"></a>
### Get total received

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_received`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L428) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L165)

<a id="op-421e65a3cac635"></a>
### Get total received amount

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_received_amount`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L429) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L166)

<a id="op-328d09a60c5074"></a>
### Get total received items

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_received_items`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L29) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L430) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L167)

<a id="op-a93aa1a98a1fc3"></a>
### Get total rejected amount

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_rejected_amount`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L30) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L431) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L168)

<a id="op-cd0830b9d97d2f"></a>
### Get total rejected items

`operation_enterprise_buying_record_definitions_supplier_scorecard_variable_business_behavior_get_total_rejected_items`

**Inputs** scorecard.

**Record and data access** resolve a document from “Supplier” via get\_doc · execute query text (SELECT, Purchase Receipt Item).

**Explicit results** data.

**Local steps**

- Set supplier from Platform.get\_doc(“Supplier”, scorecard.supplier).
- Set data from Platform.db.sql(query text (SELECT, Purchase Receipt Item), mapping(“supplier” → supplier.name, “start\_date” → scorecard.start\_date, “end\_date” → scorecard.end\_date), as\_dict = 0) at 0 at 0.
- If not data.
  - Set data from 0.
- Return data.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0027.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-006.tsv#L432) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-007.tsv#L169)
