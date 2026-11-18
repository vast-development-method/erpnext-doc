# Site operations and diagnostics · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Loader

<a id="op-5d6d4fb8a6f4b1"></a>
### Platform Test Loader.load testsuites in pymodule

`operation_foundation_testing_loader_business_behavior_foundation_test_loader_load_testsuites_in_pymodule`

**Inputs** self, file\_modules.

**Local steps**

- For each module in file\_modules.
  - Set suite from self.loadTestsFromModule(module).
  - Evaluate self.recursive\_load\_suites\_in\_pymodule(suite).

If control reaches the end, it returns no value.

**Methods declared on this owner** [recursive load suites in pymodule](operations-007.md#op-fe92ff8c090474).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L5864) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1937) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L611)

<a id="op-6ad3a9c78bfd65"></a>
### Platform Test Loader.load pymodule for files

`operation_foundation_testing_loader_business_behavior_foundation_test_loader_load_pymodule_for_files`

**Inputs** self, files.

**Explicit results** \_file\_modules.

**Local steps**

- Set \_file\_modules from list().
- For each tuple(app\_path, test\_file) in files.
  - Set module\_name from formatted text {“.”.join(test\_file.relative\_to(app\_path.parent).parent.parts)}.{test\_file.stem}.
  - Set module from importlib.import\_module(module\_name).
  - Evaluate \_file\_modules.append(module).
- Return \_file\_modules.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L5972) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1936) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L610)

<a id="op-934018428e562e"></a>
### Platform Test Loader.get files

`operation_foundation_testing_loader_business_behavior_foundation_test_loader_get_files`

**Inputs** self, apps.

**Declared result** list.

**Explicit results** files.

**Local steps**

- Set files from list().
- For each app in apps.
  - Set app\_path from Path(Platform.get\_app\_path(app)).
  - For each test\_file in app\_path.glob(“\*\*/test\_\*.py”).
    - Evaluate files.append(tuple(app\_path, test\_file)).
- Return files.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L6203) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1935) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L609)

<a id="op-625448d83d9b21"></a>
### Platform Test Loader.discover tests

`operation_foundation_testing_loader_business_behavior_foundation_test_loader_discover_tests`

**Inputs** self, params.

**Declared result** unittest.TestSuite.

**Record and data access** read “DocType” via get\_cached\_value · read “Module Def” via get\_cached\_value.

**Explicit results** self.testsuite.

**Local steps**

- Set self.params from params.
- Set self.testsuite from unittest.TestSuite().
- If self.params.tests.
  - Set files from self.get\_files(Platform.get\_installed\_apps()).
  - Set file\_pymodules from self.load\_pymodule\_for\_files(files).
  - Evaluate self.load\_testsuites\_in\_pymodule(file\_pymodules).
- Otherwise.
  - If self.params.doctype.
    - Set module from Platform.get\_cached\_value(“DocType”, self.params.doctype, “module”).
    - Set app from Platform.get\_cached\_value(“Module Def”, module, “app\_name”).
    - Set pymodule\_name from get\_module\_name(self.params.doctype, module, “test\_”, app = app).
    - Set pymodule from importlib.import\_module(pymodule\_name).
    - Evaluate self.load\_testsuites\_in\_pymodule(list(pymodule)).
  - Otherwise.
    - If self.params.app.
      - Set files from self.get\_files(list(self.params.app)).
      - Set file\_pymodules from self.load\_pymodule\_for\_files(files).
      - Evaluate self.load\_testsuites\_in\_pymodule(file\_pymodules).
    - Otherwise.
      - If self.params.module.
        - Set pymodule from importlib.import\_module(self.params.module).
        - Evaluate self.load\_testsuites\_in\_pymodule(list(pymodule)).
- Return self.testsuite.

**Methods declared on this owner** [get files](operations-008.md#op-934018428e562e), [load pymodule for files](operations-008.md#op-6ad3a9c78bfd65), [load testsuites in pymodule](operations-008.md#op-5d6d4fb8a6f4b1).

**Values supplied outside this operation** configured or stored value from Platform.get\_cached\_value(“DocType”, self.params.doctype, “module”), Platform.get\_cached\_value(“Module Def”, module, “app\_name”).

**Boundaries to resolve** stored data, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L46) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1934) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L608)

