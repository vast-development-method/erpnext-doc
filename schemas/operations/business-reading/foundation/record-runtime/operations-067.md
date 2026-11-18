# Record lifecycle and persistence · operations 67

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Naming

<a id="op-aa8bb5785cf7c8"></a>
### Set name by naming series

`operation_foundation_model_naming_business_behavior_set_name_by_naming_series`

**Inputs** doc.

**Explicit failure paths** validation helper — Platform.\_(“Naming Series mandatory”).

**Local steps**

- If not doc.naming\_series.
  - Set doc.naming\_series from get\_default\_naming\_series(doc.doctype).
- If not doc.naming\_series.
  - Call the validation error handler Platform.throw(Platform.\_(“Naming Series mandatory”)).
- Set doc.name from make\_autoname((doc.naming\_series + “.#####”), empty text, doc).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L2612) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L607) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1203)

<a id="op-9148e92efd22fe"></a>
### Make autoname

`operation_foundation_model_naming_business_behavior_make_autoname`

**Inputs** key = empty text, doctype = empty text, doc = empty text, ignore\_validate (named only, default false).

**Explicit results** (\_get\_timestamp\_prefix() + \_generate\_random\_string(7)) at slice no value to 10 · series.generate\_next\_name(doc, ignore\_validate = ignore\_validate).

**Local steps**

- If key equals “hash”.
  - Return (\_get\_timestamp\_prefix() + \_generate\_random\_string(7)) at slice no value to 10.
- Set series from NamingSeries(key).
- Return series.generate\_next\_name(doc, ignore\_validate = ignore\_validate).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L120) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L593) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1189)

<a id="op-31cb72c4ef3694"></a>
### Get timestamp prefix

`operation_foundation_model_naming_business_behavior_get_timestamp_prefix`

**Inputs** no declared parameters.

**Explicit results** (request\_part + ts\_part).

**Local steps**

- Set ts from int((time.time() × 10)).
- Set ts from (ts modulo or format (32 to the power 4)).
- Set ts\_part from nested operand in the contract.b32hexencode(nested operand in the contract(length = nested operand in the contract, byteorder = nested operand in the contract)).decode() at slice negative 3 to no value.lower().
- Set request\_part from (get\_trace\_id() or empty text) at slice negative 1 to no value.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_trace\_id() → empty text.
- Return (request\_part + ts\_part).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L119) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L589) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1185)

<a id="op-4c7ffbd9dfa852"></a>
### Generate random string

`operation_foundation_model_naming_business_behavior_generate_random_string`

**Inputs** length = 10.

**Explicit results** nested operand in the contract.b32hexencode(nested operand in the contract(nested operand in the contract)).decode() at slice no value to length.lower().

**Local steps**

- Bind dependencies get\_random\_bytes.
- Return nested operand in the contract.b32hexencode(nested operand in the contract(nested operand in the contract)).decode() at slice no value to length.lower().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L3327) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L587) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1183)

<a id="op-7019a328f3698b"></a>
### Parse naming series

`operation_foundation_model_naming_business_behavior_parse_naming_series`

**Inputs** parts, doctype = no value, doc = no value, number\_generator = no value.

**Declared result** str.

**Explicit results** name.

**Local steps**

- Set name from empty text.
- Set \_sentinel from object().
- If isinstance(parts, str).
  - Set parts from parts.split(“.”).
- If not number\_generator.
  - Set number\_generator from getseries.
