# Company enrichment · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Mapper

<a id="op-6fc28474fb91da"></a>
### Apply to document.record

`operation_relationships_binding_crm_domain_enrichment_mapper_apply_to_document_record`

**Inputs** fieldname, old\_value, new\_value, label.

**Local steps**

- If fieldname belongs to changes.
  - Set old\_value from changes at fieldname.old\_value.
- Set changes at fieldname from FieldChange(fieldname, old\_value, new\_value, label).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L179) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L335) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L316)

## Service · Pipeline

<a id="op-eb6269c5318c5f"></a>
### Normalize website

`operation_relationships_domain_enrichment_pipeline_business_behavior_normalize_website`

**Inputs** url.

**Declared result** str.

**Explicit results** url.

**Explicit failure paths** ValueError(“website URL is required”) · ValueError(formatted text unsupported URL scheme: {parsed.scheme}) · ValueError(formatted text invalid URL: {url}).

**Local steps**

- Set url from (url or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in url → empty text.
- If not url.
  - Raise ValueError(“website URL is required”).
- If not urlparse(url).scheme.
  - Set url from (text in the contract + url).
- Set parsed from urlparse(url).
- If parsed.scheme does not belong to tuple(“http”, “https”).
  - Raise ValueError(formatted text unsupported URL scheme: {parsed.scheme}).
- If not parsed.netloc.
  - Raise ValueError(formatted text invalid URL: {url}).
- Return url.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L1005) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L514) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L495)

<a id="op-b0d1f8ac78d751"></a>
### Run

`operation_relationships_domain_enrichment_pipeline_business_behavior_run`

**Inputs** website, cfg = no value, progress = no value.

**Declared result** EnrichmentResult.

**Explicit results** result.

**Local steps**

- Set website from \_normalize\_website(website).
- Set cfg from (cfg or get\_config()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cfg → get\_config().
- Set result from EnrichmentResult(website = website).
- Bind local operation emit for subsequent calls.
- Set session from build\_session(cfg).
- Attempt the following.
  - Evaluate emit(0).
  - Set crawled from crawl(website, cfg, session = session, progress = deferred anonymous expression).
  - Set pages from list of page for tuple(page, \_soup) drawn from crawled.
    - Draw tuple(page, \_soup) from crawled.
  - Set soups\_by\_url from mapping of page.url → soup for tuple(page, soup) drawn from crawled.
    - Draw tuple(page, soup) from crawled.
  - Set result.pages\_crawled from list of mapping(“url” → p.url, “status” → p.status\_code, “error” → p.error) for p drawn from pages.
    - Draw p from pages.
  - Set result.errors from list of mapping(“url” → p.url, “error” → p.error) for p drawn from pages where p.error.
    - Draw p from pages, keep a combination only if (p.error).
  - Set reason from extractors.diagnose\_readability(pages).
  - If reason belongs to tuple(“blocked”, “unreachable”).
    - Evaluate result.notes.append(extractors.READABILITY\_MESSAGES at reason).
    - Evaluate emit(6).
    - Return result.
  - If reason equals “empty”.
    - Evaluate result.notes.append(extractors.READABILITY\_MESSAGES at “empty”).
  - Set homepage from pages at 0.
  - Set home\_soup from soups\_by\_url.get(homepage.url).
  - Set max\_pages from int((cfg.setting(“max\_pages”, 10) or 10)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cfg.setting(“max\_pages”, 10) → 10.
  - If (home\_soup and len(pages) &lt; max\_pages and not any(generator of extractors.\_is\_about\_page(p.url) for p drawn from pages)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in home\_soup → len(pages) &lt; max\_pages → not any(generator of extractors.\_is\_about\_page(p.url) for p drawn from pages).
    - Draw p from pages.
    - For each tuple(page, soup) in probe\_about\_pages(homepage.url, cfg, session = session, skip\_urls = list of p.url for p drawn from pages).
      - Draw p from pages.
      - Evaluate pages.append(page).
      - Set soups\_by\_url at page.url from soup.
      - Evaluate result.pages\_crawled.append(mapping(“url” → page.url, “status” → page.status\_code, “error” → page.error)).
  - Evaluate emit(2).
  - Set company from extractors.extract\_company\_info(homepage, home\_soup) when home\_soup, otherwise mapping().
    - Value choice on home\_soup — true gives extractors.extract\_company\_info(homepage, home\_soup), false gives mapping().
  - Set result.company\_name from (company.get(“company\_name”) or Field()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in company.get(“company\_name”) → Field().
  - Set result.logo from (company.get(“logo”) or Field()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in company.get(“logo”) → Field().
  - Set result.image from (company.get(“image”) or Field()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in company.get(“image”) → Field().
  - Set result.description from (extractors.select\_description(pages, soups\_by\_url, industry\_rules = cfg.rules(“Industry”), company\_name = result.company\_name.value) or company.get(“description”) or Field()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in extractors.select\_description(pages, soups\_by\_url, industry\_rules = cfg.rules(“Industry”), company\_name = result.company\_name.value) → company.get(“description”) → Field().
  - Evaluate emit(3).
  - Set result.emails from extractors.extract\_emails(pages).
  - Set result.phones from extractors.extract\_phones(pages).
  - Set result.social\_profiles from extractors.extract\_social\_profiles(pages, soups\_by\_url, cfg.rules(“Social”), extra\_links = company.get(“social\_links”)).
  - Evaluate emit(4).
  - Set tuple(industry, confidence) from extractors.classify\_industry(pages, company, cfg.rules(“Industry”)).
  - Set result.industry from Field(industry, website, Method.KEYWORD\_CLASSIFIER) when industry, otherwise Field().
    - Value choice on industry — true gives Field(industry, website, Method.KEYWORD\_CLASSIFIER), false gives Field().
  - Set result.industry\_confidence from confidence.
  - Evaluate emit(5).
  - Evaluate emit(6).
  - Return result.
- On exit, including pending return or failure.
  - Evaluate session.close().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L1332) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L515) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L496)

<a id="op-1fdb9b5ddddffc"></a>
### Run.emit

`operation_relationships_domain_enrichment_pipeline_business_behavior_run_emit`

**Inputs** step\_index, message = empty text.

**Local steps**

- If progress.
  - Attempt the following.
    - Evaluate progress(step\_index, (message or PROGRESS\_STEPS at step\_index)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in message → PROGRESS\_STEPS at step\_index.
  - On failure (Exception).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L3368) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L516) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L497)

## Service · Result

<a id="op-2ba78419244399"></a>
### Email.to dict

`operation_relationships_domain_enrichment_result_business_behavior_email_to_mapping`

**Inputs** self.

**Explicit results** mapping(“value” → self.value, “source” → self.source, “method” → self.method).

**Local steps**

- Return mapping(“value” → self.value, “source” → self.source, “method” → self.method).

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L3483) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L519) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L500)

