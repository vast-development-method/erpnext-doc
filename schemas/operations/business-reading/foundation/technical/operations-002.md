# Site operations and diagnostics · operations 2

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Bundler

<a id="op-9fb004b70d010e"></a>
### Get safe max old space size

`operation_foundation_bundler_business_behavior_get_safe_maximum_old_space_size`

**Inputs** no declared parameters.

**Explicit results** safe\_max\_old\_space\_size.

**Local steps**

- Bind dependencies psutil.
- Set safe\_max\_old\_space\_size from 0.
- Attempt the following.
  - Set total\_memory from (psutil.virtual\_memory().total ÷ (1024 × 1024)).
  - Set safe\_max\_old\_space\_size from max(1024, int((total\_memory × 0.75))).
- On failure (Exception).
  - Take no action here.
- Return safe\_max\_old\_space\_size.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L1984) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L437) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L524)

<a id="op-37eb3f3667a38d"></a>
### Generate assets map

`operation_foundation_bundler_business_behavior_generate_assets_map`

**Inputs** no declared parameters.

**Explicit results** symlinks.

**Local steps**

- Set symlinks from mapping().
- For each app\_name in Platform.get\_all\_apps().
  - Set app\_doc\_path from no value.
  - Set pymodule from Platform.get\_module(app\_name).
  - Set app\_base\_path from os.path.abspath(os.path.dirname(pymodule.\_\_file\_\_)).
  - Set app\_public\_path from os.path.join(app\_base\_path, “public”).
  - Set app\_node\_modules\_path from os.path.join(app\_base\_path, “..”, “node\_modules”).
  - Set app\_docs\_path from os.path.join(app\_base\_path, “docs”).
  - Set app\_www\_docs\_path from os.path.join(app\_base\_path, “www”, “docs”).
  - Set app\_assets from os.path.abspath(app\_public\_path).
  - Set app\_node\_modules from os.path.abspath(app\_node\_modules\_path).
  - If os.path.isdir(app\_assets).
    - Set symlinks at app\_assets from os.path.join(assets\_path, app\_name).
  - If os.path.isdir(app\_node\_modules).
    - Set symlinks at app\_node\_modules from os.path.join(assets\_path, app\_name, “node\_modules”).
  - If os.path.isdir(app\_docs\_path).
    - Set app\_doc\_path from os.path.join(app\_base\_path, “docs”).
  - Otherwise.
    - If os.path.isdir(app\_www\_docs\_path).
      - Set app\_doc\_path from os.path.join(app\_base\_path, “www”, “docs”).
  - If app\_doc\_path.
    - Set app\_docs from os.path.abspath(app\_doc\_path).
    - Set symlinks at app\_docs from os.path.join(assets\_path, (app\_name + “\_docs”)).
- Return symlinks.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L2153) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L435) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L522)

<a id="op-f7eca989dbe3e3"></a>
### Remove stale island toolchain

`operation_foundation_binding_foundation_bundler_remove_stale_island_toolchain`

**Inputs** no declared parameters.

**Local steps**

- Set stale from os.path.join(Platform.get\_app\_source\_path(“Platform”), “ui”, “vite”, “island”, …).
- Evaluate shutil.rmtree(stale, ignore\_errors = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0002.json#L109) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L591) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L567)

<a id="op-5758b3df8a8b2a"></a>
### Setup assets dirs

`operation_foundation_bundler_business_behavior_setup_assets_dirs`

**Inputs** no declared parameters.

**Local steps**

- For each dir\_path in generator of os.path.join(assets\_path, x) for x drawn from tuple(“js”, “css”).
  - Draw x from tuple(“js”, “css”).
  - Evaluate os.makedirs(dir\_path, exist\_ok = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L2919) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L443) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L529)

<a id="op-252382740a5ca4"></a>
### Clear broken symlinks

`operation_foundation_bundler_business_behavior_clear_broken_symlinks`

**Inputs** no declared parameters.

**Local steps**

