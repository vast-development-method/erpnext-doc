# Record lifecycle and persistence · operations 58

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Installed applications

[Record definition](../../../../data/record-types/installed_applications.json)

<a id="op-2b81ed94685523"></a>
### Installed Applications.update versions

`operation_foundation_core_record_definitions_installed_applications_business_behavior_installed_applications_update_versions`

**Inputs** self.

**State and service calls** savepoint savepoint · call save on self · rollback · request set\_single\_value on “System Settings”.

**Local steps**

- Evaluate self.reload\_doc\_if\_required().
- Set app\_wise\_setup\_details from self.get\_app\_wise\_setup\_details().
- Evaluate self.delete\_key(“installed\_applications”).
- For each app in Platform.utils.get\_installed\_apps\_info().
  - Set has\_setup\_wizard from 1.
  - Set setup\_complete from (app\_wise\_setup\_details.get(app.get(“app\_name”)) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_wise\_setup\_details.get(app.get(“app\_name”)) → 0.
  - If (app.get(“app\_name”) belongs to list(“Platform”, “Enterprise”) and not setup\_complete).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in app.get(“app\_name”) belongs to list(“Platform”, “Enterprise”) → not setup\_complete.
    - If (app.get(“app\_name”) equals “Platform” and has\_non\_admin\_user()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in app.get(“app\_name”) equals “Platform” → has\_non\_admin\_user().
      - Set setup\_complete from 1.
    - If (app.get(“app\_name”) equals “Enterprise” and has\_company()).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in app.get(“app\_name”) equals “Enterprise” → has\_company().
      - Set setup\_complete from 1.
  - If app.get(“app\_name”) does not belong to list(“Platform”, “Enterprise”).
    - Set setup\_complete from 0.
    - Set has\_setup\_wizard from 0.
  - Evaluate self.append(“installed\_applications”, mapping(“app\_name” → app.get(“app\_name”), “app\_version” → (app.get(“version”) or “UNVERSIONED”), “git\_branch” → (app.get(“branch”) or “UNVERSIONED”), “has\_setup\_wizard ….
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app.get(“version”) → “UNVERSIONED”.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in app.get(“branch”) → “UNVERSIONED”.
- Attempt the following.
  - Set savepoint from “update\_installed\_apps”.
  - Evaluate Platform.db.savepoint(savepoint).
  - Evaluate self.save().
- On failure (Platform.db.DataError).
  - Evaluate Platform.db.rollback(save\_point = savepoint).
  - Evaluate self.save(ignore\_version = true).
- Evaluate Platform.clear\_cache(doctype = “System Settings”).
- Evaluate Platform.db.set\_single\_value(“System Settings”, “setup\_complete”, Platform.is\_setup\_complete()).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reload doc if required](operations-058.md#op-a86ab60e178b6a), [get app wise setup details](operations-058.md#op-f3121ff5c8b743).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L78) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1679) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1635)

<a id="op-f3121ff5c8b743"></a>
### Installed Applications.get app wise setup details

`operation_foundation_core_record_definitions_installed_applications_business_behavior_installed_applications_get_application_wise_setup_details`

**Inputs** self.

**Record and data access** read “Installed Application” via get\_all.

**Explicit results** Platform.\_dict(Platform.get\_all(“Installed Application”, fields = list(“app\_name”, “is\_setup\_complete”), filters = mapping(“has\_setup\_wizard” → 1), as\_list = true)).

**Local steps**

- Return Platform.\_dict(Platform.get\_all(“Installed Application”, fields = list(“app\_name”, “is\_setup\_complete”), filters = mapping(“has\_setup\_wizard” → 1), as\_list = true)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L4226) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1677) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1633)

<a id="op-a86ab60e178b6a"></a>
### Installed Applications.reload doc if required

`operation_foundation_core_record_definitions_installed_applications_business_behavior_installed_applications_reload_record_if_required`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If Platform.db.has\_column(“Installed Application”, “is\_setup\_complete”).
  - Return no value.
- Evaluate Platform.reload\_doc(“core”, “doctype”, “installed\_application”).
- Evaluate Platform.reload\_doc(“core”, “doctype”, “installed\_applications”).
- Evaluate Platform.reload\_doc(“integrations”, “doctype”, “webhook”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L77) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1678) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1634)