- Set series\_set from false.
- Set today from now\_datetime().
- For each e in parts.
  - If not e.
    - Continue with the next iteration or loop test.
  - Set part from empty text.
  - If e.startswith(“#”).
    - If not series\_set.
      - Set digits from len(e).
      - Set part from number\_generator(name, digits).
      - Set series\_set from true.
  - Otherwise.
    - If method bound to has\_custom\_parser(e).
      - Set part from Platform.get\_attr(method at 0)(doc, e).
    - Otherwise.
      - If e equals “YY”.
        - Set part from today.strftime(“%y”).
      - Otherwise.
        - If e equals “MM”.
          - Set part from today.strftime(“%m”).
        - Otherwise.
          - If e equals “DD”.
            - Set part from today.strftime(“%d”).
          - Otherwise.
            - If e equals “YYYY”.
              - Set part from today.strftime(“%Y”).
            - Otherwise.
              - If e equals “JJJ”.
                - Set part from today.strftime(“%j”).
              - Otherwise.
                - If e equals “WW”.
                  - Set part from determine\_consecutive\_week\_number(today).
                - Otherwise.
                  - If e equals “timestamp”.
                    - Set part from str(today).
                  - Otherwise.
                    - If (doc and (e.startswith(“{”) or doc.get(e, \_sentinel) is distinct from \_sentinel)).
                      - Evaluate in order, stop at the first false operand, otherwise use the last operand in doc → (e.startswith(“{”) or doc.get(e, \_sentinel) is distinct from \_sentinel).
                      - Evaluate in order, stop at the first true operand, otherwise use the last operand in e.startswith(“{”) → doc.get(e, \_sentinel) is distinct from \_sentinel.
                      - Set e from e.replace(“{”, empty text).replace(“}”, empty text).
                      - Set part from doc.get(e).
                    - Otherwise.
                      - Set part from e.
  - If isinstance(part, str).
    - Update name using + part.
  - Otherwise.
    - If isinstance(part, NAMING\_SERIES\_PART\_TYPES).
      - Update name using + cstr(part).strip().
- Return name.

**Values supplied outside this operation** clock or generated value from now\_datetime() · selected callable from Platform.get\_attr(method at 0).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L3445) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L603) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1199)

<a id="op-ebbe7d6898c431"></a>
### Has custom parser

`operation_foundation_model_naming_business_behavior_has_custom_parser`

**Inputs** e.

**Explicit results** Platform.get\_hooks(“naming\_series\_variables”, mapping()).get(e).

**Local steps**

- Return Platform.get\_hooks(“naming\_series\_variables”, mapping()).get(e).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“naming\_series\_variables”, mapping()).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L4615) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1187)

<a id="op-39d73927bb0e79"></a>
### Determine consecutive week number

`operation_foundation_model_naming_business_behavior_determine_consecutive_week_number`

**Inputs** datetime.

**Explicit results** w.

**Local steps**

- Set m from datetime.month.
- Set w from datetime.strftime(“%V”).
- If (m equals 1 and int(w) ≥ 52).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in m equals 1 → int(w) ≥ 52.
  - Set w from “00”.
- Otherwise.
  - If (m equals 12 and int(w) ≤ 1).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in m equals 12 → int(w) ≤ 1.
    - Set w from “53”.
- Return w.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L4692) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1179)

<a id="op-29aee31189cb58"></a>
### Getseries

`operation_foundation_model_naming_business_behavior_getseries`

**Inputs** key, digits.

**State and service calls** execute query text (UPDATE, Series) · execute query text (INSERT, Series).

**Explicit results** (((“%0” + str(digits)) + “d”) modulo or format current).

**Local steps**

- Set series from DocType(“Series”).
- Set current from nested operand in the contract(nested operand in the contract).for\_update().select(“current”).run().
- If (current and current at 0 at 0 is distinct from no value).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current → current at 0 at 0 is distinct from no value.
  - Set current from current at 0 at 0.
  - Evaluate Platform.db.sql(query text (UPDATE, Series), tuple(key)).
  - Set current from (cint(current) + 1).
- Otherwise.
  - Evaluate Platform.db.sql(query text (INSERT, Series), tuple(key)).
  - Set current from 1.
- Return (((“%0” + str(digits)) + “d”) modulo or format current).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L4914) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L590) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1186)

<a id="op-94cee8a003263f"></a>
### Revert series if last

`operation_foundation_model_naming_business_behavior_revert_series_if_last`

**Inputs** key, name, doc = no value.

**State and service calls** execute query text (UPDATE, Series).

**Explicit results** no value.

**Local steps**

- If “.#” belongs to key.
  - Set tuple(prefix, hashes) from key.rsplit(“.”, 1).
  - If “#” does not belong to hashes.
    - Set hash from re.search(“#+”, key).
    - If not hash.
      - Return no value.
    - Set name from name.replace(hashes, empty text).
    - Set prefix from prefix.replace(hash.group(), empty text).
- Otherwise.
  - Set prefix from key.
- If “.” belongs to prefix.
  - Set boundary from len(parse\_naming\_series(prefix.split(“.”), doc = doc)).
  - Set count from cint(name at slice boundary to no value).
  - Set prefix from name at slice no value to boundary.
- Otherwise.
  - Set count from cint(name.replace(prefix, empty text)).
- Set series from DocType(“Series”).
- Set current from nested operand in the contract(nested operand in the contract).for\_update().select(“current”).run().
- If (current and current at 0 at 0 equals count).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in current → current at 0 at 0 equals count.
  - Evaluate Platform.db.sql(query text (UPDATE, Series), prefix).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L5418) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L605) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1201)

