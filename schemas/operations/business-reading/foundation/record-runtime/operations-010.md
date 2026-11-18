# Record lifecycle and persistence · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-7b8f4b1edc420d"></a>
### Data Import.start import

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_start_import`

**Inputs** self.

**Explicit results** true · false.

**Explicit failure paths** validation helper — translated “Scheduler is inactive. Cannot import data.”.

**Local steps**

- Bind dependencies is\_scheduler\_inactive.
- Set run\_now from (Platform.in\_test or Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.in\_test → Platform.conf.developer\_mode.
- If (is\_scheduler\_inactive() and not run\_now).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_scheduler\_inactive() → not run\_now.
  - Call the validation error handler Platform.throw(translated “Scheduler is inactive. Cannot import data.”, title = translated “Scheduler Inactive”).
- Set job\_id from formatted text data\_import\|\|{self.name}.
- If not is\_job\_enqueued(job\_id).
  - Evaluate enqueue(start\_import, queue = “default”, timeout = 10000, event = “data\_import”, job\_id = job\_id, …).
  - Return true.
- Return false.

**Values supplied outside this operation** service or queued work from enqueue(start\_import, queue = “default”, timeout = 10000, event = “data\_import”, job\_id = job\_id, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L6464) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1149)

<a id="op-5a3fb85591256e"></a>
### Data Import.export errored rows

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_export_errored_rows`

**Inputs** self.

**Explicit results** self.get\_importer().export\_errored\_rows().

**Local steps**

- Return self.get\_importer().export\_errored\_rows().

