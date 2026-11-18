# Record lifecycle and persistence · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Data import

[Record definition](../../../../data/record-types/data_import.json)

<a id="op-9b232c7b45d486"></a>
### Get fixed csv delimiter

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_get_fixed_comma_separated_values_delimiter`

**Inputs** custom\_delimiters, delimiter\_options.

**Declared result** (str bitwise or no value).

**Explicit results** no value · options when len(options) equals 1, otherwise no value.

**Local steps**

- If (not cint(custom\_delimiters) or not delimiter\_options).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not cint(custom\_delimiters) → not delimiter\_options.
  - Return no value.
- Set options from delimiter\_options.strip().
- Return options when len(options) equals 1, otherwise no value.
  - Value choice on len(options) equals 1 — true gives options, false gives no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L3330) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1203)

<a id="op-2eed8a9e7a8fd0"></a>
### Parse number

`operation_foundation_binding_foundation_core_doctype_data_import_importer_parse_number`

**Inputs** value, number\_format.

**Declared result** (float bitwise or no value).

**Explicit results** plain · no value · formatted.

**Local steps**

- Set value from value.strip().
- Attempt the following.
  - Set plain from float(value).
- On failure (ValueError).
  - Set plain from no value.
- Set group from re.escape(number\_format.thousands\_separator).
- Set decimal from re.escape(number\_format.decimal\_separator).
- Set integer from formatted text \\d+\|&#91;1-9&#93;\\d{0,2}(?:{group}\\d{2,3})\*{group}\\d{3} when group, otherwise “\\d+”.
  - Value choice on group — true gives formatted text \\d+\|&#91;1-9&#93;\\d{0,2}(?:{group}\\d{2,3})\*{group}\\d{3}, false gives “\\d+”.
- Set fraction from formatted text (?:{decimal}\\d+)? when decimal, otherwise empty text.
  - Value choice on decimal — true gives formatted text (?:{decimal}\\d+)?, false gives empty text.
- If not re.fullmatch(formatted text &#91;+-&#93;?(?:{integer}){fraction}, value).
  - Return plain.
- If group.
  - Set value from value.replace(number\_format.thousands\_separator, empty text).
- If decimal.
  - Set value from value.replace(number\_format.decimal\_separator, “.”).
- Set formatted from float(value).
- If (plain is distinct from no value and plain differs from formatted).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in plain is distinct from no value → plain differs from formatted.
  - Return no value.
- Return formatted.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L161) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L643) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L619)

<a id="op-a977ea364e5898"></a>
### Importer.initialize

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_initialize`

**Inputs** self, doctype, data\_import = no value, file\_path = no value, import\_type = no value, console = false, use\_sniffer = false.

**Record and data access** resolve a document from “Data Import” via get\_doc.

**Local steps**

- Set self.doctype from doctype.
- Set self.console from console.
- Set self.use\_sniffer from use\_sniffer.
- Set self.blocked\_by\_warnings from false.
- Set self.data\_import from data\_import.
- If not self.data\_import.
  - Set self.data\_import from Platform.get\_doc(doctype = “Data Import”).
  - If import\_type.
    - Set self.data\_import.import\_type from import\_type.
- Set self.template\_options from Platform.parse\_json((self.data\_import.template\_options or “{}”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.data\_import.template\_options → “{}”.
- Set self.import\_type from self.data\_import.import\_type.
- Set self.import\_file from ImportFile(doctype, (file\_path or data\_import.google\_sheets\_url or data\_import.import\_file), self.template\_options, self.import\_type, data\_import\_name = self.data\_import.name, reference\_doctype = doctype,  ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in file\_path → data\_import.google\_sheets\_url → data\_import.import\_file.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L44) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1247) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1240)

<a id="op-cc11daa0118d41"></a>
### Importer.get data for import preview

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_get_data_for_import_preview`

**Inputs** self.

**Record and data access** read “Data Import Log” via get\_all.

**Explicit results** out.

**Local steps**

- Set out from self.import\_file.get\_data\_for\_import\_preview().
- Set out.import\_log from Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”, limit = 10).
- Return out.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L3970) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1244) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1237)

<a id="op-234e048b05e2ae"></a>
### Importer.before import

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_before_import`

**Inputs** self.

**State and service calls** call db\_set on self.data\_import.

**Local steps**

