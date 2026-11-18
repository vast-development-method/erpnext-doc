# Shared value and file services · operations 17

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Data

<a id="op-e6f5e0dcc1fedf"></a>
### Filter strip join

`operation_foundation_utils_data_business_behavior_filter_strip_join`

**Inputs** some\_list, sep.

**Declared result** list at str.

**Explicit results** cstr(sep).join(generator of cstr(a).strip() for a drawn from filter(no value, some\_list)).

**Local steps**

- Return cstr(sep).join(generator of cstr(a).strip() for a drawn from filter(no value, some\_list)).
  - Draw a from filter(no value, some\_list).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L5908) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1119) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1678)

<a id="op-772db7b5add24f"></a>
### Get url

`operation_foundation_utils_data_business_behavior_get_resource_address`

**Inputs** uri = no value, full\_address = false, allow\_header\_override = true.

**Declared result** str.

**Record and data access** read “Website Settings” via get\_single\_value.

**Explicit results** uri · urljoin(host\_name, uri) when uri, otherwise host\_name.

**Local steps**

- Set host\_name from (Platform.local.conf.host\_name or Platform.local.conf.hostname).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.conf.host\_name → Platform.local.conf.hostname.
- If (uri and (uri.startswith(text in the contract) or uri.startswith(text in the contract))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in uri → (uri.startswith(text in the contract) or uri.startswith(text in the contract)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in uri.startswith(text in the contract) → uri.startswith(text in the contract).
  - Return uri.
- If not host\_name.
  - Set request\_host\_name from get\_host\_name\_from\_request().
  - If (request\_host\_name and allow\_header\_override).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in request\_host\_name → allow\_header\_override.
    - Set host\_name from request\_host\_name.
  - Otherwise.
    - If Platform.local.site.
      - Set protocol from text in the contract.
      - If Platform.local.conf.ssl\_certificate.
        - Set protocol from text in the contract.
      - Otherwise.
        - If Platform.local.conf.wildcard.
          - Set domain from Platform.local.conf.wildcard.get(“domain”).
          - If (domain and Platform.local.site.endswith(domain) and Platform.local.conf.wildcard.get(“ssl\_certificate”)).
            - Evaluate in order, stop at the first false operand, otherwise use the last operand in domain → Platform.local.site.endswith(domain) → Platform.local.conf.wildcard.get(“ssl\_certificate”).
            - Set protocol from text in the contract.
      - Set host\_name from (protocol + Platform.local.site).
    - Otherwise.
      - Set host\_name from Platform.db.get\_single\_value(“Website Settings”, “subdomain”).
      - If not host\_name.
        - Set host\_name from text in the contract.
- If (host\_name and not host\_name.startswith(text in the contract) and not host\_name.startswith(text in the contract)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in host\_name → not host\_name.startswith(text in the contract) → not host\_name.startswith(text in the contract).
  - Set host\_name from (text in the contract + host\_name).
- If (not uri and full\_address).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not uri → full\_address.
  - Set uri from Platform.get\_request\_header(“REQUEST\_URI”, empty text).
- Set port from Platform.conf.http\_port.
- If (not port and Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not port → Platform.conf.developer\_mode.
  - Set port from Platform.conf.webserver\_port.
- If (not Platform.conf.restart\_supervisor\_on\_update and not Platform.conf.restart\_systemd\_on\_update and host\_name and not url\_contains\_port(host\_name) and port).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.restart\_supervisor\_on\_update → not Platform.conf.restart\_systemd\_on\_update → host\_name → not url\_contains\_port(host\_name) → port.
  - Set host\_name from ((host\_name + “:”) + str(port)).
- Return urljoin(host\_name, uri) when uri, otherwise host\_name.
  - Value choice on uri — true gives urljoin(host\_name, uri), false gives host\_name.

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“Website Settings”, “subdomain”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L6073) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1723)

<a id="op-504a71bb808348"></a>
### Get request host

`operation_foundation_binding_foundation_utils_data_get_request_host`

**Inputs** request.

**Declared result** str.

**Explicit results** (request.host or request.headers.get(“Host”, empty text)).

**Local steps**

- Return (request.host or request.headers.get(“Host”, empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in request.host → request.headers.get(“Host”, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L54) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L124) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L212)

<a id="op-11a6e761430a7c"></a>
### Get host name from request

`operation_foundation_utils_data_business_behavior_get_host_name_from_request`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** (protocol + host).

**Local steps**

- If (hasattr(Platform.local, “request”) and Platform.local.request and host bound to get\_request\_host(Platform.local.request)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in hasattr(Platform.local, “request”) → Platform.local.request → host bound to get\_request\_host(Platform.local.request).
  - Set protocol from text in the contract when “https” equals Platform.get\_request\_header(“X-Forwarded-Proto”, empty text), otherwise text in the contract.
    - Value choice on “https” equals Platform.get\_request\_header(“X-Forwarded-Proto”, empty text) — true gives text in the contract, false gives text in the contract.
  - Return (protocol + host).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L91) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1146) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1705)