**Methods declared on this owner** [get importer](operations-010.md#op-b85e1beed3a806).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L6809) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1147) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1142)

<a id="op-5fa52b4b331496"></a>
### Data Import.export skipped rows

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_export_skipped_rows`

**Inputs** self.

**Explicit results** self.get\_importer().export\_skipped\_rows().

**Local steps**

- Return self.get\_importer().export\_skipped\_rows().

**Methods declared on this owner** [get importer](operations-010.md#op-b85e1beed3a806).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L6872) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1148) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1143)

<a id="op-a214640bd14f6c"></a>
### Data Import.download import log

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_download_import_log`

**Inputs** self.

**Explicit results** self.get\_importer().export\_import\_log().

**Local steps**

- Return self.get\_importer().export\_import\_log().

**Methods declared on this owner** [get importer](operations-010.md#op-b85e1beed3a806).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L6935) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1141)

<a id="op-b85e1beed3a806"></a>
### Data Import.get importer

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_get_importer`

**Inputs** self.

**Explicit results** Importer(self.reference\_doctype, data\_import = self, use\_sniffer = self.use\_csv\_sniffer).

**Local steps**

- Return Importer(self.reference\_doctype, data\_import = self, use\_sniffer = self.use\_csv\_sniffer).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L6998) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1149) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1144)

<a id="op-2a94be5a298e3b"></a>
### Data Import.on trash

`operation_foundation_core_record_definitions_data_import_business_behavior_data_import_on_trash`

**Inputs** self.

**State and service calls** request delete on “Data Import Log”.

**Local steps**

- Evaluate Platform.db.delete(“Data Import Log”, mapping(“data\_import” → self.name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0049.json#L7075) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1146)

<a id="op-139db096a6b2e2"></a>
### Get preview from template

`operation_foundation_core_record_definitions_data_import_business_behavior_get_preview_from_template`

**Inputs** data\_import, import\_file = no value, google\_sheets\_url = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc.

**Explicit results** di.get\_preview\_from\_template(import\_file, google\_sheets\_url).

**Local steps**

- Set di from Platform.get\_doc(“Data Import”, data\_import).
- Evaluate di.check\_permission(“read”).
- Return di.get\_preview\_from\_template(import\_file, google\_sheets\_url).

**Values supplied outside this operation** effective access from di.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1171) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1165)

<a id="op-ebe43dec3c8154"></a>
### Form start import

`operation_foundation_core_record_definitions_data_import_business_behavior_form_start_import`

**Inputs** data\_import.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc.

**Explicit results** di.start\_import().

**Local steps**

- Set di from Platform.get\_doc(“Data Import”, data\_import).
- Evaluate di.check\_permission(“write”).
- Return di.start\_import().

**Values supplied outside this operation** effective access from di.check\_permission(“write”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L200) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1161)

<a id="op-a81ad437fe6b09"></a>
### Stop data import

`operation_foundation_core_record_definitions_data_import_business_behavior_stop_data_import`

**Inputs** doc\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc.

**State and service calls** request set\_value on “Data Import” · publish realtime with “data\_import\_refresh”.

**Explicit results** mapping(“status” → “not\_running”, “message” → translated “Job was not running; status updated.”) · mapping(“status” → “success”, “message” → translated “Job stopped successfully”).

**Local steps**

- Set data\_import from Platform.get\_doc(“Data Import”, doc\_name).
- Evaluate data\_import.check\_permission(“write”).
- Set rq\_job\_id from formatted text {Platform.local.site}\|\|data\_import\|\|{doc\_name}.
- Set job\_id from rq\_job\_id.replace(“:”, “\|”).
- Set job\_was\_running from true.
- Attempt the following.
  - Evaluate send\_stop\_job\_command(connection = get\_redis\_conn(), job\_id = job\_id).
- On failure (tuple(InvalidJobOperation, NoSuchJobError)).
  - Set job\_was\_running from false.
- Evaluate Platform.db.set\_value(“Data Import”, mapping(“name” → data\_import.name, “status” → “In Progress”), mapping(“status” → “Error”)).
- Evaluate Platform.publish\_realtime(“data\_import\_refresh”, mapping(“data\_import” → data\_import.name), doctype = “Data Import”, docname = data\_import.name, after\_commit = true).
- If not job\_was\_running.
  - Return mapping(“status” → “not\_running”, “message” → translated “Job was not running; status updated.”).
- Return mapping(“status” → “success”, “message” → translated “Job stopped successfully”).

**Values supplied outside this operation** effective access from data\_import.check\_permission(“write”) · service or queued work from Platform.publish\_realtime(“data\_import\_refresh”, mapping(“data\_import” → data\_import.name), doctype = “Data Import”, docname = data\_import.name, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L13) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1175) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1169)

<a id="op-2bc77b43e33748"></a>
### Start import

`operation_foundation_core_record_definitions_data_import_business_behavior_start_import`

**Inputs** data\_import.

**Record and data access** resolve a document from “Data Import” via get\_doc.

**State and service calls** rollback · call db\_set on data\_import · publish realtime with “data\_import\_refresh” · publish realtime with “list\_update”.

**Local steps**

- Set data\_import from Platform.get\_doc(“Data Import”, data\_import).
- Evaluate data\_import.set\_delimiters\_flag().
- Set i from no value.
- Attempt the following.
  - Set i from data\_import.get\_importer().
  - Evaluate i.import\_data().
- On failure (JobTimeoutException).
  - Evaluate Platform.db.rollback().
  - Evaluate data\_import.db\_set(“status”, “Timed Out”).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate data\_import.db\_set(“status”, “Error”).
  - Evaluate data\_import.log\_error(“Data import failed”).
  - Attempt the following.
    - Evaluate Platform.logger(“data\_import”).error(formatted text Data import {data\_import.name} failed, exc\_info = true).
  - On failure (Exception).
    - Take no action here.
- On exit, including pending return or failure.
  - Set Platform.flags.in\_import from false.
- If not (i and i.blocked\_by\_warnings).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in i → i.blocked\_by\_warnings.
  - Evaluate Platform.publish\_realtime(“data\_import\_refresh”, mapping(“data\_import” → data\_import.name), doctype = “Data Import”, docname = data\_import.name, after\_commit = true).
  - If (data\_import.reference\_doctype and data\_import.status belongs to tuple(“Success”, “Partial Success”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in data\_import.reference\_doctype → data\_import.status belongs to tuple(“Success”, “Partial Success”).
    - Set data from mapping(“doctype” → data\_import.reference\_doctype, “name” → no value, “user” → Platform.session.user).
    - Evaluate Platform.publish\_realtime(“list\_update”, data, after\_commit = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“data\_import\_refresh”, mapping(“data\_import” → data\_import.name), doctype = “Data Import”, docname = data\_import.name, after\_commit = true), Platform.publish\_realtime(“list\_update”, data, after\_commit = true).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L12) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1174) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1168)

<a id="op-689c4bccd70f1a"></a>
### Get import fields

`operation_foundation_binding_foundation_core_doctype_data_import_data_import_get_import_fields`

**Inputs** doctype.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · provider.get\_import\_fields() when provider, otherwise no value.

**Local steps**

- If not doctype.
  - Return no value.
- Evaluate Platform.has\_permission(doctype, “read”, throw = true).
- Bind dependencies get\_import\_provider.
- Set provider from get\_import\_provider(doctype).
- Return provider.get\_import\_fields() when provider, otherwise no value.
  - Value choice on provider — true gives provider.get\_import\_fields(), false gives no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L137) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L619) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L595)

<a id="op-6f9a77979ba968"></a>
### Download template

`operation_foundation_core_record_definitions_data_import_business_behavior_download_template`

**Inputs** doctype, export\_fields = no value, export\_records = no value, export\_filters = no value, file\_type = “CSV”.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate Platform.has\_permission(doctype, “read”, throw = true).
- Set export\_fields from Platform.parse\_json(export\_fields).
- Set export\_filters from Platform.parse\_json(export\_filters).
- Set export\_data from export\_records differs from “blank\_template”.
- Set list\_settings from Platform.parse\_json(get\_user\_settings(doctype)).get(“List”, mapping()).
- Set sort\_by from list\_settings.get(“sort\_by”).
- Set sort\_order from list\_settings.get(“sort\_order”).
- If (sort\_by and not Platform.get\_meta(doctype).get\_field(sort\_by)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sort\_by → not Platform.get\_meta(doctype).get\_field(sort\_by).
  - Set sort\_by from no value.
- If (sort\_order and sort\_order.upper() does not belong to tuple(“ASC”, “DESC”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sort\_order → sort\_order.upper() does not belong to tuple(“ASC”, “DESC”).
  - Set sort\_order from no value.
- Set order\_by from formatted text {sort\_by} {sort\_order} when (sort\_by and sort\_order), otherwise no value.
  - Value choice on (sort\_by and sort\_order) — true gives formatted text {sort\_by} {sort\_order}, false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in sort\_by → sort\_order.
- Set e from Exporter(doctype, export\_fields = export\_fields, export\_data = export\_data, export\_filters = export\_filters, file\_type = file\_type, …).
  - Value choice on export\_records equals “5\_records” — true gives 5, false gives no value.
- Evaluate e.build\_response().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(doctype, “read”, throw = true).

**Boundaries to resolve** late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L1164) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1157)

<a id="op-7f64a8affdfd6c"></a>
### Get export count

`operation_foundation_binding_foundation_core_doctype_data_import_data_import_get_export_count`

**Inputs** doctype, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** int.

**Explicit results** get\_count(doctype, get\_export\_filters(doctype, filters)).

**Local steps**

- Return get\_count(doctype, get\_export\_filters(doctype, filters)).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L136) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L618) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L594)

<a id="op-42bf5d83bdf805"></a>
### Download errored template

`operation_foundation_core_record_definitions_data_import_business_behavior_download_errored_template`

**Inputs** data\_import\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc.

**Local steps**

- Set data\_import from Platform.get\_doc(“Data Import”, data\_import\_name).
- Evaluate data\_import.check\_permission(“read”).
- Evaluate data\_import.export\_errored\_rows().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from data\_import.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L1957) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1154)

<a id="op-93af4c6a767885"></a>
### Download skipped rows

`operation_foundation_core_record_definitions_data_import_business_behavior_download_skipped_rows`

**Inputs** data\_import\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc.

**Local steps**

- Set data\_import from Platform.get\_doc(“Data Import”, data\_import\_name).
- Evaluate data\_import.check\_permission(“read”).
- Evaluate data\_import.export\_skipped\_rows().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from data\_import.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L2096) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1156)

<a id="op-6fdec6092267b5"></a>
### Download import log

`operation_foundation_core_record_definitions_data_import_business_behavior_download_import_log`

**Inputs** data\_import\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc.

**Local steps**

- Set data\_import from Platform.get\_doc(“Data Import”, data\_import\_name).
- Evaluate data\_import.check\_permission(“read”).
- Evaluate data\_import.download\_import\_log().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from data\_import.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L2235) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1155)

<a id="op-b11208238354ea"></a>
### Get import status

`operation_foundation_core_record_definitions_data_import_business_behavior_get_import_status`

**Inputs** data\_import\_name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc · read “Data Import Log” via get\_all.

**Explicit results** import\_status.

**Local steps**

- Bind dependencies ACTION\_INSERT, ACTION\_UPDATE.
- Set data\_import from Platform.get\_doc(“Data Import”, data\_import\_name).
- Evaluate data\_import.check\_permission(“read”).
- Set import\_status from mapping(“status” → data\_import.status, “total\_records” → data\_import.payload\_count).
- Set is\_upsert from data\_import.import\_type equals UPSERT.
- Set group\_by from “success, import\_action” when is\_upsert, otherwise “success”.
  - Value choice on is\_upsert — true gives “success, import\_action”, false gives “success”.
- Set log\_fields from list(mapping(“COUNT” → “\*”, “as” → “count”), “success”).
- If is\_upsert.
  - Evaluate log\_fields.append(“import\_action”).
- For each log in Platform.get\_all(“Data Import Log”, fields = log\_fields, filters = mapping(“data\_import” → data\_import\_name), group\_by = group\_by).
  - Set count from log.get(“count”).
  - If log.get(“success”).
    - Set import\_status at “success” from (import\_status.get(“success”, 0) + count).
    - If is\_upsert.
      - If log.get(“import\_action”) equals ACTION\_INSERT.
        - Set import\_status at “inserted” from count.
      - Otherwise.
        - If log.get(“import\_action”) equals ACTION\_UPDATE.
          - Set import\_status at “updated” from count.
  - Otherwise.
    - Set import\_status at “failed” from count.
- If is\_upsert.
  - Evaluate import\_status.setdefault(“inserted”, 0).
  - Evaluate import\_status.setdefault(“updated”, 0).
- Set logged\_total from (import\_status.get(“success”, 0) + import\_status.get(“failed”, 0)).
- Set import\_status at “processed\_records” from logged\_total.
- If (logged\_total and not import\_status.get(“total\_records”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in logged\_total → not import\_status.get(“total\_records”).
  - Set import\_status at “total\_records” from logged\_total.
- Return import\_status.

**Values supplied outside this operation** effective access from data\_import.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L10) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1170) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1164)

<a id="op-6b9c0e566a8efa"></a>
### Get import log count

`operation_foundation_core_record_definitions_data_import_business_behavior_get_import_log_count`

**Inputs** data\_import.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“GET”)), Platform.read\_only().

**Record and data access** resolve a document from “Data Import” via get\_doc · read “Data Import Log” via count.

**Explicit results** Platform.db.count(“Data Import Log”, mapping(“data\_import” → data\_import)).

**Local steps**

- Set doc from Platform.get\_doc(“Data Import”, data\_import).
- Evaluate doc.check\_permission(“read”).
- Return Platform.db.count(“Data Import Log”, mapping(“data\_import” → data\_import)).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L3244) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1162)

<a id="op-5f05d2d4cafef9"></a>
### Get import logs

`operation_foundation_core_record_definitions_data_import_business_behavior_get_import_logs`

**Inputs** data\_import, status = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Data Import” via get\_doc · read “Data Import Log” via get\_all.

**Explicit results** Platform.get\_all(“Data Import Log”, fields = list(“success”, “docname”, “messages”, “exception”, …), filters = filters, limit = 1000, order\_by = “log\_index”).

**Local steps**

- Set doc from Platform.get\_doc(“Data Import”, data\_import).
- Evaluate doc.check\_permission(“read”).
- Set filters from mapping(“data\_import” → data\_import).
- Set status\_key from (status or “all”).lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in status → “all”.
- If status\_key equals “success”.
  - Set filters at “success” from 1.
- Otherwise.
  - If status\_key equals “failed”.
    - Set filters at “success” from 0.
- Return Platform.get\_all(“Data Import Log”, fields = list(“success”, “docname”, “messages”, “exception”, …), filters = filters, limit = 1000, order\_by = “log\_index”).

**Values supplied outside this operation** effective access from doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L9) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1163)

<a id="op-bb6c9d264502e5"></a>
### Import file

`operation_foundation_core_record_definitions_data_import_business_behavior_import_file`

**Inputs** doctype, file\_path, import\_type, submit\_after\_import = false, console = false.

**State and service calls** request new\_doc for “Data Import”.

**Local steps**

- Set data\_import from Platform.new\_doc(“Data Import”).
- Set data\_import.reference\_doctype from doctype.
- Set data\_import.import\_file from file\_path.
- Set data\_import.submit\_after\_import from submit\_after\_import.
- Set import\_type\_lower from import\_type.lower().
- If import\_type\_lower equals “insert”.
  - Set data\_import.import\_type from “Insert New Records”.
- Otherwise.
  - If import\_type\_lower equals “upsert”.
    - Set data\_import.import\_type from UPSERT.
  - Otherwise.
    - Set data\_import.import\_type from “Update Existing Records”.
- Evaluate Platform.set\_user\_lang(Platform.session.user).
- Set i from Importer(doctype = doctype, file\_path = file\_path, data\_import = data\_import, console = console).
- Evaluate data\_import.set\_payload\_count(i).
- Evaluate i.import\_data().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L11) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1172) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1166)

<a id="op-ae4307cf5727a4"></a>
### Import doc

`operation_foundation_core_record_definitions_data_import_business_behavior_import_record`

**Inputs** path, pre\_process = no value, sort = false.

**State and service calls** commit.

**Explicit failure paths** NotImplementedError(“Only .json files can be imported”).

**Local steps**

- If os.path.isdir(path).
  - Set files from list of os.path.join(path, f) for f drawn from os.listdir(path).
    - Draw f from os.listdir(path).
  - If sort.
    - Evaluate files.sort().
- Otherwise.
  - Set files from list(path).
- For each f in files.
  - If f.endswith(“.json”).
    - Set Platform.flags.mute\_emails from true.
    - Evaluate import\_file\_by\_path(f, data\_import = true, force = true, pre\_process = pre\_process, reset\_permissions = true).
    - Set Platform.flags.mute\_emails from false.
    - Evaluate Platform.db.commit().
  - Otherwise.
    - Raise NotImplementedError(“Only .json files can be imported”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L4087) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1173) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1167)

<a id="op-0fe7e87afc12ce"></a>
### Export json

`operation_foundation_core_record_definitions_data_import_business_behavior_export_structured_data`

**Inputs** doctype, path, filters = no value, or\_filters = no value, name = no value, order\_by = “creation asc”.

**Record and data access** resolve a document from doctype via get\_doc · read “DocType” via get\_value · read doctype via get\_all.

**Local steps**

- Bind local operation post\_process for subsequent calls.
- Set out from list().
- If name.
  - Evaluate out.append(Platform.get\_doc(doctype, name).as\_dict()).
- Otherwise.
  - If Platform.db.get\_value(“DocType”, doctype, “issingle”).
    - Evaluate out.append(Platform.get\_doc(doctype).as\_dict()).
  - Otherwise.
    - For each doc in Platform.get\_all(doctype, fields = list(“name”), filters = filters, or\_filters = or\_filters, limit\_page\_length = 0, …).
      - Evaluate out.append(Platform.get\_doc(doctype, doc.name).as\_dict()).
- Evaluate post\_process(out).
- Set dirname from os.path.dirname(path).
- If not os.path.exists(dirname).
  - Set path from os.path.join(“..”, path).
- Within open(path, “w”) bound as outfile.
  - Evaluate outfile.write(Platform.as\_json(out, ensure\_ascii = false)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L4480) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1159)

<a id="op-c413bfeba3d229"></a>
### Export json.post process

`operation_foundation_core_record_definitions_data_import_business_behavior_export_structured_data_post_process`

**Inputs** out.

**Local steps**

- Set del\_keys from tuple(“modified\_by”, “creation”, “owner”, “idx”, …).
- For each doc in out.
  - For each key in del\_keys.
    - If key belongs to doc.
      - Remove doc at key.
  - For each v in doc.values().
    - If isinstance(v, list).
      - For each child in v.
        - For each key in tuple(expanded del\_keys, “docstatus”, “doctype”, “modified”, …).
          - If key belongs to child.
            - Remove child at key.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L5435) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1160)

<a id="op-d6554c62e956aa"></a>
### Export csv

`operation_foundation_core_record_definitions_data_import_business_behavior_export_comma_separated_values`

**Inputs** doctype, path.

**Local steps**

- Bind dependencies export\_data.
- Within open(path, “wb”) bound as csvfile.
  - Evaluate export\_data(doctype = doctype, all\_doctypes = true, template = true, with\_data = true).
  - Evaluate csvfile.write(Platform.response.result.encode(“utf-8”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0050.json#L5793) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1158)
