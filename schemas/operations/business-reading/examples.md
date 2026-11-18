# Worked readings

These examples follow particular declarations and state their assumptions. Their expected results are derived from the linked procedures.

## A generated user name collides during insert

A new user has the first name Mira and an empty user name. Validation derives a candidate from the first name. Assume the normalized base is `mira`, another user already has that name, and the stored matching suffixes are `mira-2`, `mira-9` and `mira-test`. The allocator considers decimal suffixes. Its candidate is `mira-10`. Validation records that this name came from the first name. The duplicate query excludes the current user's own record. [Validate the user name](foundation/record-runtime/operations-098.md#op-cf63d8a61a758a) · [Allocate a free name](foundation/record-runtime/operations-098.md#op-2b73642aa5b2b8) · [Find another owner](foundation/record-runtime/operations-098.md#op-282762bc2a931c)

| What happens during insert | Consequence |
|---|---|
| The generated candidate is available | The ordinary insert succeeds. The routine releases its savepoint and returns. |
| Another request claims `mira-10` before the insert | An eligible user-name uniqueness failure rolls back to the local savepoint. The routine removes messages added during the failed attempt, advances the candidate to `mira-11`, and retries. |
| The uniqueness failure concerns another field, or occurs on the fifth attempt | The routine propagates the failure. |
| The name was supplied directly | The routine delegates to the parent insertion method immediately. The generated-name retry loop is conditional on the origin flag. |

The allocator's read and the later insert are separate operations. Both requests can observe the same available candidate. The retry is triggered by the insert's actual uniqueness signal and its associated field information. [Insert the user record](foundation/record-runtime/operations-098.md#op-bf53675cbd1ace)

## A zero purchase-receipt rate produces a warning

Consider a purchase receipt for one stock item. Its row explicitly disables the zero-valuation allowance. The item master identifies it as a stock item. The stock controller iterates the receipt's item rows and applies these decisions independently.

| Valuation rate | Incoming rate | Stock update | Expected local result |
|---:|---:|---|---|
| 0 | 7 | Disabled | Display the orange row warning. The valuation-rate branch already qualifies the row. |
| 8 | 0 | Enabled | Display the warning through the incoming-rate branch. |
| 8 | 0 | Disabled | Continue without the warning. |
| 8 | 7 | Enabled | Continue without the warning. |

The incoming-rate branch uses an enabled default when the stock-update key is absent. A row with the allowance enabled, or an item whose master does not qualify as stock, also passes through without this warning. The operation requests a notification. It has no explicit rejection or ledger posting in this body. Another validation or posting step can still affect the receipt as a whole. [Check the row rate](enterprise/controllers/operations-023.md#op-4d543996696382)

## A payment type passes its first validation

A payment record carries `Receive`, `Pay` or `Internal Transfer`. Each of those three literals passes the payment-type membership check. An unrecognized value such as `Receive Cash` calls the validation-error helper. Passing this one check establishes the accepted category. Party, account, transfer, outstanding balance and posting rules belong to further operations on the payment document. [Validate the payment type](enterprise/accounts/operations-064.md#op-7eab4851d4fc71) · [Treasury and reconciliation](../../../docs/transactions/treasury-and-reconciliation.md)
