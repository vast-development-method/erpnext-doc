# Forms, reports and navigation · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Boot

<a id="op-98bc8b20fd76f3"></a>
### Add timezone info

`operation_foundation_boot_business_behavior_add_timezone_info`

**Inputs** bootinfo.

**Local steps**

- Set system from bootinfo.sysdefaults.get(“time\_zone”).
- Bind dependencies Platform.utils.momentjs.
- Set bootinfo.timezone\_info from mapping(“zones” → mapping(), “rules” → mapping(), “links” → mapping()).
- Evaluate Platform.utils.momentjs.update(system, bootinfo.timezone\_info).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L2901) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L400) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L488)

<a id="op-f9ffdd58b97412"></a>
### Load print

`operation_foundation_boot_business_behavior_load_print`

**Inputs** bootinfo, doclist.

**Local steps**

- Set print\_settings from Platform.db.get\_singles\_dict(“Print Settings”).
- Set print\_settings.doctype from “:Print Settings”.
- Evaluate doclist.append(print\_settings).
- Evaluate load\_print\_css(bootinfo, print\_settings).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L3080) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L426) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L513)

<a id="op-7272ca5ad9f4a9"></a>
### Load print css

`operation_foundation_boot_business_behavior_load_print_style_sheet`

**Inputs** bootinfo, print\_settings.

**Local steps**

- Bind dependencies Platform.www.printview.
- Set bootinfo.print\_css from Platform.www.printview.get\_print\_style((print\_settings.print\_style or “Redesign”), for\_legacy = true).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in print\_settings.print\_style → “Redesign”.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L3222) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L427) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L514)

<a id="op-7b76438331ef4e"></a>
### Get success action

`operation_foundation_boot_business_behavior_get_success_action`

**Inputs** no declared parameters.

**Record and data access** read “Success Action” via get\_all.

**Explicit results** Platform.get\_all(“Success Action”, fields = list(“\*”)).

**Local steps**

- Return Platform.get\_all(“Success Action”, fields = list(“\*”)).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L3335) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L418) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L505)

<a id="op-526aa50a116d2e"></a>
### Get link preview doctypes

`operation_foundation_boot_business_behavior_get_link_preview_record_types`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all · read “Property Setter” via get\_all.

**Explicit results** link\_preview\_doctypes.

**Local steps**

- Bind dependencies cint.
- Set link\_preview\_doctypes from Platform.get\_all(“DocType”, mapping(“show\_preview\_popup” → 1), pluck = “name”).
- Set customizations from Platform.get\_all(“Property Setter”, fields = list(“doc\_type”, “value”), filters = mapping(“property” → “show\_preview\_popup”)).
- For each custom in customizations.
  - If (not cint(custom.value) and custom.doc\_type belongs to link\_preview\_doctypes).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not cint(custom.value) → custom.doc\_type belongs to link\_preview\_doctypes.
    - Evaluate link\_preview\_doctypes.remove(custom.doc\_type).
  - Otherwise.
    - Evaluate link\_preview\_doctypes.append(custom.doc\_type).
- Return link\_preview\_doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L97) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L412) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L500)

<a id="op-ac4d888a2db893"></a>
### Get additional filters from hooks

`operation_foundation_boot_business_behavior_get_additional_filters_from_hooks`

**Inputs** no declared parameters.

**Explicit results** filter\_config.

**Local steps**

- Set filter\_config from Platform.\_dict().
- Set filter\_hooks from Platform.get\_hooks(“filters\_config”).
- For each hook in filter\_hooks.
  - Evaluate filter\_config.update(Platform.get\_attr(hook)()).
- Return filter\_config.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“filters\_config”), Platform.get\_attr(hook).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L3745) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L402) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L490)

<a id="op-2091414ee13e6a"></a>
### Add layouts

`operation_foundation_boot_business_behavior_add_layouts`

**Inputs** bootinfo.

**Record and data access** read “DocType Layout” via get\_all.

