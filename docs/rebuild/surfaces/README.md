# Published and internal source surfaces

A business transaction can enter through a document method, an HTTP service, a schedule, an installed application hook, a browser action or an event emitted by another document. These declarations identify where to look for that behavior. Use the [qualification ledger](qualification.json) to see which individual gates in this inventory also carry a reviewed or executed observation.

The scan covers the complete tracked source trees of [ERPNext 16.60.0](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264) and [Frappe 16.60.1](https://github.com/frappe/frappe/tree/199a0385c00e572664a099a57a00be6ce7404eeb). The [manifest](coverage.json) lists every shard, record count, SHA-256 and source URL prefix. The table links the first shard for each family. Later numbered shards continue the same ordering.

| Declaration family | ERPNext | Foundation | What a row establishes |
|---|---:|---:|---|
| Report metadata | [194](shards/erpnext-reports-001.json) | [12](shards/frappe-reports-001.json) | Record identity, report name, reference document type, kind, roles, metadata filters/columns, options, sidecars and declared executor. The 203 standard report directories and three foundation test-fixture objects remain distinguishable by origin. |
| Remote procedure registrations | [839](shards/erpnext-rpc-001.json) | [775](shards/frappe-rpc-001.json) | Source signature or alias target, module/member binding, declared verbs or inherited default, guest flags and fixture context. |
| Transport rules | 0 | [30](shards/frappe-routes-001.json) | Path pattern, mount prefixes, endpoint and explicit verb restriction for either transport generation. Generic routes may dispatch many separately catalogued methods. |
| Manifest declarations | [582](shards/erpnext-hooks-001.json) | [472](shards/frappe-hooks-001.json) | Leaf value, selector path, list position, optional activation condition and resolved local target where available. Includes metadata and client asset declarations. |
| Scheduled actions | [46](shards/erpnext-schedules-001.json) | [42](shards/frappe-schedules-001.json) | Frequency, optional cron expression, handler, registration line and resolved implementation. All 88 named handlers resolve. |
| Server lifecycle declarations | [769](shards/erpnext-lifecycle-001.json) | [450](shards/frappe-lifecycle-001.json) | Matching method name, lexical owner, bases, controller path, fixture classification, line and association strength. |
| Literal event dispatch sites | [100](shards/erpnext-event-dispatch-001.json) | [85](shards/frappe-event-dispatch-001.json) | Calls through a document or module event dispatcher with a literal event name. Several sites can emit the same event. |
| Client form handlers | [1,607](shards/erpnext-form-handlers-001.json) | [610](shards/frappe-form-handlers-001.json) | Source record selector, event/field, registration style and location for identified form registrations and legacy assignments. |
| Public-site source assets | [12](shards/erpnext-website-assets-001.json) | [75](shards/frappe-website-assets-001.json) | Each tracked non-package-marker file under the package's website directory, including supporting assets, controllers and fixtures. |
| Named server test declarations | [7,331](shards/erpnext-server-tests-001.json) | [5,163](shards/frappe-server-tests-001.json) | Test-prefixed function or method name, containing class/function, source line and decorator names. |
| Client test source files | [5](shards/erpnext-client-test-suites-001.json) | [251](shards/frappe-client-test-suites-001.json) | Conventional suite filename or discovered legacy registration, including the foundation's standalone island verification program. |
| Client test registrations | [18](shards/erpnext-client-test-declarations-001.json) | [1,965](shards/frappe-client-test-declarations-001.json) | Parsed call site, declared or computed title and test provider spelling. Parameterized cases can produce many runtime assertions. |

### Following a source decision

To inspect a scheduled accounting action, look up the frequency and handler in the schedules shards. The group's path and entry line point to its registration. The target's project, path and line point to its implementation. Look up related record fields in the [metadata inventory](../model/INDEX.md), and use the [finance](../finance/README.md) or [platform](../platform/README.md) chapter to establish consequences and authorization. A declared schedule alone gives no assurance that the scheduler is enabled on a specific site.

For a procedure called from the browser, find its source symbol in the remote procedure shards and its endpoint pattern in the transport rules. A test-only wrapper can restrict reachability even when the listed verbs would otherwise allow the request. A standard registration without explicit verbs inherits GET, POST, PUT and DELETE from the reference decorator. A transport rule with an empty list in this catalog supplies no explicit verb filter at the route declaration. Handler admission, authentication, permissions and domain lifecycle checks remain independent. [Procedure defaults](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/__init__.py#L438-L475) · [Transport mounts](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/api/__init__.py#L91-L97)

Two ERP reports store a display report name with a trailing space while their record identity omits it. Preserve the distinct `name` and `reportName` values when joining data. A script report can also export its executor by binding a controller method at module level. The executor location then points to that binding. The set includes all 188 script report objects, alongside nine query reports and nine builder reports. Empty metadata filter/column arrays are compatible with dynamic definitions supplied by client or server code. Open the named sidecars to review their computation.

### Boundaries of evidence

- **Lifecycle.** The server event vocabulary includes the ordinary save, delete, rename, naming, print, load, discard, direct-change and record-definition hooks. Static ancestry traces 1,136 declarations to a document class. Another 50 are top-level record-definition hooks. The remaining 33 share a hook name but lack proof of dispatch from that class. Hook registrations and literal dispatch sites retain distinct identities. Runtime dispatch by a computed string requires following the caller.
- **Manifest.** Mapping keys, tuple-expanded document selectors and ordered list positions are preserved. For conditional appends, the final selector is `append` and the condition is recorded textually. Site state can alter effective registrations. The source language and signatures here are for finding evidence. They do not prescribe the implementation language of a replacement.
- **Clients.** Static registrations include the normal form registration API, object entries, explicit event argument, dynamic/spread keys and direct legacy controller function assignments. A computed key or record expression names an unresolved runtime value. Dynamically constructed scripts, inherited client controllers and effects of executing a browser bundle need a configured instance. Direct-call line hints in the suite-file index are a reading aid. Use the separately parsed registration rows to identify individual declared cases.
- **Tests.** Server test entries include 12 nested test-prefixed helper declarations and suites outside regular discovery paths. Discovery can filter, parameterize or inherit cases. A test name is an index into an upstream oracle. No pass/fail status follows from its existence. [Reference discovery](https://github.com/frappe/frappe/blob/199a0385c00e572664a099a57a00be6ce7404eeb/frappe/testing/discovery.py#L48-L68)
- **Public routes.** A checked-in website asset can be a test fixture, controller, template, script, binary file or stylesheet. Site records, generated pages, redirects, renderer hooks and installed extensions contribute additional effective routes. File presence has no implication for anonymous access.
- **Scope.** These pins describe two applications. Runtime custom reports, server scripts, site permissions, installed apps and connected services require their own site manifest. References to provider-specific code do not turn it into a bundled ERP feature. Use each business specification and its fixtures to determine which behaviors have actually been reconstructed.

### Reproduce or audit

Run from this directory using Python 3.12+, the Python `jsonschema` package and Node 24 with its bundled parser or an installed Acorn 8 parser. The following creates disposable source checkouts at the exact revisions. If those checkouts already exist, supply their paths using `--erpnext` and `--frappe` and run only the two offline checks.

```sh
set -eu
sources=$(mktemp -d)
for project in erpnext frappe; do
    case "$project" in
        erpnext) revision=886ab6ae187244e7f1b852393384ab6019d56264 ;;
        frappe) revision=199a0385c00e572664a099a57a00be6ce7404eeb ;;
    esac
    git init -q "$sources/$project"
    git -C "$sources/$project" fetch --quiet --depth=1 "https://github.com/frappe/$project.git" "$revision"
    git -C "$sources/$project" checkout --quiet --detach FETCH_HEAD
done
python3 tools/inventory.py --erpnext "$sources/erpnext" --frappe "$sources/frappe"
python3 tools/reconcile.py --erpnext "$sources/erpnext" --frappe "$sources/frappe"
```

The first check regenerates the catalog into a temporary directory and compares exact bytes. The second validates every shard against the [strict schema](shard.schema.json), checks digests and source anchors, and independently counts remote registrations and server test declarations using lexical tokens. It also reconciles standard report directories, report sidecars, native schedule definitions, hook families, client suite files, website inventory and qualified evidence references. Published groups resolve to `sources[project].base + path + "#L" + line`. For binary assets use the file URL itself. The [coverage schema](coverage.schema.json) and [qualification schema](qualification.schema.json) validate their respective manifests.
