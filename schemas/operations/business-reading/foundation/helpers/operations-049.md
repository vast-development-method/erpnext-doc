# Shared value and file services · operations 49

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Scheduler

<a id="op-16deb1fb944758"></a>
### Get scheduler status

`operation_foundation_utils_scheduler_business_behavior_get_scheduler_status`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** mapping(“status” → “inactive”) · mapping(“status” → “active”).

**Local steps**

- If is\_scheduler\_inactive().
  - Return mapping(“status” → “inactive”).
- Return mapping(“status” → “active”).

**Boundaries to resolve** callee failures, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L5597) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1847) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L627)

<a id="op-a19f681759ff00"></a>
### Get scheduler tick

`operation_foundation_utils_scheduler_business_behavior_get_scheduler_tick`

**Inputs** no declared parameters.

**Declared result** int.

**Explicit results** (cint(conf.scheduler\_tick\_interval) or DEFAULT\_SCHEDULER\_TICK).

**Local steps**

- Set conf from Platform.get\_conf().
- Return (cint(conf.scheduler\_tick\_interval) or DEFAULT\_SCHEDULER\_TICK).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cint(conf.scheduler\_tick\_interval) → DEFAULT\_SCHEDULER\_TICK.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L5705) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1848) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L628)

## Service · Sentry

<a id="op-1c37fe12d4cecb"></a>
### Platform Integration.setup once

`operation_foundation_utils_sentry_business_behavior_foundation_integration_setup_once`

**Inputs** no declared parameters.

**Wrappers, in declaration order** staticmethod.

**Local steps**

- Set real\_connect from Database.connect.
- Set real\_sql from Database.sql.
- Bind local operation sql for subsequent calls.
- Bind local operation connect for subsequent calls.
- Set Database.connect from connect.
- Set Database.sql from sql.

If control reaches the end, it returns no value.

**Boundaries to resolve** wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L74) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1861) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L638)

<a id="op-0d15b7a633ade5"></a>
### Platform Integration.setup once.sql

`operation_foundation_utils_sentry_business_behavior_foundation_integration_setup_once_database_query`

**Inputs** self, query, values = no value, remaining positional values args, remaining named values kwargs.

**Explicit results** real\_sql(self, query, (values or EmptyQueryValues), expanded args, expanded names kwargs).

**Local steps**

- Set hub from Hub.current.
- If not self.\_conn.
  - Evaluate self.connect().
- Within record\_sql\_queries(hub, self.\_cursor, query, values, paramstyle = “pyformat”, executemany = false).
  - Return real\_sql(self, query, (values or EmptyQueryValues), expanded args, expanded names kwargs).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in values → EmptyQueryValues.

If control reaches the end, it returns no value.

**Methods declared on this owner** [connect](operations-049.md#op-c7598d7252e2a1).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L76) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1863) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L640)

<a id="op-c7598d7252e2a1"></a>
### Platform Integration.setup once.connect

`operation_foundation_utils_sentry_business_behavior_foundation_integration_setup_once_connect`

**Inputs** self.

**Explicit results** real\_connect(self).

**Local steps**

- Set hub from Hub.current.
- Within capture\_internal\_exceptions().
  - Evaluate hub.add\_breadcrumb(message = “connect”, category = “query”).
- Within hub.start\_span(op = “db”, description = “connect”).
  - Return real\_connect(self).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L75) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1862) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L639)

<a id="op-b41185584d1cb5"></a>
### Set scope

`operation_foundation_utils_sentry_business_behavior_set_scope`

**Inputs** scope.

**Local steps**

- If job bound to rq.get\_current\_job().
  - Set kwargs from job.\_kwargs.
  - Set transaction\_name from str(kwargs at “method”).
  - Set context from Platform.\_dict(mapping(“scheduled” → false, “wait” → 0)).
  - If “run\_scheduled\_job” belongs to transaction\_name.
    - Set transaction\_name from kwargs.get(“kwargs”, mapping()).get(“job\_type”, empty text).
    - Set context.scheduled from true.
  - Set enqueued\_at from job.enqueued\_at.
  - If enqueued\_at.tzinfo is identical to no value.
    - Set enqueued\_at from enqueued\_at.replace(tzinfo = UTC).
  - Set waitdiff from (datetime.now(UTC) − enqueued\_at).
  - Set context.uuid from job.id.
  - Set context.wait from waitdiff.total\_seconds().
  - Set context.kwargs from kwargs.
  - Evaluate scope.set\_extra(“job”, context).
  - Evaluate scope.set\_transaction\_name(transaction\_name).
