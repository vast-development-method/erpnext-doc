# Company enrichment · operations 5

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Http

<a id="op-7eb6ed5079ce92"></a>
### Retry policy

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_retry_policy`

**Inputs** retries.

**Declared result** Retry.

**Explicit results** Retry(total = retries, backoff\_factor = 0.3, status\_forcelist = RETRY\_STATUS\_FORCELIST, allowed\_methods = frozenset(list(“GET”, “HEAD”))).

**Local steps**

- Return Retry(total = retries, backoff\_factor = 0.3, status\_forcelist = RETRY\_STATUS\_FORCELIST, allowed\_methods = frozenset(list(“GET”, “HEAD”))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L1224) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L495) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L476)

<a id="op-da9a10ee3b6445"></a>
### Pinned IPAdapter.initialize

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_pinned_internet_protocol_adapter_initialize`

**Inputs** self, hostname, remaining named values kwargs.

**Local steps**

- Set self.\_server\_hostname from hostname.
- Evaluate super().\_\_init\_\_(expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L1334) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L491) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L472)

<a id="op-b0283cddb73834"></a>
### Pinned IPAdapter.init poolmanager

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_pinned_internet_protocol_adapter_initialize_poolmanager`

**Inputs** self, remaining positional values args, remaining named values kwargs.

**Local steps**

- Set kwargs at “server\_hostname” from self.\_server\_hostname.
- Evaluate super().init\_poolmanager(expanded args, expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L1433) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L492) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L473)

<a id="op-36eae39b3477b6"></a>
### Pinned adapter

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_pinned_adapter`

**Inputs** session, hostname, retries.

**Declared result** \_PinnedIPAdapter.

**Explicit results** adapter.

**Local steps**

- Set cache from getattr(session, “\_pinned\_adapters”, no value).
- If cache is identical to no value.
  - Set cache from mapping().
  - Set session.\_pinned\_adapters from cache.
- Set adapter from cache.get(hostname).
- If adapter is identical to no value.
  - Set adapter from \_PinnedIPAdapter(hostname, max\_retries = \_retry\_policy(retries)).
  - Set cache at hostname from adapter.
- Return adapter.

**Values supplied outside this operation** selected callable from getattr(session, “\_pinned\_adapters”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L1540) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L489) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L470)

<a id="op-68c3cc7f42a3ad"></a>
### Pinned get

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_pinned_get`

**Inputs** session, url, pinned\_ip, timeout, retries.

**Explicit results** \_pinned\_adapter(session, host, retries).send(prepared, timeout = timeout, stream = true, verify = session.verify, cert = session.cert).

**Local steps**

- Bind dependencies requests.
- Set parsed from urlparse(url).
- Set host from (parsed.hostname or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.hostname → empty text.
- Set ip\_netloc from formatted text &#91;{pinned\_ip}&#93; when “:” belongs to pinned\_ip, otherwise pinned\_ip.
  - Value choice on “:” belongs to pinned\_ip — true gives formatted text &#91;{pinned\_ip}&#93;, false gives pinned\_ip.
- If parsed.port.
  - Set ip\_netloc from formatted text {ip\_netloc}:{parsed.port}.
- Set host\_header from formatted text {host}:{parsed.port} when parsed.port, otherwise host.
  - Value choice on parsed.port — true gives formatted text {host}:{parsed.port}, false gives host.
- Set prepared from session.prepare\_request(requests.Request(“GET”, parsed.\_replace(netloc = ip\_netloc).geturl(), headers = mapping(“Host” → host\_header))).
- Return \_pinned\_adapter(session, host, retries).send(prepared, timeout = timeout, stream = true, verify = session.verify, cert = session.cert).

**Values supplied outside this operation** service or queued work from requests.Request(“GET”, parsed.\_replace(netloc = ip\_netloc).geturl(), headers = mapping(“Host” → host\_header)).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L1807) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L490) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L471)

<a id="op-c6804b848aac5e"></a>
### Sniff html charset

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_sniff_document_markup_charset`

**Inputs** raw.

**Declared result** (str bitwise or no value).