- Evaluate Platform.cache.hdel(“lang”, Platform.session.user).
- Evaluate Platform.set\_user\_lang(Platform.session.user).
- Set Platform.flags.in\_import from true.
- Set Platform.flags.mute\_emails from self.data\_import.mute\_emails.
- Evaluate self.data\_import.db\_set(“template\_warnings”, empty text).
- Bind dependencies get\_import\_provider.
- Set self.provider from get\_import\_provider(self.doctype).
- Set self.\_inserted\_name\_map from mapping().
- Set meta from Platform.get\_meta(self.doctype).
- Set self.\_tree\_parent\_field from meta.nsm\_parent\_field when meta.is\_nested\_set(), otherwise no value.
  - Value choice on meta.is\_nested\_set() — true gives meta.nsm\_parent\_field, false gives no value.
- Set header from getattr(self.import\_file, “header”, no value).
- Set self.\_tree\_alias\_field from getattr(header, “tree\_alias\_field”, no value).
- Set self.\_id\_fieldname from (getattr(header, “id\_fieldname”, no value) or get\_id\_field(self.doctype).fieldname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(header, “id\_fieldname”, no value) → get\_id\_field(self.doctype).fieldname.
- Set self.\_uses\_tree\_aliases from bool(self.\_tree\_alias\_field).
- Evaluate self.\_prime\_inserted\_name\_map\_from\_db().

If control reaches the end, it returns no value.

**Methods declared on this owner** [prime inserted name map from db](operations-012.md#op-24bbdb3a6e6d40).

**Values supplied outside this operation** selected callable from getattr(self.import\_file, “header”, no value), getattr(header, “tree\_alias\_field”, no value) and 1 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L41) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1240) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1233)

<a id="op-24bbdb3a6e6d40"></a>
### Importer.prime inserted name map from db

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_prime_inserted_name_map_from_database`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If not self.\_tree\_parent\_field.
  - Return no value.
- Set parent\_column from next(generator of col for col drawn from self.import\_file.header.columns where (col.df and col.df.fieldname equals self.\_tree\_parent\_field and not col.skip\_import), no value).
  - Draw col from self.import\_file.header.columns, keep a combination only if ((col.df and col.df.fieldname equals self.\_tree\_parent\_field and not col.skip\_import)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in col.df → col.df.fieldname equals self.\_tree\_parent\_field → not col.skip\_import.
- If not parent\_column.
  - Return no value.
- Set parent\_values from set of cstr(v).strip() for v drawn from parent\_column.column\_values where v does not belong to INVALID\_VALUES.
  - Draw v from parent\_column.column\_values, keep a combination only if (v does not belong to INVALID\_VALUES).
- Set header from self.import\_file.header.
- Set in\_file\_refs from ((header.import\_ids or set()) bitwise or (header.import\_aliases or set())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in header.import\_ids → set().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in header.import\_aliases → set().
- If self.import\_type equals UPDATE.
  - Set refs\_to\_fetch from parent\_values.
- Otherwise.
  - Set refs\_to\_fetch from (parent\_values − in\_file\_refs).
- If not refs\_to\_fetch.
  - Return no value.
- Evaluate self.\_inserted\_name\_map.update(\_build\_db\_tree\_parent\_name\_map(self.doctype, refs\_to\_fetch, self.\_tree\_alias\_field)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0051.json#L4645) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1249) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1242)

<a id="op-40b69fc4bb4ccd"></a>
### Importer.import data

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_import_data`

**Inputs** self.

**Record and data access** read “Data Import” via exists · read “Data Import Log” via get\_all.

**State and service calls** call db\_set on self.data\_import · publish realtime with “data\_import\_blocked” · request delete on “Data Import Log” · commit · rollback.

**Explicit results** no value · import\_log.

**Local steps**

