# Shared value and file services · operations 10

[Workflow and subject index](README.md) · [How to read local paths](../../reading.md)

## Service · Collector

<a id="op-20f8d4000fe274"></a>
### Collector.add js dependencies

`operation_foundation_binding_foundation_utils_sbom_collector_collector_add_js_dependencies`

**Inputs** self, app.

**Local steps**

- For each root in \_js\_roots(app.name).
  - Set manifest from (\_read\_json((root ÷ “package.json”)) or mapping()).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_read\_json((root ÷ “package.json”)) → mapping().
  - Set lockfile from \_read\_yarn\_lock((root ÷ “yarn.lock”)).
  - Set queue from list of tuple(app, name, spec) for tuple(name, spec) drawn from manifest.get(“dependencies”, mapping()).items().
    - Draw tuple(name, spec) from manifest.get(“dependencies”, mapping()).items().
  - While queue.
    - Set tuple(dependent, name, spec) from queue.pop(0).
    - Set entry from lockfile.get(formatted text {name}@{spec}).
    - Set tuple(package, is\_new) from self.get\_js\_package(\_npm\_alias\_target(name, spec), entry, (((root ÷ “node\_modules”) ÷ name) ÷ “package.json”)).
    - Evaluate self.link(dependent, package).
    - If (entry and is\_new).
      - Evaluate in order, stop at the first false operand, otherwise use the last operand in entry → is\_new.
      - Evaluate queue.extend(generator of tuple(package, child\_name, child\_spec) for section drawn from tuple(“dependencies”, “optionalDependencies”), then tuple(child\_name, child\_spec) drawn from entry.get(section, mappi ….
        - Draw section from tuple(“dependencies”, “optionalDependencies”).
        - Draw tuple(child\_name, child\_spec) from entry.get(section, mapping()).items().

If control reaches the end, it returns no value.

**Methods declared on this owner** [get js package](operations-010.md#op-23dfd8d31941e0), [link](operations-009.md#op-518ebef4d30cdb).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L208) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L278) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L366)

<a id="op-23dfd8d31941e0"></a>
### Collector.get js package

`operation_foundation_binding_foundation_utils_sbom_collector_collector_get_js_package`

**Inputs** self, name, entry, manifest\_path.

**Declared result** tuple at tuple(Package, bool).

**Explicit results** tuple(self.packages at key, false) · tuple(self.packages at key, true).

**Local steps**

- Set version from entry.get(“version”) when entry, otherwise no value.
  - Value choice on entry — true gives entry.get(“version”), false gives no value.
- Set key from tuple(“npm”, name, version).
- If key belongs to self.packages.
  - Return tuple(self.packages at key, false).
- Set manifest from (\_read\_json(manifest\_path) or mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in \_read\_json(manifest\_path) → mapping().
- If (version and manifest.get(“version”) differs from version).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in version → manifest.get(“version”) differs from version.
  - Set manifest from mapping().
- Set tuple(download\_url, integrity) from \_yarn\_source((entry or mapping())).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry → mapping().
- Set self.packages at key from Package(ecosystem = “npm”, name = name, version = version, license = \_npm\_license(manifest), …).
- Return tuple(self.packages at key, true).

**Boundaries to resolve** callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L212) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L282) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L370)

<a id="op-65c25f376914ef"></a>
### Collector.add vendored libraries

`operation_foundation_binding_foundation_utils_sbom_collector_collector_add_vendored_libraries`

**Inputs** self, app.

**Local steps**

- For each library in json.loads(Path(\_\_file\_\_).with\_name(“vendored\_libraries.json”).read\_text()).
  - Set package from Package(ecosystem = “npm”, name = library at “name”, version = library.get(“version”), license = License(expression = library.get(“license”)), …).
  - Set self.packages at tuple(“vendored”, package.name, package.version) from package.
  - Evaluate self.link(app, package).

If control reaches the end, it returns no value.

**Methods declared on this owner** [link](operations-009.md#op-518ebef4d30cdb).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L210) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L280) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L368)

<a id="op-55c22924fff15f"></a>
### Get app

`operation_foundation_binding_foundation_utils_sbom_collector_get_app`

**Inputs** name.

**Declared result** App.

**Explicit results** App(name = name, version = getattr(importlib.import\_module(name), “\_\_version\_\_”, no value), commit = (get\_app\_last\_commit\_ref(name) or no value), repository\_url = get\_source\_url(name), …).

**Local steps**

- Set project from (get\_pyproject(name) or mapping()).get(“project”, mapping()).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_pyproject(name) → mapping().
- Return App(name = name, version = getattr(importlib.import\_module(name), “\_\_version\_\_”, no value), commit = (get\_app\_last\_commit\_ref(name) or no value), repository\_url = get\_source\_url(name), …).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in get\_app\_last\_commit\_ref(name) → no value.
  - Draw a from project.get(“authors”, list()), keep a combination only if (a.get(“name”)).

**Values supplied outside this operation** selected callable from getattr(importlib.import\_module(name), “\_\_version\_\_”, no value).

**Boundaries to resolve** late-bound calls, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L216) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L286) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L374)