<a id="op-aa080f7e87a4a9"></a>
### Url contains port

`operation_foundation_utils_data_business_behavior_resource_address_contains_port`

**Inputs** url.

**Declared result** bool.

**Explicit results** len(parts) &gt; 2.

**Local steps**

- Set parts from url.split(“:”).
- Return len(parts) &gt; 2.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L7208) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1234) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L35)

<a id="op-f6564754e3797f"></a>
### Get host name

`operation_foundation_utils_data_business_behavior_get_host_name`

**Inputs** no declared parameters.

**Declared result** str.

**Explicit results** get\_url().rsplit(“//”, 1) at negative 1.

**Local steps**

- Return get\_url().rsplit(“//”, 1) at negative 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L7306) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1145) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1704)

<a id="op-34622949459c1b"></a>
### Get link to form

`operation_foundation_utils_data_business_behavior_get_link_to_form`

**Inputs** doctype, name = no value, label = no value.

**Declared result** str.

**Explicit results** formatted text &lt;a href="{get\_url\_to\_form(doctype, name)}"&gt;{label}&lt;/a&gt;.

**Local steps**

- Bind dependencies \_.
- If not label.
  - Set label from (name or translated doctype).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in name → translated doctype.
- Return formatted text &lt;a href="{get\_url\_to\_form(doctype, name)}"&gt;{label}&lt;/a&gt;.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L7379) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1713)

<a id="op-60663059b95250"></a>
### Get url to workspace

`operation_foundation_utils_data_business_behavior_get_resource_address_to_workspace`

**Inputs** workspace, is\_public.

**Explicit results** (url\_prefix + slug(workspace)).

**Local steps**

- Bind dependencies slug.
- Set url\_prefix from “/desk/” when is\_public, otherwise “/desk/private/”.
  - Value choice on is\_public — true gives “/desk/”, false gives “/desk/private/”.
