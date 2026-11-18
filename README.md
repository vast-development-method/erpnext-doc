# Enterprise resource planning specification

This specification follows the records and decisions that connect a business. A supplier receipt changes warehouse quantities and establishes a received-but-unbilled balance. The supplier invoice clears that balance. A payment settles the resulting liability. Each step has its own authority, currency, source rows, reversal rules and reports. The [receipt-to-cash walkthrough](docs/transactions/receipt-to-cash.md) follows twelve linked vouchers through purchasing, manufacturing, sales, returns and settlement.

## Find a rule

| To answer this question | Open |
|---|---|
| What happens when someone orders, receives, invoices, pays or returns goods? | [Commercial and financial transactions](docs/transactions/README.md) and [document handoffs](docs/transfers/README.md) |
| How are items reserved, picked, valued, produced and dispatched? | [Inventory, warehousing and production](docs/operations/README.md) |
| How do employment, payroll, project time, customer service and industry workflows interact? | [People and services](docs/people-and-services/README.md) |
| Which records, fields, links, permissions and site overrides apply? | [Relational design](docs/model/README.md), [entity and field dictionary](schema/README.md), [document lifecycle](docs/lifecycle/README.md) |
| Which amount, quantity, tax, exchange rate or rounding rule drives a posting? | [Calculation contracts and worked examples](docs/calculations/README.md) and [decision tables](docs/decisions/README.md) |
| What do authorization, tenant isolation, service calls and queued work guarantee? | [Shared services](docs/services/README.md) and [governance](docs/governance/README.md) |
| What can an optional capability contribute? Which languages can be used for an issued document? | [Capabilities and integrations](docs/capabilities/README.md) and [language and issuance](docs/capabilities/language-and-issuance.md) |
| Where are the individual decisions and machine-readable records? | [Detailed catalogs](schemas/README.md), [operation applicability and lookup](schemas/operations/current-decisions/README.md), [record and field dictionary](schema/README.md) |
| What has actually been exercised? | [Coverage by business area](docs/rebuild/coverage-review/README.md), [implementation examples and observations](docs/rebuild/README.md), [qualification register](docs/rebuild/qualification.json) |

The [documentation index](docs/README.md) covers the business chapters, interface and runtime details, implementation sequence and acceptance procedures. The [documentation rules](docs/references/documentation-rules.md) define how to specify a decision.

## How to use the specification

Start with the business action. Identify the company, acting identity, document state, effective business date and installed capabilities. Follow the affected rows to their field definitions, decisions, posting effects and reversal conditions. An entered amount and a company-currency carrying value can differ. An interface translation can change while the issued document retains its original language, identity and amounts.

Use the business chapter for the applicable policy, the dictionary for record structure and the operation lookup for detailed decision order. The lookup distinguishes a retained procedure, a current replacement and a binding absent from the inspected implementation. Supporting tests and data-migration procedures have their own scope. A changed field or function name alone is insufficient evidence that two business actions are interchangeable.

A worked calculation establishes the result for its stated inputs. A recorded posting establishes what happened in the recorded configuration. The [acceptance strategy](docs/reimplementation/acceptance-strategy.md) explains how to compare a separate implementation, including rejection, cancellation, retry and concurrency.

[Apache License, Version 2.0](LICENSE)
