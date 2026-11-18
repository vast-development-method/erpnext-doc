# Shared value and file services · operations 9

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Chrome pdf generator

<a id="op-688f71c98bdf61"></a>
### Chrome PDFGenerator.start chromium process

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_start_chromium_process_d0626d28a85d`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** self, command\_args.

**Explicit result forms** a value selected from the current context.

**Local structure** 1 condition or selection sites, 0 statement loops and 0 exception handlers.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L94) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L164) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L252)

<a id="op-0b775042bd0071"></a>
### Chrome PDFGenerator.stop chromium process

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_stop_chromium_process`

**Inputs** self.

**Local steps**

- Evaluate self.\_signal\_chromium().
- Attempt the following.
  - Evaluate self.\_chromium\_process.wait(timeout = 5).
- On failure (subprocess.TimeoutExpired).
  - Evaluate self.\_signal\_chromium(kill = true).
  - Evaluate self.\_chromium\_process.wait().
- Evaluate self.\_chromium\_process.stderr.close().

If control reaches the end, it returns no value.

**Methods declared on this owner** [signal chromium](operations-009.md#op-8a684f8e66143c).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L95) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L165) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L253)

<a id="op-8a684f8e66143c"></a>
### Chrome PDFGenerator.signal chromium

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_signal_chromium`

**Inputs** self, kill = false.

**Explicit results** no value.

**Local steps**

- Set process from self.\_chromium\_process.
- If platform.system().lower() equals “windows”.
  - Evaluate process.kill() when kill, otherwise process.terminate().
    - Value choice on kill — true gives process.kill(), false gives process.terminate().
  - Return no value.
- Attempt the following.
  - Evaluate os.killpg(process.pid, signal.SIGKILL when kill, otherwise signal.SIGTERM).
    - Value choice on kill — true gives signal.SIGKILL, false gives signal.SIGTERM.
- On failure (ProcessLookupError).
  - Take no action here.
- On failure (PermissionError).
  - Evaluate process.kill() when kill, otherwise process.terminate().
    - Value choice on kill — true gives process.kill(), false gives process.terminate().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L92) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L162) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L250)

<a id="op-e3f841bdefc75f"></a>
### Chrome PDFGenerator.reap orphaned chromium

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_reap_orphaned_chromium`

**Inputs** self.

**Local steps**

- Set chromium\_path from os.path.realpath(self.\_chromium\_path).
- For each proc in psutil.process\_iter(list(“exe”, “ppid”, “cmdline”)).
  - Attempt the following.
    - If (proc.info at “ppid” equals 1 and proc.info at “exe” equals chromium\_path and “--headless” belongs to (proc.info at “cmdline” or list())).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in proc.info at “ppid” equals 1 → proc.info at “exe” equals chromium\_path → “--headless” belongs to (proc.info at “cmdline” or list()).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in proc.info at “cmdline” → list().
      - For each child in proc.children(recursive = true).
        - Evaluate child.kill().
      - Evaluate proc.kill().
  - On failure (tuple(psutil.NoSuchProcess, psutil.AccessDenied)).
    - Continue with the next iteration or loop test.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L89) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L159) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L247)

<a id="op-429393dbd99622"></a>
### Chrome PDFGenerator.set devtools url

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_set_devtools_url`

**Inputs** self, retry = true.

**Explicit failure paths** TimeoutError(“Chromium took too long to start.”).

**Local steps**

- Set stderr from self.\_chromium\_process.stderr.
- Set start\_time from time.time().
- Set exited from false.
- While (time.time() − start\_time) &lt; self.START\_TIMEOUT.
  - Set line from stderr.readline().
  - If not line.
    - Set exited from true.
    - Leave the innermost loop without its normal-exhaustion alternative.
  - If “DevTools listening on” belongs to line.
    - Set url\_start from line.find(“ws://”).
    - If url\_start differs from negative 1.
      - Set self.\_devtools\_url from line at slice url\_start to no value.strip().
      - Leave the innermost loop without its normal-exhaustion alternative.
- If not self.\_devtools\_url.
  - Set alive from (not exited and self.\_chromium\_process.poll() is identical to no value).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in not exited → self.\_chromium\_process.poll() is identical to no value.
  - If not (retry and alive).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in retry → alive.
    - Evaluate self.\_signal\_chromium().
    - Raise TimeoutError(“Chromium took too long to start.”).
  - Evaluate self.\_stop\_chromium\_process().
  - Evaluate self.start\_chromium\_process(debug = self.debug\_mode).
  - Evaluate self.\_set\_devtools\_url(retry = false).

If control reaches the end, it returns no value.

**Methods declared on this owner** [signal chromium](operations-009.md#op-8a684f8e66143c), [stop chromium process](operations-009.md#op-0b775042bd0071), [start chromium process](operations-008.md#op-245b0dc50086b5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L91) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L161) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L249)

<a id="op-97df0d05f1f831"></a>
### Chrome PDFGenerator.close browser

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_close_browser`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.\_browsers.
  - Evaluate Platform.log(“Cannot close Chromium as there are active browser instances.”).
  - Return no value.
