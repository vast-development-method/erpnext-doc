# Production · operations 15

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Bom update log

<a id="op-6870ed4ec2cb07"></a>
### BOMUpdate Log.clear old logs

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_clear_old_logs`

**Inputs** days = no value.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Set days from (days or 90).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in days → 90.
- Evaluate clear\_logs\_with\_references(“BOM Update Log”, mapping(“creation” → tuple(“&lt;”, add\_days(now(), negative days)), “update\_type” → “Update Cost”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from now().

**Boundaries to resolve** callee failures, time or generated values, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L3387) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L604) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L307)

<a id="op-7f82c2f911d939"></a>
### BOMUpdate Log.validate

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_validate`

**Inputs** self.

**Local steps**

- If self.update\_type equals “Replace BOM”.
  - Evaluate self.validate\_boms\_are\_specified().
  - Evaluate self.validate\_same\_bom().
  - Evaluate self.validate\_bom\_items().
  - Evaluate self.validate\_not\_a\_semi\_finished\_goods\_operation\_bom().
- Otherwise.
  - Evaluate self.validate\_bom\_cost\_update\_in\_progress().
- Set self.status from “Queued”.

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate boms are specified](operations-015.md#op-c983bfb4b41a90), [validate same bom](operations-015.md#op-c1cf0fa0c90702), [validate bom items](operations-015.md#op-7260cf69e96ed1), [validate not a semi finished goods operation bom](operations-015.md#op-b0305873ad7925), [validate bom cost update in progress](operations-015.md#op-edf5cf31eb55db).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L93) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L607) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L310)

<a id="op-4d3bc0b2c8fe8b"></a>
### BOMUpdate Log.on discard

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_on_discard`

**Inputs** self.

**State and service calls** call db\_set on self.

**Local steps**

- Evaluate self.db\_set(“status”, “Cancelled”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L3707) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L605) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L308)

<a id="op-c983bfb4b41a90"></a>
### BOMUpdate Log.validate boms are specified

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_validate_bills_of_materials_are_specified`

**Inputs** self.

**Explicit failure paths** validation helper with BOMMissingError.

**Local steps**

- If (self.update\_type equals “Replace BOM” and not (self.current\_bom and self.new\_bom)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.update\_type equals “Replace BOM” → not (self.current\_bom and self.new\_bom).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.current\_bom → self.new\_bom.
  - Call the validation error handler Platform.throw(msg = translated “Please mention the Current and New BOM for replacement.”, title = translated “Mandatory”, exc = BOMMissingError).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L3770) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L610) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L313)

<a id="op-c1cf0fa0c90702"></a>
### BOMUpdate Log.validate same bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_validate_same_bill_of_materials`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Current BOM and New BOM can not be same”.

**Local steps**

- If cstr(self.current\_bom) equals cstr(self.new\_bom).
  - Call the validation error handler Platform.throw(translated “Current BOM and New BOM can not be same”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L95) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L611) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L314)

<a id="op-7260cf69e96ed1"></a>
### BOMUpdate Log.validate bom items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_validate_bill_of_materials_items`

**Inputs** self.

**Record and data access** read “BOM” via get\_all.

**Explicit failure paths** validation helper — translated “The selected BOMs are not for the same item” · validation helper — translated “New BOM {0} must be submitted and active”.format(Platform.bold(self.new\_bom)) · validation helper — translated “Current BOM and New BOM must have the same company and currency”.

**Local steps**

- Set boms from mapping of bom.name → bom for bom drawn from Platform.get\_all(“BOM”, filters = mapping(“name” → list(“in”, list(self.current\_bom, self.new\_bom))), fields = list(“name”, “item”, “company”, “currency”, …)).
  - Draw bom from Platform.get\_all(“BOM”, filters = mapping(“name” → list(“in”, list(self.current\_bom, self.new\_bom))), fields = list(“name”, “item”, “company”, “currency”, …)).
