# Customer relationships and sales

Read this chapter with [company eligibility](company-and-master-governance.md), [products and units](products-units-and-packaging.md), [pricing and taxes](taxation-and-pricing.md), [customer receivables](accounts-receivable.md) and [service response promises](service-and-support.md). Calculation definitions and exact numerical fixtures are maintained in the [customer and service calculations](../../schemas/mathematics/customer-and-service-calculations.json) and [acceptance cases](../../schemas/mathematics/customer-and-service-acceptance-cases.json).

## Unified record contracts

| Logical record | Required distinctions | Internal field definitions |
| --- | --- | --- |
| Person contact | Person identity, primary and additional communication channels, organisation and party associations; one person can represent several organisations | [Contact](../../schemas/data/record-types/contact.json) |
| Organisation | Institutional identity and descriptive commercial attributes; it does not itself establish a receivables account | [Relationship organisation](../../schemas/data/record-types/customer_relationship_organization.json) |
| Lead | Captured interest, qualification stage, owner, origin, captured person/organisation details, converted marker and response clock | [Relationship lead](../../schemas/data/record-types/customer_relationship_lead.json), [sales lead](../../schemas/data/record-types/lead.json) |
| Commercial opportunity | Organisation, original lead, contact rows, negotiating stage, proposed products, expected value, actual commercial value and expected close date | [Relationship opportunity](../../schemas/data/record-types/customer_relationship_deal.json) |
| Sales enquiry | Lead, prospect or customer origin; requested item quantities and rates; quotation progress, loss reasons and competitors | [Sales enquiry](../../schemas/data/record-types/opportunity.json) |
| Customer | Selling party role, customer group, territory, company-specific accounting and credit configuration, contacts and addresses | [Customer](../../schemas/data/record-types/customer.json) |
| Quotation | Dated commercial offer, validity, currency, product and tax rows, optional alternatives, commercial terms and resulting order progress | [Quotation](../../schemas/data/record-types/quotation.json) |
| Customer order | Accepted quantities and prices, delivery schedules, source quotation rows, project, reservations, supplier-direct delivery and billing/delivery progress | [Customer order](../../schemas/data/record-types/sales_order.json) |

These records belong to one commercial domain. A replacement can unify overlapping descriptive fields, contacts, stages, calendars and activities, while retaining the different behaviors in this table. It must not remove the enquiry-to-quotation workflow when implementing the richer negotiating opportunity, nor interpret the opportunity's won state as a submitted order. Preserve identity mappings when one migrated commercial case has both representations.

All child rows retain stable identity and parent linkage. Product-row position is presentation order; it is not a substitute for row identity in quotation conversion, alternative selection, cancellation or audit. Documents preserve the commercial descriptions and monetary values accepted at their own transaction time instead of silently refreshing historical offers from the current product master.

## Purpose and record boundaries

The commercial journey begins with an interested person or organisation, progresses through qualification and negotiation, and produces an accepted commercial document. A lead, a person, an organisation, an opportunity, and a customer are different business identities. Conversion preserves the lead and creates or associates the identities required for the next operation. A salesperson winning an opportunity does not itself recognise revenue, consume stock, create a receivable, or settle an invoice.

Use one shared contact model for people, one organisation model for institutional identity, and a customer role for the party to whom goods or services are sold. Contacts have child collections of electronic mail addresses and telephone numbers, with primary selections. An organisation holds its name, website, territory, industry, annual revenue, and employee-count range. A commercial opportunity holds the organisation reference, lead origin, one or more contacts, salesperson, expected and actual commercial value, currency, expected closure date, closure date, proposed products, stage history, and communication response measurements. Do not use a telephone number as an unconditional person-identity key: a household or office can share it.

The combined model needs separate dimensions for qualification stage, commercial outcome, conversion state, communication state, and sales-document progress. Configurable stage labels have a category of open, ongoing, on hold, won, or lost, along with display order and colour. Commercial stages may have a default probability. Sales-document progress also distinguishes an open enquiry, one with a quotation, a converted enquiry, a lost enquiry, a replied enquiry, and a closed enquiry. Preserve these dimensions; a display label such as “qualified” must not replace evidence that a customer or order has actually been created.