- If self.\_chromium\_process.
  - Evaluate self.\_stop\_chromium\_process().
- Set ChromePDFGenerator.\_instance from no value.
- Set self.\_chromium\_process from no value.
- Set self.\_devtools\_url from no value.
- Evaluate Platform.log(“Headless Chromium closed successfully.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [stop chromium process](operations-009.md#op-0b775042bd0071).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L83) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L153) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L241)

<a id="op-198b461365c538"></a>
### Chrome PDFGenerator.detach debug browser

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_detach_debug_browser`

**Inputs** self.

**Local steps**

- Set ChromePDFGenerator.\_instance from no value.
- Set self.\_initialized from false.
- Set self.\_chromium\_process from no value.
- Set self.\_devtools\_url from no value.

If control reaches the end, it returns no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L84) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L154) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L242)

<a id="op-6174affd23a3b9"></a>
### Chrome PDFGenerator.fetch devtools url

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_fetch_devtools_url`

**Inputs** self, port.

**Explicit results** no value · response\_data at “webSocketDebuggerUrl”.strip().

**Local steps**

- If not port.
  - Return no value.
- Set url from formatted command or address in the contract.
- Attempt the following.
  - Set response from requests.get(url).
  - Evaluate response.raise\_for\_status().
  - Set response\_data from response.json().
  - Return response\_data at “webSocketDebuggerUrl”.strip().
- On failure (requests.ConnectionError).
  - Evaluate Platform.log\_error(formatted text Failed to connect to the Chrome DevTools Protocol. Is Chrome running with --remote-debugging-port={port}).
- On failure (requests.RequestException) bound to e.
  - Evaluate Platform.log\_error(formatted text An error occurred: {e}).
- Return no value.

**Values supplied outside this operation** service or queued work from requests.get(url).

**Boundaries to resolve** late-bound calls, external or queued work, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L85) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L155) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L243)

## Service · Client

<a id="op-1c1b506ed7dc91"></a>
### Is enabled

`operation_foundation_utils_telemetry_pulse_client_business_behavior_is_enabled`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** false · true · bool((not Platform.conf.get(“developer\_mode”, 0) and Platform.get\_system\_settings(“enable\_telemetry”))).

**Local steps**

- If not Platform.conf.get(“pulse\_api\_key”).
  - Return false.
- If Platform.conf.get(“pulse\_force\_enabled”).
  - Return true.
- Return bool((not Platform.conf.get(“developer\_mode”, 0) and Platform.get\_system\_settings(“enable\_telemetry”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not Platform.conf.get(“developer\_mode”, 0) → Platform.get\_system\_settings(“enable\_telemetry”).

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_telemetry”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L7060) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L733)

<a id="op-cf9a57be451380"></a>
### Boot config

`operation_foundation_utils_telemetry_pulse_client_business_behavior_boot_configuration`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist(allow\_guest = true).

**Declared result** dict.

**Explicit results** mapping(“enabled” → false) · mapping(“enabled” → true, “host” → host, “client\_url” → formatted text {host}/assets/pulse/js/pulse\_client.js, “key” → Platform.conf.get(“pulse\_api\_key”), …).

**Local steps**

- If not is\_enabled().
  - Return mapping(“enabled” → false).
- Bind dependencies site\_age.
- Set host from pulse\_host().
- Set session\_user from Platform.session.user.
- If session\_user belongs to Platform.STANDARD\_USERS.
  - Set session\_user from no value.
- Return mapping(“enabled” → true, “host” → host, “client\_url” → formatted text {host}/assets/pulse/js/pulse\_client.js, “key” → Platform.conf.get(“pulse\_api\_key”), …).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L7239) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L729)

