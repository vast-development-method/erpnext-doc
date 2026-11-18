# Forms, reports and navigation · operations 31

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Full text search

<a id="op-3ef28939fb7313"></a>
### Full Text Search.build

`operation_foundation_search_full_text_search_business_behavior_full_text_search_build`

**Inputs** self.

**Local steps**

- Set self.documents from self.get\_items\_to\_index().
- Evaluate self.build\_index().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get items to index](operations-030.md#op-1e9878cf310b6f), [build index](operations-031.md#op-ef6f7734a8d947).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3076) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1757) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L434)

<a id="op-31850d8d61d5b1"></a>
### Full Text Search.update index by name

`operation_foundation_search_full_text_search_business_behavior_full_text_search_update_index_by_name`

**Inputs** self, doc\_name.

**Local steps**

- Set document from self.get\_document\_to\_index(doc\_name).
- If document.
  - Evaluate self.update\_index(document).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get document to index](operations-030.md#op-e9e50b757039fa), [update index](operations-031.md#op-e1029a10e63352).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3157) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L447)

<a id="op-145707fdbb2b43"></a>
### Full Text Search.remove document from index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_remove_document_from_index`

**Inputs** self, doc\_name.

**Explicit results** no value.

**Local steps**

- If not doc\_name.
  - Return no value.
- Set ix from self.get\_index().
- Within ix.searcher().
  - Set writer from AsyncWriter(ix).
  - Evaluate writer.delete\_by\_term(self.id, doc\_name).
  - Evaluate writer.commit(optimize = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get index](operations-031.md#op-97be55f0f58cac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3261) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1767) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L444)

<a id="op-e1029a10e63352"></a>
### Full Text Search.update index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_update_index`

**Inputs** self, document.

**Local steps**

- Set ix from self.get\_index().
- Within ix.searcher().
  - Set writer from AsyncWriter(ix).
  - Evaluate writer.delete\_by\_term(self.id, document at self.id).
  - Evaluate writer.add\_document(expanded names document).
  - Evaluate writer.commit(optimize = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get index](operations-031.md#op-97be55f0f58cac).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3458) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1769) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L446)

<a id="op-97be55f0f58cac"></a>
### Full Text Search.get index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_get_index`

**Inputs** self.

**Explicit results** open\_dir(self.index\_path) · self.create\_index().

**Local steps**

- Attempt the following.
  - Return open\_dir(self.index\_path).
- On failure (EmptyIndexError).
  - Return self.create\_index().

**Methods declared on this owner** [create index](operations-031.md#op-14c8830b1ceefd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3673) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1763) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L440)

<a id="op-14c8830b1ceefd"></a>
### Full Text Search.create index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_create_index`

**Inputs** self.

**Explicit results** create\_in(self.index\_path, self.schema).

**Local steps**

- Evaluate Platform.create\_folder(self.index\_path).
- Return create\_in(self.index\_path, self.schema).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3768) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1759) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L436)

<a id="op-ef6f7734a8d947"></a>
### Full Text Search.build index

`operation_foundation_search_full_text_search_business_behavior_full_text_search_build_index`

**Inputs** self.

**Local steps**

- Set ix from self.create\_index().
- Set writer from AsyncWriter(ix).
- For each tuple(i, document) in enumerate(self.documents).
  - If document.
    - Evaluate writer.add\_document(expanded names document).
  - Evaluate update\_progress\_bar(“Building Index”, i, len(self.documents)).
- Evaluate writer.commit(optimize = true).

If control reaches the end, it returns no value.

**Methods declared on this owner** [create index](operations-031.md#op-14c8830b1ceefd).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L3857) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1758) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L435)

<a id="op-d757fa7486e8ed"></a>
### Full Text Search.search

`operation_foundation_search_full_text_search_business_behavior_full_text_search_search`

**Inputs** self, text, scope = no value, limit = 20.

**Declared result** list at Platform.\_dict.

**Explicit results** list of self.parse\_result(r) for r drawn from results.

**Local steps**

- Set ix from self.get\_index().
- Set results from no value.
- Set search\_fields from self.get\_fields\_to\_search().
- Set fieldboosts from mapping().
- For each tuple(idx, field) in enumerate(search\_fields, start = 1).
  - Set fieldboosts at field from (1.0 ÷ idx).
- Within ix.searcher() bound as searcher.
  - Set parser from MultifieldParser(search\_fields, ix.schema, termclass = FuzzyTermExtended, fieldboosts = fieldboosts).
  - Evaluate parser.remove\_plugin\_class(FieldsPlugin).
  - Evaluate parser.remove\_plugin\_class(WildcardPlugin).
  - Set query from parser.parse(text).
  - Set filter\_scoped from no value.
  - If scope.
    - Set filter\_scoped from Prefix(self.id, scope).
  - Set results from searcher.search(query, limit = limit, filter = filter\_scoped).
  - Return list of self.parse\_result(r) for r drawn from results.
    - Draw r from results.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get index](operations-031.md#op-97be55f0f58cac), [get fields to search](operations-030.md#op-ffe770a42efb49).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L4090) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1768) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L445)

<a id="op-8c315edeba7d13"></a>
### Fuzzy Term Extended.initialize

`operation_foundation_search_full_text_search_business_behavior_fuzzy_term_extended_initialize`

**Inputs** self, fieldname, text, boost = 1.0, maxdist = 2, prefixlength = 1, constantscore = true.

**Local steps**

- Evaluate super().\_\_init\_\_(fieldname, text, boost = boost, maxdist = maxdist, prefixlength = prefixlength, constantscore = constantscore).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L4635) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L448)

