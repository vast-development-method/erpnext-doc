# Shared value and file services · operations 56

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-5754b760a9c3b3"></a>
### Get files path

`operation_foundation_utils_initialize_business_behavior_get_files_path`

**Inputs** remaining positional values path, remaining named values kwargs.

**Explicit results** get\_site\_path(“private” when kwargs.get(“is\_private”), otherwise “public”, “files”, expanded path).

**Local steps**

- Return get\_site\_path(“private” when kwargs.get(“is\_private”), otherwise “public”, “files”, expanded path).
  - Value choice on kwargs.get(“is\_private”) — true gives “private”, false gives “public”.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4572) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L227)

<a id="op-054f4679024042"></a>
### Get bench path

`operation_foundation_utils_initialize_business_behavior_get_site_management_path`

**Inputs** no declared parameters.

**Explicit results** (os.environ.get(“Platform\_BENCH\_ROOT”) or os.path.realpath(os.path.join(os.path.dirname(Platform.\_\_file\_\_), “..”, “..”, “..”))).

**Local steps**

- Return (os.environ.get(“Platform\_BENCH\_ROOT”) or os.path.realpath(os.path.join(os.path.dirname(Platform.\_\_file\_\_), “..”, “..”, “..”))).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“Platform\_BENCH\_ROOT”) → os.path.realpath(os.path.join(os.path.dirname(Platform.\_\_file\_\_), “..”, “..”, “..”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4681) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L243)

<a id="op-061863159af769"></a>
### Get bench id

`operation_foundation_utils_initialize_business_behavior_get_site_management_identifier`

**Inputs** no declared parameters.

**Explicit results** Platform.get\_conf().get(“bench\_id”, get\_bench\_path().strip(“/”).replace(“/”, “-”)).

**Local steps**

- Return Platform.get\_conf().get(“bench\_id”, get\_bench\_path().strip(“/”).replace(“/”, “-”)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4817) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L242)

<a id="op-4212369c2c638f"></a>
### Get site id

`operation_foundation_utils_initialize_business_behavior_get_site_identifier`

**Inputs** site = no value.

**Explicit results** formatted text {(site or Platform.local.site)}@{get\_bench\_id()}.

**Local steps**

- Return formatted text {(site or Platform.local.site)}@{get\_bench\_id()}.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4924) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L240)

<a id="op-9cb29959d2ddcd"></a>
### Get backups path

`operation_foundation_utils_initialize_business_behavior_get_backups_path`

**Inputs** no declared parameters.

**Explicit results** get\_site\_path(“private”, “backups”).

**Local steps**

- Return get\_site\_path(“private”, “backups”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5019) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L217)

<a id="op-ae4680a6d61238"></a>
### Get request site address

`operation_foundation_utils_initialize_business_behavior_get_request_site_address`

**Inputs** full\_address = false.

**Explicit results** get\_url(full\_address = full\_address).

**Local steps**

- Return get\_url(full\_address = full\_address).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5072) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L237)

<a id="op-e6d63036f2d28a"></a>
### Get site url

`operation_foundation_utils_initialize_business_behavior_get_site_resource_address`

**Inputs** site.

**Explicit results** conf.host\_name · formatted command or address in the contract.

**Local steps**

- Set conf from Platform.get\_conf(site).
- If conf.host\_name.
  - Return conf.host\_name.
- Return formatted command or address in the contract.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5134) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L247)

<a id="op-dd97d2bc6921a1"></a>
### Encode dict

`operation_foundation_utils_initialize_business_behavior_encode_mapping`

**Inputs** d, encoding = “utf-8”.

**Explicit results** d.

**Local steps**

- For each key in d.
  - If (isinstance(d at key, str) and isinstance(d at key, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(d at key, str) → isinstance(d at key, str).
    - Set d at key from d at key.encode(encoding).
- Return d.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L127) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L210)

<a id="op-b241b3fd0fe9e9"></a>
### Decode dict

`operation_foundation_utils_initialize_business_behavior_decode_mapping`

**Inputs** d, encoding = “utf-8”.

**Explicit results** d.

**Local steps**

- For each key in d.
  - If (isinstance(d at key, str) and not isinstance(d at key, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in isinstance(d at key, str) → not isinstance(d at key, str).
    - Set d at key from d at key.decode(encoding, “ignore”).
- Return d.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5401) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L208)

<a id="op-a61599a6c0d111"></a>
### Get site name

`operation_foundation_utils_initialize_business_behavior_get_site_name`

