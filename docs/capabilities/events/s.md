# Record event boundaries · S

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Saudi electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Branch | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | After record creation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 2 | Check existence · Customer invoice; Load or construct record · Company (2 occurrences); Load or construct record · Customer (2 occurrences); Load or construct record · Customer invoice; Load or construct record · Item Tax Template; Read field value · Company; Read record definition · Customer invoice (2 occurrences) |
| Customer invoice | Before cancellation | 2 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Load or construct record · Company (3 occurrences); Load or construct record · Cost Center; Load or construct record · Customer; Load or construct record · Item Tax Template |
| Customer invoice | Validate record | 1 | Load or construct record · Customer |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | Before cancellation | 1 | Details outside this boundary inventory |
| Payment voucher | Validate record | 1 | Details outside this boundary inventory |
| Point of sale invoice | After record creation | 1 | Details outside this boundary inventory |
| Point of sale invoice | At submission | 2 | Check existence · Point of sale invoice; Load or construct record · Company (4 occurrences); Load or construct record · Customer (2 occurrences); Load or construct record · Item Tax Template; Load or construct record · Point of sale configuration; Load or construct record · Point of sale invoice; Load or construct record · Sales Taxes and Charges Template; Read field value · Company; Read record definition · Point of sale invoice |
| Point of sale invoice | Before cancellation | 2 | Details outside this boundary inventory |
| Point of sale invoice | Before submission | 1 | Load or construct record · Company (3 occurrences); Load or construct record · Cost Center; Load or construct record · Customer; Load or construct record · Item Tax Template |
| Point of sale invoice | Validate record | 1 | Load or construct record · Customer |

## Saudi invoice signing credentials

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Address | Validate record | 1 | Details outside this boundary inventory |
| Company | At record update | 1 | Details outside this boundary inventory |
| Customer | At record update | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 3 | Read record definition · Customer invoice |
| Customer invoice | At submission | 3 | Load or construct record · Company; Read record definition · Customer invoice |
| Customer invoice | Before submission | 2 | Details outside this boundary inventory |
| Customer invoice | Validate record | 5 | Read record definition · Customer invoice |
| Point of sale invoice | At submission | 1 | Load or construct record · Company |
| Supplier | At record update | 1 | Details outside this boundary inventory |
| Supplier | Validate record | 1 | Details outside this boundary inventory |

## Scheduled report distribution

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After deletion | 1 | Details outside this boundary inventory |
| Any eligible record | At value change | 1 | Details outside this boundary inventory |

## Self-registration restrictions

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| User | Before record creation | 1 | Details outside this boundary inventory |
| User | Before save | 1 | Details outside this boundary inventory |

## Service desk management

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Assigned work item | At record update | 1 | Details outside this boundary inventory |
| Assignment Rule | At removal | 1 | Details outside this boundary inventory |
| Assignment Rule | Validate record | 1 | Details outside this boundary inventory |
| Comment | At removal | 1 | Details outside this boundary inventory |
| Comment | Before record creation | 1 | Details outside this boundary inventory |
| Comment | Validate record | 1 | Details outside this boundary inventory |
| Customer | After record creation | 1 | Details outside this boundary inventory |
| Customer | After renaming | 1 | Details outside this boundary inventory |
| Customer | At record update | 1 | Details outside this boundary inventory |
| Customer | At removal | 1 | Details outside this boundary inventory |
| Customer | Before renaming | 1 | Details outside this boundary inventory |
| Notification Log | Before record creation | 1 | Details outside this boundary inventory |
| Record sharing grant | After record creation | 1 | Details outside this boundary inventory |
| Record sharing grant | At record update | 1 | Details outside this boundary inventory |
| Record sharing grant | At removal | 1 | Details outside this boundary inventory |
| Record sharing grant | Before validation | 1 | Details outside this boundary inventory |
| User Permission | After record creation | 1 | Details outside this boundary inventory |
| User Permission | At record update | 1 | Details outside this boundary inventory |
| User Permission | At removal | 1 | Details outside this boundary inventory |
| User Permission | Before validation | 1 | Details outside this boundary inventory |

## Shared file workspaces

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Presentation | At record update | 1 | Details outside this boundary inventory |
| Presentation | At removal | 1 | Details outside this boundary inventory |
| User | After record creation | 1 | Details outside this boundary inventory |

## Sheet cutting and offcut reuse

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Bill of materials | Before cancellation | 1 | Details outside this boundary inventory |
| Bill of materials | Before record creation | 1 | Details outside this boundary inventory |

## Shift allocation imports

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Shift Allocation Tool | At submission | 1 | Read field value · Employee (2 occurrences) |
| Shift Allocation Tool | Before save | 1 | Read field value · Employee |

## Singapore goods and services tax

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | After record creation | 1 | Read configuration value · Global Defaults |

## Small enterprise supplier registration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Address | Validate record | 1 | Details outside this boundary inventory |
| Supplier | Validate record | 1 | Details outside this boundary inventory |

