# Selling and customer management

The workflow defines the business decision. The worked case supplies a concrete acceptance outcome.

## Calling campaigns and contact suppression

Choose eligible contacts, sequence, calling script and quality controls, then allocate calls to agents. Recheck suppression at dispatch. Retain call disposition and recording access separately from invoicing billable units.

**Worked case.** A contact is selected for a campaign and joins the do-not-call list before dispatch. The scheduler attempts to assign the call with a different script language. The attempt is suppressed, no provider call is made and no billable unit is recorded. Suppression follows the dialling identity and applies to every script language.

### Additional decisions

Model the customer purchasing the campaign separately from each business contact being called. Track the import batch and source row, canonical contact/number, campaign membership, suppression entry, scheduled attempt, agent, call outcome and recording reference. A review stores its rubric version and links to one attempt. Put billable events through a distinct contract that references the campaign agreement and generated invoice line.

## Business calendar follow-up

Define reminder levels, responsible caller, channel and working-day rule. Record promised payments separately from posted receipts and compare each promise with actual allocations.

**Worked case.** A quotation sent Friday at 09:00 is due for follow-up two working days later in Windhoek, without an intervening holiday. The owner opens the task in Afrikaans and the manager views it in German. They see one follow-up due on Tuesday at 09:00 Windhoek time. Language changes the captions. The business calendar and zone determine the deadline.

### Additional decisions

A rule owner selects the source record type, stable field predicates, assignee or recipient rule, time basis, trigger and localized message. For example, a quotation sent to a customer can require a sales follow-up two working days after dispatch while its state remains open. The organization's calendar supplies working days and the configured business time zone fixes the deadline. Store the resulting due instant, rule revision and the triggering document event.

Use stable codes for record states and condition operators. Each responsible colleague gets their own interface language. The due-time display uses the chosen display zone independently of language. Translate a missing notification from the configured rule fallback, while preserving customer notes and user-entered outcomes in their original language. A translated status label must not change which records match the rule.

## Marketplace inquiry conversion

Retrieve current inquiries periodically and allow a historical time window. Deduplicate by seller account and inquiry identifier. Conversion creates or returns a single linked lead while preserving the original customer text.

**Worked case.** The scheduled fetch and a historical window overlap for seller A and inquiry INQ-47. Import both windows, then request conversion in two different UI languages. Exactly one inquiry belongs to seller A and both conversion requests return the same lead ID. The original Hindi product name and provider inquiry ID remain unchanged.

## Party order dashboard

Filter submitted orders by transaction date, invoices by posting date and payment requests by creation instant. Drill down under the same scope used for the displayed total and distinguish paid from outstanding amounts.

**Worked case.** Two visible submitted orders for one customer total EUR 140; a third order is a draft. Open the submitted-order count and drill down under the same period filter. The dashboard shows 2 and EUR 140, and the drill-down returns exactly the two submitted order IDs. Changing the display language leaves the amount, filter and document identities unchanged.

### Additional decisions

A reader selects a company, party side, party and reporting period. Return one row per type, its count, amount buckets and a drill-down filter. Publish the type-specific date field, amount field, sign convention and eligible document states alongside the metric definition. For example, use submitted orders and their transaction dates for an ordered-value metric. An order, delivery and payment can describe the same sale. Present them as separate stages and do not sum their values into revenue.

Evaluate party, company and document permissions before aggregation and again for drill-down. Attribute a payment to its party and direction. If the implementation provides invoice allocation detail for payments, count each payment once at the payment level. Handle refunds and returns with the metric's published sign policy. Amounts use document currency buckets or an explicitly defined reporting-currency measure. A mixed-currency scalar without conversion evidence is invalid.

## Restaurant orders and kitchen rounds

Keep one active table order across service rounds. Route free preparation instructions to the kitchen and add billed extras as lines. Freeze dispatch identities per round before settling the final till invoice.

**Worked case.** A dish costs 60 and a billed add-on costs 5 before tax, with a free kitchen instruction. Dispatch the round twice with the same dispatch ID and pay the final order. One kitchen ticket is produced and one POS Invoice contains billable lines totaling 65 before tax. Arabic kitchen text and English checkout reference the same choice IDs and line amounts.

## Offline till sales

Open a shift, scan items and accept payment. Keep each eligible offline sale queued under a durable local identity. On upload, retain the invoice number or rejection reason. Resolve outstanding uploads before shift close.

