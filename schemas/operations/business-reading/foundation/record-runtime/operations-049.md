# Record lifecycle and persistence · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Document naming rule

[Record definition](../../../../data/record-types/document_naming_rule.json)

<a id="op-13d632f0ed6a82"></a>
### Document Naming Rule.validate

`operation_foundation_core_record_definitions_document_naming_rule_business_behavior_document_naming_rule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_fields\_in\_conditions().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate fields in conditions](operations-049.md#op-7fb84c0d1c0c81).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L5691) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1394) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1384)

<a id="op-aa04928d9c48f2"></a>
### Document Naming Rule.clear doctype map

`operation_foundation_core_record_definitions_document_naming_rule_business_behavior_document_naming_rule_clear_record_type_map`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache\_manager.clear\_doctype\_map(self.doctype, self.document\_type).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L5742) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1391) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1381)

<a id="op-5904d64c61e29b"></a>
### Document Naming Rule.on update

`operation_foundation_core_record_definitions_document_naming_rule_business_behavior_document_naming_rule_on_update`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_doctype\_map().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear doctype map](operations-049.md#op-aa04928d9c48f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L5814) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1393) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1383)

<a id="op-7b404bb03237a2"></a>
### Document Naming Rule.on trash

`operation_foundation_core_record_definitions_document_naming_rule_business_behavior_document_naming_rule_on_trash`

**Inputs** self.

**Local steps**

- Evaluate self.clear\_doctype\_map().

If control reaches the end, it returns no value.

**Methods declared on this owner** [clear doctype map](operations-049.md#op-aa04928d9c48f2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L5865) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1392) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1382)

<a id="op-7fb84c0d1c0c81"></a>
### Document Naming Rule.validate fields in conditions

`operation_foundation_core_record_definitions_document_naming_rule_business_behavior_document_naming_rule_validate_fields_in_conditions`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is not a field of doctype {1}”.format(Platform.bold(condition.field), Platform.bold(self.document\_type)).

**Local steps**

- If self.has\_value\_changed(“document\_type”).
  - Set docfields from list of x.fieldname for x drawn from Platform.get\_meta(self.document\_type).fields.
    - Draw x from Platform.get\_meta(self.document\_type).fields.
  - For each condition in self.conditions.
    - If condition.field does not belong to docfields.
      - Call the validation error handler Platform.throw(translated “{0} is not a field of doctype {1}”.format(Platform.bold(condition.field), Platform.bold(self.document\_type))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L5916) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1395) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1385)

<a id="op-14f35d34ad60f7"></a>
### Document Naming Rule.apply

`operation_foundation_core_record_definitions_document_naming_rule_business_behavior_document_naming_rule_apply`

**Inputs** self, doc.

**Record and data access** read self.doctype via get\_value.

**State and service calls** request set\_value on self.doctype.

**Explicit results** no value.

**Local steps**

- If self.conditions.
  - If not evaluate\_filters(doc, list of tuple(self.document\_type, d.field, d.condition, d.value) for d drawn from self.conditions).
    - Draw d from self.conditions.
    - Return no value.
- Set counter from (Platform.db.get\_value(self.doctype, self.name, “counter”, for\_update = true) or 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.db.get\_value(self.doctype, self.name, “counter”, for\_update = true) → 0.
- Set naming\_series from parse\_naming\_series(self.prefix, doc = doc).
- Set doc.name from (naming\_series + (((“%0” + str(self.prefix\_digits)) + “d”) modulo or format (counter + 1))).
- Evaluate Platform.db.set\_value(self.doctype, self.name, “counter”, (counter + 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0073.json#L6185) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1390) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1380)

## Record · Document naming settings

[Record definition](../../../../data/record-types/document_naming_settings.json)

<a id="op-074f957f56312e"></a>
### Document Naming Settings.get transactions and prefixes

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_get_transactions_and_prefixes`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“transactions” → transactions, “prefixes” → prefixes).

**Local steps**

- Set transactions from self.\_get\_transactions().
- Set prefixes from self.\_get\_prefixes(transactions).
- Return mapping(“transactions” → transactions, “prefixes” → prefixes).

