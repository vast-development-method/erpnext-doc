# Company enrichment · operations 4

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Extractors

<a id="op-9fc567f75b903d"></a>
### Extract logo

`operation_relationships_domain_enrichment_extractors_business_behavior_extract_logo`

**Inputs** soup, base\_url.

**Explicit results** Field(icon\_url, base\_url, Method.FAVICON) · Field(formatted text {parsed.scheme}://{parsed.netloc}/favicon.ico, base\_url, Method.FAVICON) · Field().

**Local steps**

- Set icon\_url from \_best\_icon(soup, base\_url).
- If icon\_url.
  - Return Field(icon\_url, base\_url, Method.FAVICON).
- Set parsed from urlparse(base\_url).
- If (parsed.scheme and parsed.netloc).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in parsed.scheme → parsed.netloc.
  - Return Field(formatted text {parsed.scheme}://{parsed.netloc}/favicon.ico, base\_url, Method.FAVICON).
- Return Field().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0019.json#L7515) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L469) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L450)

<a id="op-108ed332162361"></a>
### Extract image

`operation_relationships_domain_enrichment_extractors_business_behavior_extract_image`

**Inputs** soup, base\_url.

**Explicit results** Field(safe, base\_url, Method.JSON\_LD) · Field(safe, base\_url, Method.META\_TAG) · Field().

**Local steps**

- For each block in parse\_json\_ld(soup).
  - If not \_ld\_type\_matches(block, \_ORG\_TYPES).
    - Continue with the next iteration or loop test.
  - Set logo from block.get(“logo”).
  - Set url from logo.get(“url”) when isinstance(logo, dict), otherwise logo when isinstance(logo, str), otherwise empty text.
    - Value choice on isinstance(logo, dict) — true gives logo.get(“url”), false gives logo when isinstance(logo, str), otherwise empty text.
    - Value choice on isinstance(logo, str) — true gives logo, false gives empty text.
  - Set safe from \_safe\_url(base\_url, url).
  - If safe.
    - Return Field(safe, base\_url, Method.JSON\_LD).
- Set tuple(og\_content, \_name) from \_meta\_with\_method(soup, “og:image”, “og:image:url”, “twitter:image”).
- Set safe from \_safe\_url(base\_url, og\_content).
- If safe.
  - Return Field(safe, base\_url, Method.META\_TAG).
- Return Field().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L468) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L449)

<a id="op-63c23b57322ace"></a>
### Last path segment

`operation_relationships_domain_enrichment_extractors_business_behavior_last_path_segment`

**Inputs** url.

**Explicit results** path.rsplit(“/”, 1) at negative 1.lower() when path, otherwise empty text.

**Local steps**

- Set path from urlparse(url).path.rstrip(“/”).
- Return path.rsplit(“/”, 1) at negative 1.lower() when path, otherwise empty text.
  - Value choice on path — true gives path.rsplit(“/”, 1) at negative 1.lower(), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L433) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L476) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L457)

<a id="op-fcae59746dea42"></a>
### Is about page

`operation_relationships_domain_enrichment_extractors_business_behavior_is_about_page`

**Inputs** url.

**Explicit results** false · bool(\_ABOUT\_SEGMENT\_RE.match(seg)).

**Local steps**

- Set seg from \_last\_path\_segment(url).
- If (not seg or any(generator of w belongs to seg for w drawn from \_NON\_ABOUT\_WORDS)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not seg → any(generator of w belongs to seg for w drawn from \_NON\_ABOUT\_WORDS).
  - Draw w from \_NON\_ABOUT\_WORDS.
  - Return false.
- Return bool(\_ABOUT\_SEGMENT\_RE.match(seg)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L569) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L473) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L454)

<a id="op-d728be9e403c38"></a>
### Extract company info

`operation_relationships_domain_enrichment_extractors_business_behavior_extract_company_info`

**Inputs** homepage, soup.

**Explicit results** info.

**Local steps**

