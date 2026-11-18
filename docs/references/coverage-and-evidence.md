# Coverage and evidence

Use the [business chapters](../README.md) for the applicable rule and the [logical field dictionary](../../schema/README.md) for its records. The measures below describe the underlying collections. Several collections describe the same activity at different levels, so their counts cannot be added to obtain a feature total.

## Measured coverage

| Collection or test | Count | Meaning |
|---|---:|---|
| Classified input components | 12,282 | Includes production capabilities, fixtures, migration-related artifacts and supporting files. The inventory includes 5,583 parsed server files. |
| Detailed record definitions and declared fields | 1,044 / 16,813 | Includes stored values, owned children, protected values, layout declarations, settings and virtual results. |
| Relationships, field conditions and record behaviour bindings | 3,820 / 2,818 / 1,042 | Fixed links, dynamic links, child ownership, field expressions and event bindings. |
| Operation identifiers | 33,360 | Distinct callable declarations across enterprise, shared services, workforce and customer relationship functions. An ordered decision body has to be matched to its declared identifier. |
| Exposed operations | 1,771 | Of the registrations, 1,768 were classified as candidates for business use. Registration alone establishes neither permission nor reachable outcomes. |
| Reports, conditional column definitions and filter definitions | 226 / 1,609 / 1,119 | The filter inventory includes 556 parsed defaults. Dynamic runtime columns depend on the report and its arguments. |
| Operational presentation declarations | 831 | Includes workspaces, reports, dashboards, print definitions and related surfaces. |
| Arithmetic expression candidates | 6,049 | Each candidate needs its operands, units, precision, preconditions and side effects to serve as a calculation contract. |
| Named calculation definitions | 184 | The catalog contains 58 financial formulas, 51 workforce calculations, 40 inventory calculations, 30 customer/service calculations and 5 progress procedures. It also contains two ordered layer-valuation procedures. |
| Definition and worked-case coverage | 186 / 186 | The [calculation index](../../schemas/mathematics/definition-coverage.json) links all 184 named calculations and both ordered valuation procedures to their operands and worked cases. |
| Recorded example review | 180 earlier observations and 93 additional comparisons | The earlier aggregate reported 142 contracts. Its receipt includes journal and rounding observations. The additional document comparisons cover 72 definitions and procedures, including decisions and monetary, quantity, calendar and layer examples. |
| Evidence anchors in the structural review | 208 | A cited source artifact identifies evidence for a particular statement. Review of one decision does not imply review of every branch in its containing file. |

See the [structured coverage catalog](../../schemas/traceability/catalog-coverage.json), [mathematical verification register](../../schemas/traceability/mathematics-verification.json) and [validation results](../../schemas/traceability/validation-result.json). The [logical dictionary](../../schema/README.md) also covers optional business entities and distinguishes data fields from relationship fields. Its counts describe a different population.

## Where the business decisions are documented

| A reader wants to know | Local specification |
|---|---|
| What does an active operation do when a condition succeeds or fails? | [Operation reading directory](../../schemas/operations/business-reading/README.md). Find the operation by its business subject or stable identifier. Each entry joins the input signature, ordered local decisions, conditions, effects and applicable source binding. |
| Where is the worked case for a named formula? | [Definition and case cross-reference](../../schemas/mathematics/definition-coverage.json). It distinguishes the earlier arithmetic review from subsequent documentation examples. |
| Why can the same report show different columns or row totals? | [Report behaviour](../services/reports/behaviour/README.md), [dynamic outputs](../services/reports/behaviour/dynamic-output.md) and [stored query examples](../services/reports/behaviour/query-rules.md). Each report entry identifies the applicable result builder and published controls. |
| Which decision was recovered for a previously open business topic? | The [business question index](business-rule-coverage.md) and [domain review registers](../../schemas/traceability/README.md) link the decision and applicable operating conditions to the relevant business chapter. |
| How much is known about a third-party extension? | The [provider-by-provider evidence register](../rebuild/marketplace-guides/provider-evidence.md) gives the strongest available material, a specific remaining uncertainty and the evidence needed to establish what the publisher does. |

The operation reading directory covers 23,195 applicable bindings across enterprise transactions, shared services, workforce and customer relationships. Its branch descriptions come from the inspected procedures. A call to a user-selected controller still depends on the installed controller; the [project costing case](../transactions/project-costing.md) illustrates why the distinction matters. The business chapters give worked interpretations for reviewed paths.

## Decisions and field interpretation

The [operation directory](../../schemas/operations/README.md) and [decision interpretation](../runtime/decision-contract-interpretation.md) describe parameters, ordered branches, loops, failure, cleanup and completion. Call dependencies, effective configuration and permissions determine which outcomes a business request can reach. Test those outcomes at the transaction boundary.

The [conditional field semantics](../../schemas/data/conditional-field-semantics.json) resolve 85 field-condition occurrences represented by 54 distinct expressions. These cover compound and collection predicates, optional children and section expansion. A true expansion condition opens its section. A form condition and server validation are distinct decisions.

Definitions preserve field identity, order, relationship targets, defaults, naming rules and meaningful blank or punctuation values. Collection removal is a collection operation. Type alternatives in annotations describe allowed shapes. Names that would collide globally remain qualified by the owning record. The [review registers](../../schemas/traceability/README.md) connect the financial, workforce, inventory, customer, foundation and cross-domain rules to published decisions and worked cases. Each register also identifies observations that depend on the actual provider, deployment or implementation.

## Transaction and execution evidence

The [receipt-to-cash observation](../rebuild/live/README.md) records balances after each of twelve posted vouchers. The [stock results](../rebuild/stock-live/README.md) cover reservations, valuation, production and closing. The [warehouse fulfilment observations](../rebuild/warehouse-fulfilment/README.md) cover physical allocation, picking, packing and dispatch. Compare these with the [shared-service observations](../rebuild/platform-live/README.md), [restore results](../rebuild/recovery-live/README.md) and [module-level test results](../rebuild/coverage-review/reference-tests.md).

The [project-cost example](../transactions/project-costing.md) distinguishes the company-currency controller from the employee-expense controller using identical time rows. Isolated calculations establish the observed outputs for those inputs. They do not establish deployment-wide hook dispatch or successful posting to a live tenant.

## What remains dependent on the deployment

A production comparison needs the selected company, accounting and inventory policies, permissions, custom fields, language and enabled optional services. Dynamic reports, provider callbacks, concurrent operations, retries and failures after remote acceptance require their own observations. A jurisdiction’s current law and the receiver’s accepted format must be established separately from a regional fixture.

Use the [acceptance strategy](../reimplementation/acceptance-strategy.md), [conformance gates](../../schemas/traceability/conformance-gates.json), [integration qualifications](../rebuild/qualification.json) and [external record contracts](../../schemas/data/external-record-contracts.json) to record the tested profile, input, observed result and remaining uncertainty. A completed inventory and individually executed scenarios do not establish equivalence for every configuration or replacement system.
