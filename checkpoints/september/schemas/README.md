# Machine-readable specification index

Machine-readable specifications accompany the explanatory chapters. Data catalogs define records and fields; interface catalogs define public operation registration; operation catalogs supply ordered decision structures; mathematical catalogs supply quantities and financial cases; traceability catalogs state what has been checked.

[Repository overview](../README.md) · [Implementation sequence](../docs/reimplementation/sequence.md) · [Coverage and evidence](../docs/references/coverage-and-evidence.md)

## Folders

| Folder | Purpose |
|---|---|
| [Components](components/README.md) | Component contracts describe which record definitions, operations, calculations and presentation definitions contribute to each area. All linked definitions are present in this repository. Classification distinguishes production behavior, acceptance support and excluded utilities. |
| [Data](data/README.md) | The record definitions preserve ordered fields, persistence roles, defaults, value shapes, relationships and declared permissions. Shared value and condition contracts define how those declarations are interpreted. Record metadata and operation decisions must be implemented together. |
| [Interfaces](interfaces/README.md) | These catalogs connect externally callable operations and reports to the shared business specification. Read the request, response and reporting semantics before interpreting individual registration entries. Registration alone does not grant authorization. |
| [Mathematics](mathematics/README.md) | These named contracts define operands, signs, units, currencies, decision order, rounding and expected answers. Acceptance catalogs provide concrete records and events. Decimal examples establish their own arithmetic; they do not certify an unexecuted transaction engine. |
| [Operations](operations/README.md) | The operation catalogs provide semantic names, accepted bindings and ordered decision structures for 33,360 inventoried operations. Use the operation index to find an exact contract, the decision semantics to interpret its nodes, and domain chapters to understand its business purpose. Supporting checks and excluded utilities remain explicitly classified. |
| [Traceability](traceability/README.md) | Coverage and conformance catalogs separate retained inventory, specified decisions, checked examples and executed application behavior. They retain precise compatibility findings and identify the cases needed to qualify an implementation. |

## Definitions

| Entry | Contents |
|---|---|
| [Logical application architecture](architecture-map.json) | 10 components; 12 relationships. |
| [Unified enterprise business capability map](business-capability-map.json) | 36 capabilities. |