- Set url from homepage.url.
- Set info from mapping(“company\_name” → Field(), “description” → Field(), “logo” → Field(), “image” → Field(), …).
- For each block in parse\_json\_ld(soup).
  - If not \_ld\_type\_matches(block, \_ORG\_TYPES).
    - Continue with the next iteration or loop test.
  - If (not info at “company\_name”.value and block.get(“name”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not info at “company\_name”.value → block.get(“name”).
    - Set info at “company\_name” from Field(block at “name”.strip(), url, Method.JSON\_LD).
  - If (not info at “description”.value and block.get(“description”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not info at “description”.value → block.get(“description”).
    - Set info at “description” from Field(block at “description”.strip(), url, Method.JSON\_LD).
  - Set same\_as from block.get(“sameAs”).
  - If isinstance(same\_as, list).
    - Evaluate info at “social\_links”.extend(list of s for s drawn from same\_as where isinstance(s, str)).
      - Draw s from same\_as, keep a combination only if (isinstance(s, str)).
  - Otherwise.
    - If isinstance(same\_as, str).
      - Evaluate info at “social\_links”.append(same\_as).
  - Leave the innermost loop without its normal-exhaustion alternative.
- If not info at “company\_name”.value.
  - Set tuple(content, \_name) from \_meta\_with\_method(soup, “og:site\_name”, “og:title”).
  - If content.
    - Set info at “company\_name” from Field(\_clean\_company\_name(content, url), url, Method.META\_TAG).
  - Otherwise.
    - If homepage.title.
      - Set info at “company\_name” from Field(\_clean\_company\_name(homepage.title, url), url, Method.TITLE\_TAG).
- If not info at “description”.value.
  - Set content from \_meta\_description(soup).
  - If content.
    - Set info at “description” from Field(content, url, Method.META\_TAG).
- Set info at “logo” from extract\_logo(soup, url).
- Set info at “image” from extract\_image(soup, url).
- Return info.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L736) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L466) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L447)

<a id="op-ecd1e427eb02c2"></a>
### Company name hits

`operation_relationships_domain_enrichment_extractors_business_behavior_company_name_hits`

**Inputs** text, company\_name.

**Explicit results** 0 · len(re.findall(formatted text \\b{re.escape(name)}\\b, text, re.IGNORECASE)).

**Local steps**

- Set name from (company\_name or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in company\_name → empty text.
- If not name.
  - Return 0.
- Return len(re.findall(formatted text \\b{re.escape(name)}\\b, text, re.IGNORECASE)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L1855) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L462) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L443)

<a id="op-78f31a8146da7a"></a>
### Is staff profile

`operation_relationships_domain_enrichment_extractors_business_behavior_is_staff_profile`

**Inputs** text.

**Explicit results** true · false · (pronouns ≥ 2 or (pronouns ≥ 1 and bool(\_TITLE\_RE.search(text)))).

**Local steps**

- If \_CAREER\_RE.search(text).
  - Return true.
- If \_FIRST\_PERSON\_RE.search(text).
  - Return false.
- Set pronouns from len(\_PRONOUN\_RE.findall(text)).
- Return (pronouns ≥ 2 or (pronouns ≥ 1 and bool(\_TITLE\_RE.search(text)))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in pronouns ≥ 2 → (pronouns ≥ 1 and bool(\_TITLE\_RE.search(text))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pronouns ≥ 1 → bool(\_TITLE\_RE.search(text)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L2031) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L475) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L456)

<a id="op-84a0a06d0e42c1"></a>
### Describes company

`operation_relationships_domain_enrichment_extractors_business_behavior_describes_company`

**Inputs** text, company\_name.

**Explicit results** (bool(\_FIRST\_PERSON\_RE.search(text)) or \_company\_name\_hits(text, company\_name) &gt; 0).

**Local steps**

- Return (bool(\_FIRST\_PERSON\_RE.search(text)) or \_company\_name\_hits(text, company\_name) &gt; 0).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bool(\_FIRST\_PERSON\_RE.search(text)) → \_company\_name\_hits(text, company\_name) &gt; 0.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L2248) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L463) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L444)

<a id="op-ce62aea8e99a6e"></a>
### First paragraph

`operation_relationships_domain_enrichment_extractors_business_behavior_first_paragraph`

**Inputs** soup, industry\_rules = no value, company\_name = empty text.

**Explicit results** empty text · max(candidates, key = deferred anonymous expression).

**Local steps**

