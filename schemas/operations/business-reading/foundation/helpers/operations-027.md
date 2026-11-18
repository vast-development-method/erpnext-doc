# Shared value and file services · operations 27

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Legacy gravatar cleanup

<a id="op-1b8aabfb27c1d1"></a>
### Has gravatar image urls

`operation_foundation_utils_legacy_gravatar_cleanup_business_behavior_has_gravatar_image_resource_addresses`

**Inputs** no declared parameters.

**Record and data access** read doctype via exists.

**Explicit results** any(generator of Platform.db.exists(doctype, mapping(fieldname → tuple(“like”, GRAVATAR\_URL\_PATTERN))) for tuple(doctype, fieldname) drawn from get\_gravatar\_image\_fields()).

**Local steps**

- Return any(generator of Platform.db.exists(doctype, mapping(fieldname → tuple(“like”, GRAVATAR\_URL\_PATTERN))) for tuple(doctype, fieldname) drawn from get\_gravatar\_image\_fields()).
  - Draw tuple(doctype, fieldname) from get\_gravatar\_image\_fields().

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L7454) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1528) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L314)

<a id="op-eb89a75dac8d78"></a>
### Skip gravatar deletion prompt if no urls

`operation_foundation_utils_legacy_gravatar_cleanup_business_behavior_skip_gravatar_deletion_prompt_if_number_resource_addresses`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If cint(Platform.defaults.get\_global\_default(SKIP\_GRAVATAR\_DELETION\_PROMPT)).
  - Return no value.
- If not has\_gravatar\_image\_urls().
  - Evaluate Platform.defaults.set\_global\_default(SKIP\_GRAVATAR\_DELETION\_PROMPT, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L7578) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1530) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L316)

<a id="op-d87a5f54b626dd"></a>
### Submit gravatar deletion prompt

`operation_foundation_utils_legacy_gravatar_cleanup_business_behavior_submit_gravatar_deletion_prompt`

**Inputs** action.

**Wrappers, in declaration order** Platform.whitelist(methods = list(“POST”)).

**State and service calls** enqueue with delete\_gravatar\_image\_urls.

**Explicit results** “skipped” · “queued”.

**Explicit failure paths** validation helper — translated “Invalid action”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If action equals Action.KEEP\_GRAVATAR\_URLS.value.
  - Evaluate Platform.defaults.set\_global\_default(SKIP\_GRAVATAR\_DELETION\_PROMPT, 1).
  - Return “skipped”.
- If action equals Action.DELETE\_GRAVATAR\_URLS.value.
  - Evaluate Platform.enqueue(delete\_gravatar\_image\_urls, queue = “long”, now = Platform.in\_test, enqueue\_after\_commit = not Platform.in\_test, job\_id = GRAVATAR\_DELETION\_JOB\_ID, …).
  - Return “queued”.
- Call the validation error handler Platform.throw(translated “Invalid action”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”) · service or queued work from Platform.enqueue(delete\_gravatar\_image\_urls, queue = “long”, now = Platform.in\_test, enqueue\_after\_commit = not Platform.in\_test, job\_id = GRAVATAR\_DELETION\_JOB\_ID, …).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, effective access, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0485.json#L7709) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1531) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L317)

<a id="op-02879b1234aa8b"></a>
### Delete gravatar image urls

`operation_foundation_utils_legacy_gravatar_cleanup_business_behavior_delete_gravatar_image_resource_addresses`

**Inputs** no declared parameters.

**State and service calls** request set\_value on doctype.

**Local steps**

- For each tuple(doctype, fieldname) in get\_gravatar\_image\_fields().
  - Set filters from mapping(fieldname → tuple(“like”, GRAVATAR\_URL\_PATTERN)).
  - Evaluate Platform.db.set\_value(doctype, filters, fieldname, empty text, update\_modified = false).
- Evaluate Platform.defaults.set\_global\_default(SKIP\_GRAVATAR\_DELETION\_PROMPT, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1526) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L312)

## Service · Licenses

<a id="op-955e955ad688da"></a>
### To spdx license

`operation_foundation_binding_foundation_utils_sbom_licenses_to_spdx_license`

**Inputs** license.

**Declared result** tuple at tuple(str, (str bitwise or no value)).

**Explicit results** tuple(expression, no value) · tuple(NOASSERTION, (raw or no value)).

**Local steps**

- If expression bound to (\_canonicalize(license.expression) or \_canonicalize(license.text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_canonicalize(license.expression) → \_canonicalize(license.text).
  - Return tuple(expression, no value).
- If (len(license.classifiers) equals 1 and expression bound to CLASSIFIERS.get(license.classifiers at 0)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in len(license.classifiers) equals 1 → expression bound to CLASSIFIERS.get(license.classifiers at 0).
  - Return tuple(expression, no value).
- Set raw from whitespace '\\n'.join(filter(no value, tuple(license.expression, expanded license.classifiers, license.text))).
- Return tuple(NOASSERTION, (raw or no value)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in raw → no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L2) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L307) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L395)

<a id="op-5db93f2d56f7ae"></a>
### Canonicalize

`operation_foundation_binding_foundation_utils_sbom_licenses_canonicalize`

**Inputs** expression.

**Declared result** (str bitwise or no value).

**Explicit results** no value · canonicalize\_license\_expression(expression).

**Local steps**

- If not expression.
  - Return no value.
- Attempt the following.
  - Return canonicalize\_license\_expression(expression).
- On failure (InvalidLicenseExpression).
  - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L236) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L306) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L394)

