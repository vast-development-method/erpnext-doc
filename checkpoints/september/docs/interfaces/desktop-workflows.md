# Desktop and mobile workspaces

## Observable workspace contract

The application must expose business records through searchable lists, filtered views, grouping, stage boards, detail forms, linked-record panels, activities, comments, assignments, and reports. The same underlying record identity and permissions must survive movement between these surfaces. A board card is not a second opportunity record; changing a stage from a board must invoke the stage validation, history, forecasting, and service effects described in the domain contracts.

The record-list metadata service provides sortable business fields and common fields such as identity, created time, modified time, modifying user, and owner. Filterable and groupable fields are curated by value kind. A record controller may explicitly exclude fields from filtering. Quick filters and persisted views are configurable. Stored views are retrieved for the current user and globally shared views; another user's private saved view is not automatically included. A saved view controls presentation and selected filters; it does not grant row or field access. The [permission fixtures](../runtime/identity-permissions-and-tenancy.md#permission-fixtures-with-explicit-expected-results) must hold when the same record is reached from a list, board, or form.

## Salesperson path

1. Open the lead list, choose a saved view or quick filters, and inspect name, organisation, contact channels, stage, owner, and last modification.
2. Create a lead using person and organisation information, then save with validation errors tied to the relevant fields.
3. Open the detail record and record notes, communications, activities, products, ownership, and stage changes.
4. Convert the lead by selecting an existing or newly created contact and organisation. After success, navigate to the opportunity that retains the source lead reference.
5. On the opportunity, manage primary contact, expected value, currency, probability, expected closure, actual commercial outcome, loss reasons, and service response history.
6. Prepare a sales quotation or customer commitment through the commercial document workflow; continue through fulfilment and invoicing using the respective business services.

The inspected browser conversion test creates a lead, activates conversion in the lead page, and checks that an opportunity exists with its electronic mail address. It does not prove conversion idempotency, duplicate prevention under concurrency, every field transfer, or cross-role permission isolation. The detailed source tests and domain acceptance fixtures must supply those guarantees. The conversion result must retain the source lead relationship and the selected contact and organisation identities. The [customer relationships specification](../domains/customer-relationships-and-sales.md) defines the authoritative business conversion.

## Bulk actions and feedback

The inspected list provides bulk value editing, assignment, clearing assignments, deletion with linked-record review, and lead conversion. Conversion prompts for the selected count and issues a separate command for each selected lead. Success reloads the list and clears selection. This is a collection of independent operations rather than a demonstrated all-or-nothing batch transaction. A replacement should explicitly communicate per-record success and failure so that the operator can distinguish completed items from items requiring retry. That clearer outcome presentation is a proposed improvement when the source interface only presents individual success notifications.