<a id="op-31f2523a88c2e9"></a>
### Capture

`operation_foundation_utils_telemetry_pulse_client_business_behavior_capture`

**Inputs** event\_name, app = no value, user = no value, team = no value, captured\_at = no value, properties = no value, interval = no value, site (named only, default no value).

**Explicit results** no value.

**Local steps**

- If not is\_enabled().
  - Return no value.
- Set user from (user or Platform.session.user).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in user → Platform.session.user.
- Set team from (team or Platform.conf.get(“fc\_team”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in team → Platform.conf.get(“fc\_team”).
- Attempt the following.
  - Set eq from EventQueue().
  - Evaluate eq.add(mapping(“event\_name” → event\_name, “captured\_at” → (captured\_at or utc\_iso()), “app” → app, “site” → (site or Platform.local.site), …), interval = interval).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in captured\_at → utc\_iso().
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in site → Platform.local.site.
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in properties → mapping().
- On failure (Exception) bound to e.
  - Evaluate Platform.logger(“pulse”).error(formatted text pulse-client - capture failed: {e}).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L730)

<a id="op-573f3f5e24290f"></a>
### Identify

`operation_foundation_utils_telemetry_pulse_client_business_behavior_identify`

**Inputs** properties = no value.

**Explicit results** no value.

**Local steps**

- Set team from Platform.conf.get(“fc\_team”).
- If (not is\_enabled() or not team).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_enabled() → not team.
  - Return no value.
- If isinstance(properties, str).
  - Attempt the following.
    - Set properties from Platform.parse\_json(properties).
  - On failure (Exception) bound to e.
    - Evaluate Platform.logger(“pulse”).error(formatted text pulse-client - identify: invalid properties json: {e}).
    - Return no value.
- Set endpoint from (Platform.conf.get(“pulse\_identify\_endpoint”) or “/api/method/pulse.api.identify”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“pulse\_identify\_endpoint”) → “/api/method/pulse.api.identify”.
- Evaluate PulseHTTP().post(endpoint, mapping(“team” → team, “properties” → (properties or mapping())), label = “identify”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in properties → mapping().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L608) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L732)

<a id="op-4fc57652090c9a"></a>
### Alias

`operation_foundation_utils_telemetry_pulse_client_business_behavior_alias`

**Inputs** previous\_id.

**Explicit results** no value.

**Local steps**

- Set team from Platform.conf.get(“fc\_team”).
- If (not is\_enabled() or not previous\_id or not team).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not is\_enabled() → not previous\_id → not team.
  - Return no value.
- Set endpoint from (Platform.conf.get(“pulse\_alias\_endpoint”) or “/api/method/pulse.api.alias”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“pulse\_alias\_endpoint”) → “/api/method/pulse.api.alias”.
- Evaluate PulseHTTP().post(endpoint, mapping(“previous\_id” → previous\_id, “team” → team), label = “alias”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L1019) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L728)

<a id="op-e454ba72c7a042"></a>
### Send queued events

`operation_foundation_utils_telemetry_pulse_client_business_behavior_send_queued_events`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not Platform.conf.get(“pulse\_api\_key”).
  - Return no value.
- Set http from PulseHTTP().
- Set endpoint from (Platform.conf.get(“pulse\_ingest\_endpoint”) or “/api/method/pulse.api.bulk\_ingest”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.conf.get(“pulse\_ingest\_endpoint”) → “/api/method/pulse.api.bulk\_ingest”.
- Bind local operation post\_batch for subsequent calls.
- Evaluate EventQueue().batch\_process(post\_batch, batch\_size = 100, max\_batches = 10).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L1254) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L734)