**Explicit results** match.group(1).decode(“ascii”) · no value.

**Local steps**

- Set match from \_META\_CHARSET\_RE.search(raw at slice no value to 4096).
- If match.
  - Attempt the following.
    - Return match.group(1).decode(“ascii”).
  - On failure (tuple(UnicodeDecodeError, AttributeError)).
    - Return no value.
- Return no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L2315) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L496) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L477)

<a id="op-762725569c2909"></a>
### Read capped

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_read_capped`

**Inputs** resp, max\_bytes.

**Declared result** str.

**Explicit results** raw.decode(encoding, errors = “replace”) · raw.decode(“utf-8”, errors = “replace”).

**Local steps**

- Set chunks from list().
- Set total from 0.
- For each chunk in resp.iter\_content(chunk\_size = 16384, decode\_unicode = false).
  - If not chunk.
    - Continue with the next iteration or loop test.
  - Update total using + len(chunk).
  - Evaluate chunks.append(chunk).
  - If total ≥ max\_bytes.
    - Leave the innermost loop without its normal-exhaustion alternative.
- Set raw from byte value.join(chunks).
- If “charset=” belongs to resp.headers.get(“Content-Type”, empty text).lower().
  - Set encoding from (resp.encoding or “utf-8”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in resp.encoding → “utf-8”.
- Otherwise.
  - Set encoding from (\_sniff\_html\_charset(raw) or “utf-8”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_sniff\_html\_charset(raw) → “utf-8”.
- Attempt the following.
  - Return raw.decode(encoding, errors = “replace”).
- On failure (tuple(LookupError, TypeError)).
  - Return raw.decode(“utf-8”, errors = “replace”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L2496) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L493) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L474)

<a id="op-10953f69a60959"></a>
### Fetch

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_fetch`

**Inputs** url, cfg, session = no value, html\_only = true.

**Explicit results** tuple(0, empty text, formatted text blocked by SSRF guard: {exc}, current) · tuple(resp.status\_code, empty text, “redirect without Location header”, current) · tuple(status, empty text, formatted text skipped non-HTML content-type: {content\_type}, current) · tuple(status, html, empty text, current) · tuple(0, empty text, “too many redirects”, current) · 5 additional forms in the steps below.

**Local steps**

- Bind dependencies requests.
- Set timeout from int(cfg.setting(“request\_timeout”)) when cfg, otherwise 10.
  - Value choice on cfg — true gives int(cfg.setting(“request\_timeout”)), false gives 10.
- Set max\_bytes from int(cfg.setting(“max\_download\_bytes”)) when cfg, otherwise 3000000.
  - Value choice on cfg — true gives int(cfg.setting(“max\_download\_bytes”)), false gives 3000000.
- Set retries from int(cfg.setting(“retry\_count”)) when cfg, otherwise 2.
  - Value choice on cfg — true gives int(cfg.setting(“retry\_count”)), false gives 2.
