# Verify the rebuild evidence

Run the consolidated check from the repository root. It reads the checked-in supplement, validates its machine contracts and runs the documented offline examples. It uses Python 3.12+, `jsonschema` 4.18+ with its format dependencies, and `jq` 1.6+. The entry point and its child commands operate offline. Git and Node 24 are additional prerequisites for checking against upstream checkouts. Python and JavaScript are tools for this documentation audit. The exchange schemas and acceptance outcomes are language-neutral.

```sh
python3 -B docs/rebuild/verify/run.py
```

A successful result prints each executed check and the number of schema files, instance validations and resolved local links. A missing checker, broken reference, schema mismatch, differing expected result or explicitly requested unusable checkout produces a nonzero exit. Generated outputs are compared in memory or in temporary directories. Python bytecode caching is disabled for child processes.

## Supply local source revisions

The full source pass expects the ERPNext and Frappe checkouts at the revisions recorded in [the four-app pins](../model/pins.json). The extension directory contains one checkout per ID in [the extension profiles](../extensions/apps.json). The companion directory uses the checkout names in [the companion profiles](../companion/source-profiles.json). Tracked source files must be clean, and the checkout head must match its named revision. To verify release differences byte-for-byte, the corresponding September commits must already be available in the four Git object stores. Place those sources in sibling directories named `erpnext`, `frappe`, `extensions` and `companions`, then run this from the blueprint root.

```sh
python3 -B docs/rebuild/verify/run.py \
  --erpnext ../erpnext \
  --frappe ../frappe \
  --extensions ../extensions \
  --companions ../companions \
  --marketplace-archives ../marketplace-archives \
  --compare-model
```

| Inputs | Additional checks |
|---|---|
| Committed blueprint only | Parse every JSON artifact with duplicate-key and nonfinite-number rejection. Discover each Draft 2020-12 schema and validate its intended instances with format checking. Verify local Markdown file destinations and record the immutable upstream citations available for source comparison. |
| Committed blueprint only | Replay commercial decisions, extension examples, model observations, multi-site configuration and cross-version field fixtures, platform decision branches and the integrated stock–GL–settlement trace. Check recorded platform source outcomes against their cases. Reconcile committed live stock JUnit identities, actual platform observations, restoration receipts, trading receipts and financial reports. Compare the two observed credit-note outcomes and require the known open-item difference. |
| Committed blueprint only | Check financial journals balance, derive the monthly trial balance for every account from journal legs, and recompute the four group-currency examples. Reconcile declaration shard digests, counts, optional-app contributions, marketplace and manual indexes. |
| `--erpnext` | Execute pinned source witnesses for commercial reporting, production and valuation. Validate resolvable ERPNext source file, directory and line references. |
| `--frappe` | Validate resolvable Frappe source references. With ERPNext, execute the original stock algorithm tests, compare six observed stock movements, regenerate the source surfaces into a temporary directory, and run the independent surface reconciler. |
| `--extensions` | Validate resolvable app source references, replay the workforce/CRM decisions and execute isolated calculations and decisions across the five selected integration apps. |
| `--companions` | Replay 22 helpdesk, learning, storage, analytics and print decisions from five pinned repositories. |
| `--marketplace-archives` | Verify each inspected catalog package against its published SHA-256, then resolve remaining source links to archive members and line ranges by repository and commit. The cache uses lowercase `owner/repository/commit.tgz` paths. |
| ERPNext, Frappe, extensions and `--compare-model` | Read exact Git objects and compare every generated core model and four-app difference file byte-for-byte. |

Each `SKIP` for a source replay means the corresponding checkout arguments were omitted. A pinned GitHub location with an unavailable historical object or an unsupplied repository contributes to the reported unresolved repository/revision count. Supplying `--compare-model` makes the four historical model pins mandatory. External documentation URLs, moving branches, external pages and their availability are outside the offline link check. The source checker verifies that an immutable file or directory exists at the given commit and any cited line interval lies inside that file. Interpreting the cited business rule still requires review.

## Scope of a pass

The 43 operations examples receive schema checks in this entry point. The production and valuation suites additionally have their own optional source replays. The extension workflow integration scenarios are proposed observations. Their schema and reference checks do not execute their workflows.

The checks make different claims. Schema validation establishes input/output shape. Arithmetic and decision replays check the stated examples. Source extraction and witness runners compare selected upstream functions under their documented controlled dependencies. The cross-version comparison reports declaration differences between two explicit revisions. The marketplace audit checks a dated set of catalog facts. A declared child link, exposed operation or app integration is evidence of a surface, independent of its runtime qualification.

Use the [configured-site scenarios](../configuration/README.md) to identify site-specific evidence and the [end-to-end fixture](../integrated/README.md) for the expected account, warehouse and party outcomes. Live execution has its own [site runner](../live/run-cost-flow.py). Initializing a site, posting vouchers or contacting an external integration are separate operations from this offline audit. Any committed live observations carry their own environment, status and evidence.