<a id="op-d7762d5c787570"></a>
### Has non admin user

`operation_foundation_core_record_definitions_installed_applications_business_behavior_has_non_admin_user`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_value.

**Explicit results** true · false.

**Local steps**

- If (Platform.db.has\_table(“User”) and Platform.db.get\_value(“User”, mapping(“user\_type” → “System User”, “name” → list(“not in”, list(“Administrator”, “Guest”))))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.has\_table(“User”) → Platform.db.get\_value(“User”, mapping(“user\_type” → “System User”, “name” → list(“not in”, list(“Administrator”, “Guest”)))).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L4577) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1676) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1632)

<a id="op-742b9022ad1024"></a>
### Has company

`operation_foundation_core_record_definitions_installed_applications_business_behavior_has_company`

**Inputs** no declared parameters.

**Record and data access** read “Company” via get\_all.

**Explicit results** true · false.

**Local steps**

- If (Platform.db.has\_table(“Company”) and Platform.get\_all(“Company”, limit = 1)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.has\_table(“Company”) → Platform.get\_all(“Company”, limit = 1).
  - Return true.
- Return false.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L4739) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1631)

<a id="op-f76b0dc2c0dfae"></a>
### Update installed apps order

`operation_foundation_core_record_definitions_installed_applications_business_behavior_update_installed_apps_order`

**Inputs** new\_order.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** call insert on new\_order.

**Explicit failure paths** validation helper with InvalidAppOrder — translated “You are only allowed to update order, do not remove or add apps.”.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- If isinstance(new\_order, str).
  - Set new\_order from json.loads(new\_order).
- Evaluate (Platform.local.request\_cache and Platform.local.request\_cache.clear()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.local.request\_cache → Platform.local.request\_cache.clear().
- Set existing\_order from Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
- If (set(existing\_order) differs from set(new\_order) or not isinstance(new\_order, list)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in set(existing\_order) differs from set(new\_order) → not isinstance(new\_order, list).
  - Call the validation error handler Platform.throw(translated “You are only allowed to update order, do not remove or add apps.”, exc = InvalidAppOrder).
- If “Platform” belongs to new\_order.
  - Evaluate new\_order.remove(“Platform”).
- Evaluate new\_order.insert(0, “Platform”).
- Evaluate Platform.db.set\_global(“installed\_apps”, json.dumps(new\_order)).
- Evaluate \_create\_version\_log\_for\_change(existing\_order, new\_order).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0011.json#L79) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1681) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1636)

<a id="op-4b0d807e18779b"></a>
### Create version log for change

`operation_foundation_core_record_definitions_installed_applications_business_behavior_create_version_log_for_change`

**Inputs** old, new.

**State and service calls** request new\_doc for “Version” · call insert on version.

**Local steps**

- Set version from Platform.new\_doc(“Version”).
- Set version.ref\_doctype from “DefaultValue”.
- Set version.docname from “installed\_apps”.
- Set version.data from Platform.as\_json(mapping(“changed” → list(list(“current”, json.dumps(old), json.dumps(new))))).
- Set version.flags.ignore\_links from true.
- Set version.flags.ignore\_permissions from true.
- Evaluate version.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L5331) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1625)

<a id="op-ef1a9853021eee"></a>
### Get installed app order

`operation_foundation_core_record_definitions_installed_applications_business_behavior_get_installed_application_order`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Declared result** list at str.

**Explicit results** Platform.get\_installed\_apps(\_ensure\_on\_bench = true).

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Return Platform.get\_installed\_apps(\_ensure\_on\_bench = true).

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L5793) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1671) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1627)

<a id="op-b2d4fce6e96d84"></a>
### Get setup wizard completed apps

`operation_foundation_core_record_definitions_installed_applications_business_behavior_get_setup_wizard_completed_apps`

**Inputs** no declared parameters.

**Explicit results** list of a.app\_name for a drawn from apps.installed\_applications where (a.has\_setup\_wizard and a.is\_setup\_complete).

**Local steps**