- Set own\_session from session is identical to no value.
- Set session from (session or build\_session(cfg)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in session → build\_session(cfg).
- Set current from url.
- Attempt the following.
  - For each \_hop in range((MAX\_REDIRECTS + 1)).
    - Attempt the following.
      - Set ips from \_validated\_ips(current, cfg).
    - On failure (SSRFError) bound to exc.
      - Return tuple(0, empty text, formatted text blocked by SSRF guard: {exc}, current).
    - Set resp from \_pinned\_get(session, current, ips at 0, timeout, …).
    - If (resp.is\_redirect or resp.is\_permanent\_redirect).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in resp.is\_redirect → resp.is\_permanent\_redirect.
      - Set location from resp.headers.get(“Location”).
      - Evaluate resp.close().
      - If not location.
        - Return tuple(resp.status\_code, empty text, “redirect without Location header”, current).
      - Set current from requests.compat.urljoin(current, location).
      - Continue with the next iteration or loop test.
    - Set content\_type from resp.headers.get(“Content-Type”, empty text).lower().
    - If (html\_only and content\_type and not any(generator of ct belongs to content\_type for ct drawn from HTML\_CONTENT\_TYPES)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in html\_only → content\_type → not any(generator of ct belongs to content\_type for ct drawn from HTML\_CONTENT\_TYPES).
      - Draw ct from HTML\_CONTENT\_TYPES.
      - Set status from resp.status\_code.
      - Evaluate resp.close().
      - Return tuple(status, empty text, formatted text skipped non-HTML content-type: {content\_type}, current).
    - Set html from \_read\_capped(resp, max\_bytes).
    - Set status from resp.status\_code.
    - Evaluate resp.close().
    - Return tuple(status, html, empty text, current).
  - Return tuple(0, empty text, “too many redirects”, current).
- On failure (requests.exceptions.Timeout).
  - Return tuple(0, empty text, formatted text timeout after {timeout}s, current).
- On failure (requests.exceptions.TooManyRedirects).
  - Return tuple(0, empty text, “too many redirects”, current).
- On failure (requests.exceptions.SSLError) bound to exc.
  - Return tuple(0, empty text, formatted text ssl error: {exc}, current).
- On failure (requests.exceptions.ConnectionError) bound to exc.
  - Return tuple(0, empty text, formatted text connection error: {exc}, current).
- On failure (requests.exceptions.RequestException) bound to exc.
  - Return tuple(0, empty text, formatted text request error: {exc}, current).
- On failure (Exception) bound to exc.
  - Return tuple(0, empty text, formatted text unexpected error: {exc}, current).
- On exit, including pending return or failure.
  - If own\_session.
    - Evaluate session.close().

**Values supplied outside this operation** service or queued work from requests.compat.urljoin(current, location).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L2957) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L487) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L468)

## Service · Install

<a id="op-71c8447f71846b"></a>
### Seed default rules and mappings

`operation_relationships_domain_enrichment_install_business_behavior_seed_default_rules_and_mappings`

**Inputs** no declared parameters.

**Local steps**

- Evaluate \_seed\_industry\_rules().
- Evaluate \_seed\_social\_rules().
- Evaluate \_seed\_field\_mappings().
- Evaluate \_seed\_settings\_defaults().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L4291) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L501) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L482)

<a id="op-035496a2da3b89"></a>
### Seed settings defaults

`operation_relationships_domain_enrichment_install_business_behavior_seed_settings_defaults`

**Inputs** no declared parameters.

**Record and data access** read “CRM Enrichment Settings” via get\_single.

**State and service calls** call save on settings.

**Explicit results** no value.

**Local steps**

- Bind dependencies DEFAULT\_LINK\_PRIORITY.
- Set settings from Platform.get\_single(“CRM Enrichment Settings”).
- If settings.link\_priority\_order.
  - Return no value.
- For each tuple(keyword, weight) in DEFAULT\_LINK\_PRIORITY.
  - Evaluate settings.append(“link\_priority\_order”, mapping(“keyword” → keyword, “weight” → weight)).
- Evaluate settings.save(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L4378) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L504) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L485)

<a id="op-db7dedaac51e85"></a>
### Ensure industry

`operation_relationships_domain_enrichment_install_business_behavior_ensure_industry`

**Inputs** industry.

**Record and data access** read “CRM Industry” via exists · resolve a document from mapping(“doctype” → “CRM Industry”, “industry” → industry) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Industry”, “industry” → industry)).

**Local steps**

- If not Platform.db.exists(“CRM Industry”, industry).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Industry”, “industry” → industry)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L4582) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L499) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L480)

<a id="op-9683327be252c5"></a>
### Make rule

`operation_relationships_domain_enrichment_install_business_behavior_make_rule`

**Inputs** rule\_name, rule\_type, patterns, target\_value (named only, default no value), industry (named only, default no value), weight (named only, default 1), match\_scope (named only, default “Full Text”), is\_regex (named only, default false).

**Record and data access** resolve a document from mapping(“doctype” → “CRM Enrichment Rule”, “rule\_name” → rule\_name, “rule\_type” → rule\_type, “target\_value” → target\_value, …) via get\_doc.

**State and service calls** call insert on doc.

**Explicit results** no value.

**Local steps**

