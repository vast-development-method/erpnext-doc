# Site operations and diagnostics · operations 14

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Runner

<a id="op-931bb81402f338"></a>
### Test Runner.profile

`operation_foundation_testing_runner_business_behavior_test_runner_profile`

**Inputs** self.

**Wrappers, in declaration order** contextlib.contextmanager.

**Local steps**

- If self.cfg.profile.
  - Evaluate logger.debug(“profiling enabled”).
  - Set pr from cProfile.Profile().
  - Evaluate pr.enable().
- yield no value.
- If self.cfg.profile.
  - Evaluate pr.disable().
  - Set s from StringIO().
  - Set ps from pstats.Stats(pr, stream = s).sort\_stats(“cumulative”).
  - Evaluate ps.print\_stats().
  - Evaluate print(s.getvalue()).

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L6918) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L646)

<a id="op-2c39d2ee9105c2"></a>
### Test Runner.iterate suite

`operation_foundation_testing_runner_business_behavior_test_runner_iterate_suite`

**Inputs** suite.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- For each test in suite.
  - If isinstance(test, unittest.TestSuite).
    - yield values from TestRunner.\_iterate\_suite(test).
  - Otherwise.
    - If isinstance(test, unittest.TestCase).
      - yield test.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L7209) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L644)

## Service · Scheduler

<a id="op-4aab023a793680"></a>
### Trigger scheduler event

`operation_foundation_commands_scheduler_business_behavior_trigger_scheduler_event`

**Inputs** context, event.

**Wrappers, in declaration order** click.command(“trigger-scheduler-event”, help = “Trigger a scheduler event”), click.argument(“event”), pass\_context.

**Record and data access** resolve a document from “Scheduled Job Type” via get\_doc.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.utils.scheduler.
- Set exit\_code from 0.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Attempt the following.
      - Evaluate Platform.get\_doc(“Scheduled Job Type”, mapping(“method” → event)).execute().
    - On failure (Platform.DoesNotExistError).
      - Evaluate click.secho(formatted text Event {event} does not exist!, fg = “red”).
      - Set exit\_code from 1.
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.
- Evaluate sys.exit(exit\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L756) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L514) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L596)

<a id="op-13aecbf2b71bb2"></a>
### Enable scheduler

`operation_foundation_commands_scheduler_business_behavior_enable_scheduler`

**Inputs** context.

**Wrappers, in declaration order** click.command(“enable-scheduler”), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.utils.scheduler.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.utils.scheduler.enable\_scheduler().
    - Evaluate Platform.db.commit().
    - Evaluate print(“Enabled for”, site).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L1173) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L505) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L587)

<a id="op-2984d2e9d25b5e"></a>
### Disable scheduler

`operation_foundation_commands_scheduler_business_behavior_disable_scheduler`

**Inputs** context.

**Wrappers, in declaration order** click.command(“disable-scheduler”), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies Platform.utils.scheduler.
- For each site in context.sites.
  - Attempt the following.
    - Evaluate Platform.init(site).
    - Evaluate Platform.connect().
    - Evaluate Platform.utils.scheduler.disable\_scheduler().
    - Evaluate Platform.db.commit().
    - Evaluate print(“Disabled for”, site).
  - On exit, including pending return or failure.
    - Evaluate Platform.destroy().
- If not context.sites.
  - Raise SiteNotSpecifiedError.

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L1433) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L503) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L585)

<a id="op-3fc25c465b1ed4"></a>
### Scheduler

`operation_foundation_commands_scheduler_business_behavior_scheduler`

**Inputs** context, state, format, verbose = false, site = no value.

**Wrappers, in declaration order** click.command(“scheduler”), click.option(“--site”, help = “site name”), click.argument(“state”, type = click.Choice(list(“pause”, “resume”, “disable”, “enable”, …))), click.option(“--format”, “-f”, default = “text”, type = click.Choice(list(“json”, “text”)), help = “Output format”), click.option(“--verbose”, “-v”, is\_flag = true, help = “Verbose output”), pass\_context.