## South African filing and privacy obligations

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Company | After record creation | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Details outside this boundary inventory |
| South African filing receipt | At cancellation | 2 | Details outside this boundary inventory |
| South African filing receipt | At submission | 2 | Details outside this boundary inventory |
| South African statutory filing | At cancellation | 2 | Details outside this boundary inventory |
| South African statutory filing | At record update | 1 | Details outside this boundary inventory |
| South African statutory filing | At submission | 1 | Details outside this boundary inventory |

## Spanish value added tax register

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | Validate record | 1 | Details outside this boundary inventory |
| Customer | After record creation | 1 | Details outside this boundary inventory |
| Customer | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before identifier assignment | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Read field value · Company |
| Customer invoice | Before validation | 2 | Read field value · Account; Read retained field value · Company |
| Customer invoice | Validate record | 2 | Details outside this boundary inventory |
| Supplier | After record creation | 1 | Details outside this boundary inventory |
| Supplier | Validate record | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |
| Supplier invoice | Before submission | 1 | Read field value · Company |
| Supplier invoice | Before validation | 1 | Read field value · Account; Read retained field value · Company |
| Supplier invoice | Validate record | 1 | Details outside this boundary inventory |

## Sri Lankan accounting and tax

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | At record update | 1 | Write field value · Company |
| Customer invoice | Assign record identifier | 1 | Details outside this boundary inventory |
| Customer invoice | At removal | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Read field value · Company |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Supplier invoice | Assign record identifier | 1 | Details outside this boundary inventory |
| Supplier invoice | At removal | 1 | Details outside this boundary inventory |
| Supplier invoice | Validate record | 1 | Details outside this boundary inventory |

## Statement rule reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Bank Account | At removal | 1 | Details outside this boundary inventory |

## Stone lot picking and packing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Dispatch note | At cancellation | 1 | Load or construct record · Pick List Item; Load or construct record · Sales Order; Load or construct record · Sales Order Item; Read field value · Sales Order Item; Write field value · Pick List Item (2 occurrences); Write field value · Sales Order Item (3 occurrences) |
| Dispatch note | At submission | 1 | Load or construct record · Sales Order |
| Dispatch note | Before submission | 1 | Details outside this boundary inventory |
| Dispatch note | Before validation | 1 | Load or construct record · Sales Order; Read field value · Sales Order Item |
| Dispatch note | Validate record | 1 | Details outside this boundary inventory |
| Pick List | At cancellation | 1 | Details outside this boundary inventory |
| Pick List | At submission | 1 | Details outside this boundary inventory |
| Pick List | Before submission | 1 | Details outside this boundary inventory |
| Pick List | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Pick List | Validate record | 1 | Read field value · Product or service |
| Sales Order | At cancellation | 1 | Details outside this boundary inventory |
| Sales Order | At submission | 1 | Details outside this boundary inventory |
| Sales Order | At update of a submitted record | 1 | Details outside this boundary inventory |
| Sales Order | Before revalidating a submitted record | 1 | Details outside this boundary inventory |
| Sales Order | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Sales Order | Before validation | 1 | Details outside this boundary inventory |
| Sales Order | Validate record | 1 | Details outside this boundary inventory |

## Storage utilization and query performance

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At value change | 1 | Details outside this boundary inventory |
| Any eligible record | Before record creation | 1 | Details outside this boundary inventory |
| Any eligible record | Before validation | 1 | Details outside this boundary inventory |

## Storefront availability synchronization

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Dispatch note | At cancellation | 1 | Details outside this boundary inventory |
| Dispatch note | At submission | 1 | Details outside this boundary inventory |
| Inventory count adjustment | At cancellation | 1 | Details outside this boundary inventory |
| Inventory count adjustment | At submission | 1 | Details outside this boundary inventory |
| Inventory movement | At cancellation | 1 | Details outside this boundary inventory |
| Inventory movement | At submission | 1 | Details outside this boundary inventory |
| Product or service | After record creation | 1 | Details outside this boundary inventory |
| Product or service | At record update | 1 | Details outside this boundary inventory |
| Product price | At record update | 1 | Details outside this boundary inventory |
| Sales Order | At submission | 1 | Details outside this boundary inventory |

## Storefront tax and warehouse mapping

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Item warehouse balance | At record update | 1 | Details outside this boundary inventory |

## Structured trade invoice generation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Supplier invoice | At record update | 1 | Details outside this boundary inventory |

## Support ticket and engineering issue synchronization

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Assigned work item | After record creation | 1 | Details outside this boundary inventory |
| Assigned work item | At record update | 1 | Details outside this boundary inventory |
| Assigned work item | At removal | 1 | Details outside this boundary inventory |
| Communication | After record creation | 1 | Details outside this boundary inventory |
| Service ticket | At record update | 1 | Details outside this boundary inventory |
| Service ticket comment | After record creation | 1 | Details outside this boundary inventory |

## Swiss accounting export

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting exchange export | At submission | 1 | Details outside this boundary inventory |

## Swiss hours and tax reporting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Bank Transaction | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |

## Swiss hybrid electronic invoices

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Load or construct record · Company |
