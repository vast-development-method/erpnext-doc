# Company and master data · operations 11

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Install

<a id="op-d29856432f7146"></a>
### Update pegged currencies

`operation_enterprise_setup_install_business_behavior_update_pegged_currencies`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Pegged Currencies” via get\_doc · read “Currency” via get\_list.

**State and service calls** call save on doc.

**Explicit results** no value.

**Local steps**

- Set doc from Platform.get\_doc(“Pegged Currencies”, “Pegged Currencies”).
- Set existing\_sources from set of item.source\_currency for item drawn from doc.pegged\_currency\_item.
  - Draw item from doc.pegged\_currency\_item.
- Set currencies\_to\_add from list(mapping(“source\_currency” → “AED”, “pegged\_against” → “USD”, “pegged\_exchange\_rate” → 3.6725), mapping(“source\_currency” → “BHD”, “pegged\_against” → “USD”, “pegged\_exchange\_rate” → 0.376), mapping(“so ….
- Set currencies\_exist from Platform.db.get\_list(“Currency”, mapping(“name” → list(“in”, list(“AED”, “BHD”, “JOD”, “OMR”, …))), pluck = “name”).
- If “USD” does not belong to currencies\_exist.
  - Return no value.
- For each currency in currencies\_to\_add.
  - If (currency at “source\_currency” belongs to currencies\_exist and currency at “source\_currency” does not belong to existing\_sources).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in currency at “source\_currency” belongs to currencies\_exist → currency at “source\_currency” does not belong to existing\_sources.
    - Evaluate doc.append(“pegged\_currency\_item”, currency).
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0700.json#L5385) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L691) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L263)

<a id="op-aae5eeb3cfe8c0"></a>
### Set default print formats

`operation_enterprise_setup_install_business_behavior_set_default_print_formats`

**Inputs** no declared parameters.

**Record and data access** read “Print Format” via exists.

**Local steps**

- Set doctypes from tuple(“Sales Order”, “Sales Invoice”, “Delivery Note”, “Purchase Order”, …).
- For each doctype in doctypes.
  - If Platform.get\_meta(doctype).default\_print\_format.
    - Continue with the next iteration or loop test.
  - Set print\_format from formatted text {doctype} Classic.
  - If not Platform.db.exists(“Print Format”, print\_format).
    - Continue with the next iteration or loop test.
  - Evaluate Platform.make\_property\_setter(mapping(“doctype” → doctype, “doctype\_or\_field” → “DocType”, “property” → “default\_print\_format”, “value” → print\_format, …), validate\_fields\_for\_doctype = false).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L54) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L686) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L258)

<a id="op-e3d69f6368183a"></a>
### Create letter head

`operation_enterprise_binding_enterprise_setup_install_create_letter_head`

**Inputs** no declared parameters.

**Record and data access** read “Letter Head” via exists · resolve a document from mapping(“doctype” → “Letter Head”, “letter\_head\_name” → name, “source” → “HTML”, “content” → content, …) via get\_doc.

**State and service calls** call insert on doc.

**Local steps**

- Set base\_path from Platform.get\_app\_path(“Enterprise”, “accounts”, “letterhead”).
- Set letterheads from mapping(“Company Letterhead” → “company\_letterhead.html”, “Company Letterhead - Grey” → “company\_letterhead\_grey.html”).
- For each tuple(name, filename) in letterheads.items().
  - If not Platform.db.exists(“Letter Head”, name).
    - Set content from Platform.read\_file(os.path.join(base\_path, filename)).
    - Set doc from Platform.get\_doc(mapping(“doctype” → “Letter Head”, “letter\_head\_name” → name, “source” → “HTML”, “content” → content, …)).
      - Value choice on name equals “Company Letterhead - Grey” — true gives 1, false gives 0.
    - Evaluate doc.insert(ignore\_permissions = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L127) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L687) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L184)

<a id="op-54b7721960a92d"></a>
### Toggle hidden fields

`operation_enterprise_setup_install_business_behavior_toggle_hidden_fields`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Accounts Settings” via get\_doc · resolve a document from “Selling Settings” via get\_doc.

**Local steps**

