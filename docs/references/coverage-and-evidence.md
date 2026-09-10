# Coverage and evidence

## Measured baseline

The following measures describe different kinds of evidence. They are not interchangeable completion percentages.

| Measure | Count | Meaning |
|---|---:|---|
| Source files | 12,282 | Every non-directory entry in the four uploaded archives has a pack, ordinal and content digest |
| Declared record definitions | 1,044 | Includes ordinary records, child records, settings, virtual records and explicitly classified supporting definitions |
| Declared fields | 16,813 | Includes stored fields, owned collections and presentation fields |
| Parsed server source files | 5,583 | Syntax inventory, not complete semantic interpretation |
| Server callable definitions | 33,360 | Includes inspected and uninspected operations, tests and classified excluded surfaces |
| Declared exposed operations | 1,771 | Registration inventory; caller permissions and returned data still require operation-specific contracts |
| Current-candidate exposed operations | 1,768 | Scope classification after excluding identified obsolete or supporting operations |
| Arithmetic expression candidates | 6,049 | Neutral extracted expression structures; some are nonnumeric or require surrounding context |
| Report definitions | 226 | Report metadata inventory; dynamic columns and all result branches are not certified |
| Operational metadata records | 831 | Workspaces, reports, dashboards, print and related declarations |
| Source artifacts cited by chapters | 208 | Evidence anchors for reviewed statements; a citation does not imply whole-file review |
| Reviewed mathematical contracts | 142 | Named mathematical specifications, plus separately listed ordered valuation procedures |
| Independent arithmetic checks passed | 180 | Decimal, rational or calendar examples verified without executing the source application |

The [catalog coverage file](../../schemas/traceability/catalog-coverage.json) provides structural classifications and exceptions. The [mathematics verification file](../../schemas/traceability/mathematics-verification.json) records check results. Review catalogs identify inspected spans and specific remaining work.

## How to locate evidence

A source citation has an opaque artifact identifier and a line range. Resolve its identifier in the [source distribution catalogs](../../schemas/source-file-distribution/README.md). The record gives the source pack, archive-entry ordinal and content digest. Resolve the pack through [source snapshot](../../schemas/traceability/source-snapshot.json), verify the archive digest, and select the numbered central-directory entry. Ordinals start at zero and include directory entries. Archive and file content digests use the 256-bit Secure Hash Algorithm over original bytes. Name and expression digests use that algorithm over their original text encoded in Unicode Transformation Format with eight-bit code units. Verify the selected file digest before using its one-based line range.

This keeps the blueprint's terminology independent of source product and implementation names while preserving exact evidence location. The supplied archives are required only to independently audit original evidence; they are not copied into this repository. A future implementation should work from the reviewed contracts and data definitions rather than embed those archives.

## Structural completeness

Every supplied file is inventoried. Every recognised declared record definition and its fields are represented. Independent audits check record identity collisions, field identity collisions, source-name digests, field counts, relationships and catalog shape. Every folder has navigation.

Historical migration and deployment artifacts are retained in source classification but excluded from rebuilding requirements. Supporting fixtures are not counted as production capabilities. A static current-candidate classification identifies material for review; it is not a reachability proof.

## Field conditions

The mechanical parser initially left 85 field-condition occurrences unresolved. Their 54 distinct expression digests now have manually reviewed neutral decision structures in [conditional field semantics](../../schemas/data/conditional-field-semantics.json). All 85 occurrences are covered there. These include optional child collections, every-row and any-row predicates, compound conditions and section expansion. A true section condition expands the section; it does not request collapse.

These interpretations describe form behaviour. They do not turn a visibility or required-field hint into a server validation guarantee. Other mechanically extracted trees also retain explicit warnings where truthiness, coercion or a called helper's business meaning requires context.

## Remaining conformance boundary

This repository does **not** certify that every business branch in the source has been fully specified, that all current-candidate operations are reachable, or that a replacement could already pass a complete behavioural comparison without further work. Exhaustive source inventory and substantial reviewed specifications are established; universal semantic equivalence remains unproven.

The consequential remaining work is explicit:

- Some operation and report entries provide structural contracts without fully enumerated output variants, dynamic filters, all permission paths or error conditions.
- Extracted arithmetic expressions need dimensional, precondition and side-effect review before each can become a normative mathematical contract. A syntax tree alone is insufficient.
- Client component behaviour, embedded scripts, external callback formats and provider-specific failure paths are not exhaustively executed or semantically modelled.
- Private runtime custom fields, permission changes and configuration are not present in source archives. One effective schema requires a fixed configuration profile.
- Lending and payment-gateway records referenced by supplied modules are absent from the supplied definitions. Their links are documented integration boundaries; their complete internal applications are not invented.
- Regional source logic is documented as observed behaviour, not a claim of current legal compliance in every jurisdiction.
- The supplied snapshots are development revisions. Their combined installation and all extension-order effects have not been exercised here.
- Source findings include payroll calculation discrepancies, specialised valuation and reporting questions, and background identity or permission concerns. Each review catalog records the relevant evidence and needed acceptance case.

## Execution status

No source application instance or replacement application was run as part of this specification. Source test bodies were inspected, and independent numerical examples were checked. Reference execution, end-to-end integration, concurrency, external provider behaviour and replacement conformance remain separate qualification gates.

Do not describe this repository as a certified gap-free reconstruction contract while these gates and semantic gaps remain open. New evidence should close a specific row or finding, not merely add more generated lines.