- Return (url\_prefix + slug(workspace)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0475.json#L7583) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1169) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1728)

<a id="op-b65cce001f5b51"></a>
### Get link to report

`operation_foundation_utils_data_business_behavior_get_link_to_report`

**Inputs** name, label = no value, report\_type = no value, doctype = no value, filters = no value.

**Declared result** str.

**Explicit results** text in the contract.format(get\_url\_to\_report\_with\_filters(name, filters, report\_type, doctype), label) · formatted text &lt;a href='{get\_url\_to\_report(name, report\_type, doctype)}'&gt;{label}&lt;/a&gt;.

**Local steps**

- Bind dependencies \_.
- If not label.
  - Set label from translated name.
- If filters.
  - Set conditions from list().
  - For each tuple(k, v) in filters.items().
    - If isinstance(v, list).
      - For each value in v.
        - If value at 0 equals “between”.
          - Evaluate conditions.append(((((((nested operand in the contract + nested operand in the contract) + “",&#91;"”) + str(nested operand in the contract at nested operand in the contract)) + “","”) + str(value at 1 at 1)) + “"&#93;&#93;”)).
        - Otherwise.
          - Evaluate conditions.append((((str(k) + “=”) + “&#91;"”) + str(((((nested operand in the contract + nested operand in the contract) + “"”) + str(nested operand in the contract at nested operand in the contract)) + “"&#93;”)))).
    - Otherwise.
      - Evaluate conditions.append(((str(k) + “=”) + quote(str(v)))).
  - Set filters from “&amp;”.join(conditions).
  - Return text in the contract.format(get\_url\_to\_report\_with\_filters(name, filters, report\_type, doctype), label).
- Otherwise.
  - Return formatted text &lt;a href='{get\_url\_to\_report(name, report\_type, doctype)}'&gt;{label}&lt;/a&gt;.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1714)

<a id="op-fcaeedd5476c57"></a>
### Get absolute url

`operation_foundation_utils_data_business_behavior_get_absolute_resource_address`

**Inputs** doctype, name.

**Declared result** str.

**Explicit results** formatted text /desk/{quoted(slug(doctype))}/{quote(cstr(name), safe = empty text)}.

**Local steps**

- Return formatted text /desk/{quoted(slug(doctype))}/{quote(cstr(name), safe = empty text)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L89) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1129) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1688)

<a id="op-9a95f6153ecd82"></a>
### Get url to form

`operation_foundation_utils_data_business_behavior_get_resource_address_to_form`

**Inputs** doctype, name = no value.

**Declared result** str.

**Explicit results** get\_url(uri = uri).

**Local steps**

- If not name.
  - Set uri from formatted text /desk/{quoted(slug(doctype))}.
- Otherwise.
  - Set uri from formatted text /desk/{quoted(slug(doctype))}/{quote(cstr(name), safe = empty text)}.
- Return get\_url(uri = uri).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L95) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1724)

<a id="op-7dec1dd1dd8469"></a>
### Get url to list

`operation_foundation_utils_data_business_behavior_get_resource_address_to_list`

**Inputs** doctype.

**Declared result** str.

**Explicit results** get\_url(uri = formatted text /desk/{quoted(slug(doctype))}).

**Local steps**

- Return get\_url(uri = formatted text /desk/{quoted(slug(doctype))}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L1207) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1725)

<a id="op-138f2948ce38bd"></a>
### Get url to report

`operation_foundation_utils_data_business_behavior_get_resource_address_to_report`

**Inputs** name, report\_type = no value, doctype = no value.

**Declared result** str.

**Explicit results** get\_url(uri = formatted text /desk/{quoted(slug(doctype))}/view/report/{quote(cstr(name), safe = empty text)}) · get\_url(uri = formatted text /desk/query-report/{quote(cstr(name), safe = empty text)}).

**Local steps**

- If report\_type equals “Report Builder”.
  - Return get\_url(uri = formatted text /desk/{quoted(slug(doctype))}/view/report/{quote(cstr(name), safe = empty text)}).
- Otherwise.
  - Return get\_url(uri = formatted text /desk/query-report/{quote(cstr(name), safe = empty text)}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L96) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1167) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1726)

<a id="op-ef94e466691802"></a>
### Get url to report with filters

`operation_foundation_utils_data_business_behavior_get_resource_address_to_report_with_filters`

**Inputs** name, filters, report\_type = no value, doctype = no value.

**Explicit results** get\_url(uri = formatted text /desk/{quoted(slug(doctype))}/view/report?{filters}) · get\_url(uri = formatted text /desk/query-report/{quote(cstr(name), safe = empty text)}?{filters}).

**Local steps**

- If report\_type equals “Report Builder”.
  - Return get\_url(uri = formatted text /desk/{quoted(slug(doctype))}/view/report?{filters}).
- Return get\_url(uri = formatted text /desk/query-report/{quote(cstr(name), safe = empty text)}?{filters}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L97) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1168) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1727)

<a id="op-a3971b7ffa0aaa"></a>
### Get filtered list url

`operation_foundation_utils_data_business_behavior_get_filtered_list_resource_address`

**Inputs** doctype, docnames = no value.

**Declared result** str.

