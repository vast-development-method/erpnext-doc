# Record event boundaries · K

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Kenyan electronic tax reporting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer | After record creation | 1 | Details outside this boundary inventory |
| Customer | After save | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At record update | 2 | Details outside this boundary inventory |
| Customer invoice | At submission | 2 | Details outside this boundary inventory |
| Customer invoice | At update of a submitted record | 1 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 2 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Read field value · Customer invoice; Read selected rows · Customer invoice |
| Inventory movement | At submission | 1 | Details outside this boundary inventory |
| Inventory movement | Before save | 1 | Read field value · Product or service |
| Inventory movement | Before submission | 1 | Details outside this boundary inventory |
| Inventory movement | Before validation | 1 | Details outside this boundary inventory |
| Product or service | At record update | 1 | Details outside this boundary inventory |
| Product or service | At removal | 1 | Details outside this boundary inventory |
| Product or service | Before save | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Read selected rows · Item Tax Template |
| Supplier | After record creation | 1 | Details outside this boundary inventory |
| Supplier | Before save | 1 | Details outside this boundary inventory |
| Supplier | Validate record | 1 | Details outside this boundary inventory |

## Kenyan fiscal device transmission

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer | Before save | 1 | Check existence · Customer |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before save | 1 | Details outside this boundary inventory |

## Kenyan sales and workforce records

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer | Before save | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Read configuration value · Selling Settings; Read field value · Company; Read field value · Price List |
| Customer invoice | Before submission | 1 | Load or construct record · Customer |
| Dispatch note | At submission | 1 | Read configuration value · Selling Settings; Read field value · Company; Read field value · Price List |
| Goods receipt | At submission | 1 | Details outside this boundary inventory |
| Job Card | Before submission | 1 | Details outside this boundary inventory |
| Product group | Before save | 1 | Details outside this boundary inventory |
| Salary Slip | Before save | 1 | Read field value · Employee |
| Sales Order | At submission | 1 | Read configuration value · Selling Settings; Read field value · Company; Read field value · Price List |
| Sales Order | Before submission | 1 | Load or construct record · Customer |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |
