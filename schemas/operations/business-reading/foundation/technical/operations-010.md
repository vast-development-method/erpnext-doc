# Site operations and diagnostics · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Parallel test runner

<a id="op-a842e3d3b733e8"></a>
### Parallel Test Runner.setup test file list

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_setup_test_file_list`

**Inputs** self.

**Local steps**

- Set self.test\_file\_list from self.get\_test\_file\_list().
- Set self.total\_test\_weight from sum(generator of self.get\_test\_weight(test) for test drawn from self.test\_file\_list).
  - Draw test from self.test\_file\_list.

If control reaches the end, it returns no value.

**Methods declared on this owner** [get test file list](operations-010.md#op-42071e3bbf2fd9), [get test weight](operations-010.md#op-7496ca1f08dc90).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L1064) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L885) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1460)

<a id="op-bde15359a06a99"></a>
### Parallel Test Runner.run tests

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_run_tests`

**Inputs** self.

**Local steps**

- Set self.test\_result from TestResult(stream = sys.stderr, descriptions = true, verbosity = 2).
- For each test\_file\_info in self.test\_file\_list.
  - Evaluate self.run\_tests\_for\_file(test\_file\_info).

If control reaches the end, it returns no value.

**Methods declared on this owner** [run tests for file](operations-010.md#op-307ef625099219).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L37) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L882) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1457)

<a id="op-307ef625099219"></a>
### Parallel Test Runner.run tests for file

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_run_tests_for_file`

**Inputs** self, file\_info.

**Explicit results** no value.

**Local steps**

- If not file\_info.
  - Return no value.
- If self.dry\_run.
  - Evaluate print(“running tests from”, “/”.join(file\_info)).
  - Return no value.
- If Platform.session.user differs from “Administrator”.
  - Bind dependencies deprecation\_warning.
  - Evaluate record a compatibility advisory for the invoked interface.
  - Evaluate Platform.set\_user(“Administrator”).
- Set tuple(path, filename) from file\_info.
- Set module from self.get\_module(path, filename).
- If not self.lightmode.
  - Bind dependencies compat\_preload\_test\_records\_upfront.
  - Evaluate compat\_preload\_test\_records\_upfront(list(tuple(module, path, filename))).
- Set test\_suite from unittest.TestSuite().
- Set module\_test\_cases from unittest.TestLoader().loadTestsFromModule(module).
- Evaluate test\_suite.addTest(module\_test\_cases).
- Evaluate self.test\_result.startTestRun().
- Evaluate test\_suite(self.test\_result).
- Evaluate self.test\_result.stopTestRun().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get module](operations-010.md#op-339e2f534251aa).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L1340) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L883) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1458)

<a id="op-339e2f534251aa"></a>
### Parallel Test Runner.get module

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_get_module`

**Inputs** self, path, filename.

**Explicit results** Platform.get\_module(module\_name).

**Local steps**

- Set app\_path from Platform.get\_app\_path(self.app).
- Set relative\_path from os.path.relpath(path, app\_path).
- If relative\_path equals “.”.
  - Set module\_name from self.app.
- Otherwise.
  - Set relative\_path from relative\_path.replace(“/”, “.”).
  - Set module\_name from os.path.splitext(filename) at 0.
  - Set module\_name from formatted text {self.app}.{relative\_path}.{module\_name}.
- Return Platform.get\_module(module\_name).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L1826) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L877) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1452)

<a id="op-73591ee3afe4a3"></a>
### Parallel Test Runner.print result

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_print_result`

**Inputs** self.

**Local steps**

- Evaluate signal.alarm(60).
- Evaluate faulthandler.register(signal.SIGALRM).
- Evaluate self.test\_result.printErrors().
- Evaluate click.echo(self.test\_result).
- If (self.test\_result.failures or self.test\_result.errors).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in self.test\_result.failures → self.test\_result.errors.
  - If os.environ.get(“CI”).
    - Evaluate sys.exit(1).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L2142) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L881) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1456)

<a id="op-42071e3bbf2fd9"></a>
### Parallel Test Runner.get test file list

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_get_test_file_list`

**Inputs** self.

**Explicit results** test\_chunks at (self.build\_number − 1).

**Local steps**

- Set test\_list from get\_all\_tests(self.app).
- Set test\_counts from list of self.get\_test\_weight(test) for test drawn from test\_list.
  - Draw test from test\_list.
- Set test\_chunks from split\_by\_weight(test\_list, test\_counts, chunk\_count = self.total\_builds).
- Return test\_chunks at (self.build\_number − 1).