## Service · Migrate

<a id="op-2a2170460a8d5f"></a>
### Atomic

`operation_foundation_migrate_business_behavior_atomic`

**Inputs** method.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L4503) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L200) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L896)

<a id="op-756880c524599c"></a>
### Atomic.wrapper

`operation_foundation_migrate_business_behavior_atomic_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(method).

**State and service calls** commit · rollback.

**Explicit results** ret.

**Explicit failure paths** e.

**Local steps**

- Attempt the following.
  - Set ret from method(expanded args, expanded names kwargs).
  - Evaluate Platform.db.commit().
  - Return ret.
- On failure (Exception) bound to e.
  - Within contextlib.suppress(Exception).
    - Evaluate Platform.db.rollback().
  - Raise e.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L4735) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L201) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L897)

<a id="op-76fd6c611f8b5b"></a>
### Site Migration.initialize

`operation_foundation_migrate_business_behavior_site_migration_initialize`

**Inputs** self, skip\_failing = false, skip\_search\_index = false, skip\_fixtures = false.

**Declared result** no value.

**Local steps**

- Set self.skip\_failing from skip\_failing.
- Set self.skip\_search\_index from skip\_search\_index.
- Set self.skip\_fixtures from skip\_fixtures.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L4943) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L205) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L901)

<a id="op-87cf629715e5b7"></a>
### Site Migration.set Up

`operation_foundation_migrate_business_behavior_site_migration_set_up`

**Inputs** self.

**Local steps**

- Set Platform.flags.touched\_tables from set().
- Set self.touched\_tables\_file from Platform.get\_site\_path(“touched\_tables.json”).
- Evaluate Platform.clear\_cache().
- Evaluate Platform.setup\_module\_map(include\_all\_apps = false).
- If os.path.exists(self.touched\_tables\_file).
  - Evaluate os.remove(self.touched\_tables\_file).
- Evaluate self.lower\_lock\_timeout().
- Within contextlib.suppress(Exception).
  - Evaluate self.kill\_idle\_connections().
- Set Platform.flags.in\_migrate from true.

If control reaches the end, it returns no value.

**Methods declared on this owner** [lower lock timeout](operations-008.md#op-67819376e703be), [kill idle connections](operations-008.md#op-d5af29bea05ad8).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L67) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L213) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L909)

<a id="op-bb2382c7c3c459"></a>
### Site Migration.tear Down

`operation_foundation_migrate_business_behavior_site_migration_tear_down`

**Inputs** self.

**State and service calls** enqueue with build\_index\_for\_all\_routes · publish realtime with “version-update”.

**Local steps**

- Evaluate self.db\_monitor.stop().
- Evaluate Platform.translate.clear\_cache().
- Evaluate clear\_website\_cache().
- Evaluate clear\_notifications().
- Within open(self.touched\_tables\_file, “w”) bound as f.
  - Evaluate json.dump(list(Platform.flags.touched\_tables), f, sort\_keys = true, indent = 4).
- If not self.skip\_search\_index.
  - Evaluate print(formatted text Queued rebuilding of search index for {Platform.local.site}).
  - Evaluate Platform.enqueue(build\_index\_for\_all\_routes, queue = “long”).
- Evaluate Platform.publish\_realtime(“version-update”).
- Evaluate Platform.flags.touched\_tables.clear().
- Set Platform.flags.in\_migrate from false.

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(build\_index\_for\_all\_routes, queue = “long”), Platform.publish\_realtime(“version-update”).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L68) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L214) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L910)

<a id="op-7850d0fb03e2dc"></a>
### Site Migration.pre schema updates

`operation_foundation_migrate_business_behavior_site_migration_previous_schema_updates`

**Inputs** self.

**Wrappers, in declaration order** atomic.

**Local steps**

- Bind dependencies sync\_module\_defs.
- If added bound to sync\_module\_defs().
  - Evaluate print(formatted text Registered new modules: {comma\_and(added, add\_quotes = false)}).
- Set overrides from defaultdict(list).
- For each app in Platform.get\_installed\_apps().
  - For each fn in Platform.get\_hooks(“before\_migrate”, app\_name = app).
    - Evaluate Platform.get\_attr(fn)().
  - For each doctype in Platform.get\_hooks(“override\_doctype\_class”, mapping(), app\_name = app).keys().
    - Evaluate overrides at doctype.append(app).
- For each tuple(doctype, app\_names) in overrides.items().
  - If len(app\_names) &gt; 1.
    - Evaluate click.secho(formatted text The controller for {doctype} is overridden by multiple apps: {comma\_and(app\_names, add\_quotes = false)}., fg = “yellow”).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“before\_migrate”, app\_name = app), Platform.get\_attr(fn) and 1 further calls.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L5730) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L209) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L905)

<a id="op-f03dbfb8dcb989"></a>
### Site Migration.run schema updates

`operation_foundation_migrate_business_behavior_site_migration_run_schema_updates`

**Inputs** self.

**Wrappers, in declaration order** atomic.

**Local steps**

- Evaluate Platform.modules.patch\_handler.run\_all(skip\_failing = self.skip\_failing, patch\_type = PatchType.pre\_model\_sync).
- Evaluate Platform.model.sync.sync\_all().
- Evaluate Platform.modules.patch\_handler.run\_all(skip\_failing = self.skip\_failing, patch\_type = PatchType.post\_model\_sync).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L6229) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L212) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L908)

<a id="op-136b3350022dab"></a>
### Site Migration.post schema updates

`operation_foundation_migrate_business_behavior_site_migration_post_schema_updates`

**Inputs** self.

**Wrappers, in declaration order** atomic.

**Record and data access** read “Portal Settings” via get\_single · read “Installed Applications” via get\_single.

**Local steps**

- Evaluate print(“Syncing jobs...”).
- Evaluate sync\_jobs().
- Bind dependencies create\_missing\_sequences.
- If recreated bound to create\_missing\_sequences().
  - Evaluate print(formatted text Recreated missing sequences for: {“, ”.join(recreated)}).
- If not self.skip\_fixtures.
  - Evaluate print(“Syncing fixtures...”).
  - Evaluate sync\_fixtures().
- Otherwise.
  - Evaluate print(“Skipping fixtures...”).
- Evaluate sync\_standard\_items().
- Evaluate print(“Syncing dashboards...”).
- Evaluate sync\_dashboards().
- Evaluate print(“Syncing customizations...”).
- Evaluate sync\_customizations().
- Evaluate print(“Syncing languages...”).
- Evaluate sync\_languages().
- Evaluate print(“Flushing deferred inserts...”).
- Evaluate flush\_deferred\_inserts().
- Evaluate print(“Removing orphan doctypes...”).
- Evaluate Platform.model.sync.remove\_orphan\_doctypes().
- Evaluate Platform.model.sync.remove\_orphan\_entities().
- Evaluate Platform.model.sync.delete\_duplicate\_icons().
- Evaluate print(“Syncing portal menu...”).
- Evaluate Platform.get\_single(“Portal Settings”).sync\_menu().
- Evaluate print(“Updating installed applications...”).
- Evaluate Platform.get\_single(“Installed Applications”).update\_versions().
- Evaluate print(“Executing ′after\_migrate′ hooks...”).
- For each app in Platform.get\_installed\_apps().
  - For each fn in Platform.get\_hooks(“after\_migrate”, app\_name = app).
    - Evaluate Platform.get\_attr(fn)().

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“after\_migrate”, app\_name = app), Platform.get\_attr(fn).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0015.json#L66) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L208) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L904)

<a id="op-5c136734156902"></a>
### Site Migration.required services running

`operation_foundation_migrate_business_behavior_site_migration_required_services_running`

**Inputs** self.

**Declared result** bool.

**Explicit results** are\_services\_running.

**Local steps**

- Set service\_status from check\_connection(redis\_services = list(“redis\_cache”)).
- Set are\_services\_running from all(service\_status.values()).
- If not are\_services\_running.
  - For each service in service\_status.
    - If not service\_status.get(service, true).
      - Evaluate print(formatted text Service {service} is not running.).
  - Evaluate print(BENCH\_START\_MESSAGE).
- Return are\_services\_running.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L7222) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L210) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L906)

<a id="op-67819376e703be"></a>
### Site Migration.lower lock timeout

`operation_foundation_migrate_business_behavior_site_migration_lower_dependency_lock_timeout`

**Inputs** self.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- If Platform.db.db\_type differs from “mariadb”.
  - Return no value.
- Evaluate Platform.db.sql(“set session lock\_wait\_timeout = %s”, (5 × 60)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0263.json#L7457) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L207) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L903)

<a id="op-d5af29bea05ad8"></a>
### Site Migration.kill idle connections

`operation_foundation_migrate_business_behavior_site_migration_kill_idle_connections`

**Inputs** self, idle\_limit = 30.

**State and service calls** execute a supplied database query.

**Explicit results** no value.

**Local steps**

- If Platform.db.db\_type differs from “mariadb”.
  - Return no value.
- Set processes from Platform.db.sql(“show full processlist”, as\_dict = 1).
- Set connection\_id from Platform.db.sql(“select connection\_id()”) at 0 at 0.
- For each process in processes.
  - Set sleeping from process.get(“Command”) equals “Sleep”.
  - Set user from str(process.get(“User”)).lower().
  - Set sleeping\_since from (cint(process.get(“Time”)) or 0).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(process.get(“Time”)) → 0.
  - Set pid from process.get(“Id”).
  - If (pid and pid differs from connection\_id and process.db equals Platform.conf.db\_name and sleeping and sleeping\_since &gt; idle\_limit and user differs from “system user”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in pid → pid differs from connection\_id → process.db equals Platform.conf.db\_name → sleeping → sleeping\_since &gt; idle\_limit → user differs from “system user”.
    - Attempt the following.
      - Evaluate Platform.db.sql(formatted text kill {pid}).
      - Evaluate print(formatted text Killed inactive database connection with PID {pid}).
    - On failure (Exception) bound to e.
      - Evaluate print(formatted text Failed to kill inactive database connection with PID {pid}: {e}).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L206) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L902)

<a id="op-65495a959bf081"></a>
### Site Migration.run

`operation_foundation_migrate_business_behavior_site_migration_run`

**Inputs** self, site.

**Explicit failure paths** SystemExit(1).

**Local steps**

- Bind dependencies filelock.
- If site.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
- Set self.db\_monitor from DBQueryProgressMonitor().
- If not self.required\_services\_running().
  - Raise SystemExit(1).
- Within filelock(“bench\_migrate”, timeout = 1).
  - Evaluate self.setUp().
  - Attempt the following.
    - Evaluate self.pre\_schema\_updates().
    - Evaluate self.run\_schema\_updates().
    - Evaluate self.post\_schema\_updates().
  - On exit, including pending return or failure.
    - Evaluate self.tearDown().
    - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Methods declared on this owner** [required services running](operations-008.md#op-5c136734156902), [set Up](operations-008.md#op-87cf629715e5b7), [pre schema updates](operations-008.md#op-7850d0fb03e2dc), [run schema updates](operations-008.md#op-f03dbfb8dcb989), [post schema updates](operations-008.md#op-136b3350022dab), [tear Down](operations-008.md#op-bb2382c7c3c459).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L608) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L211) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L907)

<a id="op-3f52ab32f3cdd0"></a>
### DBQuery Progress Monitor.initialize

`operation_foundation_migrate_business_behavior_database_query_progress_monitor_initialize`

**Inputs** self.

**Declared result** no value.

**State and service calls** execute a supplied database query.

**Local steps**

- Evaluate super().\_\_init\_\_().
- Set self.site from Platform.local.site.
- Set self.daemon from true.
- Set self.\_running from threading.Event().
- If Platform.db.db\_type equals “mariadb”.
  - Set self.conn\_id from Platform.db.sql(“select connection\_id()”) at 0 at 0.
  - Evaluate self.start().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L955) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L202) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L898)

<a id="op-212c8628ef4eb4"></a>
### DBQuery Progress Monitor.run

`operation_foundation_migrate_business_behavior_database_query_progress_monitor_run`

**Inputs** self.

**Record and data access** execute query text (SELECT).

**Explicit results** no value.

**Local steps**

- If self.\_running.is\_set().
  - Return no value.
- Evaluate self.\_running.set().
- Evaluate Platform.init(self.site).
- Evaluate Platform.connect().
- While self.\_running.is\_set().
  - Evaluate time.sleep(self.POLL\_DURATION).
  - Set queries from Platform.db.sql(query text (SELECT), self.conn\_id, as\_dict = true).
  - If not queries.
    - Continue with the next iteration or loop test.
  - Set query from Platform.\_dict(queries at 0).
  - Set time\_taken from query.TIME.
  - If (not time\_taken or time\_taken &lt; 5).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not time\_taken → time\_taken &lt; 5.
    - Continue with the next iteration or loop test.
  - Set msg from list().
  - Set command from (query.COMMAND or empty text).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.COMMAND → empty text.
  - Evaluate msg.append(formatted text Command: {command}).
  - Evaluate msg.append(formatted text Time: {time\_taken}s).
  - Evaluate msg.append(formatted text State: {(query.STATE or “N/A”)}).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.STATE → “N/A”.
  - If query.PROGRESS.
    - Evaluate msg.append(formatted text Progress: {query.PROGRESS}%).
  - If (command and command equals “Query”).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in command → command equals “Query”.
    - Set sql\_query from (query.INFO or empty text).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in query.INFO → empty text.
    - Set sql\_query from sql\_query.replace(whitespace '\\r', empty text).replace(whitespace '\\n', one space).replace(whitespace '\\t', one space).
    - If len(sql\_query) &gt; 100.
      - Set sql\_query from ((sql\_query at slice no value to 40 + “ ... ”) + sql\_query at slice negative 20 to no value).
    - Evaluate msg.append(formatted text Query: {sql\_query}).
  - Set msg from (whitespace '\\r' + “ \| ”.join(msg)).
  - If self.\_running.is\_set().
    - Evaluate print(msg, end = empty text, flush = true).
- Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L1180) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L203) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L899)

<a id="op-c1cfcc755d0d41"></a>
### DBQuery Progress Monitor.stop

`operation_foundation_migrate_business_behavior_database_query_progress_monitor_stop`

**Inputs** self.

**Local steps**

- Evaluate print(empty text).
- Evaluate self.\_running.clear().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0264.json#L2172) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L204) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L900)

## Service · Monitor

<a id="op-d3e302ab7ea9fa"></a>
### Start

`operation_foundation_monitor_business_behavior_start`

**Inputs** transaction\_type = “request”, method = no value, kwargs = no value.

**Local steps**

- If Platform.conf.monitor.
  - Set Platform.local.monitor from Monitor(transaction\_type, method, kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L2787) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1438)

<a id="op-d7170553233a66"></a>
### Stop

`operation_foundation_monitor_business_behavior_stop`

**Inputs** response = no value.

**Local steps**

- If hasattr(Platform.local, “monitor”).
  - Evaluate Platform.local.monitor.dump(response).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L2901) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1439)

<a id="op-0aefc43f0beb7e"></a>
### Add data to monitor

`operation_foundation_monitor_business_behavior_add_data_to_monitor`

**Inputs** remaining named values kwargs.

**Declared result** no value.

**Local steps**

- If hasattr(Platform.local, “monitor”).
  - Evaluate Platform.local.monitor.add\_custom\_data(expanded names kwargs).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L2996) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L853) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1428)

<a id="op-8039c78ee6ec5a"></a>
### Get trace id

`operation_foundation_monitor_business_behavior_get_trace_identifier`

**Inputs** no declared parameters.

**Declared result** (str bitwise or no value).

**Explicit results** monitor.data.uuid.

**Local steps**

- If monitor bound to getattr(Platform.local, “monitor”, no value).
  - Return monitor.data.uuid.

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from getattr(Platform.local, “monitor”, no value).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L3090) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L855) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1430)

<a id="op-e24a26912a2928"></a>
### Log file

`operation_foundation_monitor_business_behavior_log_file`

**Inputs** no declared parameters.

**Explicit results** os.path.join(Platform.utils.get\_bench\_path(), “logs”, “monitor.json.log”).

**Local steps**

- Return os.path.join(Platform.utils.get\_bench\_path(), “logs”, “monitor.json.log”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0297.json#L3178) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L856) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1431)