- Evaluate self.before\_import().
- Set payloads from self.import\_file.get\_payloads\_for\_import().
- Set self.data\_import.payload\_count from len(payloads).
- If (self.data\_import.name and self.data\_import.meta.has\_field(“payload\_count”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.data\_import.name → self.data\_import.meta.has\_field(“payload\_count”).
  - Evaluate self.data\_import.db\_set(“payload\_count”, len(payloads)).
- Bind dependencies create\_missing\_link\_records, get\_blocking\_warnings, get\_skipped\_row\_numbers.
- Set warnings from get\_blocking\_warnings(self.import\_file.get\_all\_warnings(), self.import\_file, self.data\_import).
- If warnings.
  - Set self.blocked\_by\_warnings from true.
  - If self.console.
    - Evaluate self.print\_grouped\_warnings(warnings).
  - Otherwise.
    - Evaluate self.data\_import.db\_set(“template\_warnings”, json.dumps(warnings)).
    - Evaluate self.data\_import.db\_set(“status”, “Pending”).
    - Evaluate Platform.publish\_realtime(“data\_import\_blocked”, mapping(“data\_import” → self.data\_import.name), user = Platform.session.user).
  - Return no value.
- Evaluate create\_missing\_link\_records(self.data\_import).
- Set previous\_status from self.data\_import.status.
- If self.data\_import.name.
  - Evaluate self.data\_import.db\_set(“status”, “In Progress”).
- Set import\_log from list().
- If (self.data\_import.name and Platform.db.exists(“Data Import”, self.data\_import.name)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.data\_import.name → Platform.db.exists(“Data Import”, self.data\_import.name).
  - Set import\_log from (Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”, “log\_index”, “import\_action”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”, “log\_index”, “import\_action”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”) → list().
- Set log\_index from 0.
- If (previous\_status belongs to tuple(“Partial Success”, “Error”, “Timed Out”) and len(import\_log) ≥ self.data\_import.payload\_count).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in previous\_status belongs to tuple(“Partial Success”, “Error”, “Timed Out”) → len(import\_log) ≥ self.data\_import.payload\_count.
  - Set import\_log from list of log for log drawn from import\_log where log.get(“success”).
    - Draw log from import\_log, keep a combination only if (log.get(“success”)).
  - Evaluate Platform.db.delete(“Data Import Log”, mapping(“success” → 0, “data\_import” → self.data\_import.name)).
- Set imported\_rows from set().
- Set failed\_count from 0.
- Set inserted\_count from 0.
- Set updated\_count from 0.
- For each log in import\_log.
  - Set log from Platform.\_dict(log).
  - If log.success.
    - If self.import\_type equals UPSERT.
      - If log.import\_action equals ACTION\_UPDATE.
        - Update updated\_count using + 1.
      - Otherwise.
        - Update inserted\_count using + 1.
    - Otherwise.
      - If self.import\_type equals UPDATE.
        - Update updated\_count using + 1.
      - Otherwise.
        - Update inserted\_count using + 1.
  - Otherwise.
    - Update failed\_count using + 1.
  - If (log.success or len(import\_log) &lt; self.data\_import.payload\_count).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in log.success → len(import\_log) &lt; self.data\_import.payload\_count.
    - Evaluate imported\_rows.update(json.loads(log.row\_indexes)).
  - Set log\_index from log.log\_index.
- Set total\_payload\_count from len(payloads).
- Set skipped\_rows from get\_skipped\_row\_numbers(self.data\_import).
- Set skipped\_payload\_count from 0.
- Set batch\_size from (Platform.conf.data\_import\_batch\_size or 1000).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.data\_import\_batch\_size → 1000.
- For each tuple(batch\_index, batched\_payloads) in enumerate(Platform.utils.create\_batch(payloads, batch\_size)).
  - For each tuple(i, payload) in enumerate(batched\_payloads).
    - Set doc from payload.doc.
    - Set row\_indexes from list of row.row\_number for row drawn from payload.rows.
      - Draw row from payload.rows.
    - Set current\_index from ((i + 1) + (batch\_index × batch\_size)).
    - Set row\_set from set(row\_indexes).
    - If row\_set.intersection(skipped\_rows).
      - Update skipped\_payload\_count using + 1.
      - Evaluate self.\_publish\_skip\_progress(current\_index, total\_payload\_count, inserted\_count, updated\_count, row\_indexes = row\_indexes, reason = translated “Skipped row {0}”.format(row\_indexes at 0), …).
      - Continue with the next iteration or loop test.
    - If row\_set.intersection(imported\_rows).
      - Evaluate self.\_publish\_skip\_progress(current\_index, total\_payload\_count, inserted\_count, updated\_count, row\_indexes = row\_indexes, reason = translated “Already imported row {0}”.format(row\_indexes at 0), …).
      - Continue with the next iteration or loop test.
    - Set start from timeit.default\_timer().
    - Attempt the following.
      - Set tuple(doc, import\_action) from self.process\_doc(doc).
      - Set processing\_time from (timeit.default\_timer() − start).
      - Set eta from self.get\_eta(current\_index, total\_payload\_count, processing\_time).
      - If self.import\_type equals UPSERT.
        - If import\_action equals ACTION\_UPDATE.
          - Update updated\_count using + 1.
        - Otherwise.
          - Update inserted\_count using + 1.
      - Otherwise.
        - If self.import\_type equals UPDATE.
          - Update updated\_count using + 1.
        - Otherwise.
          - Update inserted\_count using + 1.
      - If self.console.
        - Evaluate update\_progress\_bar(formatted text Importing {self.doctype}: {total\_payload\_count} records, (current\_index − 1), total\_payload\_count).
      - Otherwise.
        - If total\_payload\_count &gt; 5.
          - Evaluate self.\_publish\_progress\_event(current\_index = current\_index, total\_payload\_count = total\_payload\_count, eta = eta, inserted\_count = inserted\_count, …).
      - Set log\_details from mapping(“success” → true, “docname” → doc.name, “row\_indexes” → row\_indexes).
      - If self.import\_type equals UPSERT.
        - Set log\_details at “import\_action” from import\_action.
      - Evaluate create\_import\_log(self.data\_import.name, log\_index, log\_details).
      - Update log\_index using + 1.
      - Evaluate Platform.db.commit().
    - On failure (Exception).
      - Set messages from Platform.local.message\_log.
      - Evaluate Platform.clear\_messages().
      - Evaluate Platform.db.rollback().
      - Evaluate create\_import\_log(self.data\_import.name, log\_index, mapping(“success” → false, “exception” → Platform.get\_traceback(), “messages” → messages, “row\_indexes” → row\_indexes)).
      - Update log\_index using + 1.
      - Update failed\_count using + 1.
      - Attempt the following.
        - Evaluate Platform.logger(“data\_import”).error(formatted text Data Import {self.data\_import.name}: row(s) {row\_indexes} failed to import, exc\_info = true).
      - On failure (Exception).
        - Take no action here.
      - Set processing\_time from (timeit.default\_timer() − start).
      - Evaluate self.\_publish\_progress\_event(current\_index = current\_index, total\_payload\_count = total\_payload\_count, eta = self.get\_eta(current\_index, total\_payload\_count, processing\_time), inserted\_count = inserted\_count, …).
- Set import\_log from (Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”, “log\_index”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”, “log\_index”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”) → list().
- Set successes from list().
- Set failures from list().
- For each log in import\_log.
  - If log.get(“success”).
    - Evaluate successes.append(log).
  - Otherwise.
    - Evaluate failures.append(log).
- Set attempted\_payload\_count from (total\_payload\_count − skipped\_payload\_count).
- If (attempted\_payload\_count equals 0 or len(successes) equals attempted\_payload\_count).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in attempted\_payload\_count equals 0 → len(successes) equals attempted\_payload\_count.
  - Set status from “Success”.
- Otherwise.
  - If (len(failures) ≥ attempted\_payload\_count and len(successes) equals 0).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(failures) ≥ attempted\_payload\_count → len(successes) equals 0.
    - Set status from “Error”.
  - Otherwise.
    - If (len(failures) &gt; 0 and len(successes) &gt; 0).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(failures) &gt; 0 → len(successes) &gt; 0.
      - Set status from “Partial Success”.
      - Attempt the following.
        - Evaluate Platform.logger(“data\_import”).warning(formatted text Data Import {self.data\_import.name}: {len(failures)} of {attempted\_payload\_count} rows failed).
      - On failure (Exception).
        - Take no action here.
    - Otherwise.
      - Set status from “Pending”.
- If self.console.
  - Evaluate self.print\_import\_log(import\_log).
- Otherwise.
  - Evaluate self.data\_import.db\_set(“status”, status).
- Evaluate self.after\_import().
- Return import\_log.

**Methods declared on this owner** [before import](operations-012.md#op-234e048b05e2ae), [print grouped warnings](operations-012.md#op-e602095004ccb1), [publish skip progress](operations-012.md#op-33f4d0cdd39c58), [process doc](operations-012.md#op-1a2016088cad34), [get eta](operations-012.md#op-df8d24cac55872), [publish progress event](operations-012.md#op-c6200c0052fe30), [build success activity](operations-012.md#op-d60e48bdca466a), [build error activity](operations-012.md#op-984779ea5fc5cc), [print import log](operations-012.md#op-0724e3acbbadc1), [after import](operations-012.md#op-0b8213e6c7de55).

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“data\_import\_blocked”, mapping(“data\_import” → self.data\_import.name), user = Platform.session.user).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L43) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1246) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1239)

