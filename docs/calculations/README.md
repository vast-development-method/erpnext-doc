# Calculations and worked cases

A formula specifies its operands, their units, the stage at which precision applies and the conditions that change the result. The linked structured definitions also carry intermediate values, exceptions and examples. A business date in a test case belongs to its transaction.

| Business area | Rule families | Worked cases |
|---|---|---|
| [Financial recognition and settlement](finance.md) | Pricing, compound and inclusive taxes, credits, withholding, currency conversion, outstanding amounts, depreciation and period close | [Journal events, opening and closing balances, refusals](../../schemas/mathematics/accounting-acceptance-cases.json) |
| [Inventory, fulfilment and production](inventory.md) | Stock units, packing, reservation, valuation layers, manufacture, overhead and quality | [Quantity, value, progress and state](../../schemas/mathematics/inventory-acceptance-cases.json) |
| [Customers, projects and service](customer-and-service.md) | Forecasts, invoice attribution, task weighting, service calendars, invoice exchange and contract fulfilment | [Selection and calculation cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json) |
| [Workforce, pay and benefits](workforce.md) | Payable days, half holidays, overtime, benefits, tax projections, advances, recruitment and appraisal | [Arithmetic and payroll transactions](../../schemas/mathematics/workforce-acceptance-cases.json) |
| [Commercial progress](transaction-progress.md) | Row allocation, clamping, tolerance, exclusion, closure and reopening | [Procedures and boundary values](../../schemas/mathematics/transaction-progress-calculations.json) |

[Inventory decisions at the voucher boundary](inventory-decisions.md) specifies how to combine item and warehouse account selection, landed costs, reservation updates, inspections and reversals. Recognising revenue, paying an invoice and shipping stock have different effects even when the documents share an amount.

The [calculation and worked-case index](../../schemas/mathematics/definition-coverage.json) connects all 184 named definitions and both ordered valuation procedures to their operands and worked cases. The [review register](../../schemas/traceability/mathematics-verification.json) identifies the calculation evidence and the scope of each comparison.
