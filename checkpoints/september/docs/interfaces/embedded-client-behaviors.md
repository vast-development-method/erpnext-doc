# Embedded client behavior contracts

This chapter specifies configurable form behaviors that calculate commercial product estimates, refresh negotiating probability and expose quotation/customer navigation. The [machine-readable behavior contracts](../../schemas/interfaces/embedded-client-behaviors.json) contain ordered events, formulas, service requirements and acceptance inputs and outputs. No executable client extension is needed to understand them.

These behaviors apply to the shared commercial domain described in [customer relationships and sales](../domains/customer-relationships-and-sales.md). Their form calculations are separate from authoritative [pricing and taxation](../domains/taxation-and-pricing.md), [record-save validation](../runtime/document-lifecycle-and-transactions.md) and [service permissions](service-contracts.md).

## Shared form context and event routing

A behavior registration has a full name, record kind, view kind, enabled marker, standard/default marker and behavior definition. The supported views are form and list. Loading retrieves enabled registrations that match both record kind and view. No matching registration returns no behavior; one returns one definition, and several return multiple definitions. The retrieval operation does not specify an explicit ordering between matching stored definitions, so conflict precedence must not be invented.

A parent form context supplies the current record, its ordered child collections, current actions and status choices, record metadata, notices and remote service invocation. Child behaviors share the parent record context. Row lookup accepts a child-collection name and an optional row position; absent or zero position falls back to the current child event position. It selects the row with that position, fills an absent parent identity from the displayed record and invokes the relevant child behavior. A missing collection or row produces a diagnostic and no row object. The product handlers below do not add a separate null-row recovery guard.

The supplied dispatcher evaluates built-in form behaviors before stored registrations. For stored behaviors, parent context must exist before a child behavior can attach. Each parent/child behavior receives the same underlying current data. A named child event invokes the corresponding child operation, while a parent event invokes the parent operation. Form save runs form validation and mandatory-field checking before calling the save service. Calculated values still require authoritative server-side acceptance; a browser formula is not a security boundary.

## Product amount and discount events

The product behavior is installed for both leads and negotiating opportunities. Each product row stores product identity/name, quantity, rate, gross amount, discount percentage, discount amount and net amount. The parent stores gross and net product totals. Each event changes the in-memory form values; it does not independently submit the record or post accounting.

| Event | Ordered effect |
| --- | --- |
| Product row added | Resolve the current row; invoke quantity calculation, including discount and parent-total refresh; invoke parent-total refresh once more |
| Product row removed | Recalculate the parent totals from the rows that remain |
| Quantity changed | Set gross amount to quantity multiplied by rate, then invoke discount calculation for the row |
| Rate changed | Resolve the current event row, set gross amount to quantity multiplied by rate, then invoke discount calculation |
| Discount changed and discount percentage is absent or zero | Set net amount to gross amount and discount amount to zero; refresh parent totals |
| Discount changed and both discount percentage and gross amount are nonzero | Set discount amount to gross amount multiplied by percentage divided by 100; set net amount to gross minus discount; refresh parent totals |
| Discount changed with nonzero percentage and zero gross amount | Neither discount assignment branch runs; retain prior discount/net values and refresh parent totals |

For ordinary numeric inputs:

$$
\operatorname{grossAmount}=\operatorname{quantity}\times\operatorname{rate}
$$

$$
\operatorname{discountAmount}=\operatorname{grossAmount}\times\operatorname{discountPercentage}/100
$$

$$
\operatorname{netAmount}=\operatorname{grossAmount}-\operatorname{discountAmount}
$$

The final two equations apply only to the nonzero-percentage/nonzero-amount branch. A full discount on gross 300 produces discount 300 and net zero. A cleared discount on gross 300 resets prior discount and yields net 300.

The zero-gross branch is a compatibility defect: a row previously carrying gross 300, discount percentage ten, discount amount thirty and net 270 can be changed to zero quantity. Gross becomes zero but discount thirty and net 270 remain because the percentage is nonzero and gross is zero. The parent can consequently show gross zero and net 270. Resetting those fields would be a deliberate correction, not an accurate description of this client behavior.

