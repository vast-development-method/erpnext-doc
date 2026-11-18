# Record event boundaries · E

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Earnest money deposit accounting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At cancellation | 1 | Details outside this boundary inventory |
| Earnest money deposit | Validate record | 1 | Details outside this boundary inventory |

## Ecuadorian electronic invoicing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Electronic submission response | After record creation | 1 | Details outside this boundary inventory |
| Electronic submission response | At record update | 1 | Details outside this boundary inventory |
| Electronic submission response | Validate record | 1 | Details outside this boundary inventory |

## Editorial publishing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Comment | After record creation | 1 | Details outside this boundary inventory |

## Egyptian electronic receipts and invoices

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | Before submission | 1 | Read field value · Company; Read field value · Customer invoice |
| Unit of measure | Before record creation | 1 | Details outside this boundary inventory |

## Electronic invoice interchange

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Company | Validate record | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Read field value · Company |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before submission | 1 | Load or construct record · Company |
| Supplier invoice | At submission | 1 | Read field value · Company |
| Supplier invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | Before submission | 1 | Load or construct record · Company |

## Employee advance repayments

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Employee Advance | At record update | 1 | Details outside this boundary inventory |

## Employee professional tax

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Salary Slip | Before save | 1 | Check existence · Employee; Load or construct record · Employee |

## Employee project assignment instructions

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Project | After record creation | 1 | Details outside this boundary inventory |
| Timesheet | At submission | 1 | Details outside this boundary inventory |

## European electronic invoice import

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |

## Event-triggered conversational messaging

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Dispatch note | At submission | 1 | Details outside this boundary inventory |
| Lead | After record creation | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Purchase Order | At submission | 1 | Details outside this boundary inventory |
| Quotation | At submission | 1 | Details outside this boundary inventory |
| Sales Order | At submission | 1 | Details outside this boundary inventory |

## Export duty rebate claims

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Validate record | 1 | Details outside this boundary inventory |
| Duty drawback claim | At submission | 1 | Construct new record · Accounting journal voucher; Read field value · Company (3 occurrences) |
| Export remission claim | At submission | 1 | Construct new record · Accounting journal voucher; Read field value · Company (3 occurrences) |

## Export letters of credit

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |

## External editorial publishing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Create Post | After record creation | 1 | Details outside this boundary inventory |