- Set candidates from list().
- For each p in soup.find\_all(“p”).
  - If any(generator of parent.name belongs to \_NON\_CONTENT\_PARENTS for parent drawn from p.parents).
    - Draw parent from p.parents.
    - Continue with the next iteration or loop test.
  - Set text from one space.join((p.get\_text(one space) or empty text).split()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in p.get\_text(one space) → empty text.
  - If (len(text) &lt; \_MIN\_PARAGRAPH\_LEN or one space does not belong to text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in len(text) &lt; \_MIN\_PARAGRAPH\_LEN → one space does not belong to text.
    - Continue with the next iteration or loop test.
  - Evaluate candidates.append(text).
  - If len(candidates) ≥ \_MAX\_PARAGRAPHS\_SCANNED.
    - Leave the innermost loop without its normal-exhaustion alternative.
- If not candidates.
  - Return empty text.
- Set candidates from (list of text for text drawn from candidates where not (\_is\_staff\_profile(text) or \_CTA\_RE.match(text)) or candidates).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in list of text for text drawn from candidates where not (\_is\_staff\_profile(text) or \_CTA\_RE.match(text)) → candidates.
  - Draw text from candidates, keep a combination only if (not (\_is\_staff\_profile(text) or \_CTA\_RE.match(text))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_is\_staff\_profile(text) → \_CTA\_RE.match(text).
- Return max(candidates, key = deferred anonymous expression).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L2362) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L472) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L453)

<a id="op-d4e5e92a5b2e7b"></a>
### Select description

`operation_relationships_domain_enrichment_extractors_business_behavior_select_description`

**Inputs** pages, soups\_by\_url, industry\_rules = no value, company\_name = empty text.

**Explicit results** (best\_field or Field()).

**Local steps**

- Set home\_url from pages at 0.url when pages, otherwise empty text.
  - Value choice on pages — true gives pages at 0.url, false gives empty text.
- Set best\_key from no value.
- Set best\_field from no value.
- Bind local operation consider for subsequent calls.
- For each page in pages.
  - Set soup from soups\_by\_url.get(page.url).
  - If soup is identical to no value.
    - Continue with the next iteration or loop test.
  - Set is\_home from page.url equals home\_url.
  - Set is\_about from \_is\_about\_page(page.url).
  - For each block in parse\_json\_ld(soup).
    - If (\_ld\_type\_matches(block, \_ORG\_TYPES) and block.get(“description”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_ld\_type\_matches(block, \_ORG\_TYPES) → block.get(“description”).
      - Evaluate consider(Field(block at “description”.strip(), page.url, Method.JSON\_LD), 6).
      - Leave the innermost loop without its normal-exhaustion alternative.
  - If is\_about.
    - Evaluate consider(Field(first\_paragraph(soup, industry\_rules, company\_name), page.url, Method.BODY\_TEXT), 5).
  - If (is\_home or is\_about).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in is\_home → is\_about.
    - Set content from \_meta\_description(soup).
    - If content.
      - Set score from 2 when (is\_home and \_COMMERCE\_RE.search(content)), otherwise 4.
        - Value choice on (is\_home and \_COMMERCE\_RE.search(content)) — true gives 2, false gives 4.
        - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_home → \_COMMERCE\_RE.search(content).
      - Evaluate consider(Field(content, page.url, Method.META\_TAG), score).
  - If is\_home.
    - Evaluate consider(Field(first\_paragraph(soup, industry\_rules, company\_name), page.url, Method.BODY\_TEXT), 1).
- Return (best\_field or Field()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in best\_field → Field().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L2965) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L482) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L463)

<a id="op-59ddd558678e93"></a>
### Select description.consider

`operation_relationships_domain_enrichment_extractors_business_behavior_select_description_consider`

**Inputs** field\_obj, score.

**Explicit results** no value.

**Local steps**

- Use enclosing bindings best\_key, best\_field.
- If not field\_obj.value.
  - Return no value.
- Set key from tuple(score, min(len(field\_obj.value), 300)).
- If (best\_key is identical to no value or key &gt; best\_key).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in best\_key is identical to no value → key &gt; best\_key.
  - Set tuple(best\_key, best\_field) from tuple(key, field\_obj).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L3913) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L483) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L464)

<a id="op-8c82dd6902b61e"></a>
### Clean email

`operation_relationships_domain_enrichment_extractors_business_behavior_clean_email`