## Lead capture and validation

A lead display name is assembled from the available salutation, first name, middle name, and last name. When the person name is absent, an organisation name supplies the display name; an electronic mail address may supply its local part. The title prefers organisation name over person name. Normal interactive creation must reject a lead without the required identifying information. The business interface must distinguish required capture fields from fallback name derivation used by import and other controlled creation paths.

Validate electronic mail syntax, and reject a lead whose electronic mail address equals its assigned owner's account address. Lead duplication by electronic mail is a configurable policy in the sales document journey. The contact reuse operation during opportunity conversion looks up a contact by electronic mail; merely matching a telephone number does not reuse a contact. These are separate checks: allowing duplicate leads does not authorise duplicate contact creation during conversion.

A new lead defaults to the configured initial qualification stage, preferring the seeded initial stage when it exists. A lost stage requires a loss reason. The general “other” reason additionally requires explanatory notes. The lead retains a stage-change history. A stage movement and a conversion are separate operations because conversion also creates linked records, changes the converted marker, transfers assignments, and affects the working list.

## Conversion contract

The conversion command accepts a lead identifier, optional existing contact identifier, optional existing organisation identifier, and optional opportunity values. It requires write permission on the lead, except for a trusted internal creation path with an explicit permission bypass. The resulting opportunity identifier is the command result.

The operation marks the lead converted and, when the corresponding configuration exists, moves it to the qualified label and marks its communication replied. Contact resolution first honours an explicitly supplied contact; otherwise it reuses a contact with matching electronic mail or creates a contact. Reuse refreshes selected lead contact details from the existing contact. New contact creation preserves name, salutation, gender, job title, organisation text, image, electronic mail, and primary telephone selections. Organisation resolution similarly honours an explicit association, otherwise reuses a matching organisation name or creates an organisation using its captured commercial attributes.

The new opportunity references the original lead and contact. Copy compatible business fields, mapping lead owner to opportunity owner. Do not copy record identity, creation and modification metadata, submission state, stage, primary contact projections, response policy identity, or stage history as if they were fresh business inputs. Matching custom fields can transfer by identical field identity; otherwise a custom field transfers only when there is exactly one destination custom field with the same label and value kind. An ambiguous pair of matching labels must not be guessed.

When the lead has already received a first response, transfer its response clock origin, response deadline, response result, communication state, first-response duration, and first-response timestamp. This is a conditional preservation rule, not an unconditional reset or unconditional copying of all response state. Additional assigned users are transferred to the opportunity. The conversion command does not establish an explicit guard that makes repeated conversion calls return one existing opportunity; any claim of retry-safe conversion requires a separate completed acceptance check.

## Ownership, sharing, and contact projections

An owner assignment is not merely a label. Changing the lead or opportunity owner grants write sharing to that user and removes other direct shares through the defined owner-management operation. Adding an assignment makes its recipient the current owner, even when an earlier owner existed. Cancelling any assignment clears the single owner field, including cancellation of one of several co-assignees. The assignment operation also creates an in-application notification. Direct assignment creation requires write access to the referenced lead or opportunity. These consequences must be visible in permission and event acceptance scenarios.

For an opportunity with exactly one contact, select that contact as primary automatically. Reject multiple primary contacts. With no primary contact, clear the opportunity's electronic mail, mobile telephone, and telephone projections. Selecting a primary contact trims those projected values. Updating a contact propagates its current primary electronic mail and mobile telephone values to linked opportunities where the contact is primary. Contact editing requires contact write permission, and fetching contact details through an opportunity must honour opportunity read permission.

## Monetary calculations and forecasts

Product suggestions are commercial estimates. Each row has a quantity, rate, amount, discount percentage, discount amount, and net amount. The standard interactive calculations are:

| Output | Calculation |
| --- | --- |
| Product amount | Quantity multiplied by rate |
| Product discount amount | Product amount multiplied by discount percentage divided by 100 |
| Product net amount | Product amount minus product discount amount |
| Opportunity product total | Sum of product amounts |
| Opportunity product net total | Sum of product net amounts; when no net amounts and no discount are present, use product total |