- If find\_duplicate(rule\_type, (target\_value or industry)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in target\_value → industry.
  - Return no value.
- Set doc from Platform.get\_doc(mapping(“doctype” → “CRM Enrichment Rule”, “rule\_name” → rule\_name, “rule\_type” → rule\_type, “target\_value” → target\_value, …)).
  - Draw p from patterns.
  - Value choice on is\_regex — true gives 1, false gives 0.
- Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L5) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L500) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L481)

<a id="op-79d3ba8f891a22"></a>
### Seed industry rules

`operation_relationships_domain_enrichment_install_business_behavior_seed_industry_rules`

**Inputs** no declared parameters.

**Local steps**

- For each tuple(industry, keywords) in INDUSTRY\_KEYWORDS.items().
  - Evaluate \_ensure\_industry(industry).
  - Evaluate \_make\_rule(formatted text Industry: {industry}, “Industry”, keywords, industry = industry, match\_scope = “Headline”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L5172) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L503) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L484)

<a id="op-bdbec603c8bb3c"></a>
### Seed social rules

`operation_relationships_domain_enrichment_install_business_behavior_seed_social_rules`

**Inputs** no declared parameters.

**Local steps**

- For each tuple(network, patterns) in SOCIAL\_PATTERNS.items().
  - Evaluate \_make\_rule(formatted text Social: {network}, “Social”, patterns, target\_value = network, match\_scope = “HTML”, is\_regex = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L5318) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L505) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L486)

<a id="op-c0b9140209e176"></a>
### Seed field mappings

`operation_relationships_domain_enrichment_install_business_behavior_seed_field_mappings`

**Inputs** no declared parameters.

**Record and data access** read “CRM Enrichment Field Mapping” via exists · resolve a document from mapping(“doctype” → “CRM Enrichment Field Mapping”, “enabled” → 1, “source\_key” → source\_key, “target\_doctype” → target\_doctype, …) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “CRM Enrichment Field Mapping”, “enabled” → 1, “source\_key” → source\_key, “target\_doctype” → target\_doctype, …)).

**Local steps**

- For each tuple(source\_key, target\_doctype, target\_fieldname, write\_policy, …) in FIELD\_MAPPINGS.
  - Set exists from Platform.db.exists(“CRM Enrichment Field Mapping”, mapping(“source\_key” → source\_key, “target\_doctype” → target\_doctype, “target\_fieldname” → target\_fieldname)).
  - If exists.
    - Continue with the next iteration or loop test.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “CRM Enrichment Field Mapping”, “enabled” → 1, “source\_key” → source\_key, “target\_doctype” → target\_doctype, …)).insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L5453) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L502) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L483)

## Service · Mapper

<a id="op-f62dd04e9720c8"></a>
### Source key labels

`operation_relationships_domain_enrichment_mapper_business_behavior_source_key_labels`

**Inputs** no declared parameters.

**Declared result** dict.

**Explicit results** mapping(“company\_name” → translated “Organization Name”, “description” → translated “Company Description”, “logo” → translated “Logo”, “industry” → translated “Industry”, …).

**Local steps**

- Return mapping(“company\_name” → translated “Organization Name”, “description” → translated “Company Description”, “logo” → translated “Logo”, “industry” → translated “Industry”, …).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L5798) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L513) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L494)

<a id="op-353c5ce54f4b87"></a>
### Filled labels

`operation_relationships_binding_crm_domain_enrichment_mapper_filled_labels`

**Inputs** changes.

**Declared result** list at str.

**Explicit results** labels.

**Local steps**

- Set labels from list().
- For each change in changes.
  - If change.label does not belong to labels.
    - Evaluate labels.append(change.label).
- Return labels.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L180) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L336) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L317)

<a id="op-0ead15f327c9ad"></a>
### First email

`operation_relationships_domain_enrichment_mapper_business_behavior_first_email`

**Inputs** result.

**Declared result** str.

**Explicit results** empty text · e.value · result.emails at 0.value.

**Local steps**

- If not result.emails.
  - Return empty text.