- Otherwise.
  - If Platform.form\_dict.cmd.
    - Set path from formatted text /api/method/{Platform.form\_dict.cmd}.
  - Otherwise.
    - Set path from Platform.request.path.
  - Evaluate scope.set\_transaction\_name(path, source = SOURCE\_FOR\_STYLE at “endpoint”).
- Evaluate scope.set\_user(mapping(“id” → Platform.local.site)).
- Set user from getattr(Platform.session, “user”, “Unidentified”).
- Evaluate scope.set\_tag(“Platform\_user”, user).
- If trace\_id bound to Platform.monitor.get\_trace\_id().
  - Evaluate scope.set\_tag(“Platform\_trace\_id”, trace\_id).

If control reaches the end, it returns no value.

**Values supplied outside this operation** clock or generated value from datetime.now(UTC) · selected callable from getattr(Platform.session, “user”, “Unidentified”).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L6598) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1864) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L641)

<a id="op-3db7e58449c5af"></a>
### Set sentry context

`operation_foundation_utils_sentry_business_behavior_set_sentry_context`

**Inputs** no declared parameters.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_system\_settings(“enable\_telemetry”).
  - Return no value.
- Set hub from Hub.current.
- Within hub.configure\_scope() bound as scope.
  - Evaluate set\_scope(scope).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_telemetry”).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L77) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1865) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L642)

<a id="op-00b7da74430199"></a>
### Before send

`operation_foundation_utils_sentry_business_behavior_before_send`

**Inputs** event, hint.

**Explicit results** no value · event.

**Local steps**

- If event.get(“logger”, empty text) equals “CSSUTILS”.
  - Return no value.
- Return event.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0502.json#L7477) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1859) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L636)

<a id="op-61e450e2734e41"></a>
### Capture exception

`operation_foundation_utils_sentry_business_behavior_capture_exception`

**Inputs** message = no value.

**Declared result** no value.

**Explicit results** no value.

**Local steps**

- If not Platform.get\_system\_settings(“enable\_telemetry”).
  - Return no value.
- Attempt the following.
  - Set hub from Hub.current.
  - Within hub.configure\_scope() bound as scope.
    - If (os.getenv(“ENABLE\_SENTRY\_DB\_MONITORING”) is identical to no value or os.getenv(“SENTRY\_TRACING\_SAMPLE\_RATE”) is identical to no value or os.getenv(“SENTRY\_PROFILING\_SAMPLE\_RATE”) is identical to no value).
      - Evaluate in order, stop at the first true operand, otherwise use the last operand in os.getenv(“ENABLE\_SENTRY\_DB\_MONITORING”) is identical to no value → os.getenv(“SENTRY\_TRACING\_SAMPLE\_RATE”) is identical to no value → os.getenv(“SENTRY\_PROFILING\_SAMPLE\_RATE”) is identical to no value.
      - Evaluate set\_scope(scope).
    - If Platform.request.
      - Set evt\_processor from \_make\_wsgi\_event\_processor(Platform.request.environ, false).
      - Evaluate scope.add\_event\_processor(evt\_processor).
      - If Platform.request.is\_json.
        - Evaluate scope.set\_context(“JSON Body”, Platform.request.json).
      - Otherwise.
        - If Platform.request.form.
          - Evaluate scope.set\_context(“Form Data”, Platform.request.form).
  - If client bound to hub.client.
    - Set exc\_info from sys.exc\_info().
    - If any(exc\_info).
      - If isinstance(exc\_info at 1, (Platform.ValidationError bitwise or Platform.PermissionError)).
        - Return no value.
      - Set tuple(event, hint) from event\_from\_exception(exc\_info, client\_options = client.options, mechanism = mapping(“type” → “wsgi”, “handled” → false)).
      - Evaluate hub.capture\_event(event, hint = hint).
    - Otherwise.
      - If message.
        - Evaluate sentry\_capture\_message(message, level = “error”).
