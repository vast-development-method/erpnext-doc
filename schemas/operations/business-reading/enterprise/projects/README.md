# Projects and time

Trace the project, task, timesheet row and cost currency through the selected controller.

[Business workflow guide](../../../../../docs/transactions/project-costing.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

382 bindings across 15 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Record · Activity cost | 3 | [validate … check unique](operations-001.md#op-8703b6cdc6991e) |
| Report · Daily timesheet summary | 4 | [execute … get conditions](operations-001.md#op-0789c7633b3fe2) |
| Report · Delayed tasks summary | 5 | [execute … get columns](operations-001.md#op-acd865efa5cf1b) |
| Record · Project | 239 | [get project accounts … by expense account](operations-001.md#op-1173ec00668ade) · [monthly … initialize](operations-002.md#op-d7d1bcbc8ad8c4) · [build … initialize](operations-003.md#op-03eb5478f3c6d4) · [build … health](operations-004.md#op-30e5ac9e6371da) · [margins … sum by](operations-005.md#op-3703d7e8cef4a5) · [work date … update costing](operations-006.md#op-5038054c4625a6) · [calculate gross margin … copy tasks](operations-007.md#op-7c73872c8cec2a) · [get projects for collect progress … summary](operations-008.md#op-d080db46222335) · [milestone … is closed](operations-009.md#op-3145176a233b38) · [can be late … percent](operations-010.md#op-8a23309eb310bd) · [today index … unbilled time logs](operations-011.md#op-f7f56d01224131) |
| Report · Project summary | 5 | [execute … get report summary](operations-011.md#op-22829e6670df39) |
| Record · Project template | 5 | [validate … get data](operations-011.md#op-a1d968c2796500) |
| Record · Project type | 1 | [on trash](operations-011.md#op-0afda22b35ec83) |
| Record · Project update | 2 | [daily reminder … email sending](operations-011.md#op-4f7da9a11f1c29) |
| Report · Project wise stock tracking | 7 | [execute … sum amount by project](operations-012.md#op-7e210926d940ba) |
| Record · Task | 50 | [get customer details … validate parent project](operations-012.md#op-82884036737dd8) · [validate project access … get project](operations-013.md#op-250d61ff8b684a) · [set multiple status … get data](operations-014.md#op-694d37a86c93cd) |
| Service · Tasks | 1 | [get context](operations-014.md#op-aed06f9a82c199) |
| Record · Timesheet | 43 | [validate … on cancel](operations-014.md#op-b420fb9fffbffa) · [on submit … get activity cost](operations-015.md#op-95c187dc5fb019) · [get activity cost … get data](operations-016.md#op-37428ae54264c2) |
| Report · Timesheet billing summary | 6 | [execute … get report summary](operations-016.md#op-e9668d7f0c8cda) |
| Record · Timesheet detail | 10 | [set to time … validate billing hours](operations-016.md#op-8bdf8f183e6f54) |
| Service · Utils | 1 | [query task](operations-016.md#op-c50d773153ee12) |