- Set registrable from registrable\_domain(urlparse((result.website or empty text)).netloc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.website → empty text.
- If registrable.
  - For each e in result.emails.
    - Set domain from e.value.lower().split(“@”) at negative 1.
    - If (domain equals registrable or domain.endswith((“.” + registrable))).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in domain equals registrable → domain.endswith((“.” + registrable)).
      - Return e.value.
- Return result.emails at 0.value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L6184) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L508) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L489)

<a id="op-4680b45b6ea771"></a>
### Phone at

`operation_relationships_domain_enrichment_mapper_business_behavior_phone_at`

**Inputs** result, index.

**Declared result** str.

**Explicit results** empty text · (p.raw or p.value).

**Local steps**

- If not result.phones.
  - Return empty text.
- If index ≥ len(result.phones).
  - Set index from 0.
- Set p from result.phones at index.
- Return (p.raw or p.value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in p.raw → p.value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L6473) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L512) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L493)

<a id="op-cb173bfc2b3bc1"></a>
### Get value for source key

`operation_relationships_domain_enrichment_mapper_business_behavior_get_value_for_source_key`

**Inputs** result, source\_key.

**Explicit results** (result.company\_name.value or empty text) · (result.description.value or empty text) · (result.logo.value or empty text) · (result.image.value or empty text) · (result.industry.value or empty text) · 5 additional forms in the steps below.

**Local steps**

- If source\_key equals “company\_name”.
  - Return (result.company\_name.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.company\_name.value → empty text.
- If source\_key equals “description”.
  - Return (result.description.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.description.value → empty text.
- If source\_key equals “logo”.
  - Return (result.logo.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.logo.value → empty text.
- If source\_key equals “image”.
  - Return (result.image.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.image.value → empty text.
- If source\_key equals “industry”.
  - Return (result.industry.value or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in result.industry.value → empty text.
- If source\_key equals “primary\_email”.
  - Return \_first\_email(result).
- If source\_key equals “primary\_phone”.
  - Return \_phone\_at(result, 0).
- If source\_key equals “secondary\_phone”.
  - Return \_phone\_at(result, 1).
- If source\_key belongs to \_SOCIAL\_KEYS.
  - Set profile from result.social\_profiles.get(source\_key).
  - Return profile.value when profile, otherwise empty text.
    - Value choice on profile — true gives profile.value, false gives empty text.
- Return empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L6643) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L509) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L490)

<a id="op-e2195dc2e3da79"></a>
### Ensure link target

`operation_relationships_domain_enrichment_mapper_business_behavior_ensure_link_target`

**Inputs** target\_doctype, target\_fieldname, value.

**Record and data access** read link\_doctype via exists · resolve a document from new\_doc via get\_doc.

**State and service calls** call insert on Platform.get\_doc(new\_doc).

**Explicit results** value · no value.

**Local steps**

- Set meta from Platform.get\_meta(target\_doctype).
- Set df from meta.get\_field(target\_fieldname).
- If (not df or df.fieldtype differs from “Link” or not df.options).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not df → df.fieldtype differs from “Link” → not df.options.
  - Return value.
- Set link\_doctype from df.options.
- If Platform.db.exists(link\_doctype, value).
  - Return value.
- If not Platform.has\_permission(link\_doctype, ptype = “create”).
  - Return no value.
- Attempt the following.
  - Set link\_meta from Platform.get\_meta(link\_doctype).
  - Set new\_doc from mapping(“doctype” → link\_doctype).
  - Set autoname from (link\_meta.autoname or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in link\_meta.autoname → empty text.
  - If autoname.startswith(“field:”).
    - Set new\_doc at autoname.split(“:”, 1) at 1 from value.
  - Otherwise.
    - If link\_meta.get\_title\_field().
      - Set new\_doc at link\_meta.get\_title\_field() from value.
    - Otherwise.
      - Set new\_doc at “\_\_newname” from value.
  - Evaluate Platform.get\_doc(new\_doc).insert().
  - Return value.
- On failure (Exception).
  - Evaluate Platform.log\_error(title = “Domain Enrichment: could not create link master”, message = formatted text {link\_doctype}={value} for {target\_doctype}.{target\_fieldname}).
  - Return no value.

**Values supplied outside this operation** effective access from Platform.has\_permission(link\_doctype, ptype = “create”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L7172) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L507) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L488)

<a id="op-8d1ad6e2c24b7b"></a>
### Label for

`operation_relationships_domain_enrichment_mapper_business_behavior_label_for`

**Inputs** doc, source\_key, target\_fieldname.

**Declared result** str.

**Explicit results** label · df.label when (df and df.label), otherwise target\_fieldname.

**Local steps**

- Set label from \_source\_key\_labels().get(source\_key).
- If label.
  - Return label.
- Set df from doc.meta.get\_field(target\_fieldname).
- Return df.label when (df and df.label), otherwise target\_fieldname.
  - Value choice on (df and df.label) — true gives df.label, false gives target\_fieldname.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df → df.label.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L7854) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L510) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L491)

