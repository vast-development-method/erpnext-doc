# Company enrichment · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Crawler

<a id="op-dfce3a98bd2389"></a>
### Normalize url

`operation_relationships_domain_enrichment_crawler_business_behavior_normalize_resource_address`

**Inputs** url.

**Declared result** str.

**Explicit results** url.

**Local steps**

- Set tuple(url, \_frag) from urldefrag(url).
- Set parsed from urlparse(url).
- If parsed.query.
  - Set url from parsed.\_replace(query = empty text).geturl().
- If (url.endswith(“/”) and len(urlparse(url).path) &gt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in url.endswith(“/”) → len(urlparse(url).path) &gt; 1.
  - Set url from url.rstrip(“/”).
- Return url.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L547) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L444) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L425)

<a id="op-af9bca0c3a670a"></a>
### Tld extractor

`operation_relationships_domain_enrichment_crawler_business_behavior_top_level_domain_extractor`

**Inputs** no declared parameters.

**Wrappers, in declaration order** lru\_cache(maxsize = 1).

**Declared result** tldextract.TLDExtract.

**Explicit results** tldextract.TLDExtract(suffix\_list\_urls = tuple(), cache\_dir = no value, include\_psl\_private\_domains = true).

**Local steps**

- Return tldextract.TLDExtract(suffix\_list\_urls = tuple(), cache\_dir = no value, include\_psl\_private\_domains = true).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L814) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L451) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L432)

<a id="op-cf4dc30b44d3d6"></a>
### Registrable domain

`operation_relationships_domain_enrichment_crawler_business_behavior_registrable_domain`

**Inputs** netloc.

**Declared result** str.

**Explicit results** formatted text {extracted.domain}.{extracted.suffix} · (extracted.domain or netloc).

**Local steps**

- Set netloc from netloc.lower().split(“:”) at 0.
- Set extracted from \_tld\_extractor()(netloc).
- If (extracted.domain and extracted.suffix).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in extracted.domain → extracted.suffix.
  - Return formatted text {extracted.domain}.{extracted.suffix}.
- Return (extracted.domain or netloc).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extracted.domain → netloc.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L906) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L448) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L429)

<a id="op-37e54e67e1b09f"></a>
### Same site

`operation_relationships_domain_enrichment_crawler_business_behavior_same_site`

**Inputs** url, base\_netloc.

**Declared result** bool.

**Explicit results** registrable\_domain(urlparse(url).netloc) equals registrable\_domain(base\_netloc) · false.

**Local steps**

- Attempt the following.
  - Return registrable\_domain(urlparse(url).netloc) equals registrable\_domain(base\_netloc).
- On failure (Exception).
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L1117) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L450) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L431)

<a id="op-0ceed4aee6ceb9"></a>
### Link priority

`operation_relationships_domain_enrichment_crawler_business_behavior_link_priority`

**Inputs** url, anchor\_text, link\_priority.

**Declared result** float.

**Explicit results** best when best is distinct from no value, otherwise (len(link\_priority) + 1).

**Local steps**

- Set path from urlparse(url).path.rstrip(“/”).
- Set leaf from path.rsplit(“/”, 1) at negative 1 when path, otherwise empty text.
  - Value choice on path — true gives path.rsplit(“/”, 1) at negative 1, false gives empty text.
- Set haystack from ((leaf + one space) + (anchor\_text or empty text)).lower().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in anchor\_text → empty text.
- Set best from no value.
- For each tuple(idx, tuple(kw, weight)) in enumerate(link\_priority).
  - If (kw and kw belongs to haystack).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in kw → kw belongs to haystack.
    - Set score from (idx − (weight or 1.0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in weight → 1.0.
    - If (best is identical to no value or score &lt; best).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in best is identical to no value → score &lt; best.
      - Set best from score.
- Return best when best is distinct from no value, otherwise (len(link\_priority) + 1).
  - Value choice on best is distinct from no value — true gives best, false gives (len(link\_priority) + 1).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L1257) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L440) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L421)

<a id="op-92915bb9171942"></a>
### Is crawlable

`operation_relationships_domain_enrichment_crawler_business_behavior_is_crawlable`

**Inputs** url, skip\_patterns.

**Declared result** bool.

**Explicit results** false · true.

**Local steps**

- Set low from url.lower().
- If any(generator of low.startswith(s) for s drawn from SKIP\_SCHEMES).
  - Draw s from SKIP\_SCHEMES.
  - Return false.