**State and service calls** commit.

**Explicit results** print(output at format.format(status = status, site = site)).

**Local steps**

- Bind dependencies Platform.
- Bind dependencies is\_scheduler\_inactive, toggle\_scheduler.
- Set site from (site or get\_site(context)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → get\_site(context).
- Set output from mapping(“text” → “Scheduler is {status} for site {site}”, “json” → “{{"status": "{status}", "site": "{site}"}}”).
- Within Platform.init\_site(site = site).
  - Select the first matching pattern against state.
    - Pattern “status”.
      - Evaluate Platform.connect().
      - Set status from “disabled” when is\_scheduler\_inactive(verbose = verbose), otherwise “enabled”.
        - Value choice on is\_scheduler\_inactive(verbose = verbose) — true gives “disabled”, false gives “enabled”.
      - Return print(output at format.format(status = status, site = site)).
    - Pattern “pause” or “resume”.
      - Bind dependencies update\_site\_config.
      - Evaluate update\_site\_config(“pause\_scheduler”, state equals “pause”).
    - Pattern “enable” or “disable”.
      - Evaluate Platform.connect().
      - Evaluate toggle\_scheduler(state equals “enable”).
      - Evaluate Platform.db.commit().
  - Evaluate print(output at format.format(status = formatted text {state}d, site = site)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L1693) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L508) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L590)

<a id="op-eb28311bc7dc48"></a>
### Set maintenance mode

`operation_foundation_commands_scheduler_business_behavior_set_maintenance_mode`

**Inputs** context, state, site = no value.

**Wrappers, in declaration order** click.command(“set-maintenance-mode”), click.option(“--site”, help = “site name”), click.argument(“state”, type = click.Choice(list(“on”, “off”))), pass\_context.

**Local steps**

- Bind dependencies update\_site\_config.
- If not site.
  - Set site from get\_site(context).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate update\_site\_config(“maintenance\_mode”, 1 when state equals “on”, otherwise 0).
    - Value choice on state equals “on” — true gives 1, false gives 0.
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L2615) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L509) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L591)

<a id="op-4b4ac8fac33e83"></a>
### Doctor

`operation_foundation_commands_scheduler_business_behavior_doctor`

**Inputs** context, site = no value.

**Wrappers, in declaration order** click.command(“doctor”), click.option(“--site”, help = “site name”), pass\_context.

**Explicit results** \_doctor(site = site).

**Local steps**

- Bind dependencies \_doctor.
- If not site.
  - Set site from get\_site(context, raise\_err = false).
- Return \_doctor(site = site).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L2936) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L504) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L586)

<a id="op-dea8df9a4ed5e7"></a>
### Show pending jobs

`operation_foundation_commands_scheduler_business_behavior_show_pending_jobs`

**Inputs** context, site = no value.

**Wrappers, in declaration order** click.command(“show-pending-jobs”), click.option(“--site”, help = “site name”), pass\_context.

**Explicit results** pending\_jobs.

**Local steps**

- Bind dependencies \_pending\_jobs.
- If not site.
  - Set site from get\_site(context).
- Within Platform.init\_site(site).
  - Set pending\_jobs from \_pending\_jobs(site = site).
- Return pending\_jobs.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L3124) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L510) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L592)

<a id="op-65e1d987675602"></a>
### Purge jobs

`operation_foundation_commands_scheduler_business_behavior_purge_jobs`

**Inputs** site = no value, queue = no value, event = no value.

**Wrappers, in declaration order** click.command(“purge-jobs”), click.option(“--site”, help = “site name”), click.option(“--queue”, default = no value, help = “one of "low", "default", "high”), click.option(“--event”, default = no value, help = “one of "all", "weekly", "monthly", "hourly", "daily", "weekly\_long", "daily\_long"”).

**Local steps**

- Bind dependencies purge\_pending\_jobs.
- Evaluate Platform.init((site or empty text)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → empty text.
- Set count from purge\_pending\_jobs(event = event, site = site, queue = queue).
- Evaluate print(formatted text Purged {count} jobs).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L3347) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L506) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L588)