**Inputs** email.

**Explicit results** no value · email.

**Local steps**

- Set email from email.strip().strip(“.”).lower().
- If any(generator of b belongs to email for b drawn from EMAIL\_BLOCKLIST\_SUBSTR).
  - Draw b from EMAIL\_BLOCKLIST\_SUBSTR.
  - Return no value.
- Return email.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L4111) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L460) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L441)

<a id="op-a72b3632fb0514"></a>
### Extract emails

`operation_relationships_domain_enrichment_extractors_business_behavior_extract_emails`

**Inputs** pages.

**Explicit results** list(found.values()).

**Local steps**

- Set found from mapping().
- For each page in pages.
  - If not page.html.
    - Continue with the next iteration or loop test.
  - For each match in EMAIL\_RE.findall(page.html).
    - Set cleaned from \_clean\_email(match).
    - If (cleaned and cleaned does not belong to found).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in cleaned → cleaned does not belong to found.
      - Set found at cleaned from Email(value = cleaned, source = page.url).
- Return list(found.values()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L4258) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L467) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L448)

<a id="op-a0b8213106c71d"></a>
### Valid phone

`operation_relationships_domain_enrichment_extractors_business_behavior_valid_phone`

**Inputs** raw.

**Explicit results** false · 7 ≤ len(digits) ≤ 15.

**Local steps**

- If not raw.strip().startswith(“+”).
  - Return false.
- Set digits from re.sub(“\\D”, empty text, raw).
- Return 7 ≤ len(digits) ≤ 15.
  - Compare adjacent operands in order, stopping at the first false comparison in 7 ≤ len(digits) ≤ 15.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L4517) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L484) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L465)

<a id="op-c3222501bfb18b"></a>
### Extract phones

`operation_relationships_domain_enrichment_extractors_business_behavior_extract_phones`

**Inputs** pages.

**Explicit results** list(found.values()).

**Local steps**