<a id="op-8182d828c19f37"></a>
### Pyproject license

`operation_foundation_binding_foundation_utils_sbom_collector_pyproject_license`

**Inputs** project.

**Declared result** License.

**Explicit results** License(expression = declared, classifiers = classifiers) · License(classifiers = classifiers, text = declared.get(“text”)) · License(classifiers = classifiers).

**Local steps**

- Set declared from project.get(“license”).
- Set classifiers from tuple(generator of c for c drawn from project.get(“classifiers”, list()) where c.startswith(“License ::”)).
  - Draw c from project.get(“classifiers”, list()), keep a combination only if (c.startswith(“License ::”)).
- If isinstance(declared, str).
  - Return License(expression = declared, classifiers = classifiers).
- If isinstance(declared, dict).
  - Return License(classifiers = classifiers, text = declared.get(“text”)).
- Return License(classifiers = classifiers).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L226) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L296) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L384)

<a id="op-ca72ec8eaa8a2d"></a>
### Parse requirements

`operation_foundation_binding_foundation_utils_sbom_collector_parse_requirements`

**Inputs** specs.

**Declared result** list at Requirement.

**Explicit results** requirements.

**Local steps**

- Set requirements from list().
- For each spec in specs.
  - Within contextlib.suppress(InvalidRequirement).
    - Evaluate requirements.append(Requirement(spec)).
- Return requirements.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L224) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L294) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L382)

<a id="op-09c1a1671e26ad"></a>
### Marker matches

`operation_foundation_binding_foundation_utils_sbom_collector_marker_matches`

**Inputs** requirement, extra.

**Declared result** bool.

**Explicit results** (marker is identical to no value or marker.evaluate(mapping(“extra” → empty text))) · (marker is distinct from no value and marker.evaluate(mapping(“extra” → extra)) and not marker.evaluate(mapping(“extra” → empty text))).

**Local steps**

- Set marker from requirement.marker.
- If extra equals empty text.
  - Return (marker is identical to no value or marker.evaluate(mapping(“extra” → empty text))).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in marker is identical to no value → marker.evaluate(mapping(“extra” → empty text)).
- Return (marker is distinct from no value and marker.evaluate(mapping(“extra” → extra)) and not marker.evaluate(mapping(“extra” → empty text))).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in marker is distinct from no value → marker.evaluate(mapping(“extra” → extra)) → not marker.evaluate(mapping(“extra” → empty text)).

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L220) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L290) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L378)

<a id="op-f10bf9a038c3f8"></a>
### Python package

`operation_foundation_binding_foundation_utils_sbom_collector_python_package`

**Inputs** distribution.

**Declared result** Package.