<a id="op-91a1edced5e345"></a>
### Start scheduler

`operation_foundation_commands_scheduler_business_behavior_start_scheduler`

**Inputs** no declared parameters.

**Wrappers, in declaration order** click.command(“schedule”).

**Local steps**

- Bind dependencies time.
- Bind dependencies start\_scheduler.
- Evaluate time.sleep(0.5).
- Evaluate start\_scheduler().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L3659) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L511) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L593)

<a id="op-9ea704ef89bb80"></a>
### Start worker

`operation_foundation_commands_scheduler_business_behavior_start_worker`

**Inputs** queue, quiet = false, rq\_username = no value, rq\_password = no value, burst = false, strategy = no value.

**Wrappers, in declaration order** click.command(“worker”), click.option(“--queue”, type = str, help = “Queue to consume from. Multiple queues can be specified using comma-separated string. If not specified all q …”), click.option(“--quiet”, is\_flag = true, default = false, help = “Hide Log Outputs”), click.option(“-u”, “--rq-username”, default = no value, help = “Redis ACL user”), click.option(“-p”, “--rq-password”, default = no value, help = “Redis ACL user password”), click.option(“--burst”, is\_flag = true, default = false, help = “Run Worker in Burst mode.”), click.option(“--strategy”, required = false, type = click.Choice(list(“round\_robin”, “random”)), help = “Dequeuing strategy to use”).

**Local steps**

- Bind dependencies start\_worker.
- Evaluate start\_worker(queue, quiet = quiet, rq\_username = rq\_username, rq\_password = rq\_password, burst = burst, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L3765) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L512) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L594)

<a id="op-e23ec54cb191a2"></a>
### Start worker pool

`operation_foundation_commands_scheduler_business_behavior_start_worker_pool`

**Inputs** queue, quiet = false, num\_workers = 2, burst = false.

**Wrappers, in declaration order** click.command(“worker-pool”), click.option(“--queue”, type = str, help = “Queue to consume from. Multiple queues can be specified using comma-separated string. If not specified all q …”), click.option(“--num-workers”, type = int, default = 2, help = “Number of workers to spawn in pool.”), click.option(“--quiet”, is\_flag = true, default = false, help = “Hide Log Outputs”), click.option(“--burst”, is\_flag = true, default = false, help = “Run Worker in Burst mode.”).

**Local steps**

- Bind dependencies start\_worker\_pool.
- Evaluate start\_worker\_pool(queue = queue, quiet = quiet, burst = burst, num\_workers = num\_workers).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L4231) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L513) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L595)

<a id="op-1b9c07f7cfc73c"></a>
### Ready for migration

`operation_foundation_commands_scheduler_business_behavior_ready_for_migration`

**Inputs** context, site = no value.

**Wrappers, in declaration order** click.command(“ready-for-migration”), click.option(“--site”, help = “site name”), pass\_context.

**Explicit results** 0.

**Local steps**

- Bind dependencies time.
- Bind dependencies any\_job\_pending.
- If not site.
  - Set site from get\_site(context).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Set pending\_jobs from false.
  - For each \_ in range(3).
    - Update pending\_jobs using bitwise or any\_job\_pending(site = site).
    - Evaluate time.sleep(1).
  - If pending\_jobs.
    - Evaluate print(formatted text NOT READY for migration: site {site} has pending background jobs).
    - Evaluate sys.exit(1).
  - Otherwise.
    - Evaluate print(formatted text READY for migration: site {site} does not have any background jobs).
    - Return 0.
- On exit, including pending return or failure.
  - Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L4557) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L507) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L589)

## Service · Site

<a id="op-4e278c29441eac"></a>
### New site

`operation_foundation_commands_site_business_behavior_new_site`

