# Record event boundaries · M

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Maker and checker audit reports

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |

## Malaysian electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | After record creation | 1 | Load or construct record · Customer |
| Customer invoice | After submission | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Load or construct record · Company (2 occurrences) |
| Customer invoice | At submission | 1 | Load or construct record · Company |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Supplier invoice | After submission | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Load or construct record · Company (2 occurrences) |
| Supplier invoice | At submission | 1 | Load or construct record · Company |
| Supplier invoice | Before submission | 1 | Details outside this boundary inventory |

## Metered utility and rental billing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Contract | At cancellation | 1 | Details outside this boundary inventory |
| Contract | At submission | 1 | Details outside this boundary inventory |
| Contract | At update of a submitted record | 1 | Details outside this boundary inventory |
| Contract | Before submission | 1 | Details outside this boundary inventory |
| Contract | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Contract | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before validation | 1 | Read selected rows · Sales Invoice Item |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Load or construct record · Product group |
| Recurring document schedule | At record update | 1 | Details outside this boundary inventory |
| Sales Order | Validate record | 1 | Details outside this boundary inventory |

## Mexican electronic invoice compliance

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Payment voucher | Before submission | 1 | Load or construct record · Customer invoice (2 occurrences); Read field value · Customer invoice |

## Mobile employee self-service

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | At value change | 1 | Details outside this boundary inventory |
| Any eligible record | Before cancellation | 1 | Details outside this boundary inventory |
| Comment | After record creation | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Employee Checkin | After record creation | 1 | Details outside this boundary inventory |
| Sales Order | At cancellation | 1 | Details outside this boundary inventory |
| Sales Order | At submission | 1 | Details outside this boundary inventory |

## Mobile employee workspace

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Prepared Report | At record update | 1 | Details outside this boundary inventory |

## Mobile record synchronization

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At update of a submitted record | 1 | Details outside this boundary inventory |
| Custom Field | At record update | 1 | Details outside this boundary inventory |
| Custom Field | At removal | 1 | Details outside this boundary inventory |
| Property Setter | At record update | 1 | Details outside this boundary inventory |
| Property Setter | At removal | 1 | Details outside this boundary inventory |
| Record class | At record update | 1 | Details outside this boundary inventory |

## Multiple attachment storage destinations

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| File | After record creation | 1 | Details outside this boundary inventory |
| File | At removal | 1 | Details outside this boundary inventory |