- On failure (Exception).
  - Evaluate Platform.logger().error(“Failed to capture exception”, exc\_info = true).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“enable\_telemetry”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0018.json#L73) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1860) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L637)

## Service · Spdx

<a id="op-b018104e713579"></a>
### To spdx

`operation_foundation_binding_foundation_utils_sbom_spdx_to_spdx`

**Inputs** inventory, site.

**Declared result** dict.

**Explicit results** mapping(“spdxVersion” → “SPDX-2.3”, “dataLicense” → “CC0-1.0”, “SPDXID” → “SPDXRef-DOCUMENT”, “name” → formatted text SBOM for {site}, …).

**Local steps**

- Set ids from \_SPDXIds().
- Set packages from list of \_app\_package(app, ids) for app drawn from inventory.apps.
  - Draw app from inventory.apps.
- Update packages using + list of \_dependency\_package(package, ids) for package drawn from inventory.packages.
  - Draw package from inventory.packages.
- Set relationships from list of \_relationship(“SPDXRef-DOCUMENT”, “DESCRIBES”, ids.get(app)) for app drawn from inventory.apps.
  - Draw app from inventory.apps.
- Update relationships using + list of \_relationship(ids.get(d.dependent), “DEPENDS\_ON”, ids.get(d.dependency)) for d drawn from inventory.dependencies.
  - Draw d from inventory.dependencies.
- Return mapping(“spdxVersion” → “SPDX-2.3”, “dataLicense” → “CC0-1.0”, “SPDXID” → “SPDXRef-DOCUMENT”, “name” → formatted text SBOM for {site}, …).

**Values supplied outside this operation** clock or generated value from uuid.uuid4(), datetime.now(UTC).

**Boundaries to resolve** late-bound calls, callee failures, time or generated values, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L14) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L319) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L407)

<a id="op-13e86ed463c258"></a>
### SPDXIds.initialize

`operation_foundation_binding_foundation_utils_sbom_spdx_spdxids_init`

**Inputs** self.

**Local steps**

- Set self.ids from mapping().
- Set self.used from set().

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L13) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L318) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L406)

<a id="op-0832e7abbf6c65"></a>
### SPDXIds.get

`operation_foundation_binding_foundation_utils_sbom_spdx_spdxids_get`

**Inputs** self, item.

**Declared result** str.

**Explicit results** self.ids at item.

**Local steps**

- If item does not belong to self.ids.
  - Set prefix from “App” when isinstance(item, App), otherwise ID\_PREFIXES at item.ecosystem.
    - Value choice on isinstance(item, App) — true gives “App”, false gives ID\_PREFIXES at item.ecosystem.
  - Set base from re.sub(“&#91;^A-Za-z0-9.-&#93;”, “-”, formatted text SPDXRef-{prefix}-{item.name}-{(item.version or empty text)}).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in item.version → empty text.
  - Set tuple(spdx\_id, suffix) from tuple(base.rstrip(“-”), 1).
  - While spdx\_id belongs to self.used.
    - Update suffix using + 1.
    - Set spdx\_id from formatted text {base.rstrip(“-”)}-{suffix}.
  - Set self.ids at item from spdx\_id.
  - Evaluate self.used.add(spdx\_id).
- Return self.ids at item.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L12) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L317) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L405)

<a id="op-83418e6d79896c"></a>
### App package

`operation_foundation_binding_foundation_utils_sbom_spdx_app_package`

**Inputs** app, ids.

**Declared result** dict.

**Explicit results** package.

**Local steps**

- Set package from mapping(“name” → app.name, “SPDXID” → ids.get(app), “downloadLocation” → (\_vcs\_location(app.repository\_url, app.commit) or app.repository\_url or NOASSERTION), “supplier” → \_actor(“Organization”, “, ”.join( ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_vcs\_location(app.repository\_url, app.commit) → app.repository\_url → NOASSERTION.
- If app.description.
  - Set package at “description” from app.description.
- If purl bound to \_github\_purl(app.repository\_url, app.commit).
  - Set package at “externalRefs” from list(\_purl\_ref(purl)).
- Return package.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L4) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L309) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L397)

