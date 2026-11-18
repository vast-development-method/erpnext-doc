# Selling and customer management

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Calling campaigns and contact suppression

Choose eligible contacts, sequence, calling script and quality controls, then allocate calls to agents. Recheck suppression at dispatch. Retain call disposition and recording access separately from invoicing billable units.

**Worked case.** A contact is selected for a campaign and joins the do-not-call list before dispatch. The scheduler attempts to assign the call with a different script language. The attempt is suppressed, no provider call is made and no billable unit is recorded. Suppression follows the dialling identity and applies to every script language.

### Additional decisions

Model the customer purchasing the campaign separately from each business contact being called. Track the import batch and source row, canonical contact/number, campaign membership, suppression entry, scheduled attempt, agent, call outcome and recording reference. A review stores its rubric version and links to one attempt. Put billable events through a distinct contract that references the campaign agreement and generated invoice line.

### Detailed workflow and cases

<a id="calling-campaigns-and-contact-suppression-2"></a>

#### Operating rules

1. Preview a filtered audience with counts for eligible, duplicate and suppressed contacts. Confirm an audience version and sequence before scheduling.
2. At dispatch, recheck current suppression and contact availability. Claim the next eligible attempt atomically and record who owns it. A call provider response completes that attempt. A later retry has its own identity.
3. A manager reviews recordings permitted for that campaign, using the rubric in force for the call. A billing user converts accepted billable events into invoice lines with a trace back to campaign activity.

<a id="calling-campaigns-and-contact-suppression-3"></a>

#### Acceptance cases

Store the agent’s interface language separately from the contact’s preferred language, outbound script variant and recording language. Translate review criteria and call outcomes by stable identifiers. A suppression applies to the dialling identity across every script language. Preserve a recorded conversation as spoken and label any subsequent translated transcript separately.

- Import the same normalised telephone number twice. After deduplication a two-step campaign has one eligible member and at most one assignment for the first step. A retry of the scheduling operation leaves that assignment intact.
- If an opted-out contact enters the Do Not Call list after audience selection and before dispatch, a Spanish script must stay suppressed even when the original campaign used English. Record the suppression decision and zero billable calls for that attempt.
- For a contract that charges per accepted review, two completed calls and one accepted review produce one billable unit. Reopening a review after invoicing produces a linked adjustment for approval.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/b2b_marketing.md).

## Business calendar follow-up

Define reminder levels, responsible caller, channel and working-day rule. Record promised payments separately from posted receipts and compare each promise with actual allocations.

**Worked case.** A quotation sent Friday at 09:00 is due for follow-up two working days later in Windhoek, without an intervening holiday. The owner opens the task in Afrikaans and the manager views it in German. They see one follow-up due on Tuesday at 09:00 Windhoek time. Language changes the captions. The business calendar and zone determine the deadline.

### Additional decisions

A rule owner selects the source record type, stable field predicates, assignee or recipient rule, time basis, trigger and localized message. For example, a quotation sent to a customer can require a sales follow-up two working days after dispatch while its state remains open. The organization's calendar supplies working days and the configured business time zone fixes the deadline. Store the resulting due instant, rule revision and the triggering document event.

Use stable codes for record states and condition operators. Each responsible colleague gets their own interface language. The due-time display uses the chosen display zone independently of language. Translate a missing notification from the configured rule fallback, while preserving customer notes and user-entered outcomes in their original language. A translated status label must not change which records match the rule.

### Detailed workflow and cases

<a id="business-calendar-follow-up-2"></a>

#### Operating rules

| Operation | Inputs | Result |
|---|---|---|
| Evaluate a candidate | Rule revision, source record ID and revision, business calendar | Create one pending occurrence when the predicate is true. Re-evaluating the same event reuses it. |
| Notify at due time | Occurrence ID, intended recipient, current time and current source state | Deliver an actionable alert only while the source still qualifies and the recipient may see it. Record the attempt and outcome. |
| Complete or supersede | Occurrence ID, actor and reason | Preserve who completed a follow-up. If the source is closed, mark an open occurrence superseded and exclude it from the overdue queue. |