- Bind dependencies toggle\_accounting\_dimension\_sections, toggle\_loyalty\_point\_program\_section, toggle\_sales\_discount\_section, toggle\_subscription\_sections.
- Bind dependencies toggle\_tracking\_sales\_commissions\_section, toggle\_utm\_analytics\_section.
- Set acc\_settings from Platform.get\_doc(“Accounts Settings”).
- Evaluate toggle\_accounting\_dimension\_sections(not acc\_settings.enable\_accounting\_dimensions).
- Evaluate toggle\_sales\_discount\_section(not acc\_settings.enable\_discounts\_and\_margin).
- Evaluate toggle\_subscription\_sections(not acc\_settings.enable\_subscription).
- Evaluate toggle\_loyalty\_point\_program\_section(not acc\_settings.enable\_loyalty\_point\_program).
- Set selling\_settings from Platform.get\_doc(“Selling Settings”).
- Evaluate toggle\_tracking\_sales\_commissions\_section(not selling\_settings.enable\_tracking\_sales\_commissions).
- Evaluate toggle\_utm\_analytics\_section(not selling\_settings.enable\_utm).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0035.json#L56) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L690) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L262)

<a id="op-9d9e6b70c253e6"></a>
### Grant address read to accounts manager

`operation_enterprise_binding_enterprise_setup_install_grant_address_read_to_accounts_manager`

**Inputs** no declared parameters.

**Record and data access** read “Role” via exists.

**Explicit results** no value.

**Local steps**

- Bind dependencies add\_permission, get\_all\_perms, update\_permission\_property.
- If not Platform.db.exists(“Role”, “Accounts Manager”).
  - Return no value.
- Set has\_rule from false.
- For each perm in get\_all\_perms(“Accounts Manager”).
  - If perm.parent equals “Address”.
    - Set has\_rule from true.
- If (has\_rule or “Accounts Manager” belongs to get\_changed\_roles(“Address”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in has\_rule → “Accounts Manager” belongs to get\_changed\_roles(“Address”).
  - Evaluate print(“Address / Accounts Manager: kept, this site already rules on this pair”).
  - Return no value.
- Evaluate add\_permission(“Address”, “Accounts Manager”, 0, “read”).
- Evaluate update\_permission\_property(“Address”, “Accounts Manager”, 0, “export”, …).
- Evaluate Platform.clear\_cache(doctype = “Address”).
- Evaluate print(“Address / Accounts Manager: added read”).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L129) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L689) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L186)

<a id="op-0c55127ddb7ba6"></a>
### Get changed roles

`operation_enterprise_binding_enterprise_setup_install_get_changed_roles`

**Inputs** doctype, statuses = tuple(“Updated”, “Removed”).

**Declared result** set.

**Record and data access** read “DocType” via exists · read “Permission Log” via get\_all · read “Custom DocPerm” via get\_value.

**Explicit results** set() · roles.

**Local steps**

- If not Platform.db.exists(“DocType”, “Permission Log”).
  - Return set().
- Set logs from Platform.get\_all(“Permission Log”, filters = mapping(“for\_doctype” → “DocType”, “for\_document” → doctype, “reference\_type” → “Custom DocPerm”, “status” → list(“in”, list(statuses))), fields = list(“changes ….
- Set roles from set().
- For each log in logs.
  - Attempt the following.
    - Set changes from (json.loads(log.changes) or mapping()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in json.loads(log.changes) → mapping().
  - On failure (tuple(TypeError, ValueError)).
    - Set changes from mapping().
  - Set logged from set().
  - For each side in tuple(“from”, “to”).
    - Set role from (changes.get(side) or mapping()).get(“role”).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in changes.get(side) → mapping().
    - If role.
      - Evaluate logged.add(role).
  - If not logged.
    - Set role from Platform.db.get\_value(“Custom DocPerm”, log.reference, “role”).
    - If role.
      - Evaluate logged.add(role).
  - Evaluate roles.update(logged).
- Return roles.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0020.json#L128) · [Binding](../../../current-decisions/enterprise/bindings-005.tsv#L688) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-006.tsv#L185)

<a id="op-21dff5f715bc90"></a>
### After app install

`operation_enterprise_setup_install_business_behavior_after_application_install`

**Inputs** app\_name = no value.

**Local steps**

- If app\_name equals “crm”.
  - Bind dependencies remove\_allowed\_users\_on\_crm\_install.
  - Evaluate remove\_allowed\_users\_on\_crm\_install().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L193) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L675) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L248)

<a id="op-68e1c86d7aef5a"></a>
### After app uninstall

`operation_enterprise_setup_install_business_behavior_after_application_uninstall`

**Inputs** app\_name = no value.

**State and service calls** commit.

**Local steps**

- If app\_name equals “crm”.
  - Bind dependencies disable\_Platform\_crm\_data\_synchronization\_on\_crm\_uninstall.
  - Evaluate disable\_Platform\_crm\_data\_synchronization\_on\_crm\_uninstall().
  - Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L273) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L676) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L249)

## Service · Install fixtures

