# Record event boundaries · C

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Cargo bookings and container movements

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Sales Order | At removal | 1 | Details outside this boundary inventory |

## Carrier dispatch automation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Before submission | 1 | Load or construct record · Dispatch note |

## Carrier service and parcel booking

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Shipment | Validate record | 2 | Details outside this boundary inventory |
| Shipment Parcel Template | Validate record | 1 | Write field value · Shipment Parcel Template |

## Carrier tracking and shipment registration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Address | At removal | 1 | Details outside this boundary inventory |
| Shipment | At cancellation | 1 | Read selected rows · Customer invoice; Write field value · Customer invoice; Write field value · Shipment |

## Cheque payment runs

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | Before cancellation | 1 | Details outside this boundary inventory |
| Bank | Validate record | 1 | Details outside this boundary inventory |
| Expense Claim | Before cancellation | 1 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 2 | Load or construct record · Payment Schedule; Read field value · Sales Taxes and Charges; Read selected rows · Payment Schedule; Write field value · Payment Schedule (3 occurrences); Write field value · Sales Taxes and Charges |
| Payment voucher | At submission | 3 | Load or construct record · Payment Schedule; Read field value · Mode of Payment; Read field value · Sales Taxes and Charges; Read selected rows · Payment Schedule; Write field value · Bank Account; Write field value · Payment Schedule (3 occurrences); Write field value · Sales Taxes and Charges |
| Payment voucher | Validate record | 1 | Read field value · Mode of Payment; Read selected rows · Payment voucher |
| Supplier invoice | Before cancellation | 1 | Details outside this boundary inventory |

## Collaborative diagramming

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| File | After record creation | 1 | Details outside this boundary inventory |
| Record sharing grant | Validate record | 1 | Details outside this boundary inventory |

## Collaborative document spaces

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Project | After record creation | 1 | Details outside this boundary inventory |
| Project | At record update | 1 | Details outside this boundary inventory |
| Project | At removal | 1 | Details outside this boundary inventory |

## Collaborative knowledge publishing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Knowledge article | At record update | 1 | Details outside this boundary inventory |
| Knowledge article | At removal | 1 | Details outside this boundary inventory |
| Knowledge workspace | At record update | 1 | Details outside this boundary inventory |
| Knowledge workspace | At removal | 1 | Details outside this boundary inventory |
| User | After record creation | 1 | Details outside this boundary inventory |

## Congregational care and events

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Address | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At removal | 3 | Details outside this boundary inventory |
| Any eligible record | Before cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | Before renaming | 1 | Details outside this boundary inventory |
| Any eligible record | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | Validate record | 2 | Details outside this boundary inventory |
| Assigned work item | After record creation | 1 | Details outside this boundary inventory |
| Assigned work item | Validate record | 1 | Details outside this boundary inventory |
| Care Request | After record creation | 1 | Details outside this boundary inventory |
| Care Request | At record update | 1 | Details outside this boundary inventory |
| Care Request | At removal | 1 | Details outside this boundary inventory |
| Communication | After record creation | 1 | Details outside this boundary inventory |
| Connection Card Photo | After record creation | 1 | Details outside this boundary inventory |
| Delegated access client | Before record creation | 1 | Details outside this boundary inventory |
| Delegated access token | After record creation | 1 | Details outside this boundary inventory |
| Email Unsubscribe | After record creation | 1 | Details outside this boundary inventory |
| Event participant arrival | After record creation | 1 | Details outside this boundary inventory |
| Event registration | At record update | 1 | Details outside this boundary inventory |
| File | Before record creation | 1 | Details outside this boundary inventory |
| Flow Knowledge Source | Validate record | 1 | Details outside this boundary inventory |
| Flow Model | At record update | 1 | Details outside this boundary inventory |
| Flow Model | Validate record | 1 | Details outside this boundary inventory |
| Flow Session | Before record creation | 1 | Details outside this boundary inventory |
| Flow Trigger | Before validation | 1 | Details outside this boundary inventory |
| Follow-up Card | After record creation | 1 | Details outside this boundary inventory |
| Group | At removal | 1 | Details outside this boundary inventory |
| Notification Log | After record creation | 1 | Details outside this boundary inventory |
| Person | At removal | 1 | Details outside this boundary inventory |
| Personal Data Deletion Request | At value change | 1 | Details outside this boundary inventory |
| Prayer Request | After record creation | 1 | Details outside this boundary inventory |
| Prayer Request | At record update | 1 | Details outside this boundary inventory |
| Prayer Request | At removal | 1 | Details outside this boundary inventory |
| Record sharing grant | Validate record | 1 | Details outside this boundary inventory |
| System Settings | Validate record | 1 | Details outside this boundary inventory |
| User | After record creation | 1 | Details outside this boundary inventory |
| User | At record update | 2 | Details outside this boundary inventory |
| User | At removal | 1 | Details outside this boundary inventory |
| User | Validate record | 1 | Details outside this boundary inventory |
| Web Form | At record update | 1 | Details outside this boundary inventory |
| Web Form | At removal | 1 | Details outside this boundary inventory |
| Web Form Request | At record update | 1 | Details outside this boundary inventory |
| Web Form Request | Validate record | 1 | Details outside this boundary inventory |
| Web Page | At record update | 2 | Details outside this boundary inventory |
| Web Page | At removal | 2 | Details outside this boundary inventory |