**Worked case.** An Arabic-speaking cashier has one eligible offline sale for two units. The device switches to German and retries after losing the upload acknowledgement. There is one posted invoice, one stock movement for two units and a German upload status referencing that invoice. The client sale key, posted quantities and original receipt language survive the locale switch.

### Additional decisions

Bind a sale to a company, outlet, open shift, device, cashier and client-generated sale ID. Preserve item identifiers, quantities, pricing context, tax amounts, payment legs, exchange rate where applicable and the receipt language in the sale snapshot. The server acknowledges each accepted submission with the original sale ID and invoice reference. Use a durable uniqueness constraint and reconcile the prior result after an acknowledgement is lost. A return references its sale and source lines. Constrain refundable quantities across online and offline returns at posting time.

Keep cashier interface, receipt language and accounting currency independently selectable. The offline cache needs the active locale's UI bundle, rendering fonts and readable rejection messages. Queue state, item identity, decimal amounts and tender codes remain stable when a cashier changes language mid-shift. Pass a preferred language for server errors and preserve a stable rejection code when localized text falls back. Retain customer/item names as recorded and render barcodes in their native direction.

## Open commerce order confirmations

Publish seller and item identities alongside localized catalogue text. Match signed order confirmations to the original seller, product and correlation identity. A duplicate confirmation must return the existing order and reservation.

**Worked case.** An English/Hindi catalog exposes one SKU and one two-unit order confirmation. The network repeats the identical confirmation after the operator changes language. The gateway returns the same outcome and a single order reserves two units. Catalog text may vary; seller IDs, SKU, correlation IDs and signed messages remain identical.

### Additional decisions

A catalog manager maps seller, location, item, unit and fulfilment IDs into a chosen, versioned network profile. Attach localized display descriptions and keep the published catalog revision. A seller gateway correlates each network transaction and message with the ERP quotation/order, stores the accepted response and distinguishes acknowledged receipt from successful confirmation. A confirmed sale uses a consistent price/stock snapshot and explicitly names the inventory reservation or rejection. Final fulfilment, invoicing, cancellation and refund require separate business transitions and references.

Choose storefront copy using the language options defined by the agreed network profile. If only one description is supported on that exchange, publish the configured default and record which locale was transmitted. Preserve wire action names, participant IDs, merchant SKU, timestamps and signed payload bytes across dashboard language changes. Show the original buyer-entered address beside any translated service notes.

## Retail shift settlement

Track sales, returns and tenders under the active shift. At closing, calculate counted minus expected for each payment method. Keep cash opening balances and changes of tender distinct from card receipts.

**Worked case.** A shift opens with cash of 100.00, takes 200.00 in cash and 50.00 by card, and refunds 30.00 in cash. Close the shift with counted cash of 268.00 and card movement of 50.00. Expected cash is 270.00, the cash shortage is 2.00 and the card difference is zero. Arabic and English closing screens refer to the same shift, method identifiers, amounts and discrepancy.

## Restaurant multi-station fulfilment

Map menu categories to kitchen or bar stations. A table round retains the selected items, units, modifiers and guest note. Route each station only its quantities and add all billable units to the same visit.

**Worked case.** A restaurant visit has two portions of a food item and one drink, each assigned to the corresponding preparation station. Submit the Nepali guest order twice with the same submission key. The English-speaking kitchen gets two portions, the German-speaking bar gets one drink, and the bill contains exactly three units. Station and item codes, quantities, modifiers and prices survive language changes. Preserve any original guest note.

### Additional decisions

The guest selects an outlet, table and menu language from the QR entry point. Store the table visit, menu revision, item and modifier codes, quantities, captured prices and original free-text instructions. Route items by configured station code. The guest, waiter, kitchen, bar and cashier can each select their language independently. Translate curated item and modifier names for each audience. Preserve original notes and identify any accompanying translation. Billing resolves one or more tenders against the same visit. A hotel integration requires an explicit room-account match and acknowledged charge reference.

## Reviewed sales reminders

Restrict staff and customer views to authorized commercial documents. A scheduled or document-triggered run can produce a preview or pause for approval. Bind approval to the recipient, exact message content and business record before releasing the dispatch.

**Worked case.** A German-speaking manager selects an ageing quotation for an Afrikaans-speaking customer. Run a dry preview, approve the corresponding live reminder, replay the scheduler, then edit the originally approved wording. The preview sends nothing, one approved message is delivered, and the revised wording requires a new approval. Approval binds to the recipient-language content, record and recipient. Changing the manager’s interface language cannot authorize a different message.
