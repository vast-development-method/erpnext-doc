# Marketplace source models

The [marketplace directory](../extensions/marketplace.json) identifies 398 publisher listings observed on November 18, 2026. This catalog inspects every publicly pinned listing outside the [core](../model/README.md) and the [18 curated extension profiles](../extensions/README.md). It covers 313 listings, including 101 that declare ERPNext as a dependency and another 111 with a production import, hook, record operation, customization or field link to an ERPNext record. The inspected sources provide 3,143 DocTypes, 29,401 declared non-layout fields, 4,099 custom-field contributions and 8,207 whitelisted service declarations. The [101-app directory](declared-apps.md) links each explicit dependency to its source. [Three worked integrations](integration-examples.md) trace invoice-to-payment mapping, property-specific cost center allocation and two-warehouse stock validation.

The [multilingual marketplace guides](../marketplace-guides/README.md) follow every one of the 69 rows whose original repository link lacked a verified revision. The guides add publisher manuals, attributed alternate sources, worked rebuild cases and the evidence still needed to verify each commercial release. The 398-listing declaration inventory below retains its original source basis.

## Reading the coverage

The classification uses the strongest evidence found for each listing. Every positive criterion observed also has a path, line and matched operand in that listing’s evidence map. A zero line identifies a whole declarative file. The owner of a record name is taken from the [pinned ERPNext record index](../model/record-index.json). The version column records the publisher's marketplace claim. A publisher's default branch can target a different version.

| Strongest evidence per listing | All | Lists v16 | Reader interpretation |
|---|---:|---:|---|
| Explicit ERPNext dependency | 101 | 75 | ERPNext occurs in a literal application dependency, project dependency or requirements declaration |
| ERPNext production import | 40 | 22 | A source module imports ERPNext. An optional or conditionally used integration is possible |
| ERPNext record hook | 36 | 14 | A literal record key appears in selected lifecycle, class, client or permission hook maps |
| ERPNext record operation | 25 | 12 | Source supplies the record name to a recognized document or database operation |
| ERPNext record customization | 2 | 0 | A custom field, property setter or custom permission names the ERPNext record |
| ERPNext record field link | 8 | 5 | A typed DocType field's options match an ERPNext record |
| No selected ERPNext evidence | 101 | 53 | Source inspected; dynamically resolved names, optional dependencies, other integration styles and standalone framework apps may fall here |
| Curated extension profile | 15 | 13 | A dedicated extension profile covers this listing |
| ERPNext itself | 1 | 1 | Covered by the core blueprint |
| Public revision unresolved | 69 | 14 | The marketplace lists a repository, but a public immutable source revision was unavailable |
| **Total** | **398** | **209** | Each listing occurs once |

There were 313 distinct repository names among the 313 inspected cards, corresponding to 311 distinct Git commits. Forks or renamed repositories can share Git history. Counts throughout this directory are per listing. Three selected files were skipped: the holiday and postal data fixtures exceeded the single-source size limit, and a controller in `stock_reconcialiation_per_item_group` contains inconsistent indentation. Their exact paths and reasons are recorded under `unparsed` on each directory row. The scanner traversed 55,113 regular files and selected 27,903. Third-party app installation, test execution, legal compliance, current provider interoperability and compatibility between arbitrary app combinations remain unverified by this catalog.

## Machine-readable surfaces

[Coverage](coverage.json) records the class precedence, tuple columns, declaration totals, shard filenames and SHA-256 digest of each file. [Directory rows](directory.schema.json) identify a source by marketplace ID, repository, full commit and source archive digest. [Surface rows](surfaces.schema.json) group entries by marketplace ID, kind and repository-relative file. Join the source path to `https://github.com/{repository}/blob/{revision}/{path}`; append `#L{l}` for an entry with a line. The last array in each surface row holds entries sharing the other three columns. Missing trailing columns are optional. Internal gaps are JSON nulls.

