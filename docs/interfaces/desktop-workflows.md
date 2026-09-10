# Desktop and mobile workspaces

## Observable workspace contract

The application must expose business records through searchable lists, filtered views, grouping, stage boards, detail forms, linked-record panels, activities, comments, assignments, and reports. The same underlying record identity and permissions must survive movement between these surfaces. A board card is not a second opportunity record; changing a stage from a board must invoke the stage validation, history, forecasting, and service effects described in the domain contracts.

The record-list metadata service provides sortable business fields and common fields such as identity, created time, modified time, modifying user, and owner. Filterable and groupable fields are curated by value kind. A record controller may explicitly exclude fields from filtering. Quick filters and persisted views are configurable. Stored views are retrieved for the current user and globally shared views; another user's private saved view is not automatically included. Evidence: `source-artifact-7132868a22d900268d75 lines 23–179`. Evidence: `source-artifact-e19f2d633c7dec69999e lines 1–16`.

## Salesperson path

1. Open the lead list, choose a saved view or quick filters, and inspect name, organisation, contact channels, stage, owner, and last modification.
2. Create a lead using person and organisation information, then save with validation errors tied to the relevant fields.
3. Open the detail record and record notes, communications, activities, products, ownership, and stage changes.
4. Convert the lead by selecting an existing or newly created contact and organisation. After success, navigate to the opportunity that retains the source lead reference.
5. On the opportunity, manage primary contact, expected value, currency, probability, expected closure, actual commercial outcome, loss reasons, and service response history.
6. Prepare a sales quotation or customer commitment through the commercial document workflow; continue through fulfilment and invoicing using the respective business services.

The inspected browser conversion test creates a lead, activates conversion in the lead page, and checks that an opportunity exists with its electronic mail address. It does not prove conversion idempotency, duplicate prevention under concurrency, every field transfer, or cross-role permission isolation. The detailed source tests and domain acceptance fixtures must supply those guarantees. Evidence: `source-artifact-d36a609174c165d281d7 lines 1–28`. Evidence: `source-artifact-3e53fa8646ba204bfd0a lines 80–580`.

## Bulk actions and feedback

The inspected list provides bulk value editing, assignment, clearing assignments, deletion with linked-record review, and lead conversion. Conversion prompts for the selected count and issues a separate command for each selected lead. Success reloads the list and clears selection. This is a collection of independent operations rather than a demonstrated all-or-nothing batch transaction. A replacement should explicitly communicate per-record success and failure so that the operator can distinguish completed items from items requiring retry. That clearer outcome presentation is a proposed improvement when the source interface only presents individual success notifications.

Before deletion, show linked-record information appropriate to the selected scope. Distinguish deleting one record with its linked-record review from deleting multiple records. Changing owner through a bulk assignment must preserve the ownership, sharing, notification, and assignment semantics; it must not update a visible owner label while leaving security state behind. Evidence: `source-artifact-3e4d96f4ff443fb3788e lines 1–140`. Evidence: `source-artifact-a8229ab8012c838746d7 lines 1–90`.

## Product editing and asynchronous lookups

The product grid recalculates quantity multiplied by rate, discount amount, and net amount when the relevant field changes. It updates document totals after row addition, deletion, quantity changes, and discount changes. A 100 percent discount remains a zero net value. A product detail lookup captures the selected product and ignores a response if the row has changed product before the response returns. This protects the user from a stale asynchronous response overwriting their current selection. It is an observable consistency requirement even when the replacement uses entirely different interface machinery. Evidence: `source-artifact-9dbe99a3c18eb4acc088 lines 108–193`.

The contextual product-rate lookup first resolves the customer's default price list, otherwise the default selling list, using the stock unit and current transaction date. The final product detail response selects the contextual rate when nonzero, otherwise catalogue standard rate. A deliberately zero contextual price is therefore treated as a fallback case in that response, even though the product mirror preserves a zero price-list result. This difference requires an explicit zero-price fixture. Evidence: `source-artifact-9dbe99a3c18eb4acc088 lines 32–88`.

The authoritative service must also validate the resulting values for remote and imported writes. The fact that a browser recalculates a displayed total does not establish server validation of that total. Treat interface calculation parity and authoritative persistence validation as separate acceptance dimensions.

## Service agent path

Agents open a customer-scoped issue, see its current service promise and timeline, reply or change state, and inspect response and resolution measurements. The interface must distinguish first response due, rolling response due where applicable, resolution due, fulfilled, and failed. A hold is an operational state with a beginning timestamp and accumulated duration, not simply a muted colour. Reopening must display the resulting deadline and clear completed resolution measurements as the contract requires.

A split action can be offered on any timeline communication, including a communication attached through a secondary timeline link. It requests the new subject and communicates that all communications from the selected communication date onward will move. A direct reference to another business document must remain intact if only the issue timeline association is moving. Evidence: `source-artifact-7d1950e0dae5a31dc840 lines 65–218`. Evidence: `source-artifact-a18b25de73c21aa2c3e9 lines 503–756`.

## Project and time path

A worker selects a project and task, records a beginning and ending or duration, chooses an activity, and marks the work billable or nonbillable. Show actual hours separately from billing hours. When billing hours exceed actual hours, present a warning while allowing the source-permitted decision. Display billing and costing rates distinctly and indicate the transaction currency. Project or task inconsistencies and time overlap are blocking errors when their rules apply.

A billing operator selects unbilled submitted time, creates a customer invoice, and sees the remaining billable amount and hours afterwards. Project managers choose the completion calculation method and see actual time, billable time, orders, invoiced amounts, labour cost, purchased cost, and material consumption independently. Draft records, submitted records, and financial completion must have unambiguous labels. Evidence: `source-artifact-8595348130b8e717250e lines 68–285`. Evidence: `source-artifact-8595348130b8e717250e lines 453–500`. Evidence: `source-artifact-fbb290b930b6e27bd40d lines 262–415`.

## Public capture and booking

Lead and opportunity forms collect a curated set of value kinds. Hidden, read-only, identity, generated display-name, converted marker, response measurement, and external acquisition identity fields are excluded from normal field selection. Relationship selection in an unauthenticated form requires deliberately granted selection permission for the target record kind. Selection permission reveals selectable identities; it is not full document read access. A form editor can choose layout sections and columns without changing the persistent entity model. Evidence: `source-artifact-ee09cbbc6fda7e0cec4c lines 19–218`.

Appointments created through the portal begin unverified and may open only after electronic mail verification. A verified appointment cannot return to unverified. Manually created appointments cannot use unverified status. Reject past bookings, bookings beyond the configured advance limit, holidays, starts whose entire duration does not fit inside an available slot, and fully occupied slots. Capacity is based on overlapping appointments and configured agent count, with a locking read for concurrent booking decisions. Evidence: `source-artifact-fd08fea67aed7e9db479 lines 45–134`.

## Accessibility and compatibility tests

The replacement acceptance plan should include keyboard operation for lists and forms, persistent readable labels, visible blocking versus nonblocking errors, focus after validation, locale-aware date and number input, accessible status text in addition to colour, responsive narrow-screen layouts, and recovery after connection loss. These are proposed quality requirements, not claims that the inspected source already proves every accessibility or offline capability.

Observed source checks cover list metadata, bulk operation wiring, product recalculation, conversion, service split, timesheet validation, and appointment constraints. Full screen inventory, mobile interactions, accessibility conformance, and automated execution of the browser suite remain unverified in this review.
