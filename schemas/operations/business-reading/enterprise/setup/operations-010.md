# Company and master data · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Holiday list

[Record definition](../../../../data/record-types/holiday_list.json)

<a id="op-ffae1b20d0e845"></a>
### Holiday List.clear table

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_clear_table`

**Inputs** self.

**Wrappers, in declaration order** Platform.whitelist().

**Local steps**

- Evaluate self.set(“holidays”, list()).
- Evaluate self.update\_total\_holidays().

If control reaches the end, it returns no value.

**Methods declared on this owner** [update total holidays](operations-009.md#op-4318fa0e456f6b).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L1523) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L921) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L470)

<a id="op-c8f1ce36507cac"></a>
### Holiday List.validate duplicate date

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_holiday_list_validate_duplicate_date`

**Inputs** self.

**Explicit failure paths** validation helper — translated “Holiday Date {0} added multiple times”.format(Platform.bold(formatdate(holiday\_date))).

**Local steps**

- Set unique\_dates from list().
- For each holiday\_date in self.get\_holidays().
  - If holiday\_date belongs to unique\_dates.
    - Call the validation error handler Platform.throw(translated “Holiday Date {0} added multiple times”.format(Platform.bold(formatdate(holiday\_date)))).
  - Evaluate unique\_dates.append(holiday\_date).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get holidays](operations-009.md#op-cfb83a5d9ca07c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L132) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L931) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L480)

<a id="op-a8bacc28131a9e"></a>
### Get events

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_get_events`

**Inputs** start, end, filters = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Record and data access** read “Holiday List” via get\_list.

**Explicit results** Platform.get\_list(“Holiday List”, fields = list(“name”, “′tabHoliday′.holiday\_date”, “′tabHoliday′.description”, “′tabHoliday List′.color”), filters = filters, update = mapping(“allDay” → 1)).

**Local steps**

- If filters.
  - Set filters from json.loads(filters).
- Otherwise.
  - Set filters from list().
- If start.
  - Evaluate filters.append(list(“Holiday”, “holiday\_date”, “&gt;”, getdate(start))).
- If end.
  - Evaluate filters.append(list(“Holiday”, “holiday\_date”, “&lt;”, getdate(end))).
- Return Platform.get\_list(“Holiday List”, fields = list(“name”, “′tabHoliday′.holiday\_date”, “′tabHoliday′.description”, “′tabHoliday List′.color”), filters = filters, update = mapping(“allDay” → 1)).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L920) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L469)

<a id="op-db84e03cee2aab"></a>
### Is holiday

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_is_holiday`

**Inputs** holiday\_list, date = no value.

**Record and data access** read “Holiday” via exists.

**Explicit results** bool(Platform.db.exists(“Holiday”, mapping(“parent” → holiday\_list, “holiday\_date” → date, “is\_half\_day” → 0), cache = true)) · false.

**Local steps**

- If date is identical to no value.
  - Set date from today().
- If holiday\_list.
  - Return bool(Platform.db.exists(“Holiday”, mapping(“parent” → holiday\_list, “holiday\_date” → date, “is\_half\_day” → 0), cache = true)).
- Otherwise.
  - Return false.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L2222) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L933) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L482)