| Kind | Entries | What each entry captures |
|---|---:|---|
| Module / record | 368 / 3,143 | Named module in a module manifest; DocType name, module, child/singleton/tree/submittable/virtual flags, number of metadata fields and ERPNext link triples |
| Field / permission | 29,401 / 4,971 | Non-layout field key, type, selected constraints, permission level, link or table target, Select options; declared role, level, grant names and owner-only flag |
| Custom field / property rule / custom permission | 4,099 / 1,136 / 234 | Target record and field definition; changed property name, target and property type; imported role grants. The exact override value and conditional behavior can be read at the pinned source |
| ERPNext record operation | 8,011 | Line, framework document or database operation and statically named ERPNext record. An operation may occur inside a branch or optional integration |
| Hook | 2,016 | Hook-file assignment, literal binding path when recognized and whether the assigned value is dynamic. Nested callback entries preserve map keys in order; fixture entries retain record types |
| Service | 8,207 | Whitelisted function or class method, declaration line, argument names, literal guest or method settings and positional decorator marker. An absent setting means the source left it unspecified. Actual authorization also depends on the handler, runtime and site |
| Report / view | 605 / 305 | Report name, module, type and reference record; workspace, dashboard, print-format or workflow identifier |
| Named test / browser test file | 50,653 / 785 | Source test function or class method and line; candidate JavaScript/TypeScript files in test trees. Fixtures, generated tests and shared harness code affect these counts |

For example, from this directory, extract a single publisher's identity and inspect its SEPA order service, or list every app supplying a custom field to Sales Invoice.

```sh
jq -c '.[] | select(.id == "banking")' catalog/directory-*.json
jq -c '.[] | select(.[0] == "banking" and .[1] == "service")
  | . as [$app,$kind,$file,$entries] | $entries[] | select(.[1] == "make_sepa_payment_order")
  | {app:$app,file:$file,line:.[0],operation:.[1],arguments:.[2]}' catalog/surfaces-*.json
jq -r '.[] | select(.[1] == "custom-field") | select(any(.[3][]; .[0] == "Sales Invoice"))
  | .[0]' catalog/surfaces-*.json | sort -u
```

## Reproduction and limits

Run the [offline verifier](tools/verify.py) from this directory. It checks every shard digest and count, checks each source identity against the publisher directory, and confirms that every declaration belongs to a scanned listing.

```sh
python3 tools/verify.py
```

The [generator](tools/build.py) and [source reader](tools/inspect_archive.py) use the standard library. The published scan used Python 3.14 and curl. Python is used to parse upstream source declarations; a target implementation can consume the JSON with any runtime. The input is the sibling marketplace snapshot, curated repository list and core record index. Set a writable cache and run from this directory. For replay with all archives already present, add `--offline`. Pass `--output DIRECTORY` to generate a comparison outside this tree.

```sh
python3.14 tools/build.py --cache "${TMPDIR:-/tmp}/erp-marketplace-archives" --workers 4
python3 tools/verify.py
```

Downloads address the publisher repository and full commit. The reader checks the archive root, streams regular files as data, excludes vendored and build trees, and records parser failures. GitHub may repackage archives over time; compare the commit and recorded archive digest when reproducing an exact byte capture. Limits are 256 MiB per compressed archive, 768 MiB of regular-file contents, 120,000 regular files and 3 MiB per selected file. No app is imported, installed or executed by this inventory. Detection does not expand runtime-generated metadata, database customization, additional permissions installed at a site, decorator wrappers, arbitrary aliases or user reports. Counts of named tests describe declarations present in each repository. For example, 19,615 occur in the Jarvis repository alone.

The next stage for an app-specific implementation is to open its pinned controller and fixtures, resolve actual state transitions and privilege checks, model effects on core documents and ledgers, and establish replayable acceptance cases for each required installation and version. The [worked integrations](integration-examples.md) demonstrate this for three distinct boundaries.
