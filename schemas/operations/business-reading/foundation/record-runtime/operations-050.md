# Record lifecycle and persistence · operations 50

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Record · Document naming settings

[Record definition](../../../../data/record-types/document_naming_settings.json)

<a id="op-49216643529ee2"></a>
### Document Naming Settings.fetch last doc if available

`operation_foundation_core_record_definitions_document_naming_settings_business_behavior_document_naming_settings_fetch_last_record_if_available`

**Inputs** self.

**Record and data access** read self.transaction\_type via get\_last\_doc.

**Explicit results** Platform.get\_last\_doc(self.transaction\_type) · no value.

**Local steps**

- Attempt the following.
  - Return Platform.get\_last\_doc(self.transaction\_type).
- On failure (Exception).
  - Return no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0074.json#L5470) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1392)

## Record · Document share key

[Record definition](../../../../data/record-types/document_share_key.json)

<a id="op-96973317ccb827"></a>
### Document Share Key.before insert

`operation_foundation_core_record_definitions_document_share_key_business_behavior_document_share_key_before_insert`

**Inputs** self.

**Local steps**

- Set self.key from Platform.generate\_hash(length = randrange(25, 35)).
- If (not self.expires\_on and not self.flags.no\_expiry).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not self.expires\_on → not self.flags.no\_expiry.
  - Set self.expires\_on from Platform.utils.add\_days(no value, days = (Platform.get\_system\_settings(“document\_share\_key\_expiry”) or 90)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“document\_share\_key\_expiry”) → 90.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = randrange(25, 35)) · configured or stored value from Platform.get\_system\_settings(“document\_share\_key\_expiry”).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1417)

<a id="op-7930508aa9f4d7"></a>
### Is expired

`operation_foundation_core_record_definitions_document_share_key_business_behavior_is_expired`

**Inputs** expires\_on.

**Explicit results** (expires\_on and expires\_on &lt; Platform.utils.getdate()).

**Local steps**

- Return (expires\_on and expires\_on &lt; Platform.utils.getdate()).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in expires\_on → expires\_on &lt; Platform.utils.getdate().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L215) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1428) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1418)

## Record · Domain

[Record definition](../../../../data/record-types/domain.json)

<a id="op-1ce7a51190cd8e"></a>
### Domain.setup domain

`operation_foundation_core_record_definitions_domain_business_behavior_domain_setup_domain`

**Inputs** self.

**Local steps**

- Evaluate self.setup\_data().
- Evaluate self.setup\_roles().
- Evaluate self.setup\_properties().
- Evaluate self.set\_values().
- If not cint(Platform.defaults.get\_defaults().setup\_complete).
  - Evaluate self.setup\_sidebar\_items().
  - Evaluate self.set\_default\_portal\_role().
- If self.data.custom\_fields.
  - Evaluate create\_custom\_fields(self.data.custom\_fields).
- If self.data.on\_setup.
  - Evaluate Platform.get\_attr(self.data.on\_setup)().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup data](operations-050.md#op-cb1f9b210327a1), [setup roles](operations-050.md#op-8c79d1420144f6), [setup properties](operations-050.md#op-6cf59bd9811716), [set values](operations-050.md#op-bdb167bf7dd4a6), [setup sidebar items](operations-050.md#op-a4c64396ba930b), [set default portal role](operations-050.md#op-9ebe69f5c2b347).

**Values supplied outside this operation** selected callable from Platform.get\_attr(self.data.on\_setup).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L292) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1425)

<a id="op-2704282cf68b39"></a>
### Domain.remove domain

`operation_foundation_core_record_definitions_domain_business_behavior_domain_remove_domain`

**Inputs** self.

**Record and data access** read “Role” via exists · resolve a document from “Role” via get\_doc.

**State and service calls** call save on role.

**Local steps**

- Evaluate self.setup\_data().
- If self.data.restricted\_roles.
  - For each role\_name in self.data.restricted\_roles.
    - If Platform.db.exists(“Role”, role\_name).
      - Set role from Platform.get\_doc(“Role”, role\_name).
      - Set role.disabled from 1.
      - Evaluate role.save().
- Evaluate self.remove\_custom\_field().

If control reaches the end, it returns no value.