<a id="op-a7caf72f22d382"></a>
### Get index path

`operation_foundation_search_full_text_search_business_behavior_get_index_path`

**Inputs** index\_name.

**Explicit results** Platform.get\_site\_path(“indexes”, index\_name).

**Local steps**

- Return Platform.get\_site\_path(“indexes”, index\_name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0327.json#L4795) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L449)

## Service · Gantt

<a id="op-94eb5e0d7babe7"></a>
### Update task

`operation_foundation_desk_gantt_business_behavior_update_task`

**Inputs** args, field\_map.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** resolve a document from args.doctype via get\_doc.

**State and service calls** call save on d.

**Local steps**

- Set args from Platform.\_dict(json.loads(args)).
- Set field\_map from Platform.\_dict(json.loads(field\_map)).
- Set d from Platform.get\_doc(args.doctype, args.name).
- Evaluate d.set(field\_map.start, args.start).
- Evaluate d.set(field\_map.end, args.end).
- Evaluate d.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0013.json#L75) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L1810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L290)

## Record · Global search settings

[Record definition](../../../../data/record-types/global_search_settings.json)

<a id="op-d0e7369e3a6f5c"></a>
### Global Search Settings.validate

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_global_search_settings_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Core Modules {0} cannot be searched in Global Search.”.format(core\_dts) · validation helper — translated “Document Type {0} has been repeated.”.format(repeated\_dts).

**Local steps**

- Set tuple(dts, core\_dts, repeated\_dts) from tuple(list(), list(), list()).
- For each dt in self.allowed\_in\_global\_search.
  - If dt.document\_type belongs to dts.
    - Evaluate repeated\_dts.append(dt.document\_type).
  - If Platform.get\_meta(dt.document\_type).module equals “Core”.
    - Evaluate core\_dts.append(dt.document\_type).
  - Evaluate dts.append(dt.document\_type).
- If core\_dts.
  - Set core\_dts from “, ”.join(generator of Platform.bold(dt) for dt drawn from core\_dts).
    - Draw dt from core\_dts.
  - Call the validation error handler Platform.throw(translated “Core Modules {0} cannot be searched in Global Search.”.format(core\_dts)).
- If repeated\_dts.
  - Set repeated\_dts from “, ”.join(list of Platform.bold(dt) for dt drawn from repeated\_dts).
    - Draw dt from repeated\_dts.
  - Call the validation error handler Platform.throw(translated “Document Type {0} has been repeated.”.format(repeated\_dts)).
- Evaluate Platform.cache.hdel(“global\_search”, “search\_priorities”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L3369) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L332) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L790)

<a id="op-9b2155b87fafc0"></a>
### Get doctypes for global search

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_get_record_types_for_global_search`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.hget(“global\_search”, “search\_priorities”, get\_from\_db).

**Local steps**

- Bind local operation get\_from\_db for subsequent calls.
- Return Platform.cache.hget(“global\_search”, “search\_priorities”, get\_from\_db).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L3898) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L330) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L788)

<a id="op-d70ae3acf67755"></a>
### Get doctypes for global search.get from db

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_get_record_types_for_global_search_get_from_database`