**Inputs** site, db\_root\_username = no value, db\_root\_password = no value, admin\_password = no value, verbose = false, source\_sql = no value, force = no value, no\_mariadb\_socket = false, mariadb\_user\_host\_login\_scope = false, install\_app = no value, db\_name = no value, db\_password = no value, db\_type = no value, db\_socket = no value, db\_host = no value, db\_port = no value, db\_user = no value, set\_default = false, setup\_db = true.

**Wrappers, in declaration order** click.command(“new-site”), click.argument(“site”), click.option(“--db-name”, help = “Database name”), click.option(“--db-password”, help = “Database password”), click.option(“--db-type”, default = “mariadb”, type = click.Choice(list(“mariadb”, “postgres”, “sqlite”)), help = “Optional "sqlite", "postgres" or "mariadb". Default is "mariadb"”), click.option(“--db-host”, help = “Database Host”), click.option(“--db-port”, type = int, help = “Database Port”), click.option(“--db-root-username”, “--mariadb-root-username”, help = “Root username for MariaDB or PostgreSQL, Default is "root"”), click.option(“--db-root-password”, “--mariadb-root-password”, help = “Root password for MariaDB or PostgreSQL”), click.option(“--db-socket”, “--mariadb-db-socket”, envvar = “MYSQL\_UNIX\_PORT”, help = “Database socket for MariaDB or folder containing database socket for PostgreSQL”), click.option(“--no-mariadb-socket”, is\_flag = true, default = false, help = “DEPRECATED: Set MariaDB host to % and use TCP/IP Socket instead of using the UNIX Socket”), click.option(“--mariadb-user-host-login-scope”, help = “Set the mariadb host for the user login scope if you don't want to use the current host as login scope which …”), click.option(“--admin-password”, help = “Administrator password for new site”, default = no value), click.option(“--verbose”, is\_flag = true, default = false, help = “Verbose”), click.option(“--force”, help = “Force restore if site/database already exists”, is\_flag = true, default = false), click.option(“--source-sql”, “--source\_sql”, help = “Initiate database with a SQL file”), click.option(“--install-app”, multiple = true, help = “Install app after installation”), click.option(“--set-default”, is\_flag = true, default = false, help = “Set the new site as default site”), click.option(“--setup-db/--no-setup-db”, default = true, help = “Create user and database in mariadb/postgres; only bootstrap if false”), click.option(“--db-user”, help = “Database user if you already have one”).

**Local steps**

- Bind dependencies \_new\_site.
- Evaluate Platform.init(site, new\_site = true).
- Set db\_labels from mapping(“postgres” → “PostgreSQL”, “sqlite” → “SQLite”).
- If db\_type belongs to db\_labels.
  - Evaluate click.secho(formatted text  Note: {db\_labels at db\_type} support is currently in development and considered experimental., fg = “yellow”, bold = true).
  - Evaluate click.secho(text in the contract, fg = “cyan”).
- If site belongs to Platform.get\_all\_apps().
  - Evaluate click.secho(formatted text Your bench has an app called {site}, please choose another name for the site., fg = “red”).
  - Evaluate sys.exit(1).
- If no\_mariadb\_socket.
  - Evaluate click.secho(“--no-mariadb-socket is DEPRECATED; use --mariadb-user-host-login-scope='%' (wildcard) or --mariadb-user-host …”, fg = “yellow”).
  - Set mariadb\_user\_host\_login\_scope from “%”.
- Set rollback\_callback from CallbackManager().
- Attempt the following.
  - Evaluate \_new\_site(db\_name, site, db\_root\_username = db\_root\_username, db\_root\_password = db\_root\_password, admin\_password = admin\_password, verbose = verbose, …).
  - If set\_default.
    - Evaluate use(site).
- On failure (Exception).
  - Evaluate traceback.print\_exc().
  - If (sys.\_\_stdin\_\_.isatty() and click.confirm(“Site creation failed, do you want to rollback the site?”, abort = true)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in sys.\_\_stdin\_\_.isatty() → click.confirm(“Site creation failed, do you want to rollback the site?”, abort = true).
    - Evaluate rollback\_callback.run().
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L126) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L542) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L621)