- Set current\_bom from (boms.get(self.current\_bom) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in boms.get(self.current\_bom) → Platform.\_dict().
- Set new\_bom from (boms.get(self.new\_bom) or Platform.\_dict()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in boms.get(self.new\_bom) → Platform.\_dict().
- If current\_bom.item differs from new\_bom.item.
  - Call the validation error handler Platform.throw(translated “The selected BOMs are not for the same item”).
- If (new\_bom.docstatus differs from 1 or not new\_bom.is\_active).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_bom.docstatus differs from 1 → not new\_bom.is\_active.
  - Call the validation error handler Platform.throw(translated “New BOM {0} must be submitted and active”.format(Platform.bold(self.new\_bom))).
- If tuple(current\_bom.company, current\_bom.currency) differs from tuple(new\_bom.company, new\_bom.currency).
  - Call the validation error handler Platform.throw(translated “Current BOM and New BOM must have the same company and currency”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L94) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L609) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L312)

<a id="op-b0305873ad7925"></a>
### BOMUpdate Log.validate not a semi finished goods operation bom

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_update_log_bom_update_log_bomupdatelog_validate_not_a_semi_finished_goods_operation_bom`

**Inputs** self.

**Explicit failure paths** validation helper — translated “BOM {0} is the BOM of an operation in {1}, which track semi-finished goods. Amend those BOMs to use the new  …”.format(Platform.bold(self.current\_bom), “, ”.join(generator of Platform.bold(name ….

**Local steps**

- Set bom from Platform.qb.DocType(“BOM”).
- Set bom\_operation from Platform.qb.DocType(“BOM Operation”).
- Set parents from nested operand in the contract(nested operand in the contract).distinct().where((((nested operand in the contract equals nested operand in the contract bitwise and nested operand in the contract equals nes ….
- If parents.
  - Call the validation error handler Platform.throw(translated “BOM {0} is the BOM of an operation in {1}, which track semi-finished goods. Amend those BOMs to use the new  …”.format(Platform.bold(self.current\_bom), “, ”.join(generator of Pla ….
    - Draw name from parents.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L65) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1562) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L802)

<a id="op-edf5cf31eb55db"></a>
### BOMUpdate Log.validate bom cost update in progress

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_validate_bill_of_materials_cost_update_in_progress`

**Inputs** self.

**Record and data access** read “BOM Update Log” via get\_all.

**Explicit failure paths** validation helper — translated “BOM Updation already in progress. Please wait until {0} is complete.”.format(log\_link).

**Local steps**

- Set wip\_log from Platform.get\_all(“BOM Update Log”, fields = list(“name”, “modified”), filters = mapping(“update\_type” → “Update Cost”, “status” → list(“in”, list(“Queued”, “In Progress”))), limit\_page\_length = 1).
- If (wip\_log and date\_diff(today(), wip\_log at 0.modified) &lt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in wip\_log → date\_diff(today(), wip\_log at 0.modified) &lt; 1.
  - Set log\_link from Platform.utils.get\_link\_to\_form(“BOM Update Log”, wip\_log at 0.name).
  - Call the validation error handler Platform.throw(translated “BOM Updation already in progress. Please wait until {0} is complete.”.format(log\_link), title = translated “Note”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L4266) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L608) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L311)

<a id="op-1031cc30c81899"></a>
### BOMUpdate Log.on submit

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_bill_of_materials_update_log_on_submit`

**Inputs** self.

**State and service calls** enqueue.

**Local steps**

- If self.update\_type equals “Replace BOM”.
  - Set boms from mapping(“current\_bom” → self.current\_bom, “new\_bom” → self.new\_bom).
  - Evaluate Platform.enqueue(method = “Enterprise.manufacturing.doctype.bom\_update\_log.bom\_update\_log.run\_replace\_bom\_job”, doc = self, boms = boms, timeout = 40000, …).
- Otherwise.
  - Evaluate Platform.enqueue(method = “Enterprise.manufacturing.doctype.bom\_update\_log.bom\_update\_log.process\_boms\_cost\_level\_wise”, queue = “long”, update\_doc = self, now = Platform.in\_test, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.manufacturing.doctype.bom\_update\_log.bom\_update\_log.run\_replace\_bom\_job”, doc = self, boms = boms, timeout = 40000, …), Platform.enqueue(method = “Enterprise.manufacturing.doctype.bom\_update\_log.bom\_update\_log.process\_boms\_cost\_level\_wise”, queue = “long”, update\_doc = self, now = Platform.in\_test, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L4645) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L606) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L309)

<a id="op-c3983f8b5c81a5"></a>
### Run replace bom job

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_run_replace_bill_of_materials_job`

