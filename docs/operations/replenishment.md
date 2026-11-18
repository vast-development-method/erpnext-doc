# Turning a shortage into an authorised material request

## Scheduled replenishment

Enable automatic requests in stock settings and initialise a company and fiscal year. Each item reorder rule supplies monitored warehouse or group, destination warehouse, stock-unit threshold, reorder quantity and request type. Consider enabled stock items whose end-of-life date is absent or later than today. Exclude disabled destination warehouses. Sum projected bin quantities up the warehouse hierarchy for a group-level comparison and use zero for a missing bin.

Given projected quantity P, reorder level L and configured lot Q, evaluate only when L or Q is nonzero and P ≤ L. Start the request at Q. If P + Q ≤ L, add L − P to Q. This second comparison is inclusive and materially affects orders.

| Projected | Level | Lot | Request in stock units | Reason |
|---:|---:|---:|---:|---|
| 11 | 10 | 4 | 0 | Above level |
| 10 | 10 | 4 | 4 | At level |
| 7 | 10 | 4 | 4 | Four takes the projection above the level |
| 6 | 10 | 4 | 8 | Six plus four equals the level. The four-unit deficit is added to the lot |
| −5 | 10 | 4 | 19 | Clear the 15-unit deficit and add four |

Group rows by company and request type, creating submitted requests marked as automatically generated. A transfer policy maps to a material-transfer request. For a purchase request use the purchase unit of measure when supplied: stock requirement divided by item-specific conversion factor, rounded up when the unit of measure requires whole quantities. Scheduled replenishment falls back to factor one on missing conversion. For the 19-unit requirement with packs of six it requests four packs, representing 24 stock units. Preserve the original threshold, configured lot and projected-on-hand evidence in the request row. Due date is current date + item lead days. The header takes the latest row date. The request changes expected supply. Receipt, supplier invoicing and settlement remain subsequent operations.

For a variant with its own reorder rule, evaluate that rule in its unit and warehouse context. A copied rule that remains flagged as belonging to a multi-variant template is skipped. A template rule alone therefore does not assure that a variant request will be generated.

## Material requests from a production plan

Reload the saved plan, check write access and enforce its open status before creating requests. The caller's submit-now option is retained while item quantities and source references come from the saved plan. Require subcontract flags for rows marked for subcontracting. Group requests by reference sales order and request type. The current grouping key supplies an empty customer segment. Refuse a group warehouse as the receiving destination. Keep the plan and its exact material requirement row on each generated line. The command may save drafts or submit according to its option.

1. Derive required purchase/transfer quantities in stock unit of measure. For purchase/subcontract rows with a positive quantity, group by item, destination, request type and supplier. Allocate minimums across groups of sales-order rows within that key, processing sales orders in name order. Transfers do not acquire purchase minimums.
2. First apply surplus from an earlier sales order to the next order's demand. If its positive remainder is below the largest minimum for its rows, add the difference to the first positive row. Carry actual purchased stock quantity minus demand forward, including surplus due to unit of measure rounding. For two orders needing 3 and 4 pieces with minimum 6, the first buys 6 (surplus 3). The second still needs 1 and buys another 6 (surplus 5). If the second instead needs exactly 3 it buys zero.
3. Convert to purchase unit of measure at field precision. When normal rounding would fall below a binding minimum in stock unit of measure, use the next representable grid value that meets the minimum. With factor 6, two decimal places, minimum 7 stock units and a divisible purchase unit of measure, 1.17 purchase units covers 7.02 stock units. If the stock unit of measure is indivisible and that conversion leaves fractional stock, use whole stock unit of measure quantities instead. Respect separately indivisible purchase units of measure.
4. For each saved plan row, outstanding request quantity in its transaction unit of measure = planned quantity − quantity already requested − stock quantity in linked drafts / conversion factor (default one). Round to field precision then round positive requests up for whole units of measure. Ten cases planned, three submitted and 24 stock pieces in drafts at six per case leaves three cases. An immediate repeat after creating those drafts leaves zero. Simultaneous requests need to arbitrate the same outstanding plan row before either saves its claim.
5. Closing/reopening reloads the plan and requires a submitted record and write permission. Closing cancels submitted reservations in Reserved or Partially Reserved state and recomputes the affected bins. Derived rollups skip a closed plan. Reopening recomputes status from produced, completed, requested and ordered quantities. Preserve physical issues already performed.