<a id="op-fda82c1d29f0d7"></a>
### Send queued events.post batch

`operation_foundation_utils_telemetry_pulse_client_business_behavior_send_queued_events_post_batch`

**Inputs** events.

**Local steps**

- Evaluate http.post(endpoint, mapping(“events” → events), label = “ingest”, raise\_on\_error = true).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L1503) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L735)

<a id="op-b98b254b2732e1"></a>
### Get debug info

`operation_foundation_utils_telemetry_pulse_client_business_behavior_get_debug_info`

**Inputs** fetch\_events = no value, fetch\_rate\_limited\_events = no value.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** info.

**Local steps**

- Evaluate Platform.only\_for(“System Manager”).
- Set info from Platform.\_dict().
- Set info.is\_enabled from is\_enabled().
- If info.is\_enabled.
  - Set eq from EventQueue().
  - Set info.queued\_event\_count from eq.length.
  - If fetch\_events.
    - Set limit from int(fetch\_events) when str(fetch\_events).isdigit(), otherwise 20.
      - Value choice on str(fetch\_events).isdigit() — true gives int(fetch\_events), false gives 20.
    - Set info.queued\_events from eq.get\_events(limit).
  - If fetch\_rate\_limited\_events.
    - Set limit from int(fetch\_rate\_limited\_events) when str(fetch\_rate\_limited\_events).isdigit(), otherwise 20.
      - Value choice on str(fetch\_rate\_limited\_events).isdigit() — true gives int(fetch\_rate\_limited\_events), false gives 20.
    - Set info.rate\_limited\_events from eq.get\_last\_sent\_events(limit).
- Return info.

**Values supplied outside this operation** effective access from Platform.only\_for(“System Manager”).

**Boundaries to resolve** late-bound calls, callee failures, effective access, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0504.json#L1592) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L731)

## Service · Collector

<a id="op-232fe0b0ca041e"></a>
### License.summary

`operation_foundation_binding_foundation_utils_sbom_collector_license_summary`

**Inputs** self.

**Wrappers, in declaration order** property.

**Declared result** (str bitwise or no value).

**Explicit results** self.expression · nested operand in the contract.classifiers at 0.split(“::”) at negative 1.strip() · self.text.

**Local steps**

- If self.expression.
  - Return self.expression.
- If self.classifiers.
  - Return nested operand in the contract.classifiers at 0.split(“::”) at negative 1.strip().
- Return self.text.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L219) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L289) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L377)

<a id="op-ea86cfd9ba46d8"></a>
### Inventory.direct dependencies

`operation_foundation_binding_foundation_utils_sbom_collector_inventory_direct_dependencies`

**Inputs** self, app.

**Declared result** list at Package.

**Explicit results** list of d.dependency for d drawn from self.dependencies where (d.dependent equals app and isinstance(d.dependency, Package)).

**Local steps**

- Return list of d.dependency for d drawn from self.dependencies where (d.dependent equals app and isinstance(d.dependency, Package)).
  - Draw d from self.dependencies, keep a combination only if ((d.dependent equals app and isinstance(d.dependency, Package))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in d.dependent equals app → isinstance(d.dependency, Package).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L217) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L287) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L375)

<a id="op-9c65009e2a3c16"></a>
### Collect

`operation_foundation_binding_foundation_utils_sbom_collector_collect`

**Inputs** apps.

**Declared result** Inventory.

**Explicit results** \_Collector(apps).collect().

**Local steps**

- Return \_Collector(apps).collect().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L207) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L277) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L365)

<a id="op-3af05fd1be9d64"></a>
### Collector.initialize

`operation_foundation_binding_foundation_utils_sbom_collector_collector_init`

**Inputs** self, app\_names.

**Local steps**

- Set self.app\_names from app\_names.
- Set self.apps from mapping().
- Set self.packages from mapping().
- Set self.dependencies from mapping().
- Set self.expanded\_python\_extras from set().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L214) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L284) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L372)

<a id="op-25bf8590dfedb8"></a>
### Collector.collect

`operation_foundation_binding_foundation_utils_sbom_collector_collector_collect`

**Inputs** self.

**Declared result** Inventory.