**Methods declared on this owner** [get test weight](operations-010.md#op-7496ca1f08dc90).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L2361) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L878) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1453)

<a id="op-7496ca1f08dc90"></a>
### Parallel Test Runner.get test weight

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_runner_get_test_weight`

**Inputs** test.

**Wrappers, in declaration order** staticmethod.

**Explicit results** test\_count.

**Local steps**

- Set file\_name from “/”.join(test).
- Set test\_weight from (TEST\_WEIGHT\_OVERRIDES.get(test at negative 1) or 1).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in TEST\_WEIGHT\_OVERRIDES.get(test at negative 1) → 1.
- Within open(file\_name) bound as f.
  - Set test\_count from (f.read().count(“def test\_”) × test\_weight).
- Return test\_count.

**Boundaries to resolve** late-bound calls, callee failures, file state, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L2546) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L879) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1454)

<a id="op-8aed1597e05077"></a>
### Split by weight

`operation_foundation_parallel_test_runner_business_behavior_split_by_weight`

**Inputs** work, weights, chunk\_count.

**Explicit results** chunks.

**Local steps**

- Set expected\_weight from (sum(weights) floor divide chunk\_count).
- Set chunks from list of list() for \_ drawn from range(chunk\_count).
  - Draw \_ from range(chunk\_count).
- Set chunk\_no from 0.
- Set chunk\_weight from 0.
- For each tuple(task, weight) in zip(work, weights, strict = false).
  - If chunk\_weight &gt; expected\_weight.
    - Set chunk\_weight from 0.
    - Update chunk\_no using + 1.
    - Require chunk\_no &lt; chunk\_count or raise an assertion failure.
  - Evaluate chunks at chunk\_no.append(task).
  - Update chunk\_weight using + weight.
- Require len(work) equals sum(generator of len(chunk) for chunk drawn from chunks) or raise an assertion failure.
  - Draw chunk from chunks.
- Require len(chunks) equals chunk\_count or raise an assertion failure.
- Return chunks.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L2746) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L894) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1469)

<a id="op-6a30a1f0653ba3"></a>
### Get all tests

`operation_foundation_parallel_test_runner_business_behavior_get_all_tests`

**Inputs** app.

**Explicit results** test\_file\_list.

**Local steps**

- Set test\_file\_list from list().
- For each tuple(path, folders, files) in os.walk(Platform.get\_app\_path(app)).
  - For each dontwalk in tuple(“node\_modules”, “locals”, “.git”, “public”, …).
    - If dontwalk belongs to folders.
      - Evaluate folders.remove(dontwalk).
  - Evaluate folders.sort().
  - Evaluate files.sort().
  - If os.path.sep.join(list(“doctype”, “doctype”, “boilerplate”)) belongs to path.
    - Continue with the next iteration or loop test.
  - Evaluate test\_file\_list.extend(generator of list(path, filename) for filename drawn from files where (filename.startswith(“test\_”) and filename.endswith(“.py”) and filename differs from “test\_runner.py”)).
    - Draw filename from files, keep a combination only if ((filename.startswith(“test\_”) and filename.endswith(“.py”) and filename differs from “test\_runner.py”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in filename.startswith(“test\_”) → filename.endswith(“.py”) → filename differs from “test\_runner.py”.
- Return test\_file\_list.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L3171) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L875) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1450)

<a id="op-c343850dfd3560"></a>
### Parallel Test With Orchestrator.initialize

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_initialize`

**Inputs** self, app, site.

**Local steps**

- Set self.orchestrator\_url from os.environ.get(“ORCHESTRATOR\_URL”).
- If not self.orchestrator\_url.
  - Evaluate click.echo(“ORCHESTRATOR\_URL environment variable not found!”).
  - Evaluate click.echo(text in the contract).
  - Evaluate sys.exit(1).
- Set self.ci\_build\_id from os.environ.get(“CI\_BUILD\_ID”).
- Set self.ci\_instance\_id from (os.environ.get(“CI\_INSTANCE\_ID”) or Platform.generate\_hash(length = 10)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.environ.get(“CI\_INSTANCE\_ID”) → Platform.generate\_hash(length = 10).
- If not self.ci\_build\_id.
  - Evaluate click.echo(“CI\_BUILD\_ID environment variable not found!”).
  - Evaluate sys.exit(1).
- Evaluate ParallelTestRunner.\_\_init\_\_(self, app, site).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from Platform.generate\_hash(length = 10).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L3589) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L890) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1465)

<a id="op-5880cd1cd7d457"></a>
### Parallel Test With Orchestrator.run tests

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_run_tests`

**Inputs** self.

**Local steps**

- Set self.test\_status from “ongoing”.
- Evaluate self.register\_instance().
- Evaluate super().run\_tests().

If control reaches the end, it returns no value.

**Methods declared on this owner** [register instance](operations-010.md#op-e0fdf716fc8ff5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L3969) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L893) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1468)

<a id="op-e306e0fd05c4c1"></a>
### Parallel Test With Orchestrator.get test file list

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_get_test_file_list`

