# Sales, retail and service decisions

Sales commitments flow from quotation and order rows into deliveries, invoices, loyalty entries and recurring billing periods. Follow the [commercial transaction chapters](../../transactions/README.md) for the decisions and worked outcomes. The service operations below bind those decisions to fixture inputs and expected errors.

| Business question | Specification |
|---|---|
| Which quote options and discounts can become an order, and what counts as conversion? | [Pipeline, alternatives, authorization, coupons and reporting](../../transactions/sales-pipeline-and-approval.md) · [evidence](sales-pipeline-and-approval.md) |
| What remains to deliver, invoice or print for a customer? | [Order promises, return-adjusted billing and pro forma issue](../../transactions/order-promises.md) · [evidence](order-promises.md) |
| Which products, rewards and amounts qualify? | [Pricing, loyalty, lot allocation and ledger effects](../../transactions/pricing-and-loyalty.md) · [evidence](pricing-and-loyalty.md) |
| Which period is due, what does it cost, and when does billing stop? | [Recurring billing](../../transactions/recurring-billing.md) · [evidence](recurring-billing.md) |
| Which receipt posted, what should be in the till, and what happens on a failed close? | [Retail closing](../../transactions/retail-closing.md) · [evidence](retail-closing.md) |
| Which customer, agent, agreement, serial number and project can be serviced? | [Appointment admission, service, maintenance and time billing](../../people-and-services/customer-appointments.md) · [evidence](appointments-and-service.md) |
| How are commissions, targets, installment coverage and company tax defaults calculated? | [Commercial reports and country setup](../../transactions/commercial-performance.md) · [evidence](commercial-reports/README.md) |
| How do bulk operations recover, portal identities bind, calls route and exchange codes resolve? | [Batch, portal and code exchange](../../transactions/batch-portal-and-codes.md) · [evidence](batch-portal-and-codes.md) |

## Machine-readable verification

[Decision definitions](decisions.json) declare each operation's input assumptions and upstream source. [JSON Schema](decisions.schema.json) defines the typed input and result separately for each operation. [Acceptance cases](acceptance.json) carry exact inputs and expected values or a business rejection. Currency examples use integer hundredths. A production adapter is responsible for the applicable field precision and currency scale. Use the case identifier when comparing a replacement's actual result with the expected one. Missing runtime permissions, settings and records must be supplied by the integration fixture according to each chapter.

The optional [example verifier](check-fixtures.jq) independently evaluates the small decision models. From this directory run:

```sh
jq -ef check-fixtures.jq acceptance.json
```

A successful check verifies the numerical and decision examples against this oracle. It does not exercise an installed site. Cross-cutting integration fixtures still needed include concurrent booking verification, concurrent period generation, atomic POS consolidation and cancellation with serialized stock, submission and email delivery of an actual PDF, and post-reversal reconciliation of the stock, receivable and reward ledgers. Report these separately from source review and fixture evaluation.
