# Shared value and file services · operations 8

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Change log

<a id="op-a187bd08c8b72f"></a>
### Get versions

`operation_foundation_utils_change_log_business_behavior_get_versions`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**Explicit results** versions.

**Local steps**

- Set versions from mapping().
- For each app in Platform.get\_installed\_apps(\_ensure\_on\_bench = true).
  - Set app\_hooks from Platform.get\_hooks(app\_name = app).
  - Set app\_color from app\_hooks.get(“app\_color”).
  - Set logo from no value.
  - Set apps\_screen from app\_hooks.get(“add\_to\_apps\_screen”).
  - If (apps\_screen and apps\_screen at 0.get(“logo”)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in apps\_screen → apps\_screen at 0.get(“logo”).
    - Set logo from apps\_screen at 0 at “logo”.
  - Otherwise.
    - If app\_hooks.get(“app\_logo\_url”).
      - Set logo from app\_hooks at “app\_logo\_url” at 0.
  - Set versions at app from mapping(“title” → app\_hooks.get(“app\_title”) at 0, “description” → app\_hooks.get(“app\_description”) at 0, “branch” → get\_app\_branch(app), “color” → app\_color at 0 when app\_color, otherwise no value, …).
    - Value choice on app\_color — true gives app\_color at 0, false gives no value.
  - If versions at app at “branch” differs from “master”.
    - Set branch\_version from app\_hooks.get(“{}\_version”.format(versions at app at “branch”)).
    - If branch\_version.
      - Set versions at app at “branch\_version” from (branch\_version at 0 + formatted text  ({get\_app\_last\_commit\_ref(app)})).
  - Attempt the following.
    - Set versions at app at “version” from Platform.get\_attr((app + “.\_\_version\_\_”)).
  - On failure (AttributeError).
    - Set versions at app at “version” from “0.0.1”.
- Return versions.

**Values supplied outside this operation** selected callable from Platform.get\_hooks(app\_name = app), Platform.get\_attr((app + “.\_\_version\_\_”)).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L78) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L966) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1591)

<a id="op-839dd0f4d67bf4"></a>
### Get app branch

`operation_foundation_utils_change_log_business_behavior_get_application_branch`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** app.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L6673) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L957) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1582)

<a id="op-18413632de5db7"></a>
### Get app last commit ref

`operation_foundation_utils_change_log_business_behavior_get_application_last_commit_reference`

**Control responsibility** Controlled execution. The caller supplies work to an execution or administration boundary. The authorized environment, isolation policy and completion status determine the effect.

**Declared inputs** app.

**Explicit result forms** a scalar literal, a value selected from the current context.

**Local structure** 0 condition or selection sites, 0 statement loops and 1 exception handlers.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L6926) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L958) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1583)

<a id="op-ec28da51e3866f"></a>
### Check for update

`operation_foundation_utils_change_log_business_behavior_check_for_update`

**Inputs** no declared parameters.

**Explicit results** no value · updates.

**Local steps**

- If (Platform.get\_system\_settings(“disable\_system\_update\_notification”) or not Platform.is\_setup\_complete()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in Platform.get\_system\_settings(“disable\_system\_update\_notification”) → not Platform.is\_setup\_complete().
  - Return no value.
- Set updates from Platform.\_dict(major = list(), minor = list(), patch = list()).
- Set apps from get\_versions().
- For each app in apps.
  - Set remote\_url from get\_source\_url(app).
  - If not remote\_url.
    - Continue with the next iteration or loop test.
  - Set tuple(owner, repo) from parse\_github\_url(remote\_url).
  - If (not owner or not repo).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not owner → not repo.
    - Continue with the next iteration or loop test.
  - Set branch\_version from apps at app at “branch\_version”.split(one space, 1) at 0 when apps at app.get(“branch\_version”, empty text), otherwise empty text.
    - Value choice on apps at app.get(“branch\_version”, empty text) — true gives apps at app at “branch\_version”.split(one space, 1) at 0, false gives empty text.
  - If “develop” belongs to branch\_version.
    - Return updates.
  - Set instance\_version from Version((branch\_version or apps at app.get(“version”))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in branch\_version → apps at app.get(“version”).
  - Set tuple(github\_version, org\_name) from check\_release\_on\_github(owner, repo, instance\_version).
  - If (not github\_version or not org\_name).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not github\_version → not org\_name.
    - Continue with the next iteration or loop test.
  - For each update\_type in updates.
    - If github\_version.\_\_dict\_\_ at update\_type &gt; instance\_version.\_\_dict\_\_ at update\_type.
      - Evaluate updates at update\_type.append(Platform.\_dict(current\_version = str(instance\_version), available\_version = str(github\_version), org\_name = org\_name, app\_name = app, …)).
      - Leave the innermost loop without its normal-exhaustion alternative.
    - If github\_version.\_\_dict\_\_ at update\_type &lt; instance\_version.\_\_dict\_\_ at update\_type.
      - Leave the innermost loop without its normal-exhaustion alternative.
- Evaluate add\_message\_to\_redis(updates).
- Return updates.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“disable\_system\_update\_notification”).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0466.json#L7179) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L955) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1580)

<a id="op-58ff89bcf50908"></a>
### Has app update notifications

`operation_foundation_utils_change_log_business_behavior_has_application_update_notifications`

**Inputs** no declared parameters.

**Declared result** bool.

**Explicit results** bool(Platform.cache.sismember(“changelog-update-user-set”, Platform.session.user)).

**Local steps**

- Return bool(Platform.cache.sismember(“changelog-update-user-set”, Platform.session.user)).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L6) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L967) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1592)