<a id="op-798f346c99477e"></a>
### Restore

`operation_foundation_commands_site_business_behavior_restore`

**Inputs** context, sql\_file\_path, encryption\_key = no value, db\_root\_username = no value, db\_root\_password = no value, db\_name = no value, verbose = no value, install\_app = no value, admin\_password = no value, force = no value, with\_public\_files = no value, with\_private\_files = no value.

**Wrappers, in declaration order** click.command(“restore”), click.argument(“sql-file-path”), click.option(“--db-root-username”, “--mariadb-root-username”, help = “Root username for MariaDB or PostgreSQL, Default is "root"”), click.option(“--db-root-password”, “--mariadb-root-password”, help = “Root password for MariaDB or PostgreSQL”), click.option(“--db-name”, help = “Database name for site in case it is a new one”), click.option(“--admin-password”, help = “Administrator password for new site”), click.option(“--install-app”, multiple = true, help = “Install app after installation”), click.option(“--with-public-files”, help = “Restores the public files of the site, given path to its tar file”), click.option(“--with-private-files”, help = “Restores the private files of the site, given path to its tar file”), click.option(“--force”, is\_flag = true, default = false, help = “Ignore the validations and downgrade warnings. This action is not recommended”), click.option(“--encryption-key”, help = “Backup encryption key”), pass\_context.

**Local steps**

- Bind dependencies filelock.
- Set site from get\_site(context).
- Evaluate Platform.init(site).
- Within filelock(“site\_restore”, timeout = 1).
  - Evaluate \_restore(site = site, sql\_file\_path = sql\_file\_path, encryption\_key = encryption\_key, db\_root\_username = db\_root\_username, …).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.verbose → verbose.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.force → force.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L128) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L550) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L629)

<a id="op-dcbd47ad9c6dca"></a>
### Restore

`operation_foundation_commands_site_business_behavior_restore_2`

**Inputs** site (named only, default no value), sql\_file\_path (named only, default no value), encryption\_key (named only, default no value), db\_root\_username (named only, default no value), db\_root\_password (named only, default no value), verbose (named only, default no value), install\_app (named only, default no value), admin\_password (named only, default no value), force (named only, default no value), with\_public\_files (named only, default no value), with\_private\_files (named only, default no value).

**Local steps**

- Bind dependencies Path.
- Bind dependencies extract\_files.
- Bind dependencies decrypt\_backup, get\_or\_generate\_backup\_encryption\_key.
- Set dirs from tuple(formatted text {site}/private/backups, “..”).
- If not Path(sql\_file\_path).exists().
  - Evaluate click.secho(formatted text File {sql\_file\_path} not found. Trying to check in alternative directories., fg = “yellow”).
  - For each dir in dirs.
    - Set potential\_path from (Path(dir) ÷ Path(sql\_file\_path)).
    - If potential\_path.exists().
      - Set sql\_file\_path from str(potential\_path.resolve()).
      - Evaluate click.secho(formatted text File {sql\_file\_path} found., fg = “green”).
      - Leave the innermost loop without its normal-exhaustion alternative.
  - After normal loop exhaustion.
    - Evaluate click.secho(formatted text File {sql\_file\_path} not found., fg = “red”).
    - Evaluate sys.exit(1).
- Set tuple(err, out) from Platform.utils.execute\_in\_shell(formatted text file {sql\_file\_path}, check\_exit\_code = true).
- If err.
  - Evaluate click.secho(“Failed to detect type of backup file”, fg = “red”).
  - Evaluate sys.exit(1).
- If “AES” belongs to nested operand in the contract().split(“:”) at negative 1.strip().
  - If encryption\_key.
    - Evaluate click.secho(“Encrypted backup file detected. Decrypting using provided key.”, fg = “yellow”).
  - Otherwise.
    - Evaluate click.secho(“Encrypted backup file detected. Decrypting using site config.”, fg = “yellow”).
    - Set encryption\_key from get\_or\_generate\_backup\_encryption\_key().
  - Within decrypt\_backup(sql\_file\_path, encryption\_key).
    - If not os.path.exists(sql\_file\_path).
      - Evaluate click.secho(“Decryption failed. Please provide a valid key and try again.”, fg = “red”).
      - Evaluate sys.exit(1).
    - Evaluate restore\_backup(sql\_file\_path, site, db\_root\_username, db\_root\_password, …).