<a id="op-af21a27dd22057"></a>
### Phone.to dict

`operation_relationships_domain_enrichment_result_business_behavior_phone_to_mapping`

**Inputs** self.

**Explicit results** mapping(“value” → self.value, “raw” → self.raw, “source” → self.source, “method” → self.method).

**Local steps**

- Return mapping(“value” → self.value, “raw” → self.raw, “source” → self.source, “method” → self.method).

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L3581) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L523) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L504)

<a id="op-ff853f7f2822ad"></a>
### Field.to dict

`operation_relationships_domain_enrichment_result_business_behavior_field_to_mapping`

**Inputs** self.

**Explicit results** mapping(“value” → self.value, “source” → self.source, “method” → self.method).

**Local steps**

- Return mapping(“value” → self.value, “source” → self.source, “method” → self.method).

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L3699) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L522) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L503)

<a id="op-08034e26daac2d"></a>
### Social Profile.to dict

`operation_relationships_domain_enrichment_result_business_behavior_social_profile_to_mapping`

**Inputs** self.

**Explicit results** mapping(“value” → self.value, “source” → self.source, “method” → self.method).

**Local steps**

- Return mapping(“value” → self.value, “source” → self.source, “method” → self.method).

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L3797) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L524) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L505)

<a id="op-46702643ffed4f"></a>
### Enrichment Result.to dict

`operation_relationships_domain_enrichment_result_business_behavior_enrichment_result_to_mapping`

**Inputs** self.

**Explicit results** mapping(“company\_name” → self.company\_name.to\_dict(), “description” → self.description.to\_dict(), “logo” → self.logo.to\_dict(), “image” → self.image.to\_dict(), …).

**Local steps**

- Return mapping(“company\_name” → self.company\_name.to\_dict(), “description” → self.description.to\_dict(), “logo” → self.logo.to\_dict(), “image” → self.image.to\_dict(), …).
  - Draw e from self.emails.
  - Draw p from self.phones.
  - Draw tuple(k, v) from self.social\_profiles.items().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L3895) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L521) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L502)

<a id="op-6b1ff43620af33"></a>
### Enrichment Result.flat

`operation_relationships_domain_enrichment_result_business_behavior_enrichment_result_flat`

**Inputs** self.

**Explicit results** mapping(“company\_name” → self.company\_name.value, “description” → self.description.value, “logo” → self.logo.value, “industry” → self.industry.value, …).

**Local steps**