**Methods declared on this owner** [setup data](operations-050.md#op-cb1f9b210327a1), [remove custom field](operations-050.md#op-0b56a5d3f8087e).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L596) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1431) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1421)

<a id="op-0b56a5d3f8087e"></a>
### Domain.remove custom field

`operation_foundation_core_record_definitions_domain_business_behavior_domain_remove_custom_field`

**Inputs** self.

**Record and data access** read “Custom Field” via get\_value.

**State and service calls** request delete\_doc for “Custom Field”.

**Local steps**

- If self.data.custom\_fields.
  - For each doctype in self.data.custom\_fields.
    - Set custom\_fields from self.data.custom\_fields at doctype.
    - If isinstance(custom\_fields, dict).
      - Set custom\_fields from list(custom\_fields).
    - For each custom\_field\_detail in custom\_fields.
      - Set custom\_field\_name from Platform.db.get\_value(“Custom Field”, dict(dt = doctype, fieldname = custom\_field\_detail.get(“fieldname”))).
      - If custom\_field\_name.
        - Evaluate Platform.delete\_doc(“Custom Field”, custom\_field\_name).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L821) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1430) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1420)

<a id="op-8c79d1420144f6"></a>
### Domain.setup roles

`operation_foundation_core_record_definitions_domain_business_behavior_domain_setup_roles`

**Inputs** self.

**Record and data access** resolve a document from “User” via get\_doc · read “Role” via get\_value · resolve a document from “Role” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “Role”, role\_name = role\_name) · call save on role · call save on user.

**Local steps**

- If self.data.restricted\_roles.
  - Set user from Platform.get\_doc(“User”, Platform.session.user).
  - For each role\_name in self.data.restricted\_roles.
    - Evaluate user.append(“roles”, mapping(“role” → role\_name)).
    - If not Platform.db.get\_value(“Role”, role\_name).
      - Evaluate Platform.get\_doc(doctype = “Role”, role\_name = role\_name).insert().
      - Continue with the next iteration or loop test.
    - Set role from Platform.get\_doc(“Role”, role\_name).
    - Set role.disabled from 0.
    - Evaluate role.save().
  - Evaluate user.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L1114) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1427)

<a id="op-cb1f9b210327a1"></a>
### Domain.setup data

`operation_foundation_core_record_definitions_domain_business_behavior_domain_setup_data`

**Inputs** self, domain = no value.

**Local steps**

- Set self.data from Platform.get\_domain\_data(self.name).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L1469) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1424)

<a id="op-fc4923da4c842c"></a>
### Domain.get domain data

`operation_foundation_core_record_definitions_domain_business_behavior_domain_get_domain_data`

**Inputs** self, module.

**Explicit results** Platform.get\_attr((Platform.get\_hooks(“domains”) at self.name + “.data”)).

**Local steps**

- Return Platform.get\_attr((Platform.get\_hooks(“domains”) at self.name + “.data”)).

**Values supplied outside this operation** selected callable from Platform.get\_attr((Platform.get\_hooks(“domains”) at self.name + “.data”)), Platform.get\_hooks(“domains”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L1551) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1419)

<a id="op-9ebe69f5c2b347"></a>
### Domain.set default portal role

`operation_foundation_core_record_definitions_domain_business_behavior_domain_set_default_portal_role`

**Inputs** self.

**State and service calls** request set\_single\_value on “Portal Settings”.

**Local steps**

- If self.data.get(“default\_portal\_role”).
  - Evaluate Platform.db.set\_single\_value(“Portal Settings”, “default\_role”, self.data.get(“default\_portal\_role”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L1652) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1432) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1422)

<a id="op-6cf59bd9811716"></a>
### Domain.setup properties

`operation_foundation_core_record_definitions_domain_business_behavior_domain_setup_properties`

**Inputs** self.

**Local steps**

- If self.data.properties.
  - For each args in self.data.properties.
    - Evaluate Platform.make\_property\_setter(args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L1777) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1436) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1426)

<a id="op-bdb167bf7dd4a6"></a>
### Domain.set values

`operation_foundation_core_record_definitions_domain_business_behavior_domain_set_values`

**Inputs** self.

**Record and data access** resolve a document from args at 0 via get\_doc.

**State and service calls** call save on doc.

**Local steps**

- If self.data.set\_value.
  - For each args in self.data.set\_value.
    - Evaluate Platform.reload\_doctype(args at 0).
    - Set doc from Platform.get\_doc(args at 0, (args at 1 or args at 0)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in args at 1 → args at 0.
    - Evaluate doc.set(args at 2, args at 3).
    - Evaluate doc.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L1874) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1423)

<a id="op-a4c64396ba930b"></a>
### Domain.setup sidebar items

`operation_foundation_core_record_definitions_domain_business_behavior_domain_setup_sidebar_items`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Local steps**

