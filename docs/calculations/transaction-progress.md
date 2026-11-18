# Transaction progress and closure

[Complete definitions, units, exceptions and examples](transaction-progress-calculations.json)

## Transaction completion percentage

- Apply explicit row exclusion; return one hundred if that exclusion leaves no rows.
- When closure applies, use open rows if any remain; otherwise use all remaining rows.
- Take absolute expected and completed values.
- Clamp each completed magnitude to its own expected magnitude.
- If sum of expected magnitudes is zero, return zero.
- Divide sum of clamped magnitudes by sum of expected magnitudes, multiply by one hundred, and round to six decimal places.

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
- Separate zero-value billing helper uses strictly greater than 99.999999 for full billing

## Closed order preserves posted effects

- If received units were invoiced, supplier debt remains 72.00 before payment or credit
- If received units were unbilled, receipt clearing remains credit 72.00

Given — ordered quantity = 10, received quantity = 6, unit cost = 12.00, all rows closed = True.

Expected — released outstanding commitment = 4, actual receipt percentage = 60.000000, warehouse quantity = 6, received value = 72.00, parent status = Closed, closure financial postings = [], closure physical stock movements = [].
