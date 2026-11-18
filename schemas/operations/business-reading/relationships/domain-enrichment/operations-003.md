# Company enrichment · operations 3

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Crm enrichment rule

<a id="op-afe963a9291a76"></a>
### CRMEnrichment Rule.validate duplicate

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_crmenrichmentrule_validate_duplicate`

**Inputs** self.

**Explicit failure paths** validation helper with Platform.DuplicateEntryError — translated “A {0} rule for {1} already exists”.format(translated self.rule\_type, self.get\_target()).

**Local steps**

- If find\_duplicate(self.rule\_type, self.get\_target(), exclude = self.name).
  - Call the validation error handler Platform.throw(translated “A {0} rule for {1} already exists”.format(translated self.rule\_type, self.get\_target()), Platform.DuplicateEntryError).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get target](operations-002.md#op-57080ed949e9f4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L167) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L323) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L304)

<a id="op-4fcc6a7287516f"></a>
### CRMEnrichment Rule.validate patterns

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_crmenrichmentrule_validate_patterns`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Row #{0}: Not a valid regular expression: {1}”.format(row.idx, str(e)).

**Local steps**

- For each row in self.patterns.
  - If not row.is\_regex.
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Evaluate re.compile(row.pattern, re.IGNORECASE).
  - On failure (re.error) bound to e.
    - Call the validation error handler Platform.throw(translated “Row #{0}: Not a valid regular expression: {1}”.format(row.idx, str(e))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L168) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L324) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L305)

## Record · Crm enrichment run

<a id="op-6f8c4a2ba2f3d4"></a>
### CRMEnrichment Run.undo

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_run_crm_enrichment_run_crmenrichmentrun_undo`

**Inputs** self.

**Declared result** dict.

**Record and data access** read self.doctype via get\_value · resolve a document from self.reference\_doctype via get\_doc.

**State and service calls** call save on record · call db\_set on self.

**Explicit results** mapping(“reverted” → reverted, “skipped” → skipped).

**Explicit failure paths** validation helper with Platform.ValidationError — translated “Only a completed enrichment run can be undone.” · validation helper with Platform.ValidationError — translated “This enrichment run did not change any fields.”.

**Local steps**

- Set status from Platform.db.get\_value(self.doctype, self.name, “status”, for\_update = true).
- If status differs from “Completed”.
  - Call the validation error handler Platform.throw(translated “Only a completed enrichment run can be undone.”, Platform.ValidationError).
- If not self.changes.
  - Call the validation error handler Platform.throw(translated “This enrichment run did not change any fields.”, Platform.ValidationError).
- Set record from Platform.get\_doc(self.reference\_doctype, self.reference\_name).
- Set tuple(reverted, skipped) from tuple(list(), list()).
- For each change in self.changes.
  - Set df from record.meta.get\_field(change.fieldname).
  - If (not df or cstr(record.get(change.fieldname)) differs from cstr(restore\_value(df, change.new\_value))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → cstr(record.get(change.fieldname)) differs from cstr(restore\_value(df, change.new\_value)).
    - Evaluate skipped.append(change.fieldname).
    - Continue with the next iteration or loop test.
  - Evaluate record.set(change.fieldname, restore\_value(df, change.old\_value)).
  - Evaluate reverted.append(change.fieldname).
- If reverted.
  - Evaluate record.save().
- Evaluate self.db\_set(mapping(“status” → “Reverted”, “undone\_on” → now\_datetime(), “undone\_by” → Platform.session.user)).
- Return mapping(“reverted” → reverted, “skipped” → skipped).

**Values supplied outside this operation** clock or generated value from now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L172) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L328) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L309)

<a id="op-1750c563532bce"></a>
### Restore value

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_run_crm_enrichment_run_restore_value`

**Inputs** df, value.

**Explicit results** no value · cast(df.fieldtype, value).

**Local steps**

- If (value is identical to no value or value equals empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in value is identical to no value → value equals empty text.
  - Return no value.
- Return cast(df.fieldtype, value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L175) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L331) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L312)

<a id="op-b7d426feac2fde"></a>
### Get permission query conditions

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_run_crm_enrichment_run_get_permission_query_conditions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** user.

**Explicit result forms** a scalar literal, the result of a delegated call.

**Local structure** 3 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L173) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L329) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L310)