- Otherwise.
  - Evaluate restore\_backup(sql\_file\_path, site, db\_root\_username, db\_root\_password, …).
- If with\_public\_files.
  - If encryption\_key.
    - Within decrypt\_backup(with\_public\_files, encryption\_key).
      - Set public from extract\_files(site, with\_public\_files).
  - Otherwise.
    - Set public from extract\_files(site, with\_public\_files).
  - Evaluate os.remove(public).
- If with\_private\_files.
  - If encryption\_key.
    - Within decrypt\_backup(with\_private\_files, encryption\_key).
      - Set private from extract\_files(site, with\_private\_files).
  - Otherwise.
    - Set private from extract\_files(site, with\_private\_files).
  - Evaluate os.remove(private).
- Set success\_message from “Site {} has been restored{}”.format(site, “ with files” when (with\_public\_files or with\_private\_files), otherwise empty text).
  - Value choice on (with\_public\_files or with\_private\_files) — true gives “ with files”, false gives empty text.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in with\_public\_files → with\_private\_files.
- Evaluate click.secho(success\_message, fg = “green”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L129) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L551) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L630)

<a id="op-fbcc4e310d387d"></a>
### Restore backup

`operation_foundation_commands_site_business_behavior_restore_backup`

**Inputs** sql\_file\_path, site, db\_root\_username, db\_root\_password, verbose, install\_app, admin\_password, force.

**Local steps**

- Bind dependencies Path.
- Bind dependencies \_new\_site, is\_downgrade, is\_partial, validate\_database\_sql.
- If is\_partial(sql\_file\_path).
  - Evaluate click.secho(“Partial Backup file detected. You cannot use a partial file to restore a Platform site.”, fg = “red”).
  - Evaluate click.secho(“Use ′bench partial-restore′ to restore a partial backup to an existing site.”, fg = “yellow”).
  - Evaluate sys.exit(1).
- If (is\_downgrade(sql\_file\_path, verbose = true) and not force).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in is\_downgrade(sql\_file\_path, verbose = true) → not force.
  - Set warn\_message from “This is not recommended and may lead to unexpected behaviour. Do you want to continue anyway?”.
  - Evaluate click.confirm(warn\_message, abort = true).
- Evaluate validate\_database\_sql(sql\_file\_path, \_raise = not force).
- Attempt the following.
  - Evaluate \_new\_site(Platform.conf.db\_name, site, db\_root\_username = db\_root\_username, db\_root\_password = db\_root\_password, admin\_password = admin\_password, verbose = verbose, …).
- On failure (Exception) bound to err.
  - Evaluate print(err).
  - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L1971) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L552) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L631)

<a id="op-e6fad20441ddc9"></a>
### Partial restore

`operation_foundation_commands_site_business_behavior_partial_restore`

**Inputs** context, sql\_file\_path, verbose, encryption\_key = no value.

**Wrappers, in declaration order** click.command(“partial-restore”), click.argument(“sql-file-path”), click.option(“--verbose”, “-v”, is\_flag = true), click.option(“--encryption-key”, help = “Backup encryption key”), pass\_context.

**Local steps**

- Bind dependencies is\_partial, partial\_restore.
- Bind dependencies decrypt\_backup, get\_or\_generate\_backup\_encryption\_key.
- If not os.path.exists(sql\_file\_path).
  - Evaluate print(“Invalid path”, sql\_file\_path).
  - Evaluate sys.exit(1).
- Set site from get\_site(context).
- Set verbose from (context.verbose or verbose).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in context.verbose → verbose.
- Evaluate Platform.init(site).
- Evaluate Platform.connect().
- If Platform.conf.db\_type equals “sqlite”.
  - Evaluate click.secho(“Partial restore is not supported for SQLite databases”, fg = “red”).
  - Evaluate sys.exit(1).
