# Customer relationships and sales

## Purpose and record boundaries

The commercial journey begins with an interested person or organisation, progresses through qualification and negotiation, and produces an accepted commercial document. A lead, a person, an organisation, an opportunity, and a customer are different business identities. Conversion preserves the lead and creates or associates the identities required for the next operation. A salesperson winning an opportunity does not itself recognise revenue, consume stock, create a receivable, or settle an invoice.

Use one shared contact model for people, one organisation model for institutional identity, and a customer role for the party to whom goods or services are sold. Contacts have child collections of electronic mail addresses and telephone numbers, with primary selections. An organisation holds its name, website, territory, industry, annual revenue, and employee-count range. A commercial opportunity holds the organisation reference, lead origin, one or more contacts, salesperson, expected and actual commercial value, currency, expected closure date, closure date, proposed products, stage history, and communication response measurements. Do not use a telephone number as an unconditional person-identity key: a household or office can share it. Evidence: `source-artifact-3e53fa8646ba204bfd0a lines 80–580`.

The combined model needs separate dimensions for qualification stage, commercial outcome, conversion state, communication state, and sales-document progress. Configurable stage labels have a category of open, ongoing, on hold, won, or lost, along with display order and colour. Commercial stages may have a default probability. Sales-document progress also distinguishes an open enquiry, one with a quotation, a converted enquiry, a lost enquiry, a replied enquiry, and a closed enquiry. Preserve these dimensions; a display label such as “qualified” must not replace evidence that a customer or order has actually been created. Evidence: `source-artifact-ada15f8badc2d24cb1ea lines 1–103`. Evidence: `source-artifact-db51d4e92cfc5adb3c9c lines 1–110`. Evidence: `source-artifact-823ef89edfc8e53d4250 lines 120–351`.

## Lead capture and validation

A lead display name is assembled from the available salutation, first name, middle name, and last name. When the person name is absent, an organisation name supplies the display name; an electronic mail address may supply its local part. The title prefers organisation name over person name. Normal interactive creation must reject a lead without the required identifying information. The business interface must distinguish required capture fields from fallback name derivation used by import and other controlled creation paths.

Validate electronic mail syntax, and reject a lead whose electronic mail address equals its assigned owner's account address. Lead duplication by electronic mail is a configurable policy in the sales document journey. The contact reuse operation during opportunity conversion looks up a contact by electronic mail; merely matching a telephone number does not reuse a contact. These are separate checks: allowing duplicate leads does not authorise duplicate contact creation during conversion. Evidence: `source-artifact-1b4692a1fea404f1b0ba lines 90–255`. Evidence: `source-artifact-7e671e38f4b1580c04af lines 280–364`.

A new lead defaults to the configured initial qualification stage, preferring the seeded initial stage when it exists. A lost stage requires a loss reason. The general “other” reason additionally requires explanatory notes. The lead retains a stage-change history. A stage movement and a conversion are separate operations because conversion also creates linked records, changes the converted marker, transfers assignments, and affects the working list.

## Conversion contract

The conversion command accepts a lead identifier, optional existing contact identifier, optional existing organisation identifier, and optional opportunity values. It requires write permission on the lead, except for a trusted internal creation path with an explicit permission bypass. The resulting opportunity identifier is the command result.

The operation marks the lead converted and, when the corresponding configuration exists, moves it to the qualified label and marks its communication replied. Contact resolution first honours an explicitly supplied contact; otherwise it reuses a contact with matching electronic mail or creates a contact. Reuse refreshes selected lead contact details from the existing contact. New contact creation preserves name, salutation, gender, job title, organisation text, image, electronic mail, and primary telephone selections. Organisation resolution similarly honours an explicit association, otherwise reuses a matching organisation name or creates an organisation using its captured commercial attributes. Evidence: `source-artifact-3e53fa8646ba204bfd0a lines 80–580`.

The new opportunity references the original lead and contact. Copy compatible business fields, mapping lead owner to opportunity owner. Do not copy record identity, creation and modification metadata, submission state, stage, primary contact projections, response policy identity, or stage history as if they were fresh business inputs. Matching custom fields can transfer by identical field identity; otherwise a custom field transfers only when there is exactly one destination custom field with the same label and value kind. An ambiguous pair of matching labels must not be guessed.

When the lead has already received a first response, transfer its response clock origin, response deadline, response result, communication state, first-response duration, and first-response timestamp. This is a conditional preservation rule, not an unconditional reset or unconditional copying of all response state. Additional assigned users are transferred to the opportunity. The inspected conversion function does not establish an explicit guard that makes repeated conversion calls return one existing opportunity; any claim of retry-safe conversion requires a separate completed acceptance check. Evidence: `source-artifact-3e53fa8646ba204bfd0a lines 80–580`.

## Ownership, sharing, and contact projections

An owner assignment is not merely a label. Changing the lead or opportunity owner grants write sharing to that user and removes other direct shares through the inspected owner-management operation. Adding an assignment makes its recipient the current owner, even when an earlier owner existed. Cancelling any assignment clears the single owner field, including cancellation of one of several co-assignees. The assignment operation also creates an in-application notification. Direct assignment creation requires write access to the referenced lead or opportunity. These consequences must be visible in permission and event acceptance scenarios. Evidence: `source-artifact-a8229ab8012c838746d7 lines 1–90`.

For an opportunity with exactly one contact, select that contact as primary automatically. Reject multiple primary contacts. With no primary contact, clear the opportunity's electronic mail, mobile telephone, and telephone projections. Selecting a primary contact trims those projected values. Updating a contact propagates its current primary electronic mail and mobile telephone values to linked opportunities where the contact is primary. Contact editing requires contact write permission, and fetching contact details through an opportunity must honour opportunity read permission. Evidence: `source-artifact-db8bdef1a4a17da375a2 lines 79–317`. Evidence: `source-artifact-621e8e26176dd7b99362 lines 1–145`. Evidence: `source-artifact-117f1eb8c12bde2d5816 lines 438–521`.

