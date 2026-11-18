# Coverage and evidence

This specification supplies its record definitions, decision structures, mathematical rules and acceptance examples directly. Internal links resolve to definitions contained in the repository. An unavailable file, archive position, digest or source-line range is never needed to obtain the meaning of a rule.

## Measured coverage

| Measure | Count | Interpretation |
|---|---:|---|
| Classified components | 12,282 | Contributions linked to local records, decisions, calculations and presentation definitions |
| Record definitions | 1,044 | Independent records, owned children, settings, virtual records and explicitly classified supporting definitions |
| Declared fields | 16,813 | Stored scalar fields, owned collections, protected values, presentation fields and virtual calculations |
| Record relationships | 3,820 | Fixed targets, dynamic targets and owned child references |
| Conditional field rules | 2,818 | Conditions with explicit evaluation semantics and meaningful identities |
| Record behavior bindings | 1,042 | Shared and record-specific lifecycle bindings |
| Ordered operation contracts | 33,360 | Operation parameters, ordered branches, values, loops, failures and completion structures |
| Exposed operation registrations | 1,771 | Public registration and binding facts with linked operation contracts |
| Calculation expression candidates | 6,049 | Explicit expressions linked to their enclosing decisions; dimensional review is separately identified |
| Report definitions | 226 | Report registration, filters, columns and projection contracts |
| Conditional report column definitions | 1,609 | Columns defined by concrete report branches and their conditions |
| Report filter definitions | 1,119 | Filter shapes, choices and defaults, including 556 parsed defaults |
| Operational presentation definitions | 831 | Reports, workspaces, dashboards, forms and related projections |

The [coverage catalog](../../schemas/traceability/catalog-coverage.json) records scope classifications, storage categories and exact mathematical catalog counts. The [validation result](../../schemas/traceability/validation-result.json) records repository-wide integrity checks. Supporting checks and excluded utilities are not counted as additional production capabilities.

## Meaning of the decision catalogs

The [operation index](../../schemas/operations/operation-index.json) locates each complete ordered decision entry. Every previously inventoried operation was matched to a definition before translation. Its data structures preserve predicates, branch ordering, assignments, iteration, errors, handlers, resource cleanup, explicit completion and declared context. The [decision interpretation](../runtime/decision-contract-interpretation.md) defines how these structures must be read.

This is a substantial increase in accessible information. It is also a specifically bounded claim: a structural translation is not an independently executed replacement, and a helper name alone does not prove every dynamic capability has been resolved. Domain chapters and the named mathematical contracts explain the consequential business meaning; effective configuration, wrappers, permissions and external counterpart behavior are part of a complete conformance profile.

## Data preservation and semantic repairs

All 1,044 record definitions and 16,813 fields were compared with the previous catalog, including identity, field order and relationship targets. The repair added typed value constraints, default semantics, naming rules, conditional presentation meaning and explicit optional-counterpart shapes. It recovered meaningful omitted help and configuration values.

The review also corrected specific catalog defects: empty strings and punctuation had been replaced with the word “unnamed”; collection removal had been misinterpreted as a mail protocol; annotation alternatives had been represented as bitwise arithmetic. These are corrected interpretation errors, not changes to the intended business decision. Per-record canonical field names are retained where a global shorthand would collide with another field.

## Verified examples

The [mathematics verification register](../../schemas/traceability/mathematics-verification.json) distinguishes independent arithmetic, isolated decision invocation and historical reported checks. Current runs checked balanced accounting events, expected account balances, foreign-currency settlements, depreciation, stock valuation, packaging, workforce calculations, customer/service calculations and cross-domain conservation.

The same example may appear in a domain check and in a cross-domain reconciliation. Those are overlapping checks, not additive measures of feature completion. Isolated invocations used controlled substitutes for their surrounding context and, where stated, numeric helpers. Their successful results must not be reported as complete application execution.

## Compatibility findings

Named [review registers](../../schemas/traceability/README.md) preserve precise findings such as inconsistent hold-release predicates, payroll attendance/leave differences, employer-contribution posting boundaries, asset reversal signs and regional import behavior. Each finding explains the actual decision and the required acceptance outcome or explicit correction decision. A reader does not need the original implementation to understand the issue.

An observed anomaly and a proposed corrected behavior are separate contracts. A replacement must declare which compatibility profile it implements and test the chosen result. Industry convention cannot silently overwrite a documented branch.

## Conformance boundary

The [conformance register](../../schemas/traceability/conformance-gates.json) defines qualification gates for integrated transactions, identity and permission enforcement, concurrency, duplicate delivery, recovery, external counterpart behavior and operational reconciliation. Application gates remain unassessed until a concrete implementation is run against them.

Optional lending and payment-provider internals are external boundaries with [required record contracts](../../schemas/data/external-record-contracts.json). Runtime customizations and dynamic presentation require an effective configuration profile. Regional behavior requires the applicable counterpart version and jurisdictional policy. These dependencies are explicitly bounded rather than supplied through guessed rules.

No complete reference application installation or replacement application was executed during this specification work. The repository therefore does not assert universal behavioral equivalence or enterprise certification. It provides the contracts, checked examples, known compatibility decisions and measurable gates needed to establish those claims honestly.