**Inputs** no declared parameters.

**Record and data access** read “Global Search DocType” via get\_all.

**Explicit results** (list of d.document\_type for d drawn from doctypes or list()).

**Local steps**

- Set doctypes from Platform.get\_all(“Global Search DocType”, fields = list(“document\_type”), order\_by = “idx ASC”).
- Return (list of d.document\_type for d drawn from doctypes or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of d.document\_type for d drawn from doctypes → list().
  - Draw d from doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L4070) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L331) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L789)

<a id="op-a57f846a04dc59"></a>
### Reset global search settings doctypes

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_reset_global_search_settings_record_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Local steps**

- Evaluate Platform.has\_permission(“Global Search Settings”, “write”, throw = true).
- Evaluate update\_global\_search\_doctypes().

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(“Global Search Settings”, “write”, throw = true).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L3) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L333) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L791)

<a id="op-e1f38623c841de"></a>
### Update global search doctypes

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_update_global_search_record_types`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all · read “Global Search Settings” via get\_single.

**State and service calls** call insert on allowed\_in\_global\_search · call save on global\_search\_settings.

**Local steps**

- Set global\_search\_doctypes from list().
- Evaluate show\_message(1, translated “Fetching default Global Search documents.”).
- Set installed\_apps from list of app for app drawn from Platform.get\_installed\_apps() where app.
  - Draw app from Platform.get\_installed\_apps(), keep a combination only if (app).
- Set active\_domains from list of domain for domain drawn from Platform.get\_active\_domains() where domain.
  - Draw domain from Platform.get\_active\_domains(), keep a combination only if (domain).
- Evaluate active\_domains.append(“Default”).
- For each app in installed\_apps.
  - Set search\_doctypes from Platform.get\_hooks(hook = “global\_search\_doctypes”, app\_name = app).
  - If not search\_doctypes.
    - Continue with the next iteration or loop test.
  - For each domain in active\_domains.
    - If search\_doctypes.get(domain).
      - Evaluate global\_search\_doctypes.extend(search\_doctypes.get(domain)).
- Set doctype\_list from set of dt.name for dt drawn from Platform.get\_all(“DocType”).
  - Draw dt from Platform.get\_all(“DocType”).
- Set allowed\_in\_global\_search from list().
- For each dt in global\_search\_doctypes.
  - If dt.get(“index”) is distinct from no value.
    - Evaluate allowed\_in\_global\_search.insert(dt.get(“index”), dt.get(“doctype”)).
    - Continue with the next iteration or loop test.
  - Evaluate allowed\_in\_global\_search.append(dt.get(“doctype”)).
- Evaluate show\_message(2, translated “Setting up Global Search documents.”).
- Set global\_search\_settings from Platform.get\_single(“Global Search Settings”).
- Set global\_search\_settings.allowed\_in\_global\_search from list().
- For each dt in allowed\_in\_global\_search.
  - If dt does not belong to doctype\_list.
    - Continue with the next iteration or loop test.
  - Evaluate global\_search\_settings.append(“allowed\_in\_global\_search”, mapping(“document\_type” → dt)).
- Evaluate global\_search\_settings.save(ignore\_permissions = true).
- Evaluate show\_message(3, “Global Search Documents have been reset.”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook = “global\_search\_doctypes”, app\_name = app).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L5) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L337) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L795)

<a id="op-868e3ffd74171d"></a>
### Show message

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_show_message`

**Inputs** progress, msg.

**State and service calls** publish realtime with “global\_search\_settings”.

**Local steps**

- Evaluate Platform.publish\_realtime(“global\_search\_settings”, mapping(“progress” → progress, “total” → 3, “msg” → msg), user = Platform.session.user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(“global\_search\_settings”, mapping(“progress” → progress, “total” → 3, “msg” → msg), user = Platform.session.user).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L5079) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L335) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L793)

