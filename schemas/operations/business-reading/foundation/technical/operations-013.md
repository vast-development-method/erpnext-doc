# Site operations and diagnostics · operations 13

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Result

<a id="op-9ba68ba23fa52d"></a>
### Test Result.add Success

`operation_foundation_testing_result_business_behavior_test_result_add_success`

**Inputs** self, test.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addSuccess(test).
- Set elapsed from (time.monotonic() − self.\_started\_at).
- Set threshold\_passed from elapsed ≥ SLOW\_TEST\_THRESHOLD.
- Set long\_elapsed from click.style(formatted text  ({elapsed}s), fg = “red”) when threshold\_passed, otherwise empty text.
  - Value choice on threshold\_passed — true gives click.style(formatted text  ({elapsed}s), fg = “red”), false gives empty text.
- Evaluate self.\_write\_result(test, “ ✔ ”, “green”, long\_elapsed).
- Evaluate logger.debug(formatted text {test} {“&#91;success&#93;”} ⌛{elapsed}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write result](operations-013.md#op-ac36607cd408a9).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L1758) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1952) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L626)

<a id="op-ac4877c37f1874"></a>
### Test Result.add Error

`operation_foundation_testing_result_business_behavior_test_result_add_error`

**Inputs** self, test, err.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addError(test, err).
- Evaluate self.\_write\_result(test, “ ✖ ”, “red”).
- Evaluate logger.debug(formatted text {test} {“&#91;error&#93;”}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write result](operations-013.md#op-ac36607cd408a9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L2091) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1948) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L622)

<a id="op-a56c5d926c5a19"></a>
### Test Result.add Failure

`operation_foundation_testing_result_business_behavior_test_result_add_failure`

**Inputs** self, test, err.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addFailure(test, err).
- Evaluate self.\_write\_result(test, “ ✖ ”, “red”).
- Evaluate logger.debug(formatted text {test} {“&#91;failure&#93;”}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write result](operations-013.md#op-ac36607cd408a9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L2279) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1950) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L624)

<a id="op-02a79fa31f1ac0"></a>
### Test Result.add Skip

`operation_foundation_testing_result_business_behavior_test_result_add_skip`

**Inputs** self, test, reason.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addSkip(test, reason).
- Evaluate self.\_write\_result(test, “ = ”, “white”).
- Evaluate logger.debug(formatted text {test} {“&#91;skipped&#93;”}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write result](operations-013.md#op-ac36607cd408a9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L2467) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1951) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L625)

<a id="op-f10af3507d9800"></a>
### Test Result.add Expected Failure

`operation_foundation_testing_result_business_behavior_test_result_add_expected_failure`

**Inputs** self, test, err.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addExpectedFailure(test, err).
- Evaluate self.stream.write(“x”).
- Evaluate self.\_write\_result(test, “✔ ”, “green”).
- Evaluate logger.debug(formatted text {test} {“&#91;expected failure&#93;”}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write result](operations-013.md#op-ac36607cd408a9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L2655) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1949) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L623)

<a id="op-7c12b82c665d8c"></a>
### Test Result.add Unexpected Success

`operation_foundation_testing_result_business_behavior_test_result_add_unexpected_success`

**Inputs** self, test.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addUnexpectedSuccess(test).
- Evaluate self.stream.write(“u”).
- Evaluate self.\_write\_result(test, “✖ ”, “red”).
- Evaluate logger.debug(formatted text {test} {“&#91;unexpected success&#93;”}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [write result](operations-013.md#op-ac36607cd408a9).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L2870) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1953) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L627)

<a id="op-469bbf1110a9ae"></a>
### Test Result.print Errors

`operation_foundation_testing_result_business_behavior_test_result_print_errors`

**Inputs** self.

**Local steps**

- Evaluate click.echo(whitespace '\\n').
- Evaluate self.printErrorList(“ ERROR ”, self.errors, “red”).
- Evaluate self.printErrorList(“ FAIL ”, self.failures, “red”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [print Error List](operations-013.md#op-72268719c777e4).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L3074) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L631)

<a id="op-72268719c777e4"></a>
### Test Result.print Error List

`operation_foundation_testing_result_business_behavior_test_result_print_error_list`

**Inputs** self, flavour, errors, color.

**Local steps**

- For each tuple(test, err) in errors.
  - Evaluate click.echo(self.separator1).
  - Evaluate click.echo(formatted text {click.style(flavour, bg = color)} {self.getDescription(test)}).
  - Evaluate click.echo(self.separator2).
  - Evaluate click.echo(err).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L3202) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L630)

<a id="op-a1f61a4dc58d61"></a>
### Test Result.str

`operation_foundation_testing_result_business_behavior_test_result_text`

**Inputs** self.

**Explicit results** formatted text Tests: {self.testsRun}, Failing: {len(self.failures)}, Errors: {len(self.errors)}.

**Local steps**

- Return formatted text Tests: {self.testsRun}, Failing: {len(self.failures)}, Errors: {len(self.errors)}.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L3444) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L638)

<a id="op-ac36607cd408a9"></a>
### Test Result.write result

`operation_foundation_testing_result_business_behavior_test_result_write_result`

**Inputs** self, test, status, color, suffix = empty text.

**Local steps**

- Set test\_method from self.getTestMethodName(test).
- Set result from formatted text    {click.style(status, fg = color)} {test\_method}.
- Update result using + formatted text  {suffix} when suffix, otherwise empty text.
  - Value choice on suffix — true gives formatted text  {suffix}, false gives empty text.
- Update result using + whitespace '\\n'.
- Evaluate self.stream.write(result).
- Evaluate self.stream.flush().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-012.md#op-9c5006ff9ac8a6).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L3563) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L639)

<a id="op-b8c6a551fcc01a"></a>
### Platform Test Result.initialize

`operation_foundation_testing_result_business_behavior_foundation_test_result_initialize`

**Inputs** self, stream, descriptions, verbosity.

**Local steps**

- Evaluate super().\_\_init\_\_(stream, descriptions, verbosity).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L3828) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1946) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L620)

<a id="op-fb5d2f1206bcb8"></a>
### Platform Test Result.start Test

`operation_foundation_testing_result_business_behavior_foundation_test_result_start_test`

**Inputs** self, test.

**Local steps**

- Set self.tb\_locals from true.
- Set self.\_started\_at from time.monotonic().
- Evaluate super(unittest.TextTestResult, self).startTest(test).
- Set test\_class from unittest.util.strclass(test.\_\_class\_\_).
- If (not hasattr(self, “current\_test\_class”) or self.current\_test\_class differs from test\_class).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not hasattr(self, “current\_test\_class”) → self.current\_test\_class differs from test\_class.
  - Evaluate click.echo(formatted text  {unittest.util.strclass(test.\_\_class\_\_)}).
  - Set self.current\_test\_class from test\_class.

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L3918) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1947) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L621)

<a id="op-448d005094bade"></a>
### Platform Test Result.get Test Method Name

`operation_foundation_testing_result_business_behavior_foundation_test_result_get_test_method_name`

**Inputs** self, test.

**Explicit results** test.\_testMethodName when hasattr(test, “\_testMethodName”), otherwise str(test).

**Local steps**

- Return test.\_testMethodName when hasattr(test, “\_testMethodName”), otherwise str(test).
  - Value choice on hasattr(test, “\_testMethodName”) — true gives test.\_testMethodName, false gives str(test).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L4216) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1945) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L619)

<a id="op-4e0f908f7e27a1"></a>
### Platform Test Result.add Success

`operation_foundation_testing_result_business_behavior_foundation_test_result_add_success`

**Inputs** self, test.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addSuccess(test).
- Set elapsed from (time.monotonic() − self.\_started\_at).
- Set threshold\_passed from elapsed ≥ SLOW\_TEST\_THRESHOLD.
- Set elapsed from click.style(formatted text  ({elapsed}s), fg = “red”) when threshold\_passed, otherwise empty text.
  - Value choice on threshold\_passed — true gives click.style(formatted text  ({elapsed}s), fg = “red”), false gives empty text.
- Evaluate click.echo(formatted text   {click.style(“ ✔ ”, fg = “green”)} {self.getTestMethodName(test)}{elapsed}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-013.md#op-448d005094bade).

**Values supplied outside this operation** clock or generated value from time.monotonic().

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L4304) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1943) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L617)

