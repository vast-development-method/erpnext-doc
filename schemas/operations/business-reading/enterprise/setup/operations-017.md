# Company and master data · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Transaction deletion record

[Record definition](../../../../data/record-types/transaction_deletion_record.json)

<a id="op-fc0cf1c30b1c90"></a>
### Transaction Deletion Record.delete comments

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_delete_comments`

**Inputs** self, doctype, reference\_doc\_names.

**Local steps**

- If reference\_doc\_names.
  - Set comment from qb.DocType(“Comment”).
  - Evaluate nested operand in the contract(nested operand in the contract).delete().where((comment.reference\_doctype equals doctype bitwise and nested operand in the contract.reference\_name.isin(reference\_doc\_names))).run().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L3925) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1014) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L562)

<a id="op-56e1c5a46ef644"></a>
### Transaction Deletion Record.unlink attachments

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_transaction_deletion_record_unlink_attachments`

**Inputs** self, doctype, reference\_doc\_names.

**Record and data access** read “File” via get\_all · resolve a document from mapping(“doctype” → “File”, “file\_name” → “Transaction Deletion Review”, “is\_folder” → 1, “folder” → “Home”) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → “Transaction Deletion Review”, “is\_folder” → 1, “folder” → “Home”)).

**Explicit results** no value.

**Local steps**

- Set files from Platform.get\_all(“File”, filters = mapping(“attached\_to\_doctype” → doctype, “attached\_to\_name” → list(“in”, reference\_doc\_names))).
- Set file\_names from list of c.name for c drawn from files.
  - Draw c from files.
- If not file\_names.
  - Return no value.
- Set folder from Platform.get\_doc(mapping(“doctype” → “File”, “file\_name” → “Transaction Deletion Review”, “is\_folder” → 1, “folder” → “Home”)).insert(ignore\_permissions = true, ignore\_if\_duplicate = true).
- Set file from qb.DocType(“File”).
- For each batch in create\_batch(file\_names, self.batch\_size).
  - Evaluate nested operand in the contract(nested operand in the contract, nested operand in the contract).set(file.folder, folder.name).where(file.name.isin(batch)).run().
- Evaluate self.add\_comment(“Info”, translated “Detached attachments are retained in {0} for review.”.format(get\_link\_to\_form(“File”, folder.name))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L18) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1052) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L599)

<a id="op-5550e3447eaa72"></a>
### Get doctypes to be ignored

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_get_record_types_to_be_ignored`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** doctypes\_to\_be\_ignored.

**Local steps**

- Set doctypes\_to\_be\_ignored from list(“Account”, “Cost Center”, “Cost Center Allocation”, “Warehouse”, …).
- Evaluate doctypes\_to\_be\_ignored.extend((Platform.get\_hooks(“company\_data\_to\_be\_ignored”) or list())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“company\_data\_to\_be\_ignored”) → list().
- Return doctypes\_to\_be\_ignored.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“company\_data\_to\_be\_ignored”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L149) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1006) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L554)

<a id="op-56e098633fffc1"></a>
### Export to delete template

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_export_to_delete_template`

**Inputs** name.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Transaction Deletion Record” via get\_doc.

**Explicit results** doc.export\_to\_delete\_template\_method().

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set doc from Platform.get\_doc(“Transaction Deletion Record”, name).
- Evaluate doc.check\_permission(“read”).
- Return doc.export\_to\_delete\_template\_method().

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”), doc.check\_permission(“read”).

**Boundaries to resolve** stored data, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L147) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1002) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L550)