**Local steps**

- Set bootinfo.doctype\_layouts from Platform.get\_all(“DocType Layout”, list(“name”, “route”, “document\_type”)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L92) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L398) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L486)

<a id="op-6f662e9e8459cf"></a>
### Get desk settings

`operation_foundation_boot_business_behavior_get_desk_settings`

**Inputs** no declared parameters.

**Record and data access** read “User” via get\_value.

**Explicit results** Platform.get\_value(“User”, Platform.session.user, desk\_properties, as\_dict = true).

**Local steps**

- Bind dependencies desk\_properties.
- Return Platform.get\_value(“User”, Platform.session.user, desk\_properties, as\_dict = true).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L4046) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L408) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L496)

<a id="op-4102e170cc7fbe"></a>
### Get notification settings

`operation_foundation_boot_business_behavior_get_notification_settings`

**Inputs** no declared parameters.

**Record and data access** resolve a document from “Notification Settings” via get\_cached\_doc.

**Explicit results** Platform.get\_cached\_doc(“Notification Settings”, Platform.session.user).

**Explicit failure paths** propagate active failure.

**Local steps**

- Bind dependencies create\_notification\_settings.
- Attempt the following.
  - Return Platform.get\_cached\_doc(“Notification Settings”, Platform.session.user).
- On failure (Platform.DoesNotExistError).
  - If Platform.flags.read\_only.
    - Propagate the active failure.
  - Evaluate Platform.clear\_last\_message().
  - Evaluate create\_notification\_settings(Platform.session.user).
  - Set Platform.local.flags.commit from true.
  - Return Platform.get\_cached\_doc(“Notification Settings”, Platform.session.user).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Notification Settings”, Platform.session.user).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L4133) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L415) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L503)

<a id="op-318709956c4c0e"></a>
### Get link title doctypes

`operation_foundation_boot_business_behavior_get_link_title_record_types`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all · read “Property Setter” via get\_all.

**Explicit results** list of d.name for d drawn from (dts + custom\_dts) where d.

**Local steps**

- Set dts from Platform.get\_all(“DocType”, mapping(“show\_title\_field\_in\_link” → 1)).
- Set custom\_dts from Platform.get\_all(“Property Setter”, mapping(“property” → “show\_title\_field\_in\_link”, “value” → “1”), list(“doc\_type as name”)).
- Return list of d.name for d drawn from (dts + custom\_dts) where d.
  - Draw d from (dts + custom\_dts), keep a combination only if (d).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L98) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L413) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L501)

<a id="op-941037cad581a2"></a>
### Get link settings

`operation_foundation_binding_foundation_boot_get_link_settings`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, dict).

**Record and data access** read “DocType” via get\_all · read “Property Setter” via get\_all.

**Explicit results** settings.

**Local steps**

- Bind dependencies get\_image\_field.
- Set flags from mapping().
- For each d in Platform.get\_all(“DocType”, or\_filters = mapping(“link\_display\_mode” → “Select”, “show\_image\_in\_link” → 1), fields = list(“name”, “link\_display\_mode”, “show\_image\_in\_link”)).
  - Set flags at d.name from mapping(“select” → d.link\_display\_mode equals “Select”, “image” → bool(cint(d.show\_image\_in\_link))).
- For each ps in Platform.get\_all(“Property Setter”, filters = mapping(“doctype\_or\_field” → “DocType”, “property” → list(“in”, list(“link\_display\_mode”, “show\_image\_in\_link”))), fields = list(“doc\_type”, “property”, “value”)).
  - Set entry from flags.setdefault(ps.doc\_type, mapping(“select” → false, “image” → false)).
  - If ps.property equals “link\_display\_mode”.
    - Set entry at “select” from ps.value equals “Select”.
  - Otherwise.
    - Set entry at “image” from bool(cint(ps.value)).