- Set apps from Platform.client\_cache.get\_doc(“Installed Applications”).
- Return list of a.app\_name for a drawn from apps.installed\_applications where (a.has\_setup\_wizard and a.is\_setup\_complete).
  - Draw a from apps.installed\_applications, keep a combination only if ((a.has\_setup\_wizard and a.is\_setup\_complete)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.has\_setup\_wizard → a.is\_setup\_complete.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L5900) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1672) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1628)

<a id="op-0c0fccc1206877"></a>
### Get setup wizard not required apps

`operation_foundation_core_record_definitions_installed_applications_business_behavior_get_setup_wizard_not_required_apps`

**Inputs** no declared parameters.

**Explicit results** list of a.app\_name for a drawn from apps.installed\_applications where not a.has\_setup\_wizard.

**Local steps**

- Set apps from Platform.client\_cache.get\_doc(“Installed Applications”).
- Return list of a.app\_name for a drawn from apps.installed\_applications where not a.has\_setup\_wizard.
  - Draw a from apps.installed\_applications, keep a combination only if (not a.has\_setup\_wizard).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6019) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1673) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1629)

<a id="op-da5131c8dab68d"></a>
### Get apps with incomplete dependencies

`operation_foundation_core_record_definitions_installed_applications_business_behavior_get_apps_with_incomplete_dependencies`

**Inputs** current\_app.

**Wrappers, in declaration order** Platform.request\_cache.

**Explicit results** pending\_apps.

**Local steps**

- Set dependent\_apps from list(“Platform”).
- If apps bound to Platform.get\_hooks(“required\_apps”, app\_name = current\_app).
  - Evaluate dependent\_apps.extend(apps).
- Set parsed\_apps from list().
- For each apps in dependent\_apps.
  - Set apps from apps.split(“/”).
  - Evaluate parsed\_apps.extend(apps).
- Set pending\_apps from get\_setup\_wizard\_pending\_apps(parsed\_apps).
- Return pending\_apps.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“required\_apps”, app\_name = current\_app).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6128) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1626)

<a id="op-345c232a5a05a0"></a>
### Get setup wizard pending apps

`operation_foundation_core_record_definitions_installed_applications_business_behavior_get_setup_wizard_pending_apps`

**Inputs** apps = no value.

**Explicit results** pending\_apps.

**Local steps**

- Set apps from Platform.client\_cache.get\_doc(“Installed Applications”).
- Set pending\_apps from list of a.app\_name for a drawn from apps.installed\_applications where (a.has\_setup\_wizard and not a.is\_setup\_complete).
  - Draw a from apps.installed\_applications, keep a combination only if ((a.has\_setup\_wizard and not a.is\_setup\_complete)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in a.has\_setup\_wizard → not a.is\_setup\_complete.
- If apps.
  - Set pending\_apps from list of a for a drawn from pending\_apps where a belongs to apps.
    - Draw a from pending\_apps, keep a combination only if (a belongs to apps).
- Return pending\_apps.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6370) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1674) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1630)

## Record · Language

[Record definition](../../../../data/record-types/language.json)

<a id="op-1aa7c863326a14"></a>
### Language.validate

`operation_foundation_core_record_definitions_language_business_behavior_language_validate`

**Inputs** self.

**Local steps**

- Evaluate validate\_with\_regex(self.language\_code, “Language Code”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6703) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1686) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1641)

<a id="op-b7e5946a20f317"></a>
### Language.before rename

`operation_foundation_core_record_definitions_language_business_behavior_language_before_rename`

**Inputs** self, old, new, merge = false.

**Local steps**

- Evaluate validate\_with\_regex(new, “Name”).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6763) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1683) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1638)

<a id="op-03ab77bd6053a3"></a>
### Language.on update

`operation_foundation_core_record_definitions_language_business_behavior_language_on_update`

**Inputs** self.

**Local steps**