- Set path from urlparse(url).path.lower().
- If path.endswith(SKIP\_EXTENSIONS).
  - Return false.
- If urlparse(url).scheme does not belong to tuple(“http”, “https”).
  - Return false.
- For each pat in skip\_patterns.
  - Attempt the following.
    - If re.search(pat, url, re.IGNORECASE).
      - Return false.
  - On failure (re.error).
    - If pat.lower() belongs to low.
      - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L1694) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L439) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L420)

<a id="op-6eab7f9778722d"></a>
### Extract content

`operation_relationships_domain_enrichment_crawler_business_behavior_extract_content`

**Inputs** soup.

**Declared result** dict.

**Explicit results** mapping(“title” → title, “headings” → headings, “text” → text).

**Local steps**

- Set title from empty text.
- If (soup.title and soup.title.string).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in soup.title → soup.title.string.
  - Set title from soup.title.string.strip().
- Set headings from list().
- For each tag in soup.find\_all(list(“h1”, “h2”, “h3”)).
  - Set txt from tag.get\_text(one space, strip = true).
  - If txt.
    - Evaluate headings.append(txt).
- For each node in soup(list(“script”, “style”, “noscript”, “template”, …)).
  - Evaluate node.decompose().
- Set text from soup.get\_text(one space, strip = true).
- Set text from one space.join(text.split()).
- Return mapping(“title” → title, “headings” → headings, “text” → text).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L2088) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L438) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L419)

<a id="op-c1c29505887c8b"></a>
### Links on page

`operation_relationships_domain_enrichment_crawler_business_behavior_links_on_page`

**Inputs** soup, page\_url, base\_netloc, skip\_patterns.

**Local steps**

- For each a in soup.find\_all(“a”, href = true).
  - Set href from a at “href”.strip().
  - If (not href or any(generator of nested operand in the contract.lower().startswith(s) for s drawn from SKIP\_SCHEMES)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not href → any(generator of href.lower().startswith(s) for s drawn from SKIP\_SCHEMES).
    - Draw s from SKIP\_SCHEMES.
    - Continue with the next iteration or loop test.
  - Set absolute from normalize\_url(urljoin(page\_url, href)).
  - If not \_is\_crawlable(absolute, skip\_patterns).
    - Continue with the next iteration or loop test.
  - If not same\_site(absolute, base\_netloc).
    - Continue with the next iteration or loop test.
  - yield tuple(absolute, a.get\_text(one space, strip = true)).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L2543) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L441) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L422)

<a id="op-e59fd37eb72234"></a>
### Parse and fill

`operation_relationships_domain_enrichment_crawler_business_behavior_parse_and_fill`

**Inputs** page, html.

**Explicit results** soup.

**Local steps**

- Set soup from BeautifulSoup(html, “html.parser”).
- Set content from extract\_content(BeautifulSoup(html, “html.parser”)).
- Set page.title from content at “title”.
- Set page.headings from content at “headings”.
- Set page.text from content at “text”.
- Return soup.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L2910) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L445) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L426)

<a id="op-dcbd135622eb66"></a>
### Crawl page

`operation_relationships_domain_enrichment_crawler_business_behavior_crawl_page`

**Inputs** url, cfg, session = no value.

**Explicit results** tuple(page, soup).

**Local steps**

- Set tuple(status, html, error, final\_url) from fetch(url, cfg, session = session).
- Set page from CrawledPage(url = (final\_url or url), status\_code = status, html = (html or empty text), error = error).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in final\_url → url.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in html → empty text.
- Set soup from \_parse\_and\_fill(page, html) when (html and not error), otherwise no value.
  - Value choice on (html and not error) — true gives \_parse\_and\_fill(page, html), false gives no value.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in html → not error.
- Return tuple(page, soup).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L3104) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L436) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L417)

<a id="op-afdc71a98fd486"></a>
### Load robots

`operation_relationships_domain_enrichment_crawler_business_behavior_load_robots`

**Inputs** start\_url, cfg, session = no value.

**Explicit results** no value · rp.

**Local steps**