**Explicit results** list\_url · empty text.join(tuple(list\_url, “?”, urlencode(mapping(“name” → json.dumps(list(“in”, docnames)))))).

**Local steps**

- Set list\_url from get\_url\_to\_list(doctype).
- If not docnames.
  - Return list\_url.
- Return empty text.join(tuple(list\_url, “?”, urlencode(mapping(“name” → json.dumps(list(“in”, docnames)))))).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L1808) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1138) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1697)

<a id="op-215b05f63aca31"></a>
### Get filtered list link

`operation_foundation_utils_data_business_behavior_get_filtered_list_link`

**Inputs** doctype, docnames = no value, label = no value.

**Declared result** str.

**Explicit results** formatted text &lt;a href="{url}"&gt;{label}&lt;/a&gt;.

**Local steps**

- Bind dependencies \_.
- Set url from get\_filtered\_list\_url(doctype, docnames).
- Set label from (label or translated doctype).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in label → translated doctype.
- Return formatted text &lt;a href="{url}"&gt;{label}&lt;/a&gt;.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L2018) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1137) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1696)

<a id="op-c039208c24945b"></a>
### Sql like

`operation_foundation_utils_data_business_behavior_database_query_like`

**Inputs** value, pattern.

**Declared result** bool.

**Explicit results** false · pattern.strip(“%”) belongs to value · value.endswith(pattern.lstrip(“%”)) · value.startswith(pattern.rstrip(“%”)) · pattern belongs to value.

**Local steps**

- If not (isinstance(pattern, str) and isinstance(value, str)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(pattern, str) → isinstance(value, str).
  - Return false.
- If (pattern.startswith(“%”) and pattern.endswith(“%”)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in pattern.startswith(“%”) → pattern.endswith(“%”).
  - Return pattern.strip(“%”) belongs to value.
- Otherwise.
  - If pattern.startswith(“%”).
    - Return value.endswith(pattern.lstrip(“%”)).
  - Otherwise.
    - If pattern.endswith(“%”).
      - Return value.startswith(pattern.rstrip(“%”)).
    - Otherwise.
      - Return pattern belongs to value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L2231) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1101) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1660)

<a id="op-cd6d27776189ef"></a>
### Filter operator is

`operation_foundation_utils_data_business_behavior_filter_operator_is`

**Inputs** value, pattern.

**Declared result** bool.

**Explicit results** is\_set() · not is\_set().

**Explicit failure paths** validation helper — Platform.\_(formatted text Invalid argument for operator 'IS': {pattern}).

**Local steps**

- Set pattern from pattern.lower().
- Bind local operation is\_set for subsequent calls.
- If pattern equals “set”.
  - Return is\_set().
- Otherwise.
  - If pattern equals “not set”.
    - Return not is\_set().
  - Otherwise.
    - Call the validation error handler Platform.throw(Platform.\_(formatted text Invalid argument for operator 'IS': {pattern})).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L2580) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1116) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1675)

<a id="op-01cb847542d36c"></a>
### Filter operator is.is set

`operation_foundation_utils_data_business_behavior_filter_operator_is_is_set`

**Inputs** no declared parameters.

**Explicit results** false · true.

**Local steps**

- If value is identical to no value.
  - Return false.
- Otherwise.
  - If (isinstance(value, str) and not value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(value, str) → not value.
    - Return false.
- Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L2895) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1117) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1676)

<a id="op-906cbe2ed90292"></a>
### Filter operator timespan

`operation_foundation_utils_data_business_behavior_filter_operator_timespan`

**Inputs** value, pattern.

**Declared result** bool.

**Explicit results** false · date\_range at 0 ≤ getdate(value) ≤ date\_range at 1.

**Local steps**

- If not value.
  - Return false.
- Set date\_range from get\_timespan\_date\_range(pattern).
- Return date\_range at 0 ≤ getdate(value) ≤ date\_range at 1.
  - Compare adjacent operands in order, stopping at the first false comparison in date\_range at 0 ≤ getdate(value) ≤ date\_range at 1.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L3001) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1118) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1677)