<a id="op-0b8213e6c7de55"></a>
### Importer.after import

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_after_import`

**Inputs** self.

**Local steps**

- Set Platform.flags.in\_import from false.
- Set Platform.flags.mute\_emails from false.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L40) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1239) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1232)

<a id="op-c6200c0052fe30"></a>
### Importer.publish progress event

`operation_foundation_binding_foundation_core_doctype_data_import_importer_importer_publish_progress_event`

**Inputs** self, current\_index (named only), total\_payload\_count (named only), inserted\_count (named only), updated\_count (named only), failed\_count (named only), success (named only, default no value), skipping (named only, default false), row\_indexes (named only, default no value), docname (named only, default no value), eta (named only, default 0), activity (named only, default no value).

**State and service calls** publish realtime with “data\_import\_progress”.

**Explicit results** no value.

**Local steps**

- If total\_payload\_count ≤ 5.
  - Return no value.
- Set payload from mapping(“current” → current\_index, “total” → total\_payload\_count, “data\_import” → self.data\_import.name, “eta” → eta, …).
- If success is distinct from no value.
  - Set payload at “success” from success.
- If row\_indexes.
  - Set payload at “row\_indexes” from row\_indexes.
- If docname.
  - Set payload at “docname” from docname.
- If activity.
  - Set payload at “activity” from activity.
- Evaluate Platform.publish\_realtime(“data\_import\_progress”, payload, user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“data\_import\_progress”, payload, user = Platform.session.user).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L156) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L638) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L614)

<a id="op-33f4d0cdd39c58"></a>
### Importer.publish skip progress

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_publish_skip_progress`