- For each path in os.listdir(assets\_path).
  - Set path from os.path.join(assets\_path, path).
  - If (os.path.islink(path) and not os.path.exists(path)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in os.path.islink(path) → not os.path.exists(path).
    - Evaluate os.remove(path).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L3051) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L433) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L520)

<a id="op-a7f7f48e42fcf7"></a>
### Unstrip

`operation_foundation_bundler_business_behavior_unstrip`

**Inputs** message.

**Declared result** str.

**Explicit results** formatted text {message}{(one space × \_rem)}.

**Local steps**

- Set \_len from len(message).
- Attempt the following.
  - Set max\_str from os.get\_terminal\_size().columns.
- On failure (Exception).
  - Set max\_str from 80.
- If \_len &lt; max\_str.
  - Set \_rem from (max\_str − \_len).
- Otherwise.
  - Set \_rem from (max\_str modulo or format \_len).
- Return formatted text {message}{(one space × \_rem)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L3229) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L445) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L531)

<a id="op-0d70bddea1b216"></a>
### Make asset dirs

`operation_foundation_bundler_business_behavior_make_asset_dirs`

**Inputs** hard\_link = false.

**Local steps**

- Evaluate remove\_stale\_island\_toolchain().
- Evaluate setup\_assets\_dirs().
- Evaluate clear\_broken\_symlinks().
- Set symlinks from generate\_assets\_map().
- For each tuple(source, target) in symlinks.items().
  - Set start\_message from unstrip(formatted text {“Copying assets from” when hard\_link, otherwise “Linking”} {source} to {target}).
    - Value choice on hard\_link — true gives “Copying assets from”, false gives “Linking”.
  - Set fail\_message from unstrip(formatted text Cannot {“copy” when hard\_link, otherwise “link”} {source} to {target}).
    - Value choice on hard\_link — true gives “copy”, false gives “link”.
  - Attempt the following.
    - Evaluate print(start\_message, end = whitespace '\\r').
    - Evaluate link\_assets\_dir(source, target, hard\_link = hard\_link).
  - On failure (Exception) bound to e.
    - Evaluate print(e).
    - Evaluate print(fail\_message).
- Evaluate click.echo((unstrip((click.style(“✔”, fg = “green”) + “ Application Assets Linked”)) + whitespace '\\n')).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L105) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L439) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L526)

<a id="op-36c31e05007fe1"></a>
### Link assets dir

`operation_foundation_bundler_business_behavior_link_assets_directory`

**Inputs** source, target, hard\_link = false.

**Explicit results** no value.

**Local steps**

- If not os.path.exists(source).
  - Return no value.
- If os.path.exists(target).
  - If os.path.islink(target).
    - Evaluate os.unlink(target).
  - Otherwise.
    - Evaluate shutil.rmtree(target).
- If hard\_link.
  - Evaluate shutil.copytree(source, target, dirs\_exist\_ok = true).
- Otherwise.
  - Evaluate symlink(source, target, overwrite = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L4056) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L438) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L525)

<a id="op-28bef0bf55048e"></a>
### Scrub html template

`operation_foundation_bundler_business_behavior_scrub_document_markup_template`

**Inputs** content.

**Explicit results** content.replace(“'”, “'”).

**Local steps**

- Set content from WHITESPACE\_PATTERN.sub(one space, content).
- Set content from HTML\_COMMENT\_PATTERN.sub(empty text, content).
- Return content.replace(“'”, “'”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L4336) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L441) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L527)

<a id="op-d79a26df2228fc"></a>
### Html to js template

`operation_foundation_bundler_business_behavior_document_markup_to_client_script_template`

**Inputs** path, content.

**Explicit results** “Platform.templates&#91;"{key}"&#93; = '{content}';\\n”.format(key = path.rsplit(“/”, 1) at negative 1 at slice no value to negative 5, content = scrub\_html\_template(content)).

**Local steps**

- Return “Platform.templates&#91;"{key}"&#93; = '{content}';\\n”.format(key = path.rsplit(“/”, 1) at negative 1 at slice no value to negative 5, content = scrub\_html\_template(content)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L4460) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L434) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L521)

