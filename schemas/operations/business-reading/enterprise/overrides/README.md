# Regional rules and controller overrides

The installed capabilities and selected controller decide which override executes. Locate the base responsibility and the values passed through the override.

[Business workflow guide](../../../../../docs/runtime/extensibility-and-configuration.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

129 bindings across 10 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Report · Electronic invoice register | 1 | [execute](operations-001.md#op-c4d089f8af7757) |
| Record · Import supplier invoice | 25 | [validate … create purchase invoice](operations-001.md#op-a75d5352ba4bab) · [get country … create uom](operations-002.md#op-2174080eaf2de8) |
| Report · Irs 1099 | 7 | [execute … get street address html](operations-002.md#op-2e4c79a9942ae6) |
| Record · Lower deduction certificate | 9 | [validate … is used](operations-002.md#op-8b242a0aeeec21) |
| Service · Regional | 2 | [check deletion permission … rename vat settings](operations-002.md#op-b576d662c5c7d0) |
| Record · South africa vat settings | 5 | [validate … validate accounts](operations-002.md#op-aced728935bdd7) · [validate account](operations-003.md#op-9292845a7e40e0) |
| Report · Uae vat 201 | 31 | [execute … get standard rated expenses total](operations-003.md#op-ca0dcdab0f5de5) · [get purchase items with vat … get sales conditions](operations-004.md#op-79a68f97c2d3c8) |
| Record · Uae vat settings | 4 | [validate … validate account](operations-004.md#op-e956f1b0da2489) |
| Service · Utils | 30 | [update itemised tax data … prepare and attach invoice](operations-004.md#op-e2f02c31d4ca39) · [generate single invoice … validate returns](operations-005.md#op-07bd849d290695) |
| Report · Vat audit report | 15 | [execute … get invoice data](operations-005.md#op-3794650031456d) · [get invoice filters … get actual tax rates](operations-006.md#op-db95bfe50c9518) |