<a id="op-56775fed299782"></a>
### Process import template

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_process_import_template`

**Inputs** transaction\_deletion\_record\_name, file\_url.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from “Transaction Deletion Record” via get\_doc · resolve a document from “File” via get\_doc.

**Explicit results** doc.import\_to\_delete\_template\_method(csv\_content).

**Explicit failure paths** validation helper — translated “Invalid file URL” · validation helper — translated “File not found” · validation helper — translated “File does not belong to this Transaction Deletion Record” · validation helper — translated “Only CSV files are allowed” · validation helper — translated “File not found on server”.

**Local steps**

- Bind dependencies os.
- Set doc from Platform.get\_doc(“Transaction Deletion Record”, transaction\_deletion\_record\_name).
- Evaluate doc.check\_permission(“write”).
- If (not file\_url or “..” belongs to file\_url).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not file\_url → “..” belongs to file\_url.
  - Call the validation error handler Platform.throw(translated “Invalid file URL”).
- Attempt the following.
  - Set file\_doc from Platform.get\_doc(“File”, mapping(“file\_url” → file\_url)).
- On failure (Platform.DoesNotExistError).
  - Call the validation error handler Platform.throw(translated “File not found”).
- If (file\_doc.attached\_to\_doctype differs from “Transaction Deletion Record” or file\_doc.attached\_to\_name differs from transaction\_deletion\_record\_name).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in file\_doc.attached\_to\_doctype differs from “Transaction Deletion Record” → file\_doc.attached\_to\_name differs from transaction\_deletion\_record\_name.
  - Call the validation error handler Platform.throw(translated “File does not belong to this Transaction Deletion Record”).
- If (not file\_doc.file\_name or not nested operand in the contract.file\_name.lower().endswith(“.csv”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not file\_doc.file\_name → not file\_doc.file\_name.lower().endswith(“.csv”).
  - Call the validation error handler Platform.throw(translated “Only CSV files are allowed”).
- Set file\_path from file\_doc.get\_full\_path().
- If not os.path.isfile(file\_path).
  - Call the validation error handler Platform.throw(translated “File not found on server”).
- Within open(file\_path, encoding = “utf-8”) bound as f.
  - Set csv\_content from f.read().
- Return doc.import\_to\_delete\_template\_method(csv\_content).

**Values supplied outside this operation** effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L2) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1008) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L556)

<a id="op-9e9ea14555c6d5"></a>
### Is deletion doc running

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_is_deletion_record_running`

**Inputs** company = no value, err\_msg = no value.

**Wrappers, in declaration order** Platform.whitelist(), request\_cache.

**Record and data access** read “Transaction Deletion Record” via get\_value.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- Set running\_deletion\_job from Platform.db.get\_value(“Transaction Deletion Record”, mapping(“docstatus” → 1, “status” → tuple(“in”, list(“Running”, “Queued”))), “name”).
- If not running\_deletion\_job.
  - Return no value.
- Call the validation error handler Platform.throw(title = translated “Deletion in Progress!”, msg = translated “Transaction Deletion Record {0} is already running. {1}”.format(get\_link\_to\_form(“Transaction Deletion Record”, running\_deletion ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in err\_msg → empty text.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L5656) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1007) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L555)

<a id="op-8e716ef5da238f"></a>
### Check for running deletion job

`operation_enterprise_setup_record_definitions_transaction_deletion_record_business_behavior_check_for_running_deletion_job`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Explicit failure paths** validation helper.

**Local steps**

- If doc.doctype belongs to LEDGER\_ENTRY\_DOCTYPES.
  - Return no value.
- If doc.doctype belongs to PROTECTED\_CORE\_DOCTYPES.
  - Return no value.