<a id="op-a64cdfc4229ede"></a>
### Dependency package

`operation_foundation_binding_foundation_utils_sbom_spdx_dependency_package`

**Inputs** package, ids.

**Declared result** dict.

**Explicit results** result.

**Local steps**

- Set result from mapping(“name” → package.name, “SPDXID” → ids.get(package), “downloadLocation” → (package.download\_url or \_vcs\_location(package.repository\_url, package.commit) or NOASSERTION), “supplier” → \_actor(“Person” ….
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in package.download\_url → \_vcs\_location(package.repository\_url, package.commit) → NOASSERTION.
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_github\_purl(package.repository\_url, package.commit) → \_purl(package).
- If checksums bound to \_checksums(package.integrity).
  - Set result at “checksums” from checksums.
- If package.vendored\_path.
  - Set result at “comment” from formatted text Vendored at {package.vendored\_path}.
- Return result.

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L7) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L312) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L400)

<a id="op-e0ab06ec2d1055"></a>
### Common fields

`operation_foundation_binding_foundation_utils_sbom_spdx_common_fields`

**Inputs** version, license.

**Declared result** dict.

**Explicit results** fields.

**Local steps**

- Set tuple(license\_declared, license\_comments) from to\_spdx\_license(license).
- Set fields from mapping(“filesAnalyzed” → false, “licenseConcluded” → NOASSERTION, “licenseDeclared” → license\_declared, “copyrightText” → NOASSERTION).
- If version.
  - Set fields at “versionInfo” from version.
- If license\_comments.
  - Set fields at “licenseComments” from license\_comments.
- Return fields.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L6) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L311) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L399)

<a id="op-c381f222a9d761"></a>
### Relationship

`operation_foundation_binding_foundation_utils_sbom_spdx_relationship`

**Inputs** element, relationship\_type, related\_element.

**Declared result** dict.

**Explicit results** mapping(“spdxElementId” → element, “relationshipType” → relationship\_type, “relatedSpdxElement” → related\_element).

**Local steps**

- Return mapping(“spdxElementId” → element, “relationshipType” → relationship\_type, “relatedSpdxElement” → related\_element).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L11) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L316) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L404)

<a id="op-d3e062a60617bf"></a>
### Actor

`operation_foundation_binding_foundation_utils_sbom_spdx_actor`

**Inputs** kind, name.

**Declared result** str.

**Explicit results** NOASSERTION · formatted text {kind}: {name}.

**Local steps**

- If not name.
  - Return NOASSERTION.
- Set name from re.sub(“\\s\*&lt;(&#91;^&gt;&#93;\*)&gt;”, “ (\\1)”, one space.join(name.split())).strip().
- Return formatted text {kind}: {name}.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L3) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L308) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L396)

<a id="op-a4879b56408012"></a>
### Vcs location

`operation_foundation_binding_foundation_utils_sbom_spdx_vcs_location`

**Inputs** repository\_url, commit.

**Declared result** (str bitwise or no value).

**Explicit results** formatted text git+{repository\_url}@{commit} · no value.

**Local steps**

- If (repository\_url and commit).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in repository\_url → commit.
  - Return formatted text git+{repository\_url}@{commit}.
- Return no value.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L15) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L320) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L408)

<a id="op-a343ec63b27801"></a>
### Purl

`operation_foundation_binding_foundation_utils_sbom_spdx_purl`

**Inputs** package.

**Declared result** str.

**Explicit results** formatted text {purl}@{quote(package.version, safe = empty text)} when package.version, otherwise purl.

**Local steps**

- If package.ecosystem equals “pypi”.
  - Set purl from formatted text pkg:pypi/{canonicalize\_name(package.name)}.
- Otherwise.
  - Set purl from formatted text pkg:npm/{quote(package.name, safe = “/”)}.
- Return formatted text {purl}@{quote(package.version, safe = empty text)} when package.version, otherwise purl.
  - Value choice on package.version — true gives formatted text {purl}@{quote(package.version, safe = empty text)}, false gives purl.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L9) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L314) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L402)

<a id="op-ab455cf1e28552"></a>
### Github purl

`operation_foundation_binding_foundation_utils_sbom_spdx_github_purl`

**Inputs** repository\_url, commit.

