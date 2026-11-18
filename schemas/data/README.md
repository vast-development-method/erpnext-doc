# Data

The record definitions preserve ordered fields, persistence roles, defaults, value shapes, relationships and declared permissions. Shared value and condition contracts define how those declarations are interpreted. Record metadata and operation decisions must be implemented together.

[Parent index](../README.md)

## Folders

| Folder | Purpose |
|---|---|
| [Conditional field rules](conditional-field-rules/README.md) | Related definitions and their complete navigation index. |
| [Numeric field catalog](numeric-field-catalog/README.md) | Related definitions and their complete navigation index. |
| [Record behavior bindings](record-behavior-bindings/README.md) | Related definitions and their complete navigation index. |
| [Record type index](record-type-index/README.md) | Related definitions and their complete navigation index. |
| [Record types](record-types/README.md) | Each file defines one named record and every declared field in order. Field contracts distinguish scalar persistence, owned child collections, protected values, presentation-only fields and virtual calculations. Common record attributes and lifecycle rules apply in addition to the fields declared here. |
| [Relationship catalog](relationship-catalog/README.md) | Related definitions and their complete navigation index. |

## Definitions

| Entry | Contents |
|---|---|
| [Common record attributes](common-record-attributes.json) | 11 attributes; 4 storage rules. |
| [Conditional field rules](conditional-field-rules.json) | Manifest for 2,818 rules in 11 ordered parts. |
| [Conditional field semantics](conditional-field-semantics.json) | Resolve every condition occurrence that the structural catalogue parser could not parse, without carrying executable source expressions into this specification. |
| [External record contracts](external-record-contracts.json) | Minimal consumed shapes for optional services whose complete record definitions are outside the integrated record inventory. The contracts preserve local callers and r… |
| [Numeric field catalog](numeric-field-catalog.json) | Manifest for 2,053 fields in 5 ordered parts. |
| [Record behavior bindings](record-behavior-bindings.json) | Manifest for 1,042 bindings in 3 ordered parts. |
| [Record type index](record-type-index.json) | Manifest for 1,044 record types in 2 ordered parts. |
| [Record type specification](record-type.schema.json) | 10 required. |
| [Record value semantics](record-value-semantics.json) | Define value normalization, validation, ownership, precision, and option comparison for all record-type and field contracts without relying on unavailable implementati… |
| [Relationship catalog](relationship-catalog.json) | Manifest for 3,820 relationships in 7 ordered parts. |

## Record identity and source bindings

Use the [entity dictionary](../../schema/README.md) for the applicable business record, effective layout, access grants and configured overrides. These detailed definitions add ordered fields, persistence behavior, naming, conditions and source bindings. The source field ordinal identifies a field across neutral identifier spellings. A `source_identifier` or `source_name` on a row preserves a second spelling of the same record or field.

Each detailed record has an applicability entry. Of the 1,044 described layouts, 1,028 resolve to effective declarations, 14 describe optional or compatibility layouts, and two are sample records used for acceptance. The [entity cross-reference](../../docs/rebuild/coverage-review/entity-cross-reference.tsv) links each business entity to its exact declaration. For fields marked `effective_field_properties_in_declaration`, read the named field in that declaration for the listed properties. Among fields on the 1,028 declared records, 666 have changed declaration properties, 155 are retained [compatibility fields](../../docs/rebuild/coverage-review/compatibility-fields.tsv), and 128 are absent from the effective declaration.