A 100 percent discount must produce a genuine zero net total. Do not replace this zero with the gross product total. The interactive product calculation explicitly distinguishes an empty net aggregate from a zero caused by a discount. Product-rate responses also guard against a user changing product selection while an earlier lookup is still in progress. These interactive calculations occur in the interactive form machinery; acceptance must separately verify that noninteractive writes enforce the same derived totals before relying on them for authoritative monetary processing.

For a sales enquiry with item rows, quantities must be positive and respect whole-unit requirements. Item amount equals rate multiplied by quantity; company-currency rate and amount equal their transaction-currency values multiplied by the conversion rate. Equal transaction and company currency force a rate of one. Otherwise an absent rate, or a rate of one, triggers a dated exchange-rate lookup. This differs from a freely editable probability-weighted forecast and must remain part of the quotation-preparation contract.

When forecasting is enabled, expected opportunity value must be nonzero and expected closure date is mandatory. If probability is absent or zero, replace it with the stage default, otherwise zero. Consequently, an explicit zero can be replaced by a nonzero stage default. The automatic expected-value setting updates an existing nonzero expected value from nonzero product net total, otherwise product total. It does not initialise every blank expected value. Moving into a won-category stage sets closure date to the current date. Do not claim this automatically records a final invoice value. Monetary fields covered by the defined tests reject negative values.

The monthly forecast report has an unusual current calculation that must remain visible:

| Stage category | Forecast contribution | Actual commercial contribution |
| --- | --- | --- |
| Lost | Expected value multiplied by stored exchange rate | Zero |
| Won | Expected value multiplied by probability divided by 100 and by stored exchange rate | Actual opportunity value multiplied by stored exchange rate |
| Other categories | Expected value multiplied by probability divided by 100 and by stored exchange rate | Zero |

The report groups by expected closure month, includes expected closure dates from twelve months before the current date onward, and optionally filters salesperson. An absent exchange rate is treated as one; absent probability is treated as zero. The report command accepts beginning and ending date parameters but its specified selection uses the twelve-month lower boundary instead. Zero aggregates are converted to blank output. These are specified compatibility rules, including the lost-opportunity contribution. Excluding lost opportunities from forecast is a plausible alternative policy, but it is a proposed change, not a fact about the defined calculation.

## Quotation, commitment, and accounting boundary

An opportunity may originate from a lead, prospect organisation, or existing customer. An incoming electronic mail address can resolve an existing customer through a contact, otherwise an existing lead, otherwise a newly created lead. Creating an opportunity from a lead links open activities and, when enabled, carries communications and comments forward. Declaring an enquiry lost is rejected while an active submitted quotation exists. Retain multiple loss reasons and competitors for this sales-document operation even though the qualification-stage operation uses a single selected loss reason.

A quotation validates its expiry date against transaction date, whole-unit quantities, customer identity, and packing composition. It may contain alternative products and, when enabled, zero-quantity rows that communicate a unit price. Quotation order progress compares ordered stock quantities against source row stock quantities. When alternatives exist, the progress calculation considers the alternatives that were actually selected in submitted orders. A quotation is partially ordered while any relevant row is missing or under-ordered; it is ordered when all relevant rows are covered.

An order validates delivery requirements, dates, project/customer compatibility, customer purchase reference, warehouse, direct supplier delivery, reservations, preceding document references, coupon, blanket agreement, and intercompany association. Submission checks customer credit and approving authority, updates reserved quantities, project totals, prior document progress, blanket agreement, coupon usage, and intercompany links. Cancellation removes delivery schedules and reservations, updates linked progress and coupon counts, and rejects a closed order until it is reopened. The sales domain must invoke the inventory and accounting contracts for these consequences; it must not independently invent a second credit or stock ledger.

## Acceptance scenarios

