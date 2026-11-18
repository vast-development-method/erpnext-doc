# Record event boundaries · B

Each row identifies when processing can occur. “Load or construct” does not imply that a record was saved or posted. A direct write concerns the named field operation. Additional effects that are not specified here must be established by the relevant workflow. Multiple registrations at the same boundary may belong to different configurations.

## Balance sheet reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| General ledger entry | After record creation | 1 | Details outside this boundary inventory |

## Bangladeshi value added tax invoices

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | Before validation | 1 | Details outside this boundary inventory |
| Point of sale invoice | At submission | 1 | Details outside this boundary inventory |
| Supplier invoice | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Supplier invoice | Validate record | 1 | Details outside this boundary inventory |

## Bank messaging and account reconciliation

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Accounting journal voucher | At removal | 1 | Check existence · Bank Transaction; Load or construct record · Bank Transaction |
| Accounting journal voucher | At submission | 1 | Load or construct record · Bank Transaction |
| Bank Account | Before validation | 1 | Details outside this boundary inventory |
| Bank Account | Validate record | 1 | Details outside this boundary inventory |
| Bank Transaction | At cancellation | 1 | Load or construct record · Accounting journal voucher; Read selected rows · Accounting journal voucher |
| Bank Transaction | At update of a submitted record | 1 | Details outside this boundary inventory |
| Bank Transaction | Before submission | 1 | Read retained field value · Bank Account; Read retained field value · Company |
| Employee | Validate record | 1 | Check existence · Bank Account |
| Expense Claim | When a euro payment order changes state | 1 | Details outside this boundary inventory |
| Expense Claim | When resolving a euro payment amount | 1 | Details outside this boundary inventory |
| Payment voucher | At removal | 1 | Check existence · Bank Transaction; Load or construct record · Bank Transaction |
| Payment voucher | At submission | 1 | Load or construct record · Bank Transaction |
| Supplier invoice | When a euro payment order changes state | 1 | Details outside this boundary inventory |
| Supplier invoice | When resolving a euro payment amount | 1 | Details outside this boundary inventory |

## Bank payout integration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Payment voucher | At load | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 1 | Details outside this boundary inventory |
| Payment voucher | Before cancellation | 1 | Details outside this boundary inventory |
| Payment voucher | Before submission | 1 | Details outside this boundary inventory |
| Payment voucher | Validate record | 1 | Details outside this boundary inventory |

## Barcode label printing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Product or service | Validate record | 1 | Details outside this boundary inventory |

## Biometric attendance and leave

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Biometric Manual Punch | At removal | 1 | Read field value · Employee (2 occurrences) |

## British value added tax filing

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Error Log | Before record creation | 1 | Details outside this boundary inventory |
| File | Before validation | 1 | Details outside this boundary inventory |
| Payment voucher | At cancellation | 1 | Details outside this boundary inventory |
| Payment voucher | At submission | 2 | Details outside this boundary inventory |
| Supplier invoice | At cancellation | 1 | Details outside this boundary inventory |
| Supplier invoice | At submission | 1 | Details outside this boundary inventory |
| User | At sign-in | 1 | Details outside this boundary inventory |

## Burundian electronic sales reporting

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Customer invoice | At submission | 1 | Details outside this boundary inventory |
| Customer invoice | Before cancellation | 1 | Details outside this boundary inventory |
| Customer invoice | Before save | 1 | Details outside this boundary inventory |
| Point of sale invoice | At submission | 1 | Details outside this boundary inventory |
| Point of sale invoice | Before cancellation | 1 | Details outside this boundary inventory |

## Business call integration

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Contact | After deletion | 1 | Details outside this boundary inventory |
| Contact | Before save | 1 | Details outside this boundary inventory |

## Business messaging dispatch

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After deletion | 1 | Details outside this boundary inventory |
| Any eligible record | After record creation | 1 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | At record update | 1 | Details outside this boundary inventory |
| Any eligible record | At removal | 1 | Details outside this boundary inventory |
| Any eligible record | At submission | 1 | Details outside this boundary inventory |
| Any eligible record | At update of a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | Before cancellation | 1 | Details outside this boundary inventory |
| Any eligible record | Before record creation | 1 | Details outside this boundary inventory |
| Any eligible record | Before submission | 1 | Details outside this boundary inventory |
| Any eligible record | Before updating a submitted record | 1 | Details outside this boundary inventory |
| Any eligible record | Before validation | 1 | Details outside this boundary inventory |
| Any eligible record | Validate record | 1 | Details outside this boundary inventory |

## Business messaging notifications

| Business record | Event | Registrations | Direct data operations |
|---|---|---:|---|
| Any eligible record | After record creation | 2 | Details outside this boundary inventory |
| Any eligible record | Assign record identifier | 2 | Details outside this boundary inventory |
| Any eligible record | At cancellation | 2 | Details outside this boundary inventory |
| Any eligible record | At load | 2 | Details outside this boundary inventory |
| Any eligible record | At record update | 2 | Details outside this boundary inventory |
| Any eligible record | At removal | 2 | Details outside this boundary inventory |
| Any eligible record | At submission | 2 | Details outside this boundary inventory |
| Any eligible record | At update of a submitted record | 2 | Details outside this boundary inventory |
| Any eligible record | At value change | 2 | Details outside this boundary inventory |
| Any eligible record | Before identifier assignment | 2 | Details outside this boundary inventory |
| Any eligible record | Before record creation | 2 | Details outside this boundary inventory |
| Any eligible record | Before save | 2 | Details outside this boundary inventory |
| Any eligible record | Before updating a submitted record | 2 | Details outside this boundary inventory |
| Any eligible record | Before validation | 2 | Details outside this boundary inventory |
| Any eligible record | Before value change | 2 | Details outside this boundary inventory |
| Any eligible record | Validate record | 2 | Details outside this boundary inventory |