<a id="op-9d973f3996c5f4"></a>
### Get default naming series

`operation_foundation_model_naming_business_behavior_get_default_naming_series`

**Inputs** doctype.

**Declared result** (str bitwise or no value).

**Explicit results** option.

**Local steps**

- Set naming\_series\_options from Platform.get\_meta(doctype).get\_naming\_series\_options().
- For each option in naming\_series\_options.
  - If option.
    - Return option.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L6163) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L588) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1184)

<a id="op-646b4c3ce466d6"></a>
### Validate name

`operation_foundation_model_naming_business_behavior_validate_name`

**Inputs** doctype, name.

**Explicit results** name.

**Explicit failure paths** validation helper — translated “No Name Specified for {0}”.format(doctype) · validation helper with Platform.NameError — translated “Invalid name type (integer) for varchar name column” · validation helper with Platform.NameError — translated “There were some errors setting the name, please contact the administrator” · validation helper with Platform.NameError — translated “Name of {0} cannot be {1}”.format(doctype, name) · validation helper with Platform.NameError — translated “Name cannot contain special characters like {0}”.format(message).

**Local steps**

- If not name.
  - Call the validation error handler Platform.throw(translated “No Name Specified for {0}”.format(doctype)).
- If isinstance(name, int).
  - If is\_autoincremented(doctype).
    - Evaluate Platform.db.set\_next\_sequence\_val(doctype, name, is\_val\_used = true).
    - Return name.
  - Call the validation error handler Platform.throw(translated “Invalid name type (integer) for varchar name column”, Platform.NameError).
- If name.startswith((“New ” + doctype)).
  - Call the validation error handler Platform.throw(translated “There were some errors setting the name, please contact the administrator”, Platform.NameError).
- Set name from name.strip().
- If (not Platform.get\_meta(doctype).get(“issingle”) and doctype equals name and name differs from “DocType”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.get\_meta(doctype).get(“issingle”) → doctype equals name → name differs from “DocType”.
  - Call the validation error handler Platform.throw(translated “Name of {0} cannot be {1}”.format(doctype, name), Platform.NameError).
- Set special\_characters from “&lt;&gt;”.
- If re.findall(formatted text &#91;{special\_characters}&#93;+, name).
  - Set message from “, ”.join(generator of formatted text '{c}' for c drawn from special\_characters).
    - Draw c from special\_characters.
  - Call the validation error handler Platform.throw(translated “Name cannot contain special characters like {0}”.format(message), Platform.NameError).
- Return name.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0286.json#L6281) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L612) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1207)

<a id="op-0c54353ca5deef"></a>
### Append number if name exists

`operation_foundation_model_naming_business_behavior_append_number_if_name_exists`

**Inputs** doctype, value, fieldname = “name”, separator = “-”, filters = no value.

**Record and data access** read doctype via exists.

**State and service calls** execute a supplied database query.

**Explicit results** value.

**Local steps**

- If not filters.
  - Set filters from dict().
- Evaluate filters.update(mapping(fieldname → value)).
- Set exists from Platform.db.exists(doctype, filters).
- Set regex from formatted text ^{re.escape(value)}{separator}\\d+$.
- If exists.
  - Set last from Platform.db.sql(formatted text SELECT ′{fieldname}′ FROM ′tab{doctype}′  WHERE ′{fieldname}′ {Platform.db.REGEX\_CHARACTER} %s  ORDER BY length({fieldname}) DESC,  ′{fieldname}, regex).
  - If last.
    - Set count from str((cint(nested operand in the contract at nested operand in the contract.rsplit(separator, 1) at 1) + 1)).
  - Otherwise.
    - Set count from “1”.
  - Set value from formatted text {value}{separator}{count}.
- Return value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L582) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1178)

<a id="op-884ba172d28810"></a>
### Set amended name

`operation_foundation_model_naming_business_behavior_set_amended_name`

**Inputs** doc.