<a id="op-b39054a0ac29b7"></a>
### Read lines

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_read_lines`

**Inputs** filename.

**Declared result** list at str.

**Explicit results** ((nested operand in the contract.parent ÷ “data”) ÷ filename).read\_text().splitlines().

**Local steps**

- Return ((nested operand in the contract.parent ÷ “data”) ÷ filename).read\_text().splitlines().

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0701.json#L5961) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1116) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L657)

<a id="op-f11e609682376c"></a>
### Get preset records

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_get_preset_records`

**Inputs** country = no value.

**Explicit results** records.

**Local steps**

- Set root\_item\_group from (get\_root\_of(“Item Group”) or translated “All Item Groups”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_root\_of(“Item Group”) → translated “All Item Groups”.
- Set records from list(mapping(“doctype” → “Address Template”, “country” → country), mapping(“doctype” → “Item Group”, “item\_group\_name” → root\_item\_group, “is\_group” → 1, “parent\_item\_group” → empty text, …), mapping(“doct ….
  - Value choice on country equals “United States” — true gives “Check”, false gives translated “Cheque”.
- Return records.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L26) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1111) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L652)

<a id="op-b9737ddef0d8f8"></a>
### Install

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_install`

**Inputs** country = no value.

**Local steps**

- Set records from get\_preset\_records(country).
- For each tuple(doctype, title\_field, filename) in tuple(tuple(“Designation”, “designation\_name”, “designation.txt”), tuple(“Sales Stage”, “stage\_name”, “sales\_stage.txt”), tuple(“Industry Type”, “industry”, “industry\_type.txt”), tuple(“UTM Source”, “name” ….
  - Update records using + list of mapping(“doctype” → doctype, title\_field → title) for title drawn from read\_lines(filename).
    - Draw title from read\_lines(filename).
- Set base\_path from Platform.get\_app\_path(“Enterprise”, “stock”, “doctype”).
- Set response from Platform.read\_file(os.path.join(base\_path, “delivery\_trip/dispatch\_notification\_template.html”)).
- Update records using + list(mapping(“doctype” → “Email Template”, “name” → translated “Dispatch Notification”, “response” → response, “subject” → translated “Your order is out for delivery!”, …)).
- Bind dependencies make\_default\_records.
- Evaluate make\_default\_records().
- Evaluate make\_records(records).
- Evaluate set\_up\_address\_templates(default\_country = country).
- Evaluate update\_selling\_defaults().
- Evaluate update\_buying\_defaults().
- Evaluate add\_uom\_data().
- Evaluate update\_item\_variant\_settings().
- Evaluate update\_global\_search\_doctypes().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L6) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1113) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L654)

<a id="op-629cdc6d17e7fa"></a>
### Update selling defaults

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_update_selling_defaults`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Selling Settings” via get\_doc.

**State and service calls** call save on selling\_settings.

**Local steps**

- Set selling\_settings from Platform.get\_doc(“Selling Settings”).
- Set selling\_settings.cust\_master\_name from “Customer Name”.
- Set selling\_settings.so\_required from “No”.
- Set selling\_settings.dn\_required from “No”.
- Set selling\_settings.allow\_multiple\_items from 1.
- Set selling\_settings.sales\_update\_frequency from “Daily”.
- Evaluate selling\_settings.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L27) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1120) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L661)

<a id="op-c37fa94aa67eaa"></a>
### Update buying defaults

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_update_buying_defaults`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Buying Settings” via get\_doc.

**State and service calls** call save on buying\_settings.

**Local steps**

- Set buying\_settings from Platform.get\_doc(“Buying Settings”).
- Set buying\_settings.supp\_master\_name from “Supplier Name”.
- Set buying\_settings.po\_required from “No”.
- Set buying\_settings.pr\_required from “No”.
- Set buying\_settings.maintain\_same\_rate from 1.
- Set buying\_settings.allow\_multiple\_items from 1.
- Evaluate buying\_settings.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L851) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1118) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L659)

<a id="op-f6fa614f99d925"></a>
### Update item variant settings

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_update_item_variant_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Item Variant Settings” via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- Set doc from Platform.get\_doc(“Item Variant Settings”).
- Evaluate doc.set\_default\_fields().
- Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L1011) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1119) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L660)

<a id="op-a9cb9aa88f39c1"></a>
### Add uom data

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_add_unit_of_measure_data`

**Inputs** no declared parameters.

**Record and data access** read “UOM Category” via exists · resolve a document from mapping(“doctype” → “UOM Category”, “category\_name” → d.get(“category”)) via get\_doc · read “UOM” via exists · read “UOM Conversion Factor” via exists · resolve a document from mapping(“doctype” → “UOM Conversion Factor”, “category” → d.get(“category”), “from\_uom” → d.get(“from\_uom”), “to\_uom” → d.get(“to\_uom”), …) via get\_doc.

