# Site operations and diagnostics · operations 12

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Recorder

<a id="op-034cd6c2df3c0b"></a>
### Recorder.patch sql

`operation_foundation_recorder_business_behavior_recorder_patch_database_query`

**Inputs** self, db.

**Explicit results** no value.

**Local steps**

- If not self.config.record\_sql.
  - Return no value.
- Set Platform.db.\_sql from Platform.db.sql.
- Set Platform.db.sql from record\_sql.
- Evaluate self.patched\_databases.append(db).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L7288) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1697) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L375)

<a id="op-d4acf84e1ae9b9"></a>
### Recorder.unpatch sql

`operation_foundation_recorder_business_behavior_recorder_unpatch_database_query`

**Inputs** self.

**Local steps**

- For each db in self.patched\_databases.
  - Evaluate vars(db).pop(“sql”, no value).
  - Evaluate vars(db).pop(“\_sql”, no value).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L10) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1701) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L379)

<a id="op-3b3445a0b8a937"></a>
### Do not record

`operation_foundation_recorder_business_behavior_do_not_record`

**Inputs** function.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L7509) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1666) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L351)

<a id="op-e74cda1139c86f"></a>
### Do not record.wrapper

`operation_foundation_recorder_business_behavior_do_not_record_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(function).

**Explicit results** function(expanded args, expanded names kwargs).

**Local steps**

- If hasattr(Platform.local, “\_recorder”).
  - Evaluate Platform.local.\_recorder.cleanup().
  - Remove Platform.local.\_recorder.
- Return function(expanded args, expanded names kwargs).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L7692) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1667) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L352)

<a id="op-2c9028609cc3d5"></a>
### Administrator only

`operation_foundation_recorder_business_behavior_administrator_only`

**Inputs** function.

**Explicit results** wrapper.

**Local steps**

- Bind local operation wrapper for subsequent calls.
- Return wrapper.

[Applicable decision contract](../../../foundation-decision-contracts/part-0325.json#L7851) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1663) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L348)

<a id="op-fa6119493c0dac"></a>
### Administrator only.wrapper

`operation_foundation_recorder_business_behavior_administrator_only_wrapper`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(function).

**Explicit results** function(expanded args, expanded names kwargs).

**Explicit failure paths** validation helper — translated “Only Administrator is allowed to use Recorder”.

**Local steps**

- If Platform.session.user differs from “Administrator”.
  - Call the validation error handler Platform.throw(translated “Only Administrator is allowed to use Recorder”).
- Return function(expanded args, expanded names kwargs).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1664) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L349)

<a id="op-5fb983e7b6abbb"></a>
### Status

`operation_foundation_recorder_business_behavior_status`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**Explicit results** bool(Platform.cache.get\_value(RECORDER\_INTERCEPT\_FLAG)).

**Local steps**

- Return bool(Platform.cache.get\_value(RECORDER\_INTERCEPT\_FLAG)).

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L162) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1704) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L381)

<a id="op-33d277517e44e4"></a>
### Start

`operation_foundation_recorder_business_behavior_start`

**Inputs** record\_jobs = true, record\_requests = true, record\_sql = true, profile = false, capture\_stack = true, capture\_doc\_events = true, explain = true, request\_filter = “/”, jobs\_filter = empty text, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**Local steps**

- Evaluate RecorderConfig(record\_requests = int(record\_requests), record\_jobs = int(record\_jobs), record\_sql = int(record\_sql), profile = int(profile), …).store().
- Evaluate Platform.client\_cache.set\_value(RECORDER\_INTERCEPT\_FLAG, true).
- Evaluate Platform.cache.expire\_key(RECORDER\_INTERCEPT\_FLAG, RECORDER\_AUTO\_DISABLE).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L262) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1703) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L380)

<a id="op-281dfc345e7550"></a>
### Stop

`operation_foundation_recorder_business_behavior_stop`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**State and service calls** enqueue with post\_process.

**Local steps**

- Evaluate Platform.client\_cache.set\_value(RECORDER\_INTERCEPT\_FLAG, false).
- Evaluate Platform.enqueue(post\_process, now = Platform.in\_test).

If control reaches the end, it returns no value.

**Values supplied outside this operation** service or queued work from Platform.enqueue(post\_process, now = Platform.in\_test).

**Boundaries to resolve** stored data, late-bound calls, external or queued work, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L714) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1705) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L382)

<a id="op-1f1e01da2a62cf"></a>
### Get

`operation_foundation_recorder_business_behavior_get`

**Inputs** uuid = no value, remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**Explicit results** result.

**Local steps**

- If uuid.
  - Set result from Platform.cache.hget(RECORDER\_REQUEST\_HASH, uuid).
- Otherwise.
  - Set result from list(Platform.cache.hgetall(RECORDER\_REQUEST\_SPARSE\_HASH).values()).
- Return result.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L843) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1670) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L355)

<a id="op-844584fb2dc27e"></a>
### Export data

`operation_foundation_recorder_business_behavior_export_data`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**Explicit results** list(Platform.cache.hgetall(RECORDER\_REQUEST\_HASH).values()).

**Local steps**

- Return list(Platform.cache.hgetall(RECORDER\_REQUEST\_HASH).values()).

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L1038) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1669) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L354)

<a id="op-e4be6d77898b18"></a>
### Delete

`operation_foundation_recorder_business_behavior_delete`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**Local steps**

- Evaluate Platform.cache.delete\_value(RECORDER\_REQUEST\_SPARSE\_HASH).
- Evaluate Platform.cache.delete\_value(RECORDER\_REQUEST\_HASH).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L1149) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1665) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L350)

<a id="op-199a08d8029748"></a>
### Record queries

`operation_foundation_recorder_business_behavior_record_queries`

**Inputs** func.

**Explicit results** wrapped.

**Local steps**

- Bind local operation wrapped for subsequent calls.
- Return wrapped.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L1263) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1687) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L366)

<a id="op-6714ccf2540fb0"></a>
### Record queries.wrapped

`operation_foundation_recorder_business_behavior_record_queries_wrapped`

**Inputs** remaining positional values args, remaining named values kwargs.

**Wrappers, in declaration order** functools.wraps(func).

**Explicit results** ret.

**Local steps**

- Set recorder from record(force = true).
- Set recorder.path from formatted text Function call: {func.\_\_module\_\_}.{func.\_\_qualname\_\_}.
- Set ret from func(expanded args, expanded names kwargs).
- Evaluate dump().
- Evaluate recorder.\_unpatch\_sql().
- Evaluate post\_process().
- Evaluate print(“Recorded queries, open recorder to view them.”).
- Return ret.

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L1550) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1688) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L367)

<a id="op-da0752b2c63308"></a>
### Import data

`operation_foundation_recorder_business_behavior_import_data`

**Inputs** file.

**Wrappers, in declaration order** Platform.whitelist(), do\_not\_record, administrator\_only.

**Declared result** no value.

**Record and data access** resolve a document from “File” via get\_doc.

**Local steps**

- Set file\_doc from Platform.get\_doc(“File”, mapping(“file\_url” → file)).
- Set file\_content from json.loads(file\_doc.get\_content()).
- For each request in file\_content.
  - Evaluate Platform.cache.hset(RECORDER\_REQUEST\_SPARSE\_HASH, request at “uuid”, request).
  - Evaluate Platform.cache.hset(RECORDER\_REQUEST\_HASH, request at “uuid”, request).
- Evaluate file\_doc.delete(delete\_permanently = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** stored data, late-bound calls, callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0326.json#L1808) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1675) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L357)

## Service · Redis utils

<a id="op-a8d1fa8bc3abe5"></a>
### Create rq users

`operation_foundation_commands_shared_cache_utils_business_behavior_create_background_queue_users`

**Inputs** set\_admin\_password = false, use\_rq\_auth = false.

**Wrappers, in declaration order** click.command(“create-rq-users”), click.option(“--set-admin-password”, is\_flag = true, default = false, help = “Set new Redis admin(default user) password”), click.option(“--use-rq-auth”, is\_flag = true, default = false, help = “Enable Redis authentication for sites”).

**Local steps**

- Bind dependencies update\_site\_config.
- Bind dependencies RedisQueue.
- Set acl\_file\_path from os.path.abspath(“../config/redis\_queue.acl”).
- Set tuple(acl\_list, user\_credentials) from RedisQueue.gen\_acl\_list(set\_admin\_password = set\_admin\_password).
- Within open(acl\_file\_path, “w”) bound as f.
  - Evaluate f.writelines(list of (acl + whitespace '\\n') for acl drawn from acl\_list).
    - Draw acl from acl\_list.
- Set sites\_path from os.getcwd().
- Set common\_site\_config\_path from os.path.join(sites\_path, “common\_site\_config.json”).
- Evaluate update\_site\_config(“rq\_username”, user\_credentials at “bench” at 0, validate = false, site\_config\_path = common\_site\_config\_path).
- Evaluate update\_site\_config(“rq\_password”, user\_credentials at “bench” at 1, validate = false, site\_config\_path = common\_site\_config\_path).
- Evaluate update\_site\_config(“use\_rq\_auth”, use\_rq\_auth, validate = false, site\_config\_path = common\_site\_config\_path).
- Evaluate click.secho(“\* ACL and site configs are updated with new user credentials. Please restart Redis Queue server to enable na …”, fg = “green”).
- If set\_admin\_password.
  - Set env\_key from “RQ\_ADMIN\_PASWORD”.
  - Evaluate click.secho(“\* Redis admin password is successfully set up. Include below line in .bashrc file for system to use”, fg = “green”).
  - Evaluate click.secho(formatted text ′export {env\_key}={user\_credentials at “default” at 1}′).
  - Evaluate click.secho(“NOTE: Please save the admin password as you can not access redis server without the password”, fg = “yellow”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0021.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L515) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L597)

## Service · Result

<a id="op-b4784ea124d379"></a>
### Test Result.initialize

`operation_foundation_testing_result_business_behavior_test_result_initialize`

**Inputs** self, stream, descriptions, verbosity.

**Local steps**

- Evaluate super().\_\_init\_\_(stream, descriptions, verbosity).
- Set self.\_old\_stdout from list().
- Set self.\_old\_stderr from list().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L48) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1955) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L629)

<a id="op-68e7c16e6085f1"></a>
### Test Result.setup Stdout

`operation_foundation_testing_result_business_behavior_test_result_setup_stdout`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L7193) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1959) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L633)

<a id="op-60e61afd76298f"></a>
### Test Result.restore Stdout

`operation_foundation_testing_result_business_behavior_test_result_restore_stdout`

**Inputs** self.

**Local steps**

- Take no action here.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L7226) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L632)

<a id="op-b1650d713c0fc2"></a>
### Test Result.start Test Run

`operation_foundation_testing_result_business_behavior_test_result_start_test_run`

**Inputs** self.

**Local steps**

- If not sys.warnoptions.
  - Bind dependencies warnings.
  - Bind dependencies PlatformDeprecationWarning.
  - Evaluate warnings.simplefilter(“ignore”).
  - Evaluate warnings.filterwarnings(“module”, category = PlatformDeprecationWarning).
- If self.buffer.
  - Evaluate self.\_old\_stderr.append(sys.stderr).
  - Evaluate self.\_old\_stdout.append(sys.stdout).
  - Set self.\_module\_or\_class\_stdout\_capture from io.StringIO().
  - Set self.\_module\_or\_class\_stderr\_capture from io.StringIO().
  - Set sys.stdout from self.\_module\_or\_class\_stdout\_capture.
  - Set sys.stderr from self.\_module\_or\_class\_stderr\_capture.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0334.json#L7259) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1961) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L635)

<a id="op-f1472066f97d6c"></a>
### Test Result.stop Test Run

`operation_foundation_testing_result_business_behavior_test_result_stop_test_run`

**Inputs** self.

**Local steps**

- If self.buffer.
  - Set sys.stdout from self.\_old\_stdout.pop().
  - Set sys.stderr from self.\_old\_stderr.pop().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L6) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L637)

<a id="op-9b7ef46ae6aa62"></a>
### Test Result.start Test

`operation_foundation_testing_result_business_behavior_test_result_start_test`

**Inputs** self, test.

**Local steps**

- Set self.tb\_locals from true.
- Set self.\_started\_at from time.monotonic().
- Evaluate super(unittest.TextTestResult, self).startTest(test).
- Set test\_class from unittest.util.strclass(test.\_\_class\_\_).
- If getattr(self, “current\_test\_class”, no value) differs from test\_class.
  - Set self.current\_test\_class from test\_class.
  - Evaluate self.stream.write(formatted text  {test\_class} ).
  - Evaluate logger.info(formatted text {test\_class}).
  - If hasattr(self, “\_module\_or\_class\_stdout\_capture”).
    - For each line in self.\_module\_or\_class\_stdout\_capture.getvalue().splitlines().
      - Evaluate self.stream.write(click.style(formatted text   ▹ {line} , fg = “bright\_black”)).
      - Evaluate self.stream.flush().
    - Evaluate self.\_module\_or\_class\_stdout\_capture.seek(0).
    - Evaluate self.\_module\_or\_class\_stdout\_capture.truncate().
  - If hasattr(self, “\_module\_or\_class\_stderr\_capture”).
    - For each line in self.\_module\_or\_class\_stderr\_capture.getvalue().splitlines().
      - Evaluate self.stream.write(click.style(formatted text   ▸ {line} , fg = “bright\_black”)).
      - Evaluate self.stream.flush().
    - Evaluate self.\_module\_or\_class\_stderr\_capture.seek(0).
    - Evaluate self.\_module\_or\_class\_stderr\_capture.truncate().
  - If new\_doctypes bound to getattr(test.\_\_class\_\_, “\_newly\_created\_test\_records”, no value).
    - Set records from list of formatted text {name} ({qty}) for tuple(name, qty) drawn from reversed(new\_doctypes).
      - Draw tuple(name, qty) from reversed(new\_doctypes).
    - Set hint from click.style(formatted text   Test Records created: {“, ”.join(records)}, fg = “bright\_black”).
    - Evaluate self.stream.write((hint + whitespace '\\n')).
    - Evaluate logger.info(formatted text records created: {“, ”.join(records)}).
  - Evaluate self.stream.flush().
- If self.buffer.
  - Evaluate self.\_old\_stderr.append(sys.stderr).
  - Evaluate self.\_old\_stdout.append(sys.stdout).
  - Set self.\_test\_stdout\_capture from io.StringIO().
  - Set self.\_test\_stderr\_capture from io.StringIO().
  - Set sys.stdout from self.\_test\_stdout\_capture.
  - Set sys.stderr from self.\_test\_stderr\_capture.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic() · selected callable from getattr(self, “current\_test\_class”, no value), getattr(test.\_\_class\_\_, “\_newly\_created\_test\_records”, no value).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L115) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1960) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L634)

<a id="op-777f205fb4ae9e"></a>
### Test Result.stop Test

`operation_foundation_testing_result_business_behavior_test_result_stop_test`

**Inputs** self, test.

**Local steps**

- Evaluate super().stopTest(test).
- If self.buffer.
  - Set sys.stdout from self.\_old\_stderr.pop().
  - Set sys.stderr from self.\_old\_stdout.pop().
  - For each line in self.\_test\_stdout\_capture.getvalue().splitlines().
    - Evaluate self.stream.write(formatted text        ▹  {line} ).
    - Evaluate self.stream.flush().
  - For each line in self.\_test\_stderr\_capture.getvalue().splitlines().
    - Evaluate self.stream.write(formatted text        ▸  {line} ).
    - Evaluate self.stream.flush().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L1307) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L636)

<a id="op-9c5006ff9ac8a6"></a>
### Test Result.get Test Method Name

`operation_foundation_testing_result_business_behavior_test_result_get_test_method_name`

**Inputs** self, test.

**Explicit results** test.\_testMethodName when hasattr(test, “\_testMethodName”), otherwise str(test).

**Local steps**

- Return test.\_testMethodName when hasattr(test, “\_testMethodName”), otherwise str(test).
  - Value choice on hasattr(test, “\_testMethodName”) — true gives test.\_testMethodName, false gives str(test).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L1670) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L628)