| Acceptance example | Expected result |
|---|---|
| A Windhoek team configures weekdays only, no intervening holiday and a two-working-day delay at 09:00 local time. A quotation is sent Friday at 09:00. | The follow-up is due Tuesday at 09:00 in the configured business zone. An Afrikaans-speaking assignee and German-speaking manager see one occurrence with the same deadline. |
| The quotation converts before its due time and the scheduler retries a previously queued job. | Recheck the source, retain the superseded occurrence for review and emit no overdue alert. |
| A translated label for an open quotation changes after the rule was saved. | Existing pending work remains pending and newly qualifying quotations use the same state ID. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/follow_up.md).

## Marketplace inquiry conversion

Retrieve current inquiries periodically and allow a historical time window. Deduplicate by seller account and inquiry identifier. Conversion creates or returns a single linked lead while preserving the original customer text.

**Worked case.** The scheduled fetch and a historical window overlap for seller A and inquiry INQ-47. Import both windows, then request conversion in two different UI languages. Exactly one inquiry belongs to seller A and both conversion requests return the same lead ID. The original Hindi product name and provider inquiry ID remain unchanged.

### Detailed workflow and cases

<a id="marketplace-inquiry-conversion-2"></a>

#### Operating rules

| Operation | Input, state and result |
|---|---|
| Retrieve a window | Scope by tenant and seller account. Record window boundaries and provider time zone, identify each inquiry by its upstream ID within the account, preserve original contact details and product description. Record the last completed window only after its rows persist. |
| Reconcile the result | A replay updates the same inquiry. A second upstream ID from the same buyer remains a second inquiry and can receive a repeat classification. A changed email address is not a reason to create another copy of the first inquiry. |
| Convert | An authorized CRM user requests conversion for one inquiry. Atomically return its linked lead or create one and save that link. Keep the original upstream ID and the status history for reporting. |
| Report | Aggregate inquiries by event date in the seller's reporting zone and by stable status code. Counts of inquiries and converted leads answer different questions. Keep the contact-suppression reason through subsequent imports. |

<a id="marketplace-inquiry-conversion-3"></a>

#### Acceptance cases

- During overlapping scheduled and historical imports, inquiry INQ-47 containing the Hindi product name “कपड़ा” appears twice. The expected result is one inquiry. The French-speaking sales user sees localized filters and can search the original product text. Language detection must not change buyer identity, email or telephone.
- Two agents request conversion of INQ-47 using different UI languages. Both receive the same lead ID and the dashboard shows one converted inquiry. Source messages stay in their original script with an optional separately identified translation.
- If authentication fails halfway through a historical fetch, retain previously committed rows and the last completed boundary, return a localizable failure code, and keep the key out of user messages. Replay the window after credential recovery.
- When the account marks a buyer as do not contact, a same-buyer inquiry in a second language stays attributable to that buyer. A change in localized display wording cannot clear the suppression decision.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/indiamart.md).

## Party order dashboard

Filter submitted orders by transaction date, invoices by posting date and payment requests by creation instant. Drill down under the same scope used for the displayed total and distinguish paid from outstanding amounts.

**Worked case.** Two visible submitted orders for one customer total EUR 140; a third order is a draft. Open the submitted-order count and drill down under the same period filter. The dashboard shows 2 and EUR 140, and the drill-down returns exactly the two submitted order IDs. Changing the display language leaves the amount, filter and document identities unchanged.

### Additional decisions

A reader selects a company, party side, party and reporting period. Return one row per type, its count, amount buckets and a drill-down filter. Publish the type-specific date field, amount field, sign convention and eligible document states alongside the metric definition. For example, use submitted orders and their transaction dates for an ordered-value metric. An order, delivery and payment can describe the same sale. Present them as separate stages and do not sum their values into revenue.

Evaluate party, company and document permissions before aggregation and again for drill-down. Attribute a payment to its party and direction. If the implementation provides invoice allocation detail for payments, count each payment once at the payment level. Handle refunds and returns with the metric's published sign policy. Amounts use document currency buckets or an explicitly defined reporting-currency measure. A mixed-currency scalar without conversion evidence is invalid.

### Detailed workflow and cases

<a id="party-order-dashboard-4"></a>

#### Acceptance cases