## Monetary calculations and forecasts

Product suggestions are commercial estimates. Each row has a quantity, rate, amount, discount percentage, discount amount, and net amount. The standard interactive calculations are:

| Output | Calculation |
| --- | --- |
| Product amount | Quantity multiplied by rate |
| Product discount amount | Product amount multiplied by discount percentage divided by 100 |
| Product net amount | Product amount minus product discount amount |
| Opportunity product total | Sum of product amounts |
| Opportunity product net total | Sum of product net amounts; when no net amounts and no discount are present, use product total |

A 100 percent discount must produce a genuine zero net total. Do not replace this zero with the gross product total. The interactive product controller explicitly distinguishes an empty net aggregate from a zero caused by a discount. Product-rate responses also guard against a user changing product selection while an earlier lookup is still in progress. These inspected calculations occur in the interactive form machinery; acceptance must separately verify that noninteractive writes enforce the same derived totals before relying on them for authoritative monetary processing. Evidence: `source-artifact-9dbe99a3c18eb4acc088 lines 108–193`.

For a sales enquiry with item rows, quantities must be positive and respect whole-unit requirements. Item amount equals rate multiplied by quantity; company-currency rate and amount equal their transaction-currency values multiplied by the conversion rate. Equal transaction and company currency force a rate of one. Otherwise an absent rate, or a rate of one, triggers a dated exchange-rate lookup. This differs from a freely editable probability-weighted forecast and must remain part of the quotation-preparation contract. Evidence: `source-artifact-823ef89edfc8e53d4250 lines 120–351`.

When forecasting is enabled, expected opportunity value must be nonzero and expected closure date is mandatory. If probability is absent or zero, replace it with the stage default, otherwise zero. Consequently, an explicit zero can be replaced by a nonzero stage default. The automatic expected-value setting updates an existing nonzero expected value from nonzero product net total, otherwise product total. It does not initialise every blank expected value. Moving into a won-category stage sets closure date to the current date. Do not claim this automatically records a final invoice value. Monetary fields covered by the inspected tests reject negative values. Evidence: `source-artifact-db8bdef1a4a17da375a2 lines 79–317`. Evidence: `source-artifact-117f1eb8c12bde2d5816 lines 438–521`.

The monthly forecast report has an unusual current calculation that must remain visible:

| Stage category | Forecast contribution | Actual commercial contribution |
| --- | --- | --- |
| Lost | Expected value multiplied by stored exchange rate | Zero |
| Won | Expected value multiplied by probability divided by 100 and by stored exchange rate | Actual opportunity value multiplied by stored exchange rate |
| Other categories | Expected value multiplied by probability divided by 100 and by stored exchange rate | Zero |

The report groups by expected closure month, includes expected closure dates from twelve months before the current date onward, and optionally filters salesperson. An absent exchange rate is treated as one; absent probability is treated as zero. The function accepts beginning and ending date parameters but its inspected selection uses the twelve-month lower boundary instead. Zero aggregates are converted to blank output. These are source-observed rules, including the lost-opportunity contribution. Excluding lost opportunities from forecast is a plausible alternative policy, but it is a proposed change, not a fact about the reviewed calculation. Evidence: `source-artifact-9947effccf4036a33db7 lines 776–835`.

## Quotation, commitment, and accounting boundary

An opportunity may originate from a lead, prospect organisation, or existing customer. An incoming electronic mail address can resolve an existing customer through a contact, otherwise an existing lead, otherwise a newly created lead. Creating an opportunity from a lead links open activities and, when enabled, carries communications and comments forward. Declaring an enquiry lost is rejected while an active submitted quotation exists. Retain multiple loss reasons and competitors for this sales-document operation even though the qualification-stage operation uses a single selected loss reason. Evidence: `source-artifact-823ef89edfc8e53d4250 lines 120–351`.

A quotation validates its expiry date against transaction date, whole-unit quantities, customer identity, and packing composition. It may contain alternative products and, when enabled, zero-quantity rows that communicate a unit price. Quotation order progress compares ordered stock quantities against source row stock quantities. When alternatives exist, the progress calculation considers the alternatives that were actually selected in submitted orders. A quotation is partially ordered while any relevant row is missing or under-ordered; it is ordered when all relevant rows are covered. Evidence: `source-artifact-cccc40bf3c9d3167fd05 lines 143–234`.

An order validates delivery requirements, dates, project/customer compatibility, customer purchase reference, warehouse, direct supplier delivery, reservations, preceding document references, coupon, blanket agreement, and intercompany association. Submission checks customer credit and approving authority, updates reserved quantities, project totals, prior document progress, blanket agreement, coupon usage, and intercompany links. Cancellation removes delivery schedules and reservations, updates linked progress and coupon counts, and rejects a closed order until it is reopened. The sales domain must invoke the inventory and accounting contracts for these consequences; it must not independently invent a second credit or stock ledger. Evidence: `source-artifact-91be43ae56a85a5b24a7 lines 243–289`. Evidence: `source-artifact-91be43ae56a85a5b24a7 lines 514–568`.

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

The inspected conversion and validation tests support several of these behaviours. They were read, not executed in a running application. The scenarios above include additional proposed cross-interface checks; their presence is not evidence of a passing runtime test. Evidence: `source-artifact-d36a609174c165d281d7 lines 1–28`. Evidence: `source-artifact-7e671e38f4b1580c04af lines 280–364`.