<a id="op-c94f37b6e70b8b"></a>
### Parse latest non beta release

`operation_foundation_utils_change_log_business_behavior_parse_latest_non_beta_release`

**Inputs** response, current\_version.

**Declared result** (list bitwise or no value).

**Explicit results** sorted(version\_list, key = prioritize\_minor\_update, reverse = true) at 0 · no value.

**Local steps**

- Set version\_list from list().
- For each release in response.
  - Set tag from release.get(“tag\_name”).
  - If (release.get(“prerelease”) or not isinstance(tag, str)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in release.get(“prerelease”) → not isinstance(tag, str).
    - Continue with the next iteration or loop test.
  - Set version from tag.removeprefix(“v”).
  - Attempt the following.
    - Evaluate Version(version).
  - On failure (ValueError).
    - Continue with the next iteration or loop test.
  - Evaluate version\_list.append(version).
- Bind local operation prioritize\_minor\_update for subsequent calls.
- If version\_list.
  - Return sorted(version\_list, key = prioritize\_minor\_update, reverse = true) at 0.
- Return no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0017.json#L79) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L969) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1594)

<a id="op-abaead3088b6aa"></a>
### Parse latest non beta release.prioritize minor update

`operation_foundation_utils_change_log_business_behavior_parse_latest_non_beta_release_prioritize_minor_update`

**Inputs** v.

**Declared result** Version.

**Explicit results** tuple(current\_version.major equals target.major, target).

**Local steps**

- Set target from Version(v).
- Return tuple(current\_version.major equals target.major, target).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L399) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L970) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1595)

<a id="op-249bb2e36a0d0d"></a>
### Check release on github

`operation_foundation_utils_change_log_business_behavior_check_release_on_github`

**Inputs** owner, repo, current\_version.

**Declared result** (tuple at tuple(Version, str) bitwise or tuple at tuple(no value, no value)).

**Explicit results** tuple(Version(latest\_non\_beta\_release), owner) · tuple(no value, no value).

**Explicit failure paths** ValueError(“Owner cannot be empty”) · ValueError(“Repo cannot be empty”).

**Local steps**

- If not owner.
  - Raise ValueError(“Owner cannot be empty”).
- If not repo.
  - Raise ValueError(“Repo cannot be empty”).
- Set releases from \_get\_latest\_releases(owner, repo).
- Set latest\_non\_beta\_release from parse\_latest\_non\_beta\_release(releases, current\_version).
- If latest\_non\_beta\_release.
  - Return tuple(Version(latest\_non\_beta\_release), owner).
- Return tuple(no value, no value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L498) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L956) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1581)

<a id="op-142a16c54ddf69"></a>
### Security issues count

`operation_foundation_utils_change_log_business_behavior_security_issues_count`

**Inputs** owner, repo, current\_version, target\_version.

**Declared result** int.

**Explicit results** len(list of sa for sa drawn from advisories where applicable(sa)).

**Local steps**

- Set advisories from \_get\_security\_issues(owner, repo).
- Bind local operation applicable for subsequent calls.
- Return len(list of sa for sa drawn from advisories where applicable(sa)).
  - Draw sa from advisories, keep a combination only if (applicable(sa)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L786) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L971) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1596)

<a id="op-f527521e867c0f"></a>
### Security issues count.applicable

`operation_foundation_utils_change_log_business_behavior_security_issues_count_applicable`

**Inputs** advisory.

**Declared result** bool.

**Explicit results** true.

**Local steps**