## Service · Cache manager

<a id="op-f3ec243c34afde"></a>
### Get doctype map key

`operation_foundation_cache_manager_business_behavior_get_record_type_map_key`

**Inputs** doctype, name = “\*”.

**Declared result** str.

**Explicit results** (Platform.scrub(doctype) + formatted text \_map::{name}).

**Local steps**

- Return (Platform.scrub(doctype) + formatted text \_map::{name}).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L4635) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L462) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L547)

<a id="op-d12b7a8d50c5d2"></a>
### Clear user cache

`operation_foundation_cache_manager_business_behavior_clear_user_cache`

**Inputs** user = no value.

**Local steps**

- Bind dependencies clear\_notifications.
- Evaluate clear\_notifications(user).
- If user.
  - Evaluate Platform.cache.hdel\_names(user\_cache\_keys, user).
  - Evaluate Platform.cache.delete\_keys((“user:” + user)).
  - Evaluate clear\_defaults\_cache(user).
- Otherwise.
  - Evaluate Platform.cache.delete\_key(user\_cache\_keys).
  - Evaluate clear\_defaults\_cache().
  - Evaluate clear\_global\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L4728) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L460) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L545)

<a id="op-356244fe920463"></a>
### Clear domain cache

`operation_foundation_cache_manager_business_behavior_clear_domain_cache`

**Inputs** user = no value.

**Local steps**

- Set domain\_cache\_keys from tuple(“domain\_restricted\_doctypes”, “domain\_restricted\_pages”).
- Evaluate Platform.cache.delete\_value(domain\_cache\_keys).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L4948) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L454) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L539)

<a id="op-5a09b9e5addd91"></a>
### Clear global cache

`operation_foundation_cache_manager_business_behavior_clear_global_cache`

**Inputs** no declared parameters.

**Local steps**

- Bind dependencies clear\_website\_cache.
- Evaluate clear\_doctype\_cache().
- Evaluate clear\_website\_cache().
- Evaluate Platform.cache.delete\_value(global\_cache\_keys).
- Evaluate Platform.cache.delete\_value(bench\_cache\_keys, shared = true).
- Evaluate Platform.setup\_module\_map().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L5031) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L455) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L540)

<a id="op-7d0f0e44948882"></a>
### Clear defaults cache

`operation_foundation_cache_manager_business_behavior_clear_defaults_cache`

**Inputs** user = no value.

**Local steps**

- If user.
  - For each key in list(user, expanded common\_default\_keys).
    - Evaluate Platform.client\_cache.delete\_value(formatted text defaults::{key}).
- Otherwise.
  - If Platform.flags.in\_install differs from “Platform”.
    - Evaluate Platform.client\_cache.delete\_keys(“defaults::\*”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L5178) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L453) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L538)

<a id="op-9e5c2cee7196cf"></a>
### Clear doctype cache

`operation_foundation_cache_manager_business_behavior_clear_record_type_cache`

**Inputs** doctype = no value.

**Local steps**

- Evaluate clear\_controller\_cache(doctype).
- Evaluate Platform.client\_cache.erase\_persistent\_caches(doctype = doctype).
- If doctype.
  - Evaluate Platform.local.valid\_columns.pop(doctype, no value).
- Otherwise.
  - Set Platform.local.valid\_columns from mapping().
- Evaluate \_clear\_doctype\_cache\_from\_redis(doctype).
- If hasattr(Platform.db, “after\_commit”).
  - Evaluate Platform.db.after\_commit.add(deferred anonymous expression).
  - Evaluate Platform.db.after\_rollback.add(deferred anonymous expression).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L5350) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L456) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L541)

<a id="op-3cdd0e15f4cf95"></a>
### Clear doctype cache from redis

`operation_foundation_cache_manager_business_behavior_clear_record_type_cache_from_cache_service`

**Inputs** doctype = no value.

**Record and data access** read “DocField” via get\_all · read “Custom Field” via get\_all.

