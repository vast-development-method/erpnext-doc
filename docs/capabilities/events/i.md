# Record event boundaries · I

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Import letters of credit

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | Validate record | 1 | Read field value · Accounting journal voucher |
| Supplier invoice | At load | 1 | Details outside this boundary inventory |
| Supplier invoice | Validate record | 1 | Read field value · Supplier invoice |

## Incoming material price controls

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Goods receipt | Before submission | 1 | Details outside this boundary inventory |
| Inventory count adjustment | Before submission | 1 | Details outside this boundary inventory |
| Inventory movement | Before submission | 1 | Details outside this boundary inventory |
| Purchase Order | Before submission | 1 | Details outside this boundary inventory |
| Supplier invoice | Before submission | 1 | Details outside this boundary inventory |

## Indian identity and signature verification

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Loan Application | Before save | 1 | Details outside this boundary inventory |

## Indian payroll

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | Validate record | 1 | Details outside this boundary inventory |
| Payroll Settings | At record update | 1 | Details outside this boundary inventory |
| Payroll Settings | Validate record | 4 | Details outside this boundary inventory |
| Salary Slip | At submission | 1 | Details outside this boundary inventory |
| Salary Structure Assignment | Validate record | 1 | Details outside this boundary inventory |
| Withholding tax payment slip | At submission | 1 | Details outside this boundary inventory |
| Withholding tax return | After record creation | 1 | Details outside this boundary inventory |
| Withholding tax return | At submission | 1 | Details outside this boundary inventory |

## Indonesian tax invoice import and export

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Before cancellation | 2 | Read field value · Customer |
| Customer invoice | Before save | 1 | Read field value · Sales Taxes and Charges |
| Customer invoice | Validate record | 1 | Read field value · Sales Taxes and Charges Template (2 occurrences) |

## Installable mobile workspace

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Notification Log | After record creation | 1 | Details outside this boundary inventory |

## Invoice payment links

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 2 | Read field value · Customer invoice |
