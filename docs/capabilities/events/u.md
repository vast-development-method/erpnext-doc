# Record event boundaries · U

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Ugandan electronic tax reporting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | Before save | 1 | Details outside this boundary inventory |
| Customer | Before save | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before save | 4 | Details outside this boundary inventory |
| Electronic invoicing settings | At record update | 1 | Details outside this boundary inventory |
| Electronic invoicing settings | Before save | 2 | Load or construct record · Company |
| Goods receipt | At submission | 1 | Details outside this boundary inventory |
| Goods receipt | Before save | 2 | Load or construct record · Product or service; Read field value · Product or service |
| Inventory count adjustment | At submission | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 1 | Details outside this boundary inventory |
| Inventory movement | Before save | 1 | Load or construct record · Goods receipt; Read field value · Product or service; Read field value · Warehouse |
| Product or service | Before save | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Details outside this boundary inventory |

## United Arab Emirates electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Read field value · Company |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Load or construct record · Company |
| Supplier invoice | At submission | 1 | Read field value · Company |
| Supplier invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | Before submission | 1 | Load or construct record · Company |

## United States payroll disbursement

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Attendance | At submission | 1 | Details outside this boundary inventory |
| Attendance | Validate record | 1 | Details outside this boundary inventory |
| Employee | Validate record | 1 | Details outside this boundary inventory |
| Payroll Entry | Before save | 1 | Details outside this boundary inventory |
| Salary Slip | After record creation | 1 | Details outside this boundary inventory |
| Salary Slip | Before save | 1 | Details outside this boundary inventory |
| Salary Slip | Before submission | 1 | Details outside this boundary inventory |