<a id="op-953d1410e1e6a7"></a>
### Eligible global search docfields

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_eligible_global_search_record_fields`

**Inputs** meta.

**Local steps**

- For each df in sorted(meta.fields, key = deferred anonymous expression).
  - If df.fieldtype belongs to NO\_VALUE\_FIELDS.
    - Continue with the next iteration or loop test.
  - If getattr(df, “hidden”, false).
    - Continue with the next iteration or loop test.
  - If getattr(df, “is\_virtual”, false).
    - Continue with the next iteration or loop test.
  - yield df.

On ordinary fall-through the sequence ends.

**Values supplied outside this operation** selected callable from getattr(df, “hidden”, false), getattr(df, “is\_virtual”, false).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L5206) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L328) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L786)

<a id="op-cd417f43cfe639"></a>
### Get global search field options

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_get_global_search_field_options`

**Inputs** doctype = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** options.

**Explicit failure paths** validation helper — translated “Document Type is required”.

**Local steps**

- If not doctype.
  - Call the validation error handler Platform.throw(translated “Document Type is required”).
- Evaluate Platform.only\_for(“System Manager”).
- Set meta from Platform.get\_meta(doctype).
- Set options from list(mapping(“label” → translated “Document Name (ID)”, “value” → “name”, “checked” → bool(getattr(meta, “show\_name\_in\_global\_search”, false)))).
- For each df in \_eligible\_global\_search\_docfields(meta).
  - Evaluate options.append(mapping(“label” → \_(df.label, context = df.parent), “value” → df.fieldname, “checked” → bool(df.in\_global\_search))).
- Return options.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · selected callable from getattr(meta, “show\_name\_in\_global\_search”, false).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L5420) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L329) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L787)

<a id="op-210b761092d79b"></a>
### Customize form stub

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_customize_form_stub`

**Inputs** doctype.

**Declared result** CustomizeForm.

**State and service calls** request new\_doc for “Customize Form”.

**Explicit results** cf.

**Local steps**

- Set cf from Platform.new\_doc(“Customize Form”).
- Set cf.doc\_type from doctype.
- Return cf.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L5866) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L327) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L785)

<a id="op-a7c6fbcc373026"></a>
### Set global search property setter

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_set_global_search_property_setter`

**Inputs** cf, fieldname, enabled.

**Declared result** no value.

**Local steps**

- Set val from 1 when enabled, otherwise 0.
  - Value choice on enabled — true gives 1, false gives 0.
- If fieldname equals “name”.
  - Evaluate cf.make\_property\_setter(“show\_name\_in\_global\_search”, val, “Check”).
- Otherwise.
  - Evaluate cf.make\_property\_setter(“in\_global\_search”, val, “Check”, fieldname = fieldname).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0173.json#L5962) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L334) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L792)

<a id="op-a4838ba4af739d"></a>
### Update global search fields

`operation_foundation_desk_record_definitions_global_search_settings_business_behavior_update_global_search_fields`

**Inputs** doctype, fields.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** enqueue with “Platform.utils.global\_search.rebuild\_for\_doctype”.

**Explicit results** mapping(“success” → true).

**Explicit failure paths** validation helper — translated “Document Type is required” · validation helper — translated “Cannot configure Core DocTypes for Global Search.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If not doctype.
  - Call the validation error handler Platform.throw(translated “Document Type is required”).
- If Platform.get\_meta(doctype).module equals “Core”.
  - Call the validation error handler Platform.throw(translated “Cannot configure Core DocTypes for Global Search.”).
- Set fields from Platform.parse\_json(fields).
- Set meta from Platform.get\_meta(doctype).
- Set current from set of df.fieldname for df drawn from \_eligible\_global\_search\_docfields(meta) where df.in\_global\_search.
  - Draw df from \_eligible\_global\_search\_docfields(meta), keep a combination only if (df.in\_global\_search).
- If bool(getattr(meta, “show\_name\_in\_global\_search”, false)).
  - Evaluate current.add(“name”).
- Set desired from set(fields).
- Set cf from \_customize\_form\_stub(doctype).
- For each fieldname in (desired − current).
  - Evaluate \_set\_global\_search\_property\_setter(cf, fieldname, true).
- For each fieldname in (current − desired).
  - Evaluate \_set\_global\_search\_property\_setter(cf, fieldname, false).