1. Convert a lead with the same electronic mail as an existing contact and a different telephone number. Reuse the contact, retain the source lead reference, and project the reused contact's current details.
2. Convert two people who share a telephone number but have different or absent electronic mail addresses. Do not merge them merely because the telephone matches.
3. Attempt conversion without lead write access. Create no contact, organisation, opportunity, or converted marker.
4. Set two primary contacts on one opportunity. Reject the change. Remove all primary selections and verify that displayed contact projections are cleared.
5. Cancel one of two assignments and verify that the owner field is cleared while the remaining assignment record is preserved according to the assignment service.
6. Save a lost stage without a reason, then with “other” but no explanation. Reject both.
7. Use quantity 12, rate 25, and discount 10 percent. Produce amount 300, discount 30, and net amount 270. With discount 100 percent, preserve net amount zero.
8. Use expected value 10,000, probability 40 percent, and exchange rate 1.2. An ongoing stage contributes 4,800 to forecast; the currently observed lost-stage calculation contributes 12,000.
9. Create an alternative-product quotation, order one selected alternative, and verify order-progress evaluation excludes unselected alternatives.
10. Compare converted opportunity, submitted order, submitted invoice, and received payment. They must remain distinct records with different financial consequences.

The defined conversion and validation tests support several of these behaviours. They were read, not executed in a running application. The scenarios above include additional proposed cross-interface checks; their presence is not evidence of a passing runtime test.

## Commercial commands and failure boundaries

| Command | Preconditions | Durable result and downstream effects |
| --- | --- | --- |
| Capture lead | Capture policy, required identifying values, valid electronic mail and duplicate policy | A lead identity, initial qualification stage, owner/assignment, optional response policy and activity history |
| Change stage | Write permission; destination stage exists; loss reason requirements satisfied | New stage plus history; conversion and posting states do not change merely because the stage label changes |
| Convert lead | Lead write permission and valid explicit associations | Retained lead plus linked contact, organisation and opportunity as described in the conversion contract |
| Change owner | Permission to write the commercial record | Owner, assignment and direct sharing change together; notification uses the selected user's identity |
| Create quotation | Origin readable and mappable; currency and item values resolved | Draft offer retaining origin links; no stock or ledger effect |
| Accept quotation into order | Valid selected rows, eligible customer/company and quantities | Draft order preserving source-row relationships; stock commitment occurs on submission |
| Submit order | Submission authority, approval threshold, credit and product/company eligibility | Submitted commitment, reservation and upstream progress changes; neither receivable nor revenue is created solely by the order |
| Cancel order | Cancellation authority and valid downstream reversal ordering; reopen a closed order first | Cancelled commitment with reservations, schedules, coupon usage and linked progress adjusted |

Conversion must preserve the complete result relationship so that failures can be distinguished from a command that committed but whose response was lost. The specified existing conversion does not guarantee one opportunity per repeated request. A replacement that supplies request deduplication must declare this as an additional command reliability policy and give the caller an explicit already-converted result; it must not silently discard a legitimate request to create another opportunity.

Changes to contact, organisation and opportunity projections require one consistent save boundary. Permission denial must occur before creating a contact or organisation. A failure after contact creation requires rollback or a documented recoverable partial result; no runtime rollback claim is established merely by the order of validation described here. This is an acceptance obligation for the replacement's transaction service.

## Product pricing versus forecast value

The opportunity product estimate is not the authoritative tax engine. Product quantity multiplied by rate gives gross product amount; a percentage discount reduces that amount. Net amount zero from a full discount must remain zero in the product summary. Separately, automatic expected-value refresh selects the nonzero net total, otherwise gross total, and only runs when the existing expected value is nonzero. Thus a fully discounted product estimate can have net total zero while its automatically refreshed forecast value is gross total. Both results must be retained as distinct field decisions until an explicit changed policy is adopted.

Example: twelve units at 25 have gross amount 300. With a full discount, the product net amount is zero. If an existing expected opportunity value of 200 is automatically refreshed, the current selection rule uses gross 300 because net zero is not selected. This is a forecast-field compatibility exception, not permission to invoice the customer for 300.

Sales-document product pricing additionally resolves the selected unit, stock-unit conversion, price list and currency, dated price, customer or customer-group context, quantity-based pricing rules, discounts, inclusive or exclusive tax, and rounding. Those calculations are owned by [taxation and pricing](taxation-and-pricing.md). A product sold in a pack of six at 90 per pack produces 180 for two packs and twelve stock units; the sales row must retain both two packs and twelve stock units. Comparing the ordered pack count directly to the quotation's stock quantity would incorrectly report incomplete ordering.