**Inputs** doc, boms = no value.

**Declared result** no value.

**State and service calls** call db\_set on doc · commit.

**Local steps**

- Attempt the following.
  - Evaluate doc.db\_set(“status”, “In Progress”).
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().
  - Set Platform.db.auto\_commit\_on\_many\_writes from 1.
  - Set boms from Platform.\_dict((boms or mapping())).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in boms → mapping().
  - Evaluate replace\_bom(boms, doc.name).
  - Evaluate doc.db\_set(“status”, “Completed”).
- On failure (Exception).
  - Evaluate handle\_exception(doc).
- On exit, including pending return or failure.
  - Set Platform.db.auto\_commit\_on\_many\_writes from 0.
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L5023) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L616) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L319)

<a id="op-6adba39042cdcb"></a>
### Process boms cost level wise

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_process_bills_of_materials_cost_level_wise`

**Inputs** update\_doc, parent\_boms = no value.

**Declared result** (no value bitwise or tuple).

**Explicit results** no value.

**Local steps**

- Set current\_boms from mapping().
- Set values from mapping().
- Attempt the following.
  - If update\_doc.status equals “Queued”.
    - Set current\_level from 0.
    - Set current\_boms from get\_leaf\_boms().
    - If not current\_boms.
      - Evaluate set\_values\_in\_log(update\_doc.name, mapping(“status” → “Completed”), commit = true).
      - Return no value.
    - Set values from mapping(“processed\_boms” → json.dumps(mapping()), “status” → “In Progress”, “current\_level” → current\_level).
  - Otherwise.
    - If not parent\_boms.
      - Return no value.
    - Set current\_level from (cint(update\_doc.current\_level) + 1).
    - Set current\_boms from parent\_boms.copy().
    - Set values from mapping(“current\_level” → current\_level).
  - Evaluate set\_values\_in\_log(update\_doc.name, values, commit = true).
  - Evaluate queue\_bom\_cost\_jobs(current\_boms, update\_doc, current\_level).
- On failure (Exception).
  - Evaluate handle\_exception(update\_doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L96) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L613) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L316)

<a id="op-65c905c0329141"></a>
### Queue bom cost jobs

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_queue_bill_of_materials_cost_jobs`

**Inputs** current\_boms\_list, update\_doc, current\_level.

**Declared result** no value.

**State and service calls** call db\_insert on batch\_row · enqueue.

**Local steps**

- Set batch\_no from 0.
- While current\_boms\_list.
  - Update batch\_no using + 1.
  - Set batch\_size from 7000.
  - Set boms\_to\_process from current\_boms\_list at slice no value to batch\_size.
  - Set current\_boms\_list from current\_boms\_list at slice batch\_size to no value when len(current\_boms\_list) &gt; batch\_size, otherwise list().
    - Value choice on len(current\_boms\_list) &gt; batch\_size — true gives current\_boms\_list at slice batch\_size to no value, false gives list().
  - Set batch\_row from update\_doc.append(“bom\_batches”, mapping(“level” → current\_level, “batch\_no” → batch\_no, “status” → “Pending”)).
  - Evaluate batch\_row.db\_insert().
  - Evaluate Platform.enqueue(method = “Enterprise.manufacturing.doctype.bom\_update\_log.bom\_updation\_utils.update\_cost\_in\_level”, doc = update\_doc, bom\_list = boms\_to\_process, batch\_name = batch\_row.name, …).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(method = “Enterprise.manufacturing.doctype.bom\_update\_log.bom\_updation\_utils.update\_cost\_in\_level”, doc = update\_doc, bom\_list = boms\_to\_process, batch\_name = batch\_row.name, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L5871) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L614) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L317)