- Attempt the following.
  - Set parsed from urlparse(normalize\_url(start\_url)).
  - If not parsed.netloc.
    - Return no value.
  - Set robots\_url from formatted text {parsed.scheme}://{parsed.netloc}/robots.txt.
  - Set own from session is identical to no value.
  - Set session from (session or build\_session(cfg)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in session → build\_session(cfg).
  - Attempt the following.
    - Set tuple(status, body, error, \_final) from fetch(robots\_url, cfg, session = session, html\_only = false).
  - On exit, including pending return or failure.
    - If own.
      - Evaluate session.close().
  - If (error or status differs from 200 or not body).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in error → status differs from 200 → not body.
    - Return no value.
  - Set rp from RobotFileParser().
  - Evaluate rp.parse(body.splitlines()).
  - Return rp.
- On failure (Exception).
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L3360) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L442) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L423)

<a id="op-3da731c9065a62"></a>
### Robots allows

`operation_relationships_domain_enrichment_crawler_business_behavior_robots_allows`

**Inputs** robots, user\_agent, url.

**Explicit results** true · robots.can\_fetch((user\_agent or “\*”), url).

**Local steps**

- If robots is identical to no value.
  - Return true.
- Attempt the following.
  - Return robots.can\_fetch((user\_agent or “\*”), url).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in user\_agent → “\*”.
- On failure (Exception).
  - Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L3825) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L449) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L430)

<a id="op-2b3ea8b19e74f2"></a>
### Probe about pages

`operation_relationships_domain_enrichment_crawler_business_behavior_probe_about_pages`

**Inputs** home\_url, cfg, session = no value, skip\_urls = tuple().

**Explicit results** list(tuple(page, soup)) · list().

**Local steps**

- Set skip from set of normalize\_url(u) for u drawn from skip\_urls.
  - Draw u from skip\_urls.
- Set user\_agent from cfg.setting(“user\_agent”).
- Set own\_session from session is identical to no value.
- Set session from (session or build\_session(cfg)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in session → build\_session(cfg).
- Set robots from load\_robots(home\_url, cfg, session).
- Set home\_netloc from urlparse(home\_url).netloc.
- Attempt the following.
  - For each path in ABOUT\_PROBE\_PATHS.
    - Set url from normalize\_url(urljoin(home\_url, path)).
    - If url belongs to skip.
      - Continue with the next iteration or loop test.
    - Evaluate skip.add(url).
    - If not \_robots\_allows(robots, user\_agent, url).
      - Continue with the next iteration or loop test.
    - Set tuple(page, soup) from crawl\_page(url, cfg, session = session).
    - If (soup is distinct from no value and page.status\_code equals 200 and not page.error and same\_site(page.url, home\_netloc) and len(page.text) ≥ ABOUT\_MIN\_TEXT).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in soup is distinct from no value → page.status\_code equals 200 → not page.error → same\_site(page.url, home\_netloc) → len(page.text) ≥ ABOUT\_MIN\_TEXT.
      - Return list(tuple(page, soup)).
- On exit, including pending return or failure.
  - If own\_session.
    - Evaluate session.close().
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L2) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L447) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L428)

<a id="op-0c2fa51c8dc21d"></a>
### Local tag

`operation_relationships_domain_enrichment_crawler_business_behavior_local_tag`

**Inputs** tag.

**Declared result** str.

**Explicit results** tag.rsplit(“}”, 1) at negative 1 when tag, otherwise tag.

**Local steps**

- Return tag.rsplit(“}”, 1) at negative 1 when tag, otherwise tag.
  - Value choice on tag — true gives tag.rsplit(“}”, 1) at negative 1, false gives tag.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L4549) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L443) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L424)

<a id="op-670170531d927b"></a>
### Parse sitemap

`operation_relationships_domain_enrichment_crawler_business_behavior_parse_sitemap`

**Inputs** xml\_text.

**Explicit results** tuple(no value, list()) · tuple(kind, locs).

**Local steps**

- If “&lt;!doctype” belongs to xml\_text.lower().
  - Return tuple(no value, list()).
- Attempt the following.
  - Set root from ET.fromstring(xml\_text).
- On failure (ET.ParseError).
  - Return tuple(no value, list()).
- Set kind from \_local\_tag(root.tag).
- If kind does not belong to tuple(“urlset”, “sitemapindex”).
  - Return tuple(no value, list()).
- Set child\_tag from “sitemap” when kind equals “sitemapindex”, otherwise “url”.
  - Value choice on kind equals “sitemapindex” — true gives “sitemap”, false gives “url”.