- Set tuple(err, out) from Platform.utils.execute\_in\_shell(formatted text file {sql\_file\_path}, check\_exit\_code = true).
- If err.
  - Evaluate click.secho(“Failed to detect type of backup file”, fg = “red”).
  - Evaluate sys.exit(1).
- If “cipher” belongs to nested operand in the contract().split(“:”) at negative 1.strip().
  - If encryption\_key.
    - Evaluate click.secho(“Encrypted backup file detected. Decrypting using provided key.”, fg = “yellow”).
    - Set key from encryption\_key.
  - Otherwise.
    - Evaluate click.secho(“Encrypted backup file detected. Decrypting using site config.”, fg = “yellow”).
    - Set key from get\_or\_generate\_backup\_encryption\_key().
  - Within decrypt\_backup(sql\_file\_path, key).
    - If not is\_partial(sql\_file\_path).
      - Evaluate click.secho(“Full backup file detected. Use ′bench restore′ to restore a Platform Site.”, fg = “red”).
      - Evaluate sys.exit(1).
    - Evaluate partial\_restore(sql\_file\_path, verbose).
  - If not os.path.exists(sql\_file\_path).
    - Evaluate click.secho(“Decryption failed. Please provide a valid key and try again.”, fg = “red”).
    - Evaluate sys.exit(1).
- Otherwise.
  - If not is\_partial(sql\_file\_path).
    - Evaluate click.secho(“Full backup file detected. Use ′bench restore′ to restore a Platform Site.”, fg = “red”).
    - Evaluate sys.exit(1).
  - Evaluate partial\_restore(sql\_file\_path, verbose).
- Evaluate Platform.destroy().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L127) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L543) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L622)

<a id="op-0c82e080cf1982"></a>
### Reinstall

`operation_foundation_commands_site_business_behavior_reinstall`

**Inputs** context, admin\_password = no value, db\_root\_username = no value, db\_root\_password = no value, yes = false.

**Wrappers, in declaration order** click.command(“reinstall”), click.option(“--admin-password”, help = “Administrator Password for reinstalled site”), click.option(“--db-root-username”, “--mariadb-root-username”, help = “Root username for MariaDB or PostgreSQL, Default is "root"”), click.option(“--db-root-password”, “--mariadb-root-password”, help = “Root password for MariaDB or PostgreSQL”), click.option(“--yes”, is\_flag = true, default = false, help = “Pass --yes to skip confirmation”), pass\_context.

**Local steps**

- Set site from get\_site(context).
- Evaluate \_reinstall(site, admin\_password, db\_root\_username, db\_root\_password, verbose = context.verbose, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L4016) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L545) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L624)

<a id="op-08af360d6c1286"></a>
### Reinstall

`operation_foundation_commands_site_business_behavior_reinstall_2`

**Inputs** site, admin\_password = no value, db\_root\_username = no value, db\_root\_password = no value, yes = false, verbose = false.

**Local steps**

- Bind dependencies \_new\_site.
- If not yes.
  - Evaluate click.confirm(“This will wipe your database. Are you sure you want to reinstall?”, abort = true).
- Attempt the following.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Evaluate Platform.clear\_cache().
  - Set installed from Platform.get\_installed\_apps().
  - Evaluate Platform.clear\_cache().
- On failure (Exception).
  - Set installed from list().
- On exit, including pending return or failure.
  - If Platform.db.
    - Evaluate Platform.db.close().
  - Evaluate Platform.destroy().
- Evaluate Platform.init(site).
- Evaluate \_new\_site(Platform.conf.db\_name, site, verbose = verbose, force = true, install\_apps = installed, db\_root\_username = db\_root\_username, …).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L4341) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L546) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L625)

<a id="op-710446978ea9c1"></a>
### Install app

`operation_foundation_commands_site_business_behavior_install_application`

**Inputs** context, apps, force = false.