<a id="op-61527732891c88"></a>
### Resume bom cost update jobs

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_resume_bill_of_materials_cost_update_jobs`

**Inputs** no declared parameters.

**Record and data access** read “BOM Update Log” via get\_all · read “BOM Update Batch” via get\_all · resolve a document from “BOM Update Log” via get\_doc.

**State and service calls** request delete on “BOM Update Batch”.

**Explicit results** no value.

**Local steps**

- Set in\_progress\_logs from Platform.db.get\_all(“BOM Update Log”, mapping(“update\_type” → “Update Cost”, “status” → “In Progress”), list(“name”, “processed\_boms”, “current\_level”)).
- If not in\_progress\_logs.
  - Return no value.
- For each log in in\_progress\_logs.
  - Set bom\_batches from Platform.db.get\_all(“BOM Update Batch”, mapping(“parent” → log.name, “level” → log.current\_level), list(“name”, “boms\_updated”, “status”)).
  - Set incomplete\_level from any(generator of row.get(“status”) equals “Pending” for row drawn from bom\_batches).
    - Draw row from bom\_batches.
  - If (not bom\_batches or incomplete\_level).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not bom\_batches → incomplete\_level.
    - Continue with the next iteration or loop test.
  - Set tuple(current\_boms, processed\_boms) from get\_processed\_current\_boms(log, bom\_batches).
  - Set parent\_boms from get\_next\_higher\_level\_boms(child\_boms = current\_boms, processed\_boms = processed\_boms).
  - Set status from “Completed” when not parent\_boms, otherwise “In Progress”.
    - Value choice on not parent\_boms — true gives “Completed”, false gives “In Progress”.
  - Set processed\_boms from json.dumps(list() when not parent\_boms, otherwise processed\_boms).
    - Value choice on not parent\_boms — true gives list(), false gives processed\_boms.
  - Evaluate set\_values\_in\_log(log.name, values = mapping(“processed\_boms” → processed\_boms, “status” → status), commit = true).
  - If status equals “Completed”.
    - Evaluate Platform.db.delete(“BOM Update Batch”, mapping(“parent” → log.name)).
  - If parent\_boms.
    - Evaluate process\_boms\_cost\_level\_wise(update\_doc = Platform.get\_doc(“BOM Update Log”, log.name), parent\_boms = parent\_boms).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0468.json#L6334) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L615) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L318)

<a id="op-1f8fafcbf71029"></a>
### Get processed current boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_business_behavior_get_processed_current_bills_of_materials`

**Inputs** log, bom\_batches.

**Declared result** tuple at tuple(list at str, dict at tuple(str, Any)).

**Explicit results** tuple(current\_boms, processed\_boms).

**Local steps**

- Set processed\_boms from json.loads(log.processed\_boms) when log.processed\_boms, otherwise mapping().
  - Value choice on log.processed\_boms — true gives json.loads(log.processed\_boms), false gives mapping().
- Set current\_boms from list().
- For each row in bom\_batches.
  - Set boms\_updated from json.loads(row.boms\_updated).
  - Evaluate current\_boms.extend(boms\_updated).
  - Set boms\_updated\_dict from mapping of bom → true for bom drawn from boms\_updated.
    - Draw bom from boms\_updated.
  - Evaluate processed\_boms.update(boms\_updated\_dict).
- Return tuple(current\_boms, processed\_boms).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L612) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L315)

<a id="op-38b75d9a8c5f2f"></a>
### Replace bom

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_replace_bill_of_materials`

**Inputs** boms, log\_name.

**Declared result** no value.

**Record and data access** resolve a document from “BOM” via get\_doc.

**State and service calls** call db\_update on bom\_obj.

**Local steps**

- Set current\_bom from boms.get(“current\_bom”).
- Set new\_bom from boms.get(“new\_bom”).
- Evaluate update\_new\_bom\_in\_bom\_items(current\_bom, new\_bom).
- Evaluate Platform.cache().delete\_key(“bom\_children”).
- Set parent\_boms from sort\_children\_first(get\_ancestor\_boms(new\_bom)).
- For each bom in parent\_boms.
  - Set bom\_obj from Platform.get\_doc(“BOM”, bom).
  - Set bom\_obj.\_doc\_before\_save from copy.deepcopy(bom\_obj).
  - Evaluate bom\_obj.update\_exploded\_items().
  - Evaluate bom\_obj.calculate\_cost(save\_updates = true).
  - Evaluate bom\_obj.db\_update().
  - Set bom\_obj.flags.updater\_reference from mapping(“doctype” → “BOM Update Log”, “docname” → log\_name, “label” → translated “via BOM Update Tool”).
  - Evaluate bom\_obj.save\_version().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L91) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L599) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L302)

<a id="op-d37bfb248c0c36"></a>
### Update cost in level

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_update_cost_in_level`

**Inputs** doc, bom\_list, batch\_name.

**Declared result** no value.