- Set locs from list().
- For each el in root.
  - If \_local\_tag(el.tag) differs from child\_tag.
    - Continue with the next iteration or loop test.
  - For each child in el.
    - If (\_local\_tag(child.tag) equals “loc” and child.text).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_local\_tag(child.tag) equals “loc” → child.text.
      - Evaluate locs.append(child.text.strip()).
      - Leave the innermost loop without its normal-exhaustion alternative.
- Return tuple(kind, locs).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L4636) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L446) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L427)

<a id="op-0065380671dc49"></a>
### Discover sitemap urls

`operation_relationships_domain_enrichment_crawler_business_behavior_discover_sitemap_resource_addresses`

**Inputs** start\_url, cfg, session, robots.

**Explicit results** list() · urls.

**Local steps**

- Attempt the following.
  - Set parsed from urlparse(normalize\_url(start\_url)).
  - If not parsed.netloc.
    - Return list().
  - Set candidates from list().
  - If robots is distinct from no value.
    - Attempt the following.
      - Evaluate candidates.extend((robots.site\_maps() or list())).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in robots.site\_maps() → list().
    - On failure (Exception).
      - Take no action here.
  - If not candidates.
    - Evaluate candidates.append(formatted text {parsed.scheme}://{parsed.netloc}/sitemap.xml).
  - Set to\_fetch from deque(candidates at slice no value to SITEMAP\_MAX\_SITEMAPS).
  - Set sitemaps\_queued from len(to\_fetch).
  - Set fetched\_sitemaps from set().
  - Set urls from list().
  - Set seen\_urls from set().
  - While (to\_fetch and len(fetched\_sitemaps) &lt; SITEMAP\_MAX\_SITEMAPS and len(urls) &lt; SITEMAP\_MAX\_URLS).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in to\_fetch → len(fetched\_sitemaps) &lt; SITEMAP\_MAX\_SITEMAPS → len(urls) &lt; SITEMAP\_MAX\_URLS.
    - Set sitemap\_url from to\_fetch.popleft().
    - If sitemap\_url belongs to fetched\_sitemaps.
      - Continue with the next iteration or loop test.
    - Evaluate fetched\_sitemaps.add(sitemap\_url).
    - If not same\_site(sitemap\_url, parsed.netloc).
      - Continue with the next iteration or loop test.
    - Set tuple(status, body, error, \_final) from fetch(sitemap\_url, cfg, session = session, html\_only = false).
    - If (error or status differs from 200 or not body).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in error → status differs from 200 → not body.
      - Continue with the next iteration or loop test.
    - Set tuple(kind, locs) from \_parse\_sitemap(body).
    - If kind equals “sitemapindex”.
      - For each loc in locs.
        - If sitemaps\_queued ≥ SITEMAP\_MAX\_SITEMAPS.
          - Leave the innermost loop without its normal-exhaustion alternative.
        - Evaluate to\_fetch.append(loc).
        - Update sitemaps\_queued using + 1.
    - Otherwise.
      - If kind equals “urlset”.
        - For each loc in locs.
          - Set norm from normalize\_url(loc).
          - If norm belongs to seen\_urls.
            - Continue with the next iteration or loop test.
          - Evaluate seen\_urls.add(norm).
          - Evaluate urls.append(norm).
          - If len(urls) ≥ SITEMAP\_MAX\_URLS.
            - Leave the innermost loop without its normal-exhaustion alternative.
  - Return urls.
- On failure (Exception).
  - Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0018.json#L5102) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L437) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L418)

<a id="op-5f84ee76c9e969"></a>
### Crawl

`operation_relationships_domain_enrichment_crawler_business_behavior_crawl`

**Inputs** start\_url, cfg, session = no value, progress = no value.

**Explicit results** results.

**Local steps**

- Set max\_pages from int(cfg.setting(“max\_pages”)).
- Set max\_depth from int(cfg.setting(“max\_depth”)).
- Set link\_priority from cfg.link\_priority.
- Set skip\_patterns from cfg.skip\_patterns.
- Set user\_agent from cfg.setting(“user\_agent”).
- Set own\_session from session is identical to no value.
- Set session from (session or build\_session(cfg)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in session → build\_session(cfg).
- Set start\_url from normalize\_url(start\_url).
- Set base\_netloc from urlparse(start\_url).netloc.
- Set crawl\_beyond\_homepage from (max\_depth ≥ 1 and max\_pages &gt; 1).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in max\_depth ≥ 1 → max\_pages &gt; 1.
- Set robots from load\_robots(start\_url, cfg, session) when crawl\_beyond\_homepage, otherwise no value.
  - Value choice on crawl\_beyond\_homepage — true gives load\_robots(start\_url, cfg, session), false gives no value.
- Set visited from set().
- Set visited\_resolved from set().
- Set results from list().
- Set queue from deque(list(tuple(start\_url, 0, empty text))).
- If (crawl\_beyond\_homepage and cfg.setting(“use\_sitemap”, true)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in crawl\_beyond\_homepage → cfg.setting(“use\_sitemap”, true).
  - Set queued\_from\_sitemap from set().
  - For each loc in discover\_sitemap\_urls(start\_url, cfg, session, robots).
    - Set link from normalize\_url(loc).
    - If (link equals start\_url or link belongs to queued\_from\_sitemap).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in link equals start\_url → link belongs to queued\_from\_sitemap.
      - Continue with the next iteration or loop test.
    - If (not same\_site(link, base\_netloc) or not \_is\_crawlable(link, skip\_patterns)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in not same\_site(link, base\_netloc) → not \_is\_crawlable(link, skip\_patterns).
      - Continue with the next iteration or loop test.
    - If not \_robots\_allows(robots, user\_agent, link).
      - Continue with the next iteration or loop test.
    - Evaluate queued\_from\_sitemap.add(link).
    - Evaluate queue.append(tuple(link, 1, empty text)).
- Attempt the following.
  - While (queue and len(results) &lt; max\_pages).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in queue → len(results) &lt; max\_pages.
    - Set queue from deque(sorted(queue, key = deferred anonymous expression)).
    - Set tuple(url, depth, \_anchor) from queue.popleft().
    - Set url from normalize\_url(url).
    - If url belongs to visited.
      - Continue with the next iteration or loop test.
    - Evaluate visited.add(url).
    - If progress.
      - Evaluate progress(formatted text Crawling {url}).
    - Set tuple(page, soup) from crawl\_page(url, cfg, session = session).
    - Set resolved from normalize\_url(page.url) when page.url, otherwise empty text.
      - Value choice on page.url — true gives normalize\_url(page.url), false gives empty text.
    - If not results.
      - If resolved.
        - Set base\_netloc from (urlparse(page.url).netloc or base\_netloc).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in urlparse(page.url).netloc → base\_netloc.
    - Otherwise.
      - If (resolved and resolved belongs to visited\_resolved).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in resolved → resolved belongs to visited\_resolved.
        - Continue with the next iteration or loop test.
      - If (soup is distinct from no value and page.url and not same\_site(page.url, base\_netloc)).
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in soup is distinct from no value → page.url → not same\_site(page.url, base\_netloc).
        - Set page.error from (page.error or formatted text redirected off-site to {urlparse(page.url).netloc}).
          - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.error → formatted text redirected off-site to {urlparse(page.url).netloc}.
        - Set page.html from empty text.
        - Set page.text from empty text.
        - Set page.title from empty text.
        - Set page.headings from list().
        - Set soup from no value.
    - If resolved.
      - Evaluate visited\_resolved.add(resolved).
    - Evaluate results.append(tuple(page, soup)).
    - If (soup is identical to no value or depth ≥ max\_depth).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in soup is identical to no value → depth ≥ max\_depth.
      - Continue with the next iteration or loop test.
    - Set seen\_here from set().
    - For each tuple(link, anchor) in \_links\_on\_page(soup, page.url, base\_netloc, skip\_patterns).
      - If (link belongs to visited or link belongs to seen\_here).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in link belongs to visited → link belongs to seen\_here.
        - Continue with the next iteration or loop test.
      - If not \_robots\_allows(robots, user\_agent, link).
        - Continue with the next iteration or loop test.
      - Evaluate seen\_here.add(link).
      - Evaluate queue.append(tuple(link, (depth + 1), anchor)).
- On exit, including pending return or failure.
  - If own\_session.
    - Evaluate session.close().
- Return results.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L435) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L416)

## Record · Crm enrichment field mapping

<a id="op-4fc484765f360b"></a>
### CRMEnrichment Field Mapping.validate

`operation_relationships_domain_enrichment_record_definitions_customer_relationship_management_enrichment_field_mapping_business_behavior_customer_relationship_enrichment_field_mapping_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Target Doctype must be one of: {0}”.format(“, ”.join(ALLOWED\_TARGET\_DOCTYPES)) · validation helper — translated “{0} has no field {1}”.format(self.target\_doctype, self.target\_fieldname).

**Local steps**

- If self.target\_doctype does not belong to ALLOWED\_TARGET\_DOCTYPES.
  - Call the validation error handler Platform.throw(translated “Target Doctype must be one of: {0}”.format(“, ”.join(ALLOWED\_TARGET\_DOCTYPES))).
- If not Platform.get\_meta(self.target\_doctype).has\_field(self.target\_fieldname).
  - Call the validation error handler Platform.throw(translated “{0} has no field {1}”.format(self.target\_doctype, self.target\_fieldname)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L3094) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L517) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L498)

## Record · Crm enrichment rule

<a id="op-da214383c26a00"></a>
### Get target field

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_get_target_field`

**Inputs** rule\_type.

**Explicit results** “target\_value” when rule\_type equals “Social”, otherwise “industry”.

**Local steps**

- Return “target\_value” when rule\_type equals “Social”, otherwise “industry”.
  - Value choice on rule\_type equals “Social” — true gives “target\_value”, false gives “industry”.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L171) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L327) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L308)