**Declared result** (str bitwise or no value).

**Explicit results** no value · formatted text pkg:github/{owner}/{repo}@{commit}.lower() when owner, otherwise no value.

**Local steps**

- If (not repository\_url or not commit).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in not repository\_url → not commit.
  - Return no value.
- Set tuple(owner, repo) from parse\_github\_url(repository\_url).
- Return formatted text pkg:github/{owner}/{repo}@{commit}.lower() when owner, otherwise no value.
  - Value choice on owner — true gives formatted text pkg:github/{owner}/{repo}@{commit}.lower(), false gives no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L8) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L313) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L401)

<a id="op-b02daaf8f3eb53"></a>
### Purl ref

`operation_foundation_binding_foundation_utils_sbom_spdx_purl_ref`

**Inputs** purl.

**Declared result** dict.

**Explicit results** mapping(“referenceCategory” → “PACKAGE-MANAGER”, “referenceType” → “purl”, “referenceLocator” → purl).

**Local steps**

- Return mapping(“referenceCategory” → “PACKAGE-MANAGER”, “referenceType” → “purl”, “referenceLocator” → purl).

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L10) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L315) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L403)

<a id="op-9703e8c0c97547"></a>
### Checksums

`operation_foundation_binding_foundation_utils_sbom_spdx_checksums`

**Inputs** integrity.

**Declared result** list at dict.

**Explicit results** checksums.

**Local steps**

- Set checksums from list().
- For each item in (integrity or empty text).split().
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in integrity → empty text.
  - Set tuple(algorithm, \_, digest) from item.partition(“-”).
  - If algorithm does not belong to CHECKSUM\_ALGORITHMS.
    - Continue with the next iteration or loop test.
  - Within contextlib.suppress(binascii.Error).
    - Evaluate checksums.append(mapping(“algorithm” → CHECKSUM\_ALGORITHMS at algorithm, “checksumValue” → base64.b64decode(digest, validate = true).hex())).
- Return checksums.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0010.json#L5) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L310) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L398)

## Service · Synchronization

<a id="op-9c6bbeaa98efbf"></a>
### Filelock

`operation_foundation_utils_synchronization_business_behavior_filelock`

**Inputs** lock\_name, timeout (named only, default 30), is\_global (named only, default false).

**Wrappers, in declaration order** contextmanager.

**Explicit failure paths** LockTimeoutError(((translated “Failed to aquire lock: {}. Lock may be held by another process.”.format(lock\_name) + text in the contract) + translated “Wait for it to finish. Deleting the lock file {} will ….

**Local steps**

- Bind dependencies \_StrongFileLock.
- Bind dependencies Timeout.
- Set lock\_filename from (lock\_name + “.lock”).
- If not is\_global.
  - Set lock\_path from os.path.abspath(get\_site\_path(LOCKS\_DIR, lock\_filename)).
- Otherwise.
  - Set lock\_path from os.path.abspath(os.path.join(get\_bench\_path(), “config”, lock\_filename)).
- Attempt the following.
  - Within \_StrongFileLock(lock\_path, timeout = timeout).
    - yield no value.
- On failure (Timeout) bound to e.
  - Evaluate Platform.log\_error(formatted text Filelock: Failed to aquire {lock\_path}).
  - Raise LockTimeoutError(((translated “Failed to aquire lock: {}. Lock may be held by another process.”.format(lock\_name) + text in the contract) + translated “Wait for it to finish. Deleting the lock file {} will … with cause e.

On ordinary fall-through the sequence ends.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L805) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1944) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L721)

## Service · Telemetry

<a id="op-1d2c0e5d3f623c"></a>
### Add bootinfo

`operation_foundation_utils_telemetry_initialize_business_behavior_add_bootinfo`

**Inputs** bootinfo.

**Local steps**

- Set bootinfo.telemetry\_site\_age from site\_age().
- Set bootinfo.telemetry\_provider from list().
- If is\_pulse\_enabled().
  - Set bootinfo.enable\_telemetry from true.
  - Evaluate bootinfo.telemetry\_provider.append(“pulse”).
  - Set bootinfo.telemetry from pulse\_boot\_config().

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0503.json#L5895) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-008.tsv#L722)