**Explicit results** Package(ecosystem = “pypi”, name = metadata at “Name”, version = distribution.version, license = License(expression = metadata.get(“License-Expression”), classifiers = tuple(generator of c for c drawn from ….

**Local steps**

- Set metadata from distribution.metadata.
- Set tuple(repository\_url, commit) from \_vcs\_source(distribution).
- Return Package(ecosystem = “pypi”, name = metadata at “Name”, version = distribution.version, license = License(expression = metadata.get(“License-Expression”), classifiers = tuple(generator of c for c drawn from ….
  - Draw c from metadata.get\_all(“Classifier”, list()), keep a combination only if (c.startswith(“License ::”)).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in metadata.get(“Author”) → metadata.get(“Maintainer”) → metadata.get(“Author-email”) → metadata.get(“Maintainer-email”).

**Boundaries to resolve** stored data, callee failures, abbreviated operands.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L227) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L297) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L385)

<a id="op-32210b3b93fab2"></a>
### Vcs source

`operation_foundation_binding_foundation_utils_sbom_collector_vcs_source`

**Inputs** distribution.

**Declared result** tuple at tuple((str bitwise or no value), (str bitwise or no value)).

**Explicit results** tuple(no value, no value) · tuple(direct\_url.get(“url”), vcs\_info.get(“commit\_id”)).

**Local steps**

- Set direct\_url from distribution.read\_text(“direct\_url.json”).
- If not direct\_url.
  - Return tuple(no value, no value).
- Within contextlib.suppress(json.JSONDecodeError).
  - Set direct\_url from json.loads(direct\_url).
  - If vcs\_info bound to direct\_url.get(“vcs\_info”).
    - Return tuple(direct\_url.get(“url”), vcs\_info.get(“commit\_id”)).
- Return tuple(no value, no value).

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L231) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L301) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L389)

<a id="op-f6fe2eac90a2e9"></a>
### Js roots

`operation_foundation_binding_foundation_utils_sbom_collector_js_roots`

**Inputs** app.

**Declared result** list at Path.

**Explicit results** list of directory for directory drawn from tuple(app\_root, expanded sorted(app\_root.iterdir())) where (directory.is\_dir() and (directory ÷ “package.json”).exists()).

**Local steps**

- Set app\_root from Path(Platform.get\_app\_path(app, “..”)).
- Return list of directory for directory drawn from tuple(app\_root, expanded sorted(app\_root.iterdir())) where (directory.is\_dir() and (directory ÷ “package.json”).exists()).
  - Draw directory from tuple(app\_root, expanded sorted(app\_root.iterdir())), keep a combination only if ((directory.is\_dir() and (directory ÷ “package.json”).exists())).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in directory.is\_dir() → (directory ÷ “package.json”).exists().

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L218) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L288) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L376)

<a id="op-38ac3cfcff2a5a"></a>
### Read json

`operation_foundation_binding_foundation_utils_sbom_collector_read_json`

**Inputs** path.

**Declared result** (dict bitwise or no value).

**Explicit results** json.loads(path.read\_text()) · no value.

**Local steps**

- Within contextlib.suppress(FileNotFoundError, json.JSONDecodeError).
  - Return json.loads(path.read\_text()).
- Return no value.

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L228) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L298) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L386)

<a id="op-3fb10e4a777a5e"></a>
### Read yarn lock

`operation_foundation_binding_foundation_utils_sbom_collector_read_yarn_lock`

**Inputs** path.

**Declared result** dict at tuple(str, dict).

**Explicit results** parse\_yarn\_lock(path.read\_text()) · mapping().

**Local steps**

- Within contextlib.suppress(FileNotFoundError).
  - Return parse\_yarn\_lock(path.read\_text()).
- Return mapping().

**Boundaries to resolve** callee failures, file state.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L229) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L299) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L387)

<a id="op-39de2bdab74baa"></a>
### Parse yarn lock

`operation_foundation_binding_foundation_utils_sbom_collector_parse_yarn_lock`

**Inputs** text.

**Declared result** dict at tuple(str, dict).

**Explicit results** mapping() · entries.

**Local steps**

- If “# yarn lockfile v1” does not belong to text.
  - Return mapping().
