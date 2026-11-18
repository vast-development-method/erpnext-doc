# Subscription periods, rate determination and invoice recognition

The agreement links a company, typed party, one or more plan/quantity lines, trigger mode, period bounds and cancellation policy. Each plan owns its product, currency, interval unit and count, rate basis, cost centre and optional accounting dimensions. The invoice links back to the subscription and stores its service period. Drafting the invoice, posting it, settling it and cancelling the agreement are four separate events.

## Construct the period

A plan interval count must be at least one. All plans on an agreement must share the same interval **and count**. Match their currencies to the party's default billing currency or the company default. A trial start requires an end and cannot follow the subscription start. The trial end cannot precede its start. A configured subscription end must be strictly later than the end computed for the first full interval. Calendar-month alignment additionally requires a monthly plan and an end date.

Counting is inclusive: a one-week period starting 5 April ends 11 April. Day and week intervals add count − 1 days and 7 × count − 1 days respectively. Month and year intervals add the selected calendar increment less one day. Calendar-month alignment overrides this end with the last day of the month containing start + (count − 1) months. Cap the resulting regular period at the subscription end. In the observed start selector, a trial end after the original start takes priority over an explicit candidate date, returning trial end + 1. Exercise that branch when testing advancement after a trial.

## Price a service period

| Basis | Unit rate calculation | Example |
|---|---|---|
| Fixed | Plan cost × period factor | At cost 310, factor 10/31, rate 100. Quantity 2 yields 200 before tax. |
| Price list | Resolve item and configured price list for the quantity and party inputs; use price-list rate × factor. Missing price gives zero. | Rate 80 and factor 0.5 give 40 per unit. |
| Monthly | Compute **completed calendar-relative years × 12 + months + 1** between the endpoints. Multiply by monthly cost. With proration, subtract cost × (days before start in start month / days in start month + days after end in end month / days in end month). | January 1, 2025 through January 31, 2026 at 100/month gives 1,300. April 11–30 of one year at 300/month gives 200. |

Monthly basis uses its own skipped-day formula. For fixed/list pricing with proration, prepaid and advance modes use factor 1. Arrears uses (today − current period start + 1)/(current end − current start + 1). This uses the actual processing clock, and the expression has no clamp to 1. Preserve the clock separately from a caller's simulated posting date. Monthly relative differences can yield surprising results when the ending day-of-month precedes the starting day in a later month.

## Process due work

1. Determine trigger from period start, period start − configured days, or period end. Block new billing if cancelled or an outstanding submitted non-Paid invoice exists and continued billing is disabled. Reject processing earlier than trigger or later than period end plus the interval adjustment. This is an inclusive late window.
2. Inspect the latest noncancelled invoice by descending service-end date, including drafts. Its service start matching this period means already generated. For an invoice lacking service start, fall back to posting date within the inclusive period. A start beyond subscription end also suppresses generation.
3. A customer generates a sales invoice; a supplier generates a purchase invoice and sets the withholding flag for a supplier with a withholding category/group. Derive currency from the first plan. Copy header dimensions, plan line dimensions, cost centres, quantities and computed rates. For deferred products copy service bounds. Apply the direction-specific tax template. A nonzero days-until-due sets one 100% installment. A trial gets a 100% additional discount. Otherwise apply configured discounts, defaulting their base to grand total.
4. Save, and submit only when the subscription requests submission. Use standard invoice posting for ledgers and receivables/payables. The generator does not enable stock updates for service billing. Advance the current period after generation subject to the end and cancellation checks. On insertion the catch-up loop skips imports, migrations and future starts. It stops on cancellation, no progress or the stop-on-outstanding configuration.
5. Status has a separate clock. Already Cancelled is terminal to ordinary status refresh. Trial precedes completed, then past-grace policy (Unpaid or Cancelled), then Grace Period, then Active if no outstanding invoice. The due day and last grace day are inclusive: due April 10 with three grace days is past grace on April 14. The status method passes the supplied posting date to its completion test but calls the trial and overdue/grace checks without it.
6. Cancellation of an active agreement billed other than at the beginning can generate a final invoice from current start through cancellation date, then saves Cancelled. Existing invoices retain their lifecycle. Restart requires Cancelled, clears the cancellation date and resets the current period; the restart method does not unlink historical invoices.

The latest-invoice check is observable repeat protection. Concurrent independent workers require an execution test for duplicate generation. A replacement can serialize per agreement and reconcile by agreement + period as an explicit reliability choice.
