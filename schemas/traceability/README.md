# Traceability

Use [source snapshot](source-snapshot.json) to identify the immutable packs, [catalog coverage](catalog-coverage.json) for structural measures, and review catalogs for manually inspected behaviour. Source locators count all archive entries from zero, including directories.

| Entry | Content |
|---|---|
| [Catalog coverage](catalog-coverage.json) | Structured catalog |
| [Catalog partitions](catalog-partitions.json) | Structured catalog |
| [Cross domain review](cross-domain-review.json) | Structured catalog |
| [Customer and service review](customer-and-service-review.json) | Structured catalog |
| [Financial review](financial-review.json) | Structured catalog |
| [Foundation review](foundation-review.json) | Structured catalog |
| [Inventory review](inventory-review.json) | Structured catalog |
| [Mathematics verification](mathematics-verification.json) | Structured catalog |
| [Source snapshot](source-snapshot.json) | Structured catalog |
| [Validation result](validation-result.json) | Structured catalog |
| [Workforce review](workforce-review.json) | Structured catalog |

Use the [implementation boundary](specification-baseline.json) for the responsibilities of the four capability groups and the [operation applicability register](../operations/current-decisions/README.md) to select a decision. Individual source fingerprints and execution receipts identify the input to a check. The linked calculation contracts and acceptance cases specify the expected business outcomes.

[Source value bindings](source-value-bindings.json) preserve the value fingerprints for normalized operation return shapes and registered record actions.
