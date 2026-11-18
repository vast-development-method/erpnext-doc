# Saved query report rules

The following rules describe all eleven stored query reports in the inspected business, foundation, workforce and optional packages. Values in the examples illustrate the query inputs and expected rows. The reporting service applies the report and reference-record access rules around query execution. [Report execution](../../reporting-and-exports.md)

## Maintenance Schedules

Start with submitted schedules and their scheduled visits. Attach a schedule item using the visit's item-row identity. When the visit has a null item reference, use matching item codes within the schedule. Keep the visit when the optional item join fails. The customer and company come from the schedule, the optional sales order from its item row. Sort by scheduled date, then item code. Two same-code item rows can therefore produce two results for a legacy visit without a row reference. An explicit reference to the second item gives one row with the second sales order.

## Trial Balance (Simple)

Select uncancelled general-ledger entries for the requested company. Sum debit and credit separately for each fiscal year, company, posting date and account, and sort by those same four fields. Two debit entries of 20 and 30 against the same account and date give debit 50. A credit of 12 on the next day occupies its own row. Finance book appears in the projection but does not participate in grouping. Rows from different books can enter one total; that total cannot be attributed to a particular book from the displayed label.

## Requested Items To Be Transferred

Include rows from submitted, non-stopped material-transfer and material-issue requests while the row's ordered quantity is below its requested stock quantity. Display the stock unit. Calculate quantity to transfer as stock quantity less ordered quantity, treating an absent ordered quantity as zero. A request for 12 stock units with 5 recorded as ordered shows 7 to transfer. A fully covered row disappears. Results sort by request date.

## Material Requests for which Supplier Quotations are not created

Select each row of a submitted, non-stopped purchase request for which no submitted supplier-quotation line points to that exact request row. Two lines can have the same item code. A submitted quotation referencing the first line removes only the first line. A draft quotation leaves the second line visible. The quantity is the request row's entered quantity. Results sort by request date.

## Open Work Orders

Select submitted orders whose status is outside Closed, Stopped and Completed, whose produced quantity is below the order quantity and which have no submitted stock entry referencing the order. Null produced quantity counts as zero. A submitted order for 10 with no production and one draft stock transfer appears. Submitting that transfer removes the order from this result.

## Work Orders in Progress

Select a submitted order outside Stopped and Closed with at least one submitted stock entry against it. Produced quantity plus process loss must be strictly below the ordered quantity. For an order of 10 with 7 produced and 2 lost, a submitted transfer qualifies it. Recording the tenth unit as additional loss removes it. The query has no separate exclusion for a stored Completed status, so inconsistent status and quantities can put an order in more than one report.

## Completed Work Orders

Select submitted work orders whose stored status is Completed. The query reads the recorded quantities and imposes no additional arithmetic completion test. An order for 10 with 9 produced and 1 process-loss unit appears if its stored status is Completed. A fully produced order still marked In Process does not enter this report.

## Issued Items Against Work Order

Join submitted stock entries to their item lines and work order. Include material transfers for manufacture. If the order skips transfer, also include manufacture and material-consumption lines that specify a source warehouse. Return entries reverse the sign of both transfer quantity and line amount. For a return line of 3 stock units with stored amount 120, the report displays −3 and −120. The source warehouse's projected quantity comes from its current item bin and can change after the original posting. Ordering uses posting date, work order and item code.

## Student Fee Collection

Group submitted sales invoices by linked student. Require a matching student master. Paid amount equals summed grand totals less summed outstanding amounts. An invoice of 100 outstanding 30 and an invoice of 50 outstanding 50 yield paid 70, outstanding 80 and grand total 150 for that student. The query declares no company, currency or payment-date grouping. Interpretation across companies or currencies needs an explicitly scoped dataset.

## Medication Item wise Sales

Join enabled medication records through their linked items to submitted sales invoices for the selected company. Sum sales-invoice line amounts by item and posting date. Two lines of 15 and 25 for the same item and day yield 40 when the item has one enabled medication mapping. The selected medication name is outside the grouping key. Multiple enabled medication mappings to one item can multiply the joined amounts, so uniqueness of the mapping matters when reconciling this report to sales.

## Planned vs Actual Therapy Session

Use plans in the requested company with status other than Cancelled. Report planned and completed sessions and their difference, grouped by plan and sorted by descending start date. A plan with 8 planned and 5 completed shows variance 3. A plan with 9 completed shows −1. The report reads those stored counts directly.