**Record and data access** read “Amended Document Naming Settings” via get\_value · read “Document Naming Settings” via get\_single\_value · read doc.doctype via get\_value.

**Explicit results** no value · doc.name.

**Local steps**

- Set amend\_naming\_rule from Platform.db.get\_value(“Amended Document Naming Settings”, mapping(“document\_type” → doc.doctype), “action”, cache = true).
- If not amend\_naming\_rule.
  - Set amend\_naming\_rule from Platform.get\_single\_value(“Document Naming Settings”, “default\_amend\_naming”).
- If amend\_naming\_rule equals “Default Naming”.
  - Return no value.
- Set am\_id from 1.
- Set am\_prefix from doc.amended\_from.
- If Platform.db.get\_value(doc.doctype, doc.amended\_from, “amended\_from”).
  - Set am\_id from (cint(doc.amended\_from.split(“-”) at negative 1) + 1).
  - Set am\_prefix from “-”.join(doc.amended\_from.split(“-”) at slice no value to negative 1).
- Set doc.name from ((am\_prefix + “-”) + str(am\_id)).
- Return doc.name.

**Values supplied outside this operation** configured or stored value from Platform.get\_single\_value(“Document Naming Settings”, “default\_amend\_naming”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L564) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L606) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1202)

<a id="op-8627cc4f79673c"></a>
### Field autoname

`operation_foundation_model_naming_business_behavior_field_autoname`

**Inputs** autoname, doc, skip\_slicing = no value.

**Explicit results** (cstr(doc.get(fieldname)) or empty text).strip().

**Local steps**

- Set fieldname from autoname when skip\_slicing, otherwise autoname at slice 6 to no value.
  - Value choice on skip\_slicing — true gives autoname, false gives autoname at slice 6 to no value.
- Return (cstr(doc.get(fieldname)) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cstr(doc.get(fieldname)) → empty text.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L1037) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1180)

<a id="op-419d48a8448952"></a>
### Prompt autoname

`operation_foundation_model_naming_business_behavior_prompt_autoname`

**Inputs** autoname, doc.

**Explicit failure paths** validation helper — translated “Please set the document name”.

**Local steps**

- If not doc.name.
  - Call the validation error handler Platform.throw(translated “Please set the document name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L1184) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L604) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1200)

<a id="op-f4f0047555cc8e"></a>
### Format autoname

`operation_foundation_model_naming_business_behavior_format_autoname`

**Inputs** autoname, doc.

**Explicit results** name.

**Local steps**

- Set first\_colon\_index from autoname.find(“:”).
- Set autoname\_value from autoname at slice (first\_colon\_index + 1) to no value.
- Bind local operation get\_param\_value\_for\_match for subsequent calls.
- Set name from BRACED\_PARAMS\_PATTERN.sub(get\_param\_value\_for\_match, autoname\_value).
- Return name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L118) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1181)

<a id="op-1f4bb7f35fff40"></a>
### Format autoname.get param value for match

`operation_foundation_model_naming_business_behavior_format_autoname_get_parameter_value_for_match`

**Inputs** match.

**Explicit results** parse\_naming\_series(list(param at slice 1 to negative 1), doc = doc).

**Local steps**

- Set param from match.group().
- Return parse\_naming\_series(list(param at slice 1 to negative 1), doc = doc).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0287.json#L1649) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L586) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1182)

## Record · Navbar settings

[Record definition](../../../../data/record-types/navbar_settings.json)

<a id="op-754f8536f8372e"></a>
### Get app logo

`operation_foundation_core_record_definitions_navbar_settings_business_behavior_get_application_logo`

**Inputs** no declared parameters.

**Record and data access** read “Navbar Settings” via get\_cached\_value.

**Explicit results** app\_logo.

**Local steps**

- Set app\_logo from (Platform.get\_website\_settings(“app\_logo”) or Platform.get\_cached\_value(“Navbar Settings”, “Navbar Settings”, “app\_logo”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_website\_settings(“app\_logo”) → Platform.get\_cached\_value(“Navbar Settings”, “Navbar Settings”, “app\_logo”).
- If not app\_logo.
  - Set logos from Platform.get\_hooks(“app\_logo\_url”).
  - Set app\_logo from logos at 0.
  - If len(logos) equals 2.
    - Set app\_logo from logos at 1.
- Return app\_logo.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“Navbar Settings”, “Navbar Settings”, “app\_logo”) · selected callable from Platform.get\_hooks(“app\_logo\_url”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L2053) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1708)

