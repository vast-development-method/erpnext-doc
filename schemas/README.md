# Structured ERP specifications

Start with the [entity and field dictionary](../schema/README.md) for records in a business area, or use the [effective operation contracts](operations/current-decisions/README.md) to follow a decision. The catalogs below supply the data constraints, ordered procedures, calculations and acceptance cases behind the business workflows.

| Implementation question | Catalog |
|---|---|
| Which capabilities interact? | [Architecture map](architecture-map.json), [business capability map](business-capability-map.json) and [component responsibilities](components/README.md) |
| What can this record store, own or reference? | [Record contracts and field semantics](data/README.md). Look up its qualified entity in the [entity dictionary](../schema/index.tsv) for the applicable field layout. |
| What happens when an operation runs? | [Operation catalog](operations/README.md), [identifier lookup](operations/operation-index.json) and [decision semantics](operations/decision-semantics.json). The applicability register identifies the effective implementation. |
| What can a caller request, and what can a report return? | [Service, presentation and reporting contracts](interfaces/README.md) |
| How are amounts, dates, quantities and percentages calculated? | [Calculation contracts and worked acceptance cases](mathematics/README.md) |
| How are results interpreted and checked? | [Coverage and evidence](traceability/README.md), [qualification criteria](traceability/conformance-gates.json) and [the boundaries of the documented behavior](../docs/references/coverage-and-evidence.md) |
| Where did a statement, symbol or field binding come from? | [Source identifiers, ranges and effect inventory](operational-source-artifacts/README.md) and [source fingerprints](source-file-distribution/README.md) |

A manifest lists its entry array, ordered partitions, counts and file sizes. A fragment identifies its parent manifest. Resolve each link from the namespace identified by its catalog. Literal external names, source identifiers and digests are retained where an adapter or an evidence check requires the exact value.