<a id="op-dd5b08472710e8"></a>
### Is half holiday

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_is_half_holiday`

**Inputs** holiday\_list, date = no value.

**Record and data access** read “Holiday” via exists.

**Explicit results** bool(Platform.db.exists(“Holiday”, mapping(“parent” → holiday\_list, “holiday\_date” → date, “is\_half\_day” → 1), cache = true)) · false.

**Local steps**

- If date is identical to no value.
  - Set date from today().
- If holiday\_list.
  - Return bool(Platform.db.exists(“Holiday”, mapping(“parent” → holiday\_list, “holiday\_date” → date, “is\_half\_day” → 1), cache = true)).
- Otherwise.
  - Return false.

**Values supplied outside this operation** clock or generated value from today().

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L2432) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L932) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L481)

<a id="op-2d1129f0a1528b"></a>
### Local country name

`operation_enterprise_setup_record_definitions_holiday_list_business_behavior_local_country_name`

**Inputs** country\_code.

**Declared result** str.

**Explicit results** Locale.parse(Platform.local.lang, sep = “-”).territories.get(country\_code, country\_code).

**Local steps**

- Bind dependencies Locale.
- Return Locale.parse(Platform.local.lang, sep = “-”).territories.get(country\_code, country\_code).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L2642) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L934) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L483)

<a id="op-ef4e2f42c02059"></a>
### Get data

`operation_enterprise_setup_record_definitions_holiday_list_holiday_list_dashboard_business_behavior_get_data`

**Inputs** no declared parameters.

**Explicit results** mapping(“fieldname” → “holiday\_list”, “non\_standard\_fieldnames” → mapping(“Company” → “default\_holiday\_list”), “transactions” → list(mapping(“items” → list(“Company”, “Employee”, “Workstation”)), mapping(“ ….

**Local steps**

- Return mapping(“fieldname” → “holiday\_list”, “non\_standard\_fieldnames” → mapping(“Company” → “default\_holiday\_list”), “transactions” → list(mapping(“items” → list(“Company”, “Employee”, “Workstation”)), mapping(“ ….

**Boundaries to resolve** abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0693.json#L2755) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L935) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L484)

## Record · Incoterm

[Record definition](../../../../data/record-types/incoterm.json)

<a id="op-ce10e123e97e57"></a>
### Create incoterms

`operation_enterprise_setup_record_definitions_incoterm_business_behavior_create_incoterms`

**Inputs** no declared parameters.

**Record and data access** read “Incoterm” via exists.

**State and service calls** request new\_doc for “Incoterm” · call save on doc.

**Local steps**

- Bind dependencies os.
- Bind dependencies DictReader.
- Within open(os.path.join(os.path.dirname(\_\_file\_\_), “incoterms.csv”)) bound as f.
  - For each incoterm in DictReader(f).
    - If Platform.db.exists(“Incoterm”, incoterm at “code”).
      - Continue with the next iteration or loop test.
    - Set doc from Platform.new\_doc(“Incoterm”).
    - Evaluate doc.update(incoterm).
    - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0694.json#L811) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L946) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L495)

## Service · Install

<a id="op-69871d88269d46"></a>
### After install

`operation_enterprise_setup_install_business_behavior_after_install`

**Inputs** no declared parameters.

**Record and data access** read “Role” via exists · resolve a document from mapping(“doctype” → “Role”, “role\_name” → “Analytics”) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Role”, “role\_name” → “Analytics”)) · commit.

**Local steps**

- If not Platform.db.exists(“Role”, “Analytics”).
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Role”, “role\_name” → “Analytics”)).insert().
- Evaluate set\_single\_defaults().
- Evaluate setup\_repost\_defaults().
- Evaluate create\_print\_setting\_custom\_fields().
- Evaluate create\_marketing\_campaign\_custom\_fields().
- Evaluate create\_address\_and\_contact\_custom\_fields().
- Evaluate setup\_company\_address\_permissions().
- Evaluate create\_custom\_company\_links().
- Evaluate add\_all\_roles\_to(“Administrator”).
- Evaluate create\_default\_success\_action().
- Evaluate create\_incoterms().
- Evaluate create\_default\_role\_profiles().
- Evaluate add\_company\_to\_session\_defaults().
- Evaluate add\_standard\_navbar\_items().
- Evaluate add\_app\_name().
- Evaluate update\_roles().
- Evaluate make\_default\_operations().
- Evaluate update\_pegged\_currencies().
- Evaluate set\_default\_print\_formats().
- Evaluate create\_letter\_head().
- Evaluate toggle\_hidden\_fields().
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L52) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L677) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L250)

<a id="op-3df0af1dc45ed7"></a>
### Make default operations

`operation_enterprise_setup_install_business_behavior_make_default_operations`

**Inputs** no declared parameters.

**Record and data access** read “Operation” via exists · resolve a document from mapping(“doctype” → “Operation”, “name” → operation) via get\_doc.

**State and service calls** call insert on doc.

**Local steps**

- For each operation in list(“Assembly”).
  - If not Platform.db.exists(“Operation”, operation).
    - Set doc from Platform.get\_doc(mapping(“doctype” → “Operation”, “name” → operation)).
    - Set doc.flags.ignore\_mandatory from true.
    - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L1304) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L685) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L257)

<a id="op-ce0248f0782d2f"></a>
### Set single defaults

`operation_enterprise_setup_install_business_behavior_set_single_defaults`

**Inputs** no declared parameters.

**Record and data access** execute query text (SELECT, Doc Field) · resolve a document from dt via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- For each dt in tuple(“Accounts Settings”, “Print Settings”, “Buying Settings”, “Selling Settings”, …).
  - Set default\_values from Platform.db.sql(query text (SELECT, Doc Field), dt).
  - If default\_values.
    - Attempt the following.
      - Set doc from Platform.get\_doc(dt, dt).
      - For each tuple(fieldname, value) in default\_values.
        - Evaluate doc.set(fieldname, value).
      - Set doc.flags.ignore\_mandatory from true.
      - Evaluate doc.save().
    - On failure (Platform.ValidationError).
      - Take no action here.
- Evaluate setup\_currency\_exchange().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L55) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L259)

<a id="op-21e2c4e461f8b6"></a>
### Setup repost defaults

`operation_enterprise_setup_install_business_behavior_setup_repost_defaults`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Accounts Settings” via get\_doc.

**State and service calls** call save on accounts\_settings.

**Local steps**

- Set accounts\_settings from Platform.get\_doc(“Accounts Settings”).
- For each x in Platform.get\_hooks(“repost\_allowed\_doctypes”).
  - Evaluate accounts\_settings.append(“repost\_allowed\_types”, mapping(“document\_type” → x)).
- Evaluate accounts\_settings.save().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“repost\_allowed\_doctypes”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L2055) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L261)

<a id="op-81b15753523689"></a>
### Setup currency exchange

`operation_enterprise_setup_install_business_behavior_setup_currency_exchange`

**Inputs** no declared parameters.

**Record and data access** read “Currency Exchange Settings” via get\_single.

**State and service calls** call save on ces.

**Local steps**

- Set ces from Platform.get\_single(“Currency Exchange Settings”).
- Attempt the following.
  - Set ces.service\_provider from “frankfurter.dev - v2”.
  - Evaluate ces.save().
- On failure (Platform.ValidationError).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L2213) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L260)

<a id="op-593a58f62d22c0"></a>
### Create print setting custom fields

`operation_enterprise_setup_install_business_behavior_create_print_setting_custom_fields`

**Inputs** no declared parameters.

**Local steps**

- Evaluate create\_custom\_fields(mapping(“Print Settings” → list(mapping(“label” → translated “Compact Item Print”, “fieldname” → “compact\_item\_print”, “fieldtype” → “Check”, “default” → “1”, …), mapping(“label” → tra ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L2332) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L683) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L256)

<a id="op-7044659fff8778"></a>
### Create marketing campaign custom fields

`operation_enterprise_setup_install_business_behavior_create_marketing_campaign_custom_fields`

**Inputs** no declared parameters.

**Local steps**

- Evaluate create\_custom\_fields(mapping(“UTM Campaign” → list(mapping(“label” → translated “Messaging CRM Campaign”, “fieldname” → “crm\_campaign”, “fieldtype” → “Link”, “options” → “Campaign”, …)))).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L2699) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L682) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L255)

<a id="op-8e6c988aa85b20"></a>
### Create address and contact custom fields

`operation_enterprise_setup_install_business_behavior_create_address_and_contact_custom_fields`

**Inputs** no declared parameters.

**Local steps**

- Evaluate create\_custom\_fields(mapping(“Address” → list(mapping(“label” → translated “Tax Category”, “fieldname” → “tax\_category”, “fieldtype” → “Link”, “options” → “Tax Category”, …), mapping(“label” → translated “ ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L53) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L678) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L251)

<a id="op-87607f5187582f"></a>
### Setup company address permissions

`operation_enterprise_binding_enterprise_setup_install_setup_company_address_permissions`

**Control responsibility** Access control. Document ownership, effective roles, shares and scope determine which operation the caller is authorized to perform.

**Declared inputs** no parameters.

**Local structure** 0 condition or selection sites, 1 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L130) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L187)

<a id="op-21bb4f6be8ad41"></a>
### Create default success action

`operation_enterprise_setup_install_business_behavior_create_default_success_action`

**Inputs** no declared parameters.

**Record and data access** read “Success Action” via exists · resolve a document from success\_action via get\_doc.

**State and service calls** call insert on doc.

**Local steps**

- For each success\_action in get\_default\_success\_action().
  - If not Platform.db.exists(“Success Action”, success\_action.get(“ref\_doctype”)).
    - Set doc from Platform.get\_doc(success\_action).
    - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L3258) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L681) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L254)

<a id="op-efcc3cb493fae4"></a>
### Create custom company links

`operation_enterprise_setup_install_business_behavior_create_custom_company_links`

**Inputs** no declared parameters.

**Local steps**

- Evaluate create\_custom\_fields(mapping(“Email Account” → list(mapping(“label” → translated “Company”, “fieldname” → “company”, “fieldtype” → “Link”, “options” → “Company”, …)), “Communication” → list(mapping(“label” ….

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L3427) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L679) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L252)

<a id="op-cae0e1879477b9"></a>
### Add company to session defaults

`operation_enterprise_setup_install_business_behavior_add_company_to_session_defaults`

**Control responsibility** Identity and credential handling. The current identity, configured authentication provider and credential lifecycle determine the applicable control. Credential material stays with its authorized provider.

**Declared inputs** no parameters.

**Observed service boundaries** record mutation request.

**Local structure** 0 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L3775) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L673) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L246)

<a id="op-f0a14dde3757a6"></a>
### Add standard navbar items

`operation_enterprise_setup_install_business_behavior_add_standard_navbar_items`

**Inputs** no declared parameters.

**Record and data access** read “Navbar Settings” via get\_single.

**State and service calls** call save on navbar\_settings.

**Local steps**

- Set navbar\_settings from Platform.get\_single(“Navbar Settings”).
- Set Enterprise\_navbar\_items from list(mapping(“item\_label” → translated “Documentation”, “item\_type” → “Route”, “route” → text in the contract, “is\_standard” → 1), mapping(“item\_label” → translated “User Forum”, “item\_type” → “Route”, “ro ….
- Set current\_navbar\_items from navbar\_settings.help\_dropdown.
- Evaluate navbar\_settings.set(“help\_dropdown”, list()).
- For each item in Enterprise\_navbar\_items.
  - Set current\_labels from list of item.get(“item\_label”) for item drawn from current\_navbar\_items.
    - Draw item from current\_navbar\_items.
  - If item.get(“item\_label”) does not belong to current\_labels.
    - Evaluate navbar\_settings.append(“help\_dropdown”, item).
- For each item in current\_navbar\_items.
  - Evaluate navbar\_settings.append(“help\_dropdown”, mapping(“item\_label” → item.item\_label, “item\_type” → item.item\_type, “route” → item.route, “action” → item.action, …)).
- Evaluate navbar\_settings.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L3904) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L674) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L247)

<a id="op-c1979682501c29"></a>
### Add app name

`operation_enterprise_setup_install_business_behavior_add_application_name`

**Inputs** no declared parameters.

**State and service calls** request set\_single\_value on “System Settings”.

**Local steps**

- Evaluate Platform.db.set\_single\_value(“System Settings”, “app\_name”, “Enterprise”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L4705) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L672) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L245)

<a id="op-db4dda7c140ade"></a>
### Update roles

`operation_enterprise_setup_install_business_behavior_update_roles`

**Inputs** no declared parameters.

**State and service calls** request set\_value on “Role”.

**Local steps**

- Set website\_user\_roles from tuple(“Customer”, “Supplier”).
- For each role in website\_user\_roles.
  - Evaluate Platform.db.set\_value(“Role”, role, “desk\_access”, 0).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L4773) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L692) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L264)

<a id="op-1f645cdc9ce3ce"></a>
### Create default role profiles

`operation_enterprise_setup_install_business_behavior_create_default_role_profiles`

**Inputs** no declared parameters.

**Record and data access** read “Role Profile” via exists · resolve a document from “Role Profile” via get\_doc.

**State and service calls** call save on role\_profile · request new\_doc for “Role Profile” · call insert on role\_profile.

**Local steps**

- For each tuple(role\_profile\_name, roles) in DEFAULT\_ROLE\_PROFILES.items().
  - If Platform.db.exists(“Role Profile”, role\_profile\_name).
    - Set role\_profile from Platform.get\_doc(“Role Profile”, role\_profile\_name).
    - Set existing\_roles from list of row.role for row drawn from role\_profile.roles.
      - Draw row from role\_profile.roles.
    - Set role\_profile.roles from list of row for row drawn from role\_profile.roles where row.role belongs to roles.
      - Draw row from role\_profile.roles, keep a combination only if (row.role belongs to roles).
    - For each role in roles.
      - If role does not belong to existing\_roles.
        - Evaluate role\_profile.append(“roles”, mapping(“role” → role)).
    - Evaluate role\_profile.save(ignore\_permissions = true).
    - Continue with the next iteration or loop test.
  - Set role\_profile from Platform.new\_doc(“Role Profile”).
  - Set role\_profile.role\_profile from role\_profile\_name.
  - For each role in roles.
    - Evaluate role\_profile.append(“roles”, mapping(“role” → role)).
  - Evaluate role\_profile.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L4892) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L680) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L253)
