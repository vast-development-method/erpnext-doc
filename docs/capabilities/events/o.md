# Record event boundaries · O

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Offline till reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer | After record creation | 3 | Read field value · Point of sale configuration; Read retained field value · Global Defaults |
| Customer | At record update | 2 | Details outside this boundary inventory |
| Customer | At removal | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Read record definition · Customer |
| Customer invoice | After record creation | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 2 | Details outside this boundary inventory |
| Customer invoice | At submission | 3 | Load or construct record · Loyalty Program; Read field value · Customer; Read field value · Loyalty Point Entry; Read field value · Loyalty Program |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 2 | Details outside this boundary inventory |
| Mode of Payment | After record creation | 1 | Details outside this boundary inventory |
| Mode of Payment | At record update | 1 | Details outside this boundary inventory |
| Mode of Payment | At removal | 1 | Details outside this boundary inventory |
| Point of sale configuration | At record update | 1 | Details outside this boundary inventory |
| Sales representative | Validate record | 1 | Details outside this boundary inventory |

## Online payment collection

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