<a id="op-3cc8771387b4ca"></a>
### Find duplicate

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_find_duplicate`

**Inputs** rule\_type, target, exclude = no value.

**Explicit results** query.limit(1).run(pluck = true).

**Local steps**

- Set field from get\_target\_field(rule\_type).
- Set Rule from Platform.qb.DocType(“CRM Enrichment Rule”).
- Set query from nested operand in the contract.qb.from\_(Rule).select(Rule.name).where((Rule.rule\_type equals rule\_type bitwise and Lower(Rule at field) equals target.lower())).
- If exclude.
  - Set query from query.where(Rule.name differs from exclude).
- Return query.limit(1).run(pluck = true).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L170) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L326) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L307)

<a id="op-d83268ed4f3e04"></a>
### CRMEnrichment Rule.before validate

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_crmenrichmentrule_before_validate`

**Inputs** self.

**Local steps**

- Set field from get\_target\_field(self.rule\_type).
- Set target from ((self.get(field) or empty text).strip() or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in (self.get(field) or empty text).strip() → no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.get(field) → empty text.
- If (target and self.rule\_type equals “Social”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in target → self.rule\_type equals “Social”.
  - Set target from target.lower().
- Evaluate self.set(field, target).
- Set self.rule\_name from formatted text {self.rule\_type}: {self.get\_target()}.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get target](operations-002.md#op-57080ed949e9f4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L164) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L320) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L301)

<a id="op-57080ed949e9f4"></a>
### CRMEnrichment Rule.get target

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_crmenrichmentrule_get_target`

**Inputs** self.

**Explicit results** self.get(get\_target\_field(self.rule\_type)).

**Local steps**

- Return self.get(get\_target\_field(self.rule\_type)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L165) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L321) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L302)

<a id="op-9ee110bac1dc50"></a>
### CRMEnrichment Rule.validate

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_crmenrichmentrule_validate`

**Inputs** self.

**Local steps**

- Evaluate self.validate\_target().
- Evaluate self.validate\_duplicate().
- Evaluate self.validate\_patterns().

If control reaches the end, it returns no value.

**Methods declared on this owner** [validate target](operations-002.md#op-687ee6a16285a7), [validate duplicate](operations-003.md#op-afe963a9291a76), [validate patterns](operations-003.md#op-4fcc6a7287516f).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L166) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L322) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L303)

<a id="op-687ee6a16285a7"></a>
### CRMEnrichment Rule.validate target

`operation_relationships_binding_crm_domain_enrichment_doctype_crm_enrichment_rule_crm_enrichment_rule_crmenrichmentrule_validate_target`

**Inputs** self.

**Explicit failure paths** validation helper — translated “{0} is required for {1} rules”.format(label, translated self.rule\_type).

**Local steps**

- If not self.get\_target().
  - Set label from translated “Target Value” when self.rule\_type equals “Social”, otherwise translated “Industry”.
    - Value choice on self.rule\_type equals “Social” — true gives translated “Target Value”, false gives translated “Industry”.
  - Call the validation error handler Platform.throw(translated “{0} is required for {1} rules”.format(label, translated self.rule\_type)).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get target](operations-002.md#op-57080ed949e9f4).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0001.json#L169) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L325) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L306)