- For each vuln in advisory at “vulnerabilities”.
  - Within suppress(Exception).
    - Set vulnerable\_range from SimpleSpec(vuln at “vulnerable\_version\_range”.replace(one space, empty text)).
    - Set patch\_version from Version(vuln at “patched\_versions”.replace(one space, empty text)).
    - If (current\_version belongs to vulnerable\_range and target\_version does not belong to vulnerable\_range and current\_version.major equals patch\_version.major).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in current\_version belongs to vulnerable\_range → target\_version does not belong to vulnerable\_range → current\_version.major equals patch\_version.major.
      - Return true.

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L1194) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L972) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1597)

<a id="op-3100d4436dce0a"></a>
### Get latest releases

`operation_foundation_utils_change_log_business_behavior_get_latest_releases`

**Inputs** owner, repo.

**Wrappers, in declaration order** redis\_cache(ttl = (((6 × 24) × 60) × 60), shared = true).

**Explicit results** list() · r.json().

**Local steps**

- Bind dependencies requests.
- Set r from requests.get(formatted command or address in the contract).
- If not r.ok.
  - Return list().
- Return r.json().

**Values supplied outside this operation** service or queued work from requests.get(formatted command or address in the contract).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L1456) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L962) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1587)

<a id="op-c4a85ee68f2432"></a>
### Get security issues

`operation_foundation_utils_change_log_business_behavior_get_security_issues`

**Inputs** owner, repo.

**Wrappers, in declaration order** redis\_cache(ttl = (((6 × 24) × 60) × 60), shared = true).

**Explicit results** list() · r.json().

**Local steps**

- Bind dependencies requests.
- Set r from requests.get(formatted command or address in the contract).
- If not r.ok.
  - Return list().
- Return r.json().

**Values supplied outside this operation** service or queued work from requests.get(formatted command or address in the contract).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L1671) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L964) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1589)

<a id="op-9d090225bffe29"></a>
### Parse github url

`operation_foundation_utils_change_log_business_behavior_parse_github_resource_address`

**Inputs** remote\_url.

**Declared result** (tuple at tuple(str, str) bitwise or tuple at tuple(no value, no value)).

**Explicit results** tuple(match at 1, match at 2) when match, otherwise tuple(no value, no value).

**Explicit failure paths** ValueError(“Remote URL cannot be empty”).

**Local steps**

- Bind dependencies re.
- If not remote\_url.
  - Raise ValueError(“Remote URL cannot be empty”).
- Set pattern from “github\\.com&#91;:/&#93;(.+)\\/(&#91;^\\.&#93;+)”.
- Set match from re.search(pattern, remote\_url).
- Return tuple(match at 1, match at 2) when match, otherwise tuple(no value, no value).
  - Value choice on match — true gives tuple(match at 1, match at 2), false gives tuple(no value, no value).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L1886) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L968) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1593)

<a id="op-02aac092b16ea6"></a>
### Get source url

`operation_foundation_utils_change_log_business_behavior_get_source_resource_address`

**Inputs** app.

**Declared result** (str bitwise or no value).

**Explicit results** no value · remote\_url.rstrip(“/”).

**Local steps**

- Set pyproject from get\_pyproject(app).
- If not pyproject.
  - Return no value.
- If remote\_url bound to nested operand in the contract.get(“project”, mapping()).get(“urls”, mapping()).get(“Repository”).
  - Return remote\_url.rstrip(“/”).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L2102) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L965) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1590)

<a id="op-293ac7e47f94fe"></a>
### Add message to redis

`operation_foundation_utils_change_log_business_behavior_add_message_to_cache_service`

**Inputs** update\_json.

**Record and data access** read “User” via get\_all.

**Local steps**

- Evaluate Platform.cache.set\_value(“changelog-update-info”, json.dumps(update\_json)).
- Set user\_list from list of x.name for x drawn from Platform.get\_all(“User”, filters = mapping(“enabled” → true)).
  - Draw x from Platform.get\_all(“User”, filters = mapping(“enabled” → true)).
- Set system\_managers from list of user for user drawn from user\_list where “System Manager” belongs to Platform.get\_roles(user).
  - Draw user from user\_list, keep a combination only if (“System Manager” belongs to Platform.get\_roles(user)).
- Evaluate Platform.cache.sadd(“changelog-update-user-set”, expanded system\_managers).

If control reaches the end, it returns no value.

**Values supplied outside this operation** effective access from Platform.get\_roles(user).

**Boundaries to resolve** stored data, late-bound calls, callee failures, effective access.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L2296) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L954) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1579)

