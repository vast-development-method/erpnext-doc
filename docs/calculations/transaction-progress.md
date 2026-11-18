# Transaction progress and closure

[Complete definitions, units, exceptions and examples](../../schemas/mathematics/transaction-progress-calculations.json)

## Transaction completion percentage

- Read every item row belonging to the given parent and document type.
- Take absolute expected and completed values.
- Clamp each completed magnitude to its own expected magnitude.
- If sum of expected magnitudes is zero, return zero.
- Divide sum of clamped magnitudes by sum of expected magnitudes, multiply by one hundred, and round to six decimal places.

A stored parent percentage at least 99.999999 snaps to 100. The [optional row-closure measure](../operations/transaction-progress-and-row-closure.md#closed-rows-in-editing-and-mapping) can exclude closed rows when any are open and falls back to actual performance when all are closed. A configured explicit exclusion that removes all rows gives 100% for that optional measure.

## Fulfilment allowance

`overflow percentage = one hundred multiplied by completed minus expected, divided by expected`

configured authorised role receives warning instead of the excess rejection

percentage check skipped by the calling guard

## Absolute no allowance boundary

- Restrict candidates to completed values greater than expected values
- Reject when completed minus expected is strictly greater than 0.01

## Completion label boundary

- Common helper: less than 0.001 is not completed
- Common helper: at least 99.999999 is fully completed
- Other values are partly completed
- Zero-value billing rounds its quantity ratio to two decimal places before multiplying by 100 and applying the same full threshold. One of three units reports 33%. A quantity of 996 billed against 1,000 reports 100%.

## Closed order preserves posted effects

- If received units were invoiced, supplier debt remains 72.00 before payment or credit
- If received units were unbilled, receipt clearing remains credit 72.00

Given — ordered quantity = 10, received quantity = 6, unit cost = 12.00, parent order closed after the partial receipt.

Expected — released outstanding commitment = 4, actual receipt percentage = 60.000000, warehouse quantity = 6, received value = 72.00, parent status = Closed, closure financial postings = [], closure physical stock movements = [].