| Scenario | Observable outcome |
|---|---|
| A reader has access to two submitted orders for customer C17, worth EUR 100 and EUR 40, and one further order is a draft | The proposed submitted-order tile shows count 2 and EUR 140. Opening the tile returns those two order IDs under the very same filters. |
| An accountant switches from German to Afrikaans | Labels, date and decimal presentation change. The query still uses the original party and document-type IDs and yields the same order list. Customer-supplied names remain searchable in their original script. |
| A third permitted order is denominated in NAD and the reporting-currency option is unset | Count becomes 3. EUR and NAD appear as distinct amount buckets, each with its currency code. |
| A supplier user cannot read another supplier's receipt | Counts, charts and drill-downs exclude that receipt. A translated document-type label cannot broaden the filter. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/insightly.md).

## Restaurant orders and kitchen rounds

Keep one active table order across service rounds. Route free preparation instructions to the kitchen and add billed extras as lines. Freeze dispatch identities per round before settling the final till invoice.

**Worked case.** A dish costs 60 and a billed add-on costs 5 before tax, with a free kitchen instruction. Dispatch the round twice with the same dispatch ID and pay the final order. One kitchen ticket is produced and one POS Invoice contains billable lines totaling 65 before tax. Arabic kitchen text and English checkout reference the same choice IDs and line amounts.

### Detailed workflow and cases

<a id="restaurant-orders-and-kitchen-rounds-3"></a>

#### Acceptance cases

1. Reserve four seats on the public Arabic booking page at outlet A. Enforce slot capacity atomically, return a stable reservation reference and show the guest’s original name to authorized staff. An English cashier marks that reservation seated. It links to the same table and one open order.
2. Two waiters open that table concurrently. At most one order remains open. Add one dish priced at 60 and its own taxable add-on priced at 5 in the outlet's currency; a free “omit onions” instruction adds zero. Before tax, billable lines sum to 65. The Arabic kitchen ticket and English till reference the same line IDs. Preserve free-text allergy notes and explicitly mark any translated copy.
3. Record a distinct dispatch ID for the first round. Retrying it returns the same ticket. Adding one more dish starts another round with only the newly ordered quantity. A cross-outlet merge fails and both existing orders retain their lines.
4. On payment, submit one POS Invoice for the final cart with the configured tax and tender rules. Switching receipt language cannot generate a second sale or change the applicable tax. If the kitchen printer fails after ticket creation, allow a reprint of that ticket with its original reference.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/lumen_restaurants.md).

## Offline till sales

Open a shift, scan items and accept payment. Keep each eligible offline sale queued under a durable local identity. On upload, retain the invoice number or rejection reason. Resolve outstanding uploads before shift close.

**Worked case.** An Arabic-speaking cashier has one eligible offline sale for two units. The device switches to German and retries after losing the upload acknowledgement. There is one posted invoice, one stock movement for two units and a German upload status referencing that invoice. The client sale key, posted quantities and original receipt language survive the locale switch.

### Additional decisions

Bind a sale to a company, outlet, open shift, device, cashier and client-generated sale ID. Preserve item identifiers, quantities, pricing context, tax amounts, payment legs, exchange rate where applicable and the receipt language in the sale snapshot. The server acknowledges each accepted submission with the original sale ID and invoice reference. Use a durable uniqueness constraint and reconcile the prior result after an acknowledgement is lost. A return references its sale and source lines. Constrain refundable quantities across online and offline returns at posting time.

Keep cashier interface, receipt language and accounting currency independently selectable. The offline cache needs the active locale's UI bundle, rendering fonts and readable rejection messages. Queue state, item identity, decimal amounts and tender codes remain stable when a cashier changes language mid-shift. Pass a preferred language for server errors and preserve a stable rejection code when localized text falls back. Retain customer/item names as recorded and render barcodes in their native direction.

### Detailed workflow and cases

<a id="offline-till-sales-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| An Arabic-speaking cashier sells two units offline, switches the till to German and reconnects after a lost acknowledgement. | One invoice and one set of stock/ledger effects exist. German status text identifies the uploaded invoice. Receipt reprint uses the stored output language. |
| A cashier tries to sell a serialized item offline while a separate eligible cash sale is queued. | The serialized sale is held for online validation, the eligible sale remains queued and shift close is blocked until the queue is settled. |
| Two devices return the last refundable unit of the same sale. | At most one return posts. The other shows a translated conflict with the original sale reference and retains its review state. |

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/lumenpos.md).

## Open commerce order confirmations

Publish seller and item identities alongside localized catalogue text. Match signed order confirmations to the original seller, product and correlation identity. A duplicate confirmation must return the existing order and reservation.

