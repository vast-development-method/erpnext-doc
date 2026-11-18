# Enterprise resource planning specification

Start with a business decision. To trace a supplier delivery through purchasing, the warehouse, the ledger, and the bank, follow [the receipt-to-cash example](transactions/receipt-to-cash.md). It identifies each voucher, the amounts posted, the stock remaining and the balance still owed. For an individual record, open the [entity and field dictionary](../schema/README.md) and follow the relevant workflow below.

| What do you need to determine? | Where to read |
|---|---|
| Which company owns a record and what can be shared? | [Company policy and shared masters](governance/README.md), [business scope](overview/scope-and-baseline.md) and [application architecture](overview/application-architecture.md) |
| What happens when an order is received, billed, settled or reversed? | [Commercial and financial transactions](transactions/README.md) and [transfers between documents](transfers/README.md) |
| How does stock move and acquire value? | [Purchasing, fulfilment, production, quality and maintenance](operations/README.md) |
| How do employment, payroll, projects and customer service interact? | [People, projects and services](people-and-services/README.md), [project costs](transactions/project-costing.md) and [workforce calculations](calculations/workforce.md) |
| What can an operator read, submit, print or retry? | [Services and administration](services/README.md), [service operations](services/operations/README.md) and [reports](services/reports/README.md) |
| Which fields, relationships and lifecycle events govern a document? | [Logical model](model/README.md), [entity dictionary](../schema/README.md), [lifecycle by record](lifecycle/README.md) and [rejection conditions](decisions/README.md) |
| How are quantities, amounts and rounding calculated? | [Formulas and acceptance cases](calculations/README.md) and [structured mathematical contracts](../schemas/mathematics/README.md) |
| Which optional capabilities participate in the transaction? | [Capability directory and multilingual workflows](capabilities/README.md) and [language selection for issued documents](services/languages-and-issuance.md) |
| Where are the detailed decisions, definitions and evidence? | [Structured catalogs](../schemas/README.md), [how to interpret ordered decisions](runtime/decision-contract-interpretation.md) and [implementation evidence](rebuild/README.md) |
| What should a replacement reproduce? | [Implementation sequence](reimplementation/sequence.md), [conformance profiles](reimplementation/conformance-profiles.md), [acceptance strategy](reimplementation/acceptance-strategy.md) and [coverage and evidence](references/coverage-and-evidence.md) |

The [domain index](domains/README.md) lists individual business subjects. The [data](data/README.md), [interfaces](interfaces/README.md) and [runtime](runtime/README.md) indexes lead to the same chapters by technical concern. The [business compatibility map](overview/business-compatibility-map.md) traces relationships across domains.