**Methods declared on this owner** [get transactions](operations-049.md#op-81d281eba26441), [get prefixes](operations-049.md#op-8b90ec8fc09b2b).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L846) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1398)

<a id="op-81d281eba26441"></a>
### Document Naming Settings.get transactions

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_get_transactions`

**Inputs** self.

**Declared result** list at str.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Explicit results** sorted(readable\_doctypes.intersection((standard + custom))).

**Local steps**

- Set readable\_doctypes from set(get\_doctypes\_with\_read()).
- Set standard from Platform.get\_all(“DocField”, mapping(“fieldname” → “naming\_series”), “parent”, pluck = “parent”).
- Set custom from Platform.get\_all(“Custom Field”, mapping(“fieldname” → “naming\_series”), “dt”, pluck = “dt”).
- Return sorted(readable\_doctypes.intersection((standard + custom))).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L982) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1407) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1397)

<a id="op-8b90ec8fc09b2b"></a>
### Document Naming Settings.get prefixes

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_get_prefixes`

**Inputs** self, doctypes.

**Declared result** list at str.

**Record and data access** read “DocType” via get\_all.

**State and service calls** msgprint with translated “Unable to find DocType {0}”.format(d).

**Explicit results** self.\_evaluate\_and\_clean\_templates(series\_templates).

**Local steps**

- Set series\_templates from set().
- For each d in doctypes.
  - Attempt the following.
    - Set options from Platform.get\_meta(d).get\_naming\_series\_options().
    - Evaluate series\_templates.update(options).
  - On failure (Platform.DoesNotExistError).
    - Evaluate Platform.msgprint(translated “Unable to find DocType {0}”.format(d)).
    - Continue with the next iteration or loop test.
- Set custom\_templates from Platform.get\_all(“DocType”, fields = list(“autoname”), filters = mapping(“name” → tuple(“not in”, doctypes), “autoname” → tuple(“like”, “%.#%”), “module” → tuple(“not in”, list(“Core”)))).
- If custom\_templates.
  - Evaluate series\_templates.update(list of d.autoname.rsplit(“.”, 1) at 0 for d drawn from custom\_templates).
    - Draw d from custom\_templates.
- Return self.\_evaluate\_and\_clean\_templates(series\_templates).

**Methods declared on this owner** [evaluate and clean templates](operations-049.md#op-0a7db40959e365).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L1274) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1406) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1396)

<a id="op-0a7db40959e365"></a>
### Document Naming Settings.evaluate and clean templates

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_evaluate_and_clean_templates`

**Inputs** self, series\_templates.

**Declared result** list at str.

**Explicit results** sorted(evalauted\_prefix).

**Local steps**

- Set evalauted\_prefix from set().
- Set series from Platform.qb.DocType(“Series”).
- Set prefixes\_from\_db from nested operand in the contract.qb.from\_(series).select(series.name).run(pluck = true).
- Evaluate evalauted\_prefix.update(prefixes\_from\_db).
- For each series\_template in series\_templates.
  - Attempt the following.
    - Set prefix from NamingSeries(series\_template).get\_prefix().
    - If “{” belongs to prefix.
      - Continue with the next iteration or loop test.
    - Evaluate evalauted\_prefix.add(prefix).
  - On failure (Exception).
    - Evaluate Platform.clear\_last\_message().
    - Evaluate Platform.log\_error(formatted text Invalid naming series {series\_template}).
- Return sorted(evalauted\_prefix).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L1757) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1391)

<a id="op-24ae0f1b6375b2"></a>
### Document Naming Settings.get options list

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_get_options_list`

**Inputs** self, options.

**Declared result** list at str.

**Explicit results** list of op.strip() for op drawn from options.split(whitespace '\\n') where op.strip().

**Local steps**

- Return list of op.strip() for op drawn from options.split(whitespace '\\n') where op.strip().
  - Draw op from options.split(whitespace '\\n'), keep a combination only if (op.strip()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L2172) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1405) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1395)

<a id="op-49c187624f3790"></a>
### Document Naming Settings.update series

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_update_series`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Series Updated for {}”.format(self.transaction\_type).

**Local steps**

- Evaluate self.validate\_set\_series().
- Evaluate self.check\_duplicate().
- Evaluate self.set\_series\_options\_in\_meta(self.transaction\_type, self.naming\_series\_options).
- Evaluate Platform.msgprint(translated “Series Updated for {}”.format(self.transaction\_type), alert = true, indicator = “green”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate set series](operations-049.md#op-79f84a2270cf59), [check duplicate](operations-049.md#op-85f2bd0e61ccd2), [set series options in meta](operations-049.md#op-2c7f90b46da27c).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L2294) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1403)

<a id="op-79f84a2270cf59"></a>
### Document Naming Settings.validate set series

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_validate_set_series`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Please set the series to be used.”.

**Local steps**

- If (self.transaction\_type and not self.naming\_series\_options).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.transaction\_type → not self.naming\_series\_options.
  - Call the validation error handler Platform.throw(translated “Please set the series to be used.”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L2501) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1406)

<a id="op-2c7f90b46da27c"></a>
### Document Naming Settings.set series options in meta

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_set_series_options_in_meta`

**Inputs** self, doctype, options.

**Declared result** no value.

**Local steps**

- Set options from self.get\_options\_list(options).
- For each series in options.
  - Evaluate self.validate\_series\_name(series).
- If (options and self.user\_must\_always\_select).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in options → self.user\_must\_always\_select.
  - Set options from list(empty text, expanded options).
- Set default from options at 0 when options, otherwise empty text.
  - Value choice on options — true gives options at 0, false gives empty text.
- Set option\_string from whitespace '\\n'.join(options).
- Evaluate self.update\_naming\_series\_property\_setter(doctype, “default”, empty text).
- Evaluate self.update\_naming\_series\_property\_setter(doctype, “options”, option\_string).
- Evaluate self.update\_naming\_series\_property\_setter(doctype, “default”, default).
- Set self.naming\_series\_options from option\_string.
- Evaluate Platform.clear\_cache(doctype = doctype).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get options list](operations-049.md#op-24ae0f1b6375b2), [validate series name](operations-049.md#op-144ba7d6b03606), [update naming series property setter](operations-049.md#op-ed3a67a2c356e8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L2603) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1410) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1400)

<a id="op-ed3a67a2c356e8"></a>
### Document Naming Settings.update naming series property setter

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_update_naming_series_property_setter`

**Inputs** self, doctype, property, value.

**Local steps**

- Bind dependencies make\_property\_setter.
- Evaluate make\_property\_setter(doctype, “naming\_series”, property, value, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L2996) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1402)

<a id="op-85f2bd0e61ccd2"></a>
### Document Naming Settings.check duplicate

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_check_duplicate`

**Inputs** self.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all · resolve a document from “DocType” via get\_doc.

**Explicit failure paths** validation helper — translated “Series {0} already used in {1}”.format(series, existing\_series at series).

**Local steps**

- Bind local operation stripped\_series for subsequent calls.
- Set standard from Platform.get\_all(“DocField”, mapping(“fieldname” → “naming\_series”), “parent”, pluck = “parent”).
- Set custom from Platform.get\_all(“Custom Field”, mapping(“fieldname” → “naming\_series”), “dt”, pluck = “dt”).
- Set all\_doctypes\_with\_naming\_series from set((standard + custom)).
- Evaluate all\_doctypes\_with\_naming\_series.remove(self.transaction\_type).
- Set existing\_series from mapping().
- For each doctype in all\_doctypes\_with\_naming\_series.
  - For each series in Platform.get\_meta(doctype).get\_naming\_series\_options().
    - Set existing\_series at stripped\_series(series) from doctype.
- Set dt from Platform.get\_doc(“DocType”, self.transaction\_type).
- Set options from self.get\_options\_list(self.naming\_series\_options).
- For each series in options.
  - If stripped\_series(series) belongs to existing\_series.
    - Call the validation error handler Platform.throw(translated “Series {0} already used in {1}”.format(series, existing\_series at series)).
  - Evaluate validate\_series(dt, series).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get options list](operations-049.md#op-24ae0f1b6375b2).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L3098) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1388)

<a id="op-ecb440963f8fc9"></a>
### Document Naming Settings.check duplicate.stripped series

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_check_duplicate_stripped_series`

**Inputs** s.

**Declared result** str.

**Explicit results** s.strip().rstrip(“#”).

**Local steps**

- Return s.strip().rstrip(“#”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L3739) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1389)

<a id="op-144ba7d6b03606"></a>
### Document Naming Settings.validate series name

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_validate_series_name`

**Inputs** self, series.

**Local steps**

- Evaluate NamingSeries(series).validate().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L3811) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1405)

<a id="op-39f1c2e6ebbbd5"></a>
### Document Naming Settings.get options

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_get_options`

**Inputs** self, doctype = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** no value · Platform.get\_meta((doctype or self.transaction\_type)).get\_field(“naming\_series”).options.

**Local steps**

- Set doctype from (doctype or self.transaction\_type).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.transaction\_type.
- If not doctype.
  - Return no value.
- If Platform.get\_meta((doctype or self.transaction\_type)).get\_field(“naming\_series”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.transaction\_type.
  - Return Platform.get\_meta((doctype or self.transaction\_type)).get\_field(“naming\_series”).options.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doctype → self.transaction\_type.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L3879) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1404) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1394)

<a id="op-31dc5b5bb288ee"></a>
### Document Naming Settings.get current

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_get_current`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** self.current\_value.

**Local steps**

- If self.prefix is distinct from no value.
  - Set self.current\_value from NamingSeries(self.prefix).get\_current\_value().
- Return self.current\_value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L4120) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1393)

<a id="op-b831ce769dc188"></a>
### Document Naming Settings.update amendment rule

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_update_amendment_rule`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Amended Document Naming Settings” via get\_all.

**State and service calls** call db\_set on self · request delete\_doc for “Amended Document Naming Settings” · call save on row · msgprint with translated “Amendment naming rules updated.”.

**Local steps**

- Evaluate self.db\_set(“default\_amend\_naming”, self.default\_amend\_naming).
- Set existing\_overrides from Platform.db.get\_all(“Amended Document Naming Settings”, filters = mapping(“name” → list(“not in”, list of d.name for d drawn from self.amend\_naming\_override)), pluck = “name”).
  - Draw d from self.amend\_naming\_override.
- For each override in existing\_overrides.
  - Evaluate Platform.delete\_doc(“Amended Document Naming Settings”, override).
- For each row in self.amend\_naming\_override.
  - Evaluate row.save().
- Evaluate Platform.msgprint(translated “Amendment naming rules updated.”, indicator = “green”, alert = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L4250) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1411) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1401)