- Set names from list of dt for tuple(dt, f) drawn from flags.items() where (f at “select” or f at “image”).
  - Draw tuple(dt, f) from flags.items(), keep a combination only if ((f at “select” or f at “image”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in f at “select” → f at “image”.
- Set existing from set(Platform.get\_all(“DocType”, filters = mapping(“name” → list(“in”, names)), pluck = “name”)).
- Set settings from mapping().
- For each dt in names.
  - If dt does not belong to existing.
    - Continue with the next iteration or loop test.
  - Set entry from mapping().
  - If flags at dt at “select”.
    - Set entry at “display\_mode” from “Select”.
  - If (flags at dt at “image” and image\_field bound to get\_image\_field(dt)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in flags at dt at “image” → image\_field bound to get\_image\_field(dt).
    - Set entry at “image\_field” from image\_field.
  - If entry.
    - Set settings at dt from entry.
- Return settings.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L101) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L583) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L559)

<a id="op-b658152c513395"></a>
### Set time zone

`operation_foundation_boot_business_behavior_set_time_zone`

**Inputs** bootinfo.

**Local steps**

- Set bootinfo.time\_zone from mapping(“system” → get\_system\_timezone(), “user” → (nested operand in the contract(nested operand in the contract, nested operand in the contract).get(nested operand in the contract.session.user, mapping() ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in bootinfo.get(“user\_info”, mapping()).get(Platform.session.user, mapping()).get(“time\_zone”, no value) → get\_system\_timezone().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L4589) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L429) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L516)

<a id="op-af91d8b2f3ec25"></a>
### Load country doc

`operation_foundation_boot_business_behavior_load_country_record`

**Inputs** bootinfo.

**Record and data access** resolve a document from “Country” via get\_cached\_doc.

**Explicit results** no value.

**Local steps**

- Set country from Platform.db.get\_default(“country”).
- If not country.
  - Return no value.
- Attempt the following.
  - Evaluate bootinfo.docs.append(Platform.get\_cached\_doc(“Country”, country)).
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_doc(“Country”, country).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L4764) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L423) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L510)

<a id="op-2cb1f9a5ac8592"></a>
### Load currency docs

`operation_foundation_boot_business_behavior_load_currency_records`

**Inputs** bootinfo.

**Local steps**

- Set currency from Platform.qb.DocType(“Currency”).
- Set currency\_docs from nested operand in the contract(nested operand in the contract).select(currency.name, currency.fraction, currency.fraction\_units, currency.number\_format, …).where(currency.enabled equals 1).run(as\_dict = 1, ….
- Update bootinfo.docs using + currency\_docs.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L4928) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L424) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L511)

<a id="op-d1f426af65b9c0"></a>
### Get tree view doctypes

`operation_foundation_boot_business_behavior_get_tree_view_record_types`

**Inputs** no declared parameters.

**Wrappers, in declaration order** redis\_cache.

**Record and data access** read “DocType” via get\_all.

**Explicit results** Platform.get\_all(“DocType”, mapping(“default\_view” → “Tree”), pluck = “name”).

**Local steps**

- Return Platform.get\_all(“DocType”, mapping(“default\_view” → “Tree”), pluck = “name”).

**Boundaries to resolve** stored data, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L99) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L419) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L506)

<a id="op-3a8015e3c2ff5a"></a>
### Add subscription conf

`operation_foundation_boot_business_behavior_add_subscription_configuration`

**Inputs** no declared parameters.

**Explicit results** Platform.conf.subscription · empty text.

**Local steps**

- Attempt the following.
  - Return Platform.conf.subscription.
- On failure (Exception).
  - Return empty text.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L5302) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L399) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L487)

<a id="op-816c00011bc2e7"></a>
### Get sentry dsn

`operation_foundation_boot_business_behavior_get_sentry_dsn`

**Inputs** no declared parameters.

**Explicit results** no value · os.getenv(“Platform\_SENTRY\_DSN”).

**Local steps**

- If not Platform.get\_system\_settings(“enable\_telemetry”).
  - Return no value.