## Service · Local

<a id="op-06794cdde772a4"></a>
### Local.getattribute

`operation_foundation_utils_local_business_behavior_local_getattribute`

**Inputs** self, name.

**Declared result** Any.

**Explicit results** obj at name.

**Explicit failure paths** AttributeError(name).

**Local steps**

- Set obj from \_contextvar.get(no value).
- If (obj is distinct from no value and name belongs to obj).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in obj is distinct from no value → name belongs to obj.
  - Return obj at name.
- Raise AttributeError(name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L179) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1535) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L321)

<a id="op-90da84030f150e"></a>
### Local.iterate

`operation_foundation_utils_local_business_behavior_local_iter`

**Inputs** self.

**Explicit results** iter(\_contextvar.get(mapping()).items()).

**Local steps**

- Return iter(\_contextvar.get(mapping()).items()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L333) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L322)

<a id="op-2783e8585b3d9a"></a>
### Local.setattr

`operation_foundation_utils_local_business_behavior_local_setattr`

**Inputs** self, name, value.

**Declared result** no value.

**Local steps**

- Set obj from \_contextvar.get(no value).
- If obj is identical to no value.
  - Set obj from mapping().
  - Evaluate \_contextvar.set(obj).
- Set obj at name from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L410) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L332)

<a id="op-964d92b4862817"></a>
### Local.delattr

`operation_foundation_utils_local_business_behavior_local_delattr`

**Inputs** self, name.

**Declared result** no value.

**Explicit results** no value.

**Explicit failure paths** AttributeError(name).

**Local steps**

- Set obj from \_contextvar.get(no value).
- If (obj is distinct from no value and name belongs to obj).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in obj is distinct from no value → name belongs to obj.
  - Remove obj at name.
  - Return no value.
- Raise AttributeError(name).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L570) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1534) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L320)

<a id="op-35ee25e3052d7d"></a>
### Local.invoke

`operation_foundation_utils_local_business_behavior_local_call`

**Inputs** self, name.

**Declared result** “LocalProxy”.

**Explicit results** lp.

**Local steps**

- Bind local operation \_get\_current\_object for subsequent calls.
- Set lp from LocalProxy(\_get\_current\_object).
- Evaluate object.\_\_setattr\_\_(lp, “\_get\_current\_object”, \_get\_current\_object).
- Return lp.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L730) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1532) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L318)

<a id="op-0cf05feb2439de"></a>
### Local.invoke.get current object

`operation_foundation_utils_local_business_behavior_local_call_get_current_object`

**Inputs** no declared parameters.

**Declared result** Any.

**Explicit results** obj at name.

**Explicit failure paths** RuntimeError(“object is not bound”).

**Local steps**

- Set obj from \_contextvar.get(no value).
- If (obj is distinct from no value and name belongs to obj).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in obj is distinct from no value → name belongs to obj.
  - Return obj at name.
- Raise RuntimeError(“object is not bound”) with cause no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L959) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1533) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L319)

<a id="op-cdc65b590cdb47"></a>
### Local Proxy.getattr

`operation_foundation_utils_local_business_behavior_local_proxy_getattr`

**Inputs** self, name.

**Declared result** Any.

**Explicit results** getattr(self.\_get\_current\_object(), name).

**Local steps**

- Return getattr(self.\_get\_current\_object(), name).

**Values supplied outside this operation** selected callable from getattr(self.\_get\_current\_object(), name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1093) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1541) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L327)

<a id="op-505e6b28e9b857"></a>
### Local Proxy.setattr

`operation_foundation_utils_local_business_behavior_local_proxy_setattr`

**Inputs** self, name, value.

**Declared result** no value.

**Local steps**

- Evaluate setattr(self.\_get\_current\_object(), name, value).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1172) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L329)

<a id="op-3bfe1aee6b7012"></a>
### Local Proxy.delattr

`operation_foundation_utils_local_business_behavior_local_proxy_delattr`

**Inputs** self, name.

**Declared result** no value.

**Local steps**

- Evaluate delattr(self.\_get\_current\_object(), name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1265) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1539) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L325)

<a id="op-98f11a72d2841f"></a>
### Local Proxy.getitem

`operation_foundation_utils_local_business_behavior_local_proxy_getitem`

**Inputs** self, key.

**Declared result** Any.

**Explicit results** self.\_get\_current\_object() at key.

**Local steps**

- Return self.\_get\_current\_object() at key.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1342) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L328)

