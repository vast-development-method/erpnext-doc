# Physical data catalog

The [logical schema directory](../../schema/README.md) defines records, fields, relationships, options and access declarations. Use the rules below when mapping those logical definitions to storage.

## Reading a record definition

For each definition, distinguish ordinary records, parent-owned child records, single-instance settings and virtual records. Check whether submission is supported and whether the record is a hierarchy. Inspect ordered fields, static links, dynamic links, child collections, mandatory and unique flags, precision, defaults and permission levels. Then read its domain specification for transaction-level constraints.

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

Do not interpret the catalog as a complete substitute for these transaction constraints. Catalog coverage measures structural inventory. Domain review and acceptance evidence measure behavioural coverage separately.

## Index and projection design

Preserve uniqueness and required query outcomes. Index selection depends on the workload. Frequent lookups select by company, posting date, party, account, warehouse, product, voucher, line identity or lifecycle state.

Materialised balances must remain reconcilable to the authoritative ledger and its cancellation rules. A stock bin is an operational projection; an account balance is not a replacement for the posting records from which it is calculated.

## Identifiers and naming

An entity name identifies its business purpose. Two records with the same display label may carry different responsibilities. Preserve each identity and the business events it controls.

## Schema construction procedure

1. Resolve the complete effective record definition, including custom fields and property overrides. Identify its storage family before allocating any physical table.
2. Add the common record envelope from [common record attributes](../model/README.md). Retain record-type-scoped identity, structural state, ownership, and modification information.
3. Classify every declared field as a stored scalar, fixed reference, dynamic reference, owned collection, computed value, or presentation control. Only stored fields contribute ordinary scalar persistence.
4. For each collection, create the ownership relationship using parent identity, parent type, parent collection, child identity, and row position. A parent identifier by itself is insufficient.
5. Resolve target types for references, and pair dynamic references with their selector fields. Decide how runtime additions are published before permitting transactions that use them.
6. Apply declared uniqueness, requiredness, range, and numeric precision independently. A field's requiredness does not imply that zero is invalid, and storage nullability does not determine whether a domain operation accepts a missing value.
7. Add domain constraints such as account/company consistency, permitted posting dates, compatible currencies, and remaining quantities through the owning operation. A database foreign key alone cannot express them.
8. Build indexes from observed query and ordering requirements. Indexes that accelerate lookups must not silently introduce additional business uniqueness.
9. Prove a round trip for draft, submitted, cancelled, singleton, child, dynamic-reference, and computed records. The same logical result must be obtained after storage and reload.

## Common storage families

| Family | Logical key | Value and integrity rules |
| --- | --- | --- |
| Ordinary business record | Tenant, record type, record identifier | One current root record plus separately retained history where enabled |
| Child record | Tenant, child type, child identifier | Ownership tuple resolves one parent collection; row position orders membership |
| Singleton setting | Tenant, setting type | One logical settings object; absence can resolve declared defaults |
| Fixed reference | Target type and identifier within tenant | Resolve existence and domain validity; maintain reference on an authorized rename |
| Dynamic reference | Selector field's target type and reference value | Neither half can be interpreted independently |
| Protected secret | Tenant, record type, record identity, field identity | Masked display and protected value are distinct representations |
| Hierarchy | Record identity and parent relationship | Keep ancestry valid; derived traversal boundaries are rebuildable indexes |
| Financial journal fact | Entry identity with voucher and dimensions | Preserve debit, credit, currency, posting order, and cancellation relationships |
| Operational balance | Product/location or other declared aggregation key | Reconcile to qualifying facts; never substitute it for retained history |

## Nullability and uniqueness example

Consider an optional unique external reference. Two records with no external reference must not collide merely because each displays an empty input. The normal persistence normalization turns blank unique values into absence. Two records with the same meaningful external reference must fail uniqueness according to the selected comparison rules. Whitespace-only text is blank for this normalization, while an ordinary nonunique text field is not automatically trimmed and erased. The precise coercion table is in [persistence identity and values](../services/persistence-identity-and-values.md#absence-empty-values-and-normalization).

Identifier comparison, collation, and maximum lengths are explicit compatibility decisions. Case-insensitive reference lookup can return a stored identity whose letter case differs from the input; the document's link value is normalized to that stored identity. A replacement using case-sensitive identity must provide a deliberate compatibility mapping or document the changed behavior. Do not derive target identity from a translated display label.

## Query and reconciliation obligations

The following queries must return equivalent business records even when their physical indexes differ: all rows owned by one parent collection; a document and its submitted descendants; entries for a voucher; account movements through a cut-off; stock movements in valuation order; all party allocations for an obligation; a hierarchy's descendants; and permission-filtered list/count pairs. Rebuild projected balances and compare them to retained movements after ordinary posting, cancellation, backdated posting, and restoration.

The [entity and relationship dictionaries](../../schema/README.md) describe individual data structures. The calculation catalog specifies business precision and rounding rules.