<a id="op-1474a5b07ea9dc"></a>
### Platform Test Result.add Error

`operation_foundation_testing_result_business_behavior_foundation_test_result_add_error`

**Inputs** self, test, err.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addError(test, err).
- Evaluate click.echo(formatted text   {click.style(“ ✖ ”, fg = “red”)} {self.getTestMethodName(test)}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-013.md#op-448d005094bade).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L4631) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1939) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L613)

<a id="op-6821614ebc908c"></a>
### Platform Test Result.add Failure

`operation_foundation_testing_result_business_behavior_foundation_test_result_add_failure`

**Inputs** self, test, err.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addFailure(test, err).
- Evaluate click.echo(formatted text   {click.style(“ ✖ ”, fg = “red”)} {self.getTestMethodName(test)}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-013.md#op-448d005094bade).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L4822) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1941) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L615)

<a id="op-8e1e6635149331"></a>
### Platform Test Result.add Skip

`operation_foundation_testing_result_business_behavior_foundation_test_result_add_skip`

**Inputs** self, test, reason.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addSkip(test, reason).
- Evaluate click.echo(formatted text   {click.style(“ = ”, fg = “white”)} {self.getTestMethodName(test)}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-013.md#op-448d005094bade).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L5013) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1942) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L616)

<a id="op-bb55b3be7000e3"></a>
### Platform Test Result.add Expected Failure

`operation_foundation_testing_result_business_behavior_foundation_test_result_add_expected_failure`

**Inputs** self, test, err.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addExpectedFailure(test, err).
- Evaluate click.echo(formatted text   {click.style(“ ✖ ”, fg = “red”)} {self.getTestMethodName(test)}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-013.md#op-448d005094bade).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L5204) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1940) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L614)

<a id="op-f6d9672c24fc49"></a>
### Platform Test Result.add Unexpected Success

`operation_foundation_testing_result_business_behavior_foundation_test_result_add_unexpected_success`

**Inputs** self, test.

**Local steps**

- Evaluate super(unittest.TextTestResult, self).addUnexpectedSuccess(test).
- Evaluate click.echo(formatted text   {click.style(“ ✔ ”, fg = “green”)} {self.getTestMethodName(test)}).

If control reaches the end, it returns no value.

**Methods declared on this owner** [get Test Method Name](operations-013.md#op-448d005094bade).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L5395) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L618)

## Service · Runner

<a id="op-17a6bbec25f64c"></a>
### Test Runner.initialize

`operation_foundation_testing_runner_business_behavior_test_runner_initialize`

**Inputs** self, stream = no value, descriptions = true, verbosity = 1, failfast = false, buffer = true, resultclass = no value, warnings = “module”, tb\_locals (named only, default false), cfg (named only).

**Local steps**

- Evaluate super().\_\_init\_\_(stream = stream, descriptions = descriptions, verbosity = verbosity, failfast = cfg.failfast, …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in resultclass → TestResult.
- Set self.cfg from cfg.
- Set self.per\_app\_categories from defaultdict(deferred anonymous expression).
- Set self.integration\_preparation from IntegrationTestPreparation(cfg).
- Evaluate logger.debug(“TestRunner initialized”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L49) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L642)

<a id="op-551b0f025ccf8e"></a>
### Test Runner.iter Run

`operation_foundation_testing_runner_business_behavior_test_runner_iter_run`

**Inputs** self.

**Declared result** Iterator at tuple at tuple(str, str, unittest.TestSuite).

**Local steps**

- For each tuple(app, categories) in self.per\_app\_categories.items().
  - Set sorted\_categories from sorted(categories.items(), key = deferred anonymous expression).
  - For each tuple(category, suite) in sorted\_categories.
    - If not self.\_has\_tests(suite).
      - Evaluate logger.debug(formatted text no tests for: {app}, {category}).
      - Continue with the next iteration or loop test.
    - Evaluate self.\_prepare\_category(category, suite, app).
    - Evaluate self.\_apply\_debug\_decorators(suite).
    - Within self.\_profile().
      - Evaluate logger.info(formatted text Starting tests for app: {app}, category: {category}).
      - yield tuple(app, category, suite).

On ordinary fall-through the sequence ends.

**Methods declared on this owner** [has tests](operations-013.md#op-16a900cc22c3b2), [prepare category](operations-013.md#op-dafb79560e98ef), [apply debug decorators](operations-013.md#op-461e03758608c7), [profile](operations-014.md#op-931bb81402f338).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L5933) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L643)

<a id="op-16a900cc22c3b2"></a>
### Test Runner.has tests

`operation_foundation_testing_runner_business_behavior_test_runner_has_tests`

**Inputs** self, suite.

**Explicit results** next(self.\_iterate\_suite(suite), no value) is distinct from no value.

**Local steps**

- Return next(self.\_iterate\_suite(suite), no value) is distinct from no value.

**Methods declared on this owner** [iterate suite](operations-014.md#op-2c39d2ee9105c2).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L6411) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L641)

<a id="op-dafb79560e98ef"></a>
### Test Runner.prepare category

`operation_foundation_testing_runner_business_behavior_test_runner_prepare_category`

**Inputs** self, category, suite, app.

**Local steps**

- Bind dependencies get\_compat\_Platform\_test\_case\_preparation.
- Set dispatcher from mapping(“integration” → self.integration\_preparation, “old-Platform-test-class-category” → get\_compat\_Platform\_test\_case\_preparation(self.cfg)).
- Set prepare\_method from dispatcher.get(category.lower()).
- If prepare\_method.
  - Evaluate prepare\_method(suite, app, category).
- Otherwise.
  - Evaluate logger.debug(formatted text Unknown test category: {category}. No specific preparation performed.).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L6501) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L645)

<a id="op-461e03758608c7"></a>
### Test Runner.apply debug decorators

`operation_foundation_testing_runner_business_behavior_test_runner_apply_debug_decorators`

**Inputs** self, suite.

**Local steps**

- If self.cfg.pdb\_on\_exceptions.
  - For each test in self.\_iterate\_suite(suite).
    - Evaluate setattr(test, test.\_testMethodName, debug\_on(expanded self.cfg.pdb\_on\_exceptions)(getattr(test, test.\_testMethodName))).

If control reaches the end, it returns no value.

**Methods declared on this owner** [iterate suite](operations-014.md#op-2c39d2ee9105c2).

**Values supplied outside this operation** selected callable from getattr(test, test.\_testMethodName).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0335.json#L6740) · [Binding](../../../current-decisions/foundation/bindings-005.tsv#L1966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-006.tsv#L640)
