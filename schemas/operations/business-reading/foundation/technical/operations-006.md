# Site operations and diagnostics · operations 6

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Installer

<a id="op-68486822692571"></a>
### Is scheduler enabled

`operation_foundation_installer_business_behavior_is_scheduler_enabled`

**Inputs** site.

**Declared result** bool.

**Record and data access** read “System Settings” via get\_single\_value.

**Explicit results** bool(enable\_scheduler).

**Local steps**

- Set enable\_scheduler from false.
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Set enable\_scheduler from cint(Platform.db.get\_single\_value(“System Settings”, “enable\_scheduler”)).
- On failure (Exception).
  - Take no action here.
- On exit, including pending return or failure.
  - Evaluate Platform.db.close().
- Return bool(enable\_scheduler).

**Values supplied outside this operation** configured or stored value from Platform.db.get\_single\_value(“System Settings”, “enable\_scheduler”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L4236) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1792) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L532)

<a id="op-68ffece5c5dde3"></a>
### New site

`operation_foundation_installer_business_behavior_new_site`

**Inputs** db\_name, site, db\_root\_username = no value, db\_root\_password = no value, admin\_password = no value, verbose = false, install\_apps = no value, source\_sql = no value, force = false, db\_password = no value, db\_type = no value, db\_socket = no value, db\_host = no value, db\_port = no value, db\_user = no value, setup\_db = true, rollback\_callback = no value, mariadb\_user\_host\_login\_scope = no value.

**State and service calls** commit.

**Local steps**

- Bind dependencies scheduler.
- If (not force and os.path.exists(site)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not force → os.path.exists(site).
  - Evaluate print(formatted text Site {site} already exists, use ′--force′ to proceed anyway).
  - Evaluate sys.exit(1).
- Evaluate Platform.init(site).
- If not db\_name.
  - Set db\_name from formatted text \_{Platform.generate\_hash(length = 16)}.
- Attempt the following.
  - Set enable\_scheduler from \_is\_scheduler\_enabled(site).
- On failure (Exception).
  - Set enable\_scheduler from false.
- Evaluate clear\_site\_locks().
- Evaluate make\_site\_dirs().
- If rollback\_callback.
  - Evaluate rollback\_callback.add(deferred anonymous expression).
- Within filelock(“bench\_new\_site”, timeout = 1).
  - Evaluate install\_db(root\_login = db\_root\_username, root\_password = db\_root\_password, db\_name = db\_name, admin\_password = admin\_password, …).
  - Set apps\_to\_install from ((list(“Platform”) + (Platform.conf.get(“install\_apps”) or list())) + list((install\_apps or list()))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“install\_apps”) → list().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in install\_apps → list().
  - For each app in apps\_to\_install.
    - Evaluate install\_app(app, verbose = verbose, set\_as\_patched = not source\_sql, force = false).
  - Evaluate scheduler.toggle\_scheduler(enable\_scheduler).
  - Evaluate Platform.db.commit().
- Set scheduler\_status from “disabled” when Platform.utils.scheduler.is\_scheduler\_disabled(), otherwise “enabled”.
  - Value choice on Platform.utils.scheduler.is\_scheduler\_disabled() — true gives “disabled”, false gives “enabled”.
- Evaluate print(“\*\*\* Scheduler is”, scheduler\_status, “\*\*\*”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 16).

**Boundaries to resolve** stored data, late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L4454) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1796) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L536)

<a id="op-3507b312d8b9df"></a>
### Install db

`operation_foundation_installer_business_behavior_install_database`

**Inputs** root\_login = no value, root\_password = no value, db\_name = no value, source\_sql = no value, admin\_password = no value, verbose = true, force = 0, site\_config = no value, db\_password = no value, db\_type = no value, db\_socket = no value, db\_host = no value, db\_port = no value, db\_user = no value, setup = true, rollback\_callback = no value, mariadb\_user\_host\_login\_scope = no value.

**Local steps**

- Bind dependencies Platform.database.
- Bind dependencies bootstrap\_database, drop\_user\_and\_database, setup\_database.
- If not db\_type.
  - Set db\_type from Platform.conf.db\_type.
- Evaluate make\_conf(db\_name, site\_config = site\_config, db\_password = db\_password, db\_type = db\_type, db\_socket = db\_socket, …).
- Set Platform.flags.in\_install\_db from true.
- If root\_login.
  - Set Platform.flags.root\_login from root\_login.