- Set found from mapping().
- For each page in pages.
  - If not page.html.
    - Continue with the next iteration or loop test.
  - For each m in re.findall(“tel:(&#91;+0-9()\\s.\\-&#93;{7,})”, page.html).
    - Set raw from m.strip().
    - Set digits from re.sub(“\\D”, empty text, raw).
    - If (\_valid\_phone(raw) and digits does not belong to found).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_valid\_phone(raw) → digits does not belong to found.
      - Set found at digits from Phone(value = (“+” + digits) when raw.strip().startswith(“+”), otherwise digits, raw = raw, source = page.url, method = Method.TEL\_LINK).
        - Value choice on raw.strip().startswith(“+”) — true gives (“+” + digits), false gives digits.
  - For each match in PHONE\_RE.finditer((page.text or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in page.text → empty text.
    - Set raw from match.group(0).strip().
    - If not raw.
      - Continue with the next iteration or loop test.
    - Set digits from re.sub(“\\D”, empty text, raw).
    - If (\_valid\_phone(raw) and digits does not belong to found).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in \_valid\_phone(raw) → digits does not belong to found.
      - Set value from (“+” + digits) when raw.startswith(“+”), otherwise digits.
        - Value choice on raw.startswith(“+”) — true gives (“+” + digits), false gives digits.
      - Set found at digits from Phone(value = value, raw = raw, source = page.url, method = Method.REGEX).
- Return list(found.values()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L4671) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L470) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L451)

<a id="op-8b665fc95a8fc5"></a>
### Extract social profiles

`operation_relationships_domain_enrichment_extractors_business_behavior_extract_social_profiles`

**Inputs** pages, soups\_by\_url, social\_rules, extra\_links = no value.

**Explicit results** profiles.

**Local steps**

- Set profiles from mapping of rule.target\_value → SocialProfile() for rule drawn from social\_rules.
  - Draw rule from social\_rules.
- Set home\_url from pages at 0.url when pages, otherwise empty text.
  - Value choice on pages — true gives pages at 0.url, false gives empty text.
- Set candidates from list of tuple(link, home\_url, Method.JSON\_LD) for link drawn from (extra\_links or list()).
  - Draw link from (extra\_links or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in extra\_links → list().
- For each page in pages.
  - Set soup from soups\_by\_url.get(page.url).
  - If soup is identical to no value.
    - Continue with the next iteration or loop test.
  - For each a in soup.find\_all(“a”, href = true).
    - Evaluate candidates.append(tuple(a at “href”.strip(), page.url, Method.SOCIAL\_RULE)).
- For each tuple(href, source, method) in candidates.
  - If (not href or SOCIAL\_NEGATIVE.search(href)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not href → SOCIAL\_NEGATIVE.search(href).
    - Continue with the next iteration or loop test.
  - Set url from urljoin(source, href.strip()).
  - For each rule in social\_rules.
    - Set network from rule.target\_value.
    - If profiles at network.value.
      - Continue with the next iteration or loop test.
    - If any(generator of rx.search(url) for tuple(rx, \_raw) drawn from rule.patterns).
      - Draw tuple(rx, \_raw) from rule.patterns.
      - Set profiles at network from SocialProfile(value = url, source = source, method = method).
- Return profiles.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L5352) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L471) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L452)

<a id="op-604d7e42192614"></a>
### Classify industry

`operation_relationships_domain_enrichment_extractors_business_behavior_classify_industry`

**Inputs** pages, company\_info, industry\_rules.

**Explicit results** tuple(empty text, 0.0) · tuple(best, round(confidence, 2)).

**Local steps**

- If not industry\_rules.
  - Return tuple(empty text, 0.0).
- Bind local operation \_val for subsequent calls.
- Set headline\_parts from list(\_val(“company\_name”), \_val(“description”)).
- If pages.
  - Set home from pages at 0.
  - Evaluate headline\_parts.append((home.title or empty text)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in home.title → empty text.
  - Evaluate headline\_parts.append(one space.join(home.headings)).
  - Set about from next(generator of p for p drawn from pages at slice 1 to no value where \_is\_about\_page(p.url), no value).
    - Draw p from pages at slice 1 to no value, keep a combination only if (\_is\_about\_page(p.url)).
  - If about.
    - Evaluate headline\_parts.append((about.title or empty text)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in about.title → empty text.
    - Evaluate headline\_parts.append(one space.join(about.headings)).
- Set headline from one space.join(generator of p for p drawn from headline\_parts where p).lower().
  - Draw p from headline\_parts, keep a combination only if (p).
- Set text\_by\_scope from mapping(SCOPE\_HEADLINE → headline, SCOPE\_FULL\_TEXT → one space.join(generator of (nested operand in the contract.text or empty text) for p drawn from pages).lower(), SCOPE\_HTML → one space.join(generator o ….
  - Draw p from pages.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in p.text → empty text.
  - Draw p from pages.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in p.html → empty text.
  - Draw p from pages, keep a combination only if ((p.url and not p.error)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in p.url → not p.error.
- Set scores from apply\_keyword\_rules(text\_by\_scope, industry\_rules).
- Set total from sum(scores.values()).
- If not total.
  - Return tuple(empty text, 0.0).
- Set best from max(scores, key = scores.get).
- If scores at best &lt; INDUSTRY\_MIN\_SCORE.
  - Return tuple(empty text, 0.0).
- Set confidence from (scores at best ÷ total).
- If confidence &lt; INDUSTRY\_MIN\_CONFIDENCE.
  - Return tuple(empty text, 0.0).
- Return tuple(best, round(confidence, 2)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/relationships/procedures-0002.json#L4) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L457) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L438)

<a id="op-b1d04c97ac0136"></a>
### Classify industry.val

`operation_relationships_domain_enrichment_extractors_business_behavior_classify_industry_val`

**Inputs** key.

**Explicit results** (getattr(f, “value”, f) or empty text).

**Local steps**

- Set f from company\_info.get(key).
- Return (getattr(f, “value”, f) or empty text).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(f, “value”, f) → empty text.

**Values supplied outside this operation** selected callable from getattr(f, “value”, f).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L6980) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L458) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L439)

## Service · Http

<a id="op-4dece8e6b24d33"></a>
### Domain in list

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_domain_in_list`

**Inputs** host, domains.

**Declared result** bool.

**Explicit results** true · false.

**Local steps**

- Set host from nested operand in the contract.lower().split(“:”) at 0.rstrip(“.”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in host → empty text.
- For each d in domains.
  - Set d from (nested operand in the contract or nested operand in the contract).lower().strip().rstrip(“.”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in d → empty text.
  - If not d.
    - Continue with the next iteration or loop test.
  - If (host equals d or host.endswith((“.” + d))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in host equals d → host.endswith((“.” + d)).
    - Return true.
- Return false.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L7082) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L486) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L467)

<a id="op-a21076bb694df8"></a>
### Is blocked ip

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_is_blocked_internet_protocol`

**Inputs** ip.

**Declared result** bool.

**Explicit results** true · (not addr.is\_global or addr.is\_multicast).

**Local steps**

- Attempt the following.
  - Set addr from ipaddress.ip\_address(ip).
- On failure (ValueError).
  - Return true.
- Return (not addr.is\_global or addr.is\_multicast).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not addr.is\_global → addr.is\_multicast.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L7366) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L488) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L469)

<a id="op-4d0478d3d54e71"></a>
### Resolve ips

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_resolve_ips`

**Inputs** host.

**Declared result** list.

**Explicit results** list(set of info at 4 at 0 for info drawn from infos).

**Local steps**

- Set infos from socket.getaddrinfo(host, no value).
- Return list(set of info at 4 at 0 for info drawn from infos).
  - Draw info from infos.

**Values supplied outside this operation** service or queued work from socket.getaddrinfo(host, no value).

**Boundaries to resolve** external or queued work, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L7489) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L494) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L475)

<a id="op-92592205e77aaa"></a>
### Validate url

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_validate_resource_address`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** url, cfg.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0020.json#L7610) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L497) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L478)

<a id="op-8316a7fbdb34d4"></a>
### Validated ips

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_validated_ips`

**Inputs** url, cfg.

**Declared result** list.

**Explicit results** sorted(ips, key = deferred anonymous expression).

**Explicit failure paths** SSRFError(formatted text unsupported URL scheme: {(parsed.scheme or “(none)”)}) · SSRFError(“URL has no host”) · SSRFError(formatted text host is on the blocked-domains list: {host}) · SSRFError(formatted text host is not on the allowed-domains list: {host}) · SSRFError(formatted text could not resolve host {host}: {exc}) · 2 additional forms in the steps below.

**Local steps**

- Set parsed from urlparse(url).
- If parsed.scheme does not belong to tuple(“http”, “https”).
  - Raise SSRFError(formatted text unsupported URL scheme: {(parsed.scheme or “(none)”)}).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.scheme → “(none)”.
- Set host from (parsed.hostname or empty text).strip().rstrip(“.”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in parsed.hostname → empty text.
- If not host.
  - Raise SSRFError(“URL has no host”).
- Set blocked from cfg.blocked\_domains when cfg, otherwise list().
  - Value choice on cfg — true gives cfg.blocked\_domains, false gives list().
- Set allowed from cfg.allowed\_domains when cfg, otherwise list().
  - Value choice on cfg — true gives cfg.allowed\_domains, false gives list().
- If \_domain\_in\_list(host, blocked).
  - Raise SSRFError(formatted text host is on the blocked-domains list: {host}).
- If (allowed and not \_domain\_in\_list(host, allowed)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in allowed → not \_domain\_in\_list(host, allowed).
  - Raise SSRFError(formatted text host is not on the allowed-domains list: {host}).
- Attempt the following.
  - Set ips from \_resolve\_ips(host).
- On failure (socket.gaierror) bound to exc.
  - Raise SSRFError(formatted text could not resolve host {host}: {exc}) with cause exc.
- If not ips.
  - Raise SSRFError(formatted text could not resolve host {host}).
- For each ip in ips.
  - If \_is\_blocked\_ip(ip).
    - Raise SSRFError(formatted text host {host} resolves to a non-public address: {ip}).
- Return sorted(ips, key = deferred anonymous expression).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L6) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L498) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L479)

<a id="op-00c1d94f9589c7"></a>
### Build session

`operation_relationships_domain_enrichment_hypertext_transfer_business_behavior_build_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** cfg.

**Explicit result forms** a value selected from the current context.

**Local structure** 2 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../relationships-decision-contracts/part-0021.json#L774) · [Binding](../../../current-decisions/relationships/bindings-001.tsv#L485) · [Declaration location](../../../current-decisions/relationships/evidence/locations-001.tsv#L466)