<a id="op-4601b59c679f1b"></a>
### Show update popup

`operation_foundation_utils_change_log_business_behavior_show_update_popup`

**Inputs** no declared parameters.

**Wrappers, in declaration order** Platform.whitelist().

**State and service calls** msgprint with update\_message.

**Explicit results** no value.

**Local steps**

- If Platform.get\_system\_settings(“disable\_system\_update\_notification”).
  - Return no value.
- Set user from Platform.session.user.
- Set update\_info from Platform.cache.get\_value(“changelog-update-info”).
- If not update\_info.
  - Return no value.
- Set updates from json.loads(update\_info).
- Set update\_message from empty text.
- If Platform.cache.sismember(“changelog-update-user-set”, user).
  - For each update\_type in updates.
    - Set release\_links from empty text.
    - For each app in updates at update\_type.
      - Set app from Platform.\_dict(app).
      - Set security\_msg from empty text.
      - If app.security\_issues.
        - Set security\_msg from translated “Contains {0} security fixes” when app.security\_issues &gt; 1, otherwise translated “Contains {0} security fix”.
          - Value choice on app.security\_issues &gt; 1 — true gives translated “Contains {0} security fixes”, false gives translated “Contains {0} security fix”.
        - Set security\_msg from security\_msg.format(Platform.bold(app.security\_issues)).
        - Set security\_msg from formatted command or address in the contract.
      - Update release\_links using + formatted command or address in the contract.
    - If release\_links.
      - Set message from translated “New {} releases for the following apps are available”.format(translated update\_type).
      - Update update\_message using + formatted text &lt;div class='new-version-log'&gt;{message}&lt;div class='new-version-links'&gt;{release\_links}&lt;/div&gt;&lt;/div&gt;.
- Set primary\_action from no value.
- If on\_Platformcloud().
  - Set primary\_action from mapping(“label” → translated “Update from Platform Cloud”, “client\_action” → “window.open”, “args” → formatted command or address in the contract).
- If update\_message.
  - Evaluate Platform.msgprint(update\_message, title = translated “New updates are available”, indicator = “green”, primary\_action = primary\_action).
  - Evaluate Platform.cache.srem(“changelog-update-user-set”, user).

If control reaches the end, it returns no value.

**Values supplied outside this operation** configured or stored value from Platform.get\_system\_settings(“disable\_system\_update\_notification”).

**Boundaries to resolve** stored data, late-bound calls, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L2590) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L973) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1598)

<a id="op-5d321b0cf53e66"></a>
### Get pyproject

`operation_foundation_utils_change_log_business_behavior_get_pyproject`

**Inputs** app.

**Declared result** (dict bitwise or no value).

**Explicit results** no value · load(f).

**Local steps**

- Bind dependencies load.
- Set pyproject\_path from Platform.get\_app\_path(app, “..”, “pyproject.toml”).
- If not os.path.exists(pyproject\_path).
  - Return no value.
- Within open(pyproject\_path, “rb”) bound as f.
  - Return load(f).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures, file state.

[Applicable decision contract](../../../foundation-decision-contracts/part-0467.json#L3653) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L963) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1588)

## Service · Chrome pdf generator

<a id="op-071c6392c1314f"></a>
### Chrome PDFGenerator.add browser

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_add_browser`

**Inputs** self, browser.

**Local steps**

- Evaluate self.\_browsers.append(browser).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L82) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L152) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L240)

<a id="op-9568c6906f8fe4"></a>
### Chrome PDFGenerator.remove browser

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_remove_browser`

**Inputs** self, browser.

**Local steps**

- If browser belongs to self.\_browsers.
  - Evaluate self.\_browsers.remove(browser).

If control reaches the end, it returns no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L90) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L160) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L248)

<a id="op-e50423c666fb19"></a>
### Chrome PDFGenerator.new

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_new`

**Inputs** cls.

**Explicit results** cls.\_instance.

**Local steps**

- If (cls.\_instance is identical to no value or cls.\_instance.\_chromium\_process is identical to no value or cls.\_instance.\_chromium\_process.poll() is distinct from no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in cls.\_instance is identical to no value → cls.\_instance.\_chromium\_process is identical to no value → cls.\_instance.\_chromium\_process.poll() is distinct from no value.
  - Set cls.\_instance from super().\_\_new\_\_(cls).
- Return cls.\_instance.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L88) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L158) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L246)

<a id="op-67a94942387c43"></a>
### Chrome PDFGenerator.initialize

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_init`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If hasattr(self, “\_initialized”).
  - Return no value.
