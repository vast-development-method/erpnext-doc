# Forms, reports and navigation · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Conversation

<a id="op-6c31e14141d1a5"></a>
### Normalize sections

`operation_foundation_binding_foundation_studio_ai_agent_tools_conversation_normalize_sections`

**Inputs** raw.

**Declared result** list at str.

**Explicit results** out.

**Local steps**

- If isinstance(raw, str).
  - Set items from raw.splitlines().
- Otherwise.
  - If isinstance(raw, list).
    - Set items from list of str(s) for s drawn from raw.
      - Draw s from raw.
  - Otherwise.
    - Set items from list().
- Set out from list().
- For each item in items.
  - Set s from nested operand in the contract(nested operand in the contract).strip().strip(“'"”).strip().
  - If s.
    - Evaluate out.append(s).
- Return out.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L96) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1759)

<a id="op-ae4bec8a153b76"></a>
### Propose plan

`operation_foundation_binding_foundation_studio_ai_agent_tools_conversation_propose_plan`

**Inputs** ctx, args.

**Declared result** no value.

**State and service calls** commit.

**Local steps**

- Set headline from (args.get(“headline”) or “Here's my plan”).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“headline”) → “Here's my plan”.
- Set data\_plan from normalize\_sections(args.get(“data\_plan”)).
- Set layout\_plan from normalize\_sections(args.get(“layout\_plan”)).
- Set palette from (args.get(“palette”) or empty text).strip().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in args.get(“palette”) → empty text.
- Set metadata from mapping(“status” → “plan\_summary”, “headline” → headline, “data\_plan” → data\_plan, “layout\_plan” → layout\_plan, …).
- Evaluate AISession.try\_append\_message(ctx.session\_id, “assistant”, headline, message\_type = “clarification”, task\_type = “agent”, metadata = metadata).
- Evaluate Platform.db.commit().
- Evaluate ctx.emit(“clarify”, question = headline, options = list(), plan\_summary = true, headline = headline, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0007.json#L97) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1760)

## Record · Country

[Record definition](../../../../data/record-types/country.json)

<a id="op-6d916c6c67752b"></a>
### Country.validate

`operation_foundation_geo_record_definitions_country_business_behavior_country_validate`

**Inputs** self.

**Explicit failure paths** validation helper — error\_msg.

**Local steps**

- Set error\_msg from translated “{0} is not a valid ISO 3166 ALPHA-2 code.”.format(self.code).
- Attempt the following.
  - Set country from pycountry.countries.lookup(self.code).
- On failure (LookupError).
  - Call the validation error handler Platform.throw(error\_msg).
- If country.alpha\_2 differs from self.code.upper().
  - Call the validation error handler Platform.throw(error\_msg).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L3097) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1578) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L343)

<a id="op-86bdc1d2ccc23c"></a>
### Import country and currency

`operation_foundation_geo_record_definitions_country_business_behavior_import_country_and_currency`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies enable\_default\_currencies.
- Set tuple(countries, currencies) from get\_countries\_and\_currencies().
- Evaluate bulk\_insert(“Country”, countries, ignore\_duplicates = true).
- Evaluate bulk\_insert(“Currency”, currencies, ignore\_duplicates = true).
- Evaluate enable\_default\_currencies().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L3323) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1580) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L345)

<a id="op-d51f9f75c4cacf"></a>
### Get countries and currencies

`operation_foundation_geo_record_definitions_country_business_behavior_get_countries_and_currencies`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Country” via get\_doc · resolve a document from “Currency” via get\_doc.

**Explicit results** tuple(countries, currencies).

**Local steps**

- Bind dependencies get\_geo\_data.
- Set data from get\_geo\_data().
- Set countries from list().
- Set currencies from list().
- Set added\_currencies from set().
- For each tuple(name, country) in data.items().
  - Set country from Platform.\_dict(country).
  - Evaluate countries.append(Platform.get\_doc(doctype = “Country”, name = name, country\_name = name, code = country.code, …)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in country.date\_format → “dd-mm-yyyy”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in country.time\_format → “HH:mm:ss”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in country.timezones → list().
  - If (country.currency and country.currency does not belong to added\_currencies).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in country.currency → country.currency does not belong to added\_currencies.
    - Evaluate added\_currencies.add(country.currency).
    - Evaluate currencies.append(Platform.get\_doc(doctype = “Currency”, name = country.currency, currency\_name = country.currency, fraction = country.currency\_fraction, …)).
- Return tuple(countries, currencies).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L3483) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1579) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L344)