**Record and data access** read “BOM Update Log” via get\_value.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - Set status from Platform.db.get\_value(“BOM Update Log”, doc.name, “status”).
  - If status equals “Failed”.
    - Return no value.
  - Evaluate update\_cost\_in\_boms(bom\_list = bom\_list).
  - Set bom\_batch from Platform.qb.DocType(“BOM Update Batch”).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(bom\_batch.status, “Completed”).where(bom\_batch.name equals batch\_name).run().
- On failure (Exception).
  - Evaluate handle\_exception(doc).
- On exit, including pending return or failure.
  - If not Platform.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L829) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L602) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L305)

<a id="op-e6ec4ff757cf8a"></a>
### Get ancestor boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_get_ancestor_bills_of_materials`

**Inputs** new\_bom.

**Declared result** list.

**Explicit results** ancestors.

**Explicit failure paths** validation helper — translated “BOM recursion: {0} cannot be an ancestor of itself”.format(new\_bom).

**Local steps**

- Set ancestors from list().
- Set seen from set().
- Set children from list(new\_bom).
- While children.
  - Set links from get\_bom\_links\_query().as\_(“bom\_links”).
  - Set parents from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.isin(children)).distinct().run(pluck = true).
  - Set children from list of parent for parent drawn from parents where parent does not belong to seen.
    - Draw parent from parents, keep a combination only if (parent does not belong to seen).
  - Evaluate seen.update(children).
  - Evaluate ancestors.extend(children).
- If new\_bom belongs to seen.
  - Call the validation error handler Platform.throw(translated “BOM recursion: {0} cannot be an ancestor of itself”.format(new\_bom)).
- Return ancestors.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L89) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L593) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L297)

<a id="op-af8223caa64236"></a>
### Get bom links query

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_update_log_bom_updation_utils_get_bom_links_query`

**Inputs** no declared parameters.

**Explicit results** (nested operand in the contract.from\_(bom\_item).select(bom\_item.parent, bom\_item.bom\_no).where((bom\_item.docstatus &lt; 2 bitwise and bom\_item.parenttype equals “BOM”)) + nested operand in the contract.from\_( ….

**Local steps**

- Set bom\_item from Platform.qb.DocType(“BOM Item”).
- Set bom\_operation from Platform.qb.DocType(“BOM Operation”).
- Return (nested operand in the contract.from\_(bom\_item).select(bom\_item.parent, bom\_item.bom\_no).where((bom\_item.docstatus &lt; 2 bitwise and bom\_item.parenttype equals “BOM”)) + nested operand in the contract.from\_( ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L66) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1563) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L803)

<a id="op-ca01852d897bdd"></a>
### Update new bom in bom items

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_update_new_bill_of_materials_in_bill_of_materials_items`

**Inputs** current\_bom, new\_bom.

**Declared result** no value.

**Local steps**

- For each doctype in tuple(“BOM Item”, “BOM Operation”).
  - Set table from Platform.qb.DocType(doctype).
  - Evaluate nested operand in the contract(nested operand in the contract).set(table.bom\_no, new\_bom).where(((nested operand in the contract.bom\_no equals current\_bom bitwise and nested operand in the contract.docstat ….run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L92) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L603) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L306)

<a id="op-d98d2b7401a197"></a>
### Sort children first

`operation_enterprise_binding_enterprise_manufacturing_doctype_bom_update_log_bom_updation_utils_sort_children_first`

**Inputs** boms.

**Declared result** list at str.

**Explicit results** boms · ordered.

**Local steps**

- <a id="op-d98d2b7401a197-guard-2"></a>If len(boms) &lt; 2.
  - Return boms.