**Inputs** hostname.

**Wrappers, in declaration order** functools.lru\_cache.

**Explicit results** hostname.split(“:”, 1) at 0.

**Local steps**

- Return hostname.split(“:”, 1) at 0.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5581) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L245)

<a id="op-9b843d8c1779d6"></a>
### Get disk usage

`operation_foundation_utils_initialize_business_behavior_get_disk_usage`

**Inputs** no declared parameters.

**Explicit results** 0 · cint(nested operand in the contract.split(whitespace '\\n') at negative 2.split(whitespace '\\t') at 0).

**Local steps**

- Set files\_path from get\_files\_path().
- If not os.path.exists(files\_path).
  - Return 0.
- Set tuple(\_err, out) from execute\_in\_shell(formatted text du -hsm {files\_path}).
- Return cint(nested operand in the contract.split(whitespace '\\n') at negative 2.split(whitespace '\\t') at 0).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5655) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L221)

<a id="op-ab5b4f9143bec7"></a>
### Touch file

`operation_foundation_utils_initialize_business_behavior_touch_file`

**Inputs** path.

**Explicit results** path.

**Local steps**

- Within open(path, “a”).
  - Evaluate os.utime(path, no value).
- Return path.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5865) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1489) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L276)

<a id="op-01d28b888947d9"></a>
### Get test client

`operation_foundation_utils_initialize_business_behavior_get_test_client`

**Inputs** use\_cookies = true.

**Declared result** “Client”.

**Explicit results** Client(application, use\_cookies = use\_cookies).

**Local steps**

- Bind dependencies Client.
- Bind dependencies application.
- Return Client(application, use\_cookies = use\_cookies).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L5962) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L250)

<a id="op-2b3aecd0f816f9"></a>
### Get hook method

`operation_foundation_utils_initialize_business_behavior_get_hook_method`

**Inputs** hook\_name, fallback = no value.

**Explicit results** method · fallback.

**Local steps**

- Set method from Platform.get\_hooks().get(hook\_name).
- If method.
  - Set method from Platform.get\_attr(method at 0).
  - Return method.
- If fallback.
  - Return fallback.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(), Platform.get\_attr(method at 0).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L6051) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L231)

<a id="op-bce703a27b0dd6"></a>
### Call hook method

`operation_foundation_utils_initialize_business_behavior_call_hook_method`

**Inputs** hook, remaining positional values args, remaining named values kwargs.

**Explicit results** out.

**Local steps**

- Set out from no value.
- For each method\_name in Platform.get\_hooks(hook).
  - Set out from (out or Platform.get\_attr(method\_name)(expanded args, expanded names kwargs)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in out → Platform.get\_attr(method\_name)(expanded args, expanded names kwargs).
- Return out.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook), Platform.get\_attr(method\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L6202) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1403) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L195)

<a id="op-265a9d50172801"></a>
### Is cli

`operation_foundation_utils_initialize_business_behavior_is_command_line_interface`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** invoked\_from\_terminal.

**Local steps**

- Set invoked\_from\_terminal from false.
- Attempt the following.
  - Set invoked\_from\_terminal from bool(os.get\_terminal\_size()).
- On failure (Exception).
  - Set invoked\_from\_terminal from (sys.stdin and sys.stdin.isatty()).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sys.stdin → sys.stdin.isatty().
- Return invoked\_from\_terminal.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L6356) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1468) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L256)

<a id="op-43fa6b2fd3328a"></a>
### Update progress bar

`operation_foundation_utils_initialize_business_behavior_update_progress_bar`

**Inputs** txt, i, l, absolute = false.

**Explicit results** no value.

**Local steps**

- If os.environ.get(“CI”).
  - If i equals 0.
    - Evaluate sys.stdout.write(txt).
  - Evaluate sys.stdout.write(“.”).
  - Evaluate sys.stdout.flush().
  - Return no value.