- If root\_password.
  - Set Platform.flags.root\_password from root\_password.
- If setup.
  - Evaluate setup\_database(force, verbose, mariadb\_user\_host\_login\_scope).
  - If rollback\_callback.
    - Evaluate rollback\_callback.add(deferred anonymous expression).
- Evaluate bootstrap\_database(verbose = verbose, source\_sql = source\_sql).
- Set Platform.conf.admin\_password from (Platform.conf.admin\_password or admin\_password).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.admin\_password → admin\_password.
- Evaluate remove\_missing\_apps().
- Evaluate Platform.db.create\_auth\_table().
- Evaluate Platform.db.create\_global\_search\_table().
- Evaluate Platform.db.create\_user\_settings\_table().
- Set Platform.flags.in\_install\_db from false.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L40) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1788) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L528)

<a id="op-38edc4154a4cc8"></a>
### Find org

`operation_foundation_installer_business_behavior_find_organization`

**Inputs** org\_repo.

**Declared result** tuple at tuple(str, str).

**Explicit results** tuple(org, org\_repo).

**Explicit failure paths** InvalidRemoteException.

**Local steps**

- Bind dependencies requests.
- Bind dependencies InvalidRemoteException.
- For each org in list(“Platform”, “Enterprise”).
  - Set response from requests.head(formatted command or address in the contract).
  - If response.status\_code equals 400.
    - Set response from requests.head(formatted command or address in the contract).
  - If response.ok.
    - Return tuple(org, org\_repo).
- Raise InvalidRemoteException.

**Values supplied outside this operation** service or queued work from requests.head(formatted command or address in the contract).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L6255) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1777) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L517)

<a id="op-3042da929b1396"></a>
### Fetch details from tag

`operation_foundation_installer_business_behavior_fetch_details_from_tag`

**Inputs** \_tag.

**Declared result** tuple at tuple(str, str, str).

**Explicit results** tuple(org, repo, tag).

**Local steps**

- Set app\_tag from \_tag.split(“@”).
- Set org\_repo from app\_tag at 0.split(“/”).
- Attempt the following.
  - Set tuple(repo, tag) from app\_tag.
- On failure (ValueError).
  - Set tuple(repo, tag) from list(expanded app\_tag, no value).
- Attempt the following.
  - Set tuple(org, repo) from org\_repo.
- On failure (Exception).
  - Set tuple(org, repo) from find\_org(org\_repo at 0).
- Return tuple(org, repo, tag).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L6539) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1776) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L516)

<a id="op-ba5b50c69a9449"></a>
### Parse app name

`operation_foundation_installer_business_behavior_parse_application_name`

**Inputs** name.

**Declared result** str.

**Explicit results** name · repo.

**Local steps**

- Set name from name.rstrip(“/”).
- If os.path.exists(name).
  - Set repo from os.path.split(name) at negative 1.
- Otherwise.
  - If is\_git\_url(name).
    - If (name.startswith(“git@”) or name.startswith(“ssh://”)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in name.startswith(“git@”) → name.startswith(“ssh://”).
      - Set \_repo from name.split(“:”) at 1.rsplit(“/”, 1) at 1.
    - Otherwise.
      - Set \_repo from name.rsplit(“/”, 2) at 2.
    - Set repo from \_repo.split(“.”, 1) at 0.
  - Otherwise.
    - If name belongs to Platform.get\_all\_apps().
      - Return name.
    - Otherwise.
      - Set tuple(\_, repo, \_) from fetch\_details\_from\_tag(name).
- Return repo.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L6843) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1797) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L537)

<a id="op-872233d46b5db8"></a>
### Parse required app name

`operation_foundation_installer_business_behavior_parse_required_application_name`

**Inputs** requirement.

**Declared result** str.

**Explicit results** name.split(“@”) at 0.removesuffix(“.git”).

**Local steps**

- Set name from requirement.rstrip(“/”).split(“#”) at 0.
- Set name from name.rsplit(“/”, 1) at negative 1.rsplit(“:”, 1) at negative 1.
- Return name.split(“@”) at 0.removesuffix(“.git”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L7294) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1798) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L538)

<a id="op-9e1e7c7e2ec414"></a>
### Is required by