- If self.data.allow\_sidebar\_items.
  - Evaluate Platform.db.sql(“update ′tabPortal Menu Item′ set enabled=0”).
  - Evaluate Platform.db.sql(“update ′tabPortal Menu Item′ set enabled=1\\n\\t\\t\\t\\twhere route in ({})”.format(“, ”.join(generator of formatted text "{d}" for d drawn from self.data.allow\_sidebar\_items))).
    - Draw d from self.data.allow\_sidebar\_items.
- If self.data.remove\_sidebar\_items.
  - Evaluate Platform.db.sql(“update ′tabPortal Menu Item′ set enabled=1”).
  - Evaluate Platform.db.sql(“update ′tabPortal Menu Item′ set enabled=0\\n\\t\\t\\t\\twhere route in ({})”.format(“, ”.join(generator of formatted text "{d}" for d drawn from self.data.remove\_sidebar\_items))).
    - Draw d from self.data.remove\_sidebar\_items.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L2102) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1428)

## Record · Domain settings

[Record definition](../../../../data/record-types/domain_settings.json)

<a id="op-a22b589854ad35"></a>
### Domain Settings.set active domains

`operation_foundation_core_record_definitions_domain_settings_business_behavior_domain_settings_set_active_domains`

**Inputs** self, domains.

**State and service calls** call save on self.

**Local steps**

- Set active\_domains from list of d.domain for d drawn from self.active\_domains.
  - Draw d from self.active\_domains.
- Set added from false.
- For each d in domains.
  - If d does not belong to active\_domains.
    - Evaluate self.append(“active\_domains”, dict(domain = d)).
    - Set added from true.
- If added.
  - Evaluate self.save().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L2570) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1442) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1432)

<a id="op-5252522598fad1"></a>
### Domain Settings.on update

`operation_foundation_core_record_definitions_domain_settings_business_behavior_domain_settings_on_update`

**Inputs** self.

**Record and data access** resolve a document from “Domain” via get\_doc.

**Local steps**

- For each tuple(i, d) in enumerate(self.active\_domains).
  - If i ≥ 1.
    - Set Platform.flags.keep\_desktop\_icons from true.
  - Set domain from Platform.get\_doc(“Domain”, d.domain).
  - Evaluate domain.setup\_domain().
- Evaluate self.restrict\_roles\_and\_modules().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Methods declared on this owner** [restrict roles and modules](operations-050.md#op-4683f04afbd568).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L2787) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1429)

<a id="op-4683f04afbd568"></a>
### Domain Settings.restrict roles and modules

`operation_foundation_core_record_definitions_domain_settings_business_behavior_domain_settings_restrict_roles_and_modules`

**Inputs** self.

**Record and data access** read “Domain” via get\_value · resolve a document from “Domain” via get\_doc · read “Role” via get\_value · resolve a document from “Role” via get\_doc.

**State and service calls** call insert on Platform.get\_doc(doctype = “Domain”, domain = domain) · request set\_value on “Module Def” · call insert on Platform.get\_doc(doctype = “Role”, role\_name = role) · request set\_value on “Role”.

**Local steps**

- Set active\_domains from Platform.get\_active\_domains().
- Set all\_domains from list((Platform.get\_hooks(“domains”) or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_hooks(“domains”) → mapping().
- Bind local operation remove\_role for subsequent calls.
- For each domain in all\_domains.
  - Set data from Platform.get\_domain\_data(domain).
  - If not Platform.db.get\_value(“Domain”, domain).
    - Evaluate Platform.get\_doc(doctype = “Domain”, domain = domain).insert().
  - If “modules” belongs to data.
    - For each module in data.get(“modules”).
      - Evaluate Platform.db.set\_value(“Module Def”, module, “restrict\_to\_domain”, domain).
  - If “restricted\_roles” belongs to data.
    - For each role in data at “restricted\_roles”.
      - If not Platform.db.get\_value(“Role”, role).
        - Evaluate Platform.get\_doc(doctype = “Role”, role\_name = role).insert().
      - Evaluate Platform.db.set\_value(“Role”, role, “restrict\_to\_domain”, domain).
      - If domain does not belong to active\_domains.
        - Evaluate remove\_role(role).
  - If “custom\_fields” belongs to data.
    - If domain does not belong to active\_domains.
      - Set inactive\_domain from Platform.get\_doc(“Domain”, domain).
      - Evaluate inactive\_domain.setup\_data().
      - Evaluate inactive\_domain.remove\_custom\_field().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“domains”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L3000) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1440) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1430)

