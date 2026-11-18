# Record event boundaries · P

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Pakistani accounting workspace

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | Validate record | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Details outside this boundary inventory |
| Employee | Validate record | 1 | Details outside this boundary inventory |
| Supplier | Validate record | 1 | Details outside this boundary inventory |

## Pakistani electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 2 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Read selected rows · Item Tax Template Detail |
| Point of sale invoice | At cancellation | 1 | Details outside this boundary inventory |
| Point of sale invoice | At submission | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before submission | 2 | Details outside this boundary inventory |
| Point of sale invoice | Validate record | 1 | Read selected rows · Item Tax Template Detail |

## Participant messaging and conversation retention

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After deletion | 1 | Details outside this boundary inventory |
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | After save | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At removal | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | At update of a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | At value change | 1 | Details outside this boundary inventory |
| Any eligible record | Before cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | Before record creation | 1 | Details outside this boundary inventory |
| Any eligible record | Before save | 1 | Details outside this boundary inventory |
| Any eligible record | Before submission | 1 | Details outside this boundary inventory |
| Any eligible record | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | Before validation | 1 | Details outside this boundary inventory |
| Any eligible record | Validate record | 1 | Details outside this boundary inventory |
| Contact | After record creation | 2 | Details outside this boundary inventory |
| Contact | At record update | 1 | Details outside this boundary inventory |
| Contact | At removal | 1 | Details outside this boundary inventory |
| Customer | At removal | 1 | Details outside this boundary inventory |
| File | Before save | 1 | Details outside this boundary inventory |
| Notification Log | After record creation | 1 | Details outside this boundary inventory |
| Supplier | At removal | 1 | Details outside this boundary inventory |

## Party-specific item account selection

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Validate record | 1 | Load or construct record · Customer; Load or construct record · Supplier |
| Supplier invoice | Validate record | 1 | Load or construct record · Customer; Load or construct record · Supplier |

## Payment confirmation challenges

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Bank Account | Validate record | 1 | Details outside this boundary inventory |
| Payment voucher | At load | 1 | Details outside this boundary inventory |
| Payment voucher | Validate record | 1 | Details outside this boundary inventory |

## Payment terminal transactions

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Payment voucher | Validate record | 2 | Details outside this boundary inventory |

## Payroll penalties and corrections

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Employee | At record update | 1 | Details outside this boundary inventory |
| Employee Transfer | At record update | 1 | Read field value · Employee |
| Salary Structure Assignment | At record update | 1 | Read field value · Employee |
| Shift Assignment | At record update | 1 | Read field value · Employee |

## Permission-scoped conversational assistance

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Assistant Audit Log | After record creation | 1 | Details outside this boundary inventory |
| Business assistant settings | At record update | 1 | Details outside this boundary inventory |

## Photo identification and tagging

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| File | After record creation | 1 | Details outside this boundary inventory |

## Production job scheduling

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Work Order | At value change | 1 | Load or construct record · Job Card; Read selected rows · Job Card |

## Project member and field permissions

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Assigned work item | Validate record | 1 | Details outside this boundary inventory |
| Communication | After record creation | 1 | Details outside this boundary inventory |
| Project | At record update | 1 | Details outside this boundary inventory |
| Project | At removal | 1 | Details outside this boundary inventory |
| Project | Validate record | 1 | Details outside this boundary inventory |
| User | At record update | 1 | Details outside this boundary inventory |

## Property inspections and occupancy

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Issue | Validate record | 1 | Details outside this boundary inventory |
| Key Set Detail | At value change | 1 | Details outside this boundary inventory |
| Material Request | At record update | 1 | Load or construct record · Issue; Load or construct record · Material Request (2 occurrences); Read configuration value · Global Defaults (2 occurrences); Read field value · Company (2 occurrences) |
| Material Request | At value change | 1 | Load or construct record · Issue; Load or construct record · Material Request (2 occurrences); Read configuration value · Global Defaults (2 occurrences); Read field value · Company (2 occurrences) |
| Material Request | Validate record | 1 | Load or construct record · Issue; Load or construct record · Material Request (2 occurrences); Read configuration value · Global Defaults (2 occurrences); Read field value · Company (2 occurrences) |
| Meter Reading | At submission | 1 | Details outside this boundary inventory |
| Property | Validate record | 1 | Details outside this boundary inventory |
| Sales Order | Validate record | 1 | Details outside this boundary inventory |

## Public forms and team ownership

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User | At record update | 1 | Details outside this boundary inventory |
| User Invitation | After record creation | 1 | Details outside this boundary inventory |

## Public search discovery

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Blog Post | Before save | 1 | Details outside this boundary inventory |
| Composed web page | Before save | 1 | Details outside this boundary inventory |
| Web Page | Before save | 1 | Details outside this boundary inventory |

## Purchase tax statement reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