- Evaluate Platform.clear\_cache(doctype = doctype).
- Evaluate Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = doctype, enqueue\_after\_commit = true).
- Return mapping(“success” → true).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · selected callable from getattr(meta, “show\_name\_in\_global\_search”, false) · service or queued work from Platform.enqueue(“Platform.utils.global\_search.rebuild\_for\_doctype”, doctype = doctype, enqueue\_after\_commit = true).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0014.json#L4) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L336) · [Declaration location](../../../current-decisions/foundation/evidence/locations-004.tsv#L794)

## Service · Grid import

<a id="op-e55221d272c89c"></a>
### Download template

`operation_foundation_binding_foundation_desk_form_grid_import_download_template`

**Inputs** doctype, title, data, file\_type = “Excel”, docname = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Explicit failure paths** validation helper — translated “Invalid template data” · validation helper — translated “Cannot download more than {0} rows.”.format(MAX\_TEMPLATE\_ROWS) · validation helper — translated “{0} is not a supported file type”.format(file\_type).

**Local steps**

- Evaluate check\_permission(doctype, “read”, docname).
- Set rows from Platform.parse\_json(data).
- If not isinstance(rows, list).
  - Call the validation error handler Platform.throw(translated “Invalid template data”, title = translated “Download Failed”).
- If (len(rows) − 1) &gt; MAX\_TEMPLATE\_ROWS.
  - Call the validation error handler Platform.throw(translated “Cannot download more than {0} rows.”.format(MAX\_TEMPLATE\_ROWS), title = translated “Download Failed”).
- If file\_type does not belong to tuple(“Excel”, “CSV”).
  - Call the validation error handler Platform.throw(translated “{0} is not a supported file type”.format(file\_type), title = translated “Download Failed”).
- Set rows from list of row when isinstance(row, list), otherwise list(row) for row drawn from rows.
  - Draw row from rows.
  - Value choice on isinstance(row, list) — true gives row, false gives list(row).
- If file\_type equals “CSV”.
  - Evaluate build\_csv\_response(rows, title).
- Otherwise.
  - Evaluate build\_xlsx\_response(rows, title).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from check\_permission(doctype, “read”, docname).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L769)

<a id="op-3bcb24afc9b460"></a>
### Parse file

`operation_foundation_binding_foundation_desk_form_grid_import_parse_file`

**Inputs** doctype, filename = no value, dataurl = no value, docname = no value, library\_file\_name = no value.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**Declared result** list at list at str.

**Record and data access** resolve a document from “File” via get\_doc.

**Explicit results** list of list of stringify(value) for value drawn from row for row drawn from (rows or list()).

**Explicit failure paths** validation helper — translated “File must be of type {0}”.format(“, ”.join(generator of formatted text .{e} for e drawn from SUPPORTED\_EXTENSIONS)).

**Local steps**

- Evaluate check\_permission(doctype, “write”, docname).
- Set file\_doc from no value.
- If library\_file\_name.
  - Set file\_doc from Platform.get\_doc(“File”, library\_file\_name).
  - Evaluate file\_doc.check\_permission(“read”).
  - Set filename from (filename or file\_doc.file\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in filename → file\_doc.file\_name.
- Set extension from get\_extension(filename).
- If extension does not belong to SUPPORTED\_EXTENSIONS.
  - Call the validation error handler Platform.throw(translated “File must be of type {0}”.format(“, ”.join(generator of formatted text .{e} for e drawn from SUPPORTED\_EXTENSIONS)), title = translated “Invalid File”).
    - Draw e from SUPPORTED\_EXTENSIONS.
- Set content from file\_doc.get\_content() when file\_doc, otherwise decode\_dataurl(dataurl).
  - Value choice on file\_doc — true gives file\_doc.get\_content(), false gives decode\_dataurl(dataurl).
- If extension equals “csv”.
  - Set rows from read\_csv\_content(content).
- Otherwise.
  - If extension equals “xlsx”.
    - Set rows from read\_xlsx\_file\_from\_attached\_file(fcontent = content, read\_only = true).
  - Otherwise.
    - Set rows from read\_xls\_file\_from\_attached\_file(content).
- Return list of list of stringify(value) for value drawn from row for row drawn from (rows or list()).
  - Draw row from (rows or list()).
  - Draw value from row.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in rows → list().

**Values supplied outside this operation** effective access from check\_permission(doctype, “write”, docname), file\_doc.check\_permission(“read”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0003.json#L56) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L781)