**Inputs** self, current\_index, total\_payload\_count, inserted\_count, updated\_count, failed\_count, row\_indexes = no value, reason = no value.

**Local steps**

- Evaluate self.\_publish\_progress\_event(current\_index = current\_index, total\_payload\_count = total\_payload\_count, inserted\_count = inserted\_count, updated\_count = updated\_count, …).
  - Value choice on reason — true gives mapping(“kind” → “info”, “text” → reason), false gives no value.

If control reaches the end, it returns no value.

**Methods declared on this owner** [publish progress event](operations-012.md#op-c6200c0052fe30).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L46) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1253) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1246)

<a id="op-d60e48bdca466a"></a>
### Importer.build success activity

`operation_foundation_binding_foundation_core_doctype_data_import_importer_importer_build_success_activity`

**Inputs** self, import\_action, docname.

**Explicit results** mapping(“kind” → “success”, “text” → formatted text {action} {docname}).

**Local steps**

- If self.import\_type equals UPSERT.
  - Set action from translated “Updated” when import\_action equals ACTION\_UPDATE, otherwise translated “Inserted”.
    - Value choice on import\_action equals ACTION\_UPDATE — true gives translated “Updated”, false gives translated “Inserted”.
- Otherwise.
  - If self.import\_type equals UPDATE.
    - Set action from translated “Updated”.
  - Otherwise.
    - Set action from translated “Imported”.
- Return mapping(“kind” → “success”, “text” → formatted text {action} {docname}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L155) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L637) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L613)

<a id="op-984779ea5fc5cc"></a>
### Importer.build error activity

`operation_foundation_binding_foundation_core_doctype_data_import_importer_importer_build_error_activity`

**Inputs** self, messages, row\_indexes.

**Explicit results** mapping(“kind” → “error”, “text” → cstr(message\_text), “is\_html” → is\_html).

**Local steps**

- Set message\_text from empty text.
- Set is\_html from false.
- If (isinstance(messages, list) and messages).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(messages, list) → messages.
  - Set first\_message from messages at 0.
  - If isinstance(first\_message, dict).
    - If first\_message.get(“message”).
      - Set message\_text from clean\_html(first\_message.get(“message”)).
      - Set is\_html from true.
    - Otherwise.
      - Set message\_text from (first\_message.get(“title”) or empty text).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in first\_message.get(“title”) → empty text.
  - Otherwise.
    - If isinstance(first\_message, str).
      - Set message\_text from first\_message.
- If not message\_text.
  - Set first\_row from row\_indexes at 0 when row\_indexes, otherwise no value.
    - Value choice on row\_indexes — true gives row\_indexes at 0, false gives no value.
  - Set message\_text from translated “Row {0} failed”.format(first\_row) when first\_row, otherwise translated “Row validation failed”.
    - Value choice on first\_row — true gives translated “Row {0} failed”.format(first\_row), false gives translated “Row validation failed”.
- Return mapping(“kind” → “error”, “text” → cstr(message\_text), “is\_html” → is\_html).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L154) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L636) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L612)