<a id="op-e20f6d01ab490c"></a>
### Document Naming Settings.update series start

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_update_series_start`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Series counter for {} updated to {} successfully”.format(self.prefix, self.current\_value).

**Explicit failure paths** validation helper — translated “Please select prefix first”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If self.prefix is identical to no value.
  - Call the validation error handler Platform.throw(translated “Please select prefix first”).
- Set naming\_series from NamingSeries(self.prefix).
- Set previous\_value from naming\_series.get\_current\_value().
- Evaluate naming\_series.update\_counter(self.current\_value).
- Evaluate self.create\_version\_log\_for\_change(naming\_series.get\_prefix(), previous\_value, self.current\_value).
- Evaluate Platform.msgprint(translated “Series counter for {} updated to {} successfully”.format(self.prefix, self.current\_value), alert = true, indicator = “green”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create version log for change](operations-049.md#op-bf6391b0741a8c).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L4598) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1404)

<a id="op-bf6391b0741a8c"></a>
### Document Naming Settings.create version log for change

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_create_version_log_for_change`

**Inputs** self, series, old, new.

**State and service calls** request new\_doc for “Version” · call insert on version.

**Local steps**

- Set version from Platform.new\_doc(“Version”).
- Set version.ref\_doctype from “Series”.
- Set version.docname from (series or “.#”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in series → “.#”.
- Set version.data from Platform.as\_json(mapping(“changed” → list(list(“current”, old, new)))).
- Set version.flags.ignore\_links from true.
- Set version.flags.ignore\_permissions from true.
- Evaluate version.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L4952) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1390)

<a id="op-bed115f87bf400"></a>
### Document Naming Settings.preview series

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_preview_series`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** str.

**Explicit results** empty text · whitespace '\\n'.join(NamingSeries(series).get\_preview(doc = doc)) · (translated “Failed to generate names from the series” + formatted text  {e}).

**Local steps**

- Set series from self.try\_naming\_series.
- If not series.
  - Return empty text.
- Attempt the following.
  - Set doc from self.\_fetch\_last\_doc\_if\_available().
  - Return whitespace '\\n'.join(NamingSeries(series).get\_preview(doc = doc)).
- On failure (Exception) bound to e.
  - Evaluate Platform.clear\_last\_message().
  - Return (translated “Failed to generate names from the series” + formatted text  {e}).

**Methods declared on this owner** [fetch last doc if available](operations-050.md#op-49216643529ee2).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L5213) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1399)