**Local steps**

- Bind dependencies delete\_notification\_count\_for.
- Bind dependencies clear\_notification\_cache.
- Bind dependencies clear\_meta\_cache.
- Set to\_del from list(“is\_table”, “doctype\_modules”).
- If doctype.
  - Bind local operation clear\_single for subsequent calls.
  - Evaluate clear\_single(doctype).
  - Attempt the following.
    - For each dt in Platform.get\_all(“DocField”, “parent”, dict(fieldtype = list(“in”, Platform.model.table\_fields), options = doctype), ignore\_ddl = true).
      - Evaluate clear\_single(dt.parent).
    - If not Platform.flags.in\_install.
      - For each dt in Platform.get\_all(“Custom Field”, “dt”, dict(fieldtype = list(“in”, Platform.model.table\_fields), options = doctype), ignore\_ddl = true).
        - Evaluate clear\_single(dt.dt).
  - On failure (Platform.DoesNotExistError).
    - Take no action here.
  - Evaluate delete\_notification\_count\_for(doctype).
- Otherwise.
  - Update to\_del using + doctype\_cache\_keys.
  - For each pattern in wildcard\_keys.
    - Update to\_del using + Platform.cache.get\_keys(pattern).
  - Evaluate clear\_meta\_cache().
- Evaluate clear\_notification\_cache().
- Evaluate Platform.cache.delete\_value(to\_del).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L5651) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L457) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L542)

<a id="op-b07118b71fe4d2"></a>
### Clear doctype cache from redis.clear single

`operation_foundation_cache_manager_business_behavior_clear_record_type_cache_from_cache_service_clear_single`

**Inputs** dt.

**Local steps**

- Evaluate Platform.clear\_document\_cache(dt).
- Evaluate Platform.client\_cache.delete\_keys(formatted text \*{dt}\*).
- Evaluate Platform.cache.hdel\_names(doctype\_cache\_keys, dt).
- Evaluate clear\_meta\_cache(dt).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0548.json#L3909) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L458) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L543)

<a id="op-d7712f9468e431"></a>
### Clear controller cache

`operation_foundation_cache_manager_business_behavior_clear_controller_cache`

**Inputs** doctype = no value, site (named only, default no value).

**Explicit results** no value.

**Local steps**

- If not doctype.
  - Evaluate Platform.controllers.pop((site or Platform.local.site), no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.
  - Evaluate Platform.lazy\_controllers.pop((site or Platform.local.site), no value).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.
  - Return no value.
- If site\_controllers bound to Platform.controllers.get((site or Platform.local.site)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.
  - Evaluate site\_controllers.pop(doctype, no value).
- If lazy\_site\_controllers bound to Platform.lazy\_controllers.get((site or Platform.local.site)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.
  - Evaluate lazy\_site\_controllers.pop(doctype, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L6357) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L452) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L537)

<a id="op-e5c877b2f29b49"></a>
### Get doctype map

`operation_foundation_cache_manager_business_behavior_get_record_type_map`

**Inputs** doctype, name, filters = no value, order\_by = no value.

**Explicit results** Platform.client\_cache.get\_value(get\_doctype\_map\_key(doctype, name), generator = deferred anonymous expression).

**Local steps**

- Return Platform.client\_cache.get\_value(get\_doctype\_map\_key(doctype, name), generator = deferred anonymous expression).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L6679) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L461) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L546)

<a id="op-512036cba30304"></a>
### Clear doctype map

`operation_foundation_cache_manager_business_behavior_clear_record_type_map`

**Inputs** doctype, name = “\*”.

**Local steps**