<a id="op-27305292b8108b"></a>
### Has permission

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_run_crm_enrichment_run_has_permission`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** doc, ptype, user.

**Explicit result forms** Boolean true, the result of a delegated call.

**Observed service boundaries** effective access lookup.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L174) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L330) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L311)

<a id="op-73af7ef0e4663f"></a>
### Shared with

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_run_crm_enrichment_run_shared_with`

**Inputs** user, doctype, Run.

**Explicit results** Run.reference\_name.isin(nested operand in the contract.from\_(Share).select(Share.share\_name).where(((Share.share\_doctype equals doctype bitwise and Share.read equals 1) bitwise and (Share.user equals user  ….

**Local steps**

- Set Share from Platform.qb.DocType(“DocShare”).
- Return Run.reference\_name.isin(nested operand in the contract.from\_(Share).select(Share.share\_name).where(((Share.share\_doctype equals doctype bitwise and Share.read equals 1) bitwise and (Share.user equals user  ….

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L176) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L332) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L313)

## Record · Crm enrichment settings

<a id="op-1b068e271227e7"></a>
### CRMEnrichment Settings.validate

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_settings_crm_enrichment_settings_crmenrichmentsettings_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_max\_pages().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate max pages](operations-003.md#op-b73f56563c45bb).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L177) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L333) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L314)

<a id="op-b73f56563c45bb"></a>
### CRMEnrichment Settings.validate max pages

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_settings_crm_enrichment_settings_crmenrichmentsettings_validate_max_pages`

**Inputs** self.

**Explicit results** no value.

**Explicit failure paths** validation helper — translated “Maximum pages must be a whole number between 1 and {0}”.format(MAX\_PAGES\_LIMIT).

**Local steps**

- If self.max\_pages belongs to tuple(no value, empty text).
  - Return no value.
- If (int(self.max\_pages) &lt; 1 or int(self.max\_pages) &gt; MAX\_PAGES\_LIMIT).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in int(self.max\_pages) &lt; 1 → int(self.max\_pages) &gt; MAX\_PAGES\_LIMIT.
  - Call the validation error handler Platform.throw(translated “Maximum pages must be a whole number between 1 and {0}”.format(MAX\_PAGES\_LIMIT), title = translated “Invalid maximum pages”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L178) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L334) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L315)

## Service · Cross record

<a id="op-5b42ed9191c05f"></a>
### Is org enriched

`operation_relationships_domain_enrichment_cross_record_business_behavior_is_organization_enriched`

**Inputs** org.

**Declared result** bool.

**Record and data access** read “CRM Enrichment Run” via exists.

**Explicit results** true · any(generator of org.get(fieldname) for fieldname drawn from \_ORG\_ENRICHED\_FIELDS).

**Local steps**

- If Platform.db.exists(“CRM Enrichment Run”, mapping(“reference\_doctype” → “CRM Organization”, “reference\_name” → org.name, “status” → “Completed”)).
  - Return true.
- Return any(generator of org.get(fieldname) for fieldname drawn from \_ORG\_ENRICHED\_FIELDS).
  - Draw fieldname from \_ORG\_ENRICHED\_FIELDS.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L1991) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L453) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L434)

<a id="op-60b1f102416610"></a>
### Result from organization

`operation_relationships_domain_enrichment_cross_record_business_behavior_result_from_organization`

**Inputs** org.

**Declared result** EnrichmentResult.

**Explicit results** result.

**Local steps**

- Set result from EnrichmentResult(website = (org.get(“website”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in org.get(“website”) → empty text.
- Set result.company\_name from Field(value = (org.get(“organization\_name”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in org.get(“organization\_name”) → empty text.
- Set result.description from Field(value = (org.get(“company\_description”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in org.get(“company\_description”) → empty text.
- Set result.logo from Field(value = (org.get(“organization\_logo”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in org.get(“organization\_logo”) → empty text.
- Set result.industry from Field(value = (org.get(“industry”) or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in org.get(“industry”) → empty text.
- For each network in tuple(“linkedin”, “twitter”, “facebook”).
  - Set value from org.get(network).
  - If value.
    - Set result.social\_profiles at network from SocialProfile(value = value).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L2183) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L454) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L435)

<a id="op-56975dd710225c"></a>
### Copy enrichment from organization

`operation_relationships_domain_enrichment_cross_record_business_behavior_copy_enrichment_from_organization`

**Inputs** target\_doc.

**Declared result** list at str.

**Record and data access** read “CRM Organization” via exists · resolve a document from “CRM Organization” via get\_cached\_doc.

**Explicit results** list() · mapper.filled\_labels(mapper.apply\_to\_document(target\_doc, result, cfg, fill\_empty\_only = true)).

**Local steps**

- Attempt the following.
  - Set org\_name from target\_doc.get(“organization”).
  - If (not org\_name or not Platform.db.exists(“CRM Organization”, org\_name)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not org\_name → not Platform.db.exists(“CRM Organization”, org\_name).
    - Return list().
  - Set org from Platform.get\_cached\_doc(“CRM Organization”, org\_name).
  - If not \_is\_org\_enriched(org).
    - Return list().
  - Set cfg from get\_config().
  - Set result from \_result\_from\_organization(org).
  - Return mapper.filled\_labels(mapper.apply\_to\_document(target\_doc, result, cfg, fill\_empty\_only = true)).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Domain Enrichment: Org -&gt; Lead/Deal copy failed”, message = formatted text {target\_doc.doctype} {target\_doc.name}: {Platform.get\_traceback()}).
  - Return list().

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“CRM Organization”, org\_name).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L3) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L452) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L433)

## Service · Extractors

<a id="op-d9528a4e8eabf7"></a>
### Apply keyword rules

`operation_relationships_domain_enrichment_extractors_business_behavior_apply_keyword_rules`

**Inputs** text\_by\_scope, rules.

**Declared result** dict.

**Explicit results** scores.

**Local steps**

- Set scores from mapping().
- For each rule in rules.
  - Set text from text\_by\_scope.get(rule.match\_scope, empty text).
  - Set hits from rule.matches(text).
  - If hits.
    - Set scores at rule.label from (scores.get(rule.label, 0.0) + (hits × (rule.weight or 1.0))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in rule.weight → 1.0.
- Return scores.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L3341) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L455) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L436)

<a id="op-f40cd1440ff212"></a>
### Parse json ld

`operation_relationships_domain_enrichment_extractors_business_behavior_parse_structured_data_ld`

**Inputs** soup.

**Explicit results** blocks.

**Local steps**

- Set blocks from list().
- For each tag in soup.find\_all(“script”, attrs = mapping(“type” → “application/ld+json”)).
  - Set raw from (tag.string or tag.get\_text() or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tag.string → tag.get\_text() → empty text.
  - If not raw.strip().
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set data from json.loads(raw).
  - On failure (tuple(ValueError, TypeError)).
    - Continue with the next iteration or loop test.
  - If isinstance(data, dict).
    - If (“@graph” belongs to data and isinstance(data at “@graph”, list)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in “@graph” belongs to data → isinstance(data at “@graph”, list).
      - Evaluate blocks.extend(list of d for d drawn from data at “@graph” where isinstance(d, dict)).
        - Draw d from data at “@graph”, keep a combination only if (isinstance(d, dict)).
    - Otherwise.
      - Evaluate blocks.append(data).
  - Otherwise.
    - If isinstance(data, list).
      - Evaluate blocks.extend(list of d for d drawn from data where isinstance(d, dict)).
        - Draw d from data, keep a combination only if (isinstance(d, dict)).
- Return blocks.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L3580) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L480) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L461)

<a id="op-a97ba4e86afec6"></a>
### Ld type matches

`operation_relationships_domain_enrichment_extractors_business_behavior_ld_type_matches`

**Inputs** block, wanted.

**Explicit results** any(generator of str(x).lower() belongs to wanted for x drawn from types).

**Local steps**

- Set t from block.get(“@type”, empty text).
- Set types from t when isinstance(t, list), otherwise list(t).
  - Value choice on isinstance(t, list) — true gives t, false gives list(t).
- Return any(generator of str(x).lower() belongs to wanted for x drawn from types).
  - Draw x from types.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L4083) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L477) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L458)

<a id="op-b162a1de9edb9b"></a>
### Diagnose readability

`operation_relationships_domain_enrichment_extractors_business_behavior_diagnose_readability`

**Inputs** pages.

**Explicit results** “unreachable” · “blocked” · “empty” · empty text.

**Local steps**

- If not pages.
  - Return “unreachable”.
- Set home from pages at 0.
- If (home.error or not home.status\_code).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in home.error → not home.status\_code.
  - Return “unreachable”.
- If home.status\_code belongs to tuple(401, 403, 429).
  - Return “blocked”.
- If home.status\_code ≥ 500.
  - Return “unreachable”.
- Set blob from (home.html or empty text) at slice no value to 5000.lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in home.html → empty text.
- Set text\_len from len((home.text or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in home.text → empty text.
- If any(generator of marker belongs to blob for marker drawn from WAF\_MARKERS\_STRONG).
  - Draw marker from WAF\_MARKERS\_STRONG.
  - Return “blocked”.
- If (text\_len &lt; WAF\_WEAK\_TEXT\_THRESHOLD and any(generator of marker belongs to blob for marker drawn from WAF\_MARKERS\_WEAK)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in text\_len &lt; WAF\_WEAK\_TEXT\_THRESHOLD → any(generator of marker belongs to blob for marker drawn from WAF\_MARKERS\_WEAK).
  - Draw marker from WAF\_MARKERS\_WEAK.
  - Return “blocked”.
- If text\_len &lt; 200.
  - Return “empty”.
- Return empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L4271) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L464) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L445)

<a id="op-6ae06457b2ec39"></a>
### Meta with method

`operation_relationships_domain_enrichment_extractors_business_behavior_meta_with_method`

**Inputs** soup, remaining positional values names.

**Explicit results** tuple(tag at “content”.strip(), name) · tuple(empty text, empty text).

**Local steps**

- For each name in names.
  - Set tag from (soup.find(“meta”, attrs = mapping(“property” → name)) or soup.find(“meta”, attrs = mapping(“name” → name))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in soup.find(“meta”, attrs = mapping(“property” → name)) → soup.find(“meta”, attrs = mapping(“name” → name)).
  - If (tag and tag.get(“content”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in tag → tag.get(“content”).
    - Return tuple(tag at “content”.strip(), name).
- Return tuple(empty text, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L4731) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L479) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L460)

<a id="op-287a304137deb7"></a>
### Is description copy

`operation_relationships_domain_enrichment_extractors_business_behavior_is_description_copy`

**Inputs** content.

**Explicit results** false · (one space belongs to content or not content.isascii()).

**Local steps**

- If len(content) &lt; \_MIN\_META\_DESC\_LEN.
  - Return false.
- Return (one space belongs to content or not content.isascii()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in one space belongs to content → not content.isascii().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L4986) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L474) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L455)

<a id="op-72ac7fc0d1397c"></a>
### Meta description

`operation_relationships_domain_enrichment_extractors_business_behavior_meta_description`

**Inputs** soup.

**Explicit results** content · fallback.

**Local steps**

- Set fallback from empty text.
- For each name in tuple(“og:description”, “description”).
  - Set tuple(content, \_name) from \_meta\_with\_method(soup, name).
  - If not content.
    - Continue with the next iteration or loop test.
  - If \_is\_description\_copy(content).
    - Return content.
  - Set fallback from (fallback or content).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in fallback → content.
- Return fallback.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L5102) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L478) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L459)

<a id="op-7e8b86945c6532"></a>
### Domain brand

`operation_relationships_domain_enrichment_extractors_business_behavior_domain_brand`

**Inputs** url.

**Explicit results** labels at negative 2 when len(labels) ≥ 2, otherwise labels at 0 when labels, otherwise empty text.

**Local steps**

- Set netloc from (nested operand in the contract.netloc or empty text).lower().split(“:”) at 0.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in urlparse((url or empty text)).netloc → empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in url → empty text.
- If netloc.startswith(“www.”).
  - Set netloc from netloc at slice 4 to no value.
- Set labels from list of label for label drawn from netloc.split(“.”) where label.
  - Draw label from netloc.split(“.”), keep a combination only if (label).
- Return labels at negative 2 when len(labels) ≥ 2, otherwise labels at 0 when labels, otherwise empty text.
  - Value choice on len(labels) ≥ 2 — true gives labels at negative 2, false gives labels at 0 when labels, otherwise empty text.
  - Value choice on labels — true gives labels at 0, false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L5293) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L465) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L446)

<a id="op-c5b87ee95f7319"></a>
### Compact

`operation_relationships_domain_enrichment_extractors_business_behavior_compact`

**Inputs** text.

**Explicit results** re.sub(“&#91;^a-z0-9&#93;”, empty text, (text or empty text).lower()).

**Local steps**

- Return re.sub(“&#91;^a-z0-9&#93;”, empty text, (text or empty text).lower()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in text → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L5585) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L461) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L442)

<a id="op-b3e4d101518056"></a>
### Clean company name

`operation_relationships_domain_enrichment_extractors_business_behavior_clean_company_name`

**Inputs** raw, site\_url = empty text.

**Explicit results** empty text · (name or raw).

**Local steps**

- Set raw from (raw or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in raw → empty text.
- If not raw.
  - Return empty text.
- Set chunks from list of c.strip() for c drawn from \_NAME\_SPLIT\_RE.split(raw) where c.strip().
  - Draw c from \_NAME\_SPLIT\_RE.split(raw), keep a combination only if (c.strip()).
- Set name from chunks at 0 when chunks, otherwise raw.
  - Value choice on chunks — true gives chunks at 0, false gives raw.
- Set brand from \_compact(\_domain\_brand(site\_url)) when site\_url, otherwise empty text.
  - Value choice on site\_url — true gives \_compact(\_domain\_brand(site\_url)), false gives empty text.
- If (brand and len(chunks) &gt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in brand → len(chunks) &gt; 1.
  - For each chunk in chunks.
    - Set c from \_compact(chunk).
    - If (c and (c equals brand or (len(min(c, brand, key = len)) ≥ 4 and (c belongs to brand or brand belongs to c)))).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in c → (c equals brand or (len(min(c, brand, key = len)) ≥ 4 and (c belongs to brand or brand belongs to c))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in c equals brand → (len(min(c, brand, key = len)) ≥ 4 and (c belongs to brand or brand belongs to c)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(min(c, brand, key = len)) ≥ 4 → (c belongs to brand or brand belongs to c).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in c belongs to brand → brand belongs to c.
      - Set name from chunk.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Set m from \_NAME\_TAGLINE\_RE.search(name).
- If (m and m.start() &gt; 0).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in m → m.start() &gt; 0.
  - Set name from name at slice no value to m.start().strip().
- If len(name.split()) &gt; \_NAME\_MAX\_WORDS.
  - Set name from name.split(“,”) at 0.strip().
- If len(name.split()) &gt; \_NAME\_MAX\_WORDS.
  - Set name from one space.join(name.split() at slice no value to \_NAME\_MAX\_WORDS).
- Return (name or raw).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → raw.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L5668) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L459) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L440)

<a id="op-3d87d31ae8ec6d"></a>
### Safe url

`operation_relationships_domain_enrichment_extractors_business_behavior_safe_resource_address`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** base\_url, raw.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L6483) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L481) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L462)

<a id="op-3e948d1480087e"></a>
### Best icon

`operation_relationships_domain_enrichment_extractors_business_behavior_best_icon`

**Inputs** soup, base\_url.

**Explicit results** empty text · candidates at 0 at 1.

**Local steps**

- Set candidates from list().
- For each tag in soup.find\_all(“link”, href = true).
  - Set rel from (tag.get(“rel”) or list()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tag.get(“rel”) → list().
  - Set rel from one space.join(rel).lower() when isinstance(rel, list), otherwise str(rel).lower().
    - Value choice on isinstance(rel, list) — true gives one space.join(rel).lower(), false gives str(rel).lower().
  - If “icon” does not belong to rel.
    - Continue with the next iteration or loop test.
  - Set href from tag at “href”.strip().
  - Set safe from \_safe\_url(base\_url, href).
  - If not safe.
    - Continue with the next iteration or loop test.
  - Set is\_svg from (“svg” belongs to (nested operand in the contract.get(“type”) or empty text).lower() or nested operand in the contract().split(“?”) at 0.endswith(“.svg”) or “mask-icon” belongs to rel).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in “svg” belongs to (tag.get(“type”) or empty text).lower() → nested operand in the contract.lower().split(“?”) at 0.endswith(“.svg”) → “mask-icon” belongs to rel.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tag.get(“type”) → empty text.
  - Set m from re.search(“(\\d+)x\\d+”, (tag.get(“sizes”, empty text) or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in tag.get(“sizes”, empty text) → empty text.
  - Set px from int(m.group(1)) when m, otherwise \_APPLE\_TOUCH\_PX when “apple-touch” belongs to rel, otherwise 0.
    - Value choice on m — true gives int(m.group(1)), false gives \_APPLE\_TOUCH\_PX when “apple-touch” belongs to rel, otherwise 0.
    - Value choice on “apple-touch” belongs to rel — true gives \_APPLE\_TOUCH\_PX, false gives 0.
  - Evaluate candidates.append(tuple(tuple(1 when is\_svg, otherwise 0, px), safe)).
    - Value choice on is\_svg — true gives 1, false gives 0.
- If not candidates.
  - Return empty text.
- Evaluate candidates.sort(key = deferred anonymous expression, reverse = true).
- Return candidates at 0 at 1.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L6747) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L456) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L437)