- If (not getattr(Platform.local, “request”, no value) or is\_cli()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not getattr(Platform.local, “request”, no value) → is\_cli().
  - Set lt from len(txt).
  - Attempt the following.
    - Set col from 40 when os.get\_terminal\_size().columns &gt; 80, otherwise 20.
      - Value choice on os.get\_terminal\_size().columns &gt; 80 — true gives 40, false gives 20.
  - On failure (OSError).
    - Set col from 40.
  - If lt &lt; 36.
    - Set txt from (txt + (one space × (36 − lt))).
  - Set complete from int(((float((i + 1)) ÷ l) × col)).
  - Set completion\_bar from (“=” × complete).ljust(col, one space).
  - Set percent\_complete from formatted text {int(((float((i + 1)) ÷ l) × 100))}%.
  - Set status from formatted text {i} of {l} when absolute, otherwise percent\_complete.
    - Value choice on absolute — true gives formatted text {i} of {l}, false gives percent\_complete.
  - Evaluate sys.stdout.write(formatted text  {txt}: &#91;{completion\_bar}&#93; {status}).
  - Evaluate sys.stdout.flush().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “request”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L6499) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1491) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L278)

<a id="op-c3c77c67aaeea7"></a>
### Get html format

`operation_foundation_utils_initialize_business_behavior_get_document_markup_format`

**Inputs** print\_path.

**Explicit results** html\_format.

**Local steps**

- Set html\_format from no value.
- If os.path.exists(print\_path).
  - Within open(print\_path) bound as f.
    - Set html\_format from f.read().
  - For each tuple(include\_directive, path) in INCLUDE\_DIRECTIVE\_PATTERN.findall(html\_format).
    - For each app\_name in Platform.get\_installed\_apps().
      - Set include\_path from Platform.get\_app\_path(app\_name, expanded path.split(os.path.sep)).
      - If os.path.exists(include\_path).
        - Within open(include\_path) bound as f.
          - Set html\_format from html\_format.replace(include\_directive, f.read()).
        - Leave the innermost loop without its normal-exhaustion alternative.
- Return html\_format.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L7234) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L223)

<a id="op-cd506aa7308796"></a>
### Is markdown

`operation_foundation_utils_initialize_business_behavior_is_markdown`

**Inputs** text.

**Explicit results** true · false · not NON\_MD\_HTML\_PATTERN.search(text).

**Local steps**

- If “&lt;!-- markdown --&gt;” belongs to text.
  - Return true.
- Otherwise.
  - If “&lt;!-- html --&gt;” belongs to text.
    - Return false.
  - Otherwise.
    - Return not NON\_MD\_HTML\_PATTERN.search(text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L7598) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1470) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L258)

<a id="op-577c7b8da19375"></a>
### Is a property

`operation_foundation_utils_initialize_business_behavior_is_a_property`

**Inputs** x.

**Declared result** bool.

**Explicit results** isinstance(x, PropertyType).

**Local steps**

- Return isinstance(x, PropertyType).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L7716) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1467) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L255)

<a id="op-fe36db137e8dda"></a>
### Get sites

`operation_foundation_utils_initialize_business_behavior_get_sites`

**Inputs** sites\_path = no value.

**Explicit results** sorted(sites).

**Local steps**

- If not sites\_path.
  - Set sites\_path from (getattr(Platform.local, “sites\_path”, no value) or “.”).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in getattr(Platform.local, “sites\_path”, no value) → “.”.
- Set sites from list().
- For each site in os.listdir(sites\_path).
  - Set path from os.path.join(sites\_path, site).
  - If (os.path.isdir(path) and not os.path.islink(path) and os.path.exists(os.path.join(path, “site\_config.json”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.isdir(path) → not os.path.islink(path) → os.path.exists(os.path.join(path, “site\_config.json”)).
    - Evaluate sites.append(site).
- Return sorted(sites).

**Values supplied outside this operation** selected callable from getattr(Platform.local, “sites\_path”, no value).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L248)

<a id="op-fe1cd13bbb42ab"></a>
### Get request session

`operation_foundation_utils_initialize_business_behavior_get_request_session`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** max\_retries, max\_redirects, adapter.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L334) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L236)

<a id="op-10aa1757c4078d"></a>
### Markdown

`operation_foundation_utils_initialize_business_behavior_markdown`

**Inputs** text, sanitize = true, linkify = true.

**Explicit results** html.

**Local steps**

- Set html from text when is\_html(text), otherwise Platform.utils.md\_to\_html(text).
  - Value choice on is\_html(text) — true gives text, false gives Platform.utils.md\_to\_html(text).
- If sanitize.
  - Set html from html.replace(“&lt;!-- markdown --&gt;”, empty text).
  - Set html from sanitize\_html(html, linkify = linkify).
- Return html.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L586) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1476) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L264)

<a id="op-0b9ce150d66767"></a>
### Sanitize email

`operation_foundation_utils_initialize_business_behavior_sanitize_email`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** emails.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0460.json#L786) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1483) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L270)
