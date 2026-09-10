# Physical data catalog

The structured data catalog enumerates declared record definitions, fields, relationships, options, constraints and permission metadata from the four reference packs. It is a design input to a replacement schema, not a requirement to reproduce a particular database engine or table-name convention.

## Reading a record definition

For each definition, distinguish ordinary records, parent-owned child records, single-instance settings and virtual records. Check whether submission is supported and whether the record is a hierarchy. Inspect ordered fields, static links, dynamic links, child collections, mandatory and unique flags, precision, defaults and permission levels. Then read its domain specification for constraints imposed by controllers.

A field appearing in a form does not prove that it has a dedicated stored column. Layout fields, buttons and display-only elements serve the experience. A read-only value may still be calculated and persisted by the server. A child collection normally contributes separately owned rows rather than an array column. A dynamic link requires both the target record type and the target identifier.

## Persistence obligations

| Information | Obligation |
|---|---|
| Record identity | Stable identity with explicit uniqueness scope and rename behaviour |
| Parent membership | Valid parent type, parent identity, collection and row ordering |
| Links | Appropriate target type and valid existence or explicit permitted missing target |
| States | Preserve lifecycle separately from business, settlement and job state |
| Money | Decimal precision, currency context, rates and rounding context |
| Quantity | Unit, factor, product identity, location and serial or batch context |
| Audit | Creation and modification identities and times, revisions and consequential cancellations |
| Secrets | Protected storage and intentional exposure rules, never ordinary report output |
| Customisation | Effective schema and permission definitions active for the record |

## Constraints not captured by field flags

A mandatory field can become conditionally required under a workflow or company policy. A linked account can exist but be invalid for a company, party, currency or posting date. A quantity can be a valid number yet exceed a remaining commitment. A time interval can be well-formed yet overlap another attendance or task record. An apparently balanced journal can violate dimension requirements or a closed accounting period.

Do not interpret the catalog as a complete substitute for these controller constraints. Catalog coverage measures structural inventory. Domain review and acceptance evidence measure behavioural coverage separately.

## Index and projection design

The source includes indexes and derived records selected for its implementation. Preserve the semantic uniqueness and query requirements; choose physical indexing for the replacement workload. Queries commonly constrain company, posting date and time, voucher identity, party, account, product, warehouse, batch and lifecycle state. Ordering must be deterministic where valuation or running balances depend on event sequence.

Materialised balances must remain reconcilable to the authoritative ledger and its cancellation rules. A stock bin is an operational projection; an account balance is not a replacement for the posting records from which it is calculated.

## Identifiers and naming

Catalog identifiers use neutral full names. A collision caused by consolidating overlapping record concepts must be resolved explicitly, retaining different business responsibilities and source evidence. Original source identifier spelling is not the target database design. A separate compatibility adapter is needed if another system depends on literal original field or endpoint names.