**Inputs** self.

**Local steps**

- While self.test\_status equals “ongoing”.
  - yield self.get\_next\_test().

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [get next test](operations-010.md#op-0bd15847db0c7e).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L4063) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L889) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1464)

<a id="op-e0fdf716fc8ff5"></a>
### Parallel Test With Orchestrator.register instance

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_register_instance`

**Inputs** self.

**Local steps**

- Set test\_spec\_list from get\_all\_tests(self.app).
- Set response\_data from self.call\_orchestrator(“register-instance”, data = mapping(“test\_spec\_list” → test\_spec\_list)).
- Set self.is\_master from response\_data.get(“is\_master”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [call orchestrator](operations-010.md#op-a698f9ed664b67).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L4143) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L892) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1467)

<a id="op-0bd15847db0c7e"></a>
### Parallel Test With Orchestrator.get next test

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_get_next_test`

**Inputs** self.

**Explicit results** response\_data.get(“next\_test”).

**Local steps**

- Set response\_data from self.call\_orchestrator(“get-next-test-spec”).
- Set self.test\_status from response\_data.get(“status”).
- Return response\_data.get(“next\_test”).

**Methods declared on this owner** [call orchestrator](operations-010.md#op-a698f9ed664b67).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L4295) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L888) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1463)

<a id="op-718c8043bdd7ef"></a>
### Parallel Test With Orchestrator.print result

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_print_result`

**Inputs** self.

**Explicit results** super().print\_result().

**Local steps**

- Evaluate self.call\_orchestrator(“test-completed”).
- Return super().print\_result().

**Methods declared on this owner** [call orchestrator](operations-010.md#op-a698f9ed664b67).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L4418) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L891) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1466)

<a id="op-a698f9ed664b67"></a>
### Parallel Test With Orchestrator.call orchestrator

`operation_foundation_parallel_test_runner_business_behavior_parallel_test_with_orchestrator_call_orchestrator`

**Inputs** self, endpoint, data = no value.

**Explicit results** response\_data.

**Local steps**

- If data is identical to no value.
  - Set data from mapping().
- Set headers from mapping(“CI-BUILD-ID” → self.ci\_build\_id, “CI-INSTANCE-ID” → self.ci\_instance\_id, “REPO-TOKEN” → “2948288382838DE”).
- Set url from formatted text {self.orchestrator\_url}/{endpoint}.
- Set res from requests.get(url, json = data, headers = headers).
- Evaluate res.raise\_for\_status().
- Set response\_data from mapping().
- If “application/json” belongs to res.headers.get(“content-type”).
  - Set response\_data from res.json().
- Return response\_data.

**Values supplied outside this operation** service or queued work from requests.get(url, json = data, headers = headers).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0299.json#L4500) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L887) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1462)

## Service · Patch handler

<a id="op-404769aeb952a0"></a>
### Run all

`operation_foundation_modules_patch_handler_business_behavior_run_all`

**Inputs** skip\_failing = false, patch\_type = no value.

**Declared result** no value.

**Record and data access** read “Patch Log” via get\_all.

**Local steps**

- Set executed from set(Platform.get\_all(“Patch Log”, filters = mapping(“skipped” → 0), fields = “patch”, pluck = “patch”)).
- Set never\_skip from set(Platform.get\_hooks(“never\_skip\_patches”)).
- Set Platform.flags.final\_patches from list().
- Bind local operation run\_patch for subsequent calls.
- Set patches from get\_all\_patches(patch\_type = patch\_type).
- For each patch in patches.
  - If (patch and patch does not belong to executed).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in patch → patch does not belong to executed.
    - Evaluate run\_patch(patch).
- For each patch in Platform.flags.final\_patches.
  - Set patch from patch.replace(“finally:”, empty text).
  - Evaluate run\_patch(patch).

If control reaches the end, it returns no value.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(“never\_skip\_patches”).

**Boundaries to resolve** stored data, late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L25) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L820) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1401)

<a id="op-d2345d6c281d0e"></a>
### Run all.run patch

`operation_foundation_modules_patch_handler_business_behavior_run_all_run_patch`

**Inputs** patch.

**Explicit failure paths** PatchError(patch) · propagate active failure.

**Local steps**

- Attempt the following.
  - If not run\_single(patchmodule = patch).
    - Evaluate print((patch + “: failed: STOPPED”)).
    - Raise PatchError(patch).
- On failure (Exception).
  - If not skip\_failing.
    - Propagate the active failure.
  - If should\_never\_skip(patch, never\_skip).
    - Evaluate print((patch + “: failed: patch cannot be skipped: STOPPED”)).
    - Propagate the active failure.
  - Evaluate print(“Failed to execute patch”).
  - Evaluate update\_patch\_log(patch, skipped = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L26) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L821) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1402)

<a id="op-b7ff7c3d9f5bb7"></a>
### Get all patches

`operation_foundation_modules_patch_handler_business_behavior_get_all_patches`

**Inputs** patch\_type = no value.

**Declared result** list at str.

**Explicit results** patches.

**Explicit failure paths** validation helper — formatted text Unsupported patch type specified: {patch\_type}.

**Local steps**

- If (patch\_type and not isinstance(patch\_type, PatchType)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in patch\_type → not isinstance(patch\_type, PatchType).
  - Call the validation error handler Platform.throw(formatted text Unsupported patch type specified: {patch\_type}).
- Set patches from list().
- For each app in Platform.get\_installed\_apps().
  - Evaluate patches.extend(get\_patches\_from\_app(app, patch\_type = patch\_type)).
- Return patches.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L2373) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L815) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1396)

<a id="op-27a4a958e00738"></a>
### Get patches from app

`operation_foundation_modules_patch_handler_business_behavior_get_patches_from_application`

**Inputs** app, patch\_type = no value.

**Declared result** list at str.

**Explicit results** parse\_as\_configfile(patches\_file, patch\_type) · Platform.get\_file\_items(patches\_file) · list().

**Local steps**

- Set patches\_file from Platform.get\_app\_path(app, “patches.txt”).
- Attempt the following.
  - Return parse\_as\_configfile(patches\_file, patch\_type).
- On failure (configparser.MissingSectionHeaderError).
  - If (not patch\_type or patch\_type equals PatchType.pre\_model\_sync).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not patch\_type → patch\_type equals PatchType.pre\_model\_sync.
    - Return Platform.get\_file\_items(patches\_file).
- Return list().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L2608) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L816) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1397)

<a id="op-a36a954293fc73"></a>
### Parse as configfile

`operation_foundation_modules_patch_handler_business_behavior_parse_as_configfile`

**Inputs** patches\_file, patch\_type = no value.

**Declared result** list at str.

**Explicit results** list() · (list of patch for patch drawn from parser at PatchType.pre\_model\_sync.value + list of patch for patch drawn from parser at PatchType.post\_model\_sync.value) · list of patch for patch drawn from parser at patch\_type.value.

**Explicit failure paths** validation helper — Platform.\_(“Patch type {} not found in patches.txt”).format(patch\_type).

**Local steps**

- Set parser from configparser.ConfigParser(allow\_no\_value = true, delimiters = whitespace '\\n').
- Set parser.optionxform from str.
- Evaluate parser.read(patches\_file).
- If not parser.sections().
  - Return list().
- If not patch\_type.
  - Return (list of patch for patch drawn from parser at PatchType.pre\_model\_sync.value + list of patch for patch drawn from parser at PatchType.post\_model\_sync.value).
    - Draw patch from parser at PatchType.pre\_model\_sync.value.
    - Draw patch from parser at PatchType.post\_model\_sync.value.
- If patch\_type.value belongs to parser.sections().
  - Return list of patch for patch drawn from parser at patch\_type.value.
    - Draw patch from parser at patch\_type.value.
- Otherwise.
  - Call the validation error handler Platform.throw(Platform.\_(“Patch type {} not found in patches.txt”).format(patch\_type)).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0016.json#L24) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L817) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1398)

<a id="op-79ffd2de8b5e54"></a>
### Reload doc

`operation_foundation_modules_patch_handler_business_behavior_reload_record`

**Inputs** args.

**Local steps**

- Bind dependencies Platform.modules.
- Evaluate run\_single(method = Platform.modules.reload\_doc, methodargs = args).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L3417) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L819) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1400)

<a id="op-31977cb286b214"></a>
### Run single

`operation_foundation_modules_patch_handler_business_behavior_run_single`

**Inputs** patchmodule = no value, method = no value, methodargs = no value, force = false.

**Explicit results** execute\_patch(patchmodule, method, methodargs) · true.

**Local steps**

- Bind dependencies conf.
- Set conf.developer\_mode from 0.
- If (force or method or not executed(patchmodule)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in force → method → not executed(patchmodule).
  - Return execute\_patch(patchmodule, method, methodargs).
- Otherwise.
  - Return true.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L3503) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L822) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1403)

<a id="op-fc384e0aa0902a"></a>
### Execute patch

`operation_foundation_modules_patch_handler_business_behavior_execute_patch`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** patchmodule, method, methodargs.

**Explicit result forms** Boolean true.

**Locally raised failures** active or constructed exception.

**Observed service boundaries** transaction control.

**Local structure** 6 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0295.json#L3674) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L813) · [Declaration location](../../../current-decisions/foundation/evidence/locations-005.tsv#L1394)