Expected and actual opportunity values remain separate from invoiced and paid values. The forecast conversion rate targets the commercial workspace's reporting currency and refreshes when currency changes or the stored rate is absent. It need not be the same dated rate later used by the invoice. Never reconcile forecast totals to receivables by replacing either exchange rate.

## Campaign schedules and recipient state

A campaign definition contains an ordered collection of message templates and integer delays measured in days. A campaign enrolment links one campaign to a lead, contact or electronic-mail group, an optional sending user and a start date. A normal save rejects a start date before the current date and a campaign with no scheduled entries. The end date is the start date plus the maximum delay.

The recipient must have a usable electronic mail address; contacts use their primary address. Another scheduled or in-progress enrolment for the same campaign and recipient is rejected. The duplicate search keys the recipient identity text and campaign and does not add a recipient-kind discriminator. Therefore matching textual identifiers across two different recipient kinds need an explicit compatibility fixture.

| Time condition | Derived enrolment status |
| --- | --- |
| Current date precedes start | Scheduled |
| Start is reached and current date is no later than end | In progress |
| Current date is later than end | Completed |
| Lead or contact unsubscribes from this enrolment | Unsubscribed; the daily status refresh excludes it |

The daily sender examines in-progress enrolments and sends entries whose start-plus-delay date equals the current date. It does not automatically catch up entries from an earlier missed day. For a group, recipients are members whose unsubscribe marker is false. For an individual, resolve the recipient address at send time. The chosen template is evaluated against the lead, contact or group record and produces subject and body. Create an outgoing communication linked to the enrolment, then queue delivery linked to that communication.

Communication creation and delivery-queue insertion have a local rollback boundary. A missing campaign or a failed entry is recorded and processing moves to other enrolments or entries. A second scheduler invocation on the same day has no documented deduplication key in this campaign operation; an exactly-once delivery claim requires a separate fixture and queue guarantee. Recording a queued communication is not proof of external delivery.

For group unsubscribe, change the member's unsubscribe marker and leave the enrolment active for other members. For lead/contact unsubscribe, mark the enrolment unsubscribed. A general save recalculates date status, whereas the daily updater expressly excludes unsubscribed records; preserving unsubscribe through edits must be tested rather than inferred from the daily rule alone.

Example: an enrolment starting 10 September with delays zero, three and seven ends 17 September. It is in progress on 17 September, completed on 18 September, and an entry missed on 13 September is not selected by a 14 September run.

## Data enrichment and linked commercial work

Selecting an already enriched organisation fills empty compatible opportunity fields and preserves values the user already supplied. New opportunities can schedule background enrichment from a website. Enrichment is best effort and must not prevent the ordinary opportunity save merely because an external provider fails. Keep the provider result, requested record, matched organisation and run outcome separately from authoritative customer accounting identity.

Notes, reminders, calls and communication history attach to the commercial identity and can follow a conversion through explicit linkage. Their ownership and completion are not quotation approval or customer credit authority. A call-log event can contribute a contact activity; it is not evidence that a promised first response has fulfilled the service deadline until the [response policy](service-and-support.md#conversation-first-and-rolling-response) records the qualifying communication-state event.

## Accounting and cancellation acceptance

For a customer order of two packs at 90 per pack, the immediate financial-ledger change from order submission is zero even though twelve stock units can be reserved. A later submitted customer invoice has its own net, tax, receivable and optional stock effects. A received payment has separate cash/bank and receivable allocation effects. A return or credit note refers to the invoiced or delivered quantities and invokes the corresponding reversal policy; changing the negotiating opportunity back to open does not reverse any of these documents.

The acceptance catalog includes full-discount and forecast-fallback cases, lost-category forecast arithmetic, conversion identity rules, contact-primary constraints, campaign date boundaries and customer/company eligibility. Runtime acceptance must additionally exercise two simultaneous conversions, a stale quote-to-order command, cancellation with submitted downstream documents, and permission changes between list display and command execution.
