# Sales, retail and service decisions

This supplement explains operational decisions traced to the [ERPNext 16.60.0 source](https://github.com/frappe/erpnext/tree/886ab6ae187244e7f1b852393384ab6019d56264). It adds a release-specific reading alongside the [September source snapshot](../../../schemas/traceability/source-snapshot.json). Where the snapshots differ, select the intended baseline explicitly when testing. The proposed service operations and error codes below are neutral vocabulary for the rebuild.

| Business question | Specification |
|---|---|
| Which quote options and discounts can become an order, and what counts as conversion? | [Pipeline, alternatives, authorization, coupons and reporting](sales-pipeline-and-approval.md) |
| What remains to deliver, invoice or print for a customer? | [Order promises, return-adjusted billing and pro forma issue](order-promises.md) |
| Which products, rewards and amounts qualify? | [Pricing, loyalty, lot allocation and ledger effects](pricing-and-loyalty.md) |
| Which period is due, what does it cost, and when does billing stop? | [Recurring billing](recurring-billing.md) |
| Which receipt posted, what should be in the till, and what happens on a failed close? | [Retail closing](retail-closing.md) |
| Which customer, agent, agreement, serial number and project can be serviced? | [Appointment admission, service, maintenance and time billing](appointments-and-service.md) |
| How are commissions, targets, installment coverage and company tax defaults calculated? | [Commercial reports and country setup](commercial-reports/README.md) |
| How do bulk operations recover, portal identities bind, calls route and exchange codes resolve? | [Batch, portal and code exchange](batch-portal-and-codes.md) |

## Machine-readable verification

[Decision definitions](decisions.json) declare each operation's input assumptions and upstream source. [JSON Schema](decisions.schema.json) defines the typed input and result separately for each operation. [Acceptance cases](acceptance.json) carry exact inputs and expected values or a business rejection. Currency examples use integer hundredths. A production adapter is responsible for the applicable field precision and currency scale. Use the case identifier when comparing a replacement's actual result with the expected one. Missing runtime permissions, settings and records must be supplied by the integration fixture according to each chapter.

The optional [example verifier](check-fixtures.jq) independently evaluates the small decision models. From this directory run:

```sh
jq -ef check-fixtures.jq acceptance.json
```

A successful check verifies the numerical and decision examples against this oracle. It does not exercise an installed ERPNext site. Cross-cutting integration fixtures still needed include concurrent booking verification, concurrent period generation, atomic POS consolidation and cancellation with serialized stock, submission and email delivery of an actual PDF, and post-reversal reconciliation of the stock, receivable and reward ledgers. Report these separately from source review and fixture evaluation.
