# Payroll and benefits

Distinguish salary structure, payroll period, calculated earning or deduction, and the accounting voucher.

[Business workflow guide](../../../../../docs/people-and-services/payroll-and-benefits.md) · [Business area](../README.md) · [How to read local paths](../../reading.md)

506 bindings across 33 records, reports and services. An operation range opens at its first binding.

| Subject | Bindings | Operation ranges |
|---|---:|---|
| Report · Accrued earnings report | 3 | [execute … get data](operations-001.md#op-8798c2a643b8b3) |
| Record · Additional salary | 16 | [before validate … get additional salaries](operations-001.md#op-9481270514f329) |
| Record · Arrear | 19 | [payroll period details … validate dates](operations-001.md#op-1d9ed45417fdd9) · [validate salary structure assignment … create benefit ledger entry](operations-002.md#op-c11656eb5ae881) |
| Report · Bank remittance | 6 | [execute … set company account](operations-002.md#op-1429d32d158244) |
| Record · Bulk salary structure assignment | 3 | [get employees … bulk assign structure](operations-002.md#op-30367a0baeae40) |
| Record · Employee benefit application | 4 | [validate](operations-002.md#op-ae2f7507c40329) · [validate max benefit … set benefit components and currency](operations-003.md#op-89350c2198ed5e) |
| Record · Employee benefit claim | 12 | [validate … get salary structure assignment](operations-003.md#op-e08f25c1ca1b0d) |
| Record · Employee benefit ledger | 5 | [validate … get benefit amount](operations-003.md#op-c9a1bfd03d77db) |
| Report · Employee ctc break up | 20 | [initialize … set salary component details](operations-003.md#op-f179aedce8981f) · [set employer contribution details … validate employee access](operations-004.md#op-f6b157c27767fb) |
| Record · Employee incentive | 3 | [validate … on submit](operations-004.md#op-29a6de7e6a9c76) |
| Record · Employee tax exemption declaration | 5 | [validate … make proof submission](operations-004.md#op-c167616cbf2dd3) |
| Record · Employee tax exemption proof submission | 4 | [validate … calculate hra exemption](operations-005.md#op-c83910c2a2ee0c) |
| Record · Employee tax exemption sub category | 1 | [validate](operations-005.md#op-c7d37e3df64bef) |
| Record · Gratuity | 22 | [validate … is experience beyond slab](operations-005.md#op-0af956467ecc0c) · [on discard … get data](operations-006.md#op-403185ae1cb265) |
| Record · Gratuity rule | 3 | [validate … get data](operations-006.md#op-bf4727f193d52b) |
| Report · Income tax computation | 28 | [execute … get hra](operations-006.md#op-06551755e9b5f7) · [get eligible hra … get fixed columns](operations-007.md#op-c7963d73b25818) |
| Report · Income tax deductions | 4 | [execute … get income tax deductions](operations-007.md#op-1ca520cdbdf65d) |
| Record · Income tax slab | 6 | [validate … apply surcharge with marginal relief](operations-007.md#op-af276cd3b710fb) |
| Record · Payroll correction | 9 | [validate … on cancel](operations-007.md#op-fab12cc2bd172d) · [fetch salary slip details … create benefit ledger entry](operations-008.md#op-6e39fee754a4f5) |
| Record · Payroll entry | 75 | [onload … get sal slip list](operations-008.md#op-6da453d4aa0f37) · [submit salary slips … process loan repayments for bank entry](operations-009.md#op-57b437acf0db73) · [set accounting entries for bank entry … create salary slips for employees](operations-010.md#op-c6f0dccd81f7f0) · [show payroll submission status … get data](operations-011.md#op-eddc4d974a43cf) |
| Record · Payroll period | 7 | [validate … get data](operations-011.md#op-8386d690076b2d) |
| Record · Payroll settings | 4 | [validate … toggle rounded total](operations-011.md#op-926d3e51f37d11) |
| Record · Retention bonus | 4 | [validate … get additional salary](operations-011.md#op-e4e8934d7fd619) |
| Service · Retention bonus | 1 | [get context](operations-011.md#op-a5a30579b402cb) |
| Record · Salary component | 10 | [before validate … update salary structures](operations-012.md#op-a49889718f1b2c) |
| Report · Salary payments based on payment mode | 8 | [execute … get chart](operations-012.md#op-ceee1bf00fe978) |
| Report · Salary payments via ecs | 4 | [execute … get data](operations-012.md#op-1ae79536e3b5ed) |
| Report · Salary register | 10 | [execute … get active parentfields](operations-012.md#op-99d6cea1cd3fbd) · [get component fieldnames … get salary slip details](operations-013.md#op-a7a85183f38efe) |
| Record · Salary slip | 134 | [initialize … create benefits ledger entry](operations-013.md#op-1f3680a3316c37) · [on cancel … calculate lwp or ppl based on leave application](operations-014.md#op-1f3736ca34cfca) · [get leave type map … add structure components](operations-015.md#op-45ba46149eae56) · [add structure component … get salary slip details](operations-016.md#op-d0d01ef72e84fa) · [get tax paid in period … get benefits details parent](operations-017.md#op-89eddf3d9f1c8a) · [unlink ref doc from salary slip … get payroll payable account](operations-018.md#op-0bdc1824e63688) |
| Record · Salary structure | 26 | [before validate … before update after submit](operations-018.md#op-95ec801cf72160) · [validate … get data](operations-019.md#op-22c3f5e9c7a467) |
| Record · Salary structure assignment | 23 | [validate … get tax component](operations-020.md#op-91085326172b51) |
| Record · Salary withholding | 12 | [validate](operations-020.md#op-2d1450630a9fa1) · [validate duplicate record … update salary withholdings](operations-021.md#op-1abad3b41680a9) |
| Service · Utils | 15 | [sanitize expression … get payroll settings for payment days](operations-021.md#op-2e72bec71794d0) · [get conditions … get years](operations-022.md#op-6fe5d15d7ba76d) |