- Return os.getenv(“Platform\_SENTRY\_DSN”).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_telemetry”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L5366) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L416) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L504)

<a id="op-18193edcdd0d87"></a>
### Get module sidebars

`operation_foundation_boot_business_behavior_get_module_sidebars`

**Inputs** no declared parameters.

**Explicit results** mapping() · payload.

**Local steps**

- Bind dependencies SidebarContext, get\_navigable\_modules, resolve\_sidebar.
- Set modules from get\_navigable\_modules().
- If not modules.
  - Return mapping().
- Set user from Platform.session.user.
- Set context from SidebarContext.for\_modules(modules, user).
- Set payload from mapping().
- For each shell in context.bases.
  - Set resolved from resolve\_sidebar(shell, user, context).
  - If resolved.
    - Set payload at shell from resolved.as\_boot\_entry().
- Return payload.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L5453) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L414) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L502)

<a id="op-f45fec0dec72a6"></a>
### Build entity module map

`operation_foundation_boot_business_behavior_build_entity_module_map`

**Inputs** module\_sidebars.

**Explicit results** mapping of entity → min(entity\_claims, key = deferred anonymous expression) at 1 for tuple(entity, entity\_claims) drawn from claims.items().

**Local steps**

- Set install\_index from mapping of app → index for tuple(index, app) drawn from enumerate(Platform.get\_installed\_apps()).
  - Draw tuple(index, app) from enumerate(Platform.get\_installed\_apps()).
- Set claims from mapping().
- For each tuple(shell, sidebar) in module\_sidebars.items().
  - Set claim from tuple(install\_index.get(sidebar.get(“app”), negative 1), shell).
  - For each item in sidebar at “items”.
    - If (item.get(“link\_to”) and item.get(“is\_default\_module”)).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in item.get(“link\_to”) → item.get(“is\_default\_module”).
      - Evaluate claims.setdefault(item at “link\_to”, list()).append(claim).
- Return mapping of entity → min(entity\_claims, key = deferred anonymous expression) at 1 for tuple(entity, entity\_claims) drawn from claims.items().
  - Draw tuple(entity, entity\_claims) from claims.items().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0017.json#L5702) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L401) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L489)

<a id="op-d01568ebf4d206"></a>
### Get desktop icon urls

`operation_foundation_boot_business_behavior_get_desktop_icon_resource_addresses`

**Inputs** no declared parameters.

**Explicit results** icons\_map.

**Local steps**

- Set icons\_map from mapping().
- For each app in Platform.get\_installed\_apps().
  - Set app\_path from Platform.get\_app\_path(app).
  - Set icons\_dir from os.path.join(app\_path, “public”, “icons”, “desktop\_icons”).
  - If not os.path.exists(icons\_dir).
    - Continue with the next iteration or loop test.
  - Set icons\_map at app from mapping(“subtle” → list(), “solid” → list()).
  - For each variant in list(“subtle”, “solid”).
    - Set variant\_path from os.path.join(icons\_dir, variant).
    - If os.path.exists(variant\_path).
      - For each fname in os.listdir(variant\_path).
        - If fname.endswith(“.svg”).
          - Set abs\_path from os.path.join(variant\_path, fname).
          - Set assets\_path from abs\_path.replace(os.path.join(app\_path, “public”), os.path.join(“assets”, app)).
          - Evaluate icons\_map at app at variant.append(assets\_path).
- Return icons\_map.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L96) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L409) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L497)

## Service · Build

<a id="op-616a3b331be123"></a>
### Can build bundle

`operation_foundation_binding_foundation_studio_build_can_build_bundle`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool(shutil.which(“yarn”)).

**Local steps**

- Return bool(shutil.which(“yarn”)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L3) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1921) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1897)

<a id="op-5a2e6748d3456c"></a>
### Studio App Build Error.initialize

`operation_foundation_binding_foundation_studio_build_studioappbuilderror_init`

**Inputs** self, message, output.

**Local steps**

