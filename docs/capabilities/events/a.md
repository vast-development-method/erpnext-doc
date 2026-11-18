# Record event boundaries · A

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Account balance feed reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Bank Transaction | At removal | 1 | Details outside this boundary inventory |

## Accounting system synchronization

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer | At record update | 1 | Details outside this boundary inventory |
| Customer invoice | After record creation | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Write field value · Customer invoice (2 occurrences) |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | After record creation | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Write field value · Supplier invoice |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |

## Administrative account access restrictions

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| System Settings | Validate record | 1 | Details outside this boundary inventory |

## Advertising lead capture

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Lead | Validate record | 1 | Details outside this boundary inventory |

## Analytical reporting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Record sharing grant | Validate record | 1 | Details outside this boundary inventory |
| User | At removal | 1 | Details outside this boundary inventory |
| User | At value change | 1 | Details outside this boundary inventory |

## Appointment capacity and coupons

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Leave Application | At cancellation | 1 | Details outside this boundary inventory |
| Leave Application | At submission | 1 | Details outside this boundary inventory |
| Leave Application | At update of a submitted record | 1 | Details outside this boundary inventory |
| Product or service | At record update | 1 | Details outside this boundary inventory |

## Argentine electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Read field value · Customer |
| Customer invoice | Validate record | 1 | Read field value · Customer |

## Attachment object storage

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| File | After record creation | 1 | Details outside this boundary inventory |
| File | At removal | 2 | Details outside this boundary inventory |
| File | Before record creation | 1 | Details outside this boundary inventory |

## Attachment routing by storage folder

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| File | After deletion | 1 | Details outside this boundary inventory |
| File | Before save | 1 | Details outside this boundary inventory |

## Australian accounting and tax

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Bank Account | Validate record | 1 | Details outside this boundary inventory |
| Bank Statement Import | At record update | 1 | Read field value · Bank Account |
| Company | After record creation | 1 | Details outside this boundary inventory |
| Company | At record update | 1 | Details outside this boundary inventory |
| Company | At removal | 1 | Details outside this boundary inventory |
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Read field value · Account |
| Employee | Validate record | 1 | Details outside this boundary inventory |
| Expense Claim | At cancellation | 1 | Details outside this boundary inventory |
| Expense Claim | At record update | 1 | Details outside this boundary inventory |
| Expense Claim | Before submission | 1 | Details outside this boundary inventory |
| Payment voucher | At record update | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Supplier | Validate record | 1 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 2 | Details outside this boundary inventory |
| Supplier invoice | Before submission | 1 | Read field value · Account |