**State and service calls** call db\_insert on Platform.get\_doc(mapping(“doctype” → “UOM Category”, “category\_name” → d.get(“category”))) · request new\_doc for “UOM” · call insert on doc · call db\_insert on Platform.get\_doc(mapping(“doctype” → “UOM Conversion Factor”, “category” → d.get(“category”), “from\_uom” → d.get(“from\_uom”), “to\_uom” → d.get(“to\_uom”), …)).

**Local steps**

- Set uoms from json.loads(open(Platform.get\_app\_path(“Enterprise”, “setup”, “setup\_wizard”, “data”, …)).read()).
- For each d in uoms.
  - If (d.get(“category”) and not Platform.db.exists(“UOM Category”, d.get(“category”))).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.get(“category”) → not Platform.db.exists(“UOM Category”, d.get(“category”)).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “UOM Category”, “category\_name” → d.get(“category”))).db\_insert().
  - If not Platform.db.exists(“UOM”, d.get(“uom\_name”)).
    - Set doc from Platform.new\_doc(“UOM”).
    - Evaluate doc.update(d).
    - Evaluate doc.insert(ignore\_permissions = true).
- Set uom\_conversions from json.loads(open(Platform.get\_app\_path(“Enterprise”, “setup”, “setup\_wizard”, “data”, …)).read()).
- For each d in uom\_conversions.
  - If not Platform.db.exists(“UOM Conversion Factor”, mapping(“from\_uom” → d.get(“from\_uom”), “to\_uom” → d.get(“to\_uom”))).
    - Evaluate Platform.get\_doc(mapping(“doctype” → “UOM Conversion Factor”, “category” → d.get(“category”), “from\_uom” → d.get(“from\_uom”), “to\_uom” → d.get(“to\_uom”), …)).db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, file state, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L1104) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1108) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L649)

<a id="op-f7125cd9dfc099"></a>
### Add market segments

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_add_market_segments`

**Inputs** no declared parameters.

**Local steps**

- Set records from list(mapping(“doctype” → “Market Segment”, “market\_segment” → translated “Lower Income”), mapping(“doctype” → “Market Segment”, “market\_segment” → translated “Middle Income”), mapping(“doctype” → “Market S ….
- Evaluate make\_records(records).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L1977) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1106) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L647)

<a id="op-e27ecb3a3c5731"></a>
### Get sale stages

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_get_sale_stages`

**Inputs** no declared parameters.

**Explicit results** list(mapping(“doctype” → “Sales Stage”, “stage\_name” → translated “Prospecting”), mapping(“doctype” → “Sales Stage”, “stage\_name” → translated “Qualification”), mapping(“doctype” → “Sales Stage”, “stage\_na ….

**Local steps**

- Return list(mapping(“doctype” → “Sales Stage”, “stage\_name” → translated “Prospecting”), mapping(“doctype” → “Sales Stage”, “stage\_name” → translated “Qualification”), mapping(“doctype” → “Sales Stage”, “stage\_na ….

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L2201) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1112) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L653)

<a id="op-cb9c91e70135e7"></a>
### Add sale stages

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_add_sale_stages`

**Inputs** no declared parameters.

**Record and data access** resolve a document from sales\_stage via get\_doc.

**State and service calls** call db\_insert on Platform.get\_doc(sales\_stage).

**Local steps**

- Set records from get\_sale\_stages().
- For each sales\_stage in records.
  - Evaluate Platform.get\_doc(sales\_stage).db\_insert().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L2673) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1107) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L648)

<a id="op-de9329965d638f"></a>
### Install company

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_install_company`

**Inputs** args.

**Local steps**

- Set records from list(mapping(“doctype” → “Fiscal Year”, “year” → get\_fy\_details(args.fy\_start\_date, args.fy\_end\_date), “year\_start\_date” → args.fy\_start\_date, “year\_end\_date” → args.fy\_end\_date), mapping(“doctype” → “Comp ….
- Evaluate make\_records(records).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L2768) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1114) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L655)