- Evaluate super().\_\_init\_\_(message).
- Set self.output from output.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L28) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1922)

<a id="op-2abd1cd3e02335"></a>
### Studio App Builder.initialize

`operation_foundation_binding_foundation_studio_build_studioappbuilder_init`

**Inputs** self, studio\_app, is\_standard, Platform\_app = no value.

**Local steps**

- Set self.app\_name from studio\_app.
- Set self.is\_standard from is\_standard.
- Set self.Platform\_app from Platform\_app.
- Set self.components from set().
- Set self.studio\_component\_blocks from mapping().
- Set self.custom\_vue\_components from mapping().
- Set self.missing\_components from set().
- Set self.page\_scripts from list().
- Set self.component\_scripts from mapping().
- Set self.router\_file from no value.
- Set self.app\_folder from no value.
- Set self.icons from set().
- Set self.tailwind\_content from list().
- Set self.page\_sources from list().
- If self.is\_standard.
  - Set self.out\_dir from Platform.get\_app\_path(self.Platform\_app, “public”, “app\_builds”, self.app\_name).
  - Set self.base from formatted text /assets/{self.Platform\_app}/app\_builds/{self.app\_name}/.
- Otherwise.
  - Set self.out\_dir from os.path.abspath(get\_files\_path(“app\_builds”, self.app\_name)).
  - Set self.base from formatted text /files/app\_builds/{self.app\_name}/.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L23) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1917)

<a id="op-8b05530b7ab246"></a>
### Studio App Builder.build

`operation_foundation_binding_foundation_studio_build_studioappbuilder_build`

**Inputs** self.

**Explicit failure paths** StudioAppBuildError(formatted text No export folder found for app '{self.app\_name}', formatted text Expected the exported app at {self.app\_folder}.).

**Local steps**

- If self.is\_standard.
  - Set self.app\_folder from self.get\_app\_folder().
  - If not os.path.isdir(self.app\_folder).
    - Raise StudioAppBuildError(formatted text No export folder found for app '{self.app\_name}', formatted text Expected the exported app at {self.app\_folder}.).
  - Evaluate self.get\_app\_components\_from\_files().
  - Evaluate self.\_validate\_components\_resolved().
  - Evaluate self.get\_page\_scripts\_from\_files().
  - Set self.component\_scripts from mapping of script at “component\_id” → script at “file\_path” for script drawn from find\_component\_scripts(os.path.join(self.app\_folder, “studio\_components”)).
    - Draw script from find\_component\_scripts(os.path.join(self.app\_folder, “studio\_components”)).
  - Set self.router\_file from get\_router\_file(self.Platform\_app, self.app\_name).
  - Set self.tailwind\_content from get\_tailwind\_content(self.app\_folder).
  - Evaluate self.\_run\_vite\_build().
- Otherwise.
  - Within tempfile.TemporaryDirectory() bound as temp\_root.
    - Set self.app\_folder from os.path.join(temp\_root, “studio”, Platform.scrub(self.app\_name)).
    - Set self.page\_scripts from write\_db\_files\_to\_folder(self.app\_name, self.app\_folder).
    - Evaluate self.get\_app\_components().
    - Set self.router\_file from find\_router\_file(self.app\_folder).
    - Within self.\_write\_page\_sources() bound as page\_sources.
      - Set self.tailwind\_content from list(expanded get\_tailwind\_content(self.app\_folder), page\_sources.name).
      - Evaluate self.\_run\_vite\_build().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get app folder](operations-009.md#op-fd5a15be779992), [get app components from files](operations-009.md#op-655d16b224411a), [validate components resolved](operations-009.md#op-418dbc74c6bf11), [get page scripts from files](operations-009.md#op-08abc1f8b5d8cf), [run vite build](operations-009.md#op-0919ec1e9c7df0), [get app components](operations-009.md#op-0718e8fb8b335d), [write page sources](operations-009.md#op-9038897be65f22).

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0008.json#L18) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1912)