<a id="op-1a2016088cad34"></a>
### Importer.process doc

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_process_record`

**Inputs** self, doc.

**Explicit results** self.provider.import\_row(self, doc) · tuple(self.insert\_record(doc), no value) · tuple(self.update\_record(doc), no value) · self.upsert\_record(doc).

**Local steps**

- If getattr(self, “provider”, no value).
  - Return self.provider.import\_row(self, doc).
- If self.import\_type equals INSERT.
  - Return tuple(self.insert\_record(doc), no value).
- If self.import\_type equals UPDATE.
  - Return tuple(self.update\_record(doc), no value).
- Return self.upsert\_record(doc).

**Methods declared on this owner** [insert record](operations-012.md#op-47d200e2fa88d8), [update record](operations-012.md#op-8ee2b485c8d71f), [upsert record](operations-012.md#op-334e6e5691626e).

**Values supplied outside this operation** selected callable from getattr(self, “provider”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L45) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1252) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1245)

<a id="op-334e6e5691626e"></a>
### Importer.upsert record

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_upsert_record`

**Inputs** self, doc.

**Record and data access** read self.doctype via exists.

**Explicit results** tuple(result, ACTION\_UPDATE) · tuple(self.insert\_record(doc), ACTION\_INSERT).

**Local steps**

- Set id\_field from get\_id\_field(self.doctype).
- Set id\_value from doc.get(id\_field.fieldname).
- If (id\_value and Platform.db.exists(self.doctype, id\_value)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in id\_value → Platform.db.exists(self.doctype, id\_value).
  - Set result from self.update\_record(doc, raise\_if\_no\_changes = false).
  - If self.\_uses\_tree\_aliases.
    - Evaluate self.\_register\_inserted\_name(doc, result).
  - Return tuple(result, ACTION\_UPDATE).
- Return tuple(self.insert\_record(doc), ACTION\_INSERT).

**Methods declared on this owner** [update record](operations-012.md#op-8ee2b485c8d71f), [register inserted name](operations-012.md#op-2039f5766189ac), [insert record](operations-012.md#op-47d200e2fa88d8).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L3699) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1257) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1250)

<a id="op-47d200e2fa88d8"></a>
### Importer.insert record

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_insert_record`

**Inputs** self, doc.

**State and service calls** request new\_doc for self.doctype · call insert on new\_doc · call submit on new\_doc.

**Explicit results** new\_doc.

**Local steps**

- Set meta from Platform.get\_meta(self.doctype).
- Set new\_doc from Platform.new\_doc(self.doctype).
- Evaluate new\_doc.update(doc).
- If (not doc.name and (meta.autoname or empty text).lower() differs from “prompt”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not doc.name → (meta.autoname or empty text).lower() differs from “prompt”.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in meta.autoname → empty text.
  - Evaluate new\_doc.set(“name”, no value).
- If (self.\_uses\_tree\_aliases and self.\_tree\_parent\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_uses\_tree\_aliases → self.\_tree\_parent\_field.
  - Evaluate self.\_resolve\_tree\_parent\_link(doc).
  - Evaluate new\_doc.set(self.\_tree\_parent\_field, doc.get(self.\_tree\_parent\_field)).
- Set new\_doc.flags.updater\_reference from mapping(“doctype” → self.data\_import.doctype, “docname” → self.data\_import.name, “label” → translated “via Data Import”).
- Evaluate new\_doc.insert().
- If self.\_uses\_tree\_aliases.
  - Evaluate self.\_register\_inserted\_name(doc, new\_doc).
- If (meta.is\_submittable and self.data\_import.submit\_after\_import).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in meta.is\_submittable → self.data\_import.submit\_after\_import.
  - Evaluate new\_doc.submit().
- Return new\_doc.

**Methods declared on this owner** [resolve tree parent link](operations-012.md#op-4cdd220487bdf6), [register inserted name](operations-012.md#op-2039f5766189ac).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L3985) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1248) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1241)

<a id="op-4cdd220487bdf6"></a>
### Importer.resolve tree parent link

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_resolve_tree_parent_link`

**Inputs** self, doc.

**Explicit results** no value.

**Local steps**

- Set parent from doc.get(self.\_tree\_parent\_field).
- If parent belongs to INVALID\_VALUES.
  - Return no value.
- Set parent from cstr(parent).strip().
- Set resolved from self.\_inserted\_name\_map.get(parent).
- If resolved.
  - Set doc at self.\_tree\_parent\_field from resolved.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L4534) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1255) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1248)