## Service · Country info

<a id="op-e91746247ff927"></a>
### Get country info

`operation_foundation_geo_country_info_business_behavior_get_country_info`

**Inputs** country = no value.

**Explicit results** data.

**Local steps**

- Set data from get\_all().
- Set data from Platform.\_dict(data.get(country, mapping())).
- If “date\_format” does not belong to data.
  - Set data.date\_format from “dd-mm-yyyy”.
- If “time\_format” does not belong to data.
  - Set data.time\_format from “HH:mm:ss”.
- Return data.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L1892) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1573) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L338)

<a id="op-ea10e18f956410"></a>
### Get all

`operation_foundation_geo_country_info_business_behavior_get_all`

**Inputs** no declared parameters.

**Explicit results** all\_data.

**Local steps**

- Within open(os.path.join(os.path.dirname(\_\_file\_\_), “country\_info.json”)) bound as local\_info.
  - Set all\_data from json.loads(local\_info.read()).
- Return all\_data.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L2093) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1572) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L337)

<a id="op-ecadc99394544d"></a>
### Get country timezone info

`operation_foundation_geo_country_info_business_behavior_get_country_timezone_info`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Explicit results** \_get\_country\_timezone\_info().

**Local steps**

- Return \_get\_country\_timezone\_info().

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L2237) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1574) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L339)

<a id="op-489be280b15723"></a>
### Get country timezone info

`operation_foundation_geo_country_info_business_behavior_get_country_timezone_info_2`

**Inputs** no declared parameters.

**Wrappers, in declaration order** lru\_cache(maxsize = 2).

**Explicit results** mapping(“country\_info” → get\_all(), “all\_timezones” → get\_all\_timezones()).

**Local steps**

- Return mapping(“country\_info” → get\_all(), “all\_timezones” → get\_all\_timezones()).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L2305) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1575) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L340)

<a id="op-837b5877594bfa"></a>
### Get translated countries

`operation_foundation_geo_country_info_business_behavior_get_translated_countries`

**Inputs** no declared parameters.

**Explicit results** translated\_dict.

**Local steps**

- Bind dependencies Locale.
- Set translated\_dict from mapping().
- Set locale from Locale.parse(Platform.local.lang, sep = “-”).
- For each tuple(country, info) in get\_all().items().
  - Set country\_name from locale.territories.get((info.get(“code”) or empty text).upper()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in info.get(“code”) → empty text.
  - If (country\_name and country differs from country\_name).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in country\_name → country differs from country\_name.
    - Set translated\_dict at country from country\_name.
- Return translated\_dict.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L2399) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1576) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L341)

<a id="op-40fd25bb6e9054"></a>
### Update

`operation_foundation_geo_country_info_business_behavior_update`

**Inputs** no declared parameters.

**Local steps**

- Within open(os.path.join(os.path.dirname(\_\_file\_\_), “currency\_info.json”)) bound as nformats.
  - Set nformats from json.loads(nformats.read()).
- Set all\_data from get\_all().
- For each country in all\_data.
  - Set data from all\_data at country.
  - Set data at “number\_format” from nformats.get(data.get(“currency”, “default”), nformats.get(“default”)) at “display”.
- Within open(os.path.join(os.path.dirname(\_\_file\_\_), “country\_info.json”), “w”) bound as local\_info.
  - Evaluate local\_info.write(json.dumps(all\_data, indent = 1)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L2671) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1577) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L342)

## Record · Currency

[Record definition](../../../../data/record-types/currency.json)

<a id="op-90083f05ee5560"></a>
### Currency.validate

`operation_foundation_geo_record_definitions_currency_business_behavior_currency_validate`