The client operations do not enforce nonnegative quantity, rate or percentage, cap the percentage at one hundred, or apply monetary rounding themselves. Negative numeric inputs can therefore calculate a negative discount or quantity in isolation. Field metadata, form validation and authoritative business validation must decide admissibility independently. Numeric zero is distinct from absence in rate response handling, as specified below.

## Parent product totals

Initialise gross total and net aggregate to zero. Visit all current product rows, sum their gross and net amounts, and remember whether any discount percentage is greater than zero. Store gross total. Store the nonzero net aggregate when present; otherwise store gross total. If the net aggregate is zero and at least one row has a positive discount, replace that fallback with the actual zero net aggregate.

This distinction preserves free products: one fully discounted row with gross 300 and net zero yields parent gross 300 and net zero. If rows have gross 300 and net zero but no positive discount, the fallback yields parent net 300. With no product rows, both totals are zero. The operation does not calculate or store a total quantity, despite the existence of an unused local quantity accumulator in the former implementation.

All row amounts must be numeric for meaningful aggregation. This contract does not prescribe string concatenation, implicit text conversion or invalid-number behavior as a legitimate commercial policy. A replacement must reject malformed nonnumeric values under its field contract and separately record any deliberate hardening difference.

## Product selection and asynchronous rate lookup

On product selection, capture the selected product identity and the row object, then request product-name/rate details with that product identity and the parent record identity as the opportunity context. This parent identity is supplied even when the behavior is running on a lead. The service attempts opportunity-based customer lookup with that identity; a lead-specific customer context is not independently selected by this request.

When the response arrives, stop if no response exists or if the row's current product identity differs from the captured identity. Otherwise replace the row's product name and rate. A missing or null returned rate becomes zero; an explicitly returned zero remains zero. Always replace an existing nonzero rate. Then invoke the rate event, which calculates gross, discount and parent totals in that order.

Example: Product One was selected, then Product Two before the first request returned. Product One's late response is ignored while the row still contains Product Two. The guard compares identity values only: if the user selects One, then Two, then One again, a late response from the first One request can still pass. It is not a request-version or row-membership guarantee.

The product handler does not locally catch a rejected lookup promise or display a custom failure notice. It does not guard against the captured row having been removed from the collection. Generic service errors and the form lifecycle must handle those cases. No stock quantity, stock reservation or inventory availability is fetched by this product-detail behavior.

## Product-rate service contract

The requested product supplies its display name and standard rate. Prefer a nonzero contextual price from the linked inventory product; otherwise return the standard rate. Thus contextual rate zero falls back to standard rate at the service selection step, although an explicit zero returned by the completed service is preserved by the client response handler.

Contextual pricing requires the optional linked inventory-product field, a populated inventory-product association and availability of inventory price records. Resolve the opportunity's linked customer when an opportunity identity is supplied. Select that customer's default price list when available, otherwise the default selling price list. If no usable price list exists, return no contextual rate.

The item-price lookup uses the selected price list, customer, inventory product's stock unit and current business date. Take the first returned price row. The price result can be a named record containing price-list rate or a positional result whose second value is rate; both representations select the same logical value. No returned rows means no contextual rate. The request does not supply quotation quantity, a chosen commercial packaging unit or the opportunity currency as extra pricing parameters. Those omissions must not be replaced by assumptions that this estimate executes every invoice pricing rule.

The price-details operation has no explicit product/opportunity read-permission check in its own body. Named service access, user permissions and the underlying lookup remain separate obligations. A replacement must document its authoritative access policy rather than infer permission from the fact that a form loaded successfully.

## Stage probability refresh

When the opportunity's stage changes, invoke the probability-refresh operation and await it. Request the stored probability from the stage-definition service using the stage currently selected when the request is made. On response, assign the returned probability directly to the opportunity probability field.

