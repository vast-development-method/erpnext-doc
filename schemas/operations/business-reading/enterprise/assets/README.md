# Asset management

Start with the asset, finance book and depreciation schedule. Distinguish changes to the asset record from posted ledger values.

[Business workflow guide](../../../../../docs/transactions/assets-and-depreciation.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

471 bindings across 15 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Asset | 153 | [validate … set missing values](operations-001.md#op-2c0873a0f347ac) · [validate finance books … has due maintenance](operations-002.md#op-8456efe8454254) · [has pending repair … get asset naming series](operations-003.md#op-58582bbbc1b9dd) · [make sales invoice … reschedule depr for updated asset](operations-004.md#op-6f0b0df1b5051a) · [create new depr schedule … notify depr entry posting error](operations-005.md#op-de18fdaf685e16) · [get comma separated links … get asset disposal values](operations-006.md#op-868b68388b9a21) · [get gross asset value … validate disposal date](operations-007.md#op-4b0c1c68628cfe) |
| Record · Asset activity | 3 | [add asset activity … has permission](operations-007.md#op-ac42e32352b558) |
| Record · Asset capitalization | 50 | [validate … validate target asset](operations-007.md#op-0fe36a9b50e8a6) · [validate consumed stock item … dispose consumed assets](operations-008.md#op-1d6afaa0714efc) · [restore consumed asset items … process fixed asset](operations-009.md#op-713a96788c327a) |
| Record · Asset category | 10 | [validate … get asset category account](operations-009.md#op-62575934b99485) |
| Record · Asset depreciation schedule | 79 | [validate … get asset shift factors map](operations-010.md#op-f8c5495f7de44c) · [get asset depreciation schedule … get last booked depreciation date](operations-011.md#op-1d097be6375c93) · [get booked depr for months count … get shift depr amount](operations-012.md#op-21bb0685c6349e) · [get asset shift factors map … get daily wdv depr amount](operations-013.md#op-1bb1070eed5a83) |
| Record · Asset maintenance | 15 | [validate … get maintenance log](operations-013.md#op-84e00b7d6e5c51) |
| Record · Asset maintenance log | 10 | [validate … validate task](operations-013.md#op-5441993776042b) · [on submit … get maintenance tasks](operations-014.md#op-617a4830e58a43) |
| Record · Asset maintenance team | 7 | [validate … get asset maintenances](operations-014.md#op-b7a9bd5981cdbf) |
| Record · Asset movement | 15 | [validate … on submit](operations-014.md#op-c9749b34d97a5d) · [on cancel … log asset activity](operations-015.md#op-fe526dc9233948) |
| Record · Asset repair | 46 | [validate … cancel stock entry](operations-015.md#op-4cfc9b5d77f233) · [after delete … get expense accounts for purchase invoice](operations-016.md#op-0c046c00170a19) · [get unallocated repair cost … get total expense amount](operations-017.md#op-088ca17f4824bb) |
| Record · Asset shift allocation | 22 | [validate … validate previous depr schedule restorable](operations-017.md#op-27cdaa2767527d) · [replace active depr schedule … get schedule rows](operations-018.md#op-63b69788939756) |
| Record · Asset shift factor | 3 | [validate … validate default](operations-018.md#op-7dd9317572e52b) |
| Record · Asset value adjustment | 24 | [validate … cancel asset revaluation entry](operations-018.md#op-31aeb7bdc1bc7b) · [update asset … get value of accounting dimensions](operations-019.md#op-7ec019a68ef5bb) |
| Report · Fixed asset register | 16 | [execute … get columns](operations-019.md#op-a280c9080d9c6f) |
| Record · Location | 18 | [validate … on trash](operations-019.md#op-7405829bfe542b) · [validate coordinates … on doctype update](operations-020.md#op-b898d6bc6cd078) |