**Inputs** self.

**Local steps**

- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L4833) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1584) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L349)

<a id="op-89a404658a8ddf"></a>
### Enable default currencies

`operation_foundation_geo_record_definitions_currency_business_behavior_enable_default_currencies`

**Inputs** no declared parameters.

**State and service calls** request set\_value on “Currency”.

**Local steps**

- Evaluate Platform.db.set\_value(“Currency”, mapping(“name” → tuple(“in”, DEFAULT\_ENABLED\_CURRENCIES)), “enabled”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0240.json#L4882) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1585) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L350)

## Record · Custom field

[Record definition](../../../../data/record-types/custom_field.json)

<a id="op-efc0b22c21da43"></a>
### Custom Field.autoname

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_autoname`

**Inputs** self.

**Local steps**

- Evaluate self.set\_fieldname().
- Set self.name from ((self.dt + “-”) + self.fieldname).

If control reaches the end, it returns no value.

**Methods declared on this owner** [set fieldname](operations-012.md#op-f90c320af75745).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L2062) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L932)

<a id="op-f90c320af75745"></a>
### Custom Field.set fieldname

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_set_fieldname`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Label is mandatory”.

**Local steps**

- Set restricted from tuple(“name”, “parent”, “creation”, “modified”, …).
- If not self.fieldname.
  - Set label from self.label.
  - If not label.
    - If self.fieldtype belongs to list(“Section Break”, “Column Break”, “Tab Break”).
      - Set label from ((self.fieldtype + “\_”) + str(random\_string(5))).
    - Otherwise.
      - Call the validation error handler Platform.throw(translated “Label is mandatory”).
  - Set self.fieldname from empty text.join(list of c for c drawn from cstr(label).replace(one space, “\_”) where (c.isdigit() or c.isalpha() or c equals “\_”)).
    - Draw c from cstr(label).replace(one space, “\_”), keep a combination only if ((c.isdigit() or c.isalpha() or c equals “\_”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in c.isdigit() → c.isalpha() → c equals “\_”.
  - Set self.fieldname from formatted text custom\_{self.fieldname}.
- Set self.fieldname from self.fieldname.lower().
- If self.fieldname belongs to restricted.
  - Set self.fieldname from (self.fieldname + “1”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L2156) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L937)

<a id="op-77fe327bfb3a0f"></a>
### Custom Field.before insert

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_before_insert`

**Inputs** self.

**Local steps**

- Evaluate self.set\_fieldname().

If control reaches the end, it returns no value.

**Methods declared on this owner** [set fieldname](operations-012.md#op-f90c320af75745).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L2731) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L933)

<a id="op-584d580005dae8"></a>
### Custom Field.validate

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_validate`

**Inputs** self.

**Explicit failure paths** validation helper — translated “A field with the name {0} already exists in {1}”.format(Platform.bold(self.fieldname), self.dt) · validation helper — translated “Fieldtype of {0} in {1} cannot be changed from {2} to {3}”.format(Platform.bold(self.fieldname), self.dt, old\_fieldtype, self.fieldtype) · validation helper — translated “Fieldname not set for Custom Field”.

**Local steps**

- Bind dependencies check\_fieldname\_conflicts.
- Bind dependencies CustomizeForm.
- If (self.is\_new() or self.insert\_after equals “append”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.is\_new() → self.insert\_after equals “append”.
  - Set meta from Platform.get\_meta(self.dt, cached = false).
  - Set fieldnames from list of df.fieldname for df drawn from meta.get(“fields”).
    - Draw df from meta.get(“fields”).
  - If (self.is\_new() and self.fieldname belongs to fieldnames).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.is\_new() → self.fieldname belongs to fieldnames.
    - Call the validation error handler Platform.throw(translated “A field with the name {0} already exists in {1}”.format(Platform.bold(self.fieldname), self.dt)).
  - If self.insert\_after equals “append”.
    - Set self.insert\_after from fieldnames at negative 1.
  - If (self.insert\_after and self.insert\_after belongs to fieldnames).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.insert\_after → self.insert\_after belongs to fieldnames.
    - Set self.idx from (fieldnames.index(self.insert\_after) + 1).
- If (not self.is\_virtual and doc\_before\_save bound to self.get\_doc\_before\_save() and old\_fieldtype bound to doc\_before\_save.fieldtype differs from self.fieldtype and not CustomizeForm.allow\_fieldtype\_change(ol ….
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.is\_virtual → doc\_before\_save bound to self.get\_doc\_before\_save() → old\_fieldtype bound to doc\_before\_save.fieldtype differs from self.fieldtype → not CustomizeForm.allow\_fieldtype\_change(old\_fieldtype, self.fieldtype).
  - Call the validation error handler Platform.throw(translated “Fieldtype of {0} in {1} cannot be changed from {2} to {3}”.format(Platform.bold(self.fieldname), self.dt, old\_fieldtype, self.fieldtype)).
- If not self.fieldname.
  - Call the validation error handler Platform.throw(translated “Fieldname not set for Custom Field”).
- If (self.get(“translatable”, 0) and not supports\_translation(self.fieldtype)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.get(“translatable”, 0) → not supports\_translation(self.fieldtype).
  - Set self.translatable from 0.
- Evaluate check\_fieldname\_conflicts(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L2782) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L938)

<a id="op-88a0ab35f419ad"></a>
### Custom Field.on update

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_on_update`

**Inputs** self.

**Local steps**

- If not self.flags.ignore\_validate.
  - Bind dependencies validate\_fields\_for\_doctype.
  - Evaluate validate\_fields\_for\_doctype(self.dt).
- If not Platform.flags.in\_create\_custom\_fields.
  - Evaluate Platform.clear\_cache(doctype = self.dt).
  - Evaluate Platform.db.updatedb(self.dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L3612) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L936)

<a id="op-34bbaf4f45e678"></a>
### Custom Field.on trash

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_on_trash`

**Inputs** self.

**Record and data access** read “DocType Layout” via get\_all · resolve a document from “DocType Layout” via get\_doc.

**State and service calls** call save on layout\_doc.

**Explicit failure paths** validation helper — translated “Custom Field {0} is created by the Administrator and can only be deleted through the Administrator account.”.format(Platform.bold(self.label)).

**Local steps**

- If (self.owner equals “Administrator” and Platform.session.user differs from “Administrator”).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in self.owner equals “Administrator” → Platform.session.user differs from “Administrator”.
  - Call the validation error handler Platform.throw(translated “Custom Field {0} is created by the Administrator and can only be deleted through the Administrator account.”.format(Platform.bold(self.label))).
- Evaluate delete\_property\_setter(self.dt, field\_name = self.fieldname).
- Set doctype\_layouts from Platform.get\_all(“DocType Layout”, filters = mapping(“document\_type” → self.dt), pluck = “name”).
- For each layout in doctype\_layouts.
  - Set layout\_doc from Platform.get\_doc(“DocType Layout”, layout).
  - For each field in layout\_doc.fields.
    - If field.fieldname equals self.fieldname.
      - Evaluate layout\_doc.remove(field).
      - Evaluate layout\_doc.save().
      - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate Platform.clear\_cache(doctype = self.dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L3783) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L790) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L935)

<a id="op-2d3a8e913e0a36"></a>
### Custom Field.validate insert after

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_validate_insert_after`

**Inputs** self, meta.

**Explicit failure paths** validation helper with Platform.DoesNotExistError — translated “Insert After field '{0}' mentioned in Custom Field '{1}', with label '{2}', does not exist”.format(self.insert\_after, self.name, self.label) · validation helper — translated “Insert After cannot be set as {0}”.format(meta.get\_label(self.insert\_after)).

**Local steps**

- If not meta.get\_field(self.insert\_after).
  - Call the validation error handler Platform.throw(translated “Insert After field '{0}' mentioned in Custom Field '{1}', with label '{2}', does not exist”.format(self.insert\_after, self.name, self.label), Platform.DoesNotExistError).
- If self.fieldname equals self.insert\_after.
  - Call the validation error handler Platform.throw(translated “Insert After cannot be set as {0}”.format(meta.get\_label(self.insert\_after))).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0012.json#L70) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L939)

<a id="op-b1bdae77106c89"></a>
### Custom Field.get permission log options

`operation_foundation_custom_record_definitions_custom_field_business_behavior_custom_field_get_permission_log_options`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** self, event.

**Explicit result forms** a structured result.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L4507) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L789) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L934)

<a id="op-715ca665c7c429"></a>
### Get fields label

`operation_foundation_custom_record_definitions_custom_field_business_behavior_get_fields_label`

**Inputs** doctype = no value.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with translated “Custom Fields cannot be added to core DocTypes.” · msgprint with translated “Custom Fields can only be added to a standard DocType.”.

**Explicit results** Platform.msgprint(translated “Custom Fields cannot be added to core DocTypes.”) · Platform.msgprint(translated “Custom Fields can only be added to a standard DocType.”) · list of mapping(“value” → (df.fieldname or empty text), “label” → \_(df.label, context = df.parent) when df.label, otherwise empty text) for df drawn from Platform.get\_meta(doctype).get(“fields”).

**Local steps**

- Set meta from Platform.get\_meta(doctype).
- If doctype belongs to core\_doctypes\_list.
  - Return Platform.msgprint(translated “Custom Fields cannot be added to core DocTypes.”).
- If meta.custom.
  - Return Platform.msgprint(translated “Custom Fields can only be added to a standard DocType.”).
- Return list of mapping(“value” → (df.fieldname or empty text), “label” → \_(df.label, context = df.parent) when df.label, otherwise empty text) for df drawn from Platform.get\_meta(doctype).get(“fields”).
  - Draw df from Platform.get\_meta(doctype).get(“fields”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in df.fieldname → empty text.
  - Value choice on df.label — true gives \_(df.label, context = df.parent), false gives empty text.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L4713) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L942)

<a id="op-5fce532d1ca01f"></a>
### Create custom field if values exist

`operation_foundation_custom_record_definitions_custom_field_business_behavior_create_custom_field_if_values_exist`

**Inputs** doctype, df.

**Record and data access** read doctype via count.

**Local steps**

- Set df from Platform.\_dict(df).
- If (df.fieldname belongs to Platform.db.get\_table\_columns(doctype) and Platform.db.count(dt = doctype, filters = functions.IfNull(Field(df.fieldname), empty text) differs from empty text)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in df.fieldname belongs to Platform.db.get\_table\_columns(doctype) → Platform.db.count(dt = doctype, filters = functions.IfNull(Field(df.fieldname), empty text) differs from empty text).
  - Evaluate create\_custom\_field(doctype, df).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L5077) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L784) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L929)

<a id="op-3e82ef6b078018"></a>
### Create custom field

`operation_foundation_custom_record_definitions_custom_field_business_behavior_create_custom_field`

**Inputs** doctype, df, ignore\_validate = false, is\_system\_generated = true.

**Record and data access** read “Custom Field” via get\_value · resolve a document from mapping(“doctype” → “Custom Field”, “dt” → doctype, “permlevel” → 0, “fieldtype” → “Data”, …) via get\_doc.

**State and service calls** call insert on custom\_field.

**Explicit results** custom\_field.

**Local steps**

- Set df from Platform.\_dict(df).
- If (not df.fieldname and df.label).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not df.fieldname → df.label.
  - Set df.fieldname from Platform.scrub(df.label).
- If not Platform.db.get\_value(“Custom Field”, mapping(“dt” → doctype, “fieldname” → df.fieldname)).
  - Set custom\_field from Platform.get\_doc(mapping(“doctype” → “Custom Field”, “dt” → doctype, “permlevel” → 0, “fieldtype” → “Data”, …)).
  - Evaluate custom\_field.update(df).
  - Set custom\_field.flags.ignore\_validate from ignore\_validate.
  - Evaluate custom\_field.insert().
  - Return custom\_field.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0122.json#L5308) · [Binding](../../../current-decisions/foundation/bindings-003.tsv#L783) · [Declaration location](../../../current-decisions/foundation/evidence/locations-003.tsv#L928)
