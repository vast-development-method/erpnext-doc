# Record event boundaries · T

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Tanzanian maintenance and inspection

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Account | After record creation | 1 | Check existence · Product group; Check existence · Product or service; Load or construct record · Product or service |
| Account | At record update | 1 | Check existence · Product group; Check existence · Product or service; Load or construct record · Product or service |
| Accounting journal voucher | Before save | 1 | Details outside this boundary inventory |
| Additional Salary | At submission | 1 | Construct new record · Accounting journal voucher |
| Additional Salary | Before validation | 1 | Details outside this boundary inventory |
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | Assign record identifier | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At load | 1 | Details outside this boundary inventory |
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At removal | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | At update of a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | At value change | 1 | Details outside this boundary inventory |
| Any eligible record | Before identifier assignment | 1 | Details outside this boundary inventory |
| Any eligible record | Before record creation | 1 | Details outside this boundary inventory |
| Any eligible record | Before save | 1 | Details outside this boundary inventory |
| Any eligible record | Before submission | 1 | Details outside this boundary inventory |
| Any eligible record | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | Before validation | 1 | Details outside this boundary inventory |
| Any eligible record | Before value change | 1 | Details outside this boundary inventory |
| Any eligible record | Validate record | 1 | Details outside this boundary inventory |
| Attendance | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 4 | Load or construct record · Customer invoice; Read field value · Account; Read field value · Company (2 occurrences); Read field value · Sales Order; Read retained field value · Product or service |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before record creation | 1 | Read field value · Point of sale configuration |
| Customer invoice | Before submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 3 | Load or construct record · Customer invoice |
| Dispatch note | At submission | 1 | Details outside this boundary inventory |
| Dispatch note | Before cancellation | 1 | Details outside this boundary inventory |
| Employee Advance | At submission | 1 | Check existence · Payment voucher |
| Employee Checkin | Validate record | 1 | Details outside this boundary inventory |
| Inventory movement | Before save | 1 | Load or construct record · Bill of materials |
| Inventory movement | Validate record | 1 | Details outside this boundary inventory |
| Landed Cost Voucher | At cancellation | 1 | Details outside this boundary inventory |
| Landed Cost Voucher | At submission | 1 | Details outside this boundary inventory |
| Landed Cost Voucher | Validate record | 1 | Details outside this boundary inventory |
| Leave Encashment | Validate record | 1 | Details outside this boundary inventory |
| Material Request | Before save | 1 | Details outside this boundary inventory |
| Open Invoice Exchange Rate Revaluation | Validate record | 1 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 1 | Load or construct record · Accounting journal voucher; Read field value · Payment voucher |
| Payment voucher | At submission | 1 | Write field value · Payment voucher |
| Payment voucher | Before submission | 2 | Load or construct record · Accounting journal voucher; Read field value · Company (2 occurrences) |
| Payment voucher | Validate record | 1 | Read retained record · Company |
| Payroll Entry | Before cancellation | 1 | Load or construct record · Accounting journal voucher |
| Payroll Entry | Before record creation | 1 | Details outside this boundary inventory |
| Payroll Entry | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Program Enrollment | At load | 1 | Details outside this boundary inventory |
| Program Enrollment | At refresh | 1 | Details outside this boundary inventory |
| Program Enrollment | At reload | 1 | Details outside this boundary inventory |
| Program Enrollment | Before submission | 1 | Details outside this boundary inventory |
| Purchase Order | Validate record | 2 | Read field value · Product price |
| Record authorization rule | Validate record | 1 | Details outside this boundary inventory |
| Salary Slip | Before record creation | 2 | Load or construct record · Employee |
| Salary Slip | Before save | 1 | Details outside this boundary inventory |
| Shift Type | Before validation | 1 | Details outside this boundary inventory |
| Student Applicant | At update of a submitted record | 1 | Read field value · Company |
| Student fee assessment | After record creation | 1 | Read field value · Company (3 occurrences) |
| Student fee assessment | At submission | 1 | Read field value · Company (3 occurrences) |
| Student fee assessment | Before cancellation | 1 | Details outside this boundary inventory |
| Student fee assessment | Before record creation | 1 | Read field value · Company (2 occurrences) |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 2 | Read field value · Account; Read field value · Company (3 occurrences); Read retained field value · Company; Write field value · Supplier invoice |
| Supplier invoice | Validate record | 1 | Details outside this boundary inventory |