<a id="op-f0ed1f0738db2f"></a>
### Overridable defaults

`operation_relationships_domain_enrichment_mapper_business_behavior_overridable_defaults`

**Inputs** mapping.

**Declared result** set.

**Explicit results** defaults.

**Local steps**

- Set defaults from set(empty text).
- For each line in (mapping.default\_values or empty text).splitlines().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in mapping.default\_values → empty text.
  - Set token from line.strip().
  - If token.
    - Evaluate defaults.add(token).
- Return defaults.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0022.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L511) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L492)

<a id="op-029d8ed5300d99"></a>
### Apply to document

`operation_relationships_domain_enrichment_mapper_business_behavior_apply_to_document`

**Inputs** doc, result, cfg, fill\_empty\_only = false.

**Declared result** list at FieldChange.

**Explicit results** list(changes.values()).

**Local steps**

- Set changes from mapping().
- Bind local operation record for subsequent calls.
- Set mappings from cfg.mappings\_by\_doctype.get(doc.doctype, list()).
- For each mapping in mappings.
  - Set fieldname from mapping.target\_fieldname.
  - If not doc.meta.has\_field(fieldname).
    - Continue with the next iteration or loop test.
  - Set value from get\_value\_for\_source\_key(result, mapping.source\_key).
  - Set label from \_label\_for(doc, mapping.source\_key, fieldname).
  - Set current from doc.get(fieldname).
  - Set policy from POLICY\_FILL\_IF\_EMPTY when fill\_empty\_only, otherwise (mapping.write\_policy or POLICY\_FILL\_IF\_EMPTY).
    - Value choice on fill\_empty\_only — true gives POLICY\_FILL\_IF\_EMPTY, false gives (mapping.write\_policy or POLICY\_FILL\_IF\_EMPTY).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in mapping.write\_policy → POLICY\_FILL\_IF\_EMPTY.
  - If policy equals POLICY\_ALWAYS\_REFRESH.
    - If (not value or current equals value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not value → current equals value.
      - Continue with the next iteration or loop test.
    - If mapping.create\_missing\_link.
      - Set value from \_ensure\_link\_target(doc.doctype, fieldname, value).
      - If value is identical to no value.
        - Continue with the next iteration or loop test.
    - Evaluate doc.set(fieldname, value).
    - Evaluate record(fieldname, current, value, label).
    - Continue with the next iteration or loop test.
  - If not value.
    - Continue with the next iteration or loop test.
  - If policy equals POLICY\_OVERRIDE\_DEFAULTS.
    - Set overridable from \_overridable\_defaults(mapping).
    - If (current and current does not belong to overridable).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in current → current does not belong to overridable.
      - Continue with the next iteration or loop test.
  - Otherwise.
    - If current.
      - Continue with the next iteration or loop test.
  - If current equals value.
    - Continue with the next iteration or loop test.
  - If mapping.create\_missing\_link.
    - Set value from \_ensure\_link\_target(doc.doctype, fieldname, value).
    - If value is identical to no value.
      - Continue with the next iteration or loop test.
  - Evaluate doc.set(fieldname, value).
  - Evaluate record(fieldname, current, value, label).
- Return list(changes.values()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L506) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L487)