`operation_foundation_installer_business_behavior_is_required_by`

**Inputs** app\_name, dependent\_app.

**Declared result** bool.

**Explicit results** any(generator of app\_name equals parse\_required\_app\_name(required\_app) for required\_app drawn from Platform.get\_hooks(“required\_apps”, app\_name = dependent\_app)).

**Local steps**

- Return any(generator of app\_name equals parse\_required\_app\_name(required\_app) for required\_app drawn from Platform.get\_hooks(“required\_apps”, app\_name = dependent\_app)).
  - Draw required\_app from Platform.get\_hooks(“required\_apps”, app\_name = dependent\_app).

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“required\_apps”, app\_name = dependent\_app).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0244.json#L7505) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1791) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L531)

<a id="op-efcd3a29119354"></a>
### Install app

`operation_foundation_installer_business_behavior_install_application`

**Inputs** name, verbose = false, set\_as\_patched = true, force = false.

**Record and data access** resolve a document from “Portal Settings” via get\_doc.

**Explicit results** no value.

**Explicit failure paths** Exception(formatted text App {name} not in apps.txt).

**Local steps**

- Bind dependencies sync\_jobs.
- Bind dependencies sync\_for.
- Bind dependencies sync\_customizations.
- Bind dependencies sync\_fixtures.
- Set Platform.flags.in\_install from name.
- Set Platform.flags.ignore\_in\_install from false.
- Evaluate Platform.clear\_cache().
- Set app\_hooks from Platform.get\_hooks(app\_name = name).
- Set installed\_apps from Platform.get\_installed\_apps().
- If app\_hooks.required\_apps.
  - For each app in app\_hooks.required\_apps.
    - Set required\_app from parse\_app\_name(app).
    - Evaluate install\_app(required\_app, verbose = verbose).
- Set Platform.flags.in\_install from name.
- Evaluate Platform.clear\_cache().
- If name does not belong to Platform.get\_all\_apps().
  - Raise Exception(formatted text App {name} not in apps.txt).
- If (not force and name belongs to installed\_apps).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not force → name belongs to installed\_apps.
  - Evaluate click.secho(formatted text App {name} already installed, fg = “yellow”).
  - Return no value.