- Set self.\_initialized from true.
- Set self.\_browsers from list().
- Set self.\_chromium\_process from no value.
- Set self.\_chromium\_path from no value.
- Set self.\_devtools\_url from no value.
- Evaluate self.\_initialize\_chromium().

If control reaches the end, it returns no value.

**Methods declared on this owner** [initialize chromium](operations-008.md#op-d37b297a8f1d63).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L86) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L156) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L244)

<a id="op-d37b297a8f1d63"></a>
### Chrome PDFGenerator.initialize chromium

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_initialize_chromium`

**Inputs** self.

**Explicit results** no value.

**Local steps**

- If self.\_chromium\_process.
  - Return no value.
- Set site\_config from Platform.get\_common\_site\_config().
- Set self.CHROMIUM\_WEBSOCKET\_URL from site\_config.get(“chromium\_websocket\_url”, empty text).
- If self.CHROMIUM\_WEBSOCKET\_URL.
  - Evaluate Platform.warn(“Using external chromium websocket url. Make sure it is accessible.”).
  - Set self.\_devtools\_url from self.CHROMIUM\_WEBSOCKET\_URL.
  - Return no value.
- Set self.CHROME\_OPEN\_CONNECTIONS from site\_config.get(“chromium\_max\_concurrent”, 1).
- Set self.USE\_PERSISTENT\_CHROMIUM from site\_config.get(“use\_persistent\_chromium”, false).
- Set self.START\_TIMEOUT from site\_config.get(“chromium\_start\_timeout”, 10).
- Set self.debug\_mode from (Platform.conf.developer\_mode and bool(Platform.form\_dict.get(“pdf\_debug”))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in Platform.conf.developer\_mode → bool(Platform.form\_dict.get(“pdf\_debug”)).
- Set self.\_chromium\_path from find\_or\_download\_chromium\_executable().
- If self.\_verify\_chromium\_installation().
  - If not self.\_devtools\_url.
    - Evaluate self.start\_chromium\_process(debug = self.debug\_mode).

If control reaches the end, it returns no value.

**Methods declared on this owner** [verify chromium installation](operations-008.md#op-6eae014486dc99), [start chromium process](operations-008.md#op-245b0dc50086b5).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L87) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L157) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L245)

<a id="op-6eae014486dc99"></a>
### Chrome PDFGenerator.verify chromium installation

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_verify_chromium_installation`

**Inputs** self.

**Explicit results** true.

**Explicit failure paths** validation helper — formatted text Chromium not available at the specified path. Please check the path: {self.\_chromium\_path} · validation helper — formatted text Chromium not executable at {self.\_chromium\_path}.

**Local steps**

- If not os.path.exists(self.\_chromium\_path).
  - Call the validation error handler Platform.throw(formatted text Chromium not available at the specified path. Please check the path: {self.\_chromium\_path}).
- If not os.access(self.\_chromium\_path, os.X\_OK).
  - Call the validation error handler Platform.throw(formatted text Chromium not executable at {self.\_chromium\_path}).
- Return true.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L96) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L166) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L254)

<a id="op-245b0dc50086b5"></a>
### Chrome PDFGenerator.start chromium process

`operation_foundation_binding_foundation_utils_pdf_generator_chrome_pdf_generator_chromepdfgenerator_start_chromium_process`

**Inputs** self, debug = false.

**Explicit failure paths** validation helper — translated “Could not start Chromium. Check logs for details.”.

**Local steps**

- Evaluate self.\_reap\_orphaned\_chromium().
- Attempt the following.
  - If debug.
    - Set command\_args from list(“/Applications/Google Chrome.app/Contents/MacOS/Google Chrome”, “--remote-debugging-port=0”, “--user-data-dir=/tmp/chromium-{}-user-data”.format((Platform.local.site + Platform.utils.random\_string(10) ….
  - Otherwise.
    - Set command\_args from list(self.\_chromium\_path, “--remote-debugging-port=0”, “--disable-gpu”, “--in-process-gpu”, …).
  - Evaluate self.\_start\_chromium\_process(command\_args).
- On failure (Exception) bound to e.
  - Evaluate Platform.log\_error(formatted text Error starting Chromium: {e}).
  - Call the validation error handler Platform.throw(translated “Could not start Chromium. Check logs for details.”).

If control reaches the end, it returns no value.

**Methods declared on this owner** [reap orphaned chromium](operations-009.md#op-e3f841bdefc75f), [start chromium process](operations-009.md#op-688f71c98bdf61).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L93) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L163) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L251)