- Set bom\_links from get\_bom\_links\_query().as\_(“bom\_links”).
- Set links from nested operand in the contract(nested operand in the contract).select(bom\_links.parent, bom\_links.bom\_no).where((nested operand in the contract.parent.isin(boms) bitwise and nested operand in the contract. ….
- Set pending\_children from defaultdict(set).
- Set parents\_of from defaultdict(set).
- For each link in links.
  - Evaluate pending\_children at link.parent.add(link.bom\_no).
  - Evaluate parents\_of at link.bom\_no.add(link.parent).
- Set ordered from list().
- Set ready from list of bom for bom drawn from boms where not pending\_children at bom.
  - Draw bom from boms, keep a combination only if (not pending\_children at bom).
- While ready.
  - Set bom from ready.pop().
  - Evaluate ordered.append(bom).
  - For each parent in parents\_of at bom.
    - Evaluate pending\_children at parent.discard(bom).
    - If not pending\_children at parent.
      - Evaluate ready.append(parent).
- Return ordered.

**Derived branch illustrations**

- At the comparison len(boms) &lt; 2, length of boms = 1 selects the branch that returns boms. With length of boms = 2, this branch is skipped and control continues with the subsequent steps. [Local guard](#op-d98d2b7401a197-guard-2)

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0016.json#L67) · [Binding](../../../current-decisions/enterprise/bindings-004.tsv#L1564) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-005.tsv#L804)

<a id="op-689b283995967c"></a>
### Update cost in boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_update_cost_in_bills_of_materials`

**Inputs** bom\_list.

**Declared result** no value.

**Record and data access** resolve a document from “BOM” via get\_doc.

**State and service calls** call db\_update on bom\_doc · commit.

**Local steps**

- For each tuple(index, bom) in enumerate(bom\_list).
  - Set bom\_doc from Platform.get\_doc(“BOM”, bom, for\_update = true).
  - Evaluate bom\_doc.calculate\_cost(save\_updates = true, update\_hour\_rate = true).
  - Evaluate bom\_doc.db\_update().
  - If ((index modulo or format 50) equals 0 and not Platform.in\_test).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in (index modulo or format 50) equals 0 → not Platform.in\_test.
    - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L2447) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L601) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L304)

<a id="op-f95fae1ce93a67"></a>
### Get next higher level boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_get_next_higher_level_bills_of_materials`

**Inputs** child\_boms, processed\_boms.

**Declared result** list at str.

**Explicit results** list(resolved\_dependants).

**Local steps**

- Bind local operation \_all\_children\_are\_processed for subsequent calls.
- Set tuple(dependants\_map, dependency\_map) from \_generate\_dependence\_map().
- Set dependants from list().
- For each bom in child\_boms.
  - Set parents from (dependants\_map.get(bom) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in dependants\_map.get(bom) → list().
  - Evaluate dependants.extend(parents).
- Set dependants from set(dependants).
- Set resolved\_dependants from set().
- For each parent\_bom in dependants.
  - If \_all\_children\_are\_processed(parent\_bom).
    - Evaluate resolved\_dependants.add(parent\_bom).
- Return list(resolved\_dependants).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L2702) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L596) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L299)

<a id="op-e012a10a46646b"></a>
### Get next higher level boms.all children are processed

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_get_next_higher_level_bills_of_materials_all_children_are_processed`

**Inputs** parent\_bom.

**Explicit results** all(generator of processed\_boms.get(bom) for bom drawn from child\_boms).

**Local steps**

- Set child\_boms from dependency\_map.get(parent\_bom).
- Return all(generator of processed\_boms.get(bom) for bom drawn from child\_boms).
  - Draw bom from child\_boms.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0469.json#L3133) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L597) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L300)

<a id="op-4924fdcb8a1c1f"></a>
### Get leaf boms

`operation_enterprise_manufacturing_record_definitions_bill_of_materials_update_log_bill_of_materials_updation_utils_business_behavior_get_leaf_bills_of_materials`

**Inputs** no declared parameters.

**Declared result** list at str.

**Explicit results** nested operand in the contract(nested operand in the contract).select(bom.name).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contract.is\_active equals 1) bitw ….

**Local steps**

- Set bom from Platform.qb.DocType(“BOM”).
- Set bom\_item from Platform.qb.DocType(“BOM Item”).
- Set child\_bom from Platform.qb.DocType(“BOM”).as\_(“child\_bom”).
- Set active\_children from nested operand in the contract(nested operand in the contract).on(nested operand in the contract.name equals nested operand in the contract.bom\_no).select(bom\_item.name).where((((bom\_item.parent equals bom ….
- Return nested operand in the contract(nested operand in the contract).select(bom.name).where(((nested operand in the contract.docstatus equals 1 bitwise and nested operand in the contract.is\_active equals 1) bitw ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0031.json#L90) · [Binding](../../../current-decisions/enterprise/bindings-007.tsv#L595) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-008.tsv#L298)