**Wrappers, in declaration order** click.command(“install-app”), click.argument(“apps”, nargs = negative 1), click.option(“--force”, is\_flag = true, default = false), pass\_context.

**State and service calls** commit.

**Explicit failure paths** SiteNotSpecifiedError.

**Local steps**

- Bind dependencies \_install\_app.
- Bind dependencies filelock.
- Set exit\_code from 0.
- If not context.sites.
  - Raise SiteNotSpecifiedError.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Within filelock(“install\_app”, timeout = 1).
    - For each app in apps.
      - Attempt the following.
        - Evaluate \_install\_app(app, verbose = context.verbose, force = force).
      - On failure (Platform.IncompatibleApp) bound to err.
        - Set err\_msg from formatted text : {err} when str(err), otherwise empty text.
          - Value choice on str(err) — true gives formatted text : {err}, false gives empty text.
        - Evaluate print(formatted text App {app} is Incompatible with Site {site}{err\_msg}).
        - Set exit\_code from 1.
      - On failure (Exception) bound to err.
        - Set err\_msg from formatted text : {err} {Platform.get\_traceback(with\_context = true)}.
        - Evaluate print(formatted text An error occurred while installing {app}{err\_msg}).
        - Set exit\_code from 1.
    - If not exit\_code.
      - Evaluate Platform.db.commit().
  - Evaluate Platform.destroy().
- Evaluate sys.exit(exit\_code).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0022.json#L4786) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L536) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L615)

<a id="op-32793c07b96add"></a>
### List apps

`operation_foundation_commands_site_business_behavior_list_apps`

**Inputs** context, format.

**Wrappers, in declaration order** click.command(“list-apps”), click.option(“--format”, “-f”, type = click.Choice(list(“text”, “json”)), default = “text”), pass\_context.

**Record and data access** read “Installed Applications” via get\_single.

**Local steps**

- Set summary\_dict from mapping().
- Bind local operation format\_app for subsequent calls.
- For each site in context.sites.
  - Evaluate Platform.init(site).
  - Evaluate Platform.connect().
  - Set site\_title from click.style(formatted text {site}, fg = “green”) when len(context.sites) &gt; 1, otherwise empty text.
    - Value choice on len(context.sites) &gt; 1 — true gives click.style(formatted text {site}, fg = “green”), false gives empty text.
  - Set installed\_apps\_info from list().
  - Set apps from Platform.get\_single(“Installed Applications”).installed\_applications.
  - If apps.
    - Evaluate installed\_apps\_info.extend(generator of format\_app(app) for app drawn from apps).
      - Draw app from apps.
  - Otherwise.
    - Evaluate installed\_apps\_info.extend(Platform.get\_installed\_apps()).
  - Set installed\_apps\_info\_str from whitespace '\\n'.join(installed\_apps\_info).
  - Set summary from formatted text {site\_title} {installed\_apps\_info\_str}.
  - Set summary\_dict at site from list of app.app\_name for app drawn from apps.
    - Draw app from apps.
  - If (format equals “text” and installed\_apps\_info and summary).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in format equals “text” → installed\_apps\_info → summary.
    - Evaluate print(summary).
  - Evaluate Platform.destroy().
- If format equals “json”.
  - Evaluate click.echo(Platform.as\_json(summary\_dict)).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L124) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L537) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L616)

<a id="op-dc5ff1ce8a6298"></a>
### List apps.format app

`operation_foundation_commands_site_business_behavior_list_apps_format_application`

**Inputs** app.

**Explicit results** template.format(app.app\_name, app.app\_version, app.git\_branch).

**Local steps**

- Set name\_len from max(generator of len(app.app\_name) for app drawn from apps).
  - Draw app from apps.
- Set ver\_len from max(generator of len(app.app\_version) for app drawn from apps).
  - Draw app from apps.
- Set template from formatted text {0:{name\_len}} {1:{ver\_len}} {2}.
- Return template.format(app.app\_name, app.app\_version, app.git\_branch).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L125) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L538) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L617)