<a id="op-2039f5766189ac"></a>
### Importer.register inserted name

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_register_inserted_name`

**Inputs** self, doc, new\_doc.

**Local steps**

- If self.\_tree\_alias\_field.
  - Set alias from (new\_doc.get(self.\_tree\_alias\_field) or doc.get(self.\_tree\_alias\_field)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in new\_doc.get(self.\_tree\_alias\_field) → doc.get(self.\_tree\_alias\_field).
  - If alias does not belong to INVALID\_VALUES.
    - Set self.\_inserted\_name\_map at cstr(alias).strip() from new\_doc.name.
- Set id\_value from doc.get(self.\_id\_fieldname).
- If id\_value does not belong to INVALID\_VALUES.
  - Set self.\_inserted\_name\_map at cstr(id\_value).strip() from new\_doc.name.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L4739) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1254) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1247)

<a id="op-8ee2b485c8d71f"></a>
### Importer.update record

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_update_record`

**Inputs** self, doc, raise\_if\_no\_changes = true.

**Record and data access** resolve a document from self.doctype via get\_doc.

**State and service calls** request copy\_doc for updated\_doc · call save on updated\_doc · call submit on updated\_doc.

**Explicit results** updated\_doc.

**Explicit failure paths** validation helper — translated “No changes to update”.

**Local steps**

- Set id\_field from get\_id\_field(self.doctype).
- Set updated\_doc from Platform.get\_doc(self.doctype, doc.get(id\_field.fieldname)).
- Set existing\_doc from Platform.copy\_doc(updated\_doc).
- Evaluate updated\_doc.update(doc).
- If (self.\_uses\_tree\_aliases and self.\_tree\_parent\_field).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.\_uses\_tree\_aliases → self.\_tree\_parent\_field.
  - Evaluate self.\_resolve\_tree\_parent\_link(doc).
  - Evaluate updated\_doc.set(self.\_tree\_parent\_field, doc.get(self.\_tree\_parent\_field)).
- Set submit\_after\_import from (updated\_doc.meta.is\_submittable and self.data\_import.submit\_after\_import and updated\_doc.docstatus.is\_draft()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in updated\_doc.meta.is\_submittable → self.data\_import.submit\_after\_import → updated\_doc.docstatus.is\_draft().
- Set updated\_doc.flags.updater\_reference from mapping(“doctype” → self.data\_import.doctype, “docname” → self.data\_import.name, “label” → translated “via Data Import”).
- If get\_diff(existing\_doc, updated\_doc).
  - Evaluate updated\_doc.save().
- Otherwise.
  - If (raise\_if\_no\_changes and not submit\_after\_import).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in raise\_if\_no\_changes → not submit\_after\_import.
    - Call the validation error handler Platform.throw(translated “No changes to update”).
- If submit\_after\_import.
  - Evaluate updated\_doc.submit().
- Return updated\_doc.

**Methods declared on this owner** [resolve tree parent link](operations-012.md#op-4cdd220487bdf6).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L47) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1256) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1249)

<a id="op-df8d24cac55872"></a>
### Importer.get eta

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_get_eta`

**Inputs** self, current, total, processing\_time.

**Explicit results** self.last\_eta.

**Local steps**

- Set self.last\_eta from getattr(self, “last\_eta”, 0).
- Set remaining from (total − current).
- Set eta from (processing\_time × remaining).
- If (not self.last\_eta or eta &lt; self.last\_eta).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.last\_eta → eta &lt; self.last\_eta.
  - Set self.last\_eta from eta.
- Return self.last\_eta.

**Values supplied outside this operation** selected callable from getattr(self, “last\_eta”, 0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L5549) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1245) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1238)

<a id="op-716519f6136452"></a>
### Importer.export errored rows

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_export_errored_rows`

**Inputs** self.

**Record and data access** read “Data Import Log” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies build\_csv\_response.
- If not self.data\_import.
  - Return no value.
- Set import\_log from (Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”) or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”) → list().
- Set failures from list of log for log drawn from import\_log where not log.get(“success”).
  - Draw log from import\_log, keep a combination only if (not log.get(“success”)).
- Set row\_indexes from list().
- For each f in failures.
  - Evaluate row\_indexes.extend(json.loads(f.get(“row\_indexes”, list()))).
- Set row\_indexes from list(set(row\_indexes)).
- Evaluate row\_indexes.sort().
- Set header\_row from list of col.header\_title for col drawn from self.import\_file.columns.
  - Draw col from self.import\_file.columns.
- Set rows from list(header\_row).
- Update rows using + list of row.data for row drawn from self.import\_file.data where row.row\_number belongs to row\_indexes.
  - Draw row from self.import\_file.data, keep a combination only if (row.row\_number belongs to row\_indexes).
- Evaluate build\_csv\_response(rows, translated self.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L5752) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1241) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1234)

