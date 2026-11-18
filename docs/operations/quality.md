# Inspection evidence, release gates and corrective action

## Bind evidence to the row

An inspection records type, referenced transaction and child row, item, optional batch, inspector, sample size, readings and decision. Copy the company's identity from its referenced transaction. When no row was specified, the operation finds eligible rows of the same item under the reference in row order, restricts by batch when supported and prefers a row without another active inspection. Stock movement lines and job cards have distinct link shapes. For a job card the update also matches its production item. If eligible rows are already inspected, do not replace the existing inspection merely because an item repeats.

For receipt R with two rows of product P in batches A and B, an inspection for B belongs to the B row. Creating a second inspection cannot displace the first from that row. Allow the next inspection for the other eligible row when no batch restriction precludes it. On delete/cancel clear only links that still point to this inspection, and notify the referenced document. On cancellation a linked submitted transaction normally must be cancelled first. The post-purchase/post-delivery inspection setting lifts that dependency.

## Decide the reading and release the operation

| Step | Decision |
|---|---|
| Populate criteria | If readings are empty, populate from the selected template or item default. In-process job-card readings refresh matching parameter criteria from the inspection's own template first. |
| Normalise evidence | Validate newly entered nonblank, automatic, numeric readings against the user's number format. Unchanged stored input passes that edit-time check even when a different locale is active. Manual reading rows keep their specified verdict. |
| Automatic range | Between one and ten nonblank values may participate. Every provided value must be within inclusive limits. An empty set fails. Automatic nonnumeric equality compares the observed and configured strings, with empty representing missing. |
| Automatic formula | Bind named readings and the mean of nonblank numeric readings, or the observed string for a nonnumeric test. An absent numeric position binds to zero. A missing expression, unknown variable or invalid expression fails validation. |
| Set header | For an automatic header and available readings, any rejected reading rejects the inspection. A manual header is separately selectable. On submission every reading must have a decision and sample size must exceed zero. Only the cancellation action may assign the Cancelled status. |
| Publish link | A blank or Warn policy for unsubmitted inspections updates the linkage on draft save. A Stop policy links on submission. |
| Gate a transaction | Apply purchase/delivery flags for stocked invoices, receipts and deliveries, or use stock-entry purpose/row rules when inspection is enabled. Validate linked reference identity. On eligible required rows, missing inspection warns in draft and stops submission. At submission, unsubmitted and non-accepted inspections have independent Warn/Stop controls. Exempt secondary-output rows and the policy allowing inspection after receipt/delivery follow separate branches. |

For numeric readings 9, 10, 11 and one blank, mean is 10 and the range 9–11 passes. Under a rule testing mean ≥ 10 and requiring the fourth position to exceed zero, it fails. A manually rejected row remains rejected even when its numbers lie inside the numeric range. A successful inspection records evidence. The accepted/rejected warehouse movements and commercial consequences are owned by the originating receipt or stock transaction.

## Review goals and resolve actions

A quality goal owns objective, target and unit of measure rows. An empty review is populated from that goal. New or changed review objectives must belong to its current goal. Changing the goal rechecks all rows. Keep existing historical objectives where the original review reference has not changed. A review stays Open when empty or when any objective lacks a final Passed/Failed result, including when another row has failed. Once all have final results, one failed objective makes the header Failed. Otherwise Passed.

The daily review schedule creates a review only when the goal's cadence is due and a review for this goal and date does not already exist. Weekly follows named weekday. Monthly caps a requested day at the last day of the month. Quarterly uses January, April, July and October with the same day cap. A monthly target on day 31 therefore falls on 28 February in a non-leap year, even though the shortest month lacks day 31. A repeated scheduler invocation for the same goal and date must reuse the review. Concurrent runs must arbitrate that goal/date identity before creating a second review.

A corrective action is Completed only if it has at least one resolution and all resolutions are Completed. Nonconformance separately records subject, procedure, responsible party, details and corrective/preventive responses. No automatic stock rejection, disposal, supplier payment block or action closure follows solely from entering that record.

## Template admission and review meeting

A template owns ordered criteria that are unique by measurement parameter. Reject a repeated parameter. A numeric range permits equality at its limits but rejects a minimum above the maximum. A descriptive equality criterion requires its expected value. A formula criterion requires a nonblank expression. These are template-admission rules, before recording the first measured value.

A quality meeting has Open or Closed status, ordered agenda items and minutes. A minute may identify a particular quality review, corrective action or feedback record. The selected kind determines which identifier is valid. Closing a meeting preserves its minutes and references. Its status cannot complete someone else's corrective action or post a stock release. Quality managers and system administrators can maintain meetings. Staff with ordinary workspace access can read, print and report on them subject to their record grants.