<a id="op-8ec9414550038a"></a>
### Convert type for between filters

`operation_foundation_utils_data_business_behavior_convert_type_for_between_filters`

**Inputs** value, set\_time.

**Declared result** datetime.datetime.

**Explicit results** value · datetime.datetime.combine(value, set\_time).

**Local steps**

- If isinstance(value, str).
  - If one space belongs to value.strip().
    - Set value from get\_datetime(value).
  - Otherwise.
    - Set value from getdate(value).
- If isinstance(value, datetime.datetime).
  - Return value.
- Otherwise.
  - If isinstance(value, datetime.date).
    - Return datetime.datetime.combine(value, set\_time).
- Return value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L3153) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1099) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1658)

<a id="op-f93aa5963a9783"></a>
### Filter operator between

`operation_foundation_utils_data_business_behavior_filter_operator_between`

**Inputs** value, pattern.

**Declared result** bool.

**Explicit results** false · pattern at 0 ≤ value ≤ pattern at 1.

**Local steps**

- If value is identical to no value.
  - Return false.
- Return pattern at 0 ≤ value ≤ pattern at 1.
  - Compare adjacent operands in order, stopping at the first false comparison in pattern at 0 ≤ value ≤ pattern at 1.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L3422) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1115) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1674)

<a id="op-0482a0ddf3054e"></a>
### Evaluate filters

`operation_foundation_utils_data_business_behavior_evaluate_filters`

**Inputs** doc, filters.

**Explicit results** false · true.

**Local steps**

- Bind dependencies get\_nested\_set\_hierarchy\_result.
- Bind dependencies NestedSetHierarchy.
- If not isinstance(filters, Filters).
  - Set filters from Filters(filters, doctype = doc.get(“doctype”)).
- For each d in filters.
  - Set f from get\_filter(no value, d).
  - If f.operator.lower() belongs to NestedSetHierarchy.
    - Set hierarchy from f.operator.lower().
    - Set df from Platform.get\_meta(f.doctype).get\_field(f.fieldname).
    - Set f.value from get\_nested\_set\_hierarchy\_result(df.options when df, otherwise f.doctype, f.value, hierarchy).
      - Value choice on df — true gives df.options, false gives f.doctype.
    - Set f.operator from “not in” when hierarchy belongs to tuple(“not ancestors of”, “not descendants of”), otherwise “in”.
      - Value choice on hierarchy belongs to tuple(“not ancestors of”, “not descendants of”) — true gives “not in”, false gives “in”.
  - If not compare(doc.get(f.fieldname), f.operator, f.value, f.fieldtype).
    - Return false.
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L87) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1111) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1670)

<a id="op-4b60043721057c"></a>
### Compare

`operation_foundation_utils_data_business_behavior_compare`

**Inputs** val1, condition, val2, fieldtype = no value.

**Declared result** bool.

**Explicit results** operator\_map at condition(val1, val2) · false.

**Local steps**

- If fieldtype.
  - If condition belongs to set(“is”, “Timespan”).
    - Take no action here.
  - Otherwise.
    - If condition belongs to set(“in”, “not in”).
      - If val1 is distinct from no value.
        - Set val1 from cast(fieldtype, val1).
    - Otherwise.
      - If condition belongs to set(“between”, “Between”).
        - If val1 is distinct from no value.
          - Set val1 from cast(fieldtype, val1).
        - If fieldtype equals “Datetime”.
          - Set val2 from list(convert\_type\_for\_between\_filters(val2 at 0, set\_time = datetime.time()), convert\_type\_for\_between\_filters(val2 at 1, set\_time = datetime.time(23, 59, 59, 999999))).
        - Otherwise.
          - Set val2 from list of cast(fieldtype, v) for v drawn from val2.
            - Draw v from val2.
      - Otherwise.
        - Set val1 from cast(fieldtype, val1).
        - Set val2 from cast(fieldtype, val2).
- If condition belongs to operator\_map.
  - Return operator\_map at condition(val1, val2).
- Return false.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0476.json#L3817) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1096) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1655)