Before deletion, show linked-record information appropriate to the selected scope. Distinguish deleting one record with its linked-record review from deleting multiple records. Changing owner through a bulk assignment must preserve the ownership, sharing, notification, and assignment semantics; it must not update a visible owner label while leaving security state behind. The [service partial-success example](service-contracts.md#partial-success-example) defines why a completed item must remain distinguishable from a failed item requiring retry.

## Product editing and asynchronous lookups

The product grid recalculates quantity multiplied by rate, discount amount, and net amount when the relevant field changes. It updates document totals after row addition, deletion, quantity changes, and discount changes. A 100 percent discount remains a zero net value. A product detail lookup captures the selected product and ignores a response if the row has changed product before the response returns. This protects the user from a stale asynchronous response overwriting their current selection. It is an observable consistency requirement even when the replacement uses entirely different interface machinery. The [draft and connection recovery contract](#draft-editing-and-connection-recovery) requires matching each asynchronous product response to the current row selection before applying it.

The contextual product-rate lookup first resolves the customer's default price list, otherwise the default selling list, using the stock unit and current transaction date. The final product detail response selects the contextual rate when nonzero, otherwise catalogue standard rate. A deliberately zero contextual price is therefore treated as a fallback case in that response, even though the product mirror preserves a zero price-list result. This difference requires an explicit zero-price fixture. An explicitly configured zero rate and an absent rate can take different paths. Test the sales-facing fallback and the authoritative transaction pricing action separately.

The authoritative service must also validate the resulting values for remote and imported writes. The fact that a browser recalculates a displayed total does not establish server validation of that total. Treat interface calculation parity and authoritative persistence validation as separate acceptance dimensions.

## Service agent path

Agents open a customer-scoped issue, see its current service promise and timeline, reply or change state, and inspect response and resolution measurements. The interface must distinguish first response due, rolling response due where applicable, resolution due, fulfilled, and failed. A hold is an operational state with a beginning timestamp and accumulated duration, not simply a muted colour. Reopening must display the resulting deadline and clear completed resolution measurements as the contract requires.

A split action can be offered on any timeline communication, including a communication attached through a secondary timeline link. It requests the new subject and communicates that all communications from the selected communication date onward will move. A direct reference to another business document must remain intact if only the issue timeline association is moving. Timeline movement must preserve unrelated direct business references. Service deadlines and reopening consequences follow the [service specification](../domains/service-and-support.md).

## Project and time path

A worker selects a project and task, records a beginning and ending or duration, chooses an activity, and marks the work billable or nonbillable. Show actual hours separately from billing hours. When billing hours exceed actual hours, present a warning while allowing the source-permitted decision. Display billing and costing rates distinctly and indicate the transaction currency. Project or task inconsistencies and time overlap are blocking errors when their rules apply.

A billing operator selects unbilled submitted time, creates a customer invoice, and sees the remaining billable amount and hours afterwards. Project managers choose the completion calculation method and see actual time, billable time, orders, invoiced amounts, labour cost, purchased cost, and material consumption independently. Draft records, submitted records, and financial completion must have unambiguous labels. The [project and time specification](../domains/projects-and-time-billing.md) defines the actual-hours, billing-hours, costing, and invoice progress measures that every workspace must display consistently.

## Public capture and booking

Lead and opportunity forms collect a curated set of value kinds. Hidden, read-only, identity, generated display-name, converted marker, response measurement, and external acquisition identity fields are excluded from normal field selection. Relationship selection in an unauthenticated form requires deliberately granted selection permission for the target record kind. Selection permission reveals selectable identities; it is not full document read access. A form editor can choose layout sections and columns without changing the persistent entity model. A public selector supplies only explicitly permitted selectable identities. It must not expose hidden fields or become an unrestricted full-document query.

Appointments created through the portal begin unverified and may open only after electronic mail verification. A verified appointment cannot return to unverified. Manually created appointments cannot use unverified status. Reject past bookings, bookings beyond the configured advance limit, holidays, starts whose entire duration does not fit inside an available slot, and fully occupied slots. Capacity is based on overlapping appointments and configured agent count, with a locking read for concurrent booking decisions. A slot booking decision must account for full duration and concurrent occupancy under its lock; a visually available start time alone does not establish admissible capacity.

## Accessibility and compatibility tests

The replacement acceptance plan should include keyboard operation for lists and forms, persistent readable labels, visible blocking versus nonblocking errors, focus after validation, locale-aware date and number input, accessible status text in addition to colour, responsive narrow-screen layouts, and recovery after connection loss. These are proposed quality requirements, not claims that the inspected source already proves every accessibility or offline capability.

Observed source checks cover list metadata, bulk operation wiring, product recalculation, conversion, service split, timesheet validation, and appointment constraints. Full screen inventory, mobile interactions, accessibility conformance, and automated execution of the browser suite remain unverified in this review.

## Distribution operator workflow contract

The following workflow consolidates the domain requirements into one operator path. It defines the necessary business information and action boundaries without prescribing screen layout.

| Operator step | Required information | Authoritative action and result |
| --- | --- | --- |
| Select commercial party | Party role, company, addresses, currency, payment terms, applicable restrictions | Resolve valid party and company defaults |
| Select product and unit | Stock identity, size variant, commercial unit, conversion factor, warehouse | Resolve the selected product's actual conversion and availability |
| Enter commitment | Ordered quantities, rates, discounts, taxes, dates, source references | Save draft, then approve and submit under commercial rules |
| Reserve or pick | Eligible source rows, requested units, available stock, serial/batch choices | Create the permitted reservation or picking facts |
| Receive or dispatch | Actual quantities, accepted/rejected split, source-row allocation, location | Submit physical execution and its stock/valuation consequences |
| Invoice | Delivered or ordered source rows, remaining billable quantity, taxes, currency, due schedule | Submit obligation and accounting consequences |
| Settle | Outstanding amount, advances, account currency, allocation, deductions | Submit payment or reconciliation with balanced accounting effects |
| Correct | Original transaction, downstream dependants, return reason, reversal date | Invoke return, cancellation, amendment, or other explicit correction service |

Show commercial and stock quantities together wherever conversion can change interpretation. Five packs of six must visibly resolve to thirty stock units. When selecting another size variant, preserve the distinction between a changed stock identity and merely changing its display label. A scan of a barcode is product/unit selection evidence; it does not automatically authorize exceeding a remaining order quantity or allocating an unrelated batch.

## Financial reviewer workflow

A reviewer must be able to inspect the transaction header and rows, base and transaction currency totals, tax calculations, selected accounts and dimensions, source-document lineage, settlements, and applicable stock effects. Submission, cancellation, and amendment are separate actions with their actual availability derived from permissions and current state.

After a successful posting, provide navigation to its retained accounting and applicable stock facts. After a blocked cancellation, preserve the original posted state and display the blocking dependant or business condition that the user is permitted to see. After an accepted queued submission, show queued status and lock feedback until completion is verified by a current read. A success toast from queue acceptance must not label the invoice financially posted.

## Workforce operator workflow

An employee-facing view permits the employee to enter the allowed leave, attendance correction, time, expense, or benefit request and inspect its approval state. A manager sees the applicable approval tasks and eligible transitions. Payroll and financial users separately prepare salary statements, review earnings and deductions, create accruals, and pay employees according to their own permissions.

The displayed employee identity, acting login, expense claimant, approver, and settlement party are distinct roles even when one person occupies several of them. Masked salary or bank fields must not become visible through a linked-record panel, downloaded report, or list column. A leave request's approval status is distinct from its attendance effect, entitlement movement, and payroll treatment.

## Draft editing and connection recovery

The form retains its originally read modification time and supplies it when stale-edit detection is intended. On conflict, show that another committed edit exists and reload or explicitly merge business changes; do not automatically replay a financial submission with a different version. A product lookup response must still correspond to the selected row's current product before applying returned rates, units, or descriptions.

A lost response is an uncertain outcome. On reconnection, read the identified document or tracked operation before repeating create, submit, payment, or cancellation. There is no universal generic financial idempotency guarantee. Ordinary unsaved calculations can be repeated when their own contract is read-only; the same must not be assumed for a similarly named mutating command.

## End-to-end acceptance journey

Use an ordinary restricted user to enter a two-row order for one product in two units, receive only the first row partially, invoice the accepted portion, allocate a partial payment, and inspect outstanding values. Confirm unit labels, factor, stock quantity, rate currency, row lineage, and current business state at every step. Attempt a stale edit, an unauthorized company change, a submitted monetary-field change, and a cancellation with a submitted dependant. Each failure must preserve the authoritative business facts and provide a readable path to correction.

The [service matrix](service-contracts.md#operation-contract-matrix), [permission fixtures](../runtime/identity-permissions-and-tenancy.md#permission-fixtures-with-explicit-expected-results), and [report contracts](reporting-and-exports.md) define the server behavior behind this journey. The desktop or mobile client is an alternate presentation of that contract, not an independent accounting engine.
