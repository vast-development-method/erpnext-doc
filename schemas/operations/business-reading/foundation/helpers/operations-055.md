# Shared value and file services · operations 55

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Utils

<a id="op-fee3ddbcf256e8"></a>
### Validate url

`operation_foundation_utils_initialize_business_behavior_validate_resource_address`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** txt, throw, valid\_schemes.

**Explicit result forms** a value selected from the current context.

**Observed service boundaries** validation or user-notification service.

**Local structure** 3 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L209) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1497) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L284)

<a id="op-a71660395f8f6b"></a>
### Validate iban

`operation_foundation_utils_initialize_business_behavior_validate_international_bank_account_number`

**Inputs** iban, throw = false.

**Declared result** bool.

**Explicit results** valid.

**Explicit failure paths** validation helper — Platform.\_(“'{0}' is not a valid IBAN”).format(Platform.bold(iban)).

**Local steps**

- Bind dependencies \_.
- Set valid from is\_valid\_iban(iban).
- If (not valid and throw).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not valid → throw.
  - Call the validation error handler Platform.throw(Platform.\_(“'{0}' is not a valid IBAN”).format(Platform.bold(iban))).
- Return valid.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L683) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1493) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L280)

<a id="op-cc4f319b9bed47"></a>
### Is valid iban

`operation_foundation_utils_initialize_business_behavior_is_valid_international_bank_account_number`

**Inputs** iban.

**Declared result** bool.

**Explicit results** false · (to\_check modulo or format 97) equals 1.

**Local steps**

- If not iban.
  - Return false.
- Bind local operation encode\_char for subsequent calls.
- Set iban from iban.replace(one space, empty text).upper().
- Set flipped from (iban at slice 4 to no value + iban at slice no value to 4).
- Set encoded from list of encode\_char(c) when (ord(c) ≥ 65 and ord(c) ≤ 90), otherwise c for c drawn from flipped.
  - Draw c from flipped.
  - Value choice on (ord(c) ≥ 65 and ord(c) ≤ 90) — true gives encode\_char(c), false gives c.
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in ord(c) ≥ 65 → ord(c) ≤ 90.
- Attempt the following.
  - Set to\_check from int(empty text.join(encoded)).
- On failure (ValueError).
  - Return false.
- Return (to\_check modulo or format 97) equals 1.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L877) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1471) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L259)

<a id="op-8a4c5ae6adc731"></a>
### Is valid iban.encode char

`operation_foundation_utils_initialize_business_behavior_is_valid_international_bank_account_number_encode_character`

**Inputs** c.

**Explicit results** str(((9 + ord(c)) − 64)).

**Local steps**

- Return str(((9 + ord(c)) − 64)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L1305) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1472) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L260)

<a id="op-f3f99edf84d387"></a>
### Random string

`operation_foundation_utils_initialize_business_behavior_random_string`

**Inputs** length.

**Declared result** str.

**Explicit results** empty text.join(generator of secrets.choice(alphabet) for i drawn from range(length)).

**Local steps**

- Bind dependencies secrets.
- Bind dependencies string.
- Set alphabet from (string.ascii\_letters + string.digits).
- Return empty text.join(generator of secrets.choice(alphabet) for i drawn from range(length)).
  - Draw i from range(length).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L1383) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1478) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L266)

<a id="op-e7840e9888bb3a"></a>
### Get identicon

`operation_foundation_utils_initialize_business_behavior_get_identicon`

**Inputs** email.

**Declared result** str.

**Explicit results** Identicon(email).base64().

**Local steps**

- Bind dependencies Identicon.
- Return Identicon(email).base64().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L1539) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L232)

<a id="op-159ba20a3eec18"></a>
### Get traceback

`operation_foundation_utils_initialize_business_behavior_get_traceback`

**Inputs** with\_context = false.

**Declared result** str.

**Explicit results** empty text · tb.replace(bench\_path, empty text).

**Local steps**

- Bind dependencies iter\_exc\_lines.
- Set tuple(exc\_type, exc\_value, exc\_tb) from sys.exc\_info().
- If not any(list(exc\_type, exc\_value, exc\_tb)).
  - Return empty text.
- If (with\_context and not Platform.conf.developer\_mode).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in with\_context → not Platform.conf.developer\_mode.
  - Set with\_context from false.
- If with\_context.
  - Set trace\_list from iter\_exc\_lines(fmt = \_get\_traceback\_sanitizer()).
  - Set tb from whitespace '\\n'.join(trace\_list).
- Otherwise.
  - Set trace\_list from traceback.format\_exception(exc\_type, exc\_value, exc\_tb).
  - Set tb from empty text.join(generator of cstr(t) for t drawn from trace\_list).
    - Draw t from trace\_list.
- Set bench\_path from (get\_bench\_path() + “/”).
- Return tb.replace(bench\_path, empty text).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L130) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1463) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L251)

<a id="op-491c334fc66cf7"></a>
### Get traceback sanitizer

`operation_foundation_utils_initialize_business_behavior_get_traceback_sanitizer`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** no parameters.

**Explicit result forms** the result of a delegated call.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L131) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1464) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L252)

<a id="op-a9d3cc37a304df"></a>
### Get traceback sanitizer.is sensitive name

`operation_foundation_binding_foundation_utils_init_get_traceback_sanitizer_is_sensitive_name`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** name.

**Explicit result forms** a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L56) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L126) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L214)

<a id="op-7fe0e5b76a5e2f"></a>
### Get traceback sanitizer.dict printer

`operation_foundation_utils_initialize_business_behavior_get_traceback_sanitizer_mapping_printer`

**Control responsibility** Input and query validation. The operation evaluates untrusted or structured input at a validation boundary. The caller must preserve its declared failure behavior.