- Set entries from mapping().
- Set entry from mapping().
- Set section from no value.
- For each line in text.splitlines().
  - If (not line.strip() or line.lstrip().startswith(“#”)).
    - Evaluate in order, stop at the first true operand, otherwise use the last operand in not line.strip() → line.lstrip().startswith(“#”).
    - Continue with the next iteration or loop test.
  - Set indent from (len(line) − len(line.lstrip(one space))).
  - Set line from line.strip().
  - If indent equals 0.
    - Set entry from mapping().
    - Set section from no value.
    - For each key in line.removesuffix(“:”).split(“, ”).
      - Set entries at \_unquote(key) from entry.
  - Otherwise.
    - If line.endswith(“:”).
      - Set section from entry.setdefault(line.removesuffix(“:”), mapping()).
    - Otherwise.
      - Set tuple(key, \_, value) from line.partition(one space).
      - Set tuple(key, value) from tuple(\_unquote(key), \_unquote(value)).
      - If indent equals 2.
        - Set entry at key from value.
        - Set section from no value.
      - Otherwise.
        - If section is distinct from no value.
          - Set section at key from value.
- Return entries.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L225) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L295) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L383)

<a id="op-1fab7726ab82a8"></a>
### Unquote

`operation_foundation_binding_foundation_utils_sbom_collector_unquote`

**Inputs** value.

**Declared result** str.

**Explicit results** value.removeprefix(“"”).removesuffix(“"”).

**Local steps**

- Return value.removeprefix(“"”).removesuffix(“"”).

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L230) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L300) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L388)

<a id="op-e2384181d107ff"></a>
### Npm alias target

`operation_foundation_binding_foundation_utils_sbom_collector_npm_alias_target`

**Inputs** name, spec.

**Declared result** str.

**Explicit results** target.rsplit(“@”, 1) at 0 when target.rfind(“@”) &gt; 0, otherwise target · name.

**Local steps**

- If spec.startswith(“npm:”).
  - Set target from spec.removeprefix(“npm:”).
  - Return target.rsplit(“@”, 1) at 0 when target.rfind(“@”) &gt; 0, otherwise target.
    - Value choice on target.rfind(“@”) &gt; 0 — true gives target.rsplit(“@”, 1) at 0, false gives target.
- Return name.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L221) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L291) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L379)

<a id="op-cc2965574c70ff"></a>
### Yarn source

`operation_foundation_binding_foundation_utils_sbom_collector_yarn_source`

**Inputs** entry.

**Declared result** tuple at tuple((str bitwise or no value), (str bitwise or no value)).

**Explicit results** tuple((url or no value), integrity).

**Local steps**

- Set tuple(url, \_, fragment) from (entry.get(“resolved”) or empty text).partition(“#”).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in entry.get(“resolved”) → empty text.
- Set integrity from entry.get(“integrity”).
- If (not integrity and re.fullmatch(“&#91;0-9a-f&#93;{40}”, fragment)).
  - Evaluate in order, stop at the first false operand, otherwise use the last operand in not integrity → re.fullmatch(“&#91;0-9a-f&#93;{40}”, fragment).
  - Set integrity from (“sha1-” + base64.b64encode(bytes.fromhex(fragment)).decode()).
- Return tuple((url or no value), integrity).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in url → no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L232) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L302) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L390)

<a id="op-3d103b94399f95"></a>
### Npm license

`operation_foundation_binding_foundation_utils_sbom_collector_npm_license`

**Inputs** pkg\_data.

**Declared result** License.

**Explicit results** License(text = license\_info.get(“type”)) · License(expression = license\_info) · License().

**Local steps**

- Set license\_info from pkg\_data.get(“license”).
- If isinstance(license\_info, dict).
  - Return License(text = license\_info.get(“type”)).
- If isinstance(license\_info, str).
  - Return License(expression = license\_info).
- Return License().

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L223) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L293) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L381)

<a id="op-1bba6cb2f1d2fd"></a>
### Npm author

`operation_foundation_binding_foundation_utils_sbom_collector_npm_author`

**Inputs** pkg\_data.