<a id="op-d28c91da1f0b9f"></a>
### Local Proxy.setitem

`operation_foundation_utils_local_business_behavior_local_proxy_setitem`

**Inputs** self, key, value.

**Declared result** no value.

**Local steps**

- Set self.\_get\_current\_object() at key from value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1412) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1544) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L330)

<a id="op-4b290171b56f98"></a>
### Local Proxy.delitem

`operation_foundation_utils_local_business_behavior_local_proxy_delitem`

**Inputs** self, key.

**Declared result** no value.

**Local steps**

- Remove self.\_get\_current\_object() at key.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1498) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1540) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L326)

<a id="op-3da69600f63c99"></a>
### Local Proxy.bool

`operation_foundation_utils_local_business_behavior_local_proxy_boolean`

**Inputs** self.

**Declared result** bool.

**Explicit results** bool(self.\_get\_current\_object()) · false.

**Local steps**

- Attempt the following.
  - Return bool(self.\_get\_current\_object()).
- On failure (RuntimeError).
  - Return false.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1568) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L323)

<a id="op-88e4e4be0fdd64"></a>
### Local Proxy.contains

`operation_foundation_utils_local_business_behavior_local_proxy_contains`

**Inputs** self, key.

**Declared result** bool.

**Explicit results** key belongs to self.\_get\_current\_object().

**Local steps**

- Return key belongs to self.\_get\_current\_object().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1658) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L324)

<a id="op-a1b578cb89080b"></a>
### Local Proxy.str

`operation_foundation_utils_local_business_behavior_local_proxy_text`

**Inputs** self.

**Declared result** str.

**Explicit results** str(self.\_get\_current\_object()).

**Local steps**

- Return str(self.\_get\_current\_object()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1733) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L331)

<a id="op-fc22655e42ba47"></a>
### Release local

`operation_foundation_utils_local_business_behavior_release_local`

**Inputs** local.

**Explicit results** no value.

**Local steps**

- If isinstance(local, Local).
  - Evaluate \_contextvar.set(mapping()).
  - Return no value.
- Evaluate release\_werkzeug\_local(local).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1796) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1547) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L333)

## Service · Logger

<a id="op-15407bdff8e8ea"></a>
### Create handler

`operation_foundation_utils_logger_business_behavior_create_handler`

**Inputs** module, site = no value, max\_size = 100000, file\_count = 20, stream\_only = false.

**Explicit results** list(handler, site\_handler) · list(handler).

**Local steps**

- Set formatter from logging.Formatter(formatted text %(asctime)s %(levelname)s {module} %(message)s).
- If stream\_only.
  - Set handler from logging.StreamHandler().
- Otherwise.
  - Set logfile from formatted text {module}.log.
  - Set log\_filename from os.path.join(“..”, “logs”, logfile).
  - Set handler from RotatingFileHandler(log\_filename, maxBytes = max\_size, backupCount = file\_count).
- Evaluate handler.setFormatter(formatter).
- If (site and not stream\_only).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in site → not stream\_only.
  - Set sitelog\_filename from os.path.join(site, “logs”, logfile).
  - Set site\_handler from RotatingFileHandler(sitelog\_filename, maxBytes = max\_size, backupCount = file\_count).
  - Evaluate site\_handler.setFormatter(formatter).
  - Return list(handler, site\_handler).
- Return list(handler).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L1901) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1548) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L334)

<a id="op-181812fce4fcc5"></a>
### Get logger

`operation_foundation_utils_logger_business_behavior_get_logger`

**Inputs** module = no value, with\_more\_info = false, allow\_site = true, filter = no value, max\_size = 100000, file\_count = 20, stream\_only = stream\_logging.

**Declared result** “logging.Logger”.

**Explicit results** Platform.loggers at logger\_name · logger.

**Local steps**

- If allow\_site is identical to true.
  - Set site from getattr(Platform.local, “site”, no value).
- Otherwise.
  - If allow\_site belongs to get\_sites().
    - Set site from allow\_site.
  - Otherwise.
    - Set site from false.
- Set logger\_name from “{}-{}”.format(module, (site or “all”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → “all”.
- Attempt the following.
  - Return Platform.loggers at logger\_name.
- On failure (KeyError).
  - Take no action here.
- If not module.
  - Set module from “Platform”.
  - Set with\_more\_info from true.
- Set logger from logging.getLogger(logger\_name).
- Evaluate logger.setLevel((Platform.log\_level or default\_log\_level)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.log\_level → default\_log\_level.
- Set logger.propagate from false.
- Set handlers from create\_handler(module, site, max\_size, file\_count, …).
- For each handler in handlers.
  - Evaluate logger.addHandler(handler).
- If with\_more\_info.
  - Evaluate handlers at 0.addFilter(SiteContextFilter()).
- If filter.
  - Evaluate logger.addFilter(filter).
- Set Platform.loggers at logger\_name from logger.
- Return logger.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “site”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0486.json#L2354) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1549) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L335)