<a id="op-51bf936535858f"></a>
### Importer.export skipped rows

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_export_skipped_rows`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- Bind dependencies build\_csv\_response.
- If (not self.data\_import or not self.data\_import.skipped\_rows).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not self.data\_import → not self.data\_import.skipped\_rows.
  - Return no value.
- Set skipped from set of cint(row.row\_number) for row drawn from self.data\_import.skipped\_rows.
  - Draw row from self.data\_import.skipped\_rows.
- Set header\_row from list of col.header\_title for col drawn from self.import\_file.columns.
  - Draw col from self.import\_file.columns.
- Set rows from list(header\_row).
- Update rows using + list of row.data for row drawn from self.import\_file.data where row.row\_number belongs to skipped.
  - Draw row from self.import\_file.data, keep a combination only if (row.row\_number belongs to skipped).
- Evaluate build\_csv\_response(rows, translated self.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L42) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1243) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1236)

<a id="op-49a882b094ceee"></a>
### Importer.export import log

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_export_import_log`

**Inputs** self.

**Record and data access** read “Data Import Log” via get\_all.

**Explicit results** no value.

**Local steps**

- Bind dependencies build\_csv\_response.
- If not self.data\_import.
  - Return no value.
- Set import\_log from Platform.get\_all(“Data Import Log”, fields = list(“row\_indexes”, “success”, “messages”, “exception”, …), filters = mapping(“data\_import” → self.data\_import.name), order\_by = “log\_index”).
- Set header\_row from list(“Row Numbers”, “Status”, “Message”, “Exception”).
- Set rows from list(header\_row).
- For each log in import\_log.
  - Set row\_number from json.loads(log.get(“row\_indexes”)) at 0.
  - Set status from “Success” when log.get(“success”), otherwise “Failure”.
    - Value choice on log.get(“success”) — true gives “Success”, false gives “Failure”.
  - Set message from “Successfully Imported {}”.format(log.get(“docname”)) when log.get(“success”), otherwise log.get(“messages”).
    - Value choice on log.get(“success”) — true gives “Successfully Imported {}”.format(log.get(“docname”)), false gives log.get(“messages”).
  - Set exception from Platform.utils.cstr(log.get(“exception”, empty text)).
  - Update rows using + list(list(row\_number, status, message, exception)).
- Evaluate build\_csv\_response(rows, self.doctype).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0052.json#L6610) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1242) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1235)

<a id="op-0724e3acbbadc1"></a>
### Importer.print import log

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_print_import_log`

**Inputs** self, import\_log.

**Local steps**

- Set failed\_records from list of log for log drawn from import\_log where not log.success.
  - Draw log from import\_log, keep a combination only if (not log.success).
- Set successful\_records from list of log for log drawn from import\_log where log.success.
  - Draw log from import\_log, keep a combination only if (log.success).
- If successful\_records.
  - Evaluate print().
  - Evaluate print(formatted text Successfully imported {len(successful\_records)} records out of {len(import\_log)}).
- If failed\_records.
  - Evaluate print(formatted text Failed to import {len(failed\_records)} records).
  - Set file\_name from formatted text {self.doctype}\_import\_on\_{Platform.utils.now()}.txt.
  - Evaluate print(“Check {} for errors”.format(os.path.join(“sites”, file\_name))).
  - Set text from empty text.
  - For each w in failed\_records.
    - Update text using + “Row Indexes: {}\\n”.format(str(w.get(“row\_indexes”, list()))).
    - Update text using + “Messages:\\n{}\\n”.format(whitespace '\\n'.join(w.get(“messages”, list()))).
    - Update text using + “Traceback:\\n{}\\n\\n”.format(w.get(“exception”)).
  - Within open(file\_name, “w”) bound as f.
    - Evaluate f.write(text).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now().

**Boundaries to resolve** late-bound calls, callee failures, file state, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1251) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1244)

<a id="op-e602095004ccb1"></a>
### Importer.print grouped warnings

`operation_foundation_core_record_definitions_data_import_importer_business_behavior_importer_print_grouped_warnings`

**Inputs** self, warnings.

**Local steps**

- Set warnings\_by\_row from mapping().
- Set other\_warnings from list().
- For each w in warnings.
  - If w.get(“row”).
    - Evaluate warnings\_by\_row.setdefault(w.get(“row”), list()).append(w).
  - Otherwise.
    - Evaluate other\_warnings.append(w).
- For each tuple(row\_number, warnings) in warnings\_by\_row.items().
  - Evaluate print(formatted text Row {row\_number}).
  - For each w in warnings.
    - Evaluate print(w.get(“message”)).
- For each w in other\_warnings.
  - Evaluate print(w.get(“message”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0053.json#L670) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1250) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1243)