**Worked case.** An English/Hindi catalog exposes one SKU and one two-unit order confirmation. The network repeats the identical confirmation after the operator changes language. The gateway returns the same outcome and a single order reserves two units. Catalog text may vary; seller IDs, SKU, correlation IDs and signed messages remain identical.

### Additional decisions

A catalog manager maps seller, location, item, unit and fulfilment IDs into a chosen, versioned network profile. Attach localized display descriptions and keep the published catalog revision. A seller gateway correlates each network transaction and message with the ERP quotation/order, stores the accepted response and distinguishes acknowledged receipt from successful confirmation. A confirmed sale uses a consistent price/stock snapshot and explicitly names the inventory reservation or rejection. Final fulfilment, invoicing, cancellation and refund require separate business transitions and references.

Choose storefront copy using the language options defined by the agreed network profile. If only one description is supported on that exchange, publish the configured default and record which locale was transmitted. Preserve wire action names, participant IDs, merchant SKU, timestamps and signed payload bytes across dashboard language changes. Show the original buyer-entered address beside any translated service notes.

### Detailed workflow and cases

<a id="open-commerce-order-confirmations-1"></a>

#### Operating rules

| Proposed acceptance case | Expected result |
|---|---|
| One catalog revision offers the same SKU in English and Hindi. A buyer confirms two units and repeats the same confirmation. | Both displays refer to one item and price. The same network message returns the same order outcome, with a single ERP order and reservation of two units. |
| Stock is exhausted after the quote but before confirmation. | The seller returns the protocol-defined failure for the negotiated version and a localized explanation for staff. No order is marked fulfilled or invoiced. |
| A callback is delayed and the operator changes interface language while waiting. | Reconciliation still matches the original transaction and callback IDs. The original response bytes and correlation record remain unchanged. |

#### Reserving a confirmed quote

Persist the incoming transaction ID, message ID, seller identity and the frozen quote revision. Bind order lines to catalog and fulfilment IDs, quantities, unit prices, currency, charges and the quote expiry instant. Keep the acknowledgement of message receipt separate from the seller’s decision and its callback. A callback recovery record references the same accepted order and quote.

For an independent seller policy, a quote permits two units at 120 each plus delivery of 30 in the quoted currency. A valid confirmation inside the expiry instant creates one order for 270, one reservation of two units and one callback identity. If dispatching the callback times out, replay that callback identity. A retry with the same message key but an added third unit is a conflict; it cannot change the order or reserve another unit. Actual message fields, signatures and version-specific extension keys belong to the negotiated network profile.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/ondc_seller_app.md).

## Retail shift settlement

Track sales, returns and tenders under the active shift. At closing, calculate counted minus expected for each payment method. Keep cash opening balances and changes of tender distinct from card receipts.

**Worked case.** A shift opens with cash of 100.00, takes 200.00 in cash and 50.00 by card, and refunds 30.00 in cash. Close the shift with counted cash of 268.00 and card movement of 50.00. Expected cash is 270.00, the cash shortage is 2.00 and the card difference is zero. Arabic and English closing screens refer to the same shift, method identifiers, amounts and discrepancy.

### Detailed workflow and cases

<a id="retail-shift-settlement-2"></a>

#### Operating rules

| Proposed operation | Contract and state |
|---|---|
| Open shift | Bind cashier, terminal, POS profile, company, warehouse, operating currency, opening time and opening amount per tender. Return a stable shift ID. |
| Build cart | A scan identifies a product and where relevant its serial or batch. Store item ID, quantity, unit, price and tax configuration on the line. A draft can be resumed across language changes. |
| Complete sale or return | Validate tracked inventory, prices and tender totals on the authoritative service. Use a durable sale key for offline submissions. Link returns to sold lines and enforce the remaining returnable quantity. Return the committed invoice and payment IDs. |
| Close shift | Require outstanding offline submissions to be resolved or explicitly carried forward. Compare expected with counted per tender and record differences separately. Handle overages and shortages with an authorized explanation. |

<a id="retail-shift-settlement-3"></a>

#### Acceptance cases

A cashier scans a serial-labelled item under an Arabic interface and saves a draft. An authorized English-speaking operator resumes it and sees the identical serial, warehouse, tax and quantity. A receipt can use the customer's language. Keep serials and barcodes in their original character order when embedded in right-to-left text.