## Task board rules and checklists

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | After save | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | At value change | 1 | Details outside this boundary inventory |

## Team communication channels

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At removal | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Department | After record creation | 1 | Details outside this boundary inventory |
| Department | At record update | 1 | Details outside this boundary inventory |
| Department | At removal | 1 | Details outside this boundary inventory |
| Employee | After record creation | 1 | Details outside this boundary inventory |
| Employee | At record update | 1 | Details outside this boundary inventory |
| Employee | At removal | 1 | Details outside this boundary inventory |
| User | After record creation | 1 | Details outside this boundary inventory |
| User | After renaming | 1 | Details outside this boundary inventory |
| User | At record update | 1 | Details outside this boundary inventory |
| User | At removal | 1 | Details outside this boundary inventory |

## Team communication integration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Leave Application | After record creation | 1 | Details outside this boundary inventory |
| Leave Application | At cancellation | 3 | Details outside this boundary inventory |
| Leave Application | At discard | 3 | Details outside this boundary inventory |
| Leave Application | At record update | 3 | Details outside this boundary inventory |
| Leave Application | At removal | 3 | Details outside this boundary inventory |
| Leave Application | At update of a submitted record | 1 | Details outside this boundary inventory |
| Leave Application | Before cancellation | 2 | Details outside this boundary inventory |
| Leave Application | Before updating a submitted record | 2 | Details outside this boundary inventory |
| Leave Application | Before validation | 2 | Details outside this boundary inventory |

## Team discussions and project collaboration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | At removal | 1 | Details outside this boundary inventory |
| User | After record creation | 1 | Details outside this boundary inventory |
| User | At record update | 1 | Details outside this boundary inventory |
| User | At removal | 2 | Details outside this boundary inventory |

## Technology asset management

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Address | At record update | 1 | Details outside this boundary inventory |

## Text message gateway

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Text message settings | Validate record | 1 | Details outside this boundary inventory |

## Thai accounting and tax

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At record update | 1 | Load or construct record · Customer; Load or construct record · Supplier; Read retained field value · Account |
| Accounting journal voucher | At submission | 1 | Load or construct record · Payment voucher |
| Address | At record update | 1 | Details outside this boundary inventory |
| Currency | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At removal | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before validation | 2 | Read field value · Product or service |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Expense Claim | After record creation | 1 | Details outside this boundary inventory |
| Expense Claim | At record update | 1 | Details outside this boundary inventory |
| General ledger entry | After record creation | 1 | Read retained field value · Account |
| Payment allocation reversal | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 1 | Load or construct record · Customer invoice |
| Payment voucher | At record update | 1 | Read selected rows · General ledger entry |
| Payment voucher | At submission | 2 | Load or construct record · Customer invoice |
| Payment voucher | Validate record | 1 | Details outside this boundary inventory |
| Print Format | Before validation | 1 | Details outside this boundary inventory |
| Product or service | Validate record | 1 | Read selected rows · Product or service |
| Supplier invoice | After record creation | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At record update | 1 | Details outside this boundary inventory |
| Supplier invoice | At removal | 1 | Details outside this boundary inventory |
| Supplier invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | Before validation | 2 | Read field value · Product or service |

## Till card payment reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Point of sale configuration | Validate record | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before submission | 3 | Read retained record · Point of sale configuration |
| Point of sale invoice | Validate record | 1 | Read retained record · Point of sale configuration |

## Till fiscal transaction certification

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Point of sale invoice | At submission | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before submission | 2 | Load or construct record · Point of sale configuration |
| Till fiscal certification client | After record creation | 1 | Write field value · Point of sale configuration |
| Till fiscal certification client | At record update | 1 | Write field value · Point of sale configuration |
| Till shift closing | At value change | 1 | Details outside this boundary inventory |
