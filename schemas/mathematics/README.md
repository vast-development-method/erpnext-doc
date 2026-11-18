# Mathematics

These named contracts define operands, signs, units, currencies, decision order, rounding and expected answers. Acceptance catalogs provide concrete records and events. Decimal examples establish their own arithmetic; they do not certify an unexecuted transaction engine.

[Parent index](../README.md)

Use the [calculation and worked-case index](definition-coverage.json) to look up a formula by identifier. Each entry identifies the exact definition, operand dictionary and at least one worked case. For example, `customer_credit_exposure` links the exposure formula to both a credit-limit boundary and the valuation of unbilled, unreturned delivery stock.

| Business area | Named definitions | Ordered procedures | Definitions with a worked case |
|---|---:|---:|---:|
| Finance | 58 | 0 | 58 |
| Inventory, manufacturing and quality | 40 | 2 | 42 |
| Workforce | 51 | 0 | 51 |
| Customers and services | 30 | 0 | 30 |
| Transaction progress | 5 | 0 | 5 |
| **Total** | **184** | **2** | **186** |

The [mathematics review register](../traceability/mathematics-verification.json) preserves 180 previously recorded observations. The index identifies 93 additional arithmetic, calendar, interval, status and layer comparisons across 72 definitions and procedures. These counts overlap at the definition level. To implement a calculation, use its stated currency or units, rounding stage, selection conditions and expected outcome.

## Definitions

| Entry | Contents |
|---|---|
| [Accounting event and boundary acceptance cases](accounting-acceptance-cases.json) | Self-contained financial reconstruction tests with fully stated journal events, expected balances, decimal arithmetic and explicit compatibility decisions |
| [Customer and service acceptance cases](customer-and-service-acceptance-cases.json) | 51 cases. |
| [Customer and service calculations](customer-and-service-calculations.json) | 30 calculations. |
| [Financial calculations and numerical acceptance fixtures](financial-calculations.json) | 58 formulas, 64 worked examples and 5 acceptance observations. |
| [Inventory, packaging, fulfilment, manufacturing and quality acceptance cases](inventory-acceptance-cases.json) | Self-contained replacement-system test inputs and expected business outcomes. Decimal quantities and money are represented by exact decimal strings. |
| [Inventory, fulfilment and manufacturing mathematical contracts](inventory-calculations.json) | Self-contained quantity, valuation, fulfilment, manufacturing and quality decision contracts. Business arithmetic is independent of implementation language and storage… |
| [Transaction progress and row closure calculations](transaction-progress-calculations.json) | 5 calculations. |
| [Workforce acceptance cases](workforce-acceptance-cases.json) | Self-contained arrangements and expected outputs for reimplementation. Values are deliberately invented conformance fixtures, not statutory rates. |
| [Workforce calculations](workforce-calculations.json) | Current employment, attendance, leave, payroll, benefits, recruitment, performance and employee-expense mathematical behaviour |