<a id="op-a1a2bc986f603b"></a>
### Get navbar settings

`operation_foundation_core_record_definitions_navbar_settings_business_behavior_get_navbar_settings`

**Inputs** no declared parameters.

**Record and data access** read “Navbar Settings” via get\_single.

**Explicit results** Platform.get\_single(“Navbar Settings”).

**Local steps**

- Return Platform.get\_single(“Navbar Settings”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L2288) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1709)

<a id="op-9d71a5ae973f41"></a>
### Sync standard items

`operation_foundation_core_record_definitions_navbar_settings_business_behavior_sync_standard_items`

**Inputs** no declared parameters.

**Local steps**

- Evaluate sync\_table(“settings\_dropdown”, “standard\_navbar\_items”).
- Evaluate sync\_table(“help\_dropdown”, “standard\_help\_items”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L2339) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1710)

<a id="op-fd1de51fac3ad6"></a>
### Sync table

`operation_foundation_core_record_definitions_navbar_settings_business_behavior_sync_table`

**Inputs** key, hook.

**State and service calls** call save on navbar\_settings.

**Local steps**

- Set navbar\_settings from NavbarSettings(“Navbar Settings”).
- Set existing\_items from mapping of d.item\_label → d for d drawn from navbar\_settings.get(key).
  - Draw d from navbar\_settings.get(key).
- Set new\_standard\_items from mapping().
- Set count from 0.
- For each item in Platform.get\_hooks(hook).
  - If item.get(“item\_label”) does not belong to existing\_items.
    - Evaluate navbar\_settings.append(key, item, count).
  - Set new\_standard\_items at item.get(“item\_label”) from true.
  - Update count using + 1.
- Set items from navbar\_settings.get(key).
- Set items from list of item for item drawn from items where not (item.is\_standard and item.item\_label does not belong to new\_standard\_items).
  - Draw item from items, keep a combination only if (not (item.is\_standard and item.item\_label does not belong to new\_standard\_items)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.is\_standard → item.item\_label does not belong to new\_standard\_items.
- Evaluate navbar\_settings.set(key, items).
- Evaluate navbar\_settings.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(hook).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0090.json#L2421) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1773) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1711)

## Service · Notifications

<a id="op-0dd2a3dd772612"></a>
### Get notification config

`operation_foundation_core_notifications_business_behavior_get_notification_configuration`

**Inputs** no declared parameters.

**Explicit results** mapping(“for\_doctype” → mapping(“Error Log” → mapping(“seen” → 0), “Communication” → mapping(“status” → “Open”, “communication\_type” → “Communication”), “ToDo” → “Platform.core.notifications.get\_things\_tod ….

**Local steps**

- Return mapping(“for\_doctype” → mapping(“Error Log” → mapping(“seen” → 0), “Communication” → mapping(“status” → “Open”, “communication\_type” → “Communication”), “ToDo” → “Platform.core.notifications.get\_things\_tod ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L3436) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L846) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L913)

<a id="op-fb210517db370c"></a>
### Get things todo

`operation_foundation_core_notifications_business_behavior_get_things_todo`

**Inputs** as\_list = false.

**Record and data access** read “ToDo” via get\_list.

**Explicit results** data · data at 0 at 0.

**Local steps**

- Set data from Platform.get\_list(“ToDo”, fields = list(“name”, “description”) when as\_list, otherwise list(mapping(“COUNT” → “\*”)), filters = list(list(“ToDo”, “status”, “=”, “Open”)), or\_filters = list(list(“ToDo”, “all ….
  - Value choice on as\_list — true gives list(“name”, “description”), false gives list(mapping(“COUNT” → “\*”)).
- If as\_list.
  - Return data.
- Return data at 0 at 0.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L3725) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L914)

<a id="op-eb4f9b0108444f"></a>
### Get todays events

`operation_foundation_core_notifications_business_behavior_get_todays_events`

**Inputs** as\_list = false.

**Explicit results** events when as\_list, otherwise len(events).

**Local steps**

- Bind dependencies get\_events.
- Bind dependencies getdate.
- Set today from getdate().
- Set events from get\_events(today, today).
- Return events when as\_list, otherwise len(events).
  - Value choice on as\_list — true gives events, false gives len(events).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0119.json#L4029) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L915)