This always replaces the displayed probability; it is not limited to an absent or zero current probability. There is no local fallback when the probability property is missing, no local error handler and no stale-stage comparison before assignment. If Stage Early's request returns after Stage Advanced's request, the earlier result can overwrite the advanced probability while the selected stage remains Advanced. The authoritative save rules for [stage probability defaults](../domains/customer-relationships-and-sales.md#monetary-calculations-and-forecasts) remain separate from this interactive behavior.

Example: Early has probability ten and Advanced has probability seventy-five. Advanced responds first, so the form briefly has seventy-five. Early then responds and overwrites probability with ten even though Advanced remains selected. A replacement can protect this with a captured-stage/request-version check only as an explicitly declared correction.

## Quotation and customer actions

On form load, do nothing for a new unsaved opportunity. For a persisted opportunity, request the enabled state of the commercial integration settings. If enabled, run action registration; otherwise add no actions. This initial settings lookup has no local rejection handler.

Action registration appends a “Create Quotation” action immediately, then asynchronously requests a customer navigation link for the displayed opportunity. If a nonempty customer link is returned, append “View Customer.” Selecting either action opens its resolved destination in a new browsing context. Registration does not remove existing actions or deduplicate by label; repeated registration can therefore append duplicates.

“Create Quotation” requests a new-quotation destination using the opportunity identity and current organisation identity. A nonempty destination is opened. An empty result displays a quotation-creation failure notice. A rejected request displays the first supplied service message when available, otherwise a general quotation failure notice. Customer-link rejection similarly displays the first supplied message or a general customer-link failure notice. The handlers assume an error-message collection exists before reading its first element; errors lacking that collection need a separate robustness decision.

Requesting a quotation destination does not submit a quotation. For a local commercial installation, resolve an existing customer by explicit opportunity association, then by the customer identity stored on the opportunity. Use customer quotation party kind when found, otherwise negotiating-opportunity party kind. Supply the configured company, first primary contact, organisation address identity and original opportunity identity to the new-quotation destination.

For a separate commercial installation, create or resolve a prospect through the external service and use prospect party kind. Send organisation identity, lead name, employee-count range, owner, original opportunity, territory, industry, website, annual revenue, contacts, configured company and optional structured address. This navigation request can therefore create a remote prospect before the user saves a quotation. Retry safety for remote prospect creation must be specified by that external service.

The destination builder omits absent values but joins populated parameter names/values without explicit percent encoding. Names containing reserved destination characters need acceptance fixtures; secure encoded destination construction is a deliberate correction where the baseline does not provide it. Customer navigation selects a directly associated customer first and falls back to the opportunity's stored customer association in both local and external modes.

Related quotation prefilling takes product rows whose commercial product has a linked inventory product and skips unlinked products. It copies the inventory identity, quantity with a zero/absent fallback of one, rate with zero fallback and discount percentage with zero fallback. It does not preserve a deliberately zero quantity in this mapping and does not insert unlinked products merely by their display names.

## Default registration and maintenance

| Default behavior | Creation and maintenance policy |
| --- | --- |
| Product calculations for lead and opportunity | Create enabled standard form registration when missing; when present, replace stored behavior definition if it differs from the current default; do not otherwise reset its enabled marker |
| Opportunity probability refresh | Create enabled standard form registration when missing; existing definition is not overwritten by this creation operation |
| Opportunity quotation/customer actions | Create enabled standard form registration when missing; existing definition is not overwritten by this creation operation |
| Explicit quotation-action reset | Replace the existing action behavior when found and return success; return false when absent or on a logged failure; this operation does not itself re-enable a disabled registration |

Normal user editing of an existing standard registration is constrained outside installation, maintenance, fixture and test contexts. When development editing is disabled, a changed enabled marker is retained but other concurrent edits are discarded by reloading the stored definition. If the enabled marker did not change, the edit is rejected. Nonstandard registrations, new registrations and explicitly enabled development editing follow their own record permission checks.

The resulting specification separates standard behavior identity from executable implementation format. A replacement can implement these ordered rules in any language or declarative engine while preserving when each behavior loads, which mutable values it changes and what gets reset during maintenance.

## Acceptance and verification scope

The machine-readable catalog includes ordinary discounts, complete discounts, cleared discounts, zero-amount stale values, row removal, empty totals, null versus zero rates, rate replacement, stale product responses, repeated-selection limitations, out-of-order probability responses, action visibility, duplicate action registration, service failures and default-reset behavior. Isolated behavior evaluation can verify those transitions with controlled service responses. It does not establish complete browser rendering, user permissions, remote prospect identity, taxation or ledger posting.