- Evaluate print(formatted text  Installing {name}...).
- Set other\_class\_overrides from Platform.get\_hooks(“override\_doctype\_class”).
- If (other\_class\_overrides and app\_hooks.override\_doctype\_class and any(generator of dt belongs to app\_hooks.override\_doctype\_class for dt drawn from other\_class\_overrides)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in other\_class\_overrides → app\_hooks.override\_doctype\_class → any(generator of dt belongs to app\_hooks.override\_doctype\_class for dt drawn from other\_class\_overrides).
  - Draw dt from other\_class\_overrides.
  - Evaluate click.secho(formatted text App {name} overrides a doctype that is already overridden by another app., fg = “yellow”).
- If name differs from “Platform”.
  - Evaluate Platform.only\_for(“System Manager”).
- For each before\_install in (app\_hooks.before\_install or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_hooks.before\_install → list().
  - Set out from Platform.get\_attr(before\_install)().
  - If out is identical to false.
    - Return no value.
- For each fn in Platform.get\_hooks(“before\_app\_install”).
  - Evaluate Platform.get\_attr(fn)(name).
- If name differs from “Platform”.
  - Evaluate add\_module\_defs(name, ignore\_if\_duplicate = force).
- If name does not belong to (Platform.local.app\_modules or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.local.app\_modules → mapping().
  - Evaluate Platform.cache.delete\_value(“app\_modules”).
  - Evaluate Platform.setup\_module\_map(include\_all\_apps = true).
- Evaluate sync\_for(name, force = force, reset\_permissions = true).
- If name equals “Platform”.
  - Evaluate add\_module\_defs(name, ignore\_if\_duplicate = true).
- Evaluate add\_to\_installed\_apps(name).
- Evaluate Platform.get\_doc(“Portal Settings”, “Portal Settings”).sync\_menu().
- If set\_as\_patched.
  - Evaluate set\_all\_patches\_as\_completed(name).
- For each after\_install in (app\_hooks.after\_install or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_hooks.after\_install → list().
  - Evaluate Platform.get\_attr(after\_install)().
- For each fn in Platform.get\_hooks(“after\_app\_install”).
  - Evaluate Platform.get\_attr(fn)(name).
- Evaluate sync\_jobs().
- Evaluate sync\_fixtures(name).
- Evaluate sync\_customizations(name).
- Evaluate sync\_dashboards(name).
- For each after\_sync in (app\_hooks.after\_sync or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_hooks.after\_sync → list().
  - Evaluate Platform.get\_attr(after\_sync)().
- Evaluate Platform.clear\_cache().
- Evaluate Platform.client\_cache.erase\_persistent\_caches().
- Set Platform.flags.in\_install from false.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(app\_name = name), Platform.get\_hooks(“override\_doctype\_class”) and 6 further calls · effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L39) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1787) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L527)

<a id="op-0ed6d9bb815bc7"></a>
### Add to installed apps

`operation_foundation_installer_business_behavior_add_to_installed_apps`

**Inputs** app\_name, rebuild\_website = true.

**Record and data access** read “Installed Applications” via get\_single.

**State and service calls** commit.

**Local steps**

- Set installed\_apps from Platform.get\_installed\_apps().
- If app\_name does not belong to installed\_apps.
  - Evaluate installed\_apps.append(app\_name).
  - Evaluate Platform.db.set\_global(“installed\_apps”, json.dumps(installed\_apps)).
  - Evaluate Platform.db.commit().
  - If Platform.flags.in\_install.
    - Evaluate post\_install(rebuild\_website).
- Evaluate Platform.get\_single(“Installed Applications”).update\_versions().
- Evaluate Platform.db.commit().
- Evaluate \_sync\_installed\_apps\_to\_site\_config().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0245.json#L1644) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1766) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L508)

<a id="op-1324e9566ec4ff"></a>
### Remove from installed apps

`operation_foundation_installer_business_behavior_remove_from_installed_apps`

**Inputs** app\_name.

**Record and data access** read “Installed Applications” via get\_single.

**State and service calls** request set\_value on “DefaultValue” · commit.

**Local steps**

- Set installed\_apps from Platform.get\_installed\_apps().
- If app\_name belongs to installed\_apps.
  - Evaluate installed\_apps.remove(app\_name).
  - Evaluate Platform.db.set\_value(“DefaultValue”, mapping(“defkey” → “installed\_apps”), “defvalue”, json.dumps(installed\_apps)).
  - Evaluate \_clear\_cache(“\_\_global”).
  - Set Platform.local.doc\_events\_hooks from no value.
  - Evaluate Platform.get\_single(“Installed Applications”).update\_versions().
  - Evaluate Platform.db.commit().
  - If Platform.flags.in\_install.
    - Evaluate post\_install().
  - Evaluate \_sync\_installed\_apps\_to\_site\_config().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L42) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1805) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L544)

<a id="op-1a8e1bd08b1b4d"></a>
### Remove app

`operation_foundation_installer_business_behavior_remove_application`

**Inputs** app\_name, dry\_run = false, yes = false, no\_backup = false, force = false.

**Record and data access** read “Installed Applications” via get\_single.

**State and service calls** commit.

**Explicit results** no value.

**Local steps**

- Set site from Platform.local.site.
- Set app\_hooks from Platform.get\_hooks(app\_name = app\_name).
- If not force.
  - If app\_name does not belong to Platform.get\_installed\_apps().
    - Evaluate click.secho(formatted text App {app\_name} not installed on Site {site}, fg = “yellow”).
    - Return no value.