**Declared result** (str bitwise or no value).

**Explicit results** author · (“, ”.join(names) or no value).

**Local steps**

- Set author from pkg\_data.get(“author”).
- If isinstance(author, dict).
  - Set author from author.get(“name”).
- If author.
  - Return author.
- Set names from list().
- For each m in pkg\_data.get(“maintainers”, list()).
  - If isinstance(m, dict).
    - Set m from m.get(“name”).
  - If (m and isinstance(m, str)).
    - Evaluate in order, stop at the first false operand, otherwise use the last operand in m → isinstance(m, str).
    - Evaluate names.append(m).
- Return (“, ”.join(names) or no value).
  - Evaluate in order, stop at the first true operand, otherwise use the last operand in “, ”.join(names) → no value.

**Boundaries to resolve** late-bound calls, callee failures.

[Applicable decision contract](../../../current-decisions/foundation/procedures-0009.json#L222) · [Binding](../../../current-decisions/foundation/bindings-002.tsv#L292) · [Declaration location](../../../current-decisions/foundation/evidence/locations-002.tsv#L380)

## Service · Commands

<a id="op-ed8f92e8392cc4"></a>
### Get first party apps

`operation_foundation_utils_commands_business_behavior_get_first_party_apps`

**Inputs** no declared parameters.

**Wrappers, in declaration order** functools.lru\_cache(maxsize = 1024).

**Explicit results** apps.

**Local steps**

- Bind dependencies requests.
- Set apps from list().
- For each org in list(“Platform”, “Enterprise”).
  - Set req from requests.get(formatted command or address in the contract, mapping(“type” → “sources”, “per\_page” → 200)).
  - If req.ok.
    - Evaluate apps.extend(list of x at “name” for x drawn from req.json()).
      - Draw x from req.json().
- Return apps.

**Values supplied outside this operation** service or queued work from requests.get(formatted command or address in the contract, mapping(“type” → “sources”, “per\_page” → 200)).

**Boundaries to resolve** external or queued work, callee failures, abbreviated operands, wrapper behavior.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L5734) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1045) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1604)

<a id="op-89c297d7bace71"></a>
### Render table

`operation_foundation_utils_commands_business_behavior_render_table`

**Inputs** data.

**Local steps**

- Bind dependencies AsciiTable.
- Evaluate print(AsciiTable(data).table).

If control reaches the end, it returns no value.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L5996) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1047) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1606)

<a id="op-ec06af7f02db59"></a>
### Add line after

`operation_foundation_utils_commands_business_behavior_add_line_after`

**Inputs** function.

**Explicit results** empty\_line.

**Local steps**

- Bind local operation empty\_line for subsequent calls.
- Return empty\_line.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6072) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1041) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1600)

<a id="op-18699796eb28f2"></a>
### Add line after.empty line

`operation_foundation_utils_commands_business_behavior_add_line_after_empty_line`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** result.

**Local steps**

- Set result from function(expanded args, expanded names kwargs).
- Evaluate print().
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6188) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1042) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1601)

<a id="op-43ee6e3f129e2b"></a>
### Add line before

`operation_foundation_utils_commands_business_behavior_add_line_before`

**Inputs** function.

**Explicit results** empty\_line.

**Local steps**

- Bind local operation empty\_line for subsequent calls.
- Return empty\_line.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6280) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1043) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1602)

<a id="op-fdde35983d2463"></a>
### Add line before.empty line

`operation_foundation_utils_commands_business_behavior_add_line_before_empty_line`

**Inputs** remaining positional values args, remaining named values kwargs.

**Explicit results** result.

**Local steps**

- Evaluate print().
- Set result from function(expanded args, expanded names kwargs).
- Return result.

**Boundaries to resolve** callee failures.

[Applicable decision contract](../../../foundation-decision-contracts/part-0470.json#L6396) · [Binding](../../../current-decisions/foundation/bindings-007.tsv#L1044) · [Declaration location](../../../current-decisions/foundation/evidence/locations-007.tsv#L1603)