<a id="op-479ae63b5f020a"></a>
### Install defaults

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_install_defaults`

**Inputs** args = no value.

**State and service calls** request set\_value on “Currency” · request set\_single\_value on “Stock Settings”.

**Local steps**

- Set records from list(mapping(“doctype” → “Price List”, “price\_list\_name” → translated “Standard Buying”, “enabled” → 1, “buying” → 1, …), mapping(“doctype” → “Price List”, “price\_list\_name” → translated “Standard Selling” ….
- Evaluate make\_records(records).
- Evaluate Platform.db.set\_value(“Currency”, args.get(“currency”), “enabled”, 1).
- Evaluate Platform.db.set\_single\_value(“Stock Settings”, “email\_footer\_address”, args.get(“company\_name”)).
- Evaluate set\_global\_defaults(args).
- Evaluate update\_stock\_settings().
- Evaluate args.update(mapping(“set\_default” → 1)).
- Evaluate create\_bank\_account(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L3120) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1115) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L656)

<a id="op-de4b9a6f7fe7a3"></a>
### Set global defaults

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_set_global_defaults`

**Inputs** kwargs.

**Record and data access** resolve a document from “Global Defaults” via get\_doc · read “Company” via get\_value.

**State and service calls** call save on global\_defaults.

**Local steps**

- Set global\_defaults from Platform.get\_doc(“Global Defaults”, “Global Defaults”).
- Set company from Platform.db.get\_value(“Company”, mapping(“company\_name” → kwargs.get(“company\_name”)), “name”).
- Evaluate global\_defaults.update(mapping(“default\_currency” → kwargs.get(“currency”), “default\_company” → company, “country” → kwargs.get(“country”))).
- Evaluate global\_defaults.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L3665) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1117) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L658)

<a id="op-626a85d9539f65"></a>
### Update stock settings

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_update_stock_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Stock Settings” via get\_doc.

**State and service calls** call save on stock\_settings.

**Local steps**

- Set stock\_settings from Platform.get\_doc(“Stock Settings”).
- Set stock\_settings.item\_naming\_by from “Item Code”.
- Set stock\_settings.valuation\_method from “FIFO”.
- Set stock\_settings.stock\_uom from “Nos”.
- Set stock\_settings.auto\_indent from 1.
- Set stock\_settings.auto\_insert\_price\_list\_rate\_if\_missing from 1.
- Set stock\_settings.update\_price\_list\_based\_on from “Rate”.
- Set stock\_settings.flags.ignore\_permissions from true.
- Evaluate stock\_settings.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L28) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1121) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L662)

<a id="op-2ed061c0c3925b"></a>
### Create bank account

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_create_bank_account`

**Inputs** args.

**Record and data access** read “Account” via get\_value · resolve a document from mapping(“doctype” → “Account”, “account\_name” → args.get(“bank\_account”), “parent\_account” → bank\_account\_group, “is\_group” → 0, …) via get\_doc.

**State and service calls** call insert on bank\_account · request set\_value on “Company”.

**Explicit results** no value · doc.

**Explicit failure paths** validation helper — Platform.\_(“Bank account cannot be named as {0}”).format(args.get(“bank\_account”)).

**Local steps**

- If not args.get(“bank\_account”).
  - Return no value.
- Set company\_name from args.get(“company\_name”).
- Set bank\_account\_group from Platform.db.get\_value(“Account”, mapping(“account\_type” → “Bank”, “is\_group” → 1, “root\_type” → “Asset”, “company” → company\_name)).
- If bank\_account\_group.
  - Set bank\_account from Platform.get\_doc(mapping(“doctype” → “Account”, “account\_name” → args.get(“bank\_account”), “parent\_account” → bank\_account\_group, “is\_group” → 0, …)).
  - Attempt the following.
    - Set doc from bank\_account.insert().
    - If args.get(“set\_default”).
      - Evaluate Platform.db.set\_value(“Company”, args.get(“company\_name”), “default\_bank\_account”, bank\_account.name, update\_modified = false).
    - Return doc.
  - On failure (RootNotEditable).
    - Call the validation error handler Platform.throw(Platform.\_(“Bank account cannot be named as {0}”).format(args.get(“bank\_account”))).
  - On failure (Platform.DuplicateEntryError).
    - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/enterprise/procedures-0036.json#L25) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1109) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L650)

<a id="op-84967964528e89"></a>
### Get fy details

`operation_enterprise_setup_setup_wizard_operations_install_fixtures_business_behavior_get_financial_year_details`

**Inputs** fy\_start\_date, fy\_end\_date.

**Explicit results** fy.

**Local steps**

- Set start\_year from getdate(fy\_start\_date).year.
- If start\_year equals getdate(fy\_end\_date).year.
  - Set fy from cstr(start\_year).
- Otherwise.
  - Set fy from ((cstr(start\_year) + “-”) + cstr((start\_year + 1))).
- Return fy.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../enterprise-decision-contracts/part-0703.json#L4942) · [Binding](../../../current-decisions/enterprise/bindings-009.tsv#L1110) · [Declaration location](../../../current-decisions/enterprise/evidence/locations-010.tsv#L651)