- For each app in Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - If (app differs from app\_name and is\_required\_by(app\_name, app)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in app differs from app\_name → is\_required\_by(app\_name, app).
    - Evaluate click.secho(formatted text App {app\_name} is a dependency of {app}. Uninstall {app} first., fg = “yellow”).
    - Return no value.
- Evaluate print(formatted text Uninstalling App {app\_name} from Site {site}...).
- If (not dry\_run and not yes).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not dry\_run → not yes.
  - Set confirm from click.confirm(“All doctypes (including custom) and modules belonging to this app will be deleted. This site's own custom mo …”).
  - If not confirm.
    - Return no value.
- If not (dry\_run or no\_backup).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in dry\_run → no\_backup.
  - Bind dependencies scheduled\_backup.
  - Evaluate print(“Backing up...”).
  - Evaluate scheduled\_backup(ignore\_files = true).
- Set Platform.flags.in\_uninstall from true.
- For each before\_uninstall in (app\_hooks.before\_uninstall or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_hooks.before\_uninstall → list().
  - Evaluate Platform.get\_attr(before\_uninstall)().
- For each fn in Platform.get\_hooks(“before\_app\_uninstall”).
  - Evaluate Platform.get\_attr(fn)(app\_name).
- Set app\_modules from get\_app\_owned\_modules(app\_name).
- Set drop\_doctypes from \_delete\_modules(app\_modules, dry\_run = dry\_run).
- Evaluate \_delete\_doctypes(drop\_doctypes, dry\_run = dry\_run).
- Evaluate \_delete\_module\_defs(app\_modules, dry\_run = dry\_run).
- Evaluate release\_custom\_module\_placements(app\_name, dry\_run = dry\_run).
- If not dry\_run.
  - Evaluate remove\_from\_installed\_apps(app\_name).
  - Evaluate Platform.get\_single(“Installed Applications”).update\_versions().
  - Evaluate Platform.db.commit().
  - Evaluate Platform.clear\_cache().
- For each after\_uninstall in (app\_hooks.after\_uninstall or list()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in app\_hooks.after\_uninstall → list().
  - Evaluate Platform.get\_attr(after\_uninstall)().
- For each fn in Platform.get\_hooks(“after\_app\_uninstall”).
  - Evaluate Platform.get\_attr(fn)(app\_name).
- Evaluate Platform.client\_cache.erase\_persistent\_caches().
- Evaluate click.secho(formatted text Uninstalled App {app\_name} from Site {site}, fg = “green”).
- Set Platform.flags.in\_uninstall from false.
- If not dry\_run.
  - Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(app\_name = app\_name), Platform.get\_attr(before\_uninstall) and 4 further calls.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L41) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1804) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L543)

<a id="op-05b0aaa2c89ba4"></a>
### Delete modules

`operation_foundation_installer_business_behavior_delete_modules`

**Inputs** modules, dry\_run.

**Declared result** list at str.

**Record and data access** read “DocType” via get\_all.

**State and service calls** request delete\_doc for doctype.name · request delete\_doc for “DocType”.

**Explicit results** drop\_doctypes.

**Local steps**

- Set drop\_doctypes from list().
- Set doctype\_link\_field\_map from \_get\_module\_linked\_doctype\_field\_map().
- For each module\_name in modules.
  - Evaluate print(formatted text Deleting Module '{module\_name}').
  - For each doctype in Platform.get\_all(“DocType”, filters = mapping(“module” → module\_name), fields = list(“name”, “issingle”)).
    - Evaluate print(formatted text \* removing DocType '{doctype.name}'...).
    - If not dry\_run.
      - If doctype.issingle.
        - Evaluate Platform.delete\_doc(doctype.name, doctype.name, ignore\_on\_trash = true, force = true).
        - Evaluate Platform.delete\_doc(“DocType”, doctype.name, ignore\_on\_trash = true, force = true).
      - Otherwise.
        - Evaluate drop\_doctypes.append(doctype.name).
  - Evaluate \_delete\_linked\_documents(module\_name, doctype\_link\_field\_map, dry\_run = dry\_run).
- Return drop\_doctypes.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L35) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1771) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L513)

<a id="op-989e09836da99d"></a>
### Delete module defs

`operation_foundation_binding_foundation_installer_delete_module_defs`

**Inputs** modules, dry\_run.

**Declared result** no value.

**State and service calls** request delete\_doc for “Module Def”.

**Local steps**

