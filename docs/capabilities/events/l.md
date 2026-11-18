# Record event boundaries · L

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Ledger and tax mapping synchronization

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Account | At record update | 1 | Load or construct record · Account; Write field value · Account |
| Accounting journal voucher | At cancellation | 1 | Details outside this boundary inventory |
| Accounting journal voucher | At submission | 1 | Details outside this boundary inventory |
| Customer | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Product or service | At record update | 1 | Load or construct record · Product or service |
| Purchase Order | At submission | 1 | Details outside this boundary inventory |
| Quotation | At submission | 1 | Details outside this boundary inventory |
| Supplier | At record update | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |

## Livestock activity and valuation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Assigned work item | At removal | 1 | Details outside this boundary inventory |
| Assigned work item | Validate record | 1 | Details outside this boundary inventory |
| Batch | Before save | 1 | Details outside this boundary inventory |
| Batch | Validate record | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 1 | Load or construct record · Batch |
| Inventory movement | Before save | 1 | Read field value · Company |
| Product or service | Validate record | 1 | Details outside this boundary inventory |