- Return mapping(“company\_name” → self.company\_name.value, “description” → self.description.value, “logo” → self.logo.value, “industry” → self.industry.value, …).
  - Draw tuple(k, v) from self.social\_profiles.items().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L4368) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L520) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L501)

<a id="op-8f0284b7b04319"></a>
### Crawled Page.to dict

`operation_relationships_domain_enrichment_result_business_behavior_crawled_page_to_mapping`

**Inputs** self.

**Explicit results** asdict(self).

**Local steps**

- Return asdict(self).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L4605) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L518) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L499)

## Service · Tasks

<a id="op-54f42571b7ec18"></a>
### Publish

`operation_relationships_domain_enrichment_tasks_business_behavior_publish`

**Inputs** reference\_doctype, reference\_name, status, message = empty text, step = 0, payload = no value, user = no value.

**State and service calls** publish realtime with PROGRESS\_EVENT.

**Local steps**

- Attempt the following.
  - Evaluate Platform.publish\_realtime(PROGRESS\_EVENT, mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “step” → step, “total” → TOTAL\_STEPS, …), user = user).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in payload → mapping().
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.publish\_realtime(PROGRESS\_EVENT, mapping(“reference\_doctype” → reference\_doctype, “reference\_name” → reference\_name, “step” → step, “total” → TOTAL\_STEPS, …), user = user).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L4655) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L527) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L508)

<a id="op-236191ce1890a9"></a>
### Write run

`operation_relationships_domain_enrichment_tasks_business_behavior_write_run`

**Inputs** reference\_doctype, reference\_name, website, status, result = no value, started\_on = no value, notes = empty text, changes = no value.

**State and service calls** request new\_doc for “CRM Enrichment Run” · call insert on doc.

**Explicit results** doc.name.

**Local steps**

- Set doc from Platform.new\_doc(“CRM Enrichment Run”).
- Set doc.reference\_doctype from reference\_doctype.
- Set doc.reference\_name from reference\_name.
- Set doc.source\_website from website.
- Set doc.status from status.
- Set doc.started\_on from (started\_on or Platform.utils.now\_datetime()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in started\_on → Platform.utils.now\_datetime().
- If status belongs to tuple(“Completed”, “Failed”).
  - Set doc.finished\_on from Platform.utils.now\_datetime().
- If notes.
  - Set doc.notes from notes.
- If result is distinct from no value.
  - Set social from “, ”.join(sorted(generator of k for tuple(k, v) drawn from result.social\_profiles.items() where v.value)).
    - Draw tuple(k, v) from result.social\_profiles.items(), keep a combination only if (v.value).
  - Set doc.company\_name from (result.company\_name.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.company\_name.value → empty text.
  - Set doc.industry from (result.industry.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.industry.value → empty text.
  - Set doc.industry\_confidence from (result.industry\_confidence or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.industry\_confidence → 0.
  - Set doc.emails\_found from len(result.emails).
  - Set doc.phones\_found from len(result.phones).
  - Set doc.social\_profiles from social.
  - Set doc.raw\_json from Platform.as\_json(result.to\_dict()).
  - If (not notes and result.notes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not notes → result.notes.
    - Set doc.notes from whitespace '\\n'.join(result.notes).
- For each change in (changes or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in changes → list().
  - Evaluate doc.append(“changes”, mapping(“fieldname” → change.fieldname, “old\_value” → change.old\_value, “new\_value” → change.new\_value)).
- Evaluate doc.insert(ignore\_permissions = true).
- Return doc.name.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L9) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L530) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L511)

<a id="op-2e49eeb1094c5e"></a>
### Enrichment job id

`operation_relationships_binding_crm_domain_enrichment_tasks_enrichment_job_id`

**Inputs** reference\_doctype, reference\_name.

**Declared result** str.

**Explicit results** formatted text domain-enrich-{reference\_doctype}-{reference\_name}.

**Local steps**

- Return formatted text domain-enrich-{reference\_doctype}-{reference\_name}.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L181) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L337) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L318)

<a id="op-5271dd92d1af2a"></a>
### Enqueue enrichment

`operation_relationships_domain_enrichment_tasks_business_behavior_enqueue_enrichment`

**Inputs** reference\_doctype, reference\_name, website, user, trigger = “manual”.

**Declared result** dict.

**State and service calls** enqueue with “crm.domain\_enrichment.tasks.run\_enrichment”.

**Explicit results** mapping(“queued” → false, “job\_id” → job\_id, “website” → website) · mapping(“queued” → true, “job\_id” → job\_id, “website” → website).

**Local steps**

- Set s from get\_settings().
- Set timeout from ((int(\_setting(s, “request\_timeout”)) × int(\_setting(s, “max\_pages”))) + 60).
- Set job\_id from enrichment\_job\_id(reference\_doctype, reference\_name).
- If is\_job\_enqueued(job\_id).
  - Return mapping(“queued” → false, “job\_id” → job\_id, “website” → website).