- For each module\_name in modules.
  - Evaluate print(formatted text \* removing Module Def '{module\_name}'...).
  - If not dry\_run.
    - Evaluate Platform.delete\_doc(“Module Def”, module\_name, ignore\_on\_trash = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0006.json#L44) · [Binding](../../../current-decisions/foundation/bindings-001.tsv#L1500) · [Declaration location](../../../current-decisions/foundation/evidence/locations-001.tsv#L1476)

<a id="op-aeb243e53f1e3a"></a>
### Delete linked documents

`operation_foundation_installer_business_behavior_delete_linked_documents`

**Inputs** module\_name, doctype\_linkfield\_map, dry\_run.

**Declared result** no value.

**Record and data access** read doctype via get\_all.

**State and service calls** request delete\_doc for doctype.

**Local steps**

- For each tuple(doctype, fieldname) in doctype\_linkfield\_map.items().
  - For each record in Platform.get\_all(doctype, filters = mapping(fieldname → module\_name), pluck = “name”).
    - Evaluate print(formatted text \* removing {doctype} '{record}'...).
    - If not dry\_run.
      - Evaluate Platform.delete\_doc(doctype, record, ignore\_on\_trash = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0245.json#L6264) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1770) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L512)

<a id="op-21fdf809dcb18a"></a>
### Get module linked doctype field map

`operation_foundation_installer_business_behavior_get_module_linked_record_type_field_map`

**Inputs** no declared parameters.

**Declared result** dict at tuple(str, str).

**Record and data access** read “DocField” via get\_all · read “DocType” via exists.

**Explicit results** doctype\_to\_field\_map.

**Local steps**

- Set ordered\_doctypes from list(tuple(“Workspace”, “module”), tuple(“Report”, “module”), tuple(“Page”, “module”), tuple(“Web Form”, “module”)).
- Set doctype\_to\_field\_map from OrderedDict(ordered\_doctypes).
- Set linked\_doctypes from Platform.get\_all(“DocField”, filters = mapping(“fieldtype” → “Link”, “options” → “Module Def”), fields = list(“parent”, “fieldname”)).
- Set tables from Platform.db.get\_tables(cached = false).
- Set existing\_linked\_doctypes from list of d for d drawn from linked\_doctypes where (Platform.db.exists(“DocType”, d.parent) and formatted text tab{d.parent} belongs to tables).
  - Draw d from linked\_doctypes, keep a combination only if ((Platform.db.exists(“DocType”, d.parent) and formatted text tab{d.parent} belongs to tables)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.db.exists(“DocType”, d.parent) → formatted text tab{d.parent} belongs to tables.
- For each d in existing\_linked\_doctypes.
  - If (d.parent does not belong to doctype\_to\_field\_map and d.parent differs from “DocType”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.parent does not belong to doctype\_to\_field\_map → d.parent differs from “DocType”.
    - Set doctype\_to\_field\_map at d.parent from d.fieldname.
- Return doctype\_to\_field\_map.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L38) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1782) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L522)

<a id="op-99eac4e8cbfe0a"></a>
### Delete doctypes

`operation_foundation_installer_business_behavior_delete_record_types`

**Inputs** doctypes, dry\_run.

**Declared result** no value.

**State and service calls** request delete\_doc for “DocType”.

**Local steps**

- For each doctype in set(doctypes).
  - Evaluate print(formatted text \* dropping Table for '{doctype}'...).
  - If not dry\_run.
    - Evaluate Platform.db.sql\_ddl(formatted text DROP TABLE IF EXISTS ′tab{doctype}′).
    - Evaluate Platform.delete\_doc(“DocType”, doctype, ignore\_on\_trash = true, force = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L36) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1772) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L514)

<a id="op-e9e52c7dce077f"></a>
### Post install

`operation_foundation_installer_business_behavior_post_install`

**Inputs** rebuild\_website = false.

**State and service calls** commit.

**Local steps**

- Bind dependencies clear\_website\_cache.
- If rebuild\_website.
  - Evaluate clear\_website\_cache().
- Evaluate init\_singles().
- Evaluate Platform.db.commit().
- Evaluate Platform.clear\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0245.json#L7271) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1800) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L540)

<a id="op-cbe6c501c6d46c"></a>
### Set all patches as completed

`operation_foundation_installer_business_behavior_set_all_patches_as_completed`

**Inputs** app.

**Record and data access** resolve a document from mapping(“doctype” → “Patch Log”, “patch” → patch) via get\_doc.

**State and service calls** call insert on Platform.get\_doc(mapping(“doctype” → “Patch Log”, “patch” → patch)) · commit.

**Local steps**

- Bind dependencies get\_patches\_from\_app.
- Set patches from get\_patches\_from\_app(app).
- For each patch in patches.
  - Evaluate Platform.get\_doc(mapping(“doctype” → “Patch Log”, “patch” → patch)).insert(ignore\_permissions = true).
- Evaluate Platform.db.commit().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0245.json#L7397) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1808) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L547)

<a id="op-64bf5f91bfaba2"></a>
### Init singles