- Set deletion\_name from Platform.cache.get\_value(formatted text deletion\_running\_doctype:{doc.doctype}).
- If deletion\_name.
  - Call the validation error handler Platform.throw(title = translated “Deletion in Progress!”, msg = translated “Transaction Deletion Record {0} is currently deleting {1}. Cannot save documents until deletion completes.”.format(get\_link\_to\_f ….

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0699.json#L5992) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1001) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L549)

## Record · Uom

<a id="op-78750a74ed5b82"></a>
### Validate uoms are enabled

`operation_enterprise_binding_enterprise_setup_doctype_uom_uom_validate_uoms_are_enabled`

**Inputs** uoms.

**Record and data access** read “UOM” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Unit of Measure {0} is disabled.”.format(Platform.bold(“, ”.join(disabled\_uoms))).

**Local steps**

- Set uoms from list(set(filter(no value, uoms))).
- If not uoms.
  - Return no value.
- Set disabled\_uoms from Platform.get\_all(“UOM”, filters = mapping(“name” → list(“in”, uoms), “enabled” → 0), pluck = “name”).
- If disabled\_uoms.
  - Call the validation error handler Platform.throw(translated “Unit of Measure {0} is disabled.”.format(Platform.bold(“, ”.join(disabled\_uoms)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L126) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L183)

<a id="op-7d59ed0ee6a207"></a>
### UOM.before rename

`operation_enterprise_binding_enterprise_setup_doctype_uom_uom_uom_before_rename`

**Inputs** self, old\_name, new\_name, merge = false.

**Record and data access** read “UOM Conversion Detail” via get\_all.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Cannot merge Unit of Measure {0} into {1} because Item {2} uses both.”.format(Platform.bold(old\_name), Platform.bold(new\_name), Platform.bold(conflicting\_items at 0)).

**Local steps**

- If not merge.
  - Return no value.
- Set item\_uoms from mapping().
- For each row in Platform.get\_all(“UOM Conversion Detail”, filters = mapping(“parenttype” → “Item”, “uom” → list(“in”, list(old\_name, new\_name))), fields = list(“parent”, “uom”)).
  - Evaluate item\_uoms.setdefault(row.parent, set()).add(row.uom).
- If conflicting\_items bound to list of item for tuple(item, uoms) drawn from item\_uoms.items() where len(uoms) equals 2.
  - Draw tuple(item, uoms) from item\_uoms.items(), keep a combination only if (len(uoms) equals 2).
  - Call the validation error handler Platform.throw(translated “Cannot merge Unit of Measure {0} into {1} because Item {2} uses both.”.format(Platform.bold(old\_name), Platform.bold(new\_name), Platform.bold(conflicting\_items at 0))).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L125) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L182)

## Record · Uom conversion factor

<a id="op-ba5fb4befa8e17"></a>
### UOMConversion Factor.validate

`operation_enterprise_binding_enterprise_setup_doctype_uom_conversion_factor_uom_conversion_factor_uomconversionfactor_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Value must be greater than zero.” · validation helper — translated “From UOM and To UOM must be different.” · validation helper — translated “A conversion factor already exists between these UOMs.”.

**Local steps**

- If flt(self.value) ≤ 0.
  - Call the validation error handler Platform.throw(translated “Value must be greater than zero.”).
- If self.from\_uom equals self.to\_uom.
  - Call the validation error handler Platform.throw(translated “From UOM and To UOM must be different.”).
- Set conversion from Platform.qb.DocType(“UOM Conversion Factor”).
- Set duplicate from nested operand in the contract(nested operand in the contract).where(nested operand in the contract.name differs from nested operand in the contract.name).limit(1).run().
- If duplicate.
  - Call the validation error handler Platform.throw(translated “A conversion factor already exists between these UOMs.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L124) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L684) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L181)

## Service · Utils

<a id="op-62a2544e591ed9"></a>
### Get pegged currencies

`operation_enterprise_setup_utils_business_behavior_get_pegged_currencies`

**Inputs** no declared parameters.

**Record and data access** read “Pegged Currency Details” via get\_all.

**Explicit results** pegged\_map.

**Local steps**

- Set pegged\_currencies from Platform.get\_all(“Pegged Currency Details”, filters = mapping(“parent” → “Pegged Currencies”), fields = list(“source\_currency”, “pegged\_against”, “pegged\_exchange\_rate”)).
- Set pegged\_map from mapping of currency.source\_currency → mapping(“pegged\_against” → currency.pegged\_against, “ratio” → flt(currency.pegged\_exchange\_rate)) for currency drawn from pegged\_currencies.
  - Draw currency from pegged\_currencies.
- Return pegged\_map.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L4996) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1135) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L676)

<a id="op-a12654da7903fb"></a>
### Get pegged rate

`operation_enterprise_setup_utils_business_behavior_get_pegged_rate`

**Inputs** pegged\_map, from\_currency, to\_currency, transaction\_date = no value.

**Explicit results** ((1 ÷ from\_entry at “ratio”) × to\_entry at “ratio”) · no value · (((1 ÷ from\_entry at “ratio”) × base\_rate) × to\_entry at “ratio”) · flt(from\_entry at “ratio”) · (1 ÷ flt(to\_entry at “ratio”)).

**Local steps**

- Set from\_entry from pegged\_map.get(from\_currency).
- Set to\_entry from pegged\_map.get(to\_currency).
- If (from\_currency belongs to pegged\_map and to\_currency belongs to pegged\_map).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_currency belongs to pegged\_map → to\_currency belongs to pegged\_map.
  - If from\_entry at “pegged\_against” equals to\_entry at “pegged\_against”.
    - Return ((1 ÷ from\_entry at “ratio”) × to\_entry at “ratio”).
  - Set base\_from from from\_entry at “pegged\_against”.
  - Set base\_to from to\_entry at “pegged\_against”.
  - Set base\_rate from get\_exchange\_rate(base\_from, base\_to, transaction\_date).
  - If not base\_rate.
    - Return no value.
  - Return (((1 ÷ from\_entry at “ratio”) × base\_rate) × to\_entry at “ratio”).
- If (from\_entry and from\_entry at “pegged\_against” equals to\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_entry → from\_entry at “pegged\_against” equals to\_currency.
  - Return flt(from\_entry at “ratio”).
- If (to\_entry and to\_entry at “pegged\_against” equals from\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_entry → to\_entry at “pegged\_against” equals from\_currency.
  - Return (1 ÷ flt(to\_entry at “ratio”)).
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0704.json#L5219) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1136) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L677)

<a id="op-0a4f9212770f33"></a>
### Get stored exchange rate

`operation_enterprise_binding_enterprise_setup_utils_get_stored_exchange_rate`

**Inputs** from\_currency, to\_currency, transaction\_date, args = no value, checkpoint\_date = no value.

**Record and data access** read “Currency Exchange” via get\_all.

**Explicit results** flt(entries at 0.exchange\_rate).

**Local steps**

- Set filters from list(list(“date”, “&lt;=”, getdate(transaction\_date)), list(“from\_currency”, “=”, from\_currency), list(“to\_currency”, “=”, to\_currency)).
- Set order\_by from “date desc”.
- If args equals “for\_buying”.
  - Evaluate filters.append(list(“for\_buying”, “=”, 1)).
  - Update order\_by using + “, for\_selling asc”.
- Otherwise.
  - If args equals “for\_selling”.
    - Evaluate filters.append(list(“for\_selling”, “=”, 1)).
    - Update order\_by using + “, for\_buying asc”.
- If checkpoint\_date.
  - Evaluate filters.append(list(“date”, “&gt;”, getdate(checkpoint\_date))).
- Set entries from Platform.get\_all(“Currency Exchange”, fields = list(“exchange\_rate”), filters = filters, order\_by = (order\_by + “, name desc”), limit = 1).
- If entries.
  - Return flt(entries at 0.exchange\_rate).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L131) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L188)

<a id="op-888b22eef0e626"></a>
### Get exchange rate

`operation_enterprise_setup_utils_business_behavior_get_exchange_rate`

**Inputs** from\_currency, to\_currency, transaction\_date = no value, args = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Currency” via exists · resolve a document from “Accounts Settings” via get\_cached\_doc · read “Currency Exchange Settings” via get\_single\_value · resolve a document from “Currency Exchange Settings” via get\_cached\_doc.

**State and service calls** msgprint with translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually”.format(from\_currency, to\_currency, transaction\_date).

**Explicit results** no value · 1 · rate · (1 ÷ reverse\_rate) · 0.0 · 1 additional forms in the steps below.

**Explicit failure paths** validation helper — translated “Invalid currency: {0}”.format(currency) · validation helper — translated “Invalid transaction date” · validation helper with Platform.PermissionError — translated “Only system users can fetch exchange rates from an external provider.” · ValueError(“Invalid exchange rate”) · ValueError(“Exchange rate must be a positive finite number”) · 1 additional forms in the steps below.

**Local steps**

- If not (from\_currency and to\_currency).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in from\_currency → to\_currency.
  - Return no value.
- For each currency in tuple(from\_currency, to\_currency).
  - If (not isinstance(currency, str) or not Platform.db.exists(“Currency”, currency)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isinstance(currency, str) → not Platform.db.exists(“Currency”, currency).
    - Call the validation error handler Platform.throw(translated “Invalid currency: {0}”.format(currency)).
- If from\_currency equals to\_currency.
  - Return 1.
- Set transaction\_date from getdate(transaction\_date).
- If not transaction\_date.
  - Call the validation error handler Platform.throw(translated “Invalid transaction date”).
- Set transaction\_date from transaction\_date.isoformat().
- Set currency\_settings from Platform.get\_cached\_doc(“Accounts Settings”).
- Set allow\_stale\_rates from currency\_settings.get(“allow\_stale”).
- Set checkpoint\_date from no value.
- If not allow\_stale\_rates.
  - Set checkpoint\_date from add\_days(transaction\_date, negative currency\_settings.get(“stale\_days”)).
- Set rate from get\_stored\_exchange\_rate(from\_currency, to\_currency, transaction\_date, args, …).
- If rate is distinct from no value.
  - Return rate.
- Set reverse\_args from mapping(“for\_buying” → “for\_selling”, “for\_selling” → “for\_buying”).get(args, args).
- Set reverse\_rate from get\_stored\_exchange\_rate(to\_currency, from\_currency, transaction\_date, reverse\_args, …).
- If reverse\_rate.
  - Return (1 ÷ reverse\_rate).
- If Platform.get\_single\_value(“Currency Exchange Settings”, “disabled”).
  - Return 0.0.
- Set pegged\_currencies from mapping().
- If currency\_settings.allow\_pegged\_currencies\_exchange\_rates.
  - Set pegged\_currencies from get\_pegged\_currencies().
  - If rate bound to get\_pegged\_rate(pegged\_currencies, from\_currency, to\_currency, transaction\_date).
    - Return rate.
- Attempt the following.
  - Set cache from Platform.cache().
  - Set key from formatted text currency\_exchange\_rate\_{transaction\_date}:{from\_currency}:{to\_currency}.
  - Set value from cache.get\_value(key).
  - If not value.
    - If not is\_system\_user().
      - Call the validation error handler Platform.throw(translated “Only system users can fetch exchange rates from an external provider.”, Platform.PermissionError).
    - Set settings from Platform.get\_cached\_doc(“Currency Exchange Settings”).
    - Set req\_params from mapping(“transaction\_date” → transaction\_date, “from\_currency” → from\_currency when from\_currency does not belong to pegged\_currencies, otherwise pegged\_currencies at from\_currency at “pegged\_against”, “to ….
      - Value choice on from\_currency does not belong to pegged\_currencies — true gives from\_currency, false gives pegged\_currencies at from\_currency at “pegged\_against”.
      - Value choice on to\_currency does not belong to pegged\_currencies — true gives to\_currency, false gives pegged\_currencies at to\_currency at “pegged\_against”.
    - Set params from mapping().
    - For each row in settings.req\_params.
      - Set params at row.key from format\_ces\_api(row.value, req\_params).
    - Set response from requests.get(format\_ces\_api(settings.api\_endpoint, mapping of key → quote(value, safe = empty text) for tuple(key, value) drawn from req\_params.items()), params = params, timeout = (Platform.conf.get(“curr ….
      - Draw tuple(key, value) from req\_params.items().
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“currency\_exchange\_request\_timeout”) → 10.
    - Evaluate response.raise\_for\_status().
    - Set value from response.json().
    - For each res\_key in settings.result\_key.
      - Set value from value at format\_ces\_api(str(res\_key.key), req\_params).
    - If isinstance(value, bool).
      - Raise ValueError(“Invalid exchange rate”).
    - Set value from float(value).
    - If (not isfinite(value) or value ≤ 0).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isfinite(value) → value ≤ 0.
      - Raise ValueError(“Exchange rate must be a positive finite number”).
    - Evaluate cache.set\_value(key, value, expires\_in\_sec = 21600).
  - Set value from float(value).
  - If (not isfinite(value) or value ≤ 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not isfinite(value) → value ≤ 0.
    - Raise ValueError(“Exchange rate must be a positive finite number”).
  - If (currency\_settings.allow\_pegged\_currencies\_exchange\_rates and to\_currency belongs to pegged\_currencies).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in currency\_settings.allow\_pegged\_currencies\_exchange\_rates → to\_currency belongs to pegged\_currencies.
    - Update value using × flt(pegged\_currencies at to\_currency at “ratio”).
  - If (currency\_settings.allow\_pegged\_currencies\_exchange\_rates and from\_currency belongs to pegged\_currencies).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in currency\_settings.allow\_pegged\_currencies\_exchange\_rates → from\_currency belongs to pegged\_currencies.
    - Update value using ÷ flt(pegged\_currencies at from\_currency at “ratio”).
  - Return flt(value).
- On failure (Platform.PermissionError).
  - Propagate the active failure.
- On failure (Exception).
  - Evaluate Platform.log\_error(“Unable to fetch exchange rate”).
  - Evaluate Platform.msgprint(translated “Unable to find exchange rate for {0} to {1} for key date {2}. Please create a Currency Exchange record manually”.format(from\_currency, to\_currency, transaction\_date)).
  - Return 0.0.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Accounts Settings”), Platform.get\_single\_value(“Currency Exchange Settings”, “disabled”) and 1 further calls · service or queued work from requests.get(format\_ces\_api(settings.api\_endpoint, mapping of key → quote(value, safe = empty text) for tuple(key, value) drawn from req\_params.items()), params = params, timeout = (Platform.conf.get(“curr ….

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L31) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1134) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L675)

<a id="op-b0fc791bb08e1d"></a>
### Format ces api

`operation_enterprise_setup_utils_business_behavior_format_ces_application_programming_interface`

**Inputs** data, param.

**Explicit results** data.format(transaction\_date = param.get(“transaction\_date”), to\_currency = param.get(“to\_currency”), from\_currency = param.get(“from\_currency”)).

**Local steps**

- Return data.format(transaction\_date = param.get(“transaction\_date”), to\_currency = param.get(“to\_currency”), from\_currency = param.get(“from\_currency”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1133) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L674)

<a id="op-fb67f527313ee8"></a>
### Enable all roles and domains

`operation_enterprise_setup_utils_business_behavior_enable_all_roles_and_domains`

**Inputs** no declared parameters.

**Local steps**

- Evaluate \_enable\_all\_roles\_for\_admin().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L151) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1131) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L672)

<a id="op-fa1e356f400db1"></a>
### Enable all roles for admin

`operation_enterprise_setup_utils_business_behavior_enable_all_roles_for_admin`

**Inputs** no declared parameters.

**Record and data access** read “Role” via get\_all · read “Has Role” via get\_values.

**Local steps**

- Bind dependencies add\_all\_roles\_to.
- Set all\_roles from set(Platform.get\_all(“Role”, pluck = “name”)).
- Set admin\_roles from set(Platform.db.get\_values(“Has Role”, mapping(“parent” → “Administrator”), fieldname = “role”, pluck = “role”)).
- If all\_roles.difference(admin\_roles).
  - Evaluate add\_all\_roles\_to(“Administrator”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L190) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1132) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L673)

<a id="op-db91a7eadcf240"></a>
### Set defaults for tests

`operation_enterprise_setup_utils_business_behavior_set_defaults_for_tests`

**Inputs** no declared parameters.

**State and service calls** request set\_single\_value on “Selling Settings” · request set\_single\_value on “Stock Settings”.

**Local steps**

- Set defaults from mapping(“customer\_group” → get\_root\_of(“Customer Group”), “territory” → get\_root\_of(“Territory”)).
- Evaluate Platform.db.set\_single\_value(“Selling Settings”, defaults).
- For each tuple(key, value) in defaults.items().
  - Evaluate Platform.db.set\_default(key, value).
- Evaluate Platform.db.set\_single\_value(“Stock Settings”, “auto\_insert\_price\_list\_rate\_if\_missing”, 0).
- Evaluate Platform.db.set\_single\_value(“Stock Settings”, “enable\_serial\_and\_batch\_no\_for\_item”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L431) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1138) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L679)

<a id="op-ad1cac1e4ef59c"></a>
### Insert record

`operation_enterprise_setup_utils_business_behavior_insert_record`

**Inputs** records.

**Local steps**

- Bind dependencies make\_records.
- Evaluate make\_records(records).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L728) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1137) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L678)

<a id="op-9d0f6a1af2990b"></a>
### Welcome email

`operation_enterprise_setup_utils_business_behavior_welcome_email`

**Inputs** no declared parameters.

**Explicit results** title.

**Local steps**

- Set site\_name from (get\_default\_company() or “Enterprise”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_default\_company() → “Enterprise”.
- Set title from translated “Welcome to {0}”.format(site\_name).
- Return title.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0705.json#L788) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1139) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L680)

<a id="op-d8634fd423e02d"></a>
### Identity

`operation_enterprise_binding_enterprise_setup_utils_identity`

**Inputs** x, remaining positional values args, remaining named values kwargs.

**Explicit results** x.

**Local steps**

- Return x.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L189)

<a id="op-15a81fc0b1348b"></a>
### Set root as default parent

`operation_enterprise_binding_enterprise_setup_utils_set_root_as_default_parent`

**Inputs** doc.

**Explicit results** no value.

**Local steps**

- If doc.get(doc.nsm\_parent\_field).
  - Return no value.
- Set root from get\_root\_of(doc.doctype).
- If root differs from doc.name.
  - Evaluate doc.set(doc.nsm\_parent\_field, root).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L133) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L693) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L190)

## Record · Vehicle

[Record definition](../../../../data/record-types/vehicle.json)

<a id="op-210825abaf0965"></a>
### Vehicle.validate

`operation_enterprise_setup_record_definitions_vehicle_business_behavior_vehicle_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Insurance Start date should be less than Insurance End date” · validation helper — translated “Last carbon check date cannot be a future date”.

**Local steps**

- If (self.start\_date and self.end\_date and getdate(self.start\_date) &gt; getdate(self.end\_date)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.start\_date → self.end\_date → getdate(self.start\_date) &gt; getdate(self.end\_date).
  - Call the validation error handler Platform.throw(translated “Insurance Start date should be less than Insurance End date”).
- If getdate(self.carbon\_check\_date) &gt; getdate().
  - Call the validation error handler Platform.throw(translated “Last carbon check date cannot be a future date”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L21) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1083) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L625)

<a id="op-80d12ccf38f9ef"></a>
### Get data

`operation_enterprise_setup_record_definitions_vehicle_vehicle_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via exists.

**State and service calls** call insert on transactions.

**Explicit results** mapping(“fieldname” → “license\_plate”, “non\_standard\_fieldnames” → mapping(“Delivery Trip” → “vehicle”), “transactions” → transactions).

**Local steps**

- Set transactions from list(mapping(“items” → list(“Delivery Trip”))).
- If Platform.db.exists(“DocType”, “Vehicle Log”, cache = true).
  - Evaluate transactions.insert(0, mapping(“items” → list(“Vehicle Log”))).
- Return mapping(“fieldname” → “license\_plate”, “non\_standard\_fieldnames” → mapping(“Delivery Trip” → “vehicle”), “transactions” → transactions).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L22) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1086) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L628)