- Evaluate Platform.client\_cache.delete\_keys(get\_doctype\_map\_key(doctype, name)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0018.json#L6843) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L459) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L544)

<a id="op-4914219929bf77"></a>
### Build table count cache

`operation_foundation_cache_manager_business_behavior_build_table_count_cache`

**Inputs** no declared parameters.

**State and service calls** execute a supplied database query.

**Explicit results** no value · counts.

**Local steps**

- If (Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_import or Platform.flags.in\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_patch → Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_import → Platform.flags.in\_setup\_wizard.
  - Return no value.
- If Platform.db.db\_type differs from “sqlite”.
  - Set table\_name from Platform.qb.Field(“table\_name”).as\_(“name”).
  - Set table\_rows from Platform.qb.Field(“table\_rows”).as\_(“count”).
  - Set information\_schema from Platform.qb.Schema(“information\_schema”).
  - Set query from Platform.qb.from\_(information\_schema.tables).select(table\_name, table\_rows).
  - If Platform.db.db\_type equals “postgres”.
    - Set query from query.where(Platform.qb.Field(“schemaname”) equals Platform.db.db\_schema).
  - Otherwise.
    - Set query from query.where(information\_schema.tables.table\_schema equals Platform.db.cur\_db\_name).
  - Set data from query.run(as\_dict = true).
  - Set counts from mapping of d.get(“name”).replace(“tab”, empty text, 1) → d.get(“count”, no value) for d drawn from data.
    - Draw d from data.
  - Evaluate Platform.cache.set\_value(“information\_schema:counts”, counts).
- Otherwise.
  - Set counts from mapping().
  - Set name from Platform.qb.Field(“name”).
  - Set type from Platform.qb.Field(“type”).
  - Set sqlite\_master from Platform.qb.Schema(“sqlite\_master”).
  - Set data from nested operand in the contract(nested operand in the contract).select(name).where(type equals “table”).run(as\_dict = true).
  - For each table in data.
    - Set count from Platform.db.sql(formatted text SELECT COUNT(\*) FROM ′{table.name}′) at 0 at 0.
    - Set counts at table.name.replace(“tab”, empty text, 1) from count.
  - Evaluate Platform.cache.set\_value(“information\_schema:counts”, counts).
- Return counts.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L107) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L450) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L535)

<a id="op-5385cbe137589e"></a>
### Build domain restricted doctype cache

`operation_foundation_cache_manager_business_behavior_build_domain_restricted_record_type_cache`

**Inputs** remaining positional values args, remaining named values kwargs.

**Record and data access** read “DocType” via get\_all.

**Explicit results** no value · doctypes.

**Local steps**

- If (Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_import or Platform.flags.in\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_patch → Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_import → Platform.flags.in\_setup\_wizard.
  - Return no value.
- Set active\_domains from Platform.get\_active\_domains().
- Set doctypes from Platform.get\_all(“DocType”, filters = mapping(“restrict\_to\_domain” → tuple(“IN”, active\_domains))).
- Set doctypes from list of doc.name for doc drawn from doctypes.
  - Draw doc from doctypes.
- Evaluate Platform.cache.set\_value(“domain\_restricted\_doctypes”, doctypes).
- Return doctypes.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L449) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L534)

<a id="op-40bbb36e2f0c17"></a>
### Build domain restricted page cache

`operation_foundation_cache_manager_business_behavior_build_domain_restricted_page_cache`

**Inputs** remaining positional values args, remaining named values kwargs.

**Record and data access** read “Page” via get\_all.

**Explicit results** no value · pages.

**Local steps**

- If (Platform.flags.in\_patch or Platform.flags.in\_install or Platform.flags.in\_migrate or Platform.flags.in\_import or Platform.flags.in\_setup\_wizard).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.flags.in\_patch → Platform.flags.in\_install → Platform.flags.in\_migrate → Platform.flags.in\_import → Platform.flags.in\_setup\_wizard.
  - Return no value.
- Set active\_domains from Platform.get\_active\_domains().
- Set pages from Platform.get\_all(“Page”, filters = mapping(“restrict\_to\_domain” → tuple(“IN”, active\_domains))).
- Set pages from list of page.name for page drawn from pages.
  - Draw page from pages.
- Evaluate Platform.cache.set\_value(“domain\_restricted\_pages”, pages).
- Return pages.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0019.json#L292) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L448) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L533)