`operation_foundation_installer_business_behavior_initialize_singles`

**Inputs** no declared parameters.

**Record and data access** read “DocType” via get\_all.

**State and service calls** request new\_doc for single · call save on doc.

**Local steps**

- Set singles from Platform.get\_all(“DocType”, filters = mapping(“issingle” → true), pluck = “name”).
- For each single in singles.
  - If Platform.db.get\_singles\_dict(single).
    - Continue with the next iteration or loop test.
  - Attempt the following.
    - Set doc from Platform.new\_doc(single).
    - Set doc.flags.ignore\_mandatory from true.
    - Set doc.flags.ignore\_validate from true.
    - Evaluate doc.save().
  - On failure (tuple(ImportError, Platform.DoesNotExistError)).
    - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L6) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1786) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L526)

<a id="op-3ebe853ebfd4c0"></a>
### Make conf

`operation_foundation_installer_business_behavior_make_configuration`

**Inputs** db\_name = no value, db\_password = no value, site\_config = no value, db\_type = no value, db\_socket = no value, db\_host = no value, db\_port = no value, db\_user = no value.

**Local steps**

- Set site from Platform.local.site.
- Evaluate make\_site\_config(db\_name, db\_password, site\_config, db\_type = db\_type, db\_socket = db\_socket, db\_host = db\_host, db\_port = db\_port, …).
- Set sites\_path from Platform.local.sites\_path.
- Evaluate Platform.destroy().
- Evaluate Platform.init(site, sites\_path = sites\_path).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L280) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1793) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L533)

<a id="op-91dbc87fb3a817"></a>
### Make site config

`operation_foundation_installer_business_behavior_make_site_configuration`

**Inputs** db\_name = no value, db\_password = no value, site\_config = no value, db\_type = no value, db\_socket = no value, db\_host = no value, db\_port = no value, db\_user = no value.

**Local steps**

- Evaluate Platform.create\_folder(os.path.join(Platform.local.site\_path)).
- Set site\_file from get\_site\_config\_path().
- If not os.path.exists(site\_file).
  - If not (site\_config and isinstance(site\_config, dict)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in site\_config → isinstance(site\_config, dict).
    - Set site\_config from get\_conf\_params(db\_name, db\_password).
    - If db\_type.
      - Set site\_config at “db\_type” from db\_type.
    - If db\_type equals “sqlite”.
      - Set site\_config at “db\_name” from db\_name.
    - Otherwise.
      - If db\_socket.
        - Set site\_config at “db\_socket” from db\_socket.
      - If db\_host.
        - Set site\_config at “db\_host” from db\_host.
      - If db\_port.
        - Set site\_config at “db\_port” from db\_port.
      - Set site\_config at “db\_user” from (db\_user or db\_name).
        - Evaluate in order, stop at the first true operand, otherwise use the last operand in db\_user → db\_name.
  - Within open(site\_file, “w”) bound as f.
    - Evaluate f.write(json.dumps(site\_config, indent = 1, sort\_keys = true)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L562) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1794) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L534)

<a id="op-12de4ca6b7bfa7"></a>
### Sync installed apps to site config

`operation_foundation_installer_business_behavior_sync_installed_apps_to_site_configuration`

**Inputs** no declared parameters.

**Local steps**

- Attempt the following.
  - Evaluate update\_site\_config(“installed\_apps”, Platform.get\_installed\_apps()).
- On failure (Exception).
  - Take no action here.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L1130) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1810) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L548)

<a id="op-d89935e8b2d80d"></a>
### Update site config

`operation_foundation_installer_business_behavior_update_site_configuration`

**Inputs** key, value, validate = true, site\_config\_path = no value.

**Local steps**

- Bind dependencies clear\_site\_config\_cache.
- Bind dependencies filelock.
- If not site\_config\_path.
  - Set site\_config\_path from get\_site\_config\_path().
- Set \_is\_global\_conf from “common\_site\_config” belongs to site\_config\_path.
- Within filelock(“site\_config”, is\_global = \_is\_global\_conf).
  - Evaluate \_update\_config\_file(key = key, value = value, config\_file = site\_config\_path).
  - Evaluate clear\_site\_config\_cache().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0246.json#L1213) · [Binding](../../../current-decisions/foundation/bindings-004.tsv#L1813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L551)