- Evaluate Platform.enqueue(“crm.domain\_enrichment.tasks.run\_enrichment”, queue = “long”, timeout = timeout, job\_id = job\_id, deduplicate = true, …).
- Return mapping(“queued” → true, “job\_id” → job\_id, “website” → website).

**Values supplied outside this operation** service or queued work from Platform.enqueue(“crm.domain\_enrichment.tasks.run\_enrichment”, queue = “long”, timeout = timeout, job\_id = job\_id, deduplicate = true, …).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L7) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L526) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L507)

<a id="op-c7e7fd9907518f"></a>
### Auto enrich on create

`operation_relationships_domain_enrichment_tasks_business_behavior_auto_enrich_on_create`

**Inputs** doc, method = no value.

**Explicit results** no value.

**Local steps**

- Attempt the following.
  - If not auto\_enrich\_enabled\_for(doc.doctype).
    - Return no value.
  - Set website from (doc.get(“website”) or empty text).strip().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in doc.get(“website”) → empty text.
  - If not website.
    - Return no value.
  - Evaluate enqueue\_enrichment(doc.doctype, doc.name, website, Platform.session.user, trigger = “auto”).
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Domain Enrichment: auto\_enrich\_on\_create failed”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L6177) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L525) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L506)

<a id="op-18278b4f47f1ee"></a>
### Run enrichment

`operation_relationships_domain_enrichment_tasks_business_behavior_run_enrichment`

**Inputs** reference\_doctype, reference\_name, website, user = no value, trigger = “manual”.

**Record and data access** resolve a document from reference\_doctype via get\_doc.

**State and service calls** call save on doc · rollback.

**Local steps**

- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set started\_on from Platform.utils.now\_datetime().
- Bind local operation progress for subsequent calls.
- Attempt the following.
  - Set cfg from get\_config().
  - Evaluate \_publish(reference\_doctype, reference\_name, status = “running”, message = “Starting”, step = 0, user = user).
  - Set result from run\_pipeline(website, cfg = cfg, progress = progress).
  - Set doc from Platform.get\_doc(reference\_doctype, reference\_name).
  - Evaluate doc.check\_permission(“write”).
  - Set changes from list of change for change drawn from apply\_to\_document(doc, result, cfg) where Platform.utils.cstr(change.old\_value) differs from Platform.utils.cstr(change.new\_value).
    - Draw change from apply\_to\_document(doc, result, cfg), keep a combination only if (Platform.utils.cstr(change.old\_value) differs from Platform.utils.cstr(change.new\_value)).
  - If changes.
    - Evaluate doc.save().
  - Set filled\_fields from filled\_labels(changes).
  - Evaluate write\_run(reference\_doctype, reference\_name, website, status = “Completed”, result = result, started\_on = started\_on, changes = changes).
  - Evaluate \_publish(reference\_doctype, reference\_name, status = “completed”, message = “Completed”, step = (TOTAL\_STEPS − 1), payload = mapping(“filled\_fields” → filled\_fields, “notes” → result.notes, expand result.flat()), …).
  - Evaluate capture(“enrichment\_run\_completed”, “crm”, properties = mapping(“doctype” → reference\_doctype, “trigger” → trigger, “status” → “success”)).
- On failure (Exception).
  - Evaluate Platform.db.rollback().
  - Evaluate Platform.log\_error(title = “Domain Enrichment: run\_enrichment failed”, message = Platform.get\_traceback()).
  - Attempt the following.
    - Evaluate write\_run(reference\_doctype, reference\_name, website, status = “Failed”, started\_on = started\_on, notes = Platform.utils.cstr(Platform.get\_traceback()) at slice no value to 1000).
  - On failure (Exception).
    - Evaluate Platform.log\_error(title = “Domain Enrichment: could not write Failed run”).
  - Evaluate \_publish(reference\_doctype, reference\_name, status = “error”, message = Platform.\_(“Enrichment failed. Check the error log.”), step = 0, user = user).
  - Evaluate capture(“enrichment\_run\_completed”, “crm”, properties = mapping(“doctype” → reference\_doctype, “trigger” → trigger, “status” → “failure”)).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.utils.now\_datetime() · effective access from doc.check\_permission(“write”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L8) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L528) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L509)

<a id="op-f7203e150b79ff"></a>
### Run enrichment.progress

`operation_relationships_domain_enrichment_tasks_business_behavior_run_enrichment_progress`

**Inputs** step\_index, message = empty text.

**Local steps**

- Evaluate \_publish(reference\_doctype, reference\_name, status = “running”, message = message, step = step\_index, user = user).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L7651) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L529) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L510)