**Explicit results** Inventory(apps = list(self.apps.values()), packages = list(self.packages.values()), dependencies = list(self.dependencies)).

**Local steps**

- For each name in self.app\_names.
  - Set self.apps at canonicalize\_name(name) from get\_app(name).
- For each app in self.apps.values().
  - Evaluate self.add\_python\_dependencies(app).
  - Evaluate self.add\_js\_dependencies(app).
- If app bound to self.apps.get(“Platform”).
  - Evaluate self.add\_vendored\_libraries(app).
- Return Inventory(apps = list(self.apps.values()), packages = list(self.packages.values()), dependencies = list(self.dependencies)).

**Methods declared on this owner** [add python dependencies](operations-009.md#op-4f49427027d0a8), [add js dependencies](operations-010.md#op-20f8d4000fe274), [add vendored libraries](operations-010.md#op-65c25f376914ef).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L211) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L281) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L369)

<a id="op-518ebef4d30cdb"></a>
### Collector.link

`operation_foundation_binding_foundation_utils_sbom_collector_collector_link`

**Inputs** self, dependent, dependency.

**Local steps**

- Set self.dependencies at Dependency(dependent, dependency) from no value.

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L215) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L285) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L373)

<a id="op-4f49427027d0a8"></a>
### Collector.add python dependencies

`operation_foundation_binding_foundation_utils_sbom_collector_collector_add_python_dependencies`

**Inputs** self, app.

**Local steps**

- Set pyproject from (get\_pyproject(app.name) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_pyproject(app.name) → mapping().
- Set queue from list of tuple(app, requirement) for requirement drawn from \_parse\_requirements(pyproject.get(“project”, mapping()).get(“dependencies”, list())) where \_marker\_matches(requirement, empty text).
  - Draw requirement from \_parse\_requirements(pyproject.get(“project”, mapping()).get(“dependencies”, list())), keep a combination only if (\_marker\_matches(requirement, empty text)).
- While queue.
  - Set tuple(dependent, requirement) from queue.pop(0).
  - Set name from canonicalize\_name(requirement.name).
  - If name belongs to self.apps.
    - Evaluate self.link(dependent, self.apps at name).
    - Continue with the next iteration or loop test.
  - Set tuple(package, distribution) from self.get\_python\_package(requirement.name).
  - Evaluate self.link(dependent, package).
  - If not distribution.
    - Continue with the next iteration or loop test.
  - For each extra in tuple(empty text, expanded sorted(requirement.extras)).
    - If tuple(name, extra) belongs to self.expanded\_python\_extras.
      - Continue with the next iteration or loop test.
    - Evaluate self.expanded\_python\_extras.add(tuple(name, extra)).
    - Evaluate queue.extend(generator of tuple(package, child) for child drawn from \_parse\_requirements((distribution.requires or list())) where \_marker\_matches(child, extra)).
      - Draw child from \_parse\_requirements((distribution.requires or list())), keep a combination only if (\_marker\_matches(child, extra)).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in distribution.requires → list().

If control reaches the end, it returns no value.

**Methods declared on this owner** [link](operations-009.md#op-518ebef4d30cdb), [get python package](operations-009.md#op-069959b89bc181).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L209) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L279) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L367)

<a id="op-069959b89bc181"></a>
### Collector.get python package

`operation_foundation_binding_foundation_utils_sbom_collector_collector_get_python_package`

**Inputs** self, name.

**Declared result** tuple at tuple(Package, (importlib.metadata.Distribution bitwise or no value)).

**Explicit results** tuple(self.packages at key, distribution).

**Local steps**

- Attempt the following.
  - Set distribution from importlib.metadata.distribution(name).
- On failure (importlib.metadata.PackageNotFoundError).
  - Set distribution from no value.
- Set key from tuple(“pypi”, canonicalize\_name(name)).
- If key does not belong to self.packages.
  - Set self.packages at key from \_python\_package(distribution) when distribution, otherwise Package(ecosystem = “pypi”, name = name).
    - Value choice on distribution — true gives \_python\_package(distribution), false gives Package(ecosystem = “pypi”, name = name).
- Return tuple(self.packages at key, distribution).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L213) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L283) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L371)