## Construction quantities and budgets

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before record creation | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Goods receipt | At cancellation | 1 | Details outside this boundary inventory |
| Goods receipt | At submission | 1 | Details outside this boundary inventory |
| Goods receipt | Before record creation | 1 | Details outside this boundary inventory |
| Inventory movement | At cancellation | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 1 | Details outside this boundary inventory |
| Inventory movement | Before record creation | 1 | Details outside this boundary inventory |
| Project | After record creation | 2 | Load or construct record · Project Template |
| Project | At record update | 1 | Details outside this boundary inventory |
| Purchase Order | At cancellation | 1 | Details outside this boundary inventory |
| Purchase Order | At record update | 1 | Details outside this boundary inventory |
| Purchase Order | At submission | 1 | Details outside this boundary inventory |
| Purchase Order | Before record creation | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At record update | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |
| Supplier invoice | Before record creation | 1 | Details outside this boundary inventory |
| Task | At record update | 1 | Check existence · Quality Inspection |
| Timesheet | At cancellation | 1 | Details outside this boundary inventory |
| Timesheet | At record update | 1 | Details outside this boundary inventory |
| Timesheet | At submission | 1 | Details outside this boundary inventory |

## Contract dues and settlement

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Contract | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Load or construct record · Customer |
| Payment voucher | At record update | 1 | Details outside this boundary inventory |
| Supplier invoice | Validate record | 1 | Load or construct record · Supplier |

## Contribution points and reviews

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At value change | 1 | Details outside this boundary inventory |
| User | At removal | 1 | Details outside this boundary inventory |

## Control evidence and risk assessment

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At cancellation | 1 | Details outside this boundary inventory |
| Accounting journal voucher | At submission | 1 | Details outside this boundary inventory |
| Control Activity | After record creation | 1 | Details outside this boundary inventory |
| Control Activity | At record update | 1 | Details outside this boundary inventory |
| Control Activity | At removal | 1 | Details outside this boundary inventory |
| Control Activity | Validate record | 1 | Details outside this boundary inventory |
| Control Evidence | After record creation | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Deficiency | At record update | 1 | Details outside this boundary inventory |
| Deficiency | Validate record | 1 | Details outside this boundary inventory |
| Inventory movement | At cancellation | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Purchase Order | At cancellation | 1 | Details outside this boundary inventory |
| Purchase Order | At submission | 1 | Details outside this boundary inventory |
| Risk Register Entry | After record creation | 1 | Details outside this boundary inventory |
| Risk Register Entry | At record update | 1 | Details outside this boundary inventory |
| Risk Register Entry | Validate record | 1 | Details outside this boundary inventory |
| Sales Order | At cancellation | 1 | Details outside this boundary inventory |
| Sales Order | At submission | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |
| Test Execution | After record creation | 1 | Details outside this boundary inventory |
| Test Execution | At record update | 1 | Details outside this boundary inventory |
| Test Execution | At submission | 1 | Details outside this boundary inventory |
| Test Execution | Before cancellation | 1 | Details outside this boundary inventory |
| Test Execution | Validate record | 1 | Details outside this boundary inventory |

## Controlled credential sharing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Email Template | At removal | 1 | Details outside this boundary inventory |
| Email Template | Validate record | 1 | Details outside this boundary inventory |
| Vault Secret | After record creation | 1 | Details outside this boundary inventory |
| Vault Secret | At record update | 1 | Details outside this boundary inventory |
| Vault Secret | At removal | 1 | Details outside this boundary inventory |
| Vault Share | After record creation | 1 | Details outside this boundary inventory |
| Vault Share | At removal | 1 | Details outside this boundary inventory |

## Controlled external file distribution

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| File | After record creation | 1 | Details outside this boundary inventory |
| File | At removal | 1 | Details outside this boundary inventory |

## Conversation history and usage

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At load | 1 | Details outside this boundary inventory |
| Accounting journal voucher | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At load | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Purchase Order | At load | 1 | Details outside this boundary inventory |
| Purchase Order | Validate record | 1 | Details outside this boundary inventory |
| Sales Order | At load | 1 | Details outside this boundary inventory |
| Sales Order | Validate record | 1 | Details outside this boundary inventory |
| Supplier invoice | At load | 1 | Details outside this boundary inventory |
| Supplier invoice | Validate record | 1 | Details outside this boundary inventory |

## Conversational business record lookup

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Employee | At record update | 1 | Read field value · Company; Read record definition · Employee |

## Conversational messaging rules

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Business message | After record creation | 1 | Details outside this boundary inventory |

## Counterparty due diligence

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Quotation | At submission | 1 | Details outside this boundary inventory |

## Customer messaging contacts

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Business message | After record creation | 1 | Details outside this boundary inventory |