**Declared inputs** v.

**Explicit result forms** the result of a delegated call.

**Local structure** 1 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L132) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1465) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L253)

<a id="op-cab10f330a7b35"></a>
### Log

`operation_foundation_utils_initialize_business_behavior_log`

**Inputs** event, details.

**Local steps**

- Evaluate Platform.logger(event).info(details).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L2535) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1474) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L262)

<a id="op-394bc394b9bcfa"></a>
### Dict to str

`operation_foundation_utils_initialize_business_behavior_mapping_to_text`

**Inputs** args, sep = “&amp;”.

**Declared result** str.

**Explicit results** sep.join(generator of (formatted text {k}= + quote(str((nested operand in the contract at nested operand in the contract or empty text)))) for k drawn from list(args)).

**Local steps**

- Return sep.join(generator of (formatted text {k}= + quote(str((nested operand in the contract at nested operand in the contract or empty text)))) for k drawn from list(args)).
  - Draw k from list(args).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args at k → empty text.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L2612) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1475) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L263)

<a id="op-98d36ebf04cb5d"></a>
### List to str

`operation_foundation_utils_initialize_business_behavior_list_to_text`

**Inputs** seq, sep = “, ”.

**Explicit results** sep.join(map(str.strip, map(str, seq))).

**Local steps**

- Return sep.join(map(str.strip, map(str, seq))).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L2799) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1473) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L261)

<a id="op-d1ad6c2ea6a733"></a>
### Get defaults

`operation_foundation_utils_initialize_business_behavior_get_defaults`

**Inputs** key = no value.

**Explicit results** Platform.db.get\_defaults(key).

**Local steps**

- Return Platform.db.get\_defaults(key).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L2899) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L220)

<a id="op-9638c3736b500e"></a>
### Set default

`operation_foundation_utils_initialize_business_behavior_set_default`

**Inputs** key, val.

**Explicit results** Platform.db.set\_default(key, val).

**Local steps**

- Return Platform.db.set\_default(key, val).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L2960) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1484) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L271)

<a id="op-161f7678006a0c"></a>
### Remove blanks

`operation_foundation_utils_initialize_business_behavior_remove_blanks`

**Inputs** d.

**Declared result** dict.

**Explicit results** d.

**Local steps**

- For each tuple(k, v) in tuple(d.items()).
  - If not v.
    - Remove d at k.
- Return d.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L3029) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1480) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L267)

<a id="op-06ce4646ed7b6b"></a>
### Strip html tags

`operation_foundation_utils_initialize_business_behavior_strip_document_markup_tags`

**Inputs** text.

**Declared result** str.

**Explicit results** HTML\_TAGS\_PATTERN.sub(empty text, text).

**Local steps**

- Return HTML\_TAGS\_PATTERN.sub(empty text, text).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L3151) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1488) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L275)

<a id="op-c3adb9eece8a9e"></a>
### Get file timestamp

`operation_foundation_utils_initialize_business_behavior_get_file_timestamp`

**Inputs** fn.

**Explicit results** str(cint(os.stat(fn).st\_mtime)) · no value.

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies cint.
- Attempt the following.
  - Return str(cint(os.stat(fn).st\_mtime)).
- On failure (OSError) bound to e.
  - If e.args at 0 differs from 2.
    - Propagate the active failure.
  - Otherwise.
    - Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L3216) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L226)

<a id="op-6cabad896a77b8"></a>
### Esc

`operation_foundation_utils_initialize_business_behavior_esc`

**Inputs** s, esc\_chars.

**Explicit results** empty text · s.

**Local steps**

- If not s.
  - Return empty text.
- For each c in esc\_chars.
  - Set esc\_str from (“\\” + c).
  - Set s from s.replace(c, esc\_str).
- Return s.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L3379) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L211)

<a id="op-9c6a64e355e988"></a>
### Unesc

`operation_foundation_utils_initialize_business_behavior_unesc`

**Inputs** s, esc\_chars.

**Explicit results** s.

**Local steps**

- For each c in esc\_chars.
  - Set esc\_str from (“\\” + c).
  - Set s from s.replace(esc\_str, c).
- Return s.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L3514) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1490) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L277)

<a id="op-e1124189d906d0"></a>
### Execute in shell

`operation_foundation_utils_initialize_business_behavior_execute_in_shell`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** cmd, verbose, low\_priority, check\_exit\_code.

**Explicit result forms** a structured result.

**Locally raised failures** CommandFailedError.

**Local structure** 6 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L3628) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1420) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L212)

<a id="op-5e4f446aabedc5"></a>
### Get path

`operation_foundation_utils_initialize_business_behavior_get_path`

**Inputs** remaining positional values path, remaining named values kwargs.

**Explicit results** os.path.join(base, expanded path).

**Local steps**

- Set base from kwargs.get(“base”).
- If not base.
  - Set base from Platform.local.site\_path.
- Return os.path.join(base, expanded path).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4326) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L235)

<a id="op-6580da0edf0372"></a>
### Get site base path

`operation_foundation_utils_initialize_business_behavior_get_site_base_path`

**Inputs** no declared parameters.

**Explicit results** Platform.local.site\_path.

**Local steps**

- Return Platform.local.site\_path.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4463) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L239)

<a id="op-b4573cd3a225ae"></a>
### Get site path

`operation_foundation_utils_initialize_business_behavior_get_site_path`

**Inputs** remaining positional values path.

**Explicit results** get\_path(expanded path, base = get\_site\_base\_path()).

**Local steps**

- Return get\_path(expanded path, base = get\_site\_base\_path()).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0459.json#L4500) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L246)
