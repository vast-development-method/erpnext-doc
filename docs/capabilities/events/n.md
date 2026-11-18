# Record event boundaries · N

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Nigerian electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At submission | 1 | Details outside this boundary inventory |
| Customer | At record update | 1 | Load or construct record · Customer |
| Customer invoice | Assign record identifier | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 2 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 2 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 2 | Details outside this boundary inventory |
| Product or service | At record update | 1 | Details outside this boundary inventory |
