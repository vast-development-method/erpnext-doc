# Record event boundaries · F

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Fiscal device end-of-day records

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before save | 1 | Details outside this boundary inventory |
| Dispatch note | Before save | 1 | Details outside this boundary inventory |

## Fixed deposit management

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At cancellation | 1 | Details outside this boundary inventory |