- Evaluate Platform.cache.delete\_value(“languages\_with\_name”).
- Evaluate Platform.client\_cache.delete\_value(“languages”).
- Evaluate self.update\_user\_defaults().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update user defaults](operations-058.md#op-a8075548465d69).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6844) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1684) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1639)

<a id="op-a8075548465d69"></a>
### Language.update user defaults

`operation_foundation_core_record_definitions_language_business_behavior_language_update_user_defaults`

**Inputs** self.

**Record and data access** read “User” via get\_all.

**Local steps**

- Set users from Platform.get\_all(“User”, filters = mapping(“language” → self.name), pluck = “name”).
- For each key in tuple(“date\_format”, “time\_format”, “number\_format”, “first\_day\_of\_the\_week”).
  - If self.has\_value\_changed(key).
    - For each user in users.
      - If new\_value bound to self.get(key).
        - Evaluate set\_default(key, new\_value, user).
      - Otherwise.
        - Evaluate clear\_default(key, parent = user).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L6950) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1685) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1640)

<a id="op-5de083a4d1ef59"></a>
### Validate with regex

`operation_foundation_core_record_definitions_language_business_behavior_validate_with_regular_expression`

**Inputs** name, label.

**Explicit failure paths** validation helper — translated “{0} must begin and end with a letter and can only contain letters, hyphen or underscore.”.format(label).

**Local steps**

- Set pattern from re.compile(“^&#91;a-zA-Z&#93;+&#91;-\_&#93;\*&#91;a-zA-Z&#93;+$”).
- If not pattern.match(name).
  - Call the validation error handler Platform.throw(translated “{0} must begin and end with a letter and can only contain letters, hyphen or underscore.”.format(label)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0086.json#L7253) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1643)

<a id="op-99b40cfe4e749c"></a>
### Sync languages

`operation_foundation_core_record_definitions_language_business_behavior_sync_languages`

**Inputs** no declared parameters.

**Record and data access** read “Language” via exists.

**State and service calls** request new\_doc for “Language” · call insert on doc.

**Local steps**

- Bind dependencies DictReader.
- Within open(Platform.get\_app\_path(“Platform”, “geo”, “languages.csv”), encoding = “utf-8”) bound as f.
  - Set reader from DictReader(f).
  - For each row in reader.
    - If not Platform.db.exists(“Language”, row at “language\_code”).
      - Set doc from Platform.new\_doc(“Language”).
      - Evaluate doc.update(row).
      - Evaluate doc.insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0087.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1642)

## Service · Lazytranslatedstring

<a id="op-2c56d9ee220979"></a>
### Lazy Translate.initialize

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_initialize`

**Inputs** self, msg, lang = no value, context = no value.

**Declared result** no value.

**Local steps**

- Set self.msg from msg.
- Set self.lang from lang.
- Set self.context from context.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4343) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L824) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1452)

<a id="op-571530cb65f072"></a>
### Lazy Translate.value

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_value`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** str.

**Explicit results** \_(str(self.msg), self.lang, self.context).

**Local steps**

- Return \_(str(self.msg), self.lang, self.context).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4482) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L829) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1457)

<a id="op-22f05cf80e7748"></a>
### Lazy Translate.str

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_text`

**Inputs** self.

**Explicit results** self.value.

**Local steps**

- Return self.value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4574) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L828) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1456)

<a id="op-1aa2028ba5ba71"></a>
### Lazy Translate.add

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_add`

**Inputs** self, other.

**Explicit results** (self.value + str(other)).

**Explicit failure paths** NotImplementedError.

**Local steps**

- If isinstance(other, (str bitwise or \_LazyTranslate)).
  - Return (self.value + str(other)).
- Raise NotImplementedError.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4615) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1450)

<a id="op-c0de5f84224242"></a>
### Lazy Translate.radd

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_radd`

**Inputs** self, other.

**Explicit results** (str(other) + self.value) · NotImplementedError.

**Local steps**

- If isinstance(other, (str bitwise or \_LazyTranslate)).
  - Return (str(other) + self.value).
- Return NotImplementedError.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4730) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L826) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1454)

<a id="op-589c6a2147179f"></a>
### Lazy Translate.repr

`operation_foundation_types_lazytranslatedstring_business_behavior_lazy_translate_representation`

**Inputs** self.

**Declared result** str.

**Explicit results** formatted text '{self.value}'.

**Local steps**

- Return formatted text '{self.value}'.

[Applicable decision contract](../../../foundation-decision-contracts/part-0458.json#L4840) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L827) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1455)