For a synthetic shift, open cash with 100.00, receive 200.00 cash and 50.00 card, and refund 30.00 cash. Expected cash is 270.00 and expected card movement is 50.00. Counts of 268.00 and 50.00 yield a 2.00 cash shortage. Both UI languages show the same discrepancy and original transactions. Replaying an already acknowledged offline sale produces one invoice. A request for a serial already sold on another terminal requires review.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/retail.md).

## Restaurant multi-station fulfilment

Map menu categories to kitchen or bar stations. A table round retains the selected items, units, modifiers and guest note. Route each station only its quantities and add all billable units to the same visit.

**Worked case.** A restaurant visit has two portions of a food item and one drink, each assigned to the corresponding preparation station. Submit the Nepali guest order twice with the same submission key. The English-speaking kitchen gets two portions, the German-speaking bar gets one drink, and the bill contains exactly three units. Station and item codes, quantities, modifiers and prices survive language changes. Preserve any original guest note.

### Additional decisions

The guest selects an outlet, table and menu language from the QR entry point. Store the table visit, menu revision, item and modifier codes, quantities, captured prices and original free-text instructions. Route items by configured station code. The guest, waiter, kitchen, bar and cashier can each select their language independently. Translate curated item and modifier names for each audience. Preserve original notes and identify any accompanying translation. Billing resolves one or more tenders against the same visit. A hotel integration requires an explicit room-account match and acknowledged charge reference.

### Detailed workflow and cases

<a id="restaurant-multi-station-fulfilment-2"></a>

#### Operating rules

1. A guest orders two portions of one food item and one drink under a Nepali menu. An English-speaking kitchen and a German-speaking bar each receive the applicable ticket lines. Kitchen quantity is two, bar quantity one, the table check contains all three units and one submission retry produces no further ticket.
2. A translated item label changes after acceptance. Print the guest receipt in their selected language while retaining the ordered item ID, captured price and modifier code. A missing approved translation for a dietary instruction shows the original text with its language.
3. A second terminal attempts to settle the same checked-out visit. Return the existing receipt or an explicit conflict without charging a second tender. A copied QR for a closed visit must resolve the current table context before accepting another order.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/sajha_menu.md).

## Reviewed sales reminders

Restrict staff and customer views to authorized commercial documents. A scheduled or document-triggered run can produce a preview or pause for approval. Bind approval to the recipient, exact message content and business record before releasing the dispatch.

**Worked case.** A German-speaking manager selects an ageing quotation for an Afrikaans-speaking customer. Run a dry preview, approve the corresponding live reminder, replay the scheduler, then edit the originally approved wording. The preview sends nothing, one approved message is delivered, and the revised wording requires a new approval. Approval binds to the recipient-language content, record and recipient. Changing the manager’s interface language cannot authorize a different message.

### Detailed workflow and cases

<a id="reviewed-sales-reminders-1"></a>

#### Operating rules

1. A scheduled playbook selects quotations satisfying its configured age and status. Constrain the query to its company and authorized records. Identify a run by the trigger, business record and evaluation window.
2. Create a proposed reminder with recipient, source quotations, contact language, template version and a stable message preview. Record any generated content as a proposal. The approving manager sees exactly what the recipient will receive.
3. Bind approval to the proposal digest. Recheck record access, recipient, quote status and action permission before sending. A changed proposal or newly accepted quotation requires reevaluation. Persist one dispatch outcome and delivery reference per approved operation.
4. The customer portal uses its own tools and identity. A translated question or quoted record name cannot expand the authenticated customer's scope. A model budget stop returns the run status and any unsent proposal.

<a id="reviewed-sales-reminders-2"></a>

#### Acceptance cases

A German-speaking manager starts a dry run for a seven-day-old quotation for an Afrikaans-speaking contact. The interface explains the proposal in German and shows the exact Afrikaans customer message. The dry run sends zero messages. Approve a live proposal once and deliver precisely one reminder, even if the scheduler repeats. If someone edits its Afrikaans text after approval, require approval of the new version. Preserve original customer names, quoted amounts and identifiers across prompts and outputs.

From another customer's portal account, request the quotation in English and Simplified Chinese. In both languages return the same access outcome without disclosing the amount, identity or existence of the record. Log the decision code and masked record context consistently.

[Implementation evidence and scope](../../rebuild/marketplace-guides/apps/sales_ai.md).