<a id="op-3ac1f71ad9f603"></a>
### Domain Settings.restrict roles and modules.remove role

`operation_foundation_core_record_definitions_domain_settings_business_behavior_domain_settings_restrict_roles_and_modules_remove_role`

**Inputs** role.

**State and service calls** request delete on “Has Role”.

**Local steps**

- Evaluate Platform.db.delete(“Has Role”, mapping(“role” → role)).
- Evaluate Platform.set\_value(“Role”, role, “disabled”, 1).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L3817) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1431)

<a id="op-661f489962734c"></a>
### Get active domains

`operation_foundation_core_record_definitions_domain_settings_business_behavior_get_active_domains`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.get\_value(“active\_domains”, \_get\_active\_domains).

**Local steps**

- Bind local operation \_get\_active\_domains for subsequent calls.
- Return Platform.cache.get\_value(“active\_domains”, \_get\_active\_domains).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L3949) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1433)

<a id="op-8b8a3be064dde4"></a>
### Get active domains.get active domains

`operation_foundation_core_record_definitions_domain_settings_business_behavior_get_active_domains_get_active_domains`

**Inputs** no declared parameters.

**Record and data access** read “Has Domain” via get\_all.

**Explicit results** active\_domains.

**Local steps**

- Set domains from Platform.get\_all(“Has Domain”, filters = mapping(“parent” → “Domain Settings”), fields = list(“domain”), distinct = true).
- Set active\_domains from list of row.get(“domain”) for row drawn from domains.
  - Draw row from domains.
- Evaluate active\_domains.append(empty text).
- Return active\_domains.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L4196) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1444) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1434)

<a id="op-00f530dec0da61"></a>
### Get active modules

`operation_foundation_core_record_definitions_domain_settings_business_behavior_get_active_modules`

**Inputs** no declared parameters.

**Explicit results** Platform.cache.get\_value(“active\_modules”, \_get\_active\_modules).

**Local steps**

- Bind local operation \_get\_active\_modules for subsequent calls.
- Return Platform.cache.get\_value(“active\_modules”, \_get\_active\_modules).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L4398) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1435)

<a id="op-ab420599fa7be4"></a>
### Get active modules.get active modules

`operation_foundation_core_record_definitions_domain_settings_business_behavior_get_active_modules_get_active_modules`

**Inputs** no declared parameters.

**Record and data access** read “Module Def” via get\_all.

**Explicit results** active\_modules.

**Local steps**

- Set active\_modules from list().
- Set active\_domains from get\_active\_domains().
- For each m in Platform.get\_all(“Module Def”, fields = list(“name”, “restrict\_to\_domain”)).
  - If (not m.restrict\_to\_domain or m.restrict\_to\_domain belongs to active\_domains).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not m.restrict\_to\_domain → m.restrict\_to\_domain belongs to active\_domains.
    - Evaluate active\_modules.append(m.name).
- Return active\_modules.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L4644) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1446) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1436)

## Record · Duckdb sync

<a id="op-650642c85738f8"></a>
### Duck DBSync.before save

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_before_save`

**Inputs** self.

**Local steps**

- Set dt from self.doc\_type.lower().replace(one space, “\_”).
- Set self.filename from formatted text {dt}\_{self.name}.duckdb.
- Set self.db\_tables from list().
- Evaluate self.append(“db\_tables”, mapping(“table” → self.doc\_type)).
- Set df from qb.DocType(“DocField”).
- If res bound to nested operand in the contract.select(nested operand in the contract.options).where((nested operand in the contract.eq(nested operand in the contract.doc\_type) bitwise and nested operand in the contract.eq ….run().
  - For each tb in res.
    - Evaluate self.append(“db\_tables”, mapping(“table” → tb at 0)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L4850) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1447) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1437)

<a id="op-8365fe65fd6ed9"></a>
### Duck DBSync.on submit

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_on_submit`

**Inputs** self.

**Local steps**

- Evaluate self.sync\_schema().
- Evaluate start\_data\_sync(self.name).

If control reaches the end, it returns no value.

**Methods declared on this owner** [sync schema](operations-051.md#op-14a4bccf5352c1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L5293) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1451) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1441)

<a id="op-b5f13e20752182"></a>
### Duck DBSync.get duckdb conn

`operation_foundation_core_record_definitions_duckdb_sync_business_behavior_duck_database_sync_get_duckdb_conn`

**Inputs** self.

**Explicit results** get\_duckdb(false, self.filename).

**Local steps**

- Return get\_duckdb(false, self.filename).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0075.json#L5371) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L1449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L1439)
